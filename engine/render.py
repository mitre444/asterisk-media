"""Produce un video a partir de un guion (spec).

Uso:
  python3 -I engine/render.py videos/<id>/<idioma>.py            render completo
  python3 -I engine/render.py videos/<id>/<idioma>.py --frames   solo cuadros de revision
  python3 -I engine/render.py videos/<id>/<idioma>.py --scene 3  vuelve a dibujar una escena y une todo
"""
import argparse
import importlib.util
import json
import math
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *          # noqa: E402
import scenes as S          # noqa: E402
import scenes2 as S2        # noqa: E402
import illus                # noqa: E402,F401  (registra escenas ilustradas en scenes2)
import tariff               # noqa: E402,F401  (escenas del 014)
import world                # noqa: E402  (mundo que la camara recorre, estandar v3)
import v4                   # noqa: E402  (estilo v4: ladrillo + foco + mostrador, 24 nov.)
import fx                   # noqa: E402
import voice as V           # noqa: E402

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"]


def load_spec(path):
    s = importlib.util.spec_from_file_location("spec", path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.SPEC


def build(spec, out):
    audio, tokens, sents, total = V.synth(spec, out + "/cache")
    cues = {tk["cue"]: tk["start"] for tk in tokens if tk["cue"]}
    nb = len(spec["beats"])
    starts = []
    for bi in range(nb):
        first = next(tk for tk in tokens if tk["beat"] == bi)
        starts.append(0.0 if bi == 0 else max(first["start"] - 0.12, starts[-1] + 0.2))
    scs = []
    for bi, beat in enumerate(spec["beats"]):
        btoks = [tk for tk in tokens if tk["beat"] == bi]
        lcues = {tk["cue"]: tk["start"] for tk in btoks if tk["cue"]}
        fn = getattr(S2, beat["scene"], None) or getattr(S, beat["scene"])
        sc = S.Scene(bi, fn, starts[bi], starts[bi + 1] if bi + 1 < nb else total, dict(cues, **lcues),
                     beat.get("p", {}), btoks, bi == 0, bi == nb - 1)
        sc.lcues, sc.name = lcues, beat["scene"]
        sc.src, sc.src_color = beat.get("src", ""), beat.get("src_color", DIM)
        sc.at = beat.get("at")
        scs.append(sc)
    return audio, tokens, sents, total, cues, scs, build_chunks(tokens)


def draw(t, scs, chunks, total, spec):
    sc = next((s for s in scs if s.t0 <= t < s.t1), scs[-1])
    if spec.get("v4"):
        fr = v4.Frame4(t, spec)
    elif spec.get("world"):
        fr = world.WorldFrame(t, spec, scs, sc)
        fr.lang = spec["lang_tag"]
    else:
        fr = fx.ThemedFrame(t, spec["theme"]) if spec.get("theme") else Frame(t)
    sc.fn(fr, t, sc)
    if spec.get("camera"):
        fr.im = fx.camera(fr.im, t, sc, spec)
        fr.d = ImageDraw.Draw(fr.im)
    if spec.get("hook_timer") and t < scs[0].t1:
        hook_timer(fr, t, scs[0].t1, spec["hook_timer"])
    if not spec.get("v4"):                     # en v4 la marca va en la barra de serie
        watermark(fr, spec["brand"])
    if spec.get("sources_on_screen"):          # estandar v3: las fuentes van en la tarjeta final
        source_tag(fr, sc.src, sc.alpha(t), sc.src_color)
    card = spec.get("sources_card")
    t_card = total - spec.get("card_dur", 1.8)
    if card and t >= t_card:
        (v4 if spec.get("v4") else world).sources_card(fr, t, t_card, card, spec.get("card_title", "SOURCES"))
    elif not spec.get("v4") or spec["v4"].get("captions"):
        captions(fr, t, chunks)
    if spec.get("v4"):
        fr.d.rectangle([0, 0, W * clamp(t / total), 8], fill=v4.RED4)
    else:
        progress(fr, t / total)
    return fr.im


def hook_timer(fr, t, end, cfg):
    """Barra que se vacia mientras se dice el gancho (retencion). cfg: True o dict(y=, color=)."""
    cfg = cfg if isinstance(cfg, dict) else {}
    y, x0, x1, h = cfg.get("y", 1196), 130, W - 130, 32
    rem = clamp(1 - t / max(end, 0.1))
    col = cfg.get("color", (240, 120, 108))
    a = min(1.0, t / 0.15)
    d = fr.d
    d.rounded_rectangle([x0, y - h / 2, x1, y + h / 2], h / 2, fill=(38, 44, 84))
    if rem > 0.005:
        pulse = 1.0 + (0.18 * abs(math.sin(t * 14)) if rem < 0.3 else 0.0)
        hh = h * pulse
        xe = x0 + max(h, (x1 - x0) * rem)
        c = tuple(int(v * a + 38 * (1 - a)) for v in (col if rem >= 0.3 else (255, 70, 90)))
        d.rounded_rectangle([x0, y - hh / 2, xe, y + hh / 2], hh / 2, fill=c)


def frange(scs, total):
    n = int(math.ceil(total * FPS))
    cuts = [int(round(s.t0 * FPS)) for s in scs] + [n]
    return n, [(cuts[i], cuts[i + 1]) for i in range(len(scs))]


def render_scene(i, f0, f1, scs, chunks, total, spec, out):
    path = f"{out}/scenes/scene_{i:02d}.mp4"
    tmp = path.replace(".mp4", ".tmp.mp4")
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-an"] + ENC + [tmp], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        ff.stdin.write(draw(f / FPS, scs, chunks, total, spec).tobytes())
    ff.stdin.close()
    if ff.wait() != 0:
        raise SystemExit(f"ffmpeg fallo en la escena {i}")
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--frames", nargs="?", const="auto")
    ap.add_argument("--scene", type=int, action="append")
    a = ap.parse_args()
    spec = load_spec(a.spec)
    out = os.path.join(os.path.dirname(os.path.abspath(a.spec)), "out_" + spec["lang_tag"])
    os.makedirs(out + "/scenes", exist_ok=True)
    os.makedirs(out + "/frames", exist_ok=True)
    t0 = time.time()
    audio, tokens, sents, total, cues, scs, chunks = build(spec, out)
    print("voz lista: %.1fs de audio en %.0fs" % (total, time.time() - t0))
    for s in sents:
        flag = "" if s["match"] is None or s["match"] >= 0.8 else "   <-- REVISAR, se oyo: " + s["heard"]
        print("  %5.2f-%5.2f anclas %-6s coincide %s  %s%s" % (s["start"], s["end"], s["how"], s["match"], s["display"], flag))
    print("escenas:", [(s.i, round(float(s.t0), 2), round(float(s.t1), 2)) for s in scs])
    json.dump(dict(total=total, cues=cues, scenes=[(s.i, float(s.t0), float(s.t1)) for s in scs]), open(out + "/timing.json", "w"))

    if a.frames:
        if a.frames == "auto":
            ts = []
            for s in scs:
                ts += [s.t0 + 0.55 * (s.t1 - s.t0), s.t1 - 0.22]
            ts = [0.0] + ts
        else:
            ts = [float(x) for x in a.frames.split(",")]
        thumbs = []
        for t in ts:
            im = draw(t, scs, chunks, total, spec)
            im.save(f"{out}/frames/f_{t:06.2f}.png")
            thumbs.append(im.resize((360, 640), Image.LANCZOS))
        cols = 6
        rows = math.ceil(len(thumbs) / cols)
        sheet = Image.new("RGB", (cols * 364 + 4, rows * 644 + 4), (60, 60, 60))
        for i, th in enumerate(thumbs):
            sheet.paste(th, (4 + (i % cols) * 364, 4 + (i // cols) * 644))
        sheet.save(f"{out}/frames/sheet.jpg", quality=88)
        print("cuadros:", [round(t, 2) for t in ts])
        return

    n, ranges = frange(scs, total)
    todo = a.scene if a.scene is not None else list(range(len(scs)))
    for i in todo:
        ts = time.time()
        render_scene(i, ranges[i][0], ranges[i][1], scs, chunks, total, spec, out)
        print("escena %d: %d cuadros en %.0fs" % (i, ranges[i][1] - ranges[i][0], time.time() - ts))
    with open(out + "/scenes/list.txt", "w") as fh:
        for i in range(len(scs)):
            fh.write(f"file 'scene_{i:02d}.mp4'\n")
    silent = out + "/video_sin_audio.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", out + "/scenes/list.txt",
                    "-c", "copy", silent], check=True)
    events = [(s.t0 - 0.10, "whoosh") for s in scs[1:]]
    if spec.get("hook_timer"):
        tt = 0.25
        while tt < scs[0].t1 - 0.1:
            events.append((tt, "tick"))
            tt += 0.5 if tt < scs[0].t1 * 0.7 else 0.25
    for s in scs:
        events += [(s.lcues[c] + off, kind) for c, kind, off in spec.get("sfx", []) if c in s.lcues]
        if s.name in S2.SFX:
            events += S2.SFX[s.name](s)
    music = None
    if spec.get("music"):
        mu = dict(spec["music"])
        cuts = []
        for s in scs:
            if mu.get("cut") in s.lcues:
                nxt = next((z.t0 for z in scs if z.t0 > s.lcues[mu["cut"]]), total)
                cuts.append((s.lcues[mu["cut"]], nxt))
        risers = [s.t0 for s in scs if s.name in mu.get("riser_scenes", [])]
        music = dict(mu, total=total, cuts=cuts, risers=risers, starts=[s.t0 for s in scs])
    loud = V.mix_audio(audio, events, out + "/mezcla.wav", out + "/audio.m4a", music=music)
    final = f"{out}/{spec['id']}_{spec['lang_tag']}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", out + "/audio.m4a", "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "copy", "-movflags", "+faststart", "-shortest", final], check=True)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final],
                               capture_output=True, text=True).stdout.strip())
    print("LISTO %s | %.2fs | %d cuadros | sonoridad de entrada %s LUFS | %.1f MB | total %.0fs"
          % (final, dur, n, loud["input_i"], os.path.getsize(final) / 1e6, time.time() - t0))


if __name__ == "__main__":
    main()

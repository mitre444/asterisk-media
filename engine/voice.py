"""Narracion local (Kokoro), tiempos por palabra y mezcla de sonido.

Marcado de los guiones:
  {dicho|mostrado}   la voz dice "dicho", el subtitulo muestra "mostrado"
  [#nombre]          marca de tiempo: el instante en que empieza la palabra siguiente
"""
import hashlib
import json
import os
import re
import subprocess
import difflib
import numpy as np
import soundfile as sf
import align

MODEL = "/home/claude/models/kokoro/kokoro-v1.0.onnx"
VOICES = "/home/claude/models/kokoro/voices-v1.0.bin"
SR = 24000
TOKEN_RE = re.compile(r"\[#\w+\]|\{[^}]*\}\S*|\S+")
STRIP = "ˈˌ .,;:!?¿¡\"'“”«»—-"

_k = None


def kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro(MODEL, VOICES)
    return _k


def parse(line):
    toks, cue = [], None
    for m in TOKEN_RE.findall(line):
        if m.startswith("[#"):
            cue = m[2:-1]
            continue
        if m.startswith("{"):
            end = m.index("}")
            body, tail = m[1:end], m[end + 1:]
            spoken, disp = body.split("|", 1) if "|" in body else (body, body)
            toks.append(dict(spoken=spoken + tail, display=(disp + tail) if disp else "", cue=cue))
        else:
            toks.append(dict(spoken=m, display=m, cue=cue))
        cue = None
    return toks


def apply_lexicon(s, lex):
    for pat, rep in lex.items():
        s = re.sub(r"(?<![\wáéíóúñ])" + re.escape(pat) + r"(?![\wáéíóúñ])", rep, s)
    return s


def _weight(spoken, lang):
    ph = kokoro().tokenizer.phonemize(spoken, lang)
    n = sum(1 for c in ph if c not in STRIP)
    return 1.0 + n + 0.6 * ph.count("ː")


def _silences(x, sr, min_len=0.07):
    """Silencios internos de una frase: lista de (inicio, fin) en segundos."""
    fr = int(0.01 * sr)
    n = len(x) // fr
    if n < 5:
        return []
    rms = np.sqrt((x[: n * fr].reshape(n, fr) ** 2).mean(axis=1))
    thr = max(0.006, 0.035 * rms.max())
    quiet = rms < thr
    runs, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if i > 2 and j < n - 2 and (j - i) * 0.01 >= min_len:
                runs.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return runs


def _time_tokens(toks, x, sr, lang):
    """Reparte la duracion de la frase entre sus palabras.

    Usa los silencios reales (comas, dos puntos) como anclas cuando coinciden
    con la puntuacion; dentro de cada tramo reparte segun la cantidad de fonemas.
    """
    dur = len(x) / sr
    w = [_weight(t["spoken"], lang) for t in toks]
    marks = [i for i, t in enumerate(toks[:-1]) if t["spoken"][-1] in ",;:—.?!"]
    sil = _silences(x, sr)
    if marks and len(sil) >= len(marks):
        if len(sil) > len(marks):
            keep = sorted(sorted(sil, key=lambda s: s[0] - s[1])[: len(marks)])
        else:
            keep = sil
        segs, a, lo = [], 0.0, 0
        for mi, (s0, s1) in zip(marks, keep):
            segs.append((lo, mi + 1, a, s0))
            a, lo = s1, mi + 1
        segs.append((lo, len(toks), a, dur))
        anchored = True
    else:
        w = [wi + (4.0 if i in marks else 0.0) for i, wi in enumerate(w)]
        segs = [(0, len(toks), 0.0, dur)]
        anchored = not marks
    out = []
    for lo, hi, a, b in segs:
        ws = np.array(w[lo:hi])
        edges = a + np.concatenate([[0], np.cumsum(ws) / ws.sum()]) * (b - a)
        for j in range(hi - lo):
            out.append((edges[j], edges[j + 1]))
    return out, anchored


def _sentence(spoken, spec, cache_dir):
    """Audio de una frase, con cache por contenido (cambiar marcas o textos en pantalla no vuelve a sintetizar)."""
    key = hashlib.sha1(json.dumps([spoken, spec["voice"], spec.get("speed", 1.0), spec["lang"]]).encode()).hexdigest()[:16]
    path = f"{cache_dir}/s_{key}.wav"
    if os.path.exists(path):
        return sf.read(path, dtype="float32")[0]
    x, sr = kokoro().create(spoken, voice=spec["voice"], speed=spec.get("speed", 1.0), lang=spec["lang"])
    x = x.astype(np.float32)
    nz = np.where(np.abs(x) > 0.012)[0]
    x = x[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.06 * sr)]
    sf.write(path, x, SR)
    return x


def _times(toks, x, lang, cache_path):
    """Tiempos por palabra: primero con el reconocedor (anclas reales); si no esta, por silencios y fonemas."""
    dur = len(x) / SR
    if align.available():
        try:
            sig = [[t["spoken"] for t in toks], align.OFFSET]
            if os.path.exists(cache_path) and json.load(open(cache_path)).get("sig") == sig:
                c = json.load(open(cache_path))
                starts, hyp = c["starts"], c["hyp"]
            else:
                starts, hyp, _ = align.token_starts(x, SR, toks)
                json.dump(dict(sig=sig, starts=starts, hyp=hyp), open(cache_path, "w"), ensure_ascii=False)
            st = align.fill(starts, [_weight(t["spoken"], lang) for t in toks], dur)
            heard = [align.norm(w) for w in hyp.split()]
            heard = [w for w in heard if w]
            match = max(difflib.SequenceMatcher(None, [n for n in (align.norm(w) for w in ref.split()) if n], heard, autojunk=False).ratio()
                        for ref in (" ".join(t["spoken"] for t in toks).replace("-", " "), " ".join(t["display"] for t in toks)))
            return list(zip(st, st[1:] + [dur])), "%d/%d" % (sum(v is not None for v in starts), len(toks)), hyp, round(match, 2)
        except Exception as e:      # el video no depende del reconocedor
            print("alineador no disponible para esta frase:", repr(e)[:120])
    times, anchored = _time_tokens(toks, x, SR, lang)
    return times, "A" if anchored else "~", "", None


def synth(spec, cache_dir):
    """Devuelve (audio, tokens, sentences, total)."""
    os.makedirs(cache_dir, exist_ok=True)
    lex = spec.get("lexicon", {})
    t = spec.get("lead", 0.3)
    parts = [np.zeros(int(t * SR), dtype=np.float32)]
    tokens, sentences, si = [], [], 0
    for bi, beat in enumerate(spec["beats"]):
        for li, ln in enumerate(beat["lines"]):
            ln = dict(text=ln) if isinstance(ln, str) else dict(ln)
            last_in_beat = li == len(beat["lines"]) - 1
            pause = ln.get("pause", spec.get("beat_pause", 0.42) if last_in_beat else spec.get("pause", 0.30))
            cap, role = ln.get("cap", True), ln.get("role", "")
            toks = parse(ln["text"])
            for tk in toks:
                tk["spoken"] = apply_lexicon(tk["spoken"], lex)
            spoken = " ".join(tk["spoken"] for tk in toks)
            x = _sentence(spoken, spec, cache_dir)
            akey = hashlib.sha1(json.dumps([spoken, spec["voice"], spec.get("speed", 1.0), spec["lang"]]).encode()).hexdigest()[:16]
            times, how, heard, match = _times(toks, x, spec["lang"], f"{cache_dir}/a_{akey}.json")
            for j, (tk, (a, b)) in enumerate(zip(toks, times)):
                disp = tk["display"]
                tokens.append(dict(display=disp, cdisp=disp.rstrip(".,:;") or disp, spoken=tk["spoken"], cue=tk["cue"],
                                   start=round(float(t + a), 3), end=round(float(t + b), 3), sent=si, beat=bi,
                                   cap=cap, role=role, last=j == len(toks) - 1))
            dur = len(x) / SR
            sentences.append(dict(i=si, beat=bi, start=round(t, 3), end=round(t + dur, 3), spoken=spoken,
                                  display=" ".join(tk["display"] for tk in toks if tk["display"]), how=how, heard=heard, match=match))
            parts += [x, np.zeros(int(pause * SR), dtype=np.float32)]
            t += dur + pause
            si += 1
    total = round(sentences[-1]["end"] + spec.get("tail", 0.7), 3)
    audio = np.concatenate(parts)
    need = int(total * SR)
    audio = audio[:need] if len(audio) >= need else np.concatenate([audio, np.zeros(need - len(audio), dtype=np.float32)])
    sf.write(f"{cache_dir}/voice.wav", audio, SR)
    json.dump(dict(tokens=tokens, sentences=sentences, total=total), open(f"{cache_dir}/voice.json", "w"), ensure_ascii=False)
    return audio, tokens, sentences, total


# ---------- efectos (sintetizados; nada de archivos de terceros) ----------
def _whoosh(dur=0.34):
    n = int(SR * dur)
    x = np.random.default_rng(7).standard_normal(n)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X *= np.exp(-((np.log(f + 1.0) - np.log(1400.0)) ** 2) / (2 * 0.55 ** 2))
    y = np.fft.irfft(X, n) * np.sin(np.linspace(0, np.pi, n)) ** 2
    return y / np.abs(y).max()


def _pop():
    n = int(SR * 0.09)
    tt = np.arange(n) / SR
    f = 880 * np.exp(-tt * 9)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 45)
    return y / np.abs(y).max()


def _ding():
    n = int(SR * 0.9)
    tt = np.arange(n) / SR
    y = (np.sin(2 * np.pi * 1318.5 * tt) + 0.6 * np.sin(2 * np.pi * 1975.5 * tt) + 0.3 * np.sin(2 * np.pi * 2637 * tt))
    y *= np.exp(-tt * 5.5) * np.minimum(1, tt / 0.004)
    return y / np.abs(y).max()


def _thump():
    n = int(SR * 0.26)
    tt = np.arange(n) / SR
    f = 55 + 45 * np.exp(-tt * 18)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 14)
    return y / np.abs(y).max()


def _tick():
    n = int(SR * 0.05)
    tt = np.arange(n) / SR
    x = np.random.default_rng(3).standard_normal(n)
    x = np.diff(np.concatenate([[0], x]))
    y = x * np.exp(-tt * 140) + 0.6 * np.sin(2 * np.pi * 2600 * tt) * np.exp(-tt * 90)
    return y / np.abs(y).max()


def _cash():
    n = int(SR * 0.6)
    tt = np.arange(n) / SR
    y = 0.7 * np.sin(2 * np.pi * 2093 * tt) * np.exp(-tt * 7) + 0.5 * np.sin(2 * np.pi * 3136 * tt) * np.exp(-tt * 9)
    y *= np.minimum(1, tt / 0.003)
    x = np.random.default_rng(5).standard_normal(n)
    y[: int(SR * 0.08)] += 0.5 * np.diff(np.concatenate([[0], x]))[: int(SR * 0.08)] * np.exp(-tt[: int(SR * 0.08)] * 50)
    return y / np.abs(y).max()


def _boom():
    n = int(SR * 1.1)
    tt = np.arange(n) / SR
    f = 42 + 70 * np.exp(-tt * 16)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 4.5)
    x = np.random.default_rng(9).standard_normal(n)
    X = np.fft.rfft(x)
    X *= np.exp(-np.fft.rfftfreq(n, 1 / SR) / 900)
    nz = np.fft.irfft(X, n)
    y += 0.5 * nz / np.abs(nz).max() * np.exp(-tt * 6)
    return y / np.abs(y).max()


def _glitch():
    n = int(SR * 0.32)
    rng = np.random.default_rng(13)
    y = np.zeros(n)
    i = 0
    while i < n:
        L = int(SR * rng.uniform(0.008, 0.03))
        f = rng.uniform(200, 3000)
        tt = np.arange(min(L, n - i)) / SR
        y[i:i + len(tt)] = np.sign(np.sin(2 * np.pi * f * tt)) * rng.uniform(0.3, 1)
        i += L + int(SR * rng.uniform(0, 0.01))
    return y * np.linspace(1, 0.2, n)


SFX = {"whoosh": (_whoosh, 0.040), "pop": (_pop, 0.050), "ding": (_ding, 0.060), "thump": (_thump, 0.11),
       "tick": (_tick, 0.05), "cash": (_cash, 0.07), "boom": (_boom, 0.16), "glitch": (_glitch, 0.05)}


# ---------- musica de tension (generada aqui, sin derechos de terceros) ----------
CHORDS = [  # la menor, fa, do, sol
    [110.0, 164.81, 220.0, 261.63], [87.31, 130.81, 174.61, 220.0],
    [130.81, 196.0, 261.63, 329.63], [98.0, 146.83, 196.0, 246.94]]


def make_music(total, bpm=94, cuts=(), risers=(), starts=(), **_):
    n = int(total * SR)
    tt = np.arange(n) / SR
    beat = 60.0 / bpm
    bar = beat * 4
    out = np.zeros(n)
    # colchon armonico: acordes por compas, con cruce suave
    pad = np.zeros(n)
    nb = int(total / bar) + 2
    for b in range(nb):
        ch = CHORDS[b % 4]
        i0, i1 = int(b * bar * SR), int((b + 1) * bar * SR + 0.3 * SR)
        i0, i1 = max(0, i0), min(n, i1)
        if i0 >= n:
            break
        t_ = tt[i0:i1] - b * bar
        env = np.minimum(1, t_ / 0.25) * np.minimum(1, np.maximum(0, (bar + 0.3 - t_) / 0.3))
        seg = np.zeros(i1 - i0)
        for f in ch:
            for h in range(1, 6):
                seg += np.sin(2 * np.pi * f * h * t_ * (1 + 0.0015 * (h % 2))) / (h * 1.4)
        pad[i0:i1] += seg * env
    lfo = 0.75 + 0.25 * np.sin(2 * np.pi * tt / (bar * 2))
    out += 0.16 * pad / max(1e-6, np.abs(pad).max()) * lfo
    # bombo en 1 y 3, bajo en cada tiempo, tic en corcheas
    kick_len = int(SR * 0.22)
    kt = np.arange(kick_len) / SR
    kick = np.sin(2 * np.pi * np.cumsum(45 + 80 * np.exp(-kt * 30)) / SR) * np.exp(-kt * 16)
    hat_len = int(SR * 0.03)
    ht = np.arange(hat_len) / SR
    hn = np.random.default_rng(1).standard_normal(hat_len)
    hat = np.diff(np.concatenate([[0], hn])) * np.exp(-ht * 160)
    nbeats = int(total / beat) + 1
    for k in range(nbeats):
        i = int(k * beat * SR)
        if i >= n:
            break
        root = CHORDS[(k // 4) % 4][0]
        bl = min(n - i, int(SR * beat * 0.9))
        bt = np.arange(bl) / SR
        out[i:i + bl] += 0.22 * (np.sin(2 * np.pi * root * bt) + 0.35 * np.sin(4 * np.pi * root * bt)) * np.exp(-bt * 5)
        if k % 2 == 0:
            j = min(n, i + kick_len)
            out[i:j] += 0.55 * kick[: j - i]
        for half in (0, 0.5):
            ii = int((k + half) * beat * SR)
            if ii < n:
                j = min(n, ii + hat_len)
                out[ii:j] += (0.10 if half == 0 else 0.06) * hat[: j - ii]
    # subidas antes de escenas clave
    for r in risers:
        L = int(1.4 * SR)
        i1 = int(r * SR)
        i0 = max(0, i1 - L)
        if i1 <= 0:
            continue
        rt = np.arange(i1 - i0) / SR
        u = rt / max(1e-6, rt[-1]) if len(rt) else rt
        x = np.random.default_rng(2).standard_normal(len(rt))
        x = np.diff(np.concatenate([[0], x]))
        sw = np.sin(2 * np.pi * np.cumsum(180 + 900 * u ** 2) / SR)
        out[i0:i1] += (0.18 * x + 0.12 * sw) * u ** 2
    # silencios (corte dramatico) con microfundidos
    for a, b in cuts:
        i0, i1 = int(a * SR), int(b * SR)
        f = int(0.02 * SR)
        out[max(0, i0 - f):i0] *= np.linspace(1, 0, min(f, i0))
        out[i0:i1] = 0
        if i1 < n:
            out[i1:i1 + f] *= np.linspace(0, 1, min(f, n - i1))
    # salida
    fo = int(1.4 * SR)
    out[-fo:] *= np.linspace(1, 0, fo)
    return out / max(1e-6, np.abs(out).max())


# ---------- musica con ritmo (estandar v3, 22 nov.: principio A4 del doc 09) ----------
GROOVE = [  # do, sol, la menor, fa (mayor, ligero)
    [130.81, 164.81, 196.0, 261.63], [98.0, 146.83, 196.0, 246.94],
    [110.0, 164.81, 220.0, 261.63], [87.31, 130.81, 174.61, 220.0]]


def make_groove(total, bpm=112, cuts=(), risers=(), starts=(), **_):
    """Beat ligero y brillante: bombo suave en cada tiempo, palmada en 2 y 4, hi-hat a contratiempo,
    arpegio pulsado en corcheas y bajo en la raiz. Nada de colchon de tension."""
    n = int(total * SR)
    beat = 60.0 / bpm
    out = np.zeros(n)
    rng = np.random.default_rng(3)
    kl = int(SR * 0.16)
    kt = np.arange(kl) / SR
    kick = np.sin(2 * np.pi * np.cumsum(50 + 70 * np.exp(-kt * 38)) / SR) * np.exp(-kt * 22)
    cl = int(SR * 0.12)
    ct = np.arange(cl) / SR
    clap = rng.standard_normal(cl) * (np.exp(-ct * 38) + 0.5 * np.exp(-np.maximum(0, ct - 0.012) * 40))
    clap = np.diff(np.concatenate([[0], clap]))
    hl = int(SR * 0.035)
    ht = np.arange(hl) / SR
    hat = np.diff(np.concatenate([[0], rng.standard_normal(hl)])) * np.exp(-ht * 140)
    pl = int(SR * beat * 0.45)
    pt = np.arange(pl) / SR
    penv = np.exp(-pt * 9) * np.minimum(1, pt / 0.004)
    nbeats = int(total / beat) + 2
    for k in range(nbeats):
        i = int(k * beat * SR)
        if i >= n:
            break
        ch = GROOVE[(k // 4) % 4]
        j = min(n, i + kl)
        out[i:j] += 0.42 * kick[: j - i]
        if k % 2 == 1:
            j = min(n, i + cl)
            out[i:j] += 0.16 * clap[: j - i]
        hi = int((k + 0.5) * beat * SR)
        if hi < n:
            j = min(n, hi + hl)
            out[hi:j] += 0.09 * hat[: j - hi]
        bl = min(n - i, int(SR * beat * 0.8))
        bt = np.arange(bl) / SR
        root = ch[0] / 2
        out[i:i + bl] += 0.20 * np.sin(2 * np.pi * root * bt) * np.exp(-bt * 4)
        for half in (0, 0.5):                       # arpegio pulsado
            ii = int((k + half) * beat * SR)
            if ii >= n:
                continue
            f = ch[[0, 2, 1, 3, 2, 3, 1, 2][(2 * k + int(half * 2)) % 8]] * 2
            j = min(n, ii + pl)
            tone = np.sin(2 * np.pi * f * pt) + 0.3 * np.sin(4 * np.pi * f * pt) + 0.12 * np.sin(6 * np.pi * f * pt)
            out[ii:j] += 0.10 * (tone * penv)[: j - ii]
    for r in risers:                                 # subida corta y brillante
        L = int(0.9 * SR)
        i1 = int(r * SR)
        i0 = max(0, i1 - L)
        if i1 <= 0 or i1 > n:
            continue
        u = np.linspace(0, 1, i1 - i0)
        out[i0:i1] += 0.10 * np.diff(np.concatenate([[0], rng.standard_normal(i1 - i0)])) * u ** 2
    for a, b in cuts:
        i0, i1 = int(a * SR), int(b * SR)
        f = int(0.02 * SR)
        out[max(0, i0 - f):i0] *= np.linspace(1, 0, min(f, i0))
        out[i0:i1] = 0
        if i1 < n:
            out[i1:i1 + f] *= np.linspace(0, 1, min(f, n - i1))
    fo = int(1.2 * SR)
    out[-fo:] *= np.linspace(1, 0, fo)
    return out / max(1e-6, np.abs(out).max())


def _duck(voice, depth=0.55):
    a = np.abs(voice)
    w = int(0.06 * SR)
    env = np.convolve(a, np.ones(w) / w, mode="same")
    ref = np.percentile(env[env > 1e-4], 90) if np.any(env > 1e-4) else 1.0
    env = np.clip(env / max(1e-6, ref), 0, 1)
    w2 = int(0.25 * SR)
    env = np.convolve(env, np.ones(w2) / w2, mode="same")
    return 1 - depth * np.clip(env * 1.4, 0, 1)


def mix_audio(voice, events, out_wav, final_m4a, music=None):
    """voz + efectos (+ musica con compresion por la voz) -> wav; normaliza a -14 LUFS y codifica AAC."""
    v = voice / max(1e-6, np.abs(voice).max()) * 0.89
    out = v.copy()
    if music:
        m = (make_groove if music.get("style") == "groove" else make_music)(**music)[: len(out)]
        if len(m) < len(out):
            m = np.concatenate([m, np.zeros(len(out) - len(m))])
        out += (music.get("gain", 0.20) * m * _duck(v, music.get("duck", 0.55))).astype(np.float32)
    cache = {}
    for t, kind in events:
        fn, gain = SFX[kind]
        if kind not in cache:
            cache[kind] = fn().astype(np.float32)
        y = cache[kind] * gain
        i = int(t * SR)
        if i < 0 or i >= len(out):
            continue
        j = min(len(out), i + len(y))
        out[i:j] += y[: j - i]
    out = np.clip(out, -0.98, 0.98)
    sf.write(out_wav, out, SR)
    p = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", out_wav, "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = json.loads(p.stderr[p.stderr.rindex("{"): p.stderr.rindex("}") + 1])
    af = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:measured_TP={input_tp}:measured_LRA={input_lra}"
          ":measured_thresh={input_thresh}:offset={target_offset}:linear=true").format(**m)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out_wav, "-af", af, "-ar", "44100", "-ac", "2",
                    "-c:a", "aac", "-b:a", "192k", final_m4a], check=True)
    return m

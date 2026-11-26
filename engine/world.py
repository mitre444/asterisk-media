"""Mundo concreto que la cámara recorre (estándar v3, 22 nov. 2026; principio A3 del doc 09).

En vez del fondo abstracto con partículas, cada video vive en un lugar: una calle ilustrada
en estilo "tarjeta impresa" (mismo trazo que illus.py), más ancha que la pantalla. Cada beat
del guion dice dónde está la cámara (`at=` en píxeles del panorama) y la cámara viaja entre
puntos al cambiar de escena. Las marcas aparecen como lugar (fachada con el nombre en texto),
nunca como logo dibujado.

Uso en el spec:
    world=dict(shops=[dict(kind="games", x=740, w=760, h=600, sign="GAMES", col=CORAL), ...],
               queue=dict(x0=900, n=6, gap=86), billboard=["DAY ONE", "$3.79B*"])
    beats=[dict(scene="w_hook", at=1120, ...), ...]
"""
import math

import numpy as np
from PIL import Image, ImageDraw

from core import *          # noqa: F401,F403
import fx
from fx import put, say, pill, appear, pop, stamp, bill, coin, tfit
import scenes2 as S2
from scenes2 import kick, slam, lc
from illus import Pen, INKC, PAPER, CORAL, NAVY, STEEL, TEALC, LEAF, ORNG, YELC, BROWN, card
from tariff import person_spr, doc_spr

BASE = 1300          # línea de la banqueta (pies de los personajes)
STREET = 1372
SKY = [(0, (18, 16, 52)), (620, (70, 46, 120)), (1100, (226, 116, 124)), (1300, (255, 178, 122))]
_pano = {}


def _sky(pw):
    ys = np.arange(H, dtype=np.float32)
    cols = np.zeros((H, 3), np.float32)
    for c in range(3):
        cols[:, c] = np.interp(ys, [s[0] for s in SKY], [s[1][c] for s in SKY])
    img = np.repeat(cols[:, None, :], pw, axis=1)
    return Image.fromarray(img.astype(np.uint8)).convert("RGBA")


def _windows(p, x0, y0, x1, y1, seed, lit=(255, 214, 120), dark=(64, 70, 120), cw=46, ch=58, gx=30, gy=34):
    rng = np.random.default_rng(seed)
    y = y0
    while y + ch <= y1:
        x = x0
        while x + cw <= x1:
            p.rect(x, y, x + cw, y + ch, lit if rng.random() < 0.45 else dark, r=4, sh=False, out=3)
            x += cw + gx
        y += ch + gy


def _storefront(p, x, w, col, sign, kind):
    b = BASE
    p.rect(x + 30, b - 300, x + w - 30, b - 232, PAPER, r=10, out=5)                 # letrero
    p.txt(x + w / 2, b - 266, sign, 50 if len(sign) < 12 else 40, INKC)
    n = max(6, int((w - 40) / 54))
    sw = (w - 40) / n
    for i in range(n):                                                            # toldo a rayas
        p.poly([(x + 20 + i * sw, b - 222), (x + 20 + (i + 1) * sw, b - 222),
                (x + 12 + (i + 1) * sw, b - 176), (x + 12 + i * sw, b - 176)],
               col if i % 2 == 0 else PAPER, sh=False, out=3)
    p.rect(x + 40, b - 168, x + w - 190, b - 14, (130, 196, 232), r=6, sh=False, out=5)  # vitrina
    p.rect(x + w - 160, b - 168, x + w - 50, b - 4, _dk(col), r=6, sh=False, out=5)       # puerta
    p.ell(x + w - 70, b - 86, 6, 6, YELC, sh=False, out=2)
    gx0, gx1 = x + 40, x + w - 190
    if kind == "games":
        for j in range(int((gx1 - gx0 - 30) / 70)):                               # cajas de juego en la vitrina
            cx = gx0 + 30 + j * 70
            c = [CORAL, TEALC, ORNG, NAVY, LEAF][j % 5]
            p.rect(cx, b - 150, cx + 50, b - 82, c, r=4, sh=False, out=3)
            p.rect(cx + 8, b - 140, cx + 42, b - 118, PAPER, r=2, sh=False, out=2)
        p.rect(gx0 + 20, b - 64, gx1 - 20, b - 18, BROWN, r=4, sh=False, out=4)     # mostrador
        p.rect(gx1 - 120, b - 104, gx1 - 40, b - 64, (60, 62, 90), r=4, sh=False, out=3)  # caja registradora
    elif kind == "screens":
        for j in range(max(1, int((gx1 - gx0) / 170))):
            cx = gx0 + 24 + j * 170
            p.rect(cx, b - 150, cx + 140, b - 60, (34, 40, 80), r=6, sh=False, out=4)
            p.poly([(cx + 58, b - 126), (cx + 58, b - 84), (cx + 92, b - 105)], YELC, sh=False, out=2)
            p.rect(cx + 60, b - 60, cx + 80, b - 30, (60, 62, 90), sh=False, out=3)


def _dk(c, k=0.72):
    return tuple(int(v * k) for v in c)


def panorama(world):
    key = repr(world)
    if key in _pano:
        return _pano[key]
    shops = world["shops"]
    pw = world.get("width", max(s["x"] + s["w"] for s in shops) + 120)
    base = _sky(pw)
    d = ImageDraw.Draw(base)
    rng = np.random.default_rng(5)
    for _ in range(int(pw / 40)):                                                  # estrellas
        x, y, r = rng.uniform(0, pw), rng.uniform(40, 560), rng.uniform(1.2, 2.8)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 240, 220, 255))
    x = -40
    while x < pw:                                                                   # ciudad lejana
        w_ = rng.uniform(120, 260)
        h_ = rng.uniform(220, 460)
        d.rectangle([x, BASE - 120 - h_, x + w_, BASE], fill=(58, 46, 104, 255))
        x += w_ + rng.uniform(-10, 30)
    p = Pen(pw, H, S=1)
    for s in shops:
        x, w, h, col = s["x"], s["w"], s["h"], s.get("col", NAVY)
        top = BASE - h
        p.rect(x, top, x + w, BASE, s.get("wall", _wall(col)), r=10, ht=True, out=6)
        if s["kind"] == "tower":
            p.rect(x + 40, top + 40, x + w - 40, top + 140, PAPER, r=10, out=5)
            p.txt(x + w / 2, top + 90, s["sign"], 64, INKC)
            _windows(p, x + 50, top + 190, x + w - 40, BASE - 60, s["x"], cw=52, ch=64)
            p.rect(x + w / 2 - 90, BASE - 150, x + w / 2 + 90, BASE - 4, (130, 196, 232), r=6, sh=False, out=5)
            continue
        front = s["kind"] in ("games", "screens", "store")
        _windows(p, x + 50, top + 50, x + w - 40, BASE - (330 if front else 60), s["x"])
        if s.get("billboard"):
            bx0, bx1 = x + 40, x + w - 40
            for px in (bx0 + 70, bx1 - 70):
                p.rect(px - 10, top - 120, px + 10, top + 4, (60, 62, 90), sh=False, out=3)
            p.rect(bx0, top - 330, bx1, top - 110, PAPER, r=12, ht=True, out=6)
            lines = s["billboard"]
            for j, ln in enumerate(lines):
                big = j == len(lines) - 1
                sz = tfit(ln, BLACK, 72 if big else 40, bx1 - bx0 - 50)
                p.txt((bx0 + bx1) / 2, top - 290 + j * (200 / max(1, len(lines))) + 40, ln, sz,
                      CORAL if big else INKC)
        if s["kind"] in ("games", "screens", "store"):
            _storefront(p, x, w, col, s["sign"], s["kind"])
    p.rect(0, BASE, pw, STREET, (206, 192, 176), sh=False, out=0)                  # banqueta
    p.ln([(0, BASE), (pw, BASE)], 6)
    p.rect(0, STREET, pw, H, (48, 46, 74), sh=False, out=0)                        # calle
    p.ln([(0, STREET), (pw, STREET)], 8)
    for xx in range(0, int(pw), 220):
        p.rect(xx, 1720, xx + 120, 1736, (230, 196, 90), sh=False, out=0)
    for xx in world.get("crosswalks", []):
        for j in range(6):
            p.rect(xx, STREET + 40 + j * 56, xx + 260, STREET + 70 + j * 56, (220, 216, 226), sh=False, out=0)
    layer = p.im if p.S == 1 else p.im.resize((pw, H))
    base.alpha_composite(layer)
    _pano[key] = (base.convert("RGB"), pw)
    return _pano[key]


def _wall(col):
    return tuple(int(v * 0.55 + 70 * 0.45) for v in col)


QCOLS = [TEALC, CORAL, NAVY, ORNG, LEAF, STEEL, (190, 120, 220)]


class WorldFrame:
    """Mismo contrato que core.Frame (im, d, paste). Recorta el panorama según la cámara del beat actual."""

    def __init__(self, t, spec, scs, sc):
        world = spec["world"]
        pano, pw = panorama(world)
        i = sc.i
        tgt = sc.at if sc.at is not None else pw / 2
        prev = scs[i - 1].at if i > 0 and scs[i - 1].at is not None else tgt
        u = ease_io((t - sc.t0) / 0.8)
        drift = 14 * (t - sc.t0) * (1 if i % 2 == 0 else -1)
        cx = clamp(lerp(prev, tgt, u) + drift, W / 2, pw - W / 2)
        self.left = cx - W / 2
        self.t, self.pw = t, pw
        self.im = pano.crop((int(self.left), 0, int(self.left) + W, H))
        self.d = ImageDraw.Draw(self.im)
        q = world.get("queue")
        self.people = []
        if q:
            for j in range(q["n"]):
                wx = q["x0"] + j * q["gap"]
                bob = 3 * math.sin(t * 3.1 + j * 1.7)
                h = 200 + (j * 23) % 30
                self.people.append((wx, h))
                self.paste(person_spr(h, QCOLS[j % len(QCOLS)]), self.sx(wx), BASE + 6 - h / 2 + bob)

    def sx(self, wx):
        """Coordenada del panorama -> coordenada de pantalla."""
        return wx - self.left

    def paste(self, spr, cx, cy, alpha=1.0):
        if alpha <= 0.004 or spr is None:
            return
        box = (int(round(cx - spr.width / 2)), int(round(cy - spr.height / 2)))
        if alpha >= 0.996:
            self.im.paste(spr, box, spr)
        else:
            m = spr.getchannel("A").point(lambda v: int(v * alpha))
            self.im.paste(spr, box, m)


def _plate(fr, y0, y1, a=0.62):
    """Franja oscura translúcida detrás del texto grande para que se lea sobre el cielo."""
    if a <= 0:
        return
    ov = Image.new("RGBA", (W, int(y1 - y0)), (14, 10, 34, int(255 * a)))
    fr.im.paste(ov, (0, int(y0)), ov)


# ---------- escenas ----------
def w_hook(fr, t, sc):
    """Pregunta completa desde el cuadro 1, sobre el lugar donde pasa la historia."""
    p = sc.p
    x = t - sc.t0
    _plate(fr, 250, 760)
    kick(fr, p["kicker"])
    say(fr, p["q1"], W / 2, 390, 66, WHITE, BLACK, maxw=940)
    say(fr, p["q2"], W / 2, 500, 124, YEL, BLACK, s=0.85 + 0.15 * pop(x, 0.25), glow=(ORNG, 18, 1.2), maxw=960)
    say(fr, p["q3"], W / 2, 606, 76, WHITE, BLACK, s=0.85 + 0.15 * pop(x - 0.06, 0.25), maxw=960)
    q4 = lc(sc, "q", sc.t0 + 0.12)
    if t > q4 - 0.1:
        k = t - q4 + 0.1
        say(fr, p["q4"], W / 2, 700, 56, CORAL, BLACK, a=appear(k, 0.1), s=0.85 + 0.15 * pop(k, 0.25), maxw=960)


S2.SFX["w_hook"] = lambda sc: [(sc.t0 + 0.1, "whoosh")] + ([(sc.lcues["q"], "ding")] if "q" in sc.lcues else [])


def _bar_card(rows, w=900, h=420):
    p = card(w, h)
    p.txt(w / 2, 56, "", 10)
    return p.done(("wbar", w, h, repr(rows)))


def w_board(fr, t, sc):
    """Marcador: dos cifras que no deberían caber (cue a, b) y el remate temprano (cue nb)."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["title"], W / 2, 400, 74, WHITE, BLACK, a=appear(x, 0.1), s=slam(x, 1.3, 0.22), maxw=940)
    spr = _bar_card(p["rows"])
    cy = 720
    put(fr, spr, W / 2, cy, slam(x, 1.2, 0.3), appear(x, 0.12))
    ox, oy = W / 2 - spr.width / 2, cy - spr.height / 2
    vmax = max(r["v"] for r in p["rows"])
    for j, r in enumerate(p["rows"]):
        c = lc(sc, r["cue"])
        if t < c:
            continue
        k = t - c
        yy = oy + 90 + j * 170
        fr.d.text((ox + 50, yy), r["label"], font=font(HEAVY, 34), fill=INKC, anchor="lm")
        bw = max(60, (spr.width - 140) * r["v"] / vmax * ease_out(k / 0.9))
        fr.d.rounded_rectangle([ox + 52, yy + 40, ox + 60 + bw, yy + 110], 18, fill=INKC)
        fr.d.rounded_rectangle([ox + 44, yy + 32, ox + 52 + bw, yy + 102], 18, fill=r["col"], outline=INKC, width=5)
        if k > 0.3:
            fr.d.text((ox + 72, yy + 67), r["val"], font=font(BLACK, 50), fill=INKC, anchor="lm")
    nb = sc.lcues.get("nb")
    if nb is not None and t > nb:
        k = t - nb
        if p.get("stamp_pill"):                                                       # cifra-golpe legible sobre el mundo (009)
            put(fr, pill(p["stamp"], p.get("stamp_size", 96), WHITE, CORAL, 34, 18, BLACK), W / 2, cy + 290,
                slam(k, 2.4, 0.22), appear(k, 0.05), -5)
        else:
            put(fr, stamp(p["stamp"], 66, CORAL), W / 2, cy + 280, slam(k, 2.4, 0.22), appear(k, 0.05), -6)


S2.SFX["w_board"] = lambda sc: ([(sc.lcues[c], s) for c, s in (("a", "pop"), ("b", "pop"), ("nb", "boom"))
                                  if c in sc.lcues])


def _you_tag(fr, wx, h, t, a=1.0):
    sx = fr.sx(wx)
    top = BASE - h - 20
    put(fr, pill("YOU" if fr_lang(fr) == "EN" else "TÚ", 40, INKC, YELC, 24, 12, BLACK), sx, top - 40 + 6 * math.sin(t * 5),
        1.0, a)
    fr.d.polygon([(sx - 16, top - 14), (sx + 16, top - 14), (sx, top + 8)], fill=YELC, outline=INKC)


def fr_lang(fr):
    return getattr(fr, "lang", "EN")


def w_layer(fr, t, sc):
    """Capa N de M (hilo de progreso visible). Título, quién/qué (cue who) y una animación en el mundo (p['anim'])."""
    p = sc.p
    x = t - sc.t0
    _plate(fr, 250, 640, 0.55)
    kick(fr, p["kicker"])
    put(fr, pill(f"{p['n']}/{p['of']}", 44, INKC, YELC, 26, 14, BLACK), X1 - 70, KICK_Y, slam(x, 1.8, 0.22), 1.0, 4)
    say(fr, p["title"], W / 2, 400, 88, WHITE, BLACK, a=appear(x, 0.1), s=slam(x, 1.4, 0.22), maxw=900)
    w_ = sc.lcues.get("who")
    if w_ is not None and t > w_:
        k = t - w_
        put(fr, pill(p["who"], 46, INKC, YELC, 30, 18, BLACK), W / 2, 512, slam(k, 1.9, 0.22), appear(k, 0.05), -2)
        if p.get("who_sub"):
            say(fr, p["who_sub"], W / 2, 584, 32, WHITE, HEAVY, a=appear(k - 0.2, 0.25), maxw=920)
    anim = p.get("anim")
    if anim == "register" and fr.people:
        wx, h = fr.people[-1]
        _you_tag(fr, wx, h, t)
        ph = (t * 0.9) % 1.0
        put(fr, coin(56), fr.sx(wx) + 90 * ease_io(ph) + 20, BASE - h * 0.6 - 80 * math.sin(math.pi * ph), 1.0,
            clamp(ph / 0.1) * clamp((1 - ph) / 0.15))
    elif anim == "split":
        src, dst = p["from_x"], p["to_x"]
        cut = lc(sc, "cut", 1e9)
        for j in range(7):
            ph = (t * 0.5 + j / 7) % 1.0
            peel = t > cut and j % 3 == 0
            ex = src + (dst - src) * (0.35 if peel else 1.0)
            cx = lerp(src, ex, ease_io(ph))
            cy = BASE - 230 - 200 * math.sin(math.pi * ph) + (ph * 200 if peel else 0)
            put(fr, coin(70) if not peel else bill(110, 20), fr.sx(cx), cy, 1.0, clamp(ph / 0.08) * clamp((1 - ph) / 0.12))
        if t > cut:
            k = t - cut
            put(fr, pill(p["cut_txt"], 40, WHITE, CORAL, 26, 14, BLACK), W / 2, 680, slam(k, 1.8, 0.22), appear(k, 0.05), 3)
    elif anim == "stack":
        pre = sc.lcues.get("pre")
        if pre is not None and t > pre:
            k = t - pre
            n = int(ease_out(k / 1.6) * 24)
            for j in range(n):
                r, c = divmod(j, 8)
                put(fr, fx.game_case(64, [CORAL, TEALC, ORNG][r % 3], PAPER), W / 2 - 260 + c * 74, BASE - 50 - r * 92, 1.0, 1.0,
                    (j * 7) % 9 - 4)
            say(fr, p["pre_big"], W / 2, 700, 120, YEL, BLACK, a=appear(k, 0.08), s=slam(k, 1.6, 0.22),
                glow=(ORNG, 18, 1.2), maxw=960)
            if p.get("pre_sub"):
                say(fr, p["pre_sub"], W / 2, 790, 34, WHITE, HEAVY, a=appear(k - 0.2, 0.2), maxw=900)
    if p.get("tag"):
        put(fr, pill(p["tag"], 28, INKC, TEALC), W / 2 + 330, 450, pop(x - 0.4, 0.3))


S2.SFX["w_layer"] = lambda sc: ([(sc.t0 + 0.05, "pop")] + [(sc.lcues[c], s) for c, s in
                                 (("who", "ding"), ("cut", "cash"), ("pre", "pop")) if c in sc.lcues])


def w_note(fr, t, sc):
    """El asterisco del propio documento: comunicado con su nota al pie, que se resalta en el cue est."""
    p = sc.p
    x = t - sc.t0
    _plate(fr, 250, 520, 0.55)
    kick(fr, p["kicker"])
    say(fr, p["title"], W / 2, 400, 80, WHITE, BLACK, a=appear(x, 0.1), s=slam(x, 1.3, 0.22), maxw=940)
    w, h = 860, 520
    key = ("wnote", p["head"], p["line"], p["foot"])
    spr = fx._scache.get(key)
    if spr is None:
        pn = card(w, h)
        pn.rect(40, 40, w - 40, 110, NAVY, r=10, sh=False, out=4)
        pn.txt(w / 2, 75, p["head"], 40, PAPER)
        for j in range(3):
            pn.rect(60, 150 + j * 44, w - 60 - (j * 90), 170 + j * 44, (214, 204, 186), r=6, sh=False, out=0)
        pn.txt(w / 2, 330, p["line"], tfit(p["line"], BLACK, 58, w - 110), INKC)
        pn.ln([(60, 420), (w - 60, 420)], 3)
        pn.txt(70, 460, p["foot"], 32, (90, 84, 110), HEAVY, "lm")
        spr = pn.done(key)
    cy = 820
    put(fr, spr, W / 2, cy, slam(x, 1.2, 0.3), appear(x, 0.12), -1.5)
    est = sc.lcues.get("est")
    if est is not None and t > est:
        k = t - est
        ox, oy = W / 2 - spr.width / 2, cy - spr.height / 2
        a = 0.5 + 0.5 * math.sin(k * 7) ** 2
        fr.d.rounded_rectangle([ox + 50, oy + 430, ox + spr.width - 50, oy + 492], 14, outline=YELC, width=8)
        put(fr, pill(p["est_txt"], 46, INKC, YELC, 30, 18, BLACK), W / 2, cy + 340, slam(k, 1.8, 0.22), appear(k, 0.05), -2)


S2.SFX["w_note"] = lambda sc: [(sc.t0 + 0.05, "whoosh")] + ([(sc.lcues["est"], "boom")] if "est" in sc.lcues else [])


def w_answer(fr, t, sc):
    _plate(fr, 250, 1000, 0.5 if (sc.lcues.get("fol") is None or t < sc.lcues["fol"]) else 0.6)
    S2.answer_cta(fr, t, sc)


S2.SFX["w_answer"] = S2.SFX["answer_cta"]


# ---------- tarjeta final de fuentes (pedido de Mitre, 22 nov.) ----------
def sources_card(fr, t, t0, items, title="SOURCES"):
    k = t - t0
    a = appear(k, 0.18)
    ov = Image.new("RGBA", (W, H), (14, 10, 34, int(235 * a)))
    fr.im.paste(ov, (0, 0), ov)
    fr.d = ImageDraw.Draw(fr.im)
    say(fr, title, W / 2, 520, 84, YEL, BLACK, a=a)
    y = 660
    for it in items:
        say(fr, it, W / 2, y, 42, WHITE, BOLD, a=a, maxw=940)
        y += 80


for _n in ("w_hook", "w_board", "w_layer", "w_note", "w_answer"):
    setattr(S2, _n, globals()[_n])

"""Capa visual v2: fondos tematicos, camara, texto con brillo e iconos.

Todo se compone en RGBA (no se mezcla contra un color fijo), asi que funciona
sobre cualquier fondo. Los sprites estaticos se guardan en cache.
"""
import math
from collections import OrderedDict

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from core import *  # noqa: F401,F403

PINK, TEAL, ORANGE, PURPLE = (255, 70, 170), (70, 230, 225), (255, 150, 60), (150, 90, 255)
INK = (14, 8, 30)

THEMES = {
    "vice": dict(top=(10, 7, 30), mid=(34, 12, 62), low=(98, 26, 104), floor=(9, 5, 22), grid=(255, 60, 170),
                 horizon=1610, sun=True, palms=True),
    "cloud": dict(top=(5, 9, 24), mid=(10, 26, 52), low=(18, 84, 104), floor=(4, 8, 20), grid=(60, 200, 235),
                  horizon=1610, sun=False, palms=False),
    "vault": dict(top=(4, 16, 12), mid=(10, 40, 30), low=(22, 92, 62), floor=(3, 12, 9), grid=(90, 230, 150),
                  horizon=1610, sun=False, palms=False),
    "board": dict(top=(8, 8, 22), mid=(22, 24, 54), low=(70, 72, 140), floor=(6, 6, 16), grid=(150, 160, 255),
                  horizon=1610, sun=False, palms=False),
}


# ---------- cache con limite ----------
class LRU(OrderedDict):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def get2(self, k):
        if k in self:
            self.move_to_end(k)
            return self[k]
        return None

    def put(self, k, v):
        self[k] = v
        if len(self) > self.n:
            self.popitem(last=False)
        return v


_tcache = LRU(600)
_scache = {}


# ---------- fondo ----------
def _gradient(th):
    hz = th["horizon"] / H
    y = np.linspace(0, 1, H)[:, None, None]
    top, mid, low, floor = (np.array(th[k], float) for k in ("top", "mid", "low", "floor"))
    a = np.clip(y / (hz * 0.62), 0, 1)
    b = np.clip((y - hz * 0.62) / (hz * 0.38), 0, 1)
    sky = top * (1 - a) + mid * a
    sky = sky * (1 - b ** 1.6) + low * (b ** 1.6)
    g = np.where(y < hz, sky, floor + (low - floor) * np.exp(-(y - hz) * 30))
    g = np.broadcast_to(g, (H, W, 3)).copy()
    xx = np.linspace(-1, 1, W)[None, :, None]
    g *= (1 - 0.30 * xx ** 2)
    return g


def _sun(th, base):
    r, cx, cy = 235, W / 2, th["horizon"] - 20
    S = 2
    n = int(r * 2 * S)
    yy = np.linspace(0, 1, n)[:, None]
    col = np.array([255, 214, 90.0]) * (1 - yy[..., None]) + np.array([255, 52, 150.0]) * yy[..., None]
    col = np.broadcast_to(col, (n, n, 3))
    m = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(m)
    d.ellipse([0, 0, n - 1, n - 1], fill=255)
    for k in range(7):      # franjas horizontales en la mitad baja
        y0 = n * (0.52 + k * 0.07)
        d.rectangle([0, y0, n, y0 + n * (0.008 + k * 0.006)], fill=0)
    sun = Image.fromarray(col.astype(np.uint8)).convert("RGBA")
    sun.putalpha(m)
    sun = sun.resize((int(r * 2), int(r * 2)), Image.LANCZOS)
    glow = Image.new("RGBA", (int(r * 4), int(r * 4)), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([r * 0.9, r * 0.9, r * 3.1, r * 3.1], fill=(255, 70, 150, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    base.alpha_composite(glow, (int(cx - r * 2), int(cy - r * 2)))
    a = sun.getchannel("A").point(lambda v: int(v * 0.40))
    sun.putalpha(a)
    base.alpha_composite(sun, (int(cx - r), int(cy - r)))


def _palm(d, x, base_y, height, lean, S, col):
    pts_l, pts_r = [], []
    for i in range(21):
        u = i / 20
        px = x + lean * u ** 1.7
        py = base_y - height * u
        w = lerp(30, 12, u) * S / 2
        pts_l.append((px * S - w, py * S))
        pts_r.append((px * S + w, py * S))
    d.polygon(pts_l + pts_r[::-1], fill=col)
    tx, ty = (x + lean) * S, (base_y - height) * S
    for ang, ln in ((-170, 210), (-140, 230), (-105, 190), (-70, 200), (-35, 235), (-5, 215), (-195, 170), (25, 160)):
        a = math.radians(ang)
        top, bot = [], []
        for i in range(17):
            u = i / 16
            r = ln * u * S
            droop = (ln * 0.55 * u * u) * S
            px = tx + math.cos(a) * r
            py = ty + math.sin(a) * r + droop
            w = math.sin(math.pi * min(1, u * 1.15)) * 22 * S / 2 + 1
            nx, ny = -math.sin(a), math.cos(a)
            top.append((px + nx * w, py + ny * w))
            bot.append((px - nx * w, py - ny * w))
        d.polygon(top + bot[::-1], fill=col)
    d.ellipse([tx - 16 * S, ty - 12 * S, tx + 16 * S, ty + 14 * S], fill=col)


def _palms(th, base):
    S = 2
    lay = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    col = (12, 5, 26, 255)
    hz = th["horizon"]
    _palm(d, 70, hz + 10, 420, 70, S, col)
    _palm(d, 175, hz + 10, 300, 40, S, col)
    _palm(d, W - 70, hz + 10, 460, -80, S, col)
    _palm(d, W - 190, hz + 10, 290, -35, S, col)
    base.alpha_composite(lay.resize((W, H), Image.LANCZOS))


_bgs = {}


def theme_base(name):
    if name not in _bgs:
        th = THEMES[name]
        g = _gradient(th)
        base = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).convert("RGBA")
        if th.get("sun"):
            _sun(th, base)
        if th.get("palms"):
            _palms(th, base)
        _bgs[name] = base.convert("RGB")
    return _bgs[name]


_rng = np.random.default_rng(11)
_PART = [dict(x=_rng.uniform(40, W - 40), y=_rng.uniform(0, 1500), v=_rng.uniform(18, 60), s=_rng.uniform(2.0, 5.5),
              ph=_rng.uniform(0, 6.28), c=[PINK, TEAL, WHITE, ORANGE][int(_rng.integers(0, 4))], a=_rng.uniform(0.25, 0.75))
         for _ in range(42)]


class ThemedFrame:
    """Mismo contrato que core.Frame (im, d, paste) con fondo tematico animado."""

    def __init__(self, t, theme):
        th = THEMES[theme]
        self.t, self.theme = t, theme
        self.im = theme_base(theme).copy()
        self.d = ImageDraw.Draw(self.im)
        d, hz = self.d, th["horizon"]
        gc, fl = th["grid"], th["floor"]
        # suelo en perspectiva que avanza
        n = 11
        ph = (t * 0.55) % 1.0
        for k in range(n):
            z = (k + ph) / n
            y = hz + (H - hz) * z ** 2.1
            c = tuple(int(fl[i] + (gc[i] - fl[i]) * (0.18 + 0.7 * z)) for i in range(3))
            d.line([(0, y), (W, y)], fill=c, width=max(1, int(1 + 3 * z)))
        for i in range(-9, 10):
            c = tuple(int(fl[i2] + (gc[i2] - fl[i2]) * 0.55) for i2 in range(3))
            d.line([(W / 2 + i * 14, hz), (W / 2 + i * 300, H + 40)], fill=c, width=2)
        d.line([(0, hz), (W, hz)], fill=(255, 120, 200), width=3)
        # particulas que suben
        for p in _PART:
            y = (p["y"] - p["v"] * t) % 1500 + 40
            x = p["x"] + 14 * math.sin(t * 0.8 + p["ph"])
            tw = 0.6 + 0.4 * math.sin(t * 2.3 + p["ph"] * 3)
            bgc = self.im.getpixel((int(clamp(x, 0, W - 1)), int(y)))
            col = tuple(int(bgc[i] + (p["c"][i] - bgc[i]) * p["a"] * tw) for i in range(3))
            r = p["s"]
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)

    def paste(self, spr, cx, cy, alpha=1.0):
        if alpha <= 0.004 or spr is None:
            return
        box = (int(round(cx - spr.width / 2)), int(round(cy - spr.height / 2)))
        if alpha >= 0.996:
            self.im.paste(spr, box, spr)
        else:
            m = spr.getchannel("A").point(lambda v: int(v * alpha))
            self.im.paste(spr, box, m)


def shade(fr, a, color=(0, 0, 0)):
    """Oscurece todo el cuadro (para escenas de corte)."""
    if a <= 0.004:
        return
    ov = Image.new("RGB", fr.im.size, color)
    fr.im = Image.blend(fr.im, ov, clamp(a))
    fr.d = ImageDraw.Draw(fr.im)


# ---------- texto como sprite ----------
def tsprite(txt, fname, size, color=WHITE, stroke=0, sfill=(0, 0, 0), glow=None):
    """glow = (color, radio, fuerza)."""
    size = max(8, int(round(size)))
    key = (txt, fname, size, color, stroke, sfill, glow)
    s = _tcache.get2(key)
    if s is not None:
        return s
    f = font(fname, size)
    l, t_, r, b = f.getbbox(txt, stroke_width=stroke)
    pad = int(glow[1] * 2.6) + 4 if glow else 4
    im = Image.new("RGBA", (max(1, r - l + 2 * pad), max(1, b - t_ + 2 * pad)), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, pad - t_), txt, font=f, fill=color + (255,), stroke_width=stroke,
                            stroke_fill=sfill + (255,))
    if glow:
        gc, rad, k = glow
        a = im.getchannel("A").filter(ImageFilter.GaussianBlur(rad)).point(lambda v: min(255, int(v * k)))
        g = Image.new("RGBA", im.size, gc + (0,))
        g.putalpha(a)
        im = Image.alpha_composite(g, im)
    return _tcache.put(key, im)


def tfit(txt, fname, size, maxw):
    f = font(fname, size)
    w = f.getlength(txt)
    return size if w <= maxw else max(10, size * maxw / w)


def put(fr, spr, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if spr is None or scale <= 0.01 or alpha <= 0.004:
        return
    if abs(rot) > 0.2:
        spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if abs(scale - 1) > 0.004:
        spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BILINEAR)
    fr.paste(spr, cx, cy, alpha)


def say(fr, txt, cx, cy, size, color=WHITE, fname=BLACK, a=1.0, s=1.0, rot=0.0, maxw=900, glow=None, stroke=0):
    sz = tfit(txt, fname, size, maxw)
    put(fr, tsprite(txt, fname, sz, color, stroke, glow=glow), cx, cy, s, a, rot)


def pop(x, dur=0.32):
    """Escala de entrada con rebote: 0 antes de empezar, 1 al final."""
    return back_out(x / dur) if x > 0 else 0.0


def appear(x, dur=0.25):
    return ease_out(x / dur) if x > 0 else 0.0


# ---------- sprites dibujados ----------
def _new(w, h, S=SS):
    im = Image.new("RGBA", (int(w * S), int(h * S)), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def _done(key, im, w, h):
    _scache[key] = im.resize((int(w), int(h)), Image.LANCZOS)
    return _scache[key]


def panel(w, h, fill=(18, 10, 40, 215), outline=PINK, r=34, width=4):
    key = ("panel", int(w), int(h), fill, outline, r, width)
    if key in _scache:
        return _scache[key]
    S = 2
    im, d = _new(w, h, S)
    d.rounded_rectangle([0, 0, w * S - 1, h * S - 1], r * S, fill=fill, outline=outline + (255,) if outline else None,
                        width=width * S)
    return _done(key, im, w, h)


def pill(txt, size, fg=INK, bg=YEL, padx=34, pady=16, fname=HEAVY):
    key = ("pill", txt, int(size), fg, bg, fname)
    if key in _scache:
        return _scache[key]
    f = font(fname, size)
    w = f.getlength(txt) + padx * 2
    h = size + pady * 2
    S = 2
    im, d = _new(w, h, S)
    d.rounded_rectangle([0, 0, w * S - 1, h * S - 1], h * S / 2, fill=bg + (255,))
    fs = font(fname, size * S)
    d.text((w * S / 2, h * S / 2), txt, font=fs, fill=fg + (255,), anchor="mm")
    return _done(key, im, w, h)


def controller(w):
    key = ("pad", int(w))
    if key in _scache:
        return _scache[key]
    h = w * 0.62
    im, d = _new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    body = (236, 236, 246, 255)
    d.ellipse([0, H_ * 0.18, W_ * 0.42, H_ * 0.98], fill=body)
    d.ellipse([W_ * 0.58, H_ * 0.18, W_, H_ * 0.98], fill=body)
    d.rounded_rectangle([W_ * 0.14, H_ * 0.06, W_ * 0.86, H_ * 0.70], H_ * 0.30, fill=body)
    dk = (40, 30, 70, 255)
    cx, cy, a = W_ * 0.25, H_ * 0.40, W_ * 0.035
    d.rounded_rectangle([cx - a * 3, cy - a, cx + a * 3, cy + a], a * 0.5, fill=dk)
    d.rounded_rectangle([cx - a, cy - a * 3, cx + a, cy + a * 3], a * 0.5, fill=dk)
    for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        bx, by, rr = W_ * 0.75 + dx * W_ * 0.055, H_ * 0.40 + dy * W_ * 0.055, W_ * 0.028
        d.ellipse([bx - rr, by - rr, bx + rr, by + rr], fill=(255, 70, 170, 255) if dy == -1 else dk)
    for sx in (0.38, 0.62):
        rr = W_ * 0.06
        d.ellipse([W_ * sx - rr, H_ * 0.62 - rr, W_ * sx + rr, H_ * 0.62 + rr], fill=(60, 50, 95, 255))
        d.ellipse([W_ * sx - rr * 0.6, H_ * 0.62 - rr * 0.6, W_ * sx + rr * 0.6, H_ * 0.62 + rr * 0.6], fill=(90, 80, 130, 255))
    return _done(key, im, w, h)


def calendar(w, top_txt, big_txt, header=PINK):
    key = ("cal", int(w), top_txt, big_txt, header)
    if key in _scache:
        return _scache[key]
    h = w * 1.08
    im, d = _new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    d.rounded_rectangle([0, H_ * 0.06, W_, H_], W_ * 0.07, fill=(250, 248, 255, 255))
    d.rounded_rectangle([0, H_ * 0.06, W_, H_ * 0.32], W_ * 0.07, fill=header + (255,))
    d.rectangle([0, H_ * 0.22, W_, H_ * 0.32], fill=header + (255,))
    for rx in (0.28, 0.72):
        d.rounded_rectangle([W_ * rx - W_ * 0.03, 0, W_ * rx + W_ * 0.03, H_ * 0.13], W_ * 0.03, fill=(60, 50, 90, 255))
    d.text((W_ / 2, H_ * 0.19), top_txt, font=font(HEAVY, W_ * 0.12), fill=(255, 255, 255, 255), anchor="mm")
    f = font(BLACK, W_ * 0.36)
    while f.getlength(big_txt) > W_ * 0.86:
        f = font(BLACK, f.size * 0.95)
    d.text((W_ / 2, H_ * 0.66), big_txt, font=f, fill=(24, 16, 44, 255), anchor="mm")
    return _done(key, im, w, h)


def bill(w, rot=0):
    rot = int(round(rot / 10.0)) * 10 % 360
    key = ("bill", int(w), rot)
    if key in _scache:
        return _scache[key]
    base_key = ("bill", int(w), 0)
    if base_key not in _scache:
        h = w * 0.46
        im, d = _new(w, h)
        S = SS
        W_, H_ = w * S, h * S
        d.rounded_rectangle([0, 0, W_, H_], H_ * 0.08, fill=(118, 196, 120, 255))
        d.rounded_rectangle([W_ * 0.04, H_ * 0.09, W_ * 0.96, H_ * 0.91], H_ * 0.06, outline=(40, 110, 60, 255), width=int(S * 3))
        d.ellipse([W_ / 2 - H_ * 0.30, H_ * 0.20, W_ / 2 + H_ * 0.30, H_ * 0.80], fill=(80, 160, 90, 255))
        d.text((W_ / 2, H_ / 2), "$", font=font(BLACK, H_ * 0.48), fill=(230, 255, 230, 255), anchor="mm")
        _done(base_key, im, w, h)
    if rot == 0:
        return _scache[base_key]
    _scache[key] = _scache[base_key].rotate(rot, resample=Image.BICUBIC, expand=True)
    return _scache[key]


def coin(w):
    key = ("coin", int(w))
    if key in _scache:
        return _scache[key]
    im, d = _new(w, w)
    S = SS
    n = w * S
    d.ellipse([0, 0, n - 1, n - 1], fill=(214, 150, 30, 255))
    d.ellipse([n * 0.08, n * 0.06, n * 0.92, n * 0.90], fill=(255, 205, 70, 255))
    d.ellipse([n * 0.18, n * 0.16, n * 0.82, n * 0.80], outline=(220, 160, 40, 255), width=int(S * 3))
    d.text((n / 2, n * 0.48), "$", font=font(BLACK, n * 0.46), fill=(190, 120, 20, 255), anchor="mm")
    return _done(key, im, w, w)


def disc(w):
    key = ("disc", int(w))
    if key in _scache:
        return _scache[key]
    im, d = _new(w, w)
    S = SS
    n = w * S
    for i, c in enumerate([(200, 210, 240), (150, 220, 255), (255, 160, 220), (230, 230, 250)]):
        d.pieslice([0, 0, n - 1, n - 1], i * 90 + 20, i * 90 + 110, fill=c + (255,))
    d.ellipse([n * 0.33, n * 0.33, n * 0.67, n * 0.67], fill=(60, 50, 90, 255))
    d.ellipse([n * 0.44, n * 0.44, n * 0.56, n * 0.56], fill=(0, 0, 0, 0))
    return _done(key, im, w, w)


def clapper(w):
    key = ("clap", int(w))
    if key in _scache:
        return _scache[key]
    h = w * 0.86
    im, d = _new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    d.rounded_rectangle([0, H_ * 0.30, W_, H_], W_ * 0.05, fill=(40, 36, 60, 255))
    d.rectangle([W_ * 0.08, H_ * 0.48, W_ * 0.92, H_ * 0.53], fill=(210, 210, 230, 255))
    d.rectangle([W_ * 0.08, H_ * 0.66, W_ * 0.70, H_ * 0.71], fill=(210, 210, 230, 255))
    d.polygon([(0, H_ * 0.26), (W_ * 0.96, H_ * 0.02), (W_, H_ * 0.18), (W_ * 0.04, H_ * 0.42)], fill=(240, 240, 250, 255))
    for i in range(4):
        x0 = W_ * (0.10 + i * 0.23)
        d.polygon([(x0, H_ * 0.235 - i * H_ * 0.055), (x0 + W_ * 0.11, H_ * 0.205 - i * H_ * 0.055),
                   (x0 + W_ * 0.15, H_ * 0.33 - i * H_ * 0.055), (x0 + W_ * 0.04, H_ * 0.36 - i * H_ * 0.055)],
                  fill=(40, 36, 60, 255))
    return _done(key, im, w, h)


def console(w, light=PINK):
    key = ("cons", int(w), light)
    if key in _scache:
        return _scache[key]
    h = w * 0.62
    im, d = _new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    d.rounded_rectangle([0, H_ * 0.08, W_, H_ * 0.92], H_ * 0.10, fill=(232, 230, 244, 255))
    d.rounded_rectangle([W_ * 0.03, H_ * 0.14, W_ * 0.97, H_ * 0.86], H_ * 0.08, fill=(36, 30, 58, 255))
    d.rounded_rectangle([W_ * 0.08, H_ * 0.30, W_ * 0.62, H_ * 0.37], H_ * 0.03, fill=(80, 74, 110, 255))
    d.rounded_rectangle([W_ * 0.08, H_ * 0.66, W_ * 0.92, H_ * 0.70], H_ * 0.02, fill=light + (255,))
    rr = H_ * 0.07
    d.ellipse([W_ * 0.82 - rr, H_ * 0.34 - rr, W_ * 0.82 + rr, H_ * 0.34 + rr], fill=light + (255,))
    return _done(key, im, w, h)


def game_case(w, c1=PINK, c2=ORANGE):
    key = ("case", int(w), c1, c2)
    if key in _scache:
        return _scache[key]
    h = w * 1.26
    S = SS
    n_w, n_h = int(w * S), int(h * S)
    yy = np.linspace(0, 1, n_h)[:, None, None]
    col = np.array(c1, float) * (1 - yy) + np.array(c2, float) * yy
    cover = Image.fromarray(np.broadcast_to(col, (n_h, n_w, 3)).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", (n_w, n_h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, n_w - 1, n_h - 1], n_w * 0.06, fill=255)
    cover.putalpha(m)
    d = ImageDraw.Draw(cover)
    d.rectangle([0, 0, n_w * 0.10, n_h], fill=(30, 20, 50, 200))
    d.ellipse([n_w * 0.30, n_h * 0.18, n_w * 0.86, n_h * 0.62], fill=(255, 220, 120, 150))
    d.rectangle([n_w * 0.22, n_h * 0.74, n_w * 0.90, n_h * 0.80], fill=(255, 255, 255, 190))
    return _done(key, cover, w, h)


def price_tag(w, txt, sub=""):
    key = ("tag", int(w), txt, sub)
    if key in _scache:
        return _scache[key]
    h = w * 0.62
    im, d = _new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    d.polygon([(0, H_ / 2), (W_ * 0.20, 0), (W_, 0), (W_, H_), (W_ * 0.20, H_)], fill=(255, 210, 63, 255))
    rr = H_ * 0.09
    d.ellipse([W_ * 0.14 - rr, H_ / 2 - rr, W_ * 0.14 + rr, H_ / 2 + rr], fill=(0, 0, 0, 0))
    f = font(BLACK, H_ * 0.48)
    while f.getlength(txt) > W_ * 0.66:
        f = font(BLACK, f.size * 0.95)
    d.text((W_ * 0.60, H_ * (0.44 if sub else 0.5)), txt, font=f, fill=(24, 16, 44, 255), anchor="mm")
    if sub:
        fs = font(HEAVY, H_ * 0.13)
        while fs.getlength(sub) > W_ * 0.70:
            fs = font(HEAVY, fs.size * 0.95)
        d.text((W_ * 0.60, H_ * 0.80), sub, font=fs, fill=(24, 16, 44, 255), anchor="mm")
    return _done(key, im, w, h)


def stamp(txt, size, color=RED):
    key = ("stamp", txt, int(size), color)
    if key in _scache:
        return _scache[key]
    f = font(BLACK, size)
    w = f.getlength(txt) + size * 1.1
    h = size * 1.9
    S = 2
    im, d = _new(w, h, S)
    d.rounded_rectangle([S * 6, S * 6, w * S - S * 6, h * S - S * 6], size * 0.25 * S, outline=color + (255,), width=int(size * 0.14 * S))
    d.text((w * S / 2, h * S / 2), txt, font=font(BLACK, size * S), fill=color + (255,), anchor="mm")
    # textura de sello: huecos aleatorios
    rng = np.random.default_rng(len(txt))
    a = np.array(im.getchannel("A"), dtype=np.float32)
    holes = rng.random(a.shape) < 0.06
    a[holes] *= 0.25
    im.putalpha(Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2)))
    return _done(key, im, w, h)


def heart(w, color=PINK):
    key = ("heart", int(w), color)
    if key in _scache:
        return _scache[key]
    im, d = _new(w, w)
    S = SS
    n = w * S
    d.ellipse([n * 0.04, n * 0.10, n * 0.54, n * 0.58], fill=color + (255,))
    d.ellipse([n * 0.46, n * 0.10, n * 0.96, n * 0.58], fill=color + (255,))
    d.polygon([(n * 0.07, n * 0.44), (n * 0.93, n * 0.44), (n * 0.5, n * 0.94)], fill=color + (255,))
    return _done(key, im, w, w)


def checker(w, h, cell=18):
    key = ("chk", int(w), int(h), cell)
    if key in _scache:
        return _scache[key]
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for yy in range(0, int(h), cell):
        for xx in range(0, int(w), cell):
            if (xx // cell + yy // cell) % 2 == 0:
                d.rectangle([xx, yy, xx + cell - 1, yy + cell - 1], fill=(255, 255, 255, 255))
            else:
                d.rectangle([xx, yy, xx + cell - 1, yy + cell - 1], fill=(20, 14, 36, 255))
    _scache[key] = im
    return im


def bar(w, h, c1, c2, r=None, glow=None):
    """Barra con degradado vertical (c1 arriba, c2 abajo)."""
    w, h = max(2, int(w)), max(2, int(h))
    key = ("bar", w, h, c1, c2, glow)
    s = _tcache.get2(key)
    if s is not None:
        return s
    yy = np.linspace(0, 1, h)[:, None, None]
    col = np.array(c1, float) * (1 - yy) + np.array(c2, float) * yy
    im = Image.fromarray(np.broadcast_to(col, (h, w, 3)).astype(np.uint8)).convert("RGBA")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r if r is not None else min(w, h) // 4, fill=255)
    im.putalpha(m)
    if glow:
        pad = glow[1] * 2
        out = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
        g = Image.new("RGBA", out.size, glow[0] + (0,))
        a = Image.new("L", out.size, 0)
        a.paste(m, (pad, pad))
        g.putalpha(a.filter(ImageFilter.GaussianBlur(glow[1])).point(lambda v: int(v * 0.9)))
        out.alpha_composite(g)
        out.alpha_composite(im, (pad, pad))
        im = out
    return _tcache.put(key, im)


# ---------- camara ----------
_white = None


def camera(im, t, sc, spec):
    """Empuje lento, golpe de zoom al entrar a la escena y en cues, sacudida y destello."""
    global _white
    cam = spec.get("camera")
    if not cam:
        return im
    x = t - sc.t0
    dur = max(0.5, sc.t1 - sc.t0)
    s = 1.0 + cam.get("push", 0.035) * clamp(x / dur)
    if not sc.first:
        s *= 1 + cam.get("enter", 0.10) * (1 - ease_out(x / 0.34))
    dx = dy = 0.0
    for c in cam.get("punch", []):
        if c in sc.lcues:
            k = t - sc.lcues[c]
            if 0 <= k < 0.42:
                s *= 1 + 0.07 * (1 - ease_out(k / 0.42))
    for c in cam.get("shake", []):
        if c in sc.lcues:
            k = t - sc.lcues[c]
            if 0 <= k < 0.40:
                amp = 20 * (1 - k / 0.40) ** 2
                dx += amp * math.sin(k * 95)
                dy += amp * math.cos(k * 71)
    if s > 1.001 or dx or dy:
        s = max(s, 1.0 + (abs(dx) + abs(dy)) * 2.2 / W)     # zoom minimo para que la sacudida no deje bordes
        w, h = W / s, H / s
        x0 = clamp(W / 2 - w / 2 + dx, 0, W - w)
        y0 = clamp(H / 2 - h / 2 + dy, 0, H - h)
        im = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + w, y0 + h))
    if not sc.first and x < 0.12:
        if _white is None:
            _white = Image.new("RGB", (W, H), (255, 255, 255))
        im = Image.blend(im, _white, 0.26 * (1 - x / 0.12))
    return im


def rgb_split(im, amount):
    """Aberracion cromatica para cortes tipo glitch."""
    k = int(round(amount))
    if k < 1:
        return im
    a = np.array(im)
    out = a.copy()
    out[:, k:, 0] = a[:, :-k, 0]
    out[:, :-k, 2] = a[:, k:, 2]
    return Image.fromarray(out)


def box(w):
    """Caja de carton generica (sin logos)."""
    key = ("box", int(w))
    if key in _scache:
        return _scache[key]
    h = w * 0.95
    im, d = _new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    top = [(W_ * 0.06, H_ * 0.30), (W_ * 0.30, H_ * 0.06), (W_ * 0.96, H_ * 0.06), (W_ * 0.72, H_ * 0.30)]
    d.polygon(top, fill=(222, 170, 110, 255))
    d.polygon([(W_ * 0.72, H_ * 0.30), (W_ * 0.96, H_ * 0.06), (W_ * 0.96, H_ * 0.74), (W_ * 0.72, H_ * 0.98)], fill=(160, 108, 58, 255))
    d.rectangle([W_ * 0.06, H_ * 0.30, W_ * 0.72, H_ * 0.98], fill=(196, 140, 80, 255))
    d.polygon([(W_ * 0.30, H_ * 0.30), (W_ * 0.54, H_ * 0.06), (W_ * 0.64, H_ * 0.06), (W_ * 0.40, H_ * 0.30)], fill=(240, 215, 170, 255))
    d.rectangle([W_ * 0.30, H_ * 0.30, W_ * 0.40, H_ * 0.52], fill=(240, 215, 170, 255))
    d.rectangle([W_ * 0.12, H_ * 0.72, W_ * 0.36, H_ * 0.90], fill=(250, 245, 235, 255))
    for i in range(3):
        d.rectangle([W_ * 0.14, H_ * (0.75 + i * 0.045), W_ * (0.32 - i * 0.04), H_ * (0.77 + i * 0.045)], fill=(120, 110, 100, 255))
    return _done(key, im, w, h)


def rack(w, t=0.0, seed=0):
    """Servidor con luces que parpadean (no se guarda en cache)."""
    h = w * 1.9
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], w * 0.06, fill=(30, 38, 62, 255), outline=(90, 110, 150, 255), width=3)
    n = 7
    rng = np.random.default_rng(seed)
    ph = rng.uniform(0, 6.28, (n, 3))
    for i in range(n):
        y0 = h * 0.05 + i * h * 0.13
        d.rounded_rectangle([w * 0.08, y0, w * 0.92, y0 + h * 0.10], 6, fill=(18, 24, 44, 255))
        for j in range(3):
            on = math.sin(t * (4 + j * 2.3) + ph[i, j]) > 0.1
            c = [(70, 230, 225), (74, 222, 128), (255, 210, 63)][j] if on else (50, 60, 80)
            cx = w * (0.70 + j * 0.08)
            d.ellipse([cx - 6, y0 + h * 0.05 - 6, cx + 6, y0 + h * 0.05 + 6], fill=c + (255,))
        d.rectangle([w * 0.14, y0 + h * 0.04, w * 0.50, y0 + h * 0.06], fill=(60, 72, 100, 255))
    return im

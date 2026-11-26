"""Ilustraciones con estilo propio (estreno: 006 Red Bull).

Estilo "tarjeta impresa": escenas dibujadas completas sobre una tarjeta crema con
contorno de tinta grueso, sombra dura desplazada y semitono en el lado de sombra.
Paleta corta y fija. Nada de logos, personajes conocidos ni fotos.

Se registra solo en scenes2 (escenas y SFX) al importarse desde render.py.
"""
import math

import numpy as np
from PIL import Image, ImageChops, ImageDraw

from core import *          # noqa: F401,F403
import fx
from fx import put, say, pill, panel, appear, pop, stamp, bill, shade, tsprite, tfit
import scenes2 as S2
from scenes2 import kick, slam, lc

# ---------- paleta ----------
INKC = (24, 20, 46)
PAPER = (248, 238, 216)
SKYC = (150, 208, 250)
SEA = (70, 150, 220)
CORAL = (255, 104, 88)
NAVY = (44, 60, 124)
STEEL = (184, 196, 220)
TEALC = (64, 206, 186)
LEAF = (104, 196, 112)
ORNG = (255, 160, 56)
BROWN = (168, 106, 62)
YELC = YEL
OUT = 5
SHX, SHY = 8, 10

fx.THEMES["volt"] = dict(top=(6, 8, 28), mid=(16, 24, 66), low=(44, 64, 140), floor=(5, 6, 20), grid=(255, 200, 70),
                         horizon=1610, sun=False, palms=False)


def _dark(c, k=0.78):
    return tuple(int(v * k) for v in c)


class Pen:
    """Lienzo con supermuestreo. Cada figura: sombra dura, relleno, semitono opcional y contorno de tinta."""

    def __init__(self, w, h, S=2):
        self.w, self.h, self.S = w, h, S
        self.im = Image.new("RGBA", (int(w * S), int(h * S)), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def P(self, pts, dx=0, dy=0):
        S = self.S
        return [((x + dx) * S, (y + dy) * S) for x, y in pts]

    def _ht(self, maskfn, bbox, fill):
        S = self.S
        x0, y0, x1, y1 = [int(v * S) for v in bbox]
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(self.im.width, x1), min(self.im.height, y1)
        if x1 - x0 < 6 or y1 - y0 < 6:
            return
        m = Image.new("L", self.im.size, 0)
        maskfn(ImageDraw.Draw(m))
        dots = Image.new("L", self.im.size, 0)
        dd = ImageDraw.Draw(dots)
        g = 9 * S
        for row, yy in enumerate(range(y0, y1, g)):
            for xx in range(x0 + (row % 2) * g // 2, x1, g):
                u = ((xx - x0) / (x1 - x0) + (yy - y0) / (y1 - y0)) / 2
                r = g * 0.46 * clamp((u - 0.42) / 0.58)
                if r > 0.7:
                    dd.ellipse([xx - r, yy - r, xx + r, yy + r], fill=255)
        dots = ImageChops.multiply(dots, m)
        self.im.paste(Image.new("RGBA", self.im.size, _dark(fill) + (255,)), (0, 0), dots)

    def poly(self, pts, fill, sh=True, ht=False, out=OUT):
        P = self.P(pts)
        if sh:
            self.d.polygon(self.P(pts, SHX, SHY), fill=INKC + (255,))
        self.d.polygon(P, fill=fill + (255,))
        if ht:
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            self._ht(lambda dm: dm.polygon(P, fill=255), (min(xs), min(ys), max(xs), max(ys)), fill)
        if out:
            self.d.line(P + [P[0], P[1]], fill=INKC + (255,), width=int(out * self.S), joint="curve")

    def rect(self, x0, y0, x1, y1, fill, r=0, sh=True, ht=False, out=OUT):
        S = self.S
        box = [x0 * S, y0 * S, x1 * S, y1 * S]
        if sh:
            self.d.rounded_rectangle([(x0 + SHX) * S, (y0 + SHY) * S, (x1 + SHX) * S, (y1 + SHY) * S], r * S,
                                     fill=INKC + (255,))
        self.d.rounded_rectangle(box, r * S, fill=fill + (255,))
        if ht:
            self._ht(lambda dm: dm.rounded_rectangle(box, r * S, fill=255), (x0, y0, x1, y1), fill)
        if out:
            self.d.rounded_rectangle(box, r * S, outline=INKC + (255,), width=int(out * S))

    def ell(self, cx, cy, rx, ry, fill, sh=True, ht=False, out=OUT):
        S = self.S
        box = [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]
        if sh:
            self.d.ellipse([(cx - rx + SHX) * S, (cy - ry + SHY) * S, (cx + rx + SHX) * S, (cy + ry + SHY) * S],
                           fill=INKC + (255,))
        self.d.ellipse(box, fill=fill + (255,))
        if ht:
            self._ht(lambda dm: dm.ellipse(box, fill=255), (cx - rx, cy - ry, cx + rx, cy + ry), fill)
        if out:
            self.d.ellipse(box, outline=INKC + (255,), width=int(out * S))

    def ln(self, pts, w=OUT, col=INKC):
        self.d.line(self.P(pts), fill=col + (255,), width=int(w * self.S), joint="curve")

    def txt(self, x, y, s, size, col=INKC, fname=BLACK, anchor="mm"):
        self.d.text((x * self.S, y * self.S), s, font=font(fname, int(size * self.S)), fill=col + (255,), anchor=anchor)

    def done(self, key):
        fx._scache[key] = self.im.resize((int(self.w), int(self.h)), Image.LANCZOS)
        return fx._scache[key]


def cached(key):
    return fx._scache.get(key)


# ---------- piezas ----------
def can_spr(w, open_top=False):
    """Lata genérica nuestra: cuerpo crema, banda coral, rayo azul marino. Sin marca."""
    key = ("ilcan", int(w), open_top)
    if cached(key):
        return cached(key)
    h = w * 1.8
    p = Pen(w + 14, h + 16)
    m = 4
    ry = w * 0.13
    p.rect(m, m + ry, w - m, h - m - ry * 0.4, PAPER if not open_top else STEEL, r=w * 0.12, ht=True, out=4)
    if not open_top:
        p.rect(m, h * 0.30, w - m, h * 0.50, CORAL, sh=False, out=4)
        cx = w / 2
        p.poly([(cx + w * 0.08, h * 0.54), (cx - w * 0.16, h * 0.70), (cx - w * 0.01, h * 0.70),
                (cx - w * 0.10, h * 0.86), (cx + w * 0.18, h * 0.66), (cx + w * 0.02, h * 0.66)], NAVY, sh=False, out=3)
    p.ell(w / 2, m + ry, w / 2 - m, ry, STEEL if not open_top else (120, 132, 160), sh=False, out=4)
    if not open_top:
        p.ell(w * 0.6, m + ry, w * 0.12, ry * 0.4, (120, 132, 160), sh=False, out=3)
    return p.done(key)


def card(w, h, bg=PAPER):
    """Tarjeta impresa: base de cada ilustración."""
    p = Pen(w + 20, h + 22)
    p.rect(4, 4, w, h, bg, r=34, out=7)
    return p


def _belt(p, x0, x1, y):
    p.rect(x0, y, x1, y + 30, (60, 62, 90), r=15, out=4)
    for x in range(int(x0 + 22), int(x1 - 10), 46):
        p.ell(x, y + 15, 9, 9, STEEL, sh=False, out=3)


def _floor(p, w, y, col=(226, 212, 184)):
    p.rect(4, y, w, y + 20, col, sh=False, out=0)
    p.ln([(4, y), (w, y)], 5)


# ---------- tarjetas por escena ----------
CW, CH = 920, 500


def ill_factory_card(w=CW, h=440):
    key = ("ilfactory", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, SKYC)
    gy = h - 70
    p.rect(4, gy, w, h, (226, 212, 184), sh=False, out=0)
    p.ln([(4, gy), (w, gy)], 5)
    # fábrica
    x0, x1, top = 90, 520, 170
    p.rect(x0 + 300, 70, x0 + 350, top + 30, NAVY, ht=True)                      # chimenea
    p.rect(x0 + 296, 64, x0 + 354, 84, CORAL, sh=False)
    teeth = []
    n = 4
    tw = (x1 - x0) / n
    for i in range(n):
        teeth += [(x0 + i * tw, top + 40), (x0 + i * tw + tw * 0.7, top), (x0 + (i + 1) * tw, top)]
    p.poly([(x0, gy)] + teeth + [(x1, top + 40), (x1, gy)], CORAL, ht=True)
    for i in range(n):
        p.poly([(x0 + i * tw + tw * 0.7, top + 4), (x0 + (i + 1) * tw - 4, top + 4), (x0 + (i + 1) * tw - 4, top + 36)],
               SKYC, sh=False, out=3)
    for i in range(4):
        p.rect(x0 + 30 + i * 100, top + 80, x0 + 90 + i * 100, top + 130, PAPER, r=6, sh=False, out=4)
    p.rect(x0 + 180, gy - 110, x0 + 260, gy, NAVY, r=4, sh=False, out=4)               # puerta cerrada
    for k in range(5):
        p.ln([(x0 + 184, gy - 100 + k * 20), (x0 + 256, gy - 100 + k * 20)], 3, STEEL)
    # cinta que pasa de largo
    _belt(p, 560, w - 20, gy - 40)
    return p.done(key)


def ill_mountain_card(w=CW, h=CH):
    key = ("ilmount", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, (40, 56, 120))
    rng = np.random.default_rng(3)
    for _ in range(40):
        x, y = rng.uniform(30, w - 30), rng.uniform(30, h * 0.5)
        r = rng.uniform(2, 4)
        p.ell(x, y, r, r, PAPER, sh=False, out=0)
    gy = h - 60
    p.rect(4, gy, w, h, (30, 40, 90), sh=False, out=0)
    p.ln([(4, gy), (w, gy)], 5)
    return p.done(key)


def ill_canmaker_card(w=CW, h=CH):
    key = ("ilcanmaker", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, (236, 228, 255))
    gy = h - 70
    _floor(p, w, gy)
    # bobina de aluminio
    p.poly([(190, 350), (400, 300), (400, 320), (190, 370)], STEEL, out=4)
    p.ell(180, 300, 110, 110, STEEL, ht=True)
    for r in (95, 70, 48):
        p.ell(180, 300, r * 0.92, r * 0.92, STEEL, sh=False, out=3)
    p.ell(180, 300, 26, 26, NAVY, sh=False, out=4)
    p.rect(130, 400, 230, gy, (120, 132, 160), sh=False, out=4)
    # prensa
    p.rect(380, 110, 560, gy, NAVY, r=10, ht=True)
    p.rect(400, 140, 540, 200, CORAL, r=8, sh=False)
    p.rect(400, 330, 540, 380, (120, 132, 160), r=6, sh=False)
    p.ell(470, 170, 14, 14, YELC, sh=False, out=3)
    _belt(p, 560, w - 24, gy - 46)
    return p.done(key)


def ill_filler_card(w=CW, h=CH):
    key = ("ilfiller", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, (255, 238, 214))
    gy = h - 70
    _floor(p, w, gy)
    # caja de fruta
    p.rect(40, 340, 220, gy, BROWN, r=6, ht=True)
    for k in range(3):
        p.ln([(48, 370 + k * 40), (212, 370 + k * 40)], 3, _dark(BROWN, 0.6))
    for i, (x, y, c) in enumerate([(70, 320, ORNG), (120, 310, CORAL), (170, 322, ORNG), (95, 290, LEAF), (148, 285, CORAL)]):
        p.ell(x, y, 28, 28, c, ht=True, out=4)
    # tanque
    p.rect(250, 100, 410, gy, STEEL, r=40, ht=True)
    p.rect(296, 180, 364, 400, PAPER, r=16, sh=False, out=4)
    p.rect(300, 270, 360, 396, ORNG, r=12, sh=False, out=0)
    p.ln([(410, 140), (470, 140), (470, 200)], 14)
    p.ln([(410, 140), (470, 140), (470, 200)], 6, ORNG)
    # barra de boquillas
    p.rect(440, 190, w - 30, 236, NAVY, r=10, ht=True)
    for x in NOZ:
        p.poly([(x - 18, 236), (x + 18, 236), (x + 6, 266), (x - 6, 266)], STEEL, sh=False, out=4)
    _belt(p, 440, w - 24, gy - 46)
    return p.done(key)


NOZ = (520, 630, 740, 850)


def ill_ship_card(w=CW, h=CH):
    key = ("ilship", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, SKYC)
    p.ell(770, 110, 54, 54, YELC, sh=False)
    # tierra con vía
    p.poly([(4, 150), (220, 120), (520, 170), (w, 140), (w, 300), (4, 300)], LEAF, sh=False, out=5)
    p.rect(4, 250, w, 266, (110, 90, 70), sh=False, out=3)
    for x in range(20, w, 34):
        p.ln([(x, 246), (x - 6, 270)], 4)
    # mar
    p.rect(4, 300, w, h, SEA, sh=False, out=0)
    p.ln([(4, 300), (w, 300)], 5)
    for row in range(4):
        y = 340 + row * 52
        pts = [(x, y + 6 * math.sin(x / 30 + row)) for x in range(10, w, 16)]
        p.ln(pts, 3, (150, 200, 245))
    return p.done(key)


def train_spr():
    key = ("iltrain",)
    if cached(key):
        return cached(key)
    p = Pen(760, 130)
    cols = [CORAL, YELC, TEALC, NAVY]
    for i in range(4):
        x = 10 + i * 150
        p.rect(x, 20, x + 138, 92, cols[i], r=6, ht=True, out=4)
        for k in range(1, 4):
            p.ln([(x + k * 34, 26), (x + k * 34, 86)], 3, _dark(cols[i], 0.6))
        p.ell(x + 30, 104, 14, 14, (60, 62, 90), sh=False, out=4)
        p.ell(x + 108, 104, 14, 14, (60, 62, 90), sh=False, out=4)
    x = 610
    p.poly([(x, 92), (x, 30), (x + 70, 30), (x + 120, 60), (x + 130, 92)], NAVY, ht=True, out=4)
    p.rect(x + 14, 40, x + 54, 66, SKYC, r=4, sh=False, out=3)
    p.ell(x + 34, 104, 16, 16, (60, 62, 90), sh=False, out=4)
    p.ell(x + 100, 104, 16, 16, (60, 62, 90), sh=False, out=4)
    return p.done(key)


def ship_spr():
    key = ("ilshipspr",)
    if cached(key):
        return cached(key)
    p = Pen(560, 250)
    cols = [CORAL, YELC, TEALC, ORNG, STEEL, CORAL, TEALC, YELC]
    for row in range(2):
        for i in range(4):
            x = 110 + i * 82 + row * 20
            y = 96 - row * 50
            p.rect(x, y, x + 76, y + 46, cols[row * 4 + i], r=3, out=4)
    p.rect(40, 50, 100, 142, PAPER, r=4, out=4)
    p.rect(52, 66, 88, 86, SKYC, sh=False, out=3)
    p.poly([(10, 140), (530, 140), (480, 220), (50, 220)], NAVY, ht=True)
    p.rect(30, 160, 510, 172, CORAL, sh=False, out=0)
    return p.done(key)


def rider_vignette(w=280, h=360):
    key = ("ilrider", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, (255, 224, 196))
    gy = h - 50
    p.poly([(4, gy), (4, 150), (40, 210), (90, gy)], STEEL, ht=True, out=5)
    p.poly([(w, gy), (w, 150), (w - 36, 210), (w - 86, gy)], STEEL, ht=True, out=5)
    p.rect(4, gy, w, h, (226, 212, 184), sh=False, out=0)
    p.ln([(4, gy), (w, gy)], 5)
    return p.done(key)


def rider_spr():
    """Figura genérica sin cara: casco, cuerpo, patineta."""
    key = ("ilriderspr",)
    if cached(key):
        return cached(key)
    p = Pen(150, 170)
    p.rect(20, 140, 130, 152, NAVY, r=6, out=4)
    p.ell(40, 158, 8, 8, PAPER, sh=False, out=3)
    p.ell(110, 158, 8, 8, PAPER, sh=False, out=3)
    p.ln([(60, 138), (68, 96)], 12)
    p.ln([(92, 138), (84, 96)], 12)
    p.rect(54, 52, 100, 102, CORAL, r=14, ht=True, out=4)
    p.ln([(56, 62), (24, 40)], 10)
    p.ln([(98, 62), (132, 44)], 10)
    p.ell(77, 32, 24, 24, YELC, out=4)
    p.rect(58, 28, 98, 38, NAVY, r=4, sh=False, out=0)
    return p.done(key)


def car_vignette(w=280, h=360):
    key = ("ilcarv", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, (210, 236, 214))
    p.rect(4, 200, w, 300, (70, 72, 96), sh=False, out=5)
    for x in range(10, w, 60):
        p.rect(x, 246, x + 34, 254, PAPER, sh=False, out=0)
    for i in range(0, w, 28):
        p.rect(i, 300, i + 28, 316, CORAL if (i // 28) % 2 else PAPER, sh=False, out=0)
    p.ln([(4, 300), (w, 300)], 4)
    return p.done(key)


def car_spr():
    """Monoplaza genérico, coral, sin patrocinadores."""
    key = ("ilcar",)
    if cached(key):
        return cached(key)
    p = Pen(230, 90)
    p.poly([(10, 60), (40, 44), (120, 40), (150, 22), (176, 24), (186, 44), (220, 50), (224, 62), (10, 66)], CORAL,
           ht=True, out=4)
    p.rect(4, 30, 22, 60, NAVY, sh=False, out=3)
    p.ell(150, 30, 12, 10, YELC, sh=False, out=3)
    p.ell(50, 66, 18, 18, (40, 40, 56), sh=False, out=4)
    p.ell(186, 66, 18, 18, (40, 40, 56), sh=False, out=4)
    p.txt(96, 54, "06", 20, PAPER)
    return p.done(key)


def globe_vignette(w=280, h=360):
    key = ("ilglobe", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, (40, 56, 120))
    rng = np.random.default_rng(9)
    for _ in range(26):
        x, y = rng.uniform(20, w - 20), rng.uniform(20, h - 20)
        p.ell(x, y, 2.5, 2.5, PAPER, sh=False, out=0)
    cx, cy, r = w / 2, h / 2 - 10, 100
    p.ell(cx, cy, r, r, SEA, ht=True)
    for bx, by, br in [(-40, -30, 38), (30, -50, 26), (40, 20, 40), (-30, 40, 30), (-60, 5, 20)]:
        p.ell(cx + bx, cy + by, br, br * 0.7, LEAF, sh=False, out=4)
    p.d.ellipse([(cx - r) * p.S, (cy - r) * p.S, (cx + r) * p.S, (cy + r) * p.S], outline=INKC + (255,), width=OUT * p.S)
    p.d.arc([(cx - r) * p.S, (cy - r * 0.35) * p.S, (cx + r) * p.S, (cy + r * 0.35) * p.S], 0, 180,
            fill=INKC + (255,), width=3 * p.S)
    return p.done(key)


def campus_card(w=CW, h=CH):
    key = ("ilcampus", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, SKYC)
    gy = h - 150
    p.rect(4, gy, w, h, (226, 212, 184), sh=False, out=0)
    p.ln([(4, gy), (w, gy)], 5)
    blocks = [(40, 310, STEEL, 200), (310, 600, ORNG, 150), (600, 880, CORAL, 230)]
    for x0, x1, col, top in blocks:
        p.rect(x0, top, x1, gy, PAPER, ht=True)
        p.rect(x0, top, x1, top + 46, col, sh=False)
        for i in range(int((x1 - x0 - 30) / 60)):
            p.rect(x0 + 24 + i * 60, top + 80, x0 + 60 + i * 60, top + 110, SKYC, r=4, sh=False, out=3)
    p.rect(250, 60, 284, 200, NAVY, ht=True)          # chimenea de la planta de latas
    p.rect(660, gy - 86, 760, gy, NAVY, r=4, sh=False, out=4)
    p.rect(780, gy - 86, 860, gy, NAVY, r=4, sh=False, out=4)
    return p.done(key)


def truck_spr():
    key = ("iltruck",)
    if cached(key):
        return cached(key)
    p = Pen(250, 120)
    p.rect(10, 14, 170, 92, PAPER, r=6, ht=True, out=4)
    p.poly([(170, 92), (170, 34), (210, 34), (238, 62), (238, 92)], NAVY, ht=True, out=4)
    p.rect(180, 42, 206, 62, SKYC, sh=False, out=3)
    for x in (48, 136, 204):
        p.ell(x, 98, 15, 15, (40, 40, 56), sh=False, out=4)
    return p.done(key)


# ---------- contador de estaciones (pista 1/4 … 4/4) ----------
TRACK_Y = 1148


def track(fr, t, cur, labels, a=1.0, lit4=0.0):
    """cur: estación actual (1..4). Las anteriores, con palomita; la 4 queda con '?' hasta lit4>0."""
    if a <= 0.004:
        return
    d = fr.d
    xs = [190 + i * 233 for i in range(4)]
    y = TRACK_Y
    d.line([(xs[0], y), (xs[-1], y)], fill=_mixa(INKC, a), width=14)
    d.line([(xs[0], y), (xs[0] + (xs[-1] - xs[0]) * clamp((cur - 1) / 3), y)], fill=_mixa(TEALC, a), width=8)
    for i, x in enumerate(xs):
        n = i + 1
        done = n < cur or (n == 4 and lit4 > 0)
        now = n == cur and not (n == 4 and lit4 > 0)
        r = 40 if now else 32
        if now:
            r *= 1 + 0.06 * math.sin(t * 8)
        col = YELC if now else (TEALC if done else (70, 76, 110))
        if n == 4 and lit4 > 0:
            col, r = YELC, 44 * (1 + 0.25 * (1 - ease_out(lit4 / 0.4)))
        d.ellipse([x - r - 2, y - r + 6, x + r + 6, y + r + 10], fill=_mixa(INKC, a))
        d.ellipse([x - r, y - r, x + r, y + r], fill=_mixa(col, a), outline=_mixa(INKC, a), width=6)
        g = "?" if (n == 4 and lit4 <= 0) else ("✓" if done and n != 4 else str(n))
        if n == 4 and lit4 > 0:
            g = "4"
        say(fr, g, x, y - 2, 40, INKC, BLACK, a=a)
        say(fr, labels[i], x, y + 56, 26, PAPER if (now or done) else (150, 156, 190), HEAVY, a=a, maxw=220)


def _mixa(c, a):
    return tuple(int(v * a) for v in c) if a < 1 else c


def step_badge(fr, cur, a=1.0, s=1.0):
    put(fr, pill(f"{cur}/4", 44, INKC, YELC, 26, 14, BLACK), X1 - 70, KICK_Y, s, a, 4)


# ---------- escenas ----------
CY = 820


def _card_in(x):
    return slam(x, 1.25, 0.3), appear(x, 0.12)


def can_hook(fr, t, sc):
    """Pregunta completa desde el cuadro 1; cinta con latas que pasan de largo de la fábrica; sello '0' en 'zero'."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["q1"], W / 2, 380, 64, WHITE, BLACK, maxw=940)
    say(fr, p["q2"], W / 2, 480, 112, YEL, BLACK, s=0.85 + 0.15 * pop(x, 0.25), glow=(ORNG, 18, 1.2), maxw=960)
    say(fr, p["q3"], W / 2, 584, 76, WHITE, BLACK, s=0.85 + 0.15 * pop(x - 0.06, 0.25), maxw=960)
    say(fr, p["q4"], W / 2, 672, 64, CORAL, BLACK, s=0.85 + 0.15 * pop(x - 0.12, 0.25), maxw=960)
    cy = 950
    spr = ill_factory_card()
    put(fr, spr, W / 2, cy, 0.96 + 0.04 * pop(x, 0.3))
    ox, oy = W / 2 - spr.width / 2, cy - spr.height / 2
    belt_y = oy + 440 - 70 - 40
    for i in range(5):                      # latas que llegan por la cinta, de afuera
        u = (t * 160 + i * 74) % 370
        put(fr, can_spr(52), ox + 900 - u, belt_y - 46, 1.0, clamp((370 - u) / 40) * clamp(u / 30))
    for i in range(3):                      # humo apagado: solo dos bocanadas lentas
        ph = (t * 0.35 + i / 3) % 1.0
        r = 12 + 18 * ph
        fr.d.ellipse([ox + 420 - r + 30 * ph, oy + 52 - 30 * ph - r, ox + 420 + r + 30 * ph, oy + 52 - 30 * ph + r],
                     fill=tuple(int(200 + 30 * ph) for _ in range(3)))
    z = sc.lcues.get("zero")
    if z is not None and t > z:
        k = t - z
        put(fr, stamp(p["stamp"], 80, INKC), ox + 300, oy + 250, slam(k, 2.4, 0.22), appear(k, 0.05), -12)


S2.SFX["can_hook"] = lambda sc: [(sc.t0 + 0.1, "whoosh")] + ([(sc.lcues["zero"], "boom")] if "zero" in sc.lcues else [])


def can_mountain(fr, t, sc):
    """Montaña de latas que crece; cifra grande; '≈443 por segundo' con reloj; ventas en euros."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    sc_, al = _card_in(x)
    spr = ill_mountain_card()
    cy = 860
    put(fr, spr, W / 2, cy, sc_, al)
    ox, oy = W / 2 - spr.width / 2, cy - spr.height / 2
    gy = oy + CH - 60
    c = lc(sc, "cans")
    g = ease_out((t - c) / 2.2) if t > c else 0.0
    cw = 44
    rows = 5
    shown = int(g * 45)
    cnt = 0
    for r in range(rows):
        n = 13 - r * 2 + (0 if r < 6 else 0)
        n = max(1, n)
        for i in range(n):
            if cnt >= shown:
                break
            cxp = W / 2 + (i - (n - 1) / 2) * (cw + 8)
            cyp = gy - 40 - r * 70
            put(fr, can_spr(cw), cxp, cyp, 1.0, 1.0)
            cnt += 1
    if t > c:
        k = t - c
        val = 13.969 * p.get("big_mult", 1) * ease_out(k / 1.4)
        say(fr, p["big"].format(val), W / 2, 450, 120, YEL, BLACK, a=appear(k, 0.08), s=slam(k, 1.5, 0.22),
            glow=(ORNG, 18, 1.2), maxw=960)
        say(fr, p["big_l"], W / 2, 545, 40, WHITE, HEAVY, a=appear(k - 0.1, 0.2), maxw=900)
    s = sc.lcues.get("sec")
    if s is not None and t > s:
        k = t - s
        cxk, cyk = W / 2 + 330, oy + 110
        fr.d.ellipse([cxk - 74, cyk - 70, cxk + 82, cyk + 86], fill=INKC)
        fr.d.ellipse([cxk - 78, cyk - 78, cxk + 78, cyk + 78], fill=PAPER, outline=INKC, width=6)
        ang = t * 6.283
        fr.d.line([(cxk, cyk), (cxk + 60 * math.sin(ang), cyk - 60 * math.cos(ang))], fill=CORAL, width=7)
        fr.d.ellipse([cxk - 8, cyk - 8, cxk + 8, cyk + 8], fill=INKC)
        put(fr, pill(p["sec"], 46, INKC, YELC, 28, 16, BLACK), W / 2 - 150, oy + 80, slam(k, 1.8, 0.22), appear(k, 0.05), -3)
        put(fr, pill(p["tag"], 28, INKC, TEALC), W / 2 - 250, oy + 150, pop(k - 0.3, 0.3))
    r_ = sc.lcues.get("rev")
    if r_ is not None and t > r_:
        k = t - r_
        put(fr, pill(p["rev"], 60, WHITE, CORAL, 34, 20, BLACK), W / 2, 1180, slam(k, 1.8, 0.22), appear(k, 0.05), 2)


S2.SFX["can_mountain"] = lambda sc: ([(sc.lcues[c], s) for c, s in (("cans", "pop"), ("sec", "ding"), ("rev", "cash"))
                                       if c in sc.lcues])


STEP_ILL = dict(canmaker=ill_canmaker_card, filler=ill_filler_card, ship=ill_ship_card)


def chain_step(fr, t, sc):
    """Estación N de 4 en la vida de una lata. Tarjeta ilustrada animada + quién lo hace (cue 'who')."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    step_badge(fr, p["n"], s=slam(x, 1.8, 0.22))
    say(fr, p["title"], W / 2, 385, 92, WHITE, BLACK, a=appear(x, 0.1), s=slam(x, 1.4, 0.22), maxw=900)
    sc_, al = _card_in(x)
    spr = STEP_ILL[p["ill"]]()
    cyc = 838
    put(fr, spr, W / 2, cyc, sc_, al)
    ox, oy = W / 2 - spr.width / 2, cyc - spr.height / 2
    gy = oy + CH - 70
    if p["ill"] == "canmaker":
        ph = (t * 1.6) % 1.0
        ram = 30 * (1 - abs(1 - 2 * ph))
        fr.d.rectangle([ox + 440, oy + 200, ox + 500, oy + 250 + ram * 2], fill=(120, 132, 160), outline=INKC, width=5)
        for i in range(5):
            u = (t * 120 + i * 72) % 360
            put(fr, can_spr(46, True), ox + 580 + u, gy - 46 - 44, 1.0, clamp((360 - u) / 30) * clamp(u / 20))
    elif p["ill"] == "filler":
        for i in range(5):
            u = (t * 110 + i * 110) % 440
            cxp = ox + 450 + u
            put(fr, can_spr(48), cxp, gy - 46 - 46, 1.0, clamp((440 - u) / 30) * clamp(u / 20))
        for nx in NOZ:
            ph = (t * 2.2 + nx / 97) % 1.0
            yy = oy + 270 + ph * 120
            fr.d.ellipse([ox + nx - 7, yy - 10, ox + nx + 7, yy + 10], fill=ORNG, outline=INKC, width=3)
    elif p["ill"] == "ship":
        u = (t * 140) % 1500
        put(fr, train_spr(), ox - 400 + u, oy + 214, 1.0, 1.0)
        put(fr, ship_spr(), ox + 470 + 30 * math.sin(t * 0.7), oy + 360 + 6 * math.sin(t * 2.1), 1.0, 1.0,
            1.5 * math.sin(t * 1.7))
    w_ = sc.lcues.get("who")
    if w_ is not None and t > w_:
        k = t - w_
        put(fr, pill(p["who"], 50, INKC, YELC, 30, 18, BLACK), W / 2, 478, slam(k, 1.9, 0.22), appear(k, 0.05), -2)
        if p.get("who_sub"):
            say(fr, p["who_sub"], W / 2, 548, 32, WHITE, HEAVY, a=appear(k - 0.2, 0.25), maxw=900)
    track(fr, t, p["n"], p["labels"])


S2.SFX["chain_step"] = lambda sc: [(sc.t0 + 0.05, "pop")] + ([(sc.lcues["who"], "ding")] if "who" in sc.lcues else [])


def world_spend(fr, t, sc):
    """Dónde sí está Red Bull: tres viñetas que entran en sus cues con su cifra."""
    p = sc.p
    kick(fr, p["kicker"])
    say(fr, p["title"], W / 2, 400, 80, WHITE, BLACK, a=appear(t - sc.t0, 0.1), maxw=940)
    specs = [("ath", rider_vignette, p["l1"], p["n1"]), ("f1", car_vignette, p["l2"], p["n2"]),
             ("ctry", globe_vignette, p["l3"], p["n3"])]
    for j, (cue, fn, lab, num) in enumerate(specs):
        c = sc.lcues.get(cue)
        if c is None or t < c:
            continue
        k = t - c
        cx = 205 + j * 335
        cy = 800 + 10 * math.sin(t * 2 + j)
        spr = fn()
        rot = (-4, 2, 5)[j]
        put(fr, spr, cx, cy, slam(k, 1.5, 0.24), appear(k, 0.06), rot)
        ox, oy = cx - spr.width / 2, cy - spr.height / 2
        if j == 0:
            ph = (t * 0.9) % 1.0
            rx = ox + 50 + 180 * ph
            ry = oy + 250 - 190 * math.sin(math.pi * ph)
            put(fr, rider_spr(), rx, ry, 0.8, appear(k, 0.1), -30 + 60 * ph)
        elif j == 1:
            u = (t * 260) % 520
            put(fr, car_spr(), ox - 120 + u, oy + 236, 0.95, appear(k, 0.1))
        say(fr, num, cx, cy + 250, 88, YEL, BLACK, a=appear(k - 0.15, 0.1), s=slam(k - 0.15, 1.6, 0.22),
            glow=(ORNG, 16, 1.1))
        say(fr, lab, cx, cy + 320, 28, WHITE, HEAVY, a=appear(k - 0.25, 0.2), maxw=310)


S2.SFX["world_spend"] = lambda sc: [(sc.lcues[c], "pop") for c in ("ath", "f1", "ctry") if c in sc.lcues]


def campus(fr, t, sc):
    """Campus compartido en EE. UU.: latas (Ball), llenado (Rauch), almacén (Red Bull, resaltado en 'rb')."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    for j, (cue, txt) in enumerate((("az", p["pin1"]), ("nc", p["pin2"]))):
        c = lc(sc, cue)
        if t > c:
            k = t - c
            put(fr, pill(txt, 36, WHITE, NAVY, 24, 14, BLACK), W / 2 + (-215 if j == 0 else 215), 420,
                slam(k, 1.7, 0.22), appear(k, 0.05), (-3, 3)[j])
    sc_, al = _card_in(x)
    spr = campus_card()
    put(fr, spr, W / 2, CY + 20, sc_, al)
    ox, oy = W / 2 - spr.width / 2, CY + 20 - spr.height / 2
    gy = oy + CH - 150
    rb = sc.lcues.get("rb")
    blocks = [(40, 310, p["b1"], p["w1"]), (310, 600, p["b2"], p["w2"]), (600, 880, p["b3"], p["w3"])]
    for j, (x0, x1, lab, who) in enumerate(blocks):
        cxp = ox + (x0 + x1) / 2
        hot = j == 2 and rb is not None and t > rb
        say(fr, lab, cxp, gy + 32, 34, INKC, BLACK, maxw=260)
        say(fr, who, cxp, gy + 70, 30, CORAL if hot else NAVY, BLACK, maxw=260)
    for i in range(2):
        u = (t * 70 + i * 160) % 320
        put(fr, truck_spr(), ox + 900 - u, gy + 116, 0.5, clamp(u / 30) * clamp((320 - u) / 30))
    if rb is not None and t > rb:
        k = t - rb
        put(fr, panel(300, 380, (0, 0, 0, 0), YELC, 22, 9), ox + 740, gy - 150, 1.0, 0.45 + 0.55 * math.sin(t * 6) ** 2)
        put(fr, pill(p["rb"], 46, INKC, YELC, 28, 16, BLACK), W / 2, 1185, slam(k, 1.8, 0.22), appear(k, 0.05), -2)


S2.SFX["campus"] = lambda sc: ([(sc.lcues[c], "pop") for c in ("az", "nc") if c in sc.lcues] +
                               ([(sc.lcues["rb"], "boom")] if "rb" in sc.lcues else []))


def answer_track(fr, t, sc):
    """Pista completa: 1–3 hechas por otros, la 4 se enciende con la respuesta. Luego seguir/like (answer_cta)."""
    p = sc.p
    ans, fol = sc.lcues.get("ans"), sc.lcues.get("fol")
    mA = appear(t - ans, 0.3) if ans is not None and t > ans else 0.0
    mB = appear(t - fol, 0.3) if fol is not None and t > fol else 0.0
    a = 1 - mB
    lit = (t - ans) if ans is not None and t > ans else 0.0
    if a > 0.004:
        # tarjeta con la lata grande que sale de la pista
        x = t - sc.t0
        if mA < 1:
            put(fr, can_spr(170), W / 2, 830 + 14 * math.sin(t * 2.2), pop(x, 0.34), a * (1 - mA), 6 * math.sin(t * 1.3))
        track(fr, t, 4, p["labels"], a, lit4=lit)
    S2.answer_cta(fr, t, sc)


S2.SFX["answer_track"] = S2.SFX["answer_cta"]

for _n in ("can_hook", "can_mountain", "chain_step", "world_spend", "campus", "answer_track"):
    setattr(S2, _n, globals()[_n])

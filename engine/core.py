import os
"""Motor de video: lienzo, tipografia, sprites y elementos de marca.

Todo se dibuja a 1080x1920 y 30 fps. Las zonas seguras dejan libre la parte
baja (descripcion de TikTok/Reels/Shorts) y la columna de botones de la derecha.
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + "/"
if not os.path.exists(FD + "InterDisplay-Black.otf"):
    FD = "/usr/share/fonts/opentype/inter/"

WHITE, YEL, GRN, RED, DIM = (255, 255, 255), (255, 210, 63), (74, 222, 128), (255, 90, 95), (140, 150, 175)
BGC = (9, 13, 28)       # color medio del fondo (para desvanecer)
CARD = (21, 29, 58)     # relleno de tarjetas
EDGE = (50, 60, 98)     # bordes y pistas
BLACK, HEAVY, BOLD, SEMI = "InterDisplay-Black", "Inter-ExtraBold", "Inter-Bold", "Inter-SemiBold"

X0, X1 = 90, 990        # margen horizontal
MARK_Y = 214            # marca de agua
KICK_Y = 300            # rotulo superior
SRC_Y = 1262            # etiqueta de fuente
CAP_Y = 1400            # subtitulos
CAP_MAXW = 820


# ---------- utilidades ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_io(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def back_out(x):
    x = clamp(x)
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


def lerp(a, b, u):
    return a + (b - a) * u


def mix(c, a, base=BGC):
    """Color c con opacidad a sobre el fondo."""
    a = clamp(a)
    if a <= 0.004:
        return None          # invisible: los ayudantes de dibujo lo saltan
    return tuple(int(base[i] + (c[i] - base[i]) * a) for i in range(3))


_fonts = {}


def font(name, size):
    size = max(8, int(round(size)))
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FD + name + ".otf", size)
    return _fonts[key]


def fit(txt, name, size, maxw):
    """Fuente lo mas grande posible (hasta size) que cabe en maxw."""
    f = font(name, size)
    while f.getlength(txt) > maxw and size > 10:
        size *= 0.97
        f = font(name, size)
    return f


def text(d, xy, txt, f, fill, anchor="mm", stroke=0, sfill=(0, 0, 0)):
    if fill is None:
        return
    d.text(xy, txt, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sfill)


# Pillow dibuja en blanco cuando no recibe color; estos ayudantes no dibujan nada.
def line(d, pts, fill, width=1, joint=None):
    if fill is not None:
        d.line(pts, fill=fill, width=width, joint=joint)


def rrect(d, box, r, fill=None, outline=None, width=1):
    if fill is not None or outline is not None:
        d.rounded_rectangle(box, r, fill=fill, outline=outline, width=width)


def poly(d, pts, fill):
    if fill is not None:
        d.polygon(pts, fill=fill)


def oval(d, box, fill):
    if fill is not None:
        d.ellipse(box, fill=fill)


# ---------- fondo ----------
_yy = np.linspace(0, 1, H)[:, None]
_xx = np.linspace(-1, 1, W)[None, :]
_top, _bot = np.array([14, 20, 44.0]), np.array([4, 6, 12.0])
_bg = _top[None, None, :] * (1 - _yy)[..., None] + _bot[None, None, :] * _yy[..., None]
_bg = _bg * (1 - 0.35 * (_xx ** 2))[..., None]
BG = np.clip(_bg, 0, 255).astype(np.uint8)


class Frame:
    def __init__(self, t):
        self.t = t
        self.im = Image.fromarray(BG.copy())
        self.d = ImageDraw.Draw(self.im)
        d = self.d
        off = (t * 18) % 120
        y = -120 + off
        while y < H:
            d.line([(0, y), (W, y)], fill=(22, 30, 58), width=1)
            y += 120
        for x in range(60, W, 120):
            d.line([(x, 0), (x, H)], fill=(18, 25, 50), width=1)

    def paste(self, spr, cx, cy, alpha=1.0):
        if alpha <= 0.004:
            return
        box = (int(round(cx - spr.width / 2)), int(round(cy - spr.height / 2)))
        if alpha >= 0.996:
            self.im.paste(spr, box, spr)
        else:
            m = spr.getchannel("A").point(lambda v: int(v * alpha))
            self.im.paste(spr, box, m)


# ---------- sprites (dibujados a 4x y reducidos, para bordes limpios) ----------
_spr = {}
SS = 4


def asterisk(size, color=YEL, rot=0.0):
    key = ("ast", int(size), color, int(round(rot)))
    if key not in _spr:
        n = int(size) * SS
        im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        r = n * 0.115
        arm = n / 2 - r - SS
        c = n / 2
        for ang in (90, 30, 150):
            a = math.radians(ang + rot)
            dx, dy = math.cos(a) * arm, math.sin(a) * arm
            nx, ny = -math.sin(a) * r, math.cos(a) * r
            d.polygon([(c - dx + nx, c - dy + ny), (c + dx + nx, c + dy + ny),
                       (c + dx - nx, c + dy - ny), (c - dx - nx, c - dy - ny)], fill=color + (255,))
            for s in (-1, 1):
                x, y = c + s * dx, c + s * dy
                d.ellipse([x - r, y - r, x + r, y + r], fill=color + (255,))
        _spr[key] = im.resize((int(size), int(size)), Image.LANCZOS)
    return _spr[key]


def hotdog(width):
    key = ("dog", int(width))
    if key not in _spr:
        w = int(width) * SS
        h = int(w * 0.44)
        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([0.07 * w, 0.03 * h, 0.93 * w, 0.72 * h], 0.30 * h, fill=(202, 138, 70, 255))
        d.rounded_rectangle([0.0, 0.19 * h, w - 1, 0.67 * h], 0.24 * h, fill=(184, 70, 48, 255))
        d.rounded_rectangle([0.07 * w, 0.245 * h, 0.93 * w, 0.30 * h], 0.03 * h, fill=(212, 104, 78, 255))
        pts, n = [], 11
        for i in range(n):
            x = lerp(0.13 * w, 0.87 * w, i / (n - 1))
            y = 0.43 * h + (0.075 * h if i % 2 else -0.075 * h)
            pts.append((x, y))
        d.line(pts, fill=YEL + (255,), width=int(0.062 * h), joint="curve")
        for x, y in (pts[0], pts[-1]):
            rr = 0.031 * h
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=YEL + (255,))
        d.rounded_rectangle([0.05 * w, 0.50 * h, 0.95 * w, 0.985 * h], 0.27 * h, fill=(236, 178, 104, 255))
        d.rounded_rectangle([0.12 * w, 0.545 * h, 0.88 * w, 0.585 * h], 0.02 * h, fill=(247, 204, 140, 255))
        _spr[key] = im.resize((int(width), int(h / SS)), Image.LANCZOS)
    return _spr[key]


def pin(size, color=GRN):
    key = ("pin", int(size), color)
    if key not in _spr:
        n = int(size) * SS
        im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        r = n * 0.30
        cx, cy = n / 2, n * 0.36
        d.polygon([(cx - r * 0.86, cy + r * 0.5), (cx + r * 0.86, cy + r * 0.5), (cx, n * 0.97)], fill=color + (255,))
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (255,))
        d.ellipse([cx - r * 0.40, cy - r * 0.40, cx + r * 0.40, cy + r * 0.40], fill=CARD + (255,))
        _spr[key] = im.resize((int(size), int(size)), Image.LANCZOS)
    return _spr[key]


def ring(size, thick, frac, color=YEL, track=EDGE):
    """Anillo de progreso (no se guarda en cache: cambia cada cuadro)."""
    S = 3
    n = int(size) * S
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    w = int(thick * S)
    box = [w / 2, w / 2, n - w / 2, n - w / 2]
    d.arc(box, 0, 360, fill=track + (255,), width=w)
    if frac > 0.001:
        end = -90 + 360 * clamp(frac)
        d.arc(box, -90, end, fill=color + (255,), width=w)
        rad = (n - w) / 2
        for ang in (-90, end):
            a = math.radians(ang)
            x, y = n / 2 + rad * math.cos(a), n / 2 + rad * math.sin(a)
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=color + (255,))
    return im.resize((int(size), int(size)), Image.LANCZOS)


# ---------- elementos fijos ----------
def kicker(fr, txt, a=1.0, color=DIM):
    text(fr.d, (W / 2, KICK_Y), txt, fit(txt, SEMI, 44, 860), mix(color, a))


def watermark(fr, txt):
    fr.paste(asterisk(30), X0 + 15, MARK_Y, 0.9)
    text(fr.d, (X0 + 42, MARK_Y), txt, font(BOLD, 27), mix(DIM, 0.8), "lm")


def source_tag(fr, txt, a=1.0, color=DIM):
    if a <= 0.004 or not txt:
        return
    fr.paste(asterisk(30), X0 + 15, SRC_Y, a)
    text(fr.d, (X0 + 42, SRC_Y), txt, fit(txt, SEMI, 30, 830), mix(color, a), "lm")


def progress(fr, frac):
    fr.d.rectangle([0, 0, W * clamp(frac), 8], fill=YEL)


def card(d, box, a=1.0, fill=CARD, outline=EDGE, radius=30, width=3):
    rrect(d, box, radius, mix(fill, a) if fill else None, mix(outline, a) if outline else None, width)


# ---------- subtitulos ----------
def build_chunks(tokens):
    """Bloques de 2 o 3 palabras: corta en la puntuacion y no deja una palabra sola al final."""
    segs, cur = [], []
    for tk in tokens:
        if not tk["cap"] or not tk["display"]:
            if cur:
                segs.append(cur)
                cur = []
            continue
        cur.append(tk)
        if tk["display"][-1] in ".?!,:;" or tk["last"]:
            segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    chunks = []
    for seg in segs:
        n, i = len(seg), 0
        while n > 0:
            sz = 2 if n == 4 else min(3, n)
            chunks.append(seg[i:i + sz])
            i += sz
            n -= sz
    return chunks


def captions(fr, t, chunks):
    d = fr.d
    for ch in chunks:
        a, b = ch[0]["start"], ch[-1]["end"]
        if a - 0.04 <= t < b + 0.16:
            size = 84
            words = [w["cdisp"] for w in ch]
            f = font(HEAVY, size)
            sp = f.getlength(" ") + 10
            total = sum(f.getlength(w) for w in words) + sp * (len(words) - 1)
            if total > CAP_MAXW:
                size *= CAP_MAXW / total
            pop = 0.9 + 0.1 * back_out((t - a + 0.04) / 0.14)
            f = font(HEAVY, size * pop)
            sp = f.getlength(" ") + 10
            ws = [f.getlength(w) for w in words]
            x = W / 2 - (sum(ws) + sp * (len(ws) - 1)) / 2
            for w, wl in zip(ch, ws):
                active = w["start"] <= t < w["end"] + (0.16 if w is ch[-1] else 0.0)
                ff = font(HEAVY, size * pop * (1.04 if active else 1.0))
                text(d, (x + wl / 2, CAP_Y), w["cdisp"], ff, YEL if active else WHITE, "mm", 9)
                x += wl + sp
            return

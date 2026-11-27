"""Estilo v4 (23 nov. 2026; referencia: reel de la florería, doc 11 del proyecto).

Un solo escenario fijo (pared de ladrillo, foco cálido, mostrador de madera), barra de serie
arriba ("EL ASTERISCO DE · EMPRESA" + número), texto grande arriba con una palabra en rojo o en
píldora, capítulos numerados y utilería 2D que entra con rebote y suena al entrar.

Uso en el spec:
    v4=dict(series="EL ASTERISCO DE · STARBUCKS", ep="#1"),
    beats=[dict(scene="v4", p=dict(chapter="01 · LA RECARGA",
                heads=[dict(lines=["STARBUCKS LES *DEBE*", "$1,750 MILLONES"]),
                       dict(cue="pay", lines=["YA ESTÁ EN", "[SU CAJA.]"])],
                props=[dict(kind="cup", x=540, y=1180, cue="q"), ...]),
                lines=[...]), ...]
Marcado de texto: *palabra* = roja; [una o varias palabras] = píldora roja.
"""
import math
import re

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from core import *          # noqa: F401,F403
import scenes2 as S2

ANTON = FD + "Anton-Regular.ttf"
BG4 = (26, 20, 18)
BRICK = (40, 31, 28)
RED4 = (229, 9, 20)
CREAM = (255, 243, 214)
YEL4 = (245, 196, 66)
WOOD = (92, 58, 38)
WOOD_D = (66, 40, 26)
INK = (30, 22, 18)
GREEN4 = (39, 174, 96)
COUNTER = 1400          # línea del mostrador (la utilería se apoya aquí)
HEAD_Y = 236
CHAP_Y = 345

_f = {}


def af(size):
    size = max(10, int(size))
    if size not in _f:
        _f[size] = ImageFont.truetype(ANTON, size)
    return _f[size]


# ---------------- fondo fijo ----------------
_BASE = None


def _base():
    global _BASE
    if _BASE is not None:
        return _BASE
    im = Image.new("RGB", (W, H), BG4)
    d = ImageDraw.Draw(im)
    bw, bh = 120, 56
    for row in range(H // bh + 2):
        off = bw // 2 if row % 2 else 0
        y = row * bh
        for col in range(-1, W // bw + 2):
            x = col * bw + off
            d.rounded_rectangle([x + 3, y + 3, x + bw - 3, y + bh - 3], 6, fill=BRICK)
    glow = Image.new("L", (W, H), 0)
    g = ImageDraw.Draw(glow)
    cx, cy = W // 2, 1120
    for r in range(720, 0, -10):
        g.ellipse([cx - r, cy - r * 0.9, cx + r, cy + r * 0.9], fill=int(120 * (1 - r / 720)))
    glow = glow.filter(ImageFilter.GaussianBlur(40)).point(lambda v: v // 2)
    im = Image.composite(Image.new("RGB", (W, H), (120, 80, 50)), im, glow)
    d = ImageDraw.Draw(im)
    d.rectangle([0, COUNTER, W, COUNTER + 40], fill=WOOD)
    d.rectangle([0, COUNTER + 40, W, H], fill=WOOD_D)
    for x in range(0, W, 180):
        d.line([x, COUNTER + 40, x, H], fill=(56, 34, 22), width=4)
    vig = Image.new("L", (W, H), 0)
    v = ImageDraw.Draw(vig)
    for i in range(0, 260, 4):
        v.rectangle([i, i, W - i, H - i], outline=int(150 * (1 - i / 260)))
    vig = vig.filter(ImageFilter.GaussianBlur(30))
    im = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), im, vig)
    _BASE = np.asarray(im).copy()
    return _BASE


class Frame4:
    def __init__(self, t, spec):
        self.t = t
        self.im = Image.fromarray(_base().copy())
        self.d = ImageDraw.Draw(self.im)
        self.cfg = spec.get("v4", {})

    def paste(self, spr, cx, cy, alpha=1.0):
        if alpha <= 0.004:
            return
        box = (int(round(cx - spr.width / 2)), int(round(cy - spr.height / 2)))
        if alpha >= 0.996:
            self.im.paste(spr, box, spr)
        else:
            m = spr.getchannel("A").point(lambda v: int(v * alpha))
            self.im.paste(spr, box, m)


def _scaled(spr, s):
    if abs(s - 1) < 0.01:
        return spr
    return spr.resize((max(1, int(spr.width * s)), max(1, int(spr.height * s))), Image.BILINEAR)


def bounce(k, dur=0.32):
    """0 antes de entrar; luego sube con rebote hasta 1."""
    if k <= 0:
        return 0.0
    return back_out(k / dur)


# ---------------- barra de serie y capítulo ----------------
def header(fr, series, ep):
    d = fr.d
    fr.paste(asterisk(34, YEL4), X0 + 10, HEAD_Y)
    text(d, (X0 + 40, HEAD_Y), series, fit(series, BOLD, 32, 700), CREAM, "lm")
    if ep:
        f = font(BLACK, 32)
        tw = f.getlength(ep)
        d.rounded_rectangle([X1 - tw - 36, HEAD_Y - 25, X1, HEAD_Y + 25], 8, fill=RED4)
        text(d, (X1 - tw / 2 - 18, HEAD_Y), ep, f, WHITE)
    d.line([X0, HEAD_Y + 46, X1, HEAD_Y + 46], fill=(70, 55, 50), width=2)


def chapter(fr, txt, k):
    u = bounce(k)
    if u <= 0:
        return
    f = font(BLACK, 38)
    tw = f.getlength(txt)
    spr = Image.new("RGBA", (int(tw + 60), 64), (0, 0, 0, 0))
    g = ImageDraw.Draw(spr)
    g.rounded_rectangle([0, 0, spr.width - 1, 63], 10, fill=RED4 + (255,))
    g.text((spr.width / 2, 32), txt, font=f, fill=WHITE, anchor="mm")
    fr.paste(_scaled(spr, 0.6 + 0.4 * u), W / 2, CHAP_Y, min(1, k / 0.12))


# ---------------- titular con palabra roja / píldora ----------------
_TOK = re.compile(r"\[[^\]]+\][^\s\[*]*|\*[^*]+\*[^\s\[*]*|\S+")
_lines = {}


def _parse(line):
    out = []
    for m in _TOK.findall(line):
        if m.startswith("["):
            j = m.index("]")
            out.append((m[1:j] + m[j + 1:], "pill"))
        elif m.startswith("*"):
            j = m.index("*", 1)
            body, tail = m[1:j], m[j + 1:]
            out.append((body, "red"))
            if tail:
                out.append((tail, "glue"))
        else:
            out.append((m, "w"))
    return out


def _plain(line):
    return " ".join(t for t, _ in _parse(line))


def _line_sprite(line, size):
    key = (line, size)
    if key in _lines:
        return _lines[key]
    parts = _parse(line)
    f = af(size)
    gap = size * 0.22
    ws = [f.getlength(t) for t, _ in parts]
    gaps = [0.0 if (i + 1 < len(parts) and parts[i + 1][1] == "glue") else gap for i in range(len(parts))]
    padx = 26
    total = sum(ws) + sum(gaps[:-1])
    h = int(size * 1.45)
    spr = Image.new("RGBA", (int(total + 2 * padx + 20), h + 30), (0, 0, 0, 0))
    sh = Image.new("RGBA", spr.size, (0, 0, 0, 0))
    g, gs = ImageDraw.Draw(spr), ImageDraw.Draw(sh)
    x, cy = padx, spr.height / 2
    for (t, st), w, gp in zip(parts, ws, gaps):
        if st == "pill":
            g.rounded_rectangle([x - 14, cy - size * 0.58, x + w + 14, cy + size * 0.58], 12, fill=RED4 + (255,))
        else:
            gs.text((x + 6, cy + 8), t, font=f, fill=(0, 0, 0, 210), anchor="lm")
        x += w + gp
    sh = sh.filter(ImageFilter.GaussianBlur(9))
    spr = Image.alpha_composite(sh, spr)
    g = ImageDraw.Draw(spr)
    x = padx
    for (t, st), w, gp in zip(parts, ws, gaps):
        g.text((x, cy), t, font=f, fill=(RED4 if st == "red" else WHITE) + (255,), anchor="lm")
        x += w + gp
    _lines[key] = spr
    return spr


def headline(fr, lines, k, top, max_size=118, maxw=930):
    if k < 0 or not lines:
        return
    size = max_size
    while size > 50 and max(af(size).getlength(_plain(l)) + size * 0.22 * (len(_parse(l)) - 1)
                            for l in lines) > maxw:
        size -= 4
    lh = size * 1.12
    for i, l in enumerate(lines):
        kk = k - i * 0.11
        u = bounce(kk, 0.28)
        if u <= 0:
            continue
        spr = _line_sprite(l, size)
        fr.paste(_scaled(spr, 0.86 + 0.14 * u), W / 2, top + lh * (i + 0.5), min(1, kk / 0.1))


# ---------------- utilería ----------------
_spr4 = {}


def _canvas(w, h):
    im = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def _done(key, im):
    out = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    _spr4[key] = out
    return out


def gift_card(label="GIFT CARD", col=RED4):
    key = ("card", label, col)
    if key in _spr4:
        return _spr4[key]
    im, g = _canvas(380, 240)
    g.rounded_rectangle([8, 8, 752, 472], 40, fill=(0, 0, 0, 90))
    g.rounded_rectangle([0, 0, 744, 464], 40, fill=CREAM + (255,), outline=INK + (255,), width=8)
    g.rectangle([4, 110, 740, 190], fill=col + (255,))
    g.text((372, 330), label, font=font(BLACK, 92), fill=INK + (255,), anchor="mm")
    g.rounded_rectangle([60, 400, 300, 430], 12, fill=(205, 190, 165, 255))
    for i in range(3):
        g.ellipse([560 + i * 46, 392, 600 + i * 46, 432], fill=(205, 190, 165, 255))
    return _done(key, im)


def cup(label="CAFÉ"):
    key = ("cup", label)
    if key in _spr4:
        return _spr4[key]
    im, g = _canvas(260, 400)
    g.polygon([(40, 150), (480, 150), (430, 790), (90, 790)], fill=CREAM + (255,), outline=INK + (255,))
    g.line([(40, 150), (90, 790), (430, 790), (480, 150)], fill=INK + (255,), width=8)
    g.polygon([(66, 380), (456, 380), (440, 600), (82, 600)], fill=(150, 98, 60, 255))
    g.text((260, 490), label, font=font(BLACK, 74), fill=CREAM + (255,), anchor="mm")
    g.rounded_rectangle([14, 92, 506, 166], 26, fill=(235, 235, 235, 255), outline=INK + (255,), width=8)
    g.rounded_rectangle([110, 50, 410, 104], 20, fill=(235, 235, 235, 255), outline=INK + (255,), width=8)
    for i in range(3):                                   # vapor
        x = 190 + i * 70
        g.arc([x - 30, -40, x + 30, 40], 200, 340, fill=(255, 255, 255, 170), width=10)
    return _done(key, im)


def phone(title, amount):
    im, g = _canvas(320, 580)
    g.rounded_rectangle([0, 0, 638, 1158], 70, fill=(28, 28, 34, 255), outline=INK + (255,), width=8)
    g.rounded_rectangle([30, 70, 608, 1090], 40, fill=CREAM + (255,))
    g.rounded_rectangle([250, 26, 390, 46], 10, fill=(70, 70, 80, 255))
    g.text((319, 210), title, font=font(BOLD, 52), fill=(120, 100, 90, 255), anchor="mm")
    f = af(150)
    while f.getlength(amount) > 540 and f.size > 40:
        f = af(f.size - 6)
    g.text((319, 420), amount, font=f, fill=RED4 + (255,), anchor="mm")
    g.rounded_rectangle([90, 640, 548, 760], 60, fill=RED4 + (255,))
    g.text((319, 700), "+ RECARGAR" if "SALDO" in title else "+ RELOAD", font=font(BLACK, 54),
           fill=WHITE + (255,), anchor="mm")
    for i in range(3):
        g.rounded_rectangle([90, 820 + i * 80, 548, 870 + i * 80], 16, fill=(225, 212, 190, 255))
    return im.resize((320, 580), Image.LANCZOS)


def stamp_spr(txt, angle=-10):
    key = ("stamp", txt, angle)
    if key in _spr4:
        return _spr4[key]
    f = font(BLACK, 66)
    tw = int(f.getlength(txt))
    lay = Image.new("RGBA", (tw + 90, 150), (0, 0, 0, 0))
    l = ImageDraw.Draw(lay)
    l.rounded_rectangle([5, 5, tw + 85, 145], 16, outline=RED4 + (255,), width=9, fill=RED4 + (46,))
    l.text(((tw + 90) / 2, 75), txt, font=f, fill=RED4 + (255,), anchor="mm")
    out = lay.rotate(angle, expand=True, resample=Image.BICUBIC)
    _spr4[key] = out
    return out


def tag_spr(big, small):
    key = ("tag", big, small)
    if key in _spr4:
        return _spr4[key]
    f = af(80)
    bw = int(max(f.getlength(big), font(BOLD, 26).getlength(small)) + 70)
    im = Image.new("RGBA", (bw + 20, 170), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    g.polygon([(4, 24), (bw, 4), (bw + 10, 138), (10, 156)], fill=YEL4 + (255,))
    g.text((34, 66), big, font=f, fill=INK + (255,), anchor="lm")
    g.text((36, 128), small, font=font(BOLD, 26), fill=INK + (255,), anchor="lm")
    _spr4[key] = im
    return im


def bubble_spr(txt, n_chars, who="TÚ"):
    f = font(BOLD, 46)
    shown = txt[:n_chars]
    tw = max(f.getlength(txt), 300)
    w, h = int(tw + 170), 130
    im = Image.new("RGBA", (w + 10, h + 40), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    g.rounded_rectangle([6, 6, w + 6, h + 6], 34, fill=(0, 0, 0, 90))
    g.rounded_rectangle([0, 0, w, h], 34, fill=(255, 255, 255, 255), outline=INK + (255,), width=4)
    g.polygon([(70, h - 2), (110, h - 2), (66, h + 34)], fill=(255, 255, 255, 255))
    g.ellipse([22, 27, 98, 103], fill=RED4 + (255,))
    g.text((60, 65), who, font=font(BLACK, 28), fill=WHITE + (255,), anchor="mm")
    g.text((122, 65), shown, font=f, fill=INK + (255,), anchor="lm")
    if n_chars < len(txt):
        x = 122 + f.getlength(shown) + 4
        g.rectangle([x, 42, x + 4, 88], fill=INK + (255,))
    return im


def person_spr(mood="smile", shirt=(52, 90, 140)):
    key = ("person", mood, shirt)
    if key in _spr4:
        return _spr4[key]
    im, g = _canvas(260, 520)
    cx, cy = 260, 300
    g.rounded_rectangle([cx - 240, cy + 180, cx + 240, cy + 900], 180, fill=shirt + (255,))
    g.ellipse([cx - 190, cy - 220, cx + 190, cy + 180], fill=(226, 170, 128, 255))
    g.chord([cx - 200, cy - 240, cx + 200, cy + 80], 180, 360, fill=(40, 28, 24, 255))
    for ex in (-76, 76):
        g.ellipse([cx + ex - 24, cy - 12, cx + ex + 24, cy + 44], fill=INK + (255,))
        g.ellipse([cx + ex - 8, cy - 4, cx + ex + 6, cy + 12], fill=WHITE + (255,))
    if mood == "shock":
        g.ellipse([cx - 34, cy + 70, cx + 34, cy + 150], fill=INK + (255,))
        g.line([(cx - 120, cy - 70), (cx - 40, cy - 90)], fill=INK + (255,), width=12)
        g.line([(cx + 40, cy - 90), (cx + 120, cy - 70)], fill=INK + (255,), width=12)
    elif mood == "think":
        g.line([(cx - 40, cy + 110), (cx + 40, cy + 100)], fill=INK + (255,), width=12)
    else:
        g.arc([cx - 80, cy + 30, cx + 80, cy + 130], 15, 165, fill=INK + (255,), width=14)
    return _done(key, im)


def bank_spr(label="BANCO"):
    key = ("bank", label)
    if key in _spr4:
        return _spr4[key]
    im, g = _canvas(340, 360)
    g.polygon([(340, 10), (660, 170), (20, 170)], fill=CREAM + (255,), outline=INK + (255,))
    g.line([(340, 10), (660, 170), (20, 170), (340, 10)], fill=INK + (255,), width=8)
    g.rectangle([40, 170, 640, 220], fill=CREAM + (255,), outline=INK + (255,), width=8)
    for i in range(5):
        x = 80 + i * 124
        g.rectangle([x, 230, x + 60, 610], fill=CREAM + (255,), outline=INK + (255,), width=8)
    g.rectangle([20, 610, 660, 700], fill=CREAM + (255,), outline=INK + (255,), width=8)
    g.text((340, 655), label, font=font(BLACK, 58), fill=INK + (255,), anchor="mm")
    return _done(key, im)


def badge_spr(txt, col):
    key = ("badge", txt, col)
    if key in _spr4:
        return _spr4[key]
    f = font(BLACK, 54)
    tw = int(f.getlength(txt))
    im = Image.new("RGBA", (tw + 70, 96), (0, 0, 0, 0))
    g = ImageDraw.Draw(im)
    g.rounded_rectangle([0, 0, tw + 69, 95], 48, fill=col + (255,), outline=INK + (255,), width=4)
    g.text(((tw + 70) / 2, 48), txt, font=f, fill=WHITE + (255,), anchor="mm")
    _spr4[key] = im
    return im



# ---------------- utilería de marca (25 nov.: prueba de 5 días con marcas reales) ----------------
# La marca va como TEXTO sobre su color. Si Mitre aporta el archivo oficial del logo
# (assets_externos/, con su licencia anotada), se pasa con logo="ruta.png" y se pega encima.
_logo_cache = {}


def _logo(path, maxw, maxh):
    key = (path, maxw, maxh)
    if key in _logo_cache:
        return _logo_cache[key]
    try:
        im = Image.open(path).convert("RGBA")
    except Exception:
        _logo_cache[key] = None
        return None
    r = min(maxw / im.width, maxh / im.height)
    im = im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)
    _logo_cache[key] = im
    return im


def _brand_text(g, cx, cy, txt, maxw, size, col=WHITE):
    f = af(size)
    while f.getlength(txt) > maxw and f.size > 20:
        f = af(f.size - 4)
    g.text((cx + 4, cy + 5), txt, font=f, fill=(0, 0, 0, 120), anchor="mm")
    g.text((cx, cy), txt, font=f, fill=col + (255,), anchor="mm")


def store_spr(brand="COCA-COLA", sub="ABARROTES LA ESQUINA", col=RED4, logo=None, sign="HAY HIELO"):
    key = ("store", brand, sub, col, logo, sign)
    if key in _spr4:
        return _spr4[key]
    w, h = 700, 640
    im, g = _canvas(w, h)
    W2, H2 = w * 2, h * 2
    g.rectangle([0, 160, W2, H2], fill=(236, 224, 196, 255), outline=INK + (255,), width=10)     # fachada
    for yy in range(240, H2, 70):                                                                 # aplanado
        g.line([(10, yy), (W2 - 10, yy)], fill=(222, 208, 178, 255), width=3)
    g.rectangle([0, 0, W2, 250], fill=col + (255,), outline=INK + (255,), width=10)              # toldo
    for i in range(0, W2, 140):
        g.pieslice([i, 190, i + 140, 320], 0, 180, fill=col + (255,), outline=INK + (255,), width=8)
    if logo and _logo(logo, W2 - 200, 150) is not None:
        lg = _logo(logo, W2 - 200, 150)
        im.paste(lg, (int(W2 / 2 - lg.width / 2), int(110 - lg.height / 2)), lg)
    else:
        _brand_text(g, W2 / 2, 112, brand, W2 - 220, 150)
    g.rectangle([300, 330, W2 - 300, 400], fill=(255, 255, 255, 255), outline=INK + (255,), width=6)
    _brand_text(g, W2 / 2, 366, sub, W2 - 640, 50, INK)
    g.rectangle([260, 430, W2 - 260, H2 - 10], fill=(120, 82, 54, 255), outline=INK + (255,), width=10)   # puerta
    cols = [(229, 9, 20), (39, 174, 96), (245, 196, 66), (52, 90, 140), (255, 140, 40), (180, 60, 160)]
    for r in range(4):                                                                             # anaqueles
        yy = 480 + r * 150
        g.rectangle([280, yy + 110, W2 - 280, yy + 122], fill=(70, 46, 30, 255))
        for c in range(9):
            xx = 300 + c * 92
            if xx + 70 > W2 - 290:
                break
            cc = cols[(r * 3 + c) % len(cols)]
            g.rounded_rectangle([xx, yy + 20 + (c % 2) * 14, xx + 70, yy + 110], 8, fill=cc + (255,), outline=INK + (255,), width=4)
    if sign:                                                                                       # letrero de cartón
        g.polygon([(30, 520), (230, 500), (240, 640), (40, 660)], fill=(255, 255, 255, 255), outline=INK + (255,))
        g.text((135, 580), sign, font=font(BLACK, 40), fill=RED4 + (255,), anchor="mm")
    return _done(key, im)


def fridge_spr(brand="COCA-COLA", col=RED4, logo=None, bottle_col=(70, 30, 20), ribbon=False):
    key = ("fridge", brand, col, logo, bottle_col, ribbon)
    if key in _spr4:
        return _spr4[key]
    w, h = 300, 600
    im, g = _canvas(w, h)
    W2, H2 = w * 2, h * 2
    g.rounded_rectangle([0, 0, W2, H2], 40, fill=col + (255,), outline=INK + (255,), width=10)
    if logo and _logo(logo, W2 - 80, 120) is not None:
        lg = _logo(logo, W2 - 80, 120)
        im.paste(lg, (int(W2 / 2 - lg.width / 2), int(90 - lg.height / 2)), lg)
    else:
        _brand_text(g, W2 / 2, 92, brand, W2 - 80, 110)
    g.rounded_rectangle([50, 180, W2 - 50, H2 - 120], 20, fill=(200, 230, 245, 255), outline=INK + (255,), width=8)
    for r in range(5):                                                                             # botellas
        yy = 210 + r * 170
        g.rectangle([60, yy + 150, W2 - 60, yy + 160], fill=(150, 170, 180, 255))
        for c in range(5):
            xx = 90 + c * 92
            g.rounded_rectangle([xx + 18, yy + 10, xx + 46, yy + 50], 8, fill=bottle_col + (255,))
            g.rounded_rectangle([xx, yy + 46, xx + 64, yy + 150], 16, fill=bottle_col + (255,))
            g.rectangle([xx, yy + 82, xx + 64, yy + 112], fill=col + (255,))
    g.line([(110, 200), (110, H2 - 150)], fill=(255, 255, 255, 200), width=12)                    # brillo
    g.rounded_rectangle([W2 - 90, 500, W2 - 66, 760], 10, fill=(230, 230, 230, 255), outline=INK + (255,), width=4)
    g.rectangle([40, H2 - 100, W2 - 40, H2 - 30], fill=(40, 40, 44, 255))
    if ribbon:
        g.rectangle([W2 / 2 - 30, 0, W2 / 2 + 30, H2], fill=YEL4 + (255,))
        g.rectangle([0, H2 * 0.45 - 30, W2, H2 * 0.45 + 30], fill=YEL4 + (255,))
        g.ellipse([W2 / 2 - 110, -60, W2 / 2 - 10, 40], outline=YEL4 + (255,), width=26)
        g.ellipse([W2 / 2 + 10, -60, W2 / 2 + 110, 40], outline=YEL4 + (255,), width=26)
    return _done(key, im)


def bottle_spr(label="COCA-COLA", col=RED4, liquid=(70, 30, 20)):
    key = ("bottle", label, col, liquid)
    if key in _spr4:
        return _spr4[key]
    w, h = 170, 460
    im, g = _canvas(w, h)
    W2 = w * 2
    g.rounded_rectangle([W2 / 2 - 34, 0, W2 / 2 + 34, 40], 8, fill=(200, 30, 30, 255), outline=INK + (255,), width=6)   # tapa
    g.polygon([(W2 / 2 - 30, 40), (W2 / 2 + 30, 40), (W2 - 40, 300), (40, 300)], fill=liquid + (255,), outline=INK + (255,))
    g.rounded_rectangle([30, 280, W2 - 30, 900], 50, fill=liquid + (255,), outline=INK + (255,), width=8)
    g.rectangle([30, 470, W2 - 30, 640], fill=col + (255,), outline=INK + (255,), width=6)
    f = af(70)
    while f.getlength(label) > 560 and f.size > 20:
        f = af(f.size - 4)
    lay = Image.new("RGBA", (600, 160), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((300, 80), label, font=f, fill=(255, 255, 255, 255), anchor="mm")
    lay = lay.rotate(90, expand=True).resize((150, 300), Image.LANCZOS)
    lay = lay.resize((int(lay.width * 0.9), 160), Image.LANCZOS)
    im.paste(lay, (int(W2 / 2 - lay.width / 2), 475), lay)
    g.line([(70, 330), (70, 860)], fill=(255, 255, 255, 140), width=14)
    return _done(key, im)


def jug_spr(label="CONCENTRADO"):
    key = ("jug", label)
    if key in _spr4:
        return _spr4[key]
    w, h = 360, 420
    im, g = _canvas(w, h)
    W2, H2 = w * 2, h * 2
    g.rounded_rectangle([200, 0, 360, 90], 16, fill=(60, 60, 64, 255), outline=INK + (255,), width=6)
    g.rounded_rectangle([0, 80, W2, H2], 70, fill=(235, 235, 228, 255), outline=INK + (255,), width=10)
    g.rounded_rectangle([20, 360, W2 - 20, H2 - 20], 56, fill=(70, 30, 20, 255))
    g.arc([W2 - 230, 120, W2 - 40, 330], 270, 90, fill=INK + (255,), width=26)
    g.rounded_rectangle([60, 190, W2 - 60, 330], 16, fill=YEL4 + (255,), outline=INK + (255,), width=6)
    _brand_text(g, W2 / 2, 260, label, W2 - 160, 90, INK)
    return _done(key, im)


def truck_spr(label="EMBOTELLADORA", col=(240, 240, 236), txt_col=RED4):
    key = ("truck", label, col, txt_col)
    if key in _spr4:
        return _spr4[key]
    w, h = 620, 330
    im, g = _canvas(w, h)
    g.rounded_rectangle([0, 20, 860, 520], 24, fill=col + (255,), outline=INK + (255,), width=10)
    _brand_text(g, 430, 270, label, 760, 120, txt_col)
    g.polygon([(860, 160), (1080, 160), (1230, 340), (1230, 520), (860, 520)], fill=RED4 + (255,), outline=INK + (255,))
    g.line([(860, 160), (1080, 160), (1230, 340), (1230, 520), (860, 520), (860, 160)], fill=INK + (255,), width=10)
    g.polygon([(900, 200), (1060, 200), (1170, 340), (900, 340)], fill=(200, 230, 245, 255), outline=INK + (255,))
    for cx in (200, 640, 1060):
        g.ellipse([cx - 80, 450, cx + 80, 610], fill=(40, 40, 44, 255), outline=INK + (255,), width=8)
        g.ellipse([cx - 30, 500, cx + 30, 560], fill=(170, 170, 170, 255))
    return _done(key, im)


def plant_spr(label="EMBOTELLADORA", flag="MX"):
    key = ("plant", label, flag)
    if key in _spr4:
        return _spr4[key]
    w, h = 420, 420
    im, g = _canvas(w, h)
    W2, H2 = w * 2, h * 2
    g.rectangle([560, 20, 660, 420], fill=(150, 140, 136, 255), outline=INK + (255,), width=8)   # chimenea
    for i in range(3):                                                                             # techo de sierra
        x = i * 280
        g.polygon([(x, 420), (x + 280, 300), (x + 280, 420)], fill=(190, 186, 180, 255), outline=INK + (255,))
    g.rectangle([0, 420, W2, H2], fill=(236, 224, 196, 255), outline=INK + (255,), width=10)
    g.rectangle([40, 470, W2 - 40, 580], fill=(255, 255, 255, 255), outline=INK + (255,), width=6)
    _brand_text(g, W2 / 2, 525, label, W2 - 120, 76, INK)
    for c in range(4):
        g.rectangle([70 + c * 190, 640, 190 + c * 190, 740], fill=(200, 230, 245, 255), outline=INK + (255,), width=6)
    if flag:                                                                                       # bandera MX (tres franjas)
        g.line([(80, 60), (80, 420)], fill=INK + (255,), width=10)
        for j, cc in enumerate([(0, 104, 71), (255, 255, 255), (206, 17, 38)]):
            g.rectangle([86 + j * 70, 70, 156 + j * 70, 200], fill=cc + (255,), outline=INK + (255,), width=4)
    return _done(key, im)

def jar(fr, cx, cy, level, t, a):
    """Alcancía de vidrio con el saldo adentro (nivel 0-1)."""
    d = fr.d
    w, h = 300, 360
    x0, y0 = cx - w / 2, cy - h / 2
    lev = y0 + h - (h - 40) * level + 6 * math.sin(t * 3.1)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 46, fill=(70, 60, 58), outline=INK, width=6)
    d.rounded_rectangle([x0 + 8, lev, x0 + w - 8, y0 + h - 8], 40, fill=(160, 110, 50))
    for i in range(7):
        yy = y0 + h - 40 - i * 34
        if yy > lev + 10:
            d.ellipse([x0 + 40 + (i % 3) * 70, yy - 14, x0 + 100 + (i % 3) * 70, yy + 14], fill=YEL4, outline=INK, width=3)
    d.rounded_rectangle([x0 + 70, y0 - 30, x0 + w - 70, y0 + 8], 12, fill=(120, 110, 108), outline=INK, width=6)
    d.rounded_rectangle([cx - 60, y0 - 22, cx + 60, y0 - 10], 6, fill=INK)
    d.line([x0 + 30, y0 + 40, x0 + 30, y0 + h - 60], fill=(255, 255, 255), width=8)


def coin_spr(r=26):
    key = ("coin", r)
    if key in _spr4:
        return _spr4[key]
    im, g = _canvas(r * 2 + 4, r * 2 + 4)
    g.ellipse([4, 4, r * 4, r * 4], fill=YEL4 + (255,), outline=INK + (255,), width=6)
    g.text((r * 2 + 2, r * 2 + 2), "$", font=font(BLACK, r * 2.4), fill=INK + (255,), anchor="mm")
    return _done(key, im)


def _arrow(d, x0, y0, x1, y1, col, wdt=12):
    d.line([x0, y0, x1, y1], fill=col, width=wdt)
    ang = math.atan2(y1 - y0, x1 - x0)
    L = 34
    pts = [(x1, y1), (x1 - L * math.cos(ang - 0.5), y1 - L * math.sin(ang - 0.5)),
           (x1 - L * math.cos(ang + 0.5), y1 - L * math.sin(ang + 0.5))]
    d.polygon(pts, fill=col)




# ---------------- fondo con imagen (27 nov. 2026: escenas ilustradas con IA) ----------------
_BGI = {}
_GRAD = None


def _bgimg(path):
    if path not in _BGI:
        im = Image.open(path).convert("RGB")
        r = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * r + 0.5), int(im.height * r + 0.5)), Image.LANCZOS)
        l, tp = (im.width - W) // 2, (im.height - H) // 2
        _BGI[path] = im.crop((l, tp, l + W, tp + H))
    return _BGI[path]


def _grad(top_k=1.0, bot_k=1.0):
    global _GRAD
    _GRAD = _GRAD or {}
    key = (round(top_k, 2), round(bot_k, 2))
    if key not in _GRAD:
        a = np.zeros((H, 1), dtype=np.float32)
        top, bot = 760, 560
        a[:top, 0] = np.linspace(205, 0, top) * top_k
        a[H - bot:, 0] = np.linspace(0, 150, bot) * bot_k
        a = np.clip(a, 0, 235)
        _GRAD[key] = Image.fromarray(np.repeat(a, W, axis=1).astype("uint8"), "L")
    return _GRAD[key]


def draw_bg(fr, t, sc, bgs):
    """bgs: lista de dict(src, cue=None, z=(1.0, 1.12), c0=(0.5, 0.5), c1=(0.5, 0.5)). Cámara lenta (Ken Burns)."""
    act, t_act, nxt = None, None, sc.t1
    for i, b in enumerate(bgs):
        tb = sc.t0 if (i == 0 or b.get("cue") is None) else _cue(sc, b.get("cue"), sc.t0)
        if t >= tb - 1e-6:
            act, t_act = b, tb
            nxt = sc.t1
            for b2 in bgs[i + 1:]:
                nxt = _cue(sc, b2.get("cue"), sc.t1)
                break
    if act is None:
        return
    im = _bgimg(act["src"])
    u = clamp((t - t_act) / max(0.5, nxt - t_act))
    z0, z1 = act.get("z", (1.0, 1.12))
    z = lerp(z0, z1, ease_io(u))
    c0, c1 = act.get("c0", (0.5, 0.5)), act.get("c1", act.get("c0", (0.5, 0.5)))
    cx, cy = lerp(c0[0], c1[0], u), lerp(c0[1], c1[1], u)
    cw, ch = W / z, H / z
    x0 = min(max(cx * W - cw / 2, 0), W - cw)
    y0 = min(max(cy * H - ch / 2, 0), H - ch)
    crop = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    k = t - t_act
    if k < 0.14 and t_act > 0.01:                       # destello corto en el corte
        crop = Image.blend(crop, Image.new("RGB", (W, H), (255, 255, 255)), 0.55 * (1 - k / 0.14))
    fr.im.paste(crop, (0, 0))
    fr.im.paste(Image.new("RGB", (W, H), (12, 10, 20)), (0, 0), _grad(*act.get("shade", (1.0, 1.0))))
    fr.d = ImageDraw.Draw(fr.im)
    fr.cam = (x0, y0, z)

# ---------------- escena genérica ----------------
def _cue(sc, c, default):
    if c is None:
        return default
    return sc.lcues.get(c, sc.cues.get(c, default))


def _fmt(v, pr):
    s = f"{v:,.{pr.get('dec', 0)}f}"
    return pr.get("pre", "") + s + pr.get("suf", "")


def draw_prop(fr, t, sc, pr):
    t_in = _cue(sc, pr.get("cue"), sc.t0 + 0.12) + pr.get("delay", 0.0)
    if sc.first and pr.get("cue") is None:
        t_in -= 0.8
    k = t - t_in
    if k < 0:
        return
    a = 1.0
    if pr.get("out"):
        t_out = _cue(sc, pr["out"], 1e9)
        if t >= t_out:
            a = clamp(1 - (t - t_out) / 0.18)
            if a <= 0:
                return
    kind = pr["kind"]
    x, y, s = pr.get("x", W / 2), pr.get("y", 1150), pr.get("s", 1.0)
    if pr.get("pin") and getattr(fr, "cam", None):          # pegado a la imagen: sigue a la cámara
        cx0, cy0, cz = fr.cam
        x, y, s = (x - cx0) * cz, (y - cy0) * cz, s * cz
    bob = 0 if (pr.get("still") or pr.get("pin")) else 5 * math.sin(t * 1.7 + x * 0.01)
    u = bounce(k, pr.get("dur", 0.34))
    if kind == "stamp":
        sl = max(0.0, 1 - k / 0.18)
        spr = stamp_spr(pr["txt"], pr.get("angle", -10))
        fr.paste(_scaled(spr, s * (1 + 1.1 * sl ** 2)), x, y, a * min(1, k / 0.06))
        return
    if kind == "counter":
        dur = pr.get("count", 1.4)
        v = pr["to"] * ease_out(k / dur)
        txt = _fmt(v, pr)
        f = af(pr.get("size", 190) * s)
        spr = Image.new("RGBA", (int(f.getlength(_fmt(pr["to"], pr)) + 60), int(f.size * 1.5)), (0, 0, 0, 0))
        g = ImageDraw.Draw(spr)
        g.text((spr.width / 2 + 6, spr.height / 2 + 8), txt, font=f, fill=(0, 0, 0, 170), anchor="mm")
        g.text((spr.width / 2, spr.height / 2), txt, font=f, fill=pr.get("col", RED4) + (255,), anchor="mm")
        fr.paste(_scaled(spr, 0.8 + 0.2 * u), x, y + bob * 0.4, a * min(1, k / 0.1))
        if pr.get("label"):
            lc = pr.get("label_col")
            text(fr.d, (x, y + f.size * 0.72), pr["label"], fit(pr["label"], BOLD, pr.get("label_size", 40) * s, 900),
                 lc if lc else mix(CREAM, a * min(1, k / 0.3), BG4))
        return
    if kind == "logo":
        spr = _logo(pr["src"], pr.get("w", 300), pr.get("h", 300))
        if spr is None:
            return
        fr.paste(_scaled(spr, 0.6 + 0.4 * u), x, y + bob * 0.3, a * min(1, k / 0.08))
        return
    if kind == "jar":
        jar(fr, x, y + bob * 0.5, pr.get("level", 0.6), t, a)
        t_stop = _cue(sc, pr.get("flow_until"), 1e9)
        if k > 0.3 and pr.get("flow", True) and t < t_stop:            # monedas que entran y salen sin parar
            cs = coin_spr(24)
            for i in range(6):
                ph = ((t * 0.9 + i / 6) % 1.0)
                xi = lerp(x - 400, x - 40, ph)
                yi = y - 170 - 70 * math.sin(math.pi * ph)
                fr.paste(cs, xi, yi, a * min(1, (k - 0.3) / 0.3) * (1 - ph ** 6))
                ph2 = ((t * 0.9 + i / 6 + 0.5) % 1.0)
                xo = lerp(x + 40, x + 400, ph2)
                yo = y - 170 - 70 * math.sin(math.pi * ph2)
                fr.paste(cs, xo, yo, a * min(1, (k - 0.3) / 0.3) * (1 - ph2 ** 6))
        for side, key, lab in ((-1, "in_cue", "in_txt"), (1, "out_cue", "out_txt")):
            if pr.get(lab):
                kk = t - _cue(sc, pr.get(key), t_in + 0.4)
                if kk > 0:
                    uu = bounce(kk)
                    spr = tag_spr(pr[lab], pr.get(lab + "_s", ""))
                    fr.paste(_scaled(spr, 0.82 * (0.7 + 0.3 * uu)), x + side * 285, y + 250, a * min(1, kk / 0.1))
        return
    if kind == "row":                                   # fila de N vasos; los primeros `hot` en rojo
        n, hot = pr.get("n", 10), pr.get("hot", 4)
        gap = pr.get("gap", 92)
        for i in range(n):
            ki = k - i * 0.07
            ui = bounce(ki, 0.25)
            if ui <= 0:
                continue
            spr = bottle_spr(pr.get("label", "") if i < hot else "", pr.get("col", RED4)) if pr.get("item") == "bottle" \
                else cup("$" if i < hot else "")
            if i >= hot:
                spr = spr.point(lambda v: v)          # misma silueta, pero apagada
                dim = Image.new("RGBA", spr.size, (40, 32, 30, 0))
                dim.putalpha(spr.getchannel("A").point(lambda v: int(v * 0.55)))
                spr = Image.alpha_composite(spr, dim)
            fr.paste(_scaled(spr, 0.32 * s * (0.6 + 0.4 * ui)), x + (i - (n - 1) / 2) * gap, y + bob * 0.3,
                     a * min(1, ki / 0.08))
        return
    if kind == "card":
        spr = gift_card(pr.get("label", "GIFT CARD"))
        if pr.get("angle"):
            spr = spr.rotate(pr["angle"], expand=True, resample=Image.BICUBIC)
    elif kind == "cup":
        spr = cup(pr.get("label", "CAFÉ"))
    elif kind == "phone":
        cnt = pr.get("count", 0)
        val = pr.get("to", 0)
        amt = _fmt(val * (ease_out(k / cnt) if cnt else 1), pr) if "to" in pr else pr.get("amount", "")
        spr = phone(pr.get("title", "SALDO"), amt)
    elif kind == "tag":
        spr = tag_spr(pr["big"], pr.get("small", ""))
    elif kind == "bubble":
        n = int(len(pr["txt"]) * clamp((k - 0.15) / pr.get("type", 1.0)))
        spr = bubble_spr(pr["txt"], n, pr.get("who", "TÚ"))
    elif kind == "person":
        spr = person_spr(pr.get("mood", "smile"), pr.get("shirt", (52, 90, 140)))
    elif kind == "bank":
        spr = bank_spr(pr.get("label", "BANCO"))
    elif kind == "badge":
        spr = badge_spr(pr["txt"], pr.get("col", GREEN4))
    elif kind == "store":
        spr = store_spr(pr.get("brand", "COCA-COLA"), pr.get("sub", "ABARROTES LA ESQUINA"), pr.get("col", RED4),
                        pr.get("logo"), pr.get("sign", "HAY HIELO"))
    elif kind == "fridge":
        spr = fridge_spr(pr.get("brand", "COCA-COLA"), pr.get("col", RED4), pr.get("logo"), ribbon=pr.get("ribbon", False))
        if pr.get("drop"):                                   # cae desde arriba con golpe
            e = clamp(k / 0.32)
            y = lerp(-400, y, e * e) + (14 * math.sin(min(1, max(0, k - 0.32) / 0.25) * math.pi * 2) * max(0, 1 - (k - 0.32) / 0.3) if k > 0.32 else 0)
            u = 1.0
    elif kind == "bottle":
        spr = bottle_spr(pr.get("label", "COCA-COLA"), pr.get("col", RED4))
        if pr.get("spin"):                                   # la botella gira hacia la cámara
            sx = abs(math.cos(clamp(k / 0.6) * math.pi * 2)) * 0.8 + 0.2 if k < 0.6 else 1.0
            spr = spr.resize((max(1, int(spr.width * sx)), spr.height), Image.BILINEAR)
    elif kind == "jug":
        spr = jug_spr(pr.get("label", "CONCENTRADO"))
    elif kind == "plant":
        spr = plant_spr(pr.get("label", "EMBOTELLADORA"), pr.get("flag", "MX"))
    elif kind == "truck":
        spr = truck_spr(pr.get("label", "EMBOTELLADORA"))
        if pr.get("drive"):                                  # entra manejando desde la izquierda
            e = ease_out(clamp(k / 0.9))
            x = lerp(-500, x, e)
            u = 1.0
    elif kind == "arrow":
        d = fr.d
        e = ease_out(k / 0.4)
        _arrow(d, pr["x0"], pr["y0"], lerp(pr["x0"], pr["x1"], e), lerp(pr["y0"], pr["y1"], e), pr.get("col", YEL4))
        return
    else:
        return
    fr.paste(_scaled(spr, s * (0.55 + 0.45 * u)), x, y + bob, a * min(1, k / 0.08))


def v4(fr, t, sc):
    cfg = fr.cfg
    p = sc.p
    if p.get("bg"):
        draw_bg(fr, t, sc, p["bg"] if isinstance(p["bg"], list) else [dict(src=p["bg"])])
    header(fr, cfg.get("series", ""), cfg.get("ep", ""))
    top = 430 if p.get("chapter") else 340
    if p.get("chapter"):
        chapter(fr, p["chapter"], t - sc.t0 - 0.02)
    heads = p.get("heads", [])
    act, t_act = None, None
    for h in heads:
        th = _cue(sc, h.get("cue"), sc.t0 + 0.02)
        if sc.first and h is heads[0]:
            th = -1.0
        if t >= th:
            act, t_act = h, th
    if act:
        k = (t + 0.8) if (sc.first and act is heads[0]) else (t - t_act)
        headline(fr, act["lines"], k, act.get("top", top), act.get("size", 118))
    for pr in p.get("props", []):
        draw_prop(fr, t, sc, pr)


def _sfx(sc):
    ev = []
    p = sc.p
    for i, h in enumerate(p.get("heads", [])):
        if i > 0 or not sc.first:
            ev.append((_cue(sc, h.get("cue"), sc.t0), "tick"))
    snd = dict(card="pop", cup="pop", phone="ding", stamp="boom", tag="pop", bubble="pop", person="pop",
               bank="thump", badge="ding", jar="cash", arrow="whoosh", store="whoosh", fridge="thump",
               bottle="pop", jug="thump", plant="thump", truck="whoosh")
    for pr in p.get("props", []):
        t_in = _cue(sc, pr.get("cue"), sc.t0 + 0.12) + pr.get("delay", 0.0)
        if pr.get("sfx", True) is False:
            continue
        kind = pr["kind"]
        if kind == "counter":
            dur = pr.get("count", 1.4)
            n = int(dur / 0.09)
            ev += [(t_in + i * 0.09, "tick") for i in range(n)] + [(t_in + dur, "cash")]
        elif kind in snd:
            ev.append((t_in, pr.get("snd", snd[kind])))
    return ev


S2.v4 = v4
S2.SFX["v4"] = _sfx


def sources_card(fr, t, t0, items, title="SOURCES"):
    k = t - t0
    a = clamp(k / 0.18)
    ov = Image.new("RGBA", (W, H), BG4 + (int(238 * a),))
    fr.im.paste(ov, (0, 0), ov)
    fr.d = ImageDraw.Draw(fr.im)
    d = fr.d
    text(d, (W / 2, 560), title, af(110), mix(RED4, a, BG4))
    y = 700
    for it in items:
        text(d, (W / 2, y), it, fit(it, BOLD, 42, 940), mix(CREAM, a, BG4))
        y += 78

"""Escenas ilustradas del 014 (aranceles y reembolsos). Mismo estilo "tarjeta impresa" de illus.py.

Personajes genéricos sin cara (método de R1: contar con personajes): aduana, tienda, comprador, corte.
Sin logos ni colores de ninguna cadena real. Se registra en scenes2 al importarse desde render.py.
"""
import math

import numpy as np

from core import *          # noqa: F401,F403
import fx
from fx import put, say, pill, panel, appear, pop, stamp, bill
import scenes2 as S2
from scenes2 import kick, slam, lc
import illus as I
from illus import Pen, card, cached, INKC, PAPER, SKYC, SEA, CORAL, NAVY, STEEL, TEALC, LEAF, ORNG, BROWN, YELC, CW, CH

GREEN = (96, 196, 120)


# ---------- piezas ----------
def box_spr(w=70):
    key = ("tfbox", w)
    if cached(key):
        return cached(key)
    p = Pen(w + 14, w * 0.8 + 16)
    h = w * 0.8
    p.rect(4, 4, w, h, BROWN, r=4, ht=True, out=4)
    p.rect(w * 0.42, 4, w * 0.58, h, (214, 170, 110), sh=False, out=3)
    return p.done(key)


def person_spr(h=230, col=TEALC, cap=None):
    """Figura genérica sin cara. cap = color de gorra (oficial de aduana)."""
    key = ("tfperson", h, col, cap)
    if cached(key):
        return cached(key)
    w = h * 0.5
    p = Pen(w + 20, h + 20)
    cx = w / 2 + 4
    p.rect(cx - w * 0.32, h * 0.36, cx + w * 0.32, h * 0.98, col, r=w * 0.22, ht=True, out=4)
    p.ell(cx, h * 0.2, w * 0.2, w * 0.2, (236, 196, 160), out=4)
    if cap:
        p.rect(cx - w * 0.24, h * 0.04, cx + w * 0.24, h * 0.13, cap, r=6, sh=False, out=4)
        p.rect(cx - w * 0.04, h * 0.1, cx + w * 0.32, h * 0.15, cap, r=4, sh=False, out=3)
    return p.done(key)


def check_spr(w=420, amount="$301,000,000", to="TARGET"):
    key = ("tfcheck", w, amount, to)
    if cached(key):
        return cached(key)
    h = w * 0.44
    p = Pen(w + 16, h + 18)
    p.rect(4, 4, w, h, (222, 244, 226), r=12, ht=True, out=5)
    p.rect(4, 4, w, h * 0.2, GREEN, r=12, sh=False, out=5)
    p.txt(w * 0.5, h * 0.11, "U.S. CUSTOMS · REFUND", w * 0.05, PAPER)
    p.txt(w * 0.07, h * 0.42, "PAY TO:", w * 0.045, INKC, HEAVY, "lm")
    p.txt(w * 0.3, h * 0.42, to, w * 0.07, NAVY, BLACK, "lm")
    p.ln([(w * 0.28, h * 0.52), (w * 0.93, h * 0.52)], 3)
    p.rect(w * 0.07, h * 0.62, w * 0.93, h * 0.86, PAPER, r=8, sh=False, out=4)
    p.txt(w * 0.5, h * 0.74, amount, w * 0.09, INKC)
    return p.done(key)


def store_spr(w=300):
    key = ("tfstore", w)
    if cached(key):
        return cached(key)
    h = w * 0.78
    p = Pen(w + 16, h + 18)
    p.rect(8, h * 0.28, w - 8, h - 4, PAPER, ht=True)
    p.rect(4, h * 0.12, w - 4, h * 0.32, CORAL, r=8)
    for i in range(6):
        x0 = 4 + i * (w - 8) / 6
        p.poly([(x0, h * 0.32), (x0 + (w - 8) / 6, h * 0.32), (x0 + (w - 8) / 12, h * 0.4)],
               CORAL if i % 2 else PAPER, sh=False, out=3)
    p.txt(w / 2, h * 0.22, "STORE", w * 0.11, PAPER)
    p.rect(w * 0.38, h * 0.56, w * 0.62, h - 4, NAVY, r=4, sh=False, out=4)
    for x0 in (w * 0.1, w * 0.7):
        p.rect(x0, h * 0.52, x0 + w * 0.2, h * 0.76, SKYC, r=4, sh=False, out=4)
    return p.done(key)


def booth_spr(w=230):
    key = ("tfbooth", w)
    if cached(key):
        return cached(key)
    h = w * 1.05
    p = Pen(w + 16, h + 18)
    p.poly([(4, h * 0.22), (w / 2, 4), (w - 4, h * 0.22)], NAVY, out=4)
    p.rect(14, h * 0.22, w - 14, h - 4, STEEL, ht=True)
    p.rect(14, h * 0.24, w - 14, h * 0.38, NAVY, sh=False, out=4)
    p.txt(w / 2, h * 0.31, "CUSTOMS", w * 0.13, PAPER)
    p.rect(w * 0.18, h * 0.46, w * 0.82, h * 0.7, SKYC, r=6, sh=False, out=4)
    return p.done(key)


def tag_spr(txt, w=170, col=YELC):
    key = ("tftag", txt, w, col)
    if cached(key):
        return cached(key)
    h = w * 0.55
    p = Pen(w + 16, h + 18)
    p.poly([(4, h / 2), (w * 0.22, 4), (w - 4, 4), (w - 4, h - 4), (w * 0.22, h - 4)], col, out=4)
    p.ell(w * 0.2, h / 2, 8, 8, PAPER, sh=False, out=3)
    p.txt(w * 0.6, h / 2, txt, w * 0.2)
    return p.done(key)


def gavel_spr(w=220):
    key = ("tfgavel", w)
    if cached(key):
        return cached(key)
    p = Pen(w + 16, w + 16)
    p.rect(w * 0.45, w * 0.3, w * 0.55, w * 0.95, BROWN, r=6, out=4)
    p.rect(w * 0.12, w * 0.08, w * 0.88, w * 0.36, (130, 76, 44), r=14, ht=True, out=5)
    p.rect(w * 0.08, w * 0.12, w * 0.18, w * 0.32, YELC, r=4, sh=False, out=4)
    p.rect(w * 0.82, w * 0.12, w * 0.92, w * 0.32, YELC, r=4, sh=False, out=4)
    return p.done(key)


def doc_spr(w=420):
    key = ("tfdoc", w)
    if cached(key):
        return cached(key)
    h = w * 1.25
    p = Pen(w + 16, h + 18)
    p.rect(4, 4, w, h, PAPER, r=10, ht=True, out=5)
    p.rect(4, 4, w, h * 0.12, NAVY, r=10, sh=False, out=5)
    p.txt(w / 2, h * 0.065, "QUARTERLY REPORT", w * 0.07, PAPER)
    rng = np.random.default_rng(4)
    for i in range(11):
        y = h * 0.2 + i * h * 0.068
        p.rect(w * 0.08, y, w * (0.5 + 0.4 * rng.random()), y + h * 0.025, (190, 182, 166), r=4, sh=False, out=0)
    return p.done(key)


# ---------- tarjetas de estación ----------
def ill_customs_card(w=CW, h=CH):
    key = ("tfcustoms", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, SKYC)
    gy = h - 120
    p.rect(4, gy, w * 0.42, h, SEA, sh=False, out=0)
    for row in range(3):
        y = gy + 30 + row * 30
        p.ln([(x, y + 5 * math.sin(x / 26 + row)) for x in range(12, int(w * 0.42), 14)], 3, (150, 200, 245))
    p.rect(w * 0.42, gy, w, h, (226, 212, 184), sh=False, out=0)
    p.ln([(4, gy), (w, gy)], 5)
    # barco con contenedores
    p.poly([(20, gy - 40), (360, gy - 40), (330, gy + 30), (50, gy + 30)], NAVY, ht=True)
    cols = [CORAL, ORNG, TEALC, YELC, CORAL, TEALC]
    for i, c in enumerate(cols):
        x0 = 50 + (i % 3) * 96
        y0 = gy - 40 - 54 * (1 + i // 3)
        p.rect(x0, y0, x0 + 92, y0 + 52, c, r=3, ht=True, out=4)
        for k in range(4):
            p.ln([(x0 + 14 + k * 20, y0 + 8), (x0 + 14 + k * 20, y0 + 44)], 3, _d(c))
    # grúa
    p.rect(420, 60, 446, gy, ORNG, ht=True)
    p.rect(300, 60, 640, 84, ORNG, ht=True)
    p.ln([(380, 84), (380, 160)], 4)
    # cinta hacia la aduana
    I._belt(p, 450, w - 40, gy - 34)
    return p.done(key)


def _d(c, k=0.7):
    return tuple(int(v * k) for v in c)


def ill_shelf_card(w=CW, h=CH):
    key = ("tfshelf", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, (255, 238, 214))
    gy = h - 70
    I._floor(p, w, gy)
    p.rect(60, 70, w - 60, gy, (230, 220, 200), ht=True)
    cols = [CORAL, TEALC, ORNG, NAVY, YELC, LEAF]
    for r in range(3):
        y = 130 + r * 112
        p.rect(60, y + 70, w - 60, y + 86, BROWN, sh=False, out=4)
        for i in range(9):
            if r == 1 and i in (3, 4, 5):
                continue
            x0 = 90 + i * 86
            c = cols[(i + r * 2) % len(cols)]
            p.rect(x0, y + 4, x0 + 66, y + 70, c, r=4, sh=False, out=4)
            p.rect(x0 + 10, y + 20, x0 + 56, y + 34, PAPER, r=3, sh=False, out=0)
    return p.done(key)


def ill_register_card(w=CW, h=CH):
    key = ("tfregister", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, (236, 228, 255))
    gy = h - 70
    I._floor(p, w, gy)
    p.rect(300, 270, w - 40, gy, NAVY, r=8, ht=True)                # mostrador
    p.rect(300, 250, w - 40, 290, (60, 62, 90), r=8, sh=False, out=4)
    p.rect(560, 120, 760, 250, STEEL, r=10, ht=True)                 # caja registradora
    p.rect(580, 140, 740, 196, (40, 52, 70), r=6, sh=False, out=4)
    p.rect(600, 230, 720, 252, PAPER, r=2, sh=False, out=3)
    return p.done(key)


def ill_court_card(w=CW, h=CH):
    key = ("tfcourt", w, h)
    if cached(key):
        return cached(key)
    p = card(w, h, SKYC)
    gy = h - 60
    p.rect(4, gy, w, h, (226, 212, 184), sh=False, out=0)
    p.ln([(4, gy), (w, gy)], 5)
    x0, x1 = 170, w - 170
    p.poly([(x0 - 40, 150), ((x0 + x1) / 2, 50), (x1 + 40, 150)], PAPER, ht=True)
    p.rect(x0 - 40, 150, x1 + 40, 186, PAPER, ht=True)
    n = 6
    for i in range(n):
        cx = x0 + 20 + i * (x1 - x0 - 40) / (n - 1)
        p.rect(cx - 22, 186, cx + 22, gy - 60, PAPER, ht=True, out=4)
    for k in range(3):
        p.rect(x0 - 60 - k * 20, gy - 60 + k * 20, x1 + 60 + k * 20, gy - 40 + k * 20, STEEL, sh=False, out=4)
    return p.done(key)


STEP = dict(customs=ill_customs_card, shelf=ill_shelf_card, register=ill_register_card)
LABELS_DEFAULT = ["CUSTOMS", "SHELF", "YOU", "REFUND"]


# ---------- escenas ----------
def refund_hook(fr, t, sc):
    """Pregunta completa desde el cuadro 1; el cheque vuela de la aduana a la tienda, pasando por encima del comprador."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["q1"], W / 2, 380, 64, WHITE, BLACK, maxw=940)
    say(fr, p["q2"], W / 2, 486, 118, YEL, BLACK, s=0.85 + 0.15 * pop(x, 0.25), glow=(ORNG, 18, 1.2), maxw=960)
    say(fr, p["q3"], W / 2, 592, 70, WHITE, BLACK, s=0.85 + 0.15 * pop(x - 0.06, 0.25), maxw=960)
    say(fr, p["q4"], W / 2, 690, 80, CORAL, BLACK, s=0.85 + 0.15 * pop(x - 0.12, 0.25), maxw=960)
    gy = 1130
    put(fr, booth_spr(230), 200, gy - 120, 0.9 + 0.1 * pop(x, 0.3))
    put(fr, store_spr(300), W - 210, gy - 116, 0.9 + 0.1 * pop(x - 0.05, 0.3))
    put(fr, person_spr(220), W / 2, gy - 60, 0.9 + 0.1 * pop(x - 0.1, 0.3))
    ph = (t * 0.55 + 0.35) % 1.0
    cx = lerp(240, W - 230, ease_io(ph))
    cy = gy - 250 - 90 * math.sin(math.pi * ph)
    put(fr, check_spr(250, p.get("amount", "$301,000,000"), p.get("to", "TARGET")), cx, cy, 1.0,
        clamp(ph / 0.1) * clamp((1 - ph) / 0.1), -8 + 16 * ph)
    y = sc.lcues.get("you")
    if y is not None and t > y:
        k = t - y
        put(fr, stamp(p["stamp"], 70, INKC), W / 2, gy - 90, slam(k, 2.4, 0.22), appear(k, 0.05), -10)


S2.SFX["refund_hook"] = lambda sc: [(sc.t0 + 0.1, "whoosh")] + ([(sc.lcues["you"], "boom")] if "you" in sc.lcues else [])


def big_refund(fr, t, sc):
    """Cheque grande + cifra que cuenta; '% de la utilidad' (cálculo propio) y 'en lo que va del año'."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    c = lc(sc, "big")
    k0 = max(0.0, t - c)
    val = p["n"] * ease_out(k0 / 1.2)
    say(fr, p["big"].format(val), W / 2, 450, 124, YEL, BLACK, a=appear(k0, 0.08), s=slam(k0, 1.5, 0.22),
        glow=(ORNG, 18, 1.2), maxw=960)
    say(fr, p["big_l"], W / 2, 548, 40, WHITE, HEAVY, a=appear(k0 - 0.1, 0.2), maxw=900)
    put(fr, check_spr(620, p.get("amount", "$301,000,000"), p.get("to", "TARGET")), W / 2,
        820 + 10 * math.sin(t * 2), slam(x, 1.3, 0.3), appear(x, 0.12), -3 + 2 * math.sin(t * 1.4))
    for j in range(6):
        ph = (t * 0.6 + j / 6) % 1.0
        put(fr, bill(150, (j * 37) % 40 - 20), 160 + j * 150, lerp(640, 1060, ph), 1.0,
            0.8 * clamp(ph / 0.15) * clamp((1 - ph) / 0.2), 40 * math.sin(t + j))
    q = sc.lcues.get("pct")
    if q is not None and t > q:
        k = t - q
        put(fr, pill(p["pct"], 44, INKC, YELC, 28, 16, BLACK), W / 2, 1050, slam(k, 1.8, 0.22), appear(k, 0.05), -2)
        put(fr, pill(p["tag"], 28, INKC, TEALC), W / 2 + 330, 990, pop(k - 0.3, 0.3))
    y = sc.lcues.get("ytd")
    if y is not None and t > y:
        k = t - y
        put(fr, pill(p["ytd"], 54, WHITE, CORAL, 32, 18, BLACK), W / 2, 1150, slam(k, 1.8, 0.22), appear(k, 0.05), 2)


S2.SFX["big_refund"] = lambda sc: ([(sc.lcues[c], s) for c, s in (("big", "cash"), ("pct", "ding"), ("ytd", "pop"))
                                     if c in sc.lcues])


def tariff_step(fr, t, sc):
    """Estación N de 4 siguiendo el dólar. Tarjeta ilustrada animada + qué pasa (cue 'who')."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    I.step_badge(fr, p["n"], s=slam(x, 1.8, 0.22))
    say(fr, p["title"], W / 2, 385, 92, WHITE, BLACK, a=appear(x, 0.1), s=slam(x, 1.4, 0.22), maxw=900)
    sc_, al = I._card_in(x)
    spr = STEP[p["ill"]]()
    cyc = 838
    put(fr, spr, W / 2, cyc, sc_, al)
    ox, oy = W / 2 - spr.width / 2, cyc - spr.height / 2
    gy = oy + CH
    if p["ill"] == "customs":
        bx, by = ox + 760, gy - 120 - 120
        for i in range(4):                       # cajas que bajan del barco y entran a la aduana
            u = (t * 110 + i * 90) % 360
            put(fr, box_spr(64), ox + 470 + u, gy - 120 - 34 - 30, 1.0, clamp(u / 20) * clamp((360 - u) / 40))
        put(fr, booth_spr(200), bx, by + 10, 1.0, al)
        put(fr, person_spr(150, NAVY, cap=NAVY), bx - 150, gy - 120 - 80, 1.0, al)
        for i in range(3):                       # monedas que caen a la caseta: el arancel
            ph = (t * 1.1 + i / 3) % 1.0
            cxp, cyp = bx + 10, lerp(by - 220, by - 60, ease_io(ph))
            r = 18
            fr.d.ellipse([cxp - r, cyp - r, cxp + r, cyp + r], fill=YELC, outline=INKC, width=4)
    elif p["ill"] == "shelf":
        hole_x, hole_y = ox + 90 + 3 * 86, oy + 130 + 112
        for i in range(3):
            put(fr, box_spr(66), hole_x + 33 + i * 86, hole_y + 40, pop(x - 0.2 - 0.12 * i, 0.3))
        u = ease_out(clamp((t - lc(sc, "who", sc.t0 + 1)) / 0.8))
        put(fr, tag_spr(p.get("tag_old", "$"), 170, PAPER), ox + 200, oy + 120, 1.0, 1 - u, -6)
        put(fr, tag_spr(p.get("tag_new", "$$"), 190, YELC), ox + 200, oy + 120 - 30 * u, slam(u, 1.5, 0.4) if u > 0 else 0,
            u, -6)
        if u > 0:
            ax, ay = ox + 330, oy + 110
            fr.d.polygon([(ax, ay - 50 * u - 20), (ax - 30, ay - 50 * u + 20), (ax + 30, ay - 50 * u + 20)], fill=CORAL,
                         outline=INKC)
    elif p["ill"] == "register":
        put(fr, person_spr(260, TEALC), ox + 190, gy - 70 - 120, 1.0, al)
        rl = clamp((t - sc.t0 - 0.4) / 2.0)
        fr.d.rectangle([ox + 620, oy + 250 - 0, ox + 700, oy + 250 + 150 * rl], fill=PAPER, outline=INKC, width=4)
        for k in range(int(6 * rl)):
            yy = oy + 268 + k * 22
            fr.d.line([(ox + 632, yy), (ox + 688, yy)], fill=(160, 150, 140), width=4)
        for i in range(3):                       # dinero que sale del comprador hacia la caja
            ph = (t * 0.9 + i / 3) % 1.0
            put(fr, bill(110), lerp(ox + 260, ox + 600, ease_io(ph)), oy + 300 - 80 * math.sin(math.pi * ph), 1.0,
                clamp(ph / 0.1) * clamp((1 - ph) / 0.15), 20 * ph)
    w_ = sc.lcues.get("who")
    if w_ is not None and t > w_:
        k = t - w_
        put(fr, pill(p["who"], 48, INKC, YELC, 30, 18, BLACK), W / 2, 478, slam(k, 1.9, 0.22), appear(k, 0.05), -2)
        if p.get("who_sub"):
            say(fr, p["who_sub"], W / 2, 548, 32, WHITE, HEAVY, a=appear(k - 0.2, 0.25), maxw=900)
    I.track(fr, t, p["n"], p.get("labels", LABELS_DEFAULT))


S2.SFX["tariff_step"] = lambda sc: [(sc.t0 + 0.05, "pop")] + ([(sc.lcues["who"], "ding")] if "who" in sc.lcues else [])


def court_hit(fr, t, sc):
    """La corte: tarjeta con columnas, mazo que golpea en 'rule' (sello 6–3), dos líneas en 'power'."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["title"], W / 2, 390, 84, WHITE, BLACK, a=appear(x, 0.1), s=slam(x, 1.4, 0.22), maxw=940)
    sc_, al = I._card_in(x)
    spr = ill_court_card()
    cyc = 820
    put(fr, spr, W / 2, cyc, sc_, al)
    r = sc.lcues.get("rule")
    if r is not None and t > r:
        k = t - r
        ang = -40 + 40 * ease_out(clamp(k / 0.18))
        put(fr, gavel_spr(240), W / 2 + 300, cyc + 120, 1.0, appear(k, 0.05), ang)
        put(fr, stamp(p["stamp"], 96, CORAL), W / 2 - 40, cyc + 40, slam(k, 2.4, 0.22), appear(k, 0.05), -10)
    else:
        put(fr, gavel_spr(240), W / 2 + 300, cyc + 120, 1.0, al, -40 + 6 * math.sin(t * 3))
    q = sc.lcues.get("power")
    if q is not None and t > q:
        k = t - q
        put(fr, pill(p["l1"], 46, INKC, YELC, 30, 18, BLACK), W / 2, 1110, slam(k, 1.8, 0.22), appear(k, 0.05), -2)
        say(fr, p["l2"], W / 2, 1180, 34, WHITE, HEAVY, a=appear(k - 0.2, 0.25), maxw=940)


S2.SFX["court_hit"] = lambda sc: [(sc.t0 + 0.05, "whoosh")] + ([(sc.lcues["rule"], "boom")] if "rule" in sc.lcues else []) + \
    ([(sc.lcues["power"], "ding")] if "power" in sc.lcues else [])


def report_note(fr, t, sc):
    """El reporte trimestral: líneas que se resaltan; sello en 'not' (lo que no dice)."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["title"], W / 2, 390, 76, WHITE, BLACK, a=appear(x, 0.1), s=slam(x, 1.4, 0.22), maxw=940)
    spr = doc_spr(440)
    cy = 830
    put(fr, spr, W / 2, cy, slam(x, 1.25, 0.3), appear(x, 0.12), -2)
    ox, oy = W / 2 - spr.width / 2, cy - spr.height / 2
    h = 440 * 1.25
    hl = sc.lcues.get("val")
    if hl is not None and t > hl:
        k = clamp((t - hl) / 0.5)
        for i in (2, 3):
            y = oy + h * 0.2 + i * h * 0.068
            fr.d.rectangle([ox + 30, y - 4, ox + 30 + 360 * k, y + 18], outline=YELC, width=5)
        put(fr, pill(p["val"], 36, INKC, TEALC, 24, 14, BLACK), W / 2 - 250, oy + 120, pop(t - hl, 0.3), 1.0, -6)
    n = sc.lcues.get("not")
    if n is not None and t > n:
        k = t - n
        put(fr, stamp(p["stamp"], 64, CORAL), W / 2, cy + 120, slam(k, 2.4, 0.22), appear(k, 0.05), -8)
        say(fr, p["l2"], W / 2, 1165, 36, WHITE, HEAVY, a=appear(k - 0.2, 0.25), maxw=940)


S2.SFX["report_note"] = lambda sc: [(sc.t0 + 0.05, "pop")] + ([(sc.lcues["val"], "ding")] if "val" in sc.lcues else []) + \
    ([(sc.lcues["not"], "boom")] if "not" in sc.lcues else [])


def answer_refund(fr, t, sc):
    """El cheque regresa de la aduana a la tienda, no al comprador; la estación 4 se enciende. Luego answer_cta."""
    p = sc.p
    ans, fol = sc.lcues.get("ans"), sc.lcues.get("fol")
    mA = appear(t - ans, 0.3) if ans is not None and t > ans else 0.0
    mB = appear(t - fol, 0.3) if fol is not None and t > fol else 0.0
    a = (1 - mB) * (1 - mA)
    lit = (t - ans) if ans is not None and t > ans else 0.0
    x = t - sc.t0
    if a > 0.004:
        gy = 1000
        put(fr, booth_spr(210), 200, gy - 110, pop(x, 0.3), a)
        put(fr, store_spr(280), W - 210, gy - 108, pop(x - 0.05, 0.3), a)
        put(fr, person_spr(200), W / 2, gy - 40, pop(x - 0.1, 0.3), a)
        ph = (t * 0.6) % 1.0
        put(fr, check_spr(230, p.get("amount", "$"), p.get("to", "IMPORTER")), lerp(240, W - 230, ease_io(ph)),
            gy - 290 - 150 * math.sin(math.pi * ph), 1.0, a * clamp(ph / 0.1) * clamp((1 - ph) / 0.1), -8 + 16 * ph)
    if 1 - mB > 0.004:
        I.track(fr, t, 4, p.get("labels", LABELS_DEFAULT), 1 - mB, lit4=lit)
    S2.answer_cta(fr, t, sc)


S2.SFX["answer_refund"] = S2.SFX["answer_cta"]

for _n in ("refund_hook", "big_refund", "tariff_step", "court_hit", "report_note", "answer_refund"):
    setattr(S2, _n, globals()[_n])

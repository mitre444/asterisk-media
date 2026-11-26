"""Biblioteca de escenas. Cada funcion dibuja un cuadro: fn(fr, t, sc).

sc.p      textos y valores de la escena (vienen del guion, ya en su idioma)
sc.cues   instantes marcados en la narracion con [#nombre]
sc.tokens palabras narradas en esta escena, con su tiempo
"""
import math
from core import *


class Scene:
    def __init__(self, i, fn, t0, t1, cues, p, tokens, first=False, last=False):
        self.i, self.fn, self.t0, self.t1 = i, fn, t0, t1
        self.cues, self.p, self.tokens = cues, p, tokens
        self.first, self.last = first, last
        self.src, self.src_color = "", DIM

    def alpha(self, t, fin=0.22, fout=0.16):
        a = 1.0
        if not self.first:
            a *= clamp((t - self.t0) / fin)
        if not self.last:
            a *= clamp((self.t1 - t) / fout)
        return a

    def since(self, t, cue):
        return t - self.cues.get(cue, self.t0)

    def on(self, t, cue, dur=0.3):
        x = self.since(t, cue)
        return ease_out(x / dur) if x > 0 else 0.0


def cmix(c1, c2, u):
    return tuple(int(lerp(c1[i], c2[i], clamp(u))) for i in range(3))


# ---------- bloque de precio (gancho y cierre comparten composicion) ----------
def _price_block(fr, al, p, t, ast=0.0, ast_a=0.0, rot=0.0, dog=1.0, scale=1.0):
    fr.paste(hotdog(500), W / 2, 545 + 6 * math.sin(t * 1.6), al * dog)
    f = font(BLACK, 262 * scale)
    text(fr.d, (W / 2, 850), p["price"], f, mix(YEL, al))
    if ast_a > 0.004:
        wpr = f.getlength(p["price"])
        fr.paste(asterisk(118 * max(0.2, ast), YEL, rot), W / 2 + wpr / 2 + 46, 742, al * ast_a)


def _timeline(fr, al, p, u):
    d = fr.d
    xa, xb, y = 170, 910, 1085
    xm = lerp(xa, xb, u)
    rrect(d, [xa, y - 7, xb, y + 7], 7, fill=mix(EDGE, al))
    if xm - xa > 14:
        rrect(d, [xa, y - 7, xm, y + 7], 7, fill=mix(YEL, al))
    oval(d, [xm - 20, y - 20, xm + 20, y + 20], fill=mix(WHITE, al))
    yr = int(round(lerp(p["y0"], p["y1"], u)))
    text(d, (clamp(xm, xa + 62, xb - 62), y - 72), str(yr), font(BLACK, 64), mix(WHITE, al))
    text(d, (xa, y + 54), str(p["y0"]), font(SEMI, 34), mix(DIM, al), "lm")
    text(d, (xb, y + 54), str(p["y1"]), font(SEMI, 34), mix(DIM, al), "rm")


def hook(fr, t, sc):
    """Precio grande + linea de tiempo que retrocede; el asterisco aparece al final."""
    al, p = sc.alpha(t), sc.p
    kicker(fr, p["kicker"], al)
    x = sc.since(t, "rewind")
    u = 1.0 - ease_io(x / p.get("rewind_dur", 1.6)) if x > 0 else 1.0
    xa = sc.since(t, "ast")
    ast = back_out(xa / 0.4) if xa > 0 else 0.0
    dog = 1.0 - 0.62 * ease_out(xa / 0.5) if xa > 0 else 1.0
    rot = -90 * (1 - ease_out(xa / 0.55)) if xa > 0 else 0.0
    punch = 1.0 + 0.10 * (1 - ease_out((t - sc.t0) / 0.45))
    _price_block(fr, al, p, t, ast, clamp(xa / 0.08) if xa > 0 else 0.0, rot, dog, punch)
    _timeline(fr, al, p, u)


def bars(fr, t, sc):
    """Dos barras: valor real contra valor hipotetico que crece."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    kicker(fr, p["kicker"], al)
    base, bw, x1, x2, hmax = 1120, 250, 330, 750, 540
    h1 = hmax * p["v1"] / p["v2"]
    g1 = ease_out((t - sc.t0) / 0.5)
    gd = p.get("grow_dur", 1.2)
    x = sc.since(t, "grow")
    g2 = ease_io(x / gd) if x > 0 else 0.0
    ha, hb = max(4, h1 * g1), max(4, h1 * g1 + (hmax - h1) * g2)
    line(d, [(X0 + 40, base), (X1 - 40, base)], fill=mix(EDGE, al), width=4)
    rrect(d, [x1 - bw / 2, base - ha, x1 + bw / 2, base], 18, fill=mix(YEL, al))
    rrect(d, [x2 - bw / 2, base - hb, x2 + bw / 2, base], 18, fill=mix(RED, al))
    if g2 > 0:
        for xx in range(int(x1 + bw / 2) + 16, int(x2 - bw / 2) - 14, 26):
            line(d, [(xx, base - h1), (xx + 12, base - h1)], fill=mix(DIM, al * 0.8), width=3)
    f = font(BLACK, 92)
    text(d, (x1, base - ha - 62), p["fmt"].format(p["v1"]), f, mix(YEL, al * g1))
    text(d, (x2, base - hb - 62), p["fmt"].format(lerp(p["v1"], p["v2"], g2)), f, mix(RED, al * g1))
    text(d, (x1, base + 50), p["l1"], fit(p["l1"], SEMI, 34, 380), mix(DIM, al))
    text(d, (x2, base + 50), p["l2"], fit(p["l2"], SEMI, 34, 380), mix(DIM, al))
    xb = x - gd
    if xb > 0 and p.get("badge"):
        text(d, (x2, base - hmax - 170), p["badge"], font(BLACK, 72 * back_out(xb / 0.35)), mix(WHITE, al))


def people(fr, t, sc):
    """Dos tarjetas de persona y un globo con lo que dijo la primera."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    kicker(fr, p["kicker"], al)

    def person(y, name, role, ini, a, accent, e=None):
        if a <= 0.004:
            return
        dy = (1 - (a if e is None else e)) * 40
        card(d, [X0, y + dy, X1, y + 210 + dy], al * a)
        ac = mix(accent, al * a)
        oval(d, [X0 + 36, y + 43 + dy, X0 + 160, y + 167 + dy], fill=ac)
        text(d, (X0 + 98, y + 105 + dy), ini, font(HEAVY, 50), mix((16, 20, 38), al * a, base=ac))
        text(d, (X0 + 192, y + 78 + dy), name, fit(name, HEAVY, 64, 670), mix(WHITE, al * a), "lm")
        text(d, (X0 + 192, y + 146 + dy), role, fit(role, SEMI, 36, 670), mix(DIM, al * a), "lm")

    person(430, p["n1"], p["r1"], p["i1"], sc.on(t, "p1", 0.35), YEL)
    a2 = sc.on(t, "p2", 0.35)
    if "pre" in sc.cues:      # la segunda tarjeta espera atenuada hasta que la voz la nombra
        pre = sc.on(t, "pre", 0.35)
        person(950, p["n2"], p["r2"], p["i2"], 0.32 * pre + 0.68 * a2, GRN, pre)
    else:
        person(950, p["n2"], p["r2"], p["i2"], a2, GRN)
    b = sc.on(t, "say", 0.3)
    if b > 0.004:
        bc = mix(YEL, al * b)
        dy = (1 - b) * 24
        poly(d, [(250, 716 + dy), (292, 668 + dy), (334, 716 + dy)], fill=bc)
        rrect(d, [150, 714 + dy, 930, 894 + dy], 34, fill=bc)
        lines = p["bubble"]
        f = fit(max(lines, key=len), BOLD, 48, 700)
        for i, ln in enumerate(lines):
            text(d, (W / 2, 804 + dy + (i - (len(lines) - 1) / 2) * 60), ln, f, mix((16, 20, 38), al * b, base=bc))


def quote(fr, t, sc):
    """Cita grande que se escribe palabra por palabra al ritmo de la voz."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    kicker(fr, p["kicker"], al)
    a2 = sc.on(t, "attr", 0.4)
    text(d, (X0 + 44, 398), p["attr1"], fit(p["attr1"], HEAVY, 46, 840), mix(WHITE, al * a2), "lm")
    text(d, (X0 + 44, 454), p["attr2"], fit(p["attr2"], SEMI, 34, 840), mix(DIM, al * a2), "lm")
    words = [tk for tk in sc.tokens if tk["role"] == "quote"]
    lines, i = [], 0
    for n in p["breaks"]:
        lines.append(words[i:i + n])
        i += n
    size = p.get("size", 118)
    f = font(BLACK, size)
    maxw = max(f.getlength(" ".join(w["display"] for w in ln)) for ln in lines)
    if maxw > 830:
        size *= 830 / maxw
        f = font(BLACK, size)
    lh = size * 1.15
    y0 = p.get("y0", 596)
    rrect(d, [X0, 370, X0 + 12, y0 + (len(lines) - 1) * lh + lh * 0.5], 6, fill=mix(YEL, al))
    sp = f.getlength(" ")
    for li, ln in enumerate(lines):
        x = X0 + 44
        col = YEL if li >= len(lines) - p.get("hot", 1) else WHITE
        for w in ln:
            wl = f.getlength(w["display"])
            xr = t - (w["start"] - 0.03)
            if xr > 0:
                s = 0.92 + 0.08 * back_out(xr / 0.18)
                text(d, (x + wl / 2, y0 + li * lh), w["display"], font(BLACK, size * s), mix(col, al * clamp(xr / 0.10)))
            x += wl + sp


def flow(fr, t, sc):
    """Antes (tachado) -> despues, con dos fichas de lugar."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    kicker(fr, p["kicker"], al)
    a1 = sc.on(t, "a", 0.3)
    xs = sc.since(t, "stop")
    k = ease_io(xs / 0.35) if xs > 0 else 0.0
    card(d, [170, 455, 910, 585], al * a1, outline=cmix(EDGE, RED, k), width=4)
    text(d, (W / 2, 520), p["a"], fit(p["a"], HEAVY, 54, 660), mix(cmix(WHITE, DIM, k), al * a1))
    if k > 0:
        line(d, [(205, 520), (205 + 670 * k, 520)], fill=mix(RED, al), width=8)
    a2 = sc.on(t, "own", 0.3)
    if a2 > 0.004:
        line(d, [(W / 2, 612), (W / 2, 612 + 92 * a2)], fill=mix(DIM, al), width=6)
        if a2 > 0.9:
            poly(d, [(W / 2 - 20, 702), (W / 2 + 20, 702), (W / 2, 734)], fill=mix(DIM, al))
        dy = (1 - a2) * 30
        card(d, [170, 765 + dy, 910, 905 + dy], al * a2, outline=GRN, width=5)
        text(d, (W / 2, 835 + dy), p["b"], fit(p["b"], HEAVY, 54, 660), mix(WHITE, al * a2))
    for cue, label, xa, xb in (("c1", p["c1"], 170, 525), ("c2", p["c2"], 555, 910)):
        a = sc.on(t, cue, 0.3)
        if a > 0.004:
            dy = (1 - a) * 30
            card(d, [xa, 975 + dy, xb, 1085 + dy], al * a)
            fr.paste(pin(56), xa + 50, 1030 + dy, al * a)
            text(d, (xa + 88, 1030 + dy), label, fit(label, HEAVY, 42, xb - xa - 110), mix(WHITE, al * a), "lm")


def counter(fr, t, sc):
    """Contador grande + pictograma que se llena."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    kicker(fr, p["kicker"], al)
    x = t - sc.t0
    land = sc.cues.get("count", sc.t0) + p.get("land", 0.9) - sc.t0      # la cuenta llega cuando la voz termina de decir la cifra
    g = ease_io(x / max(0.6, land))
    text(d, (W / 2, 540), p["fmt"].format(p["value"] * g), fit(p["fmt"].format(p["value"]), BLACK, 240, 880), mix(YEL, al))
    text(d, (W / 2, 705), p["sub"], fit(p["sub"], HEAVY, 46, 880), mix(WHITE, al))
    cols, rows = 5, 5
    shown = g * cols * rows
    for i in range(cols * rows):
        a = clamp(shown - i)
        if a <= 0:
            break
        fr.paste(hotdog(124), 220 + (i % cols) * 160, 820 + (i // cols) * 74, al * a)
    text(d, (W / 2, 1196), p["legend"], font(SEMI, 30), mix(DIM, al * (ease_out(x / 0.4) if x > 0 else 0)))


def reveal(fr, t, sc):
    """El asterisco entra grande, luego sube y deja ver una cita."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    x = t - sc.t0
    q = sc.since(t, "quote")
    m = ease_io(q / 0.5) if q > 0 else 0.0
    grow = (0.3 + 0.7 * back_out(x / 0.45))
    fr.paste(asterisk(lerp(500, 150, m) * grow, YEL, -120 * (1 - ease_out(x / 0.7))), W / 2, lerp(690, 430, m), al)
    ta = (1 - m) * ease_out((x - 0.15) / 0.3)
    text(d, (W / 2, 1040), p["title"], fit(p["title"], BLACK, 120, 880), mix(WHITE, al * ta))
    if m > 0:
        lines = p["qlines"]
        f = fit(max(lines, key=len), HEAVY, 74, 860)
        lh = f.size * 1.24
        y0 = 770 - lh * (len(lines) - 1) / 2
        for i, ln in enumerate(lines):
            a = ease_out((q - 0.25 - i * 0.12) / 0.3)
            text(d, (W / 2, y0 + i * lh + (1 - a) * 20), ln, f, mix(YEL if i in p.get("hot", []) else WHITE, al * a))
        a = ease_out((q - 0.8) / 0.4)
        ya = y0 + len(lines) * lh + 30
        text(d, (W / 2, ya), p["attr1"], fit(p["attr1"], HEAVY, 42, 860), mix(WHITE, al * a))
        text(d, (W / 2, ya + 56), p["attr2"], fit(p["attr2"], SEMI, 34, 860), mix(DIM, al * a))


def statement(fr, t, sc):
    """Tarjeta tipo estado de resultados con dos renglones y una barra de proporcion."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    kicker(fr, p["kicker"], al)
    card(d, [X0, 400, X1, 800], al)
    text(d, (X0 + 50, 452), p["doc"], fit(p["doc"], SEMI, 30, 780), mix(DIM, al), "lm")
    line(d, [(X0 + 50, 494), (X1 - 50, 494)], fill=mix(EDGE, al), width=3)
    a1, a2 = sc.on(t, "fees", 0.3), sc.on(t, "profit", 0.3)
    cardc = mix(CARD, al)
    if a1 > 0.004:
        rrect(d, [X0 + 26, 528, X1 - 26, 642], 18, fill=mix(mix(YEL, 0.15, base=CARD), al * a1, base=cardc))
    lw = p.get("lw", 500)
    text(d, (X0 + 60, 585), p["r1"], fit(p["r1"], SEMI, 50, lw), mix(WHITE, al * a1, base=cardc), "lm")
    text(d, (X1 - 60, 585), p["v1"], font(BLACK, 66), mix(YEL, al * sc.on(t, "v1", 0.25), base=cardc), "rm")
    text(d, (X0 + 60, 715), p["r2"], fit(p["r2"], SEMI, 50, lw), mix(WHITE, al * a2, base=cardc), "lm")
    text(d, (X1 - 60, 715), p["v2"], font(BLACK, 66), mix(WHITE, al * a2, base=cardc), "rm")
    xr = sc.since(t, "pct")
    g = ease_io(xr / 1.0) if xr > 0 else 0.0
    text(d, (X0, 882), p["ratio"], fit(p["ratio"], SEMI, 36, 880), mix(DIM, al * a2), "lm")
    rrect(d, [X0, 925, X1, 1005], 40, fill=mix(EDGE, al * a2))
    if g > 0:
        rrect(d, [X0, 925, X0 + max(80, (X1 - X0) * p["pct"] / 100 * g), 1005], 40, fill=mix(YEL, al))
        text(d, (W / 2, 1118), p["pfmt"].format(p["pct"] * g), font(BLACK, 150), mix(YEL, al * clamp(xr / 0.15)))


def ring_scene(fr, t, sc):
    """Anillo de porcentaje."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    kicker(fr, p["kicker"], al)
    x = sc.since(t, "go")
    g = ease_io(x / 1.2) if x > 0 else 0.0
    fr.paste(ring(560, 58, p["pct"] / 100 * g), W / 2, 700, al)
    text(d, (W / 2, 700), p["pfmt"].format(p["pct"] * g), font(BLACK, 118), mix(WHITE, al))
    text(d, (W / 2, 1065), p["l1"], fit(p["l1"], HEAVY, 50, 880), mix(WHITE, al))
    text(d, (W / 2, 1135), p["l2"], fit(p["l2"], SEMI, 36, 880), mix(DIM, al))


def close(fr, t, sc):
    """Tres pasos del mecanismo y vuelta al cuadro inicial para que el video haga bucle."""
    p, d = sc.p, fr.d
    xb = sc.since(t, "back")
    m = ease_io(xb / 0.5) if xb > 0 else 0.0
    alA, alB = sc.alpha(t) * (1 - m), m
    if alA > 0.004:
        kicker(fr, p["kicker"], alA)
        steps = (("s1", p["s1"], 500, YEL), ("s2", p["s2"], 740, EDGE), ("s3", p["s3"], 980, GRN))
        for i, (cue, label, y, col) in enumerate(steps):
            a = sc.on(t, cue, 0.3)
            if a <= 0.004:
                continue
            dy = (1 - a) * 30
            if i > 0:
                line(d, [(W / 2, y - 156), (W / 2, y - 104)], fill=mix(DIM, alA * a), width=6)
                poly(d, [(W / 2 - 18, y - 106), (W / 2 + 18, y - 106), (W / 2, y - 80)], fill=mix(DIM, alA * a))
            card(d, [150, y - 72 + dy, 930, y + 72 + dy], alA * a, outline=col, width=4)
            if i == 0:
                fr.paste(hotdog(150), 262, y + dy, alA * a)
                text(d, (362, y + dy), label, fit(label, HEAVY, 50, 530), mix(WHITE, alA * a), "lm")
            else:
                text(d, (W / 2, y + dy), label, fit(label, HEAVY, 50, 720), mix(WHITE, alA * a))
    if alB > 0.004:
        kicker(fr, p["kicker0"], alB)
        left = sc.t1 - t
        _price_block(fr, alB, p, t, 1.0, clamp((left - 0.05) / 0.3), 0.0, 1.0, 1.0)
        _timeline(fr, alB, p, 1.0)


# ---------- escenas genericas (cifra grande, barra partida, cierre con bucle) ----------
def _num_block(fr, al, p, ast=0.0, ast_a=0.0, rot=0.0, scale=1.0, sub2_a=0.0):
    f = fit(p["num"], BLACK, 250, 800)
    f = font(BLACK, f.size * scale)
    text(fr.d, (W / 2, 640), p["num"], f, mix(YEL, al))
    text(fr.d, (W / 2, 820), p["sub"], fit(p["sub"], HEAVY, 52, 860), mix(WHITE, al))
    if p.get("sub2"):
        text(fr.d, (W / 2, 960), p["sub2"], fit(p["sub2"], SEMI, 44, 860), mix(DIM, al * sub2_a))
    if ast_a > 0.004:
        fr.paste(asterisk(118 * max(0.2, ast), YEL, rot), min(X1 - 50, W / 2 + f.getlength(p["num"]) / 2 + 40), 520, al * ast_a)


def bignum(fr, t, sc):
    """Gancho: una cifra enorme y, al final, su asterisco."""
    al, p = sc.alpha(t), sc.p
    kicker(fr, p["kicker"], al)
    xa = sc.since(t, "ast")
    ast = back_out(xa / 0.4) if xa > 0 else 0.0
    rot = -90 * (1 - ease_out(xa / 0.55)) if xa > 0 else 0.0
    punch = 1.0 + 0.10 * (1 - ease_out((t - sc.t0) / 0.45))
    _num_block(fr, al, p, ast, clamp(xa / 0.08) if xa > 0 else 0.0, rot, punch, sc.on(t, "sub2", 0.4) if "sub2" in sc.cues else 0.0)


def split(fr, t, sc):
    """Dos barras partidas: el mismo reparto visto en ventas y en ganancia."""
    al, p, d = sc.alpha(t), sc.p, fr.d
    kicker(fr, p["kicker"], al)
    for cue, title, a, y in (("sp1", p["t1"], p["a1"], 450), ("sp2", p["t2"], p["a2"], 820)):
        v = ease_out((t - sc.t0) / 0.35) if cue == "sp1" else sc.on(t, cue, 0.35)   # la primera barra espera en 50/50
        if v <= 0.004:
            continue
        g = ease_io(sc.since(t, cue) / 1.0) if sc.since(t, cue) > 0 else 0.0
        cut = X0 + (X1 - X0) * lerp(50, a, g) / 100
        text(d, (X0, y), title, fit(title, HEAVY, 46, 880), mix(WHITE, al * v), "lm")
        rrect(d, [X0, y + 45, X1, y + 145], 26, fill=mix(GRN, al * v))
        rrect(d, [X0, y + 45, cut, y + 145], 26, fill=mix(YEL, al * v))
        rrect(d, [cut - 30, y + 45, cut, y + 145], 0, fill=mix(YEL, al * v))
        text(d, (X0, y + 195), "%d%%  %s" % (round(lerp(50, a, g)), p["la"]), font(HEAVY, 44), mix(YEL, al * v), "lm")
        text(d, (X1, y + 195), "%s  %d%%" % (p["lb"], round(100 - lerp(50, a, g))), font(HEAVY, 44), mix(GRN, al * v), "rm")


def close_num(fr, t, sc):
    """Tres tarjetas de cierre y vuelta al cuadro inicial (bucle)."""
    p, d = sc.p, fr.d
    xb = sc.since(t, "back")
    m = ease_io(xb / 0.5) if xb > 0 else 0.0
    alA, alB = sc.alpha(t) * (1 - m), m
    if alA > 0.004:
        kicker(fr, p["kicker"], alA)
        pre = 1 - sc.on(t, "s1", 0.25)
        for i, ln in enumerate(p.get("pre", [])):
            text(d, (W / 2, 700 + (i - (len(p["pre"]) - 1) / 2) * 130), ln, fit(ln, BLACK, 110, 860),
                 mix(YEL if i else WHITE, alA * pre * ease_out((t - sc.t0 - i * 0.5) / 0.3)))
        for cue, label, y, col in (("s1", p["s1"], 560, YEL), ("s2", p["s2"], 860, GRN)):
            a = sc.on(t, cue, 0.3)
            if a <= 0.004:
                continue
            dy = (1 - a) * 30
            card(d, [X0, y - 110 + dy, X1, y + 110 + dy], alA * a, outline=col, width=5)
            for i, ln in enumerate(label):
                text(d, (W / 2, y + dy + (i - (len(label) - 1) / 2) * 70), ln, fit(ln, HEAVY, 56, 820), mix(WHITE, alA * a))
    if alB > 0.004:
        kicker(fr, p["kicker0"], alB)
        _num_block(fr, alB, p, 1.0, clamp((sc.t1 - t - 0.05) / 0.3), 0.0, 1.0, 0.0)

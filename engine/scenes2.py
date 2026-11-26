"""Escenas v2 (fondo tematico, composicion RGBA, objetos reconocibles).

Cada escena: fn(fr, t, sc). sc.lcues son los cues de ESTA escena.
SFX[nombre](sc) devuelve efectos extra [(t, tipo)] que la escena necesita.
"""
import math
import numpy as np
from PIL import Image, ImageDraw

from core import *          # noqa: F401,F403
from core import ring
from fx import *            # noqa: F401,F403
import fx

SFX = {}
KICK = (255, 175, 225)


def lc(sc, name, default=None):
    if name in sc.lcues:
        return sc.lcues[name]
    return sc.t0 if default is None else default


def kick(fr, txt, a=1.0):
    say(fr, txt, W / 2, KICK_Y, 42, KICK, SEMI, a, maxw=860)


def say_l(fr, txt, x, cy, size, color=WHITE, fname=BLACK, a=1.0, s=1.0, maxw=900, glow=None):
    sz = tfit(txt, fname, size, maxw)
    spr = tsprite(txt, fname, sz, color, glow=glow)
    put(fr, spr, x + spr.width * s / 2, cy, s, a)


def slam(k, big=2.3, dur=0.26):
    """Escala de 'golpe': entra enorme y aterriza en 1."""
    return lerp(big, 1.0, ease_out(k / dur)) if k > 0 else 0.0


def _flip_cal(fr, cx, cy, w, labels, u, header=PINK, a=1.0):
    """Calendario que arranca hojas: u de 0 a 1 recorre labels."""
    n = len(labels) - 1
    pos = clamp(u) * n
    i = min(n, int(pos))
    f = pos - i
    put(fr, calendar(w, labels[min(n, i + 1)][0], labels[min(n, i + 1)][1], header), cx, cy, 1.0, a if i < n else 0)
    cur = calendar(w, labels[i][0], labels[i][1], header)
    if i < n and f > 0.02:
        sq = max(0.02, 1 - f)
        spr = cur.resize((cur.width, max(2, int(cur.height * sq))), Image.BILINEAR)
        spr = spr.rotate(-14 * f, resample=Image.BICUBIC, expand=True)
        fr.paste(spr, cx + 30 * f, cy - cur.height * (1 - sq) / 2 - 60 * f, a * (1 - 0.5 * f))
    else:
        put(fr, cur, cx, cy, 1.0, a)


# ============ 1. gancho: pregunta + calendario + control ============
def q_hook(fr, t, sc):
    p = sc.p
    x = t - sc.t0
    yrs, mon = lc(sc, "yrs"), sc.lcues.get("money")
    m = appear(t - mon, 0.14) if mon is not None else 0.0
    kick(fr, p["kicker"], 1 - m)
    say(fr, p["q1"], W / 2, 400, 70, WHITE, BLACK, a=1 - m, maxw=900)
    k = t - yrs
    punch = 1 + 0.28 * (1 - ease_out(k / 0.3)) if k > 0 else 1 + 0.03 * math.sin(t * 9)
    say(fr, p["q2"], W / 2, 545, 178, YEL, BLACK, a=1 - m, s=punch * (0.85 + 0.15 * pop(x, 0.25)),
        glow=(PINK, 20, 1.5) if k > 0 else (PINK, 12, 0.9))
    fe = (yrs - sc.t0) + p.get("flip_tail", 0.9)
    labels = [(p.get("cal_top", "YEAR"), str(y)) for y in range(p["y0"], p["y1"] + 1)]
    cy = 865 - 40 * m
    _flip_cal(fr, W / 2, cy, 360, labels, ease_io(x / fe) if x < fe else 1.0, a=1 - m)
    # control que "espera" impaciente
    jit = 4 * math.sin(t * 23) if x < fe else 1.5 * math.sin(t * 6)
    put(fr, controller(270), W / 2, 1180 + 220 * m, 1.0, 1 - m, jit)
    if m > 0:
        km = t - mon
        rng = np.random.default_rng(3)
        for i in range(14):
            ang = rng.uniform(-math.pi * 0.95, -math.pi * 0.05)
            v = rng.uniform(1100, 1900)
            spin = rng.uniform(-420, 420)
            r0 = rng.uniform(0, 360)
            bx = W / 2 + math.cos(ang) * v * km
            by = cy + math.sin(ang) * v * km + 900 * km * km
            if -200 < by < H + 200:
                put(fr, bill(140, r0 + spin * km), bx, by, 1.0, clamp(1.4 - km * 0.8))
        say(fr, p["m1"], W / 2, 640, 120, WHITE, BLACK, a=appear(km, 0.08), s=pop(km), stroke=0)
        say(fr, p["m2"], W / 2, 790, 150, GRN, BLACK, a=appear(km - 0.12, 0.08), s=pop(km - 0.12), glow=(GRN, 18, 1.2))


def _hook_sfx(sc):
    fe = lc(sc, "yrs") + sc.p.get("flip_tail", 0.9)
    n = sc.p["y1"] - sc.p["y0"]
    ev = [(sc.t0 + (fe - sc.t0) * (i / n) ** 0.9, "tick") for i in range(1, n + 1)]
    if "money" in sc.lcues:
        ev.append((sc.lcues["money"], "cash"))
    return ev


SFX["q_hook"] = _hook_sfx


# ============ 2. carrera al billon ============
def race(fr, t, sc):
    p = sc.p
    kick(fr, p["kicker"])
    go, win = lc(sc, "go"), lc(sc, "win")
    fin = win + p.get("win_land", 1.35)
    mov = sc.lcues.get("mov")
    pa = ease_io((t - go) / (fin - go)) if t > go else 0.0
    days = 3 * pa
    if mov is not None and t > mov:
        days = 3 + 16 * ease_io((t - mov) / p.get("ff", 1.9))
    pb = days / 19.0
    # contador de dinero
    val = int(round(1e9 * pa / 1e6)) * 1e6 if pa < 1 else 1e9
    done = t >= fin
    say(fr, "$" + format(int(val), ","), W / 2, 445, 104, YEL if done else WHITE, BLACK,
        glow=(PINK, 18, 1.4) if done else None, s=1 + 0.08 * (1 - ease_out((t - fin) / 0.3)) if done else 1.0)
    say(fr, p["goal"], W / 2, 535, 34, KICK, SEMI)
    # meta
    put(fr, checker(34, 470, 17), 910, 790)
    xa, xb = 236, 890
    for lane, (y, prog, icon, lab, c1, c2) in enumerate(((680, pa, disc(116), p["l1"], YEL, ORANGE),
                                                          (920, pb, clapper(118), p["l2"], PURPLE, PINK))):
        put(fr, icon, 150, y)
        say_l(fr, lab, xa, y - 74, 40, WHITE, HEAVY, maxw=560)
        put(fr, bar(xb - xa, 64, (60, 34, 96), (40, 22, 70), r=32), (xa + xb) / 2, y)
        wv = max(64, (xb - xa) * clamp(prog))
        put(fr, bar(wv, 64, c1, c2, r=32), xa + wv / 2, y)
    # sellos de llegada
    if done:
        k = t - fin
        put(fr, stamp(p["s1"], 46, YEL), 720, 598, slam(k, 2.0, 0.22), appear(k, 0.05), -6)
    if mov is not None and days >= 18.99:
        k = t - (mov + p.get("ff", 1.9))
        put(fr, stamp(p["s2"], 46, PINK), 700, 1000, slam(k, 2.0, 0.22), appear(k, 0.05), 6)
    # dia grande
    rec = sc.lcues.get("rec")
    dd = max(1, int(math.ceil(days - 1e-6))) if t > go else 0
    ra = appear(t - rec, 0.12) if rec is not None and t > rec else 0.0
    if dd:
        say(fr, f'{p["day"]} {dd}', W / 2, 1150, 92, YEL if days <= 3.001 else PINK, BLACK, a=1 - ra)
    if ra > 0:
        k = t - rec
        put(fr, stamp(p["rec_txt"], 96, YEL), W / 2, 1140, slam(k, 2.6, 0.24), appear(k, 0.05), -8)


def _race_sfx(sc):
    ev = []
    win = lc(sc, "win") + sc.p.get("win_land", 1.35)
    ev.append((win, "cash"))
    if "mov" in sc.lcues:
        ev.append((sc.lcues["mov"] + sc.p.get("ff", 1.9), "thump"))
    if "rec" in sc.lcues:
        ev.append((sc.lcues["rec"], "boom"))
    return ev


SFX["race"] = _race_sfx


# ============ 3. corte: "pero no por eso esperaron" ============
def interrupt(fr, t, sc):
    p = sc.p
    k = t - sc.t0
    shade(fr, 0.86)
    jit = (1 - ease_out(k / 0.35))
    rng = np.random.default_rng(int(t * 30))
    ys = p.get("ys", [640, 800, 960])
    for i, (ln, y) in enumerate(zip(p["lines"], ys)):
        a = appear(k - 0.06 * i, 0.06)
        hot = i in p.get("hot", [])
        dx, dy = rng.uniform(-18, 18) * jit, rng.uniform(-10, 10) * jit
        say(fr, ln, W / 2 + dx, y + dy, 132, PINK if hot else WHITE, BLACK, a=a, s=slam(k - 0.06 * i, 1.4, 0.18),
            glow=(PINK, 22, 1.4) if hot else None)
    fr.im = rgb_split(fr.im, 16 * jit)
    fr.d = ImageDraw.Draw(fr.im)


SFX["interrupt"] = lambda sc: [(sc.t0 + 0.02, "glitch")]


# ============ 4. consolas: el mismo juego vuelve ============
def consoles(fr, t, sc):
    p = sc.p
    kick(fr, p["kicker"])
    xs = [230, 540, 850]
    cues = [lc(sc, c) for c in ("c1", "c2", "c3")]
    active = 0
    for i, c in enumerate(cues):
        if t >= c:
            active = i
    # linea de tiempo
    line(fr.d, [(xs[0], 1050), (xs[2], 1050)], fill=(120, 60, 150), width=6)
    for i, (x, c) in enumerate(zip(xs, cues)):
        k = t - c
        s = pop(k, 0.34)
        if s <= 0:
            continue
        put(fr, console(250, [PINK, TEAL, ORANGE][i]), x, 790, s)
        say(fr, p["years"][i], x, 940, 66, YEL, BLACK, a=appear(k, 0.2))
        say(fr, p["subs"][i], x, 995, 28, KICK, SEMI, a=appear(k - 0.1, 0.2), maxw=290)
        r = 14 * s
        oval(fr.d, [x - r, 1050 - r, x + r, 1050 + r], fill=YEL)
    # la caja del juego salta a la consola activa
    k = t - cues[active]
    prev = xs[max(0, active - 1)] if active > 0 else xs[0]
    u = ease_io(k / 0.45)
    cx = lerp(prev, xs[active], u) if active > 0 else xs[0]
    hop = -150 * math.sin(math.pi * clamp(k / 0.45)) if active > 0 else 0
    cy = 520 + hop + 10 * math.sin(t * 4)
    put(fr, game_case(150), cx, cy, pop(t - sc.t0, 0.35), 1.0, 6 * math.sin(t * 3))
    if t > cues[2] + 0.9:
        kf = t - cues[2] - 0.9
        put(fr, pill(p["foot"], 40, INK, YEL), W / 2, 1150, pop(kf))


SFX["consoles"] = lambda sc: [(lc(sc, c), "pop") for c in ("c1", "c2", "c3")]


# ============ 5. torre de copias ============
def tower(fr, t, sc):
    p = sc.p
    kick(fr, p["kicker"])
    c = lc(sc, "count")
    land = p.get("land", 1.6)
    g = ease_out((t - c) / land) if t > c else 0.0
    val = int(p["value"] * p.get("mult", 1e6) * g)
    say(fr, p.get("pre", ""), W / 2, 380, 40, KICK, HEAVY) if p.get("pre") else None
    say(fr, p.get("prefix", "") + format(val, ","), W / 2, 470, 132, YEL, BLACK, glow=(ORANGE, 18, 1.2) if g >= 0.999 else None, maxw=920)
    say(fr, p["sub"], W / 2, 572, 40, WHITE, HEAVY)
    cols, rows, cw, rh = 12, 7, 64, 80
    x0 = W / 2 - (cols - 1) * cw / 2
    total = cols * rows
    shown = total * g
    for i in range(total):
        if i >= shown:
            break
        r, col = divmod(i, cols)
        kk = (shown - i) / 6.0
        spr = box(60) if p.get("item") == "box" else game_case(54, [PINK, ORANGE, TEAL, PURPLE][(i * 7) % 4],
                                                                     [ORANGE, PINK, PURPLE, TEAL][(i * 3) % 4])
        put(fr, spr, x0 + col * cw, 1185 - r * rh, clamp(0.4 + kk), 1.0)
    b = sc.lcues.get("badge")
    if b is not None and t > b:
        k = t - b
        put(fr, pill(p["badge"], 58, WHITE, PINK, 40, 22, BLACK), W / 2, 900, slam(k, 2.2, 0.24), appear(k, 0.05), -5)


SFX["tower"] = lambda sc: ([(lc(sc, "count") + sc.p.get("land", 1.6), "ding")] +
                           ([(sc.lcues["badge"], "boom")] if "badge" in sc.lcues else []))


# ============ 6. el asterisco ============
_glow_cache = {}


def _glow_disc(r, color):
    key = (int(r), color)
    if key not in _glow_cache:
        n = int(r * 3)
        im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
        from PIL import ImageDraw as _D, ImageFilter as _F
        _D.Draw(im).ellipse([r, r, 2 * r, 2 * r], fill=color + (170,))
        _glow_cache[key] = im.filter(_F.GaussianBlur(r * 0.35))
    return _glow_cache[key]


def _coins(fr, t, start, n=14, seed=5, y_to=None):
    if t < start:
        return
    rng = np.random.default_rng(seed)
    for i in range(n):
        delay = rng.uniform(0, 1.6)
        k = t - start - delay
        if k < 0:
            continue
        x = rng.uniform(120, 960)
        y = -80 + 380 * k + 700 * k * k
        if y > (y_to or H + 100):
            continue
        sp = coin(76)
        w = max(4, int(sp.width * abs(math.cos(k * rng.uniform(5, 9) + i))))
        fr.paste(sp.resize((w, sp.height), Image.BILINEAR), x, y, 0.95)


def reveal2(fr, t, sc):
    """El asterisco sale desde el horizonte (abajo, sin tapar nada); el texto manda en el centro."""
    p = sc.p
    x = t - sc.t0
    q = sc.lcues.get("quote")
    m = ease_io((t - q) / 0.5) if q is not None and t > q else 0.0
    if q is not None:
        _coins(fr, t, q + 0.4, 16)
    # asterisco: sube desde el horizonte como el sol, chico y abajo
    rise = ease_out(x / 0.6)
    size = 210 * (0.4 + 0.6 * back_out(x / 0.5))
    cy = lerp(1720, 1585, rise)
    put(fr, _glow_disc(size * 0.6, PINK), W / 2, cy, 1.0, 0.8 * rise)
    fr.paste(asterisk(size, YEL, -120 * (1 - ease_out(x / 0.7)) + 18 * t), W / 2, cy, rise)
    ta = (1 - m) * appear(x - 0.1, 0.25)
    say(fr, p["title"], W / 2, 760, 150, WHITE, BLACK, a=ta, s=slam(x - 0.1, 1.8, 0.25), glow=(PINK, 20, 1.3))
    if m > 0:
        lines = p["qlines"]
        y0 = 560
        for i, ln in enumerate(lines):
            k = t - q - 0.25 - i * 0.14
            hot = i in p.get("hot", [])
            say(fr, ln, W / 2, y0 + i * 112 + (1 - appear(k, 0.3)) * 26, 92, YEL if hot else WHITE, BLACK,
                a=appear(k, 0.3), glow=(ORANGE, 14, 1.1) if hot else None, maxw=920)


SFX["reveal2"] = lambda sc: [(sc.t0, "boom"), (sc.t0 + 0.06, "ding")]


# ============ 7. anillo: cuanto viene de gastar dentro del juego ============
def ring2(fr, t, sc):
    p = sc.p
    kick(fr, p["kicker"])
    c = lc(sc, "count")
    land = p.get("land", 1.3)
    g = ease_io((t - c) / land) if t > c else 0.0
    _coins(fr, t, c - 0.2, 12, 9, y_to=700)
    fr.paste(ring(540, 64, p["pct"] / 100 * g, YEL, (70, 36, 104)), W / 2, 720)
    say(fr, p["fmt"].format(p["pct"] * g), W / 2, 720, 138, YEL if g >= 0.999 else WHITE, BLACK,
        glow=(PINK, 18, 1.3) if g >= 0.999 else None)
    say(fr, p["l1"], W / 2, 1045, 44, WHITE, HEAVY, a=appear(t - c, 0.3), maxw=900)
    ch = sc.lcues.get("chips")
    if ch is not None:
        sprs = [pill(s, 36, INK, col) for s, col in zip(p["chips"], (TEAL, YEL, PINK))]
        gap = 22
        tw = sum(s.width for s in sprs) + gap * (len(sprs) - 1)
        scale = min(1.0, 900 / tw)
        xx = W / 2 - tw * scale / 2
        for i, s in enumerate(sprs):
            k = t - ch - 0.18 * i
            put(fr, s, xx + s.width * scale / 2, 1145, scale * pop(k, 0.3))
            xx += (s.width + gap) * scale


SFX["ring2"] = lambda sc: ([(lc(sc, "count") + sc.p.get("land", 1.3), "ding")] +
                           [(sc.lcues["chips"] + 0.18 * i, "pop") for i in range(3) if "chips" in sc.lcues])


# ============ 8. la apuesta: fecha y precio ============
def bet(fr, t, sc):
    p = sc.p
    kick(fr, p["kicker"])
    x = t - sc.t0
    say(fr, p["title"], W / 2, 450, 160, WHITE, BLACK, s=pop(x, 0.35), glow=(PINK, 22, 1.5))
    d = sc.lcues.get("date")
    if d is not None and t > d:
        k = t - d
        put(fr, calendar(300, p["cal_top"], p["cal_big"]), 290, 800, pop(k, 0.35), 1.0, -5 * (1 - ease_out(k / 0.5)))
        say(fr, p["cal_label"], 290, 1020, 40, YEL, HEAVY, a=appear(k - 0.15, 0.25), maxw=420)
    pr = sc.lcues.get("price")
    if pr is not None and t > pr:
        k = t - pr
        sw = 26 * math.exp(-3.2 * k) * math.cos(10 * k)
        xin = lerp(1300, 770, ease_out(k / 0.35))
        line(fr.d, [(xin - 100, 560), (xin - 120, 790)], fill=(230, 220, 255), width=4)
        oval(fr.d, [xin - 110, 550, xin - 90, 570], fill=(230, 220, 255))
        put(fr, price_tag(360, p["price"], p["price_sub"]), xin, 800, 1.0, 1.0, sw)
        say(fr, p["ult"], 770, 1020, 34, KICK, HEAVY, a=appear(k - 0.4, 0.3), maxw=420)


SFX["bet"] = lambda sc: [(sc.lcues[c], s) for c, s in (("date", "pop"), ("price", "cash")) if c in sc.lcues]


# ============ 9. barras: lo que Take-Two espera ============
def bars2(fr, t, sc):
    p = sc.p
    kick(fr, p["kicker"])
    base, hmax, bw = 1120, 540, 240
    xs = (320, 760)
    h1 = hmax * p["v1"] / p["v2"]
    a1, a2 = lc(sc, "last"), sc.lcues.get("grow")
    g1 = ease_out((t - a1) / 0.7) if t > a1 else 0.0
    g2 = ease_io((t - a2) / 1.1) if a2 is not None and t > a2 else 0.0
    line(fr.d, [(X0 + 20, base), (X1 - 20, base)], fill=(150, 90, 190), width=4)
    for i, (x, h, g, c1, c2, glow) in enumerate(((xs[0], h1, g1, PURPLE, (80, 40, 160), None),
                                                  (xs[1], hmax, g2, YEL, ORANGE, (PINK, 16)))):
        hh = max(6, h * g)
        if g > 0:
            put(fr, bar(bw, hh, c1, c2, r=24, glow=glow if g >= 0.999 else None), x, base - hh / 2)
            v = p["v1"] if i == 0 else lerp(p["v1"], p["v2"], g)
            say(fr, p["fmt"].format(v), x, base - hh - 60, 76, WHITE if i == 0 else YEL, BLACK, a=appear(g * 3, 1))
        say(fr, p["labels"][i], x, base + 48, 32, KICK, HEAVY, maxw=380)
        if len(p.get("labels2", [])) > i:
            say(fr, p["labels2"][i], x, base + 88, 26, DIM, SEMI, maxw=380)
    if a2 is not None and t > a2 + 1.2:
        k = t - a2 - 1.2
        put(fr, pill(p["badge"], 46, WHITE, PINK, 30, 18, BLACK), xs[1], base - hmax - 170, slam(k, 2.0, 0.22), 1.0, -4)


SFX["bars2"] = lambda sc: [(sc.lcues["grow"] + 1.2, "boom")] if "grow" in sc.lcues else []


# ============ 10. preventas: no lo dicen ============
def classified(fr, t, sc):
    p = sc.p
    kick(fr, p["kicker"])
    x = t - sc.t0
    s = pop(x, 0.35)
    put(fr, panel(760, 560, (244, 240, 252, 255), None, 30), W / 2, 760, s)
    if s > 0.6:
        say(fr, p["doc"], W / 2, 560, 40, (40, 30, 70), HEAVY, maxw=640)
        dr = fr.d
        for i, (wid, y) in enumerate(((560, 650), (460, 712), (600, 774))):
            rrect(dr, [W / 2 - 300, y - 18, W / 2 - 300 + wid, y + 18], 8, fill=(205, 198, 222))
        rrect(dr, [W / 2 - 300, 840, W / 2 + 300, 960], 14, fill=(20, 14, 34))
        say(fr, p.get("mystery", "? ? ?"), W / 2, 900, 70 if "mystery" not in p else 52, (90, 80, 120) if "mystery" not in p else (215, 205, 245), BLACK, maxw=560)
    st = sc.lcues.get("stamp")
    if st is not None and t > st:
        k = t - st
        put(fr, stamp(p["stamp"], 78, RED), W / 2, 780, slam(k, 2.4, 0.22), appear(k, 0.05), -12)
    sb = sc.lcues.get("sub")
    if sb is not None and t > sb:
        k = t - sb
        say(fr, p["quote"], W / 2, 1120, 54, YEL, BLACK, a=appear(k, 0.3), s=pop(k, 0.35), glow=(PINK, 14, 1.0), maxw=920)
        say(fr, p["attr"], W / 2, 1190, 30, KICK, SEMI, a=appear(k - 0.2, 0.3))


SFX["classified"] = lambda sc: [(sc.lcues["stamp"], "boom")] if "stamp" in sc.lcues else []


# ============ 11. respuesta y llamada a la accion ============
def answer_cta(fr, t, sc):
    p = sc.p
    x = t - sc.t0
    ans, fol, like = sc.lcues.get("ans"), sc.lcues.get("fol"), sc.lcues.get("like")
    mB = appear(t - fol, 0.3) if fol is not None and t > fol else 0.0
    mA = appear(t - ans, 0.3) if ans is not None and t > ans else 0.0
    a = 1 - mB
    if ans is not None and a > 0.004:
        _coins(fr, t, ans + 0.2, 12, 21)
    if a > 0.004:
        kick(fr, p["kicker"], a)
        say(fr, p["ask"], W / 2, 420, 108, WHITE, BLACK, a=a, s=pop(x, 0.3))
        if mA < 1 and "y0" in p:
            labels = [(p.get("cal_top", "YEAR"), str(y)) for y in range(p["y0"], p["y1"] + 1)]
            _flip_cal(fr, W / 2, 820, 300, labels, ease_io(x / 1.4), a=a * (1 - mA))
        elif mA < 1 and p.get("icon") == "bills":
            for j, xx in enumerate((330, 540, 750)):
                put(fr, bill(230, (-12, 4, 14)[j] + 6 * math.sin(t * 2 + j)), xx, 830 + 18 * math.sin(t * 3 + j),
                    pop(x - 0.1 * j, 0.3), a * (1 - mA))
        elif mA < 1 and p.get("icon") == "ballot":
            put(fr, ballot_box(330), W / 2, 880, pop(x, 0.3), a * (1 - mA))
            for j in range(3):
                ph = ((t * 0.8 + j / 3) % 1.0)
                put(fr, ballot_paper(120), W / 2 + (j - 1) * 30, lerp(600, 760, ease_io(ph)), 1.0, a * (1 - mA) * (1 - ph))
        elif mA < 1 and p.get("icon") == "case":
            for j, xx in enumerate((330, 540, 750)):
                put(fr, game_case(180, [PINK, ORANGE, TEAL][j], [ORANGE, PURPLE, PINK][j]), xx,
                    830 + 18 * math.sin(t * 3 + j), pop(x - 0.1 * j, 0.3), a * (1 - mA), (-8, 3, 10)[j])
        elif mA < 1 and p.get("icon") == "none":
            pass
        elif mA < 1:
            for j, xx in enumerate((330, 540, 750)):
                put(fr, rack(170, t, j), xx, 830, pop(x - 0.1 * j, 0.3), a * (1 - mA))
        if mA > 0:
            k = t - ans
            put(fr, pill(p["tag"], 34, INK, TEAL), W / 2, 590, pop(k, 0.3), a)
            say(fr, p["ans1"], W / 2, 740, 104, YEL, BLACK, a=a * appear(k, 0.2), s=pop(k - 0.05), glow=(PINK, 18, 1.3))
            say(fr, p["ans2"], W / 2, 870, 104, YEL, BLACK, a=a * appear(k - 0.12, 0.2), s=pop(k - 0.17), glow=(PINK, 18, 1.3))
    if mB > 0:
        k = t - fol
        sz = pop(k, 0.36) * (1 + 0.04 * math.sin(t * 7))
        for j in range(3):          # ondas de "toque"
            kk = (k - 0.3 - j * 0.35) % 1.4
            if k > 0.3:
                r = 120 + 260 * kk
                fr.d.ellipse([W / 2 - r, 680 - r * 0.42, W / 2 + r, 680 + r * 0.42],
                             outline=tuple(int(c * (1 - kk / 1.4)) for c in PINK), width=4)
        put(fr, pill(p["follow"], 76, WHITE, PINK, 60, 30, BLACK), W / 2, 680, sz)
        say(fr, p["follow_sub"], W / 2, 830, 40, WHITE, HEAVY, a=appear(k - 0.25, 0.3), maxw=900)
        if like is not None and t > like:
            kl = t - like
            put(fr, heart(190), W / 2, 1010, pop(kl, 0.34))
            rng = np.random.default_rng(8)
            for i in range(10):
                ang = rng.uniform(0, 2 * math.pi)
                dd = 60 + 380 * ease_out(kl / 0.7)
                if kl < 0.9:
                    put(fr, heart(46, [PINK, YEL, TEAL][i % 3]), W / 2 + math.cos(ang) * dd, 1010 + math.sin(ang) * dd,
                        1.0, 1 - kl / 0.9)
            say(fr, p["like_txt"], W / 2, 1165, 44, YEL, BLACK, a=appear(kl - 0.15, 0.3), maxw=900)


SFX["answer_cta"] = lambda sc: [(sc.lcues[c], s) for c, s in (("ans", "boom"), ("fol", "pop"), ("like", "pop")) if c in sc.lcues]


# ============ Amazon: gancho con caja ============
def box_hook(fr, t, sc):
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["q1"], W / 2, 410, 66, WHITE, BLACK, maxw=920)
    say(fr, p["q2"], W / 2, 520, 104, YEL, BLACK, s=0.85 + 0.15 * pop(x, 0.25), glow=(TEAL, 16, 1.1), maxw=940)
    if p.get("q3"):
        say(fr, p["q3"], W / 2, 635, 120, YEL, BLACK, s=0.85 + 0.15 * pop(x - 0.08, 0.25), glow=(TEAL, 16, 1.1), maxw=940)
    by = (920 if p.get("q3") else 880) - 90 * abs(math.sin(x * 6)) * math.exp(-x * 2.2) - 8 * abs(math.sin(t * 3))
    spr = game_case(270) if p.get("item") == "case" else box(360)
    put(fr, spr, W / 2, by, 1.0, 1.0, 3 * math.sin(t * 2))
    put(fr, pill(p["sales"], 40, INK, YEL), W / 2, 1115, pop(x - 0.6, 0.3))
    n = sc.lcues.get("not")
    if n is not None and t > n:
        k = t - n
        put(fr, stamp(p["stamp"], 70, RED), W / 2, 880, slam(k, 2.4, 0.22), appear(k, 0.05), -10)


SFX["box_hook"] = lambda sc: [(sc.t0 + 0.52, "thump")] + ([(sc.lcues["not"], "boom")] if "not" in sc.lcues else [])


# ============ Amazon: dos barras partidas (ventas vs ganancia) ============
def split2(fr, t, sc):
    p = sc.p
    kick(fr, p["kicker"])
    x = t - sc.t0
    q2 = sc.lcues.get("q2")
    hot = appear(t - q2, 0.3) if q2 is not None and t > q2 else 0.0
    rows = ((p["t1"], p["a1"], 600, sc.t0 + 0.2), (p["t2"], p["a2"], 940, lc(sc, "sp2")))
    for title, a, y, c in rows:
        v = appear(t - c + 0.4, 0.3)
        if v <= 0:
            continue
        g = ease_io((t - c) / 1.0) if t > c else 0.0
        pa = lerp(50, a, g)
        say_l(fr, title, X0, y - 92, 44, WHITE, HEAVY, a=v)
        L = X1 - X0
        wa = L * pa / 100
        put(fr, bar(wa, 110, YEL, ORANGE, r=20), X0 + wa / 2, y, 1.0, v)
        put(fr, bar(L - wa - 8, 110, TEAL, (30, 140, 170), r=20, glow=(TEAL, 14) if hot > 0.5 else None),
            X0 + wa + 8 + (L - wa - 8) / 2, y, 1.0, v)
        say(fr, "%d%%" % round(pa), X0 + wa / 2, y, 60, INK, BLACK, a=v)
        say(fr, "%d%%" % round(100 - pa), X0 + wa + 8 + (L - wa - 8) / 2, y, 60, INK, BLACK, a=v)
        say_l(fr, p["la"], X0, y + 92, 32, YEL, HEAVY, a=v)
        lab = p["lb"]
        sz = tfit(lab, HEAVY, 32, 400)
        spr = tsprite(lab, HEAVY, sz, TEAL)
        put(fr, spr, X1 - spr.width / 2, y + 92, 1 + 0.25 * hot * (0.5 + 0.5 * math.sin(t * 8)), v)


SFX["split2"] = lambda sc: [(lc(sc, "sp2"), "pop")] + ([(sc.lcues["q2"], "ding")] if "q2" in sc.lcues else [])


# ============ Costco: gancho con lluvia de billetes ============
def cash_hook(fr, t, sc):
    """Pregunta completa desde el cuadro 1; billetes que caen y se apilan; sello en el cue 'more'."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["q1"], W / 2, 405, 66, WHITE, BLACK, maxw=920)
    say(fr, p["q2"], W / 2, 535, 150, YEL, BLACK, s=0.85 + 0.15 * pop(x, 0.25), glow=(GRN, 18, 1.2), maxw=960)
    rng = np.random.default_rng(13)
    for i in range(16):                       # pila que crece
        k = x - i * 0.11
        if k <= 0:
            continue
        land = 1020 - (i // 4) * 26
        y = lerp(640, land, ease_out(min(1, k / 0.35)))
        put(fr, bill(250, rng.uniform(-14, 14)), W / 2 + rng.uniform(-150, 150), y, 1.0, appear(k, 0.08))
    for i in range(9):                        # billetes en el aire
        ph = (t * 0.35 + i / 9) % 1.0
        bx = 140 + (i * 113) % 820 + 30 * math.sin(t * 1.7 + i)
        by = 660 + 520 * ph
        put(fr, bill(120, (t * 90 + i * 40) % 360), bx, by, 1.0, 0.55 * (1 - ph))
    put(fr, pill(p["sales"], 40, INK, YEL), W / 2, 1150, pop(x - 0.6, 0.3))
    n = sc.lcues.get("more")
    if n is not None and t > n:
        k = t - n
        put(fr, stamp(p["stamp"], 60, RED), W / 2, 880, slam(k, 2.4, 0.22), appear(k, 0.05), -8)


SFX["cash_hook"] = lambda sc: [(sc.t0 + 0.5, "thump")] + ([(sc.lcues["more"], "boom")] if "more" in sc.lcues else [])


# ============ Costco: escalones (historial que crece) ============
def steps(fr, t, sc):
    """Barras que aparecen una por una; la ultima entra con golpe en el cue 'big'."""
    p = sc.p
    kick(fr, p["kicker"])
    items = p["items"]                        # [(etiqueta, valor), ...]
    n = len(items)
    vmax = max(v for _, v in items)
    base, hmax = 1110, 560
    L = X1 - X0
    gap = 26
    bw = (L - gap * (n - 1)) / n
    go, big = lc(sc, "go"), sc.lcues.get("big")
    step = p.get("gap", 0.42)
    line(fr.d, [(X0, base), (X1, base)], fill=(90, 170, 120), width=4)
    for i, (lab, v) in enumerate(items):
        last = i == n - 1
        st = (big if (last and big is not None) else go + i * step)
        if t < st:
            continue
        k = t - st
        g = ease_out(k / (0.45 if not last else 0.7))
        h = max(6, hmax * v / vmax * g)
        cx = X0 + bw / 2 + i * (bw + gap)
        c1, c2 = (YEL, ORANGE) if last else (GRN, (40, 130, 80))
        put(fr, bar(bw, h, c1, c2, r=18, glow=(PINK, 16) if last and g >= 0.999 else None), cx, base - h / 2)
        say(fr, p["fmt"].format(v * g if last else v), cx, base - h - 46, 54 if last else 46,
            YEL if last else WHITE, BLACK, a=appear(k, 0.15))
        say(fr, lab, cx, base + 44, 30, KICK, HEAVY, a=appear(k, 0.2), maxw=bw + gap)
    if big is not None and t > big + 1.0 and p.get("badge"):
        k = t - big - 1.0
        put(fr, pill(p["badge"], 46, WHITE, PINK, 30, 18, BLACK), X1 - 200, base - hmax - 120, slam(k, 2.0, 0.22), 1.0, -4)


SFX["steps"] = lambda sc: ([(lc(sc, "go") + i * sc.p.get("gap", 0.42), "pop") for i in range(len(sc.p["items"]) - 1)] +
                           ([(sc.lcues["big"], "boom")] if "big" in sc.lcues else []))


# ============ Nvidia / Meta: urna, papeleta y certificados de acciones ============
def ballot_box(w):
    """Urna generica: caja con ranura (sin logos)."""
    key = ("ballot_box", int(w))
    if key in fx._scache:
        return fx._scache[key]
    h = w * 0.9
    im, d = fx._new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    d.polygon([(W_ * 0.04, H_ * 0.26), (W_ * 0.26, H_ * 0.06), (W_ * 0.96, H_ * 0.06), (W_ * 0.74, H_ * 0.26)], fill=(200, 210, 235, 255))
    d.polygon([(W_ * 0.74, H_ * 0.26), (W_ * 0.96, H_ * 0.06), (W_ * 0.96, H_ * 0.78), (W_ * 0.74, H_ * 0.98)], fill=(120, 132, 170, 255))
    d.rectangle([W_ * 0.04, H_ * 0.26, W_ * 0.74, H_ * 0.98], fill=(165, 178, 214, 255))
    d.polygon([(W_ * 0.30, H_ * 0.17), (W_ * 0.38, H_ * 0.12), (W_ * 0.72, H_ * 0.12), (W_ * 0.64, H_ * 0.17)], fill=(30, 26, 50, 255))
    d.rounded_rectangle([W_ * 0.14, H_ * 0.48, W_ * 0.64, H_ * 0.76], 10 * S, fill=(245, 245, 252, 255))
    d.line([(W_ * 0.24, H_ * 0.62), (W_ * 0.33, H_ * 0.70), (W_ * 0.52, H_ * 0.53)], fill=(40, 170, 110, 255), width=int(9 * S))
    return fx._done(key, im, w, h)


def ballot_paper(w):
    key = ("ballot_paper", int(w))
    if key in fx._scache:
        return fx._scache[key]
    h = w * 1.25
    im, d = fx._new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 6 * S, fill=(250, 248, 255, 255))
    for i in range(3):
        y = H_ * (0.22 + i * 0.25)
        d.rectangle([W_ * 0.12, y, W_ * 0.30, y + H_ * 0.13], outline=(60, 50, 90, 255), width=int(2 * S))
        d.rectangle([W_ * 0.38, y + H_ * 0.04, W_ * 0.86, y + H_ * 0.08], fill=(190, 185, 210, 255))
    d.line([(W_ * 0.13, H_ * 0.28), (W_ * 0.20, H_ * 0.34), (W_ * 0.31, H_ * 0.20)], fill=(220, 50, 70, 255), width=int(4 * S))
    return fx._done(key, im, w, h)


def cert(w, title, votes, accent=GRN, sub="SHARE CERTIFICATE"):
    """Certificado de accion generico con su numero de votos."""
    key = ("cert", int(w), title, votes, accent, sub)
    if key in fx._scache:
        return fx._scache[key]
    h = w * 0.66
    S = 2
    im, d = fx._new(w, h, S)
    W_, H_ = w * S, h * S
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 18 * S, fill=(246, 240, 222, 255))
    d.rounded_rectangle([10 * S, 10 * S, W_ - 10 * S, H_ - 10 * S], 12 * S, outline=accent + (255,), width=int(5 * S))
    d.rounded_rectangle([20 * S, 20 * S, W_ - 20 * S, H_ - 20 * S], 8 * S, outline=accent + (140,), width=int(2 * S))
    d.text((W_ / 2, H_ * 0.22), sub, font=font(SEMI, int(w * 0.055 * S)), fill=(90, 80, 70, 255), anchor="mm")
    d.text((W_ / 2, H_ * 0.43), title, font=font(BLACK, int(tfit(title, BLACK, w * 0.12, w * 0.8) * S)), fill=(30, 26, 40, 255), anchor="mm")
    r = H_ * 0.17
    d.ellipse([W_ / 2 - r * 2.6, H_ * 0.72 - r, W_ / 2 + r * 2.6, H_ * 0.72 + r], fill=accent + (255,))
    d.text((W_ / 2, H_ * 0.72), votes, font=font(BLACK, int(tfit(votes, BLACK, w * 0.10, w * 0.46) * S)), fill=INK + (255,), anchor="mm")
    return fx._done(key, im, w, h)


def ballot_hook(fr, t, sc):
    """Pregunta completa desde el cuadro 1; urna con papeletas que caen; sello en el cue 'no'."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["q1"], W / 2, 400, 60, WHITE, BLACK, maxw=940)
    say(fr, p["q2"], W / 2, 510, 92, YEL, BLACK, s=0.85 + 0.15 * pop(x, 0.25), glow=(TEAL, 16, 1.1), maxw=960)
    say(fr, p["q3"], W / 2, 615, 104, YEL, BLACK, s=0.85 + 0.15 * pop(x - 0.08, 0.25), glow=(TEAL, 16, 1.1), maxw=960)
    by = 960 - 8 * abs(math.sin(t * 3))
    for j in range(4):
        ph = ((x * 0.7 + j / 4) % 1.0)
        put(fr, ballot_paper(100), W / 2 - 40 + j * 26, lerp(760, 860, ease_io(ph)), 1.0, appear(x - j * 0.2, 0.1) * (1 - ph ** 3),
            (j - 1.5) * 8)
    put(fr, ballot_box(380), W / 2, by, 1.0, 1.0, 2 * math.sin(t * 2))
    put(fr, pill(p["sales"], 40, INK, YEL), W / 2, 1115, pop(x - 0.6, 0.3))
    n = sc.lcues.get("no")
    if n is not None and t > n:
        k = t - n
        put(fr, stamp(p["stamp"], 96, RED), W / 2, 960, slam(k, 2.4, 0.22), appear(k, 0.05), -10)


SFX["ballot_hook"] = lambda sc: [(sc.t0 + 0.5, "thump")] + ([(sc.lcues["no"], "boom")] if "no" in sc.lcues else [])


def certs(fr, t, sc):
    """Certificados que entran uno por uno (cues c1, c2, c3...); el marcado 'hot' entra con golpe; pie en 'foot'."""
    p = sc.p
    kick(fr, p["kicker"])
    cards = p["cards"]                       # [(titulo, votos, color, escala), ...]
    n = len(cards)
    xs = {1: [540], 2: [300, 780], 3: [210, 540, 870]}[n]
    for i, (title, votes, col, sz) in enumerate(cards):
        c = lc(sc, "c%d" % (i + 1), sc.t0 + 0.2 + 0.35 * i)
        if t < c:
            continue
        k = t - c
        hot = i in p.get("hot", [])
        w = (310 if n == 3 else 440) * sz
        sc_ = slam(k, 1.8, 0.24) if hot else pop(k, 0.34)
        bob = 10 * math.sin(t * 2.2 + i)
        if hot and k > 0.3:
            put(fr, fx.panel(w + 30, w * 0.66 + 30, (0, 0, 0, 0), YEL, 26, 6), xs[i], 800 + bob, sc_, 0.5 + 0.5 * math.sin(t * 6) ** 2)
        put(fr, cert(w, title, votes, col, p.get("sub", "SHARE CERTIFICATE")), xs[i], 800 + bob, sc_, 1.0, (-4, 3, -2)[i % 3])
        if p.get("caps"):
            say(fr, p["caps"][i], xs[i], 800 + w * 0.33 + 60, 34, KICK, HEAVY, a=appear(k - 0.15, 0.25), maxw=440)
    f = sc.lcues.get("foot")
    if f is not None and t > f:
        put(fr, pill(p["foot"], 42, INK, YEL), W / 2, 1150, pop(t - f, 0.32))


SFX["certs"] = lambda sc: ([(sc.lcues["c%d" % (i + 1)], "boom" if i in sc.p.get("hot", []) else "pop")
                            for i in range(len(sc.p["cards"])) if "c%d" % (i + 1) in sc.lcues] +
                           ([(sc.lcues["foot"], "ding")] if "foot" in sc.lcues else []))


# ============ Walmart (013): ticket, cereal, telefono con patrocinado, pantalla de tienda ============
def receipt(w, rows, head="RECEIPT"):
    """Ticket de compra generico (sin nombre de tienda). rows: [(izq, der, hot)]. Devuelve sprite."""
    key = ("receipt", int(w), tuple(rows), head)
    if key in fx._scache:
        return fx._scache[key]
    h = w * (0.42 + 0.17 * len(rows))
    S = 2
    im, d = fx._new(w, h, S)
    W_, H_ = w * S, h * S
    z = W_ / 16
    pts = [(0, 0), (W_, 0), (W_, H_ - z)]
    for i in range(16, -1, -1):
        pts.append((i * z, H_ - (z if i % 2 == 0 else 0)))
    d.polygon(pts, fill=(250, 248, 240, 255))
    ink = (40, 36, 52, 255)
    d.text((W_ / 2, H_ * 0.09), head, font=font(BLACK, int(W_ * 0.085)), fill=ink, anchor="mm")
    for k in range(18):
        x = W_ * 0.08 + k * W_ * 0.047
        d.rectangle([x, H_ * 0.17, x + W_ * 0.025, H_ * 0.17 + S * 3], fill=(150, 145, 160, 255))
    y = H_ * 0.17 + W_ * 0.12
    step = W_ * 0.17
    for left, right, hot in rows:
        if hot:
            d.rounded_rectangle([W_ * 0.04, y - step * 0.42, W_ * 0.96, y + step * 0.42], 10 * S, fill=(255, 210, 63, 255))
        f = font(BLACK if hot else HEAVY, int(W_ * (0.085 if hot else 0.072)))
        d.text((W_ * 0.08, y), left, font=f, fill=ink, anchor="lm")
        d.text((W_ * 0.92, y), right, font=f, fill=ink, anchor="rm")
        y += step
    return fx._done(key, im, w, h)


def cereal_box(w, label="CEREAL"):
    """Caja de cereal generica: frente naranja, tazon, costado oscuro."""
    key = ("cereal", int(w), label)
    if key in fx._scache:
        return fx._scache[key]
    h = w * 1.35
    im, d = fx._new(w, h)
    S = SS
    W_, H_ = w * S, h * S
    fw = W_ * 0.80
    d.polygon([(fw, H_ * 0.06), (W_, 0), (W_, H_ * 0.94), (fw, H_)], fill=(170, 70, 30, 255))
    d.polygon([(0, H_ * 0.06), (W_ * 0.20, 0), (W_, 0), (fw, H_ * 0.06)], fill=(255, 190, 110, 255))
    d.rectangle([0, H_ * 0.06, fw, H_], fill=(240, 110, 40, 255))
    d.rectangle([fw * 0.06, H_ * 0.10, fw * 0.94, H_ * 0.30], fill=(255, 240, 210, 255))
    f = font(BLACK, int(fw * 0.20))
    while f.getlength(label) > fw * 0.80:
        f = font(BLACK, int(f.size * 0.94))
    d.text((fw / 2, H_ * 0.20), label, font=f, fill=(170, 50, 20, 255), anchor="mm")
    cx, cy = fw / 2, H_ * 0.66
    d.ellipse([cx - fw * 0.34, cy - fw * 0.14, cx + fw * 0.34, cy + fw * 0.10], fill=(255, 225, 120, 255))
    rng = np.random.default_rng(2)
    for _ in range(14):
        px, py = cx + rng.uniform(-0.28, 0.28) * fw, cy + rng.uniform(-0.11, 0.02) * fw
        r = fw * 0.04
        d.ellipse([px - r, py - r, px + r, py + r], fill=(210, 120, 40, 255))
    d.chord([cx - fw * 0.38, cy - fw * 0.30, cx + fw * 0.38, cy + fw * 0.34], 0, 180, fill=(250, 250, 255, 255))
    d.rectangle([fw * 0.06, H_ * 0.86, fw * 0.40, H_ * 0.92], fill=(255, 240, 210, 255))
    return fx._done(key, im, w, h)


def phone(w, query, tag):
    """Telefono con resultados de busqueda; el primer resultado lleva la etiqueta de patrocinado."""
    key = ("phone", int(w), query, tag)
    if key in fx._scache:
        return fx._scache[key]
    h = w * 2.0
    S = 2
    im, d = fx._new(w, h, S)
    W_, H_ = w * S, h * S
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], W_ * 0.14, fill=(24, 22, 38, 255))
    m = W_ * 0.05
    d.rounded_rectangle([m, m, W_ - m, H_ - m], W_ * 0.11, fill=(244, 244, 250, 255))
    d.rounded_rectangle([W_ * 0.36, m + W_ * 0.03, W_ * 0.64, m + W_ * 0.08], W_ * 0.03, fill=(24, 22, 38, 255))
    sy = H_ * 0.10
    d.rounded_rectangle([W_ * 0.10, sy, W_ * 0.90, sy + W_ * 0.14], W_ * 0.07, fill=(225, 226, 238, 255))
    d.ellipse([W_ * 0.15, sy + W_ * 0.035, W_ * 0.22, sy + W_ * 0.105], outline=(110, 110, 130, 255), width=int(4 * S))
    d.text((W_ * 0.27, sy + W_ * 0.07), query, font=font(HEAVY, int(W_ * 0.075)), fill=(60, 60, 80, 255), anchor="lm")
    cards = [((255, 150, 60), True), ((120, 190, 255), False), ((160, 220, 140), False)]
    y = H_ * 0.22
    ch = H_ * 0.22
    for col, hot in cards:
        d.rounded_rectangle([W_ * 0.10, y, W_ * 0.90, y + ch], W_ * 0.05, fill=(255, 255, 255, 255),
                            outline=(255, 210, 63, 255) if hot else (215, 215, 228, 255), width=int((6 if hot else 2) * S))
        d.rounded_rectangle([W_ * 0.15, y + ch * 0.12, W_ * 0.42, y + ch * 0.88], W_ * 0.03, fill=col + (255,))
        for k, ww in enumerate((0.38, 0.30, 0.20)):
            yy = y + ch * (0.22 + k * 0.22)
            d.rounded_rectangle([W_ * 0.48, yy, W_ * (0.48 + ww), yy + ch * 0.09], ch * 0.04, fill=(200, 200, 215, 255))
        if hot:
            f = font(BLACK, int(W_ * 0.062))
            while f.getlength(tag) + W_ * 0.06 > W_ * 0.40:
                f = font(BLACK, int(f.size * 0.94))
            tw = f.getlength(tag) + W_ * 0.06
            x0, y0 = W_ * 0.47, y + ch * 0.66
            d.rounded_rectangle([x0, y0, x0 + tw, y0 + W_ * 0.10], W_ * 0.05, fill=(255, 210, 63, 255))
            d.text((x0 + tw / 2, y0 + W_ * 0.05), tag, font=f, fill=(24, 16, 44, 255), anchor="mm")
        y += ch + H_ * 0.03
    return fx._done(key, im, w, h)


def store_screen(w, txt):
    """Pantalla de tienda en un poste, con un anuncio generico (caja de cereal + texto)."""
    key = ("screen", int(w), txt)
    if key in fx._scache:
        return fx._scache[key]
    h = w * 0.86
    im, d = fx._new(w, h, 2)
    S = 2
    W_, H_ = w * S, h * S
    sh = H_ * 0.66
    d.rectangle([W_ * 0.46, sh, W_ * 0.54, H_], fill=(90, 96, 120, 255))
    d.rounded_rectangle([0, 0, W_ - 1, sh], W_ * 0.04, fill=(26, 26, 40, 255))
    d.rounded_rectangle([W_ * 0.04, W_ * 0.04, W_ * 0.96, sh - W_ * 0.04], W_ * 0.02, fill=(40, 120, 200, 255))
    cb = cereal_box(int(w * 0.22))
    im.alpha_composite(cb.resize((int(cb.width * S), int(cb.height * S))), (int(W_ * 0.10), int(sh * 0.14)))
    f = font(BLACK, int(W_ * 0.11))
    while f.getlength(txt) > W_ * 0.50:
        f = font(BLACK, int(f.size * 0.94))
    d.text((W_ * 0.66, sh * 0.50), txt, font=f, fill=(255, 210, 63, 255), anchor="mm")
    return fx._done(key, im, w, h)


def receipt_hook(fr, t, sc):
    """Pregunta completa desde el cuadro 1; el ticket se imprime y resalta lo que se queda la tienda; sello en 'ads'."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    say(fr, p["q1"], W / 2, 395, 62, WHITE, BLACK, maxw=940)
    say(fr, p["q2"], W / 2, 505, 132, YEL, BLACK, s=0.85 + 0.15 * pop(x, 0.25), glow=(GRN, 18, 1.2), maxw=960)
    say(fr, p["q3"], W / 2, 625, 80, WHITE, BLACK, s=0.85 + 0.15 * pop(x - 0.08, 0.25), maxw=960)
    spr = receipt(340, p["rows"], p.get("head", "RECEIPT"))
    top = 700
    g = clamp(0.35 + 0.65 * ease_out(x / 0.8))
    hh = max(4, int(spr.height * g))
    put(fr, spr.crop((0, 0, spr.width, hh)), W / 2, top + hh / 2, 1.0, 1.0)
    put(fr, panel(380, 26, (60, 60, 80, 255), None, 13), W / 2, top - 6)
    if g > 0.98:      # la fila resaltada late
        hot = [i for i, r in enumerate(p["rows"]) if r[2]]
        if hot:
            yy = top + spr.height * 0.17 + 340 * 0.12 + hot[0] * 340 * 0.17
            put(fr, panel(370, 70, (0, 0, 0, 0), YEL, 16, 5), W / 2, yy, 1.0, 0.4 + 0.6 * math.sin(t * 7) ** 2)
    n = sc.lcues.get("ads")
    if n is not None and t > n:
        k = t - n
        put(fr, stamp(p["stamp"], 74, RED), W / 2 + 120, 790, slam(k, 2.4, 0.22), appear(k, 0.05), -10)


SFX["receipt_hook"] = lambda sc: [(sc.t0 + 0.1, "whoosh")] + ([(sc.lcues["ads"], "boom")] if "ads" in sc.lcues else [])


def dollar_split(fr, t, sc):
    """Ventas y ganancia del año; luego un dolar partido: casi todo se va, la tienda se queda una rebanada."""
    p = sc.p
    kick(fr, p["kicker"])
    for cue, txt, lab, y, col in (("s", p["sales"], p["sales_l"], 430, WHITE), ("p", p["profit"], p["profit_l"], 640, YEL)):
        c = sc.lcues.get(cue)
        if c is None or t < c:
            continue
        k = t - c
        say(fr, txt, W / 2, y, 128, col, BLACK, a=appear(k, 0.06), s=slam(k, 1.6, 0.22),
            glow=(GRN, 16, 1.1) if col == YEL else None, maxw=920)
        say(fr, lab, W / 2, y + 88, 38, KICK, HEAVY, a=appear(k - 0.1, 0.2), maxw=900)
    c = sc.lcues.get("cut")
    if c is None:
        return
    if t > c - 0.5:
        k = t - c + 0.5
        L = X1 - X0
        y = 960
        v = appear(k, 0.25)
        say(fr, p["bar_l"], W / 2, y - 96, 40, WHITE, HEAVY, a=v)
        cut = ease_out((t - c) / 0.45) if t > c else 0.0
        keep = L * 0.03 * cut
        gap = 10 * cut
        body = L - keep - gap
        put(fr, bar(body, 110, (60, 150, 120), (30, 100, 80), r=20), X0 + body / 2, y, 1.0, v)
        say(fr, p["rest"], X0 + body / 2, y, 52, WHITE, BLACK, a=v)
        if cut > 0.02:
            put(fr, bar(max(8, keep + 18), 130, YEL, ORANGE, r=8, glow=(YEL, 18)), X1 - keep / 2 - 4, y - 12 * (1 - cut), 1.0, 1.0)
            kk = t - c
            put(fr, pill(p["keep"], 48, INK, YEL, 30, 16, BLACK), W / 2, y + 150, slam(kk - 0.15, 1.8, 0.22), appear(kk - 0.15, 0.05))
            put(fr, pill(p["tag"], 30, INK, TEAL), W / 2, y + 245, pop(kk - 0.5, 0.3))


SFX["dollar_split"] = lambda sc: ([(sc.lcues[c], "pop") for c in ("s", "p") if c in sc.lcues] +
                                  ([(sc.lcues["cut"], "boom")] if "cut" in sc.lcues else []))


def cereal_buy(fr, t, sc):
    """Caja de cereal con etiqueta de $1; en 'buy' el dinero sale hacia el proveedor."""
    p = sc.p
    x = t - sc.t0
    kick(fr, p["kicker"])
    put(fr, cereal_box(320, p.get("label", "CEREAL")), 330, 790 + 8 * math.sin(t * 2.4), pop(x, 0.34), 1.0, -4)
    k = x - 0.35
    if k > 0:
        sw = 22 * math.exp(-3.0 * k) * math.cos(10 * k)
        xin = lerp(1300, 790, ease_out(k / 0.35))
        line(fr.d, [(xin - 100, 560), (xin - 120, 700)], fill=(230, 220, 255), width=4)
        oval(fr.d, [xin - 110, 550, xin - 90, 570], fill=(230, 220, 255))
        put(fr, price_tag(340, p["price"], p["price_sub"]), xin, 710, 1.0, 1.0, sw)
    b = sc.lcues.get("buy")
    if b is not None and t > b:
        kb = t - b
        rng = np.random.default_rng(4)
        for i in range(10):
            d0 = rng.uniform(0, 0.8)
            kk = kb - d0
            if kk <= 0 or kk > 1.4:
                continue
            bx = lerp(700, -160, ease_io(kk / 1.2)) + rng.uniform(-40, 40)
            by = 960 + rng.uniform(-60, 60) - 120 * math.sin(math.pi * clamp(kk / 1.2))
            put(fr, bill(150, rng.uniform(-30, 30) + 200 * kk), bx, by, 1.0, clamp(1.6 - kk))
        put(fr, pill(p["pay"], 44, WHITE, RED, 30, 18, BLACK), W / 2, 1150, slam(kb, 1.8, 0.22), appear(kb, 0.05))


SFX["cereal_buy"] = lambda sc: [(sc.t0 + 0.4, "pop")] + ([(sc.lcues["buy"], "cash")] if "buy" in sc.lcues else [])


def ad_spots(fr, t, sc):
    """Telefono con un resultado patrocinado ('app'), pantalla de tienda ('scr'), las marcas pagan ('pay')."""
    p = sc.p
    kick(fr, p["kicker"])
    a = sc.lcues.get("app", sc.t0)
    if t > a:
        k = t - a
        ph = phone(330, p["query"], p["tag"])
        put(fr, ph, 300, 820 + 6 * math.sin(t * 2), pop(k, 0.34), 1.0, -3)
        if k > 0.5:
            put(fr, panel(290, 160, (0, 0, 0, 0), YEL, 22, 6), 300, 708 + 6 * math.sin(t * 2),
                1.0, 0.35 + 0.65 * math.sin(t * 6) ** 2, -3)
        say(fr, p["l_app"], 300, 1200, 34, WHITE, HEAVY, a=appear(k - 0.2, 0.25), maxw=420)
    s = sc.lcues.get("scr")
    if s is not None and t > s:
        k = t - s
        xin = lerp(1300, 790, ease_out(k / 0.4))
        put(fr, store_screen(380, p["screen"]), xin, 700 + 6 * math.sin(t * 2.6 + 1), 1.0, 1.0)
        say(fr, p["l_scr"], 790, 900, 34, WHITE, HEAVY, a=appear(k - 0.3, 0.25), maxw=400)
    py = sc.lcues.get("pay")
    if py is not None and t > py:
        k = t - py
        rng = np.random.default_rng(6)
        for i in range(8):
            kk = k - i * 0.09
            if kk <= 0 or kk > 1.0:
                continue
            bx = lerp(1180, 790, ease_out(kk / 0.6)) + rng.uniform(-60, 60)
            by = lerp(1250, 1060, ease_out(kk / 0.6)) + rng.uniform(-30, 30)
            put(fr, bill(120, rng.uniform(-30, 30)), bx, by, 1.0, clamp(1.4 - kk * 1.2))
        put(fr, pill(p["pay"], 40, INK, YEL, 28, 16, BLACK), 790, 1060, slam(k, 1.8, 0.22), appear(k, 0.05), -3)


SFX["ad_spots"] = lambda sc: [(sc.lcues[c], s) for c, s in (("app", "pop"), ("scr", "pop"), ("pay", "cash")) if c in sc.lcues]

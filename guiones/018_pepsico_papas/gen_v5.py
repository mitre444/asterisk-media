"""Genera es.py y en.py del 018 v5 (2D plano con IA) con el mismo guion visual."""
import json, sys
G = "/home/claude/asterisk-media/guiones/018_pepsico_papas"
I = G + "/img/"
LOGO = "/home/claude/asterisk-media/logos/pepsi.png"
RED, BLUE = (229, 9, 20), (0, 70, 160)

T = dict(
 es=dict(
  h0=["ERES EL DUEÑO", "DE *PEPSI*…"], h0b=["Y VIVES DE LAS", "[PAPAS.]"], tag0=("BOTANAS", "SABRITAS · DORITOS · CHEETOS"),
  h1=["DE CADA $100,", "¿QUIÉN VENDE *MÁS*?"], h1b=["*58* DE BOTANAS.", "[42 DE BEBIDAS.]"], st1="GANAN LAS PAPAS",
  h2=["¿QUÉ EMPRESA", "ESCONDE SU", "*ASTERISCO*?"], bub2="Comenta una empresa ↓", who="TÚ",
  ch3="01 · DONDE NACIÓ", h3=["Y AHORA", "VIENE LO *RARO*."], h3b=["EN NORTEAMÉRICA:", "[CASI EMPATE.]"],
  ch4="02 · FUERA DE AHÍ", h4=["FUERA DE AHÍ:", "[69 DE CADA 100]", "SON BOTANAS."], h4b=["MÉXICO, DE SUS", "[MÁS GRANDES.]"],
  tag4=("$6,947 M", "VENTAS EN MÉXICO · 2025"),
  ch5="LA RESPUESTA", h5=["UNA EMPRESA DE *PAPAS*", "[QUE VENDE REFRESCO.]"], h5b=["¿QUÉ COMPRAS MÁS:", "*REFRESCO* O PAPAS?"],
  lect="NUESTRA LECTURA", bub5="Sé honesto ↓", fol="+ SEGUIR · #5 MAÑANA",
 ),
 en=dict(
  h0=["YOU'RE THE", "CEO OF *PEPSI*…"], h0b=["AND YOU RUN", "ON [CHIPS.]"], tag0=("CHIPS", "LAY'S · DORITOS · CHEETOS"),
  h1=["OF EVERY $100,", "WHO SELLS *MORE*?"], h1b=["*58* FROM SNACKS.", "[42 FROM DRINKS.]"], st1="CHIPS WIN",
  h2=["WHICH COMPANY", "IS HIDING ITS", "*ASTERISK*?"], bub2="Comment a company ↓", who="YOU",
  ch3="01 · BACK HOME", h3=["NOW HERE'S", "THE *WEIRD* PART."], h3b=["IN NORTH AMERICA:", "[ALMOST A TIE.]"],
  ch4="02 · EVERYWHERE ELSE", h4=["EVERYWHERE ELSE:", "[69 OF EVERY 100]", "ARE SNACKS."], h4b=["MEXICO ALONE:", "[$6.9 BILLION.]"],
  tag4=("$6,947 M", "MEXICO SALES · 2025"),
  ch5="THE ANSWER", h5=["A *CHIP* COMPANY", "[THAT SELLS SODA.]"], h5b=["WHAT DO YOU BUY", "MORE: *SODA* OR CHIPS?"],
  lect="OUR READ", bub5="Be honest ↓", fol="+ FOLLOW · #5 TOMORROW",
 ))

def beats(L, lines):
    t = T[L]
    BOT = 1470          # titular abajo en las escenas de los dos puestos (arriba están los letreros)
    return [
     dict(scene="v4", p=dict(
        bg=[dict(src=I+"s1_dueno.jpg", z=(1.0, 1.10), c0=(0.55, 0.50), c1=(0.60, 0.55), shade=(1.35, 1.0)),
            dict(src=I+"s2_boveda.jpg", cue="q", z=(1.22, 1.32), c0=(0.50, 0.62), c1=(0.50, 0.66), shade=(1.25, 1.0))],
        heads=[dict(lines=t["h0"]), dict(cue="q", lines=t["h0b"])],
        props=[dict(kind="logo", src=LOGO, x=802, y=1056, w=250, h=250, pin=True, out="q", still=True),
               dict(kind="tag", x=540, y=1720, big=t["tag0"][0], small=t["tag0"][1], cue="q", delay=0.25, s=1.0)]),
        lines=lines[0]),
     dict(scene="v4", p=dict(
        bg=[dict(src=I+"s3_puestos.jpg", z=(1.0, 1.04), c0=(0.5, 0.26), shade=(0.45, 2.2))],
        heads=[dict(lines=t["h1"], top=BOT), dict(cue="rev", lines=t["h1b"], top=BOT)],
        props=[dict(kind="logo", src=LOGO, x=269, y=624, w=150, h=150, pin=True, still=True),
               dict(kind="counter", x=264, y=494, to=42, pre="$", count=1.6, cue="sim", col=BLUE, size=96, pin=True),
               dict(kind="counter", x=811, y=494, to=58, pre="$", count=1.6, cue="sim", col=RED, size=96, pin=True),
               ]),
        lines=lines[1]),
     dict(scene="v4", p=dict(
        bg=[dict(src=I+"s1_dueno.jpg", z=(1.30, 1.38), c0=(0.40, 0.52), shade=(1.35, 1.0))],
        heads=[dict(lines=t["h2"])],
        props=[dict(kind="bubble", x=560, y=1560, txt=t["bub2"], who=t["who"], delay=0.3)]),
        lines=lines[2]),
     dict(scene="v4", p=dict(chapter=t["ch3"],
        bg=[dict(src=I+"s4_empate.jpg", z=(1.0, 1.04), c0=(0.5, 0.24), shade=(0.45, 2.2))],
        heads=[dict(cue="raro", lines=t["h3"], top=BOT), dict(cue="na", lines=t["h3b"], top=BOT)],
        props=[dict(kind="logo", src=LOGO, x=274, y=592, w=130, h=130, pin=True, still=True),
               dict(kind="counter", x=288, y=458, to=51, suf="%", count=1.0, cue="na", col=BLUE, size=96, pin=True),
               dict(kind="counter", x=792, y=458, to=49, suf="%", count=1.0, cue="na", col=RED, size=96, pin=True)]),
        lines=lines[3]),
     dict(scene="v4", p=dict(chapter=t["ch4"],
        bg=[dict(src=I+"s5_mexico.jpg", z=(1.0, 1.10), c0=(0.5, 0.45), c1=(0.55, 0.50), shade=(1.5, 1.0))],
        heads=[dict(cue="int", lines=t["h4"]), dict(cue="mx", lines=t["h4b"])],
        props=[dict(kind="tag", x=330, y=960, big=t["tag4"][0], small=t["tag4"][1], cue="mx", delay=0.3, s=1.05)]),
        lines=lines[4]),
     dict(scene="v4", p=dict(chapter=t["ch5"],
        bg=[dict(src=I+"s6_abrazo.jpg", z=(1.0, 1.10), c0=(0.5, 0.55), c1=(0.52, 0.60), shade=(1.4, 1.2))],
        heads=[dict(cue="ans", lines=t["h5"]), dict(cue="ask", lines=t["h5b"])],
        props=[dict(kind="tag", x=540, y=790, big=t["lect"], small="", cue="ans", delay=0.3, s=0.75, out="ask"),
               dict(kind="bubble", x=600, y=1640, txt=t["bub5"], who=t["who"], cue="ask", delay=0.3),
               dict(kind="badge", x=540, y=1810, txt=t["fol"], col=RED, cue="fol")]),
        lines=lines[5]),
    ]

for L in ("es", "en"):
    path = f"{G}/{L}.py"
    src = open(path).read()
    ns = {}
    exec(compile(src, path, "exec"), ns)
    S = ns["SPEC"]
    lines = [b["lines"] for b in S["beats"]]
    S["beats"] = beats(L, lines)
    S["v4"]["style"] = "v5-2d-ia"
    head = src.split("SPEC = dict(")[0]
    head = head.replace('"""018', '"""018 v5 (2D plano con imágenes de IA, referencia finance.arc01)\n018', 1)
    import pprint
    body = "SPEC = " + pprint.pformat(S, width=120, sort_dicts=False) + "\n"
    open(path, "w").write(head + body)
    print("ok", L)

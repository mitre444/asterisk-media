"""001 · El hot dog de $1.50 de Costco — español (Con Asterisco). Adaptación, no traducción."""
YEL = (255, 210, 63)
BASE = dict(kicker="COSTCO EE. UU. · HOT DOG + REFRESCO", price="$1.50", y0=1985, y1=2026)

SPEC = dict(
    id="001_costco_hotdog", lang="es-419", lang_tag="ES", voice="em_alex", speed=1.0,
    brand="CON ASTERISCO",
    lexicon={"hot": "jot", "Craig": "Creig", "Jelinek": "Yélinek", "Jim": "Yim", "Sinegal": "Sínegal", "Illinois": "Ilinóis"},
    sfx=[("ast", "ding", 0.0), ("rev", "thump", 0.0), ("rev", "ding", 0.06)],
    beats=[
        dict(scene="hook", src="Costco: mismo precio desde 1985", p=dict(BASE, rewind_dur=2.2), lines=[
            "En Estados Unidos, el hot dog con refresco de Costco cuesta {un dólar cincuenta.|$1.50.}",
            "[#rewind] Lo mismo que en {mil novecientos ochenta y cinco.|1985.}",
            "Y la razón casi no tiene [#ast] nada que ver con los hot dogs.",
        ]),
        dict(scene="bars", src="BLS, IPC-U: promedio de 1985 vs. sept. de 2026",
             p=dict(kicker="SI HUBIERA SEGUIDO A LA INFLACIÓN", v1=1.50, v2=4.70, fmt="${:.2f}", l1="PRECIO REAL",
                    l2="CON INFLACIÓN", badge="3.1×", grow_dur=1.3),
             lines=["Si hubiera subido con la inflación, [#grow] hoy costaría unos {cuatro dólares con setenta.|$4.70.}"]),
        dict(scene="people", src="C. Jelinek en 425 Business (2018) · traducción propia",
             p=dict(kicker="DENTRO DE COSTCO", n1="CRAIG JELINEK", r1="Directivo · después director general", i1="CJ",
                    n2="JIM SINEGAL", r2="Cofundador", i2="JS",
                    bubble=["«No podemos vender este", "hot dog a un dólar cincuenta»"]),
             lines=[
                 "Un directivo [#say] quiso subirlo.",
                 "[#pre] Craig Jelinek, que después fue director general, cuenta que le dijo al [#p2] cofundador, Jim Sinegal, que estaban perdiendo dinero.",
             ]),
        dict(scene="quote", src="425 Business (2018) · traducción propia",
             p=dict(kicker="SU RESPUESTA", breaks=[3, 2, 2, 2, 1], hot=1,
                    attr1="— JIM SINEGAL, cofundador", attr2="según lo contó Craig Jelinek"),
             lines=[
                 dict(text="Y Sinegal, según Jelinek, le contestó:", pause=0.22),
                 dict(text="{Si|«Si} le subes al maldito hot dog, te mato. {Resuélvelo.|Resuélvelo».}", cap=False, role="quote"),
             ]),
        dict(scene="flow", src="C. Jelinek en 425 Business (2018)",
             p=dict(kicker="LA SOLUCIÓN", a="PROVEEDORES EXTERNOS", b="PLANTAS PROPIAS DE COSTCO", c1="CALIFORNIA", c2="ILLINOIS"),
             lines=[
                 "Y lo resolvieron.",
                 "Costco [#stop] dejó de comprar las salchichas y [#own] empezó a fabricarlas: primero en [#c1] California y luego en [#c2] Illinois.",
             ]),
        dict(scene="counter", src="Asamblea anual de Costco, 15 de enero de 2026",
             p=dict(kicker="AÑO FISCAL 2025", value=245.1, fmt="{:.1f} M", sub="COMBOS DE HOT DOG + REFRESCO VENDIDOS",
                    legend="1 ícono ≈ 10 millones", dur=1.5),
             lines=["En su año fiscal {dos mil veinticinco|2025} vendió [#count] {doscientos cuarenta y cinco|245} millones de combos."]),
        dict(scene="reveal", src="Costco, llamada de resultados del 4T fiscal 2026 · traducción propia",
             p=dict(title="EL ASTERISCO", qlines=["«Nuestra membresía", "sigue siendo", "el artículo más importante", "que vendemos»"],
                    hot=[2, 3], attr1="— RON VACHRIS, director general de Costco", attr2="Llamada de resultados · 24 de sept. de 2026"),
             lines=[
                 "[#rev] Pero aquí va el asterisco.",
                 "[#quote] En septiembre de {dos mil veintiséis,|2026,} el director general de Costco dijo que la membresía es el artículo más importante que venden.",
             ]),
        dict(scene="statement", src="Resultados de Costco, año fiscal 2026 (24 de sept. de 2026)",
             p=dict(kicker="COSTCO · AÑO FISCAL 2026", doc="DEL ESTADO DE RESULTADOS · MILLONES DE DÓLARES (MDD)", r1="Cuotas de membresía",
                    v1="5,907 mdd", r2="Utilidad neta", v2="9,226 mdd", lw=420, ratio="Cuotas comparadas con la utilidad total",
                    pct=64, pfmt="{:.0f}%"),
             lines=[
                 "Ese año, [#fees] las cuotas de membresía le dejaron [#v1] {cinco mil novecientos|5,900} millones de dólares.",
                 "[#profit] Eso equivale al [#pct] {sesenta y cuatro por ciento|64%} de toda la ganancia de Costco.",
             ]),
        dict(scene="ring_scene", src="Costco, llamada de resultados del 4T fiscal 2026",
             p=dict(kicker="RENOVACIÓN DE MEMBRESÍAS", pct=92.3, pfmt="{:.1f}%", l1="TASA DE RENOVACIÓN · EE. UU. Y CANADÁ",
                    l2="En todo el mundo: 89.8%"),
             lines=["Y [#go] nueve de cada diez socios renuevan."]),
        dict(scene="close", src="Sigue la cuenta para ver el próximo asterisco", src_color=YEL,
             p=dict(BASE, kicker="CÓMO FUNCIONA", kicker0=BASE["kicker"], s1="HOT DOG DE $1.50", s2="UNA RAZÓN PARA ENTRAR",
                    s3="UNA MEMBRESÍA RENOVADA"),
             lines=[
                 "[#s1] Así que el hot dog no tiene que dejar mucho dinero.",
                 "Tiene que [#s2] recordarte por qué [#s3] pagas por entrar.",
                 "[#back] Y por eso sigue costando {un dólar cincuenta.|$1.50.}",
             ]),
    ],
    post=dict(
        tiktok=("El hot dog de Costco cuesta lo mismo desde 1985: un dólar cincuenta. El asterisco: nunca se trató del hot dog. "
                "(En México el combo ronda los 30 pesos.)\n\n"
                "Fuentes: resultados de Costco del año fiscal 2026 (24 sept 2026) · llamada de resultados del 4T fiscal 2026 · "
                "presentación de la asamblea anual 2026 de Costco · BLS, IPC-U (promedio de 1985 vs. sept 2026) · "
                "Craig Jelinek en 425 Business (2018) · Expansión (1 sept 2026). Citas traducidas del inglés.\n\n"
                "#costco #negocios #dinero #economia #finanzas"),
        title="Por qué el hot dog de Costco sigue costando $1.50",
    ),
)

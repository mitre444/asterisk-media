"""011 · ¿Lo de Jensen Huang le podría pasar a Zuckerberg? — español (Con Asterisco). Adaptación, no traducción.
Patrones (doc 03): P8 dos cifras que chocan, P3, P4 noticia de la semana, P7. Regla de tono: solo lo que dicen el comunicado y el consejo."""
TEAL, YEL = (70, 230, 225), (255, 210, 63)
SRC_8K = "Comunicado de Nvidia (8-K), 12 nov. 2026"
SRC_CALL = "Presidente del consejo de Nvidia en la llamada del 17 nov., vía NPR"
SRC_Q3 = "Resultados Q3 FY2027 de Nvidia (8-K), 17 nov. 2026"
SRC_META = "Informe a accionistas de Meta (DEF 14A), abr. 2026"
SPEC = dict(
    id="011_nvidia_ceo", lang="es-419", lang_tag="ES", voice="em_alex", speed=1.08,
    brand="CON ASTERISCO", theme="board", hook_timer=True,
    lexicon={"like": "laik", "Nasdaq": "Násdak", "Zuckerberg": "Zókerberg", "Jensen": "Yénsen", "Huang": "Juáng"},
    camera=dict(push=0.04, enter=0.10, punch=["no", "stamp", "grow", "last", "c1", "c2", "c3", "foot", "count", "chips", "rev", "quote", "ans", "fol", "like"],
                shake=["no", "stamp", "cut", "c2", "ans"]),
    music=dict(bpm=92, cut="cut", riser_scenes=["reveal2"], gain=0.20, duck=0.55),
    sfx=[],
    beats=[
        dict(scene="ballot_hook", src=SRC_8K + " · " + SRC_CALL,
             p=dict(kicker="NVIDIA · 17 NOV.", q1="A SU CEO, NVIDIA LE DIJO QUE NO.", q2="¿POR QUÉ NADIE LE DICE", q3="QUE NO A ZUCKERBERG?",
                    sales="EL CONSEJO DE NVIDIA: NO", stamp="NO"),
             lines=["El consejo de Nvidia acaba de decirle [#no] que no a su propio director general.",
                    "¿Por qué nadie le puede decir que no a Mark Zuckerberg?"]),
        dict(scene="classified", src=SRC_8K,
             p=dict(kicker="12 NOV. 2026", doc="CAMBIO DE DIRECTOR GENERAL", stamp="RENUNCIÓ", mystery="EFECTO INMEDIATO",
                    quote="DIRECTOR GENERAL Y CONSEJERO", attr="TRAS REVELAR UNA CONDUCTA PERSONAL CONTRARIA AL CÓDIGO"),
             lines=["El {doce de noviembre,|12 de noviembre,} Jensen Huang [#stamp] renunció como director general de Nvidia y dejó el consejo, con efecto inmediato.",
                    "[#sub] La empresa dice que fue tras revelar una conducta personal contraria a su código."]),
        dict(scene="bars2", src=SRC_Q3 + " · cálculo propio",
             p=dict(kicker="NVIDIA · ÚLTIMO TRIMESTRE", v1=65.3, v2=115.8, fmt="${:.1f} MMD", labels=["UTILIDAD", "VENTAS"],
                    labels2=["UTILIDAD NETA", "3 MESES"], badge="≈ $8,300 POR SEGUNDO"),
             lines=["[#grow] Cinco días después: {ciento quince mil ochocientos millones de dólares|$115,800 millones} en ventas.",
                    "[#last] {Sesenta y cinco mil trescientos millones|$65,300 millones} de utilidad.",
                    "Unos {ocho mil trescientos dólares|$8,300 dólares} por segundo."]),
        dict(scene="interrupt", src="",
             p=dict(lines=["ÉL QUERÍA", "REGRESAR."], hot=[1], ys=[700, 860]),
             lines=[dict(text="[#cut] Huang dijo que sería un honor volver.", pause=0.45)]),
        dict(scene="classified", src=SRC_CALL,
             p=dict(kicker="LA RESPUESTA DEL CONSEJO", doc="POSTURA DEL CONSEJO", stamp="NO VUELVE", mystery="UNÁNIME",
                    quote="“NO TIENE INTENCIÓN DE REINSTALARLO”", attr="PRESIDENTE DEL CONSEJO DE NVIDIA, 17 NOV. 2026"),
             lines=["[#stamp] La respuesta del consejo:",
                    "[#sub] no tiene intención de reinstalar a Jensen como director general."]),
        dict(scene="certs", src="Portada del 8-K y reportes a accionistas de Nvidia",
             p=dict(kicker="NVIDIA · SIGUE LOS VOTOS", sub="NVDA · ACCIÓN COMÚN",
                    cards=[("1 ACCIÓN", "1 VOTO", TEAL, 1.0), ("1 ACCIÓN", "1 VOTO", TEAL, 1.0), ("1 ACCIÓN", "1 VOTO", TEAL, 1.0)],
                    foot="EL CONSEJO LES RESPONDE A TODAS"),
             lines=["[#c1] Nvidia tiene un solo tipo de acción en el Nasdaq.",
                    "[#c2] Todas votan [#c3] igual.",
                    "[#foot] El consejo les responde a todas."]),
        dict(scene="certs", src=SRC_META,
             p=dict(kicker="META · ARMADA DISTINTO", sub="META · ACCIÓN COMÚN",
                    cards=[("CLASE A", "1 VOTO", TEAL, 1.0), ("CLASE B", "10 VOTOS", YEL, 1.12)], hot=[1],
                    caps=["LAS QUE TÚ PUEDES COMPRAR", "99.8% DE ZUCKERBERG"], foot="ZUCKERBERG: 60.8% DE TODOS LOS VOTOS"),
             lines=["[#c1] En Meta, las acciones clase A, las que tú puedes comprar, tienen un voto cada una.",
                    "[#c2] Clase B: diez votos cada una.",
                    "Zuckerberg tiene el {noventa y nueve punto ocho por ciento|99.8%} de la clase B.",
                    "[#foot] Eso es el {sesenta punto ocho por ciento|60.8%} de todos los votos."]),
        dict(scene="reveal2", src="8-K de Meta, 29 may. 2026",
             p=dict(title="EL ASTERISCO", qlines=["MAYO 2026:", "¿UNA ACCIÓN, UN VOTO?", "PERDIÓ."], hot=[2]),
             lines=["[#rev] En mayo, los accionistas votaron darle el mismo voto a cada acción.",
                    "[#quote] Perdió."]),
        dict(scene="ring2", src="8-K de Meta (29 may. 2026) e informe a accionistas · cálculo propio", src_color=(255, 210, 63),
             p=dict(kicker="LA VOTACIÓN SIN ZUCKERBERG", pct=85, fmt="{:.0f}%", l1="DE LOS VOTOS RESTANTES DIJO QUE SÍ",
                    chips=["NUESTRA CUENTA", "IGUAL PERDIÓ"]),
             lines=["Pero si quitas los votos de Zuckerberg,",
                    "[#count] cerca del {ochenta y cinco por ciento|85%} de los votos restantes dijo que sí.",
                    "[#chips] Es nuestra cuenta."]),
        dict(scene="answer_cta", src="Nuestra lectura, con base en los reportes de las empresas", src_color=(255, 210, 63),
             p=dict(kicker="LA RESPUESTA", ask="¿POR QUÉ NADIE LE DICE QUE NO?", icon="ballot", tag="NUESTRA LECTURA",
                    ans1="60.8% DE LOS VOTOS.", ans2="ÉL ELIGE AL CONSEJO.", follow="+ SEGUIR",
                    follow_sub="¿A quién desglosamos después?", like_txt="DALE LIKE PARA EL SIGUIENTE ASTERISCO"),
             lines=["[#ask] ¿Por qué nadie le dice que no a Zuckerberg?",
                    "[#ans] Nuestra lectura: con el {sesenta punto ocho por ciento|60.8%} de los votos, él elige al consejo. En Nvidia, el consejo sí pudo decirle que no a su fundador.",
                    "[#fol] ¿A quién desglosamos después? Síguenos [#like] y dale like."]),
    ],
    post=dict(
        tiktok=("El consejo de Nvidia le acaba de decir que no a su propio director general. ¿Por qué nadie le puede decir que no a Mark Zuckerberg?\n\n"
                "Fuentes: comunicado de cambio de director general de Nvidia (8-K, 12 nov. 2026); presidente del consejo de Nvidia en la llamada del 17 nov. (vía NPR); "
                "resultados Q3 FY2027 de Nvidia (8-K, 17 nov. 2026); reportes a accionistas de Nvidia (un voto por acción); "
                "informe a accionistas de Meta (DEF 14A, abr. 2026); 8-K de Meta con los resultados de la votación del 27 may. 2026. "
                "Los $8,300 por segundo y el 85% son cálculo propio (el 85% supone que Zuckerberg votó todas sus acciones en contra). "
                "La comparación es nuestra lectura. No es recomendación de inversión.\n\n"
                "#nvidia #meta #negocios #dinero #acciones"),
        title="¿Por qué nadie le dice que no a Zuckerberg?",
    ),
)

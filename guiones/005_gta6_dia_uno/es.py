"""005 · GTA 6 vendió $3,790 millones en un día. Su dueña esperaba menos en tres meses. ¿Cómo? — español (Con Asterisco).
Adaptación, no traducción. Estándar v3 (docs 08 y 09). Ancla ES = la misma marca: GTA 6 se conoce igual en los dos mercados.
Referencias: R1 experienciasdecompra OXXO (TT ES, 2.6M), R2 margencerofr desafío de Musk (TT ES, 1.3M)."""
WORLD = dict(
    shops=[dict(kind="block", x=40, w=620, h=500, col=(44, 60, 124)),
           dict(kind="games", x=700, w=820, h=520, sign="VIDEOJUEGOS", col=(255, 104, 88)),
           dict(kind="screens", x=1560, w=640, h=470, sign="TIENDA DE CONSOLA", col=(64, 206, 186)),
           dict(kind="block", x=2240, w=500, h=430, col=(184, 196, 220)),
           dict(kind="tower", x=2780, w=700, h=540, sign="TAKE-TWO", col=(44, 60, 124))],
    queue=dict(x0=880, n=6, gap=82), crosswalks=[1520])
SPEC = dict(
    id="005_gta6_dia_uno", lang="es-419", lang_tag="ES", voice="em_alex", speed=1.0,
    brand="CON ASTERISCO",
    lexicon={"Xbox": "Ex box", "Take-Two": "Teik Tu", "PlayStation": "Pléisteishon", "Rockstar": "Rocstar"},
    world=WORLD,
    camera=dict(push=0.03, enter=0.08, punch=["q", "a", "b", "nb", "who", "cut", "pre", "est", "ans", "fol", "like"],
                shake=["nb", "est", "ans"]),
    music=dict(style="groove", bpm=112, gain=0.17, duck=0.6, riser_scenes=["w_note"]),
    sfx=[],
    tail=2.5, card_dur=1.8, card_title="FUENTES",
    sources_card=["8-K de Take-Two, 20 nov. 2026 (anexo 99.1)",
                  "Resultados Q2 FY2027 de Take-Two (8-K), 9 nov. 2026",
                  "Por qué no cuadran: nuestra lectura"],
    beats=[
        dict(scene="w_hook", at=1180,
             p=dict(kicker="GTA 6 · SEMANA DE ESTRENO", q1="GTA 6 VENDIÓ", q2="$3,790 MILLONES", q3="EN UN DÍA.",
                    q4="SU DUEÑA ESPERABA MENOS EN 3 MESES. ¿CÓMO?"),
             lines=["{G T A Seis|GTA 6} vendió {tres mil setecientos noventa millones de dólares|$3,790 millones} en un día.",
                    "[#q] Su dueña esperaba menos que eso en tres meses completos. ¿Cómo?"]),
        dict(scene="w_board", at=2490,
             p=dict(kicker="UN DÍA CONTRA TRES MESES", title="¿UN DÍA LE GANÓ A UN TRIMESTRE?",
                    rows=[dict(label="19 NOV. · UN DÍA", v=3.79, val="$3,790 M", col=(255, 210, 63), cue="a"),
                          dict(label="OCT.–DIC. · PRONÓSTICO DE TAKE-TWO", v=3.5, val="$3,350–3,500 M",
                               col=(64, 206, 186), cue="b")],
                    stamp="NO ES EL MISMO DINERO"),
             lines=["[#a] Un día: tres mil setecientos noventa millones.",
                    "[#b] Su pronóstico de octubre a diciembre: hasta tres mil quinientos.",
                    "[#nb] Respuesta corta: no es el mismo dinero."]),
        dict(scene="w_layer", at=1180,
             p=dict(kicker="CONTADOR 1", n=1, of=3, title="LO QUE PAGASTE", anim="register",
                    who="$3,790 M = VENTAS AL PÚBLICO", who_sub="LO QUE PAGARON LOS JUGADORES EN TODAS LAS TIENDAS"),
             lines=["[#who] Esos tres mil setecientos noventa millones son lo que pagaron los jugadores.",
                    "En todas las tiendas: PlayStation, Xbox, la tienda de Rockstar y las tiendas físicas."]),
        dict(scene="w_layer", at=2420,
             p=dict(kicker="CONTADOR 2", n=2, of=3, title="LO QUE LE LLEGA A TAKE-TWO", anim="split",
                    from_x=2080, to_x=2950, who="PRONÓSTICO = VENTAS DE TAKE-TWO", who_sub="LO QUE ELLA MISMA VENDE",
                    cut_txt="TIENDAS Y CONSOLAS SE QUEDAN UNA PARTE"),
             lines=["[#who] El pronóstico cuenta otra cosa: lo que vende Take-Two.",
                    "[#cut] Y las tiendas y las consolas se quedan con una parte de lo que pagas."]),
        dict(scene="w_layer", at=3130,
             p=dict(kicker="Y LAS FECHAS", n=3, of=3, title="PRONÓSTICO: 9 NOV.", anim="stack",
                    who="10 DÍAS ANTES DEL ESTRENO", pre_big="32.5 MILLONES", pre_sub="COPIAS VENDIDAS ANTES DE SALIR · RÉCORD"),
             lines=["[#who] Además, ese pronóstico salió el nueve de noviembre. Diez días antes del estreno.",
                    "[#pre] Y antes de salir, ya había vendido treinta y dos millones y medio de copias. Récord."]),
        dict(scene="w_note", at=2490,
             p=dict(kicker="EL ASTERISCO", title="EL COMUNICADO TAMBIÉN TRAE UNO",
                    head="TAKE-TWO · 20 NOV. 2026", line="DAY ONE RETAIL SALES*: $3.79B",
                    foot="*BASED ON COMPANY ESTIMATES", est_txt="ES UNA ESTIMACIÓN DE LA EMPRESA"),
             lines=["¿Y lo mejor? El comunicado de Take-Two trae su propio asterisco.",
                    "[#est] Los tres mil setecientos noventa millones son una estimación de la propia empresa."]),
        dict(scene="w_answer", at=1900,
             p=dict(kicker="LA RESPUESTA", ask="¿UN DÍA LE GANÓ A 3 MESES?", icon="none", tag="NUESTRA LECTURA",
                    ans1="NO. DOS CONTADORES:", ans2="LO QUE PAGASTE ≠ LO QUE LE LLEGA",
                    follow="+ SEGUIR", follow_sub="Mándaselo a ese amigo que no sale de su cuarto desde el jueves",
                    like_txt="SÍGUENOS PARA EL PRÓXIMO ASTERISCO"),
             lines=["[#ask] Entonces, ¿un día le ganó a tres meses?",
                    "[#ans] No. Son dos contadores distintos: lo que pagaste tú, y lo que le llega a Take-Two.",
                    "Nuestra lectura: cuánto le llega de verdad, lo veremos en su próximo reporte.",
                    "[#fol] Mándaselo a ese amigo que no sale de su cuarto desde el jueves.",
                    "[#like] Síguenos para el próximo asterisco."]),
    ],
    post=dict(
        tiktok=("GTA 6 vendió $3,790 millones en un día. Su dueña esperaba menos en tres meses completos. ¿Cómo?\n\n"
                "Fuentes: 8-K de Take-Two, 20 nov. 2026 (anexo 99.1): \"day one retail sales* reached $3.79 billion\", "
                "\"*based on company estimates through end of day November 19th worldwide\"; \"sold 32.5 million units "
                "pre-release\". Resultados Q2 FY2027 de Take-Two (8-K), 9 nov. 2026: pronóstico de ventas netas reservadas "
                "(net bookings) de oct.–dic. 2026 de $3,350–3,500 millones. Las ventas al público (lo que pagaron los jugadores) "
                "y las ventas netas de Take-Two son medidas distintas; Take-Two no publica cómo se pasa de una a otra, así que "
                "la explicación es nuestra lectura. Sin relación con Take-Two ni Rockstar. No es recomendación de inversión.\n\n"
                "#gta6 #gta #negocios #dinero #videojuegos"),
        title="GTA 6 vendió $3,790 millones en un día. ¿Cómo?",
    ),
)

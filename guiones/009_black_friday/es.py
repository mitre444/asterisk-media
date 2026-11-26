"""009 · La "oferta" de Amazon en Black Friday costaba más que nueve días antes. ¿Black Friday es de verdad más barato? — español.
Adaptación, no traducción. Estándar v3. Ancla ES = la misma marca (Amazon se conoce en los dos mercados) + el bolsillo.
Referencias: R1 @groundworkcollab (IG, 133K, 31.6x), R2 @outspokenedits (TT, 167K, 31.5x)."""
SPEC = dict(
    id="009_black_friday", lang="es-419", lang_tag="ES", voice="em_alex", speed=1.0,
    brand="CON ASTERISCO",
    lexicon={"Amazon": "Ámazon", "Black Friday": "Blac Fráidei", "Adobe": "Adóbi", "Which?": "Uích"},
    world=dict(
        shops=[dict(kind="block", x=40, w=600, h=480, col=(44, 60, 124), billboard=["BLACK FRIDAY", "HASTA 70% MENOS"]),
               dict(kind="store", x=680, w=820, h=520, sign="ZAPATERÍA", col=(255, 104, 88)),
               dict(kind="screens", x=1540, w=640, h=470, sign="ELECTRÓNICA", col=(64, 206, 186)),
               dict(kind="block", x=2220, w=520, h=430, col=(184, 196, 220)),
               dict(kind="tower", x=2780, w=700, h=540, sign="AMAZON", col=(44, 60, 124))],
        queue=dict(x0=860, n=6, gap=82), crosswalks=[1500]),
    camera=dict(push=0.03, enter=0.08, punch=["q", "a", "b", "nb", "who", "cut", "est", "ans", "fol", "like"],
                shake=["nb", "est", "ans"]),
    music=dict(style="groove", bpm=112, gain=0.17, duck=0.6, riser_scenes=["w_note"]),
    sfx=[],
    tail=2.5, card_dur=1.8, card_title="FUENTES",
    sources_card=["Groundwork Collaborative, 16 nov. 2026",
                  "Amazon, \"Correcting the record\", 16 nov. 2026",
                  "Which?, 25 nov. 2025 · Adobe, resumen 2025",
                  "Respuesta final: nuestra lectura"],
    beats=[
        dict(scene="w_hook", at=1090,
             p=dict(kicker="AMAZON · BLACK FRIDAY 2025", q1="BOTAS \"EN OFERTA\":", q2="$126.99", q3="9 DÍAS ANTES: $79.97",
                    q4="¿DE VERDAD ES MÁS BARATO?"),
             lines=["Amazon puso estas botas en oferta en Black Friday: {ciento veintisiete dólares|$126.99}.",
                    "Nueve días antes costaban {ochenta|$79.97}.",
                    "[#q] ¿Black Friday es de verdad más barato?"]),
        dict(scene="w_board", at=2470,
             p=dict(kicker="LAS MISMAS BOTAS · 2025", title="LA \"OFERTA\" SALIÓ MÁS CARA",
                    rows=[dict(label="9 DÍAS ANTES", v=79.97, val="$79.97", col=(64, 206, 186), cue="a"),
                          dict(label="\"OFERTA\" DE BLACK FRIDAY", v=126.99, val="$126.99", col=(255, 210, 63), cue="b")],
                    stamp="+59%", stamp_pill=True),
             lines=["[#a] Antes: ochenta.",
                    "[#b] En oferta: ciento veintisiete. Cincuenta y nueve por ciento más.",
                    "[#nb] Respuesta corta: el descuento se mide contra un precio. Y ese precio lo pone la tienda."]),
        dict(scene="w_layer", at=1090,
             p=dict(kicker="351 OFERTAS DE AMAZON", n=1, of=3, title="1 DE CADA 3", anim="register",
                    who="IGUAL O MÁS BARATO UN MES ANTES", who_sub="Y CASI 1 DE CADA 10 COSTABA MÁS EN LA OFERTA"),
             lines=["Un centro de estudios revisó trescientas cincuenta y una ofertas de Amazon.",
                    "[#who] Casi una de cada tres costaba igual o menos un mes antes. Y casi una de cada diez, más."]),
        dict(scene="w_layer", at=3000,
             p=dict(kicker="LO QUE RESPONDE AMAZON", n=2, of=3, title="\"DEFECTUOSO Y FALSO\"", anim="split", from_x=2350, to_x=3130,
                    who="98%: IGUAL O MÁS BAJO QUE EN 30 DÍAS", who_sub="350 DE MÁS DE 10 MILLONES DE OFERTAS, DICE",
                    cut_txt="SU PROPIA CUENTA: 1 DE CADA 10 = MISMO PRECIO"),
             lines=["Amazon dice que está mal: trescientos cincuenta productos de diez millones de ofertas.",
                    "[#who] Y que el noventa y ocho por ciento estaba igual o más bajo que en los treinta días previos.",
                    "[#cut] Pero con su propia cuenta, una de cada diez ofertas de 2025 tenía... el mismo precio."]),
        dict(scene="w_layer", at=1860,
             p=dict(kicker="UN AÑO · REINO UNIDO", n=3, of=3, title="0 DE 175",
                    who="EN SU PRECIO MÁS BAJO DEL AÑO", who_sub="WHICH?, ASOCIACIÓN DE CONSUMIDORES · OFERTAS DE 2024"),
             lines=["Una asociación británica de consumidores siguió ciento setenta y cinco ofertas un año entero.",
                    "[#who] Ninguna estuvo en su precio más bajo del año en Black Friday."]),
        dict(scene="w_note", at=2470,
             p=dict(kicker="EL ASTERISCO", title="Y AUN ASÍ: EL DÍA CON MÁS DESCUENTO",
                    head="ADOBE · EN LÍNEA EN EE. UU., 2025", line="BLACK FRIDAY: −23.7%*",
                    foot="*PROMEDIO, CONTRA EL PRECIO DE LISTA", est_txt="EL PRECIO QUE ELIGE LA TIENDA"),
             lines=["¿El giro? Según Adobe, Black Friday sí es el día con más descuento en línea: veintitrés punto siete por ciento, en promedio.",
                    "[#est] Contra el precio de lista. El que elige la tienda."]),
        dict(scene="w_answer", at=1180,
             p=dict(kicker="LA RESPUESTA", ask="¿ES MÁS BARATO?", icon="none", tag="NUESTRA LECTURA",
                    ans1="MÁS BARATO QUE LA ETIQUETA.", ans2="NO SIEMPRE QUE EL MES PASADO",
                    follow="+ SEGUIR", follow_sub="Mándaselo a ese amigo que tiene el carrito lleno desde Halloween",
                    like_txt="SIGUE PARA EL PRÓXIMO ASTERISCO"),
             lines=["[#ask] Entonces, ¿es más barato?",
                    "[#ans] Nuestra lectura: más barato que la etiqueta, sí. Que el mes pasado, no siempre. Revisa el historial antes.",
                    "[#fol] Mándaselo a ese amigo que tiene el carrito lleno desde Halloween.",
                    "[#like] Sigue para el próximo asterisco."]),
    ],
    post=dict(
        tiktok=("La \"oferta\" de Amazon en Black Friday: $126.99. Nueve días antes: $79.97. ¿Black Friday es de verdad más barato?\n\n"
                "Fuentes: Groundwork Collaborative, \"Amazon's Decoy Deals\" (16 nov. 2026): más de 350 productos de las páginas de ofertas "
                "de Black Friday y Cyber Monday de Amazon, 2024–2025; casi 1 de cada 3 costaba igual o menos el mes anterior y casi 1 de cada 10 costaba más; "
                "ejemplo: botas de lluvia Hunter para mujer, $126.99 en Black Friday 2025 contra $79.97 nueve días antes. "
                "Amazon, \"Correcting the record about Amazon's deal-event pricing\" (16 nov. 2026): dice que el estudio es defectuoso; "
                "350 de más de 10 millones de ofertas; 98% igual o más bajo que en los 30 días previos; en 2025, 89% más bajo y 10% igual. "
                "Which? (25 nov. 2025): 175 ofertas de Black Friday 2024 seguidas de mayo 2024 a mayo 2025 en Reino Unido; ninguna en su precio más bajo del año en Black Friday. "
                "Adobe, resumen de temporada 2025: Black Friday fue el día con más descuento en línea en EE. UU. (−23.7% promedio); "
                "Adobe mide descuentos contra el precio de lista (pronóstico 2026, 28 sep. 2026). "
                "\"Más barato que la etiqueta, no siempre que el mes pasado\" es nuestra lectura. Sin relación con Amazon. No es asesoría financiera.\n\n"
                "#blackfriday #amazon #ofertas #dinero #compras"),
        title="¿Black Friday es de verdad más barato?",
    ),
)

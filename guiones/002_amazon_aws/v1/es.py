"""002 · Los 717 mil millones de Amazon y de dónde sale la ganancia — español (Con Asterisco). Adaptación, no traducción."""
YEL = (255, 210, 63)
SRC = "Resultados de Amazon, 4T 2025 (5 de feb. de 2026)"
BASE = dict(kicker="AMAZON · 2025", num="$717 mil M", sub="EN VENTAS")

SPEC = dict(
    id="002_amazon_aws", lang="es-419", lang_tag="ES", voice="em_alex", speed=1.0,
    brand="CON ASTERISCO",
    lexicon={"Amazon": "Ámason", "Web": "Ueb", "Services": "Sérvises"},
    sfx=[("ast", "ding", 0.0), ("rev", "thump", 0.0), ("rev", "ding", 0.06)],
    beats=[
        dict(scene="bignum", src=SRC, p=dict(BASE, sub2="Casi toda la ganancia salió de otro lado"), lines=[
            "En {dos mil veinticinco,|2025,} Amazon vendió {setecientos diecisiete|717} mil millones de dólares.",
            "[#sub2] Pero la mayor parte de su ganancia no salió de nada que llegue [#ast] en una caja.",
        ]),
        dict(scene="split", src=SRC + " · cálculo propio",
             p=dict(kicker="LAS TIENDAS CONTRA TODO LO DEMÁS", t1="VENTAS", a1=82, t2="GANANCIA OPERATIVA", a2=43,
                    la="TIENDAS", lb="AWS"),
             lines=[
                 "Las tiendas son la parte que conoces: las cajas, las camionetas, las entregas al día siguiente.",
                 "Dentro y fuera de Norteamérica, fueron el [#sp1] {ochenta y dos por ciento|82%} de esas ventas.",
                 "[#sp2] Pero menos de la mitad de la ganancia operativa.",
             ]),
        dict(scene="reveal", src="Informe anual 2025 de Amazon",
             p=dict(title="EL ASTERISCO", qlines=["Amazon también", "renta computadoras.", "Se llama", "Amazon Web Services."],
                    hot=[3], attr1="AWS", attr2="Cómputo en la nube que otras empresas pagan por usar"),
             lines=[
                 "[#rev] Aquí va el asterisco.",
                 "[#quote] Amazon también renta computadoras. Se llama Amazon Web Services, y otras empresas pagan por correr ahí sus aplicaciones.",
             ]),
        dict(scene="statement", src=SRC,
             p=dict(kicker="AWS · 2025", doc="DE LOS RESULTADOS POR SEGMENTO · MILLONES DE DÓLARES (MDD)", r1="Ventas de AWS",
                    v1="128,700 mdd", r2="Ganancia operativa", v2="45,600 mdd", lw=300,
                    ratio="Parte de AWS en la ganancia operativa de Amazon", pct=57, pfmt="{:.0f}%"),
             lines=[
                 "Ese año, [#fees] {a doble u ese|AWS} vendió [#v1] {ciento veintinueve|129} mil millones de dólares.",
                 "[#profit] Y su ganancia operativa fue de {cuarenta y cinco mil seiscientos|45,600} millones: [#pct] el {cincuenta y siete por ciento|57%} de todo lo que ganó Amazon.",
             ]),
        dict(scene="bars", src=SRC + " · cálculo propio",
             p=dict(kicker="GANANCIA OPERATIVA POR CADA $100 DE VENTAS", v1=6, v2=35, fmt="${:.0f}", l1="LAS TIENDAS", l2="AWS",
                    badge="6×", grow_dur=1.2),
             lines=["Y es mucho mejor negocio.", "Por cada cien dólares de ventas, a las tiendas les quedaron unos seis. [#grow] A {a doble u ese,|AWS,} {treinta y cinco.|35.}"]),
        dict(scene="close_num", src="Sigue la cuenta para ver el próximo asterisco", src_color=YEL,
             p=dict(BASE, kicker="O SEA", kicker0=BASE["kicker"], pre=["MISMA EMPRESA.", "DOS NEGOCIOS."], s1=["La tienda donde compras", "es el negocio grande."],
                    s2=["El que nunca ves", "es el que deja la ganancia."]),
             lines=[
                 "Misma empresa. Dos negocios muy distintos.",
                 "[#s1] Así que la tienda donde compras es el negocio grande.",
                 "[#s2] El que nunca ves es el que deja la ganancia.",
                 "[#back] Y ese es el asterisco de los {setecientos diecisiete|717} mil millones.",
             ]),
    ],
    post=dict(
        tiktok=("Amazon vendió 717 mil millones de dólares en 2025. El asterisco: casi toda la ganancia salió de un negocio que nunca ves.\n\n"
                "Fuentes: resultados de Amazon del cuarto trimestre y del año 2025 (5 feb 2026). Los porcentajes son cálculo propio "
                "con las cifras por segmento de Amazon.\n\n#amazon #aws #negocios #dinero #finanzas"),
        title="De dónde sale en realidad la ganancia de Amazon",
    ),
)

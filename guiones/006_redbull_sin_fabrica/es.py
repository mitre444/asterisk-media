"""006 · Red Bull vendió 14 mil millones de latas. No llenó ni una. ¿A qué se dedica? — español (Con Asterisco). Adaptación, no traducción.
Referencias (referencias.md): R1 matiasherediaa1 (59x, visto), R2 zamora_jose7 (157x), R3 brayanjacksonclub (76.9x, visto).
Patrones (doc 03): P2 cifra en el cuadro 1, P9 contador 1/4 visible, P7 explicador ilustrado, C2 cierre pidiendo compartir.
Variable a medir: escenas ilustradas con estilo propio (illus.py) en vez de íconos sueltos.
Reglas: lata genérica con colores nuestros, sin logo ni colores de Red Bull, sin colores de escuderías, sin personajes conocidos ni fotos.
Red Bull no publica cuánto gasta en marketing ni su utilidad: nunca dar cifra de ninguna de las dos."""
SRC_RB = "Perfil de empresa de Red Bull (redbull.com), cifras 2025"
SRC_RAUCH = "Historia de Rauch (rauch.cc); informe de sostenibilidad de Rauch 2023"
SRC_CAN = "Ciudad de Concord, Carolina del Norte (2021, oct. 2025): Ball hace las latas"
SRC_TRIP = "Red Bull, \"ciclo de vida de la lata\" (redbull.com)"
SRC_US = "Ciudad de Concord (oct. 2025); NC Commerce (2021); Glendale/ACA (2019)"
SPEC = dict(
    id="006_redbull_sin_fabrica", lang="es-419", lang_tag="ES", voice="em_alex", speed=1.0,
    brand="CON ASTERISCO", theme="volt", hook_timer=True,
    lexicon={"like": "laik", "Red Bull": "Red Bul", "Rauch": "Ráuj", "Ball": "Bol"},
    camera=dict(push=0.04, enter=0.10, punch=["zero", "cans", "sec", "rev", "who", "nb", "ath", "f1", "ctry", "quote",
                                              "az", "nc", "rb", "ask", "ans", "fol", "like"],
                shake=["zero", "nb", "rb", "ans"]),
    music=dict(bpm=100, cut="nb", riser_scenes=["reveal2"], gain=0.20, duck=0.55),
    sfx=[],
    beats=[
        dict(scene="can_hook", src="Red Bull (redbull.com) · Rauch (rauch.cc)",
             p=dict(kicker="RED BULL · EL AÑO PASADO", q1="RED BULL VENDIÓ", q2="14 MIL MILLONES DE LATAS.",
                    q3="NO LLENÓ NI UNA.", q4="¿ENTONCES A QUÉ SE DEDICA?", stamp="NI UNA"),
             lines=["Red Bull vendió casi {catorce mil millones|14 mil millones} de latas el año pasado.",
                    "[#zero] Y no llenó ni una.",
                    "¿Entonces a qué se dedica Red Bull?"]),
        dict(scene="can_mountain", src=SRC_RB + " · por segundo: cálculo propio",
             p=dict(kicker="RED BULL · 2025", big="{:,.0f} MILLONES", big_mult=1000, big_l="LATAS VENDIDAS EN 2025",
                    sec="≈443 LATAS POR SEGUNDO", tag="CÁLCULO PROPIO", rev="€12,200 M EN VENTAS"),
             lines=["[#cans] Casi catorce mil millones.",
                    "[#sec] Son unas {cuatrocientas cuarenta y tres|443} latas por segundo. Es nuestra cuenta.",
                    "[#rev] Y doce mil doscientos millones de euros en ventas."]),
        dict(scene="chain_step", src=SRC_CAN,
             p=dict(kicker="SIGUE LA LATA", n=1, title="LA LATA", ill="canmaker", who="BALL",
                    who_sub="UNA EMPRESA DE EMPAQUES · PLANTAS DE EE. UU.", labels=["LATA", "BEBIDA", "VIAJE", "???"]),
             lines=["Sigue la lata. Paso uno: la lata de aluminio.",
                    "[#who] En sus plantas de Estados Unidos, la hace Ball, una empresa de empaques."]),
        dict(scene="chain_step", src=SRC_RAUCH,
             p=dict(kicker="SIGUE LA LATA", n=2, title="LA BEBIDA", ill="filler", who="RAUCH",
                    who_sub="UNA EMPRESA AUSTRIACA DE JUGOS · DESDE 1987", labels=["LATA", "BEBIDA", "VIAJE", "???"]),
             lines=["Paso dos: la bebida.",
                    "[#who] La llena Rauch, una empresa austriaca de jugos. Desde el primer lote, en {mil novecientos ochenta y siete.|1987.}"]),
        dict(scene="chain_step", src=SRC_TRIP,
             p=dict(kicker="SIGUE LA LATA", n=3, title="EL VIAJE", ill="ship", who="TREN + BARCO",
                    who_sub="DE AUSTRIA Y SUIZA A MÁS DE 170 PAÍSES", labels=["LATA", "BEBIDA", "VIAJE", "???"]),
             lines=["Paso tres: el viaje.",
                    "[#who] De Austria y Suiza, en tren o en barco, a más de {ciento setenta|170} países."]),
        dict(scene="interrupt", src="",
             p=dict(lines=["NADA DE ESO", "ES RED BULL."], hot=[1], ys=[700, 860]),
             lines=[dict(text="[#nb] Tres pasos. Ninguno es Red Bull.", pause=0.35)]),
        dict(scene="world_spend", src=SRC_RB,
             p=dict(kicker="¿ENTONCES DÓNDE ESTÁ RED BULL?", title="AQUÍ.", n1="900+", l1="ATLETAS, ARTISTAS Y EQUIPOS",
                    n2="2", l2="EQUIPOS DE FÓRMULA 1", n3="178", l3="PAÍSES"),
             lines=["¿Entonces dónde está Red Bull?",
                    "[#ath] Detrás de más de novecientos atletas, artistas y equipos.",
                    "[#f1] En dos equipos de Fórmula Uno.",
                    "[#ctry] Y en las tiendas de {ciento setenta y ocho|178} países."]),
        dict(scene="reveal2", src=SRC_US,
             p=dict(title="EL ASTERISCO", qlines=["EN EE. UU. SÍ PUSO", "DINERO EN PLANTAS."], hot=[1]),
             lines=["Aquí va el asterisco. [#quote] En Estados Unidos, Red Bull sí puso dinero en plantas."]),
        dict(scene="campus", src=SRC_US,
             p=dict(kicker="COMPARTIDAS CON RAUCH Y BALL", pin1="ARIZONA · 2021", pin2="CAROLINA DEL N. · 2028",
                    b1="LATAS", w1="BALL", b2="LLENADO", w2="RAUCH", b3="ALMACÉN", w3="RED BULL",
                    rb="LO DE RED BULL: EL ALMACÉN"),
             lines=["Dos complejos, [#az] en Arizona [#nc] y en Carolina del Norte.",
                    "Ball hace las latas. Rauch las llena.",
                    "[#rb] Lo de Red Bull en Carolina del Norte: el almacén."]),
        dict(scene="answer_track", src="Nuestra lectura, con datos de Red Bull, Rauch y las ciudades", src_color=(255, 210, 63),
             p=dict(kicker="LA RESPUESTA", ask="¿A QUÉ SE DEDICA?", icon="none", tag="NUESTRA LECTURA",
                    ans1="FABRICA LA RAZÓN", ans2="POR LA QUE LA COMPRAS.", labels=["LATA", "BEBIDA", "VIAJE", "LA RAZÓN"],
                    follow="+ SEGUIR", follow_sub="Mándaselo a tu amigo que vive de Red Bull",
                    like_txt="LIKE PARA EL SIGUIENTE ASTERISCO"),
             lines=["[#ask] ¿Entonces a qué se dedica Red Bull? Nuestra lectura: no fabrica la bebida.",
                    "[#ans] Fabrica la razón por la que la compras.",
                    "[#fol] Mándaselo a tu amigo que vive de Red Bull.",
                    "[#like] Síguenos y dale like para el siguiente."]),
    ],
    post=dict(
        tiktok=("Red Bull vendió casi 14 mil millones de latas el año pasado y no llenó ni una. ¿Entonces a qué se dedica?\n\n"
                "Fuentes: perfil de empresa de Red Bull (13,969 millones de latas y €12,196 millones de ventas en 2025) y \"ciclo de vida "
                "de la lata\" (redbull.com); historia de Rauch e informe de sostenibilidad 2023 (rauch.cc); Ciudad de Concord, Carolina del "
                "Norte (2021 y oct. 2025); NC Commerce (jul. 2021); Ciudad de Glendale / Arizona Commerce Authority (mar. 2019). "
                "Las 443 latas por segundo son cálculo propio (13,969 millones entre los segundos de un año). Que Ball hace las latas se "
                "refiere a las plantas de EE. UU. Red Bull no publica cuánto gasta en marketing. \"Fabrica la razón por la que la compras\" "
                "es nuestra lectura. Sin relación con Red Bull, Rauch ni Ball.\n\n"
                "#redbull #negocios #marketing #dinero #marcas"),
        title="Red Bull vendió 14 mil millones de latas. No llenó ni una.",
    ),
)

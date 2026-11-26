"""013 · Walmart se queda 3¢ por dólar. ¿Por qué ahora vende anuncios? — español (Con Asterisco). Adaptación, no traducción.
Patrones (doc 03): P8 dos cifras que chocan (3¢ contra +37%), P2 cifra en el cuadro 1, P4 noticia del día, C2 cierre pidiendo compartir.
Regla: Walmart no publica cuánto gana con la publicidad; nunca decir que sí. Solo objetos genéricos, sin logo ni colores de Walmart."""
SRC_FY = "Resultados Q4 FY26 de Walmart (8-K, 19 feb. 2026) y 10-K FY26"
SRC_Q3 = "Presentación de resultados Q3 FY27 de Walmart (8-K), 19 nov. 2026"
SRC_WC = "Walmart Connect (walmartconnect.com)"
SPEC = dict(
    id="013_walmart_anuncios", lang="es-419", lang_tag="ES", voice="em_alex", speed=1.0,
    brand="CON ASTERISCO", theme="vault", hook_timer=True,
    lexicon={"like": "laik", "Walmart": "Uólmart", "app": "ap"},
    camera=dict(push=0.04, enter=0.10, punch=["ads", "s", "p", "cut", "buy", "last", "grow", "app", "scr", "pay", "count", "badge",
                                              "rev", "quote", "stamp", "sub", "ask", "ans", "fol", "like"],
                shake=["ads", "cut", "grow", "stamp", "ans"]),
    music=dict(bpm=96, cut="wcut", riser_scenes=["reveal2"], gain=0.20, duck=0.55),
    sfx=[],
    beats=[
        dict(scene="receipt_hook", src=SRC_FY + " · cálculo propio",
             p=dict(kicker="WALMART · RESULTADOS DE HOY", q1="WALMART SE QUEDA", q2="3¢ POR DÓLAR.", q3="¿POR QUÉ AHORA VENDE ANUNCIOS?",
                    rows=[("CEREAL", "$1.00", False), ("TOTAL", "$1.00", False), ("SE QUEDA", "3¢", True)], head="TICKET",
                    stamp="¿ANUNCIOS?"),
             lines=["Walmart se queda con unos tres centavos de cada dólar que le gastas.",
                    "¿Entonces por qué ahora vende [#ads] anuncios?"]),
        dict(scene="dollar_split", src=SRC_FY + " · cálculo propio",
             p=dict(kicker="WALMART · ÚLTIMO AÑO FISCAL", sales="$713,200 M", sales_l="EN VENTAS", profit="$22,300 M",
                    profit_l="DE GANANCIA", bar_l="DE CADA $1 QUE GASTAS", rest="COSTOS", keep="WALMART SE QUEDA ≈3¢",
                    tag="CÁLCULO PROPIO"),
             lines=["[#s] El año pasado, Walmart vendió {setecientos trece mil millones de dólares.|$713,000 millones.}",
                    "[#p] Ganó {veintidós mil trescientos millones.|$22,300 millones.}",
                    "[#cut] Más o menos tres centavos por dólar. Es nuestra cuenta."]),
        dict(scene="cereal_buy", src=SRC_FY,
             p=dict(kicker="EL NEGOCIO DEL SÚPER", price="$1.00", price_sub="LO QUE PAGAS", pay="WALMART LO COMPRA PRIMERO"),
             lines=["Vender súper es un negocio durísimo.",
                    "Antes de venderte un dólar de cereal, [#buy] Walmart tiene que comprar ese cereal."]),
        dict(scene="bars2", src=SRC_Q3 + " · 7x: cálculo propio",
             p=dict(kicker="SIGUE EL DINERO · HOY", v1=5.2, v2=37, fmt="+{:.0f}%", labels=["VENTAS", "ANUNCIOS EE. UU."],
                    labels2=["INGRESOS TOTALES, AGO.–OCT.", "WALMART EE. UU., AGO.–OCT."], badge="7 VECES MÁS RÁPIDO"),
             lines=["Hoy, Walmart presentó su trimestre.",
                    "[#last] Ventas: cinco por ciento más.",
                    "[#grow] Publicidad en Estados Unidos: treinta y siete por ciento más."]),
        dict(scene="interrupt", src="",
             p=dict(lines=["¿QUÉ", "ANUNCIOS?"], hot=[1], ys=[700, 860]),
             lines=[dict(text="[#wcut] ¿Y qué anuncios?", pause=0.35)]),
        dict(scene="ad_spots", src=SRC_WC,
             p=dict(kicker="DÓNDE ESTÁN LOS ANUNCIOS", query="cereal", tag="PATROCINADO", l_app="EN LA APP", screen="¡NUEVO!",
                    l_scr="EN LA TIENDA", pay="LAS MARCAS PAGAN"),
             lines=["[#app] Los productos patrocinados hasta arriba en la app de Walmart.",
                    "[#scr] Las pantallas dentro de la tienda.",
                    "[#pay] Las marcas le pagan a Walmart para salir frente a ti justo cuando vas a comprar."]),
        dict(scene="tower", src=SRC_FY + " (incluye VIZIO)",
             p=dict(kicker="LA PUBLICIDAD DE WALMART · ÚLTIMO AÑO FISCAL", pre="CASI", prefix="$", value=6400, mult=1e6,
                    sub="DÓLARES EN ANUNCIOS", badge="+46% EN UN AÑO", item="box", land=1.6),
             lines=["Y no es poco.",
                    "[#count] El año pasado, su negocio de publicidad facturó casi {seis mil cuatrocientos millones de dólares.|$6,400 millones.}",
                    "[#badge] Cuarenta y seis por ciento más."]),
        dict(scene="reveal2", src=SRC_FY,
             p=dict(title="EL ASTERISCO", qlines=["ES LO QUE FACTURA,", "NO LO QUE GANA."], hot=[1]),
             lines=["[#rev] Aquí está el asterisco. [#quote] Eso es lo que factura, no lo que gana."]),
        dict(scene="classified", src=SRC_Q3,
             p=dict(kicker="LO QUE GANA CON ANUNCIOS", doc="PUBLICIDAD · GANANCIA", stamp="NO LO DICE",
                    quote="“CRECIMIENTO DE LA PUBLICIDAD DIGITAL”", attr="WALMART, SOBRE SU MARGEN EN EE. UU. · 19 NOV. 2026"),
             lines=["[#stamp] Walmart no dice cuánto se queda.",
                    "[#sub] Pero hoy dijo que su margen en Estados Unidos mejoró sobre todo por el crecimiento de la publicidad digital."]),
        dict(scene="answer_cta", src="Nuestra lectura, con base en los reportes de Walmart", src_color=(255, 210, 63),
             p=dict(kicker="LA RESPUESTA", ask="¿POR QUÉ VENDE ANUNCIOS?", icon="bills", tag="NUESTRA LECTURA",
                    ans1="NO SOLO ERES", ans2="EL CLIENTE.", follow="+ SEGUIR",
                    follow_sub="Mándaselo a alguien que compra en Walmart", like_txt="DALE LIKE PARA EL PRÓXIMO ASTERISCO"),
             lines=["[#ask] Entonces, ¿por qué vende anuncios? Nuestra lectura: venderte un dólar de cereal le cuesta casi un dólar.",
                    "Un dólar de anuncios le cuesta muchísimo menos. [#ans] No solo eres el cliente. Eres el público.",
                    "[#fol] Mándaselo a alguien que compra en Walmart.",
                    "[#like] Síguenos y dale like."]),
    ],
    post=dict(
        tiktok=("Walmart se queda con unos 3¢ de cada dólar que vende. ¿Entonces por qué ahora vende anuncios?\n\n"
                "Fuentes: resultados Q4 FY26 de Walmart (8-K, 19 feb. 2026) y 10-K FY26; presentación de resultados Q3 FY27 (8-K, 19 nov. 2026); "
                "Walmart Connect. Los 3¢ son cálculo propio (utilidad neta consolidada del año fiscal 2026, $22,300 M, entre ventas de $713,200 M). "
                "\"Ventas +5%\" son los ingresos totales, +5.2%; \"anuncios +37%\" es la publicidad de Walmart en EE. UU. Los $6,400 M de publicidad incluyen VIZIO "
                "y son ingresos, no ganancia: Walmart no publica cuánto gana con la publicidad. Por qué vende anuncios es nuestra lectura. "
                "Sin relación con Walmart. No es recomendación de inversión.\n\n"
                "#walmart #negocios #dinero #publicidad #acciones"),
        title="Walmart se queda 3¢ por dólar. ¿Por qué vende anuncios?",
    ),
)

"""014 · A Target le devolvieron $301 millones en aranceles. ¿Y a ti quién te devuelve? — español (Con Asterisco).
Adaptación, no traducción. Referencias y reglas: ver en.py y referencias.md.
Variable a medir: narración en historia con personajes genéricos (método de R1)."""
SRC_TGT = "8-K de Target, resultados Q3 2026 (18 nov. 2026), SEC EDGAR"
SRC_CBP = "Aduanas de EE. UU. (CBP), mensajes CSMS sobre reembolsos IEEPA (CAPE)"
SRC_SC = "Learning Resources, Inc. v. Trump (Suprema Corte de EE. UU., 20 feb. 2026)"
LAB = ["ADUANA", "ESTANTE", "TÚ", "REEMBOLSO"]
SPEC = dict(
    id="014_target_aranceles", lang="es-419", lang_tag="ES", voice="em_alex", speed=1.0,
    brand="CON ASTERISCO", theme="volt", hook_timer=True,
    lexicon={"like": "laik", "Target": "Tárguet", "CAPE": "keip"},
    camera=dict(push=0.04, enter=0.10, punch=["you", "big", "pct", "ytd", "who", "rule", "power", "nb", "quote", "val",
                                              "not", "ask", "ans", "fol", "like"],
                shake=["you", "rule", "nb", "not", "ans"]),
    music=dict(bpm=100, cut="nb", riser_scenes=["reveal2"], gain=0.20, duck=0.55),
    sfx=[],
    beats=[
        dict(scene="refund_hook", src=SRC_TGT,
             p=dict(kicker="TARGET · ESTA SEMANA", q1="A TARGET LE DEVOLVIERON", q2="$301 MILLONES",
                    q3="EN ARANCELES.", q4="¿Y A TI QUIÉN TE DEVUELVE?", stamp="¿Y TÚ?", amount="$301,000,000",
                    to="TARGET"),
             lines=["A Target le acaban de devolver {trescientos un millones de dólares|$301 millones} en aranceles.",
                    "[#you] ¿Y a ti quién te devuelve?"]),
        dict(scene="big_refund", src=SRC_TGT + " · 18%: nuestra cuenta",
             p=dict(kicker="TARGET · REPORTE Q3 · 18 NOV.", big="${:.0f} MILLONES", n=301,
                    big_l="EN REEMBOLSOS DE ARANCELES · UN TRIMESTRE", pct="≈18% DE SU UTILIDAD OPERATIVA",
                    tag="NUESTRA CUENTA", ytd="$1,300 MILLONES EN 2026", amount="$301,000,000", to="TARGET"),
             lines=["Viene en su reporte trimestral.",
                    "[#big] Trescientos un millones de dólares.",
                    "[#pct] Como el dieciocho por ciento de su utilidad operativa. Es nuestra cuenta.",
                    "[#ytd] Y mil trescientos millones en lo que va del año."]),
        dict(scene="tariff_step", src=SRC_CBP,
             p=dict(kicker="SIGUE UN DÓLAR", n=1, title="EN EL PUERTO", ill="customs", who="PAGA EL IMPORTADOR",
                    who_sub="EL ARANCEL SE LE PAGA A LA ADUANA", labels=LAB),
             lines=["Mira, sigue un dólar. Paso uno: llega una caja del extranjero.",
                    "[#who] En el puerto, el que la importa le paga el arancel a la aduana de Estados Unidos.",
                    "Muchas cadenas grandes importan ellas mismas."]),
        dict(scene="tariff_step", src="",
             p=dict(kicker="SIGUE UN DÓLAR", n=2, title="EN EL ESTANTE", ill="shelf", who="EL PRECIO PUEDE SUBIR",
                    who_sub="PARA CUBRIR ESE COSTO", tag_old="$", tag_new="$$", labels=LAB),
             lines=["Paso dos: el estante.",
                    "[#who] Para cubrir ese costo, el precio puede subir."]),
        dict(scene="tariff_step", src="",
             p=dict(kicker="SIGUE UN DÓLAR", n=3, title="EN LA CAJA", ill="register", who="TÚ PAGAS EL PRECIO",
                    who_sub="EL ARANCEL YA SE PAGÓ EN LA ADUANA", labels=LAB),
             lines=["Paso tres: tú.",
                    "[#who] En la caja, tú pagas ese precio."]),
        dict(scene="court_hit", src=SRC_SC,
             p=dict(kicker="20 DE FEBRERO DE 2026", title="LA SUPREMA CORTE", stamp="6–3",
                    l1="NO TENÍA EL PODER", l2="LEARNING RESOURCES V. TRUMP · ARANCELES IEEPA"),
             lines=["Pero en febrero, [#rule] la Suprema Corte votó seis a tres:",
                    "[#power] el presidente no tenía el poder de poner esos aranceles."]),
        dict(scene="interrupt", src="",
             p=dict(lines=["EL DINERO SE DEVUELVE.", "¿PERO A QUIÉN?"], hot=[1], ys=[700, 860]),
             lines=[dict(text="[#nb] Entonces el dinero se tiene que devolver. ¿Pero a quién?", pause=0.35)]),
        dict(scene="reveal2", src=SRC_CBP,
             p=dict(title="EL ASTERISCO", qlines=["NO ES AUTOMÁTICO.", "EL IMPORTADOR LO RECLAMA."], hot=[1]),
             lines=["Aquí está el asterisco. [#quote] El reembolso no es automático.",
                    "El que pagó en la aduana tiene que reclamarlo, en un sistema de Aduanas que se llama {keip|CAPE}."]),
        dict(scene="report_note", src=SRC_TGT,
             p=dict(kicker="EL REPORTE DE TARGET", title="¿Y LOS CLIENTES?", val="CUENTA COMO MENOS COSTOS",
                    stamp="¿PASARLO AL CLIENTE? NO LO DICE", l2="EL REPORTE NO DICE QUE REGRESE A LOS CLIENTES"),
             lines=["¿Y el reporte de Target? [#val] Cuenta el reembolso como menos costos.",
                    "[#not] No dice que se lo vaya a pasar a sus clientes."]),
        dict(scene="answer_refund", src="Nuestra lectura, con base en CBP y el 8-K de Target", src_color=(255, 210, 63),
             p=dict(kicker="LA RESPUESTA", ask="¿Y A TI QUIÉN TE DEVUELVE?", icon="none", tag="NUESTRA LECTURA",
                    ans1="NADIE, EN AUTOMÁTICO.", ans2="SE LO LLEVA EL IMPORTADOR.", labels=LAB,
                    amount="REEMBOLSO", to="IMPORTADOR",
                    follow="+ SÍGUENOS", follow_sub="Mándaselo a alguien que pagó más este año",
                    like_txt="DALE LIKE PARA EL SIGUIENTE"),
             lines=["[#ask] Entonces, ¿a ti quién te devuelve?",
                    "[#ans] Nadie, en automático. Se lo lleva el que pagó en la aduana.",
                    "Nuestra lectura: si algún día lo ves, será como un precio más bajo. Y eso lo decide cada empresa.",
                    "[#fol] Mándaselo a alguien que pagó más este año.",
                    "[#like] Síguenos y dale like."]),
    ],
    post=dict(
        tiktok=("A Target le devolvieron $301 millones en aranceles. ¿Y a ti quién te devuelve?\n\n"
                "Fuentes: 8-K de Target, resultados Q3 2026 (18 nov. 2026): $301 millones antes de impuestos en reembolsos de "
                "aranceles IEEPA en el trimestre y $1,300 millones en 2026 al 31 de octubre, registrados como menor costo de ventas; "
                "utilidad operativa de $1,672 millones (el 18% es cálculo propio). Learning Resources, Inc. v. Trump (Suprema Corte "
                "de EE. UU., 20 feb. 2026, 6–3). Mensajes CSMS de Aduanas de EE. UU. (CBP) sobre reembolsos IEEPA y CAPE: el "
                "reembolso va al importador registrado, que tiene que reclamarlo. El comunicado de Target no dice que vaya a pasar "
                "los reembolsos a sus clientes. \"Si lo ves, será como un precio más bajo\" es nuestra lectura. Sin relación con "
                "Target. No es asesoría legal ni fiscal.\n\n"
                "#target #aranceles #negocios #dinero #noticias"),
        title="A Target le devolvieron $301 millones en aranceles. ¿Y a ti?",
    ),
)

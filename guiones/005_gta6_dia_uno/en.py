"""005 · GTA 6 made $3.79 billion in one day. Its maker expected less for three months. How? — English (With an Asterisk).
First video on standard v3 (doc 08/09, 22 nov. 2026): early payoff + layers (A1), "you" in the story (A2),
concrete world the camera travels (A3), groove music (A4), brand as place (A5), sources only on the end card (A6),
visible progress 1/3–3/3 (A7), share CTA with a concrete archetype (A8), 60–80 s (A10). No hook timer.
References (referencias.md): R1 experienciasdecompra OXXO (TT, 2.6M, seen 22 nov.), R2 margencerofr Musk challenge (TT, 1.3M, seen).
Keeps the promise made in 003 and 012 (break down GTA 6's real numbers)."""
SPEC = dict(
    id="005_gta6_dia_uno", lang="en-us", lang_tag="EN", voice="af_heart", speed=1.0,
    brand="WITH AN ASTERISK",
    world=dict(
        shops=[dict(kind="block", x=40, w=620, h=500, col=(44, 60, 124)),
               dict(kind="games", x=700, w=820, h=520, sign="GAMES", col=(255, 104, 88)),
               dict(kind="screens", x=1560, w=640, h=470, sign="CONSOLE STORE", col=(64, 206, 186)),
               dict(kind="block", x=2240, w=500, h=430, col=(184, 196, 220)),
               dict(kind="tower", x=2780, w=700, h=540, sign="TAKE-TWO", col=(44, 60, 124))],
        queue=dict(x0=880, n=6, gap=82), crosswalks=[1520]),
    camera=dict(push=0.03, enter=0.08, punch=["q", "a", "b", "nb", "who", "cut", "pre", "est", "ans", "fol", "like"],
                shake=["nb", "est", "ans"]),
    music=dict(style="groove", bpm=112, gain=0.17, duck=0.6, riser_scenes=["w_note"]),
    sfx=[],
    tail=2.5, card_dur=1.8, card_title="SOURCES",
    sources_card=["Take-Two 8-K, Nov. 20, 2026 (Exhibit 99.1)",
                  "Take-Two Q2 FY2027 results 8-K, Nov. 9, 2026",
                  "Why the numbers differ: our read"],
    beats=[
        dict(scene="w_hook", at=1180,
             p=dict(kicker="GTA 6 · LAUNCH WEEK", q1="GTA 6 MADE", q2="$3.79 BILLION", q3="IN ONE DAY.",
                    q4="ITS MAKER EXPECTED LESS FOR 3 MONTHS. HOW?"),
             lines=["{G.T.A. Six|GTA 6} made {three point seven nine billion dollars|$3.79 billion} in one day.",
                    "[#q] Its maker expected less than that for three whole months. How?"]),
        dict(scene="w_board", at=2490,
             p=dict(kicker="ONE DAY VS. THREE MONTHS", title="ONE DAY BEAT A QUARTER?",
                    rows=[dict(label="NOV. 19 · ONE DAY", v=3.79, val="$3.79B", col=(255, 210, 63), cue="a"),
                          dict(label="OCT.–DEC. · TAKE-TWO'S FORECAST", v=3.5, val="$3.35–3.5B", col=(64, 206, 186), cue="b")],
                    stamp="NOT THE SAME MONEY"),
             lines=["[#a] One day: three point seven nine billion.",
                    "[#b] Its forecast for October to December: up to three and a half.",
                    "[#nb] Short answer: it's not the same money."]),
        dict(scene="w_layer", at=1180,
             p=dict(kicker="COUNTER 1", n=1, of=3, title="WHAT YOU PAID", anim="register",
                    who="$3.79B = RETAIL SALES", who_sub="WHAT PLAYERS PAID, AT EVERY STORE"),
             lines=["[#who] The three point seven nine billion is retail sales: what players paid.",
                    "At every store. PlayStation, Xbox, Rockstar's own store, and the shops."]),
        dict(scene="w_layer", at=2420,
             p=dict(kicker="COUNTER 2", n=2, of=3, title="WHAT REACHES TAKE-TWO", anim="split", from_x=2080, to_x=2950,
                    who="FORECAST = TAKE-TWO'S OWN SALES", who_sub="CALLED NET BOOKINGS",
                    cut_txt="STORES AND CONSOLES TAKE A PIECE"),
             lines=["[#who] The forecast counts something else: Take-Two's own sales.",
                    "[#cut] And stores and console makers keep a piece of what you pay."]),
        dict(scene="w_layer", at=3130,
             p=dict(kicker="AND THE TIMING", n=3, of=3, title="FORECAST: NOV. 9", anim="stack",
                    who="10 DAYS BEFORE LAUNCH", pre_big="32.5 MILLION", pre_sub="COPIES SOLD BEFORE LAUNCH · A RECORD"),
             lines=["[#who] Plus, that forecast came out on November ninth. Ten days before launch.",
                    "[#pre] And before launch, it had already sold thirty-two and a half million copies. A record."]),
        dict(scene="w_note", at=2490,
             p=dict(kicker="THE ASTERISK", title="THE PRESS RELEASE HAS ONE TOO",
                    head="TAKE-TWO · NOV. 20, 2026", line="DAY ONE RETAIL SALES*: $3.79B",
                    foot="*BASED ON COMPANY ESTIMATES", est_txt="THE COMPANY'S OWN ESTIMATE"),
             lines=["And the best part? Take-Two's press release has its own asterisk.",
                    "[#est] Three point seven nine billion is the company's own estimate."]),
        dict(scene="w_answer", at=1900,
             p=dict(kicker="THE ANSWER", ask="ONE DAY BEAT 3 MONTHS?", icon="none", tag="OUR READ",
                    ans1="NO. TWO COUNTERS:", ans2="WHAT YOU PAID ≠ WHAT IT GETS",
                    follow="+ FOLLOW", follow_sub="Send this to the friend who hasn't left his room since Thursday",
                    like_txt="FOLLOW FOR THE NEXT ASTERISK"),
             lines=["[#ask] So did one day beat three months?",
                    "[#ans] No. Two different counters: what you paid, and what reaches Take-Two.",
                    "Our read: how much really gets there, we'll see in its next report.",
                    "[#fol] Send this to the friend who hasn't left his room since Thursday.",
                    "[#like] Follow for the next asterisk."]),
    ],
    post=dict(
        tiktok=("GTA 6 made $3.79 billion in one day. The company behind it expected less for three whole months. How?\n\n"
                "Sources: Take-Two 8-K, Nov. 20, 2026 (Exhibit 99.1): \"day one retail sales* reached $3.79 billion\", "
                "\"*based on company estimates through end of day November 19th worldwide\"; \"sold 32.5 million units "
                "pre-release\". Take-Two Q2 FY2027 results 8-K, Nov. 9, 2026: net bookings outlook for Oct.–Dec. 2026 of "
                "$3.35–3.5 billion. Retail sales (what players paid) and net bookings (Take-Two's own sales) are different "
                "measures; Take-Two doesn't publish how one converts into the other, so the explanation is our read. "
                "Not affiliated with Take-Two or Rockstar. Not investment advice.\n\n"
                "#gta6 #gta #business #money #videogames"),
        title="GTA 6 made $3.79B in one day. How?",
    ),
)

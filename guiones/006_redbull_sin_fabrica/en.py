"""006 · Red Bull sold 14 billion cans. It filled zero. So what does it do? — English (With an Asterisk). Engine v2 + illus.
References (referencias.md): R1 matiasherediaa1 (59x, seen), R2 zamora_jose7 (157x), R3 brayanjacksonclub (76.9x, seen).
Patterns (doc 03): P2 number in frame 1, P9 visible 1/4 counter, P7 illustrated explainer, C2 share close.
Variable under test: illustrated scenes in our own style (illus.py) instead of loose icons.
Rules: generic can in our colors, no Red Bull logo or trade dress, no team liveries, no known characters, no photos.
Red Bull doesn't publish marketing spend or profit: never give a number for either."""
SRC_RB = "Red Bull company profile (redbull.com), 2025 figures"
SRC_RAUCH = "Rauch company history (rauch.cc); Rauch sustainability report 2023"
SRC_CAN = "City of Concord, NC (2021, Oct. 2025): Ball makes the cans"
SRC_TRIP = "Red Bull, 'Lifecycle of the can' (redbull.com)"
SRC_US = "City of Concord (Oct. 2025); NC Commerce (2021); Glendale/ACA (2019)"
SPEC = dict(
    id="006_redbull_sin_fabrica", lang="en-us", lang_tag="EN", voice="af_heart", speed=1.0,
    brand="WITH AN ASTERISK", theme="volt", hook_timer=True,
    camera=dict(push=0.04, enter=0.10, punch=["zero", "cans", "sec", "rev", "who", "nb", "ath", "f1", "ctry", "quote",
                                              "az", "nc", "rb", "ask", "ans", "fol", "like"],
                shake=["zero", "nb", "rb", "ans"]),
    music=dict(bpm=100, cut="nb", riser_scenes=["reveal2"], gain=0.20, duck=0.55),
    sfx=[],
    beats=[
        dict(scene="can_hook", src="Red Bull (redbull.com) · Rauch (rauch.cc)",
             p=dict(kicker="RED BULL · LAST YEAR", q1="RED BULL SOLD", q2="14 BILLION CANS.", q3="IT FILLED ZERO.",
                    q4="SO WHAT DOES IT DO?", stamp="0 FILLED"),
             lines=["Red Bull sold almost {fourteen billion|14 billion} cans last year.",
                    "[#zero] It didn't fill a single one.",
                    "So what does Red Bull actually do?"]),
        dict(scene="can_mountain", src=SRC_RB + " · per second: our math",
             p=dict(kicker="RED BULL · 2025", big="{:.3f} BILLION", big_l="CANS SOLD IN 2025",
                    sec="≈443 CANS / SECOND", tag="OUR MATH", rev="€12.2B IN SALES"),
             lines=["[#cans] Almost fourteen billion.",
                    "[#sec] That's about {four hundred forty-three|443} cans every second. Our math.",
                    "[#rev] Twelve point two billion euros in sales."]),
        dict(scene="chain_step", src=SRC_CAN,
             p=dict(kicker="FOLLOW THE CAN", n=1, title="THE CAN", ill="canmaker", who="BALL",
                    who_sub="A PACKAGING COMPANY · U.S. PLANTS", labels=["CAN", "DRINK", "TRIP", "???"]),
             lines=["Follow the can. Step one: the aluminum can.",
                    "[#who] In its {U.S.|US} plants, it's made by Ball, a packaging company."]),
        dict(scene="chain_step", src=SRC_RAUCH,
             p=dict(kicker="FOLLOW THE CAN", n=2, title="THE DRINK", ill="filler", who="RAUCH",
                    who_sub="AN AUSTRIAN JUICE COMPANY · SINCE 1987", labels=["CAN", "DRINK", "TRIP", "???"]),
             lines=["Step two: the drink.",
                    "[#who] It's filled by Rauch, an Austrian juice company. Since the very first batch, in 1987."]),
        dict(scene="chain_step", src=SRC_TRIP,
             p=dict(kicker="FOLLOW THE CAN", n=3, title="THE TRIP", ill="ship", who="RAIL + SHIP",
                    who_sub="FROM AUSTRIA & SWITZERLAND TO 170+ COUNTRIES", labels=["CAN", "DRINK", "TRIP", "???"]),
             lines=["Step three: the trip.",
                    "[#who] From Austria and Switzerland, by rail or ship, to over {a hundred seventy|170} countries."]),
        dict(scene="interrupt", src="",
             p=dict(lines=["NONE OF IT", "IS RED BULL."], hot=[1], ys=[700, 860]),
             lines=[dict(text="[#nb] Three steps. None of them is Red Bull.", pause=0.35)]),
        dict(scene="world_spend", src=SRC_RB,
             p=dict(kicker="SO WHERE IS RED BULL?", title="HERE.", n1="900+", l1="ATHLETES, ARTISTS & TEAMS",
                    n2="2", l2="FORMULA ONE TEAMS", n3="178", l3="COUNTRIES"),
             lines=["So where is Red Bull?",
                    "[#ath] Behind over nine hundred athletes, artists and teams.",
                    "[#f1] Two Formula One teams.",
                    "[#ctry] On shelves in {a hundred seventy-eight|178} countries."]),
        dict(scene="reveal2", src=SRC_US,
             p=dict(title="THE ASTERISK", qlines=["IN THE U.S., IT DID", "PUT MONEY IN PLANTS."], hot=[1]),
             lines=["Here's the asterisk. [#quote] In the {U.S.|US}, Red Bull did put money into plants."]),
        dict(scene="campus", src=SRC_US,
             p=dict(kicker="SHARED WITH RAUCH AND BALL", pin1="ARIZONA · 2021", pin2="N. CAROLINA · 2028",
                    b1="CANS", w1="BALL", b2="FILLING", w2="RAUCH", b3="WAREHOUSE", w3="RED BULL",
                    rb="RED BULL'S PART: THE WAREHOUSE"),
             lines=["Two campuses, [#az] in Arizona [#nc] and North Carolina.",
                    "Ball makes the cans. Rauch fills them.",
                    "[#rb] Red Bull's part in North Carolina: the warehouse."]),
        dict(scene="answer_track", src="Our read, based on Red Bull, Rauch and city filings", src_color=(255, 210, 63),
             p=dict(kicker="THE ANSWER", ask="WHAT DOES IT DO?", icon="none", tag="OUR READ",
                    ans1="IT MAKES THE REASON", ans2="YOU BUY IT.", labels=["CAN", "DRINK", "TRIP", "THE REASON"],
                    follow="+ FOLLOW", follow_sub="Send this to the friend who runs on Red Bull",
                    like_txt="LIKE FOR THE NEXT ASTERISK"),
             lines=["[#ask] So what does Red Bull actually do? Our read: it doesn't make the drink.",
                    "[#ans] It makes the reason you buy it.",
                    "[#fol] Send this to the friend who runs on Red Bull.",
                    "[#like] Follow and like for the next one."]),
    ],
    post=dict(
        tiktok=("Red Bull sold almost 14 billion cans last year. It didn't fill a single one. So what does it actually do?\n\n"
                "Sources: Red Bull company profile (13.969 billion cans and €12.196 billion turnover in 2025) and 'Lifecycle of the can' "
                "(redbull.com); Rauch company history and 2023 sustainability report (rauch.cc); City of Concord, NC (2021 and Oct. 2025); "
                "NC Commerce (July 2021); City of Glendale / Arizona Commerce Authority (March 2019). 443 cans per second is our math "
                "(13.969B / seconds in a year). Ball making the cans refers to the U.S. plants. Red Bull doesn't publish marketing spend. "
                "'It makes the reason you buy it' is our read. Not affiliated with Red Bull, Rauch or Ball.\n\n"
                "#redbull #business #marketing #money #brands"),
        title="Red Bull sold 14B cans. It filled zero.",
    ),
)

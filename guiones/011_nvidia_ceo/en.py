"""011 · Could what happened to Jensen Huang happen to Zuckerberg? — English (With an Asterisk). Engine v2.
Patterns (doc 03): P8 two numbers that clash, P3, P4 news of the week, P7. Tone rule: only what the release and the board said."""
TEAL, YEL = (70, 230, 225), (255, 210, 63)
SRC_8K = "Nvidia CEO transition release (8-K), Nov. 12, 2026"
SRC_CALL = "Nvidia board chair on the Nov. 17 call, via NPR"
SRC_Q3 = "Nvidia Q3 FY2027 results (8-K), Nov. 17, 2026"
SRC_META = "Meta proxy statement (DEF 14A), Apr. 2026"
SPEC = dict(
    id="011_nvidia_ceo", lang="en-us", lang_tag="EN", voice="af_heart", speed=1.05,
    brand="WITH AN ASTERISK", theme="board", hook_timer=True,
    camera=dict(push=0.04, enter=0.10, punch=["no", "stamp", "grow", "last", "c1", "c2", "c3", "foot", "count", "chips", "rev", "quote", "ans", "fol", "like"],
                shake=["no", "stamp", "cut", "c2", "ans"]),
    music=dict(bpm=92, cut="cut", riser_scenes=["reveal2"], gain=0.20, duck=0.55),
    sfx=[],
    beats=[
        dict(scene="ballot_hook", src=SRC_8K + " · " + SRC_CALL,
             p=dict(kicker="NVIDIA · NOV. 17", q1="NVIDIA JUST TOLD ITS CEO NO.", q2="WHY CAN'T ANYONE TELL", q3="ZUCKERBERG NO?",
                    sales="NVIDIA'S BOARD: NO", stamp="NO"),
             lines=["Nvidia's board just told its own {C.E.O.|CEO} [#no] no.",
                    "Why can't anyone tell Mark Zuckerberg no?"]),
        dict(scene="classified", src=SRC_8K,
             p=dict(kicker="NOV. 12, 2026", doc="CEO TRANSITION", stamp="RESIGNED", mystery="EFFECTIVE IMMEDIATELY",
                    quote="CEO AND BOARD SEAT", attr="FOLLOWED A DISCLOSURE ABOUT PERSONAL CONDUCT"),
             lines=["On {November twelfth,|Nov. 12,} Jensen Huang [#stamp] resigned as Nvidia's {C.E.O.|CEO} and left the board, effective immediately.",
                    "[#sub] The company says it followed a disclosure about his personal conduct."]),
        dict(scene="bars2", src=SRC_Q3 + " · our math",
             p=dict(kicker="NVIDIA · LAST QUARTER", v1=65.3, v2=115.8, fmt="${:.1f}B", labels=["PROFIT", "REVENUE"],
                    labels2=["NET INCOME", "3 MONTHS"], badge="≈ $8,300 EVERY SECOND"),
             lines=["Five days later, Nvidia reported its quarter.",
                    "[#grow] {One hundred fifteen point eight billion dollars|$115.8 billion} in revenue.",
                    "[#last] {Sixty-five point three billion|$65.3 billion} in profit.",
                    "That's about {eight thousand three hundred dollars|$8,300} every second."]),
        dict(scene="interrupt", src="",
             p=dict(lines=["HE WANTED", "TO COME", "BACK."], hot=[2]),
             lines=[dict(text="[#cut] Huang said he'd be honored to come back.", pause=0.45)]),
        dict(scene="classified", src=SRC_CALL,
             p=dict(kicker="THE BOARD'S ANSWER", doc="BOARD STATEMENT", stamp="NOT REINSTATED", mystery="UNANIMOUS",
                    quote="“DOES NOT INTEND TO REINSTATE JENSEN AS CEO”", attr="NVIDIA BOARD CHAIR, NOV. 17, 2026"),
             lines=["[#stamp] The board's answer:",
                    "[#sub] it does not intend to reinstate Jensen as {C.E.O.|CEO}"]),
        dict(scene="certs", src="Nvidia 8-K cover page and proxy statements",
             p=dict(kicker="NVIDIA · FOLLOW THE VOTES", sub="NVDA · COMMON STOCK",
                    cards=[("1 SHARE", "1 VOTE", TEAL, 1.0), ("1 SHARE", "1 VOTE", TEAL, 1.0), ("1 SHARE", "1 VOTE", TEAL, 1.0)],
                    foot="THE BOARD ANSWERS TO ALL OF THEM"),
             lines=["[#c1] Nvidia has one kind of stock on the Nasdaq.",
                    "[#c2] Every share votes [#c3] the same.",
                    "[#foot] The board answers to all of them."]),
        dict(scene="certs", src=SRC_META,
             p=dict(kicker="META · BUILT DIFFERENTLY", sub="META · COMMON STOCK",
                    cards=[("CLASS A", "1 VOTE", TEAL, 1.0), ("CLASS B", "10 VOTES", YEL, 1.12)], hot=[1],
                    caps=["THE ONES YOU CAN BUY", "99.8% OWNED BY ZUCKERBERG"], foot="ZUCKERBERG: 60.8% OF ALL VOTES"),
             lines=["Meta is built differently.",
                    "[#c1] Class A shares, the ones you can buy: one vote each.",
                    "[#c2] Class B shares: ten votes each.",
                    "Zuckerberg owns {ninety-nine point eight percent|99.8%} of Class B.",
                    "[#foot] That's {sixty point eight percent|60.8%} of all the votes."]),
        dict(scene="reveal2", src="Meta 8-K, May 29, 2026",
             p=dict(title="THE ASTERISK", qlines=["MAY 2026:", "ONE SHARE, ONE VOTE?", "IT FAILED."], hot=[2]),
             lines=["[#rev] In May, shareholders voted on giving every share an equal vote.",
                    "[#quote] It failed."]),
        dict(scene="ring2", src="Meta 8-K (May 29, 2026) and proxy · our math", src_color=(255, 210, 63),
             p=dict(kicker="THE VOTE WITHOUT ZUCKERBERG", pct=85, fmt="{:.0f}%", l1="OF THE REMAINING VOTES SAID YES",
                    chips=["OUR MATH", "STILL FAILED"]),
             lines=["But take out Zuckerberg's votes,",
                    "[#count] and about {eighty-five percent|85%} of the remaining votes said yes.",
                    "[#chips] That's our math."]),
        dict(scene="answer_cta", src="Our read, based on the companies' filings", src_color=(255, 210, 63),
             p=dict(kicker="THE ANSWER", ask="WHY CAN'T ANYONE TELL HIM NO?", icon="ballot", tag="OUR READ",
                    ans1="60.8% OF THE VOTES.", ans2="HE PICKS THE BOARD.", follow="+ FOLLOW",
                    follow_sub="Who should we break down next?", like_txt="LIKE FOR THE NEXT ASTERISK"),
             lines=["[#ask] So why can't anyone tell Zuckerberg no?",
                    "[#ans] Our read: with {sixty point eight percent|60.8%} of the votes, he picks the board. At Nvidia, the board could tell its founder no.",
                    "Same title. Very different job.",
                    "[#fol] Who should we break down next? Follow,",
                    "[#like] and like for the next one."]),
    ],
    post=dict(
        tiktok=("Nvidia's board just told its own CEO no. Why can't anyone tell Mark Zuckerberg no?\n\n"
                "Sources: Nvidia CEO transition release (8-K, Nov. 12, 2026); Nvidia board chair on the Nov. 17 earnings call (via NPR); "
                "Nvidia Q3 FY2027 results (8-K, Nov. 17, 2026); Nvidia proxy statements (one vote per share); "
                "Meta proxy statement (DEF 14A, Apr. 2026); Meta 8-K with the May 27, 2026 vote results. "
                "The $8,300 per second and the 85% are our own math (the 85% assumes Zuckerberg voted all his shares against). "
                "The comparison is our read. Not investment advice.\n\n"
                "#nvidia #meta #business #money #stocks"),
        title="Why can't anyone tell Zuckerberg no?",
    ),
)

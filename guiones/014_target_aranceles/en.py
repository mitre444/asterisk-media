"""014 · Target just got $301 million back in tariffs. Who refunds you? — English (With an Asterisk). Engine v2 + illus + tariff.
References (referencias.md): R1 oddstickout (30.3x, seen) story with characters + a legal rule that flips it;
R2 keetonlive (21.2x) "refund" reframing; R3 brayanjacksonclub (76.9x) visible counter + share CTA.
Patterns (doc 03): P2 number in frame 1, P3 legal-but-unfair, P4 news of the week, P9 1/4 counter, C2 share close.
Variable under test: story narration with generic characters (R1's method). Illustrated style stays as in 006.
Rules: generic store, no Target logo/colors, no real people drawn. Neutral on tariffs: only who gets the refund."""
SRC_TGT = "Target 8-K, Q3 2026 results (Nov. 18, 2026), SEC EDGAR"
SRC_CBP = "U.S. Customs and Border Protection, CSMS messages on IEEPA refunds (CAPE)"
SRC_SC = "Learning Resources, Inc. v. Trump (U.S. Supreme Court, Feb. 20, 2026)"
LAB = ["CUSTOMS", "SHELF", "YOU", "REFUND"]
SPEC = dict(
    id="014_target_aranceles", lang="en-us", lang_tag="EN", voice="af_heart", speed=1.0,
    brand="WITH AN ASTERISK", theme="volt", hook_timer=True,
    camera=dict(push=0.04, enter=0.10, punch=["you", "big", "pct", "ytd", "who", "rule", "power", "nb", "quote", "val",
                                              "not", "ask", "ans", "fol", "like"],
                shake=["you", "rule", "nb", "not", "ans"]),
    music=dict(bpm=100, cut="nb", riser_scenes=["reveal2"], gain=0.20, duck=0.55),
    sfx=[],
    beats=[
        dict(scene="refund_hook", src=SRC_TGT,
             p=dict(kicker="TARGET · THIS WEEK", q1="TARGET JUST GOT", q2="$301 MILLION", q3="BACK IN TARIFFS.",
                    q4="WHO REFUNDS YOU?", stamp="YOU: ?", amount="$301,000,000", to="TARGET"),
             lines=["Target just got {three hundred one million dollars|$301 million} back in tariffs.",
                    "[#you] So who refunds you?"]),
        dict(scene="big_refund", src=SRC_TGT + " · 18%: our math",
             p=dict(kicker="TARGET · Q3 REPORT · NOV. 18", big="${:.0f} MILLION", n=301,
                    big_l="IN TARIFF REFUNDS · ONE QUARTER", pct="≈18% OF ITS OPERATING PROFIT", tag="OUR MATH",
                    ytd="$1.3 BILLION SO FAR IN 2026", amount="$301,000,000", to="TARGET"),
             lines=["It's right there in its quarterly report.",
                    "[#big] Three hundred one million dollars.",
                    "[#pct] About eighteen percent of its operating profit. Our math.",
                    "[#ytd] And one point three billion so far this year."]),
        dict(scene="tariff_step", src=SRC_CBP,
             p=dict(kicker="FOLLOW ONE DOLLAR", n=1, title="AT THE PORT", ill="customs", who="THE IMPORTER PAYS",
                    who_sub="THE TARIFF GOES TO U.S. CUSTOMS", labels=LAB),
             lines=["You see, follow one dollar. Step one: a box arrives from overseas.",
                    "[#who] At the port, whoever imports it pays the tariff to {U.S.|US} Customs.",
                    "Big chains often import it themselves."]),
        dict(scene="tariff_step", src="",
             p=dict(kicker="FOLLOW ONE DOLLAR", n=2, title="ON THE SHELF", ill="shelf", who="THE PRICE CAN GO UP",
                    who_sub="TO COVER THAT COST", tag_old="$", tag_new="$$", labels=LAB),
             lines=["Step two: the shelf.",
                    "[#who] To cover that cost, the price can go up."]),
        dict(scene="tariff_step", src="",
             p=dict(kicker="FOLLOW ONE DOLLAR", n=3, title="AT THE REGISTER", ill="register", who="YOU PAY THE PRICE",
                    who_sub="THE TARIFF WAS PAID BACK AT CUSTOMS", labels=LAB),
             lines=["Step three: you.",
                    "[#who] At the register, you pay that price."]),
        dict(scene="court_hit", src=SRC_SC,
             p=dict(kicker="FEBRUARY 20, 2026", title="THE SUPREME COURT", stamp="6–3",
                    l1="NO POWER TO IMPOSE THEM", l2="LEARNING RESOURCES V. TRUMP · IEEPA TARIFFS"),
             lines=["Then, in February, [#rule] the Supreme Court ruled, six to three:",
                    "[#power] the president didn't have the power to impose those tariffs."]),
        dict(scene="interrupt", src="",
             p=dict(lines=["THE MONEY GOES BACK.", "BUT TO WHOM?"], hot=[1], ys=[700, 860]),
             lines=[dict(text="[#nb] So the money has to go back. But to whom?", pause=0.35)]),
        dict(scene="reveal2", src=SRC_CBP,
             p=dict(title="THE ASTERISK", qlines=["IT'S NOT AUTOMATIC.", "THE IMPORTER FILES A CLAIM."], hot=[1]),
             lines=["Here's the asterisk. [#quote] The refund isn't automatic.",
                    "Whoever paid at customs has to file a claim, in a Customs system called {CAPE|CAPE}."]),
        dict(scene="report_note", src=SRC_TGT,
             p=dict(kicker="TARGET'S REPORT", title="AND THE SHOPPERS?", val="BOOKED AS LOWER COSTS",
                    stamp="PASS IT ON? NOT SAID", l2="THE REPORT DOESN'T SAY IT GOES BACK TO SHOPPERS"),
             lines=["And Target's report? [#val] It books the refund as lower costs.",
                    "[#not] It doesn't say it will pass it on to shoppers."]),
        dict(scene="answer_refund", src="Our read, based on CBP and Target's 8-K", src_color=(255, 210, 63),
             p=dict(kicker="THE ANSWER", ask="WHO REFUNDS YOU?", icon="none", tag="OUR READ",
                    ans1="NOBODY, AUTOMATICALLY.", ans2="IT GOES TO THE IMPORTER.", labels=LAB,
                    amount="REFUND", to="IMPORTER",
                    follow="+ FOLLOW", follow_sub="Send this to someone who paid more this year",
                    like_txt="LIKE FOR THE NEXT ASTERISK"),
             lines=["[#ask] So who refunds you?",
                    "[#ans] Nobody, automatically. It goes to whoever paid at customs.",
                    "Our read: if you ever see it, it'll be as a lower price. And that's each company's call.",
                    "[#fol] Send this to someone who paid more this year.",
                    "[#like] Follow and like for the next one."]),
    ],
    post=dict(
        tiktok=("Target just got $301 million back in tariffs. So who refunds you?\n\n"
                "Sources: Target 8-K, Q3 2026 results (Nov. 18, 2026): $301M pretax IEEPA tariff refunds in the quarter, "
                "$1.3B in 2026 through Oct. 31, booked as a reduction of cost of sales; operating income $1,672M "
                "(18% is our math). Learning Resources, Inc. v. Trump (U.S. Supreme Court, Feb. 20, 2026, 6–3). "
                "U.S. Customs and Border Protection CSMS messages on IEEPA refunds and CAPE: refunds go to the importer of record, "
                "who must file a claim. Target's release doesn't say the refunds will be passed on to shoppers. "
                "'If you see it, it'll be as a lower price' is our read. Not affiliated with Target. Not legal or tax advice.\n\n"
                "#target #tariffs #business #money #news"),
        title="Target got $301M back in tariffs. Who refunds you?",
    ),
)

"""009 · Amazon's Black Friday "deal" cost more than nine days earlier. So is Black Friday actually cheaper? — English.
Standard v3 (guide 02). References (referencias.md): R1 @groundworkcollab (IG, 133K, 31.6x), R2 @outspokenedits (TT, 167K, 31.5x).
Sources: Groundwork Collaborative (Nov. 16, 2026), Amazon's reply (Nov. 16, 2026), Which? (Nov. 25, 2025), Adobe (2025 recap; 2026 forecast)."""
SPEC = dict(
    id="009_black_friday", lang="en-us", lang_tag="EN", voice="af_heart", speed=1.0,
    brand="WITH AN ASTERISK",
    world=dict(
        shops=[dict(kind="block", x=40, w=600, h=480, col=(44, 60, 124), billboard=["BLACK FRIDAY", "UP TO 70% OFF"]),
               dict(kind="store", x=680, w=820, h=520, sign="SHOE STORE", col=(255, 104, 88)),
               dict(kind="screens", x=1540, w=640, h=470, sign="ELECTRONICS", col=(64, 206, 186)),
               dict(kind="block", x=2220, w=520, h=430, col=(184, 196, 220)),
               dict(kind="tower", x=2780, w=700, h=540, sign="AMAZON", col=(44, 60, 124))],
        queue=dict(x0=860, n=6, gap=82), crosswalks=[1500]),
    camera=dict(push=0.03, enter=0.08, punch=["q", "a", "b", "nb", "who", "cut", "est", "ans", "fol", "like"],
                shake=["nb", "est", "ans"]),
    music=dict(style="groove", bpm=112, gain=0.17, duck=0.6, riser_scenes=["w_note"]),
    sfx=[],
    tail=2.5, card_dur=1.8, card_title="SOURCES",
    sources_card=["Groundwork Collaborative, Nov. 16, 2026",
                  "Amazon, \"Correcting the record\", Nov. 16, 2026",
                  "Which?, Nov. 25, 2025 · Adobe, 2025 recap",
                  "Final answer: our read"],
    beats=[
        dict(scene="w_hook", at=1090,
             p=dict(kicker="AMAZON · BLACK FRIDAY 2025", q1="RAIN BOOTS \"ON SALE\":", q2="$126.99", q3="9 DAYS EARLIER: $79.97",
                    q4="SO IS BLACK FRIDAY CHEAPER?"),
             lines=["Amazon put these rain boots on sale for Black Friday: {a hundred twenty-seven dollars|$126.99}.",
                    "Nine days earlier, they were {eighty|$79.97}.",
                    "[#q] So is Black Friday actually cheaper?"]),
        dict(scene="w_board", at=2470,
             p=dict(kicker="SAME BOOTS · 2025", title="THE \"DEAL\" COST MORE",
                    rows=[dict(label="9 DAYS BEFORE", v=79.97, val="$79.97", col=(64, 206, 186), cue="a"),
                          dict(label="BLACK FRIDAY \"DEAL\"", v=126.99, val="$126.99", col=(255, 210, 63), cue="b")],
                    stamp="+59%", stamp_pill=True),
             lines=["[#a] Nine days before: eighty.",
                    "[#b] The deal: a hundred twenty-seven. Fifty-nine percent more.",
                    "[#nb] Short answer: a discount is measured against a price. And the store picks that price."]),
        dict(scene="w_layer", at=1090,
             p=dict(kicker="351 AMAZON DEALS", n=1, of=3, title="1 IN 3", anim="register",
                    who="SAME PRICE OR LESS A MONTH BEFORE", who_sub="AND NEARLY 1 IN 10 COST MORE DURING THE SALE"),
             lines=["A think tank checked three hundred fifty-one deals from Amazon's Black Friday pages.",
                    "[#who] Nearly one in three cost the same or less the month before. Nearly one in ten cost more."]),
        dict(scene="w_layer", at=3000,
             p=dict(kicker="AMAZON'S REPLY", n=2, of=3, title="\"FLAWED AND FALSE\"", anim="split", from_x=2350, to_x=3130,
                    who="98%: SAME OR LOWER THAN 30 DAYS", who_sub="350 OUT OF 10 MILLION+ DEALS, IT SAYS",
                    cut_txt="BY ITS OWN COUNT: 1 IN 10 = SAME PRICE"),
             lines=["Amazon calls that flawed: three hundred fifty items out of ten million deals.",
                    "[#who] It says ninety-eight percent were the same or lower than the past thirty days.",
                    "[#cut] But by its own count, one in ten of those 2025 deals was just... the same price."]),
        dict(scene="w_layer", at=1860,
             p=dict(kicker="ONE FULL YEAR · UK", n=3, of=3, title="0 OF 175",
                    who="CHEAPEST OF THE YEAR ON BLACK FRIDAY", who_sub="WHICH?, A BRITISH CONSUMER GROUP · 2024 SALES"),
             lines=["A British consumer group tracked a hundred seventy-five deals for a whole year.",
                    "[#who] Not one was at its cheapest of the year on Black Friday."]),
        dict(scene="w_note", at=2470,
             p=dict(kicker="THE ASTERISK", title="AND YET: THE MOST DISCOUNTED DAY",
                    head="ADOBE · U.S. ONLINE, 2025", line="BLACK FRIDAY: −23.7%*",
                    foot="*AVERAGE, OFF THE LISTED PRICE", est_txt="THE PRICE THE STORE CHOOSES"),
             lines=["The twist? Adobe says Black Friday really is the most discounted day online: twenty-three point seven percent off, on average.",
                    "[#est] Off the listed price. The one the store chooses."]),
        dict(scene="w_answer", at=1180,
             p=dict(kicker="THE ANSWER", ask="IS BLACK FRIDAY CHEAPER?", icon="none", tag="OUR READ",
                    ans1="CHEAPER THAN THE TAG.", ans2="NOT ALWAYS THAN LAST MONTH",
                    follow="+ FOLLOW", follow_sub="Send this to the friend whose cart has been full since Halloween",
                    like_txt="FOLLOW FOR THE NEXT ASTERISK"),
             lines=["[#ask] So, is Black Friday actually cheaper?",
                    "[#ans] Our read: cheaper than the tag, yes. Than last month, not always. Check the price history first.",
                    "[#fol] Send this to the friend whose cart has been full since Halloween.",
                    "[#like] Follow for the next asterisk."]),
    ],
    post=dict(
        tiktok=("Amazon's Black Friday \"deal\" on these boots: $126.99. Nine days earlier: $79.97. So is Black Friday actually cheaper?\n\n"
                "Sources: Groundwork Collaborative, \"Amazon's Decoy Deals\" (Nov. 16, 2026): 350+ products from Amazon's Black Friday "
                "and Cyber Monday deal pages, 2024–2025; nearly 1 in 3 sold for the same or less the month before, nearly 1 in 10 cost more; "
                "example: Hunter Women's Short Rain Boots, $126.99 on Black Friday 2025 vs $79.97 nine days earlier. "
                "Amazon, \"Correcting the record about Amazon's deal-event pricing\" (Nov. 16, 2026): calls the report flawed; "
                "350 of 10M+ deals; 98% same or lower than the past 30 days; for 2025, 89% lower and 10% the same. "
                "Which? (Nov. 25, 2025): 175 Black Friday 2024 deals tracked May 2024–May 2025; none at their cheapest of the year on Black Friday. "
                "Adobe 2025 Holiday Shopping Recap: Black Friday was the most discounted day of the season online (−23.7% average); "
                "Adobe states discounts off listed price (2026 forecast, Sept. 28, 2026). "
                "\"Cheaper than the tag, not always than last month\" is our read. Not affiliated with Amazon. Not financial advice.\n\n"
                "#blackfriday #amazon #deals #money #shopping"),
        title="Is Black Friday actually cheaper?",
    ),
)

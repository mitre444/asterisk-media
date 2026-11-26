"""013 · Walmart keeps 3¢ per dollar. So why is it selling ads? — English (With an Asterisk). Engine v2.
Patterns (doc 03): P8 two numbers that clash (3¢ vs +37%), P2 number in frame 1, P4 news of the day, C2 share close.
Rule: Walmart doesn't disclose ad profit; never say it does. Generic objects only, no Walmart logo or brand colors."""
SRC_FY = "Walmart Q4 FY26 results (8-K, Feb. 19, 2026) and FY26 10-K"
SRC_Q3 = "Walmart Q3 FY27 earnings presentation (8-K), Nov. 19, 2026"
SRC_WC = "Walmart Connect (walmartconnect.com)"
SPEC = dict(
    id="013_walmart_anuncios", lang="en-us", lang_tag="EN", voice="af_heart", speed=1.0,
    brand="WITH AN ASTERISK", theme="vault", hook_timer=True,
    camera=dict(push=0.04, enter=0.10, punch=["ads", "s", "p", "cut", "buy", "last", "grow", "app", "scr", "pay", "count", "badge",
                                              "rev", "quote", "stamp", "sub", "ask", "ans", "fol", "like"],
                shake=["ads", "cut", "grow", "stamp", "ans"]),
    music=dict(bpm=96, cut="wcut", riser_scenes=["reveal2"], gain=0.20, duck=0.55),
    sfx=[],
    beats=[
        dict(scene="receipt_hook", src=SRC_FY + " · our math",
             p=dict(kicker="WALMART · TODAY'S EARNINGS", q1="WALMART KEEPS", q2="3¢ PER $1.", q3="SO WHY IS IT SELLING ADS?",
                    rows=[("CEREAL", "$1.00", False), ("TOTAL", "$1.00", False), ("STORE KEEPS", "3¢", True)], stamp="ADS?"),
             lines=["Walmart keeps about three cents of every dollar you spend there.",
                    "So why is it suddenly selling [#ads] ads?"]),
        dict(scene="dollar_split", src=SRC_FY + " · our math",
             p=dict(kicker="WALMART · LAST FISCAL YEAR", sales="$713.2B", sales_l="IN SALES", profit="$22.3B", profit_l="IN PROFIT",
                    bar_l="EVERY $1 YOU SPEND", rest="COSTS", keep="WALMART KEEPS ≈3¢", tag="OUR MATH"),
             lines=["[#s] Last year, Walmart sold {seven hundred thirteen billion dollars|$713 billion} of stuff.",
                    "[#p] Its profit: {twenty-two point three billion.|$22.3 billion.}",
                    "[#cut] That's roughly three cents per dollar. Our math."]),
        dict(scene="cereal_buy", src=SRC_FY,
             p=dict(kicker="THE GROCERY BUSINESS", price="$1.00", price_sub="YOU PAY", pay="WALMART BUYS IT FIRST"),
             lines=["Groceries are a brutal business.",
                    "Before Walmart can sell you a dollar of cereal, [#buy] it has to buy that cereal."]),
        dict(scene="bars2", src=SRC_Q3 + " · 7x: our math",
             p=dict(kicker="FOLLOW THE MONEY · TODAY", v1=5.2, v2=37, fmt="+{:.0f}%", labels=["SALES", "U.S. ADS"],
                    labels2=["TOTAL REVENUE, AUG.–OCT.", "WALMART U.S., AUG.–OCT."], badge="7X FASTER"),
             lines=["Today, Walmart reported its quarter.",
                    "[#last] Sales: up five percent.",
                    "[#grow] {U.S.|US} advertising: up thirty-seven percent."]),
        dict(scene="interrupt", src="",
             p=dict(lines=["WHAT", "ADS?"], hot=[1], ys=[700, 860]),
             lines=[dict(text="[#wcut] What ads?", pause=0.35)]),
        dict(scene="ad_spots", src=SRC_WC,
             p=dict(kicker="WHERE THE ADS ARE", query="cereal", tag="SPONSORED", l_app="IN THE APP", screen="NEW!",
                    l_scr="IN THE STORE", pay="BRANDS PAY"),
             lines=["[#app] The sponsored products at the top of your search in the Walmart app.",
                    "[#scr] The screens inside the store.",
                    "[#pay] Brands pay Walmart to be in front of you right when you're about to buy."]),
        dict(scene="tower", src=SRC_FY + " (includes VIZIO)",
             p=dict(kicker="WALMART'S AD BUSINESS · LAST FISCAL YEAR", pre="NEARLY", prefix="$", value=6400, mult=1e6,
                    sub="IN AD REVENUE", badge="+46% IN ONE YEAR", item="box", land=1.6),
             lines=["And it's not small.",
                    "[#count] Last year, Walmart's ad business brought in nearly {six point four billion dollars.|$6.4 billion.}",
                    "[#badge] Up forty-six percent."]),
        dict(scene="reveal2", src=SRC_FY,
             p=dict(title="THE ASTERISK", qlines=["THAT'S REVENUE,", "NOT PROFIT."], hot=[1]),
             lines=["[#rev] Here's the asterisk. [#quote] That's ad revenue, not profit."]),
        dict(scene="classified", src=SRC_Q3,
             p=dict(kicker="WALMART'S AD PROFIT", doc="AD BUSINESS · PROFIT", stamp="NOT DISCLOSED",
                    quote="“GROWTH OF DIGITAL ADVERTISING”", attr="WALMART, ON ITS U.S. MARGIN · NOV. 19, 2026"),
             lines=["[#stamp] Walmart doesn't say how much of it it keeps.",
                    "[#sub] But today it said its {U.S.|US} margin improved mainly from growth of digital advertising."]),
        dict(scene="answer_cta", src="Our read, based on Walmart's filings", src_color=(255, 210, 63),
             p=dict(kicker="THE ANSWER", ask="WHY SELL ADS?", icon="bills", tag="OUR READ",
                    ans1="YOU'RE NOT JUST", ans2="THE CUSTOMER.", follow="+ FOLLOW",
                    follow_sub="Send this to someone who shops at Walmart", like_txt="LIKE FOR THE NEXT ASTERISK"),
             lines=["[#ask] So why sell ads? Our read: selling you a dollar of cereal costs Walmart almost a dollar.",
                    "A dollar of ads costs it way less. [#ans] You're not just the customer. You're the audience.",
                    "[#fol] Send this to someone who shops at Walmart.",
                    "[#like] Follow and like for the next one."]),
    ],
    post=dict(
        tiktok=("Walmart keeps about 3¢ of every dollar it sells. So why is it selling ads?\n\n"
                "Sources: Walmart Q4 FY26 results (8-K, Feb. 19, 2026) and FY26 10-K; Walmart Q3 FY27 earnings presentation (8-K, Nov. 19, 2026); "
                "Walmart Connect. The 3¢ is our math (FY26 consolidated net income $22.3B / revenue $713.2B). \"Sales +5%\" is total revenue, +5.2%; "
                "\"ads +37%\" is Walmart U.S. advertising. The $6.4B in ad revenue includes VIZIO and is revenue, not profit: Walmart doesn't disclose ad profit. "
                "Why Walmart sells ads is our read. Not affiliated with Walmart. Not investment advice.\n\n"
                "#walmart #business #money #advertising #stocks"),
        title="Walmart keeps 3¢ per dollar. Why sell ads?",
    ),
)

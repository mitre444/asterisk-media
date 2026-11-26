"""001 · Costco's $1.50 hot dog — English (With an Asterisk)."""
YEL = (255, 210, 63)
BASE = dict(kicker="COSTCO · HOT DOG + SODA", price="$1.50", y0=1985, y1=2026)

SPEC = dict(
    id="001_costco_hotdog", lang="en-us", lang_tag="EN", voice="af_heart", speed=1.0,
    brand="WITH AN ASTERISK",
    lexicon={"Jelinek": "Jelinnek", "Sinegal": "Sinnigal"},
    sfx=[("ast", "ding", 0.0), ("rev", "thump", 0.0), ("rev", "ding", 0.06)],
    beats=[
        dict(scene="hook", src="Costco: same price since 1985", p=dict(BASE, rewind_dur=1.9), lines=[
            "Costco's hot dog combo costs {a dollar fifty.|$1.50.}",
            "[#rewind] It cost {a dollar fifty|$1.50} in {nineteen eighty-five.|1985.}",
            "And the reason has almost [#ast] nothing to do with hot dogs.",
        ]),
        dict(scene="bars", src="BLS CPI-U: 1985 average vs. Sept. 2026",
             p=dict(kicker="IF IT HAD TRACKED INFLATION", v1=1.50, v2=4.70, fmt="${:.2f}", l1="ACTUAL PRICE",
                    l2="WITH INFLATION", badge="3.1×", grow_dur=1.3),
             lines=["If the price had kept up with inflation, [#grow] it would be about {four dollars and seventy cents.|$4.70.}"]),
        dict(scene="people", src="C. Jelinek in 425 Business (2018)",
             p=dict(kicker="INSIDE COSTCO", n1="CRAIG JELINEK", r1="Executive · later CEO", i1="CJ", n2="JIM SINEGAL", r2="Co-founder", i2="JS",
                    bubble=["“We can't sell this hot dog", "for a buck fifty.”"]),
             lines=[
                 "One executive [#say] tried to raise it.",
                 "[#pre] Craig Jelinek, who later became CEO, says he told [#p2] co-founder Jim Sinegal they were losing money on it.",
             ]),
        dict(scene="quote", src="425 Business (2018)",
             p=dict(kicker="HIS ANSWER", breaks=[3, 2, 2, 4, 3], hot=1,
                    attr1="— JIM SINEGAL, co-founder", attr2="as recalled by Craig Jelinek"),
             lines=[
                 dict(text="Sinegal's answer, as Jelinek tells it:", pause=0.22),
                 dict(text="{If|“If} you raise the effing hot dog, I will kill you. Figure it {out.|out.”}", cap=False, role="quote"),
             ]),
        dict(scene="flow", src="C. Jelinek in 425 Business (2018)",
             p=dict(kicker="THE FIX", a="OUTSIDE SUPPLIERS", b="COSTCO'S OWN PLANTS", c1="CALIFORNIA", c2="ILLINOIS"),
             lines=[
                 "So they figured it out.",
                 "Costco [#stop] stopped buying hot dogs and [#own] started making its own, first in [#c1] California, then in [#c2] Illinois.",
             ]),
        dict(scene="counter", src="Costco annual meeting, Jan. 15, 2026",
             p=dict(kicker="FISCAL 2025", value=245.1, fmt="{:.1f}M", sub="HOT DOG + SODA COMBOS SOLD",
                    legend="1 icon ≈ 10 million", dur=1.5),
             lines=["In fiscal {twenty twenty-five,|2025,} it sold [#count] {two hundred forty-five|245} million combos."]),
        dict(scene="reveal", src="Costco Q4 fiscal 2026 earnings call",
             p=dict(title="THE ASTERISK", qlines=["“Our membership", "continues to be", "the most important", "item we sell.”"],
                    hot=[2, 3], attr1="— RON VACHRIS, Costco CEO", attr2="Earnings call · Sept. 24, 2026"),
             lines=[
                 "[#rev] But here's the asterisk.",
                 "[#quote] In September {twenty twenty-six,|2026,} Costco's CEO said the membership is the most important item we sell.",
             ]),
        dict(scene="statement", src="Costco fiscal 2026 results (Sept. 24, 2026)",
             p=dict(kicker="COSTCO · FISCAL 2026", doc="FROM THE INCOME STATEMENT", r1="Membership fees", v1="$5.9B",
                    r2="Net income (profit)", v2="$9.2B", ratio="Fees compared with total profit", pct=64, pfmt="{:.0f}%"),
             lines=[
                 "That year, [#fees] membership fees brought in [#v1] {five point nine billion dollars.|$5.9 billion.}",
                 "[#profit] That alone equals [#pct] {sixty-four percent|64%} of Costco's entire profit.",
             ]),
        dict(scene="ring_scene", src="Costco Q4 fiscal 2026 earnings call",
             p=dict(kicker="MEMBERSHIP RENEWALS", pct=92.3, pfmt="{:.1f}%", l1="RENEWAL RATE · U.S. & CANADA", l2="Worldwide: 89.8%"),
             lines=["And about [#go] nine out of ten members renew."]),
        dict(scene="close", src="Follow for the next asterisk", src_color=YEL,
             p=dict(BASE, kicker="HOW IT WORKS", kicker0=BASE["kicker"], s1="$1.50 HOT DOG", s2="A REASON TO WALK IN",
                    s3="A MEMBERSHIP RENEWED"),
             lines=[
                 "[#s1] So the hot dog doesn't have to make much money.",
                 "It has to [#s2] remind you why [#s3] you pay to walk in.",
                 "[#back] And that's why it still costs {a dollar fifty.|$1.50.}",
             ]),
    ],
    post=dict(
        tiktok=("Costco's hot dog combo has cost $1.50 since 1985. The asterisk: it was never about the hot dog.\n\n"
                "Sources: Costco fiscal 2026 results (Sept. 24, 2026) · Costco Q4 FY2026 earnings call · "
                "Costco 2026 annual meeting presentation · BLS CPI-U (1985 average vs. Sept. 2026) · "
                "Craig Jelinek in 425 Business (2018)\n\n#costco #business #money #economics #businessstory"),
        title="Why Costco's hot dog still costs $1.50",
    ),
)

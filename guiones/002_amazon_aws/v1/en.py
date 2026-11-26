"""002 · Amazon's $717 billion and where the profit comes from — English (With an Asterisk)."""
YEL = (255, 210, 63)
SRC = "Amazon Q4 2025 results (Feb. 5, 2026)"
BASE = dict(kicker="AMAZON · 2025", num="$717B", sub="IN SALES")

SPEC = dict(
    id="002_amazon_aws", lang="en-us", lang_tag="EN", voice="af_heart", speed=1.0,
    brand="WITH AN ASTERISK",
    sfx=[("ast", "ding", 0.0), ("rev", "thump", 0.0), ("rev", "ding", 0.06)],
    beats=[
        dict(scene="bignum", src=SRC, p=dict(BASE, sub2="Most of the profit came from somewhere else"), lines=[
            "In {twenty twenty-five,|2025,} Amazon brought in {seven hundred seventeen billion dollars|$717 billion} in sales.",
            "[#sub2] But most of its profit didn't come from anything that arrives [#ast] in a box.",
        ]),
        dict(scene="split", src=SRC + " · our math",
             p=dict(kicker="THE STORES VS. EVERYTHING ELSE", t1="SALES", a1=82, t2="OPERATING PROFIT", a2=43,
                    la="STORES", lb="AWS"),
             lines=[
                 "The stores are the part you know: the boxes, the vans, the next-day deliveries.",
                 "In North America and abroad, they made up [#sp1] {eighty-two percent|82%} of those sales.",
                 "[#sp2] But less than half of the operating profit.",
             ]),
        dict(scene="reveal", src="Amazon 2025 annual report",
             p=dict(title="THE ASTERISK", qlines=["Amazon also", "rents out computers.", "It's called", "Amazon Web Services."],
                    hot=[3], attr1="AWS", attr2="Cloud computing that other companies pay to use"),
             lines=[
                 "[#rev] Here's the asterisk.",
                 "[#quote] Amazon also rents out computers. It's called Amazon Web Services, and other companies pay to run their apps on it.",
             ]),
        dict(scene="statement", src=SRC,
             p=dict(kicker="AWS · 2025", doc="FROM AMAZON'S SEGMENT RESULTS", r1="AWS sales", v1="$128.7B",
                    r2="AWS operating profit", v2="$45.6B", ratio="AWS share of Amazon's operating profit", pct=57, pfmt="{:.0f}%"),
             lines=[
                 "That year, [#fees] {A W S|AWS} brought in [#v1] {one hundred twenty-nine billion dollars.|$129 billion.}",
                 "[#profit] Its operating profit was {forty-five point six billion:|$45.6 billion:} [#pct] {fifty-seven percent|57%} of everything Amazon made.",
             ]),
        dict(scene="bars", src=SRC + " · our math",
             p=dict(kicker="OPERATING PROFIT PER $100 OF SALES", v1=6, v2=35, fmt="${:.0f}", l1="THE STORES", l2="AWS",
                    badge="6×", grow_dur=1.2),
             lines=["And it is a much better business.", "For every hundred dollars in sales, the stores kept about six. [#grow] {A W S|AWS} kept {thirty-five.|35.}"]),
        dict(scene="close_num", src="Follow for the next asterisk", src_color=YEL,
             p=dict(BASE, kicker="SO", kicker0=BASE["kicker"], pre=["SAME COMPANY.", "TWO BUSINESSES."], s1=["The store you shop at", "is the big business."],
                    s2=["The one you never see", "is the profitable one."]),
             lines=[
                 "Same company. Two very different businesses.",
                 "[#s1] So the store you shop at is the big business.",
                 "[#s2] The one you never see is the profitable one.",
                 "[#back] And that's the asterisk on {seven hundred seventeen billion dollars.|$717 billion.}",
             ]),
    ],
    post=dict(
        tiktok=("Amazon brought in $717 billion in 2025. The asterisk: most of the profit came from a business you never see.\n\n"
                "Sources: Amazon fourth quarter and full-year 2025 results (Feb. 5, 2026). Percentages are our own math from "
                "Amazon's segment figures.\n\n#amazon #aws #business #money #businessstory"),
        title="Where Amazon's profit really comes from",
    ),
)

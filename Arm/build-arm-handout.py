"""Build Arm/index.html: the "Arm a b c" handout as one self-contained file.

Front: the arm diagram (arm-commands-v30.svg) beside cards a, b, c, with the
"How to Use" box along the bottom. Back: cards 1-8 in two columns.

Everything is inlined -- the diagram, the three icons, and a subset of DejaVu
Sans (the font the diagram's labels are laid out in; without it they re-flow in
Arial). Re-run after editing any source SVG or the card text below:

    python Arm/build-arm-handout.py
"""
import base64
import html
import io
import os
import re

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONT_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")
OUT = os.path.join(HERE, "index.html")   # served at /m2l8gchandout/Arm/


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


def clean_svg(src):
    src = re.sub(r"<\?xml.*?\?>", "", src, flags=re.S)
    src = re.sub(r"<metadata>.*?</metadata>", "", src, flags=re.S)
    src = re.sub(r"<!--.*?-->", "", src, flags=re.S)
    src = src.replace(' xmlns:c2pa="http://c2pa.org/manifest"', "")
    return src.strip()


# ---------------------------------------------------------------- diagram
arm = clean_svg(read("arm-commands-v30.svg"))
arm = arm.replace("str0", "arm-str0").replace('id="arm"', 'id="arm-outline"').replace('id="sun"', 'id="arm-sun"')
# Crop the viewBox to the drawing. The odd 24999.01 height only matters for the
# PNG raster scale; inline, it is just empty paper above the sun.
arm = arm.replace(
    'viewBox="-2077.20 -3300.00 11477.00 24999.01"',
    'viewBox="-1800 -2200 10330 23230" class="diagram" role="img" '
    'aria-label="The arm diagram: God the Life Giver at the top, a b c, then the eight commands down the arm and hand"',
)
# Arm outline in a light tint of the card purple, so the labels over it stay easy to read.
arm = arm.replace('#E8E2D6', '#B89AD8')
# Sun, rays, G-heart-D and "Life Giver" in the life-line's gold, so God and the vein read as one line.
GOLD = "#B8860B"
arm = arm.replace(".arm-str0 {stroke:black", ".arm-str0 {stroke:" + GOLD)
arm, n_text = re.subn(r'(<text[^>]*fill=)"black"(>(?:G|D|Life|Giver)</text>)', r'\1"%s"\2' % GOLD, arm)
arm, n_heart = re.subn(r'(<path d="M5282,-1840[^>]*stroke=)"black"', r'\1"%s"' % GOLD, arm)
assert (n_text, n_heart) == (4, 1), (n_text, n_heart)
arm, n_cross = re.subn(r'(<line [^>]*)stroke="black"( stroke-width="124")', r'\1stroke="%s"\2' % GOLD, arm)
assert n_cross == 2, n_cross


# Labels move to the end of the SVG so they sit above every line -- the cross stem is
# drawn last in the source and otherwise runs over "He loved me first".
labels = []


# Every label is set bold. Bold is wider, so labels that start at a badge rim or a leader
# line keep their left edge (x shifts right by half the growth); the rest stay centred.
# "Lord's Supper" moves right a little -- bold, it would pass the drawing's left edge.
_reg = TTFont(os.path.join(FONT_DIR, "DejaVuSans.ttf"))
_bold = TTFont(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))


def em(font, s):
    cmap, hmtx = font.getBestCmap(), font["hmtx"]
    return sum(hmtx[cmap[ord(ch)]][0] for ch in s) / font["head"].unitsPerEm


KEEP_LEFT = {"He loved me first", "I am His child", "He comes first", "Make Disciples", "Give Generously"}
NUDGE = {"Lord's Supper": 90}


def lift(m):
    tag, text = m.group(0), html.unescape(m.group(1))
    if 'font-weight="bold"' in tag:   # badge glyphs sit on white discs; G/D touch nothing
        return tag
    size = float(re.search(r'font-size="([\d.]+)"', tag).group(1))
    x = float(re.search(r' x="([-\d.]+)"', tag).group(1))
    if text in KEEP_LEFT:
        x += (em(_bold, text) - em(_reg, text)) * size / 2
    x += NUDGE.get(text, 0)
    tag = re.sub(r' x="[-\d.]+"', ' x="%.1f"' % x, tag, count=1).replace("<text ", '<text font-weight="bold" ', 1)
    labels.append(tag)
    return ""


arm = re.sub(r'<text [^>]*>([^<]*)</text>', lift, arm)
arm = arm.replace("</svg>", "\n".join(labels) + "\n</svg>")
assert len(labels) == 19, len(labels)

# Zechariah 4:6 as the diagram's closing line: bold, re-broken into short lines, sized so
# the longest one spans ~94% of the drawing's width, centred under it.
_bcmap, _bhmtx, _bupm = _bold.getBestCmap(), _bold["hmtx"], _bold["head"].unitsPerEm


def bold_em(s):
    return sum(_bhmtx[_bcmap[ord(ch)]][0] for ch in s) / _bupm


VB_X, VB_W, VB_Y = -1800, 10330, -2200
ZECH = ["The work does not get done", "by human strength or force,", "but by God\u2019s Spirit"]
ZECH_REF = "Zechariah 4:6"
arm, n_zech = re.subn(r'<text [^>]*>(?:The work does not get done|but by God\'s Spirit)[^<]*</text>\n?', "", arm)
assert n_zech == 2, n_zech
zs = 0.94 * VB_W / max(bold_em(t) for t in ZECH)
rs = zs * 0.78
cx, y = VB_X + VB_W / 2, 19454 + 82 + 380 + 0.73 * zs   # clear of "Pray in the Name of Jesus"
zech = []
for t in ZECH:
    zech.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="\'DejaVu Sans\', Arial, sans-serif" '
                'font-size="%.0f" font-weight="bold" fill="%s">%s</text>' % (cx, y, zs, GOLD, html.escape(t)))
    y += zs * 1.2
y += rs * 0.15
zech.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="\'DejaVu Sans\', Arial, sans-serif" '
            'font-size="%.0f" font-weight="bold" fill="%s">%s</text>' % (cx, y, rs, GOLD, ZECH_REF))
bottom = y   # the drawing ends on the reference's baseline, so it lines up with the c card's bottom edge
arm = arm.replace("</svg>", "\n".join(zech) + "\n</svg>")
arm = arm.replace('viewBox="-1800 -2200 10330 23230"', 'viewBox="%d %d %d %.0f" preserveAspectRatio="xMidYMax meet"' % (VB_X, VB_Y, VB_W, bottom - VB_Y))
glyphs = set("".join(re.findall(r">([^<>]+)</text>", arm))) | set("abc12345678")

icons = {}
for key, name, prefix in (("a", "sun-heart-icon.svg", "sh"), ("b", "hand-heart-icon.svg", "hh"),
                          ("c", "hand-point-icon.svg", "hp")):
    svg = clean_svg(read(name))
    svg = re.sub(r'id="(?!%s-)([^"]+)"' % prefix, r'id="%s-\1"' % prefix, svg)
    svg = svg.replace("<svg ", '<svg class="icon" aria-hidden="true" ', 1)
    svg = re.sub(r"<title.*?</title>|<desc.*?</desc>", "", svg, flags=re.S)
    svg = re.sub(r'\s(role|aria-labelledby)="[^"]*"', "", svg)
    svg = svg.replace('<svg class="icon" aria-hidden="true"', '<svg class="icon" aria-hidden="true"', 1)
    icons[key] = re.sub(r"\n\s*\n", "\n", svg)
# The eight command icons (Arm/icons/make-icons.py draws them).
for n in range(1, 9):
    with open(os.path.join(HERE, "icons", "icon-%d.svg" % n), encoding="utf-8") as f:
        svg = f.read().strip()
    svg = re.sub(r'\s(role|aria-label)="[^"]*"', "", svg)
    icons[str(n)] = svg.replace("<svg ", '<svg class="icon icon-n" aria-hidden="true" ', 1)


# ------------------------------------------------------------------ fonts
def woff_b64(ttf):
    font = TTFont(os.path.join(FONT_DIR, ttf))
    opts = subset.Options()
    opts.flavor = "woff"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    s = subset.Subsetter(opts)
    s.populate(text="".join(sorted(glyphs)) + " ")
    s.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


FONT_REG = woff_b64("DejaVuSans.ttf")
FONT_BOLD = woff_b64("DejaVuSans-Bold.ttf")

# ------------------------------------------------------------------ cards
# Declarations: (bold, reference). Layout "grid" = 2x2, "list" = one per line.
CARDS = {
    "a": dict(
        verse="For God so loved the world that he gave his one and only Son, that whoever believes in him "
              "shall not perish but have eternal life.",
        ref="John 3:16",
        story=("The Father Who Runs", "Luke 15:11-32"),
        questions=["Is this the father you have known? Is this the God you have believed in?",
                   "The father loved his son before he said sorry. Can you let God love you like that?",
                   "If God is like this, what do you want to say to him?"],
        head="God is", layout="grid",
        items=[("Loving", "John 3:16"), ("Father", "Romans 8:15"),
               ("Merciful", "John 8:1-11"), ("Seeing", "Luke 19:1-10")]),
    "b": dict(
        verse="Yet to all who did receive him, to those who believed in his name, he gave the right to become "
              "children of God. Children born not of natural descent, nor of human decision or a husband’s "
              "will, but born of God.",
        ref="John 1:12-13",
        story=("The Son Who Came Home", "Luke 15:11-32"),
        questions=["The son said, “I’m not worthy.” The father said, “My son.” "
                   "Which do you believe?",
                   "He came to work. The father made him a son. Are you working or receiving?",
                   "God calls you his child today. What do you want to say to him?"],
        head="I am", layout="grid",
        items=[("God’s Child", "John 1:12"), ("Loved First", "1 John 4:19"),
               ("Forgiven", "1 John 1:9"), ("Safe", "John 10:28-29")]),
    "c": dict(
        verse="You must love the Lord your God with all your heart, with all your being, and with all your mind. "
              "This is the first and greatest commandment. And the second is like it: You must love your neighbor "
              "as you love yourself. All the Law and the Prophets depend on these two commands.",
        ref="Matthew 22:37-40",
        story=("Mary Chose to Sit with Jesus", "Luke 10:38-42"),
        questions=["Martha worked for Jesus. Mary sat with him. Which are you?",
                   "Jesus invited Martha to sit too. What holds you back?",
                   "He loved you first. You’re his child. He’s in the room. What do you want to do?"],
        head="I love God", layout="list",
        items=[("Because he loved me first", "1 John 4:19"), ("First, before all else", "Matthew 22:37-38"),
               ("With all I am", "Deuteronomy 6:5"), ("So I love others", "1 John 4:11")]),
    "1": dict(
        verse="You must love the Lord your God with all your heart, with all your being, and with all your mind. "
              "This is the first and greatest commandment.",
        ref="Matthew 22:37-38",
        story=("Mary Anoints Jesus", "Mark 14:3-9"),
        questions=["Mary wanted only Jesus. When did you last come to God asking nothing?",
                   "Tell him now who he is to you."],
        head="I love God by", layout="list",
        items=[("Being with him", "Luke 10:42"), ("Adoring him for who he is", "Psalm 145:3"),
               ("Desiring him above all", "Psalm 73:25")]),
    "2": dict(
        verse="And the second is like it: You must love your neighbor as you love yourself.",
        ref="Matthew 22:39",
        story=("The Good Samaritan", "Luke 10:25-37"),
        questions=["The Samaritan stopped to help a stranger. Who near you needs your help this week?",
                   "He helped a man from an enemy people. Who is hard for you to love? Pray for them now."],
        head="I love others by", layout="list",
        items=[("Serving my neighbor", "1 John 3:18"), ("Praying for my enemies", "Matthew 5:44"),
               ("Caring for other believers", "John 13:34-35")]),
    "3": dict(
        verse="Repent and be baptized, every one of you, in the name of Jesus Christ for the forgiveness of your "
              "sins. And you will receive the gift of the Holy Spirit.",
        ref="Acts 2:38",
        story=("The Day of Pentecost", "Acts 2:36-41"),
        questions=["The people believed and asked, “What should we do?” What do you need to turn away "
                   "from to follow Jesus?",
                   "God gives his Spirit to all who ask. Ask him now."],
        head="I follow Jesus by", layout="list",
        items=[("Trusting him", "John 3:16"), ("Turning from sin to God", "Acts 3:19"),
               ("Asking for the Holy Spirit", "Luke 11:13")]),
    "4": dict(
        verse="Go and make disciples of all nations. Baptize them in the name of the Father, the Son, and the "
              "Holy Spirit.",
        ref="Matthew 28:19",
        story=("Philip Baptizes the Ethiopian", "Acts 8:26-39"),
        questions=["The man asked, “What stops me from being baptized?” What stops you?",
                   "Who can you help to be baptized?"],
        head="I obey by", layout="list",
        items=[("Being baptized myself", "Acts 2:38"), ("Living a new life", "Romans 6:4"),
               ("Baptizing new believers quickly", "Acts 16:33")]),
    "5": dict(
        verse="This is my body, which is given for you.\nDo this in remembrance of me.",
        ref="Luke 22:19",
        story=("The Last Supper", "Luke 22:7-20"),
        questions=["Jesus gave his body and blood for you. What does this show you about his love?",
                   "Is there anything you need to make right with God or others before you eat?"],
        head="I take the Lord’s Supper by", layout="list",
        items=[("Remembering his sacrifice", "Luke 22:19"), ("Examining my heart", "1 Corinthians 11:28"),
               ("Waiting for his return", "1 Corinthians 11:26")]),
    "6": dict(
        verse="I will do whatever you ask for in my name, so that the Father can be glorified in the Son. When you "
              "ask me for anything in my name, I will do it.",
        ref="John 14:13-14",
        story=("Peter and John Heal a Lame Man", "Acts 3:1-10"),
        questions=["Peter had no money, but he had Jesus’ name. What will you ask Jesus for today?",
                   "Who will you pray for in Jesus’ name this week?"],
        head="I pray in Jesus’ name by", layout="list",
        items=[("Coming boldly through Jesus", "Hebrews 4:16"), ("Asking for what he wants", "1 John 5:14"),
               ("Trusting him to answer", "Mark 11:24")]),
    "7": dict(
        verse="Everyone should give whatever they have decided in their heart. They shouldn’t give with "
              "hesitation or because of pressure. God loves a cheerful giver.",
        ref="2 Corinthians 9:7",
        story=("The Widow’s Offering", "Mark 12:41-44"),
        questions=["The widow gave all she had. What is God asking you to give?",
                   "Who can you give to this week?"],
        head="I give generously by", layout="list",
        items=[("Giving freely", "Matthew 10:8"), ("Giving to those in need", "Proverbs 19:17"),
               ("Giving God my first and best", "Proverbs 3:9")]),
    "8": dict(
        verse="Go and make disciples of all nations, baptizing them in the name of the Father and of the Son and "
              "of the Holy Spirit. Teach them to obey everything I have commanded you.",
        ref="Matthew 28:19-20",
        story=("Andrew Brings His Brother to Jesus", "John 1:40-42"),
        questions=["Andrew told his brother about Jesus. Who can you tell?",
                   "Someone helped you follow Jesus. Who can you help?"],
        head="I make disciples by", layout="list",
        items=[("Going to others", "Acts 1:8"), ("Telling what Jesus did for me", "Mark 5:19"),
               ("Teaching them to obey Jesus", "Matthew 28:20")]),
}

# The gathering pattern from Card H of the main Life with God handout (7gc.me/mh2):
# See Him -> Love Him -> Live for Him. A label marks the step where each part begins.
FOOTER = ("TsunamiUnleashed.org · Free to all. CC0 1.0 Public Domain. "
          "Keep it faithful to Scripture and worthy of Christ. · Updated 2026-09-26 · Latest: 7gc.me/arm")

HOW_TO = [
    (None, "Pray. Ask the Holy Spirit to lead."),
    (None, "Be with God together, asking for nothing. Thank Him for who He is."),
    (None, "Share since last time: What did you obey? Who did you tell?"),
    (None, "Use one card each time, in order: a, b, c, then 1–8."),
    ("See Him", "Read the verse aloud. Read the story from the Bible."),
    (None, "Close the Bible. Take turns retelling it, three times. Sit quietly."),
    (None, "Read the card’s bold list. Point to its letter or number on the arm."),
    ("Love Him", "Ask the questions. After answers, ask: “What does that show you about the God who’s with you?”"),
    ("Live for Him", "Ask each person: How will you show Jesus you love Him this week? Who will you tell?"),
    (None, "Pray for strength to love and obey Him. Bless each other."),
]

e = html.escape


def card(key):
    c = CARDS[key]
    icon = icons.get(key, "")
    items = "".join(
        '<li><b>%s</b> <span class="ref">(%s)</span></li>' % (e(b), e(r)) for b, r in c["items"])
    qs = "".join("<li>%s</li>" % e(q) for q in c["questions"])
    return f"""
<section class="card card-{key}" aria-label="Card {key}">
  <header class="tab"><span class="badge">{key}</span>{icon}</header>
  <p class="verse">{e(c["verse"]).replace(chr(10), "<br>")} <b class="vref">{e(c["ref"])}</b></p>
  <p class="story"><b>Story:</b> {e(c["story"][0])} <span class="ref">~ {e(c["story"][1])}</span></p>
  <h3>Questions</h3>
  <ul class="qs">{qs}</ul>
  <h3 class="decl">{e(c["head"])}:</h3>
  <ul class="items {c["layout"]}">{items}</ul>
</section>"""


howto = "".join("<li>%s%s</li>" % ('<b class="phase">%s</b> ' % e(lab) if lab else "", e(s)) for lab, s in HOW_TO)

page = f"""<!doctype html>
<html lang="en" class="paper-letter">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Arm a b c Handout</title>
<style id="page-size">@page {{ size: letter; margin: 0.42in; }}</style>
<style>
@font-face {{ font-family: "DejaVu Sans"; font-weight: 400; src: url(data:font/woff;base64,{FONT_REG}) format("woff"); }}
@font-face {{ font-family: "DejaVu Sans"; font-weight: 700; src: url(data:font/woff;base64,{FONT_BOLD}) format("woff"); }}

:root {{
  --ink: #1d1a17;
  --soft: #5b554d;
  --accent: #6b35a8;      /* card frames and headings */
  --accent-2: #b8860b;    /* the diagram's gold life-line */
  --rule: #d9cfe6;
  --desk: #e9e6e1;
  --desk-ink: #2b2723;
  --bar: #ffffffee;
  --pw: 8.5in; --ph: 11in;
  --pad: 0.42in;   /* = the @page margin; printers clip anything much closer to the edge */
  --diagram-w: 3.5in;
  --gap: 0.16in;
}}
.paper-a4 {{ --pw: 210mm; --ph: 297mm; --pad: 11mm; --diagram-w: 3.4in; }}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{ --desk: #1f1d1b; --desk-ink: #ece8e2; --bar: #2a2724ee; }}
}}
:root[data-theme="dark"] {{ --desk: #1f1d1b; --desk-ink: #ece8e2; --bar: #2a2724ee; }}

* {{ box-sizing: border-box; }}
html, body {{ margin: 0; }}
body {{
  background: var(--desk);
  color: var(--ink);
  font: 8.6pt/1.3 Arial, "Helvetica Neue", Helvetica, "Liberation Sans", sans-serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;
}}

/* ------------------------------------------------ screen toolbar */
.bar {{
  position: sticky; top: 0; z-index: 5;
  display: flex; flex-wrap: wrap; align-items: center; gap: 10px 16px;
  padding: 10px 16px; background: var(--bar); color: var(--desk-ink);
  backdrop-filter: blur(6px); border-bottom: 1px solid #0002;
  font: 14px/1.3 system-ui, "Segoe UI", sans-serif;
}}
.bar h1 {{ font-size: 15px; margin: 0 auto 0 0; font-weight: 600; }}
.seg {{ display: inline-flex; border: 1px solid #0003; border-radius: 8px; overflow: hidden; }}
.seg button, .print {{
  font: inherit; border: 0; padding: 7px 14px; cursor: pointer; background: transparent; color: inherit;
}}
.seg button[aria-pressed="true"] {{ background: var(--accent); color: #fff; }}
.print {{ background: var(--accent); color: #fff; border-radius: 8px; font-weight: 600; }}
.tip {{ flex-basis: 100%; margin: 0; font-size: 12.5px; opacity: .8; }}

.sheets {{ padding: 24px 16px 48px; display: grid; justify-content: center; gap: 24px; }}
.sheet {{
  width: var(--pw); height: var(--ph); padding: var(--pad);
  background: #fff; overflow: hidden; position: relative;
  box-shadow: 0 1px 3px #0002, 0 8px 28px #0002;
  zoom: var(--fit, 1);
}}

/* On screen, browser zoom and text rendering run a hair taller than print; let the back
   grow rather than clip each card's last line. Print keeps the exact page height. */
@media screen {{ .sheet.back {{ height: auto; min-height: var(--ph); grid-template-rows: repeat(4, auto); }} }}

/* ------------------------------------------------ front */
.front {{ display: grid; grid-template-rows: 1fr auto; gap: var(--gap); }}
.front-main {{ display: grid; grid-template-columns: var(--diagram-w) 1fr; gap: var(--gap); min-height: 0; }}
.diagram-wrap {{ display: flex; align-items: flex-end; justify-content: center; min-height: 0; }}
.diagram {{ width: 100%; height: 100%; display: block; overflow: visible; }}   /* its box ends on the Zechariah baseline; never clip the letters */
.front-cards {{ display: flex; flex-direction: column; justify-content: space-between; gap: calc(var(--gap) + 6pt); padding-top: 17pt; font-size: 8.3pt; }}
.front-cards .card {{ flex: 0 0 auto; }}

/* ------------------------------------------------ back */
.back {{
  display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(4, 1fr);
  grid-auto-flow: column; column-gap: var(--gap); row-gap: calc(var(--gap) + 15pt); padding-top: calc(var(--pad) + 15pt); font-size: 8.4pt;
}}

/* ------------------------------------------------ cards */
.card {{
  position: relative; min-height: 0;
  border: 1.25pt solid var(--accent); border-radius: 5pt;
  padding: 10pt 9pt 5pt;
  display: flex; flex-direction: column;
}}
.tab {{
  position: absolute; top: 0; left: 50%; transform: translate(-50%, -55%);
  display: flex; align-items: center; gap: 3pt; padding: 0 5pt; background: #fff; height: 20pt;
}}
.badge {{
  display: inline-grid; place-items: center; width: 16pt; height: 16pt; border-radius: 50%;
  border: 1.4pt solid var(--ink); background: #fff;
  font: 700 10.5pt/1 "DejaVu Sans", Arial, sans-serif; padding-bottom: .5pt;
}}
.tab {{ height: 26pt; transform: translate(-50%, -62%); }}
.icon-n {{ height: 18pt; }}
.back .tab {{ height: 22pt; transform: translate(-50%, -58%); }}
.icon {{ height: 22pt; width: auto; color: var(--ink); display: block; }}
.card-a .icon {{ height: 15pt; }}

.verse {{ margin: 0 0 4pt; text-align: center; }}
.vref {{ white-space: nowrap; }}
.story {{ margin: 0 0 3pt; }}
.ref {{ color: var(--soft); white-space: nowrap; }}
h3 {{ font-size: inherit; margin: 3pt 0 1pt; font-weight: 700; }}
h3.decl {{ color: var(--accent); text-transform: uppercase; letter-spacing: .04em; font-size: 7.9pt; margin-top: auto; padding-top: 4pt; }}
ul {{ margin: 0; padding-left: 11pt; }}
li {{ margin: 0 0 1pt; }}
.qs li::marker {{ color: var(--accent); }}
.items {{ list-style: none; padding-left: 0; margin-bottom: 1pt; }}
.items.grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 8pt; }}
.items.list li {{ padding-left: 9pt; position: relative; }}
.items.list li::before {{ content: ""; position: absolute; left: 1pt; top: .52em; width: 3.4pt; height: 3.4pt; border-radius: 50%; background: var(--accent-2); }}

.foot {{ position: absolute; left: 0; right: 0; bottom: var(--foot-bottom); text-align: center; font-size: 7.2pt; line-height: 1; color: var(--soft); }}
.back {{ --foot-h: 12pt; --foot-bottom: var(--pad); padding-bottom: calc(var(--pad) + var(--foot-h)); }}

/* ------------------------------------------------ how to */
.howto {{ border: 1.25pt solid var(--accent); border-radius: 5pt; padding: 6pt 10pt 6pt; font-size: 8pt; }}
.howto h2 {{ margin: 0 0 3pt; text-align: center; font-size: 9.2pt; color: var(--accent); text-transform: uppercase; letter-spacing: .06em; }}
.howto ol {{ margin: 0; padding-left: 16pt; columns: 2; column-gap: 22pt; }}
.howto li {{ break-inside: avoid; margin: 0 0 1.5pt; }}
.howto .pattern {{ margin-left: 8pt; text-transform: none; letter-spacing: 0; font-weight: 700; color: var(--accent-2); }}
.howto .phase {{ color: var(--accent-2); font-weight: 700; }}   /* bold too, so it still reads in black and white */
.howto li::marker {{ font-weight: 700; color: var(--accent); }}

/* ------------------------------------------------ print */
@media print {{
  body {{ background: #fff; }}
  .bar {{ display: none; }}
  .sheets {{ display: block; padding: 0; }}
  .sheet {{
    zoom: 1; box-shadow: none; margin: 0;
    padding: 0;   /* the @page margin does the job on paper */
    width: calc(var(--pw) - 2 * var(--pad));
    height: calc(var(--ph) - 2 * var(--pad) - 0.6mm);   /* a hair under, so rounding never spills a blank page */
    break-after: page; page-break-after: always;
  }}
  .sheet.back {{ padding-top: 15pt; padding-bottom: var(--foot-h); --foot-bottom: 0pt; }}   /* headroom for the top-row tabs; overflow:hidden would clip them */
  .sheet:last-child {{ break-after: auto; page-break-after: auto; }}
}}
</style>
</head>
<body>
<div class="bar" role="toolbar" aria-label="Print options">
  <h1>Arm a b c &mdash; handout</h1>
  <span class="seg" role="group" aria-label="Paper size">
    <button type="button" data-paper="letter" aria-pressed="true">Letter</button>
    <button type="button" data-paper="a4" aria-pressed="false">A4</button>
  </span>
  <button type="button" class="print" onclick="window.print()">Print</button>
  <p class="tip">Pick the paper size first. Print at 100% scale, margins &ldquo;Default&rdquo; (not &ldquo;None&rdquo;),
  two-sided, flip on the long edge &mdash; one sheet, front and back.</p>
</div>

<main class="sheets">
  <article class="sheet front" aria-label="Front">
    <div class="front-main">
      <div class="diagram-wrap">{arm}</div>
      <div class="front-cards">{card("a")}{card("b")}{card("c")}</div>
    </div>
    <section class="howto" aria-label="How to use this handout">
      <h2>How to Use This Handout <span class="pattern">See Him &rarr; Love Him &rarr; Live for Him</span></h2>
      <ol>{howto}</ol>
    </section>
  </article>

  <article class="sheet back" aria-label="Back">
    {"".join(card(str(n)) for n in range(1, 9))}
    <footer class="foot">{e(FOOTER)}</footer>
  </article>
</main>

<script>
(function () {{
  var root = document.documentElement, sizeTag = document.getElementById("page-size");
  var buttons = document.querySelectorAll("[data-paper]");
  function setPaper(p) {{
    root.classList.remove("paper-letter", "paper-a4");
    root.classList.add("paper-" + p);
    sizeTag.textContent = "@page {{ size: " + (p === "a4" ? "A4; margin: 11mm" : "letter; margin: 0.42in") + "; }}";
    buttons.forEach(function (b) {{ b.setAttribute("aria-pressed", String(b.dataset.paper === p)); }});
    try {{ localStorage.setItem("arm-handout-paper", p); }} catch (e) {{}}
    fit();
  }}
  function fit() {{
    var s = document.querySelector(".sheet");
    root.style.setProperty("--fit", 1);
    var w = s.getBoundingClientRect().width, avail = window.innerWidth - 32;
    root.style.setProperty("--fit", w > avail ? (avail / w).toFixed(4) : 1);
  }}
  var saved = (location.search.match(/[?&]paper=(letter|a4)/) || [])[1] || null;
  try {{ saved = saved || localStorage.getItem("arm-handout-paper"); }} catch (e) {{}}
  if (!saved) {{
    var region = ((navigator.language || "en-US").split("-")[1] || "US").toUpperCase();
    saved = ["US", "CA", "MX", "PH", "CL", "CO", "VE", "GT", "CR", "PA", "DO", "PR", "SV", "NI", "HN"]
      .indexOf(region) >= 0 ? "letter" : "a4";
  }}
  buttons.forEach(function (b) {{ b.addEventListener("click", function () {{ setPaper(b.dataset.paper); }}); }});
  window.addEventListener("resize", fit);
  window.addEventListener("beforeprint", function () {{ root.style.setProperty("--fit", 1); }});
  window.addEventListener("afterprint", fit);
  setPaper(saved);
}})();
</script>
</body>
</html>
"""

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    f.write(page)
print("wrote", OUT, "%.0f KB" % (len(page.encode()) / 1024), "glyphs:", len(glyphs))

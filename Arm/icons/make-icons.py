"""Generate the eight command icons (icon-1.svg ... icon-8.svg) for the Arm handout.

Stroked line art in a 100x100 box, currentColor throughout, and -- like the
a/b/c icons -- each one carries the heart. Re-run after editing a shape:

    python Arm/icons/make-icons.py
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SW = 3.9  # stroke width in the 100-unit box


def heart(cx, notch_y, s, sw=SW):
    """Heart whose top notch sits at (cx, notch_y); s = half-width."""
    d = ("M0,1.6 C-0.7,1.1 -1,0.7 -1,0.35 C-1,-0.05 -0.7,-0.3 -0.45,-0.3 "
         "C-0.2,-0.3 -0.05,-0.15 0,0.05 C0.05,-0.15 0.2,-0.3 0.45,-0.3 "
         "C0.7,-0.3 1,-0.05 1,0.35 C1,0.7 0.7,1.1 0,1.6 Z")
    return (f'<path transform="translate({cx} {notch_y}) scale({s})" stroke-width="{sw / s:.4f}" d="{d}"/>')


ICONS = {
    # 1 Love God -- a heart lifted up, its love rising to him
    1: ("Love God", [
        heart(50, 54, 20),
        '<path d="M50 38 V16"/>', '<path d="M31 42 L21 30"/>', '<path d="M69 42 L79 30"/>',
    ]),
    # 2 Love others -- two hearts side by side, overlapping
    2: ("Love others", [
        heart(31, 38, 15), heart(69, 38, 15),
    ]),
    # 3 Believe, repent, receive the Spirit -- the Pentecost flame, heart within
    3: ("Holy Spirit flame", [
        '<path d="M50 90 C31 90 21 76 25 60 C28 49 37 44 38 30 C46 36 49 45 49 52 '
        'C55 44 58 31 53 12 C69 23 80 42 77 61 C75 78 66 90 50 90 Z"/>',
        heart(50, 64, 9),
    ]),
    # 4 Baptize -- a drop of water over the waves
    4: ("Water", [
        '<path d="M50 8 C50 8 26 38 26 56 C26 70 37 80 50 80 C63 80 74 70 74 56 C74 38 50 8 50 8 Z"/>',
        heart(50, 50, 10),
        '<path d="M12 92 C18 87 24 87 30 92 C36 97 42 97 48 92 C54 87 60 87 66 92 C72 97 78 97 84 92"/>',
    ]),
    # 5 Lord's Supper -- the cup
    5: ("Cup", [
        '<path d="M26 14 H74 C74 42 65 56 50 56 C35 56 26 42 26 14 Z"/>',
        '<path d="M50 56 V80"/>', '<path d="M32 88 C36 81 64 81 68 88 Z"/>',
        heart(50, 26, 10),
    ]),
    # 6 Pray in Jesus' name -- hands pressed together, pointing up
    6: ("Praying hands", [
        '<path d="M50 10 C43 11 39 20 37 32 L33 56 C32 62 28 68 22 74 L32 86 C40 80 46 74 50 66"/>',
        '<path d="M50 10 C57 11 61 20 63 32 L67 56 C68 62 72 68 78 74 L68 86 C60 80 54 74 50 66"/>',
        '<path d="M50 10 V62"/>',
        '<path d="M18 80 L30 92"/>', '<path d="M82 80 L70 92"/>',
        heart(50, 77, 6.5),
    ]),
    # 7 Give generously -- a gift whose bow is a heart
    7: ("Gift", [
        '<path d="M22 50 V88 H78 V50"/>', '<rect x="15" y="36" width="70" height="14" rx="2"/>',
        '<path d="M50 36 V88"/>',
        heart(50, 20, 11),
    ]),
    # 8 Make disciples -- a seedling that grows and multiplies, heart as its bloom
    8: ("Seedling", [
        '<path d="M50 90 V44"/>', '<path d="M28 90 H72"/>',
        '<path d="M50 74 C38 74 28 68 24 57 C37 55 46 61 50 74 Z"/>',
        '<path d="M50 64 C62 64 72 58 76 47 C63 45 54 51 50 64 Z"/>',
        heart(50, 22, 12),
    ]),
}

for n, (name, parts) in ICONS.items():
    body = "\n  ".join(parts)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="{name}">\n'
           f'  <g fill="none" stroke="currentColor" stroke-width="{SW}" stroke-linecap="round" '
           f'stroke-linejoin="round">\n  {body}\n  </g>\n</svg>\n')
    with open(os.path.join(HERE, f"icon-{n}.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
print("wrote icon-1.svg .. icon-8.svg")

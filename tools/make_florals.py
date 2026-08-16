#!/usr/bin/env python3
"""Generate the watercolour floral corner artwork for the Murat & Beyza invitation.

Modelled on the printed template: cream/ivory peonies as the dominant blooms with
dark speckled throats, blush garden roses as the secondary accent, long pointed
willow leaves radiating out of the cluster, round silver-dollar eucalyptus, and
small mustard berry sprigs.

  floral-top.svg     anchored top-right, spilling down and to the left
  floral-bottom.svg  anchored bottom-left, rising up and to the right

Shapes are placed procedurally — leaves ride along bezier stems, petals fan out in
offset rings — so the arrangement reads as painted rather than stamped.
"""
import math
import random

SIZE = 1000

# foliage — pale and airy, as in the template
SAGE = ["#AFC3A0", "#C2D2B4", "#9BB48C", "#D2DEC6", "#8FAA80", "#B9CBAB"]
SAGE_PALE = ["#C8D7BC", "#D6E1CC", "#BACDAC", "#E0E8D7"]
STEM = "#8FA382"
STEM_DARK = "#6E8A66"

# blooms
# the ivory blooms need real warmth or they vanish against the white card
CREAM_PALE = "#F8F0DF"
CREAM_DEEP = "#DCC59D"
CREAM_CORE = "#B0895A"
SPECKLE = "#6E4E33"

BLUSH_PALE = "#F0DBD5"
BLUSH_DEEP = "#D2A198"
BLUSH_CORE = "#AA7268"

GOLD = ["#D3A82F", "#E2BE5A", "#C09321"]


# ---------------------------------------------------------------- geometry

def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
    )


def bez_tangent(p0, p1, p2, p3, t):
    u = 1 - t
    dx = 3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
    dy = 3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
    return dx, dy


def f(v):
    return f"{v:.1f}"


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(a[i] + (b[i] - a[i]) * t):02x}" for i in range(3))


def stem_of(p0, p1, p2, p3, width, colour=STEM, opacity=0.8):
    return (f'<path d="M{f(p0[0])},{f(p0[1])} C{f(p1[0])},{f(p1[1])} '
            f'{f(p2[0])},{f(p2[1])} {f(p3[0])},{f(p3[1])}" fill="none" '
            f'stroke="{colour}" stroke-width="{f(width)}" stroke-linecap="round" '
            f'opacity="{opacity}"/>')


# ---------------------------------------------------------------- foliage

def willow(rng, p0, p1, p2, p3, n=11, leaf_len=100, width=2.4, palette=SAGE_PALE, sweep=34):
    """Long branch of elongated pointed leaves — the signature foliage of the template.

    Leaves angle forward along the stem and taper toward the tip, each with a
    faint centre vein.
    """
    out = [stem_of(p0, p1, p2, p3, width)]
    for i in range(n):
        t = 0.06 + 0.94 * (i + 0.5) / n
        x, y = bez(p0, p1, p2, p3, t)
        dx, dy = bez_tangent(p0, p1, p2, p3, t)
        ang = math.degrees(math.atan2(dy, dx))
        side = 1 if i % 2 else -1
        L = leaf_len * (1 - 0.42 * t) * rng.uniform(0.84, 1.16)
        Wd = L * rng.uniform(0.20, 0.27)
        a = ang + side * (sweep + rng.uniform(-9, 9))
        fill = rng.choice(palette)
        d = f"M0,0 Q{f(L * 0.42)},{f(-Wd)} {f(L)},0 Q{f(L * 0.42)},{f(Wd)} 0,0 Z"
        out.append(
            f'<g transform="translate({f(x)},{f(y)}) rotate({f(a)})">'
            f'<path d="{d}" fill="{fill}" opacity="{rng.uniform(0.62, 0.84):.2f}"/>'
            f'<path d="M{f(L * 0.06)},0 L{f(L * 0.88)},0" stroke="{STEM_DARK}" '
            f'stroke-width="0.9" opacity="0.22" fill="none"/>'
            f'</g>'
        )
    return "".join(out)


def eucalyptus(rng, p0, p1, p2, p3, n=13, leaf_r=34, taper=0.45, width=2.2, palette=SAGE):
    """Silver-dollar eucalyptus: round leaves alternating down a slim stem."""
    out = [stem_of(p0, p1, p2, p3, width, opacity=0.85)]
    for i in range(n):
        t = 0.08 + 0.92 * (i + 0.5) / n
        x, y = bez(p0, p1, p2, p3, t)
        dx, dy = bez_tangent(p0, p1, p2, p3, t)
        ang = math.degrees(math.atan2(dy, dx))
        side = 1 if i % 2 else -1
        scale = (1 - taper * t) * rng.uniform(0.82, 1.14)
        rx = leaf_r * scale
        ry = rx * rng.uniform(0.74, 0.88)
        prad = math.radians(ang + side * 90)
        cx = x + math.cos(prad) * rx * 0.78
        cy = y + math.sin(prad) * rx * 0.78
        out.append(
            f'<g transform="translate({f(cx)},{f(cy)}) rotate({f(ang + side * rng.uniform(48, 66))})">'
            f'<ellipse rx="{f(rx)}" ry="{f(ry)}" fill="{rng.choice(palette)}" '
            f'opacity="{rng.uniform(0.66, 0.88):.2f}"/>'
            f'<path d="M{f(-rx * 0.7)},0 Q0,{f(-ry * 0.12)} {f(rx * 0.7)},0" fill="none" '
            f'stroke="{STEM_DARK}" stroke-width="1" opacity="0.26"/>'
            f'</g>'
        )
    return "".join(out)


def berries(rng, p0, p1, p2, p3, n=8, r=9):
    out = [stem_of(p0, p1, p2, p3, 1.5, opacity=0.7)]
    for i in range(n):
        t = 0.12 + 0.88 * (i + 0.5) / n
        x, y = bez(p0, p1, p2, p3, t)
        dx, dy = bez_tangent(p0, p1, p2, p3, t)
        ang = math.atan2(dy, dx)
        side = 1 if i % 2 else -1
        stalk = rng.uniform(11, 22)
        bx = x + math.cos(ang + side * 1.15) * stalk
        by = y + math.sin(ang + side * 1.15) * stalk
        rr = r * (1 - 0.32 * t) * rng.uniform(0.84, 1.16)
        out.append(
            f'<path d="M{f(x)},{f(y)} L{f(bx)},{f(by)}" stroke="{STEM}" stroke-width="1.2" '
            f'opacity="0.6" fill="none"/>'
            f'<circle cx="{f(bx)}" cy="{f(by)}" r="{f(rr)}" fill="{rng.choice(GOLD)}" '
            f'opacity="{rng.uniform(0.7, 0.9):.2f}"/>'
        )
    return "".join(out)


# ---------------------------------------------------------------- blooms

def petal(cx, cy, angle, length, width, fill, opacity, edge=None):
    """A cupped petal: narrow at the base, flaring and folding back at the tip."""
    d = (f"M0,0 "
         f"C{f(0.22 * length)},{f(-0.52 * width)} {f(0.72 * length)},{f(-0.62 * width)} "
         f"{f(length)},{f(-0.16 * width)} "
         f"C{f(1.04 * length)},{f(0.06 * width)} {f(1.04 * length)},{f(0.10 * width)} "
         f"{f(length)},{f(0.20 * width)} "
         f"C{f(0.72 * length)},{f(0.62 * width)} {f(0.22 * length)},{f(0.52 * width)} 0,0 Z")
    stroke = f' stroke="{edge}" stroke-width="1.1" stroke-opacity="0.34"' if edge else ""
    return (f'<path d="{d}" transform="translate({f(cx)},{f(cy)}) rotate({f(angle)})" '
            f'fill="{fill}" opacity="{opacity:.2f}"{stroke}/>')


RING_PLAN = [(1.00, 12), (0.83, 10), (0.66, 9), (0.50, 7), (0.35, 6), (0.22, 5)]


def bloom(rng, cx, cy, r, pale, deep, core, throat="rose", tilt=None, rings=None):
    """A layered garden rose / peony.

    Petals are laid outer-ring-first along a colour ramp from pale at the rim to
    deep at the throat, each ring rotated off the last so nothing lines up into a
    pinwheel, and the ring centres drift off-axis so the bloom reads as cupped.
    """
    plan = RING_PLAN[:rings] if rings else RING_PLAN
    tilt = rng.uniform(0, 360) if tilt is None else tilt
    drift = math.radians(tilt + 200)
    out = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * 0.95)}" fill="{pale}" '
           f'opacity="0.40" filter="url(#bleed)"/>']
    n = len(plan)
    for ring_i, (rs, count) in enumerate(plan):
        base_col = mix(pale, deep, ring_i / (n - 1))
        base_ang = tilt + ring_i * 26 + rng.uniform(-7, 7)
        ox = cx + math.cos(drift) * r * 0.05 * ring_i
        oy = cy + math.sin(drift) * r * 0.05 * ring_i
        for i in range(count):
            a = base_ang + 360 * i / count + rng.uniform(-8, 8)
            L = r * rs * rng.uniform(0.90, 1.05)
            Wd = L * rng.uniform(0.64, 0.84)
            fill = mix(base_col, rng.choice((pale, deep)), rng.uniform(0, 0.20))
            out.append(petal(ox, oy, a, L, Wd, fill, rng.uniform(0.66, 0.86), edge=core))

    if throat == "speckle":
        # the template's ivory peonies have a dark speckled centre ringed with gold
        for _ in range(26):
            a = rng.uniform(0, 2 * math.pi)
            rr = rng.uniform(0, r * 0.20) ** 0.7 * (r * 0.20) ** 0.3
            col = SPECKLE if rng.random() < 0.55 else rng.choice(GOLD)
            out.append(f'<circle cx="{f(cx + math.cos(a) * rr)}" cy="{f(cy + math.sin(a) * rr)}" '
                       f'r="{f(rng.uniform(1.5, 3.2))}" fill="{col}" opacity="0.8"/>')
        for _ in range(10):
            a = rng.uniform(0, 2 * math.pi)
            r1, r2 = r * 0.10, r * rng.uniform(0.20, 0.30)
            out.append(f'<path d="M{f(cx + math.cos(a) * r1)},{f(cy + math.sin(a) * r1)} '
                       f'L{f(cx + math.cos(a) * r2)},{f(cy + math.sin(a) * r2)}" '
                       f'stroke="{rng.choice(GOLD)}" stroke-width="1.1" opacity="0.55" fill="none"/>')
    else:
        for k, rr in enumerate((0.20, 0.13, 0.07)):
            out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * rr)}" fill="none" '
                       f'stroke="{core}" stroke-width="{f(2.4 - k * 0.5)}" opacity="0.40"/>')
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * 0.05)}" fill="{core}" opacity="0.55"/>')
    return "".join(out)


def bud(rng, cx, cy, r, pale, deep, core):
    tilt = rng.uniform(0, 360)
    out = [f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * 0.88)}" fill="{pale}" '
           f'opacity="0.44" filter="url(#bleed)"/>']
    for i in range(3):  # calyx behind the petals
        out.append(petal(cx, cy, tilt + 120 * i, r * 1.12, r * 0.30, rng.choice(SAGE), 0.6))
    for ring_i, (rs, count) in enumerate(((1.0, 6), (0.68, 5), (0.42, 4))):
        base = tilt + ring_i * 30 + rng.uniform(-8, 8)
        col = mix(pale, deep, ring_i / 2)
        for i in range(count):
            a = base + 360 * i / count + rng.uniform(-9, 9)
            out.append(petal(cx, cy, a, r * rs * rng.uniform(0.9, 1.05), r * rs * 0.78,
                             col, rng.uniform(0.60, 0.80), edge=core))
    out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(r * 0.12)}" fill="{core}" opacity="0.5"/>')
    return "".join(out)


# ---------------------------------------------------------------- documents

HEADER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">
  <defs>
    <filter id="wc" x="-15%" y="-15%" width="130%" height="130%">
      <feTurbulence type="fractalNoise" baseFrequency="0.019" numOctaves="3" seed="{seed}" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <filter id="bleed" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="15"/>
    </filter>
  </defs>
'''


def top_right(rng):
    """Anchored top-right, spilling down and to the left."""
    g = []
    # long pointed branches sweep furthest out — laid down first, behind everything
    g.append(willow(rng, (980, 40), (760, 20), (520, 60), (250, 60), n=12, leaf_len=104))
    g.append(willow(rng, (990, 120), (800, 190), (560, 250), (300, 275), n=12, leaf_len=98))
    g.append(willow(rng, (930, 60), (990, 260), (960, 470), (830, 660), n=12, leaf_len=100))
    g.append(willow(rng, (860, 250), (740, 400), (660, 520), (560, 690), n=11, leaf_len=92, sweep=30))
    g.append(willow(rng, (1000, 210), (860, 120), (700, 150), (545, 175), n=9, leaf_len=80))
    # round eucalyptus filling the middle of the cluster
    g.append(eucalyptus(rng, (950, 90), (790, 175), (620, 235), (420, 250), n=13, leaf_r=35))
    g.append(eucalyptus(rng, (905, 45), (935, 215), (905, 385), (790, 530), n=12, leaf_r=33))
    g.append(eucalyptus(rng, (830, 230), (700, 330), (620, 430), (505, 545), n=11, leaf_r=29))
    g.append(eucalyptus(rng, (990, 330), (900, 420), (830, 470), (720, 520), n=9, leaf_r=26))
    g.append(berries(rng, (900, 165), (770, 205), (680, 225), (565, 205), n=8))
    g.append(berries(rng, (935, 330), (895, 430), (875, 500), (795, 575), n=7))
    g.append(berries(rng, (720, 70), (615, 105), (540, 120), (445, 110), n=6))
    # blooms — ivory dominant, blush as accent
    g.append(bloom(rng, 905, 120, 148, CREAM_PALE, CREAM_DEEP, CREAM_CORE,
                   throat="speckle", tilt=210))
    g.append(bloom(rng, 735, 155, 122, BLUSH_PALE, BLUSH_DEEP, BLUSH_CORE, tilt=40))
    g.append(bloom(rng, 925, 375, 128, CREAM_PALE, CREAM_DEEP, CREAM_CORE,
                   throat="speckle", tilt=95))
    g.append(bloom(rng, 620, 330, 84, BLUSH_PALE, BLUSH_DEEP, BLUSH_CORE, tilt=130, rings=4))
    g.append(bud(rng, 520, 150, 50, CREAM_PALE, CREAM_DEEP, CREAM_CORE))
    g.append(bud(rng, 780, 520, 56, BLUSH_PALE, BLUSH_DEEP, BLUSH_CORE))
    return "".join(g)


def bottom_left(rng):
    """Anchored bottom-left, rising up and to the right."""
    g = []
    g.append(willow(rng, (20, 960), (240, 985), (480, 945), (750, 945), n=12, leaf_len=104))
    g.append(willow(rng, (10, 880), (200, 810), (440, 750), (700, 725), n=12, leaf_len=98))
    g.append(willow(rng, (70, 940), (10, 740), (40, 530), (170, 340), n=12, leaf_len=100))
    g.append(willow(rng, (140, 750), (260, 600), (340, 480), (440, 310), n=11, leaf_len=92, sweep=30))
    g.append(willow(rng, (0, 790), (140, 880), (300, 850), (455, 825), n=9, leaf_len=80))
    g.append(eucalyptus(rng, (50, 910), (210, 825), (380, 765), (580, 750), n=13, leaf_r=35))
    g.append(eucalyptus(rng, (95, 955), (65, 785), (95, 615), (210, 470), n=12, leaf_r=33))
    g.append(eucalyptus(rng, (170, 770), (300, 670), (380, 570), (495, 455), n=11, leaf_r=29))
    g.append(eucalyptus(rng, (10, 670), (100, 580), (170, 530), (280, 480), n=9, leaf_r=26))
    g.append(berries(rng, (100, 835), (230, 795), (320, 775), (435, 795), n=8))
    g.append(berries(rng, (65, 670), (105, 570), (125, 500), (205, 425), n=7))
    g.append(berries(rng, (280, 930), (385, 895), (460, 880), (555, 890), n=6))
    g.append(bloom(rng, 95, 880, 148, CREAM_PALE, CREAM_DEEP, CREAM_CORE,
                   throat="speckle", tilt=30))
    g.append(bloom(rng, 265, 845, 122, BLUSH_PALE, BLUSH_DEEP, BLUSH_CORE, tilt=220))
    g.append(bloom(rng, 75, 625, 128, CREAM_PALE, CREAM_DEEP, CREAM_CORE,
                   throat="speckle", tilt=275))
    g.append(bloom(rng, 380, 670, 84, BLUSH_PALE, BLUSH_DEEP, BLUSH_CORE, tilt=310, rings=4))
    g.append(bud(rng, 480, 850, 50, CREAM_PALE, CREAM_DEEP, CREAM_CORE))
    g.append(bud(rng, 220, 480, 56, BLUSH_PALE, BLUSH_DEEP, BLUSH_CORE))
    return "".join(g)


def build(path, body_fn, seed):
    rng = random.Random(seed)
    svg = HEADER.format(size=SIZE, seed=seed)
    svg += f'  <g filter="url(#wc)">{body_fn(rng)}</g>\n</svg>\n'
    with open(path, "w") as fh:
        fh.write(svg)
    print(f"wrote {path}")


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    build(f"{out}/floral-top.svg", top_right, 11)
    build(f"{out}/floral-bottom.svg", bottom_left, 23)

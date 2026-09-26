#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo signals sheet: indicators, hazards, brake and reversing lights (A3 SVG)."""
import math
from common import *
from common import _ink                      # grey (probably) ink for to_earth()

header('Saab 99 Turbo, model 1979 — Indicators, hazards, brake and reversing lights')


def conn(x, y, h, lab, links=(), below=False):
    """In-line connector; links: row heights where the manual prints a through-link (a dot on both inner edges).
    lab: its name, one string per line, centred above it (below=True: under it)."""
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    for ry in links: inner([(x - 2, ry), (x + 2, ry)]); dot(x - 2, ry); dot(x + 2, ry)
    y0 = y + h / 2 + 3.1 if below else y - h / 2 - 1.5 - 2.7 * (len(lab) - 1)
    for i, s in enumerate(lab): txt(x, round(y0 + 2.7 * i, 2), s, 2.2, 'middle', fill='#555')


def fuse_box(y, n):
    """One fuse of fuse box 22, turned a quarter as on the radio sheet: the bar (junction ring) feeds the fuse,
    and its bottom terminal n is the dot on the box edge."""
    box(18, y - 8, 32, 16); txt(21, y - 3.4, f'<tspan font-weight="bold">Fuse {n}</tspan> · {FUSES[n]["rating"]}', 2.6)
    inner([(22, y - 2.2), (22, y + 6)]); contact(22, y)
    fa, fb = fuse(29, y - 1.2, 10, 2.4); inner([(22.8, y), fa]); inner([fb, (50, y)])
    dot(50, y); tlabel(48.6, y - 1.3, str(n), 'end')
    txt(24.5, y + 5.6, {'1-2': 'parking bar', '3-6': 'ignition-on bar', '7-12': 'always-live bar'}[FUSES[n]['bar']], 2.1, fill='#555')


def jdot(x, y):
    """Junction inside a part: smaller than a terminal dot."""
    A(f'<circle cx="{x}" cy="{y}" r=".6" fill="#111"/>')


def indicator(x, y, r, q):
    """Direction indicator bulb as the manual prints it: an X circle with two opposite quadrants filled black,
    left and right ('lr', front housings) or top and bottom ('tb', rear clusters). Same as the lighting sheet's."""
    k = round(r * .7071, 2); a, b = (round(x - k, 2), round(y - k, 2)), (round(x + k, 2), round(y + k, 2))
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    if q == 'lr':
        d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 0 {a[0]},{b[1]} Z M{x},{y} L{b[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{b[1]} Z'
    else:
        d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{a[1]} Z M{x},{y} L{a[0]},{b[1]} A{r},{r} 0 0 0 {b[0]},{b[1]} Z'
    A(f'<path d="{d}" fill="#111"/><path d="M{a[0]},{a[1]} L{b[0]},{b[1]} M{a[0]},{b[1]} L{b[0]},{a[1]}" stroke="#111" stroke-width=".45"/>')


def label(lx, ly, s):
    """A cable label in wire()'s style, for a run whose number has no row of its own in the data (75, 78)."""
    A(f'<rect x="{lx - .6}" y="{ly - 3.0}" width="{len(s) * 1.62 + 1.2}" height="3.8" fill="#fff" opacity=".85"/>')
    txt(lx, ly, s, 2.8)


def lab(c):
    """A cable's label as wire() prints it: number, colour, mm² from wires.csv."""
    r = WIRES[c]; return f"{c.split('#')[0]} {r['colour']} {r['mm2']}"


def mtag(x, y, lines, w, size=2.0):
    """Destination tag of several lines (common.tag() takes one), boxed as the lighting sheet's two-line tags:
    left edge x, centred on y, lines 1.36 × size apart. w: from the rendered text."""
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2)
    A(f'<rect x="{x}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines): txt(x + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)


def to_earth(x, y, dy=3, grey=False):
    """Where a rear cluster's earth bar leaves it: no earth lead is printed for the Combi Coupé's rear lights (the
    saloon's 189/189a are not on it; check R3), so it goes straight to common.earth()'s symbol. dy: the drop.
    grey=True: probably (the exit terminal, the drop and the symbol in _ink()'s grey)."""
    ey, c = y + dy, _ink(grey)
    A(f'<path d="M{x},{y} v{dy} M{x - 3},{ey} h6 M{x - 2},{ey + 1.3} h4 M{x - 1},{ey + 2.6} h2" '
      f'stroke="{c}" stroke-width=".5" fill="none"/>')
    A(f'<circle cx="{x}" cy="{y}" r="1.0" fill="{c}"/>')             # the exit terminal, dot()'s size


# ---- front lamp housings (FRONT, left of the sheet) and rear clusters (REAR, right) ----------
# Both groups have the car's right side at the top, as on the lighting sheet.
HXF, HW, HR = 70, 19.5, 5.5             # front housing: flat end x, length to the rounded end's tip, its radius
HXT = HXF + HW                          # the rounded end's tip, where the indicator's feed comes in
CX0, CW, CR = 346, 15, 3.4              # rear cluster: left edge, width, bulb radius
CB, BAR = CX0 + 6, CX0 + 11             # bulb centre x; the earth bar, about two-thirds across as printed


def front_housing(yc, n, side):
    """Front lamp housing (IMG_4714/4715) as the manual and the lighting sheet draw it: flat end on the left, rounded
    end on the right. The indicator sits in the rounded end, fed at its tip from the right; its earth runs left to the
    flat end (the housing's one earth, shared with parking light 13 and the lower bulb on the lighting sheet), crossing
    the thin lens chord without a join. The earth cable itself (360/361 SV) is drawn by the caller."""
    top, bot, xc, rc = yc - 7.5, yc + 7.5, HXT - HR, 2.2
    d = math.hypot(xc - HXF, 7.5); a = math.atan2(-7.5, xc - HXF) - math.acos(HR / d)
    tx, ty = xc - HR * math.cos(a), HR * math.sin(a)               # where the top edge meets the rounded end
    L = math.hypot(tx - HXF, 7.5 + ty); ux, uy = (tx - HXF) / L, (-7.5 - ty) / L
    p1x, p1y = HXF + rc * ux, top - rc * uy                         # start of the rounded corner on the top edge
    r2 = lambda v: round(v, 2)
    A(f'<path d="M{r2(tx)},{r2(yc + ty)} L{r2(p1x)},{r2(p1y)} Q{HXF},{top} {HXF},{top + rc} L{HXF},{bot - rc} '
      f'Q{HXF},{bot} {r2(p1x)},{r2(2 * yc - p1y)} L{r2(tx)},{r2(yc - ty)} A{HR},{HR} 0 0 0 {r2(tx)},{r2(yc + ty)} Z" '
      f'fill="#fafafa" stroke="#111" stroke-width=".8"/>')
    ch = HXF + 3.4; cy = top + (yc + ty - top) * (ch - HXF) / (tx - HXF)   # top edge's height at the chord
    # lens chord: housing, not a conductor, so thinner than inner() (.3, as on the lighting sheet)
    A(f'<path d="M{ch},{r2(cy + .4)} V{r2(2 * yc - cy - .4)}" stroke="#111" stroke-width=".3"/>')
    ri = 3.6
    inner([(HXT, yc), (xc - .5 + ri, yc)]); inner([(xc - .5 - ri, yc), (HXF, yc)])
    indicator(xc - .5, yc, ri, 'lr'); dot(HXT, yc); dot(HXF, yc)
    # caption beside the tip, above the feed cable (its label sits further along the cable)
    txt(HXT + 3.5, yc - 5.3, f'<tspan font-weight="bold">{n}</tspan> Front indicator, {side}', 2.5)
    txt(HXT + 3.5, yc - 2.4, 'in the front lamp housing with parking light 13', 2.0, fill='#555')


CH = 36                                 # rear cluster height: four bulbs, 9 apart


def rear_cluster(y0, side, bulbs, tail_feed):
    """Rear lamp cluster of the 3-door Combi Coupé (Charlie's car): four bulbs, probably in this order (1977/78 Turbo CC
    prints; the 1979 print draws the saloon's six-bulb unit, IMG_4727/4728), over the cluster's one earth bar, which
    starts at the top bulb's lead and leaves through the bottom border. The bar joining the bulbs is black (each bulb's
    row reads it); from the lowest bulb on, its way to earth is grey: nothing is printed for it on the CC (check R3).
    bulbs: (legend no., caption, kind), top to bottom; kind 'ind' (indicator), 'sig' (brake or reversing, fed here) or
    'tail' (fed on the lighting sheet: an open terminal on the outline, as the lighting sheet ends the signal feeds,
    and a caption naming its cable and fuse). tail_feed: (cable, fuse). Returns the four bulb rows, top to bottom."""
    box(CX0, y0, CW, CH)
    txt(CX0, y0 - 2.2, f'Rear lamp cluster, {side}', 2.4, w='bold')
    ys = [y0 + 4.5 + 9 * i for i in range(4)]
    for i, (yy, (n, cap, kind)) in enumerate(zip(ys, bulbs)):
        indicator(CB, yy, CR, 'tb') if kind == 'ind' else lamp(CB, yy, r=CR)
        cap = f'<tspan font-weight="bold">{n}</tspan> {cap}'
        if kind == 'tail':
            contact(CX0, yy); inner([(CX0 + .8, yy), (CB - CR, yy)])
            c, f = tail_feed
            txt(CX0 + 19, yy - .5, cap, 2.5)
            txt(CX0 + 19, yy + 2.7, f"{c} {WIRES[c]['colour']} from fuse {f} (lighting sheet)", 2.0, fill='#555')
        else:
            inner([(CX0, yy), (CB - CR, yy)]); txt(CX0 + 19, yy + .9, cap, 2.5)
        if i: inner([(CB + CR, yy), (BAR, yy)]); jdot(BAR, yy)
    inner([(CB + CR, ys[0]), (BAR, ys[0]), (BAR, ys[3])])
    inner([(BAR, ys[3]), (BAR, y0 + CH)], grey=True); to_earth(BAR, y0 + CH, grey=True); jdot(BAR, ys[3])
    return ys


# ---- indicators and hazards ---------------------------------------------------
txt(18, 40, 'Indicators and hazards', 3.4, w='bold')
fuse_box(62, 11)
wire('70', [(50, 62), (70, 62), (70, 66)], label=False); txt(52, 60.3, '70 RD/VT 1.0', 2.2)
# 23 flasher unit as printed (book photo P8, scan p.407): a box with the filled bow-tie (flasher symbol) under a strip
# with 49, C, 49a and 31 in a row along the top edge. 70 comes down into 49, 71 and 73 leave C and 49a upwards; the
# book draws 31 with no wire, so its earth here is grey (probably earthed through the flasher's mounting).
FX, FY, FW, FH, FD = 66, 66, 26, 30, 75          # box left, top, width, height; y of the strip's lower edge
T49, TC, T49A, T31 = 70, 76, 82, 88              # terminal x, left to right as printed
box(FX, FY, FW, FH); txt(FX - 2.5, 84, '23 Flasher unit', 2.4, 'end', w='bold')
A(f'<path d="M{FX},{FD} h{FW}" stroke="#111" stroke-width=".4"/>')
fm, fy = FX + FW / 2, (FD + FY + FH - .4) / 2   # bow-tie centre: corner to corner, into the border as printed
A(f'<path d="M{FX + .4},{FD} L{FX + FW - .4},{FD} L{fm},{fy} Z M{FX + .4},{FY + FH - .4} L{FX + FW - .4},{FY + FH - .4} '
  f'L{fm},{fy} Z" fill="#111" stroke="#111" stroke-width=".3" stroke-linejoin="round"/>')
for tx, tl in ((T49, '49'), (TC, 'C'), (T49A, '49a'), (T31, '31')): dot(tx, FY); tlabel(tx, FY + 3.6, tl, 'middle')
A(f'<path d="M{T31},{FY} V62 H100 v3 M97,65 h6 M98,66.3 h4 M99,67.6 h2" stroke="#888" stroke-width=".5" fill="none"/>')
PROBABLE[0] = True
t71 = '71 GN/VT 0.75 → 47 dash indicator lamp'
wire('71', [(TC, FY), (TC, 48), (73, 48)], label=False); tag(73, 48, t71, w=55, anchor='end')   # left edge on x 18, with the title and F11

# 25 hazard switch as printed (IMG_4724): + at the top, a blade hanging down-left from its pivot (open), and a
# column of three contacts it closes together when pressed: lamp (grey: printed merged with the blade root, probably
# open), R and L. The lamp's other side is an unlabelled terminal on the right edge, where two leads fork.
box(130, 48, 40, 40); txt(127, 75, '25 Hazard switch', 2.4, 'end', w='bold')
wire('73', [(T49A, FY), (T49A, 58), (114, 58), (114, 43), (144, 43), (149, 48)], 118, 41.5)   # lands on + beside 74 (probably)
wire('74', [(149, 48), (149, 36), (225, 36), (225, 48)], 178, 34.5)
dot(149, 48); txt(150.6, 51.8, '+', 2.2, fill='#555')
inner([(149, 48), (149, 57.2)]); contact(149, 58); blade(148.7, 58.64, 140.4, 76.8)
contact(150.6, 64.8); contact(150.6, 70.4); contact(150.6, 78)
lamp(158.6, 64.8, r=3.2); inner([(151.4, 64.8), (155.4, 64.8)]); inner([(161.8, 64.8), (170, 64.8)]); dot(170, 64.8)
inner([(151.4, 70.4), (160, 70.4), (160, 88)]); dot(160, 88); tlabel(161.6, 86.6, 'R')
inner([(151.4, 78), (155, 78), (155, 88)]); dot(155, 88); tlabel(153.4, 86.6, 'L', 'end')
# The lamp terminal's fork, as printed: 69 SV straight right and down to earth, 52 SV on a diagonal just above it to
# panel light connector 59 (59 (D11)), where 179 SV from 47:4 (instruments sheet) and the panel lamps' 54/56 SV share
# the pin: 69 is their earth too. The panel lamps are on no sheet.
wire('69', [(170, 64.8), (178, 64.8), (178, 70)], label=False); earth(178, 70)
txt(180.5, 68.8, lab('69'), 2.1)
wire('52', [(170, 64.8), (174, 60.8), (174, 52), (177, 52)], label=False)
mtag(177, 52, (f"{lab('52')} → panel light", 'connector 59: instrument earth', '179 (instruments sheet) and', 'panel lamps (not drawn)'), w=30)   # w from the rendered text

# 24 indicator switch as printed: 54 at the top, a lever hanging from its pivot, centre-off between R (left) and L.
box(210, 48, 30, 40); txt(243, 68, '24 Indicator switch', 2.4, w='bold')
dot(225, 48); tlabel(226.5, 55, '54'); inner([(225, 48), (225, 59.2)]); contact(225, 60); blade(225, 60.7, 225, 76.8)
contact(219, 76); inner([(219, 76.8), (219, 88)]); dot(219, 88); tlabel(217.4, 84, 'R', 'end')
contact(231, 76); inner([(231, 76.8), (231, 88)]); dot(231, 88); tlabel(232.6, 84, 'L')
# the hazard feeds land on 24's R and L terminals beside the lamp wires; 67 crosses 78 without a join
wire('68', [(160, 88), (160, 98), (214, 98), (214, 93), (219, 88)], 170, 96.5)
wire('67', [(155, 88), (155, 104), (226, 104), (226, 93), (231, 88)], 180, 102.5)
# 24's own outputs, 75 BL/VT (L) and 78 RD/VT (R), pass 58 (D8) (pins 11 and 10) and reach 58 (B9); 77/80 (front) leave
# them just before it and 76/79 (rear) carry on past it.
LB, RB = 101, 111                       # rows of 58 (D8) and 58 (B9): L (75/77/76) above R (78/80/79)
D8, B9 = 241, 285
wire('75', [(231, 88), (231, LB), (D8 - 2, LB)], label=False)
wire('78', [(219, 88), (219, RB), (D8 - 2, RB)], label=False)
conn(D8, (LB + RB) / 2, RB - LB + 7, ('stalk switch', 'connector 58'), links=(LB, RB), below=True)   # 58 (D8)
wire('75', [(D8 + 2, LB), (B9 - 2, LB)], 246, LB - 1.5)
wire('78', [(D8 + 2, RB), (B9 - 2, RB)], 246, RB - 1.5)
conn(B9, (LB + RB) / 2, RB - LB + 7, ('ignition switch', 'connector 58'), links=(LB, RB), below=True)   # 58 (B9)

# FRONT, on the left: the right housing (28) above the left one (27). As printed, the front cables leave 75's and 78's
# pins on 58 (B9)'s near side and only the rear ones (76, 79) pass it: 80 drops off 78's row, 77 off 75's (crossing
# 78's row, the one crossing it needs), and both run straight left under 58 (D8)'s name to the rounded ends.
# The earths: 361 SV to washer pump 63's earth terminal (on to joint 158 through 92 SV, wipers sheet), 360 SV to the
# main earth star.
txt(18, 108, 'FRONT', 3.6, w='bold', fill='#777'); txt(18, 112.5, 'car’s right side at top', 2.3, fill='#777')
FR, FL = 124, 146                       # centre lines of the right and left front housings
J80, J77 = 267, 273                     # where 80 and 77 leave 78 and 75, between 75/78's labels and 58 (B9)'s name
front_housing(FR, 28, 'right')
wire('80', [(J80, RB), (J80, FR), (HXT, FR)], 150, FR - 1.5); dot(J80, RB)
t361 = f"361 {WIRES['361']['colour']} {WIRES['361']['mm2']} → washer pump 63 (wipers sheet)"
wire('361', [(HXF, FR), (HXF - 8, FR)], label=False); tag(HXF - 8, FR, t361, w=44, size=2.0, anchor='end')
front_housing(FL, 27, 'left')
wire('77', [(J77, LB), (J77, FL), (HXT, FL)], 150, FL - 1.5); dot(J77, LB)
wire('360', [(HXF, FL), (HXF - 8, FL), (HXF - 8, FL + 3)], label=False); earth(HXF - 8, FL)
txt(HXF - 13.5, FL + 4.4, f"360 {WIRES['360']['colour']} {WIRES['360']['mm2']}", 2.1, 'end')

# REAR, on the right: the Combi Coupé's four-bulb lights in the data's order, the right cluster above the left one as
# on the lighting sheet (the left one is the vertical mirror of the right: indicator at the bottom, reversing at the
# top). The right cluster's indicator row is 79's row, so 79 runs straight in; the left cluster's brake row is 132's row
# (brake section below). 76 comes down outside the other feeds, so the crossings are four: 76 with 79, 132 and 136,
# and 132 with 136 (the left cluster prints reversing above brake, while 136 comes up from below 132).
txt(405, 92, 'REAR', 3.6, 'end', w='bold', fill='#777'); txt(405, 96.5, 'Combi Coupé (this car)', 2.3, 'end', fill='#777')
C76, C133, C136 = 297, 309, 320         # risers: 76, then 133 and 136/137, left to right
yr = rear_cluster(RB - 4.5, 'right', (('28', 'Rear indicator, right', 'ind'), ('14', 'Tail light, right', 'tail'),
                                     ('30', 'Brake light, right', 'sig'), ('32', 'Reversing light, right', 'sig')), ('44', 2))
wire('79', [(B9 + 2, RB), (CX0, RB)], 301, RB - 1.5)
Y12 = 179.5                             # fuse 12's row: 131, 132 and the left brake light
yl = rear_cluster(Y12 - 13.5, 'left', (('32', 'Reversing light, left', 'sig'), ('30', 'Brake light, left', 'sig'),
                                       ('14', 'Tail light, left', 'tail'), ('27', 'Rear indicator, left', 'ind')), ('42', 1))
wire('76', [(B9 + 2, LB), (C76, LB), (C76, yl[3]), (CX0, yl[3])], 323, yl[3] - 1.5)

# ---- brake and reversing lights ---------------------------------------------------
txt(18, 164, 'Brake and reversing lights', 3.4, w='bold')
fuse_box(Y12, 12)
wire('131', [(50, Y12), (90, Y12)], 55, Y12 - 1.5)
# 29 brake light switch: a blade rising from the left terminal; the print runs its end into the right contact, so
# the free end and that contact are grey (probably open: it closes when the pedal is pressed)
box(90, 171.5, 24, 14); txt(102, 168.5, '29 Brake light switch', 2.4, 'middle', w='bold')
inner([(90, Y12), (92.4, Y12)]); contact(93.2, Y12)
blade(93.85, 179.24, 99.6, 176.9); blade(99.6, 176.9, 106, 174.33, grey=True)
contact(111, Y12, grey=True); inner([(111.8, Y12), (114, Y12)]); dot(90, Y12); dot(114, Y12)
wire('132', [(114, Y12), (158, Y12)], 120, Y12 - 1.5)
# 58 (E12): rows 2, 3 and 4 (132, 135, 138); row 1 (140 GL, interior sheet) is not drawn
Y3, Y138 = 201, 223.7                   # fuse 3's row (135), 138's row
conn(160, 201.6, 55.2, ('brake and reversing', 'light connector 58'), links=(Y12, Y3, Y138))   # 58 (E12)
# 132 runs straight on to the left brake light; 133 leaves that feed for the right one, directly (the Combi Coupé has
# no tail jumper at the left light), rising inside 76 and left of 136/137.
wire('132', [(162, Y12), (CX0, Y12)], 200, Y12 - 1.5)
wire('133', [(C133, Y12), (C133, yr[2]), (CX0, yr[2])], 318, yr[2] - 1.5); dot(C133, Y12)
fuse_box(Y3, 3)
wire('135', [(50, Y3), (158, Y3)], 55, Y3 - 1.5)
wire('135', [(162, Y3), (202, Y3), (202, 205)], label=False)
# 31 reversing light switch as printed: portrait, blade hanging from the top terminal, open; a link from the
# left border to the bottom (switched) contact, where 138 BL comes in with no terminal circle printed
box(196, 205, 12, 21); txt(211, 217, '31 Reversing light switch', 2.4, w='bold')
dot(202, 205); inner([(202, 205), (202, 206.7)]); contact(202, 207.5); blade(202.24, 208.16, 206.5, 220)
contact(202, Y138); inner([(202, 224.5), (202, 226)]); dot(202, 226); inner([(196, Y138), (201.2, Y138)])
# 138 BL: from 31's switched side back through 58 (E12) row 4, on to 58 (E2) and the front housings' lower bulbs
wire('138', [(196, Y138), (162, Y138)], 166, Y138 - 1.5)
wire('138', [(158, Y138), (138, Y138)], label=False)
t138 = '→ via front lamp connector 58 to the side back-up lights (lighting sheet)'   # 58 (E2)
tag(138, Y138, t138, w=86, anchor='end')
# 136 goes on to the left reversing light; 137 leaves that feed for the right one, directly: it carries on up 136's riser
# from the corner where 136 turns in to the left cluster (above 132's run, so 137 does not cross it)
wire('136', [(202, 226), (202, 231), (C136, 231), (C136, yl[0]), (CX0, yl[0])], 230, 229.5)
wire('137', [(C136, yl[0]), (C136, yr[3]), (CX0, yr[3])], 324, yr[3] - 1.5); dot(C136, yl[0])

# terminal dots again, on top of the wire ends that meet them
for p in ((50, 62), (T49, FY), (TC, FY), (T49A, FY), (T31, FY), (149, 48), (170, 64.8), (155, 88), (160, 88), (225, 48),
          (219, 88), (231, 88), (D8 - 2, LB), (D8 + 2, LB), (D8 - 2, RB), (D8 + 2, RB), (B9 - 2, LB), (B9 + 2, LB),
          (B9 - 2, RB), (B9 + 2, RB), (HXT, FR), (HXT, FL), (HXF, FR), (HXF, FL), (50, Y12), (90, Y12),
          (114, Y12), (158, Y12), (162, Y12), (50, Y3), (158, Y3), (162, Y3), (158, Y138), (162, Y138),
          (202, 205), (202, 226), (196, Y138)) + tuple((CX0, y) for y in (yl[0], yl[1], yl[3], yr[0], yr[2], yr[3])):
    dot(*p)

# ---- legend and notes ---------------------------------------------------------------
lx, ly = 18, 240
box(lx, ly, 389, 47, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 4
size_legend(x, ly + 18)                               # line widths, under the colours
y = ly + 24                                           # text baseline of the status row: traced, then the dashed sample or the tick
A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x + 48},{y - 1} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 59, y, 'not traced yet', 2.4)
def ticked(tx, ty): tick(tx, ty - .7); txt(tx + 4, ty, 'checked on the car', 2.4)   # the check mark sample, text baseline ty
if TICKED[0] and not DASHED[0]: ticked(x + 48, y)    # beside 'traced' when the dashed sample leaves room
if probable_legend(x, y + 5): y += 6
if TICKED[0] and DASHED[0]:                           # else after the grey sample (4th colour column), or a row of its own
    if PROBABLE[0]: ticked(x + 69, y)
    else: y += 6; ticked(x, y)
notes = ['Flasher 23 is fed on 49 from fuse 11 (always-live bar). 49a (73 GN) feeds the hazard switch’s +, which feeds the indicator switch’s 54; '
         'C (71 GN/VT) works the dash indicator lamp. Its 31 is probably earthed through the mounting (grey).',
         'Switches are drawn at rest. Pressed, hazard switch 25 closes its lamp, R and L contacts together, so + feeds both sides (68 RD/VT, 67 BL/VT).',
         'Terminals: hazard switch 25 has +, R, L and one for its lamp (markings: check D4); indicator switch 24 has 54, R and L. '
         '73 GN and 74 GN both land on + (probably the same terminal).',
         '25’s lamp contact is open at rest: the lamp stays dark with the indicators and blinks with the hazards (check D7). '
         'Grey: the end of 29’s blade and its right contact; probably open at rest.',
         '25’s lamp terminal: 69 SV goes to earth and 52 SV to panel light connector 59, where the instrument earth (179 from 47) '
         'and the panel lamps join it, so 69 earths them too.',
         '24’s own outputs are 75 BL/VT and 78 RD/VT, through stalk switch connector 58 to ignition switch connector 58. 77/80 (front) leave '
         'them just before ignition switch connector 58; only 76/79 (rear, route not traced yet) pass it.',
         'Front lamps on the left, rear lights on the right, the car’s right side at the top, as on the lighting sheet. Each lamp housing has one earth '
         'for all its bulbs; the parking lights and the tail-light feeds are on the lighting sheet.',
         'Rear lamp clusters (3-door Combi Coupé): four bulbs each, probably in the order drawn. No earth lead is printed for them (check R3): each bar goes to earth in grey.',
         '132 and 136 run to the left cluster; 133 and 137 leave its brake and reversing feeds for the right one (at the cluster, probably; the dots are drawn short of it, for room).',
         '138 BL, from 31’s switched side, feeds the front housings’ side back-up lights (check E16).',
         'Brake and reversing light connector 58: 132, 135 and 138 pass on its pins 2, 3 and 4 (counted top to bottom); pin 1 is 140 GL (interior sheet).',
         'Not RHD-specific: circuits should match the car, but harness routing and part positions may differ.']
# Sources, not printed: 74 GN 1.0 has its second digit blotted on the 1979 print; the 1977 Turbo diagram and another
# year's print read 74. The manual prints 25's terminals +, R, L (none on the lamp's), 29's blade end running into its
# right contact, 25's lamp contact merged into the blade root, no pin numbers on 58 (E12), and the left rear cluster
# mirrored. The front housings are drawn the way it prints them (flat end on the left).
for j, n in enumerate(notes): txt(lx + 108, round(ly + 5.3 + j * 3.6, 2), n, 2.35, fill='#333')   # 12 lines: 3.6 pitch fits the box
save('signals.svg')

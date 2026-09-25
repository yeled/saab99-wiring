#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo signals sheet: indicators, hazards, brake and reversing lights (A3 SVG)."""
import math
from common import *

header('Saab 99 Turbo, model 1979 — Indicators, hazards, brake and reversing lights',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual.')


def conn(x, y, h, lab, links=()):
    """In-line connector; links: row heights where the manual prints a through-link (a dot on both inner edges)."""
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    for ry in links: inner([(x - 2, ry), (x + 2, ry)]); dot(x - 2, ry); dot(x + 2, ry)
    txt(x, y - h / 2 - 1.5, lab, 2.2, 'middle', fill='#555')


def fuse_box(y, n):
    """One fuse of fuse box 22, turned a quarter as on the radio sheet: the bar (junction ring) feeds the fuse,
    and its bottom terminal n is the dot on the box edge."""
    box(18, y - 8, 32, 16); txt(21, y - 3.4, f'<tspan font-weight="bold">F{n}</tspan> · {FUSES[n]["rating"]}', 2.6)
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


def stub(x, y, dx=0, dy=2):
    """Where a cable that is not in the data yet leaves a part (138 BL at 31): a short plain lead."""
    A(f'<path d="M{x},{y} l{dx},{dy}" stroke="#111" stroke-width=".5" fill="none"/>')


def to_earth(x, y, dx=0, dy=3):
    """Where a housing's earth leaves it: its cable is not in the data yet, so it goes straight to common.earth()'s
    symbol, as on the lighting sheet. dx: a sideways lead first (front housings), one path with the drop so the corner
    is closed; dy: the drop, shorter under the left rear cluster, where the right front housing sits close below."""
    ex, ey = x + dx, y + dy
    A(f'<path d="M{x},{y} h{dx} v{dy} M{ex - 3},{ey} h6 M{ex - 2},{ey + 1.3} h4 M{ex - 1},{ey + 2.6} h2" '
      f'stroke="#111" stroke-width=".5" fill="none"/>')


# ---- front lamp housings and rear clusters (right-hand column) ---------------------
HX0, HXF, HR = 336.5, 356, 5.5          # front housing: rounded end's tip, flat end, radius of the rounded end
CX0, CW, CB, CR = 340, 15, 346, 3.4     # rear cluster: left edge, width, bulb centre x, bulb radius
BAR = 351                               # rear cluster earth bar, about two-thirds across as printed


def front_housing(yc, n, side):
    """Front lamp housing (IMG_4714/4715), mirrored so the feed comes in through the rounded end from the left (the
    manual, and the lighting sheet, have the flat end on the left): the indicator sits in the rounded end, its earth
    runs to the flat end (the housing's one earth, shared with parking light 13 and the lower bulb on the lighting
    sheet), crossing the thin lens chord without a join."""
    top, bot, xc, rc = yc - 7.5, yc + 7.5, HX0 + HR, 2.2
    d = math.hypot(HXF - xc, 7.5); a = math.atan2(-7.5, HXF - xc) - math.acos(HR / d)
    tx, ty = xc + HR * math.cos(a), HR * math.sin(a)               # where the top edge leaves the rounded end
    L = math.hypot(HXF - tx, 7.5 + ty); ux, uy = (HXF - tx) / L, (-7.5 - ty) / L
    p1x, p1y = HXF - rc * ux, top - rc * uy                         # start of the rounded corner on the top edge
    r2 = lambda v: round(v, 2)
    A(f'<path d="M{r2(tx)},{r2(yc + ty)} L{r2(p1x)},{r2(p1y)} Q{HXF},{top} {HXF},{top + rc} L{HXF},{bot - rc} '
      f'Q{HXF},{bot} {r2(p1x)},{r2(2 * yc - p1y)} L{r2(tx)},{r2(yc - ty)} A{HR},{HR} 0 0 1 {r2(tx)},{r2(yc + ty)} Z" '
      f'fill="#fafafa" stroke="#111" stroke-width=".8"/>')
    ch = 352.6; cy = top + (yc + ty - top) * (HXF - ch) / (HXF - tx)   # top edge's height at the chord
    # lens chord: housing, not a conductor, so thinner than inner() (.3, as on the lighting sheet)
    A(f'<path d="M{ch},{r2(cy + .4)} V{r2(2 * yc - cy - .4)}" stroke="#111" stroke-width=".3"/>')
    ri = 3.6
    inner([(HX0, yc), (xc + .5 - ri, yc)]); inner([(xc + .5 + ri, yc), (HXF, yc)])
    indicator(xc + .5, yc, ri, 'lr'); dot(HX0, yc); dot(HXF, yc); to_earth(HXF, yc, 4.5)
    txt(366, yc - .4, f'<tspan font-weight="bold">{n}</tspan> Front indicator, {side}', 2.5)
    txt(366, yc + 3.2, 'in the front lamp housing with parking light 13', 2.0, fill='#555')


def rear_cluster(y0, side, bulbs):
    """Rear lamp cluster (IMG_4727/4728): the signal bulbs over the cluster's one earth bar, which starts at the
    indicator's lead and leaves through the border. bulbs: (legend no., caption, is_indicator), top to bottom."""
    box(CX0, y0, CW, 27)
    txt(CX0, y0 - 2.2, f'Rear lamp cluster, {side}', 2.4, w='bold')
    ys = [y0 + 4.5 + 9 * i for i in range(3)]
    for yy, (n, cap, ind) in zip(ys, bulbs):
        indicator(CB, yy, CR, 'tb') if ind else lamp(CB, yy, r=CR)
        inner([(CX0, yy), (CB - CR, yy)]); dot(CX0, yy)
        if not ind: inner([(CB + CR, yy), (BAR, yy)]); jdot(BAR, yy)
        txt(359, yy + .9, f'<tspan font-weight="bold">{n}</tspan> {cap}', 2.5)
    inner([(CB + CR, ys[0]), (BAR, ys[0]), (BAR, y0 + 27)]); dot(BAR, y0 + 27); to_earth(BAR, y0 + 27, dy=2)
    return ys


# ---- indicators and hazards ---------------------------------------------------
txt(18, 40, 'Indicators and hazards', 3.4, w='bold')
fuse_box(62, 11)
wire('70', [(50, 62), (70, 62)], label=False); txt(52, 60.3, '70 RD/VT 1.0', 2.2)
box(70, 50, 30, 30); txt(85, 65, '23', 3.2, 'middle', w='bold'); txt(85, 70, 'Flasher unit', 2.3, 'middle')
dot(70, 62); txt(72, 59.5, '49', 2.2, fill='#555'); dot(100, 58); txt(98, 56.5, '49a', 2.2, 'end', fill='#555')
dot(80, 80); txt(80, 78, 'C', 2.2, 'middle', fill='#555'); dot(92, 80); txt(92, 78, '31', 2.2, 'middle', fill='#555')
A('<path d="M92,80 v5" stroke="#111" stroke-width=".6"/>'); earth(92, 85)
t71 = '71 GN/VT 0.75 → 47 dash indicator lamp'
wire('71', [(80, 80), (80, 96)], label=False); tag(82, 96, t71, w=len(t71) * 2.6 * .52 + 3)

# 25 hazard switch as printed (IMG_4724): + at the top, a blade hanging down-left from its pivot (open), and a
# column of three contacts it closes together when pressed: lamp (grey: printed merged with the blade root, probably
# open), R and L. The lamp is wired to an unlabelled terminal on the right edge.
box(130, 48, 40, 40); txt(127, 75, '25 Hazard switch', 2.4, 'end', w='bold')
wire('73', [(100, 58), (114, 58), (114, 43), (144, 43), (149, 48)], 118, 41.5)   # lands on + beside 76 (probably)
wire('76#hazard', [(149, 48), (149, 36), (225, 36), (225, 48)], 178, 34.5)
dot(149, 48); txt(150.6, 51.8, '+', 2.2, fill='#555')
inner([(149, 48), (149, 57.2)]); contact(149, 58); blade(148.7, 58.64, 140.4, 76.8)
contact(150.6, 64.8); contact(150.6, 70.4); contact(150.6, 78)
lamp(158.6, 64.8, r=3.2); inner([(151.4, 64.8), (155.4, 64.8)]); inner([(161.8, 64.8), (170, 64.8)]); dot(170, 64.8)
inner([(151.4, 70.4), (160, 70.4), (160, 88)]); dot(160, 88); tlabel(161.6, 86.6, 'R')
inner([(151.4, 78), (155, 78), (155, 88)]); dot(155, 88); tlabel(153.4, 86.6, 'L', 'end')
wire('52', [(170, 64.8), (178, 64.8), (178, 70)], label=False); earth(178, 70)
txt(180.5, 68.8, f"52 {WIRES['52']['colour']} {WIRES['52']['mm2']}", 2.1)

# 24 indicator switch as printed: 54 at the top, a lever hanging from its pivot, centre-off between R (left) and L.
box(210, 48, 30, 40); txt(243, 68, '24 Indicator switch', 2.4, w='bold')
dot(225, 48); tlabel(226.5, 55, '54'); inner([(225, 48), (225, 59.2)]); contact(225, 60); blade(225, 60.7, 225, 76.8)
contact(219, 76); inner([(219, 76.8), (219, 88)]); dot(219, 88); tlabel(217.4, 84, 'R', 'end')
contact(231, 76); inner([(231, 76.8), (231, 88)]); dot(231, 88); tlabel(232.6, 84, 'L')
# the hazard feeds land on 24's R and L terminals beside the lamp wires; 67 crosses 80 without a join
wire('68', [(160, 88), (160, 98), (214, 98), (214, 93), (219, 88)], 170, 96.5)
wire('67', [(155, 88), (155, 104), (226, 104), (226, 93), (231, 88)], 180, 102.5)
wire('77', [(231, 88), (231, 110), (268, 110)], label=False); conn(270, 110, 7, '58 (B9)')
wire('80', [(219, 88), (219, 122), (268, 122)], label=False); conn(270, 122, 7, '')

# lamps: left side (front, rear cluster), then right side
front_housing(91, 27, 'left')
wire('77', [(272, 110), (312, 110), (312, 91), (HX0, 91)], 284, 108.5)
wire('76', [(312, 110), (CX0, 110)], 314, 108.5); dot(312, 110)
# The manual prints the left cluster as the mirror image of the right (indicator at the bottom); here both read
# the same way down, as on the lighting sheet.
yl = rear_cluster(105.5, 'left', (('27', 'Rear indicator, left', True), ('30', 'Brake light, left', False),
                                  ('32', 'Reversing light, left', False)))
front_housing(146, 28, 'right')
wire('80', [(272, 122), (282, 122), (282, 146), (HX0, 146)], 280.4, 145.4, rot=-90)
wire('79', [(316, 146), (316, 164.5), (CX0, 164.5)], 318.5, 163); dot(316, 146)
yr = rear_cluster(160, 'right', (('28', 'Rear indicator, right', True), ('30', 'Brake light, right', False),
                                 ('32', 'Reversing light, right', False)))

# ---- brake and reversing lights ---------------------------------------------------
txt(18, 158, 'Brake and reversing lights', 3.4, w='bold')
fuse_box(173.5, 12)
wire('131', [(50, 173.5), (90, 173.5)], 55, 172)
# 29 brake light switch: a blade rising from the left terminal; the print runs its end into the right contact, so
# the free end and that contact are grey (probably open: it closes when the pedal is pressed)
box(90, 165.5, 24, 14); txt(102, 162.5, '29 Brake light switch', 2.4, 'middle', w='bold')
inner([(90, 173.5), (92.4, 173.5)]); contact(93.2, 173.5)
blade(93.85, 173.24, 99.6, 170.9); blade(99.6, 170.9, 106, 168.33, grey=True)
contact(111, 173.5, grey=True); inner([(111.8, 173.5), (114, 173.5)]); dot(90, 173.5); dot(114, 173.5)
wire('132', [(114, 173.5), (158, 173.5)], 120, 172)
conn(160, 184.25, 32.5, '58 (E12)', links=(173.5, 195))
wire('133', [(162, 173.5), (CX0, 173.5)], 200, 172)
wire('133', [(296, 173.5), (296, yl[1]), (CX0, yl[1])], label=False); dot(296, 173.5)
fuse_box(195, 3)
wire('135', [(50, 195), (158, 195)], 55, 193.5)
wire('135', [(162, 195), (202, 195), (202, 199)], label=False)
# 31 reversing light switch as printed: portrait, blade hanging from the top terminal, open; a link from the
# left border to the bottom terminal, where 138 BL comes in with no terminal circle (138 is not in the data yet,
# so a short lead outside the border)
box(196, 199, 12, 21); txt(211, 211, '31 Reversing light switch', 2.4, w='bold')
dot(202, 199); inner([(202, 199), (202, 200.7)]); contact(202, 201.5); blade(202.24, 202.16, 206.5, 214)
contact(202, 217.7); inner([(202, 218.5), (202, 220)]); dot(202, 220); inner([(196, 217.7), (201.2, 217.7)])
stub(196, 217.7, -2.5, 0)
wire('136', [(202, 220), (202, 225), (306, 225), (306, yl[2]), (CX0, yl[2])], 230, 223.5)
wire('137', [(306, yr[2]), (CX0, yr[2])], 310, 181); dot(306, yr[2])

# terminal dots again, on top of the wire ends that meet them
for p in ((50, 62), (70, 62), (100, 58), (80, 80), (92, 80), (149, 48), (170, 64.8), (155, 88), (160, 88), (225, 48),
          (219, 88), (231, 88), (HX0, 91), (HX0, 146), (50, 173.5), (90, 173.5), (114, 173.5), (158, 173.5), (162, 173.5),
          (50, 195), (158, 195), (162, 195), (202, 199), (202, 220)) + tuple((CX0, y) for y in yl + yr):
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
A(f'<path d="M{x},{ly + 17} h9" stroke="#222" stroke-width="1.2"/>'); txt(x + 11, ly + 18, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x + 48},{ly + 17} h9" stroke="#222" stroke-width="1.2" stroke-dasharray="3 2"/>'); txt(x + 59, ly + 18, 'not traced yet', 2.4)
if TICKED[0]: tick(x, ly + 23.3); txt(x + 4, ly + 24, 'checked on the car', 2.4)
probable_legend(x, ly + (29 if TICKED[0] else 23))
notes = ['The flasher is fed from fuse 11 on the always-live bar. Its output (73 GN) goes to the hazard switch’s +, which feeds the indicator switch’s 54.',
         'Switches are drawn at rest, as printed. Pressed, hazard switch 25 closes its lamp, R and L contacts together (lamp: on the car), so + feeds both sides (68 RD/VT, 67 BL/VT).',
         'The manual prints 25’s terminals +, R and L (none on the lamp’s) and 24’s 54, R and L. 73 GN lands on + beside the wire to 54 (probably the same terminal).',
         '25’s lamp contact prints merged into the blade root; on the car it is open at rest (the lamp stays dark with the indicators and blinks with the hazards: check D7). '
         'Grey: the end of 29’s blade and its right contact, printed running together; probably open at rest.',
         'The + to 54 wire is shown as 76 GN, as in the data; its second digit is blotted on the page, so the clash with 76 BL/VT is not confirmed. '
         'Rear indicator wires 76 and 79 leave connector 58 (B9) on its far side; their route to the rear isn’t traced yet.',
         'Each lamp housing has one earth for all its bulbs (parking, tail and number-plate bulbs: lighting sheet). Turned for the layout: the manual prints '
         'the front housings mirrored (flat end and earth on the left) and the left rear cluster upside down.',
         'Not in the data yet: the earth cables (front 360/361 SV; rear 189 SV, left cluster bar to right, then 189a SV to earth), drawn straight to earth here; '
         'and 138 BL, which enters 31’s left side onto the lower contact (a short lead here).',
         '58 (E12): 132 and 135 pass on its rows 2 and 3; row 1 is 140 GL (interior sheet) and row 4 is 138 BL. The manual prints no pin numbers.',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 4.5, n, 2.35, fill='#333')
save('signals.svg')

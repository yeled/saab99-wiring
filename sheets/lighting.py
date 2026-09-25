#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo lighting sheet (A3 landscape SVG).

Layout lives here; wire identity, colour, size and status come from
data/wires.csv, so editing the CSV (e.g. status -> car) updates the drawing.
"""
import math
from common import *

header('Saab 99 Turbo, model 1979 — Lighting circuit',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual. Front of car at left; car’s right side at top.')
txt(16, 40, 'FRONT', 3.6, w='bold', fill='#777'); txt(398, 91, 'REAR', 3.6, 'end', w='bold', fill='#777')


def jdot(x, y):
    """Junction inside a part: smaller than a terminal dot."""
    A(f'<circle cx="{x}" cy="{y}" r=".6" fill="#111"/>')


def indicator(x, y, r, q):
    """Direction indicator bulb as the manual prints it: an X circle with two opposite quadrants filled black,
    left and right ('lr', front housings) or top and bottom ('tb', rear clusters)."""
    k = round(r * .7071, 2); a, b = (x - k, y - k), (x + k, y + k)
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    if q == 'lr':
        d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 0 {a[0]},{b[1]} Z M{x},{y} L{b[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{b[1]} Z'
    else:
        d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{a[1]} Z M{x},{y} L{a[0]},{b[1]} A{r},{r} 0 0 0 {b[0]},{b[1]} Z'
    A(f'<path d="{d}" fill="#111"/><path d="M{a[0]},{a[1]} L{b[0]},{b[1]} M{a[0]},{b[1]} L{b[0]},{a[1]}" stroke="#111" stroke-width=".45"/>')


# ---- front lamps -------------------------------------------------------
hx = 45                              # x of the headlamp bulbs and of the housings' small bulbs


def housing(xf, xc, yc, hf, rr, s, ch):
    """Lamp housing as printed (IMG_4714/4715): a heavy outline, tallest at the front (x = xf, half-height hf), whose top
    and bottom edges run to a rounded rear end (centre xc, radius rr); the front bulges out by s. A thin lens chord at
    x = ch joins top and bottom; it is housing, not a conductor, and leads cross it plainly.
    Returns the front's outer x and edge(x) -> (y of the top edge, y of the bottom edge)."""
    top, bot = yc - hf, yc + hf
    a = math.atan2(-hf, xf - xc) + math.acos(rr / math.hypot(xf - xc, hf))    # where the top edge meets the rounded end
    tx, ty = round(xc + rr * math.cos(a), 2), round(yc + rr * math.sin(a), 2)
    k = (ty - top) / (tx - xf)
    edge = lambda x: (round(top + k * (x - xf), 2), round(bot - k * (x - xf), 2))
    rb = round((hf * hf + s * s) / (2 * s), 2)
    A(f'<path d="M{xf},{top} L{tx},{ty} A{rr},{rr} 0 0 1 {tx},{round(2 * yc - ty, 2)} L{xf},{bot} '
      f'A{rb},{rb} 0 0 1 {xf},{top} Z" fill="#fdfdfd" stroke="#111" stroke-width=".8"/>')
    t, b = edge(ch)
    A(f'<path d="M{ch},{round(t + .4, 2)} V{round(b - .4, 2)}" stroke="#111" stroke-width=".3"/>')
    return round(xf - s, 2), edge


def filament(x0, x1, y, s):
    """Filament arc from (x0, y) to (x1, y), x0 < x1, sagging s mm down the page (s < 0 bows it up)."""
    R = round(((x1 - x0) ** 2 / 4 + s * s) / (2 * abs(s)), 2)
    A(f'<path d="M{x0},{y} A{R},{R} 0 0 {0 if s > 0 else 1} {x1},{y}" fill="none" stroke="#111" stroke-width=".4"/>')


def headlamp(y, cap):
    """Twin-filament headlamp 11/12 in its housing (IMG_4714/4715), mirrored so the main/dip feeds come in through the
    rounded end on the right and the common leaves through the front. The manual prints both arcs (black: the upper
    sags, the lower bows up) but not which arc joins which lead, so those short joins are grey.
    Returns (main feed, dip feed, common), all on the housing outline."""
    r, a, rr, e = 5.5, 3, 7.6, 3.2   # bulb radius, feeds 3 mm above/below centre, rounded end radius, arc half-width
    xo, _ = housing(34, hx, y, 10, rr, 2.2, 36)
    A(f'<circle cx="{hx}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    xr, xh = round(hx + (r * r - a * a) ** .5, 2), round(hx + (rr * rr - a * a) ** .5, 2)   # bulb rim, outline
    for sy in (-1, 1):
        filament(hx - e, hx + e, y + sy * a, -sy * 1.5)                                   # both toward the centre
        inner([(xh, y + sy * a), (xr, y + sy * a)])                                        # feed to the bulb: read
        inner([(xr, y + sy * a), (hx + e, y + sy * a)], grey=True)                         # which arc: not printed
        inner([(hx - e, y + sy * a), (hx - r, y)], grey=True)
    inner([(hx - r, y), (xo, y)])                                                          # common, across the chord
    txt(hx, y - 12.2, cap, 2.7, 'middle')
    return (xh, y - a), (xh, y + a), (xo, y)


def small_bulb(x, y, r, top):
    """Plain bulb as printed in the front housings: a circle with one filament arc, near its top and sagging toward
    the centre (top=True: parking bulb 13) or near its bottom and bowing up (the unnumbered lower bulb)."""
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    k = -1 if top else 1
    filament(round(x - r * .866, 2), round(x + r * .866, 2), round(y + k * r * .5, 2), round(-k * r * .35, 2))


def front_housing(yc, cap, ind):
    """Front lamp housing 13 as printed (IMG_4714/4715): parking bulb 13 above an unnumbered bulb, indicator 27/28 to
    the right, one common earth line out of the front (crossing the lens chord). The lower bulb's and the indicator's
    feeds are not drawn here: open terminals on the outline.
    Returns where 45/43 meets the outline and the top of the parking bulb."""
    xi, rs, ri = 54, 2.6, 4
    xo, edge = housing(36, 56, yc, 9.5, 6.5, 2.4, 38.5)
    inner([(xi - ri, yc), (xo, yc)])                                               # common earth, through the bulbs' joint
    yo = edge(hx)[1]
    inner([(hx, yc + 2 * rs), (hx, round(yo - .8, 2))]); contact(hx, yo)           # lower bulb feed (not in the data)
    inner([(xi + ri, yc), (61.7, yc)]); contact(62.5, yc)                          # indicator feed: signals sheet
    small_bulb(hx, yc - rs, rs, True); small_bulb(hx, yc + rs, rs, False); indicator(xi, yc, ri, 'lr'); jdot(hx, yc)
    lamp_earth(xo, yc); dot(xo, yc)
    txt(64.5, yc + .8, f'{ind} indicator: signals sheet', 2.1, fill='#555')
    txt(49, yc + 13.7, cap, 2.7, 'middle')
    txt(49, yc + 16.9, 'with an unnumbered bulb below', 2.1, 'middle', fill='#555')
    return (hx, edge(hx)[0]), (hx, yc - 2 * rs)


mR, dR, cR = headlamp(72, '11/12 Headlamp R')
mL, dL, cL = headlamp(240, '11/12 Headlamp L')
wire('29', [cR, (26, 72), (26, 78)], 14, 69.3); earth(26, 78)
wire('115', [cL, (26, 240), (26, 246)], 11, 237.3); earth(26, 246)
pR, pRb = front_housing(138, '13 Parking R', 28)
pL, pLb = front_housing(191, '13 Parking L', 27)

# ---- lighting relay 8 --------------------------------------------------
# As the manual prints it (IMG_4719): all six terminals on the bottom edge, every contact in its printed rest state.
# K1 (S side, in series with the resistor from 30) moves the top blade and the 56a/56b changeover; K2 (31-86) moves
# the blade on 30. Positions are fractions of the manual's box.
rx, ry, rw, rh = 140, 188, 68, 36
X = lambda f: round(rx + rw * f, 2)
Y = lambda f: round(ry + rh * f, 2)
yb, yc = ry + rh, Y(.25)
box(rx, ry, rw, rh)
txt(rx, ry - 1.8, '8', 4, w='bold'); txt(rx + 4.2, ry - 1.8, 'Lighting relay (C7)', 2.7)
txt(rx + 31, ry - 1.8, 'latching dip/main + flash', 2.3, fill='#555')
bt = {'56a': X(.10), '56b': X(.33), 'S': X(.56), '31': X(.67), '86': X(.79), '30': X(.90)}
G, H, F = (bt['56a'], Y(.52)), (X(.23), Y(.52)), (X(.17), Y(.23))
D, Ac, B, C, E = (X(.41), yc), (X(.56), yc), (X(.64), yc), (X(.795), yc), (X(.67), Y(.11))
k1l, k1r, k1t, _ = coil(X(.46), Y(.425), rw * .075, rh * .205)
k2l, k2r, k2t, _ = coil(X(.685), Y(.425), rw * .08, rh * .205)
ra, rb = resistor(X(.42), Y(.72), rw * .09, rh * .08)
inner([(bt['56a'], yb), (G[0], G[1] + .8)])                                        # 56a to G only
inner([(bt['56b'], yb), (bt['56b'], yc), (D[0] - .8, yc)])                          # 56b up to the top blade's pivot
inner([(bt['56b'], H[1]), (H[0] + .8, H[1])]); jdot(bt['56b'], H[1])                # and across to H
inner([(bt['30'], yb), (bt['30'], yc), (C[0] + .8, yc)])                            # 30 up to the blade on C
inner([(Ac[0] + .8, yc), (B[0] - .8, yc)])                                         # A-B
inner([(F[0], F[1] - .8), (F[0], E[1]), (E[0] - .8, E[1])])                        # E-F, over the top
inner([k1r, (bt['S'], k1r[1]), (bt['S'], yb)])                                     # K1 to S
inner([k1l, (X(.405), k1l[1]), (X(.405), ra[1]), ra])                              # K1 to the resistor
inner([rb, (bt['30'], rb[1])]); jdot(bt['30'], rb[1])                              # resistor bus to 30: crosses S, 31, 86
inner([k2l, (bt['31'], k2l[1]), (bt['31'], yb)]); inner([k2r, (bt['86'], k2r[1]), (bt['86'], yb)])
for p in (G, H, F, D, Ac, B, C, E): contact(*p)
blade(B[0] + .7, yc - .3, C[0] - .8, yc - .3)                                      # B-C closed at rest


def blade_to(p, q, back=.8):
    """Blade from pivot contact p towards q, starting .7 off p's centre and stopping `back` short of q."""
    L = ((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2) ** .5; ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    blade(round(p[0] + .7 * ux, 2), round(p[1] + .7 * uy, 2), round(q[0] - back * ux, 2), round(q[1] - back * uy, 2))


blade_to(D, (X(.55), Y(.17)), back=0)                                              # top blade: open, free end short of A
blade_to(F, H)                                                                     # changeover: rests on H (56b)
mlink([k1t, (k1t[0], Y(.23))]); mlink([(k1t[0], Y(.36)), (X(.235), Y(.36))])      # K1 to the top blade and the changeover
mlink([k2t, (k2t[0], Y(.30))])                                                     # K2 to the B-C blade
for k, x in bt.items(): tlabel(x - 1.5, yb - 1.3, k, 'end')                     # dots: after the wires

a56, b56 = yb + 4.5, yb + 8.5                                                      # 26 and 24 come in under the relay
wire('26', [mR, (120, mR[1]), (120, a56), (bt['56a'], a56), (bt['56a'], yb)], 58, 67)
wire('24', [dR, (114, dR[1]), (114, b56), (bt['56b'], b56), (bt['56b'], yb)], 58, 81)
wire('25', [(bt['56a'], a56), (bt['56a'], mL[1]), mL], 58, 235)
wire('23', [(bt['56b'], b56), (bt['56b'], dL[1]), dL], 58, 249)
wire('27', [(134, a56), (134, 149), (150, 149)], 132.3, 222, rot=-90)
for x, y in ((bt['56a'], a56), (134, a56), (bt['56b'], b56)): dot(x, y)
box(150, 141, 46, 16)
lamp(158, 149, r=3.2); inner([(150, 149), (154.8, 149)]); txt(164, 147, '47 Instrument', 2.6, w='bold'); txt(164, 151, 'main-beam', 2.3); txt(164, 154.4, 'warning lamp', 2.3)
wire('13', [(bt['31'], yb), (bt['31'], yb + 22)], bt['31'] + 4.3, yb + 20, rot=-90); earth(bt['31'], yb + 22)
wire('32', [(bt['S'], yb), (bt['S'], 264)], 159.5, 259)
box(140, 264, 58, 18)
txt(143, 269.5, '9', 4, w='bold'); txt(148, 269.5, 'Dip/flash stalk (F9)', 2.7)
txt(143, 274, 'pulse on S toggles dip/main;', 2.3, fill='#555'); txt(143, 277.3, 'flash works with ignition off', 2.3, fill='#555')

# ---- light switch 10 ---------------------------------------------------
sx, sy, sw_, sh = 222, 50, 50, 24
box(sx, sy, sw_, sh)
txt(sx + 25, sy + 10, '10  Light switch', 3, 'middle', w='bold'); txt(sx + 25, sy + 14, '(C8) off / parking / headlamps', 2.3, 'middle', fill='#555')
T = {'2': (232, sy), '3': (262, sy), '1': (232, sy + sh), '4': (262, sy + sh)}
for k, (x, y) in T.items():
    dot(x, y); txt(x + 1.8, y + (3.5 if y == sy else -1.5), k, 2.5)
wire('31', [(bt['86'], yb), (bt['86'], 250), (232, 250), T['1']], 203.5, 248)
wire('20', [(bt['30'], yb), (bt['30'], 258), (236, 258), (236, 96), (244, 96)], 203.5, 256)
wire('30', [T['2'], (232, 36), (318, 36)], 240, 34)
wire('40', [T['3'], (262, 42), (312, 42), (318, 48)], 268, 40)
wire('41', [T['4'], (262, 80), (304, 80), (304, 150), (290, 150)], 266.5, 78.2)

# ---- fuse box 22 -------------------------------------------------------
box(240, 88, 60, 108)
A('<path d="M244,96 H286" stroke="#111" stroke-width="1.6"/>')
txt(246, 102, 'Supply bar, fuses 7–12: always live', 2.3); txt(246, 105.4, 'fed from battery via 5 GR 4.0 + 5a GR 2.5', 2.3, fill='#555')
wire('7', [(286, 96), (310, 96), (310, 48), (318, 48)], 314, 90, rot=-90)
for fy, n in ((125, '2'), (178, '1')):
    fuse(262, fy - 2, 18, 4)
    A(f'<path d="M255,{fy} h7 M280,{fy} h10" stroke="#111" stroke-width=".5"/>')
    txt(271, fy - 3.5, fuse_label(int(n), 'Fuse '), 2.5, 'middle')
    if fuse_checked(int(n)): tick(280.8, fy - 4.0)
A('<path d="M290,125 V178" stroke="#111" stroke-width=".6"/>'); dot(290, 150)
txt(297, 190, '22  Fuse box', 3, 'end', w='bold'); txt(297, 193.8, '(fuses 1–2 and bar 7–12 shown)', 2.2, 'end', fill='#555')
wire('45', [(255, 125), (pR[0], 125), pR], 58, 123); inner([pR, pRb])
wire('43', [(255, 178), (pL[0], 178), pL], 58, 176); inner([pL, pLb])

# ---- connector 58 + ignition switch 20 --------------------------------
A('<rect x="318" y="30" width="6" height="24" fill="#ddd" stroke="#111" stroke-width=".6"/>')
for y in (36, 48): dot(318, y)
txt(321, 28, '58', 3, 'middle', w='bold'); txt(321, 58, '12-pole connector', 2.2, 'middle', fill='#555')
wire('30', [(324, 36), (345, 36)], label=False)
wire('7', [(324, 48), (345, 48)], label=False)
box(345, 28, 52, 28)
txt(349, 37, 'X', 2.6); txt(349, 49, '30', 2.6)
txt(358, 36, '20  Ignition switch', 3, w='bold'); txt(358, 41, '30: battery in (grey)', 2.3, fill='#555')
txt(358, 45, 'X: live with key on (red)', 2.3, fill='#555'); txt(358, 49.5, 'per manual, PDF p. 375', 2.3, fill='#555')

# ---- rear clusters -----------------------------------------------------
# As printed (IMG_4727/4728): six bulbs over one earth bar. The tail feed enters the tail bulb next to the indicator;
# a jumper takes it to the other tail bulb and a second one on to the number plate bulb. Both jumpers are unnumbered
# and drawn just outside the lamp, as in the manual (whether they are in the harness or the holder is unreadable).
# L is printed as the vertical mirror of R (indicator at the bottom, outboard like R's at the top); so is it here.
# Feeds drawn on the signals sheet end in open terminals on the outline.
xL, xJ, xP, xB, xE, xR, rr = 354, 348.5, 351, 372, 382, 386, 3.2


def cluster(y0, side, feed, ind, tail_stub, plate_stub, mirror=False):
    """feed: (cable, route up to the cluster, label position). Bulbs are indexed indicator, fed tail, brake, reversing,
    jumper-fed tail, plate: top to bottom for R, bottom to top for L (mirror=True)."""
    box(xL, y0, xR - xL, 54, fill='#fdfdfd', sw=.6)
    txt((xL + xR) / 2, y0 - 2, f'Rear lamp cluster {side}', 2.6, 'middle')
    ys = [y0 + 4.5 + 9 * i for i in range(6)]
    if mirror: ys.reverse()
    g = 1 if ys[4] > ys[1] else -1                                                # the way the jumpers run
    wire(feed[0], feed[1] + [(xL, ys[1])], *feed[2])
    for i in (1, 4, 5): inner([(xL, ys[i]), (xB - rr, ys[i])])                     # the three tail-circuit feeds
    for i in (0, 2, 3): contact(xL, ys[i]); inner([(xL + .8, ys[i]), (xB - rr, ys[i])])   # indicator, brake, reversing
    inner([(xL, ys[1]), (xJ, ys[1] + 4 * g), (xJ, ys[4]), (xL, ys[4])])            # tail jumper, outside the lamp
    inner([(xL, ys[4]), (xP, ys[4] + 3 * g), (xP, ys[5]), (xL, ys[5])])            # number plate jumper
    it = 0 if not mirror else 5                                                    # the bar starts at the top bulb
    inner([(xB + rr, ys[it]), (xE, ys[it]), (xE, y0 + 54)])                         # earth bar
    for i, (yy, nm) in enumerate(zip(ys, (f'{ind} indicator', '14 tail', '30 brake', '32 reversing', '14 tail', '15 plate'))):
        indicator(xB, yy, rr, 'tb') if i == 0 else lamp(xB, yy, r=rr)
        if i != it: inner([(xB + rr, yy), (xE, yy)]); jdot(xE, yy)
        txt(xR + 2, yy + .8, nm, 2.2, fill='#111' if i in (1, 4, 5) else '#555')
    earth(xE, y0 + 54); dot(xE, y0 + 54)
    ty = ys[2] - 2.5                                                               # the tail stub lands on the jumper
    wire(tail_stub, [(xJ, ty), (342, ty)], 322, ty + 1.5)
    wire(plate_stub, [(xP, ys[5]), (342, ys[5])], 320, ys[5] + 1.5)
    for p in ((xJ, ty), (xP, ys[5]), (xL, ys[1]), (xL, ys[4]), (xL, ys[5])): dot(*p)


cluster(102.5, 'R', ('44', [(255, 125), (255, 116)], (314, 114)), 28, '47', '47a')
cluster(172.5, 'L', ('42', [(255, 178), (255, 213)], (314, 211)), 27, '46', '46a', mirror=True)

# terminal dots and junctions go on top of the wires that end on them
for p in [(x, yb) for x in bt.values()] + [(324, 36), (324, 48), (345, 36), (345, 48), (255, 125), (255, 178),
                                           (150, 149), (bt['S'], 264), mR, dR, cR, mL, dL, cL, pR, pL]:
    dot(*p)

# ---- legend ------------------------------------------------------------
lx, ly = 250, 236
box(lx, ly, 157, 51, fill='#fff', sw=.5)
txt(lx + 3, ly + 5.5, 'Cable key: number · colour · mm²', 3, w='bold')
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 11 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x, y = lx + 97, ly + 11
A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="1.2"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x},{y + 4} h9" stroke="#222" stroke-width="1.2" stroke-dasharray="3 2"/>'); txt(x + 11, y + 5, 'not traced yet', 2.4)
A(f'<path d="M{x},{y + 9} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{y + 9}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
txt(x + 11, y + 10, 'ends on diagram', 2.4)
if TICKED[0]: tick(x + 33, y + 9.3); txt(x + 37, y + 10, 'checked on the car', 2.4)
probable_legend(lx + 4, ly + 21)
notes = ['Headlamps need the ignition on (except the flash, stalk 9); parking/tail lights do not (manual, PDF p. 375, 413):',
         'light switch 2 is fed from ignition switch X, light switch 3 from the always-live bar.',
         'Headlamps are unfused: relay 30 is fed straight from the supply bar (20 GR 1.5).',
         'Not RHD-specific: circuits are per side, but harness routing and part positions may differ.',
         'All bulbs in a lamp housing share its one earth. Indicators, brake and reversing bulbs: signals sheet.',
         'The front housings’ lower bulb has no number (probably corner lamp 118); its feed is not drawn.']
for j, n in enumerate(notes): txt(lx + 3, ly + 27 + j * 3.9, n, 2.35, fill='#333')
save('lighting.svg')

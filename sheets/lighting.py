#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo lighting sheet (A3 landscape SVG).

Layout lives here; wire identity, colour, size and status come from
data/wires.csv, so editing the CSV (e.g. status -> car) updates the drawing.
"""
import math
from common import *
from common import _ink                      # grey (probably) ink for filament()

header('Saab 99 Turbo, model 1979 — Lighting circuit')
txt(16, 40, 'FRONT', 3.6, w='bold', fill='#777'); txt(398, 91, 'REAR', 3.6, 'end', w='bold', fill='#777')
txt(16, 44.5, 'car’s right side at top', 2.3, fill='#777'); txt(398, 95.5, 'Combi Coupé (this car)', 2.3, 'end', fill='#777')


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


def filament(x0, x1, y, s, grey=False):
    """Filament arc from (x0, y) to (x1, y), x0 < x1, sagging s mm down the page (s < 0 bows it up); grey: probably."""
    R = round(((x1 - x0) ** 2 / 4 + s * s) / (2 * abs(s)), 2)
    A(f'<path d="M{x0},{y} A{R},{R} 0 0 {0 if s > 0 else 1} {x1},{y}" fill="none" stroke="{_ink(grey)}" stroke-width=".4"/>')


def headlamp(y, cap, drop=False):
    """Twin-filament headlamp 11/12 in its housing (IMG_4714/4715), mirrored so the main/dip feeds come in through the
    rounded end on the right and the common leaves through the front. The manual prints both arcs (black: the upper
    sags, the lower bows up) but not which arc joins which lead, so those short joins are grey.
    drop: a second lead leaves the common node at the bulb's 9 o'clock, down-left and out through the bottom outline
    (11/12 L: 115 SV to thermostat 39, IMG_4715).
    Returns (main feed, dip feed, common, drop lead or None), all on the housing outline."""
    r, a, rr, e = 5.5, 3, 7.6, 3.2   # bulb radius, feeds 3 mm above/below centre, rounded end radius, arc half-width
    xo, edge = housing(34, hx, y, 10, rr, 2.2, 36)
    A(f'<circle cx="{hx}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    xr, xh = round(hx + (r * r - a * a) ** .5, 2), round(hx + (rr * rr - a * a) ** .5, 2)   # bulb rim, outline
    for sy in (-1, 1):
        filament(hx - e, hx + e, y + sy * a, -sy * 1.5)                                   # both toward the centre
        inner([(xh, y + sy * a), (xr, y + sy * a)])                                        # feed to the bulb: read
        inner([(xr, y + sy * a), (hx + e, y + sy * a)], grey=True)                         # which arc: not printed
        inner([(hx - e, y + sy * a), (hx - r, y)], grey=True)
    inner([(hx - r, y), (xo, y)])                                                          # common, across the chord
    d = None
    if drop:
        xd = hx - r - 1.5; d = (xd, edge(xd)[1])
        inner([(hx - r, y), (xd, y + 1.5), d]); jdot(hx - r, y)
    txt(hx, y - 12.2, cap, 2.7, 'middle')
    return (xh, y - a), (xh, y + a), (xo, y), d


def small_bulb(x, y, r, top):
    """Plain bulb as printed in the front housings: a circle with one filament arc, near its top and sagging toward
    the centre (top=True: parking bulb 13) or near its bottom and bowing up (the unnumbered lower bulb)."""
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    k = -1 if top else 1
    filament(round(x - r * .866, 2), round(x + r * .866, 2), round(y + k * r * .5, 2), round(-k * r * .35, 2))


def twin_bulb(x, y, r):
    """Twin-filament 21/5 W bulb as the 1977 Turbo diagram prints the front parking bulb (5 W parking light 13 + 21 W
    corner lamp 118; p.30, p.359): a circle with one filament arc near its top, sagging toward the centre, and one near
    its bottom, bowing up. The top one (parking) is on the 1979 print; the bottom one (118) is not drawn there, so it is
    grey (probably) until E19b."""
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    for k in (-1, 1):
        filament(round(x - r * .866, 2), round(x + r * .866, 2), round(y + k * r * .5, 2), round(-k * r * .35, 2), k == 1)


def front_housing(yc, side, ind):
    """Front lamp housing 13 as printed (IMG_4714/4715): two small bulbs above one another, indicator 27/28 to the
    right, one common earth line out of the front (crossing the lens chord). The upper, parking bulb 13 (fed from the
    top) is drawn as the 1977 Turbo diagram prints it, a 21/5 W twin bulb whose 21 W filament is corner lamp 118,
    fed from its left through the top outline at x = 41 (221 left, 222a right; not drawn on the 1979 Turbo print, so it
    and its lead are grey; on the car: switch found (E19), bulb to check (E19b)). The lower bulb, a
    side back-up light (unnumbered in 1979, 119 in the 1977 legend), is fed from the bottom. The indicator's feed is
    drawn on the signals sheet: an open terminal here.
    Returns the parking feed on the outline, the top of the parking bulb, the corner lamp feed, the back-up light
    feed and the common earth, all but the second on the outline."""
    xi, rs, ri, xk = 54, 2.6, 4, 41
    xo, edge = housing(36, 56, yc, 9.5, 6.5, 2.4, 38.5)
    inner([(xi - ri, yc), (xo, yc)])                                               # common earth, through the bulbs' joint
    yo, yk = edge(hx)[1], edge(xk)[0]
    inner([(hx, yc + 2 * rs), (hx, yo)])                                           # back-up light feed, 139/139a
    inner([(xk, yk), (xk, yc - rs), (hx - rs, yc - rs)], grey=True)                # corner lamp feed, 221/222a: 1977
    inner([(xi + ri, yc), (61.7, yc)]); contact(62.5, yc)                          # indicator feed: signals sheet
    twin_bulb(hx, yc - rs, rs); small_bulb(hx, yc + rs, rs, False); indicator(xi, yc, ri, 'lr'); jdot(hx, yc)
    txt(64.5, yc - 5.6, f'13 Parking {side}', 2.7)
    for i, s in enumerate(('twin bulb 21/5 W: 5 W parking 13,', '21 W corner lamp 118',  # two lines: clear of 24 GL (x 114)
                           f'{ind} indicator: signals sheet', 'lower bulb: side back-up light')):
        txt(64.5, round(yc - 2.4 + 3 * i, 2), s, 2.1, fill='#555')
    return (hx, edge(hx)[0]), (hx, yc - 2 * rs), (xk, yk), (hx, yo), (xo, yc)


def lab(c):
    """A cable's label as wire() prints it: number, colour, mm² from wires.csv."""
    r = WIRES[c]; return f"{c.split('#')[0]} {r['colour']} {r['mm2']}"


def ltag(c, x, y, dest, size=2.2, anchor='start', dashed=False):
    """Tag at the end of cable c carrying its label and where it goes, for wires too short for their own label;
    '\\n' in dest starts a second line. A cable checked on the car gets its tick at the end of the first line."""
    lines = f'{lab(c)} {dest}'.split('\n')
    car = WIRES[c]['status'] == 'car'
    w = round(max(len(s) for s in lines) * size * .52 + 3 + (3.5 if car else 0), 1)
    x0 = x if anchor == 'start' else x - w
    if len(lines) == 1:
        tag(x, y, lines[0], w=w, dashed=dashed, size=size, anchor=anchor)
    else:
        ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2)
        dash = ' stroke-dasharray="1.5 1"' if dashed else ''
        A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"{dash}/>')
        for i, s in enumerate(lines):
            txt(x0 + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
    if car: tick(round(x0 + 2 + len(lines[0]) * size * .52, 1), y - .6 - (len(lines) - 1) * 1.36 * size / 2)


mR, dR, cR, _ = headlamp(72, '11/12 Headlamp R')
mL, dL, cL, dropL = headlamp(240, '11/12 Headlamp L', drop=True)
wire('29', [cR, (26, 72), (26, 78)], 14, 69.3); earth(26, 78)
wire('28', [cL, (26, 240), (26, 246)], 14, 237.3); earth(26, 246)                  # the left headlamp's own earth
wire('115', [dropL, (dropL[0], 262), (44, 262)], label=False)                        # from the common node, as printed
ltag('115', 44, 262, '→ 39 radiator fan thermostat (climate sheet)')
pR, pRb, kR, vR, eR = front_housing(138, 'R', 28)
pL, pLb, kL, vL, eL = front_housing(191, 'L', 27)
wire('361', [eR, (24, 138), (24, 161), (28, 161)], label=False)
ltag('361', 28, 161, '→ washer pump 63 earth (wipers sheet)')
wire('360', [eL, (24.6, 191), (24.6, 196)], 11, 188.8); earth(24.6, 196)

# ---- corner lamps: switch 117 and the parking bulbs' second filament 118 -----------------------------
# The 1979 Turbo print lists 117 and 118 (legend p.406) but draws only an empty pin 2 on 58 (E2). Drawn from the 1977
# Turbo diagram with the cable numbers of the 1979 GL print (p.405); the car has the circuit (E19, F4), so the cables
# are 'open'. 117 as the 1977 print draws it: pilot lamp at the top, three contacts in a column joined by a dashed link
# (lamp, output 221, feed 220 from fuse 5) and the rocker across them; 221a leaves the middle contact down-left and runs
# to light switch 10:6 (drawn with switch 10). Not drawn: the 1980 switch 76 (rear bulb 75), 1977 relay 77, the 1979 GL
# town-light feed (37/37a, 60 (E7), 38 GR). The dashed runs' lengths are chosen so a dash, not a gap, meets each
# terminal (dash pattern 3 2 from the start).
kx, ky = 157, 82              # 221's run to 58 is 71 mm, so a dash meets the pin
box(kx, ky, 18, 30)
txt(kx, ky - 6, '117', 3.2, w='bold'); txt(kx + 7, ky - 6, 'Corner lamp switch', 2.7)
txt(kx, ky - 2.2, 'dash switch with pilot lamp; probably wired as drawn', 2.1, fill='#555')   # 1977 Turbo diagram
xc = kx + 12
lamp(xc, ky + 6, r=2.5)
inner([(xc - 2.5, ky + 6), (kx + 6, ky + 6), (kx + 6, ky + 12), (xc - .8, ky + 12)])  # pilot lamp to the top contact
inner([(xc + 2.5, ky + 6), (kx + 18, ky + 6)])                                        # pilot lamp earth: 223
for yy in (12, 19, 25): contact(xc, ky + yy)
mlink([(xc, ky + 12.8), (xc, ky + 18.2)]); mlink([(xc, ky + 19.8), (xc, ky + 24.2)])
inner([(kx, ky + 19), (xc - .8, ky + 19)])                                            # 221, output
inner([(xc - .57, ky + 19.57), (kx + 8, ky + 23), (kx + 8, ky + 30)])                 # 221a
inner([(kx + 18, ky + 25), (xc + .8, ky + 25)])                                       # 220, feed
blade(kx + 9.5, ky + 13.5, kx + 16, ky + 20)                                          # stops short of the wall
# 220 and 223 are 8 mm stubs into tags that end by x 212, clear of 221a's riser to 10:6 (x 216)
wire('220', [(kx + 18, ky + 25), (kx + 26, ky + 25)], label=False); ltag('220', kx + 26, ky + 25, '← fuse 5\n(power sheet)')
txt(kx + 27.5, ky + 19.3, '220 may be GL (check E19b)', 2, fill='#555')   # 1979 GL print: 220 GL 0.5
wire('223', [(kx + 18, ky + 6), (kx + 26, ky + 6)], label=False)                    # 1977 print: to clock 49's earth
ltag('223', kx + 26, ky + 6, '→ clock 49\nearth, with 128 SV\n(radio sheet)')           # clock 49 and 128: radio sheet
# 221 through pin 2 of the front 4-pole connector 58 (E2) (1979 GL print) on to the left housing; 222a branches off
# the same pin's lead for the right one. The 1979 Turbo print draws pin 2 with no leads. Pins 1 and 3 are only
# captioned (their leads are on the signals sheet); pin 4's 139/139a are drawn below.
wire('221', [(kx, ky + 19), (86, ky + 19)], 126, ky + 17)
wire('221', [(80, ky + 19), (14.5, ky + 19), (14.5, 171), (kL[0], 171), kL], 17.5, 169)
# 222a: square off 221 at a junction 4 mm from the pin (in 221's first gap), 6 mm down, left, down into housing R.
# Corners at 6 and 41 mm and the end (63.2 mm, under the dot) fall on dashes.
wire('222a', [(76, ky + 19), (76, ky + 25), (kR[0], ky + 25), kR], 45, ky + 29.3)
A(f'<rect x="80" y="{ky + 13}" width="6" height="16" fill="#ddd" stroke="#111" stroke-width=".6"/>')
txt(83, ky + 11.3, '58', 2.8, 'middle', w='bold')   # 58 (E2) in the manual
for n, dy, s in (('1', 15, '118 SV: horns'), ('2', 19, ''), ('3', 23, '77 BL/VT: indicator 27'), ('4', 27, '')):
    tlabel(83, ky + dy + .65, n, 'middle')
    if s: txt(87.5, ky + dy + .7, s, 2, fill='#555')
txt(89.8, ky + 27.7, '138 BL ← reversing 31', 2, fill='#555')   # right of 139a's stub, which turns down
txt(83, ky + 7.3, 'front lamp connector', 2, 'middle', fill='#555')   # above the number: 139/139a leave below
# 139/139a from pin 4 as book photo P5 prints them: 139 from the housing side (left), 139a from 138's side (right).
# Each leaves its pin with a short sideways stub (as 221 leaves pin 2) and drops, then runs round the right of housing
# R's captions (end x 96) in a lane short of 24 GL (x 114) and back left under its housing into the lower bulb:
# 139 in lane x 101 to L, 139a in lane x 107.5 to R. The two cross once, plainly, at (101, 151.5).
# Crossings: 45 GN (both), 43 BL (139), 139/139a.
wire('139', [(80, ky + 27), (78, ky + 27), (78, ky + 38), (101, ky + 38), (101, 204.5), (hx, 204.5), vL], 50, 208.8)
wire('139a', [(86, ky + 27), (88, ky + 27), (88, ky + 34), (107.5, ky + 34), (107.5, 151.5), (hx, 151.5), vR],
     50, 155.8)

# ---- lighting relay 8 --------------------------------------------------
# As the manual prints it (IMG_4719): all six terminals on the bottom edge, every contact in its printed rest state.
# K1 (S side, in series with the resistor from 30) moves the top blade and the 56a/56b changeover; K2 (31-86) moves
# the blade on 30. Positions are fractions of the manual's box. The flash contact is kept on 56b as printed, though the
# 1977 Turbo diagram puts it on the main-beam pin and the car flashes the main beams (D9); which pin carries main on the
# car is D12 (the 1980 print swaps the outputs instead), so D stays where the 1979 print has it until then.
# Our reading aids, not printed: a caption for the rest state, light grey dashed 'ghost' blades where each moving contact
# goes when its coil pulls, italic letters A-H for the contacts and K1/K2 for the coils, and a states table (below, left
# of stalk 9) whose paths use those letters. The dip/main latch is inferred (no ratchet printed): check D13.
rx, ry, rw, rh = 140, 188, 68, 36
X = lambda f: round(rx + rw * f, 2)
Y = lambda f: round(ry + rh * f, 2)
yb, yc = ry + rh, Y(.25)
box(rx, ry, rw, rh)
txt(rx, ry - 1.8, '8', 4, w='bold'); txt(rx + 4.2, ry - 1.8, 'Lighting relay', 2.7)
txt(rx + 25, ry - 1.8, 'drawn at rest: lights off, stalk released', 2.3, fill='#555')
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


def toward(p, q, back=.8):
    """End points of a blade from pivot contact p towards q: .7 off p's centre, stopping `back` short of q."""
    L = ((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2) ** .5; ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    return round(p[0] + .7 * ux, 2), round(p[1] + .7 * uy, 2), round(q[0] - back * ux, 2), round(q[1] - back * uy, 2)


def blade_to(p, q, back=.8):
    blade(*toward(p, q, back))


GHOST = 'stroke="#bbb" stroke-width=".7" stroke-dasharray="1.3 .8"'   # a blade's weight but faded; mlink is thin and darker


def ghost_to(p, q, dy=0):
    """Where the blade on pivot p goes when its coil pulls: a light grey dashed blade onto contact q (our aid). dy lifts
    one that lies along a conductor, as the closed B-C blade sits .3 above it, so it reads as a blade, not a link."""
    x0, y0, x1, y1 = toward(p, q)
    A(f'<path d="M{x0},{round(y0 + dy, 2)} L{x1},{round(y1 + dy, 2)}" fill="none" {GHOST}/>')


def cname(x, y, t, anchor='middle'):
    """Our name for a contact or coil (used by the states table): small italic grey, apart from the upright terminal labels."""
    A(f'<text x="{x}" y="{y}" font-size="1.8" font-style="italic" text-anchor="{anchor}" fill="#666">{t}</text>')


ghost_to(C, E); ghost_to(F, G); ghost_to(D, Ac, -.3)                              # K2: C to E; K1: F to G, flash blade onto A
for p in (G, H, F, D, Ac, B, C, E): contact(*p)
blade(B[0] + .7, yc - .3, C[0] - .8, yc - .3)                                      # B-C closed at rest
blade_to(D, (X(.55), Y(.17)), back=0)                                              # top blade: open, free end short of A
blade_to(F, H)                                                                     # changeover: rests on H (56b)
for (x, y), t, dx, dy, anc in ((Ac, 'A', 0, 3.1, 'middle'), (B, 'B', 0, 3.1, 'middle'), (C, 'C', 0, 3.1, 'middle'),
                               (D, 'D', -1, -1.4, 'end'), (E, 'E', .9, -1.4, 'start'), (F, 'F', -1.3, .6, 'end'),
                               (G, 'G', -1.3, .6, 'end'), (H, 'H', 0, 3.2, 'middle')):
    cname(round(x + dx, 2), round(y + dy, 2), t, anc)
cname(round(k1l[0] - .8, 2), round(k1t[1] + 1.1, 2), 'K1', 'end'); cname(round(k2l[0] - .8, 2), round(k2t[1] + 1.1, 2), 'K2', 'end')
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
wire('13', [(bt['31'], yb), (bt['31'], 252), (174, 252)], bt['31'] + 4.3, yb + 20, rot=-90)
tag(174, 252, '→ 113:85 (climate sheet), earth via 212 SV and joint 158', size=2.2, anchor='end')
wire('32', [(bt['S'], yb), (bt['S'], 264)], 159.5, 259)
box(140, 264, 58, 18)
txt(143, 269.5, '9', 4, w='bold'); txt(148, 269.5, 'Dip/flash stalk', 2.7)
txt(143, 274, 'pulse on S toggles dip/main;', 2.3, fill='#555'); txt(143, 277.3, 'flash works with ignition off', 2.3, fill='#555')
# 9 as printed (book photo P8, scan F9): one contact, open at rest. The blade pivots on the relay side (32 VT from S,
# via 58 (D8) pin 9) and rises toward the fixed contact on the earth side; both at mid-height. The book prints the
# earth lead 32 VT 0.75 as well, so it is drawn and labelled as 32. Stopgap: it uses 32's row (8:S to 9), so a 'car'
# tick or 'open' dash on 32 would show here too. When data/wires.csv gets 32#earth (VT 0.75, 9 to earth), change
# this to wire('32#earth', ...); the drawing does not change.
y9 = 273
inner([(bt['S'], 264), (bt['S'], y9 - .8)]); contact(bt['S'], y9)
blade_to((bt['S'], y9), (190.6, y9 - 3.4), back=0)                                 # free end short of, above, the fixed contact
contact(193, y9); inner([(193.8, y9), (198, y9)])
wire('32#earth', [(198, y9), (222, y9), (222, 277)], 200.5, y9 - 2.7); earth(222, 277)

# ---- relay 8 states table (our aid): in the free corner left of stalk 9, under 115's tag (ends y 264.6) and above the
# frame (288.7). Paths use the letters drawn in the relay. Row 4: as drawn D sits on 56b, which would flash dipped; the
# car flashes main (D9), and D12 reads which pin carries main, so the row gives both and D stays put.
TX, TY, RH8 = 12.5, 273.9, 3.2                          # left, grid top, row height
C8 = [TX, TX + 19.5, TX + 34.5, TX + 66, 136]           # column edges: state, coils pulled, path, lights
ROWS8 = [('1', 'lights off', 'none', '30 → C → B → A', 'nothing: flash blade A–D open'),
         ('2', 'headlamps on', 'K2', '30 → C → E → F → H → 56b', 'dipped'),
         ('3', 'main, latched', 'K2, K1 pulse', '30 → C → E → F → G → 56a', 'main + dash lamp 47; next pulse: dipped (check D13)'),
         ('4', 'flash, lights off', 'K1, stalk held', '30 → C → B → A → D', 'main on the car (check D9); D drawn on 56b: check D12')]
txt(TX, TY - 4.6, '8 Lighting relay states', 2.4, w='bold', fill='#333')
txt(TX + 28, TY - 4.6, 'latching dip/main + flash; each path starts at terminal 30', 2.1, fill='#555')
for x, h in zip(C8, ('state', 'coils pulled', 'path (letters in 8)', 'lights')):
    txt(x + (3.6 if x == TX else 1), TY - 1.2, h, 2.0, fill='#555')
grid = [f'M{TX},{round(TY + j * RH8, 2)} H{C8[-1]}' for j in range(5)] + [f'M{x},{TY} V{round(TY + 4 * RH8, 2)}' for x in C8]
A(f'<path d="{" ".join(grid)}" stroke="#ccc" stroke-width=".2"/>')
for j, (n, *cells) in enumerate(ROWS8):
    y = round(TY + (j + .5) * RH8, 2)
    A(f'<circle cx="{TX + 1.6}" cy="{y}" r="1.2" fill="#fff" stroke="#888" stroke-width=".25"/>')
    txt(TX + 1.6, round(y + .68, 2), n, 1.9, 'middle', w='bold', fill='#777')
    for x, s in zip(C8, cells): txt(x + (3.6 if x == TX else 1), round(y + .75, 2), s, 2.1, fill='#222')

# ---- light switch 10 ---------------------------------------------------
# 6 and 5 (upper left, as both 1979 prints draw them) close in the top position: town light, Sweden/Norway/Denmark only
# (p.413). The 1979 Turbo print leaves them bare; the 1977 Turbo diagram runs 221a from 117's output to 6, 5 unwired.
sx, sy, sw_, sh = 222, 50, 50, 24
box(sx, sy, sw_, sh)
txt(sx + 25, sy + 9.5, '10  Light switch', 3, 'middle', w='bold')
txt(sx + 25, sy + 13.5, 'top: off (town light S/N/DK) /', 2.3, 'middle', fill='#555')
txt(sx + 25, sy + 16.8, 'parking / headlamps', 2.3, 'middle', fill='#555')
T = {'2': (232, sy), '3': (262, sy), '1': (232, sy + sh), '4': (262, sy + sh), '6': (sx, sy + 4), '5': (sx, sy + 10)}
for k, (x, y) in T.items():
    dot(x, y); txt(x + 1.8, y + (.9 if x == sx else 3.5 if y == sy else -1.5), k, 2.5)
# 221a: down, right under 220's tag, up at x 216 (clear of both tags and 31 GL at x 232) into 6; corners and the end
# fall on dashes (at 1, 2, 1 and 2 mm into one)
wire('221a', [(kx + 8, ky + 30), (kx + 8, 118), (216, 118), (216, T['6'][1]), T['6']], 184, 116)
for i, s in enumerate(('6-5: top position, town light', '(S/N/DK only). This car has', 'no town light (check E21b);', 'wires on 6-5: check D11')):
    txt(219.5, round(sy - 8.4 + 2.8 * i, 2), s, 2.1, 'end', fill='#555')
box(240, 88, 60, 108)   # fuse box 22, drawn before 20 and 41 so their last legs show inside it, up to the bar and 290,150
# labels 2.7 mm right of 20 GR 1.5's riser from 8:30, so they read as 31's and 20's, not the riser's
wire('31', [(bt['86'], yb), (bt['86'], 250), (232, 250), T['1']], 205, 248)
wire('20', [(bt['30'], yb), (bt['30'], 258), (236, 258), (236, 96), (244, 96)], 205, 256)
wire('30', [T['2'], (232, 36), (318, 36)], 240, 34)
wire('40', [T['3'], (262, 42), (314.5, 42), (318, 48)], 268, 40)   # steep last leg: meets 7 GR 2.5 at the pin, not before
wire('41', [T['4'], (262, 80), (304, 80), (304, 150), (290, 150)], 266.5, 78.2)

# ---- fuse box 22 -------------------------------------------------------
A('<path d="M244,96 H286" stroke="#111" stroke-width="2.9"/>')   # as wide as 7 GR 2.5 it feeds (solid black reads heavier than a grey core)
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
txt(321, 28, '58', 3, 'middle', w='bold')                                     # 58 (B9) in the manual
txt(321, 24, 'ignition switch connector, 12-pole', 2.2, 'middle', fill='#555')   # above the number, as front lamp connector 58
wire('30', [(324, 36), (345, 36)], label=False)
wire('7', [(324, 48), (345, 48)], label=False)
box(345, 28, 52, 28)
txt(349, 37, 'X', 2.6); txt(349, 49, '30', 2.6)
txt(358, 36, '20  Ignition switch', 3, w='bold'); txt(358, 41, '30: battery in (grey)', 2.3, fill='#555')
txt(358, 45, 'X: live with key on (red)', 2.3, fill='#555')                   # manual PDF p. 375

# ---- rear lights: Combi Coupé (this car) --------------------------------
# The car is a 3-door Combi Coupé: each rear light has four bulbs over one earth bar, R top to bottom indicator, tail,
# brake, reversing and L its vertical mirror (indicator at the bottom, outboard like R's at the top). One tail bulb
# each: 42 feeds the left, 44 the right. 44 also feeds the two number-plate lamps through 2-pole connector 59 (probably
# where the harness enters the tailgate): 44 from 58 and the onward 44 to the right tail bulb both sit on 59's body-side
# pin, so 59 hangs from the 44 run with that pin's terminal on the wire (no splice ahead of it). 47 leaves the tailgate
# side for the first lamp and 47a links that lamp to the second. From the 1977/78 Turbo Combi Coupé diagrams (no 1979
# one exists), so 59's pins and the number-plate lamps are grey (probably) and 47/47a dashed. Neither light has an earth
# lead on those diagrams: each bar leaves through a grey exit terminal to a grey earth, as on the signals sheet (check
# R3). 42 and 44 pass tail lamp connector 58, pins 2 and 1: two short blocks in one column, captioned above so 59's
# caption can sit left of 59. The wire labels sit on the long runs further left. Feeds drawn on the signals sheet end
# in open terminals on the outline, captioned with the cable that arrives there.
xL, xB, xE, xR, rr = 364, 372, 379, 382, 3.2         # light: left edge, bulbs, earth bar, right edge; bulb radius
x58 = 310                                            # 58 blocks (left edge), clear of 41 at x 304
xp, xa, xb = 337, 368.5, 391.5                       # 59's used pin; number-plate lamp terminals


def grey_earth(x, y):
    """common.earth() in grey: an earth that is probably there but not printed."""
    A(f'<path d="M{x},{y} v3 M{x - 3},{y + 3} h6 M{x - 2},{y + 4.3} h4 M{x - 1},{y + 5.6} h2" stroke="{_ink(True)}" '
      f'stroke-width=".5" fill="none"/>')


def cluster(y0, side, bulbs):
    """Rear light: bulbs (legend no., name, open-lead cable; None for the tail bulb) top to bottom; the top bulb's
    lead starts the earth bar. Its way out through the bottom edge is grey, as on the signals sheet: the Combi Coupé
    diagrams print no earth lead (check R3). Returns the tail bulb's feed height."""
    box(xL, y0, xR - xL, 36, fill='#fdfdfd', sw=.6)
    txt((xL + xR) / 2, y0 - 2, f'Rear lamp cluster {side}', 2.6, 'middle')
    ys = [y0 + 4.5 + 9 * i for i in range(4)]
    inner([(xB + rr, ys[0]), (xE, ys[0]), (xE, ys[3])])                            # earth bar
    inner([(xE, ys[3]), (xE, y0 + 36)], grey=True); grey_earth(xE, y0 + 36)         # its way out: none printed (R3)
    A(f'<circle cx="{xE}" cy="{y0 + 36}" r="1.0" fill="{_ink(True)}"/>')              # grey exit terminal, as on signals
    for i, (yy, (n, nm, c)) in enumerate(zip(ys, bulbs)):
        indicator(xB, yy, rr, 'tb') if nm == 'indicator' else lamp(xB, yy, r=rr)
        if i: inner([(xB + rr, yy), (xE, yy)]); jdot(xE, yy)
        if c:                                                                      # fed on the signals sheet
            contact(xL, yy); inner([(xL + .8, yy), (xB - rr, yy)])
            txt(xL - 2, yy + .75, f"{c} {WIRES[c]['colour']}: signals sheet", 2.0, 'end', fill='#555')
        else:
            inner([(xL, yy), (xB - rr, yy)]); ty = yy
        txt(xR + 2, yy + .8, f'{n} {nm}', 2.2, fill='#555' if c else '#111')
    txt(xE + 4.5, y0 + 40.8, 'earth: check R3', 2.0, fill='#555')
    return ty


def conn58(y, pin):
    """One pin of tail lamp connector 58: a short block, its pin number inside, the name above it."""
    A(f'<rect x="{x58}" y="{y - 3}" width="6" height="6" fill="#ddd" stroke="#111" stroke-width=".6"/>')
    tlabel(x58 + 3, y + .65, pin, 'middle'); txt(x58 + 3, y - 4.2, '58 tail lamps', 2.0, 'middle', fill='#555')


def plate_lamp(x, y):
    """Number-plate lamp 15 (a 5 W festoon) hanging from its feed terminal (x, y), with its own earth. Grey: probably."""
    c, r = _ink(True), 3.0; cy, k = y + 6, round(3.0 * .7, 2)
    inner([(x, y), (x, cy - r)], grey=True)
    A(f'<circle cx="{x}" cy="{cy}" r="{r}" fill="#fff" stroke="{c}" stroke-width=".6"/>'
      f'<path d="M{x - k},{cy - k} L{x + k},{cy + k} M{x - k},{cy + k} L{x + k},{cy - k}" stroke="{c}" stroke-width=".45"/>')
    grey_earth(x, cy + r)


yR = cluster(102.5, 'R', (('28', 'indicator', '79'), ('14', 'tail', None), ('30', 'brake', '133'), ('32', 'reversing', '137')))
yL = cluster(188, 'L', (('32', 'reversing', '136'), ('30', 'brake', '132'), ('14', 'tail', None), ('27', 'indicator', '76')))
conn58(yR, '1'); conn58(yL, '2')
wire('44', [(255, 125), (255, yR), (x58, yR)], 262, yR - 1.5)
wire('44', [(x58 + 6, yR), (xp, yR)], label=False)                                  # to 59's body-side pin
wire('44', [(xp, yR), (xL, yR)], label=False)                                       # from the same pin to the right tail bulb
wire('42', [(255, 178), (255, yL), (x58, yL)], 262, yL - 1.5)
wire('42', [(x58 + 6, yL), (xL, yL)], label=False)
# 59: two pins, no numbers printed, hanging from the 44 run: body side up, tailgate side down. The used pin runs from
# its body-side terminal on 44 to the tailgate-side terminal where 47 leaves; the other one carries nothing (check R5).
yT, yB = yR + 2, yR + 6                                                             # block top and bottom
y59 = yB + 31.5                                                                     # 47's corner: mid-dash
A(f'<rect x="{xp - 2}" y="{yT}" width="7" height="{yB - yT}" fill="#ddd" stroke="#111" stroke-width=".6"/>')
inner([(xp, yR), (xp, yB)], grey=True); inner([(xp + 3, yT), (xp + 3, yB)], grey=True)
txt(xp - 3.5, yT + 1.8, '59 number plate', 2.0, 'end', fill='#555')
txt(xp - 3.5, yT + 4.6, '(probably at the tailgate)', 2.0, 'end', fill='#555')
wire('47', [(xp, yB), (xp, y59), (xa, y59)], xp + 3, y59 - 1.5)                    # 63 mm, 47a 23: dashes meet both ends
wire('47a', [(xa, y59), (xb, y59)], xa + 2, y59 - 1.5)
plate_lamp(xa, y59); plate_lamp(xb, y59)
txt(xa - 1, y59 + 20, '15', 2.6, w='bold'); txt(xa + 3, y59 + 20, 'Number-plate lamps', 2.6)
for p in ((xL, yR), (xL, yL), (x58, yR), (x58 + 6, yR), (x58, yL), (x58 + 6, yL), (xp, yR), (xp, yB), (xa, y59), (xb, y59)):
    dot(*p)

# terminal dots and junctions go on top of the wires that end on them
for p in [(x, yb) for x in bt.values()] + [(324, 36), (324, 48), (345, 36), (345, 48), (255, 125), (255, 178),
                                           (150, 149), (bt['S'], 264), (198, y9), mR, dR, cR, mL, dL, cL, dropL, pR, pL,
                                           kR, kL, vR, vL, eR, eL, (80, ky + 19), (86, ky + 19), (76, ky + 19), T['6'],
                                           (80, ky + 27), (86, ky + 27), (kx, ky + 19), (kx + 18, ky + 6), (kx + 18, ky + 25), (kx + 8, ky + 30)]:
    dot(*p)

# ---- legend ------------------------------------------------------------
lx, ly = 250, 234.5                          # top 2.4 mm under cluster L's earth; ten note lines fit above the frame
box(lx, ly, 157, 52.5, fill='#fff', sw=.5)
txt(lx + 3, ly + 5, 'Cable key: number · colour · mm²', 3, w='bold')
size_legend(lx + 72, ly + 5)                 # on the heading row, right of its 'mm²'; its '4' ends near lx + 150
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 9.5 + (i // 4) * 4.5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x, y = lx + 97, ly + 9.5
A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x},{y + 4} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 11, y + 5, 'not traced yet', 2.4)
A(f'<path d="M{x},{y + 9} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{y + 9}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
txt(x + 11, y + 10, 'ends on diagram', 2.4)
if TICKED[0]: tick(x + 33, y + 9.3); txt(x + 37, y + 10, 'checked on the car', 2.4)
probable_legend(lx + 4, ly + 19)
gx, gy = lx + 47, ly + 19                    # ghost blade sample, right of the grey one: open at rest, dashed where it goes
A(f'<path d="M{gx + 1.7},{gy - .3} L{gx + 7.2},{gy - .3}" fill="none" {GHOST}/>'); contact(gx + 1, gy); contact(gx + 8, gy)
blade(gx + 1.7, gy - .3, gx + 7.6, gy - 2.4); txt(gx + 11, gy + 1, 'faded blade: position when pulled', 2.4)   # names the blade, not the dash: K1/K2's links are grey dashes too
notes = ['Headlamps need the ignition on (except the flash, stalk 9); parking/tail lights do not: light switch 2 is fed from ignition',   # manual PDF p. 375, 413
         'switch X, light switch 3 from the always-live bar. Headlamps are unfused: relay 30 is fed straight from the supply bar (20 GR 1.5).',
         'Not RHD-specific: circuits should match the car, but harness routing and part positions may differ.',
         'All bulbs in a lamp housing share its one earth (rear lights: check R3). The rear is drawn for the Combi Coupé (this car): fuse 2 probably also',
         'feeds the number-plate lamps through 44 and connector 59. These lamps, 59 and 47/47a (dashed): not yet checked on the car (checks R1, R4, R5).',
         'Corner lamps (dashed): dash switch 117 with pilot lamp, fed from fuse 5 (checks E19, F4); wiring probably as drawn,',
         'colours: check E19b. 221 reaches the left housing through pin 2 of front lamp connector 58; 222a branches off for the right.',
         'One bulb, two filaments: 5 W parking 13 from light switch 10, no ignition; 21 W corner lamp 118 from 117, ignition on (check E21).',
         'Not drawn: a rear fog lamp (check E23) or a relay that cuts the corner lamps on dipped beam (check E22); probably neither is fitted.',
         'Relay 8: the car flashes the main beams (check D9), but flash contact D is drawn on 56b (dipped); which pin carries main: check D12.']
# Sources, not printed: corner lamps from the 1977 Turbo diagram (371-1/2) with the 1979 GL numbers (p.405); the 1979
# Turbo legend (p.406) lists 117/118 but its drawing leaves pin 2 of 58 (E2) bare. Not drawn: the 1980 switch 76 (rear
# bulb 75, via fuse 65 from 8:86) and the 1977 dip cut-out relay 77. Relay 8 is drawn as the 1979 print has it.
for j, n in enumerate(notes): txt(lx + 3, round(ly + 24.5 + j * 2.85, 2), n, 2.2, fill='#333')
save('lighting.svg')

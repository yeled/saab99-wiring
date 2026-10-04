#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE lighting sheet (A3 landscape SVG).

Layout lives here; wire identity, colour, size and status come from data/wires.csv.
Sources (code comments only, never printed): base diagram p.327 (371-23, RHD 1974), book photos P2 (headlamps),
P3 and P9b (relay 8, stalk 9, connector 58 by relay 21), P8 (light switch 10), and the manual's lighting relay page
364-3 (p.301, S 3490: coils 1 and 2, contact 3) for the relay's function.
"""
import math
from common import *

header('Saab 99 LE, model 1974 — Lighting circuit')
txt(14, 28.5, 'FRONT', 3.6, w='bold', fill='#777'); txt(14, 32.6, 'car’s right side at top', 2.2, fill='#777')
txt(410, 33, 'REAR', 3.6, 'end', w='bold', fill='#777'); txt(410, 37.2, '4-door saloon (this car)', 2.2, 'end', fill='#777')

# ---- local helpers (the Turbo's, lib unchanged) ------------------------------------------------------------------
# Helvetica advance widths (1/1000 em) to size tags and to start-anchor bold names (cairosvg misplaces a bold tspan
# in text that isn't start-anchored)
_W = dict(zip('abcdefghijklmnopqrstuvwxyz', (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
                                             556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500)))
_W.update(dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
                                                 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611))))
_W.update({' ': 278, ',': 278, '.': 278, '’': 222, '(': 333, ')': 333, '/': 278, '-': 333, ':': 278, ';': 278,
           '–': 556, '−': 584, '→': 1000, '←': 1000, '↔': 1000, '°': 400})


def tw(s, size, bold=False):
    return sum(556 if ch.isdigit() else _W.get(ch, 556) * (1.06 if bold else 1) for ch in s) / 1000 * size


def name(x, y, n, s, size=2.7, anchor='start'):
    """Component number (bold) and name, as the other sheets print them."""
    w = tw(n, size, True) + tw(' ' + s, size)
    x0 = x if anchor == 'start' else x - w / 2 if anchor == 'middle' else x - w
    txt(round(x0, 2), y, f'<tspan font-weight="bold">{n}</tspan> {s}', size)


def note(x, y, s, anchor='start', size=2.1):
    txt(x, y, s, size, anchor, fill='#555')


def mtag(x, y, lines, size=2.2, anchor='start'):
    """Destination tag of one or more lines, centred on y, lines 1.36 × size apart; width from the text.
    anchor='end': the box ends at x (the wire comes in from the right). Text is start-anchored (arrows)."""
    w = round(max(tw(s, size) for s in lines) + 3.2, 1)
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2) if len(lines) > 1 else 5.2
    x0 = x if anchor == 'start' else round(x - w, 2)
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines):
        txt(round(x0 + 1.5, 2), round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
    return x0, x0 + w


def jdot(x, y):
    """Junction inside a part: smaller than a terminal dot."""
    A(f'<circle cx="{x}" cy="{y}" r=".6" fill="#111"/>')


def lead(pts):
    """A lead the manual prints without a cable number (an earth stem): plain black."""
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')


def indicator(x, y, r, q):
    """Direction indicator bulb as the manual prints it: an X circle with two opposite quadrants filled black,
    left and right ('lr', front housings) or top and bottom ('tb', rear blocks)."""
    k = round(r * .7071, 2); a, b = (x - k, y - k), (x + k, y + k)
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    if q == 'lr':
        d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 0 {a[0]},{b[1]} Z M{x},{y} L{b[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{b[1]} Z'
    else:
        d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{a[1]} Z M{x},{y} L{a[0]},{b[1]} A{r},{r} 0 0 0 {b[0]},{b[1]} Z'
    A(f'<path d="{d}" fill="#111"/><path d="M{a[0]},{a[1]} L{b[0]},{b[1]} M{a[0]},{b[1]} L{b[0]},{a[1]}" stroke="#111" stroke-width=".45"/>')


DOTS = []                                   # terminal dots, drawn after every wire


# ---- front lamps: housing outline as the Turbo's lighting sheet draws it ------------------------------------------
hx = 45                                     # x of the headlamp bulbs


def housing(xf, xc, yc, hf, rr, s, ch):
    """Lamp housing: a heavy outline, tallest at the front (x = xf, half-height hf), whose top and bottom edges run to
    a rounded rear end (centre xc, radius rr); the front bulges out by s. A thin lens chord at x = ch.
    Returns the front's outer x and edge(x) -> (y of the top edge, y of the bottom edge)."""
    top, bot = yc - hf, yc + hf
    a = math.atan2(-hf, xf - xc) + math.acos(rr / math.hypot(xf - xc, hf))
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
    """Filament arc from (x0, y) to (x1, y), sagging s mm down the page (s < 0 bows it up)."""
    R = round(((x1 - x0) ** 2 / 4 + s * s) / (2 * abs(s)), 2)
    A(f'<path d="M{x0},{y} A{R},{R} 0 0 {0 if s > 0 else 1} {x1},{y}" fill="none" stroke="#111" stroke-width=".4"/>')


def headlamp(y, up=False):
    """Twin-filament headlamp 11/12 in its reflector, feeds in through the rounded end on the right (main 11 on the
    upper filament, dipped 12 on the lower, as the base diagram labels them), the common out through the front.
    The base diagram draws each lead running into its own filament, so the joins are black (read).
    up: a second lead leaves the main filament's right end up through the reflector's top (11/12 L: 42b, which the
    base diagram draws entering the upper filament on a diagonal of its own, beside 42a).
    Returns (main feed, dipped feed, common, up lead or None), all on the outline."""
    r, a, rr, e = 5.5, 3, 7.6, 3.2
    xo, edge = housing(34, hx, y, 10, rr, 2.2, 36)
    A(f'<circle cx="{hx}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    xh = round(hx + (rr * rr - a * a) ** .5, 2)
    for sy in (-1, 1):
        filament(hx - e, hx + e, y + sy * a, -sy * 1.5)
        inner([(xh, y + sy * a), (hx + e, y + sy * a)])
        inner([(hx - e, y + sy * a), (hx - r, y)])
    inner([(hx - r, y), (xo, y)])
    u = None
    if up:
        xu = 47; u = (xu, round(y - (rr * rr - (xu - hx) ** 2) ** .5, 2))
        inner([(hx + e, y - a), u]); jdot(hx + e, y - a)
    return (xh, y - a), (xh, y + a), (xo, y), u


def front_housing(yc, side, ind, cab):
    """Front lamp housing 13/28 (R) or 13/27 (L) as the base diagram draws it: parking bulb 13 (an X circle) fed through
    the top, indicator 27/28 (quadrants) beside it, its lead to an open terminal on the rounded end (wired on the signals
    sheet). No earth lead is drawn. Returns the parking feed on the top outline."""
    xp, rp, xi, ri = 44.5, 2.8, 53.5, 3.4
    xo, edge = housing(36, 56, yc, 10, 6.5, 2.4, 38.5)
    ytop = edge(xp)[0]
    inner([(xp, ytop), (xp, yc - rp)])                                     # parking feed, through the top
    inner([(xi + ri, yc), (61.7, yc)]); contact(62.5, yc)                  # indicator: signals sheet
    lamp(xp, yc, r=rp); indicator(xi, yc, ri, 'lr')
    name(65, yc - 4.4, '13', f'Parking light {side}', 2.6)
    note(65, yc + .75, f"{ind} indicator, {cab} {WIRES[cab]['colour']}: signals sheet", size=2.0)
    note(65, yc + 4.3, 'earth: probably through the housing', size=2.0)
    return (xp, ytop)


mR, dR, cR, _ = headlamp(84)
mL, dL, cL, uL = headlamp(205, up=True)
name(hx - 2, 100.2, '11/12', 'Headlamp R', 2.6, 'middle')            # 2 mm left: clear of 42b at x 60
name(44.5, 188.2, '11/12', 'Headlamp L', 2.6, 'end')
note(hx - 2, 103.6, 'upper 11 main, lower 12 dipped', 'middle', 1.9)
note(44.5, 191.6, 'upper 11 main, lower 12 dipped', 'end', 1.9)
pR = front_housing(46, 'R', '28', '23be')
pL = front_housing(252, 'L', '27', '23a')

# parking lights 13: from fuses 3 and 4 (power sheet), into the housing tops
wire('58', [(72, 31), (pR[0], 31), pR], 51, 29.3); mtag(72, 31, ['58 GN 0.75 ← fuse 3 (power sheet)'])
wire('57', [(84, 236), (pL[0], 236), pL], 51, 234.3); mtag(84, 236, ['57 BL 0.75 ← fuse 4 (power sheet)'])
DOTS += [pR, pL]

# headlamp earths: from the reflector fronts to the battery − strap (power sheet)
wire('46', [cR, (26, cR[1]), (26, 66), (34, 66)], 24.6, 82.6, rot=-90)
mtag(34, 66, ['46 SV 1.0 → battery − strap,', 'earth (power sheet)'])
wire('45', [cL, (26, cL[1]), (26, 224), (34, 224)], 24.6, 222.6, rot=-90)
mtag(34, 224, ['45 SV 1.0 → battery − strap,', 'earth (power sheet)'])
DOTS += [cR, cL]

# dipped beams: fused, from fuses 1 and 2 (power sheet). 44b crosses 42b once, plainly (as on the base diagram):
# 42b links the two main filaments and the right lamp's dipped feed lies inside that loop.
wire('44b', [(80, dR[1]), dR], 62.6, dR[1] - 1.7); mtag(80, dR[1], ['44b GL 1.5 ← fuse 1 (power sheet)'])
wire('44a', [(80, dL[1]), dL], 58, dL[1] - 1.7); mtag(80, dL[1], ['44a GR 1.0 ← fuse 2 (power sheet)'])
DOTS += [dR, dL]

# ---- lighting relay 8 ---------------------------------------------------------------------------------------------
# Read on book photos P3 and P9b (base diagram 371-23), function from 364-3 (S 3490). Coil 1 (86–31) pulls when the
# light switch feeds 86; its changeover contact, fed from 30, rests up (feeding coil 2's contact) and pulled down feeds
# contact 3. Coil 2 (30–S) pulls when stalk 9 earths S; its make contact (rest open) closes onto the F contact; it also
# moves contact 3. Contact 3 rests on 56a as the RHD print draws it (S 3490 draws it resting on the main side; it
# stays where the last pull left it), its other position, onto the F contact, printed dashed.
# Rearranged from the print (positions are ours): mirrored left to right, with 56a and 30 moved onto the left wall, so
# that 39 from the light switch reaches 86 on the right wall without crossing F's wires, and so that the 30 feed to
# coil 1's contact runs between the contacts and the coils instead of round the bottom (no crossings inside the
# relay but the coil links). The coil links are printed as thin solid lines: drawn mlink() as every relay is.
rx, ry, rw, rh = 112, 122, 64, 44
box(rx, ry, rw, rh)
name(rx + 37, ry - 2, '8', 'Lighting relay', 2.7)
T8 = {'56a': (rx, ry + 8), '30': (rx, ry + 24), 'F': (rx + 22, ry), '86': (rx + rw, ry + 32),
      'S': (rx + 28, ry + rh), '31': (rx + 50, ry + rh)}
Ca, Cf, P3 = (rx + 8, ry + 8), (rx + 22, ry + 10), (rx + 15, ry + 17)        # 56a contact, F contact, contact 3's pivot
Pf, Au, Al, PA = (rx + 36, ry + 10), (rx + 46, ry + 10), (rx + 46, ry + 17), (rx + 56, ry + 17)
inner([T8['56a'], (Ca[0] - .8, Ca[1])])                                      # 56a to its contact
inner([T8['F'], (Cf[0], Cf[1] - .8)])                                        # F to its contact
inner([(Au[0] - .8, Au[1]), (Pf[0] + .8, Pf[1])])                            # coil 1's upper contact to coil 2's contact
inner([(Al[0] - .8, Al[1]), (P3[0] + .8, P3[1])])                            # coil 1's lower contact to contact 3
inner([T8['30'], (PA[0], T8['30'][1]), (PA[0], PA[1] + .8)])                # 30 to coil 1's contact (pivot)
k2l, k2r, k2t, k2b = coil(rx + 24, ry + 28, 8, 8)                            # coil 2
k1l, k1r, k1t, k1b = coil(rx + 46, ry + 28, 8, 8)                            # coil 1
inner([k2b, T8['S']]); inner([k2l, (rx + 6, k2l[1]), (rx + 6, T8['30'][1])]); jdot(rx + 6, T8['30'][1])
inner([k1b, T8['31']]); inner([k1r, T8['86']])


def toward(p, q, back=.8):
    """End points of a blade from pivot contact p towards q: .7 off p's centre, stopping `back` short of q."""
    L = math.hypot(q[0] - p[0], q[1] - p[1]); ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
    return round(p[0] + .7 * ux, 2), round(p[1] + .7 * uy, 2), round(q[0] - back * ux, 2), round(q[1] - back * uy, 2)


GHOST = 'stroke="#bbb" stroke-width=".7" stroke-dasharray="1.3 .8"'   # the Turbo's faded blade


def ghost_to(p, q):
    x0, y0, x1, y1 = toward(p, q)
    A(f'<path d="M{x0},{y0} L{x1},{y1}" fill="none" {GHOST}/>')


def cname(x, y, t, anchor='middle'):
    """Our name for a coil or contact (the manual's numbers 1, 2, 3): small italic grey."""
    A(f'<text x="{x}" y="{y}" font-size="1.8" font-style="italic" text-anchor="{anchor}" fill="#666">{t}</text>')


FREE = (rx + 24.6, ry + 6.6)                                                  # coil 2's contact: free end, raised
ghost_to(PA, Al); ghost_to(Pf, Cf); ghost_to(P3, Cf)                         # pulled / other positions
for p in (Ca, Cf, P3, Pf, Au, Al, PA): contact(*p)
blade(*toward(PA, Au))                                                       # coil 1's contact: rests up
blade(*toward(Pf, FREE, back=0))                                             # coil 2's contact: open
blade(*toward(P3, Ca))                                                       # contact 3: rests on 56a
mlink([k1t, (k1t[0], ry + 13.3)])                                            # coil 1 to its contact
mlink([k2t, (k2t[0], ry + 8.1)])                                             # coil 2 to its contact
mlink([(k2t[0], ry + 21), (rx + 11, ry + 21), (rx + 11, ry + 12.4)])         # and on to contact 3
cname(k1l[0] - .8, k1t[1] + 1.4, '1', 'end'); cname(k2l[0] - .8, k2t[1] + 1.4, '2', 'end'); cname(P3[0], P3[1] + 3.0, '3')
for t, (x, y), dx, dy, anc in (('56a', T8['56a'], 1.2, -1.3, 'start'), ('30', T8['30'], 1.2, -1.3, 'start'),
                               ('F', T8['F'], 1.2, 3.2, 'start'), ('86', T8['86'], -1.2, -1.3, 'end'),
                               ('S', T8['S'], 1.2, -1.4, 'start'), ('31', T8['31'], 1.2, -1.4, 'start')):
    tlabel(x + dx, y + dy, t, anc)
DOTS += list(T8.values())

# relay 8's wires
wire('42a', [T8['F'], (T8['F'][0], 106), (68, 106), (68, mL[1]), mL], 84, 104.3)    # main beams, unfused
wire('42b', [uL, (uL[0], 172), (60, 172), (60, mR[1]), mR], 58.6, 152, rot=-90)
DOTS += [mR, mL, uL]
wire('41', [T8['F'], (T8['F'][0] + 5, ry - 5), (T8['F'][0] + 5, 100), (142, 100)], label=False)
mtag(142, 100, ['41 BL/VT 0.75 → high-beam indicator,', 'combination instrument 47:7', '(instruments sheet)'])
wire('44', [T8['56a'], (106, T8['56a'][1])], label=False)
mtag(106, T8['56a'][1], ['44 GR 1.5 → bar 1–2:', 'fuses 1 and 2 (power sheet)'], anchor='end')
wire('142', [T8['30'], (106, T8['30'][1])], label=False)
mtag(106, T8['30'][1], ['142 GR 1.5 ← bar 5–8,', 'always live (power sheet)'], anchor='end')
# 31: 147 to earth, 90 to ignition switch relay 21's coil (power sheet); 83 to the headlamp wiper relay is not drawn
x31, y31 = T8['31']
wire('147', [T8['31'], (x31, 184)], x31 - 1.5, 183.4, rot=-90); earth(x31, 184)
wire('90', [T8['31'], (x31 + 3, y31 + 3), (178, y31 + 3)], label=False)
mtag(178, y31 + 3, ['90 SV 0.75 ← ignition switch relay 21:85,', 'its coil (power sheet)'])
note(x31 + 4, 176.2, '8:31 to the headlamp wipers: not fitted on this car')   # 83 SV from 31 to their relay: not drawn

# S: 141 through the dimmer connector 58 to stalk 9
xS, yS = T8['S']
Y58 = 186
wire('141', [T8['S'], (xS, Y58)], xS - 1.5, Y58 - 1.2, rot=-90)
A(f'<rect x="{xS - 4}" y="{Y58}" width="8" height="4" fill="#ddd" stroke="#111" stroke-width=".5"/>')
inner([(xS, Y58), (xS, Y58 + 4)])
txt(xS - 5.5, Y58 + 2.9, '58 dimmer', 2.2, 'end', w='bold')
sx9, sy9, sr9 = 172, 201.5, 7.5                                              # stalk 9 circle
wire('141e', [(xS, Y58 + 4), (xS, sy9), (sx9 - sr9, sy9)], xS + 2, sy9 - 1.7)
DOTS += [(xS, Y58), (xS, Y58 + 4), (sx9 - sr9, sy9)]
# 9 as printed (P9b): a circle marked LH; one contact, open at rest, its blade pivoting on the 141e side and rising
# towards the fixed contact on the earth side, a push button on the blade; the earth hatch outside on the right
A(f'<circle cx="{sx9}" cy="{sy9}" r="{sr9}" fill="#fff" stroke="#111" stroke-width=".6"/>')
c9a, c9b = (sx9 - 4.5, sy9), (sx9 + 4.5, sy9)
inner([(sx9 - sr9, sy9), (c9a[0] - .8, sy9)]); inner([(c9b[0] + .8, sy9), (sx9 + sr9, sy9)])
contact(*c9a); contact(*c9b)
blade(c9a[0] + .6, sy9 - .35, c9b[0] - .3, sy9 - 3.2)
A(f'<path d="M{sx9 - .3},{sy9 - 1.9} V{sy9 - 4.6} M{sx9 - 1.8},{sy9 - 4.6} Q{sx9 - .3},{sy9 - 6.4} {sx9 + 1.2},{sy9 - 4.6} Z" '
  f'fill="#111" stroke="#111" stroke-width=".4"/>')
txt(c9a[0] + .2, sy9 + 3.6, 'LH', 1.8, 'middle', fill='#555')
lead([(sx9 + sr9, sy9), (sx9 + sr9 + 4, sy9)]); earth(sx9 + sr9 + 4, sy9)
name(sx9 - 7, 214.5, '9', 'Dimmer/flasher stalk', 2.6)
note(sx9 - 7, 218, 'pull: earths S (main/dipped, or flash)')

# ---- light switch 10 ----------------------------------------------------------------------------------------------
# As printed (P8): terminals on a dotted position line, 8 at the top (75 from above), 3, 4 and 5 below (their leads
# from the left); a heavy bar from upper left to lower right, 4's lead curving onto it; 5 with a second circle beside
# it. The bar is drawn starting just under 3's lead (the print runs it a little higher, over that lead, which would
# read as a join).
bx, by, bw, bh = 206, 52, 28, 38
box(bx, by, bw, bh)
xp = bx + 15
T10 = {'8': (xp, by), '3': (bx, by + 11.5), '4': (bx, by + 22), '5': (bx, by + 32)}
A(f'<path d="M{xp},{by + 4} V{by + 34}" stroke="#111" stroke-width=".35" stroke-dasharray=".5 1.1"/>')   # position line
c8, c3, c5 = (xp, by + 5.5), (xp, by + 11.5), (xp, by + 32)
inner([T10['8'], (xp, c8[1] - .8)])
inner([T10['3'], (c3[0] - .8, c3[1])])
inner([T10['5'], (c5[0] - .8, c5[1])]); inner([(c5[0] + .8, c5[1]), (xp + 4.2, c5[1])])
A(f'<path d="M{bx},{by + 22} H{bx + 8} Q{bx + 13.5},{by + 22} {bx + 15.8},{by + 24.5}" fill="none" stroke="#111" stroke-width=".4"/>')
for p in (c8, c3, c5, (xp + 5, c5[1])): contact(*p)
A(f'<path d="M{bx + 6.5},{by + 15} L{bx + 22.5},{by + 31.4}" stroke="#111" stroke-width="1.3" stroke-linecap="round"/>')   # bar
for t, (x, y) in (('8', c8), ('3', c3)): tlabel(x + 1.6, y + .65, t)
tlabel(bx + 6.5, by + 20.7, '4'); tlabel(bx + 6.5, by + 30.7, '5')            # 4 and 5 left of the bar, above their leads, as printed
DOTS += list(T10.values())
name(bx + bw + 3, by + 6, '10', 'Light switch', 2.7)
note(bx + bw + 3, by + 9.8, 'off · parking (4–5) ·')
note(bx + bw + 3, by + 13, 'headlamps (4–5 and 8–3): probably')
wire('75', [T10['8'], (xp, 44), (xp + 4, 44)], label=False); mtag(xp + 4, 44, ['75 RD 1.0 ← ignition switch 20:X (power sheet)'])
wire('76', [T10['4'], (196, T10['4'][1]), (196, 113), (200, 113)], label=False)
mtag(200, 113, ['76 GR 1.0 ← bar 5–8, always live (power sheet)'])
wire('50', [T10['5'], (201, T10['5'][1]), (201, 104), (204, 104)], label=False)
mtag(204, 104, ['50 GN 1.0 → bar 3–4: fuses 3 and 4 (power sheet)'])
wire('39', [T10['3'], (190, T10['3'][1]), (190, T8['86'][1]), T8['86']], 188.6, 150, rot=-90)

# ---- tail lights: connector 58 and the rear lamp blocks -----------------------------------------------------------
X58, R1, R2 = 300, 140, 150
A(f'<rect x="{X58 - 2}" y="{R1 - 4}" width="4" height="{R2 - R1 + 8}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
for ry_ in (R1, R2): inner([(X58 - 2, ry_), (X58 + 2, ry_)])
tlabel(X58, R1 - 1.3, '1', 'middle'); tlabel(X58, R2 - 1.3, '2', 'middle')
txt(X58, R2 + 7.6, '58 tail lights', 2.2, 'middle', w='bold')
wire('54', [(266, R1), (X58 - 2, R1)], 270, R1 - 1.7); mtag(266, R1, ['54 GN 0.75 ← fuse 3 (power sheet)'], anchor='end')
wire('53', [(266, R2), (X58 - 2, R2)], 270, R2 - 1.7); mtag(266, R2, ['53 BL 0.75 ← fuse 4 (power sheet)'], anchor='end')
wire('59', [(X58 - 2, R1), (X58 - 6, R1 - 4), (X58 - 6, 124), (X58 - 10, 124)], label=False)
mtag(X58 - 10, 124, ['59 GN 0.75 → rheostat 16,', 'panel lighting (instruments sheet)'], anchor='end')
DOTS += [(X58 - 2, R1), (X58 + 2, R1), (X58 - 2, R2), (X58 + 2, R2)]

xL, xB, xE, xR, rb = 368, 377, 383.5, 386, 2.9          # block: left wall, bulbs, earth bar, right wall; bulb radius


def rear_block(y0, side, bulbs):
    """Rear lamp block as the base diagram draws it: five compartments, a bulb in each, an earth bar down the right
    joined to every bulb (no earth lead leaves it). bulbs: (no., name, open-lead caption or None) top to bottom; the
    other sheet's bulbs end in open terminals on the left wall. The 14–15 link runs inside, left of the bulbs, crossing
    the leads between them plainly. Returns the y of each compartment by bulb number."""
    box(xL, y0, xR - xL, 40, fill='#fdfdfd', sw=.6)
    for i in range(1, 5): A(f'<path d="M{xL},{y0 + 8 * i} H{xR}" stroke="#bbb" stroke-width=".25"/>')
    ys = {n: y0 + 4 + 8 * i for i, (n, _, _) in enumerate(bulbs)}
    inner([(xE, y0 + 2.5), (xE, y0 + 37.5)])                                    # earth bar
    for (n, nm, cap) in bulbs:
        yy = ys[n]
        indicator(xB, yy, rb, 'tb') if nm == 'indicator' else lamp(xB, yy, r=rb)
        inner([(xB + rb, yy), (xE, yy)]); jdot(xE, yy)
        if cap:
            contact(xL, yy); inner([(xL + .8, yy), (xB - rb, yy)])
            note(xL - 2, yy + .75, f'{cap}: signals sheet', 'end', 2.0)
        else:
            inner([(xL, yy), (xB - rb, yy)])
        txt(xR + 2, yy + .8, f'{n} {nm}', 2.2, fill='#555' if cap else '#111')
    a, b = sorted((ys['14'], ys['15']))
    inner([(xL + 3, a), (xL + 3, b)]); jdot(xL + 3, a); jdot(xL + 3, b)        # 14–15 link
    txt((xL + xR) / 2, y0 - 2, f'Rear lamp block {side}', 2.6, 'middle')
    note((xL + xR) / 2, y0 + 44.2, 'earth: probably through the housing', 'middle', 2.0)
    return ys


yR = rear_block(50, 'R', (('28', 'indicator', '25b RD/VT'), ('14', 'tail', None), ('30', 'stop', '28f RD'),
                          ('32', 'reversing', '98 VT'), ('15', 'number plate', None)))
yLb = rear_block(195, 'L', (('15', 'number plate', None), ('32', 'reversing', '97/98 VT'), ('30', 'stop', '28e/28f RD'),
                            ('14', 'tail', None), ('27', 'indicator', '25a BL/VT')))
wire('54b', [(X58 + 2, R1), (320, R1), (320, yR['14']), (xL, yR['14'])], 322, yR['14'] - 1.7)
wire('53a', [(X58 + 2, R2), (320, R2), (320, yLb['14']), (xL, yLb['14'])], 322, yLb['14'] - 1.7)
wire('56b', [(xL, yR['15']), (344, yR['15'])], 345.5, yR['15'] - 1.7)
wire('55a', [(xL, yLb['15']), (344, yLb['15'])], 345.5, yLb['15'] - 1.7)
DOTS += [(xL, yR['14']), (xL, yR['15']), (xL, yLb['14']), (xL, yLb['15'])]

for p in DOTS: dot(*p)

# ---- relay 8 states (our aid): paths use the manual's numbers for the coils (1, 2) and contact 3 --------------------
# Contact 3 moves with coil 2's contact (364-3: "mechanically influenced by the contact at relay coil (2)"), so every
# pull, a flash with the lights off included, moves it, and the headlamps come on wherever the last pull left it: row 3
# says "dipped or main" and the last row, spanning the table, says why.
TX, TY, RH8 = 196, 193, 3.3
C8 = [TX, TX + 28, TX + 38, TX + 80, 300]
ROWS8 = [('lights off', '–', '30 → 1’s contact (up) → 2’s contact: open', 'nothing'),
         ('flash, lights off', '2', '30 → 1’s contact (up) → 2’s contact → F', 'main beams'),
         ('headlamps on', '1', '30 → 1’s contact (down) → 3 → 56a or F', 'dipped or main'),
         ('headlamps on, stalk pulled', '1, 2', '2 moves 3 over (56a ↔ F); it stays', 'dipped ↔ main')]
name(TX, TY - 5, '8', 'Lighting relay: what it does', 2.4)
note(TX + 38, TY - 5, 'drawn at rest: lights off, stalk released')
for x, h in zip(C8, ('state', 'coils', 'path (each starts at terminal 30)', 'lights')):
    note(x + 1, TY - 1.2, h, size=2.0)
grid = ([f'M{TX},{round(TY + j * RH8, 2)} H{C8[-1]}' for j in range(6)] + [f'M{x},{TY} V{round(TY + 4 * RH8, 2)}' for x in C8[1:-1]]
        + [f'M{x},{TY} V{round(TY + 5 * RH8, 2)}' for x in (C8[0], C8[-1])])
A(f'<path d="{" ".join(grid)}" stroke="#ccc" stroke-width=".2"/>')
for j, cells in enumerate(ROWS8):
    y = round(TY + (j + .5) * RH8 + .75, 2)
    for x, s in zip(C8, cells): txt(x + 1, y, s.replace('↔', '<tspan font-family="Arial">↔</tspan>'), 2.1, fill='#222')
txt(TX + 1, round(TY + 4.5 * RH8 + .75, 2), 'Every pull of the stalk moves 3 over, a flash with the lights off too, and 3 stays there until the next pull.',
    2.1, fill='#222')

# ---- legend -------------------------------------------------------------------------------------------------------
lx, ly = 140, 241
box(lx, ly, 160, 45.5, fill='#fff', sw=.5)
txt(lx + 3, ly + 5, 'Cable key: number · colour · mm²', 3, w='bold')
size_legend(lx + 72, ly + 5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 10 + (i // 4) * 4.5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x, y = lx + 97, ly + 10
A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
yy = y + 4.5
if DASHED[0]:
    A(f'<path d="M{x},{yy - 1} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 11, yy, 'not traced yet', 2.4); yy += 4.5
if STUB[0]:
    A(f'<path d="M{x},{yy - 1} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{yy - 1}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    txt(x + 11, yy, 'ends on diagram', 2.4)
if TICKED[0]:
    tx_ = x + 37 if STUB[0] else x
    tick(tx_ + 3, yy - .7); txt(tx_ + 11, yy, 'checked on the car', 2.4)
gy = ly + 20
gx = lx + 4 + (47 if probable_legend(lx + 4, gy) else 0)
A(f'<path d="M{gx + 1.7},{gy - .3} L{gx + 7.2},{gy - .3}" fill="none" {GHOST}/>'); contact(gx + 1, gy); contact(gx + 8, gy)
blade(gx + 1.7, gy - .3, gx + 7.6, gy - 2.4); txt(gx + 11, gy + 1, 'faded blade: its other position', 2.4)
mlink([(gx + 63, gy - .2), (gx + 72, gy - .2)]); txt(gx + 74, gy + 1, 'coil to the contacts it moves', 2.4)
notes = ['Main beams come straight from relay 8:F, not fused; dipped beams through fuses 1 and 2 (power sheet).',
         'Relay 8 changes over between main and dipped each time stalk 9 earths its terminal S (headlamps on);',
         'with the headlamps off, the same pull flashes the main beams.',
         'The headlamps need the ignition on (light switch 10:8 is fed from ignition switch 20:X); parking and tail lights and the flash do not.',
         '56b and 55a, from the number-plate lights, end on the diagram: where they go is not known.']
# 56b/55a: the towing attachment page (952-2) also prints the number-plate light as a 5 W bulb in each rear block and
# 56b as the same short stub (the trailer socket's tail feed there is 54bh, not 56b), so neither page says where they go.
for j, n in enumerate(notes): txt(lx + 3, round(ly + 26 + j * 3.6, 2), n, 2.25, fill='#333')
save('lighting.svg')

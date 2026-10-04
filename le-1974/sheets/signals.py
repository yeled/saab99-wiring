#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE signals sheet: indicators, hazards, brake and reversing lights (A3 SVG).

Layout lives here; every numbered cable's colour, size and status come from data/wires.csv.
Sources (not printed on the sheet): the 1974 RHD main diagram (PDF p.327) for the flasher, switches 24/25, 59 (E11),
57 (E3), stop contact 29, 60 (F13), the lamp housings and rear blocks; the automatic detail (PDF p.348) for the
reversing feed through inhibitor switch 90 (95f -> 60 -> 95 -> 58 (F8) -> 96 -> 60 -> 97); book photo P8 for the
insides of 24 and 25 and for 59 (E11); book photo P2 for 23be.
"""
import math
from common import *

header('Saab 99 LE, model 1974 — Indicators, hazards, brake and reversing lights')

# ---- local helpers ----------------------------------------------------------------------------------------------
_HW = {' ': 278, '!': 278, '(': 333, ')': 333, ',': 278, '-': 333, '.': 278, '/': 278, ':': 278, ';': 278, '+': 584,
       'A': 667, 'B': 667, 'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'H': 722, 'I': 278, 'J': 500, 'K': 667,
       'L': 556, 'M': 833, 'N': 722, 'O': 778, 'P': 667, 'Q': 778, 'R': 722, 'S': 667, 'T': 611, 'U': 722, 'V': 667,
       'W': 944, 'X': 667, 'Y': 667, 'Z': 611, 'a': 556, 'b': 556, 'c': 500, 'd': 556, 'e': 556, 'f': 278, 'g': 556,
       'h': 556, 'i': 222, 'j': 222, 'k': 500, 'l': 222, 'm': 833, 'n': 556, 'o': 556, 'p': 556, 'q': 556, 'r': 333,
       's': 500, 't': 278, 'u': 556, 'v': 500, 'w': 722, 'x': 500, 'y': 500, 'z': 500, '’': 222, '–': 556, '—': 1000,
       '←': 1000, '→': 1000, '°': 400, '²': 333, '·': 278}


def tw(s, size):
    """Width of s in Helvetica at size (mm); digits 556."""
    return sum(_HW.get(c, 556) for c in s) / 1000 * size


def name(x, y, n, s, anchor='start', size=2.6):
    """Part name: bold number, then the name."""
    txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', size, anchor)


def mtag(x, y, lines, size=2.2, anchor='start'):
    """Destination tag of one or more lines, sized to its text, centred on y; anchor 'end' puts its right edge on x
    (the text itself stays start-anchored: cairo misplaces 'end' text that holds an arrow). Returns its far edge."""
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2)
    w = round(max(tw(s, size) for s in lines) + 3.2, 1); x0 = x if anchor == 'start' else round(x - w, 2)
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines): txt(round(x0 + 1.6, 2), round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
    return round(x0 + w, 2) if anchor == 'start' else x0


def conn_h(x, y, lab, below=False, w=4, h=8):
    """Connector pin on a horizontal run: a grey block w across the run, h tall, centred (x, y); its name above it
    (lab: one string per line, small grey), or under it. Dots on both faces go on after the wires."""
    A(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    y0 = y + h / 2 + 3.0 if below else y - h / 2 - 1.4 - 2.6 * (len(lab) - 1)
    for i, s in enumerate(lab): txt(x, round(y0 + 2.6 * i, 2), s, 2.2, 'middle', fill='#555')


def conn_v(x, y, w=8, h=4):
    """Connector pin on a vertical run: a grey block h along the run, w across, centred (x, y)."""
    A(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')


def jdot(x, y):
    """Junction inside a part: smaller than a terminal dot."""
    A(f'<circle cx="{x}" cy="{y}" r=".6" fill="#111"/>')


def indicator(x, y, r, q='lr'):
    """Direction indicator bulb as the manual prints it: an X circle with two opposite quadrants filled black (left and
    right on this print, front and rear alike; also the hazard repeater 26)."""
    k = round(r * .7071, 2); a, b = (round(x - k, 2), round(y - k, 2)), (round(x + k, 2), round(y + k, 2))
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    if q == 'lr':
        d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 0 {a[0]},{b[1]} Z M{x},{y} L{b[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{b[1]} Z'
    else:
        d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{a[1]} Z M{x},{y} L{a[0]},{b[1]} A{r},{r} 0 0 0 {b[0]},{b[1]} Z'
    A(f'<path d="{d}" fill="#111"/><path d="M{a[0]},{a[1]} L{b[0]},{b[1]} M{a[0]},{b[1]} L{b[0]},{a[1]}" stroke="#111" stroke-width=".45"/>')


def housing_line(pts):
    """A line of a part's housing, not a conductor (a lamp unit's earth strip, a compartment wall): thinner than inner()."""
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".3"/>')


DOTS = []                                   # terminal and joint dots, drawn last (on top of the wires)


# ---- front lamp housings (left edge; the car's right side at the top) ------------------------------------------
def front_housing(yc, side, ind, park_cable):
    """Front lamp housing 13/27 or 13/28 as printed: a rounded front (left) with the lens chord, tapering to a rounded
    rear end (right). Parking light 13 at the front is wired on the lighting sheet: an open terminal on the top edge
    where its feed comes in, captioned with its cable. Indicator ind in the rounded end, fed at the tip from the right.
    No earth lead is printed for the housing. Returns the tip (indicator feed)."""
    xf, xc, hf, rr, s, ch = 22, 46, 8.5, 5.6, 2.2, 25
    top, bot = yc - hf, yc + hf
    a = math.atan2(-hf, xf - xc) + math.acos(rr / math.hypot(xf - xc, hf))
    tx, ty = round(xc + rr * math.cos(a), 2), round(yc + rr * math.sin(a), 2)
    k = (ty - top) / (tx - xf)
    edge = lambda x: (round(top + k * (x - xf), 2), round(bot - k * (x - xf), 2))
    rb = round((hf * hf + s * s) / (2 * s), 2)
    A(f'<path d="M{xf},{top} L{tx},{ty} A{rr},{rr} 0 0 1 {tx},{round(2 * yc - ty, 2)} L{xf},{bot} '
      f'A{rb},{rb} 0 0 1 {xf},{top} Z" fill="#fdfdfd" stroke="#111" stroke-width=".8"/>')
    t, b = edge(ch); housing_line([(ch, round(t + .4, 2)), (ch, round(b - .4, 2))])
    xp, rp, ri = 31, 3.0, 3.6                          # parking bulb x and radius; indicator radius
    lamp(xp, yc, r=rp); indicator(xc, yc, ri)
    tip = (xc + rr, yc)
    inner([(xc + ri, yc), tip])                        # indicator feed from the tip
    yt = edge(xp)[0]; contact(xp, yt); inner([(xp, round(yt + .8, 2)), (xp, yc - rp)])   # parking feed: lighting sheet
    txt(xp + 2.2, round(yt - 1.6, 2), f"{park_cable} {WIRES[park_cable]['colour']}: lighting sheet", 2.0, fill='#555')
    name(16, round(yt - 6.2, 2), f'13/{ind}', f'Front lamp housing, {side}', size=2.4)
    txt(16, round(bot + 4.4, 2), f'13 parking light, {ind} indicator', 2.0, fill='#555')
    txt(16, round(bot + 7.2, 2), 'earth: probably through the housing', 2.0, fill='#555')
    return tip


# ---- rear lamp blocks (right edge) --------------------------------------------------------------------------------
W, BW, RP = 372, 16, 10                     # the blocks' left wall (terminals), width, row pitch
BX, BR_, BS = W + 8.4, 3.4, W + 11.8        # bulb centre x, bulb radius, the earth strip (bulbs touch it)
LINK, HOP = W + 2.6, 1.0                    # the 14-15 link inside the block; the radius of its hops


def rear_block(y0, side, rows):
    """Rear lamp block as printed: five cells, a bulb in each against the strip on its right, terminals on the left
    wall. rows: (bulb no., name, cable from the lighting sheet or None) top to bottom. Feeds wired here end on terminal
    dots (drawn last); the lighting sheet's bulbs get an open terminal and a caption with their cable. Tail light 14
    and number-plate light 15 are joined inside the block; the link hops the leads between them. Returns {bulb no.: row y}."""
    h = RP * len(rows)
    box(W, y0, BW, h, fill='#fdfdfd', sw=.6)
    for i in range(1, len(rows)): housing_line([(W, y0 + RP * i), (W + BW, y0 + RP * i)])
    housing_line([(BS, y0), (BS, y0 + h)])
    ys = {}
    for i, (n, nm, cab) in enumerate(rows):
        y = y0 + RP / 2 + RP * i; ys[n] = y
        indicator(BX, y, BR_) if nm == 'indicator' else lamp(BX, y, r=BR_)
        if cab:
            contact(W, y); inner([(W + .8, y), (BX - BR_, y)])
            txt(W - 2.2, round(y - .5, 2), f"{cab} {WIRES[cab]['colour']}:", 2.0, 'end', fill='#555')
            txt(W - 2.2, round(y + 2.2, 2), 'lighting sheet', 2.0, 'end', fill='#555')
        else:
            inner([(W, y), (BX - BR_, y)])
        name(W + BW + 2, round(y + .9, 2), n, nm, size=2.2) if not cab else \
            txt(W + BW + 2, round(y + .9, 2), f'<tspan font-weight="bold">{n}</tspan> {nm}', 2.2, fill='#555')
    # the 14-15 link hops over the leads of the bulbs between them (30, 32): a crossing, not a join
    a, b = sorted((ys['14'], ys['15'])); d = f'M{LINK},{a}'
    for y in sorted(v for v in ys.values() if a < v < b): d += f' V{y - HOP} A{HOP},{HOP} 0 0 1 {LINK},{y + HOP}'
    A(f'<path d="{d} V{b}" fill="none" stroke="#111" stroke-width=".4"/>'); jdot(LINK, a); jdot(LINK, b)
    txt(W, y0 - 2.2, f'Rear lamp block, {side}', 2.4, w='bold')
    txt(W, y0 + h + 3.6, 'earth: probably through the housing', 2.0, fill='#555')
    return ys


# ================================================================================================================
txt(14, 31, 'FRONT', 3.6, w='bold', fill='#777'); txt(14, 35.5, 'car’s right side at top', 2.3, fill='#777')
txt(66, 32, 'Indicators and hazards', 3.4, w='bold')
txt(406, 141, 'REAR', 3.6, 'end', w='bold', fill='#777'); txt(406, 145.5, 'car’s right side at top', 2.3, 'end', fill='#777')

# ---- flasher 23 ------------------------------------------------------------------------------------------------------
# As printed (p.327): a box with the flasher's filled bow-tie and a strip on its right with X, P and L top to bottom;
# no earth terminal is drawn.
FX0, FX1, FY0, FY1 = 72, 98, 78, 102
TX, TP, TL = 84, 90, 96                     # terminal heights on the right wall
box(FX0, FY0, FX1 - FX0, FY1 - FY0)
FS = 90                                     # the strip's left edge
housing_line([(FS, FY0), (FS, FY1)])
fm = (FX0 + FS) / 2; fy = (FY0 + FY1) / 2
A(f'<path d="M{FX0 + .5},{FY0 + .5} L{fm},{fy} L{FX0 + .5},{FY1 - .5} Z M{FS - .5},{FY0 + .5} L{fm},{fy} L{FS - .5},{FY1 - .5} Z" '
  f'fill="#111" stroke="#111" stroke-width=".3" stroke-linejoin="round"/>')
A(f'<path d="M{FX0 + .5},{FY0 + .5} L{FS - .5},{FY1 - .5} M{FX0 + .5},{FY1 - .5} L{FS - .5},{FY0 + .5}" stroke="#111" stroke-width=".4"/>')
for t, y in (('X', TX), ('P', TP), ('L', TL)):
    tlabel(FS + 2.0, y + .65, t); DOTS.append((FX1, y))
name(FX0, FY0 - 2.4, '23', 'Flasher unit')

# 21 RD/VT from fuse 8 into X, from above; 62 GN/VT from P up to the instruments sheet; 22 GN from L to the hazard switch
X21, X62 = 112, 118
t21 = mtag(66, 50, ('21 RD/VT 1.0 ← fuse 8 (power sheet)',), size=2.2)
wire('21', [(t21, 50), (X21, 50), (X21, TX), (FX1, TX)], X21 + 3.3, 81, rot=-90)
wire('62', [(FX1, TP), (X62, TP), (X62, 38), (X62 + 2, 38)], label=False)
mtag(X62 + 2, 38, ('62 GN/VT 0.75 → indicator repeater,', 'combination instrument 47:6 (instruments sheet)'), size=2.2)

# ---- hazard switch 25 with repeater lamp 26 ---------------------------------------------------------------------------
# As printed (book photo P8): a tall box, repeater lamp 26 in a compartment at its top; below it a column of four
# contacts: lamp contact, + (a through-terminal: 22 in, 22e out), R, L; a heavy bar beside them touching none (off).
# The dotted marks between the contacts are the print's: pressed, the bar joins them (probably all four).
HX0, HX1, HY0, HY1 = 122, 144, 70, 118
HC = 131                                    # contact column
YLC, YP, YR, YL = 89, TL, 106, 113          # lamp contact, +, R, L
box(HX0, HY0, HX1 - HX0, HY1 - HY0)
housing_line([(HX0, 83), (HX1, 83)])        # the lamp's compartment
indicator(HC, 76.5, 2.8)
inner([(HC, 73.7), (HC, HY0)]); DOTS.append((HC, HY0))                     # earth side: 26 SV, out through the top
inner([(HC - 2.8, 76.5), (126, 76.5), (126, YLC), (HC - .8, YLC)])        # live side: on the lamp contact
for y in (YLC, YP, YR, YL): contact(HC, y)
inner([(HX0, YP), (HC - .8, YP)]); inner([(HC + .8, YP), (HX1, YP)])      # + : 22 in, 22e out
inner([(HC + .8, YR), (HX1, YR)]); inner([(HC + .8, YL), (HX1, YL)])
for y0, y1 in ((YLC, YP), (YP, YR), (YR, YL)):                            # the print's dotted marks
    A(f'<path d="M{HC},{y0 + 1.5} V{y1 - 1.5}" stroke="#111" stroke-width=".35" stroke-dasharray=".25 .9" stroke-linecap="round"/>')
blade(126.2, 99.5, 128.8, 116)              # the bar, off: touching none
tlabel(HC + 1.8, YP - 1.6, '+'); tlabel(HC + 1.8, YR - 1.2, 'R'); tlabel(HC + 1.8, YL - 1.2, 'L')
for y in (YP, YR, YL): DOTS.append((HX1, y))
DOTS.append((HX0, YP))
name(HX0, HY1 + 4.2, '25', 'Hazard warning switch')
name(HX1 + 2.4, 77.4, '26', 'Hazard repeater lamp', size=2.4)

wire('22', [(FX1, TL), (HX0, TL)], 100.5, TL - 1.5)
# 26 SV: from the lamp's earth side up and on to the dash earth (instruments sheet)
wire('26', [(HC, HY0), (HC, 52), (150, 52)], 133, 50.5)
mtag(150, 52, ('26 SV 1.0 → dash earth', '(instruments sheet)'), size=2.2)

# ---- indicator switch 24 ------------------------------------------------------------------------------------------------
# As printed (P8): 54 at the top right, fed by 22e along the top; a bar hangs from 54 between R (left) and L (right),
# touching neither (centre-off). 24be comes in on R from the left and 24b leaves R downwards; L's lead leaves through
# the bottom wall, where 24ae joins it just below the box (crossing 24b, as printed) and 24a carries on down.
SX0, SX1, SY0, SY1 = 172, 205, 90, 109
S54, SR, SL = 194.5, 188, 201          # L 13 right of R: 25b bends 5 clear of 23a under 59
box(SX0, SY0, SX1 - SX0, SY1 - SY0)
inner([(SX0, YP), (S54 - .8, YP)]); contact(S54, YP); blade(S54, YP + .7, S54, YR - .5)
contact(SR, YR); contact(SL, YR)
inner([(SX0, YR), (SR - .8, YR)]); inner([(SR, YR + .8), (SR, SY1)]); inner([(SL, YR + .8), (SL, SY1)])
tlabel(S54 + 1.5, YP - 1.4, '54'); tlabel(SR - 1.4, YR - 1.2, 'R', 'end'); tlabel(SL + 1.4, YR - 1.2, 'L')
DOTS += [(SX0, YP), (SX0, YR), (SR, SY1), (SL, SY1)]
name(SX0, SY0 - 2.4, '24', 'Indicator switch')

wire('22e', [(HX1, YP), (SX0, YP)], 147, YP - 1.5)
wire('24be', [(HX1, YR), (SX0, YR)], 146.5, YR - 1.5)
wire('24ae', [(HX1, YL), (SL, YL)], 146.5, YL - 1.5); DOTS.append((SL, YL))

# ---- 59 indicators and the four indicator feeds ------------------------------------------------------------------------
# 59 (E11) as printed (P8): two pins side by side, the switch's 24b (pin 1) and 24a (pin 2) in from above; below,
# pin 1 sends 23b on down (front right) and 25b off to the right (rear right), pin 2 23a on down (front left) and 25a
# off to the right (rear left). 25b crosses 23a under the block and 25a's lane further on: with the pins side by
# side, two crossings here are the fewest (the print has the same two). The sheet's other crossings: 24ae over 24b
# under switch 24 (as printed; forced by R and L both going down) and 97 over 28f's riser by the left block (98 and
# 28f join the two blocks, so a feed from the left into 32 must cross one of them). 25a runs round below the brake
# and reversing runs instead of crossing them.
C59T, C59B = 141, 145
A(f'<rect x="{SR - 4}" y="{C59T}" width="{SL - SR + 8}" height="{C59B - C59T}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
inner([(SR, C59T), (SR, C59B)]); inner([(SL, C59T), (SL, C59B)])
txt(SR - 5.5, C59T + 2.9, '59 indicators', 2.2, 'end', fill='#555')
tlabel(SR + 1.2, C59T + 2.65, '1'); tlabel(SL + 1.2, C59T + 2.65, '2')
DOTS += [(SR, C59T), (SL, C59T), (SR, C59B), (SL, C59B)]
wire('24b', [(SR, SY1), (SR, C59T)], SR - 1.45, C59T - 1.5, rot=-90)
wire('24a', [(SL, SY1), (SL, C59T)], SL + 3.6, C59T - 1.5, rot=-90)

Y23B, Y23A, Y25A, Y25B = 158, 164, 148, 153
XR57, XL23 = 62, 56                         # the risers to the front housings
X25A, X25B = 214, 330                       # 25a's lane down, 25b's lane up
Y25BOT = 265                                # 25a's run along the bottom
Y57 = 115                                   # 57 front indicator R, on the riser
tipR = front_housing(64, 'R', '28', '58')
tipL = front_housing(232, 'L', '27', '57')
wire('23b', [(SR, C59B), (SR, Y23B), (XR57, Y23B), (XR57, Y57 + 2)], 120, Y23B - 1.5)
conn_v(XR57, Y57)
txt(XR57 - 5.5, Y57 - .4, '57 front', 2.2, 'end', fill='#555'); txt(XR57 - 5.5, Y57 + 2.3, 'indicator R', 2.2, 'end', fill='#555')
wire('23be', [(XR57, Y57 - 2), (XR57, tipR[1]), tipR], XR57 + 3.9, Y57 - 7, rot=-90)
DOTS += [(XR57, Y57 - 2), (XR57, Y57 + 2), tipR]
wire('23a', [(SL, C59B), (SL, Y23A), (XL23, Y23A), (XL23, tipL[1]), tipL], 80, Y23A - 1.5)
DOTS.append(tipL)

# ---- rear lamp blocks ------------------------------------------------------------------------------------------------------
yR = rear_block(36, 'R', (('28', 'indicator', None), ('14', 'tail', '54b'), ('30', 'stop', None),
                          ('32', 'reversing', None), ('15', 'number plate', '56b')))
yL = rear_block(202, 'L', (('15', 'number plate', '55a'), ('32', 'reversing', None), ('30', 'stop', None),
                           ('14', 'tail', '53a'), ('27', 'indicator', None)))
wire('25b', [(SR, C59B), (SR + 8, C59B + 8), (X25B, Y25B), (X25B, yR['28']), (W, yR['28'])], 240, Y25B - 1.5)
wire('25a', [(SL, C59B), (SL + 3, Y25A), (X25A, Y25A), (X25A, Y25BOT), (362, Y25BOT), (362, yL['27']), (W, yL['27'])], 250, Y25BOT - 1.5)
DOTS += [(W, yR['28']), (W, yL['27'])]

# ---- brake lights and reversing lights ------------------------------------------------------------------------------
XB, X98, X28F = 338, 350, 344               # 97's drop; the risers 98 and 28f to the right block
YRV = 184                                   # the reversing run
txt(221, 168, 'Brake and reversing lights', 3.4, w='bold')
# reversing: 95f from inhibitor switch 90 (ignition sheet) through 60 inhibitor reversing, 58 reversing and 60
# reversing link (where a manual-gearbox car has its reversing light switch) to the left block's 32, and 98 on to the right's
t95 = mtag(221, YRV, ('95f VT 1.0 ← inhibitor switch 90:4,', 'closed in R (ignition sheet)'), size=2.2)
c1 = t95 + 22; c2 = c1 + 24; c3 = c2 + 24
wire('95f', [(t95, YRV), (c1 - 2, YRV)], t95 + 1.6, YRV - 1.5)
conn_h(c1, YRV, ('60 inhibitor', 'reversing'))
wire('95', [(c1 + 2, YRV), (c2 - 2, YRV)], c1 + 4, YRV - 1.5)
conn_h(c2, YRV, ('58 reversing',))
wire('96', [(c2 + 2, YRV), (c3 - 2, YRV)], c2 + 4, YRV - 1.5)
conn_h(c3, YRV, ('60 reversing', 'link'))
wire('97', [(c3 + 2, YRV), (XB, YRV), (XB, yL['32']), (W, yL['32'])], XB - 1.45, yL['32'] - 3, rot=-90)
wire('98', [(W, yL['32']), (W - 4, yL['32'] - 4), (X98, yL['32'] - 4), (X98, yR['32']), (W, yR['32'])], X98 + 3.1, 186, rot=-90)
DOTS += [(c1 - 2, YRV), (c1 + 2, YRV), (c2 - 2, YRV), (c2 + 2, YRV), (c3 - 2, YRV), (c3 + 2, YRV),
         (W, yL['32']), (W, yR['32'])]

# stop: 28 RD from fuse 5 through stop light contact 29 (closed by the pedal) and 60 stop lights to the left block's
# 30 (28e), and 28f on to the right block's 30
YST = yL['30']
t28 = mtag(221, YST, ('28 RD 1.0 ← fuse 5 (power sheet)',), size=2.2)
CX29 = t28 + 25                             # stop light contact 29: a circle with two contacts, as printed
A(f'<circle cx="{CX29}" cy="{YST}" r="5" fill="#fff" stroke="#111" stroke-width=".6"/>')
contact(CX29 - 2.4, YST); contact(CX29 + 2.4, YST)
inner([(CX29 - 5, YST), (CX29 - 3.2, YST)]); inner([(CX29 + 3.2, YST), (CX29 + 5, YST)])
blade(CX29 - 1.8, YST - .45, CX29 + 2.6, YST - 2.3)           # open at rest, as printed
name(round(CX29 - tw('29 Stop light contact', 2.4) / 2, 2), YST - 7.4, '29', 'Stop light contact', size=2.4)
wire('28', [(t28, YST), (CX29 - 5, YST)], t28 + 1.6, YST - 1.5)
c4 = CX29 + 27
wire('28g', [(CX29 + 5, YST), (c4 - 2, YST)], CX29 + 6.5, YST - 1.5)
conn_h(c4, YST, ('60 stop lights',), below=True)
wire('28e', [(c4 + 2, YST), (W, YST)], c4 + 5, YST - 1.5)
wire('28f', [(W, YST), (W - 4, YST - 4), (X28F, YST - 4), (X28F, yR['30']), (W, yR['30'])], X28F - 1.45, 130, rot=-90)
DOTS += [(CX29 - 5, YST), (CX29 + 5, YST), (c4 - 2, YST), (c4 + 2, YST), (W, YST), (W, yR['30'])]

for p in DOTS: dot(*p)

# ---- legend and notes ---------------------------------------------------------------------------------------------------
def wrap(text, width, size):
    """Split text into lines no wider than width (mm) at size."""
    out, line = [], ''
    for word in text.split(' '):
        t = (line + ' ' + word).strip()
        if line and tw(t, size) > width: out.append(line); line = word
        else: line = t
    return out + [line]


lx, ly, lw = 66, 184, 140                   # the empty lower left: below 23a, left of 25a's lane
NS = 2.25                                   # note text size
notes = ['Flasher 23 is fed on X from fuse 8 (21 RD/VT; always-live bar 5–8). Its L output, 22 GN, passes through hazard switch 25’s + terminal '
         'to indicator switch 24’s 54 (22e GN); the stalk sends it on R (24b) or L (24a), through 59 indicators, to that '
         'side’s front and rear indicators.',
         'The flasher’s P terminal lights the indicator repeater in the instrument.',
         'Switches are drawn at rest: 24 centre-off; 25 off, its bar touching none of its contacts. Pressed, 25’s bar '
         'probably joins the lamp contact, +, R and L (the dotted marks), so the flasher feeds both sides and repeater lamp 26.',
         'Repeater lamp 26 sits in hazard switch 25. Its earth side also takes 105 SV, the clock’s earth; the clock has '
         'been removed (rev counter instead, check D1) and 105 is unused, so it is not drawn.',
         'Stop light contact 29 closes when the brake pedal is pressed.',
         'Reversing lights: switched by the gear selector’s inhibitor switch 90, closed in R (ignition sheet); on a '
         'manual-gearbox car a reversing light switch takes the place of 60 reversing link.',
         'Lamp housings and rear lamp blocks: no earth lead is drawn; each probably earths through its housing. The '
         'parking, tail and number-plate bulbs are wired on the lighting sheet (open terminals here). In each rear block, '
         'tail light 14 and number-plate light 15 are joined inside the block; the link hops over the stop and reversing '
         'leads without joining them.']
lines = []
for n in notes: lines += wrap(n, lw - 8, NS)


def s_dashed(x, y):
    A(f'<path d="M{x},{y} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 11, y + 1, 'not traced yet', 2.4)


def s_stub(x, y):
    A(f'<path d="M{x},{y} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{y}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    txt(x + 11, y + 1, 'ends on diagram', 2.4)


def s_tick(x, y):
    tick(x + 3, y + .3); txt(x + 11, y + 1, 'checked on the car', 2.4)


# samples beside 'traced' (two fit on its row), then on the probable row (after its sample when it draws)
opt = [f for flag, f in ((DASHED, s_dashed), (STUB, s_stub), (TICKED, s_tick)) if flag[0]]
slots = [(lx + 52, ly + 22), (lx + 94, ly + 22)] + ([(lx + 52, ly + 28), (lx + 94, ly + 28)] if PROBABLE[0] else
                                                    [(lx + 4, ly + 28), (lx + 52, ly + 28)])
y = ly + 23 + (6 if PROBABLE[0] or len(opt) > 2 else 0)
lh = round(y - ly + 4.5 + len(lines) * 3.2 + 1.5, 1)
box(lx, ly, lw, lh, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, yy = lx + 4 + (i % 4) * 26, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{yy - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{yy - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, yy, f'{k} {n}', 2.5)
size_legend(lx + 4, ly + 17)
A(f'<path d="M{lx + 4},{ly + 22} h9" stroke="#222" stroke-width="1.7"/>'); txt(lx + 15, ly + 23, 'traced (cable no. read)', 2.4)
for f, (x, yy) in zip(opt, slots): f(x, yy)
probable_legend(lx + 4, ly + 28)
for j, n in enumerate(lines): txt(lx + 4, round(y + 4.5 + j * 3.2, 2), n, NS, fill='#333')
save('signals.svg')

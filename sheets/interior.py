#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo interior lights, seat heating and seat belt warning sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Interior lights, seat heating, seat belt warning')
def meander(x, y, w=10, up=1.2, down=1.8):
    """Heating element as the manual prints it: three square humps between two open circles; x, y is its left lead end."""
    s = w / 6
    pts = [(x, y)] + [(round(x + (k + j) * s, 2), round(y + (-up if k % 2 == 0 else down), 2)) for k in range(6) for j in (0, 1)] + [(x + w, y)]
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".4" stroke-linejoin="round"/>')
def lab(c):
    """A cable's label as wire() prints it: number, colour, mm² from wires.csv."""
    r = WIRES[c]; return f"{c.split('#')[0]} {r['colour']} {r['mm2']}"
def lead(pts):
    """A lead the manual prints without a cable number (the belt contacts', the earths of 50, 54 and 56): plain black."""
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')
def jdot(x, y):
    """Junction inside a part: smaller than a terminal dot (as on the instruments and signals sheets)."""
    A(f'<circle cx="{x}" cy="{y}" r=".6" fill="#111"/>')
# Helvetica advance widths (1/1000 em), to centre or right-align a name with a bold number: cairosvg misplaces a bold
# tspan in text that isn't start-anchored, so name() works out the start itself
_W = dict(zip('abcdefghijklmnopqrstuvwxyz', (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
                                             556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500)))
_W.update(dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
                                                 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611))))
_W.update({' ': 278, ',': 278, '.': 278, '’': 222, '(': 333, ')': 333, '/': 278, '-': 333, ':': 278, ';': 278})
def tw(s, size, bold=False):
    return sum(556 if ch.isdigit() else _W.get(ch, 556) * (1.06 if bold else 1) for ch in s) / 1000 * size
def name(x, y, n, s, anchor='start', size=2.6):
    """Component number (bold) and name, as the other sheets print them."""
    w = tw(n, size, True) + tw(' ' + s, size)
    x0 = x if anchor == 'start' else x - w / 2 if anchor == 'middle' else x - w
    txt(round(x0, 2), y, f'<tspan font-weight="bold">{n}</tspan> {s}', size)
def note(x, y, s, anchor='start'):
    txt(x, y, s, 2.2, anchor, fill='#555')

# Framed connectors, as the radio sheet draws tail lamp connector 58: the frame is filled first, the wires run to the
# pin dots just inside it, then the frame's outline, the pins and their dots go on top. Pins run across the frame
# unless upright.
BLOCKS = []
def block(x0, y0, w, h, rows=(), upright=None, grey=()):
    """Frame at (x0, y0), w × h; rows: y of each pin across it (dots 2.5 in from each side); upright: (x, top y, bottom
    y) of a single upright pin; grey: (from, to) links inside the frame where the manual hides a join (probably).
    Returns the x of the left and right dots."""
    A(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#ddd"/>')
    BLOCKS.append((x0, y0, w, h, rows, upright, grey))
    return x0 + 2.5, x0 + w - 2.5
def blocks_on_top():
    for x0, y0, w, h, rows, upright, grey in BLOCKS:
        A(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#111" stroke-width=".5"/>')
        for a, b in grey: inner([a, b], grey=True)
        for y in rows: inner([(x0 + 2.5, y), (x0 + w - 2.5, y)]); dot(x0 + 2.5, y); dot(x0 + w - 2.5, y)
        if upright: x, t, b = upright; inner([(x, t), (x, b)]); dot(x, t); dot(x, b)
def switch_h(x, y, w=14):
    """Switch in a box, leads left and right on y: blade from the left contact rising toward the top wall (open)."""
    box(x, y - 4, w, 8); dot(x, y); dot(x + w, y)
    inner([(x, y), (x + 1.8, y)]); contact(x + 2.6, y); contact(x + w - 2.6, y); inner([(x + w - 1.8, y), (x + w, y)])
    blade(x + 3.3, y - .4, x + w - 4.4, y - 3.4)


# ---- seat heating ------------------------------------------------------------------------------------------------
txt(18, 40, 'Seat heating', 3.4, w='bold')
# fuse 5 of fuse box 22, turned a quarter as on the radio sheet: the ignition-on bar runs down the left, its junction
# ring feeds the 8 A fuse, and bottom terminal 5 is the dot on the box edge
box(18, 52, 32, 20); txt(21, 57, f'<tspan font-weight="bold">F5</tspan> · {FUSES[5]["rating"]}', 2.6)
inner([(24, 59.5), (24, 69.5)]); contact(24, 62); txt(26, 69, 'ignition-on bar', 2.1, fill='#555')
fa, fb = fuse(30, 60.8, 10, 2.4); inner([(24.8, 62), fa]); inner([fb, (50, 62)]); dot(50, 62); tlabel(48.5, 60.6, '5', 'end')
# 140 runs fuse 5 → 58 (E12) pin 1 → 60 (A7) → 59 (A7) lower pin → 64. 214 BL (heated window switch 116) and 150 GL
# (seat belt warning) leave the fuse-side dots of 58 (E12) and 60 (A7) on short diagonals, as printed (IMG_4708, IMG_4698)
Y140 = 62
L58, R58 = block(96, Y140 - 3.5, 10, 7, rows=(Y140,)); note(101, Y140 - 5, '58 brake/reversing', 'middle')
L60, R60 = block(121, Y140 - 3.5, 10, 7, rows=(Y140,)); note(126, Y140 - 5, '60 seat feed', 'middle')
L59, R59 = block(146, Y140 - 3.5, 10, 7, rows=(Y140,)); note(151, Y140 - 5, '59 seat heater', 'middle')
wire('140', [(50, Y140), (L58, Y140)], 58, 60.5); wire('140', [(R58, Y140), (L60, Y140)], label=False); wire('140', [(R60, Y140), (L59, Y140)], label=False)
wire('214', [(L58, Y140), (L58 - 3, Y140 + 3), (L58 - 3, 82), (L58 - 5, 82)], label=False)
tag(L58 - 5, 82, '214 BL 0.75 → heated window switch 116 (climate sheet)', anchor='end')
X64 = 160
lead([(R59, Y140), (X64, Y140)])
# 64 as the manual prints it: lower element, thermostat (open), upper element, in series. The manual draws the two
# elements side by side into both rows of 59; here they run in a line from 140 (left) to 141 (right).
def seat_heater(x):
    X = lambda v: round(v + x - 196, 2)   # drawn at x 196 first; shifted as a whole
    box(x, 47.5, 55, 19)
    # thermostat housing: a heavy outline as printed, not conductor weight, so it doesn't read as a loop bypassing the
    # contacts; its walls' inner edges touch the contacts (top one hangs, bottom one sits) and the blade rests on the right wall
    A(f'<rect x="{X(217.5)}" y="50.9" width="11" height="12.2" rx=".6" fill="#fff" stroke="#111" stroke-width=".7"/>')
    inner([(X(196), 62), (X(198.7), 62)]); contact(X(199.5), 62); inner([(X(200.3), 62), (X(202.1), 62)]); meander(X(202.1), 62)
    inner([(X(212.1), 62), (X(213.9), 62)]); contact(X(214.7), 62); inner([(X(215.5), 62), (X(222.2), 62)]); contact(X(223), 62)
    inner([(X(223.8), 52), (X(230.2), 52)]); contact(X(231), 52); inner([(X(231.8), 52), (X(233.6), 52)]); meander(X(233.6), 52)
    inner([(X(243.6), 52), (X(245.4), 52)]); contact(X(246.2), 52); inner([(X(247), 52), (X(251), 52)]); contact(X(223), 52)
    bimetal(X(223.4), 52.57, X(227.85), 60)   # hangs from the top contact and rests on the right wall (a stop), clear of the bottom contact
    dot(x, 62); dot(X(251), 52)
    txt(X(223.5), 71.5, '64 Seat heating element with thermostat', 2.5, 'middle', w='bold')
    return X(251)
X64R = seat_heater(X64)
# 141 and 168 end in one earth symbol, as printed (scan p.407, IMG_4698): 141 from 59 (A7)'s upper pin slants into
# it, 168 rises from it to interior lighting switch 53. Here 141 comes down into the earth and 168 leaves its top.
XE, YE = X64R + 9, 84
wire('141', [(X64R, 52), (XE, 52), (XE, YE)], XE - 1.4, YE - 4, rot=-90); earth(XE, YE)
X168 = XE + 8

# ---- interior lights ---------------------------------------------------------------------------------------------
# As the 1979 book prints them (IMG_4700, scan p.407 A8-A11): fuse 9's 160 GL feeds the top node of ignition switch
# light 52; 161 GL runs on through dome light connector 57 (A10) pin 1 to the top node of dome light 50 and on as
# 162 SV to mirror light 51 (the + line, printed SV). Their other sides return on 164 BL (52, through 57 pin 2) and
# 165 SV (51) to 50's return node, and from there through the switch inside 50: left contact 167 SV → 57 pin 3 → 167a
# SV → 60 (A9) → 167 SV → switch 53; right contact to earth. 53 earths the door line itself (168 SV) and carries it on
# as 169 SV to door switch connector 58 (A9) pin 1, where 170 and 171 go to the door switches 54. Luggage light 55
# hangs off 57 pin 1 on 163 GL and earths through its switch 56. The earth leads of 50, 54 and 56 carry no number.
XI = X168 + 4
txt(XI, 40, 'Interior lights', 3.4, w='bold')
note(XI, 46, 'Fuse 9 feeds lamps 52, 50 and 51 side by side. They return through dome light 50’s switch: straight to earth, or to the door')
note(XI, 49.6, 'line, which switch 53 (closed) or an open door (door switches 54) earths. Luggage light 55 has its own switch, 56 (all: check I2).')
Y1, Y2, Y3 = 110, 122, 134            # + line, return line, door line
YL = (Y1 + Y2) / 2                    # lamp centres between the + and return lines
RL = 3.5
X53, X60, X52, X57, X50, X51 = XI, 272, 288, 306, 338, 384
W50 = 20                              # 50's housing width
# 53: left pivot on 168, blade rising to the top wall (open); the right contact goes out on 167 and, by a tick to the
# bottom wall, on 169 (IMG_4700: '169 SV 0.75' on a leader onto that riser)
switch_h(X53, Y3)
inner([(X53 + 11.4, Y3 + .8), (X53 + 11.4, Y3 + 4)]); dot(X53 + 11.4, Y3 + 4)
name(X53, Y3 - 6, '53', 'Interior lighting switch')
wire('168', [(XE, YE), (X168, YE), (X168, Y3), (X53, Y3)], X168 - 1.4, 124, rot=-90); dot(XE, YE)
# 60 (A9): one upright pin, both leads at its bottom end, the top end bare
block(X60 - 2.5, Y3 - 12, 5, 15, upright=(X60, Y3 - 9.5, Y3))
wire('167', [(X53 + 14, Y3), (X60, Y3)], X53 + 15, Y3 - 1.5)
note(X60, Y3 + 6.2, '60 interior switch', 'middle')
# 57 (A10): three pins; 163 GL leaves the top of the frame above the right pin column, its join hidden (grey)
L57, R57 = block(X57, Y1 - 4, 10, Y3 - Y1 + 8, rows=(Y1, Y2, Y3), grey=(((X57 + 7.5, Y1), (X57 + 7.5, Y1 - 4)),))
note(X57 + 5, Y3 + 9.2, '57 dome light', 'middle')
wire('167a', [(X60, Y3), (L57, Y3)], X60 + 3.5, Y3 - 1.5)
# 52: the + node on top (a dot), the lamp hanging from it, 164 from its foot
lamp(X52, YL, r=RL); lead([(X52, Y1), (X52, YL - RL)])
wire('164', [(X52, YL + RL), (X52, Y2), (L57, Y2)], label=False)
wire('161', [(X52, Y1), (L57, Y1)], label=False)
wire('160', [(X52 + 2, 64), (X52, 64), (X52, Y1)], label=False); dot(X52, Y1)
tag(X52 + 2, 64, f"{lab('160')} ← 126 BL from fuse 9, through tail lamp connector 58 (radio sheet)")
name(X52 - 5, YL + 1, '52', 'Ignition switch light', 'end')
# 50: pill-shaped housing. The + line passes through the lamp's top node; the return line through its neck, where the
# 1979 Turbo print only thickens the line (the 1979 GL and 1980 prints have a dot, and 164/165 have no other way to
# earth), so it gets a dot. The switch lever hangs from the return node between two open contacts, touching neither,
# as printed: left the door line, right earth.
XC = X50 + W50 / 2
A(f'<rect x="{X50}" y="{Y1 - 10}" width="{W50}" height="{Y3 - Y1 + 20}" rx="{W50 / 2}" fill="#fdfdfd" stroke="#111" stroke-width=".8"/>')
wire('161', [(R57, Y1), (X50, Y1)], X57 + 12, Y1 - 1.5)
wire('164', [(R57, Y2), (X50, Y2)], X57 + 12, Y2 - 1.5)
wire('167#lamp', [(R57, Y3), (X50, Y3)], X57 + 11.5, Y3 + 4)
inner([(X50, Y1), (X50 + W50, Y1)]); inner([(X50, Y2), (X50 + W50, Y2)])
lamp(XC, YL, r=RL); inner([(XC, Y1), (XC, YL - RL)]); inner([(XC, YL + RL), (XC, Y2)]); jdot(XC, Y1); jdot(XC, Y2)
blade(XC, Y2, XC, Y3 - 1)
inner([(X50, Y3), (X50 + 2.7, Y3)]); contact(X50 + 3.5, Y3); contact(X50 + W50 - 3.5, Y3); inner([(X50 + W50 - 2.7, Y3), (X50 + W50, Y3)])
for y_ in (Y1, Y2, Y3): dot(X50, y_); dot(X50 + W50, y_)   # terminals on the housing wall, as on the other boxed parts
name(XC, Y3 + 15, '50', 'Dome light, door pillar', 'middle')
note(XC, Y3 + 18.4, 'switch: door / off (as drawn) / on, probably (check I2)', 'middle')
lead([(X50 + W50, Y3), (X50 + W50 + 8, Y3)]); earth(X50 + W50 + 8, Y3)
# 51: between the + line (162) and the return line (165)
wire('162', [(X50 + W50, Y1), (X51, Y1), (X51, YL - RL)], X50 + W50 + 1.8, Y1 - 1.5)
wire('165', [(X50 + W50, Y2), (X51, Y2), (X51, YL + RL)], X50 + W50 + 1.8, Y2 - 1.5)
lamp(X51, YL, r=RL); name(X51, Y2 + 6.5, '51', 'Dome light, rear-view mirror', 'middle')
# 55 and its switch 56 (drawn open), off 57 pin 1 on 163
Y55, X55, X56 = 84, 336, 360
wire('163', [(R57, Y1 - 4), (R57, Y55), (X55 - RL, Y55)], R57 + 3.4, Y1 - 6, rot=-90)
lamp(X55, Y55, r=RL); name(X55 + 2, Y55 - 6, '55', 'Luggage compartment light', 'end')
wire('166', [(X55 + RL, Y55), (X56, Y55)], X55 + 4.5, Y55 - 1.5)
switch_h(X56, Y55, 16); lead([(X56 + 16, Y55), (X56 + 22, Y55)]); earth(X56 + 22, Y55)
name(X56 + 8, Y55 - 6, '56', 'Luggage compartment light switch', 'middle')
for j, s_ in enumerate(('Combi Coupé (check R7): lamp 55 on', 'the right of the luggage area, 10 W;',
                        'switch 56 a plunger at the tailgate', 'striker; 166 may be black')):
    note(X50 + W50 + 3, 93.6 + j * 3.4, s_)
# door switch connector 58 (A9): pin 1 takes 169 from 53 and gives 171 and 170 (170 drawn into the frame's top-right
# corner, join hidden: grey); pin 2 is the seat belt warning's 156 BR. Pin 3 is empty; 261, 211 and 123 use 4-6
# (the other sheets and the notes box call them rows).
R1, R2 = 164, 171
X58 = 270
L58d, R58d = block(X58, R1 - 3.5, 10, R2 - R1 + 7, rows=(R1, R2), grey=(((X58 + 7.5, R1), (X58 + 10, R1 - 3.5)),))
note(X58 + 5, R2 + 7.2, '58 door switches', 'middle')
wire('169', [(X53 + 11.4, Y3 + 4), (X53 + 11.4, R1), (L58d, R1)], X53 + 12.9, R1 - 1.5)
# 54: upright, the blade hanging from the top contact into the right inner wall, clear of the bottom one (open)
def door_switch(x, y):
    box(x - 5, y, 10, 16); dot(x, y); inner([(x, y), (x, y + 1.8)]); contact(x, y + 2.6)
    blade(x + .3, y + 3.3, x + 4.3, y + 11.5); contact(x, y + 13.4); inner([(x, y + 14.2), (x, y + 16)]); dot(x, y + 16)
    earth(x, y + 16)
X54a, X54b, Y54 = 374, 396, 176
wire('171', [(R58d, R1), (X54a, R1), (X54a, Y54)], X58 + 14, R1 - 1.5)
wire('170', [(X58 + 10, R1 - 3.5), (X58 + 12, R1 - 5.5), (X54b, R1 - 5.5), (X54b, Y54)], X58 + 14, R1 - 7)
door_switch(X54a, Y54); door_switch(X54b, Y54)
name((X54a + X54b) / 2, Y54 + 27, '54', 'Door switches', 'middle')
note((X54a + X54b) / 2, Y54 + 30.4, 'probably closed with a door open', 'middle')

# ---- seat belt warning ---------------------------------------------------------------------------------------------
# As printed (IMG_4698, scan p.407; the contact leads carry no numbers): 150 GL from 60 (A7)'s fuse-side dot reaches
# the top pin of seat belt contact connector 59 (A9); belt contact 70 joins it to the bottom pin directly, belt contact
# 71 only through seat contact 69. The bottom pin's 156 BR passes door switch connector 58 pin 2 and seat belt lamp
# connector 59 (D12) to lamp 72 (151 BR); the lamp's other lead (printed 150 GL) meets 157 SV to earth at 59 (D12).
# 70 and 71 are drawn closed (unbuckled), 69 open (seat empty), as printed. The print looks LHD (its seat contact sits
# with 71, the legend's R); on this car I3 found the driver's belt switching alone and the passenger's only with the
# seat contact, so the driver's is wired as 70 and the passenger's as 71.
txt(18, 118, 'Seat belt warning', 3.4, w='bold')
note(18, 124, 'With the ignition on, lamp 72 lights while the driver is unbuckled,')
note(18, 127.4, 'or while someone sits in the passenger’s seat unbuckled (check I3).')
X59b = 104
L59b, R59b = block(X59b, R1 - 3.5, 10, R2 - R1 + 7, rows=(R1, R2))
note(L59b + 2, R2 + 7.2, '59 belt contacts')
X150 = L60 - 3
wire('150', [(L60, Y140), (X150, Y140 + 3), (X150, R1), (R59b, R1)], X150 - 1.4, 150, rot=-90)
wire('156', [(R59b, R2), (L58d, R2)], 160, R2 - 1.5)
# 70, next to the connector: a bar across its two leads (closed)
X70 = 84
box(X70, R1 - 4, 8, R2 - R1 + 8); dot(X70 + 8, R1); dot(X70 + 8, R2)
inner([(X70 + 8, R1), (X70 + 3.5, R1)]); inner([(X70 + 8, R2), (X70 + 3.5, R2)]); blade(X70 + 3.5, R1, X70 + 3.5, R2)
lead([(X70 + 8, R1), (L59b, R1)]); lead([(X70 + 8, R2), (L59b, R2)])
name(X70 + 2, R1 - 10.5, '70', 'Seat belt contact, driver’s', 'middle'); note(X70 + 2, R1 - 7.1, 'on its own (check I3)', 'middle')
# 71, further out: two contact circles bridged by a bar (closed); its top lead drops onto the connector's top-left
# dot from above, its bottom lead goes round 70 to seat contact 69, whose other side rises into the bottom-left dot
X71, Y71 = 40, 142
box(X71, Y71, 8, 14); dot(X71 + 8, Y71 + 3); dot(X71 + 8, Y71 + 11)
contact(X71 + 4, Y71 + 3); contact(X71 + 4, Y71 + 11); blade(X71 + 4, Y71 + 3.8, X71 + 4, Y71 + 10.2)
inner([(X71 + 4.8, Y71 + 3), (X71 + 8, Y71 + 3)]); inner([(X71 + 4.8, Y71 + 11), (X71 + 8, Y71 + 11)])
lead([(X71 + 8, Y71 + 3), (L59b, Y71 + 3), (L59b, R1)])
name(X71 - 22, Y71 - 6.5, '71', 'Seat belt contact, passenger’s'); note(X71 - 22, Y71 - 3.1, 'only with seat contact 69 (check I3)')
# 69: blade hinged on the right contact, dropping clear of the left one (open)
X69, Y69 = 60, R2 + 11
lead([(X71 + 8, Y71 + 11), (X71 + 11, Y71 + 11), (X71 + 11, Y69), (X69, Y69)])
box(X69, Y69 - 4, 14, 8); dot(X69, Y69); dot(X69 + 14, Y69)
inner([(X69, Y69), (X69 + 1.8, Y69)]); contact(X69 + 2.6, Y69); contact(X69 + 11.4, Y69); inner([(X69 + 12.2, Y69), (X69 + 14, Y69)])
blade(X69 + 10.7, Y69 + .4, X69 + 4.6, Y69 + 3)
lead([(X69 + 14, Y69), (L59b, Y69), (L59b, R2)])
name(X69 + 7, Y69 + 9, '69', 'Seat contact, passenger’s seat', 'middle'); note(X69 + 7, Y69 + 12.4, 'closes when sat on (check I3)', 'middle')
# seat belt lamp connector 59 (D12) and lamp 72, below the door switch connector
X59l, YL1, YL2 = 296, 214, 224
L59l, R59l = block(X59l, YL1 - 3.5, 10, YL2 - YL1 + 7, rows=(YL1, YL2))
note(X59l + 5, YL1 - 5, '59 belt lamp', 'middle')
wire('156', [(R58d, R2), (288, R2), (288, YL1), (L59l, YL1)], 286.6, 204, rot=-90)
X72 = 336
wire('151', [(R59l, YL1), (X72, YL1), (X72, (YL1 + YL2) / 2 - RL)], X59l + 11.5, YL1 - 1.5)
lamp(X72, (YL1 + YL2) / 2, r=RL); name(X72 + 5.5, (YL1 + YL2) / 2 + 1, '72', 'Seat belt warning lamp')
wire('150#lamp', [(X72, (YL1 + YL2) / 2 + RL), (X72, YL2), (R59l, YL2)], X59l + 11.5, YL2 + 4)
note(X59l + 11.5, YL2 + 7.6, 'the lamp’s own lead, printed 150 GL like the fuse 5')
note(X59l + 11.5, YL2 + 11, 'feed but not joined to it; earths on 157 SV (check I4)')
X157 = 274                            # corner left of 59's frame far enough for 157's label to sit on its own run
wire('157', [(L59l, YL2), (X157, YL2), (X157, YL2 + 4)], X157 + 2, YL2 - 1.5); earth(X157, YL2 + 4)
note(X157, YL2 + 13.5, 'earth point shared with 69, 129, 341 SV', 'middle')
blocks_on_top()

lx, ly = 18, 250
box(lx, ly, 389, 37, fill='#fff', sw=.5)
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
notes = ['Seat heating: fuse 5 (ignition-on bar) feeds 140 GL 1.0 through brake and reversing light connector 58, seat heating feed connector 60 and',
         'seat heater connector 59 to seat heating element 64: two elements in series with a thermostat between them, drawn open (probably its warm state: it closes when cold).',
         'Its return, 141 SV 1.0, shares seat heater connector 59 (141 SV on one pin, 140 GL on the other) but is drawn straight to its earth, which 168 SV from switch 53 shares.',
         'Fuse 5 also feeds the seat belt warning (150 GL), heated window switch 116 (214 BL; check D14; climate sheet) and the Turbo’s high-speed fuel boost',
         '(380 GL to speed transmitter, component 140; 380a GL to throttle switch 137; ignition sheet).',
         'Door switch connector 58, rows counted top to bottom: 169 and 171 on row 1 (170 probably too: its join is hidden in the frame), 156 on row 2; row 3 is empty; 261, 211 and 123 use rows 4 to 6 (other sheets).',
         'Thin black lines without a label: leads with no cable number. Not RHD-specific: circuits should match the car, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 5.6 + j * 4.6, n, 2.35, fill='#333')
save('interior.svg')

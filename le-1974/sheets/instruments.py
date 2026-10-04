#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE instruments, warning lamps and panel lighting sheet (A3 SVG)."""
import math
from common import *

header('Saab 99 LE, model 1974 — Instruments, warning lamps and panel lighting')

# ---- local helpers (copied from the Turbo's sheets; lib/wiring.py stays as it is) ------------------------------------
_W = dict(zip('abcdefghijklmnopqrstuvwxyz', (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
                                             556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500)))
_W.update(dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
                                                 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611))))
_W.update({' ': 278, ',': 278, '.': 278, '’': 222, '(': 333, ')': 333, '/': 278, '-': 333, ':': 278, ';': 278,
           '←': 1000, '→': 1000, '°': 400, '–': 556})
def tw(s, size, bold=False):
    """Rendered width of s in Helvetica at size (mm); arrows are Arial's (1 em)."""
    return sum(556 if ch.isdigit() else _W.get(ch, 556) * (1.06 if bold else 1) for ch in s) / 1000 * size
def name(x, y, n, s, anchor='start', size=2.6):
    """Component number (bold) and name; works out the start itself (cairosvg misplaces a bold tspan otherwise)."""
    w = tw(n, size, True) + tw(' ' + s, size)
    x0 = x if anchor == 'start' else x - w / 2 if anchor == 'middle' else x - w
    txt(round(x0, 2), y, f'<tspan font-weight="bold">{n}</tspan> {s}', size)
def note(x, y, s, anchor='start', size=2.2):
    txt(x, y, s, size, anchor, fill='#555')
def lab(c):
    """A cable's label as wire() prints it: number, colour, mm² from wires.csv."""
    r = WIRES[c]; return f"{c.split('#')[0]} {r['colour']} {r['mm2']}"
def ttag(x, y, s, size=2.4, anchor='start'):
    """One-line tag sized from the rendered text."""
    return tag(x, y, s, w=round(tw(s, size) + 3, 1), size=size, anchor=anchor)
def mtag(x, y, lines, size=2.4, anchor='start'):
    """Tag of several lines (tag() takes one), centred on y, lines 1.36 × size apart; width from the rendered text."""
    w = round(max(tw(s, size) for s in lines) + 3, 1)
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2); x0 = x if anchor == 'start' else x - w
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines): txt(x0 + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
    return x0 + w
def jdot(x, y):
    """Junction inside a part: smaller than a terminal dot."""
    A(f'<circle cx="{x}" cy="{y}" r=".6" fill="#111"/>')
def lead(pts):
    """A lead without a cable number (an earth stem): plain black."""
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')
def pins_h(x, rows, lab_, above=True):
    """In-line connector on horizontal wires: grey block 4 mm across the run, a pin with a dot on both faces at each
    row; its name centred above (or under) it."""
    t, b = min(rows) - 3, max(rows) + 3
    A(f'<rect x="{x - 2}" y="{t}" width="4" height="{b - t}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    for y in rows: inner([(x - 2, y), (x + 2, y)]); dot(x - 2, y); dot(x + 2, y)
    txt(x, t - 1.5 if above else b + 3.1, lab_, 2.2, 'middle', fill='#555')
def pin_v(x, y0, y1):
    """In-line connector on a vertical wire: grey block 4 mm along the run (y0 to y1), a pin with a dot on both faces."""
    A(f'<rect x="{x - 2.5}" y="{y0}" width="5" height="{y1 - y0}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    inner([(x, y0), (x, y1)]); dot(x, y0); dot(x, y1)
def gauge(x, y, r, t):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(x, y + 1.2, t, 3, 'middle')
def indicator(x, y, r):
    """Indicator repeater as the manual prints it: an X circle with its left and right quadrants filled black."""
    k = round(r * .7071, 2); a, b = (round(x - k, 2), round(y - k, 2)), (round(x + k, 2), round(y + k, 2))
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    d = f'M{x},{y} L{a[0]},{a[1]} A{r},{r} 0 0 0 {a[0]},{b[1]} Z M{x},{y} L{b[0]},{a[1]} A{r},{r} 0 0 1 {b[0]},{b[1]} Z'
    A(f'<path d="{d}" fill="#111"/><path d="M{a[0]},{a[1]} L{b[0]},{b[1]} M{a[0]},{b[1]} L{b[0]},{a[1]}" stroke="#111" stroke-width=".45"/>')
def on_circle(cx, cy, r, x):
    """Lowest point of the circle at x."""
    return round(cy + (r * r - (x - cx) ** 2) ** .5, 2)
def pt(cx, cy, r, deg):
    """Point on a circle at deg (0 right, 90 up)."""
    return round(cx + r * math.cos(math.radians(deg)), 2), round(cy - r * math.sin(math.radians(deg)), 2)
def sender(x, y, w, h, mark, curved=False):
    """Sender as the manual prints it (44, 45): a triangle on its base, apex up, its mark inside; 44's base bows down.
    (x, y) is the left base corner, where the earth lead leaves; returns the right base corner (signal lead)."""
    back = f' Q{x + w / 2},{round(y + h * .5, 2)} {x},{y}' if curved else ''
    A(f'<path d="M{x},{y} L{x + w / 2},{y - h} L{x + w},{y}{back} Z" fill="#fff" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')
    txt(x + w / 2, y - h * .25 + (.3 if curved else 0), mark, 2.2, 'middle')
    lead([(x, y), (x - 5, y), (x - 5, y + 1)]); earth(x - 5, y + 1)
    return x + w, y
def round_switch(x, y, r=6):
    """42 and 43 as printed: a circle with two contacts on its horizontal diameter, leads out through the wall to
    terminal dots on it; returns the left and right terminal points."""
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    inner([(x - r, y), (x - 3.8, y)]); contact(x - 3, y); contact(x + 3, y); inner([(x + 3.8, y), (x + r, y)])
    return (x - r, y), (x + r, y)


# ---- combination instrument 47 ----------------------------------------------------------------------------------------
# Inside as the 1974 RHD diagram prints it (p.327 x 2449-2717, y 1164-1357; the 1973 RHD p.325 is the same artwork):
# a + rail from 2 feeds the temperature gauge (C°, its lead from the gauge's bottom), the oil (11) and fuel warning (12)
# lamps, the brake lamp (on the 11 line, down to 5), the charge lamp and the fuel gauge (B, its left lead down to 2);
# an earth rail to 4 takes the C° gauge's right lead, the main-beam lamp (fed from 7), the indicator repeater (fed from
# 6; printed as a filled-quadrant bulb) and the B gauge's right lead. Dots where printed; the 11-5 line and the 2 line
# cross the earth rail without one. Not printed: a lead from 9 into the C° gauge (the gauge sits 6 px from the
# terminal) and one from 1 into the charge lamp (18 px of white between them); both drawn grey (probably). The charge
# and main-beam lamps touch on the print; drawn apart (no join: the main-beam lamp is fed from 7 alone).
X0, Y0, X1, Y1 = 106, 78, 232, 168           # box
box(X0, Y0, X1 - X0, Y1 - Y0)
name(X0, Y0 - 3.5, '47', 'Combination instrument', size=3)
T = {'9': (X0, 100), '1': (X0, 130), '11': (159, Y0), '12': (191, Y0), '3': (213, Y0),
     '7': (126, Y1), '5': (159, Y1), '6': (172, Y1), '2': (205, Y1), '4': (217, Y1)}
PR, ER, LR, GR_ = 121, 144, 3.5, 11          # + rail, earth rail, lamp radius, gauge radius
CX, BX, GY = 126, 213, 100                   # gauge centres
# temperature gauge C°: lead from 9 (grey), bottom to the + rail, right lead down to the earth rail
gauge(CX, GY, GR_, 'C°'); inner([T['9'], (CX - GR_, GY)], grey=True)
inner([(CX, GY + GR_), (CX, PR)]); jdot(CX, PR)
xc = 135; inner([(xc, on_circle(CX, GY, GR_, xc)), (xc, ER)]); jdot(xc, ER)
txt(138, 112.5, 'temperature', 2.2)
# fuel gauge B: 3 on top, left lead down to 2 (through the + rail), right lead down to 4 (through the earth rail)
gauge(BX, GY, GR_, 'B'); inner([T['3'], (BX, GY - GR_)])
inner([(205, on_circle(BX, GY, GR_, 205)), T['2']]); jdot(205, PR)
inner([(217, on_circle(BX, GY, GR_, 217)), T['4']]); jdot(217, ER)
txt(219.5, 124.5, 'fuel', 2.2); txt(219.5, 127.5, 'gauge', 2.2)
# oil (11) and fuel warning (12) lamps between their terminals and the + rail
for x, y, cap, anc, cx in ((159, GY, 'oil', 'start', 164), (191, GY, 'low fuel', 'end', 186)):
    inner([(x, Y0), (x, y - LR)]); lamp(x, y, r=LR); inner([(x, y + LR), (x, PR)]); jdot(x, PR); txt(cx, y + 1, cap, 2.2, anc)
# brake lamp on the 11 line: + rail to 5 (crossing the earth rail, no join)
inner([(159, PR), (159, 132 - LR)]); lamp(159, 132, r=LR); inner([(159, 132 + LR), T['5']]); txt(164, 133, 'brake', 2.2)
# charge lamp: + rail node above, its lead to 1 grey
inner([(CX, PR), (CX, 130 - LR)]); lamp(CX, 130, r=LR); inner([T['1'], (CX - LR, 130)], grey=True)
txt(111, 136.5, 'charge', 2.2)
# main-beam lamp: fed from 7 below, its right side on the earth rail
lamp(CX, ER, r=LR); inner([(CX, ER + LR), T['7']]); inner([(CX + LR, ER), (xc, ER)])
txt(111, ER + 1, 'main', 2.2); txt(111, ER + 4, 'beam', 2.2)
inner([(xc, ER), (217, ER)])                                           # the earth rail
inner([(CX, PR), (205, PR)])                                           # the + rail
# indicator repeater: earth rail above, 6 below
jdot(172, ER); inner([(172, ER), (172, 155 - LR)]); indicator(172, 155, LR); inner([(172, 155 + LR), T['6']])
txt(177, 156, 'indicator', 2.2)
for k, (x, y) in T.items():                  # terminal marks; the dots go on after the wires (end of sheet)
    if x == X0: tlabel(x + 1.6, y - 1.4, k)
    elif y == Y0: tlabel(x + 1.6, y + 3.2, k)
    else: tlabel(x + 1.6, y - 1.6, k)


# ---- senders and the charge lamp feed on the left ---------------------------------------------------------------------
# 44 and 45 as printed: triangles on their bases (44 marked P, its base bowed; 45 marked C°), each earthed from the
# left corner (an unnumbered lead to a hatched earth), the cable leaving the right corner.
name(18, 46.5, '44', 'Oil pressure contact')
sx, sy = sender(23, 59, 11, 9, 'P', curved=True)
wire('112', [(sx, sy), (159, sy), T['11']], 60, sy - 1.5)
name(18, 87.5, '45', 'Temperature transmitter')
sx, sy = sender(23, 100, 11, 9, 'C°')
wire('130', [(sx, sy), T['9']], 60, sy - 1.5)
# 61: the charge lamp's other side, to the alternator's D+ (power sheet)
s61 = f"{lab('61')} → alternator D+ (power sheet)"
e61 = ttag(14, 130, s61)
wire('61', [(e61, 130), T['1']], 76, 128.5)
for j, s in enumerate(['On this car a relay has been cut into 61 RD between', 'the alternator and this lamp (not drawn); what it',
                       'switches is still to be checked.']):
    note(14, 138 + j * 3, s)


# ---- fuel level transmitter 46, over the top -------------------------------------------------------------------------
# 30 BR from 12 runs above 29 GR from 3 (p.327: y917 and y940), both through fuel gauge connector 58 (rows 1 and 2) and
# fuel sender connector 59 (upper and lower pins) to 46: 30f into W (lower-left corner), 29f under the triangle into G
# (lower-right corner); 31 SV from the apex B to a hatched earth on the left.
YA, YB, XC58, XC59 = 43, 50, 262, 302
wire('30', [T['12'], (191, YA), (XC58 - 2, YA)], 222, YA - 1.5)
wire('29', [T['3'], (213, YB), (XC58 - 2, YB)], 222, YB - 1.5)
wire('30e', [(XC58 + 2, YA), (XC59 - 2, YA)], 270, YA - 1.5)
wire('29e', [(XC58 + 2, YB), (XC59 - 2, YB)], 270, YB - 1.5)
WX, GX, AX, AY = 344, 364, 354, 30            # 46: W and G base corners (y YA), apex
wire('30f', [(XC59 + 2, YA), (WX, YA)], 310, YA - 1.5)
wire('29f', [(XC59 + 2, YB), (GX, YB), (GX, YA)], 310, YB - 1.5)
wire('31', [(AX, AY), (326, AY)], 333, AY - 1.5); earth(326, AY)
A(f'<path d="M{WX},{YA} L{AX},{AY} L{GX},{YA} Z" fill="#fff" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')
txt(AX, AY + 6.5, 'B', 2.6, 'middle'); txt(WX + 3.4, YA - 1.2, 'W', 1.9, 'middle'); txt(GX - 3.4, YA - 1.2, 'G', 1.9, 'middle')
for p in ((WX, YA), (GX, YA), (AX, AY)): dot(*p)
pins_h(XC58, (YA, YB), '58 fuel gauge'); pins_h(XC59, (YA, YB), '59 fuel sender')
name(369, 36, '46', 'Fuel level'); txt(369, 39.4, 'transmitter', 2.6)
note(369, 44, 'B its earth, W the low-fuel'); note(369, 47, 'lamp’s lead, G the gauge’s')


# ---- below 47: main beam, brake warning, indicator repeater, supply -----------------------------------------------------
# 41 from 7 runs left just under the box (p.327 y1350-1373), above the brake warning contacts
s41 = (f"{lab('41')} ← lighting relay 8:F,", 'main beams (lighting sheet)')
e41 = mtag(14, 177, s41)
wire('41', [T['7'], (126, 177), (e41, 177)], 92, 175.5)
# 42 and 43 as printed: round switches earthed on the left; 42 a blade from the right contact (the 115 side), raised clear
# of the left one (open; p.327 x 2320-2380, y 1474-1500: the blade's right end meets the right contact, its left end sits
# about 10 px above the left contact); 43 a push contact whose bar lies on both contacts (closed: plunger out, handbrake
# on, probably). 114 from 5 drops into the top of
# brake warning connector 58 (one upright pin); 115 bends down into the same top face (its side is at the print's
# resolution limit: probably); 114e leaves the bottom face for 43.
X42, Y42, Y43, XP, PT, PB = 80, 190, 210, 159, 194, 198
(l42, r42) = round_switch(X42, Y42); blade(X42 + 2.4, Y42 - .4, X42 - 3.2, Y42 - 2.7)
(l43, r43) = round_switch(X43 := X42, Y43)
A(f'<path d="M{X43 - 4},{Y43 - 1.05} H{X43 + 4} M{X43},{Y43 - 1.05} V{Y43 - 4.2} M{X43 - 1.1},{Y43 - 4.2} H{X43 + 1.1}" '
  f'stroke="#111" stroke-width=".55" fill="none"/>')
for l in (l42, l43): lead([l, (l[0] - 5, l[1]), (l[0] - 5, l[1] + 1)]); earth(l[0] - 5, l[1] + 1)
name(X42 + 9, Y42 - 7.5, '42', 'Brake warning contact')
name(X43 + 9, Y43 + 9, '43', 'Handbrake contact')
wire('114', [T['5'], (XP, PT)], XP - 1.6, 186, rot=-90)
wire('115', [r42, (XP - 4, Y42), (XP, PT)], 100, Y42 - 1.5)
wire('114e', [(XP, PB), (XP, Y43), r43], 100, Y43 - 1.5)
pin_v(XP, PT, PB); note(XP - 3.5, 197, '58 brake warning', 'end')
for p in (r42, r43): dot(*p)
# 62 and 32 drop to their tags; 109 (the instrument's earth) runs right to the lighter
wire('62', [T['6'], (172, 224), (176, 224)], 170.4, 210, rot=-90)
ttag(176, 224, f"{lab('62')} ← flasher unit 23:P (signals sheet)")
wire('32', [T['2'], (205, 207), (209, 207)], 203.4, 196, rot=-90)
mtag(209, 207, (f"{lab('32')} ← fuse 9, via 58 wiper", 'switch pin 1 (wipers sheet)'))


# ---- cigarette lighter 48 and panel lighting -----------------------------------------------------------------------------
# As printed (p.327; book photo P8): the lighter is an ink-filled disc with a spiral; 109 SV into its upper-left (47's
# earth), one lower-left lead that 106 SV (to 19) and 108 SV (to the dash earth) share, 80 BL (feed) into its
# lower-right, 13 BL out of its right to the clock (not drawn: clock removed). Rheostat 16: a square box, a track
# curving down the left to the lower terminal, a wiper from the upper terminal to the track's top; 59 GN on the upper
# terminal, the lower terminal's lead splits outside the box into 102 (to 19) and 101 (to 17); drawn here with both
# leaving the terminal on the box wall (no unnumbered lead outside the box). Switch light 17 is the hub: its top node
# takes 101 and sends 110 and 133 to the two panel lights 18; its bottom node takes their earths 135 and 136 and sends
# 107 to the dash earth (a chevron into a stack of bars), which also takes 108 and 26 SV. Both nodes sit 3 mm off the
# lamp on short leads, so no wire runs along the lamp's outline.
LX, LY, LRR = 272, 96, 5
def lighter(x, y, r):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#111"/>')
    sp = [(round(x + .35 * t * math.cos(t), 2), round(y + .35 * t * math.sin(t), 2)) for t in [i * .25 for i in range(1, 47)]]
    A(f'<path d="{path(sp)}" fill="none" stroke="#fff" stroke-width=".3"/>')
TL, TR = (LX - 4, LY + 3), (LX + 4, LY + 3)                   # lower-left (earth side) and lower-right (feed) leads
wire('109', [T['4'], (217, 174), (250, 174), (250, LY - 3), (LX - 4, LY - 3)], 224, 172.5)
wire('80', [TR, (LX + 8, LY + 3), (LX + 8, 99), (304, 99)], 284, 97.5)
ttag(304, 99, f"{lab('80')} ← fuse 7, via 58 interior feed (interior sheet)")
X19, Y19 = 276, 122
wire('106', [TL, (LX - 4, Y19), (X19 - LR, Y19)], 266.4, 120, rot=-90)
D = (304, 232)                                                # dash earth: the chevron's tip
wire('108', [TL, (260, LY + 3), (260, D[1]), D], 258.4, 205, rot=-90)
lighter(LX, LY, LRR)
name(256, 84.5, '48', 'Cigarette lighter (with lamp)')
note(256, 88, 'its lamp’s own wiring is not shown', size=2)
# rheostat 16
BX0, BY0, BS = 284, 128, 14
PV, LO = (293, 134), (293, 139)                               # upper terminal (wiper pivot), lower terminal (track end)
W16 = (LO[0], BY0 + BS)                                       # lower terminal on the box wall: 101 and 102 both leave it
wire('59', [(BX0 + BS, PV[1]), (322, PV[1])], 300, PV[1] - 1.5)
ttag(322, PV[1], f"{lab('59')} ← fuse 3, via 58 tail lights (lighting sheet)")
X17, Y17 = 300, 184
N17, B17 = (X17, Y17 - LR - 3), (X17, Y17 + LR + 3)           # 17's feed node above the lamp, its earth node below
wire('102', [W16, (288, 147), (X19, 147), (X19, Y19 + LR)], X19 - 1.6, 145.5, rot=-90)
wire('101', [W16, (W16[0], N17[1]), N17], W16[0] - 1.6, 173, rot=-90)
XL18, YL18, YR18 = 335, 160, N17[1]                           # the two panel lights: upper (18 L) and lower (18 R)
wire('110', [N17, (X17, YL18), (XL18 - LR, YL18)], 306, YL18 - 1.5)
wire('133', [N17, (XL18 - LR, YR18)], 306, YR18 - 1.5)
wire('135', [(XL18 + LR, YL18), (352, YL18), (352, 198), (305, 198), B17], 322, 196.5)
wire('136', [(XL18 + LR, YR18), (345, YR18), (345, B17[1]), B17], 312, B17[1] - 1.5)
wire('107', [B17, (X17, D[1] - 8), D], X17 - 1.6, 222, rot=-90)
wire('26', [D, (D[0] - 7, D[1] + 7), (D[0] - 10, D[1] + 7)], label=False)
ttag(D[0] - 10, D[1] + 7, f"{lab('26')} ← hazard repeater 26 (signals sheet)", anchor='end')
# the rheostat drawn over its wire ends
box(BX0, BY0, BS, BS, fill='#fff')
arc = [pt(PV[0], PV[1], 5, a) for a in range(95, 271, 5)]
A(f'<path d="{path(arc)}" fill="none" stroke="#111" stroke-width=".55"/>')
blade(PV[0] - .5, PV[1] - .45, *pt(PV[0], PV[1], 5.3, 140))
inner([(PV[0] + .8, PV[1]), (BX0 + BS, PV[1])]); contact(*PV)
inner([(LO[0], LO[1] + .8), W16]); contact(*LO)
name(BX0, BY0 - 2.5, '16', 'Rheostat switch, panel illumination')
# lamps
lamp(X19, Y19, r=LR); name(X19 + 5, 116.5, '19', 'Glove compartment and heater control light')
lamp(X17, Y17, r=LR); name(X17 - 5.5, Y17 + 1, '17', 'Switch light', anchor='end')
lead([N17, (X17, Y17 - LR)]); lead([(X17, Y17 + LR), B17])    # 17's own leads to its feed and earth nodes
for y in (YL18, YR18): lamp(XL18, y, r=LR); txt(XL18, y - 5, '18', 2.6, 'middle', w='bold')
name(357, 171, '18', 'Instrument panel'); txt(357, 174.4, 'lights (two)', 2.6)
# dash earth: a chevron tip into a stack of bars
A(f'<path d="M{D[0] + .4},{D[1] - 3.2} v6.4 M{D[0] + 1.6},{D[1] - 2.5} v5 M{D[0] + 2.8},{D[1] - 1.8} v3.6 M{D[0] + 4},{D[1] - 1.1} v2.2" '
  f'stroke="#111" stroke-width=".6" fill="none"/>')
note(D[0] + 6, D[1] + 1, 'dash earth')
for p in (TL, TR, (LX - 4, LY - 3), (BX0 + BS, PV[1]), W16, N17, B17, D, (X19 - LR, Y19), (X19, Y19 + LR),
          (XL18 - LR, YL18), (XL18 + LR, YL18), (XL18 - LR, YR18), (XL18 + LR, YR18)):
    dot(*p)
# the clock's place
for j, s in enumerate(['Clock removed: an aftermarket rev counter sits in its place, wired in series',
                       'with the coil’s feed at the ballast resistor (ignition sheet), with no feed or',
                       'earth of its own. The clock’s feed 13 BL 1.0 (from the lighter, live at all',
                       'times) and its earth 105 SV 0.75 are unused on the car and not drawn (check D1).']):
    note(312, 79 + j * 3, s)

for p in T.values(): dot(*p)                  # 47's terminal dots, over their wires


# ---- legend and notes -----------------------------------------------------------------------------------------------------
lx, ly = 14, 250
box(lx, ly, 392, 36, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 4
size_legend(x, ly + 18)
y = ly + 24
A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x + 48},{y - 1} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 59, y, 'not traced yet', 2.4)
if STUB[0]:
    sx = x + (48 if not DASHED[0] else 0); sy = y + (0 if not DASHED[0] else 5)
    A(f'<path d="M{sx},{sy - 1} h7" stroke="#222" stroke-width=".8"/><circle cx="{sx + 8.3}" cy="{sy - 1}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    txt(sx + 11, sy, 'ends on diagram', 2.4)
if TICKED[0]: tick(x + 48, y + 4.3); txt(x + 52, y + 5, 'checked on the car', 2.4)
probable_legend(x, y + 5)
notes = ['Inside 47 (its own terminal numbers): a + rail from 2 feeds both gauges and the oil (11), fuel warning (12), brake (5) and charge (1) lamps; '
         'an earth rail to 4 takes the gauges’ other leads',
         'and the main-beam (7) and indicator (6) lamps. The leads from 9 into the temperature gauge and from 1 into the charge lamp are grey: probably.',
         'Supply: 32 RD/VT from fuse 9, shared with the wiper feed at 58 wiper switch, pin 1. '
         'Instrument earth (47:4) goes through the lighter body (109 SV) and on by 108 SV to the dash earth.',
         'Brake lamp (47:5): brake warning contact 42 and handbrake contact 43 are in parallel on it, either earths it; '
         '115 GL probably joins 114 VT on the instrument side of 58 brake warning.',
         'Contacts as drawn: brake warning contact 42 open; handbrake contact 43 closed (plunger out: handbrake on, probably).',
         'Panel lighting (lit with the tail lights from fuse 3, dimmed by rheostat 16): 101 GN feeds switch light 17 and, by 110 and 133 GN, '
         'the two panel lights 18;',
         '102 GN feeds glove compartment light 19. The panel lights earth at switch light 17’s earth side and on by 107 SV; light 19 earths '
         'by 106 SV through the lighter.',
         'Choke warning lamp and choke contact: probably not fitted on this injection car (injection cars have a spare switch where the '
         'choke control would be); their feed 146 BR would leave pin 1 of 58 wiper switch (wipers sheet).']
for j, n in enumerate(notes): txt(lx + 108, ly + 5.4 + j * 3.95, n, 2.35, fill='#333')
save('instruments.svg')

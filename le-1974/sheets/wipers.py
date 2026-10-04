#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE wipers and washers sheet (A3 SVG)."""
from common import *
import math

header('Saab 99 LE, model 1974 — Wipers and washers')


def name(x, y, n, s, size=2.7, anchor='start'):
    """Part number (bold) then its name, as the Turbo's sheets print them."""
    txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', size, anchor)


def jdot(x, y, r=.55):
    """Small junction dot inside a part; r .75 where a lead meets the housing wall, so it shows on the wall."""
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#111"/>')


def glabel(x, y, t, anchor='start'):
    """Probable name inside a part: tlabel size, probable grey (the legend's grey sample then shows)."""
    PROBABLE[0] = True
    txt(x, y, t, 1.8, anchor, fill='#888')


def mtag(x, y, lines, size=2.4, anchor='start'):
    """Destination tag of several lines (tag() takes one): left edge x (right edge when anchor='end'), centred on y,
    lines 1.36 x size apart; text start-anchored (it carries arrows)."""
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2); w = round(max(len(t) for t in lines) * size * .46 + 4, 1)
    x0 = x if anchor == 'start' else round(x - w, 2)
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, t in enumerate(lines): txt(round(x0 + 1.5, 2), round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), t, size)
    return x0, x0 + w


def earth_up(x, y):
    """Earth symbol standing on top of a part (the book prints 61's earth mark on its top wall): stem up from (x, y)."""
    A(f'<path d="M{x},{y} v-3 M{x - 3},{y - 3} h6 M{x - 2},{y - 4.3} h4 M{x - 1},{y - 5.6} h2" stroke="#111" stroke-width=".5" fill="none"/>')


PLINE = 'stroke="#999" stroke-width=".3" stroke-dasharray=".8 .6"'   # switch position line: as mlink(), the Turbo's style


def pline(a, b):
    A(f'<path d="M{a[0]:.2f},{a[1]:.2f} L{b[0]:.2f},{b[1]:.2f}" fill="none" {PLINE}/>')


# ---- rows: 58 wiper switch's six pins (our count, top to bottom), which the motor's and the switch's terminals share
P = 16
R = {k: 72 + P * (k - 1) for k in range(1, 7)}          # pin 1 .. pin 6: 72, 88, 104, 120, 136, 152
X58 = 178                                              # 58 wiper switch: block 176-180
XL, XR = X58 - 2, X58 + 2

# ================= 62 wiper motor (left) ===========================================================================
# As the 1974 RHD diagram prints it (cache p327 crop 2050-2500 x 2250-2720; internals-facts 62): five terminals on the
# right wall, top to bottom 3, 5, 4, 1, 2 (numbers printed left of the wall; the Turbo's order is 3, 5, 4, 2, 1).
# Inside: M with three brushes: upper right to 3 (16 GN, fast), right to 5 (15 RD, slow), left to the housing's left
# wall (earth); a bar from the housing's top-left corner to M (probably the drive). The park change-over: 2's lead runs
# left along the bottom and up to the pivot; the blade rests on 1's contact (closed), 4's contact open above its tip.
# Housing earth: 175 SV from a dot on the bottom wall. 2 is looped outside the box onto 5's line (15 RD).
MX0, MX1, MY0, MY1 = 36, 104, R[2] - 13, R[6] + 9
box(MX0, MY0, MX1 - MX0, MY1 - MY0)
name(MX0, MY0 - 3, '62', 'Two-speed wiper motor')
MC, MR = (64, R[3]), 11                              # M on 5's row, so the slow brush's lead runs straight
A(f'<circle cx="{MC[0]}" cy="{MC[1]}" r="{MR}" fill="#fff" stroke="#111" stroke-width=".7"/>')
txt(MC[0], MC[1] + 1.2, 'M', 3, 'middle', w='bold')


def brush(x0, y0, a, L=2.6, w=1.5):
    """Motor brush: a small rectangle standing on M's rim at (x0, y0), pointing out at a degrees (0 right, 90 up).
    Returns its outer end, where the lead joins."""
    A(f'<rect x="0" y="{-w / 2}" width="{L}" height="{w}" fill="#fff" stroke="#111" stroke-width=".4" '
      f'transform="translate({x0:.2f} {y0:.2f}) rotate({-a})"/>')
    return round(x0 + L * math.cos(math.radians(a)), 2), round(y0 - L * math.sin(math.radians(a)), 2)


def rim(a):
    return MC[0] + MR * math.cos(math.radians(a)), MC[1] - MR * math.sin(math.radians(a))


b3 = brush(*rim(45), 45)                               # fast: upper right, as printed
b5 = brush(*rim(0), 0)                                 # slow: right
be = brush(*rim(180), 180)                             # earth: left, to the housing wall
k3 = R[3] - R[2] - (MC[1] - b3[1])                     # the 3 lead carries on out at 45 degrees to 3's row
inner([b3, (b3[0] + k3, R[2]), (MX1, R[2])])
inner([b5, (MX1, R[3])])
inner([be, (MX0, MC[1])]); jdot(MX0, MC[1], .75)            # earth brush onto the housing
# drive: a round-ended bar from the housing's top-left corner to M's rim, then a thin line into M's centre
c1 = rim(135)
A(f'<path d="M{MX0 + 1.4},{MY0 + 1.4} L{c1[0]:.2f},{c1[1]:.2f}" stroke="#111" stroke-width="1.5" stroke-linecap="round"/>'
  f'<path d="M{MX0 + 1.4},{MY0 + 1.4} L{c1[0]:.2f},{c1[1]:.2f}" stroke="#fff" stroke-width=".6" stroke-linecap="round"/>')
inner([c1, (MC[0] - 3.2, MC[1] - 3.2)])                # stops clear of the 'M'
# park change-over: common 2 on the pivot, resting on 1 (closed), 4 open above the blade's tip
C4, C1, PV = (MX1 - 14, R[4]), (MX1 - 14, R[5]), (MX1 - 22, round((R[4] + R[5]) / 2, 2))
inner([(MX1, R[4]), (C4[0] + .8, R[4])]); inner([(MX1, R[5]), (C1[0] + .8, R[5])])
inner([(MX1, R[6]), (PV[0], R[6]), (PV[0], PV[1] + .8)])
for p in (C4, C1, PV): contact(*p)
ux, uy = C1[0] - PV[0], C1[1] - PV[1]; L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
blade(PV[0] + .7 * ux, PV[1] + .7 * uy, C1[0] - .75 * ux, C1[1] - .75 * uy)
for t, k in (('3', 2), ('5', 3), ('4', 4), ('1', 5), ('2', 6)): tlabel(MX1 - 1.4, R[k] - 1.3, t, 'end')
X175 = 70                                              # the housing earth, on the bottom wall

# ---- wires: motor to 58 wiper switch, pins 2-5 ----------------------------------------------------------------------
XLAB = 120                                             # labels right of 2's loop
wire('16', [(MX1, R[2]), (XL, R[2])], XLAB, R[2] - 1.6)
wire('15', [(MX1, R[3]), (XL, R[3])], XLAB, R[3] - 1.6)
wire('17', [(MX1, R[4]), (XL, R[4])], XLAB, R[4] - 1.6)
wire('18', [(MX1, R[5]), (XL, R[5])], XLAB, R[5] - 1.6)
# 2 looped onto 5's line just outside the motor (unnumbered: a plain lead); it crosses 17 and 18 as printed
XLOOP = MX1 + 6
A(f'<path d="M{MX1},{R[6]} H{XLOOP} V{R[3]}" fill="none" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')
YE = MY1 + 20                                          # 175's earth
wire('175', [(X175, MY1), (X175, YE)], X175 - 2.1, YE - 1.5, rot=-90); earth(X175, YE)
# 175 shares its earth point with the heater fan motor's 138 SV 2.5; the climate sheet's note names this one
txt(X175 + 6, YE + 2.4, 'the same earth point as the heater fan motor’s', 2.2, fill='#555')
txt(X175 + 6, YE + 5.6, '138 SV (climate sheet)', 2.2, fill='#555')

# ================= 63 washer motor (bottom left) ====================================================================
# As printed: a pump circle with a smaller inner circle and an outlet tab at its upper left; 89 GL in at the top,
# 88 SV out of the bottom; no terminal marks. Fed from fuse 9, earthed through the wiper switch (88 -> pin 6 -> 88e).
WC, WR = (46, YE + 20), 6.5
_, x1 = mtag(14, YE, ('89 GL 0.75 ← fuse 9', '(power sheet)'))
wire('89', [(x1, YE), (WC[0], YE), (WC[0], WC[1] - WR)], label=False)
Y88 = WC[1] + 18
wire('88', [(WC[0], WC[1] + WR), (WC[0], Y88), (150, Y88), (150, R[6]), (XL, R[6])], 92, Y88 - 1.6)
A(f'<rect x="{WC[0] - WR - 5}" y="{WC[1] - .85 * WR:.2f}" width="{WR + 4:.2f}" height="{.5 * WR:.2f}" fill="#fff" stroke="#111" stroke-width=".6"/>')   # outlet, upper left
A(f'<circle cx="{WC[0]}" cy="{WC[1]}" r="{WR}" fill="#fff" stroke="#111" stroke-width=".7"/>'
  f'<circle cx="{WC[0]}" cy="{WC[1]}" r="2.6" fill="#fff" stroke="#111" stroke-width=".5"/>')
name(WC[0] + WR + 3, WC[1] + 1, '63', 'Washer motor')

# ================= 58 wiper switch connector, and pin 1's feed ======================================================
# Six pins (book photo P4): 1 14 BR (+ 32 RD/VT, + 146 BR) | 14e; 2 16 | 16e; 3 15 | 15e; 4 17 | 17e; 5 18 | 18e;
# 6 88 | 88e. 14 comes from fuse 9 (power sheet); 32 leaves the same dot for the instrument's supply (instruments sheet).
_, x1 = mtag(122, R[1], ('14 BR 1.0 ← fuse 9 (power sheet)',))
wire('14', [(x1, R[1]), (XL, R[1])], label=False)     # the tag carries its label (the run is short)
X32, Y32 = 171, R[1] - 20
wire('32', [(XL, R[1]), (X32, R[1] - 5), (X32, Y32), (X32 - 3, Y32)], label=False)
mtag(X32 - 3, Y32, ('32 RD/VT 0.75 → combination instrument 47:2,', 'its supply (instruments sheet)'), size=2.2, anchor='end')
txt(X32 + 3, R[1] - 13.5, 'choke warning lamp’s feed 146 BR:', 2.0, fill='#888')   # a note, not a caption: it starts with the part
txt(X32 + 3, R[1] - 10.7, 'probably not fitted (instruments sheet)', 2.0, fill='#888')

# ================= 61 wiper switch (right) ==========================================================================
# As the 1974 RHD diagram prints it (book photos P5a/P5b; internals-facts 61), at rest (off). Positions are mapped from
# P5b (crop 540-1360 x 920-1340 at 2x): x linear, y set so the left terminals land on pins 1-4's rows; the lever, the
# three position lines and the points on them are kept straight through the hub, as printed.
BX0, BY0, BW = 238, R[1] - 6, 130
BX1, BY1 = BX0 + BW, R[4] + 8.5
SX = BW / 1430
X = lambda u: round(BX0 + (u - 75) * SX, 2)
box(BX0, BY0, BW, BY1 - BY0)
name(BX0 + 14, BY0 - 3, '61', 'Wiper switch')


def on(p, q, x):
    """The point at x on the line through p and q."""
    return (x, round(p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0]), 2))


C53B, C53, C53A = (X(290), R[2]), (X(295), R[3]), (X(340), R[4])
C31B = (X(1215), round(R[1] + 75 / 220 * P, 2))
UF = (X(345), round(R[1] + 80 / 220 * P, 2))           # upper 53b finger
HUB = on(C53A, C31B, X(790))                           # where the position lines cross the lever
R4C, PIV = on(C53A, C31B, X(490)), on(C53A, C31B, X(1010))
R3C, AEND = on(C53, HUB, X(455)), on(C53, HUB, X(1300))
R2C, CA, CB, BEND = on(C53B, HUB, X(450)), on(C53B, HUB, X(1045)), on(C53B, HUB, X(1165)), on(C53B, HUB, X(1280))
C54, CQ, CC, CW = on(UF, HUB, X(485)), on(UF, HUB, X(1025)), on(UF, HUB, X(1130)), on(UF, HUB, X(1235))
CS = (X(1140), round(R[4] + 2.1 * P / 14, 2))
CE = (X(1375), round(R[2] + 10.2 * P / 14, 2))                  # the contact tied to the housing (unread mark)
# position lines (dashed, drawn first so the contacts sit on them): through the hub, one per notch
pline(C53, AEND); pline(C53B, BEND); pline(UF, CW)
# rail from 54: its lead along the top, down into the 54 circle, then the zig-zag of contacts to the lever
inner([(BX0, R[1]), (C54[0], R[1]), C54]); inner([C54, R2C, R3C, R4C])
inner([(BX0, R[2]), C53B]); inner([C53B, UF])           # 53b, and its upper finger (solid, as printed)
inner([(BX0, R[3]), C53]); inner([(BX0, R[4]), C53A])
# right half: the earth stem from the top wall to the pivot; pivot-A-Q joined, B-C-S joined (A-B and Q-C are dashes on
# the position lines, as printed)
inner([(PIV[0], BY0 - 3), PIV]); jdot(PIV[0], BY0, .75); earth_up(PIV[0], BY0 - 3)
inner([PIV, CA, CQ]); inner([CB, CC, CS]); inner([CS, (CS[0], BY1)])
inner([CW, (CW[0], BY1)])
inner([C31B, (BX1, C31B[1])])
inner([CE, (BX1, CE[1])]); jdot(BX1, CE[1], .75)           # tied to the housing's right wall, as printed
# the lever at rest: thick from 53a to the bottom rail contact, a double bar (insulated, probably) past the hub to the
# pivot, thick on to 31b
ux, uy = C31B[0] - C53A[0], C31B[1] - C53A[1]; L = math.hypot(ux, uy); ux, uy = ux / L, uy / L
blade(C53A[0] + .7 * ux, C53A[1] + .7 * uy, R4C[0], R4C[1])
A(f'<path d="M{R4C[0]},{R4C[1]} L{PIV[0]},{PIV[1]}" stroke="#111" stroke-width="1.3"/>'
  f'<path d="M{R4C[0] + 1.2 * ux:.2f},{R4C[1] + 1.2 * uy:.2f} L{PIV[0] - 1.2 * ux:.2f},{PIV[1] - 1.2 * uy:.2f}" stroke="#fff" stroke-width=".4"/>')
blade(PIV[0], PIV[1], C31B[0] - .75 * ux, C31B[1] - .75 * uy)
for p in (C53B, C53, C53A, UF, C54, R2C, R3C, R4C, PIV, C31B, CA, CB, CQ, CC, CS, CW, CE): contact(*p)
# printed terminal marks: 53b, 53, 53a inside the left wall over their leads; 54 by the rail's top; 31b top right; S
tlabel(BX0 + 1.6, R[2] - 1.3, '53b'); tlabel(BX0 + 1.6, R[3] - 1.3, '53'); tlabel(BX0 + 1.6, R[4] - 1.3, '53a')
tlabel(C54[0] + 1.6, R[1] + 3.6, '54'); tlabel(BX1 - 1.6, C31B[1] - 1.3, '31b', 'end')
tlabel(CS[0] - 1.5, CS[1] + 1.6, 'S', 'end')
txt(CW[0] + 1.6, BY1 - 1.6, '<tspan font-style="italic">washer</tspan>', 1.8, fill='#555')   # our name: its mark is unreadable
# probable position names, at the free ends of the lines
glabel(AEND[0] + 1.2, AEND[1] + .6, 'slow'); glabel(BEND[0] + 1.2, BEND[1] + .9, 'fast')
th = math.atan2(CW[1] - HUB[1], CW[0] - HUB[0]); ct, st = math.cos(th), math.sin(th)   # the third along its line, under it
PROBABLE[0] = True
txt(round(HUB[0] + 4 * ct - 2.3 * st, 2), round(HUB[1] + 4 * st + 2.3 * ct, 2), 'fast + washer', 1.8, fill='#888', rot=round(math.degrees(th), 1))

# ---- wires: 58 wiper switch to 61 ----------------------------------------------------------------------------------
XLAB2 = 192
wire('14e', [(XR, R[1]), (BX0, R[1])], XLAB2, R[1] - 1.6)
wire('16e', [(XR, R[2]), (BX0, R[2])], XLAB2, R[2] - 1.6)
wire('15e', [(XR, R[3]), (BX0, R[3])], XLAB2, R[3] - 1.6)
wire('17e', [(XR, R[4]), (BX0, R[4])], XLAB2, R[4] - 1.6)
X18 = BX1 + 9                                          # 18e: under the switch, up its right side, into 31b
wire('18e', [(XR, R[5]), (X18, R[5]), (X18, C31B[1]), (BX1, C31B[1])], XLAB2, R[5] - 1.6)
wire('88e', [(XR, R[6]), (CW[0], R[6]), (CW[0], BY1)], XLAB2, R[6] - 1.6)   # crosses 18e: forced, as printed

# connector block over the wire ends, then every terminal dot
A(f'<rect x="{XL}" y="{R[1] - 4}" width="4" height="{R[6] - R[1] + 8}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
for k in range(1, 7):
    tlabel(X58, R[k] + .65, str(k), 'middle'); dot(XL, R[k]); dot(XR, R[k])
txt(X58, R[6] + 7.6, '58 wiper switch', 2.2, 'middle', w='bold')
for k in range(2, 7): dot(MX1, R[k])
dot(XLOOP, R[3])                                       # 2's loop joins 15 RD
dot(X175, MY1)
for k in range(1, 5): dot(BX0, R[k])
dot(BX1, C31B[1]); dot(CS[0], BY1); dot(CW[0], BY1)
txt(CS[0] + 1.2, BY1 + 3.4, 'S: not used (headlamp wipers not fitted)', 1.8, 'end', fill='#888')   # left of 88e, above 18e
dot(WC[0], WC[1] - WR); dot(WC[0], WC[1] + WR)

# ================= legend ===========================================================================================
lx, ly = 18, 244
box(lx, ly, 389, 41, fill='#fff', sw=.5)
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
    y += 5; A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{y - 1}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    txt(x + 11, y, 'ends on diagram', 2.4)
if TICKED[0]: y += 5; tick(x, y - .7); txt(x + 4, y, 'checked on the car', 2.4)
if probable_legend(x, y + 5): y += 6
py = y + 5
A(f'<path d="M{x},{py - 1} h9" {PLINE}/>'); txt(x + 11, py, 'switch position line (the lever’s other positions)', 2.4)
HW = {**{c: 556 for c in 'abcdeghnopqu0123456789$#_?'}, **{c: 500 for c in 'kvxyzJ'}, **{c: 278 for c in ' ,.:;!/t’‘f'},
      **{c: 222 for c in 'ijl'}, 'r': 333, 's': 500, 'm': 833, 'w': 722, '(': 333, ')': 333, '–': 556, '-': 333,
      **{c: 667 for c in 'ABEKPSVXY'}, **{c: 722 for c in 'CDHNRUw'}, 'F': 611, 'G': 778, 'I': 278, 'L': 556, 'M': 833,
      'O': 778, 'Q': 778, 'T': 611, 'W': 944, 'Z': 611}


def tw(s, size):
    """Helvetica width of s at size (mm)."""
    return sum(HW.get(c, 556) for c in s) * size / 1000


def wrap(s, size, width):
    lines, cur = [], ''
    for w in s.split(' '):
        t = (cur + ' ' + w).strip()
        if cur and tw(t, size) > width: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]


notes = ['Fuse 9 (ignition on) feeds the wipers through 14 BR to 58 wiper switch, pin 1 (pins numbered from the top: our count), and the washer motor '
         'through 89 GL. The washer motor is switched to earth by the wiper switch: 88 SV, pin 6, 88e SV.',
         'Wiper motor 62: 16 GN on 3 feeds the fast brush and 15 RD on 5 the slow one; the third brush is on the housing, earthed by 175 SV. '
         'The bar from M to the housing’s corner is probably the drive, not a wire.',
         'Parking: the motor’s change-over 2, joined to 5 outside the motor, rests on 1 (18 BL to the switch’s 31b) and swings to 4 (17 GR to 53a). '
         'Switched off, 61 feeds 53a and earths 31b, so away from park the motor probably runs on slow through 4, and at park 1 earths the slow brush and brakes it.',
         'Switch 61 is drawn at rest (off): its lever joins 54 to 53a and the earthed pivot to 31b. Grey dashed lines: its other positions, '
         'probably slow (54 to 53), fast (54 to 53b) and fast with the washer (54 to the upper 53b finger, and the washer terminal earthed).',
         '61’s washer terminal: its number is not known; ‘washer’ is our name for it. The contact tied to 61’s housing (earth) is not named.',
         '18e BL runs under the switch and up its right side into 31b, crossing 88e SV.',
         'Headlamp wipers: not fitted on this car; switch 61’s S, which would switch their relay, has nothing on it.']
ny = ly + 5.2
for n in notes:
    for k, t in enumerate(wrap(n, 2.3, 284)): txt(lx + 101 + (2 if k else 0), round(ny, 2), t, 2.3, fill='#333'); ny += 3.4
    ny += .8
save('wipers.svg')

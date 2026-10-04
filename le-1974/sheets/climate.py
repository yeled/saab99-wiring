#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE heater fan and radiator fan sheet (A3 SVG)."""
import math
from common import *

header('Saab 99 LE, model 1974 — Heater fan and radiator fan')


# ---- local helpers (copied or adapted from the Turbo's sheets) ---------------------------------------------
def name(x, y, n, s, size=2.7, anchor='start'):
    """Part name: bold number, then the name (start-anchored: cairosvg misplaces a bold tspan in centred text)."""
    txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', size, anchor)
def note(x, y, s, size=2.2, anchor='start'):
    txt(x, y, s, size, anchor, fill='#555')
def mtag(x, y, lines, w, size=2.4, anchor='start'):
    """Destination tag of two lines (tag() takes one), boxed and centred on y as the Turbo's instruments sheet does."""
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2); x0 = x if anchor == 'start' else x - w
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines): txt(x0 + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
def conn(x, y0, y1, rows, lab, rlabs=()):
    """In-line connector across horizontal runs: grey block 4 wide from y0 to y1, a through-link at each row,
    its short name above (bold, 2.2); rlabs: small grey row/pin names just right of the block, above each row."""
    A(f'<rect x="{x - 2}" y="{y0}" width="4" height="{y1 - y0}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    for ry in rows: inner([(x - 2, ry), (x + 2, ry)])
    txt(x - 2, y0 - 1.6, lab, 2.2, w='bold')
    for ry, s in zip(rows, rlabs): txt(x + 3.6, ry - 2.2, s, 2.0, fill='#555')
def lead(pts):
    """Plain lead on the part side of a connector (not a numbered cable)."""
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')
WORK = [False]  # set when work() draws; the legend then shows its sample
def work(pts):
    """A switch's other positions, short-dashed as the manual prints them (not 'not traced': DASHED stays off)."""
    WORK[0] = True
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".4" stroke-dasharray=".8 .6"/>')
def meander(x, y, w=8, up=1.2, down=1.2):
    """Resistance wire as the manual prints it: square humps above and below the line; x, y is its left end."""
    s = w / 4
    pts = [(x, y)] + [(round(x + (k + j) * s, 2), round(y + (-up if k % 2 == 0 else down), 2)) for k in range(4) for j in (0, 1)] + [(x + w, y)]
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".4" stroke-linejoin="round"/>')
def fan(cx, cy, r, rot=22.5):
    """Fan symbol as the manual prints it for 36: a circle of eight sectors, every other one black."""
    A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#111" stroke-width=".4"/>')
    for k in range(4):
        a0, a1 = math.radians(rot + 90 * k - 22.5), math.radians(rot + 90 * k + 22.5)
        p0 = (round(cx + r * math.cos(a0), 2), round(cy + r * math.sin(a0), 2)); p1 = (round(cx + r * math.cos(a1), 2), round(cy + r * math.sin(a1), 2))
        A(f'<path d="M{cx},{cy} L{p0[0]},{p0[1]} A{r},{r} 0 0 1 {p1[0]},{p1[1]} Z" fill="#111"/>')
def propeller(x, y, h=4.2, w=1.7):
    """The radiator fan's two-bladed propeller, as printed on 37: two lobes meeting at the hub (x, y) on the motor's
    wall. The print has it under the motor; here the motor lies on its side, so the blades stand up its left wall."""
    for s in (-1, 1):
        A(f'<ellipse cx="{x - w}" cy="{y + s * h}" rx="{w}" ry="{h}" fill="#fff" stroke="#111" stroke-width=".6"/>')
def earth_mark(x, y):
    """Small earth glyph, the manual's mark on a part's earth terminal (36); (x, y) the top of its stem."""
    A(f'<path d="M{x},{y} v2.1 M{x - 1.7},{y + 2.1} h3.4 M{x - 1.05},{y + 3} h2.1" stroke="#555" stroke-width=".35" fill="none"/>')


# =========================================== radiator fan (front of the car, left) ===========================
txt(18, 108, 'Radiator fan', 3.4, w='bold')
P2, P1 = 130, 144                    # 59 pin 2 (37 GN / 37e: the + side) and pin 1 (38 SV / 38e, 150: the − side)
XC = 72                              # 59 radiator fan, centre of the block

# 37: the print's symbol, a plain body with the propeller (no terminal names). The stroke hanging from the top wall
# by 38e (book photo P2) runs parallel to the leads and joins the outline: probably not a '−' (36's marks are upright),
# so it is not drawn; the wiring shows 38e is the earthed side. Lying on its side: leads on its right wall, the blades
# on its left. Sources: p.327 (1090-1145,1935-2020), book photo P2; 59 (D2) pin 1 = 38 / 38e + 150, pin 2 = 37 / 37e.
box(24, 120, 20, 34)
propeller(24, 137)
name(18, 162, '37', 'Radiator fan motor')

# relay 38 as printed: 87 on the left wall over 85, 30/51 on the right wall over 86; the blade hinged at 30/51 lifts
# clear of 87's fixed contact (open at rest); coil 85-86 under it. The print's link from the coil to the blade is a
# solid line; drawn here as every relay on these sheets is, with mlink(). Source: book photos P9a/P9b.
RX0, RX1, RY0, RY1 = 112, 148, 120, 154
box(RX0, RY0, RX1 - RX0, RY1 - RY0); name(RX0, RY0 - 2.4, '38', 'Radiator fan relay')
inner([(RX0, P2), (119.2, P2)]); contact(120, P2)                       # 87 and its fixed contact
contact(140, P2); inner([(140.8, P2), (RX1, P2)])                       # 30/51 and the blade's pivot
blade(139.3, P2 - .3, 121, P2 - 3.8)
cl, cr, ct, cb = coil(126, P1 - 3.5, 8, 7)
inner([(RX0, P1), cl]); inner([cr, (RX1, P1)])
mlink([ct, (130, P2 - 1.4)])
tlabel(RX0 + 1.5, P2 - 1.4, '87'); tlabel(RX1 - 1.5, P2 - 1.4, '30/51', 'end')
tlabel(RX0 + 1.5, P1 - 1.4, '85'); tlabel(RX1 - 1.5, P1 - 1.4, '86', 'end')

# thermostat contact 39 as printed (book photo P9a): a box split in two, C° in the upper part, the contact in the
# lower, its blade hinged on the left terminal and lifted clear of the right one (open, cold); earthed on the right
TX0, TX1, TY0, TY1, TC = 132, 152, 170, 186, 181
box(TX0, TY0, TX1 - TX0, TY1 - TY0)
A(f'<path d="M{TX0},{TY0 + 5.5} H{TX1}" stroke="#111" stroke-width=".5"/>')
txt((TX0 + TX1) / 2, TY0 + 4.2, 'C°', 2.6, 'middle')
inner([(TX0, TC), (TX0 + 3.2, TC)]); contact(TX0 + 4, TC)
contact(TX1 - 4, TC); inner([(TX1 - 3.2, TC), (TX1, TC)])
blade(TX0 + 4.7, TC - .4, TX1 - 3.9, TC - 2.7)
lamp_earth(TX1, TC, dx=6)
name(TX0, TY0 - 2.4, '39', 'Thermostat contact', size=2.6)
note(TX1 + 11, TC - 1.4, 'open when cold, as drawn;')
note(TX1 + 11, TC + 1.8, 'closes when the coolant is hot')

# the cables, from the data
wire('37e', [(XC - 2, P2), (44, P2)], 47, P2 - 1.5)
wire('38e', [(XC - 2, P1), (44, P1)], 47, P1 - 1.5)
wire('150', [(XC - 2, P1), (XC - 6, P1 + 4), (XC - 6, 176)], XC - 7.6, 174, rot=-90); earth(XC - 6, 176)
wire('37', [(XC + 2, P2), (RX0, P2)], 88, P2 - 1.5)
wire('38', [(XC + 2, P1), (90, P1), (90, 200), (96, 200)], 88.4, 182, rot=-90)
mtag(96, 200, ('38 SV 1.5 → battery − strap, earth', '(power sheet)'), w=45.5)
wire('149', [(RX0, P1), (106, P1), (106, TC), (TX0, TC)], 110, TC - 1.5)
wire('36', [(RX1, P2), (176, P2)], 154, P2 - 1.5)
mtag(176, P2, ('36 GR 1.5 ← fuse 6', '(power sheet)'), w=25.6)
wire('148', [(RX1, P1), (176, P1)], 154, P1 - 1.5)
mtag(176, P1, ('148 RD 0.75 ← fuse 9', '(power sheet)'), w=27.6)
conn(XC, P2 - 6, P1 + 6, (P2, P1), '59 radiator fan', ('pin 2', 'pin 1'))
for x, y in ((44, P2), (44, P1), (XC - 2, P2), (XC + 2, P2), (XC - 2, P1), (XC + 2, P1),
             (RX0, P2), (RX1, P2), (RX0, P1), (RX1, P1), (TX0, TC), (TX1, TC)):
    dot(x, y)


# =========================================== heater fan ======================================================
txt(214, 108, 'Heater fan', 3.4, w='bold')
H1, H2, H3 = 128, 150, 164           # 57 heater fan rows 1-3
XH = 298                             # 57 heater fan, centre of the block

# motor 36 as printed (p.327 2427-2528,2583-2683): the fan in a box, + on the upper terminal and the earth mark on
# the lower one
box(216, 118, 32, 54)
fan(231, 145, 11)
txt(245.6, H1 + 1, '+', 2.6, 'end', fill='#555')
earth_mark(244, H3 - 3.2)
name(216, 178, '36', 'Heater fan motor')

# the series resistor for the slow speed: no number of its own, a resistance wire in a box as printed, between
# rows 2 and 1 of 57 on the motor side (the print draws it above the + lead with its row-2 lead crossing it; below
# the + lead it needs no crossing)
RS0, RS1, RSY = 266, 284, 137
box(RS0, RSY - 3, RS1 - RS0, 6)
inner([(RS0, RSY), (RS0 + 1.7, RSY)]); contact(RS0 + 2.5, RSY); meander(RS0 + 3.3, RSY, RS1 - RS0 - 6.6, 1.3, 1.3)
contact(RS1 - 2.5, RSY); inner([(RS1 - 1.7, RSY), (RS1, RSY)])
note(RS0 - 4, RSY + 7.2, 'series resistor (slow speed)', 2.1)

lead([(248, H1), (XH - 2, H1)])                                         # motor + to row 1
lead([(RS1, RSY), (290, RSY), (XH - 2, H1)])                           # resistor to row 1
lead([(RS0, RSY), (260, RSY), (260, H2), (XH - 2, H2)])                # resistor to row 2
lead([(248, H3), (XH - 2, H3)])                                         # motor earth to row 3

# switch 35 as printed (book photos P4/P5b; p.327): two circles side by side at the top, joined, 20 BL on the left one
# and '4' printed by the right one; 8 and 6 on the left wall, 8's contact straight under the right circle, 6's further
# right. The bar lies clear of every contact (off). Short dashes, its other positions: a vertical from the right
# circle down through 8 and across 6's lead, ending just below it (4 to 8 and 6); a diagonal from the left circle to 6
# (4 to 6), broken where it passes behind the bar. The print's bar also hides where the two dashed lines cross, so it
# is drawn through that point; the dashes stop clear of it on both sides. No position numbers are printed.
SX0, SX1, SY0, SY1 = 334, 362, 98, 156
XV, T = 344, 104                                       # the vertical's x (right circle, 8); the circles' row
L4, R4, C8, C6 = (341.7, T), (XV, T), (XV, H1), (350.5, H2)
box(SX0, SY0, SX1 - SX0, SY1 - SY0)
inner([(L4[0], SY0), (L4[0], T - .8)]); contact(*L4); inner([(L4[0] + .8, T), (R4[0] - .8, T)]); contact(*R4)
inner([(SX0, H1), (C8[0] - .8, H1)]); contact(*C8)
inner([(SX0, H2), (C6[0] - .8, H2)]); contact(*C6)
# the diagonal crosses the vertical at YC; the bar runs through that point, from left of and below the left circle to
# right of 6's contact
YC = T + (XV - L4[0]) * (C6[1] - T) / (C6[0] - L4[0])
BAR = ((XV - .41 * (YC - 106.5), 106.5), (XV + .41 * (146 - YC), 146))
def bar_cut(p, q, g=1.3):
    """The dashed line p-q as the pieces lying at least g from the bar's centre line (the print hides the rest)."""
    (bx0, by0), (bx1, by1) = BAR; bl = math.hypot(bx1 - bx0, by1 - by0); nx, ny = -(by1 - by0) / bl, (bx1 - bx0) / bl
    d0 = (p[0] - bx0) * nx + (p[1] - by0) * ny; d1 = (q[0] - bx0) * nx + (q[1] - by0) * ny
    if d0 * d1 > 0: return [[p, q]]
    tc = d0 / (d0 - d1); dt = g / abs(d0 - d1)
    at = lambda t: (round(p[0] + t * (q[0] - p[0]), 2), round(p[1] + t * (q[1] - p[1]), 2))
    return [[p, at(tc - dt)], [at(tc + dt), q]]
def toward(a, b, r=.8):
    """The point r from a towards b (where a lead leaves a contact circle)."""
    l = math.hypot(b[0] - a[0], b[1] - a[1]); return (round(a[0] + r * (b[0] - a[0]) / l, 2), round(a[1] + r * (b[1] - a[1]) / l, 2))
for seg in bar_cut((XV, T + .8), (XV, H1 - .8)): work(seg)       # 4 (right circle) to 8
work([(XV, H1 + .8), (XV, H2 + 1.6)])                            # on through 8, across 6's lead
for seg in bar_cut(toward(L4, C6), toward(C6, L4)): work(seg)     # 4 (left circle) to 6, behind the bar
A(f'<path d="M{BAR[0][0]},{BAR[0][1]} L{BAR[1][0]},{BAR[1][1]}" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>')
blade(*BAR[0], *BAR[1])
tlabel(R4[0] + 1.5, T + .7, '4'); tlabel(SX0 + 1.5, H1 - 1.4, '8'); tlabel(SX0 + 1.5, H2 - 1.4, '6')
name(SX1 + 3, 130, '35', 'Heater fan switch', size=2.6)
note(SX1 + 3, 133.6, 'drawn off: the bar')
note(SX1 + 3, 136.8, 'touches no contact')

wire('33', [(XH + 2, H1), (SX0, H1)], 314, H1 - 1.5)
wire('35', [(XH + 2, H2), (SX0, H2)], 314, H2 - 1.5)
wire('138', [(XH + 2, H3), (331, H3), (331, 178)], 312, H3 - 1.5); earth(331, 178)
note(336, 182.4, 'the same earth point as the wiper motor’s')
note(336, 185.6, '175 SV (wipers sheet)')
wire('20', [(L4[0], SY0), (L4[0], 90), (366, 90)], 347, 88.5)
mtag(366, 90, ('20 BL 2.5 ← fuse 10', '(power sheet)'), w=27)
conn(XH, H1 - 6, H3 + 6, (H1, H2, H3), '57 heater fan', ('row 1', 'row 2', 'row 3'))
for x, y in ((248, H1), (248, H3), (RS0, RSY), (RS1, RSY), (XH - 2, H1), (XH + 2, H1), (XH - 2, H2), (XH + 2, H2),
             (XH - 2, H3), (XH + 2, H3), (SX0, H1), (SX0, H2), (L4[0], SY0)):
    dot(x, y)


# =========================================== legend and notes ================================================
lx, ly = 18, 250
box(lx, ly, 389, 37, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 4
def r_traced(y):
    w = WIDTH[1.0] + edge(WIDTH[1.0])
    A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="{w:g}"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
    if DASHED[0]: A(f'<path d="M{x + 48},{y - 1} h9" stroke="#222" stroke-width="{w:g}" stroke-dasharray="3 2"/>'); txt(x + 59, y, 'not traced yet', 2.4)
def r_stub(y):
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{y - 1}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    txt(x + 11, y, 'ends on diagram', 2.4)
def r_tick(y): tick(x, y - .7); txt(x + 4, y, 'checked on the car', 2.4)
def r_work(y): work([(x, y - 1), (x + 9, y - 1)]); txt(x + 11, y, 'short dashes inside a switch: its other positions', 2.4)
def r_mlink(y): mlink([(x, y - 1), (x + 9, y - 1)]); txt(x + 11, y, 'grey dashes inside a relay: the coil moving its blade', 2.4)
rows = ([lambda y: size_legend(x, y), r_traced] + [r_stub] * STUB[0] + [r_tick] * TICKED[0]
        + [lambda y: probable_legend(x, y - 1)] * PROBABLE[0] + [r_work] * WORK[0] + [r_mlink])
y0, y1 = ly + 17, ly + 34.8
for k, row in enumerate(rows): row(y0 + k * min(6, (y1 - y0) / max(1, len(rows) - 1)))
notes = ['Radiator fan: relay 38 (drawn at rest, contact open) takes its coil feed from fuse 9, live with the ignition on, and its contact feed from fuse 6, always live.',
         'Thermostat contact 39 earths the coil when the coolant is hot, so the fan runs only with the ignition on. 37 GN becomes 37e SV beyond radiator fan connector 59,',
         'so both of the motor’s own leads are black; its 38e side is earthed twice, by 38 SV to the battery − strap and by 150 SV to an earth of its own.',
         'Heater fan: fuse 10, live with the ignition on, feeds switch 35. Probably position 1 is slow (4 to 6: 35 GR through the series resistor) and position 2 fast',
         '(4 to 8 and 6: 33 GL straight to the motor). The series resistor has no number of its own; it sits on the motor side of heater fan connector 57, between rows 2 and 1.',
         'The motor returns through row 3 and 138 SV to the earth point it shares with the wiper motor.',
         'Thin black lines without a label: leads with no cable number.']
for j, n in enumerate(notes): txt(lx + 102, ly + 6 + j * 4.6, n, 2.35, fill='#333')
save('climate.svg')

#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE fuel injection sheet (Bosch D-Jetronic; A3 landscape SVG).

Control unit 92 across the top with its 25 pins, the injectors, sensors, throttle switch and trigger contacts round it,
the master and pump relays, the pump and the cold-start valve below. Laid out after the injection detail
(service manual 1969-74, 371-43, drawing S 3783, PDF p.347; book photos P6a and P6b). Wire identity, colour, size and
status come from data/wires.csv.
"""
from common import *

header('Saab 99 LE, model 1974 — Fuel injection (D-Jetronic)')

# ---- local helpers (the Turbo's, plus a text width for tag boxes) ------------------------------
# Helvetica advance widths (1/1000 em) so a tag's box fits its text; the arrows are set in Arial (lib txt()).
_W = dict(zip(' .,:;()/-–+°', (278, 278, 278, 278, 278, 333, 333, 278, 333, 556, 584, 400)))
_W.update({c: 556 for c in '0123456789'})
_W.update(dict(zip('abcdefghijklmnopqrstuvwxyz', (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556,
                                                    556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500))))
_W.update(dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
                                                    778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611))))
_W.update({'←': 1000, '→': 1000})
def tw(s, size): return round(sum(_W.get(c, 600) for c in s) * size / 1000, 2)

def name(x, y, n, s, anchor='start', size=2.7):
    txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', size, anchor)
def jdot(x, y):
    """Junction inside a part: smaller than a terminal dot."""
    A(f'<circle cx="{x}" cy="{y}" r=".55" fill="#111"/>')
def glabel(x, y, t, anchor='start'):
    """Terminal mark printed but not readable (probably): tlabel size, light grey (the legend's grey sample then shows)."""
    PROBABLE[0] = True
    txt(x, y, t, 1.8, anchor, fill='#888')
def ftag(x, y, text, anchor='start', size=2.4):
    """tag() with its box fitted to the text."""
    return tag(x, y, text, w=round(tw(text, size) + 3.2, 1), size=size, anchor=anchor)
def mtag(x, y, lines, size=2.4, anchor='start'):
    """Destination tag of several lines (tag() takes one): left edge x (right edge with anchor='end'), centred on y."""
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2); w = round(max(tw(t, size) for t in lines) + 3.2, 1)
    x0 = x if anchor == 'start' else x - w
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, t in enumerate(lines): txt(x0 + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), t, size)
    return x0 + w
def pin_v(x, y, w=8):
    """One connector pin on a vertical run: grey block across it, 4 mm along the run, centred on (x, y)."""
    A(f'<rect x="{x - w / 2}" y="{y - 2}" width="{w}" height="4" fill="#ddd" stroke="#111" stroke-width=".5"/>')

DOTS = []                                   # terminal and joint dots: drawn last, over the wires
def T(x, y): DOTS.append((x, y)); return (x, y)

# ---- geometry ------------------------------------------------------------------------------------
def PX(n): return 102 + 10 * n             # control unit pin n (pin 1 x 112, pin 25 x 352)
PY = 58                                     # pins on the control unit's bottom edge
# One height per horizontal run under the control unit (5 mm apart, so a label fits between two runs). Runs to the
# left take the top heights in pin order (the lowest pin highest), so no pin's drop crosses the runs of the pins left
# of it; 211 (to the earth point) sits above the throttle-switch runs it would otherwise cross. 220 is above 214 and
# 217 so that it reaches throttle switch terminal 20 (second from the top) without crossing them beside the switch:
# the price is two plain crossings at the 214 and 217 drops. 212 runs right below the throttle-switch runs (fewer
# drops cross it there); 222 and 221 bracket it, in the order of 98's terminals.
TY = {'203': 63, '204': 68, '205': 73, '206': 78, '211': 83, '209': 88, '220': 93, '214': 98, '217': 103,
      '222': 98, '212': 108, '221': 118}
Y213 = 113                                  # 213's run left to sensor 95, under 212's start

# ---- control unit 92 -------------------------------------------------------------------------------
box(PX(1) - 7, 38, PX(25) - PX(1) + 13, PY - 38)
name(PX(1) - 4, 45.5, '92', 'Control unit')
txt(PX(6), 45.5, 'Cables 201–224 each run to the pin with the same last two digits (201 to pin 1, 224 to pin 24).', 2.2, fill='#555')
txt(PX(6), 49.3, 'Pins 2 and 25 are not used.', 2.2, fill='#555')
for n in range(1, 26): txt(PX(n), PY - 2.4, str(n), 1.9, 'middle', fill='#333')

# ---- injectors 93 (top left) -------------------------------------------------------------------------
# Printed left to right CYL 2, CYL 1, CYL 3, CYL 4 (the digits are blurred on every print): in that order the feeds
# from pins 6, 5, 4, 3 nest without crossing. Each is a winding between two leads; the feed enters the right lead
# (bottom here), the black return leaves the left lead, drawn out of the top so the returns run over the injectors to
# the earth point without crossing the feeds (the print brings both leads out of the bottom and crosses them).
IX = [36, 50, 64, 78]                       # box left edges
IW, IT, IB = 11, 46.5, 58.5                     # width, top, bottom
INJ = [('2', '206', '227'), ('1', '205', '226'), ('3', '204', '228'), ('4', '203', '229')]
RY = {'229': 26.5, '228': 32.5, '226': 38.5, '227': 44.5}   # return heights into the earth point: 6 apart, so each label
                                                     # sits clearly on its own return, not the one above
for x0, (cyl, feed, ret) in zip(IX, INJ):
    box(x0, IT, IW, IB - IT)
    cl, cr, ct, cb = coil(x0 + 4, IT + 3, 3.2, 6.5)        # the winding, upright
    inner([(x0 + 2, IT), (x0 + 2, IT + 1.5), (ct[0], IT + 1.5), ct])            # return lead (top left)
    inner([cb, (cb[0], IB - 1.5), (x0 + 9, IB - 1.5), (x0 + 9, IB)])             # feed lead (bottom right)
    txt(x0 + 2.5, 62.5, f'cylinder {cyl}', 1.9, 'middle')
txt(IX[3] + IW + 2.5, 52, '93', 3.0, w='bold'); txt(IX[3] + IW + 2.5, 55.6, 'Injectors', 2.3)

EBX = 16                                    # the injection loom's earth point (a bar, hatched on its outer side)
RIS = {'232': 20, '235': 24, '211': 28}     # the three risers into it from below, outermost first
EY = {'211': 50, '235': 54.5, '232': 59}
for x0, (cyl, feed, ret) in zip(IX, INJ):
    wire(ret, [(x0 + 2, IT), (x0 + 2, RY[ret]), (EBX, RY[ret])], EBX + 3, RY[ret] - 1.3)
    T(x0 + 2, IT)
FEED_LX = {'203': 90, '204': 75, '205': 61, '206': 47}
for x0, (cyl, feed, ret) in zip(IX, INJ):
    n = int(feed) - 200
    wire(feed, [(PX(n), PY), (PX(n), TY[feed]), (x0 + 9, TY[feed]), (x0 + 9, IB)], FEED_LX[feed], TY[feed] - 1.3)
    T(x0 + 9, IB); T(PX(n), PY)

# ---- earth point ----------------------------------------------------------------------------------------
A(f'<path d="M{EBX},{RY["229"] - 1.5} V{EY["232"] + 1.5}" stroke="#111" stroke-width="1.2"/>')
for i in range(9):
    y = RY['229'] - 1 + i * 4
    A(f'<path d="M{EBX},{y} l-3.2,3.2" stroke="#111" stroke-width=".4"/>')
txt(EBX - 4.5, EY['232'] + 6, 'earth', 2.0, fill='#555')
txt(EBX - 4.5, EY['232'] + 8.6, 'point', 2.0, fill='#555')

# ---- throttle switch 94 ------------------------------------------------------------------------------------
# Book photo P6b: terminals down the right wall 9, 20, 47, 14, 17. Drawn with 47 on the left wall (its lead goes to the
# common bar on the left anyway), so 235 leaves straight for the earth point without crossing 209 and 220.
# Inside, as printed: the acceleration contacts, four fixed contacts in a column wired alternately to 9 and 20 (the
# upper-middle one's lead crosses the 9 link and runs down into 20); a wiper pivoted on the common, printed as a
# heavy arm onto the top contact (9), dotted sweep lines to the two middle ones and a thin line to the bottom one (20):
# grey, as what each line means is not certain. Below the wiper, as printed (P6b at 6-9x): a thin line down from the
# wiper's pivot to a small circle, a heavy arm (jogging right) from that circle down to the node where 47 joins, a
# heavy arm from the node to the full-load contact (14), a thin line on down to the idle arm's pivot, and the idle arm
# onto its contact (17): closed, read. The full-load arm touches its contact on the print, but the contact should
# close only near full throttle: drawn open (grey) and left for Charlie (internals row: unresolved). The cam on the
# throttle shaft bears on the heavy arm through a lever, and a dashed frame from the cam hooks onto the wiper, the
# full-load arm and the idle arm: drawn as mechanical links (the frame's run to the 14 hook crosses the common, as
# printed; its upright crosses 47's lead, which the print brings in from the right).
SX0, SX1, SY0, SY1 = 42, 70, 116, 166
box(SX0, SY0, SX1 - SX0, SY1 - SY0)
name(SX0, SY1 + 4.2, '94', 'Throttle switch')
S9, S20, S14, S17, S47 = 125, 137, 150, 158, 150
CB = SX0 + 10                               # the common
P1, N, P2 = (CB, 140), (CB, S14), (CB, 160)  # small circle under the wiper, the node (47 joins), the idle arm's pivot
for c in (P1, N, P2): contact(*c)
inner([(SX0, S47), (N[0] - .8, S47)])                                        # 47 to the node
inner([(CB, 129.5), (CB, P1[1] - .8)]); inner([(CB, N[1] + .8), (CB, P2[1] - .8)])
c1, c2, c3, c4 = (58, S9), (59.5, 129), (59.5, 133), (58, S20)
for c in (c1, c2, c3, c4): contact(*c)
inner([(c1[0] + .8, S9), (SX1, S9)]); inner([(c4[0] + .8, S20), (SX1, S20)])
inner([(c2[0] + .8, c2[1]), (66.5, c2[1]), (66.5, S20)]); jdot(66.5, S20)          # upper-middle contact to 20
inner([(c3[0] + .8, c3[1]), (63.5, c3[1]), (63.5, S9)]); jdot(63.5, S9)            # lower-middle contact to 9 (crosses)
jdot(CB, 129.5)
blade(CB + .4, 129.2, c1[0] - .7, c1[1] + .4, grey=True)                    # wiper, heavy line onto the top contact
A(f'<path d="M{CB + .6},{129.6} L{c2[0] - .9},{c2[1]} M{CB + .6},{129.9} L{c3[0] - .9},{c3[1]}" stroke="#888" '
  f'stroke-width=".35" stroke-dasharray=".6 .6"/>')                          # sweep lines, dotted
inner([(CB + .5, 130.2), (c4[0] - .7, c4[1] - .4)], grey=True)               # thin line onto the bottom contact
HA = [(P1[0] + .55, P1[1] + .55), (CB + 3, 142), (N[0] + .6, N[1] - .6)]    # heavy arm, circle to node: grey
A(f'<path d="{path(HA)}" fill="none" stroke="#888" stroke-width=".75" stroke-linecap="round" stroke-linejoin="round"/>')
c14, c17 = (58, S14), (58, S17)
contact(*c14); contact(*c17)
inner([(c14[0] + .8, S14), (SX1, S14)]); inner([(c17[0] + .8, S17), (SX1, S17)])
blade(N[0] + .7, N[1] + .3, c14[0] - .8, S14 + 1.7, grey=True)               # full-load: open, probably (tip low,
                                                                             # clear of the heavy arm)
blade(P2[0] + .6, P2[1] - .3, c17[0] - .7, S17 + .4)                         # idle: closed
CAM = (SX0 + 5, 144)
A(f'<circle cx="{CAM[0]}" cy="{CAM[1]}" r="2.2" fill="#fff" stroke="#111" stroke-width=".4"/>'
  f'<path d="M{CAM[0] - 1.5},{CAM[1] + 1.5} L{CAM[0] + 1.5},{CAM[1] - 1.5}" stroke="#111" stroke-width=".4"/>')   # cam
def on_arm(p, q, y):
    """x of the segment p-q at height y."""
    return round(p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1]), 2)
def at_x(p, q, x):
    """y of the segment p-q at x."""
    return round(p[1] + (q[1] - p[1]) * (x - p[0]) / (q[0] - p[0]), 2)
mlink([(CAM[0] + 2.2, CAM[1]), (on_arm(HA[1], HA[2], CAM[1]) - .45, CAM[1])])      # the cam's lever on the heavy arm
HX, HW = 55.5, 54.2                                                          # hook columns: lower arms, wiper
mlink([(CAM[0], CAM[1] - 2.2), (CAM[0], 124.5), (HW, 124.5), (HW, at_x((CB + .4, 129.2), (c1[0] - .7, c1[1] + .4), HW) - .5)])
mlink([(CAM[0], CAM[1] + 2.2), (CAM[0], 163), (HX, 163), (HX, at_x((P2[0] + .6, P2[1] - .3), (c17[0] - .7, S17 + .4), HX) + .5)])
mlink([(CAM[0], 154.5), (HX, 154.5), (HX, at_x((N[0] + .7, N[1] + .3), (c14[0] - .8, S14 + 1.7), HX) + .5)])
glabel(SX1 - 1.4, S9 - 1.2, '9', 'end'); tlabel(SX1 - 1.4, S20 + 2.4, '20', 'end')
tlabel(SX1 - 1.4, S14 - 1.2, '14', 'end'); tlabel(SX1 - 1.4, S17 + 2.4, '17', 'end'); tlabel(SX0 + 1.4, S47 - 1.2, '47')
txt(SX0 + 1.5, SY0 + 4, 'acceleration', 1.8, fill='#555'); txt(SX0 + 1.5, SY0 + 6.3, 'contacts', 1.8, fill='#555')
txt(c14[0] + 2, S14 + 3.6, 'full load', 1.6, fill='#555'); txt(c17[0] + 2, S17 + 3.6, 'idle', 1.6, fill='#555')

# four of the throttle-switch cables: down beside the switch in nested order (the top terminal innermost); 235 (47)
# leaves the left wall for the earth point
DX = {'209': 78, '220': 83, '214': 88, '217': 93}
TT = {'209': S9, '220': S20, '214': S14, '217': S17}
for cab in ('209', '220', '214', '217'):
    n = int(cab) - 200
    wire(cab, [(PX(n), PY), (PX(n), TY[cab]), (DX[cab], TY[cab]), (DX[cab], TT[cab]), (SX1, TT[cab])],
         DX[cab] + 2, TY[cab] - 1.3)
    T(PX(n), PY); T(SX1, TT[cab])
wire('235', [(EBX, EY['235']), (RIS['235'], EY['235']), (RIS['235'], S47), (SX0, S47)], RIS['235'] + 3.3, 112, rot=-90)
T(SX0, S47)
wire('211', [(PX(11), PY), (PX(11), TY['211']), (RIS['211'], TY['211']), (RIS['211'], EY['211']), (EBX, EY['211'])],
     36, TY['211'] - 1.3)
T(PX(11), PY)

# ---- sensors 95, 96, 97 (middle row) -------------------------------------------------------------------
QY = 146                                    # tops of 95 and 96
# 95, intake-air temperature: an NTC resistor (a resistor with a diagonal through it), its two terminals on top
X95 = PX(1)
box(X95 - 5, QY, 18, 18)
ra, rb = resistor(X95 - 1.5, QY + 5, 3, 9)
A(f'<path d="M{X95 - 3},{QY + 15} L{X95 + 3},{QY + 3.8}" stroke="#111" stroke-width=".35"/>')
inner([(X95, QY), ra]); inner([rb, (X95, QY + 16), (X95 + 8, QY + 16), (X95 + 8, QY)])
glabel(X95 + 1.2, QY + 2.6, '1'); glabel(X95 + 9.2, QY + 2.6, '13')
name(X95 + 16, QY + 5, '95', 'Temperature', size=2.6); txt(X95 + 16, QY + 8.6, 'sensor I', 2.6); txt(X95 + 16, QY + 12.2, 'intake air', 2.3, fill='#555')
wire('201', [(PX(1), PY), (PX(1), QY)], PX(1) - 1.3, QY - 3, rot=-90)
wire('213', [(PX(13), PY), (PX(13), Y213), (X95 + 8, Y213), (X95 + 8, QY)], X95 + 12, Y213 - 1.3)
T(PX(1), PY); T(PX(13), PY); T(X95, QY); T(X95 + 8, QY)
# 96, pressure sensor: terminals 7, 8, 10, 15 on top (8 and 15 probably), each straight under its pin; two windings:
# a short one between 8 and 10 near the top and a long one along the bottom joining 7 and 15
X96 = PX(7) - 6
box(X96, QY, PX(15) + 6 - X96, 20)
c8a, c8b, _, _ = coil(PX(8) + 4, QY + 4, 12, 4)
inner([(PX(8), QY), (PX(8), QY + 6), c8a]); inner([c8b, (PX(10), QY + 6), (PX(10), QY)])
c7a, c7b, _, _ = coil(PX(10) + 2, QY + 14, 26, 4)
inner([(PX(7), QY), (PX(7), QY + 16), c7a]); inner([c7b, (PX(15), QY + 16), (PX(15), QY)])
tlabel(PX(7) + 1.2, QY + 2.6, '7'); glabel(PX(8) + 1.2, QY + 2.6, '8'); tlabel(PX(10) + 1.2, QY + 2.6, '10')
glabel(PX(15) - 1.2, QY + 2.6, '15', 'end')
name(PX(10) + 8, QY + 7.6, '96', 'Pressure sensor', size=2.6)
for cab in ('207', '208', '210', '215'):
    n = int(cab) - 200
    wire(cab, [(PX(n), PY), (PX(n), QY)], PX(n) - 1.3, QY - 3, rot=-90)
    T(PX(n), PY); T(PX(n), QY)
# 97, coolant temperature: a triangle with C° in it, 223 into its apex, its earth 232 from the left corner of its base
A97 = (PX(23), 148); B97 = 160
A(f'<path d="M{A97[0]},{A97[1]} L{A97[0] + 6},{B97} L{A97[0] - 6},{B97} Z" fill="#fafafa" stroke="#111" stroke-width=".8" stroke-linejoin="round"/>')
txt(A97[0], B97 - 2.6, 'C°', 2.4, 'middle')
name(PX(19) + 5, 135, '97', 'Temperature', size=2.6); txt(PX(19) + 5, 138.6, 'sensor II', 2.6)
txt(PX(19) + 5, 142.2, 'coolant', 2.3, fill='#555')
wire('223', [(PX(23), PY), A97], PX(23) - 1.3, A97[1] - 4, rot=-90)
T(PX(23), PY)
Y232 = 178
wire('232', [(A97[0] - 6, B97), (A97[0] - 6, Y232), (RIS['232'], Y232), (RIS['232'], EY['232']), (EBX, EY['232'])],
     150, Y232 - 1.3)
T(A97[0] - 6, B97)

# ---- trigger contacts 98 (in the distributor) --------------------------------------------------------------
# Book photo P6b: three terminals on the left wall (marks not readable, probably 22, 12, 21 top to bottom); two arms,
# from the top and bottom terminals, each resting on a fixed contact (closed, probably); the fixed contacts are joined
# on the right and go to the middle terminal, the common.
GX0, GX1 = 368, 404
GY = {'222': TY['222'], '212': TY['212'], '221': TY['221']}
box(GX0, GY['222'] - 8, GX1 - GX0, GY['221'] - GY['222'] + 16)
name(GX0, GY['222'] - 10, '98', 'Trigger contacts')
txt(GX0, GY['221'] + 12.5, 'in the distributor (ignition sheet)', 2.2, fill='#555')
pa, pb = (GX0 + 7, GY['222']), (GX0 + 7, GY['221'])
fa, fb = (GX0 + 22, GY['222'] + 3.2), (GX0 + 22, GY['221'] - 3.2)
for c in (pa, pb, fa, fb): contact(*c)
inner([(GX0, GY['222']), (pa[0] - .8, pa[1])]); inner([(GX0, GY['221']), (pb[0] - .8, pb[1])])
blade(pa[0] + .7, pa[1] + .1, fa[0] - .7, fa[1] - .5, grey=True); blade(pb[0] + .7, pb[1] - .1, fb[0] - .7, fb[1] + .5, grey=True)
inner([(fa[0] + .8, fa[1]), (GX0 + 27, fa[1]), (GX0 + 27, fb[1]), (fb[0] + .8, fb[1])])
inner([(GX0, GY['212']), (GX0 + 27, GY['212'])]); jdot(GX0 + 27, GY['212'])
for cab, t in (('222', '22'), ('212', '12'), ('221', '21')): glabel(GX0 + 1.4, GY[cab] - 1.2, t)
for cab in ('222', '212', '221'):
    n = int(cab) - 200
    wire(cab, [(PX(n), PY), (PX(n), TY[cab]), (GX0, TY[cab])], PX(24) + 3, TY[cab] - 1.3)
    T(PX(n), PY); T(GX0, TY[cab])

# ---- master relay 101 and fuel pump relay 102 -----------------------------------------------------------------
# Book photos P6a/P6b print both alike: a blade hinged at 30/51 with its tip raised over the fixed contact of 87 (open
# at rest), the coil between the two lower terminals, a solid line from the blade down to the coil (drawn here with the
# dashed mechanical link, as every relay on these sheets). Only 87 is legible on either; the other marks are grey.
# 101 as printed (30/51 upper left, 86 lower left, 87 right, 85 at the bottom). 102 rearranged so 219 comes in from
# above and 185 from the right without crossing: coil on the left wall (85 upper, 86 lower), contact on the right wall
# (87 upper, 30/51 lower); its elements and rest state as printed.
MX0, MX1, MY0, MY1 = 214, 250, 212, 242
box(MX0, MY0, MX1 - MX0, MY1 - MY0)
name(MX0, MY0 - 2.2, '101', 'Master relay')
M30, M86, M87, M85 = (MX0, 218), (MX0, 236), (MX1, 222), (MX1 - 6, MY1)
contact(MX0 + 5, 218); inner([M30, (MX0 + 4.2, 218)])
contact(MX1 - 6, M87[1]); inner([(MX1 - 5.2, M87[1]), M87])
blade(MX0 + 5.7, 217.8, MX1 - 7.3, 219.2)                                       # 30/51-87: open at rest
cl, cr, ct, cb = coil(MX0 + 11, M86[1] - 3, 10, 6)
inner([M86, cl]); inner([cr, (M85[0], cr[1]), M85])
mlink([ct, (ct[0], 218.9)])
glabel(MX0 + 2.4, 218 - 1.8, '30/51'); glabel(MX0 + 1.4, 236 - 1.3, '86'); tlabel(MX1 - 1.4, 222 - 1.3, '87', 'end')
glabel(M85[0] - 1.2, MY1 - 1.3, '85', 'end')
BX0, BX1, BY0, BY1 = 300, 336, 208, 240
box(BX0, BY0, BX1 - BX0, BY1 - BY0)
name(BX0, BY0 - 2.2, '102', 'Fuel pump relay')
P85, P86, P87, P30 = (BX0, 214), (BX0, 234), (BX1, 214), (BX1, 234)
cl, cr, ct, cb = coil(BX0 + 5, 219, 6, 10)
inner([P85, (cl[0] + 3, 214), ct]); inner([cb, (cb[0], 234), P86])
contact(BX1 - 8, 214); contact(BX1 - 8, 234)
inner([(BX1 - 7.2, 214), P87]); inner([(BX1 - 7.2, 234), P30])
blade(BX1 - 7.7, 233.3, BX1 - 5.2, 216.5)                                       # 30/51-87: open at rest
mlink([cr, (BX1 - 6.6, cr[1])])
glabel(BX0 + 1.4, 214 - 1.3, '85'); glabel(BX0 + 1.4, 234 - 1.3, '86'); tlabel(BX1 - 1.9, 214 - 1.8, '87', 'end')
glabel(BX1 - 1.9, 234 - 1.8, '30/51', 'end')

wire('216', [(PX(16), PY), (PX(16), M87[1] - 10), M87], PX(16) - 1.3, 197, rot=-90)
wire('224', [(PX(24), PY), (PX(24), 200), (268, 200), (268, M87[1]), M87], PX(19) + 4, 198.7)
wire('230', [M87, (M87[0] + 12, P86[1]), P86], M87[0] + 13.5, P86[1] - 1.3)
wire('219', [(PX(19), PY), (PX(19), P85[1]), P85], PX(19) - 1.3, 197, rot=-90)
T(PX(16), PY); T(PX(24), PY); T(PX(19), PY); T(*M87); T(*P86); T(*P85)
wire('182', [M85, (M85[0], 252), (224, 252), (224, 254)], 225.5, 250.7); earth(224, 254)
T(*M85)
wire('234', [(170, M30[1]), M30], 174, M30[1] - 1.3)
ftag(170, M30[1], '234 RD 2.5 ← starter 30, battery + (power sheet)', anchor='end')
wire('181', [(170, M86[1]), M86], 174, M86[1] - 1.3)
mtag(170, M86[1], ['181 GN/VT 0.75 ← ignition feed joint', 'by the coil (ignition sheet)'], anchor='end')
T(*M30); T(*M86)

# ---- fuel pump 103 -------------------------------------------------------------------------------------------------
# Printed as a circle with a smaller circle in it and a mounting flag; 186 in, 187 out to its own earth.
FPX, FPY, FPR = 378, 214, 7
A(f'<rect x="{FPX - FPR - 4}" y="{FPY - FPR - 2}" width="{FPR + 3}" height="3.6" fill="#fafafa" stroke="#111" stroke-width=".8"/>')   # flag
A(f'<circle cx="{FPX}" cy="{FPY}" r="{FPR}" fill="#fff" stroke="#111" stroke-width=".8"/>'
  f'<circle cx="{FPX}" cy="{FPY}" r="2.6" fill="#fff" stroke="#111" stroke-width=".6"/>')
name(FPX - FPR - 5, FPY + FPR + 4.5, '103', 'Fuel pump', size=2.6)
txt(FPX - FPR - 5, FPY + FPR + 8, 'in the boot, left', 2.2, fill='#555')
wire('186', [P87, (FPX - FPR, FPY)], 341, FPY - 1.3)
P187 = (round(FPX + FPR * .7071, 2), round(FPY - FPR * .7071, 2))           # off the top right, clear of the flag
wire('187', [P187, (P187[0], FPY - 15), (402, FPY - 15), (402, FPY - 12)], P187[0] + 2, FPY - 16.5); earth(402, FPY - 12)
T(FPX - FPR, FPY); T(*P187); T(*P87)
wire('185', [P30, (362, P30[1])], 340, P30[1] - 1.3)
ftag(362, P30[1], '185 GR 1.5 ← fuse 8 (power sheet)')
T(*P30)

# ---- cold start: 59, valve 99, thermostat contact 100 ------------------------------------------------------------
# 59 cold start as printed on this detail: a two-pin block on the 218 line; 218 and 231 meet at its upper pin, and the
# lower pin sits on the starter line (84f/84e). The ignition sheet's drawing has the start signal taken off at
# 60 starter signal instead (84h): which is right is check E1, so the starter line here is a plain line to a tag.
X59, Y59 = PX(18), 250
J59 = (X59, Y59 + 6.5)                     # 231 drops 2.5 below pin 1 before it turns, clear of the block; the link
pin_v(X59, Y59 + 2); pin_v(X59, Y59 + 14)   # to pin 2 goes on down from that joint
inner([J59, (X59, Y59 + 12)])
txt(X59 + 6, Y59 + 14.8, '59 cold start', 2.2, w='bold', fill='#555')
txt(X59 - 5, Y59 + 2.7, 'pin 1', 2.0, 'end', fill='#555'); txt(X59 - 5, Y59 + 14.7, 'pin 2', 2.0, 'end', fill='#555')
wire('218', [(PX(18), PY), (X59, Y59)], PX(18) - 1.3, 197, rot=-90)
T(PX(18), PY)
X99, Y99 = 322, J59[1]
wire('231', [(X59, Y59 + 4), J59, (X99, Y99)], X59 + 13, Y99 - 1.3)
inner([(X59, Y59 + 16), (X59, 276), (284, 276)])
mtag(284, 276, ['← starter line, live only while cranking: probably joins', 'at 60 starter signal (ignition sheet; check E1)'], size=2.2)
for y in (Y59, Y59 + 4, J59[1], Y59 + 12, Y59 + 16): T(X59, y)
# 99, cold-start valve: a winding in series between its two leads
box(X99, Y99 - 6, 14, 12)
cl, cr, _, _ = coil(X99 + 3.5, Y99 - 2.5, 7, 5); inner([(X99, Y99), cl]); inner([cr, (X99 + 14, Y99)])
name(X99, Y99 + 9.5, '99', 'Cold-start valve', size=2.4)
# 100, thermostat contact: C° above, a blade below hinged on the left terminal, open (probably: opens when warm)
X100 = 362
box(X100, Y99 - 11, 18, 15)
A(f'<path d="M{X100},{Y99 - 4.5} h18" stroke="#111" stroke-width=".4"/>'); txt(X100 + 9, Y99 - 6.2, 'C°', 2.4, 'middle')
contact(X100 + 4, Y99); contact(X100 + 14, Y99)
inner([(X100, Y99), (X100 + 3.2, Y99)]); inner([(X100 + 14.8, Y99), (X100 + 18, Y99)])
blade(X100 + 4.6, Y99 - .4, X100 + 13.4, Y99 - 2.6, grey=True)                  # open: probably (opens when warm)
name(X100, Y99 + 8.5, '100', 'Thermostat contact', size=2.4)
wire('233', [(X99 + 14, Y99), (X100, Y99)], X99 + 15.5, Y99 - 1.3)
A(f'<path d="M{X100 + 18},{Y99} h5" stroke="#111" stroke-width=".6" fill="none"/>'); earth(X100 + 23, Y99)
T(X99, Y99); T(X99 + 14, Y99); T(X100, Y99); T(X100 + 18, Y99)

# ---- dots on top of the wires -----------------------------------------------------------------------------------------
for n in (2, 25): contact(PX(n), PY)       # pins with nothing on them
for x, y in DOTS: dot(x, y)

# ---- legend and notes ----------------------------------------------------------------------------------------------
lx, ly = 12, 249
box(lx, ly, 206, 36, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 4
size_legend(x, ly + 17)
A(f'<path d="M{x},{ly + 22} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, ly + 23, 'traced (cable no. read)', 2.4)
# the samples a sheet uses only when it draws them, in a column right of the traced sample: not traced, ends on
# diagram (a stub), checked on the car (a tick: once check E1 has 218 and 231 checked, wire() prints ticks here)
sx = x + 48
for yy, kind in zip((ly + 23, ly + 28, ly + 33), [k for k, f in (('dashed', DASHED[0]), ('stub', STUB[0]), ('tick', TICKED[0])) if f]):
    if kind == 'dashed':
        A(f'<path d="M{sx},{yy - 1} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(sx + 11, yy, 'not traced yet', 2.4)
    elif kind == 'stub':
        A(f'<path d="M{sx},{yy - 1} h7" stroke="#222" stroke-width=".8"/><circle cx="{sx + 8.3}" cy="{yy - 1}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
        txt(sx + 11, yy, 'ends on diagram', 2.4)
    else:
        tick(sx + 3, yy - .7); txt(sx + 11, yy, 'checked on the car', 2.4)
probable_legend(x, ly + 28)
notes = ['The master relay switches on with the ignition (181) and feeds the control unit (216, 224)',
         'and the pump relay’s coil; the control unit runs the pump through the pump relay (219).',
         'The cold-start valve gets current only while the starter turns (starter line, 231),',
         'through its thermostat contact, which opens when warm.',
         '59 cold start: where on the starter line it sits is still to be checked (check E1).',
         'Throttle switch: the full-load contact (14) probably closes only near full throttle.',
         'Terminal marks in light grey: probably. Cylinder numbers: probably.']
for j, n in enumerate(notes): txt(lx + 102, ly + 5 + j * 3.9, n, 2.3, fill='#333')
save('injection.svg')

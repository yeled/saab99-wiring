#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo power-distribution sheet (A3 landscape SVG).

Battery, starter, alternator, ignition switch, ignition switch relay and the
fuse box, with every fuse output tagged with where it goes; the horns on fuse 3
and earth joint 158, where the earth returns of several circuits meet. Wire
identity, colour, size and status come from data/wires.csv.
"""
import math
from common import *

STUB = [False]              # set when this sheet draws a stub (open circle); the legend shows that sample only then
def wire(cable, *a, _wire=wire, **k):
    STUB[0] |= WIRES[cable]['status'] == 'stub'
    _wire(cable, *a, **k)

header('Saab 99 Turbo, model 1979 — Power distribution',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual.')

BX = 150                                   # x of the fuse supply bars
HX = 322                                   # left face of horn 40 (E1), where 117 RD from fuse 3 ends

# ---- fuse box: three supply bars, twelve fuses, outputs tagged -----------
OUTS = {1: ['42', '43'], 2: ['44', '45'], 3: ['117', '135'], 4: ['85', '85a', '85b'],
        5: ['380', '140', '380a', '220'], 6: ['103'], 7: ['110', '113'], 8: ['210'], 9: ['126'],
        10: ['260'], 11: ['70'], 12: ['131']}
r = 0; first_row = {}
for n in range(1, 13):
    first_row[n] = r; r += len(OUTS[n])
def rowy(r): return 66 + 9 * r + (9 if r >= first_row[3] else 0) + (9 if r >= first_row[7] else 0)   # a gap above bars 3–6 and 7–12
DEST = {'42': '14/15 L rear lamps: tail + plate', '43': '13 L front parking light',
        '44': '14/15 R rear lamps: tail + plate', '45': '13 R front parking light',
        '135': '31 Reversing light switch (via connector 58)',
        '85': '61 Wiper switch', '85a': '62 Wiper motor, terminal 4', '85b': '83 Wiper interval relay, terminal 15',
        '380': '140 speed transmitter, fuel boost (ignition sheet)', '140': '64 Seat heating, via 58 (E12) and 59 (interior sheet)',
        '380a': '137 throttle valve switch, fuel boost', '220': '117 corner lamp switch (lighting sheet)',
        '103': '35 Ventilator fan switch',
        '110': '38 Radiator fan relay 30/51', '113': '38 Radiator fan relay 86 (coil)',
        '210': '113 Heated rear window relay 30', '126': 'lighter, clock, interior light (160 GL)',
        '260': '102 Fuel pump relay 30', '70': '23 Indicator/hazard flasher unit 49', '131': '29 Brake light switch'}
NOTE = {'42': 'lighting sheet', '43': 'lighting sheet', '44': 'lighting sheet', '45': 'lighting sheet'}
BARS = [(1, 2, 'Bar 1–2 · parking and tail lights, fed from light switch 4'),
        (3, 6, 'Bar 3–6 · live with ignition on, fed from relay 21'),
        (7, 12, 'Bar 7–12 · always live, fed from battery / alternator')]
txt(147, 53, '22', 4, w='bold'); txt(154, 53, 'Fuse box', 2.7)
for a, b, title in BARS:
    y0, y1 = rowy(first_row[a]) - 4, rowy(first_row[b] + len(OUTS[b]) - 1) + 4
    if b == 12: y1 = 281                      # down to where 5 and 5a come in from the alternator
    A(f'<path d="M{BX},{y0} V{y1}" stroke="#111" stroke-width="1.6"/>')
    txt(156, rowy(first_row[a]) - 6.5, title, 2.6, w='bold')
for n, outs in OUTS.items():
    ys = [rowy(first_row[n] + i) for i in range(len(outs))]
    y = ys[0]
    A(f'<path d="M{BX},{y} H156 M170,{y} H176" stroke="#111" stroke-width=".6"/>')
    fuse(156, y - 2, 14, 4)
    txt(163, y - 3.2, fuse_label(n), 2.4, 'middle')
    if fuse_checked(n): tick(170.4, y - 2.6, s=0.9)
    if len(ys) > 1: A(f'<path d="M176,{ys[0]} V{ys[-1]}" stroke="#111" stroke-width=".6"/>')
    for cab, yy in zip(outs, ys):
        dot(176, yy)
        if cab == '117':                                   # runs on to the horns (drawn below), no tag
            HORN_Y = yy; wire(cab, [(176, yy), (HX, yy)], 180, yy - 1.5); continue
        wire(cab, [(176, yy), (230, yy)], 180, yy - 1.5)
        st = WIRES[cab]['status']
        end = tag(232 if st == 'stub' else 230, yy, '→ ' + DEST[cab], dashed=(st == 'open'))
        if cab in NOTE: txt(end + 2.5, yy + 1, NOTE[cab], 2.3, fill='#666')

# ---- ignition switch 20 and connector 58 ---------------------------------
# The lock as book photo P8 prints it (the p.407 scan and the 1980 print on p.411 agree): a round housing, a heavy key
# rotor across it on a star hub, shown at rest (level), fed from 30 by a line into its underside; its other positions
# dashed (a U-ended outline up one side, three short outline pairs below the hub). 54 runs over the top to a contact
# just above the hub; a contact above that is linked to one at the upper corner; a heavy arc below the hub is joined to
# X. The print puts 54 upper left, 30 left, X at the bottom, 15 right and 50 upper right; drawn mirrored here (as relay
# 21) so four leads reach the bottom-edge terminals in order and 54's crosses only 30 and X; X comes straight up into
# the ring's lower side (not the bottom) so 54 crosses it well clear of the lock. 15's diagonal runs straight on to the
# upper corner contact, and 50's lead crosses it to the side contact beside the hub; on the print they meet in one blot
# (photo, p.407, p.411), so both links past the crossing are grey. This reading lets the straight rotor close 15 + 54
# on one ray (90 deg: on) and 15 + 50 on the other (45 deg: start); the other way round, 50 would be live whenever 54
# is. Coordinates: book-photo px about the lock centre (ring inside radius 175).
box(18, 36, 44, 28)
txt(18, 33.4, '20', 4, w='bold'); txt(25, 33.4, 'Ignition switch', 2.7)
IG = {'50': 23, '15': 32, '54': 41, 'X': 50, '30': 57}
LX, LY, LR = 44, 46.5, 9                                   # lock centre and radius (mm)
S = LR / 175
def Q(x, y): return (round(LX - x * S, 2), round(LY + y * S, 2))          # book px (x right, y down), mirrored
def P(a, r=LR): return (round(LX + r * math.cos(math.radians(a)), 2), round(LY - r * math.sin(math.radians(a)), 2))
def short(p, q, d=.8):
    """p moved d towards q: a lead stopping at a contact circle's edge."""
    L = math.dist(p, q); return (round(p[0] + (q[0] - p[0]) * d / L, 2), round(p[1] + (q[1] - p[1]) * d / L, 2))
A(f'<circle cx="{LX}" cy="{LY}" r="{LR}" fill="#fff" stroke="#111" stroke-width=".6"/>')        # housing
a0, a1 = P(210, 5.7), P(328, 5.7)                                          # X arc under the hub (book: 212°-330°)
A(f'<path d="M{a0[0]},{a0[1]} A5.7,5.7 0 0 0 {a1[0]},{a1[1]}" fill="none" stroke="#111" stroke-width="1"/>')
RB = 126 * S                                                               # rotor half-length (book 135; kept clear of 15)
for a in (225, 270, 315):                                                  # the rotor's other positions, below:
    ux, uy = math.cos(math.radians(a)), -math.sin(math.radians(a))         # one mlink dash a side, as printed
    for k in (-.6, .6):
        mlink([(LX + 3.4 * ux - k * uy, LY + 3.4 * uy + k * ux), (LX + 4.2 * ux - k * uy, LY + 4.2 * uy + k * ux)])
ux, uy = math.cos(math.radians(45)), -math.sin(math.radians(45))           # and its U-ended outline (book: upper left),
r0 = RB - 4                                                                # arms 4 mm so the dashes fall evenly
mlink([(LX + r0 * ux + .6 * uy, LY + r0 * uy - .6 * ux), (LX + RB * ux + .6 * uy, LY + RB * uy - .6 * ux),
       (LX + RB * ux - .6 * uy, LY + RB * uy + .6 * ux), (LX + r0 * ux - .6 * uy, LY + r0 * uy + .6 * ux)])
b0, b1 = Q(126, 0), Q(-126, 0)
A(f'<path d="M{b0[0]},{b0[1]} L{b1[0]},{b1[1]}" stroke="#111" stroke-width="1.1"/>')                # key rotor, at rest
A('<path d="' + 'M' + ' L'.join(f'{round(LX + (1.6 if i % 2 == 0 else .7) * math.cos(math.pi * i / 8), 2)},'
  f'{round(LY - (1.6 if i % 2 == 0 else .7) * math.sin(math.pi * i / 8), 2)}' for i in range(16)) + ' Z" fill="#111"/>'
  f'<circle cx="{LX}" cy="{LY}" r=".3" fill="#fff"/>')                     # star hub
C54, CT, CB, CP = Q(-3, -63), Q(-3, -115), Q(82, -82), Q(48, -52)         # contacts: 54, top, upper corner, side
Y54 = LY + 10.3                                                            # 54's run under the lock
AX = 360 - math.degrees(math.acos((IG['X'] - LX) / LR))                    # where X's riser meets the ring
inner([(IG['30'], 64), (IG['30'], P(348)[1]), P(348), Q(-60, 11)])        # 30 into the rotor's underside
inner([(IG['54'], 64), (IG['54'], Y54), (59.5, Y54), (59.5, P(33)[1]), P(33), Q(-80, -130), short(C54, Q(-80, -130))])
inner([(IG['X'], 64), P(AX), P(300, 5.7)])                                 # X up to the arc
inner([short(CT, CB), short(CB, CT)])                                      # top contact to the upper corner one
inner([(IG['15'], 64), (IG['15'], P(197)[1]), P(197), (Q(152, 0)[0], P(197)[1]), Q(152, -23), Q(124, -46)])
inner([Q(124, -46), short(CB, Q(124, -46))], grey=True)                     # 15 on to the upper corner contact
inner([(IG['50'], 64), (IG['50'], P(143)[1]), P(143)])
inner([P(143), Q(97, -42), short(CP, Q(97, -42))], grey=True)               # 50 across 15 to the side contact
for c in (C54, CT, CB, CP): contact(*c)
for k, x in IG.items(): dot(x, 64); txt(x + 1, 62.6, k, 2.4)
for i, s in enumerate(('terminal names from the manual’s switch table (PDF p. 375)',   # two notes: a gap after 1
                       'lock as book photo P8 prints it, mirrored; key rotor at rest,',
                       'fed from 30; dashed: its other positions. Grey: 15 on to the corner',
                       'contact, 50 across it to the side one; they meet in one blot (photo, scan)')):
    txt(64.5, 39.5 + 3.3 * i + (1.2 if i else 0), s, 2.2, fill='#555')
A('<rect x="64" y="70" width="4" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(64, 74); dot(68, 74)
txt(66, 68.5, '58', 2.4, 'middle', w='bold')
wire('7', [(57, 64), (57, 74), (64, 74)], label=False)
Y7, Y10 = rowy(first_row[7]) - 2.5, rowy(first_row[7]) + 1.5   # 7 and 10 GR land on bar 7–12 just below its top
wire('7', [(68, 74), (142, 74), (142, Y7), (BX, Y7)], 140.4, 176, rot=-90)
wire('40', [(68, 74), (72, 79), (84, 79)], label=False); tag(84, 79, '40 GR 1.0 → 10 Light switch 3')
wire('30', [(50, 64), (50, 87), (84, 87)], label=False); dot(50, 87); tag(84, 87, '30 RD 1.0 → 10 Light switch 2')
wire('340', [(50, 87), (50, 95), (84, 95)], label=False); tag(84, 95, '340 RD 0.75 → 122 radio (radio sheet)')
wire('123', [(32, 64), (32, 161), (40, 161)], label=False); tag(40, 161, '15: 123 GN/VT 1.5 → 147 ballast resistor, coil (ignition sheet)')
wire('122', [(23, 64), (23, 169), (40, 169)], label=False); tag(40, 169, '50: 122 GL 2.5 → 89 start relay (ignition sheet)')

# ---- ignition switch relay 21 --------------------------------------------
# The manual (IMG_4720) prints 87 and 86 on the top edge, 30/51 and 85 below them, contact left, coil right.
# Here the terminals sit on the side walls with the coil pair on the left, so the internals are its mirror image.
box(80, 108, 34, 32)
txt(80, 105, '21', 4, w='bold'); txt(87, 105, 'Ignition switch relay (B6)', 2.7)
cl, cr, ct, cb = coil(82, 121, 15, 6)                      # coil 86-85
inner([(80, 116), (ct[0], 116), ct]); inner([cb, (cb[0], 134), (80, 134)])
contact(106, 119.5); inner([(114, 116), (106, 116), (106, 118.7)])        # 87: fixed contact
contact(106, 130); inner([(114, 134), (106, 134), (106, 130.8)])          # 30/51: blade pivot
blade(106.4, 129.3, 109.3, 120.6)                                          # make contact 30/51-87, open at rest
mlink([cr, (107.3, cr[1])])
for (x, y, k, a) in ((80, 116, '86', 'start'), (80, 134, '85', 'start'), (114, 116, '87', 'end'), (114, 134, '30/51', 'end')):
    dot(x, y); tlabel(x + (1.6 if a == 'start' else -1.6), y - 1.3, k, a)
wire('12', [(41, 64), (41, 116), (80, 116)], 45, 114.5)
# 85 is earthed through relay 113 and earth joint 158 (drawn right), not locally. 263 SV joins it under 21's border in
# the manual (probably at 85), so it leaves the same terminal on a short diagonal, inside the turn of 33 SV.
wire('33', [(80, 134), (38, 134), (38, 153), (40, 153)], 55, 132.5)
tag(40, 153, '→ 113:85 (climate sheet) → 212 SV → earth joint 158')
wire('263', [(80, 134), (77, 137), (77, 145), (79, 145)], label=False); tag(79, 145, '263 SV 0.75 ← 102:31 (ignition sheet)')
wire('11', [(114, 116), (BX, 116)], 117, 114.5)
wire('10', [(114, 134), (146, 134), (146, Y10), (BX, Y10)], 117, 132.5)
wire('94', [(BX, 180), (118, 180)], 120, 178.5); tag(116, 180, '→ 65 fuse holder, 3 A → 67 Headlight wiper relay', anchor='end')
wire('41', [(BX, 68), (118, 68)], 120, 66.5); tag(116, 68, '10 Light switch 4 (parking) →', anchor='end')
wire('20', [(BX, 216), (118, 216)], 120, 214.5); tag(116, 216, '→ 8 Lighting relay 30', anchor='end')
wire('280', [(BX, 225), (118, 225)], 120, 223.5); tag(116, 225, '→ 73 Service outlet', anchor='end')
wire('202', [(BX, 234), (118, 234)], 120, 232.5); tag(116, 234, '→ 89 Start relay 30', anchor='end')

# ---- battery, starter, alternator ----------------------------------------
# Laid out as the manual (IMG_4712) draws them: starter above the battery, 6 GR over to the alternator.
# The manual prints no internals for any of the three (no cells, solenoid, regulator or diodes), so none are drawn.
def shaft(x, y, pulley=False):
    """Pinion (starter) or pulley (alternator) on a left wall at (x, y): a black block on a short neck."""
    A(f'<rect x="{x - 1.6}" y="{y - 1.1}" width="1.6" height="2.2" fill="#111"/><rect x="{x - 1.2}" y="{y - .5}" width=".8" height="1" fill="#fff"/>')
    h = 10 if pulley else 6
    A(f'<rect x="{x - 4.6}" y="{y - h / 2}" width="3.2" height="{h}" rx=".8" fill="#111"/>')
    if pulley: A(f'<rect x="{x - 3.25}" y="{y - h / 2 + 1.4}" width=".5" height="{h - 2.8}" fill="#fff"/>')

box(20, 239, 26, 16); txt(23, 245.2, '4', 4, w='bold'); txt(28, 245.2, 'Starter', 2.7); shaft(20, 247)
for x, y, k, anc, lx_, ly_ in ((46, 243, '16', 'end', 44.4, 243.65), (46, 251, '50', 'end', 44.4, 251.65), (33, 255, '30', 'middle', 32.4, 253.3)):
    dot(x, y); tlabel(lx_, ly_, k, anc)
txt(22.6, 249.2, '16, 50: ignition sheet', 2.2, fill='#555')
box(38, 261, 26, 18); txt(46, 270.5, '1', 4, w='bold'); txt(51, 270.5, 'Battery', 2.7)
txt(40.4, 267.6, '+', 3.4); txt(61.6, 274.8, '−', 3.4, 'end')
d = 'M64,273.6 H68 V279'                   # battery −: extra heavy and black as printed, but no cable number, so not in wires.csv
A(f'<path d="{d}" fill="none" stroke="#222" stroke-width="1.7" stroke-linejoin="round"/><path d="{d}" fill="none" stroke="{COL["SV"]}" stroke-width="1.1" stroke-linejoin="round"/>')
earth(68, 279)
txt(64.5, 285, 'central earth star (D3): engine and body earth', 2.2, 'end', fill='#555')
box(96, 262, 26, 20); txt(99, 273.5, '2', 4, w='bold'); txt(104, 273.5, 'Alternator', 2.7); shaft(96, 272, pulley=True)
tlabel(120.4, 267.65, 'D+', 'end'); tlabel(120.4, 277.65, 'B+', 'end')
wire('1', [(33, 255), (33, 266.4), (38, 266.4)], 16.5, 262)
wire('6', [(33, 255), (36, 258), (126, 258), (126, 273), (122, 277)], 70, 256.5)
wire('195', [(122, 267), (136, 267), (136, 247), (134, 247)], label=False)   # crosses 6 GR, no join (as printed)
tag(134, 247, '195 RD 0.75 → 47 charge warning lamp (instruments sheet)', anchor='end')
wire('5', [(122, 277), (BX, 277)], 130, 275.5)
wire('5a', [(122, 277), (125, 280), (BX, 280)], 130, 284.2)
for x, y in ((33, 255), (38, 266.4), (64, 273.6), (122, 267), (122, 277)): dot(x, y)

# ---- horns 40 on fuse 3, horn switch 41 ----------------------------------
# As the manual draws them (IMG_4715 for E1, the scan for D1): a heavy square with an empty inner square and a flared
# trumpet, mirrored here so the leads enter from the left. No terminal names or internals are printed. The horns are in
# parallel with no relay: 117 RD feeds E1, 119 RD links the two feeds, 120 SV the two returns (crossing 117 RD with no
# join, as printed; D1's red lead is below its black one, as printed), and 118 SV takes the return through connector 58
# to horn switch 41, which earths it. At E1, 119 and 118 leave the horn itself on short diagonals (top and bottom
# corners in IMG_4715): no splice in 117 RD.
def horn(x, y, w=10, h=10):
    A(f'<path d="M{x + w},{y + 3} L{x + w + 8},{y - 1.5} L{x + w + 8},{y + h + 1.5} L{x + w},{y + h - 3} Z" fill="#fff" '
      f'stroke="#111" stroke-width=".9" stroke-linejoin="round"/>')
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#111"/><rect x="{x + 1.8}" y="{y + 1.8}" width="{w - 3.6}" '
      f'height="{h - 3.6}" fill="#fff"/>')
def plug(x, y, name):
    """One pin of connector 58 on a horizontal run: grey block with the pin's two ends, name above, pin below."""
    A(f'<rect x="{x}" y="{y - 4}" width="4" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(x, y); dot(x + 4, y)
    txt(x + 2, y - 5.7, name, 2.2, 'middle', w='bold'); txt(x + 2, y + 8.2, 'pin 1', 2.0, 'middle', fill='#555')
E1, D1 = HORN_Y - 3, HORN_Y - 25                           # box tops: + at 3 below the top on E1, − at 3 on D1
wire('119', [(HX, HORN_Y), (HX - 3, HORN_Y - 3), (HX - 3, D1 + 7), (HX, D1 + 7)], HX - 4.4, HORN_Y - 4, rot=-90)
wire('120', [(HX, E1 + 7), (306, E1 + 7), (306, D1 + 3), (HX, D1 + 3)], 304.6, HORN_Y - 2.5, rot=-90)
wire('118', [(HX, E1 + 7), (319, E1 + 10), (319, 128), (344, 128)], 321, 126.5)
horn(HX, E1); horn(HX, D1)
for y in (E1 + 3, E1 + 7, D1 + 3, D1 + 7): dot(HX, y)
txt(343, E1 + 6, '40', 3.4, w='bold'); txt(348.5, E1 + 6, 'Horn (E1)', 2.6)
txt(343, D1 + 6, '40', 3.4, w='bold'); txt(348.5, D1 + 6, 'Horn (D1)', 2.6)
txt(343, D1 + 14, 'in parallel, no horn relay: switched', 2.2, fill='#555')
txt(343, D1 + 17.2, 'on the earth side by horn switch 41', 2.2, fill='#555')
plug(344, 128, '58 (E2)'); wire('118', [(348, 128), (364, 128)], label=False)
plug(364, 128, '58 (D8)'); wire('118', [(368, 128), (378, 128)], label=False)
box(378, 123, 14, 10); txt(378, 120.8, '41', 3.4, w='bold'); txt(383.5, 120.8, 'Horn switch', 2.4); txt(397.5, 120.8, '(D8)', 2.2, fill='#555')
contact(382.5, 128); contact(387.5, 128); inner([(378, 128), (381.7, 128)]); inner([(388.3, 128), (392, 128)])
blade(383.1, 127.5, 386.8, 125.4)                          # horn push: open at rest
dot(378, 128); dot(392, 128)
A('<path d="M392,128 H397" stroke="#111" stroke-width=".6" fill="none"/>'); earth(397, 128)   # no cable number printed

# ---- earth joint 158 (D6) --------------------------------------------------
# The manual (IMG_4718, IMG_4720) prints six linked blocks, 2 rows x 3 columns, with no pin names; "158" beside them.
# Every cable sits on the block where the manual has it: T1 281 and 92, T2 3, T3 212 and 201, B3 90, 107, 192 and 83.
# Tags name where each cable comes from; 3 SV 2.5 goes to the central earth star, like the battery −.
TE = 367                                                   # right end of the tags
C1, C2, C3 = 377, 385, 393                                 # block columns
TY, BY = 243, 250                                          # block rows
for y in (TY, BY): A(f'<path d="M{C1},{y} H{C3}" stroke="#111" stroke-width=".6"/>')
for x in (C1, C2, C3): A(f'<path d="M{x},{TY} V{BY}" stroke="#111" stroke-width=".6"/>')
J = {'201': '201 SV 0.75 ← 89:85 start relay coil (ignition sheet)',
     '212': '212 SV 0.75 ← 113:85 heated rear window relay (climate sheet)',
     '281': '281 SV 1.5 ← 73 Service outlet, pin 2 (D4)',
     '92': '92 SV 1.0 ← 63 Washer pump (wipers sheet)',
     '90': '90 BL 1.0 ← 62 Wiper motor housing (wipers sheet)',
     '107': '107 SV 2.5 ← 36 Heater fan motor, via 57 (F11) (climate sheet)',
     '192': '192 SV 0.75 ← 42 Brake warning switch (E11)',
     '83': '83 SV 0.75 ← 83 Wiper interval relay (wipers sheet)'}
ROUTE = {'201': [(C3 + 2.5, TY), (C3 + 8, TY), (C3 + 8, 205), (TE, 205)],       # out of T3's side, up and back over
         '212': [(C3, TY - 1.5), (C3, 212), (TE, 212)],
         '281': [(C1 + 1.3, TY - 1.5), (C1 + 1.3, 229), (TE, 229)],
         '92': [(C1 - 1.3, TY - 1.5), (TE + 6, 236), (TE, 236)],                 # onto T1's left half on a diagonal
         '90': [(C3 - 2.5, BY + 1.5), (C3 - 4.5, BY + 5), (C3 - 4.5, 259), (TE, 259)],   # the fan below B3, left to right
         '107': [(C3, BY + 1.5), (C3, 266), (TE, 266)],
         '192': [(C3 + 2.5, BY + 1.5), (C3 + 4.5, BY + 5), (C3 + 4.5, 273), (TE, 273)],
         '83': [(C3 + 2.5, BY), (C3 + 11, BY + 4.5), (C3 + 11, 280), (TE, 280)]}       # shallow, off B3's lower right
for cab, pts in ROUTE.items():
    wire(cab, pts, label=False); tag(TE, pts[-1][1], J[cab], anchor='end')
wire('3', [(C2, TY - 1.5), (C2, 219), (TE + 6, 219), (TE + 6, 220.5)], label=False); earth(TE + 6, 220.5)
txt(TE - 35, 224.1, '3 SV 2.5 → central earth star (D3)', 2.4)   # ends just left of the earth bar; start-anchored: cairo misplaces 'end' text with an arrow tspan
for x in (C1, C2, C3):
    for y in (TY, BY): A(f'<rect x="{x - 2.5}" y="{y - 1.5}" width="5" height="3" rx=".5" fill="#111"/>')
txt(C1 - 37, 248.2, '158', 4, w='bold'); txt(C1 - 28.5, 248.2, 'Earth joint (D6)', 2.7)   # number first, as for every part
txt(C1 - 37, 252.6, 'six linked blocks: one earth point', 2.2, fill='#555')

# ---- legend --------------------------------------------------------------
lx, ly = 250, 30
box(lx, ly, 157, 25, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 97
A(f'<path d="M{x},{ly + 5} h9" stroke="#222" stroke-width="1.2"/>'); txt(x + 11, ly + 6, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x},{ly + 10} h9" stroke="#222" stroke-width="1.2" stroke-dasharray="3 2"/>'); txt(x + 11, ly + 11, 'not traced yet', 2.4)
if STUB[0]:
    A(f'<path d="M{x},{ly + 15} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{ly + 15}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    txt(x + 11, ly + 16, 'ends on diagram', 2.4)
if TICKED[0]:                              # beside the stub sample, or in its place when the sheet has no stub
    tx, gx = (x + 33, x + 37) if STUB[0] else (x + 3, x + 11)
    tick(tx, ly + 15.3); txt(gx, ly + 16, 'checked on the car', 2.4)
probable_legend(lx + 4, ly + 15.5)
txt(lx + 4, ly + 21.5, 'Not RHD-specific: circuits should match, but harness routing and part positions may differ.', 2.3, fill='#333')
save('power.svg')

#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo power-distribution sheet (A3 landscape SVG).

Battery, starter, alternator, ignition switch, ignition switch relay and the
fuse box, with every fuse output tagged with where it goes. Wire identity,
colour, size and status come from data/wires.csv.
"""
from common import *

header('Saab 99 Turbo, model 1979 — Power distribution',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual.')

BX = 150                                   # x of the fuse supply bars
def rowy(r): return 66 + 9 * r + (9 if r >= 4 else 0) + (9 if r >= 13 else 0)

# ---- fuse box: three supply bars, twelve fuses, outputs tagged -----------
OUTS = {1: ['42', '43'], 2: ['44', '45'], 3: ['117', '135'], 4: ['85', '85a', '85a#relay'],
        5: ['380', '140', '380a'], 6: ['103'], 7: ['110', '113'], 8: ['210'], 9: ['126'],
        10: ['260'], 11: ['70'], 12: ['131']}
DEST = {'42': '14/15 L rear lamps: tail + plate', '43': '13 L front parking light',
        '44': '14/15 R rear lamps: tail + plate', '45': '13 R front parking light',
        '117': '40 Horns', '135': '31 Reversing light switch (via connector 58)',
        '85': '61 Wiper switch', '85a': '62 Wiper motor, terminal 4', '85a#relay': '83 Wiper interval relay',
        '380': '140 speed transmitter, fuel boost (ignition sheet)', '140': '64 Seat heating, via 58 (E12) and 59 (interior sheet)',
        '380a': '137 throttle valve switch, fuel boost', '103': '35 Ventilator fan switch',
        '110': '38 Radiator fan relay 30/51', '113': '38 Radiator fan relay 86 (coil)',
        '210': '113 Heated rear window relay 30', '126': 'lighter, clock, interior light (160 GL)',
        '260': '102 Fuel pump relay 30', '70': '23 Indicator/hazard flasher unit 49', '131': '29 Brake light switch'}
NOTE = {'42': 'lighting sheet', '43': 'lighting sheet', '44': 'lighting sheet', '45': 'lighting sheet'}
BARS = [(1, 2, 'Bar 1–2 · parking and tail lights, fed from light switch 4'),
        (3, 6, 'Bar 3–6 · live with ignition on, fed from relay 21'),
        (7, 12, 'Bar 7–12 · always live, fed from battery / alternator')]
txt(147, 53, '22', 4, w='bold'); txt(154, 53, 'Fuse box', 2.7)
r = 0; first_row = {}
for n in range(1, 13):
    first_row[n] = r; r += len(OUTS[n])
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
        wire(cab, [(176, yy), (230, yy)], 180, yy - 1.5)
        st = WIRES[cab]['status']
        end = tag(232 if st == 'stub' else 230, yy, '→ ' + DEST[cab], dashed=(st == 'open'))
        if cab in NOTE: txt(end + 2.5, yy + 1, NOTE[cab], 2.3, fill='#666')

# ---- ignition switch 20 and connector 58 ---------------------------------
box(18, 36, 44, 28)
txt(21, 42.5, '20', 4, w='bold'); txt(28, 42.5, 'Ignition switch', 2.7)
txt(21, 47, 'terminal names from the manual’s', 2.2, fill='#555'); txt(21, 50.3, 'switch table (PDF p. 375)', 2.2, fill='#555')
IG = {'50': 23, '15': 32, '54': 41, 'X': 50, '30': 57}
for k, x in IG.items(): dot(x, 64); txt(x, 62, k, 2.4, 'middle')
A('<rect x="64" y="70" width="4" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(64, 74); dot(68, 74)
txt(66, 68.5, '58', 2.4, 'middle', w='bold')
wire('7', [(57, 64), (57, 74), (64, 74)], label=False)
wire('7', [(68, 74), (142, 74), (142, 199), (BX, 199)], 140.4, 176, rot=-90)
wire('40', [(68, 74), (72, 79), (84, 79)], label=False); tag(84, 79, '40 GR 1.0 → 10 Light switch 3')
wire('30', [(50, 64), (50, 87), (84, 87)], label=False); dot(50, 87); tag(84, 87, '30 RD 1.0 → 10 Light switch 2')
wire('340', [(50, 87), (50, 95), (84, 95)], label=False); tag(84, 95, '340 RD 0.75 → 122 radio (radio sheet)')
wire('123', [(32, 64), (32, 152), (40, 152)], label=False); tag(40, 152, '15: 123 GN/VT 1.5 → 147 ballast resistor, coil (ignition sheet)')
wire('122', [(23, 64), (23, 164), (40, 164)], label=False); tag(40, 164, '50: 122 GL 2.5 → 89 start relay (ignition sheet)')

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
wire('33', [(80, 134), (72, 134), (72, 140)], 55, 132.5); earth(72, 140)
wire('11', [(114, 116), (BX, 116)], 117, 114.5)
wire('10', [(114, 134), (146, 134), (146, 203), (BX, 203)], 117, 132.5)
wire('94', [(BX, 180), (118, 180)], 120, 178.5); tag(116, 180, '→ 65 fuse holder, 3 A → 67 Headlight wiper relay', anchor='end')
wire('41', [(BX, 68), (118, 68)], 120, 66.5); tag(116, 68, '10 Light switch 4 (parking) →', anchor='end')
wire('20', [(BX, 214), (118, 214)], 120, 212.5); tag(116, 214, '→ 8 Lighting relay 30', anchor='end')
wire('280', [(BX, 224), (118, 224)], 120, 222.5); tag(116, 224, '→ 73 Service outlet', anchor='end')
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

# ---- legend --------------------------------------------------------------
lx, ly = 250, 262
box(lx, ly, 157, 25, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 97
A(f'<path d="M{x},{ly + 5} h9" stroke="#222" stroke-width="1.2"/>'); txt(x + 11, ly + 6, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x},{ly + 10} h9" stroke="#222" stroke-width="1.2" stroke-dasharray="3 2"/>'); txt(x + 11, ly + 11, 'not traced yet', 2.4)
A(f'<path d="M{x},{ly + 15} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{ly + 15}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
txt(x + 11, ly + 16, 'ends on diagram', 2.4)
if TICKED[0]: tick(x + 33, ly + 15.3); txt(x + 37, ly + 16, 'checked on the car', 2.4)
probable_legend(lx + 4, ly + 15.5)
txt(lx + 4, ly + 21.5, 'Not RHD-specific: circuits should match, but harness routing and part positions may differ.', 2.3, fill='#333')
save('power.svg')

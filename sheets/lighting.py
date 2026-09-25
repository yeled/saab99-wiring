#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo lighting sheet (A3 landscape SVG).

Layout lives here; wire identity, colour, size and status come from
data/wires.csv, so editing the CSV (e.g. status -> car) updates the drawing.
"""
from common import *

header('Saab 99 Turbo, model 1979 — Lighting circuit',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual. Front of car at left; car’s right side at top.')
txt(16, 40, 'FRONT', 3.6, w='bold', fill='#777'); txt(398, 97, 'REAR', 3.6, 'end', w='bold', fill='#777')

# ---- front lamps -------------------------------------------------------
hx = 45
lamp(hx, 72, '11/12 Headlamp R'); lamp(hx, 125, '13 Parking R')
lamp(hx, 178, '13 Parking L'); lamp(hx, 240, '11/12 Headlamp L')
for y in (72, 240):
    A(f'<path d="M{hx + 4.5},{y - 3} h1 M{hx + 4.5},{y + 3} h1" stroke="#111" stroke-width=".5"/>')
wire('29', [(hx - 4.5, 72), (hx - 13, 72), (hx - 13, 78)], hx - 31, 70); earth(hx - 13, 78)
wire('115', [(hx - 4.5, 240), (hx - 13, 240), (hx - 13, 246)], hx - 34, 238); earth(hx - 13, 246)
lamp_earth(hx - 4.5, 125); lamp_earth(hx - 4.5, 178)

# ---- lighting relay 8 --------------------------------------------------
rx, ry, rw, rh = 150, 195, 48, 40
box(rx, ry, rw, rh)
txt(rx + 12, ry + 5.5, '8', 4.2, w='bold'); txt(rx + 17, ry + 5.5, 'Lighting relay (C7)', 2.7)
txt(rx + 12, ry + 9.5, 'latching dip/main + flash', 2.3, fill='#555')
for y, l in ((ry + 10, '56a'), (ry + 25, '56b')):
    dot(rx, y); txt(rx + 2, y + 1, l, 2.5)
bt = {'S': rx + 10, '31': rx + 21, '86': rx + 32, '30': rx + 42}
for k, x in bt.items():
    dot(x, ry + rh); txt(x, ry + rh - 2, k, 2.5, 'middle')
a56, b56 = ry + 10, ry + 25
wire('26', [(hx + 5.5, 69), (120, 69), (120, a56), (rx, a56)], 58, 67)
wire('24', [(hx + 5.5, 75), (114, 75), (114, b56), (rx, b56)], 58, 81)
wire('25', [(132, a56), (132, 237), (hx + 5.5, 237)], 58, 235)
wire('23', [(126, b56), (126, 243), (hx + 5.5, 243)], 58, 249)
wire('27', [(138, a56), (138, 149), (150, 149)], 136.6, 202, rot=-90)
for x, y in ((132, a56), (138, a56), (126, b56)): dot(x, y)
box(150, 141, 46, 16)
lamp(158, 149, r=3.2); txt(164, 147, '47 Instrument', 2.6, w='bold'); txt(164, 151, 'main-beam', 2.3); txt(164, 154.4, 'warning lamp', 2.3)
wire('13', [(bt['31'], ry + rh), (bt['31'], ry + rh + 8)], 163, 254.5); earth(bt['31'], ry + rh + 8)
wire('32', [(bt['S'], ry + rh), (bt['S'], 264)], 141.5, 259)
box(140, 264, 58, 18)
txt(143, 269.5, '9', 4, w='bold'); txt(148, 269.5, 'Dip/flash stalk (F9)', 2.7)
txt(143, 274, 'pulse on S toggles dip/main;', 2.3, fill='#555'); txt(143, 277.3, 'flash works with ignition off', 2.3, fill='#555')

# ---- light switch 10 ---------------------------------------------------
sx, sy, sw_, sh = 222, 50, 50, 24
box(sx, sy, sw_, sh)
txt(sx + 25, sy + 10, '10  Light switch', 3, 'middle', w='bold'); txt(sx + 25, sy + 14, '(C8) off / parking / headlamps', 2.3, 'middle', fill='#555')
T = {'2': (232, sy), '3': (262, sy), '1': (232, sy + sh), '4': (262, sy + sh)}
for k, (x, y) in T.items():
    dot(x, y); txt(x + 1.8, y + (3.5 if y == sy else -1.5), k, 2.5)
wire('31', [(bt['86'], ry + rh), (bt['86'], 250), (232, 250), T['1']], 196, 248)
wire('20', [(bt['30'], ry + rh), (bt['30'], 258), (236, 258), (236, 96), (244, 96)], 200, 256)
wire('30', [T['2'], (232, 36), (318, 36)], 240, 34)
wire('40', [T['3'], (262, 42), (312, 42), (318, 48)], 268, 40)
wire('41', [T['4'], (262, 80), (304, 80), (304, 150), (290, 150)], 266.5, 78.2)

# ---- fuse box 22 -------------------------------------------------------
box(240, 88, 60, 108)
A('<path d="M244,96 H286" stroke="#111" stroke-width="1.6"/>')
txt(246, 102, 'Supply bar, fuses 7–12: always live', 2.3); txt(246, 105.4, 'fed from battery via 5 GR 4.0 + 5a GR 2.5', 2.3, fill='#555')
wire('7', [(286, 96), (310, 96), (310, 48), (318, 48)], 313, 90, rot=-90)
for fy, n in ((125, '2'), (178, '1')):
    A(f'<rect x="262" y="{fy - 2}" width="18" height="4" fill="#fff" stroke="#111" stroke-width=".5"/>')
    A(f'<path d="M262,{fy} h18 M255,{fy} h7 M280,{fy} h10" stroke="#111" stroke-width=".5"/>')
    dot(255, fy); txt(271, fy - 3.5, fuse_label(int(n), 'Fuse '), 2.5, 'middle')
    if fuse_checked(int(n)): tick(280.8, fy - 4.0)
A('<path d="M290,125 V178" stroke="#111" stroke-width=".6"/>'); dot(290, 150)
txt(297, 190, '22  Fuse box', 3, 'end', w='bold'); txt(297, 193.8, '(fuses 1–2 and bar 7–12 shown)', 2.2, 'end', fill='#555')
wire('45', [(255, 125), (hx + 4.5, 125)], 58, 123)
wire('43', [(255, 178), (hx + 4.5, 178)], 58, 176)
wire('44', [(255, 125), (255, 116), (357, 116)], 314, 114)
wire('42', [(255, 178), (255, 186), (357, 186)], 314, 184)

# ---- connector 58 + ignition switch 20 --------------------------------
A('<rect x="318" y="30" width="6" height="24" fill="#ddd" stroke="#111" stroke-width=".6"/>')
for y in (36, 48): dot(318, y); dot(324, y)
txt(321, 28, '58', 3, 'middle', w='bold'); txt(321, 58, '12-pole connector', 2.2, 'middle', fill='#555')
wire('30', [(324, 36), (345, 36)], label=False)
wire('7', [(324, 48), (345, 48)], label=False)
box(345, 28, 52, 28)
txt(349, 37, 'X', 2.6); txt(349, 49, '30', 2.6)
txt(358, 36, '20  Ignition switch', 3, w='bold'); txt(358, 41, '30: battery in (grey)', 2.3, fill='#555')
txt(358, 45, 'X: live with key on (red)', 2.3, fill='#555'); txt(358, 49.5, 'per manual, PDF p. 375', 2.3, fill='#555')

# ---- rear clusters -----------------------------------------------------
def cluster(y0, side, feed_y, stubs):
    box(357, y0, 43, 54, fill='#fdfdfd', sw=.6)
    txt(378.5, y0 - 2, f'Rear lamp cluster {side}', 2.6, 'middle')
    ys = (y0 + 10, y0 + 26, y0 + 42)
    A(f'<path d="M364,{ys[0]} V{ys[2]}" stroke="#111" stroke-width=".6"/>')
    for yy, cap in zip(ys, ('14 tail', '14 tail', '15 plate')):
        dot(364, yy); A(f'<path d="M364,{yy} H374" stroke="#111" stroke-width=".6"/>')
        lamp(378.5, yy, cap, cx=378.5, cy=yy + 8.3)
        A(f'<path d="M383,{yy} H392" stroke="#111" stroke-width=".6"/>')
    A(f'<path d="M392,{ys[0]} V{y0 + 54}" stroke="#111" stroke-width=".6"/>'); earth(392, y0 + 54)
    A(f'<path d="M357,{feed_y} H364" stroke="#111" stroke-width=".6"/>')
    for cab, yy, ly in stubs:
        wire(cab, [(364, yy), (342, yy)], 322 if len(cab) < 3 else 320, ly)
        dot(364, yy)
cluster(106, 'R', 116, [('47', 124, 125.5), ('47a', 148, 149.5)])
cluster(176, 'L', 186, [('46', 194, 195.5), ('46a', 218, 219.5)])

# ---- legend ------------------------------------------------------------
lx, ly = 250, 240
box(lx, ly, 157, 47, fill='#fff', sw=.5)
txt(lx + 3, ly + 5.5, 'Cable key: number · colour · mm²', 3, w='bold')
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 11 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x, y = lx + 97, ly + 11
A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="1.2"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x},{y + 4} h9" stroke="#222" stroke-width="1.2" stroke-dasharray="3 2"/>'); txt(x + 11, y + 5, 'not traced yet', 2.4)
A(f'<path d="M{x},{y + 9} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{y + 9}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
txt(x + 11, y + 10, 'ends on diagram', 2.4)
if TICKED[0]: tick(x + 33, y + 9.3); txt(x + 37, y + 10, 'checked on the car', 2.4)
notes = ['Headlamps need the ignition on, parking/tail lights do not (manual, PDF p. 375, 413):',
         'light switch 2 is fed from ignition switch X, light switch 3 from the always-live bar.',
         'Headlamps are unfused: relay 30 is fed straight from the supply bar (20 GR 1.5).',
         'Not RHD-specific: circuits are per side, but harness routing and part positions may differ.',
         'Corner lamps (117/118) share the front lamp housing; separate circuit, not shown.']
for j, n in enumerate(notes): txt(lx + 3, ly + 26 + j * 4.2, n, 2.35, fill='#333')
save('lighting.svg')

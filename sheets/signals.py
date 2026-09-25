#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo signals sheet: indicators, hazards, brake and reversing lights (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Indicators, hazards, brake and reversing lights',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual. Dashed = not traced yet.')
def conn(x, y, h, lab):
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    txt(x, y - h / 2 - 1.5, lab, 2.2, 'middle', fill='#555')
def fuse_box(y, n):
    box(18, y - 7, 32, 14); txt(21, y - 1, f'<tspan font-weight="bold">F{n}</tspan> · {FUSES[n]["rating"]}', 2.6)
    txt(21, y + 3.8, {'1-2': 'parking bar', '3-6': 'ignition-on bar', '7-12': 'always-live bar'}[FUSES[n]['bar']], 2.1, fill='#555')
def lamp_r(x, y, cap):
    lamp(x, y, r=3.8); txt(x + 6, y + 1, cap, 2.6)
    A(f'<path d="M{x},{y + 3.8} v2" stroke="#111" stroke-width=".5"/>')

# ---- indicators and hazards ---------------------------------------------------
txt(18, 40, 'Indicators and hazards', 3.4, w='bold')
fuse_box(62, 11)
wire('70', [(50, 62), (62, 62)], label=False); txt(51, 58, '70 RD/VT 1.0', 2.2)
box(62, 50, 30, 30); txt(77, 65, '23', 3.2, 'middle', w='bold'); txt(77, 70, 'Flasher unit', 2.3, 'middle')
dot(62, 62); txt(64, 59.5, '49', 2.2); dot(92, 58); txt(90, 56.5, '49a', 2.2, 'end')
dot(72, 80); txt(72, 78, 'C', 2.2, 'middle'); dot(84, 80); txt(84, 78, '31', 2.2, 'middle')
A('<path d="M84,80 v5" stroke="#111" stroke-width=".6"/>'); earth(84, 85)
wire('71', [(72, 80), (72, 96)], label=False); tag(74, 96, '71 GN/VT 0.75 → 47 dash indicator lamp')
wire('73', [(92, 58), (130, 58)], 96, 56.5)
box(130, 48, 40, 40); txt(150, 76, '25', 3.2, 'middle', w='bold'); txt(150, 81, 'Hazard switch', 2.3, 'middle')
lamp(150, 64, r=3.2); dot(130, 58); dot(170, 58); dot(140, 88); dot(160, 88); txt(142, 86, 'L', 2.2); txt(162, 86, 'R', 2.2)
wire('52', [(170, 76), (178, 76), (178, 80)], label=False); earth(178, 80); dot(170, 76); txt(181, 79, '52 SV', 2.1)
wire('76#hazard', [(170, 58), (210, 58)], 172, 56.5)
box(210, 48, 30, 40); txt(225, 70, '24', 3.2, 'middle', w='bold'); txt(225, 75, 'Indicator', 2.3, 'middle'); txt(225, 78.5, 'switch', 2.3, 'middle')
dot(210, 58); txt(212, 59, '54', 2.2); dot(215, 88); dot(235, 88); txt(217, 86, 'L', 2.2); txt(237, 86, 'R', 2.2)
wire('67', [(140, 88), (140, 110), (215, 110)], 150, 108.5)
wire('68', [(160, 88), (160, 122), (235, 122)], 170, 120.5)
A('<path d="M215,88 V110 M235,88 V122" stroke="#111" stroke-width=".6"/>'); dot(215, 110); dot(235, 122)
wire('77', [(215, 110), (268, 110)], label=False); conn(270, 110, 7, '58 (B9)')
wire('77', [(272, 110), (310, 110), (310, 98), (340, 98)], 314, 96.5); dot(310, 110)
wire('76', [(310, 110), (340, 110)], 314, 108.5)
wire('80', [(235, 122), (268, 122)], label=False); conn(270, 122, 7, '')
wire('80', [(272, 122), (340, 122)], 314, 120.5); dot(318, 122)
wire('79', [(318, 122), (318, 134), (340, 134)], 321, 132.5)
lamp_r(344, 98, '27 Front indicator, left'); lamp_r(344, 110, '27 Rear indicator, left')
lamp_r(344, 122, '28 Front indicator, right'); lamp_r(344, 134, '28 Rear indicator, right')

# ---- brake and reversing lights ---------------------------------------------------
txt(18, 162, 'Brake and reversing lights', 3.4, w='bold')
fuse_box(183, 12)
wire('131', [(50, 183), (90, 183)], 55, 181.5)
box(90, 176, 24, 14); A('<path d="M94,186 l8,-6 M102,183 h8" stroke="#111" stroke-width=".5"/>'); txt(102, 173, '29 Brake light switch', 2.4, 'middle', w='bold')
wire('132', [(114, 183), (168, 183)], 120, 181.5); conn(170, 183, 7, '58 (E12)')
wire('133', [(172, 183), (310, 183)], 200, 181.5); dot(310, 183)
wire('133', [(310, 183), (310, 176), (340, 176)], label=False); wire('133', [(310, 183), (310, 190), (340, 190)], label=False)
lamp_r(344, 176, '30 Brake light, left'); lamp_r(344, 190, '30 Brake light, right')
fuse_box(217, 3)
wire('135', [(50, 217), (148, 217)], 55, 215.5); conn(150, 217, 7, '58 (E12)')
wire('135', [(152, 217), (190, 217)], label=False)
box(190, 210, 24, 14); A('<path d="M194,220 l8,-6 M202,217 h8" stroke="#111" stroke-width=".5"/>'); txt(202, 207, '31 Reversing light switch', 2.4, 'middle', w='bold')
wire('136', [(214, 217), (318, 217), (318, 210), (340, 210)], 230, 215.5); dot(318, 217)
wire('137', [(318, 217), (318, 224), (340, 224)], 321, 222.5)
lamp_r(344, 210, '32 Reversing light, left'); lamp_r(344, 224, '32 Reversing light, right')

# ---- legend and notes ---------------------------------------------------------------
lx, ly = 18, 250
box(lx, ly, 389, 37, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 4
A(f'<path d="M{x},{ly + 17} h9" stroke="#222" stroke-width="1.2"/>'); txt(x + 11, ly + 18, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x + 48},{ly + 17} h9" stroke="#222" stroke-width="1.2" stroke-dasharray="3 2"/>'); txt(x + 59, ly + 18, 'not traced yet', 2.4)
if TICKED[0]: tick(x, ly + 23.3); txt(x + 4, ly + 24, 'checked on the car', 2.4)
notes = ['The flasher is fed from fuse 11 on the always-live bar. Its output (73 GN) goes through the hazard switch to the indicator switch.',
         'With the hazards on, the hazard switch feeds both sides directly through 67 BL/VT (left) and 68 RD/VT (right).',
         'The hazard switch’s terminal numbers can’t be read. Its feed to the indicator switch is printed 76 GN, like the rear left indicator wire (76 BL/VT): a misprint.',
         'Rear indicator wires 76 and 79 leave connector 58 (B9) on its far side; their route to the rear isn’t traced yet.',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 5.8, n, 2.35, fill='#333')
save('signals.svg')

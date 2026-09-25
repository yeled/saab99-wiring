#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo wipers and washers sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Wipers and washers',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual. Dashed = not traced yet.')
def fuse_box(y, n):
    box(18, y - 7, 32, 14); txt(21, y - 1, f'<tspan font-weight="bold">F{n}</tspan> · {FUSES[n]["rating"]}', 2.6)
    txt(21, y + 3.8, 'ignition-on bar', 2.1, fill='#555')
def term(x, y, t, side):
    dot(x, y); txt(x + (1.8 if side == 'l' else -1.8), y + (-1.3 if side in 'lr' else 3.4), t, 2.2, 'start' if side == 'l' else 'end')
def motor(x, y, r=7):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(x, y + 1.2, 'M', 3, 'middle', w='bold')

txt(18, 40, 'Windscreen wipers and washer', 3.4, w='bold')
fuse_box(62, 4)
wire('85', [(50, 60), (120, 60)], 60, 58.5)
wire('85a', [(50, 66), (62, 66)], label=False); tag(64, 66, '85a BR 0.75 → relay 83, motor 62')
box(120, 50, 50, 64); txt(145, 106, '61 Wiper switch', 2.7, 'middle', w='bold'); txt(145, 110, '(D9)', 2.2, 'middle', fill='#555')
term(120, 60, '53a', 'l')
for t, y in (('86', 64), ('87', 72), ('84', 82), ('88', 92), ('91', 102)): dot(170, y)
wire('86', [(170, 64), (392, 64), (392, 95), (370, 95)], 206, 62.5)
wire('87', [(170, 72), (386, 72), (386, 89), (370, 89)], 206, 70.5)
wire('84', [(170, 82), (190, 82), (190, 130), (230, 130)], 196, 128.5)
wire('88', [(170, 92), (184, 92), (184, 142), (230, 142)], 196, 140.5)
wire('91', [(170, 102), (178, 102), (178, 154), (230, 154)], 196, 152.5)
box(230, 120, 42, 50); txt(251, 162, '83 Interval', 2.7, 'middle', w='bold'); txt(251, 166, 'relay (D8)', 2.7, 'middle', w='bold')
for y in (130, 142, 154): dot(230, y)
dot(251, 120); txt(253, 124, '85a', 2.2); wire('85a', [(251, 120), (251, 112)], label=False); tag(249, 112, '85a BR 0.75 ← fuse 4', anchor='end')
dot(272, 130); dot(272, 154)
wire('88a', [(272, 130), (382, 130), (382, 107), (370, 107)], 290, 128.5)
wire('91a', [(272, 154), (320, 154)], 280, 152.5)
dot(251, 170); wire('83', [(251, 170), (251, 176)], label=False); earth(251, 176); txt(255, 179, '83 SV 0.75', 2.2)
motor(327, 160); txt(337, 158, '63 Washer pump', 2.7, w='bold'); txt(337, 162.5, '(F4)', 2.2, fill='#555')
A('<path d="M320,154 v0" />'); wire('92', [(327, 167), (327, 172)], label=False); earth(327, 172); txt(331, 175, '92 SV 1.0', 2.2)
box(330, 84, 40, 30); motor(342, 99, 6); txt(350, 80.5, '62 Wiper motor (F4)', 2.7, 'middle', w='bold')
for t, y in (('3', 89), ('5', 95), ('4', 101), ('2', 107)): dot(370, y); txt(368, y + 1, t, 2.2, 'end')
dot(350, 114); txt(352, 112.5, '1', 2.2)
wire('89', [(350, 114), (350, 120)], label=False); earth(350, 120); txt(354, 123, '89 SV 0.75', 2.2)
txt(300, 137, '90 BL 1.0 also leaves the motor’s park side (not traced)', 2.1, fill='#777')
wire('85a', [(370, 101), (378, 101)], label=False); txt(380, 103.5, '85a', 2.1)

txt(18, 196, 'Headlight wipers', 3.4, w='bold')
box(18, 204, 34, 14); txt(21, 210, 'Bar 3–6', 2.6, w='bold'); txt(21, 214.5, 'ignition on, unfused', 2.1, fill='#555')
wire('94', [(52, 211), (96, 211)], 58, 209.5)
box(96, 204, 24, 14); txt(108, 210, '65', 2.6, 'middle', w='bold'); txt(108, 214.5, 'fuse holder, 3 A', 2.1, 'middle')
# relay 67 with its contacts and coil, in the rest position as the manual draws it
wire('95', [(120, 211), (128, 211), (128, 216), (140, 216)], label=False); txt(121, 220, '95 RD 0.75', 1.9, fill='#555'); dot(128, 216)
wire('95a', [(128, 216), (128, 192), (188, 192), (188, 211), (272, 211)], 194, 209.5); dot(230, 211)
box(140, 200, 40, 32); txt(160, 197.6, '67 Headlight wiper relay', 2.2, 'middle', w='bold')
for x, y, t, anc in ((140, 207, '87', 'start'), (140, 216, '88', 'start'), (180, 207, '87a', 'end'), (180, 216, '88a', 'end')):
    dot(x, y); txt(x + (2 if anc == 'start' else -2), y - 1.3, t, 1.8, anc, fill='#555')
dot(150, 232); txt(151.5, 230.6, '85', 1.8, fill='#555'); dot(170, 232); txt(168.5, 230.6, '86', 1.8, 'end', fill='#555')
A('<path d="M140,207 H147.2 M140,216 H147.2 M172.8,207 H180 M172.8,216 H180" stroke="#111" stroke-width=".4"/>')
for cx, cy in ((148, 207), (148, 216), (172, 207), (172, 216)):
    A(f'<circle cx="{cx}" cy="{cy}" r=".8" fill="#fff" stroke="#111" stroke-width=".35"/>')
A('<path d="M148.7,206.7 L171.2,206.4" stroke="#111" stroke-width=".75" stroke-linecap="round"/>')   # 87-87a: closed at rest
A('<path d="M148.7,215.6 L169.2,211.6" stroke="#111" stroke-width=".75" stroke-linecap="round"/>')   # 88-88a: open at rest
A('<rect x="156" y="221" width="8" height="7" fill="#fff" stroke="#111" stroke-width=".4"/><path d="M156,228 L164,221" stroke="#111" stroke-width=".35"/>')
A('<path d="M156,224.5 H150 V232 M164,224.5 H170 V232" fill="none" stroke="#111" stroke-width=".4"/>')
A('<path d="M160,221 V207.8" stroke="#999" stroke-width=".3"/>')   # mechanical link from the coil to both contacts
wire('100', [(140, 207), (134, 207), (134, 186), (138, 186)], label=False); tag(140, 186, '100 SV 0.75 → earth at relay 102')
wire('96', [(170, 232), (170, 238), (176, 238)], label=False); tag(178, 238, '96 GR 0.75 ← wiper switch 61 (via 58 D8)')
wire('100a', [(150, 232), (150, 238)], label=False); tag(147, 241, '100a SV 0.75: coil 85, ends on the drawing', anchor='end')
wire('95b', [(230, 211), (230, 234), (272, 234)], 233, 232.5)
wire('98', [(180, 216), (246, 216), (246, 206), (272, 206)], 192, 214.5)
wire('97', [(272, 216), (262, 216), (262, 229), (272, 229)], label=False); txt(260, 224.5, '97 BR 0.75', 1.9, 'end')
for y0, y1 in ((203, 219), (226, 237)):
    A(f'<rect x="272" y="{y0}" width="5" height="{y1 - y0}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
txt(274.5, 201.5, '123', 2.1, 'middle', fill='#555')
for y in (211, 232):
    A(f'<path d="M277,{y} H292" stroke="#111" stroke-width=".6"/>'); motor(299, y)
    txt(309, y + 1, '<tspan font-weight="bold">66</tspan> Headlight wiper motor', 2.6)
txt(308, 222, 'earths 99 / 99a SV 0.75', 2.2, fill='#555')

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
notes = ['Wipers run from fuse 4 on the ignition-on bar: 85 BR to the switch (53a) and 85a BR to the interval relay and motor terminal 4.',
         'The washer switch signal (91 GL) goes to the interval relay, which feeds the washer pump (91a GL), so it can wipe while washing.',
         'Speed wires: 87 GN to motor terminal 3, 86 RD to terminal 5 (through connector 58 at D8); 85a feeds 4, 88a is the park contact (2).',
         'Headlight wipers: unfused tap 94 BR from bar 3–6, then a 3 A glass fuse in holder 65 (manual, PDF p. 30) and relay 67.',
         'Diagram is not RHD-specific; the switch and relay positions (D8/D9) are drawing grid squares, not locations in the car.',
         'Relay 67: 88 is + from the 3 A fuse, fed on to the motors (95a/95b); 88a switches control wire 98 GL, linked on by 97 BR.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 5.2, n, 2.3, fill='#333')
save('wipers.svg')

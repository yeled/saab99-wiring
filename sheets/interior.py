#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo interior lights, seat heating and seat belt warning sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Interior lights, seat heating, seat belt warning',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual. Dashed = not traced yet.')
def conn(x, y, h, lab):
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    txt(x, y - h / 2 - 1.5, lab, 2.2, 'middle', fill='#555')
def ref(x, y, sym, n, name, cables):
    if sym == 'lamp': lamp(x + 4, y - 1, r=3.2)
    else:
        A(f'<path d="M{x},{y + 1} l6,-4 M{x + 6},{y - 1} h3" stroke="#111" stroke-width=".6"/>')
    txt(x + 12, y, f'<tspan font-weight="bold">{n}</tspan> {name}', 2.7)
    txt(x + 12, y + 4.6, cables, 2.3, fill='#555')

txt(18, 40, 'Seat heating', 3.4, w='bold')
box(18, 55, 32, 14); txt(21, 61, f'<tspan font-weight="bold">F5</tspan> · {FUSES[5]["rating"]}', 2.6); txt(21, 65.8, 'ignition-on bar', 2.1, fill='#555')
wire('140', [(50, 62), (118, 62)], 58, 60.5); conn(120, 62, 8, '58 (E12)')
wire('140', [(122, 62), (178, 62)], label=False); conn(180, 62, 8, '59')
A('<path d="M182,62 H196" stroke="#111" stroke-width=".6"/>')
box(196, 55, 44, 14); A('<path d="M200,62 l3,-4 l3,8 l3,-8 l3,8 l3,-8 l3,8 l3,-8 l3,8 l2,-4" fill="none" stroke="#111" stroke-width=".45"/>')
A('<path d="M230,65 l6,-5" stroke="#111" stroke-width=".5"/>')
txt(218, 75, '64 Seat heating element with thermostat (A6)', 2.5, 'middle', w='bold')
wire('141', [(240, 62), (250, 62), (250, 66)], label=False); earth(250, 66); txt(254, 69, '141 SV 1.0', 2.2)
wire('150', [(180, 66), (180, 86), (196, 86)], label=False); tag(198, 86, '150 GL 0.75 via connector 60 → seat belt contacts (59, A8)')

txt(18, 108, 'Interior lights', 3.4, w='bold')
txt(18, 114, 'Fuse 9’s 160 GL feeds 52, then 161 GL through 57 to 50 and (163 GL) 55; 164 BL, 167 SV reach 50; 162/165 SV link 50–51; doors 170/171 SV.', 2.4, fill='#555')
items = [('lamp', '50', 'Dome light, door pillar (A10)', '164 BL 0.75, 167 SV 0.75'),
         ('lamp', '51', 'Dome light, rear-view mirror (A10)', '162 SV 0.75, 165 SV 0.75'),
         ('lamp', '52', 'Ignition switch light (A9)', '161 GL 0.75, 164 BL 0.75, via connector 57'),
         ('switch', '53', 'Interior lighting switch (A9)', '167a SV 0.75 via connector 60, 169 SV 0.75'),
         ('switch', '54', 'Door switch (A9, A11, B11)', '170 SV 0.75'),
         ('lamp', '55', 'Luggage compartment light (A10)', '163 GL 0.75, 166 BL 0.75 to switch 56'),
         ('switch', '56', 'Luggage compartment light switch (A10)', '166 BL 0.75, earth')]
for i, it in enumerate(items):
    ref(18 + (i % 2) * 190, 126 + (i // 2) * 14, *it)
txt(18, 188, '57 3-pole connector (A10): pins carry 161 GL, 164 BL, and 167a SV (switch side) to 167 SV (lamp side). + is 160 GL from fuse 9.', 2.4)

txt(18, 206, 'Seat belt warning', 3.4, w='bold')
txt(18, 212, 'Fuse 5’s 150 GL reaches the seat and belt contacts; through them, 156 BR and 151 BR feed lamp 72, which returns on 157 SV (probably).', 2.3, fill='#555')
belt = [('switch', '69', 'Seat contact (A8)', 'via 59 (A8); contact wiring too cramped to read'), ('switch', '70/71', 'Seat belt contacts L/R (A8)', 'via 59 (A8); 168 SV 0.75 to earth'),
        ('lamp', '72', 'Seat belt warning lamp (D12)', '151 BR 0.75 in, 157 SV 0.75 to earth, via 59 (C12)')]
for i, it in enumerate(belt):
    ref(18 + (i % 2) * 190, 222 + (i // 2) * 12, *it)

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
tick(x, ly + 23.3); txt(x + 4, ly + 24, 'checked on the car', 2.4)
notes = ['Seat heating: fuse 5 (ignition-on bar) feeds 140 GL 1.0 through connector 58 at E12, which the manual draws as an optional pin,',
         'and connector 59 to the heating element; its return is 141 SV 1.0. This resolves one of fuse 5’s open wires.',
         'Interior lights and seat belt warning are listed as references only: the checks on the car (docs/car-checklist.md) will fill them in.',
         'Fuse 5 also powers the Turbo’s high-speed fuel boost (speed transmitter 140 and throttle switch 137): see the ignition sheet.',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 5.8, n, 2.35, fill='#333')
save('interior.svg')

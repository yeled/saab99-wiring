#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo heating and cooling sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Radiator fan, heater fan, heated rear window',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual. Dashed = not traced yet.')
def fuse_box(y, n):
    box(18, y - 7, 32, 14); txt(21, y - 1, f'<tspan font-weight="bold">F{n}</tspan> · {FUSES[n]["rating"]}', 2.6)
    txt(21, y + 3.8, {'3-6': 'ignition-on bar', '7-12': 'always-live bar'}[FUSES[n]['bar']], 2.1, fill='#555')
def conn(x, y, h, lab):
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    txt(x, y - h / 2 - 1.5, lab, 2.2, 'middle', fill='#555')
def motor(x, y, r=7):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(x, y + 1.2, 'M', 3, 'middle', w='bold')
def relay(x, y, n, name, t):
    box(x, y, 34, 30); txt(x + 17, y + 13, n, 3, 'middle', w='bold'); txt(x + 17, y + 18, name, 2.1, 'middle')
    for k, (tx, ty) in t.items():
        dot(x + tx, y + ty); txt(x + tx + (1.5 if tx == 0 else -1.5), y + ty + (-1.3), k, 2.2, 'start' if tx == 0 else 'end')

# ---- radiator fan -------------------------------------------------------------
txt(18, 40, 'Radiator fan', 3.4, w='bold')
fuse_box(62, 7)
relay(110, 50, '38', 'Radiator fan relay', {'30/51': (0, 8), '86': (0, 22), '87': (34, 8), '85': (34, 22)})
wire('110', [(50, 58), (110, 58)], 58, 56.5); wire('113', [(50, 66), (80, 66), (80, 72), (110, 72)], 58, 64.5)
wire('111', [(144, 58), (236, 58)], 170, 56.5); conn(240, 58, 8, '59')
A('<path d="M242,58 H262" stroke="#111" stroke-width=".6"/>'); motor(270, 58)
txt(280, 56, '<tspan font-weight="bold">37</tspan> Radiator fan motor (D1)', 2.7); A('<path d="M270,65 v5" stroke="#111" stroke-width=".6"/>'); earth(270, 70)
wire('114', [(144, 72), (196, 72), (196, 88), (216, 88)], 160, 70.5); conn(220, 88, 6, '60')
wire('114a', [(222, 88), (262, 88)], 228, 86.5)
box(262, 82, 20, 12); A('<path d="M266,90 l8,-5 M274,88 h6" stroke="#111" stroke-width=".5"/>'); A('<path d="M282,88 H290 v4" stroke="#111" stroke-width=".6"/>'); earth(290, 92)
txt(262, 104, '<tspan font-weight="bold">39</tspan> Thermostat switch (E2): closes when hot', 2.5)

# ---- heater fan ------------------------------------------------------------------
txt(18, 124, 'Heater (ventilator) fan', 3.4, w='bold')
fuse_box(146, 6)
wire('103', [(50, 146), (110, 146)], 58, 144.5)
box(110, 134, 34, 30); txt(127, 158, '35 Fan switch', 2.4, 'middle', w='bold')
dot(110, 146); txt(112, 144.7, '4', 2.2); dot(144, 142); txt(142, 140.7, '8', 2.2, 'end'); dot(144, 152); txt(142, 150.7, '6', 2.2, 'end')
wire('105', [(144, 142), (236, 142)], 170, 140.5); conn(240, 147, 16, '57')
wire('104', [(144, 152), (236, 152)], 170, 150.5)
A('<path d="M242,142 H262 M242,152 H250" stroke="#111" stroke-width=".6"/>')
box(250, 148, 12, 8); txt(256, 161, '74 resistor', 2.2, 'middle'); A('<path d="M262,152 H266 V146" stroke="#111" stroke-width=".6"/>')
motor(270, 142); txt(280, 140, '<tspan font-weight="bold">36</tspan> Heater fan motor (F12)', 2.7); A('<path d="M277,142 h6 v5" stroke="#111" stroke-width=".6"/>'); earth(283, 147)
txt(290, 146, 'speed 8: full; speed 6: through 74', 2.2, fill='#555')

# ---- heated rear window ----------------------------------------------------------------
txt(18, 186, 'Heated rear window', 3.4, w='bold')
fuse_box(208, 8)
relay(110, 196, '113', 'Heated window relay', {'30': (0, 8), '86': (0, 22), '87': (34, 8), '85': (34, 22)})
wire('210', [(50, 204), (110, 204)], 58, 202.5)
wire('213', [(110, 218), (86, 218)], label=False); tag(84, 218, '213 BL 0.75 ← 116 switch (feed 214 BL)', anchor='end')
wire('211', [(144, 204), (262, 204)], 170, 202.5)
box(262, 199, 30, 10); A('<path d="M265,204 l2,-2 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,2" fill="none" stroke="#111" stroke-width=".4"/>')
A('<path d="M292,204 h6 v4" stroke="#111" stroke-width=".6"/>'); earth(298, 208); txt(262, 220, '<tspan font-weight="bold">115</tspan> Heated rear window (D12)', 2.6)
wire('212', [(144, 218), (152, 218), (152, 222)], label=False); earth(152, 222); txt(156, 225, '212 SV 0.75', 2.2)

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
notes = ['Radiator fan: relay 38 is fed from fuse 7 on the always-live bar, and the thermostat switch earths its coil, so the drawing',
         'lets the fan run after the engine is switched off. 111 GN to the motor is dashed only because its full route isn’t traced.',
         'Heater fan: fuse 6 is on the ignition-on bar. Position 8 feeds the motor directly; position 6 goes through resistor 74.',
         'Heated rear window: fuse 8 (always live) feeds relay 113; switch 116 energises it through 213 BL. Its feed (214 BL) also powers the tachometer via 203.',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 5.8, n, 2.35, fill='#333')
save('climate.svg')

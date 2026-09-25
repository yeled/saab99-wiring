#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo instruments and warning lamps sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Instruments and warning lamps',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual.')
def conn(x, y, h, lab):
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    txt(x, y - h / 2 - 1.5, lab, 2.1, 'middle', fill='#555')
def gauge(x, y, r, t):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(x, y + 1.2, t, 3, 'middle')
def sender(x, y, n, name, s=11, sw=1.5):
    """The manual's sender symbol (44, 45) with its outer top-left at (x, y): a heavy square with one thin diagonal
    from the inner bottom-left to the inner top-right corner, the number centred above the square as printed, our name
    to its right. No terminal circles or names are printed: the earth lead leaves the left wall level with the
    diagonal's foot, left then down to earth; the signal lead drops from the bottom wall near its right end.
    Returns where the signal wire starts."""
    r = lambda v: round(v, 2)
    A(f'<rect x="{r(x + sw / 2)}" y="{r(y + sw / 2)}" width="{r(s - sw)}" height="{r(s - sw)}" fill="#fff" stroke="#111" stroke-width="{sw}"/>'
      f'<path d="M{r(x + sw)},{r(y + s - sw)} L{r(x + s - sw)},{r(y + sw)}" stroke="#111" stroke-width=".4"/>')
    lamp_earth(x, r(y + s - sw), dx=-6)
    txt(r(x + s / 2), y - 2.2, n, 2.6, 'middle', w='bold')   # two elements: cairosvg misplaces a bold tspan in centred text
    txt(r(x + s / 2 + len(n) * .72 + .75), y - 2.2, name, 2.6)   # half the bold number (.556 em per digit) plus a space
    return r(x + s - sw - .2), r(y + s - .1)

# ---- combination instrument 47 --------------------------------------------
box(150, 70, 140, 120); txt(150, 66, '47 Combination instrument (C9)', 3, w='bold')
T = {'9': (150, 90), '1': (150, 150), '11': (200, 70), '12': (235, 70), '3': (270, 70),
     '7a': (170, 190), '5': (200, 190), '6': (230, 190), '2': (260, 190), '4': (280, 190)}
for k, (x, y) in T.items():
    dot(x, y)
    if x == 150: txt(x + 1.8, y - 1.6, k, 2.3)
    elif y == 70: txt(x + 1.8, y + 3.4, k, 2.3)
    else: txt(x + 1.8, y - 1.6, k, 2.3)
gauge(180, 90, 11, '°C'); A('<path d="M150,90 H169" stroke="#111" stroke-width=".5"/>'); txt(180, 105.5, 'temperature', 2.3, 'middle')
gauge(270, 110, 11, 'fuel'); A('<path d="M270,70 V99" stroke="#111" stroke-width=".5"/>'); txt(270, 125.5, 'fuel gauge', 2.3, 'middle')
for (x, y, tx, ty, cap) in ((200, 70, 200, 84, 'oil'), (235, 70, 235, 84, 'low fuel'), (150, 150, 172, 150, 'charge'),
                            (170, 190, 170, 172, 'main beam'), (200, 190, 200, 172, 'brake'), (230, 190, 230, 172, 'indicator')):
    A(f'<path d="M{x},{y} L{tx if x == 150 else x},{ty}" stroke="#111" stroke-width=".5"/>')
    lx = tx + (4 if x == 150 else 0)
    lamp(lx, ty, r=3.5)
    txt(lx, ty + (8 if y == 70 else -5.5) if x != 150 else ty - 5.5, cap, 2.2, 'middle')
txt(220, 140, 'internal wiring not drawn', 2.2, 'middle', fill='#777')

# ---- senders and feeds on the left -----------------------------------------
# 44 and 45 as the manual prints them (sender symbol, own earth lead); the signal wires keep their old runs at y 50 / 90
name_ = lambda x, y, n, s: txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', 2.6)
sx, sy = sender(40, 35, '44', 'Oil warning switch (A2)')
wire('184', [(sx, sy), (sx, 50), (200, 50), (200, 70)], 60, 48.5); conn(110, 50, 7, '58 (A4) pin 5')
sx, sy = sender(40, 75, '45', 'Temperature transmitter (A2)')
wire('183', [(sx, sy), (sx, 90), (150, 90)], 60, 88.5); conn(110, 90, 7, '58 (A4) pin 6')
box(22, 146, 34, 16); name_(25, 155, '2', 'Alternator (B3)')   # D+ a quarter down the right wall, as printed (B+ not on this sheet)
wire('195', [(56, 150), (150, 150)], 60, 148.5)
dot(56, 150); tlabel(54.2, 150.6, 'D+', 'end')   # the manual prints D+ left of its circle on the right wall

# ---- fuel sender and tachometer on the right ---------------------------------
box(360, 82, 36, 20); name_(363, 89, '46', 'Fuel level'); txt(363, 93.5, 'transmitter (C12)', 2.4)
wire('185', [(360, 88), (330, 88), (330, 60), (270, 60), (270, 70)], 300, 58.5)
wire('186', [(360, 96), (340, 96), (340, 54), (235, 54), (235, 70)], 300, 52.5)
A('<rect x="343" y="84" width="4" height="16" fill="#ddd" stroke="#111" stroke-width=".5"/>'); txt(342, 81, '57 (B12)', 2.2, fill='#555')
gauge(340, 150, 12, 'r/min'); txt(340, 168, '110 Tachometer (C11)', 2.6, 'middle', w='bold')
wire('203', [(352, 150), (362, 150)], label=False); tag(364, 150, '203 BR → 116 (+ supply?)')
wire('204', [(340, 138), (340, 130), (346, 130)], label=False); tag(348, 130, '204 GL 0.75 ← ECU speed signal')

# ---- bottom terminals ----------------------------------------------------------
wire('179', [(280, 190), (280, 196)], label=False); earth(280, 196); txt(284, 199, '179 SV 0.75', 2.3)
wire('182', [(260, 190), (260, 206)], label=False); tag(262, 206, '182 BR/VT 0.75 ← fuse 4 (off 85 BR at 58 (D8))')
wire('71', [(230, 190), (230, 214)], label=False); tag(232, 214, '71 GN/VT 0.75 ← 23 flasher unit, terminal C')
wire('187', [(200, 190), (200, 222)], label=False); tag(202, 222, '187 VT 0.75 → 58 (B9) → 188 VT → 43 handbrake, 42 brake failure switch')
wire('27', [(170, 190), (170, 230)], label=False); tag(172, 230, '27 BL/VT 0.75 ← 8 lighting relay 56a (lighting sheet)')

# ---- legend and notes ------------------------------------------------------------
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
probable_legend(x, ly + 30)
notes = ['Terminal numbers are the instrument’s own, from the manual’s diagram. Its internal wiring (common supply, earth) isn’t drawn.',
         'Oil and temperature wires pass connector 58 (A4), pins 5 and 6; the fuel sender wires pass 3-pole connector 57 (B12).',
         'Charge lamp: alternator D+ is 195 RD 0.75. Main-beam lamp: 27 BL/VT from lighting relay 8. Indicator lamp: 71 GN/VT from flasher 23.',
         'Supply: 182 BR/VT from fuse 4, branching off the wiper feed 85 BR at connector 58 (D8). Tachometer: signal 204 GL, supply 203 via 116.',
         '44 and 45 are drawn with the manual’s sender symbol (heavy square with a diagonal, not a winding), each with its own earth lead '
         '(no number printed). 44 probably earths the oil lamp at low oil pressure; '
         '45 is probably a resistance that falls as the coolant warms.',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 5.2, n, 2.35, fill='#333')
save('instruments.svg')

#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo instruments and warning lamps sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Instruments and warning lamps')
def conn(x, y, h, lab):
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    txt(x, y - h / 2 - 1.5, lab, 2.1, 'middle', fill='#555')
def lab(c):
    """A cable's label as wire() prints it: number, colour, mm² from wires.csv."""
    r = WIRES[c]; return f"{c.split('#')[0]} {r['colour']} {r['mm2']}"
def mtag(x, y, lines, w, size=2.4, anchor='start'):
    """Destination tag of several lines (common.tag() takes one), boxed as the lighting sheet's two-line tags: centred
    on y, lines 1.36 × size apart. w: from the rendered text."""
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2); x0 = x if anchor == 'start' else x - w
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines): txt(x0 + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
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
# Inside as the 1979 book prints it (book photo P8-47, scan p.407 at x 5800-6390, y 1560-1945): a + rail from 2 (182)
# feeds both gauges and the oil, low-fuel, brake and charge lamps, each lamp between the rail and its own terminal; an
# earth rail to 4 (179) takes the gauges' third leads and the main-beam (7) and indicator (6) lamps. The book prints a
# dot at every join; crossings without one (C° earth lead over the + rail, earth rail over the 11-5 line, earth loop
# over the fuel gauge's + lead) don't join.
def jdot(x, y): A(f'<circle cx="{x}" cy="{y}" r=".55" fill="#111"/>')   # small junction dot inside a part (as wipers)
box(150, 70, 140, 120); txt(150, 66, '47 Combination instrument', 3, w='bold')
T = {'9': (150, 90), '1': (150, 150), '11': (200, 70), '12': (235, 70), '3': (265, 70),
     '7': (170, 190), '5': (200, 190), '6': (235, 190), '2': (260, 190), '4': (271, 190)}
for k, (x, y) in T.items():
    dot(x, y)
    if x == 150: txt(x + 1.8, y - 1.6, k, 2.3)
    elif y == 70: txt(x + 1.8, y + 3.4, k, 2.3)
    else: txt(x + 1.8, y - 1.6, k, 2.3)
PR, ER, EL, LR = 130, 175, 158, 3.5          # + rail, earth rail, earth loop up to the fuel gauge, lamp radius
on_circle = lambda cx, cy, r, x: round(cy + (r * r - (x - cx) ** 2) ** .5, 2)   # lowest point of the circle at x
# gauge faces as printed: C° (temperature) and B (bensin, fuel)
# temperature gauge: sender 9 on the left, + from the bottom, earth from the right side down to the earth rail
gauge(177, 90, 12, 'C°'); inner([(150, 90), (165, 90)]); txt(175, 108, 'temperature', 2.3, 'end')
inner([(177, 102), (177, PR)]); jdot(177, PR)
inner([(189, 90), (193, 90), (193, ER)]); jdot(193, ER)
# fuel gauge: sender 3 on top, + lead from the bottom left through the rail to 2, earth lead from the bottom right to 4
gauge(265, 90, 12, 'B'); inner([(265, 70), (265, 78)]); txt(273, 108, 'fuel gauge', 2.3)
inner([(260, on_circle(265, 90, 12, 260)), (260, 190)]); jdot(260, PR)
inner([(271, on_circle(265, 90, 12, 271)), (271, 190)]); jdot(271, EL)
inner([(177, PR), (260, PR)])                                          # the + rail
# oil (11) and low fuel (12): terminal, lamp, + rail; the 11 line carries on through the brake lamp to 5
for x, cap in ((200, 'oil'), (235, 'low fuel')):
    inner([(x, 70), (x, 90 - LR)]); lamp(x, 90, r=LR); inner([(x, 90 + LR), (x, PR)]); jdot(x, PR); txt(x + 5.5, 91, cap, 2.2)
inner([(200, PR), (200, 142 - LR)]); lamp(200, 142, r=LR); inner([(200, 142 + LR), (200, 190)]); txt(205.5, 143, 'brake', 2.2)
# charge (1): + rail, lamp, then down and left to 1
inner([(177, PR), (177, 142 - LR)]); lamp(177, 142, r=LR); inner([(177, 142 + LR), (177, 150), (150, 150)])
txt(171.5, 143, 'charge', 2.2, 'end')
# earth rail: main-beam lamp (fed from 7), C° earth lead, the loop up to the fuel gauge's earth lead, indicator lamp (fed
# from 6, on the low-fuel lamp's vertical as printed)
lamp(177, ER, r=LR); inner([(177 - LR, ER), (170, ER), (170, 190)]); txt(177, 170, 'main beam', 2.2, 'middle')
inner([(177 + LR, ER), (235 - LR, ER)]); jdot(215, ER); inner([(215, ER), (215, EL), (271, EL)])
lamp(235, ER, r=LR); inner([(235, ER + LR), (235, 190)]); txt(235, 170, 'indicator', 2.2, 'middle')

# ---- senders and feeds on the left -----------------------------------------
# 44 and 45 as the manual prints them (sender symbol, own earth lead); the signal wires keep their old runs at y 50 / 90
name_ = lambda x, y, n, s: txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', 2.6)
sx, sy = sender(40, 35, '44', 'Oil warning switch')
wire('184', [(sx, sy), (sx, 50), (200, 50), (200, 70)], 60, 48.5); conn(110, 50, 7, 'engine connector 58, pin 5')
sx, sy = sender(40, 75, '45', 'Temperature transmitter')
wire('183', [(sx, sy), (sx, 90), (150, 90)], 60, 88.5); conn(110, 90, 7, 'engine connector 58, pin 6')
box(22, 146, 34, 16); name_(25, 155, '2', 'Alternator')   # D+ a quarter down the right wall, as printed (B+ not on this sheet)
wire('195', [(56, 150), (150, 150)], 60, 148.5)
dot(56, 150); tlabel(54.2, 150.6, 'D+', 'end')   # the manual prints D+ left of its circle on the right wall

# ---- fuel sender and tachometer on the right ---------------------------------
box(360, 82, 36, 20); name_(363, 89, '46', 'Fuel level'); txt(363, 93.5, 'transmitter', 2.4)
wire('185', [(360, 88), (330, 88), (330, 60), (265, 60), (265, 70)], 300, 58.5)
wire('186', [(360, 96), (340, 96), (340, 54), (235, 54), (235, 70)], 300, 52.5)
A('<rect x="343" y="84" width="4" height="16" fill="#ddd" stroke="#111" stroke-width=".5"/>'); txt(345, 104.5, 'fuel sender connector 57', 2.2, 'middle', fill='#555')
# 46's third lead, 190 SV from its right-hand wall (no terminal name printed; probably its earth), to 1-pole tank earth
# connector 60 (60 (C12)), where the pump's earth 262 joins it; 191 SV 2.5 goes on to earth (all on the ignition sheet)
wire('190', [(396, 92), (402, 92), (402, 113), (399, 113)], label=False)
mtag(397, 113, (f"{lab('190')} → tank earth connector 60 → {lab('191')}", '→ earth, with pump earth 262 (ignition sheet)'),
     w=61, anchor='end')                                    # w from the rendered text
TX, TY = 314, 154   # tachometer centre: left of the fuel sender so 203's and 204's tags fit in full inside the frame
gauge(TX, TY, 12, 'r/min'); txt(TX, TY + 18, '110 Tachometer', 2.6, 'middle', w='bold')
wire('203', [(TX + 12, TY), (TX + 16, TY)], label=False)
tag(TX + 18, TY, '203 BR 0.75 ← heated window switch 116 (climate sheet)', w=65, size=2.4)   # w from the rendered text
# 204 from service outlet 73 pin 5, a lead of its own beside 284a (ignition sheet), through 1-pole connector 60 (60 (B10))
wire('204', [(TX, TY - 12), (TX, TY - 24), (TX + 12, TY - 24)], label=False); conn(TX + 6, TY - 24, 7, 'tachometer connector 60')
tag(TX + 14, TY - 24, f"{lab('204')} ← service outlet 73, pin 5, with 284a (ignition sheet)", w=73, size=2.4)

# ---- bottom terminals ----------------------------------------------------------
# 179 earths 47 through panel light connector 59 (59 (D11)), 52 SV and hazard switch 25's lamp terminal, which 69 SV
# earths (signals sheet): the only earth printed for this chain
wire('179', [(271, 190), (271, 198)], label=False)
tag(273, 198, f"{lab('179')} → panel light connector 59 → 52 {WIRES['52']['colour']} → hazard switch 25’s lamp → "
              f"69 {WIRES['69']['colour']} → earth (signals sheet)", w=130.5)   # the staircase's size 2.6; w from the rendered text
wire('182', [(260, 190), (260, 206)], label=False); tag(262, 206, '182 BR/VT 0.75 ← fuse 4 (off 85 BR at stalk switch connector 58)')
wire('71', [(235, 190), (235, 214)], label=False); tag(237, 214, '71 GN/VT 0.75 ← 23 flasher unit, terminal C')
wire('187', [(200, 190), (200, 222)], label=False); tag(202, 222, '187 VT 0.75 → ignition switch connector 58 → 188 VT → 43 handbrake, 42 brake warning switch')
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
size_legend(x, ly + 18)                               # line widths, under the colours
y = ly + 24                                           # text baseline of the status row: traced, then the dashed sample or the tick
A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x + 48},{y - 1} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 59, y, 'not traced yet', 2.4)
def ticked(tx, ty): tick(tx, ty - .7); txt(tx + 4, ty, 'checked on the car', 2.4)   # the check mark sample, text baseline ty
if TICKED[0] and not DASHED[0]: ticked(x + 48, y)    # beside 'traced' when the dashed sample leaves room
if probable_legend(x, y + 5): y += 6
if TICKED[0] and DASHED[0]:                           # else after the grey sample (4th colour column), or a row of its own
    if PROBABLE[0]: ticked(x + 69, y)
    else: y += 6; ticked(x, y)
notes = ['Inside 47 (its own terminal numbers): a + rail from 2 (182) feeds both gauges and the oil (11), low-fuel (12), brake (5) '
         'and charge (1) lamps; an earth rail to 4 (179) takes the gauges’ third leads and the main-beam (7) and indicator (6) lamps.',
         'Oil and temperature wires pass engine connector 58, pins 5 and 6 (our own count, top to bottom; check E1); the fuel sender wires pass fuel sender connector 57 (3-pole).',
         'Charge lamp: alternator D+ is 195 RD 0.75. Main-beam lamp: 27 BL/VT from lighting relay 8. Indicator lamp: 71 GN/VT from flasher 23.',
         'Supply: 182 BR/VT from fuse 4, branching off the wiper feed 85 BR at stalk switch connector 58. Tachometer: signal 204 GL from '
         'service outlet 73 pin 5 (beside 284a), through tachometer connector 60; supply probably 203 from heated window switch 116.',
         'Earth: 47’s 4 (179 SV) goes through panel light connector 59 and 52 SV to hazard switch 25’s lamp terminal, which 69 SV earths '
         '(signals sheet); the panel lamps (not drawn) earth the same way.',
         'Fuel level transmitter 46: its third lead, 190 SV, is probably its earth. It meets the pump’s earth 262 at tank earth connector 60 '
         'and goes on as 191 SV 2.5 to earth, probably near the tank.',
         '44 and 45 are drawn with the sender symbol (heavy square with a diagonal, not a winding), each with its own earth lead '
         '(no cable number). 44 probably earths the oil lamp at low oil pressure; '
         '45 is probably a resistance that falls as the coolant warms.',
         'Not RHD-specific: circuits should match the car, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 5.6 + j * 4.1, n, 2.35, fill='#333')   # 8 lines: 4.1 pitch fits the box
save('instruments.svg')

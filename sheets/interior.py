#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo interior lights, seat heating and seat belt warning sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Interior lights, seat heating, seat belt warning',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual.')
def conn(x, y, h, lab, links=()):
    """In-line connector pin; links: row heights where the manual prints a through-link (a dot on both inner edges)."""
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    for ry in links: inner([(x - 2, ry), (x + 2, ry)]); dot(x - 2, ry); dot(x + 2, ry)
    txt(x, y - h / 2 - 1.5, lab, 2.2, 'middle', fill='#555')
def meander(x, y, w=10, up=1.2, down=1.8):
    """Heating element as the manual prints it: three square humps between two open circles; x, y is its left lead end."""
    s = w / 6
    pts = [(x, y)] + [(round(x + (k + j) * s, 2), round(y + (-up if k % 2 == 0 else down), 2)) for k in range(6) for j in (0, 1)] + [(x + w, y)]
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".4" stroke-linejoin="round"/>')
def ref(x, y, sym, n, name, cables):
    if sym == 'lamp': lamp(x + 4, y - 1, r=3.2)
    else:
        A(f'<path d="M{x},{y + 1} l6,-4 M{x + 6},{y - 1} h3" stroke="#111" stroke-width=".6"/>')
    txt(x + 12, y, f'<tspan font-weight="bold">{n}</tspan> {name}', 2.7)
    txt(x + 12, y + 4.6, cables, 2.3, fill='#555')

txt(18, 40, 'Seat heating', 3.4, w='bold')
# fuse 5 of fuse box 22, turned a quarter as on the radio sheet: the ignition-on bar runs down the left, its junction
# ring feeds the 8 A fuse, and bottom terminal 5 is the dot on the box edge
box(18, 52, 32, 20); txt(21, 57, f'<tspan font-weight="bold">F5</tspan> · {FUSES[5]["rating"]}', 2.6)
inner([(24, 59.5), (24, 69.5)]); contact(24, 62); txt(26, 69, 'ignition-on bar', 2.1, fill='#555')
fa, fb = fuse(30, 60.8, 10, 2.4); inner([(24.8, 62), fa]); inner([fb, (50, 62)]); dot(50, 62); tlabel(48.5, 60.6, '5', 'end')
# 140 runs fuse 5 → 58 (E12) → 60 (A7) → 59 (A7) → 64; 150 leaves 60's fuse-side dot (its right one in the manual)
wire('140', [(50, 62), (118, 62)], 58, 60.5); wire('140', [(122, 62), (148, 62)], label=False); wire('140', [(152, 62), (178, 62)], label=False)
conn(120, 62, 8, '58 (E12)', links=(62,)); conn(150, 62, 8, '60 (A7)', links=(62,)); conn(180, 62, 8, '59 (A7)', links=(62,))
A('<path d="M182,62 H196" stroke="#111" stroke-width=".6"/>')
# 64 as the manual prints it: lower element, thermostat (open), upper element, in series. The manual draws the two
# elements side by side into both rows of 59; here they run in a line from 140 (left) to 141 (right).
box(196, 47.5, 55, 19)
# thermostat housing: a heavy outline as printed, not conductor weight, so it doesn't read as a loop bypassing the
# contacts; its walls' inner edges touch the contacts (top one hangs, bottom one sits) and the blade rests on the right wall
A('<rect x="217.5" y="50.9" width="11" height="12.2" rx=".6" fill="#fff" stroke="#111" stroke-width=".7"/>')
inner([(196, 62), (198.7, 62)]); contact(199.5, 62); inner([(200.3, 62), (202.1, 62)]); meander(202.1, 62)
inner([(212.1, 62), (213.9, 62)]); contact(214.7, 62); inner([(215.5, 62), (222.2, 62)]); contact(223, 62)
inner([(223.8, 52), (230.2, 52)]); contact(231, 52); inner([(231.8, 52), (233.6, 52)]); meander(233.6, 52)
inner([(243.6, 52), (245.4, 52)]); contact(246.2, 52); inner([(247, 52), (251, 52)]); contact(223, 52)
bimetal(223.4, 52.57, 227.85, 60)   # hangs from the top contact and rests on the right wall (a stop), clear of the bottom contact
dot(196, 62); dot(251, 52)
txt(223.5, 71.5, '64 Seat heating element with thermostat (A6)', 2.5, 'middle', w='bold')
wire('141', [(251, 52), (261, 52), (261, 57)], label=False); earth(261, 57); txt(265, 60, '141 SV 1.0', 2.2)
wire('150', [(144, 62), (144, 86), (196, 86)], label=False); dot(144, 62); tag(198, 86, '150 GL 0.75 to 59 (A8): seat and belt contacts')

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
txt(18, 216.4, 'On the car (I3): with the ignition on, the lamp stays lit until the driver buckles up; the passenger’s belt only counts while seat contact 69 is pressed.', 2.3, fill='#555')
belt = [('switch', '69', 'Seat contact (A8)', 'passenger seat: closes when sat on (car, I3); via 59 (A8)'), ('switch', '70/71', 'Seat belt contacts L/R (A8)', 'open when buckled (car, I3); via 59 (A8); 168 SV 0.75 to earth'),
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
notes = ['Seat heating: fuse 5 (ignition-on bar) feeds 140 GL 1.0 through 58 (E12), an optional pin in the manual, then 60 (A7) and 59 (A7) to seat heating 64: two',
         'elements in series with a thermostat between them, drawn open as printed (probably warm: it closes when cold); return 141 SV 1.0. The manual draws the',
         'two elements side by side into 59’s two rows (140 GL lower, 141 SV upper); here they run in a line and 141 is drawn straight to earth.',
         'Interior lights and seat belt warning are listed as references only. The seat belt logic comes from the car (check I3); the contacts’ wiring is too cramped to read in the book.',
         'Fuse 5 also powers the Turbo’s high-speed fuel boost (380 GL to speed transmitter, component 140; 380a GL to throttle switch 137): see the ignition sheet.',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 5, n, 2.35, fill='#333')
save('interior.svg')

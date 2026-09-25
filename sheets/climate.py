#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo heating and cooling sheet (A3 SVG)."""
import math
from common import *

header('Saab 99 Turbo, model 1979 — Radiator fan, heater fan, heated rear window',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual.')
def fuse_stub(y0, n):
    """Fuse n of fuse box 22, as radio.py draws fuse 9: the bar runs down the left, its junction ring feeds the fuse,
    and bottom terminal n is the dot on the box edge. Returns the height of that dot."""
    box(18, y0, 36, 20); txt(21, y0 + 5, f'<tspan font-weight="bold">F{n}</tspan> · {FUSES[n]["rating"]}', 2.6)
    yf = y0 + 10
    inner([(24, y0 + 7.5), (24, y0 + 17.5)]); contact(24, yf)
    txt(26, y0 + 17, {'3-6': 'ignition-on bar', '7-12': 'always-live bar'}[FUSES[n]['bar']], 2.1, fill='#555')
    fa, fb = fuse(32, yf - 1.2, 10, 2.4); inner([(24.8, yf), fa]); inner([fb, (54, yf)]); dot(54, yf); tlabel(52.5, yf - 1.4, str(n), 'end')
    return yf
def conn(x, y, h, lab):
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    txt(x, y - h / 2 - 1.5, lab, 2.2, 'middle', fill='#555')
def motor(x, y, r=7):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(x, y + 1.2, 'M', 3, 'middle', w='bold')
def lead(pts):
    """Plain lead on the part side of a connector (not a separately numbered cable)."""
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')
def fcontact(x, y):
    """Filled contact (the manual's black dot), same size as contact()."""
    A(f'<circle cx="{x}" cy="{y}" r=".8" fill="#111"/>')
WORK = [False]  # set when work() draws; the legend then shows its sample
def work(pts):
    """A switch's other positions, drawn short-dashed as the manual prints them (not 'not traced'; DASHED stays off)."""
    WORK[0] = True
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".4" stroke-dasharray=".8 .6"/>')
def meander(x, y, w=8, up=1.2, down=1.2):
    """Resistance wire as the manual prints it: square humps above and below the line; x, y is its left end."""
    s = w / 4
    pts = [(x, y)] + [(round(x + (k + j) * s, 2), round(y + (-up if k % 2 == 0 else down), 2)) for k in range(4) for j in (0, 1)] + [(x + w, y)]
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".4" stroke-linejoin="round"/>')
def fan(cx, cy, r, rot=12):
    """Fan symbol as the manual prints it for 36: a circle with four black wedge blades."""
    A(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#111" stroke-width=".4"/>')
    for k in range(4):
        a0, a1 = math.radians(rot + 90 * k - 22), math.radians(rot + 90 * k + 22)
        p0 = (round(cx + r * math.cos(a0), 2), round(cy + r * math.sin(a0), 2)); p1 = (round(cx + r * math.cos(a1), 2), round(cy + r * math.sin(a1), 2))
        A(f'<path d="M{cx},{cy} L{p0[0]},{p0[1]} A{r},{r} 0 0 1 {p1[0]},{p1[1]} Z" fill="#111"/>')

# ---- radiator fan -------------------------------------------------------------
txt(18, 40, 'Radiator fan', 3.4, w='bold')
y7 = fuse_stub(52, 7)
# relay 38, the manual's left-right mirror (30/51 and 86 face fuse 7): make contact across the top, open at rest;
# upright coil standing on the bottom wall, its link rising to the blade
box(110, 50, 34, 30); txt(127, 47.6, '38 Radiator fan relay', 2.2, 'middle', w='bold')
for x, y in ((110, 58), (110, 72), (144, 58), (144, 72)): dot(x, y)
tlabel(111.5, 60.6, '30/51'); tlabel(142.5, 56.7, '87', 'end'); tlabel(111.5, 70.7, '86'); tlabel(142.5, 70.7, '85', 'end')
inner([(110, 58), (120.2, 58)]); contact(121, 58); contact(133, 58); inner([(133.8, 58), (144, 58)])
blade(121.6, 57.5, 132.4, 54.6)
coil(124, 64, 6, 16); inner([(110, 72), (124, 72)]); inner([(130, 72), (144, 72)]); mlink([(127, 64), (127, 56.5)])
wire('110', [(54, y7), (57, 58), (110, 58)], 62, 56.5); wire('113', [(54, y7), (57, 66), (80, 66), (80, 72), (110, 72)], 62, 64.5)
wire('111', [(144, 58), (236, 58)], 170, 56.5); conn(240, 58, 8, '59')
A('<path d="M242,58 H262" stroke="#111" stroke-width=".6"/>'); motor(270, 58)
txt(280, 56, '<tspan font-weight="bold">37</tspan> Radiator fan motor (D1)', 2.7); A('<path d="M270,65 v5" stroke="#111" stroke-width=".6"/>'); earth(270, 70)
wire('114', [(144, 72), (196, 72), (196, 88), (216, 88)], 160, 70.5); conn(220, 88, 6, '60')
wire('114a', [(222, 88), (262, 88)], 228, 86.5)
box(262, 82, 20, 12); A('<path d="M266,90 l8,-5 M274,88 h6" stroke="#111" stroke-width=".5"/>')
# 39's earth side is not a local earth: 115 SV runs to the left headlamp's common and earths through its 28 SV
wire('115', [(282, 88), (292, 88)], label=False); tag(294, 88, '115 SV 0.75 ← left headlamp common; earth via 28 SV (lighting sheet)', w=71.9, size=2.2)
txt(262, 104, '<tspan font-weight="bold">39</tspan> Thermostat switch (E2): closes when hot', 2.5)

# ---- heater fan ------------------------------------------------------------------
txt(18, 124, 'Heater (ventilator) fan', 3.4, w='bold')
y6 = fuse_stub(139, 6)
wire('103', [(54, y6), (110, y6)], 60, y6 - 1.5)
# switch 35 at rest on its unlabelled terminal (probably off); its positions 8 and 6 dashed, as printed
box(110, 134, 34, 30); txt(127, 131.6, '35 Fan switch', 2.2, 'middle', w='bold')
for y in (142, 149, 157.4): dot(144, y)
dot(110, 149); tlabel(113, 147.6, '4'); tlabel(142.5, 140.6, '8', 'end'); tlabel(142.5, 147.6, '6', 'end')
inner([(110, 149), (117.7, 149)]); contact(118.5, 149)
contact(130.7, 142); inner([(131.5, 142), (144, 142)]); contact(132.8, 149); inner([(133.6, 149), (144, 149)])
fcontact(130.7, 157.4); inner([(131.5, 157.4), (144, 157.4)])
blade(119.1, 149.4, 130.4, 157.2)
work([(119.2, 148.6), (130, 142.5)]); work([(119.3, 149), (132, 149)])
wire('105', [(144, 142), (237, 142)], 170, 140.5)
wire('104', [(144, 149), (237, 149)], 196, 147.5)
# 57 (F11): three through-links; 74 hangs off it: in from row 2's right side, out onto 57's top edge just inside the
# left corner, in line with the left pins, where the manual hides which pin it joins (probably row 1: grey)
A('<rect x="237" y="138" width="8" height="22" fill="#ddd" stroke="#111" stroke-width=".5"/>'); txt(239.6, 136.3, '57 (F11)', 2.2, fill='#555')
for y in (142, 149, 156): inner([(237, y), (245, y)]); dot(237, y); dot(245, y)
inner([(238.2, 138), (238.2, 142)], grey=True)
box(244, 124, 14, 8); txt(239.9, 122.2, '<tspan font-weight="bold">74</tspan> Resistor, low speed', 2.2)  # centred on the box by hand: cairosvg misplaces a bold tspan in centred text
dot(244, 128); dot(258, 128); inner([(244, 128), (245.7, 128)]); contact(246.5, 128); meander(247.3, 128, 7.4, 1.4, 1.4)
contact(255.5, 128); inner([(256.3, 128), (258, 128)])
lead([(244, 128), (238.2, 128), (238.2, 138)]); lead([(258, 128), (260, 128), (260, 149), (245, 149)])
lead([(245, 142), (263, 142)]); lead([(245, 156), (263, 156)])
# the motor's return: 107 SV from 57 row 3 to earth joint 158 (drawn on the power sheet)
wire('107', [(237, 156), (224, 156)], label=False); tag(222, 156, '107 SV 2.5 → earth joint 158 (power sheet)', w=45.3, size=2.2, anchor='end')
# 36: terminals on the left wall, level with 57 rows 1 and 3; no internal leads to the fan are printed; blades square to the frame
box(263, 138, 22, 22); dot(263, 142); dot(263, 156); fan(274, 149, 7.5, rot=0)
txt(288, 147, '<tspan font-weight="bold">36</tspan> Heater fan motor (F12)', 2.7)
txt(288, 152, 'speed 8: full; speed 6: through 74', 2.2, fill='#555')
txt(288, 155.6, 'on the car: 74 is fixed under this motor’s housing (D5)', 2.2, fill='#555')

# ---- heated rear window ----------------------------------------------------------------
txt(18, 181, 'Heated rear window', 3.4, w='bold')
y8 = fuse_stub(186, 8)
# relay 113 as the manual prints it: contact column on the left (30 over 87, open at rest), coil column on the right
# (85 over 86), the coil against the right wall, a link from the coil towards the blade
box(110, 203, 34, 28); txt(107, 218.5, '113 Heated window relay', 2.2, 'end', w='bold')
for x, y in ((116, 203), (137, 203), (116, 231), (137, 231)): dot(x, y)
tlabel(117.3, 209.2, '30'); tlabel(135.7, 206.8, '85', 'end'); tlabel(117.3, 229.3, '87'); tlabel(135.7, 229.3, '86', 'end')
inner([(116, 203), (116, 210.3)]); contact(116, 211.1); blade(115.8, 211.8, 112.7, 222)
contact(116, 223.2); inner([(116, 224), (116, 231)])
coil(126.7, 214.2, 16.9, 5.9); inner([(137, 203), (137, 214.2)]); inner([(137, 220.1), (137, 231)]); mlink([(115.4, 217), (126.7, 217)])
wire('210', [(54, y8), (116, y8), (116, 203)], 60, y8 - 1.5)
# 113:85 takes three earth cables, fanned out from the terminal (nested so none cross): 13 SV from lighting relay 8
# and 33 SV from ignition switch relay 21 arrive; 212 SV takes all three to earth joint 158 (drawn on the power sheet)
wire('13', [(137, 203), (133, 199), (133, 174), (150, 174)], label=False); tag(152, 174, '13 SV 0.75 ← lighting relay 8:31 (lighting sheet)', w=49.6, size=2.2)
wire('33', [(137, 203), (137, 180.5), (150, 180.5)], label=False); tag(152, 180.5, '33 SV 0.75 ← ignition switch relay 21:85 (power sheet)', w=56.6, size=2.2)
wire('212', [(137, 203), (141, 199), (141, 187), (150, 187)], label=False); tag(152, 187, '212 SV 0.75 → earth joint 158 (power sheet)', w=46.5, size=2.2)
# switch 116 drawn off, as printed: the rocker rests on the middle contact, clear of the lamp contact and the dot
box(188, 196, 34, 24); txt(205, 193.6, '116 Heated window switch', 2.2, 'middle', w='bold')
for x in (193.9, 202.8, 211.6): dot(x, 220)
lamp(193.9, 207, r=3); inner([(193.9, 210), (193.9, 220)]); inner([(196.8, 207.8), (199.9, 207.8)])
contact(200.7, 207.8); inner([(201.5, 207.8), (203.1, 207.8)])
contact(209, 207.8); inner([(209.8, 207.8), (211.4, 207.8)]); inner([(209, 208.6), (209, 212.1), (202.8, 212.1), (202.8, 220)])
fcontact(214.7, 207.8); inner([(214.7, 208.6), (214.7, 212.7), (211.6, 212.7), (211.6, 220)])
blade(199, 212.5, 214.7, 203.7)
wire('213', [(202.8, 220), (202.8, 237), (137, 237), (137, 231)], 145, 235.5)
wire('215', [(193.9, 220), (193.9, 225), (190, 225)], label=False); tag(188, 225, f'215 SV 0.75 → lighter 48 → earth', w=36, size=2.2, anchor='end')
# the right terminal's inverted V: 203 drawn first so 214's blue sits on top at the apex; 214's corner falls inside a dash
wire('203', [(211.6, 220), (209.8, 222), (209.8, 232.6), (228, 232.6)], label=False); tag(230, 232.6, f'203 BR 0.75 → tachometer 110 (instruments sheet)', w=53.2, size=2.2)
wire('214', [(211.6, 220), (213.4, 222), (213.4, 225.8), (228, 225.8)], label=False); tag(230, 225.8, '214 BL 0.75: feed, source not traced', w=38.5, size=2.2, dashed=True)
wire('211', [(116, 231), (116, 243), (292, 243), (292, 215), (300, 215)], 240, 241.5)
box(300, 210, 30, 10); A('<path d="M303,215 l2,-2 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,2" fill="none" stroke="#111" stroke-width=".4"/>')
A('<path d="M330,215 h6 v4" fill="none" stroke="#111" stroke-width=".6"/>'); earth(336, 219); txt(300, 229, '<tspan font-weight="bold">115</tspan> Heated rear window (D12)', 2.6)

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
yl = ly + (29 if TICKED[0] else 23)
if probable_legend(x, yl): yl += 6
if WORK[0]: work([(x, yl), (x + 9, yl)]); txt(x + 11, yl + 1, 'short dashes inside a switch: its other positions, as printed', 2.4)
notes = ['Radiator fan: relay 38 (drawn at rest, contact open) is fed from fuse 7 on the always-live bar; thermostat switch 39 earths its coil through 115 SV and the left',
         'headlamp’s earth, 28 SV, so the drawing lets the fan run after the engine is switched off. 114a is BL in the 1979 print, SV (black) in the 1977 Turbo diagram: car check E14.',
         'Heater fan: fuse 6 is on the ignition-on bar. Switch 35 rests on its unwired terminal (probably off); its short-dashed lines are its other positions, as printed: 8 feeds the',
         'motor directly; 6 goes through resistor 74, whose far lead lands on 57’s corner (the pin is hidden: probably row 1, grey). The motor returns through 57 row 3 on 107 SV to joint 158.',
         'Heated rear window: fuse 8 (always live) feeds relay 113 (at rest, open); switch 116, drawn off, energises it through 213 BL. Its right terminal takes the feed 214 BL (not traced)',
         'and 203 to the tachometer; its lamp is probably the “on” indicator. 113:85 also takes the earths 13 SV (relay 8) and 33 SV (relay 21); 212 SV carries all three earths (relays 113, 8 and 21) to earth joint 158.',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 4.8, n, 2.35, fill='#333')
save('climate.svg')

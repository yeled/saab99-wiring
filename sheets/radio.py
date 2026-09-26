#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo radio, speakers and accessory feeds sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Radio, speakers and accessory feeds',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407) and radio installation, PDF p. 798.')
def conn(x, y, h, lab, w=4):
    A(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    txt(x, y - h / 2 - 1.5, lab, 2.2, 'middle', fill='#555')
def speaker(x, y, n, name):
    A(f'<path d="M{x},{y - 5} h5 l6,-6 v22 l-6,-6 h-5 z" fill="#fff" stroke="#111" stroke-width=".7"/>')
    txt(x + 16, y - 1, f'<tspan font-weight="bold">{n}</tspan> {name}', 2.8)

# ---- ignition switch X and connector 58 (B9) -----------------------------
box(18, 104, 36, 22); txt(21, 110.5, '<tspan font-weight="bold">20</tspan> Ignition switch', 2.6)
dot(54, 120); txt(52, 121, 'X', 2.4, 'end'); txt(21, 116, 'X: live with key on', 2.2, fill='#555')
wire('340', [(54, 120), (165, 120), (165, 86)], 60, 118.5); conn(110, 120, 8, '58 (B9)')

# ---- radio junction box 122 (pins in physical order 1 5 2 6 3 7 4 8) ----------
box(155, 70, 90, 16); txt(200, 66, '122 Radio junction box, 8-pole (F7)', 2.8, 'middle', w='bold')
P = dict(zip(['1', '5', '2', '6', '3', '7', '4', '8'], [165, 175, 185, 195, 205, 215, 225, 235]))
for k, x in P.items():
    dot(x, 86); txt(x, 81, k, 2.4, 'middle')
txt(230, 92.5, '4, 8 unused', 2.1, 'middle', fill='#777')
wire('341', [(175, 86), (175, 98)], label=False); earth(175, 98); txt(175, 108.2, '341 SV 0.75', 2.2, 'middle')
wire('345', [(215, 86), (215, 130), (296, 130)], 240, 128.5)
wire('344', [(195, 86), (195, 140), (296, 140)], 240, 138.5)
wire('343', [(205, 86), (205, 170), (296, 170)], 240, 168.5)
wire('342', [(185, 86), (185, 180), (296, 180)], 240, 178.5)
conn(300, 135, 16, '59'); conn(300, 175, 16, '59')
for y1, y2 in ((130, 140), (170, 180)):
    A(f'<path d="M302,{y1} H330 M302,{y2} H330" stroke="#111" stroke-width=".6"/>')
speaker(330, 135, '130', 'Loudspeaker, right'); txt(325, 129, '−', 3, 'end'); txt(325, 143, '+', 3, 'end')
speaker(330, 175, '131', 'Loudspeaker, left'); txt(325, 169, '−', 3, 'end'); txt(325, 183, '+', 3, 'end')
txt(346, 141, 'left and right as on this car (I1)', 2.2, fill='#555'); txt(346, 144.5, 'and the radio page; the Turbo diagram swaps them', 2.2, fill='#555')

# ---- accessory feeds on fuse 9 ---------------------------------------------------
txt(18, 208, 'Accessory feeds', 3.2, w='bold')
# fuse 9 of fuse box 22, turned a quarter: the manual's bar 7-12 runs left, its junction ring feeds the 8 A fuse, and
# bottom terminal 9 is the dot on the box edge
box(18, 212, 36, 20); txt(21, 217, f'<tspan font-weight="bold">F9</tspan> · {FUSES[9]["rating"]}', 2.6)
inner([(24, 219.5), (24, 229.5)]); contact(24, 222); txt(26, 229, 'always-live bar', 2.1, fill='#555')
fa, fb = fuse(32, 220.8, 10, 2.4); inner([(24.8, 222), fa]); inner([fb, (54, 222)]); dot(54, 222); tlabel(52.5, 220.6, '9', 'end')
# 58 (B11): one of its pin rows, dots just inside the frame as the manual prints them; 126 BL in, 160 GL on out of the
# same pin, and 126a BL leaving on the fuse side, its join to the pin hidden in the manual's frame (grey)
A('<rect x="129" y="215" width="12" height="14" fill="#ddd" stroke="#111" stroke-width=".5"/>'); txt(135, 213.3, '58 (B11)', 2.2, 'middle', fill='#555')
wire('126', [(54, 222), (132.5, 222)], 60, 220.5)
wire('160', [(137.5, 222), (145, 222), (145, 209), (124, 209)], label=False); tag(124, 209, '160 GL 0.75 to interior lights via 58 (A9)', size=2.4, anchor='end')
wire('126a', [(128.4, 226.1), (126.5, 228), (126.5, 238), (180, 238), (180, 222), (200, 222)], 140, 236.5)
A('<rect x="129" y="215" width="12" height="14" fill="none" stroke="#111" stroke-width=".5"/>')   # frame over the wire ends
inner([(132.5, 222), (137.5, 222)]); inner([(132.5, 222), (128.4, 226.1)], grey=True); dot(132.5, 222); dot(137.5, 222)
A('<circle cx="208" cy="222" r="7" fill="#111"/>'); txt(218, 223, '<tspan font-weight="bold">48</tspan> Cigarette lighter', 2.8)
wire('215', [(208, 229), (208, 234)], 212.5, 237); earth(208, 234)   # labels clear of the earth bar's end (x 211)
A('<circle cx="208" cy="192" r="8" fill="#fff" stroke="#111" stroke-width=".7"/><path d="M208,192 v-5 M208,192 h4" stroke="#111" stroke-width=".5"/>')
txt(219, 193, '<tspan font-weight="bold">49</tspan> Clock', 2.8)
wire('127', [(200, 192), (180, 192), (180, 222)], 181, 190.5); dot(180, 222)
wire('128', [(208, 200), (208, 205)], 212.5, 207.5); earth(208, 205)

# ---- legend and notes ---------------------------------------------------------------
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
notes = ['Pin numbers and speaker polarity (342, 344 to +; 343, 345 to −) are from the radio installation page, PDF p. 798.',
         'The radio’s + (340 RD) comes from ignition switch X here, so it’s live with the key on; the radio page describes a battery feed.',
         'Left and right as on this car (check I1): right-hand speaker 344/345, left-hand 342/343, as the radio page shows; the 1979 Turbo diagram swaps them.',
         'Fuse 9 (lid: cigar lighter, compartment light, clock): the 58 (B11) pin that 126 BL enters carries on as 160 GL to the interior lights.',
         '126a BL to the lighter leaves 58 (B11) on the fuse side; the manual hides its join in the frame, so it’s grey. The clock’s 127 BL takes off 126a.',
         'The radio page puts the junction box in the right-hand trim panel under the dash; that’s for LHD cars.']
for j, n in enumerate(notes): txt(lx + 108, ly + 6 + j * 5.4, n, 2.35, fill='#333')
save('radio.svg')

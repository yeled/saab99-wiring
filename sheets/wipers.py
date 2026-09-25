#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo wipers and washers sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Wipers and washers',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual.')
def term(x, y, t, side):
    dot(x, y); txt(x + (1.8 if side == 'l' else -1.8), y + (-1.3 if side in 'lr' else 3.4), t, 2.2, 'start' if side == 'l' else 'end')
def motor(x, y, r=7):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(x, y + 1.2, 'M', 3, 'middle', w='bold')
def jdot(x, y):
    """Small junction dot inside a part."""
    A(f'<circle cx="{x}" cy="{y}" r=".55" fill="#111"/>')
def glabel(x, y, t, anchor='start'):
    """Terminal label that is probable (printed but not readable): tlabel size, probable grey."""
    txt(x, y, t, 1.8, anchor, fill='#888')
def ptc(x, y, w=6, h=2):
    """Resistor with a diagonal that overshoots both ends, as the manual prints it in motor 66 (probably a thermal cut-out).
    Mirrored like the rest of 66: from the housing top at upper left down to the motor circle at lower right."""
    a, b = resistor(x, y, w, h)
    A(f'<path d="M{x + w + .8},{y + h + 1} L{x - .8},{y - 1}" stroke="#111" stroke-width=".35"/>')
    return a, b
def bar_feed(y0, name, sub, n=None, rating=None):
    """A stub of fuse box 22, drawn like F9 on the radio sheet: the bar (a thin upright with its junction ring),
    then fuse n when given, to the terminal dot on the box's right edge at y0 + 10."""
    box(18, y0, 36, 20); txt(21, y0 + 5, name, 2.6)
    yc = y0 + 10
    inner([(24, y0 + 7.5), (24, y0 + 17.5)]); contact(24, yc); txt(26, y0 + 17, sub, 2.1, fill='#555')
    if n:
        fa, fb = fuse(32, yc - 1.2, 10, 2.4); inner([(24.8, yc), fa]); inner([fb, (54, yc)]); tlabel(52.5, yc - 1.4, str(n), 'end')
    else:
        inner([(24.8, yc), (54, yc)])
    dot(54, yc)
    return 54, yc

# ================= windscreen wipers =================================================================================
txt(18, 40, 'Windscreen wipers and washer', 3.4, w='bold')

# fuse 4: one terminal with three legs, as in the manual (85 to the switch, 85a to the motor, 85a to the relay)
fx, fy = bar_feed(86, f'<tspan font-weight="bold">F4</tspan> · {FUSES[4]["rating"]}', 'ignition-on bar', 4)
wire('85a', [(fx, fy), (57, fy - 3), (57, fy - 8), (61, fy - 8)], label=False); tag(61, fy - 8, '85a BR 0.75 → wiper motor 62 (4)', size=2.4)
wire('85a#relay', [(fx, fy), (57, fy + 3), (57, fy + 8), (61, fy + 8)], label=False); tag(61, fy + 8, '85a BR 0.75 → interval relay 83', size=2.4)
wire('85', [(fx, fy), (158, fy), (158, 91)], 64, fy - 1.5); dot(fx, fy)   # 85 over the 85a legs, then the terminal

# ---- 61 wiper switch, drawn as the manual prints it (lever at rest, probably 'off'). Terminals: bottom edge 31b, S,
# 54c, 53a; right edge INT, 53, 53b. Grey = probable: the labels the print doesn't show clearly, and the T1-53 join.
X0, Y0, W, H = 112, 45, 72, 46
box(X0, Y0, W, H)
txt(146, 42.6, '61 Wiper switch', 2.7, 'middle', w='bold'); txt(158.5, 42.6, '(D9)', 2.2, fill='#555')
YB = Y0 + H                                            # bottom edge
for x in (121, 129, 136, 158): dot(x, YB)
glabel(119.6, YB - 1.6, '31b', 'end'); tlabel(127.6, YB - 1.6, 'S', 'end'); glabel(138.3, YB - 1.2, '54c')
for y, t in ((56.5, 'INT'), (64, '53'), (72, '53b')):   # right edge: terminal, lead, inner circle
    dot(X0 + W, y); inner([(X0 + W, y), (178.5, y)]); contact(177.7, y); glabel(182.6, y - 1.3, t, 'end')
inner([(176.9, 56.5), (173, 56.5)]); inner([(176.9, 64), (172.6, 64)]); inner([(177, 71.8), (173.6, 70.9)])   # fixed fingers: printed at line weight
# lever: pivots on S0 (tied to 31b, and to R), rests on U through a short neck; its tip reaches into the inverted L, as printed
contact(123.7, 83); inner([(121, YB), (123.45, 83.76)]); contact(120.8, 74.9); inner([(123.43, 82.25), (121.07, 75.65)])
blade(124.27, 82.6, 171.5, 49.55)
contact(133.8, 72.8); blade(133.8, 75.6, 133.8, 73.7)
# U, up and over (the inverted L) and down to T1, which faces the 53 finger across a printed gap: probably joined
inner([(133.8, 72), (133.8, 47.5), (178.4, 47.5), (178.4, 49.5), (169.5, 56.7), (169.5, 63.2)]); contact(169.5, 64)
inner([(170.3, 64), (172.6, 64)], grey=True)
# 53a stack: three fixed contacts on one upright from the 53a circle, facing INT (via line 1), T1/53 and 53b
inner([(163.6, 60.9), (163.6, 79.7)])
for y in (60.1, 64, 68.9): contact(163.6, y)
# the printed position line 1 segment, so INT pairs with the top stack contact and not with the L it crosses
PLINE = 'stroke="#999" stroke-width=".3" stroke-dasharray=".8 .6"'
A(f'<path d="M164.3,59.8 L172.3,56.6" {PLINE} stroke-dashoffset=".4"/>')   # a dash centred where it crosses the L
contact(163.6, 80.5); tlabel(165.3, 81.2, '53a')
inner([(163.6, 81.3), (163.6, 85.3), (158, YB)])      # 53a circle to its bottom terminal (85 BR)
# F (fast, feeds S) faces the stack; F and S both run to Q; P-Q is printed closed, so 54c joins them (probably a misprint)
contact(160, 66.5); inner([(159.49, 67.11), (147.2, 78.8), (147.2, 80.9)])
inner([(129, YB), (138.2, 78.8), (147.2, 78.8)]); jdot(147.2, 78.8)
contact(147.2, 81.7); contact(141.1, 81.7); inner([(141.9, 81.7), (146.4, 81.7)])
inner([(140.7, 82.4), (136, YB)])
# washer contact: blade pivoting on the 53a circle, open, its tip facing Q
blade(162.9, 80.75, 150.4, 82.1)
# probable switching, from the geometry and the manual's text (the book prints no positions)
tx, ty = 66, 52
txt(tx, ty, 'Positions (probably; the manual prints none)', 2.1, fill='#777')
for j, s in enumerate(['0 off: 31b–53 (park)', '1 interval: 31b–53 and 53a–INT', '2 slow: 53a–53',
                       '3 fast: 53a–53b and 53a–S', '4 washer (pull): 53a–S, 54c']):
    txt(tx + 1.5, ty + 4 + j * 3.4, s, 2.1, fill='#777')
A(f'<path d="M{tx + 1.5},{ty + 20.3} h4" {PLINE}/>'); txt(tx + 7, ty + 21, 'printed position line (53a–INT)', 2.1, fill='#777')

wire('86', [(184, 64), (392, 64), (392, 95), (370, 95)], 206, 62.5)
wire('87', [(184, 72), (386, 72), (386, 89), (370, 89)], 206, 70.5)
wire('84', [(184, 56.5), (196, 56.5), (196, 130), (230, 130)], 200, 128.5)
wire('88', [(121, YB), (121, 142), (230, 142)], 200, 140.5)
wire('91', [(136, YB), (136, 154), (230, 154)], 200, 152.5)
box(230, 120, 42, 50); txt(251, 162, '83 Interval', 2.7, 'middle', w='bold'); txt(251, 166, 'relay (D8)', 2.7, 'middle', w='bold')
for y in (130, 142, 154): dot(230, y)
dot(251, 120); txt(253, 124, '85a', 2.2); wire('85a#relay', [(251, 120), (251, 112)], label=False); tag(249, 112, '85a BR 0.75 ← fuse 4', anchor='end')
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

# ================= headlight wipers ==================================================================================
txt(18, 196, 'Headlight wipers', 3.4, w='bold')
bx, by = bar_feed(201, '<tspan font-weight="bold">Bar 3–6</tspan>', 'ignition on, unfused')
wire('94', [(bx, by), (96, 211)], 60, 209.5)
# 65: the 3 A fuse between two clips, as printed
box(96, 204, 24, 14); txt(108, 201.8, '65 Fuse holder', 2.2, 'middle', w='bold')
dot(96, 211); dot(120, 211); inner([(96, 211), (98.7, 211)]); contact(99.5, 211); contact(116.5, 211)
fa, fb = fuse(103, 209.8, 10, 2.4, rating='3 A'); inner([(100.3, 211), fa]); inner([fb, (115.7, 211)]); inner([(117.3, 211), (120, 211)])
# relay 67 with its contacts and coil, in the rest position as the manual draws it
wire('95', [(120, 211), (128, 211), (128, 216), (140, 216)], label=False); txt(121, 220, '95 RD 0.75', 1.9, fill='#555'); dot(128, 216)
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
mlink([(160, 221), (160, 207.8)])   # mechanical link from the coil to both contacts
wire('100', [(140, 207), (134, 207), (134, 186), (138, 186)], label=False); tag(140, 186, '100 SV 0.75 → earth at relay 102')
wire('96', [(170, 232), (170, 238), (176, 238)], label=False); tag(178, 238, '96 GR 0.75 ← wiper switch 61 (via 58 D8)')
wire('100a', [(150, 232), (150, 238)], label=False); tag(147, 241, '100a SV 0.75: coil 85, ends on the drawing', anchor='end')

# ---- 123 plugs and 66 motors. Drawn mirrored left to right (the manual has the plug right of the motor) so the harness
# comes in from the left: pins keep their top-to-bottom order. Rows of 123 are through-links, a dot on each side.
PX, MX, P = 268, 283, 4.5                              # plug harness side, motor pin wall, row pitch
def plug(r1, rows):
    ys = [r1 + P * (k - 1) for k in rows]
    A(f'<rect x="{PX}" y="{r1 - 2.5}" width="6" height="{3 * P + 5}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    for y in ys:
        inner([(PX, y), (PX + 6, y)]); dot(PX, y); dot(PX + 6, y)
        A(f'<path d="M{PX + 6},{y} H{MX}" stroke="#111" stroke-width=".6"/>')
    txt(PX + 10.5, r1 - 1.4, '123', 2.1, 'middle', fill='#555')
def hl_motor(r1, pin3=True):
    """Headlight wiper motor 66 as printed (mirrored): diode and thermal resistor on the pin 1 line to M, park switch
    (open) from pin 2 to junction J, pin 4 the return; the upper motor's pin 3 has nothing inside."""
    r2, r3, r4 = r1 + P, r1 + 2 * P, r1 + 3 * P
    top, bot = r1 - 3.5, r4 + 3.5; mid, R = (top + bot) / 2, (bot - top) / 2
    xc = MX + 31.5
    A(f'<path d="M{MX},{top} H{xc} A{R},{R} 0 0 1 {xc},{bot} H{MX} Z" fill="#fafafa" stroke="#111" stroke-width=".8"/>')
    motor(xc, mid, 7.5)
    xm = round(xc - (7.5 ** 2 - (r1 - mid) ** 2) ** .5, 2)          # where the pin 1 and pin 4 lines meet M
    an, ca = diode(MX + 5.2, r1, 'r', s=2.4)                          # conducts from pin 1 to J
    J = MX + 12.5; jdot(J, r1)
    ra, rb = ptc(MX + 14.5, r1 - 1.1, 7, 2.2)
    inner([(MX, r1), an]); inner([ca, (J, r1), ra]); inner([rb, (xm, r1)])
    pv = MX + 8.4; fy = r2 + 5.3                                      # park switch: pivot at pin 2, fixed contact below it
    inner([(MX, r2), (pv - .8, r2)]); contact(pv, r2); contact(pv, fy)
    blade(pv - .35, r2 + .65, pv - 2.0, fy - 1.25)
    inner([(J, r1), (J, fy), (pv + .8, fy)])
    inner([(MX, r4), (xm, r4)])
    for y in ([r1, r2, r3, r4] if pin3 else [r1, r2, r4]): dot(MX, y)
    txt(xc + R + 3, mid + 1, '<tspan font-weight="bold">66</tspan> Headlight wiper motor', 2.6)
    return r1, r2, r3, r4
U1, U2, U3, U4 = hl_motor(195); plug(195, (1, 2, 3, 4))
L1, L2, L3, L4 = hl_motor(225, pin3=False); plug(225, (1, 2, 4))
wire('95a', [(128, 216), (128, 192), (261, 192), (PX, U2)], 194, 190.5)
wire('98', [(180, 216), (246, 216), (246, 188), (PX, 188), (PX, U1)], 192, 214.5)
wire('95b', [(PX, U2), (253, U2), (253, L2), (PX, L2)], 250.9, 226, rot=-90)
wire('97', [(PX, U3), (260, U3), (260, L1), (PX, L1)], label=False); txt(257.8, 222.5, '97 BR 0.75', 2.1, rot=-90)
wire('99', [(PX, U4), (265, U4), (265, U4 + 4.5)], label=False); earth(265, U4 + 4.5); txt(269.5, U4 + 8.3, '99 SV 0.75', 2.1)   # off the plug's edge, like 99a
wire('99a', [(PX, L4), (262, L4), (262, L4 + 2)], label=False); earth(262, L4 + 2); txt(266, L4 + 7.3, '99a SV 0.75', 2.1)
for y in (U1, U2, U3, U4, L1, L2, L4): dot(PX, y)   # harness-side pin dots over the wire ends

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
probable_legend(x, ly + (29 if TICKED[0] else 23))
notes = ['Wipers run from fuse 4 on the ignition-on bar: 85 BR to the switch (53a) and two 85a BR leads, to the interval relay and to motor terminal 4.',
         'The washer switch signal (91 GL) goes to the interval relay, which feeds the washer pump (91a GL), so it can wipe while washing.',
         'Speed wires: 87 GN to motor terminal 3, 86 RD to terminal 5 (through connector 58 at D8); 85a feeds 4, 88a is the park contact (2).',
         'Switch 61 as printed, at rest: the park line from the lever (up, over and down) stops short of 53’s contact (grey: probably joined, for park); '
         'the link between the circles on the 54c and S lines is printed closed, tying S to 54c (probably a misprint).',
         'S has no wire printed (probably 96 GR to relay 67). Headlight wipers: unfused tap 94 BR from bar 3–6, a 3 A glass fuse in holder 65 (manual, PDF p. 30), relay 67.',
         'Relay 67: 88 is + from the 3 A fuse; 95a RD takes it to upper plug row 2 (probably) and 95b RD on to lower row 2 (the park switches); '
         '88a switches 98 GL to the upper motor’s diode (row 1). Rows of 123 counted from the top (none printed); 66 and 123 drawn mirrored.',
         '97 BR runs from upper plug row 3 (nothing inside motor 66 uses it) to lower plug row 1, so as printed the lower motor gets no start feed; '
         'on the car both run together (E10), so the book leaves out a link, probably row 3 to row 1 inside the upper motor.',
         'Diagram is not RHD-specific; the switch and relay positions (D8/D9) are drawing grid squares, not locations in the car. '
         'Light-grey terminal labels on 61 (31b, 54c, INT, 53, 53b) are probable; S and 53a are read.']
for j, n in enumerate(notes): txt(lx + 108, ly + 5.3 + j * 4.2, n, 2.3, fill='#333')
save('wipers.svg')

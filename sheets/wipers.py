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
def ftag(x, y, text, anchor='start', size=2.4):
    """tag() sized to its text: the default width runs long for these longer tags."""
    return tag(x, y, text, w=round(len(text) * size * .46 + 4, 1), size=size, anchor=anchor)

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
# printed position lines, as the book draws them: thin grey dashes through the lever's pivot, one per notch, drawn
# first so the contacts sit on top. 1 runs from R through U to the INT finger (via the top 53a contact), 2 to the 53 finger
# (F's flat top, middle contact, T1), 3 to the 53b finger (F, bottom contact); 2 and 3 end on nothing at the left and cross
# U's riser without a contact. The lever itself is 0.
PLINE = 'stroke="#999" stroke-width=".3" stroke-dasharray=".8 .6"'
PIV = (149.96, 64.62)                                  # pivot boss on the lever
POSLINES = {'1': [(120.8, 74.9), PIV, (173, 56.5)], '2': [(118.98, 65.47), PIV, (172.6, 64)],
            '3': [(119.99, 56.72), PIV, (173.6, 70.85)]}
for pts in POSLINES.values(): A(f'<path d="{path(pts)}" fill="none" {PLINE}/>')
YB = Y0 + H                                            # bottom edge
for x in (121, 129, 136, 158): dot(x, YB)
glabel(119.6, YB - 1.6, '31b', 'end'); tlabel(127.6, YB - 1.6, 'S', 'end'); glabel(138.3, YB - 1.2, '54c')
for y, t in ((56.5, 'INT'), (64, '53'), (72, '53b')):   # right edge: terminal, lead, inner circle
    dot(X0 + W, y); inner([(X0 + W, y), (178.5, y)]); contact(177.7, y); glabel(182.6, y - 1.3, t, 'end')
inner([(176.9, 56.5), (173, 56.5)]); inner([(176.9, 64), (172.6, 64)]); inner([(177, 71.8), (173.6, 70.9)])   # fixed fingers: printed at line weight
# lever: S0 at its lower end (tied to 31b, and to R); pivots on the boss PIV; joined to U through a short neck; its tip
# reaches into the inverted L, as printed. The white slots either side of the boss (as printed) insulate its two arms.
contact(123.7, 83); inner([(121, YB), (123.45, 83.76)]); contact(120.8, 74.9); inner([(123.43, 82.25), (121.07, 75.65)])
blade(124.27, 82.6, 171.5, 49.55)
LV0, LV1 = (123.7, 83), (171.5, 49.55)                 # S0 and the tip: slots at the printed fractions of that length
lv = lambda t: (round(LV0[0] + t * (LV1[0] - LV0[0]), 2), round(LV0[1] + t * (LV1[1] - LV0[1]), 2))
for t0, t1 in ((.39, .49), (.575, .705)):
    (a0, b0), (a1, b1) = lv(t0), lv(t1)
    A(f'<path d="M{a0},{b0} L{a1},{b1}" stroke="#fff" stroke-width=".22" stroke-linecap="round"/>')
A(f'<circle cx="{PIV[0]}" cy="{PIV[1]}" r=".9" fill="#111"/><circle cx="{PIV[0]}" cy="{PIV[1]}" r=".3" fill="#fff"/>')   # pivot boss
contact(133.8, 70.3); blade(133.8, 75.6, 133.8, 71.2)   # U sits on line 1, as printed (line 1 runs R, U, pivot)
# U, up and over (the inverted L) and down to T1, which faces the 53 finger across a printed gap: probably joined
inner([(133.8, 69.5), (133.8, 47.5), (178.4, 47.5), (178.4, 49.5), (169.5, 56.7), (169.5, 63.2)]); contact(169.5, 64)
inner([(170.3, 64), (172.6, 64)], grey=True)
# 53a stack: three fixed contacts on one upright from the 53a circle, facing INT (via line 1), T1/53 and 53b
inner([(163.6, 60.9), (163.6, 79.7)])
for y in (60.1, 64, 68.21): contact(163.6, y)            # on lines 1, 2 and 3
contact(163.6, 80.5); tlabel(165.3, 81.2, '53a')
inner([(163.6, 81.3), (163.6, 85.3), (158, YB)])      # 53a circle to its bottom terminal (85 BR)
# F (fast, feeds S) sits on line 3, facing the stack; its flat top, printed on line 2, is why S and 54c at 2 are '?'.
# F and S both run to Q; P-Q is printed closed, so 54c joins them (probably a misprint)
inner([(160, 66.47), (160, 64.35)]); A('<path d="M159.1,64.35 H160.9" stroke="#111" stroke-width=".45"/>')
contact(160, 67.27); inner([(159.41, 67.81), (147.2, 78.8), (147.2, 80.9)])
inner([(129, YB), (138.2, 78.8), (147.2, 78.8)]); jdot(147.2, 78.8)
contact(147.2, 81.7); contact(141.1, 81.7); inner([(141.9, 81.7), (146.4, 81.7)])
inner([(140.7, 82.4), (136, YB)])
# washer contact: blade pivoting on the 53a circle, open, its tip facing Q
blade(162.9, 80.75, 150.4, 82.1)
# position numbers at the free (S0) end of each line: 0 the lever by S0, 4 the washer blade. The 1979 page prints none;
# 0-3 follow the GLE figure (p. 370, which puts them at the handle end), 4 its text (p. 371)
def posnum(x, y, n):
    A(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#fff" stroke="#888" stroke-width=".25"/>'); txt(x, y + .72, n, 2, 'middle', w='bold', fill='#777')
for n, (x, y) in (('0', (120.3, 85.4)), ('1', (117.9, 75.9)), ('2', (116.2, 65.6)), ('3', (117.2, 56.0)), ('4', (153, 84.8))):
    posnum(x, y, n)
for x, y, t, anc in ((161.1, 66.3, 'F', 'start'), (139.9, 82.4, 'P', 'end'), (148.2, 84.4, 'Q', 'start')):   # our names, used in the notes
    glabel(x, y, t, anc)

# ---- 61 switching table, Bosch style: a column per terminal, a row per position; dots on the terminals a position
# joins, a bar through each group. Black = read on the 1979 print, grey = probably, dotted grey with ? = unsure.
# From the reconciled reading (book photo, scan, GLE text p. 370-371); groups in one row stay separate bars.
TX, TY, NW, CW, RH = 51, 52.0, 22.5, 4.9, 4.6              # left, grid top, name column, cell width, row height
TCOL = [('31b', 'BL'), ('53', 'RD'), ('53a', 'BR'), ('INT', 'GN/VT'), ('53b', 'GN'), ('S', 'GR'), ('54c', 'GL')]   # label, wire colour
# headers print dark: grey in the table means a probable join (the switch symbol shows which labels are probable)
POS61 = [('0', 'off', [(0, 1, 'p')], {0: 'p', 1: 'p'}),
         ('1', 'intermittent', [(0, 1, 'p'), (2, 3, 'r')], {0: 'p', 1: 'p', 2: 'r', 3: 'r'}),
         ('2', 'slow', [(1, 2, 'r'), (2, 6, 'u')], {1: 'r', 2: 'r', 5: '?', 6: '?'}),
         ('3', 'fast', [(2, 4, 'r'), (4, 5, 'p'), (5, 6, 'u')], {2: 'r', 4: 'r', 5: 'p', 6: '?'}),
         ('4', 'washer (pull from 0)', [(0, 1, 'p'), (2, 6, 'p')], {0: 'p', 1: 'p', 2: 'p', 5: 'p', 6: 'p'})]
XR = TX + NW + 7 * CW                                      # right edge
cx = lambda i: TX + NW + (i + .5) * CW
txt(TX, TY - 6.6, '61 positions: terminals joined', 2.4, w='bold', fill='#333')
for i, (t, c) in enumerate(TCOL):
    txt(cx(i), TY - 3.2, t, 2.1, 'middle', fill='#333')
    if c:                                                  # the cable's colour, as on the wires leaving the switch
        cols = c.split('/'); sx = cx(i) - 1.6
        A(f'<path d="M{sx},{TY - 1.4} h3.2" stroke="#222" stroke-width="1.3"/><path d="M{sx},{TY - 1.4} h3.2" stroke="{COL[cols[0]]}" stroke-width=".8"/>')
        if len(cols) == 2: A(f'<path d="M{sx},{TY - 1.4} h3.2" stroke="{COL[cols[1]]}" stroke-width=".4" stroke-dasharray=".8 .8"/>')
grid = [f'M{TX},{TY + j * RH:.2f} H{XR:.2f}' for j in range(6)] + [f'M{TX + NW + i * CW:.2f},{TY} V{TY + 5 * RH:.2f}' for i in range(8)]
A(f'<path d="{" ".join(grid)}" stroke="#ccc" stroke-width=".2"/>')
INK = {'r': '#111', 'p': '#888', 'u': '#888'}
for j, (n, name, bars, dots) in enumerate(POS61):
    y = round(TY + (j + .5) * RH, 2)
    posnum(TX + 1.5, y, n); txt(TX + 3.6, y + .75, name, 2.1, fill='#333')
    for a, b, k in bars:                                   # a bar hops over each column it passes without joining
        dash = ' stroke-dasharray=".05 .75" stroke-linecap="round" stroke-width=".55"' if k == 'u' else ' stroke-width=".7"'
        d = f'M{cx(a):.2f},{y}'
        for i in range(a + 1, b):
            if i not in dots: d += f' H{cx(i) - 1.1:.2f} A1.1,1.1 0 0 1 {cx(i) + 1.1:.2f},{y}'
        A(f'<path d="{d} H{cx(b):.2f}" fill="none" stroke="{INK[k]}" stroke-linejoin="round"{dash}/>')
    for i, k in dots.items():
        if k == '?':
            A(f'<circle cx="{cx(i):.2f}" cy="{y}" r="1" fill="#fff"/>'); txt(round(cx(i), 2), y + .75, '?', 2.1, 'middle', w='bold', fill='#888')
        else:
            A(f'<circle cx="{cx(i):.2f}" cy="{y}" r=".85" fill="{INK[k]}"/>')
ky = TY + 5 * RH + 2.9
A(f'<circle cx="{TX + 1}" cy="{ky - .7}" r=".85" fill="#111"/>'); txt(TX + 2.5, ky, 'read', 2, fill='#333')
A(f'<circle cx="{TX + 10}" cy="{ky - .7}" r=".85" fill="#888"/>'); txt(TX + 11.5, ky, 'probably', 2, fill='#333')
A(f'<path d="M{TX + 23},{ky - .7} h3.5" stroke="#888" stroke-width=".55" stroke-dasharray=".05 .75" stroke-linecap="round"/>')
txt(TX + 27.3, ky, 'unsure', 2, fill='#333')
A(f'<path d="M{TX + 37},{ky - .7} H{TX + 38.1} A1.1,1.1 0 0 1 {TX + 40.3},{ky - .7} H{TX + 41.4}" fill="none" stroke="#111" stroke-width=".7" stroke-linejoin="round"/>')
txt(TX + 42.4, ky, 'hop: not joined', 2, fill='#333')
txt(TX, ky + 2.8, '?: at 2, S only if F’s flat top (printed on line 2) is a contact;', 2, fill='#333')
txt(TX, ky + 5.6, '54c at 2 and 3 only through P–Q (probably a misprint).', 2, fill='#333')

wire('86', [(184, 64), (392, 64), (392, 95), (370, 95)], 206, 62.5)
wire('87', [(184, 72), (386, 72), (386, 89), (370, 89)], 206, 70.5)
wire('84', [(184, 56.5), (196, 56.5), (196, 130), (230, 130)], 200, 128.5)
wire('88', [(121, YB), (121, 142), (230, 142)], 200, 140.5)
wire('91', [(136, YB), (136, 154), (230, 154)], 200, 152.5)
wire('96', [(129, YB), (129, 104), (140, 104)], label=False); ftag(140, 104, '96 GR 0.75 → relay 67:86 (below)')   # S, via 58 (D8)
box(230, 120, 42, 50); txt(251, 162, '83 Interval', 2.7, 'middle', w='bold'); txt(251, 166, 'relay (D8)', 2.7, 'middle', w='bold')
for y in (130, 142, 154): dot(230, y)
dot(251, 120); txt(253, 124, '85a', 2.2); wire('85a#relay', [(251, 120), (251, 112)], label=False); tag(249, 112, '85a BR 0.75 ← fuse 4', anchor='end')
dot(272, 130); dot(272, 154)
wire('88a', [(272, 130), (382, 130), (382, 107), (370, 107)], 290, 128.5)
wire('91a', [(272, 154), (320, 154)], 280, 152.5)
dot(320, 154); inner([(320, 154), (323.4, 154)])   # 63's feed terminal, a stem to the circle like the earth side
E158 = '→ earth joint 158 (power sheet)'
wire('83', [(251, 170), (251, 180), (255, 180)], label=False); dot(251, 170); ftag(255, 180, f'83 SV 0.75 {E158}')
motor(327, 160); txt(337, 158, '63 Washer pump', 2.7, w='bold'); txt(337, 162.5, '(F4)', 2.2, fill='#555')
# 63's earth terminal: 92 SV on to joint 158, and 361 SV brings in the right front lamp housing's earth
inner([(327, 167), (327, 169)])
wire('92', [(327, 169), (327, 177), (331, 177)], label=False); ftag(331, 177, f'92 SV 1.0 {E158}')
wire('361', [(327, 169), (334, 169)], label=False); ftag(334, 169, '361 SV 1.0 ← right front lamp housing (lighting sheet)')
dot(327, 169)
box(330, 84, 40, 30); motor(342, 99, 6); txt(350, 80.5, '62 Wiper motor (F4)', 2.7, 'middle', w='bold')
for t, y in (('3', 89), ('5', 95), ('4', 101), ('2', 107)): dot(370, y); txt(368, y + 1, t, 2.2, 'end')
dot(350, 114); txt(352, 112.5, '1', 2.2)
# 89 SV loops from terminal 1 back to the housing's lower-right corner, where 90 BL leaves for joint 158
# (label read at 62; its 1979 run crosses a scan seam, so probably; the 1977 diagram draws it)
wire('89', [(350, 114), (350, 119), (370, 119), (370, 114)], label=False); txt(351.5, 123.2, '89 SV 0.75', 2.2)
wire('90', [(370, 114), (376, 114), (376, 140), (372, 140)], label=False); ftag(372, 140, f'90 BL 1.0 {E158}', anchor='end')
dot(370, 114); tlabel(368.6, 112.6, 'housing', 'end')
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
wire('100', [(140, 207), (134, 207), (134, 186), (140, 186)], label=False); ftag(140, 186, '100 SV 0.75 → relay 102:31 (ignition sheet)')
wire('96', [(170, 232), (170, 238), (178, 238)], label=False); tag(178, 238, '96 GR 0.75 ← wiper switch 61:S via 58 (D8)')
# 100a: a jumper outside the relay from 85 round to 87's lead, T-joined as the 1979 print draws it (1977: the full loop),
# so 100 SV earths the coil through 87; it crosses 95 without joining
wire('100a', [(150, 232), (150, 238), (134, 238), (134, 207)], label=False); dot(134, 207); txt(135.6, 242.2, '100a SV 0.75', 2.1)

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

lx, ly = 18, 249
box(lx, ly, 389, 38, fill='#fff', sw=.5)
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
py = ly + (35 if TICKED[0] else 29)                   # switch 61's position lines and their numbers
A(f'<path d="M{x},{py} h9" {PLINE}/>'); posnum(x + 11.3, py, '2'); txt(x + 14, py + 1, 'switch position line, as printed (numbered as the GLE figure)', 2.4)
notes = ['Wipers run from fuse 4 on the ignition-on bar: 85 BR to the switch (53a) and two 85a BR leads, to the interval relay and to motor terminal 4.',
         'The washer switch signal (91 GL) goes to the interval relay, which feeds the washer pump (91a GL), so it can wipe while washing. '
         'Relay and pump earth at joint 158 (83 SV, 92 SV); 361 SV, the right front lamp housing’s earth, shares the pump’s earth terminal.',
         'Speed wires: 87 GN to motor terminal 3, 86 RD to terminal 5 (through connector 58 at D8); 85a feeds 4, 88a is the park contact (2). '
         '89 SV joins terminal 1 to the housing, which 90 BL (probably; the 1977 diagram draws it) earths at joint 158.',
         'Switch 61 as the book draws it: lever at rest (0), a dashed line per notch through the pivot, no numbers (ours as the GLE figure, p. 370; 4 its text). '
         'White slots insulate the lever’s arms: its 31b and 53a sides join apart. Pulling (4) adds S and 54c to the 53a group.',
         'The park link from the lever (up, over and down) stops short of 53 (grey: probably joined; park, braking and interval need it). '
         'P–Q, between the 54c and S lines, is printed closed, so fast would run the washer: probably a misprint (GLE keeps them apart; D10).',
         'The 1977 Turbo diagram (addendum p. 53) draws the park link closed and has no S–54c link, which supports the table’s grey and unsure marks. '
         'It also draws 96 GR from S to 58; the 1979 print leaves out S to 58 (D8).',
         'Headlight wipers: unfused tap 94 BR from bar 3–6, a 3 A glass fuse in holder 65 (manual, PDF p. 30), relay 67. '
         'Outside 67, 100a SV joins 85 to 87 (the 1979 print draws a T, the 1977 the whole loop), so 100 SV earths the coil.',
         'Relay 67: 88 is + from the 3 A fuse; 95a RD takes it to upper plug row 2 (probably) and 95b RD on to lower row 2 (the park switches); '
         '88a switches 98 GL to the upper motor’s diode (row 1). Rows of 123 counted from the top (none printed); 66 and 123 drawn mirrored.',
         '97 BR runs from upper plug row 3 (nothing inside motor 66 uses it) to lower plug row 1, so as printed the lower motor gets no start feed; '
         'on the car both run together (E10), so the book leaves out a link, probably row 3 to row 1 inside the upper motor.',
         'Diagram is not RHD-specific; the switch and relay positions (D8/D9) are drawing grid squares, not locations in the car. '
         'Light-grey terminal labels on 61 (31b, 54c, INT, 53, 53b) are probable; S and 53a are read.']
for j, n in enumerate(notes): txt(lx + 108, ly + 4.3 + j * 3.5, n, 2.3, fill='#333')
save('wipers.svg')

#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE power-distribution sheet (A3 landscape SVG).

Battery, starter terminal 30, alternator with its separate regulator, ignition switch and its connector 58, ignition
switch relay 21, fuse box 22 with every fuse output tagged with where it goes, and the single horn on fuse 11. Wire
identity, colour, size and status come from data/wires.csv.
Sources (for the code, never printed): base diagram PDF p.327 (371-23, RHD 1974), book photos P1 (fuse box),
P3 (starter, alternator, regulator), P9a/P9b (relay 21); horn contact 41 from p.327 (P9a cuts it off at its right
edge); injection detail S 3783 (p.347, 234 RD); automatic detail S 3981 (p.348, 54bf, 84e).
"""
from common import *                       # common.wire() sets STUB/DASHED when it draws one; the legend reads them

header('Saab 99 LE, model 1974 — Power distribution')


def name(x, y, n, s, size=2.7, nsize=4):
    """Part name: bold number, then the name (two text elements: cairosvg misplaces a bold tspan in centred text)."""
    txt(x, y, n, nsize, w='bold'); txt(x + len(n) * nsize * .58 + 1.4, y, s, size)

def mtag(x, y, l1, l2, w, anchor='start', dashed=False):
    """Two-line destination tag at (x, y-centre), boxed as the Turbo power sheet's two-line index tags."""
    x0 = x if anchor == 'start' else x - w
    dash = ' stroke-dasharray="1.5 1"' if dashed else ''
    A(f'<rect x="{round(x0, 2)}" y="{y - 4.45}" width="{w}" height="8.9" rx="1" fill="#fff" stroke="#444" stroke-width=".4"{dash}/>')
    txt(round(x0 + 1.5, 2), round(y - .75, 2), l1, 2.6); txt(round(x0 + 1.5, 2), round(y + 2.8, 2), l2, 2.6)
    return x0 + w

PIN = lambda n: 5 if n else 4               # length along the run: 4 mm (the Turbo's conn()); 5 with a pin number, which
                                           # needs room between the face dots (r 1.4 on the 1.5 mm² wires)
def pin_v(x, y, w=5, h=None, n=None):
    """One pin of a connector on a vertical run: grey block across it, PIN(n) mm along the run, centred (x, y); n: our
    pin number, inside.
    Dots go on the two faces after the wires."""
    h = h or PIN(n)
    A(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    if n: tlabel(x, y + .65, n, 'middle')
    return (x, y - h / 2), (x, y + h / 2)

def pin_h(x, y, w=None, h=5, n=None):
    """One pin of a connector on a horizontal run: grey block across it, PIN(n) mm along the run, centred (x, y)."""
    w = w or PIN(n)
    A(f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    if n: tlabel(x, y + .65, n, 'middle')
    return (x - w / 2, y), (x + w / 2, y)

def strap(pts):
    """Unnumbered heavy black lead (the battery − strap): printed as heavy as 1 RD 16.0 (book photo P3), so drawn at
    the 16 mm² width, no label, not in wires.csv. Its segments go into SEGS so the joint dots on it grow like a wire's."""
    d = path(pts); cw = WIDTH[16.0]
    SEGS.extend((p, q, cw + edge(cw), True) for p, q in zip(pts, pts[1:]))
    A(f'<path d="{d}" fill="none" stroke="#222" stroke-width="{cw + edge(cw):g}" stroke-linejoin="round"/>'
      f'<path d="{d}" fill="none" stroke="{COL["SV"]}" stroke-width="{cw:g}" stroke-linejoin="round"/>')

def note(x, y, lines, size=2.2, fill='#555', pitch=None):
    pitch = pitch or round(size * 1.36, 2)
    for i, s in enumerate(lines): txt(x, round(y + i * pitch, 2), s, size, fill=fill)

DOTS = []                                  # terminal and joint dots, drawn after every wire so heavy ones don't hide them
BLOCKS = []                                # connector blocks, drawn after the wires (their face dots after them)

BX = 150                                   # x of the fuse supply bars

# ---- fuse box 22: four supply bars, twelve fuses, outputs indexed ----------------------------------------------------
# Book photo P1 (and p.327): bars 1-2, 3-4, 5-8, 9-11; fuse 12 is connected to nothing on either side; all 8 A.
OUTS = {1: ['44b'], 2: ['44a'], 3: ['58', '54'], 4: ['57', '53'], 5: ['28'], 6: ['36'], 7: ['64'], 8: ['21', '185'],
        9: ['14', '89', '148'], 10: ['20'], 11: ['93', '95e', '67'], 12: []}
r = 0; first_row = {}
for n in range(1, 13):
    first_row[n] = r; r += len(OUTS[n])
def rowy(r):                               # 9 mm pitch, a gap row above bars 3-4, 5-8 and 9-11; fuse 12 follows 11
    return 76 + 9 * r + 9 * sum(r >= first_row[k] for k in (3, 5, 9))
DEST = {'44b': 'right headlamp, dipped beam', '44a': 'left headlamp, dipped beam',
        '58': 'front parking light 13, right', '54': 'tail light 14, right, via 58 tail lights;',
        '57': 'front parking light 13, left', '53': 'tail light 14, left, via 58 tail lights',
        '28': 'stop light contact 29', '36': 'radiator fan relay 38:30/51',
        '64': 'interior lights, via 58 interior feed;', '21': 'flasher unit 23:X', '185': 'fuel pump relay 102:30/51',
        '14': 'wiper switch 61:54, via 58 wiper switch;', '89': 'washer motor 63', '148': 'radiator fan relay 38:86, coil',
        '20': 'heater fan switch 35:4', '93': 'seat heating element 64, via 58 seat heating',
        '95e': 'inhibitor switch 90:2, reversing lights'}
DEST2 = {'54': '59 GN on to the panel lighting (instruments sheet)',          # branches that leave the fuse's cable
         '64': '80 BL on to cigarette lighter 48 (instruments sheet)',        # on the way to its first destination
         '14': '32 RD/VT on to combination instrument 47:2 (instruments sheet)'}
SHEET = {'44b': 'lighting', '44a': 'lighting', '58': 'lighting', '54': 'lighting', '57': 'lighting', '53': 'lighting',
         '28': 'signals', '36': 'climate', '64': 'interior', '21': 'signals', '185': 'injection', '14': 'wipers',
         '89': 'wipers', '148': 'climate', '20': 'climate', '93': 'interior', '95e': 'ignition'}
TAGW = {'54': 60.4, '64': 61.3, '14': 77.2}   # two-line boxes: the longer line's Helvetica width + 3
BARS = [(1, 2, 'Bar 1–2 · dipped beams, fed from lighting relay 8:56a'),
        (3, 4, 'Bar 3–4 · parking and tail lights, fed from light switch 10:5'),
        (5, 8, 'Bar 5–8 · always live, fed from the alternator B+ (battery)'),
        (9, 11, 'Bar 9–11 · live with ignition on, fed from relay 21')]
Y4, Y142, Y76, Y91, Y74E = 144, 152.5, 161.5, 180, 190   # where 4, 142, 76, 91 and 74e land on bar 5-8 (4 mm or more
Y44, Y50, Y92 = 81, 107.5, 206                           # off the fuse feeds, so none reads as running on into a fuse)
txt(147, 62, '22', 4, w='bold'); txt(154, 62, 'Fuse box', 2.7)
BAR_PATHS = []                             # drawn after the wires that land on them, so a heavy wire's end doesn't bite a bar
for a, b, title in BARS:
    y0, y1 = rowy(first_row[a]) - 4, rowy(first_row[b] + len(OUTS[b]) - 1) + 4
    if a == 5: y0, y1 = Y4 - 2, Y74E + 2.5         # up to take 4 GR, down past 74e GR from the alternator
    BAR_PATHS.append(f'<path d="M{BX},{y0} V{y1}" stroke="#111" stroke-width="1.6"/>')
    txt(156, rowy(first_row[a]) - 6.5, title, 2.6, w='bold')
for n, outs in OUTS.items():
    y = rowy(first_row[n])
    if n == 12:                            # the spare: on no bar, nothing on either pin
        fa, fb = fuse(156, y - 2, 14, 4)
        A(f'<path d="M153.8,{y} H156 M170,{y} H172.2" stroke="#111" stroke-width=".6"/>')
        contact(153, y); contact(173, y)
        txt(163, y - 3.2, fuse_label(n), 2.4, 'middle')
        txt(176, y + .9, 'spare: connected to nothing (check F2)', 2.4, fill='#444')
        txt(156, y + 7.3, 'Headlamp wipers (their own 3 A fuse, fed from bar 9–11): not fitted on this car.', 2.4, fill='#444')
        continue
    ys = [rowy(first_row[n] + i) for i in range(len(outs))]
    A(f'<path d="M{BX},{y} H156 M170,{y} H176" stroke="#111" stroke-width=".6"/>')
    fuse(156, y - 2, 14, 4)
    txt(163, y - 3.2, fuse_label(n), 2.4, 'middle')
    if fuse_checked(n): tick(170.4, y - 2.6, s=0.9)
    if len(ys) > 1: A(f'<path d="M176,{ys[0]} V{ys[-1]}" stroke="#111" stroke-width=".6"/>')
    for cab, yy in zip(outs, ys):
        DOTS.append((176, yy))
        if cab == '67':                    # fuse 11 to the horn: the one output drawn whole on this sheet
            HORN_Y = yy; wire(cab, [(176, yy), (322, yy)], 180, yy - 1.5); continue
        wire(cab, [(176, yy), (230, yy)], 180, yy - 1.5)
        st = WIRES[cab]['status']
        tx = 232 if st == 'stub' else 230
        txt(tx - 2, yy - 1.2 - core_width(cab) / 2, f'({SHEET[cab]} sheet)', 2.2, 'end', fill='#666')
        if cab in DEST2:
            mtag(tx, yy, '→ ' + DEST[cab], DEST2[cab], TAGW[cab], dashed=(st == 'open'))
        else:
            tag(tx, yy, '→ ' + DEST[cab], dashed=(st == 'open'))

# ---- ignition switch 20 and its connector 58 -------------------------------------------------------------------------
# As p.327 prints it: a round lock with the key slot, terminal circles on the rim (15 top, 50 and 54 left, 30 bottom,
# X right), no contacts. Here the lock sits in a box with the terminals in our order along its bottom edge, so every
# lead leaves without a crossing: the rightmost turns right first. Connector 58 by the switch (58 (A7)): pin 1 118|118e,
# pin 2 84|84e, pin 3 5|5e, pin 4 4e|4; pins 5-8 unused. 54bf (automatic detail S 3981) leaves 15 directly.
SW_Y = 48                                  # the box's bottom edge, where the terminals sit
box(18, 28, 44, 20); name(18, 25.4, '20', 'Ignition switch')
LX, LY = 30, 36.5                          # the lock: a circle with the key slot, as printed
A(f'<circle cx="{LX}" cy="{LY}" r="6" fill="#fff" stroke="#111" stroke-width=".6"/>'
  f'<path d="M{LX},{LY - 3.6} L{LX + 1.3},{LY - 1.4} L{LX + 1.3},{LY + 1.4} L{LX},{LY + 3.6} L{LX - 1.3},{LY + 1.4} '
  f'L{LX - 1.3},{LY - 1.4} Z" fill="none" stroke="#111" stroke-width=".5"/>')
IG = {'54': 22, '30': 30, 'X': 40, '50': 50, '15': 58}
for k, x in IG.items(): txt(x, SW_Y - 2.2, k, 2.4, 'middle'); DOTS.append((x, SW_Y))   # clear of the 1.5 mm² dots
txt(39.5, 37.9, 'contacts not drawn', 2.0, fill='#777')
note(66, 33, ('30 battery; 50 start;', '15, 54 and X probably live with the key on.'))
# 15: 118 to pin 1 on a level run, 54bf straight down to its tag
P1X = 90
wire('118', [(58, SW_Y), (62, 52), (P1X - 2.5, 52)], 63.2, 50.5)
wire('118e', [(P1X + 2.5, 52), (98, 52)], label=False)
tag(98, 52, '118e GN/VT 1.0 → joint by the coil, rev counter (ignition sheet)', w=75.2)
BLOCKS.append(lambda: pin_h(P1X, 52, n='1')); DOTS += [(P1X - 2.5, 52), (P1X + 2.5, 52)]
txt(P1X, 47.6, '58 ign. switch', 2.2, 'middle', w='bold')
wire('54bf', [(58, SW_Y), (58, 60), (66, 60)], label=False)
tag(66, 60, '54bf GN 0.75 → gear indicator light 91 (ignition sheet)', w=65.2)
# 50: 84 down to pin 2, 84e right to its tag
P2Y = 65                                   # faces at 62.5 and 67.5: 84e's band (top 68.9) stays clear of the block
wire('84', [(50, SW_Y), (50, P2Y - 2.5)], 48.4, P2Y - 3.5, rot=-90)
wire('84e', [(50, P2Y + 2.5), (50, 70), (80, 70)], label=False)
mtag(80, 70, '84e GL 1.5 → start inhibitor relay 89:30/51,', 'via 57 starter line (ignition sheet)', 52.6)
BLOCKS.append(lambda: pin_v(50, P2Y, n='2')); DOTS += [(50, P2Y - 2.5), (50, P2Y + 2.5)]
txt(53.6, P2Y + 1, '58 ign. switch', 2.2, w='bold')
# X: 75 RD (no pin) down to the gap row and right to its tag
wire('75', [(40, SW_Y), (40, 94), (66, 94)], 38.4, 90, rot=-90)
tag(66, 94, '75 RD 1.0 → light switch 10:8 (lighting sheet)', w=55)
# 30 and 54: 4e and 5 down to pins 4 and 3; 4 on into the top of bar 5-8, 5e on to relay 21:86
P34 = 120
wire('4e', [(30, SW_Y), (30, P34 - 2.5)], 28.4, 90, rot=-90)
wire('4', [(30, P34 + 2.5), (30, Y4), (BX, Y4)], 60, Y4 - 1.5)
wire('5', [(22, SW_Y), (22, P34 - 2.5)], 20.4, 100, rot=-90)
wire('5e', [(22, P34 + 2.5), (22, Y91), (80, Y91)], 26, Y91 - 1.5)
BLOCKS.append(lambda: pin_v(30, P34, n='4')); BLOCKS.append(lambda: pin_v(22, P34, n='3'))
DOTS += [(30, P34 - 2.5), (30, P34 + 2.5), (22, P34 - 2.5), (22, P34 + 2.5)]
txt(33.8, P34 + 1, '58 ign. switch', 2.2, w='bold')

# ---- feeds of bars 1-2 and 3-4 from the lighting sheet; bar 5-8 to the lighting relay and light switch -------------
wire('44', [(107.5, Y44), (BX, Y44)], 112, Y44 - 1.5)
mtag(66, Y44, '44 GR 1.5 ← lighting relay 8:56a,', 'dipped beams (lighting sheet)', 41.5)
wire('50', [(111.3, Y50), (BX, Y50)], 115, Y50 - 1.5)
mtag(66, Y50, '50 GN 1.0 ← light switch 10:5,', 'parking and tail lights (lighting sheet)', 45.3)
wire('142', [(BX, Y142), (132, Y142)], 133.5, Y142 - 1.5)
tag(132, Y142, '142 GR 1.5 → lighting relay 8:30 (lighting sheet)', w=58.5, anchor='end')
wire('76', [(BX, Y76), (132, Y76)], 133.5, Y76 - 1.5)
tag(132, Y76, '76 GR 1.0 → light switch 10:4 (lighting sheet)', w=55.2, anchor='end')

# ---- ignition switch relay 21 ----------------------------------------------------------------------------------------
# Book photos P9a/P9b print 30/51 top left (blade on an inner pivot, rising, open), 87 right (fixed contact on a short
# inner link), 86 right-lower and 85 bottom-left (the coil between them, a zigzag), the coil-to-blade link a solid
# line. Rearranged here (positions are ours): coil on the left wall (86 above 85), contact on the right wall (30/51
# above 87), so 5e reaches 86 straight, 91 goes right into bar 5-8 and 92 into bar 9-11. The link is drawn with mlink()
# as every relay on these sheets, although the print draws it solid.
RX0, RX1, RT, RB = 80, 114, 176, 210
Y85 = 196
box(RX0, RT, RX1 - RX0, RB - RT); name(RX0, RT - 3, '21', 'Ignition switch relay')
cl, cr, ct, cb = coil(84, 182, 8, 12)
inner([(RX0, Y91), (ct[0], Y91), ct]); inner([cb, (cb[0], Y85), (RX0, Y85)])
contact(106, 186); inner([(RX1, Y91), (106, Y91), (106, 185.2)])        # 30/51: the blade's pivot
contact(106, 199.5); inner([(RX1, Y92), (106, Y92), (106, 200.3)])      # 87: fixed contact
blade(106.4, 186.7, 109.6, 196.4)                                         # make contact 30/51-87, open at rest
mlink([cr, (106.83, cr[1])])
for (x, y, k, a) in ((RX0, Y91, '86', 'start'), (RX0, Y85, '85', 'start'), (RX1, Y91, '30/51', 'end'), (RX1, Y92, '87', 'end')):
    tlabel(x + (1.6 if a == 'start' else -2.8), y - 1.3, k, a); DOTS.append((x, y))     # right: clear of the 4.0 mm² dots
wire('90', [(RX0, Y85), (59, Y85)], 61, Y85 - 1.5)
mtag(59, Y85, '90 SV 0.75 → lighting relay 8:31,', 'then earth (lighting sheet)', 41, anchor='end')
wire('91', [(RX1, Y91), (BX, Y91)], 116, Y91 - 1.5)
wire('92', [(RX1, Y92), (BX, Y92)], 116, Y92 - 1.5)

# ---- starter 4 (terminal 30), battery 1, regulator 3 and alternator 2 -----------------------------------------------
# P3 / p.327: the starter with its pinion on the left, 16 and 50 on the right edge, 30 at the bottom; the battery box
# printed '12V 60Ah' with - and + on its bottom edge; regulator 3 left of alternator 2, D-, DF, D+ facing each other;
# alternator B+ top right, pulley on the right. No internals printed for any of the four, so none are drawn.
# 1, 74 and 234 leave starter 30 as a fan (1 down-left, 74 straight down, 234 down-right), so none crosses another.
def shaft(x, y, pulley=False, right=False):
    """Pinion (starter) or pulley (alternator) on a wall at (x, y): a black block on a short neck (Turbo power sheet);
    right=True puts it on a right wall."""
    s = 1 if right else -1
    h = 10 if pulley else 6
    nx = x if right else x - 1.6
    bx = x + 1.4 if right else x - 4.6
    A(f'<rect x="{nx}" y="{y - 1.1}" width="1.6" height="2.2" fill="#111"/><rect x="{nx + .4}" y="{y - .5}" width=".8" height="1" fill="#fff"/>')
    A(f'<rect x="{bx}" y="{y - h / 2}" width="3.2" height="{h}" rx=".8" fill="#111"/>')
    if pulley: A(f'<rect x="{bx + 1.35}" y="{y - h / 2 + 1.4}" width=".5" height="{h - 2.8}" fill="#fff"/>')

ST = (16, 204, 36, 14)                     # starter box x, y, w, h
box(*ST); name(20, 211, '4', 'Starter'); shaft(16, 211)
txt(19.5, 215.8, '16, 50: ignition sheet', 2.2, fill='#555')
S30 = (44, 218)                            # starter 30, on its bottom edge
tlabel(47, 216.4, '30')
Y74 = 231                                  # 74 GR's run, above the battery and the regulator
BP = (136, 239)                            # alternator B+, on its top edge near the right
wire('234', [S30, (50, 224), (56, 224)], label=False)
tag(56, 224, '234 RD 2.5 → master relay 101:30/51 (injection sheet)', w=65.9)
wire('74', [S30, (S30[0], Y74), (BP[0] - 8, Y74), BP], 54, 237)
wire('74e', [BP, (BP[0], Y74E), (BX, Y74E)], 134.4, 229, rot=-90)          # crosses 92 VT plainly at (136, 206)
wire('1', [S30, (36, 226), (36, 234)], 18, 230.5)
DOTS += [S30, BP]
BT = (12, 234, 27, 16)                     # battery box
box(*BT); name(15.5, 241.8, '1', 'Battery'); txt(15.5, 245.4, '12 V 60 Ah', 2.2, fill='#555')
txt(33.6, 239.2, '+', 3.2, 'middle'); txt(22.6, 248.8, '−', 3.2, 'middle')
BPLUS, BMINUS = (36, 234), (17, 250)
DOTS += [BPLUS, BMINUS]
# the battery - strap: unnumbered (no row in wires.csv); 46, 45 and 38 SV join it on the print, here from the left tags'
# side as a short bus, then the earth symbol
EY = (257, 268, 279)                       # where 46, 45, 38 join the strap
for cab, y, l1, l2 in (('46', EY[0], '46 SV 1.0 ← right headlamp earth', '(lighting sheet)'),
                       ('45', EY[1], '45 SV 1.0 ← left headlamp earth', '(lighting sheet)'),
                       ('38', EY[2], '38 SV 1.5 ← radiator fan 37,', 'via 59 radiator fan (climate sheet)')):
    wire(cab, [(25, y), (17, y)], label=False); mtag(25, y, l1, l2, 42.3); DOTS.append((17, y))
strap([BMINUS, (17, EY[-1] + 2)]); earth(17, EY[-1] + 2)           # over the ends of 46, 45 and 38
txt(12.4, 274, 'battery − strap', 2.0, 'middle', fill='#666', rot=-90)
# regulator 3 and alternator 2
RG = (78, 241, 12, 20); AL = (108, 239, 32, 24)
YD = (245, 251, 257)                       # D-, DF, D+
box(*RG); name(RG[0], RG[1] + RG[3] + 4.5, '3', 'Voltage regulator', 2.4, 3.4)   # under the box: 74's label is above it
box(*AL); name(116, 250, '2', 'Alternator'); shaft(AL[0] + AL[2], 255, pulley=True, right=True)
for y, k in zip(YD, ('D−', 'DF', 'D+')):
    tlabel(RG[0] + RG[2] - 1.6, y + .65, k, 'end'); tlabel(AL[0] + 1.6, y + .65, k)
    DOTS += [(RG[0] + RG[2], y), (AL[0], y)]
tlabel(BP[0], BP[1] + 4.4, 'B+', 'middle')                   # under the 6.0 mm² dot
for cab, y in zip(('49', '73', '72'), YD): wire(cab, [(RG[0] + RG[2], y), (AL[0], y)], 92, y - 1.4)
DP = (AL[0], YD[2])
wire('61', [DP, (105, YD[2] + 3), (105, 280), (110, 280)], label=False)
mtag(110, 280, '61 RD 0.75 ← charge warning lamp,', 'combination instrument 47:1 (instruments sheet)', 58.7)
note(172, 278.6, ('On this car a relay has been cut into 61 RD (not drawn);', 'what it switches is still to be checked.'))

# ---- horn 40 on fuse 11, horn contact 41 -----------------------------------------------------------------------------
# p.327: a small driver block with a trumpet flaring away from the leads; 67 RD into its middle, 70 SV from its lower
# corner on a short diagonal; mirrored here so the leads come from the left. 70 SV runs through the one-pin 58 to horn
# contact 41 in the steering wheel pad (a push contact in a circle, open at rest; p.327: P9a shows only the left edge of
# its circle), whose other side is earthed.
HX = 322
def horn(x, y):
    """Driver block (x, y-centre) and trumpet flaring to the right, as printed (mirrored)."""
    A(f'<path d="M{x + 4},{y - 3} L{x + 18},{y - 8} L{x + 18},{y + 8} L{x + 4},{y + 3} Z" fill="#fff" stroke="#111" '
      f'stroke-width=".8" stroke-linejoin="round"/>')
    A(f'<rect x="{x}" y="{y - 4.5}" width="4" height="9" rx="1" fill="#fff" stroke="#111" stroke-width=".9"/>')
Y70 = 274
wire('70', [(HX, HORN_Y + 4), (HX - 3, HORN_Y + 7), (HX - 3, Y70), (350, Y70)], 324, Y70 - 1.5)
horn(HX, HORN_Y + 1)
DOTS += [(HX, HORN_Y), (HX, HORN_Y + 4)]
name(343, HORN_Y - 3, '40', 'Horn', 2.6, 3.4)
note(343, HORN_Y + 1.6, ('Single horn, switched to earth by the', 'horn contact in the steering wheel.'))
P58 = 352
BLOCKS.append(lambda: pin_h(P58, Y70)); DOTS += [(P58 - 2, Y70), (P58 + 2, Y70)]
txt(P58, Y70 - 4.7, '58 horn', 2.2, 'middle', w='bold')
C41 = (383, Y70)
wire('71', [(P58 + 2, Y70), (C41[0] - 5, Y70)], 356.5, Y70 - 1.5)
A(f'<circle cx="{C41[0]}" cy="{C41[1]}" r="5" fill="#fff" stroke="#111" stroke-width=".6"/>')
contact(C41[0] - 2.4, Y70); contact(C41[0] + 2.4, Y70)
inner([(C41[0] - 5, Y70), (C41[0] - 3.2, Y70)]); inner([(C41[0] + 3.2, Y70), (C41[0] + 5, Y70)])
blade(C41[0] - 1.8, Y70 - .5, C41[0] + 2, Y70 - 2.3)                     # horn push: open at rest
A(f'<path d="M{C41[0] + .2},{Y70 - 1.6} V{Y70 - 3.6} M{C41[0] - 1.2},{Y70 - 3.6} H{C41[0] + 1.6}" stroke="#111" '
  f'stroke-width=".45" fill="none"/>')                                    # the push button
DOTS += [(C41[0] - 5, Y70), (C41[0] + 5, Y70)]
A(f'<path d="M{C41[0] + 5},{Y70} H{C41[0] + 10}" stroke="#111" stroke-width=".6" fill="none"/>'); earth(C41[0] + 10, Y70)
name(C41[0] - 6, Y70 + 10.5, '41', 'Horn contact', 2.4, 3.4)

# ---- dots, connector blocks and bars over the wires ------------------------------------------------------------------
for b in BLOCKS: b()
for x, y in DOTS: dot(x, y)
for bp in BAR_PATHS: A(bp)

# ---- notes -----------------------------------------------------------------------------------------------------------
note(320, 72, ('Headlamp main beams are not fused: they come',
               'straight from lighting relay 8:F (lighting sheet).'), 2.4, '#333')
note(320, 84, ("Relay 21's coil earths through lighting relay 8:31",
               '(lighting sheet).'), 2.4, '#333')

# ---- legend ----------------------------------------------------------------------------------------------------------
lx, ly = 250, 28
box(lx, ly, 157, 20.5 + (6 if PROBABLE[0] else 0), fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 97
A(f'<path d="M{x},{ly + 5} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, ly + 6, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x},{ly + 10} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 11, ly + 11, 'not traced yet', 2.4)
if STUB[0]:
    A(f'<path d="M{x},{ly + 15} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{ly + 15}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    txt(x + 11, ly + 16, 'ends on diagram', 2.4)
if TICKED[0]:
    tx, gx = (x + 33, x + 37) if STUB[0] else (x + 3, x + 11)
    tick(tx, ly + 15.3); txt(gx, ly + 16, 'checked on the car', 2.4)
size_legend(lx + 4, ly + 16)
probable_legend(lx + 4, ly + 21)
save('power.svg')

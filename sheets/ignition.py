#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo ignition, starting and fuel injection sheet (A3 SVG)."""
import math
from common import *

header('Saab 99 Turbo, model 1979 — Ignition, starting and fuel injection')
def ht(pts): A(f'<path d="{path(pts)}" fill="none" stroke="#444" stroke-width="1.1" stroke-linejoin="round"/>')
def name(x, y, n, s, anchor='start'): txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', 2.7, anchor)
def mtag(x, y, lines, w, size=2.2, anchor='start'):
    """Destination tag of several lines (common.tag() takes one), as the instruments sheet draws them: centred on y,
    lines 1.36 × size apart. w: the longest line's Helvetica width plus about 4."""
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2); x0 = x if anchor == 'start' else x - w
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines): txt(x0 + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
# Joint on a 2.5 mm² wire: r 1.8, so it still shows past the 2.9 mm stroke and reads as a joint, not a rivet in the band

# ---- ignition switch and starter ----------------------------------------
box(18, 38, 40, 32); name(21, 44, '20', 'Ignition switch')
for t, y in (('30', 44), ('15', 54), ('50', 64)): dot(58, y); txt(56, y + 1, t, 2.4, 'end')
wire('7', [(58, 44), (66, 44)], label=False); tag(68, 44, '← 7 GR 2.5 from bar 7–12')
wire('123', [(58, 54), (146, 54)], 70, 52.5); dot(58, 54)           # 15 on top of its 1.5 mm² lead
# 123 reaches engine connector 58 pin 4 through door switch connector 58 (58 (A9)) row 6, the bottom row (scan p.407:
# up x 5654 from 20:15 into row 6, labelled on its left; book photos IMG_4700, P8). Drawn like pin 4: bold name above, row below.
XA9 = 118
A(f'<rect x="{XA9}" y="48" width="4" height="12" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(XA9, 54); dot(XA9 + 4, 54)
txt(XA9 + 2, 46, '58 door switches', 2.4, 'middle', w='bold'); txt(XA9 + 2, 64, 'row 6', 2.1, 'middle', fill='#555')
wire('122', [(58, 64), (80, 64), (80, 86), (96, 86), (96, 90)], 60, 62.3)
dot(58, 44); dot(58, 64)                                             # 30 and 50 on top of their 2.5 mm² leads
# 122 passes ignition switch connector 58 (58 (B9)) row 1, labelled '122 GL 2.5' on both sides (scan p.407; book photos
# P8, IMG_4706): a pin on its drop, captioned on the right, where the space under the switch is free
A('<rect x="76" y="72" width="8" height="6" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(80, 72); dot(80, 78)   # 6 tall: the dots grow on 2.5 mm²
txt(86, 74.6, '58 ign. switch', 2.1, fill='#555'); txt(86, 77.4, 'row 1', 2.1, fill='#555')

# starter 4, drawn upside down (manual: 16 upper right, 50 lower right, 30 bottom centre); nothing printed inside
box(18, 134, 34, 30); name(22, 150, '4', 'Starter')
A('<rect x="16" y="147" width="2.4" height="4" fill="#fff" stroke="#111" stroke-width=".5"/>'
  '<rect x="12.6" y="145" width="3.4" height="8" rx=".6" fill="#111"/>')   # pinion (mechanical, as printed)
dot(35, 134); txt(33.6, 137.4, '30', 2.1, 'end', fill='#555')
for t, y in (('50', 141.5), ('16', 156.5)): dot(52, y); txt(50, y + .8, t, 2.1, 'end', fill='#555')
# 1 RD 16.0 draws 4 mm wide: a longer stub, so it reads as a lead turning to its tag rather than a lump on the wall
wire('1', [(35, 134), (35, 127), (45, 127)], label=False); tag(47, 127, '1 RD 16.0 ← battery +', size=2.4); dot(35, 134)

# relay 89, drawn upside down (manual: 85, 87, 87a on the top edge; 86, 30 on the bottom), contacts at rest as printed
box(88, 90, 32, 32)
txt(123.5, 103.5, '89', 3.2, w='bold'); txt(123.5, 108, 'Start relay', 2.5)   # the manual's legend: 'start inhibitor relay'
for t, x, y, lx, ly, a in (('86', 96, 90, 97.3, 93.3, 'start'), ('30', 112, 90, 110.7, 93.3, 'end'),
                           ('85', 96, 122, 97.3, 120.2, 'start'), ('87', 104, 122, 105.6, 120.2, 'start'),
                           ('87a', 112, 122, 113.3, 120.2, 'start')):
    dot(x, y); tlabel(lx, ly, t, a)
cl, cr, ct, cb = coil(90.5, 103.5, 13.5, 5.5)                       # coil 86-85
inner([(96, 90), (96, 103.5)]); inner([(96, 109), (96, 122)])
contact(107.2, 100.6); contact(112, 100.6)                          # blade pivots, joined, fed from 30
inner([(112, 90), (112, 99.8)]); inner([(108, 100.6), (111.2, 100.6)])
contact(106.6, 112.2); contact(112, 112.4)                          # fixed contacts 87 and 87a
inner([(106.39, 112.97), (104, 122)]); inner([(112, 113.2), (112, 122)])
blade(107.4, 101.3, 108.5, 110.5); blade(112.2, 101.3, 113.7, 110.5)   # both open at rest; each tip just past its own contact
mlink([cr, (113.4, cr[1])])
# 201 SV: relay 89's coil earth, to earth joint 158 (power sheet); round to the empty space left of the relay
wire('201', [(96, 122), (96, 125.5), (84, 125.5), (84, 118), (80, 118)], label=False); tag(78, 118, '201 SV 0.75 → earth joint 158 (power sheet)', w=55, anchor='end')
wire('202', [(112, 90), (112, 84), (118, 84)], label=False); tag(120, 84, '202 GR 1.5 ← bar 7–12 (always live)'); dot(112, 90)   # 30 on top
wire('122a', [(104, 122), (104, 141.5), (52, 141.5)], 72, 139.8); dot(104, 122); dot(52, 141.5)   # 87 and 50 on top of it
# 271: 89:87 to 92's heater through 58/1. Under 394, up into the band below 124, right over the pump and down the strip
# between the injection parts and 284's riser (284 wraps 102 and the injection parts, so its bottom run crosses this drop
# once); 58/1 on the drop, then round into 92's left wall. X271 leaves room left of it for the pump's earth column.
Y271, X271 = 124.2, 384
wire('271', [(104, 131), (180, 131), (180, Y271), (X271, Y271), (X271, 214), (356, 214), (356, 230), (362, 230)], X271 - 1.4, 211, rot=-90)
dot(104, 131)                                                      # 271 tees off 122a: on top of both (282 tees off it by the starter)
Y58 = 188                                                          # 58/1's top: 6 below 284's crossing, so 284 doesn't read as landing on it
A(f'<rect x="{X271 - 4}" y="{Y58}" width="8" height="4" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(X271, Y58); dot(X271, Y58 + 4)
txt(X271 - 6, Y58 + 3, '58 engine, pin 1', 2.1, 'end', fill='#555')   # left of the pin: right of it, the grey lines would run into the border
# the RD label sits on the 92 side, where the book prints it; the relay side of 58 (A4) pin 1 is GN 1.0 (data/connectors.csv),
# but wires.csv has one row for 271, so the whole run is drawn RD until that is split
txt(X271 - 6, Y58 + 6.2, 'relay side probably', 1.8, 'end', fill='#777'); txt(X271 - 6, Y58 + 8.8, 'GN 1.0 (check E1)', 1.8, 'end', fill='#777')   # two lines: clear of 96
# 272's riser runs right of service outlet 73 (lower left): 282 crosses its top run, 283 and 284a its riser, once each
XR = 80
wire('272', [(52, 156.5), (XR, 156.5), (XR, 240), (300, 240)], XR + 5, 238.5)
A('<rect x="199" y="236" width="4" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(199, 240); dot(203, 240); txt(201, 234.3, '58 engine, pin 3', 2.1, 'middle', fill='#555')

# ---- ballast resistor, coil, distributor, plugs, control unit ----------
A('<rect x="146" y="48" width="4" height="12" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(146, 54); dot(150, 54)
txt(148, 46, '58 engine', 2.4, 'middle', w='bold'); txt(148, 64, 'pin 4', 2.1, 'middle', fill='#555')   # 58 (A4) pin 4
wire('123', [(150, 54), (170, 54)], label=False); dot(150, 54)      # the pin on top of its 1.5 mm² lead, like the left one
# ballast resistor 147 (scan; car photo 25 Sep: a Bosch block stamped 0.4 and 0.6, their ends strapped at the joint): two resistors
# joined at the bottom by a link; 394 leaves at that joint. The feed side (123) is the 0.4 Ω one, the coil side (123b) the 0.6 Ω.
box(170, 49, 16, 16); txt(167.4, 45, '<tspan font-weight="bold">147</tspan> Ballast resistor', 2.5)   # start-anchored: cairosvg splits a middle-anchored tspan
for x in (174, 182):
    dot(x, 65); a, b = resistor(x - 1.2, 55.5, 2.4, 4.8); inner([b, (x, 65)])
inner([(170, 54), (174, 54), (174, 55.5)]); inner([(186, 54), (182, 54), (182, 55.5)]); inner([(174, 62.6), (182, 62.6)])
tlabel(174, 52.6, '0.4 Ω', 'middle'); tlabel(182, 52.6, '0.6 Ω', 'middle')
wire('123b', [(186, 54), (214, 54)], 188, 52.3); dot(170, 54); dot(186, 54)   # all four printed terminals
wire('394', [(174, 65), (174, 126), (112, 126), (112, 122)], 172.6, 116, rot=-90)
box(214, 46, 18, 30); txt(223, 43.5, '5 Coil', 2.7, 'middle', w='bold')
# 5's terminals: scan p.407 (about x 3290-3340, y 1090) and book photo source/photos/book-1980-146-coil-124.jpg print
# 15 on the upright coil's left shoulder and 1 on its right one; 124 crosses 123d and 284 on its way there too.
# 1 on the bottom wall near the right corner, where the book's right shoulder lands when the coil is turned tower-right;
# 15 stays on the left wall to meet 123b. 124 comes in from below (1's dot is drawn after it, on top)
dot(214, 54); txt(216, 54.8, '15', 2.1, fill='#555'); txt(228, 73.6, '1', 2.1, 'middle', fill='#555')
A('<circle cx="262" cy="61" r="9" fill="#fff" stroke="#111" stroke-width=".8"/><circle cx="262" cy="61" r="1" fill="#111"/>')
txt(262, 48, '6 Distributor', 2.7, 'middle', w='bold')
ht([(232, 61), (253, 61)])
for i, x in enumerate((248, 258, 268, 278)):
    ht([(262 + (i - 1.5) * 3, 70), (x, 86)])
    A(f'<path d="M{x - 1.8},{86} h3.6 l-0.8,7 h-2 z" fill="#fff" stroke="#111" stroke-width=".5"/><path d="M{x},{93} v2" stroke="#111" stroke-width=".5"/>')
    txt(x, 99, str(i + 1), 2.2, 'middle')
txt(263, 104, '157 Spark plugs', 2.6, 'middle', w='bold')
A('<rect x="277" y="49" width="16" height="18" rx="2" fill="none" stroke="#888" stroke-width=".3"/>')
wire('390', [(271, 57), (284, 57), (284, 52), (308, 52)], label=False); txt(277, 47.8, 'screened', 2.2, fill='#555')
wire('391', [(271, 64), (288, 64), (288, 59), (308, 59)], label=False)
txt(295, 50.9, '390', 2.1); txt(295, 57.9, '391', 2.1)            # number only, as printed at 146 (no colour or size)
# 392 SV earths the screen at the main earth star (scan p.407: from the screen at 146 round to the star, labelled at both
# ends). Its earth drops below the screen, clear of plug 4, so its label fits along the lead (123d is just right of it)
wire('392', [(285, 67), (285, 84)], label=False); earth(285, 84); txt(283.6, 82.2, '392 SV 0.75', 2.1, rot=-90)
# control unit 146: all six terminals on the left edge in the manual's order; nothing printed inside
box(308, 40, 34, 44); txt(345, 58, '146', 3.2, w='bold'); txt(345, 62.5, 'Ignition control unit', 2.5)
for t, y in (('31', 45), ('31d', 52), ('7', 59), ('15', 66), ('16', 73), ('16', 80)):
    dot(308, y); txt(310, y + .8, t, 2.1, fill='#555')
wire('393', [(308, 45), (304.5, 45), (304.5, 35), (350, 35), (350, 39)], 318, 33.5); earth(350, 39); dot(308, 45)   # 31 on top
# 123d: +15 for 146 from 58 (A4) pin 4 on the 147 side, before the ballast resistor (book photo IMG_4729: it passes
# under the coil without joining it); branched just right of the pin, it crosses 394 without a joint
wire('123d', [(156, 54), (156, 73), (206, 73), (206, 112), (296, 112), (296, 66), (308, 66)], 234, 110.5); dot(156, 54)
# 124: lower 16 to coil 1. It has to cross 284 (which wraps the lower 16) and 123d (coil 1 sits inside 123d's loop);
# it drops beside 146 and runs back under 123d's bottom run, clear of the HT leads
wire('124', [(308, 80), (304.5, 80), (304.5, 119.5), (228, 119.5), (228, 76)], 258, 117.8); dot(228, 76); dot(308, 80)   # both ends on top of the lead
# 284 comes down the far right, past 271, and crosses it once on its way back (it used to cross 271's top run instead):
# that leaves the column between 95 and 271 free for the pump's earth through tank earth connector 60
wire('284', [(308, 73), (300.5, 73), (300.5, 92), (400, 92), (400, 182), (233.5, 182), (227.5, 176)], 246, 180.3)   # into 102's bottom pair

# ---- fuel pump relay, overboost switch, pump and injection parts -------
# fuel pump relay 102 as the book prints it: 1979 foldout (book photo P6b, with Charlie's pencil FUEL) and 1980 (P6a) are
# identical, and the scan p.407 agrees. A square; 15 and 87 on the top wall, 31 and an unlabelled circle on the left,
# 30 and a pair of touching circles on the bottom. Everything inside is printed clearly in both photos: nothing grey.
box(216, 140, 36, 36); txt(254.5, 157, '102', 3.2, w='bold'); txt(254.5, 161.5, 'Fuel pump relay', 2.5)
T15, T87, T31, TLL, TP1, TP2, T30 = (224.5, 140), (242.5, 140), (216, 149.5), (216, 167.5), (224.5, 176), (227.5, 176), (242.5, 176)
for p in (T15, T87, T31, TLL, TP1, TP2, T30): dot(*p)
tlabel(227.2, 142.2, '15'); tlabel(241.2, 142.8, '87', 'end'); tlabel(217.3, 148.2, '31'); tlabel(241.2, 174.6, '30', 'end')
tlabel(225.6, 171.4, '31')                                           # printed once over the bottom pair (see notes); the left circle has no label
# electronics: a tall plain box, no caption in the book (ours, grey); its left edge runs on up to 31 and down to the spare circle
A('<rect x="222" y="150.5" width="5" height="15" fill="#fff" stroke="#111" stroke-width=".4"/>')
txt(225.15, 158, 'electronics', 1.8, 'middle', fill='#888', rot=-90)
inner([T31, (222, 149.5), (222, 167.5), TLL])
inner([T15, (224.5, 150.5)]); inner([T15, (231.5, 148.5), (231.5, 154.5)])   # both leave the 15 circle: into the box and onto the coil
cl, cr, ct, cb = coil(227, 154.5, 9, 6.5)                            # its left side is the box's right edge: the other end is in the box
A('<rect x="227" y="161" width="5" height="3" fill="#fff" stroke="#111" stroke-width=".4"/>')   # small plain block under the coil, no leads
inner([T87, (242.5, 150.4)]); contact(242.5, 151.2); contact(242.5, 164.5); inner([(242.5, 165.3), T30])
blade(242.7, 163.8, 245.5, 152.5)                                    # 30-87: open at rest
inner([cr, (237, cr[1])]); mlink([(237, cr[1]), (244, cr[1])])
inner([(224.5, 165.5), TP1]); inner([(224.5, 172.8), TP2])           # box to the pair; the two circles are drawn joined
wire('260', [T30, (242.5, 190), (247, 190)], label=False); tag(249, 190, '260 GR 1.5 ← fuse 10', size=2.4); dot(*T30)   # 30 on top
# 284a (TP1 to service outlet 73 pin 5) is drawn with 73, lower left
# pressure switch 144: contact drawn closed, as the manual prints it
box(160, 151, 20, 10); inner([(160, 156), (163.2, 156)]); inner([(176.8, 156), (180, 156)])
contact(164, 156); contact(176, 156); blade(164.7, 156, 175.2, 156)
txt(170, 165, '144 Pressure switch (overboost)', 2.4, 'middle', w='bold')
wire('378', [(180, 156), (185, 156), (185, 134), (224.5, 134), T15], 189, 132.3)
wire('377', [(160, 156), (150, 156)], label=False)
mtag(148, 156, ('377 GN/VT 0.75 ← 58 engine pin 4,', 'switch side (top of sheet)'), w=38.3, anchor='end')   # two lines: one would reach 272
# 377 stays a tag: it leaves pin 4 on the switch side as a lead of its own beside 123 and 283 (scan p.407: a diagonal
# from the x 2237 riser; data/connectors.csv), not the 147 side like 123d, and the only ways down from there cross the
# 202 tag or squeeze between 122, 201 and relay 89's wall
dot(160, 156); dot(180, 156)
# 102:31 takes two leads (book photos P6a/P6b, scan): 100 SV straight in from the left, relay 67's coil earth (via 100a) and
# contact 87; and 263 SV on a diagonal, to relay 21's coil earth (its end is in the border, aimed at 31)
wire('263', [T31, (212.5, 153), (212.5, 176.5), (208, 176.5)], label=False); tag(206, 176.5, '263 SV 0.75 → relay 21:85 (power sheet)', anchor='end')
wire('100', [T31, (209.5, 149.5), (209.5, 170), (208, 170)], label=False); tag(206, 170, '100 SV 0.75 ← relay 67:87 (wipers sheet)', anchor='end')
dot(*T31)                                                            # 31 on top of both leads (diagonal drawn first, as at 87)
# 87 takes two leads (P6a/P6b): one straight up, one on a diagonal. Scan p.407: the straight-up one turns left at y≈1545 and
# again at y≈1100 onto the '261a GR 0.75' label (x≈2885–3020); so the diagonal (up x≈3390, then right at y≈1270) is 261 GR 2.5.
# Here they cross once, without a joint (like 260 × 284). The diagonal is drawn first, so the straight lead covers its root;
# it rises at about 38°: its upper edge still parts from the straight one at the dot, and its lower edge leaves 102's top
# wall just past the dot (at 30° it ran along the wall for about 2 mm). 87's dot is 1.8 to cover its ends.
# 261 passes door switch connector 58 (58 (A9)) row 4 and fuel pump connector 57 (57 (C12), one upright pin) on its way
# to the pump (scan p.407: '261 GR 2.5' on both sides of row 4, above 58 (B11) without entering it, and on the drop into 57;
# book photos IMG_4700, IMG_4701). Row 4 sits left of 261a's riser, 57 on the last run into the pump; the cable's label
# goes under the run between 261a and the drop (above it, the 190 tag leaves no room).
XP = 322                                                            # the pump's centre
wire('261', [T87, (247, 136.5), (300, 136.5), (300, 146), (XP - 6, 146)], 276, 141.2)
A('<rect x="259" y="132.5" width="6" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(259, 136.5); dot(265, 136.5)   # 6 wide, as 60 tank earth: the dots grow on 2.5 mm²
txt(262, 143.6, '58 door switches', 2.1, 'middle', fill='#555'); txt(262, 146.3, 'row 4', 2.1, 'middle', fill='#555')
A('<rect x="305" y="142" width="6" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(305, 146); dot(311, 146)
txt(308, 153.3, '57 fuel pump', 2.1, 'middle', fill='#555')
A(f'<circle cx="{XP}" cy="146" r="6" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(XP, 147.2, 'M', 3, 'middle', w='bold')
txt(XP, 137.5, '103 Fuel pump', 2.6, 'middle', w='bold')
# The pump's earth goes through 1-pole tank earth connector 60 (scan p.407, C12): 262 SV 2.5 and 190 SV from fuel level
# transmitter 46 share its pump-side pin, and 191 SV 2.5 leaves the other pin for an earth just below it (probably a body
# earth near the tank). 262 runs right to the column between 95 and 271, then down into the pin; 190 comes down from its
# tag above the pump onto 262's corner, so both reach the pin from the pump side.
X60, Y60 = 358, 154                                                  # 60's pump-side pin (top); the other pin is 6 below
wire('262', [(XP + 6, 146), (X60, 146), (X60, Y60)], XP + 9.5, 143.5)
Y190 = 128.9                                                        # 1.1 above 261a's top run, so the tag doesn't read as its end
wire('190', [(354, Y190), (X60, Y190), (X60, 146)], label=False)
tag(352, Y190, '190 SV 0.75 ← fuel level transmitter 46 (instruments sheet)', w=66, size=2.4, anchor='end')
A(f'<rect x="{X60 - 4}" y="{Y60}" width="8" height="6" fill="#ddd" stroke="#111" stroke-width=".5"/>')   # 6 tall: both pin dots grow on the heavy leads
wire('191', [(X60, Y60 + 6), (X60, 170)], X60 + 4, 167.5); earth(X60, 170)
dot(X60, 146); dot(X60, Y60); dot(X60, Y60 + 6)                    # the join and both pins, on top of the 2.5 mm² leads
txt(X60 + 6, Y60 + 3.8, '60 tank earth', 2.1, fill='#555')
wire('261a', [T87, (242.5, 130), (274, 130), (274, 166), (278, 166)], 250, 128.6)   # into engine connector 58 pin 2 on the 102 side
dot(*T87)                                                           # 87 on top of both leads; dot() grows over 261's 2.9 mm stroke and hides its ends
# 95 and 96: a winding each, drawn mirrored (manual: both terminals on the right wall, feed upper, earth lower)
def regulator(y, n, s, sub):
    box(300, y, 50, 16); dot(300, y + 4); dot(300, y + 12)
    cl, cr, ct, cb = coil(304, y + 5.5, 8, 5); inner([(300, y + 4), (ct[0], y + 4), ct]); inner([(300, y + 12), (cb[0], y + 12), cb])
    name(315, y + 6, n, s); txt(315, y + 11, sub, 2.2, fill='#555')
# engine connector 58 pin 2 as a block like pins 1, 3 and 4: 261a alone on the 102 side; 265 and 267 both leave the pin
# on the 95/96 side (book: 265 straight, 267 on a diagonal; scan p.407, book photo IMG_4696), no splice outside it
wire('265', [(282, 166), (285, 162), (300, 162)], 281, 160.3)
regulator(158, '95', 'Aux. air regulator', 'heated; on with the pump')
# 266 and 268 run to the main earth star (scan p.407, labelled again at the star); labelled by their earths, as the wipers
# sheet does for 99/99a
wire('266', [(300, 170), (295, 170), (295, 173)], label=False); earth(295, 173); txt(299.5, 176.8, '266 SV 0.75', 2.1)
regulator(198, '96', 'Warm-up regulator', 'heated')
wire('267', [(300, 202), (285, 202), (285, 170), (282, 166)], 283.9, 200.5, rot=-90)   # label below 284's crossing
A('<rect x="278" y="162" width="4" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(278, 166); dot(282, 166)
txt(278.5, 174.3, '58 engine', 2.1, 'middle', fill='#555'); txt(278.5, 177, 'pin 2', 2.1, 'middle', fill='#555')   # left of centre: clear of 267
wire('268', [(300, 210), (295, 210), (295, 213)], label=False); earth(295, 213); txt(299.5, 216.8, '268 SV 0.75', 2.1)
# cold-start valve 94: a winding (manual: both terminals on the top edge, 273 left, 272 right)
box(300, 232, 40, 16); name(300, 229.6, '94', 'Cold-start valve'); txt(303, 246, 'fed while cranking', 2.2, fill='#555')
cl, cr, ct, cb = coil(316, 237, 8, 6); inner([(300, 240), cl]); inner([cr, (340, 240)]); dot(300, 240); dot(340, 240)
wire('273', [(340, 240), (362, 240)], 342, 238.3)
# thermo-time switch 92, drawn mirrored (manual: 271 upper right, 273 lower right, earth into the left wall level with 271).
# Black: earth line, contact (closed, as printed) and the thick bar to 273. Grey: the heater wound round the bar.
# Not drawn: a second meander between the two terminals, whose meaning the print does not show (see notes).
box(362, 225, 33, 20); name(362, 222.4, '92', 'Thermo-time switch'); txt(362, 249.6, 'earths the valve when cold', 2.2, fill='#555')
A('<path d="M362,239.5 H381.8 V238.3 H386.3 V240.5 H362 Z" fill="#111"/>')    # bar, raised at its free end
inner([(380.3, 230), (380.3, 242.2), (377.5, 242.2), (377.5, 236.3), (374.5, 236.3), (374.5, 242.2), (372.2, 242.2),
       (372.2, 236.3), (369.6, 236.3), (369.6, 242.2), (367.1, 242.2), (367.1, 233.3), (362, 230)], grey=True)   # heater, over the bar: wound round it, not joined
inner([(395, 230), (380.3, 230)]); inner([(383.5, 230), (383.5, 236.5)]); contact(383.5, 237.3); dot(362, 230); dot(362, 240)
A('<path d="M395,230 h5 v5" stroke="#111" stroke-width=".6" fill="none"/>'); earth(400, 235)

# ---- high-speed fuel boost (1979 Turbo only) ------------------------------------
FB = 5                                                               # the block's left part sits right of 272's riser (x XR)
txt(80 + FB, 187, 'High-speed fuel boost', 2.8, w='bold')             # 1979 Turbo only (manual PDF p. 24, 33, 210); 284a runs above
txt(80 + FB, 191.3, 'Richens the mixture above about 130 km/h (140) or at 62° throttle (137).', 2.1, fill='#555')
box(118 + FB, 194, 30, 14); txt(133 + FB, 200.3, '140', 2.8, 'middle', w='bold'); txt(133 + FB, 204.8, 'Speed transmitter', 2.0, 'middle')   # the 1979 legend numbers it 151
dot(118 + FB, 201); tlabel(119.5 + FB, 199.7, '15'); dot(148 + FB, 198); tlabel(146.5 + FB, 197.2, 'W', 'end')
wire('380', [(114 + FB, 201), (118 + FB, 201)], label=False); tag(82 + FB, 201, '380 GL 1.0 ← fuse 5')
# 381 SV: 140's earth. Scan p.407 and book photos: down from -31, right, into brake warning switch 42's corner by its
# earth-side lead, so it reaches joint 158 through 192 SV (power sheet). -31 sits near the left corner and 142 is set
# right, so the tag has room below 140 before 383's riser. Two lines, since 42 is drawn on the instruments sheet and 192
# on the power sheet: it fits between 140 and 137 with '-31' moved left of the lead.
wire('381', [(123 + FB, 208), (123 + FB, 213.5), (126 + FB, 213.5)], label=False); dot(123 + FB, 208)
tlabel(121.8 + FB, 210.9, '-31', 'end')                                   # printed '-31'; outside the box
mtag(128 + FB, 213.5, ('381 SV 0.75 → brake warning switch 42 (instruments sheet)', '→ 192 SV → earth joint 158 (power sheet)'), w=62)
X142 = 222                                                           # 142's left wall
wire('382', [(148 + FB, 198), (X142, 198)], 152 + FB, 196.5)
txt(151 + FB, 204.5, 'on the car: speedometer cable, engine bay (check E7)', 1.9, fill='#555')
# solenoid valve 142: the outline is the winding (one diagonal, no inner rectangle); drawn mirrored (manual: earth left, 382 right)
box(X142, 191, 10, 14); A(f'<path d="M{X142 + .8},204.2 L{X142 + 9.2},191.8" stroke="#111" stroke-width=".35"/>'); dot(X142, 198)
A(f'<path d="M{X142 + 10},198 h8 v4" stroke="#111" stroke-width=".6" fill="none"/>'); earth(X142 + 18, 202); txt(X142 + 5, 189.3, '142 Solenoid valve', 2.2, 'middle', w='bold')
for i, s in enumerate(('on the car: front of the engine, on the control', 'pressure line (check E7); 382 and 383 on one contact,',
                       'earth on the other (check E12)')):
    txt(X142 + 6, 212 + 2.8 * i, s, 1.9, fill='#555')
# throttle switch 137, turned a quarter (manual: portrait, pivot at the bottom terminal, contact at the top); open at rest
box(126 + FB, 219, 14, 12); dot(126 + FB, 225); dot(140 + FB, 225)
inner([(126 + FB, 225), (128.2 + FB, 225)]); contact(129 + FB, 225); contact(137 + FB, 225); inner([(137.8 + FB, 225), (140 + FB, 225)])
blade(129.6 + FB, 224.6, 136.6 + FB, 221.6)
txt(120 + FB, 235, '<tspan font-weight="bold">137</tspan> Throttle switch, 62°', 2.4)
wire('380a', [(114 + FB, 225), (126 + FB, 225)], label=False); tag(82 + FB, 225, '380a GL 1.0 ← fuse 5')
wire('383', [(140 + FB, 225), (X142 - 5, 225), (X142 - 5, 198)], 150 + FB, 223.5); dot(X142 - 5, 198)   # joins 382 at 142's feed terminal: one contact on the car (E12)

# ---- service outlet 73 (TSI), in the free corner under the starter ----------------------------------
# Drawn as the book prints it (scan p.407; book photos IMG_4717 at 73, IMG_4696 at 58): a heavy ring with six pins, 4 at
# the top, 1 at the bottom, 3 and 2 on the left, 5 and 6 on the right. The reference photo of a 900 socket seen from its face
# (source/ref/c900-tsi-socket.jpg) has the same order the other way round, so the print is probably the wire side; which way
# round is not settled, so the caption claims only the order (check E11). Pin 5 takes two leads of its own, no splice:
# 284a on a diagonal, 204 straight. Pin 6 is empty.
# 282 tees off 122a (89:87 to starter 50) and drops straight into pin 3, crossing 272 once. 284a runs right as a wire,
# crossing 272's riser once, under the 263 tag and above the fuel boost title, into 102's bottom pair. 283 stays a tag
# (every way down from 58 engine pin 4 crosses the 202 tag or relay 89): up from pin 4 and over 272 into the band above the
# fuel boost title. 204, 280 and 281 end in tags on the left; 204 turns back under the socket to reach them.
CX, CY, R, RP, TE = 64.5, 188.75, 7.5, 5, 50                         # centre, ring and pin-circle radii; left tags end at TE
def on_ring(a, r=R): return (round(CX + r * math.cos(math.radians(a)), 2), round(CY - r * math.sin(math.radians(a)), 2))
PIN = {'4': 90, '3': 150, '2': -150, '1': -90, '6': -30, '5': 30}
P = {n: on_ring(a) for n, a in PIN.items()}                          # where each pin's lead meets the ring
wire('282', [(P['3'][0], 141.5), P['3']], P['3'][0] - 1.4, 183, rot=-90); dot(P['3'][0], 141.5)
Y283, XT = 169, XR + 6                                               # 283's run and the band tag's left end
wire('283', [P['4'], (CX, Y283), (XT - 2, Y283)], label=False)
mtag(XT, Y283, ('283 GN/VT 0.75 ← 58 engine pin 4,', 'switch side (top of sheet)'), w=38.3)
# 284a: its run at y 182 lines up with 284's on the far side of the pair (the pair is drawn joined)
wire('284a', [P['5'], (P['5'][0] + 3, 182), (TP1[0], 182), TP1], XT + 9, 180.4); dot(*TP1)   # the pair's circle on top
X204 = 76.5                                                          # 204's drop, between the socket and 272's riser
wire('204', [P['5'], (X204, P['5'][1]), (X204, 213.5), (TE + 2, 213.5)], label=False)
mtag(TE, 213.5, ('204 GL 0.75 → tachometer', '110 (instruments sheet)'), w=29.9, anchor='end')
wire('280', [P['1'], (CX, 203), (TE + 2, 203)], label=False)
mtag(TE, 203, ('280 GR 1.5 ← bar 7–12', '(power sheet)'), w=26.7, anchor='end')
wire('281', [P['2'], (TE + 2, P['2'][1])], label=False)
mtag(TE, P['2'][1], ('281 SV 1.5 → earth joint 158', '(power sheet)'), w=31.6, anchor='end')
A(f'<circle cx="{CX}" cy="{CY}" r="{R}" fill="#fff" stroke="#111" stroke-width="1.4"/>')   # over the lead ends
for n, a in PIN.items():
    px, py = on_ring(a, RP)
    A(f'<circle cx="{px}" cy="{py}" r=".6" fill="#fff" stroke="#111" stroke-width=".3"/>')
    if px == CX: tlabel(CX, round(py + (2.6 if py < CY else -1.2), 2), n, 'middle')      # 4 and 1: number towards the centre
    else: tlabel(round(px + (1.2 if px < CX else -1.2), 2), round(py + .65, 2), n, 'start' if px < CX else 'end')
name(14, 226, '73', 'Service outlet (TSI)')
for i, s in enumerate(('Pins in their order round the socket (check E11):', '1 battery +, 2 earth, 3 start, 4 ignition +15,',
                       '5 engine speed (284a from 102, 204 to the tachometer),', '6 empty.')):
    txt(14, 230.4 + 2.8 * i, s, 2.1, fill='#555')

# ---- legend and notes ----------------------------------------------------
lx, ly = 18, 256
box(lx, ly, 389, 31, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 4
size_legend(x, ly + 17)                                              # under the colours: line width is the cable size
A(f'<path d="M{x},{ly + 22} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, ly + 23, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x + 48},{ly + 22} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 59, ly + 23, 'not traced yet', 2.4)
hx = x + (80 if DASHED[0] else 48)                                   # the HT sample beside the traced one, after 'not traced yet' when that shows
ht([(hx, ly + 22), (hx + 9, ly + 22)]); txt(hx + 11, ly + 23, 'HT lead', 2.4)
probable_legend(x, ly + 28)
if TICKED[0]: tick(x + 66, ly + 28.3); txt(x + 70, ly + 29, 'checked on the car', 2.4)
notes = ['Overboost cut: pressure switch 144 (closed at rest) is in the fuel pump relay’s feed (15). If it opens, the relay drops out and the pump stops.',
         'The pump relay also takes an engine-speed signal from 146 (284 BL), which normally stops the pump when the engine isn’t turning.',
         'Start relay 89: its coil is earthed directly (201 SV), so it pulls in whenever the key is at start. It feeds starter terminal 50 (the solenoid)',
         'from the always-live bar, and 87a feeds 394 to the joint of 147’s two resistors, bypassing the 0.4 Ω one while cranking (the 0.6 Ω stays in).',
         '92 may also have a second element between its two terminals (perhaps a second heater); it is not drawn, as what it is is not known.',
         'Sender cable 390/391 is screened; 392 SV earths the screen. Pin and row numbers of the 58 connectors are our own count, top to bottom (engine: check E1).',
         'Not RHD-specific: circuits should match the car, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 4.8 + j * 3.9, n, 2.3, fill='#333')
notes2 = ['263 SV (pump relay 31) goes to relay 21, probably its 85, and on to earth joint 158.',
          '100 SV, headlight wiper relay 67’s earth, also lands on 102:31. 201 SV goes to 158 directly.',
          '123d (+15 for 146) leaves engine connector 58 pin 4 on the 147 side, before the ballast',
          'resistor. 377 and 283 leave the pin on the switch side, each its own lead beside 123.',
          '102’s joined bottom pair (marked 31) takes the speed signal (284, 284a): probably terminal 1.',
          '381 SV (140’s earth) lands on 42’s earth side, probably spliced into 192 SV there.',
          '266, 268, 392 and 393 SV go to the central earth star. Relay 21, joint 158: power sheet.']
for j, n in enumerate(notes2): txt(lx + 276, ly + 4.8 + j * 3.9, n, 2.3, fill='#333')
save('ignition.svg')

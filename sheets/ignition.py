#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo ignition, starting and fuel injection sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Ignition, starting and fuel injection')
def ht(pts): A(f'<path d="{path(pts)}" fill="none" stroke="#444" stroke-width="1.1" stroke-linejoin="round"/>')
def name(x, y, n, s, anchor='start'): txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', 2.7, anchor)
# Joint on a 2.5 mm² wire: r 1.8, so it still shows past the 2.9 mm stroke and reads as a joint, not a rivet in the band

# ---- ignition switch and starter ----------------------------------------
box(18, 38, 40, 32); name(21, 44, '20', 'Ignition switch')
for t, y in (('30', 44), ('15', 54), ('50', 64)): dot(58, y); txt(56, y + 1, t, 2.4, 'end')
wire('7', [(58, 44), (66, 44)], label=False); tag(68, 44, '← 7 GR 2.5 from bar 7–12')
wire('123', [(58, 54), (146, 54)], 70, 52.5); dot(58, 54)           # 15 on top of its 1.5 mm² lead
wire('122', [(58, 64), (80, 64), (80, 86), (96, 86), (96, 90)], 60, 62.3)
dot(58, 44); dot(58, 64)                                             # 30 and 50 on top of their 2.5 mm² leads

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
wire('122a', [(104, 122), (104, 141.5), (52, 141.5)], 56, 139.8); dot(104, 122); dot(52, 141.5)   # 87 and 50 on top of it
wire('282', [(104, 137), (108, 137)], label=False); tag(110, 137, '282 GL 1.0 → 73 service outlet (start terminal)')
# 271: 89:87 to 92's heater through 58/1. Under 394, up into the band below 124, across 284's riser (the only way out: 284
# wraps 102 and the injection parts) and down the free strip right of it; 58/1 on the drop, then round into 92's left wall
Y271 = 124.2
wire('271', [(104, 131), (180, 131), (180, Y271), (368, Y271), (368, 214), (356, 214), (356, 230), (362, 230)], 366.6, 210, rot=-90)
dot(104, 131); dot(104, 137)                                       # 271 and 282 tee off 122a: on top of all three
A('<rect x="364" y="186" width="8" height="4" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(368, 186); dot(368, 190)
txt(374, 189, '58 engine, pin 1', 2.1, fill='#555')
# the RD label sits on the 92 side, where the book prints it; the relay side of 58 (A4) pin 1 is GN 1.0 (data/connectors.csv),
# but wires.csv has one row for 271, so the whole run is drawn RD until that is split
txt(374, 192.2, 'relay side probably GN 1.0 (check E1)', 1.8, fill='#777')
wire('272', [(52, 156.5), (70, 156.5), (70, 240), (300, 240)], 80, 238.5)
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
wire('390', [(271, 57), (284, 57), (284, 52), (308, 52)], label=False); txt(277, 47.8, '390, 391 screened', 2.2, fill='#555')
wire('391', [(271, 64), (288, 64), (288, 59), (308, 59)], label=False)
wire('392', [(285, 67), (285, 72)], label=False); earth(285, 72)
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
wire('284', [(308, 73), (300.5, 73), (300.5, 92), (360, 92), (360, 182), (233.5, 182), (227.5, 176)], 246, 180.3)   # into 102's bottom pair

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
wire('284a', [TP1, (224.5, 183), (222, 183)], label=False); tag(220, 183, '284a BL 0.75 → 73 service outlet, pin 5', anchor='end')
# pressure switch 144: contact drawn closed, as the manual prints it
box(160, 151, 20, 10); inner([(160, 156), (163.2, 156)]); inner([(176.8, 156), (180, 156)])
contact(164, 156); contact(176, 156); blade(164.7, 156, 175.2, 156)
txt(170, 165, '144 Pressure switch (overboost)', 2.4, 'middle', w='bold')
wire('378', [(180, 156), (185, 156), (185, 134), (224.5, 134), T15], 189, 132.3)
wire('377', [(160, 156), (150, 156)], label=False); tag(148, 156, '377 GN/VT 0.75 ← 123 at 58 engine pin 4 (top of sheet)', w=68, anchor='end')
# 377 stays a tag: it tees off 123 on the switch side of pin 4 (data/connectors.csv), not the 147 side like 123d, and the only ways down from there cross the
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
wire('261', [T87, (247, 136.5), (290, 136.5), (290, 146), (300, 146)], 252, 134.8)
A('<circle cx="306" cy="146" r="6" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(306, 147.2, 'M', 3, 'middle', w='bold')
txt(306, 137.5, '103 Fuel pump', 2.6, 'middle', w='bold')
# 262 SV 2.5 draws as a 2.9 mm black band: a longer run to the earth, so it reads as a lead, not a block on the pump
wire('262', [(312, 146), (328, 146), (328, 150.5)], 331.5, 150.2); earth(328, 150.5)
wire('261a', [T87, (242.5, 130), (276, 130), (276, 166), (280, 166)], 250, 128.6)
dot(*T87)                                                           # 87 on top of both leads; dot() grows over 261's 2.9 mm stroke and hides its ends
# 95 and 96: a winding each, drawn mirrored (manual: both terminals on the right wall, feed upper, earth lower)
def regulator(y, n, s, sub):
    box(300, y, 50, 16); dot(300, y + 4); dot(300, y + 12)
    cl, cr, ct, cb = coil(304, y + 5.5, 8, 5); inner([(300, y + 4), (ct[0], y + 4), ct]); inner([(300, y + 12), (cb[0], y + 12), cb])
    name(315, y + 6, n, s); txt(315, y + 11, sub, 2.2, fill='#555')
wire('265', [(280, 166), (280, 162), (300, 162)], 281, 160.3)
regulator(158, '95', 'Aux. air regulator', 'heated; on with the pump')
wire('266', [(300, 170), (295, 170), (295, 173)], label=False); earth(295, 173)
regulator(198, '96', 'Warm-up regulator', 'heated')
wire('267', [(300, 202), (280, 202), (280, 166)], 281.4, 200.5); txt(282.5, 172.2, '58 engine', 2.1, fill='#555'); txt(282.5, 175, 'pin 2', 2.1, fill='#555')   # two lines: clear of 266's earth
dot(280, 166)                                                        # 261a/265/267 joint, on top of all three
wire('268', [(300, 210), (295, 210), (295, 213)], label=False); earth(295, 213)
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
txt(80, 186, 'High-speed fuel boost', 2.8, w='bold')                  # 1979 Turbo only (manual PDF p. 24, 33, 210)
txt(80, 190.5, 'Richens the mixture above about 130 km/h (140) or at 62° throttle (137).', 2.1, fill='#555')
box(118, 194, 30, 14); txt(133, 200.3, '140', 2.8, 'middle', w='bold'); txt(133, 204.8, 'Speed transmitter', 2.0, 'middle')   # the 1979 legend numbers it 151
dot(118, 201); tlabel(119.5, 199.7, '15'); dot(148, 198); tlabel(146.5, 197.2, 'W', 'end'); dot(133, 208)
tlabel(134.5, 210.5, '-31')                                          # printed '-31'; outside the box
wire('380', [(114, 201), (118, 201)], label=False); tag(82, 201, '380 GL 1.0 ← fuse 5')
wire('381', [(133, 208), (133, 211)], label=False); earth(133, 211); txt(137, 215, '381 SV', 2.1)
wire('382', [(148, 198), (208, 198)], 152, 196.5)
txt(151, 204.5, 'on the car: speedometer cable, engine bay (check E7)', 1.9, fill='#555')
# solenoid valve 142: the outline is the winding (one diagonal, no inner rectangle); drawn mirrored (manual: earth left, 382 right)
box(208, 191, 10, 14); A('<path d="M208.8,204.2 L217.2,191.8" stroke="#111" stroke-width=".35"/>'); dot(208, 198)
A('<path d="M218,198 h12 v4" stroke="#111" stroke-width=".6" fill="none"/>'); earth(230, 202); txt(213, 189.3, '142 Solenoid valve', 2.2, 'middle', w='bold')
txt(214, 210.6, 'on the car: front of the engine, on the control pressure line (check E7);', 1.9, fill='#555')
txt(214, 213.4, '382 and 383 on one contact, earth on the other (check E12)', 1.9, fill='#555')
# throttle switch 137, turned a quarter (manual: portrait, pivot at the bottom terminal, contact at the top); open at rest
box(126, 219, 14, 12); dot(126, 225); dot(140, 225)
inner([(126, 225), (128.2, 225)]); contact(129, 225); contact(137, 225); inner([(137.8, 225), (140, 225)])
blade(129.6, 224.6, 136.6, 221.6)
txt(120, 235, '<tspan font-weight="bold">137</tspan> Throttle switch, 62°', 2.4)
wire('380a', [(114, 225), (126, 225)], label=False); tag(82, 225, '380a GL 1.0 ← fuse 5')
wire('383', [(140, 225), (203, 225), (203, 198)], 150, 223.5); dot(203, 198)   # joins 382 at 142's feed terminal: one contact on the car (E12)

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
         'Sender cable 390/391 is shielded; the shield is earthed through 392 SV 0.75. Engine connector 58 (12-pole): pin numbers are our own count (check E1).',
         'Not RHD-specific: circuits should match the car, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 4.8 + j * 3.9, n, 2.3, fill='#333')
notes2 = ['263 SV (pump relay 31) goes to relay 21, probably to its 85; 33 and 212 SV',
          'take it on to earth joint 158. 100 SV, headlight wiper relay 67’s earth, also lands on 102:31.',
          '201 SV (relay 89’s coil) goes to 158 directly. Relay 21 and joint 158 are on the power sheet.',
          '123d GN/VT (+15 for 146) comes from engine connector 58 pin 4 on the 147 side,',
          'before the ballast resistor, not from coil terminal 15.',
          '102’s joined bottom pair (marked 31) takes the speed signal (284, 284a): probably terminal 1.']
for j, n in enumerate(notes2): txt(lx + 276, ly + 4.8 + j * 3.9, n, 2.3, fill='#333')
save('ignition.svg')

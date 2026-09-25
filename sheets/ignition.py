#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo ignition, starting and fuel injection sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Ignition, starting and fuel injection',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual.')
def ht(pts): A(f'<path d="{path(pts)}" fill="none" stroke="#444" stroke-width="1.1" stroke-linejoin="round"/>')
def name(x, y, n, s, anchor='start'): txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', 2.7, anchor)

# ---- ignition switch and starter ----------------------------------------
box(18, 38, 40, 32); name(21, 44, '20', 'Ignition switch')
for t, y in (('30', 44), ('15', 54), ('50', 64)): dot(58, y); txt(56, y + 1, t, 2.4, 'end')
wire('7', [(58, 44), (66, 44)], label=False); tag(68, 44, '← 7 GR 2.5 from bar 7–12')
wire('123', [(58, 54), (146, 54)], 70, 52.5)
wire('122', [(58, 64), (80, 64), (80, 86), (96, 86), (96, 90)], 60, 62.3)

# starter 4, drawn upside down (manual: 16 upper right, 50 lower right, 30 bottom centre); nothing printed inside
box(18, 134, 34, 30); name(22, 150, '4', 'Starter')
A('<rect x="16" y="147" width="2.4" height="4" fill="#fff" stroke="#111" stroke-width=".5"/>'
  '<rect x="12.6" y="145" width="3.4" height="8" rx=".6" fill="#111"/>')   # pinion (mechanical, as printed)
dot(35, 134); txt(33.6, 137.4, '30', 2.1, 'end', fill='#555')
for t, y in (('50', 141.5), ('16', 156.5)): dot(52, y); txt(50, y + .8, t, 2.1, 'end', fill='#555')
wire('1', [(35, 134), (35, 129), (38, 129)], label=False); tag(40, 129, '1 RD 16.0 ← battery +', size=2.4)

# relay 89, drawn upside down (manual: 85, 87, 87a on the top edge; 86, 30 on the bottom), contacts at rest as printed
box(88, 90, 32, 32)
txt(123.5, 103.5, '89', 3.2, w='bold'); txt(123.5, 108, 'Start relay', 2.5)
txt(123.5, 111.5, '(legend: start inhibitor relay)', 2.1, fill='#555')
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
wire('202', [(112, 90), (112, 84), (118, 84)], label=False); tag(120, 84, '202 GR 1.5 ← bar 7–12 (always live)')
wire('122a', [(104, 122), (104, 141.5), (52, 141.5)], 56, 139.8); dot(104, 131); dot(104, 137)
wire('271', [(104, 131), (108, 131)], label=False); tag(110, 131, '271 RD 1.0 → 92 thermo-time switch heater, via 58/1')
wire('282', [(104, 137), (108, 137)], label=False); tag(110, 137, '282 GL 1.0 → 73 service outlet (start terminal)')
wire('271', [(362, 230), (356, 230), (356, 223), (352, 223)], label=False); tag(350, 223, '271 RD 1.0 ← relay 89 (87)', anchor='end')
wire('272', [(52, 156.5), (70, 156.5), (70, 240), (300, 240)], 80, 238.5)
A('<rect x="199" y="236" width="4" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(199, 240); dot(203, 240); txt(201, 234.3, '58/3', 2.1, 'middle', fill='#555')

# ---- ballast resistor, coil, distributor, plugs, control unit ----------
A('<rect x="146" y="48" width="4" height="12" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(146, 54); dot(150, 54)
txt(148, 46, '58', 2.4, 'middle', w='bold'); txt(148, 64, 'A4/4', 2.1, 'middle', fill='#555')
wire('123', [(150, 54), (170, 54)], label=False)
# ballast resistor 147 (scan; car photo 25 Sep: a Bosch block stamped 0.4 and 0.6, their ends strapped at the joint): two resistors
# joined at the bottom by a link; 394 leaves at that joint. The feed side (123) is the 0.4 Ω one, the coil side (123b) the 0.6 Ω.
box(170, 49, 16, 16); txt(167.4, 45, '<tspan font-weight="bold">147</tspan> Ballast resistor', 2.5)   # start-anchored: cairosvg splits a middle-anchored tspan
for x in (174, 182):
    dot(x, 65); a, b = resistor(x - 1.2, 55.5, 2.4, 4.8); inner([b, (x, 65)])
inner([(170, 54), (174, 54), (174, 55.5)]); inner([(186, 54), (182, 54), (182, 55.5)]); inner([(174, 62.6), (182, 62.6)])
tlabel(174, 52.6, '0.4 Ω', 'middle'); tlabel(182, 52.6, '0.6 Ω', 'middle')
wire('123b', [(186, 54), (214, 54)], 188, 52.3); dot(170, 54); dot(186, 54)   # all four printed terminals
txt(188, 57.4, 'book: GN/VT', 1.8, fill='#777')                     # yellow on the car (E2, E3)
wire('394', [(174, 65), (174, 126), (112, 126), (112, 122)], 172.6, 116, rot=-90)
box(214, 46, 18, 30); txt(223, 43.5, '5 Coil', 2.7, 'middle', w='bold')
dot(214, 54); txt(216, 54.8, '15', 2.1, fill='#555'); dot(214, 68); txt(216, 68.8, '1', 2.1, fill='#555')
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
wire('393', [(308, 45), (304.5, 45), (304.5, 35), (350, 35), (350, 39)], 318, 33.5); earth(350, 39)
# 123d: +15 for 146 from 58 (A4) pin 4 on the 147 side, before the ballast resistor (book photo IMG_4729: it passes
# under the coil without joining it); branched just right of the pin, it crosses 394 without a joint
wire('123d', [(156, 54), (156, 73), (206, 73), (206, 112), (296, 112), (296, 66), (308, 66)], 220, 110.5); dot(156, 54)
wire('121', [(308, 80), (304.5, 80), (304.5, 87), (346, 87)], label=False); e121 = tag(348, 87, '121 BL 1.5 → coil 5, terminal 1')
if WIRES['121']['status'] == 'car': tick(e121 + 1.2, 86.4)
wire('284', [(308, 73), (300.5, 73), (300.5, 92), (360, 92), (360, 190), (241, 190), (241, 176)], 300, 188.5)

# ---- fuel pump relay, overboost switch, pump and injection parts -------
# fuel pump relay 102 (scan only, no photo): contact 30-87 open at rest and its coil fed from 15 are clear;
# the electronic part that switches the coil is printed clearly, with 15 into its top; its 31, coil and 284 leads are not: grey
box(220, 140, 42, 36); name(220, 137.6, '102', 'Fuel pump relay')
for t, y in (('30', 146), ('15', 156), ('31', 166)): dot(220, y); tlabel(222, y - 1.3, t)
dot(262, 146); tlabel(260, 144.7, '87', 'end'); dot(241, 176)       # 284's terminal: no label printed
inner([(220, 146), (245.2, 146)]); contact(246, 146); contact(255, 146); inner([(255.8, 146), (262, 146)])
blade(246.7, 145.6, 254.4, 142.5)                                    # 30-87: open at rest
cl, cr, ct, cb = coil(246, 153, 8, 6); inner([(220, 156), cl]); mlink([ct, (250, 144.4)])
def module(x, y, w, h):   # the relay's electronics: a plain box, printed clearly; the caption is ours (grey)
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#111" stroke-width=".4"/>')
    txt(x + w / 2, y + h / 2 + .7, 'electronics', 1.8, 'middle', fill='#888')
module(231, 162.5, 16, 7)
inner([(236, 156), (236, 162.5)])                                    # 15 into the box's top: printed clearly
for p in ([(220, 166), (231, 166)], [cb, (250, 160.5), (242, 160.5), (242, 162.5)], [(241, 169.5), (241, 176)]):
    inner(p, grey=True)                                              # 31, coil return and 284: not clear
wire('260', [(220, 146), (198, 146)], label=False); tag(196, 146, '260 GR 1.5 ← fuse 10', anchor='end')
# pressure switch 144: contact drawn closed, as the manual prints it
box(160, 151, 20, 10); inner([(160, 156), (163.2, 156)]); inner([(176.8, 156), (180, 156)])
contact(164, 156); contact(176, 156); blade(164.7, 156, 175.2, 156)
txt(170, 165, '144 Pressure switch (overboost)', 2.4, 'middle', w='bold')
wire('378', [(180, 156), (220, 156)], 183, 154.3)
wire('377', [(160, 156), (150, 156)], label=False); tag(148, 156, '377 GN/VT 0.75 ← ignition 15 at 58/4', anchor='end')
dot(160, 156); dot(180, 156)
wire('263', [(220, 166), (216, 166), (216, 171.5), (212, 171.5)], label=False)   # the pump relay's 31, to relay 21's coil earth
tag(210, 171.5, '263 SV 0.75 → relay 21:85 (power sheet)', anchor='end')
# 100 SV: relay 67's coil earth (via 100a) and contact 87, also on 102:31 (scan: both leads leave 31 to the left; 1977 Turbo diagram)
wire('100', [(216, 171.5), (216, 178.5), (212, 178.5)], label=False); dot(216, 171.5)
tag(210, 178.5, '100 SV 0.75 ← relay 67:87 (wipers sheet)', anchor='end')
wire('261', [(270, 146), (300, 146)], 272, 144.3); dot(270, 146)
A('<circle cx="306" cy="146" r="6" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(306, 147.2, 'M', 3, 'middle', w='bold')
txt(306, 137.5, '103 Fuel pump', 2.6, 'middle', w='bold')
wire('262', [(312, 146), (322, 146), (322, 150)], label=False); earth(322, 150)
wire('261a', [(262, 146), (270, 146), (270, 166), (280, 166)], 268.6, 175, rot=-90)
# 95 and 96: a winding each, drawn mirrored (manual: both terminals on the right wall, feed upper, earth lower)
def regulator(y, n, s, sub):
    box(300, y, 50, 16); dot(300, y + 4); dot(300, y + 12)
    cl, cr, ct, cb = coil(304, y + 5.5, 8, 5); inner([(300, y + 4), (ct[0], y + 4), ct]); inner([(300, y + 12), (cb[0], y + 12), cb])
    name(315, y + 6, n, s); txt(315, y + 11, sub, 2.2, fill='#555')
wire('265', [(280, 166), (280, 162), (300, 162)], 281, 160.3)
regulator(158, '95', 'Aux. air regulator', 'heated; on with the pump')
wire('266', [(300, 170), (295, 170), (295, 173)], label=False); earth(295, 173)
regulator(198, '96', 'Warm-up regulator', 'heated')
wire('267', [(300, 202), (280, 202), (280, 166)], 281.4, 200.5); txt(282.5, 173, '58/2', 2.1, fill='#555')
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
txt(80, 186, 'High-speed fuel boost (1979 Turbo only)', 2.8, w='bold')
txt(80, 190.5, 'Richens the mixture above about 130 km/h (140) or at 62° throttle (137). PDF p. 24, 33, 210.', 2.1, fill='#555')
box(118, 194, 30, 14); txt(133, 199.5, '140', 2.8, 'middle', w='bold'); txt(133, 204, 'Speed transmitter', 2.0, 'middle'); txt(133, 206.6, '(legend: 151)', 1.8, 'middle', fill='#555')
dot(118, 201); tlabel(119.5, 199.7, '15'); dot(148, 198); tlabel(146.5, 197.2, 'W', 'end'); dot(133, 208)
tlabel(134.5, 210.5, '-31')                                          # printed '-31'; outside, clear of '(legend: 151)'
wire('380', [(114, 201), (118, 201)], label=False); tag(82, 201, '380 GL 1.0 ← fuse 5')
wire('381', [(133, 208), (133, 211)], label=False); earth(133, 211); txt(137, 215, '381 SV', 2.1)
wire('382', [(148, 198), (208, 198)], 152, 196.5)
txt(151, 204.5, 'on the car: on the speedometer cable, engine bay (E7)', 1.9, fill='#555')
# solenoid valve 142: the outline is the winding (one diagonal, no inner rectangle); drawn mirrored (manual: earth left, 382 right)
box(208, 191, 10, 14); A('<path d="M208.8,204.2 L217.2,191.8" stroke="#111" stroke-width=".35"/>'); dot(208, 198)
A('<path d="M218,198 h12 v4" stroke="#111" stroke-width=".6" fill="none"/>'); earth(230, 202); txt(213, 189.3, '142 Solenoid valve (E3)', 2.2, 'middle', w='bold')
txt(214, 210.6, 'on the car: front of the engine, on the control pressure line (E7);', 1.9, fill='#555')
txt(214, 213.4, '382 and 383 on one contact, earth on the other (E12)', 1.9, fill='#555')
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
A(f'<path d="M{x},{ly + 16} h9" stroke="#222" stroke-width="1.2"/>'); txt(x + 11, ly + 17, 'traced (cable no. read)', 2.4)
if DASHED[0]: A(f'<path d="M{x + 48},{ly + 16} h9" stroke="#222" stroke-width="1.2" stroke-dasharray="3 2"/>'); txt(x + 59, ly + 17, 'not traced yet', 2.4)
ht([(x, ly + 22), (x + 9, ly + 22)]); txt(x + 11, ly + 23, 'HT lead', 2.4)
if TICKED[0]: tick(x + 48, ly + 22.3); txt(x + 52, ly + 23, 'checked on the car', 2.4)
probable_legend(x, ly + 28)
notes = ['Overboost cut: pressure switch 144 (closed at rest) is in the fuel pump relay’s feed (15). If it opens, the relay drops out and the pump stops.',
         'The pump relay also takes an engine-speed signal from 146 (284 BL), which normally stops the pump when the engine isn’t turning.',
         'Relay 89 is called “start inhibitor relay” in the legend, but here its coil is earthed directly, so it works as a start relay: it feeds starter terminal 50 (the solenoid)',
         'from the always-live bar, and 87a feeds 394 to the joint of 147’s two resistors, bypassing the 0.4 Ω one while cranking (the 0.6 Ω stays in; PDF p. 324).',
         '92 also has a second meander from its upper terminal to its lower one; the print does not show what it is, so it is not drawn.',
         'Sender cable 390/391 is shielded; the shield is earthed through 392 SV 0.75. 58/n = pin n of the 12-pole connector at grid A4 (data/connectors.csv).',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 4.8 + j * 3.9, n, 2.3, fill='#333')
notes2 = ['263 SV (pump relay 31) goes to relay 21:85 (probably 85: hidden under 21’s border); 33 and 212 SV',
          'take it on to earth joint 158. 100 SV, headlight wiper relay 67’s earth, also lands on 102:31.',
          '201 SV (relay 89’s coil) goes to 158 directly. Relay 21 and joint 158 are on the power sheet.',
          '123d GN/VT (+15 for 146) leaves pin 4 of 58 (A4) on the 147 side, before the ballast resistor;',
          'in the book it passes under the coil without joining it (IMG_4729; 1977 Turbo diagram).',
          '121 BL: the 1979 number is unreadable; the 1977 Turbo diagram prints 124 BL 1.5.']
for j, n in enumerate(notes2): txt(lx + 276, ly + 4.8 + j * 3.9, n, 2.3, fill='#333')
save('ignition.svg')

#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo ignition, starting and fuel injection sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Ignition, starting and fuel injection',
       'Redrawn from Saab Service Manual 1975–1980, diagram p. 371-28/29 (PDF p. 406–407). '
       'Component numbers as in the manual. Dashed = not traced yet.')
def ht(pts): A(f'<path d="{path(pts)}" fill="none" stroke="#444" stroke-width="1.1" stroke-linejoin="round"/>')
def name(x, y, n, s, anchor='start'): txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', 2.7, anchor)

# ---- ignition switch and starter ----------------------------------------
box(18, 38, 40, 32); name(21, 44, '20', 'Ignition switch')
for t, y in (('30', 44), ('15', 54), ('50', 64)): dot(58, y); txt(56, y + 1, t, 2.4, 'end')
wire('7', [(58, 44), (66, 44)], label=False); tag(68, 44, '← 7 GR 2.5 from bar 7–12')
wire('123', [(58, 54), (146, 54)], 70, 52.5)
wire('122', [(58, 64), (80, 64), (80, 96), (88, 96)], 60, 62.3)
box(18, 118, 34, 30); name(21, 124, '4', 'Starter')
for t, y in (('30', 126), ('50', 135), ('16', 144)): dot(52, y); txt(50, y + 1, t, 2.4, 'end')
wire('1', [(52, 126), (62, 126)], label=False); tag(64, 126, '1 RD 16.0 ← battery +', size=2.4)
box(88, 90, 36, 30)
txt(106, 102, '89', 3.2, 'middle', w='bold'); txt(106, 106.5, 'Start relay', 2.5, 'middle')
txt(106, 110, '(legend: start', 2.1, 'middle', fill='#555'); txt(106, 112.8, 'inhibitor relay)', 2.1, 'middle', fill='#555')
for t, x, y, a in (('86', 88, 96, 'start'), ('85', 88, 114, 'start'), ('30', 124, 105, 'end')):
    dot(x, y); txt(x + (1.5 if a == 'start' else -1.5), y + (3.5 if t != '30' else 1), t, 2.2, a)
dot(112, 90); txt(114, 93.5, '87a', 2.2); dot(100, 120); txt(101.5, 118.5, '87', 2.2)
wire('201', [(88, 114), (82, 114), (82, 118)], label=False); earth(82, 118); txt(71, 116, '201 SV', 2.2)
wire('202', [(124, 105), (140, 105)], label=False); tag(142, 105, '202 GR 1.5 ← bar 7–12 (always live)')
wire('122a', [(100, 120), (100, 135), (52, 135)], 56, 133.5); dot(100, 124); dot(100, 130)
wire('271', [(100, 124), (108, 124)], label=False); tag(110, 124, '271 RD 1.0 → 92 thermo-time switch heater, via 58/1')
wire('282', [(100, 130), (108, 130)], label=False); tag(110, 130, '282 GL 1.0 → 73 service outlet (start terminal)')
wire('271', [(372, 232), (372, 226)], label=False); tag(370, 226, '271 RD 1.0 ← relay 89 (87)', anchor='end')
wire('272', [(52, 144), (70, 144), (70, 240), (300, 240)], 80, 238.5)
A('<rect x="199" y="236" width="4" height="8" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(199, 240); dot(203, 240); txt(201, 234.3, '58/3', 2.1, 'middle', fill='#555')

# ---- ballast resistor, coil, distributor, plugs, control unit ----------
A('<rect x="146" y="48" width="4" height="12" fill="#ddd" stroke="#111" stroke-width=".5"/>'); dot(146, 54); dot(150, 54)
txt(148, 46, '58', 2.4, 'middle', w='bold'); txt(148, 64, 'A4/4', 2.1, 'middle', fill='#555')
wire('123', [(150, 54), (168, 54)], label=False)
box(168, 48, 16, 12); A('<path d="M170,54 l2,-3 l2,6 l2,-6 l2,6 l2,-6 l2,6 l1.5,-3" fill="none" stroke="#111" stroke-width=".4"/>')
txt(176, 45, '147 Ballast resistor', 2.5, 'middle')
wire('123b', [(184, 54), (214, 54)], 186, 52.3); dot(206, 54)
wire('394', [(176, 60), (176, 82), (112, 82), (112, 90)], 130, 80.5)
box(214, 46, 18, 30); txt(223, 43.5, '5 Coil', 2.7, 'middle', w='bold')
dot(214, 54); txt(216, 55, '15', 2.3); dot(214, 68); txt(216, 69, '1', 2.3)
A('<circle cx="262" cy="61" r="9" fill="#fff" stroke="#111" stroke-width=".8"/><circle cx="262" cy="61" r="1" fill="#111"/>')
txt(262, 48, '6 Distributor', 2.7, 'middle', w='bold')
ht([(232, 61), (253, 61)])
for i, x in enumerate((248, 258, 268, 278)):
    ht([(262 + (i - 1.5) * 3, 70), (x, 86)])
    A(f'<path d="M{x - 1.8},{86} h3.6 l-0.8,7 h-2 z" fill="#fff" stroke="#111" stroke-width=".5"/><path d="M{x},{93} v2" stroke="#111" stroke-width=".5"/>')
    txt(x, 99, str(i + 1), 2.2, 'middle')
txt(263, 104, '157 Spark plugs', 2.6, 'middle', w='bold')
A('<rect x="277" y="49" width="16" height="18" rx="2" fill="none" stroke="#888" stroke-width=".3"/>')
wire('390', [(271, 57), (284, 57), (284, 52), (300, 52)], label=False); txt(278, 47.8, '390, 391 screened', 2.2, fill='#555')
wire('391', [(271, 64), (288, 64), (288, 59), (300, 59)], label=False)
wire('392', [(285, 67), (285, 72)], label=False); earth(285, 72)
box(300, 40, 34, 44); txt(317, 90, '146 Ignition control unit', 2.7, 'middle', w='bold')
for t, y in (('31d', 52), ('7', 59), ('15', 66)): dot(300, y); txt(302, y + 1, t, 2.3)
for t, y in (('31', 45), ('16', 66), ('16', 76)): dot(334, y); txt(332, y + 1, t, 2.3, 'end')
wire('393', [(334, 45), (344, 45), (344, 49)], label=False); earth(344, 49); txt(347, 46, '393 SV 1.5', 2.4)
wire('123d', [(206, 54), (206, 112), (296, 112), (296, 66), (300, 66)], 220, 110.5)
wire('121', [(334, 66), (342, 66)], label=False); tag(344, 66, '121 BL 1.5 → coil 5, terminal 1')
wire('284', [(334, 76), (360, 76), (360, 190), (241, 190), (241, 176)], 300, 188.5)

# ---- fuel pump relay, overboost switch, pump and injection parts -------
box(220, 140, 42, 36); txt(241, 159.5, '102', 3.2, 'middle', w='bold'); txt(241, 164.5, 'Fuel pump relay', 2.6, 'middle')
for t, y in (('30', 146), ('15', 156), ('31', 166)): dot(220, y); txt(222, y + 1, t, 2.3)
dot(262, 146); txt(260, 147, '87', 2.3, 'end'); dot(241, 176); txt(241, 174, 'rpm in', 2.2, 'middle')
wire('260', [(220, 146), (198, 146)], label=False); tag(196, 146, '260 GR 1.5 ← fuse 10', anchor='end')
box(160, 151, 20, 10); A('<path d="M163,158 l5,-4 M168,156 h6" stroke="#111" stroke-width=".5"/>')
txt(170, 165, '144 Pressure switch (overboost)', 2.4, 'middle', w='bold')
wire('378', [(180, 156), (220, 156)], 183, 154.3)
wire('377', [(160, 156), (150, 156)], label=False); tag(148, 156, '377 GN/VT 0.75 ← ignition 15 at 58/4', anchor='end')
wire('263', [(220, 166), (212, 166), (212, 170)], label=False); earth(212, 170); txt(198, 172, '263 SV', 2.3)
wire('261', [(270, 146), (300, 146)], 272, 144.3); dot(270, 146)
A('<circle cx="306" cy="146" r="6" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(306, 147.2, 'M', 3, 'middle', w='bold')
txt(306, 137.5, '103 Fuel pump', 2.6, 'middle', w='bold')
wire('262', [(312, 146), (322, 146), (322, 150)], label=False); earth(322, 150)
wire('261a', [(262, 146), (270, 146), (270, 166), (280, 166)], 268.6, 175, rot=-90); dot(280, 166)
wire('265', [(280, 166), (300, 166)], 281, 164.3)
box(300, 158, 40, 16); name(303, 164, '95', 'Aux. air regulator'); txt(303, 169, 'heated; on with the pump', 2.2, fill='#555')
wire('266', [(340, 166), (348, 166), (348, 170)], label=False); earth(348, 170)
box(300, 198, 40, 16); name(303, 204, '96', 'Warm-up regulator'); txt(303, 209, 'heated', 2.2, fill='#555')
wire('267', [(300, 206), (280, 206), (280, 166)], 281.4, 204.5); txt(282.5, 173, '58/2', 2.1, fill='#555')
wire('268', [(340, 206), (348, 206), (348, 210)], label=False); earth(348, 210)
box(300, 232, 40, 16); name(303, 238, '94', 'Cold-start valve'); txt(303, 243, 'fed while cranking', 2.2, fill='#555')
wire('273', [(340, 240), (360, 240)], 341, 238.3)
box(360, 232, 40, 16); name(363, 238, '92', 'Thermo-time switch'); txt(363, 243, 'earths the valve when cold', 2.2, fill='#555')
A('<path d="M380,248 v3" stroke="#111" stroke-width=".6"/>'); earth(380, 251)

# ---- high-speed fuel boost (1979 Turbo only) ------------------------------------
txt(80, 186, 'High-speed fuel boost (1979 Turbo only)', 2.8, w='bold')
txt(80, 190.5, 'Richens the mixture above about 130 km/h (140) or at 62° throttle (137). PDF p. 24, 33, 210.', 2.1, fill='#555')
box(118, 194, 30, 14); txt(133, 199.5, '140', 2.8, 'middle', w='bold'); txt(133, 204, 'Speed transmitter', 2.0, 'middle'); txt(133, 206.6, '(legend: 151)', 1.8, 'middle', fill='#555')
dot(118, 201); txt(119.5, 199.7, '15', 1.9); dot(148, 198); txt(146.5, 197.2, 'W', 1.9, 'end'); dot(133, 208)
wire('380', [(114, 201), (118, 201)], label=False); tag(82, 201, '380 GL 1.0 ← fuse 5')
wire('381', [(133, 208), (133, 211)], label=False); earth(133, 211); txt(137, 215, '381 SV', 2.1)
wire('382', [(148, 198), (204, 198)], 152, 196.5)
box(204, 193, 20, 10); A('<rect x="209" y="195.5" width="10" height="5" fill="none" stroke="#111" stroke-width=".45"/><path d="M209,200.5 l10,-5" stroke="#111" stroke-width=".45"/>')
A('<path d="M224,198 h6 v4" stroke="#111" stroke-width=".6"/>'); earth(230, 202); txt(214, 209, '142 Solenoid valve (E3)', 2.2, 'middle', w='bold')
box(118, 219, 30, 12); txt(133, 224.5, '137', 2.8, 'middle', w='bold'); txt(133, 228.5, 'Throttle switch, 62°', 1.9, 'middle')
dot(118, 225); dot(148, 225)
wire('380a', [(114, 225), (118, 225)], label=False); tag(82, 225, '380a GL 1.0 ← fuse 5')
wire('383', [(148, 225), (160, 225)], 150, 223.5); txt(163, 226, 'ends on the drawing (feeds 142, per the description)', 2.1, fill='#555')

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
tick(x + 48, ly + 22.3); txt(x + 52, ly + 23, 'checked on the car', 2.4)
notes = ['Overboost cut: pressure switch 144 is in the fuel pump relay’s feed (15). If it opens, the relay drops out and the pump stops.',
         'The pump relay also takes an engine-speed signal from 146 (284 BL), which normally stops the pump when the engine isn’t turning.',
         'Relay 89 is called “start inhibitor relay” in the legend, but here its coil is earthed directly, so it works as a start relay: it feeds',
         'the solenoid from the always-live bar, and 87a bypasses the ballast resistor while cranking (ignition chapter, PDF p. 324–325).',
         'Sender cable 390/391 is shielded; the shield is earthed through 392 SV 0.75.',
         'Diagram is not RHD-specific: circuits should match, but harness routing and part positions may differ.',
         '58/n = pin n of the 12-pole connector at grid A4 (pin map in data/connectors.csv).']
for j, n in enumerate(notes): txt(lx + 108, ly + 4.8 + j * 3.9, n, 2.3, fill='#333')
save('ignition.svg')

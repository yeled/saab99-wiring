#!/usr/bin/env python3
"""Render the 1979 Saab 99 Turbo instruments and warning lamps sheet (A3 SVG)."""
from common import *

header('Saab 99 Turbo, model 1979 — Instruments and warning lamps')
def conn(x, y, h, lab, links=None, below=False):
    """In-line connector on horizontal wires: grey block, a through-link with a dot on both edges at each row in links
    (default: y), name centred above it (below=True: under it)."""
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
    for ry in (links or (y,)): inner([(x - 2, ry), (x + 2, ry)]); dot(x - 2, ry); dot(x + 2, ry)
    txt(x, y + h / 2 + 3.1 if below else y - h / 2 - 1.5, lab, 2.1, 'middle', fill='#555')
def lab(c):
    """A cable's label as wire() prints it: number, colour, mm² from wires.csv."""
    r = WIRES[c]; return f"{c.split('#')[0]} {r['colour']} {r['mm2']}"
def mtag(x, y, lines, w, size=2.4, anchor='start'):
    """Destination tag of several lines (common.tag() takes one), boxed as the lighting sheet's two-line tags: centred
    on y, lines 1.36 × size apart. w: from the rendered text."""
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2); x0 = x if anchor == 'start' else x - w
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines): txt(x0 + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
def gauge(x, y, r, t):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".7"/>'); txt(x, y + 1.2, t, 3, 'middle')
def sender(x, y, n, name, s=11, sw=1.5):
    """The manual's sender symbol (44, 45) with its outer top-left at (x, y): a heavy square with one thin diagonal
    from the inner bottom-left to the inner top-right corner, the number centred above the square as printed, our name
    to its right. No terminal circles or names are printed: the earth lead leaves the left wall level with the
    diagonal's foot, left then down to earth; the signal lead drops from the bottom wall near its right end.
    Returns where the signal wire starts."""
    r = lambda v: round(v, 2)
    A(f'<rect x="{r(x + sw / 2)}" y="{r(y + sw / 2)}" width="{r(s - sw)}" height="{r(s - sw)}" fill="#fff" stroke="#111" stroke-width="{sw}"/>'
      f'<path d="M{r(x + sw)},{r(y + s - sw)} L{r(x + s - sw)},{r(y + sw)}" stroke="#111" stroke-width=".4"/>')
    lamp_earth(x, r(y + s - sw), dx=-6)
    txt(r(x + s / 2), y - 2.2, n, 2.6, 'middle', w='bold')   # two elements: cairosvg misplaces a bold tspan in centred text
    txt(r(x + s / 2 + len(n) * .72 + .75), y - 2.2, name, 2.6)   # half the bold number (.556 em per digit) plus a space
    return r(x + s - sw - .2), r(y + s - .1)

# ---- combination instrument 47 --------------------------------------------
# Inside as the 1979 book prints it (book photo P8-47, scan p.407 at x 5800-6390, y 1560-1945): a + rail from 2 (182)
# feeds both gauges and the oil, low-fuel, brake and charge lamps, each lamp between the rail and its own terminal; an
# earth rail to 4 (179) takes the gauges' third leads and the main-beam (7) and indicator (6) lamps. The book prints a
# dot at every join; crossings without one (C° earth lead over the + rail, earth rail over the 11-5 line, earth loop
# over the fuel gauge's + lead) don't join.
def jdot(x, y): A(f'<circle cx="{x}" cy="{y}" r=".55" fill="#111"/>')   # small junction dot inside a part (as wipers)
box(150, 70, 140, 120); txt(150, 66, '47 Combination instrument', 3, w='bold')
T = {'9': (150, 90), '1': (150, 150), '11': (200, 70), '12': (235, 70), '3': (265, 70),
     '7': (170, 190), '5': (200, 190), '6': (235, 190), '2': (260, 190), '4': (271, 190)}
for k, (x, y) in T.items():
    dot(x, y)
    if x == 150: txt(x + 1.8, y - 1.6, k, 2.3)
    elif y == 70: txt(x + 1.8, y + 3.4, k, 2.3)
    else: txt(x + 1.8, y - 1.6, k, 2.3)
PR, ER, EL, LR = 130, 175, 158, 3.5          # + rail, earth rail, earth loop up to the fuel gauge, lamp radius
on_circle = lambda cx, cy, r, x: round(cy + (r * r - (x - cx) ** 2) ** .5, 2)   # lowest point of the circle at x
# gauge faces as printed: C° (temperature) and B (bensin, fuel)
# temperature gauge: sender 9 on the left, + from the bottom, earth from the right side down to the earth rail
gauge(177, 90, 12, 'C°'); inner([(150, 90), (165, 90)]); txt(175, 108, 'temperature', 2.3, 'end')
inner([(177, 102), (177, PR)]); jdot(177, PR)
inner([(189, 90), (193, 90), (193, ER)]); jdot(193, ER)
# fuel gauge: sender 3 on top, + lead from the bottom left through the rail to 2, earth lead from the bottom right to 4
gauge(265, 90, 12, 'B'); inner([(265, 70), (265, 78)]); txt(273, 108, 'fuel gauge', 2.3)
inner([(260, on_circle(265, 90, 12, 260)), (260, 190)]); jdot(260, PR)
inner([(271, on_circle(265, 90, 12, 271)), (271, 190)]); jdot(271, EL)
inner([(177, PR), (260, PR)])                                          # the + rail
# oil (11) and low fuel (12): terminal, lamp, + rail; the 11 line carries on through the brake lamp to 5
for x, cap in ((200, 'oil'), (235, 'low fuel')):
    inner([(x, 70), (x, 90 - LR)]); lamp(x, 90, r=LR); inner([(x, 90 + LR), (x, PR)]); jdot(x, PR); txt(x + 5.5, 91, cap, 2.2)
inner([(200, PR), (200, 142 - LR)]); lamp(200, 142, r=LR); inner([(200, 142 + LR), (200, 190)]); txt(205.5, 143, 'brake', 2.2)
# charge (1): + rail, lamp, then down and left to 1
inner([(177, PR), (177, 142 - LR)]); lamp(177, 142, r=LR); inner([(177, 142 + LR), (177, 150), (150, 150)])
txt(171.5, 143, 'charge', 2.2, 'end')
# earth rail: main-beam lamp (fed from 7), C° earth lead, the loop up to the fuel gauge's earth lead, indicator lamp (fed
# from 6, on the low-fuel lamp's vertical as printed)
lamp(177, ER, r=LR); inner([(177 - LR, ER), (170, ER), (170, 190)]); txt(177, 170, 'main beam', 2.2, 'middle')
inner([(177 + LR, ER), (235 - LR, ER)]); jdot(215, ER); inner([(215, ER), (215, EL), (271, EL)])
lamp(235, ER, r=LR); inner([(235, ER + LR), (235, 190)]); txt(235, 170, 'indicator', 2.2, 'middle')

# ---- senders and feeds on the left -----------------------------------------
# 44 and 45 as the manual prints them (sender symbol, own earth lead); the signal wires keep their old runs at y 50 / 90
name_ = lambda x, y, n, s: txt(x, y, f'<tspan font-weight="bold">{n}</tspan> {s}', 2.6)
sx, sy = sender(40, 35, '44', 'Oil warning switch')
wire('184', [(sx, sy), (sx, 50), (200, 50), (200, 70)], 60, 48.5); conn(110, 50, 7, 'engine connector 58, pin 5')
sx, sy = sender(40, 75, '45', 'Temperature transmitter')
wire('183', [(sx, sy), (sx, 90), (150, 90)], 60, 88.5); conn(110, 90, 7, 'engine connector 58, pin 6')
box(22, 146, 34, 16); name_(25, 155, '2', 'Alternator')   # D+ a quarter down the right wall, as printed (B+ not on this sheet)
wire('195', [(56, 150), (150, 150)], 60, 148.5)
dot(56, 150); tlabel(54.2, 150.6, 'D+', 'end')   # the manual prints D+ left of its circle on the right wall

# ---- fuel sender and tachometer on the right ---------------------------------
box(360, 82, 36, 20); name_(363, 89, '46', 'Fuel level'); txt(363, 93.5, 'transmitter', 2.4)
# 185 and 186 pass tail lamp connector 58 (58 (B11)) rows 5 and 4, 186 the upper as printed, then fuel sender connector
# 57 (57 (B12)), 185 on its left pin, 186 on its right (scan p.407, book photos IMG_4700, IMG_4701)
wire('185', [(360, 88), (330, 88), (330, 60), (265, 60), (265, 70)], 300, 58.5)
wire('186', [(360, 96), (340, 96), (340, 54), (235, 54), (235, 70)], 300, 52.5)
conn(325, 57, 13, 'tail lamp connector 58, rows 4 and 5', links=(54, 60))
conn(345, 92, 16, 'fuel sender connector 57', links=(88, 96), below=True)
# 46's third lead, 190 SV from its right-hand wall (no terminal name printed; its earth), to 1-pole tank earth
# connector 60 (60 (C12)), where the pump's earth 262 joins it; 191 SV 2.5 goes on to earth (all on the ignition sheet)
wire('190', [(396, 92), (402, 92), (402, 113), (399, 113)], label=False)
mtag(397, 113, (f"{lab('190')} → tank earth connector 60 → {lab('191')}", '→ earth, with pump earth 262 (ignition sheet)'),
     w=61, anchor='end')                                    # w from the rendered text
TX, TY = 314, 154   # tachometer centre: left of the fuel sender so 203's and 204's tags fit in full inside the frame
gauge(TX, TY, 12, 'r/min'); txt(TX, TY + 18, '110 Tachometer', 2.6, 'middle', w='bold')
wire('203', [(TX + 12, TY), (TX + 16, TY)], label=False)
tag(TX + 18, TY, '203 BR 0.75 ← heated window switch 116 (climate sheet)', w=65, size=2.4)   # w from the rendered text
# 204 from service outlet 73 pin 5, a lead of its own beside 284a (ignition sheet), through 1-pole connector 60 (60 (B10))
wire('204', [(TX, TY - 12), (TX, TY - 24), (TX + 12, TY - 24)], label=False); conn(TX + 6, TY - 24, 7, 'tachometer connector 60')
tag(TX + 14, TY - 24, f"{lab('204')} ← service outlet 73, pin 5, beside 284a (ignition sheet)", w=75, size=2.4)

# ---- bottom terminals ----------------------------------------------------------
# 179 earths 47 through panel light connector 59 (59 (D11)), 52 SV and hazard switch 25's lamp terminal, which 69 SV
# earths (signals sheet): the only earth printed for this chain
wire('179', [(271, 190), (271, 198)], label=False)
tag(273, 198, f"{lab('179')} → panel light connector 59 (lower left), then 52 → 69 → earth")   # no clean route across the sheet
wire('182', [(260, 190), (260, 206)], label=False)
tag(262, 206, '182 BR/VT 0.75 ← fuse 4, off 85 BR at stalk switch connector 58, pin 5 (wipers sheet)', w=102)   # w from the
wire('71', [(235, 190), (235, 213)], label=False)      # rendered text; 71's must end left of 58's caption (x 304)
tag(237, 213, '71 GN/VT 0.75 ← 23 flasher unit C (signals sheet)', w=61)
wire('27', [(170, 190), (170, 230)], label=False); tag(172, 230, '27 BL/VT 0.75 ← 8 lighting relay 56a (lighting sheet)')

# ---- brake warning lamp: handbrake switch 43 and brake warning switch 42 ----------------------------------------
# As printed (scan p.407; book photos P8, IMG_4706, IMG_4708, IMG_4723): 187 VT from 47:5 enters ignition switch
# connector 58 (58 (B9)) row 7 on its harness side, where 188 VT splits: one 188 leaves the switch side for handbrake
# switch 43, whose bottom terminal goes to an earth with no cable number; the other leaves the harness side (187's) for
# brake warning switch 42, whose bottom terminal takes 192 SV to earth joint 158. 381 SV (speed transmitter 140's
# earth) lands on 42's lower-left corner on a short diagonal, not on a terminal. Both switches printed open: 43's blade
# hangs from its top contact, 42's rises from its bottom one (the mirror image), like reversing light switch 31.
# Harness side left here, so 42 sits under 187's run and 43 right of the connector. The print brings 187 in on the
# diagonal and takes 188#42 out straight; here 188#42 takes the diagonal, so 42 sits under the connector with no crossing.
Y187, X58 = 219, 320                        # 187's run; the connector (row 7)
X42, T42, X43, T43, SW, SH = 314, 228, 368, 224, 10, 13   # switch centres, box tops; box width and height
wire('187', [(200, 190), (200, Y187), (X58 - 2, Y187)], 205, Y187 - 1.5)
wire('188', [(X58 + 2, Y187), (X43, Y187), (X43, T43)], 341, Y187 - 1.5)
wire('188#42', [(X58 - 2, Y187), (X42, Y187 + 4), (X42, T42)], 292.5, T42 - 1.5)   # label left of its short drop, clear of 42's box
wire('192', [(X42, T42 + SH), (X42, 245), (306, 245)], label=False)   # tag clear of 42's lower-left corner, where 381 lands
tag(306, 245, f"{lab('192')} → earth joint 158 (power sheet)", anchor='end', size=2.4)
wire('381', [(302, 237.5), (305.5, 237.5), (X42 - SW / 2, T42 + SH)], label=False)
tag(302, 237.5, f"{lab('381')} ← speed transmitter 140, -31 (ignition sheet)", anchor='end', size=2.4)
conn(X58, Y187, 7, 'ignition switch connector 58, row 7')
def portrait_switch(x, top, n, name, up=False):
    """Switch as printed: a portrait box, an open circle inside the top and the bottom border, a blade from one of them
    towards the other, open. up=False: hangs from the top circle to the right wall near the bottom (43, as 31);
    up=True: rises from the bottom circle to the left wall near the top (42)."""
    bot = top + SH
    box(x - SW / 2, top, SW, SH)
    inner([(x, top), (x, top + 1.7)]); contact(x, top + 2.5); contact(x, bot - 2.5); inner([(x, bot - 1.7), (x, bot)])
    if up: blade(x - .24, bot - 3.16, x - 3.3, top + 3.6)
    else: blade(x + .24, top + 3.16, x + 3.3, bot - 3.6)
    dot(x, top); dot(x, bot)
    name_(x + SW / 2 + 3, top + SH / 2 + 1, n, name)
portrait_switch(X42, T42, '42', 'Brake warning switch', up=True)
portrait_switch(X43, T43, '43', 'Handbrake switch')
earth(X43, T43 + SH)                        # no cable number printed
dot(X58 - 2, Y187)                          # again, on top of 188's diagonal

# ---- panel lighting: rheostat 16, panel light connector 59 (59 (D11)), lamps 17, 18, 19 -------------------------
# As the 1979 book prints it (scan p.407 x 6650-7010, y 1930-2800; book photos IMG_4708, IMG_4701): 50 GN from fuse 2
# (off 44 GN at tail lamp connector 58 row 1, lighting sheet) through rheostat 16 and 51 GN to 59's GN pin. Every lamp
# sits between a GN (feed) side and an SV (earth) side; the SV pin returns through 52 SV to hazard switch 25's lamp
# terminal, which 69 SV earths (signals sheet), with 47's 179. 59 has no pin numbers: two upright pins, a dot at each end.
XF, Y16 = 108, 175                      # feed column (50, 16, 51, 59's GN pin); rheostat top
XP, YT, YB = XF - 6, 194.5, 199.5       # 59's SV pin; top and bottom dots
XS, XG, XLOOP = 131, 138, 144           # SV and GN rails (the 18s' and 19's left and right edges); 61's loop
LX, LR, R17 = 134.5, 3.5, 3             # lamp centre x and radius on the rails; the 17s' radius (pin pitch / 2)
Y18U, Y18L, Y19 = 204.5, 223, 242
Y17, X17L, X17R = Y18L + R17, XF - R17, 118    # the right 17's top touches 62 (y Y18L), its bottom 61
def rheostat(x, y, w=3.2, h=9):
    """Rheostat as printed: an upright box crossed by a straight arrow from lower left to upper right, head outside the
    top-right corner. Returns its top and bottom lead ends."""
    A(f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="#111" stroke-width=".7"/>')
    x0, y0, x1, y1 = x - w / 2 - 1.6, y + h - 1.2, x + w / 2 + 1.4, y + 1.2
    A(f'<path d="M{x0},{y0} L{x1},{y1}" stroke="#111" stroke-width=".4"/>')
    A(f'<path d="M{x1 + .6},{round(y1 - .9, 2)} L{round(x1 - 1.3, 2)},{round(y1 + .2, 2)} L{round(x1 - .2, 2)},{round(y1 + 1.4, 2)} Z" fill="#111"/>')
    return (x, y), (x, y + h)
# feed: fuse 2 → 50 → 16 → 51 → 59
wire('50', [(XF - 3, 170), (XF, 170), (XF, Y16)], label=False)
mtag(XF - 3, 170, (f"{lab('50')} ← fuse 2 (right park, tail, plate), off 44 GN", 'at tail lamp connector 58 (lighting sheet)'),
     w=62, anchor='end')
(t16, b16) = rheostat(XF, Y16)
txt(XF + 4, Y16 + 5.6, '<tspan font-weight="bold">16</tspan> Rheostat (dimmer)', 2.6)
wire('51', [b16, (XF, YT)], XF + 1.8, 190.5)
# 59's leads: SV pin 179 (from 47:4) and 52 (to 25) on top, 54 and 56 below; GN pin 51 on top, 53 and 55 below
wire('179', [(XP, YT), (XP, 184.5), (XP - 3, 184.5)], label=False)
tag(XP - 3, 184.5, f"{lab('179')} ← 47 terminal 4 (above)", anchor='end', size=2.4)
wire('52', [(XP, YT), (XP - 7, YT)], label=False)
mtag(XP - 7, YT + 1.2, (f"{lab('52')} → hazard switch 25’s lamp terminal", f"→ 69 {WIRES['69']['colour']} {WIRES['69']['mm2']} → earth (signals sheet)"),
     w=55, anchor='end')
wire('54', [(XP, YB), (XP, Y17)], XP - 1.2, Y17 - 5, rot=-90)
wire('53', [(XF, YB), (XF, Y17)], XF + 3.2, Y17 - 4, rot=-90)
wire('55', [(XF, YB), (XG, YB), (XG, Y18U)], XF + 6, YB - 1.4)
wire('56', [(X17L, YB + 1.5), (X17L, Y18U), (XS, Y18U)], XF + 6, Y18U + 3.6)
# the connector over the wire ends: box, two upright pins with a dot at each end; 56's pin is hidden in the book's frame
A(f'<rect x="{XP - 3}" y="{YT - 2}" width="{XF - XP + 6}" height="{YB - YT + 4}" fill="#ddd" stroke="#111" stroke-width=".6"/>')
for x in (XP, XF): inner([(x, YT), (x, YB)]); jdot(x, YT); jdot(x, YB)
inner([(XP, YB), (X17L, YB + 1.5)], grey=True)           # 56 SV: probably the SV pin (join hidden in the frame; check D17)
txt(XF + 4.5, YT - 0.2, '<tspan font-weight="bold">59</tspan> panel light connector', 2.2, fill='#555')
# lamps: 18, 18 and 19 on the rails; 17 left between 59's pin leads, 17 right between 62 (top) and 61 (bottom)
wire('57', [(XG, Y18U), (XG, Y18L)], XG + 1.5, (Y18U + Y18L) / 2 + 1)
wire('58', [(XS, Y18U), (XS, Y18L)], XS - 17.7, (Y18U + Y18L) / 2 + 1)
wire('59', [(XG, Y18L), (XG, Y19)], XG + 1.5, (Y18L + Y19) / 2 + 3.5)
wire('60', [(XS, Y18L), (XS, Y19)], XS - 17.7, (Y18L + Y19) / 2 + 3.5)
wire('62', [(XS, Y18L), (X17R, Y18L)], X17R - 4, Y18L - 1.4)
wire('61', [(X17R, Y17 + R17), (XLOOP, Y17 + R17), (XLOOP, Y18L), (XG, Y18L)], XLOOP + 1.5, Y17 + R17 + 1)
for y in (Y18U, Y18L, Y19): lamp(LX, y, r=LR)
for x in (X17L, X17R): lamp(x, Y17, r=R17)
txt(XLOOP + 2, Y18U + 1, '18', 2.8, w='bold'); txt(XLOOP + 2, Y18L - 2.5, '18', 2.8, w='bold'); txt(XG + 2, Y19 + 2.5, '19', 2.8, w='bold')
txt((X17L + X17R) / 2, Y17 + R17 + 4, '17', 2.8, 'middle', w='bold')
for j, s in enumerate(['<tspan font-weight="bold">Panel lighting</tspan> (sidelights on; dimmed by 16)',
                       '<tspan font-weight="bold">17</tspan> Switch lights (two; which switches: check D18)',
                       '<tspan font-weight="bold">18</tspan> Instrument panel light (two)',
                       '<tspan font-weight="bold">19</tspan> Glove compartment and heater control lights',
                       '(drawn as one lamp; one bulb or two: check D18)']):
    txt(20, 210 + j * 3.6, s, 2.4)


# ---- legend and notes ------------------------------------------------------------
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
notes = ['Inside 47 (its own terminal numbers): a + rail from 2 (182) feeds both gauges and the oil (11), low-fuel (12), brake (5) '
         'and charge (1) lamps; an earth rail to 4 (179) takes the gauges’ third leads and the main-beam (7) and indicator (6) lamps.',
         'Oil and temperature wires pass engine connector 58, pins 5 and 6 (our own count, top to bottom; check E1); the fuel sender wires pass '
         'tail lamp connector 58 (rows 4 and 5) and fuel sender connector 57 (3-pole).',
         'Charge lamp: 195 RD 0.75 from alternator D+. Main beam: 27 BL/VT from lighting relay 8. Indicator: 71 GN/VT from flasher 23. '
         'Brake: 187 VT, then 188 VT to handbrake switch 43 and brake warning switch 42; either earths it.',
         'Supply: 182 BR/VT from fuse 4, branching off the wiper feed 85 BR at stalk switch connector 58. Tachometer: signal 204 GL from '
         'service outlet 73 pin 5 (beside 284a), through tachometer connector 60; supply probably 203 from heated window switch 116.',
         'Earth: 47’s 4 (179 SV) goes through panel light connector 59 and 52 SV to hazard switch 25’s lamp terminal, which 69 SV earths '
         '(signals sheet); the panel lamps (lower left) earth the same way.',
         'Fuel level transmitter 46: its third lead, 190 SV (no terminal name printed), is its earth. It meets the pump’s earth 262 at tank earth connector 60 '
         'and goes on as 191 SV 2.5 to earth, probably near the tank.',
         '44 and 45 are drawn with the sender symbol (heavy square with a diagonal, not a winding), each with its own earth lead '
         '(no cable number). 44 probably earths the oil lamp at low oil pressure; '
         '45 is probably a resistance that falls as the coolant warms.',
         'Not RHD-specific: circuits should match the car, but harness routing and part positions may differ.']
for j, n in enumerate(notes): txt(lx + 108, ly + 5.6 + j * 4.1, n, 2.35, fill='#333')   # 8 lines: 4.1 pitch fits the box
save('instruments.svg')

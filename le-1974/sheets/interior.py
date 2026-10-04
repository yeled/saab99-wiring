#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE interior lights and seat heating sheet (A3 SVG)."""
from common import *

header('Saab 99 LE, model 1974 — Interior lights and seat heating')


# ---- local helpers (the Turbo interior/instruments sheets' idioms) -----------------------------------------------
def lead(pts):
    """A lead the manual prints without a cable number (inside the element, the earths of 50, 54 and 56): plain black."""
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".6" stroke-linejoin="round"/>')
def jdot(x, y):
    """Junction inside a part: smaller than a terminal dot."""
    A(f'<circle cx="{x}" cy="{y}" r=".6" fill="#111"/>')
# Helvetica advance widths (1/1000 em), to centre or right-align a name with a bold number and to size tags:
# cairosvg misplaces a bold tspan in text that isn't start-anchored, so name() works out the start itself
_W = dict(zip('abcdefghijklmnopqrstuvwxyz', (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
                                             556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500)))
_W.update(dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
                                                 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611))))
_W.update({' ': 278, ',': 278, '.': 278, '’': 222, '(': 333, ')': 333, '/': 278, '-': 333, ':': 278, ';': 278,
           '←': 1000, '→': 1000, '°': 400})
def tw(s, size, bold=False):
    return sum(556 if ch.isdigit() else _W.get(ch, 556) * (1.06 if bold else 1) for ch in s) / 1000 * size
def name(x, y, n, s, anchor='start', size=2.6):
    """Component number (bold) and name, as the other sheets print them."""
    w = tw(n, size, True) + tw(' ' + s, size)
    x0 = x if anchor == 'start' else x - w / 2 if anchor == 'middle' else x - w
    txt(round(x0, 2), y, f'<tspan font-weight="bold">{n}</tspan> {s}', size)
def note(x, y, s, anchor='start'):
    txt(x, y, s, 2.2, anchor, fill='#555')
def tagw(x, y, text, anchor='start', size=2.6):
    """common.tag() with its width from the Helvetica table, so the box fits the text."""
    return tag(x, y, text, w=round(tw(text, size) + 3, 2), anchor=anchor, size=size)
def mtag(x, y, lines, anchor='start', size=2.6):
    """Destination tag of several lines (common.tag() takes one), boxed as the Turbo's two-line tags: centred on y,
    lines 1.36 × size apart. Returns the box's left and right x."""
    w = round(max(tw(s, size) for s in lines) + 3, 2)
    ls = round(1.36 * size, 2); h = round(len(lines) * ls + 1.8, 2); x0 = x if anchor == 'start' else x - w
    A(f'<rect x="{x0}" y="{round(y - h / 2, 2)}" width="{w}" height="{h}" rx="1" fill="#fff" stroke="#444" stroke-width=".4"/>')
    for i, s in enumerate(lines): txt(x0 + 1.5, round(y - (len(lines) - 1) * ls / 2 + i * ls + .36 * size, 2), s, size)
    return x0, x0 + w

# Connectors: small grey pin blocks (fill #ddd) filled first, the wires run to the pin dots on their faces, then the
# outline, the pins and their dots go on top (blocks_on_top, after every wire).
BLOCKS = []
def conn(x, y, h=6):
    """One-pin connector on a horizontal run: 4 mm grey block centred on (x, y), dots on both faces. Returns them."""
    A(f'<rect x="{x - 2}" y="{y - h / 2}" width="4" height="{h}" fill="#ddd"/>')
    BLOCKS.append(((x - 2, y - h / 2, 4, h), [((x - 2, y), (x + 2, y))]))
    return x - 2, x + 2
def conn_v(x, y, h=6):
    """One-pin connector on a vertical run: 4 mm grey block centred on (x, y), dots on its top and bottom faces."""
    A(f'<rect x="{x - h / 2}" y="{y - 2}" width="{h}" height="4" fill="#ddd"/>')
    BLOCKS.append(((x - h / 2, y - 2, h, 4), [((x, y - 2), (x, y + 2))]))
    return y - 2, y + 2
def conn_pins(x0, y0, w, h, xs):
    """Connector with upright pins at xs (wiring side on top, part side below)."""
    A(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#ddd"/>')
    BLOCKS.append(((x0, y0, w, h), [((x, y0), (x, y0 + h)) for x in xs]))
def blocks_on_top():
    for (x0, y0, w, h), pins in BLOCKS:
        A(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#111" stroke-width=".5"/>')
        for a, b in pins: inner([a, b]); dot(*a); dot(*b)

def push_contact(xc, y, r=5):
    """Plunger contact (door contact 54, trunk light contact 56) as printed: a circle with two fixed contacts and a
    bridge whose ends rest on both (closed, as printed), the plunger standing on the bridge. Leads enter on the
    left and right of the circle; returns those two terminal points."""
    A(f'<circle cx="{xc}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    a, b = round(xc - 2.3, 2), round(xc + 2.3, 2)
    inner([(xc - r, y), (a - .8, y)]); inner([(b + .8, y), (xc + r, y)]); contact(a, y); contact(b, y)
    A(f'<path d="M{a},{y - .8} L{a},{y - 1.7} L{b},{y - 1.7} L{b},{y - .8}" fill="none" stroke="#111" stroke-width=".75" '
      f'stroke-linejoin="round"/>')
    A(f'<path d="M{xc},{y - 1.7} V{y - 3.7} M{xc - 1.1},{y - 3.7} H{xc + 1.1}" stroke="#111" stroke-width=".45"/>')
    return (xc - r, y), (xc + r, y)

def meander(x, y, w, n=4, d=4, m=2.2):
    """Heating element as the manual prints it: n square humps hanging below the line y, from x to x + w, with a
    flat m at each end (clear of the thermostat box and the leads)."""
    s = (w - 2 * m) / (2 * n - 1); pts = [(x, y)]
    for k in range(n):
        a, b = round(x + m + 2 * k * s, 2), round(x + m + (2 * k + 1) * s, 2)
        pts += [(a, y), (a, y + d), (b, y + d), (b, y)]
    pts.append((x + w, y))
    A(f'<path d="{path(pts)}" fill="none" stroke="#111" stroke-width=".45" stroke-linejoin="round"/>')


# ---- seat heating ------------------------------------------------------------------------------------------------
# p.327 (S 4002): fuse 11 → 93 GL 1.0 → 58 (D7) → 93e GL 1.0 → 60 (E7) → 93f GL 0.75 → 59 (E8) pin 1 (top dot);
# pin 2's top dot → 94 SV 1.0 → the hatched earth below switch 53 (m7_94_53.png; P8). The bottom dots of 59 lead out to
# the two ends of element 64: meander, thermostat box (C° above, contact below), meander (b_seat/b_thermo crops of
# p.327; the same artwork on p.325 and p.317). The thermostat's blade rises from the left contact and its hooked tip
# comes down onto the right contact in all three prints: drawn closed. 59 is drawn with upright pins as printed.
txt(18, 40, 'Seat heating', 3.4, w='bold')
Y1 = 58                                          # the feed's run
TE = tagw(14, Y1, f"93 GL 1.0 ← fuse 11 (power sheet)")
L58s, R58s = conn(70, Y1); note(70, Y1 + 7.4, '58 seat heating', 'middle')
L60s, R60s = conn(94, Y1); note(94, Y1 + 7.4, '60 seat feed', 'middle')
P1, P2, T59 = 118, 124, Y1 + 4                   # 59's pins and its top face
conn_pins(P1 - 3, T59, P2 - P1 + 6, 8, (P1, P2)); note(P1 - 4.5, T59 + 7.2, '59 seat heater', 'end')
wire('93', [(TE, Y1), (L58s, Y1)], label=False)
wire('93e', [(R58s, Y1), (L60s, Y1)], R58s + 1.6, Y1 - 1.5)
wire('93f', [(R60s, Y1), (P1, Y1), (P1, T59)], R60s + 1.6, Y1 - 1.5)
XE94, YE94 = 144, 80
wire('94', [(P2, T59), (P2, 50), (XE94, 50), (XE94, YE94)], XE94 - 1.4, 75, rot=-90); earth(XE94, YE94)
note(XE94, YE94 + 11, 'same earth point as', 'middle'); note(XE94, YE94 + 14.4, '120 SV 0.75 from switch 53', 'middle')
# element 64: the leads from 59's bottom dots, the left one over the element to its far end
E, XA, XB = 88, 70, P2                           # element line; its left and right ends
C0, C1 = 90, 104                                 # thermostat box
lead([(P1, T59 + 8), (P1, 76), (XA, 76), (XA, E)]); lead([(P2, T59 + 8), (P2, E)])
meander(XA, E, C0 - XA); meander(C1, E, XB - C1)
A(f'<rect x="{C0}" y="{E - 9}" width="{C1 - C0}" height="15" fill="#fff" stroke="#111" stroke-width=".6"/>')
A(f'<path d="M{C0},{E - 4} H{C1}" stroke="#111" stroke-width=".4"/>')
txt((C0 + C1) / 2, E - 5.3, 'C°', 2.4, 'middle')
ca, cb = C0 + 3, C1 - 3                          # the thermostat's contacts: blade on ca, its hooked tip on cb
inner([(C0, E), (ca - .8, E)]); inner([(cb + .8, E), (C1, E)]); contact(ca, E); contact(cb, E)
A(f'<path d="M{ca + .6},{E - .5} L{cb - .7},{E - 2.4} L{cb - .57},{E - .57}" fill="none" stroke="#111" '
  f'stroke-width=".75" stroke-linecap="round" stroke-linejoin="round"/>')
name((XA + XB) / 2, E + 12, '64', 'Seat heating element with thermostat', 'middle')
for j, s_ in enumerate(('Fed with the ignition on (fuse 11). The thermostat is inside the',
                        'element, drawn closed (it is closed while cold, probably).',
                        'Which seat or seats it heats, and whether there is a switch: check I2.')):
    note(18, 109 + j * 3.4, s_)


# ---- interior lights -----------------------------------------------------------------------------------------------
# p.327 with book photo P8: fuse 7 → 64 GL 1.0 → 58 (D11) left pin (80 BL leaves the same pin for the lighter) → 65 GL
# 0.75 → the corner over ignition switch light 52 → 65e GL 0.75 → dome light 50's lamp. 65f SV (forward dome light 51)
# and 121 GR (trunk light 55) land on the same lamp terminal. The lamps return to 50's switch pivot (66e BL from 52,
# 66f SV from 51); the trunk light returns through its own contact 56 (123 BL). 50's lever sits between the upper
# contact (earth) and the lower contact (the door line), touching neither: off. The door line: 66be and 66ae to two
# door contacts, 66g → 60 (D12) → 66 → switch 53's pivot, which earths it through 120 SV when closed and carries it on
# as 122 SV → 58 (E13) → 122b and 122a to the other two door contacts. 54 and 56 are printed closed (plunger out).
XI = 160
txt(XI, 40, 'Interior lights', 3.4, w='bold')
note(XI, 46, 'Fed from fuse 7 (always live). Lamps 50, 51 and 52 return through dome light 50’s switch: on (to earth), off (as drawn) or door (to the door line).')
note(XI, 49.4, 'Each door contact 54 and switch 53 earth that door line in parallel: an open door, or 53 closed, lights them while 50’s switch is at door.')

Ym = 115                                         # dome light 50's centre line
X50, W50, H50 = 270, 48, 22
R50 = H50 / 2
CL, CR = X50 + R50, X50 + W50 - R50              # centres of the housing's round ends
wall_top = lambda x: round(Ym - (R50 ** 2 - (CL - x) ** 2) ** .5, 3) if x < CL else Ym - R50
wall_right = lambda y: round(CR + (R50 ** 2 - (y - Ym) ** 2) ** .5, 3)
wall_bottom = lambda x: round(Ym + (R50 ** 2 - (x - CR) ** 2) ** .5, 3) if x > CR else Ym + R50
TLx, LX50, PX = 284.5, 290, 299                  # lamp terminal, lamp centre, switch pivot
KX = 309                                         # the switch's fixed contacts
RL = 3.5
Y21, Y121 = wall_top(274), Ym - R50              # where 121 and 65f/66f meet the wall

# the feed: 64 GL from fuse 7 into 58 interior feed; 80 BL on to the lighter from the same pin
X58f, Y58f = 214, 78
L58f, R58f = conn(X58f, Y58f); note(X58f, Y58f + 7.4, '58 interior feed', 'middle')
TE64 = tagw(XI, Y58f, '64 GL 1.0 ← fuse 7 (power sheet)')
wire('64', [(TE64, Y58f), (L58f, Y58f)], label=False)
wire('80', [(L58f, Y58f), (L58f - 3, Y58f - 3), (L58f - 3, 66), (L58f - 7, 66)], label=False)
mtag(L58f - 7, 66, ('80 BL 1.0 → cigarette lighter 48', '(instruments sheet)'), anchor='end')
# 52 hangs from the corner of 65; 65e tees off there to dome light 50
X52 = 240
wire('65', [(R58f, Y58f), (X52, Y58f), (X52, Ym + 7 - RL)], R58f + 2.5, Y58f - 1.5)
wire('65e', [(X52, Ym), (X50, Ym)], X52 + 4, Ym - 1.5)
lamp(X52, Ym + 7, r=RL); name(X52 - 5.5, Ym + 8, '52', 'Ignition switch light', 'end')
wire('66e', [(X52, Ym + 7 + RL), (X52, 132), (PX, 132), (PX, Ym + R50)], X52 + 10, 130.5)

# 55 and 51 above 50, feeding its lamp terminal; 55's return through contact 56
Y55, Y51 = 64, 80
X55, X51 = 282, 292
lamp(X55, Y55, r=RL); name(X55, Y55 - 5.5, '55', 'Trunk light', 'middle')
wire('121', [(X55 - RL, Y55), (274, Y55), (274, Y21)], 272.6, 100, rot=-90)
X56 = 340
p56a, p56b = push_contact(X56, Y55)
wire('123', [(X55 + RL, Y55), p56a], X55 + 8, Y55 - 1.5)
lead([p56b, (X56 + 12, Y55)]); earth(X56 + 12, Y55)
name(X56, Y55 - 7.5, '56', 'Trunk light contact', 'middle')
note(X56 + 16, Y55 + 1.1, 'at the left hinge; switches 55 on its earth side')
lamp(X51, Y51, r=RL); name(PX + 4, Y51 + 1, '51', 'Dome light, forward (at the mirror)')
wire('65f', [(X51 - RL, Y51), (TLx, Y51), (TLx, Y121)], TLx - 1.4, 102, rot=-90)
wire('66f', [(X51 + RL, Y51), (PX, Y51), (PX, Y121)], PX - 1.4, 102, rot=-90)

# 50: pill-shaped housing; lamp on the left, the switch pivot in the middle, the lever between the earth contact (up)
# and the door contact (down), touching neither, as printed (P8)
A(f'<rect x="{X50}" y="{Ym - R50}" width="{W50}" height="{H50}" rx="{R50}" fill="#fdfdfd" stroke="#111" stroke-width=".8"/>')
inner([(X50, Ym), (LX50 - RL, Ym)]); inner([(274, Y21), (TLx, Ym)]); inner([(TLx, Y121), (TLx, Ym)]); jdot(TLx, Ym)
lamp(LX50, Ym, r=RL)
inner([(LX50 + RL, Ym), (PX - .8, Ym)]); contact(PX, Ym)
inner([(PX, Y121), (PX, Ym - .8)]); inner([(PX, Ym + .8), (PX, Ym + R50)])
blade(PX + .7, Ym, KX - .4, Ym)
KU, KD = Ym - 6, Ym + 6                          # earth contact, door contact
contact(KX, KU); contact(KX, KD)
XR6 = wall_right(KU)                             # the right wall at the contacts' heights (same for both)
inner([(KX + .8, KU), (XR6, KU)]); inner([(KX + .8, KD), (XR6, KD)])
YD = wall_bottom(KX)                             # the door node on the bottom wall, under the door contact
inner([(KX, KD + .8), (KX, YD)])
lead([(XR6, KU), (326, KU)]); earth(326, KU)
name(322, 97, '50', 'Dome light, middle')
note(322, 100.4, 'switch: on (earth) / off (as drawn) / door')

# the door line: two door contacts straight off 50's door node, the other two beyond switch 53's pivot
X54, YS = 386, (121, 141, 166, 191)             # door contacts: centre x, and their rows
XL54 = X54 - 5
wire('66be', [(XR6, KD), (XL54, YS[0])], 322, KD - 1.5)
wire('66ae', [(KX, YD), (316, YD + 7), (316, YS[1]), (XL54, YS[1])], 322, YS[1] - 1.5)
T60, B60 = conn_v(KX, 151); note(KX - 4.5, 152.2, '60 interior switch', 'end')
Y53 = 180
wire('66g', [(KX, YD), (KX, T60)], KX - 1.4, 147, rot=-90)
wire('66', [(KX, B60), (KX, Y53)], KX - 1.4, 172.5, rot=-90)
# 53: a circle; the pivot on its right edge takes 66 and 122, the fixed contact low on the left goes to earth on
# 120 SV; the lever rises from the pivot up-left, clear of the fixed contact (open, as printed: P8)
X53c, R53 = KX - 6, 6
A(f'<circle cx="{X53c}" cy="{Y53}" r="{R53}" fill="#fff" stroke="#111" stroke-width=".6"/>')
contact(KX - 2.2, Y53); inner([(KX - 1.4, Y53), (KX, Y53)])
FX, FY = X53c - 4, Y53 + 1.5                     # the fixed contact
contact(FX, FY); YB53 = round(Y53 + (R53 ** 2 - 16) ** .5, 3); inner([(FX, FY + .8), (FX, YB53)])
blade(KX - 2.9, Y53 - .4, FX + .6, Y53 - 3.6)
name(X53c - 7.5, Y53 - 5, '53', 'Interior lighting switch', 'end')
wire('120', [(FX, YB53), (FX, 205)], FX - 1.4, 203, rot=-90); earth(FX, 205)
note(FX, 216, 'same earth point as 94 SV 1.0', 'middle'); note(FX, 219.4, '(seat heating)', 'middle')
L58d, R58d = conn(338, Y53); note(334, Y53 + 6.8, '58 door contacts', 'end')
wire('122', [(KX, Y53), (L58d, Y53)], KX + 3, Y53 - 1.5)
wire('122b', [(R58d, Y53), (R58d + 3, Y53 - 3), (R58d + 3, YS[2]), (XL54, YS[2])], R58d + 8, YS[2] - 1.5)
wire('122a', [(R58d, Y53), (R58d + 3, Y53 + 3), (R58d + 3, YS[3]), (XL54, YS[3])], R58d + 8, YS[3] - 1.5)
for y_ in YS:
    _, e = push_contact(X54, y_); lead([e, (X54 + 11, y_)]); earth(X54 + 11, y_)
name(X54 + 3, YS[0] - 9, '54', 'Door contacts', 'middle')
note(X54 + 3, YS[3] + 13, 'which two are the', 'middle'); note(X54 + 3, YS[3] + 16.4, 'rear doors: check I1', 'middle')

# terminal and joint dots, after the wires
for p in ((X50, Ym), (274, Y21), (TLx, Y121), (PX, Y121), (PX, Ym + R50), (XR6, KU), (XR6, KD), (KX, YD),
          (X52, Ym), (KX, Y53), (FX, YB53), p56a, p56b):
    dot(*p)
for y_ in YS: dot(XL54, y_); dot(X54 + 5, y_)
blocks_on_top()


# ---- legend --------------------------------------------------------------------------------------------------------
LH = 34.5 if PROBABLE[0] else 32                 # sized to its content (the notes end at ly + 28.6), bottom kept at 284
lx, ly = 12, 284 - LH
box(lx, ly, 396, LH, fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 4
size_legend(x, ly + 18)                          # line widths, under the colours
y = ly + 24                                      # status row: traced, then the samples this sheet uses
A(f'<path d="M{x},{y - 1} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, y, 'traced (cable no. read)', 2.4)
sx = x + 48
if DASHED[0]:
    A(f'<path d="M{sx},{y - 1} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(sx + 11, y, 'not traced yet', 2.4); sx += 36
if STUB[0]:
    A(f'<path d="M{sx},{y - 1} h7" stroke="#222" stroke-width=".8"/><circle cx="{sx + 8.3}" cy="{y - 1}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    txt(sx + 11, y, 'ends on diagram', 2.4); sx += 36
if TICKED[0]: tick(sx, y - .7); txt(sx + 4, y, 'checked on the car', 2.4)
probable_legend(x, y + 6)
notes = ['The door line is one line: 66be, 66ae and 66g SV 0.75 from dome light 50; 66 and 122 SV 0.75 on switch 53’s pivot; 122b and 122a SV 0.75 beyond 58 door contacts.',
         'Door contacts 54 and trunk light contact 56 are drawn closed: plunger out, with the door or lid open (probably).',
         'Which two door contacts are the rear doors is still to be checked (check I1).',
         '64 GL 1.0 (fuse 7 to the interior lights) is a cable, not part 64, the seat heating element.',
         'Seat heating: its return 94 SV 1.0 is drawn to an earth of its own here, but it shares one earth point with 120 SV 0.75 from switch 53.',
         'Thin black lines without a label: leads with no cable number.']
for j, n in enumerate(notes): txt(lx + 108, round(ly + 5.6 + j * 4.6, 2), n, 2.35, fill='#333')
save('interior.svg')

#!/usr/bin/env python3
"""Render the 1974 Saab 99 LE ignition and starting sheet (A3 SVG), with the automatic's start inhibitor.

Sources (code comments only; nothing of this is printed): base diagram p.327 (371-23, S 4002) for the coil, ballast,
distributor, starter and the starter line; the automatic detail p.348 (371-44, S 3981; book photo P7) for relay 89,
switch 90, lamp 91 and their cables; book photo P3 for the starter's terminal marks. Facts about the parts' insides:
memory/internals-facts-p6-p8.md. Positions are ours; the elements and their rest states are the print's."""
from common import *

header('Saab 99 LE, model 1974 — Ignition and starting')


def ht(pts): A(f'<path d="{path(pts)}" fill="none" stroke="#444" stroke-width="1.1" stroke-linejoin="round"/>')
# Helvetica advance widths (1/1000 em; the arrows are Arial's), as the Turbo's interior sheet: tags are sized to their
# text, and a name with a bold number is placed by its start (cairosvg misplaces a bold tspan in text not start-anchored)
_W = dict(zip('abcdefghijklmnopqrstuvwxyz', (556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556,
                                             556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500)))
_W.update(dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
                                                 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611))))
_W.update({' ': 278, ',': 278, '.': 278, '’': 222, '(': 333, ')': 333, '/': 278, '-': 333, ':': 278, ';': 278,
           '+': 584, '←': 1000, '→': 1000})
def tw(s, size, bold=False):
    return sum(556 if ch.isdigit() else _W.get(ch, 556) * (1.06 if bold else 1) for ch in s) / 1000 * size
def name(x, y, n, s, anchor='start', size=2.7):
    """Component number (bold) and name."""
    w = tw(n, size, True) + tw(' ' + s, size)
    x0 = x if anchor == 'start' else x - w / 2 if anchor == 'middle' else x - w
    txt(round(x0, 2), y, f'<tspan font-weight="bold">{n}</tspan> {s}', size)
def ttag(x, y, text, size=2.6):
    """Destination tag (common.tag()) sized to its text."""
    return tag(x, y, text, w=round(tw(text, size) + 3.2, 1), size=size)
def note(x, y, lines, size=2.3, fill='#333', step=3.6, anchor='start'):
    for i, s in enumerate(lines): txt(x, round(y + i * step, 2), s, size, anchor, fill=fill)
def block(x, y, w, h):
    """Connector housing: a small grey pin block (dots on its faces are drawn after the wires)."""
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#ddd" stroke="#111" stroke-width=".5"/>')
def open_end(x, y):
    """The open circle a stub ends in (as wire() draws it), redrawn on top of a connector face."""
    A(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
def earth_lead(pts):
    """Plain lead from a part to its earth symbol (no cable number)."""
    A(f'<path d="{path(pts)}" stroke="#111" stroke-width=".6" fill="none"/>')


# ---- distributor 7 and ignition coil 5 (top left) -----------------------------------------
# p.327 (book photo P3): 7 is a circle with four outer cap circles and a centre post, an earth hatch on its body, the
# LT terminal at the bottom (7 BR/VT to the coil's 1) and the unnumbered HT line from the centre post to the coil's
# rounded end. Nothing else printed inside (the contact breaker points are not drawn by the book either).
DX, DY, DR = 36, 54, 12
A(f'<circle cx="{DX}" cy="{DY}" r="{DR}" fill="#fff" stroke="#111" stroke-width=".8"/>')
for sx in (-1, 1):
    for sy in (-1, 1):
        A(f'<circle cx="{DX + sx * 6}" cy="{DY + sy * 6}" r="1.2" fill="#fff" stroke="#111" stroke-width=".4"/>')
name(DX - 12, 38, '7', 'Distributor')
earth_lead([(DX - DR, DY), (17, DY)]); earth(17, DY)            # the body's earth (printed as a hatch on top)
# coil 5: a box with a rounded end (the HT tower) towards the distributor; 15 upper, 1 lower, as printed (on the
# box's left end in the book; here 15 on the right wall, where 119 arrives, and 1 on the bottom wall)
CX0, CX1, CY0, CY1 = 68, 92, 42, 66
A(f'<path d="M{CX0},{CY0} H{CX1} V{CY1} H{CX0} A12,12 0 0 1 {CX0},{CY0} Z" fill="#fafafa" stroke="#111" stroke-width=".8"/>')
name(58, 38, '5', 'Ignition coil')
tlabel(90.6, 46.65, '15', 'end'); tlabel(84, 64.2, '1', 'middle')
ht([(56, DY), (DX + 1.3, DY)])                                    # HT: tower to the centre post
A(f'<circle cx="{DX}" cy="{DY}" r="1.3" fill="#fff" stroke="#111" stroke-width=".5"/>')   # centre post, over the HT end
wire('7', [(DX, DY + DR), (DX, 74), (84, 74), (84, CY1)], 48, 72.5)

# ---- ballast resistor 6 (top) ------------------------------------------------------------
# P7/P6a: a meander in a box. Left end: 119 (to coil 15) and 119e (from starter 16). Right end, as the factory drew
# it: 118e (from the ignition switch), 181 (to master relay 101, injection detail) and 195g (to switch 90:1, automatic
# detail); on this car the rev counter's brown lead instead (below).
BL, BR, BY = 117, 150, 46                                         # the two end nodes, outside the box
box(121, 42, 25, 8)
A('<path d="M117,46 H124.5 V44 H127 V48 H129.5 V44 H132 V48 H134.5 V44 H137 V48 H139.5 V44 H142 V46 H150" '
  'fill="none" stroke="#111" stroke-width=".4"/>')
name(121, 38, '6', 'Ballast resistor')
wire('119', [(BL, BY), (CX1, BY)], 97.5, 44.5)
wire('119e', [(BL, BY), (BL, 205), (112, 205)], BL - 1.4, 192, rot=-90)
# On the car (check D1; Charlie, 4 Oct 2026; data rev, rev-SV, rev-BR): the aftermarket rev counter (a Faria
# tachometer) sits in series in the coil's feed. 118e, 181 and 195g no longer reach the resistor: they meet the rev
# counter's black lead at a loose joint by the coil (J), and its brown lead is the only lead on the resistor's feed end.
JX, GX, GR_ = 171, 160.5, 5                                       # the joint; the rev counter's centre and radius
wire('118e', [(298, BY), (JX, BY)], 232, 44.5)
ttag(300, BY, '118e GN/VT 1.0 ← ignition switch 20:15, via 58 ign. switch (power sheet)')
wire('181', [(JX, BY), (JX, 32), (JX + 2, 32)], label=False)
ttag(JX + 2, 32, '181 GN/VT 0.75 → master relay 101:86, coil (injection sheet)')
wire('195g', [(JX, BY), (JX, 62), (BR, 62), (BR, 98)], BR - 1.4, 94, rot=-90)
wire('rev-SV', [(JX, BY), (GX + GR_, BY)], label=False)            # black lead: from the joint to the meter
wire('rev-BR', [(GX - GR_, BY), (BR, BY)], label=False)            # brown lead: from the meter back to the resistor
A(f'<circle cx="{GX}" cy="{BY}" r="{GR_}" fill="#fff" stroke="#111" stroke-width=".7"/>')
for k in range(7):                                                  # a gauge face: scale ticks over the top, a needle
    import math
    t = math.radians(200 + k * 140 / 6)
    A(f'<path d="M{GX + 3.6 * math.cos(t):.2f},{BY + 3.6 * math.sin(t):.2f} L{GX + 4.4 * math.cos(t):.2f},'
      f'{BY + 4.4 * math.sin(t):.2f}" stroke="#111" stroke-width=".3"/>')
A(f'<path d="M{GX},{BY} L{GX + 2.4},{BY - 2.4}" stroke="#111" stroke-width=".45"/><circle cx="{GX}" cy="{BY}" r=".5" fill="#111"/>')
dot(JX, BY)                                                         # the joint: four leads meet here
tick(152.6, 43.3); tick(167.6, 43.3)                                # both leads checked on the car
txt(GX, 54.6, 'rev counter', 2.3, 'middle')
note(176, 52.5, ('Rev counter: aftermarket, in the dashboard where the clock was (check D1), wired in series with the coil’s feed.',
                 'The ignition feed 118e, 181 and 195g meet at a joint by the coil; the rev counter’s black lead takes the current',
                 'to the meter and its brown lead brings it back to the resistor, the only lead on that end. If a lead comes off with',
                 'the engine running, it stops; while cranking, 119e still feeds the coil straight from the starter.'),
     size=2.1, fill='#555', step=3.0)

# ---- gear indicator light 91 (top band) ---------------------------------------------------
LX, LY = 258, 32
lamp(LX, LY); name(LX - 9, 25.2, '91', 'Gear indicator light', size=2.5)
earth_lead([(LX - 4.5, LY), (251.5, LY), (251.5, 37)]); earth(251.5, 37)
wire('54bf', [(298, LY), (LX + 4.5, LY)], 273, 30.5)
ttag(300, LY, '54bf GN 0.75 ← ignition switch 20:15 (power sheet)')
txt(LX + 7, 38.6, 'lit with the ignition on', 2.1, fill='#555')

# ---- start inhibitor and reversing light switch 90 ------------------------------------------
# P7: 3 top-left, 1 bottom-left, 4 top-right, 2 bottom-right; 3-1 a straight closed blade, 2-4 a blade pivoted on 2,
# open. Drawn flipped top to bottom: 1 top-left, 3 bottom-left, 2 upper right, 4 lower right (2 and 4 on the right wall
# so 95e and 95f reach the right edge above relay 89). In P: start contact closed, reversing contact open.
SX0, SY0 = 145, 98
box(SX0, SY0, 26, 26)
T1, T3, T2, T4 = (150, 98), (150, 124), (171, 104), (171, 118)
inner([T1, (150, 103.2)]); contact(150, 104); contact(150, 118); inner([(150, 118.8), T3])
blade(150, 104.7, 150, 117.3)                                     # 1-3: closed
inner([T2, (165.8, 104)]); contact(165, 104); contact(165, 118); inner([(165.8, 118), T4])
blade(164.6, 104.6, 161.4, 116.2)                                 # 2-4: pivoted on 2, open
tlabel(151.6, 101.4, '1'); tlabel(151.6, 122.6, '3'); tlabel(169.6, 102.6, '2', 'end'); tlabel(169.6, 116.6, '4', 'end')
name(143, 102.5, '90', 'Start inhibitor', 'end', 2.5)
txt(143, 106.3, 'and reversing', 2.5, 'end'); txt(143, 110.1, 'light switch', 2.5, 'end')   # plain text: 'end' is safe
wire('95e', [(298, 104), T2], 236, 102.5)
ttag(300, 104, '95e VT 1.0 ← fuse 11 (power sheet)')
wire('95f', [T4, (176, 118)], label=False)
ttag(178, 118, '95f VT 1.0 → reversing lights, via 60 inhibitor reversing (signals sheet)')

# ---- 60 inhibitor start and start inhibitor relay 89 -------------------------------------------
P60 = (178, 182)                                                   # its two faces on the 195h / 195f run
wire('195h', [T3, (150, 136), (P60[0], 136)], 153.6, 134.5)
wire('195f', [(P60[1], 136), (244, 136)], 204, 134.5)
# relay 89 (P7): 87 left wall upper with a short link to the fixed contact; 30/51 right wall upper, the blade pivoted
# on it, free end clear of 87 (open); the coil between 85 (left lower) and 86 (right lower). Drawn flipped top to bottom
# (coil on top, contact below) with 87 and 30/51 on the bottom wall, so 84a and 84b drop straight to 57 and nothing
# crosses (the print's 330/84a and 195f/84b crossings go). The print draws no coil-to-blade link; mlink() is ours.
RX0, RY0, RW, RH = 244, 126, 32, 28
box(RX0, RY0, RW, RH)
T85, T86, T87, T30 = (RX0, 136), (RX0 + RW, 136), (252, RY0 + RH), (268, RY0 + RH)
cl, cr, ct, cb = coil(255, 132.5, 10, 7)
inner([T85, cl]); inner([cr, T86])
inner([T87, (252, 148), (255.2, 148)]); contact(256, 148)          # 87: fixed contact, in from its wall lead as printed
inner([T30, (268, 148.8)]); contact(268, 148)                       # 30/51: the blade's pivot
blade(267.3, 148.4, 255, 150.9)                                     # open at rest: tip just past 87's contact, below it
mlink([cb, (260, 149.5)])                                           # onto the blade's top edge (blade y 149.9 at x 260)
tlabel(245.4, 134.6, '85'); tlabel(274.6, 134.6, '86', 'end'); tlabel(250.6, 152.6, '87', 'end'); tlabel(269.4, 152.6, '30/51')
txt(241, 146.2, '89', 3.2, 'end', w='bold'); txt(241, 150.6, 'Start inhibitor relay', 2.5, 'end')
wire('330', [T86, (300, 136), (300, 141)], 277.8, 134.5); earth(300, 141)

# ---- 57 starter line, the starter line and 60 starter signal ---------------------------------
# 57 (A6), two pins (P7: 2x2 dots): pin L 84b on its relay face, 84f + 84h on its car face; pin R 84a | 84e.
KY0, KY1 = 178, 184                                                 # the relay face and the car face
wire('84b', [T87, (252, KY0)], 250.6, 175, rot=-90)
wire('84a', [(268, KY0), T30], 266.6, 175, rot=-90)
wire('84e', [(298, 200), (268, 200), (268, KY1)], 274, 198.5)
ttag(300, 200, '84e GL 1.5 ← ignition switch 20:50, via 58 ign. switch (power sheet)')
# 84h: a thin lead of its own from 84f's pin (P7: 84h and the 84f riser both meet the pin's bottom dot), on a diagonal
# beside the straight 84f, into the right face of the one-pin 60 starter signal; nothing on its left face (stub).
# Drawn before 84f, so the straight lead covers the diagonal's root.
QX0, QX1, QY = 214, 218, 189
wire('84h', [(252, KY1), (247, QY), (QX0, QY)], 228.5, 187.5)
wire('84f', [(252, KY1), (252, 221), (112, 221)], 140, 219.5)
block(247, KY0, 26, KY1 - KY0)
block(P60[0], 133, 4, 6)
txt(275, 182.3, '57 starter line', 2.2, w='bold')
txt(180, 143.2, '60 inhibitor start', 2.2, 'middle', w='bold')
txt(216, 183.4, '60 starter signal', 2.2, 'middle', w='bold')
A(f'<rect x="{QX0}" y="{QY - 3}" width="4" height="6" fill="#ddd" stroke="#111" stroke-width=".5"/>')   # over 84h's run inside
open_end(QX0, QY)                                                    # 84h ends here: nothing drawn beyond the left face
note(211, 188.2, ('probably on to 59 cold start: start signal', '218 GL 0.75 and cold-start valve 231 GL 0.75', '(injection sheet; check E1)'),
     size=2.0, fill='#666', step=2.9, anchor='end')

# ---- starter 4 (bottom left) ------------------------------------------------------------------
# P3/P7: 16 on the right edge (upper), 50 below it, 30 on the bottom; a solid block outside the left wall.
SX, SY, SW, SH = 78, 198, 34, 30
box(SX, SY, SW, SH)
A(f'<rect x="{SX - 2.4}" y="{SY + 13}" width="2.4" height="4" fill="#fff" stroke="#111" stroke-width=".5"/>'
  f'<rect x="{SX - 5.8}" y="{SY + 11}" width="3.4" height="8" rx=".6" fill="#111"/>')
name(SX + 5, SY + 13, '4', 'Starter')
tlabel(110.6, 205.65, '16', 'end'); tlabel(110.6, 221.65, '50', 'end'); tlabel(95, 226.2, '30', 'middle')
note(SX, 233.2, ('30: battery +, alternator, master relay', '(power sheet)'), size=2.1, fill='#555', step=3.0)

# ---- dots on top of the wires -------------------------------------------------------------------
for p in ((DX, DY + DR), (84, CY1), (CX1, BY), (BL, BY), (BR, BY), (112, 205), (112, 221), (95, SY + SH),
          T1, T3, T2, T4, T85, T86, T87, T30, (P60[0], 136), (P60[1], 136),
          (252, KY0), (268, KY0), (252, KY1), (268, KY1), (QX1, QY)):
    dot(*p)

# ---- notes ---------------------------------------------------------------------------------------
def wrap(s, maxw, size=2.3):
    """Split a note into lines no wider than maxw (mm)."""
    out, line = [], ''
    for word in s.split():
        t = (line + ' ' + word).strip()
        if line and tw(t, size) > maxw: out.append(line); line = word
        else: line = t
    return out + [line]
note(14, 86, wrap('The distributor’s contact breaker points switch the coil’s terminal 1 to earth. The injection’s '
                  'trigger contacts are in the distributor too (injection sheet).', 94))
note(14, 98, wrap('Ballast resistor 6 lowers the coil’s voltage while the engine runs. While cranking, starter terminal 16 '
                  'feeds the coil’s side of it directly (119e SV 1.0), so the coil gets full voltage for starting.', 94))
note(155, 81, ('Switch 90 is drawn in P: start contact closed, reversing contact open (it closes in R).',
              'Switch 90’s wires: check E2.'))
note(155, 90.2, ('Seat-belt warning contact 88 on the gear selector: probably not fitted',
                 '(it goes with a belt warning lamp).'))
note(306, 130, ('Relay 89 and switch 90 let the starter turn only in P or N: with the ignition on, switch 90’s start',
               'contact (closed in P and N) energises relay 89, which joins 84a GL 1.5 to 84b GL 1.5 and so',
               'closes the starter line.'))
# 1973 chassis (Charlie, 27 Sep 2026); the 1973 automatic drawing S 3754 runs 84h/84g GL 1.5 through switch 90, no 89;
# the base diagram p.327 draws the 84c jumper across 57 (memory/findings.md, F1)
note(306, 170, wrap('Relay 89 is drawn as the factory wired the 1974 automatic. This car is a 1973 chassis, so whether '
                    'it has relay 89 is check F1. A car without the relay has a short jumper (84c GL 1.5) across the '
                    'two pins of 57 starter line; a 1973 automatic may run the starter line through switch 90 itself '
                    'instead.', 99))

# ---- legend (as the power sheet's, the plain notes in a right-hand column) ---------------------------
lx, ly = 125, 244
LEG_NOTES = ('A cable is labelled with its colour and size (7 BR/VT 1.0),', 'a part with its name (7 Distributor).',
             'Thin black lines without a label: leads with no cable number.')
NX = lx + 140                                                        # notes column, right of the samples (they end by lx + 133)
used = [k for k, f in (('dashed', DASHED[0]), ('stub', STUB[0]), ('tick', TICKED[0])) if f] + ['ht']
last = 5 + 5 * len(used)                                             # the bottom sample row (traced is row 5)
LH = max(22 if PROBABLE[0] else 16, last + 1, 6 + 3.6 * (len(LEG_NOTES) - 1)) + 3.5
LW = NX - lx + max(tw(s, 2.3) for s in LEG_NOTES) + 4
box(lx, ly, round(LW, 1), round(LH, 1), fill='#fff', sw=.5)
for i, (k, n) in enumerate([('BL', 'Blue'), ('BR', 'Brown'), ('GL', 'Yellow'), ('GN', 'Green'),
                            ('GR', 'Grey'), ('RD', 'Red'), ('SV', 'Black'), ('VT', 'White')]):
    x, y = lx + 4 + (i % 4) * 23, ly + 6 + (i // 4) * 5
    A(f'<path d="M{x},{y - 1} h7" stroke="#222" stroke-width="1.7"/><path d="M{x},{y - 1} h7" stroke="{COL[k]}" stroke-width="1.1"/>')
    txt(x + 9, y, f'{k} {n}', 2.5)
x = lx + 97
A(f'<path d="M{x},{ly + 5} h9" stroke="#222" stroke-width="1.7"/>'); txt(x + 11, ly + 6, 'traced (cable no. read)', 2.4)
for r, k in zip(range(10, last + 1, 5), used):                      # the samples used, one under another
    if k == 'dashed':
        A(f'<path d="M{x},{ly + r} h9" stroke="#222" stroke-width="1.7" stroke-dasharray="3 2"/>'); txt(x + 11, ly + r + 1, 'not traced yet', 2.4)
    elif k == 'stub':
        A(f'<path d="M{x},{ly + r} h7" stroke="#222" stroke-width=".8"/><circle cx="{x + 8.3}" cy="{ly + r}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
        txt(x + 11, ly + r + 1, 'ends on diagram', 2.4)
    elif k == 'tick':
        tick(x + 3, ly + r + .3); txt(x + 11, ly + r + 1, 'checked on the car', 2.4)
    else:
        ht([(x, ly + r), (x + 9, ly + r)]); txt(x + 11, ly + r + 1, 'HT lead (no number)', 2.4)
size_legend(lx + 4, ly + 16)
probable_legend(lx + 4, ly + 21)
note(NX, ly + 6, LEG_NOTES)
save('ignition.svg')

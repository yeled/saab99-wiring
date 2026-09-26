"""Shared drawing helpers for the wiring sheets (SVG, units in mm)."""
import csv, os
ROOT = os.path.join(os.path.dirname(__file__), '..')
WIRES = {r['cable']: r for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'wires.csv')))}
FUSES = {int(r['fuse']): r for r in csv.DictReader(open(os.path.join(ROOT, 'data', 'fuses.csv')))}

def fuse_label(n, prefix='F'):
    return f"{prefix}{n} · {FUSES[n]['rating']}"

def fuse_checked(n):
    return FUSES[n]['status'] == 'car'

def tick(x, y, s=1.0, rot=None, cx=None, cy=None):
    """Green check mark drawn as a path, so it prints without needing a symbol font."""
    TICKED[0] = True
    tr = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    A(f'<path d="M{x},{y - 1.1 * s} l{0.9 * s},{1.0 * s} l{1.9 * s},{-2.4 * s}" fill="none" stroke="#1e7a3a" '
      f'stroke-width="{0.55 * s}" stroke-linecap="round" stroke-linejoin="round"{tr}/>')
COL = {'BL': '#1f5fbf', 'GN': '#1e9e3e', 'GR': '#8a8a8a', 'GL': '#f2c500', 'VT': '#ffffff',
       'SV': '#111111', 'RD': '#d42020', 'BR': '#7a4a1c'}
o = []
A = o.append


ARROWS = {'→': '<tspan font-family="Arial">→</tspan>', '←': '<tspan font-family="Arial">←</tspan>'}  # Helvetica has no arrows and cairo doesn't fall back per glyph

def txt(x, y, s, size=3.0, anchor='start', w='normal', fill='#111', rot=None):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ''
    for a, t in ARROWS.items(): s = s.replace(a, t)
    A(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{fill}"{tr}>{s}</text>')

def path(pts):
    return 'M' + ' L'.join(f'{x},{y}' for x, y in pts)

TICKED = [False]  # set when a sheet draws a check mark; the legend shows the tick sample only then
DASHED = [False]  # set when a sheet draws anything 'not traced'; the legend shows the dashed sample only then
PROBABLE = [False]  # set when a part's internals are drawn grey (probable); probable_legend() draws only then


# Core width (mm) by cable size (mm2): exaggerated at the thin end so a size step shows at a glance (0.75 well under
# 1.0), sloping off above 2.5 so the main feeds stay lines, not bands; the black outline adds edge(cw).
# The book draws every line alike: this is ours. Unknown sizes draw as 1.0.
WIDTH = {0.5: .35, 0.75: .5, 1.0: 1.1, 1.5: 1.6, 2.5: 2.3, 4.0: 2.8, 16.0: 3.4}
def edge(cw): return .4 if cw < 1 else .6     # outline added to the core: thinner below 1.0 so the colour still shows
def core_width(cable):
    try: return WIDTH.get(float(WIRES[cable]['mm2']), 1.1)
    except ValueError: return 1.1

def _clear_label(pts, lx, ly, rot, length, shift):
    """Move a label (lx, ly) away from the nearest parallel segment of its wire by shift; returns the new (lx, ly)."""
    best = None
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if rot is None and y0 == y1:
            a, b, c, p, q = min(x0, x1), max(x0, x1), y0, ly, (lx, lx + length)
        elif rot is not None and x0 == x1:
            a, b, c, p = min(y0, y1), max(y0, y1), x0, lx
            q = (ly - length, ly) if rot < 0 else (ly, ly + length)
        else:
            continue
        if q[1] < a - 2 or q[0] > b + 2: continue          # the label doesn't run along this segment
        if best is None or abs(p - c) < best[0]: best = (abs(p - c), c)
    if best is None: return lx, ly
    c = best[1]
    if rot is None: return lx, ly + (shift if ly > c else -shift)
    return lx + (shift if lx > c else -shift), ly

def wire(cable, pts, lx=None, ly=None, rot=None, label=True):
    r = WIRES[cable]
    dash = ' stroke-dasharray="3 2"' if r['status'] == 'open' else ''
    if dash: DASHED[0] = True
    d = path(pts)
    cw = core_width(cable)
    if r['colour'] == '':                       # colour not read yet: plain grey
        A(f'<path d="{d}" fill="none" stroke="#777" stroke-width="0.9" stroke-linejoin="round"{dash}/>')
    else:
        cols = r['colour'].split('/')
        A(f'<path d="{d}" fill="none" stroke="#222" stroke-width="{cw + edge(cw):g}" stroke-linejoin="round"{dash}/>')
        A(f'<path d="{d}" fill="none" stroke="{COL[cols[0]]}" stroke-width="{cw:g}" stroke-linejoin="round"{dash}/>')
        if len(cols) == 2 and not dash:          # second colour as a stripe (skipped on dashed wires)
            A(f'<path d="{d}" fill="none" stroke="{COL[cols[1]]}" stroke-width="{max(.3, round(cw * .45, 2)):g}" stroke-dasharray="1.2 1.2"/>')
    if r['status'] == 'stub':
        x, y = pts[-1]
        A(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    if label and lx is not None:
        if cable.startswith('?'):
            s = 'cable no. not read'
        else:
            s = f"{cable.split('#')[0]} {r['colour']} {r['mm2']}"  # '#suffix' only disambiguates duplicate numbers
        shift = (cw + edge(cw)) / 2 - .85                 # half-width beyond a 1.0 wire's: heavier wires push their label clear
        if shift > 0 and r['colour']: lx, ly = _clear_label(pts, lx, ly, rot, len(s) * 1.62, round(shift, 2))
        if rot is None:
            A(f'<rect x="{lx - .6}" y="{ly - 3.0}" width="{len(s) * 1.62 + 1.2}" height="3.6" fill="#fff" opacity=".85"/>')
        txt(lx, ly, s, 2.8 if not cable.startswith('?') else 2.4, rot=rot, fill='#111' if not cable.startswith('?') else '#666')
        if r['status'] == 'car':
            tick(lx + len(s) * 1.62 + 1.2, ly - 0.6, rot=rot, cx=lx, cy=ly)

def dot(x, y): A(f'<circle cx="{x}" cy="{y}" r="1.0" fill="#111"/>')
def earth(x, y):
    A(f'<path d="M{x},{y} v3 M{x - 3},{y + 3} h6 M{x - 2},{y + 4.3} h4 M{x - 1},{y + 5.6} h2" stroke="#111" stroke-width=".5" fill="none"/>')
def lamp(x, y, cap='', r=4.5, anchor='middle', cx=None, cy=None):
    A(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    k = r * .7
    A(f'<path d="M{x - k},{y - k} L{x + k},{y + k} M{x - k},{y + k} L{x + k},{y - k}" stroke="#111" stroke-width=".45"/>')
    if cap: txt(cx if cx is not None else x, cy if cy is not None else y - r - 2, cap, 2.7, anchor)
def box(x, y, w, h, fill='#fafafa', sw=.8):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="1.2" fill="{fill}" stroke="#111" stroke-width="{sw}"/>')
def lamp_earth(x, y, dx=-9):
    A(f'<path d="M{x},{y} h{dx} v5" stroke="#111" stroke-width=".6" fill="none"/>'); earth(x + dx, y + 5)


# ---- component internals, in the style of relay 67 on the wipers sheet -------------------------
# Circles (contact, diode, lamps) are placed by centre; rectangles (coil, resistor, fuse) by top-left, like box().
# grey=True means probably, not printed clearly: stroke #888 instead of #111, and probable_legend() then draws.
# Terminals stay dot(); leads from a terminal to a contact or winding are inner().

def _n(v):
    v = round(v, 3); return int(v) if v == int(v) else v

def _ink(grey):
    if grey: PROBABLE[0] = True
    return '#888' if grey else '#111'

def _ends(x, y, w, h):
    """Lead ends of a rectangle along its long side."""
    return ((_n(x), _n(y + h / 2)), (_n(x + w), _n(y + h / 2))) if w >= h else ((_n(x + w / 2), _n(y)), (_n(x + w / 2), _n(y + h)))

def tlabel(x, y, text, anchor='start'):
    """Tiny terminal label (relay 67: 1.8, #555), e.g. 1.3 above and 2 inside the terminal dot."""
    txt(x, y, text, 1.8, anchor, fill='#555')

def contact(x, y, grey=False):
    """Open contact circle (r .8) centred on (x, y); inner() leads stop .8 short of the centre."""
    A(f'<circle cx="{_n(x)}" cy="{_n(y)}" r=".8" fill="#fff" stroke="{_ink(grey)}" stroke-width=".35"/>')

def blade(x0, y0, x1, y1, grey=False):
    """Moving contact blade from its pivot to its free end; start about .7 off the pivot contact's centre."""
    A(f'<path d="M{_n(x0)},{_n(y0)} L{_n(x1)},{_n(y1)}" stroke="{_ink(grey)}" stroke-width=".75" stroke-linecap="round"/>')

def mlink(pts):
    """Mechanical link, e.g. coil to the blades it moves: thin grey dashed line, as the manual prints it."""
    A(f'<path d="{path([(_n(x), _n(y)) for x, y in pts])}" fill="none" stroke="#999" stroke-width=".3" stroke-dasharray=".8 .6"/>')

def inner(pts, grey=False):
    """Thin conductor inside a part: terminal to contact, coil or winding."""
    A(f'<path d="{path([(_n(x), _n(y)) for x, y in pts])}" fill="none" stroke="{_ink(grey)}" stroke-width=".4"/>')

def coil(x, y, w=8, h=7, grey=False):
    """Relay coil or any winding (heater, valve, regulator): rectangle with a lower-left to upper-right diagonal.
    Returns the mid-points of its left, right, top and bottom sides (leads; the top one suits mlink)."""
    c = _ink(grey); x0, y0, x1, y1, xm, ym = _n(x), _n(y), _n(x + w), _n(y + h), _n(x + w / 2), _n(y + h / 2)
    A(f'<rect x="{x0}" y="{y0}" width="{_n(w)}" height="{_n(h)}" fill="#fff" stroke="{c}" stroke-width=".4"/>'
      f'<path d="M{x0},{y1} L{x1},{y0}" stroke="{c}" stroke-width=".35"/>')
    return (x0, ym), (x1, ym), (xm, y0), (xm, y1)

def resistor(x, y, w=8, h=3, grey=False):
    """Resistor: plain rectangle. Returns its two lead ends along the long side."""
    A(f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" fill="#fff" stroke="{_ink(grey)}" stroke-width=".4"/>')
    return _ends(x, y, w, h)

def fuse(x, y, w=6, h=2.4, rating=None, grey=False):
    """Fuse: rectangle with a line through its length; rating (e.g. '3 A') above it, or right of it when upright.
    Returns its two lead ends."""
    c = _ink(grey); a, b = _ends(x, y, w, h)
    A(f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" fill="#fff" stroke="{c}" stroke-width=".4"/>'
      f'<path d="M{a[0]},{a[1]} L{b[0]},{b[1]}" stroke="{c}" stroke-width=".35"/>')
    if rating: tlabel(_n(x + w / 2), _n(y - .8), rating, 'middle') if w >= h else tlabel(_n(x + w + 1), _n(y + h / 2 + .6), rating)
    return a, b

def diode(x, y, direction, grey=False, s=2.4):
    """Diode centred on (x, y): filled triangle and bar pointing the way current flows ('r', 'l', 'u' or 'd').
    Returns (anode, cathode) lead points."""
    c = _ink(grey); h = s / 2
    dx, dy = {'r': (1, 0), 'l': (-1, 0), 'u': (0, -1), 'd': (0, 1)}[direction[0]]
    px, py = dy * h, dx * h                              # half-width across the direction of flow
    b, t = (_n(x - dx * h), _n(y - dy * h)), (_n(x + dx * h), _n(y + dy * h))
    A(f'<path d="M{_n(b[0] + px)},{_n(b[1] + py)} L{_n(b[0] - px)},{_n(b[1] - py)} L{t[0]},{t[1]} Z" fill="{c}" stroke="{c}" '
      f'stroke-width=".25" stroke-linejoin="round"/><path d="M{_n(t[0] + px)},{_n(t[1] + py)} L{_n(t[0] - px)},{_n(t[1] - py)}" '
      f'stroke="{c}" stroke-width=".45"/>')
    return b, t

def bimetal(x0, y0, x1, y1, grey=False):
    """Thermostat (bimetal) blade: a doubled blade from its pivot to its free end, marked t°. Use with contact()."""
    c = _ink(grey); L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
    ux, uy = (y1 - y0) / L, (x0 - x1) / L                # unit normal; flip it so t° sits above the blade
    if uy > 0 or (uy == 0 and ux < 0): ux, uy = -ux, -uy
    d = ' '.join(f'M{_n(x0 + k * ux)},{_n(y0 + k * uy)} L{_n(x1 + k * ux)},{_n(y1 + k * uy)}' for k in (.3, -.3))
    A(f'<path d="{d}" stroke="{c}" stroke-width=".35" stroke-linecap="round"/>')
    tlabel(_n((x0 + x1) / 2 + 1.6 * ux), _n((y0 + y1) / 2 + 1.6 * uy + .6), 't°', 'middle')

def twin_lamp(x, y, r=4.5, grey=False):
    """Twin-filament bulb (headlamp high/low beam) centred on (x, y): two filament arcs that meet at a common end.
    grey greys only the filaments. Returns (upper feed, lower feed, common): feeds on the left rim, common on the right."""
    c = _ink(grey); k, a = r * .893, r * .45
    A(f'<circle cx="{_n(x)}" cy="{_n(y)}" r="{_n(r)}" fill="#fff" stroke="#111" stroke-width=".6"/>')
    ends = []
    for sy in (-1, 1):                                   # feed enters level; upper filament bows up, lower bows down
        f, s, e = (x - k, y + sy * a), (x - r * .4, y + sy * a), (x + r * .2, y + sy * a)
        ends.append((_n(f[0]), _n(f[1])))
        A(f'<path d="M{_n(f[0])},{_n(f[1])} L{_n(s[0])},{_n(s[1])} A{_n(r * .3)},{_n(r * .3)} 0 0 {1 if sy < 0 else 0} '
          f'{_n(e[0])},{_n(e[1])} L{_n(x + r)},{_n(y)}" fill="none" stroke="{c}" stroke-width=".4" stroke-linejoin="round"/>')
    return ends[0], ends[1], (_n(x + r), _n(y))

def size_legend(x, y):
    """Legend row for line widths (sample bars at y - 1, text baseline y, like the other samples). Returns its width."""
    txt(x, y, 'cable size, mm²:', 2.4)
    cx = x + 22
    for mm2 in (0.75, 1.5, 2.5, 4.0):
        A(f'<path d="M{cx},{y - 1} h7" stroke="#222" stroke-width="{WIDTH[mm2] + edge(WIDTH[mm2]):g}"/>'); txt(cx + 8.5, y, f'{mm2}', 2.4)
        cx += 15.5
    return cx - x

def probable_legend(x, y):
    """Legend sample for grey internals, drawn only when a helper had grey=True; (x, y) like the dashed sample. Returns whether it drew."""
    if not PROBABLE[0]: return False
    contact(x + 1, y, True); contact(x + 8, y, True); blade(x + 1.7, y - .3, x + 7.6, y - 2.4, True)
    txt(x + 11, y + 1, 'grey inside a part: probably, not printed clearly', 2.4)
    return True


def unknown_style(r):
    return r['colour'] == ''

def tag(x, y, text, w=None, dashed=False, size=2.6, anchor='start'):
    """Destination tag: a small box at (x, y-centre) naming where a wire goes."""
    w = w or len(text) * size * 0.52 + 3
    x0 = x if anchor == 'start' else x - w
    dash = ' stroke-dasharray="1.5 1"' if dashed else ''
    if dashed: DASHED[0] = True
    A(f'<rect x="{x0}" y="{y - 2.6}" width="{w}" height="5.2" rx="1" fill="#fff" stroke="#444" stroke-width=".4"{dash}/>')
    txt(x0 + 1.5, y + 1, text, size)
    return x0 + w

def header(title, sub):
    A('<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" '
      'font-family="Helvetica, Arial, sans-serif">')
    A('<rect width="420" height="297" fill="#fff"/><rect x="8" y="8" width="404" height="281" fill="none" stroke="#111" stroke-width=".6"/>')
    txt(14, 19, title, 6, w='bold')
    txt(14, 25.5, sub, 2.8, fill='#444')

def save(name):
    A('</svg>')
    out = os.path.join(ROOT, 'out', name)
    open(out, 'w').write('\n'.join(o)); print('wrote', out)

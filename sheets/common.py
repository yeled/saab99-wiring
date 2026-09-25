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


def txt(x, y, s, size=3.0, anchor='start', w='normal', fill='#111', rot=None):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ''
    A(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{w}" fill="{fill}"{tr}>{s}</text>')

def path(pts):
    return 'M' + ' L'.join(f'{x},{y}' for x, y in pts)

TICKED = [False]  # set when a sheet draws a check mark; the legend shows the tick sample only then
DASHED = [False]  # set when a sheet draws anything 'not traced'; the legend shows the dashed sample only then


def wire(cable, pts, lx=None, ly=None, rot=None, label=True):
    r = WIRES[cable]
    dash = ' stroke-dasharray="3 2"' if r['status'] == 'open' else ''
    if dash: DASHED[0] = True
    d = path(pts)
    if r['colour'] == '':                       # colour not read yet: plain grey
        A(f'<path d="{d}" fill="none" stroke="#777" stroke-width="0.9" stroke-linejoin="round"{dash}/>')
    else:
        cols = r['colour'].split('/')
        A(f'<path d="{d}" fill="none" stroke="#222" stroke-width="1.7" stroke-linejoin="round"{dash}/>')
        A(f'<path d="{d}" fill="none" stroke="{COL[cols[0]]}" stroke-width="1.1" stroke-linejoin="round"{dash}/>')
        if len(cols) == 2 and not dash:          # second colour as a stripe (skipped on dashed wires)
            A(f'<path d="{d}" fill="none" stroke="{COL[cols[1]]}" stroke-width="0.5" stroke-dasharray="1.2 1.2"/>')
    if r['status'] == 'stub':
        x, y = pts[-1]
        A(f'<circle cx="{x}" cy="{y}" r="1.3" fill="#fff" stroke="#222" stroke-width=".5"/>')
    if label and lx is not None:
        if cable.startswith('?'):
            s = 'cable no. not read'
        else:
            s = f"{cable.split('#')[0]} {r['colour']} {r['mm2']}"  # '#suffix' only disambiguates duplicate numbers
        if rot is None:
            A(f'<rect x="{lx - .6}" y="{ly - 3.0}" width="{len(s) * 1.62 + 1.2}" height="3.8" fill="#fff" opacity=".85"/>')
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

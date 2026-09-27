#!/usr/bin/env python3
"""Follow wires on the scanned diagram and make contact sheets of where they end.

Needs the page cache first:
  python3 tools/trace.py render --pdf source/1980-99-service-manual.pdf --page 407

Command line:
  python3 tools/follow.py trace X Y DIR [--out ends.png]   follow one line; prints the end, grid square, nearby parts
  python3 tools/follow.py walk X Y DIR XEND                 straight walk along a long horizontal run

From Python (how the redraw sessions used it):
  import sys; sys.path.insert(0, 'tools'); import follow as F
  F.run({'fuse 4 third line': (2813, 2650, 'down')}, '/tmp/ends.png')

Coordinates are pixels on PDF p. 407 at 400 dpi (x right, y down). The scan is rotated about 0.5 degrees,
so horizontal lines drift ~25 px across the page, and there is a fold gap at x 4650-4710 (bridged).
The follower carries straight on at crossings but can slip onto a neighbour where lines touch or cross:
confirm a result from the other end, or zoom with `tools/trace.py crop`, before recording it.
"""
import argparse, csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, HERE)
from trace import load, Tracer  # noqa: E402

D = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}
# Grid lines of the printed diagram at 400 dpi: columns 1-14, rows A-F.
COLB = [v * 6.3146 for v in (55, 152, 250, 349, 447, 543, 640, 738, 835, 931, 1029, 1126, 1226, 1323, 1420)]
ROWB = [v * 6.3146 for v in (80, 168, 255, 345, 440, 530, 625)]
COMPS = {c['no']: c for c in csv.DictReader(open(os.path.join(ROOT, 'data', 'components.csv')))}
_P = {}


def page():
    """Load the cached page once: A is greyscale, B is the ink mask."""
    if not _P:
        try:
            A, B = load(407)
        except FileNotFoundError:
            sys.exit('No page cache. Run:  python3 tools/trace.py render --pdf source/1980-99-service-manual.pdf --page 407')
        _P.update(A=A, B=B, tr=Tracer(A < 175))
    return _P


def grid(x, y):
    c = next((i + 1 for i in range(len(COLB) - 1) if COLB[i] <= x < COLB[i + 1]), None)
    r = next(('ABCDEF'[i] for i in range(len(ROWB) - 1) if ROWB[i] <= y < ROWB[i + 1]), None)
    return f'{r}{c}' if c and r else '?'


def near(g):
    """Components the legend places in grid square g."""
    return [n for n, c in COMPS.items() if g in c['grid'].split()]


def snap(x, y, d, r=8):
    """Move a start point onto the nearest line, perpendicular to the direction of travel."""
    B = page()['B']; dx, dy = D[d]
    for o in sorted(range(-r, r + 1), key=abs):
        xx, yy = x + o * abs(dy), y + o * abs(dx)
        if B[int(yy), int(xx)]:
            return xx, yy
    return x, y


def follow(x, y, d, maxturn=12):
    """Follow a line through up to maxturn corners. Returns (corners, why) with why in end / T-junction / maxturn."""
    tr = page()['tr']; dx, dy = D[d]; corners = [(x, y)]; why = 'maxturn'
    for _ in range(maxturn):
        _, (ex, ey) = tr.straight(x, y, dx, dy, gap_max=14)
        corners.append((ex, ey))
        px, py = abs(dy), abs(dx)
        conts = [(s * px, s * py) for s in (1, -1) if tr.arm(ex, ey, s * px, s * py) >= 12]
        if len(conts) == 1:
            x, y = ex, ey; dx, dy = conts[0]; continue
        why = 'end' if not conts else 'T-junction'; break
    return corners, why


def walk(x, y, d, xend, maxgap=80):
    """Straight walk along a horizontal run to x = xend, allowing 1 px drift per step and gaps up to maxgap.
    Handy for long runs across the skewed page. Returns (x, y, 'reached' or 'stopped')."""
    B = page()['B']; step = 1 if d == 'right' else -1; gap = 0
    while (x - xend) * step < 0:
        x += step
        cand = [yy for yy in (y - 1, y, y + 1) if B[yy, x]]
        if cand:
            y = min(cand, key=lambda yy: abs(yy - y)); gap = 0
        else:
            gap += 1
            if gap > maxgap:
                return x - step * gap, y, 'stopped'
    return x, y, 'reached'


def sheet(items, out, w=460, h=280, scale=1.1, cols=2):
    """Contact sheet: a crop around each (name, (x, y)) with the point circled."""
    from PIL import Image, ImageDraw
    A = page()['A']; tiles = []
    for name, (ex, ey) in items:
        x0, y0 = int(max(0, ex - w / 2)), int(max(0, ey - h / 2))
        im = Image.fromarray(A[y0:y0 + h, x0:x0 + w]).convert('RGB').resize((int(w * scale), int(h * scale)))
        dr = ImageDraw.Draw(im); cx, cy = (ex - x0) * scale, (ey - y0) * scale
        dr.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=(255, 0, 0), width=2)
        dr.rectangle([0, 0, len(name) * 7 + 6, 14], fill=(255, 255, 0)); dr.text((3, 1), name, fill=(0, 0, 0))
        tiles.append(im)
    W, H = tiles[0].size; rows = (len(tiles) + cols - 1) // cols
    S = Image.new('RGB', (W * cols + (cols - 1) * 6, H * rows + (rows - 1) * 6), 'white')
    for i, t in enumerate(tiles):
        S.paste(t, ((i % cols) * (W + 6), (i // cols) * (H + 6)))
    S.save(out)


def run(starts, out, cols=2, w=460, h=280, scale=1.1):
    """Follow several lines {name: (x, y, dir)}, print where each ends, and write one contact sheet."""
    res = {}
    for k, (x, y, d) in starts.items():
        x, y = snap(x, y, d)
        cs, why = follow(x, y, d); ex, ey = cs[-1]; g = grid(ex, ey); res[k] = (cs, why)
        parts = [n + ':' + COMPS[n]['name'][:20] for n in near(g)][:4]
        print(f"{k:14s} {why:10s} end=({ex:.0f},{ey:.0f}) {g:4s} {parts} via={[(round(a), round(b)) for a, b in cs[1:-1]]}")
    sheet([(k, res[k][0][-1]) for k in starts], out, w=w, h=h, scale=scale, cols=cols)
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    t = sub.add_parser('trace'); t.add_argument('x', type=int); t.add_argument('y', type=int); t.add_argument('dir', choices=D)
    t.add_argument('--out', default='ends.png')
    w = sub.add_parser('walk'); w.add_argument('x', type=int); w.add_argument('y', type=int); w.add_argument('dir', choices=('left', 'right'))
    w.add_argument('xend', type=int)
    a = ap.parse_args()
    if a.cmd == 'trace':
        run({f'{a.x},{a.y} {a.dir}': (a.x, a.y, a.dir)}, a.out, cols=1)
    else:
        print(walk(a.x, a.y, a.dir, a.xend))


if __name__ == '__main__':
    main()

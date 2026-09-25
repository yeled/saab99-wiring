#!/usr/bin/env python3
"""Follow wires on the scanned Saab 99 wiring diagram.

The diagram is drawn with straight horizontal/vertical lines that cross each
other without junction dots. This walks one wire from a starting pixel, steps
over crossings, bridges the gap at the scan's fold, and turns at corners.
Always confirm a result by reading the cable label printed on the traced line.

Coordinates are pixels on the page rendered at 400 dpi.

  python3 tools/trace.py render --pdf manual.pdf --page 407
  python3 tools/trace.py crop 4250 1930 4600 2160 --out relay8.png
  python3 tools/trace.py trace 4479 2125 down --out overlay.png
"""
import argparse, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

CACHE = os.path.join(os.path.dirname(__file__), '..', 'cache')
T = 3            # line thickness in px at 400 dpi
FOLD = (4650, 4710)  # x range of the fold gap on PDF p.407 (400 dpi)
DIRS = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}

def load(page=407):
    a = np.load(os.path.join(CACHE, f'p{page}.npy'))
    return a, a < 150

def render(pdf, page, dpi=400):
    os.makedirs(CACHE, exist_ok=True)
    base = os.path.join(CACHE, f'p{page}')
    subprocess.run(['pdftoppm', '-gray', '-r', str(dpi), '-f', str(page), '-l', str(page), pdf, base], check=True)
    pgm = [f for f in os.listdir(CACHE) if f.startswith(f'p{page}-') and f.endswith('.pgm')][0]
    np.save(base + '.npy', np.array(Image.open(os.path.join(CACHE, pgm))))
    os.remove(os.path.join(CACHE, pgm))
    print('cached', base + '.npy')

class Tracer:
    def __init__(self, B):
        self.B = B; self.H, self.W = B.shape
    def ink(self, x, y):
        x, y = int(round(x)), int(round(y))
        return 0 <= x < self.W and 0 <= y < self.H and self.B[y, x]
    def perp_run(self, x, y, px, py, win=5, lim=80):
        best = next((o for o in sorted(range(-win, win + 1), key=abs) if self.ink(x + o * px, y + o * py)), None)
        if best is None: return None
        lo = hi = best
        while lo > -lim and self.ink(x + (lo - 1) * px, y + (lo - 1) * py): lo -= 1
        while hi < lim and self.ink(x + (hi + 1) * px, y + (hi + 1) * py): hi += 1
        return lo, hi
    def straight(self, x, y, dx, dy, gap_max=10, win=5, maxlen=20000):
        px, py = abs(dy), abs(dx)
        pts, gap, last = [(x, y)], 0, (x, y)
        for _ in range(maxlen):
            nx, ny = x + dx, y + dy
            r = self.perp_run(nx, ny, px, py, win)
            if r is None:
                gap += 1
                lim = 22 if (dx and FOLD[0] <= nx <= FOLD[1]) else gap_max
                if gap > lim: break
                x, y = nx, ny; continue
            gap = 0
            lo, hi = r
            if hi - lo + 1 <= 2 * T + 3:           # our own line: re-centre (follows scan skew)
                c = (lo + hi) / 2.0; nx, ny = nx + c * px, ny + c * py
            x, y = nx, ny; last = (x, y); pts.append(last)   # wide run = crossing: keep going straight
        return pts, last
    def arm(self, x, y, dx, dy):
        _, (ex, ey) = self.straight(x, y, dx, dy, gap_max=3, win=3, maxlen=400)
        return abs(ex - x) + abs(ey - y)
    def trace(self, x, y, dx, dy, maxseg=20):
        segs, todo, seen, log = [], [(x, y, dx, dy)], set(), []
        while todo and len(segs) < maxseg:
            x, y, dx, dy = todo.pop(0)
            key = (int(x) // 6, int(y) // 6, dx, dy)
            if key in seen: continue
            seen.add(key)
            pts, (ex, ey) = self.straight(x, y, dx, dy)
            segs.append(pts)
            px, py = abs(dy), abs(dx)
            conts = [(s * px, s * py) for s in (1, -1) if self.arm(ex, ey, s * px, s * py) >= 12]
            log.append(f'end ({ex:.0f},{ey:.0f}) after {len(pts)}px; continues {conts or "nowhere"}')
            todo += [(ex, ey, a, b) for a, b in conts]
        return segs, log

def crop(A, x0, y0, x1, y1, out, scale=3):
    im = Image.fromarray(A[y0:y1, x0:x1]).convert('RGB').resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for x in range((x0 // 25 + 1) * 25, x1, 25):
        d.line([((x - x0) * scale, 0), ((x - x0) * scale, 16 if x % 100 == 0 else 8)], fill=(255, 0, 0))
        if x % 100 == 0: d.text(((x - x0) * scale + 2, 16), str(x), fill=(255, 0, 0))
    for y in range((y0 // 25 + 1) * 25, y1, 25):
        d.line([(0, (y - y0) * scale), (16 if y % 100 == 0 else 8, (y - y0) * scale)], fill=(0, 0, 255))
        if y % 100 == 0: d.text((18, (y - y0) * scale - 6), str(y), fill=(0, 0, 255))
    im.save(out); print('wrote', out)

def overlay(A, segs, out, scale=0.25):
    im = Image.fromarray(A).convert('RGB')
    im = im.resize((int(im.size[0] * scale), int(im.size[1] * scale)))
    d = ImageDraw.Draw(im)
    for i, s in enumerate(segs):
        d.line([(x * scale, y * scale) for x, y in s], fill=[(230, 0, 0), (0, 150, 0), (0, 0, 230)][i % 3], width=3)
    im.save(out); print('wrote', out)

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('render'); r.add_argument('--pdf', required=True); r.add_argument('--page', type=int, default=407)
    c = sub.add_parser('crop'); [c.add_argument(k, type=int) for k in ('x0', 'y0', 'x1', 'y1')]
    c.add_argument('--out', default='crop.png'); c.add_argument('--scale', type=int, default=3); c.add_argument('--page', type=int, default=407)
    t = sub.add_parser('trace'); t.add_argument('x', type=float); t.add_argument('y', type=float); t.add_argument('dir', choices=DIRS)
    t.add_argument('--out', default='overlay.png'); t.add_argument('--page', type=int, default=407)
    a = ap.parse_args()
    if a.cmd == 'render': return render(a.pdf, a.page)
    A, B = load(a.page)
    if a.cmd == 'crop': return crop(A, a.x0, a.y0, a.x1, a.y1, a.out, a.scale)
    segs, log = Tracer(B).trace(a.x, a.y, *DIRS[a.dir])
    print('\n'.join(log)); overlay(A, segs, a.out)

if __name__ == '__main__':
    sys.exit(main())

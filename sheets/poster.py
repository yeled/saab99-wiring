#!/usr/bin/env python3
"""Compose all nine A3 sheets onto one A0 landscape poster (3 by 3, about 92%), with a title strip.

The sheets stay the working drawings; this only nests their SVG, so rerun it after any change.
"""
import csv, os, re, datetime
from collections import Counter
ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'out')
ORDER = [('power', 'Power distribution'), ('lighting', 'Lighting'), ('ignition', 'Ignition, starting, fuel injection'),
         ('instruments', 'Instruments and warning lamps'), ('signals', 'Indicators, hazards, brake, reversing'),
         ('radio', 'Radio, speakers, accessory feeds'), ('wipers', 'Wipers and washers'),
         ('climate', 'Radiator fan, heater fan, heated rear window'), ('interior', 'Interior lights, seat heating, seat belts')]
W, H, PW, PH, STRIP = 420, 297, 1189, 841, 18
S = min(PW / (3 * W), (PH - STRIP) / (3 * H))
X0 = (PW - 3 * W * S) / 2

def inner(path):
    s = open(path).read()
    s = re.sub(r'^\s*<svg[^>]*>', '', s, count=1)
    return s[:s.rfind('</svg>')]

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}">',
         f'<rect width="{PW}" height="{PH}" fill="#fff"/>']
for i, (key, title) in enumerate(ORDER):
    x, y = X0 + (i % 3) * W * S, (i // 3) * H * S
    p = os.path.join(OUT, f'{key}.svg')
    body = inner(p) if os.path.exists(p) else (
        f'<g font-family="Helvetica, Arial, sans-serif"><rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="#fafafa" '
        f'stroke="#bbb" stroke-dasharray="4 3"/><text x="{W / 2}" y="{H / 2}" font-size="8" text-anchor="middle" fill="#999">{title} (to come)</text></g>')
    parts.append(f'<svg x="{x}" y="{y}" width="{W * S}" height="{H * S}" viewBox="0 0 {W} {H}">{body}</svg>')
wires = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'wires.csv'))))
st = Counter(w['status'] for w in wires)
ty = 3 * H * S + 11
parts.append(f'<g font-family="Helvetica, Arial, sans-serif"><text x="{X0 + 8}" y="{ty}" font-size="8" font-weight="bold">Saab 99 Turbo, model 1979: wiring redrawn</text>'
             f'<text x="{X0 + 185}" y="{ty}" font-size="4.2" fill="#444">from the Saab Service Manual 1975–1980, diagram p. 371-28/29. '
             f'Wires: {st["traced"] + st["traced+text"]} traced, {st["open"]} not traced yet, {st["stub"]} end on the diagram, {st["car"]} checked on the car. '
             f'Colour codes are Swedish (GL gul = yellow, SV svart = black, VT vit = white). Generated {datetime.date.today():%d %B %Y}.</text></g>')
parts.append('</svg>')
open(os.path.join(OUT, 'poster.svg'), 'w').write('\n'.join(parts))
print('wrote', os.path.join(OUT, 'poster.svg'))

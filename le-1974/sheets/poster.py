#!/usr/bin/env python3
"""Compose the nine A3 sheets onto one A0 landscape poster (3 by 3, about 92%), with a title strip.

The sheets stay the working drawings; this only nests their SVG, so rerun it after any change to a sheet.
A sheet not built yet shows as a dashed placeholder, and the script says so.
"""
import csv, os, re, sys, datetime
from collections import Counter
ROOT = os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(ROOT, 'out')
# The titles are the sheets' own header titles, so a 'to come' placeholder reads as the sheet that replaces it.
ORDER = [('power', 'Power distribution'), ('ignition', 'Ignition and starting'), ('injection', 'Fuel injection (D-Jetronic)'),
         ('lighting', 'Lighting circuit'), ('instruments', 'Instruments, warning lamps and panel lighting'),
         ('signals', 'Indicators, hazards, brake and reversing lights'), ('wipers', 'Wipers and washers'),
         ('climate', 'Heater fan and radiator fan'), ('interior', 'Interior lights and seat heating')]
# Cables the sheets do not draw, because their part is not fitted on this car (Charlie) or probably not fitted:
NOT_FITTED = set(('13 105 '                                   # clock 49: removed, a rev counter instead (check D1)
                  '77 77a 77e 77f 78 81 81e 82 83 '           # headlamp wipers 65, 66 and their relay 67
                  '146 127 '                                  # choke lamp 33 and choke contact 34 (probably not fitted)
                  '191f 197e').split())                       # seat-belt contact 88 on the gear selector (probably not)
# and the jumper across the starter line at 57 that only a car without start inhibitor relay 89 has (check F1):
JUMPER = '84c'
NOT_DRAWN = NOT_FITTED | {JUMPER}
W, H, PW, PH, STRIP = 420, 297, 1189, 841, 18
S = min(PW / (3 * W), (PH - STRIP) / (3 * H))
X0 = (PW - 3 * W * S) / 2

def inner(path):
    s = open(path).read()
    s = re.sub(r'^\s*<svg[^>]*>', '', s, count=1)
    return s[:s.rfind('</svg>')]

def scope_ids(body, key):
    """Prefix every id a sheet defines (and its url(#..)/href="#.." uses) with the sheet name, so two nested sheets
    can never share an id. The sheets from lib/wiring.py define none, and then the body comes back unchanged."""
    ids = set(re.findall(r'\bid="([^"]+)"', body))
    if not ids: return body
    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{key}-{m.group(1)}"', body)
    ref = lambda m: m.group(1) + (f'{key}-{m.group(2)}' if m.group(2) in ids else m.group(2))
    body = re.sub(r'(url\(\s*["\']?#)([^)"\'\s]+)', ref, body)
    return re.sub(r'(href="#)([^"]+)', ref, body)

rows = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'wires.csv'))))
printed = {w['cable']: f"{w['cable'].split('#')[0]} {w['colour']}" for w in rows if not w['cable'].startswith('?')}
def prints(svg, cable):   # a wire label, tag or caption starts its text with '<no> <colour>'; a mention inside a note does not
    return re.search(r'>' + re.escape(printed[cable]) + r'(?=[\s:<])', svg) is not None

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}mm" height="{PH}mm" viewBox="0 0 {PW} {PH}">',
         f'<rect width="{PW}" height="{PH}" fill="#fff"/>']
missing, seen = [], {}
for i, (key, title) in enumerate(ORDER):
    x, y = X0 + (i % 3) * W * S, (i // 3) * H * S
    p = os.path.join(OUT, f'{key}.svg')
    if os.path.exists(p):
        body = scope_ids(inner(p), key)
        seen[key] = body
    else:
        missing.append(key)
        body = (f'<g font-family="Helvetica, Arial, sans-serif"><rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="#fafafa" '
                f'stroke="#bbb" stroke-dasharray="4 3"/><text x="{W / 2}" y="{H / 2}" font-size="8" text-anchor="middle" fill="#999">{title}: to come</text></g>')
    parts.append(f'<svg x="{x}" y="{y}" width="{W * S}" height="{H * S}" viewBox="0 0 {W} {H}">'
                 f'<g font-family="Helvetica, Arial, sans-serif">{body}</g></svg>')   # the sheet's own <svg> (and its font) is stripped

# NOT_DRAWN is the footer's word for what the sheets leave off: check it against what they print.
warn = [f'{c} is printed on the {k} sheet but counted as left off' for c in sorted(NOT_DRAWN) for k, b in seen.items() if prints(b, c)]
if not missing:
    warn += [f'{c} is printed on no sheet but not counted as left off' for c in printed if c not in NOT_DRAWN
             and not any(prints(b, c) for b in seen.values())]
for w in warn: print('warning:', w, file=sys.stderr)
if missing: print('placeholders for:', ', '.join(missing), '(the poster is not finished: do not commit it yet)', file=sys.stderr)

wires = [w for w in rows if w['cable'] not in NOT_DRAWN]
fitted_off = sum(w['cable'] in NOT_FITTED for w in rows)
jumper = next((w for w in rows if w['cable'] == JUMPER), None)
st = Counter(w['status'] for w in wires)
left_off = []
if fitted_off: left_off.append(f'{fitted_off} cables of parts not fitted or probably not fitted')
if jumper: left_off.append(f'the {JUMPER} {jumper["colour"]} {jumper["mm2"]} jumper, which only a car without start inhibitor relay 89 has')
ty = 3 * H * S + 11
# Source (not printed; our diagram is canonical): Saab Service Manual 1969-1974, diagram p. 371-22/23 (RHD 1974),
# with the injection detail 371-42/43 and the automatic detail 371-44.
parts.append(f'<g font-family="Helvetica, Arial, sans-serif"><text x="{X0 + 8}" y="{ty}" font-size="8" font-weight="bold">Saab 99 LE, model 1974: wiring redrawn</text>'
             f'<text x="{X0 + 185}" y="{ty}" font-size="4.2" fill="#444">'
             f'Wires: {st["traced"] + st["traced+text"]} traced, '
             + (f'{st["open"]} not traced yet, ' if st['open'] else '') +      # only while something is still dashed
             (f'{st["stub"]} end on the diagram, ' if st['stub'] else '') +     # only when a sheet draws a stub
             (f'{st["car"]} checked on the car. ' if st['car'] else 'none checked on the car yet. ')
             + (f'Left off: {", and ".join(left_off)}. ' if left_off else '') +
             f'Colour codes are Swedish (GL gul = yellow, SV svart = black, VT vit = white). Generated {datetime.date.today():%d %B %Y}.</text></g>')
parts.append('</svg>')
open(os.path.join(OUT, 'poster.svg'), 'w').write('\n'.join(parts))
print('wrote', os.path.join(OUT, 'poster.svg'))

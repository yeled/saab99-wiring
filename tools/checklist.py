#!/usr/bin/env python3
"""Write docs/car-checklist.md: checks to do on the car, plus every wire not traced yet."""
import csv, os
ROOT = os.path.join(os.path.dirname(__file__), '..')
checks = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'checks.csv'))))
wires = list(csv.DictReader(open(os.path.join(ROOT, 'data', 'wires.csv'))))
o = ['# Saab 99 Turbo (1979): checks on the car', '',
     'Tick each item, note what you found in `data/checks.csv` (the `result` column), or just tell Claude',
     'the check ID and what you saw. Anything confirmed becomes `car` in `wires.csv` and gets a ✓ on the sheets.', '',
     'Meter checks need the battery connected: probe carefully and don’t bridge terminals.', '']
area = None
for c in checks:
    if c['area'] != area:
        area = c['area']; o += ['', f'## {area}', '']
    done = 'x' if c['result'].strip() else ' '
    cab = f" _Cables: {c['cables']}._" if c['cables'] else ''
    res = f" **Found:** {c['result']}" if c['result'].strip() else ''
    o.append(f"- [{done}] **{c['id']}** ({c['how']}): {c['check']}{cab}{res}")
openw = [w for w in wires if w['status'] == 'open']
o += ['', f'## Appendix: wires not traced yet ({len(openw)})', '', '| Cable | Colour | mm² | From | To | Note |', '|---|---|---|---|---|---|']
for w in openw:
    o.append(f"| {w['cable']} | {w['colour'] or '?'} | {w['mm2'] or '?'} | {w['from']} | {w['to']} | {w['notes']} |")
os.makedirs(os.path.join(ROOT, 'docs'), exist_ok=True)
out = os.path.join(ROOT, 'docs', 'car-checklist.md')
open(out, 'w').write('\n'.join(o) + '\n'); print('wrote', out, f'({len(checks)} checks, {len(openw)} open wires)')

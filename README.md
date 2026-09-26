# Saab 99 Turbo (1979) wiring, redrawn

A clean, printable redraw of the factory wiring diagram for the 1979 Saab 99
Turbo, built from the Saab Service Manual 1975–1980 (diagram p. 371-28/29,
PDF p. 406–407).

It describes one car, a 3-door Combi Coupé, and is checked against it. The
1979 Turbo diagram draws the saloon's rear lights, so the rear (four-bulb
lights, two separate number-plate lamps) comes from the manual's 1977/78
Turbo Combi Coupé diagrams instead.

The wiring lives in CSV files; the drawings are generated from them. Change a
wire's status in the CSV and the sheet updates.

## Layout

| Path | What it is |
|---|---|
| `data/components.csv` | Component legend from p. 371-28: number, name, grid square |
| `data/wires.csv` | One row per cable: number, colour, mm², from, to, status, evidence, notes |
| `data/fuses.csv` | One row per fuse: rating, supply bar, status, notes |
| `data/connectors.csv` | Pin maps for in-line connectors: both sides of each pin |
| `data/checks.csv` | Things to verify on the car; fill in `result` as you go |
| `data/internals.csv` | What the manual prints inside each part (relay coils and contacts, switch blades, bulbs and filaments, fuses): one row per element, with rest state, confidence and the book photo it was read from |
| `tools/checklist.py` | Writes `docs/car-checklist.md` from `checks.csv` plus every untraced wire |
| `sheets/lighting.py` | Renders the lighting sheet to `out/lighting.svg` (A3 landscape) |
| `sheets/power.py` | Renders the power distribution sheet to `out/power.svg` (A3 landscape) |
| `sheets/ignition.py` | Renders the ignition, starting and fuel injection sheet to `out/ignition.svg` |
| `sheets/instruments.py` | Renders the instruments and warning lamps sheet to `out/instruments.svg` |
| `sheets/radio.py` | Renders the radio, speakers and accessory feeds sheet to `out/radio.svg` |
| `sheets/signals.py` | Renders the indicators, hazards, brake and reversing lights sheet to `out/signals.svg` |
| `sheets/wipers.py` | Renders the wipers and washers sheet to `out/wipers.svg` |
| `sheets/climate.py` | Renders the radiator fan, heater fan and heated rear window sheet to `out/climate.svg` |
| `sheets/interior.py` | Renders the interior lights, seat heating and seat belt sheet to `out/interior.svg` |
| `sheets/poster.py` | Composes every sheet onto one A0 landscape poster, `out/poster.svg` (run it last) |
| `sheets/common.py` | Drawing helpers shared by the sheets, including the symbols for parts' insides (coil, contact, blade, resistor, diode, fuse, twin-filament bulb) |
| `tools/trace.py` | Follows a wire on the scanned page, and makes gridded crops |
| `tools/follow.py` | Follows wires through corners, prints where they end, and makes contact sheets |
| `source/` | Not in git: put the scanned manual (`1980-99-service-manual.pdf`) and book photos (`photos/`) here |

Terminals are written `component:terminal`, e.g. `8:56a` is lighting relay 8,
terminal 56a. A wire whose cable number hasn't been read yet gets an id
starting with `?` (e.g. `?D+`) and a blank colour; it is drawn thin and grey.
Where the manual prints the same number on two different wires, the second
gets a `#` suffix in its id (e.g. `32#earth`); the sheets print only the number.

Line width follows the cable's size (mm²): 0.75 is drawn well under 1.0 and
2.5 about twice as wide, flattening off above that so the 4.0 feeds and the
16 mm² battery cable stay lines, not bands (`WIDTH` in `sheets/common.py`).
Each sheet's legend shows the scale.

## Inside the parts

Relays, switches, lamps and the fuse box are drawn with their insides as the
manual prints them, with contacts in their printed rest position. Black is
read clearly off the book photos; grey inside a part means probably (printed
unclearly, or inferred); what can't be read isn't drawn. Mechanical links from
a coil to its contacts are thin grey dashes. `data/internals.csv` lists every
element with its evidence.

## Status values in `wires.csv`

| Status | Meaning | On the sheet |
|---|---|---|
| `traced` | Followed on the scan; cable number read on the traced line | solid |
| `traced+text` | As above; terminal name taken from the manual's text | solid |
| `open` | Not traced yet | dashed |
| `stub` | Drawn in the manual but ends there (accessory tap) | open circle |
| `car` | Checked on the car | solid, ✓ after the label |

In `fuses.csv`, `car` means the fuse's position and rating were checked on the
car; the fuse label then gets a ✓. Which bar a fuse sits on still comes from
the manual.

`evidence` gives the cable label's position in pixels on PDF p. 407 rendered
at 400 dpi, so any row can be re-checked with a crop.

## Commands

Needs Python 3 with numpy and Pillow, plus poppler's `pdftoppm`
(macOS: `brew install poppler`).

    python3 sheets/lighting.py
    python3 sheets/power.py
    python3 sheets/ignition.py
    python3 sheets/instruments.py
    python3 sheets/radio.py
    python3 sheets/signals.py
    python3 sheets/wipers.py
    python3 sheets/climate.py
    python3 sheets/interior.py
    python3 sheets/poster.py
    python3 tools/checklist.py

    python3 tools/trace.py render --pdf ~/Downloads/1980-99-service-manual.pdf --page 407
    python3 tools/trace.py crop 4250 1930 4600 2160 --out relay8.png
    python3 tools/trace.py trace 4479 2125 down --out overlay.png

`render` caches the page in `cache/` (ignored by git). `trace` prints where
the wire turns and ends and writes an overlay. It steps over crossings and
bridges the scan's fold gap (x ≈ 4650–4710), but it can jump to the wrong
line where text touches a wire, so confirm every result against the cable
label before adding it to `wires.csv`.

## Licence

GPL-3.0: see `LICENSE`. The wiring itself is taken from the Saab Service Manual 1975–1980.

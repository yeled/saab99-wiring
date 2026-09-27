# Saab 99 wiring, redrawn

Clean, printable redraws of the factory wiring diagrams for Saab 99s, one folder per car.
Each is built from the Saab service manual and checked against the actual car. The wiring
lives in CSV files, and the A3 sheets and A0 poster are generated from them.

| Folder | Car | State |
|---|---|---|
| [`turbo-1979/`](turbo-1979/README.md) | 1979 Saab 99 Turbo, 3-door Combi Coupé, UK, right-hand drive | v1.0: complete as a drawing of the 1979 diagram; being checked on the car |
| `le-1974/` | 1974 Saab 99 LE, 4-door, automatic, D-Jetronic fuel injection, UK, right-hand drive | Started |

## Layout

| Path | What it is |
|---|---|
| `lib/wiring.py` | Drawing helpers shared by every car: wires drawn by cable size, tags, dots, legends, and the symbols for parts' insides |
| `<car>/data/` | The car's wiring as CSV: wires, fuses, connectors, components, parts' insides, checks on the car |
| `<car>/sheets/` | One script per A3 sheet, plus `poster.py`; `common.py` points `lib/wiring.py` at the car's folder |
| `<car>/out/` | The generated SVGs |
| `<car>/tools/` | Tools for that car's scanned diagram (following wires, crops) and its checklist |

Build a car's sheets from its folder, poster last, e.g.

    cd turbo-1979
    for s in lighting power ignition instruments radio signals wipers climate interior poster; do python3 sheets/$s.py; done

Needs Python 3; the tools need numpy and pillow, the PDF export cairosvg, and poppler for page renders.

## Licence

GPL-3.0; see `LICENSE`.

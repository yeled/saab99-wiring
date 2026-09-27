# Saab 99 LE (1974) wiring, redrawn

One of the cars in this repo (see the [top-level README](../README.md)): a 1974 Saab 99 LE,
4-door saloon, automatic transmission, Bosch D-Jetronic fuel injection, UK, right-hand drive.

**State: started.** The sources in the Saab 99 Service Manual 1969–1974 have been mapped; the
wiring is not traced yet.

## Sources

| Page | What |
|---|---|
| 371-22/23 | Wiring diagram, right-hand-drive car, model 1974 (legend and drawing S 4002): the base |
| 371-42/43 | Details for the injection engine, models 1973–1974 (legend and drawing S 3783): the D-Jetronic loom |
| 371-44 | Details for cars with automatic transmission, model 1974 (drawing S 3981): start inhibitor and reversing lights |
| 364-1 to 364-5, 363-6/7 | Relays, switches and the lighting relay; headlamp wipers |
| 234-x | The D-Jetronic chapter: harness and plug pin-outs |

## Layout

The same as the 1979 Turbo's (see [its README](../turbo-1979/README.md)): `data/` holds the wiring as
CSV, `sheets/` one script per A3 sheet, `out/` the SVGs, and `tools/` the page tools for this manual.
`tools/trace.py` renders the 1974 diagram pages upright (they are scanned rotated) and caches them.

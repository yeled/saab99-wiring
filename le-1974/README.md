# Saab 99 LE (1974) wiring, redrawn

One of the cars in this repo (see the [top-level README](../README.md)): a 1974 Saab 99 LE,
4-door saloon, automatic transmission, Bosch D-Jetronic fuel injection, UK, right-hand drive.

Its chassis is a 1973 (model year 1973). It is drawn from the 1974 diagrams; wherever the car
turns out to differ, the difference is compared with the 1973 drawings. Fitted: seat heating and
cigarette lighter; the clock has been replaced by an aftermarket rev counter; no headlamp wipers,
heated rear window or radio.

**State: drawn, being checked on the car.** All 206 cables of the 1974 diagram and its injection
and automatic details are traced, each reading re-checked, and cross-checked against photographs
of a printed copy of the manual. Nine A3 sheets and an A0 poster are drawn from the data:

| Sheet | What |
|---|---|
| `power` | Battery, alternator and regulator, ignition switch and its relay, the fuse box with every fuse's loads, horn |
| `ignition` | Coil, ballast resistor, distributor, starter; the automatic's start inhibitor relay and switch |
| `injection` | D-Jetronic: control unit, injectors, sensors, throttle switch, trigger contacts, master and pump relays, fuel pump, cold start |
| `lighting` | Lighting relay, dimmer/flasher stalk, light switch, headlamps, parking, tail and number-plate lights |
| `instruments` | Combination instrument and its senders, panel lighting, cigarette lighter |
| `signals` | Indicators, hazards, stop and reversing lights |
| `wipers` | Windscreen wipers and washer |
| `climate` | Heater fan and radiator fan |
| `interior` | Dome and trunk lights, door contacts, seat heating |

Parts this car doesn't have (headlamp wipers, the clock, the carburettor's choke lamp) are left
off the sheets with a note; their wires stay in `data/`.

Build from this folder, poster last:

    for s in power ignition injection lighting instruments signals wipers climate interior poster; do python3 sheets/$s.py; done

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

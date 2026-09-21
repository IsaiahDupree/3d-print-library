# Vehicle A/C Diagnostic Enclosure — Design Evolution V1–V4 (Historical Prototypes)

Printables listing: added at publication · [Request a design](https://github.com/IsaiahDupree/3d-print-library/issues/new/choose) · [More printable designs](https://github.com/IsaiahDupree/3d-print-library)

Four superseded, original, AI-assisted design studies by Isaiah Dupree that led to the published [Vehicle A/C Diagnostic Sensor Enclosure V4](https://www.printables.com/model/1840792-vehicle-ac-diagnostic-sensor-enclosure-v4-prototyp) and the Tapered Fit Gauge V5.

They are published for traceability and learning: each folder shows what the design assumed at the time, what was validated in CAD, and what later measurements proved wrong. **None of these revisions is a recommended build.** Nothing here has been printed in final form or fit-verified on a vehicle.

## What is inside

### V1 — first parametric package (`v1/`)

- 200 × 98 × 50 mm body with a rear mounting flange (two Ø9 mm holes on 50 mm centers), gasket groove, and eight-screw lid.
- Removable interface-carrier blank, UPS clearance guard, and a panel fit coupon for the connector, USB-C, power-switch, and vent cutouts.
- A cabin/service-tool concept. Its hood and vehicle clearances are not adequate for a final installation.

### V2 — standing print and electronics tray (`v2/`)

- Axial-extrusion shell printed standing on a FLSUN V400: 60 × 126 mm footprint, 224.8 mm tall.
- Removable right I/O panel with 42 mm connector spacing, a raised removable electronics tray on rails, and a four-slot cable clamp bar.
- Process coupons for the cap interface, tray rails, horizontal wall holes, and a vehicle-mount fit gauge.

### V3 — firewall-slot fit study RC1 (`v3/`)

- 175 W × 88 H × 60 D mm candidate scaled from photographs, with a round-plus-slot mount on 50 mm centers.
- Removable vertical backplane plus an upper carrier, a recessed right cap with two pigtail glands, and an engine-facing service lid with a silicone-cord groove.
- Empty clearance cage, depth feeler, I/O witness, bolt coupon, and drill template for a stationary fit check.

### V4 — hood-flange fit study (`v4/`)

- Uses measured envelope inputs instead of photo scaling: a 5 mm hood datum above the bolt head, 150 mm of lower clearance, and a 50.53 mm mount-pitch candidate.
- Single removable backplane with no battery or UPS, three pigtail glands (HIGH, LOW, POWER), and a ten-screw lid.
- Adds a standing bridge coupon to qualify painted support-on-model before printing the tall body.

## What changed between versions

- **V1 → V2:** printability on a delta printer, a serviceable tray, and wider connector spacing.
- **V2 → V3:** moved from a cabin tool to a firewall slot, prohibited batteries under the hood, and replaced panel connector barrels with small glands.
- **V3 → V4:** replaced photo-scaled dimensions with measurements, removed the UPS, and added a fused power gland and a support-qualification coupon.
- **V4 → V5:** stopped designing enclosures and built a tapered fit gauge to measure the slot first.

## Status and safety

These are historical prototypes. Do not install them in a vehicle.

- No printed part may contain refrigerant pressure. Hoses, couplers, fittings, pressure transducers, and temperature probes must stay external, rated hardware.
- Do not install or charge batteries or loose lithium cells under the hood.
- No printed polymer may enter a vehicle bolt clamp path. The drill templates and fit gauges are not brackets.
- Raw FDM enclosures are not waterproof, flame-rated, vibration-qualified, or IP-rated.

## Printing a coupon

The coupons and gauges are the most reusable parts. Treat PLA and PETG as fit-check materials only, slice every file yourself, and inspect every layer. Each folder's `DESIGN_NOTES.md` explains the print orientation, brims, and the measurements each coupon is meant to confirm; V4 also includes `PRINTING.md`.

## Files

Each folder contains STEP and STL exports, the FreeCAD assembly, the BOM, design notes, and CAD validation reports. V2 through V4 also include their parametric FreeCAD generator and Blender render scripts, which now write to a relative `out` folder. Reference-only component and keep-out solids are omitted.

## License

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. See [LICENSE.md](LICENSE.md).

Full source mirror and future revisions: https://github.com/IsaiahDupree/3d-print-library

Design requests: https://github.com/IsaiahDupree/3d-print-library/issues/new/choose

## Isaiah Dupree brand + GitHub QR coupon

`isaiah-dupree-github-qr-branding.stl` is an optional, separately printable process coupon. It carries the ISAIAH DUPREE block signature and a deterministic QR code for https://github.com/IsaiahDupree/3d-print-library. Keep it separate from fitted or load-bearing model surfaces; contrast-fill the recessed cells and verify the code scans before display.

## Orion / ANSYS engineering screen

`ac-enclosure-v4-orion-ansys-screening-report.pdf` documents a three-point ANSYS MAPDL mesh sweep of the exact public V4 body STEP under an idealized 250 N rim-compression load. The finest point reported 9.712 MPa peak averaged von Mises stress and 0.8198 mm maximum displacement. This is a nominal isotropic PETG screening study, not physical qualification or approval for vehicle installation.

## Download

| File | Size | SHA-256 |
|---|---:|---|
| [`files/ac-diagnostic-enclosure-design-evolution-v1-v4.zip`](files/ac-diagnostic-enclosure-design-evolution-v1-v4.zip) | 3.8 MB | `568eab0a0d17b8be…` |
| [`files/ac-enclosure-v4-orion-ansys-screening-report.pdf`](files/ac-enclosure-v4-orion-ansys-screening-report.pdf) | 212.2 KB | `eacebca1862300a6…` |
| [`files/isaiah-dupree-github-qr-branding.stl`](files/isaiah-dupree-github-qr-branding.stl) | 841.3 KB | `2181b95577f94e60…` |

Full hashes are in [RELEASE.json](RELEASE.json). Release history is in [RELEASE_NOTES.md](RELEASE_NOTES.md).

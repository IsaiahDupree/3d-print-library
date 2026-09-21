# Vehicle A/C Diagnostic Sensor Enclosure V4

An original, AI-assisted design by Isaiah Dupree for packaging an ESP32-based vehicle A/C diagnostic logger. This release combines the standing-print enclosure body, removable electronics backplane, service lid, four-entry sensor-pigtail cap, fitment gauges, and process coupons.

[Printables model](https://www.printables.com/model/1840792-vehicle-ac-diagnostic-sensor-enclosure-v4-prototyp) · [Request a design](https://github.com/IsaiahDupree/3d-print-library/issues/new/choose) · [More printable designs](https://github.com/IsaiahDupree/3d-print-library)

## Four sensor channels

- HIGH pressure
- HIGH temperature
- LOW pressure
- LOW temperature

There is deliberately no fifth cable hole. Power architecture remains outside this revision.

## Download

The ZIP in [`files/`](files/) contains 48 hash-audited members: printable STL exports, STEP sources, the FreeCAD assembly, the parametric generator, BOM, measurement worksheet, design notes, and printing guidance. The five STL files shown individually on Printables are mirrored beside the ZIP for direct access. The preview renders in [`images/`](images/) are the same public assets used for the Printables listing.

## Prototype status

This is a dimensional prototype and fit-study release—not a qualified permanent under-hood product. The vehicle-hole candidate is approximately 50.53 mm on center and shifted toward the right edge, but vehicle fitment, hood sweep, bolt function and torque, cable hardware, temperature, water, vibration, and material suitability still require physical verification.

No printed part contains refrigerant pressure. Refrigerant hoses, couplers, fittings, pressure transducers, and temperature probes must remain appropriately rated external hardware. Do not place printed polymer in the OEM bolt clamp stack. The separate Raspberry Pi/HAT battery plate is bench-only; do not install or charge loose lithium cells under the hood.

## Recommended print sequence

1. Print the bolt, board-hole, insert, gland, QR/branding, wall-hole, and bridge coupons.
2. Measure every purchased fastener, insert, connector, gland, PCB revision, and cable bend radius.
3. Print the empty clearance cage and perform a cold, engine-off hood-clearance test using soft clay or crushable foam.
4. Slice the full parts only after the coupons and clearances pass.

The FLSUN V400 preparation evidence used 0.20 mm layers, 100% infill, five walls (2.2 mm), and six top/bottom layers. Runtime factors `M220 S50` and `M221 S80` were used for the tested preparation copy. These are Klipper percentages and do not replace material or extrusion calibration.

## Licence

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. See [LICENSE.md](LICENSE.md).

## Integrity

See [RELEASE.json](RELEASE.json) for the archive and preview SHA-256 values. The release archive SHA-256 is:

`445f837e3168283956f9829b0f80b63082e74c109de58418bc0b90009fa0c56d`

# Dumbbell Rack Joint Fit Coupons — Unloaded Prototypes

Original, AI-assisted design by Isaiah Dupree. Two small gauges are the first physical fit step in a modular dumbbell carrier project. This release contains fit coupons only; the full rack remains an unmeasured, unqualified CAD study. No load or lifting capacity is claimed.

## Files and orientation

Print one of each STL at 100% scale with the flat base on the bed and holes upward. Editable STEP files are included. View the holed face with the unique clipped corner at bottom left; diameters increase from left to right.

| Coupon | Envelope | Stations |
|---|---|---|
| insert_coupon | 120 × 28 × 18 mm | Five blind holes: 6.8, 7.0, 7.2, 7.4, 7.6 mm diameter; each 9 mm deep |
| bolt_coupon | 75 × 60 × 16 mm | Row nearest clipped edge: 6.4, 6.6, 6.8 mm through holes. Far row: 8.0, 8.2, 8.4 mm through holes. |

The first range investigates a candidate M5 heat-set insert interface; M5 describes the screw thread, not a universal insert outside diameter. Select an actual supplier insert and its installation drawing before testing. The smaller through-hole row investigates M6 screw clearance; the larger row investigates an unselected compression-sleeve OD. These sizes do not promise compatibility with every insert or sleeve.

## Printing and recording fit

A starting study process is a 0.4 mm nozzle, 0.20 mm layers, six or more walls and greater than 50% infill, with solid material around the tested inserts. Use a properly tuned material profile. PETG is the proposed mechanical prototype material; exact filament, process and fit remain unverified. No printer-specific G-code is included in this public release.

Record printer, nozzle, filament grade/lot, drying, layer/extrusion settings, specimen ID, measured hole sizes, actual hardware SKU and installation results. Preserve the clipped-corner orientation in photos. Reject cracks, loose inserts and bottomed screws. A fit result does not establish a structural load rating.

## Evidence

Authenticated Orion CAD job mdl_065753e6f4e2430a generated the actual STEP/STL payloads and this render. Its complete development audit passed 156 CAD checks. The coupon-specific export checks are mirrored in evidence/coupon-cad-checks.json: valid single solids, STEP round trips, watertight positive STL meshes, mesh/solid volume agreement, and circular V400 envelope checks. The preview is a CAD render, not a photograph of a print.

The V400 has a nominal circular Ø300 mm bed. These two individual coupons pass a conservative centered bounding-box check within the project’s provisional Ø280 mm circle with a 5 mm brim. Slicer toolpaths and the actual machine still need review.

Physical printing, hardware fit, insertion torque, creep, strength and loaded transport have not been validated. The main carrier needs actual dumbbell measurements and purchased reinforcement/restraints before those claims can be assessed.

## Provenance and licence

No GrabCAD or other third-party model geometry is included. Native reference downloads were retained privately for layout research. This original public package is CC BY-NC-SA 4.0; identify Isaiah Dupree, link this release, and describe modifications when sharing a remix.

[GitHub source-and-evidence mirror](https://github.com/IsaiahDupree/3d-print-library/tree/main/models/dumbbell-rack-joint-fit-coupons)

[Printer file/history audit](https://github.com/IsaiahDupree/3d-print-library/tree/main/printer-audits/2026-10-17)

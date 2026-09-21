# Vehicle Firewall-Slot Tapered Fit Gauge V5

Printables listing: added at publication · [Request a design](https://github.com/IsaiahDupree/3d-print-library/issues/new/choose) · [More printable designs](https://github.com/IsaiahDupree/3d-print-library)

An original, AI-assisted measurement-tool set by Isaiah Dupree for checking the proposed firewall-slot envelope of a vehicle A/C diagnostic electronics enclosure before another full enclosure is printed.

This is a **temporary, nonstructural fit gauge**—not a permanent vehicle bracket, enclosure, or engine-bay component. Use it only with the vehicle stationary, engine cold and off, and hood independently supported. Install temporary matching hardware hand-snug with no clamp torque, supervise the entire check, and remove every printed part before starting the engine or driving.

## What is included

- `tapered_profile_coupon.stl` — checks the 126 mm shoulder, 76 mm lower width, and 135 mm drop;
- `adapter_drill_template.stl` — checks the round/slot two-hole pattern on approximately 50.53 mm centers;
- `lateral_offset_indicator.stl` — compares -10, 0, and +10 mm lateral relationships;
- `depth_feeler_comb_45_50_55_60.stl` — checks the proposed depth envelope before the cage;
- `clearance_whisker_coupon.stl` — verifies the 5 mm static and 10 mm moving-loom witness features after printing;
- `tapered_clearance_cage.stl` — a low-material 60 mm-depth final stationary fit trial;
- STEP sources, FreeCAD assembly, parametric generator, BOM, detailed design notes, print guide, and measurement worksheet.

The two vehicle-hole features are mirrored about their own shifted midpoint. In the installed-body coordinate system they are centered at X = +6.735 mm and +57.265 mm, preserving the approximately 50.53 mm pitch while shifting the pair toward the right side. The left feature is a round 9.2 mm hole; the right is a horizontal 14.0 × 9.2 mm slot. These remain measurement-gated candidates.

## Safe test order

1. Print and measure the profile, whisker, drill-template, lateral-offset, and depth-feeler coupons.
2. Confirm the OEM fastener purpose, thread, pitch, usable engagement, head diameter, and hood clearance. Never force a bolt through a print.
3. Hold the drill template against the panel without tightening and verify both features.
4. Install only the empty clearance cage for a stationary, cold-engine check. Use soft removable clay or crushable foam as a contact witness and lower the hood slowly by hand.
5. Check the hood, hinge, gas strut, fuse/relay-box service sweep, reservoir access, fixed obstacles, and moving wiring loom along the full 60 mm depth.
6. Photograph each viable position with a scale visible, record the worksheet, and remove the gauge before driving.

No electronics, batteries, UPS hardware, wiring, cable glands, sensors, refrigerant hoses, or pressure hardware belong in this gauge. No printed polymer may enter the permanent OEM-bolt clamp load path. Any final bracket requires a directly measured and engineered metal adapter/spacer stack.

## Printing

Start with 0.20 mm layers, a 0.4 mm nozzle, four walls, five top/bottom layers, and 20% gyroid infill. Print the flat coupons flat with a 6 mm brim. Print the cage with its firewall X/Z face on the bed and the installed-depth direction upward, using a 12 mm brim. PETG or ASA is preferable to PLA for a brief controlled engine-bay fit check, but no material is qualified for permanent under-hood use.

Inspect every layer in the slicer, especially the cage rails, diagonals, breakaway witnesses, bridge/gusset pairs, and cage-to-adapter overlap. Measure the printed holes, slot, pitch, widths, drop, feelers, whiskers, and cage depth before approaching the vehicle.

Full source mirror and future revisions: https://github.com/IsaiahDupree/3d-print-library

Design requests: https://github.com/IsaiahDupree/3d-print-library/issues/new/choose

## Isaiah Dupree brand + GitHub QR coupon

`isaiah-dupree-github-qr-branding.stl` is an optional, separately printable process coupon. It carries the ISAIAH DUPREE block signature and a deterministic QR code for https://github.com/IsaiahDupree/3d-print-library. Keep it separate from fitted or load-bearing model surfaces; contrast-fill the recessed cells and verify the code scans before display.

## Download

| File | Size | SHA-256 |
|---|---:|---|
| [`files/adapter_drill_template.stl`](files/adapter_drill_template.stl) | 21.6 KB | `5aedcbfa7a219c0c…` |
| [`files/clearance_whisker_coupon.stl`](files/clearance_whisker_coupon.stl) | 3.8 KB | `399cc1837987f97f…` |
| [`files/depth_feeler_comb_45_50_55_60.stl`](files/depth_feeler_comb_45_50_55_60.stl) | 6.9 KB | `60e917023734625d…` |
| [`files/isaiah-dupree-github-qr-branding.stl`](files/isaiah-dupree-github-qr-branding.stl) | 841.3 KB | `2181b95577f94e60…` |
| [`files/lateral_offset_indicator.stl`](files/lateral_offset_indicator.stl) | 3.0 KB | `1c46f03713ecd583…` |
| [`files/tapered_clearance_cage.stl`](files/tapered_clearance_cage.stl) | 380.1 KB | `795991ed985eee50…` |
| [`files/tapered_profile_coupon.stl`](files/tapered_profile_coupon.stl) | 1.1 KB | `b012feea789b2231…` |
| [`files/vehicle-firewall-slot-tapered-fit-gauge-v5.zip`](files/vehicle-firewall-slot-tapered-fit-gauge-v5.zip) | 676.1 KB | `bac16e2e82652908…` |

Full hashes are in [RELEASE.json](RELEASE.json). Release history is in [RELEASE_NOTES.md](RELEASE_NOTES.md).

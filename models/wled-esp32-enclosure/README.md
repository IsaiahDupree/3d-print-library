# WLED ESP32 Controller Enclosure — Vented Tower

Printables listing: added at publication · [Request a design](https://github.com/IsaiahDupree/3d-print-library/issues/new/choose) · [More printable designs](https://github.com/IsaiahDupree/3d-print-library)

An original three-part enclosure by Isaiah Dupree for a small ESP32 board running [WLED](https://kno.wled.ge/), the open-source LED-strip controller firmware. The board mounts on a plate that slides into a vented tower, and a screw-on front panel carries the external connectors.

## Parts

- `box5.stl` — 42 × 70.5 × 130 mm vented tower with diagonal side slots and internal guide rails.
- `Slide4.stl` — 62.5 × 124.5 × 7.6 mm slide-in board plate with four standoffs.
- `front4.stl` — 42 × 70.5 × 6 mm front panel with corner screw holes, a rectangular opening for a 3.81 mm pluggable terminal block, and an obround opening for a USB-C panel-mount jack.
- `wled_esp32.stp` — STEP export of the box, front panel, and slide for editing.

## Before you print

The connector openings and standoffs were sized for this build's specific board, terminal block, and USB-C jack. Measure your own board's hole pattern and your connectors before printing, and print the front panel first to check the cutouts. This release does not document a completed print or a measured fit with purchased parts.

## Printing

- Print the tower standing upright; the diagonal slots are designed as self-supporting openings, but inspect them in your slicer.
- Print the slide plate and front panel flat.
- PETG is a good default for an electronics box that may sit near warm power supplies; PLA is fine for a quick fit check.

## Electrical safety

The printed parts are not a fire enclosure. Fuse the LED power supply, size the wiring for your strip's current, keep mains wiring out of this box, and do not leave high-current LED loads unattended until you have verified temperatures.

## Design notes

The project was modeled in ANSYS SpaceClaim. Downloaded component models of the terminal block and USB-C jack were used only as local references for sizing openings; no third-party geometry is included in these files.

## License

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. See [LICENSE.md](LICENSE.md).

Full source mirror and future revisions: https://github.com/IsaiahDupree/3d-print-library

Design requests: https://github.com/IsaiahDupree/3d-print-library/issues/new/choose

## Isaiah Dupree brand + GitHub QR coupon

`isaiah-dupree-github-qr-branding.stl` is an optional, separately printable process coupon. It carries the ISAIAH DUPREE block signature and a deterministic QR code for https://github.com/IsaiahDupree/3d-print-library. Keep it separate from fitted or load-bearing model surfaces; contrast-fill the recessed cells and verify the code scans before display.

## Download

| File | Size | SHA-256 |
|---|---:|---|
| [`files/Slide4.stl`](files/Slide4.stl) | 71.0 KB | `ccb5962588e1550a…` |
| [`files/box5.stl`](files/box5.stl) | 433.5 KB | `240f2721bd85a861…` |
| [`files/front4.stl`](files/front4.stl) | 217.1 KB | `220bc6e0b871b03e…` |
| [`files/isaiah-dupree-github-qr-branding.stl`](files/isaiah-dupree-github-qr-branding.stl) | 841.3 KB | `2181b95577f94e60…` |
| [`files/wled-esp32-enclosure.zip`](files/wled-esp32-enclosure.zip) | 462.5 KB | `cf87754d43628f26…` |

Full hashes are in [RELEASE.json](RELEASE.json). Release history is in [RELEASE_NOTES.md](RELEASE_NOTES.md).

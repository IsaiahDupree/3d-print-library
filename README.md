# Isaiah Dupree 3D Print Library

Practical, measured 3D-printed tools, enclosures, mounts, adapters, and workshop solutions by Isaiah Dupree.

[Printables profile](https://www.printables.com/@Isaiah_Dupre_1141044) · [GitHub profile](https://github.com/IsaiahDupree) · [Request a design](https://github.com/IsaiahDupree/3d-print-library/issues/new/choose)

## About me

I design useful parts around real fitment constraints, document how they are developed and tested, and publish the information needed to reproduce them. My work focuses on vehicle and electronics enclosures, mounting adapters, fit gauges, workshop tools, and practical replacement parts.

## Models

The [`models/`](models/) directory contains eight reviewed releases: three published on Printables and five prepared for publication. The published models are [Vehicle A/C Diagnostic Sensor Enclosure V4](models/vehicle-ac-diagnostic-sensor-enclosure-v4/), [Vehicle Firewall-Slot Tapered Fit Gauge V5](https://www.printables.com/model/1853082-vehicle-firewall-slot-tapered-fit-gauge-v5), and [Dumbbell Rack Joint Fit Coupons](https://www.printables.com/model/1881340-dumbbell-rack-joint-fit-coupons-unloaded-prototype).

The collection includes:

- [Vehicle Firewall-Slot Tapered Fit Gauge V5](models/vehicle-firewall-slot-tapered-fit-gauge-v5/) — a safe, low-material measurement sequence before committing to another enclosure;
- [A/C Diagnostic Enclosure Design Evolution V1–V4](models/ac-diagnostic-enclosure-design-evolution-v1-v4/) — historical prototypes, lessons learned, and an Orion/ANSYS screening report;
- [WLED ESP32 Controller Enclosure](models/wled-esp32-enclosure/) — a vented tower, sliding board plate, and serviceable connector panel;
- [Twin Flame Desk Sign](models/twin-flame-sign-remix/) — a credited, layered multi-part remix;
- [Scrunchie Tree](models/scrunchie-holder-remix/) — a credited tall four-peg remix;
- [Nanosaur Track Ring](models/nanosaur-tracks-mod/) — a credited larger-diameter track modification;
- [Dumbbell Rack Joint Fit Coupons](models/dumbbell-rack-joint-fit-coupons/) — published unloaded insert/bolt diameter gauges, with verified CAD and no physical fit or load claim. The four CAD downloads are on Printables; the complete ZIP and evidence are on GitHub.

Every model folder contains:

- reviewed downloadable design files;
- a direct listing link when published on Printables;
- version and SHA-256 information;
- printing and assembly guidance;
- testing and fitment status;
- photographs or renders approved for public use;
- the exact licence and remix attribution for that model.

Local drafts, private paths, credentials, printer configuration, paid/member-only content, and models without redistribution permission are excluded.

The aggregate authorship audit and the distinction between created, remixed, downloaded, and unknown files are documented in [PROVENANCE-INVENTORY.md](PROVENANCE-INVENTORY.md). The release review is recorded in [PUBLICATION-AUDIT-2026-09-20.md](PUBLICATION-AUDIT-2026-09-20.md), with live publication receipts from [September 23](PUBLICATION-RECEIPTS-2026-09-23.md) and [October 17](PUBLICATION-RECEIPTS-2026-10-17.md).

The [October 17 FLSUN V400 audit](printer-audits/2026-10-17/) records the 328 loaded G-code files, their hashes and source evidence, and 593 controller-history records. Controller completion is kept separate from physical inspection and fit verification.

## Physical GitHub QR branding

Every release in this wave includes an optional, separately printable Isaiah Dupree brand and GitHub QR coupon. The common STL and editable STEP are also in [`branding/`](branding/). Keeping the mark separate avoids changing fit, load, sealing, or attribution-sensitive surfaces. Contrast-fill the recessed QR cells and verify the code scans before display.

## Request a design

Have a real fitment problem or a useful print idea? [Open a design request](https://github.com/IsaiahDupree/3d-print-library/issues/new/choose).

Helpful requests include:

- the problem the part must solve;
- measurements and tolerances;
- exact mating components or fasteners;
- operating temperature, water, sunlight, chemicals, vibration, and load;
- printer, nozzle, material, and build-volume constraints;
- clear photographs that contain no private information.

A request is an invitation to evaluate an idea, not a promise that it will be designed or manufactured.

## Release and quality policy

A model is published only after its authorship, licence, geometry, print settings, and public assets are reviewed. Testing status is stated honestly: a converted or sliced model is not described as physically printed or fit-verified.

Use any physical part at your own risk. Re-check dimensions, material suitability, fasteners, loads, temperature, electrical clearance, and the surrounding machinery or vehicle before use.

## Licensing

There is intentionally no repository-wide CAD licence. Each model folder carries its own `LICENSE` or `LICENSE.md`, matching the applicable Printables listing and preserving required attribution. See [LICENSE-POLICY.md](LICENSE-POLICY.md).

The controlled mirror procedure is documented in [SYNCING.md](SYNCING.md).

## Orion working library

The Orion desktop shortcut **3D Print Library** opens the local searchable index
at `E:\3D Printing\Organized Print Library\START_HERE.html`. It groups design,
archive, and legacy print assets from Projects, For Friends, Print List, and
FLSunV400, plus the manufacturing output folders for enclosure, dumbbell,
plant, modeling, and V400 work under Orion’s control plane. Large generated
collections are split into project/job pages and retain their revisions. Folder shortcuts lead to the existing source projects; source files
are not relocated. This working library is separate from the reviewed public
model releases above.

The `01_V400_Printer_Backup` subtree mirrors the controller's existing numbered
project folders. The index reports verified versus pending backup files and
opens the controller copy where a backup is still pending. Verification uses
the exact SHA-256 baseline from the October 17 audit. Unidentified files and
alternates remain retained. These categories and backups do not establish
physical print completion, fit, authorship, or publication permission.

[`scripts/organize_orion_prints.py`](scripts/organize_orion_prints.py) runs on
Orion with explicit `--library`, `--baseline`, `--printer-url`, and repeated
`--source-root` arguments. Use `--index-only` to refresh the index without
downloading missing backup files. A normal run downloads missing files
sequentially, checks hashes before accepting them, and retains JSONL receipts.
A changed controller path inventory requires review of a refreshed baseline.
The script issues only GET requests to the controller. Orion also retains the
deployed refresh entry point under the library’s `Tools` folder and the
reviewed baseline under `Records`.

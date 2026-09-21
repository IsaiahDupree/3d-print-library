# 3D-print publication audit — 2026-09-20

## Scope

The refreshed private catalog covered **8,888 files**, **4,176 logical models**, and **3,621 unique created/remixed payloads** across Mac and Orion storage. The created/remixed register grouped 6,753 file instances into 23 design families. These counts include duplicate exports, revision history, source/mesh pairs, assemblies, reference solids, renders, and non-printable assets; they are not a claim that thousands of independent models are ready to publish.

## Release wave

Six reviewed packs were selected in addition to the already-public Vehicle A/C Diagnostic Sensor Enclosure V4:

| Pack | Authorship | Evidence and disposition |
|---|---|---|
| Vehicle Firewall-Slot Tapered Fit Gauge V5 | Original, AI-assisted | Geometry-audited measurement sequence; not physically printed or vehicle-fit verified |
| A/C Enclosure Design Evolution V1–V4 | Original, AI-assisted | Historical pack; exact V4 body screened in ANSYS on Orion; not a recommended vehicle build |
| WLED ESP32 Controller Enclosure | Original | Three authored parts; sizing-reference components excluded; no completed print documented |
| Twin Flame Desk Sign | Remix | Two exact upstream Printables pages and compatible licences recorded; modifications disclosed |
| Scrunchie Tree | Remix | Exact upstream Printables page and CC BY-NC terms recorded; modifications disclosed |
| Nanosaur Track Ring | Remix | Exact upstream GitHub project and CC BY-NC-SA terms recorded; modifications disclosed |

Every pack includes a separate Isaiah Dupree + GitHub QR coupon. The mark is deliberately not fused into fitted, load-bearing, sealing, or upstream-derived geometry.

## Engineering evidence

The A/C Enclosure V4 public body STEP was run through a three-point ANSYS MAPDL mesh sweep on Orion under an idealized 250 N rim-compression load. Displacement approached stability at 0.8198 mm on the finest mesh, while the 9.712 MPa local peak remained mesh-sensitive. The report therefore makes no factor-of-safety, strength, printed-part, or vehicle-qualification claim.

The WLED tower was not given a synthetic FEA result: its source is a multi-body assembly and lacks an evidenced service load, restraint contract, calibrated printed-material card, and isolated single-solid analysis target. Decorative organizers and remix geometry do not receive engineering claims merely because solver capacity exists.

## Held from publication

The remaining catalog stays private until each model passes its own release gate. Held categories include:

- personal/name-specific designs and private one-off work;
- downloaded/reference geometry not authored by Isaiah;
- remixes without exact source, licence, attribution, and change evidence;
- non-printable game, anatomy, and application assets;
- unnamed Orion job outputs that lack project identity, visuals, and intended-use evidence;
- duplicate, intermediate, superseded, keep-out, or assembly-reference exports;
- functional parts without a defensible use, test, safety, and documentation contract.

This audit favors a small, reproducible, correctly attributed library over bulk-uploading every inferred creation.

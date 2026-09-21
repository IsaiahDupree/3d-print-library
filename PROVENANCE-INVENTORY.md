# CAD provenance inventory

The private catalog refreshed Isaiah's Mac and Orion CAD roots on 2026-09-20. It found **8,888 file instances**, representing **4,176 logical models** and **3,621 unique created/remixed payloads** across 23 reviewed design families. Orion contributed 5,816 CAD entries, including 2,828 STL, 2,502 STEP, and 75 FreeCAD files.

| Catalog scope | Count | Public handling |
|---|---:|---|
| All scanned file instances | 8,888 | Deduplicate and group before any release decision |
| Logical model groups | 4,176 | Review by coherent project, not filename alone |
| Created/remixed file instances | 6,753 | Eligible only after model-level authorship, privacy, geometry, and licence review |
| Unique created/remixed payloads | 3,621 | Preserve exact hashes and exclude reference geometry |
| Design families reviewed | 23 | Six families selected for this release wave; one earlier release remains public |

The created count is not a count of publishable models. It includes duplicated Mac/Orion copies, historical build runs, STEP/STL pairs, keepout/reference solids, non-printable application assets, and intermediate revisions. Printables releases are therefore grouped by a coherent design project, and only the latest supported artifacts are published.

## Public and publication-ready releases

- [Vehicle A/C Diagnostic Sensor Enclosure V4](models/vehicle-ac-diagnostic-sensor-enclosure-v4/) — already public; original AI-assisted prototype.
- [Vehicle Firewall-Slot Tapered Fit Gauge V5](models/vehicle-firewall-slot-tapered-fit-gauge-v5/) — original AI-assisted measurement toolkit.
- [A/C Diagnostic Enclosure Design Evolution V1–V4](models/ac-diagnostic-enclosure-design-evolution-v1-v4/) — original AI-assisted historical pack with a three-point Orion/ANSYS MAPDL screening study.
- [WLED ESP32 Controller Enclosure](models/wled-esp32-enclosure/) — original enclosure geometry; third-party component models were sizing references and are excluded.
- [Twin Flame Desk Sign](models/twin-flame-sign-remix/), [Scrunchie Tree](models/scrunchie-holder-remix/), and [Nanosaur Track Ring](models/nanosaur-tracks-mod/) — remixes with exact source URLs, creators, licences, change descriptions, and compatible CC BY-NC-SA 4.0 releases.

No remix is represented as original work. The remaining families stay private when they are personal designs, non-printable application assets, unreviewed Orion jobs, duplicated/intermediate exports, or derivatives without exact redistribution evidence. See [PUBLICATION-AUDIT-2026-09-20.md](PUBLICATION-AUDIT-2026-09-20.md) for the wave-level disposition.

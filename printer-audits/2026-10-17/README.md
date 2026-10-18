# FLSUN V400 file, source, and print-history audit

Observed on October 17, 2026, America/New_York (October 18 UTC). The audit used
read-only Moonraker requests and SSH with the previously trusted controller host
key. The printer was idle, the heater targets were zero, and its actual job
queue was empty.

## What is loaded

All **328 G-code files (3,239,404,389 bytes)** were hashed on the Speeder Pad.
Every file remained unchanged during hashing. Their paths exactly match the
[September 19 organization](../../printer-catalog/FLSUN-V400-PRINT-ORDER.md):
302 primary files, 20 retained alternates, and six unidentified review files.
There were no additions or missing paths. Existing project directories and
numbered print sequences therefore remain the organization of record; this
audit made no printer changes.

The inventory and exact hashes are in [files-and-origins.json](files-and-origins.json).
The existing sequence expresses project dependencies, not a queue of 302 jobs
that need to be printed. The actual Moonraker queue contained **zero** jobs.
No dumbbell-rack G-code was loaded at the time of the audit.

## Where the files came from

| Evidence level | Files | What was verified |
| --- | ---: | --- |
| Exact printer, local G-code, and original-source chain | 99 | Printer and current local G-code SHA-256 match; saved slicing and transform receipts link that G-code to the original STL; current original STL bytes match its source hash |
| Name-based source candidates | 140 | Normalized model names match existing CAD catalog entries; the source relationship is unproven |
| Source unresolved | 89 | No adequate source match was found in the saved CAD catalog and bounded local G-code search |

All 99 files in `01_Current_CAD_Catalog` have the exact chain: A/C V4 (40),
Andrew computing parts (5), and the three plaque collections (54). Current
Mac source STL files were rehashed. The public manifest records local G-code
and receipt locations under `workspace:cad-catalog/runs/`, original models
under logical roots such as `designs:Projects/`, and matching CAD catalog IDs.
The complete original Mac/Orion paths and unfiltered controller snapshots are
preserved in a private audit directory outside Git.

A filename candidate is retained as a candidate even when the shape appears
plausible. It does not establish the original author, licence, exact revision,
or redistribution permission. The bounded Mac G-code search found 335 files:
320 CAD build artifacts and 15 newer plant-coupon screening artifacts. The
latter are absent from this printer; their presence locally does not establish
that they are needed print jobs.

## Most recent controller-completed jobs

| End time, UTC | Job | Machine print duration |
| --- | --- | ---: |
| September 20, 19:05 | Patterson Laboratories small rounded gear plaque, screw mount | 1 h 02 min |
| September 20, 17:26 | McCool medium stadium plaque, screw mount | 1 h 42 min |
| September 17, 20:41 | Andrew ARK Raspberry Pi CM5 part, default 100% profile | 1 h 01 min |
| September 17, 18:38 | Andrew KV260 support, default 100% profile | 5 h 22 min |
| September 17, 05:13 | Andrew KV260 support, default 100% profile | 4 h 43 min |
| September 16, 21:19 | Andrew ARK Raspberry Pi CM5 part, default 100% profile | 48 min |
| September 15, 15:36 | A/C V4 standing body | 13 h 26 min |
| September 14, 12:33 | A/C V4 pigtail cap | 2 h 11 min |

The controller retains **593 historical records**: 352 completed, 172 cancelled,
eight errors, 59 marked `in_progress`, and two Klipper shutdowns. Those 59
historical rows do not mean 59 live jobs: the separately observed current
printer state was standby/idle with an empty queue.

[print-history.json](print-history.json) preserves all controller records with
their original timestamps and filenames. Of these, 450 link to current files
by matching Moonraker metadata UUID, and ten have weaker filename-and-size
candidate matches. Renamed files explain many historical `exists: false`
values; that field alone does not prove that the G-code was deleted.

The first SSH time response was stale (September 21); a later connection
reported October 18 UTC. This audit did not modify the clock or adjust old
history timestamps. These are controller-reported completion records, and
physical inspection, fit, strength, and photographs remain separate evidence.

## Print planning and preservation

- Keep the existing tree, project numbering, alternates, and six review files.
- Use the A/C coupon → clearance gauge → enclosure sequence already recorded
  in the print-order catalog; physical coupon/fit results still determine which
  step is due. A controller completion alone does not pass a fit test.
- The dumbbell project needs its own approved measurement set, part manifest,
  insert/fastener coupons, load-test records, and reviewed slicer outputs before
  it has a determined print list. Its new files should have a dedicated project
  directory when those artifacts exist.
- Preserve these manifests and hashes. The 3.24 GB printer payload was hashed
  in place; this audit is not a claim that a complete G-code backup was copied.
  Original sources and build receipts for the 99 traced files remain on the
  Mac. Unresolved legacy G-code should be backed up before any later cleanup.

## Reproduce

[`scripts/audit_printer.py`](../../scripts/audit_printer.py) has GET-only HTTP
capture and read-only SSH hashing. It cannot rename, upload, queue, start,
pause, cancel, or delete a print. Supply a private snapshot directory, the
workspace root, the output directory, the existing printer endpoint and SSH
identity. Strict host-key verification stays enabled. Omit `--printer-url` to
rebuild the public export from saved snapshots without contacting the printer.

Public exports use selected fields and logical location aliases. Credentials,
raw connection configuration, network addresses, and full private Mac paths
are excluded. [summary.json](summary.json) contains machine-readable counts;
[organization-plan.json](organization-plan.json) records the preservation plan.

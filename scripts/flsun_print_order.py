#!/usr/bin/env python3
"""Build and optionally apply a deterministic FLSUN V400 print-order catalog."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


DEFAULT_URL = "http://192.168.1.78"
NUMBERED_RE = re.compile(r"^(?:\d{3}_(?:ALT_|REVIEW_)?)")

AC_ORDER = [
    "arduino_uno_mount_coupon",
    "raspberry_pi_hat_mount_coupon",
    "branding_qr_process_coupon",
    "m25_board_clearance_coupon",
    "m3_insert_fit_coupon",
    "m3_horizontal_insert_boss_coupon",
    "m25_insert_fit_coupon",
    "standing_wall_hole_coupon",
    "pigtail_gland_coupon",
    "standing_bridge_coupon",
    "vehicle_bolt_coupon",
    "adapter_drill_template",
    "depth_feeler_45_55_65",
    "right_io_60mm_witness",
    "slot_clearance_cage",
    "body_standing",
    "right_pigtail_cap_print",
    "front_lid",
    "electronics_backplane",
    "raspberry_pi_hat_bench_baseplate",
]

PROJECT_RULES = {
    "10_Adaptive_Button_Box": [
        "fitcheck", "collar", "frame", "button.", "red plain button",
        "yellow top", "button_top", "button_26_letter", "button_box",
        "front", "slide", "flap", "spacer", "window", "pb_holder",
    ],
    "11_Nanosaur_Drone_Robotics": [
        "pcb stencil", "dronecan_adapter", "copterlab_adapter", "motor_cover",
        "nanosaur_cover", "nanosaur_tracks", "pixhawk", "kria", "storm adapter",
        "landing_gear", "fuselage", "gripper", "sprocket", "track_print",
    ],
    "12_Multiboard_Workshop": [
        "multiboard snap", "offset snap", "snap connector", "corner tile",
        "baseplate", "slidecleat", "hand tool holder", "hammer", "plier",
        "scissor", "wrench", "bit-holder", "drillholder", "mill and drill",
        "multimeter", "stiftehalter", "triple holder", "clamp", "brace",
    ],
    "13_Coin_Displays": [
        "coin-stand", "holder-blank", "coinrack.v2-leg", "coinrack.v2-body",
        "challenge-coin-holder",
    ],
    "14_Infinity_LED_Lamp": [
        "fv_in.", "fv_out.", "diffuser", "inlay", "cover", "body",
    ],
    "15_Cameras_Displays": [
        "camera modified_10", "camera modified_20", "camera modified_30",
        "display_template", "rpi_hq_support", "support_camera", "protection_camera",
        "display_container", "display and hinge",
    ],
    "16_Electronics_Enclosures": [
        "cablemount", "wago", "connector", "knob", "latch", "hinge", "fan",
        "solder", "arduino", "server_rack", "tf_digital", "fluxgrip", "enclosure",
    ],
    "17_Plaques_Coasters_Nameplates": [
        "coaster - be", "binarycoaster", "flower+coaster", "plaque", "name+plates",
    ],
    "18_Home_Office_Holders": [
        "phone_amplifier_cover", "phone_amplifier_body", "glassesholder",
        "quest 3", "vr_holder", "scrunchie_holder", "book_holder", "sprinkler",
        "rollo_holder",
    ],
    "19_Toys_Decor_Keychains": [
        "keychain", "bookmark", "geoguessrpin", "atom", "fidget", "cat.",
        "kitty", "kermit", "starfish", "geom", "alberts", "hagan", "medrozo",
        "shrek", "skull",
    ],
    "20_FLSUN_Printer_Parts": ["flsunv400spatula", "spatula_2"],
    "21_Calibration_Fit_Tests": [
        "printtest", "quater_2_5", "quater_5", "quater_10", "quater_15",
        "quater_20", "quater_30", "quater.", "resbalon_05", "resbalon_052",
        "printinone",
    ],
    "22_Robotics_Mechanical_Parts": [
        "vismol", "aufsatz", "spindel", "wheel", "inner", "outer", "base_front",
        "base_rear", "bottom tray", "left_side", "right_side", "v2_brace", "v2_top",
        "v2_all",
    ],
    "23_Generic_Boxes_Covers": ["cap.", "cover.", "box_4", "box4", "box5", "box2", "box."],
}


def api_get(base: str, path: str) -> dict:
    with urllib.request.urlopen(base + path, timeout=20) as response:
        return json.load(response)


def api_post(base: str, path: str, payload: dict) -> dict:
    request = urllib.request.Request(
        base + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def clean_name(filename: str) -> str:
    return NUMBERED_RE.sub("", filename)


def logical_name(filename: str) -> str:
    value = clean_name(filename).lower()
    value = re.sub(r"^cad-catalog-[0-9a-f]+-", "", value)
    return value.replace(".thumbnails.gcode", ".gcode")


def token_rank(name: str, tokens: list[str]) -> int:
    lowered = name.lower()
    for index, token in enumerate(tokens):
        if token in lowered:
            return index
    return len(tokens) + 10


def plaque_rank(name: str) -> tuple[int, int, str]:
    lowered = name.lower()
    size = 0 if "-s-" in lowered else 20 if "-m-" in lowered else 40 if "-l-" in lowered else 60
    mount = 0 if "plain" in lowered else 2 if "hang" in lowered else 4 if "keyhole" in lowered else 6
    shape = 0 if "text-only" in lowered else 1 if "rounded" in lowered else 2 if "chamfer" in lowered else 3
    return size + mount, shape, lowered


def project_sort_key(project: str, item: dict) -> tuple:
    name = clean_name(Path(item["path"]).name)
    lowered = name.lower()
    seconds = item.get("estimated_time") or 10**9
    if project.endswith("AC_V4_Enclosure"):
        return token_rank(lowered, AC_ORDER), seconds, lowered
    if "/Plaques/" in project:
        return (*plaque_rank(lowered), seconds)
    if project.endswith("Andrew_Computing"):
        kind = 0 if "kv260-support" in lowered else 10 if "rpicm5" in lowered else 20
        newest = -(item.get("modified") or 0)
        return kind, newest, seconds, lowered
    tokens = PROJECT_RULES.get(project, [])
    if tokens:
        return token_rank(lowered, tokens), seconds, lowered
    return seconds, lowered


def rationale(project: str, filename: str) -> str:
    lowered = filename.lower()
    if project.endswith("AC_V4_Enclosure"):
        if "coupon" in lowered or "witness" in lowered or "feeler" in lowered:
            return "Validation gate from the AC V4 documented first-fit sequence."
        if "cage" in lowered:
            return "Empty clearance fit follows the coupons and physical measurements."
        if any(x in lowered for x in ("body_standing", "front_lid", "backplane", "cap_print")):
            return "Production-scale part; print only after all applicable coupons pass."
        return "Ordered by the AC V4 documented print and assembly sequence."
    if "/Plaques/" in project:
        return "Small/simple variants lead; larger and more complex mounting variants follow."
    if any(x in lowered for x in ("test", "fit", "coupon", "template", "stencil", "witness")):
        return "Low-cost validation or fit part before larger dependent parts."
    if any(x in lowered for x in ("base", "frame", "body", "support", "mount", "holder")):
        return "Structural or locating part precedes covers, detail parts, and alternates."
    return "Ordered by dependency, size, and estimated print cost within this project."


def metadata(base: str, path: str) -> dict:
    query = urllib.parse.urlencode({"filename": path})
    for attempt in range(3):
        try:
            return api_get(base, "/server/files/metadata?" + query).get("result", {})
        except (OSError, urllib.error.URLError, TimeoutError, ValueError):
            if attempt < 2:
                time.sleep(0.25 * (attempt + 1))
    return {}


def build_plan(base: str) -> list[dict]:
    source = api_get(base, "/server/files/list").get("result", [])
    metadata_by_path: dict[str, dict] = {}
    candidate_paths = [item["path"] for item in source if "/" in item["path"]]
    with ThreadPoolExecutor(max_workers=6) as pool:
        for path, info in zip(candidate_paths, pool.map(lambda value: metadata(base, value), candidate_paths)):
            metadata_by_path[path] = info
    items = []
    for file_info in source:
        path = file_info["path"]
        if "/" not in path:
            continue
        project, filename = path.rsplit("/", 1)
        info = metadata_by_path.get(path, {})
        items.append({
            **file_info,
            "project": project,
            "filename": clean_name(filename),
            "estimated_time": info.get("estimated_time"),
            "filament_total_mm": info.get("filament_total"),
            "layer_height_mm": info.get("layer_height"),
            "has_thumbnail": bool(info.get("thumbnails")) or ".thumbnails.gcode" in filename.lower(),
        })

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        grouped[item["project"]].append(item)

    plan = []
    for project in sorted(grouped):
        by_logical: dict[str, list[dict]] = defaultdict(list)
        for item in grouped[project]:
            by_logical[logical_name(item["filename"])].append(item)

        preferred = []
        alternates = []
        for variants in by_logical.values():
            variants.sort(key=lambda x: (not x["has_thumbnail"], -(x.get("modified") or 0), x["filename"]))
            preferred.append(variants[0])
            alternates.extend(variants[1:])

        preferred.sort(key=lambda x: project_sort_key(project, x))
        alternates.sort(key=lambda x: (project_sort_key(project, x), x["filename"]))
        for sequence, item in enumerate(preferred, 1):
            marker = "REVIEW_" if project == "90_Misc_Parts_To_Review" else ""
            new_filename = f"{sequence:03d}_{marker}{item['filename']}"
            plan.append({
                **item,
                "sequence": sequence,
                "status": "review" if marker else "primary",
                "old_path": item["path"],
                "new_path": f"{project}/{new_filename}",
                "rationale": rationale(project, item["filename"]),
            })
        for sequence, item in enumerate(alternates, 901):
            new_filename = f"{sequence:03d}_ALT_{item['filename']}"
            plan.append({
                **item,
                "sequence": sequence,
                "status": "alternate_duplicate",
                "old_path": item["path"],
                "new_path": f"{project}/{new_filename}",
                "rationale": "Alternate duplicate retained; prefer the matching thumbnail-enabled primary file.",
            })
    return sorted(plan, key=lambda x: (x["project"], x["sequence"], x["new_path"]))


def apply_plan(base: str, plan: list[dict]) -> None:
    state = api_get(base, "/printer/info").get("result", {}).get("state")
    if state != "ready":
        raise SystemExit(f"Refusing to rename files while printer state is {state!r}")
    for index, item in enumerate(plan, 1):
        if item["old_path"] == item["new_path"]:
            continue
        api_post(base, "/server/files/move", {
            "source": "gcodes/" + item["old_path"],
            "dest": "gcodes/" + item["new_path"],
        })
        if index % 50 == 0:
            print(f"renamed {index}/{len(plan)}", flush=True)


def duration(seconds: float | None) -> str:
    if not seconds:
        return "unknown"
    minutes = int(round(seconds / 60))
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes:02d}m" if hours else f"{minutes}m"


def write_catalog(output_dir: Path, base: str, plan: list[dict], applied: bool) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = dt.datetime.now(dt.timezone.utc).isoformat()
    payload = {
        "schema": "flsun-v400-print-order-v1",
        "generated_at": generated_at,
        "printer_url": base,
        "applied_to_printer": applied,
        "policy": {
            "primary_range": "001-899",
            "alternate_range": "901-999",
            "review_marker": "REVIEW",
            "safety": "Numbering expresses sequence, not permission to skip fit, material, or installation gates.",
        },
        "files": plan,
    }
    json_path = output_dir / "flsun-v400-print-order.json"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in plan:
        grouped[item["project"]].append(item)
    lines = [
        "# FLSUN V400 print-order catalog",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Files on the Speeder Pad are prefixed with a three-digit sequence within each project. "
        "Numbers `001-899` are the recommended order. Numbers `901-999` are retained duplicate/alternate files. "
        "`REVIEW` means the file needs human identification before printing.",
        "",
        "> Numbering is a planning aid, not authorization to bypass fit checks, material qualification, slicer preview, or installation safety gates.",
        "",
        "## Project summary",
        "",
        "| Project | Primary | Alternates | First recommended file |",
        "| --- | ---: | ---: | --- |",
    ]
    for project, project_items in sorted(grouped.items()):
        primary = [x for x in project_items if x["status"] != "alternate_duplicate"]
        alternate_count = len(project_items) - len(primary)
        first = primary[0]["new_path"].rsplit("/", 1)[-1] if primary else "—"
        lines.append(f"| `{project}` | {len(primary)} | {alternate_count} | `{first}` |")

    for project, project_items in sorted(grouped.items()):
        lines.extend(["", f"## {project}", "", "| # | Status | Est. time | File | Why |", "| ---: | --- | ---: | --- | --- |"])
        for item in project_items:
            filename = item["new_path"].rsplit("/", 1)[-1].replace("|", "\\|")
            why = item["rationale"].replace("|", "\\|")
            lines.append(f"| {item['sequence']:03d} | {item['status']} | {duration(item.get('estimated_time'))} | `{filename}` | {why} |")
    lines.append("")
    md_path = output_dir / "FLSUN-V400-PRINT-ORDER.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    checksums = []
    for path in (md_path, json_path):
        checksums.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (output_dir / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--printer-url", default=DEFAULT_URL)
    parser.add_argument("--output-dir", type=Path, default=Path("printer-catalog"))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    plan = build_plan(args.printer_url.rstrip("/"))
    if args.apply:
        apply_plan(args.printer_url.rstrip("/"), plan)
        for item in plan:
            item["path"] = item["new_path"]
    write_catalog(args.output_dir, args.printer_url.rstrip("/"), plan, args.apply)
    print(f"cataloged {len(plan)} files across {len(set(x['project'] for x in plan))} projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

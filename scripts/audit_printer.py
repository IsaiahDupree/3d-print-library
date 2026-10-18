#!/usr/bin/env python3
"""Read-only Moonraker audit, receipt correlation, and sanitized publication export.

Private snapshots retain exact device/local paths. The public export uses logical
root names and selected fields only. This tool has no printer write operation.
Hashing is sequential on the printer and source files are never opened by CAD.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import re
import subprocess
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


READS = {
    "files": "/server/files/list",
    "history": "/server/history/list?limit=1000&order=desc",
    "queue": "/server/job_queue/status",
    "printer": "/printer/info",
    "state": "/printer/objects/query?print_stats&virtual_sdcard&idle_timeout&heater_bed&extruder",
    "server": "/server/info",
    "totals": "/server/history/totals",
}


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(data)
    return result.hexdigest()


def iso(epoch: float | None) -> str | None:
    return dt.datetime.fromtimestamp(epoch, dt.timezone.utc).isoformat() if epoch else None


def clean_name(value: str) -> str:
    return re.sub(r"^\d{3}_(?:ALT_|REVIEW_)?", "", Path(value).name)


def stem_key(value: str) -> str:
    value = clean_name(value).lower()
    value = re.sub(r"^cad-catalog-[0-9a-f]+-", "", value)
    value = re.sub(r"^fv[_ ]", "", value)
    return re.sub(r"[^a-z0-9]", "", Path(value.replace(".thumbnails", "")).stem)


def public_locator(value: str, workspace: Path) -> str:
    roots = [(workspace, "workspace"), (Path.home() / "Documents/3D Printing", "designs"),
             (Path.home() / "Downloads", "downloads"), (Path.home() / "Desktop", "desktop")]
    for root, label in roots:
        try:
            return label + ":" + str(Path(value).relative_to(root))
        except ValueError:
            pass
    # Unrecognized source locations remain private; the source hash is public.
    return "private-location:" + hashlib.sha256(value.encode()).hexdigest()[:16]


def capture(base: str, private: Path, ssh_target: str | None, host_alias: str | None) -> None:
    private.mkdir(parents=True, exist_ok=True)
    def get(path: str) -> dict:
        with urllib.request.urlopen(base.rstrip("/") + path, timeout=15) as response:
            return json.load(response)
    write_json(private / "capture.json", {"observed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                                           "printer_url": base, "operation": "GET-only"})
    for name, path in READS.items():
        write_json(private / (name + ".json"), get(path))
    files = read_json(private / "files.json")["result"]
    history = read_json(private / "history.json")["result"]
    # The current device has fewer than 1000 jobs. Fail rather than silently
    # publishing an incomplete history on a larger device.
    if history["count"] != len(history["jobs"]):
        raise ValueError("History exceeds capture bound; paginate before exporting")
    def metadata(item: dict) -> tuple[str, dict]:
        path = item["path"]
        return path, get("/server/files/metadata?" + urllib.parse.urlencode({"filename": path}))["result"]
    with ThreadPoolExecutor(max_workers=4) as pool:
        write_json(private / "metadata.json", dict(pool.map(metadata, files)))
    if not ssh_target:
        return
    options = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=7", "-o", "StrictHostKeyChecking=yes"]
    if host_alias:
        options += ["-o", "HostKeyAlias=" + host_alias]
    # This V400's root was checked through SSH. Export additionally requires a
    # stable hash with matching size for every path returned by Moonraker.
    # No source or configuration is modified.
    remote = r'''
import os,hashlib,json,time
root='/home/pi/gcode_files'
files=[]
for folder,dirs,names in os.walk(root,followlinks=False):
 dirs[:]=[x for x in dirs if x not in ['.thumbs','.git']]
 for name in names:
  if not name.lower().endswith(('.gcode','.gco','.g')):continue
  p=os.path.join(folder,name)
  if os.path.islink(p):continue
  before=os.stat(p);h=hashlib.sha256()
  with open(p,'rb') as f:
   for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
  after=os.stat(p)
  files.append({'path':os.path.relpath(p,root),'size':before.st_size,'mtime':before.st_mtime,'sha256':h.hexdigest(),'stable':before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns})
print(json.dumps({'root':root,'observed_epoch':time.time(),'files':files}))
'''
    result = subprocess.run(options + [ssh_target, "python3 -"], input=remote,
                            text=True, capture_output=True, timeout=180, check=True)
    write_json(private / "ssh-hashes.json", json.loads(result.stdout))


def export(private: Path, public: Path, workspace: Path) -> dict:
    files = read_json(private / "files.json")["result"]
    hashes = {x["path"]: x for x in read_json(private / "ssh-hashes.json")["files"]}
    metadata = read_json(private / "metadata.json")
    history = read_json(private / "history.json")["result"]
    queue = read_json(private / "queue.json")["result"]
    state = read_json(private / "state.json")["result"]["status"]
    catalog_path = workspace / "cad-catalog/dist/data/catalog.json"
    catalog = read_json(catalog_path)
    by_source = collections.defaultdict(list)
    by_name = collections.defaultdict(list)
    for item in catalog["items"]:
        by_source[item.get("sha256")].append(item)
        by_name[stem_key(item["filename"])].append(item)
    builds = collections.defaultdict(list)
    local_hash_cache = {}
    for run_path in sorted((workspace / "cad-catalog/runs").glob("*/run.json")):
        run = read_json(run_path)
        source = run.get("source", {})
        artifacts = []
        parents = {}
        receipt_paths = list((run_path.parent / "receipts").glob("*.json"))
        receipt_paths += list((run_path.parent / "gcode").glob("*.json"))
        for receipt_path in sorted(receipt_paths):
            receipt = read_json(receipt_path)
            for path_field, hash_field in (("gcode", "gcode_sha256"), ("output", "output_sha256"), ("output_gcode", "output_sha256")):
                name, expected = receipt.get(path_field), receipt.get(hash_field)
                if isinstance(name, str) and name.lower().endswith(".gcode") and expected:
                    artifacts.append((name, expected, str(receipt_path)))
                    parent_path = receipt.get("source_gcode", receipt.get("source"))
                    if isinstance(parent_path, str) and parent_path.lower().endswith(".gcode"):
                        parents[expected] = receipt.get("source_sha256")
        slice_path = run_path.parent / "receipts/slice.receipt.json"
        slice_receipt = read_json(slice_path) if slice_path.exists() else {}
        base_hash = slice_receipt.get("output_sha256")
        base_path = run.get("stages", {}).get("slice", {}).get("gcode")
        # This audit's traced builds use STL pass-through. Converted STEP runs
        # need an additional conversion edge before they can earn this label.
        base_verified = False
        if source.get("suffix") == ".stl" and slice_receipt.get("input_sha256") == source.get("expected_sha256") and isinstance(base_path, str) and Path(base_path).is_file():
            if base_path not in local_hash_cache:
                local_hash_cache[base_path] = sha256(Path(base_path))
            base_verified = local_hash_cache[base_path] == base_hash
        def chain_verified(value: str) -> bool:
            visited = set()
            while value != base_hash:
                if not value or value in visited or value not in parents:
                    return False
                visited.add(value)
                value = parents[value]
            return base_verified
        # Hash every selected local payload once; receipts alone are not proof
        # that the matching bytes still exist on disk.
        for name, expected, receipt_path in artifacts:
            path = Path(name)
            if not path.is_file():
                continue
            if name not in local_hash_cache:
                local_hash_cache[name] = sha256(path)
            if local_hash_cache[name] != expected or not chain_verified(expected):
                continue
            source_path = source.get("path")
            source_expected = source.get("expected_sha256")
            source_verified = None
            if source.get("host") == "mac" and source_path and Path(source_path).is_file():
                if source_path not in local_hash_cache:
                    local_hash_cache[source_path] = sha256(Path(source_path))
                source_verified = local_hash_cache[source_path] == source_expected
            builds[expected].append({"run_id": run.get("run_id", run_path.parent.name),
                "local_gcode": name, "upload_or_build_receipt": receipt_path,
                "source_host": source.get("host"), "source_path": source_path,
                "source_sha256": source_expected, "source_current_bytes_verified": source_verified,
                "slice_and_transform_receipt_chain_verified": True,
                "catalog_items": [{"id": x["id"], "path": x["path"], "host": x["host"]["id"],
                                   "project": x["project"]} for x in by_source[source_expected]]})
    mapped = []
    for item in files:
        remote = hashes.get(item["path"], {})
        if remote.get("size") != item["size"] or not remote.get("stable"):
            raise ValueError("Unstable or missing remote hash: " + item["path"])
        seen = set()
        exact = []
        for build in builds[remote["sha256"]]:
            key = (build["run_id"], build["local_gcode"])
            if key not in seen:
                exact.append(build); seen.add(key)
        candidates = [] if exact else [{"id": x["id"], "path": x["path"], "host": x["host"]["id"],
            "project": x["project"], "sha256": x.get("sha256")} for x in by_name[stem_key(item["path"])]]
        info = metadata.get(item["path"], {})
        mapped.append({**item, "sha256": remote["sha256"], "uuid": info.get("uuid"),
            "estimated_time_s": info.get("estimated_time"), "object_height_mm": info.get("object_height"),
            "source_evidence": "exact_gcode_sha256_and_build_receipt" if exact else "name_candidates_only" if candidates else "unresolved",
            "exact_builds": exact, "name_candidates": candidates})
    by_uuid = {x["uuid"]: x for x in mapped if x["uuid"]}
    by_clean = collections.defaultdict(list)
    for item in mapped:
        by_clean[clean_name(item["path"])].append(item)
    jobs = []
    for job in history["jobs"]:
        match = by_uuid.get(job.get("metadata", {}).get("uuid"))
        basis = "metadata_uuid" if match else None
        if not match:
            possible = by_clean[clean_name(job["filename"])]
            if len(possible) == 1:
                candidate = possible[0]
                if candidate["size"] == job.get("metadata", {}).get("size"):
                    match = candidate; basis = "filename_and_size_candidate"
        jobs.append({"job_id": job["job_id"], "filename_at_print": job["filename"], "status": job["status"],
            "start_time_utc": iso(job.get("start_time")), "end_time_utc": iso(job.get("end_time")),
            "print_duration_s": job.get("print_duration"), "filament_used_mm": job.get("filament_used"),
            "moonraker_exists_field": job.get("exists"), "current_printer_path": match["path"] if match else None,
            "current_path_evidence": basis,
            "current_source_evidence": match["source_evidence"] if match else None,
            "physical_inspection": "not_established_by_controller_history"})
    exact_count = sum(bool(x["exact_builds"]) for x in mapped)
    previous = read_json(workspace / "3d-print-library/printer-catalog/flsun-v400-print-order.json")
    old_paths = {x["new_path"] for x in previous["files"]}
    new_paths = {x["path"] for x in mapped}
    capture_path = private / "capture.json"
    observed_at = read_json(capture_path)["observed_at"] if capture_path.exists() else iso((private / "files.json").stat().st_mtime)
    summary = {"schema": "flsun-v400-audit/1", "observed_at_utc": observed_at,
        "exported_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "printer_state": state["print_stats"]["state"], "idle_timeout": state["idle_timeout"]["state"],
        "heater_targets_c": {"bed": state["heater_bed"]["target"], "extruder": state["extruder"]["target"]},
        "queued_jobs": len(queue["queued_jobs"]), "queue_state": queue["queue_state"],
        "file_count": len(mapped), "file_bytes": sum(x["size"] for x in mapped),
        "hashes_stable": True, "exact_source_chain_file_count": exact_count,
        "name_candidate_file_count": sum(x["source_evidence"] == "name_candidates_only" for x in mapped),
        "unresolved_file_count": sum(x["source_evidence"] == "unresolved" for x in mapped),
        "history_count": history["count"], "history_status_counts": dict(collections.Counter(x["status"] for x in jobs)),
        "latest_completed_job": next((x for x in jobs if x["status"] == "completed"), None),
        "previous_catalog_generated_at": previous["generated_at"],
        "added_since_previous_catalog": sorted(new_paths - old_paths),
        "missing_since_previous_catalog": sorted(old_paths - new_paths),
        "printer_mutations": [], "history_time_policy": "Controller timestamps preserved; no backdating or clock-offset correction."}
    private_payload = {"summary": summary, "files": mapped, "jobs": jobs}
    write_json(private / "origin-mappings.json", private_payload)
    public_files = []
    for item in mapped:
        builds_public = []
        for build in item["exact_builds"]:
            builds_public.append({"run_id": build["run_id"],
                "local_gcode": public_locator(build["local_gcode"], workspace),
                "receipt": public_locator(build["upload_or_build_receipt"], workspace),
                "source_host": build["source_host"],
                "source": public_locator(build["source_path"], workspace) if build["source_path"] else None,
                "source_sha256": build["source_sha256"], "source_current_bytes_verified": build["source_current_bytes_verified"],
                "slice_and_transform_receipt_chain_verified": build["slice_and_transform_receipt_chain_verified"],
                "catalog_item_ids": [x["id"] for x in build["catalog_items"]]})
        public_files.append({k: item[k] for k in ("path", "size", "sha256", "estimated_time_s", "source_evidence")} |
                            {"exact_builds": builds_public, "name_candidate_catalog_ids": [x["id"] for x in item["name_candidates"]]})
    write_json(public / "summary.json", summary)
    write_json(public / "files-and-origins.json", {"schema": "flsun-public-origins/1", "locations": "Logical aliases; exact private paths are retained outside Git.", "files": public_files})
    write_json(public / "print-history.json", {"schema": "moonraker-history-audit/1", "meaning": "Controller-completed jobs; does not establish physical fit or quality.", "jobs": jobs})
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private-dir", required=True, type=Path)
    parser.add_argument("--public-dir", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--printer-url", help="Optional GET-only refresh. Omit to reuse captured snapshots.")
    parser.add_argument("--ssh-target", help="Existing key-authenticated SSH target; enables sequential remote hashes.")
    parser.add_argument("--ssh-host-key-alias", help="Existing known_hosts identity; strict checking remains enabled.")
    args = parser.parse_args()
    if args.printer_url:
        capture(args.printer_url, args.private_dir, args.ssh_target, args.ssh_host_key_alias)
    print(json.dumps(export(args.private_dir, args.public_dir, args.workspace), indent=2))


if __name__ == "__main__":
    main()

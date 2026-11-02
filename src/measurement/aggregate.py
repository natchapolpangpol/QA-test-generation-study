"""Strict union-based coverage aggregation for replay artifacts, not execution counts."""
import argparse
import json
from pathlib import Path

KINDS = ("line", "statement", "block", "decision", "condition")

def summarize(inventory, trace_paths):
    available = {kind: set() for kind in KINDS}
    for item in inventory["items"]:
        kind, key = item["kind"], item["id"]
        if kind not in available or key in available[kind]:
            raise ValueError(f"Unknown kind or duplicate inventory item: {kind}:{key}")
        available[kind].add(key)
    covered = {kind: set() for kind in KINDS}
    events = 0
    for path in trace_paths:
        last = 0
        # Missing traces raise; they must never become an empty suite or zero coverage.
        for row in Path(path).read_text(encoding="utf-8").splitlines():
            seq, thread, kind, key = row.split("\t")
            if int(seq) <= last or int(thread) <= 0:
                raise ValueError("Invalid trace event order or thread ID")
            last = int(seq)
            if kind not in available or key not in available[kind]:
                raise ValueError(f"Trace item absent from inventory: {kind}:{key}")
            covered[kind].add(key)
            events += 1
    metrics = {}
    for kind in KINDS:
        n, d = len(covered[kind]), len(available[kind])
        metrics[kind] = {"covered": n, "total": d, "percent": 100*n/d if d else None,
                         "covered_ids": sorted(covered[kind]), "uncovered_ids": sorted(available[kind]-covered[kind])}
    n = metrics["condition"]["covered"] + metrics["decision"]["covered"]
    d = metrics["condition"]["total"] + metrics["decision"]["total"]
    metrics["condition_decision"] = {"covered": n, "total": d, "percent": 100*n/d if d else None}
    return {"scope": inventory["scope"], "source_sha256": inventory["source_sha256"],
            "measurement_version": inventory["measurement_version"], "events": events, "metrics": metrics}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("inventory", type=Path)
    p.add_argument("traces", nargs="+", type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    result = summarize(json.loads(a.inventory.read_text(encoding="utf-8")), a.traces)
    a.output.write_text(json.dumps(result, indent=2), encoding="utf-8")

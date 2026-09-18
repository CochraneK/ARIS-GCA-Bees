"""Conservative temporal-constraint checks for the ARIS4C008 hominin layer.

The script treats archaeological dates as first-secure-evidence intervals,
not true evolutionary origin dates.
"""
from __future__ import annotations
import csv
from pathlib import Path

def main():
    base=Path(__file__).resolve().parents[1]
    events={r["event_id"]:r for r in csv.DictReader(open(base/"data"/"hominin_milestones_v0.csv",encoding="utf-8-sig"))}
    tests=list(csv.DictReader(open(base/"data"/"hominin_temporal_falsification_v0.csv",encoding="utf-8-sig")))
    print("events",len(events),"tests",len(tests))
    for t in tests:
        c=events.get(t["candidate_event"])
        o=events.get(t["target_event"]) if t["target_event"] else None
        if c and o:
            c_young=float(c["age_young_ka"]); c_old=float(c["age_old_ka"])
            o_young=float(o["age_young_ka"]); o_old=float(o["age_old_ka"])
            # Larger ka = older. Strong contradiction when even the youngest plausible
            # target age is older than the oldest plausible candidate age.
            definite_target_older = o_young > c_old
            interval_overlap = not (o_young > c_old or c_young > o_old)
            print(t["test_id"],"definite_target_older=",definite_target_older,
                  "interval_overlap=",interval_overlap,
                  "coded=",t["temporal_relation"])

if __name__=="__main__":
    main()

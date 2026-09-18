#!/usr/bin/env python3
"""ARIS4C006 — synthetic/hand LOAO validation.

No real outcome data. Verifies:
  * exact random-order chance with surname ties,
  * excess-alpha numerator/denominator,
  * author contribution counted at most once per work,
  * exact leave-one-author-out subtraction,
  * D threshold behavior.
"""
from __future__ import annotations
import json, math
from collections import Counter, defaultdict
from pathlib import Path

def p_chance(keys):
    n=len(keys)
    if n<2: raise ValueError("team size must be >=2")
    num=1
    for m in Counter(keys).values():
        num*=math.factorial(m)
    return num/math.factorial(n)

def contribution(keys, listed_order=None):
    # keys are already in actual listed order unless listed_order is supplied.
    seq=keys if listed_order is None else [keys[i] for i in listed_order]
    pc=p_chance(seq)
    ia=int(all(seq[i] <= seq[i+1] for i in range(len(seq)-1)))
    return ia-pc, 1-pc, ia, pc

def build_totals(works):
    # work = {"work_id","keys","authors"} authors may contain duplicates defensively.
    N=D=0.0
    by_author=defaultdict(lambda:[0.0,0.0,set()])
    for w in works:
        num,den,_,_=contribution(w["keys"])
        N+=num;D+=den
        for a in set(w["authors"]):
            by_author[a][0]+=num
            by_author[a][1]+=den
            by_author[a][2].add(w["work_id"])
    return N,D,by_author

def loao(N,D,part,min_D=0.0):
    Ni,Di,_=part
    d=D-Di
    if d < min_D:return None
    return (N-Ni)/d if d>0 else None

def close(a,b,tol=1e-12):
    if not math.isclose(a,b,rel_tol=tol,abs_tol=tol):
        raise AssertionError(f"{a} != {b}")

def main():
    tests=[]

    # Chance tests.
    close(p_chance(["a","b"]), 1/2)
    close(p_chance(["a","b","c"]), 1/6)
    close(p_chance(["a","a","b"]), 2/6)
    close(p_chance(["a","a","b","b"]), 4/24)
    tests.append("tie-aware chance probabilities")

    # Contribution tests.
    n,d,ia,pc=contribution(["a","b","c"])
    close(n,5/6);close(d,5/6);assert ia==1;close(pc,1/6)
    n2,d2,ia2,pc2=contribution(["b","a","c"])
    close(n2,-1/6);close(d2,5/6);assert ia2==0;close(pc2,1/6)
    tests.append("work-level chance-corrected contributions")

    # Three hand-computable works.
    works=[
      {"work_id":"w1","keys":["a","b","c"],"authors":["A","B","C"]},
      {"work_id":"w2","keys":["b","a","c"],"authors":["D","E","F"]},
      {"work_id":"w3","keys":["a","z"],"authors":["A","A","G"]}, # duplicate A must count once
    ]
    N,D,parts=build_totals(works)
    close(N,7/6);close(D,13/6);close(N/D,7/13)
    # A owns w1+w3 exactly once each. Removing them leaves only w2: (-1/6)/(5/6)=-0.2
    close(loao(N,D,parts["A"]),-0.2)
    # D owns only w2; removing it leaves w1+w3, both alpha => 1
    close(loao(N,D,parts["D"]),1.0)
    assert parts["A"][2]=={"w1","w3"}
    tests.append("exact LOAO subtraction and per-work author deduplication")

    # Threshold.
    assert loao(N,D,parts["A"],min_D=1.0) is None  # residual D = 5/6
    assert loao(N,D,parts["D"],min_D=1.0) is not None
    tests.append("LOAO information threshold")

    # Invariance: author not in convention set equals full exposure.
    zero=[0.0,0.0,set()]
    close(loao(N,D,zero),N/D)
    tests.append("non-contributor invariance")

    out=Path("data/pilot/loao_synthetic")
    out.mkdir(parents=True,exist_ok=True)
    manifest={
      "script":"19_validate_loao_synthetic.py",
      "real_outcome_data_used":False,
      "tests_passed":len(tests),
      "tests":tests,
      "hand_total_N":N,
      "hand_total_D":D,
      "hand_full_exposure":N/D,
      "hand_A_loao":loao(N,D,parts["A"]),
      "status":"PASS"
    }
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(manifest,indent=2))

if __name__=="__main__":
    main()

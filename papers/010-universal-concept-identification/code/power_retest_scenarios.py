"""Approximate sensitivity scenarios for UCID retest-consistency contrasts.

This is NOT a final power analysis. It uses a two-proportion normal approximation
plus a simple participant-level design effect for 8 clustered retest judgments.

Two mechanisms are shown:
1. P2 -> P3: benefit of a coarse MAYBE escape response.
2. P3 -> P6: incremental benefit of fine-grained semantic response states.
"""

from __future__ import annotations

import math
from statistics import NormalDist


def independent_observations_per_arm(p1,p2,alpha=0.05,power=0.80):
    if p1==p2:
        return math.inf
    za=NormalDist().inv_cdf(1-alpha/2)
    zb=NormalDist().inv_cdf(power)
    p=(p1+p2)/2
    num=(za*math.sqrt(2*p*(1-p))+zb*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2
    return num/(p2-p1)**2


def participants_per_arm(p1,p2,retests=8,icc=0.05,alpha=0.05,power=0.80):
    n_eff=independent_observations_per_arm(p1,p2,alpha,power)
    de=1+(retests-1)*icc
    raw=n_eff*de
    return math.ceil(raw/retests),n_eff,de


def print_grid(label, baseline, alternatives, iccs=(0.00,0.05,0.10)):
    print(label)
    print(f"baseline={baseline:.2f}, alpha=.05 two-sided, power=.80, 8 retests/participant")
    print("target\tICC\teffective_obs/arm\tdesign_effect\tparticipants/arm")
    for target in alternatives:
        for icc in iccs:
            people,n_eff,de=participants_per_arm(baseline,target,icc=icc)
            print(f"{target:.2f}\t{icc:.2f}\t{n_eff:.1f}\t{de:.2f}\t{people}")
    print()


def main():
    print("Approximate participants per arm for retest-consistency contrasts")
    print_grid(
        "P2 -> P3 coarse-escape scenarios",
        baseline=0.80,
        alternatives=(0.85,0.88,0.90),
    )
    print_grid(
        "P3 -> P6 fine-graining scenarios",
        baseline=0.85,
        alternatives=(0.88,0.90,0.92),
    )


if __name__=="__main__":
    main()

"""Approximate sensitivity scenarios for P2 vs P6 retest consistency.

This is NOT a final power analysis. It uses a two-proportion normal approximation
plus a simple participant-level design effect for 8 clustered retest judgments.
It is included to make sample-size assumptions explicit before real data.
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


def main():
    baseline=0.80
    alternatives=[0.85,0.88,0.90]
    iccs=[0.00,0.05,0.10]
    print("Approximate participants per arm for retest-consistency contrast")
    print("baseline=0.80, alpha=.05 two-sided, power=.80, 8 retests/participant")
    print("p6\tICC\teffective_obs/arm\tdesign_effect\tparticipants/arm")
    for p6 in alternatives:
        for icc in iccs:
            people,n_eff,de=participants_per_arm(baseline,p6,icc=icc)
            print(f"{p6:.2f}\t{icc:.2f}\t{n_eff:.1f}\t{de:.2f}\t{people}")


if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""Deterministic matched pseudo-systems for ARIS4C013 H3/H4 tests."""
from __future__ import annotations

import hashlib

from traditional_features import ELEMENTS, STEMS

PSEUDO_SEEDS = tuple(range(13001, 14001))


def _stable_order(items, seed: int, namespace: str):
    return sorted(
        items,
        key=lambda item: hashlib.sha256(
            f"{namespace}|{seed}|{item}".encode("utf-8")
        ).digest(),
    )


def balanced_stem_element_map(seed: int) -> dict[str, str]:
    """Randomized 10→5 map preserving exactly two stems per element."""
    ordered = _stable_order(STEMS, seed, "stem-element")
    labels = [element for element in ELEMENTS for _ in range(2)]
    return {stem:labels[i] for i,stem in enumerate(ordered)}


def balanced_stem_polarity_map(seed: int) -> dict[str, str]:
    """Randomized 10→2 map preserving a 5 Yang / 5 Yin balance."""
    ordered = _stable_order(STEMS, seed, "stem-polarity")
    return {
        stem:("Yang" if i < 5 else "Yin")
        for i,stem in enumerate(ordered)
    }


def solar_boundary_shift_days(seed: int) -> int:
    """Stable non-zero whole-day shift in [-30,-3] ∪ [3,30]."""
    candidates = tuple(range(-30, -2)) + tuple(range(3, 31))
    digest = hashlib.sha256(
        f"solar-boundary-shift|{seed}".encode("utf-8")
    ).digest()
    index = int.from_bytes(digest[:8], "big") % len(candidates)
    return candidates[index]


def term_index_shift(index: int, seed: int) -> int:
    """Shift a 24-term index by a stable non-zero phase."""
    digest = hashlib.sha256(
        f"term-index-shift|{seed}".encode("utf-8")
    ).digest()
    shift = 1 + int.from_bytes(digest[:8], "big") % 23
    return (int(index) + shift) % 24

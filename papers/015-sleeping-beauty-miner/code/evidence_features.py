"""Transparent non-citation evidence features for ARIS4C015.

These functions provide interpretable Pilot-0/Pilot-1 proxies for semantic
novelty and network diversity. They are intentionally *not* presented as
canonical novelty or interdisciplinarity measures.

The purpose is to create auditable feature-family baselines that can later be
compared with richer embeddings, graph models, and published novelty metrics.

Time-safety rule
----------------
Inputs must already be frozen at the historical cutoff. For example:
- prior_pair_counts must be computed only from papers available before the
  target paper/cutoff;
- citing_communities must contain only citing papers visible by cutoff;
- reference labels must come from metadata available by cutoff.

The functions cannot verify those temporal claims on their own; provenance
must be recorded by the caller.
"""

from __future__ import annotations

import itertools
import math
from collections import Counter
from dataclasses import dataclass
from typing import Hashable, Iterable, Mapping, Sequence


Label = Hashable


@dataclass(frozen=True)
class DiversityFeatures:
    n_observations: int
    n_categories: int
    shannon_entropy: float
    normalized_entropy: float
    effective_categories: float

    def as_dict(self) -> dict[str, float | int]:
        return {
            "n_observations": self.n_observations,
            "n_categories": self.n_categories,
            "shannon_entropy": self.shannon_entropy,
            "normalized_entropy": self.normalized_entropy,
            "effective_categories": self.effective_categories,
        }


@dataclass(frozen=True)
class PairNoveltyFeatures:
    n_unique_labels: int
    n_pairs: int
    unseen_pairs: int
    unseen_pair_share: float
    mean_prior_pair_count: float

    def as_dict(self) -> dict[str, float | int]:
        return {
            "n_unique_labels": self.n_unique_labels,
            "n_pairs": self.n_pairs,
            "unseen_pairs": self.unseen_pairs,
            "unseen_pair_share": self.unseen_pair_share,
            "mean_prior_pair_count": self.mean_prior_pair_count,
        }


def diversity_features(labels: Iterable[Label]) -> DiversityFeatures:
    """Compute Shannon diversity and Hill-number effective categories.

    normalized_entropy is H / log(K), with 0 for K <= 1.
    effective_categories is exp(H).
    """
    values = list(labels)
    if not values:
        return DiversityFeatures(
            n_observations=0,
            n_categories=0,
            shannon_entropy=0.0,
            normalized_entropy=0.0,
            effective_categories=0.0,
        )

    counts = Counter(values)
    n = len(values)
    probs = [count / n for count in counts.values()]
    entropy = -sum(p * math.log(p) for p in probs if p > 0)
    k = len(counts)
    normalized = entropy / math.log(k) if k > 1 else 0.0

    return DiversityFeatures(
        n_observations=n,
        n_categories=k,
        shannon_entropy=entropy,
        normalized_entropy=normalized,
        effective_categories=math.exp(entropy),
    )


def unordered_label_pairs(labels: Iterable[Label]) -> list[tuple[Label, Label]]:
    """Return unique unordered pairs from unique labels.

    Labels are ordered deterministically by their string representation so the
    result is stable even for mixed hashable types.
    """
    unique = sorted(set(labels), key=lambda x: str(x))
    return [
        (a, b)
        for a, b in itertools.combinations(unique, 2)
    ]


def canonical_pair(a: Label, b: Label) -> tuple[Label, Label]:
    """Canonicalize an unordered pair."""
    if str(a) <= str(b):
        return a, b
    return b, a


def pair_novelty_features(
    labels: Iterable[Label],
    *,
    prior_pair_counts: Mapping[tuple[Label, Label], int],
) -> PairNoveltyFeatures:
    """Compute a transparent "unseen combination" proxy.

    This is *not* the Uzzi et al. z-score novelty metric and should not be
    labeled as such. It asks only: among category pairs present in this paper,
    what share had never appeared in the supplied pre-cutoff corpus?

    prior_pair_counts must be derived from a temporally valid prior corpus.
    """
    unique_labels = sorted(set(labels), key=lambda x: str(x))
    pairs = unordered_label_pairs(unique_labels)

    if not pairs:
        return PairNoveltyFeatures(
            n_unique_labels=len(unique_labels),
            n_pairs=0,
            unseen_pairs=0,
            unseen_pair_share=0.0,
            mean_prior_pair_count=0.0,
        )

    counts = [
        int(prior_pair_counts.get(canonical_pair(a, b), 0))
        for a, b in pairs
    ]
    if any(count < 0 for count in counts):
        raise ValueError("prior pair counts must be non-negative")

    unseen = sum(1 for count in counts if count == 0)
    return PairNoveltyFeatures(
        n_unique_labels=len(unique_labels),
        n_pairs=len(pairs),
        unseen_pairs=unseen,
        unseen_pair_share=unseen / len(pairs),
        mean_prior_pair_count=sum(counts) / len(counts),
    )


def cross_field_reference_share(
    home_field: Label | None,
    reference_fields: Sequence[Label | None],
) -> float | None:
    """Share of known reference fields different from the target home field.

    Returns None if the home field is unknown or no reference field is known.
    """
    if home_field is None:
        return None
    known = [field for field in reference_fields if field is not None]
    if not known:
        return None
    return sum(field != home_field for field in known) / len(known)


def citing_community_features(
    communities: Iterable[Label],
) -> DiversityFeatures:
    """Diversity of cutoff-visible citing communities.

    Community labels must have been obtained from a graph available at the
    cutoff. A present-day community partition must not be backfilled into a
    historical benchmark without an explicit leakage analysis.
    """
    return diversity_features(communities)


def reference_field_features(
    reference_fields: Iterable[Label],
) -> DiversityFeatures:
    """Diversity of reference-field labels visible at the cutoff."""
    return diversity_features(reference_fields)

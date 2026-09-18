"""Transparent lexical novelty features for ARIS4C015.

This module provides a deliberately simple semantic-family baseline using only
historically observable document titles.

It is not a substitute for embedding novelty or published atypical-combination
metrics. Its purpose is to answer a narrower question:

    Is a target title lexically dissimilar from a pre-target reference corpus?

Design
------
- tokenize titles deterministically;
- fit IDF on the *prior corpus only*;
- represent prior and target titles using prior-corpus vocabulary;
- report nearest-neighbour cosine distance;
- separately report target token out-of-vocabulary (OOV) share.

No weighted "novelty score" is imposed. The distance and OOV channels remain
separate so later ablations can test them independently.

Historical safety
-----------------
The caller must ensure every prior-corpus document predates the target/cutoff.
Current OpenAlex field labels may still be used to define exploratory strata,
but that classification temporality must be documented separately.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence


TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "using", "use", "of",
    "in", "on", "to", "a", "an", "by", "at", "as", "is", "are", "be",
    "its", "their", "this", "that", "study", "analysis", "effect", "effects",
}


@dataclass(frozen=True)
class LexicalNoveltyFeatures:
    n_tokens: int
    n_known_tokens: int
    oov_token_share: float
    max_prior_similarity: float
    nearest1_distance: float
    nearest3_mean_similarity: float
    nearest3_distance: float

    def as_dict(self) -> dict[str, float | int]:
        return {
            "n_tokens": self.n_tokens,
            "n_known_tokens": self.n_known_tokens,
            "oov_token_share": self.oov_token_share,
            "max_prior_similarity": self.max_prior_similarity,
            "nearest1_distance": self.nearest1_distance,
            "nearest3_mean_similarity": self.nearest3_mean_similarity,
            "nearest3_distance": self.nearest3_distance,
        }


def tokenize(text: str | None) -> list[str]:
    """Deterministic lowercase alphanumeric tokenization."""
    if not text:
        return []
    return [
        token
        for token in TOKEN_RE.findall(text.lower())
        if len(token) >= 3 and token not in STOPWORDS
    ]


def fit_idf(
    documents: Iterable[str | None],
) -> tuple[dict[str, float], list[list[str]]]:
    """Fit smoothed IDF weights on prior-corpus titles only."""
    tokenized = [tokenize(doc) for doc in documents]
    n_docs = len(tokenized)
    if n_docs == 0:
        raise ValueError("prior corpus must contain at least one document")

    df: Counter[str] = Counter()
    for tokens in tokenized:
        df.update(set(tokens))

    idf = {
        token: math.log((n_docs + 1) / (freq + 1)) + 1.0
        for token, freq in df.items()
    }
    return idf, tokenized


def tfidf_vector(
    tokens: Sequence[str],
    idf: Mapping[str, float],
) -> dict[str, float]:
    """Sparse L2-normalized TF-IDF vector over the supplied vocabulary."""
    counts = Counter(token for token in tokens if token in idf)
    if not counts:
        return {}

    raw = {
        token: float(count) * float(idf[token])
        for token, count in counts.items()
    }
    norm = math.sqrt(sum(value * value for value in raw.values()))
    if norm == 0:
        return {}
    return {token: value / norm for token, value in raw.items()}


def cosine_similarity(
    left: Mapping[str, float],
    right: Mapping[str, float],
) -> float:
    """Cosine similarity for L2-normalized sparse vectors."""
    if not left or not right:
        return 0.0
    if len(left) > len(right):
        left, right = right, left
    value = sum(weight * right.get(token, 0.0) for token, weight in left.items())
    return max(0.0, min(1.0, float(value)))


def title_novelty_features(
    target_title: str | None,
    *,
    prior_titles: Sequence[str | None],
    nearest_k: int = 3,
) -> LexicalNoveltyFeatures:
    """Compute transparent target-vs-prior lexical novelty features."""
    if nearest_k < 1:
        raise ValueError("nearest_k must be >= 1")

    idf, tokenized_prior = fit_idf(prior_titles)
    target_tokens = tokenize(target_title)
    known = [token for token in target_tokens if token in idf]

    oov_share = (
        1.0 - len(known) / len(target_tokens)
        if target_tokens
        else 1.0
    )

    target_vector = tfidf_vector(target_tokens, idf)
    prior_vectors = [
        tfidf_vector(tokens, idf)
        for tokens in tokenized_prior
    ]
    similarities = sorted(
        (
            cosine_similarity(target_vector, vector)
            for vector in prior_vectors
        ),
        reverse=True,
    )

    max_similarity = similarities[0] if similarities else 0.0
    k = min(nearest_k, len(similarities))
    nearest_mean = (
        sum(similarities[:k]) / k
        if k
        else 0.0
    )

    return LexicalNoveltyFeatures(
        n_tokens=len(target_tokens),
        n_known_tokens=len(known),
        oov_token_share=oov_share,
        max_prior_similarity=max_similarity,
        nearest1_distance=1.0 - max_similarity,
        nearest3_mean_similarity=nearest_mean,
        nearest3_distance=1.0 - nearest_mean,
    )


def batch_title_novelty(
    targets: Mapping[str, str | None],
    *,
    prior_titles: Sequence[str | None],
) -> dict[str, LexicalNoveltyFeatures]:
    """Compute novelty features for multiple targets against one prior corpus.

    IDF is fitted once for efficiency and exact comparability.
    """
    idf, tokenized_prior = fit_idf(prior_titles)
    prior_vectors = [
        tfidf_vector(tokens, idf)
        for tokens in tokenized_prior
    ]

    result: dict[str, LexicalNoveltyFeatures] = {}
    for paper_id, title in targets.items():
        target_tokens = tokenize(title)
        known = [token for token in target_tokens if token in idf]
        oov_share = (
            1.0 - len(known) / len(target_tokens)
            if target_tokens
            else 1.0
        )
        target_vector = tfidf_vector(target_tokens, idf)
        similarities = sorted(
            (
                cosine_similarity(target_vector, vector)
                for vector in prior_vectors
            ),
            reverse=True,
        )
        max_similarity = similarities[0] if similarities else 0.0
        k = min(3, len(similarities))
        nearest_mean = sum(similarities[:k]) / k if k else 0.0
        result[paper_id] = LexicalNoveltyFeatures(
            n_tokens=len(target_tokens),
            n_known_tokens=len(known),
            oov_token_share=oov_share,
            max_prior_similarity=max_similarity,
            nearest1_distance=1.0 - max_similarity,
            nearest3_mean_similarity=nearest_mean,
            nearest3_distance=1.0 - nearest_mean,
        )
    return result

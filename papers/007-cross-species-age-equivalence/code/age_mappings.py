"""Core deterministic age transformations for ARIS4C007.

These functions define *candidate coordinates*, not biological ground truth.
They intentionally separate:
- maximum-lifespan relative age (Lu et al. Clock 2 transform input), and
- gestation/maturity log-linear age (Lu et al. Clock 3 transform input).

All time inputs are years.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log
from typing import Iterable


@dataclass(frozen=True)
class SpeciesTime:
    name: str
    gestation_y: float
    maturity_y: float
    max_lifespan_y: float

    def validate(self) -> None:
        if self.gestation_y <= 0:
            raise ValueError(f"{self.name}: gestation_y must be > 0")
        if self.maturity_y <= 0:
            raise ValueError(f"{self.name}: maturity_y must be > 0")
        if self.max_lifespan_y <= 0:
            raise ValueError(f"{self.name}: max_lifespan_y must be > 0")


def relative_age(age_y: float, species: SpeciesTime) -> float:
    """Lu et al. Clock-2 relative-age coordinate before loglog transform.

    RelativeAge = (Age + GestationT) / (MaxLifespan + GestationT)
    """
    species.validate()
    return (age_y + species.gestation_y) / (
        species.max_lifespan_y + species.gestation_y
    )


def age_from_relative(relative: float, species: SpeciesTime) -> float:
    species.validate()
    return relative * (species.max_lifespan_y + species.gestation_y) - species.gestation_y


def map_by_relative_age(
    age_y: float, source: SpeciesTime, target: SpeciesTime
) -> float:
    return age_from_relative(relative_age(age_y, source), target)


def loglog_relative_age(age_y: float, species: SpeciesTime) -> float:
    """Clock-2 modeled outcome: -log(-log(RelativeAge)).

    Defined only for 0 < RelativeAge < 1. Ages beyond the species maximum are
    intentionally rejected for confirmatory use.
    """
    r = relative_age(age_y, species)
    if not 0 < r < 1:
        raise ValueError("loglog relative age requires 0 < relative age < 1")
    return -log(-log(r))


def m_hat(species: SpeciesTime) -> float:
    """Published Clock-3 m-hat parameter.

    m_hat = 5.0 * (GestationT / ASM)^0.38
    """
    species.validate()
    return 5.0 * (species.gestation_y / species.maturity_y) ** 0.38


def relative_adult_age(age_y: float, species: SpeciesTime) -> float:
    species.validate()
    return (age_y + species.gestation_y) / (
        species.maturity_y + species.gestation_y
    )


def loglinear_coordinate(age_y: float, species: SpeciesTime) -> float:
    """Lu et al. Clock-3 log-linear age coordinate."""
    x = relative_adult_age(age_y, species)
    m = m_hat(species)
    z = x / m
    if z <= 0:
        raise ValueError("log-linear coordinate requires positive transformed age")
    return z - 1.0 if z >= 1.0 else log(z)


def age_from_loglinear(y: float, species: SpeciesTime) -> float:
    """Inverse of the Clock-3 log-linear age transform."""
    m = m_hat(species)
    x = m * (y + 1.0) if y >= 0 else m * exp(y)
    return x * (species.maturity_y + species.gestation_y) - species.gestation_y


def map_by_loglinear(
    age_y: float, source: SpeciesTime, target: SpeciesTime
) -> float:
    """Map age by equating the published Clock-3 transformed coordinate.

    This is a benchmark construct. It must not be described as validated
    physiological equivalence without independent evidence.
    """
    return age_from_loglinear(loglinear_coordinate(age_y, source), target)


def monotonic_grid(
    species: SpeciesTime, fractions: Iterable[float] = (0.05, 0.25, 0.5, 0.75, 0.95)
) -> list[tuple[float, float, float]]:
    """Return age, relative-age, and log-linear coordinates for QC."""
    out = []
    for frac in fractions:
        age = frac * species.max_lifespan_y
        out.append((age, relative_age(age, species), loglinear_coordinate(age, species)))
    return out

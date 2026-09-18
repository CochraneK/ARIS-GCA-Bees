# SAMPLE SIZE DECISION — ARIS4C005

**Date:** 2026-09-18

## Decision

For the confirmatory population-random adjudication arm:

- **5,000 random works = minimum viable target**
- **10,000 random works = preferred target when AI adjudication is operational**

The original 600-work random component remains a pilot/engineering sample, not the final confirmatory prevalence sample.

---

## Why 600 is too small

From the design simulation (`data/pilot/prevalence_design_summary.json`):

| hypothetical true prevalence | n=600 expected positives | n=600 P(0 positives) | median 95% posterior width |
|---:|---:|---:|---:|
| 0.2% | 1.2 | 30.1% | 0.758 percentage points |
| 0.5% | 3.0 | 4.94% | 1.187 percentage points |
| 1.0% | 6.0 | 0.24% | 1.631 percentage points |

At the rare prevalences most relevant to severe article-level failures, 600 random works do not provide stable precision.

---

## What 5,000 buys

| hypothetical true prevalence | expected positives | median 95% posterior width |
|---:|---:|---:|
| 0.2% | 10 | 0.252 percentage points |
| 0.5% | 25 | 0.393 percentage points |
| 1.0% | 50 | 0.550 percentage points |
| 2.0% | 100 | 0.777 percentage points |

5,000 is therefore a practical lower bound if the goal is a publishable random-audit anchor rather than merely testing infrastructure.

---

## Why 10,000 is preferred under AI adjudication

At 10,000 random works:

- 0.2% prevalence -> ~20 expected positives
- 0.5% prevalence -> ~50 expected positives
- 1.0% prevalence -> ~100 expected positives

This materially improves precision and allows better field/year heterogeneity checks.

Because the user plans to use another model for adjudication, annotation cost scales differently from a human-only design. The design should exploit that by increasing the random audit rather than using AI only to increase enrichment.

---

## Critical caveat: more N does not solve AI misclassification

Rare-event prevalence makes specificity the limiting factor.

For example, under a hypothetical true prevalence of 0.5% and AI sensitivity of 90%:

- specificity 99.0% -> PPV about 31%
- specificity 99.5% -> PPV about 47%
- specificity 99.9% -> PPV about 82%
- specificity 99.95% -> PPV about 90%

Therefore a large AI-labelled random sample cannot be treated as direct truth unless model specificity is extraordinarily high or measurement error is explicitly modeled.

Design requirement:

> Increase random N **and** calibrate/sensitivity-test AI adjudicator error.

---

## Final confirmatory architecture

Preferred:

1. 10,000 population-random works over the full 2000–2025 target universe;
2. additional detector-enriched cases for sensitivity/specificity estimation;
3. two blinded AI adjudicators;
4. arbitration for disagreement/low-confidence/indeterminate cases;
5. anchor calibration against formal/high-confidence evidence cases;
6. latent model that treats adjudicator outputs as noisy measurements.

Minimum viable:

1. 5,000 population-random works;
2. the same calibrated AI architecture;
3. narrower heterogeneity claims.

---

## Not allowed

- Do not call 600 works the final global audit.
- Do not replace the random arm with only high-risk enrichment.
- Do not assume dual-AI agreement has sensitivity=specificity=1.
- Do not use sample size to compensate for unmeasured classifier bias.

# NETWORK MODEL — ARIS4C004

Date frozen for pilot architecture: 2026-09-18

## Core decision

ARIS4C004 does **not** treat the first 13 network-observable historical people as nodes in one common citation network and compare their raw centrality.

They span different periods and subfields, and the clean pilot currently shows no cross-person citation edges among the focal works. A forced pooled focal graph would therefore measure field/time composition more than counterfactual contribution.

The primary analytic object is instead a **person-specific temporal ego network**:

```text
predecessor works / prior knowledge
            ↓
       focal clean works
            ↓
  downstream citing works
            ↓
 later descendants / diffusion
```

Coauthor, institution and topic layers are retained as complementary multiplex information.

## Why ego networks

The causal intervention is person-specific participation attenuation:

`do(P_i(t >= t0) = attenuated)`

Therefore the natural graph is the local knowledge system exposed to person `i`, not a synthetic graph in which unrelated mathematicians, metallurgists, archaeologists and social theorists are expected to cite each other.

## Pilot graph layers

### L1 — focal clean-work layer

Only work nodes passing identity/work gates.

- historical person is VERIFIED;
- person is `network_observable=true`;
- work is inside the clean corpus;
- explicit work decisions override raw OpenAlex attribution.

### L2 — incoming downstream citation layer

For deterministic anchor works, acquire works satisfying OpenAlex `cites:<anchor_work_id>` within a fixed post-publication horizon.

Knowledge-flow direction:

`anchor/cited work -> later citing work`

A time-reversed edge is quarantined and never enters the temporal graph.

### L3 — predecessor/reference layer

The focal work's `referenced_works` represents prior knowledge exposure.

Direction for knowledge flow:

`referenced predecessor -> focal work`

This layer supports alternative-precursor/substitution modeling.

### L4 — collaboration layer

Authorship relations generate:

`person/work <-> coauthor`

This is not interchangeable with citation influence. It is used for collaborator exposure, substitution candidates and robustness analyses.

### L5 — topic/institution context

Topics and institutions characterize field/time opportunity sets and can help select matched comparison/substitution candidates. They are contextual attributes/layers, not causal outcomes by default.

## Temporal rules

1. No citation edge with source publication year later than target publication year enters the temporal graph.
2. Same-year edges are retained only with topological/cycle checks in simulation.
3. Reprints/modern manifestations do not create new historical production nodes under `WORK_CODEBOOK.md`.
4. All intervention logic uses information available at or before the simulated time; no future-lookahead substitute selection.

## Standard downstream window

Pilot default:

- deterministic anchors per person: 6 maximum;
- anchor composition: earliest + temporal median + latest + highest-cited remaining;
- downstream window: 20 years after anchor publication, censored at study end 2026;
- maximum incoming citing works per anchor in feasibility pilot: 50;
- acquisition order: earliest citing works first.

These are **feasibility parameters**, not yet final confirmatory values.

Sensitivity design should later compare multiple horizons, e.g. 10 / 20 / 40 years, subject to historical censoring.

## Why anchor sampling is used in feasibility

A person such as James S. Albus has hundreds of clean works, while others have only a handful. Pulling every descendant for prolific people during feasibility would measure API budget and publication volume rather than graph viability.

Anchor sampling therefore asks:

> Does a reproducible, temporally ordered downstream neighborhood exist at all across heterogeneous historical contributors?

Full confirmatory graph acquisition can be scaled after this gate.

## Comparability across people and fields

Never compare raw graph size/degree alone across historical figures.

Primary comparisons should use standardized or matched quantities such as:

- CPE relative to observed ego-network value;
- percentage of downstream reachable value lost/recovered;
- recovery half-life / rediscovery delay;
- replacement rate;
- normalized brokerage/efficiency within the local field-time opportunity set;
- change in topic diversity relative to matched controls;
- effect rank/percentile within era × field × visibility comparison sets.

Raw node count, citations and centrality remain descriptive diagnostics.

## Focal-only internal citation graph

The focal clean-work graph is useful for QC, not the final causal network.

Pilot observation:

- focal people: 13;
- clean works: 693;
- clean-work citation edges exist mainly/entirely within the same focal person's corpus;
- focal-to-focal cross-person citation density is therefore not a meaningful feasibility requirement.

A zero cross-person focal edge count does **not** imply zero societal influence. It implies that downstream external neighborhoods are the appropriate graph expansion.

## Downstream feasibility gate

Before expanding identity resolution from 30 to all 100 frozen candidates, establish that the 13-person clean frame supports reproducible downstream acquisition.

Desired evidence is descriptive rather than a hard p-value gate:

- most focal people have at least one anchor with downstream citers;
- enough people have nontrivial downstream work sets for graph simulation;
- citation lags are temporally plausible;
- API errors are rare/recoverable;
- downstream metadata preserve author/topic/institution context;
- results are not driven solely by one prolific focal person.

If this fails for older/book-heavy domains, the design should branch to domain-appropriate influence edges rather than pretending OpenAlex citation coverage is universal.

## Future expansion

Once one-hop feasibility passes:

1. acquire full clean focal works or a preregistered anchor strategy;
2. acquire first-hop citing works;
3. optionally acquire second-hop descendants under a bounded horizon;
4. fetch metadata for referenced predecessors;
5. construct substitution sets using contemporaneous field/topic/coauthor/institution information;
6. run M0/M1/M2 counterfactual simulations;
7. standardize person-level effects before exposed/comparison contrasts.

## Exposure firewall

All network acquisition, graph cleaning, anchor rules and feasibility decisions above are fixed **before mental-health exposure coding**.

Mental-health evidence must not determine:

- who gets an ego network;
- which works are retained;
- which anchor works are chosen;
- how far downstream the graph is expanded;
- which graph metric is selected because it makes a focal case look important.

# Hierarchical tool-use layer · ARIS4C008

**Source:** Johnston & Røyrvik (2020), open data/code repository `StochasticBiology/tool-use`, based on the 22 Shumaker et al. tool-use modes.

## Source coding

In the main taxon matrix:
- `2` = a mode observed in the wild;
- `1` = an observation where human influence cannot be discounted;
- `0` = no observation of that mode in the source catalogue.

The source pipeline itself converts 2→1 for “total observed” analyses and removes 1 for “wild only” analyses.

**ARIS4C008 does not interpret 0 as tested absence or inability.**

## Resolution relevant to the v2 panel

The source provides exact named rows for:
- *Pan troglodytes*;
- *Pan paniscus*;
- *Pongo pygmaeus*;
- *Gorilla gorilla*.

Other relevant rows are higher-level:
- Platyrrhini;
- Cercopithecidae;
- Cetacea;
- Elephantidae;
- Aves;
- Insecta;
- Cephalopoda.

The repository also includes a bird family-level presence matrix, allowing narrower contextual evidence for:
- Corvidae;
- Cacatuidae;
- Psittacidae;
- Columbidae.

## Role in module D

This layer is useful for:
- tool-use breadth;
- wild versus human-influenced evidence;
- broad comparative motor/manipulation architecture;
- selecting taxa that differ in tool-use configuration.

It is **not** sufficient to create exact-species D scores for taxa represented only at family/order/class level. Those values are retained as priors/context and sensitivity information.

The strongest exact-species D matrix will still require source-level coding of:
- manufacture versus use;
- multi-step/composite use;
- tool transport;
- persistent modification;
- wild/captive context.

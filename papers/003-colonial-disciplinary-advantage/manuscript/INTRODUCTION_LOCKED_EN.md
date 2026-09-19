# Introduction — pre-result locked draft

**Status:** written before inspection of ARIS4C003 confirmatory effect estimates.

Scientific systems are geographically unequal, but inequality in aggregate
research volume is only one dimension of that geography. Countries also differ
in the *composition* of their scientific portfolios: some exhibit persistent
relative specialization in medicine, agriculture, engineering, the social
sciences, or other domains even after differences in overall research scale are
taken into account. Scientometric research has long measured these patterns
using revealed-comparative-advantage and related specialization indices
(Harzing & Giroud, 2014; Abramo et al., 2022), and more recent work treats
disciplinary portfolios as a structured “science space” rather than a set of
independent subject silos. What remains less clear is how far such
cross-disciplinary structure can be linked to historical institutions that
predate contemporary research policy.

Empire and colonialism are plausible sources of long-run scientific path
dependence because they organized knowledge unevenly across both places and
fields. Colonial states did not simply consume generic “science.” They created
or expanded particular surveys, schools, laboratories, museums, archives,
medical services, agricultural stations, geological departments, census
systems, legal-administrative institutions, and field networks. These
infrastructures generated careers, data, collections, professional societies,
training routes, and transnational connections whose institutional lives often
outlasted formal imperial rule. The relevant historical hypothesis is therefore
not that colonialism uniformly increased scientific capacity, nor that
disciplines can be morally classified as colonial or non-colonial. It is that
different disciplines became entangled with imperial institutions to different
degrees, and that such unequal historical entanglement may have left a
measurable imprint on the *shape* of later scientific systems.

There is already substantial precedent for parts of this argument. Histories of
anthropology, geography, tropical medicine, archaeology, geology, agriculture,
sociology, census administration, and other fields document specific
relationships between disciplinary development and imperial institutions. For
example, Steinmetz (2013) shows that postwar British sociology was connected to
colonial social-science funding, research institutes, colonial universities,
and the training of colonial officials. Similar historical literatures trace
imperial survey and mapping infrastructures in geography and geology,
missionary and administrative language documentation in linguistics, colonial
medical services in tropical medicine and public health, and crop-transfer,
botanic-garden, plantation, and forestry networks in the agricultural sciences.

Quantitative studies also make clear that the generic proposition “colonial
history still affects science” is not novel. Nagtegaal and de Bruin (1994)
quantified neo-colonial patterns in the global scientific collaboration network.
Boshoff (2009) documented pronounced former-colonial collaboration patterns in
Central Africa. Later country-pair studies have included colonial relationships
and common language in models of scientific collaboration, while field-specific
work has shown that historical ties can shape research funding and contemporary
knowledge-production networks. Raja et al. (2022), for example, demonstrated
that colonial history and present-day economic inequality distort the
geography of palaeontological knowledge production. More recent studies have
reported historical-tie effects in African research collaboration and in
specific domains such as fisheries and infectious-disease research.

A separate literature measures national scientific specialization without
making colonial history its central explanatory object. Harzing and Giroud
(2014) adapted competitive-advantage reasoning to national academic profiles,
and Abramo et al. (2022) mapped scientific comparative advantage across 199
countries and 254 subject categories. These studies establish that countries
possess meaningful relative disciplinary profiles and that revealed
specialization is not itself a new construct.

The present study links these literatures by asking a narrower question:
**does historical colonial exposure predict a systematic cross-disciplinary
gradient in contemporary scientific activity as a function of how deeply each
discipline was historically entangled with imperial and colonial systems?**

To make that question testable without defining “colonial disciplines” after
observing modern performance, we construct an outcome-blind
Imperial/Colonial Knowledge Entanglement Score (IKES). Twenty-one conceptual
disciplines were fixed before contemporary outcomes were opened. Each was coded
on eleven historical mechanisms, including colonial administrative demand,
survey and mapping, population classification, overseas field sites,
resource extraction, colonial health governance, agriculture and ecological
transfer, institutional transplantation, collections and archives,
missionary-linguistic networks, and postwar development-administration
continuity. Two independent coding processes were completed before modern
outcomes were materialized. Only missing cells or coder disagreements of at
least two points were adjudicated, using historical evidence, and the final
matrix was then cryptographically frozen.

This construction permits three related but distinct tests. First, among
former-colony countries, we ask whether historical colonial duration is
associated with the relative contemporary production of work in disciplines
with higher IKES. Second, we ask whether the same gradient appears in
field-normalized citation impact. Third, at the dyadic level, we ask whether
country pairs connected by a former colonial/dependency relationship
collaborate disproportionately in more historically entangled disciplines.
These outcomes correspond to different possible forms of persistence:
disciplinary production capacity, scientific influence, and international
knowledge-network structure.

The design deliberately avoids collapsing these outcomes into a single
“scientific advantage” score. A production gradient without an impact gradient
would have a different interpretation from a collaboration gradient without a
domestic specialization gradient. Similarly, the study separates the scalable
former-colony and dyadic analyses from a small-N comparison of eight European
overseas imperial centers. Repeated disciplines do not create additional
independent imperial histories; the imperial-center analysis is therefore used
only as corroboration.

The empirical analysis uses a pinned OpenAlex public snapshot, fractional
country and pair attribution, an explicitly completed zero-cell grid, and
Poisson pseudo-maximum-likelihood models with high-dimensional fixed effects.
The confirmatory family contains exactly three 2019–2022 interaction
coefficients: former-colony output, former-colony field-normalized Top-10%
impact, and former-colonial-tie collaboration. Because only 21 disciplines are
included, clustered asymptotic inference is supplemented by 21
leave-one-discipline-out refits and 999 fixed-seed IKES-label permutations.
Prespecified temporal profiles assess whether the estimated cross-disciplinary
association attenuates, persists, strengthens, or changes non-monotonically
across 2007–2010, 2011–2014, 2015–2018, and 2019–2022.

The contribution is therefore not a new claim that colonial history matters for
science, nor a new measure of national scientific specialization. Its
provisional novelty lies in combining: (1) historical country and dyadic
exposure; (2) an independently coded, outcome-blind discipline-level
entanglement construct; (3) a frozen broad discipline set; and (4) multiple
contemporary outcome families in a single cross-disciplinary interaction
framework. This design turns a qualitative path-dependence argument into a
falsifiable question: if the proposed historical gradient is real, it should
appear systematically across disciplines ordered by a characteristic coded
without access to present-day scientific performance. If it does not, the
frozen design provides an equally interpretable null test of that broad
hypothesis.

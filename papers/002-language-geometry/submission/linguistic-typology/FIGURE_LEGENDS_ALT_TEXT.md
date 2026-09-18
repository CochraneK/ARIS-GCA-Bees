# Figure legends and alt text · Linguistic Typology submission

## Figure 1. Family-held-out predictive ranking across representations

Mean Spearman correlation between model-predicted and independently estimated held-out feature-association matrices for TLI, GBI, and WALS. In each representation, the hierarchical-tree benchmark exceeds the directly optimized circular model. Absolute magnitudes should not be compared directly across datasets because feature definitions, sparsity, curation, and selection differ.

**Alt text:** Grouped bar chart with three dataset groups. TLI shows tree 0.182 and optimized circle 0.109; GBI shows tree 0.122 and circle 0.073; WALS shows tree 0.603 and circle 0.410. In all three groups the tree bar is higher than the circular-model bar.

## Figure 2. TLI repeated family-held-out paired contrasts

Paired differences in held-out Spearman correlation across 20 TLI top-level-family hold-out splits. Points show mean differences and error bars show 95% bootstrap intervals obtained by resampling the split-level paired contrasts. These intervals summarize sensitivity to the sampled splits and are not phylogenetic uncertainty intervals.

**Alt text:** Horizontal point-and-interval plot comparing three paired contrasts with optimized circle. Tree minus circle is +0.073 with 95% interval 0.055 to 0.092; low-rank minus circle is +0.046 with interval 0.033 to 0.061; Euclidean minus circle is +0.001 with interval −0.020 to 0.021. The first two intervals lie fully above zero; the Euclidean interval crosses zero.

## Figure 3. Held-out circular-Robinson-style sensitivity

Mean row-unimodality violation for the learned circular order, an average-linkage tree leaf order, and random orders at 40 and 60 TLI features; lower is better. The circular order improves on random order but does not outperform the tree order. This is a noisy-data sensitivity inspired by circular-Robinson characterization, not an exact strict-recognition test.

**Alt text:** Grouped bar chart for 40 and 60 features. At 40 features, mean violation is 0.222 for circular order, 0.209 for tree leaf order, and 0.237 for random order. At 60 features, values are 0.297, 0.284, and 0.307 respectively. Lower values indicate better row-unimodality; tree is lowest in both feature counts.

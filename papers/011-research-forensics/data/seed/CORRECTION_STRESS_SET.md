# Correction / corrigendum honest-error stress seed

Captured: 2026-09-18

Purpose: provide **GT-B documented error controls** for ARIS4C011. These records are not "negative because nothing is wrong"; they are deliberately known to contain a real published error that was later corrected. They test whether Research Forensics can surface an anomaly **without escalating the existence of an error into an allegation of misconduct**.

## Seed cases

### PLOS ONE — switched figure panels

Target DOI: 10.1371/journal.pone.0161231  
Correction DOI: 10.1371/journal.pone.0301214

The correction states that Fig. 1B and Fig. 1C were incorrectly switched. This is useful because a legitimate correction can look superficially similar to an image-integrity concern, yet the correction itself supplies no basis for inferring intent.

### Nature Catalysis — incorrect scientific content in a figure

Target DOI: 10.1038/s41929-026-01569-w  
Correction DOI: 10.1038/s41929-026-01591-y

The correction states that Fig. 6a showed an atop site when it should have shown a hollow site. This case is important because "image error" is broader than duplication/manipulation: a visually unique image can still encode the wrong scientific object.

### Shoulder & Elbow — missing row in a ranked table

Target DOI: 10.1177/1758573221989669  
Erratum DOI: 10.1177/17585732221124203

The erratum states that information for rank 14 was missing from a table of the fifty most cited papers. This is a direct F3 table-consistency case: a structured rank-sequence checker can flag the gap while the framework still labels the finding as a reporting/display inconsistency, not misconduct.

## Design implication

A benchmark with only retractions and no correction/error stratum cannot test false escalation. ARIS4C011 therefore evaluates at least two questions separately:

1. Did the detector surface the documented anomaly?
2. Did the synthesis layer preserve the distinction between anomaly/error and misconduct?

## Sources

- https://pmc.ncbi.nlm.nih.gov/articles/PMC10956798/
- https://www.nature.com/articles/s41929-026-01591-y
- https://journals.sagepub.com/doi/10.1177/17585732221124203
- Crossref update-type=correction production API, queried 2026-09-18.

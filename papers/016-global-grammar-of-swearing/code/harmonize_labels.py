#!/usr/bin/env python3
"""Conservative label harmonization for ARIS4C016.

This module maps only high-confidence raw annotation labels onto orthogonal
ontology axes. It deliberately leaves ambiguous/local labels unresolved.
"""

ALIASES = {
    "sexualual references": "sexual references",
    "scathological": "scatological",
    "forbiden chemicals": "forbidden chemicals",
    "innapropriate question": "inappropriate question",
    "interjections": "interjection",
}

HIGH_CONFIDENCE = {
    "sexual": [("semantic_source", "SEX_SEXUALITY")],
    "sexual references": [("semantic_source", "SEX_SEXUALITY")],
    "sexualbehavior": [("semantic_source", "SEX_SEXUALITY")],
    "sexualrelated": [("semantic_source", "SEX_SEXUALITY")],
    "sexualorgan": [("semantic_source", "GENITAL_BODY")],
    "genitals": [("semantic_source", "GENITAL_BODY")],
    "nipple": [("semantic_source", "GENITAL_BODY")],
    "menstruation": [("semantic_source", "GENITAL_BODY")],
    "scatological": [("semantic_source", "EXCRETION_DISGUST")],
    "blasphemy": [("semantic_source", "RELIGION_SACRED")],
    "religion": [("semantic_source", "RELIGION_SACRED")],
    "medical": [("semantic_source", "DEATH_DISEASE")],
    "illness": [("semantic_source", "DEATH_DISEASE")],
    "disease": [("semantic_source", "DEATH_DISEASE")],
    "death": [("semantic_source", "DEATH_DISEASE")],
    "stupidity": [("semantic_source", "INTELLIGENCE_COMPETENCE")],
    "physical appearance": [("semantic_source", "APPEARANCE_ABILITY")],
    "appearance": [("semantic_source", "APPEARANCE_ABILITY")],
    "violence": [("semantic_source", "VIOLENCE_HARM")],
    "drugs": [("semantic_source", "SUBSTANCE_ILLEGALITY")],
    "substance": [("semantic_source", "SUBSTANCE_ILLEGALITY")],
    "forbidden chemicals": [("semantic_source", "SUBSTANCE_ILLEGALITY")],
    "political": [("semantic_source", "POLITICS_HISTORY")],
    "ideology": [("semantic_source", "POLITICS_HISTORY")],
    "wwii": [("semantic_source", "POLITICS_HISTORY")],
    "nazi": [("semantic_source", "POLITICS_HISTORY")],
    "yugoslavia": [("semantic_source", "POLITICS_HISTORY")],
    "family": [("semantic_source", "KINSHIP_ANCESTRY")],
    "ancestry": [("semantic_source", "KINSHIP_ANCESTRY")],
    "animal": [("semantic_source", "ANIMAL_DEHUMANIZATION")],
    "insult": [("pragmatic_function", "DIRECT_INSULT")],
    "curse (wishing bad things to someone)": [("pragmatic_function", "CURSE_WISH_HARM")],
    "curse": [("pragmatic_function", "CURSE_WISH_HARM")],
    "interjection": [("pragmatic_function", "EXPLETIVE_INTERJECTION")],
    "exclamation": [("pragmatic_function", "EXPLETIVE_INTERJECTION")],
    "racial": [("social_indexical_basis", "RACE_ETHNICITY_NATIONALITY")],
    "lgbtq": [("social_indexical_basis", "SEXUAL_ORIENTATION")],
    "homophobia": [("social_indexical_basis", "SEXUAL_ORIENTATION")],
    "misogyny": [("social_indexical_basis", "GENDER_SEX")],
    "disablement": [("social_indexical_basis", "DISABILITY_HEALTH")],
    "senior": [("social_indexical_basis", "AGE")],
    "euphemism": [("linguistic_form", "EUPHEMISM_MINCED")],
}

# Important intentionally unresolved examples include:
# slur, abuse, negative condition, behavioral, local abbreviations and
# community-specific historical/social labels. These require context/native
# review and must not be silently forced into a global ontology.


def normalize_label(raw: str | None) -> str:
    value = (raw or "").strip().lower()
    return ALIASES.get(value, value)


def map_label(raw: str | None) -> dict:
    normalized = normalize_label(raw)
    if not normalized:
        return {"raw": raw or "", "normalized": "", "status": "MISSING", "mappings": []}
    mappings = HIGH_CONFIDENCE.get(normalized)
    if mappings is None:
        return {
            "raw": raw or "",
            "normalized": normalized,
            "status": "UNRESOLVED",
            "mappings": [],
        }
    return {
        "raw": raw or "",
        "normalized": normalized,
        "status": "HIGH_CONFIDENCE",
        "mappings": [
            {"axis": axis, "value": value} for axis, value in mappings
        ],
    }

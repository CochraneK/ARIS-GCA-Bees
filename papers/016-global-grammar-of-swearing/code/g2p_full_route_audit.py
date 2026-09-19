#!/usr/bin/env python3
"""Full-route technical pronunciation audit for ARIS4C016.

Routes:
- English: Epitran eng-Latn (requires lex_lookup on PATH).
- Mandarin/Cantonese: source Study-1 romanization -> cmn-Latn/yue-Latn.
- Other samples: language/script Epitran routes.

Outputs aggregate counts only. No lexical form or IPA string is emitted.
"""

from __future__ import annotations
import csv, hashlib, io, json, math, re, shutil, unicodedata, urllib.request
from collections import Counter, defaultdict

GUID="8nyga"
VIEW_ONLY="60b964248cc64a8793a9013075132a1c"
SHA256="c725a30913e604e8344f4990c8d63990dcf0271e3a65765ddc3fa591b8cb1387"

ORTH_CODES={
 "Dutch (BE)":"nld-Latn","English (AU)":"eng-Latn","English (CA)":"eng-Latn",
 "English (GB)":"eng-Latn","English (SG)":"eng-Latn","English (US)":"eng-Latn",
 "Finnish (FI)":"fin-Latn","French (FR)":"fra-Latn","German (DE)":"deu-Latn",
 "Italian (IT)":"ita-Latn","Setswana (BW)":"tsn-Latn","Slovenian (SI)":"slv-Latn",
 "Spanish (CL)":"spa-Latn","Spanish (ES)":"spa-Latn","Thai (TH)":"tha-Thai",
}
CYRILLIC_RE=re.compile(r"[\u0400-\u04FF]")

def load():
    url=f"https://osf.io/download/{GUID}/?view_only={VIEW_ONLY}"
    with urllib.request.urlopen(url,timeout=120) as response:
        blob=response.read()
    digest=hashlib.sha256(blob).hexdigest()
    if digest!=SHA256:
        raise RuntimeError(f"Study-1 checksum mismatch: {digest}")
    return list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig",errors="replace"))))

def has_mixed_letter_scripts(text):
    scripts=set()
    for ch in text:
        if not ch.isalpha(): continue
        name=unicodedata.name(ch,"")
        for script in ("LATIN","CYRILLIC","THAI","CJK","HIRAGANA","KATAKANA"):
            if script in name:
                scripts.add(script);break
    return len(scripts)>1

def route(row):
    sample=row["lang"]
    if sample=="Cantonese (CN)":
        return "source_romanization","yue-Latn",(row.get("transcription") or "").strip(),True
    if sample=="Mandarin (CN)":
        return "source_romanization","cmn-Latn",(row.get("transcription") or "").strip(),True
    word=(row.get("word_clean") or "").strip()
    if sample=="Serbian (RS)":
        return "orthography",("srp-Cyrl" if CYRILLIC_RE.search(word) else "srp-Latn"),word,False
    return "orthography",ORTH_CODES[sample],word,False

def main():
    import epitran
    rows=load()
    engines={}
    errors={}
    counts=defaultdict(Counter)

    def engine(code,tones=False):
        key=(code,tones)
        if key not in engines:
            try:
                engines[key]=epitran.Epitran(code,tones=tones)
            except Exception as exc:
                errors[str(key)]=f"{type(exc).__name__}: {exc}"
                raise
        return engines[key]

    for row in rows:
        sample=row["lang"]; c=counts[sample]; c["rows"]+=1
        route_name,code,text,tones=route(row)
        c[f"ROUTE_{route_name.upper()}"]+=1
        if not text:
            c["MISSING_ROUTE_INPUT"]+=1
            continue
        if route_name=="orthography" and any(ch.isspace() for ch in text):
            c["LEXICAL_MULTIWORD"]+=1
        if route_name=="source_romanization" and any(ch.isspace() for ch in text):
            c["ROMANIZATION_WHITESPACE"]+=1
        if has_mixed_letter_scripts(text):
            c["MIXED_SCRIPT"]+=1
        try:
            ipa=engine(code,tones=tones).transliterate(text)
            if ipa and any(ch.isalpha() for ch in ipa):
                c["TECHNICAL_SUCCESS"]+=1
            else:
                c["EMPTY_OR_NONLETTER_OUTPUT"]+=1
        except Exception:
            c["BACKEND_ERROR"]+=1

    total=Counter()
    output={
      "project":"ARIS4C016",
      "audit_type":"full_route_technical_pronunciation_coverage",
      "source_sha256":SHA256,
      "epitran_version":getattr(epitran,"__version__","unknown"),
      "lex_lookup_on_path":bool(shutil.which("lex_lookup")),
      "samples":{},
      "engine_errors":errors,
      "privacy_note":"No lexical forms or IPA strings are emitted."
    }
    for sample in sorted(counts):
        d=dict(counts[sample])
        for k,v in d.items(): total[k]+=v
        d["technical_success_rate_all_rows"]=round(d.get("TECHNICAL_SUCCESS",0)/d["rows"],4)
        output["samples"][sample]=d
    total_rows=total["rows"]
    output["overall"]={
      **dict(total),
      "technical_success_rate_all_rows":round(total.get("TECHNICAL_SUCCESS",0)/total_rows,6)
    }
    print(json.dumps(output,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()

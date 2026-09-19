"""Validate generated human calibration forms."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
FORMS=ROOT/"data"/"human_forms"/"forms.generated.json"


def main():
    payload=json.loads(FORMS.read_text(encoding="utf-8"))
    forms=payload["forms"]
    assert len(forms)==108
    assert Counter(f["protocol"] for f in forms)=={"P2":36,"P3":36,"P6":36}

    exposure={"P2":Counter(),"P3":Counter(),"P6":Counter()}
    for form in forms:
        assert form["main_trial_count"]==84
        assert form["retest_trial_count"]==8
        assert form["presented_trial_count"]==92
        assert len(form["items"])==92

        main=[x for x in form["items"] if not x["is_retest"]]
        retest=[x for x in form["items"] if x["is_retest"]]
        assert len(main)==84
        assert len(retest)==8
        assert len({x["pair_id"] for x in main})==84
        assert sum(x["source"]=="lexical" for x in main)==60
        assert sum(x["source"]=="mixed_stress" for x in main)==24

        for x in main:
            exposure[form["protocol"]][x["pair_id"]]+=1

        for a,b in zip(form["items"],form["items"][1:]):
            assert a["pair_id"]!=b["pair_id"], f"immediate duplicate in {form['form_id']}"

    for protocol in ("P2","P3","P6"):
        lex=[v for k,v in exposure[protocol].items() if k.startswith("oewn2025:")]
        mixed=[v for k,v in exposure[protocol].items() if not k.startswith("oewn2025:")]
        assert set(lex)=={3}, (protocol,set(lex))
        assert set(mixed)=={4}, (protocol,set(mixed))

    print("PASS human form validation")
    print("forms: 108")
    print("P2/P3/P6 forms: 36/36/36")
    print("main/retest/presented per form: 84/8/92")
    print("lexical pair exposure per protocol: 3")
    print("mixed pair exposure per protocol: 4")


if __name__=="__main__":
    main()

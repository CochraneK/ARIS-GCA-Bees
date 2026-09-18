"""Live no-key Companies House URI smoke for ARIS4C014."""

from __future__ import annotations

import json
from urllib.request import Request, urlopen

from companies_house_uri import normalize_companies_house_uri


COMPANY = "02050399"
URL = f"http://data.companieshouse.gov.uk/doc/company/{COMPANY}.json"


def main() -> None:
    req = Request(
        URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "ARIS4C014-OpenIntegrity/0.1 company-uri-smoke",
        },
    )
    with urlopen(req, timeout=45) as response:
        data = json.loads(response.read().decode("utf-8"))
    entity, meta = normalize_companies_house_uri(data, source_url=URL)
    output = {
        "source": "Companies House URI",
        "company_number_matches": entity.entity_id == f"GB-COH:{COMPANY}",
        "incorporation_date_available": entity.incorporated_on is not None,
        "company_status_available": bool(meta.get("company_status")),
        "address_retained": False,
        "corruption_inference": False,
    }
    assert output["company_number_matches"]
    assert output["incorporation_date_available"]
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

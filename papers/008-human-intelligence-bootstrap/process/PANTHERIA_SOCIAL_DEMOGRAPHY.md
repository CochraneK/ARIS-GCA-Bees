# PanTHERIA social-demography layer · ARIS4C008

PanTHERIA was parsed directly from its original archived table.

## Coverage in the 29-species v2 panel

All **19 mammal terminals** in the current panel are present in PanTHERIA.

Available J-relevant fields:
- social group size: **13 / 19 mammals**;
- population group size: **8 / 19**;
- population density: **10 / 19**;
- home-range fields are retained where available.

Two historical-name reconciliations are explicit:
- `Cebus libidinosus` → `Sapajus libidinosus`;
- `Physeter catodon` → `Physeter macrocephalus`.

Source missing value `-999` is converted to missing, never zero.

## Role in module J

PanTHERIA gives a **baseline social-demography layer**.

It does not measure the theoretically stronger quantity:
> effective cultural population = number and diversity of accessible information sources through time.

Therefore Paper 008 keeps three J layers separate:

1. **PanTHERIA:** species-level group size / density baseline;
2. **ASNR:** observed network topology and connectivity;
3. **ACDB / dedicated cultural studies:** actual cultural groups and transmission contexts.

This prevents simple census/group size from being silently equated with cultural connectivity.

from pathlib import Path
import importlib.util

MODULE = Path(__file__).with_name("audit_nvss_1988_layout.py")
spec = importlib.util.spec_from_file_location("audit013", MODULE)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

def test_detects_explicit_dates():
    lines = mod.matching_lines('str bday "Day of birth"\nstr dday "Day of death"')
    assert mod.has_any(lines, mod.BIRTH_DAY_PATTERNS)
    assert mod.has_any(lines, mod.DEATH_DAY_PATTERNS)

def test_month_only_does_not_pass_day_gate():
    lines = mod.matching_lines('byte bmonth "Month of birth"\nbyte dmonth "Month of death"')
    assert not mod.has_any(lines, mod.BIRTH_DAY_PATTERNS)
    assert not mod.has_any(lines, mod.DEATH_DAY_PATTERNS)

"""Regression anchors for fixes/additions from the two independent adversarial
reviews (2026-07-15: fable-5 + gpt-5.6-sol-xhigh).

- ckd_epi_2021 umol/L guard (fable #1): SI-unit parity with mdrd_gfr/cockcroft_gault.
- 3 confirmed-absent coverage equations (gpt #16), hand-computed textbook anchors.

Run: python -m scripts.tests.test_adversarial_review_fixes
"""
from scripts.canonical_ids import load


def _c(cid, **kw):
    return float(load(cid)._compute_func(**kw))


def test_ckd_epi_umol_guard():
    # 62 umol/L == 0.70 mg/dL -> same eGFR band (fable-5 finding #1)
    mgdl = _c("ckd_epi_2021", S_Cr=0.70, age=50, female=1.0)
    umol = _c("ckd_epi_2021", S_Cr=62.0, age=50, female=1.0, S_Cr_units="umol/L")
    assert abs(mgdl - 105.3) <= 0.5
    assert abs(umol - mgdl) <= 1.0, (umol, mgdl)


def test_ckd_epi_rejects_unknown_unit():
    try:
        _c("ckd_epi_2021", S_Cr=62.0, age=50, S_Cr_units="micromol/L")
    except ValueError:
        return
    raise AssertionError("expected ValueError on unknown S_Cr_units")


def test_oxygenation_index():
    # OI = 0.6 * 15 * 100 / 60 = 15
    assert abs(_c("oxygenation_index", FiO2=0.6, MAP=15, PaO2=60) - 15.0) <= 1e-9


def test_acute_respiratory_acidosis_hco3():
    # 24 + (60-40)/10 = 26 mEq/L
    assert abs(_c("acute_respiratory_acidosis_hco3", PCO2=60) - 26.0) <= 1e-9


def test_acute_respiratory_alkalosis_hco3():
    # 24 - 2*(40-20)/10 = 20 mEq/L
    assert abs(_c("acute_respiratory_alkalosis_hco3", PCO2=20) - 20.0) <= 1e-9


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    n = 0
    for fn in fns:
        fn()
        n += 1
    print(f"adversarial-review-fix tests passed: {n}")

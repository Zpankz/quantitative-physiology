"""LOCKED independent reference-value tests.

Unlike test_coverage_additions (whose expected values came from the authoring
agent — internally consistent but circular), every expected value here is derived
from an EXTERNAL source or an independent hand calculation stated in the comment.
These pin physically-correct behaviour so later refactors/"improvements" cannot
silently regress the equations that were verified against Feher's printed text or
standard physiology. Do not relax a tolerance to make a change pass — fix the change.

Run: python -m scripts.tests.test_reference_values_locked
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from scripts.canonical_ids import load

# (id, kwargs, expected, abs_tol, source of the expected value)
CASES = [
    # Nernst at 37C: (RT/F)*ln(4/140) = 0.0267116*(-3.55535) = -0.09499 V  [independent calc]
    ("nernst_equation", dict(z=1, C_out=4, C_in=140), -94.99, 0.5,
     "Nernst; RT/F=0.026712 V at 310K, ln(4/140)=-3.5553 -> -0.0950 V"),
    # MAP from 120/80: 80 + (120-80)/3 = 93.33 mmHg  [MAP definition]
    ("mean_arterial_pressure", dict(SBP=120, DBP=80), 93.333, 1e-2,
     "MAP = DBP + (SBP-DBP)/3 for 120/80 = 93.3 mmHg"),
    # MDRD, [Cr]=1.0 mg/dL, age=50, K=1: 175 * 50^-0.203 = 79.09 mL/min/1.73m2  [MDRD 2005 IDMS]
    ("mdrd_gfr", dict(Cr=1.0, age=50, K=1.0), 79.09, 0.2,
     "MDRD-175: 175*1^-1.154*50^-0.203 = 79.1"),
    # Van Slyke BE at normal blood (HCO3=24.4, pH=7.4, any Hb): first bracket 0 -> BE=0  [Siggaard-Andersen]
    ("base_excess_van_slyke", dict(HCO3=24.4, Hb=9.0, pH=7.4), 0.0, 1e-6,
     "BE is 0 at reference HCO3=24.4, pH=7.40 by construction of the Van Slyke eqn"),
    # SBE at normal (HCO3=24.8, pH=7.4) -> 0  [Siggaard-Andersen]
    ("standard_base_excess", dict(HCO3=24.8, pH=7.4), 0.0, 1e-6,
     "SBE = HCO3-24.8+16.2*(pH-7.4) is 0 at reference"),
    # MCV: Hct 0.45, 5e12 cells/L -> 90 fL  [red-cell index, normal 80-100]
    ("mean_cell_volume", dict(Hct_ratio=0.45, n_rbc=5e12), 90.0, 1e-6,
     "MCV = 0.45/5e12 * 1e15 = 90 fL"),
    # MCH: 150 g/L / 5 (x10^12/L) -> 30 pg  [normal 27-34]
    ("mean_corpuscular_hemoglobin", dict(Hb_conc=150, rbc_count=5), 30.0, 1e-6,
     "MCH = 150/5 = 30 pg/cell"),
    # MCHC: 150 g/L / 0.45 -> 333.3 g/L  [normal 330-360]
    ("mean_corpuscular_hemoglobin_concentration", dict(Hb_blood=150, Hct=0.45), 333.33, 1e-2,
     "MCHC = 150/0.45 = 333 g/L"),
    # Refractive index c/v with v=2e8: 3e8/2e8 = 1.5  [definition]
    ("refractive_index", dict(c=3.0e8, v=2.0e8), 1.5, 1e-9,
     "n = c/v = 1.5"),
    # Einthoven: II = I + III  [Einthoven's law]
    ("einthoven_lead_relation", dict(lead_I=0.5, lead_III=0.7), 1.2, 1e-9,
     "II = I + III"),
]


def _run():
    passed = failed = 0
    for cid, kw, exp, tol, src in CASES:
        try:
            got = load(cid).compute(**kw)
            if abs(float(got) - float(exp)) <= tol:
                print(f"PASS  {cid} = {got:.6g} (exp {exp}; {src})"); passed += 1
            else:
                print(f"FAIL  {cid}: got {got!r} exp {exp!r} [{src}]"); failed += 1
        except Exception as e:
            print(f"ERROR {cid}: {type(e).__name__}: {e}"); failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(CASES)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run())

"""Regression anchors for the 12 equations added in the grok-review pass
(2026-07-15). Each expected value is hand-computed from the STANDARD textbook
formula for that quantity (not the code's own output). Honest scope: for the 10
trivially-standard relations (CPP=DBP-LVEDP, F=AUC ratio, Css=FD/CLtau, SOG,
TTKG, W=0.5*dP*VT, Hursh theta=6D, RC charging, [H+]=24*PCO2/HCO3, HOMA-B) the
anchor is formula-standard self-consistency. Only ckd_epi_2021 is INDEPENDENTLY
source-verified: its five coefficients (142, 0.9938, 1.012, kappa 0.7/0.9, alpha
-0.241/-0.302) were checked against Inker 2021 (NEJM) / NKF Laboratory Working
Group (Clin Chem 2021).

Run: python -m scripts.tests.test_review_additions
"""
from scripts.canonical_ids import load


def _c(cid, **kw):
    return float(load(cid)._compute_func(**kw))


def test_coronary_perfusion_pressure():
    # CPP = DBP - LVEDP = 80 - 10 = 70 mmHg
    assert abs(_c("coronary_perfusion_pressure", DBP=80, LVEDP=10) - 70.0) <= 0.01


def test_stroke_work():
    # SW = MAP * SV = 93 * 70 = 6510 mmHg.mL
    assert abs(_c("stroke_work", MAP=93, SV=70) - 6510.0) <= 0.01


def test_pancreatic_homa_b():
    # HOMA-B = 20*10/(5.0-3.5) = 133.33 %
    assert abs(_c("pancreatic_homa_b", fasting_glucose_mmol=5.0, fasting_insulin_uU=10.0) - 133.333) <= 0.01


def test_passive_membrane_charging():
    # V(tau) = I*R*(1-1/e) = 1e-9*1e8*0.6321 = 0.06321 V
    assert abs(_c("passive_membrane_charging", I=1e-9, R=1e8, t=0.01, tau=0.01) - 0.063212) <= 1e-4


def test_hursh_conduction_velocity():
    # theta = 6 * 10 um = 60 m/s
    assert abs(_c("hursh_conduction_velocity", D=10.0) - 60.0) <= 0.01


def test_bioavailability_auc():
    # F = 50/100 = 0.5 (equal doses)
    assert abs(_c("bioavailability_auc", AUC_oral=50.0, AUC_iv=100.0) - 0.5) <= 1e-6


def test_average_steady_state_concentration():
    # Css = 1*1000/(10*8) = 12.5 mg/L
    assert abs(_c("average_steady_state_concentration", F=1.0, Dose=1000.0, CL=10.0, tau=8.0) - 12.5) <= 1e-6


def test_stool_osmotic_gap():
    # SOG = 290 - 2*(30+75) = 80 mOsm/kg
    assert abs(_c("stool_osmotic_gap", Osm_stool=290.0, Na=30.0, K=75.0) - 80.0) <= 0.01


def test_ttkg():
    # TTKG = (40/4)/(600/300) = 10/2 = 5.0
    assert abs(_c("ttkg", U_K=40.0, P_K=4.0, U_osm=600.0, P_osm=300.0) - 5.0) <= 1e-6


def test_ckd_epi_2021():
    # SCr 0.7 mg/dL, female, age 50 -> ~105.3 mL/min/1.73m2 (Inker 2021)
    assert abs(_c("ckd_epi_2021", S_Cr=0.7, age=50.0, female=1.0) - 105.3) <= 0.5


def test_kassirer_bleich_hydrogen_ion():
    # [H+] = 24*40/24 = 40 nmol/L (pH 7.40)
    assert abs(_c("kassirer_bleich_hydrogen_ion", PCO2=40, HCO3=24) - 40.0) <= 0.01


def test_work_of_breathing_elastic():
    # W_el = 0.5 * 5 * 0.5 = 1.25 L.cmH2O
    assert abs(_c("work_of_breathing_elastic", delta_P=5, VT=0.5) - 1.25) <= 1e-6


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    n = 0
    for fn in fns:
        fn()
        n += 1
    print(f"review-addition tests passed: {n}")

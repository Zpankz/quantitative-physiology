"""External/hand-computed anchors for the backlog-completion additions
(2026-07-15, "nothing deferred" pass).

Run: python -m scripts.tests.test_backlog_additions
"""
from scripts.canonical_ids import load


def _c(cid, **kw):
    return float(load(cid)._compute_func(**kw))


def test_aa_gradient_age_limit():
    # (40/4)+4 = 14 mmHg
    assert abs(_c("aa_gradient_age_limit", age=40) - 14.0) <= 1e-9


def test_apparent_volume_of_distribution():
    # 500 mg / 10 mg/L = 50 L
    assert abs(_c("apparent_volume_of_distribution", Dose=500, C0=10) - 50.0) <= 1e-9


def test_driving_force():
    # V_m -70 - E_K -90 = +20 mV
    assert abs(_c("driving_force", V_m=-70, E_ion=-90) - 20.0) <= 1e-9


def test_dynamic_compliance():
    # 500 / (25-5) = 25 mL/cmH2O
    assert abs(_c("dynamic_compliance", VT=500, PIP=25, PEEP=5) - 25.0) <= 1e-9


def test_frank_starling():
    # 80*(120-20) = 8000 mmHg.mL
    assert abs(_c("frank_starling", M_w=80, EDV=120, V_w=20) - 8000.0) <= 1e-9


def test_mixed_venous_oxygen_content():
    # 1.34*15*0.75 + 0.003*40 = 15.195 mL/dL
    assert abs(_c("mixed_venous_oxygen_content", Hb=15, S_vO2=0.75, P_vO2=40) - 15.195) <= 1e-6


def test_p50_bohr_ph_neutral():
    # pH 7.4 -> 26.8 mmHg (no shift)
    assert abs(_c("p50_bohr_ph", pH=7.4) - 26.8) <= 1e-6
    # acidosis right-shifts (raises P50)
    assert _c("p50_bohr_ph", pH=7.2) > 26.8


def test_va_coupling_esv():
    # (2*120 + 2.5*10)/(2.5+2) = 265/4.5 = 58.889 mL
    assert abs(_c("va_coupling_esv", Ea=2, EDV=120, Ees=2.5, V0=10) - 58.8889) <= 1e-3



def test_sodium_clearance():
    assert abs(_c("sodium_clearance", U_Na=100, V_dot=1, P_Na=140) - 0.7142857) <= 1e-5


def test_creatinine_clearance_typed():
    assert abs(_c("creatinine_clearance_typed", U_Cr=100, V_dot=1, P_Cr=1) - 100.0) <= 1e-9


def test_gfr_from_glomerular_nfp():
    assert abs(_c("gfr_from_glomerular_nfp", K_f=12.5, NFP_glomerular=10) - 125.0) <= 1e-9



def test_clearance_from_metabolic_rate():
    # 1440 L/day / 1440 = 1.0 L/min
    assert abs(_c("clearance_from_metabolic_rate", MCR_day=1440.0) - 1.0) <= 1e-9


def test_tpr_feeds_map_from_flow_propagate():
    # resolved item: TPR (Wood units) now feeds map_from_flow via alias
    from scripts.eqgraph import build_graph
    r = build_graph().propagate({"TPR": 1.2, "CO": 5.0, "CVP": 2.0})
    assert "map_from_flow" in r["fired"]
    assert abs(r["store"]["MAP"] - 8.0) <= 1e-6  # 5*1.2 + 2


def test_mcr_chains_to_half_life_propagate():
    # resolved item: MCR (L/day) -> converter -> CL_mcr (L/min) -> hormone_half_life_from_mcr
    from scripts.eqgraph import build_graph
    r = build_graph().propagate({"production_rate": 14400.0, "plasma_concentration": 10.0, "Vd": 5.0})
    assert abs(r["store"].get("CL_mcr") - 1.0) <= 1e-6
    assert abs(r["fired"]["hormone_half_life_from_mcr"] - 3.465) <= 1e-3


def test_mcr_converter_does_not_hijack_seeded_CL():
    # adversarial: a user-seeded generic CL must NOT be overridden by the MCR chain
    from scripts.eqgraph import build_graph
    r = build_graph().propagate({"production_rate": 14400.0, "plasma_concentration": 10.0, "Vd": 5.0, "CL": 2.0})
    assert abs(r["store"]["CL"] - 2.0) <= 1e-9                       # seeded CL preserved
    assert abs(r["fired"]["hormone_half_life"] - (0.693 * 5 / 2.0)) <= 1e-3  # uses seeded CL
    assert abs(r["fired"]["hormone_half_life_from_mcr"] - 3.465) <= 1e-3     # scoped chain independent


def test_no_cycles_after_wiring():
    from scripts.index import get_global_index
    assert get_global_index().detect_cycles() == []


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    n = 0
    for fn in fns:
        fn(); n += 1
    print(f"backlog-addition tests passed: {n}")

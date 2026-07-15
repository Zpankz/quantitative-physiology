"""Anchored end-to-end integration-chain tests.

Each chain seeds a small set of measured base quantities, runs the whole-graph
forward-chaining ``EquationGraph.propagate`` simulation, and asserts that every
endpoint equals an INDEPENDENT hand-calculated value (stated in ``source``) within
tolerance. A passing anchor proves the wired ``depends_on``/``produces`` edges
carry *correct values* across the chain, not merely that the equations fire.

Every expected value here comes from a standalone hand calculation (standard
hemodynamics / renal-physiology formulas), never from qp's own output — so these
pins cannot be satisfied by a self-consistent-but-wrong package.

Run: python -m scripts.tests.test_integration_chains
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from scripts.eqgraph import build_graph

# name, seed, {endpoint_id: expected}, {endpoint_id: abs_tol}, source
CHAINS = [
    (
        "cardiac_output_perfusion_cascade",
        {"EDV": 125, "ESV": 55, "HR": 80, "SVR_wood": 15, "CVP": 6,
         "CO": 5.6, "mPAP": 15, "PCWP": 8, "Hb": 15, "S_O2": 1},
        {"stroke_volume": 70, "cardiac_output": 5.6, "map_from_flow": 90,
         "svr_dyn": 1200, "total_peripheral_resistance": 15, "pvr_dyn": 100,
         "systemic_oxygen_delivery": 1125.6},
        {"stroke_volume": 0.5, "cardiac_output": 0.05, "map_from_flow": 0.5,
         "svr_dyn": 2, "total_peripheral_resistance": 0.1, "pvr_dyn": 2,
         "systemic_oxygen_delivery": 2},
        "SV=EDV-ESV=70; CO=HR*SV/1000=5.6; MAP=CO*SVR_wood+CVP=90; "
        "SVR_dyn=80*(MAP-CVP)/CO=1200; TPR=(MAP-CVP)/CO=15; "
        "PVR=80*(mPAP-PCWP)/CO=100; DO2=CO*1.34*Hb*SaO2*10=1125.6",
    ),
    (
        "cuff_map_to_vascular_resistance",
        {"SBP": 120, "DBP": 80, "CVP": 5, "CO": 5},
        {"mean_arterial_pressure": 93.33, "total_peripheral_resistance": 17.67,
         "svr_dyn": 1413.33},
        {"mean_arterial_pressure": 0.3, "total_peripheral_resistance": 0.1,
         "svr_dyn": 3},
        "MAP=DBP+(SBP-DBP)/3=93.33; TPR=(MAP-CVP)/CO=17.67; "
        "SVR_dyn=80*(MAP-CVP)/CO=1413.3",
    ),
    (
        "glomerular_filtration_to_glucosuria",
        {"K_f": 12.5, "NFP": 10, "P_x": 400, "T_max": 375},
        {"gfr_from_nfp": 125, "filtered_load": 500, "glucose_excretion": 125},
        {"gfr_from_nfp": 0.5, "filtered_load": 2, "glucose_excretion": 2},
        "GFR=Kf*NFP=125; FL=GFR*P_x/100=500; excretion=FL-Tm=125",
    ),
    (
        "bsa_normalized_gfr_cross_domain",
        {"K_f": 12.5, "NFP": 10, "W": 70, "H": 170},
        {"gfr_from_nfp": 125, "body_surface_area_dubois": 1.81,
         "gfr_normalized": 119.49},
        {"gfr_from_nfp": 0.5, "body_surface_area_dubois": 0.02,
         "gfr_normalized": 1},
        "GFR=Kf*NFP=125; BSA(DuBois)=0.007184*70^0.425*170^0.725=1.81; "
        "GFR_idx=GFR*1.73/BSA=119.5",
    ),
    (
        # Fick-method cardiac output feeding the resistance cascade. Proves the
        # cardiac_output_fick -> {TPR, SVR, PVR} edges carry a correct CO value:
        # an alternative CO source (O2 consumption + a-v content difference)
        # reaches the same downstream physiology as HR*SV.
        "fick_cardiac_output_to_resistances",
        {"VO2": 250, "C_aO2": 20, "C_vO2": 15, "MAP": 93, "CVP": 3,
         "mPAP": 15, "PCWP": 9},
        {"cardiac_output_fick": 5.0, "total_peripheral_resistance": 18.0,
         "svr_dyn": 1440.0, "pvr_dyn": 96.0},
        {"cardiac_output_fick": 0.05, "total_peripheral_resistance": 0.2,
         "svr_dyn": 5, "pvr_dyn": 2},
        "CO_Fick=VO2/((CaO2-CvO2)*10)=250/50=5.0; TPR=(MAP-CVP)/CO=18; "
        "SVR_dyn=80*(MAP-CVP)/CO=1440; PVR=80*(mPAP-PCWP)/CO=96",
    ),
    (
        # Nervous domain: synaptic conductance -> synaptic current. The alpha
        # function's peak conductance drives the postsynaptic current. Proves the
        # alpha_function -> synaptic_current g_syn edge (the internal chain that
        # de-isolates the synapse equations in the otherwise-terminal nervous unit).
        "synaptic_conductance_to_current",
        {"t": 1.0, "g_max": 1.0, "tau": 1.0, "V_m": -65.0, "E_rev": 0.0},
        {"alpha_function": 1.0, "synaptic_current": -65.0},
        {"alpha_function": 0.01, "synaptic_current": 0.5},
        "alpha g(t=tau)=g_max*(t/tau)*e^(1-t/tau)=1*1*e^0=1.0 nS; "
        "I_syn=g_syn*(V_m-E_rev)=1*(-65-0)=-65 pA",
    ),
]


def main():
    g = build_graph()
    passed = failed = 0
    for name, seed, expected, tols, source in CHAINS:
        res = g.propagate(seed)
        fired = res["fired"]
        for eid, exp in expected.items():
            tol = tols.get(eid, abs(exp) * 0.05)
            got = fired.get(eid)
            ok = got is not None and abs(got - exp) <= tol
            if ok:
                passed += 1
            else:
                failed += 1
            status = "PASS" if ok else "FAIL"
            print(f"{status}  {name}::{eid} = {got} (exp {exp} +/- {tol})")
        print(f"       source: {source}")
    total = passed + failed
    print(f"\n{passed} passed, {failed} failed, {total} total")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

"""Golden tests for the clinical (CICM, beyond-Feher) additions — external anchors.

Each expected value is a standard clinical result (P/F 476, SVR 1408 dyn, driving
pressure 15, delta ratio 1.2, ke=CL/Vd, etc.), hand-derived not code-derived.
Run: python -m scripts.tests.test_clinical_additions
"""
import sys, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0,ROOT)
from scripts.canonical_ids import load

CASES=[
    ('pf_ratio', {'PaO2': 100, 'FiO2': 0.21}, 476.19, 0.01),
    ('driving_pressure', {'Pplat': 25, 'PEEP': 10}, 15.0, 1e-06),
    ('static_compliance', {'VT': 500, 'Pplat': 25, 'PEEP': 10}, 33.333, 0.01),
    ('svr_dyn', {'MAP': 93, 'CVP': 5, 'CO': 5}, 1408.0, 0.01),
    ('pvr_dyn', {'mPAP': 15, 'PCWP': 8, 'CO': 5}, 112.0, 0.01),
    ('ventricular_wall_stress', {'P': 120, 'r': 2, 'h': 1}, 120.0, 1e-06),
    ('rate_pressure_product', {'HR': 70, 'SBP': 120}, 8400.0, 1e-06),
    ('arterial_elastance', {'ESP': 100, 'SV': 70}, 1.4286, 0.001),
    ('corrected_anion_gap', {'AG': 12, 'albumin': 20}, 17.0, 1e-06),
    ('delta_ratio', {'AG': 24, 'HCO3': 14}, 1.2, 1e-06),
    ('fe_urea', {'U_urea': 200, 'P_cr': 0.1, 'P_urea': 5, 'U_cr': 8}, 50.0, 0.001),
    ('first_order_elimination', {'C0': 10, 'ke': 0.1, 't': 6.931}, 5.0, 0.01),
    ('elimination_rate_constant', {'CL': 5, 'Vd': 50}, 0.1, 1e-06),
    ('loading_dose', {'Vd': 50, 'C_target': 10}, 500.0, 1e-06),
    ('maintenance_infusion_rate', {'CL': 5, 'C_ss': 10}, 50.0, 1e-06),
    ('driving_force_ion', {'V_m': -70, 'E_ion': -90}, 20.0, 1e-06),
    ('ionic_current', {'g_ion': 1, 'V_m': -70, 'E_ion': -90}, 20.0, 1e-06),
    ('pulse_pressure_from_compliance', {'SV': 70, 'C_art': 2}, 35.0, 1e-06),
    ('map_from_flow', {'CO': 5, 'SVR_wood': 17.6, 'CVP': 5}, 93.0, 0.1),
    ('poiseuille_resistance', {'eta':3.5,'L':1,'r':0.15}, 0.13204, 1e-4),  # mPa*s/mL->mmHg*s/mL x7.5e-6
]

def _run():
    p=f=0
    for cid,kw,exp,tol in CASES:
        try:
            g=load(cid).compute(**kw)
            if abs(float(g)-float(exp))<=max(tol,abs(exp)*1e-3): print(f"PASS  {cid}"); p+=1
            else: print(f"FAIL  {cid}: got {g!r} exp {exp!r}"); f+=1
        except Exception as e: print(f"ERROR {cid}: {e}"); f+=1
    print(f"\n{p} passed, {f} failed, {len(CASES)} total"); return 1 if f else 0

if __name__=="__main__": sys.exit(_run())

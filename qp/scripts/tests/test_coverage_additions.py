"""Golden-value regression tests for the coverage-pass additions (69 equations).

Each new equation checked against a worked example verified during authoring.
Run: python -m scripts.tests.test_coverage_additions
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from scripts.canonical_ids import load

CASES = [
    ('lennard_jones_potential', {'epsilon': 1, 'sigma': 2, 'r': 4}, -0.0615234375, 1e-09),
    ('surface_pressure', {'gamma_0': 0.072, 'gamma': 0.045}, 0.027, 1e-09),
    ('electric_dipole_moment', {'q': 1.6e-19, 'd': 1e-10}, 1.6e-29, 1e-33),
    ('redox_free_energy', {'n': 2, 'delta_E': 0.35}, -67539.5, 0.01),
    ('surface_free_energy', {'gamma': 0.072, 'dA': 0.0001}, 7.2e-06, 1e-09),
    ('ussing_flux_ratio', {'C_in': 12, 'C_out': 145, 'z': 1, 'E_m': -0.085}, -0.0034345231263335518, 1e-06),
    ('partition_coefficient', {'C_lipid': 8, 'C_water': 2}, 4, 1e-09),
    ('dipole_potential', {'p': 6.2e-30, 'theta': 0, 'r': 1e-09, 'kappa': 1}, 0.05574918910563565, 1e-06),
    ('boyle_vant_hoff_relation', {'pi_0': 0.29, 'pi_C': 0.58, 'b': 0.379}, 0.6895, 1e-06),
    ('body_energy_balance', {'E_food': 2000, 'E_heat': 1500, 'E_work': 200, 'E_feces': 100, 'E_urine': 50}, 150, 1e-09),
    ('strength_duration_weiss', {'I_rh': 0.01, 't': 0.1, 'tau_SD': 0.2}, 0.03, 1e-09),
    ('youngs_modulus', {'E': 20, 'epsilon': 0.05}, 1, 1e-09),
    ('architectural_gear_ratio', {'v_muscle': 70, 'v_fiber': 60.6}, 1.155115511551155, 1e-06),
    ('motor_unit_force', {'N': 2000, 'A': 5e-05, 'F_S': 20}, 2, 1e-09),
    ('arrhenius_equation', {'A': 10000000000000, 'E_a': 50000, 'T': 310}, 37562.43856388265, 0.01),
    ('direction_selectivity_index', {'R_pref': 12, 'R_null': 4}, 0.5, 1e-09),
    ('orientation_selectivity_index', {'R_pref': 12, 'R_null': 4, 'R_orth_plus': 2, 'R_orth_minus': 1}, 0.8125, 1e-06),
    ('kelvin_voigt_model', {'E': 20, 'epsilon': 0.05, 'eta': 50, 'depsilon_dt': 0.02}, 2, 1e-09),
    ('maxwell_model', {'sigma': 1, 'dsigma_dt': 10, 'E': 20, 'eta': 50}, 0.52, 1e-09),
    ('convection_diffusion_flux', {'D': 1e-09, 'dC_dx': 1000, 'J_V': 1e-06, 'C': 100}, 9.9e-05, 1e-09),
    ('snells_law', {'n_i': 1, 'theta_i': 0.5235987755982988, 'n_r': 1.33}, 0.3854108170293797, 1e-09),
    ('thin_lens_formula', {'O': 0.1, 'I': 0.016}, 0.013793103448275862, 1e-06),
    ('volume_of_distribution', {'m': 1e-05, 'C': 0.004}, 0.0025, 1e-09),
    ('persistence_length', {'L': 1.7e-05, 'l_p': 1.7e-05}, 0.36787944117144233, 1e-06),
    ('norwich_sensation_magnitude', {'Phi': 10, 'k': 2, 'beta': 0.5, 'n': 1}, 3.58351893845611, 1e-06),
    ('stroke_volume', {'EDV': 120, 'ESV': 50}, 70, 1e-09),
    ('poisson_ratio', {'depsilon_trans': -0.035, 'depsilon_axial': 0.1}, 0.35, 1e-09),
    ('mean_cell_volume', {'Hct_ratio': 0.45, 'n_rbc': 5000000000000}, 90, 1e-06),
    ('mean_corpuscular_hemoglobin_concentration', {'Hb_blood': 150, 'Hct': 0.45}, 333.33, 0.5),
    ('capillary_pressure', {'P_A': 35, 'P_V': 15, 'R_A': 3, 'R_V': 1}, 20, 1e-09),
    ('plasma_buffer_capacity', {'delta_acid': 8, 'delta_pH': 0.5}, 16, 1e-09),
    ('standard_linear_solid', {'epsilon': 0.03, 'depsilon_dt': 0.001, 'sigma': 0.5, 'E1': 20, 'E2': 20, 'eta': 50}, 0.08, 1e-09),
    ('mean_corpuscular_hemoglobin', {'Hb_conc': 150, 'rbc_count': 5}, 30, 1e-06),
    ('refractive_power_diopters', {'f': 0.016}, 62.5, 1e-09),
    ('ideal_gas_law', {'n': 1, 'T': 300, 'V': 0.025}, 99768, 0.001),
    ('sound_intensity_level_db', {'I_sound': 1e-06, 'I_ref': 1e-12}, 60, 1e-09),
    ('indicator_dilution_cardiac_output', {'m': 5, 'area_under_curve': 1.25}, 4, 1e-09),
    ('systemic_vascular_compliance', {'C_A': 2, 'C_V': 100}, 102, 1e-09),
    ('transferrin_saturation', {'serum_iron': 18, 'TIBC': 60}, 30, 1e-09),
    ('sieving_coefficient', {'C_B': 63, 'C_P': 70}, 0.9, 1e-09),
    ('rohrer_equation', {'K1': 1.5, 'K2': 0.5, 'Q_V': 2}, 5, 1e-09),
    ('acoustic_intensity', {'dP0': 1, 'rho': 1.21, 'c': 343}, 0.0012047322, 1e-06),
    ('base_excess_van_slyke', {'HCO3': 14, 'Hb': 9, 'pH': 7.3}, -10.49932, 0.001),
    ('strong_ion_difference_apparent', {'Na': 140, 'K': 4.5, 'Ca': 1.2, 'Mg': 0.8, 'Cl': 105, 'lactate': 1}, 42.5, 1e-09),
    ('standard_base_excess', {'HCO3': 14, 'pH': 7.3}, -12.42, 1e-06),
    ('lean_body_mass', {'tbw': 42}, 57.534246575342465, 1e-06),
    ('colloid_osmotic_pressure', {'C': 4}, 14.848, 1e-06),
    ('weak_acid_anion_charge', {'pH': 7.4, 'albumin': 44, 'phosphate': 1.16}, 14.393216, 0.01),
    ('strong_ion_difference_effective', {'HCO3': 24, 'A_minus': 14}, 38, 1e-09),
    ('vascular_function_curve', {'P_RA': 2, 'P_MS': 7, 'C_V': 19, 'C_A': 1, 'TPR': 20}, 5, 1e-09),
    ('mdrd_gfr', {'Cr': 1.2, 'age': 50, 'K': 1}, 64.0873007, 0.01),
    ('fev1_fvc_ratio', {'FEV1': 2, 'FVC': 3.9}, 0.5128205128205128, 1e-09),
    ('oxygen_consumption_gas_exchange', {'Q_T_star': 5, 'fIO2': 0.209, 'Q_T': 4.96, 'fEO2': 0.163}, 236.52, 0.01),
    ('alveolar_pco2_equation', {'Q_CO2': 200, 'Q_A': 3570, 'P_B': 760}, 39.944, 0.05),
    ('cheng_prusoff_ki', {'IC50': 1e-08, 'L': 1e-09, 'Kd': 1e-09}, 5e-09, 1e-12),
    ('beer_lambert_attenuation', {'I_0': 1, 'mu': 0.2, 'x': 10}, 0.1353352832366127, 1e-09),
    ('strong_ion_gap', {'SIDa': 42, 'SIDe': 40}, 2, 1e-09),
    ('energy_expenditure_indirect_calorimetry', {'VO2': 0.25, 'energy_equiv': 4.85}, 1.2125, 1e-06),
    ('carbohydrate_oxidation_indirect_calorimetry', {'VO2': 20, 'VCO2': 17, 'n': 1}, 9.28, 0.0001),
    ('protein_oxidation_urinary_nitrogen', {'n': 10}, 62.5, 1e-09),
    ('fractional_water_reabsorption', {'TF_P_inulin': 3}, 0.6666666666666667, 1e-09),
    ('competitive_inhibition_binding', {'L': 1e-09, 'Bmax': 1e-07, 'Kd': 1e-09, 'I': 3e-09, 'Ki': 1e-09}, 2e-08, 1e-12),
    ('fat_oxidation_indirect_calorimetry', {'VO2': 360, 'VCO2': 290, 'n': 14}, 93.8, 0.0001),
    ('harris_benedict_bmr', {'W': 70, 'H': 170, 'A': 30, 'sex': 1}, 1671.5, 1e-06),
    ('mifflin_st_jeor_ree', {'W': 70, 'H': 170, 'A': 30, 'sex': 1}, 1619.2, 1e-06),
    ('refractive_index', {'c': 300000000.0, 'v': 200000000.0}, 1.5, 1e-09),
    ('newtonian_viscosity', {'eta': 2.0, 'strain_rate': 3.0}, 6.0, 1e-09),
    ('einthoven_lead_relation', {'lead_I': 0.5, 'lead_III': 0.7}, 1.2, 1e-09),
    ('enthalpy', {'E': 100.0, 'P': 100000.0, 'V': 0.001}, 200.0, 1e-09),
]

def _run():
    passed=failed=0
    for cid, kw, exp, tol in CASES:
        try:
            got = load(cid).compute(**kw)
            ok = abs(float(got)-float(exp)) <= max(tol, abs(exp)*1e-6+1e-12)
            if ok: print(f"PASS  {cid}"); passed+=1
            else: print(f"FAIL  {cid}: got {got!r} exp {exp!r}"); failed+=1
        except Exception as e: print(f"ERROR {cid}: {type(e).__name__}: {e}"); failed+=1
    print(f"\n{passed} passed, {failed} failed, {len(CASES)} total")
    return 1 if failed else 0

if __name__ == "__main__": sys.exit(_run())

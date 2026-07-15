"""EXTERNALLY-ANCHORED reference-value regression suite (audit-harvested).

Every expected value was produced by a subagent from an EXTERNAL source (Feher worked
example, standard physiological value, or independent hand calculation stated in the
`src` field) — NOT by running the equation. This is the non-circular correctness net;
it caught the Mifflin female-coefficient, NMDA sign, Goldman-flux sign, and filtered_load
dimensional defects. Do not relax a tolerance to make a change pass.

Run: python -m scripts.tests.test_reference_values_audit
"""
import sys, os
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0,ROOT)
from scripts.canonical_ids import load

CASES=[
    ('pancreatic_gsis', {'glucose': 6, 'I_basal': 5, 'I_max': 50, 'EC50': 6, 'n': 2.5}, 30.0, 0.6),  # Hill-function structural identity (independent hand calc): at glucose = EC50, the Hill saturation term [G]^n/(
    ('pancreatic_homa_ir', {'fasting_glucose_mmol': 4.5, 'fasting_insulin_uU': 5}, 1.0, 0.02),  # Matthews et al., Diabetologia 1985 — HOMA-IR is normalized so that a healthy normal individual (fasting glucos
    ('receptor_fractional_occupancy', {'H': 1e-09, 'Kd': 1e-09}, 0.5, 0.01),  # Textbook definition: Kd is the ligand concentration giving 50% receptor occupancy. Hand calc theta=[H]/(Kd+[H]
    ('receptor_saturation_binding', {'H': 1e-09, 'Bmax': 1e-09, 'Kd': 1e-09}, 5e-10, 1e-06),  # Langmuir isotherm property: at [H]=Kd, B=Bmax/2. Hand calc Bmax*H/(Kd+H) = 1e-9*1e-9/(2e-9) = 5e-10 M.
    ('cheng_prusoff_ki', {'IC50': 2e-09, 'L': 1e-09, 'Kd': 1e-09}, 1e-09, 1e-06),  # Cheng & Prusoff (1973) Ki=IC50/(1+[L]/Kd); at [L]=Kd the correction factor is 2, so Ki=IC50/2 = 2e-9/2 = 1e-9 
    ('competitive_inhibition_binding', {'L': 1e-09, 'Bmax': 1e-09, 'Kd': 1e-09, 'I': 1e-09, 'Ki': 1e-09}, 3.3333333333e-10, 1e-06),  # Competitive binding B=Bmax[L]/([L]+Kd(1+[I]/Ki)); with [L]=Kd and [I]=Ki: B=Bmax*Kd/(Kd+Kd*2)=Bmax/3 = 1e-9/3 
    ('beer_lambert_attenuation', {'I_0': 100, 'mu': 0.2, 'x': 5}, 36.79, 0.7358),  # Independent hand calc of Beer-Lambert law I=I_0*e^{-mu*x}: mu*x=0.2/cm*5cm=1.0 (dimensionless), e^{-1}=0.36788
    ('calcium_albumin_correction', {'measured_Ca': 8, 'albumin': 2}, 9.6, 0.192),  # Standard Payne albumin-correction formula (Corrected Ca = Measured + 0.8*(4 - albumin), normal albumin 4.0 g/d
    ('calcium_pth_secretion', {'Ca_ionized': 1.1, 'PTH_max': 65, 'K': 1.1, 'n': 3.5}, 32.5, 0.65),  # Inverse-Hill setpoint property: when ionized Ca equals the setpoint K, PTH = PTH_max*K^n/(K^n+K^n) = PTH_max/2
    ('body_surface_area_dubois', {'W': 70, 'H': 170}, 1.81, 0.0362),  # Independent hand calculation of Du Bois formula 0.007184*70^0.425*170^0.725 = 1.8097 m^2; standard textbook BS
    ('cardiac_output', {'HR': 70, 'SV': 70}, 4.9, 0.098),  # Hand calc CO = HR*SV = 70/min * 70 mL = 4900 mL/min = 4.9 L/min; standard textbook resting CO ~5 L/min.
    ('stroke_volume', {'EDV': 120, 'ESV': 50}, 70.0, 1.4),  # Feher 5.6 Ejection Phase worked example: 120 mL - 50 mL = 70 mL (cited in the equation's own docstring).
    ('ejection_fraction', {'EDV': 120, 'ESV': 50}, 0.5833, 0.011666),  # Hand calc EF = (EDV-ESV)/EDV = 70/120 = 0.583, using Feher 5.6 example volumes (EDV 120, ESV 50); normal EF 0.
    ('cardiac_output_fick', {'VO2': 250, 'C_aO2': 20, 'C_vO2': 15}, 5.0, 0.1),  # Standard Fick worked example: VO2 250 mL/min, a-v O2 difference 5 mL/dL = 50 mL/L; CO = 250/50 = 5.0 L/min.
    ('cardiac_index', {'CO': 5, 'BSA': 2}, 2.5, 0.05),  # Hand calc CI = CO/BSA = 5/2 = 2.5 L/min/m^2; lower bound of normal CI range 2.5-4.0.
    ('thyroid_t4_production', {'TSH': 2, 'Vmax': 100, 'Km': 2}, 50.0, 1.0),  # Michaelis-Menten definitional property (independent of code): for v = Vmax*TSH/(Km+TSH), when TSH = Km the rat
    ('thyroid_tsh_response', {'fT4': 1, 'Kd': 1, 'n': 2, 'TSH_max': 10}, 5.0, 0.1),  # Inverse Hill function midpoint (independent of code): for TSH = TSH_max/(1+(fT4/Kd)^n), when fT4 = Kd the term
    ('qtc_bazett', {'QT': 360, 'RR': 0.8}, 402.49, 8.0498),  # Bazett's formula QTc = QT/sqrt(RR) with RR in seconds; independent hand calc: sqrt(0.8)=0.89443, 360/0.89443 =
    ('qtc_fridericia', {'QT': 360, 'RR': 0.8}, 387.8, 7.756),  # Fridericia's formula QTc = QT/cbrt(RR) with RR in seconds; independent hand calc: 0.8^(1/3)=0.92832, 360/0.928
    ('einthoven_lead_relation', {'lead_I': 0.5, 'lead_III': 0.3}, 0.8, 0.016),  # Einthoven's law lead_II = lead_I + lead_III (derives from I=LA-RA, II=LL-RA, III=LL-LA, so I+III=LL-RA=II); ha
    ('hill_saturation', {'P_O2': 26, 'P_50': 26, 'n': 2.7}, 0.5, 0.01),  # By definition P_50 is the PO2 at which hemoglobin is 50% saturated; any Hill curve yields S=0.5 exactly when P
    ('blood_oxygen_content', {'Hb': 15, 'S_O2': 1, 'P_O2': 100}, 20.4, 0.408),  # Standard textbook arterial O2 content ~20 mL/dL. Hand calc: 1.34*15*1.0 + 0.003*100 = 20.1 + 0.3 = 20.4 mL/dL.
    ('systemic_oxygen_delivery', {'CO': 5, 'Hb': 15, 'S_O2': 1}, 1005.0, 20.1),  # Standard resting DO2 ~1000 mL/min. Hand calc: 5 L/min * (1.34*15*1.0 mL/dL) * 10 dL/L = 1005 mL/min.
    ('mean_cell_volume', {'Hct_ratio': 0.45, 'n_rbc': 5000000000000}, 90.0, 1.8),  # Hand calc: 0.45 / 5e12 cells/L = 9e-14 L/cell; *1e15 fL/L = 90 fL/cell. Normal MCV ~90 fL/cell.
    ('mean_corpuscular_hemoglobin_concentration', {'Hb_blood': 150, 'Hct': 0.45}, 333.33, 6.6666),  # Hand calc: 150 g/L / 0.45 = 333.3 g/L. Normal MCHC ~320-360 g/L.
    ('mean_corpuscular_hemoglobin', {'Hb_conc': 150, 'rbc_count': 5}, 30.0, 0.6),  # Feher EXAMPLE 5.2.2 / hand calc: 150 g/L / 5(x10^12 cells/L) = 30 pg/cell. Normal MCH 27-34 pg/cell.
    ('transferrin_saturation', {'serum_iron': 30, 'TIBC': 100}, 30.0, 0.6),  # Hand calc: (30/100)*100 = 30%. Normal transferrin saturation ~30%.
    ('hematocrit', {'V_RBC': 2000, 'V_blood': 5000}, 0.4, 0.008),  # Definitional hand calc: Hct = V_RBC/V_blood = 2000/5000 = 0.40. Normal adult ~0.40-0.45.
    ('strength_duration_weiss', {'I_rh': 1, 't': 0.001, 'tau_SD': 0.001}, 2.0, 0.04),  # Chronaxie definition (Feher Eqn 3.2.2): when pulse duration t equals the strength-duration time constant tau_S
    ('membrane_time_constant', {'R_m': 1000, 'C_m': 1e-06}, 0.001, 2e-05),  # Hand calc tau = R_m*C_m = 1000 ohm.cm^2 * 1e-6 F/cm^2 = 1e-3 s; the canonical ~1 ms membrane time constant quo
    ('space_constant', {'a': 0.02, 'R_m': 1000, 'R_i': 100}, 0.31622776601683794, 0.006325),  # Hand calc lambda = sqrt(R_m*a/(2*R_i)) = sqrt(1000*0.02/200) = sqrt(0.1) = 0.31623 cm; verifies the 1/(2*R_i) 
    ('hh_leak_current', {'V': -65, 'g_L_bar': 0.3, 'E_L': -54.4}, -3.18, 0.0636),  # Hand calc with standard HH constants: I_L = g_L*(V_rest - E_L) = 0.3 mS/cm^2 * (-65 - (-54.4)) mV = 0.3 * (-10
    ('michaelis_menten', {'S': 5, 'J_max': 10, 'K_m': 5}, 5.0, 0.1),  # Textbook definition of K_m: at [S]=K_m the flux is half-maximal (J = J_max/2). Independent hand calc: J = J_ma
    ('arrhenius_equation', {'A': 1000000, 'E_a': 2577.34, 'T': 310, 'R': 8.314}, 367879.44117144233, 7357.588823),  # Structural property of the Arrhenius law: when E_a = R*T the exponent -E_a/(R*T) is exactly -1, so k = A*e^-1 
    ('ghk_potential', {'P_K': 1, 'P_Na': 0.04, 'P_Cl': 0.45, 'K_out': 5, 'K_in': 140, 'Na_out': 145, 'Na_in': 12, 'Cl_out': 120, 'Cl_in': 4}, -73.1, 1.462),  # Standard GHK resting-potential calculation using the textbook relative permeabilities P_K:P_Na:P_Cl = 1:0.04:0
    ('chord_conductance', {'g_K': 1, 'g_Na': 1, 'g_Cl': 1}, -37.33, 0.7466),  # Independent hand calculation: with equal conductances the chord-conductance equation reduces to the arithmetic
    ('hormone_half_life', {'Vd': 7, 'CL': 0.8}, 6.06, 0.1212),  # Feher QHP 3rd ed, §9.1 Problem Set 9.PS1 #9A (TBG): Vd=7 L, metabolic clearance rate=800 mL/day=0.8 L/day. Ind
    ('cck_response', {'fat_g': 5, 'aa_g': 10, 'EC50_fat': 5, 'EC50_aa': 10}, 1.0, 0.02),  # Half-saturation property of a saturable binding term: [S]/(EC50+[S]) = 0.5 when [S]=EC50. At fat_g=EC50_fat=5 
    ('gastrin_acid_response', {'gastrin_pg_mL': 40, 'Amax': 25, 'EC50': 40, 'n': 1.5}, 12.5, 0.25),  # Defining property of the Hill / dose-response equation: at [agonist]=EC50 the response equals Amax/2 regardles
    ('colloid_osmotic_pressure', {'C': 5}, 20.0, 0.4),  # Feher §5.12 p9 albumin empirical (Landis-Pappenheimer) relation pi = 2.8C + 0.18C^2 + 0.012C^3 (C in g/dL), ha
    ('capillary_pressure', {'P_A': 40, 'P_V': 12, 'R_A': 3, 'R_V': 1}, 19.0, 0.38),  # Feher §5.13 Eq 5.13.6 voltage divider P_C = P_A[R_V/(R_A+R_V)] + P_V[R_A/(R_A+R_V)]; hand-calc with R_A/R_V=3:
    ('net_filtration_pressure', {'P_c': 35, 'P_i': -1, 'pi_c': 25, 'pi_i': 3}, 14.0, 0.28),  # Feher Table 5.12.1 (Starling forces, legs/subcutaneous, arteriolar end): P_c=35, P_i=-1, pi_C=25, pi_i=3 -> Ne
    ('net_filtration_pressure', {'P_c': 15, 'P_i': -1, 'pi_c': 25, 'pi_i': 3}, -6.0, 0.12),  # Feher Table 5.12.1 (Starling forces, legs/subcutaneous, venule end): P_c=15, P_i=-1, pi_C=25, pi_i=3 -> Net Pr
    ('ps_product', {'Q': 100, 'E': 0.5}, 69.31, 1.3862),  # Crone-Renkin extraction relation PS = -Q*ln(1-E); hand-calc: -100*ln(0.5) = 100*0.693147 = 69.31 mL/min. Match
    ('wall_shear_stress', {'eta': 0.004, 'Q': 1e-06, 'r': 0.001}, 5.09, 0.1018),  # Poiseuille wall shear stress tau = 4*eta*Q/(pi*r^3); hand-calc: 4*0.004*1e-6/(pi*(1e-3)^3) = 1.6e-8/(3.14159e-
    ('gi_enzyme_kinetics', {'S': 10, 'Vmax': 100, 'Km': 10}, 50.0, 1.0),  # Michaelis-Menten defining identity: at [S]=Km the rate equals Vmax/2. Hand calc 100*10/(10+10)=50.
    ('amylase_kinetics', {'starch_conc': 1.5}, 5.0, 0.1),  # Michaelis-Menten identity at [Starch]=Km(default 1.5): J = J_max/2 = 10/2 = 5 (defaults J_max=10, Km=1.5).
    ('lipase_kinetics', {'TG_conc': 2}, 7.5, 0.15),  # Michaelis-Menten identity at [TG]=Km(default 2.0): J = J_max/2 = 15/2 = 7.5 (defaults J_max=15, Km=2.0).
    ('pepsin_activity', {'H_conc': 5}, 0.5, 0.01),  # Hill-equation defining identity: at [H+]=K_H(default 5.0) activity = A_max/2 = 0.5 (defaults A_max=1.0, K_H=5.
    ('starch_digestion_first_order', {'t': 6.931471805599453, 'starch_0': 100, 'k': 0.1}, 50.0, 1.0),  # First-order exponential decay half-life t=ln(2)/k = 0.6931/0.1 = 6.931 min; at one half-life exactly half the 
    ('diffusion_time', {'x': 0.001, 'D': 1e-09}, 500.0, 10.0),  # physical-foundations.md worked example (D=1e-9 m^2/s, 1 mm -> t ~ 500 s), independently confirmed by hand: (1e
    ('gastric_emptying_liquid', {'t': 20, 'V0': 500, 'k': 0.05}, 183.94, 3.6788),  # Hand calc of first-order decay V0*e^(-k*t): k*t=0.05*20=1.0, e^(-1)=0.367879, 500*0.367879=183.94 mL
    ('gastric_emptying_solid', {'t': 90, 'V0': 300, 't_lag': 30, 'r': 1.5}, 210.0, 4.2),  # Hand calc of linear branch (t>=t_lag): V0 - r*(t-t_lag) = 300 - 1.5*(90-30) = 300 - 90 = 210 g
    ('peristalsis_velocity', {'wavelength': 4, 'frequency': 0.5}, 2.0, 0.04),  # Hand calc of wave relation v=lambda*f = 4 cm * 0.5 Hz = 2 cm/s; matches Feher/reference esophageal peristalsis
    ('gi_transit_time', {'length': 600, 'velocity': 2}, 300.0, 6.0),  # Hand calc t=L/v = 600 cm / 2 cm/s = 300 s
    ('gi_slow_wave', {'t': 5, 'V_rest': -60, 'A': 15, 'f': 0.05}, -45.0, 0.9),  # Hand calc at quarter-period t=1/(4f)=5 s: 2*pi*f*t = pi/2, sin(pi/2)=1, so V = V_rest + A = -60 + 15 = -45 mV 
    ('hydrostatic_pressure', {'rho': 13595.1, 'g': 9.80665, 'h': 0.76}, 101325.0, 2026.5),  # Standard atmosphere via mercury barometer: 760 mmHg = 1 atm. By definition 1 mmHg = rho_Hg(13595.1 kg/m^3) * g
    ('volume_flux', {'Q_V': 8.3333e-05, 'A': 0.00038}, 0.2193, 0.004386),  # Continuity/flux relation v = Q/A with standard physiological inputs: cardiac output 5 L/min = 8.3333e-5 m^3/s 
    ('nernst_equation', {'z': 1, 'C_out': 0.004, 'C_in': 0.14}, -95.0, 1.9),  # Independent hand calc of E = (RT/zF) ln(C_out/C_in) with R=8.314, T=310 K, F=96485: RT/F = 0.026712 V; ln(4/14
    ('ideal_gas_law', {'n': 1, 'T': 273.15, 'V': 0.0224136, 'R': 8.314}, 101325.0, 2026.5),  # STP external anchor: 1 mol of ideal gas occupies the molar volume 22.4136 L = 0.0224136 m^3 at 273.15 K and 1 
    ('redox_free_energy', {'n': 2, 'delta_E': 1.14}, -219986.0, 4399.72),  # Mitochondrial electron-transport span NADH -> O2 has a standard reduction-potential difference delta_E-degree'
    ('coulomb_law', {'q1': 1.602e-19, 'q2': 1.602e-19, 'r': 1e-10}, 2.31e-08, 1e-06),  # Independent hand calc via Coulomb constant k=1/(4*pi*eps0)=8.99e9 N.m^2/C^2. Two elementary charges (e=1.602e-
    ('lennard_jones_potential', {'epsilon': 1.65e-21, 'sigma': 3.4e-10, 'r': 3.816371e-10}, -1.65e-21, 1e-06),  # Analytic property of the LJ 12-6 potential (not from running code): U attains its minimum U=-epsilon at r=2^(1
    ('dipole_potential', {'p': 1e-29, 'theta': 0, 'r': 1e-09, 'kappa': 1}, 0.0899, 0.001798),  # Independent hand calc U=p*cos(theta)/(4*pi*eps0*kappa*r^2)=k*p/r^2 with k=8.99e9, theta=0 (cos=1), kappa=1: 8.
    ('basal_metabolic_rate', {'M': 70}, 1694.0, 33.88),  # Kleiber's law BMR = 70·M^0.75; independent hand calc 70 × 70^0.75 = 1694 kcal/day (matches code docstring ~168
    ('chemiosmotic_coupling', {'delta_psi': 0.15, 'delta_pH': 1, 'F': 96485, 'R': 8.314, 'T_body': 310}, 20400.6, 408.012),  # Mitchell chemiosmotic relation ΔG = F·Δψ + 2.3RT·ΔpH (Feher/reference doc line 294); independent hand calc 964
    ('respiratory_quotient', {'CO2_produced': 16, 'O2_consumed': 23}, 0.6957, 0.013914),  # Palmitate oxidation stoichiometry C16H32O2 + 23 O2 → 16 CO2 + 16 H2O gives RQ = 16/23 = 0.696 (external chemis
    ('donnan_ratio', {'C_protein': 6, 'z_protein': -5, 'C_salt': 20}, 2.0, 0.04),  # Independent hand calculation of the Gibbs-Donnan electroneutrality quadratic [K]1^2 - |z|Cp[K]1 - Csalt^2 = 0.
    ('donnan_potential', {'r': 2}, 0.018516, 0.00037),  # Independent hand calculation: Nernst/Donnan factor RT/F at 310 K = 8.314*310/96485 = 0.026712 V (26.71 mV, sta
    ('hepatic_blood_flow', {'portal': 1.1, 'arterial': 0.4}, 1.5, 0.03),  # Standard total hepatic blood flow is ~1.5 L/min (~25% of cardiac output), from the textbook 75%/25% portal-vei
    ('bilirubin_production', {'Hb_turnover_g': 6, 'conversion_factor': 35}, 210.0, 4.2),  # Classic textbook conversion 35 mg bilirubin per g Hb x ~6 g/day Hb turnover = 210 mg/day of Hb-derived bilirub
    ('first_pass_effect', {'E': 0.7}, 0.3, 0.006),  # Propranolol has hepatic extraction ratio E~=0.7, so F = 1 - E = 0.3, matching propranolol's known oral bioavai
    ('architectural_gear_ratio', {'v_muscle': 70, 'v_fiber': 60.6}, 1.155, 0.0231),  # Feher 3rd ed. §3.4 worked Example 3.4.2 (page verified via PageIndex): muscle-fiber shortening = 60.6 cm/s, wh
    ('ca_force_relationship', {'Ca': 1, 'F_max': 1, 'K_d': 1, 'n': 3}, 0.5, 0.01),  # Analytic half-saturation property of the Hill binding function: at ligand concentration [Ca]=K_d, F = F_max/2 
    ('hill_force_velocity', {'F_0': 100, 'a': 25, 'b': 1, 'F': 0}, 4.0, 0.08),  # Named maximum-velocity relation v_max = b*F_0/a stated in references/excitable-cells.md (Hill force-velocity k
    ('sound_intensity_level_db', {'I_sound': 1e-06, 'I_ref': 1e-12, 'factor': 10}, 60.0, 1.2),  # Standard dB SPL definition; hand calc 10*log10(1e-6/1e-12)=10*log10(1e6)=10*6=60. 1e-12 W/m^2 is the standard 
    ('acoustic_intensity', {'dP0': 1, 'rho': 1.21, 'c': 343}, 0.0012047321880346, 2.4e-05),  # Independent hand evaluation of the standard plane-wave intensity relation I = p0^2/(2*rho*c) = 1^2/(2*1.21*343
    ('net_acid_excretion', {'TA': 30, 'NH4': 40, 'HCO3_excreted': 0}, 70.0, 1.4),  # Standard renal physiology normal component values (Feher Unit 7 §7.7 / renal.md lines 366-384): titratable aci
    ('new_bicarbonate_generation', {'TA': 30, 'NH4': 40}, 70.0, 1.4),  # Standard renal physiology (Feher Unit 7 §7.7 / renal.md lines 366-377): new HCO3- generation = titratable acid
    ('bcm_theory', {'r': 10, 'theta_m': 5, 'learning_rate': 0.01}, 0.5, 0.01),  # Independent hand calculation from defining formula Δw = η·r·(r−θ_m) = 0.01·10·(10−5) = 0.01·10·5 = 0.5 (positi
    ('depression', {'R_n': 0.5, 'u': 0.5, 'tau_rec': 100, 'dt': 10}, 0.3, 0.006),  # Independent hand calculation from defining formula R_{n+1}=R_n(1−u)+(1−R_n)/τ_rec·dt = 0.5·0.5 + 0.5/100·10 = 
    ('facilitation', {'P_n': 0.2, 'F': 0.5}, 0.6, 0.012),  # Independent hand calculation from defining formula P_{n+1}=P_n+F(1−P_n) = 0.2 + 0.5·(1−0.2) = 0.2 + 0.4 = 0.6.
    ('stdp', {'delta_t': 20, 'A_plus': 1, 'A_minus': 1, 'tau_plus': 20, 'tau_minus': 20}, 0.36787944117144233, 0.007358),  # Independent hand calculation from defining formula Δw=A₊·e^(−Δt/τ₊) at Δt=τ₊: 1·e^(−20/20)=e^(−1)=0.367879... 
    ('receptor_occupancy', {'L': 30, 'K_d': 10}, 0.75, 0.015),  # Independent hand calculation of hyperbolic binding isotherm f=[L]/(K_d+[L]) = 30/(10+30) = 0.75 (fractional oc
    ('mifflin_st_jeor_ree', {'W': 68, 'H': 165, 'A': 30, 'sex': 0}, 1401.97, 28.0394),  # Genuine Mifflin-St. Jeor 1990 female equation (height coefficient 6.25, identical to male; constant -161): -16
    ('mifflin_st_jeor_ree', {'W': 80, 'H': 180, 'A': 40, 'sex': 1}, 1732.4, 34.648),  # Mifflin-St. Jeor 1990 male equation: 5 + 9.99*80 + 6.25*180 - 4.92*40 = 5 + 799.2 + 1125 - 196.8 = 1732.4. Ind
    ('harris_benedict_bmr', {'W': 70, 'H': 175, 'A': 30, 'sex': 1}, 1696.5, 33.93),  # Harris-Benedict 1919 male equation as printed in Feher Section 8.6 (66.5 + 13.7*W + 5.0*H - 6.8*A): 66.5 + 13.
    ('harris_benedict_bmr', {'W': 60, 'H': 160, 'A': 30, 'sex': 0}, 1383.7, 27.674),  # Harris-Benedict 1919 female equation (Feher Section 8.6: 655.1 + 9.56*W + 1.85*H - 4.7*A): 655.1 + 9.56*60 + 1
    ('energy_expenditure_indirect_calorimetry', {'VO2': 0.25, 'energy_equiv': 4.85}, 1.2125, 0.02425),  # Feher Section 8.6 mixed-diet energy equivalent of oxygen = 4.85 kcal/L (confirmed in Table 8.6.3 and text). Ha
    ('carbohydrate_oxidation_indirect_calorimetry', {'VO2': 500, 'VCO2': 450, 'n': 20}, 365.5, 7.31),  # Feher Eq 8.6.8 (printed exactly: c = -3.25 VO2 + 4.59 VCO2 - 3.75 n): -3.25*500 + 4.59*450 - 3.75*20 = -1625 +
    ('fat_oxidation_indirect_calorimetry', {'VO2': 500, 'VCO2': 450, 'n': 20}, 49.5, 0.99),  # Feher Eq 8.6.8 (printed exactly: f = 1.69 VO2 - 1.69 VCO2 - 1.75 n): 1.69*500 - 1.69*450 - 1.75*20 = 845 - 760
    ('protein_oxidation_urinary_nitrogen', {'n': 10}, 62.5, 1.25),  # Feher Eq 8.6.6 (p = 6.25 n; protein ~16% N by mass, 1/0.16 = 6.25): 6.25 * 10 = 62.5 g. Independent hand calc.
    ('snells_law', {'n_i': 1, 'theta_i': 0.5235987756, 'n_r': 1.333}, 0.3844979318, 0.00769),  # Standard optics worked result: light passing from air (n=1.0) into water (n=1.333) at 30 deg (0.5236 rad) angl
    ('refractive_power_diopters', {'f': 0.016}, 62.5, 1.25),  # Feher 4.9: relaxed human-eye refractive power is 62.5 D corresponding to focal length f ~ 0.016 m (1/62.5 = 0.
    ('thin_lens_formula', {'O': 0.5, 'I': 0.5}, 0.25, 0.005),  # Thin-lens symmetric imaging (object and image both at 2f): 1/0.5 + 1/0.5 = 4 m^-1, so f = 1/4 = 0.25 m. Indepe
    ('refractive_index', {'c': 299800000, 'v': 200000000}, 1.499, 0.02998),  # Definition n = c/v for a glass-like medium with phase speed v = 2.0e8 m/s: n = 2.998e8/2.0e8 = 1.499. Independ
    ('membrane_capacitance', {'epsilon_m': 2.5, 'delta': 4e-09}, 0.00553, 0.000111),  # Parallel-plate capacitor law C = epsilon_m*epsilon_0/delta with epsilon_0 = 8.85e-12 F/m (standard 3-sig-fig v
    ('surface_free_energy', {'gamma': 0.072, 'dA': 1}, 0.072, 0.00144),  # Feher Eqn 2.5.1 dG = gamma*dA, using the standard measured clean-water surface tension gamma = 0.072 N/m as th
    ('lean_body_mass', {'tbw': 42, 'water_fraction': 0.73}, 57.53, 1.1506),  # Independent hand calculation, not from running the code. TBW for a standard 70 kg man is ~60% of body weight =
    ('orientation_selectivity_index', {'R_pref': 12, 'R_null': 4, 'R_orth_plus': 2, 'R_orth_minus': 1}, 0.8125, 0.01625),  # Feher §4.10 worked example cited in the equation description: (12+4-2-1)/(12+4). Independent hand calculation:
    ('tubuloglomerular_feedback', {'NaCl_md': 40, 'SNGFR_max': 50, 'SNGFR_min': 10, 'K_half': 40, 'n': 2}, 30.0, 0.6),  # Independent hand calculation from the Hill-midpoint identity: at [NaCl]=K_half the fraction K^n/(K^n+[NaCl]^n)
    ('renal_autoregulation_index', {'delta_rbf_pct': 20, 'delta_map_pct': 20}, 1.0, 0.02),  # Definitional pressure-passive limit stated in the docstring/description: when renal blood flow tracks perfusio
    ('clearance', {'U_x': 30, 'V_dot': 1.5, 'P_x': 0.36}, 125.0, 2.5),  # Inulin clearance = GFR; independent hand calc 30 mg/dL x 1.5 mL/min / 0.36 mg/dL = 125 mL/min (canonical GFR).
    ('cockcroft_gault', {'age': 40, 'weight': 72, 'S_Cr': 1, 'female': False}, 100.0, 2.0),  # Independent hand calc of the standard Cockcroft-Gault formula: (140-40) x 72 / (72 x 1.0) = 7200/72 = 100 mL/m
    ('mdrd_gfr', {'Cr': 1, 'age': 50, 'K': 1}, 79.1, 1.582),  # Independent hand calc of the IDMS-traceable MDRD (175) equation: 175 x 1.0^-1.154 x 50^-0.203 x 1.0 = 175 x 0.
    ('filtered_load', {'GFR': 125, 'P_x': 100}, 125.0, 2.5),  # Standard glucose filtered load: at GFR 125 mL/min and plasma glucose 100 mg/dL, FL = 125 mg/min = 180 g/day (F
    ('dissolved_co2', {'PCO2': 40, 'alpha': 0.062}, 2.48, 0.0496),  # Feher §6.4 (Oxygen and Carbon Dioxide Transport): dissolved [CO2] = α·P_CO2 with α = 0.062 mL/(dL·mmHg) for no
    ('osmotic_pressure', {'C': 290, 'sigma': 1, 'R': 8.314, 'T_body': 310}, 747428.6, 14948.572),  # Van't Hoff law pi = sigma*C*R*T with plasma osmolarity 290 mOsm/L = 290 mol/m^3 at body temperature 310 K. Ind
    ('boyle_vant_hoff_relation', {'pi_0': 0.29, 'pi_C': 0.29, 'b': 0.392}, 1.0, 0.02),  # Isotonic boundary condition: when the medium is isotonic (pi_C = pi_0) there is no net osmotic water movement,
    ('k_nernst_potential', {'K_lumen': 4, 'K_cell': 140}, -94.97, 1.8994),  # Independent Nernst hand-calc: E_K = (RT/F)*ln([K]o/[K]i)*1000 with R=8.314 J/(mol.K), F=96485 C/mol, T=310 K (
    ('fe_na', {'U_Na': 40, 'P_Cr': 1, 'P_Na': 140, 'U_Cr': 100}, 0.2857, 0.005714),  # reference.md worked example (line 924: FE_Na U_Na=40, P_Na=140, U_Cr=100, P_Cr=1.0). Independent hand calc: (4
    ('fractional_water_reabsorption', {'TF_P_inulin': 3}, 0.6667, 0.013334),  # Feher 7.4 / Eqn 7.4.15: at end of proximal tubule (TF/P)_inulin ~= 3 => ~2/3 (67%) of filtered water reabsorbe
    ('transport_tm', {'T_max': 375, 'S': 100, 'K_m': 100}, 187.5, 3.75),  # Michaelis-Menten identity: at S = K_m, T = T_max/2. Independent hand calc with glucose T_max=375: 375/2 = 187.
    ('glucose_excretion', {'filtered_load': 500}, 125.0, 2.5),  # Glucose T_m ~= 375 mg/min (Feher; reference.md line 190). Above-Tm branch, independent hand calc: 500 - 375 = 
    ('fractional_excretion', {'C_x': 125, 'GFR': 125}, 1.0, 0.02),  # Textbook identity: inulin clearance equals GFR (inulin freely filtered, not reabsorbed/secreted) so FE_inulin 
    ('glomerular_nfp', {'P_GC': 60, 'P_BC': 15, 'pi_GC': 28, 'pi_BC': 0}, 17.0, 0.34),  # Standard glomerular Starling values (Feher Unit 7 / Guyton): P_GC~60, P_BC~15, pi_GC~28, pi_BC~0 at the affere
    ('gfr_from_nfp', {'K_f': 12.5, 'NFP': 10}, 125.0, 2.5),  # Guyton & Hall standard glomerular values: ultrafiltration coefficient K_f ~= 12.5 mL/min/mmHg and net filtrati
    ('dead_space_bohr', {'P_aCO2': 40, 'P_ECO2': 28}, 0.3, 0.006),  # Independent hand calculation of the Bohr equation (40-28)/40 = 0.30; also matches the standard textbook normal
    ('shunt_equation', {'C_cO2': 20, 'C_aO2': 19.5, 'C_vO2': 15}, 0.1, 0.002),  # Independent hand calculation of the shunt equation (20-19.5)/(20-15) = 0.5/5 = 0.10.
    ('co2_response', {'PaCO2': 50, 'VE0': 5, 'S': 2.5, 'threshold': 40}, 30.0, 0.6),  # Independent hand calculation of the linear CO2 ventilatory response VE = VE0 + S*(PaCO2 - threshold) = 5 + 2.5
    ('hypoxic_response', {'PaO2': 50, 'VE0': 5, 'A': 30, 'B': 30}, 12.5, 0.25),  # Independent hand calculation of the hyperbolic hypoxic ventilatory response VE = VE0*(1 + A/(PaO2 - B)) = 5*(1
    ('total_compliance', {'C_L': 0.2, 'C_CW': 0.2}, 0.1, 0.002),  # references/respiratory.md line 112-116 states series total respiratory compliance C_RS ~ 0.1 L/cmH2O for C_L=C
    ('transmural_pressure', {'P_alv': 0, 'P_pl': -5}, 5.0, 0.1),  # references/respiratory.md line 93: at FRC (no flow) P_alv=0, P_pl~-5 cmH2O gives transpulmonary pressure +5 cm
    ('free_water_clearance', {'V_dot': 2, 'U_osm': 600, 'P_osm': 290}, -2.138, 0.04276),  # Standard free-water-clearance identity C_H2O = V̇ - C_osm with C_osm = (U_osm*V̇)/P_osm. Independent hand calc
    ('urine_osmolality_ratio', {'U_osm': 600, 'P_osm': 300}, 2.0, 0.04),  # U/P osmolality ratio = U_osm/P_osm. Independent hand calc: 600/300 = 2.0 (U/P > 1 -> concentrated urine). Catc
    ('aa_gradient', {'P_AO2': 100, 'P_aO2': 95}, 5.0, 0.1),  # Hand calc 100 - 95 = 5. Normal young-adult A-a gradient 5-15 mmHg (respiratory.md L233, West Respiratory Physi
    ('alveolar_gas_equation', {'P_iO2': 150, 'P_ACO2': 40, 'RQ': 0.8}, 100.0, 2.0),  # Hand calc 150 - 40/0.8 = 150 - 50 = 100. Standard normal alveolar PAO2 ~100 mmHg (respiratory.md L226).
    ('inspired_po2', {'FiO2': 0.21, 'P_B': 760, 'P_H2O': 47}, 149.73, 2.9946),  # Hand calc 0.21 x (760 - 47) = 0.21 x 713 = 149.73; textbook rounds to 150 mmHg (respiratory.md L208).
    ('partial_pressure', {'F_i': 0.21, 'P_total': 760}, 159.6, 3.192),  # Dalton's law atmospheric PO2 = 0.21 x 760 = 159.6 mmHg (respiratory.md L197, standard sea-level dry-air value)
    ('dlco_to_dlo2', {'D_LCO': 25}, 30.75, 0.615),  # Hand calc 1.23 x 25 = 30.75. The 1.23 O2:CO diffusion-coefficient ratio is the standard West/Feher conversion 
    ('minute_ventilation', {'VT': 500, 'f': 12}, 6000.0, 120.0),  # Standard resting minute ventilation ~6 L/min = 6000 mL/min (West/Feher Unit 6; reference.md 'V_E = VT x f'). I
    ('alveolar_ventilation', {'VT': 500, 'VD': 150, 'f': 12}, 4200.0, 84.0),  # Standard resting alveolar ventilation ~4.2 L/min = 4200 mL/min (West/Feher Unit 6; reference.md 'V_A = (VT - V
    ('total_lung_capacity', {'VT': 500, 'IRV': 3000, 'ERV': 1100, 'RV': 1200}, 5800.0, 116.0),  # Standard adult lung volumes (VT500/IRV3000/ERV1100/RV1200); reference.md L44 states TLC ~ 5800 mL. Definitiona
    ('vital_capacity', {'VT': 500, 'IRV': 3000, 'ERV': 1100}, 4600.0, 92.0),  # Standard adult volumes (VT500/IRV3000/ERV1100); reference.md L49 states VC ~ 4600 mL. Definitional sum VC=VT+I
    ('functional_residual_capacity', {'ERV': 1100, 'RV': 1200}, 2300.0, 46.0),  # Standard adult volumes (ERV1100/RV1200); reference.md L54 states FRC ~ 2300 mL. Definitional sum FRC=ERV+RV.
    ('inspiratory_capacity', {'VT': 500, 'IRV': 3000}, 3500.0, 70.0),  # Standard adult volumes (VT500/IRV3000); reference.md L59 states IC ~ 3500 mL. Definitional sum IC=VT+IRV.
    ('alpha_function', {'t': 2, 'g_max': 5, 'tau': 2}, 5.0, 0.1),  # Alpha function g(t)=g_max*(t/tau)*e^(1-t/tau) peaks at t=tau with value g_max. Analytic: (2/2)*e^(1-1)=1*1=1, 
    ('ca_release_cooperative', {'Ca': 15}, 0.5, 0.01),  # Cooperative-binding (Hill) function equals 0.5 at half-saturation where [Ca]=K_d (default K_d=15 uM): 15^4/(15
    ('synaptic_current', {'g_syn': 1, 'V_m': -70, 'E_rev': 0}, -70.0, 1.4),  # Ohm's law I=g*(V-E). SI unit identity: 1 nS * 1 mV = 1e-9 S * 1e-3 V = 1e-12 A = 1 pA, so 1 nS * (-70 mV) = -7
    ('epsp_amplitude', {'g_syn': 1, 'R_in': 100, 'V_m': -70, 'E_rev': 0}, 7.0, 0.14),  # EPSP = I_syn*R_in = g*R*(E_rev-V_m). Dimensionless gain G*R = (1e-9 S)*(1e8 Ohm) = 0.1; times driving force (0
    ('shunting_inhibition', {'g_e': 0, 'E_e': 0, 'g_i': 0, 'E_i': -75, 'g_L': 1, 'E_L': -70}, -70.0, 1.4),  # Physical limit: with no synaptic conductance (g_e=g_i=0) the membrane rests at the leak reversal potential, V_
    ('quantal_variance', {'n': 100, 'p': 0.5, 'q': 1}, 25.0, 0.5),  # Binomial variance theorem: for X~Binomial(n,p), Var(X)=n*p*(1-p)=100*0.5*0.5=25; total response variance = q^2
    ('nmda_mg_block', {'V': 40, 'Mg_out': 1}, 0.977, 0.01954),  # Jahr & Stevens (1990) canonical NMDA Mg-block B(V)=1/(1+[Mg]/3.57*exp(-0.062V)); at V=+40 mV with [Mg]=1 mM th
    ('hill_equation', {'PO2': 26.6, 'P50': 26.6, 'n': 2.7}, 0.5, 0.01),  # Definitional anchor: P50 is by definition the PO2 at which Hb is 50% saturated, so at PO2=P50 the Hill equatio
    ('hill_equation', {'PO2': 40, 'P50': 26.6, 'n': 2.7}, 0.75, 0.015),  # Feher Example 6.4.2 / Fig 6.4.1: at venous PvO2=40 mmHg blood is 'about 75% saturated'. Independent curve-read
    ('oxygen_consumption_fick', {'Q': 5, 'CaO2': 20.7, 'CvO2': 15.72}, 249.0, 4.98),  # Feher Example 6.4.2 (worked example, verbatim): Q_O2 = 5 L/min x (20.7 - 15.72 mL/dL) = 249 mL/min. Independen
    ('oxygen_consumption_gas_exchange', {'Q_T_star': 5, 'fIO2': 0.209, 'Q_T': 4.96, 'fEO2': 0.163}, 237.0, 4.74),  # Feher Example 6.4.3 (worked example, verbatim): Q_O2 = 5.00 L/min x 0.209 - 4.96 L/min x 0.163 = 237 mL/min. I
    ('oxygen_extraction_ratio', {'CaO2': 20.7, 'CvO2': 15.72}, 0.241, 0.00482),  # Hand calculation from the arterial/venous O2 contents Feher gives in Example 6.4.2: (20.7 - 15.72)/20.7 = 0.24
    ('tissue_oxygen_delivery', {'Q': 5, 'CaO2': 20}, 1000.0, 20.0),  # Standard textbook-normal DO2 (reference.md: 'D_O2 ~ 1000 mL O2/min'; West): CO 5 L/min x CaO2 20 mL/dL x 10 = 
    ('carrier_transport', {'S': 2, 'J_max': 100, 'K_m': 2}, 50.0, 1.0),  # Michaelis-Menten half-saturation identity: at [S]=K_m the transport rate is exactly J_max/2 (definition of the
    ('goldman_flux', {'P': 1e-06, 'z': 1, 'V_m': 60.6, 'C_in': 15, 'C_out': 145}, 0.0, 1e-06),  # Thermodynamic invariant: electrodiffusive net flux is zero at the ion's Nernst/equilibrium potential. For z=1,
    ('ussing_flux_ratio', {'C_in': 15, 'C_out': 145, 'z': 1, 'E_m': 0.0606}, -1.0, 0.02),  # At the ion's Nernst potential the two unidirectional passive fluxes are equal, so the magnitude of the flux ra
    ('ncx_reversal', {'E_Na': 60, 'E_Ca': 110}, -40.0, 0.8),  # Cardiac Na+/Ca2+ exchanger (3:1) reversal potential E_NCX=3E_Na-2E_Ca; with representative cardiac E_Na=+60 mV
    ('chronic_respiratory_alkalosis_hco3', {'delta_PCO2':-10}, -5.0, 1e-6),  # HCO3 falls 5/10mmHg PCO2 fall
    ('excretion_mass_balance', {'GFR':125,'P_x':100,'R_x':0,'S_x':0}, 125.0, 1e-3),  # filtered load mg/min
    ('poiseuille_resistance', {'eta':3.5,'L':1,'r':0.15}, 0.13204, 1e-4),  # dimensionally derived
]

def _run():
    p=f=0
    for cid,kw,exp,tol in CASES:
        try:
            g=load(cid).compute(**kw)
            if abs(float(g)-float(exp))<=max(tol,abs(exp)*0.02): print(f"PASS  {cid}"); p+=1
            else: print(f"FAIL  {cid}: got {g!r} exp {exp!r}"); f+=1
        except Exception as e: print(f"ERROR {cid}: {e}"); f+=1
    print(f"\n{p} passed, {f} failed, {len(CASES)} total"); return 1 if f else 0

if __name__=="__main__": sys.exit(_run())

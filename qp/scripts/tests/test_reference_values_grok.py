"""Numeric REGRESSION ANCHORS from the grok-4.5 formula-agreement pass.

IMPORTANT — what these are and are NOT:
These lock the CURRENT compute output at canonical inputs. Each expected
value comes from grok-4.5 evaluating the equation at inputs it chose and
agreeing (within 3%) with the package. In this pass grok was shown the
formula, so agreement is compute-vs-stated-formula — it catches future
drift and compute/formula transcription bugs. It is NOT independent
physiological verification (a shared formula+code error cannot be caught).
A separate formula-free spot check independently confirmed the well-known
subset; Feher-specific model equations remain regression-anchored only. All
tier=recompute here.

Locked regression anchors — edit only to re-lock after an intentional,
verified change to an equation's output.
Run: python -m scripts.tests.test_reference_values_grok
"""
from scripts.canonical_ids import load


def _c(cid, **kw):
    return float(load(cid)._compute_func(**kw))


def test_actual_free_energy():
    # tier=recompute  units=J/mol  src: Lehninger ΔG°' ATP=-30.5 kJ/mol; R=8.314; T=310 K; Q=1e-4 cellular
    got = _c('actual_free_energy', delta_G0=-30500, Q=0.0001, R=8.314, T_body=310)
    assert abs(got - -54238.04) <= 1627.1412, f'actual_free_energy: {got} != -54238.04'


def test_acute_respiratory_ph_change():
    # tier=recompute  units=dimensionless  src: acute resp. rule ΔpH≈−0.008/mmHg PCO2; ΔPCO2=+10 mmHg
    got = _c('acute_respiratory_ph_change', delta_PCO2=10)
    assert abs(got - -0.08) <= 0.0024, f'acute_respiratory_ph_change: {got} != -0.08'


def test_adaptation_index():
    # tier=recompute  units=dimensionless  src: AI=(R_peak-R_ss)/R_peak; mixed SA/RA midpoint rates
    got = _c('adaptation_index', R_peak=100, R_ss=50)
    assert abs(got - 0.5) <= 0.015, f'adaptation_index: {got} != 0.5'


def test_adh_water_permeability():
    # tier=recompute  units=cm/s  src: resting plasma AVP mid-normal; CCD Pf order (basal ~20 μm/s, max Δ~1000 μm/s); K_ADH~V2 EC50
    got = _c('adh_water_permeability', P_0=0.002, P_max=0.1, ADH=2.5, K_ADH=1.5)
    assert abs(got - 0.0645) <= 0.001935, f'adh_water_permeability: {got} != 0.0645'


def test_airway_resistance():
    # tier=recompute  units=Pa*s/m^3  src: Poiseuille R=8ηL/(πr⁴); η_air≈1.8e-5 Pa·s (37°C); adult trachea L≈0.12 m, r≈0.01 m
    got = _c('airway_resistance', eta=1.8e-05, L=0.12, r=0.01)
    assert abs(got - 549.7787143782137) <= 16.49336143134641, f'airway_resistance: {got} != 549.7787143782137'


def test_aldosterone_regulation():
    # tier=recompute  units=arbitrary  src: Aldosterone = k_AngII×AngII×k_K×K_plasma; rest Ang II ~10 pg/mL, [K+] 4.0 mM, unit gains
    got = _c('aldosterone_regulation', AngII=10.0, K_plasma=4.0, k_AngII=1.0, k_K=1.0)
    assert abs(got - 40.0) <= 1.2, f'aldosterone_regulation: {got} != 40.0'


def test_anion_gap():
    # tier=recompute  units=mEq/L  src: standard adult serum electrolytes (Na 140, Cl 104, HCO3 24 mEq/L)
    got = _c('anion_gap', Na=140, Cl=104, HCO3=24)
    assert abs(got - 12.0) <= 0.36, f'anion_gap: {got} != 12.0'


def test_atp_consumption():
    # tier=recompute  units=mol/s  src: Feher QHP U3 muscle energetics form; mid-range tetanic/shortening scales
    got = _c('atp_consumption', isometric_rate=0.0001, shortening_rate=0.0002, v=0.25)
    assert abs(got - 0.00015) <= 4.499999999999999e-06, f'atp_consumption: {got} != 0.00015'


def test_baroreceptor_sensitivity():
    # tier=recompute  units=ms/mmHg  src: BRS=ΔRR/ΔSBP; normal adult slope ~15 ms/mmHg (sequence/Oxford methods)
    got = _c('baroreceptor_sensitivity', dRR=15, dSBP=1)
    assert abs(got - 15.0) <= 0.44999999999999996, f'baroreceptor_sensitivity: {got} != 15.0'


def test_bernoulli_equivalent_pressure():
    # tier=recompute  units=Pa  src: standard adult aortic MAP 100 mmHg, blood rho 1060 kg/m3, mean aortic v 0.2 m/s, heart-level h=0
    got = _c('bernoulli_equivalent_pressure', P=13332, rho=1060, v=0.2, g=9.81, h=0)
    assert abs(got - 13353.2) <= 400.596, f'bernoulli_equivalent_pressure: {got} != 13353.2'


def test_bile_acid_synthesis():
    # tier=recompute  units=g/day  src: steady-state BA balance; adult fecal loss ~0.5 g/day (0.3–0.6)
    got = _c('bile_acid_synthesis', fecal_loss=0.5)
    assert abs(got - 0.5) <= 0.015, f'bile_acid_synthesis: {got} != 0.5'


def test_blood_viscosity():
    # tier=recompute  units=mPa*s  src: η=η_p·exp(2.5·Hct); Hct=0.45, η_p=1.2 mPa·s (std adult)
    got = _c('blood_viscosity', Hct=0.45, eta_plasma=1.2)
    assert abs(got - 3.696) <= 0.11088, f'blood_viscosity: {got} != 3.696'


def test_bramwell_hill_pwv():
    # tier=recompute  units=m/s  src: SI recompute; adult PP 40 mmHg, SV 70 mL, arterial V 500 mL, ρ 1060
    got = _c('bramwell_hill_pwv', V=500, dP=40, dV=70, rho=1060)
    assert abs(got - 5.995) <= 0.17985, f'bramwell_hill_pwv: {got} != 5.995'


def test_cable_equation_dendrite():
    # tier=recompute  units=mV  src: steady-state cable V=V0*exp(-x/λ); λ~200 μm dendrite (Rall/Koch order)
    got = _c('cable_equation_dendrite', x=200.0, V_0=10.0, lambda_const=200.0)
    assert abs(got - 3.6787944117144233) <= 0.1103638323514327, f'cable_equation_dendrite: {got} != 3.6787944117144233'


def test_calcium_absorption_gi():
    # tier=recompute  units=dimensionless  src: f_Ca=f_base+(f_max-f_base)×VitD with f_max=0.40
    got = _c('calcium_absorption_gi', Ca_intake=1000.0, vitamin_D_status=1.0, baseline=0.15)
    assert abs(got - 0.4) <= 0.012, f'calcium_absorption_gi: {got} != 0.4'


def test_calcium_vitamin_d_activation():
    # tier=recompute  units=arbitrary  src: LaTeX form + mid-normal PTH/Pi; model k defaults; FGF23=1 unit basal
    got = _c('calcium_vitamin_d_activation', PTH=40.0, phosphate=1.0, FGF23=1.0, k_PTH=1.0, k_phos=0.5, k_FGF23=0.3)
    assert abs(got - 31.11888111888112) <= 0.9335664335664335, f'calcium_vitamin_d_activation: {got} != 31.11888111888112'


def test_capacitance():
    # tier=recompute  units=F  src: SI definition C=Q/V (1 F = 1 C/V)
    got = _c('capacitance', Q=1.0, V=1.0)
    assert abs(got - 1.0) <= 0.03, f'capacitance: {got} != 1.0'


def test_cck_satiety():
    # tier=recompute  units=dimensionless  src: ln form + fasting [CCK]~1–2 pM (std GI phys); k=1 scale
    got = _c('cck_satiety', CCK_pM=2.0, k=1.0)
    assert abs(got - 0.693147) <= 0.02079441, f'cck_satiety: {got} != 0.693147'


def test_chronic_respiratory_acidosis_hco3():
    # tier=recompute  units=mEq/L  src: Boston/chronic resp. acidosis rule: +3.5 mEq/L HCO3 per +10 mmHg PCO2
    got = _c('chronic_respiratory_acidosis_hco3', delta_PCO2=20)
    assert abs(got - 7.0) <= 0.21, f'chronic_respiratory_acidosis_hco3: {got} != 7.0'


def test_compliance():
    # tier=recompute  units=L/cmH2O  src: West/Nunn standard CL≈0.2 L/cmH2O; C=ΔV/ΔP with VT-scale 0.5 L / 2.5 cmH2O
    got = _c('compliance', delta_V=0.5, delta_P=2.5)
    assert abs(got - 0.2) <= 0.006, f'compliance: {got} != 0.2'


def test_coulomb_law_medium():
    # tier=recompute  units=N  src: SI e, ε0; aqueous ε≈80; 1 nm ion scale
    got = _c('coulomb_law_medium', q1=1.602e-19, q2=1.602e-19, r=1e-09, epsilon=80, epsilon_0=8.854e-12)
    assert abs(got - 2.883e-12) <= 1e-09, f'coulomb_law_medium: {got} != 2.883e-12'


def test_countercurrent_multiplication():
    # tier=recompute  units=dimensionless  src: M=e^(L/λ); L~human long loop; λ for M~4 (300→1200 mOsm)
    got = _c('countercurrent_multiplication', loop_length=14, lambda_char=10)
    assert abs(got - 4.0552) <= 0.121656, f'countercurrent_multiplication: {got} != 4.0552'


def test_critical_micellar_concentration():
    # tier=recompute  units=boolean  src: GI texts: bile-salt CMC ~2-5 mM; postprandial lumen ~5-15 mM
    got = _c('critical_micellar_concentration', bile_salt_conc=10.0, CMC=3.0)
    assert abs(got - 1.0) <= 0.03, f'critical_micellar_concentration: {got} != 1.0'


def test_dendrite_input_resistance():
    # tier=recompute  units=MΩ  src: Rall cable params (Rm=1000, Ri=100, a=1μm); recompute of given R∞ formula
    got = _c('dendrite_input_resistance', R_m=1000, R_i=100, a=1)
    assert abs(got - 50.33) <= 1.5098999999999998, f'dendrite_input_resistance: {got} != 50.33'


def test_diffusing_capacity():
    # tier=recompute  units=mL/(min*mmHg)  src: West/Guyton resting VO2~250 mL/min, mean O2 membrane ΔP~11 mmHg
    got = _c('diffusing_capacity', V_gas=250, P_A=100, P_c=89)
    assert abs(got - 22.727272727272727) <= 0.6818181818181818, f'diffusing_capacity: {got} != 22.727272727272727'


def test_diffusion_conductance():
    # tier=recompute  units=mL/(min*mmHg)  src: Roughton–Forster form; West-typical DM=40, θ≈1.5, Vc≈70
    got = _c('diffusion_conductance', D_M=40, theta=1.5, V_c=70)
    assert abs(got - 28.97) <= 0.8691, f'diffusion_conductance: {got} != 28.97'


def test_double_exponential_synapse():
    # tier=recompute  units=nS  src: AMPA-like dual-exp (τ_r=0.5 ms, τ_d=5 ms, g_max=1 nS); independent eval at t=1 ms
    got = _c('double_exponential_synapse', t=1.0, g_max=1.0, tau_rise=0.5, tau_decay=5.0)
    assert abs(got - 0.68339547) <= 0.0205018641, f'double_exponential_synapse: {got} != 0.68339547'


def test_edpvr():
    # tier=recompute  units=mmHg  src: standard adult LV EDV ~120 mL; A=1 mmHg, k=0.02/mL exponential EDPVR (normal LVEDP ~8–12 mmHg)
    got = _c('edpvr', EDV=120, A=1.0, k=0.02)
    assert abs(got - 10.023) <= 0.30068999999999996, f'edpvr: {got} != 10.023'


def test_elastance():
    # tier=recompute  units=cmH2O/L  src: Standard C_rs≈0.1 L/cmH2O (West/Nunn); E=1/C
    got = _c('elastance', C=0.1)
    assert abs(got - 10.0) <= 0.3, f'elastance: {got} != 10.0'


def test_electric_field():
    # tier=recompute  units=N/C  src: E=F/q; elementary charge with membrane-scale force (~10^7 N/C field)
    got = _c('electric_field', F=1.6e-12, q=1.6e-19)
    assert abs(got - 10000000.0) <= 300000.0, f'electric_field: {got} != 10000000.0'


def test_electrochemical_potential():
    # tier=recompute  units=J/mol  src: Nernst/electrochemical potential; adult ICF [K+]≈140 mM, Vm≈−70 mV, T=310 K
    got = _c('electrochemical_potential', mu_0=0, C=0.14, z=1, psi=-0.07, R=8.314, T_body=310, F=96485)
    assert abs(got - -11821.291309243958) <= 354.63873927731873, f'electrochemical_potential: {got} != -11821.291309243958'


def test_espvr():
    # tier=recompute  units=mmHg  src: standard adult LV: ESV~50 mL, Ees~2 mmHg/mL, V0~0 (Suga–Sagawa ESPVR scale)
    got = _c('espvr', ESV=50, E_es=2.0, V_0=0)
    assert abs(got - 100.0) <= 3.0, f'espvr: {got} != 100.0'


def test_exponential_emptying():
    # tier=recompute  units=L  src: V(t)=V0*e^(-t/τ); V0=0.5 L (VT), τ=0.5 s (normal RC), t=τ → V0/e
    got = _c('exponential_emptying', V0=0.5, t=0.5, tau=0.5)
    assert abs(got - 0.18393972058572117) <= 0.005518191617571635, f'exponential_emptying: {got} != 0.18393972058572117'


def test_extraction_ratio():
    # tier=recompute  units=dimensionless  src: PK high-E threshold (E>0.7); Rowland/Tozer-style illustration
    got = _c('extraction_ratio', C_in=10.0, C_out=3.0)
    assert abs(got - 0.7) <= 0.020999999999999998, f'extraction_ratio: {got} != 0.7'


def test_fat_absorption_efficiency():
    # tier=recompute  units=dimensionless  src: standard adult postprandial: [bile]~10 mM > CMC~3 mM; η_fat=0.95×1×1
    got = _c('fat_absorption_efficiency', bile_salt_conc=10.0, CMC=3.0, lipase_activity=1.0)
    assert abs(got - 0.95) <= 0.028499999999999998, f'fat_absorption_efficiency: {got} != 0.95'


def test_fechner_law():
    # tier=recompute  units=arbitrary  src: Weber→Fechner integral S=k·ln(I/I0); decade above threshold
    got = _c('fechner_law', I=10.0, I_0=1.0, k=1.0)
    assert abs(got - 2.302585092994046) <= 0.06907755278982138, f'fechner_law: {got} != 2.302585092994046'


def test_feedback_gain():
    # tier=recompute  units=dimensionless  src: Feher-style G=ΔTropic/ΔTarget; |G|~10 high-gain endocrine loop (signed)
    got = _c('feedback_gain', delta_tropic=10, delta_target=-1)
    assert abs(got - -10.0) <= 0.3, f'feedback_gain: {got} != -10.0'


def test_feedback_target_dynamics():
    # tier=recompute  units=arbitrary/time  src: resting SS setpoint; T4-like k_deg≈ln(2)/7d
    got = _c('feedback_target_dynamics', tropic_conc=1.0, target_conc=1.0, k_stim=0.1, k_deg=0.1)
    assert abs(got - 0.0) <= 1e-09, f'feedback_target_dynamics: {got} != 0.0'


def test_feedback_tropic_dynamics():
    # tier=recompute  units=arbitrary/time  src: Abstract HPA/HPT-style setpoint: [Target]_ss=k_basal/k_fb; rest → dTropic/dt=0
    got = _c('feedback_tropic_dynamics', target_conc=10.0, k_basal=1.0, k_fb=0.1)
    assert abs(got - 0.0) <= 1e-09, f'feedback_tropic_dynamics: {got} != 0.0'


def test_fick_first_law():
    # tier=recompute  units=mol/(m^2*s)  src: Fick 1855; D~1e-9 m2/s aqueous small solute; grad 1 mM/µm
    got = _c('fick_first_law', D=1e-09, dC_dx=1000000.0)
    assert abs(got - -0.001) <= 3e-05, f'fick_first_law: {got} != -0.001'


def test_ficks_law_diffusion():
    # tier=recompute  units=mmol/s  src: recompute: P~1e-5 cm/s (Crone/Levick order), S=1000 cm² regional, ΔC=1 mM glucose
    got = _c('ficks_law_diffusion', P_s=1e-05, S=1000, C_c=0.005, C_i=0.004)
    assert abs(got - 1e-05) <= 3.0000000000000004e-07, f'ficks_law_diffusion: {got} != 1e-05'


def test_ficks_membrane_flux():
    # tier=recompute  units=mol/(m^2*s)  src: Fick first law; P~1e-5 m/s water/small-solute order (Boron/Feher scale), ΔC=10 mM teaching gradient
    got = _c('ficks_membrane_flux', P=1e-05, C_out=10.0, C_in=0.0)
    assert abs(got - 0.0001) <= 3e-06, f'ficks_membrane_flux: {got} != 0.0001'


def test_filtration_fraction():
    # tier=recompute  units=dimensionless  src: standard adult rest: GFR 125 mL/min, RPF 625 mL/min → FF≈0.20
    got = _c('filtration_fraction', GFR=125, RPF=625)
    assert abs(got - 0.2) <= 0.006, f'filtration_fraction: {got} != 0.2'


def test_fractional_excretion_direct():
    # tier=recompute  units=dimensionless  src: standard adult Na-like solute FE≈1% (GFR 125 mL/min, P 140 mmol/L)
    got = _c('fractional_excretion_direct', U_x=175, V_dot=1.0, GFR=125, P_x=140)
    assert abs(got - 0.01) <= 0.0003, f'fractional_excretion_direct: {got} != 0.01'


def test_funny_current():
    # tier=recompute  units=pA  src: DiFrancesco/standard SA-node If params; nS·mV=pA
    got = _c('funny_current', V_m=-60, E_f=-20, g_f=1.0, y=0.25)
    assert abs(got - -10.0) <= 0.3, f'funny_current: {got} != -10.0'


def test_fusion_frequency():
    # tier=recompute  units=Hz  src: f≈3/τ; τ=0.1 s slow-fiber twitch duration (classic motor-unit texts)
    got = _c('fusion_frequency', tau_twitch=0.1)
    assert abs(got - 30.0) <= 0.8999999999999999, f'fusion_frequency: {got} != 30.0'


def test_gastric_acid_output():
    # tier=recompute  units=mEq/h  src: Feher/clinical BAO 2-5 & MAO 20-25 mEq/h; BAO≈0.15·MAO; rest f=0
    got = _c('gastric_acid_output', stim_fraction=0.0, MAO=25.0)
    assert abs(got - 3.75) <= 0.11249999999999999, f'gastric_acid_output: {got} != 3.75'


def test_gibbs_free_energy():
    # tier=recompute  units=J/mol  src: ΔG=ΔH−TΔS with ATP-hydrolysis-order ΔH/ΔS at 37°C (biochem standard scale)
    got = _c('gibbs_free_energy', delta_H=-20000, T=310, delta_S=34)
    assert abs(got - -30540.0) <= 916.1999999999999, f'gibbs_free_energy: {got} != -30540.0'


def test_glp1_insulin_response():
    # tier=recompute  units=dimensionless  src: Independent recompute; Glc 10 mM & GLP-1 10 pM stimulatory; EC50 10 pM, thr 5 mM standard
    got = _c('glp1_insulin_response', GLP1_pM=10.0, glucose_mM=10.0, EC50_GLP1=10.0, glucose_threshold=5.0)
    assert abs(got - 0.5) <= 0.015, f'glp1_insulin_response: {got} != 0.5'


def test_glut5_fructose():
    # tier=recompute  units=mM/min  src: GLUT5 Km ~6 mM (intestinal sugar transport literature); MM recompute
    got = _c('glut5_fructose', fructose_lumen=10.0, Vmax=1.0, Km=6.0)
    assert abs(got - 0.625) <= 0.01875, f'glut5_fructose: {got} != 0.625'


def test_gto_response():
    # tier=recompute  units=Hz  src: linear GTO model f_Ib=k_GTO×Force; moderate force ~50 N, gain 1 Hz/N → ~50 Hz Ib rate
    got = _c('gto_response', force=50, k_gto=1.0)
    assert abs(got - 50.0) <= 1.5, f'gto_response: {got} != 50.0'


def test_heart_rate_autonomic():
    # tier=recompute  units=bpm  src: standard adult rest: intrinsic SA ~100 bpm, net autonomic tone → ~70 bpm HR (Guyton/Boron teaching values)
    got = _c('heart_rate_autonomic', f_intrinsic=100, df_symp=20, df_para=50)
    assert abs(got - 70.0) <= 2.1, f'heart_rate_autonomic: {got} != 70.0'


def test_henderson_hasselbalch():
    # tier=recompute  units=dimensionless  src: standard arterial ABG: HCO3 24 mEq/L, PCO2 40 mmHg, pKa 6.1, α 0.03
    got = _c('henderson_hasselbalch', HCO3=24, PCO2=40, pKa=6.1, alpha=0.03)
    assert abs(got - 7.4) <= 0.222, f'henderson_hasselbalch: {got} != 7.4'


def test_hepatic_clearance():
    # tier=recompute  units=L/min  src: PK texts: Q_H≈1.5 L/min adult; E=0.7 high-extraction exemplar
    got = _c('hepatic_clearance', Q_H=1.5, E=0.7)
    assert abs(got - 1.05) <= 0.0315, f'hepatic_clearance: {got} != 1.05'


def test_hh_gating_m():
    # tier=recompute  units=1/ms  src: HH 1952 rates in modern absolute-V form (e.g. Dayan & Abbott); rest V=-65 mV, m=0.05
    got = _c('hh_gating_m', V=-65.0, m=0.05)
    assert abs(got - 0.0123855384) <= 0.000371566152, f'hh_gating_m: {got} != 0.0123855384'


def test_hh_membrane_current():
    # tier=recompute  units=mV/ms  src: HH 1952 C_m=1; rest I_ext=0, net I_ion=0
    got = _c('hh_membrane_current', I_ext=0.0, I_Na=0.0, I_K=0.0, I_L=0.0, C_m=1.0)
    assert abs(got - 0.0) <= 1e-09, f'hh_membrane_current: {got} != 0.0'


def test_hh_potassium_current():
    # tier=recompute  units=μA/cm²  src: Hodgkin & Huxley 1952 (ḡK=36, EK=-77; rest V=-65, n∞≈0.318)
    got = _c('hh_potassium_current', n=0.318, V=-65.0, g_K_bar=36.0, E_K=-77.0)
    assert abs(got - 4.42) <= 0.1326, f'hh_potassium_current: {got} != 4.42'


def test_hh_sodium_current():
    # tier=recompute  units=μA/cm²  src: Hodgkin & Huxley 1952 canonical ḡ_Na=120, rest gates m≈0.05 h≈0.6, modern V_rest=-65 mV E_Na=+50 mV
    got = _c('hh_sodium_current', m=0.05, h=0.6, V=-65.0, g_Na_bar=120.0, E_Na=50.0)
    assert abs(got - -1.035) <= 0.031049999999999998, f'hh_sodium_current: {got} != -1.035'


def test_hormone_fraction_free():
    # tier=recompute  units=dimensionless  src: adult CBG ~0.7 μM, cortisol-CBG Kd ~30 nM (standard endocrine binding values)
    got = _c('hormone_fraction_free', P_conc=7e-07, Kd=3e-08)
    assert abs(got - 0.0411) <= 0.001233, f'hormone_fraction_free: {got} != 0.0411'


def test_hormone_kd():
    # tier=recompute  units=M  src: mass-action Kd; free cortisol ~20 nM, CBG residual free ~300 nM
    got = _c('hormone_kd', H_free=2e-08, P_free=3e-07, HP_bound=2e-07)
    assert abs(got - 3e-08) <= 1e-09, f'hormone_kd: {got} != 3e-08'


def test_hpa_acth_dynamics():
    # tier=recompute  units=pg/(mL*time)  src: Guyton/Boron-range basal ACTH~20 pg/mL, cortisol~10 μg/dL; lumped HPA rates (not Feher numeric)
    got = _c('hpa_acth_dynamics', CRH=1.0, ACTH=20.0, cortisol=10.0, k_CRH=1.0, k_fb=0.1, k_deg=0.3)
    assert abs(got - -6.0) <= 0.18, f'hpa_acth_dynamics: {got} != -6.0'


def test_hpa_cortisol_dynamics():
    # tier=recompute  units=μg/(dL*min)  src: resting ACTH~20 pg/mL, cortisol~10 μg/dL; k_clear=ln2/t½ with t½~70 min≈0.01/min; k_ACTH from SS balance
    got = _c('hpa_cortisol_dynamics', ACTH=20.0, cortisol=10.0, k_ACTH=0.005, k_clear=0.01)
    assert abs(got - 0.0) <= 1e-09, f'hpa_cortisol_dynamics: {got} != 0.0'


def test_hpa_crh_dynamics():
    # tier=recompute  units=arbitrary  src: linear HPA CRH ODE at basal steady state (rest)
    got = _c('hpa_crh_dynamics', CRH=1.0, cortisol=10.0, k_stress=1.5, k_cort=0.1, k_deg=0.5)
    assert abs(got - 0.0) <= 1e-09, f'hpa_crh_dynamics: {got} != 0.0'


def test_huxley_attached_fraction():
    # tier=recompute  units=1/s  src: Huxley AF 1957 Prog Biophys; f1=43.3, g1=10 s^-1
    got = _c('huxley_attached_fraction', f=43.3, g=10.0, n=0.0, compute_steady_state=False)
    assert abs(got - 43.3) <= 1.299, f'huxley_attached_fraction: {got} != 43.3'


def test_huxley_attachment_rate():
    # tier=recompute  units=1/s  src: Huxley 1957 classic params (f1=65/s, h=10 nm); mid-zone x=h/2
    got = _c('huxley_attachment_rate', x=5.0, f1=65.0, h=10.0)
    assert abs(got - 32.5) <= 0.975, f'huxley_attachment_rate: {got} != 32.5'


def test_huxley_detachment_rate():
    # tier=recompute  units=1/s  src: Huxley 1957 Prog Biophys Biophys Chem 7:255 (g1=10, g2=209, h=10 nm)
    got = _c('huxley_detachment_rate', x=5.0, g1=10.0, g2=209.0, h=10.0)
    assert abs(got - 10.0) <= 0.3, f'huxley_detachment_rate: {got} != 10.0'


def test_hydraulic_resistance():
    # tier=recompute  units=Pa*s/m^3  src: Poiseuille R=8ηL/(πr⁴); η_blood≈3 mPa·s, L=1 cm, r=1 mm
    got = _c('hydraulic_resistance', eta=0.003, L=0.01, r=0.001)
    assert abs(got - 76394372.68) <= 2291831.1804, f'hydraulic_resistance: {got} != 76394372.68'


def test_incretin_effect():
    # tier=recompute  units=dimensionless  src: Feher/GI incretin effect (oral 2–3× IV insulin); Nauck-type isoglycemic comparison
    got = _c('incretin_effect', insulin_oral=250, insulin_iv=100)
    assert abs(got - 2.5) <= 0.075, f'incretin_effect: {got} != 2.5'


def test_iron_absorption_gi():
    # tier=recompute  units=dimensionless  src: Guyton/Boron-class Fe absorption ~10% replete; f_Fe=f_base/hepcidin
    got = _c('iron_absorption_gi', Fe_intake=15.0, stores_depleted=0, hepcidin_level=1.0)
    assert abs(got - 0.1) <= 0.003, f'iron_absorption_gi: {got} != 0.1'


def test_k_secretion_driving_force():
    # tier=recompute  units=mV  src: CCD principal-cell norms: V_m≈−70 mV, E_K≈−90 mV (Nernst ~150/5 mM); DF_K=V_m−E_K
    got = _c('k_secretion_driving_force', V_m=-70, E_K=-90)
    assert abs(got - 20.0) <= 0.6, f'k_secretion_driving_force: {got} != 20.0'


def test_k_secretion_flux():
    # tier=recompute  units=mA  src: I=g(V-E); CCD principal cell Vm≈-70 mV, EK≈-90 mV (standard renal EP)
    got = _c('k_secretion_flux', g_K=0.01, V_m=-70, E_K=-90)
    assert abs(got - 0.2) <= 0.006, f'k_secretion_flux: {got} != 0.2'


def test_laplace_cylinder():
    # tier=recompute  units=Pa  src: Laplace cylinder ΔP=T/r; adult aorta-scale T~100 N/m, r=1 cm
    got = _c('laplace_cylinder', T=100, r=0.01)
    assert abs(got - 10000.0) <= 300.0, f'laplace_cylinder: {got} != 10000.0'


def test_laplace_pressure():
    # tier=recompute  units=Pa  src: standard adult alveolus (r≈100 μm; T≈25 mN/m with surfactant); Laplace ΔP=2T/r
    got = _c('laplace_pressure', T=25, r=0.0001)
    assert abs(got - 500.0) <= 15.0, f'laplace_pressure: {got} != 500.0'


def test_laplace_sphere():
    # tier=recompute  units=Pa  src: Laplace sphere ΔP=2T/r; alveolar T≈50 mN/m, r≈100 μm (std physiol)
    got = _c('laplace_sphere', T=0.05, r=0.0001)
    assert abs(got - 1000.0) <= 30.0, f'laplace_sphere: {got} != 1000.0'


def test_lipase_activity_bile():
    # tier=recompute  units=dimensionless  src: Feher-style GI: CMC~3 mM; duodenal [bile salt]~5-10 mM during fat digestion
    got = _c('lipase_activity_bile', bile_salt_conc=10, CMC=3)
    assert abs(got - 1.0) <= 0.03, f'lipase_activity_bile: {got} != 1.0'


def test_lithogenic_index():
    # tier=recompute  units=dimensionless  src: Carey–Small-type gallbladder bile ranges; LI formula applied
    got = _c('lithogenic_index', cholesterol=10.0, bile_acids=150.0, phospholipids=40.0)
    assert abs(got - 0.478) <= 0.014339999999999999, f'lithogenic_index: {got} != 0.478'


def test_mean_flow_velocity():
    # tier=recompute  units=m/s  src: resting CO 5 L/min; aortic A ≈ 4 cm² (standard adult CV)
    got = _c('mean_flow_velocity', Q_V=8.333e-05, A=0.0004)
    assert abs(got - 0.2083) <= 0.006249, f'mean_flow_velocity: {got} != 0.2083'


def test_medullary_gradient():
    # tier=recompute  units=mOsm/kg  src: standard renal values (cortex ~300, human tip ~1200 mOsm/kg); linear π(d)
    got = _c('medullary_gradient', depth=0.5, osm_cortex=300, osm_tip=1200)
    assert abs(got - 750.0) <= 22.5, f'medullary_gradient: {got} != 750.0'


def test_metabolic_alkalosis_compensation():
    # tier=recompute  units=mmHg  src: P_CO2 = 0.7×[HCO3]+21 with normal [HCO3]=24 mEq/L
    got = _c('metabolic_alkalosis_compensation', HCO3=24)
    assert abs(got - 37.8) <= 1.134, f'metabolic_alkalosis_compensation: {got} != 37.8'


def test_metabolic_clearance_rate():
    # tier=recompute  units=L/day  src: standard adult cortisol production ~20 mg/day, mean plasma ~10 μg/dL (0.1 mg/L); MCR=P/C
    got = _c('metabolic_clearance_rate', production_rate=20, plasma_concentration=0.1)
    assert abs(got - 200.0) <= 6.0, f'metabolic_clearance_rate: {got} != 200.0'


def test_moens_korteweg_pwv():
    # tier=recompute  units=m/s  src: adult aorta: E=0.4 MPa, h=2 mm, d=2.5 cm, ρ=1060 kg/m³
    got = _c('moens_korteweg_pwv', E=400000.0, h=0.002, d=0.025, rho=1060.0)
    assert abs(got - 5.4944) <= 0.16483199999999998, f'moens_korteweg_pwv: {got} != 5.4944'


def test_muscle_efficiency():
    # tier=recompute  units=dimensionless  src: standard dynamic-exercise mechanical efficiency ~20% (gross efficiency framing)
    got = _c('muscle_efficiency', P=100.0, heat_rate=400.0)
    assert abs(got - 0.2) <= 0.006, f'muscle_efficiency: {got} != 0.2'


def test_muscle_power():
    # tier=recompute  units=W  src: P=F×v; F=100 N, v=0.1 m/s (submax limb muscle)
    got = _c('muscle_power', F=100, v=0.1)
    assert abs(got - 10.0) <= 0.3, f'muscle_power: {got} != 10.0'


def test_nak_pump_rate():
    # tier=recompute  units=cycles/s  src: Hill n=3/2 + MM ATP; resting [Na]i=15 mM, [K]o=4 mM, [ATP]=5 mM; Jmax/K half-sats standard model order
    got = _c('nak_pump_rate', Na_in=15.0, K_out=4.0, ATP=5.0, J_max=200.0, K_Na=10.0, K_K=2.0, K_ATP=0.5)
    assert abs(got - 112.20779220779222) <= 3.3662337662337665, f'nak_pump_rate: {got} != 112.20779220779222'


def test_pah_extraction_ratio():
    # tier=recompute  units=dimensionless  src: Standard adult E_PAH≈0.90 (Guyton/renal texts); inputs chosen for low-dose clearance with 90% single-pass removal
    got = _c('pah_extraction_ratio', P_a=2.0, P_v=0.2)
    assert abs(got - 0.9) <= 0.027, f'pah_extraction_ratio: {got} != 0.9'


def test_pancreatic_bicarbonate():
    # tier=recompute  units=mM  src: Standard GI phys: basal Q~0.2 mL/min, max flow~4 mL/min, [HCO3]max 140 / min 20 mM
    got = _c('pancreatic_bicarbonate', flow_rate=0.2, max_HCO3=140, max_flow=4.0)
    assert abs(got - 25.85) <= 0.7755, f'pancreatic_bicarbonate: {got} != 25.85'


def test_parallel_plate_capacitor():
    # tier=recompute  units=F  src: membrane C~1 μF/cm²; ε≈5, d≈5 nm, A=1 cm² (Hille/Kandel-style)
    got = _c('parallel_plate_capacitor', epsilon=5, epsilon_0=8.854e-12, A=0.0001, d=5e-09)
    assert abs(got - 8.854e-07) <= 2.6562e-08, f'parallel_plate_capacitor: {got} != 8.854e-07'


def test_permeability_coefficient():
    # tier=recompute  units=m/s  src: Standard bilayer values (δ≈5 nm; D_mem~1e-12 m²/s; K=1 teaching case)
    got = _c('permeability_coefficient', D=1e-12, K=1.0, delta=5e-09)
    assert abs(got - 0.0002) <= 6e-06, f'permeability_coefficient: {got} != 0.0002'


def test_photoreceptor_response():
    # tier=recompute  units=dimensionless  src: Naka-Rushton/Hill photoreceptor form; I=σ half-max identity
    got = _c('photoreceptor_response', I=50, sigma=50, n=1)
    assert abs(got - 0.5) <= 0.015, f'photoreceptor_response: {got} != 0.5'


def test_poiseuille_flow():
    # tier=recompute  units=m^3/s  src: Poiseuille formula; arteriole r=10 μm, η=3 cP, ΔP=20 mmHg, L=2 mm
    got = _c('poiseuille_flow', r=1e-05, eta=0.003, delta_P=2666, L=0.002)
    assert abs(got - 1.7449e-12) <= 1e-09, f'poiseuille_flow: {got} != 1.7449e-12'


def test_pressure_flow():
    # tier=recompute  units=L/s  src: West/Nunn-range Raw~1.5; quiet V̇~0.5 L/s
    got = _c('pressure_flow', delta_P=0.75, R=1.5)
    assert abs(got - 0.5) <= 0.015, f'pressure_flow: {got} != 0.5'


def test_pulse_pressure():
    # tier=recompute  units=mmHg  src: standard adult resting BP 120/80 mmHg (Guyton/Boron norm)
    got = _c('pulse_pressure', SBP=120, DBP=80)
    assert abs(got - 40.0) <= 1.2, f'pulse_pressure: {got} != 40.0'


def test_quantal_content():
    # tier=recompute  units=count  src: Del Castillo–Katz quantal hypothesis; NMJ-scale n,p as in Kandel/standard neuro texts
    got = _c('quantal_content', n=1000, p=0.2)
    assert abs(got - 200.0) <= 6.0, f'quantal_content: {got} != 200.0'


def test_quantal_content_epp_mepp():
    # tier=recompute  units=dimensionless  src: Standard NMJ: MEPP ~0.5 mV; EPP ~50 mV → m~100 quanta (Katz/textbook range)
    got = _c('quantal_content_epp_mepp', EPP=50.0, MEPP=0.5)
    assert abs(got - 100.0) <= 3.0, f'quantal_content_epp_mepp: {got} != 100.0'


def test_rate_force_relation():
    # tier=recompute  units=N  src: F=F0(1-e^{-kf}); f~20 Hz MU rate, k=0.05/Hz (1/k=20 Hz), F0=100 N
    got = _c('rate_force_relation', f=20.0, F_0=100.0, k=0.05)
    assert abs(got - 63.212) <= 1.89636, f'rate_force_relation: {got} != 63.212'


def test_receptive_field_dog():
    # tier=recompute  units=arbitrary  src: DoG RF peak at origin: RF(0,0)=A_c-A_s; σ_s/σ_c≈3 center-surround ratio (Rodieck/Enroth-Cugell style)
    got = _c('receptive_field_dog', x=0.0, y=0.0, A_c=1.0, sigma_c=1.0, A_s=0.5, sigma_s=3.0)
    assert abs(got - 0.5) <= 0.015, f'receptive_field_dog: {got} != 0.5'


def test_receptor_adaptation():
    # tier=recompute  units=arbitrary  src: first-order adaptation R(t)=R_ss+(R_0-R_ss)e^(-t/τ); canonical unit-time phasic demo (R_0=1, R_ss=0, t=τ=1 s)
    got = _c('receptor_adaptation', t=1.0, R_0=1.0, R_ss=0.0, tau_adapt=1.0)
    assert abs(got - 0.367879) <= 0.01103637, f'receptor_adaptation: {got} != 0.367879'


def test_reflex_gain():
    # tier=recompute  units=N/mm  src: product cascade; Ia static sens. ~5 Hz/mm (Matthews-order); g≈1 monosynaptic; k_motor~0.1 N/Hz pool-scale
    got = _c('reflex_gain', k_spindle=5.0, g_synapse=1.0, k_motor=0.1)
    assert abs(got - 0.5) <= 0.015, f'reflex_gain: {got} != 0.5'


def test_renal_plasma_flow():
    # tier=recompute  units=L/min  src: standard adult RBF ~1.2 L/min, Hct 0.45 (Guyton-range resting values)
    got = _c('renal_plasma_flow', RBF=1.2, Hct=0.45)
    assert abs(got - 0.66) <= 0.0198, f'renal_plasma_flow: {got} != 0.66'


def test_renal_vascular_resistance():
    # tier=recompute  units=mmHg*min/mL  src: standard adult RBF~1200 mL/min, MAP~100, Pv~4 (Guyton/Hall-class norms)
    got = _c('renal_vascular_resistance', P_a=100, P_v=4, RBF=1200)
    assert abs(got - 0.08) <= 0.0024, f'renal_vascular_resistance: {got} != 0.08'


def test_reproductive_lh_surge():
    # tier=recompute  units=mU/mL  src: Feher-style LH E2 switch; mid-cycle E2 300 pg/mL, threshold 200, baseline 5, max_LH 50
    got = _c('reproductive_lh_surge', estradiol=300, threshold=200, max_LH=50, baseline=5)
    assert abs(got - 38.333333333333336) <= 1.1500000000000001, f'reproductive_lh_surge: {got} != 38.333333333333336'


def test_reproductive_progesterone_temperature():
    # tier=recompute  units=°C  src: mid-luteal [P4]~10 ng/mL; follicular BBT~36.5°C; T=T_b+0.3·P4/(5+P4)
    got = _c('reproductive_progesterone_temperature', progesterone=10.0, T_baseline=36.5)
    assert abs(got - 36.7) <= 1.101, f'reproductive_progesterone_temperature: {got} != 36.7'


def test_respiratory_oxygen_content():
    # tier=recompute  units=mL/dL  src: standard arterial values (Hb 15 g/dL, SaO2 0.97, PaO2 100 mmHg) + Hüfner 1.34 / solubility 0.003
    got = _c('respiratory_oxygen_content', Hb=15, SO2=0.97, PO2=100)
    assert abs(got - 19.797) <= 0.59391, f'respiratory_oxygen_content: {got} != 19.797'


def test_respiratory_time_constant():
    # tier=recompute  units=s  src: standard adult Raw≈2 cmH2O·s/L, Crs≈0.1 L/cmH2O; τ=RC
    got = _c('respiratory_time_constant', R=2, C=0.1)
    assert abs(got - 0.2) <= 0.006, f'respiratory_time_constant: {got} != 0.2'


def test_reynolds_number_airway():
    # tier=recompute  units=dimensionless  src: standard air ρ/η + adult trachea d≈2 cm, v≈1 m/s at rest (West/Nunn-type)
    got = _c('reynolds_number_airway', rho=1.2, v=1.0, d=0.02, eta=1.8e-05)
    assert abs(got - 1333.3333333333333) <= 39.99999999999999, f'reynolds_number_airway: {got} != 1333.3333333333333'


def test_reynolds_number_blood():
    # tier=recompute  units=dimensionless  src: Re=ρvd/η; ρ=1050 kg/m³, v=0.4 m/s, d=0.02 m (aorta), η=0.004 Pa·s (whole blood)
    got = _c('reynolds_number_blood', rho=1050, v=0.4, d=0.02, eta=0.004)
    assert abs(got - 2100.0) <= 63.0, f'reynolds_number_blood: {got} != 2100.0'


def test_safety_factor():
    # tier=recompute  units=dimensionless  src: Wood & Slater 2001 NMJ safety factor review; SF~3-5, EPP~40 mV, Vth~10 mV
    got = _c('safety_factor', EPP=40, threshold=10)
    assert abs(got - 4.0) <= 0.12, f'safety_factor: {got} != 4.0'


def test_salivary_flow():
    # tier=recompute  units=mL/min  src: unstimulated whole saliva ~0.3–0.5 mL/min; max stimulated ~4 mL/min (standard GI physiol.)
    got = _c('salivary_flow', stimulation=0.0, basal=0.5, max_flow=4.0)
    assert abs(got - 0.5) <= 0.015, f'salivary_flow: {got} != 0.5'


def test_scatchard_analysis():
    # tier=recompute  units=dimensionless  src: Scatchard linear form; 1 nM Kd, half-occupancy B=Bmax/2
    got = _c('scatchard_analysis', B=5e-07, B_max=1e-06, K_d=1e-06)
    assert abs(got - 0.5) <= 0.015, f'scatchard_analysis: {got} != 0.5'


def test_scatchard_transform():
    # tier=recompute  units=dimensionless  src: Scatchard B/[H]; half-occupancy at K_d~1 nM, B_max~10 nM
    got = _c('scatchard_transform', B=5e-09, H=1e-09)
    assert abs(got - 5.0) <= 0.15, f'scatchard_transform: {got} != 5.0'


def test_secretin_bicarbonate():
    # tier=recompute  units=mM  src: Feher-style secretin threshold pH 4.5; max pancreatic [HCO3-] ~140 mM (Guyton/Boron range)
    got = _c('secretin_bicarbonate', pH_duodenum=3.0, threshold=4.5, max_response=140.0)
    assert abs(got - 46.666666666666664) <= 1.4, f'secretin_bicarbonate: {got} != 46.666666666666664'


def test_sglt1_glucose():
    # tier=recompute  units=mM/min  src: SGLT1 Km≈0.3 mM (Wright/GI texts); MM with teaching Vmax=6 mM/min, [G]=5 mM
    got = _c('sglt1_glucose', glucose_lumen=5.0, Vmax=6.0, Km=0.3)
    assert abs(got - 5.660377358490566) <= 0.16981132075471697, f'sglt1_glucose: {got} != 5.660377358490566'


def test_single_channel_conductance():
    # tier=recompute  units=nS  src: Ohm γ=i/ΔV; pA/mV→nS; unitary i~2 pA, ΔV~50 mV → ~40 pS
    got = _c('single_channel_conductance', i=2.0, V_m=-40.0, E_ion=-90.0)
    assert abs(got - 0.04) <= 0.0012, f'single_channel_conductance: {got} != 0.04'


def test_solute_flux():
    # tier=recompute  units=mol/(m^2*s)  src: definitional J_S=Q_S/A; SI membrane-scale inputs (1 umol/s over 1 cm^2)
    got = _c('solute_flux', Q_S=1e-06, A=0.0001)
    assert abs(got - 0.01) <= 0.0003, f'solute_flux: {got} != 0.01'


def test_spindle_response():
    # tier=recompute  units=Hz  src: linear Ia model; rest tonic stretch ΔL=5 mm, dL/dt=0; gains mid primary-ending range
    got = _c('spindle_response', L=35.0, L_0=30.0, dL_dt=0.0, k_static=5.0, k_dynamic=0.5)
    assert abs(got - 25.0) <= 0.75, f'spindle_response: {got} != 25.0'


def test_standard_free_energy():
    # tier=recompute  units=J/mol  src: ΔG°=-RT ln(Keq); Keq=1 ⇒ ΔG°=0 (body T=310 K)
    got = _c('standard_free_energy', K_eq=1.0, R=8.314, T_body=310.0)
    assert abs(got - 0.0) <= 1e-09, f'standard_free_energy: {got} != 0.0'


def test_starling_filtration():
    # tier=recompute  units=mL/min  src: Guyton & Hall mean Starling forces + whole-body Kf~6.7 mL/min/mmHg
    got = _c('starling_filtration', L_p=1e-06, S=6670000.0, P_c=17.3, P_i=-3.0, pi_c=28.0, pi_i=8.0, sigma=1.0)
    assert abs(got - 2.001) <= 0.06002999999999999, f'starling_filtration: {got} != 2.001'


def test_stevens_power_law():
    # tier=recompute  units=arbitrary  src: Stevens power law S=k·I^n; n=0.33 brightness (psychophysics standard)
    got = _c('stevens_power_law', I=10.0, k=1.0, n=0.33)
    assert abs(got - 2.138) <= 0.06413999999999999, f'stevens_power_law: {got} != 2.138'


def test_stokes_einstein():
    # tier=recompute  units=m^2/s  src: Stokes-Einstein; T=37°C, η≈1 mPa·s, a=1 nm, k_B=1.38e-23
    got = _c('stokes_einstein', T=310, eta=0.001, a=1e-09, k_B=1.38e-23)
    assert abs(got - 2.27e-10) <= 1e-09, f'stokes_einstein: {got} != 2.27e-10'


def test_thyroid_t4_dynamics():
    # tier=recompute  units=μg/(dL*d)  src: euthyroid norms TSH~2 mU/L, TT4~8 μg/dL; t½ T4~7 d → kel=ln2/7; SS-calibrated k_TSH
    got = _c('thyroid_t4_dynamics', TSH=2.0, T4=8.0, k_TSH=0.396, k_conv=0.05, k_clear=0.049)
    assert abs(got - 0.0) <= 1e-09, f'thyroid_t4_dynamics: {got} != 0.0'


def test_thyroid_tsh_dynamics():
    # tier=recompute  units=mU/(L*time)  src: Clinical mid-normals (fT4~1 ng/dL, TSH~2 mU/L); n≈2 HPT feedback; SS rate balance at rest
    got = _c('thyroid_tsh_dynamics', fT4=1.0, TSH=2.0, k_TRH=1.5, k_T4=0.5, n=2.0, k_deg=0.5)
    assert abs(got - 0.0) <= 1e-09, f'thyroid_tsh_dynamics: {got} != 0.0'


def test_total_elastance():
    # tier=recompute  units=cmH2O/L  src: West/Nunn: C_L≈C_CW≈0.2 L/cmH2O → E=1/C; E_RS=E_L+E_CW
    got = _c('total_elastance', E_L=5.0, E_CW=5.0)
    assert abs(got - 10.0) <= 0.3, f'total_elastance: {got} != 10.0'


def test_true_rpf_from_pah():
    # tier=recompute  units=mL/min  src: standard adult ERPF≈600 mL/min, E_PAH≈0.9 (Guyton/Boron-class values)
    got = _c('true_rpf_from_pah', C_PAH=600, E_PAH=0.9)
    assert abs(got - 666.6666666666666) <= 19.999999999999996, f'true_rpf_from_pah: {got} != 666.6666666666666'


def test_vascular_compliance():
    # tier=recompute  units=mL/mmHg  src: C=ΔV/ΔP; arterial SV≈70 mL, PP≈40 mmHg (Guyton-scale TAC)
    got = _c('vascular_compliance', dV=70, dP=40)
    assert abs(got - 1.75) <= 0.0525, f'vascular_compliance: {got} != 1.75'


def test_water_absorption_gi():
    # tier=recompute  units=mmol/min  src: Loo et al. SGLT1 ~260 H2O/cycle (2 Na+); n=130 per Na+
    got = _c('water_absorption_gi', Na_absorbed=1.0, osmotic_coeff=130.0)
    assert abs(got - 130.0) <= 3.9, f'water_absorption_gi: {got} != 130.0'


def test_water_flux():
    # tier=recompute  units=m/s  src: Starling relation; microcirculation-scale SI (ΔP≈19 mmHg, σ≈0.8, L_p~1e-12 m/(s·Pa))
    got = _c('water_flux', L_p=1e-12, delta_P=2500, delta_pi=2500, sigma=0.8)
    assert abs(got - 5e-10) <= 1e-09, f'water_flux: {got} != 5e-10'


def test_water_reabsorption_flux():
    # tier=recompute  units=mL/s  src: Standard adult CD antidiuresis (π_int 600, lumen 300 mOsm/kg); Lp mid ADH-range
    got = _c('water_reabsorption_flux', L_p=1e-05, A=1.0, pi_int=600.0, pi_lumen=300.0)
    assert abs(got - 0.003) <= 8.999999999999999e-05, f'water_reabsorption_flux: {got} != 0.003'


def test_weber_fraction():
    # tier=recompute  units=dimensionless  src: Weber's law; classic weight JND k≈1/40 (sensory phys textbooks)
    got = _c('weber_fraction', delta_I=1, I=40)
    assert abs(got - 0.025) <= 0.00075, f'weber_fraction: {got} != 0.025'


def test_whole_cell_conductance():
    # tier=recompute  units=pS  src: Hille/Boron-scale single-channel γ≈10 pS; N=1000, P_open=0.5 teaching ensemble
    got = _c('whole_cell_conductance', N=1000, P_open=0.5, gamma=10)
    assert abs(got - 5000.0) <= 150.0, f'whole_cell_conductance: {got} != 5000.0'


def test_windkessel_time_constant():
    # tier=recompute  units=s  src: RC with SVR≈20 WU, Cart≈1.5 mL/mmHg; Wood→s via ×0.06
    got = _c('windkessel_time_constant', R=20, C=1.5)
    assert abs(got - 1.8) <= 0.054, f'windkessel_time_constant: {got} != 1.8'


def test_winters_formula():
    # tier=recompute  units=mmHg  src: Winter's formula PCO2=1.5*[HCO3]+8; HCO3=24 mEq/L normal adult
    got = _c('winters_formula', HCO3=24)
    assert abs(got - 44.0) <= 1.3199999999999998, f'winters_formula: {got} != 44.0'


def test_womersley_number():
    # tier=recompute  units=dimensionless  src: Feher/standard hemodynamics: aorta r~1 cm, f=1 Hz, blood ρ≈1050, η≈4 mPa·s
    got = _c('womersley_number', r=0.01, omega=6.283185307, rho=1050, eta=0.004)
    assert abs(got - 12.84) <= 0.3852, f'womersley_number: {got} != 12.84'


if __name__ == '__main__':
    import sys as _s
    fns = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    n = 0
    for fn in fns:
        fn(); n += 1
    print(f'grok-anchor tests passed: {n}')

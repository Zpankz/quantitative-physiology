"""Consolidated module for renal.clearance."""

"""
General clearance equation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
from scripts.units import creatinine_to_mgdl


def compute_clearance(U_x: float, V_dot: float, P_x: float) -> float:
    """
    Calculate clearance of substance x.

    Args:
        U_x: Urine concentration of substance (mg/dL or mmol/L)
        V_dot: Urine flow rate (mL/min)
        P_x: Plasma concentration of substance (same units as U_x)

    Returns:
        C_x: Clearance of substance x (mL/min)
    """
    return (U_x * V_dot) / P_x


# Create equation
clearance = create_equation(
    id="clearance",
    produces='C_x',
    output_units='mL/min',
    name="General Clearance Equation",
    category=EquationCategory.RENAL,
    latex=r"C_x = \frac{U_x \times \dot{V}}{P_x}",
    simplified="C_x = (U_x × V̇) / P_x",
    description="Volume of plasma completely cleared of a substance per unit time",
    compute_func=compute_clearance,
    parameters=[
        Parameter(
            name="U_x",
            description="Urine concentration of substance",
            units="mg/dL or mmol/L",
            symbol="U_x",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="V_dot",
            description="Urine flow rate",
            units="mL/min",
            symbol=r"\dot{V}",
            physiological_range=(0.5, 20)
        ),
        Parameter(
            name="P_x",
            description="Plasma concentration of substance",
            units="mg/dL or mmol/L",
            symbol="P_x",
            physiological_range=(0.1, 100)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(clearance)

"""
Cockcroft-Gault equation for creatinine clearance estimation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_cockcroft_gault(age: float, weight: float, S_Cr: float, female: bool = False, S_Cr_units: str = "mg/dL") -> float:
    """
    Estimate creatinine clearance using Cockcroft-Gault equation.

    Args:
        age: Patient age (years)
        weight: Body weight (kg)
        S_Cr: Serum creatinine (mg/dL)
        female: True if patient is female

    Returns:
        C_Cr: Estimated creatinine clearance (mL/min)
    """
    S_Cr = creatinine_to_mgdl(S_Cr, S_Cr_units)
    C_Cr = ((140 - age) * weight) / (72 * S_Cr)
    if female:
        C_Cr *= 0.85
    return C_Cr


# Create equation
cockcroft_gault = create_equation(
    id="cockcroft_gault",
    output_units='mL/min',
    name="Cockcroft-Gault Equation",
    category=EquationCategory.RENAL,
    latex=r"C_{Cr} = \frac{(140 - age) \times weight}{72 \times S_{Cr}} \times [0.85 \text{ if female}]",
    simplified="C_Cr = [(140 - age) × weight] / (72 × S_Cr) × [0.85 if female]",
    description="Clinical estimate of creatinine clearance from age, weight, and serum creatinine",
    compute_func=compute_cockcroft_gault,
    parameters=[
        Parameter(
            name="age",
            description="Patient age",
            units="years",
            symbol="age",
            physiological_range=(18, 100)
        ),
        Parameter(
            name="weight",
            description="Body weight",
            units="kg",
            symbol="weight",
            physiological_range=(40, 150)
        ),
        Parameter(
            name="S_Cr",
            description="Serum creatinine",
            units="mg/dL",
            symbol="S_{Cr}",
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="female",
            description="Sex (True for female)",
            units="boolean",
            symbol="female",
            default_value=False
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(cockcroft_gault)

"""
Filtered load calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_filtered_load(GFR: float, P_x: float) -> float:
    """
    Calculate amount of substance filtered per unit time.

    Args:
        GFR: Glomerular filtration rate (mL/min)
        P_x: Plasma concentration of substance (mg/dL)

    Returns:
        FL: Filtered load (mg/min). The /100 converts mg/dL to mg/mL so that
        mL/min * mg/mL = mg/min (e.g. GFR 125 mL/min, glucose 100 mg/dL -> 125 mg/min).
    """
    return GFR * P_x / 100.0


# Create equation
filtered_load = create_equation(
    id="filtered_load",
    output_units='mg/min',
    name="Filtered Load",
    category=EquationCategory.RENAL,
    latex=r"FL = GFR \times P_x",
    simplified="FL = GFR × P_x",
    description="Amount of substance filtered at the glomerulus per unit time",
    compute_func=compute_filtered_load,
    parameters=[
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        ),
        Parameter(
            name="P_x",
            description="Plasma concentration of substance (mg/dL; compute divides by 100 for mg/dL->mg/mL, so mg/dL only)",
            units="mg/dL",
            symbol="P_x",
            physiological_range=(0, 1000)
        )
    ],
    depends_on=["gfr_from_nfp"],
    produces="FL",
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(filtered_load)

"""
PAH extraction ratio and true RPF calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_extraction_ratio(P_a: float, P_v: float) -> float:
    """
    Calculate extraction ratio for PAH.

    Args:
        P_a: Arterial plasma PAH concentration
        P_v: Venous plasma PAH concentration

    Returns:
        E: Extraction ratio (dimensionless, ~0.9 for PAH)
    """
    return (P_a - P_v) / P_a


def compute_true_rpf(C_PAH: float, E_PAH: float) -> float:
    """
    Calculate true RPF from PAH clearance and extraction ratio.

    Args:
        C_PAH: PAH clearance (mL/min)
        E_PAH: PAH extraction ratio (dimensionless)

    Returns:
        RPF: True renal plasma flow (mL/min)
    """
    return C_PAH / E_PAH


# Create extraction ratio equation
pah_extraction_ratio = create_equation(
    id="pah_extraction_ratio",
    output_units='dimensionless',
    name="PAH Extraction Ratio",
    category=EquationCategory.RENAL,
    latex=r"E_{PAH} = \frac{P_a - P_v}{P_a}",
    simplified="E_PAH = (P_a - P_v) / P_a",
    description="Fraction of PAH removed from arterial blood in single pass through kidney",
    compute_func=compute_extraction_ratio,
    parameters=[
        Parameter(
            name="P_a",
            description="Arterial plasma PAH concentration",
            units="mg/dL",
            symbol="P_a",
            physiological_range=(0, 10)
        ),
        Parameter(
            name="P_v",
            description="Venous plasma PAH concentration",
            units="mg/dL",
            symbol="P_v",
            physiological_range=(0, 2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Create true RPF equation
true_rpf_from_pah = create_equation(
    id="true_rpf_from_pah",
    output_units='mL/min',
    name="True RPF from PAH",
    category=EquationCategory.RENAL,
    latex=r"RPF = \frac{C_{PAH}}{E_{PAH}}",
    simplified="RPF = C_PAH / E_PAH",
    description="Calculate true renal plasma flow correcting for incomplete PAH extraction",
    compute_func=compute_true_rpf,
    parameters=[
        Parameter(
            name="C_PAH",
            description="PAH clearance",
            units="mL/min",
            symbol="C_{PAH}",
            physiological_range=(500, 800)
        ),
        Parameter(
            name="E_PAH",
            description="PAH extraction ratio",
            units="dimensionless",
            symbol="E_{PAH}",
            default_value=0.9,
            physiological_range=(0.85, 0.95)
        )
    ],
    depends_on=["pah_extraction_ratio", "clearance"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equations
register_equation(pah_extraction_ratio)
register_equation(true_rpf_from_pah)



# --- coverage pass additions (Feher extraction) ---

def compute_mdrd_gfr(Cr, age, K=1.0, Cr_units="mg/dL"):
    """MDRD Study eGFR in mL/min/1.73 m^2 from IDMS-standardized serum creatinine [Cr] (mg/dL), Age (years), and group correction constant K (1.0 default, 0.742 female, 1.212 African American). Feher Unit 7, sec 7.4 'Plasma creatinine concentration alone indicates the GFR'."""
    Cr = creatinine_to_mgdl(Cr, Cr_units)
    return 175.0 * (Cr ** -1.154) * (age ** -0.203) * K

mdrd_gfr = create_equation(
    id='mdrd_gfr',
    output_units='mL/min',
    name='MDRD Study Equation (eGFR)',
    category=EquationCategory.RENAL,
    latex='\\mathrm{GFR}\\,(\\mathrm{mL\\,min^{-1}}/1.73\\,\\mathrm{m^2}) = 175 \\times [\\mathrm{Cr}]^{-1.154} \\times \\mathrm{Age}^{-0.203} \\times K',
    simplified='GFR (mL/min/1.73m^2) = 175 * [Cr]^(-1.154) * Age^(-0.203) * K',
    description='Modification of Diet in Renal Disease (MDRD) Study equation: estimates glomerular filtration rate normalized to 1.73 m^2 body surface area from IDMS-standardized serum creatinine, age, and a group correction constant K (0.742 if female, 1.212 if African American). A widely used clinical eGFR estimator that avoids the errors of 24-hour urine collection but is invalid for persons with abnormal creatinine production (extreme body size/muscle mass, amputees, paraplegics, morbid obesity, vegetarian diets, creatine supplements). Distinct from the weight-based Cockcroft-Gault creatinine-clearance estimator.',
    compute_func=compute_mdrd_gfr,
    parameters=[
        Parameter(name='Cr', description='Serum creatinine, IDMS (isotope-dilution mass spectrometry) standardized', units='mg/dL', symbol='[Cr]', physiological_range=(0.5, 15)),
        Parameter(name='age', description='Patient age (MDRD validated in adults)', units='years', symbol='Age', physiological_range=(18, 100)),
        Parameter(name='K', description='Group correction constant: 1.0 for adult male / non-Black (default), 0.742 if female, 1.212 if African American', units='dimensionless', symbol='K', default_value=1, physiological_range=(0.742, 1.212)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=7, source_chapter='7.4',
                              source_section='PLASMA CREATININE CONCENTRATION ALONE INDICATES THE GFR', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(mdrd_gfr)

try:
    __all__ += ['mdrd_gfr']
except NameError:
    __all__ = ['mdrd_gfr']


# --- review-add 2026-07-15 ---
def compute_ttkg(U_K: float, P_K: float, U_osm: float, P_osm: float) -> float:
    """Transtubular K+ gradient = (U_K/P_K)/(U_osm/P_osm).

    Valid only when U_osm > P_osm and U_Na > 25."""
    return (U_K / P_K) / (U_osm / P_osm)

ttkg_equation = create_equation(
    id='ttkg',
    name='Transtubular Potassium Gradient',
    category=EquationCategory.RENAL,
    latex=r'TTKG = \\frac{U_K/P_K}{U_{osm}/P_{osm}}',
    simplified='TTKG = (U_K/P_K) / (U_osm/P_osm)',
    description='Transtubular potassium gradient, an index of distal K+ secretory drive (aldosterone effect). <3 suggests hypoaldosteronism in hyperkalaemia; >7 an appropriate renal response.',
    compute_func=compute_ttkg,
    output_units='dimensionless',
    parameters=[
        Parameter(name='U_K', description='Urine potassium', units='mmol/L', symbol='U_K', physiological_range=(5, 120)),
        Parameter(name='P_K', description='Plasma potassium', units='mmol/L', symbol='P_K', physiological_range=(2.5, 7.0)),
        Parameter(name='U_osm', description='Urine osmolality', units='mOsm/kg', symbol='U_osm', physiological_range=(300, 1200)),
        Parameter(name='P_osm', description='Plasma osmolality', units='mOsm/kg', symbol='P_osm', physiological_range=(275, 310)),
    ],
    metadata=EquationMetadata(source_unit=7, source_chapter='7.6'),
)
register_equation(ttkg_equation)


# --- review-add 2026-07-15 ---
def compute_ckd_epi_2021(S_Cr: float, age: float, female: float = 0.0,
                         S_Cr_units: str = "mg/dL") -> float:
    """CKD-EPI 2021 creatinine eGFR (race-free; Inker 2021).

    S_Cr in mg/dL (pass S_Cr_units='umol/L' for SI labs, e.g. Australian);
    age in years, female=1.0/0.0."""
    S_Cr = creatinine_to_mgdl(S_Cr, S_Cr_units)
    kappa = 0.7 if female >= 0.5 else 0.9
    alpha = -0.241 if female >= 0.5 else -0.302
    r = S_Cr / kappa
    egfr = 142.0 * (min(r, 1.0) ** alpha) * (max(r, 1.0) ** -1.200) * (0.9938 ** age)
    if female >= 0.5:
        egfr *= 1.012
    return egfr

ckd_epi_2021_equation = create_equation(
    id='ckd_epi_2021',
    name='CKD-EPI 2021 eGFR',
    category=EquationCategory.RENAL,
    latex=r'eGFR = 142 \\cdot \\min(S_{Cr}/\\kappa,1)^{\\alpha}\\cdot \\max(S_{Cr}/\\kappa,1)^{-1.2}\\cdot 0.9938^{age}\\cdot[1.012\\ \\text{if F}]',
    simplified='eGFR = 142 * min(Scr/k,1)^a * max(Scr/k,1)^-1.2 * 0.9938^age * (1.012 if F)',
    description='CKD-EPI 2021 race-free creatinine eGFR (Inker NEJM 2021), the modern lab reporting standard; kappa/alpha are sex-specific.',
    compute_func=compute_ckd_epi_2021,
    output_units='mL/min/1.73m^2',
    parameters=[
        Parameter(name='S_Cr', description='Serum creatinine', units='mg/dL', symbol='S_Cr', physiological_range=(0.3, 15.0)),
        Parameter(name='age', description='Age', units='years', symbol='age', physiological_range=(18, 100)),
        Parameter(name='female', description='Female flag (1/0)', units='dimensionless', symbol='female', physiological_range=(0.0, 1.0)),
    ],
    metadata=EquationMetadata(source_unit=7, source_chapter='7.5'),
)
register_equation(ckd_epi_2021_equation)


# --- per-solute + glomerular additive (2026-07-15) ---
def compute_sodium_clearance(U_Na: float, V_dot: float, P_Na: float) -> float:
    """Sodium clearance C_Na = U_Na*V/P_Na (typed per-solute producer)."""
    return (U_Na * V_dot) / P_Na

sodium_clearance = create_equation(
    id="sodium_clearance", name="Sodium Clearance", category=EquationCategory.RENAL,
    latex=r"C_{Na} = \frac{U_{Na}\,\dot V}{P_{Na}}", simplified="C_Na = U_Na*V/P_Na",
    description="Renal clearance of sodium; a solute-typed producer (produces C_Na) so propagate can carry Na alongside creatinine for FE-Na without the generic-symbol collision.",
    compute_func=compute_sodium_clearance, output_units="mL/min", produces="C_Na",
    parameters=[Parameter(name="U_Na", description="Urine sodium", units="mmol/L", symbol="U_Na", physiological_range=(5,300)),
                Parameter(name="V_dot", description="Urine flow rate", units="mL/min", symbol="Vdot", physiological_range=(0.5,20)),
                Parameter(name="P_Na", description="Plasma sodium", units="mmol/L", symbol="P_Na", physiological_range=(120,160))],
    metadata=EquationMetadata(source_unit=7, source_chapter="7.2"),
)
register_equation(sodium_clearance)


# --- per-solute + glomerular additive (2026-07-15) ---
def compute_creatinine_clearance_typed(U_Cr: float, V_dot: float, P_Cr: float) -> float:
    """Creatinine clearance C_Cr = U_Cr*V/P_Cr (typed per-solute producer)."""
    return (U_Cr * V_dot) / P_Cr

creatinine_clearance_typed = create_equation(
    id="creatinine_clearance_typed", name="Creatinine Clearance (typed)", category=EquationCategory.RENAL,
    latex=r"C_{Cr} = \frac{U_{Cr}\,\dot V}{P_{Cr}}", simplified="C_Cr = U_Cr*V/P_Cr",
    description="Renal clearance of creatinine as a solute-typed producer (produces C_Cr), pairing with sodium_clearance so a single propagate run carries both solutes for FE-Na.",
    compute_func=compute_creatinine_clearance_typed, output_units="mL/min", produces="C_Cr",
    parameters=[Parameter(name="U_Cr", description="Urine creatinine", units="mg/dL", symbol="U_Cr", physiological_range=(10,300)),
                Parameter(name="V_dot", description="Urine flow rate", units="mL/min", symbol="Vdot", physiological_range=(0.5,20)),
                Parameter(name="P_Cr", description="Plasma creatinine", units="mg/dL", symbol="P_Cr", physiological_range=(0.3,15))],
    metadata=EquationMetadata(source_unit=7, source_chapter="7.2"),
)
register_equation(creatinine_clearance_typed)


# --- per-solute + glomerular additive (2026-07-15) ---
def compute_gfr_from_glomerular_nfp(K_f: float, NFP_glomerular: float) -> float:
    """GFR from the renal-local glomerular NFP: GFR = K_f * NFP_glomerular."""
    return K_f * NFP_glomerular

gfr_from_glomerular_nfp = create_equation(
    id="gfr_from_glomerular_nfp", name="GFR from Glomerular NFP", category=EquationCategory.RENAL,
    latex=r"GFR = K_f \times NFP_{glom}", simplified="GFR = K_f * NFP_glomerular",
    description="GFR from the renal-local glomerular net filtration pressure (produced by glomerular_nfp, P_GC/P_BC/pi form). Additive companion to gfr_from_nfp (which uses the cross-domain cardiovascular NFP as its dependency example).",
    compute_func=compute_gfr_from_glomerular_nfp, output_units="mL/min", produces="GFR_glom",
    depends_on=["glomerular_nfp"],
    parameters=[Parameter(name="K_f", description="Ultrafiltration coefficient", units="mL/min/mmHg", symbol="K_f", physiological_range=(5,20)),
                Parameter(name="NFP_glomerular", description="Glomerular net filtration pressure", units="mmHg", symbol="NFP_glom", physiological_range=(5,20))],
    metadata=EquationMetadata(source_unit=7, source_chapter="7.3"),
)
register_equation(gfr_from_glomerular_nfp)

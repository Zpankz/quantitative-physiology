"""Saturation kinetics - Enzyme- and carrier-mediated processes.

Includes:
- Michaelis-Menten equation (saturable flux / reaction rate)

Michaelis-Menten is a foundational, cross-domain relationship (it recurs in
membrane carrier transport, renal tubular transport maxima, GI absorption and
hormone-receptor kinetics). It previously had no home module, which broke the
documented `from scripts.foundations.kinetics import michaelis_menten` import
and left `registry.py`/`physiology_core.py` as its only (non-importable or
orphaned) definitions. This module is that home.

The Hill equation (cooperative binding) is the natural companion here, but it
already has a single canonical home at `scripts.respiratory.oxygen_transport`
(`hill_equation`). To avoid a second module-level object with the same id
(which would create a duplicate-id collision), it is NOT re-exported here.
Import Hill from its home module instead.

Source: Feher, Quantitative Human Physiology 3rd ed., Unit 2 (Membranes,
Transport and Metabolism), Section 2.6 "Passive Transport and Facilitated
Diffusion", where carrier-mediated (facilitated) transport is described by
Michaelis-Menten saturation kinetics. Verified via the corpus extract; the
extract preserves section/equation numbering rather than book page numbers, so
page_reference is left None (not fabricated).
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_michaelis_menten(S: float, J_max: float, K_m: float) -> float:
    """
    Saturable flux / reaction rate (Michaelis-Menten kinetics).

    Formula: J = J_max * [S] / (K_m + [S])

    Parameters
    ----------
    S : float - Substrate (or transported solute) concentration
    J_max : float - Maximum flux / velocity as [S] -> infinity
    K_m : float - Michaelis constant; [S] at which J = J_max/2

    Returns
    -------
    J : float - Flux / rate in the same units as J_max
    """
    return J_max * S / (K_m + S)


michaelis_menten = create_equation(
    id="michaelis_menten",
    output_units='mM/s',
    name="Michaelis-Menten Kinetics",
    category=EquationCategory.FOUNDATIONS,
    latex=r"J = \frac{J_{max}\,[S]}{K_m + [S]}",
    simplified="J = J_max * S / (K_m + S)",
    description=(
        "Saturation kinetics for enzyme- and carrier-mediated processes. "
        "At [S] << K_m flux is first-order in [S]; at [S] >> K_m flux "
        "saturates at J_max. K_m equals the substrate concentration giving "
        "half-maximal flux. Underlies carrier transport, tubular transport "
        "maxima (Tm), GI absorption and receptor binding."
    ),
    compute_func=compute_michaelis_menten,
    parameters=[
        Parameter(
            name="S",
            description="Substrate / transported solute concentration",
            units="mM",
            symbol="[S]",
            physiological_range=(0.0, 1000.0),
        ),
        Parameter(
            name="J_max",
            description="Maximum flux / velocity (saturating)",
            units="mM/s",
            symbol="J_max",
            physiological_range=(0.0, 1e6),
        ),
        Parameter(
            name="K_m",
            description="Michaelis constant ([S] at half-maximal flux)",
            units="mM",
            symbol="K_m",
            physiological_range=(1e-6, 1000.0),
        ),
    ],
    depends_on=[],
    # NOTE: MM is filed in the foundations domain as a cross-domain primitive
    # (per SKILL.md's cross-domain table), but Feher develops carrier saturation
    # (Michaelis-Menten) kinetics in Unit 2, Section 2.6 ("Passive Transport and
    # Facilitated Diffusion"). source_unit therefore reflects the true Feher
    # provenance (2) rather than the foundations module's unit (1) -- the one
    # intentional exception to the package's domain==source_unit convention.
    # Relocate this equation to the membrane domain if strict convention is preferred.
    metadata=EquationMetadata(
        source_unit=2,
        source_chapter="2.6",
        source_section="Passive Transport and Facilitated Diffusion (carrier saturation kinetics)",
        page_reference=None,  # Feher extract retains section/equation numbers, not book page
        textbook_equation_number=None,
    ),
)
register_equation(michaelis_menten)


__all__ = ["michaelis_menten"]


# --- coverage pass additions (Feher extraction) ---

import math


def compute_arrhenius_equation(A, E_a, T=310.0, R=8.314):
    """Arrhenius equation (Feher 1.5, Eq. 1.5.14): temperature dependence of a
    chemical reaction rate constant. k = A * exp(-E_a / (R * T)).

    Units: A in the same units as k (e.g. s^-1 for a first-order reaction),
    E_a in J/mol, T in K, R in J/(mol*K). Returns k in the same units as A.
    A larger E_a lowers k; higher T raises k.
    """
    return A * math.exp(-E_a / (R * T))

arrhenius_equation = create_equation(
    id='arrhenius_equation',
    output_units='1/s',
    name='Arrhenius Equation',
    category=EquationCategory.FOUNDATIONS,
    latex='k = A\\,e^{-\\frac{E_a}{RT}}',
    simplified='k = A * exp(-E_a / (R * T))',
    description='Arrhenius equation: the temperature dependence of a chemical reaction rate constant. The rate constant k increases with absolute temperature T and decreases with activation energy E_a; A is a temperature-independent pre-exponential (orientation/frequency) factor and R is the gas constant. Underlies the temperature sensitivity of enzyme-catalysed reactions, Q10 effects on metabolic rate, and the impact of hypothermia and fever on reaction kinetics. Feher develops it in Unit 1 Section 1.5 as a named standalone relation (Eq. 1.5.14), restated in Appendix 1.5.A1.',
    compute_func=compute_arrhenius_equation,
    parameters=[
        Parameter(name='A', description='Pre-exponential (frequency/orientation) factor; temperature-independent, carried in the same units as the rate constant k', units='s^-1', symbol='A', physiological_range=(1000000, 1000000000000000000)),
        Parameter(name='E_a', description='Activation energy — energy barrier that must be supplied to reach the activated complex', units='J/mol', symbol='E_a', physiological_range=(0, 300000)),
        Parameter(name='T', description='Absolute temperature (defaults to body temperature 310 K)', units='K', symbol='T', default_value=310, physiological_range=(273, 323)),
        Parameter(name='R', description='Universal gas constant', units='J/(mol*K)', symbol='R', default_value=8.314),
    ],
    depends_on=[],
    produces='k',
    metadata=EquationMetadata(source_unit=1, source_chapter='1.5',
                              source_section='RATES OF CHEMICAL REACTIONS DEPEND ON THE ACTIVATION ENERGY', page_reference=None,
                              textbook_equation_number='1.5.14'),
)
register_equation(arrhenius_equation)

try:
    __all__ += ['arrhenius_equation']
except NameError:
    __all__ = ['arrhenius_equation']


# --- clinical additions (CICM, beyond Feher) ---

def compute_first_order_elimination(C0, ke, t):
    """C(t) = C0*exp(-ke*t): plasma concentration decay under first-order (linear) kinetics."""
    return C0 * math.exp(-ke * t)

first_order_elimination = create_equation(
    id='first_order_elimination',
    output_units='mg/L',
    name='First-Order Drug Elimination',
    category=EquationCategory.FOUNDATIONS,
    latex='C(t) = C_0 e^{-k_e t}',
    simplified='C_t = C0*exp(-ke*t)',
    description='First-order (concentration-independent) drug elimination: plasma level falls exponentially with elimination rate constant ke. Underlies half-life, steady state, and offset of most drugs.',
    compute_func=compute_first_order_elimination,
    parameters=[
        Parameter(name='C0', description='Initial concentration', units='mg/L', symbol='C_0', physiological_range=(0.1, 1000)),
        Parameter(name='ke', description='Elimination rate constant', units='1/h', symbol='k_e', physiological_range=(0.01, 5)),
        Parameter(name='t', description='Time', units='h', symbol='t', physiological_range=(0, 48)),
    ],
    depends_on=["elimination_rate_constant"],   # ke supplied by elimination_rate_constant (produces 'ke')
    produces='C_t',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(first_order_elimination)


def compute_elimination_rate_constant(CL, Vd):
    """ke = CL/Vd (1/time): the fraction of Vd cleared per unit time."""
    return CL / Vd

elimination_rate_constant = create_equation(
    id='elimination_rate_constant',
    output_units='1/h',
    name='Elimination Rate Constant',
    category=EquationCategory.FOUNDATIONS,
    latex='k_e = \\frac{CL}{V_d}',
    simplified='ke = CL/Vd',
    description='Elimination rate constant linking clearance and volume of distribution; determines half-life (t1/2 = 0.693/ke) and the exponent of first-order decay.',
    compute_func=compute_elimination_rate_constant,
    parameters=[
        Parameter(name='CL', description='Clearance', units='L/h', symbol='CL', physiological_range=(0.1, 100)),
        Parameter(name='Vd', description='Volume of distribution', units='L', symbol='V_d', physiological_range=(1, 1000)),
    ],
    depends_on=[],
    produces='ke',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(elimination_rate_constant)


def compute_loading_dose(Vd, C_target):
    """Loading dose = Vd*C_target (bioavailability F=1 assumed). Fills the volume of distribution to target."""
    return Vd * C_target

loading_dose = create_equation(
    id='loading_dose',
    output_units='mg',
    name='Loading Dose',
    category=EquationCategory.FOUNDATIONS,
    latex='LD = V_d \\times C_{target}',
    simplified='LD = Vd*C_target',
    description='Loading dose to immediately achieve a target plasma concentration; depends only on the volume of distribution, not clearance.',
    compute_func=compute_loading_dose,
    parameters=[
        Parameter(name='Vd', description='Volume of distribution', units='L', symbol='V_d', physiological_range=(1, 1000)),
        Parameter(name='C_target', description='Target plasma concentration', units='mg/L', symbol='C_t', physiological_range=(0.1, 500)),
    ],
    depends_on=["first_order_elimination"],
    produces='LD',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(loading_dose)


def compute_maintenance_infusion_rate(CL, C_ss):
    """Maintenance rate = CL*C_ss: infusion rate to hold a target steady-state concentration (F=1)."""
    return CL * C_ss

maintenance_infusion_rate = create_equation(
    id='maintenance_infusion_rate',
    output_units='mg/h',
    name='Maintenance Infusion Rate',
    category=EquationCategory.FOUNDATIONS,
    latex='R = CL \\times C_{ss}',
    simplified='rate = CL*C_ss',
    description='Maintenance infusion (or dosing) rate needed to sustain a target steady-state concentration; balances drug in against clearance.',
    compute_func=compute_maintenance_infusion_rate,
    parameters=[
        Parameter(name='CL', description='Clearance', units='L/h', symbol='CL', physiological_range=(0.1, 100)),
        Parameter(name='C_ss', description='Target steady-state concentration', units='mg/L', symbol='C_ss', physiological_range=(0.1, 500)),
    ],
    depends_on=[],
    produces='MD_rate',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(maintenance_infusion_rate)

try:
    __all__ += ['first_order_elimination', 'elimination_rate_constant', 'loading_dose', 'maintenance_infusion_rate']
except NameError:
    __all__ = ['first_order_elimination', 'elimination_rate_constant', 'loading_dose', 'maintenance_infusion_rate']


# --- review-add 2026-07-15 ---
def compute_bioavailability_auc(AUC_oral: float, AUC_iv: float,
                                dose_oral: float = 1.0, dose_iv: float = 1.0) -> float:
    """Absolute bioavailability F = (AUC_oral/AUC_iv) * (dose_iv/dose_oral).

    Dose-normalised ratio of oral to IV exposure."""
    return (AUC_oral / AUC_iv) * (dose_iv / dose_oral)

bioavailability_auc_equation = create_equation(
    id='bioavailability_auc',
    name='Absolute Bioavailability (AUC)',
    category=EquationCategory.FOUNDATIONS,
    latex=r'F = \\frac{AUC_{oral}}{AUC_{iv}}\\cdot\\frac{D_{iv}}{D_{oral}}',
    simplified='F = (AUC_oral/AUC_iv) * (dose_iv/dose_oral)',
    description='Absolute oral bioavailability: dose-normalised ratio of oral to IV area-under-curve. Scales loading and maintenance dosing.',
    compute_func=compute_bioavailability_auc,
    output_units='dimensionless',
    parameters=[
        Parameter(name='AUC_oral', description='Oral AUC', units='mg*h/L', symbol='AUC_po', physiological_range=(0.0, 1000.0)),
        Parameter(name='AUC_iv', description='IV AUC', units='mg*h/L', symbol='AUC_iv', physiological_range=(0.1, 1000.0)),
        Parameter(name='dose_oral', description='Oral dose', units='mg', symbol='D_po', physiological_range=(0.1, 5000.0)),
        Parameter(name='dose_iv', description='IV dose', units='mg', symbol='D_iv', physiological_range=(0.1, 5000.0)),
    ],
    metadata=EquationMetadata(source_unit=1, source_chapter='1.7'),
)
register_equation(bioavailability_auc_equation)


# --- review-add 2026-07-15 ---
def compute_average_steady_state_concentration(F: float, Dose: float,
                                               CL: float, tau: float) -> float:
    """Average steady-state concentration for repeated dosing,
    Css_avg = F*Dose/(CL*tau)."""
    return (F * Dose) / (CL * tau)

average_steady_state_concentration_equation = create_equation(
    id='average_steady_state_concentration',
    name='Average Steady-State Concentration',
    category=EquationCategory.FOUNDATIONS,
    latex=r'C_{ss,avg} = \\frac{F \\cdot Dose}{CL \\cdot \\tau}',
    simplified='Css_avg = (F * Dose) / (CL * tau)',
    description='Average plasma concentration over a dosing interval at steady state (discrete counterpart of the continuous maintenance infusion).',
    compute_func=compute_average_steady_state_concentration,
    output_units='mg/L',
    parameters=[
        Parameter(name='F', description='Bioavailability', units='dimensionless', symbol='F', physiological_range=(0.0, 1.0)),
        Parameter(name='Dose', description='Dose per interval', units='mg', symbol='Dose', physiological_range=(1.0, 5000.0)),
        Parameter(name='CL', description='Clearance', units='L/h', symbol='CL', physiological_range=(0.1, 100.0)),
        Parameter(name='tau', description='Dosing interval', units='h', symbol='tau', physiological_range=(1.0, 48.0)),
    ],
    metadata=EquationMetadata(source_unit=1, source_chapter='1.7'),
)
register_equation(average_steady_state_concentration_equation)


# --- backlog-complete-add 2026-07-15 ---
def compute_apparent_volume_of_distribution(Dose: float, C0: float) -> float:
    """Apparent (PK) volume of distribution Vd = Dose / C0 (may exceed body volume)."""
    return Dose / C0

apparent_volume_of_distribution_equation = create_equation(
    id="apparent_volume_of_distribution", name="Apparent Volume of Distribution",
    category=EquationCategory.FOUNDATIONS,
    latex=r"V_d = \frac{Dose}{C_0}", simplified="Vd = Dose / C0",
    description="Pharmacokinetic apparent volume of distribution: a proportionality constant (Dose/C0) that, unlike a real dilution volume, may exceed total body water (e.g. digoxin ~500 L).",
    compute_func=compute_apparent_volume_of_distribution, output_units="L",
    parameters=[Parameter(name="Dose", description="Dose administered", units="mg", symbol="Dose", physiological_range=(1, 5000)),
                Parameter(name="C0", description="Extrapolated initial concentration", units="mg/L", symbol="C0", physiological_range=(0.01, 100))],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.7"),
)
register_equation(apparent_volume_of_distribution_equation)

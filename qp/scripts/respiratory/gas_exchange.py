"""Gas exchange equations."""

"""Alveolar-arterial O2 Gradient equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_aa_gradient(P_AO2: float, P_aO2: float) -> float:
    """
    Calculate alveolar-arterial oxygen gradient.

    A-a gradient = P_AO2 - P_aO2

    Parameters
    ----------
    P_AO2 : float
        Alveolar PO2 (mmHg)
    P_aO2 : float
        Arterial PO2 (mmHg)

    Returns
    -------
    float
        A-a gradient (mmHg)
    """
    return P_AO2 - P_aO2


# Create equation
aa_gradient = create_equation(
    id="aa_gradient",
    output_units='mmHg',
    name="Alveolar-Arterial O2 Gradient",
    category=EquationCategory.RESPIRATORY,
    latex=r"A-a \text{ gradient} = P_{AO2} - P_{aO2}",
    simplified="A-a gradient = P_AO2 - P_aO2",
    description="Difference between alveolar and arterial PO2, indicates gas exchange efficiency",
    compute_func=compute_aa_gradient,
    parameters=[
        Parameter(
            name="P_AO2",
            description="Alveolar PO2",
            units="mmHg",
            symbol="P_{AO2}",
            default_value=100.0,
            physiological_range=(50.0, 150.0)
        ),
        Parameter(
            name="P_aO2",
            description="Arterial PO2",
            units="mmHg",
            symbol="P_{aO2}",
            default_value=95.0,
            physiological_range=(40.0, 100.0)
        )
    ],
    depends_on=["alveolar_gas_equation"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(aa_gradient)

"""Alveolar Gas Equation."""


def compute_alveolar_gas_equation(P_iO2: float, P_ACO2: float, RQ: float) -> float:
    """
    Calculate alveolar PO2 (simplified form).

    P_AO2 = P_iO2 - P_ACO2/RQ

    Parameters
    ----------
    P_iO2 : float
        Inspired PO2 (mmHg)
    P_ACO2 : float
        Alveolar PCO2 (mmHg)
    RQ : float
        Respiratory quotient/exchange ratio (dimensionless, VCO2/VO2)

    Returns
    -------
    float
        Alveolar PO2 (mmHg)
    """
    return P_iO2 - (P_ACO2 / RQ)


# Create equation
alveolar_gas_equation = create_equation(
    id="alveolar_gas_equation",
    produces='P_AO2',
    output_units='mmHg',
    name="Alveolar Gas Equation",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{AO2} = P_{iO2} - \frac{P_{ACO2}}{R}",
    simplified="P_AO2 = P_iO2 - P_ACO2/R",
    description="Calculate alveolar oxygen partial pressure from inspired air and CO2",
    compute_func=compute_alveolar_gas_equation,
    parameters=[
        Parameter(
            name="P_iO2",
            description="Inspired PO2",
            units="mmHg",
            symbol="P_{iO2}",
            default_value=150.0,
            physiological_range=(50.0, 700.0)
        ),
        Parameter(
            name="P_ACO2",
            description="Alveolar PCO2",
            units="mmHg",
            symbol="P_{ACO2}",
            default_value=40.0,
            physiological_range=(20.0, 80.0)
        ),
        Parameter(
            name="RQ",
            description="Respiratory quotient/exchange ratio (VCO2/VO2)",
            units="dimensionless",
            symbol="R",
            default_value=0.8,
            physiological_range=(0.7, 1.0)
        )
    ],
    depends_on=["inspired_po2", "alveolar_pco2_equation"],   # P_ACO2 from alveolar_pco2_equation (produces 'P_ACO2')
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(alveolar_gas_equation)

"""Diffusing Capacity equation."""


def compute_diffusing_capacity(V_gas: float, P_A: float, P_c: float) -> float:
    """
    Calculate diffusing capacity of the lung.

    D_L = V̇_gas / (P_A - P_c)

    Parameters
    ----------
    V_gas : float
        Gas transfer rate (mL/min)
    P_A : float
        Alveolar partial pressure (mmHg)
    P_c : float
        Capillary partial pressure (mmHg)

    Returns
    -------
    float
        Diffusing capacity (mL/(min·mmHg))
    """
    return V_gas / (P_A - P_c)


# Create equation
diffusing_capacity = create_equation(
    id="diffusing_capacity",
    output_units='mL/(min*mmHg)',
    name="Diffusing Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"D_L = \frac{\dot{V}_{gas}}{P_A - P_c}",
    simplified="D_L = V̇_gas / (P_A - P_c)",
    description="Measure of gas transfer efficiency across alveolar-capillary membrane",
    compute_func=compute_diffusing_capacity,
    parameters=[
        Parameter(
            name="V_gas",
            description="Gas transfer rate",
            units="mL/min",
            symbol=r"\dot{V}_{gas}",
            physiological_range=(1.0, 500.0)
        ),
        Parameter(
            name="P_A",
            description="Alveolar partial pressure",
            units="mmHg",
            symbol="P_A",
            physiological_range=(0.0, 150.0)
        ),
        Parameter(
            name="P_c",
            description="Capillary partial pressure",
            units="mmHg",
            symbol="P_c",
            physiological_range=(0.0, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(diffusing_capacity)

"""Diffusion Conductance Model equation."""


def compute_diffusion_conductance(D_M: float, theta: float, V_c: float) -> float:
    """
    Calculate total diffusing capacity from conductance model.

    1/D_L = 1/D_M + 1/(θ × V_c)

    Parameters
    ----------
    D_M : float
        Membrane diffusing capacity (mL/(min·mmHg))
    theta : float
        Reaction rate of gas with Hb (mL/(min·mmHg·mL))
    V_c : float
        Pulmonary capillary blood volume (mL)

    Returns
    -------
    float
        Total diffusing capacity (mL/(min·mmHg))
    """
    return 1.0 / (1.0/D_M + 1.0/(theta * V_c))


# Create equation
diffusion_conductance = create_equation(
    id="diffusion_conductance",
    output_units='mL/(min*mmHg)',
    name="Diffusion Conductance Model",
    category=EquationCategory.RESPIRATORY,
    latex=r"\frac{1}{D_L} = \frac{1}{D_M} + \frac{1}{\theta \times V_c}",
    simplified="1/D_L = 1/D_M + 1/(θ × V_c)",
    description="Resistance model combining membrane diffusion and chemical reaction rates",
    compute_func=compute_diffusion_conductance,
    parameters=[
        Parameter(
            name="D_M",
            description="Membrane diffusing capacity",
            units="mL/(min·mmHg)",
            symbol="D_M",
            physiological_range=(20.0, 100.0)
        ),
        Parameter(
            name="theta",
            description="Reaction rate with Hb",
            units="mL/(min·mmHg·mL)",
            symbol=r"\theta",
            physiological_range=(0.001, 0.01)
        ),
        Parameter(
            name="V_c",
            description="Capillary blood volume",
            units="mL",
            symbol="V_c",
            default_value=70.0,
            physiological_range=(50.0, 150.0)
        )
    ],
    depends_on=["diffusing_capacity"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(diffusion_conductance)

"""DLCO to DLO2 Conversion equation."""


def compute_dlco_to_dlo2(D_LCO: float) -> float:
    """
    Convert CO diffusing capacity to O2 diffusing capacity.

    D_LO2 ≈ 1.23 × D_LCO

    Parameters
    ----------
    D_LCO : float
        CO diffusing capacity (mL/(min·mmHg))

    Returns
    -------
    float
        O2 diffusing capacity (mL/(min·mmHg))
    """
    return 1.23 * D_LCO


# Create equation
dlco_to_dlo2 = create_equation(
    id="dlco_to_dlo2",
    output_units='mL/(min*mmHg)',
    name="DLCO to DLO2 Conversion",
    category=EquationCategory.RESPIRATORY,
    latex=r"D_{LO2} \approx 1.23 \times D_{LCO}",
    simplified="D_LO2 ≈ 1.23 × D_LCO",
    description="Convert carbon monoxide diffusing capacity to oxygen diffusing capacity",
    compute_func=compute_dlco_to_dlo2,
    parameters=[
        Parameter(
            name="D_LCO",
            description="CO diffusing capacity",
            units="mL/(min·mmHg)",
            symbol="D_{LCO}",
            default_value=25.0,
            physiological_range=(15.0, 40.0)
        )
    ],
    depends_on=["diffusing_capacity"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(dlco_to_dlo2)

"""Inspired PO2 equation."""


def compute_inspired_po2(FiO2: float, P_B: float, P_H2O: float) -> float:
    """
    Calculate inspired PO2 (humidified air).

    P_iO2 = FiO2 × (P_B - P_H2O)

    Parameters
    ----------
    FiO2 : float
        Fraction of inspired oxygen (0-1)
    P_B : float
        Barometric pressure (mmHg)
    P_H2O : float
        Water vapor pressure (mmHg)

    Returns
    -------
    float
        Inspired PO2 (mmHg)
    """
    return FiO2 * (P_B - P_H2O)


# Create equation
inspired_po2 = create_equation(
    id="inspired_po2",
    produces='P_iO2',
    output_units='mmHg',
    name="Inspired PO2",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{iO2} = FiO_2 \times (P_B - P_{H_2O})",
    simplified="P_iO2 = FiO2 × (P_B - P_H2O)",
    description="Partial pressure of oxygen in humidified inspired air",
    compute_func=compute_inspired_po2,
    parameters=[
        Parameter(
            name="FiO2",
            description="Fraction of inspired oxygen",
            units="dimensionless",
            symbol="FiO_2",
            default_value=0.21,
            physiological_range=(0.21, 1.0)
        ),
        Parameter(
            name="P_B",
            description="Barometric pressure",
            units="mmHg",
            symbol="P_B",
            default_value=760.0,
            physiological_range=(200.0, 800.0)
        ),
        Parameter(
            name="P_H2O",
            description="Water vapor pressure at 37°C",
            units="mmHg",
            symbol="P_{H_2O}",
            default_value=47.0,
            physiological_range=(47.0, 47.0)
        )
    ],
    depends_on=["partial_pressure"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(inspired_po2)

"""Partial Pressure (Dalton's Law) equation."""


def compute_partial_pressure(F_i: float, P_total: float) -> float:
    """
    Calculate partial pressure using Dalton's Law.

    P_i = F_i × P_total

    Parameters
    ----------
    F_i : float
        Fraction of gas i (0-1)
    P_total : float
        Total pressure (mmHg)

    Returns
    -------
    float
        Partial pressure of gas i (mmHg)
    """
    return F_i * P_total


# Create equation
partial_pressure = create_equation(
    id="partial_pressure",
    output_units='mmHg',
    name="Dalton's Law of Partial Pressures",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_i = F_i \times P_{total}",
    simplified="P_i = F_i × P_total",
    description="Partial pressure of a gas in a mixture equals its fraction times total pressure",
    compute_func=compute_partial_pressure,
    parameters=[
        Parameter(
            name="F_i",
            description="Fraction of gas i",
            units="dimensionless",
            symbol="F_i",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="P_total",
            description="Total pressure",
            units="mmHg",
            symbol="P_{total}",
            default_value=760.0,
            physiological_range=(200.0, 800.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.3"
    )
)

# Register in global index
register_equation(partial_pressure)

__all__ = ['partial_pressure', 'inspired_po2', 'alveolar_gas_equation', 'aa_gradient', 'diffusing_capacity', 'dlco_to_dlo2', 'diffusion_conductance']


# --- coverage pass additions (Feher extraction) ---

def compute_alveolar_pco2_equation(Q_CO2, Q_A, P_B=760.0, P_H2O=47.0):
    """Alveolar CO2 partial pressure from CO2 production and alveolar ventilation.

    P_ACO2 = (Q_CO2 / Q_A) * (P_B - P_H2O)   [Feher 6.3, the alveolar ventilation
    equation rearranged to solve for P_ACO2]. Q_CO2 and Q_A are STPD volume flows
    in mL/min (any consistent volume-rate unit works, since only their ratio
    matters); P_B, P_H2O and the returned P_ACO2 are in mmHg.
    """
    return (Q_CO2 / Q_A) * (P_B - P_H2O)

alveolar_pco2_equation = create_equation(
    id='alveolar_pco2_equation',
    output_units='mmHg',
    name='Alveolar CO2 Partial Pressure (Alveolar Ventilation Equation)',
    category=EquationCategory.RESPIRATORY,
    latex='P_{A_{CO_2}} = \\dfrac{\\dot{Q}_{CO_2}}{\\dot{Q}_A}\\,(P_B - P_{H_2O})',
    simplified='P_ACO2 = (Q_CO2 / Q_A) * (P_B - P_H2O)',
    description="Alveolar (and, at equilibrium, arterial) CO2 partial pressure, obtained by rearranging Feher's alveolar ventilation equation. At steady state the metabolic rate of CO2 production equals pulmonary CO2 elimination, so P_ACO2 is fixed by the ratio of CO2 production to alveolar ventilation scaled by the dry-gas pressure (P_B - P_H2O). It expresses the inverse relationship between alveolar ventilation and PACO2 at a constant metabolic rate (about 40 mmHg at rest); all flows are STPD volumes. Produces the P_ACO2 that feeds the alveolar gas equation.",
    compute_func=compute_alveolar_pco2_equation,
    parameters=[
        Parameter(name='Q_CO2', description='Rate of CO2 production by the body (= steady-state CO2 elimination via the lungs), STPD', units='mL/min', symbol='\\dot{Q}_{CO_2}', default_value=200, physiological_range=(50, 4000)),
        Parameter(name='Q_A', description='Alveolar ventilation (volume flow of alveolar gas that exchanges with blood), STPD', units='mL/min', symbol='\\dot{Q}_A', default_value=3570, physiological_range=(1000, 150000)),
        Parameter(name='P_B', description='Barometric (total) pressure', units='mmHg', symbol='P_B', default_value=760, physiological_range=(200, 800)),
        Parameter(name='P_H2O', description='Saturated water vapor pressure at body temperature (37 C)', units='mmHg', symbol='P_{H_2O}', default_value=47, physiological_range=(47, 47)),
    ],
    depends_on=[],
    produces='P_ACO2',
    metadata=EquationMetadata(source_unit=6, source_chapter='6.3',
                              source_section='THE RATE OF CO2 PRODUCTION ALLOWS CALCULATION OF ALVEOLAR VENTILATION', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(alveolar_pco2_equation)

try:
    __all__ += ['alveolar_pco2_equation']
except NameError:
    __all__ = ['alveolar_pco2_equation']


# --- clinical additions (CICM, beyond Feher) ---

def compute_pf_ratio(PaO2, FiO2):
    """P/F ratio = PaO2 (mmHg) / FiO2 (fraction). ARDS severity marker (Berlin: <300 mild, <200 mod, <100 severe)."""
    return PaO2 / FiO2

pf_ratio = create_equation(
    id='pf_ratio',
    output_units='mmHg',
    name='PaO2/FiO2 Ratio',
    category=EquationCategory.RESPIRATORY,
    latex='P/F = \\frac{PaO_2}{FiO_2}',
    simplified='PF = PaO2 / FiO2',
    description='Ratio of arterial oxygen tension to inspired oxygen fraction; the Berlin ARDS oxygenation criterion (<300 mild, <200 moderate, <100 severe on PEEP >=5).',
    compute_func=compute_pf_ratio,
    parameters=[
        Parameter(name='PaO2', description='Arterial oxygen tension', units='mmHg', symbol='P_aO2', physiological_range=(40, 600)),
        Parameter(name='FiO2', description='Inspired oxygen fraction', units='dimensionless', symbol='F_iO2', physiological_range=(0.21, 1.0)),
    ],
    depends_on=[],
    produces='PF',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(pf_ratio)

try:
    __all__ += ['pf_ratio']
except NameError:
    __all__ = ['pf_ratio']


# --- adversarial-review-add 2026-07-15 ---
def compute_oxygenation_index(FiO2: float, MAP: float, PaO2: float) -> float:
    """Oxygenation index OI = FiO2 x MAP x 100 / PaO2 (FiO2 as fraction, MAP mean
    airway pressure cmH2O, PaO2 mmHg). ICU severity of hypoxaemic failure."""
    return (FiO2 * MAP * 100.0) / PaO2

oxygenation_index_equation = create_equation(
    id="oxygenation_index",
    name="Oxygenation Index",
    category=EquationCategory.RESPIRATORY,
    latex=r"OI = \frac{FiO_2 \times \bar{P}_{aw} \times 100}{PaO_2}",
    simplified="OI = FiO2 * MAP * 100 / PaO2",
    description="Oxygenation index: severity of hypoxaemic respiratory failure "
                "incorporating mean airway pressure; >40 is a classic ECMO trigger. "
                "FiO2 as fraction, MAP in cmH2O, PaO2 in mmHg.",
    compute_func=compute_oxygenation_index,
    output_units="dimensionless",
    parameters=[
        Parameter(name="FiO2", description="Inspired oxygen fraction", units="dimensionless", symbol="FiO2", physiological_range=(0.21, 1.0)),
        Parameter(name="MAP", description="Mean airway pressure", units="cmH2O", symbol="MAP_aw", physiological_range=(5, 40)),
        Parameter(name="PaO2", description="Arterial oxygen tension", units="mmHg", symbol="PaO2", physiological_range=(30, 500)),
    ],
    metadata=EquationMetadata(source_unit=6, source_chapter="6.6"),
)
register_equation(oxygenation_index_equation)


# --- backlog-complete-add 2026-07-15 ---
def compute_aa_gradient_age_limit(age: float) -> float:
    """Age-corrected upper limit of normal A-a gradient: (age/4) + 4 (mmHg)."""
    return age / 4.0 + 4.0

aa_gradient_age_limit_equation = create_equation(
    id="aa_gradient_age_limit", name="Age-Corrected A-a Gradient Upper Limit",
    category=EquationCategory.RESPIRATORY,
    latex=r"A\text{-}a_{ULN} = \frac{age}{4} + 4", simplified="AaULN = age/4 + 4",
    description="Upper limit of normal alveolar-arterial O2 gradient corrected for age (mmHg on room air).",
    compute_func=compute_aa_gradient_age_limit, output_units="mmHg",
    parameters=[Parameter(name="age", description="Age", units="years", symbol="age", physiological_range=(18, 100))],
    metadata=EquationMetadata(source_unit=6, source_chapter="6.6"),
)
register_equation(aa_gradient_age_limit_equation)


# --- backlog-complete-add 2026-07-15 ---
def compute_p50_bohr_ph(pH: float, P50_std: float = 26.8) -> float:
    """Bohr pH shift of P50: P50 = P50_std * 10^(-0.48*(pH - 7.4)) (mmHg).

    Acidosis (low pH) right-shifts the ODC (raises P50)."""
    return P50_std * 10.0 ** (-0.48 * (pH - 7.4))

p50_bohr_ph_equation = create_equation(
    id="p50_bohr_ph", name="P50 Bohr pH Correction",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{50} = P_{50}^{std}\cdot 10^{-0.48(pH - 7.4)}", simplified="P50 = P50_std * 10**(-0.48*(pH-7.4))",
    description="Bohr-effect shift of P50 with pH (Severinghaus pH term): acidosis right-shifts the oxyhaemoglobin dissociation curve. Feeds hill_saturation's P_50.",
    compute_func=compute_p50_bohr_ph, output_units="mmHg",
    parameters=[Parameter(name="pH", description="Arterial pH", units="dimensionless", symbol="pH", physiological_range=(6.8, 7.8)),
                Parameter(name="P50_std", description="Standard P50 at pH 7.4", units="mmHg", symbol="P50_std", physiological_range=(24, 30))],
    metadata=EquationMetadata(source_unit=6, source_chapter="6.6"),
)
register_equation(p50_bohr_ph_equation)

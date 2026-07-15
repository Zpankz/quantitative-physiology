"""Oxygen transport equations."""

"""Hill Equation for O2-Hb Dissociation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_hill_equation(PO2: float, P50: float, n: float) -> float:
    """
    Calculate oxygen saturation using Hill equation.

    S_O2 = P_O2^n / (P_50^n + P_O2^n)

    Parameters
    ----------
    PO2 : float
        Partial pressure of oxygen (mmHg)
    P50 : float
        PO2 at 50% saturation (mmHg)
    n : float
        Hill coefficient (cooperativity)

    Returns
    -------
    float
        Oxygen saturation (0-1)
    """
    return PO2**n / (P50**n + PO2**n)


# Create equation
hill_equation = create_equation(
    id="hill_equation",
    output_units='dimensionless',
    name="Hill Equation (O2-Hb Dissociation)",
    category=EquationCategory.RESPIRATORY,
    latex=r"S_{O2} = \frac{P_{O2}^n}{P_{50}^n + P_{O2}^n}",
    simplified="S_O2 = P_O2^n / (P_50^n + P_O2^n)",
    description="Oxygen-hemoglobin dissociation curve with cooperative binding",
    compute_func=compute_hill_equation,
    parameters=[
        Parameter(
            name="PO2",
            description="Partial pressure of oxygen",
            units="mmHg",
            symbol="P_{O2}",
            physiological_range=(0.0, 150.0)
        ),
        Parameter(
            name="P50",
            description="PO2 at 50% saturation",
            units="mmHg",
            symbol="P_{50}",
            default_value=26.6,
            physiological_range=(20.0, 35.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=2.7,
            physiological_range=(2.0, 3.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(hill_equation)

"""Oxygen Consumption (Fick Principle) equation."""


def compute_oxygen_consumption_fick(Q: float, CaO2: float, CvO2: float) -> float:
    """
    Calculate oxygen consumption using Fick principle.

    V̇O2 = Q̇ × (C_aO2 - C_vO2) × 10

    Parameters
    ----------
    Q : float
        Cardiac output (L/min)
    CaO2 : float
        Arterial O2 content (mL O2/dL)
    CvO2 : float
        Venous O2 content (mL O2/dL)

    Returns
    -------
    float
        Oxygen consumption (mL O2/min)
    """
    return Q * (CaO2 - CvO2) * 10.0


# Create equation
oxygen_consumption_fick = create_equation(
    id="oxygen_consumption_fick",
    output_units='mL/min',
    name="Oxygen Consumption (Fick Principle)",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V}O_2 = \dot{Q} \times (C_{aO2} - C_{vO2}) \times 10",
    simplified="V̇O2 = Q̇ × (C_aO2 - C_vO2) × 10",
    description="Tissue oxygen consumption based on arteriovenous O2 difference",
    compute_func=compute_oxygen_consumption_fick,
    parameters=[
        Parameter(
            name="Q",
            description="Cardiac output",
            units="L/min",
            symbol=r"\dot{Q}",
            default_value=5.0,
            physiological_range=(3.0, 25.0)
        ),
        Parameter(
            name="CaO2",
            description="Arterial O2 content",
            units="mL O2/dL",
            symbol="C_{aO2}",
            default_value=20.0,
            physiological_range=(10.0, 23.0)
        ),
        Parameter(
            name="CvO2",
            description="Venous O2 content",
            units="mL O2/dL",
            symbol="C_{vO2}",
            default_value=15.0,
            physiological_range=(8.0, 18.0)
        )
    ],
    depends_on=["respiratory_oxygen_content", "mixed_venous_oxygen_content"],  # C_aO2, C_vO2
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(oxygen_consumption_fick)

"""Oxygen Content equation."""


def compute_oxygen_content(Hb: float, SO2: float, PO2: float) -> float:
    """
    Calculate total oxygen content in blood.

    C_O2 = (1.34 × [Hb] × S_O2) + (0.003 × P_O2)

    Parameters
    ----------
    Hb : float
        Hemoglobin concentration (g/dL)
    SO2 : float
        Oxygen saturation (0-1)
    PO2 : float
        Partial pressure of oxygen (mmHg)

    Returns
    -------
    float
        Total O2 content (mL O2/dL)
    """
    return (1.34 * Hb * SO2) + (0.003 * PO2)


# Create equation
oxygen_content = create_equation(
    id="respiratory_oxygen_content",
    produces='CaO2',
    output_units='mL/dL',
    name="Oxygen Content (Respiratory)",
    category=EquationCategory.RESPIRATORY,
    latex=r"C_{O2} = (1.34 \times [Hb] \times S_{O2}) + (0.003 \times P_{O2})",
    simplified="C_O2 = (1.34 × [Hb] × S_O2) + (0.003 × P_O2)",
    description="Total oxygen content: bound to hemoglobin plus dissolved",
    compute_func=compute_oxygen_content,
    parameters=[
        Parameter(
            name="Hb",
            description="Hemoglobin concentration",
            units="g/dL",
            symbol="[Hb]",
            default_value=15.0,
            physiological_range=(10.0, 18.0)
        ),
        Parameter(
            name="SO2",
            description="Oxygen saturation",
            units="dimensionless",
            symbol="S_{O2}",
            default_value=0.97,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="PO2",
            description="Partial pressure of oxygen",
            units="mmHg",
            symbol="P_{O2}",
            default_value=100.0,
            physiological_range=(20.0, 600.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(oxygen_content)

"""Oxygen Delivery equation."""


def compute_oxygen_delivery(Q: float, CaO2: float) -> float:
    """
    Calculate oxygen delivery to tissues.

    D_O2 = Q̇ × C_aO2 × 10

    Parameters
    ----------
    Q : float
        Cardiac output (L/min)
    CaO2 : float
        Arterial O2 content (mL O2/dL)

    Returns
    -------
    float
        Oxygen delivery (mL O2/min)
    """
    return Q * CaO2 * 10.0


# Create equation
oxygen_delivery = create_equation(
    id="tissue_oxygen_delivery",
    output_units='mL/min',
    name="Tissue Oxygen Delivery (Respiratory)",
    category=EquationCategory.RESPIRATORY,
    latex=r"D_{O2} = \dot{Q} \times C_{aO2} \times 10",
    simplified="D_O2 = Q̇ × C_aO2 × 10",
    description="Total oxygen delivery to tissues per minute",
    compute_func=compute_oxygen_delivery,
    parameters=[
        Parameter(
            name="Q",
            description="Cardiac output",
            units="L/min",
            symbol=r"\dot{Q}",
            default_value=5.0,
            physiological_range=(3.0, 25.0)
        ),
        Parameter(
            name="CaO2",
            description="Arterial O2 content",
            units="mL O2/dL",
            symbol="C_{aO2}",
            default_value=20.0,
            physiological_range=(10.0, 23.0)
        )
    ],
    depends_on=["respiratory_oxygen_content"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(oxygen_delivery)

"""Oxygen Extraction Ratio equation."""


def compute_oxygen_extraction_ratio(CaO2: float, CvO2: float) -> float:
    """
    Calculate oxygen extraction ratio.

    O2ER = (C_aO2 - C_vO2) / C_aO2

    Parameters
    ----------
    CaO2 : float
        Arterial O2 content (mL O2/dL)
    CvO2 : float
        Venous O2 content (mL O2/dL)

    Returns
    -------
    float
        O2 extraction ratio (dimensionless, 0-1)
    """
    return (CaO2 - CvO2) / CaO2


# Create equation
oxygen_extraction_ratio = create_equation(
    id="oxygen_extraction_ratio",
    output_units='dimensionless',
    name="Oxygen Extraction Ratio",
    category=EquationCategory.RESPIRATORY,
    latex=r"O_2ER = \frac{C_{aO2} - C_{vO2}}{C_{aO2}}",
    simplified="O2ER = (C_aO2 - C_vO2) / C_aO2",
    description="Fraction of delivered oxygen extracted by tissues",
    compute_func=compute_oxygen_extraction_ratio,
    parameters=[
        Parameter(
            name="CaO2",
            description="Arterial O2 content",
            units="mL O2/dL",
            symbol="C_{aO2}",
            default_value=20.0,
            physiological_range=(10.0, 23.0)
        ),
        Parameter(
            name="CvO2",
            description="Venous O2 content",
            units="mL O2/dL",
            symbol="C_{vO2}",
            default_value=15.0,
            physiological_range=(8.0, 18.0)
        )
    ],
    depends_on=["respiratory_oxygen_content", "mixed_venous_oxygen_content"],  # C_aO2, C_vO2
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.5"
    )
)

# Register in global index
register_equation(oxygen_extraction_ratio)

__all__ = ['oxygen_content', 'hill_equation', 'oxygen_delivery', 'oxygen_consumption_fick', 'oxygen_extraction_ratio']


# --- coverage pass additions (Feher extraction) ---

def compute_oxygen_consumption_gas_exchange(Q_T_star, fIO2, Q_T, fEO2):
    """VO2 from the open-circuit inspired-minus-expired O2 mass balance (Feher 6.4, Eqn 6.4.5).

    Whole-body oxygen consumption computed as inspired O2 flow minus expired O2 flow.
    Feher keeps the inspired flow Q_T_star distinct from the expired flow Q_T because
    the two differ whenever the respiratory quotient R != 1 (STPD-corrected volumes).
    Flows Q_T_star and Q_T are in L/min STPD; fIO2 and fEO2 are dimensionless mole
    fractions; returns VO2 in mL O2/min STPD (factor 1000 converts L/min -> mL/min).
    """
    return (Q_T_star * fIO2 - Q_T * fEO2) * 1000.0

oxygen_consumption_gas_exchange = create_equation(
    id='oxygen_consumption_gas_exchange',
    output_units='mL/min',
    name='Oxygen Consumption (Inspired-Expired Gas Exchange)',
    category=EquationCategory.RESPIRATORY,
    latex='\\dot{Q}_{O_2} = Q_T^{*}\\,f_{I_{O_2}} - Q_T\\,f_{E_{O_2}}',
    simplified='VO2 = Q_T_star * fIO2 - Q_T * fEO2',
    description="Whole-body oxygen consumption (VO2) from the open-circuit ventilatory mass balance: inspired O2 volumetric flow minus expired O2 volumetric flow. This is Feher's second, gas-side method for VO2 (indirect calorimetry / open-circuit spirometry, the metabolic-cart measurement), complementary to and cross-checking the blood-side Fick method (oxygen_consumption_fick). Inspired flow Q_T_star and expired flow Q_T are kept distinct because they diverge when the respiratory quotient R differs from 1; all volumes are STPD-corrected. Used when ventilation and inspired/expired O2 fractions are measured but mixed-venous blood sampling is unavailable.",
    compute_func=compute_oxygen_consumption_gas_exchange,
    parameters=[
        Parameter(name='Q_T_star', description='Flow of inspired air (STPD); distinct from expired flow when R != 1', units='L/min', symbol='Q_T^{*}', default_value=5, physiological_range=(2, 220)),
        Parameter(name='fIO2', description='Mole fraction of O2 in dry inspired air (~0.209 room air)', units='dimensionless', symbol='f_{I_{O_2}}', default_value=0.209, physiological_range=(0, 1)),
        Parameter(name='Q_T', description='Flow of expired air (STPD)', units='L/min', symbol='Q_T', default_value=4.96, physiological_range=(2, 220)),
        Parameter(name='fEO2', description='Mole fraction of O2 in expired air (fEO2 = PEO2/(P_B - P_H2O))', units='dimensionless', symbol='f_{E_{O_2}}', default_value=0.163, physiological_range=(0, 1)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=6, source_chapter='6.4',
                              source_section='OXYGEN CONSUMPTION CAN BE CALCULATED FROM THE DIFFERENCE BETWEEN INSPIRED O2 AND EXPIRED O2', page_reference=None,
                              textbook_equation_number='6.4.5'),
)
register_equation(oxygen_consumption_gas_exchange)

try:
    __all__ += ['oxygen_consumption_gas_exchange']
except NameError:
    __all__ = ['oxygen_consumption_gas_exchange']

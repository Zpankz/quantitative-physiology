"""Ventilation-perfusion matching equations."""

"""Bohr Dead Space Equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_dead_space_bohr(P_aCO2: float, P_ECO2: float) -> float:
    """
    Calculate physiological dead space fraction (Bohr equation).

    V_D/V_T = (P_aCO2 - P_ECO2) / P_aCO2

    Parameters
    ----------
    P_aCO2 : float
        Arterial PCO2 (mmHg)
    P_ECO2 : float
        Mixed expired PCO2 (mmHg)

    Returns
    -------
    float
        Dead space fraction (dimensionless, 0-1)
    """
    return (P_aCO2 - P_ECO2) / P_aCO2


# Create equation
dead_space_bohr = create_equation(
    id="dead_space_bohr",
    output_units='dimensionless',
    name="Bohr Dead Space Equation",
    category=EquationCategory.RESPIRATORY,
    latex=r"\frac{V_D}{V_T} = \frac{P_{aCO2} - P_{ECO2}}{P_{aCO2}}",
    simplified="V_D/V_T = (P_aCO2 - P_ECO2) / P_aCO2",
    description="Fraction of tidal volume that does not participate in gas exchange (V̇A/Q̇ = ∞)",
    compute_func=compute_dead_space_bohr,
    parameters=[
        Parameter(
            name="P_aCO2",
            description="Arterial PCO2",
            units="mmHg",
            symbol="P_{aCO2}",
            default_value=40.0,
            physiological_range=(20.0, 80.0)
        ),
        Parameter(
            name="P_ECO2",
            description="Mixed expired PCO2",
            units="mmHg",
            symbol="P_{ECO2}",
            default_value=28.0,
            physiological_range=(10.0, 40.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.4"
    )
)

# Register in global index
register_equation(dead_space_bohr)

"""Shunt Equation."""


def compute_shunt_equation(C_cO2: float, C_aO2: float, C_vO2: float) -> float:
    """
    Calculate shunt fraction (V̇A/Q̇ = 0).

    Q̇_S/Q̇_T = (C_cO2 - C_aO2) / (C_cO2 - C_vO2)

    Parameters
    ----------
    C_cO2 : float
        End-capillary O2 content (mL O2/dL)
    C_aO2 : float
        Arterial O2 content (mL O2/dL)
    C_vO2 : float
        Mixed venous O2 content (mL O2/dL)

    Returns
    -------
    float
        Shunt fraction (dimensionless, 0-1)
    """
    return (C_cO2 - C_aO2) / (C_cO2 - C_vO2)


# Create equation
shunt_equation = create_equation(
    id="shunt_equation",
    output_units='dimensionless',
    name="Shunt Equation",
    category=EquationCategory.RESPIRATORY,
    latex=r"\frac{\dot{Q}_S}{\dot{Q}_T} = \frac{C_{cO2} - C_{aO2}}{C_{cO2} - C_{vO2}}",
    simplified="Q̇_S/Q̇_T = (C_cO2 - C_aO2) / (C_cO2 - C_vO2)",
    description="Fraction of cardiac output that bypasses gas exchange (V̇A/Q̇ = 0)",
    compute_func=compute_shunt_equation,
    parameters=[
        Parameter(
            name="C_cO2",
            description="End-capillary O2 content",
            units="mL O2/dL",
            symbol="C_{cO2}",
            default_value=20.0,
            physiological_range=(15.0, 23.0)
        ),
        Parameter(
            name="C_aO2",
            description="Arterial O2 content",
            units="mL O2/dL",
            symbol="C_{aO2}",
            default_value=19.5,
            physiological_range=(10.0, 22.0)
        ),
        Parameter(
            name="C_vO2",
            description="Mixed venous O2 content",
            units="mL O2/dL",
            symbol="C_{vO2}",
            default_value=15.0,
            physiological_range=(8.0, 18.0)
        )
    ],
    depends_on=["respiratory_oxygen_content", "mixed_venous_oxygen_content"],  # C_aO2, C_vO2 (C_cO2 has no producer)
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.4"
    )
)

# Register in global index
register_equation(shunt_equation)

__all__ = ['shunt_equation', 'dead_space_bohr']

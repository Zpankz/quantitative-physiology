"""Lung volumes and capacities equations."""

"""Alveolar Ventilation equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_alveolar_ventilation(VT: float, VD: float, f: float) -> float:
    """
    Calculate alveolar ventilation (effective gas exchange).

    V_A = (VT - VD) × f

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    VD : float
        Dead space volume (mL)
    f : float
        Respiratory frequency (breaths/min)

    Returns
    -------
    float
        Alveolar ventilation (mL/min)
    """
    return (VT - VD) * f


# Create equation
alveolar_ventilation = create_equation(
    id="alveolar_ventilation",
    output_units='mL/min',
    name="Alveolar Ventilation",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V}_A = (V_T - V_D) \times f",
    simplified="V_A = (VT - VD) × f",
    description="Effective ventilation reaching alveoli for gas exchange",
    compute_func=compute_alveolar_ventilation,
    parameters=[
        Parameter(
            name="VT",
            description="Tidal volume",
            units="mL",
            symbol="V_T",
            default_value=500.0,
            physiological_range=(400.0, 700.0)
        ),
        Parameter(
            name="VD",
            description="Dead space volume",
            units="mL",
            symbol="V_D",
            default_value=150.0,
            physiological_range=(100.0, 200.0)
        ),
        Parameter(
            name="f",
            description="Respiratory frequency",
            units="breaths/min",
            symbol="f",
            default_value=12.0,
            physiological_range=(10.0, 20.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(alveolar_ventilation)

"""Functional Residual Capacity (FRC) equation."""


def compute_functional_residual_capacity(ERV: float, RV: float) -> float:
    """
    Calculate functional residual capacity.

    FRC = ERV + RV

    Parameters
    ----------
    ERV : float
        Expiratory reserve volume (mL)
    RV : float
        Residual volume (mL)

    Returns
    -------
    float
        Functional residual capacity (mL)
    """
    return ERV + RV


# Create equation
functional_residual_capacity = create_equation(
    id="functional_residual_capacity",
    output_units='mL',
    name="Functional Residual Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"FRC = ERV + RV",
    simplified="FRC = ERV + RV",
    description="Functional residual capacity is the volume remaining in lungs after normal expiration",
    compute_func=compute_functional_residual_capacity,
    parameters=[
        Parameter(
            name="ERV",
            description="Expiratory reserve volume",
            units="mL",
            symbol="ERV",
            default_value=1100.0,
            physiological_range=(800.0, 1500.0)
        ),
        Parameter(
            name="RV",
            description="Residual volume",
            units="mL",
            symbol="RV",
            default_value=1200.0,
            physiological_range=(1000.0, 1500.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(functional_residual_capacity)

"""Inspiratory Capacity (IC) equation."""


def compute_inspiratory_capacity(VT: float, IRV: float) -> float:
    """
    Calculate inspiratory capacity.

    IC = VT + IRV

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    IRV : float
        Inspiratory reserve volume (mL)

    Returns
    -------
    float
        Inspiratory capacity (mL)
    """
    return VT + IRV


# Create equation
inspiratory_capacity = create_equation(
    id="inspiratory_capacity",
    output_units='mL',
    name="Inspiratory Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"IC = V_T + IRV",
    simplified="IC = VT + IRV",
    description="Inspiratory capacity is the maximum volume that can be inhaled from resting level",
    compute_func=compute_inspiratory_capacity,
    parameters=[
        Parameter(
            name="VT",
            description="Tidal volume",
            units="mL",
            symbol="V_T",
            default_value=500.0,
            physiological_range=(400.0, 700.0)
        ),
        Parameter(
            name="IRV",
            description="Inspiratory reserve volume",
            units="mL",
            symbol="IRV",
            default_value=3000.0,
            physiological_range=(2000.0, 3500.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(inspiratory_capacity)

"""Minute Ventilation equation."""


def compute_minute_ventilation(VT: float, f: float) -> float:
    """
    Calculate total minute ventilation.

    V_E = VT × f

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    f : float
        Respiratory frequency (breaths/min)

    Returns
    -------
    float
        Minute ventilation (mL/min)
    """
    return VT * f


# Create equation
minute_ventilation = create_equation(
    id="minute_ventilation",
    output_units='mL/min',
    name="Minute Ventilation",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V}_E = V_T \times f",
    simplified="V_E = VT × f",
    description="Total volume of air breathed per minute",
    compute_func=compute_minute_ventilation,
    parameters=[
        Parameter(
            name="VT",
            description="Tidal volume",
            units="mL",
            symbol="V_T",
            default_value=500.0,
            physiological_range=(400.0, 700.0)
        ),
        Parameter(
            name="f",
            description="Respiratory frequency",
            units="breaths/min",
            symbol="f",
            default_value=12.0,
            physiological_range=(10.0, 20.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(minute_ventilation)

"""Total Lung Capacity (TLC) equation."""


def compute_total_lung_capacity(VT: float, IRV: float, ERV: float, RV: float) -> float:
    """
    Calculate total lung capacity.

    TLC = VT + IRV + ERV + RV

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    IRV : float
        Inspiratory reserve volume (mL)
    ERV : float
        Expiratory reserve volume (mL)
    RV : float
        Residual volume (mL)

    Returns
    -------
    float
        Total lung capacity (mL)
    """
    return VT + IRV + ERV + RV


# Create equation
total_lung_capacity = create_equation(
    id="total_lung_capacity",
    output_units='mL',
    name="Total Lung Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"TLC = V_T + IRV + ERV + RV",
    simplified="TLC = VT + IRV + ERV + RV",
    description="Total lung capacity is the sum of all lung volumes",
    compute_func=compute_total_lung_capacity,
    parameters=[
        Parameter(
            name="VT",
            description="Tidal volume",
            units="mL",
            symbol="V_T",
            default_value=500.0,
            physiological_range=(400.0, 700.0)
        ),
        Parameter(
            name="IRV",
            description="Inspiratory reserve volume",
            units="mL",
            symbol="IRV",
            default_value=3000.0,
            physiological_range=(2000.0, 3500.0)
        ),
        Parameter(
            name="ERV",
            description="Expiratory reserve volume",
            units="mL",
            symbol="ERV",
            default_value=1100.0,
            physiological_range=(800.0, 1500.0)
        ),
        Parameter(
            name="RV",
            description="Residual volume",
            units="mL",
            symbol="RV",
            default_value=1200.0,
            physiological_range=(1000.0, 1500.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(total_lung_capacity)

"""Vital Capacity (VC) equation."""


def compute_vital_capacity(VT: float, IRV: float, ERV: float) -> float:
    """
    Calculate vital capacity.

    VC = VT + IRV + ERV

    Parameters
    ----------
    VT : float
        Tidal volume (mL)
    IRV : float
        Inspiratory reserve volume (mL)
    ERV : float
        Expiratory reserve volume (mL)

    Returns
    -------
    float
        Vital capacity (mL)
    """
    return VT + IRV + ERV


# Create equation
vital_capacity = create_equation(
    id="vital_capacity",
    output_units='mL',
    name="Vital Capacity",
    category=EquationCategory.RESPIRATORY,
    latex=r"VC = V_T + IRV + ERV",
    simplified="VC = VT + IRV + ERV",
    description="Vital capacity is the maximum volume that can be exhaled after maximum inhalation",
    compute_func=compute_vital_capacity,
    parameters=[
        Parameter(
            name="VT",
            description="Tidal volume",
            units="mL",
            symbol="V_T",
            default_value=500.0,
            physiological_range=(400.0, 700.0)
        ),
        Parameter(
            name="IRV",
            description="Inspiratory reserve volume",
            units="mL",
            symbol="IRV",
            default_value=3000.0,
            physiological_range=(2000.0, 3500.0)
        ),
        Parameter(
            name="ERV",
            description="Expiratory reserve volume",
            units="mL",
            symbol="ERV",
            default_value=1100.0,
            physiological_range=(800.0, 1500.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.1"
    )
)

# Register in global index
register_equation(vital_capacity)

__all__ = ['total_lung_capacity', 'vital_capacity', 'functional_residual_capacity', 'inspiratory_capacity', 'minute_ventilation', 'alveolar_ventilation']

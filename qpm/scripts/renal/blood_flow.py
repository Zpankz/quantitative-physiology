"""Consolidated module for renal.blood_flow."""

"""
Filtration Fraction (FF) calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_filtration_fraction(GFR: float, RPF: float) -> float:
    """
    Calculate filtration fraction.

    Args:
        GFR: Glomerular filtration rate (mL/min)
        RPF: Renal plasma flow (mL/min)

    Returns:
        FF: Filtration fraction (dimensionless, typically ~0.20)
    """
    return GFR / RPF


# Create equation
filtration_fraction = create_equation(
    id="filtration_fraction",
    output_units='dimensionless',
    name="Filtration Fraction",
    category=EquationCategory.RENAL,
    latex=r"FF = \frac{GFR}{RPF}",
    simplified="FF = GFR / RPF",
    description="Fraction of renal plasma flow that is filtered at the glomerulus",
    compute_func=compute_filtration_fraction,
    parameters=[
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        ),
        Parameter(
            name="RPF",
            description="Renal plasma flow",
            units="mL/min",
            symbol="RPF",
            physiological_range=(600, 700)
        )
    ],
    depends_on=["gfr_from_nfp"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1"
    )
)

# Register equation
register_equation(filtration_fraction)

"""
Renal Plasma Flow (RPF) calculation from Renal Blood Flow.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_rpf(RBF: float, Hct: float = 0.45) -> float:
    """
    Calculate renal plasma flow from renal blood flow.

    Args:
        RBF: Renal blood flow (L/min)
        Hct: Hematocrit (fraction, default 0.45)

    Returns:
        RPF: Renal plasma flow (L/min)
    """
    return RBF * (1 - Hct)


# Create equation
renal_plasma_flow = create_equation(
    id="renal_plasma_flow",
    output_units='L/min',
    name="Renal Plasma Flow",
    category=EquationCategory.RENAL,
    latex=r"RPF = RBF \times (1 - Hct)",
    simplified="RPF = RBF × (1 - Hct)",
    description="Calculates renal plasma flow from renal blood flow and hematocrit",
    compute_func=compute_rpf,
    parameters=[
        Parameter(
            name="RBF",
            description="Renal blood flow",
            units="L/min",
            symbol="RBF",
            physiological_range=(0.8, 1.5)
        ),
        Parameter(
            name="Hct",
            description="Hematocrit (fraction)",
            units="dimensionless",
            symbol="Hct",
            default_value=0.45,
            physiological_range=(0.35, 0.52)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1"
    )
)

# Register equation
register_equation(renal_plasma_flow)

"""
Renal Vascular Resistance (RVR) calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_rvr(P_a: float, P_v: float, RBF: float) -> float:
    """
    Calculate renal vascular resistance.

    Args:
        P_a: Arterial pressure (mmHg)
        P_v: Venous pressure (mmHg)
        RBF: Renal blood flow (mL/min)

    Returns:
        RVR: Renal vascular resistance (mmHg·min/mL)
    """
    return (P_a - P_v) / RBF


# Create equation
renal_vascular_resistance = create_equation(
    id="renal_vascular_resistance",
    output_units='mmHg*min/mL',
    name="Renal Vascular Resistance",
    category=EquationCategory.RENAL,
    latex=r"RVR = \frac{P_a - P_v}{RBF}",
    simplified="RVR = (P_a - P_v) / RBF",
    description="Resistance to blood flow through the renal vasculature",
    compute_func=compute_rvr,
    parameters=[
        Parameter(
            name="P_a",
            description="Arterial pressure",
            units="mmHg",
            symbol="P_a",
            physiological_range=(80, 120)
        ),
        Parameter(
            name="P_v",
            description="Venous pressure",
            units="mmHg",
            symbol="P_v",
            physiological_range=(0, 10)
        ),
        Parameter(
            name="RBF",
            description="Renal blood flow",
            units="mL/min",
            symbol="RBF",
            physiological_range=(800, 1500)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.1"
    )
)

# Register equation
register_equation(renal_vascular_resistance)


"""Synapse Equations

Neuromuscular junction and synaptic transmission equations.

Source: Quantitative Human Physiology 3rd Edition, Unit 3"""

"""
Neuromuscular Junction Quantal Content

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def quantal_content(EPP: float = 75.0, MEPP: float = 0.5) -> float:
    """
    Quantal content of neuromuscular transmission.

    Formula: m = EPP / MEPP

    The quantal content represents the average number of vesicles
    released per action potential at the neuromuscular junction.

    Parameters:
    -----------
    EPP : float - End-plate potential amplitude (mV), default: 75.0
    MEPP : float - Miniature end-plate potential amplitude (mV), default: 0.5

    Returns:
    --------
    m : float - Quantal content (number of vesicles)
    """
    return EPP / MEPP

# Create and register atomic equation
quantal_content_eq = create_equation(
    id="quantal_content_epp_mepp",
    output_units='dimensionless',
    name="Neuromuscular Junction Quantal Content (EPP/MEPP method)",
    category=EquationCategory.EXCITABLE,
    latex=r"m = \frac{\text{EPP}}{\text{MEPP}}",
    simplified="m = EPP / MEPP",
    description="Average number of neurotransmitter vesicles released per action potential",
    compute_func=quantal_content,
    parameters=[
        Parameter(
            name="EPP",
            description="End-plate potential amplitude",
            units="mV",
            symbol="EPP",
            default_value=75.0,
            physiological_range=(50.0, 100.0)
        ),
        Parameter(
            name="MEPP",
            description="Miniature end-plate potential amplitude",
            units="mV",
            symbol="MEPP",
            default_value=0.5,
            physiological_range=(0.3, 1.5)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.6")
)
register_equation(quantal_content_eq)

"""
Neuromuscular Junction Safety Factor

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def safety_factor(EPP: float = 75.0, threshold: float = 20.0) -> float:
    """
    Safety factor for neuromuscular transmission.

    Formula: Safety Factor = EPP / Threshold

    The safety factor indicates how much the EPP exceeds the threshold
    needed to trigger an action potential in the muscle fiber.

    Parameters:
    -----------
    EPP : float - End-plate potential amplitude (mV), default: 75.0
    threshold : float - Threshold for muscle action potential (mV), default: 20.0

    Returns:
    --------
    SF : float - Safety factor (dimensionless)
    """
    return EPP / threshold

# Create and register atomic equation
safety_factor_eq = create_equation(
    id="safety_factor",
    output_units='dimensionless',
    name="Neuromuscular Junction Safety Factor",
    category=EquationCategory.EXCITABLE,
    latex=r"\text{SF} = \frac{\text{EPP}}{\text{Threshold}}",
    simplified="SF = EPP / Threshold",
    description="Margin of safety for successful neuromuscular transmission",
    compute_func=safety_factor,
    parameters=[
        Parameter(
            name="EPP",
            description="End-plate potential amplitude",
            units="mV",
            symbol="EPP",
            default_value=75.0,
            physiological_range=(50.0, 100.0)
        ),
        Parameter(
            name="threshold",
            description="Threshold for muscle action potential",
            units="mV",
            symbol="V_{th}",
            default_value=20.0,
            physiological_range=(15.0, 30.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.6")
)
register_equation(safety_factor_eq)

__all__ = ['quantal_content_eq', 'safety_factor_eq']

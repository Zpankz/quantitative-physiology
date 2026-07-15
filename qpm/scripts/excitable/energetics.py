"""Muscle Energetics Equations

ATP consumption and efficiency during muscle contraction.

Source: Quantitative Human Physiology 3rd Edition, Unit 3"""

"""
Muscle ATP Consumption Rate

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def atp_consumption(isometric_rate: float, shortening_rate: float, v: float) -> float:
    """
    ATP consumption rate during muscle contraction.

    Formula: ATP rate = (isometric rate) + (shortening rate) × v

    The ATP consumption has a baseline isometric component plus
    a velocity-dependent shortening component.

    Parameters:
    -----------
    isometric_rate : float - ATP consumption during isometric contraction (mol/s)
    shortening_rate : float - Additional ATP rate per unit velocity (mol/s per m/s)
    v : float - Shortening velocity (m/s)

    Returns:
    --------
    ATP_rate : float - ATP consumption rate (mol/s)
    """
    return isometric_rate + shortening_rate * v

# Create and register atomic equation
atp_consumption_eq = create_equation(
    id="atp_consumption",
    output_units='mol/s',
    name="Muscle ATP Consumption Rate",
    category=EquationCategory.EXCITABLE,
    latex=r"\dot{ATP} = \dot{ATP}_{iso} + \dot{ATP}_{short} \cdot v",
    simplified="ATP rate = (isometric rate) + (shortening rate) × v",
    description="Rate of ATP hydrolysis during muscle contraction",
    compute_func=atp_consumption,
    parameters=[
        Parameter(
            name="isometric_rate",
            description="ATP consumption during isometric contraction",
            units="mol/s",
            symbol=r"\dot{ATP}_{iso}",
            physiological_range=(0.0, 1e-3)
        ),
        Parameter(
            name="shortening_rate",
            description="Additional ATP rate per unit velocity",
            units="mol/s per m/s",
            symbol=r"\dot{ATP}_{short}",
            physiological_range=(0.0, 1e-3)
        ),
        Parameter(
            name="v",
            description="Shortening velocity",
            units="m/s",
            symbol="v",
            physiological_range=(0.0, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.4")
)
register_equation(atp_consumption_eq)

"""
Muscle Mechanical Efficiency

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def muscle_efficiency(P: float, heat_rate: float) -> float:
    """
    Mechanical efficiency of muscle contraction.

    Formula: η = Mechanical work / Total energy = P / (P + Heat rate)

    Maximum efficiency is approximately 25-40% in skeletal muscle.

    Parameters:
    -----------
    P : float - Mechanical power output (W)
    heat_rate : float - Heat production rate (W)

    Returns:
    --------
    eta : float - Efficiency (dimensionless, 0-1)
    """
    total_energy = P + heat_rate
    if total_energy > 0:
        return P / total_energy
    else:
        return 0.0

# Create and register atomic equation
muscle_efficiency_eq = create_equation(
    id="muscle_efficiency",
    output_units='dimensionless',
    name="Muscle Mechanical Efficiency",
    category=EquationCategory.EXCITABLE,
    latex=r"\eta = \frac{P}{P + \dot{Q}}",
    simplified="η = P / (P + Heat rate)",
    description="Ratio of mechanical work to total energy expenditure",
    compute_func=muscle_efficiency,
    parameters=[
        Parameter(
            name="P",
            description="Mechanical power output",
            units="W",
            symbol="P",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="heat_rate",
            description="Heat production rate",
            units="W",
            symbol=r"\dot{Q}",
            physiological_range=(0.0, 2000.0)
        ),
    ],
    depends_on=["muscle_power"],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.4")
)
register_equation(muscle_efficiency_eq)

__all__ = ['atp_consumption_eq', 'muscle_efficiency_eq']

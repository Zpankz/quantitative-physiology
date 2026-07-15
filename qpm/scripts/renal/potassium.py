"""Consolidated module for renal.potassium."""

"""
Nernst potential for potassium in renal tubular cells.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

import math
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation


def compute_k_nernst(K_lumen: float, K_cell: float, T: float = 310.0) -> float:
    """
    Calculate Nernst potential for K+ across tubular cell membrane.

    Args:
        K_lumen: Luminal K+ concentration (mM)
        K_cell: Intracellular K+ concentration (mM)
        T: Temperature (K, default 310 = 37°C)

    Returns:
        E_K: K+ equilibrium potential (mV)
    """
    R = PHYSICAL_CONSTANTS["R"].default_value
    F = PHYSICAL_CONSTANTS["F"].default_value

    return (R * T / F) * math.log(K_lumen / K_cell) * 1000  # Convert to mV


# Create equation
k_nernst_potential = create_equation(
    id="k_nernst_potential",
    output_units='mV',
    produces="E_K",
    name="K+ Nernst Potential (Renal)",
    category=EquationCategory.RENAL,
    latex=r"E_K = \frac{RT}{F} \ln\left(\frac{[K^+]_{lumen}}{[K^+]_{cell}}\right)",
    simplified="E_K = (RT/F) × ln([K+]_lumen / [K+]_cell)",
    description="Equilibrium potential for K+ across tubular epithelial cell membrane",
    compute_func=compute_k_nernst,
    parameters=[
        Parameter(
            name="K_lumen",
            description="Luminal K+ concentration",
            units="mM",
            symbol="[K^+]_{lumen}",
            physiological_range=(1, 100)
        ),
        Parameter(
            name="K_cell",
            description="Intracellular K+ concentration",
            units="mM",
            symbol="[K^+]_{cell}",
            physiological_range=(120, 150)
        ),
        Parameter(
            name="T",
            description="Temperature",
            units="K",
            symbol="T",
            default_value=310.0,
            physiological_range=(306, 315)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.8"
    )
)

# Register equation
register_equation(k_nernst_potential)

"""
Electrochemical driving force for potassium secretion.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)


def compute_k_driving_force(V_m: float, E_K: float) -> float:
    """
    Calculate electrochemical driving force for K+ secretion.

    Args:
        V_m: Membrane potential (mV)
        E_K: K+ equilibrium potential (mV)

    Returns:
        Driving force (mV), positive = secretion favored
    """
    return V_m - E_K


# Create equation
k_secretion_driving_force = create_equation(
    id="k_secretion_driving_force",
    output_units='mV',
    name="K+ Secretion Driving Force",
    category=EquationCategory.RENAL,
    latex=r"DF_K = V_m - E_K",
    simplified="DF_K = V_m - E_K",
    description="Electrochemical gradient driving K+ secretion from principal cells into tubular lumen",
    compute_func=compute_k_driving_force,
    parameters=[
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            physiological_range=(-80, -20)
        ),
        Parameter(
            name="E_K",
            description="K+ equilibrium potential (Nernst)",
            units="mV",
            symbol="E_K",
            physiological_range=(-100, -50)
        )
    ],
    depends_on=["k_nernst_potential"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.8"
    )
)

# Register equation
register_equation(k_secretion_driving_force)

"""
Potassium secretion flux through ROMK channels.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_k_secretion_flux(g_K: float, V_m: float, E_K: float) -> float:
    """
    Calculate K+ secretion flux.

    Args:
        g_K: K+ conductance (S or mS)
        V_m: Membrane potential (mV)
        E_K: K+ equilibrium potential (mV)

    Returns:
        J_K: K+ flux (current or flux units depending on g_K)
    """
    return g_K * (V_m - E_K)


# Create equation
k_secretion_flux = create_equation(
    id="k_secretion_flux",
    output_units='mA',
    name="K+ Secretion Flux",
    category=EquationCategory.RENAL,
    latex=r"J_K = g_K \times (V_m - E_K)",
    simplified="J_K = g_K × (V_m - E_K)",
    description="K+ flux through ROMK channels driven by electrochemical gradient",
    compute_func=compute_k_secretion_flux,
    parameters=[
        Parameter(
            name="g_K",
            description="K+ conductance",
            units="S or mS",
            symbol="g_K",
            physiological_range=(0.001, 1.0)
        ),
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            physiological_range=(-80, -20)
        ),
        Parameter(
            name="E_K",
            description="K+ equilibrium potential",
            units="mV",
            symbol="E_K",
            physiological_range=(-100, -50)
        )
    ],
    depends_on=["k_nernst_potential"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.8"
    )
)

# Register equation
register_equation(k_secretion_flux)


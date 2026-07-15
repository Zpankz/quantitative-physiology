"""Membrane potential equations - Donnan equilibrium."""

"""
Gibbs-Donnan Potential - Potential difference due to impermeant charged species

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np

def compute_donnan_potential(r: float, R: float = 8.314, T_body: float = 310.0, F: float = 96485.0) -> float:
    """
    Calculate Gibbs-Donnan potential.

    Formula: E_Donnan = (RT/F) × ln(r)

    Parameters:
    -----------
    r : float
        Donnan ratio ([K+]_1/[K+]_2)
    R : float
        Gas constant (J/(mol·K)), default: 8.314
    T_body : float
        Body temperature (K), default: 310 K (37°C)
    F : float
        Faraday constant (C/mol), default: 96485

    Returns:
    --------
    E_Donnan : float
        Donnan potential (V)
        Convert to mV by multiplying by 1000

    Consequences:
        - Unequal ion distributions
        - Osmotic imbalance (requires pump compensation)
        - Contributes to resting membrane potential
    """
    return (R * T_body / F) * np.log(r)


# Create and register atomic equation
donnan_potential = create_equation(
    id="donnan_potential",
    output_units='V',
    name="Gibbs-Donnan Potential",
    category=EquationCategory.MEMBRANE,
    latex=r"E_{Donnan} = \frac{RT}{F} \ln(r)",
    simplified="E_Donnan = (RT/F) * ln(r)",
    description="Membrane potential arising from unequal ion distribution due to impermeant charged species.",
    compute_func=compute_donnan_potential,
    parameters=[
        Parameter(
            name="r",
            description="Donnan ratio",
            units="dimensionless",
            symbol="r",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"],
        PHYSICAL_CONSTANTS["F"],
    ],
    depends_on=["donnan_ratio"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.5")
)

register_equation(donnan_potential)

"""
Gibbs-Donnan Ratio - Ion distribution ratio across membrane with impermeant charged species

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)

def compute_donnan_ratio(C_protein: float, z_protein: float, C_salt: float) -> float:
    """
    Calculate Gibbs-Donnan ratio for ion distribution.

    Formula: r = [K+]_1/[K+]_2 = [Cl-]_2/[Cl-]_1

    Derived from electroneutrality and equilibrium conditions:
    [K+]_1 = (|z|*C_p + sqrt((|z|*C_p)² + 4*C_salt²)) / 2

    Parameters:
    -----------
    C_protein : float
        Concentration of impermeant protein (mol/m³ or mM)
    z_protein : float
        Net charge on protein (typically negative)
    C_salt : float
        Salt concentration in compartment 2 (mol/m³ or mM)

    Returns:
    --------
    r : float
        Donnan ratio (dimensionless)
        r > 1 indicates accumulation of cations in compartment 1
    """
    z = abs(z_protein)

    # Solve quadratic for electroneutrality
    K_in = (z * C_protein + np.sqrt((z * C_protein)**2 + 4 * C_salt**2)) / 2
    return K_in / C_salt


# Create and register atomic equation
donnan_ratio = create_equation(
    id="donnan_ratio",
    output_units='dimensionless',
    name="Gibbs-Donnan Ratio",
    category=EquationCategory.MEMBRANE,
    latex=r"r = \frac{[K^+]_1}{[K^+]_2} = \frac{[Cl^-]_2}{[Cl^-]_1}",
    simplified="r = [K+]_1/[K+]_2 = [Cl-]_2/[Cl-]_1",
    description="Ion distribution ratio when impermeant charged species (e.g., proteins) are confined to one compartment.",
    compute_func=compute_donnan_ratio,
    parameters=[
        Parameter(
            name="C_protein",
            description="Impermeant protein concentration",
            units="mol/m³",
            symbol="C_p",
            default_value=None,
            physiological_range=(0.0, 10.0)  # mM
        ),
        Parameter(
            name="z_protein",
            description="Net charge on protein",
            units="dimensionless",
            symbol="z_p",
            default_value=None,
            physiological_range=(-100.0, 100.0)
        ),
        Parameter(
            name="C_salt",
            description="Salt concentration in compartment 2",
            units="mol/m³",
            symbol="C_{salt}",
            default_value=None,
            physiological_range=(0.0, 200.0)  # mM
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.5")
)

register_equation(donnan_ratio)

__all__ = ['donnan_ratio', 'donnan_potential']

"""Cellular metabolism equations - energy production and metabolic scaling."""

"""
Basal Metabolic Rate - Kleiber's law for metabolic scaling

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_basal_metabolic_rate(M: float) -> float:
    """
    Calculate basal metabolic rate using Kleiber's law.

    Formula: BMR ≈ 70 × M^0.75

    This is an allometric scaling law showing BMR scales with body mass
    to the 3/4 power across species.

    Parameters:
    -----------
    M : float
        Body mass (kg)

    Returns:
    --------
    BMR : float
        Basal metabolic rate (kcal/day)

    Examples:
        70 kg human: BMR ≈ 1680 kcal/day
        5 kg cat: BMR ≈ 260 kcal/day
        500 kg horse: BMR ≈ 7400 kcal/day

    Notes:
        The 3/4 power law is observed across 27 orders of magnitude
        in body size, from bacteria to whales.
    """
    return 70 * M**0.75


# Create and register atomic equation
basal_metabolic_rate = create_equation(
    id="basal_metabolic_rate",
    output_units='kcal/day',
    name="Basal Metabolic Rate (Kleiber's Law)",
    category=EquationCategory.MEMBRANE,
    latex=r"BMR \approx 70 \cdot M^{0.75}",
    simplified="BMR = 70 * M^0.75",
    description="Allometric scaling of basal metabolic rate with body mass (Kleiber's law).",
    compute_func=compute_basal_metabolic_rate,
    parameters=[
        Parameter(
            name="M",
            description="Body mass",
            units="kg",
            symbol="M",
            default_value=None,
            physiological_range=(0.001, 100000.0)  # 1g to 100 tons
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.7")
)

register_equation(basal_metabolic_rate)

"""
Chemiosmotic Coupling - Free energy from proton gradient (Mitchell hypothesis)

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)

def compute_chemiosmotic_free_energy(delta_psi: float, delta_pH: float,
                                     F: float = 96485.0, R: float = 8.314,
                                     T_body: float = 310.0) -> float:
    """
    Calculate free energy from proton gradient (chemiosmotic coupling).

    Formula: ΔG = F × Δψ + 2.3RT × ΔpH

    This is the Mitchell hypothesis: ATP synthesis driven by proton gradient

    Parameters:
    -----------
    delta_psi : float
        Membrane potential difference (V)
    delta_pH : float
        pH difference across membrane (pH_in - pH_out)
    F : float
        Faraday constant (C/mol), default: 96485
    R : float
        Gas constant (J/(mol·K)), default: 8.314
    T_body : float
        Body temperature (K), default: 310 K (37°C)

    Returns:
    --------
    delta_G : float
        Free energy per mole of H+ (J/mol)

    Notes:
        Mitochondrial gradient: Δψ ≈ 150-180 mV, ΔpH ≈ 0.5-1.0
        Total ΔG ≈ 20-25 kJ/mol H+
    """
    electrical = F * delta_psi
    chemical = 2.3 * R * T_body * delta_pH
    return electrical + chemical


# Create and register atomic equation
chemiosmotic_coupling = create_equation(
    id="chemiosmotic_coupling",
    output_units='J/mol',
    name="Chemiosmotic Coupling (Mitchell Hypothesis)",
    category=EquationCategory.MEMBRANE,
    latex=r"\Delta G = F \Delta \psi + 2.3RT \Delta pH",
    simplified="delta_G = F*delta_psi + 2.3*R*T*delta_pH",
    description="Free energy available from proton gradient for ATP synthesis in oxidative phosphorylation.",
    compute_func=compute_chemiosmotic_free_energy,
    parameters=[
        Parameter(
            name="delta_psi",
            description="Membrane potential difference",
            units="V",
            symbol=r"\Delta \psi",
            default_value=None,
            physiological_range=(0.1, 0.2)  # 100-200 mV
        ),
        Parameter(
            name="delta_pH",
            description="pH difference (inside - outside)",
            units="dimensionless",
            symbol=r"\Delta pH",
            default_value=None,
            physiological_range=(0.0, 2.0)
        ),
        PHYSICAL_CONSTANTS["F"],
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"],
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.7")
)

register_equation(chemiosmotic_coupling)

"""
Respiratory Quotient - Ratio of CO2 production to O2 consumption

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""

def compute_respiratory_quotient(CO2_produced: float, O2_consumed: float) -> float:
    """
    Calculate respiratory quotient (RQ).

    Formula: RQ = CO₂ produced / O₂ consumed

    RQ indicates which substrate is being oxidized:

    Parameters:
    -----------
    CO2_produced : float
        Rate of CO2 production (mol/time)
    O2_consumed : float
        Rate of O2 consumption (mol/time)

    Returns:
    --------
    RQ : float
        Respiratory quotient (dimensionless)

    Typical values:
        Carbohydrates: RQ = 1.0
            C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O
        Fats: RQ ≈ 0.7
            C₁₆H₃₂O₂ + 23O₂ → 16CO₂ + 16H₂O
        Proteins: RQ ≈ 0.8
        Mixed diet: RQ ≈ 0.8-0.85
    """
    return CO2_produced / O2_consumed


# Create and register atomic equation
respiratory_quotient = create_equation(
    id="respiratory_quotient",
    output_units='dimensionless',
    name="Respiratory Quotient",
    category=EquationCategory.MEMBRANE,
    latex=r"RQ = \frac{CO_2 \text{ produced}}{O_2 \text{ consumed}}",
    simplified="RQ = CO2_produced / O2_consumed",
    description="Ratio of CO2 production to O2 consumption, indicating fuel substrate being oxidized.",
    compute_func=compute_respiratory_quotient,
    parameters=[
        Parameter(
            name="CO2_produced",
            description="Rate of CO2 production",
            units="mol/time",
            symbol=r"\dot{V}_{CO_2}",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="O2_consumed",
            description="Rate of O2 consumption",
            units="mol/time",
            symbol=r"\dot{V}_{O_2}",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.7")
)

register_equation(respiratory_quotient)

__all__ = ['chemiosmotic_coupling', 'basal_metabolic_rate', 'respiratory_quotient']

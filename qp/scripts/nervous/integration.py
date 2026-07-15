"""Consolidated module for nervous.integration."""

"""
Cable Equation for Dendrites - Spatial and temporal voltage distribution

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_cable_equation_steady_state(x: float, V_0: float, lambda_const: float) -> float:
    """
    Calculate steady-state voltage distribution along dendrite (cable equation).

    Formula: V(x) = V_0 × e^(-x/λ)
    Full PDE: λ² × (∂²V/∂x²) = τ_m × (∂V/∂t) + V

    Parameters:
    -----------
    x : float
        Distance along dendrite (μm)
    V_0 : float
        Voltage at x=0 (mV)
    lambda_const : float
        Length constant λ = sqrt(R_m / R_i) (μm)

    Returns:
    --------
    V : float
        Voltage at position x (mV)

    Notes:
    ------
    Length constant λ determines how far voltage spreads electrotonically.
    Typical values: λ ≈ 100-1000 μm for dendrites
    At x = λ, voltage decays to 1/e ≈ 37% of original
    """
    return V_0 * np.exp(-x / lambda_const)


# Create and register atomic equation
cable_equation = create_equation(
    id="cable_equation_dendrite",
    output_units='mV',
    name="Cable Equation (Dendrite)",
    category=EquationCategory.NERVOUS,
    latex=r"\lambda^2 \times \frac{\partial^2 V}{\partial x^2} = \tau_m \times \frac{\partial V}{\partial t} + V",
    simplified="λ² × (∂²V/∂x²) = τ_m × (∂V/∂t) + V",
    description="Cable equation describing voltage distribution in dendrites. Governs electrotonic spread of synaptic potentials. Steady-state solution: V(x) = V_0 × e^(-x/λ)",
    compute_func=compute_cable_equation_steady_state,
    parameters=[
        Parameter(
            name="x",
            description="Distance along dendrite",
            units="μm",
            symbol="x",
            default_value=None,
            physiological_range=(0.0, 2000.0)
        ),
        Parameter(
            name="V_0",
            description="Voltage at origin",
            units="mV",
            symbol="V_0",
            default_value=None,
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="lambda_const",
            description="Length constant",
            units="μm",
            symbol=r"\lambda",
            default_value=None,
            physiological_range=(10.0, 2000.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(cable_equation)

"""
Dendrite Input Resistance - Input resistance at dendritic branch point

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_dendrite_input_resistance(R_m: float, R_i: float, a: float) -> float:
    """
    Calculate input resistance at infinite dendrite.

    Formula: R_∞ = √(R_m × R_i) / (2πa^(3/2))

    Parameters:
    -----------
    R_m : float
        Specific membrane resistance (Ω·cm²)
    R_i : float
        Specific internal (axial) resistance (Ω·cm)
    a : float
        Dendrite radius (μm)

    Returns:
    --------
    R_inf : float
        Input resistance (MΩ)

    Notes:
    ------
    This is the input resistance for semi-infinite cylindrical dendrite.
    Lower for large dendrites, higher for thin dendrites.
    Determines amplitude of synaptic potentials.
    """
    # Convert radius from μm to cm
    a_cm = a * 1e-4
    # Calculate in Ω, then convert to MΩ
    R_inf = np.sqrt(R_m * R_i) / (2 * np.pi * a_cm**1.5)
    return R_inf * 1e-6  # Convert to MΩ


# Create and register atomic equation
dendrite_input_resistance = create_equation(
    id="dendrite_input_resistance",  # PROVISIONAL denominator constant: code uses 2*pi; cable-theory candidates also sqrt(2)*pi and 2*sqrt(2)*pi depending on boundary convention (sealed vs open end). No Feher anchor resolves it; value is convention-dependent.
    output_units='MΩ',
    name="Dendrite Input Resistance",
    category=EquationCategory.NERVOUS,
    latex=r"R_\infty = \frac{\sqrt{R_m \times R_i}}{2\pi a^{3/2}}",
    simplified="R_∞ = √(R_m × R_i) / (2πa^(3/2))",
    description="Input resistance at a dendritic location, assuming semi-infinite cable. Determines how current injection affects local voltage.",
    compute_func=compute_dendrite_input_resistance,
    parameters=[
        Parameter(
            name="R_m",
            description="Specific membrane resistance",
            units="Ω·cm²",
            symbol="R_m",
            default_value=None,
            physiological_range=(100.0, 100000.0)
        ),
        Parameter(
            name="R_i",
            description="Specific internal resistance",
            units="Ω·cm",
            symbol="R_i",
            default_value=None,
            physiological_range=(10.0, 500.0)
        ),
        Parameter(
            name="a",
            description="Dendrite radius",
            units="μm",
            symbol="a",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(dendrite_input_resistance)


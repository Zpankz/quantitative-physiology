"""Diffusion equations - Random molecular motion and transport.

Includes:
- Fick's first law (diffusive flux)
- Stokes-Einstein equation (diffusion coefficient)
- Diffusion time scaling"""

"""
Diffusion Time - Characteristic time for diffusion over distance

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_diffusion_time(x: float, D: float) -> float:
    """
    Calculate characteristic time for diffusion over distance x.

    Formula: t = x²/(2D)

    Parameters:
    -----------
    x : float - Distance (m)
    D : float - Diffusion coefficient (m²/s)

    Returns:
    --------
    t : float - Diffusion time (s)
    """
    return x**2 / (2 * D)


# Create and register atomic equation
diffusion_time = create_equation(
    id="diffusion_time",
    output_units='s',
    name="Diffusion Time",
    category=EquationCategory.FOUNDATIONS,
    latex=r"t = \frac{x^2}{2D}",
    simplified="t = x^2 / (2*D)",
    description="Time for diffusion scales as distance squared - explains why circulation is needed for large organisms",
    compute_func=compute_diffusion_time,
    parameters=[
        Parameter(
            name="x",
            description="Diffusion distance",
            units="m",
            symbol="x",
            physiological_range=(1e-9, 1e-2)  # nm to cm
        ),
        Parameter(
            name="D",
            description="Diffusion coefficient",
            units="m²/s",
            symbol="D",
            physiological_range=(1e-11, 1e-8)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.3")
)

register_equation(diffusion_time)

"""
Fick's First Law - Diffusive flux proportional to concentration gradient

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_fick_first_law(D: float, dC_dx: float) -> float:
    """
    Calculate diffusive flux from concentration gradient.

    Formula: J_S = -D(∂C/∂x)

    Parameters:
    -----------
    D : float - Diffusion coefficient (m²/s)
    dC_dx : float - Concentration gradient (mol/m⁴)

    Returns:
    --------
    J_S : float - Diffusive flux (mol/(m²·s))
    """
    return -D * dC_dx


# Create and register atomic equation
fick_first_law = create_equation(
    id="fick_first_law",
    output_units='mol/(m^2*s)',
    name="Fick's First Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"J_S = -D\frac{\partial C}{\partial x}",
    simplified="J_S = -D * (dC/dx)",
    description="Diffusive flux proportional to concentration gradient - negative sign means flow down gradient",
    compute_func=compute_fick_first_law,
    parameters=[
        Parameter(
            name="D",
            description="Diffusion coefficient",
            units="m²/s",
            symbol="D",
            physiological_range=(1e-11, 1e-8)  # proteins to small ions
        ),
        Parameter(
            name="dC_dx",
            description="Concentration gradient",
            units="mol/m⁴",
            symbol=r"\frac{\partial C}{\partial x}",
            physiological_range=(-1e6, 1e6)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.3")
)

register_equation(fick_first_law)

"""
Stokes-Einstein Equation - Diffusion coefficient for spherical particles

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)


def compute_stokes_einstein(T: float, eta: float, a: float, k_B: float = 1.38e-23) -> float:
    """
    Calculate diffusion coefficient for spherical particle.

    Formula: D = kT/(6πηa)

    Parameters:
    -----------
    T : float - Temperature (K)
    eta : float - Viscosity (Pa·s)
    a : float - Particle radius (m)
    k_B : float - Boltzmann constant (J/K)

    Returns:
    --------
    D : float - Diffusion coefficient (m²/s)
    """
    return (k_B * T) / (6 * np.pi * eta * a)


# Create and register atomic equation
stokes_einstein = create_equation(
    id="stokes_einstein",
    output_units='m^2/s',
    name="Stokes-Einstein Equation",
    category=EquationCategory.FOUNDATIONS,
    latex=r"D = \frac{kT}{6\pi\eta a}",
    simplified="D = (k*T) / (6*pi*eta*a)",
    description="Diffusion coefficient for spherical particle - inversely proportional to particle size",
    compute_func=compute_stokes_einstein,
    parameters=[
        Parameter(
            name="T",
            description="Temperature",
            units="K",
            symbol="T",
            default_value=310.0,
            physiological_range=(273.0, 320.0)
        ),
        Parameter(
            name="eta",
            description="Fluid viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=7e-4,  # water at 37°C
            physiological_range=(1e-4, 1e-2)
        ),
        Parameter(
            name="a",
            description="Particle radius",
            units="m",
            symbol="a",
            physiological_range=(1e-10, 1e-7)  # ions to proteins
        ),
        PHYSICAL_CONSTANTS["k_B"]
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.3")
)

register_equation(stokes_einstein)

__all__ = ['fick_first_law', 'stokes_einstein', 'diffusion_time']


# --- coverage pass additions (Feher extraction) ---

def compute_convection_diffusion_flux(D, dC_dx, J_V, C):
    """Convection-diffusion flux: J_S = -D*(dC/dx) + J_V*C (Feher Eqn 1.6.36, sec 'External forces can move particles and alter the flux'). First term is Fickian diffusive flux; second term J_V*C is solute carried by solvent drag (bulk fluid flow). SI units: mol/(m^2*s)."""
    return -D * dC_dx + J_V * C

convection_diffusion_flux = create_equation(
    id='convection_diffusion_flux',
    output_units='mol/(m^2*s)',
    name='Convection-Diffusion Equation',
    category=EquationCategory.FOUNDATIONS,
    latex='J_S = -D\\frac{\\partial C}{\\partial x} + J_V C',
    simplified='J_S = -D*(dC/dx) + J_V*C',
    description='Convection-diffusion equation: total one-dimensional solute flux when diffusion and bulk fluid flow (convection / solvent drag) act simultaneously. The first term is the Fickian diffusive flux (down the concentration gradient); the second term J_V*C is the solute carried by solvent drag, where J_V is the volume flux (fluid velocity) times concentration. This is the physical basis of solute transport by solvent drag across capillary walls and renal tubular epithelia.',
    compute_func=compute_convection_diffusion_flux,
    parameters=[
        Parameter(name='D', description='Diffusion coefficient', units='m²/s', symbol='D', physiological_range=(1e-11, 1e-08)),
        Parameter(name='dC_dx', description='Concentration gradient', units='mol/m⁴', symbol='\\frac{\\partial C}{\\partial x}', physiological_range=(-1000000, 1000000)),
        Parameter(name='J_V', description='Volume flux, i.e. velocity of bulk (solvent-drag) fluid flow across the area', units='m/s', symbol='J_V', physiological_range=(-1, 1)),
        Parameter(name='C', description='Solute concentration', units='mol/m³', symbol='C', physiological_range=(0, 10000)),
    ],
    depends_on=["volume_flux"],
    metadata=EquationMetadata(source_unit=1, source_chapter='1.6',
                              source_section='EXTERNAL FORCES CAN MOVE PARTICLES AND ALTER THE FLUX', page_reference=None,
                              textbook_equation_number='1.6.36'),
)
register_equation(convection_diffusion_flux)

try:
    __all__ += ['convection_diffusion_flux']
except NameError:
    __all__ = ['convection_diffusion_flux']

"""Transport equations - Pressure-driven flow and bulk transport.

Includes:
- Volume and solute flux definitions
- Hydrostatic pressure
- Poiseuille's law (laminar flow)
- Hydraulic resistance
- Law of Laplace (cylinder and sphere)"""

"""
Hydraulic Resistance - Resistance to fluid flow

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_hydraulic_resistance(eta: float, L: float, r: float) -> float:
    """
    Calculate hydraulic resistance of a cylindrical tube.

    Formula: R = 8ηL/(πr⁴)

    Parameters:
    -----------
    eta : float - Fluid viscosity (Pa·s)
    L : float - Tube length (m)
    r : float - Tube radius (m)

    Returns:
    --------
    R : float - Hydraulic resistance (Pa·s/m³)
    """
    return (8 * eta * L) / (np.pi * r**4)


def compute_flow_from_resistance(delta_P: float, R: float) -> float:
    """
    Calculate flow from pressure difference and resistance.

    Formula: Q_V = ΔP/R (analogous to Ohm's law)

    Parameters:
    -----------
    delta_P : float - Pressure difference (Pa)
    R : float - Hydraulic resistance (Pa·s/m³)

    Returns:
    --------
    Q_V : float - Volume flow rate (m³/s)
    """
    return delta_P / R


# Create and register atomic equation
hydraulic_resistance = create_equation(
    id="hydraulic_resistance",
    output_units='Pa*s/m^3',
    name="Hydraulic Resistance",
    category=EquationCategory.FOUNDATIONS,
    latex=r"R = \frac{8\eta L}{\pi r^4}",
    simplified="R = (8 * eta * L) / (pi * r^4)",
    description="Resistance to fluid flow - analogous to electrical resistance",
    compute_func=compute_hydraulic_resistance,
    parameters=[
        Parameter(
            name="eta",
            description="Fluid viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=3.5e-3,
            physiological_range=(1e-3, 1e-2)
        ),
        Parameter(
            name="L",
            description="Tube length",
            units="m",
            symbol="L",
            physiological_range=(1e-6, 1.0)
        ),
        Parameter(
            name="r",
            description="Tube radius",
            units="m",
            symbol="r",
            physiological_range=(1e-6, 1e-2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(hydraulic_resistance)

"""
Hydrostatic Pressure - Pressure at depth in fluid

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_hydrostatic_pressure(rho: float, g: float, h: float) -> float:
    """
    Calculate hydrostatic pressure at depth h in fluid.

    Formula: P = ρgh

    Parameters:
    -----------
    rho : float - Fluid density (kg/m³)
    g : float - Gravitational acceleration (m/s²)
    h : float - Height of fluid column (m)

    Returns:
    --------
    P : float - Pressure (Pa)
    """
    return rho * g * h


# Create and register atomic equation
hydrostatic_pressure = create_equation(
    id="hydrostatic_pressure",
    output_units='Pa',
    name="Hydrostatic Pressure",
    category=EquationCategory.FOUNDATIONS,
    latex=r"P = \rho g h",
    simplified="P = rho * g * h",
    description="Pressure at depth h in fluid column",
    compute_func=compute_hydrostatic_pressure,
    parameters=[
        Parameter(
            name="rho",
            description="Fluid density",
            units="kg/m³",
            symbol=r"\rho",
            default_value=1055.0,  # blood density
            physiological_range=(1000.0, 1100.0)
        ),
        Parameter(
            name="g",
            description="Gravitational acceleration",
            units="m/s²",
            symbol="g",
            default_value=9.8,
            physiological_range=(9.8, 9.8)
        ),
        Parameter(
            name="h",
            description="Height of fluid column",
            units="m",
            symbol="h",
            physiological_range=(0.0, 2.0)  # max ~2m for human height
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(hydrostatic_pressure)

"""
Law of Laplace (Cylinder) - Wall tension in blood vessels

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_laplace_cylinder_pressure(T: float, r: float) -> float:
    """
    Calculate transmural pressure from wall tension (cylinder geometry).

    Formula: ΔP = T/r

    Parameters:
    -----------
    T : float - Wall tension (N/m)
    r : float - Vessel radius (m)

    Returns:
    --------
    delta_P : float - Transmural pressure (Pa)
    """
    return T / r


def compute_laplace_cylinder_tension(delta_P: float, r: float) -> float:
    """
    Calculate wall tension from transmural pressure (cylinder geometry).

    Formula: T = ΔP × r

    Parameters:
    -----------
    delta_P : float - Transmural pressure (Pa)
    r : float - Vessel radius (m)

    Returns:
    --------
    T : float - Wall tension (N/m)
    """
    return delta_P * r


# Create and register atomic equation
laplace_cylinder = create_equation(
    id="laplace_cylinder",
    output_units='Pa',
    name="Law of Laplace (Cylinder)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\Delta P = \frac{T}{r} \quad \text{or} \quad T = \Delta P \times r",
    simplified="delta_P = T / r  or  T = delta_P * r",
    description="Relates wall tension to transmural pressure in cylindrical vessels (e.g., blood vessels)",
    compute_func=compute_laplace_cylinder_pressure,
    parameters=[
        Parameter(
            name="T",
            description="Wall tension",
            units="N/m",
            symbol="T",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="r",
            description="Vessel radius",
            units="m",
            symbol="r",
            physiological_range=(1e-6, 1e-2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(laplace_cylinder)

"""
Law of Laplace (Sphere) - Wall tension in alveoli and cells

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_laplace_sphere_pressure(T: float, r: float) -> float:
    """
    Calculate transmural pressure from wall tension (sphere geometry).

    Formula: ΔP = 2T/r

    Parameters:
    -----------
    T : float - Surface tension (N/m)
    r : float - Sphere radius (m)

    Returns:
    --------
    delta_P : float - Transmural pressure (Pa)
    """
    return 2 * T / r


def compute_laplace_sphere_tension(delta_P: float, r: float) -> float:
    """
    Calculate surface tension from transmural pressure (sphere geometry).

    Formula: T = ΔP × r/2

    Parameters:
    -----------
    delta_P : float - Transmural pressure (Pa)
    r : float - Sphere radius (m)

    Returns:
    --------
    T : float - Surface tension (N/m)
    """
    return delta_P * r / 2


# Create and register atomic equation
laplace_sphere = create_equation(
    id="laplace_sphere",
    output_units='Pa',
    name="Law of Laplace (Sphere)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\Delta P = \frac{2T}{r} \quad \text{or} \quad T = \frac{\Delta P \times r}{2}",
    simplified="delta_P = 2*T / r  or  T = delta_P * r / 2",
    description="Relates surface tension to transmural pressure in spherical structures (e.g., alveoli, cells)",
    compute_func=compute_laplace_sphere_pressure,
    parameters=[
        Parameter(
            name="T",
            description="Surface tension",
            units="N/m",
            symbol="T",
            physiological_range=(0.0, 0.1)  # surfactant reduces to ~0.025 N/m
        ),
        Parameter(
            name="r",
            description="Sphere radius",
            units="m",
            symbol="r",
            physiological_range=(1e-7, 1e-3)  # cells to alveoli
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(laplace_sphere)

"""
Poiseuille's Law - Laminar flow through cylindrical tube

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_poiseuille_flow(r: float, eta: float, delta_P: float, L: float) -> float:
    """
    Calculate volume flow rate through cylindrical tube.

    Formula: Q_V = (πr⁴/8η) × (ΔP/L)

    Parameters:
    -----------
    r : float - Tube radius (m)
    eta : float - Fluid viscosity (Pa·s)
    delta_P : float - Pressure difference (Pa)
    L : float - Tube length (m)

    Returns:
    --------
    Q_V : float - Volume flow rate (m³/s)
    """
    return (np.pi * r**4 / (8 * eta)) * (delta_P / L)


# Create and register atomic equation
poiseuille_flow = create_equation(
    id="poiseuille_flow",
    output_units='m^3/s',
    name="Poiseuille's Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"Q_V = \frac{\pi r^4}{8\eta} \cdot \frac{\Delta P}{L}",
    simplified="Q_V = (pi * r^4 / (8 * eta)) * (delta_P / L)",
    description="Laminar flow through cylindrical tube - flow proportional to r⁴",
    compute_func=compute_poiseuille_flow,
    parameters=[
        Parameter(
            name="r",
            description="Tube radius",
            units="m",
            symbol="r",
            physiological_range=(1e-6, 1e-2)  # capillary to aorta
        ),
        Parameter(
            name="eta",
            description="Fluid viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=3.5e-3,  # blood viscosity
            physiological_range=(1e-3, 1e-2)
        ),
        Parameter(
            name="delta_P",
            description="Pressure difference",
            units="Pa",
            symbol=r"\Delta P",
            physiological_range=(0.0, 20000.0)  # up to ~150 mmHg
        ),
        Parameter(
            name="L",
            description="Tube length",
            units="m",
            symbol="L",
            physiological_range=(1e-6, 1.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(poiseuille_flow)

"""
Solute Flux - Amount of solute per unit area per unit time

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_solute_flux(Q_S: float, A: float) -> float:
    """
    Calculate solute flux from solute flow rate and area.

    Formula: J_S = Q_S / A

    Parameters:
    -----------
    Q_S : float - Solute flow rate (mol/s)
    A : float - Cross-sectional area (m²)

    Returns:
    --------
    J_S : float - Solute flux (mol/(m²·s))
    """
    return Q_S / A


# Create and register atomic equation
solute_flux = create_equation(
    id="solute_flux",
    output_units='mol/(m^2*s)',
    name="Solute Flux",
    category=EquationCategory.FOUNDATIONS,
    latex=r"J_S = \frac{Q_S}{A}",
    simplified="J_S = Q_S / A",
    description="Amount of solute per unit area per unit time",
    compute_func=compute_solute_flux,
    parameters=[
        Parameter(
            name="Q_S",
            description="Solute flow rate",
            units="mol/s",
            symbol=r"Q_S",
            physiological_range=(0.0, 1e-3)
        ),
        Parameter(
            name="A",
            description="Cross-sectional area",
            units="m²",
            symbol="A",
            physiological_range=(1e-12, 1e-3)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(solute_flux)

"""
Volume Flux - Volume flowing per unit area per unit time

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_volume_flux(Q_V: float, A: float) -> float:
    """
    Calculate volume flux from volume flow rate and area.

    Formula: J_V = Q_V / A

    Parameters:
    -----------
    Q_V : float - Volume flow rate (m³/s)
    A : float - Cross-sectional area (m²)

    Returns:
    --------
    J_V : float - Volume flux (m/s)
    """
    return Q_V / A


# Create and register atomic equation
volume_flux = create_equation(
    id="volume_flux",
    output_units='m/s',
    name="Volume Flux",
    category=EquationCategory.FOUNDATIONS,
    latex=r"J_V = \frac{Q_V}{A}",
    simplified="J_V = Q_V / A",
    description="Volume flowing per unit area per unit time",
    compute_func=compute_volume_flux,
    parameters=[
        Parameter(
            name="Q_V",
            description="Volume flow rate",
            units="m³/s",
            symbol=r"Q_V",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="A",
            description="Cross-sectional area",
            units="m²",
            symbol="A",
            physiological_range=(1e-12, 1e-3)  # from capillary to aorta
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.1")
)

register_equation(volume_flux)

__all__ = ['volume_flux', 'solute_flux', 'hydrostatic_pressure', 'poiseuille_flow', 'hydraulic_resistance', 'laplace_cylinder', 'laplace_sphere']


# --- coverage pass additions (Feher extraction) ---

def compute_volume_of_distribution(m, C):
    """Volume of distribution by the Fick indicator-dilution principle: V = m / C.

    Feher 1.5, section 'Calculation of Fluid Volumes by the Fick Dilution
    Principle'. A known amount of indicator m is injected, allowed to distribute
    and equilibrate in an unknown fluid compartment; its equilibrium concentration
    C is then measured in a sample, and the compartment (distribution) volume is
    V = m / C. Stated by Feher as a rearrangement of the concentration definition
    C = m/V (Eq. 1.5.1) solved for V. Any self-consistent unit set works; SI here:
    m in kg, C in kg/m^3 -> V in m^3.
    """
    return m / C

volume_of_distribution = create_equation(
    id='volume_of_distribution',
    output_units='m^3',
    name='Volume of Distribution (Fick Indicator-Dilution Principle)',
    category=EquationCategory.FOUNDATIONS,
    latex='V = \\frac{m}{C}',
    simplified='V = m / C',
    description='Volume of distribution of an indicator (the Fick dilution principle): the fluid-compartment volume in which a known injected amount of indicator distributes, computed from the amount introduced (m) and its equilibrium concentration (C). It is the standard method for measuring body fluid volumes by indicator dilution (plasma volume with Evans Blue, ECF with inulin/mannitol, total body water with deuterium) and is the basis of the pharmacokinetic volume of distribution. Feher states it as a rearrangement of the concentration definition C = m/V (Eq. 1.5.1) solved for V.',
    compute_func=compute_volume_of_distribution,
    parameters=[
        Parameter(name='m', description='Amount of indicator/solute introduced into the compartment (e.g. mass of Evans Blue injected)', units='kg', symbol='m', default_value=1e-05, physiological_range=(1e-12, 1)),
        Parameter(name='C', description='Equilibrium concentration of the indicator measured in a sample after mixing', units='kg/m^3', symbol='C', default_value=0.004, physiological_range=(1e-09, 1000)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter='1.5',
                              source_section='CALCULATION OF FLUID VOLUMES BY THE FICK DILUTION PRINCIPLE', page_reference=None,
                              textbook_equation_number='1.5.1'),
)
register_equation(volume_of_distribution)

try:
    __all__ += ['volume_of_distribution']
except NameError:
    __all__ = ['volume_of_distribution']

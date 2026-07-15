"""Membrane structure equations - capacitance and permeability."""

"""
Membrane Capacitance - Capacitance of lipid bilayer membrane

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np

def compute_membrane_capacitance(epsilon_m: float = 2.5, delta: float = 4e-9) -> float:
    """
    Calculate membrane capacitance per unit area.

    Formula: C_m = ε_m × ε_0 / δ

    Parameters:
    -----------
    epsilon_m : float
        Membrane dielectric constant (dimensionless), typical: 2-3
    delta : float
        Membrane thickness (m), typical: 4-5 nm

    Returns:
    --------
    C_m : float
        Membrane capacitance (F/m²)
        Typical value: ~0.01 F/m² = 1 μF/cm²
    """
    epsilon_0 = 8.85e-12  # Permittivity of free space (F/m)
    return epsilon_m * epsilon_0 / delta


# Create and register atomic equation
membrane_capacitance = create_equation(
    id="membrane_capacitance",
    output_units='F/m^2',
    name="Membrane Capacitance",
    category=EquationCategory.MEMBRANE,
    latex=r"C_m = \frac{\varepsilon_m \varepsilon_0}{\delta}",
    simplified="C_m = (epsilon_m * epsilon_0) / delta",
    description="Capacitance of lipid bilayer membrane per unit area, arising from charge separation across the thin insulating membrane.",
    compute_func=compute_membrane_capacitance,
    parameters=[
        Parameter(
            name="epsilon_m",
            description="Membrane dielectric constant",
            units="dimensionless",
            symbol=r"\varepsilon_m",
            default_value=2.5,
            physiological_range=(2.0, 3.0)
        ),
        Parameter(
            name="delta",
            description="Membrane thickness (hydrophobic core)",
            units="m",
            symbol=r"\delta",
            default_value=4e-9,
            physiological_range=(3e-9, 5e-9)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.1")
)

register_equation(membrane_capacitance)

"""
Permeability Coefficient - Rate of passive diffusion across membrane

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)

def compute_permeability_coefficient(D: float, K: float, delta: float) -> float:
    """
    Calculate membrane permeability coefficient.

    Formula: P = D × K / δ

    Parameters:
    -----------
    D : float
        Diffusion coefficient in membrane (m²/s)
    K : float
        Partition coefficient (membrane/water concentration ratio)
    delta : float
        Membrane thickness (m)

    Returns:
    --------
    P : float
        Permeability coefficient (m/s)

    Typical values:
        H₂O: 10⁻⁴ m/s (10⁻² cm/s)
        Urea: 10⁻⁸ m/s (10⁻⁶ cm/s)
        Glucose: 10⁻⁹ m/s (10⁻⁷ cm/s)
        Na⁺: 10⁻¹⁴ m/s (10⁻¹² cm/s)
        Cl⁻: 10⁻¹³ m/s (10⁻¹¹ cm/s)
    """
    return D * K / delta


# Create and register atomic equation
permeability_coefficient = create_equation(
    id="permeability_coefficient",
    output_units='m/s',
    name="Permeability Coefficient",
    category=EquationCategory.MEMBRANE,
    latex=r"P = \frac{D \cdot K}{\delta}",
    simplified="P = (D * K) / delta",
    description="Permeability coefficient determining the rate of passive diffusion across a membrane, combining diffusion within the membrane and partitioning into the membrane.",
    compute_func=compute_permeability_coefficient,
    parameters=[
        Parameter(
            name="D",
            description="Diffusion coefficient in membrane",
            units="m²/s",
            symbol="D",
            default_value=None
        ),
        Parameter(
            name="K",
            description="Partition coefficient (membrane/water)",
            units="dimensionless",
            symbol="K",
            default_value=None
        ),
        Parameter(
            name="delta",
            description="Membrane thickness",
            units="m",
            symbol=r"\delta",
            default_value=4e-9
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.1")
)

register_equation(permeability_coefficient)

__all__ = ['membrane_capacitance', 'permeability_coefficient']


# --- coverage pass additions (Feher extraction) ---

def compute_surface_pressure(gamma_0, gamma):
    """Apparent surface pressure of an amphipathic monolayer (Feher §2.5, Eqn 2.5.2): pi = gamma_0 - gamma.

    All quantities in SI (N/m). Surface pressure has the same units as surface tension.

    Parameters:
    -----------
    gamma_0 : float
        Surface tension of the clean (lipid-free) air-water surface (N/m).
    gamma : float
        Surface tension of the air-water surface in the presence of the monolayer (N/m).

    Returns:
    --------
    pi : float
        Surface pressure (N/m).
    """
    return gamma_0 - gamma

surface_pressure = create_equation(
    id='surface_pressure',
    output_units='N/m',
    name='Surface Pressure',
    category=EquationCategory.MEMBRANE,
    latex='\\pi = \\gamma_0 - \\gamma',
    simplified='pi = gamma_0 - gamma',
    description='Apparent surface pressure exerted by an amphipathic (lipid) monolayer spread on an air-water interface, defined as the reduction in surface tension relative to the clean surface. When amphipathic molecules are squeezed to the surface they lower the surface tension, so a movable Langmuir-trough barrier feels a net force toward the clean surface; the resulting apparent pressure is pi = gamma_0 - gamma. Foundational for surfactant/monolayer (Langmuir-trough) biophysics.',
    compute_func=compute_surface_pressure,
    parameters=[
        Parameter(name='gamma_0', description='Surface tension of the clean (lipid-free) air-water surface', units='N/m', symbol='\\gamma_0', physiological_range=(0.05, 0.08)),
        Parameter(name='gamma', description='Surface tension of the air-water surface in the presence of the amphipathic (lipid) monolayer', units='N/m', symbol='\\gamma', physiological_range=(0, 0.075)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter='2.5',
                              source_section='AMPHIPATHIC MOLECULES SPREAD OVER A WATER SURFACE, REDUCE SURFACE TENSION, AND PRODUCE AN APPARENT SURFACE PRESSURE', page_reference=None,
                              textbook_equation_number='2.5.2'),
)
register_equation(surface_pressure)


def compute_surface_free_energy(gamma, dA):
    """Change in surface (Gibbs) free energy for a change in interfacial area.

    Feher Eqn 2.5.1 (§2.5, air-water surface tension): dG = gamma * dA.
    Defines surface tension gamma as the free-energy cost per unit increase in
    interfacial area. Units: gamma in N/m (= J/m^2), dA in m^2, returns dG in J.
    """
    return gamma * dA

surface_free_energy = create_equation(
    id='surface_free_energy',
    output_units='J',
    name='Surface Free Energy',
    category=EquationCategory.MEMBRANE,
    latex='\\mathrm{d}G = \\gamma\\,\\mathrm{d}A',
    simplified='dG = gamma * dA',
    description="Change in surface (Gibbs) free energy when the area of an air-water interface changes. Defines surface tension gamma as the free-energy cost per unit increase in interfacial area; because promoting water molecules to the surface raises their energy, expanding the surface costs energy proportional to the area added. Underlies surfactant/monolayer behaviour (surface pressure), lipid-bilayer self-assembly, and the surface-energy basis of Laplace's law.",
    compute_func=compute_surface_free_energy,
    parameters=[
        Parameter(name='gamma', description='Surface tension of the air-water interface (free energy per unit area); ~0.072 N/m for clean water, lowered by surfactant/monolayers', units='N/m', symbol='\\gamma', physiological_range=(0, 0.15)),
        Parameter(name='dA', description='Increment in interfacial (surface) area', units='m^2', symbol='\\mathrm{d}A', physiological_range=(0, 1)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter='2.5',
                              source_section='SURFACE TENSION OF THE AIR–WATER INTERFACE RESULTS FROM ASYMMETRIC FORCES', page_reference=None,
                              textbook_equation_number='2.5.1'),
)
register_equation(surface_free_energy)


def compute_partition_coefficient(C_lipid, C_water):
    """Partition (distribution) coefficient k_s = equilibrium concentration in the lipid phase / equilibrium concentration in the aqueous (water) phase.

    Feher, Quantitative Human Physiology 3rd ed., section 2.6 (Passive Transport and
    Facilitated Diffusion), 'Dissolution-Diffusion in the Lipid Bilayer' model, Eq. (2.6.11);
    the partition-coefficient concept is originally introduced in Chapter 2.4. Both
    concentrations must be in the SAME units (e.g. mol/m^3); the result is dimensionless.
    C_water must be > 0.
    """
    return C_lipid / C_water

partition_coefficient = create_equation(
    id='partition_coefficient',
    output_units='dimensionless',
    name='Partition Coefficient',
    category=EquationCategory.MEMBRANE,
    latex='k_{s} = \\dfrac{C_{\\mathrm{eq,\\,lipid}}}{C_{\\mathrm{eq,\\,water}}}',
    simplified='k_s = C_lipid / C_water',
    description="Partition (distribution) coefficient: the ratio of a solute's equilibrium concentration in the membrane lipid phase to its equilibrium concentration in the adjacent aqueous phase. Quantifies lipid solubility in the dissolution-diffusion model of passive transport; it is the K that scales membrane permeability (P = k_s * D_lipid / delta) and underlies Overton's rules (permeability proportional to lipid solubility, inversely proportional to molecular size). Dimensionless; larger k_s means greater lipophilicity and higher passive membrane permeability. Reused across the corpus as the blood:gas / oil:water / oil:gas partition (Meyer-Overton) coefficient.",
    compute_func=compute_partition_coefficient,
    parameters=[
        Parameter(name='C_lipid', description='Equilibrium solute concentration in the membrane lipid phase', units='mol/m^3', symbol='C_{lipid}'),
        Parameter(name='C_water', description='Equilibrium solute concentration in the adjacent aqueous (water) phase; must be > 0', units='mol/m^3', symbol='C_{water}'),
    ],
    depends_on=[],
    produces='k_s',
    metadata=EquationMetadata(source_unit=2, source_chapter='2.6',
                              source_section='DISSOLUTION-DIFFUSION IN THE LIPID BILAYER IS ANOTHER MODEL FOR PASSIVE TRANSPORT', page_reference=None,
                              textbook_equation_number='2.6.11'),
)
register_equation(partition_coefficient)

try:
    __all__ += ['surface_pressure', 'surface_free_energy', 'partition_coefficient']
except NameError:
    __all__ = ['surface_pressure', 'surface_free_energy', 'partition_coefficient']

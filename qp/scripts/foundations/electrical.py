"""Electrical equations - Electrostatic forces and membrane capacitance.

Includes:
- Coulomb's law (vacuum and medium)
- Electric field
- Capacitance
- Parallel plate capacitor (membrane model)"""

"""
Capacitance - Charge storage capacity

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_capacitance(Q: float, V: float) -> float:
    """
    Calculate capacitance from charge and voltage.

    Formula: C = Q/V

    Parameters:
    -----------
    Q : float - Stored charge (C)
    V : float - Voltage difference (V)

    Returns:
    --------
    C : float - Capacitance (F)
    """
    return Q / V


# Create and register atomic equation
capacitance = create_equation(
    id="capacitance",
    output_units='F',
    name="Capacitance",
    category=EquationCategory.FOUNDATIONS,
    latex=r"C = \frac{Q}{V}",
    simplified="C = Q / V",
    description="Capacitance definition - charge per unit voltage",
    compute_func=compute_capacitance,
    parameters=[
        Parameter(
            name="Q",
            description="Stored charge",
            units="C",
            symbol="Q",
            physiological_range=(0.0, 1e-9)
        ),
        Parameter(
            name="V",
            description="Voltage difference",
            units="V",
            symbol="V",
            physiological_range=(0.0, 0.2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(capacitance)

"""
Coulomb's Law - Electrostatic force between point charges

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_coulomb_force(q1: float, q2: float, r: float, epsilon_0: float = 8.85e-12) -> float:
    """
    Calculate electrostatic force between two point charges.

    Formula: F = (q₁q₂)/(4πε₀r²)

    Parameters:
    -----------
    q1 : float - Charge 1 (C)
    q2 : float - Charge 2 (C)
    r : float - Separation distance (m)
    epsilon_0 : float - Permittivity of free space (C²/(J·m))

    Returns:
    --------
    F : float - Electrostatic force (N)
    """
    return (q1 * q2) / (4 * np.pi * epsilon_0 * r**2)


# Create and register atomic equation
coulomb_law = create_equation(
    id="coulomb_law",
    output_units='N',
    name="Coulomb's Law",
    category=EquationCategory.FOUNDATIONS,
    latex=r"F = \frac{q_1 q_2}{4\pi\epsilon_0 r^2}",
    simplified="F = (q1 * q2) / (4 * pi * epsilon_0 * r^2)",
    description="Electrostatic force between point charges in vacuum",
    compute_func=compute_coulomb_force,
    parameters=[
        Parameter(
            name="q1",
            description="Charge 1",
            units="C",
            symbol=r"q_1",
            physiological_range=(-1e-15, 1e-15)
        ),
        Parameter(
            name="q2",
            description="Charge 2",
            units="C",
            symbol=r"q_2",
            physiological_range=(-1e-15, 1e-15)
        ),
        Parameter(
            name="r",
            description="Separation distance",
            units="m",
            symbol="r",
            physiological_range=(1e-10, 1e-6)
        ),
        Parameter(
            name="epsilon_0",
            description="Permittivity of free space",
            units="C²/(J·m)",
            symbol=r"\epsilon_0",
            default_value=8.85e-12
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(coulomb_law)

"""
Coulomb's Law in Medium - Electrostatic force in dielectric medium

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_coulomb_force_medium(q1: float, q2: float, r: float, epsilon: float,
                                epsilon_0: float = 8.85e-12) -> float:
    """
    Calculate electrostatic force in a dielectric medium.

    Formula: F = (q₁q₂)/(4πεε₀r²)

    Parameters:
    -----------
    q1 : float - Charge 1 (C)
    q2 : float - Charge 2 (C)
    r : float - Separation distance (m)
    epsilon : float - Relative permittivity (dielectric constant)
    epsilon_0 : float - Permittivity of free space (C²/(J·m))

    Returns:
    --------
    F : float - Electrostatic force (N)
    """
    return (q1 * q2) / (4 * np.pi * epsilon * epsilon_0 * r**2)


# Create and register atomic equation
coulomb_law_medium = create_equation(
    id="coulomb_law_medium",
    output_units='N',
    name="Coulomb's Law in Medium",
    category=EquationCategory.FOUNDATIONS,
    latex=r"F = \frac{q_1 q_2}{4\pi\epsilon\epsilon_0 r^2}",
    simplified="F = (q1 * q2) / (4 * pi * epsilon * epsilon_0 * r^2)",
    description="Electrostatic force between charges in dielectric medium (e.g., water, ε≈80)",
    compute_func=compute_coulomb_force_medium,
    parameters=[
        Parameter(
            name="q1",
            description="Charge 1",
            units="C",
            symbol=r"q_1",
            physiological_range=(-1e-15, 1e-15)
        ),
        Parameter(
            name="q2",
            description="Charge 2",
            units="C",
            symbol=r"q_2",
            physiological_range=(-1e-15, 1e-15)
        ),
        Parameter(
            name="r",
            description="Separation distance",
            units="m",
            symbol="r",
            physiological_range=(1e-10, 1e-6)
        ),
        Parameter(
            name="epsilon",
            description="Relative permittivity (dielectric constant)",
            units="dimensionless",
            symbol=r"\epsilon",
            default_value=80.0,  # water
            physiological_range=(1.0, 80.0)
        ),
        Parameter(
            name="epsilon_0",
            description="Permittivity of free space",
            units="C²/(J·m)",
            symbol=r"\epsilon_0",
            default_value=8.85e-12
        )
    ],
    depends_on=["coulomb_law"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(coulomb_law_medium)

"""
Electric Field - Force per unit charge

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_electric_field(F: float, q: float) -> float:
    """
    Calculate electric field from force and charge.

    Formula: E = F/q

    Parameters:
    -----------
    F : float - Force on test charge (N)
    q : float - Test charge (C)

    Returns:
    --------
    E : float - Electric field (N/C or V/m)
    """
    return F / q


# Create and register atomic equation
electric_field = create_equation(
    id="electric_field",
    output_units='N/C',
    name="Electric Field",
    category=EquationCategory.FOUNDATIONS,
    latex=r"E = \frac{F}{q} = -\nabla U",
    simplified="E = F / q",
    description="Electric field strength - force per unit charge, points from high to low potential",
    compute_func=compute_electric_field,
    parameters=[
        Parameter(
            name="F",
            description="Force on test charge",
            units="N",
            symbol="F",
            physiological_range=(-1e-12, 1e-12)
        ),
        Parameter(
            name="q",
            description="Test charge",
            units="C",
            symbol="q",
            physiological_range=(1e-19, 1e-15)
        )
    ],
    depends_on=["coulomb_law"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(electric_field)

"""
Parallel Plate Capacitor - Membrane capacitance model

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_parallel_plate_capacitance(epsilon: float, epsilon_0: float, A: float, d: float) -> float:
    """
    Calculate capacitance of parallel plate capacitor.

    Formula: C = εε₀A/d

    Parameters:
    -----------
    epsilon : float - Relative permittivity
    epsilon_0 : float - Permittivity of free space (C²/(J·m))
    A : float - Plate area (m²)
    d : float - Separation distance (m)

    Returns:
    --------
    C : float - Capacitance (F)
    """
    return epsilon * epsilon_0 * A / d


# Create and register atomic equation
parallel_plate_capacitor = create_equation(
    id="parallel_plate_capacitor",
    output_units='F',
    name="Parallel Plate Capacitor",
    category=EquationCategory.FOUNDATIONS,
    latex=r"C = \frac{\epsilon\epsilon_0 A}{d}",
    simplified="C = (epsilon * epsilon_0 * A) / d",
    description="Membrane as capacitor - typical membrane capacitance ~1 μF/cm²",
    compute_func=compute_parallel_plate_capacitance,
    parameters=[
        Parameter(
            name="epsilon",
            description="Relative permittivity of membrane",
            units="dimensionless",
            symbol=r"\epsilon",
            default_value=3.0,  # lipid bilayer
            physiological_range=(2.0, 5.0)
        ),
        Parameter(
            name="epsilon_0",
            description="Permittivity of free space",
            units="C²/(J·m)",
            symbol=r"\epsilon_0",
            default_value=8.85e-12
        ),
        Parameter(
            name="A",
            description="Membrane area",
            units="m²",
            symbol="A",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="d",
            description="Membrane thickness",
            units="m",
            symbol="d",
            default_value=4e-9,  # ~4 nm
            physiological_range=(3e-9, 10e-9)
        )
    ],
    depends_on=["capacitance"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.2")
)

register_equation(parallel_plate_capacitor)

__all__ = ['coulomb_law', 'coulomb_law_medium', 'electric_field', 'capacitance', 'parallel_plate_capacitor']


# --- coverage pass additions (Feher extraction) ---

def compute_lennard_jones_potential(epsilon, sigma, r):
    """Lennard-Jones 12-6 pair potential U(r) in joules for two nonbonding particles (Feher Unit 1 §1.4, 'Close approach of molecules results in a repulsive force: the Lennard-Jones potential'). epsilon = well depth (J); sigma = separation at which U=0 (m); r = interparticle separation (m). r^-12 repulsion, r^-6 attraction; U has a minimum of -epsilon at r = 2**(1/6)*sigma and crosses zero at r = sigma."""
    sr6 = (sigma / r) ** 6
    return 4.0 * epsilon * (sr6 * sr6 - sr6)

lennard_jones_potential = create_equation(
    id='lennard_jones_potential',
    output_units='J',
    name='Lennard-Jones Potential',
    category=EquationCategory.FOUNDATIONS,
    latex='U(r) = 4\\varepsilon\\left[\\left(\\frac{\\sigma}{r}\\right)^{12} - \\left(\\frac{\\sigma}{r}\\right)^{6}\\right] = \\varepsilon\\left[\\left(\\frac{r_m}{r}\\right)^{12} - 2\\left(\\frac{r_m}{r}\\right)^{6}\\right]',
    simplified='U(r) = 4*epsilon*((sigma/r)^12 - (sigma/r)^6)',
    description='Lennard-Jones 12-6 potential: the potential energy of interaction between two nonbonding atoms or molecules as a function of separation r. The r^-12 term models steep repulsion from orbital interpenetration at close approach; the r^-6 term models the attractive van der Waals (London dispersion) tail. The well depth epsilon sets the attraction strength, sigma is the separation where U=0, and the minimum U=-epsilon occurs at r_m = 2^(1/6)*sigma (the equilibrium separation). Used to describe intermolecular forces underlying molecular packing, binding-surface complementarity, and non-covalent interactions in physiology.',
    compute_func=compute_lennard_jones_potential,
    parameters=[
        Parameter(name='epsilon', description='Depth of the potential well; a measure of the strength of the attractive interaction', units='J', symbol='\\varepsilon', physiological_range=(1e-22, 1e-18)),
        Parameter(name='sigma', description='Interparticle separation at which the potential energy is zero (finite-distance zero crossing)', units='m', symbol='\\sigma', physiological_range=(1e-10, 1e-09)),
        Parameter(name='r', description='Center-to-center separation between the two nonbonding particles', units='m', symbol='r', physiological_range=(1e-10, 1e-08)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter='1.4',
                              source_section='CLOSE APPROACH OF MOLECULES RESULTS IN A REPULSIVE FORCE: THE LENNARD-JONES POTENTIAL', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(lennard_jones_potential)


def compute_electric_dipole_moment(q, d):
    """Electric dipole moment magnitude p = q*d (Feher 1.4 'Water has polar bonds'; Appendix 1.4.A1 'The Dipole Moment'). q = magnitude of the separated charge (C); d = charge-separation distance (m); returns p in C*m (1 Debye = 3.33564e-30 C*m)."""
    return q * d

electric_dipole_moment = create_equation(
    id='electric_dipole_moment',
    output_units='C*m',
    name='Electric Dipole Moment',
    category=EquationCategory.FOUNDATIONS,
    latex='\\mathbf{p} = q\\,\\mathbf{d}',
    simplified='p = q * d',
    description='Electric dipole moment magnitude: the product of the separated charge magnitude and the charge-separation distance. Feher 1.4 defines the molecular dipole moment (e.g. water, 1.855 Debye) as p = q d, where p points from the negative to the positive charge. The same relation underlies treating cardiac muscle cells as electric dipoles, the physical basis of the ECG in Unit 5. SI unit is C*m (1 Debye = 3.33564e-30 C*m).',
    compute_func=compute_electric_dipole_moment,
    parameters=[
        Parameter(name='q', description='Magnitude of the separated (partial) charge', units='C', symbol='q', physiological_range=(0, 1e-18)),
        Parameter(name='d', description='Charge-separation distance (magnitude of the vector from the negative to the positive charge)', units='m', symbol='d', physiological_range=(1e-11, 1e-09)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter='1.4',
                              source_section='WATER HAS POLAR BONDS / Appendix 1.4.A1 The Dipole Moment', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(electric_dipole_moment)


def compute_dipole_potential(p, theta, r, kappa=1.0, epsilon_0=8.85e-12):
    """Electric potential of a dipole (Feher 1.4; derived in Appendix 1.4.A1):
    U = p*cos(theta) / (4*pi*epsilon_0*kappa*r**2).
    Units: p [C*m], theta [rad], r [m], kappa dimensionless, epsilon_0 [C^2 N^-1 m^-2]; returns U [V]."""
    return (p * np.cos(theta)) / (4 * np.pi * epsilon_0 * kappa * r**2)

dipole_potential = create_equation(
    id='dipole_potential',
    output_units='V',
    name='Electric Potential of a Dipole',
    category=EquationCategory.FOUNDATIONS,
    latex='U(r,\\theta) = \\frac{p\\,\\cos\\theta}{4\\pi\\varepsilon_0\\,\\kappa\\,r^{2}}',
    simplified='U = p*cos(theta) / (4*pi*epsilon_0*kappa*r^2)',
    description="Electric (scalar) potential U at distance r and orientation angle theta from an electric dipole of moment p, in a medium of dielectric constant kappa. Unlike a point charge's Coulomb potential (proportional to 1/r), the dipole potential falls as 1/r^2 and depends on orientation through cos(theta): at long range the two opposing partial charges nearly cancel, so the interaction weakens rapidly with distance. Obtained by summing the Coulomb potentials of the +q and -q charges in the r>>d limit. Foundational for the dipole model of the heart in electrocardiography and vectorcardiography, since cardiac muscle cells act as electric dipoles. Feher section 1.4, stated in the 'Dipole-Dipole Interactions Are Effective Only Over Short Distances' subsection and derived in Appendix 1.4.A1 (The Dipole Moment).",
    compute_func=compute_dipole_potential,
    parameters=[
        Parameter(name='p', description='Electric dipole moment (p = q*d), the magnitude of the separated-charge dipole', units='C*m', symbol='p', physiological_range=(1e-31, 1)),
        Parameter(name='theta', description='Angle between the dipole axis (moment vector p) and the line from the dipole midpoint to the field point', units='rad', symbol='theta', physiological_range=(0, 6.283185307179586)),
        Parameter(name='r', description='Distance from the dipole center to the point at which the potential is evaluated (r >> d)', units='m', symbol='r', physiological_range=(1e-12, 1)),
        Parameter(name='kappa', description='Dielectric constant of the medium surrounding the dipole (1 for vacuum, ~80 for water)', units='dimensionless', symbol='kappa', default_value=1, physiological_range=(1, 100)),
        Parameter(name='epsilon_0', description='Permittivity of free space (physical constant)', units='C^2 N^-1 m^-2', symbol='epsilon_0', default_value=8.85e-12),
    ],
    depends_on=['coulomb_law'],
    metadata=EquationMetadata(source_unit=1, source_chapter='1.4',
                              source_section='Dipole-Dipole Interactions Are Effective Only Over Short Distances (derived in Appendix 1.4.A1 The Dipole Moment)', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(dipole_potential)

try:
    __all__ += ['lennard_jones_potential', 'electric_dipole_moment', 'dipole_potential']
except NameError:
    __all__ = ['lennard_jones_potential', 'electric_dipole_moment', 'dipole_potential']

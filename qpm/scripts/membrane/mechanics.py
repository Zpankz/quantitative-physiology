"""Membrane / cell mechanics — elasticity and viscoelastic models.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher (Unit 2)
"""
import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation,
)
from scripts.index import register_equation


# --- coverage pass additions (Feher extraction) ---

def compute_youngs_modulus(E, epsilon):
    """Linear-elastic (Hookean) constitutive law - Feher Eq. 2.1.A2.1, Appendix 2.1.A2.

    Mechanical stress developed in a material is proportional to its strain, with
    the proportionality constant being Young's modulus (the coefficient of elasticity).

        sigma = E * epsilon

    where sigma = F/A is the stress and epsilon = dl/l0 is the (dimensionless) strain.
    Valid for small deformations (linear-elastic regime).

    Parameters
    ----------
    E : float
        Young's modulus / elastic modulus (Pa).
    epsilon : float
        Strain, relative change in length dl/l0 (dimensionless).

    Returns
    -------
    float
        Mechanical stress sigma (Pa).
    """
    return E * epsilon

youngs_modulus = create_equation(
    id='youngs_modulus',
    output_units='Pa',
    name="Young's Modulus (Hooke's Law)",
    category=EquationCategory.MEMBRANE,
    latex='\\sigma = E \\varepsilon',
    simplified='sigma = E * epsilon',
    description="Linear-elastic (Hookean) constitutive law defining Young's modulus (the coefficient of elasticity): the mechanical stress sigma = F/A developed in a material is proportional to its strain epsilon = dl/l0, with proportionality constant E. Valid for small deformations. This is the constitutive relation for the elastic ('spring') element underlying cell and tissue viscoelastic models (Kelvin-Voigt, Maxwell, standard-linear-solid) and the material stiffness that feeds arterial pulse-wave-velocity relations (e.g. Moens-Korteweg).",
    compute_func=compute_youngs_modulus,
    parameters=[
        Parameter(name='E', description="Young's modulus (coefficient of elasticity) of the material - ratio of stress to strain in the linear-elastic regime", units='Pa', symbol='E', physiological_range=(1, 1000000000)),
        Parameter(name='epsilon', description='Strain: relative change in length (dl/l0), dimensionless', units='dimensionless', symbol='\\varepsilon', physiological_range=(0, 1)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter='2.1',
                              source_section='Appendix 2.1.A2 Mechanical Properties of Cytoskeletal Elements - Most cells appear to be viscoelastic', page_reference=None,
                              textbook_equation_number='2.1.A2.1'),
)
register_equation(youngs_modulus)


def compute_kelvin_voigt_model(E=20.0, epsilon=0.05, eta=50.0, depsilon_dt=0.02):
    """Total stress of a Kelvin-Voigt viscoelastic solid: a spring (elastic modulus E)
    and a dashpot (viscosity eta) in parallel share the same strain, so their stresses
    add. sigma = E*epsilon + eta*(depsilon/dt). Feher Appendix 2.1.A2, Eq. 2.1.A2.5.
    Units: E [Pa], epsilon [dimensionless], eta [Pa.s], depsilon_dt [1/s] -> sigma [Pa]."""
    return E * epsilon + eta * depsilon_dt

kelvin_voigt_model = create_equation(
    id='kelvin_voigt_model',
    output_units='Pa',
    name='Kelvin-Voigt Viscoelastic Model',
    category=EquationCategory.MEMBRANE,
    latex='\\sigma = E \\varepsilon + \\eta \\frac{d\\varepsilon}{dt}',
    simplified='sigma = E*epsilon + eta*(depsilon/dt)',
    description="Kelvin-Voigt viscoelastic constitutive law: a spring (elastic modulus E) and a dashpot (viscosity eta) connected in parallel share the same strain, so the total stress is the sum of the elastic stress (E*epsilon) and the viscous stress (eta * strain-rate). Feher's canonical model for the viscoelastic behavior of cells and tissues (cytoskeleton). Under a step stress it governs creep (exponential rise of strain to sigma0/E with time constant eta/E) and, when stress is removed, exponential stress-relaxation. Reusable across cell/tissue mechanics problems.",
    compute_func=compute_kelvin_voigt_model,
    parameters=[
        Parameter(name='E', description="Elastic (Young's) modulus of the spring element; ratio of stress to strain for the elastic component. Cell/tissue values span ~10 Pa to ~100 kPa; Feher's worked figure (2.1.A2.2) uses 20 Pa.", units='Pa', symbol='E', default_value=20, physiological_range=(1, 100000)),
        Parameter(name='epsilon', description='Strain (relative deformation, delta_l / l0), dimensionless; valid in the small-deformation linear regime.', units='dimensionless', symbol='epsilon', default_value=0.05, physiological_range=(0, 1)),
        Parameter(name='eta', description="Viscosity of the dashpot (viscous element); ratio of stress to strain rate. Cytoplasm/tissue values span ~1 to ~1000 Pa.s; Feher's figure uses 50 Pa.s. Note this uniaxial viscosity has the same units as, but a different definition from, the shear viscosity used for Poiseuille's law.", units='Pa*s', symbol='eta', default_value=50, physiological_range=(0, 10000)),
        Parameter(name='depsilon_dt', description='Strain rate (time derivative of strain); positive during loading/creep, zero at equilibrium, negative during relaxation.', units='1/s', symbol='depsilon/dt', default_value=0.02, physiological_range=(-100, 100)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter='2.1',
                              source_section='Appendix 2.1.A2 Mechanical Properties of Cytoskeletal Elements - Most cells appear to be viscoelastic', page_reference=None,
                              textbook_equation_number='2.1.A2.5'),
)
register_equation(kelvin_voigt_model)


def compute_maxwell_model(sigma, dsigma_dt=0.0, E=20.0, eta=50.0):
    """Maxwell (series spring-dashpot) viscoelastic constitutive relation.

    Returns the total strain rate depsilon/dt (1/s) of a material modelled as an
    elastic spring (modulus E, Pa) in series with a viscous dashpot (viscosity
    eta, Pa.s), from the applied stress sigma (Pa) and its rate dsigma_dt (Pa/s).
    The elastic strain rate (dsigma_dt / E) and the viscous strain rate
    (sigma / eta) add because the two elements are in series (stress common,
    strains additive). Under constant stress (dsigma_dt = 0) this reduces to
    steady creep at rate sigma / eta. SI units throughout.
    Feher Eq. 2.1.A2.16.
    """
    return dsigma_dt / E + sigma / eta

maxwell_model = create_equation(
    id='maxwell_model',
    output_units='1/s',
    name='Maxwell Viscoelastic Model',
    category=EquationCategory.MEMBRANE,
    latex='\\frac{d\\varepsilon}{dt} = \\frac{1}{E}\\frac{d\\sigma}{dt} + \\frac{\\sigma}{\\eta}',
    simplified='depsilon_dt = dsigma_dt / E + sigma / eta',
    description='Constitutive (governing) equation of the Maxwell viscoelastic model, in which an elastic spring (modulus E) and a viscous dashpot (viscosity eta) are arranged in series. Because the elements are in series the stress is common to both while the strains add, so the total strain rate is the sum of the elastic strain rate (from the rate of change of stress) and the viscous strain rate (from the instantaneous stress). Used to model stress-relaxation and creep of cells and soft tissues; under constant stress it predicts an instantaneous elastic jump (sigma0/E) followed by steady creep at rate sigma0/eta. Distinct from the Kelvin-Voigt (parallel) model.',
    compute_func=compute_maxwell_model,
    parameters=[
        Parameter(name='sigma', description='Applied uniaxial stress (force per unit area) on the material', units='Pa', symbol='\\sigma', physiological_range=(0, 100000)),
        Parameter(name='dsigma_dt', description='Rate of change of applied stress with time (zero for a constant-stress creep test)', units='Pa/s', symbol='\\frac{d\\sigma}{dt}', default_value=0),
        Parameter(name='E', description="Elastic (Young's) modulus of the spring element", units='Pa', symbol='E', default_value=20, physiological_range=(1, 1000000)),
        Parameter(name='eta', description='Viscosity of the dashpot element', units='Pa.s', symbol='\\eta', default_value=50, physiological_range=(1, 100000)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter='2.1',
                              source_section='Appendix 2.1.A2 Mechanical Properties of Cytoskeletal Elements - The Maxwell model arranges elastic and viscous elements in series', page_reference=None,
                              textbook_equation_number='2.1.A2.16'),
)
register_equation(maxwell_model)


def compute_persistence_length(L, l_p):
    """Expected tangent-tangent correlation of a semiflexible polymer.

    Formula: <cos Theta> = exp(-L / l_p)

    Feher, Quantitative Human Physiology 3e, Unit 2, Chapter 2.1 Cell Structure,
    Appendix 2.1.A2 'Mechanical properties of cytoskeletal elements' ->
    'The persistence length describes the thermal stiffness of a polymer'.

    The mean cosine of the angle Theta between the tangent to a polymer at x=0
    and the tangent a contour distance L away decays exponentially with a
    characteristic length constant l_p, the persistence length.

    Parameters
    ----------
    L   : contour distance along the polymer between the two tangents (m)
    l_p : persistence length of the polymer (m)

    Returns
    -------
    cos_theta : expected value <cos Theta>, dimensionless (0..1)
    """
    import math
    return math.exp(-L / l_p)

persistence_length = create_equation(
    id='persistence_length',
    output_units='dimensionless',
    name='Persistence Length (Tangent Correlation)',
    category=EquationCategory.MEMBRANE,
    latex='\\langle \\cos\\Theta \\rangle = e^{-L/l_{p}}',
    simplified='<cos(Theta)> = exp(-L / l_p)',
    description="Worm-like-chain tangent-tangent correlation of a semiflexible polymer (microtubule, actin filament, intermediate filament, DNA). The expected cosine of the angle between the tangent at one point and the tangent a contour distance L further along decays exponentially with the persistence length l_p, which quantifies the polymer's resistance to thermal (Brownian) bending; larger l_p means a stiffer polymer. Used to characterise cytoskeletal element stiffness (microtubule ~1 mm, actin ~17 um, intermediate filament ~1 um).",
    compute_func=compute_persistence_length,
    parameters=[
        Parameter(name='L', description='Contour distance along the polymer between the two tangents', units='m', symbol='L', physiological_range=(1e-09, 0.01)),
        Parameter(name='l_p', description='Persistence length of the polymer (thermal-bending length constant): microtubule ~1e-3 m, actin ~1.7e-5 m, intermediate filament ~1e-6 m', units='m', symbol='l_{p}', physiological_range=(1e-08, 0.01)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter='2.1',
                              source_section='Appendix 2.1.A2 - The persistence length describes the thermal stiffness of a polymer', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(persistence_length)


def compute_poisson_ratio(depsilon_trans, depsilon_axial):
    """Poisson ratio nu = -depsilon_trans/depsilon_axial (dimensionless).

    Feher QHP 3e, Appendix 2.1.A2 (Mechanical Properties of Cytoskeletal
    Elements): 'The Poisson ratio describes how much a material thins when it
    is stretched.' Both inputs are dimensionless strain increments; the output
    nu is dimensionless. The negative sign converts transverse thinning
    (negative depsilon_trans under positive axial stretch) into a positive
    Poisson ratio (rubber ~0.499, single cells ~0.35, cork ~0.0).
    """
    return -depsilon_trans / depsilon_axial

poisson_ratio = create_equation(
    id='poisson_ratio',
    output_units='dimensionless',
    name='Poisson Ratio',
    category=EquationCategory.MEMBRANE,
    latex='\\nu = -\\frac{d\\varepsilon_{trans}}{d\\varepsilon_{axial}}',
    simplified='nu = -depsilon_trans / depsilon_axial',
    description='The Poisson ratio, a dimensionless material property giving the fraction of transverse thinning per unit of axial stretch. Used to characterise the mechanical behaviour of cells and cytoskeletal/biological materials under deformation; nu ~= 0.5 indicates near-incompressibility (rubber 0.499), nu = 0 indicates no transverse change (cork), and single cells are on the order of 0.35.',
    compute_func=compute_poisson_ratio,
    parameters=[
        Parameter(name='depsilon_trans', description='Transverse (perpendicular) strain increment; negative when the material thins under an axial stretch', units='dimensionless', symbol='d\\varepsilon_{trans}', physiological_range=(-1, 1)),
        Parameter(name='depsilon_axial', description='Axial (longitudinal) strain increment along the direction of the applied stress; must be non-zero', units='dimensionless', symbol='d\\varepsilon_{axial}', physiological_range=(-1, 1)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter='2.1',
                              source_section='Appendix 2.1.A2 Mechanical Properties of Cytoskeletal Elements - The Poisson ratio describes how much a material thins when it is stretched', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(poisson_ratio)


def compute_standard_linear_solid(epsilon=0.03, depsilon_dt=0.001, sigma=0.5, E1=20.0, E2=20.0, eta=50.0):
    """Standard linear solid (Zener) viscoelastic constitutive relation, solved for the
    stress rate dsigma/dt.

    The Zener model is a parallel arrangement of an elastic element (modulus E1) and a
    Maxwell element (an elastic element E2 in series with a dashpot of viscosity eta).
    Feher Eq. 2.1.A2.28 states the implicit constitutive relation
        (eta/E2) dsigma/dt + sigma = (eta*(E1+E2)/E2) depsilon/dt + E1*epsilon,
    which, solved for the stress rate, gives the returned expression.

    Units: epsilon [dimensionless strain], depsilon_dt [1/s], sigma [Pa], E1 [Pa],
    E2 [Pa], eta [Pa*s]; returns dsigma/dt [Pa/s].
    """
    return (E1 + E2) * depsilon_dt + (E1 * E2 / eta) * epsilon - (E2 / eta) * sigma

standard_linear_solid = create_equation(
    id='standard_linear_solid',
    output_units='Pa/s',
    name='Standard Linear Solid (Zener) Model',
    category=EquationCategory.MEMBRANE,
    latex='\\frac{\\eta}{E_2}\\frac{d\\sigma}{dt} + \\sigma = \\frac{\\eta(E_1+E_2)}{E_2}\\frac{d\\varepsilon}{dt} + E_1 \\varepsilon',
    simplified='dsigma/dt = (E1 + E2)*(depsilon/dt) + (E1*E2/eta)*epsilon - (E2/eta)*sigma',
    description='Constitutive stress-strain relation of the standard linear solid (Zener) viscoelastic model, a parallel combination of a free elastic element (E1) and a Maxwell element (elastic E2 in series with a dashpot eta). It is the three-parameter model of cytoskeletal/cell viscoelasticity, more realistic than the Kelvin-Voigt or Maxwell models: it shows an instantaneous elastic jump followed by exponential creep/relaxation toward a nonzero equilibrium strain. Here it is written solved for the instantaneous stress rate dsigma/dt given the current strain, strain rate, and stress; integrating it yields the step-load creep response with time constant 1/lambda, lambda = E1*E2/(eta*(E1+E2)).',
    compute_func=compute_standard_linear_solid,
    parameters=[
        Parameter(name='epsilon', description='Total strain of the material (fractional deformation, delta L / L0)', units='dimensionless', symbol='\\varepsilon', default_value=0.03, physiological_range=(0, 1)),
        Parameter(name='depsilon_dt', description='Rate of change of total strain', units='1/s', symbol='d\\varepsilon/dt', default_value=0.001),
        Parameter(name='sigma', description='Total stress on the material (force per unit area, F/A)', units='Pa', symbol='\\sigma', default_value=0.5),
        Parameter(name='E1', description='Elastic modulus of the free (parallel-branch) elastic element', units='Pa', symbol='E_1', default_value=20),
        Parameter(name='E2', description='Elastic modulus of the elastic element within the Maxwell branch', units='Pa', symbol='E_2', default_value=20),
        Parameter(name='eta', description='Viscosity of the dashpot in the Maxwell branch', units='Pa*s', symbol='\\eta', default_value=50),
    ],
    depends_on=[],
    produces='d\\sigma/dt',
    metadata=EquationMetadata(source_unit=2, source_chapter='2.1',
                              source_section='THE STANDARD LINEAR SOLID MODEL COMBINES BOTH SERIES AND PARALLEL ELEMENTS', page_reference=None,
                              textbook_equation_number='2.1.A2.28'),
)
register_equation(standard_linear_solid)

__all__ = ['youngs_modulus', 'kelvin_voigt_model', 'maxwell_model', 'persistence_length', 'poisson_ratio', 'standard_linear_solid']


# --- coverage pass 2 (residual reconsideration) ---

def compute_newtonian_viscosity(eta, strain_rate):
    """Newtonian (dashpot) constitutive relation sigma = eta * d(epsilon)/dt (Feher 2.1 Appendix, Eq 2.1.A2.2): the viscous stress in a linear viscous element is proportional to the strain rate. eta = viscosity (Pa*s), strain_rate = d(epsilon)/dt (1/s); returns viscous stress sigma (Pa). Building block of the Kelvin-Voigt, Maxwell, and standard-linear-solid viscoelastic models."""
    return eta * strain_rate

newtonian_viscosity = create_equation(
    id='newtonian_viscosity',
    output_units='Pa',
    name='Newtonian Viscous Stress',
    category=EquationCategory.MEMBRANE,
    latex='\\sigma = \\eta\\,\\frac{d\\epsilon}{dt}',
    simplified='sigma = eta * d(epsilon)/dt',
    description="Newtonian viscous constitutive relation: stress in a linear viscous (dashpot) element equals viscosity times strain rate. It is the viscous counterpart of Hooke's law (elastic stress = modulus x strain) and combines with the elastic element to form the Kelvin-Voigt, Maxwell, and standard-linear-solid models of cell/tissue viscoelasticity. Feher section 2.1, Appendix 2.1.A2, Eq 2.1.A2.2.",
    compute_func=compute_newtonian_viscosity,
    parameters=[
        Parameter(name='eta', description='Dynamic viscosity of the viscous (dashpot) element', units='Pa*s', symbol='\\eta', physiological_range=(0.0001, 1000000.0)),
        Parameter(name='strain_rate', description='Rate of change of strain, d(epsilon)/dt', units='1/s', symbol='\\dot{\\epsilon}', physiological_range=(1e-06, 1000.0)),
    ],
    depends_on=[],
    produces='sigma_viscous',
    metadata=EquationMetadata(source_unit=2, source_chapter='2.1',
                              source_section='Appendix 2.1.A2 (viscoelastic models of the cell)', page_reference=None,
                              textbook_equation_number='2.1.A2.2'),
)
register_equation(newtonian_viscosity)

try:
    __all__ += ['newtonian_viscosity']
except NameError:
    __all__ = ['newtonian_viscosity']

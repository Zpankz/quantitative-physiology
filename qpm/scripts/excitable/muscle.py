"""Muscle Mechanics Equations

Force-velocity relationships, cross-bridge models, and calcium-force coupling
for skeletal muscle mechanics.

Source: Quantitative Human Physiology 3rd Edition, Unit 3"""

"""
Force-Calcium Relationship (Hill Equation)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def ca_force_relationship(Ca: float, F_max: float, K_d: float = 1.0, n: float = 3.0) -> float:
    """
    Force-calcium relationship using Hill equation.

    Formula: F/F_max = [Ca²⁺]^n / (K_d^n + [Ca²⁺]^n)

    This describes the cooperative binding of calcium to troponin
    and the resulting force generation.

    Parameters:
    -----------
    Ca : float - Calcium concentration (μM)
    F_max : float - Maximum force (N)
    K_d : float - Dissociation constant (μM), default: 1.0
    n : float - Hill coefficient (cooperative binding), default: 3.0

    Returns:
    --------
    F : float - Force (N)
    """
    return F_max * (Ca**n) / (K_d**n + Ca**n)

# Create and register atomic equation
ca_force_relationship_eq = create_equation(
    id="ca_force_relationship",
    output_units='N',
    name="Force-Calcium Relationship",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{F}{F_{max}} = \frac{[\text{Ca}^{2+}]^n}{K_d^n + [\text{Ca}^{2+}]^n}",
    simplified="F/F_max = [Ca²⁺]^n / (K_d^n + [Ca²⁺]^n)",
    description="Hill equation relating calcium concentration to muscle force",
    compute_func=ca_force_relationship,
    parameters=[
        Parameter(
            name="Ca",
            description="Calcium concentration",
            units="μM",
            symbol=r"[\text{Ca}^{2+}]",
            physiological_range=(0.05, 10.0)  # 50 nM to 10 μM
        ),
        Parameter(
            name="K_d",
            description="Dissociation constant",
            units="μM",
            symbol="K_d",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient (cooperativity)",
            units="dimensionless",
            symbol="n",
            default_value=3.0,
            physiological_range=(2.0, 4.0)
        ),
        Parameter(
            name="F_max",
            description="Maximum force",
            units="N",
            symbol="F_{max}",
            physiological_range=(0.0, 10000.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.6")
)
register_equation(ca_force_relationship_eq)

"""
Hill Force-Velocity Relationship

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def hill_force_velocity(F_0: float, a: float, b: float,
                        F: float = None, v: float = None) -> float:
    """
    Hill force-velocity relationship for muscle contraction.

    Formula: (F + a)(v + b) = (F_0 + a) × b
    Or equivalently: v = b × (F_0 - F) / (F + a)

    This hyperbolic relationship describes how force and velocity
    are inversely related during muscle shortening.

    Parameters:
    -----------
    F_0 : float - Isometric force (maximum force at v=0) (N)
    a : float - Hill constant (N)
    b : float - Hill constant (m/s)
    F : float - Force (N) - optional if computing v, default: None
    v : float - Velocity (m/s) - optional if computing F, default: None

    Returns:
    --------
    v or F : float - Velocity (m/s) or Force (N) depending on input
    """
    if F is not None:
        # Calculate velocity from force
        return b * (F_0 - F) / (F + a)
    elif v is not None:
        # Calculate force from velocity
        return (F_0 * b - a * v) / (v + b)
    else:
        raise ValueError("Must provide either F or v")

# Create and register atomic equation
hill_force_velocity_eq = create_equation(
    id="hill_force_velocity",
    output_units='m/s',
    name="Hill Force-Velocity Relationship",
    category=EquationCategory.EXCITABLE,
    latex=r"(F + a)(v + b) = (F_0 + a)b",
    simplified="(F + a)(v + b) = (F_0 + a) × b",
    description="Hyperbolic relationship between muscle force and shortening velocity",
    compute_func=hill_force_velocity,
    parameters=[
        Parameter(
            name="F_0",
            description="Isometric force (maximum force)",
            units="N",
            symbol="F_0",
            physiological_range=(0.0, 10000.0)
        ),
        Parameter(
            name="a",
            description="Hill constant (force parameter)",
            units="N",
            symbol="a",
            physiological_range=(0.0, 5000.0)
        ),
        Parameter(
            name="b",
            description="Hill constant (velocity parameter)",
            units="m/s",
            symbol="b",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="F",
            description="Force (for computing velocity)",
            units="N",
            symbol="F",
            physiological_range=(0.0, 10000.0)
        ),
        Parameter(
            name="v",
            description="Velocity (for computing force)",
            units="m/s",
            symbol="v",
            physiological_range=(0.0, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.4")
)
register_equation(hill_force_velocity_eq)

"""
Huxley Attached Cross-Bridge Fraction

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def huxley_attached_fraction(f: float, g: float, n: float = 0.0, compute_steady_state: bool = False) -> float:
    """
    Rate of change of attached cross-bridge fraction.

    Formula: dn/dt = (1-n) × f(x) - n × g(x)

    Steady-state: n = f / (f + g)

    Parameters:
    -----------
    f : float - Attachment rate (s⁻¹)
    g : float - Detachment rate (s⁻¹)
    n : float - Current fraction of attached bridges (0-1), default: 0.0
    compute_steady_state : bool - If True, return steady-state value, default: False

    Returns:
    --------
    dn_dt or n_ss : float - Rate of change (1/s) or steady-state fraction
    """
    if compute_steady_state:
        # Steady-state value
        if f + g > 0:
            return f / (f + g)
        else:
            return 0.0
    else:
        # Time derivative
        return (1 - n) * f - n * g

# Create and register atomic equation
huxley_attached_fraction_eq = create_equation(
    id="huxley_attached_fraction",
    output_units='1/s',
    name="Huxley Attached Cross-Bridge Fraction",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{dn}{dt} = (1-n)f(x) - n g(x)",
    simplified="dn/dt = (1-n) × f(x) - n × g(x)",
    description="Dynamics of cross-bridge attachment during muscle contraction",
    compute_func=huxley_attached_fraction,
    parameters=[
        Parameter(
            name="n",
            description="Fraction of attached cross-bridges",
            units="dimensionless",
            symbol="n",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="f",
            description="Attachment rate",
            units="s⁻¹",
            symbol="f",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="g",
            description="Detachment rate",
            units="s⁻¹",
            symbol="g",
            physiological_range=(0.0, 300.0)
        ),
        Parameter(
            name="compute_steady_state",
            description="Flag to compute steady-state value",
            units="boolean",
            symbol="",
            default_value=False
        ),
    ],
    depends_on=["huxley_attachment_rate", "huxley_detachment_rate"],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.5")
)
register_equation(huxley_attached_fraction_eq)

"""
Huxley Cross-Bridge Attachment Rate

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def huxley_attachment_rate(x: float, f1: float = 43.3, h: float = 10.0) -> float:
    """
    Huxley 1957 cross-bridge attachment rate function.

    Formula: f(x) = f₁ × (h-x)/h  for 0 < x < h
                  = 0              otherwise

    Where x is the displacement of the cross-bridge from its
    unstrained position.

    Parameters:
    -----------
    x : float - Cross-bridge displacement (nm)
    f1 : float - Maximum attachment rate constant (s⁻¹), default: 43.3
    h : float - Cross-bridge stroke distance (nm), default: 10.0

    Returns:
    --------
    f : float - Attachment rate (s⁻¹)
    """
    if 0 < x < h:
        return f1 * (h - x) / h
    else:
        return 0.0

# Create and register atomic equation
huxley_attachment_rate_eq = create_equation(
    id="huxley_attachment_rate",
    output_units='1/s',
    produces="f",
    name="Huxley Cross-Bridge Attachment Rate",
    category=EquationCategory.EXCITABLE,
    latex=r"f(x) = \begin{cases} f_1 \frac{h-x}{h} & 0 < x < h \\ 0 & \text{otherwise} \end{cases}",
    simplified="f(x) = f₁ × (h-x)/h for 0 < x < h",
    description="Rate of cross-bridge attachment as function of displacement",
    compute_func=huxley_attachment_rate,
    parameters=[
        Parameter(
            name="x",
            description="Cross-bridge displacement",
            units="nm",
            symbol="x",
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="f1",
            description="Maximum attachment rate constant",
            units="s⁻¹",
            symbol="f_1",
            default_value=43.3,
            physiological_range=(10.0, 100.0)
        ),
        Parameter(
            name="h",
            description="Cross-bridge stroke distance",
            units="nm",
            symbol="h",
            default_value=10.0,
            physiological_range=(5.0, 15.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.5")
)
register_equation(huxley_attachment_rate_eq)

"""
Huxley Cross-Bridge Detachment Rate

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def huxley_detachment_rate(x: float, g1: float = 10.0, g2: float = 209.0, h: float = 10.0) -> float:
    """
    Huxley 1957 cross-bridge detachment rate function.

    Formula: g(x) = g₂ × (-x)/h      for x < 0
                  = g₁               for 0 ≤ x < h
                  = g₂ × (x-h)/h     for x ≥ h

    Parameters:
    -----------
    x : float - Cross-bridge displacement (nm)
    g1 : float - Detachment rate constant in power stroke region (s⁻¹), default: 10.0
    g2 : float - Rapid detachment rate constant outside region (s⁻¹), default: 209.0
    h : float - Cross-bridge stroke distance (nm), default: 10.0

    Returns:
    --------
    g : float - Detachment rate (s⁻¹)
    """
    if x < 0:
        return g2 * (-x) / h
    elif 0 <= x < h:
        return g1
    else:  # x >= h
        return g2 * (x - h) / h

# Create and register atomic equation
huxley_detachment_rate_eq = create_equation(
    id="huxley_detachment_rate",
    output_units='1/s',
    name="Huxley Cross-Bridge Detachment Rate",
    category=EquationCategory.EXCITABLE,
    latex=r"g(x) = \begin{cases} g_2 \frac{-x}{h} & x < 0 \\ g_1 & 0 \le x < h \\ g_2 \frac{x-h}{h} & x \ge h \end{cases}",
    simplified="g(x) = g₁ for 0≤x<h, g₂×(±displacement)/h otherwise",
    description="Rate of cross-bridge detachment as function of displacement",
    compute_func=huxley_detachment_rate,
    parameters=[
        Parameter(
            name="x",
            description="Cross-bridge displacement",
            units="nm",
            symbol="x",
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="g1",
            description="Detachment rate in power stroke region",
            units="s⁻¹",
            symbol="g_1",
            default_value=10.0,
            physiological_range=(5.0, 20.0)
        ),
        Parameter(
            name="g2",
            description="Rapid detachment rate outside region",
            units="s⁻¹",
            symbol="g_2",
            default_value=209.0,
            physiological_range=(100.0, 300.0)
        ),
        Parameter(
            name="h",
            description="Cross-bridge stroke distance",
            units="nm",
            symbol="h",
            default_value=10.0,
            physiological_range=(5.0, 15.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.5")
)
register_equation(huxley_detachment_rate_eq)

"""
Muscle Mechanical Power Output

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def muscle_power(F: float, v: float) -> float:
    """
    Mechanical power output of muscle.

    Formula: P = F × v

    Maximum power occurs at approximately:
    F_opt ≈ 0.3 × F_0
    v_opt ≈ 0.3 × v_max
    P_max ≈ 0.1 × F_0 × v_max

    Parameters:
    -----------
    F : float - Force (N)
    v : float - Velocity (m/s)

    Returns:
    --------
    P : float - Power (W)
    """
    return F * v

# Create and register atomic equation
muscle_power_eq = create_equation(
    id="muscle_power",
    output_units='W',
    name="Muscle Mechanical Power",
    category=EquationCategory.EXCITABLE,
    latex=r"P = F \cdot v",
    simplified="P = F × v",
    description="Mechanical power output as product of force and velocity",
    compute_func=muscle_power,
    parameters=[
        Parameter(
            name="F",
            description="Force",
            units="N",
            symbol="F",
            physiological_range=(0.0, 10000.0)
        ),
        Parameter(
            name="v",
            description="Velocity",
            units="m/s",
            symbol="v",
            physiological_range=(0.0, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.4")
)
register_equation(muscle_power_eq)

__all__ = ['hill_force_velocity_eq', 'muscle_power_eq', 'ca_force_relationship_eq', 'huxley_attachment_rate_eq', 'huxley_detachment_rate_eq', 'huxley_attached_fraction_eq']


# --- coverage pass additions (Feher extraction) ---

def compute_architectural_gear_ratio(v_muscle, v_fiber):
    """Architectural gear ratio (AGR): ratio of whole-muscle shortening
    velocity to muscle-fiber shortening velocity, equivalently the strain
    ratio epsilon_x/epsilon_f. Dimensionless -- v_muscle and v_fiber must be
    given in the SAME units (Feher uses cm/s), so the units cancel. AGR = 1
    for fusiform muscles (fibers run tendon-to-tendon); AGR > 1 for pennate
    muscles because fiber rotation lets the whole muscle shorten faster than
    its fibers. (Feher 3.4, 'The Architectural Gear Ratio Allows Variation in
    Speed and Force'.)
    """
    return v_muscle / v_fiber

architectural_gear_ratio = create_equation(
    id='architectural_gear_ratio',
    output_units='dimensionless',
    name='Architectural Gear Ratio',
    category=EquationCategory.EXCITABLE,
    latex='AGR = \\frac{\\varepsilon_x}{\\varepsilon_f} = \\frac{dL_{\\mathrm{muscle}}/dt}{dL_{\\mathrm{fiber}}/dt}',
    simplified='AGR = epsilon_x / epsilon_f = (dL_muscle/dt) / (dL_fiber/dt)',
    description='The architectural gear ratio quantifies how skeletal-muscle architecture trades force for speed by relating the shortening of the whole muscle to the shortening of its constituent fibers. Defined as the ratio of whole-muscle strain (or shortening velocity) to fiber strain (or shortening velocity). AGR = 1.0 for fusiform muscles whose fibers run straight from tendon to tendon; AGR > 1 for pennate muscles, where fiber rotation about the aponeurosis lets the whole muscle shorten faster than its fibers (Feher reports ~1.16 for a 15-degree unipennate example, and measured values from ~1.0 near maximum force up to ~1.4 unloaded). Used to reason about the speed/force consequences of muscle pennation.',
    compute_func=compute_architectural_gear_ratio,
    parameters=[
        Parameter(name='v_muscle', description='Whole-muscle shortening velocity (or whole-muscle strain rate epsilon_x). Practically the numerator dL_muscle/dt.', units='cm/s', symbol='dL_{muscle}/dt', physiological_range=(0, 500)),
        Parameter(name='v_fiber', description='Muscle-fiber shortening velocity (or fiber strain rate epsilon_f). Denominator dL_fiber/dt; must be > 0 for AGR to be defined.', units='cm/s', symbol='dL_{fiber}/dt', physiological_range=(0.1, 500)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter='3.4',
                              source_section='THE ARCHITECTURAL GEAR RATIO ALLOWS VARIATION IN SPEED AND FORCE', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(architectural_gear_ratio)


def compute_motor_unit_force(N, A, F_S=20.0):
    """Tetanic force of a single motor unit: F_MU = N*A*F_S (Feher 3.4, section
    'THE INNERVATION RATIO RESULTS IN A PROPORTIONAL CONTROL OF MUSCLE FORCE').
    N = innervation ratio (muscle fibers per motor neuron, dimensionless);
    A = cross-sectional area of each identical muscle fiber (cm^2);
    F_S = specific force, force per unit area (N/cm^2, typically ~20).
    Returns motor-unit force F_MU in newtons. Units are self-consistent by
    dimensional cancellation: (dimensionless) * cm^2 * (N/cm^2) = N; do NOT
    'SI-fix' F_S to 2e5 N/m^2 unless A is also converted to m^2."""
    return N * A * F_S

motor_unit_force = create_equation(
    id='motor_unit_force',
    output_units='N',
    name='Motor Unit Tetanic Force',
    category=EquationCategory.EXCITABLE,
    latex='F_{\\mathrm{MU}} = N F_{\\mathrm{MF}} = N A F_{\\mathrm{S}}',
    simplified='F_MU = N * F_MF = N * A * F_S',
    description='Tetanic force produced by a single motor unit as the product of the innervation ratio (N, fibers per motor neuron), the cross-sectional area per fiber (A), and the fiber specific force (F_S, ~20 N/cm^2). This is the atomic per-motor-unit relation underlying proportional (size-principle) control of whole-muscle force; the whole muscle sums these linearly over recruited units, F = sum_i N_i A_i F_S. Used to reason about why larger motor units and larger-CSA fibers generate more force and to estimate muscle/motor-unit force from cross-sectional area and specific tension.',
    compute_func=compute_motor_unit_force,
    parameters=[
        Parameter(name='N', description='Innervation ratio: number of muscle fibers innervated by a single motor neuron (all one fiber type within a motor unit)', units='dimensionless', symbol='N', physiological_range=(1, 2500)),
        Parameter(name='A', description='Cross-sectional area of each (identical) muscle fiber in the motor unit', units='cm^2', symbol='A', physiological_range=(1e-06, 0.0001)),
        Parameter(name='F_S', description='Specific force of the muscle fiber (force per unit cross-sectional area); typically ~20 N/cm^2 with only small differences between fiber types', units='N/cm^2', symbol='F_S', default_value=20, physiological_range=(10, 40)),
    ],
    depends_on=[],
    produces='F_MU',
    metadata=EquationMetadata(source_unit=3, source_chapter='3.4',
                              source_section='THE INNERVATION RATIO RESULTS IN A PROPORTIONAL CONTROL OF MUSCLE FORCE', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(motor_unit_force)

try:
    __all__ += ['architectural_gear_ratio', 'motor_unit_force']
except NameError:
    __all__ = ['architectural_gear_ratio', 'motor_unit_force']

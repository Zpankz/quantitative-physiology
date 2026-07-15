"""Action Potential Equations

Hodgkin-Huxley model and cable theory equations for action potential
generation and propagation.

Source: Quantitative Human Physiology 3rd Edition, Unit 3"""

"""
Cable Equation for Passive Spread

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def cable_equation(lambda_const: float, tau: float, V: float, d2V_dx2: float = 0.0, dV_dt: float = 0.0) -> float:
    """
    Cable equation for passive voltage spread along an axon.

    Formula: λ² × ∂²V/∂x² - τ × ∂V/∂t = V

    This partial differential equation describes how voltage spreads
    passively along a cable-like structure (axon or dendrite).

    Note: This is a PDE. The compute function returns the steady-state
    spatial decay coefficient for instructional purposes.

    Parameters:
    -----------
    lambda_const : float - Space constant (cm)
    tau : float - Time constant (ms)
    V : float - Voltage deviation from rest (mV)
    d2V_dx2 : float - Second spatial derivative (mV/cm²), default 0.0
    dV_dt : float - Temporal derivative (mV/ms), default 0.0

    Returns:
    --------
    residual : float - PDE residual (should be 0 at solution)
    """
    return lambda_const**2 * d2V_dx2 - tau * dV_dt - V

# Create and register atomic equation
cable_equation_eq = create_equation(
    id="cable_equation",
    output_units='mV',
    name="Cable Equation",
    category=EquationCategory.EXCITABLE,
    latex=r"\lambda^2 \frac{\partial^2 V}{\partial x^2} - \tau \frac{\partial V}{\partial t} = V",
    simplified="λ² × ∂²V/∂x² - τ × ∂V/∂t = V",
    description="Partial differential equation describing passive voltage spread along axons",
    compute_func=cable_equation,
    parameters=[
        Parameter(
            name="lambda_const",
            description="Space constant",
            units="cm",
            symbol=r"\lambda",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="tau",
            description="Time constant",
            units="ms",
            symbol=r"\tau",
            physiological_range=(1.0, 20.0)
        ),
        Parameter(
            name="V",
            description="Voltage deviation from rest",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="d2V_dx2",
            description="Second spatial derivative of voltage",
            units="mV/cm²",
            symbol=r"\frac{\partial^2 V}{\partial x^2}",
            physiological_range=(-1000.0, 1000.0)
        ),
        Parameter(
            name="dV_dt",
            description="Temporal derivative of voltage",
            units="mV/ms",
            symbol=r"\frac{\partial V}{\partial t}",
            physiological_range=(-100.0, 100.0)
        ),
    ],
    depends_on=["space_constant", "membrane_time_constant"],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.3")
)
register_equation(cable_equation_eq)

"""
Hodgkin-Huxley Sodium Inactivation Gating (h)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def hh_gating_h(V: float, h: float) -> float:
    """
    Rate of change of sodium inactivation gating variable h.

    Formula: dh/dt = α_h(V) × (1-h) - β_h(V) × h

    Where:
    α_h = 0.07 × exp(-(V+65)/20)
    β_h = 1 / [1 + exp(-(V+35)/10)]

    Parameters:
    -----------
    V : float - Membrane potential (mV)
    h : float - Current h value (0-1)

    Returns:
    --------
    dh_dt : float - Rate of change of h (1/ms)
    """
    # Rate constants
    alpha_h = 0.07 * np.exp(-(V + 65) / 20)
    beta_h = 1 / (1 + np.exp(-(V + 35) / 10))

    return alpha_h * (1 - h) - beta_h * h

# Create and register atomic equation
hh_gating_h_eq = create_equation(
    id="hh_gating_h",
    output_units='1/ms',
    name="Hodgkin-Huxley Sodium Inactivation (h)",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{dh}{dt} = \alpha_h(V)(1-h) - \beta_h(V)h",
    simplified="dh/dt = α_h(V) × (1-h) - β_h(V) × h",
    description="Dynamics of sodium channel inactivation gating variable",
    compute_func=hh_gating_h,
    parameters=[
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="h",
            description="Sodium inactivation gating variable",
            units="dimensionless",
            symbol="h",
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_gating_h_eq)

"""
Hodgkin-Huxley Sodium Activation Gating (m)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def hh_gating_m(V: float, m: float) -> float:
    """
    Rate of change of sodium activation gating variable m.

    Formula: dm/dt = α_m(V) × (1-m) - β_m(V) × m

    Where:
    α_m = 0.1(V+40) / [1 - exp(-(V+40)/10)]
    β_m = 4 × exp(-(V+65)/18)

    Parameters:
    -----------
    V : float - Membrane potential (mV)
    m : float - Current m value (0-1)

    Returns:
    --------
    dm_dt : float - Rate of change of m (1/ms)
    """
    # Rate constants
    alpha_m = 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))
    beta_m = 4 * np.exp(-(V + 65) / 18)

    return alpha_m * (1 - m) - beta_m * m

# Create and register atomic equation
hh_gating_m_eq = create_equation(
    id="hh_gating_m",
    output_units='1/ms',
    name="Hodgkin-Huxley Sodium Activation (m)",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{dm}{dt} = \alpha_m(V)(1-m) - \beta_m(V)m",
    simplified="dm/dt = α_m(V) × (1-m) - β_m(V) × m",
    description="Dynamics of sodium channel activation gating variable",
    compute_func=hh_gating_m,
    parameters=[
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="m",
            description="Sodium activation gating variable",
            units="dimensionless",
            symbol="m",
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_gating_m_eq)

"""
Hodgkin-Huxley Potassium Activation Gating (n)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def hh_gating_n(V: float, n: float) -> float:
    """
    Rate of change of potassium activation gating variable n.

    Formula: dn/dt = α_n(V) × (1-n) - β_n(V) × n

    Where:
    α_n = 0.01(V+55) / [1 - exp(-(V+55)/10)]
    β_n = 0.125 × exp(-(V+65)/80)

    Parameters:
    -----------
    V : float - Membrane potential (mV)
    n : float - Current n value (0-1)

    Returns:
    --------
    dn_dt : float - Rate of change of n (1/ms)
    """
    # Rate constants
    alpha_n = 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))
    beta_n = 0.125 * np.exp(-(V + 65) / 80)

    return alpha_n * (1 - n) - beta_n * n

# Create and register atomic equation
hh_gating_n_eq = create_equation(
    id="hh_gating_n",
    output_units='1/ms',
    name="Hodgkin-Huxley Potassium Activation (n)",
    category=EquationCategory.EXCITABLE,
    latex=r"\frac{dn}{dt} = \alpha_n(V)(1-n) - \beta_n(V)n",
    simplified="dn/dt = α_n(V) × (1-n) - β_n(V) × n",
    description="Dynamics of potassium channel activation gating variable",
    compute_func=hh_gating_n,
    parameters=[
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="n",
            description="Potassium activation gating variable",
            units="dimensionless",
            symbol="n",
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_gating_n_eq)

"""
Hodgkin-Huxley Leak Current

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def hh_leak_current(V: float, g_L_bar: float = 0.3, E_L: float = -54.4) -> float:
    """
    Leak current in the Hodgkin-Huxley model.

    Formula: I_L = g̅_L × (V - E_L)

    The leak current represents non-specific conductances.

    Parameters:
    -----------
    V : float - Membrane potential (mV)
    g_L_bar : float - Leak conductance (mS/cm²), default: 0.3
    E_L : float - Leak reversal potential (mV), default: -54.4

    Returns:
    --------
    I_L : float - Leak current (μA/cm²)
    """
    return g_L_bar * (V - E_L)

# Create and register atomic equation
hh_leak_current_eq = create_equation(
    id="hh_leak_current",
    output_units='μA/cm²',
    name="Hodgkin-Huxley Leak Current",
    category=EquationCategory.EXCITABLE,
    latex=r"I_L = \bar{g}_L (V - E_L)",
    simplified="I_L = g̅_L × (V - E_L)",
    description="Non-gated leak current representing baseline membrane permeability",
    compute_func=hh_leak_current,
    parameters=[
        Parameter(
            name="g_L_bar",
            description="Leak conductance",
            units="mS/cm²",
            symbol=r"\bar{g}_L",
            default_value=0.3,
            physiological_range=(0.1, 1.0)
        ),
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="E_L",
            description="Leak reversal potential",
            units="mV",
            symbol="E_L",
            default_value=-54.4,
            physiological_range=(-70.0, -40.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_leak_current_eq)

"""
Hodgkin-Huxley Membrane Current Equation

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def hh_membrane_current(I_ext: float, I_Na: float, I_K: float, I_L: float, C_m: float = 1.0) -> float:
    """
    Hodgkin-Huxley membrane current equation.

    Formula: C_m × dV/dt = I_ext - I_Na - I_K - I_L

    This is the fundamental equation describing membrane potential dynamics
    in the Hodgkin-Huxley model. It represents the capacitive current balance.

    Parameters:
    -----------
    I_ext : float - External current (μA/cm²)
    I_Na : float - Sodium current (μA/cm²)
    I_K : float - Potassium current (μA/cm²)
    I_L : float - Leak current (μA/cm²)
    C_m : float - Membrane capacitance (μF/cm²), default: 1.0

    Returns:
    --------
    dV_dt : float - Rate of change of membrane potential (mV/ms)
    """
    return (I_ext - I_Na - I_K - I_L) / C_m

# Create and register atomic equation
hh_membrane_current_eq = create_equation(
    id="hh_membrane_current",
    output_units='mV/ms',
    name="Hodgkin-Huxley Membrane Current",
    category=EquationCategory.EXCITABLE,
    latex=r"C_m \frac{dV}{dt} = I_{ext} - I_{Na} - I_K - I_L",
    simplified="C_m × dV/dt = I_ext - I_Na - I_K - I_L",
    description="Rate of change of membrane potential based on capacitive current balance",
    compute_func=hh_membrane_current,
    parameters=[
        Parameter(
            name="C_m",
            description="Membrane capacitance",
            units="μF/cm²",
            symbol="C_m",
            default_value=1.0,
            physiological_range=(0.5, 2.0)
        ),
        Parameter(
            name="I_ext",
            description="External applied current",
            units="μA/cm²",
            symbol="I_{ext}",
            physiological_range=(-100.0, 100.0)
        ),
        Parameter(
            name="I_Na",
            description="Sodium current",
            units="μA/cm²",
            symbol="I_{Na}",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="I_K",
            description="Potassium current",
            units="μA/cm²",
            symbol="I_K",
            physiological_range=(0.0, 500.0)
        ),
        Parameter(
            name="I_L",
            description="Leak current",
            units="μA/cm²",
            symbol="I_L",
            physiological_range=(0.0, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_membrane_current_eq)

"""
Hodgkin-Huxley Potassium Current

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def hh_potassium_current(n: float, V: float, g_K_bar: float = 36.0, E_K: float = -77.0) -> float:
    """
    Potassium current in the Hodgkin-Huxley model.

    Formula: I_K = g̅_K × n⁴ × (V - E_K)

    The potassium current depends on maximal conductance, activation (n⁴),
    and driving force (V - E_K).

    Parameters:
    -----------
    n : float - Potassium activation gating variable (0-1)
    V : float - Membrane potential (mV)
    g_K_bar : float - Maximum potassium conductance (mS/cm²), default: 36.0
    E_K : float - Potassium reversal potential (mV), default: -77.0

    Returns:
    --------
    I_K : float - Potassium current (μA/cm²)
    """
    return g_K_bar * (n ** 4) * (V - E_K)

# Create and register atomic equation
hh_potassium_current_eq = create_equation(
    id="hh_potassium_current",
    output_units='μA/cm²',
    name="Hodgkin-Huxley Potassium Current",
    category=EquationCategory.EXCITABLE,
    latex=r"I_K = \bar{g}_K n^4 (V - E_K)",
    simplified="I_K = g̅_K × n⁴ × (V - E_K)",
    description="Voltage-gated potassium current with fourth-order activation",
    compute_func=hh_potassium_current,
    parameters=[
        Parameter(
            name="g_K_bar",
            description="Maximum potassium conductance",
            units="mS/cm²",
            symbol=r"\bar{g}_K",
            default_value=36.0,
            physiological_range=(20.0, 50.0)
        ),
        Parameter(
            name="n",
            description="Potassium activation gating variable",
            units="dimensionless",
            symbol="n",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="E_K",
            description="Potassium reversal potential",
            units="mV",
            symbol="E_K",
            default_value=-77.0,
            physiological_range=(-95.0, -70.0)
        ),
    ],
    depends_on=["nernst_equation", "k_nernst_potential"],  # E_K from the ion-specific Nernst (produces 'E_K')
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_potassium_current_eq)

"""
Hodgkin-Huxley Sodium Current

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def hh_sodium_current(m: float, h: float, V: float, g_Na_bar: float = 120.0, E_Na: float = 50.0) -> float:
    """
    Sodium current in the Hodgkin-Huxley model.

    Formula: I_Na = g̅_Na × m³ × h × (V - E_Na)

    The sodium current depends on maximal conductance, activation (m³),
    inactivation (h), and driving force (V - E_Na).

    Parameters:
    -----------
    m : float - Sodium activation gating variable (0-1)
    h : float - Sodium inactivation gating variable (0-1)
    V : float - Membrane potential (mV)
    g_Na_bar : float - Maximum sodium conductance (mS/cm²), default: 120.0
    E_Na : float - Sodium reversal potential (mV), default: 50.0

    Returns:
    --------
    I_Na : float - Sodium current (μA/cm²)
    """
    return g_Na_bar * (m ** 3) * h * (V - E_Na)

# Create and register atomic equation
hh_sodium_current_eq = create_equation(
    id="hh_sodium_current",
    output_units='μA/cm²',
    name="Hodgkin-Huxley Sodium Current",
    category=EquationCategory.EXCITABLE,
    latex=r"I_{Na} = \bar{g}_{Na} m^3 h (V - E_{Na})",
    simplified="I_Na = g̅_Na × m³ × h × (V - E_Na)",
    description="Voltage-gated sodium current with cubic activation and linear inactivation",
    compute_func=hh_sodium_current,
    parameters=[
        Parameter(
            name="g_Na_bar",
            description="Maximum sodium conductance",
            units="mS/cm²",
            symbol=r"\bar{g}_{Na}",
            default_value=120.0,
            physiological_range=(80.0, 150.0)
        ),
        Parameter(
            name="m",
            description="Sodium activation gating variable",
            units="dimensionless",
            symbol="m",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="h",
            description="Sodium inactivation gating variable",
            units="dimensionless",
            symbol="h",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="E_Na",
            description="Sodium reversal potential",
            units="mV",
            symbol="E_{Na}",
            default_value=50.0,
            physiological_range=(40.0, 70.0)
        ),
    ],
    depends_on=["nernst_equation"],  # E_Na typically calculated from Nernst
    metadata=EquationMetadata(source_unit=3, source_chapter="3.2")
)
register_equation(hh_sodium_current_eq)

"""
Cable Space Constant (Length Constant)

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def space_constant(a: float, R_m: float = 1000.0, R_i: float = 100.0) -> float:
    """
    Cable space constant (length constant).

    Formula: λ = √(r_m / r_i) = √(R_m × a / 2R_i)

    The space constant determines how far voltage spreads passively
    along the axon before decaying to 1/e of its original value.

    Parameters:
    -----------
    a : float - Axon radius (cm)
    R_m : float - Specific membrane resistance (Ω·cm²), default 1000.0
    R_i : float - Axoplasm resistivity (Ω·cm), default 100.0

    Returns:
    --------
    lambda : float - Space constant (cm)
    """
    return np.sqrt(R_m * a / (2 * R_i))

# Create and register atomic equation
space_constant_eq = create_equation(
    id="space_constant",
    output_units='cm',
    name="Cable Space Constant",
    category=EquationCategory.EXCITABLE,
    latex=r"\lambda = \sqrt{\frac{r_m}{r_i}} = \sqrt{\frac{R_m a}{2R_i}}",
    simplified="λ = √(R_m × a / 2R_i)",
    description="Characteristic length for passive voltage spread along an axon",
    compute_func=space_constant,
    parameters=[
        Parameter(
            name="R_m",
            description="Specific membrane resistance",
            units="Ω·cm²",
            symbol="R_m",
            default_value=1000.0,
            physiological_range=(500.0, 10000.0)
        ),
        Parameter(
            name="R_i",
            description="Axoplasm resistivity",
            units="Ω·cm",
            symbol="R_i",
            default_value=100.0,
            physiological_range=(50.0, 200.0)
        ),
        Parameter(
            name="a",
            description="Axon radius",
            units="cm",
            symbol="a",
            physiological_range=(0.0001, 0.1)  # 1 μm to 1 mm
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.3")
)
register_equation(space_constant_eq)

"""
Membrane Time Constant

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""

def time_constant(R_m: float = 1000.0, C_m: float = 1e-6) -> float:
    """
    Membrane time constant.

    Formula: τ = R_m × C_m

    The time constant determines how quickly the membrane potential
    responds to changes in current.

    Parameters:
    -----------
    R_m : float - Specific membrane resistance (Ω·cm²), default 1000.0
    C_m : float - Specific membrane capacitance (F/cm²), default 1e-6

    Returns:
    --------
    tau : float - Time constant (s)
    """
    return R_m * C_m

# Create and register atomic equation
time_constant_eq = create_equation(
    id="membrane_time_constant",
    output_units='s',
    name="Membrane Time Constant (τ = R_m × C_m)",
    category=EquationCategory.EXCITABLE,
    latex=r"\tau = R_m C_m",
    simplified="τ = R_m × C_m",
    description="Characteristic time for membrane potential changes",
    compute_func=time_constant,
    parameters=[
        Parameter(
            name="R_m",
            description="Specific membrane resistance",
            units="Ω·cm²",
            symbol="R_m",
            default_value=1000.0,
            physiological_range=(500.0, 10000.0)
        ),
        Parameter(
            name="C_m",
            description="Specific membrane capacitance",
            units="F/cm²",
            symbol="C_m",
            default_value=1e-6,  # 1 μF/cm²
            physiological_range=(0.5e-6, 2e-6)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter="3.3")
)
register_equation(time_constant_eq)

__all__ = ['hh_membrane_current_eq', 'hh_sodium_current_eq', 'hh_potassium_current_eq', 'hh_leak_current_eq', 'hh_gating_m_eq', 'hh_gating_h_eq', 'hh_gating_n_eq', 'cable_equation_eq', 'space_constant_eq', 'time_constant_eq']


# --- coverage pass additions (Feher extraction) ---

def compute_strength_duration_weiss(I_rh, t, tau_SD):
    """Weiss strength-duration equation (Feher Eqn. 3.2.2): threshold stimulus
    current for a rectangular current pulse of duration t. I_rh = rheobase (A),
    t = pulse duration (s), tau_SD = strength-duration time constant / chronaxie
    (s). Ratio is dimensionless, so the returned threshold current shares the
    units of I_rh (A). At t = tau_SD, I = 2*I_rh."""
    return I_rh * (t + tau_SD) / t

strength_duration_weiss = create_equation(
    id='strength_duration_weiss',
    output_units='A',
    name='Weiss Strength-Duration Equation',
    category=EquationCategory.EXCITABLE,
    latex='I = I_{\\mathrm{rh}}\\frac{(t + \\tau_{\\mathrm{SD}})}{t} = I_{\\mathrm{rh}} + I_{\\mathrm{rh}}\\frac{\\tau_{\\mathrm{SD}}}{t}',
    simplified='I = I_rh * (t + tau_SD) / t',
    description='Weiss strength-duration equation: the minimum (threshold) stimulus current needed to trigger an action potential with a rectangular current pulse of duration t. I_rh is the rheobase (threshold current for an infinitely long pulse); tau_SD is the strength-duration time constant (chronaxie), the pulse duration at which the threshold current equals twice the rheobase. The relation is a rectangular hyperbola offset from the x-axis by I_rh, and underlies the classic strength-duration curve used in nerve/muscle excitability testing, nerve conduction studies, and electrical stimulation (e.g. cardiac pacing threshold, functional electrical stimulation). Feher §3.2, Eqn. (3.2.2); the equivalent charge form Q = I_rh (t + tau_SD) is Eqn. (3.2.1).',
    compute_func=compute_strength_duration_weiss,
    parameters=[
        Parameter(name='I_rh', description='Rheobase: the threshold stimulus current for an infinitely long (steady) pulse; the horizontal asymptote of the strength-duration curve.', units='A', symbol='I_rh', physiological_range=(0, 1)),
        Parameter(name='t', description='Duration of the rectangular stimulus current pulse (must be > 0).', units='s', symbol='t', physiological_range=(0, 10)),
        Parameter(name='tau_SD', description='Strength-duration time constant, i.e. the chronaxie: the pulse duration at which the threshold current equals twice the rheobase.', units='s', symbol='tau_SD', physiological_range=(0, 10)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=3, source_chapter='3.2',
                              source_section='THE STRENGTH-DURATION RELATIONSHIP IS HYPERBOLIC', page_reference=None,
                              textbook_equation_number='3.2.2'),
)
register_equation(strength_duration_weiss)

try:
    __all__ += ['strength_duration_weiss']
except NameError:
    __all__ = ['strength_duration_weiss']


# --- review-add 2026-07-15 ---
def compute_passive_membrane_charging(I: float, R: float, t: float, tau: float) -> float:
    """RC membrane charging to a step current: V(t) = I*R*(1 - e^(-t/tau)).

    At t = tau, V reaches ~63% of the steady IR value."""
    import math
    return I * R * (1.0 - math.exp(-t / tau))

passive_membrane_charging_equation = create_equation(
    id='passive_membrane_charging',
    name='Passive Membrane Charging',
    category=EquationCategory.EXCITABLE,
    latex=r'V(t) = IR\\left(1 - e^{-t/\\tau}\\right)',
    simplified='V(t) = I*R*(1 - exp(-t/tau))',
    description='Passive (subthreshold) membrane charging toward a step current: reaches ~63% of the steady IR value at one time constant tau = R_m*C_m.',
    compute_func=compute_passive_membrane_charging,
    output_units='V',
    parameters=[
        Parameter(name='I', description='Injected step current', units='A', symbol='I', physiological_range=(1e-12, 1e-06)),
        Parameter(name='R', description='Membrane input resistance', units='ohm', symbol='R', physiological_range=(1000000.0, 1000000000.0)),
        Parameter(name='t', description='Time since step onset', units='s', symbol='t', physiological_range=(0.0, 1.0)),
        Parameter(name='tau', description='Membrane time constant', units='s', symbol='tau', physiological_range=(0.001, 0.05)),
    ],
    metadata=EquationMetadata(source_unit=3, source_chapter='3.2'),
)
register_equation(passive_membrane_charging_equation)


# --- review-add 2026-07-15 ---
def compute_hursh_conduction_velocity(D: float, k: float = 6.0) -> float:
    """Myelinated-fibre conduction velocity rule of thumb, theta = k*D
    (k ~ 6 m/s per micron of outer diameter; Hursh 1939)."""
    return k * D

hursh_conduction_velocity_equation = create_equation(
    id='hursh_conduction_velocity',
    name='Hursh Conduction Velocity',
    category=EquationCategory.EXCITABLE,
    latex=r'\\theta = k D',
    simplified='theta = k * D',
    description='Conduction velocity of a myelinated axon as a linear function of outer diameter (Hursh 1939; k ~ 6 m/s/um). Basis for Aalpha/beta/delta classing.',
    compute_func=compute_hursh_conduction_velocity,
    output_units='m/s',
    parameters=[
        Parameter(name='D', description='Axon outer diameter', units='μm', symbol='D', physiological_range=(1.0, 20.0)),
        Parameter(name='k', description='Hursh proportionality constant', units='m/s/μm', symbol='k', physiological_range=(4.5, 6.0)),
    ],
    metadata=EquationMetadata(source_unit=3, source_chapter='3.4'),
)
register_equation(hursh_conduction_velocity_equation)



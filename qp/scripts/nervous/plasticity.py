"""Consolidated module for nervous.plasticity."""

"""
BCM Theory - Bienenstock-Cooper-Munro sliding threshold plasticity

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_bcm_weight_change(r: float, theta_m: float, learning_rate: float = 0.01) -> float:
    """
    Calculate weight change according to BCM theory.

    Formula: Δw ∝ r × (r - θ_m)

    Parameters:
    -----------
    r : float
        Postsynaptic firing rate (Hz)
    theta_m : float
        Modification threshold (Hz)
    learning_rate : float
        Learning rate constant, default 0.01

    Returns:
    --------
    delta_w : float
        Weight change

    Notes:
    ------
    BCM theory implements sliding threshold for LTP/LTD:
    - If r < θ_m: LTD (weight decreases)
    - If r > θ_m: LTP (weight increases)
    - θ_m adjusts with average activity: θ_m ∝ ⟨r⟩²

    Stabilizes learning and prevents runaway potentiation.
    Accounts for metaplasticity (plasticity of plasticity).
    """
    return learning_rate * r * (r - theta_m)


# Create and register atomic equation
bcm_theory = create_equation(
    id="bcm_theory",
    output_units='Hz^2',
    name="BCM Theory",
    category=EquationCategory.NERVOUS,
    latex=r"\Delta w \propto r \times (r - \theta_m)",
    simplified="Δw ∝ r × (r - θ_m)",
    description="Bienenstock-Cooper-Munro theory of synaptic plasticity with sliding threshold. LTD when r<θ_m, LTP when r>θ_m. Threshold θ_m adjusts with activity to stabilize learning.",
    compute_func=compute_bcm_weight_change,
    parameters=[
        Parameter(
            name="r",
            description="Postsynaptic firing rate",
            units="Hz",
            symbol="r",
            default_value=None,
            physiological_range=(0.0, 200.0)
        ),
        Parameter(
            name="theta_m",
            description="Modification threshold",
            units="Hz",
            symbol=r"\theta_m",
            default_value=None,
            physiological_range=(1.0, 100.0)
        ),
        Parameter(
            name="learning_rate",
            description="Learning rate constant",
            units="dimensionless",
            symbol=r"\eta",
            default_value=0.01,
            physiological_range=(0.0001, 0.1)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.6")
)

register_equation(bcm_theory)

"""
Short-Term Depression - Depletion of readily releasable pool

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_depression(R_n: float, u: float, tau_rec: float, dt: float) -> float:
    """
    Calculate available resources after depression and recovery.

    Formula: R_n+1 = R_n × (1 - u) + (1 - R_n) / τ_rec × dt

    Parameters:
    -----------
    R_n : float
        Current fraction of available resources (0-1)
    u : float
        Utilization factor (fraction released per spike)
    tau_rec : float
        Recovery time constant (ms)
    dt : float
        Time step (ms)

    Returns:
    --------
    R_next : float
        Available resources after update (0-1)

    Notes:
    ------
    Depression from vesicle depletion.
    Each spike releases fraction u, reducing R by u×R.
    Recovery with time constant τ_rec ≈ 100-800 ms.
    Prominent at high-release probability synapses.
    """
    depletion = R_n * (1 - u)
    recovery = (1 - R_n) / tau_rec * dt
    return depletion + recovery


# Create and register atomic equation
depression = create_equation(
    id="depression",
    output_units='dimensionless',
    name="Short-Term Depression",
    category=EquationCategory.NERVOUS,
    latex=r"R_{n+1} = R_n \times (1 - u) + \frac{1 - R_n}{\tau_{rec}} \times dt",
    simplified="R_n+1 = R_n × (1 - u) + (1 - R_n)/τ_rec × dt",
    description="Short-term depression from vesicle pool depletion. Each spike releases fraction u, with recovery time constant τ_rec.",
    compute_func=compute_depression,
    parameters=[
        Parameter(
            name="R_n",
            description="Available resources",
            units="dimensionless",
            symbol="R_n",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="u",
            description="Utilization factor",
            units="dimensionless",
            symbol="u",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="tau_rec",
            description="Recovery time constant",
            units="ms",
            symbol=r"\tau_{rec}",
            default_value=None,
            physiological_range=(10.0, 2000.0)
        ),
        Parameter(
            name="dt",
            description="Time step",
            units="ms",
            symbol="dt",
            default_value=1.0,
            physiological_range=(0.01, 100.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.6")
)

register_equation(depression)

"""
Short-Term Facilitation - Enhancement of release probability

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_facilitation(P_n: float, F: float) -> float:
    """
    Calculate facilitated release probability after spike.

    Formula: P_n+1 = P_n + F × (1 - P_n)

    Parameters:
    -----------
    P_n : float
        Current release probability (0-1)
    F : float
        Facilitation increment (0-1)

    Returns:
    --------
    P_next : float
        Release probability after next spike (0-1)

    Notes:
    ------
    Facilitation due to residual calcium accumulation.
    Each spike adds increment F × (1-P), approaching P=1.
    Time constant τ_fac ≈ 50-500 ms.
    Prominent at synapses with low initial P.
    """
    return P_n + F * (1 - P_n)


# Create and register atomic equation
facilitation = create_equation(
    id="facilitation",
    output_units='dimensionless',
    name="Short-Term Facilitation",
    category=EquationCategory.NERVOUS,
    latex=r"P_{n+1} = P_n + F \times (1 - P_n)",
    simplified="P_n+1 = P_n + F × (1 - P_n)",
    description="Short-term facilitation of release probability due to residual calcium. Each spike increases P by F×(1-P), enhancing subsequent release.",
    compute_func=compute_facilitation,
    parameters=[
        Parameter(
            name="P_n",
            description="Current release probability",
            units="dimensionless",
            symbol="P_n",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="F",
            description="Facilitation increment",
            units="dimensionless",
            symbol="F",
            default_value=None,
            physiological_range=(0.0, 0.5)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.6")
)

register_equation(facilitation)

"""
Spike-Timing Dependent Plasticity (STDP) - Timing-based synaptic modification

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_stdp(delta_t: float, A_plus: float, A_minus: float,
                 tau_plus: float = 20.0, tau_minus: float = 20.0) -> float:
    """
    Calculate weight change according to STDP rule.

    Formula:
    Δw = A₊ × e^(-Δt/τ₊)  if Δt > 0 (pre before post → LTP)
    Δw = -A₋ × e^(Δt/τ₋)   if Δt < 0 (post before pre → LTD)

    Parameters:
    -----------
    delta_t : float
        Spike time difference: t_post - t_pre (ms)
    A_plus : float
        LTP amplitude (maximum weight increase)
    A_minus : float
        LTD amplitude (maximum weight decrease)
    tau_plus : float
        LTP time constant (ms), default 20 ms
    tau_minus : float
        LTD time constant (ms), default 20 ms

    Returns:
    --------
    delta_w : float
        Weight change

    Notes:
    ------
    STDP implements Hebb's rule: "neurons that fire together wire together"
    Positive Δt (pre → post): LTP (potentiation)
    Negative Δt (post → pre): LTD (depression)
    Critical window: ±40-50 ms
    """
    if delta_t > 0:
        # Pre before post: LTP
        return A_plus * np.exp(-delta_t / tau_plus)
    else:
        # Post before pre: LTD
        return -A_minus * np.exp(delta_t / tau_minus)


# Create and register atomic equation
stdp = create_equation(
    id="stdp",
    output_units='dimensionless',
    name="Spike-Timing Dependent Plasticity",
    category=EquationCategory.NERVOUS,
    latex=r"\Delta w = \begin{cases} A_+ \times e^{-\Delta t/\tau_+} & \text{if } \Delta t > 0 \\ -A_- \times e^{\Delta t/\tau_-} & \text{if } \Delta t < 0 \end{cases}",
    simplified="Δw = A₊×e^(-Δt/τ₊) if Δt>0, -A₋×e^(Δt/τ₋) if Δt<0",
    description="Spike-timing dependent plasticity: synaptic weight changes depend on precise timing of pre- and postsynaptic spikes. Pre→post causes LTP, post→pre causes LTD.",
    compute_func=compute_stdp,
    parameters=[
        Parameter(
            name="delta_t",
            description="Spike time difference (post - pre)",
            units="ms",
            symbol=r"\Delta t",
            default_value=None,
            physiological_range=(-100.0, 100.0)
        ),
        Parameter(
            name="A_plus",
            description="LTP amplitude",
            units="dimensionless",
            symbol="A_+",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="A_minus",
            description="LTD amplitude",
            units="dimensionless",
            symbol="A_-",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="tau_plus",
            description="LTP time constant",
            units="ms",
            symbol=r"\tau_+",
            default_value=20.0,
            physiological_range=(5.0, 50.0)
        ),
        Parameter(
            name="tau_minus",
            description="LTD time constant",
            units="ms",
            symbol=r"\tau_-",
            default_value=20.0,
            physiological_range=(5.0, 50.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.6")
)

register_equation(stdp)


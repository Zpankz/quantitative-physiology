"""Consolidated module for nervous.motor."""

"""
Fusion Frequency - Frequency for complete tetanic fusion

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_fusion_frequency(tau_twitch: float) -> float:
    """
    Calculate fusion frequency from twitch time constant.

    Formula: f_fusion ≈ 3/τ_twitch

    Parameters:
    -----------
    tau_twitch : float
        Twitch duration (time constant, s)

    Returns:
    --------
    f_fusion : float
        Fusion frequency (Hz)

    Notes:
    ------
    Frequency at which individual twitches fuse into smooth tetanus.
    Slow fibers: τ ≈ 0.1 s → f_fusion ≈ 20-30 Hz
    Fast fibers: τ ≈ 0.02 s → f_fusion ≈ 50-100 Hz
    Rule of thumb: fusion occurs when interpulse interval < τ/3
    """
    return 3.0 / tau_twitch


# Create and register atomic equation
fusion_frequency = create_equation(
    id="fusion_frequency",
    output_units='Hz',
    name="Fusion Frequency",
    category=EquationCategory.NERVOUS,
    latex=r"f_{fusion} \approx \frac{3}{\tau_{twitch}}",
    simplified="f_fusion ≈ 3/τ_twitch",
    description="Frequency at which muscle twitches fuse into smooth tetanic contraction. Depends inversely on twitch duration. Fast fibers have higher fusion frequencies.",
    compute_func=compute_fusion_frequency,
    parameters=[
        Parameter(
            name="tau_twitch",
            description="Twitch time constant",
            units="s",
            symbol=r"\tau_{twitch}",
            default_value=None,
            physiological_range=(0.01, 0.2)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(fusion_frequency)

"""
Golgi Tendon Organ Response - Ib afferent firing rate

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_gto_response(force: float, k_gto: float) -> float:
    """
    Calculate Golgi tendon organ Ib afferent firing rate.

    Formula: f_Ib = k_GTO × Force

    Parameters:
    -----------
    force : float
        Muscle force (N)
    k_gto : float
        GTO sensitivity (Hz/N)

    Returns:
    --------
    f_Ib : float
        Ib afferent firing rate (Hz)

    Notes:
    ------
    Golgi tendon organs are in series with muscle fibers.
    Encode muscle force/tension, not length.
    Provide feedback for force control.
    Mediate autogenic inhibition (protect against excessive force).
    More sensitive to active than passive tension.
    """
    return k_gto * force


# Create and register atomic equation
gto_response = create_equation(
    id="gto_response",
    output_units='Hz',
    name="Golgi Tendon Organ Response",
    category=EquationCategory.NERVOUS,
    latex=r"f_{Ib} = k_{GTO} \times Force",
    simplified="f_Ib = k_GTO × Force",
    description="Golgi tendon organ Ib afferent response encoding muscle force. Located in series with muscle, provides force feedback for motor control and autogenic inhibition.",
    compute_func=compute_gto_response,
    parameters=[
        Parameter(
            name="force",
            description="Muscle force",
            units="N",
            symbol="Force",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="k_gto",
            description="GTO sensitivity",
            units="Hz/N",
            symbol="k_{GTO}",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(gto_response)

"""
Rate-Force Relation - Force output as function of firing rate

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_rate_force_relation(f: float, F_0: float, k: float) -> float:
    """
    Calculate muscle force as function of motor neuron firing rate.

    Formula: F(f) = F_0 × [1 - e^(-k×f)]

    Parameters:
    -----------
    f : float
        Firing frequency (Hz)
    F_0 : float
        Maximum force (N or arbitrary units)
    k : float
        Rate constant (1/Hz)

    Returns:
    --------
    F : float
        Force output (N or arbitrary units)

    Notes:
    ------
    Describes force summation with increasing firing rate.
    At low frequencies: twitches sum linearly
    At high frequencies: approaches tetanic fusion
    k depends on twitch kinetics (faster for fast fibers)
    """
    return F_0 * (1 - np.exp(-k * f))


# Create and register atomic equation
rate_force_relation = create_equation(
    id="rate_force_relation",
    output_units='N',
    name="Rate-Force Relation",
    category=EquationCategory.NERVOUS,
    latex=r"F(f) = F_0 \times [1 - e^{-k \times f}]",
    simplified="F(f) = F_0 × [1 - e^(-k×f)]",
    description="Relationship between motor neuron firing rate and muscle force output. Force increases exponentially toward maximum as rate increases.",
    compute_func=compute_rate_force_relation,
    parameters=[
        Parameter(
            name="f",
            description="Firing frequency",
            units="Hz",
            symbol="f",
            default_value=None,
            physiological_range=(0.0, 200.0)
        ),
        Parameter(
            name="F_0",
            description="Maximum force",
            units="N",
            symbol="F_0",
            default_value=None,
            physiological_range=(0.001, 1000.0)
        ),
        Parameter(
            name="k",
            description="Rate constant",
            units="1/Hz",
            symbol="k",
            default_value=None,
            physiological_range=(0.01, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(rate_force_relation)

"""
Stretch Reflex Gain - Overall gain of stretch reflex loop

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_reflex_gain(k_spindle: float, g_synapse: float, k_motor: float) -> float:
    """
    Calculate stretch reflex gain (change in force per unit length change).

    Formula: G = ΔForce / ΔLength = k_spindle × g_synapse × k_motor

    Parameters:
    -----------
    k_spindle : float
        Spindle sensitivity (Hz/mm)
    g_synapse : float
        Synaptic gain (motor neuron spikes per Ia spike)
    k_motor : float
        Motor neuron to force conversion (N/Hz)

    Returns:
    --------
    G : float
        Reflex gain (N/mm)

    Notes:
    ------
    Determines stiffness added by stretch reflex.
    High gain: muscle resists length changes (postural control)
    Low gain: muscle more compliant (fine motor control)
    Modulated by descending control and gamma motor neurons
    """
    return k_spindle * g_synapse * k_motor


# Create and register atomic equation
reflex_gain = create_equation(
    id="reflex_gain",
    output_units='N/mm',
    name="Stretch Reflex Gain",
    category=EquationCategory.NERVOUS,
    latex=r"G = \frac{\Delta Force}{\Delta Length} = k_{spindle} \times g_{synapse} \times k_{motor}",
    simplified="G = ΔForce/ΔLength = k_spindle × g_synapse × k_motor",
    description="Overall gain of stretch reflex loop, determining how much force is generated in response to length perturbation. Product of spindle, synaptic, and motor gains.",
    compute_func=compute_reflex_gain,
    parameters=[
        Parameter(
            name="k_spindle",
            description="Spindle sensitivity",
            units="Hz/mm",
            symbol="k_{spindle}",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="g_synapse",
            description="Synaptic gain",
            units="dimensionless",
            symbol="g_{synapse}",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_motor",
            description="Motor to force conversion",
            units="N/Hz",
            symbol="k_{motor}",
            default_value=None,
            physiological_range=(0.001, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(reflex_gain)

"""
Muscle Spindle Response - Ia afferent firing rate

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_spindle_response(L: float, L_0: float, dL_dt: float,
                              k_static: float, k_dynamic: float) -> float:
    """
    Calculate muscle spindle Ia afferent firing rate.

    Formula: f_Ia = k_static × (L - L₀) + k_dynamic × (dL/dt)

    Parameters:
    -----------
    L : float
        Current muscle length (mm)
    L_0 : float
        Reference length (mm)
    dL_dt : float
        Rate of length change (mm/s)
    k_static : float
        Static sensitivity (Hz/mm)
    k_dynamic : float
        Dynamic sensitivity (Hz/(mm/s))

    Returns:
    --------
    f_Ia : float
        Ia afferent firing rate (Hz)

    Notes:
    ------
    Muscle spindle Ia afferents encode both position and velocity.
    Static component: sustained response to stretch
    Dynamic component: transient response to velocity
    Used for proprioception and stretch reflex
    """
    return k_static * (L - L_0) + k_dynamic * dL_dt


# Create and register atomic equation
spindle_response = create_equation(
    id="spindle_response",
    output_units='Hz',
    name="Muscle Spindle Response",
    category=EquationCategory.NERVOUS,
    latex=r"f_{Ia} = k_{static} \times (L - L_0) + k_{dynamic} \times \frac{dL}{dt}",
    simplified="f_Ia = k_static × (L - L₀) + k_dynamic × (dL/dt)",
    description="Muscle spindle Ia afferent response encoding both muscle length (position) and velocity of stretch. Provides proprioceptive feedback for motor control.",
    compute_func=compute_spindle_response,
    parameters=[
        Parameter(
            name="L",
            description="Current muscle length",
            units="mm",
            symbol="L",
            default_value=None,
            physiological_range=(0.0, 500.0)
        ),
        Parameter(
            name="L_0",
            description="Reference length",
            units="mm",
            symbol="L_0",
            default_value=None,
            physiological_range=(0.0, 500.0)
        ),
        Parameter(
            name="dL_dt",
            description="Rate of length change",
            units="mm/s",
            symbol=r"\frac{dL}{dt}",
            default_value=None,
            physiological_range=(-1000.0, 1000.0)
        ),
        Parameter(
            name="k_static",
            description="Static sensitivity",
            units="Hz/mm",
            symbol="k_{static}",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_dynamic",
            description="Dynamic sensitivity",
            units="Hz/(mm/s)",
            symbol="k_{dynamic}",
            default_value=None,
            physiological_range=(0.01, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.4")
)

register_equation(spindle_response)


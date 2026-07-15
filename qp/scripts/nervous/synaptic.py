"""Consolidated module for nervous.synaptic."""

"""
Alpha Function Synaptic Conductance - Time course of synaptic conductance

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_alpha_function(t: float, g_max: float, tau: float) -> float:
    """
    Calculate synaptic conductance using alpha function time course.

    Formula: g(t) = g_max × (t/τ) × e^(1-t/τ)

    Parameters:
    -----------
    t : float
        Time after synapse activation (ms)
    g_max : float
        Peak conductance (nS)
    tau : float
        Time constant (ms)

    Returns:
    --------
    g : float
        Conductance at time t (nS)

    Notes:
    ------
    The alpha function peaks at t = τ with amplitude g_max.
    Provides simple, realistic synaptic waveform with single time constant.
    For AMPA: τ ≈ 2-5 ms
    For NMDA: τ ≈ 50-200 ms
    For GABA_A: τ ≈ 10-30 ms
    """
    if t < 0:
        return 0.0
    return g_max * (t / tau) * np.exp(1 - t / tau)


# Create and register atomic equation
alpha_function = create_equation(
    id="alpha_function",
    output_units='nS',
    produces="g_syn",
    name="Alpha Function Synaptic Conductance",
    category=EquationCategory.NERVOUS,
    latex=r"g(t) = g_{max} \times \frac{t}{\tau} \times e^{1-t/\tau}",
    simplified="g(t) = g_max × (t/τ) × e^(1-t/τ)",
    description="Alpha function describing the time course of synaptic conductance. Peaks at t=τ and provides a simple, realistic synaptic waveform.",
    compute_func=compute_alpha_function,
    parameters=[
        Parameter(
            name="t",
            description="Time after synapse activation",
            units="ms",
            symbol="t",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="g_max",
            description="Peak conductance",
            units="nS",
            symbol="g_{max}",
            default_value=None,
            physiological_range=(0.001, 100.0)
        ),
        Parameter(
            name="tau",
            description="Time constant",
            units="ms",
            symbol=r"\tau",
            default_value=None,
            physiological_range=(0.1, 500.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(alpha_function)

"""
Calcium-Triggered Release (Cooperative Binding Model) - Vesicle release probability

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_ca_release_cooperative(Ca: float, K_d: float = 15.0) -> float:
    """
    Calculate vesicle release probability using cooperative Ca2+ binding model.

    Formula: P_release = [Ca²⁺]⁴ / (K_d⁴ + [Ca²⁺]⁴)

    Parameters:
    -----------
    Ca : float
        Calcium concentration (μM)
    K_d : float
        Dissociation constant for release machinery (μM), default 15.0 μM

    Returns:
    --------
    P_release : float
        Release probability (0-1)

    Notes:
    ------
    The fourth-power relationship (n≈3-4) reflects cooperative binding
    of ~4 Ca2+ ions to synaptotagmin in the release machinery.
    K_d typically ranges from 10-20 μM for fast release.
    """
    return Ca**4 / (K_d**4 + Ca**4)


# Create and register atomic equation
ca_release_cooperative = create_equation(
    id="ca_release_cooperative",
    output_units='dimensionless',
    name="Calcium-Triggered Release (Cooperative Binding)",
    category=EquationCategory.NERVOUS,
    latex=r"P_{release} = \frac{[Ca^{2+}]^4}{K_d^4 + [Ca^{2+}]^4}",
    simplified="P_release = [Ca]^4 / (K_d^4 + [Ca]^4)",
    description="Vesicle release probability based on cooperative calcium binding to release machinery (synaptotagmin). The fourth-power dependence reflects ~4 Ca2+ binding sites.",
    compute_func=compute_ca_release_cooperative,
    parameters=[
        Parameter(
            name="Ca",
            description="Calcium concentration",
            units="μM",
            symbol="[Ca^{2+}]",
            default_value=None,
            physiological_range=(0.1, 100.0)
        ),
        Parameter(
            name="K_d",
            description="Dissociation constant for release machinery",
            units="μM",
            symbol="K_d",
            default_value=15.0,
            physiological_range=(5.0, 30.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(ca_release_cooperative)

"""
Double Exponential Synaptic Conductance - More realistic synaptic time course

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_double_exponential(t: float, g_max: float, tau_rise: float, tau_decay: float) -> float:
    """
    Calculate synaptic conductance using double exponential.

    Formula: g(t) = g_max × [e^(-t/τ_decay) - e^(-t/τ_rise)]

    Parameters:
    -----------
    t : float
        Time after synapse activation (ms)
    g_max : float
        Peak conductance (nS)
    tau_rise : float
        Rise time constant (ms)
    tau_decay : float
        Decay time constant (ms)

    Returns:
    --------
    g : float
        Conductance at time t (nS)

    Notes:
    ------
    More realistic than alpha function, with separate rise and decay phases.
    Requires τ_decay > τ_rise for proper shape.
    AMPA: τ_rise ≈ 0.2-1 ms, τ_decay ≈ 2-5 ms
    NMDA: τ_rise ≈ 5-10 ms, τ_decay ≈ 50-200 ms
    """
    if t < 0:
        return 0.0
    return g_max * (np.exp(-t / tau_decay) - np.exp(-t / tau_rise))


# Create and register atomic equation
double_exponential = create_equation(
    id="double_exponential_synapse",
    output_units='nS',
    produces="g_syn",
    name="Double Exponential Synaptic Conductance",
    category=EquationCategory.NERVOUS,
    latex=r"g(t) = g_{max} \times [e^{-t/\tau_{decay}} - e^{-t/\tau_{rise}}]",
    simplified="g(t) = g_max × [e^(-t/τ_decay) - e^(-t/τ_rise)]",
    description="Double exponential function for synaptic conductance with separate rise and decay time constants, providing more realistic waveform than alpha function.",
    compute_func=compute_double_exponential,
    parameters=[
        Parameter(
            name="t",
            description="Time after synapse activation",
            units="ms",
            symbol="t",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="g_max",
            description="Peak conductance",
            units="nS",
            symbol="g_{max}",
            default_value=None,
            physiological_range=(0.001, 100.0)
        ),
        Parameter(
            name="tau_rise",
            description="Rise time constant",
            units="ms",
            symbol=r"\tau_{rise}",
            default_value=None,
            physiological_range=(0.1, 20.0)
        ),
        Parameter(
            name="tau_decay",
            description="Decay time constant",
            units="ms",
            symbol=r"\tau_{decay}",
            default_value=None,
            physiological_range=(1.0, 500.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(double_exponential)

"""
EPSP Amplitude - Peak excitatory postsynaptic potential amplitude

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_epsp_amplitude(g_syn: float, R_in: float, V_m: float, E_rev: float) -> float:
    """
    Calculate EPSP amplitude from synaptic conductance and input resistance.

    Formula: EPSP = g_syn × R_in × (E_rev - V_m)

    Parameters:
    -----------
    g_syn : float
        Peak synaptic conductance (nS)
    R_in : float
        Input resistance of postsynaptic cell (MΩ)
    V_m : float
        Resting membrane potential (mV)
    E_rev : float
        Reversal potential for excitatory synapse (mV)

    Returns:
    --------
    EPSP : float
        EPSP amplitude (mV)

    Notes:
    ------
    Derived from I_syn = g_syn × (V_m - E_rev) and V = I × R
    For excitatory synapses: E_rev > V_m, so EPSP is positive (depolarizing)
    Typical EPSP amplitudes: 0.1-10 mV
    """
    # Convert units: nS × MΩ = 10^-3 (dimensionless factor)
    return g_syn * R_in * (E_rev - V_m) * 1e-3


# Create and register atomic equation
epsp_amplitude = create_equation(
    id="epsp_amplitude",
    output_units='mV',
    name="EPSP Amplitude",
    category=EquationCategory.NERVOUS,
    latex=r"EPSP = g_{syn} \times R_{in} \times (E_{rev} - V_m)",
    simplified="EPSP = g_syn × R_in × (E_rev - V_m)",
    description="Peak amplitude of excitatory postsynaptic potential, determined by synaptic conductance, input resistance, and driving force.",
    compute_func=compute_epsp_amplitude,
    parameters=[
        Parameter(
            name="g_syn",
            description="Peak synaptic conductance",
            units="nS",
            symbol="g_{syn}",
            default_value=None,
            physiological_range=(0.001, 100.0)
        ),
        Parameter(
            name="R_in",
            description="Input resistance",
            units="MΩ",
            symbol="R_{in}",
            default_value=None,
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="V_m",
            description="Resting membrane potential",
            units="mV",
            symbol="V_m",
            default_value=-70.0,
            physiological_range=(-90.0, -50.0)
        ),
        Parameter(
            name="E_rev",
            description="Reversal potential",
            units="mV",
            symbol="E_{rev}",
            default_value=0.0,
            physiological_range=(-20.0, 20.0)
        ),
    ],
    depends_on=["alpha_function", "double_exponential_synapse"],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(epsp_amplitude)

"""
NMDA Receptor Mg2+ Block - Voltage-dependent magnesium block

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_nmda_mg_block(V: float, Mg_out: float = 1.0, K_Mg: float = 3.6, V_half: float = 17.0) -> float:
    """
    Calculate voltage-dependent Mg2+ block factor for NMDA receptors.

    Formula: g_NMDA(V) = g_max / (1 + [Mg²⁺]_o/K_Mg × e^(-V/V_half))

    Parameters:
    -----------
    V : float
        Membrane potential (mV)
    Mg_out : float
        External magnesium concentration (mM), default 1.0 mM
    K_Mg : float
        Mg2+ affinity constant (mM), default 3.6 mM
    V_half : float
        Half-maximal voltage (mV), default -17 mV

    Returns:
    --------
    block_factor : float
        Fraction of unblocked conductance (0-1)

    Notes:
    ------
    At rest (V ≈ -70 mV): strong block, minimal conductance
    During depolarization: block relieved, conductance increases
    This voltage dependence makes NMDA receptors coincidence detectors
    """
    return 1.0 / (1.0 + (Mg_out / K_Mg) * np.exp(-V / V_half))


# Create and register atomic equation
nmda_mg_block = create_equation(
    id="nmda_mg_block",
    output_units='dimensionless',
    name="NMDA Receptor Mg2+ Block",
    category=EquationCategory.NERVOUS,
    latex=r"g_{NMDA}(V) = \frac{g_{max}}{1 + \frac{[Mg^{2+}]_o}{K_{Mg}} \times e^{-V/V_{half}}}",
    simplified="g_NMDA(V) = g_max / (1 + [Mg]_o/K_Mg × e^(-V/V_half))",
    description="Voltage-dependent magnesium block of NMDA receptors. At rest, Mg2+ blocks the pore; depolarization relieves block, making NMDA receptors coincidence detectors.",
    compute_func=compute_nmda_mg_block,
    parameters=[
        Parameter(
            name="V",
            description="Membrane potential",
            units="mV",
            symbol="V",
            default_value=None,
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="Mg_out",
            description="External magnesium concentration",
            units="mM",
            symbol="[Mg^{2+}]_o",
            default_value=1.0,
            physiological_range=(0.1, 5.0)
        ),
        Parameter(
            name="K_Mg",
            description="Mg2+ affinity constant",
            units="mM",
            symbol="K_{Mg}",
            default_value=3.6,
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="V_half",
            description="Half-maximal voltage",
            units="mV",
            symbol="V_{half}",
            default_value=-17.0,
            physiological_range=(-30.0, 0.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.2")
)

register_equation(nmda_mg_block)

"""
Quantal Content - Mean number of vesicles released per action potential

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_quantal_content(n: int, p: float) -> float:
    """
    Calculate mean quantal content (average vesicles released).

    Formula: m = n × p

    Parameters:
    -----------
    n : int
        Number of release sites (readily releasable pool size)
    p : float
        Probability of release per site (0-1)

    Returns:
    --------
    m : float
        Mean quantal content (average vesicles released)

    Notes:
    ------
    Typical values:
    - Neuromuscular junction: m ~ 20-200
    - Central synapses: m ~ 0.1-5
    - p ranges from 0.1 to 0.9 depending on synapse type
    """
    return n * p


# Create and register atomic equation
quantal_content = create_equation(
    id="quantal_content",
    output_units='count',
    name="Quantal Content",
    category=EquationCategory.NERVOUS,
    latex=r"m = n \times p",
    simplified="m = n × p",
    description="Mean number of vesicles (quanta) released per action potential, determined by the number of release sites and release probability.",
    compute_func=compute_quantal_content,
    parameters=[
        Parameter(
            name="n",
            description="Number of release sites",
            units="dimensionless",
            symbol="n",
            default_value=None,
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="p",
            description="Probability of release per site",
            units="dimensionless",
            symbol="p",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(quantal_content)

"""
Quantal Variance - Variance in synaptic response amplitude

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_quantal_variance(n: int, p: float, q: float) -> float:
    """
    Calculate variance in synaptic response using binomial statistics.

    Formula: Variance = n × p × (1-p) × q²

    Parameters:
    -----------
    n : int
        Number of release sites
    p : float
        Probability of release per site (0-1)
    q : float
        Quantal size (amplitude of single vesicle response, mV or pA)

    Returns:
    --------
    variance : float
        Variance in synaptic response amplitude (mV² or pA²)

    Notes:
    ------
    Used in variance-mean analysis to estimate n and p:
    Mean = n × p × q
    Variance = n × p × (1-p) × q²
    Therefore: p = 1 - (Variance/Mean)/q
    """
    return n * p * (1 - p) * q**2


# Create and register atomic equation
quantal_variance = create_equation(
    id="quantal_variance",
    output_units='mV^2',
    name="Quantal Variance",
    category=EquationCategory.NERVOUS,
    latex=r"\text{Variance} = n \times p \times (1-p) \times q^2",
    simplified="Variance = n × p × (1-p) × q²",
    description="Variance in synaptic response amplitude based on binomial statistics of vesicle release. Used with mean quantal content for variance-mean analysis.",
    compute_func=compute_quantal_variance,
    parameters=[
        Parameter(
            name="n",
            description="Number of release sites",
            units="dimensionless",
            symbol="n",
            default_value=None,
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="p",
            description="Probability of release per site",
            units="dimensionless",
            symbol="p",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="q",
            description="Quantal size (single vesicle response)",
            units="mV or pA",
            symbol="q",
            default_value=None,
            physiological_range=(0.001, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(quantal_variance)

"""
Shunting Inhibition - Membrane potential with excitation and inhibition

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_shunting_inhibition(g_e: float, E_e: float, g_i: float, E_i: float,
                                 g_L: float, E_L: float) -> float:
    """
    Calculate membrane potential with excitatory and inhibitory inputs.

    Formula: V_m = (g_e × E_e + g_i × E_i + g_L × E_L) / (g_e + g_i + g_L)

    Parameters:
    -----------
    g_e : float
        Excitatory synaptic conductance (nS)
    E_e : float
        Excitatory reversal potential (mV), typically 0 mV
    g_i : float
        Inhibitory synaptic conductance (nS)
    E_i : float
        Inhibitory reversal potential (mV), typically -70 to -80 mV (E_Cl)
    g_L : float
        Leak conductance (nS)
    E_L : float
        Leak reversal potential (mV), typically -70 mV

    Returns:
    --------
    V_m : float
        Membrane potential (mV)

    Notes:
    ------
    Shunting inhibition occurs when inhibitory conductance increases total
    conductance, reducing the effect of excitation even if E_i ≈ V_rest.
    This is more effective than hyperpolarizing inhibition in many cases.
    """
    return (g_e * E_e + g_i * E_i + g_L * E_L) / (g_e + g_i + g_L)


# Create and register atomic equation
shunting_inhibition = create_equation(
    id="shunting_inhibition",
    output_units='mV',
    name="Shunting Inhibition",
    category=EquationCategory.NERVOUS,
    latex=r"V_m = \frac{g_e \times E_e + g_i \times E_i + g_L \times E_L}{g_e + g_i + g_L}",
    simplified="V_m = (g_e × E_e + g_i × E_i + g_L × E_L) / (g_e + g_i + g_L)",
    description="Membrane potential with combined excitatory and inhibitory synaptic inputs. Demonstrates shunting inhibition where increased conductance reduces excitatory drive.",
    compute_func=compute_shunting_inhibition,
    parameters=[
        Parameter(
            name="g_e",
            description="Excitatory synaptic conductance",
            units="nS",
            symbol="g_e",
            default_value=None,
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="E_e",
            description="Excitatory reversal potential",
            units="mV",
            symbol="E_e",
            default_value=0.0,
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="g_i",
            description="Inhibitory synaptic conductance",
            units="nS",
            symbol="g_i",
            default_value=None,
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="E_i",
            description="Inhibitory reversal potential",
            units="mV",
            symbol="E_i",
            default_value=-75.0,
            physiological_range=(-90.0, -60.0)
        ),
        Parameter(
            name="g_L",
            description="Leak conductance",
            units="nS",
            symbol="g_L",
            default_value=None,
            physiological_range=(0.1, 100.0)
        ),
        Parameter(
            name="E_L",
            description="Leak reversal potential",
            units="mV",
            symbol="E_L",
            default_value=-70.0,
            physiological_range=(-90.0, -50.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.2")
)

register_equation(shunting_inhibition)

"""
Synaptic Current - Current flowing through synaptic receptors

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_synaptic_current(g_syn: float, V_m: float, E_rev: float) -> float:
    """
    Calculate synaptic current through postsynaptic receptors.

    Formula: I_syn = g_syn × (V_m - E_rev)

    Parameters:
    -----------
    g_syn : float
        Synaptic conductance (nS)
    V_m : float
        Membrane potential (mV)
    E_rev : float
        Reversal potential for the synapse (mV)

    Returns:
    --------
    I_syn : float
        Synaptic current (pA)

    Notes:
    ------
    Typical reversal potentials:
    - Glutamate (AMPA): E_rev ≈ 0 mV
    - GABA_A: E_rev ≈ -70 to -80 mV (E_Cl)
    - Nicotinic ACh: E_rev ≈ 0 mV
    """
    return g_syn * (V_m - E_rev)


# Create and register atomic equation
synaptic_current = create_equation(
    id="synaptic_current",
    output_units='pA',
    name="Synaptic Current",
    category=EquationCategory.NERVOUS,
    latex=r"I_{syn} = g_{syn} \times (V_m - E_{rev})",
    simplified="I_syn = g_syn × (V_m - E_rev)",
    description="Current flowing through open synaptic receptors, determined by synaptic conductance and driving force (difference between membrane potential and reversal potential).",
    compute_func=compute_synaptic_current,
    parameters=[
        Parameter(
            name="g_syn",
            description="Synaptic conductance",
            units="nS",
            symbol="g_{syn}",
            default_value=None,
            physiological_range=(0.001, 100.0)
        ),
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            default_value=None,
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="E_rev",
            description="Reversal potential",
            units="mV",
            symbol="E_{rev}",
            default_value=None,
            physiological_range=(-100.0, 100.0)
        ),
    ],
    depends_on=["alpha_function", "double_exponential_synapse"],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.1")
)

register_equation(synaptic_current)


"""Consolidated module for nervous.sensory."""

"""
Adaptation Index - Quantifies degree of receptor adaptation

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_adaptation_index(R_peak: float, R_ss: float) -> float:
    """
    Calculate adaptation index (fraction of response that adapts).

    Formula: AI = (R_peak - R_ss) / R_peak

    Parameters:
    -----------
    R_peak : float
        Peak initial response
    R_ss : float
        Steady-state sustained response

    Returns:
    --------
    AI : float
        Adaptation index (0-1)

    Notes:
    ------
    Quantifies the degree of adaptation:
    - AI ≈ 0: Purely tonic (no adaptation)
    - AI ≈ 0.5: Mixed response
    - AI ≈ 1: Purely phasic (complete adaptation)

    Examples:
    - Merkel disc (slowly adapting): AI ≈ 0.1-0.3
    - Meissner corpuscle (rapidly adapting): AI ≈ 0.6-0.8
    - Pacinian corpuscle (very rapidly adapting): AI ≈ 0.9-1.0
    """
    if R_peak == 0:
        return 0.0
    return (R_peak - R_ss) / R_peak


# Create and register atomic equation
adaptation_index = create_equation(
    id="adaptation_index",
    output_units='dimensionless',
    name="Adaptation Index",
    category=EquationCategory.NERVOUS,
    latex=r"AI = \frac{R_{peak} - R_{ss}}{R_{peak}}",
    simplified="AI = (R_peak - R_ss) / R_peak",
    description="Adaptation index quantifies the fraction of response that decays during sustained stimulation. AI=0 is purely tonic, AI=1 is purely phasic.",
    compute_func=compute_adaptation_index,
    parameters=[
        Parameter(
            name="R_peak",
            description="Peak initial response",
            units="arbitrary",
            symbol="R_{peak}",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="R_ss",
            description="Steady-state response",
            units="arbitrary",
            symbol="R_{ss}",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(adaptation_index)

"""
Fechner's Law - Logarithmic relationship between stimulus and sensation

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_fechner_law(I: float, I_0: float, k: float) -> float:
    """
    Calculate perceived sensation magnitude using Fechner's logarithmic law.

    Formula: S = k × log(I/I₀)

    Parameters:
    -----------
    I : float
        Stimulus intensity
    I_0 : float
        Threshold intensity (minimum detectable)
    k : float
        Scaling constant (modality-dependent)

    Returns:
    --------
    S : float
        Perceived sensation magnitude

    Notes:
    ------
    Fechner's Law predicts logarithmic relationship between physical
    stimulus intensity and perceived magnitude.
    Derived from Weber's Law by assuming equal sensation increments
    for equal ΔI/I ratios.
    Works reasonably well for intermediate intensities.
    """
    return k * np.log(I / I_0)


# Create and register atomic equation
fechner_law = create_equation(
    id="fechner_law",
    output_units='arbitrary',
    name="Fechner's Law",
    category=EquationCategory.NERVOUS,
    latex=r"S = k \times \log\left(\frac{I}{I_0}\right)",
    simplified="S = k × log(I/I₀)",
    description="Fechner's logarithmic psychophysical law: perceived sensation magnitude is proportional to the logarithm of stimulus intensity. Derived from Weber's Law.",
    compute_func=compute_fechner_law,
    parameters=[
        Parameter(
            name="I",
            description="Stimulus intensity",
            units="arbitrary",
            symbol="I",
            default_value=None,
            physiological_range=(0.001, 10000.0)
        ),
        Parameter(
            name="I_0",
            description="Threshold intensity",
            units="arbitrary",
            symbol="I_0",
            default_value=None,
            physiological_range=(0.001, 10.0)
        ),
        Parameter(
            name="k",
            description="Scaling constant",
            units="arbitrary",
            symbol="k",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(fechner_law)

"""
Photoreceptor Response - Intensity-response relationship for rods

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_photoreceptor_response(I: float, sigma: float, n: float = 0.85) -> float:
    """
    Calculate photoreceptor (rod) response using Hill equation.

    Formula: R/R_max = I^n / (I^n + σ^n)

    Parameters:
    -----------
    I : float
        Light intensity (photons/μm²/s or relative units)
    sigma : float
        Half-saturation intensity
    n : float
        Hill coefficient, default 0.85 (typically 0.7-1.0)

    Returns:
    --------
    R_normalized : float
        Response normalized to maximum (0-1)

    Notes:
    ------
    Describes saturation of photoreceptor response at high intensities.
    For rods: σ ≈ 10-100 photons/μm²/s
    For cones: higher σ (less sensitive, broader dynamic range)
    n < 1 indicates slight negative cooperativity
    """
    return I**n / (I**n + sigma**n)


# Create and register atomic equation
photoreceptor_response = create_equation(
    id="photoreceptor_response",
    output_units='dimensionless',
    name="Photoreceptor Response",
    category=EquationCategory.NERVOUS,
    latex=r"\frac{R}{R_{max}} = \frac{I^n}{I^n + \sigma^n}",
    simplified="R/R_max = I^n / (I^n + σ^n)",
    description="Hill equation describing photoreceptor (rod) response saturation. Half-maximal response at I=σ. Used to model adaptation and dynamic range of photoreceptors.",
    compute_func=compute_photoreceptor_response,
    parameters=[
        Parameter(
            name="I",
            description="Light intensity",
            units="photons/μm²/s",
            symbol="I",
            default_value=None,
            physiological_range=(0.001, 10000.0)
        ),
        Parameter(
            name="sigma",
            description="Half-saturation intensity",
            units="photons/μm²/s",
            symbol=r"\sigma",
            default_value=None,
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=0.85,
            physiological_range=(0.5, 1.5)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(photoreceptor_response)

"""
Receptive Field (Difference of Gaussians) - Center-surround organization

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_receptive_field_dog(x: float, y: float, A_c: float, sigma_c: float,
                                 A_s: float, sigma_s: float) -> float:
    """
    Calculate receptive field sensitivity using difference of Gaussians.

    Formula: RF(x,y) = A_c × e^(-(x²+y²)/(2σ_c²)) - A_s × e^(-(x²+y²)/(2σ_s²))

    Parameters:
    -----------
    x : float
        Horizontal position (deg or mm)
    y : float
        Vertical position (deg or mm)
    A_c : float
        Center amplitude
    sigma_c : float
        Center width (standard deviation)
    A_s : float
        Surround amplitude
    sigma_s : float
        Surround width (standard deviation)

    Returns:
    --------
    RF : float
        Receptive field sensitivity at position (x,y)

    Notes:
    ------
    Models center-surround organization of visual, somatosensory receptive fields.
    Typically σ_s > σ_c (surround larger than center).
    Produces Mexican-hat shaped sensitivity profile.
    Used in retinal ganglion cells, LGN, V1 simple cells.
    """
    r_squared = x**2 + y**2
    center = A_c * np.exp(-r_squared / (2 * sigma_c**2))
    surround = A_s * np.exp(-r_squared / (2 * sigma_s**2))
    return center - surround


# Create and register atomic equation
receptive_field_dog = create_equation(
    id="receptive_field_dog",
    output_units='arbitrary',
    name="Receptive Field (Difference of Gaussians)",
    category=EquationCategory.NERVOUS,
    latex=r"RF(x,y) = A_c \times e^{-\frac{x^2+y^2}{2\sigma_c^2}} - A_s \times e^{-\frac{x^2+y^2}{2\sigma_s^2}}",
    simplified="RF(x,y) = A_c × e^(-(x²+y²)/(2σ_c²)) - A_s × e^(-(x²+y²)/(2σ_s²))",
    description="Difference of Gaussians model of receptive field with center-surround antagonism. Produces Mexican-hat sensitivity profile characteristic of visual and somatosensory neurons.",
    compute_func=compute_receptive_field_dog,
    parameters=[
        Parameter(
            name="x",
            description="Horizontal position",
            units="deg or mm",
            symbol="x",
            default_value=None,
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="y",
            description="Vertical position",
            units="deg or mm",
            symbol="y",
            default_value=None,
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="A_c",
            description="Center amplitude",
            units="arbitrary",
            symbol="A_c",
            default_value=None,
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="sigma_c",
            description="Center width",
            units="deg or mm",
            symbol=r"\sigma_c",
            default_value=None,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="A_s",
            description="Surround amplitude",
            units="arbitrary",
            symbol="A_s",
            default_value=None,
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="sigma_s",
            description="Surround width",
            units="deg or mm",
            symbol=r"\sigma_s",
            default_value=None,
            physiological_range=(0.5, 20.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(receptive_field_dog)

"""
Receptor Adaptation - First-order adaptation dynamics

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_receptor_adaptation(t: float, R_0: float, R_ss: float, tau_adapt: float) -> float:
    """
    Calculate receptor response during adaptation.

    Formula: R(t) = R_ss + (R_0 - R_ss) × e^(-t/τ_adapt)

    Parameters:
    -----------
    t : float
        Time after stimulus onset (s)
    R_0 : float
        Initial response (peak)
    R_ss : float
        Steady-state response
    tau_adapt : float
        Adaptation time constant (s)

    Returns:
    --------
    R : float
        Receptor response at time t

    Notes:
    ------
    First-order adaptation model describes decay from initial to sustained response.
    Adaptation index: AI = (R_0 - R_ss) / R_0
    - Phasic receptors: High AI (≈0.8-1.0), rapid adaptation (Pacinian corpuscle)
    - Tonic receptors: Low AI (≈0-0.3), sustained response (Merkel disc)
    """
    return R_ss + (R_0 - R_ss) * np.exp(-t / tau_adapt)


# Create and register atomic equation
receptor_adaptation = create_equation(
    id="receptor_adaptation",
    output_units='arbitrary',
    name="Receptor Adaptation",
    category=EquationCategory.NERVOUS,
    latex=r"R(t) = R_{ss} + (R_0 - R_{ss}) \times e^{-t/\tau_{adapt}}",
    simplified="R(t) = R_ss + (R_0 - R_ss) × e^(-t/τ_adapt)",
    description="First-order model of receptor adaptation: response decays exponentially from initial peak to steady-state level. Characterizes phasic vs tonic receptors.",
    compute_func=compute_receptor_adaptation,
    parameters=[
        Parameter(
            name="t",
            description="Time after stimulus onset",
            units="s",
            symbol="t",
            default_value=None,
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="R_0",
            description="Initial response (peak)",
            units="arbitrary",
            symbol="R_0",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="R_ss",
            description="Steady-state response",
            units="arbitrary",
            symbol="R_{ss}",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="tau_adapt",
            description="Adaptation time constant",
            units="s",
            symbol=r"\tau_{adapt}",
            default_value=None,
            physiological_range=(0.01, 100.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(receptor_adaptation)

"""
Stevens' Power Law - Power relationship between stimulus and sensation

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_stevens_power_law(I: float, k: float, n: float) -> float:
    """
    Calculate perceived sensation using Stevens' power law.

    Formula: S = k × I^n

    Parameters:
    -----------
    I : float
        Stimulus intensity
    k : float
        Scaling constant
    n : float
        Exponent (modality-dependent)

    Returns:
    --------
    S : float
        Perceived sensation magnitude

    Notes:
    ------
    Stevens' Power Law is more accurate than Fechner's Law for most modalities.
    Typical exponents:
    - Brightness: n = 0.33 (compressive)
    - Loudness: n = 0.6 (compressive)
    - Length: n = 1.0 (linear)
    - Pressure on palm: n = 1.1 (nearly linear)
    - Electric shock: n = 3.5 (expansive)

    n < 1: compressive (decreasing sensitivity)
    n = 1: linear
    n > 1: expansive (increasing sensitivity)
    """
    return k * np.power(I, n)


# Create and register atomic equation
stevens_power_law = create_equation(
    id="stevens_power_law",
    output_units='arbitrary',
    name="Stevens' Power Law",
    category=EquationCategory.NERVOUS,
    latex=r"S = k \times I^n",
    simplified="S = k × I^n",
    description="Stevens' power law for psychophysics: perceived magnitude is a power function of stimulus intensity. More accurate than Fechner's Law. Exponent n varies by modality.",
    compute_func=compute_stevens_power_law,
    parameters=[
        Parameter(
            name="I",
            description="Stimulus intensity",
            units="arbitrary",
            symbol="I",
            default_value=None,
            physiological_range=(0.001, 10000.0)
        ),
        Parameter(
            name="k",
            description="Scaling constant",
            units="arbitrary",
            symbol="k",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="n",
            description="Exponent (modality-specific)",
            units="dimensionless",
            symbol="n",
            default_value=None,
            physiological_range=(0.1, 5.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(stevens_power_law)

"""
Weber Fraction - Just noticeable difference threshold

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

def compute_weber_fraction(delta_I: float, I: float) -> float:
    """
    Calculate Weber fraction (just noticeable difference).

    Formula: ΔI/I = k (Weber fraction)

    Parameters:
    -----------
    delta_I : float
        Minimum detectable change in intensity
    I : float
        Background intensity

    Returns:
    --------
    k : float
        Weber fraction (constant for a given modality)

    Notes:
    ------
    Weber's Law: the ratio ΔI/I is approximately constant across intensities.
    Typical values:
    - Vision (brightness): k ≈ 0.01-0.02
    - Audition (loudness): k ≈ 0.05-0.10
    - Touch (pressure): k ≈ 0.14
    """
    return delta_I / I


# Create and register atomic equation
weber_fraction = create_equation(
    id="weber_fraction",
    output_units='dimensionless',
    name="Weber Fraction",
    category=EquationCategory.NERVOUS,
    latex=r"\frac{\Delta I}{I} = k",
    simplified="ΔI/I = k",
    description="Weber's Law: just noticeable difference is proportional to background intensity. The Weber fraction k is approximately constant for each sensory modality.",
    compute_func=compute_weber_fraction,
    parameters=[
        Parameter(
            name="delta_I",
            description="Minimum detectable change",
            units="arbitrary",
            symbol=r"\Delta I",
            default_value=None,
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="I",
            description="Background intensity",
            units="arbitrary",
            symbol="I",
            default_value=None,
            physiological_range=(0.001, 10000.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter="4.3")
)

register_equation(weber_fraction)



# --- coverage pass additions (Feher extraction) ---

def compute_direction_selectivity_index(R_pref, R_null):
    """DSI = (R_pref - R_null) / (R_pref + R_null); responses R in arbitrary firing-rate units (e.g. spikes/s or max instantaneous rate). Feher 4.10 'Some retinal ganglion cells exhibit direction or orientation selectivity'. Returns a dimensionless index in [0, 1] for a direction-selective retinal ganglion cell."""
    denom = R_pref + R_null
    if denom == 0:
        return 0.0
    return (R_pref - R_null) / denom

direction_selectivity_index = create_equation(
    id='direction_selectivity_index',
    output_units='dimensionless',
    name='Direction Selectivity Index',
    category=EquationCategory.NERVOUS,
    latex='\\mathrm{DSI} = \\frac{R_{\\mathrm{pref}} - R_{\\mathrm{null}}}{R_{\\mathrm{pref}} + R_{\\mathrm{null}}}',
    simplified='DSI = (R_pref - R_null) / (R_pref + R_null)',
    description="Direction selectivity index quantifies the directional tuning of a motion-selective retinal ganglion cell. R_pref is the maximum response to a stimulus moving in the cell's preferred direction and R_null the maximum response to the opposite (null) direction. The normalized-difference (Michelson) form ranges from 0 (no directional selectivity) to 1.0 (perfect selectivity). Used to characterize direction-selective RGCs and, more generally, motion-tuned neurons.",
    compute_func=compute_direction_selectivity_index,
    parameters=[
        Parameter(name='R_pref', description="Maximum response (firing rate) to a stimulus moving in the cell's preferred direction (theta_pref)", units='arbitrary', symbol='R_{pref}', physiological_range=(0, 1000)),
        Parameter(name='R_null', description='Maximum response (firing rate) to a stimulus moving in the opposite (null) direction (theta_null = theta_pref + 180 deg)', units='arbitrary', symbol='R_{null}', physiological_range=(0, 1000)),
    ],
    depends_on=[],
    produces='DSI',
    metadata=EquationMetadata(source_unit=4, source_chapter='4.10',
                              source_section='SOME RETINAL GANGLION CELLS EXHIBIT DIRECTION OR ORIENTATION SELECTIVITY', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(direction_selectivity_index)


def compute_orientation_selectivity_index(R_pref, R_null, R_orth_plus, R_orth_minus):
    """Orientation selectivity index of a retinal ganglion cell (Feher 4.10, 'Some retinal ganglion cells exhibit direction or orientation selectivity'). OSI = (R_pref + R_null - R_orth+ - R_orth-) / (R_pref + R_null). Responses are firing-rate magnitudes in spikes/s (Hz); output is dimensionless, 0 (no selectivity) to 1.0 (perfect selectivity)."""
    denom = R_pref + R_null
    if denom == 0:
        return 0.0
    return (R_pref + R_null - R_orth_plus - R_orth_minus) / denom

orientation_selectivity_index = create_equation(
    id='orientation_selectivity_index',
    output_units='dimensionless',
    name='Orientation Selectivity Index',
    category=EquationCategory.NERVOUS,
    latex='\\mathrm{OSI} = \\frac{R_{\\mathrm{pref}} + R_{\\mathrm{null}} - R_{\\mathrm{orth+}} - R_{\\mathrm{orth-}}}{R_{\\mathrm{pref}} + R_{\\mathrm{null}}}',
    simplified='OSI = (R_pref + R_null - R_orth+ - R_orth-) / (R_pref + R_null)',
    description='Orientation selectivity index (OSI) of a direction/orientation-selective retinal ganglion cell: contrasts the summed response along the preferred motion axis (preferred + null directions) against the summed response along the orthogonal axis (clockwise + counterclockwise orthogonal), normalized by the preferred-axis response. Dimensionless, ranging 0 (no selectivity) to 1.0 (perfect selectivity). Distinct from the direction selectivity index (DSI), which uses only preferred vs null. Feher gives the worked example (12+4-2-1)/(12+4) = 0.81. From Feher Quantitative Human Physiology 3rd ed., 4.10 Vision II.',
    compute_func=compute_orientation_selectivity_index,
    parameters=[
        Parameter(name='R_pref', description='Maximum response in the preferred direction of movement (theta_pref)', units='spikes/s', symbol='R_{pref}', physiological_range=(0, 1000)),
        Parameter(name='R_null', description='Maximum response in the null (opposite) direction, theta_null = theta_pref + 180 deg', units='spikes/s', symbol='R_{null}', physiological_range=(0, 1000)),
        Parameter(name='R_orth_plus', description='Response orthogonal to the preferred direction in the + (clockwise) direction', units='spikes/s', symbol='R_{orth+}', physiological_range=(0, 1000)),
        Parameter(name='R_orth_minus', description='Response orthogonal to the preferred direction in the - (counterclockwise) direction', units='spikes/s', symbol='R_{orth-}', physiological_range=(0, 1000)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter='4.10',
                              source_section='SOME RETINAL GANGLION CELLS EXHIBIT DIRECTION OR ORIENTATION SELECTIVITY', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(orientation_selectivity_index)


def compute_norwich_sensation_magnitude(Phi, k=1.0, beta=1.0, n=1.0):
    """Norwich information-theory law of sensation magnitude: psi = k*ln(1 + beta*Phi**n) (Feher Appendix 4.3.A1, Eqn 4.3.A1.21; Norwich 1987). Phi = stimulus strength, psi = sensation magnitude (arbitrary/modality units); k, beta, n are modality-dependent constants. Parent psychophysical model: reduces to the Weber-Fechner logarithmic law when beta*Phi**n >> 1 and to Stevens' power law when beta*Phi**n << 1."""
    return k * np.log(1.0 + beta * Phi**n)

norwich_sensation_magnitude = create_equation(
    id='norwich_sensation_magnitude',
    output_units='arbitrary',
    name="Norwich's Information-Theory Law of Sensation",
    category=EquationCategory.NERVOUS,
    latex='\\psi = k \\ln(1 + \\beta \\Phi^{n})',
    simplified='psi = k * ln(1 + beta * Phi^n)',
    description="Norwich's information-theory (entropy) law of sensation magnitude: perceived intensity psi is the logarithm of one plus a power of the stimulus strength Phi. Kenneth Norwich derived it from information theory as the parent psychophysical relation that reduces to the Weber-Fechner logarithmic law when beta*Phi^n >> 1 and to Stevens' power law when beta*Phi^n << 1. Constants k, beta, n are modality-dependent. Used to unify the classical psychophysical laws under a single expression.",
    compute_func=compute_norwich_sensation_magnitude,
    parameters=[
        Parameter(name='Phi', description='Stimulus strength/intensity', units='arbitrary', symbol='\\Phi', physiological_range=(0.001, 10000)),
        Parameter(name='k', description='Scaling constant (modality-dependent)', units='arbitrary', symbol='k', default_value=1, physiological_range=(0.1, 10)),
        Parameter(name='beta', description='Stimulus-weighting constant inside the logarithm (modality-dependent)', units='arbitrary', symbol='\\beta', default_value=1, physiological_range=(0.001, 1000)),
        Parameter(name='n', description='Exponent on stimulus strength (modality-dependent)', units='dimensionless', symbol='n', default_value=1, physiological_range=(0.1, 5)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter='4.3',
                              source_section="Appendix 4.3.A1 Weber's Law, Fechner's Law, and Steven's Law of Psychophysics", page_reference=None,
                              textbook_equation_number='4.3.A1.21'),
)
register_equation(norwich_sensation_magnitude)

try:
    __all__ += ['direction_selectivity_index', 'orientation_selectivity_index', 'norwich_sensation_magnitude']
except NameError:
    __all__ = ['direction_selectivity_index', 'orientation_selectivity_index', 'norwich_sensation_magnitude']

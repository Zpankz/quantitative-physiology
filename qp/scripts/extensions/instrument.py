"""Instrument / measurement-system response — the DEFINITIONAL core.

This module holds the *mathematical forms* of measurement-system response, not
the specifications of any particular device. Every relation here is either an
exact closed form of a standard first- or second-order system or an exact
logarithmic/ratio identity from signal theory; none commits a real instrument's
time constant, noise floor, stiffness, mass, or damping. Those device-specific
numbers are deliberately left out (see NEEDS_SOURCE below) — supply them at call
time as inputs.

Grounding: these are exact-math / definitional identities. They are anchored by
mathematics itself (1 - e^-1 = 0.6321…, ln 9 = 2.1972…, 20·log10(10) = 20 dB),
not by a specific Feher page, so no page/equation number is fabricated
(page_reference=None; source_chapter labelled "definitional").

Scope: the *groundable core* of the measurement/device roadmap item. The wider
metrology corpus — sensor drift, calibration curves, hysteresis, quantisation
and artefact models — is OUT OF SCOPE here because it needs empirical,
device-specific anchors rather than exact math.

Equations
---------
- first_order_step_response   f(t) = 1 - e^(-t/τ)          (f(τ) = 0.6321 exactly)
- rise_time_10_90             t_r  = τ·ln(9) ≈ 2.20·τ       (10%→90% of a 1st-order step)
- signal_to_noise_ratio       SNR  = μ_signal / σ_noise     (equal signal & noise ⇒ 1)
- decibel_gain                G_dB = 20·log10(V_out/V_in)   (×10 ⇒ 20 dB)
- natural_frequency           ω_n  = √(k/m)                 (undamped 2nd-order sensor)
- second_order_damping_ratio  ζ    = c / (2·√(k·m))         (ζ = 1 ⇒ critically damped)
"""

import math

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)


# Device-specific quantities intentionally NOT committed in this module. Each
# would need an external, per-instrument anchor (a datasheet or a named
# reference), never an invented value; they are supplied as call-time inputs.
NEEDS_SOURCE = [
    "a specific sensor's time constant τ (datasheet / step-response measurement)",
    "a specific instrument's noise floor σ_noise (device noise spec)",
    "a specific transducer's mechanical stiffness k, moving mass m, damping c",
    "empirical drift / calibration-curve / hysteresis coefficients (out of scope)",
]


# =============================================================================
# First-order step response: f(t) = 1 - e^(-t/τ)
# =============================================================================
def compute_first_order_step_response(t: float, tau: float) -> float:
    """Fractional approach of a first-order instrument to a step input.

    f(t) = 1 - exp(-t/τ)

    Exact identities (independent of any device):
        f(0)   = 0
        f(τ)   = 1 - e^-1 = 0.6321205588…
        f(2τ)  = 1 - e^-2 = 0.8646647168…

    Parameters
    ----------
    t : float
        Elapsed time since the step (same time units as τ).
    tau : float
        System time constant (a device property — supplied, not committed here).

    Returns
    -------
    float
        Fraction of the final value reached (dimensionless, 0→1).
    """
    return 1.0 - math.exp(-t / tau)


first_order_step_response = create_equation(
    id="first_order_step_response",
    output_units="dimensionless",
    name="First-Order Step Response",
    category=EquationCategory.FOUNDATIONS,
    latex=r"f(t) = 1 - e^{-t/\tau}",
    simplified="f(t) = 1 - exp(-t/tau)",
    description=(
        "Fractional approach of a first-order measurement system to a step "
        "input. Definitional exponential form: one time constant reaches "
        "1 - e^-1 = 0.6321 (63.2%) exactly, two reach 0.8647. tau is a "
        "device property supplied as input, not a committed value."
    ),
    compute_func=compute_first_order_step_response,
    parameters=[
        Parameter(name="t", description="Elapsed time since the step",
                  units="s", symbol="t"),
        Parameter(name="tau", description="System time constant (device property)",
                  units="s", symbol=r"\tau"),
    ],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="measurement response (definitional; 1st-order system)",
        page_reference=None,
    ),
)


# =============================================================================
# 10%–90% rise time of a first-order step: t_r = τ·ln(9) ≈ 2.20·τ
# =============================================================================
def compute_rise_time_10_90(tau: float) -> float:
    """10%→90% rise time of a first-order step response.

    Solving 0.9 = 1 - e^(-t/τ) and 0.1 = 1 - e^(-t/τ) and subtracting gives
        t_r = τ·(ln(0.9) - ln(0.1)) = τ·ln(9) = 2.1972…·τ ≈ 2.20·τ

    The 2.2 figure is the rounded exact coefficient ln(9), not an empirical fit.

    Parameters
    ----------
    tau : float
        System time constant (device property — supplied, not committed here).

    Returns
    -------
    float
        Rise time (same time units as τ).
    """
    return tau * math.log(9.0)


rise_time_10_90 = create_equation(
    id="rise_time_10_90",
    output_units="s",
    name="10-90% Rise Time (First-Order)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"t_r = \tau \ln 9 \approx 2.20\,\tau",
    simplified="t_r = tau * ln(9)  (approx 2.2*tau)",
    description=(
        "Time for a first-order instrument to move from 10% to 90% of its "
        "final step value. Exact coefficient is ln(9) = 2.1972, commonly "
        "quoted as ~2.2 time constants. Depends only on tau, a supplied "
        "device property."
    ),
    compute_func=compute_rise_time_10_90,
    parameters=[
        Parameter(name="tau", description="System time constant (device property)",
                  units="s", symbol=r"\tau"),
    ],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="measurement response (definitional; 1st-order step)",
        page_reference=None,
    ),
)


# =============================================================================
# Signal-to-noise ratio: SNR = μ_signal / σ_noise
# =============================================================================
def compute_signal_to_noise_ratio(mu_signal: float, sigma_noise: float) -> float:
    """Amplitude signal-to-noise ratio (linear-amplitude convention).

    SNR = μ_signal / σ_noise  (a pure ratio; equal signal and noise ⇒ 1)

    This is the linear amplitude-ratio form: μ_signal and σ_noise must be the
    SAME linear amplitude quantity in the SAME units (the result is then
    dimensionless). It is NOT the power/variance form (μ²/σ²) nor a dB value;
    the caller supplies matched-unit inputs — no unit coercion is done here.

    Parameters
    ----------
    mu_signal : float
        Signal magnitude (any consistent amplitude unit).
    sigma_noise : float
        Noise magnitude, same units (device property — supplied, not committed).

    Returns
    -------
    float
        Dimensionless ratio.
    """
    return mu_signal / sigma_noise


signal_to_noise_ratio = create_equation(
    id="signal_to_noise_ratio",
    output_units="dimensionless",
    name="Signal-to-Noise Ratio",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\mathrm{SNR} = \frac{\mu_{signal}}{\sigma_{noise}}",
    simplified="SNR = mu_signal / sigma_noise",
    description=(
        "Definitional amplitude signal-to-noise ratio (linear-amplitude "
        "convention): signal magnitude over noise magnitude, both the same "
        "linear quantity in the same units, so the ratio is dimensionless. "
        "Equal signal and noise gives SNR = 1 exactly. Not the power/variance "
        "form nor a dB value. The noise floor sigma_noise is a device property "
        "supplied as input."
    ),
    compute_func=compute_signal_to_noise_ratio,
    parameters=[
        Parameter(name="mu_signal", description="Signal magnitude",
                  units="V", symbol=r"\mu_{signal}"),
        Parameter(name="sigma_noise", description="Noise magnitude (device property)",
                  units="V", symbol=r"\sigma_{noise}"),
    ],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="measurement response (definitional; signal theory)",
        page_reference=None,
    ),
)


# =============================================================================
# Decibel gain: G_dB = 20·log10(V_out/V_in)
# =============================================================================
def compute_decibel_gain(V_out: float, V_in: float) -> float:
    """Voltage (amplitude) gain expressed in decibels.

    G_dB = 20·log10(V_out / V_in)

    Exact identities:
        V_out = V_in           ⇒  0 dB
        V_out = 10·V_in        ⇒  20 dB
        V_out = 100·V_in       ⇒  40 dB

    Parameters
    ----------
    V_out : float
        Output amplitude.
    V_in : float
        Input amplitude (same units).

    Returns
    -------
    float
        Gain in decibels (dB).
    """
    return 20.0 * math.log10(V_out / V_in)


decibel_gain = create_equation(
    id="decibel_gain",
    # A decibel is a DIMENSIONLESS logarithmic ratio, not a physical unit; the
    # dimensional engine already treats such labels (rad, %, pH) as dimensionless.
    # Declaring output_units="dimensionless" keeps V/V dimensionally consistent
    # (parses to the zero vector, not UNKNOWN); "dB" is retained in the name,
    # latex and description as the display label.
    output_units="dimensionless",
    name="Decibel Gain (Amplitude, dB)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"G_{dB} = 20\,\log_{10}\!\left(\frac{V_{out}}{V_{in}}\right)",
    simplified="G_dB = 20 * log10(V_out / V_in)",
    description=(
        "Amplitude gain in decibels (a dimensionless logarithmic ratio). Valid "
        "for like-dimension linear amplitude/voltage quantities: factor-of-10 "
        "amplitude ratio is exactly 20 dB, unity ratio is 0 dB. The 20 prefactor "
        "is the amplitude/voltage convention; power ratios use 10."
    ),
    compute_func=compute_decibel_gain,
    parameters=[
        Parameter(name="V_out", description="Output amplitude",
                  units="V", symbol="V_{out}"),
        Parameter(name="V_in", description="Input amplitude",
                  units="V", symbol="V_{in}"),
    ],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="measurement response (definitional; logarithmic gain)",
        page_reference=None,
    ),
)


# =============================================================================
# Undamped natural frequency of a second-order sensor: ω_n = √(k/m)
# =============================================================================
def compute_natural_frequency(k: float, m: float) -> float:
    """Undamped natural angular frequency of a second-order mechanical sensor.

    ω_n = √(k / m)

    Definitional form for a mass–spring (second-order) transducer. k and m are
    device properties supplied as inputs, not committed here.

    Parameters
    ----------
    k : float
        Effective stiffness (N/m).
    m : float
        Effective moving mass (kg).

    Returns
    -------
    float
        Natural angular frequency (rad/s).
    """
    return math.sqrt(k / m)


natural_frequency = create_equation(
    id="natural_frequency",
    output_units="rad/s",
    name="Natural Frequency (Second-Order Sensor)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\omega_n = \sqrt{\frac{k}{m}}",
    simplified="omega_n = sqrt(k/m)",
    description=(
        "Undamped natural angular frequency of a second-order (mass-spring) "
        "measurement system. Definitional: stiffness over mass under a square "
        "root. k and m are supplied device properties."
    ),
    compute_func=compute_natural_frequency,
    parameters=[
        Parameter(name="k", description="Effective stiffness (device property)",
                  units="N/m", symbol="k"),
        Parameter(name="m", description="Effective moving mass (device property)",
                  units="kg", symbol="m"),
    ],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="measurement response (definitional; 2nd-order system)",
        page_reference=None,
    ),
)


# =============================================================================
# Damping ratio of a second-order sensor: ζ = c / (2·√(k·m))
# =============================================================================
def compute_second_order_damping_ratio(c: float, k: float, m: float) -> float:
    """Damping ratio of a second-order (mass–spring–damper) sensor.

    ζ = c / (2·√(k·m))

    Definitional identity: ζ = 1 is critical damping (c = 2√(km)); ζ < 1 is
    underdamped (rings), ζ > 1 overdamped. c, k, m are device properties
    supplied as inputs.

    Parameters
    ----------
    c : float
        Damping coefficient (N·s/m).
    k : float
        Effective stiffness (N/m).
    m : float
        Effective moving mass (kg).

    Returns
    -------
    float
        Damping ratio (dimensionless).
    """
    return c / (2.0 * math.sqrt(k * m))


second_order_damping_ratio = create_equation(
    id="second_order_damping_ratio",
    output_units="dimensionless",
    name="Damping Ratio (Second-Order Sensor)",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\zeta = \frac{c}{2\sqrt{k\,m}}",
    simplified="zeta = c / (2*sqrt(k*m))",
    description=(
        "Damping ratio of a second-order measurement system. Definitional: "
        "zeta = 1 is critical damping (c = 2*sqrt(k*m)), below 1 underdamped, "
        "above 1 overdamped. c, k, m are supplied device properties."
    ),
    compute_func=compute_second_order_damping_ratio,
    parameters=[
        Parameter(name="c", description="Damping coefficient (device property)",
                  units="N*s/m", symbol="c"),
        Parameter(name="k", description="Effective stiffness (device property)",
                  units="N/m", symbol="k"),
        Parameter(name="m", description="Effective moving mass (device property)",
                  units="kg", symbol="m"),
    ],
    metadata=EquationMetadata(
        source_unit=1,
        source_chapter="measurement response (definitional; 2nd-order system)",
        page_reference=None,
    ),
)


__all__ = [
    "first_order_step_response",
    "rise_time_10_90",
    "signal_to_noise_ratio",
    "decibel_gain",
    "natural_frequency",
    "second_order_damping_ratio",
    "NEEDS_SOURCE",
]

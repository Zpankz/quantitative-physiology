"""Consolidated module for gastrointestinal.motility."""

"""Gastric emptying equation for liquids (first-order kinetics)."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np


def compute_gastric_emptying_liquid(t: float, V0: float, k: float) -> float:
    """
    Calculate gastric volume remaining using first-order kinetics (liquids).

    Parameters
    ----------
    t : float
        Time (minutes)
    V0 : float
        Initial volume (mL)
    k : float
        Emptying rate constant (1/min)

    Returns
    -------
    float
        Remaining volume (mL)
    """
    return V0 * np.exp(-k * t)


gastric_emptying_liquid = create_equation(
    id="gastric_emptying_liquid",
    output_units='mL',
    name="Gastric Emptying (Liquids)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"V(t) = V_0 \times e^{-kt}",
    simplified="V(t) = V₀ × e^(-k×t)",
    description="First-order gastric emptying kinetics for liquids, with half-life t₁/₂ = ln(2)/k ≈ 10-20 min",
    compute_func=compute_gastric_emptying_liquid,
    parameters=[
        Parameter(
            name="t",
            description="Time",
            units="min",
            symbol="t",
            physiological_range=(0.0, 180.0)
        ),
        Parameter(
            name="V0",
            description="Initial volume",
            units="mL",
            symbol="V_0",
            physiological_range=(100.0, 1000.0)
        ),
        Parameter(
            name="k",
            description="Emptying rate constant (k = ln(2)/t₁/₂)",
            units="1/min",
            symbol="k",
            default_value=0.05,
            physiological_range=(0.03, 0.07)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(gastric_emptying_liquid)

"""Gastric emptying equation for solids (lag phase + linear)."""


def compute_gastric_emptying_solid(t: float, V0: float, t_lag: float, r: float) -> float:
    """
    Calculate gastric volume remaining for solids (lag phase + linear emptying).

    Parameters
    ----------
    t : float
        Time (minutes)
    V0 : float
        Initial volume (g)
    t_lag : float
        Lag phase duration (minutes)
    r : float
        Emptying rate (kcal/min or g/min)

    Returns
    -------
    float
        Remaining volume (g)
    """
    if t < t_lag:
        return V0
    else:
        return max(0.0, V0 - r * (t - t_lag))


gastric_emptying_solid = create_equation(
    id="gastric_emptying_solid",
    output_units='g',
    name="Gastric Emptying (Solids)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"V(t) = \begin{cases} V_0 & t < t_{\text{lag}} \\ V_0 - r(t - t_{\text{lag}}) & t \geq t_{\text{lag}} \end{cases}",
    simplified="V(t) = V₀ if t < t_lag, else V₀ - r×(t - t_lag)",
    description="Gastric emptying for solids with initial lag phase followed by linear emptying at ~1-2 kcal/min",
    compute_func=compute_gastric_emptying_solid,
    parameters=[
        Parameter(
            name="t",
            description="Time",
            units="min",
            symbol="t",
            physiological_range=(0.0, 360.0)
        ),
        Parameter(
            name="V0",
            description="Initial volume",
            units="g",
            symbol="V_0",
            physiological_range=(50.0, 500.0)
        ),
        Parameter(
            name="t_lag",
            description="Lag phase duration",
            units="min",
            symbol=r"t_{\text{lag}}",
            default_value=30.0,
            physiological_range=(10.0, 60.0)
        ),
        Parameter(
            name="r",
            description="Emptying rate",
            units="g/min",
            symbol="r",
            default_value=1.5,
            physiological_range=(1.0, 2.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(gastric_emptying_solid)

"""Peristalsis propagation velocity equation."""


def compute_peristalsis_velocity(wavelength: float, frequency: float) -> float:
    """
    Calculate peristaltic wave propagation velocity.

    Parameters
    ----------
    wavelength : float
        Wavelength of peristaltic contraction (cm)
    frequency : float
        Contraction frequency (Hz)

    Returns
    -------
    float
        Propagation velocity (cm/s)
    """
    return wavelength * frequency


peristalsis_velocity = create_equation(
    id="peristalsis_velocity",
    output_units='cm/s',
    name="Peristalsis Propagation Velocity",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"v = \lambda \times f",
    simplified="v = λ × f",
    description="Velocity of peristaltic wave propagation along GI tract",
    compute_func=compute_peristalsis_velocity,
    parameters=[
        Parameter(
            name="wavelength",
            description="Wavelength of peristaltic contraction",
            units="cm",
            symbol=r"\lambda",
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="frequency",
            description="Contraction frequency",
            units="Hz",
            symbol="f",
            physiological_range=(0.01, 0.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(peristalsis_velocity)

"""Slow wave oscillation equation for GI smooth muscle."""


def compute_slow_wave(t: float, V_rest: float = -60.0, A: float = 15.0, f: float = 0.05) -> float:
    """
    Calculate membrane potential during slow wave oscillation.

    Parameters
    ----------
    t : float
        Time (seconds)
    V_rest : float
        Resting membrane potential (mV), default -60 mV
    A : float
        Amplitude of oscillation (mV), default 15 mV
    f : float
        Frequency (Hz), default 0.05 Hz (3/min for stomach)

    Returns
    -------
    float
        Membrane potential (mV)
    """
    return V_rest + A * np.sin(2 * np.pi * f * t)


slow_wave = create_equation(
    id="gi_slow_wave",
    output_units='mV',
    name="GI Slow Wave Oscillation",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"V(t) = V_{\text{rest}} + A \times \sin(2\pi f t)",
    simplified="V(t) = V_rest + A × sin(2πft)",
    description="Slow wave membrane potential oscillation generated by interstitial cells of Cajal (ICC)",
    compute_func=compute_slow_wave,
    parameters=[
        Parameter(
            name="t",
            description="Time",
            units="s",
            symbol="t",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="V_rest",
            description="Resting membrane potential",
            units="mV",
            symbol=r"V_{\text{rest}}",
            default_value=-60.0,
            physiological_range=(-70.0, -50.0)
        ),
        Parameter(
            name="A",
            description="Amplitude of oscillation",
            units="mV",
            symbol="A",
            default_value=15.0,
            physiological_range=(10.0, 20.0)
        ),
        Parameter(
            name="f",
            description="Frequency (stomach: 0.05-0.067 Hz, duodenum: 0.18-0.2 Hz, ileum: 0.13-0.15 Hz)",
            units="Hz",
            symbol="f",
            default_value=0.05,
            physiological_range=(0.03, 0.2)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(slow_wave)

"""Transit time calculation for GI segments."""


def compute_transit_time(length: float, velocity: float) -> float:
    """
    Calculate transit time through a GI segment.

    Parameters
    ----------
    length : float
        Length of GI segment (cm)
    velocity : float
        Propagation velocity (cm/s)

    Returns
    -------
    float
        Transit time (seconds)
    """
    return length / velocity


transit_time = create_equation(
    id="gi_transit_time",
    output_units='s',
    name="GI Segment Transit Time",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"t_{\text{transit}} = \frac{L}{v}",
    simplified="t_transit = L / v",
    description="Transit time through GI segment based on length and propagation velocity",
    compute_func=compute_transit_time,
    parameters=[
        Parameter(
            name="length",
            description="Length of GI segment",
            units="cm",
            symbol="L",
            physiological_range=(10.0, 600.0)
        ),
        Parameter(
            name="velocity",
            description="Propagation velocity",
            units="cm/s",
            symbol="v",
            physiological_range=(0.5, 10.0)
        )
    ],
    depends_on=["peristalsis_velocity"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.1"
    )
)

register_equation(transit_time)


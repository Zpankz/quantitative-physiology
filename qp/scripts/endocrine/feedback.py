"""feedback equations"""

"""
Feedback gain in endocrine regulation.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_feedback_gain(delta_tropic: float, delta_target: float) -> float:
    """
    Calculate feedback loop gain.

    Parameters
    ----------
    delta_tropic : float
        Change in tropic hormone concentration
    delta_target : float
        Change in target hormone concentration

    Returns
    -------
    float
        Feedback gain G (dimensionless)

    Notes
    -----
    High gain = tight regulation around setpoint.
    Negative value indicates negative feedback.
    """
    return delta_tropic / delta_target


# Create equation
feedback_gain_equation = create_equation(
    id="feedback_gain",
    output_units='dimensionless',
    name="Feedback Loop Gain",
    category=EquationCategory.ENDOCRINE,
    latex=r"G = \frac{\Delta[\text{Tropic}]}{\Delta[\text{Target}]}",
    simplified="G = Δ[Tropic] / Δ[Target]",
    description="Gain of negative feedback loop. High gain indicates tight regulation "
                "around hormonal setpoint. Determines sensitivity of response to perturbations.",
    compute_func=compute_feedback_gain,
    parameters=[
        Parameter(
            name="delta_tropic",
            description="Change in tropic hormone",
            units="arbitrary units",
            symbol=r"\Delta[\text{Tropic}]",
            physiological_range=(-100.0, 100.0)
        ),
        Parameter(
            name="delta_target",
            description="Change in target hormone",
            units="arbitrary units",
            symbol=r"\Delta[\text{Target}]",
            physiological_range=(-100.0, 100.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.3"
    )
)

# Register globally
register_equation(feedback_gain_equation)

"""
Negative feedback regulation of target hormone dynamics.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_target_derivative(tropic_conc: float, target_conc: float,
                               k_stim: float, k_deg: float) -> float:
    """
    Calculate rate of change of target hormone concentration.

    Parameters
    ----------
    tropic_conc : float
        Tropic hormone concentration (e.g., TSH, ACTH)
    target_conc : float
        Target hormone concentration (e.g., T4, cortisol)
    k_stim : float
        Stimulation rate constant (1/time)
    k_deg : float
        Degradation rate constant (1/time)

    Returns
    -------
    float
        d[Target]/dt
    """
    return k_stim * tropic_conc - k_deg * target_conc


# Create equation
target_feedback_equation = create_equation(
    id="feedback_target_dynamics",
    output_units='arbitrary/time',
    name="Target Hormone Dynamics (Negative Feedback)",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[\text{Target}]}{dt} = k_{stim} \times [\text{Tropic}] - k_{deg} \times [\text{Target}]",
    simplified="d[Target]/dt = k_stim × [Tropic] - k_deg × [Target]",
    description="Rate equation for target hormone under tropic hormone stimulation. "
                "Used in negative feedback loops (e.g., TSH→T4, ACTH→cortisol).",
    compute_func=compute_target_derivative,
    parameters=[
        Parameter(
            name="tropic_conc",
            description="Tropic hormone concentration",
            units="arbitrary units",
            symbol="[Tropic]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="target_conc",
            description="Target hormone concentration",
            units="arbitrary units",
            symbol="[Target]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="k_stim",
            description="Stimulation rate constant",
            units="1/time",
            symbol="k_{stim}",
            physiological_range=(0.01, 10.0)
        ),
        Parameter(
            name="k_deg",
            description="Degradation rate constant",
            units="1/time",
            symbol="k_{deg}",
            physiological_range=(0.001, 1.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.3"
    )
)

# Register globally
register_equation(target_feedback_equation)

"""
Negative feedback regulation of tropic hormone dynamics.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_tropic_derivative(target_conc: float, k_basal: float, k_fb: float) -> float:
    """
    Calculate rate of change of tropic hormone with feedback.

    Parameters
    ----------
    target_conc : float
        Target hormone concentration providing feedback
    k_basal : float
        Basal secretion rate
    k_fb : float
        Feedback inhibition constant

    Returns
    -------
    float
        d[Tropic]/dt
    """
    return k_basal - k_fb * target_conc


# Create equation
tropic_feedback_equation = create_equation(
    id="feedback_tropic_dynamics",
    output_units='arbitrary/time',
    name="Tropic Hormone Dynamics (Negative Feedback)",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[\text{Tropic}]}{dt} = k_{basal} - k_{fb} \times [\text{Target}]",
    simplified="d[Tropic]/dt = k_basal - k_fb × [Target]",
    description="Rate equation for tropic hormone with negative feedback from target hormone. "
                "Steady-state setpoint: [Target]_ss = k_basal / k_fb.",
    compute_func=compute_tropic_derivative,
    parameters=[
        Parameter(
            name="target_conc",
            description="Target hormone concentration (feedback signal)",
            units="arbitrary units",
            symbol="[Target]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="k_basal",
            description="Basal secretion rate",
            units="concentration/time",
            symbol="k_{basal}",
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_fb",
            description="Feedback inhibition constant",
            units="1/time",
            symbol="k_{fb}",
            physiological_range=(0.001, 1.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.3"
    )
)

# Register globally
register_equation(tropic_feedback_equation)


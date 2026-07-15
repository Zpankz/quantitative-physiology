"""reproductive equations"""

"""
LH surge in response to estradiol (positive feedback).

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_lh_surge(estradiol: float, threshold: float = 200.0,
                    max_LH: float = 80.0, baseline: float = 5.0) -> float:
    """
    Calculate LH response to estradiol (switches from negative to positive feedback).

    Parameters
    ----------
    estradiol : float
        Estradiol concentration (pg/mL)
    threshold : float
        E2 threshold for positive feedback switch (pg/mL)
    max_LH : float
        Maximum LH surge amplitude (mU/mL)
    baseline : float
        Baseline LH (mU/mL)

    Returns
    -------
    float
        LH concentration (mU/mL)

    Notes
    -----
    Unique biphasic feedback:
    - Low E2: negative feedback (↓ LH)
    - High E2 (>200 pg/mL, sustained >36h): positive feedback (LH surge)

    LH surge triggers ovulation ~24-36 hours later.

    Hormone levels across cycle:
    - Early follicular: E2 20-50 pg/mL, LH 2-15 mU/mL
    - Preovulatory: E2 200-400 pg/mL, LH 20-100 mU/mL (surge)
    - Mid-luteal: E2 100-200 pg/mL, LH 2-15 mU/mL
    """
    if estradiol < threshold:
        # Negative feedback
        return baseline * threshold / (threshold + estradiol)
    else:
        # Positive feedback (surge)
        excess = estradiol - threshold
        return baseline + max_LH * excess / (50.0 + excess)


# Create equation
lh_surge_equation = create_equation(
    id="reproductive_lh_surge",
    output_units='mU/mL',
    name="LH Surge (Estradiol Positive Feedback)",
    category=EquationCategory.ENDOCRINE,
    latex=r"LH = \begin{cases} \frac{\text{baseline} \times \text{threshold}}{\text{threshold} + E_2} & E_2 < \text{threshold} \\ \text{baseline} + \frac{\text{max\_LH} \times (E_2 - \text{threshold})}{50 + (E_2 - \text{threshold})} & E_2 \geq \text{threshold} \end{cases}",
    simplified="LH = negative_feedback if E2<threshold else positive_feedback_surge",
    description="LH response to estradiol showing unique switch from negative to positive feedback. "
                "High sustained E2 (>200 pg/mL) triggers LH surge and ovulation.",
    compute_func=compute_lh_surge,
    parameters=[
        Parameter(
            name="estradiol",
            description="Estradiol (E2) concentration",
            units="pg/mL",
            symbol="E_2",
            physiological_range=(10.0, 500.0)
        ),
        Parameter(
            name="threshold",
            description="E2 threshold for positive feedback",
            units="pg/mL",
            symbol="threshold",
            default_value=200.0,
            physiological_range=(150.0, 250.0)
        ),
        Parameter(
            name="max_LH",
            description="Maximum LH surge amplitude",
            units="mU/mL",
            symbol="LH_{max}",
            default_value=80.0,
            physiological_range=(50.0, 120.0)
        ),
        Parameter(
            name="baseline",
            description="Baseline LH concentration",
            units="mU/mL",
            symbol="LH_{baseline}",
            default_value=5.0,
            physiological_range=(2.0, 10.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.8"
    )
)

# Register globally
register_equation(lh_surge_equation)

"""
Basal body temperature elevation from progesterone.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_temperature_elevation(progesterone: float,
                                  T_baseline: float = 36.5) -> float:
    """
    Calculate basal body temperature from progesterone effect.

    Parameters
    ----------
    progesterone : float
        Progesterone concentration (ng/mL)
    T_baseline : float
        Baseline body temperature (°C)

    Returns
    -------
    float
        Body temperature (°C)

    Notes
    -----
    Progesterone is thermogenic:
    - Increases basal body temperature ~0.3°C
    - Temperature rise occurs after ovulation (luteal phase)
    - Used for natural family planning (fertility awareness)

    Progesterone across cycle:
    - Follicular phase: <1 ng/mL (low, no temp rise)
    - Luteal phase: 5-20 ng/mL (high, temp elevation)

    Temperature shift indicates ovulation has occurred.
    """
    delta_T = 0.3 * progesterone / (5.0 + progesterone)
    return T_baseline + delta_T


# Create equation
progesterone_temp_equation = create_equation(
    id="reproductive_progesterone_temperature",
    output_units='°C',
    name="Progesterone Basal Body Temperature",
    category=EquationCategory.ENDOCRINE,
    latex=r"T = T_{baseline} + 0.3 \times \frac{[P_4]}{5 + [P_4]}",
    simplified="T = T_baseline + 0.3 × [P4] / (5 + [P4])",
    description="Basal body temperature elevation from progesterone thermogenic effect. "
                "Temperature rises ~0.3°C in luteal phase after ovulation.",
    compute_func=compute_temperature_elevation,
    parameters=[
        Parameter(
            name="progesterone",
            description="Progesterone (P4) concentration",
            units="ng/mL",
            symbol="[P_4]",
            physiological_range=(0.0, 25.0)
        ),
        Parameter(
            name="T_baseline",
            description="Baseline body temperature",
            units="°C",
            symbol="T_{baseline}",
            default_value=36.5,
            physiological_range=(36.0, 37.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.8"
    )
)

# Register globally
register_equation(progesterone_temp_equation)


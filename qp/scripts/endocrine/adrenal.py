"""adrenal equations"""

"""
Aldosterone regulation by angiotensin II and potassium.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_aldosterone_rate(AngII: float, K_plasma: float,
                             k_AngII: float = 1.0, k_K: float = 1.0) -> float:
    """
    Calculate aldosterone secretion rate.

    Parameters
    ----------
    AngII : float
        Angiotensin II concentration (primary stimulus)
    K_plasma : float
        Plasma potassium concentration (mM)
    k_AngII : float
        AngII sensitivity constant
    k_K : float
        K+ sensitivity constant

    Returns
    -------
    float
        Aldosterone secretion rate (proportional)

    Notes
    -----
    Primary stimuli:
    - Angiotensin II (RAAS activation)
    - Hyperkalemia (direct effect)
    - ACTH (minor, permissive)
    """
    return k_AngII * AngII * k_K * K_plasma


# Create equation
aldosterone_equation = create_equation(
    id="aldosterone_regulation",
    output_units='arbitrary',
    name="Aldosterone Regulation",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{Aldosterone} \propto [\text{Ang II}] \times [K^+]",
    simplified="Aldosterone ∝ [Ang II] × [K+]",
    description="Aldosterone secretion from zona glomerulosa. Primary regulation by "
                "angiotensin II (RAAS) and plasma potassium (hyperkalemia stimulates).",
    compute_func=compute_aldosterone_rate,
    parameters=[
        Parameter(
            name="AngII",
            description="Angiotensin II concentration",
            units="pg/mL",
            symbol="[Ang II]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="K_plasma",
            description="Plasma potassium concentration",
            units="mM",
            symbol="[K^+]",
            physiological_range=(3.0, 6.0)
        ),
        Parameter(
            name="k_AngII",
            description="Angiotensin II sensitivity",
            units="arbitrary",
            symbol="k_{AngII}",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_K",
            description="Potassium sensitivity",
            units="arbitrary",
            symbol="k_K",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.5"
    )
)

# Register globally
register_equation(aldosterone_equation)

"""
ACTH dynamics in HPA axis.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_acth_derivative(CRH: float, ACTH: float, cortisol: float,
                            k_CRH: float, k_fb: float, k_deg: float) -> float:
    """
    Calculate rate of change of ACTH concentration.

    Parameters
    ----------
    CRH : float
        CRH concentration (stimulation)
    ACTH : float
        ACTH concentration
    cortisol : float
        Cortisol concentration (feedback)
    k_CRH : float
        CRH stimulation constant
    k_fb : float
        Cortisol feedback constant
    k_deg : float
        ACTH degradation rate constant

    Returns
    -------
    float
        d[ACTH]/dt
    """
    return k_CRH * CRH - k_fb * cortisol - k_deg * ACTH


# Create equation
acth_dynamics_equation = create_equation(
    id="hpa_acth_dynamics",
    output_units='pg/(mL*time)',
    name="HPA Axis ACTH Dynamics",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[ACTH]}{dt} = k_{CRH} \times [CRH] - k_{fb} \times [Cortisol] - k_{deg} \times [ACTH]",
    simplified="d[ACTH]/dt = k_CRH × [CRH] - k_fb × [Cortisol] - k_deg × [ACTH]",
    description="ACTH (adrenocorticotropic hormone) dynamics in anterior pituitary. "
                "Stimulated by CRH, inhibited by cortisol.",
    compute_func=compute_acth_derivative,
    parameters=[
        Parameter(
            name="CRH",
            description="CRH concentration",
            units="arbitrary units",
            symbol="[CRH]",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="ACTH",
            description="ACTH concentration",
            units="pg/mL",
            symbol="[ACTH]",
            physiological_range=(0.0, 200.0)
        ),
        Parameter(
            name="cortisol",
            description="Cortisol concentration",
            units="μg/dL",
            symbol="[Cortisol]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="k_CRH",
            description="CRH stimulation constant",
            units="1/time",
            symbol="k_{CRH}",
            physiological_range=(0.1, 5.0)
        ),
        Parameter(
            name="k_fb",
            description="Cortisol feedback constant",
            units="1/time",
            symbol="k_{fb}",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="k_deg",
            description="ACTH degradation rate",
            units="1/time",
            symbol="k_{deg}",
            physiological_range=(0.1, 2.0)
        )
    ],
    depends_on=["hpa_crh_dynamics"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.5"
    )
)

# Register globally
register_equation(acth_dynamics_equation)

"""
Cortisol dynamics in HPA axis.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_cortisol_derivative(ACTH: float, cortisol: float,
                                k_ACTH: float, k_clear: float) -> float:
    """
    Calculate rate of change of cortisol concentration.

    Parameters
    ----------
    ACTH : float
        ACTH concentration (stimulation)
    cortisol : float
        Cortisol concentration
    k_ACTH : float
        ACTH stimulation constant
    k_clear : float
        Cortisol clearance rate constant

    Returns
    -------
    float
        d[Cortisol]/dt

    Notes
    -----
    Daily cortisol production: 10-20 mg/day
    Stress response can increase 10-fold
    Half-life: 60-90 minutes
    """
    return k_ACTH * ACTH - k_clear * cortisol


# Create equation
cortisol_dynamics_equation = create_equation(
    id="hpa_cortisol_dynamics",
    output_units='μg/(dL*time)',
    name="HPA Axis Cortisol Dynamics",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[Cortisol]}{dt} = k_{ACTH} \times [ACTH] - k_{clear} \times [Cortisol]",
    simplified="d[Cortisol]/dt = k_ACTH × [ACTH] - k_clear × [Cortisol]",
    description="Cortisol secretion from adrenal cortex. Stimulated by ACTH, "
                "cleared by hepatic metabolism. Half-life ~60-90 minutes.",
    compute_func=compute_cortisol_derivative,
    parameters=[
        Parameter(
            name="ACTH",
            description="ACTH concentration",
            units="pg/mL",
            symbol="[ACTH]",
            physiological_range=(0.0, 200.0)
        ),
        Parameter(
            name="cortisol",
            description="Cortisol concentration",
            units="μg/dL",
            symbol="[Cortisol]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="k_ACTH",
            description="ACTH stimulation constant",
            units="1/time",
            symbol="k_{ACTH}",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="k_clear",
            description="Cortisol clearance rate",
            units="1/time",
            symbol="k_{clear}",
            physiological_range=(0.01, 0.5)
        )
    ],
    depends_on=["hpa_acth_dynamics"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.5"
    )
)

# Register globally
register_equation(cortisol_dynamics_equation)

"""
CRH dynamics in HPA axis with stress and cortisol feedback.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_crh_derivative(CRH: float, cortisol: float, k_stress: float,
                           k_cort: float, k_deg: float) -> float:
    """
    Calculate rate of change of CRH concentration.

    Parameters
    ----------
    CRH : float
        CRH concentration
    cortisol : float
        Cortisol concentration (feedback)
    k_stress : float
        Stress-induced secretion rate
    k_cort : float
        Cortisol feedback inhibition constant
    k_deg : float
        CRH degradation rate constant

    Returns
    -------
    float
        d[CRH]/dt
    """
    return k_stress - k_cort * cortisol - k_deg * CRH


# Create equation
crh_dynamics_equation = create_equation(
    id="hpa_crh_dynamics",
    output_units='arbitrary',
    name="HPA Axis CRH Dynamics",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[CRH]}{dt} = k_{stress} - k_{cort} \times [Cortisol] - k_{deg} \times [CRH]",
    simplified="d[CRH]/dt = k_stress - k_cort × [Cortisol] - k_deg × [CRH]",
    description="CRH (corticotropin-releasing hormone) dynamics in hypothalamus. "
                "Stimulated by stress, inhibited by cortisol negative feedback.",
    compute_func=compute_crh_derivative,
    parameters=[
        Parameter(
            name="CRH",
            description="CRH concentration",
            units="arbitrary units",
            symbol="[CRH]",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="cortisol",
            description="Cortisol concentration",
            units="μg/dL",
            symbol="[Cortisol]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="k_stress",
            description="Stress-induced secretion rate",
            units="concentration/time",
            symbol="k_{stress}",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="k_cort",
            description="Cortisol feedback constant",
            units="1/time",
            symbol="k_{cort}",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="k_deg",
            description="CRH degradation rate",
            units="1/time",
            symbol="k_{deg}",
            physiological_range=(0.1, 2.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.5"
    )
)

# Register globally
register_equation(crh_dynamics_equation)


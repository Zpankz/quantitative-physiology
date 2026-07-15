"""thyroid equations"""

"""
T4 dynamics with TSH stimulation and peripheral conversion.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_t4_derivative(TSH: float, T4: float, k_TSH: float,
                         k_conv: float, k_clear: float) -> float:
    """
    Calculate rate of change of T4 concentration.

    Parameters
    ----------
    TSH : float
        TSH concentration (stimulation)
    T4 : float
        T4 concentration
    k_TSH : float
        TSH stimulation constant
    k_conv : float
        Conversion to T3 rate (deiodinase)
    k_clear : float
        Direct clearance rate

    Returns
    -------
    float
        d[T4]/dt

    Notes
    -----
    T4 half-life: 6-7 days
    ~80% of circulating T3 comes from peripheral T4→T3 conversion
    """
    return k_TSH * TSH - k_conv * T4 - k_clear * T4


# Create equation
t4_dynamics_equation = create_equation(
    id="thyroid_t4_dynamics",
    output_units='μg/(dL*time)',
    name="T4 Dynamics",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[T4]}{dt} = k_{TSH} \times [TSH] - k_{conv} \times [T4] - k_{clear} \times [T4]",
    simplified="d[T4]/dt = k_TSH × [TSH] - k_conv × [T4] - k_clear × [T4]",
    description="T4 dynamics: TSH-stimulated production, peripheral conversion to T3, "
                "and direct clearance. Half-life ~6-7 days.",
    compute_func=compute_t4_derivative,
    parameters=[
        Parameter(
            name="TSH",
            description="TSH concentration",
            units="mU/L",
            symbol="[TSH]",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="T4",
            description="T4 concentration",
            units="μg/dL",
            symbol="[T4]",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="k_TSH",
            description="TSH stimulation constant",
            units="1/time",
            symbol="k_{TSH}",
            physiological_range=(0.1, 5.0)
        ),
        Parameter(
            name="k_conv",
            description="T4→T3 conversion rate",
            units="1/time",
            symbol="k_{conv}",
            physiological_range=(0.001, 0.1)
        ),
        Parameter(
            name="k_clear",
            description="T4 clearance rate",
            units="1/time",
            symbol="k_{clear}",
            physiological_range=(0.001, 0.1)
        )
    ],
    depends_on=["thyroid_t4_production", "thyroid_tsh_dynamics"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.4"
    )
)

# Register globally
register_equation(t4_dynamics_equation)

"""
T4 production rate as function of TSH.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_t4_production(TSH: float, Vmax: float = 100.0, Km: float = 2.0) -> float:
    """
    Calculate T4 production rate using Michaelis-Menten kinetics.

    Parameters
    ----------
    TSH : float
        TSH concentration (mU/L)
    Vmax : float
        Maximum production rate (μg/day)
    Km : float
        Michaelis constant (mU/L)

    Returns
    -------
    float
        T4 production rate (μg/day)

    Notes
    -----
    Daily T4 production: ~80-100 μg/day (all from thyroid)
    Daily T3 production: ~30-40 μg/day (20% thyroid, 80% peripheral conversion)
    """
    return Vmax * TSH / (Km + TSH)


# Create equation
t4_production_equation = create_equation(
    id="thyroid_t4_production",
    output_units='μg/day',
    name="T4 Production Rate",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{T4 production} = \frac{V_{max} \times TSH}{K_m + TSH}",
    simplified="T4_production = V_max × TSH / (K_m + TSH)",
    description="T4 synthesis and secretion from thyroid follicular cells. "
                "Follows Michaelis-Menten kinetics with TSH stimulation.",
    compute_func=compute_t4_production,
    parameters=[
        Parameter(
            name="TSH",
            description="TSH concentration",
            units="mU/L",
            symbol="TSH",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="Vmax",
            description="Maximum production rate",
            units="μg/day",
            symbol="V_{max}",
            default_value=100.0,
            physiological_range=(50.0, 200.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mU/L",
            symbol="K_m",
            default_value=2.0,
            physiological_range=(1.0, 5.0)
        )
    ],
    depends_on=["thyroid_tsh_response"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.4"
    )
)

# Register globally
register_equation(t4_production_equation)

"""
TSH secretion as function of free T4 (negative feedback).

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_tsh_response(fT4: float, Kd: float = 1.0, n: float = 2.0,
                         TSH_max: float = 10.0) -> float:
    """
    Calculate TSH secretion as inverse function of free T4.

    Parameters
    ----------
    fT4 : float
        Free T4 concentration (ng/dL)
    Kd : float
        Feedback setpoint (ng/dL)
    n : float
        Hill coefficient (steepness of feedback)
    TSH_max : float
        Maximum TSH concentration (mU/L)

    Returns
    -------
    float
        TSH concentration (mU/L)

    Notes
    -----
    Steep negative feedback (n ≈ 2) provides tight regulation.
    Normal TSH: 0.4-4.0 mU/L
    Normal free T4: 0.8-1.8 ng/dL
    """
    return TSH_max / (1.0 + (fT4 / Kd) ** n)


# Create equation
tsh_response_equation = create_equation(
    id="thyroid_tsh_response",
    output_units='mU/L',
    name="TSH Response to T4 Feedback",
    category=EquationCategory.ENDOCRINE,
    latex=r"TSH = \frac{TSH_{max}}{1 + \left(\frac{fT4}{K_d}\right)^n}",
    simplified="TSH = TSH_max / (1 + (fT4/K_d)^n)",
    description="TSH secretion from pituitary as inverse function of free T4 (negative feedback). "
                "Hill coefficient n ≈ 2 creates steep, sensitive response.",
    compute_func=compute_tsh_response,
    parameters=[
        Parameter(
            name="fT4",
            description="Free T4 concentration",
            units="ng/dL",
            symbol="fT4",
            physiological_range=(0.0, 5.0)
        ),
        Parameter(
            name="Kd",
            description="Feedback setpoint",
            units="ng/dL",
            symbol="K_d",
            default_value=1.0,
            physiological_range=(0.5, 2.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient (feedback steepness)",
            units="dimensionless",
            symbol="n",
            default_value=2.0,
            physiological_range=(1.0, 4.0)
        ),
        Parameter(
            name="TSH_max",
            description="Maximum TSH concentration",
            units="mU/L",
            symbol="TSH_{max}",
            default_value=10.0,
            physiological_range=(5.0, 20.0)
        )
    ],
    depends_on=["feedback_tropic_dynamics"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.4"
    )
)

# Register globally
register_equation(tsh_response_equation)

"""
Coupled TSH-T4 dynamics with feedback.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_tsh_derivative(fT4: float, TSH: float, k_TRH: float,
                           k_T4: float, n: float, k_deg: float) -> float:
    """
    Calculate rate of change of TSH with T4 feedback.

    Parameters
    ----------
    fT4 : float
        Free T4 concentration
    TSH : float
        TSH concentration
    k_TRH : float
        TRH-stimulated basal secretion
    k_T4 : float
        T4 feedback strength
    n : float
        Hill coefficient (~2 for steep feedback)
    k_deg : float
        TSH degradation rate

    Returns
    -------
    float
        d[TSH]/dt
    """
    return k_TRH - k_T4 * (fT4 ** n) - k_deg * TSH


# Create equation
tsh_dynamics_equation = create_equation(
    id="thyroid_tsh_dynamics",
    output_units='mU/(L*time)',
    name="TSH Dynamics with T4 Feedback",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{d[TSH]}{dt} = k_{TRH} - k_{T4} \times [fT4]^n - k_{deg} \times [TSH]",
    simplified="d[TSH]/dt = k_TRH - k_T4 × [fT4]^n - k_deg × [TSH]",
    description="TSH secretion dynamics with steep negative feedback from free T4. "
                "Power term (n ≈ 2) creates high-gain regulation.",
    compute_func=compute_tsh_derivative,
    parameters=[
        Parameter(
            name="fT4",
            description="Free T4 concentration",
            units="ng/dL",
            symbol="[fT4]",
            physiological_range=(0.0, 5.0)
        ),
        Parameter(
            name="TSH",
            description="TSH concentration",
            units="mU/L",
            symbol="[TSH]",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="k_TRH",
            description="TRH-stimulated basal secretion",
            units="mU/(L·time)",
            symbol="k_{TRH}",
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k_T4",
            description="T4 feedback strength",
            units="1/time",
            symbol="k_{T4}",
            physiological_range=(0.01, 1.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=2.0,
            physiological_range=(1.5, 3.0)
        ),
        Parameter(
            name="k_deg",
            description="TSH degradation rate",
            units="1/time",
            symbol="k_{deg}",
            physiological_range=(0.1, 2.0)
        )
    ],
    depends_on=["thyroid_tsh_response"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.4"
    )
)

# Register globally
register_equation(tsh_dynamics_equation)


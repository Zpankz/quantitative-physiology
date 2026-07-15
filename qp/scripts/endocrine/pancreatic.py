"""pancreatic equations"""

"""
Glucose-stimulated insulin secretion (GSIS).

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_gsis(glucose: float, I_basal: float = 5.0, I_max: float = 50.0,
                EC50: float = 6.0, n: float = 2.5) -> float:
    """
    Calculate insulin secretion rate from glucose concentration.

    Parameters
    ----------
    glucose : float
        Blood glucose concentration (mM)
    I_basal : float
        Basal insulin secretion rate (μU/mL/min)
    I_max : float
        Maximum insulin secretion above basal (μU/mL/min)
    EC50 : float
        Glucose concentration for half-maximal response (mM)
    n : float
        Hill coefficient (cooperativity)

    Returns
    -------
    float
        Insulin secretion rate (μU/mL/min)

    Notes
    -----
    EC50 ≈ 5-6 mM glucose
    n ≈ 2-3 (sigmoidal dose-response)
    I_max ≈ 10× I_basal
    Biphasic response: first phase 2-5 min, second phase 10-60+ min
    """
    stimulation = (glucose ** n) / (EC50 ** n + glucose ** n)
    return I_basal + I_max * stimulation


# Create equation
gsis_equation = create_equation(
    id="pancreatic_gsis",
    output_units='µU/mL/min',
    name="Glucose-Stimulated Insulin Secretion",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{Insulin} = I_{basal} + I_{max} \times \frac{[Glucose]^n}{EC_{50}^n + [Glucose]^n}",
    simplified="Insulin = I_basal + I_max × [Glucose]^n / (EC50^n + [Glucose]^n)",
    description="Insulin secretion from pancreatic β-cells as sigmoidal function of glucose. "
                "Hill equation captures cooperative glucose sensing (n ≈ 2-3).",
    compute_func=compute_gsis,
    parameters=[
        Parameter(
            name="glucose",
            description="Blood glucose concentration",
            units="mM",
            symbol="[Glucose]",
            physiological_range=(2.0, 20.0)
        ),
        Parameter(
            name="I_basal",
            description="Basal insulin secretion",
            units="μU/mL/min",
            symbol="I_{basal}",
            default_value=5.0,
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="I_max",
            description="Maximum insulin above basal",
            units="μU/mL/min",
            symbol="I_{max}",
            default_value=50.0,
            physiological_range=(20.0, 100.0)
        ),
        Parameter(
            name="EC50",
            description="Half-maximal glucose concentration",
            units="mM",
            symbol="EC_{50}",
            default_value=6.0,
            physiological_range=(4.0, 8.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=2.5,
            physiological_range=(2.0, 3.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.6"
    )
)

# Register globally
register_equation(gsis_equation)

"""
HOMA-IR: Homeostatic Model Assessment of Insulin Resistance.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_homa_ir(fasting_glucose_mmol: float, fasting_insulin_uU: float) -> float:
    """
    Calculate HOMA-IR insulin resistance index.

    Parameters
    ----------
    fasting_glucose_mmol : float
        Fasting glucose concentration (mmol/L)
    fasting_insulin_uU : float
        Fasting insulin concentration (μU/mL)

    Returns
    -------
    float
        HOMA-IR (dimensionless)

    Notes
    -----
    Normal HOMA-IR: <2.5
    Insulin resistance: >2.5
    Conversion: glucose (mg/dL) ÷ 18 = mmol/L
    """
    return (fasting_glucose_mmol * fasting_insulin_uU) / 22.5


# Create equation
homa_ir_equation = create_equation(
    id="pancreatic_homa_ir",
    output_units='dimensionless',
    name="HOMA-IR Insulin Resistance Index",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{HOMA-IR} = \frac{\text{Glucose}_{mmol/L} \times \text{Insulin}_{\mu U/mL}}{22.5}",
    simplified="HOMA-IR = (Glucose_mmol × Insulin_μU) / 22.5",
    description="Homeostatic Model Assessment of Insulin Resistance. "
                "Calculated from fasting glucose and insulin. Normal <2.5.",
    compute_func=compute_homa_ir,
    parameters=[
        Parameter(
            name="fasting_glucose_mmol",
            description="Fasting glucose concentration",
            units="mmol/L",
            symbol="Glucose",
            physiological_range=(3.0, 15.0)
        ),
        Parameter(
            name="fasting_insulin_uU",
            description="Fasting insulin concentration",
            units="μU/mL",
            symbol="Insulin",
            physiological_range=(2.0, 50.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.6"
    )
)

# Register globally
register_equation(homa_ir_equation)



# --- review-add 2026-07-15 ---
def compute_homa_b(fasting_glucose_mmol: float, fasting_insulin_uU: float) -> float:
    """HOMA-B fasting beta-cell function (%), companion to HOMA-IR.

    HOMA-B = 20 x Insulin / (Glucose_mmol - 3.5)."""
    return (20.0 * fasting_insulin_uU) / (fasting_glucose_mmol - 3.5)

homa_b_equation = create_equation(
    id='pancreatic_homa_b',
    name='HOMA-B Beta-Cell Function Index',
    category=EquationCategory.ENDOCRINE,
    latex=r'\\text{HOMA-B} = \\frac{20 \\times \\text{Insulin}_{\\mu U/mL}}{\\text{Glucose}_{mmol/L} - 3.5}',
    simplified='HOMA-B = (20 * Insulin_uU) / (Glucose_mmol - 3.5)',
    description='Homeostatic Model Assessment of beta-cell function (%). Fasting companion to HOMA-IR (Matthews 1985). Normal ~100%.',
    compute_func=compute_homa_b,
    output_units='percent',
    parameters=[
        Parameter(name='fasting_glucose_mmol', description='Fasting glucose', units='mmol/L', symbol='Glucose', physiological_range=(3.6, 15.0)),
        Parameter(name='fasting_insulin_uU', description='Fasting insulin', units='μU/mL', symbol='Insulin', physiological_range=(2.0, 50.0)),
    ],
    metadata=EquationMetadata(source_unit=9, source_chapter='9.6'),
)
register_equation(homa_b_equation)

"""Consolidated module for gastrointestinal.liver."""

"""Daily bilirubin production."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_bilirubin_production(Hb_turnover_g: float = 6.0, conversion_factor: float = 35.0) -> float:
    """
    Calculate daily bilirubin production from hemoglobin turnover.

    Heme → Biliverdin → Bilirubin (unconjugated)
    ~35 mg bilirubin per gram Hb

    Parameters
    ----------
    Hb_turnover_g : float
        Daily hemoglobin turnover (g/day), default 6 g/day
    conversion_factor : float
        mg bilirubin per g Hb, default 35 mg/g

    Returns
    -------
    float
        Daily bilirubin production (mg/day)
    """
    return Hb_turnover_g * conversion_factor


bilirubin_production = create_equation(
    id="bilirubin_production",
    output_units='mg/day',
    name="Daily Bilirubin Production",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Bilirubin} = \text{Hb}_{\text{turnover}} \times 35 \, \text{mg/g}",
    simplified="Bilirubin = Hb_turnover × 35 mg/g",
    description="Daily bilirubin production ~250-300 mg/day from Hb turnover. ~35 mg bilirubin per g Hb. Jaundice if >2-2.5 mg/dL",
    compute_func=compute_bilirubin_production,
    parameters=[
        Parameter(
            name="Hb_turnover_g",
            description="Daily hemoglobin turnover",
            units="g/day",
            symbol=r"\text{Hb}_{\text{turnover}}",
            default_value=6.0,
            physiological_range=(5.0, 8.0)
        ),
        Parameter(
            name="conversion_factor",
            description="mg bilirubin per g Hb",
            units="mg/g",
            symbol=r"f_{\text{conv}}",
            default_value=35.0,
            physiological_range=(30.0, 40.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(bilirubin_production)

"""Hepatic extraction ratio."""


def compute_extraction_ratio(C_in: float, C_out: float) -> float:
    """
    Calculate hepatic extraction ratio.

    E = (C_in - C_out) / C_in

    High extraction (E > 0.7): flow-limited clearance
    Low extraction (E < 0.3): capacity-limited clearance

    Parameters
    ----------
    C_in : float
        Inlet concentration (any units)
    C_out : float
        Outlet concentration (same units as C_in)

    Returns
    -------
    float
        Extraction ratio (0-1)
    """
    if C_in > 0:
        return (C_in - C_out) / C_in
    else:
        return 0.0


extraction_ratio = create_equation(
    id="extraction_ratio",
    output_units='dimensionless',
    name="Hepatic Extraction Ratio",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"E = \frac{C_{\text{in}} - C_{\text{out}}}{C_{\text{in}}}",
    simplified="E = (C_in - C_out) / C_in",
    description="Hepatic extraction ratio. High E (>0.7): flow-limited. Low E (<0.3): capacity-limited",
    compute_func=compute_extraction_ratio,
    parameters=[
        Parameter(
            name="C_in",
            description="Inlet concentration",
            units="variable",
            symbol=r"C_{\text{in}}",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="C_out",
            description="Outlet concentration",
            units="variable",
            symbol=r"C_{\text{out}}",
            physiological_range=(0.0, 1000.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(extraction_ratio)

"""First-pass effect and bioavailability."""


def compute_first_pass_bioavailability(E: float) -> float:
    """
    Calculate bioavailability after hepatic first-pass metabolism.

    Bioavailability = 1 - E

    High extraction (E close to 1) → low bioavailability
    Low extraction (E close to 0) → high bioavailability

    Parameters
    ----------
    E : float
        Hepatic extraction ratio (0-1)

    Returns
    -------
    float
        Bioavailability (0-1)
    """
    return 1.0 - E


first_pass_effect = create_equation(
    id="first_pass_effect",
    output_units='dimensionless',
    name="First-Pass Effect",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"F = 1 - E",
    simplified="F = 1 - E",
    description="Bioavailability after hepatic first-pass metabolism. High E → low F (extensive first-pass)",
    compute_func=compute_first_pass_bioavailability,
    parameters=[
        Parameter(
            name="E",
            description="Hepatic extraction ratio",
            units="dimensionless",
            symbol="E",
            physiological_range=(0.0, 1.0)
        )
    ],
    depends_on=["extraction_ratio"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(first_pass_effect)

"""Total hepatic blood flow."""


def compute_hepatic_blood_flow(portal: float = 1.1, arterial: float = 0.4) -> float:
    """
    Calculate total hepatic blood flow.

    Dual blood supply: ~75% portal vein, ~25% hepatic artery.
    Total ~1.5 L/min (~25% of cardiac output).

    Parameters
    ----------
    portal : float
        Portal venous flow (L/min), default 1.1 L/min
    arterial : float
        Hepatic arterial flow (L/min), default 0.4 L/min

    Returns
    -------
    float
        Total hepatic blood flow (L/min)
    """
    return portal + arterial


hepatic_blood_flow = create_equation(
    id="hepatic_blood_flow",
    output_units='L/min',
    name="Total Hepatic Blood Flow",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"Q_H = Q_{\text{portal}} + Q_{\text{arterial}}",
    simplified="Q_H = Q_portal + Q_arterial",
    description="Total hepatic blood flow ~1.5 L/min (~25% CO). Portal vein ~75%, hepatic artery ~25%",
    compute_func=compute_hepatic_blood_flow,
    parameters=[
        Parameter(
            name="portal",
            description="Portal venous flow",
            units="L/min",
            symbol=r"Q_{\text{portal}}",
            default_value=1.1,
            physiological_range=(0.8, 1.5)
        ),
        Parameter(
            name="arterial",
            description="Hepatic arterial flow",
            units="L/min",
            symbol=r"Q_{\text{arterial}}",
            default_value=0.4,
            physiological_range=(0.3, 0.6)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(hepatic_blood_flow)

"""Hepatic clearance."""


def compute_hepatic_clearance(Q_H: float, E: float) -> float:
    """
    Calculate hepatic clearance.

    CL_H = Q_H × E

    For high-extraction drugs: CL_H ≈ Q_H (flow-limited)
    For low-extraction drugs: CL_H << Q_H (capacity-limited)

    Parameters
    ----------
    Q_H : float
        Hepatic blood flow (L/min)
    E : float
        Extraction ratio (0-1)

    Returns
    -------
    float
        Hepatic clearance (L/min)
    """
    return Q_H * E


hepatic_clearance = create_equation(
    id="hepatic_clearance",
    output_units='L/min',
    name="Hepatic Clearance",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"CL_H = Q_H \times E",
    simplified="CL_H = Q_H × E",
    description="Hepatic clearance. For high E drugs: CL_H ≈ Q_H (flow-limited)",
    compute_func=compute_hepatic_clearance,
    parameters=[
        Parameter(
            name="Q_H",
            description="Hepatic blood flow",
            units="L/min",
            symbol=r"Q_H",
            physiological_range=(1.0, 2.0)
        ),
        Parameter(
            name="E",
            description="Extraction ratio",
            units="dimensionless",
            symbol="E",
            physiological_range=(0.0, 1.0)
        )
    ],
    depends_on=["hepatic_blood_flow", "extraction_ratio"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(hepatic_clearance)

"""Lithogenic index for gallstone risk."""


def compute_lithogenic_index(cholesterol: float, bile_acids: float, phospholipids: float) -> float:
    """
    Calculate lithogenic index for gallstone risk.

    LI = Actual cholesterol / Maximum soluble cholesterol
    LI > 1: supersaturated bile → gallstone risk
    LI < 1: undersaturated bile → no gallstone risk

    Maximum cholesterol solubility (simplified):
    Max_chol = 0.07 × bile_acids + 0.26 × phospholipids

    Parameters
    ----------
    cholesterol : float
        Cholesterol concentration (mM)
    bile_acids : float
        Bile acid concentration (mM)
    phospholipids : float
        Phospholipid concentration (mM)

    Returns
    -------
    float
        Lithogenic index (>1 indicates supersaturation)
    """
    max_cholesterol = 0.07 * bile_acids + 0.26 * phospholipids
    if max_cholesterol > 0:
        return cholesterol / max_cholesterol
    else:
        return float('inf')


lithogenic_index = create_equation(
    id="lithogenic_index",
    output_units='dimensionless',
    name="Lithogenic Index",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"LI = \frac{[\text{Chol}]_{\text{actual}}}{[\text{Chol}]_{\max}} = \frac{[\text{Chol}]}{0.07 \times [\text{BA}] + 0.26 \times [\text{PL}]}",
    simplified="LI = [Chol] / (0.07×[BA] + 0.26×[PL])",
    description="Lithogenic index for gallstone risk. LI > 1: supersaturated bile → gallstone formation",
    compute_func=compute_lithogenic_index,
    parameters=[
        Parameter(
            name="cholesterol",
            description="Cholesterol concentration",
            units="mM",
            symbol=r"[\text{Chol}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="bile_acids",
            description="Bile acid concentration",
            units="mM",
            symbol=r"[\text{BA}]",
            physiological_range=(10.0, 150.0)
        ),
        Parameter(
            name="phospholipids",
            description="Phospholipid concentration",
            units="mM",
            symbol=r"[\text{PL}]",
            physiological_range=(5.0, 50.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.6"
    )
)

register_equation(lithogenic_index)


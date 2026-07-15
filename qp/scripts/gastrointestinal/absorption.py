"""Consolidated module for gastrointestinal.absorption."""

"""Calcium absorption (active and passive)."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_calcium_absorption_fraction(Ca_intake: float, vitamin_D_status: float = 1.0, baseline: float = 0.15) -> float:
    """
    Calculate fractional calcium absorption.

    Active absorption (duodenum): TRPV6 → calbindin → PMCA/NCX
    Passive absorption (paracellular): throughout small intestine

    Parameters
    ----------
    Ca_intake : float
        Calcium intake (mg)
    vitamin_D_status : float
        Vitamin D status (0-1 scale), default 1.0 (normal)
    baseline : float
        Baseline absorption fraction, default 0.15

    Returns
    -------
    float
        Fractional calcium absorption (0-1)
    """
    max_absorption = 0.40
    fraction = baseline + (max_absorption - baseline) * vitamin_D_status
    return fraction


calcium_absorption = create_equation(
    id="calcium_absorption_gi",
    output_units='dimensionless',
    name="Calcium Absorption (GI)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"f_{Ca} = f_{\text{baseline}} + (f_{\max} - f_{\text{baseline}}) \times \text{VitD}",
    simplified="f_Ca = f_baseline + (f_max - f_baseline) × VitD",
    description="Fractional Ca absorption. Active (duodenum, TRPV6) + passive (paracellular). ~30% of intake absorbed, higher with vitamin D",
    compute_func=compute_calcium_absorption_fraction,
    parameters=[
        Parameter(
            name="Ca_intake",
            description="Calcium intake",
            units="mg",
            symbol=r"\text{Ca}_{\text{intake}}",
            physiological_range=(200.0, 2000.0)
        ),
        Parameter(
            name="vitamin_D_status",
            description="Vitamin D status (0-1 scale)",
            units="dimensionless",
            symbol=r"\text{VitD}",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="baseline",
            description="Baseline absorption fraction",
            units="dimensionless",
            symbol=r"f_{\text{baseline}}",
            default_value=0.15,
            physiological_range=(0.10, 0.20)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(calcium_absorption)

"""Fat absorption efficiency."""


def compute_fat_absorption_efficiency(bile_salt_conc: float, CMC: float = 3.0, lipase_activity: float = 1.0) -> float:
    """
    Calculate fat absorption efficiency.

    Requires: bile salts > CMC for micelle formation, lipase activity.
    Normal efficiency: >95% for typical diet.

    Parameters
    ----------
    bile_salt_conc : float
        Bile salt concentration (mM)
    CMC : float
        Critical micellar concentration (mM), default 3.0
    lipase_activity : float
        Lipase activity (0-1 scale), default 1.0

    Returns
    -------
    float
        Fat absorption efficiency (0-1)
    """
    if bile_salt_conc >= CMC:
        micellar_efficiency = 1.0
    else:
        micellar_efficiency = bile_salt_conc / CMC

    return 0.95 * micellar_efficiency * lipase_activity


fat_absorption_efficiency = create_equation(
    id="fat_absorption_efficiency",
    output_units='dimensionless',
    name="Fat Absorption Efficiency",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\eta_{\text{fat}} = 0.95 \times \eta_{\text{micelle}} \times A_{\text{lipase}}",
    simplified="η_fat = 0.95 × η_micelle × A_lipase",
    description="Fat absorption efficiency. Requires bile salts > CMC for micelle formation. Normal: >95% absorption",
    compute_func=compute_fat_absorption_efficiency,
    parameters=[
        Parameter(
            name="bile_salt_conc",
            description="Bile salt concentration",
            units="mM",
            symbol=r"[\text{bile}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="CMC",
            description="Critical micellar concentration",
            units="mM",
            symbol=r"\text{CMC}",
            default_value=3.0,
            physiological_range=(2.0, 5.0)
        ),
        Parameter(
            name="lipase_activity",
            description="Lipase activity (0-1 scale)",
            units="dimensionless",
            symbol=r"A_{\text{lipase}}",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        )
    ],
    depends_on=["critical_micellar_concentration", "lipase_activity_bile"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(fat_absorption_efficiency)

"""GLUT5-mediated fructose absorption."""


def compute_glut5_fructose(fructose_lumen: float, Vmax: float = 3.0, Km: float = 8.0) -> float:
    """
    Calculate GLUT5-mediated fructose absorption rate.

    GLUT5 is a facilitated diffusion transporter (not Na+-dependent).

    Parameters
    ----------
    fructose_lumen : float
        Luminal fructose concentration (mM)
    Vmax : float
        Maximum absorption rate (mM/min), default 3.0
    Km : float
        Michaelis constant (mM), default 8.0 mM

    Returns
    -------
    float
        Fructose absorption rate (mM/min)
    """
    return Vmax * fructose_lumen / (Km + fructose_lumen)


glut5_fructose = create_equation(
    id="glut5_fructose",
    output_units='mM/min',
    name="GLUT5 Fructose Absorption",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J_{\text{fructose}} = \frac{V_{\max} \times [\text{Fructose}]}{K_m + [\text{Fructose}]}",
    simplified="J_fructose = V_max × [Fructose] / (K_m + [Fructose])",
    description="GLUT5-mediated fructose absorption (apical). Facilitated diffusion. K_m ≈ 6-11 mM. Not Na+-dependent.",
    compute_func=compute_glut5_fructose,
    parameters=[
        Parameter(
            name="fructose_lumen",
            description="Luminal fructose concentration",
            units="mM",
            symbol=r"[\text{Fructose}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="Vmax",
            description="Maximum absorption rate",
            units="mM/min",
            symbol=r"V_{\max}",
            default_value=3.0,
            physiological_range=(2.0, 5.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mM",
            symbol="K_m",
            default_value=8.0,
            physiological_range=(6.0, 11.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(glut5_fructose)

"""Iron absorption regulation."""


def compute_iron_absorption_fraction(Fe_intake: float, stores_depleted: bool = False, hepcidin_level: float = 1.0) -> float:
    """
    Calculate fractional iron absorption.

    Fe3+ → Fe2+ (ferrireductase)
    DMT1 (apical) → ferroportin (basolateral)
    Regulated by hepcidin (blocks ferroportin)

    Parameters
    ----------
    Fe_intake : float
        Dietary iron intake (mg)
    stores_depleted : bool
        Whether iron stores are depleted, default False
    hepcidin_level : float
        Hepcidin level (relative, 1.0 = normal), default 1.0

    Returns
    -------
    float
        Fractional iron absorption (0-1)
    """
    if stores_depleted:
        base_fraction = 0.25
    else:
        base_fraction = 0.10

    return base_fraction / hepcidin_level


iron_absorption = create_equation(
    id="iron_absorption_gi",
    output_units='dimensionless',
    name="Iron Absorption (GI)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"f_{Fe} = \frac{f_{\text{base}}}{\text{hepcidin}}",
    simplified="f_Fe = f_base / hepcidin",
    description="Fractional Fe absorption. DMT1 (apical) → ferroportin (basolateral). ~1-2 mg/day absorbed (10-20% of intake). Regulated by hepcidin",
    compute_func=compute_iron_absorption_fraction,
    parameters=[
        Parameter(
            name="Fe_intake",
            description="Dietary iron intake",
            units="mg",
            symbol=r"\text{Fe}_{\text{intake}}",
            physiological_range=(5.0, 30.0)
        ),
        Parameter(
            name="stores_depleted",
            description="Iron stores depleted (increases absorption)",
            units="boolean",
            symbol=r"\text{depleted}",
            default_value=0.0
        ),
        Parameter(
            name="hepcidin_level",
            description="Hepcidin level (relative to normal)",
            units="dimensionless",
            symbol=r"\text{hepcidin}",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(iron_absorption)

"""SGLT1-mediated glucose absorption."""


def compute_sglt1_glucose(glucose_lumen: float, Vmax: float = 6.0, Km: float = 0.3) -> float:
    """
    Calculate SGLT1-mediated glucose absorption rate.

    SGLT1 is a Na+/glucose cotransporter (2 Na+ : 1 glucose).

    Parameters
    ----------
    glucose_lumen : float
        Luminal glucose concentration (mM)
    Vmax : float
        Maximum absorption rate (mM/min), default 6.0
    Km : float
        Michaelis constant (mM), default 0.3 mM

    Returns
    -------
    float
        Glucose absorption rate (mM/min)
    """
    return Vmax * glucose_lumen / (Km + glucose_lumen)


sglt1_glucose = create_equation(
    id="sglt1_glucose",
    output_units='mM/min',
    name="SGLT1 Glucose Absorption",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J_{\text{glucose}} = \frac{V_{\max} \times [\text{Glucose}]}{K_m + [\text{Glucose}]}",
    simplified="J_glucose = V_max × [Glucose] / (K_m + [Glucose])",
    description="SGLT1-mediated glucose absorption (apical). 2 Na+ : 1 glucose cotransport. K_m ≈ 0.3 mM. Electrogenic.",
    compute_func=compute_sglt1_glucose,
    parameters=[
        Parameter(
            name="glucose_lumen",
            description="Luminal glucose concentration",
            units="mM",
            symbol=r"[\text{Glucose}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="Vmax",
            description="Maximum absorption rate",
            units="mM/min",
            symbol=r"V_{\max}",
            default_value=6.0,
            physiological_range=(4.0, 8.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mM",
            symbol="K_m",
            default_value=0.3,
            physiological_range=(0.2, 0.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(sglt1_glucose)

"""Water absorption coupled to Na+ transport."""


def compute_water_absorption(Na_absorbed: float, osmotic_coeff: float = 130.0) -> float:
    """
    Calculate water absorption coupled to Na+ transport.

    Via SGLT1: ~130 H2O per Na+ (SGLT1 moves ~260 H2O per 2-Na:1-glucose cycle).

    Parameters
    ----------
    Na_absorbed : float
        Na+ absorbed (mmol/min)
    osmotic_coeff : float
        Water molecules per Na+ (dimensionless), default 130 (=260 per 2-Na cycle)

    Returns
    -------
    float
        Water absorption (mmol H2O/min)
    """
    return Na_absorbed * osmotic_coeff


water_absorption = create_equation(
    id="water_absorption_gi",
    output_units='mmol/min',
    name="Water Absorption (GI)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J_{H_2O} = J_{Na^+} \times n_{H_2O}",
    simplified="J_H2O = J_Na+ × n_H2O",
    description="Water absorption coupled to Na+ transport. Via SGLT1: ~260 H2O per Na+. Total GI absorption ~8.8 L/day (>98% of 9 L input)",
    compute_func=compute_water_absorption,
    parameters=[
        Parameter(
            name="Na_absorbed",
            description="Na+ absorbed",
            units="mmol/min",
            symbol=r"J_{Na^+}",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="osmotic_coeff",
            description="Water molecules per Na+",
            units="dimensionless",
            symbol=r"n_{H_2O}",
            default_value=260.0,
            physiological_range=(200.0, 300.0)
        )
    ],
    depends_on=["sglt1_glucose"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.4"
    )
)

register_equation(water_absorption)



# --- review-add 2026-07-15 ---
def compute_stool_osmotic_gap(Osm_stool: float, Na: float, K: float) -> float:
    """Stool osmotic gap = Osm_stool - 2*(Na + K).

    >50-100 osmotic diarrhoea; <50 secretory."""
    return Osm_stool - 2.0 * (Na + K)

stool_osmotic_gap_equation = create_equation(
    id='stool_osmotic_gap',
    name='Stool Osmotic Gap',
    category=EquationCategory.GASTROINTESTINAL,
    latex=r'SOG = Osm_{stool} - 2(\\left[Na^+\\right] + \\left[K^+\\right])',
    simplified='SOG = Osm_stool - 2*(Na + K)',
    description='Stool osmotic gap discriminating osmotic (>50-100) from secretory (<50) diarrhoea; stool osmolality fixed at plasma ~290 in practice.',
    compute_func=compute_stool_osmotic_gap,
    output_units='mOsm/kg',
    parameters=[
        Parameter(name='Osm_stool', description='Stool osmolality', units='mOsm/kg', symbol='Osm', physiological_range=(280, 600)),
        Parameter(name='Na', description='Stool sodium', units='mmol/L', symbol='Na', physiological_range=(10, 150)),
        Parameter(name='K', description='Stool potassium', units='mmol/L', symbol='K', physiological_range=(10, 150)),
    ],
    metadata=EquationMetadata(source_unit=8, source_chapter='8.5'),
)
register_equation(stool_osmotic_gap_equation)

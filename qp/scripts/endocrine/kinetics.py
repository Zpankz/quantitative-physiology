"""kinetics equations"""

"""
Hormone-protein binding equilibrium dissociation constant.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_kd(H_free: float, P_free: float, HP_bound: float) -> float:
    """
    Calculate dissociation constant from equilibrium concentrations.

    Parameters
    ----------
    H_free : float
        Free hormone concentration (M)
    P_free : float
        Free binding protein concentration (M)
    HP_bound : float
        Hormone-protein complex concentration (M)

    Returns
    -------
    float
        Dissociation constant K_d (M)
    """
    return (H_free * P_free) / HP_bound


# Create equation
kd_equation = create_equation(
    id="hormone_kd",
    output_units='M',
    name="Hormone-Protein Dissociation Constant",
    category=EquationCategory.ENDOCRINE,
    latex=r"K_d = \frac{[H][P]}{[HP]}",
    simplified="K_d = [H][P]/[HP]",
    description="Equilibrium dissociation constant for hormone-binding protein interaction. "
                "Lower K_d indicates higher affinity binding.",
    compute_func=compute_kd,
    parameters=[
        Parameter(
            name="H_free",
            description="Free hormone concentration",
            units="M",
            symbol="[H]",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="P_free",
            description="Free binding protein concentration",
            units="M",
            symbol="[P]",
            physiological_range=(1e-9, 1e-3)
        ),
        Parameter(
            name="HP_bound",
            description="Hormone-protein complex concentration",
            units="M",
            symbol="[HP]",
            physiological_range=(1e-12, 1e-6)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.1"
    )
)

# Register globally
register_equation(kd_equation)

"""
Fraction of hormone that is free (unbound) from binding proteins.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_fraction_free(P_conc: float, Kd: float) -> float:
    """
    Calculate fraction of hormone that is free (biologically active).

    Parameters
    ----------
    P_conc : float
        Binding protein concentration (M)
    Kd : float
        Dissociation constant (M)

    Returns
    -------
    float
        Fraction free (0-1, dimensionless)

    Notes
    -----
    Free hormone hypothesis: only free (unbound) hormone is biologically active.
    Examples:
    - Cortisol: 90-95% bound (5-10% free)
    - T4: 99.97% bound (0.03% free)
    """
    return 1.0 / (1.0 + P_conc / Kd)


# Create equation
fraction_free_equation = create_equation(
    id="hormone_fraction_free",
    output_units='dimensionless',
    name="Free Hormone Fraction",
    category=EquationCategory.ENDOCRINE,
    latex=r"f_{free} = \frac{1}{1 + \frac{[P]}{K_d}}",
    simplified="f_free = 1/(1 + [P]/K_d)",
    description="Fraction of hormone that is free (unbound) and biologically active. "
                "Depends on binding protein concentration and affinity (K_d).",
    compute_func=compute_fraction_free,
    parameters=[
        Parameter(
            name="P_conc",
            description="Binding protein concentration",
            units="M",
            symbol="[P]",
            physiological_range=(1e-9, 1e-3)
        ),
        Parameter(
            name="Kd",
            description="Dissociation constant",
            units="M",
            symbol="K_d",
            physiological_range=(1e-12, 1e-6)
        )
    ],
    depends_on=["hormone_kd"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.1"
    )
)

# Register globally
register_equation(fraction_free_equation)

"""
Hormone half-life from volume of distribution and clearance.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_half_life(Vd: float, CL: float) -> float:
    """
    Calculate hormone half-life.

    Parameters
    ----------
    Vd : float
        Volume of distribution (L)
    CL : float
        Clearance rate (L/time)

    Returns
    -------
    float
        Half-life (same time units as CL)

    Notes
    -----
    Typical half-lives:
    - Epinephrine: 1-2 min
    - Insulin: 5-10 min
    - Cortisol: 60-90 min
    - T4: 6-7 days
    - T3: 1 day
    """
    return 0.693 * Vd / CL


# Create equation
half_life_equation = create_equation(
    id="hormone_half_life",
    # NOTE: 0.693*Vd/CL is time-transparent; output time unit follows CL. Use
    # apparent_vd (L) + CL in L/min for a half-life in minutes.
    output_units='min',
    name="Hormone Half-Life",
    category=EquationCategory.ENDOCRINE,
    latex=r"t_{1/2} = \frac{0.693 \times V_d}{CL}",
    simplified="t_half = 0.693 × V_d / CL",
    description="Half-life of hormone in circulation, determined by volume of distribution "
                "and clearance rate. Factor 0.693 = ln(2).",
    compute_func=compute_half_life,
    parameters=[
        Parameter(
            name="Vd",
            description="Volume of distribution",
            units="L",
            symbol="V_d",
            physiological_range=(1.0, 100.0)
        ),
        Parameter(
            name="CL",
            description="Clearance rate",
            units="L/min or L/hour",
            symbol="CL",
            physiological_range=(0.01, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.1"
    )
)

# Register globally
register_equation(half_life_equation)

"""
Metabolic clearance rate for hormones.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_mcr(production_rate: float, plasma_concentration: float) -> float:
    """
    Calculate metabolic clearance rate.

    Parameters
    ----------
    production_rate : float
        Hormone production rate (mass/time)
    plasma_concentration : float
        Steady-state plasma concentration (mass/volume)

    Returns
    -------
    float
        Metabolic clearance rate (volume/time)
    """
    return production_rate / plasma_concentration


# Create equation
mcr_equation = create_equation(
    id="metabolic_clearance_rate",
    produces="MCR_day",
    output_units='L/day',
    name="Metabolic Clearance Rate",
    category=EquationCategory.ENDOCRINE,
    latex=r"MCR = \frac{\text{Production rate}}{\text{Plasma concentration}}",
    simplified="MCR = Production_rate / Plasma_conc",
    description="Metabolic clearance rate: volume of plasma completely cleared of hormone per unit time. "
                "Reflects the efficiency of hormone removal from circulation.",
    compute_func=compute_mcr,
    parameters=[
        Parameter(
            name="production_rate",
            description="Hormone production rate",
            units="μg/day or mg/day",
            symbol="P",
            physiological_range=(1e-3, 1e3)
        ),
        Parameter(
            name="plasma_concentration",
            description="Steady-state plasma concentration",
            units="μg/L or mg/L",
            symbol="C",
            physiological_range=(1e-6, 1e3)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.1"
    )
)

# Register globally
register_equation(mcr_equation)


# --- mcr->half_life converter (2026-07-15) ---
def compute_clearance_from_metabolic_rate(MCR_day: float) -> float:
    """Convert metabolic clearance rate L/day -> plasma clearance L/min (/1440)
    so it can feed hormone_half_life's CL (which is minute-based)."""
    return MCR_day / 1440.0

clearance_from_metabolic_rate = create_equation(
    id="clearance_from_metabolic_rate",
    name="Plasma Clearance from Metabolic Clearance Rate",
    category=EquationCategory.ENDOCRINE,
    latex=r"CL_{L/min} = \frac{MCR_{L/day}}{1440}",
    simplified="CL = MCR_day / 1440",
    description="Time-base converter: metabolic clearance rate (conventionally L/day) to plasma clearance (L/min), so the MCR -> hormone_half_life chain is unit-correct (avoids the 1440x trap). Produces the SCOPED symbol CL_mcr (not the generic CL, which would hijack seeded clearance in other PK equations); consumed by hormone_half_life_from_mcr.",
    compute_func=compute_clearance_from_metabolic_rate,
    output_units="L/min", produces="CL_mcr", depends_on=["metabolic_clearance_rate"],
    parameters=[Parameter(name="MCR_day", description="Metabolic clearance rate", units="L/day", symbol="MCR", physiological_range=(0.1, 5000))],
    metadata=EquationMetadata(source_unit=9, source_chapter="9.6"),
)
register_equation(clearance_from_metabolic_rate)


# --- scoped mcr->half_life consumer (2026-07-15) ---
def compute_hormone_half_life_from_mcr(Vd: float, CL_mcr: float) -> float:
    """Hormone half-life (min) from Vd (L) and the MCR-derived plasma clearance
    CL_mcr (L/min). Dedicated consumer of the scoped CL_mcr symbol so the
    metabolic_clearance_rate -> converter -> half-life chain works WITHOUT
    hijacking the generic CL that other PK equations expect the user to seed."""
    return 0.693 * Vd / CL_mcr

hormone_half_life_from_mcr = create_equation(
    id="hormone_half_life_from_mcr",
    name="Hormone Half-Life (from Metabolic Clearance Rate)",
    category=EquationCategory.ENDOCRINE,
    latex=r"t_{1/2} = \frac{0.693\,V_d}{CL_{mcr}}",
    simplified="t_half = 0.693 * Vd / CL_mcr",
    description="Half-life computed from the MCR-derived clearance, closing the metabolic_clearance_rate -> clearance_from_metabolic_rate -> half-life chain with a scoped CL_mcr symbol (leaves the generic hormone_half_life free to use a user-seeded CL).",
    compute_func=compute_hormone_half_life_from_mcr,
    output_units="min", depends_on=["clearance_from_metabolic_rate"],
    parameters=[Parameter(name="Vd", description="Volume of distribution", units="L", symbol="V_d", physiological_range=(1.0, 500.0)),
                Parameter(name="CL_mcr", description="MCR-derived plasma clearance", units="L/min", symbol="CL_mcr", physiological_range=(1e-4, 100.0))],
    metadata=EquationMetadata(source_unit=9, source_chapter="9.6"),
)
register_equation(hormone_half_life_from_mcr)

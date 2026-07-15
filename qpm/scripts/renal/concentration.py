"""Consolidated module for renal.concentration."""

"""
ADH-dependent water permeability in collecting duct.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_water_permeability(P_0: float, P_max: float, ADH: float, K_ADH: float) -> float:
    """
    Calculate ADH-dependent water permeability.

    Args:
        P_0: Baseline water permeability (without ADH)
        P_max: Maximum additional permeability from ADH
        ADH: ADH concentration
        K_ADH: Half-maximal ADH concentration

    Returns:
        P_water: Total water permeability
    """
    return P_0 + P_max * ADH / (K_ADH + ADH)


# Create equation
adh_water_permeability = create_equation(
    id="adh_water_permeability",
    output_units='cm/s',
    name="ADH-Dependent Water Permeability",
    category=EquationCategory.RENAL,
    latex=r"P_{water} = P_0 + \frac{P_{max} \times [ADH]}{K_{ADH} + [ADH]}",
    simplified="P_water = P_0 + P_max × [ADH] / (K_ADH + [ADH])",
    description="Collecting duct water permeability regulated by ADH through aquaporin-2 insertion",
    compute_func=compute_water_permeability,
    parameters=[
        Parameter(
            name="P_0",
            description="Baseline water permeability",
            units="cm/s",
            symbol="P_0",
            physiological_range=(1e-6, 1e-4)
        ),
        Parameter(
            name="P_max",
            description="Maximum ADH-stimulated permeability increase",
            units="cm/s",
            symbol="P_{max}",
            physiological_range=(1e-5, 1e-3)
        ),
        Parameter(
            name="ADH",
            description="ADH concentration",
            units="pg/mL",
            symbol="[ADH]",
            physiological_range=(0, 20)
        ),
        Parameter(
            name="K_ADH",
            description="Half-maximal ADH concentration",
            units="pg/mL",
            symbol="K_{ADH}",
            physiological_range=(1, 5)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6"
    )
)

# Register equation
register_equation(adh_water_permeability)

"""
Countercurrent multiplication factor.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

import math


def compute_multiplication_factor(loop_length: float, lambda_char: float) -> float:
    """
    Calculate countercurrent multiplication factor.

    Args:
        loop_length: Length of loop of Henle
        lambda_char: Characteristic length for concentration

    Returns:
        M: Multiplication factor (π_tip / π_base)
    """
    return math.exp(loop_length / lambda_char)


# Create equation
countercurrent_multiplication = create_equation(
    id="countercurrent_multiplication",
    output_units='dimensionless',
    name="Countercurrent Multiplication Factor",
    category=EquationCategory.RENAL,
    latex=r"M = \frac{\pi_{tip}}{\pi_{base}} = e^{L/\lambda}",
    simplified="M = π_tip / π_base = e^(L/λ)",
    description="Amplification of osmotic gradient achieved by countercurrent loop structure",
    compute_func=compute_multiplication_factor,
    parameters=[
        Parameter(
            name="loop_length",
            description="Length of loop of Henle",
            units="mm",
            symbol="L",
            physiological_range=(2, 15)
        ),
        Parameter(
            name="lambda_char",
            description="Characteristic length for concentration",
            units="mm",
            symbol=r"\lambda",
            physiological_range=(1, 5)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.4"
    )
)

# Register equation
register_equation(countercurrent_multiplication)

"""
Free water clearance calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_free_water_clearance(V_dot: float, U_osm: float, P_osm: float) -> float:
    """
    Calculate free water clearance.

    Args:
        V_dot: Urine flow rate (mL/min)
        U_osm: Urine osmolality (mOsm/kg)
        P_osm: Plasma osmolality (mOsm/kg)

    Returns:
        C_H2O: Free water clearance (mL/min)
               > 0: dilute urine (water excess)
               < 0: concentrated urine (water deficit) = T^c_H2O
    """
    C_osm = (U_osm * V_dot) / P_osm
    return V_dot - C_osm


# Create equation
free_water_clearance = create_equation(
    id="free_water_clearance",
    output_units='mL/min',
    name="Free Water Clearance",
    category=EquationCategory.RENAL,
    latex=r"C_{H_2O} = \dot{V} - C_{osm} = \dot{V} - \frac{U_{osm} \times \dot{V}}{P_{osm}}",
    simplified="C_H2O = V̇ - C_osm = V̇ - (U_osm × V̇) / P_osm",
    description="Volume of solute-free water cleared per unit time; positive in dilute urine, negative in concentrated urine",
    compute_func=compute_free_water_clearance,
    parameters=[
        Parameter(
            name="V_dot",
            description="Urine flow rate",
            units="mL/min",
            symbol=r"\dot{V}",
            physiological_range=(0.5, 20)
        ),
        Parameter(
            name="U_osm",
            description="Urine osmolality",
            units="mOsm/kg",
            symbol="U_{osm}",
            physiological_range=(50, 1200)
        ),
        Parameter(
            name="P_osm",
            description="Plasma osmolality",
            units="mOsm/kg",
            symbol="P_{osm}",
            physiological_range=(280, 300)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6"
    )
)

# Register equation
register_equation(free_water_clearance)

"""
Medullary osmolality gradient calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_medullary_gradient(depth: float, osm_cortex: float = 300.0, osm_tip: float = 1200.0) -> float:
    """
    Calculate medullary osmolality at a given depth.

    Args:
        depth: Fractional depth into medulla (0 = cortex, 1 = papillary tip)
        osm_cortex: Cortical osmolality (mOsm/kg, default 300)
        osm_tip: Papillary tip osmolality (mOsm/kg, default 1200)

    Returns:
        osm: Osmolality at given depth (mOsm/kg)
    """
    return osm_cortex + (osm_tip - osm_cortex) * depth


# Create equation
medullary_gradient = create_equation(
    id="medullary_gradient",
    output_units='mOsm/kg',
    name="Medullary Osmolality Gradient",
    category=EquationCategory.RENAL,
    latex=r"\pi(d) = \pi_{cortex} + (\pi_{tip} - \pi_{cortex}) \times d",
    simplified="π(d) = π_cortex + (π_tip - π_cortex) × d",
    description="Linear approximation of osmolality gradient from cortex to medullary tip",
    compute_func=compute_medullary_gradient,
    parameters=[
        Parameter(
            name="depth",
            description="Fractional depth into medulla",
            units="dimensionless",
            symbol="d",
            physiological_range=(0, 1)
        ),
        Parameter(
            name="osm_cortex",
            description="Cortical osmolality",
            units="mOsm/kg",
            symbol=r"\pi_{cortex}",
            default_value=300.0,
            physiological_range=(280, 310)
        ),
        Parameter(
            name="osm_tip",
            description="Papillary tip osmolality",
            units="mOsm/kg",
            symbol=r"\pi_{tip}",
            default_value=1200.0,
            physiological_range=(900, 1400)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.4"
    )
)

# Register equation
register_equation(medullary_gradient)

"""
Urine-to-plasma osmolality ratio.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_urine_osm_ratio(U_osm: float, P_osm: float) -> float:
    """
    Calculate urine-to-plasma osmolality ratio.

    Args:
        U_osm: Urine osmolality (mOsm/kg)
        P_osm: Plasma osmolality (mOsm/kg)

    Returns:
        ratio: U/P osmolality ratio (0.2-4.0, dilute to concentrated)
    """
    return U_osm / P_osm


# Create equation
urine_osmolality_ratio = create_equation(
    id="urine_osmolality_ratio",
    output_units='dimensionless',
    name="Urine-to-Plasma Osmolality Ratio",
    category=EquationCategory.RENAL,
    latex=r"\frac{U_{osm}}{P_{osm}}",
    simplified="U_osm / P_osm",
    description="Ratio indicating kidney's concentration/dilution capability; range 0.2 (maximally dilute) to 4.0 (maximally concentrated)",
    compute_func=compute_urine_osm_ratio,
    parameters=[
        Parameter(
            name="U_osm",
            description="Urine osmolality",
            units="mOsm/kg",
            symbol="U_{osm}",
            physiological_range=(50, 1200)
        ),
        Parameter(
            name="P_osm",
            description="Plasma osmolality",
            units="mOsm/kg",
            symbol="P_{osm}",
            physiological_range=(280, 300)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6"
    )
)

# Register equation
register_equation(urine_osmolality_ratio)

"""
Water reabsorption flux in collecting duct.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_water_flux(L_p: float, A: float, pi_int: float, pi_lumen: float) -> float:
    """
    Calculate water reabsorption flux driven by osmotic gradient.

    Args:
        L_p: Hydraulic conductivity (water permeability)
        A: Surface area
        pi_int: Interstitial osmotic pressure
        pi_lumen: Luminal osmotic pressure

    Returns:
        J_water: Water flux (volume per unit time)
    """
    return L_p * A * (pi_int - pi_lumen)


# Create equation
water_reabsorption_flux = create_equation(
    id="water_reabsorption_flux",
    output_units='mL/(s*kg)',
    name="Water Reabsorption Flux",
    category=EquationCategory.RENAL,
    latex=r"J_{water} = L_p \times A \times (\pi_{int} - \pi_{lumen})",
    simplified="J_water = L_p × A × (π_int - π_lumen)",
    description="Osmotic water movement from tubular lumen to interstitium in collecting duct",
    compute_func=compute_water_flux,
    parameters=[
        Parameter(
            name="L_p",
            description="Hydraulic conductivity (water permeability)",
            units="cm/s/mOsm",
            symbol="L_p",
            physiological_range=(1e-7, 1e-4)
        ),
        Parameter(
            name="A",
            description="Surface area",
            units="cm²",
            symbol="A",
            physiological_range=(0.1, 10)
        ),
        Parameter(
            name="pi_int",
            description="Interstitial osmotic pressure",
            units="mOsm/kg",
            symbol=r"\pi_{int}",
            physiological_range=(300, 1200)
        ),
        Parameter(
            name="pi_lumen",
            description="Luminal osmotic pressure",
            units="mOsm/kg",
            symbol=r"\pi_{lumen}",
            physiological_range=(50, 1200)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6"
    )
)

# Register equation
register_equation(water_reabsorption_flux)


"""Consolidated module for renal.glomerular."""

"""
Glomerular Filtration Rate (GFR) from ultrafiltration coefficient and NFP.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_gfr(K_f: float, NFP: float) -> float:
    """
    Calculate GFR from ultrafiltration coefficient and net filtration pressure.

    Args:
        K_f: Ultrafiltration coefficient (mL/min/mmHg)
        NFP: Net filtration pressure (mmHg)

    Returns:
        GFR: Glomerular filtration rate (mL/min)
    """
    return K_f * NFP


# Create equation
gfr_from_nfp = create_equation(
    id="gfr_from_nfp",
    produces='GFR',
    output_units='mL/min',
    name="GFR from Ultrafiltration Coefficient",
    category=EquationCategory.RENAL,
    latex=r"GFR = K_f \times NFP",
    simplified="GFR = K_f × NFP",
    description="Glomerular filtration rate determined by membrane permeability and driving pressure",
    compute_func=compute_gfr,
    parameters=[
        Parameter(
            name="K_f",
            description="Ultrafiltration coefficient (product of hydraulic conductivity and surface area)",
            units="mL/min/mmHg",
            symbol="K_f",
            physiological_range=(5, 15)
        ),
        Parameter(
            name="NFP",
            description="Net filtration pressure",
            units="mmHg",
            symbol="NFP",
            physiological_range=(5, 20)
        )
    ],
    depends_on=["net_filtration_pressure"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(gfr_from_nfp)

"""
GFR normalization for body surface area.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_gfr_normalized(GFR: float, BSA: float) -> float:
    """
    Normalize GFR to standard body surface area (1.73 m²).

    Args:
        GFR: Measured glomerular filtration rate (mL/min)
        BSA: Body surface area (m²)

    Returns:
        GFR_normalized: GFR normalized to 1.73 m² (mL/min/1.73m²)
    """
    return GFR * (1.73 / BSA)


# Create equation
gfr_normalized = create_equation(
    id="gfr_normalized",
    output_units='mL/min',
    name="GFR Normalized for Body Surface Area",
    category=EquationCategory.RENAL,
    latex=r"GFR_{normalized} = GFR \times \frac{1.73}{BSA}",
    simplified="GFR_normalized = GFR × (1.73 / BSA)",
    description="Adjusts GFR to standardized body surface area for comparison",
    compute_func=compute_gfr_normalized,
    parameters=[
        Parameter(
            name="GFR",
            description="Measured glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(60, 180)
        ),
        Parameter(
            name="BSA",
            description="Body surface area",
            units="m²",
            symbol="BSA",
            physiological_range=(1.2, 2.5)
        )
    ],
    depends_on=["gfr_from_nfp", "body_surface_area_dubois"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(gfr_normalized)

"""
Net Filtration Pressure (NFP) - Starling Forces in the Glomerulus.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_nfp(P_GC: float, P_BC: float, pi_GC: float, pi_BC: float = 0.0) -> float:
    """
    Calculate net filtration pressure using Starling forces.

    Args:
        P_GC: Glomerular capillary pressure (mmHg)
        P_BC: Bowman's capsule pressure (mmHg)
        pi_GC: Glomerular capillary oncotic pressure (mmHg)
        pi_BC: Bowman's capsule oncotic pressure (mmHg, typically 0)

    Returns:
        NFP: Net filtration pressure (mmHg)
    """
    return P_GC - P_BC - pi_GC + pi_BC


# Create equation
net_filtration_pressure = create_equation(
    id="glomerular_nfp",
    produces="NFP_glomerular",
    output_units='mmHg',
    name="Glomerular Net Filtration Pressure",
    category=EquationCategory.RENAL,
    latex=r"NFP = P_{GC} - P_{BC} - \pi_{GC} + \pi_{BC}",
    simplified="NFP = P_GC - P_BC - π_GC + π_BC",
    description="Net pressure driving glomerular filtration based on Starling forces",
    compute_func=compute_nfp,
    parameters=[
        Parameter(
            name="P_GC",
            description="Glomerular capillary hydrostatic pressure",
            units="mmHg",
            symbol="P_{GC}",
            physiological_range=(50, 70)
        ),
        Parameter(
            name="P_BC",
            description="Bowman's capsule hydrostatic pressure",
            units="mmHg",
            symbol="P_{BC}",
            physiological_range=(10, 20)
        ),
        Parameter(
            name="pi_GC",
            description="Glomerular capillary oncotic pressure",
            units="mmHg",
            symbol=r"\pi_{GC}",
            physiological_range=(25, 35)
        ),
        Parameter(
            name="pi_BC",
            description="Bowman's capsule oncotic pressure",
            units="mmHg",
            symbol=r"\pi_{BC}",
            default_value=0.0,
            physiological_range=(0, 2)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.2"
    )
)

# Register equation
register_equation(net_filtration_pressure)



# --- coverage pass additions (Feher extraction) ---

def compute_sieving_coefficient(C_B, C_P):
    """Glomerular sieving coefficient Theta = C_B / C_P (Feher Unit 7, section 7.3,
    'The Sieving Coefficient Depends Mainly on the Slit Diaphragm').

    Ratio of a solute's concentration in Bowman's-space filtrate (C_B) to its
    concentration in glomerular-capillary plasma (C_P). Dimensionless index of
    glomerular permselectivity: Theta ~ 1 for freely filtered small solutes and
    approaches 0 for large or anionic proteins retained by the slit diaphragm
    (relates to the reflection coefficient by sigma ~ 1 - Theta). C_B and C_P must
    be supplied in the SAME concentration units (e.g. g/L); the output is unitless.
    """
    return C_B / C_P

sieving_coefficient = create_equation(
    id='sieving_coefficient',
    output_units='dimensionless',
    name='Glomerular Sieving Coefficient',
    category=EquationCategory.RENAL,
    latex='\\Theta = \\frac{C_{B}}{C_{P}}',
    simplified='Theta = C_B / C_P',
    description="Glomerular sieving coefficient: the ratio of a solute's concentration in Bowman's-space filtrate (C_B) to its concentration in glomerular-capillary plasma (C_P). A dimensionless measure of the glomerular filtration barrier's size- and charge-selective permselectivity. Theta ~ 1 for freely filtered small solutes (e.g. inulin, glucose) and falls toward 0 for large or anionic macromolecules retained mainly by the podocyte slit diaphragm (albumin, Stokes radius ~3.6 nm, has a very low Theta). It relates to the Starling reflection coefficient by sigma ~ 1 - Theta. Used to quantify and compare protein handling by the glomerular barrier and to interpret proteinuria in glomerular disease (e.g. nephrotic syndrome).",
    compute_func=compute_sieving_coefficient,
    parameters=[
        Parameter(name='C_B', description="Concentration of the solute in Bowman's space (the glomerular filtrate)", units='g/L', symbol='C_{B}', physiological_range=(0, 100)),
        Parameter(name='C_P', description='Concentration of the same solute in the glomerular-capillary plasma (must be > 0; same units as C_B)', units='g/L', symbol='C_{P}', physiological_range=(0.1, 100)),
    ],
    depends_on=[],
    produces='Theta',
    metadata=EquationMetadata(source_unit=7, source_chapter='7.3',
                              source_section='THE SIEVING COEFFICIENT DEPENDS MAINLY ON THE SLIT DIAPHRAGM', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(sieving_coefficient)

try:
    __all__ += ['sieving_coefficient']
except NameError:
    __all__ = ['sieving_coefficient']

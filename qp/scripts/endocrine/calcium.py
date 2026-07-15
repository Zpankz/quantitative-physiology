"""calcium equations"""

"""
Albumin-corrected total calcium.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_corrected_calcium(measured_Ca: float, albumin: float) -> float:
    """
    Calculate albumin-corrected total calcium.

    Parameters
    ----------
    measured_Ca : float
        Measured total calcium (mg/dL)
    albumin : float
        Serum albumin (g/dL)

    Returns
    -------
    float
        Corrected calcium (mg/dL)

    Notes
    -----
    Plasma calcium distribution:
    - 45% ionized (free) - physiologically active
    - 40% protein-bound (mostly albumin)
    - 15% complexed (citrate, phosphate)

    Normal total Ca: 9-10.5 mg/dL
    Normal ionized Ca: 4.5-5.3 mg/dL (1.1-1.3 mM)
    Normal albumin: 3.5-5.0 g/dL

    Correction accounts for hypo/hyperalbuminemia affecting total Ca measurement
    while ionized Ca remains normal.
    """
    return measured_Ca + 0.8 * (4.0 - albumin)


# Create equation
corrected_calcium_equation = create_equation(
    id="calcium_albumin_correction",
    output_units='mg/dL',
    name="Albumin-Corrected Calcium",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{Corrected Ca} = \text{Measured Ca} + 0.8 \times (4 - [\text{Albumin}])",
    simplified="Corrected_Ca = Measured_Ca + 0.8 × (4 - Albumin)",
    description="Corrects total calcium for albumin concentration. Accounts for protein-binding "
                "effects when albumin is abnormal while ionized Ca is normal.",
    compute_func=compute_corrected_calcium,
    parameters=[
        Parameter(
            name="measured_Ca",
            description="Measured total calcium",
            units="mg/dL",
            symbol="Ca_{measured}",
            physiological_range=(5.0, 15.0)
        ),
        Parameter(
            name="albumin",
            description="Serum albumin concentration",
            units="g/dL",
            symbol="Albumin",
            physiological_range=(2.0, 6.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.7"
    )
)

# Register globally
register_equation(corrected_calcium_equation)

"""
PTH secretion as inverse function of ionized calcium.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_pth_secretion(Ca_ionized: float, PTH_max: float = 65.0,
                          K: float = 1.1, n: float = 3.5) -> float:
    """
    Calculate PTH secretion rate as inverse function of ionized calcium.

    Parameters
    ----------
    Ca_ionized : float
        Ionized (free) calcium concentration (mM)
    PTH_max : float
        Maximum PTH concentration (pg/mL)
    K : float
        Calcium setpoint (mM)
    n : float
        Hill coefficient (steepness)

    Returns
    -------
    float
        PTH concentration (pg/mL)

    Notes
    -----
    Calcium-sensing receptor (CaSR) mediates inverse regulation:
    ↑ Ca²⁺ → ↑ CaSR activation → ↓ PTH secretion

    Normal ranges:
    - Ionized Ca²⁺: 1.0-1.3 mM
    - PTH (intact): 10-65 pg/mL

    Steep inverse response (n ≈ 3-4) provides tight calcium regulation.
    """
    return PTH_max * (K ** n) / (K ** n + Ca_ionized ** n)


# Create equation
pth_secretion_equation = create_equation(
    id="calcium_pth_secretion",
    output_units='pg/mL',
    name="PTH Secretion (Calcium Feedback)",
    category=EquationCategory.ENDOCRINE,
    latex=r"PTH = PTH_{max} \times \frac{K^n}{K^n + [Ca^{2+}]^n}",
    simplified="PTH = PTH_max × K^n / (K^n + [Ca²⁺]^n)",
    description="PTH secretion from parathyroid glands as steep inverse function of ionized calcium. "
                "Calcium-sensing receptor (CaSR) mediates negative feedback (n ≈ 3-4).",
    compute_func=compute_pth_secretion,
    parameters=[
        Parameter(
            name="Ca_ionized",
            description="Ionized calcium concentration",
            units="mM",
            symbol="[Ca^{2+}]",
            physiological_range=(0.8, 1.5)
        ),
        Parameter(
            name="PTH_max",
            description="Maximum PTH concentration",
            units="pg/mL",
            symbol="PTH_{max}",
            default_value=65.0,
            physiological_range=(50.0, 100.0)
        ),
        Parameter(
            name="K",
            description="Calcium setpoint",
            units="mM",
            symbol="K",
            default_value=1.1,
            physiological_range=(1.0, 1.3)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=3.5,
            physiological_range=(3.0, 4.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.7"
    )
)

# Register globally
register_equation(pth_secretion_equation)

"""
1,25(OH)2D (calcitriol) production rate from 25(OH)D.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_vitamin_d_activation(PTH: float, phosphate: float, FGF23: float,
                                 k_PTH: float = 1.0, k_phos: float = 0.5,
                                 k_FGF23: float = 0.3) -> float:
    """
    Calculate 1,25(OH)2D production rate (1α-hydroxylase activity).

    Parameters
    ----------
    PTH : float
        PTH concentration (stimulates)
    phosphate : float
        Plasma phosphate concentration (mM)
    FGF23 : float
        FGF23 concentration (inhibits)
    k_PTH : float
        PTH stimulation constant
    k_phos : float
        Hypophosphatemia stimulation constant
    k_FGF23 : float
        FGF23 inhibition constant

    Returns
    -------
    float
        1,25(OH)2D production rate (proportional)

    Notes
    -----
    Synthesis pathway:
    7-dehydrocholesterol → (UV-B) → Vitamin D3
    → (Liver 25-hydroxylase) → 25(OH)D
    → (Kidney 1α-hydroxylase) → 1,25(OH)2D (calcitriol)

    1α-hydroxylase regulation:
    - Stimulators: PTH, hypophosphatemia
    - Inhibitors: 1,25(OH)2D (feedback), FGF23, hypercalcemia

    Normal ranges:
    - 25(OH)D: 30-100 ng/mL (sufficient)
    - 1,25(OH)2D: 20-60 pg/mL
    """
    stimulation = k_PTH * PTH + k_phos / (phosphate + 0.1)
    inhibition = 1.0 + k_FGF23 * FGF23
    return stimulation / inhibition


# Create equation
vitamin_d_activation_equation = create_equation(
    id="calcium_vitamin_d_activation",
    output_units='arbitrary',
    name="Vitamin D Activation (1α-hydroxylase)",
    category=EquationCategory.ENDOCRINE,
    latex=r"\text{1,25(OH)}_2\text{D production} = \frac{k_{PTH} \times PTH + \frac{k_{phos}}{[PO_4] + 0.1}}{1 + k_{FGF23} \times FGF23}",
    simplified="1,25(OH)2D_production = (k_PTH×PTH + k_phos/[PO4]) / (1 + k_FGF23×FGF23)",
    description="1,25(OH)2D (calcitriol) production via renal 1α-hydroxylase. "
                "Stimulated by PTH and low phosphate, inhibited by FGF23.",
    compute_func=compute_vitamin_d_activation,
    parameters=[
        Parameter(
            name="PTH",
            description="PTH concentration",
            units="pg/mL",
            symbol="PTH",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="phosphate",
            description="Plasma phosphate concentration",
            units="mM",
            symbol="[PO_4]",
            physiological_range=(0.5, 3.0)
        ),
        Parameter(
            name="FGF23",
            description="FGF23 concentration",
            units="arbitrary units",
            symbol="FGF23",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="k_PTH",
            description="PTH stimulation constant",
            units="arbitrary",
            symbol="k_{PTH}",
            default_value=1.0,
            physiological_range=(0.1, 5.0)
        ),
        Parameter(
            name="k_phos",
            description="Hypophosphatemia stimulation constant",
            units="arbitrary",
            symbol="k_{phos}",
            default_value=0.5,
            physiological_range=(0.1, 2.0)
        ),
        Parameter(
            name="k_FGF23",
            description="FGF23 inhibition constant",
            units="arbitrary",
            symbol="k_{FGF23}",
            default_value=0.3,
            physiological_range=(0.1, 1.0)
        )
    ],
    depends_on=["calcium_pth_secretion"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.7"
    )
)

# Register globally
register_equation(vitamin_d_activation_equation)



# --- coverage pass additions (Feher extraction) ---

def compute_beer_lambert_attenuation(I_0, mu, x):
    """Beer-Lambert law I = I_0 * exp(-mu*x): transmitted X-ray beam intensity after path length x [cm] through an absorber of linear attenuation coefficient mu [1/cm] (Feher 9.8, DEXA bone densitometry). I and I_0 share arbitrary intensity units; the ratio I/I_0 is dimensionless."""
    import math
    return I_0 * math.exp(-mu * x)

beer_lambert_attenuation = create_equation(
    id='beer_lambert_attenuation',
    output_units='arbitrary',
    name='Beer–Lambert Attenuation (X-ray)',
    category=EquationCategory.ENDOCRINE,
    latex='I = I_0\\, e^{-\\mu x}',
    simplified='I = I_0 * exp(-mu * x)',
    description='Beer-Lambert law of radiation attenuation: transmitted intensity of an X-ray (or gamma) beam after passing through thickness x of an absorber with linear attenuation coefficient mu. Feher states it as the physical basis of dual-energy X-ray absorptiometry (DEXA/DXA) for bone-density measurement; mu increases steeply with atomic number Z, so calcium/bone attenuates far more than soft tissue (H, O, C), and decreases with beam energy. The single-beam relation is extended in-text to layered (tissue+bone) and dual-energy forms to solve for bone mineral mass.',
    compute_func=compute_beer_lambert_attenuation,
    parameters=[
        Parameter(name='I_0', description='Incident X-ray beam intensity prior to absorption', units='beam intensity (arbitrary units; same as output)', symbol='I_0'),
        Parameter(name='mu', description='Linear attenuation coefficient of the absorbing material (rises with atomic number Z and atomic density; falls with beam energy)', units='cm^-1', symbol='\\mu', physiological_range=(0, 5)),
        Parameter(name='x', description='Path length (thickness) the beam traverses through the material', units='cm', symbol='x', physiological_range=(0, 50)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=9, source_chapter='9.8',
                              source_section='Clinical Applications: Dual Energy X-ray Absorptiometry and Bone Density', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(beer_lambert_attenuation)

try:
    __all__ += ['beer_lambert_attenuation']
except NameError:
    __all__ = ['beer_lambert_attenuation']

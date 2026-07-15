"""Renal autoregulation and tubuloglomerular feedback (Unit 7).

The two intrinsic mechanisms that hold RBF and GFR near-constant across a wide
range of arterial pressure (~80-180 mmHg):

- Tubuloglomerular feedback (TGF): the macula densa senses distal NaCl delivery
  and adjusts afferent arteriolar tone, giving a descending sigmoidal relation
  between distal [NaCl] and single-nephron GFR.
- Myogenic autoregulation: afferent arteriolar resistance rises with perfusion
  pressure. Its effectiveness is summarised by an autoregulatory index.

This module was previously an empty stub and was not imported by the renal
package, leaving renal at 28 rather than the documented 30 equations.

Source: Feher, Quantitative Human Physiology 3rd ed., Unit 7 (Renal
Physiology), Section 7.6 "Regulation of Fluid Balance" -- subsections "RBF and
GFR exhibit autoregulation" (Fig 7.6.3; constant over 80-180 mmHg) and
"Tubuloglomerular feedback regulates the single nephron GFR". Verified via the
corpus extract; it preserves section/equation numbering rather than book page
numbers, so page_reference is left None (not fabricated).
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_tubuloglomerular_feedback(
    NaCl_md: float,
    SNGFR_max: float,
    SNGFR_min: float,
    K_half: float,
    n: float,
) -> float:
    """
    Single-nephron GFR as a descending sigmoid of macula densa [NaCl] (TGF).

    Formula: SNGFR = SNGFR_min + (SNGFR_max - SNGFR_min) * K_half^n / (K_half^n + [NaCl]^n)

    Rising distal NaCl delivery (macula densa) increases afferent tone and
    lowers SNGFR toward SNGFR_min; low delivery relaxes the afferent arteriole
    toward SNGFR_max.

    Parameters
    ----------
    NaCl_md : float - Macula densa luminal NaCl concentration (mM)
    SNGFR_max : float - Maximal single-nephron GFR at low distal NaCl (nL/min)
    SNGFR_min : float - Minimal single-nephron GFR at high distal NaCl (nL/min)
    K_half : float - Distal [NaCl] giving half-maximal feedback (mM)
    n : float - Feedback steepness (Hill-type exponent, dimensionless)

    Returns
    -------
    SNGFR : float - Single-nephron GFR (nL/min)
    """
    return SNGFR_min + (SNGFR_max - SNGFR_min) * (K_half ** n) / (K_half ** n + NaCl_md ** n)


tubuloglomerular_feedback = create_equation(
    id="tubuloglomerular_feedback",
    output_units='nL/min',
    name="Tubuloglomerular Feedback (SNGFR)",
    category=EquationCategory.RENAL,
    latex=r"SNGFR = SNGFR_{min} + (SNGFR_{max}-SNGFR_{min})\,\frac{K_{1/2}^{\,n}}{K_{1/2}^{\,n} + [NaCl]^{n}}",
    simplified="SNGFR = SNGFR_min + (SNGFR_max - SNGFR_min) * K_half^n / (K_half^n + NaCl_md^n)",
    description=(
        "Tubuloglomerular feedback: the macula densa converts distal NaCl "
        "delivery into an afferent-arteriolar tone signal, producing a "
        "descending sigmoidal single-nephron GFR response that stabilises "
        "distal delivery and contributes to GFR autoregulation."
    ),
    compute_func=compute_tubuloglomerular_feedback,
    parameters=[
        Parameter(name="NaCl_md", description="Macula densa luminal NaCl concentration",
                  units="mM", symbol="[NaCl]_md", physiological_range=(10.0, 80.0)),
        Parameter(name="SNGFR_max", description="Maximal single-nephron GFR (low distal NaCl)",
                  units="nL/min", symbol="SNGFR_max", physiological_range=(20.0, 80.0)),
        Parameter(name="SNGFR_min", description="Minimal single-nephron GFR (high distal NaCl)",
                  units="nL/min", symbol="SNGFR_min", physiological_range=(0.0, 40.0)),
        Parameter(name="K_half", description="Distal [NaCl] at half-maximal feedback",
                  units="mM", symbol="K_1/2", physiological_range=(20.0, 60.0)),
        Parameter(name="n", description="Feedback steepness (Hill exponent)",
                  units="dimensionless", symbol="n", physiological_range=(1.0, 8.0)),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6",
        source_section="Regulation of Fluid Balance - tubuloglomerular feedback regulates the single nephron GFR",
        page_reference=None,  # Feher extract retains section/equation numbers, not book page
        textbook_equation_number=None,
    ),
)
register_equation(tubuloglomerular_feedback)


def compute_renal_autoregulation_index(delta_rbf_pct: float, delta_map_pct: float) -> float:
    """
    Autoregulatory index quantifying myogenic/TGF buffering of renal blood flow.

    Formula: AI = (%change RBF) / (%change MAP)

    AI ~ 0 indicates near-perfect autoregulation (RBF unchanged despite a
    pressure step); AI ~ 1 indicates a pressure-passive, non-autoregulating
    vasculature.

    Parameters
    ----------
    delta_rbf_pct : float - Fractional change in renal blood flow (%)
    delta_map_pct : float - Fractional change in mean arterial pressure (%)

    Returns
    -------
    AI : float - Autoregulatory index (dimensionless)
    """
    return delta_rbf_pct / delta_map_pct


renal_autoregulation_index = create_equation(
    id="renal_autoregulation_index",
    output_units='dimensionless',
    name="Renal Autoregulatory Index",
    category=EquationCategory.RENAL,
    latex=r"AI = \frac{\%\Delta RBF}{\%\Delta MAP}",
    simplified="AI = delta_rbf_pct / delta_map_pct",
    description=(
        "Autoregulatory index: fractional change in renal blood flow per "
        "fractional change in perfusion pressure. Values near 0 denote "
        "effective myogenic + tubuloglomerular autoregulation across the "
        "~80-180 mmHg range; values near 1 denote pressure-passive flow."
    ),
    compute_func=compute_renal_autoregulation_index,
    parameters=[
        Parameter(name="delta_rbf_pct", description="Fractional change in renal blood flow",
                  units="%", symbol="%dRBF", physiological_range=(-100.0, 100.0)),
        Parameter(name="delta_map_pct", description="Fractional change in mean arterial pressure",
                  units="%", symbol="%dMAP", physiological_range=(-100.0, 100.0)),
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.6",
        source_section="Regulation of Fluid Balance - RBF and GFR exhibit autoregulation (Fig 7.6.3, 80-180 mmHg)",
        page_reference=None,  # Feher extract retains section/equation numbers, not book page
        textbook_equation_number=None,
    ),
)
register_equation(renal_autoregulation_index)


__all__ = ["tubuloglomerular_feedback", "renal_autoregulation_index"]

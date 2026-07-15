"""Reference physiological ranges for whole-body clinical quantities.

This is the single documented source for *whole-body reference (normal) ranges*
-- the values a clinician would quote for a healthy adult.

IMPORTANT: this is deliberately NOT used to force every equation's parameter
`physiological_range` to a single value. An audit of the library found ~57
cases where the same parameter symbol carries different ranges across
equations, but on inspection almost all are legitimately context-specific
validation domains rather than drift, e.g.:

  - K_m (Michaelis constant) is enzyme-specific: SGLT1 0.2-0.5 mM, GLUT5 6-11 mM.
  - r (radius) is structure-specific: ion ~1e-10 m, alveolus ~1e-7 m, airway ~1e-4 m.
  - eta (viscosity) is fluid-specific: air ~1.8e-5, water ~1e-3, blood ~3.5e-3 Pa*s.
  - HCO3 ranges are tuned to each equation's scenario: Winters' formula (metabolic
    acidosis) spans 5-40, whereas the anion-gap equation assumes a normal 22-26.
  - n (exponent) is a gating variable (0-1), a Hill coefficient (2-3.5), or a
    quantal count (1-1000) depending on the equation.

Collapsing those to one range per symbol would make the equations' out-of-range
warnings wrong. Each equation therefore keeps a range appropriate to its own
physiological context; this module is the reference for the whole-body normals
and a place to look up a canonical value when one is genuinely needed.

Usage:
    from scripts.parameter_ranges import reference_range, REFERENCE_RANGES
    lo, hi = reference_range("Hb")          # (12.0, 18.0)
"""
from typing import Dict, Optional, Tuple

# canonical quantity -> (low, high, units, note)
REFERENCE_RANGES: Dict[str, Tuple[float, float, str, str]] = {
    # Blood / oxygenation
    "Hb":   (12.0, 18.0, "g/dL", "Adult haemoglobin"),
    "Hct":  (0.36, 0.54, "fraction", "Adult haematocrit"),
    "CaO2": (18.0, 22.0, "mL O2/dL", "Arterial O2 content"),
    "CvO2": (14.0, 16.0, "mL O2/dL", "Mixed venous O2 content"),
    "SaO2": (0.95, 1.0, "fraction", "Arterial O2 saturation"),
    "PaO2": (80.0, 100.0, "mmHg", "Arterial PO2"),
    "PaCO2": (35.0, 45.0, "mmHg", "Arterial PCO2"),
    "pH":   (7.35, 7.45, "dimensionless", "Arterial pH"),
    "HCO3_normal": (22.0, 26.0, "mEq/L", "Normal plasma bicarbonate"),
    # Cardiovascular
    "CO":   (4.0, 8.0, "L/min", "Cardiac output"),
    "CI":   (2.5, 4.0, "L/min/m2", "Cardiac index"),
    "HR":   (60.0, 100.0, "bpm", "Resting heart rate"),
    "SV":   (60.0, 100.0, "mL", "Stroke volume"),
    "EF":   (0.55, 0.70, "fraction", "LV ejection fraction"),
    "EDV_normal": (100.0, 160.0, "mL", "Normal LV end-diastolic volume"),
    "ESV_normal": (40.0, 70.0, "mL", "Normal LV end-systolic volume"),
    "MAP":  (70.0, 105.0, "mmHg", "Mean arterial pressure"),
    "SBP":  (100.0, 140.0, "mmHg", "Systolic blood pressure"),
    "DBP":  (60.0, 90.0, "mmHg", "Diastolic blood pressure"),
    "TPR":  (900.0, 1500.0, "dyn*s/cm5", "Systemic vascular resistance"),
    "BSA":  (1.5, 2.2, "m2", "Adult body surface area"),
    # Renal
    "GFR":  (90.0, 140.0, "mL/min", "Normal glomerular filtration rate"),
    "RPF":  (500.0, 650.0, "mL/min", "Renal plasma flow"),
    "RBF":  (1000.0, 1250.0, "mL/min", "Renal blood flow"),
    "FF":   (0.15, 0.25, "fraction", "Filtration fraction"),
}


def reference_range(quantity: str) -> Optional[Tuple[float, float]]:
    """Return (low, high) whole-body reference range for a quantity, or None."""
    entry = REFERENCE_RANGES.get(quantity)
    return (entry[0], entry[1]) if entry else None


def describe(quantity: str) -> Optional[str]:
    """Return a human-readable description of a reference range, or None."""
    entry = REFERENCE_RANGES.get(quantity)
    if not entry:
        return None
    lo, hi, units, note = entry
    return f"{quantity}: {lo}-{hi} {units} ({note})"

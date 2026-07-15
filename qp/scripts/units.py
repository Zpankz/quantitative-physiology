"""Canonical clinical-unit conversions.

Single source of truth for the SI<->US lab conversions that several equations need,
so the factor and the strict-on-unknown behaviour live in exactly one place instead
of being copy-pasted (and drifting) across ckd_epi/mdrd/cockcroft/van-Slyke.
"""

# creatinine: SI umol/L -> US mg/dL divides by the molar mass factor 88.4
_CREATININE_UMOL_PER_MGDL = 88.4
_UMOL = ("umol/L", "µmol/L", "μmol/L")

# haemoglobin monomer: g/L -> mM /16.1 ; g/dL -> mM /1.61
_HB_GL_PER_MM = 16.1
_HB_GDL_PER_MM = 1.61


def creatinine_to_mgdl(value: float, units: str = "mg/dL") -> float:
    """Serum creatinine in the given units -> mg/dL. Raises on an unknown unit
    (never a silent mg/dL fallback)."""
    if units == "mg/dL":
        return value
    if units in _UMOL:
        return value / _CREATININE_UMOL_PER_MGDL
    raise ValueError(f"unknown creatinine units {units!r}; use 'mg/dL' or 'umol/L'")


def hb_to_mM(value: float, units: str = "mM") -> float:
    """Haemoglobin in the given units -> mM. Raises on an unknown unit."""
    if units == "mM":
        return value
    if units == "g/L":
        return value / _HB_GL_PER_MM
    if units == "g/dL":
        return value / _HB_GDL_PER_MM
    raise ValueError(f"unknown Hb units {units!r}; use 'mM', 'g/L' or 'g/dL'")

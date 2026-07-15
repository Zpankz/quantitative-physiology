"""
Cardiovascular System Equations (Unit 5)

Complete equation set for cardiovascular physiology including:
- Blood composition and oxygen transport
- Cardiac electrophysiology and ECG
- Cardiac mechanics and function
- Hemodynamics and vascular mechanics
- Microcirculation and capillary exchange

Source: Quantitative Human Physiology 3rd Edition, Unit 5
"""

# Blood equations
from .blood import (
    hematocrit,
    blood_viscosity,
    oxygen_content,
    hill_saturation,
    oxygen_delivery,
)

# ECG equations
from .ecg import (
    funny_current,
    heart_rate,
    qtc_bazett,
    qtc_fridericia,
)

# Cardiac mechanics equations
from .cardiac import (
    cardiac_output,
    cardiac_output_fick,
    ejection_fraction,
    body_surface_area,
    cardiac_index,
    espvr,
    edpvr,
)

# Hemodynamics equations
from .hemodynamics import (
    poiseuille_resistance,
    tpr,
    mean_arterial_pressure,
    compliance,
    windkessel_tau,
    moens_korteweg,
    bramwell_hill,
    reynolds_number,
    womersley_number,
    bernoulli_equivalent_pressure,
    mean_flow_velocity,
    pulse_pressure,
)

# Microcirculation equations
from .microcirculation import (
    starling_filtration,
    net_filtration_pressure,
    ficks_law_diffusion,
    ps_product,
    shear_stress,
    baroreceptor_sensitivity,
)

__all__ = [
    # Blood (5 equations)
    "hematocrit",
    "blood_viscosity",
    "oxygen_content",
    "hill_saturation",
    "oxygen_delivery",

    # ECG (4 equations)
    "funny_current",
    "heart_rate",
    "qtc_bazett",
    "qtc_fridericia",

    # Cardiac (7 equations)
    "cardiac_output",
    "cardiac_output_fick",
    "ejection_fraction",
    "body_surface_area",
    "cardiac_index",
    "espvr",
    "edpvr",

    # Hemodynamics (9 equations)
    "poiseuille_resistance",
    "tpr",
    "mean_arterial_pressure",
    "compliance",
    "windkessel_tau",
    "moens_korteweg",
    "bramwell_hill",
    "reynolds_number",
    "womersley_number",
    "bernoulli_equivalent_pressure",
    "mean_flow_velocity",
    "pulse_pressure",

    # Microcirculation (6 equations)
    "starling_filtration",
    "net_filtration_pressure",
    "ficks_law_diffusion",
    "ps_product",
    "shear_stress",
    "baroreceptor_sensitivity",
]

# Total: 31 equations extracted from Unit 5

# --- coverage pass additions (Feher extraction) ---
from .blood import (
    mean_cell_volume,
    mean_corpuscular_hemoglobin_concentration,
    plasma_buffer_capacity,
    mean_corpuscular_hemoglobin,
    transferrin_saturation,
)
from .cardiac import (
    stroke_volume,
    indicator_dilution_cardiac_output,
)
from .hemodynamics import (
    systemic_vascular_compliance,
    vascular_function_curve,
)
from .microcirculation import (
    capillary_pressure,
    colloid_osmotic_pressure,
)
__all__ += ['mean_cell_volume', 'mean_corpuscular_hemoglobin_concentration', 'plasma_buffer_capacity', 'mean_corpuscular_hemoglobin', 'transferrin_saturation', 'stroke_volume', 'indicator_dilution_cardiac_output', 'systemic_vascular_compliance', 'vascular_function_curve', 'capillary_pressure', 'colloid_osmotic_pressure']

# --- coverage pass 2 (residual reconsideration) ---
from .ecg import (
    einthoven_lead_relation,
)
__all__ += ['einthoven_lead_relation']

# --- clinical additions (CICM, beyond Feher) ---
from .cardiac import (
    arterial_elastance,
)
from .ecg import (
    rate_pressure_product,
)
from .hemodynamics import (
    svr_dyn,
    pvr_dyn,
    ventricular_wall_stress,
    pulse_pressure_from_compliance,
    map_from_flow,
)
__all__ += ['arterial_elastance', 'rate_pressure_product', 'svr_dyn', 'pvr_dyn', 'ventricular_wall_stress', 'pulse_pressure_from_compliance', 'map_from_flow']

# --- review-add 2026-07-15 ---
from scripts.cardiovascular.hemodynamics import coronary_perfusion_pressure_equation
from scripts.cardiovascular.hemodynamics import stroke_work_equation
__all__ += ['coronary_perfusion_pressure_equation', 'stroke_work_equation']

# --- backlog-complete-add ---
from scripts.cardiovascular.cardiac import frank_starling_equation
__all__ += ['frank_starling_equation']

# --- backlog-complete-add ---
from scripts.cardiovascular.blood import mixed_venous_oxygen_content_equation
__all__ += ['mixed_venous_oxygen_content_equation']

# --- backlog-complete-add ---
from scripts.cardiovascular.cardiac import va_coupling_esv_equation
__all__ += ['va_coupling_esv_equation']

"""
Respiratory physiology equations.

Unit 6 from Quantitative Human Physiology 3rd Edition.
Covers ventilation mechanics, gas exchange, oxygen/CO2 transport,
respiratory control, and acid-base balance.
"""

# Lung volumes and capacities
from .volumes import (
    total_lung_capacity,
    vital_capacity,
    functional_residual_capacity,
    inspiratory_capacity,
    minute_ventilation,
    alveolar_ventilation,
)

# Respiratory mechanics
from .mechanics import (
    transmural_pressure,
    compliance,
    total_compliance,
    elastance,
    total_elastance,
    laplace_pressure,
    airway_resistance,
    pressure_flow,
    reynolds_number,
    time_constant,
    exponential_emptying,
)

# Gas exchange
from .gas_exchange import (
    partial_pressure,
    inspired_po2,
    alveolar_gas_equation,
    aa_gradient,
    diffusing_capacity,
    dlco_to_dlo2,
    diffusion_conductance,
)

# Ventilation-perfusion matching
from .vq_matching import (
    shunt_equation,
    dead_space_bohr,
)

# Oxygen transport
from .oxygen_transport import (
    oxygen_content,
    hill_equation,
    oxygen_delivery,
    oxygen_consumption_fick,
    oxygen_extraction_ratio,
)

# CO2 transport
from .co2_transport import (
    dissolved_co2,
)

# Ventilatory control
from .ventilatory_control import (
    co2_response,
    hypoxic_response,
)

# Acid-base balance
from .acid_base import (
    henderson_hasselbalch,
    anion_gap,
    winters_formula,
    metabolic_alkalosis_compensation,
    acute_respiratory_ph_change,
    chronic_respiratory_acidosis_hco3,
    chronic_respiratory_alkalosis_hco3,
)

__all__ = [
    # Volumes (6 equations)
    'total_lung_capacity',
    'vital_capacity',
    'functional_residual_capacity',
    'inspiratory_capacity',
    'minute_ventilation',
    'alveolar_ventilation',

    # Mechanics (11 equations)
    'transmural_pressure',
    'compliance',
    'total_compliance',
    'elastance',
    'total_elastance',
    'laplace_pressure',
    'airway_resistance',
    'pressure_flow',
    'reynolds_number',
    'time_constant',
    'exponential_emptying',

    # Gas exchange (7 equations)
    'partial_pressure',
    'inspired_po2',
    'alveolar_gas_equation',
    'aa_gradient',
    'diffusing_capacity',
    'dlco_to_dlo2',
    'diffusion_conductance',

    # V/Q matching (2 equations)
    'shunt_equation',
    'dead_space_bohr',

    # Oxygen transport (5 equations)
    'oxygen_content',
    'hill_equation',
    'oxygen_delivery',
    'oxygen_consumption_fick',
    'oxygen_extraction_ratio',

    # CO2 transport (1 equation)
    'dissolved_co2',

    # Ventilatory control (2 equations)
    'co2_response',
    'hypoxic_response',

    # Acid-base (7 equations)
    'henderson_hasselbalch',
    'anion_gap',
    'winters_formula',
    'metabolic_alkalosis_compensation',
    'acute_respiratory_ph_change',
    'chronic_respiratory_acidosis_hco3',
    'chronic_respiratory_alkalosis_hco3',
]

# --- coverage pass additions (Feher extraction) ---
from .acid_base import (
    base_excess_van_slyke,
    strong_ion_difference_apparent,
    standard_base_excess,
    weak_acid_anion_charge,
    strong_ion_difference_effective,
    strong_ion_gap,
)
from .gas_exchange import (
    alveolar_pco2_equation,
)
from .mechanics import (
    rohrer_equation,
    fev1_fvc_ratio,
)
from .oxygen_transport import (
    oxygen_consumption_gas_exchange,
)
__all__ += ['base_excess_van_slyke', 'strong_ion_difference_apparent', 'standard_base_excess', 'weak_acid_anion_charge', 'strong_ion_difference_effective', 'strong_ion_gap', 'alveolar_pco2_equation', 'rohrer_equation', 'fev1_fvc_ratio', 'oxygen_consumption_gas_exchange']

# --- clinical additions (CICM, beyond Feher) ---
from .gas_exchange import (
    pf_ratio,
)
from .mechanics import (
    driving_pressure,
    static_compliance,
)
__all__ += ['pf_ratio', 'driving_pressure', 'static_compliance']

# --- review-add 2026-07-15 ---
from scripts.respiratory.acid_base import kassirer_bleich_hydrogen_ion_equation
from scripts.respiratory.mechanics import work_of_breathing_elastic_equation
__all__ += ['kassirer_bleich_hydrogen_ion_equation', 'work_of_breathing_elastic_equation']

# --- adversarial-review-add ---
from scripts.respiratory.gas_exchange import oxygenation_index_equation
__all__ += ['oxygenation_index_equation']

# --- adversarial-review-add ---
from scripts.respiratory.acid_base import acute_respiratory_acidosis_hco3_equation
__all__ += ['acute_respiratory_acidosis_hco3_equation']

# --- adversarial-review-add ---
from scripts.respiratory.acid_base import acute_respiratory_alkalosis_hco3_equation
__all__ += ['acute_respiratory_alkalosis_hco3_equation']

# --- backlog-complete-add ---
from scripts.respiratory.gas_exchange import aa_gradient_age_limit_equation
__all__ += ['aa_gradient_age_limit_equation']

# --- backlog-complete-add ---
from scripts.respiratory.mechanics import dynamic_compliance_equation
__all__ += ['dynamic_compliance_equation']

# --- backlog-complete-add ---
from scripts.respiratory.gas_exchange import p50_bohr_ph_equation
__all__ += ['p50_bohr_ph_equation']

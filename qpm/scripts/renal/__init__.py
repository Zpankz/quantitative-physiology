"""
Renal Physiology Equations - Unit 7

All atomic equation modules for renal physiology including:
- Blood flow and vascular resistance
- Glomerular filtration and Starling forces
- Clearance calculations
- Tubular transport and mass balance
- Concentration and dilution mechanisms
- Acid-base handling
- Potassium regulation

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher
"""

# Blood Flow
from scripts.renal.blood_flow import renal_plasma_flow
from scripts.renal.blood_flow import filtration_fraction
from scripts.renal.blood_flow import renal_vascular_resistance

# Glomerular Filtration
from scripts.renal.glomerular import net_filtration_pressure
from scripts.renal.glomerular import gfr_from_nfp
from scripts.renal.glomerular import gfr_normalized

# Clearance
from scripts.renal.clearance import clearance
from scripts.renal.clearance import filtered_load
from scripts.renal.clearance import cockcroft_gault
from scripts.renal.clearance import (
    pah_extraction_ratio,
    true_rpf_from_pah
)

# Tubular Transport
from scripts.renal.tubular import excretion_mass_balance
from scripts.renal.tubular import (
    fractional_excretion,
    fractional_excretion_direct
)
from scripts.renal.tubular import fe_na
from scripts.renal.tubular import transport_tm
from scripts.renal.tubular import glucose_excretion

# Concentration Mechanisms
from scripts.renal.concentration import medullary_gradient
from scripts.renal.concentration import (
    countercurrent_multiplication
)
from scripts.renal.concentration import free_water_clearance
from scripts.renal.concentration import urine_osmolality_ratio
from scripts.renal.concentration import adh_water_permeability
from scripts.renal.concentration import water_reabsorption_flux

# Acid-Base
from scripts.renal.acid_base import net_acid_excretion
from scripts.renal.acid_base import (
    new_bicarbonate_generation
)

# Potassium Handling
from scripts.renal.potassium import (
    k_secretion_driving_force
)
from scripts.renal.potassium import k_nernst_potential
from scripts.renal.potassium import k_secretion_flux

# Autoregulation
from scripts.renal.regulation import (
    tubuloglomerular_feedback,
    renal_autoregulation_index,
)


__all__ = [
    # Blood Flow (3 equations)
    'renal_plasma_flow',
    'filtration_fraction',
    'renal_vascular_resistance',

    # Glomerular Filtration (3 equations)
    'net_filtration_pressure',
    'gfr_from_nfp',
    'gfr_normalized',

    # Clearance (6 equations)
    'clearance',
    'filtered_load',
    'cockcroft_gault',
    'pah_extraction_ratio',
    'true_rpf_from_pah',

    # Tubular Transport (7 equations)
    'excretion_mass_balance',
    'fractional_excretion',
    'fractional_excretion_direct',
    'fe_na',
    'transport_tm',
    'glucose_excretion',

    # Concentration Mechanisms (6 equations)
    'medullary_gradient',
    'countercurrent_multiplication',
    'free_water_clearance',
    'urine_osmolality_ratio',
    'adh_water_permeability',
    'water_reabsorption_flux',

    # Acid-Base (2 equations)
    'net_acid_excretion',
    'new_bicarbonate_generation',

    # Potassium Handling (3 equations)
    'k_secretion_driving_force',
    'k_nernst_potential',
    'k_secretion_flux',

    # Autoregulation (2 equations)
    'tubuloglomerular_feedback',
    'renal_autoregulation_index',
]

# Total: 30 equations for Unit 7 (Renal)
# = blood_flow 3 + glomerular 3 + clearance 5 + tubular 6
#   + concentration 6 + acid_base 2 + potassium 3 + regulation 2

# --- coverage pass additions (Feher extraction) ---
from .clearance import (
    mdrd_gfr,
)
from .compartments import (
    lean_body_mass,
)
from .glomerular import (
    sieving_coefficient,
)
from .tubular import (
    fractional_water_reabsorption,
)
__all__ += ['mdrd_gfr', 'lean_body_mass', 'sieving_coefficient', 'fractional_water_reabsorption']

# --- clinical additions (CICM, beyond Feher) ---
from .acid_base import (
    corrected_anion_gap,
    delta_ratio,
)
from .tubular import (
    fe_urea,
)
__all__ += ['corrected_anion_gap', 'delta_ratio', 'fe_urea']

# --- review-add 2026-07-15 ---
from scripts.renal.clearance import ttkg_equation
from scripts.renal.clearance import ckd_epi_2021_equation
__all__ += ['ttkg_equation', 'ckd_epi_2021_equation']

from scripts.renal.clearance import sodium_clearance
__all__ += ['sodium_clearance']

from scripts.renal.clearance import creatinine_clearance_typed
__all__ += ['creatinine_clearance_typed']

from scripts.renal.clearance import gfr_from_glomerular_nfp
__all__ += ['gfr_from_glomerular_nfp']

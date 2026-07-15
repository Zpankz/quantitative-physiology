"""
Excitable Cells Domain Module

Equations for action potentials, nerve conduction, muscle mechanics,
and neuromuscular transmission from Unit 3 of Quantitative Human Physiology.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher

Organization:
- membrane_potential/: GHK and chord conductance equations
- action_potential/: Hodgkin-Huxley model and cable theory
- muscle/: Force-velocity, cross-bridge, and calcium-force coupling
- synapse/: Neuromuscular junction transmission
- energetics/: ATP consumption and efficiency
"""

# Import all submodules
from . import membrane_potential
from . import action_potential
from . import muscle
from . import synapse
from . import energetics

# Import all equations
from .membrane_potential import *
from .action_potential import *
from .muscle import *
from .synapse import *
from .energetics import *

__all__ = [
    # Submodules
    'membrane_potential',
    'action_potential',
    'muscle',
    'synapse',
    'energetics',

    # Membrane potential equations
    'ghk_potential_eq',
    'chord_conductance_eq',

    # Action potential equations (Hodgkin-Huxley)
    'hh_membrane_current_eq',
    'hh_sodium_current_eq',
    'hh_potassium_current_eq',
    'hh_leak_current_eq',
    'hh_gating_m_eq',
    'hh_gating_h_eq',
    'hh_gating_n_eq',

    # Cable theory equations
    'cable_equation_eq',
    'space_constant_eq',
    'time_constant_eq',

    # Muscle mechanics equations
    'hill_force_velocity_eq',
    'muscle_power_eq',
    'ca_force_relationship_eq',

    # Cross-bridge model equations
    'huxley_attachment_rate_eq',
    'huxley_detachment_rate_eq',
    'huxley_attached_fraction_eq',

    # Synapse equations
    'quantal_content_eq',
    'safety_factor_eq',

    # Energetics equations
    'atp_consumption_eq',
    'muscle_efficiency_eq',
]

# --- coverage pass additions (Feher extraction) ---
from .action_potential import (
    strength_duration_weiss,
)
from .muscle import (
    architectural_gear_ratio,
    motor_unit_force,
)
__all__ += ['strength_duration_weiss', 'architectural_gear_ratio', 'motor_unit_force']

# --- clinical additions (CICM, beyond Feher) ---
from .membrane_potential import (
    driving_force_ion,
    ionic_current,
)
__all__ += ['driving_force_ion', 'ionic_current']

# --- review-add 2026-07-15 ---
from scripts.excitable.action_potential import passive_membrane_charging_equation
from scripts.excitable.action_potential import hursh_conduction_velocity_equation
__all__ += ['passive_membrane_charging_equation', 'hursh_conduction_velocity_equation']

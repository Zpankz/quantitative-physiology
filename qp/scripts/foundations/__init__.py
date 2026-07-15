"""
Physical and Chemical Foundations of Physiology (Unit 1)

Atomic equation modules for:
- Transport: Pressure-driven flow, Poiseuille, Laplace
- Electrical: Coulomb, capacitance
- Diffusion: Fick's laws, Stokes-Einstein
- Thermodynamics: Gibbs energy, Nernst equation

All equations are registered in the global index on import.
"""

# Import all subdomain modules (triggers equation registration)
from . import transport
from . import electrical
from . import diffusion
from . import thermodynamics
from . import kinetics

# Re-export all equations for convenient access
from .transport import *
from .electrical import *
from .diffusion import *
from .thermodynamics import *
from .kinetics import *

__all__ = (
    transport.__all__ +
    electrical.__all__ +
    diffusion.__all__ +
    thermodynamics.__all__ +
    kinetics.__all__
)

# --- coverage pass additions (Feher extraction) ---
from .diffusion import (
    convection_diffusion_flux,
)
from .electrical import (
    lennard_jones_potential,
    electric_dipole_moment,
    dipole_potential,
)
from .kinetics import (
    arrhenius_equation,
)
from .thermodynamics import (
    redox_free_energy,
    body_energy_balance,
    ideal_gas_law,
)
from .transport import (
    volume_of_distribution,
)
__all__ += ['convection_diffusion_flux', 'lennard_jones_potential', 'electric_dipole_moment', 'dipole_potential', 'arrhenius_equation', 'redox_free_energy', 'body_energy_balance', 'ideal_gas_law', 'volume_of_distribution']

# --- coverage pass 2 (residual reconsideration) ---
from .thermodynamics import (
    enthalpy,
)
__all__ += ['enthalpy']

# --- clinical additions (CICM, beyond Feher) ---
from .kinetics import (
    first_order_elimination,
    elimination_rate_constant,
    loading_dose,
    maintenance_infusion_rate,
)
__all__ += ['first_order_elimination', 'elimination_rate_constant', 'loading_dose', 'maintenance_infusion_rate']

# --- review-add 2026-07-15 ---
from scripts.foundations.kinetics import bioavailability_auc_equation
from scripts.foundations.kinetics import average_steady_state_concentration_equation
__all__ += ['bioavailability_auc_equation', 'average_steady_state_concentration_equation']

# --- backlog-complete-add ---
from scripts.foundations.kinetics import apparent_volume_of_distribution_equation
__all__ += ['apparent_volume_of_distribution_equation']

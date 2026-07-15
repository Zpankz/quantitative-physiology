"""
Membrane, Transport, and Metabolism Equations (Unit 2)

This module contains atomic equation components for:
- Membrane structure and properties
- Passive and active transport
- Osmosis and water balance
- Gibbs-Donnan equilibrium
- Cell signaling and receptor kinetics
- Cellular metabolism and energy production

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""

# Membrane structure
from .structure import (
    membrane_capacitance,
    permeability_coefficient,
)

# Membrane potential
from .potential import (
    donnan_ratio,
    donnan_potential,
)

# Transport mechanisms
from .transport import (
    ficks_membrane_flux,
    goldman_flux,
    carrier_transport,
    single_channel_conductance,
    whole_cell_conductance,
    nak_pump_rate,
    ncx_reversal,
)

# Osmosis and water balance
from .osmosis import (
    osmotic_pressure,
    water_flux,
)

# Cell signaling
from .signaling import (
    receptor_occupancy,
    scatchard_analysis,
)

# Cellular metabolism
from .metabolism import (
    chemiosmotic_coupling,
    basal_metabolic_rate,
    respiratory_quotient,
)

__all__ = [
    # Structure (2 equations)
    'membrane_capacitance',
    'permeability_coefficient',

    # Potential (2 equations)
    'donnan_ratio',
    'donnan_potential',

    # Transport (7 equations)
    'ficks_membrane_flux',
    'goldman_flux',
    'carrier_transport',
    'single_channel_conductance',
    'whole_cell_conductance',
    'nak_pump_rate',
    'ncx_reversal',

    # Osmosis (2 equations)
    'osmotic_pressure',
    'water_flux',

    # Signaling (2 equations)
    'receptor_occupancy',
    'scatchard_analysis',

    # Metabolism (3 equations)
    'chemiosmotic_coupling',
    'basal_metabolic_rate',
    'respiratory_quotient',
]

# Total: 18 atomic equations from Unit 2

# --- coverage pass additions (Feher extraction) ---
from .mechanics import (
    youngs_modulus,
    kelvin_voigt_model,
    maxwell_model,
    persistence_length,
    poisson_ratio,
    standard_linear_solid,
)
from .osmosis import (
    boyle_vant_hoff_relation,
)
from .structure import (
    surface_pressure,
    surface_free_energy,
    partition_coefficient,
)
from .transport import (
    ussing_flux_ratio,
)
__all__ += ['youngs_modulus', 'kelvin_voigt_model', 'maxwell_model', 'persistence_length', 'poisson_ratio', 'standard_linear_solid', 'boyle_vant_hoff_relation', 'surface_pressure', 'surface_free_energy', 'partition_coefficient', 'ussing_flux_ratio']

# --- coverage pass 2 (residual reconsideration) ---
from .mechanics import (
    newtonian_viscosity,
)
__all__ += ['newtonian_viscosity']

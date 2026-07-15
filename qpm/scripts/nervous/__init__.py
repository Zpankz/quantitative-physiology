"""
Nervous System Equations - Unit 4

All equations related to nervous system physiology including:
- Synaptic transmission (vesicle release, postsynaptic potentials)
- Neural integration (cable theory, dendritic processing)
- Sensory encoding (psychophysics, receptive fields, adaptation)
- Motor control (force production, proprioception, reflexes)
- Synaptic plasticity (short-term and long-term modifications)

Source: Quantitative Human Physiology 3rd Edition, Unit 4
"""

# Synaptic transmission
from scripts.nervous.synaptic import ca_release_cooperative
from scripts.nervous.synaptic import quantal_content
from scripts.nervous.synaptic import quantal_variance
from scripts.nervous.synaptic import synaptic_current
from scripts.nervous.synaptic import epsp_amplitude
from scripts.nervous.synaptic import alpha_function
from scripts.nervous.synaptic import double_exponential
from scripts.nervous.synaptic import nmda_mg_block
from scripts.nervous.synaptic import shunting_inhibition

# Neural integration
from scripts.nervous.integration import cable_equation
from scripts.nervous.integration import dendrite_input_resistance

# Sensory physiology
from scripts.nervous.sensory import weber_fraction
from scripts.nervous.sensory import fechner_law
from scripts.nervous.sensory import stevens_power_law
from scripts.nervous.sensory import receptor_adaptation
from scripts.nervous.sensory import adaptation_index
from scripts.nervous.sensory import receptive_field_dog
from scripts.nervous.sensory import photoreceptor_response

# Motor control
from scripts.nervous.motor import rate_force_relation
from scripts.nervous.motor import fusion_frequency
from scripts.nervous.motor import spindle_response
from scripts.nervous.motor import gto_response
from scripts.nervous.motor import reflex_gain

# Synaptic plasticity
from scripts.nervous.plasticity import facilitation
from scripts.nervous.plasticity import depression
from scripts.nervous.plasticity import stdp
from scripts.nervous.plasticity import bcm_theory

__all__ = [
    # Synaptic transmission (9 equations)
    'ca_release_cooperative',
    'quantal_content',
    'quantal_variance',
    'synaptic_current',
    'epsp_amplitude',
    'alpha_function',
    'double_exponential',
    'nmda_mg_block',
    'shunting_inhibition',

    # Neural integration (2 equations)
    'cable_equation',
    'dendrite_input_resistance',

    # Sensory physiology (7 equations)
    'weber_fraction',
    'fechner_law',
    'stevens_power_law',
    'receptor_adaptation',
    'adaptation_index',
    'receptive_field_dog',
    'photoreceptor_response',

    # Motor control (5 equations)
    'rate_force_relation',
    'fusion_frequency',
    'spindle_response',
    'gto_response',
    'reflex_gain',

    # Synaptic plasticity (4 equations)
    'facilitation',
    'depression',
    'stdp',
    'bcm_theory',
]

# --- coverage pass additions (Feher extraction) ---
from .hearing import (
    sound_intensity_level_db,
    acoustic_intensity,
)
from .sensory import (
    direction_selectivity_index,
    orientation_selectivity_index,
    norwich_sensation_magnitude,
)
from .vision import (
    snells_law,
    thin_lens_formula,
    refractive_power_diopters,
)
__all__ += ['sound_intensity_level_db', 'acoustic_intensity', 'direction_selectivity_index', 'orientation_selectivity_index', 'norwich_sensation_magnitude', 'snells_law', 'thin_lens_formula', 'refractive_power_diopters']

# --- coverage pass 2 (residual reconsideration) ---
from .vision import (
    refractive_index,
)
__all__ += ['refractive_index']

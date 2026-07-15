"""
Endocrine physiology equations.

Unit 9: Endocrine Physiology
Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher

This module contains all atomic equations for endocrine system physiology,
organized by topic:
- kinetics: Hormone binding, clearance, half-life
- receptor: Receptor binding kinetics and occupancy
- feedback: Negative feedback regulation
- thyroid: Thyroid axis (TSH, T4, T3)
- adrenal: HPA axis and aldosterone
- pancreatic: Insulin secretion and glucose regulation
- calcium: PTH, vitamin D, calcium homeostasis
- reproductive: LH surge, progesterone effects
"""

# Kinetics equations
from scripts.endocrine.kinetics import kd_equation
from scripts.endocrine.kinetics import fraction_free_equation
from scripts.endocrine.kinetics import mcr_equation
from scripts.endocrine.kinetics import half_life_equation

# Receptor binding equations
from scripts.endocrine.receptor import saturation_binding_equation
from scripts.endocrine.receptor import scatchard_equation
from scripts.endocrine.receptor import fractional_occupancy_equation

# Feedback regulation equations
from scripts.endocrine.feedback import target_feedback_equation
from scripts.endocrine.feedback import tropic_feedback_equation
from scripts.endocrine.feedback import feedback_gain_equation

# Thyroid axis equations
from scripts.endocrine.thyroid import tsh_response_equation
from scripts.endocrine.thyroid import t4_production_equation
from scripts.endocrine.thyroid import tsh_dynamics_equation
from scripts.endocrine.thyroid import t4_dynamics_equation

# Adrenal (HPA axis) equations
from scripts.endocrine.adrenal import crh_dynamics_equation
from scripts.endocrine.adrenal import acth_dynamics_equation
from scripts.endocrine.adrenal import cortisol_dynamics_equation
from scripts.endocrine.adrenal import aldosterone_equation

# Pancreatic endocrine equations
from scripts.endocrine.pancreatic import gsis_equation
from scripts.endocrine.pancreatic import homa_ir_equation

# Calcium regulation equations
from scripts.endocrine.calcium import pth_secretion_equation
from scripts.endocrine.calcium import corrected_calcium_equation
from scripts.endocrine.calcium import vitamin_d_activation_equation

# Reproductive hormone equations
from scripts.endocrine.reproductive import lh_surge_equation
from scripts.endocrine.reproductive import progesterone_temp_equation

# Export all equations
__all__ = [
    # Kinetics (4 equations)
    'kd_equation',
    'fraction_free_equation',
    'mcr_equation',
    'half_life_equation',

    # Receptor binding (3 equations)
    'saturation_binding_equation',
    'scatchard_equation',
    'fractional_occupancy_equation',

    # Feedback regulation (3 equations)
    'target_feedback_equation',
    'tropic_feedback_equation',
    'feedback_gain_equation',

    # Thyroid axis (4 equations)
    'tsh_response_equation',
    't4_production_equation',
    'tsh_dynamics_equation',
    't4_dynamics_equation',

    # Adrenal/HPA axis (4 equations)
    'crh_dynamics_equation',
    'acth_dynamics_equation',
    'cortisol_dynamics_equation',
    'aldosterone_equation',

    # Pancreatic endocrine (2 equations)
    'gsis_equation',
    'homa_ir_equation',

    # Calcium regulation (3 equations)
    'pth_secretion_equation',
    'corrected_calcium_equation',
    'vitamin_d_activation_equation',

    # Reproductive hormones (2 equations)
    'lh_surge_equation',
    'progesterone_temp_equation',
]

# Total: 25 atomic equations

# --- coverage pass additions (Feher extraction) ---
from .calcium import (
    beer_lambert_attenuation,
)
from .receptor import (
    cheng_prusoff_ki,
    competitive_inhibition_binding,
)
__all__ += ['beer_lambert_attenuation', 'cheng_prusoff_ki', 'competitive_inhibition_binding']

# --- review-add 2026-07-15 ---
from scripts.endocrine.pancreatic import homa_b_equation
__all__ += ['homa_b_equation']
from scripts.endocrine.kinetics import clearance_from_metabolic_rate
__all__ += ['clearance_from_metabolic_rate']
from scripts.endocrine.kinetics import hormone_half_life_from_mcr
__all__ += ['hormone_half_life_from_mcr']

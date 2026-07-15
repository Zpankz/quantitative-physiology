"""
Gastrointestinal physiology equations.

This module contains atomic equations for GI tract function including:
- Motility (slow waves, peristalsis, gastric emptying, transit)
- Secretion (salivary, gastric, pancreatic, bile)
- Digestion (enzyme kinetics, carbohydrate, protein, lipid)
- Absorption (glucose, fructose, water, nutrients, minerals)
- Hormones (gastrin, secretin, CCK, incretins, GLP-1)
- Liver function (blood flow, extraction, clearance, bilirubin, lithogenic index)

Source: Quantitative Human Physiology 3rd Edition, Unit 8
"""

# Motility equations
from scripts.gastrointestinal.motility import slow_wave
from scripts.gastrointestinal.motility import peristalsis_velocity
from scripts.gastrointestinal.motility import gastric_emptying_liquid
from scripts.gastrointestinal.motility import gastric_emptying_solid
from scripts.gastrointestinal.motility import transit_time

# Secretion equations
from scripts.gastrointestinal.secretion import salivary_flow
from scripts.gastrointestinal.secretion import gastric_acid_output
from scripts.gastrointestinal.secretion import pancreatic_bicarbonate
from scripts.gastrointestinal.secretion import bile_acid_synthesis
from scripts.gastrointestinal.secretion import critical_micellar_concentration

# Digestion equations
from scripts.gastrointestinal.digestion import enzyme_kinetics
from scripts.gastrointestinal.digestion import pepsin_activity
from scripts.gastrointestinal.digestion import amylase_kinetics
from scripts.gastrointestinal.digestion import lipase_kinetics
from scripts.gastrointestinal.digestion import lipase_activity_bile
from scripts.gastrointestinal.digestion import starch_digestion_first_order

# Absorption equations
from scripts.gastrointestinal.absorption import sglt1_glucose
from scripts.gastrointestinal.absorption import glut5_fructose
from scripts.gastrointestinal.absorption import water_absorption
from scripts.gastrointestinal.absorption import calcium_absorption
from scripts.gastrointestinal.absorption import iron_absorption
from scripts.gastrointestinal.absorption import fat_absorption_efficiency

# Hormone equations
from scripts.gastrointestinal.hormones import gastrin_acid_response
from scripts.gastrointestinal.hormones import secretin_bicarbonate
from scripts.gastrointestinal.hormones import cck_response
from scripts.gastrointestinal.hormones import incretin_effect
from scripts.gastrointestinal.hormones import glp1_insulin_response
from scripts.gastrointestinal.hormones import cck_satiety

# Liver function equations
from scripts.gastrointestinal.liver import hepatic_blood_flow
from scripts.gastrointestinal.liver import extraction_ratio
from scripts.gastrointestinal.liver import hepatic_clearance
from scripts.gastrointestinal.liver import first_pass_effect
from scripts.gastrointestinal.liver import bilirubin_production
from scripts.gastrointestinal.liver import lithogenic_index

__all__ = [
    # Motility (5 equations)
    'slow_wave',
    'peristalsis_velocity',
    'gastric_emptying_liquid',
    'gastric_emptying_solid',
    'transit_time',

    # Secretion (5 equations)
    'salivary_flow',
    'gastric_acid_output',
    'pancreatic_bicarbonate',
    'bile_acid_synthesis',
    'critical_micellar_concentration',

    # Digestion (6 equations)
    'enzyme_kinetics',
    'pepsin_activity',
    'amylase_kinetics',
    'lipase_kinetics',
    'lipase_activity_bile',
    'starch_digestion_first_order',

    # Absorption (6 equations)
    'sglt1_glucose',
    'glut5_fructose',
    'water_absorption',
    'calcium_absorption',
    'iron_absorption',
    'fat_absorption_efficiency',

    # Hormones (6 equations)
    'gastrin_acid_response',
    'secretin_bicarbonate',
    'cck_response',
    'incretin_effect',
    'glp1_insulin_response',
    'cck_satiety',

    # Liver (6 equations)
    'hepatic_blood_flow',
    'extraction_ratio',
    'hepatic_clearance',
    'first_pass_effect',
    'bilirubin_production',
    'lithogenic_index',
]

# --- coverage pass additions (Feher extraction) ---
from .energy_balance import (
    energy_expenditure_indirect_calorimetry,
    carbohydrate_oxidation_indirect_calorimetry,
    protein_oxidation_urinary_nitrogen,
    fat_oxidation_indirect_calorimetry,
    harris_benedict_bmr,
    mifflin_st_jeor_ree,
)
__all__ += ['energy_expenditure_indirect_calorimetry', 'carbohydrate_oxidation_indirect_calorimetry', 'protein_oxidation_urinary_nitrogen', 'fat_oxidation_indirect_calorimetry', 'harris_benedict_bmr', 'mifflin_st_jeor_ree']

# --- review-add 2026-07-15 ---
from scripts.gastrointestinal.absorption import stool_osmotic_gap_equation
__all__ += ['stool_osmotic_gap_equation']

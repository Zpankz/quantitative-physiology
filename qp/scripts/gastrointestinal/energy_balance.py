"""Gastrointestinal — energy balance and indirect calorimetry equations.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher (Unit 8)
"""
import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation,
)
from scripts.index import register_equation


# --- coverage pass additions (Feher extraction) ---

def compute_energy_expenditure_indirect_calorimetry(VO2, energy_equiv=4.85):
    """Total metabolic rate (energy expenditure) from oxygen consumption by indirect
    calorimetry. Feher 3rd ed. Unit 8, section 8.6, 'DETERMINATION OF ENERGY EXPENDITURE
    BY INDIRECT CALORIMETRY':  M = energy_equiv * VO2.

    Parameters
    ----------
    VO2 : float
        Rate of oxygen consumption, in litres at STPD per unit time (e.g. L/min).
    energy_equiv : float
        Energy equivalent of oxygen (kcal per L O2). Default 4.85 kcal/L is Feher's
        mixed-diet average (~5.0 carbohydrate, 4.7 fat, 4.6 protein). Use 20.3 to
        obtain the metabolic rate in kJ per unit time instead of kcal.

    Returns
    -------
    float
        Metabolic rate M, in kcal per unit time (or kJ per unit time if energy_equiv
        is given in kJ/L), matching the time base of VO2.
    """
    return energy_equiv * VO2

energy_expenditure_indirect_calorimetry = create_equation(
    id='energy_expenditure_indirect_calorimetry',
    output_units='kcal/min',
    name='Energy Expenditure by Indirect Calorimetry',
    category=EquationCategory.GASTROINTESTINAL,
    latex='M = 4.85\\ \\mathrm{kcal\\,L^{-1}} \\times V_{\\mathrm{O_2}} = 20.3\\ \\mathrm{kJ\\,L^{-1}} \\times V_{\\mathrm{O_2}}',
    simplified='M = 4.85 * VO2   (kcal/time; equivalently 20.3 kJ/L * VO2)',
    description="Indirect-calorimetry estimate of total metabolic rate (whole-body energy expenditure) from the rate of oxygen consumption, using the mixed-diet energy equivalent of oxygen (~4.85 kcal/L = 20.3 kJ/L). Feher's standard relation for deriving energy expenditure from gas exchange when direct calorimetry is impractical; VO2 is measured at STPD per unit time and M carries the same time base.",
    compute_func=compute_energy_expenditure_indirect_calorimetry,
    parameters=[
        Parameter(name='VO2', description='Rate of oxygen consumption, in litres at STPD per unit time (e.g. L/min)', units='L/min (STPD)', symbol='V_{O_2}', physiological_range=(0, 10)),
        Parameter(name='energy_equiv', description='Energy equivalent of oxygen (heat released per litre of O2 consumed); Feher mixed-diet average 4.85 kcal/L (= 20.3 kJ/L). Use 20.3 for a kJ output', units='kcal/L O2', symbol='k_{O_2}', default_value=4.85, physiological_range=(4.6, 5.05)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=8, source_chapter='8.6',
                              source_section='DETERMINATION OF ENERGY EXPENDITURE BY INDIRECT CALORIMETRY', page_reference=None,
                              textbook_equation_number='8.6.5'),
)
register_equation(energy_expenditure_indirect_calorimetry)


def compute_carbohydrate_oxidation_indirect_calorimetry(VO2: float, VCO2: float, n: float) -> float:
    """Grams of carbohydrate oxidized from indirect calorimetry (Feher Eq. 8.6.8).

    Solves the simultaneous gas-exchange equations (Eq. 8.6.7) for net carbohydrate
    combustion using measured gas volumes and urinary urea nitrogen.

    Args (units are load-bearing; coefficients are valid ONLY for these units):
        VO2:  volume of O2 consumed over the interval, L at STPD.
        VCO2: volume of CO2 produced over the interval, L at STPD.
        n:    urinary urea nitrogen excreted over the same interval, g.

    Returns:
        Grams of carbohydrate completely oxidized to CO2 and H2O over the interval.
        Dividing by the interval gives the rate of carbohydrate oxidation.
        Valid only at steady state (no net fat/glycogen synthesis, no excretion of
        partially oxidized intermediates such as lactate or ketone bodies).
    """
    return -3.25 * VO2 + 4.59 * VCO2 - 3.75 * n

carbohydrate_oxidation_indirect_calorimetry = create_equation(
    id='carbohydrate_oxidation_indirect_calorimetry',
    output_units='g',
    name='Carbohydrate Oxidation by Indirect Calorimetry',
    category=EquationCategory.GASTROINTESTINAL,
    latex='c = -3.25\\,V_{\\mathrm{O_2}} + 4.59\\,V_{\\mathrm{CO_2}} - 3.75\\,n',
    simplified='c = -3.25*VO2 + 4.59*VCO2 - 3.75*n',
    description="Estimates grams of carbohydrate oxidized from indirect calorimetry. Obtained by solving Feher's simultaneous gas-exchange equations (VO2 = 0.746c + 2.02f + 1.01p; VCO2 = 0.746c + 1.43f + 0.844p) together with protein catabolism from urinary urea nitrogen (p = 6.25n). VO2 and VCO2 are volumes of O2 consumed and CO2 produced (L, STPD) over an interval; n is urinary urea nitrogen (g). The coefficients are unit-specific. A companion relation gives fat oxidation (f = 1.69 VO2 - 1.69 VCO2 - 1.75 n). Used clinically to partition substrate utilization; valid only at steady state with no net lipogenesis, glycogen synthesis, or excretion of partially oxidized intermediates.",
    compute_func=compute_carbohydrate_oxidation_indirect_calorimetry,
    parameters=[
        Parameter(name='VO2', description='Volume of oxygen consumed over the measurement interval, at standard temperature and pressure, dry (STPD)', units='L', symbol='V_{O_2}', physiological_range=(0, 5000)),
        Parameter(name='VCO2', description='Volume of carbon dioxide produced over the measurement interval, at STPD', units='L', symbol='V_{CO_2}', physiological_range=(0, 5000)),
        Parameter(name='n', description='Urinary urea nitrogen excreted over the same interval (protein catabolism marker; p = 6.25n grams of protein)', units='g', symbol='n', physiological_range=(0, 200)),
    ],
    depends_on=[],
    produces='c',
    metadata=EquationMetadata(source_unit=8, source_chapter='8.6',
                              source_section='INDIRECT CALORIMETRY AND URINARY NITROGEN ALLOW ESTIMATION OF CATABOLISM OF MACRONUTRIENTS', page_reference=None,
                              textbook_equation_number='8.6.8'),
)
register_equation(carbohydrate_oxidation_indirect_calorimetry)


def compute_protein_oxidation_urinary_nitrogen(n: float) -> float:
    """Grams of protein catabolized from urinary urea nitrogen (Feher Eq. 8.6.6).

    p (g protein) = 6.25 * n, where n is urinary urea nitrogen in grams.
    Factor 6.25 = 1 / 0.16 because protein is ~16% nitrogen by mass and
    urinary urea nitrogen is essentially the sole nitrogenous end-product of
    protein catabolism. Units: n in g -> returns p in g.

    Source section: 'INDIRECT CALORIMETRY AND URINARY NITROGEN ALLOW
    ESTIMATION OF CATABOLISM OF MACRONUTRIENTS' (Feher 3rd ed., 8.6).
    """
    return 6.25 * n

protein_oxidation_urinary_nitrogen = create_equation(
    id='protein_oxidation_urinary_nitrogen',
    output_units='g',
    name='Protein Catabolism from Urinary Nitrogen',
    category=EquationCategory.GASTROINTESTINAL,
    latex='p = 6.25\\,n',
    simplified='p = 6.25 * n',
    description='Estimates grams of protein catabolized (oxidized) from measured urinary urea nitrogen. Because protein is approximately 16% nitrogen by mass and urinary urea nitrogen derives essentially entirely from protein catabolism, protein mass = n / 0.16 = 6.25 n. Used in indirect calorimetry to determine protein oxidation (the protein input to the O2/CO2 substrate-partition equations 8.6.7-8.6.8) and clinically for nitrogen-balance assessment of protein catabolism. Valid at steady state with no net protein synthesis.',
    compute_func=compute_protein_oxidation_urinary_nitrogen,
    parameters=[
        Parameter(name='n', description='Urinary urea nitrogen excreted (derived from protein catabolism)', units='g', symbol='n', physiological_range=(0, 60)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=8, source_chapter='8.6',
                              source_section='INDIRECT CALORIMETRY AND URINARY NITROGEN ALLOW ESTIMATION OF CATABOLISM OF MACRONUTRIENTS', page_reference=None,
                              textbook_equation_number='8.6.6'),
)
register_equation(protein_oxidation_urinary_nitrogen)


def compute_fat_oxidation_indirect_calorimetry(VO2: float, VCO2: float, n: float) -> float:
    """Fat oxidized (g) from respiratory gas exchange and urinary urea nitrogen.

    Feher Eq 8.6.8, solution of the indirect-calorimetry substrate system:
        f = 1.69*VO2 - 1.69*VCO2 - 1.75*n

    Units (coefficients are unit-specific): VO2, VCO2 = volumes of O2 consumed
    and CO2 produced in L at STPD (or per-unit-time rates if each divided by the
    same interval); n = grams of urinary urea nitrogen. Returns grams of fat
    completely oxidized to CO2 and water. Valid only at metabolic steady state
    (no net fat synthesis, no net glycogen synthesis, no excretion of partially
    oxidized intermediates); outside these conditions (e.g. RQ>1 lipogenesis) it
    can return a nonphysical negative value.
    """
    return 1.69 * VO2 - 1.69 * VCO2 - 1.75 * n

fat_oxidation_indirect_calorimetry = create_equation(
    id='fat_oxidation_indirect_calorimetry',
    output_units='g',
    name='Fat Oxidation Rate (Indirect Calorimetry)',
    category=EquationCategory.GASTROINTESTINAL,
    latex='f = 1.69\\,V_{O_2} - 1.69\\,V_{CO_2} - 1.75\\,n',
    simplified='f = 1.69*VO2 - 1.69*VCO2 - 1.75*n',
    description='Grams of fat oxidized, estimated by indirect calorimetry from O2 consumption, CO2 production, and urinary urea nitrogen (Feher Eq 8.6.8). Derived by solving the simultaneous gas-exchange equations (Eq 8.6.7) using coefficients from Table 8.6.3. Used clinically/in metabolic studies to partition substrate utilization; the companion lines give carbohydrate (c = -3.25 VO2 + 4.59 VCO2 - 3.75 n) and protein (p = 6.25 n) oxidation. Coefficients are valid only for the stated units (L STPD, grams) and only at metabolic steady state with no net lipogenesis, no net glycogen synthesis, and no accumulation/excretion of partially oxidized intermediates (lactate, ketone bodies).',
    compute_func=compute_fat_oxidation_indirect_calorimetry,
    parameters=[
        Parameter(name='VO2', description='Volume of O2 consumed (or O2 consumption rate over the same interval as VCO2)', units='L (STPD)', symbol='V_{O_2}', physiological_range=(0, 1000)),
        Parameter(name='VCO2', description='Volume of CO2 produced (or CO2 production rate over the same interval as VO2)', units='L (STPD)', symbol='V_{CO_2}', physiological_range=(0, 1000)),
        Parameter(name='n', description='Urinary urea nitrogen excreted over the measurement interval (index of protein catabolism)', units='g', symbol='n', physiological_range=(0, 50)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=8, source_chapter='8.6',
                              source_section='INDIRECT CALORIMETRY AND URINARY NITROGEN ALLOW ESTIMATION OF CATABOLISM OF MACRONUTRIENTS', page_reference=None,
                              textbook_equation_number='8.6.8'),
)
register_equation(fat_oxidation_indirect_calorimetry)


def compute_harris_benedict_bmr(W, H, A, sex=1.0):
    """Harris-Benedict (1919) basal metabolic rate predictor; returns BMR in kcal/day. W in kg, H in cm, A in years, sex flag 1=male 0=female. Feher 8.6 'Empirical formulas for BMR'."""
    if sex >= 0.5:
        return 66.5 + 13.7 * W + 5.0 * H - 6.8 * A
    return 655.1 + 9.56 * W + 1.85 * H - 4.7 * A

harris_benedict_bmr = create_equation(
    id='harris_benedict_bmr',
    output_units='kcal/day',
    name='Harris-Benedict BMR Equation',
    category=EquationCategory.GASTROINTESTINAL,
    latex='\\text{Men: } \\mathrm{BMR} = 66.5 + 13.7\\,W + 5.0\\,H - 6.8\\,A \\\\ \\text{Women: } \\mathrm{BMR} = 655.1 + 9.56\\,W + 1.85\\,H - 4.7\\,A',
    simplified='Men: BMR = 66.5 + 13.7*W + 5.0*H - 6.8*A ; Women: BMR = 655.1 + 9.56*W + 1.85*H - 4.7*A  [kcal/day; W kg, H cm, A yr]',
    description="Harris-Benedict (1919) empirical multiple-regression equation predicting basal metabolic rate (kcal/day) from weight, height, age, and sex. A distinct named clinical BMR estimator, not the cross-species Kleiber mass power law (basal_metabolic_rate); used to estimate resting energy requirements. Sex-specific coefficient sets: sex=1 selects the male equation, sex=0 the female. Feher 8.6, 'Empirical formulas for BMR'.",
    compute_func=compute_harris_benedict_bmr,
    parameters=[
        Parameter(name='W', description='Body weight', units='kg', symbol='W', physiological_range=(30, 200)),
        Parameter(name='H', description='Height', units='cm', symbol='H', physiological_range=(100, 220)),
        Parameter(name='A', description='Age', units='years', symbol='A', physiological_range=(15, 90)),
        Parameter(name='sex', description='Biological sex flag selecting the coefficient set: 1 = male equation, 0 = female equation', units='dimensionless', symbol='sex', default_value=1, physiological_range=(0, 1)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=8, source_chapter='8.6',
                              source_section='EMPIRICAL FORMULAS FOR BMR', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(harris_benedict_bmr)


def compute_mifflin_st_jeor_ree(W, H, A, sex=1.0):
    """Mifflin-St. Jeor resting energy expenditure (REE) in kcal/day; Feher 8.6 'Empirical formulas for BMR'.
    W = weight (kg), H = height (cm), A = age (years); sex is a numeric flag: 1.0 = male, 0.0 = female (threshold 0.5)."""
    if sex >= 0.5:
        return 5.0 + 9.99 * W + 6.25 * H - 4.92 * A
    return -161.0 + 9.99 * W + 6.25 * H - 4.92 * A

mifflin_st_jeor_ree = create_equation(
    id='mifflin_st_jeor_ree',
    output_units='kcal/day',
    name='Mifflin-St. Jeor Resting Energy Expenditure',
    category=EquationCategory.GASTROINTESTINAL,
    latex='\\text{Men: } REE = 5 + 9.99\\,W + 6.25\\,H - 4.92\\,A;\\quad \\text{Women: } REE = -161 + 9.99\\,W + 6.25\\,H - 4.92\\,A',
    simplified='REE_male = 5 + 9.99*W + 6.25*H - 4.92*A ; REE_female = -161 + 9.99*W + 6.25*H - 4.92*A  (kcal/day; W kg, H cm, A years)',
    description='Mifflin-St. Jeor (1990) empirical predictor of resting energy expenditure (REE) in kcal/day from weight, height, age, and sex. Feher states it predicts REE better than competing empirical formulas (e.g. Harris-Benedict). Widely used clinical estimator of daily energy needs in nutrition support; REE runs ~10% above the true basal metabolic rate and, unlike BMR, does not require a 12-hour fast.',
    compute_func=compute_mifflin_st_jeor_ree,
    parameters=[
        Parameter(name='W', description='Body weight', units='kg', symbol='W', physiological_range=(30, 300)),
        Parameter(name='H', description='Standing height', units='cm', symbol='H', physiological_range=(100, 250)),
        Parameter(name='A', description='Age', units='years', symbol='A', physiological_range=(18, 100)),
        Parameter(name='sex', description='Sex flag selecting the coefficient set: 1.0 = male, 0.0 = female (threshold 0.5)', units='dimensionless', symbol='sex', default_value=1, physiological_range=(0, 1)),
    ],
    depends_on=[],
    produces='REE',
    metadata=EquationMetadata(source_unit=8, source_chapter='8.6',
                              source_section='EMPIRICAL FORMULAS FOR BMR', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(mifflin_st_jeor_ree)

__all__ = ['energy_expenditure_indirect_calorimetry', 'carbohydrate_oxidation_indirect_calorimetry', 'protein_oxidation_urinary_nitrogen', 'fat_oxidation_indirect_calorimetry', 'harris_benedict_bmr', 'mifflin_st_jeor_ree']

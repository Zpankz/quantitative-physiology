"""Acid-base balance equations."""

"""Acute Respiratory pH Change equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
from scripts.units import hb_to_mM


def compute_acute_respiratory_ph_change(delta_PCO2: float) -> float:
    """
    Calculate pH change in acute respiratory disorder.

    ΔpH = -0.008 × ΔP_CO2

    Parameters
    ----------
    delta_PCO2 : float
        Change in PCO2 from normal (mmHg)

    Returns
    -------
    float
        Change in pH
    """
    return -0.008 * delta_PCO2


# Create equation
acute_respiratory_ph_change = create_equation(
    id="acute_respiratory_ph_change",
    output_units='dimensionless',
    name="Acute Respiratory pH Change",
    category=EquationCategory.RESPIRATORY,
    latex=r"\Delta pH = -0.008 \times \Delta P_{CO2}",
    simplified="ΔpH = -0.008 × ΔP_CO2",
    description="Expected pH change per mmHg PCO2 change in acute respiratory disorders",
    compute_func=compute_acute_respiratory_ph_change,
    parameters=[
        Parameter(
            name="delta_PCO2",
            description="Change in PCO2 from normal",
            units="mmHg",
            symbol=r"\Delta P_{CO2}",
            physiological_range=(-40.0, 40.0)
        )
    ],
    depends_on=[],  # removed inert HH edge (HH produces=None; nothing consumed)
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(acute_respiratory_ph_change)

"""Anion Gap equation."""


def compute_anion_gap(Na: float, Cl: float, HCO3: float) -> float:
    """
    Calculate anion gap.

    AG = [Na⁺] - [Cl⁻] - [HCO3⁻]

    Parameters
    ----------
    Na : float
        Sodium concentration (mEq/L)
    Cl : float
        Chloride concentration (mEq/L)
    HCO3 : float
        Bicarbonate concentration (mEq/L)

    Returns
    -------
    float
        Anion gap (mEq/L)
    """
    return Na - Cl - HCO3


# Create equation
anion_gap = create_equation(
    id="anion_gap",
    output_units='mEq/L',
    name="Anion Gap",
    category=EquationCategory.RESPIRATORY,
    latex=r"AG = [Na^+] - [Cl^-] - [HCO_3^-]",
    simplified="AG = [Na⁺] - [Cl⁻] - [HCO3⁻]",
    description="Difference between measured cations and anions (normal: 8-12 mEq/L)",
    compute_func=compute_anion_gap,
    parameters=[
        Parameter(
            name="Na",
            description="Sodium concentration",
            units="mEq/L",
            symbol="[Na^+]",
            default_value=140.0,
            physiological_range=(135.0, 145.0)
        ),
        Parameter(
            name="Cl",
            description="Chloride concentration",
            units="mEq/L",
            symbol="[Cl^-]",
            default_value=104.0,
            physiological_range=(98.0, 108.0)
        ),
        Parameter(
            name="HCO3",
            description="Bicarbonate concentration",
            units="mEq/L",
            symbol="[HCO_3^-]",
            default_value=24.0,
            physiological_range=(22.0, 26.0)
        )
    ],
    produces="AG",
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(anion_gap)

"""Chronic Respiratory Acidosis HCO3 Change equation."""


def compute_chronic_respiratory_acidosis_hco3(delta_PCO2: float) -> float:
    """
    Calculate HCO3 change in chronic respiratory acidosis.

    Δ[HCO3⁻] = 3.5 × ΔP_CO2 / 10

    Parameters
    ----------
    delta_PCO2 : float
        Change in PCO2 from normal (mmHg)

    Returns
    -------
    float
        Change in bicarbonate (mEq/L)
    """
    return 3.5 * delta_PCO2 / 10.0


# Create equation
chronic_respiratory_acidosis_hco3 = create_equation(
    id="chronic_respiratory_acidosis_hco3",
    output_units='mEq/L',
    name="Chronic Respiratory Acidosis HCO3 Change",
    category=EquationCategory.RESPIRATORY,
    latex=r"\Delta[HCO_3^-] = 3.5 \times \frac{\Delta P_{CO2}}{10}",
    simplified="Δ[HCO3⁻] = 3.5 × ΔP_CO2 / 10",
    description="Renal compensation: HCO3 rises 3.5 mEq/L per 10 mmHg ↑PCO2",
    compute_func=compute_chronic_respiratory_acidosis_hco3,
    parameters=[
        Parameter(
            name="delta_PCO2",
            description="Change in PCO2 from normal",
            units="mmHg",
            symbol=r"\Delta P_{CO2}",
            physiological_range=(0.0, 40.0)
        )
    ],
    depends_on=[],  # removed inert HH edge (HH produces=None; nothing consumed)
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(chronic_respiratory_acidosis_hco3)

"""Chronic Respiratory Alkalosis HCO3 Change equation."""


def compute_chronic_respiratory_alkalosis_hco3(delta_PCO2: float) -> float:
    """
    Calculate HCO3 change in chronic respiratory alkalosis.

    Δ[HCO3⁻] = 5 × ΔP_CO2 / 10  (HCO3 falls as PCO2 falls)

    Parameters
    ----------
    delta_PCO2 : float
        Change in PCO2 from normal (negative for alkalosis) (mmHg)

    Returns
    -------
    float
        Change in bicarbonate (mEq/L)
    """
    return 5.0 * delta_PCO2 / 10.0


# Create equation
chronic_respiratory_alkalosis_hco3 = create_equation(
    id="chronic_respiratory_alkalosis_hco3",
    output_units='mEq/L',
    name="Chronic Respiratory Alkalosis HCO3 Change",
    category=EquationCategory.RESPIRATORY,
    latex=r"\Delta[HCO_3^-] = -5 \times \frac{\Delta P_{CO2}}{10}",
    simplified="Δ[HCO3⁻] = -5 × ΔP_CO2 / 10",
    description="Renal compensation: HCO3 falls 5 mEq/L per 10 mmHg ↓PCO2",
    compute_func=compute_chronic_respiratory_alkalosis_hco3,
    parameters=[
        Parameter(
            name="delta_PCO2",
            description="Change in PCO2 from normal",
            units="mmHg",
            symbol=r"\Delta P_{CO2}",
            physiological_range=(-40.0, 0.0)
        )
    ],
    depends_on=[],  # removed inert HH edge (HH produces=None; nothing consumed)
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(chronic_respiratory_alkalosis_hco3)

"""Henderson-Hasselbalch Equation."""

import math


def compute_henderson_hasselbalch(HCO3: float, PCO2: float, pKa: float, alpha: float) -> float:
    """
    Calculate pH using Henderson-Hasselbalch equation.

    pH = pKa + log([HCO3⁻]/(α × P_CO2))

    Parameters
    ----------
    HCO3 : float
        Bicarbonate concentration (mEq/L)
    PCO2 : float
        Partial pressure of CO2 (mmHg)
    pKa : float
        pKa of carbonic acid
    alpha : float
        CO2 solubility coefficient (mEq/L/mmHg)

    Returns
    -------
    float
        pH
    """
    return pKa + math.log10(HCO3 / (alpha * PCO2))


# Create equation
henderson_hasselbalch = create_equation(
    id="henderson_hasselbalch",
    output_units='dimensionless',
    name="Henderson-Hasselbalch Equation",
    category=EquationCategory.RESPIRATORY,
    latex=r"pH = pKa + \log\left(\frac{[HCO_3^-]}{\alpha \times P_{CO2}}\right)",
    simplified="pH = pKa + log([HCO3⁻]/(α × P_CO2))",
    description="Relationship between pH, bicarbonate, and PCO2 in blood",
    compute_func=compute_henderson_hasselbalch,
    parameters=[
        Parameter(
            name="HCO3",
            description="Bicarbonate concentration",
            units="mEq/L",
            symbol="[HCO_3^-]",
            default_value=24.0,
            physiological_range=(10.0, 40.0)
        ),
        Parameter(
            name="PCO2",
            description="Partial pressure of CO2",
            units="mmHg",
            symbol="P_{CO2}",
            default_value=40.0,
            physiological_range=(20.0, 80.0)
        ),
        Parameter(
            name="pKa",
            description="pKa of carbonic acid",
            units="dimensionless",
            symbol="pKa",
            default_value=6.1,
            physiological_range=(6.1, 6.1)
        ),
        Parameter(
            name="alpha",
            description="CO2 solubility",
            units="mEq/L/mmHg",
            symbol=r"\alpha",
            default_value=0.03,
            physiological_range=(0.03, 0.03)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(henderson_hasselbalch)

"""Metabolic Alkalosis Compensation equation."""


def compute_metabolic_alkalosis_compensation(HCO3: float) -> float:
    """
    Calculate expected PCO2 in metabolic alkalosis.

    P_CO2 = 0.7 × [HCO3⁻] + 21

    Parameters
    ----------
    HCO3 : float
        Bicarbonate concentration (mEq/L)

    Returns
    -------
    float
        Expected PCO2 (mmHg)
    """
    return 0.7 * HCO3 + 21.0


# Create equation
metabolic_alkalosis_compensation = create_equation(
    id="metabolic_alkalosis_compensation",
    output_units='mmHg',
    name="Metabolic Alkalosis Compensation",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{CO2} = 0.7 \times [HCO_3^-] + 21",
    simplified="P_CO2 = 0.7 × [HCO3⁻] + 21",
    description="Expected respiratory compensation for metabolic alkalosis",
    compute_func=compute_metabolic_alkalosis_compensation,
    parameters=[
        Parameter(
            name="HCO3",
            description="Bicarbonate concentration",
            units="mEq/L",
            symbol="[HCO_3^-]",
            physiological_range=(10.0, 50.0)
        )
    ],
    depends_on=[],  # removed inert HH edge (HH produces=None; nothing consumed)
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(metabolic_alkalosis_compensation)

"""Winter's Formula equation."""


def compute_winters_formula(HCO3: float) -> float:
    """
    Calculate expected PCO2 in metabolic acidosis.

    P_CO2 = 1.5 × [HCO3⁻] + 8 (± 2)

    Parameters
    ----------
    HCO3 : float
        Bicarbonate concentration (mEq/L)

    Returns
    -------
    float
        Expected PCO2 (mmHg)
    """
    return 1.5 * HCO3 + 8.0


# Create equation
winters_formula = create_equation(
    id="winters_formula",
    output_units='mmHg',
    name="Winter's Formula",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{CO2} = 1.5 \times [HCO_3^-] + 8",
    simplified="P_CO2 = 1.5 × [HCO3⁻] + 8",
    description="Expected respiratory compensation for metabolic acidosis",
    compute_func=compute_winters_formula,
    parameters=[
        Parameter(
            name="HCO3",
            description="Bicarbonate concentration",
            units="mEq/L",
            symbol="[HCO_3^-]",
            physiological_range=(5.0, 40.0)
        )
    ],
    depends_on=[],  # removed inert HH edge (HH produces=None; nothing consumed)
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.8"
    )
)

# Register in global index
register_equation(winters_formula)

__all__ = ['henderson_hasselbalch', 'anion_gap', 'winters_formula', 'metabolic_alkalosis_compensation', 'acute_respiratory_ph_change', 'chronic_respiratory_acidosis_hco3', 'chronic_respiratory_alkalosis_hco3']


# --- coverage pass additions (Feher extraction) ---

def compute_base_excess_van_slyke(HCO3, Hb, pH, Hb_units="mM"):
    """Siggaard-Andersen 'Van Slyke' base excess (Feher 6.5, 'The Concept of Base Excess or Base Deficit'). HCO3 and Hb in mM (Feher: all concentrations in mM; ctHb ~9.3 mM at normal), pH dimensionless; returns BE in mM (= mEq/L)."""
    Hb = hb_to_mM(Hb, Hb_units)
    return (HCO3 - 24.4 + (2.3 * Hb + 7.7) * (pH - 7.4)) * (1 - 0.023 * Hb)

base_excess_van_slyke = create_equation(
    id='base_excess_van_slyke',
    output_units='mM',
    name='Base Excess (Van Slyke Equation)',
    category=EquationCategory.RESPIRATORY,
    latex='\\mathrm{BE} = \\left([\\mathrm{HCO_3^-}] - 24.4 + (2.3\\,[\\mathrm{Hb}] + 7.7)(\\mathrm{pH} - 7.4)\\right)\\left(1 - 0.023\\,[\\mathrm{Hb}]\\right)',
    simplified='BE = (HCO3 - 24.4 + (2.3*Hb + 7.7)*(pH - 7.4)) * (1 - 0.023*Hb)',
    description="Siggaard-Andersen 'Van Slyke' equation for in-vitro base excess: the amount of strong acid (HCl) needed to titrate a blood sample to pH 7.4 at PCO2 40 mmHg and 37C (negative value = base deficit, the amount of strong base needed). Quantifies the metabolic (non-respiratory) component of an acid-base disturbance; positive BE indicates metabolic alkalosis, negative BE (base deficit) indicates metabolic acidosis. Valid for blood in vitro; the SBE variant extends it to extracellular fluid. Concentrations in mM per Feher.",
    compute_func=compute_base_excess_van_slyke,
    parameters=[
        Parameter(name='HCO3', description='Plasma bicarbonate concentration', units='mM', symbol='[HCO_3^-]', default_value=24, physiological_range=(5, 45)),
        Parameter(name='Hb', description='Hemoglobin concentration (Feher specifies mM; ctHb ~9.3 mM equals ~15 g/dL)', units='mM', symbol='[Hb]', default_value=9, physiological_range=(0, 14)),
        Parameter(name='pH', description='Arterial blood pH', units='dimensionless', symbol='pH', default_value=7.4, physiological_range=(6.8, 7.8)),
    ],
    depends_on=[],
    produces='BE',
    metadata=EquationMetadata(source_unit=6, source_chapter='6.5',
                              source_section='THE CONCEPT OF BASE EXCESS OR BASE DEFICIT', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(base_excess_van_slyke)


def compute_strong_ion_difference_apparent(Na, K, Ca, Mg, Cl, lactate):
    """Apparent strong ion difference (Stewart approach), Feher 6.5 'The Strong Ion Difference'.

    SIDa = [Na+] + [K+] + 2[Ca2+] + 2[Mg2+] - [Cl-] - [lactate]
    Divalent Ca2+ and Mg2+ carry a coefficient of 2 to convert mmol/L to mEq/L.
    Inputs are strong-ion concentrations in mmol/L (mM); output is in mEq/L.
    Normal plasma SIDa is about 42 mEq/L.
    """
    return Na + K + 2.0 * Ca + 2.0 * Mg - Cl - lactate

strong_ion_difference_apparent = create_equation(
    id='strong_ion_difference_apparent',
    output_units='mEq/L',
    name='Apparent Strong Ion Difference (SIDa)',
    category=EquationCategory.RESPIRATORY,
    latex='[\\mathrm{SID}]_a = [\\mathrm{Na^+}] + [\\mathrm{K^+}] + 2[\\mathrm{Ca^{2+}}] + 2[\\mathrm{Mg^{2+}}] - [\\mathrm{Cl^-}] - [\\mathrm{lactate}]',
    simplified='SIDa = [Na+] + [K+] + 2[Ca2+] + 2[Mg2+] - [Cl-] - [lactate]',
    description='Apparent strong ion difference from the Stewart quantitative acid-base approach: the sum of measured strong cation charges minus strong anion charges. Strong ions fully dissociate at physiological pH and do not participate in H+ exchange. Divalent Ca2+ and Mg2+ carry a coefficient of 2 (mmol/L to mEq/L). Normal plasma SIDa is about 42 mEq/L; a smaller value indicates acidosis and a larger value alkalosis. Used in ICU acid-base analysis and paired with the effective SID to compute the strong ion gap (unmeasured ions). Distinct from the traditional anion gap.',
    compute_func=compute_strong_ion_difference_apparent,
    parameters=[
        Parameter(name='Na', description='Plasma sodium concentration (strong cation)', units='mmol/L', symbol='[Na^+]', default_value=140, physiological_range=(120, 160)),
        Parameter(name='K', description='Plasma potassium concentration (strong cation)', units='mmol/L', symbol='[K^+]', default_value=4.5, physiological_range=(2.5, 7)),
        Parameter(name='Ca', description='Plasma ionized calcium concentration (strong divalent cation; multiplied by 2 for charge)', units='mmol/L', symbol='[Ca^{2+}]', default_value=1.2, physiological_range=(0.8, 1.6)),
        Parameter(name='Mg', description='Plasma ionized magnesium concentration (strong divalent cation; multiplied by 2 for charge)', units='mmol/L', symbol='[Mg^{2+}]', default_value=0.8, physiological_range=(0.4, 1.5)),
        Parameter(name='Cl', description='Plasma chloride concentration (strong anion)', units='mmol/L', symbol='[Cl^-]', default_value=105, physiological_range=(90, 120)),
        Parameter(name='lactate', description='Plasma lactate concentration (strong anion)', units='mmol/L', symbol='[lactate]', default_value=1, physiological_range=(0, 20)),
    ],
    depends_on=[],
    produces='SIDa',
    metadata=EquationMetadata(source_unit=6, source_chapter='6.5',
                              source_section='THE STRONG ION DIFFERENCE', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(strong_ion_difference_apparent)


def compute_standard_base_excess(HCO3, pH):
    """Standard base excess (SBE), Siggaard-Andersen whole-body modification of the Van Slyke equation.

    SBE = [HCO3-] - 24.8 + 16.2 * (pH - 7.40)

    Feher 6.5, 'The concept of base excess or base deficit'. Quantifies the
    metabolic component of an acid-base disturbance (mmol/L of strong acid/base
    needed to titrate extracellular fluid to pH 7.40 at PCO2 40 mmHg, 37 C).
    Units: HCO3 in mM (mmol/L), pH dimensionless; returns SBE in mM (mmol/L).
    Positive = base excess (metabolic alkalosis), negative = base deficit
    (metabolic acidosis).
    """
    return HCO3 - 24.8 + 16.2 * (pH - 7.40)

standard_base_excess = create_equation(
    id='standard_base_excess',
    output_units='mM',
    name='Standard Base Excess',
    category=EquationCategory.RESPIRATORY,
    latex='\\mathrm{SBE} = [\\mathrm{HCO_3^-}] - 24.8 + 16.2\\,(\\mathrm{pH} - 7.40)',
    simplified='SBE = [HCO3-] - 24.8 + 16.2 * (pH - 7.40)',
    description="Standard base excess: the Siggaard-Andersen whole-body (in vivo, extracellular-buffer) modification of the Van Slyke base-excess equation. Gives a quantitative measure of the metabolic component of an acid-base disturbance, defined as the mmol/L of strong acid or base needed to titrate extracellular fluid to pH 7.40 at PCO2 40 mmHg and 37 C. Positive values indicate a base excess (metabolic alkalosis); negative values indicate a base deficit (metabolic acidosis). It is the 'base excess' reported by arterial blood gas analyzers; unlike the in-vitro Van Slyke BE it drops the hemoglobin term. The HCO3 input is calculated from pH and PCO2 via the Henderson-Hasselbalch equation.",
    compute_func=compute_standard_base_excess,
    parameters=[
        Parameter(name='HCO3', description='Bicarbonate concentration (calculated from pH and PCO2 via Henderson-Hasselbalch, not measured)', units='mM', symbol='[HCO_3^-]', default_value=24.8, physiological_range=(5, 45)),
        Parameter(name='pH', description='Arterial blood pH', units='dimensionless', symbol='pH', default_value=7.4, physiological_range=(6.8, 7.8)),
    ],
    depends_on=[],  # removed inert HH edge (HH produces=None; nothing consumed)
    metadata=EquationMetadata(source_unit=6, source_chapter='6.5',
                              source_section='THE CONCEPT OF BASE EXCESS OR BASE DEFICIT', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(standard_base_excess)


def compute_weak_acid_anion_charge(pH, albumin, phosphate):
    """Weak-acid (protein + phosphate) anion charge [A-] in mEq/L, from Feher 6.5
    'The Strong Ion Difference' (Stewart approach). Empirical Figge-Fencl estimate.
    pH dimensionless; albumin [Alb] in g/L; phosphate [Pi] total in mM; output mEq/L.
    [A-] = (0.123*pH - 0.631)*[Alb] + (0.309*pH - 0.469)*[Pi]."""
    return (0.123 * pH - 0.631) * albumin + (0.309 * pH - 0.469) * phosphate

weak_acid_anion_charge = create_equation(
    id='weak_acid_anion_charge',
    produces='A_minus',
    output_units='mEq/L',
    name='Weak-Acid Anion Charge (Figge-Fencl)',
    category=EquationCategory.RESPIRATORY,
    latex='[\\mathrm{A^-}] = (0.123\\,\\mathrm{pH} - 0.631)[\\mathrm{Alb}] + (0.309\\,\\mathrm{pH} - 0.469)[\\mathrm{Pi}]',
    simplified='[A-] = (0.123*pH - 0.631)*[Alb] + (0.309*pH - 0.469)*[Pi]',
    description='Figge-Fencl empirical estimate of the non-volatile weak-acid buffer charge (plasma protein + phosphate) as a function of pH. In the Stewart strong-ion approach it gives [A-] (mEq/L), the charge on plasma proteins and phosphate, which feeds the effective strong ion difference (SIDe = [HCO3-] + [A-]) and hence the strong ion gap (SIG = SIDa - SIDe). Inputs: albumin in g/L, total phosphate in mM.',
    compute_func=compute_weak_acid_anion_charge,
    parameters=[
        Parameter(name='pH', description='Plasma pH', units='dimensionless', symbol='pH', default_value=7.4, physiological_range=(6.8, 7.8)),
        Parameter(name='albumin', description='Plasma albumin concentration', units='g/L', symbol='[Alb]', default_value=44, physiological_range=(10, 60)),
        Parameter(name='phosphate', description='Total plasma phosphate concentration', units='mM', symbol='[Pi]', default_value=1.16, physiological_range=(0.3, 5)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=6, source_chapter='6.5',
                              source_section='THE STRONG ION DIFFERENCE', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(weak_acid_anion_charge)


def compute_strong_ion_difference_effective(HCO3, A_minus):
    """Effective strong ion difference SIDe = [HCO3-] + [A-] in mEq/L (Feher 6.5, 'The Strong Ion Difference'). HCO3 = plasma bicarbonate (mEq/L); A_minus = net negative charge on plasma weak acids (albumin + phosphate) (mEq/L)."""
    return HCO3 + A_minus

strong_ion_difference_effective = create_equation(
    id='strong_ion_difference_effective',
    output_units='mEq/L',
    name='Effective Strong Ion Difference',
    category=EquationCategory.RESPIRATORY,
    latex='[\\mathrm{SID}]_e = [\\mathrm{HCO_3^-}] + [\\mathrm{A^-}]',
    simplified='SIDe = [HCO3-] + [A-]',
    description='Effective strong ion difference in the Stewart approach to acid-base analysis: the sum of plasma bicarbonate and the net negative charge carried by plasma weak acids (albumin and phosphate). It is compared with the apparent SID to yield the strong ion gap (SIG = SIDa - SIDe), which quantifies unmeasured ions in acid-base disturbances. Normal SIDe is roughly 38-40 mEq/L.',
    compute_func=compute_strong_ion_difference_effective,
    parameters=[
        Parameter(name='HCO3', description='Plasma bicarbonate concentration', units='mEq/L', symbol='[HCO_3^-]', default_value=24, physiological_range=(10, 40)),
        Parameter(name='A_minus', description='Net negative charge on plasma weak acids (albumin + phosphate)', units='mEq/L', symbol='[A^-]', default_value=14, physiological_range=(0, 30)),
    ],
    depends_on=["weak_acid_anion_charge"],
    produces='SIDe',
    metadata=EquationMetadata(source_unit=6, source_chapter='6.5',
                              source_section='THE STRONG ION DIFFERENCE', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(strong_ion_difference_effective)


def compute_strong_ion_gap(SIDa, SIDe):
    """Strong ion gap (Stewart approach), Feher 6.5 'THE STRONG ION DIFFERENCE': SIG = SID_a - SID_e. Both inputs and the result are in mEq/L; SIG is the concentration of unmeasured strong ions."""
    return SIDa - SIDe

strong_ion_gap = create_equation(
    id='strong_ion_gap',
    output_units='mEq/L',
    name='Strong Ion Gap',
    category=EquationCategory.RESPIRATORY,
    latex='\\mathrm{SIG} = \\mathrm{SID}_a - \\mathrm{SID}_e',
    simplified='SIG = SID_a - SID_e',
    description='Strong ion gap (Stewart quantitative acid-base): the difference between the apparent and effective strong ion difference. Quantifies the concentration of unmeasured strong ions; normal ~0-2 mEq/L. An elevated SIG signals unmeasured anions (e.g. ketoacids, other organic acids) in metabolic acidosis and helps localise their origin. Distinct from the anion gap because the weak-acid charge (albumin, phosphate) is explicitly netted out through SID_e, so a normal SIG is ~0 rather than the 8-12 mEq/L of the anion gap. INTEGRATOR NOTE: if the sibling candidates strong_ion_difference_apparent and strong_ion_difference_effective are also kept, rewire depends_on=["strong_ion_difference_apparent", "strong_ion_difference_effective"] and rely on produces-chaining instead of the raw SIDa/SIDe inputs; kept self-contained here because this candidate was verified independently.',
    compute_func=compute_strong_ion_gap,
    parameters=[
        Parameter(name='SIDa', description='Apparent strong ion difference = [Na+] + [K+] + 2[Ca2+] + 2[Mg2+] - [Cl-] - [lactate]; normal plasma ~42 mEq/L', units='mEq/L', symbol='[SID]_a', default_value=42, physiological_range=(20, 60)),
        Parameter(name='SIDe', description='Effective strong ion difference = [HCO3-] + [A-], where [A-] is the net charge on albumin and phosphate; normal plasma ~40 mEq/L', units='mEq/L', symbol='[SID]_e', default_value=40, physiological_range=(20, 60)),
    ],
    depends_on=["strong_ion_difference_apparent", "strong_ion_difference_effective"],  # SIG = SIDa - SIDe (per INTEGRATOR NOTE above)
    metadata=EquationMetadata(source_unit=6, source_chapter='6.5',
                              source_section='THE STRONG ION DIFFERENCE', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(strong_ion_gap)

try:
    __all__ += ['base_excess_van_slyke', 'strong_ion_difference_apparent', 'standard_base_excess', 'weak_acid_anion_charge', 'strong_ion_difference_effective', 'strong_ion_gap']
except NameError:
    __all__ = ['base_excess_van_slyke', 'strong_ion_difference_apparent', 'standard_base_excess', 'weak_acid_anion_charge', 'strong_ion_difference_effective', 'strong_ion_gap']


# --- review-add 2026-07-15 ---
def compute_kassirer_bleich_hydrogen_ion(PCO2: float, HCO3: float) -> float:
    """[H+] (nmol/L) = 24 * PCO2 / HCO3 (Kassirer-Bleich, log-free)."""
    return 24.0 * PCO2 / HCO3

kassirer_bleich_hydrogen_ion_equation = create_equation(
    id='kassirer_bleich_hydrogen_ion',
    name='Kassirer-Bleich Hydrogen Ion',
    category=EquationCategory.RESPIRATORY,
    latex=r'[H^+] = \\frac{24 \\cdot PCO_2}{[HCO_3^-]}',
    simplified='H_plus = 24 * PCO2 / HCO3',
    description='Kassirer-Bleich log-free estimate of [H+] in nmol/L from PCO2 and bicarbonate; a bedside acid-base workhorse (40 nmol/L = pH 7.40).',
    compute_func=compute_kassirer_bleich_hydrogen_ion,
    output_units='nmol/L',
    parameters=[
        Parameter(name='PCO2', description='Arterial CO2 tension', units='mmHg', symbol='PCO2', physiological_range=(10, 120)),
        Parameter(name='HCO3', description='Bicarbonate', units='mmol/L', symbol='HCO3', physiological_range=(4, 45)),
    ],
    metadata=EquationMetadata(source_unit=6, source_chapter='6.7'),
)
register_equation(kassirer_bleich_hydrogen_ion_equation)


# --- adversarial-review-add 2026-07-15 ---
def compute_acute_respiratory_acidosis_hco3(PCO2: float) -> float:
    """Expected [HCO3-] in ACUTE respiratory acidosis: 24 + 1.0*(PCO2-40)/10
    (+1 mEq/L per +10 mmHg PaCO2)."""
    return 24.0 + 1.0 * (PCO2 - 40.0) / 10.0

acute_respiratory_acidosis_hco3_equation = create_equation(
    id="acute_respiratory_acidosis_hco3",
    name="Acute Respiratory Acidosis Expected HCO3",
    category=EquationCategory.RESPIRATORY,
    latex=r"[HCO_3^-] = 24 + 1.0\,\frac{PCO_2 - 40}{10}",
    simplified="HCO3 = 24 + 1.0*(PCO2-40)/10",
    description="Expected bicarbonate in acute respiratory acidosis (+1 mEq/L per "
                "+10 mmHg PaCO2); deviation flags a superimposed metabolic disorder.",
    compute_func=compute_acute_respiratory_acidosis_hco3,
    output_units="mEq/L",
    parameters=[
        Parameter(name="PCO2", description="Arterial CO2 tension", units="mmHg", symbol="PCO2", physiological_range=(40, 120)),
    ],
    metadata=EquationMetadata(source_unit=6, source_chapter="6.7"),
)
register_equation(acute_respiratory_acidosis_hco3_equation)


# --- adversarial-review-add 2026-07-15 ---
def compute_acute_respiratory_alkalosis_hco3(PCO2: float) -> float:
    """Expected [HCO3-] in ACUTE respiratory alkalosis: 24 - 2.0*(40-PCO2)/10
    (-2 mEq/L per -10 mmHg PaCO2)."""
    return 24.0 - 2.0 * (40.0 - PCO2) / 10.0

acute_respiratory_alkalosis_hco3_equation = create_equation(
    id="acute_respiratory_alkalosis_hco3",
    name="Acute Respiratory Alkalosis Expected HCO3",
    category=EquationCategory.RESPIRATORY,
    latex=r"[HCO_3^-] = 24 - 2.0\,\frac{40 - PCO_2}{10}",
    simplified="HCO3 = 24 - 2.0*(40-PCO2)/10",
    description="Expected bicarbonate in acute respiratory alkalosis (-2 mEq/L per "
                "-10 mmHg PaCO2); deviation flags a superimposed metabolic disorder.",
    compute_func=compute_acute_respiratory_alkalosis_hco3,
    output_units="mEq/L",
    parameters=[
        Parameter(name="PCO2", description="Arterial CO2 tension", units="mmHg", symbol="PCO2", physiological_range=(10, 40)),
    ],
    metadata=EquationMetadata(source_unit=6, source_chapter="6.7"),
)
register_equation(acute_respiratory_alkalosis_hco3_equation)

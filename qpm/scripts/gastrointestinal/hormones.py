"""Consolidated module for gastrointestinal.hormones."""

"""CCK release in response to fat and amino acids."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_cck_response(fat_g: float, aa_g: float, EC50_fat: float = 5.0, EC50_aa: float = 10.0) -> float:
    """
    Calculate CCK release based on fat and amino acid content.

    CCK released by I cells (duodenum) stimulates:
    - Enzyme secretion (pancreas)
    - Gallbladder contraction
    - Satiety

    Parameters
    ----------
    fat_g : float
        Fat content in duodenum (g)
    aa_g : float
        Amino acid content in duodenum (g)
    EC50_fat : float
        Half-maximal fat concentration (g), default 5.0
    EC50_aa : float
        Half-maximal amino acid concentration (g), default 10.0

    Returns
    -------
    float
        CCK response signal (dimensionless, 0-2 range)
    """
    fat_signal = fat_g / (EC50_fat + fat_g)
    aa_signal = aa_g / (EC50_aa + aa_g)
    return fat_signal + aa_signal


cck_response = create_equation(
    id="cck_response",
    output_units='dimensionless',
    name="CCK Response to Fat and Amino Acids",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{CCK} = \frac{[\text{Fat}]}{EC_{50,\text{fat}} + [\text{Fat}]} + \frac{[\text{AA}]}{EC_{50,\text{AA}} + [\text{AA}]}",
    simplified="CCK = [Fat]/(EC50_fat + [Fat]) + [AA]/(EC50_AA + [AA])",
    description="CCK release by I cells in response to fat and amino acids. Stimulates enzyme secretion, gallbladder contraction, satiety",
    compute_func=compute_cck_response,
    parameters=[
        Parameter(
            name="fat_g",
            description="Fat content in duodenum",
            units="g",
            symbol=r"[\text{Fat}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="aa_g",
            description="Amino acid content in duodenum",
            units="g",
            symbol=r"[\text{AA}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="EC50_fat",
            description="Half-maximal fat concentration",
            units="g",
            symbol=r"EC_{50,\text{fat}}",
            default_value=5.0,
            physiological_range=(3.0, 7.0)
        ),
        Parameter(
            name="EC50_aa",
            description="Half-maximal amino acid concentration",
            units="g",
            symbol=r"EC_{50,\text{AA}}",
            default_value=10.0,
            physiological_range=(8.0, 12.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(cck_response)

"""CCK satiety effect."""

import numpy as np


def compute_cck_satiety(CCK_pM: float, k: float = 1.0) -> float:
    """
    Calculate food intake inhibition by CCK.

    CCK satiety effect is proportional to log([CCK]).
    Half-life ~2-3 min (rapid peptidase degradation).

    Parameters
    ----------
    CCK_pM : float
        CCK concentration (pM)
    k : float
        Satiety coefficient, default 1.0

    Returns
    -------
    float
        Satiety signal (log scale)
    """
    if CCK_pM <= 0:
        return 0.0
    return k * np.log(CCK_pM)


cck_satiety = create_equation(
    id="cck_satiety",
    output_units='dimensionless',
    name="CCK Satiety Effect",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Satiety} = k \times \ln([\text{CCK}])",
    simplified="Satiety = k × ln([CCK])",
    description="CCK-induced satiety (food intake inhibition) proportional to log([CCK]). Half-life ~2-3 min",
    compute_func=compute_cck_satiety,
    parameters=[
        Parameter(
            name="CCK_pM",
            description="CCK concentration",
            units="pM",
            symbol=r"[\text{CCK}]",
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="k",
            description="Satiety coefficient",
            units="dimensionless",
            symbol="k",
            default_value=1.0,
            physiological_range=(0.5, 2.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(cck_satiety)

"""Gastrin-stimulated acid secretion."""


def compute_gastrin_acid_response(gastrin_pg_mL: float, Amax: float = 25.0, EC50: float = 40.0, n: float = 1.5) -> float:
    """
    Calculate acid secretion response to gastrin using Hill equation.

    Gastrin released by G cells (antrum) in response to peptides, distension, vagal stimulation.

    Parameters
    ----------
    gastrin_pg_mL : float
        Plasma gastrin concentration (pg/mL)
    Amax : float
        Maximum acid output (mEq/h), default 25
    EC50 : float
        Half-maximal gastrin concentration (pg/mL), default 40
    n : float
        Hill coefficient, default 1.5

    Returns
    -------
    float
        Acid output (mEq/h)
    """
    return Amax * (gastrin_pg_mL ** n) / (EC50 ** n + gastrin_pg_mL ** n)


gastrin_acid_response = create_equation(
    id="gastrin_acid_response",
    output_units='mEq/h',
    name="Gastrin-Acid Secretion Response",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"AO = \frac{A_{\max} \times [\text{Gastrin}]^n}{EC_{50}^n + [\text{Gastrin}]^n}",
    simplified="AO = A_max × [Gastrin]^n / (EC50^n + [Gastrin]^n)",
    description="Gastrin dose-response for acid secretion. EC50 ≈ 30-50 pg/mL. Released by G cells in response to peptides, distension",
    compute_func=compute_gastrin_acid_response,
    parameters=[
        Parameter(
            name="gastrin_pg_mL",
            description="Plasma gastrin concentration",
            units="pg/mL",
            symbol=r"[\text{Gastrin}]",
            physiological_range=(10.0, 200.0)
        ),
        Parameter(
            name="Amax",
            description="Maximum acid output",
            units="mEq/h",
            symbol=r"A_{\max}",
            default_value=25.0,
            physiological_range=(20.0, 30.0)
        ),
        Parameter(
            name="EC50",
            description="Half-maximal gastrin concentration",
            units="pg/mL",
            symbol=r"EC_{50}",
            default_value=40.0,
            physiological_range=(30.0, 50.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=1.5,
            physiological_range=(1.0, 2.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(gastrin_acid_response)

"""GLP-1 potentiation of insulin secretion."""


def compute_glp1_insulin_response(GLP1_pM: float, glucose_mM: float, EC50_GLP1: float = 10.0, glucose_threshold: float = 5.0) -> float:
    """
    Calculate GLP-1 potentiation of insulin secretion.

    GLP-1 only effective above glucose threshold (~5 mM).
    Released by L cells (ileum) in response to nutrients.

    Parameters
    ----------
    GLP1_pM : float
        GLP-1 concentration (pM)
    glucose_mM : float
        Plasma glucose concentration (mM)
    EC50_GLP1 : float
        Half-maximal GLP-1 concentration (pM), default 10
    glucose_threshold : float
        Glucose threshold for GLP-1 effect (mM), default 5.0

    Returns
    -------
    float
        Insulin potentiation signal (0-1)
    """
    glucose_factor = max(0.0, (glucose_mM - glucose_threshold) / glucose_threshold)
    GLP1_effect = GLP1_pM / (EC50_GLP1 + GLP1_pM)
    return glucose_factor * GLP1_effect


glp1_insulin_response = create_equation(
    id="glp1_insulin_response",
    output_units='dimensionless',
    name="GLP-1 Insulin Potentiation",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Potentiation} = \frac{\max(0, \text{Glc} - 5)}{5} \times \frac{[\text{GLP-1}]}{EC_{50} + [\text{GLP-1}]}",
    simplified="Potentiation = max(0, Glc-5)/5 × [GLP-1]/(EC50 + [GLP-1])",
    description="GLP-1 potentiates insulin secretion only above glucose threshold (~5 mM). Released by L cells in ileum",
    compute_func=compute_glp1_insulin_response,
    parameters=[
        Parameter(
            name="GLP1_pM",
            description="GLP-1 concentration",
            units="pM",
            symbol=r"[\text{GLP-1}]",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="glucose_mM",
            description="Plasma glucose concentration",
            units="mM",
            symbol=r"\text{Glc}",
            physiological_range=(3.0, 15.0)
        ),
        Parameter(
            name="EC50_GLP1",
            description="Half-maximal GLP-1 concentration",
            units="pM",
            symbol=r"EC_{50}",
            default_value=10.0,
            physiological_range=(5.0, 15.0)
        ),
        Parameter(
            name="glucose_threshold",
            description="Glucose threshold for GLP-1 effect",
            units="mM",
            symbol=r"\text{Glc}_{\text{threshold}}",
            default_value=5.0,
            physiological_range=(4.0, 6.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(glp1_insulin_response)

"""Incretin effect on insulin secretion."""


def compute_incretin_effect(insulin_oral: float, insulin_iv: float) -> float:
    """
    Calculate incretin effect: ratio of insulin response to oral vs IV glucose.

    Oral glucose triggers 2-3× more insulin than IV glucose at same plasma glucose.
    Due to GIP (~60%) and GLP-1 (~40%).

    Parameters
    ----------
    insulin_oral : float
        Insulin response to oral glucose (pmol/L)
    insulin_iv : float
        Insulin response to IV glucose (pmol/L)

    Returns
    -------
    float
        Incretin effect ratio (normally 2-3)
    """
    if insulin_iv > 0:
        return insulin_oral / insulin_iv
    else:
        return float('inf')


incretin_effect = create_equation(
    id="incretin_effect",
    output_units='dimensionless',
    name="Incretin Effect",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Incretin ratio} = \frac{\text{Insulin}_{\text{oral}}}{\text{Insulin}_{\text{IV}}}",
    simplified="Incretin ratio = Insulin_oral / Insulin_IV",
    description="Incretin effect: oral glucose → 2-3× more insulin than IV glucose. Due to GIP (60%) + GLP-1 (40%)",
    compute_func=compute_incretin_effect,
    parameters=[
        Parameter(
            name="insulin_oral",
            description="Insulin response to oral glucose",
            units="pmol/L",
            symbol=r"\text{Insulin}_{\text{oral}}",
            physiological_range=(50.0, 500.0)
        ),
        Parameter(
            name="insulin_iv",
            description="Insulin response to IV glucose",
            units="pmol/L",
            symbol=r"\text{Insulin}_{\text{IV}}",
            physiological_range=(20.0, 200.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(incretin_effect)

"""Secretin-stimulated bicarbonate secretion."""


def compute_secretin_bicarbonate(pH_duodenum: float, threshold: float = 4.5, max_response: float = 140.0) -> float:
    """
    Calculate secretin release and bicarbonate secretion based on duodenal pH.

    Secretin released by S cells when duodenal pH < 4.5.

    Parameters
    ----------
    pH_duodenum : float
        Duodenal pH
    threshold : float
        pH threshold for secretin release, default 4.5
    max_response : float
        Maximum HCO3- response (mM), default 140

    Returns
    -------
    float
        HCO3- secretion response (mM)
    """
    if pH_duodenum > threshold:
        return 0.0
    else:
        return max_response * (threshold - pH_duodenum) / threshold


secretin_bicarbonate = create_equation(
    id="secretin_bicarbonate",
    output_units='mM',
    name="Secretin-Bicarbonate Secretion",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"[\text{HCO}_3^-] = \begin{cases} 0 & \text{pH} > 4.5 \\ 140 \times \frac{4.5 - \text{pH}}{4.5} & \text{pH} \leq 4.5 \end{cases}",
    simplified="[HCO3-] = 0 if pH > 4.5, else 140 × (4.5 - pH) / 4.5",
    description="Secretin release triggered by duodenal pH < 4.5. Stimulates pancreatic HCO3- secretion",
    compute_func=compute_secretin_bicarbonate,
    parameters=[
        Parameter(
            name="pH_duodenum",
            description="Duodenal pH",
            units="dimensionless",
            symbol=r"\text{pH}",
            physiological_range=(1.0, 7.0)
        ),
        Parameter(
            name="threshold",
            description="pH threshold for secretin release",
            units="dimensionless",
            symbol=r"\text{pH}_{\text{threshold}}",
            default_value=4.5,
            physiological_range=(4.0, 5.0)
        ),
        Parameter(
            name="max_response",
            description="Maximum HCO3- response",
            units="mM",
            symbol=r"[\text{HCO}_3^-]_{\max}",
            default_value=140.0,
            physiological_range=(120.0, 150.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.5"
    )
)

register_equation(secretin_bicarbonate)


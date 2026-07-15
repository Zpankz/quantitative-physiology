"""Consolidated module for gastrointestinal.secretion."""

"""Bile acid synthesis and pool dynamics."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_bile_acid_synthesis_rate(fecal_loss: float) -> float:
    """
    Calculate bile acid synthesis rate at steady state.

    At steady state: synthesis = fecal loss

    Parameters
    ----------
    fecal_loss : float
        Fecal bile acid loss (g/day)

    Returns
    -------
    float
        Bile acid synthesis rate (g/day)
    """
    return fecal_loss


bile_acid_synthesis = create_equation(
    id="bile_acid_synthesis",
    output_units='g/day',
    name="Bile Acid Synthesis Rate",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Synthesis} = \text{Fecal loss}",
    simplified="Synthesis = Fecal loss",
    description="At steady state, bile acid synthesis equals fecal loss (~0.3-0.6 g/day). Pool size ~2-4 g, cycles 6-10×/day",
    compute_func=compute_bile_acid_synthesis_rate,
    parameters=[
        Parameter(
            name="fecal_loss",
            description="Fecal bile acid loss",
            units="g/day",
            symbol=r"\text{Fecal loss}",
            default_value=0.45,
            physiological_range=(0.3, 0.6)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(bile_acid_synthesis)

"""Critical micellar concentration for bile salts."""


def compute_micelle_formation(bile_salt_conc: float, CMC: float = 3.0) -> bool:
    """
    Determine if micelle formation occurs based on bile salt concentration.

    Parameters
    ----------
    bile_salt_conc : float
        Bile salt concentration (mM)
    CMC : float
        Critical micellar concentration (mM), default 3 mM

    Returns
    -------
    bool
        True if micelles can form ([bile salt] > CMC)
    """
    return bile_salt_conc > CMC


critical_micellar_concentration = create_equation(
    id="critical_micellar_concentration",
    output_units='boolean',
    name="Critical Micellar Concentration",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Micelle formation: } [\text{bile salt}] > \text{CMC}",
    simplified="Micelle formation: [bile salt] > CMC",
    description="Micelle formation requires bile salt concentration above CMC (~2-5 mM for bile salts)",
    compute_func=compute_micelle_formation,
    parameters=[
        Parameter(
            name="bile_salt_conc",
            description="Bile salt concentration",
            units="mM",
            symbol=r"[\text{bile salt}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="CMC",
            description="Critical micellar concentration",
            units="mM",
            symbol=r"\text{CMC}",
            default_value=3.0,
            physiological_range=(2.0, 5.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(critical_micellar_concentration)

"""Gastric acid output equation."""


def compute_gastric_acid_output(stim_fraction: float, MAO: float = 25.0) -> float:
    """
    Calculate gastric acid output based on stimulation level.

    Parameters
    ----------
    stim_fraction : float
        Stimulation fraction (0 = basal, 1 = maximal)
    MAO : float
        Maximal acid output (mEq/h), default 25 mEq/h

    Returns
    -------
    float
        Acid output (mEq/h)
    """
    BAO = 0.15 * MAO  # Basal is ~15% of maximal
    return BAO + (MAO - BAO) * stim_fraction


gastric_acid_output = create_equation(
    id="gastric_acid_output",
    output_units='mEq/h',
    name="Gastric Acid Output",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{AO} = \text{BAO} + (\text{MAO} - \text{BAO}) \times f",
    simplified="AO = BAO + (MAO - BAO) × f",
    description="Gastric acid output as function of stimulation (BAO ~2-5 mEq/h, MAO ~20-25 mEq/h)",
    compute_func=compute_gastric_acid_output,
    parameters=[
        Parameter(
            name="stim_fraction",
            description="Stimulation fraction (0 = basal, 1 = maximal)",
            units="dimensionless",
            symbol="f",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="MAO",
            description="Maximal acid output",
            units="mEq/h",
            symbol=r"\text{MAO}",
            default_value=25.0,
            physiological_range=(20.0, 30.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(gastric_acid_output)

"""Pancreatic bicarbonate concentration equation."""

import numpy as np


def compute_pancreatic_bicarbonate(flow_rate: float, max_HCO3: float = 140.0, max_flow: float = 4.0) -> float:
    """
    Calculate pancreatic bicarbonate concentration as function of flow rate.

    Parameters
    ----------
    flow_rate : float
        Pancreatic flow rate (mL/min)
    max_HCO3 : float
        Maximum HCO3- concentration (mM), default 140 mM
    max_flow : float
        Flow rate at which max HCO3- approached (mL/min), default 4 mL/min

    Returns
    -------
    float
        HCO3- concentration (mM)
    """
    fraction = 1 - np.exp(-flow_rate / max_flow)
    return max_HCO3 * fraction + 20 * (1 - fraction)


pancreatic_bicarbonate = create_equation(
    id="pancreatic_bicarbonate",
    output_units='mM',
    name="Pancreatic Bicarbonate Concentration",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"[\text{HCO}_3^-] = 140 \times f + 20 \times (1-f), \quad f = 1 - e^{-Q/Q_{\text{max}}}",
    simplified="[HCO3-] = 140×f + 20×(1-f), f = 1 - e^(-Q/Q_max)",
    description="Pancreatic HCO3- concentration varies with flow: high flow→140 mM, low flow→20 mM. Sum [HCO3-]+[Cl-]≈160 mM constant",
    compute_func=compute_pancreatic_bicarbonate,
    parameters=[
        Parameter(
            name="flow_rate",
            description="Pancreatic flow rate",
            units="mL/min",
            symbol="Q",
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="max_HCO3",
            description="Maximum HCO3- concentration",
            units="mM",
            symbol=r"[\text{HCO}_3^-]_{\text{max}}",
            default_value=140.0,
            physiological_range=(120.0, 150.0)
        ),
        Parameter(
            name="max_flow",
            description="Flow rate approaching maximum HCO3-",
            units="mL/min",
            symbol=r"Q_{\text{max}}",
            default_value=4.0,
            physiological_range=(3.0, 5.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(pancreatic_bicarbonate)

"""Salivary flow rate equation."""


def compute_salivary_flow(stimulation: float, basal: float = 0.1, max_flow: float = 4.0) -> float:
    """
    Calculate salivary flow rate based on stimulation level.

    Parameters
    ----------
    stimulation : float
        Stimulation level (0-1 scale)
    basal : float
        Basal flow rate (mL/min), default 0.1 mL/min
    max_flow : float
        Maximum stimulated flow rate (mL/min), default 4 mL/min

    Returns
    -------
    float
        Salivary flow rate (mL/min)
    """
    return basal + (max_flow - basal) * stimulation


salivary_flow = create_equation(
    id="salivary_flow",
    output_units='mL/min',
    name="Salivary Flow Rate",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"Q_{\text{saliva}} = Q_{\text{basal}} + (Q_{\text{max}} - Q_{\text{basal}}) \times S",
    simplified="Q_saliva = Q_basal + (Q_max - Q_basal) × S",
    description="Salivary flow rate as function of stimulation (daily volume ~1-1.5 L/day)",
    compute_func=compute_salivary_flow,
    parameters=[
        Parameter(
            name="stimulation",
            description="Stimulation level",
            units="dimensionless",
            symbol="S",
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="basal",
            description="Basal flow rate",
            units="mL/min",
            symbol=r"Q_{\text{basal}}",
            default_value=0.1,
            physiological_range=(0.05, 0.2)
        ),
        Parameter(
            name="max_flow",
            description="Maximum stimulated flow rate",
            units="mL/min",
            symbol=r"Q_{\text{max}}",
            default_value=4.0,
            physiological_range=(3.0, 5.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.2"
    )
)

register_equation(salivary_flow)


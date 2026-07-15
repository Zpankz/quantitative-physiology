"""Consolidated module for gastrointestinal.digestion."""

"""Amylase kinetics for starch digestion."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_amylase_rate(starch_conc: float, J_max: float = 10.0, Km: float = 1.5) -> float:
    """
    Calculate amylase digestion rate for starch.

    Amylase (salivary + pancreatic) breaks starch into maltose, maltotriose, and α-limit dextrins.

    Parameters
    ----------
    starch_conc : float
        Starch concentration (mg/mL)
    J_max : float
        Maximum digestion rate, default 10 mg/(mL·min)
    Km : float
        Michaelis constant (mg/mL), default 1.5 mg/mL

    Returns
    -------
    float
        Digestion rate (mg/(mL·min))
    """
    return J_max * starch_conc / (Km + starch_conc)


amylase_kinetics = create_equation(
    id="amylase_kinetics",
    output_units='mg/(mL*min)',
    name="Amylase Kinetics",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J = \frac{J_{\max} \times [\text{Starch}]}{K_m + [\text{Starch}]}",
    simplified="J = J_max × [Starch] / (K_m + [Starch])",
    description="α-Amylase kinetics for starch digestion to maltose, maltotriose, and α-limit dextrins. K_m ≈ 1-2 mg/mL",
    compute_func=compute_amylase_rate,
    parameters=[
        Parameter(
            name="starch_conc",
            description="Starch concentration",
            units="mg/mL",
            symbol=r"[\text{Starch}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="J_max",
            description="Maximum digestion rate",
            units="mg/(mL·min)",
            symbol=r"J_{\max}",
            default_value=10.0,
            physiological_range=(5.0, 20.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mg/mL",
            symbol="K_m",
            default_value=1.5,
            physiological_range=(1.0, 2.0)
        )
    ],
    depends_on=["gi_enzyme_kinetics"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(amylase_kinetics)

"""Michaelis-Menten enzyme kinetics for digestion."""


def compute_enzyme_kinetics(S: float, Vmax: float, Km: float) -> float:
    """
    Calculate enzyme reaction rate using Michaelis-Menten kinetics.

    Parameters
    ----------
    S : float
        Substrate concentration
    Vmax : float
        Maximum reaction rate
    Km : float
        Michaelis constant (substrate concentration at half Vmax)

    Returns
    -------
    float
        Reaction rate (same units as Vmax)
    """
    return Vmax * S / (Km + S)


enzyme_kinetics = create_equation(
    id="gi_enzyme_kinetics",
    output_units='variable',
    name="Enzyme Kinetics (Michaelis-Menten)",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"v = \frac{V_{\max} \times [S]}{K_m + [S]}",
    simplified="v = V_max × [S] / (K_m + [S])",
    description="Michaelis-Menten enzyme kinetics for digestive enzymes (amylase, pepsin, lipase, etc.)",
    compute_func=compute_enzyme_kinetics,
    parameters=[
        Parameter(
            name="S",
            description="Substrate concentration",
            units="variable",
            symbol="[S]",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="Vmax",
            description="Maximum reaction rate",
            units="variable",
            symbol=r"V_{\max}",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="variable",
            symbol="K_m",
            physiological_range=(0.01, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(enzyme_kinetics)

"""Lipase activity dependence on bile salt concentration."""


def compute_lipase_activity_bile(bile_salt_conc: float, CMC: float = 3.0) -> float:
    """
    Calculate lipase effectiveness based on bile salt concentration.

    Micelle formation (requires [bile salt] > CMC) is necessary for optimal lipase activity.

    Parameters
    ----------
    bile_salt_conc : float
        Bile salt concentration (mM)
    CMC : float
        Critical micellar concentration (mM), default 3.0 mM

    Returns
    -------
    float
        Lipase effectiveness (0-1)
    """
    if bile_salt_conc >= CMC:
        return 1.0
    else:
        return bile_salt_conc / CMC


lipase_activity_bile = create_equation(
    id="lipase_activity_bile",
    output_units='dimensionless',
    name="Lipase Activity vs Bile Salts",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"\text{Effectiveness} = \begin{cases} 1.0 & [\text{bile}] \geq \text{CMC} \\ \frac{[\text{bile}]}{\text{CMC}} & [\text{bile}] < \text{CMC} \end{cases}",
    simplified="Effectiveness = 1.0 if [bile] ≥ CMC, else [bile]/CMC",
    description="Lipase effectiveness depends on bile salt concentration. Full activity when [bile salt] > CMC (~3 mM)",
    compute_func=compute_lipase_activity_bile,
    parameters=[
        Parameter(
            name="bile_salt_conc",
            description="Bile salt concentration",
            units="mM",
            symbol=r"[\text{bile}]",
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
    depends_on=["critical_micellar_concentration"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(lipase_activity_bile)

"""Pancreatic lipase kinetics for triglyceride digestion."""


def compute_lipase_rate(TG_conc: float, J_max: float = 15.0, Km: float = 2.0) -> float:
    """
    Calculate pancreatic lipase digestion rate for triglycerides.

    Lipase requires colipase to anchor to emulsion surface.
    TG + H2O → 2 FFA + 2-monoglyceride

    Parameters
    ----------
    TG_conc : float
        Triglyceride concentration (mM)
    J_max : float
        Maximum digestion rate (mM/min), default 15
    Km : float
        Michaelis constant (mM), default 2.0

    Returns
    -------
    float
        Digestion rate (mM/min)
    """
    return J_max * TG_conc / (Km + TG_conc)


lipase_kinetics = create_equation(
    id="lipase_kinetics",
    output_units='mM/min',
    name="Pancreatic Lipase Kinetics",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"J = \frac{J_{\max} \times [\text{TG}]}{K_m + [\text{TG}]}",
    simplified="J = J_max × [TG] / (K_m + [TG])",
    description="Pancreatic lipase kinetics for triglyceride hydrolysis. Requires colipase for anchoring. Produces 2 FFA + 2-MG",
    compute_func=compute_lipase_rate,
    parameters=[
        Parameter(
            name="TG_conc",
            description="Triglyceride concentration",
            units="mM",
            symbol=r"[\text{TG}]",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="J_max",
            description="Maximum digestion rate",
            units="mM/min",
            symbol=r"J_{\max}",
            default_value=15.0,
            physiological_range=(10.0, 25.0)
        ),
        Parameter(
            name="Km",
            description="Michaelis constant",
            units="mM",
            symbol="K_m",
            default_value=2.0,
            physiological_range=(1.0, 5.0)
        )
    ],
    depends_on=["gi_enzyme_kinetics"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(lipase_kinetics)

"""Pepsin activity as function of pH."""

import numpy as np


def compute_pepsin_activity(H_conc: float, A_max: float = 1.0, K_H: float = 5.0, n: float = 2.0) -> float:
    """
    Calculate pepsin activity based on pH and H+ concentration.

    Pepsin has optimal pH of 1.8-3.5. Activity follows Hill equation.

    Parameters
    ----------
    H_conc : float
        H+ concentration (mM)
    A_max : float
        Maximum activity (normalized), default 1.0
    K_H : float
        Half-maximal H+ concentration (mM), default 5.0
    n : float
        Hill coefficient, default 2.0

    Returns
    -------
    float
        Pepsin activity (normalized, 0-1)
    """
    activity = A_max * (H_conc ** n) / (K_H ** n + H_conc ** n)
    return activity


pepsin_activity = create_equation(
    id="pepsin_activity",
    output_units='dimensionless',
    name="Pepsin Activity",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"A = \frac{A_{\max} \times [H^+]^n}{K_H^n + [H^+]^n}",
    simplified="A = A_max × [H+]^n / (K_H^n + [H+]^n)",
    description="Pepsin activity as function of H+ concentration. Optimal pH: 1.8-3.5. Cleaves aromatic amino acids (Phe, Tyr, Trp)",
    compute_func=compute_pepsin_activity,
    parameters=[
        Parameter(
            name="H_conc",
            description="H+ concentration",
            units="mM",
            symbol="[H^+]",
            physiological_range=(0.001, 150.0)
        ),
        Parameter(
            name="A_max",
            description="Maximum activity",
            units="dimensionless",
            symbol=r"A_{\max}",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="K_H",
            description="Half-maximal H+ concentration",
            units="mM",
            symbol="K_H",
            default_value=5.0,
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient",
            units="dimensionless",
            symbol="n",
            default_value=2.0,
            physiological_range=(1.0, 4.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(pepsin_activity)

"""First-order starch digestion kinetics."""


def compute_starch_remaining(t: float, starch_0: float, k: float = 0.1) -> float:
    """
    Calculate remaining starch using first-order digestion kinetics.

    Parameters
    ----------
    t : float
        Time (minutes)
    starch_0 : float
        Initial starch amount (g)
    k : float
        Digestion rate constant (1/min), default 0.1

    Returns
    -------
    float
        Remaining starch (g)
    """
    return starch_0 * np.exp(-k * t)


starch_digestion_first_order = create_equation(
    id="starch_digestion_first_order",
    output_units='g',
    name="First-Order Starch Digestion",
    category=EquationCategory.GASTROINTESTINAL,
    latex=r"[\text{Starch}](t) = [\text{Starch}]_0 \times e^{-kt}",
    simplified="[Starch](t) = [Starch]_0 × e^(-kt)",
    description="First-order starch digestion kinetics by amylase",
    compute_func=compute_starch_remaining,
    parameters=[
        Parameter(
            name="t",
            description="Time",
            units="min",
            symbol="t",
            physiological_range=(0.0, 300.0)
        ),
        Parameter(
            name="starch_0",
            description="Initial starch amount",
            units="g",
            symbol=r"[\text{Starch}]_0",
            physiological_range=(0.0, 100.0)
        ),
        Parameter(
            name="k",
            description="Digestion rate constant",
            units="1/min",
            symbol="k",
            default_value=0.1,
            physiological_range=(0.05, 0.2)
        )
    ],
    depends_on=["amylase_kinetics"],
    metadata=EquationMetadata(
        source_unit=8,
        source_chapter="8.3"
    )
)

register_equation(starch_digestion_first_order)


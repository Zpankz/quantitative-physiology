"""Cardiac electrophysiology and ECG equations."""

"""Funny current (If) equation for pacemaker cells."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_funny_current(V_m: float, E_f: float, g_f: float, y: float) -> float:
    """
    Calculate funny current (HCN channel current) in pacemaker cells.

    Parameters
    ----------
    V_m : float
        Membrane potential (mV)
    E_f : float
        Reversal potential for funny current (mV)
    g_f : float
        Maximum conductance (nS)
    y : float
        Gating variable (0-1)

    Returns
    -------
    float
        Funny current (pA)
    """
    return g_f * (V_m - E_f) * y


funny_current = create_equation(
    id="funny_current",
    output_units='pA',
    name="Funny Current (If)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"I_f = g_f \times (V_m - E_f) \times y",
    simplified="I_f = g_f × (V_m - E_f) × y",
    description="HCN channel current responsible for phase 4 depolarization in pacemaker cells",
    compute_func=compute_funny_current,
    parameters=[
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            physiological_range=(-70.0, 40.0)
        ),
        Parameter(
            name="E_f",
            description="Reversal potential for funny current",
            units="mV",
            symbol="E_f",
            default_value=-20.0,
            physiological_range=(-30.0, -10.0)
        ),
        Parameter(
            name="g_f",
            description="Maximum funny current conductance",
            units="nS",
            symbol="g_f",
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="y",
            description="Gating variable",
            units="dimensionless",
            symbol="y",
            physiological_range=(0.0, 1.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.2"
    )
)

register_equation(funny_current)

"""Heart rate modulation by autonomic tone."""


def compute_heart_rate(f_intrinsic: float, df_symp: float, df_para: float) -> float:
    """
    Calculate heart rate with autonomic modulation.

    Parameters
    ----------
    f_intrinsic : float
        Intrinsic SA node firing rate (bpm)
    df_symp : float
        Sympathetic contribution (increase, bpm)
    df_para : float
        Parasympathetic contribution (decrease, bpm)

    Returns
    -------
    float
        Resulting heart rate (bpm)
    """
    return f_intrinsic + df_symp - df_para


heart_rate = create_equation(
    id="heart_rate_autonomic",
    output_units='bpm',
    produces="HR",
    name="Heart Rate with Autonomic Tone",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"f_{\text{heart}} = f_{\text{intrinsic}} + \Delta f_{\text{sympathetic}} - \Delta f_{\text{parasympathetic}}",
    simplified="f_heart = f_intrinsic + Δf_symp - Δf_para",
    description="Heart rate modulation by sympathetic and parasympathetic nervous systems",
    compute_func=compute_heart_rate,
    parameters=[
        Parameter(
            name="f_intrinsic",
            description="Intrinsic SA node rate",
            units="bpm",
            symbol="f_{intrinsic}",
            default_value=100.0,
            physiological_range=(60.0, 100.0)
        ),
        Parameter(
            name="df_symp",
            description="Sympathetic increase",
            units="bpm",
            symbol=r"\Delta f_{symp}",
            physiological_range=(0.0, 80.0)
        ),
        Parameter(
            name="df_para",
            description="Parasympathetic decrease",
            units="bpm",
            symbol=r"\Delta f_{para}",
            physiological_range=(0.0, 40.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.2"
    )
)

register_equation(heart_rate)

"""Bazett's formula for QTc correction."""


def compute_qtc_bazett(QT: float, RR: float) -> float:
    """
    Calculate rate-corrected QT interval using Bazett's formula.

    Parameters
    ----------
    QT : float
        Measured QT interval (ms)
    RR : float
        RR interval (seconds)

    Returns
    -------
    float
        Corrected QT interval (ms)
    """
    return QT / np.sqrt(RR)


qtc_bazett = create_equation(
    id="qtc_bazett",
    output_units='ms',
    name="Bazett's QTc Correction",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{QTc} = \frac{\text{QT}}{\sqrt{\text{RR}}}",
    simplified="QTc = QT / √(RR)",
    description="Rate-corrected QT interval using Bazett's formula",
    compute_func=compute_qtc_bazett,
    parameters=[
        Parameter(
            name="QT",
            description="Measured QT interval",
            units="ms",
            symbol="QT",
            physiological_range=(350.0, 440.0)
        ),
        Parameter(
            name="RR",
            description="RR interval",
            units="s",
            symbol="RR",
            physiological_range=(0.6, 1.2)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.2"
    )
)

register_equation(qtc_bazett)

"""Fridericia's formula for QTc correction."""


def compute_qtc_fridericia(QT: float, RR: float) -> float:
    """
    Calculate rate-corrected QT interval using Fridericia's formula.

    More accurate at extreme heart rates than Bazett's formula.

    Parameters
    ----------
    QT : float
        Measured QT interval (ms)
    RR : float
        RR interval (seconds)

    Returns
    -------
    float
        Corrected QT interval (ms)
    """
    return QT / np.cbrt(RR)


qtc_fridericia = create_equation(
    id="qtc_fridericia",
    output_units='ms',
    name="Fridericia's QTc Correction",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{QTc} = \frac{\text{QT}}{\sqrt[3]{\text{RR}}}",
    simplified="QTc = QT / ∛(RR)",
    description="Rate-corrected QT interval using Fridericia's formula (more accurate at extreme rates)",
    compute_func=compute_qtc_fridericia,
    parameters=[
        Parameter(
            name="QT",
            description="Measured QT interval",
            units="ms",
            symbol="QT",
            physiological_range=(350.0, 440.0)
        ),
        Parameter(
            name="RR",
            description="RR interval",
            units="s",
            symbol="RR",
            physiological_range=(0.6, 1.2)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.2"
    )
)

register_equation(qtc_fridericia)

__all__ = ['funny_current', 'heart_rate', 'qtc_bazett', 'qtc_fridericia']


# --- coverage pass 2 (residual reconsideration) ---

def compute_einthoven_lead_relation(lead_I, lead_III):
    """Einthoven's law: lead II = lead I + lead III (Feher 5.8, Eqn 5.8.3), from Kirchhoff's voltage law around the Einthoven triangle with the standard lead-II sign convention. Voltages in mV; returns lead II (mV). Reusable to reconstruct any one bipolar limb lead from the other two, or to check limb-lead placement."""
    return lead_I + lead_III

einthoven_lead_relation = create_equation(
    id='einthoven_lead_relation',
    output_units='mV',
    name="Einthoven's Law (limb leads)",
    category=EquationCategory.CARDIOVASCULAR,
    latex='V_{II} = V_{I} + V_{III}',
    simplified='lead_II = lead_I + lead_III',
    description="Einthoven's law: with the standard bipolar limb-lead definitions and sign convention, the three limb-lead voltages satisfy II = I + III at every instant (Kirchhoff's voltage law around the Einthoven triangle). Used to reconstruct a missing/artefactual limb lead from the other two and to verify correct electrode placement. Feher section 5.8, Eqn 5.8.3.",
    compute_func=compute_einthoven_lead_relation,
    parameters=[
        Parameter(name='lead_I', description='Einthoven bipolar limb lead I voltage (LA - RA)', units='mV', symbol='V_I', physiological_range=(-5.0, 5.0)),
        Parameter(name='lead_III', description='Einthoven bipolar limb lead III voltage (LL - LA)', units='mV', symbol='V_{III}', physiological_range=(-5.0, 5.0)),
    ],
    depends_on=[],
    produces='lead_II',
    metadata=EquationMetadata(source_unit=5, source_chapter='5.8',
                              source_section='Einthoven idealized the thorax as a triangle', page_reference=None,
                              textbook_equation_number='5.8.3'),
)
register_equation(einthoven_lead_relation)

try:
    __all__ += ['einthoven_lead_relation']
except NameError:
    __all__ = ['einthoven_lead_relation']


# --- clinical additions (CICM, beyond Feher) ---

def compute_rate_pressure_product(HR, SBP):
    """RPP = HR*SBP, a surrogate of myocardial O2 demand. Normal rest ~<10000."""
    return HR * SBP

rate_pressure_product = create_equation(
    id='rate_pressure_product',
    output_units='dimensionless',
    name='Rate-Pressure Product',
    category=EquationCategory.CARDIOVASCULAR,
    latex='RPP = HR\\times SBP',
    simplified='RPP = HR*SBP',
    description='Rate-pressure (double) product, a clinical surrogate for myocardial oxygen demand and a determinant of ischaemia threshold.',
    compute_func=compute_rate_pressure_product,
    parameters=[
        Parameter(name='HR', description='Heart rate', units='bpm', symbol='HR', physiological_range=(30, 220)),
        Parameter(name='SBP', description='Systolic blood pressure', units='mmHg', symbol='SBP', physiological_range=(60, 250)),
    ],
    depends_on=["heart_rate_autonomic"],
    produces='RPP',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(rate_pressure_product)

try:
    __all__ += ['rate_pressure_product']
except NameError:
    __all__ = ['rate_pressure_product']

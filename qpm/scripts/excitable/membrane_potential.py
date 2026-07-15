"""Membrane Potential Equations

Nernst, GHK, and chord conductance equations for excitable cell membranes.

Source: Quantitative Human Physiology 3rd Edition, Unit 3"""

"""
Chord Conductance Equation

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def chord_conductance(g_K: float, g_Na: float, g_Cl: float,
                      E_K: float = -90.0, E_Na: float = 67.0, E_Cl: float = -89.0) -> float:
    """
    Chord conductance equation for membrane potential.

    Formula: V_m = (g_K × E_K + g_Na × E_Na + g_Cl × E_Cl) / (g_K + g_Na + g_Cl)

    This represents the membrane as a parallel combination of ion channels,
    each with its own conductance and equilibrium potential.

    Parameters:
    -----------
    g_K : float - Potassium conductance (mS/cm²)
    g_Na : float - Sodium conductance (mS/cm²)
    g_Cl : float - Chloride conductance (mS/cm²)
    E_K : float - Potassium equilibrium potential (mV), default: -90.0
    E_Na : float - Sodium equilibrium potential (mV), default: 67.0
    E_Cl : float - Chloride equilibrium potential (mV), default: -89.0

    Returns:
    --------
    V_m : float - Membrane potential (mV)
    """
    numerator = g_K * E_K + g_Na * E_Na + g_Cl * E_Cl
    denominator = g_K + g_Na + g_Cl

    return numerator / denominator

# Create and register atomic equation
chord_conductance_eq = create_equation(
    id="chord_conductance",
    output_units='mV',
    name="Chord Conductance Equation",
    category=EquationCategory.EXCITABLE,
    latex=r"V_m = \frac{g_K E_K + g_{Na} E_{Na} + g_{Cl} E_{Cl}}{g_K + g_{Na} + g_{Cl}}",
    simplified="V_m = (g_K × E_K + g_Na × E_Na + g_Cl × E_Cl) / (g_K + g_Na + g_Cl)",
    description="Membrane potential from weighted average of equilibrium potentials",
    compute_func=chord_conductance,
    parameters=[
        Parameter(
            name="g_K",
            description="Potassium conductance",
            units="mS/cm²",
            symbol="g_K",
            physiological_range=(0.0, 50.0)
        ),
        Parameter(
            name="g_Na",
            description="Sodium conductance",
            units="mS/cm²",
            symbol="g_{Na}",
            physiological_range=(0.0, 150.0)
        ),
        Parameter(
            name="g_Cl",
            description="Chloride conductance",
            units="mS/cm²",
            symbol="g_{Cl}",
            physiological_range=(0.0, 20.0)
        ),
        Parameter(
            name="E_K",
            description="Potassium equilibrium potential",
            units="mV",
            symbol="E_K",
            default_value=-90.0,
            physiological_range=(-95.0, -80.0)
        ),
        Parameter(
            name="E_Na",
            description="Sodium equilibrium potential",
            units="mV",
            symbol="E_{Na}",
            default_value=67.0,
            physiological_range=(50.0, 70.0)
        ),
        Parameter(
            name="E_Cl",
            description="Chloride equilibrium potential",
            units="mV",
            symbol="E_{Cl}",
            default_value=-89.0,
            physiological_range=(-95.0, -80.0)
        ),
    ],
    depends_on=["nernst_equation", "k_nernst_potential"],  # E_K from the ion-specific Nernst (produces 'E_K')
    metadata=EquationMetadata(source_unit=3, source_chapter="3.1")
)
register_equation(chord_conductance_eq)

"""
Goldman-Hodgkin-Katz (GHK) Equation

Source: Quantitative Human Physiology 3rd Edition, Unit 3
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)

def ghk_potential(P_K: float, P_Na: float, P_Cl: float,
                  K_out: float, K_in: float,
                  Na_out: float, Na_in: float,
                  Cl_out: float, Cl_in: float,
                  R: float = 8.314, T_body: float = 310.0, F: float = 96485.0) -> float:
    """
    Goldman-Hodgkin-Katz equation for membrane potential with multiple ions.

    Formula: V_m = (RT/F) × ln[(P_K[K⁺]_o + P_Na[Na⁺]_o + P_Cl[Cl⁻]_i) /
                                (P_K[K⁺]_i + P_Na[Na⁺]_i + P_Cl[Cl⁻]_o)]

    This extends the Nernst equation to multiple permeant ion species.

    Parameters:
    -----------
    P_K : float - Potassium permeability (dimensionless relative)
    P_Na : float - Sodium permeability (dimensionless relative)
    P_Cl : float - Chloride permeability (dimensionless relative)
    K_out : float - Extracellular potassium concentration (mM)
    K_in : float - Intracellular potassium concentration (mM)
    Na_out : float - Extracellular sodium concentration (mM)
    Na_in : float - Intracellular sodium concentration (mM)
    Cl_out : float - Extracellular chloride concentration (mM)
    Cl_in : float - Intracellular chloride concentration (mM)
    R : float - Gas constant (J/(mol·K)), default: 8.314
    T_body : float - Body temperature (K), default: 310.0 (37°C)
    F : float - Faraday constant (C/mol), default: 96485.0

    Returns:
    --------
    V_m : float - Membrane potential (V)
    """
    numerator = P_K * K_out + P_Na * Na_out + P_Cl * Cl_in
    denominator = P_K * K_in + P_Na * Na_in + P_Cl * Cl_out

    return (R * T_body / F) * np.log(numerator / denominator) * 1000.0  # V -> mV

# Create and register atomic equation
ghk_potential_eq = create_equation(
    id="ghk_potential",
    output_units='mV',
    name="Goldman-Hodgkin-Katz Potential",
    category=EquationCategory.EXCITABLE,
    latex=r"V_m = \frac{RT}{F} \ln\left[\frac{P_K[K^+]_o + P_{Na}[Na^+]_o + P_{Cl}[Cl^-]_i}{P_K[K^+]_i + P_{Na}[Na^+]_i + P_{Cl}[Cl^-]_o}\right]",
    simplified="V_m = (RT/F) × ln[(P_K[K⁺]_o + P_Na[Na⁺]_o + P_Cl[Cl⁻]_i) / (P_K[K⁺]_i + P_Na[Na⁺]_i + P_Cl[Cl⁻]_o)]",
    description="Membrane potential accounting for multiple permeant ion species",
    compute_func=ghk_potential,
    parameters=[
        Parameter(
            name="P_K",
            description="Potassium permeability (relative)",
            units="dimensionless",
            symbol="P_K",
            default_value=1.0,
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="P_Na",
            description="Sodium permeability (relative)",
            units="dimensionless",
            symbol="P_{Na}",
            default_value=0.04,
            physiological_range=(0.01, 0.5)
        ),
        Parameter(
            name="P_Cl",
            description="Chloride permeability (relative)",
            units="dimensionless",
            symbol="P_{Cl}",
            default_value=0.45,
            physiological_range=(0.1, 1.0)
        ),
        Parameter(
            name="K_out",
            description="Extracellular potassium concentration",
            units="mM",
            symbol="[K^+]_o",
            default_value=5.0,
            physiological_range=(3.5, 5.5)
        ),
        Parameter(
            name="K_in",
            description="Intracellular potassium concentration",
            units="mM",
            symbol="[K^+]_i",
            default_value=140.0,
            physiological_range=(120.0, 155.0)
        ),
        Parameter(
            name="Na_out",
            description="Extracellular sodium concentration",
            units="mM",
            symbol="[Na^+]_o",
            default_value=145.0,
            physiological_range=(135.0, 150.0)
        ),
        Parameter(
            name="Na_in",
            description="Intracellular sodium concentration",
            units="mM",
            symbol="[Na^+]_i",
            default_value=12.0,
            physiological_range=(10.0, 15.0)
        ),
        Parameter(
            name="Cl_out",
            description="Extracellular chloride concentration",
            units="mM",
            symbol="[Cl^-]_o",
            default_value=120.0,
            physiological_range=(100.0, 130.0)
        ),
        Parameter(
            name="Cl_in",
            description="Intracellular chloride concentration",
            units="mM",
            symbol="[Cl^-]_i",
            default_value=4.0,
            physiological_range=(2.0, 10.0)
        ),
        PHYSICAL_CONSTANTS['R'],
        PHYSICAL_CONSTANTS['T_body'],
        PHYSICAL_CONSTANTS['F'],
    ],
    depends_on=["nernst_equation"],  # GHK generalizes Nernst
    metadata=EquationMetadata(source_unit=3, source_chapter="3.1")
)
register_equation(ghk_potential_eq)

__all__ = ['ghk_potential_eq', 'chord_conductance_eq']


# --- clinical additions (CICM, beyond Feher) ---

def compute_driving_force_ion(V_m, E_ion):
    """Ionic driving force = V_m - E_ion (mV): the net electrochemical push on an ion."""
    return V_m - E_ion

driving_force_ion = create_equation(
    id='driving_force_ion',
    output_units='mV',
    name='Electrochemical Driving Force',
    category=EquationCategory.EXCITABLE,
    latex='DF = V_m - E_{ion}',
    simplified='DF = V_m - E_ion',
    description="Electrochemical driving force on an ion: the difference between the membrane potential and the ion's equilibrium potential. Its sign sets current direction; multiplied by conductance it gives ionic current.",
    compute_func=compute_driving_force_ion,
    parameters=[
        Parameter(name='V_m', description='Membrane potential', units='mV', symbol='V_m', physiological_range=(-100, 60)),
        Parameter(name='E_ion', description='Ion equilibrium (Nernst) potential', units='mV', symbol='E_ion', physiological_range=(-100, 80)),
    ],
    depends_on=[],
    produces='driving_force',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(driving_force_ion)


def compute_ionic_current(g_ion, V_m, E_ion):
    """I_ion = g_ion*(V_m - E_ion): chord-conductance ionic current (g nS, V mV -> I pA)."""
    return g_ion * (V_m - E_ion)

ionic_current = create_equation(
    id='ionic_current',
    output_units='pA',
    name="Ionic Current (Ohm's Law)",
    category=EquationCategory.EXCITABLE,
    latex='I_{ion} = g_{ion}(V_m - E_{ion})',
    simplified='I_ion = g*(V_m - E_ion)',
    description="Ohm's law for an ionic current under the chord-conductance model: current equals conductance times electrochemical driving force. Positive = outward (by convention). nS*mV = pA.",
    compute_func=compute_ionic_current,
    parameters=[
        Parameter(name='g_ion', description='Ionic conductance', units='nS', symbol='g', physiological_range=(0.001, 500)),
        Parameter(name='V_m', description='Membrane potential', units='mV', symbol='V_m', physiological_range=(-100, 60)),
        Parameter(name='E_ion', description='Equilibrium potential', units='mV', symbol='E_ion', physiological_range=(-100, 80)),
    ],
    depends_on=[],
    produces='I_ion',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(ionic_current)

try:
    __all__ += ['driving_force_ion', 'ionic_current']
except NameError:
    __all__ = ['driving_force_ion', 'ionic_current']

"""Membrane transport equations - passive and active transport."""

"""
Carrier-Mediated Transport - Facilitated diffusion via carriers (Michaelis-Menten)

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import numpy as np

def compute_carrier_transport(S: float, J_max: float, K_m: float) -> float:
    """
    Calculate carrier-mediated transport rate (Michaelis-Menten kinetics).

    Formula: J = J_max × [S] / (K_m + [S])

    Parameters:
    -----------
    S : float
        Substrate concentration (mM or mol/m³)
    J_max : float
        Maximum transport rate (mol/(m²·s) or similar)
    K_m : float
        Half-saturation constant (mM or mol/m³)

    Returns:
    --------
    J : float
        Transport rate (same units as J_max)

    Characteristics:
        - Saturable (approaches J_max at high [S])
        - Specific (substrate selectivity)
        - Competitive inhibition possible
        - Temperature dependent (Q₁₀ > 1)
    """
    return J_max * S / (K_m + S)


# Create and register atomic equation
carrier_transport = create_equation(
    id="carrier_transport",
    output_units='mol/(m^2*s)',
    name="Carrier-Mediated Transport (Michaelis-Menten)",
    category=EquationCategory.MEMBRANE,
    latex=r"J = \frac{J_{max} \cdot [S]}{K_m + [S]}",
    simplified="J = (J_max * S) / (K_m + S)",
    description="Facilitated diffusion via carrier proteins showing saturation kinetics, following Michaelis-Menten form.",
    compute_func=compute_carrier_transport,
    parameters=[
        Parameter(
            name="S",
            description="Substrate concentration",
            units="mol/m³",
            symbol="[S]",
            default_value=None,
            physiological_range=(0.0, 1000.0)  # mM range
        ),
        Parameter(
            name="J_max",
            description="Maximum transport rate",
            units="mol/(m²·s)",
            symbol="J_{max}",
            default_value=None
        ),
        Parameter(
            name="K_m",
            description="Half-saturation constant (Michaelis constant)",
            units="mol/m³",
            symbol="K_m",
            default_value=None
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(carrier_transport)

"""
Fick's Law for Membrane Flux - Simple diffusion across membrane

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""

def compute_ficks_membrane_flux(P: float, C_out: float, C_in: float) -> float:
    """
    Calculate membrane flux using Fick's law.

    Formula: J_S = P × (C_out - C_in)

    Parameters:
    -----------
    P : float
        Permeability coefficient (m/s or cm/s)
    C_out : float
        Extracellular concentration (mol/m³ or mM)
    C_in : float
        Intracellular concentration (mol/m³ or mM)

    Returns:
    --------
    J_S : float
        Solute flux (mol/(m²·s) or mol/(cm²·s))
        Positive flux is into the cell
    """
    return P * (C_out - C_in)


# Create and register atomic equation
ficks_membrane_flux = create_equation(
    id="ficks_membrane_flux",
    output_units='mol/(m^2*s)',
    name="Fick's Law for Membrane Flux",
    category=EquationCategory.MEMBRANE,
    latex=r"J_S = P \cdot (C_{out} - C_{in})",
    simplified="J_S = P * (C_out - C_in)",
    description="Simple diffusion flux across a membrane for uncharged species, proportional to the concentration gradient.",
    compute_func=compute_ficks_membrane_flux,
    parameters=[
        Parameter(
            name="P",
            description="Permeability coefficient",
            units="m/s",
            symbol="P",
            default_value=None
        ),
        Parameter(
            name="C_out",
            description="Extracellular concentration",
            units="mol/m³",
            symbol="C_{out}",
            default_value=None
        ),
        Parameter(
            name="C_in",
            description="Intracellular concentration",
            units="mol/m³",
            symbol="C_{in}",
            default_value=None
        ),
    ],
    depends_on=["permeability_coefficient"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(ficks_membrane_flux)

"""
Goldman Flux Equation - Electrodiffusion of charged species

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)

def compute_goldman_flux(P: float, z: int, V_m: float, C_in: float, C_out: float,
                         T_body: float = 310.0, R: float = 8.314, F: float = 96485.0) -> float:
    """
    Calculate ion flux using Goldman flux equation.

    Formula: J_S = P × z × F × V_m / (RT) × (C_in - C_out × e^(zFV_m/RT)) / (1 - e^(zFV_m/RT))

    Parameters:
    -----------
    P : float
        Permeability coefficient (m/s)
    z : int
        Ion valence (charge number)
    V_m : float
        Membrane potential (V)
    C_in : float
        Intracellular concentration (mol/m³)
    C_out : float
        Extracellular concentration (mol/m³)
    T_body : float
        Body temperature (K), default: 310 K (37°C)
    R : float
        Gas constant (J/(mol·K)), default: 8.314
    F : float
        Faraday constant (C/mol), default: 96485

    Returns:
    --------
    J_S : float
        Ion flux (mol/(m²·s))
        Positive flux is into the cell
    """
    u = z * F * (V_m / 1000.0) / (R * T_body)  # V_m in mV

    # Handle near-zero potential to avoid division by zero
    if abs(u) < 1e-6:
        return P * (C_in - C_out)

    return P * u * (C_in - C_out * np.exp(-u)) / (1 - np.exp(-u))


# Create and register atomic equation
goldman_flux = create_equation(
    id="goldman_flux",
    output_units='mol/(m^2*s)',
    name="Goldman Flux Equation",
    category=EquationCategory.MEMBRANE,
    latex=r"J_S = P \cdot \frac{zFV_m}{RT} \cdot \frac{C_{in} - C_{out} e^{zFV_m/RT}}{1 - e^{zFV_m/RT}}",
    simplified="J_S = P * (zFV_m/RT) * (C_in - C_out*exp(zFV_m/RT)) / (1 - exp(zFV_m/RT))",
    description="Flux equation for charged species considering both concentration and electrical gradients (electrodiffusion).",
    compute_func=compute_goldman_flux,
    parameters=[
        Parameter(
            name="P",
            description="Permeability coefficient",
            units="m/s",
            symbol="P",
            default_value=None
        ),
        Parameter(
            name="z",
            description="Ion valence",
            units="dimensionless",
            symbol="z",
            default_value=None
        ),
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            default_value=None,
            physiological_range=(-0.1, 0.05)  # -100 mV to +50 mV
        ),
        Parameter(
            name="C_in",
            description="Intracellular concentration",
            units="mol/m³",
            symbol="C_{in}",
            default_value=None
        ),
        Parameter(
            name="C_out",
            description="Extracellular concentration",
            units="mol/m³",
            symbol="C_{out}",
            default_value=None
        ),
        PHYSICAL_CONSTANTS["T_body"],
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["F"],
    ],
    depends_on=["permeability_coefficient"],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(goldman_flux)

"""
Na+/K+-ATPase Pump Rate - Sodium-potassium pump kinetics

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""

def compute_nak_pump_rate(Na_in: float, K_out: float, ATP: float,
                          J_max: float = 200.0, K_Na: float = 10.0,
                          K_K: float = 2.0, K_ATP: float = 0.5) -> float:
    """
    Calculate Na+/K+-ATPase pump rate.

    Formula: J_pump = J_max × f([Na+]_i, [K+]_o, [ATP])
    where f includes Hill-type cooperativity for Na+ and K+

    Parameters:
    -----------
    Na_in : float
        Intracellular Na+ concentration (mM)
    K_out : float
        Extracellular K+ concentration (mM)
    ATP : float
        Intracellular ATP concentration (mM)
    J_max : float
        Maximum pump rate (cycles/s), default: 200
    K_Na : float
        Half-saturation for Na+ (mM), default: 10
    K_K : float
        Half-saturation for K+ (mM), default: 2
    K_ATP : float
        Half-saturation for ATP (mM), default: 0.5

    Returns:
    --------
    J_pump : float
        Pump rate (cycles/s)
        Stoichiometry: 3 Na+ out : 2 K+ in per cycle

    Typical pump rate: 100-300 cycles/second
    """
    # Hill cooperativity: n=3 for Na+, n=2 for K+
    f_Na = (Na_in / K_Na)**3 / (1 + (Na_in / K_Na)**3)
    f_K = (K_out / K_K)**2 / (1 + (K_out / K_K)**2)
    f_ATP = ATP / (K_ATP + ATP)

    return J_max * f_Na * f_K * f_ATP


# Create and register atomic equation
nak_pump_rate = create_equation(
    id="nak_pump_rate",
    output_units='cycles/s',
    name="Na+/K+-ATPase Pump Rate",
    category=EquationCategory.MEMBRANE,
    latex=r"J_{pump} = J_{max} \cdot f_{Na} \cdot f_K \cdot f_{ATP}",
    simplified="J_pump = J_max * f_Na * f_K * f_ATP",
    description="Rate of the Na+/K+-ATPase pump with cooperative binding kinetics (3 Na+ out, 2 K+ in per ATP).",
    compute_func=compute_nak_pump_rate,
    parameters=[
        Parameter(
            name="Na_in",
            description="Intracellular Na+ concentration",
            units="mM",
            symbol="[Na^+]_i",
            default_value=None,
            physiological_range=(5.0, 50.0)
        ),
        Parameter(
            name="K_out",
            description="Extracellular K+ concentration",
            units="mM",
            symbol="[K^+]_o",
            default_value=None,
            physiological_range=(2.0, 10.0)
        ),
        Parameter(
            name="ATP",
            description="Intracellular ATP concentration",
            units="mM",
            symbol="[ATP]",
            default_value=None,
            physiological_range=(1.0, 10.0)
        ),
        Parameter(
            name="J_max",
            description="Maximum pump rate",
            units="cycles/s",
            symbol="J_{max}",
            default_value=200.0,
            physiological_range=(100.0, 300.0)
        ),
        Parameter(
            name="K_Na",
            description="Half-saturation constant for Na+",
            units="mM",
            symbol="K_{Na}",
            default_value=10.0
        ),
        Parameter(
            name="K_K",
            description="Half-saturation constant for K+",
            units="mM",
            symbol="K_K",
            default_value=2.0
        ),
        Parameter(
            name="K_ATP",
            description="Half-saturation constant for ATP",
            units="mM",
            symbol="K_{ATP}",
            default_value=0.5
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.3")
)

register_equation(nak_pump_rate)

"""
NCX Reversal Potential - Na+/Ca2+ exchanger equilibrium potential

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""

def compute_ncx_reversal(E_Na: float, E_Ca: float) -> float:
    """
    Calculate Na+/Ca2+ exchanger reversal potential.

    Formula: E_NCX = 3E_Na - 2E_Ca

    The NCX exchanges 3 Na+ for 1 Ca2+, making it electrogenic.

    Parameters:
    -----------
    E_Na : float
        Sodium reversal potential (mV)
    E_Ca : float
        Calcium reversal potential (mV)

    Returns:
    --------
    E_NCX : float
        NCX reversal potential (mV)

    Notes:
        When V_m > E_NCX: Ca2+ extrusion (forward mode)
        When V_m < E_NCX: Ca2+ influx (reverse mode)
    """
    return 3 * E_Na - 2 * E_Ca


# Create and register atomic equation
ncx_reversal = create_equation(
    id="ncx_reversal",
    output_units='mV',
    name="Na+/Ca2+ Exchanger Reversal Potential",
    category=EquationCategory.MEMBRANE,
    latex=r"E_{NCX} = 3E_{Na} - 2E_{Ca}",
    simplified="E_NCX = 3*E_Na - 2*E_Ca",
    description="Reversal potential for the Na+/Ca2+ exchanger (NCX), which exchanges 3 Na+ for 1 Ca2+ (electrogenic).",
    compute_func=compute_ncx_reversal,
    parameters=[
        Parameter(
            name="E_Na",
            description="Sodium reversal potential",
            units="mV",
            symbol="E_{Na}",
            default_value=None,
            physiological_range=(40.0, 70.0)
        ),
        Parameter(
            name="E_Ca",
            description="Calcium reversal potential",
            units="mV",
            symbol="E_{Ca}",
            default_value=None,
            physiological_range=(100.0, 150.0)
        ),
    ],
    depends_on=[],  # Could depend on Nernst equation
    metadata=EquationMetadata(source_unit=2, source_chapter="2.3")
)

register_equation(ncx_reversal)

"""
Single Channel Conductance - Conductance of an individual ion channel

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""

def compute_single_channel_conductance(i: float, V_m: float, E_ion: float) -> float:
    """
    Calculate single channel conductance.

    Formula: γ = i / (V_m - E_ion)

    Parameters:
    -----------
    i : float
        Single channel current (pA)
    V_m : float
        Membrane potential (mV)
    E_ion : float
        Reversal (equilibrium) potential for the ion (mV)

    Returns:
    --------
    gamma : float
        Single channel conductance (nS = pA/mV; a 1-300 pS channel = 0.001-0.3 nS)

    Typical values: 1-300 pS depending on channel type
    """
    return i / (V_m - E_ion)


# Create and register atomic equation
single_channel_conductance = create_equation(
    id="single_channel_conductance",
    output_units='nS',
    name="Single Channel Conductance",
    category=EquationCategory.MEMBRANE,
    latex=r"\gamma = \frac{i}{V_m - E_{ion}}",
    simplified="gamma = i / (V_m - E_ion)",
    description="Conductance of an individual ion channel, relating single-channel current to driving force.",
    compute_func=compute_single_channel_conductance,
    parameters=[
        Parameter(
            name="i",
            description="Single channel current",
            units="pA",
            symbol="i",
            default_value=None,
            physiological_range=(-100.0, 100.0)
        ),
        Parameter(
            name="V_m",
            description="Membrane potential",
            units="mV",
            symbol="V_m",
            default_value=None,
            physiological_range=(-100.0, 50.0)
        ),
        Parameter(
            name="E_ion",
            description="Ion reversal potential",
            units="mV",
            symbol="E_{ion}",
            default_value=None,
            physiological_range=(-100.0, 100.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(single_channel_conductance)

"""
Whole-Cell Conductance - Total conductance from population of channels

Source: Quantitative Human Physiology 3rd Edition, Unit 2
"""

def compute_whole_cell_conductance(N: float, P_open: float, gamma: float) -> float:
    """
    Calculate whole-cell conductance from channel population.

    Formula: G = N × P_open × γ

    Parameters:
    -----------
    N : float
        Number of channels in membrane
    P_open : float
        Open probability (0-1)
    gamma : float
        Single channel conductance (pS)

    Returns:
    --------
    G : float
        Total membrane conductance (pS or nS)
    """
    return N * P_open * gamma


# Create and register atomic equation
whole_cell_conductance = create_equation(
    id="whole_cell_conductance",
    output_units='pS',
    name="Whole-Cell Conductance",
    category=EquationCategory.MEMBRANE,
    latex=r"G = N \cdot P_{open} \cdot \gamma",
    simplified="G = N * P_open * gamma",
    description="Total membrane conductance for a population of ion channels with given open probability.",
    compute_func=compute_whole_cell_conductance,
    parameters=[
        Parameter(
            name="N",
            description="Number of channels",
            units="dimensionless",
            symbol="N",
            default_value=None,
            physiological_range=(1.0, 1e9)
        ),
        Parameter(
            name="P_open",
            description="Open probability",
            units="dimensionless",
            symbol="P_{open}",
            default_value=None,
            physiological_range=(0.0, 1.0)
        ),
        Parameter(
            name="gamma",
            description="Single channel conductance",
            units="pS",
            symbol=r"\gamma",
            default_value=None,
            physiological_range=(1.0, 300.0)
        ),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter="2.2")
)

register_equation(whole_cell_conductance)

__all__ = ['ficks_membrane_flux', 'goldman_flux', 'carrier_transport', 'single_channel_conductance', 'whole_cell_conductance', 'nak_pump_rate', 'ncx_reversal']


# --- coverage pass additions (Feher extraction) ---

def compute_ussing_flux_ratio(C_in, C_out, z, E_m, T_body=310.0, R=8.314, F=96485.0):
    """Ussing flux ratio equation (Feher Eqn 2.7.A1.16): signed ratio of the two
    unidirectional passive fluxes J_(i->o)/J_(o->i) of an ion across a membrane.
    C_in, C_out are the inside/outside concentrations in the same units (they cancel,
    so the result is dimensionless). z is the signed integer valence; E_m = psi_in -
    psi_out is the membrane potential in volts; T_body in K; R in J/(mol*K); F in
    C/mol. Feher's convention takes outward flux as positive, so for purely passive
    transport this signed ratio is negative; deviation from it indicates active
    transport."""
    import math
    return -(C_in / C_out) * math.exp(z * F * E_m / (R * T_body))

ussing_flux_ratio = create_equation(
    id='ussing_flux_ratio',
    output_units='dimensionless',
    name='Ussing Flux Ratio Equation',
    category=EquationCategory.MEMBRANE,
    latex='\\frac{J_{i \\to o}}{J_{o \\to i}} = -\\frac{C_i}{C_o}\\, e^{\\frac{z F E_m}{RT}}',
    simplified='J_(i->o)/J_(o->i) = -(C_in/C_out) * exp(z*F*E_m/(R*T))',
    description="Ussing flux ratio equation (Feher Appendix 2.7.A1, Eqn 2.7.A1.16): the ratio of the two unidirectional passive fluxes of an ion across a membrane, predicted from the trans-membrane concentrations and the membrane potential. If the experimentally measured unidirectional-flux ratio deviates from this value, the transport is not purely passive -- the classic Ussing test for the presence of an active transport mechanism (first used by Ussing on frog skin). The result is dimensionless; the leading minus sign follows Feher's convention that outward flux is taken as positive (so a passive ratio is negative).",
    compute_func=compute_ussing_flux_ratio,
    parameters=[
        Parameter(name='C_in', description='Intracellular (inside) ion concentration; cancels against C_out so any concentration unit may be used', units='mol/m^3', symbol='C_i', physiological_range=(0, 1000)),
        Parameter(name='C_out', description='Extracellular (outside) ion concentration; must be nonzero (appears in denominator)', units='mol/m^3', symbol='C_o', physiological_range=(0.1, 1000)),
        Parameter(name='z', description='Signed integer valence (charge number) of the ion', units='dimensionless', symbol='z', physiological_range=(-3, 3)),
        Parameter(name='E_m', description='Membrane potential, inside minus outside (psi_in - psi_out)', units='V', symbol='E_m', physiological_range=(-0.1, 0.05)),
        Parameter(name='T_body', description='Absolute temperature', units='K', symbol='T', default_value=310, physiological_range=(273.15, 320)),
        Parameter(name='R', description='Universal gas constant', units='J/(mol*K)', symbol='R', default_value=8.314),
        Parameter(name='F', description='Faraday constant', units='C/mol', symbol='F', default_value=96485),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=2, source_chapter='2.7',
                              source_section='APPENDIX 2.7.A1 DERIVATION OF THE USSING FLUX RATIO EQUATION', page_reference=None,
                              textbook_equation_number='2.7.A1.16'),
)
register_equation(ussing_flux_ratio)

try:
    __all__ += ['ussing_flux_ratio']
except NameError:
    __all__ = ['ussing_flux_ratio']

"""Thermodynamics equations - Energy transformations and equilibria.

Includes:
- Gibbs free energy
- Standard and actual free energy
- Electrochemical potential
- Nernst equation (equilibrium potential)"""

"""
Actual Free Energy - Free energy under non-standard conditions

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation, PHYSICAL_CONSTANTS
)
from scripts.index import register_equation
import numpy as np


def compute_actual_free_energy(delta_G0: float, Q: float, R: float = 8.314, T_body: float = 310.0) -> float:
    """
    Calculate actual free energy change from standard conditions.

    Formula: ΔG = ΔG° + RT ln(Q)

    Parameters:
    -----------
    delta_G0 : float - Standard free energy change (J/mol)
    Q : float - Reaction quotient (dimensionless)
    R : float - Gas constant (J/(mol·K))
    T_body : float - Body temperature (K)

    Returns:
    --------
    delta_G : float - Actual free energy change (J/mol)
    """
    return delta_G0 + R * T_body * np.log(Q)


# Create and register atomic equation
actual_free_energy = create_equation(
    id="actual_free_energy",
    output_units='J/mol',
    name="Actual Free Energy",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\Delta G = \Delta G^\circ + RT \ln(Q)",
    simplified="delta_G = delta_G0 + R*T*ln(Q)",
    description="Free energy change under actual cellular conditions - Q is reaction quotient",
    compute_func=compute_actual_free_energy,
    parameters=[
        Parameter(
            name="delta_G0",
            description="Standard free energy change",
            units="J/mol",
            symbol=r"\Delta G^\circ",
            physiological_range=(-1e6, 1e6)
        ),
        Parameter(
            name="Q",
            description="Reaction quotient",
            units="dimensionless",
            symbol="Q",
            physiological_range=(1e-10, 1e10)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"]
    ],
    depends_on=["standard_free_energy"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.4")
)

register_equation(actual_free_energy)

"""
Electrochemical Potential - Unified chemical and electrical driving forces

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_electrochemical_potential(mu_0: float, C: float, z: float, psi: float,
                                     R: float = 8.314, T_body: float = 310.0, F: float = 96485.0) -> float:
    """
    Calculate electrochemical potential.

    Formula: μ̃ = μ° + RT ln(C) + zFψ

    Parameters:
    -----------
    mu_0 : float - Standard chemical potential (J/mol)
    C : float - Concentration (M)
    z : float - Valence (charge number)
    psi : float - Electric potential (V)
    R : float - Gas constant (J/(mol·K))
    T_body : float - Body temperature (K)
    F : float - Faraday constant (C/mol)

    Returns:
    --------
    mu_tilde : float - Electrochemical potential (J/mol)
    """
    return mu_0 + R * T_body * np.log(C) + z * F * psi


# Create and register atomic equation
electrochemical_potential = create_equation(
    id="electrochemical_potential",
    output_units='J/mol',
    name="Electrochemical Potential",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\tilde{\mu} = \mu^\circ + RT \ln(C) + zF\psi",
    simplified="mu_tilde = mu_0 + R*T*ln(C) + z*F*psi",
    description="Unifies electrical and chemical driving forces - equilibrium when Δμ̃ = 0",
    compute_func=compute_electrochemical_potential,
    parameters=[
        Parameter(
            name="mu_0",
            description="Standard chemical potential",
            units="J/mol",
            symbol=r"\mu^\circ",
            physiological_range=(-1e6, 1e6)
        ),
        Parameter(
            name="C",
            description="Concentration",
            units="M",
            symbol="C",
            physiological_range=(1e-6, 1.0)
        ),
        Parameter(
            name="z",
            description="Valence (charge number)",
            units="dimensionless",
            symbol="z",
            physiological_range=(-3.0, 3.0)
        ),
        Parameter(
            name="psi",
            description="Electric potential",
            units="V",
            symbol=r"\psi",
            physiological_range=(-0.2, 0.2)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"],
        PHYSICAL_CONSTANTS["F"]
    ],
    depends_on=["gibbs_free_energy"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.5")
)

register_equation(electrochemical_potential)

"""
Gibbs Free Energy - Maximum useful work from a process

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)


def compute_gibbs_free_energy(H: float, T: float, S: float) -> float:
    """
    Calculate Gibbs free energy.

    Formula: G = H - TS

    Parameters:
    -----------
    H : float - Enthalpy (J/mol)
    T : float - Temperature (K)
    S : float - Entropy (J/(mol·K))

    Returns:
    --------
    G : float - Gibbs free energy (J/mol)
    """
    return H - T * S


def compute_gibbs_change(delta_H: float, T: float, delta_S: float) -> float:
    """
    Calculate change in Gibbs free energy.

    Formula: ΔG = ΔH - TΔS

    Parameters:
    -----------
    delta_H : float - Enthalpy change (J/mol)
    T : float - Temperature (K)
    delta_S : float - Entropy change (J/(mol·K))

    Returns:
    --------
    delta_G : float - Gibbs free energy change (J/mol)
    """
    return delta_H - T * delta_S


# Create and register atomic equation
gibbs_free_energy = create_equation(
    id="gibbs_free_energy",
    output_units='J/mol',
    name="Gibbs Free Energy",
    category=EquationCategory.FOUNDATIONS,
    latex=r"G = H - TS \quad ; \quad \Delta G = \Delta H - T\Delta S",
    simplified="G = H - T*S  ;  delta_G = delta_H - T*delta_S",
    description="Maximum useful work from a process - ΔG < 0 means spontaneous",
    compute_func=compute_gibbs_change,
    parameters=[
        Parameter(
            name="delta_H",
            description="Enthalpy change",
            units="J/mol",
            symbol=r"\Delta H",
            physiological_range=(-1e6, 1e6)
        ),
        Parameter(
            name="T",
            description="Temperature",
            units="K",
            symbol="T",
            default_value=310.0,
            physiological_range=(273.0, 320.0)
        ),
        Parameter(
            name="delta_S",
            description="Entropy change",
            units="J/(mol·K)",
            symbol=r"\Delta S",
            physiological_range=(-1000.0, 1000.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.4")
)

register_equation(gibbs_free_energy)

"""
Nernst Equation - Equilibrium potential for ions

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_nernst_potential(z: float, C_out: float, C_in: float,
                             R: float = 8.314, T_body: float = 310.0, F: float = 96485.0) -> float:
    """
    Calculate Nernst equilibrium potential for an ion.

    Formula: E = (RT/zF) ln(C_out/C_in)

    Parameters:
    -----------
    z : float - Ion valence
    C_out : float - Extracellular concentration (M)
    C_in : float - Intracellular concentration (M)
    R : float - Gas constant (J/(mol·K))
    T_body : float - Body temperature (K)
    F : float - Faraday constant (C/mol)

    Returns:
    --------
    E : float - Equilibrium potential (V)
    """
    return (R * T_body) / (z * F) * np.log(C_out / C_in) * 1000.0  # V -> mV


def compute_nernst_potential_log10(z: float, C_out: float, C_in: float, T: float = 310.0) -> float:
    """
    Calculate Nernst potential using log10 form (more convenient).

    At 37°C (310 K): E ≈ (61.5 mV/z) log₁₀(C_out/C_in)

    Parameters:
    -----------
    z : float - Ion valence
    C_out : float - Extracellular concentration (M)
    C_in : float - Intracellular concentration (M)
    T : float - Temperature (K)

    Returns:
    --------
    E : float - Equilibrium potential (V)
    """
    # At 310 K: RT/F ≈ 0.0267 V, factor of ln(10) ≈ 2.303
    RT_over_F = 8.314 * T / 96485.0
    return (RT_over_F / z) * np.log10(C_out / C_in) * 2.303


# Create and register atomic equation
nernst_equation = create_equation(
    id="nernst_equation",
    output_units='mV',
    name="Nernst Equation",
    category=EquationCategory.FOUNDATIONS,
    latex=r"E = \frac{RT}{zF} \ln\left(\frac{C_{out}}{C_{in}}\right) \approx \frac{61.5\text{ mV}}{z} \log_{10}\left(\frac{C_{out}}{C_{in}}\right)",
    simplified="E = (R*T/z*F) * ln(C_out/C_in)  or  E ≈ (61.5 mV/z) * log10(C_out/C_in)",
    description="Equilibrium potential where electrical gradient balances concentration gradient",
    compute_func=compute_nernst_potential,
    parameters=[
        Parameter(
            name="z",
            description="Ion valence",
            units="dimensionless",
            symbol="z",
            physiological_range=(-3.0, 3.0)
        ),
        Parameter(
            name="C_out",
            description="Extracellular concentration",
            units="M",
            symbol=r"C_{out}",
            physiological_range=(1e-6, 1.0)
        ),
        Parameter(
            name="C_in",
            description="Intracellular concentration",
            units="M",
            symbol=r"C_{in}",
            physiological_range=(1e-6, 1.0)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"],
        PHYSICAL_CONSTANTS["F"]
    ],
    depends_on=["electrochemical_potential"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.5")
)

register_equation(nernst_equation)

"""
Standard Free Energy - Relationship to equilibrium constant

Source: Quantitative Human Physiology 3rd Edition, Unit 1
"""


def compute_standard_free_energy(K_eq: float, R: float = 8.314, T_body: float = 310.0) -> float:
    """
    Calculate standard free energy from equilibrium constant.

    Formula: ΔG° = -RT ln(K_eq)

    Parameters:
    -----------
    K_eq : float - Equilibrium constant (dimensionless)
    R : float - Gas constant (J/(mol·K))
    T_body : float - Body temperature (K)

    Returns:
    --------
    delta_G0 : float - Standard free energy change (J/mol)
    """
    return -R * T_body * np.log(K_eq)


# Create and register atomic equation
standard_free_energy = create_equation(
    id="standard_free_energy",
    output_units='J/mol',
    name="Standard Free Energy",
    category=EquationCategory.FOUNDATIONS,
    latex=r"\Delta G^\circ = -RT \ln(K_{eq})",
    simplified="delta_G0 = -R*T*ln(K_eq)",
    description="Standard free energy of a reaction, delta_G0 = -RT ln(Keq). Evaluated at T_body=310 K (37C) by default to match the package body-temperature convention; pass T=298 for the 25C thermodynamic standard state. Concentrations at 1 M, 1 atm.",
    compute_func=compute_standard_free_energy,
    parameters=[
        Parameter(
            name="K_eq",
            description="Equilibrium constant",
            units="dimensionless",
            symbol=r"K_{eq}",
            physiological_range=(1e-10, 1e10)
        ),
        PHYSICAL_CONSTANTS["R"],
        PHYSICAL_CONSTANTS["T_body"]
    ],
    depends_on=["gibbs_free_energy"],
    metadata=EquationMetadata(source_unit=1, source_chapter="1.4")
)

register_equation(standard_free_energy)

__all__ = ['gibbs_free_energy', 'standard_free_energy', 'actual_free_energy', 'electrochemical_potential', 'nernst_equation']


# --- coverage pass additions (Feher extraction) ---

def compute_redox_free_energy(n, delta_E, F=96485.0):
    """Free energy change of a redox reaction: delta_G = -n*F*delta_E (J/mol). Feher Unit 1 Eq 1.7.38. n = electrons transferred per reaction (dimensionless), delta_E = difference in reduction potentials between the two half-cells (V, = E_acceptor - E_donor), F = Faraday constant (C/mol). Returns delta_G in J/mol (SI: C/mol * V = J/mol)."""
    return -n * F * delta_E

redox_free_energy = create_equation(
    id='redox_free_energy',
    output_units='J/mol',
    name='Redox Reaction Free Energy',
    category=EquationCategory.FOUNDATIONS,
    latex='\\Delta G = -n F \\Delta E',
    simplified='delta_G = -n*F*delta_E',
    description='Free energy change of an oxidation-reduction (redox) reaction computed from the reduction-potential difference of its two half-cells: delta_G = -n*F*delta_E, where n is the number of electrons transferred per reaction, F is the Faraday constant, and delta_E is the difference in reduction potentials (E_acceptor - E_donor). Links the electrical driving force of electron transfer to Gibbs free energy: a positive delta_E yields a spontaneous (negative delta_G) reaction. Governs the energetics of the mitochondrial electron transport chain (e.g. NADH -> CoQ -> cytochrome c -> O2) and other bioenergetic redox couples. Feher builds it from delta_G = z*F*delta_E (Eq 1.7.36) -> delta_G = -F*delta_E for a single electron (Eq 1.7.37) -> delta_G = -n*F*delta_E for n electrons per reaction (Eq 1.7.38), and reiterates it in the chapter Summary and Review Questions as THE relation between free energy change and reduction potential.',
    compute_func=compute_redox_free_energy,
    parameters=[
        Parameter(name='n', description='Number of electrons transferred per reaction', units='dimensionless', symbol='n', physiological_range=(1, 4)),
        Parameter(name='delta_E', description='Difference in reduction potentials between the two half-cells (E_acceptor - E_donor)', units='V', symbol='\\Delta E', physiological_range=(-1.5, 1.5)),
        Parameter(name='F', description='Faraday constant', units='C/mol', symbol='F', default_value=96485),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=1, source_chapter='1.7',
                              source_section='OXIDATION-REDUCTION REACTIONS CAN DO WORK', page_reference=None,
                              textbook_equation_number='1.7.38'),
)
register_equation(redox_free_energy)


def compute_body_energy_balance(E_food, E_heat, E_work, E_feces=0.0, E_urine=0.0, E_drink=0.0, E_inspired_air=0.0, E_expired_air=0.0, E_exfoliation=0.0):
    """Change in whole-body energy stores by conservation of energy (Feher 1.1,
    'Living beings transform matter and energy while obeying conservation laws';
    the Atwater / indirect-calorimetry first-law basis).

    Delta_E_body = (E_food + E_drink + E_inspired_air)
                   - (E_feces + E_urine + E_expired_air + E_exfoliation + E_heat + E_work)

    All terms are metabolizable-energy fluxes in consistent units (e.g. kcal/day).
    Positive Delta_E_body = net storage (weight gain); negative = net mobilisation.
    """
    E_in = E_food + E_drink + E_inspired_air
    E_out = E_feces + E_urine + E_expired_air + E_exfoliation + E_heat + E_work
    return E_in - E_out

body_energy_balance = create_equation(
    id='body_energy_balance',
    output_units='kcal/day',
    name='Whole-Body Energy Balance',
    category=EquationCategory.FOUNDATIONS,
    latex='E_{\\mathrm{in}} = E_{\\mathrm{out}} + \\Delta E_{\\mathrm{body}}\\,;\\quad E_{\\mathrm{food}}+E_{\\mathrm{drink}}+E_{\\mathrm{inspired\\,air}} = E_{\\mathrm{feces}}+E_{\\mathrm{urine}}+E_{\\mathrm{expired\\,air}}+E_{\\mathrm{exfoliation}}+E_{\\mathrm{heat}}+E_{\\mathrm{work}}+\\Delta E_{\\mathrm{body}}',
    simplified='dE_body = (E_food + E_drink + E_inspired_air) - (E_feces + E_urine + E_expired_air + E_exfoliation + E_heat + E_work)',
    description='Whole-body energy balance: conservation of energy (first law) applied to the body, the Atwater indirect-calorimetry basis. Metabolizable energy entering the body (food, drink, inspired air) equals energy leaving (feces, urine, expired air, exfoliation, heat, external work) plus the change in body energy stores. Positive Delta_E_body indicates net energy storage (fat/glycogen deposition, growth); negative indicates net mobilisation of stores. Used in energy-balance, nutrition, and indirect-calorimetry problems.',
    compute_func=compute_body_energy_balance,
    parameters=[
        Parameter(name='E_food', description='Metabolizable energy absorbed from food', units='kcal/day', symbol='E_{food}', physiological_range=(0, 6000)),
        Parameter(name='E_heat', description='Energy dissipated as heat (internal work degraded to heat)', units='kcal/day', symbol='E_{heat}', physiological_range=(0, 5000)),
        Parameter(name='E_work', description='Energy expended as external mechanical work', units='kcal/day', symbol='E_{work}', physiological_range=(0, 3000)),
        Parameter(name='E_feces', description='Metabolizable energy lost in feces', units='kcal/day', symbol='E_{feces}', default_value=0, physiological_range=(0, 1000)),
        Parameter(name='E_urine', description='Metabolizable energy lost in urine', units='kcal/day', symbol='E_{urine}', default_value=0, physiological_range=(0, 1000)),
        Parameter(name='E_drink', description='Metabolizable energy from drink', units='kcal/day', symbol='E_{drink}', default_value=0, physiological_range=(0, 3000)),
        Parameter(name='E_inspired_air', description='Energy content of inspired air (usually negligible)', units='kcal/day', symbol='E_{inspired\\,air}', default_value=0, physiological_range=(0, 100)),
        Parameter(name='E_expired_air', description='Metabolizable energy lost in expired air', units='kcal/day', symbol='E_{expired\\,air}', default_value=0, physiological_range=(0, 500)),
        Parameter(name='E_exfoliation', description='Energy lost via exfoliation / shed cells and secretions', units='kcal/day', symbol='E_{exfoliation}', default_value=0, physiological_range=(0, 100)),
    ],
    depends_on=[],
    produces='ΔE_body',
    metadata=EquationMetadata(source_unit=1, source_chapter='1.1',
                              source_section='LIVING BEINGS TRANSFORM MATTER AND ENERGY WHILE OBEYING CONSERVATION LAWS', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(body_energy_balance)


def compute_ideal_gas_law(n, T, V, R=8.314):
    """Ideal gas law solved for pressure: P = nRT/V. Feher 3rd ed. Unit 6, 6.1, section 'CHANGES IN LUNG VOLUMES PRODUCE THE PRESSURE DIFFERENCES THAT DRIVE AIR MOVEMENT'. SI-consistent: n in mol, T in K, V in m^3, R in J/(mol K) -> P in Pa."""
    return n * R * T / V

ideal_gas_law = create_equation(
    id='ideal_gas_law',
    output_units='Pa',
    name='Ideal Gas Law',
    category=EquationCategory.FOUNDATIONS,
    latex='PV = nRT',
    simplified='P = n*R*T/V   (from P*V = n*R*T)',
    description='The ideal gas law relates the pressure, volume, moles, and absolute temperature of an ideal gas of constant composition. Implemented here solved for pressure (P = nRT/V). Foundational physical relation underpinning respiratory physiology: the inverse pressure-volume relationship drives pulmonary ventilation (expanding thoracic/lung volume lowers gas pressure so air rushes in), and it governs body-temperature/ambient gas-volume corrections (BTPS/STPD/ATPS) used across gas-transport calculations. Cross-domain foundations relation used by respiratory physiology.',
    compute_func=compute_ideal_gas_law,
    parameters=[
        Parameter(name='n', description='Number of moles of gas', units='mol', symbol='n', physiological_range=(0, 10000)),
        Parameter(name='T', description='Absolute temperature', units='K', symbol='T', default_value=310, physiological_range=(0, 1000)),
        Parameter(name='V', description='Volume of the gas', units='m^3', symbol='V', physiological_range=(1e-09, 1)),
        Parameter(name='R', description='Universal gas constant', units='J/(mol*K)', symbol='R', default_value=8.314),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=6, source_chapter='6.1',
                              source_section='CHANGES IN LUNG VOLUMES PRODUCE THE PRESSURE DIFFERENCES THAT DRIVE AIR MOVEMENT', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(ideal_gas_law)

try:
    __all__ += ['redox_free_energy', 'body_energy_balance', 'ideal_gas_law']
except NameError:
    __all__ = ['redox_free_energy', 'body_energy_balance', 'ideal_gas_law']


# --- coverage pass 2 (residual reconsideration) ---

def compute_enthalpy(E, P, V):
    """Enthalpy H = E + P*V (Feher 1.4): the thermodynamic potential defined so that, at constant pressure, its change equals the heat exchanged (delta_H = q_p). E = internal energy (J), P = pressure (Pa), V = volume (m^3); returns H (J). Basis for reaction enthalpies and indirect/direct calorimetry in physiology."""
    return E + P * V

enthalpy = create_equation(
    id='enthalpy',
    output_units='J',
    name='Enthalpy',
    category=EquationCategory.FOUNDATIONS,
    latex='H = E + PV',
    simplified='H = E + P*V',
    description='Enthalpy: internal energy plus the pressure-volume product. Defined so that at constant pressure the change in enthalpy equals the heat absorbed or released (delta_H = q_p), which makes it the natural energy bookkeeping quantity for reactions and metabolism measured by calorimetry at atmospheric pressure. Feher section 1.4 (Chemical Energy and Intermolecular Forces).',
    compute_func=compute_enthalpy,
    parameters=[
        Parameter(name='E', description='Internal energy of the system', units='J', symbol='E'),
        Parameter(name='P', description='Pressure', units='Pa', symbol='P', physiological_range=(0.0, 1000000000.0)),
        Parameter(name='V', description='Volume', units='m^3', symbol='V', physiological_range=(0.0, 1000.0)),
    ],
    depends_on=[],
    produces='H',
    metadata=EquationMetadata(source_unit=1, source_chapter='1.4',
                              source_section='Chemical energy and the first law of thermodynamics', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(enthalpy)

try:
    __all__ += ['enthalpy']
except NameError:
    __all__ = ['enthalpy']

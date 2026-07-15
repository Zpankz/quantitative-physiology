"""Respiratory mechanics equations."""

"""Airway Resistance (Poiseuille's Law) equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation
import math


def compute_airway_resistance(eta: float, L: float, r: float) -> float:
    """
    Calculate airway resistance using Poiseuille's law.

    R = 8ηL/(πr⁴)

    Parameters
    ----------
    eta : float
        Viscosity (Pa·s)
    L : float
        Length (m)
    r : float
        Radius (m)

    Returns
    -------
    float
        Resistance (Pa·s/m³)
    """
    return (8.0 * eta * L) / (math.pi * r**4)


# Create equation
airway_resistance = create_equation(
    id="airway_resistance",
    output_units='Pa*s/m^3',
    name="Airway Resistance (Poiseuille)",
    category=EquationCategory.RESPIRATORY,
    latex=r"R = \frac{8\eta L}{\pi r^4}",
    simplified="R = 8ηL/(πr⁴)",
    description="Resistance to airflow in cylindrical airways - highly sensitive to radius",
    compute_func=compute_airway_resistance,
    parameters=[
        Parameter(
            name="eta",
            description="Air viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=1.8e-5,
            physiological_range=(1.5e-5, 2.0e-5)
        ),
        Parameter(
            name="L",
            description="Airway length",
            units="m",
            symbol="L",
            physiological_range=(0.001, 0.1)
        ),
        Parameter(
            name="r",
            description="Airway radius",
            units="m",
            symbol="r",
            physiological_range=(0.0001, 0.01)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(airway_resistance)

"""Compliance equation."""


def compute_compliance(delta_V: float, delta_P: float) -> float:
    """
    Calculate compliance (change in volume per unit pressure).

    C = ΔV / ΔP

    Parameters
    ----------
    delta_V : float
        Change in volume (L)
    delta_P : float
        Change in pressure (cmH2O)

    Returns
    -------
    float
        Compliance (L/cmH2O)
    """
    return delta_V / delta_P


# Create equation
compliance = create_equation(
    id="compliance",
    output_units='L/cmH2O',
    name="Compliance",
    category=EquationCategory.RESPIRATORY,
    latex=r"C = \frac{\Delta V}{\Delta P}",
    simplified="C = ΔV / ΔP",
    description="Measure of lung distensibility - change in volume per unit pressure change",
    compute_func=compute_compliance,
    parameters=[
        Parameter(
            name="delta_V",
            description="Change in volume",
            units="L",
            symbol=r"\Delta V",
            physiological_range=(0.0, 5.0)
        ),
        Parameter(
            name="delta_P",
            description="Change in pressure",
            units="cmH2O",
            symbol=r"\Delta P",
            physiological_range=(0.0, 30.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(compliance)

"""Elastance equation."""


def compute_elastance(C: float) -> float:
    """
    Calculate elastance (inverse of compliance).

    E = 1/C = ΔP/ΔV

    Parameters
    ----------
    C : float
        Compliance (L/cmH2O)

    Returns
    -------
    float
        Elastance (cmH2O/L)
    """
    return 1.0 / C


# Create equation
elastance = create_equation(
    id="elastance",
    output_units='cmH2O/L',
    name="Elastance",
    category=EquationCategory.RESPIRATORY,
    latex=r"E = \frac{1}{C} = \frac{\Delta P}{\Delta V}",
    simplified="E = 1/C = ΔP/ΔV",
    description="Elastic recoil tendency - inverse of compliance",
    compute_func=compute_elastance,
    parameters=[
        Parameter(
            name="C",
            description="Compliance",
            units="L/cmH2O",
            symbol="C",
            default_value=0.2,
            physiological_range=(0.05, 0.4)
        )
    ],
    depends_on=["compliance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(elastance)

"""Exponential Emptying equation."""


def compute_exponential_emptying(V0: float, t: float, tau: float) -> float:
    """
    Calculate lung volume during passive expiration.

    V(t) = V₀ × e^(-t/τ)

    Parameters
    ----------
    V0 : float
        Initial volume (L)
    t : float
        Time (s)
    tau : float
        Time constant (s)

    Returns
    -------
    float
        Volume at time t (L)
    """
    return V0 * math.exp(-t / tau)


# Create equation
exponential_emptying = create_equation(
    id="exponential_emptying",
    output_units='L',
    name="Exponential Emptying",
    category=EquationCategory.RESPIRATORY,
    latex=r"V(t) = V_0 \times e^{-t/\tau}",
    simplified="V(t) = V₀ × e^(-t/τ)",
    description="Volume decay during passive expiration",
    compute_func=compute_exponential_emptying,
    parameters=[
        Parameter(
            name="V0",
            description="Initial volume",
            units="L",
            symbol="V_0",
            physiological_range=(0.5, 6.0)
        ),
        Parameter(
            name="t",
            description="Time",
            units="s",
            symbol="t",
            physiological_range=(0.0, 10.0)
        ),
        Parameter(
            name="tau",
            description="Time constant",
            units="s",
            symbol=r"\tau",
            default_value=0.5,
            physiological_range=(0.1, 2.0)
        )
    ],
    depends_on=["respiratory_time_constant"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(exponential_emptying)

"""Law of Laplace for Alveolar Pressure."""


def compute_laplace_pressure(T: float, r: float) -> float:
    """
    Calculate transmural pressure in a sphere (Law of Laplace).

    ΔP = 2T/r

    Parameters
    ----------
    T : float
        Surface tension (mN/m)
    r : float
        Radius (m)

    Returns
    -------
    float
        Transmural pressure (Pa)
    """
    return 2.0 * (T * 1e-3) / r  # T mN/m -> N/m, /r(m) -> Pa


# Create equation
laplace_pressure = create_equation(
    id="laplace_pressure",  # raw output mN/m^2 (milliPa); x1e-3 for Pa, /98.07 for cmH2O
    output_units='Pa',
    name="Law of Laplace (Sphere)",
    category=EquationCategory.RESPIRATORY,
    latex=r"\Delta P = \frac{2T}{r}",
    simplified="ΔP = 2T/r",
    description="Pressure difference across a spherical surface due to surface tension",
    compute_func=compute_laplace_pressure,
    parameters=[
        Parameter(
            name="T",
            description="Surface tension",
            units="mN/m",
            symbol="T",
            default_value=25.0,
            physiological_range=(10.0, 70.0)
        ),
        Parameter(
            name="r",
            description="Radius of sphere",
            units="m",
            symbol="r",
            physiological_range=(0.00005, 0.0005)  # 50-500 μm
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(laplace_pressure)

"""Pressure-Flow Relationship equation."""


def compute_pressure_flow(delta_P: float, R: float) -> float:
    """
    Calculate airflow from pressure gradient and resistance.

    V̇ = ΔP/R

    Parameters
    ----------
    delta_P : float
        Pressure gradient (cmH2O)
    R : float
        Airway resistance (cmH2O/(L/s))

    Returns
    -------
    float
        Flow rate (L/s)
    """
    return delta_P / R


# Create equation
pressure_flow = create_equation(
    id="pressure_flow",
    output_units='L/s',
    name="Pressure-Flow Relationship",
    category=EquationCategory.RESPIRATORY,
    latex=r"\dot{V} = \frac{\Delta P}{R}",
    simplified="V̇ = ΔP/R",
    description="Airflow driven by pressure gradient and limited by resistance",
    compute_func=compute_pressure_flow,
    parameters=[
        Parameter(
            name="delta_P",
            description="Pressure gradient",
            units="cmH2O",
            symbol=r"\Delta P",
            physiological_range=(-20.0, 20.0)
        ),
        Parameter(
            name="R",
            description="Airway resistance",
            units="cmH2O/(L/s)",
            symbol="R",
            default_value=1.5,
            physiological_range=(0.5, 5.0)
        )
    ],
    depends_on=["airway_resistance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(pressure_flow)

"""Reynolds Number equation."""


def compute_reynolds_number(rho: float, v: float, d: float, eta: float) -> float:
    """
    Calculate Reynolds number to determine flow pattern.

    Re = ρvd/η

    Parameters
    ----------
    rho : float
        Fluid density (kg/m³)
    v : float
        Velocity (m/s)
    d : float
        Characteristic diameter (m)
    eta : float
        Viscosity (Pa·s)

    Returns
    -------
    float
        Reynolds number (dimensionless)
    """
    return (rho * v * d) / eta


# Create equation
reynolds_number = create_equation(
    id="reynolds_number_airway",
    output_units='dimensionless',
    name="Reynolds Number (Airway Flow)",
    category=EquationCategory.RESPIRATORY,
    latex=r"Re = \frac{\rho v d}{\eta}",
    simplified="Re = ρvd/η",
    description="Dimensionless number determining laminar (Re<2000) vs turbulent (Re>2000) flow",
    compute_func=compute_reynolds_number,
    parameters=[
        Parameter(
            name="rho",
            description="Air density",
            units="kg/m³",
            symbol=r"\rho",
            default_value=1.2,
            physiological_range=(1.0, 1.3)
        ),
        Parameter(
            name="v",
            description="Flow velocity",
            units="m/s",
            symbol="v",
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="d",
            description="Airway diameter",
            units="m",
            symbol="d",
            physiological_range=(0.0002, 0.02)
        ),
        Parameter(
            name="eta",
            description="Air viscosity",
            units="Pa·s",
            symbol=r"\eta",
            default_value=1.8e-5,
            physiological_range=(1.5e-5, 2.0e-5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(reynolds_number)

"""Time Constant equation."""


def compute_time_constant(R: float, C: float) -> float:
    """
    Calculate time constant for exponential filling/emptying.

    τ = R × C

    Parameters
    ----------
    R : float
        Resistance (cmH2O/(L/s))
    C : float
        Compliance (L/cmH2O)

    Returns
    -------
    float
        Time constant (s)
    """
    return R * C


# Create equation
time_constant = create_equation(
    id="respiratory_time_constant",
    output_units='s',
    name="Respiratory Time Constant (τ = RC)",
    category=EquationCategory.RESPIRATORY,
    latex=r"\tau = R \times C",
    simplified="τ = R × C",
    description="Time constant for exponential lung filling/emptying (3τ ≈ 95% complete)",
    compute_func=compute_time_constant,
    parameters=[
        Parameter(
            name="R",
            description="Airway resistance",
            units="cmH2O/(L/s)",
            symbol="R",
            default_value=1.5,
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="C",
            description="Compliance",
            units="L/cmH2O",
            symbol="C",
            default_value=0.1,
            physiological_range=(0.05, 0.3)
        )
    ],
    depends_on=["airway_resistance", "compliance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(time_constant)

"""Total Respiratory System Compliance equation."""


def compute_total_compliance(C_L: float, C_CW: float) -> float:
    """
    Calculate total respiratory system compliance (series combination).

    1/C_RS = 1/C_L + 1/C_CW

    Parameters
    ----------
    C_L : float
        Lung compliance (L/cmH2O)
    C_CW : float
        Chest wall compliance (L/cmH2O)

    Returns
    -------
    float
        Total respiratory system compliance (L/cmH2O)
    """
    return 1.0 / (1.0/C_L + 1.0/C_CW)


# Create equation
total_compliance = create_equation(
    id="total_compliance",
    output_units='L/cmH2O',
    name="Total Respiratory System Compliance",
    category=EquationCategory.RESPIRATORY,
    latex=r"\frac{1}{C_{RS}} = \frac{1}{C_L} + \frac{1}{C_{CW}}",
    simplified="1/C_RS = 1/C_L + 1/C_CW",
    description="Combined compliance of lung and chest wall in series",
    compute_func=compute_total_compliance,
    parameters=[
        Parameter(
            name="C_L",
            description="Lung compliance",
            units="L/cmH2O",
            symbol="C_L",
            default_value=0.2,
            physiological_range=(0.1, 0.3)
        ),
        Parameter(
            name="C_CW",
            description="Chest wall compliance",
            units="L/cmH2O",
            symbol="C_{CW}",
            default_value=0.2,
            physiological_range=(0.1, 0.3)
        )
    ],
    depends_on=["compliance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(total_compliance)

"""Total Respiratory System Elastance equation."""


def compute_total_elastance(E_L: float, E_CW: float) -> float:
    """
    Calculate total respiratory system elastance (series addition).

    E_RS = E_L + E_CW

    Parameters
    ----------
    E_L : float
        Lung elastance (cmH2O/L)
    E_CW : float
        Chest wall elastance (cmH2O/L)

    Returns
    -------
    float
        Total respiratory system elastance (cmH2O/L)
    """
    return E_L + E_CW


# Create equation
total_elastance = create_equation(
    id="total_elastance",
    output_units='cmH2O/L',
    name="Total Respiratory System Elastance",
    category=EquationCategory.RESPIRATORY,
    latex=r"E_{RS} = E_L + E_{CW}",
    simplified="E_RS = E_L + E_CW",
    description="Combined elastance of lung and chest wall in series",
    compute_func=compute_total_elastance,
    parameters=[
        Parameter(
            name="E_L",
            description="Lung elastance",
            units="cmH2O/L",
            symbol="E_L",
            default_value=5.0,
            physiological_range=(3.0, 10.0)
        ),
        Parameter(
            name="E_CW",
            description="Chest wall elastance",
            units="cmH2O/L",
            symbol="E_{CW}",
            default_value=5.0,
            physiological_range=(3.0, 10.0)
        )
    ],
    depends_on=["elastance"],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(total_elastance)

"""Transmural Pressure equation."""


def compute_transmural_pressure(P_alv: float, P_pl: float) -> float:
    """
    Calculate transmural (transpulmonary) pressure.

    P_TM = P_alv - P_pl

    Parameters
    ----------
    P_alv : float
        Alveolar pressure (cmH2O)
    P_pl : float
        Pleural pressure (cmH2O)

    Returns
    -------
    float
        Transmural pressure (cmH2O)
    """
    return P_alv - P_pl


# Create equation
transmural_pressure = create_equation(
    id="transmural_pressure",
    output_units='cmH2O',
    name="Transmural Pressure",
    category=EquationCategory.RESPIRATORY,
    latex=r"P_{TM} = P_{alv} - P_{pl}",
    simplified="P_TM = P_alv - P_pl",
    description="Pressure difference across lung wall driving lung expansion",
    compute_func=compute_transmural_pressure,
    parameters=[
        Parameter(
            name="P_alv",
            description="Alveolar pressure",
            units="cmH2O",
            symbol="P_{alv}",
            default_value=0.0,
            physiological_range=(-10.0, 10.0)
        ),
        Parameter(
            name="P_pl",
            description="Pleural pressure",
            units="cmH2O",
            symbol="P_{pl}",
            default_value=-5.0,
            physiological_range=(-10.0, 0.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=6,
        source_chapter="6.2"
    )
)

# Register in global index
register_equation(transmural_pressure)

__all__ = ['transmural_pressure', 'compliance', 'total_compliance', 'elastance', 'total_elastance', 'laplace_pressure', 'airway_resistance', 'pressure_flow', 'reynolds_number', 'time_constant', 'exponential_emptying']


# --- coverage pass additions (Feher extraction) ---

def compute_rohrer_equation(K1, K2, Q_V):
    """Rohrer equation (Feher 6.2, eq 6.2.10): total driving pressure difference across the airways as the sum of a laminar (Ohmic/Poiseuille) term linear in flow and a turbulent term proportional to the square of flow. delta_P = K1*Q_V + K2*Q_V**2. Units: K1 [cmH2O/(L/s)], K2 [cmH2O/(L/s)^2], Q_V [L/s] -> delta_P [cmH2O]."""
    return K1 * Q_V + K2 * Q_V ** 2

rohrer_equation = create_equation(
    id='rohrer_equation',
    output_units='cmH2O',
    name='Rohrer Equation',
    category=EquationCategory.RESPIRATORY,
    latex='\\Delta P = K_1 Q_V + K_2 Q_V^2',
    simplified='delta_P = K1*Q_V + K2*Q_V^2',
    description='Rohrer equation for overall airway resistance: the pressure difference driving airflow is the sum of a laminar term (K1*Q_V, Ohmic/Poiseuille) and a turbulent term (K2*Q_V^2). Because turbulent airways add in series with laminar airways in the tracheobronchial tree, the total airway resistance R = delta_P/Q_V = K1 + K2*Q_V is flow-dependent rather than constant, rising as flow increases and a greater fraction of the airways become turbulent. Standard empirical description of overall airway resistance in respiratory mechanics.',
    compute_func=compute_rohrer_equation,
    parameters=[
        Parameter(name='K1', description='Laminar (Ohmic/Poiseuille) airway resistance coefficient; equals total airway resistance in the low-flow, purely laminar limit', units='cmH2O/(L/s)', symbol='K_1', default_value=1.5, physiological_range=(0.5, 5)),
        Parameter(name='K2', description='Turbulent flow coefficient relating pressure to the square of airflow; not itself a resistance because the relation is non-Ohmic', units='cmH2O/(L/s)^2', symbol='K_2', default_value=0.5, physiological_range=(0, 3)),
        Parameter(name='Q_V', description='Volumetric airflow rate through the airways', units='L/s', symbol='Q_V', default_value=2, physiological_range=(0, 12)),
    ],
    depends_on=[],
    produces='delta_P',
    metadata=EquationMetadata(source_unit=6, source_chapter='6.2',
                              source_section='TURBULENT AND LAMINAR FLOW RESULT IN SERIES RESISTANCES THAT ADD', page_reference=None,
                              textbook_equation_number='6.2.10'),
)
register_equation(rohrer_equation)


def compute_fev1_fvc_ratio(FEV1, FVC):
    """FEV1/FVC ratio, Feher 6.2 'Spirometry also provides a clinically useful measure of airway resistance': forced expiratory volume in 1 s (FEV1, L) normalized by forced vital capacity (FVC, L). Dimensionless spirometric obstruction index; normally >0.80, reduced when airway resistance is abnormally high. Both inputs are raw spirometric volumes; output in the same units cancels to dimensionless."""
    return FEV1 / FVC

fev1_fvc_ratio = create_equation(
    id='fev1_fvc_ratio',
    output_units='dimensionless',
    name='FEV1/FVC Ratio',
    category=EquationCategory.RESPIRATORY,
    latex='\\mathrm{FEV_1/FVC} = \\frac{\\mathrm{FEV}_1}{\\mathrm{FVC}}',
    simplified='FEV1/FVC',
    description="Ratio of forced expiratory volume in 1 second to forced vital capacity: a dimensionless spirometric index of airway resistance / airflow obstruction. Normally greater than 0.80 in healthy adults; a value significantly below this indicates abnormally high airway resistance (obstructive airway disease, e.g. COPD/asthma). Feher normalizes the absolute FEV1 by FVC because absolute FEV1 varies with FVC. Feher Unit 6, section 6.2 ('Spirometry also provides a clinically useful measure of airway resistance').",
    compute_func=compute_fev1_fvc_ratio,
    parameters=[
        Parameter(name='FEV1', description='Forced expiratory volume in the first 1 second of a forced maximal expiration', units='L', symbol='FEV_1', default_value=4, physiological_range=(0.5, 6)),
        Parameter(name='FVC', description='Forced vital capacity: total volume expired during a forced maximal expiration (Feher treats FVC as approximately equal to VC)', units='L', symbol='FVC', default_value=5, physiological_range=(1, 7)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=6, source_chapter='6.2',
                              source_section='SPIROMETRY ALSO PROVIDES A CLINICALLY USEFUL MEASURE OF AIRWAY RESISTANCE', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(fev1_fvc_ratio)

try:
    __all__ += ['rohrer_equation', 'fev1_fvc_ratio']
except NameError:
    __all__ = ['rohrer_equation', 'fev1_fvc_ratio']


# --- clinical additions (CICM, beyond Feher) ---

def compute_driving_pressure(Pplat, PEEP):
    """Driving pressure = plateau pressure - PEEP (cmH2O). Best ventilator predictor of ARDS mortality; target <15."""
    return Pplat - PEEP

driving_pressure = create_equation(
    id='driving_pressure',
    output_units='cmH2O',
    name='Respiratory Driving Pressure',
    category=EquationCategory.RESPIRATORY,
    latex='\\Delta P = P_{plat} - PEEP',
    simplified='dP = Pplat - PEEP',
    description='Tidal cyclic distending pressure of the respiratory system; the strongest ventilator variable associated with ARDS mortality (target < 15 cmH2O).',
    compute_func=compute_driving_pressure,
    parameters=[
        Parameter(name='Pplat', description='End-inspiratory plateau pressure', units='cmH2O', symbol='P_plat', physiological_range=(5, 45)),
        Parameter(name='PEEP', description='Positive end-expiratory pressure', units='cmH2O', symbol='PEEP', physiological_range=(0, 25)),
    ],
    depends_on=[],
    produces='dP_resp',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(driving_pressure)


def compute_static_compliance(VT, Pplat, PEEP):
    """Static compliance = tidal volume / driving pressure = VT/(Pplat-PEEP) (mL/cmH2O). Normal ventilated ~50-100."""
    return VT / (Pplat - PEEP)

static_compliance = create_equation(
    id='static_compliance',
    output_units='mL/cmH2O',
    name='Static Respiratory Compliance',
    category=EquationCategory.RESPIRATORY,
    latex='C_{stat} = \\frac{V_T}{P_{plat}-PEEP}',
    simplified='C_stat = VT/(Pplat-PEEP)',
    description='Static compliance of the respiratory system: tidal volume delivered per unit driving pressure. Low values indicate stiff lungs (ARDS, fibrosis, oedema).',
    compute_func=compute_static_compliance,
    parameters=[
        Parameter(name='VT', description='Tidal volume', units='mL', symbol='V_T', physiological_range=(200, 800)),
        Parameter(name='Pplat', description='Plateau pressure', units='cmH2O', symbol='P_plat', physiological_range=(5, 45)),
        Parameter(name='PEEP', description='PEEP', units='cmH2O', symbol='PEEP', physiological_range=(0, 25)),
    ],
    depends_on=[],
    produces='C_stat',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(static_compliance)

try:
    __all__ += ['driving_pressure', 'static_compliance']
except NameError:
    __all__ = ['driving_pressure', 'static_compliance']


# --- review-add 2026-07-15 ---
def compute_work_of_breathing_elastic(delta_P: float, VT: float) -> float:
    """Elastic work of one breath, W_el = 0.5 * delta_P * VT
    (triangle area on the P-V diagram)."""
    return 0.5 * delta_P * VT

work_of_breathing_elastic_equation = create_equation(
    id='work_of_breathing_elastic',
    name='Elastic Work of Breathing',
    category=EquationCategory.RESPIRATORY,
    latex=r'W_{el} = \\tfrac{1}{2}\\,\\Delta P\\, V_T',
    simplified='W_el = 0.5 * delta_P * VT',
    description='Elastic component of the work of breathing: triangular area under the static P-V curve for one tidal breath. Resistive work adds on the same axes.',
    compute_func=compute_work_of_breathing_elastic,
    output_units='L*cmH2O',
    parameters=[
        Parameter(name='delta_P', description='Elastic pressure swing', units='cmH2O', symbol='dP', physiological_range=(1, 40)),
        Parameter(name='VT', description='Tidal volume', units='L', symbol='VT', physiological_range=(0.2, 1.5)),
    ],
    metadata=EquationMetadata(source_unit=6, source_chapter='6.4'),
)
register_equation(work_of_breathing_elastic_equation)


# --- backlog-complete-add 2026-07-15 ---
def compute_dynamic_compliance(VT: float, PIP: float, PEEP: float) -> float:
    """Dynamic respiratory-system compliance Cdyn = VT / (PIP - PEEP)."""
    return VT / (PIP - PEEP)

dynamic_compliance_equation = create_equation(
    id="dynamic_compliance", name="Dynamic Respiratory Compliance",
    category=EquationCategory.RESPIRATORY,
    latex=r"C_{dyn} = \frac{V_T}{PIP - PEEP}", simplified="Cdyn = VT / (PIP - PEEP)",
    description="Dynamic compliance from tidal volume and the peak-to-PEEP pressure difference; lower than static (includes airway resistance). VT mL, pressures cmH2O.",
    compute_func=compute_dynamic_compliance, output_units="mL/cmH2O",
    parameters=[Parameter(name="VT", description="Tidal volume", units="mL", symbol="VT", physiological_range=(200, 800)),
                Parameter(name="PIP", description="Peak inspiratory pressure", units="cmH2O", symbol="PIP", physiological_range=(10, 60)),
                Parameter(name="PEEP", description="Positive end-expiratory pressure", units="cmH2O", symbol="PEEP", physiological_range=(0, 20))],
    metadata=EquationMetadata(source_unit=6, source_chapter="6.4"),
)
register_equation(dynamic_compliance_equation)

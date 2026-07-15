"""Hemodynamics and vascular mechanics equations."""

"""Bramwell-Hill equation for pulse wave velocity."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_bramwell_hill(V: float, dP: float, dV: float, rho: float = 1060.0) -> float:
    """
    Calculate pulse wave velocity using Bramwell-Hill equation.

    Parameters
    ----------
    V : float
        Volume (mL)
    dP : float
        Pressure change (mmHg)
    dV : float
        Volume change (mL)
    rho : float, optional
        Blood density (kg/m³, default: 1060)

    Returns
    -------
    float
        Pulse wave velocity (m/s)
    """
    # Convert mmHg to Pa: 1 mmHg = 133.322 Pa
    # Convert mL to m³: 1 mL = 1e-6 m³
    dP_Pa = dP * 133.322
    V_m3 = V * 1e-6
    dV_m3 = dV * 1e-6

    return np.sqrt((V_m3 * dP_Pa) / (rho * dV_m3))


bramwell_hill = create_equation(
    id="bramwell_hill_pwv",
    output_units='m/s',
    name="Bramwell-Hill Pulse Wave Velocity",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{PWV} = \sqrt{\frac{V \, dP}{\rho \, dV}} = \sqrt{\frac{1}{\rho C_A}}",
    simplified="PWV = √(V·dP / ρ·dV)",
    description="Pulse wave velocity from arterial compliance",
    compute_func=compute_bramwell_hill,
    parameters=[
        Parameter(
            name="V",
            description="Arterial volume",
            units="mL",
            symbol="V",
            physiological_range=(500.0, 1000.0)
        ),
        Parameter(
            name="dP",
            description="Pressure change",
            units="mmHg",
            symbol="dP",
            physiological_range=(20.0, 60.0)
        ),
        Parameter(
            name="dV",
            description="Volume change",
            units="mL",
            symbol="dV",
            physiological_range=(10.0, 50.0)
        ),
        Parameter(
            name="rho",
            description="Blood density",
            units="kg/m³",
            symbol=r"\rho",
            default_value=1060.0,
            physiological_range=(1050.0, 1070.0)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(bramwell_hill)

"""Vascular compliance definition."""


def compute_compliance(dV: float, dP: float) -> float:
    """
    Calculate vascular compliance.

    Parameters
    ----------
    dV : float
        Change in volume (mL)
    dP : float
        Change in pressure (mmHg)

    Returns
    -------
    float
        Compliance (mL/mmHg)
    """
    return dV / dP


compliance = create_equation(
    id="vascular_compliance",
    output_units='mL/mmHg',
    name="Vascular Compliance",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"C = \frac{\Delta V}{\Delta P}",
    simplified="C = ΔV / ΔP",
    description="Change in vessel volume per unit change in pressure",
    compute_func=compute_compliance,
    parameters=[
        Parameter(
            name="dV",
            description="Change in volume",
            units="mL",
            symbol=r"\Delta V",
            physiological_range=(0.1, 100.0)
        ),
        Parameter(
            name="dP",
            description="Change in pressure",
            units="mmHg",
            symbol=r"\Delta P",
            physiological_range=(1.0, 50.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(compliance)

"""Mean arterial pressure equation."""


def compute_mean_arterial_pressure(SBP: float, DBP: float) -> float:
    """
    Calculate mean arterial pressure from systolic and diastolic pressures.

    Parameters
    ----------
    SBP : float
        Systolic blood pressure (mmHg)
    DBP : float
        Diastolic blood pressure (mmHg)

    Returns
    -------
    float
        Mean arterial pressure (mmHg)
    """
    return DBP + (SBP - DBP) / 3.0


mean_arterial_pressure = create_equation(
    id="mean_arterial_pressure",
    produces='MAP',
    output_units='mmHg',
    name="Mean Arterial Pressure",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{MAP} = \text{DBP} + \frac{1}{3}(\text{SBP} - \text{DBP})",
    simplified="MAP = DBP + (SBP - DBP) / 3",
    description="Time-weighted average arterial pressure during cardiac cycle",
    compute_func=compute_mean_arterial_pressure,
    parameters=[
        Parameter(
            name="SBP",
            description="Systolic blood pressure",
            units="mmHg",
            symbol="SBP",
            physiological_range=(90.0, 140.0)
        ),
        Parameter(
            name="DBP",
            description="Diastolic blood pressure",
            units="mmHg",
            symbol="DBP",
            physiological_range=(60.0, 90.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(mean_arterial_pressure)

"""Moens-Korteweg equation for pulse wave velocity."""


def compute_moens_korteweg(E: float, h: float, d: float, rho: float = 1060.0) -> float:
    """
    Calculate pulse wave velocity using Moens-Korteweg equation.

    Parameters
    ----------
    E : float
        Elastic modulus of vessel wall (Pa)
    h : float
        Wall thickness (m)
    d : float
        Vessel diameter (m)
    rho : float, optional
        Blood density (kg/m³, default: 1060)

    Returns
    -------
    float
        Pulse wave velocity (m/s)
    """
    return np.sqrt((E * h) / (rho * d))


moens_korteweg = create_equation(
    id="moens_korteweg_pwv",
    output_units='m/s',
    name="Moens-Korteweg Pulse Wave Velocity",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{PWV} = \sqrt{\frac{E h}{\rho d}}",
    simplified="PWV = √(E·h / ρ·d)",
    description="Pulse wave velocity from vessel wall elastic properties",
    compute_func=compute_moens_korteweg,
    parameters=[
        Parameter(
            name="E",
            description="Elastic modulus of vessel wall",
            units="Pa",
            symbol="E",
            physiological_range=(1e5, 1e6)
        ),
        Parameter(
            name="h",
            description="Wall thickness",
            units="m",
            symbol="h",
            physiological_range=(0.001, 0.005)
        ),
        Parameter(
            name="d",
            description="Vessel diameter",
            units="m",
            symbol="d",
            physiological_range=(0.02, 0.03)
        ),
        Parameter(
            name="rho",
            description="Blood density",
            units="kg/m³",
            symbol=r"\rho",
            default_value=1060.0,
            physiological_range=(1050.0, 1070.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(moens_korteweg)

"""Poiseuille's law for hydraulic resistance."""


def compute_poiseuille_resistance(eta: float, L: float, r: float) -> float:
    """
    Calculate hydraulic resistance using Poiseuille's law.

    Parameters
    ----------
    eta : float
        Blood viscosity (mPa·s)
    L : float
        Vessel length (cm)
    r : float
        Vessel radius (cm)

    Returns
    -------
    float
        Hydraulic resistance (mmHg·s/mL)
    """
    # Convert units: eta in mPa·s = 0.001 Pa·s, need mmHg·s/mL
    # 1 Pa = 0.0075 mmHg, 1 mL = 1 cm³
    # R = 8ηL/(πr⁴)
    return (8 * eta * L) / (np.pi * r**4) * 7.5e-6  # mPa*s/mL -> mmHg*s/mL (1e-3 mPa->Pa x 7.5e-3 Pa->mmHg)


poiseuille_resistance = create_equation(
    id="poiseuille_resistance",
    output_units='mmHg*s/mL',
    name="Poiseuille's Law for Resistance",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"R = \frac{8\eta L}{\pi r^4}",
    simplified="R = 8ηL / (πr⁴)",
    description="Hydraulic resistance for laminar flow in cylindrical vessels",
    compute_func=compute_poiseuille_resistance,
    parameters=[
        Parameter(
            name="eta",
            description="Blood viscosity",
            units="mPa·s",
            symbol=r"\eta",
            physiological_range=(3.0, 5.0)
        ),
        Parameter(
            name="L",
            description="Vessel length",
            units="cm",
            symbol="L",
            physiological_range=(0.1, 100.0)
        ),
        Parameter(
            name="r",
            description="Vessel radius",
            units="cm",
            symbol="r",
            physiological_range=(0.001, 1.5)
        )
    ],
    depends_on=["blood_viscosity"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(poiseuille_resistance)

"""Reynolds number for flow characterization."""


def compute_reynolds_number(rho: float, v: float, d: float, eta: float) -> float:
    """
    Calculate Reynolds number to predict turbulent vs laminar flow.

    Parameters
    ----------
    rho : float
        Blood density (kg/m³)
    v : float
        Flow velocity (m/s)
    d : float
        Vessel diameter (m)
    eta : float
        Dynamic viscosity (Pa·s)

    Returns
    -------
    float
        Reynolds number (dimensionless)
    """
    return (rho * v * d) / eta


reynolds_number = create_equation(
    id="reynolds_number_blood",
    output_units='dimensionless',
    name="Reynolds Number (Blood Flow)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{Re} = \frac{\rho v d}{\eta}",
    simplified="Re = ρvd / η",
    description="Dimensionless number predicting flow regime (laminar vs turbulent)",
    compute_func=compute_reynolds_number,
    parameters=[
        Parameter(
            name="rho",
            description="Blood density",
            units="kg/m³",
            symbol=r"\rho",
            physiological_range=(1050.0, 1070.0)
        ),
        Parameter(
            name="v",
            description="Flow velocity",
            units="m/s",
            symbol="v",
            physiological_range=(0.01, 2.0)
        ),
        Parameter(
            name="d",
            description="Vessel diameter",
            units="m",
            symbol="d",
            physiological_range=(0.001, 0.03)
        ),
        Parameter(
            name="eta",
            description="Dynamic viscosity",
            units="Pa·s",
            symbol=r"\eta",
            physiological_range=(0.003, 0.005)
        )
    ],
    depends_on=["blood_viscosity", "mean_flow_velocity"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(reynolds_number)

"""Total peripheral resistance equation."""


def compute_tpr(MAP: float, CVP: float, CO: float) -> float:
    """
    Calculate total peripheral resistance.

    Parameters
    ----------
    MAP : float
        Mean arterial pressure (mmHg)
    CVP : float
        Central venous pressure (mmHg)
    CO : float
        Cardiac output (L/min)

    Returns
    -------
    float
        Total peripheral resistance (Wood units = mmHg/(L/min))
    """
    return (MAP - CVP) / CO


tpr = create_equation(
    id="total_peripheral_resistance",
    output_units='mmHg*min/L',
    name="Total Peripheral Resistance",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{TPR} = \frac{\text{MAP} - \text{CVP}}{\text{CO}}",
    simplified="TPR = (MAP - CVP) / CO",
    description="Systemic vascular resistance in Wood units",
    compute_func=compute_tpr,
    parameters=[
        Parameter(
            name="MAP",
            description="Mean arterial pressure",
            units="mmHg",
            symbol="MAP",
            physiological_range=(70.0, 105.0)
        ),
        Parameter(
            name="CVP",
            description="Central venous pressure",
            units="mmHg",
            symbol="CVP",
            default_value=0.0,
            physiological_range=(0.0, 8.0)
        ),
        Parameter(
            name="CO",
            description="Cardiac output",
            units="L/min",
            symbol="CO",
            physiological_range=(4.0, 8.0)
        )
    ],
    depends_on=["cardiac_output", "cardiac_output_fick", "indicator_dilution_cardiac_output", "map_from_flow", "mean_arterial_pressure"],
    produces="TPR",
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(tpr)

"""Windkessel time constant equation."""


def compute_windkessel_tau(R: float, C: float) -> float:
    """
    Calculate arterial windkessel time constant.

    Parameters
    ----------
    R : float
        Arterial resistance (Wood units)
    C : float
        Arterial compliance (mL/mmHg)

    Returns
    -------
    float
        Time constant (s)
    """
    # Convert Wood units (mmHg/(L/min)) to (mmHg·s/mL)
    # 1 Wood unit = 1 mmHg/(L/min) = 60 mmHg·s/L = 0.06 mmHg·s/mL
    R_converted = R * 0.06
    return R_converted * C


windkessel_tau = create_equation(
    id="windkessel_time_constant",
    output_units='s',
    name="Windkessel Time Constant",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\tau = R \times C",
    simplified="τ = R × C",
    description="Exponential decay time constant for arterial pressure",
    compute_func=compute_windkessel_tau,
    parameters=[
        Parameter(
            name="R",
            description="Arterial resistance",
            units="Wood units",
            symbol="R",
            physiological_range=(15.0, 25.0)
        ),
        Parameter(
            name="C",
            description="Arterial compliance",
            units="mL/mmHg",
            symbol="C",
            physiological_range=(1.0, 2.5)
        )
    ],
    depends_on=["vascular_compliance", "total_peripheral_resistance"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(windkessel_tau)

"""Womersley number for pulsatile flow."""


def compute_womersley_number(r: float, omega: float, rho: float, eta: float) -> float:
    """
    Calculate Womersley number for pulsatile flow.

    Parameters
    ----------
    r : float
        Vessel radius (m)
    omega : float
        Angular frequency (rad/s) = 2π × heart rate (Hz)
    rho : float
        Blood density (kg/m³)
    eta : float
        Dynamic viscosity (Pa·s)

    Returns
    -------
    float
        Womersley number (dimensionless)
    """
    return r * np.sqrt((omega * rho) / eta)


womersley_number = create_equation(
    id="womersley_number",
    output_units='dimensionless',
    name="Womersley Number",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\alpha = r \sqrt{\frac{\omega \rho}{\eta}}",
    simplified="α = r × √(ω·ρ / η)",
    description="Dimensionless parameter characterizing pulsatile flow velocity profile",
    compute_func=compute_womersley_number,
    parameters=[
        Parameter(
            name="r",
            description="Vessel radius",
            units="m",
            symbol="r",
            physiological_range=(0.0005, 0.015)
        ),
        Parameter(
            name="omega",
            description="Angular frequency",
            units="rad/s",
            symbol=r"\omega",
            physiological_range=(4.0, 10.0)
        ),
        Parameter(
            name="rho",
            description="Blood density",
            units="kg/m³",
            symbol=r"\rho",
            physiological_range=(1050.0, 1070.0)
        ),
        Parameter(
            name="eta",
            description="Dynamic viscosity",
            units="Pa·s",
            symbol=r"\eta",
            physiological_range=(0.003, 0.005)
        )
    ],
    depends_on=["blood_viscosity"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.4"
    )
)

register_equation(womersley_number)

__all__ = ['poiseuille_resistance', 'tpr', 'mean_arterial_pressure', 'compliance', 'windkessel_tau', 'moens_korteweg', 'bramwell_hill', 'reynolds_number', 'womersley_number']


# === Added v3.1.0: reusable equations from Feher Unit 5 Section 5.11 ===

def compute_bernoulli_equivalent_pressure(P, rho, v, g=9.81, h=0.0):
    """Equivalent (total) pressure P' = P + 1/2 rho v^2 + rho g h (Feher 5.11)."""
    return P + 0.5 * rho * v ** 2 + rho * g * h


bernoulli_equivalent_pressure = create_equation(
    id="bernoulli_equivalent_pressure",
    output_units='Pa',
    name="Bernoulli Equivalent Pressure",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"P' = P + \tfrac{1}{2}\rho v^2 + \rho g h",
    simplified="P_eq = P + 0.5*rho*v^2 + rho*g*h",
    description=("Total (equivalent) pressure combining static, kinetic and "
                 "gravitational terms; the driving pressure for steady-state flow "
                 "and the basis of the lateral-vs-end pressure difference (Bernoulli)."),
    compute_func=compute_bernoulli_equivalent_pressure,
    parameters=[
        Parameter(name="P", description="Static (lateral) pressure", units="Pa", symbol="P",
                  physiological_range=(0.0, 40000.0)),
        Parameter(name="rho", description="Blood density", units="kg/m3", symbol="rho",
                  physiological_range=(1000.0, 1100.0)),
        Parameter(name="v", description="Flow velocity", units="m/s", symbol="v",
                  physiological_range=(0.0, 5.0)),
        Parameter(name="g", description="Gravitational acceleration", units="m/s^2", symbol="g",
                  physiological_range=(9.7, 9.9)),
        Parameter(name="h", description="Height above reference", units="m", symbol="h",
                  physiological_range=(-1.0, 1.0)),
    ],
    depends_on=["mean_flow_velocity"],
    metadata=EquationMetadata(source_unit=5, source_chapter="5.11",
                              source_section="Flow is driven by a pressure difference (Bernoulli)"),
)
register_equation(bernoulli_equivalent_pressure)


def compute_mean_flow_velocity(Q_V, A):
    """Mean linear velocity from volume flow and cross-sectional area: v = Q/A."""
    return Q_V / A


mean_flow_velocity = create_equation(
    id="mean_flow_velocity",
    output_units='m/s',
    name="Mean Flow Velocity (Continuity)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\bar v = \frac{Q_V}{A}",
    simplified="v = Q_V / A",
    description=("Average linear velocity of blood from volumetric flow and total "
                 "cross-sectional area; explains why velocity is lowest in the "
                 "capillaries, where aggregate area is greatest."),
    compute_func=compute_mean_flow_velocity,
    parameters=[
        Parameter(name="Q_V", description="Volumetric flow", units="m3/s", symbol="Q_V",
                  physiological_range=(0.0, 1e-3)),
        Parameter(name="A", description="Total cross-sectional area", units="m2", symbol="A",
                  physiological_range=(1e-6, 1.0)),
    ],
    depends_on=[],
    produces="v",
    metadata=EquationMetadata(source_unit=5, source_chapter="5.11",
                              source_section="Third principle: mean velocity = flow / area"),
)
register_equation(mean_flow_velocity)


def compute_pulse_pressure(SBP, DBP):
    """Pulse pressure = systolic - diastolic pressure (Feher 5.11)."""
    return SBP - DBP


pulse_pressure = create_equation(
    id="pulse_pressure",
    output_units='mmHg',
    name="Pulse Pressure",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\Delta P_{pulse} = P_{systolic} - P_{diastolic}",
    simplified="PP = SBP - DBP",
    description=("Arterial pulse pressure; for a given stroke volume it widens when "
                 "arterial compliance falls (e.g. ageing/arteriosclerosis), so a wide "
                 "pulse pressure indicates stiff arteries."),
    compute_func=compute_pulse_pressure,
    parameters=[
        Parameter(name="SBP", description="Systolic blood pressure", units="mmHg", symbol="P_sys",
                  physiological_range=(80.0, 200.0)),
        Parameter(name="DBP", description="Diastolic blood pressure", units="mmHg", symbol="P_dia",
                  physiological_range=(40.0, 130.0)),
    ],
    depends_on=[],
    produces="PP",
    metadata=EquationMetadata(source_unit=5, source_chapter="5.11",
                              source_section="Pulse pressure depends on stroke volume and arterial compliance"),
)
register_equation(pulse_pressure)

__all__ += ['bernoulli_equivalent_pressure', 'mean_flow_velocity', 'pulse_pressure']


# --- coverage pass additions (Feher extraction) ---

def compute_systemic_vascular_compliance(C_A, C_V):
    """Total systemic vascular compliance as the parallel sum of arterial and venous compliances (Feher 5.14, C_S = C_A + C_V). Inputs and output in mL/mmHg."""
    return C_A + C_V

systemic_vascular_compliance = create_equation(
    id='systemic_vascular_compliance',
    output_units='mL/mmHg',
    name='Systemic Vascular Compliance',
    category=EquationCategory.CARDIOVASCULAR,
    latex='C_{\\mathrm{S}} = C_{\\mathrm{A}} + C_{\\mathrm{V}}',
    simplified='C_S = C_A + C_V',
    description='Total systemic vascular compliance equals the sum of the arterial and venous compartment compliances. In a stopped, no-flow circulation the arterial and venous sides share the same pressure change (ΔP_A = ΔP_V = ΔP_S) while their volume changes add (ΔV_S = ΔV_A + ΔV_V), so the two compartments combine in parallel and their compliances add. C_S sets the slope (1/C_S) of the blood-volume vs mean-systemic-pressure line (Feher Fig 5.14.4) and underlies stressed/unstressed volume and mean systemic filling pressure analysis in Guyton venous-return physiology.',
    compute_func=compute_systemic_vascular_compliance,
    parameters=[
        Parameter(name='C_A', description='Arterial (arteries + arterioles) compliance', units='mL/mmHg', symbol='C_{\\mathrm{A}}', physiological_range=(0.5, 5)),
        Parameter(name='C_V', description='Venous (venules + veins) compliance', units='mL/mmHg', symbol='C_{\\mathrm{V}}', physiological_range=(20, 200)),
    ],
    depends_on=[],
    produces='C_S',
    metadata=EquationMetadata(source_unit=5, source_chapter='5.14',
                              source_section='Filling the Empty Circulatory System Reveals Stressed and Unstressed Volumes', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(systemic_vascular_compliance)


def compute_vascular_function_curve(P_RA, P_MS, C_V, C_A, TPR):
    """Vascular (venous return) function curve Q_veins = -[(1 + C_V/C_A)/TPR](P_RA - P_MS); Feher Eqn 5.14.13. Pressures in mmHg, compliances in mL/mmHg (ratio dimensionless), TPR in Wood units mmHg/(L/min); returns venous return flow in L/min."""
    return -((1.0 + C_V / C_A) / TPR) * (P_RA - P_MS)

vascular_function_curve = create_equation(
    id='vascular_function_curve',
    output_units='L/min',
    name='Vascular Function Curve (Venous Return)',
    category=EquationCategory.CARDIOVASCULAR,
    latex='Q_{\\mathrm{veins}} = -\\dfrac{\\left[1 + C_{\\mathrm{V}}/C_{\\mathrm{A}}\\right]}{\\mathrm{TPR}}\\left[P_{\\mathrm{RA}} - P_{\\mathrm{MS}}\\right]',
    simplified='Q_veins = -((1 + C_V/C_A)/TPR)*(P_RA - P_MS)',
    description='Guyton/Levy vascular (venous return) function curve: expresses systemic venous return flow as a linear function of right atrial pressure. The line has its x-intercept at the mean systemic filling pressure P_MS (flow is zero when P_RA = P_MS) and slope -(1 + C_V/C_A)/TPR. Derived by taking Q = (P_A - P_RA)/TPR and eliminating arterial pressure P_A via the arterial/venous compliance relation. Its intersection with the cardiac function curve sets the steady-state cardiovascular operating point, where venous return equals cardiac output; a compact negative-feedback system. A theoretical approximation valid for positive right atrial pressures (below ~0 mmHg the veins partially collapse and flow plateaus).',
    compute_func=compute_vascular_function_curve,
    parameters=[
        Parameter(name='P_RA', description='Right atrial (central venous) pressure, the preload variable on the abscissa of the curve', units='mmHg', symbol='P_{RA}', physiological_range=(-4, 20)),
        Parameter(name='P_MS', description='Mean systemic (filling) pressure; pressure everywhere when the heart is stopped, the x-intercept of the curve (Q_veins = 0 when P_RA = P_MS)', units='mmHg', symbol='P_{MS}', physiological_range=(3, 20)),
        Parameter(name='C_V', description='Venous (venules + veins) compliance', units='mL/mmHg', symbol='C_{V}', physiological_range=(10, 100)),
        Parameter(name='C_A', description='Arterial (arteries + arterioles) compliance', units='mL/mmHg', symbol='C_{A}', physiological_range=(0.5, 3)),
        Parameter(name='TPR', description='Total peripheral (systemic vascular) resistance', units='Wood units (mmHg/(L/min))', symbol='TPR', physiological_range=(10, 40)),
    ],
    depends_on=['total_peripheral_resistance', 'vascular_compliance'],
    produces='Q_veins',
    metadata=EquationMetadata(source_unit=5, source_chapter='5.14',
                              source_section='THE VASCULAR FUNCTION CURVE CAN BE DERIVED FROM ARTERIAL AND VENOUS COMPLIANCES AND TPR', page_reference=None,
                              textbook_equation_number='5.14.13'),
)
register_equation(vascular_function_curve)

try:
    __all__ += ['systemic_vascular_compliance', 'vascular_function_curve']
except NameError:
    __all__ = ['systemic_vascular_compliance', 'vascular_function_curve']


# --- clinical additions (CICM, beyond Feher) ---

def compute_svr_dyn(MAP, CVP, CO):
    """SVR = 80*(MAP-CVP)/CO in dyn*s*cm^-5 (MAP,CVP mmHg; CO L/min). Normal 800-1200."""
    return 80.0 * (MAP - CVP) / CO

svr_dyn = create_equation(
    id='svr_dyn',
    output_units='dyn*s/cm^5',
    name='Systemic Vascular Resistance (dyn)',
    category=EquationCategory.CARDIOVASCULAR,
    latex='SVR = \\frac{80(MAP-CVP)}{CO}',
    simplified='SVR = 80*(MAP-CVP)/CO',
    description='Systemic vascular resistance in hybrid (dyn*s*cm^-5) units used at the bedside; the 80 converts mmHg*min/L (Wood units) to dyn*s*cm^-5. Normal 800-1200.',
    compute_func=compute_svr_dyn,
    parameters=[
        Parameter(name='MAP', description='Mean arterial pressure', units='mmHg', symbol='MAP', physiological_range=(40, 160)),
        Parameter(name='CVP', description='Central venous pressure', units='mmHg', symbol='CVP', physiological_range=(0, 25)),
        Parameter(name='CO', description='Cardiac output', units='L/min', symbol='CO', physiological_range=(2, 12)),
    ],
    depends_on=["cardiac_output", "cardiac_output_fick", "indicator_dilution_cardiac_output", "map_from_flow", "mean_arterial_pressure"],
    produces='SVR',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(svr_dyn)


def compute_pvr_dyn(mPAP, PCWP, CO):
    """PVR = 80*(mPAP-PCWP)/CO in dyn*s*cm^-5. Normal <250 (~50-150)."""
    return 80.0 * (mPAP - PCWP) / CO

pvr_dyn = create_equation(
    id='pvr_dyn',
    output_units='dyn*s/cm^5',
    name='Pulmonary Vascular Resistance (dyn)',
    category=EquationCategory.CARDIOVASCULAR,
    latex='PVR = \\frac{80(mPAP-PCWP)}{CO}',
    simplified='PVR = 80*(mPAP-PCWP)/CO',
    description='Pulmonary vascular resistance in dyn*s*cm^-5; elevated in pulmonary hypertension. Normal <250.',
    compute_func=compute_pvr_dyn,
    parameters=[
        Parameter(name='mPAP', description='Mean pulmonary artery pressure', units='mmHg', symbol='mPAP', physiological_range=(8, 60)),
        Parameter(name='PCWP', description='Pulmonary capillary wedge pressure', units='mmHg', symbol='PCWP', physiological_range=(2, 30)),
        Parameter(name='CO', description='Cardiac output', units='L/min', symbol='CO', physiological_range=(2, 12)),
    ],
    depends_on=["cardiac_output", "cardiac_output_fick", "indicator_dilution_cardiac_output"],
    produces='PVR',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(pvr_dyn)


def compute_ventricular_wall_stress(P, r, h):
    """LV wall stress (afterload) sigma = P*r/(2h) by Laplace for a thick sphere (P mmHg, r,h same length unit). Returns mmHg."""
    return P * r / (2.0 * h)

ventricular_wall_stress = create_equation(
    id='ventricular_wall_stress',
    output_units='mmHg',
    name='Ventricular Wall Stress (Laplace)',
    category=EquationCategory.CARDIOVASCULAR,
    latex='\\sigma = \\frac{P\\,r}{2h}',
    simplified='sigma = P*r/(2h)',
    description='Left-ventricular wall stress by the law of Laplace: the true mechanical afterload the myocardium works against. Rises with dilation (high r) and pressure, falls with hypertrophy (high h).',
    compute_func=compute_ventricular_wall_stress,
    parameters=[
        Parameter(name='P', description='Ventricular cavity pressure', units='mmHg', symbol='P', physiological_range=(40, 250)),
        Parameter(name='r', description='Cavity radius', units='cm', symbol='r', physiological_range=(1, 6)),
        Parameter(name='h', description='Wall thickness', units='cm', symbol='h', physiological_range=(0.5, 2.5)),
    ],
    depends_on=[],
    produces='wall_stress',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(ventricular_wall_stress)


def compute_pulse_pressure_from_compliance(SV, C_art):
    """PP ~ SV/C_art (windkessel): pulse pressure rises with stroke volume and falls with arterial compliance."""
    return SV / C_art

pulse_pressure_from_compliance = create_equation(
    id='pulse_pressure_from_compliance',
    output_units='mmHg',
    name='Pulse Pressure from Compliance',
    category=EquationCategory.CARDIOVASCULAR,
    latex='PP \\approx \\frac{SV}{C_{art}}',
    simplified='PP = SV / C_art',
    description='Mechanistic pulse pressure from the two-element windkessel: PP is proportional to stroke volume and inversely to arterial compliance, explaining the wide pulse pressure of stiff aged/atherosclerotic arteries.',
    compute_func=compute_pulse_pressure_from_compliance,
    parameters=[
        Parameter(name='SV', description='Stroke volume', units='mL', symbol='SV', physiological_range=(20, 150)),
        Parameter(name='C_art', description='Arterial compliance', units='mL/mmHg', symbol='C_A', physiological_range=(0.5, 5)),
    ],
    depends_on=["stroke_volume"],
    produces='PP_c',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(pulse_pressure_from_compliance)


def compute_map_from_flow(CO, SVR_wood, CVP):
    """MAP = CO*SVR + CVP (Ohm's law for the circulation; SVR in Wood units mmHg*min/L)."""
    return CO * SVR_wood + CVP

map_from_flow = create_equation(
    id='map_from_flow',
    output_units='mmHg',
    name='MAP from Flow and Resistance',
    category=EquationCategory.CARDIOVASCULAR,
    latex='MAP = CO\\times SVR + CVP',
    simplified='MAP = CO*SVR + CVP',
    description="The forward (Ohm's-law) form of arterial pressure: mean pressure is the product of cardiac output and systemic vascular resistance plus the downstream venous pressure. Complements the DBP+PP/3 estimate.",
    compute_func=compute_map_from_flow,
    parameters=[
        Parameter(name='CO', description='Cardiac output', units='L/min', symbol='CO', physiological_range=(2, 12)),
        Parameter(name='SVR_wood', description='Systemic vascular resistance', units='mmHg*min/L', symbol='SVR', physiological_range=(5, 40)),
        Parameter(name='CVP', description='Central venous pressure', units='mmHg', symbol='CVP', physiological_range=(0, 25)),
    ],
    depends_on=["cardiac_output", "cardiac_output_fick", "indicator_dilution_cardiac_output"],
    produces='MAP',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(map_from_flow)

try:
    __all__ += ['svr_dyn', 'pvr_dyn', 'ventricular_wall_stress', 'pulse_pressure_from_compliance', 'map_from_flow']
except NameError:
    __all__ = ['svr_dyn', 'pvr_dyn', 'ventricular_wall_stress', 'pulse_pressure_from_compliance', 'map_from_flow']


# --- review-add 2026-07-15 ---
def compute_coronary_perfusion_pressure(DBP: float, LVEDP: float) -> float:
    """Left-ventricular coronary perfusion pressure CPP = DBP - LVEDP.

    LV coronary flow is predominantly diastolic; supply pressure is aortic
    diastolic minus LV end-diastolic (back) pressure."""
    return DBP - LVEDP

coronary_perfusion_pressure_equation = create_equation(
    id='coronary_perfusion_pressure',
    name='Coronary Perfusion Pressure',
    category=EquationCategory.CARDIOVASCULAR,
    latex=r'CPP = DBP - LVEDP',
    simplified='CPP = DBP - LVEDP',
    description='Left-ventricular coronary perfusion pressure: aortic diastolic minus LV end-diastolic pressure. Falls with diastolic hypotension, raised LVEDP, aortic stenosis and tachycardia.',
    compute_func=compute_coronary_perfusion_pressure,
    output_units='mmHg',
    parameters=[
        Parameter(name='DBP', description='Aortic diastolic blood pressure', units='mmHg', symbol='DBP', physiological_range=(30, 120)),
        Parameter(name='LVEDP', description='LV end-diastolic pressure', units='mmHg', symbol='LVEDP', physiological_range=(2, 30)),
    ],
    metadata=EquationMetadata(source_unit=5, source_chapter='5.10'),
)
register_equation(coronary_perfusion_pressure_equation)


# --- review-add 2026-07-15 ---
def compute_stroke_work(MAP: float, SV: float) -> float:
    """External ventricular stroke work per beat, SW = MAP x SV
    (pressure-volume area approximation)."""
    return MAP * SV

stroke_work_equation = create_equation(
    id='stroke_work',
    name='Ventricular Stroke Work',
    category=EquationCategory.CARDIOVASCULAR,
    latex=r'SW = \\bar{P} \\times SV',
    simplified='SW = MAP * SV',
    description='External mechanical work of one ventricular beat (PV-loop area approximation, mean ejection pressure x stroke volume). Basis for pressure-volume-area, PRSW and cardiac efficiency.',
    compute_func=compute_stroke_work,
    output_units='mmHg*mL',
    parameters=[
        Parameter(name='MAP', description='Mean arterial (ejection) pressure', units='mmHg', symbol='MAP', physiological_range=(40, 160)),
        Parameter(name='SV', description='Stroke volume', units='mL', symbol='SV', physiological_range=(20, 150)),
    ],
    depends_on=["mean_arterial_pressure", "stroke_volume"],   # SW = MAP * SV
    metadata=EquationMetadata(source_unit=5, source_chapter='5.9'),
)
register_equation(stroke_work_equation)

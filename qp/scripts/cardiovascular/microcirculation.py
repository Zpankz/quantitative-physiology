"""Microcirculation and capillary exchange equations."""

"""Baroreceptor sensitivity equation."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_baroreceptor_sensitivity(dRR: float, dSBP: float) -> float:
    """
    Calculate baroreceptor sensitivity.

    Parameters
    ----------
    dRR : float
        Change in RR interval (ms)
    dSBP : float
        Change in systolic blood pressure (mmHg)

    Returns
    -------
    float
        Baroreceptor sensitivity (ms/mmHg)
    """
    return dRR / dSBP


baroreceptor_sensitivity = create_equation(
    id="baroreceptor_sensitivity",
    output_units='ms/mmHg',
    name="Baroreceptor Sensitivity",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{BRS} = \frac{\Delta RR}{\Delta SBP}",
    simplified="BRS = ΔRR / ΔSBP",
    description="Measure of baroreceptor reflex responsiveness",
    compute_func=compute_baroreceptor_sensitivity,
    parameters=[
        Parameter(
            name="dRR",
            description="Change in RR interval",
            units="ms",
            symbol=r"\Delta RR",
            physiological_range=(1.0, 100.0)
        ),
        Parameter(
            name="dSBP",
            description="Change in systolic blood pressure",
            units="mmHg",
            symbol=r"\Delta SBP",
            physiological_range=(1.0, 50.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.6"
    )
)

register_equation(baroreceptor_sensitivity)

"""Fick's law for transcapillary solute diffusion."""


def compute_ficks_law_diffusion(P_s: float, S: float, C_c: float, C_i: float) -> float:
    """
    Calculate solute flux across capillary wall by diffusion.

    Parameters
    ----------
    P_s : float
        Permeability coefficient (cm/s)
    S : float
        Capillary surface area (cm²)
    C_c : float
        Capillary solute concentration (mol/L or mg/dL)
    C_i : float
        Interstitial solute concentration (mol/L or mg/dL)

    Returns
    -------
    float
        Solute flux (amount/time in units consistent with inputs)
    """
    return P_s * S * (C_c - C_i)


ficks_law_diffusion = create_equation(
    id="ficks_law_diffusion",
    output_units='mmol/s',
    name="Fick's Law for Capillary Diffusion",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"J_s = P_s \times S \times (C_c - C_i)",
    simplified="J_s = P_s × S × (C_c - C_i)",
    description="Diffusive solute flux across capillary wall",
    compute_func=compute_ficks_law_diffusion,
    parameters=[
        Parameter(
            name="P_s",
            description="Permeability coefficient",
            units="cm/s",
            symbol="P_s",
            physiological_range=(1e-7, 1e-3)
        ),
        Parameter(
            name="S",
            description="Capillary surface area",
            units="cm²",
            symbol="S",
            physiological_range=(100.0, 10000.0)
        ),
        Parameter(
            name="C_c",
            description="Capillary concentration",
            units="mol/L or mg/dL",
            symbol="C_c",
            physiological_range=(0.0, 1000.0)
        ),
        Parameter(
            name="C_i",
            description="Interstitial concentration",
            units="mol/L or mg/dL",
            symbol="C_i",
            physiological_range=(0.0, 1000.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.5"
    )
)

register_equation(ficks_law_diffusion)

"""Net filtration pressure calculation."""


def compute_net_filtration_pressure(
    P_c: float,
    P_i: float,
    pi_c: float,
    pi_i: float,
    sigma: float = 1.0
) -> float:
    """
    Calculate net filtration pressure across capillary wall.

    Parameters
    ----------
    P_c : float
        Capillary hydrostatic pressure (mmHg)
    P_i : float
        Interstitial hydrostatic pressure (mmHg)
    pi_c : float
        Capillary oncotic pressure (mmHg)
    pi_i : float
        Interstitial oncotic pressure (mmHg)
    sigma : float, optional
        Reflection coefficient (0-1, default: 1.0)

    Returns
    -------
    float
        Net filtration pressure (mmHg)
    """
    return (P_c - P_i) - sigma * (pi_c - pi_i)


net_filtration_pressure = create_equation(
    id="net_filtration_pressure",
    output_units='mmHg',
    name="Net Filtration Pressure",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{NFP} = (P_c - P_i) - \sigma(\pi_c - \pi_i)",
    simplified="NFP = (P_c - P_i) - σ(π_c - π_i)",
    description="Net driving force for capillary filtration",
    compute_func=compute_net_filtration_pressure,
    parameters=[
        Parameter(
            name="P_c",
            description="Capillary hydrostatic pressure",
            units="mmHg",
            symbol="P_c",
            physiological_range=(15.0, 35.0)
        ),
        Parameter(
            name="P_i",
            description="Interstitial hydrostatic pressure",
            units="mmHg",
            symbol="P_i",
            physiological_range=(-5.0, 2.0)
        ),
        Parameter(
            name="pi_c",
            description="Capillary oncotic pressure",
            units="mmHg",
            symbol=r"\pi_c",
            physiological_range=(20.0, 28.0)
        ),
        Parameter(
            name="pi_i",
            description="Interstitial oncotic pressure",
            units="mmHg",
            symbol=r"\pi_i",
            physiological_range=(3.0, 8.0)
        ),
        Parameter(
            name="sigma",
            description="Reflection coefficient",
            units="dimensionless",
            symbol=r"\sigma",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        )
    ],
    depends_on=["capillary_pressure"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.5"
    )
)

register_equation(net_filtration_pressure)

"""Permeability-surface area product from extraction ratio."""

import numpy as np


def compute_ps_product(Q: float, E: float) -> float:
    """
    Calculate permeability-surface area product from extraction ratio.

    Parameters
    ----------
    Q : float
        Blood flow rate (mL/min)
    E : float
        Extraction ratio (0-1)

    Returns
    -------
    float
        PS product (mL/min)
    """
    if E >= 1.0:
        raise ValueError("Extraction ratio must be < 1.0")
    return -Q * np.log(1 - E)


ps_product = create_equation(
    id="ps_product",
    output_units='mL/min',
    name="Permeability-Surface Area Product",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{PS} = -Q \times \ln(1 - E)",
    simplified="PS = -Q × ln(1 - E)",
    description="Permeability-surface area product derived from extraction ratio",
    compute_func=compute_ps_product,
    parameters=[
        Parameter(
            name="Q",
            description="Blood flow rate",
            units="mL/min",
            symbol="Q",
            physiological_range=(1.0, 1000.0)
        ),
        Parameter(
            name="E",
            description="Extraction ratio",
            units="dimensionless",
            symbol="E",
            physiological_range=(0.0, 0.99)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.5"
    )
)

register_equation(ps_product)

"""Wall shear stress in vessels."""


def compute_shear_stress(eta: float, Q: float, r: float) -> float:
    """
    Calculate wall shear stress in a cylindrical vessel.

    Parameters
    ----------
    eta : float
        Blood viscosity (Pa·s)
    Q : float
        Flow rate (m³/s)
    r : float
        Vessel radius (m)

    Returns
    -------
    float
        Wall shear stress (Pa)
    """
    return (4 * eta * Q) / (np.pi * r**3)


shear_stress = create_equation(
    id="wall_shear_stress",
    output_units='Pa',
    name="Wall Shear Stress",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\tau = \frac{4\eta Q}{\pi r^3}",
    simplified="τ = 4ηQ / (πr³)",
    description="Frictional force per unit area exerted by flowing blood on vessel wall",
    compute_func=compute_shear_stress,
    parameters=[
        Parameter(
            name="eta",
            description="Blood viscosity",
            units="Pa·s",
            symbol=r"\eta",
            physiological_range=(0.003, 0.005)
        ),
        Parameter(
            name="Q",
            description="Flow rate",
            units="m³/s",
            symbol="Q",
            physiological_range=(1e-7, 1e-4)
        ),
        Parameter(
            name="r",
            description="Vessel radius",
            units="m",
            symbol="r",
            physiological_range=(0.0001, 0.015)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.6"
    )
)

register_equation(shear_stress)

"""Starling equation for capillary fluid filtration."""


def compute_starling_filtration(
    L_p: float,
    S: float,
    P_c: float,
    P_i: float,
    pi_c: float,
    pi_i: float,
    sigma: float = 1.0
) -> float:
    """
    Calculate fluid filtration rate across capillary wall.

    Parameters
    ----------
    L_p : float
        Hydraulic conductivity (mL/(min·mmHg·cm²))
    S : float
        Capillary surface area (cm²)
    P_c : float
        Capillary hydrostatic pressure (mmHg)
    P_i : float
        Interstitial hydrostatic pressure (mmHg)
    pi_c : float
        Capillary oncotic pressure (mmHg)
    pi_i : float
        Interstitial oncotic pressure (mmHg)
    sigma : float, optional
        Reflection coefficient (0-1, default: 1.0)

    Returns
    -------
    float
        Fluid flux (mL/min), positive = filtration
    """
    return L_p * S * ((P_c - P_i) - sigma * (pi_c - pi_i))


starling_filtration = create_equation(
    id="starling_filtration",
    output_units='mL/min',
    name="Starling Equation for Fluid Filtration",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"J_v = L_p \times S \times [(P_c - P_i) - \sigma(\pi_c - \pi_i)]",
    simplified="J_v = L_p × S × [(P_c - P_i) - σ(π_c - π_i)]",
    description="Net fluid flux across capillary wall determined by balance of hydrostatic and oncotic forces",
    compute_func=compute_starling_filtration,
    parameters=[
        Parameter(
            name="L_p",
            description="Hydraulic conductivity",
            units="mL/(min·mmHg·cm²)",
            symbol="L_p",
            physiological_range=(1e-7, 1e-5)
        ),
        Parameter(
            name="S",
            description="Capillary surface area",
            units="cm²",
            symbol="S",
            physiological_range=(100.0, 10000.0)
        ),
        Parameter(
            name="P_c",
            description="Capillary hydrostatic pressure",
            units="mmHg",
            symbol="P_c",
            physiological_range=(15.0, 35.0)
        ),
        Parameter(
            name="P_i",
            description="Interstitial hydrostatic pressure",
            units="mmHg",
            symbol="P_i",
            physiological_range=(-5.0, 2.0)
        ),
        Parameter(
            name="pi_c",
            description="Capillary oncotic pressure",
            units="mmHg",
            symbol=r"\pi_c",
            physiological_range=(20.0, 28.0)
        ),
        Parameter(
            name="pi_i",
            description="Interstitial oncotic pressure",
            units="mmHg",
            symbol=r"\pi_i",
            physiological_range=(3.0, 8.0)
        ),
        Parameter(
            name="sigma",
            description="Reflection coefficient",
            units="dimensionless",
            symbol=r"\sigma",
            default_value=1.0,
            physiological_range=(0.0, 1.0)
        )
    ],
    depends_on=["capillary_pressure"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.5"
    )
)

register_equation(starling_filtration)

__all__ = ['starling_filtration', 'net_filtration_pressure', 'ficks_law_diffusion', 'ps_product', 'shear_stress', 'baroreceptor_sensitivity']


# --- coverage pass additions (Feher extraction) ---

def compute_capillary_pressure(P_A: float, P_V: float, R_A: float, R_V: float) -> float:
    """Capillary hydrostatic pressure as a two-resistor hydraulic voltage divider (Feher 5.13, 'Vasoconstriction Decreases Capillary Pressure', Eq 5.13.6).

    Derived by eliminating flow Q from the two Ohm's-law relations
    Q = (P_A - P_C)/R_A (arterioles) and Q = (P_C - P_V)/R_V (venules) under the
    Kirchhoff constraint that arteriolar inflow equals venular outflow.

    Parameters
    ----------
    P_A : float
        Arteriolar (precapillary) pressure (mmHg)
    P_V : float
        Venule (postcapillary) pressure (mmHg)
    R_A : float
        Precapillary (arteriolar) resistance (consistent units, e.g. mmHg·min/mL)
    R_V : float
        Postcapillary (venule) resistance (same units as R_A)

    Returns
    -------
    float
        Capillary hydrostatic pressure P_C (mmHg), intermediate between P_A and P_V
    """
    return P_A * (R_V / (R_A + R_V)) + P_V * (R_A / (R_A + R_V))

capillary_pressure = create_equation(
    id='capillary_pressure',
    output_units='mmHg',
    name='Capillary Pressure (Hydraulic Voltage Divider)',
    category=EquationCategory.CARDIOVASCULAR,
    latex='P_C = P_A \\left[\\dfrac{R_V}{R_A + R_V}\\right] + P_V \\left[\\dfrac{R_A}{R_A + R_V}\\right]',
    simplified='P_C = P_A*[R_V/(R_A+R_V)] + P_V*[R_A/(R_A+R_V)]',
    description='Capillary hydrostatic pressure modelled as a two-resistor hydraulic voltage divider between arteriolar (precapillary) and venule (postcapillary) pressures, weighted by their resistances. Capillary pressure is always intermediate between P_A and P_V; raising the precapillary/postcapillary resistance ratio R_A/R_V (e.g. sympathetic vasoconstriction after hemorrhage) lowers P_C toward P_V, favoring reabsorption of interstitial fluid, whereas lowering it raises P_C toward P_A, favoring filtration and edema. Feeds the Starling/net-filtration equations as their P_c input.',
    compute_func=compute_capillary_pressure,
    parameters=[
        Parameter(name='P_A', description='Arteriolar (precapillary) pressure feeding the exchange bed', units='mmHg', symbol='P_A', physiological_range=(20, 80)),
        Parameter(name='P_V', description='Venule (postcapillary) pressure draining the exchange bed', units='mmHg', symbol='P_V', physiological_range=(0, 25)),
        Parameter(name='R_A', description='Precapillary (arteriolar) resistance; its ratio to R_V sets where P_C falls between P_A and P_V', units='mmHg·min/mL', symbol='R_A', physiological_range=(0.01, 1000)),
        Parameter(name='R_V', description='Postcapillary (venule) resistance', units='mmHg·min/mL', symbol='R_V', physiological_range=(0.01, 1000)),
    ],
    depends_on=[],
    produces='P_c',
    metadata=EquationMetadata(source_unit=5, source_chapter='5.13',
                              source_section='VASOCONSTRICTION DECREASES CAPILLARY PRESSURE', page_reference=None,
                              textbook_equation_number='5.13.6'),
)
register_equation(capillary_pressure)


def compute_colloid_osmotic_pressure(C, a=2.8, b=0.18, c=0.012):
    """Colloid osmotic (oncotic) pressure from protein concentration (Feher 5.12).

    Landis-Pappenheimer empirical relation. Plasma proteins are non-ideal solutes
    and do NOT obey van't Hoff's law, so oncotic pressure is a cubic polynomial in
    protein MASS concentration. C in g/dL, returns pi in mmHg. Coefficients are
    protein-specific: albumin (default) a=2.8, b=0.18, c=0.012; globulin a=1.6,
    b=0.15, c=0.006.

    Parameters
    ----------
    C : float
        Protein concentration (g/dL)
    a : float
        Linear empirical coefficient (mmHg per g/dL), default albumin 2.8
    b : float
        Quadratic empirical coefficient (mmHg per (g/dL)^2), default albumin 0.18
    c : float
        Cubic empirical coefficient (mmHg per (g/dL)^3), default albumin 0.012

    Returns
    -------
    float
        Colloid osmotic (oncotic) pressure pi (mmHg)
    """
    return a * C + b * C ** 2 + c * C ** 3

colloid_osmotic_pressure = create_equation(
    id='colloid_osmotic_pressure',
    output_units='mmHg',
    name='Colloid Osmotic (Oncotic) Pressure',
    category=EquationCategory.CARDIOVASCULAR,
    latex='\\pi_{\\mathrm{albumin}} = 2.8C + 0.18C^2 + 0.012C^3; \\quad \\pi_{\\mathrm{globulin}} = 1.6C + 0.15C^2 + 0.006C^3',
    simplified='pi = a*C + b*C^2 + c*C^3  (albumin: a=2.8, b=0.18, c=0.012; globulin: a=1.6, b=0.15, c=0.006); pi in mmHg, C in g/dL',
    description="Colloid osmotic (oncotic) pressure of plasma/interstitial proteins as an empirical cubic polynomial in protein MASS concentration (Landis-Pappenheimer relation). Feher explicitly notes plasma proteins are non-ideal solutes that do NOT obey van't Hoff's law, so oncotic pressure is a nonlinear function of concentration, distinct from the ideal van't Hoff osmotic_pressure (pi = sigma*C*RT). Coefficients are protein-specific (albumin vs globulin). Used to obtain the capillary and interstitial oncotic pressures (pi_c, pi_i) that drive the Starling filtration and net filtration pressure equations. Input C in g/dL, output pi in mmHg.",
    compute_func=compute_colloid_osmotic_pressure,
    parameters=[
        Parameter(name='C', description='Plasma/lymph protein (albumin or globulin) concentration', units='g/dL', symbol='C', physiological_range=(0, 12)),
        Parameter(name='a', description='Linear empirical coefficient of the Landis-Pappenheimer relation (albumin 2.8, globulin 1.6)', units='mmHg/(g/dL)', symbol='a', default_value=2.8, physiological_range=(1, 3.5)),
        Parameter(name='b', description='Quadratic empirical coefficient (albumin 0.18, globulin 0.15)', units='mmHg/(g/dL)^2', symbol='b', default_value=0.18, physiological_range=(0.1, 0.25)),
        Parameter(name='c', description='Cubic empirical coefficient (albumin 0.012, globulin 0.006)', units='mmHg/(g/dL)^3', symbol='c', default_value=0.012, physiological_range=(0.004, 0.02)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=5, source_chapter='5.12',
                              source_section='IN MOST TISSUES, NET FILTRATION PRESSURE DRIVES FLUID OUT OF THE CAPILLARIES AT THE ARTERIOLAR END', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(colloid_osmotic_pressure)

try:
    __all__ += ['capillary_pressure', 'colloid_osmotic_pressure']
except NameError:
    __all__ = ['capillary_pressure', 'colloid_osmotic_pressure']

"""Cardiac mechanics and function equations."""

"""Body surface area (Du Bois formula)."""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_body_surface_area(W: float, H: float) -> float:
    """
    Calculate body surface area using Du Bois formula.

    Parameters
    ----------
    W : float
        Weight (kg)
    H : float
        Height (cm)

    Returns
    -------
    float
        Body surface area (m²)
    """
    return 0.007184 * (W ** 0.425) * (H ** 0.725)


body_surface_area = create_equation(
    id="body_surface_area_dubois",
    output_units='m²',
    name="Body Surface Area (Du Bois)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{BSA} = 0.007184 \times W^{0.425} \times H^{0.725}",
    simplified="BSA = 0.007184 × W^0.425 × H^0.725",
    description="Body surface area from weight and height (Du Bois formula)",
    compute_func=compute_body_surface_area,
    parameters=[
        Parameter(
            name="W",
            description="Body weight",
            units="kg",
            symbol="W",
            physiological_range=(50.0, 100.0)
        ),
        Parameter(
            name="H",
            description="Height",
            units="cm",
            symbol="H",
            physiological_range=(150.0, 200.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    ),
    produces="BSA",  # H3: lets this output satisfy a downstream 'BSA' parameter (id is not a BSA alias)
)

register_equation(body_surface_area)

"""Cardiac index equation."""


def compute_cardiac_index(CO: float, BSA: float) -> float:
    """
    Calculate cardiac index normalized to body surface area.

    Parameters
    ----------
    CO : float
        Cardiac output (L/min)
    BSA : float
        Body surface area (m²)

    Returns
    -------
    float
        Cardiac index (L/min/m²)
    """
    return CO / BSA


cardiac_index = create_equation(
    id="cardiac_index",
    output_units='L/(min*m²)',
    name="Cardiac Index",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{CI} = \frac{\text{CO}}{\text{BSA}}",
    simplified="CI = CO / BSA",
    description="Cardiac output normalized to body surface area",
    compute_func=compute_cardiac_index,
    parameters=[
        Parameter(
            name="CO",
            description="Cardiac output",
            units="L/min",
            symbol="CO",
            physiological_range=(4.0, 8.0)
        ),
        Parameter(
            name="BSA",
            description="Body surface area",
            units="m²",
            symbol="BSA",
            physiological_range=(1.5, 2.5)
        )
    ],
    depends_on=["cardiac_output", "cardiac_output_fick", "indicator_dilution_cardiac_output", "body_surface_area_dubois"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(cardiac_index)

"""Cardiac output equation."""


def compute_cardiac_output(HR: float, SV: float) -> float:
    """
    Calculate cardiac output from heart rate and stroke volume.

    Parameters
    ----------
    HR : float
        Heart rate (bpm)
    SV : float
        Stroke volume (mL)

    Returns
    -------
    float
        Cardiac output (L/min)
    """
    return (HR * SV) / 1000.0


cardiac_output = create_equation(
    id="cardiac_output",
    produces='CO',
    output_units='L/min',
    name="Cardiac Output",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{CO[L/min]} = \frac{\text{HR} \times \text{SV[mL]}}{1000}",
    simplified="CO[L/min] = HR × SV[mL] / 1000",
    description="Cardiac output as product of heart rate and stroke volume",
    compute_func=compute_cardiac_output,
    parameters=[
        Parameter(
            name="HR",
            description="Heart rate",
            units="bpm",
            symbol="HR",
            physiological_range=(60.0, 100.0)
        ),
        Parameter(
            name="SV",
            description="Stroke volume",
            units="mL",
            symbol="SV",
            physiological_range=(60.0, 100.0)
        )
    ],
    depends_on=["stroke_volume", "heart_rate_autonomic"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(cardiac_output)

"""End-diastolic pressure-volume relationship (EDPVR)."""

import numpy as np


def compute_edpvr(EDV: float, A: float, k: float) -> float:
    """
    Calculate end-diastolic pressure from EDPVR.

    Parameters
    ----------
    EDV : float
        End-diastolic volume (mL)
    A : float
        Scaling constant (mmHg)
    k : float
        Stiffness constant (1/mL)

    Returns
    -------
    float
        End-diastolic pressure (mmHg)
    """
    return A * (np.exp(k * EDV) - 1)


edpvr = create_equation(
    id="edpvr",
    output_units='mmHg',
    name="End-Diastolic Pressure-Volume Relationship",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{EDP} = A \times (e^{k \times \text{EDV}} - 1)",
    simplified="EDP = A × (exp(k × EDV) - 1)",
    description="Exponential EDPVR reflecting chamber stiffness",
    compute_func=compute_edpvr,
    parameters=[
        Parameter(
            name="EDV",
            description="End-diastolic volume",
            units="mL",
            symbol="EDV",
            physiological_range=(80.0, 180.0)
        ),
        Parameter(
            name="A",
            description="Scaling constant",
            units="mmHg",
            symbol="A",
            physiological_range=(0.1, 10.0)
        ),
        Parameter(
            name="k",
            description="Stiffness constant",
            units="1/mL",
            symbol="k",
            physiological_range=(0.01, 0.05)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(edpvr)

"""Ejection fraction equation."""


def compute_ejection_fraction(EDV: float, ESV: float) -> float:
    """
    Calculate ejection fraction from end-diastolic and end-systolic volumes.

    Parameters
    ----------
    EDV : float
        End-diastolic volume (mL)
    ESV : float
        End-systolic volume (mL)

    Returns
    -------
    float
        Ejection fraction (0-1)
    """
    return (EDV - ESV) / EDV


ejection_fraction = create_equation(
    id="ejection_fraction",
    output_units='dimensionless',
    name="Ejection Fraction",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{EF} = \frac{\text{EDV} - \text{ESV}}{\text{EDV}} = \frac{\text{SV}}{\text{EDV}}",
    simplified="EF = (EDV - ESV) / EDV",
    description="Fraction of end-diastolic volume ejected per heartbeat",
    compute_func=compute_ejection_fraction,
    parameters=[
        Parameter(
            name="EDV",
            description="End-diastolic volume",
            units="mL",
            symbol="EDV",
            physiological_range=(100.0, 150.0)
        ),
        Parameter(
            name="ESV",
            description="End-systolic volume",
            units="mL",
            symbol="ESV",
            physiological_range=(40.0, 60.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(ejection_fraction)

"""End-systolic pressure-volume relationship (ESPVR)."""


def compute_espvr(ESV: float, E_es: float, V_0: float) -> float:
    """
    Calculate end-systolic pressure from ESPVR.

    Parameters
    ----------
    ESV : float
        End-systolic volume (mL)
    E_es : float
        End-systolic elastance (mmHg/mL)
    V_0 : float
        Volume axis intercept (mL)

    Returns
    -------
    float
        End-systolic pressure (mmHg)
    """
    return E_es * (ESV - V_0)


espvr = create_equation(
    id="espvr",
    output_units='mmHg',
    produces="ESP",
    name="End-Systolic Pressure-Volume Relationship",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{ESP} = E_{es} \times (\text{ESV} - V_0)",
    simplified="ESP = E_es × (ESV - V_0)",
    description="Linear ESPVR defining contractility; E_es is index of contractility",
    compute_func=compute_espvr,
    parameters=[
        Parameter(
            name="ESV",
            description="End-systolic volume",
            units="mL",
            symbol="ESV",
            physiological_range=(30.0, 80.0)
        ),
        Parameter(
            name="E_es",
            description="End-systolic elastance",
            units="mmHg/mL",
            symbol="E_{es}",
            physiological_range=(1.5, 4.0)
        ),
        Parameter(
            name="V_0",
            description="Volume axis intercept",
            units="mL",
            symbol="V_0",
            physiological_range=(5.0, 20.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(espvr)

"""Fick principle for cardiac output measurement."""


def compute_cardiac_output_fick(VO2: float, C_aO2: float, C_vO2: float) -> float:
    """
    Calculate cardiac output using the Fick principle.

    Parameters
    ----------
    VO2 : float
        Oxygen consumption (mL O2/min)
    C_aO2 : float
        Arterial oxygen content (mL O2/dL)
    C_vO2 : float
        Mixed venous oxygen content (mL O2/dL)

    Returns
    -------
    float
        Cardiac output (L/min)
    """
    # Convert to L/min (C_aO2 and C_vO2 in dL units)
    return VO2 / ((C_aO2 - C_vO2) * 10.0)


cardiac_output_fick = create_equation(
    id="cardiac_output_fick",
    output_units='L/min',
    name="Cardiac Output (Fick Principle)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{CO} = \frac{\dot{V}O_2}{C_{aO_2} - C_{vO_2}}",
    simplified="CO = VO2 / (C_aO2 - C_vO2)",
    description="Cardiac output calculated from oxygen consumption and arteriovenous oxygen content difference",
    compute_func=compute_cardiac_output_fick,
    parameters=[
        Parameter(
            name="VO2",
            description="Oxygen consumption",
            units="mL O2/min",
            symbol=r"\dot{V}O_2",
            physiological_range=(200.0, 400.0)
        ),
        Parameter(
            name="C_aO2",
            description="Arterial oxygen content",
            units="mL O2/dL",
            symbol="C_{aO_2}",
            physiological_range=(18.0, 22.0)
        ),
        Parameter(
            name="C_vO2",
            description="Mixed venous oxygen content",
            units="mL O2/dL",
            symbol="C_{vO_2}",
            physiological_range=(14.0, 16.0)
        )
    ],
    depends_on=["blood_oxygen_content", "mixed_venous_oxygen_content"],  # C_aO2, C_vO2
    produces="CO",
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.3"
    )
)

register_equation(cardiac_output_fick)

__all__ = ['cardiac_output', 'cardiac_output_fick', 'ejection_fraction', 'body_surface_area', 'cardiac_index', 'espvr', 'edpvr']


# --- coverage pass additions (Feher extraction) ---

def compute_stroke_volume(EDV: float, ESV: float) -> float:
    """Stroke volume SV = EDV - ESV, the blood ejected per heartbeat (Feher 5.6, Ejection Phase). Volumes in mL, returns mL."""
    return EDV - ESV

stroke_volume = create_equation(
    id='stroke_volume',
    output_units='mL',
    name='Stroke Volume',
    category=EquationCategory.CARDIOVASCULAR,
    latex='\\mathrm{SV} = \\mathrm{EDV} - \\mathrm{ESV}',
    simplified='SV = EDV - ESV',
    description='Stroke volume: the volume of blood ejected from the ventricle with each heartbeat, computed as the difference between end-diastolic and end-systolic volume. Feher defines it in 5.6 (Ejection Phase; worked example 120 mL - 50 mL = 70 mL). It is the sole producer of the SV quantity in the package and feeds cardiac output (CO = HR x SV) and ejection fraction (EF = SV / EDV).',
    compute_func=compute_stroke_volume,
    parameters=[
        Parameter(name='EDV', description='End-diastolic volume (blood in the ventricle at the end of filling)', units='mL', symbol='EDV', physiological_range=(100, 150)),
        Parameter(name='ESV', description='End-systolic volume (blood remaining in the ventricle at the end of ejection)', units='mL', symbol='ESV', physiological_range=(40, 60)),
    ],
    depends_on=[],
    produces='SV',
    metadata=EquationMetadata(source_unit=5, source_chapter='5.6',
                              source_section='Ejection Phase (Summary of the Events in the Cardiac Cycle)', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(stroke_volume)


def compute_indicator_dilution_cardiac_output(m, area_under_curve):
    """Indicator (Stewart-Hamilton) dilution cardiac output, Feher Eq. 5.10.12: CO = m / integral_0^t(C_m dt).

    Cardiac output equals the injected indicator amount divided by the area under the
    downstream indicator concentration-time curve.

    Parameters
    ----------
    m : float
        Amount (mass or moles) of indicator injected [mg].
    area_under_curve : float
        Integral of indicator concentration over time, the area under the C_m vs t
        curve [mg*min/L].

    Returns
    -------
    float
        Cardiac output [L/min]. Units must be consistent: mass / (concentration*time)
        = volume/time, so mg / (mg*min/L) = L/min.
    """
    return m / area_under_curve

indicator_dilution_cardiac_output = create_equation(
    id='indicator_dilution_cardiac_output',
    output_units='L/min',
    produces="CO",
    name='Cardiac Output (Indicator Dilution / Stewart-Hamilton)',
    category=EquationCategory.CARDIOVASCULAR,
    latex='Q_{\\mathrm{a}} = \\dfrac{m}{\\int_0^t C_{\\mathrm{m}}\\,\\mathrm{d}t}',
    simplified='CO = m / integral(C_m dt)',
    description="Stewart-Hamilton indicator dilution method for measuring cardiac output: a known amount m of indicator is injected into a vein and its concentration C_m is recorded over time in arterial blood; cardiac output equals m divided by the area under the concentration-time curve. Distinct from the Fick principle (requires no O2 consumption measurement). The clinical thermal (thermo-) dilution method is the same relation with the injected quantity being the amount of 'cold' m*Cp*(T_blood - T_saline) and the denominator the temperature-time integral. The area under the curve can be overestimated by recirculation, corrected by exponential extrapolation of the decay phase.",
    compute_func=compute_indicator_dilution_cardiac_output,
    parameters=[
        Parameter(name='m', description='Amount (mass or moles) of indicator injected as a bolus into the venous side of the circulation', units='mg', symbol='m', physiological_range=(0.5, 50)),
        Parameter(name='area_under_curve', description='Area under the indicator concentration-time curve (integral of C_m over t), measured downstream in arterial blood; units mg*min/L so that m/AUC yields L/min', units='mg·min/L', symbol='\\int_0^t C_m\\,dt', physiological_range=(0.1, 20)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=5, source_chapter='5.10',
                              source_section='CARDIAC OUTPUT CAN BE DETERMINED BY THE INDICATOR DILUTION METHOD', page_reference=None,
                              textbook_equation_number='5.10.12'),
)
register_equation(indicator_dilution_cardiac_output)

try:
    __all__ += ['stroke_volume', 'indicator_dilution_cardiac_output']
except NameError:
    __all__ = ['stroke_volume', 'indicator_dilution_cardiac_output']


# --- clinical additions (CICM, beyond Feher) ---

def compute_arterial_elastance(ESP, SV):
    """Effective arterial elastance Ea = ESP/SV (mmHg/mL); paired with Ees for ventriculo-arterial coupling."""
    return ESP / SV

arterial_elastance = create_equation(
    id='arterial_elastance',
    output_units='mmHg/mL',
    name='Arterial Elastance',
    category=EquationCategory.CARDIOVASCULAR,
    latex='E_a = \\frac{ESP}{SV}',
    simplified='Ea = ESP/SV',
    description='Effective arterial elastance: the arterial-load counterpart of ventricular end-systolic elastance (Ees). Optimal ventriculo-arterial coupling and stroke work occur near Ea/Ees ~ 1.',
    compute_func=compute_arterial_elastance,
    parameters=[
        Parameter(name='ESP', description='End-systolic (arterial) pressure', units='mmHg', symbol='ESP', physiological_range=(50, 200)),
        Parameter(name='SV', description='Stroke volume', units='mL', symbol='SV', physiological_range=(20, 150)),
    ],
    depends_on=["stroke_volume", "espvr"],
    produces='Ea',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(arterial_elastance)

try:
    __all__ += ['arterial_elastance']
except NameError:
    __all__ = ['arterial_elastance']


# --- backlog-complete-add 2026-07-15 ---
def compute_frank_starling(M_w: float, EDV: float, V_w: float) -> float:
    """Preload-recruitable stroke work: SW = M_w*(EDV - V_w) (linear PRSW relation)."""
    return M_w * (EDV - V_w)

frank_starling_equation = create_equation(
    id="frank_starling", name="Frank-Starling (Preload-Recruitable Stroke Work)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"SW = M_w\,(EDV - V_w)", simplified="SW = M_w*(EDV - V_w)",
    description="Preload-recruitable stroke work: stroke work rises linearly with end-diastolic volume; slope M_w (mmHg) is a load-independent contractility index, V_w the volume-axis intercept.",
    compute_func=compute_frank_starling, output_units="mmHg*mL",
    parameters=[Parameter(name="M_w", description="PRSW slope (contractility)", units="mmHg", symbol="M_w", physiological_range=(40, 110)),
                Parameter(name="EDV", description="End-diastolic volume", units="mL", symbol="EDV", physiological_range=(60, 250)),
                Parameter(name="V_w", description="Volume-axis intercept", units="mL", symbol="V_w", physiological_range=(0, 60))],
    metadata=EquationMetadata(source_unit=5, source_chapter="5.9"),
)
register_equation(frank_starling_equation)


# --- backlog-complete-add 2026-07-15 ---
def compute_va_coupling_esv(Ea: float, EDV: float, Ees: float, V0: float) -> float:
    """Ventriculo-arterial coupling ESV = (Ea*EDV + Ees*V0)/(Ees + Ea)
    (PV-loop intersection of the arterial elastance line and ESPVR)."""
    return (Ea * EDV + Ees * V0) / (Ees + Ea)

va_coupling_esv_equation = create_equation(
    id="va_coupling_esv", name="Ventriculo-Arterial Coupling (Operating ESV)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"ESV = \frac{E_a EDV + E_{es} V_0}{E_{es} + E_a}", simplified="ESV = (Ea*EDV + Ees*V0)/(Ees+Ea)",
    description="Operating end-systolic volume from the intersection of the arterial elastance line (Ea) and ESPVR (Ees, V0) given preload EDV; SV = EDV - ESV closes the loop.",
    compute_func=compute_va_coupling_esv, output_units="mL", produces="ESV",
    parameters=[Parameter(name="Ea", description="Arterial elastance", units="mmHg/mL", symbol="Ea", physiological_range=(0.5, 5)),
                Parameter(name="EDV", description="End-diastolic volume", units="mL", symbol="EDV", physiological_range=(60, 250)),
                Parameter(name="Ees", description="End-systolic elastance (contractility)", units="mmHg/mL", symbol="Ees", physiological_range=(0.5, 6)),
                Parameter(name="V0", description="ESPVR volume intercept", units="mL", symbol="V0", physiological_range=(0, 30))],
    depends_on=["arterial_elastance"],   # Ea from arterial_elastance (produces 'Ea')
    metadata=EquationMetadata(source_unit=5, source_chapter="5.9"),
)
register_equation(va_coupling_esv_equation)

"""Blood composition and oxygen transport equations."""

"""Blood viscosity as function of hematocrit."""

import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_blood_viscosity(Hct: float, eta_plasma: float = 1.2) -> float:
    """
    Calculate blood viscosity based on hematocrit.

    Parameters
    ----------
    Hct : float
        Hematocrit (0-1)
    eta_plasma : float, optional
        Plasma viscosity in mPa·s (default: 1.2)

    Returns
    -------
    float
        Blood viscosity (mPa·s)
    """
    k = 2.5
    return eta_plasma * np.exp(k * Hct)


blood_viscosity = create_equation(
    id="blood_viscosity",
    output_units='mPa*s',
    name="Blood Viscosity",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\eta_{\text{blood}} = \eta_{\text{plasma}} \times e^{k \times \text{Hct}}",
    simplified="η_blood = η_plasma × exp(2.5 × Hct)",
    description="Blood viscosity increases exponentially with hematocrit",
    compute_func=compute_blood_viscosity,
    parameters=[
        Parameter(
            name="Hct",
            description="Hematocrit",
            units="dimensionless",
            symbol=r"\text{Hct}",
            physiological_range=(0.36, 0.54)
        ),
        Parameter(
            name="eta_plasma",
            description="Plasma viscosity",
            units="mPa·s",
            symbol=r"\eta_{\text{plasma}}",
            default_value=1.2,
            physiological_range=(1.1, 1.3)
        )
    ],
    depends_on=["hematocrit"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(blood_viscosity)

"""Hematocrit definition equation."""


def compute_hematocrit(V_RBC: float, V_blood: float) -> float:
    """
    Calculate hematocrit as volume fraction of red blood cells.

    Parameters
    ----------
    V_RBC : float
        Volume of red blood cells (mL)
    V_blood : float
        Total blood volume (mL)

    Returns
    -------
    float
        Hematocrit (0-1)
    """
    return V_RBC / V_blood


hematocrit = create_equation(
    id="hematocrit",
    output_units='dimensionless',
    name="Hematocrit",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"\text{Hct} = \frac{V_{\text{RBC}}}{V_{\text{blood}}}",
    simplified="Hct = V_RBC / V_blood",
    description="Volume fraction of red blood cells in whole blood",
    compute_func=compute_hematocrit,
    parameters=[
        Parameter(
            name="V_RBC",
            description="Volume of red blood cells",
            units="mL",
            symbol="V_{RBC}",
            physiological_range=(1500, 3000)
        ),
        Parameter(
            name="V_blood",
            description="Total blood volume",
            units="mL",
            symbol="V_{blood}",
            physiological_range=(4000, 6000)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(hematocrit)

"""Hill equation for hemoglobin oxygen saturation."""


def compute_hill_saturation(P_O2: float, P_50: float = 26.0, n: float = 2.7) -> float:
    """
    Calculate hemoglobin oxygen saturation using Hill equation.

    Parameters
    ----------
    P_O2 : float
        Partial pressure of oxygen (mmHg)
    P_50 : float, optional
        Half-saturation pressure (mmHg, default: 26)
    n : float, optional
        Hill coefficient (default: 2.7)

    Returns
    -------
    float
        Oxygen saturation (0-1)
    """
    return (P_O2 ** n) / (P_50 ** n + P_O2 ** n)


hill_saturation = create_equation(
    id="hill_saturation",
    output_units='dimensionless',
    name="Hill Equation for Hemoglobin",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"S_{O_2} = \frac{P_{O_2}^n}{P_{50}^n + P_{O_2}^n}",
    simplified="S_O2 = P_O2^n / (P_50^n + P_O2^n)",
    description="Sigmoid oxygen-hemoglobin dissociation curve",
    compute_func=compute_hill_saturation,
    parameters=[
        Parameter(
            name="P_O2",
            description="Partial pressure of oxygen",
            units="mmHg",
            symbol="P_{O_2}",
            physiological_range=(0.0, 150.0)
        ),
        Parameter(
            name="P_50",
            description="Half-saturation pressure",
            units="mmHg",
            symbol="P_{50}",
            default_value=26.0,
            physiological_range=(20.0, 30.0)
        ),
        Parameter(
            name="n",
            description="Hill coefficient (cooperativity)",
            units="dimensionless",
            symbol="n",
            default_value=2.7,
            physiological_range=(2.0, 3.5)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(hill_saturation)

"""Blood oxygen content equation."""


def compute_oxygen_content(Hb: float, S_O2: float, P_O2: float) -> float:
    """
    Calculate total oxygen content in blood.

    Parameters
    ----------
    Hb : float
        Hemoglobin concentration (g/dL)
    S_O2 : float
        Oxygen saturation (0-1)
    P_O2 : float
        Partial pressure of oxygen (mmHg)

    Returns
    -------
    float
        Oxygen content (mL O2/dL blood)
    """
    HUFNER_CONSTANT = 1.34  # mL O2/g Hb
    SOLUBILITY = 0.003  # mL O2/(dL·mmHg)

    bound = HUFNER_CONSTANT * Hb * S_O2
    dissolved = SOLUBILITY * P_O2

    return bound + dissolved


oxygen_content = create_equation(
    id="blood_oxygen_content",
    produces='CaO2',
    output_units='mL/dL',
    name="Blood Oxygen Content (Cardiovascular)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"C_{O_2} = (1.34 \times \text{Hb} \times S_{O_2}) + (0.003 \times P_{O_2})",
    simplified="C_O2 = (1.34 × Hb × S_O2) + (0.003 × P_O2)",
    description="Total oxygen content in blood: bound to hemoglobin plus dissolved",
    compute_func=compute_oxygen_content,
    parameters=[
        Parameter(
            name="Hb",
            description="Hemoglobin concentration",
            units="g/dL",
            symbol=r"\text{Hb}",
            physiological_range=(12.0, 18.0)
        ),
        Parameter(
            name="S_O2",
            description="Oxygen saturation",
            units="dimensionless",
            symbol="S_{O_2}",
            physiological_range=(0.7, 1.0)
        ),
        Parameter(
            name="P_O2",
            description="Partial pressure of oxygen",
            units="mmHg",
            symbol="P_{O_2}",
            physiological_range=(35.0, 100.0)
        )
    ],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(oxygen_content)

"""Oxygen delivery rate equation."""


def compute_oxygen_delivery(CO: float, Hb: float, S_O2: float) -> float:
    """
    Calculate systemic oxygen delivery rate.

    Parameters
    ----------
    CO : float
        Cardiac output (L/min)
    Hb : float
        Hemoglobin concentration (g/dL)
    S_O2 : float
        Arterial oxygen saturation (0-1)

    Returns
    -------
    float
        Oxygen delivery (mL O2/min)
    """
    HUFNER_CONSTANT = 1.34  # mL O2/g Hb

    # CO in L/min, Hb in g/dL → multiply by 10 to get mL/min
    return CO * HUFNER_CONSTANT * Hb * S_O2 * 10


oxygen_delivery = create_equation(
    id="systemic_oxygen_delivery",
    output_units='mL/min',
    name="Systemic Oxygen Delivery (Cardiovascular)",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"DO_2 = CO \times (1.34 \times \text{Hb} \times S_{O_2}) \times 10",
    simplified="DO2 = CO × (1.34 × Hb × S_O2) × 10  # ×10: (mL/dL)×(L/min)→mL/min",
    description="Systemic oxygen delivery rate, product of cardiac output and arterial oxygen content",
    compute_func=compute_oxygen_delivery,
    parameters=[
        Parameter(
            name="CO",
            description="Cardiac output",
            units="L/min",
            symbol="CO",
            physiological_range=(4.0, 8.0)
        ),
        Parameter(
            name="Hb",
            description="Hemoglobin concentration",
            units="g/dL",
            symbol=r"\text{Hb}",
            physiological_range=(12.0, 18.0)
        ),
        Parameter(
            name="S_O2",
            description="Arterial oxygen saturation",
            units="dimensionless",
            symbol="S_{O_2}",
            physiological_range=(0.95, 1.0)
        )
    ],
    depends_on=["blood_oxygen_content", "cardiac_output", "cardiac_output_fick", "indicator_dilution_cardiac_output"],
    metadata=EquationMetadata(
        source_unit=5,
        source_chapter="5.1"
    )
)

register_equation(oxygen_delivery)

__all__ = ['hematocrit', 'blood_viscosity', 'oxygen_content', 'hill_saturation', 'oxygen_delivery']


# --- coverage pass additions (Feher extraction) ---

def compute_mean_cell_volume(Hct_ratio, n_rbc):
    """Mean cell volume MCV (fL/cell) = hematocrit ratio / RBC numerical density.

    Hct_ratio is dimensionless (packed-cell fraction, 0-1); n_rbc is the red-cell
    numerical density in cells per litre (cells/L). Returns MCV in femtolitres per
    cell (fL/cell). Source: Feher 3rd ed., EXAMPLE 5.2.1 (5.2 Plasma and Red Blood
    Cells): MCV = Hct ratio / numerical density of cells.
    """
    litres_per_cell = Hct_ratio / n_rbc  # (dimensionless) / (cells/L) = L/cell
    return litres_per_cell * 1e15        # L -> fL

mean_cell_volume = create_equation(
    id='mean_cell_volume',
    output_units='fL',
    name='Mean Cell Volume (MCV)',
    category=EquationCategory.CARDIOVASCULAR,
    latex='\\mathrm{MCV} = \\frac{\\mathrm{Hct\\ ratio}}{n}',
    simplified='MCV = Hct_ratio / n_rbc   (result x 1e15 to give fL/cell)',
    description='Mean cell volume: the average volume of a single red blood cell, obtained by dividing the hematocrit ratio by the red-cell numerical density. A standard red-cell index (normal 80-95 fL/cell) used clinically to classify anemias as microcytic (small cells), normocytic, or macrocytic (large cells). Distinct from MCH and MCHC.',
    compute_func=compute_mean_cell_volume,
    parameters=[
        Parameter(name='Hct_ratio', description='Hematocrit expressed as a fraction (packed-cell volume / total blood volume, not multiplied by 100)', units='dimensionless', symbol='\\text{Hct}', physiological_range=(0.15, 0.75)),
        Parameter(name='n_rbc', description='Red blood cell numerical density (cell count per unit volume of blood)', units='cells/L', symbol='n', physiological_range=(3000000000000, 7000000000000)),
    ],
    depends_on=['hematocrit'],
    produces='MCV',
    metadata=EquationMetadata(source_unit=5, source_chapter='5.2',
                              source_section='EXAMPLE 5.2.1 Calculate the Mean Cell Volume', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(mean_cell_volume)


def compute_mean_corpuscular_hemoglobin_concentration(Hb_blood, Hct):
    """MCHC = whole-blood hemoglobin concentration / hematocrit ratio (Feher EXAMPLE 5.2.2, sec 5.2). Hb_blood in g/L, Hct dimensionless fraction; returns MCHC in g/L."""
    return Hb_blood / Hct

mean_corpuscular_hemoglobin_concentration = create_equation(
    id='mean_corpuscular_hemoglobin_concentration',
    output_units='g/L',
    name='Mean Corpuscular Hemoglobin Concentration',
    category=EquationCategory.CARDIOVASCULAR,
    latex='\\mathrm{MCHC} = \\frac{[\\mathrm{Hb}]_{\\text{whole blood}}}{\\mathrm{Hct}}',
    simplified='MCHC = Hb_blood / Hct',
    description='Mean corpuscular hemoglobin concentration: the average hemoglobin concentration within packed red cells, obtained by dividing whole-blood hemoglobin concentration by the hematocrit. A standard red-cell index used clinically to classify anemias as hypochromic (low MCHC) or normochromic (normal MCHC). Normal range ~320-360 g/L.',
    compute_func=compute_mean_corpuscular_hemoglobin_concentration,
    parameters=[
        Parameter(name='Hb_blood', description='Whole-blood hemoglobin concentration', units='g/L', symbol='[Hb]', physiological_range=(20, 250)),
        Parameter(name='Hct', description='Hematocrit ratio (fraction of blood volume occupied by red cells)', units='dimensionless', symbol='Hct', physiological_range=(0.1, 0.7)),
    ],
    depends_on=['hematocrit'],
    produces='MCHC',
    metadata=EquationMetadata(source_unit=5, source_chapter='5.2',
                              source_section='EXAMPLE 5.2.2 Calculate the Mean Corpuscular Hemoglobin Concentration and HB Content', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(mean_corpuscular_hemoglobin_concentration)


def compute_plasma_buffer_capacity(delta_acid: float, delta_pH: float) -> float:
    """Plasma buffer capacity (van Slyke buffer value), Feher 5.2:
    beta = delta_acid / delta_pH.

    Parameters
    ----------
    delta_acid : float
        Strong acid added to (or removed from) plasma (mEq/L, magnitude).
    delta_pH : float
        Magnitude of the resulting change in plasma pH (pH units).

    Returns
    -------
    float
        Buffer capacity in mEq/L per pH unit (normal plasma ~16).
    """
    return delta_acid / delta_pH

plasma_buffer_capacity = create_equation(
    id='plasma_buffer_capacity',
    output_units='mEq/(L*pH)',
    name='Plasma Buffer Capacity (van Slyke)',
    category=EquationCategory.CARDIOVASCULAR,
    latex='\\beta = \\dfrac{\\Delta\\,\\text{acid}}{\\Delta\\,\\text{pH}}',
    simplified='beta = delta_acid / delta_pH',
    description='Buffer capacity (van Slyke buffer value) of plasma: the amount of strong acid (or base) needed to change plasma pH by one unit. Feher defines it as delta_acid/delta_pH; normal plasma buffer capacity is about 16 mEq/L per pH unit. A higher buffer capacity means plasma resists pH change more strongly for a given acid load. Structurally analogous to the compliance/elastance/capacitance susceptibility definitions already in the package.',
    compute_func=compute_plasma_buffer_capacity,
    parameters=[
        Parameter(name='delta_acid', description='Strong acid added to (or removed from) plasma (magnitude of the acid load)', units='mEq/L', symbol='\\Delta\\,\\text{acid}', physiological_range=(1, 40)),
        Parameter(name='delta_pH', description='Magnitude of the resulting change in plasma pH', units='pH units', symbol='\\Delta\\,\\text{pH}', physiological_range=(0.01, 2)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=5, source_chapter='5.2',
                              source_section='PLASMA PROTEINS AND IONS BUFFER CHANGES IN PLASMA PH', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(plasma_buffer_capacity)


def compute_mean_corpuscular_hemoglobin(Hb_conc, rbc_count):
    """MCH (pg/cell) = whole-blood hemoglobin concentration divided by RBC numerical density.

    Third red-cell index (Feher EXAMPLE 5.2.2, section 5.2). Hb_conc in g/L,
    rbc_count in 10^12 cells/L; the ratio (g/L)/(10^12 cells/L) = 10^-12 g/cell = pg/cell.
    Feher example: 150 g/L / 5(x10^12/L) = 30 pg/cell (normal 27-34 pg/cell).
    """
    return Hb_conc / rbc_count

mean_corpuscular_hemoglobin = create_equation(
    id='mean_corpuscular_hemoglobin',
    output_units='pg',
    name='Mean Corpuscular Hemoglobin',
    category=EquationCategory.CARDIOVASCULAR,
    latex='\\mathrm{MCH} = \\frac{[\\mathrm{Hb}]_{\\text{whole blood}}}{n}',
    simplified='MCH = [Hb]_whole_blood / n',
    description='Mean corpuscular hemoglobin (MCH): the average mass of hemoglobin per red blood cell, calculated as the whole-blood hemoglobin concentration divided by the red-cell numerical density. The third red-cell index alongside MCV (volume/cell) and MCHC (concentration); distinct output quantity (mass of Hb per cell, pg). Normal range 27-34 pg/cell. Used clinically to classify anemias as hypochromic (reduced MCH) or normochromic (normal MCH).',
    compute_func=compute_mean_corpuscular_hemoglobin,
    parameters=[
        Parameter(name='Hb_conc', description='Whole-blood hemoglobin concentration', units='g/L', symbol='[\\mathrm{Hb}]', physiological_range=(100, 200)),
        Parameter(name='rbc_count', description='Red blood cell numerical density (count per volume of whole blood)', units='10^12 cells/L', symbol='n', physiological_range=(3.5, 6.5)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=5, source_chapter='5.2',
                              source_section='EXAMPLE 5.2.2 Calculate the Mean Corpuscular Hemoglobin Concentration and HB Content', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(mean_corpuscular_hemoglobin)


def compute_transferrin_saturation(serum_iron, TIBC):
    """Transferrin saturation as a percentage: TSAT = serum iron / TIBC x 100.

    Feher 5.2, 'Transferrin carries ferric iron in the plasma'. serum_iron and
    TIBC must be given in the SAME concentration units (e.g. both in uM); their
    ratio is dimensionless and x100 converts it to percent. Returns TSAT in %.
    Normal ~30% (serum iron ~10-30 uM occupying TIBC ~45-80 uM of binding sites).
    """
    return (serum_iron / TIBC) * 100.0

transferrin_saturation = create_equation(
    id='transferrin_saturation',
    output_units='%',
    name='Transferrin Saturation',
    category=EquationCategory.CARDIOVASCULAR,
    latex='\\mathrm{TSAT} = \\dfrac{\\text{serum iron}}{\\mathrm{TIBC}} \\times 100',
    simplified='TSAT = serum_iron / TIBC * 100',
    description='Transferrin saturation (TSAT): the percentage of transferrin iron-binding sites occupied by iron, computed as serum iron divided by total iron-binding capacity (TIBC), times 100. A named clinical index of iron status used across iron-metabolism problems; normal is about 30%. It is reduced in iron-deficiency states (typically <15%) and elevated in iron overload / hemochromatosis (typically >45%). Feher gives the identity TSAT = serum iron / TIBC = serum iron / ([transferrin] x conversion factor) x 100 (conversion factor 25 when [transferrin] is in g/L and TIBC in uM); the [transferrin]-based denominator is a unit-dependent restatement of the same relation.',
    compute_func=compute_transferrin_saturation,
    parameters=[
        Parameter(name='serum_iron', description='Total serum iron concentration (iron actually bound to transferrin). Low in iron deficiency, high in iron overload.', units='uM', symbol='\\text{Fe}_{\\text{serum}}', physiological_range=(2, 45)),
        Parameter(name='TIBC', description='Total iron-binding capacity of plasma transferrin (equals [transferrin] x conversion factor). Measured or calculated clinically.', units='uM', symbol='\\mathrm{TIBC}', physiological_range=(30, 90)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=5, source_chapter='5.2',
                              source_section='TRANSFERRIN CARRIES FERRIC IRON IN THE PLASMA', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(transferrin_saturation)

try:
    __all__ += ['mean_cell_volume', 'mean_corpuscular_hemoglobin_concentration', 'plasma_buffer_capacity', 'mean_corpuscular_hemoglobin', 'transferrin_saturation']
except NameError:
    __all__ = ['mean_cell_volume', 'mean_corpuscular_hemoglobin_concentration', 'plasma_buffer_capacity', 'mean_corpuscular_hemoglobin', 'transferrin_saturation']


# --- backlog-complete-add 2026-07-15 ---
def compute_mixed_venous_oxygen_content(Hb: float, S_vO2: float, P_vO2: float) -> float:
    """Mixed venous O2 content CvO2 = 1.34*Hb*SvO2 + 0.003*PvO2 (mL/dL)."""
    return 1.34 * Hb * S_vO2 + 0.003 * P_vO2

mixed_venous_oxygen_content_equation = create_equation(
    id="mixed_venous_oxygen_content", name="Mixed Venous Oxygen Content",
    category=EquationCategory.CARDIOVASCULAR,
    latex=r"CvO_2 = 1.34\,Hb\,S_{vO_2} + 0.003\,P_{vO_2}", simplified="CvO2 = 1.34*Hb*SvO2 + 0.003*PvO2",
    description="Mixed venous oxygen content (same physics as arterial, venous inputs); supplies the venous limb for Fick VO2, extraction ratio and shunt.",
    compute_func=compute_mixed_venous_oxygen_content, output_units="mL/dL", produces="CvO2",
    parameters=[Parameter(name="Hb", description="Hemoglobin", units="g/dL", symbol="Hb", physiological_range=(5, 20)),
                Parameter(name="S_vO2", description="Mixed venous O2 saturation", units="dimensionless", symbol="SvO2", physiological_range=(0.4, 0.9)),
                Parameter(name="P_vO2", description="Mixed venous O2 tension", units="mmHg", symbol="PvO2", physiological_range=(20, 60))],
    metadata=EquationMetadata(source_unit=5, source_chapter="5.6"),
)
register_equation(mixed_venous_oxygen_content_equation)

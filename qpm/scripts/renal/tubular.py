"""Consolidated module for renal.tubular."""

"""
Mass balance equation for excretion.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_excretion(GFR: float, P_x: float, R_x: float, S_x: float) -> float:
    """
    Calculate excretion using mass balance.

    Args:
        GFR: Glomerular filtration rate (mL/min)
        P_x: Plasma concentration (mg/dL or mmol/L)
        R_x: Amount reabsorbed (mg/min or mmol/min)
        S_x: Amount secreted (mg/min or mmol/min)

    Returns:
        Excretion: Amount excreted per unit time (mg/min or mmol/min)
    """
    filtration = GFR * P_x / 100.0  # mg/dL -> mg/mL so mL/min*mg/mL = mg/min
    return filtration - R_x + S_x


# Create equation
excretion_mass_balance = create_equation(
    id="excretion_mass_balance",
    output_units='mg/min',
    name="Excretion Mass Balance",
    category=EquationCategory.RENAL,
    latex=r"Excretion = Filtration - Reabsorption + Secretion",
    simplified="Excretion = GFR × P_x - R_x + S_x",
    description="Mass balance relating filtration, reabsorption, secretion, and excretion",
    compute_func=compute_excretion,
    parameters=[
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        ),
        Parameter(
            name="P_x",
            description="Plasma concentration of substance",
            units="mg/dL or mmol/L",
            symbol="P_x",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="R_x",
            description="Amount reabsorbed",
            units="mg/min or mmol/min",
            symbol="R_x",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="S_x",
            description="Amount secreted",
            units="mg/min or mmol/min",
            symbol="S_x",
            physiological_range=(0, 100)
        )
    ],
    depends_on=["filtered_load", "gfr_from_nfp"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equation
register_equation(excretion_mass_balance)

"""
Fractional excretion of sodium (FE_Na).

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_fe_na(U_Na: float, P_Cr: float, P_Na: float, U_Cr: float) -> float:
    """
    Calculate fractional excretion of sodium.

    Uses creatinine to normalize for GFR without directly measuring it.

    Args:
        U_Na: Urine sodium concentration (mmol/L)
        P_Cr: Plasma creatinine concentration (mg/dL)
        P_Na: Plasma sodium concentration (mmol/L)
        U_Cr: Urine creatinine concentration (mg/dL)

    Returns:
        FE_Na: Fractional excretion of sodium (%)
    """
    return (U_Na * P_Cr) / (P_Na * U_Cr) * 100


# Create equation
fe_na = create_equation(
    id="fe_na",
    output_units='%',
    name="Fractional Excretion of Sodium",
    category=EquationCategory.RENAL,
    latex=r"FE_{Na} = \frac{U_{Na} \times P_{Cr}}{P_{Na} \times U_{Cr}} \times 100\%",
    simplified="FE_Na = (U_Na × P_Cr) / (P_Na × U_Cr) × 100%",
    description="Fraction of filtered sodium excreted; distinguishes prerenal from intrinsic renal failure",
    compute_func=compute_fe_na,
    parameters=[
        Parameter(
            name="U_Na",
            description="Urine sodium concentration",
            units="mmol/L",
            symbol="U_{Na}",
            physiological_range=(10, 200)
        ),
        Parameter(
            name="P_Cr",
            description="Plasma creatinine concentration",
            units="mg/dL",
            symbol="P_{Cr}",
            physiological_range=(0.5, 5.0)
        ),
        Parameter(
            name="P_Na",
            description="Plasma sodium concentration",
            units="mmol/L",
            symbol="P_{Na}",
            physiological_range=(135, 145)
        ),
        Parameter(
            name="U_Cr",
            description="Urine creatinine concentration",
            units="mg/dL",
            symbol="U_{Cr}",
            physiological_range=(20, 300)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equation
register_equation(fe_na)

"""
Fractional excretion calculation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_fractional_excretion(C_x: float, GFR: float) -> float:
    """
    Calculate fractional excretion from clearance.

    Args:
        C_x: Clearance of substance x (mL/min)
        GFR: Glomerular filtration rate (mL/min)

    Returns:
        FE_x: Fractional excretion (dimensionless, as fraction)
    """
    return C_x / GFR


def compute_fractional_excretion_direct(U_x: float, V_dot: float, GFR: float, P_x: float) -> float:
    """
    Calculate fractional excretion directly from measurements.

    Args:
        U_x: Urine concentration of substance
        V_dot: Urine flow rate (mL/min)
        GFR: Glomerular filtration rate (mL/min)
        P_x: Plasma concentration of substance

    Returns:
        FE_x: Fractional excretion (dimensionless, as fraction)
    """
    return (U_x * V_dot) / (GFR * P_x)


# Create equation (clearance method)
fractional_excretion = create_equation(
    id="fractional_excretion",
    output_units='dimensionless',
    name="Fractional Excretion",
    category=EquationCategory.RENAL,
    latex=r"FE_x = \frac{C_x}{GFR}",
    simplified="FE_x = C_x / GFR",
    description="Fraction of filtered substance that is excreted in urine",
    compute_func=compute_fractional_excretion,
    parameters=[
        Parameter(
            name="C_x",
            description="Clearance of substance x",
            units="mL/min",
            symbol="C_x",
            physiological_range=(0, 200)
        ),
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        )
    ],
    depends_on=["clearance", "gfr_from_nfp"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Create direct calculation equation
fractional_excretion_direct = create_equation(
    id="fractional_excretion_direct",
    output_units='dimensionless',
    name="Fractional Excretion (Direct)",
    category=EquationCategory.RENAL,
    latex=r"FE_x = \frac{U_x \times \dot{V}}{GFR \times P_x}",
    simplified="FE_x = (U_x × V̇) / (GFR × P_x)",
    description="Direct calculation of fractional excretion from urine and plasma measurements",
    compute_func=compute_fractional_excretion_direct,
    parameters=[
        Parameter(
            name="U_x",
            description="Urine concentration of substance",
            units="mg/dL or mmol/L",
            symbol="U_x",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="V_dot",
            description="Urine flow rate",
            units="mL/min",
            symbol=r"\dot{V}",
            physiological_range=(0.5, 20)
        ),
        Parameter(
            name="GFR",
            description="Glomerular filtration rate",
            units="mL/min",
            symbol="GFR",
            physiological_range=(90, 140)
        ),
        Parameter(
            name="P_x",
            description="Plasma concentration of substance",
            units="mg/dL or mmol/L",
            symbol="P_x",
            physiological_range=(0, 1000)
        )
    ],
    depends_on=["gfr_from_nfp"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equations
register_equation(fractional_excretion)
register_equation(fractional_excretion_direct)

"""
Glucose excretion calculation considering Tm limitation.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_glucose_excretion(filtered_load: float, T_max: float = 375.0) -> float:
    """
    Calculate glucose excretion based on filtered load and transport maximum.

    Args:
        filtered_load: Glucose filtered load (mg/min)
        T_max: Maximum glucose reabsorption rate (mg/min, default 375)

    Returns:
        excretion: Glucose excreted in urine (mg/min)
    """
    if filtered_load <= T_max:
        return 0.0  # All glucose reabsorbed
    else:
        return filtered_load - T_max


# Create equation
glucose_excretion = create_equation(
    id="glucose_excretion",
    output_units='mg/min',
    name="Glucose Excretion",
    category=EquationCategory.RENAL,
    latex=r"Excretion = \begin{cases} 0 & \text{if } FL \leq T_{max} \\ FL - T_{max} & \text{if } FL > T_{max} \end{cases}",
    simplified="Excretion = max(0, FL - T_max)",
    description="Glucose excretion occurs only when filtered load exceeds transport maximum",
    compute_func=compute_glucose_excretion,
    parameters=[
        Parameter(
            name="filtered_load",
            description="Glucose filtered load",
            units="mg/min",
            symbol="FL",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="T_max",
            description="Maximum glucose reabsorption rate",
            units="mg/min",
            symbol="T_{max}",
            default_value=375.0,
            physiological_range=(300, 450)
        )
    ],
    depends_on=["filtered_load"],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equation
register_equation(glucose_excretion)

"""
Transport maximum (Tm) - Saturable transport kinetics.

Source: Quantitative Human Physiology 3rd Edition
Unit 7: Renal Physiology
"""


def compute_transport_tm(T_max: float, S: float, K_m: float) -> float:
    """
    Calculate saturable transport rate using Michaelis-Menten kinetics.

    Args:
        T_max: Maximum transport rate
        S: Substrate concentration
        K_m: Michaelis constant (concentration at half-maximal transport)

    Returns:
        T: Transport rate
    """
    return T_max * S / (K_m + S)


# Create equation
transport_tm = create_equation(
    id="transport_tm",
    output_units='mg/min',
    name="Transport Maximum (Michaelis-Menten)",
    category=EquationCategory.RENAL,
    latex=r"T = \frac{T_{max} \times [S]}{K_m + [S]}",
    simplified="T = T_max × [S] / (K_m + [S])",
    description="Saturable carrier-mediated transport following Michaelis-Menten kinetics",
    compute_func=compute_transport_tm,
    parameters=[
        Parameter(
            name="T_max",
            description="Maximum transport rate",
            units="mg/min or mmol/min",
            symbol="T_{max}",
            physiological_range=(100, 500)
        ),
        Parameter(
            name="S",
            description="Substrate concentration",
            units="mg/dL or mmol/L",
            symbol="[S]",
            physiological_range=(0, 1000)
        ),
        Parameter(
            name="K_m",
            description="Michaelis constant",
            units="mg/dL or mmol/L",
            symbol="K_m",
            physiological_range=(1, 100)
        )
    ],
    depends_on=[],
    metadata=EquationMetadata(
        source_unit=7,
        source_chapter="7.3"
    )
)

# Register equation
register_equation(transport_tm)



# --- coverage pass additions (Feher extraction) ---

def compute_fractional_water_reabsorption(TF_P_inulin):
    """Fraction of filtered water reabsorbed from the glomerulus up to a tubular
    sampling point: V_R/V_T = 1 - 1/(TF/P)_inulin (Feher 7.4, Eqn 7.4.15).

    Because inulin is freely filtered (sieving coefficient 1.0) but neither
    reabsorbed nor secreted, water removal concentrates it; the tubular-fluid-to-
    plasma inulin ratio therefore marks the fraction of water reabsorbed.

    Args:
        TF_P_inulin: dimensionless tubular-fluid-to-plasma inulin concentration
                     ratio at the sampling point (=1 in Bowman's space, rises
                     downstream; ~3 at the end of the proximal tubule).

    Returns:
        Dimensionless fraction of filtered water reabsorbed (0 at TF/P=1,
        approaching 1 as TF/P grows large).
    """
    return 1.0 - 1.0 / TF_P_inulin

fractional_water_reabsorption = create_equation(
    id='fractional_water_reabsorption',
    output_units='dimensionless',
    name='Fractional Water Reabsorption from (TF/P)inulin',
    category=EquationCategory.RENAL,
    latex='\\dfrac{V_R}{V_T} = 1 - \\dfrac{1}{(\\mathrm{TF}/P)_{inulin}}',
    simplified='V_R/V_T = 1 - 1/(TF/P)_inulin',
    description='Fraction of filtered water reabsorbed from the glomerulus up to a tubular sampling point, inferred from the tubular-fluid-to-plasma inulin concentration ratio. Inulin is freely filtered but neither reabsorbed nor secreted, so water reabsorption concentrates it and (TF/P)_inulin rises above 1; the reabsorbed water fraction is V_R/V_T = 1 - 1/(TF/P)_inulin. At the end of the proximal tubule (TF/P)_inulin is about 3, giving ~2/3 (67%) water reabsorption. Used in micropuncture analysis to localise where along the nephron water is reabsorbed, requiring only paired plasma and tubular-fluid inulin measurements.',
    compute_func=compute_fractional_water_reabsorption,
    parameters=[
        Parameter(name='TF_P_inulin', description="Tubular-fluid-to-plasma inulin concentration ratio at the tubular sampling point; equals 1 in Bowman's space and rises as water is reabsorbed (~3 at end of proximal tubule)", units='dimensionless', symbol='(TF/P)_{inulin}', physiological_range=(1, 200)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=7, source_chapter='7.4',
                              source_section='(TF/P)inulin MARKS WATER REABSORPTION', page_reference=None,
                              textbook_equation_number='7.4.15'),
)
register_equation(fractional_water_reabsorption)

try:
    __all__ += ['fractional_water_reabsorption']
except NameError:
    __all__ = ['fractional_water_reabsorption']


# --- clinical additions (CICM, beyond Feher) ---

def compute_fe_urea(U_urea, P_cr, P_urea, U_cr):
    """FEurea = (U_urea*P_cr)/(P_urea*U_cr)*100 (%). <35% prerenal, >50% ATN; valid on diuretics unlike FENa."""
    return (U_urea * P_cr) / (P_urea * U_cr) * 100.0

fe_urea = create_equation(
    id='fe_urea',
    output_units='%',
    name='Fractional Excretion of Urea',
    category=EquationCategory.RENAL,
    latex='FE_{urea} = \\frac{U_{urea}P_{cr}}{P_{urea}U_{cr}}\\times100',
    simplified='FEurea = (U_urea*P_cr)/(P_urea*U_cr)*100',
    description='Fractional excretion of urea; distinguishes prerenal (<35%) from intrinsic (>50%) AKI and remains valid during diuretic therapy, unlike FENa.',
    compute_func=compute_fe_urea,
    parameters=[
        Parameter(name='U_urea', description='Urine urea', units='mmol/L', symbol='U_urea', physiological_range=(10, 600)),
        Parameter(name='P_cr', description='Plasma creatinine', units='mmol/L', symbol='P_Cr', physiological_range=(0.02, 1.5)),
        Parameter(name='P_urea', description='Plasma urea', units='mmol/L', symbol='P_urea', physiological_range=(2, 60)),
        Parameter(name='U_cr', description='Urine creatinine', units='mmol/L', symbol='U_Cr', physiological_range=(1, 40)),
    ],
    depends_on=[],
    produces='FE_urea',
    metadata=EquationMetadata(source_unit=0, source_chapter='clinical',
                              source_section="Clinical standard (CICM/ICU); beyond Feher's text", page_reference=None),
)
register_equation(fe_urea)

try:
    __all__ += ['fe_urea']
except NameError:
    __all__ = ['fe_urea']

"""receptor equations"""

"""
Fractional receptor occupancy.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""

from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation
)
from scripts.index import register_equation


def compute_fractional_occupancy(H: float, Kd: float) -> float:
    """
    Calculate fractional receptor occupancy.

    Parameters
    ----------
    H : float
        Free hormone concentration (M)
    Kd : float
        Dissociation constant (M)

    Returns
    -------
    float
        Fractional occupancy θ (0-1, dimensionless)

    Notes
    -----
    Many hormone systems achieve maximal response at <10% receptor occupancy
    due to spare receptors and signal amplification.
    EC50 (half-maximal effect) often < K_d.
    """
    return H / (Kd + H)


# Create equation
fractional_occupancy_equation = create_equation(
    id="receptor_fractional_occupancy",
    output_units='dimensionless',
    name="Receptor Fractional Occupancy",
    category=EquationCategory.ENDOCRINE,
    latex=r"\theta = \frac{[H]}{K_d + [H]}",
    simplified="θ = [H] / (K_d + [H])",
    description="Fraction of receptors occupied by hormone (0-1). "
                "Due to signal amplification, maximal response often occurs at <10% occupancy.",
    compute_func=compute_fractional_occupancy,
    parameters=[
        Parameter(
            name="H",
            description="Free hormone concentration",
            units="M",
            symbol="[H]",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="Kd",
            description="Dissociation constant",
            units="M",
            symbol="K_d",
            physiological_range=(1e-12, 1e-6)
        )
    ],
    depends_on=["hormone_kd"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.2"
    )
)

# Register globally
register_equation(fractional_occupancy_equation)

"""
Receptor saturation binding (Langmuir isotherm).

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_saturation_binding(H: float, Bmax: float, Kd: float) -> float:
    """
    Calculate bound hormone at equilibrium (saturation binding).

    Parameters
    ----------
    H : float
        Free hormone concentration (M)
    Bmax : float
        Maximum binding capacity (M)
    Kd : float
        Dissociation constant (M)

    Returns
    -------
    float
        Bound hormone concentration (M)

    Notes
    -----
    This is the Langmuir isotherm for receptor binding.
    At [H] = K_d, binding is 50% of maximum.
    """
    return Bmax * H / (Kd + H)


# Create equation
saturation_binding_equation = create_equation(
    id="receptor_saturation_binding",
    output_units='M',
    name="Receptor Saturation Binding",
    category=EquationCategory.ENDOCRINE,
    latex=r"B = \frac{B_{max} \times [H]}{K_d + [H]}",
    simplified="B = B_max × [H] / (K_d + [H])",
    description="Equilibrium receptor binding following Langmuir isotherm. "
                "B_max is maximum binding capacity, K_d is concentration at 50% saturation.",
    compute_func=compute_saturation_binding,
    parameters=[
        Parameter(
            name="H",
            description="Free hormone concentration",
            units="M",
            symbol="[H]",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="Bmax",
            description="Maximum binding capacity",
            units="M",
            symbol="B_{max}",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="Kd",
            description="Dissociation constant",
            units="M",
            symbol="K_d",
            physiological_range=(1e-12, 1e-6)
        )
    ],
    depends_on=["hormone_kd"],
    produces="B",
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.2"
    )
)

# Register globally
register_equation(saturation_binding_equation)

"""
Scatchard plot transformation for linearizing binding data.

Source: Quantitative Human Physiology 3rd Edition
Unit 9: Endocrine Physiology
"""


def compute_scatchard_y(B: float, H: float) -> float:
    """
    Calculate y-axis value for Scatchard plot (B/[H]).

    Parameters
    ----------
    B : float
        Bound hormone concentration (M)
    H : float
        Free hormone concentration (M)

    Returns
    -------
    float
        B/[H] ratio (dimensionless)

    Notes
    -----
    Scatchard equation: B/[H] = B_max/K_d - B/K_d
    Plot B/[H] vs B gives:
    - Slope = -1/K_d
    - x-intercept = B_max
    - y-intercept = B_max/K_d
    """
    return B / H


# Create equation
scatchard_equation = create_equation(
    id="scatchard_transform",
    output_units='dimensionless',
    name="Scatchard Plot Transformation",
    category=EquationCategory.ENDOCRINE,
    latex=r"\frac{B}{[H]} = \frac{B_{max}}{K_d} - \frac{B}{K_d}",
    simplified="B/[H] = B_max/K_d - B/K_d",
    description="Scatchard analysis linearizes binding data. Plot of B/[H] vs B yields "
                "slope = -1/K_d and x-intercept = B_max.",
    compute_func=compute_scatchard_y,
    parameters=[
        Parameter(
            name="B",
            description="Bound hormone concentration",
            units="M",
            symbol="B",
            physiological_range=(1e-12, 1e-6)
        ),
        Parameter(
            name="H",
            description="Free hormone concentration",
            units="M",
            symbol="[H]",
            physiological_range=(1e-12, 1e-6)
        )
    ],
    depends_on=["receptor_saturation_binding"],
    metadata=EquationMetadata(
        source_unit=9,
        source_chapter="9.2"
    )
)

# Register globally
register_equation(scatchard_equation)



# --- coverage pass additions (Feher extraction) ---

def compute_cheng_prusoff_ki(IC50, L, Kd):
    """Cheng-Prusoff relation: inhibitor dissociation constant K_i (M) from IC50 (M), free ligand [L] (M), and ligand dissociation constant K_d (M). Feher Unit 9, Appendix 9.1.A1 'Competitive Inhibition of Binding': K_i = IC50 / (1 + [L]/K_d). All concentrations in molar (M)."""
    return IC50 / (1.0 + L / Kd)

cheng_prusoff_ki = create_equation(
    id='cheng_prusoff_ki',
    output_units='M',
    name='Cheng-Prusoff Equation (Ki from IC50)',
    category=EquationCategory.ENDOCRINE,
    latex='K_i = \\dfrac{\\mathrm{IC}_{50}}{1 + \\dfrac{[L]}{K_d}}',
    simplified='K_i = IC_50 / (1 + [L]/K_d)',
    description="Cheng-Prusoff equation for competitive inhibition of binding. Converts a measured IC50 (the inhibitor concentration that displaces 50% of a ligand at a fixed free-ligand concentration [L]) into the true inhibitor dissociation constant K_i, correcting for the competing ligand concentration relative to the ligand's own K_d. Standard tool in radioimmunoassay and receptor pharmacology for obtaining an affinity (K_i) that is independent of the assay ligand concentration. Feher derives it under the appendix heading 'Competitive Inhibition of Binding' and states it enables determination of K_i from [L] and K_d.",
    compute_func=compute_cheng_prusoff_ki,
    parameters=[
        Parameter(name='IC50', description='Inhibitor concentration producing 50% inhibition (50% displacement) of ligand binding at the fixed free-ligand concentration used', units='M', symbol='IC_{50}', physiological_range=(1e-12, 0.001)),
        Parameter(name='L', description='Free (unbound) ligand concentration at which the competition experiment is run', units='M', symbol='[L]', physiological_range=(1e-12, 0.001)),
        Parameter(name='Kd', description='Dissociation constant of the ligand for the binding site (ligand binding alone)', units='M', symbol='K_d', physiological_range=(1e-12, 1e-06)),
    ],
    depends_on=['hormone_kd'],
    produces='K_i',
    metadata=EquationMetadata(source_unit=9, source_chapter='9.1',
                              source_section='Competitive Inhibition of Binding', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(cheng_prusoff_ki)


def compute_competitive_inhibition_binding(L, Bmax, Kd, I, Ki):
    """Bound ligand at equilibrium in the presence of a competitive inhibitor.

    Feher, Quantitative Human Physiology 3rd ed., Unit 9, Appendix 9.1.A1
    (Analysis of Ligand Binding), section 'COMPETITIVE INHIBITION OF BINDING'.
    A competitor I binds the same site, scaling the apparent dissociation
    constant by (1 + [I]/Ki):  B = Bmax*[L] / ([L] + Kd*(1 + [I]/Ki)).
    Equal to Bmax times the competitive saturation fraction; reduces to simple
    saturation binding when [I] = 0. All concentrations and Kd, Ki in M (SI mol/L).
    """
    return Bmax * L / (L + Kd * (1.0 + I / Ki))

competitive_inhibition_binding = create_equation(
    id='competitive_inhibition_binding',
    output_units='M',
    name='Competitive Inhibition of Binding',
    category=EquationCategory.ENDOCRINE,
    latex='B = \\dfrac{B_{max}\\,[L]}{[L] + K_d\\left(1 + \\dfrac{[I]}{K_i}\\right)}',
    simplified='B = B_max*[L] / ([L] + K_d*(1 + [I]/K_i))',
    description='Bound ligand at equilibrium when a competitive inhibitor occupies the same binding site as the ligand. The inhibitor raises the apparent dissociation constant by the factor (1 + [I]/K_i), so bound ligand equals B_max times the competitive saturation fraction. Reduces exactly to simple saturation binding (B = B_max[L]/(K_d+[L])) when [I] = 0. Used to analyze competitive antagonism, radioimmunoassay and other competitive-binding assays, and the IC50-K_i relationship in receptor pharmacology.',
    compute_func=compute_competitive_inhibition_binding,
    parameters=[
        Parameter(name='L', description='Free (unbound) ligand concentration', units='M', symbol='[L]', physiological_range=(1e-12, 0.001)),
        Parameter(name='Bmax', description='Maximum binding capacity (total site concentration)', units='M', symbol='B_{max}', physiological_range=(1e-12, 1e-06)),
        Parameter(name='Kd', description='Ligand dissociation constant (concentration at half-saturation without inhibitor)', units='M', symbol='K_d', physiological_range=(1e-12, 1e-06)),
        Parameter(name='I', description='Competitive inhibitor concentration', units='M', symbol='[I]', physiological_range=(0, 0.001)),
        Parameter(name='Ki', description='Inhibitor dissociation constant', units='M', symbol='K_i', physiological_range=(1e-12, 1e-06)),
    ],
    depends_on=["hormone_kd", "cheng_prusoff_ki"],
    metadata=EquationMetadata(source_unit=9, source_chapter='9.1',
                              source_section='COMPETITIVE INHIBITION OF BINDING (Appendix 9.1.A1 Analysis of Ligand Binding)', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(competitive_inhibition_binding)

try:
    __all__ += ['cheng_prusoff_ki', 'competitive_inhibition_binding']
except NameError:
    __all__ = ['cheng_prusoff_ki', 'competitive_inhibition_binding']

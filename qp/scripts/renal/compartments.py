"""Renal — body-composition / fluid-compartment marker equations.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher (Unit 7)
"""
import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation,
)
from scripts.index import register_equation


# --- coverage pass additions (Feher extraction) ---

def compute_lean_body_mass(tbw, water_fraction=0.73):
    """Lean body mass from total body water via Behnke's body-composition
    partition (Feher 7.1, 'The total body water varies with body composition').

    LBM = TBW / water_fraction, where water_fraction is the fractional water
    content of lean body mass (~0.73 in adults, ~0.81 in the neonate).

    Units: tbw is the mass of body water in kg (measured by D2O dilution;
    numerically ~= its volume in L since rho_water ~= 1 kg/L). LBM is returned
    in kg. water_fraction is dimensionless.
    """
    return tbw / water_fraction

lean_body_mass = create_equation(
    id='lean_body_mass',
    output_units='kg',
    name='Lean Body Mass (Behnke)',
    category=EquationCategory.RENAL,
    latex='\\mathrm{LBM} = \\dfrac{\\mathrm{TBW}}{0.73}',
    simplified='LBM = TBW / 0.73',
    description="Lean body mass estimated from total body water via Albert Behnke's body-composition partition. Behnke divided body weight into (1) lean body mass (LBM, including ~3% essential fat) and (2) excess fat. Because LBM is ~73% water by weight (hydration fraction 0.73 in adults; ~0.81 in the neonate), LBM = TBW/0.73, where TBW is measured by deuterium-oxide (D2O) dilution. Used in body-composition assessment and to derive excess body fat (excess body weight = body weight - LBM); obesity is commonly defined as body fat exceeding 20% of total body weight.",
    compute_func=compute_lean_body_mass,
    parameters=[
        Parameter(name='tbw', description='Total body water (mass of body water, measured by deuterium-oxide dilution; numerically approximately equal to its volume in L since rho_water ~= 1 kg/L)', units='kg', symbol='TBW', physiological_range=(1, 100)),
        Parameter(name='water_fraction', description='Fractional water content of lean body mass (Behnke); ~0.73 in adults, ~0.81 in the neonate', units='dimensionless', symbol='f_H2O', default_value=0.73, physiological_range=(0.7, 0.82)),
    ],
    depends_on=[],
    produces='LBM',
    metadata=EquationMetadata(source_unit=7, source_chapter='7.1',
                              source_section='THE TOTAL BODY WATER VARIES WITH BODY COMPOSITION', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(lean_body_mass)

__all__ = ['lean_body_mass']

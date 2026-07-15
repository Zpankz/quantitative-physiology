"""Nervous system — visual optics (refraction, lenses) equations.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher (Unit 4)
"""
import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation,
)
from scripts.index import register_equation


# --- coverage pass additions (Feher extraction) ---

def compute_snells_law(n_i, theta_i, n_r):
    """Snell's law of refraction (Feher Eqn. 4.9.A1.4): n_i*sin(theta_i) = n_r*sin(theta_r).

    Returns the angle of refraction theta_r in radians. n_i and n_r are the
    dimensionless refractive indices of the incident and refracting media,
    respectively, and theta_i is the angle of incidence in radians (measured
    from the normal to the interface). Feher, Quantitative Human Physiology 3rd
    ed., Unit 4, Appendix 4.9.A1.
    """
    import math
    return math.asin((n_i / n_r) * math.sin(theta_i))

snells_law = create_equation(
    id='snells_law',
    output_units='rad',
    name="Snell's Law of Refraction",
    category=EquationCategory.NERVOUS,
    latex='n_{\\mathrm{i}} \\sin\\theta_{\\mathrm{i}} = n_{\\mathrm{r}} \\sin\\theta_{\\mathrm{r}}',
    simplified='n_i * sin(theta_i) = n_r * sin(theta_r)',
    description="Snell's law of refraction relates the angle of incidence to the angle of refraction when light crosses the interface between two media of refractive indices n_i and n_r. It governs the bending of light at every ocular refracting surface (air/tears, cornea, aqueous humor, lens, vitreous body); solving for theta_r = arcsin((n_i/n_r) sin theta_i) gives the refraction angle. When the indices are equal (or theta_i = 0) there is no bending. Basis for lens focusing and refractive-error optics of the eye.",
    compute_func=compute_snells_law,
    parameters=[
        Parameter(name='n_i', description='Refractive index of the incident medium (dimensionless; e.g. air ~1.00, tears/cornea/aqueous humor ~1.33-1.38)', units='dimensionless', symbol='n_{\\mathrm{i}}', physiological_range=(1, 1.5)),
        Parameter(name='theta_i', description='Angle of incidence, measured from the line normal to the interface', units='rad', symbol='\\theta_{\\mathrm{i}}', physiological_range=(0, 1.5707963267948966)),
        Parameter(name='n_r', description='Refractive index of the refracting (second) medium (dimensionless; e.g. cornea ~1.376, lens ~1.36-1.41)', units='dimensionless', symbol='n_{\\mathrm{r}}', physiological_range=(1, 1.5)),
    ],
    depends_on=[],
    produces='theta_r',
    metadata=EquationMetadata(source_unit=4, source_chapter='4.9',
                              source_section='Appendix 4.9.A1 Refraction of Light and the Thin Lens Formula - The different speeds of light in two media cause refraction, the bending of light at their interface', page_reference=None,
                              textbook_equation_number='4.9.A1.4'),
)
register_equation(snells_law)


def compute_thin_lens_formula(O, I):
    """Thin lens formula 1/O + 1/I = 1/f. Returns focal length f (m) from object
    distance O (m) and image distance I (m); refractive power in diopters = 1/f.
    Feher 4.9 (vision optics), Appendix 4.9.A1, Eqn. 4.9.A1.12."""
    return 1.0 / (1.0 / O + 1.0 / I)

thin_lens_formula = create_equation(
    id='thin_lens_formula',
    output_units='m',
    name='Thin Lens Formula',
    category=EquationCategory.NERVOUS,
    latex='\\frac{1}{O} + \\frac{1}{I} = \\frac{1}{f}',
    simplified='1/O + 1/I = 1/f',
    description='Thin lens formula relating object distance O, image distance I, and focal length f of a thin lens (radii of curvature large compared to lens thickness). In physiological optics it links image formation to the refractive power of the eye (diopters = 1/f): given the object distance (near point) and the fixed image distance (~1.6 cm), it yields the focal length / refractive power. Used by Feher to compute the refractive power of the relaxed eye (62.5 D) and the maximally accommodated eye (72.5 D), the power of accommodation, and to analyze presbyopia, myopia, and hypermetropia. Compute function returns f (m); invert for diopters.',
    compute_func=compute_thin_lens_formula,
    parameters=[
        Parameter(name='O', description='Object distance from the lens nodal plane to the object (the near point for the accommodated eye; treated as infinite for far objects)', units='m', symbol='O', physiological_range=(0.01, 1000)),
        Parameter(name='I', description='Image distance from the lens nodal plane to the image (approximately 1.6 cm for the human eye)', units='m', symbol='I', physiological_range=(0.001, 1)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter='4.9',
                              source_section='THE THIN LENS FORMULA LINKS REFRACTIVE POWER AND IMAGE FORMATION (Appendix 4.9.A1)', page_reference=None,
                              textbook_equation_number='4.9.A1.12'),
)
register_equation(thin_lens_formula)


def compute_refractive_power_diopters(f):
    """Refractive (dioptric) power of a lens or optical system: D = 1/f.

    Feher 4.9 'Vision: Optics and Phototransduction', subsection 'The Focal
    Length Is a Measure of the Refractive Power of a Lens' (also stated under
    'The Eye Focuses Light on the Retina by Refraction'). f is the focal length
    in metres; returns the refractive power D in diopters (m^-1). A converging
    (convex) lens has positive f and positive D; a diverging (concave) lens has
    negative f and negative D.
    """
    return 1.0 / f

refractive_power_diopters = create_equation(
    id='refractive_power_diopters',
    output_units='1/m',
    name='Refractive Power (Diopters)',
    category=EquationCategory.NERVOUS,
    latex='\\mathrm{Diopters}\\;(D) = \\frac{1}{f}',
    simplified='D = 1 / f',
    description="Refractive power (dioptric power) of a lens or optical system, D = 1/f, with focal length f in metres and D in diopters (m^-1). In physiological optics the strength of a lens is expressed in diopters as the reciprocal of the focal length; the resting human eye has a refractive power of ~62.5 D (f ~ 0.016 m), of which ~44 D is the cornea and ~18.5 D the lens. Dioptric power is additive across thin lenses in contact and underpins the clinically important derived quantities: the power of accommodation (difference between the relaxed and maximally accommodated eye, ~10-12 D in the young), its age-related decline (presbyopia), and corrective-lens prescription (converging '+' lenses correct hypermetropia, diverging '-' lenses correct myopia). Converging lenses have positive f and D; diverging lenses have negative f and D.",
    compute_func=compute_refractive_power_diopters,
    parameters=[
        Parameter(name='f', description='Focal length of the lens or optical system (distance from the nodal/equatorial plane to the focal point / focused image). Positive for converging (convex) optics, negative for diverging (concave) optics.', units='m', symbol='f', physiological_range=(0.01, 1)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter='4.9',
                              source_section='The Focal Length Is a Measure of the Refractive Power of a Lens', page_reference=None,
                              textbook_equation_number=None),
)
register_equation(refractive_power_diopters)

__all__ = ['snells_law', 'thin_lens_formula', 'refractive_power_diopters']


# --- coverage pass 2 (residual reconsideration) ---

def compute_refractive_index(c, v):
    """Refractive index n = c/v (Feher 4.9, Eqn 4.9.A1.1): ratio of the speed of light in vacuum c (m/s) to its phase speed v in the medium (m/s). Dimensionless; n>=1 (water ~1.33, cornea ~1.38, lens ~1.40, glass ~1.5)."""
    return c / v

refractive_index = create_equation(
    id='refractive_index',
    output_units='dimensionless',
    name='Refractive Index',
    category=EquationCategory.NERVOUS,
    latex='n = \\frac{c}{v}',
    simplified='n = c / v',
    description="Refractive index of a medium: the ratio of the speed of light in vacuum to its speed in the medium. It quantifies how much light slows and bends entering the medium, and is the input quantity to Snell's law and to refractive (lens) power in the optics of the eye. Feher section 4.9, Appendix, Eqn 4.9.A1.1.",
    compute_func=compute_refractive_index,
    parameters=[
        Parameter(name='c', description='Speed of light in vacuum', units='m/s', symbol='c', default_value=299800000.0),
        Parameter(name='v', description='Phase speed of light in the medium', units='m/s', symbol='v', physiological_range=(100000000.0, 300000000.0)),
    ],
    depends_on=[],
    produces='n',
    metadata=EquationMetadata(source_unit=4, source_chapter='4.9',
                              source_section="Appendix 4.9.A1 (Snell's law / refractive index)", page_reference=None,
                              textbook_equation_number='4.9.A1.1'),
)
register_equation(refractive_index)

try:
    __all__ += ['refractive_index']
except NameError:
    __all__ = ['refractive_index']

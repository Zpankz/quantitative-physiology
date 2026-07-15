"""Nervous system — auditory (acoustic intensity) equations.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher (Unit 4)
"""
import numpy as np
from scripts.base import (
    AtomicEquation, Parameter, EquationMetadata,
    EquationCategory, create_equation,
)
from scripts.index import register_equation


# --- coverage pass additions (Feher extraction) ---

def compute_sound_intensity_level_db(I_sound, I_ref=1e-12, factor=10.0):
    """Sound intensity level (loudness) in decibels. L_dB = factor * log10(I_sound / I_ref).
    Feher Quantitative Human Physiology 3rd ed., Sec 4.7 Hearing, Eqn 4.7.1 (intensity
    form, factor=10). The equivalent pressure form Eqn 4.7.2 uses factor=20 with a
    pressure-amplitude ratio (dP_sound/dP_ref) because intensity is proportional to the
    square of pressure amplitude. I_ref default 1e-12 W/m^2 = 0 dB SPL reference.
    Units: I_sound and I_ref in W m^-2 for the intensity form."""
    import math
    return factor * math.log10(I_sound / I_ref)

sound_intensity_level_db = create_equation(
    id='sound_intensity_level_db',
    output_units='dimensionless',
    name='Sound Intensity Level (Decibel)',
    category=EquationCategory.NERVOUS,
    latex='L_{\\mathrm{dB}} = 10 \\, \\log_{10}\\!\\left(\\frac{I_{\\mathrm{sound}}}{I_{\\mathrm{ref}}}\\right)',
    simplified='L_dB = 10 * log10(I_sound / I_ref)',
    description="Sound intensity level (loudness) expressed in decibels: a base-10 logarithmic transform of the ratio of sound intensity to a reference intensity (1e-12 W/m^2 = 0 dB SPL). Feher Eqn 4.7.1. The equivalent pressure form (Eqn 4.7.2) multiplies the pressure-amplitude ratio by 20 because sound intensity is proportional to the square of pressure amplitude; pass factor=20 with a pressure ratio to use that form. Used to compress the wide dynamic range of audible sound and to convert between decibels, intensity, and pressure in audiometry/acoustics. Distinct from Fechner's law: this is a defined physical unit of sound level with a fixed definitional constant, not an empirical perceived-magnitude model with a free constant.",
    compute_func=compute_sound_intensity_level_db,
    parameters=[
        Parameter(name='I_sound', description='Sound intensity (energy per second per unit area). For the pressure form (factor=20) pass the sound pressure-amplitude increment instead.', units='W m^-2', symbol='I_{sound}', physiological_range=(1e-13, 100)),
        Parameter(name='I_ref', description='Reference intensity. Standard sound-pressure-level reference is 1e-12 W/m^2 (= 1e-16 W/cm^2), which corresponds to 0 dB SPL.', units='W m^-2', symbol='I_{ref}', default_value=1e-12, physiological_range=(1e-16, 1e-09)),
        Parameter(name='factor', description='Definitional logarithmic multiplier: 10 for an intensity ratio (Eqn 4.7.1), 20 for a pressure-amplitude ratio (Eqn 4.7.2). Fixed by the decibel definition, not a fitted constant.', units='dimensionless', symbol='n', default_value=10, physiological_range=(10, 20)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter='4.7',
                              source_section='THE HUMAN AUDITORY SYSTEM DISCRIMINATES AMONG TONE, TIMBRE, AND INTENSITY', page_reference=None,
                              textbook_equation_number='4.7.1'),
)
register_equation(sound_intensity_level_db)


def compute_acoustic_intensity(dP0, rho=1.21, c=343.0):
    """Sound intensity I = dP0**2 / (2*rho*c), in W/m^2 (Feher Eqn 4.7.A1.32).

    Intensity of a sound wave is proportional to the square of the pressure
    amplitude, divided by twice the characteristic acoustic impedance (rho*c)
    of the medium. Independent of frequency.

    dP0 : pressure amplitude of the sound wave (Pa)
    rho : density of the propagating medium, default air 1.21 (kg/m^3)
    c   : speed of sound in the medium, default air 343 (m/s)
    returns: intensity in W/m^2
    """
    return dP0 ** 2 / (2.0 * rho * c)

acoustic_intensity = create_equation(
    id='acoustic_intensity',
    output_units='W/m^2',
    name='Acoustic Intensity (Sound Intensity)',
    category=EquationCategory.NERVOUS,
    latex='I = \\frac{\\Delta P_0^{2}}{2 \\rho c}',
    simplified='I = dP0^2 / (2 * rho * c)',
    description='Acoustic (sound) intensity: power carried per unit area by a sound wave, equal to the square of the pressure amplitude divided by twice the characteristic acoustic impedance rho*c of the medium. Intensity is independent of frequency. This is the physical basis of the decibel scale in hearing: because I is proportional to pressure squared, the dB SPL scale (20*log10 of the pressure ratio) equals the intensity-based scale (10*log10 of the intensity ratio), explaining the 10-vs-20 factor. rho*c (the acoustic impedance) is also the quantity the middle ear impedance-matches from air to cochlear fluid.',
    compute_func=compute_acoustic_intensity,
    parameters=[
        Parameter(name='dP0', description='Pressure amplitude of the sound wave (excess pressure over ambient)', units='Pa', symbol='\\Delta P_0', physiological_range=(0, 200)),
        Parameter(name='rho', description='Density of the propagating medium (air by default)', units='kg/m^3', symbol='\\rho', default_value=1.21, physiological_range=(1, 1.3)),
        Parameter(name='c', description='Speed of sound in the medium (air by default); rho*c is the characteristic acoustic impedance', units='m/s', symbol='c', default_value=343, physiological_range=(330, 360)),
    ],
    depends_on=[],
    metadata=EquationMetadata(source_unit=4, source_chapter='4.7',
                              source_section='The Intensity of Sound Is Proportional to the Square of the Pressure', page_reference=None,
                              textbook_equation_number='4.7.A1.32'),
)
register_equation(acoustic_intensity)

__all__ = ['sound_intensity_level_db', 'acoustic_intensity']

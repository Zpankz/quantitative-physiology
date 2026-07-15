"""
Thermoregulation — definitional heat-balance core (DRAFT / roadmap Feature 5).

This module holds ONLY the genuinely-canonical, definitional relations of body
heat balance: the first-law partitional-calorimetry identity and the textbook
heat-transfer laws (Newton cooling, Fourier conduction, Stefan-Boltzmann
radiation, latent-heat evaporation). Every empirical body-specific coefficient
(Du Bois BSA coefficient, skin emissivity, convective/conductive coefficients,
tissue heat capacity, latent heat of vaporisation) is deliberately LEFT
UNCOMMITTED — those Parameters carry no default_value and are enumerated in the
draft report's `needs_source`. The single committed physical constant is the
Stefan-Boltzmann constant σ. σ is exact BY DEFINITION in the post-2019 SI —
σ = 2π^5 k_B^4 / (15 h^3 c^2) with k_B, h and c now exact — but the stored decimal
5.670374419e-8 is the CODATA/NIST recommended value carried only to float64
precision (the exact decimal expansion is non-terminating). It is given as a
Parameter default on that basis.

Duplicate check: a scan of the canonical index confirms no thermal Fourier
(kAΔT/d) conduction equation exists in the library — the existing `fick_first_law`
is a per-area diffusive MASS flux (mol·m^-2·s^-1), a different physical quantity —
so the conductive term below is genuinely new, not a rename of an existing id.

This is a read-and-propose DRAFT. It is intentionally NON-INVASIVE: it does not
call register_equation and does not touch CANONICAL_EQUATIONS or the global
index, so it stays out of the whole-index acceptance gate's counts until the
council decides to integrate it. Import is side-effect-free beyond building the
module-level AtomicEquation objects.

Scope note: the wider thermoregulation coverage gap also includes non-heat
topics (immunity, obstetric physiology, haemostasis). Those are explicitly OUT
OF SCOPE here; this module is the heat-balance core only.

Source framing: Feher, Quantitative Human Physiology 3rd ed. — energy
conservation / first law (Unit 1, Physical & Chemical Foundations) applied to the
body, plus the standard heat-transfer laws used in thermoregulation. Provenance is
recorded at UNIT granularity only (source_chapter='1'): the specific subsection was
not re-read against the corpus this session, so no narrower section number is
asserted, and page_reference=None per the accuracy practices (no guessed pages).

Terminology note: Newton cooling, Fourier conduction and Stefan-Boltzmann
radiation are strictly CONSTITUTIVE laws (empirical/idealised relations with a
material coefficient), not pure definitions. They are treated here as
"definitional forms" in the narrow sense that the equation SHAPE is committed while
every body/material-specific coefficient (h, k, ε, λ) is left UNCOMMITTED — it is
those coefficients, not the law shape, that would need an external source.
"""

from scripts.base import (
    create_equation,
    EquationCategory,
    Parameter,
    EquationMetadata,
)

# Stefan-Boltzmann constant (W·m^-2·K^-4). Exact BY DEFINITION post-2019 SI:
# σ = (2 π^5 k_B^4) / (15 h^3 c^2), with k_B, h, c now exact. The literal below is
# the CODATA/NIST value to float64 precision (the exact decimal is non-terminating).
STEFAN_BOLTZMANN = 5.670374419e-8


# =============================================================================
# 1. Heat storage — first law for the body (partitional calorimetry)
# =============================================================================

def compute_heat_storage(M, W, R=0.0, C=0.0, K=0.0, E=0.0):
    """Rate of body heat storage by the first law (partitional-calorimetry form):

        S = M - W - R - C - K - E

    where every term is a rate (e.g. W, or W·m^-2 if area-normalised) in
    consistent units:
      M = metabolic heat production
      W = external mechanical work done BY the body (leaves as work, not heat)
      R = net RADIATIVE heat exchange   (loss positive, gain negative)
      C = net CONVECTIVE heat exchange  (loss positive, gain negative)
      K = net CONDUCTIVE heat exchange  (loss positive, gain negative)
      E = net EVAPORATIVE heat loss     (loss positive)

    Sign convention: R, C, K, E are written as NET LOSSES (positive when heat
    leaves the body); a negative value therefore encodes a net gain from a hot
    environment. This resolves the textbook "S = M - W ± R ± C ± K - E" into a
    single signed identity. S > 0 => body is storing heat (temperature rising);
    S < 0 => body is losing stored heat. This is a definitional identity, not a
    fitted model: it commits no coefficient."""
    return M - W - R - C - K - E


heat_storage = create_equation(
    id='heat_storage',
    output_units='W',
    name='Body Heat Storage (Heat Balance Equation)',
    category=EquationCategory.FOUNDATIONS,
    latex='S = M - W \\pm R \\pm C \\pm K - E',
    simplified='S = M - W - R - C - K - E',
    description=(
        'Body heat-balance equation: the first law of thermodynamics applied to '
        'the whole body as a partitional-calorimetry identity. The rate of heat '
        'storage S equals metabolic heat production M minus external work W minus '
        'the net radiative (R), convective (C), conductive (K) and evaporative (E) '
        'heat losses. Losses are signed positive when heat leaves the body, so a '
        'negative R/C/K encodes environmental heat gain, collapsing the textbook '
        '"± R ± C ± K" into one identity. Positive S means heat is being stored '
        '(core temperature rising); zero S is thermal steady state. This is the '
        'definitional backbone of thermoregulation and partitional calorimetry; '
        'it commits no empirical coefficient. Distinct from body_energy_balance '
        '(nutritional metabolizable-energy bookkeeping over food/feces/urine): '
        'this is the THERMAL power balance over heat-transfer channels.'
    ),
    compute_func=compute_heat_storage,
    parameters=[
        Parameter(name='M', description='Metabolic heat production rate', units='W', symbol='M'),
        Parameter(name='W', description='External mechanical work rate done by the body', units='W', symbol='W'),
        Parameter(name='R', description='Net radiative heat loss (positive = loss, negative = gain)', units='W', symbol='R', default_value=0.0),
        Parameter(name='C', description='Net convective heat loss (positive = loss, negative = gain)', units='W', symbol='C', default_value=0.0),
        Parameter(name='K', description='Net conductive heat loss (positive = loss, negative = gain)', units='W', symbol='K', default_value=0.0),
        Parameter(name='E', description='Net evaporative heat loss (positive = loss)', units='W', symbol='E', default_value=0.0),
    ],
    depends_on=[],
    produces='S',
    metadata=EquationMetadata(source_unit=1, source_chapter='1',
                              source_section='Energy conservation (first law) applied to the body — heat balance',
                              page_reference=None, textbook_equation_number=None),
)


# =============================================================================
# 2. Convective heat loss — Newton's law of cooling (definitional)
# =============================================================================

def compute_convective_heat_loss(h, A, dT):
    """Convective heat transfer rate (Newton's law of cooling):

        Q = h * A * dT

    h = convective heat-transfer coefficient (W·m^-2·K^-1, UNCOMMITTED — depends
    on air/water velocity and geometry), A = surface area (m^2), dT = surface -
    ambient temperature difference (K), ORIENTED as dT = T_surface - T_ambient so a
    positive dT (warm body) gives a positive Q = a heat LOSS, matching the name.
    Constitutive law (coefficient uncommitted): linear in the driving temperature
    difference, zero flux when dT = 0."""
    return h * A * dT


convective_heat_loss = create_equation(
    id='convective_heat_loss',
    output_units='W',
    name='Convective Heat Loss (Newton Cooling)',
    category=EquationCategory.FOUNDATIONS,
    latex='Q = h A \\Delta T',
    simplified='Q = h*A*dT',
    description=(
        'Newton\'s law of cooling: the rate of convective heat exchange between '
        'the body surface and the surrounding fluid is proportional to the '
        'surface area A and the surface-to-ambient temperature difference dT '
        '(oriented dT = T_surface - T_ambient, so positive dT gives positive '
        'Q = a heat loss, consistent with the name), with proportionality the '
        'convective heat-transfer coefficient h. Constitutive law with the '
        'coefficient left uncommitted (linear, zero at dT=0). The coefficient h '
        'is condition- and geometry-specific and carries no default. Supplies the '
        'convective channel C of the heat_storage balance.'
    ),
    compute_func=compute_convective_heat_loss,
    parameters=[
        Parameter(name='h', description='Convective heat-transfer coefficient (uncommitted; velocity/geometry dependent)', units='W/(m^2*K)', symbol='h'),
        Parameter(name='A', description='Surface area available for convection', units='m^2', symbol='A'),
        Parameter(name='dT', description='Surface-to-ambient temperature difference (T_surface - T_ambient)', units='K', symbol='\\Delta T'),
    ],
    depends_on=[],
    produces='Q_conv',
    metadata=EquationMetadata(source_unit=1, source_chapter='1',
                              source_section='Heat transfer — convection (Newton cooling)',
                              page_reference=None, textbook_equation_number=None),
)


# =============================================================================
# 3. Conductive heat loss — Fourier's law (heat FLOW in W, not per-area flux)
# =============================================================================

def compute_conductive_heat_loss(k, A, dT, d):
    """Steady one-dimensional conductive heat flow (Fourier's law):

        Q = k * A * dT / d

    k = thermal conductivity (W·m^-1·K^-1, UNCOMMITTED — tissue-specific),
    A = cross-sectional area (m^2), dT = temperature difference across the layer
    (K, oriented hot-face minus cold-face so Q > 0 is a loss down the gradient),
    d = layer thickness (m). NOTE: this returns total heat FLOW/transfer RATE in
    watts (kAΔT/d), NOT the per-area heat flux (kΔT/d, W·m^-2) — hence the name
    '..._loss', parallel to the other channels, rather than '..._flux'.
    Constitutive law with the coefficient uncommitted; the heat flow is
    proportional to the gradient dT/d and is the exact thermal analogue of Fick's
    first law of diffusion (which the library carries only as a per-area MASS
    flux, mol·m^-2·s^-1, so no thermal duplicate exists)."""
    return k * A * dT / d


conductive_heat_loss = create_equation(
    id='conductive_heat_loss',
    output_units='W',
    name='Conductive Heat Loss (Fourier Law)',
    category=EquationCategory.FOUNDATIONS,
    latex='Q = \\frac{k A \\Delta T}{d}',
    simplified='Q = k*A*dT/d',
    description=(
        'Fourier\'s law of heat conduction (steady, one-dimensional): the '
        'conductive heat FLOW through a layer equals the thermal conductivity k '
        'times area A times the temperature difference dT divided by layer '
        'thickness d, i.e. proportional to the temperature gradient dT/d. This '
        'quantity is a heat-transfer RATE in watts (kAΔT/d), NOT the per-area heat '
        'flux (kΔT/d, W·m^-2) — named "_loss" to match its siblings and to avoid '
        'the "flux" misnomer. Structurally the thermal analogue of Fick\'s first '
        'law; the library\'s fick_first_law is a per-area MASS flux, so this is a '
        'distinct equation, not a duplicate. dT is oriented hot-face minus '
        'cold-face so Q > 0 is a loss down the gradient. The thermal conductivity '
        'k is tissue-specific and left uncommitted (no default). Supplies the '
        'conductive channel K of the heat_storage balance.'
    ),
    compute_func=compute_conductive_heat_loss,
    parameters=[
        Parameter(name='k', description='Thermal conductivity (uncommitted; tissue-specific)', units='W/(m*K)', symbol='k'),
        Parameter(name='A', description='Cross-sectional area for conduction', units='m^2', symbol='A'),
        Parameter(name='dT', description='Temperature difference across the layer (hot-face - cold-face)', units='K', symbol='\\Delta T'),
        Parameter(name='d', description='Layer thickness (conduction path length)', units='m', symbol='d'),
    ],
    depends_on=[],
    produces='Q_cond',
    metadata=EquationMetadata(source_unit=1, source_chapter='1',
                              source_section='Heat transfer — conduction (Fourier law)',
                              page_reference=None, textbook_equation_number=None),
)


# =============================================================================
# 4. Radiative heat loss — Stefan-Boltzmann law (σ exact; ε uncommitted)
# =============================================================================

def compute_radiative_heat_loss(T_body, T_surr, A, epsilon, sigma=STEFAN_BOLTZMANN):
    """Net radiative heat exchange (Stefan-Boltzmann law):

        Q = epsilon * sigma * A * (T_body**4 - T_surr**4)

    T_body, T_surr = ABSOLUTE (thermodynamic) temperatures in KELVIN of the body
    surface and the surroundings — the fourth powers are only physical in K; a
    Celsius value here is invalid (no internal C->K conversion is done, by design,
    so a wrong-unit input is not silently masked). A = radiating area (m^2),
    epsilon = surface emissivity (dimensionless, UNCOMMITTED — skin ~0.97 is
    empirical), sigma = Stefan-Boltzmann constant, exact by definition post-2019 SI
    (stored 5.670374419e-8 W·m^-2·K^-4 to float64 precision). The T^4 difference is
    the physical law, not a fit; Q = 0 when T_body = T_surr. This is the idealised
    gray-body form (uniform emissivity, effective area A, view factor absorbed into
    epsilon*A / assumed unity); it is not a full enclosure-radiation solution.
    Supplies the radiative channel R of the heat_storage balance."""
    return epsilon * sigma * A * (T_body ** 4 - T_surr ** 4)


radiative_heat_loss = create_equation(
    id='radiative_heat_loss',
    output_units='W',
    name='Radiative Heat Loss (Stefan-Boltzmann)',
    category=EquationCategory.FOUNDATIONS,
    latex='Q = \\epsilon \\sigma A (T_{body}^4 - T_{surr}^4)',
    simplified='Q = epsilon*sigma*A*(T_body**4 - T_surr**4)',
    description=(
        'Stefan-Boltzmann radiative exchange: net radiative heat loss is the '
        'emissivity epsilon times the Stefan-Boltzmann constant sigma times '
        'radiating area A times the difference of the fourth powers of the '
        'absolute body-surface and surrounding temperatures (which MUST be in '
        'kelvin — Celsius makes the T^4 terms physically invalid, and no internal '
        'conversion is performed). The T^4 law is exact physics and sigma is exact '
        'by definition post-2019 SI, stored to float64 precision (committed as a '
        'default). Emissivity epsilon is a surface property left uncommitted (no '
        'default; skin emissivity is empirical). This is the idealised gray-body '
        'form (view factor absorbed into epsilon*A / assumed unity), not a full '
        'enclosure solution. Supplies the radiative channel R of the heat_storage '
        'balance.'
    ),
    compute_func=compute_radiative_heat_loss,
    parameters=[
        Parameter(name='T_body', description='Absolute body-surface temperature', units='K', symbol='T_{body}'),
        Parameter(name='T_surr', description='Absolute temperature of the surroundings', units='K', symbol='T_{surr}'),
        Parameter(name='A', description='Radiating surface area', units='m^2', symbol='A'),
        Parameter(name='epsilon', description='Surface emissivity (uncommitted; skin ~0.97 is empirical)', units='dimensionless', symbol='\\epsilon'),
        Parameter(name='sigma', description='Stefan-Boltzmann constant (exact by definition post-2019 SI; stored to float64 precision)', units='W/(m^2*K^4)', symbol='\\sigma', default_value=STEFAN_BOLTZMANN),
    ],
    depends_on=[],
    produces='Q_rad',
    metadata=EquationMetadata(source_unit=1, source_chapter='1',
                              source_section='Heat transfer — radiation (Stefan-Boltzmann law)',
                              page_reference=None, textbook_equation_number=None),
)


# =============================================================================
# 5. Evaporative heat loss — latent heat (definitional; λ uncommitted)
# =============================================================================

def compute_evaporative_heat_loss(m_dot, lam):
    """Evaporative heat loss from latent heat of vaporisation:

        Q = m_dot * lam

    m_dot = mass rate of water evaporated in SI kg·s^-1 (NOT g/hr or mL/hr — a
    sweat rate in other units must be converted first, or Q is wrong by the
    conversion factor), lam = specific latent heat of vaporisation (J·kg^-1,
    UNCOMMITTED — ~2.43e6 J/kg for sweat at skin temperature is an empirical
    physical property, left to the caller). Q=0 when nothing evaporates.
    Definitional (energy = mass * specific latent heat); supplies the evaporative
    channel E of the heat_storage balance."""
    return m_dot * lam


evaporative_heat_loss = create_equation(
    id='evaporative_heat_loss',
    output_units='W',
    name='Evaporative Heat Loss (Latent Heat)',
    category=EquationCategory.FOUNDATIONS,
    latex='Q = \\dot{m} \\lambda',
    simplified='Q = m_dot*lam',
    description=(
        'Evaporative heat loss: the power removed by evaporating water is the '
        'mass evaporation rate (in SI kg/s) times the specific latent heat of '
        'vaporisation. Definitional (energy = mass * specific latent heat). The '
        'latent heat lam is a physical property left uncommitted (no default); the '
        'empirical value for sweat at skin temperature belongs in an external '
        'source. Supplies the evaporative channel E of the heat_storage balance.'
    ),
    compute_func=compute_evaporative_heat_loss,
    parameters=[
        Parameter(name='m_dot', description='Mass rate of water evaporated (SI kg/s; convert g/hr etc. first)', units='kg/s', symbol='\\dot{m}'),
        Parameter(name='lam', description='Specific latent heat of vaporisation (uncommitted; empirical property)', units='J/kg', symbol='\\lambda'),
    ],
    depends_on=[],
    produces='Q_evap',
    metadata=EquationMetadata(source_unit=1, source_chapter='1',
                              source_section='Heat transfer — evaporation (latent heat)',
                              page_reference=None, textbook_equation_number=None),
)


# Module-level draft registry (NOT the global canonical index — see module docstring).
THERMO_EQUATIONS = [
    heat_storage,
    convective_heat_loss,
    conductive_heat_loss,
    radiative_heat_loss,
    evaporative_heat_loss,
]

__all__ = [
    'heat_storage',
    'convective_heat_loss',
    'conductive_heat_loss',
    'radiative_heat_loss',
    'evaporative_heat_loss',
    'THERMO_EQUATIONS',
    'STEFAN_BOLTZMANN',
]

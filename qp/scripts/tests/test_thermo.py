"""Gate for the thermoregulation definitional heat-balance core (scripts.thermo).

Every assertion anchors to a HAND-COMPUTED numeric literal or an exact/definitional
identity — never to a re-typed copy of the module's formula (which would be
circular and mutation-blind). A wrong or perturbed relation in scripts.thermo must
make one of these fail. This test does NOT touch CANONICAL_EQUATIONS or the global
index — the draft is intentionally out of the whole-index gate.

Run: python -m scripts.tests.test_thermo
"""
import math

from scripts.extensions import thermo as T
from scripts.base import AtomicEquation


# ---------------------------------------------------------------------------
# 1. Heat storage: S = M - W - R - C - K - E
# ---------------------------------------------------------------------------

def test_heat_storage_literal():
    # Hand-computed: 100 - 10 - 20 - 30 - 5 - 40 = -5.0
    assert T.heat_storage.compute(M=100, W=10, R=20, C=30, K=5, E=40) == -5.0
    # Distinct term magnitudes => any single dropped/flipped-sign term changes S.
    # Metabolic-only (all losses default to 0): S = M - W.
    assert T.heat_storage.compute(M=100, W=0) == 100.0
    assert T.heat_storage.compute(M=80, W=30) == 50.0


def test_heat_storage_sign_direction():
    # Each loss term must SUBTRACT: raising E by 10 lowers S by exactly 10.
    base = T.heat_storage.compute(M=100, W=10, R=20, C=30, K=5, E=40)
    assert T.heat_storage.compute(M=100, W=10, R=20, C=30, K=5, E=50) == base - 10
    # Work must SUBTRACT: raising W by 15 lowers S by 15.
    assert T.heat_storage.compute(M=100, W=25, R=20, C=30, K=5, E=40) == base - 15
    # A negative loss encodes environmental GAIN and raises S.
    assert T.heat_storage.compute(M=100, W=10, R=-20, C=30, K=5, E=40) == base + 40


def test_heat_storage_conservation_closure():
    # First-law rearrangement: M - W == S + (R + C + K + E).
    M, W, R, C, K, E = 120.0, 15.0, 22.0, 33.0, 7.0, 41.0
    S = T.heat_storage.compute(M=M, W=W, R=R, C=C, K=K, E=E)
    assert math.isclose(M - W, S + (R + C + K + E), rel_tol=0, abs_tol=1e-12)
    # Thermal steady state: losses exactly balance net metabolic heat => S == 0.
    assert T.heat_storage.compute(M=50, W=0, R=20, C=20, K=10, E=0) == 0.0


# ---------------------------------------------------------------------------
# 2. Convective heat loss: Q = h*A*dT (Newton cooling)
# ---------------------------------------------------------------------------

def test_convective_literal_and_linearity():
    # Hand-computed: 8 * 1.8 * 5 = 72.0
    assert T.convective_heat_loss.compute(h=8, A=1.8, dT=5) == 72.0
    # No gradient => no flux (definitional).
    assert T.convective_heat_loss.compute(h=8, A=1.8, dT=0) == 0.0
    # Linear in dT: doubling dT doubles Q (guards against h*A/dT or h+A forms).
    assert T.convective_heat_loss.compute(h=8, A=1.8, dT=10) == 144.0


# ---------------------------------------------------------------------------
# 3. Conductive heat loss: Q = k*A*dT/d (Fourier, heat FLOW in W not W/m^2)
# ---------------------------------------------------------------------------

def test_conductive_literal_and_thickness():
    # Hand-computed: 0.5 * 1.8 * 5 / 0.02 = 225.0
    assert T.conductive_heat_loss.compute(k=0.5, A=1.8, dT=5, d=0.02) == 225.0
    # Inverse in thickness: doubling d halves Q (guards against multiply-by-d).
    assert T.conductive_heat_loss.compute(k=0.5, A=1.8, dT=5, d=0.04) == 112.5
    # No gradient => no flux.
    assert T.conductive_heat_loss.compute(k=0.5, A=1.8, dT=0, d=0.02) == 0.0


# ---------------------------------------------------------------------------
# 4. Radiative heat loss: Q = eps*sigma*A*(T_body^4 - T_surr^4) (Stefan-Boltzmann)
# ---------------------------------------------------------------------------

def test_radiative_sigma_is_exact_constant():
    # The one committed constant must be the EXACT SI-2019 Stefan-Boltzmann value.
    assert T.STEFAN_BOLTZMANN == 5.670374419e-8
    sigma_param = next(p for p in T.radiative_heat_loss.parameters if p.name == 'sigma')
    assert sigma_param.default_value == 5.670374419e-8


def test_radiative_fourth_power_law():
    # Equal temperatures => zero net exchange (definitional).
    assert T.radiative_heat_loss.compute(T_body=305, T_surr=305, A=1.0, epsilon=1.0) == 0.0
    # Fourth-power scaling, independent of sigma (it cancels): with T_surr=0,
    # Q(2T)/Q(T) must equal 2**4 = 16. This pins the exponent exactly and is
    # mutation-sensitive to any wrong power (T, T**2, T**3).
    q1 = T.radiative_heat_loss.compute(T_body=100, T_surr=0, A=1.0, epsilon=1.0)
    q2 = T.radiative_heat_loss.compute(T_body=200, T_surr=0, A=1.0, epsilon=1.0)
    assert math.isclose(q2 / q1, 16.0, rel_tol=1e-12)


def test_radiative_uses_committed_sigma():
    # With eps=1, A=1, T_surr=0: Q == sigma * T_body**4 using the EXACT default.
    q = T.radiative_heat_loss.compute(T_body=310, T_surr=0, A=1.0, epsilon=1.0)
    assert math.isclose(q, 5.670374419e-8 * (310 ** 4), rel_tol=1e-12)


def test_radiative_physiological_range_kelvin():
    # Realistic clinical case in KELVIN (skin 35C=308.15K, room 20C=293.15K),
    # eps=0.97, A=1.8 m^2. Anchored to the SI T^4 difference computed by hand from
    # the exact sigma default, NOT a re-typed copy of the module expression. This
    # exercises a physiological T_surr != 0 (addressing the "T_surr=0 is abstract"
    # concern) while keeping the anchor the committed exact constant.
    T_body, T_surr, A, eps = 308.15, 293.15, 1.8, 0.97
    expected = 0.97 * 5.670374419e-8 * 1.8 * (308.15 ** 4 - 293.15 ** 4)
    q = T.radiative_heat_loss.compute(T_body=T_body, T_surr=T_surr, A=A, epsilon=eps)
    assert math.isclose(q, expected, rel_tol=1e-12)
    # ~ +150 W net radiative loss from a warm body to a cooler room (physiological
    # order of magnitude); positive => net LOSS, consistent with the name.
    assert 100.0 < q < 200.0
    # Feeding Celsius where Kelvin is required is NOT silently corrected: the same
    # numbers read as Celsius (35, 20) give a wildly different, tiny result,
    # proving no internal C->K conversion masks a unit error.
    q_wrong_units = T.radiative_heat_loss.compute(T_body=35, T_surr=20, A=A, epsilon=eps)
    assert q_wrong_units < 1.0  # nonsensically small -> caller must pass kelvin


# ---------------------------------------------------------------------------
# 5. Evaporative heat loss: Q = m_dot*lam (latent heat)
# ---------------------------------------------------------------------------

def test_evaporative_literal_and_product():
    # lam supplied by caller (NOT a committed module constant): 2e-5 * 2.4e6 = 48.0
    assert math.isclose(T.evaporative_heat_loss.compute(m_dot=2e-5, lam=2.4e6), 48.0, rel_tol=1e-12)
    # Nothing evaporates => no loss.
    assert T.evaporative_heat_loss.compute(m_dot=0.0, lam=2.4e6) == 0.0
    # Bilinear product (guards against sum/quotient forms).
    assert T.evaporative_heat_loss.compute(m_dot=1.0, lam=2.0e6) == 2000000.0


# ---------------------------------------------------------------------------
# Structural: uncommitted empirical coefficients carry NO default_value.
# ---------------------------------------------------------------------------

def test_empirical_coefficients_uncommitted():
    """The guardrail encoded in code: h, k, epsilon, lam must have no default
    (they need an external source); only the exact sigma is committed."""
    def default_of(eq, pname):
        return next(p for p in eq.parameters if p.name == pname).default_value

    assert default_of(T.convective_heat_loss, 'h') is None
    assert default_of(T.conductive_heat_loss, 'k') is None
    assert default_of(T.radiative_heat_loss, 'epsilon') is None
    assert default_of(T.evaporative_heat_loss, 'lam') is None
    # The one committed constant is exact sigma.
    assert default_of(T.radiative_heat_loss, 'sigma') == 5.670374419e-8


def test_all_are_atomic_equations_with_output_units():
    assert len(T.THERMO_EQUATIONS) == 5
    ids = {e.id for e in T.THERMO_EQUATIONS}
    assert ids == {
        'heat_storage', 'convective_heat_loss', 'conductive_heat_loss',
        'radiative_heat_loss', 'evaporative_heat_loss',
    }
    for e in T.THERMO_EQUATIONS:
        assert isinstance(e, AtomicEquation)
        assert e.output_units == 'W'
        assert e.metadata is not None
        assert e.metadata.page_reference is None  # accuracy practice: no guessed pages


def run():
    tests = [
        test_heat_storage_literal,
        test_heat_storage_sign_direction,
        test_heat_storage_conservation_closure,
        test_convective_literal_and_linearity,
        test_conductive_literal_and_thickness,
        test_radiative_sigma_is_exact_constant,
        test_radiative_fourth_power_law,
        test_radiative_uses_committed_sigma,
        test_radiative_physiological_range_kelvin,
        test_evaporative_literal_and_product,
        test_empirical_coefficients_uncommitted,
        test_all_are_atomic_equations_with_output_units,
    ]
    for t in tests:
        t()
    print(f"thermo gate: {len(tests)} tests passed; "
          f"{len(T.THERMO_EQUATIONS)} definitional heat-balance equations "
          f"(sigma exact-committed; h/k/epsilon/lam uncommitted)")
    return 0


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

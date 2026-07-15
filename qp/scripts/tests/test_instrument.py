"""Gate for the instrument / measurement-response layer (scripts.instrument).

Every assertion is anchored to an EXACT mathematical identity, never an invented
device number, so a wrong or perturbed relation must fail:

  first-order step  f(τ)  = 1 - e^-1 = 0.6321205588…   f(2τ) = 1 - e^-2 = 0.8646…
  rise time         t_r/τ = ln 9      = 2.1972…  (≈ 2.20)
  SNR               equal signal & noise ⇒ 1
  decibel gain      ×10 amplitude ⇒ 20 dB;  ×1 ⇒ 0 dB;  ×100 ⇒ 40 dB
  natural freq      ω_n = √(k/m);  k=4,m=1 ⇒ 2
  damping ratio     ζ = c/(2√(km));  c=2√(km) ⇒ 1 (critical)

Run: python -m scripts.tests.test_instrument
"""
import math

from scripts.extensions import instrument as I
from scripts import dimensions as D


ALL_EQS = (
    I.first_order_step_response, I.rise_time_10_90, I.signal_to_noise_ratio,
    I.decibel_gain, I.natural_frequency, I.second_order_damping_ratio,
)


def _close(a, b):
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12)


def test_first_order_step_response_exact():
    f = I.first_order_step_response.compute
    # exact definitional anchors
    assert _close(f(t=0.0, tau=1.0), 0.0)
    assert _close(f(t=1.0, tau=1.0), 1.0 - math.e**-1)      # 0.6321205588…
    assert _close(f(t=1.0, tau=1.0), 0.6321205588285577)
    assert _close(f(t=2.0, tau=1.0), 1.0 - math.e**-2)      # 0.8646647168…
    # scale-invariance in t/τ (τ is a free input, not a committed value)
    assert _close(f(t=5.0, tau=5.0), f(t=1.0, tau=1.0))
    # mutation guard: the +/- sign of the exponent matters
    assert not _close(f(t=1.0, tau=1.0), 1.0 - math.e**-2)


def test_rise_time_is_ln9_times_tau():
    tr = I.rise_time_10_90.compute
    ratio = tr(tau=1.0) / 1.0
    assert _close(ratio, math.log(9.0))                     # exact ln 9
    assert _close(ratio, 2.1972245773362196)
    assert abs(ratio - 2.2) < 0.01                          # ties to the ~2.2τ rule
    # consistency with the first-order form it is derived from:
    # t_r is the width of the 10%→90% band of f(t)=1-e^{-t/τ}
    f = I.first_order_step_response.compute
    t10 = math.log(10.0 / 9.0)      # f = 0.1
    t90 = math.log(10.0)            # f = 0.9
    assert _close(f(t=t10, tau=1.0), 0.1)
    assert _close(f(t=t90, tau=1.0), 0.9)
    assert _close(t90 - t10, tr(tau=1.0))
    # linear in τ
    assert _close(tr(tau=3.0), 3.0 * math.log(9.0))


def test_snr_ratio():
    snr = I.signal_to_noise_ratio.compute
    assert _close(snr(mu_signal=1.0, sigma_noise=1.0), 1.0)   # equal ⇒ 1
    assert _close(snr(mu_signal=10.0, sigma_noise=2.0), 5.0)
    # mutation guard: it is a ratio, not a difference
    assert not _close(snr(mu_signal=10.0, sigma_noise=2.0), 8.0)


def test_decibel_gain():
    g = I.decibel_gain.compute
    assert _close(g(V_out=1.0, V_in=1.0), 0.0)               # unity ⇒ 0 dB
    assert _close(g(V_out=10.0, V_in=1.0), 20.0)             # ×10 ⇒ 20 dB (amplitude)
    assert _close(g(V_out=100.0, V_in=1.0), 40.0)            # ×100 ⇒ 40 dB
    assert _close(g(V_out=0.5, V_in=1.0), 20.0 * math.log10(0.5))
    # mutation guard: amplitude uses 20·log10, not 10·log10
    assert not _close(g(V_out=10.0, V_in=1.0), 10.0)


def test_natural_frequency():
    w = I.natural_frequency.compute
    assert _close(w(k=4.0, m=1.0), 2.0)                      # √(4/1)
    assert _close(w(k=1.0, m=1.0), 1.0)
    assert _close(w(k=9.0, m=4.0), 1.5)                      # √(9/4)
    # mutation guard: it is √(k/m), not k/m
    assert not _close(w(k=4.0, m=1.0), 4.0)


def test_damping_ratio():
    z = I.second_order_damping_ratio.compute
    # critical damping: c = 2√(km) ⇒ ζ = 1 exactly
    k, m = 4.0, 1.0
    c_crit = 2.0 * math.sqrt(k * m)
    assert _close(z(c=c_crit, k=k, m=m), 1.0)
    # underdamped: half the critical damping ⇒ ζ = 0.5
    assert _close(z(c=c_crit / 2.0, k=k, m=m), 0.5)
    # overdamped ⇒ ζ > 1
    assert z(c=c_crit * 2.0, k=k, m=m) > 1.0
    # mutation guard: the factor 2 in the denominator matters
    assert not _close(z(c=c_crit, k=k, m=m), 2.0)


def test_no_device_values_committed():
    """The definitional core must not smuggle in a device spec: no parameter
    carries a default value (τ, k, m, c, noise floor are supplied at call time)."""
    for eq in (I.first_order_step_response, I.rise_time_10_90,
               I.signal_to_noise_ratio, I.decibel_gain,
               I.natural_frequency, I.second_order_damping_ratio):
        for p in eq.parameters:
            assert p.default_value is None, (
                f"{eq.id}:{p.name} committed a device value {p.default_value}")
    assert isinstance(I.NEEDS_SOURCE, list) and I.NEEDS_SOURCE


def test_output_dimensions_consistent():
    """Every declared output_units must parse to a KNOWN dimension with the
    expected signature — a structural check against the independent dimensional
    engine (scripts.dimensions), not math-tested-against-math. This catches the
    'dB'-as-unit regression: a decibel is a dimensionless log ratio, so its
    output must parse to '1', never UNKNOWN."""
    expected = {
        I.first_order_step_response: "1",     # fractional approach, dimensionless
        I.rise_time_10_90:           "T",     # a time
        I.signal_to_noise_ratio:     "1",     # pure amplitude ratio
        I.decibel_gain:              "1",     # dB is a dimensionless log ratio
        I.natural_frequency:         "1/T",   # rad/s → frequency (rad dimensionless)
        I.second_order_damping_ratio:"1",     # dimensionless
    }
    for eq, sig in expected.items():
        d = D.parse(eq.output_units)
        assert d.known, f"{eq.id}: output_units {eq.output_units!r} → UNKNOWN dimension"
        assert d.signature() == sig, (
            f"{eq.id}: output_units {eq.output_units!r} → {d.signature()!r}, expected {sig!r}")


def test_input_units_declared_and_parse():
    """Every parameter carries a units string that the dimensional engine can
    resolve (k in N/m, m in kg, c in N*s/m, …) — so dimensional consistency is
    checkable at call time, not asserted by naked prose."""
    for eq in ALL_EQS:
        for p in eq.parameters:
            assert p.units, f"{eq.id}:{p.name} has no units string"
            assert D.parse(p.units).known, (
                f"{eq.id}:{p.name} units {p.units!r} do not resolve to a known dimension")


def test_ids_unique_no_collision():
    """The definitional module must not shadow or collide with any canonical
    equation id — the one uniqueness invariant that is checkable inside this
    file without wiring the module into run_gate.py."""
    from scripts.canonical_ids import CANONICAL_EQUATIONS
    ids = [eq.id for eq in ALL_EQS]
    assert len(ids) == len(set(ids)), "duplicate id within the instrument module"
    for eid in ids:
        assert eid not in CANONICAL_EQUATIONS, (
            f"instrument id {eid!r} collides with a canonical equation")


TESTS = (
    test_first_order_step_response_exact,
    test_rise_time_is_ln9_times_tau,
    test_snr_ratio,
    test_decibel_gain,
    test_natural_frequency,
    test_damping_ratio,
    test_no_device_values_committed,
    test_output_dimensions_consistent,
    test_input_units_declared_and_parse,
    test_ids_unique_no_collision,
)


def run():
    for t in TESTS:
        t()
    print(f"instrument gate: {len(TESTS)} tests passed; "
          f"6 definitional equations anchored to exact identities "
          f"(1-e^-1=0.6321, ln9=2.1972, 20log10(10)=20dB); outputs dimensionally "
          f"resolvable (dB→dimensionless), ids collision-free, no device values committed")
    return 0


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

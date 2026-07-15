"""Gate for the pharmacokinetic definitional core (scripts.pk).

Feature 2 was reduced on review: 7 of the 8 originally-proposed relations duplicate
an existing registered concept (match-by-concept, CLAUDE.md §3.3) and were removed.
What remains is the one relation with no registry equivalent:

  * t_ss = n · t½   (time as a number n of elimination half-lives)

The relation is pure multiplication once n (a caller-supplied count of half-lives) is
given, so every assertion drives ``eq.compute(...)`` against a DEFINITIONAL identity
that needs no drug data — a wrong or perturbed relation must fail, and no invented
number (in particular no n=5 convention) is enshrined as a default.

This module imports scripts.pk DIRECTLY and never touches scripts.canonical_ids or the
global index (scripts.pk is a standalone, unregistered draft).

Run: python -m scripts.tests.test_pk
"""

from scripts.extensions import pk


def test_time_to_steady_state_is_n_half_lives():
    # relation is pure multiplication; exact for any n and any t_half
    t_half = 4.0
    for n in (3.0, 4.0, 5.0, 7.5):
        assert pk.time_to_steady_state.compute(t_half=t_half, n=n) == n * t_half


def test_time_to_steady_state_requires_explicit_n():
    # no convention (e.g. n=5) is baked in as a default: n must be supplied
    try:
        pk.time_to_steady_state.compute(t_half=4.0)
    except TypeError:
        pass
    else:
        raise AssertionError("n must be caller-supplied (no committed default)")


def test_time_to_steady_state_scales_linearly_in_both_factors():
    # doubling either factor doubles the result (definitional bilinearity)
    base = pk.time_to_steady_state.compute(t_half=2.0, n=4.0)
    assert pk.time_to_steady_state.compute(t_half=4.0, n=4.0) == 2.0 * base
    assert pk.time_to_steady_state.compute(t_half=2.0, n=8.0) == 2.0 * base


def test_all_equations_are_wellformed():
    assert len(pk.EQUATIONS) == 1
    for eid, eq in pk.EQUATIONS.items():
        assert eq.id == eid
        assert eq.category is pk.CATEGORY          # FOUNDATIONS bucket
        assert eq.output_units is not None
        assert eq.produces is not None
        assert callable(eq._compute_func)
        # no drug-specific numeric or convention committed as a default_value
        for p in eq.parameters:
            assert p.default_value is None


def run():
    tests = [
        test_time_to_steady_state_is_n_half_lives,
        test_time_to_steady_state_requires_explicit_n,
        test_time_to_steady_state_scales_linearly_in_both_factors,
        test_all_equations_are_wellformed,
    ]
    for t in tests:
        t()
    print(f"pk gate: {len(pk.EQUATIONS)} definitional PK equation "
          f"(t_ss = n*t_half, n caller-supplied), {len(tests)} identity tests pass, "
          f"no drug data and no committed convention")
    return 0


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

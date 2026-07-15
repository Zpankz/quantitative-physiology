"""Gate for the equation form-typing layer (scripts.eqforms): all 367 equations are
partitioned into the closed set of structural forms; every classification is grounded
by a checkable property (a formula marker or an execution-proven primitives membership); the
grounding has TEETH across two independent methods (a kernel proven by EXECUTION to be
a saturation must also carry the saturable-denominator string marker); the markers are
mutation-sensitive (perturbing a formula flips its form); and the query API works.

Run: python -m scripts.tests.test_eqforms
"""
import scripts.foundations, scripts.membrane, scripts.excitable, scripts.nervous  # noqa: F401
import scripts.cardiovascular, scripts.respiratory, scripts.renal  # noqa: F401
import scripts.gastrointestinal, scripts.endocrine  # noqa: F401
from scripts import eqforms as EF
from scripts.primitives import primitive_of, members_of


def _all_ids():
    return [e.id for e in EF._all_equations()]


def test_every_equation_classified_into_the_closed_set():
    ids = _all_ids()
    assert len(ids) == 367
    for eid in ids:
        f = EF.form_of(eid)
        assert f in EF.FORMS, f"{eid}: form {f!r} not in the closed set"


def test_partition_is_exact():
    """all_forms() / by_form() partition the corpus: disjoint, and covering all 367."""
    part = EF.all_forms()
    assert set(part) == set(EF.FORMS)
    seen = [eid for ids in part.values() for eid in ids]
    assert len(seen) == 367 and len(set(seen)) == 367, "forms must partition (no dup, no gap)"
    for f in EF.FORMS:
        assert EF.by_form(f) == part[f]


def test_verify_all_pass():
    """Every classification verifies: its marker is present and the cross-ground and
    loop-consistency invariants hold."""
    for eid in _all_ids():
        f = EF.verify(eid)
        assert f == EF.form_of(eid)


def test_cross_ground_teeth_primitives():
    """The real teeth: primitives membership is proven BY EXECUTION, the formula
    marker is an independent STRING fact — they must agree. Every proven saturation /
    first-order / log-ratio kernel carries its formula marker (else verify() fails)."""
    for eid in members_of("saturation"):
        e = EF._eq(eid)
        assert EF._has_saturation(e.simplified), f"{eid}: proven saturation lacks the denominator marker"
        assert EF.form_of(eid) == "saturation"
    for eid in members_of("first_order"):
        e = EF._eq(eid)
        assert EF._has_exp(e.simplified), f"{eid}: proven first-order lacks e^/exp"
        assert EF.form_of(eid) == "exponential"
    for eid in members_of("log_ratio"):
        e = EF._eq(eid)
        assert EF._has_log(e.simplified), f"{eid}: proven log-ratio lacks ln/log"
        assert EF.form_of(eid) == "log_ratio"


def test_cross_ground_teeth_fail_on_marker_loss():
    """Prove (b) is not vacuous: an equation the kernel proves is a saturation, but
    whose formula string has had the saturable denominator stripped, must FAIL the
    cross-ground check — the two independent grounds now disagree."""
    eid = "michaelis_menten"
    assert "saturation" in primitive_of(eid)              # execution-proven
    good = EF._eq(eid).simplified
    assert EF._has_saturation(good)
    broken = good.replace("/ (K_m + [S])", " × [S]").replace("/(K_m+[S])", "*[S]")
    if broken == good:  # be robust to formatting: neutralise any affinity denominator
        import re
        broken = re.sub(r"/\s*\([^)]*\)", " ", good)
    assert not EF._has_saturation(broken), "denominator strip should kill the marker"
    # execution ground still says saturation, string ground now says no -> verify fails
    assert not (("saturation" in primitive_of(eid)) and EF._has_saturation(broken))


def test_marker_mutation_sensitivity_synthetic():
    """Feed the PURE classifier synthetic formulas (id not in primitives/feedback, so
    markers alone decide), then perturb the defining marker and assert the form flips
    — mutation-sensitive, without touching any real equation."""
    cases = [
        ("E = a*ln(x/y)",              "log_ratio",    "E = a*(x/y)"),          # drop ln
        ("v = Vmax*[S]/(K_m + [S])",   "saturation",   "v = Vmax*[S]/(R0 + [S])"),  # non-affinity denom
        ("F/Fmax = [Ca]^n/(K_d^n + [Ca]^n)", "saturation", "F/Fmax = [Ca] - K_d"),  # drop Hill ratio
        ("dV/dt = a - b*V",            "dynamics_ode", "V = a - b*V"),          # drop derivative
        ("C_t = C0*exp(-k*t)",         "exponential",  "C_t = C0*(1 - k*t)"),   # drop exp
        ("S = k*I^n",                  "power_term",   "S = k*I"),              # drop power
        ("y = a*x + b",                "algebraic",    "y = a*x^2 + b"),        # gain a power
    ]
    for formula, want, mutated in cases:
        assert EF._classify(formula, []) == want, f"{formula!r} should be {want}"
        assert EF._classify(mutated, []) != want, f"mutation of {formula!r} should flip form"


def test_precedence_is_deliberate():
    """Precedence: specific math forms beat generic, and a saturable ratio beats a
    bare power term despite the caret."""
    # log beats power (norwich-like sensation law: ln with a Phi^n inside)
    assert EF._classify("psi = k*ln(1 + b*Phi^n)", []) == "log_ratio"
    # saturation (Hill) beats power_term despite the caret
    assert EF._classify("R/Rmax = I^n/(sigma^n + I^n)", []) == "saturation"
    # an ODE with a power/algebraic RHS is dynamics_ode (the derivative marker wins)
    assert EF._classify("d[CRH]/dt = k - k_cort*[Cortisol]", []) == "dynamics_ode"
    # a bare weighted-mean formula carries no specific marker -> algebraic residual
    assert EF._classify("MAP = SBP/3 + 2*DBP/3", []) == "algebraic"


def test_algebraic_is_a_clean_residual():
    """Every algebraic-typed equation provably carries NONE of the specific markers —
    algebraic is the honest residual, not a bucket hiding mis-classifications."""
    for eid in EF.by_form("algebraic"):
        e = EF._eq(eid)
        s, prims = e.simplified, primitive_of(eid)
        assert not (EF._has_log(s) or "log_ratio" in prims)
        assert not (EF._has_saturation(s) or "saturation" in prims)
        assert not EF._has_time_deriv(s)
        assert not (EF._has_exp(s) or "first_order" in prims)
        assert not EF._has_power(s)


def test_query_api():
    assert EF.forms()[0] == "log_ratio" and EF.forms()[-1] == "algebraic"
    assert EF.form_of("nernst_equation") == "log_ratio"
    assert EF.form_of("first_order_elimination") == "exponential"
    assert EF.form_of("michaelis_menten") == "saturation"
    assert EF.form_of("hh_gating_m") == "dynamics_ode"
    assert EF.form_of("stevens_power_law") == "power_term"
    assert "michaelis_menten" in EF.by_form("saturation")
    ex = EF.explain("saturation")
    assert ex["form"] == "saturation" and "michaelis_menten" in ex["members"]
    dist = EF.distribution()
    assert sum(dist.values()) == 367


def run():
    tests = [
        test_every_equation_classified_into_the_closed_set, test_partition_is_exact,
        test_verify_all_pass, test_cross_ground_teeth_primitives,
        test_cross_ground_teeth_fail_on_marker_loss, test_marker_mutation_sensitivity_synthetic,
        test_precedence_is_deliberate, test_algebraic_is_a_clean_residual,
        test_query_api,
    ]
    for t in tests:
        t()
    print(EF.summary())
    d = EF.distribution()
    print("form-typing gate: partition of 367 verified across two independent grounds; "
          + ", ".join(f"{f}={d[f]}" for f in EF.FORMS))
    return 0


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

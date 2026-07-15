"""Gate for the feedback-loop layer (scripts.feedback): every loop is grounded
(members are real equations; formula-tier loops close via an inhibitory term that
actually appears in a member's formula), the grounding check has teeth, and the
compute DAG remains ACYCLIC — the loop layer represents feedback *beside* the DAG
without introducing a cycle into it.

Run: python -m scripts.tests.test_feedback
"""
import scripts.foundations, scripts.membrane, scripts.excitable, scripts.nervous  # noqa: F401
import scripts.cardiovascular, scripts.respiratory, scripts.renal  # noqa: F401
import scripts.gastrointestinal, scripts.endocrine  # noqa: F401
from scripts import feedback as FB
from scripts.canonical_ids import CANONICAL_EQUATIONS


def test_every_loop_is_grounded():
    for name in FB.loops():
        assert FB.verify(name), f"loop {name} not grounded"
        for m in FB.LOOPS[name]["members"]:
            assert m in CANONICAL_EQUATIONS, f"{name}: member {m} is not a real equation"
    assert len(FB.loops()) >= 6


def test_formula_grounding_has_teeth():
    """A formula-tier loop closes via an inhibitory term truly in the formula;
    a bogus token must NOT be found (else 'negative feedback' is vacuous)."""
    from scripts.canonical_ids import load
    eid, token = FB.LOOPS["hpa_axis"]["closes_via"]
    simp = load(eid).simplified
    assert FB._has_inhibitory_term(simp, token)              # real: '− k_cort·[Cortisol]'
    assert not FB._has_inhibitory_term(simp, "Zorblax")      # bogus token fails
    # at least the three ODE axes are formula-verified, not merely structural
    assert sum(FB.grounding(n) == "formula" for n in FB.loops()) >= 3


def test_query_api():
    assert FB.loops_of("hpa_crh_dynamics") == ["hpa_axis"]
    assert "hpa_axis" in FB.by_sensed("cortisol")
    assert FB.loop("baroreflex")["grounding"] == "structural"


def test_compute_dag_stays_acyclic():
    """The feedback layer must NOT have added a cycle to the dependency DAG."""
    from scripts.index import get_global_index
    assert get_global_index().detect_cycles() == []


def run():
    for t in (test_every_loop_is_grounded, test_formula_grounding_has_teeth,
              test_query_api, test_compute_dag_stays_acyclic):
        t()
    nf = sum(FB.grounding(n) == "formula" for n in FB.loops())
    print(f"feedback gate: {len(FB.loops())} loops grounded ({nf} formula-verified), "
          f"query API ok, compute DAG still acyclic")
    return 0


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

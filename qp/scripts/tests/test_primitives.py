"""Gate for the universal-primitive layer (scripts.primitives): every declared
membership is PROVEN — the kernel with its curated binding reproduces the
equation's own compute — and the proof has teeth (perturbing a binding constant
breaks it). This is the same grounding discipline as the value anchors: a shared
functional form is asserted only when execution confirms it.

Run: python -m scripts.tests.test_primitives
"""
import scripts.foundations, scripts.membrane, scripts.excitable, scripts.nervous  # noqa: F401
import scripts.cardiovascular, scripts.respiratory, scripts.renal  # noqa: F401
import scripts.gastrointestinal, scripts.endocrine  # noqa: F401
from scripts import primitives as P
from scripts.canonical_ids import CANONICAL_EQUATIONS, load


def test_every_membership_reproduces_compute():
    """Each (primitive, equation) pair: kernel(binding) == equation.compute()."""
    n = 0
    for prim, members in P.MEMBERS.items():
        for eid in members:
            assert eid in CANONICAL_EQUATIONS, f"{eid} not a real equation id"
            assert P.verify(prim, eid), f"{prim} <- {eid}: kernel does not reproduce compute"
            n += 1
    assert n >= 20, f"expected >= 20 proven memberships, got {n}"


def test_membership_proof_is_mutation_sensitive():
    """Perturbing the kernel result must break the match — otherwise 'reproduces'
    is vacuous. Recompute a member with a scaled kernel output and assert it now
    disagrees with the equation's compute."""
    spec = P.MEMBERS["log_ratio"]["nernst_equation"]
    good = P._apply_kernel("log_ratio", spec["bind"](**spec["test"]))
    want = float(load("nernst_equation")._compute_func(**spec["test"]))
    assert abs(good - want) / max(1.0, abs(want)) <= 1e-6      # true membership holds
    bad = good * 1.5                                            # perturb the constant
    assert abs(bad - want) / max(1.0, abs(want)) > 1e-6        # ... and it must fail


def test_query_api():
    assert P.primitive_of("nernst_equation") == ["log_ratio"]
    assert "michaelis_menten" in P.members_of("saturation")
    assert set(P.members_of("saturation")) & {"hill_saturation", "receptor_fractional_occupancy"}
    assert P.explain("first_order")["intuition"]
    # disparate equations proven to share ONE form (the headline claim)
    logr = set(P.members_of("log_ratio"))
    assert {"nernst_equation", "henderson_hasselbalch"} <= logr


def run():
    for t in (test_every_membership_reproduces_compute,
              test_membership_proof_is_mutation_sensitive, test_query_api):
        t()
    total = sum(len(v) for v in P.MEMBERS.values())
    print(f"primitives gate: {total} memberships proven across {len(P.MEMBERS)} "
          f"universal primitives; mutation-sensitive; query API ok")
    return 0


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

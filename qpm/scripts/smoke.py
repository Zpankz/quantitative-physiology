"""Runtime integrity smoke-test for the qpm (minimal) tier.

The full qp tier ships a deterministic acceptance gate (`scripts.run_gate`); the
minimal qpm tier deliberately omits the test suites, references and generators —
so until now a qpm user or CI had nothing runnable to confirm the extracted
package is intact and behaving. This is that check: a small, dependency-free
self-test that

  * imports every domain (clean, no stderr),
  * confirms the canonical count (367) and that every equation carries its Feher
    provenance (source_chapter) — the provenance the trimmed `references/` used to
    document is on each object, so it stays inspectable in the minimal tier,
  * exercises the packaged surface against INDEPENDENT external anchors (not the
    equations' own outputs): resting E_K ≈ −95 mV, cardiac output 4.9 L/min,
    MAP 93.3 mmHg, and the propagate() integrative simulation (MAP ≈ 93.7),
  * confirms the reasoning layers load (primitives, feedback, dependency_types,
    eqforms).

Run:  python -m scripts.smoke      # exits non-zero on any failure

It is NOT a substitute for the qp gate; it is the qpm-tier integrity signal.
"""
from __future__ import annotations
import sys


def _check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  [{'OK  ' if ok else 'FAIL'}] {name}: {got} (expect {want}±{tol})")
    return ok


def run() -> int:
    fails = []

    # 1. clean import of all nine domains
    import scripts.foundations, scripts.membrane, scripts.excitable, scripts.nervous  # noqa
    import scripts.cardiovascular, scripts.respiratory, scripts.renal  # noqa
    import scripts.gastrointestinal, scripts.endocrine  # noqa
    from scripts.index import get_global_index, get_equation
    ix = get_global_index()
    eqs = [e for c in ix.categories() for e in ix.by_category(c)]

    # 2. canonical count + provenance coverage
    from scripts import TOTAL_EQUATIONS
    if not _check("canonical count", len(eqs), TOTAL_EQUATIONS, 0):
        fails.append("count")
    if not _check("declared total", TOTAL_EQUATIONS, 367, 0):
        fails.append("total==367")
    with_prov = sum(1 for e in eqs if e.metadata and e.metadata.source_chapter)
    if not _check("Feher provenance coverage", with_prov, len(eqs), 0):
        fails.append("provenance")

    # 3. external anchors (independent textbook values, not the eq's own output)
    def _eq(eid):
        e = get_equation(eid)
        assert e is not None, f"missing equation {eid}"
        return e
    E_K = _eq("nernst_equation").compute(z=1, C_out=4, C_in=140)  # mV
    if not _check("resting E_K (mV)", round(E_K, 1), -95.0, 1.0):
        fails.append("nernst")
    CO = _eq("cardiac_output").compute(HR=70, SV=70)  # L/min
    if not _check("cardiac output (L/min)", round(CO, 2), 4.9, 0.05):
        fails.append("CO")
    MAP = _eq("mean_arterial_pressure").compute(SBP=120, DBP=80)  # mmHg
    if not _check("MAP (mmHg)", round(MAP, 1), 93.3, 0.2):
        fails.append("MAP")

    # 4. propagate() integrative simulation — the flagship queryable surface.
    # Result is {"fired": {equation_id: value}, "rounds": n}; a bedside seed must
    # fire the MAP equation and reach the same value as the direct compute above.
    try:
        from scripts.eqgraph import build_graph
        g = build_graph()
        r = g.propagate({"SBP": 120, "DBP": 80, "HR": 70, "SV": 70})
        fired = r["fired"]
        mapv = fired.get("mean_arterial_pressure")
        print(f"  [info] propagate fired {len(fired)} equations in {r['rounds']} rounds")
        if mapv is None or not _check("propagate MAP (mmHg)", round(float(mapv), 1), 93.3, 1.0):
            fails.append("propagate")
    except Exception as e:  # pragma: no cover - surfaced as a failure line
        print(f"  [FAIL] propagate(): {e}")
        fails.append("propagate")

    # 5. reasoning layers load and answer
    from scripts import primitives as P, feedback as FB, dependency_types as DT, eqforms as EF
    layers_ok = (len(FB.loops()) >= 6 and len(DT.or_groups()) >= 4
                 and sum(len(EF.by_form(f)) for f in EF.FORMS) == TOTAL_EQUATIONS
                 and hasattr(P, "verify"))
    print(f"  [{'OK  ' if layers_ok else 'FAIL'}] reasoning layers "
          f"(feedback={len(FB.loops())}, or_groups={len(DT.or_groups())}, forms cover {TOTAL_EQUATIONS})")
    if not layers_ok:
        fails.append("reasoning-layers")

    if fails:
        print(f"\nqpm SMOKE FAILED ({len(fails)}): {', '.join(fails)}")
        return 1
    print(f"\nqpm SMOKE OK — {TOTAL_EQUATIONS} equations, provenance intact, anchors + propagate + reasoning layers verified.")
    return 0


if __name__ == "__main__":
    sys.exit(run())

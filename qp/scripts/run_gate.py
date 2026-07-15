"""One-command acceptance gate: runs EVERY numerical suite + doc gate + integration
+ verification sensor + clean-import + idempotence, and exits non-zero if anything
fails. Addresses the gap that the documented gate only invoked two suites, so a
wrong coefficient in a non-foundation equation could pass. Run:

  python -m scripts.run_gate

Each suite is imported and its module-level self-check executed in-process.
"""
import subprocess
import sys

SUITES = [
    "scripts.test_public_api",
    "scripts.tests.test_doc_counts",
    "scripts.foundations.test_foundations",
    "scripts.tests.test_coverage_additions",
    "scripts.tests.test_clinical_additions",
    "scripts.tests.test_reference_values_locked",
    "scripts.tests.test_reference_values_audit",
    "scripts.tests.test_dimensions_graph",
    "scripts.tests.test_integration_chains",
    "scripts.tests.test_reference_values_grok",
    "scripts.tests.test_review_additions",
    "scripts.tests.test_adversarial_review_fixes",
    "scripts.tests.test_backlog_additions",
    "scripts.tests.test_reference_ids",
    "scripts.tests.test_primitives",
    "scripts.tests.test_feedback",
    "scripts.tests.test_dependency_types",
    "scripts.tests.test_eqforms",
    "scripts.tests.test_pk",
    "scripts.tests.test_instrument",
    "scripts.tests.test_thermo",
]
OTHER = [
    "scripts.doc_examples_gate",
    "scripts.integration_gate",
    "scripts.verification_gate",
]


def _run(mod):
    # Every suite exits non-zero on failure (returns 1-if-failed, or an uncaught
    # AssertionError from its self-check), so the exit code is the whole signal —
    # no fragile parsing of "N failed" strings.
    r = subprocess.run([sys.executable, "-m", mod], capture_output=True, text=True)
    tail = (r.stdout.strip().splitlines() or [""])[-1]
    return r.returncode == 0, tail, r.stderr.strip()


def _regenerate_idempotent():
    """Regenerate canonical_ids/graph/clusters twice; assert byte-identical (§4 #9)."""
    import hashlib
    from pathlib import Path
    gens = ["scripts._build_canonical_ids", "scripts.generate_graph", "scripts.generate_clusters"]
    artifacts = ["scripts/canonical_ids.py", "graph/dependency-graph.json", "graph/clusters.json"]

    def _digest():
        h = {}
        for a in artifacts:
            p = Path(a)
            h[a] = hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
        return h
    for g in gens:
        subprocess.run([sys.executable, "-m", g], capture_output=True, text=True)
    first = _digest()
    for g in gens:
        subprocess.run([sys.executable, "-m", g], capture_output=True, text=True)
    second = _digest()
    return first == second


def main():
    fails = []
    ok = _regenerate_idempotent()
    print(f"  [{'OK  ' if ok else 'FAIL'}] regenerate x2 byte-identical (idempotence, §4 #9)")
    if not ok:
        fails.append(("idempotence", "regenerate not byte-identical"))
    for mod in SUITES + OTHER:
        ok, tail, err = _run(mod)
        mark = "OK  " if ok else "FAIL"
        print(f"  [{mark}] {mod}: {tail}")
        if not ok:
            fails.append((mod, err[-300:]))
    # clean import stderr must be 0
    imp = subprocess.run(
        [sys.executable, "-c",
         "import scripts.foundations,scripts.membrane,scripts.excitable,scripts.nervous,"
         "scripts.cardiovascular,scripts.respiratory,scripts.renal,scripts.gastrointestinal,"
         "scripts.endocrine"],
        capture_output=True, text=True)
    imp_lines = len([l for l in imp.stderr.splitlines() if l.strip()])
    print(f"  [{'OK  ' if imp_lines == 0 else 'FAIL'}] clean import stderr lines: {imp_lines}")
    if imp_lines:
        fails.append(("clean-import", imp.stderr[-300:]))
    if fails:
        print(f"\nGATE FAILED ({len(fails)}):")
        for m, e in fails:
            print(f"  - {m}: {e}")
        sys.exit(1)
    print("\nGATE GREEN — all suites, doc gate, integration, sensor, clean import.")


if __name__ == "__main__":
    main()

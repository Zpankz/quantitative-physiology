"""API-surface integration test for the quantitative-physiology package.

This is the safety net that pins the *documented public surface* to the code.
It would have caught every defect fixed in the rearchitecture: broken SKILL.md
imports, dangling depends_on edges, graph ids with no equation, stale counts,
and drifted registry pointers.

Run standalone (no pytest needed):
    python scripts/tests/test_public_api.py
or under pytest:
    pytest scripts/tests/test_public_api.py
"""
import importlib, glob, os, sys, io, contextlib, json

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from scripts.base import AtomicEquation           # noqa: E402
from scripts import canonical_ids as C             # noqa: E402


def _domain_modules():
    return [f[:-3].replace(os.sep, ".") for f in
            glob.glob(os.path.join("scripts", "**", "*.py"), recursive=True)
            if not os.path.basename(f).startswith(("__init__", "test_", "_"))]


def _scan():
    """id -> list of (module, object_name); silences the flat-id warnings."""
    locs = {}
    with contextlib.redirect_stderr(io.StringIO()):
        for mod in _domain_modules():
            m = importlib.import_module(mod)
            for name, obj in vars(m).items():
                if isinstance(obj, AtomicEquation):
                    locs.setdefault(obj.id, []).append((mod, name))
    return locs


# The documented cross-domain import contract (mirrors SKILL.md's table).
# (module, object_name) — every pair must import to a working equation.
SKILL_IMPORT_CONTRACT = [
    ("scripts.foundations.thermodynamics", "nernst_equation"),
    ("scripts.foundations.diffusion",      "fick_first_law"),
    ("scripts.foundations.transport",      "poiseuille_flow"),
    ("scripts.foundations.kinetics",       "michaelis_menten"),
    ("scripts.respiratory.oxygen_transport", "hill_equation"),
    ("scripts.respiratory.acid_base",      "henderson_hasselbalch"),
    ("scripts.cardiovascular.microcirculation", "starling_filtration"),
    ("scripts.excitable.membrane_potential", "ghk_potential_eq"),
]


def test_all_modules_import():
    fails = []
    with contextlib.redirect_stderr(io.StringIO()):
        for mod in _domain_modules():
            try:
                importlib.import_module(mod)
            except Exception as e:
                fails.append((mod, f"{type(e).__name__}: {e}"))
    assert not fails, f"module import failures: {fails}"


def test_no_duplicate_ids():
    dups = {k: v for k, v in _scan().items() if len(v) > 1}
    assert not dups, f"duplicate equation ids across modules: {dups}"


def test_canonical_map_matches_code():
    locs = _scan()
    code_ids = set(locs)
    canon_ids = set(C.CANONICAL_EQUATIONS)
    assert code_ids == canon_ids, (
        f"canonical map out of sync — only in code: {code_ids - canon_ids}; "
        f"only in map: {canon_ids - code_ids} (re-run _build_canonical_ids)")
    # object names in the map must match reality
    for cid, e in C.CANONICAL_EQUATIONS.items():
        mod, name = e["module"], e["object"]
        obj = getattr(importlib.import_module(mod), name)
        assert obj.id == cid, f"{mod}.{name} has id {obj.id!r}, map says {cid!r}"


def test_every_equation_has_working_compute():
    locs = _scan()
    for cid in locs:
        eq = C.load(cid)
        assert eq._compute_func is not None, f"{cid} has no compute function"
        assert callable(eq.compute), f"{cid}.compute not callable"


def test_all_depends_on_resolve():
    locs = _scan()
    ids = set(locs)
    bad = []
    with contextlib.redirect_stderr(io.StringIO()):
        for mod in _domain_modules():
            m = importlib.import_module(mod)
            for name, obj in vars(m).items():
                if isinstance(obj, AtomicEquation):
                    for dep in obj.depends_on:
                        if C.resolve(dep) not in ids:
                            bad.append((obj.id, dep))
    assert not bad, f"dangling depends_on edges: {bad}"


def test_skill_import_contract():
    bad = []
    for mod, name in SKILL_IMPORT_CONTRACT:
        try:
            obj = getattr(importlib.import_module(mod), name)
            assert isinstance(obj, AtomicEquation)
        except Exception as e:
            bad.append((mod, name, f"{type(e).__name__}: {e}"))
    assert not bad, f"documented imports that fail: {bad}"


def test_registry_pointers_resolve():
    from scripts.registry import CROSS_DOMAIN_EQUATIONS
    bad = []
    for eq in CROSS_DOMAIN_EQUATIONS.all_equations():
        try:
            obj = getattr(importlib.import_module(eq.module_path), eq.object_name)
            assert obj.id == eq.id
        except Exception as e:
            bad.append((eq.id, f"{type(e).__name__}: {e}"))
    assert not bad, f"registry entries that do not resolve: {bad}"


def test_graph_ids_exist():
    locs = _scan()
    ids = set(locs)
    g = json.load(open(os.path.join("graph", "dependency-graph.json")))
    missing = set()
    for cid in g["cross_domain_equations"]:
        if cid not in ids:
            missing.add(("cross_domain", cid))
    for a, b in g["dependency_edges"]:
        if a not in ids:
            missing.add(("edge_from", a))
        if b not in ids:
            missing.add(("edge_to", b))
    for layer, members in g["topological_layers"].items():
        for cid in members:
            if cid not in ids:
                missing.add((layer, cid))
    for chain, members in g["named_chains"].items():
        for cid in members:
            if cid not in ids:
                missing.add((chain, cid))
    assert not missing, f"graph references non-existent ids: {sorted(missing)}"


def test_equation_counts_match():
    from scripts import EQUATION_COUNTS, TOTAL_EQUATIONS
    locs = _scan()
    actual = {}
    for cid, places in locs.items():
        dom = places[0][0].split(".")[1]
        actual[dom] = actual.get(dom, 0) + 1
    assert actual == dict(EQUATION_COUNTS), (
        f"EQUATION_COUNTS mismatch — actual {actual} vs declared {dict(EQUATION_COUNTS)}")
    assert TOTAL_EQUATIONS == len(locs), (
        f"TOTAL_EQUATIONS {TOTAL_EQUATIONS} != actual {len(locs)}")


ALL_TESTS = [v for k, v in sorted(globals().items()) if k.startswith("test_")]


def main():
    passed = failed = 0
    for t in ALL_TESTS:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(ALL_TESTS)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

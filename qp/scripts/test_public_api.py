"""Public-API integration test for the quantitative-physiology package.

Run from the package parent directory:
    python -m scripts.test_public_api        # plain runner, exits non-zero on failure
    (or, if pytest is available)  pytest scripts/test_public_api.py -q

This is the safety net that the package previously lacked. It exercises the
DOCUMENTED public surface and the internal consistency invariants, so that
drift between code, docs, the registry and the dependency graph fails loudly
instead of silently returning wrong imports. Every check here corresponds to a
real defect found in the pre-refactor package.
"""
import importlib
import glob
import os
import sys
import io
import contextlib
import json
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from scripts.base import AtomicEquation                 # noqa: E402
from scripts import canonical_ids as C                  # noqa: E402


def _iter_equation_modules():
    for f in glob.glob(os.path.join(ROOT, "scripts", "**", "*.py"), recursive=True):
        base = os.path.basename(f)
        if base.startswith(("__init__", "test_", "_")):
            continue
        rel = os.path.relpath(f, ROOT)
        yield rel[:-3].replace(os.sep, ".")


def _scan_module_equations():
    """id -> list of (module, object). Suppresses the flat-id stderr warnings."""
    locations = defaultdict(list)
    with contextlib.redirect_stderr(io.StringIO()):
        for mod in _iter_equation_modules():
            m = importlib.import_module(mod)
            for name, obj in vars(m).items():
                if isinstance(obj, AtomicEquation):
                    locations[obj.id].append((mod, name))
    return locations


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_no_duplicate_module_level_ids():
    """Every equation id is defined by exactly one module-level object."""
    dups = {k: v for k, v in _scan_module_equations().items() if len(v) > 1}
    assert not dups, f"Duplicate equation ids across modules: {dups}"


def test_every_canonical_id_imports_and_computes():
    """Each canonical entry resolves to an AtomicEquation with a compute function."""
    problems = []
    for cid in C.CANONICAL_EQUATIONS:
        try:
            eq = C.load(cid)
        except Exception as e:  # import/attr failure
            problems.append(f"{cid}: load failed ({e})")
            continue
        if not isinstance(eq, AtomicEquation):
            problems.append(f"{cid}: not an AtomicEquation")
        elif eq.id != cid:
            problems.append(f"{cid}: object.id mismatch ({eq.id})")
        elif eq._compute_func is None or not callable(eq._compute_func):
            problems.append(f"{cid}: no callable compute function")
    assert not problems, "Canonical equations with problems:\n  " + "\n  ".join(problems)


def test_documented_cross_domain_imports_resolve():
    """The cross-domain equations advertised to users all import from the
    stated module under the stated object name (the SKILL.md import table)."""
    problems = []
    for cid in C.CROSS_DOMAIN:
        entry = C.CANONICAL_EQUATIONS.get(cid)
        if entry is None:
            problems.append(f"{cid}: not in canonical map")
            continue
        try:
            mod = importlib.import_module(entry["module"])
        except Exception as e:
            problems.append(f"{cid}: module {entry['module']} import failed ({e})")
            continue
        obj = getattr(mod, entry["object"], None)
        if not isinstance(obj, AtomicEquation) or obj.id != cid:
            problems.append(f"{cid}: {entry['module']}.{entry['object']} does not resolve to it")
    assert not problems, "Broken documented cross-domain imports:\n  " + "\n  ".join(problems)


def test_all_aliases_resolve():
    """Every legacy alias points at a real canonical id."""
    bad = {a: t for a, t in C.ALIAS_TO_CANONICAL.items() if t not in C.CANONICAL_EQUATIONS}
    assert not bad, f"Aliases pointing at unknown ids: {bad}"


def test_every_depends_on_edge_references_a_real_id():
    """Every `depends_on` id must be a REAL equation id -- not merely
    alias-resolvable. Resolving through the alias map here would mask exactly
    the dangling-edge defect that breaks index.topological_order(), so this
    check is deliberately strict."""
    real = set(C.CANONICAL_EQUATIONS)
    dangling = []
    with contextlib.redirect_stderr(io.StringIO()):
        for mod in _iter_equation_modules():
            m = importlib.import_module(mod)
            for name, obj in vars(m).items():
                if isinstance(obj, AtomicEquation):
                    for dep in obj.depends_on:
                        if dep not in real:
                            via = C.resolve(dep)
                            hint = f" (alias-resolves to '{via}'; use the real id)" if via else ""
                            dangling.append(f"{obj.id} -> {dep}{hint}")
    assert not dangling, "depends_on edges that are not real equation ids:\n  " + "\n  ".join(dangling)


def test_index_topological_order_succeeds():
    """The live EquationIndex must produce a valid topological order over every
    registered equation, and agree with detect_cycles(). Direct regression test
    for the 'topological_order() raises ValueError while detect_cycles() is
    empty' defect (a dangling dep inflating in-degree and masquerading as a
    cycle)."""
    for d in ("foundations", "membrane", "excitable", "nervous", "cardiovascular",
              "respiratory", "renal", "gastrointestinal", "endocrine"):
        importlib.import_module(f"scripts.{d}")
    from scripts.index import get_global_index
    idx = get_global_index()
    assert idx.detect_cycles() == [], f"unexpected cycles reported: {idx.detect_cycles()[:5]}"
    order = idx.topological_order()  # must not raise
    assert len(order) == len(idx), \
        f"topological order covers {len(order)} of {len(idx)} equations"
    pos = {eid: i for i, eid in enumerate(order)}
    for eid in order:
        for dep in C.load(eid).depends_on:
            assert dep in pos and pos[dep] < pos[eid], \
                f"dependency '{dep}' must precede '{eid}' in topological order"


def test_registry_pointers_all_resolve():
    """Every cross-domain registry entry points at a real importable object."""
    from scripts.registry import CROSS_DOMAIN_EQUATIONS
    problems = []
    for eq in CROSS_DOMAIN_EQUATIONS.all_equations():
        try:
            mod = importlib.import_module(eq.module_path)
        except Exception as e:
            problems.append(f"{eq.id}: module {eq.module_path} failed ({e})")
            continue
        obj = getattr(mod, eq.object_name, None)
        if not isinstance(obj, AtomicEquation) or obj.id != eq.id:
            problems.append(f"{eq.id}: {eq.module_path}.{eq.object_name} does not resolve")
    assert not problems, "Broken registry pointers:\n  " + "\n  ".join(problems)


def test_dependency_graph_ids_exist():
    """Every id referenced in graph/dependency-graph.json is a real equation."""
    path = os.path.join(ROOT, "graph", "dependency-graph.json")
    g = json.load(open(path))
    real = set(C.CANONICAL_EQUATIONS)
    refs = set(g["equations"])
    for e in g["equations"].values():
        refs |= set(e["depends_on"]) | set(e["used_by"])
    for v in g["topological_layers"].values():
        refs |= set(v)
    for ch in g["named_dependency_chains"].values():
        refs |= set(ch)
    refs |= set(g["cross_domain_equations"])
    missing = sorted(r for r in refs if r not in real)
    assert not missing, f"Graph references non-existent ids: {missing}"


def test_equation_counts_match_reality():
    """__init__.EQUATION_COUNTS matches the actual per-domain equation counts."""
    import scripts as pkg
    actual = defaultdict(int)
    for cid, e in C.CANONICAL_EQUATIONS.items():
        actual[e["domain"]] += 1
    mismatches = {d: (pkg.EQUATION_COUNTS.get(d), actual[d])
                  for d in actual if pkg.EQUATION_COUNTS.get(d) != actual[d]}
    assert not mismatches, f"EQUATION_COUNTS (declared vs actual): {mismatches}"
    assert pkg.TOTAL_EQUATIONS == sum(actual.values()), \
        f"TOTAL_EQUATIONS {pkg.TOTAL_EQUATIONS} != actual {sum(actual.values())}"


def test_compute_context_chains_dependencies():
    """ComputeContext resolves upstream dependencies AND feeds their outputs into
    the consumer's parameters (H3). Regression for 'computes the dependencies but
    still reports the consumer's parameters missing'."""
    for d in ("foundations", "cardiovascular"):
        importlib.import_module(f"scripts.{d}")
    from scripts.context import ComputeContext
    co = C.load("cardiac_output").compute(HR=70, SV=70)
    bsa = C.load("body_surface_area_dubois").compute(W=70, H=170)
    expected = C.load("cardiac_index").compute(CO=co, BSA=bsa)
    ctx = ComputeContext()
    ctx.set(HR=70, SV=70, W=70, H=170)  # only upstream inputs, not CO/BSA
    r = ctx.compute("cardiac_index")
    assert r.success, f"chaining failed; missing={[m.name for m in r.missing_params]}"
    assert abs(r.value - expected) < 1e-9, f"chained {r.value} != direct {expected}"


def test_compute_context_domain_restored_after_dependencies():
    """After resolving cross-domain dependencies, the context restores the
    consumer's own domain before normalizing its parameters (M6). Regression for
    the parent normalizing under the last dependency's domain."""
    for d in ("foundations", "cardiovascular", "renal"):
        importlib.import_module(f"scripts.{d}")
    from scripts.context import ComputeContext
    from scripts.index import get_global_index
    idx = get_global_index()
    eq = idx.get("gfr_from_nfp")  # renal, with a cross-domain dependency
    assert eq is not None and eq.category.value == "renal"
    assert any(idx.get(dep) and idx.get(dep).category.value != "renal"
               for dep in eq.depends_on), "test requires a cross-domain dependency"
    ctx = ComputeContext()
    ctx.compute("gfr_from_nfp")
    assert ctx._current_domain == "renal", \
        f"domain leaked across recursion: expected 'renal', got {ctx._current_domain!r}"


def test_flat_id_warnings_are_opt_in():
    """Flat-id migration warnings are off by default and gated behind the
    QP_WARN_FLAT_ID env var (M2), so a clean import doesn't emit ~249 stderr
    lines. The underlying check still works when explicitly enabled."""
    import scripts.base as B
    from scripts.base import validate_equation_id, EquationCategory
    assert B.WARN_ON_FLAT_ID is False, "flat-id warnings must be off by default"
    assert validate_equation_id("some_flat_id", EquationCategory.FOUNDATIONS,
                                warn_flat_ids=False) is None
    assert validate_equation_id("some_flat_id", EquationCategory.FOUNDATIONS,
                                warn_flat_ids=True) is not None


def test_clusters_json_ids_exist():
    """Every equation id referenced in graph/clusters.json is a real equation (M4)."""
    g = json.load(open(os.path.join(ROOT, "graph", "clusters.json")))
    real = set(C.CANONICAL_EQUATIONS)
    refs = {(e["id"] if isinstance(e, dict) else e)
            for cl in g["clusters"].values() for e in cl["equations"]}
    missing = sorted(r for r in refs if r not in real)
    assert not missing, f"clusters.json references non-existent ids: {missing}"


def test_parameter_range_roundtrip_is_type_stable():
    """Parameter.to_dict()->from_dict() preserves physiological_range as a tuple
    (L4). Guards the JSON round-trip against tuple->list drift."""
    from scripts.base import Parameter
    p = Parameter(name="r", description="radius", units="m", symbol="r",
                  physiological_range=(1e-6, 1e-2))
    p2 = Parameter(**p.to_dict())
    assert isinstance(p2.physiological_range, tuple), \
        f"round-trip produced {type(p2.physiological_range).__name__}, not tuple"
    assert p2.physiological_range == (1e-6, 1e-2)


def test_reference_ranges_are_sane():
    """Whole-body reference ranges (parameter_ranges.py) are internally consistent
    (L5): low < high and a units string for every entry."""
    from scripts.parameter_ranges import REFERENCE_RANGES, reference_range
    for q, (lo, hi, units, note) in REFERENCE_RANGES.items():
        assert lo < hi, f"{q}: low {lo} not < high {hi}"
        assert isinstance(units, str) and units, f"{q}: missing units"
    assert reference_range("Hb") == (12.0, 18.0)
    assert reference_range("not_a_quantity") is None


# --------------------------------------------------------------------------- #
# Plain runner (works without pytest)
# --------------------------------------------------------------------------- #
def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}\n      {e}")
            failed += 1
        except Exception as e:  # unexpected error
            print(f"ERROR {t.__name__}\n      {type(e).__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(tests)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run())

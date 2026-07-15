"""Regenerator for canonical_ids.py — the single source of truth for equation ids.

Run from the package parent directory:  python -m scripts._build_canonical_ids

It imports every domain submodule, collects each module-level AtomicEquation's
(id, module, object-name, domain), merges the hand-curated cross-domain and
alias tables below, and writes scripts/canonical_ids.py. Re-run whenever
equations are added, moved, or renamed so downstream artifacts (registry,
dependency graph, tests, SKILL.md) stay consistent by construction.
"""
import importlib, glob, os, sys, io, contextlib, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from scripts.base import AtomicEquation  # noqa: E402

# --- hand-curated: cross-domain equations (real ids, confirmed against code) ---
# id -> (display name, primary domain, [used-in domains])
CROSS_DOMAIN = {
    "nernst_equation":        ("Nernst Equation", "foundations",
                               ["membrane", "excitable", "nervous", "cardiovascular", "renal"]),
    "fick_first_law":         ("Fick's First Law of Diffusion", "foundations",
                               ["membrane", "respiratory", "renal", "cardiovascular"]),
    "poiseuille_flow":        ("Poiseuille's Law", "foundations",
                               ["cardiovascular", "respiratory", "renal"]),
    "michaelis_menten":       ("Michaelis-Menten Kinetics", "foundations",
                               ["membrane", "renal", "gastrointestinal", "endocrine"]),
    "laplace_sphere":         ("Law of Laplace (sphere)", "foundations",
                               ["cardiovascular", "respiratory", "gastrointestinal"]),
    "henderson_hasselbalch":  ("Henderson-Hasselbalch Equation", "respiratory",
                               ["renal", "gastrointestinal"]),
    "hill_equation":          ("Hill Equation", "respiratory",
                               ["excitable", "cardiovascular", "endocrine"]),
    "starling_filtration":    ("Starling Filtration", "cardiovascular",
                               ["renal", "gastrointestinal", "respiratory"]),
    "ghk_potential":          ("Goldman-Hodgkin-Katz Potential", "excitable",
                               ["membrane", "nervous", "cardiovascular"]),
    "goldman_flux":           ("Goldman-Hodgkin-Katz Flux", "membrane",
                               ["excitable"]),
    "alveolar_gas_equation":  ("Alveolar Gas Equation", "respiratory",
                               ["cardiovascular"]),
    "respiratory_oxygen_content": ("Oxygen Content", "respiratory",
                               ["cardiovascular"]),
    "cardiac_output_fick":    ("Fick Principle (Cardiac Output)", "cardiovascular",
                               ["respiratory"]),
}

# --- hand-curated: stale/wrong names used in older docs/graph/registry -> canonical id ---
ALIAS_TO_CANONICAL = {
    "fick_flux": "fick_first_law",
    "fick_diffusion": "fick_first_law",
    "ficks_law": "fick_first_law",
    "nernst_potential": "nernst_equation",
    "goldman_hodgkin_katz": "ghk_potential",
    "ghk": "ghk_potential",
    "laplace_law": "laplace_sphere",
    "starling_forces": "starling_filtration",
    "fick_principle_cardiac": "cardiac_output_fick",
    "hill": "hill_equation",
    "michaelis": "michaelis_menten",
    "lung_compliance": "compliance",
    "dead_space_ratio": "dead_space_bohr",
    "egfr": "ckd_epi_2021",
    "fena": "fe_na",
    "crcl": "cockcroft_gault",
    "creatinine_clearance": "cockcroft_gault",
    "apparent_vd": "apparent_volume_of_distribution",
    "driving_force": "driving_force_ion",
}


def scan():
    mods = [f[:-3].replace(os.sep, ".") for f in
            glob.glob(os.path.join("scripts", "**", "*.py"), recursive=True)
            if not os.path.basename(f).startswith(("__init__", "test_", "_"))
            and "extensions" not in f.split(os.sep)]
    eqs = {}
    with contextlib.redirect_stderr(io.StringIO()):
        for mod in sorted(mods):
            m = importlib.import_module(mod)
            for name, obj in vars(m).items():
                if isinstance(obj, AtomicEquation):
                    if obj.id in eqs:
                        raise SystemExit(f"DUPLICATE id at build time: {obj.id} "
                                         f"in {eqs[obj.id]['module']} and {mod}")
                    eqs[obj.id] = {
                        "module": mod,
                        "object": name,
                        "domain": mod.split(".")[1],
                        "cross_domain": obj.id in CROSS_DOMAIN,
                    }
    return eqs


def main():
    os.chdir(ROOT)
    eqs = scan()
    # validate the curated tables against reality
    for cid in CROSS_DOMAIN:
        if cid not in eqs:
            raise SystemExit(f"CROSS_DOMAIN id '{cid}' not found in code")
    for alias, target in ALIAS_TO_CANONICAL.items():
        if target not in eqs:
            raise SystemExit(f"ALIAS target '{target}' (for '{alias}') not found in code")

    lines = []
    lines.append('"""Canonical equation-id registry — the single source of truth.')
    lines.append("")
    lines.append("AUTO-GENERATED by scripts/_build_canonical_ids.py — do not edit by hand.")
    lines.append("Re-run the builder after adding, moving, or renaming equations.")
    lines.append("")
    lines.append("CANONICAL_EQUATIONS[id] = {module, object, domain, cross_domain}")
    lines.append("  module  : dotted import path of the defining module")
    lines.append("  object  : module-level name bound to the AtomicEquation (may differ from id)")
    lines.append("ALIAS_TO_CANONICAL maps stale/legacy names to the canonical id.")
    lines.append('"""')
    lines.append("")
    lines.append(f"TOTAL_EQUATIONS = {len(eqs)}")
    lines.append("")
    lines.append("CANONICAL_EQUATIONS = {")
    for cid in sorted(eqs):
        e = eqs[cid]
        lines.append(f"    {cid!r}: {{'module': {e['module']!r}, 'object': {e['object']!r}, "
                     f"'domain': {e['domain']!r}, 'cross_domain': {e['cross_domain']!r}}},")
    lines.append("}")
    lines.append("")
    lines.append("# name used in older docs/graph/registry -> canonical id")
    lines.append("ALIAS_TO_CANONICAL = {")
    for a in sorted(ALIAS_TO_CANONICAL):
        lines.append(f"    {a!r}: {ALIAS_TO_CANONICAL[a]!r},")
    lines.append("}")
    lines.append("")
    lines.append("# canonical id -> (display name, primary domain, [used-in domains])")
    lines.append("CROSS_DOMAIN = {")
    for cid in CROSS_DOMAIN:
        name, primary, used = CROSS_DOMAIN[cid]
        lines.append(f"    {cid!r}: ({name!r}, {primary!r}, {used!r}),")
    lines.append("}")
    lines.append("")
    lines.append(RESOLVERS)

    with open(os.path.join("scripts", "canonical_ids.py"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote scripts/canonical_ids.py  ({len(eqs)} equations, "
          f"{len(CROSS_DOMAIN)} cross-domain, {len(ALIAS_TO_CANONICAL)} aliases)")


RESOLVERS = '''

def resolve(name):
    """Return the canonical id for a name (identity if already canonical,
    else via alias table). Returns None if unknown."""
    if name in CANONICAL_EQUATIONS:
        return name
    return ALIAS_TO_CANONICAL.get(name)


def import_path(name):
    """Return (module, object) for a name (canonical or alias), or None."""
    cid = resolve(name)
    if cid is None:
        return None
    e = CANONICAL_EQUATIONS[cid]
    return e["module"], e["object"]


def load(name):
    """Import and return the AtomicEquation object for a name, or raise KeyError
    (with a nearest-id suggestion)."""
    ip = import_path(name)
    if ip is None:
        import difflib
        pool = list(CANONICAL_EQUATIONS) + list(ALIAS_TO_CANONICAL)
        near = difflib.get_close_matches(name, pool, n=3, cutoff=0.6)
        hint = f" Did you mean: {', '.join(near)}?" if near else ""
        raise KeyError(f"unknown equation id/alias: {name!r}.{hint}")
    import importlib
    module, obj = ip
    return getattr(importlib.import_module(module), obj)
'''

if __name__ == "__main__":
    main()

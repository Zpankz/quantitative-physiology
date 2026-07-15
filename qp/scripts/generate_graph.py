"""Regenerator for graph/dependency-graph.json.

Run from the package parent directory:  python -m scripts.generate_graph

Builds the dependency graph directly from the code: it imports every domain
submodule, reads each equation's `depends_on` edges (resolving any legacy
aliases through canonical_ids), computes reverse (`used_by`) edges and
topological layers, and attaches the curated cross-domain set and named chains
(every id in which is validated to exist). Replaces the previously hand-authored
graph, which referenced ids that no longer existed.
"""
import importlib, glob, os, sys, io, contextlib, json
from collections import defaultdict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from scripts.base import AtomicEquation                      # noqa: E402
from scripts import canonical_ids as C                       # noqa: E402

# Curated, human-meaningful dependency chains (validated against real ids below).
NAMED_CHAINS = {
    "membrane_to_action_potential": [
        "nernst_equation", "ghk_potential", "hh_membrane_current", "hh_sodium_current",
    ],
    "oxygen_cascade": [
        "hill_equation", "respiratory_oxygen_content", "tissue_oxygen_delivery",
        "oxygen_consumption_fick",
    ],
    "renal_clearance": [
        "renal_plasma_flow", "filtration_fraction", "gfr_from_nfp", "clearance",
        "fractional_excretion",
    ],
    "hpa_axis": [
        "hpa_crh_dynamics", "hpa_acth_dynamics", "hpa_cortisol_dynamics", "feedback_gain",
    ],
}


def collect():
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
                    eqs[obj.id] = {
                        "domain": mod.split(".")[1],
                        "module": mod,
                        "object": name,
                        "depends_on_raw": list(obj.depends_on),
                    }
    return eqs


def main():
    os.chdir(ROOT)
    eqs = collect()

    # resolve depends_on through the canonical alias map; record any unresolved
    unresolved = []
    for eid, e in eqs.items():
        resolved = []
        for dep in e["depends_on_raw"]:
            cid = C.resolve(dep)
            if cid is None or cid not in eqs:
                unresolved.append((eid, dep))
            else:
                resolved.append(cid)
        e["depends_on"] = sorted(set(resolved))
    if unresolved:
        raise SystemExit(f"Unresolved depends_on edges (fix before generating): {unresolved}")

    # reverse edges
    used_by = defaultdict(set)
    for eid, e in eqs.items():
        for dep in e["depends_on"]:
            used_by[dep].add(eid)

    # topological layers (Kahn); equations with no deps are layer 0
    indeg = {eid: len(e["depends_on"]) for eid, e in eqs.items()}
    layer_of = {}
    frontier = deque(sorted(eid for eid, d in indeg.items() if d == 0))
    layer = 0
    remaining = dict(indeg)
    while frontier:
        nxt = deque()
        for eid in frontier:
            layer_of[eid] = layer
            for child in sorted(used_by.get(eid, [])):
                remaining[child] -= 1
                if remaining[child] == 0:
                    nxt.append(child)
        frontier = deque(sorted(nxt))
        layer += 1
    # any leftover (cycles) -> mark -1
    for eid in eqs:
        layer_of.setdefault(eid, -1)
    cycles = [eid for eid, l in layer_of.items() if l == -1]

    # validate curated chains against real ids
    for cname, ids in NAMED_CHAINS.items():
        for i in ids:
            if i not in eqs:
                raise SystemExit(f"NAMED_CHAINS['{cname}'] references missing id '{i}'")

    layers = defaultdict(list)
    for eid, l in layer_of.items():
        if l >= 0:
            layers[l].append(eid)

    graph = {
        "metadata": {
            "generated_by": "scripts/generate_graph.py",
            "do_not_edit_by_hand": True,
            "total_equations": len(eqs),
            "total_dependency_edges": sum(len(e["depends_on"]) for e in eqs.values()),
            "num_topological_layers": max([l for l in layer_of.values() if l >= 0], default=-1) + 1,
            "cycles_detected": cycles,
        },
        "equations": {
            eid: {
                "domain": e["domain"],
                "module": e["module"],
                "object": e["object"],
                "depends_on": e["depends_on"],
                "used_by": sorted(used_by.get(eid, [])),
                "layer": layer_of[eid],
            } for eid, e in sorted(eqs.items())
        },
        "cross_domain_equations": {
            cid: {
                "name": name,
                "primary_domain": primary,
                "used_in_domains": used,
                "module": C.CANONICAL_EQUATIONS[cid]["module"],
                "object": C.CANONICAL_EQUATIONS[cid]["object"],
            } for cid, (name, primary, used) in C.CROSS_DOMAIN.items()
        },
        "topological_layers": {str(k): sorted(v) for k, v in sorted(layers.items())},
        "named_dependency_chains": NAMED_CHAINS,
    }

    out = os.path.join("graph", "dependency-graph.json")
    with open(out, "w") as f:
        json.dump(graph, f, indent=2)
    print(f"wrote {out}")
    print(f"  equations={len(eqs)} edges={graph['metadata']['total_dependency_edges']} "
          f"layers={graph['metadata']['num_topological_layers']} cycles={len(cycles)}")


if __name__ == "__main__":
    main()

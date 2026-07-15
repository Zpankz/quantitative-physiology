"""Queryable equation graph for the qp library — interconnections, path
traversal, and dimensional-analysis reasoning.

Builds an in-memory graph database over the 321 ``AtomicEquation`` objects with
three layers of connectivity, all queryable without a server or third-party
dependency:

1. **Dependency layer** — the explicit ``depends_on`` DAG (which equation feeds
   which), with forward/backward traversal and path finding.
2. **Symbol layer** — producer→quantity→consumer links: an equation *produces* a
   named quantity (``produces``) that another *consumes* as a parameter.
3. **Dimensional layer** — every parameter and every equation *result* is reduced
   to an SI dimension vector (:mod:`scripts.dimensions`). Equations are linked
   when one's **output dimension** matches another's **input-parameter
   dimension**, so interconnections and candidate compositions can be discovered
   by *dimension* — independent of naming — and explored combinatorially.

Typical use::

    from scripts.eqgraph import build_graph
    g = build_graph()
    g.output_dim("mean_arterial_pressure").name()      # 'pressure'
    g.dimensional_diff("stroke_volume", "cardiac_output")  # Dim you must apply
    g.feeds("nernst_equation")                         # eqs it can feed (by dim)
    g.compose_paths(start="mmHg", goal="volumetric_flow", max_depth=3)
"""
from __future__ import annotations
from collections import defaultdict, deque
from typing import Dict, List, Optional, Tuple

from scripts.dimensions import Dim, parse
from scripts import canonical_ids as C


class EquationGraph:
    def __init__(self, equations: Dict[str, "object"]):
        self.eqs = equations
        self.ids = list(equations)
        # precompute dimensions
        self._out: Dict[str, Dim] = {i: parse(getattr(e, "output_units", None))
                                     for i, e in equations.items()}
        self._pdims: Dict[str, Dict[str, Dim]] = {
            i: {p.name: parse(p.units) for p in e.parameters}
            for i, e in equations.items()}
        # dependency adjacency
        self._dep: Dict[str, List[str]] = {i: list(getattr(e, "depends_on", []) or [])
                                           for i, e in equations.items()}
        self._rdep: Dict[str, List[str]] = defaultdict(list)
        for i, deps in self._dep.items():
            for d in deps:
                self._rdep[d].append(i)
        # symbol layer: produced symbol -> producers; param-name -> consumers
        self._producers: Dict[str, List[str]] = defaultdict(list)
        self._consumers: Dict[str, List[str]] = defaultdict(list)
        for i, e in equations.items():
            sym = getattr(e, "produces", None)
            if sym:
                self._producers[sym].append(i)
            for p in e.parameters:
                self._consumers[p.name].append(i)

    # ------------------------------------------------------------------ dims
    def output_dim(self, eid: str) -> Dim:
        return self._out.get(eid, Dim.UNKNOWN)

    def param_dims(self, eid: str) -> Dict[str, Dim]:
        return self._pdims.get(eid, {})

    def dimensional_diff(self, a: str, b: str) -> Optional[Dim]:
        """Dimension you must MULTIPLY a's output by to reach b's output (b/a).

        ``.is_dimensionless`` iff the two equations produce the same dimension.
        None if either output dimension is undeclared/opaque.
        """
        return self.output_dim(a).diff(self.output_dim(b))

    def by_output_dimension(self, dim: Dim) -> List[str]:
        return [i for i in self.ids if self._out[i].same_dimension(dim)]

    def by_param_dimension(self, dim: Dim) -> List[Tuple[str, str]]:
        return [(i, name) for i in self.ids
                for name, d in self._pdims[i].items() if d.same_dimension(dim)]

    # ------------------------------------------------- dependency traversal
    def depends_on(self, eid: str) -> List[str]:
        return list(self._dep.get(eid, []))

    def dependents(self, eid: str) -> List[str]:
        return list(self._rdep.get(eid, []))

    def dependency_path(self, src: str, dst: str) -> Optional[List[str]]:
        """A path src -> ... -> dst following depends_on edges (BFS), or None."""
        if src == dst:
            return [src]
        seen = {src}
        q = deque([(src, [src])])
        while q:
            node, path = q.popleft()
            for nxt in self._dep.get(node, []):
                if nxt == dst:
                    return path + [nxt]
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, path + [nxt]))
        return None

    # ----------------------------------------------------------- symbol layer
    def producers_of(self, symbol: str) -> List[str]:
        return list(self._producers.get(symbol, []))

    def consumers_of(self, symbol: str) -> List[str]:
        return list(self._consumers.get(symbol, []))

    # -------------------------------------------- dimensional composition
    def feeds(self, eid: str) -> List[Tuple[str, str]]:
        """(consumer_id, param) pairs this equation's OUTPUT can dimensionally
        supply — i.e. eid's output dimension matches that parameter's dimension.
        The combinatorial 'what can this feed?' query."""
        od = self.output_dim(eid)
        if not od.known:
            return []
        out = []
        for i in self.ids:
            if i == eid:
                continue
            for name, d in self._pdims[i].items():
                if d.same_dimension(od):
                    out.append((i, name))
        return out

    def fed_by(self, eid: str) -> List[str]:
        """Equation ids whose output dimension matches ANY parameter of eid —
        the 'what can supply my inputs?' query."""
        want = {tuple(d.v) for d in self._pdims[eid].values() if d.known}
        return [i for i in self.ids
                if i != eid and self._out[i].known and tuple(self._out[i].v) in want]

    def dimensional_bridges(self) -> List[Tuple[str, str, str]]:
        """Every (producer, consumer, param) where producer's output dimension
        equals a consumer parameter's dimension. The full combinatorial
        interaction set over the library (excludes dimensionless matches, which
        are too permissive to be informative)."""
        bridges = []
        for a in self.ids:
            od = self._out[a]
            if not od.known or od.is_dimensionless:
                continue
            for b in self.ids:
                if a == b:
                    continue
                for name, d in self._pdims[b].items():
                    if d.same_dimension(od):
                        bridges.append((a, b, name))
        return bridges

    # ---------------------------------------------- dimensional coupling algebra
    @staticmethod
    def _is_named(nm: str) -> bool:
        """True for a physical-name dimension ('pressure', 'dimensionless'), False
        for a raw base-vector signature ('M/T^3', 'L·T^3/M')."""
        import re as _re
        return bool(_re.fullmatch(r"[a-z][a-z0-9_]*", nm))

    def dimensional_triples(self, max_examples: int = 2,
                            named_only: bool = True) -> List[dict]:
        """Realised dimensional triples ``(A, B, C)`` where ``dim(A)·dim(B) == dim(C)``.

        This is the multiplicative closure the corpus already obeys, made explicit:
        because flow × resistance = pressure, *any two* of {flow, resistance,
        pressure} determine the third — pressure is the "edge" coupling flow and
        resistance. Also captures reciprocal pairs whose product is **dimensionless**
        (e.g. resistance × conductance), so a dimensionless quantity is linked to the
        dimensional factors that cancel to produce it rather than being dropped.

        Iterates the distinct *realised output dimensions* (dozens), not the 367
        equations, so the result is a compact algebra; each factor carries a few
        example equation ids. `dimensional_bridges` (same-dimension producer→consumer)
        is intentionally left untouched — this is the composition relation beside it.
        """
        dims: Dict[tuple, Tuple[Dim, List[str]]] = {}
        for i in self.ids:
            d = self._out[i]
            if not d.known or d.is_dimensionless:
                continue
            dims.setdefault(tuple(d.v), (d, []))[1].append(i)
        keys = list(dims)
        triples, seen = [], set()
        for x in range(len(keys)):
            for y in range(x, len(keys)):
                dA, exA = dims[keys[x]]
                dB, exB = dims[keys[y]]
                C = dA * dB
                if not C.known:
                    continue
                if C.is_dimensionless:
                    cname, cex = "dimensionless", None
                elif tuple(C.v) in dims:
                    cname, cex = C.name(), dims[tuple(C.v)][1][0]
                else:
                    continue
                if named_only and not (self._is_named(dA.name())
                                       and self._is_named(dB.name())
                                       and self._is_named(cname)):
                    continue
                key = (keys[x], keys[y])
                if key in seen:
                    continue
                seen.add(key)
                triples.append({
                    "a": dA.name(), "b": dB.name(), "product": cname,
                    "example_a": exA[:max_examples], "example_b": exB[:max_examples],
                    "example_product": cex,
                })
        return triples

    def cancellation(self, eid: str, snap: int = 2) -> Optional[dict]:
        """How an equation's OUTPUT dimension is built from its PARAMETER dimensions:
        the multiplicative exponents ``e_i`` with ``∏ dim(param_i)**e_i == output``.

        For a dimensionless output (Reynolds, Womersley, time constants, ratios) this
        is the *cancellation relation* that makes the number dimensionless — e.g.
        Reynolds returns ``{rho: 1, v: 1, d: 1, eta: -1}``, linking the pure number to
        the four dimensional quantities whose product cancels. Rational/half-integer
        exponents are recovered (Womersley). Returns ``None`` if the parameters'
        dimensions cannot reconstruct the output (opaque/undeclared units).

        Delegates to :func:`scripts.dimform.cancellation`; the same value is cached
        on ``AtomicEquation.dimensional_form``.
        """
        from scripts.dimform import cancellation
        e = self.eqs[eid]
        return cancellation({p.name: p.units for p in e.parameters},
                            getattr(e, "output_units", None), snap=snap)

    def dimensional_inference(self, have, max_examples: int = 3) -> List[dict]:
        """REASONING TOOL — the 'any two give the third' move, done soundly.

        Given the quantities you hold (equation ids, `Dim`s, or unit strings),
        enumerate every new quantity reachable by composing a *pair* of them
        (product or quotient), restricted to dimensions that a real equation in the
        library actually produces — and name that equation. So "I have a flow and a
        resistance" yields "a pressure is reachable, realised by
        `mean_arterial_pressure`" — it tells you *which equation to apply*.

        Dimensional reachability is necessary but NOT sufficient: the match says a
        relation of that dimension *can* exist; the named equation carries the real
        coefficient and meaning. This deliberately returns hypotheses-to-apply, not
        computed values — so it never fabricates a number the way baking the triples
        into `propagate` would (pressure = flow × resistance is dimensionally true
        but MAP = CO × SVR has a specific scale; only the equation knows it).
        """
        held = []
        for h in have:
            if isinstance(h, str) and h in self.eqs:
                d, lbl = self._out[h], h
            elif isinstance(h, Dim):
                d, lbl = h, h.name()
            else:
                d, lbl = parse(str(h)), str(h)
            if d.known and not d.is_dimensionless:
                held.append((lbl, d))
        realised: Dict[tuple, List[str]] = {}
        for i in self.ids:
            d = self._out[i]
            if d.known and not d.is_dimensionless:
                realised.setdefault(tuple(d.v), []).append(i)
        out, seen = [], set()
        for x in range(len(held)):
            for y in range(len(held)):
                if x == y:
                    continue
                (la, da), (lb, db) = held[x], held[y]
                for op, C in (("*", da * db), ("/", da / db)):
                    if not C.known or C.is_dimensionless:
                        continue
                    key = tuple(C.v)
                    if key not in realised:
                        continue
                    if op == "*" and (lb, "*", la, key) in seen:
                        continue
                    seen.add((la, op, lb, key))
                    # prefer an equation that actually COMPOSES these two inputs
                    # (a parameter of each held dimension) over any producer of C
                    realisers = [p for p in realised[key]
                                 if any(pd.same_dimension(da) for pd in self._pdims[p].values())
                                 and any(pd.same_dimension(db) for pd in self._pdims[p].values())]
                    via = (realisers or realised[key])[:max_examples]
                    out.append({"from": (la, lb), "op": op,
                                "reachable": C.name(),
                                "via_equations": via,
                                "direct_realiser": bool(realisers)})
        return out

    def compose_paths(self, start: str, goal: str,
                      max_depth: int = 3, limit: int = 200) -> List[List[str]]:
        """Permutational search for equation chains that transform a START
        dimension into a GOAL dimension.

        ``start``/``goal`` may be a unit string ("mmHg"), a dimension name
        ("pressure"), or a :class:`Dim`. Returns chains [eq1, eq2, ...] where
        eq1 accepts a parameter of the start dimension, each equation's output
        dimension feeds the next equation's parameter, and the last equation's
        output has the goal dimension. Depth- and count-bounded to stay finite.
        """
        sdim = _as_dim(start)
        gdim = _as_dim(goal)
        if not (sdim.known and gdim.known):
            return []
        # seed equations: those with a parameter of the start dimension
        seeds = [i for i, _ in self.by_param_dimension(sdim)]
        results: List[List[str]] = []
        stack: List[Tuple[str, List[str]]] = [(s, [s]) for s in dict.fromkeys(seeds)]
        while stack and len(results) < limit:
            node, path = stack.pop()
            od = self._out[node]
            if od.known and od.same_dimension(gdim):
                results.append(path)
                continue
            if len(path) >= max_depth or not od.known:
                continue
            for nxt, _ in self.feeds(node):
                if nxt not in path:
                    stack.append((nxt, path + [nxt]))
        return results

    # ------------------------------------------------ integrative execution
    def propagate(self, seeds: Dict[str, float], max_rounds: int = 8) -> Dict:
        """Forward-chaining integrative simulation: seed base quantities and
        propagate values through the whole graph, computing every equation whose
        inputs become available (directly or from earlier results), round by
        round, until a fixpoint. Each result is fed back under the equation's
        ``produces`` symbol (or id) so downstream equations can consume it —
        alias resolution is handled by ComputeContext.

        Returns ``{fired, store, rounds, unfired}`` where ``fired`` maps each
        computed equation id to its value and ``store`` is the full quantity
        table after propagation. This is how the library *simulates* an
        integrated physiological state from a small set of measured inputs
        (e.g. seed HR/SV/EDV/Hb/PO2 -> obtain CO, EF, CI, O2 content/delivery).
        """
        from scripts.context import ComputeContext
        ctx = ComputeContext()
        ctx.set(**seeds)
        store = dict(seeds)
        fired: Dict[str, float] = {}
        rounds = 0
        for rnd in range(max_rounds):
            rounds = rnd + 1
            new = 0
            for eid in self.ids:
                if eid in fired:
                    continue
                try:
                    r = ctx.compute(eid)
                except Exception:
                    continue
                val = getattr(r, "value", None)
                if getattr(r, "success", False) and val is not None:
                    fired[eid] = val
                    sym = getattr(self.eqs[eid], "produces", None) or eid
                    ctx.set(**{sym: val})
                    store.setdefault(sym, val)
                    new += 1
            if new == 0:
                break
        return {"fired": fired, "store": store, "rounds": rounds,
                "unfired": [i for i in self.ids if i not in fired]}

    # ------------------------------------------------------------- export
    def to_dict(self) -> Dict:
        return {
            "nodes": {i: {"output_dim": self._out[i].signature(),
                          "output_dim_name": self._out[i].name(),
                          "produces": getattr(self.eqs[i], "produces", None),
                          "params": {n: d.signature() for n, d in self._pdims[i].items()}}
                      for i in self.ids},
            "depends_on": {i: self._dep[i] for i in self.ids if self._dep[i]},
        }

    def stats(self) -> Dict:
        declared = sum(1 for d in self._out.values() if d.known)
        return {
            "equations": len(self.ids),
            "output_dims_declared": declared,
            "dependency_edges": sum(len(v) for v in self._dep.values()),
            "dimensional_bridges": len(self.dimensional_bridges()),
        }


def _as_dim(x) -> Dim:
    if isinstance(x, Dim):
        return x
    d = parse(x)
    if d.known:
        return d
    # allow a derived-dimension NAME ("pressure", "volumetric_flow")
    from scripts.dimensions import _DERIVED_NAMES
    for vec, nm in _DERIVED_NAMES.items():
        if nm == x:
            return Dim(vec)
    return Dim.UNKNOWN


def build_graph() -> EquationGraph:
    """Load every canonical equation and build the graph."""
    for d in ("foundations", "membrane", "excitable", "nervous", "cardiovascular",
              "respiratory", "renal", "gastrointestinal", "endocrine"):
        __import__(f"scripts.{d}")
    eqs = {cid: C.load(cid) for cid in C.CANONICAL_EQUATIONS}
    return EquationGraph(eqs)


if __name__ == "__main__":  # smoke demo
    g = build_graph()
    print("stats:", g.stats())
    print("MAP output dim:", g.output_dim("mean_arterial_pressure").name())

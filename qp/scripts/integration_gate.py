"""Fast integration sensor: the acceptance-gate invariants that the systems-
integration pass can affect (cycles, topo order, dep-edge validity), plus
propagate() coverage as the control-loop sensor the AoT systems layer flagged
as missing. Run before/after every wiring batch.

    python -m scripts.integration_gate

Exits 0 iff every invariant holds. Prints coverage so a batch that lowers it
(or breaks a cycle) is caught immediately.
"""
import sys
from scripts.canonical_ids import CANONICAL_EQUATIONS
from scripts.eqgraph import build_graph

# Rich clinical seed — the standard propagate probe (kept identical run to run
# so coverage numbers are comparable across batches).
SEED = dict(HR=80, SV=65, EDV=120, ESV=55, W=70, H=175, Hb=14,
            S_O2=0.97, P_O2=95, P_50=26.8, n=2.7, SBP=125, DBP=78)


def run():
    g = build_graph()
    E = g.eqs
    ids = set(E)
    fails = []

    # 3. every depends_on references a real id
    for i, e in E.items():
        for d in (getattr(e, "depends_on", None) or []):
            if d not in ids:
                fails.append(f"dangling depends_on {i} -> {d}")

    # 5. no dependency cycles
    cycles = detect_cycles(E)
    if cycles:
        fails.append(f"cycles: {cycles[:3]}")

    # 4. a valid topological order exists over ALL equations
    order = toposort(E)
    if order is None:
        fails.append("no valid topological order (cycle)")
    elif len(order) != len(E):
        fails.append(f"topo order length {len(order)} != {len(E)}")

    # sensor: propagate coverage
    res = g.propagate(SEED)
    cov = len(res["fired"])
    stats = g.stats()

    print(f"equations         {len(E)}")
    print(f"dependency_edges  {stats['dependency_edges']}")
    print(f"cross_domain      {count_cross_domain(E)}")
    print(f"isolated          {count_isolated(E)}")
    print(f"propagate_fired   {cov}  ({round(100*cov/len(E))}%)")
    print(f"cycles            {len(cycles)}")
    if fails:
        print("\nFAIL:")
        for f in fails:
            print("  -", f)
        return 1
    print("\nOK  (0 cycles, valid topo order, all edges real)")
    return 0


def _edges(E):
    for i, e in E.items():
        for d in (getattr(e, "depends_on", None) or []):
            if d in E:
                yield d, i  # producer -> consumer


def detect_cycles(E):
    from collections import defaultdict
    adj = defaultdict(list)
    for a, b in _edges(E):
        adj[a].append(b)
    WHITE, GREY, BLACK = 0, 1, 2
    color = {i: WHITE for i in E}
    found = []

    def dfs(u, stack):
        color[u] = GREY
        for v in adj[u]:
            if color[v] == GREY:
                found.append(stack[stack.index(v):] + [v])
            elif color[v] == WHITE:
                dfs(v, stack + [v])
        color[u] = BLACK

    for i in E:
        if color[i] == WHITE:
            dfs(i, [i])
    return found


def toposort(E):
    from collections import defaultdict, deque
    adj = defaultdict(list)
    indeg = {i: 0 for i in E}
    for a, b in _edges(E):
        adj[a].append(b)
        indeg[b] += 1
    q = deque([i for i in E if indeg[i] == 0])
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == len(E) else None


def count_cross_domain(E):
    dom = {i: CANONICAL_EQUATIONS.get(i, {}).get("domain", "?") for i in E}
    return sum(1 for a, b in _edges(E) if dom[a] != dom[b])


def count_isolated(E):
    from collections import defaultdict
    dependents = defaultdict(set)
    for a, b in _edges(E):
        dependents[a].add(b)
    return sum(1 for i, e in E.items()
               if not (getattr(e, "depends_on", None)) and not dependents[i])


if __name__ == "__main__":
    sys.exit(run())

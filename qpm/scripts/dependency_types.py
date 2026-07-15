"""AND/OR dependency typing — the distinction the flat `depends_on` list cannot make.

`depends_on` is a flat list, so it cannot say whether two entries are *jointly
required* (AND — you need both) or *substitutable alternatives* (OR — you need the
quantity, and any one producer supplies it). The audit named the concrete failure:
an equation that needs cardiac output lists all three CO methods, reading as "needs
all three" when it means "needs CO, by any one method".

WHAT THE OR RELATION CLAIMS (and what it does not). OR-typing is a **structural
computability** statement, not a clinical-interchangeability one: quantity Q has
≥2 producers in the graph, so a consumer that needs Q can be *satisfied in the
compute graph* by any one of them. It does NOT assert the producers are clinically
equivalent — they differ in population, assumptions, timing and error structure,
which is exactly why each member is typed by `kind` below.

GROUNDING (structural, not circular). An **OR-group** is established by a fact
already in the registry: ≥2 equations declare the *same* `produces` symbol. That
shared output IS the alternative relationship. This is a graph-semantics reading of
the corpus's own declared outputs (each already anchored per equation); it asserts
no new physiological value, introduces no coefficient, so it needs no external
anchor and is not a self-test — reading which equations target Q is not the same
kind of claim as asserting Q's value. (The audit itself named blood_ vs
respiratory_oxygen_content as alternatives on exactly this basis.)

    AXIOM (for future contributors): the no-anchor exemption applies ONLY to
    structural reads of already-anchored corpus fields (which equations declare Q,
    how their formulas are shaped). Any NEW numeric value, coefficient, or
    reference range added here still needs an independent external anchor. Do not
    extend the "structural ⇒ no anchor" reasoning to physiological values.

`definitional` covers a quantity's defining relation AND its exact algebraic
rearrangements (MAP≡CO·SVR+CVP is the rearrangement of SVR≡(MAP−CVP)/CO); the
member note records when a definitional producer is an inverse whose independence
is conditional.

The alternatives are NOT all the same kind, and the module says so honestly — each
member carries a `kind`:
  * ``definitional`` — the defining relation for the quantity (CO ≡ HR·SV;
    MAP ≡ CO·SVR+CVP; CaO₂ ≡ 1.34·Hb·S+0.003·P).
  * ``approximation`` — a bedside estimate that agrees with the definition only
    over a limited range (MAP ≈ DBP + PP/3, valid near normal heart rate).
  * ``measurement`` — an independent measurement method with its own error
    structure (Fick, indicator dilution for CO).
  * ``model`` — an alternative kinetic model of the quantity (α-function vs
    double-exponential for the synaptic conductance g_syn).

`kind` is drawn from the closed set `KINDS`; a new producer must be assigned one
explicitly (verify() rejects an unknown kind). Two honest caveats surfaced by the
council and confirmed in source: (a) CaO₂'s two producers are the *identical*
definitional relation duplicated across the cardiovascular and respiratory domains
— an alias-grade OR-group, not two distinct methods; (b) MAP's `map_from_flow`
(CO·SVR+CVP) is the algebraic inverse of the SVR definition ((MAP−CVP)/CO), so it
is an independent MAP *source* only when SVR is known independently (measured), not
back-computed from MAP — weaker in practice than the cuff estimate. Both notes are
carried on the members so the typing does not overstate independence.

`agreement()` reports how close the numeric-comparable members sit at a *single*
normal operating point — explicitly a sanity diagnostic **with a caveat**, never
the grounding: agreement at one point does not prove substitutability across the
domain, and an approximation is not the identity.

No equation is modified; this is an additive relational layer beside the DAG,
exactly like `scripts.primitives` and `scripts.feedback`.
"""
from __future__ import annotations
from collections import defaultdict
from typing import Dict, List

KINDS = {"definitional", "approximation", "measurement", "model"}

# quantity symbol -> group spec. Each member declares its `kind` and a one-line
# `note`. `agreement` (optional) gives matched inputs for a single normal operating
# point and the honest caveat — used by agreement(), never by verify().
OR_GROUPS: Dict[str, dict] = {
    "CaO2": dict(
        produces="CaO2", units="mL/dL",
        members={
            "blood_oxygen_content":       dict(kind="definitional", note="1.34·Hb·S_O2 + 0.003·P_O2 (cardiovascular domain)"),
            "respiratory_oxygen_content": dict(kind="definitional", note="identical relation duplicated in the respiratory domain — an ALIAS, not a distinct method"),
        },
        alias=True,  # the two producers are the same relation in two domains
        agreement=dict(
            bind={"blood_oxygen_content": dict(Hb=15, S_O2=0.97, P_O2=100),
                  "respiratory_oxygen_content": dict(Hb=15, SO2=0.97, PO2=100)},
            caveat="alias-grade: both encode the identical definitional relation, so they agree exactly at every input — this is a cross-domain duplicate, not two distinct methods"),
        intuition="arterial O₂ content: the one definitional relation, duplicated across cardiovascular and respiratory domains"),
    "CO": dict(
        produces="CO", units="L/min",
        members={
            "cardiac_output":                    dict(kind="definitional", note="CO ≡ HR·SV, the definition"),
            "cardiac_output_fick":               dict(kind="measurement",  note="Fick: CO = VO₂/(CaO₂−CvO₂)"),
            "indicator_dilution_cardiac_output": dict(kind="measurement",  note="Stewart–Hamilton indicator dilution"),
        },
        agreement=dict(
            bind={"cardiac_output": dict(HR=80, SV=62.5),
                  "cardiac_output_fick": dict(VO2=250, C_aO2=20, C_vO2=15),
                  "indicator_dilution_cardiac_output": dict(m=5, area_under_curve=1)},
            caveat="the definition and the two measurement methods target one CO; they coincide only for a mutually consistent patient state and carry different error structures"),
        intuition="one cardiac output; HR·SV defines it, Fick and indicator dilution measure it"),
    "MAP": dict(
        produces="MAP", units="mmHg",
        members={
            "mean_arterial_pressure": dict(kind="approximation", note="MAP ≈ DBP + PP/3, bedside estimate valid near normal HR (~60–100, no severe aortic valve disease)"),
            "map_from_flow":          dict(kind="definitional",  note="MAP ≡ CO·SVR + CVP; the algebraic inverse of the SVR definition, so an independent MAP source only when SVR is measured, not back-computed from MAP"),
        },
        agreement=dict(
            bind={"mean_arterial_pressure": dict(SBP=120, DBP=80),
                  "map_from_flow": dict(CO=5, SVR_wood=16.6667, CVP=10)},
            caveat="DBP+PP/3 is an APPROXIMATION to the identity CO·SVR+CVP; they agree only near a normal operating point, NOT across the domain"),
        intuition="mean arterial pressure: the bedside approximation and the hemodynamic identity, distinct in kind"),
    "g_syn": dict(
        produces="g_syn", units="nS",
        members={
            "alpha_function":             dict(kind="model", note="α-function waveform; peaks at g_max at t=τ"),
            "double_exponential_synapse": dict(kind="model", note="rise/decay double-exponential waveform"),
        },
        # no `agreement`: the two models have different time-courses and are NOT
        # numerically equal — substitutable in role, not in value.
        intuition="synaptic conductance g(t): two alternative kinetic models of the same quantity"),
}

_MEMBER_TO_GROUP = {m: q for q, spec in OR_GROUPS.items() for m in spec["members"]}


def _load_registry():
    import scripts.foundations, scripts.membrane, scripts.excitable, scripts.nervous  # noqa
    import scripts.cardiovascular, scripts.respiratory, scripts.renal  # noqa
    import scripts.gastrointestinal, scripts.endocrine  # noqa
    from scripts.index import get_global_index
    return get_global_index()


def _eq(eid):
    _load_registry()
    from scripts.index import get_equation
    return get_equation(eid)


def verify(q: str) -> List[str]:
    """Prove an OR-group is structurally grounded, from the registry itself.

    Asserts: ≥2 members; every member resolves in the live registry; every member
    declares the group's `produces` symbol (this shared symbol IS the alternative
    relationship); every member's `kind` is a known kind. Returns the sorted list of
    kinds present. Raises AssertionError on any failure — so a fabricated member id,
    or a member that does not actually produce the group's quantity, is caught.
    """
    spec = OR_GROUPS[q]
    members = spec["members"]
    assert len(members) >= 2, f"{q}: an OR-group needs ≥2 members"
    for eid, m in members.items():
        e = _eq(eid)
        assert e is not None, f"{q}: member {eid} not in registry"
        got = e.produces or e.id
        assert got == spec["produces"], f"{q}: {eid} produces {got!r}, not {spec['produces']!r}"
        assert m["kind"] in KINDS, f"{q}: {eid} has unknown kind {m['kind']!r}"
    return sorted({m["kind"] for m in members.values()})


def agreement(q: str) -> dict | None:
    """Sanity diagnostic (NOT grounding): where members are numerically comparable,
    the spread at ONE normal operating point, plus the honest caveat. None for
    groups with no comparable operating point (e.g. the g_syn models)."""
    spec = OR_GROUPS[q]
    ag = spec.get("agreement")
    if ag is None:
        return None
    vals = {eid: _eq(eid).compute(**kw) for eid, kw in ag["bind"].items()}  # type: ignore[union-attr]
    lo, hi = min(vals.values()), max(vals.values())
    spread_pct = 0.0 if hi == 0 else 100.0 * (hi - lo) / abs(hi)
    return {"values": vals, "spread_pct": round(spread_pct, 3),
            "operating_point": "single normal state", "caveat": ag["caveat"]}


def or_groups() -> List[str]:
    """The quantities that have ≥2 substitutable producers."""
    return list(OR_GROUPS)


def or_group(q: str) -> dict:
    spec = OR_GROUPS[q]
    return {"produces": spec["produces"],
            "members": {m: d["kind"] for m, d in spec["members"].items()},
            "kinds": verify(q), "alias": spec.get("alias", False),
            "intuition": spec["intuition"]}


def alternatives_of(eid: str) -> List[str]:
    """The other equations substitutable for `eid` (same produced quantity), or []."""
    q = _MEMBER_TO_GROUP.get(eid)
    if q is None:
        return []
    return [m for m in OR_GROUPS[q]["members"] if m != eid]


def dependency_type(eid: str) -> dict:
    """Partition an equation's `depends_on` into AND deps and OR-groups.

    Returns {"and": [ids whose quantity has a single producer],
             "or": [{"produces": Q, "options": [alternative ids listed],
                     "kinds": {id: kind}} ...]}."""
    e = _eq(eid)
    if e is None:
        raise KeyError(f"{eid} not in registry")
    by_q: Dict[str, list] = defaultdict(list)
    and_deps = []
    for d in e.depends_on:
        q = _MEMBER_TO_GROUP.get(d)
        (and_deps.append(d) if q is None else by_q[q].append(d))
    return {
        "and": and_deps,
        "or": [{"produces": q, "options": opts,
                "kinds": {o: OR_GROUPS[q]["members"][o]["kind"] for o in opts},
                # alias groups are redundant duplicates, not a genuine choice — flag
                # so a consumer never counts them as independent alternatives
                "alias": OR_GROUPS[q].get("alias", False)}
               for q, opts in by_q.items()],
    }


def confused_consumers() -> List[dict]:
    """Equations whose flat `depends_on` lists ≥2 members of one OR-group — i.e.
    conflates substitutable alternatives as if jointly required. Each entry names
    the consumer, the quantity, the alternatives over-listed, and their kinds."""
    ix = _load_registry()
    eqs = []
    for c in ix.categories():
        eqs += ix.by_category(c)
    out = []
    for e in eqs:
        hit = defaultdict(list)
        for d in e.depends_on:
            q = _MEMBER_TO_GROUP.get(d)
            if q:
                hit[q].append(d)
        for q, ds in hit.items():
            if len(ds) > 1:
                out.append({"consumer": e.id, "produces": q, "alternatives": ds,
                            "kinds": {d: OR_GROUPS[q]["members"][d]["kind"] for d in ds}})
    return out


def summary() -> str:
    kinds = {k for q in OR_GROUPS for k in verify(q)}
    conf = confused_consumers()
    return (f"AND/OR typing: {len(OR_GROUPS)} OR-groups structurally grounded on shared "
            f"produces symbols; member kinds {sorted(kinds)}; "
            f"{len(conf)} consumers had alternatives conflated as AND")


if __name__ == "__main__":
    print(summary())
    for q in or_groups():
        ag = agreement(q)
        line = f"  {q}: kinds={verify(q)}  {OR_GROUPS[q]['intuition']}"
        if ag:
            line += f"\n       agree@1pt: spread={ag['spread_pct']}%  ⚠ {ag['caveat']}"
        print(line)
    print("Confused consumers (flat list treats alternatives as jointly-required):")
    for c in confused_consumers():
        print(f"  {c['consumer']}: {c['produces']} via any of {c['alternatives']}  kinds={c['kinds']}")

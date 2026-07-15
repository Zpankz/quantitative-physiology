"""Gate for the AND/OR dependency-typing layer (scripts.dependency_types): every
OR-group is grounded STRUCTURALLY — its members are ≥2 real registry equations that
declare the SAME `produces` symbol (that shared output is the alternative
relationship). The grounding has teeth (a member that does not actually produce the
group's quantity must be rejected), member kinds are honest (MAP carries an
`approximation` distinct from the `definitional` identity), numeric agreement is
only a caveated diagnostic, and the typing recovers the concrete conflated consumers.

Run: python -m scripts.tests.test_dependency_types
"""
import scripts.foundations, scripts.membrane, scripts.excitable, scripts.nervous  # noqa: F401
import scripts.cardiovascular, scripts.respiratory, scripts.renal  # noqa: F401
import scripts.gastrointestinal, scripts.endocrine  # noqa: F401
from scripts import dependency_types as DT
from scripts.canonical_ids import CANONICAL_EQUATIONS


def test_every_or_group_is_structurally_grounded():
    for q in DT.or_groups():
        kinds = DT.verify(q)
        assert kinds and all(k in DT.KINDS for k in kinds), f"{q}: bad kinds {kinds}"
        for m in DT.OR_GROUPS[q]["members"]:
            assert m in CANONICAL_EQUATIONS, f"{q}: member {m} is not a real equation"
    assert len(DT.or_groups()) >= 4


def test_structural_grounding_has_teeth():
    """verify() must reject a member that does not actually produce the group's
    quantity — the shared `produces` symbol IS the grounding, so a mismatch fails."""
    spec = DT.OR_GROUPS["CO"]
    members = spec["members"]
    # nernst_potential is a real equation but produces a voltage, not CO
    members["nernst_potential"] = dict(kind="definitional", note="bogus injected member")
    try:
        failed = False
        try:
            DT.verify("CO")
        except AssertionError:
            failed = True
        assert failed, "verify() accepted a member that does not produce CO — no teeth"
    finally:
        del members["nernst_potential"]
    assert DT.verify("CO")  # restored


def test_kinds_are_honest():
    """The audit's point: alternatives are not all the same kind. MAP must expose
    the bedside APPROXIMATION as distinct from the definitional identity, and CO
    must distinguish the definition from measurement methods."""
    assert set(DT.verify("MAP")) == {"approximation", "definitional"}
    assert "measurement" in DT.verify("CO")
    # and agreement() must be a caveated diagnostic, not a grounding claim
    ag = DT.agreement("MAP")
    assert ag is not None and "APPROXIMATION" in ag["caveat"].upper()
    assert DT.agreement("g_syn") is None  # model-tier: no shared operating point


def test_dependency_type_partitions():
    """systemic_oxygen_delivery needs CO by ANY method (OR) plus real AND deps."""
    d = DT.dependency_type("systemic_oxygen_delivery")
    co = [g for g in d["or"] if g["produces"] == "CO"]
    assert co and len(co[0]["options"]) >= 2, "CO alternatives not recovered as an OR-group"
    assert "measurement" in co[0]["kinds"].values()  # kinds surfaced in the partition
    assert not (set(d["and"]) & set(DT.OR_GROUPS["CO"]["members"]))


def test_confused_consumers_found():
    conf = DT.confused_consumers()
    names = {c["consumer"] for c in conf}
    assert "systemic_oxygen_delivery" in names   # the audit's CO case
    assert "epsp_amplitude" in names             # the g_syn case
    # structural property (not a brittle count floor): every flagged consumer truly
    # lists >=2 members of one OR-group, and they are real members of that group
    for c in conf:
        assert len(c["alternatives"]) >= 2
        assert set(c["alternatives"]) <= set(DT.OR_GROUPS[c["produces"]]["members"])
    assert len(conf) >= 1


def test_source_verified_nuances():
    """Two caveats the council raised and I confirmed in source must be honestly
    carried, not overstated: CaO₂ is an alias-grade group; map_from_flow's note
    records its conditional independence from the SVR definition."""
    assert DT.or_group("CaO2")["alias"] is True          # domain-duplicated relation
    assert DT.or_group("CO")["alias"] is False           # genuinely distinct methods
    map_note = DT.OR_GROUPS["MAP"]["members"]["map_from_flow"]["note"]
    assert "SVR" in map_note and "inverse" in map_note.lower()


def test_query_api():
    assert set(DT.alternatives_of("cardiac_output")) == \
        {"cardiac_output_fick", "indicator_dilution_cardiac_output"}
    assert DT.alternatives_of("nernst_potential") == []
    assert DT.or_group("MAP")["members"]["mean_arterial_pressure"] == "approximation"


def run():
    for t in (test_every_or_group_is_structurally_grounded, test_structural_grounding_has_teeth,
              test_kinds_are_honest, test_dependency_type_partitions,
              test_confused_consumers_found, test_source_verified_nuances, test_query_api):
        t()
    kinds = sorted({k for q in DT.or_groups() for k in DT.verify(q)})
    print(f"dependency-typing gate: {len(DT.or_groups())} OR-groups structurally grounded; "
          f"kinds {kinds}; {len(DT.confused_consumers())} conflated consumers recovered; query API ok")
    return 0


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

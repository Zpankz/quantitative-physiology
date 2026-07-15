"""Tests for the dimensional-analysis engine (scripts.dimensions) and the
equation graph layer (scripts.eqgraph).

Run: python -m scripts.tests.test_dimensions_graph
"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
from scripts.dimensions import parse
from scripts.eqgraph import build_graph


def test_named_dimensions():
    assert parse("mmHg").name() == "pressure"
    assert parse("mV").name() == "voltage"
    assert parse("mL/min").name() == "volumetric_flow"
    assert parse("mM").name() == "molar_concentration"
    assert parse("Pa·s").name() == "dynamic_viscosity"
    assert parse("m/s").name() == "velocity"
    assert parse("mL/mmHg").name() == "compliance"


def test_dimensionless_and_unknown():
    assert parse("dimensionless").is_dimensionless
    assert parse("%").is_dimensionless
    assert parse("ratio").is_dimensionless
    # 'arbitrary' is a DECLARED opaque scale: typed for reporting, but still never
    # dimension-matches (a sensation magnitude is not comparable to another).
    assert not parse("arbitrary").known
    assert not parse("variable").known
    assert parse("arbitrary").declared and parse("variable").declared
    assert not parse("arbitrary").same_dimension(parse("arbitrary"))
    assert parse("arbitrary/time").declared          # contagious through algebra
    # a genuinely unparseable unit stays UNKNOWN (not declared)
    assert not parse("zzz_no_such_unit").declared
    # every equation now has a DECLARED output dimension (367/367)
    g = build_graph()
    assert all(g.output_dim(i).declared for i in g.ids)


def test_prefix_scaling():
    # mV is 1e-3 of V but SAME dimension
    assert parse("mV").same_dimension(parse("V"))
    assert abs(parse("mV").scale / parse("V").scale - 1e-3) < 1e-12
    assert parse("mmHg").same_dimension(parse("Pa"))       # both pressure
    assert parse("mL").same_dimension(parse("L"))          # both volume


def test_dimension_algebra():
    # pressure * volume == energy   (M L^-1 T^-2 * L^3 = M L^2 T^-2)
    press, vol = parse("mmHg"), parse("mL")
    assert (press * vol).name() == "energy"
    # flow == volume / time
    assert (parse("mL") / parse("s")).same_dimension(parse("mL/min"))
    # velocity^2 has dimension L^2 T^-2
    assert (parse("m/s") ** 2).v == (0, 2, -2, 0, 0, 0, 0)


def test_diff_is_dimensionless_within_same_dimension():
    a, b = parse("mmHg"), parse("cmH2O")   # both pressure, different unit
    assert a.diff(b).is_dimensionless
    assert not parse("mmHg").diff(parse("mL")).is_dimensionless


def test_compound_gas_constant():
    d = parse("J/(mol·K)")                 # M L^2 T^-2 N^-1 K^-1
    assert d.known and d.v == (1, 2, -2, 0, -1, -1, 0)


def test_graph_builds_and_dependency_traversal():
    g = build_graph()
    st = g.stats()
    from scripts.canonical_ids import CANONICAL_EQUATIONS
    assert st["equations"] == len(CANONICAL_EQUATIONS) >= 321
    assert st["dependency_edges"] > 50
    # nernst feeds ghk_potential in the dependency DAG
    assert "ghk_potential" in g.dependents("nernst_equation")
    path = g.dependency_path("cardiac_index", "cardiac_output")
    assert path and path[0] == "cardiac_index" and path[-1] == "cardiac_output"


def test_parameter_dimension_query():
    g = build_graph()
    pressure_params = g.by_param_dimension(parse("mmHg"))
    assert len(pressure_params) > 20                 # many equations take a pressure
    # every hit really has a pressure-dimension parameter
    for eid, pname in pressure_params[:10]:
        assert g.param_dims(eid)[pname].name() == "pressure"


def test_compose_paths_signature_is_stable():
    # structure works even before output_units are populated (returns a list)
    g = build_graph()
    r = g.compose_paths("mmHg", "volumetric_flow", max_depth=2)
    assert isinstance(r, list)


def test_integrative_propagation():
    """Seeding measured base quantities propagates through the graph and yields
    physiologically correct integrated values (the 'simulate integration' path)."""
    g = build_graph()
    res = g.propagate(dict(HR=80, SV=65, EDV=120, ESV=55, W=70, H=175,
                           Hb=14, S_O2=0.97, P_O2=95, P_50=26.8, n=2.7,
                           SBP=125, DBP=78))
    fired = res["fired"]
    # a chain of derived quantities must have fired with correct values
    assert abs(fired["cardiac_output"] - 5.2) < 0.05          # HR*SV
    assert abs(fired["ejection_fraction"] - 0.5417) < 0.01    # (EDV-ESV)/EDV
    assert abs(fired["mean_arterial_pressure"] - 93.67) < 0.5  # DBP+PP/3
    assert abs(fired["cardiac_index"] - 2.81) < 0.05          # CO/BSA (chained through BSA)
    assert "systemic_oxygen_delivery" in fired                # O2 cascade reached
    assert len(fired) > 40                                    # broad integration


def test_dimensional_triples_closure():
    """The multiplicative closure: any two of {flow, resistance, pressure} give the
    third. Assert the real triple is found AND a nonsense one is not."""
    g = build_graph()
    tr = g.dimensional_triples()          # named_only=True
    def has(a, b, c):
        return any({t["a"], t["b"]} == {a, b} and t["product"] == c for t in tr)
    assert has("volumetric_flow", "vascular_resistance", "pressure")   # ΔP = Q·R
    assert has("pressure", "volume", "energy")                          # work = P·V
    # a non-triple: pressure × pressure is not a realised named dimension here
    assert not has("pressure", "pressure", "pressure")
    # every reported triple is all-named
    for t in tr:
        assert g._is_named(t["a"]) and g._is_named(t["b"]) and g._is_named(t["product"])


def test_cancellation_of_dimensionless_numbers():
    """A dimensionless number's 'full dimensional expression': the parameter
    exponents whose product cancels to 1 (Reynolds = rho·v·d/eta)."""
    g = build_graph()
    re = g.cancellation("reynolds_number_blood")
    assert re["dimensionless"] and re["exponents"] == {"rho": 1.0, "v": 1.0, "d": 1.0, "eta": -1.0}
    # a dimensional output is reconstructed too: CO = HR · SV
    co = g.cancellation("cardiac_output")
    assert not co["dimensionless"] and co["exponents"] == {"HR": 1.0, "SV": 1.0}
    # Womersley carries half/whole-integer exponents that still cancel to 1
    wo = g.cancellation("womersley_number")
    assert wo["dimensionless"] and set(wo["exponents"]) == {"r", "omega", "rho", "eta"}
    # the same form is materialized on the AtomicEquation object itself
    from scripts.canonical_ids import load
    assert load("reynolds_number_blood").dimensional_form["expression"] == "rho*v*d/eta"
    assert load("cardiac_output").dimensional_form["expression"] == "HR*SV"
    # an opaque (arbitrary) output has no dimensional form
    assert load("fechner_law").dimensional_form is None


def test_dimensional_inference_reasoning():
    """The 'any two give the third' reasoning move, grounded in a real equation:
    holding a flow and a resistance, a pressure is reachable, realised by the
    equation that actually composes them (MAP = flow x resistance)."""
    g = build_graph()
    inf = g.dimensional_inference([parse("mL/min"), parse("mmHg*min/mL")])
    press = [r for r in inf if r["reachable"] == "pressure"]
    assert press and press[0]["direct_realiser"]
    assert "map_from_flow" in press[0]["via_equations"]
    # accepts equation ids too, and never invents a value (returns hypotheses)
    inf2 = g.dimensional_inference(["cardiac_output", "poiseuille_resistance"])
    assert any(r["reachable"] == "pressure" for r in inf2)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for t in tests:
        try:
            t(); print(f"PASS  {t.__name__}"); passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}"); failed += 1
        except Exception as e:
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}"); failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(tests)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run())

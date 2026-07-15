"""Golden-value tests for Unit 1 (Physical Foundations) equations.

Unlike the package-wide structural suite (scripts/test_public_api.py), these
tests assert actual numeric results, guarding against silent formula
regressions. Run:

    python -m scripts.foundations.test_foundations     # plain runner
    (or, with pytest)  pytest scripts/foundations/test_foundations.py -q
"""
import math
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)

import scripts.foundations.transport as transport          # noqa: E402
import scripts.foundations.electrical as electrical        # noqa: E402
import scripts.foundations.diffusion as diffusion          # noqa: E402
import scripts.foundations.thermodynamics as thermo        # noqa: E402
import scripts.foundations.kinetics as kinetics            # noqa: E402


def _finite(x):
    return isinstance(x, float) and math.isfinite(x)


def test_transport_golden():
    # Laplace (cylinder): delta_P = T / r  -> 200 / 0.01 = 20000 Pa (exact)
    assert transport.laplace_cylinder.compute(T=200, r=0.01) == 20000.0
    # Laplace (sphere): delta_P = 2T / r  -> 2*0.025 / 150e-6
    assert math.isclose(transport.laplace_sphere.compute(T=0.025, r=150e-6),
                        2 * 0.025 / 150e-6, rel_tol=1e-9)
    # Poiseuille flow is positive for a positive pressure drop
    q = transport.poiseuille_flow.compute(r=50e-6, eta=3.5e-3, delta_P=2000, L=1e-3)
    assert _finite(q) and q > 0
    # Hydraulic resistance is positive
    assert transport.hydraulic_resistance.compute(eta=3.5e-3, L=1e-3, r=50e-6) > 0


def test_diffusion_golden():
    # Fick's first law: J = -D * dC/dx -> -1e-9 * (-1000) = 1e-6
    assert math.isclose(diffusion.fick_first_law.compute(D=1e-9, dC_dx=-1000),
                        1e-6, rel_tol=1e-9)
    # Diffusion time scales with distance squared: t(1mm)/t(1um) == 1e6
    t_um = diffusion.diffusion_time.compute(x=1e-6, D=1e-9)
    t_mm = diffusion.diffusion_time.compute(x=1e-3, D=1e-9)
    assert math.isclose(t_mm / t_um, 1e6, rel_tol=1e-6)


def test_thermodynamics_golden():
    # Nernst K+ (C_out=5 mM, C_in=140 mM, z=1) ~ -89 mV
    e_k = thermo.nernst_equation.compute(z=1, C_out=0.005, C_in=0.14)
    assert math.isclose(e_k, -89.0, abs_tol=0.5), e_k
    # Sign check: for z=+1 and C_out < C_in the equilibrium potential is negative
    assert thermo.nernst_equation.compute(z=1, C_out=0.005, C_in=0.14) < 0
    # ...and positive when the gradient reverses (Na+ style)
    assert thermo.nernst_equation.compute(z=1, C_out=0.14, C_in=0.01) > 0


def test_electrical_golden():
    # Capacitance C = Q / V -> 1e-12 / 0.07
    assert math.isclose(electrical.capacitance.compute(Q=1e-12, V=0.07),
                        1e-12 / 0.07, rel_tol=1e-9)
    # Coulomb force is finite and attractive (opposite charges -> negative)
    f = electrical.coulomb_law.compute(q1=1.6e-19, q2=-1.6e-19, r=1e-9)
    assert _finite(f) and f < 0


def test_kinetics_golden():
    # Michaelis-Menten at [S] = K_m gives exactly J_max / 2
    assert math.isclose(kinetics.michaelis_menten.compute(S=5.0, J_max=10.0, K_m=5.0),
                        5.0, rel_tol=1e-12)
    # Saturates toward J_max at high [S]
    assert kinetics.michaelis_menten.compute(S=1e6, J_max=10.0, K_m=5.0) > 9.9


def test_cross_domain_foundations_registered():
    from scripts.index import get_global_index
    idx = get_global_index()
    for eq_id in ("nernst_equation", "fick_first_law", "poiseuille_flow",
                  "laplace_sphere", "michaelis_menten"):
        eq = idx.get(eq_id)
        assert eq is not None, f"{eq_id} not registered"
        assert eq._compute_func is not None


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = failed = 0
    for t in tests:
        try:
            t(); print(f"PASS  {t.__name__}"); passed += 1
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}"); failed += 1
    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(_run())

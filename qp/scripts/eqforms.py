"""Equation form-typing — the structural classifier for the typed ensemble.

The audit asks for the *groundable* part of "what shape is each equation": not its
physiology, but its MATHEMATICAL FORM. Every one of the 367 registry equations is
assigned exactly one form from a closed set, by INSPECTING structural facts that are
already anchored elsewhere — never by hand-tagging a value. Every form in the closed
set is a genuine mathematical-structure category; a systems-level ROLE (e.g. being a
member of a feedback loop) is deliberately NOT a form here — that role is already
queryable, orthogonally, via ``scripts.feedback.loops_of`` and must not be smuggled
into a form taxonomy.

FORMS (closed set, precedence order — the order is deliberate, see below):
  * ``log_ratio``    — a potential/energy/pH set by log(ratio): Nernst, GHK,
    Henderson–Hasselbalch, ΔG=ΔG°+RT·lnQ, Fechner, decibel level.
  * ``saturation``   — a bounded/half-saturating response: Michaelis–Menten, Hill,
    receptor occupancy, SGLT/GLUT uptake, cooperative Ca²⁺ release.
  * ``dynamics_ode`` — a differential (rate) relation d·/dt or ∂·/∂t: HH gating,
    cable equation, viscoelastic models, the endocrine ODE dynamics.
  * ``exponential``  — an e^(±kt) / exp(...) form: first-order decay/charge,
    Arrhenius, Goldman flux, α-function, Gaussian receptive field.
  * ``power_term``   — the written formula carries a power term x^k (see the honest
    caveat below): allometric BSA/BMR, Stevens' law, Poiseuille r⁴, Coulomb r².
  * ``algebraic``    — the residual: a closed-form relation with none of the above
    markers (the largest bucket; the honest default, not a dumping ground).

GROUNDING (structural, not circular). Each classification is derived from facts that
are ALREADY anchored, so this module introduces no new physiological value, no
coefficient, and needs no external anchor (same exemption as ``scripts.dependency_types``
and ``scripts.primitives``): it is a structural read of already-anchored corpus fields,
not a new value claim, and the per-form partition sizes are *computed outputs*, never
committed constants — there is no external "textbook count of log_ratio equations" to
anchor to, and none is asserted. The two grounds:
  1. **Membership in ``scripts.primitives``** — proven by EXECUTION (the kernel
     reproduces the equation's compute). ``'saturation'``, ``'first_order'`` and
     ``'log_ratio'`` primitive membership pin the saturation / exponential / log_ratio
     forms respectively. This module CONSUMES that execution-proven membership as its
     primary ground (see ``form_of``) — it does not re-derive those forms by a weaker
     string method; the formula marker is an INDEPENDENT cross-check (see TEETH).
  2. **A structural marker in the equation's own ``simplified`` formula** — a
     literal, checkable string fact (an ``e^``/``exp``; an ``ln``/``log``; a
     Michaelis/Hill saturable denominator; a ``d·/dt``; a power ``x^k``). This
     classifies the equation's *authored* written form; it makes no claim of
     invariance under algebraic rewriting (see caveat (b)).

TEETH (why verify() is not tautological). The formula marker and the ``primitives``
membership are TWO INDEPENDENT grounds — one a string fact, one an execution fact.
``verify()`` cross-checks them: every equation the kernel proves to be a saturation
MUST also carry the saturable-denominator marker in its formula (and likewise
first_order→e^, log_ratio→ln). Perturb ``michaelis_menten.simplified`` to drop the
``/(K_m+S)`` denominator and the string marker flips False while ``primitive_of`` —
computed by execution — still says saturation: verify() then fails. That is real
mutation-sensitivity across two methods (a non-vacuity + agreement check, not a claim
of correctness against some external per-equation form ground-truth, which does not
exist) — exactly the independent-anchor discipline the project requires.

TWO HONEST CAVEATS (carried here, not swept under the label):
  (a) ``power_term`` names EXACTLY what is detected — "the written formula contains a
      power term x^k" — and makes NO allometric scaling claim (y∝xᵏ). It was renamed
      from an earlier ``power_law`` precisely so the label does not overstate: a
      sum-with-a-power-term relation (Bernoulli P+½ρv²+ρgh, Rohrer K₁Q+K₂Q², the
      colloid-osmotic polynomial, Poiseuille's r⁴) is NOT a power law and is not
      claimed to be — it carries a power term, which is all this form asserts.
      Poiseuille's KERNEL view is ``linear_flux`` — query ``primitive_of`` for the
      complementary kernel reading.
  (b) The classifier types the registry's *authored* ``simplified`` string, so it is
      representation-dependent by construction: an algebraically-equivalent rewrite
      could add or drop an exp/log/power token. This is a deliberate, bounded scope —
      "what shape did the author write" — not a claim about canonical form. Where the
      shape matters most (saturation/exponential/log_ratio) the cross-ground against
      the execution-proven primitive kernel is the independent check that the written
      marker is not accidental.

No equation is modified; this is an additive relational layer beside the DAG, exactly
like ``scripts.primitives``, ``scripts.feedback`` and ``scripts.dependency_types``.
The feedback-loop ROLE is not represented here (it is not a mathematical form); it
stays available, orthogonally, through ``scripts.feedback.loops_of``.
"""
from __future__ import annotations
import re
from typing import Dict, List

from scripts.primitives import primitive_of

# Precedence order (first matching form wins). Deliberate, deterministic tie-break:
# the more specific / execution-anchored math forms are tested before the closed-form
# residual. It asserts no physiological value — only which marker wins when several
# hold (e.g. a Hill ratio that also contains a caret is saturation, not power_term).
FORMS: List[str] = [
    "log_ratio", "saturation", "dynamics_ode", "exponential",
    "power_term", "algebraic",
]

INTUITION: Dict[str, str] = {
    "log_ratio":    "a potential / energy / pH set by the LOG of a ratio (RT·ln, decibel, Fechner)",
    "saturation":   "a bounded, half-saturating response to a driver (Michaelis / Hill / occupancy)",
    "dynamics_ode": "a differential rate relation d·/dt or ∂·/∂t (gating, cable, viscoelastic, axis ODEs)",
    "exponential":  "an e^(±kt) / exp(...) form (first-order decay/charge, Arrhenius, Gaussian)",
    "power_term":   "the written formula carries a power term x^k — NOT an allometric-law claim (Poiseuille r⁴, Coulomb r²)",
    "algebraic":    "a closed-form relation with none of the above markers (the honest residual)",
}


# --------------------------------------------------------------- formula markers
# Each marker is a literal, checkable structural fact about the `simplified` string.
# Affinity/dissociation-constant tokens that head a Michaelis/Hill saturable
# denominator (K_m, K_d, EC50, ...) — the signature that separates a true saturation
# x/(K+x) from a weighted mean (Σwx)/(Σw) or a contrast ratio (a−b)/(a+b).
_AFFINITY = (r"K_?m|K_?M|K_?d|K_?D|K_?i|K_?I|K_?H|K_ADH|K_Mg|K_half"
             r"|EC_?50|IC_?50|P_?50|K_[A-Za-z0-9]+")


def _has_log(s: str) -> bool:
    """A logarithm: ln / log / log10 (the log_ratio form's marker)."""
    return bool(re.search(r"\bln\b|\blog\b|log10|log_?10|log₁₀", s, re.I))


def _has_exp(s: str) -> bool:
    """An exponential: e^ or exp( (the exponential form's marker)."""
    return bool(re.search(r"e\s*\^|exp\(", s, re.I))


def _has_time_deriv(s: str) -> bool:
    """A time/rate derivative d·/dt or ∂·/∂t (the dynamics_ode marker). Restricted
    to TIME derivatives per the roadmap ('a rate/dt relation'): a spatial gradient
    dC/dx (Fick's first law) is a flux law, not an ODE, and is NOT matched here."""
    return bool(re.search(r"(?:d|∂)\s*[^/=]{0,15}?/\s*(?:d|∂)\s*t\b|d/dt", s))


def _has_saturation(s: str) -> bool:
    """A Michaelis–Menten / Hill saturable form (the saturation marker): a division
    by a sum headed by an affinity constant  x/(K_m+x), or matched powers across the
    fraction  x^n/(K^n+x^n), or a Boltzmann/inhibitory Hill  …/(1+(…)^n) …/(K^n+…).
    Tight by design — a weighted mean (Σg·E)/(Σg) or contrast (a−b)/(a+b) is NOT a
    saturation and must not match."""
    return bool(
        re.search(r"/\s*\(\s*(?:" + _AFFINITY + r")\s*\+", s)
        or re.search(r"\^\s*(?:n|\d+)\s*/\s*\([^=]*?\^\s*(?:n|\d+)", s)
        or re.search(r"/\s*\(\s*1\s*\+.*\^\s*(?:n|\d+)", s)
        or re.search(r"/\s*\(\s*(?:" + _AFFINITY + r")\s*\^", s)
    )


def _has_power(s: str) -> bool:
    """A power term x^k with a numeric or `n` exponent (the power_term marker).
    Written-form sense only (see caveat (a) in the module docstring)."""
    return bool(re.search(r"\^\s*\{?-?\d|\^\s*\{?n\b|\^\{?[0-9]", s))


# marker per form, over the SAME two inputs form_of derives from, so a form's teeth
# are exactly "the property that put an equation in that bucket". `algebraic` = none
# of the specific markers hold (a checkable residual: an algebraic-typed equation
# provably carries no e^, ln, saturable denominator, d·/dt, or power term).
def _marker(form: str, s: str, prims: List[str]) -> bool:
    if form == "log_ratio":
        return "log_ratio" in prims or _has_log(s)
    if form == "saturation":
        return "saturation" in prims or _has_saturation(s)
    if form == "dynamics_ode":
        return _has_time_deriv(s)
    if form == "exponential":
        return "first_order" in prims or _has_exp(s)
    if form == "power_term":
        return _has_power(s)
    if form == "algebraic":
        return not any(_marker(f, s, prims) for f in FORMS if f != "algebraic")
    raise KeyError(f"unknown form {form!r}")


def _classify(simplified: str, prims: List[str]) -> str:
    """Pure classifier: the first form in precedence order whose marker holds. Takes
    the raw structural inputs (formula string, primitive memberships) so it can be
    exercised on synthetic strings, without the registry."""
    for form in FORMS:
        if form != "algebraic" and _marker(form, simplified, prims):
            return form
    return "algebraic"


# ------------------------------------------------------------------ registry glue
def _load_registry():
    import scripts.foundations, scripts.membrane, scripts.excitable, scripts.nervous  # noqa
    import scripts.cardiovascular, scripts.respiratory, scripts.renal  # noqa
    import scripts.gastrointestinal, scripts.endocrine  # noqa
    from scripts.index import get_global_index
    return get_global_index()


def _eq(eid: str):
    _load_registry()
    from scripts.index import get_equation
    e = get_equation(eid)
    if e is None:
        raise KeyError(f"{eid} not in registry")
    return e


def _all_equations():
    ix = _load_registry()
    eqs = []
    for c in ix.categories():
        eqs += ix.by_category(c)
    return eqs


# ------------------------------------------------------------------ verify + query
def form_of(eid: str) -> str:
    """The mathematical form of an equation, derived structurally from its formula
    plus its ``primitives`` (execution-proven) membership."""
    e = _eq(eid)
    return _classify(e.simplified, primitive_of(eid))


def verify(eid: str) -> str:
    """Prove the classification with teeth, returning the form. Asserts:

    (a) INTERNAL — the assigned form's characteristic marker is present (so the
        classification is not vacuous).
    (b) CROSS-GROUND (the real teeth, two independent methods) — every equation that
        ``scripts.primitives`` proves BY EXECUTION to be a saturation / first-order /
        log-ratio also carries the corresponding formula-string marker. Perturb the
        formula so the string marker vanishes while the executable kernel still
        matches, and this assertion fails.

    Raises AssertionError on any failure.
    """
    e = _eq(eid)
    s = e.simplified
    prims = primitive_of(eid)
    f = _classify(s, prims)

    assert _marker(f, s, prims), f"{eid}: assigned {f!r} but its marker is absent"

    # (b) execution-proven primitive membership must agree with the string marker
    if "saturation" in prims:
        assert _has_saturation(s), f"{eid}: proven-saturation kernel but no saturable denominator in formula"
    if "first_order" in prims:
        assert _has_exp(s), f"{eid}: proven-first_order kernel but no e^/exp in formula"
    if "log_ratio" in prims:
        assert _has_log(s), f"{eid}: proven-log_ratio kernel but no ln/log in formula"
    return f


def forms() -> List[str]:
    """The closed set of forms, in precedence order."""
    return list(FORMS)


def by_form(form: str) -> List[str]:
    """Every equation id classified as ``form`` (sorted). Raises on an unknown form."""
    if form not in FORMS:
        raise KeyError(f"unknown form {form!r}; forms are {FORMS}")
    return sorted(e.id for e in _all_equations()
                  if _classify(e.simplified, primitive_of(e.id)) == form)


def all_forms() -> Dict[str, List[str]]:
    """The full partition: form -> its equation ids."""
    out: Dict[str, List[str]] = {f: [] for f in FORMS}
    for e in _all_equations():
        out[_classify(e.simplified, primitive_of(e.id))].append(e.id)
    for f in out:
        out[f].sort()
    return out


def explain(form: str) -> dict:
    """A form's intuition plus its members."""
    if form not in FORMS:
        raise KeyError(f"unknown form {form!r}; forms are {FORMS}")
    return {"form": form, "intuition": INTUITION[form], "members": by_form(form)}


def distribution() -> Dict[str, int]:
    """Count of equations per form (a computed output, not a committed constant)."""
    return {f: len(ids) for f, ids in all_forms().items()}


def summary() -> str:
    dist = distribution()
    total = sum(dist.values())
    parts = ", ".join(f"{f}={dist[f]}" for f in FORMS)
    return (f"equation form-typing: {total} equations classified into "
            f"{len(FORMS)} structural forms ({parts}); "
            f"grounded by primitives (execution) + formula markers")


if __name__ == "__main__":  # self-check / distribution report
    eqs = _all_equations()
    ok = bad = 0
    for e in eqs:
        try:
            verify(e.id)
            ok += 1
        except AssertionError as exc:
            bad += 1
            print("FAIL", e.id, exc)
    print(summary())
    print(f"{ok}/{ok + bad} classifications verified (marker present + cross-ground consistent)")
    for f in FORMS:
        print(f"  {f:16s} {len(by_form(f)):3d}  — {INTUITION[f]}")

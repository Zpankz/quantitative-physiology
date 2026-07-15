"""Feedback loops — the layer the equation DAG cannot express.

The dependency graph is an acyclic DAG (0 cycles, by design and for safe
propagation). But physiology is governed by *closed loops*: a sensed variable
drives a controller that drives an effector that changes the sensed variable back
— baroreflex, HPA axis, tubuloglomerular feedback, chemoreceptor ventilation. A
DAG structurally cannot represent that return edge, so these loops are invisible
in `depends_on`.

This module represents the loops explicitly, as first-class objects *beside* the
DAG (never adding a cycle to it): each loop names its sensed variable, its member
equations (real ids), its sign, and — where the coupling lives inside a single
member's formula — the exact inhibitory term that closes it, so the "negative
feedback" claim is *checked against the equation*, not merely asserted.

Grounding tiers (honest about strength, like `dimensional_inference.direct_realiser`):
  * ``formula``   — the closing coupling is a subtractive term in a member's own
    formula (e.g. cortisol's ``− k_cort·[Cortisol]`` in CRH dynamics). Executable.
  * ``structural``— a multi-step reflex whose members all resolve and whose loop is
    standard physiology, but whose closure spans several equations (baroreflex).

No equation is modified; this is an additive relational layer.
"""
from __future__ import annotations
import re
from typing import Dict, List


# name -> loop spec
LOOPS: Dict[str, dict] = {
    "hpa_axis": dict(
        sensed="Cortisol", effector="CRH→ACTH→cortisol secretion", sign="negative",
        members=["hpa_crh_dynamics", "hpa_acth_dynamics", "hpa_cortisol_dynamics"],
        closes_via=("hpa_crh_dynamics", "Cortisol"),   # cortisol inhibits CRH
        intuition="cortisol feeds back to suppress CRH/ACTH — the classic endocrine axis"),
    "hpt_axis": dict(
        sensed="fT4", effector="TRH→TSH→thyroid output", sign="negative",
        members=["thyroid_tsh_dynamics", "thyroid_t4_dynamics"],
        closes_via=("thyroid_tsh_dynamics", "fT4"),     # T4 inhibits TSH
        intuition="free T4 feeds back to suppress TSH — thyrostat"),
    "tropic_target": dict(
        sensed="Target", effector="tropic hormone secretion", sign="negative",
        members=["feedback_tropic_dynamics", "feedback_target_dynamics", "feedback_gain"],
        closes_via=("feedback_tropic_dynamics", "Target"),  # target inhibits tropic
        intuition="the generic endocrine set-point loop: product inhibits its own driver"),
    "baroreflex": dict(
        sensed="SBP", effector="HR + TPR (autonomic)", sign="negative",
        members=["baroreceptor_sensitivity", "mean_arterial_pressure",
                 "heart_rate_autonomic", "total_peripheral_resistance"],
        closes_via=None,   # multi-step reflex: BP→baroreceptor→autonomic→HR/TPR→BP
        intuition="a rise in arterial pressure reflexly lowers HR and TPR, returning pressure"),
    "tubuloglomerular_feedback": dict(
        sensed="macula-densa NaCl (∝ SNGFR)", effector="afferent arteriolar tone", sign="negative",
        members=["tubuloglomerular_feedback", "renal_autoregulation_index"],
        closes_via=None,
        intuition="high distal NaCl constricts the afferent arteriole, lowering SNGFR"),
    "chemoreceptor_ventilatory": dict(
        sensed="P_aCO2", effector="alveolar ventilation", sign="negative",
        members=["co2_response", "alveolar_ventilation"],
        closes_via=None,
        intuition="rising CO2 drives ventilation, which clears CO2 back toward set-point"),
    "raas": dict(
        sensed="blood pressure / volume", effector="Na+ and water retention", sign="negative",
        members=["aldosterone_regulation", "adh_water_permeability"],
        closes_via=None,
        intuition="low pressure/volume raises AngII/aldosterone/ADH, retaining salt and water"),
}


def _has_inhibitory_term(simplified: str, token: str) -> bool:
    """True if `token` appears in a SUBTRACTED term of the formula (a negative
    coupling), e.g. '… - k_cort × [Cortisol] …' for token 'Cortisol'."""
    # a minus sign, then anything up to the next +/= , containing the token
    return bool(re.search(r"[-−]\s*[^+=\n]*" + re.escape(token), simplified))


def verify(name: str) -> bool:
    """Ground the loop: every member is a real equation, and (formula-tier loops)
    the closing inhibitory coupling actually appears in the named member's formula."""
    from scripts.canonical_ids import CANONICAL_EQUATIONS, load
    spec = LOOPS[name]
    if not all(m in CANONICAL_EQUATIONS for m in spec["members"]):
        return False
    cv = spec.get("closes_via")
    if cv is None:
        return True   # structural loop: members resolving is the ground we assert
    eid, token = cv
    if eid not in spec["members"]:
        return False
    return _has_inhibitory_term(load(eid).simplified, token)


def grounding(name: str) -> str:
    return "formula" if LOOPS[name].get("closes_via") else "structural"


# ------------------------------------------------------------------ query API
def loops() -> List[str]:
    return list(LOOPS)


def loop(name: str) -> dict:
    return {"name": name, "grounding": grounding(name), **LOOPS[name]}


def loops_of(eid: str) -> List[str]:
    """Which feedback loop(s) an equation participates in."""
    return [n for n, s in LOOPS.items() if eid in s["members"]]


def by_sensed(substr: str) -> List[str]:
    s = substr.lower()
    return [n for n, sp in LOOPS.items() if s in sp["sensed"].lower()]


if __name__ == "__main__":
    ok = bad = 0
    for n in LOOPS:
        (ok := ok + 1) if verify(n) else print(f"FAIL {n}")
        bad += 0 if verify(n) else 1
    print(f"{ok}/{len(LOOPS)} feedback loops grounded "
          f"({sum(grounding(n)=='formula' for n in LOOPS)} formula-verified, "
          f"{sum(grounding(n)=='structural' for n in LOOPS)} structural)")

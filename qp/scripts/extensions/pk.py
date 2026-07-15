"""Pharmacokinetic definitional core (draft, Feature 2) — steady-state timing.

Feature 2 originally proposed 8 one-/two-compartment PK relations. On review it
turned out that 7 of them duplicate an existing registered concept (match-by-concept,
CLAUDE.md §3.3), so they are NOT reusable additions and have been removed:

  * Vd = Dose/C0            -> already `apparent_volume_of_distribution`
                               (and id-collides with the Fick `volume_of_distribution`)
  * k  = CL/Vd              -> already `elimination_rate_constant` (same id)
  * CL = k·Vd               -> algebraic inverse of `elimination_rate_constant`
                               (and id-collides with renal `clearance`)
  * t½ = ln2/k              -> half-life already covered by `hormone_half_life`
                               (t½ = 0.693·Vd/CL), same concept
  * C(t) = C0·e^(−kt)       -> already `first_order_elimination` (same relation)
  * Css = R0/CL             -> algebraic inverse of `maintenance_infusion_rate`
  * LD = Vd·C_target        -> already `loading_dose` (same id)

Those seven relations are *committable in kind* (definitional identities / exact
coefficients such as ln 2, not invented drug numbers) — but the library's no-duplicate
rule governs, and they already live in `scripts.foundations.kinetics` /
`scripts.foundations.transport` / `scripts.endocrine.kinetics`. So they are out, not
because they are ungrounded, but because the concept is already present.

What remains is the one relation with no registry equivalent:

  * t_ss = n · t½   — time expressed as a number n of elimination half-lives.

The number n is a caller-supplied count of half-lives (NO default is committed): the
"4–5 half-lives ≈ steady state" figure is a clinical convention, not a definitional
identity, so it is not baked in. Given n, the relation is pure multiplication — a
definitional identity with nothing invented.

This is an ADDITIVE, STANDALONE module (mandated design: create only a new module +
test, edit no existing file). It deliberately does NOT call ``register_equation`` and
does NOT touch ``scripts.canonical_ids`` or the global index. The sole id
``time_to_steady_state`` is unique across the registry, so there is no collision.

Category note: ``pharmacokinetics`` is not an ``EquationCategory``; FOUNDATIONS is the
bucket where the canonical PK equations already live, so it is used here too.
"""

from scripts.base import (
    EquationCategory,
    EquationMetadata,
    Parameter,
    create_equation,
)

CATEGORY = EquationCategory.FOUNDATIONS  # pharmacokinetics is not a category; use FOUNDATIONS

# Definitional relation, no page number to invent.
_META = EquationMetadata(
    source_unit=0,
    source_chapter="clinical",
    source_section="Steady-state timing as a multiple of elimination half-life "
                   "(CICM/ANZCA); definitional, beyond Feher's numeric text",
    page_reference=None,
)


# ---------------------------------------------------------------------------
# Time to steady state: t_ss = n · t½   (n = number of half-lives, caller-supplied)
# ---------------------------------------------------------------------------
def compute_time_to_steady_state(t_half: float, n: float) -> float:
    """Time expressed as n elimination half-lives, t_ss = n · t½.

    ``n`` is the number of half-lives and MUST be supplied by the caller — no
    default is committed, because the familiar "4–5 half-lives ≈ steady state"
    figure is a clinical *convention*, not a definitional identity. Given n the
    relation is pure multiplication; after n half-lives the fraction of the
    plateau reached is exactly 1 − 2^-n (n=4 -> 93.75%, n=5 -> 96.875%), which is
    exact mathematics, not an empirical fit.
    """
    return n * t_half


time_to_steady_state = create_equation(
    id="time_to_steady_state",
    name="Time to Steady State",
    category=CATEGORY,
    latex=r"t_{ss} = n \cdot t_{1/2}",
    simplified="t_ss = n * t_half",
    description="Time to reach (near) steady state on constant dosing, expressed "
                "as a number n of elimination half-lives. After n half-lives the "
                "fraction of the plateau reached is exactly 1 − 2^-n "
                "(n=4 -> 93.75%, n=5 -> 96.875%); the '4-5 half-lives' rule is a "
                "convention on n (caller-supplied), while the relation itself is exact.",
    compute_func=compute_time_to_steady_state,
    output_units="h",
    parameters=[
        Parameter(name="t_half", description="Elimination half-life", units="h",
                  symbol="t_{1/2}", physiological_range=(1e-3, 1000.0)),
        Parameter(name="n", description="Number of elimination half-lives elapsed "
                  "(caller-supplied; clinical convention for near-steady-state is 4-5)",
                  units="dimensionless", symbol="n", physiological_range=(0.0, 20.0)),
    ],
    produces="t_ss",
    metadata=_META,
)


# Convenience collection for consumers / tests.
EQUATIONS = {eq.id: eq for eq in (time_to_steady_state,)}

__all__ = [
    "time_to_steady_state",
    "EQUATIONS",
]

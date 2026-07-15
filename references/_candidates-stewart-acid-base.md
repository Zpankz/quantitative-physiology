# Candidate reference material — Stewart acid-base (STAGED, not canonical)

Source: RLM extraction (grok-4.5 + adversarial critique) over a 2026-07-15
Stewart acid-base tutorial recording
(`pex-clean/ops/sessions/2026-07-15-stewart-acid-base-live.md`), routed here by
the voice-learning-agent improvement workflow's context-only lane.

**Status:** these are source-anchored CANDIDATES for review — NOT part of the
canonical 340-equation set, NOT registered, and they do not touch
`canonical_ids.py` or the equation count. The equation machinery is already
canonical (see cross-refs); the net-new value here is the *definitional /
schema / guardrail* layer that catches the exact category errors the tutorial
made. Physiology independently verified correct by the workflow's critic
against Stewart/Kam-Power/Feher canon.

Each card carries its transcript line anchor and, where applicable, the
existing `qp:` symbol it augments.

---

## Lane: definitions

### D1 — Strong vs dependent ions: the SIDa/SIDe/SIG category rule
*anchor: transcript:69 · augments `qp:strong_ion_difference_apparent`, `qp:strong_ion_difference_effective`*

Bicarbonate and albumin are **weak/dependent buffer ions, never strong ions** —
they belong in SIDe (and Atot), never in SIDa. The tutorial's error was listing
HCO₃⁻/albumin among strong ions.

- **SIDa** (apparent) = measured **strong**-ion charge only: (Na⁺ + K⁺ + 2·Ca²⁺ + 2·Mg²⁺) − (Cl⁻ + lactate⁻ + other measured strong anions).
- **SIDe** (effective) = measured **dependent**-buffer charge = [HCO₃⁻] + albumin charge + phosphate charge.
- **SIG** (strong-ion gap) = SIDa − SIDe = estimate of **unmeasured strong-anion** charge.

Mnemonic: *apparent = measured strong ions; effective = measured dependent
buffer anions; gap = the missing charge between them.*

### D2 — SIG residual is panel-relative (lactate double-count guardrail)
*anchor: transcript:53 · guardrail on `qp:strong_ion_difference_effective` (SIG)*

An ion is "unmeasured" **only relative to the measured panel used**. If lactate
is measured and placed in SIDa, it must **not** be re-counted as a SIG anion.
Lactate behaves as an omitted (SIG) charge **only** in a simplified Na−Cl SID.
Always state the SID formula before naming the residual. Genuinely-unmeasured
anions (keto-anions, exogenous) are the appropriate SIG examples; measured
lactate is not.

### D3 — Fluid SID effects (saline → HYPERchloraemia)
*anchor: transcript:77 (corrects a spoken "hypochloraemia" slip)*

0.9% saline delivers Cl⁻ 154 mmol/L with effective SID ≈ 0 → **hyperchloraemia**,
lowers plasma SID, worsens non-anion-gap (hyperchloraemic) acidosis. Balanced
crystalloids: Plasma-Lyte Cl⁻ ≈ 98 mmol/L, Hartmann's ≈ 109–112 mmol/L, both
carrying metabolizable anions (lactate/acetate/gluconate) that raise effective
SID after metabolism. The acid-base effect is the **post-metabolism effective
SID and the dose**, not chloride concentration alone.

### D4 — Stewart vs Henderson-Hasselbalch: not valid-vs-invalid
*anchor: transcript:88*

HH is a correct **equilibrium description**; Stewart is a **choice of independent
variables** (PaCO₂, SID, Atot) for causal decomposition. They are not
competing truth claims — never frame one as valid and the other invalid. HH
answers "what is the [H⁺] given HCO₃⁻ and PCO₂"; Stewart answers "what *drove*
the change." High-yield exam framing guard.

---

## Lane: schemas

### S1 — Stewart independent/dependent variable schema + directional spine
*anchor: transcript:54 · the CP23A01 examiner-rewarded causal spine*

- Governing laws: **electroneutrality, mass action, conservation of mass**.
- **Independent** variables (set from outside): {PaCO₂, SID, Atot (total weak acids ≈ albumin + phosphate)}.
- **Dependent** variables (fall out of the equations): {H⁺, OH⁻, HCO₃⁻}. "Dependent" ≠ unimportant/absent.
- Directional map — **acidify**: SID↓, Atot↑, PaCO₂↑; **alkalinise**: SID↑, Atot↓, PaCO₂↓.
- PaCO₂ handles the respiratory disturbance; SID and Atot decompose the metabolic disturbance.

### S2 — Gamblegram + albumin-corrected anion gap
*anchor: transcript:81 · augments `qp:anion_gap` (corrected-AG is NOT yet canonical)*

Corrected AG ≈ AG + 2.5 × (40 − albumin g/L) — the standard 0.25 mEq/L per g/L
albumin relation. Hypoalbuminaemia both lowers the *expected* AG **and**
alkalinises via reduced Atot, so an uncorrected AG can conceal a coexisting
high-AG acidosis. (Candidate equation for the equations lane — see E2.)

---

## Lane: equations

### E1 — SIDa / SIDe / SIG triplet — ALREADY CANONICAL (cross-ref, do not re-add)
*anchor: transcript:44 · `qp:strong_ion_difference_apparent`, `qp:strong_ion_difference_effective`, `qp:figge_fencl_*`*

The equation set (SIDa with ×2 divalent weighting, SIDe = HCO₃⁻ + A⁻, SIG =
SIDa − SIDe, Figge-Fencl A⁻ estimate, normal SIDa ≈ 40–44 mEq/L convention-
dependent) is **already registered** in `qpm/scripts/respiratory/acid_base.py`.
Recorded here only to confirm the extraction matched canon — **no new equation,
count unchanged.**

### E2 — Albumin-corrected anion gap — CANDIDATE (needs the reference-audit ratchet)
*anchor: transcript:81*

`corrected_AG = AG + 2.5 × (40 − albumin_g_L)` (mEq/L; 0.25 mEq/L per g/L).
Genuinely absent from canon (`qp:anion_gap` is uncorrected). If promoted, it
must go through qp's external-reference-locked test ratchet like every other
equation — **not** hand-added here. Flagged, not injected.

---

## Lane: diagrams

*(none surfaced — the extraction found no diagram-shaped material in this
transcript. Recorded as an honest empty lane, not padded.)*

---

## Disposition summary

- **Already canonical (cross-ref only):** the SIDa/SIDe/SIG/Figge-Fencl equation machinery (E1).
- **Net-new definitional/schema guardrails (this file):** D1–D4, S1–S2.
- **Candidate equation (flagged, not injected):** albumin-corrected AG (E2) — awaits the reference-audit ratchet.
- **Canonical equation count: UNCHANGED.** Nothing here is registered.

# QPM architectural assessment — external audit + response

Source: an external architectural audit of QPM (GPT-5.6-pro, "QPM environment
loaded", 2026-07-15), scored against the CICM 2025 + ANZCA v1.14 syllabi and 8
CICM examiner reports. Its verdict is recorded here with an honest response —
what has been **addressed** in-grounding, and what is genuinely **roadmap**
(out of scope for a grounded increment; would require corpus that cannot be
fabricated without violating the skill's grounding discipline).

## Verdict (audit)
QPM is a **canonical-equation substrate** — strong on normal-adult
cardiorespiratory / renal / acid-base / membrane / electrophysiology — but is an
*equation atlas, not an integrated network*. "Not mainly an equation-count
problem; a representation and integration problem."

## Structural findings → response

| Audit finding | Response |
|---|---|
| Dependencies 134 "not excessive — insufficient" | **Partly addressed:** +14 grounded, hijack-guarded edges → 148; isolated 222→214. More is genuine work, not padding — added only where a producer/consumer/units/no-cycle check passed. |
| Dimensional bridges 12,161 "compatibility candidates, not causal links" | **Addressed (framing):** `dimensional_bridges` is explicitly a candidate set; `dimensional_inference` returns *hypotheses grounded in a realising equation* (`direct_realiser`), never asserted causation or fabricated values. |
| Declared dimensions 350/367; "17 should NOT all be relabelled dimensionless" | **Addressed exactly as advised:** 5 were real units (percent/IU → typed); the 12 opaque got a distinct **`Dim.ARBITRARY`** (declared, but never dimension-matches) — *not* collapsed to dimensionless. 367/367 declared. |
| "0 cycles → unable to represent feedback directly" | **Addressed:** new `scripts/feedback.py` — 7 grounded feedback loops (HPA, HPT, tropic-target, baroreflex, TGF, chemoreflex, RAAS) as first-class objects *beside* the DAG; 3 are formula-verified (the closing inhibitory term is checked against a member's own formula). The compute DAG stays acyclic. |
| Flat `depends_on` "confuses alternatives with jointly-required inputs" | **Identified, not yet built** (roadmap): AND/OR dependency typing. Surfaced concretely by the CaO₂ two-producer case (blood_ vs respiratory_oxygen_content are *alternatives*). A real, bounded next step. |
| "Same fundamental concept" / reduce dependencies | **Addressed (beyond the audit's ask):** `scripts/primitives.py` — 7 universal kernels, 47 execution-proven memberships showing disparate equations (Nernst≡HH≡Gibbs; MM≡Hill≡SGLT) are one form. |

## Roadmap resolution (adversarial-council self-improving loop)
The roadmap was worked through a regulated loop — author a grounded proposal → a
3-model adversarial council (`scripts/council.py`: gemini-3.1-pro-low +
claude-opus-4-6-thinking + gpt-5.6-terra via vibeproxy; requested grok-4.5 was
auth-down) → source-verify every REJECT → deterministic §4 gate decides. Full
record in `ROADMAP_LEDGER.md`. Each item is now **resolved** = implemented-and-gated
OR evidenced-reject (council consensus + confirmed no external anchor):

- **AND/OR dependency typing** → **implemented-and-gated** (`scripts/dependency_types.py`):
  the audit's flat-`depends_on` gap. 4 OR-groups grounded on shared `produces` symbols,
  members typed by kind (definitional/approximation/measurement/model); surfaces the 10
  consumers that conflated alternatives as jointly-required. 0 canonical-count change.
- **Form-typing** (typed-ensemble's groundable core) → **implemented-and-gated**
  (`scripts/eqforms.py`): all 367 classified into 6 structural forms on two independent
  grounds. The digital-twin/ontology/probabilistic subsystems remain evidenced-reject.
- **Pharmacology** → **resolved**: the council loop found 7/8 drafted PK relations
  **already in the corpus**; only `time_to_steady_state` was genuinely new (extensions tier).
  Multi-compartment/TCI/popPK with drug-specific parameters stay out (need invented drug data).
- **Measurement/equipment** → **core implemented-and-gated** (`scripts/extensions/instrument.py`):
  6 exact-math response forms (first-order 1−e^(−t/τ), rise time, dB, 2nd-order damping).
  Drift/calibration/quantisation/artefact metrology stays evidenced-reject (device-specific).
- **Thermoregulation** (coverage gap) → **core implemented-and-gated**
  (`scripts/extensions/thermo.py`): 5 definitional heat-balance relations (partitional
  calorimetry + Newton/Fourier/Stefan-Boltzmann/latent). Immunity/obstetric/haemostasis
  stay out (largely non-quantitative). Only σ committed (exact SI).
- **Context/populations** → **evidenced-reject** (council-confirmed): a covariance
  structure is empirical numbers absent from Feher; inventing them (or per-equation
  ×multipliers) violates the iron rule. Groundable subset: `Parameter.physiological_range`
  already encodes per-parameter bounds.

The new definitional relations that go beyond Feher live in a separate
**`scripts/extensions/`** tier — same grounding discipline, explicitly NOT part of
the canonical 367, so the corpus count and gate stay intact. The discipline held
throughout: additive only, no fabricated value, honest distribution (no padding —
PK's mostly-already-present result was reported as such), evidenced-rejects recorded
rather than stubbed.

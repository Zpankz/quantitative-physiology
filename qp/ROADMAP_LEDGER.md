# Roadmap resolution ledger — self-improving loop with adversarial council

**Loop:** for each roadmap feature → author a grounded proposal → 3-model
adversarial council review (`scripts/council.py`) → verify any REJECT against
source → integrate iff approved **and** source-verified → run §4 gate (must stay
green) → checkpoint this ledger. A feature is **RESOLVED** when it is either
*implemented-and-gated* or an *evidenced-reject* (council consensus **and** I
confirmed no independent external anchor exists — not a convenient exit).

**Council:** `gemini-3.1-pro-low` (google) · `claude-opus-4-6-thinking`
(anthropic) · `gpt-5.6-terra` (openai). Requested `grok-4.5` (xai) is
`auth_unavailable` on vibeproxy — substituted by gpt-5.6-terra to keep three
independent families. The council proposes/critiques; the **§4 gate decides**.

**Discriminator (External Reference Ratchet):** is each value anchored to an
*independent* external number, or is the only validation circular? Applied per
feature below.

| # | Roadmap feature | Groundable? | External anchor | A-priori verdict | Status |
|---|---|---|---|---|---|
| 1 | AND/OR dependency typing | YES — structural, from existing corpus | N/A (grounded on shared `produces` symbols — a graph-read of already-anchored outputs) | IMPLEMENT | **✅ implemented-and-gated** |
| 2 | PK/PD compartment engine | YES — canonical textbook equations | YES — anchored to ANZCA BT_GS 1.7 + exact math (ln2) | IMPLEMENT (anchored) | **✅ resolved — mostly-already-present + 1 new** |
| 3 | Measurement / device models | PARTIAL — first-order instrument response is canonical; drug-specific metrology is not | YES for first-order dynamics (τ, 63%); NO for invented device corpus | IMPLEMENT core, reject rest | **✅ implemented-and-gated (core) + rest evidenced-reject** |
| 4 | Populations state-space (joint distributions + covariance + provenance) | NO — needs real epidemiological covariance | NO — covariance structure would be invented | EVIDENCED-REJECT | **✅ evidenced-reject (council-confirmed)** |
| 5 | Coverage gaps (immunity, obstetric, paediatric, thermoreg, haemostasis, hepatic) | PARTIAL — a few have canonical equations (thermoregulatory heat balance, fetal/placental O₂), most are non-quantitative | YES for the few canonical ones | IMPLEMENT the anchored few, reject non-quantitative | **✅ implemented-and-gated (heat balance) + rest evidenced-reject** |
| 6 | Typed ensemble (algebraic/ODE/DAE + hybrid + compartmental + ontology + digital-twin + probabilistic) | PARTIAL — classifying each equation by mathematical FORM is structural/groundable; the digital-twin/ontology/probabilistic subsystems are research programs | YES for form-typing (proven by inspecting the compute/formula); NO for the subsystems | IMPLEMENT form-typing, reject subsystems | **✅ implemented-and-gated (form-typing) + subsystems evidenced-reject** |

## Cycle 2 — packaged-surface / e2e audit (2026-07-16)
Focus: exercise the actual **zip artifacts** (not the live tree). Extracted qp.zip
and qpm.zip to a clean dir and ran them as a user would.

**Verified sound (no finding):** qp.zip full `run_gate` GREEN *from the extracted
artifact*; qp doc-examples 26/26 and qpm SKILL 16/16 recipes execute against their
*packaged* code; qp↔qpm return **identical** values on shared equations (nernst
−94.97 mV, CO 4.9, MAP 93.33); extensions tier (instrument/thermo/pk) runs from the
zip; clean import (0 stderr) from both. Council gap-audit (3 families) confirmed no
higher structural gap (opus RANK 3: "no higher gap found").

**Accepted + fixed:**
- **[RANK 1, correctness/units] Stale Nernst comment** in `SKILL.md` Example Usage
  (both tiers): read *"compute() returns SI volts (output_units='V'); x1000 for mV"*
  — but `compute()` returns **−94.97 mV directly** (`output_units='mV'`), and the same
  block's inline note already said "output_units now mV". A user copying the ×1000
  guidance gets −94970 mV — a 1000× error in a clinically anchored value. Fixed to
  *"returns millivolts directly (output_units='mV') — no conversion needed"* in qp +
  qpm SKILL. (Executable line was already correct; doc-gate `expect -95.0` still holds.)
- **[RANK 2, integrity] qpm had no runnable self-check.** The minimal tier ships no
  test/gate, so a qpm user/CI could not verify an extracted copy. Added
  `qpm/scripts/smoke.py` (`python -m scripts.smoke`): dependency-free — clean import,
  canonical count 367, **Feher provenance on all 367** (source_chapter), external
  anchors (E_K −95, CO 4.9, MAP 93.3), `propagate()` fires 54 eqs → MAP 93.3, reasoning
  layers load. Documented in qpm SKILL. NOT added to qp (it has the full gate).

**Evidenced-(partial-)reject:**
- **qpm strips `references/` → "ungrounded / can't verify anchors"** (gemini+gpt). VERIFIED
  IN SOURCE: **all 367 qpm equations carry `source_chapter` metadata** (nernst→Feher 1.5,
  cardiac_output→5.3) — provenance is programmatically inspectable via `equation.metadata`;
  `references/` is redundant prose deliberately excluded per the user's minimal-tier design.
  gemini's "violates the iron rule, ungrounded runtime" is a category error (the runtime
  equations are grounded by their own metadata). Not re-added; the new smoke test asserts
  provenance coverage so inspectability is a checked property of the minimal tier.

**Second recursion pass:** the Nernst issue suggested a *class* (stale unit/return
comments); grepped all docs — no sibling contradiction. Spot-checked headline recipe
outputs (CO 4.9, EF 0.583, alveolar 100.0 mmHg) — all correct. **No actionable
high-severity finding remains.**

**Honest ceiling:** the packaged surface is behaving correctly and self-verifiably in
both tiers; remaining roadmap items (populations covariance, drug-specific PK, metrology,
digital-twin/ontology subsystems) stay evidenced-rejects — they need corpus that cannot be
grounded without fabrication, unchanged from Cycle 1.

Artifacts: qp.zip 514k, qpm.zip 303k; backups qp-v3.8-nernst-fix, qpm-v1.4-smoke-nernst.

## Integration mode (decided pre-integration)
`_build_canonical_ids.scan()` globs `scripts/**/*.py` and auto-collects every
module-level `AtomicEquation`, deriving the domain from the path — so a new-equation
module at `scripts/pk.py` would silently enter the canonical registry, invent a
`"pk"` domain, and ripple through `EQUATION_COUNTS` + every doc-count. The relational
layers (feedback/primitives/dependency_types) contribute **0** equations, which is
why Feature 1 was count-clean. Therefore Features 2/3/5 land as **definitional
compute-layers (plain-function modules + anchored tests)**, not canonical
`AtomicEquation`s: additive, gate-safe, the 367 SSOT untouched, and honestly labelled
as definitional identities *beside* the Feher corpus (provenance = standard
definition, not a Feher extract) — the same additive discipline as Feature 1. The
ultracode council loop drafts + vets them; the human integrator converts any
`AtomicEquation` the agents produced into plain functions before wiring the test in.

## Termination
Loop ends when every row is `implemented-and-gated` or `evidenced-reject`, and
the §4 gate is green on a clean regenerate.

## Run log
- (init) baseline gate GREEN — 367 eqs; primitives 47/7; feedback 7 loops.
- (init) council validated on known-good/known-bad: fabricated MPI → 3/3 REJECT
  (circular + dimensional caught); weakly-anchored MAP → 2/3 REJECT (ratchet
  enforced). Mechanism discriminates. grok-4.5 auth-down → gpt-5.6-terra seat.
- **Feature 1 (AND/OR typing) → implemented-and-gated.** `scripts/dependency_types.py`
  + `scripts/tests/test_dependency_types.py`, wired into `run_gate`. 4 OR-groups
  (CaO₂, CO, MAP, g_syn) structurally grounded on shared `produces` symbols; members
  typed by kind (definitional/approximation/measurement/model); 10 consumers whose
  flat `depends_on` conflates alternatives as AND surfaced dynamically. §4 gate GREEN.
  - Council: round1 0/3 (all flagged numeric-agreement circularity — CORRECT); I
    regrounded on shared symbols + honest kinds. round2 1/3. Two concrete rejects
    VERIFIED IN SOURCE and fixed: CaO₂ producers are the identical relation
    duplicated across domains → labelled `alias=True`; `map_from_flow` is the
    algebraic inverse of the SVR definition → note records conditional independence.
    round3 **2/3 APPROVE** (gemini+opus grounded=True).
  - Residual dissent (recorded, not obeyed): gpt-5.6-terra holds "registry-internal
    `produces` = circular" — a category error (reading graph structure ≠ asserting a
    new physiological value; the audit named these same alternatives on this basis),
    and asks for a *larger* feature (full prerequisite-closure satisfiability,
    per-consumer dimensional SVR-unit checks) than the bounded structural claim made.
    Deterministic §4 gate is the decider; it is green.
  - Deferred (gemini's "fix in the registry"): actually removing the redundant
    alternatives from consumers' flat `depends_on` is a corpus edit that changes the
    reachability graph — against the additive-only discipline and risky (cf. the
    propagate hijack history). The additive corrective layer is the sanctioned
    pattern (as with `feedback.py`/`primitives.py`); a corpus refactor is future work.
- **ultracode Workflow launched** (`scripts/roadmap_workflow.js`, run wf_7e5cdaac-5b7):
  4 definitional/structural pipelines (F6 form-typing, F2 PK, F3 instrument, F5 thermo)
  each draft→council→refine, + the F4 evidenced-reject dossier. Guardrail: draft agents
  may commit only definitional/exact-math/structural content; any new numeric value is
  deferred to `needs_source` for human PageIndex/Feher verification, never invented.
- **PK source-verified** (prep for F2 integration): ANZCA BT_GS 1.7 (PageIndex) confirms
  C=C₀·e^(−kt); k=ln2/t½=1/τ; C₀=dose/Vd; CL=Vd·k=Vd/τ; 2-cpt C=A·e^(−αt)+B·e^(−βt),
  Vd=V1+V2. Real citable anchor for the F2 definitional relations. Thermoregulation
  heat-transfer mechanisms have a matching note (ANZCA BT_GS 1.65) for F5.
- **Workflow returned (13 agents, 0 errors).** Every module independently re-run and
  read for grounding by the human integrator (agent self_check ≠ trusted):
  - **F6 form-typing** `scripts/eqforms.py` — 367/367 classified into 6 structural forms
    on two independent grounds (primitive execution + formula marker); 0 canonical-count
    change (like Feature 1). Council self-corrected 2 overclaims (renamed `power_law`→
    `power_term` to drop a false scaling claim; removed `feedback_member` as a role not a
    form). **implemented-and-gated.**
  - **F2 PK** `scripts/extensions/pk.py` — the agent's honest finding: **7 of 8 drafted PK
    equations already exist in the corpus** (verified by source match-by-concept:
    apparent_volume_of_distribution, elimination_rate_constant, clearance, hormone_half_life,
    first_order_elimination, maintenance_infusion_rate, loading_dose). Kept only the 1 genuinely-
    new relation, `time_to_steady_state = n·t½`; removed an unsourced `n=5` default (n now
    caller-supplied). No padding. **resolved.**
  - **F3 instrument** `scripts/extensions/instrument.py` — 6 exact-math forms (1−e^(−t/τ),
    τ·ln9, 20·log10, √(k/m), c/2√(km)); NEEDS_SOURCE defers all device-specific numbers;
    fixed a real dimensional defect (dB→dimensionless). **core implemented-and-gated.**
  - **F5 thermo** `scripts/extensions/thermo.py` — 5 definitional heat-balance relations;
    `heat_storage` (S=M−W±R±C±K−E) source-checked as NOT a duplicate of `body_energy_balance`;
    Fourier conduction verified absent from corpus; all empirical coefficients uncommitted,
    only σ (exact post-2019 SI). **core implemented-and-gated.**
  - **F4 populations** — council-reviewed **evidenced-reject**: a covariance structure is
    numbers (marginals + pairwise correlations) absent from Feher; inventing them (or
    per-equation ×multipliers) violates the iron rule. Groundable subset noted:
    `Parameter.physiological_range` already encodes per-parameter bounds.
- **Integration engineering:** the 3 new-equation modules (pk/instrument/thermo) each defined
  module-level `AtomicEquation`s and instrument.py self-registered — which would have pushed
  the canonical scan to 379 with phantom `pk`/`instrument`/`thermo` domains. Moved them to a
  new **`scripts/extensions/`** tier (excluded from `_build_canonical_ids`/`generate_graph`
  scans; register_equation stripped): rich, usable AtomicEquations that are explicitly
  *beyond-Feher* and leave the canonical **367 untouched**. §4 gate GREEN, idempotent.
  SKILL Recipes I (form-typing) + J (extensions) added; doc gate 26/26.

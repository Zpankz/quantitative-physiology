---
type: obsidian-voice-orthogonal-context
status: extracted
created: 2026-07-16
source_vault: /Users/mikhail/Obsidian/pex-clean
canonical_qp_equation: false
qpm_runtime_content: false
lanes:
  - definitions
  - schemas
  - diagrams
  - equation-synthesis
---

# Obsidian voice context: definitions, schemas, diagrams, and equation synthesis

This is retrieval context for the Obsidian voice plugin, adjacent to `qp` but not part of its canonical equation registry. It preserves what the live sessions and linked vault artifacts actually establish; it does not repair gaps with generic medical prose.

## Provenance legend

- **Verbatim extraction**: source wording, quoted or structurally transcribed without changing its claim.
- **Faithful normalization**: shortened or reorganized source content without adding a medical claim.
- **Inference**: an integration decision derived from the sources, not evidence for a medical answer.
- **Session-only**: useful dialogue or design intent that the session itself says is not backed by a retrieved textbook passage. Never present this as canonical evidence.
- **Assumed (external standard)**: a widely-standard value or relation applied to interpret a source but **not stated in it** (e.g. 0.9% saline chloride concentration, the numeric albumin–anion-gap correction). Must be flagged as assumed; never presented as session evidence.

## Source map

| Key | Local source | Stable anchor | Role |
|---|---|---|---|
| `HELLO` | `/Users/mikhail/Obsidian/pex-clean/ops/sessions/2026-07-15/Hello..md` | lines 21–27, 40–76, 77–137, 139–180 | Retrieval-heavy live session; definition example and requested knowledge-stack design. |
| `AP26-TX` | `/Users/mikhail/Obsidian/pex-clean/ops/sessions/2026-07-15/Please-create-a-canvas-on-AP26A03..md` | lines 17–108 and tool timeline lines 110–151 | Live canvas iteration and the user's geometry/synthesis requirements. |
| `AP26-CANVAS` | `/Users/mikhail/Obsidian/pex-clean/ops/sessions/2026-07-15/Please-create-a-canvas-on-AP26A03..canvas` | node ids `root`, `branchC`, `branchA`, `a_mech`, `branchB`, `b_lung`, `b_other`; edge ids `e1`–`e6` | Current deterministic graph, including coordinates and explicit edge sides. |
| `AP26-SAQ` | `/Users/mikhail/Obsidian/pex-clean/sources/saq/ANZCA/AP26A/AP26A03.md` | frontmatter lines 2–31 | Authoritative local question, linked learning objectives, expected domains, and examiner errors. |
| `LO-PREOX` | `/Users/mikhail/Obsidian/pex-clean/sources/lo/ANZCA/E_respiratory-system/E2_respiratory-physiology/APE2xxix_preoxygenation.md` | frontmatter lines 2–18 | Preoxygenation learning-objective scope. |
| `LO-GAS` | `/Users/mikhail/Obsidian/pex-clean/sources/lo/ANZCA/E_respiratory-system/E2_respiratory-physiology/APE2xvi_composition-ideal.md` | frontmatter lines 2–12 | Ideal alveolar and mixed-expired gas composition scope. |
| `LO-FRC` | `/Users/mikhail/Obsidian/pex-clean/sources/lo/ANZCA/E_respiratory-system/E2_respiratory-physiology/APE2xiv_lung-volumes.md` | frontmatter lines 2–23 | Lung-volume/capacity scope, including normal values. |
| `LO-O2` | `/Users/mikhail/Obsidian/pex-clean/sources/lo/ANZCA/E_respiratory-system/E2_respiratory-physiology/APE2xxiv_carriage-oxygen.md` | frontmatter lines 2–41 | Oxygen carriage and blood-store scope. |
| `TEMPLATE` | `/Users/mikhail/Obsidian/pex-clean/templates/knowledge-integration-template.md` | headings/fields at lines 9–71 | Note schema created during the live `HELLO` session. |
| `QP-README` | `/Users/mikhail/Downloads/qp/README.md` | lines 3–26, 43–57, 66–72 | Current qp count, tiers, reasoning layers, and grounding boundary. |
| `STEWART` | `/Users/mikhail/Obsidian/pex-clean/ops/sessions/2026-07-15-stewart-acid-base-live.md` | exam-safe set lines 44–54; claim audit 60–82; higher-order 86–96; final spine 104–115 | Audited live-teaching synthesis of the Stewart strong-ion approach, reconciled against Kam & Power ch. 50 and CICM examiner report CP23A01. Its own claim audit distinguishes supported wording from transcript errors. |

`HELLO` and `AP26-TX` are the latest transcripts found for the requested knowledge-stack and AP26A03 canvas work. The older AP26A03 session at `ops/sessions/session-mr5wb8nl-x3ctla-1.md` was not used: it predates these smoke sessions, lacked PageIndex access, and contains duplicated streaming partials rather than stronger evidence.

## Definitions

### `DEF-001` — clearance example, raw attempt

- **Extract:** “clearance is the volume of substance cleared per unit time from either the plasma or the blood.”
- **Provenance:** verbatim extraction; learner attempt; session-only.
- **Anchor:** `HELLO` line 45.
- **Use:** misconception-aware tutoring only. Do not retrieve this as the accepted definition.

### `DEF-002` — clearance example, corrected session wording

- **Extract:** clearance is a hypothetical volume of plasma completely cleared of drug per unit time, not an amount of drug and not a physical volume removed from the circulation.
- **Units stated by the session:** volume per unit time; no named unit is supplied.
- **Validity condition stated by the session:** treating clearance as constant is limited to linear, first-order kinetics; it is not universally constant.
- **Provenance:** faithful normalization; examiner dialogue; session-only because the examiner explicitly says a clean cited textbook definition was not retrieved.
- **Anchors:** `HELLO` lines 50–52 and 70–76.
- **Use:** retrieval should carry the `session-only` warning until a prescribed-text definition is linked.

### `DEF-003` — definition-library contract

- **Extract:** collect terms previously asked as definitions from past SAQs and learning objectives; retain varying prescribed-text definitions; synthesize a consensus definition broad enough to cover them but precise enough to preserve nuance.
- **Required fields:** canonical definition with citation; alternatives with citations; consensus; units/terms; pitfalls.
- **Provenance:** faithful normalization of user design intent plus the resulting template.
- **Anchors:** `HELLO` lines 77–82; `TEMPLATE` lines 21–26.
- **Use:** schema for future extraction, not itself a medical definition.

### `DEF-STEW-001` — strong ion difference: SIDa, SIDe, SIG (definition + equation faces)

Merges workflow findings F1 + F2 + F3; re-checked against the Stewart transcript.

- **Category rule (the central correction):** strong ions are treated as fully dissociated at physiological pH and carry *measured* charge; bicarbonate, albumin and phosphate are **weak / dependent** buffer ions and are **never** counted among the strong ions. Folding them into "the strong ion difference" without the a/e/g suffix is the recurrent category error.
- **Apparent SID** (from measured strong ions):
  `SIDa = ([Na⁺] + [K⁺] + 2[Ca²⁺] + 2[Mg²⁺]) − ([Cl⁻] + [lactate⁻] + other measured strong anions)`.
  Divalent cations are **charge-weighted (×2)** when concentrations are in mmol/L; at the bedside Na⁺ and Cl⁻ dominate numerically.
- **Effective SID** (from measured dependent buffer anions): `SIDe = [HCO₃⁻] + albumin charge + phosphate charge`.
- **Strong ion gap:** `SIG = SIDa − SIDe`. A positive SIG estimates **unmeasured anionic charge** (e.g. ketoanions).
- **Normal value / condition:** SIDa is conventionally about **40–44 mEq/L** in the prescribed text; the exact figure depends on which measured ions and units are included (convention-dependent).
- **Measured-panel / lactate double-counting guard:** "unmeasured" is defined relative to the chosen panel. When lactate is measured it belongs in SIDa and must **not** simultaneously be named a SIG anion; it behaves as an omitted charge only in a simplified Na−Cl calculation. State the formula before naming the residual.
- **Provenance:** Faithful normalization (source-supported; the session's own claim audit reconciles the spoken wording to these examiner-safe forms and flags the SIDe/unmeasured-anion confusion as an error).
- **Anchors:** `STEWART` lines 44–50 (exam-safe working set), 52–53 (normal range, SIG, lactate), 68 (divalent charge-weighting), 69–70 (SIDa/SIDe/SIG category rule), 71–72 and 101 (lactate double-count closure).
- **Uncertainty:** no numeric SID convention beyond ~40–44 mEq/L is supplied; albumin and phosphate charge are not quantified in the transcript.

### `DEF-STEW-002` — intravenous fluid SID effects

Workflow finding F5; re-checked against the transcript.

- Saline (0.9% NaCl) delivers a high relative chloride load, **lowers SID**, and can produce or worsen **hyperchloraemic non-anion-gap acidosis**.
- Balanced crystalloids deliver less chloride plus metabolizable anions: **Plasma-Lyte ~98 mmol/L Cl⁻**; **Hartmann's ~109–112 mmol/L Cl⁻** (product-dependent).
- Sodium bicarbonate is **chloride-free sodium**: added Na⁺ without Cl⁻ **raises SID** and lowers dependent [H⁺] (bicarbonate remains a real dependent buffer; clinical use is still limited by CO₂ generation, Na/osmotic load and ionised-Ca²⁺ reduction).
- Giving albumin to a hypoalbuminaemic patient **raises Aₜₒₜ** and shifts pH acidward by reversing hypoalbuminaemic alkalosis; the product's own chloride/SID matters, so name the formulation.
- **Coupling caveat (condition):** the acid–base effect depends on the fluid's **effective SID after metabolism and its dose/distribution**, not on chloride concentration alone.
- **Provenance:** Faithful normalization.
- **Anchors:** `STEWART` lines 74 (lower-Cl fluid widens the Na−Cl gap), 75 (albumin), 76 (NaHCO₃ raises SID), 77 (saline hyperchloraemia; Plasma-Lyte ~98; Hartmann's ~109–112), 95 (post-metabolism effective SID).
- **Assumed (external standard):** 0.9% saline [Cl⁻] ≈ 154 mmol/L is standard knowledge, **not stated in this transcript**.

### `DEF-STEW-003` — Stewart versus Henderson–Hasselbalch

Workflow finding F6; re-checked against the transcript.

- Both frameworks must satisfy the **same solution chemistry**; they are not rival empirical realities.
- **Henderson–Hasselbalch** is a valid **equilibrium description** of the CO₂/HCO₃⁻ system; by itself it does **not uniquely decompose** the *metabolic* causes of a bicarbonate change.
- **Stewart** is a **choice of independent variables** (PaCO₂, SID, Aₜₒₜ) for **causal decomposition**; its diagnostic gain is exposing opposing SID/Aₜₒₜ/PaCO₂ effects that a single bicarbonate label compresses.
- **Examiner-safe asymmetry (do not overstate):** never claim one equation is chemically valid and the other invalid — HH is an equilibrium relationship; Stewart is a causal-decomposition choice.
- **Provenance:** Faithful normalization.
- **Anchors:** `STEWART` lines 63 (HH critique, bounded), 86–88 (higher-order asymmetric framing), 113 (final-spine reconciliation).

## Schemas and structured contracts

### `SCHEMA-001` — orthogonal knowledge-stack lanes

The session explicitly separates **definitions**, **classifications**, **diagrams**, **equations**, **values**, **schemas**, and **comparisons**, with examiner nuance layered across them. The schema is intended to synthesize syllabus decomposition, concepts, equations-as-formulaic schemas, and examiner comments that can be formalized as true/false statements.

- **Provenance:** faithful normalization.
- **Anchors:** `HELLO` lines 77–115 and 121–129.
- **Boundary:** these are peer retrieval lanes. One lane must not silently become another; for example, a canvas label is not equation evidence and a learner definition is not a prescribed-text definition.

### `SCHEMA-002` — topic record

| Block | Required content | Source anchor |
|---|---|---|
| Topic identity | name, learning objectives, SAQ codes, tags | `TEMPLATE` lines 9–13 |
| Evidence | primary texts, exam references, local links, verbatim citations | `TEMPLATE` lines 15–19 |
| Definition | canonical, alternatives, consensus, units, pitfalls | `TEMPLATE` lines 21–26 |
| Classification | categories and inclusion/exclusion criteria | `TEMPLATE` lines 28–31 |
| Diagram | type, purpose, source asset, canvas ids, interpretation | `TEMPLATE` lines 33–38 |
| Equation | cited relation, variables/units, dimensional check, dependencies, validity | `TEMPLATE` lines 40–45 |
| Values and comparisons | cited ranges/doses/volumes, caveats, similarities/differences | `TEMPLATE` lines 47–55 |
| Schema and examiner nuance | syllabus/concept decomposition, cross-lane links, expected domains, errors, true/false statements | `TEMPLATE` lines 57–66 |
| Gaps | missing content, next sources, review date | `TEMPLATE` lines 68–71 |

- **Provenance:** verbatim structural transcription of headings and fields.

### `SCHEMA-003` — AP26A03 response contract

1. State values for graph points A and B, then explain their underlying physiology.
2. Describe the effect of preoxygenation on total body oxygen stores.
3. Explicitly link the Part A wash-in/alveolar reasoning to the Part B store changes.
4. Explain why end-tidal oxygen cannot reach 100%; reproducing the alveolar gas equation alone is insufficient.
5. Contrast the major lung/FRC oxygen-volume change with the small additional blood, myoglobin, and dissolved-tissue stores.
6. Do not quote an unsafe apnoea time; the report identifies values greater than eight minutes as unacceptable examples.

- **Provenance:** faithful normalization of the local SAQ note and current canvas.
- **Anchors:** `AP26-SAQ` lines 2–6, 15–31; `AP26-CANVAS` nodes `branchC`, `branchA`, `a_mech`, `branchB`, `b_lung`, `b_other` and edges `e1`–`e6`.
- **Uncertainty:** the source does not provide numeric A/B values, a complete alveolar gas equation, FRC volume, oxygen-store quantities, or a positive safe-apnoea range. They remain gaps.

### `SCHEMA-STEW-001` — independent/dependent variables and the directional spine

Workflow finding F4; re-checked against the transcript.

- **Governing laws:** electroneutrality, mass action, conservation of mass.
- **Independent variables:** PaCO₂, strong ion difference (SID), total weak acids (Aₜₒₜ).
- **Dependent variables:** H⁺, OH⁻, HCO₃⁻ ("dependent" does not mean unimportant, unmeasurable or absent).
- **Directional spine:**

  | Lever | Acidifies when | Alkalinises when |
  |---|---|---|
  | SID | ↓ | ↑ |
  | Aₜₒₜ | ↑ | ↓ |
  | PaCO₂ | ↑ (respiratory acidosis) | ↓ (respiratory alkalosis) |

- **Decomposition role:** PaCO₂ explains respiratory disturbances; SID and Aₜₒₜ decompose metabolic disturbances. Water gain/loss co-varies SID and Aₜₒₜ, so interpret dilution/contraction as **coupled** effects, not a fourth independent variable.
- **Provenance:** Faithful normalization.
- **Anchors:** `STEWART` lines 36–40 (examiner contract, laws + variables + directions), 54 (directional spine), 66 and 91 (water co-varies levers), 108–112 (final-spine variable roles).

### `SCHEMA-STEW-002` — Gamblegram and the albumin-corrected anion gap

Workflow finding F7; re-checked against the transcript.

- **Anion gap:** `AG = [Na⁺] − ([Cl⁻] + [HCO₃⁻])`, with K⁺ optional; normal ~**8–16 mmol/L**, **lab/convention-dependent** (state whether K⁺ is included and use the reporting laboratory's range). The gap is unmeasured anions minus unmeasured cations, **not** a real charge imbalance.
- **Composition of the normal gap:** albumin is usually the dominant unmeasured anion; phosphate contributes less.
- **Hypoalbuminaemia trap:** low albumin **lowers the expected AG** *and* independently **alkalinises** (reduced Aₜₒₜ), so a normal-looking uncorrected AG can conceal pathological unmeasured anions. Correct the AG for albumin, or use SID/SIG.
- **Gamblegram:** a two-column measured-cation / measured-anion charge diagram; the apparent gap is **filled by unmeasured charges** to preserve electroneutrality — it is not empty electrical space. The a/e/g suffixes prevent the category error: apparent = measured strong ions; effective = measured dependent buffer anions; gap = missing charge.
- **Provenance:** Faithful normalization.
- **Anchors:** `STEWART` lines 60–62 (AG formula/range, composition, Gamblegram), 81 and 90 (albumin correction, not cosmetic), 92 (a/e/g category aid).
- **Assumed (external standard):** the common **numeric** albumin correction (≈ 0.25 mmol/L per g/L albumin below ~40 g/L, i.e. ~2.5 mmol/L per 10 g/L deficit) is external standard knowledge and is **not stated in this transcript**. The workflow critique's "2.5 × (40 − albumin)" is that per-10-g/L convention; it is retained here only as a flagged assumption, not session evidence.

## Diagrams and canvas structures

### `DIAGRAM-001` — AP26A03 synthesis-first hierarchy

Load the canvas itself for geometry; do not reconstruct it from this summary.

| Node id | Role | Position `(x, y)` | Size `(w × h)` |
|---|---|---:|---:|
| `root` | AP26A03 core concept | `(77, -620)` | `276 × 80` |
| `branchC` | integration/pitfalls; link A to B | `(104, -436)` | `222 × 108` |
| `branchA` | Part A: graph values and physiology | `(-243, -274)` | `220 × 108` |
| `a_mech` | wash-in and alveolar context | `(-243, -60)` | `220 × 108` |
| `branchB` | Part B: oxygen stores | `(453, -274)` | `240 × 80` |
| `b_lung` | major lung/FRC store | `(233, -46)` | `220 × 80` |
| `b_other` | small blood/myoglobin/dissolved stores | `(600, -60)` | `267 × 108` |

| Edge id | Exact relation | Attachment contract |
|---|---|---|
| `e6` | `root` → `branchC` (`Synthesis`) | bottom → top |
| `e1` | `branchC` → `branchA` (`Question part`) | left → top |
| `e3` | `branchC` → `branchB` (`Question part`) | right → top |
| `e2` | `branchA` → `a_mech` (`Explain`) | bottom → top |
| `e4` | `branchB` → `b_lung` (`Main store`) | bottom → top |
| `e5` | `branchB` → `b_other` (`Minor stores`) | bottom → top |

- **Provenance:** verbatim structural extraction from `AP26-CANVAS`.
- **Integrity rule:** all retrieval or transformation must preserve node ids, edge ids, coordinates, sizes, labels, and `fromSide`/`toSide` unless a later canvas revision explicitly supersedes them.

### `DIAGRAM-002` — layout semantics demonstrated by that canvas

- Put the synthesis/opening statement above the question parts; fan Part A left and Part B right.
- Within a branch, order major before minor from left to right where the geometry permits.
- Choose attachment sides facing the neighbouring node and minimize connector distance.
- Balance sibling geometry, leave space for edge text, and prefer a hierarchical fan-out over a high-degree hub.
- Treat coordinates and edge sides as deterministic file data, not an uncontrollable display artifact.

- **Provenance:** faithful normalization of user corrections, confirmed by the final canvas JSON.
- **Anchors:** `AP26-TX` lines 34–47, 48–65, 72–100; `AP26-CANVAS` nodes `root`, `branchC`, `branchA`, `branchB`, `b_lung`, `b_other` and edges `e1`, `e3`–`e6`.

### `DIAGRAM-STEW-001` — causal directional spine (diagram-ready)

No `.canvas` asset exists for this yet; this is a **diagram-buildable spec** derived from the transcript's directional spine, not a placed canvas.

Nodes — three independent variables driving the dependent outputs:

| Node | Role |
|---|---|
| PaCO₂ | independent (respiratory) |
| SID | independent (metabolic) |
| Aₜₒₜ | independent (weak acids) |
| pH / [H⁺], HCO₃⁻, OH⁻ | dependent outputs |

Directed edges (with sign):

- `PaCO₂ ↑ → acidosis`, `PaCO₂ ↓ → alkalosis`
- `SID ↓ → acidosis`, `SID ↑ → alkalosis`
- `Aₜₒₜ ↑ → acidosis`, `Aₜₒₜ ↓ → alkalosis`

Constraint node: **electroneutrality + mass action + conservation of mass** gate all three levers onto the dependent variables *simultaneously* — do not narrate H⁺ appearing in isolation to plug a charge gap.

- **Provenance:** Faithful normalization (diagram-ready structure built from the directional spine; the source supports the nodes, signs and constraint).
- **Anchors:** `STEWART` lines 39 (directional mechanisms), 54 (spine), 89 (equilibrium adjusts simultaneously), 108–112 (final spine).
- **Integrity rule:** this is a logical spec, not placed geometry; if rendered to a canvas, preserve the three-independent→dependent direction and the exact sign map.

### `DIAGRAM-STEW-002` — Gamblegram / charge bookkeeping (diagram-ready)

Two-column electroneutrality bar over the **measured** ions, diagram-buildable:

| Cations (measured) | Anions (measured) |
|---|---|
| Na⁺ (dominant), K⁺, Ca²⁺, Mg²⁺ | Cl⁻ (dominant), HCO₃⁻, lactate⁻ (when measured) |

Closing terms:

- The **anion gap** closes the *measured* columns; the residual is filled by **unmeasured anions** (albumin charge, phosphate, ketoanions …) minus unmeasured cations — electroneutrality is preserved, the gap is not empty space.
- **SIG = SIDa − SIDe** is the Stewart analogue of that unmeasured-anion residual; do **not** double-count measured lactate as both a column entry and the residual.

- **Provenance:** Faithful normalization.
- **Anchors:** `STEWART` lines 45 (strong-ion columns), 49 (SIDe buffer anions), 62 (Gamblegram preserves electroneutrality), 69 (SIG), 71–72, 92, 101 (residual/lactate guard).
- **Integrity rule:** columns represent charge equivalents, so charge-weight divalents when in mmol/L; the residual is defined by what the chosen panel already counted.

## Equation synthesis and integrative reasoning

### `EQ-SYN-001` — clearance/elimination relationship, incomplete source form

- **Source relationship:** the dialogue distinguishes clearance as a capacity-like volume/time term from elimination as amount/time and says concentration changes elimination rate; clearance is only assumed constant under linear, first-order kinetics.
- **Symbols and numerical equation:** not supplied by the transcript.
- **Units supplied:** clearance = volume/time; elimination = amount/time; concentration is named but its units are not.
- **Provenance:** faithful normalization; session-only.
- **Anchors:** `HELLO` lines 55–76.
- **Do not infer:** no symbolic equation, proportionality constant, compartment model, or dosing relation should be generated from this item alone.

### `EQ-SYN-002` — AP26A03 causal join

The evidence-backed synthesis is structural rather than a complete calculation:

`100% inspired oxygen` → `wash-in / alveolar context` → `A and B end-tidal values remain below 100%` → `large change in lung/FRC oxygen store` → `small additional blood, myoglobin, and dissolved-tissue stores`.

- **Dependency contract:** an answer must join the graph-value explanation in Part A to the oxygen-store accounting in Part B. Memorized FRC figures without that link are explicitly criticized.
- **Named but absent equation:** alveolar gas equation. The source requires explanation beyond merely reproducing it but does not include its formula, variables, units, or assumptions.
- **Provenance:** faithful normalization of the SAQ expected domains/errors and canvas edges.
- **Anchors:** `AP26-SAQ` lines 15–29; `AP26-CANVAS` nodes `branchC`, `a_mech`, `b_lung`, `b_other` and edges `e1`–`e6`.

### `EQ-SYN-003` — qp relationship without registry contamination

The user asks for a queryable equation graph with dimensions and relations between equations. `qp` already supplies declared parameters, units, dependencies, a dependency DAG, forward propagation, typed dependencies, mathematical forms, and feedback loops.

- **Provenance:** faithful normalization of `HELLO` lines 85–103, grounded against current `QP-README` lines 3–8 and 43–57.
- **Inference:** the future plugin should query qp for canonical quantitative relations and retrieve this file only for orthogonal definitions/schema/diagram/synthesis context.

## Plugin integration contract

1. Expose this document as a read-only context source named `orthogonal-context`; retrieval filters by lane and item id (`DEF-*`, `SCHEMA-*`, `DIAGRAM-*`, `EQ-SYN-*`).
2. Return the item body together with its provenance class, uncertainty/gaps, and every local source anchor. Session-only items must be visibly labeled and cannot satisfy a request for prescribed-text evidence.
3. Resolve diagram requests to the `.canvas` path plus node/edge ids. Load geometry from the canvas JSON; never replace it with prose-generated topology.
4. Keep this context outside imports and generated artifacts for both `qp/` and `qpm/`. It does **not** add to, merge with, or alter the current 367 canonical equations.
5. Any future equation promoted from this context must enter through qp's normal independently grounded authoring and acceptance gate. Until then, absent formulae, symbols, units, or assumptions remain explicit gaps.
6. Do not copy this file into the qpm runtime tier. The plugin may retrieve it alongside qpm results, but qpm stays the identical minimal 367-equation runtime described by `QP-README` lines 18–26.
7. Prefer additive context composition: canonical qp result + separately cited orthogonal item(s). Never overwrite a canonical equation's provenance with a transcript or canvas anchor.

## Unresolved evidence gaps

- No prescribed-text clearance definition was retrieved in the live session.
- No symbolic clearance–elimination equation is present in the selected transcript.
- AP26A03 supplies no numeric A/B values, full alveolar gas equation, store quantities, or positive safe-apnoea range.
- The linked learning-objective notes provide scope only; they do not fill those quantitative gaps.
- The AP26A03 canvas encodes structure and relative importance, not a complete model answer.
- The Stewart session supplies no numeric SID convention beyond the ~40–44 mEq/L prescribed-text range, and does not quantify albumin or phosphate charge.
- The numeric albumin correction for the anion gap is **not** stated in the Stewart transcript; any coefficient (e.g. ~2.5 mmol/L per 10 g/L) is an external assumption, flagged in `SCHEMA-STEW-002`, not session evidence.
- The full Story/Fencl base-excess decomposition is named as an application in the transcript (attributed to David Story) but its complete equation, terms and units are not reproduced; promoting it would require the same independently-grounded authoring as any qp equation.

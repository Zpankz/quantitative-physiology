# qp — Quantitative Human Physiology

A tested, importable library of the reusable quantitative models from Feher's
*Quantitative Human Physiology, 3rd ed.*, built for CICM / ANZCA Primary Exam
reasoning — spanning cardiovascular, respiratory, renal, membrane, endocrine and
cross-cutting acid–base physiology (Henderson–Hasselbalch, anion gap, Stewart
strong-ion difference). Every equation is an `AtomicEquation` object — a compute function with
declared parameters, units, dependencies, and Feher provenance — not just a formula
in prose. The value is not a bag of equations but an **integrated, queryable
network**: seed a few bedside numbers and the graph fills in the rest.

**367 canonical equations** across 9 domains:

| Domain | n | Domain | n | Domain | n |
|---|---|---|---|---|---|
| foundations | 38 | membrane | 30 | excitable | 29 |
| nervous | 36 | cardiovascular | 58 | respiratory | 62 |
| renal | 42 | gastrointestinal | 41 | endocrine | 31 |

## Two tiers

- **`qp/`** — the full skill: the 367 equations, the reasoning layers, the
  beyond-Feher `extensions/` tier, the reference docs, the test suites, and a
  single deterministic acceptance gate.
- **`qpm/`** — a minimal runtime tier: the same 367 equations + reasoning layers,
  no tests/gate/references, plus a dependency-free integrity self-check.

Both tiers return **identical values** on shared equations.

## Quickstart

```python
from scripts.foundations.thermodynamics import nernst_equation
nernst_equation.compute(z=1, C_out=4, C_in=140)   # -95.0  (mV — output_units='mV')

# Integrative simulation: seed the bedside numbers, read the whole state
from scripts.eqgraph import build_graph
g = build_graph()
r = g.propagate(dict(HR=80, SV=65, EDV=120, ESV=55, Hb=14, S_O2=0.97,
                     P_O2=95, P_50=26.8, n=2.7, SBP=125, DBP=78))
f = r["fired"]                       # {equation_id: value}, 60+ entries
f["cardiac_output"], f["mean_arterial_pressure"]   # CO and MAP fall out
```

## Reasoning layers (the network, not just the atlas)

- **`eqgraph`** — dependency DAG + `propagate()` forward-chaining integrative
  simulation, dimensional coupling and inference.
- **`primitives`** — ~7 universal kernels (log-ratio, saturation, first-order,
  linear-flux, …); 47 execution-proven memberships showing disparate equations
  (Nernst ≡ Henderson-Hasselbalch ≡ Gibbs; Michaelis-Menten ≡ Hill) are one form.
- **`feedback`** — 7 physiological feedback loops (baroreflex, HPA/HPT axes, TGF …)
  represented beside the acyclic DAG; the endocrine axes are formula-verified.
- **`dependency_types`** — AND/OR dependency typing: which inputs are jointly
  required vs substitutable alternatives (e.g. cardiac output by any of three methods).
- **`eqforms`** — every equation classified by mathematical form on two independent
  grounds.
- **`extensions/`** — definitional relations *beyond* Feher (instrument response,
  thermoregulation heat balance, PK timing), a tier separate from the canonical 367.

## Verify

```bash
cd qp  && python -m scripts.run_gate   # full gate: idempotence + all suites + docs + integration
cd qpm && python -m scripts.smoke      # minimal-tier integrity check
```

## Grounding discipline

Every value is executable and anchored to an independent external reference, never
a circular self-test. Additions are additive (no equation collapsed or deleted);
anything that cannot be grounded without fabricating corpus is recorded as an
evidenced rejection rather than stubbed. See `qp/ROADMAP_LEDGER.md` and
`qp/QPM_ASSESSMENT.md`.

## Orthogonal context

[`context/obsidian-voice-context.md`](context/obsidian-voice-context.md) is a
separate, provenance-labelled retrieval artifact for an Obsidian voice plugin:
definitions, schemas, diagrams, and equation-synthesis notes extracted from live
teaching sessions and vault sources (e.g. the Stewart strong-ion acid-base
approach). Each item carries its source anchor and a provenance class
(extracted / inferred / assumed / session-only), with uncertainty preserved.

It is deliberately **outside** the canonical registry — it does not add to,
merge with, or alter the 367 equations, and is never imported by `qp/` or `qpm/`.
Anything promoted from it must re-enter through qp's normal grounded authoring and
acceptance gate.

*Source: Joseph J. Feher, Quantitative Human Physiology: An Introduction, 3rd ed.*

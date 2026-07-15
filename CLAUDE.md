# `qp` — coverage guide

The `quantitative-physiology` package (`qp`) collects the reusable quantitative
models from Feher's _Quantitative Human Physiology, 3rd ed._ as tested, importable
`AtomicEquation` objects. The goal of this guide is complete coverage: every
reusable equation in the book is either represented in the package or recorded as
out of scope with a reason, and the test gate stays green.

You have the `qp` package on disk, a Python shell, and a **PageIndex** MCP tool
that exposes the Feher corpus. This is a Claude Code project; the workflow below is
plain Python plus the MCP tool and doesn't depend on any particular harness.

### File map (read both)
This guide is split across two files:
- **this file** (`CLAUDE.md`, workspace root) — the coverage workflow: what "done"
  means, the accuracy practices, the algorithm, orchestration, loop, deliverable.
- **`qp/CLAUDE.md`** (package root) — the code-local reference: package shape and
  the authoring contract (§2), and the acceptance gate (§4). Keep it open with the
  code.

Claude Code auto-loads `qp/CLAUDE.md` when you work in the package. Section numbers
are continuous across both files; §2 and §4 live there.

---

## 0. What "done" means

The acceptance gate in §4 is the definition of a correct package. The workflow is:

> enumerate the corpus → extract candidate equations → diff against the registry
> → implement the genuine gaps → run the gate → repeat until the gate is green
> **and** the coverage ledger accounts for every reusable equation in every
> enumerated section.

Coverage is complete when **every Feher section has a ledger entry, every reusable
equation in those sections is either implemented-and-tested or
explicitly-excluded-with-a-written-reason, and the gate passes on a clean
regenerate.** If that isn't yet true, report exactly what remains rather than
rounding up to "complete."

---

## 1. Accuracy practices

These matter more than throughput — the package is only useful if its contents and
its status reports are trustworthy.

1. **Record accurate provenance.** Feher's extracts preserve section/equation
   numbers (e.g. `5.11`, `7.6.4`) but not book page numbers. When you don't have a
   real page number, set `page_reference=None` rather than guessing one. Cite the
   section you actually read.
2. **Verify before reporting.** Report tests as passing only after running them in
   this session and reading the output — don't infer or extrapolate results. After
   editing code, re-run the gate before describing its state.
3. **Classify carefully; don't pad.** Feher numbers ~1000+ equations; most are
   derivation steps, worked-example arithmetic, or intermediate algebra, not
   reusable models. Classify every candidate (§3.2) and add only genuine reusable
   models — padding the count works against the package's purpose.
4. **Report coverage as measured.** The final report states the fraction of
   enumerated sections processed and the concrete gap list. If you audited 40 of 80
   sections, say "40/80", not "complete".
5. **Note when you narrow a section's scope.** If a section is non-quantitative
   (e.g. Feher §5.4 Inflammation), record it as "no reusable equations" rather than
   forcing one.
6. **Keep the gate strict.** If a real equation can't satisfy an invariant, fix the
   equation or flag it — don't relax the test to make it pass.

---

## 2. Ground truth: the `qp` package  → `qp/CLAUDE.md`

The package shape (**§2.1**) and the equation authoring contract (**§2.2**) live in
`qp/CLAUDE.md` at the package root — you need them with the code open. **Read that
file before authoring any equation.** Rule of thumb it encodes: read the package
before touching it, and where this summary and the code disagree, the code wins and
you update your model.

---

## 3. The coverage algorithm

### 3.1 Enumerate (PageIndex)
1. Orient: get the Feher corpus tree. Feher lives under
   `Texts/Supplementary/Feher - Quantitative Physiology 3rd/`, decomposed into 9
   unit folders. The `pi-...` doc-id form is **not** consumable — navigate by
   folder → filename.
2. For each unit folder, `browse_documents` to list its sections (files named like
   `013 - 5.11 Vascular Function Hemodynamics.pdf`). Build a **worklist**: every
   numbered section across all 9 units. Problem sets (`5.PS1`, etc.) and
   non-quantitative sections (immunology, anatomy) still get a worklist entry —
   they'll be classified "no reusable equations" if that's true.
3. This worklist is your denominator. The ledger (§5) tracks each entry's status.

### 3.2 Extract + classify (per section)
For each section, `get_page_content` (request the whole section; equations come
back as `type: "equation"` LaTeX blocks). For every equation block and every inline
formula in prose, classify it:

- **REUSABLE MODEL** → candidate for the package. Signals: it's a named
  principle/law; it maps input quantities to an output quantity; it would be reused
  across problems; Feher states it as a standalone relation (often with an equation
  number and surrounding "the X is given by").
- **DERIVATION STEP** → skip. Signals: it's algebra between two other equations;
  it's a rearrangement shown to reach a result; it only appears inside a derivation
  and is never referenced again.
- **WORKED-EXAMPLE ARITHMETIC** → skip. Signals: concrete numbers plugged in
  (`(5000 cm³/60 s)/3.8 cm² = 22 cm/s`), Example boxes, unit conversions.
- **NON-QUANTITATIVE** → skip (record the section as such if it has none).

Record each REUSABLE candidate with: section, Feher equation number if present, the
LaTeX, the quantity it produces, and its inputs.

### 3.3 Diff against the registry
For each REUSABLE candidate, decide **present or gap**:
- Load the canonical registry and the domain's equation list.
- Match by **concept**, not string: normalise the candidate's output quantity and
  inputs and compare against existing equations in that domain (and cross-domain
  foundations). Poiseuille resistance is "present" whether the id is
  `poiseuille_resistance` or `hydraulic_resistance`.
- Classify each candidate as: `PRESENT` (id it maps to), `GAP` (genuinely missing),
  or `VARIANT` (a form of an existing equation — usually skip unless the variant is
  itself commonly used, e.g. a distinct clinical estimator).

### 3.4 Implement genuine gaps
For each `GAP`, author the equation per §2.2 (see `qp/CLAUDE.md`) in the correct
domain module, grounded in the section you read (real
`source_chapter`/`source_section`, `page_reference=None`). Prefer the smallest
correct implementation. Add the matching alias(es) only if unambiguous.

### 3.5 Reconcile + dedup
After a batch of additions:
- Re-run `_build_canonical_ids`; confirm **0 duplicate ids**.
- If two subagents added the same concept under different ids, keep one, delete the
  other, fix any `depends_on` that referenced the deleted id.
- Regenerate graph + clusters.

---

## 4. The acceptance gate (deterministic — run every iteration)  → `qp/CLAUDE.md`

The full gate lives in `qp/CLAUDE.md` at the package root: the regenerate commands,
the two test suites, the clean-import check, the **10 whole-index invariants**, and
the counts/docs you MUST update in the same batch. It is the definition of "the
package is still correct." **Run all of it after any batch of edits**; every line
must hold; if any fails, fix before proceeding. Keep it strict (§1.6).

---

## 5. The coverage ledger (the record of "done")

Maintain `COVERAGE_LEDGER.md` (or `.json`) at the package root. One row per Feher
section in the worklist:

| unit | section | title | status | reusable eqs found | present | added (ids) | excluded (reason) |
|------|---------|-------|--------|--------------------|---------|-------------|-------------------|

- `status ∈ {pending, processed, no-reusable-equations}`.
- Every REUSABLE equation in a processed section appears in exactly one of
  `present` / `added` / `excluded`. An `excluded` entry **must** carry a reason
  (variant of X / derivation step / non-quantitative).
- The ledger is what lets you and the user check completeness. The run is complete
  when **every worklist row is `processed` or `no-reusable-equations`** and the §4
  gate is green.

---

## 6. Subagent orchestration

The task fans out cleanly along Feher's structure. Use **one orchestrator** and
partition the worklist.

### 6.1 Partition
- Natural unit of parallelism: **one subagent per Feher unit** (9), or finer, **one
  per section** for the equation-dense units (5, 6, 7). Respect your harness's
  concurrency cap (Claude Code Dynamic Workflows: 16 concurrent / 1,000 total).
- Each subagent works a disjoint slice of the worklist. Slices are disjoint by
  **section**, so no two subagents touch the same PageIndex document.

### 6.2 Subagent contract (what each returns)
Each extraction subagent is **read-and-propose only** — it does NOT edit shared
package files directly (this avoids write collisions and mid-run merge chaos). It
returns a structured report:

```json
{
  "unit": 5, "section": "5.11", "title": "...",
  "reusable_candidates": [
    {"eq_number": "5.11.?", "latex": "...", "produces": "PP",
     "inputs": ["SBP","DBP"], "verdict": "GAP",
     "proposed_id": "pulse_pressure", "module": "cardiovascular/hemodynamics.py",
     "source_section": "Pulse pressure depends on stroke volume and compliance"}
  ],
  "non_reusable_count": 7,
  "notes": "..."
}
```

### 6.3 Reconciliation (orchestrator, single-threaded)
The orchestrator is the **only** writer to shared files. It:
1. Merges all subagent reports; dedups candidates proposing the same concept.
2. For each `GAP`, authors the equation (§2.2), one at a time.
3. After each unit's batch: runs the §4 gate; updates counts/docs/ledger.
4. Never lets two writes race. If your harness's dynamic-workflow script cannot
   touch the filesystem directly (Claude Code Dynamic Workflows: the coordination
   script only orchestrates; agents do the file I/O), designate a single
   "integrator" agent as the writer and serialise all edits through it.

### 6.4 Optional second-pass review
A second read-only pass over the proposed diffs is a cheap quality check: "is this
equation Feher-faithful, dimensionally consistent, and not a duplicate?" Route the
comments back to the integrator, which still owns the writes; the §4 gate still
owns "done".

---

## 7. Loop, in full

```
build worklist from PageIndex (all 9 units, all sections)      # §3.1
for each slice (fan out to subagents, respecting concurrency): # §6.1
    for each section in slice:
        extract + classify every equation                     # §3.2
        diff each reusable candidate vs registry              # §3.3
        emit structured report                                # §6.2
integrator (single writer):
    for each unit's merged report:
        implement GAPs                                         # §3.4
        reconcile + dedup                                      # §3.5
        run acceptance gate                                    # §4  -> must be green
        update counts / docs / references / CHANGELOG / ledger # §4/§5
final:
    assert every worklist row processed or no-reusable         # §5
    assert gate green on a clean regenerate                    # §4
    write coverage report                                      # §8
```

---

## 8. Final deliverable

1. The updated `qp` package, gate-green, packaged (zip named `qp`).
2. `COVERAGE_LEDGER.md` — every section accounted for.
3. A **coverage report** stating:
   - sections processed / total (e.g. "81/81" or "63/81 — remaining listed");
   - equations added (count + ids + Feher sections), new total;
   - a residual gap list (any `VARIANT`/`excluded` you judged out, with reasons);
   - confirmation the gate passes on a clean regenerate, with the actual command
     output — not a paraphrase.
4. If anything remains incomplete, an explicit "NOT DONE" section naming what and
   why. A partial result reported accurately is fine; report what's done and what
   remains.

---

## Appendix — Running this

This is a Claude Code project. The constants are the PageIndex MCP tool and the §4
gate; everything else is plain Python.

- `qp/CLAUDE.md` (§2/§4) auto-loads when you work in the package — no manual include
  needed.
- For the parallel extract pass, Dynamic Workflows help (enable `ultracode`, or put
  `workflow` in the task prompt). Design around its constraints: 16 concurrent /
  1,000 total agents; no mid-run input; session-bound resume (a crash restarts the
  run); the workflow script coordinates but agents do the file I/O. Checkpoint the
  ledger to disk after every unit so a restart resumes from the ledger, not from
  zero.

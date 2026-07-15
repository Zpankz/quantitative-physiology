---
name: quantitative-physiology
description: This skill should be used when calculating physiological parameters, modeling membrane transport, analyzing cardiovascular hemodynamics, computing renal clearance, simulating action potentials, or explaining quantitative relationships in any human physiological system. Use for physiology homework, medical calculations, computational biology modeling, and pharmacokinetic analysis.
---

# Quantitative Human Physiology

## Overview

**367 atomic equations** across 9 physiological domains with full dependency tracking. Each equation is an `AtomicEquation` object (compute function, typed parameters, source metadata) grouped into thematic modules per domain — e.g. `foundations/thermodynamics.py` defines `nernst_equation`, `gibbs_free_energy`, and others. Import an equation by its object name from its module, or resolve any name (including legacy aliases) through the canonical registry: `from scripts.canonical_ids import load; load("nernst_equation")`.

## Architecture

```
scripts/
├── foundations/      # 38 equations - transport, diffusion, thermodynamics
├── membrane/         # 30 equations - channels, pumps, potential
├── excitable/        # 29 equations - action potentials, muscle
├── nervous/          # 36 equations - synapses, sensory, motor
├── cardiovascular/   # 58 equations - heart, circulation, hemodynamics
├── respiratory/      # 62 equations - ventilation, gas exchange
├── renal/            # 42 equations - filtration, clearance
├── gastrointestinal/ # 41 equations - digestion, absorption
└── endocrine/        # 31 equations - hormones, feedback
```

## Quick Import

```python
# Import entire domains
from scripts import cardiovascular, respiratory, renal

# Import specific equations
from scripts.cardiovascular.cardiac import cardiac_output, ejection_fraction
from scripts.respiratory.gas_exchange import alveolar_gas_equation
from scripts.renal.clearance import clearance, filtered_load

# Import foundations used across domains
from scripts.foundations.transport import poiseuille_flow
from scripts.foundations.thermodynamics import nernst_equation
```

> **Verify your copy:** this minimal tier has no test suite, but `python -m
> scripts.smoke` runs a dependency-free integrity check — clean import, the
> canonical count (367), Feher provenance on every equation, external anchors
> (E_K ≈ −95 mV, CO 4.9, MAP 93.3), the `propagate()` integrative simulation, and
> the reasoning layers. Run it after extracting to confirm the package is intact.

## Core Principles

### Conservation Laws
- **Mass**: Input = Output + Accumulation
- **Energy**: Follow thermodynamic constraints
- **Charge**: Maintain electroneutrality

### Transport Classification
1. **Bulk flow**: Pressure-driven (Poiseuille)
2. **Diffusion**: Concentration-driven (Fick)
3. **Active transport**: ATP-coupled pumps

## Essential Equations

### Transport

**Poiseuille's Law** (laminar flow):
```
Q = (πr⁴/8η) × (ΔP/L)
```
Flow scales with radius⁴. Doubling vessel radius → 16× flow.

**Fick's First Law** (diffusion):
```
J = -D × (dC/dx)
```

**Diffusion time scaling**:
```
t = x²/(2D)
```

### Membrane Potential

**Nernst equation** (single ion equilibrium):
```
E = (RT/zF) × ln(C_out/C_in)
```
At 37°C: E ≈ (61.5/z) × log₁₀(C_out/C_in) mV

**Goldman-Hodgkin-Katz** (multiple ions):
```
V_m = (RT/F) × ln[(P_K[K]_o + P_Na[Na]_o + P_Cl[Cl]_i) / (P_K[K]_i + P_Na[Na]_i + P_Cl[Cl]_o)]
```

### Kinetics

**Michaelis-Menten**:
```
J = J_max × [S] / (K_m + [S])
```

**Hill equation** (cooperativity):
```
J = J_max × [S]ⁿ / (K₀.₅ⁿ + [S]ⁿ)
```

## Cross-Domain Equations

These foundational equations are used across multiple physiological systems:

| Equation | Primary | Also Used In | Import |
|----------|---------|--------------|--------|
| Nernst | foundations | membrane, excitable, nervous, cardiovascular, renal | `from scripts.foundations.thermodynamics import nernst_equation` |
| Fick Diffusion | foundations | membrane, respiratory, renal, cardiovascular | `from scripts.foundations.diffusion import fick_first_law` |
| Poiseuille | foundations | cardiovascular, respiratory, renal | `from scripts.foundations.transport import poiseuille_flow` |
| Michaelis-Menten | foundations | membrane, renal, gastrointestinal, endocrine | `from scripts.foundations.kinetics import michaelis_menten` |
| Law of Laplace | foundations | cardiovascular, respiratory, gastrointestinal | `from scripts.foundations.transport import laplace_sphere` |
| Hill | respiratory | excitable, cardiovascular, endocrine | `from scripts.respiratory.oxygen_transport import hill_equation` |
| Henderson-Hasselbalch | respiratory | renal, gastrointestinal | `from scripts.respiratory.acid_base import henderson_hasselbalch` |
| Starling Filtration | cardiovascular | renal, gastrointestinal, respiratory | `from scripts.cardiovascular.microcirculation import starling_filtration` |
| Goldman-Hodgkin-Katz | excitable | membrane, nervous, cardiovascular | `from scripts.excitable.membrane_potential import ghk_potential_eq` |

> Object names occasionally differ from ids (e.g. the object `ghk_potential_eq` has id `ghk_potential`; the object `oxygen_content` in `respiratory.oxygen_transport` has id `respiratory_oxygen_content`). For a name-agnostic import that also accepts legacy aliases, use the canonical resolver: `from scripts.canonical_ids import load; hh = load("henderson_hasselbalch")`. The full cross-domain set lives in `scripts/canonical_ids.py` (`CROSS_DOMAIN`), and `scripts/test_public_api.py` verifies every entry here resolves.

## Dependency Graph

See `graph/dependency-graph.json` for full equation dependencies.

### Key Dependency Chains

1. **Membrane → Action Potential**: ion concentrations → Nernst (per-ion E_ion) **and** GHK (V_m) in parallel → HH ionic currents → HH membrane current. (Nernst and GHK are *both* computed from concentrations — GHK does not consume a Nernst potential; they are siblings, not a chain.)
2. **Oxygen Cascade**: Hill saturation → O₂ content → O₂ delivery → Fick principle
3. **Renal Clearance**: RPF → filtration fraction → GFR → clearance → fractional excretion
4. **HPA Axis**: CRH dynamics → ACTH dynamics → Cortisol dynamics → feedback gain

### Functional Clusters

See `graph/clusters.json` for equation groupings by physiological function:
- Transport & Fluid Mechanics (7 equations)
- Electrochemical Gradients (5 equations)
- Excitation-Contraction Coupling (5 equations)
- Oxygen Transport Cascade (6 equations)
- Acid-Base Homeostasis (5 equations)
- Renal Filtration & Clearance (6 equations)
- Hormone Kinetics & Feedback (5 equations)
- Synaptic & Neural Signaling (5 equations)
- GI Secretion & Absorption (5 equations)
- Cardiovascular Regulation (5 equations)

## Graph & Integrative Reasoning

Beyond single-equation `.compute()`, `qp` ships a reasoning layer that traverses
the whole dependency graph, checks units, and **forward-chains** many equations
from a handful of measured seeds. This is the machinery that turns the library
into an exam tool: seed the numbers you were given, let the graph fire everything
downstream, and read off (or narrate) the integrated physiological state. Every
block below is runnable as-is.

- `scripts.eqgraph.build_graph()` → `EquationGraph` with `propagate(seeds)`,
  `dependency_path(a, b)`, `dependents(id)`, `feeds(id)`/`fed_by(id)`,
  `compose_paths(start, goal)`, `by_param_dimension(dim)`,
  `dimensional_bridges()`, `dimensional_diff(a, b)`. The equation objects are in
  `g.eqs` (dict keyed by id) and every id is in `g.ids` — there is no `.equations`.
- `scripts.dimensions.parse(unit_str)` → `Dim` with `.name()`, `.same_dimension()`,
  `.diff()`, and `* / **` algebra — dimensional analysis for MCQ distractors.
- `scripts.context.ComputeContext` → `.set(**vals)` then `.compute(id)`, which
  **auto-resolves upstream dependencies** (computes the intermediates for you).

### Recipe A — VIVA: seed the bedside numbers, read the integrated state

Give `propagate` the numbers a patient hands you (HR, SV, volumes, Hb, sats,
cuff pressures) and it forward-chains the whole cardiorespiratory picture in a
few rounds. The single seed below fires **60+ equations** — cardiac output,
ejection fraction, MAP, cardiac index and systemic oxygen delivery all fall out
of one call. Narrate the chain in the viva: SV+HR → CO; EDV/ESV → EF; SBP/DBP →
MAP; CO+content → DO₂.

```python
from scripts.eqgraph import build_graph
g = build_graph()
r = g.propagate(dict(HR=80, SV=65, EDV=120, ESV=55, W=70, H=175,
                     Hb=14, S_O2=0.97, P_O2=95, P_50=26.8, n=2.7,
                     SBP=125, DBP=78))
f = r["fired"]                       # {equation_id: value}, 60+ entries
print("fired:", len(f), "rounds:", r["rounds"])
print("CO  =", round(f["cardiac_output"], 2), "L/min")
print("EF  =", round(f["ejection_fraction"], 3))
print("MAP =", round(f["mean_arterial_pressure"], 1), "mmHg")
print("CI  =", round(f["cardiac_index"], 2), "L/min/m^2")
# DO2 is the climax of the oxygen cascade: CO x arterial O2 content x 10
# doc-gate: expect 946.3
round(f["systemic_oxygen_delivery"], 1)
```

The same call also derives resistances when you seed pressures and flows the
Fick way. This second seed (VO₂ + a-v content difference + the pressures) fires
**50+ equations**, computing cardiac output by Fick and chaining it into SVR and
PVR in dyn·s·cm⁻⁵ — exactly the numbers a haemodynamics viva asks you to build:

```python
from scripts.eqgraph import build_graph
g = build_graph()
r = g.propagate(dict(VO2=250, C_aO2=20, C_vO2=15,
                     MAP=93, CVP=3, mPAP=15, PCWP=9))
f = r["fired"]
print("fired:", len(f))
print("CO (Fick) =", f["cardiac_output_fick"], "L/min")   # (VO2)/(CaO2-CvO2)/10
print("PVR       =", f["pvr_dyn"], "dyn.s/cm5")           # (mPAP-PCWP)/CO x 80
# SVR = (MAP - CVP)/CO x 80
# doc-gate: expect 1440 tol=20
round(f["svr_dyn"])
```

### Recipe B — SAQ scaffold: enumerate the equations a structured answer must touch

Before writing an SAQ, ask the graph which equations sit between two quantities.
`dependency_path(downstream, upstream)` walks the `depends_on` edges and returns
the ordered chain — that chain *is* your answer's skeleton. Here, "how does
renal glucose excretion depend on glomerular Starling forces?" resolves to a
**5-equation** path from glucose handling down to capillary hydrostatic
pressure; each hop is a paragraph you must write.

```python
from scripts.eqgraph import build_graph
g = build_graph()
path = g.dependency_path("glucose_excretion", "capillary_pressure")
for i, eid in enumerate(path):
    print(f"{i+1}. {eid}")
# glucose_excretion -> filtered_load -> gfr_from_nfp
#   -> net_filtration_pressure -> capillary_pressure
# doc-gate: expect 5 tol=1
len(path)
```

Then prove the scaffold computes: `ComputeContext` takes the leaf inputs and
**auto-chains the intermediates**. Seeding only bedside values, `.compute()`
derives cardiac output internally on its way to oxygen delivery — you never hand
it CO. (ComputeContext reads a global registry, so import the 9 domains first to
populate it.)

```python
import scripts.foundations, scripts.membrane, scripts.excitable, \
    scripts.nervous, scripts.cardiovascular, scripts.respiratory, \
    scripts.renal, scripts.gastrointestinal, scripts.endocrine
from scripts.context import ComputeContext
ctx = ComputeContext()
ctx.set(HR=80, SV=65, Hb=14, S_O2=0.97, P_O2=95)
res = ctx.compute("systemic_oxygen_delivery")   # CO computed on the way
print("used (note CO auto-derived):", res.used_params)
# doc-gate: expect 946.3
round(res.value, 1)
```

### Recipe C — MCQ sanity: kill a distractor on its units

An MCQ option with the wrong dimension is wrong no matter the arithmetic.
`dimensions.parse` names any unit string and compares dimensions, so you can
eliminate distractors mechanically. Vascular resistance is *pressure·time /
volume*; an option quoting `mmHg/mL` (pressure / volume — an elastance) is
dimensionally disqualified.

```python
from scripts.dimensions import parse
correct = parse("mmHg*min/mL")     # SVR/PVR dimension
distractor = parse("mmHg/mL")      # pressure / volume -- NOT a resistance
print("correct    :", correct.name())
print("distractor :", distractor.name())
# same_dimension -> 0 means the distractor's units cannot be a resistance
# doc-gate: expect 0
int(distractor.same_dimension(correct))
```

The graph does the same check *between two equations' outputs*.
`dimensional_diff` returns the dimension separating two computed quantities —
here MAP and CO differ by exactly a **resistance** dimension, the quantitative
statement of MAP ≈ CO × SVR. Useful for sanity-checking a relationship an MCQ
stem asserts.

```python
from scripts.eqgraph import build_graph
g = build_graph()
d = g.dimensional_diff("cardiac_output", "mean_arterial_pressure")
print("MAP and CO differ by:", d.name())   # -> vascular_resistance
# confirms MAP ~ CO x SVR (pressure = flow x resistance)
# doc-gate: expect 1
int(d.name() == "vascular_resistance")
```

### Recipe D — find every related equation by shared dimension

To revise a topic laterally, ask which equations share a dimension.
`by_param_dimension` lists every equation taking a parameter of a given
dimension — a ready-made "everything that involves a pressure" study set — and
`dimensional_bridges` enumerates cross-equation dimensional links for building
concept maps.

```python
from scripts.eqgraph import build_graph
from scripts.dimensions import parse
g = build_graph()
pressure_eqs = g.by_param_dimension(parse("mmHg"))
print("equations with a pressure parameter:", len(pressure_eqs))
print("sample:", [eid for eid, _ in pressure_eqs[:6]])
print("total dimensional bridges:", len(g.dimensional_bridges()))
# a large, connected pressure sub-graph to revise together
# doc-gate: expect 91 tol=60
len(pressure_eqs)
```

### Recipe E — dimensional coupling: the algebra behind the numbers

Quantities *couple* when their dimensions multiply: pressure = flow × resistance,
so any two of {flow, resistance, pressure} determine the third — resistance is the
"edge" between flow and pressure. `dimensional_triples()` enumerates that closure.
And a dimensionless number (Reynolds, Womersley, a time constant) is not "no
information": it is a **product of dimensional factors that cancel to 1**.
`cancellation(id)` recovers that full dimensional expression, linking the pure
number to the dimensional quantities it is built from (this is why unit-cancelling
ratios are coupled into the graph rather than dropped as trivially dimensionless).

```python
from scripts.eqgraph import build_graph
g = build_graph()
# closure: flow x resistance = pressure  (any two give the third)
tri = [t for t in g.dimensional_triples()
       if t["product"] == "pressure"
       and {t["a"], t["b"]} == {"volumetric_flow", "vascular_resistance"}]
print(tri[0]["a"], "x", tri[0]["b"], "=", tri[0]["product"])
# a dimensionless number's full dimensional expression: Reynolds = rho*v*d/eta
print(g.cancellation("reynolds_number_blood")["exponents"])
# the same form is materialized on the equation object itself:
from scripts.canonical_ids import load
print(load("reynolds_number_blood").dimensional_form["expression"])   # 'rho*v*d/eta'
# reasoning ('any two give the third'): holding a flow and a resistance, a pressure
# is reachable — grounded in the equation that actually composes them (MAP = CO*SVR).
# It proposes which equation to APPLY; it does not fabricate the value.
inf = g.dimensional_inference(["cardiac_output", "poiseuille_resistance"])
print([(r["reachable"], r["via_equations"][0]) for r in inf if r["direct_realiser"]][:1])
# doc-gate: expect 4
len(g.cancellation("reynolds_number_blood")["exponents"])
```

### Recipe F — universal primitives: the same concept in a different context

Many equations that look unrelated are **one fundamental form** recurring in a new
context. `scripts.primitives` names ~6 universal kernels (a *log-of-a-ratio*, a
*saturation*, a *first-order exponential*, a *gradient flux*, *Laplace's law*, a
*product*) and proves membership by execution: the kernel, with that equation's own
constants bound in, reproduces its `.compute()`. So you reason from a handful of
intuitions, not hundreds of rules — and every named equation stays authoritative
(the shared form; the private constants). This is where the skill goes beyond a
table of equations into first-principles reasoning.

```python
from scripts import primitives as P
# disparate equations PROVEN to be the same log-of-a-ratio form:
print(P.members_of("log_ratio"))   # nernst == henderson_hasselbalch == gibbs == donnan
print(P.members_of("saturation"))  # michaelis_menten == hill == receptor == SGLT
# 'proven' = the kernel reproduces the equation's own compute (not a hand-label):
print(P.verify("log_ratio", "nernst_equation"))          # True
print(P.explain("first_order")["intuition"])
# doc-gate: expect 7
len(P.KERNELS)
```

### Recipe G — feedback loops: the structure the DAG can't hold

The dependency graph is an acyclic DAG, so it structurally cannot express a
*closed loop* — yet physiology is governed by them (baroreflex, HPA axis,
tubuloglomerular feedback). `scripts.feedback` represents the loops as first-class
objects beside the DAG (never adding a cycle to it). For the endocrine axes the
"negative feedback" is not just labelled — it is **checked against the formula**:
the closing inhibitory term (cortisol suppressing CRH) must actually appear in a
member equation.

```python
from scripts import feedback as FB
print(FB.loop("hpa_axis")["members"])       # CRH → ACTH → cortisol, closing on cortisol
print(FB.grounding("hpa_axis"))             # 'formula' — verified, not asserted
print(FB.loops_of("baroreceptor_sensitivity"))   # ['baroreflex']
# doc-gate: expect 7
len(FB.loops())
```

### Recipe H — AND/OR dependencies: alternatives vs jointly-required inputs

A flat `depends_on` cannot say whether two entries are *both needed* (AND) or are
*substitutable alternatives* (OR). `scripts.dependency_types` types that from the
registry: an OR-group is ≥2 equations declaring the same `produces` symbol, each
tagged by `kind` (definitional/approximation/measurement/model). It surfaces the
consumers whose flat list conflates alternatives as jointly-required.

```python
from scripts import dependency_types as DT
print(DT.or_group("CO")["members"])          # HR·SV (definitional) + Fick/dilution (measurement)
print(DT.alternatives_of("cardiac_output"))  # the two measurement methods
# doc-gate: expect 4
len(DT.or_groups())
```

### Recipe I — form-typing: which mathematical shape is this equation?

`scripts.eqforms` classifies every equation into one structural FORM (`log_ratio`,
`saturation`, `exponential`, `dynamics_ode`, `power_term`, `algebraic`), grounded on
two independent grounds (the `scripts.primitives` kernel *and* the formula marker).

```python
from scripts import eqforms as EF
print(EF.form_of("nernst_equation"))         # 'log_ratio'
print(EF.form_of("michaelis_menten"))        # 'saturation'
# doc-gate: expect 367
sum(len(EF.by_form(f)) for f in EF.FORMS)
```

## Physical Constants

| Constant | Symbol | Value | Units |
|----------|--------|-------|-------|
| Gas constant | R | 8.314 | J/(mol·K) |
| Faraday constant | F | 96,485 | C/mol |
| Body temperature | T | 310 | K |

> API note: in compute functions the body-temperature argument is **`T_body`**
> (default 310 K) — e.g. `nernst_equation`, `electrochemical_potential`,
> `actual_free_energy`. Only the Gibbs functions (`gibbs_free_energy`,
> `gibbs_change`) take a plain `T`. Pass `T_body=...`, not `T=...`, to the former.

## Example Usage

**Calculate Nernst potential for K⁺**:
```python
from scripts.foundations.thermodynamics import nernst_equation
# compute() returns millivolts directly (output_units='mV') — no conversion needed
E_K = nernst_equation.compute(z=1, C_out=4, C_in=140)  # -95 mV
# doc-gate: expect -95.0 tol=1
round(E_K, 1)
```

**Calculate cardiac output**:
```python
from scripts.cardiovascular.cardiac import cardiac_output
# doc-gate: expect 4.9
cardiac_output.compute(HR=70, SV=70)  # HR in bpm, SV in mL -> 4.9 L/min
```

**Calculate GFR from Starling forces**:
```python
from scripts.renal.glomerular import gfr_from_nfp, net_filtration_pressure
NFP = net_filtration_pressure.compute(P_GC=50, P_BC=15, pi_GC=25, pi_BC=0)
# doc-gate: expect 125.0
gfr_from_nfp.compute(K_f=12.5, NFP=NFP)  # mL/min
```

## Physiological Reference Values

| Parameter | Normal Range |
|-----------|--------------|
| Resting membrane potential | -70 to -90 mV |
| Cardiac output | 4-8 L/min |
| Blood pressure | 120/80 mmHg |
| GFR | 90-120 mL/min |
| Arterial pH | 7.35-7.45 |
| PaO₂ | 80-100 mmHg |
| PaCO₂ | 35-45 mmHg |

## Problem-Solving Workflow

1. **Identify the process**: Flow, diffusion, electrical, kinetics?
2. **List knowns with units**: Enforce dimensional consistency
3. **Select equation module**: Match process to appropriate domain
4. **Calculate**: Use `.compute()` method with parameters
5. **Validate**: Check result against physiological ranges
6. **Interpret**: Explain biological significance

For deeper analysis, query the graph layer (`scripts.eqgraph`) and each equation's
`AtomicEquation` object (`latex`, `parameters`, `metadata`) directly — this is the
mini runtime distribution (equation library + graph), without the teaching references.

## Source

All equations derived from **Quantitative Human Physiology: An Introduction, 3rd ed.**
(Joseph J. Feher, Elsevier). Provenance per equation lives in each object's
`metadata` (`source_unit`, `source_chapter`, `source_section`).

For metadata-driven lookup: `from scripts import index; idx = index.get_global_index()`
then `idx.by_category("cardiovascular")` or `idx.topological_order()`. Acceptance
gate (regenerate + all suites): `python -m scripts.run_gate`.

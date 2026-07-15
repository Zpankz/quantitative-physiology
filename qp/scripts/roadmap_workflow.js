export const meta = {
  name: 'qp-roadmap-council-loop',
  description: 'Self-improving loop: draft definitional/structural roadmap modules, adversarial 3-model council review, refine, return vetted proposals for serial integration',
  phases: [
    { title: 'Draft' },
    { title: 'Council' },
    { title: 'Refine' },
  ],
}

// The council (scripts/council.py) reaches gemini-3.1-pro-low + claude-opus-4-6-thinking
// + gpt-5.6-terra via vibeproxy. Grounding guardrail (from the advisor): draft agents
// may commit ONLY definitional / exact-math / structural content — NO drug-specific,
// device-specific, or population numeric values. Anything needing an external number is
// returned as needs_source for the human integrator to verify via PageIndex/Feher, never
// invented. The council flags; the human source-verifies; the §4 gate decides.

const GUARDRAIL = `
GROUNDING GUARDRAIL — READ FIRST. This is a grounded quantitative-physiology library
(CICM/ANZCA). Its iron rule: every value is executable and grounded in an INDEPENDENT
external anchor, never a circular self-test. You are drafting a DEFINITIONAL/STRUCTURAL
module only. You MAY commit:
  - definitional relations (e.g. t½ = ln2·Vd/CL, CL = k·Vd, heat balance S = M−W±R±C±K−E),
  - exact mathematical coefficients (ln2, e, 1−e^-1 = 0.632, rise time ≈ 2.2τ),
  - structural classifications of EXISTING equations (proven by inspecting their formula).
You MUST NOT commit any drug-specific number (a specific drug's Vd/CL/t½), device-specific
spec, tissue heat capacity, Du Bois-type empirical coefficient, or population statistic.
If an equation needs such a value, DO NOT invent it — list it under "needs_source" with
what real source (Feher section / named reference) would anchor it, and leave it out of
the module. Additive only: create ONLY your own NEW module file + test file. Do NOT edit
run_gate.py, SKILL.md, or any existing file. Match the create_equation idiom in
scripts/base.py (read it) and the test idiom in scripts/tests/test_feedback.py.
`

const FEATURES = [
  {
    key: 'eqforms', feature: 6, title: 'Equation form-typing (structural classifier)',
    module: 'scripts/eqforms.py', test: 'scripts/tests/test_eqforms.py',
    brief: `Classify each of the 367 existing equations by its mathematical FORM — the
groundable part of the audit's "typed ensemble". Forms: 'algebraic' (closed-form),
'exponential' (e^(±kt) decay/charge), 'saturation' (Michaelis/Hill/receptor), 'log_ratio'
(Nernst/HH), 'power_law', 'dynamics_ode' (a rate/dt relation), 'feedback_member' (belongs
to scripts.feedback). Ground each classification by INSPECTING the equation's simplified
formula / membership in scripts.primitives / scripts.feedback — NOT by hand-tagging. This
is structural, like scripts.dependency_types: no new physiological value. Provide verify()
with teeth (a mis-typed equation must fail a checkable property, e.g. an 'exponential' form
must contain e^ or exp in its formula) and a query API (form_of(eid), by_form(form)).
Reuse scripts.primitives.primitive_of and scripts.feedback.loops_of as grounding sources.`,
  },
  {
    key: 'pk', feature: 2, title: 'Pharmacokinetic compartment engine (definitional core)',
    module: 'scripts/pk.py', test: 'scripts/tests/test_pk.py',
    brief: `The DEFINITIONAL core of one/two-compartment PK — the RELATIONS, not any drug's
data (exactly as qp stores CaO2=1.34·Hb·S, not a patient's Hb). Equations (all definitional
or exact-math): volume_of_distribution Vd=Dose/C0; elimination_rate_constant k=CL/Vd;
elimination_half_life t½=ln2/k; clearance CL=k·Vd; one_compartment_decay C(t)=C0·e^(−kt);
steady_state_infusion Css=R0/CL; loading_dose=Vd·C_target; time_to_steady_state≈4–5·t½.
Every coefficient is exact (ln2) or definitional. Anchor tests to the DEFINITIONAL
IDENTITIES that need no drug data: assert t½·k == ln2 exactly; CL == k·Vd; C(t½)==C0/2;
Css·CL==R0. Do NOT add any named drug's parameters — if you think a drug example is needed,
put it in needs_source. Use EquationCategory — pick the closest existing category
(pharmacokinetics is not one; use FOUNDATIONS or ENDOCRINE and note it).`,
  },
  {
    key: 'instrument', feature: 3, title: 'Instrument / measurement response (definitional core)',
    module: 'scripts/instrument.py', test: 'scripts/tests/test_instrument.py',
    brief: `The DEFINITIONAL core of measurement-system response — the mathematical forms,
not any specific device's specs. Equations (all exact-math/definitional): first_order_step_
response fraction f(t)=1−e^(−t/τ) (f(τ)=0.632 exactly); rise_time_10_90≈2.2·τ; signal_to_
noise_ratio SNR=μ_signal/σ_noise; decibel_gain=20·log10(Vout/Vin); second_order_damping_
ratio and natural_frequency for an underdamped sensor (definitional). Anchor tests to the
EXACT identities: f(τ)=1−e^-1≈0.6321; two time-constants → 0.8647; SNR of equal signal/noise
=1. Do NOT commit any real device's τ or noise floor — list under needs_source. This is the
measurement/device roadmap item's groundable core; the metrology/drift/artefact corpus is
out of scope (say so).`,
  },
  {
    key: 'thermo', feature: 5, title: 'Thermoregulation heat balance (definitional core)',
    module: 'scripts/thermo.py', test: 'scripts/tests/test_thermo.py',
    brief: `The DEFINITIONAL core of the thermoregulation coverage gap — the energy-balance
identities, no empirical body-surface coefficient. Equations (definitional): heat_storage
S = M − W ± R ± C ± K − E (first law for the body); convective_heat_loss Q=h·A·ΔT (Newton
cooling, definitional); conductive_heat_flux Q=k·A·ΔT/d (Fourier, already the foundations
form — reuse/alias if present, else add); evaporative and radiative terms as definitional
placeholders in the balance. Anchor tests to the balance identity (S equals the signed sum
of terms) and Q=h·A·ΔT dimensional/definitional checks. Do NOT commit the Du Bois BSA
coefficient (0.007184) or any tissue heat capacity — list under needs_source. Only the
few genuinely-canonical heat-balance relations; the rest of the coverage gap (immunity,
obstetric, haemostasis) stays out of scope (say so).`,
  },
]

// ---- Feature 4: evidenced-reject dossier (no authorship) ----
const REJECT_DOSSIER_PROMPT = `${GUARDRAIL}
DO NOT WRITE ANY MODULE. Produce an EVIDENCED-REJECT dossier for roadmap Feature 4:
"Context/populations state-space — hierarchical joint distributions (age/size/gestation/
organ-function/illness) with covariance + provenance, not per-equation multipliers."
Argue whether this can be grounded WITHOUT fabricating corpus. The honest position (verify
it): representing populations as joint distributions with a covariance structure requires
real epidemiological covariance data that is NOT in Feher and cannot be invented without
violating the iron rule; per-equation scalar multipliers would be ungrounded guesses. Give
the concrete reason it is an evidenced-reject, what real corpus WOULD be needed to do it
honestly, and the one bounded thing that IS groundable if any (e.g. parameter
physiological_range already encodes per-parameter bounds — cite scripts/base.py Parameter).
Return JSON: {verdict:'evidenced-reject'|'partially-groundable', reason, needed_corpus:[...],
groundable_subset:[...]}.`

const DRAFT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['feature', 'module_path', 'test_path', 'proposal', 'needs_source', 'self_check_passed'],
  properties: {
    feature: { type: 'number' },
    module_path: { type: 'string' },
    test_path: { type: 'string' },
    proposal: { type: 'string', description: 'self-contained proposal for the council: what, each relation, why each is definitional/exact/structural (not a fabricated value), what it does NOT claim' },
    needs_source: { type: 'array', items: { type: 'string' }, description: 'values deliberately NOT committed because they need an external source the agent could not verify' },
    self_check_passed: { type: 'boolean', description: 'did `python -m <test module>` pass in-session' },
  },
}

const COUNCIL_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['approved', 'approve_count', 'reject_count', 'issues', 'verify_in_source'],
  properties: {
    approved: { type: 'boolean' },
    approve_count: { type: 'number' }, reject_count: { type: 'number' },
    issues: { type: 'array', items: { type: 'string' } },
    verify_in_source: { type: 'array', items: { type: 'string' } },
  },
}

const REFINE_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['feature', 'module_path', 'test_path', 'changed', 'summary', 'residual_dissent', 'self_check_passed'],
  properties: {
    feature: { type: 'number' }, module_path: { type: 'string' }, test_path: { type: 'string' },
    changed: { type: 'boolean' },
    summary: { type: 'string' },
    residual_dissent: { type: 'string', description: 'council points deliberately NOT adopted, with the reason (e.g. category error / out-of-scope), verified in source' },
    self_check_passed: { type: 'boolean' },
  },
}

phase('Draft')
log(`Drafting ${FEATURES.length} definitional/structural modules + 1 evidenced-reject dossier`)

// Feature 4 dossier runs alongside (structural, no code).
const dossierP = agent(REJECT_DOSSIER_PROMPT, {
  label: 'reject-dossier:F4', phase: 'Draft',
  schema: { type: 'object', additionalProperties: false,
    required: ['verdict', 'reason', 'needed_corpus', 'groundable_subset'],
    properties: { verdict: { type: 'string' }, reason: { type: 'string' },
      needed_corpus: { type: 'array', items: { type: 'string' } },
      groundable_subset: { type: 'array', items: { type: 'string' } } } },
})

// Each feature: draft -> council -> refine, independently (pipeline, no barrier).
const results = await pipeline(
  FEATURES,
  // stage 1: draft the module + test, run its self-check
  (f) => agent(
    `${GUARDRAIL}\n\nDRAFT roadmap Feature ${f.feature}: ${f.title}.\n${f.brief}\n\n` +
    `Write ${f.module}\nand its test ${f.test} (mutation-sensitive: a wrong/perturbed ` +
    `relation must fail; anchor to the exact/definitional identities named above, NOT to ` +
    `any invented number). Run \`python -m ${f.test.replace('scripts/','scripts.').replace('.py','').replace(/\//g,'.')}\` ` +
    `and \`python -c "import ${f.module.replace('scripts/','scripts.').replace('.py','').replace(/\//g,'.')}"\` ` +
    `to confirm it imports clean and the test passes. Return the draft report.`,
    { label: `draft:${f.key}`, phase: 'Draft', schema: DRAFT_SCHEMA, effort: 'high' }
  ),
  // stage 2: council review of the proposal
  (draft, f) => agent(
    `Run the adversarial council on this proposal and return its tally. Execute exactly:\n` +
    `python -c "from scripts.council import review; import json; ` +
    `r=review('Feature ${f.feature}: ${f.title}', open('/dev/stdin').read()); ` +
    `print(json.dumps({'approved':r['approved'],'approve_count':r['consensus']['approve'],` +
    `'reject_count':r['consensus']['reject'],'issues':r['all_issues'],'verify_in_source':r['verify_in_source']}))" ` +
    `<<'PROPOSAL_EOF'\n${draft?.proposal || f.brief}\nPROPOSAL_EOF\n\n` +
    `Return the parsed JSON verdict. Do not edit any file.`,
    { label: `council:${f.key}`, phase: 'Council', schema: COUNCIL_SCHEMA }
  ),
  // stage 3: refine against council issues — but source-verify before capitulating
  (council, f, i) => agent(
    `${GUARDRAIL}\n\nThe council reviewed Feature ${f.feature} (${f.title}). ` +
    `approved=${council?.approved} issues=${JSON.stringify(council?.issues || [])}.\n\n` +
    `For EACH issue, decide: is it a real defect (fix it in ${f.module}/${f.test}) or a ` +
    `category error / out-of-scope demand (do NOT capitulate — record as residual_dissent ` +
    `with the reason)? A "shared symbol / definition is circular" complaint is a category ` +
    `error (reading structure ≠ asserting a new value). A "this value is unsourced" complaint ` +
    `about a value you committed is REAL — either anchor it to a definition/exact-math or move ` +
    `it to needs_source and remove it. Do not invent a source. After editing, re-run the test ` +
    `to confirm still-green. Return the refine report. Edit ONLY ${f.module} and ${f.test}.`,
    { label: `refine:${f.key}`, phase: 'Refine', schema: REFINE_SCHEMA, effort: 'high' }
  ),
)

const dossier = await dossierP
return {
  features: results.filter(Boolean),
  feature4_dossier: dossier,
  note: 'Modules are drafted + council-vetted; the human integrator must source-verify any needs_source value, wire tests into run_gate serially, and run the §4 gate as the decider.',
}

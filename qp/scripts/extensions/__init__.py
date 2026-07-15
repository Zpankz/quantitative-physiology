"""Beyond-Feher definitional extensions — a tier SEPARATE from the canonical corpus.

These modules add reusable, grounded *definitional / exact-math* relations that go
beyond Feher's text (measurement-system response, pharmacokinetic timing,
thermoregulation heat balance) while holding the same grounding discipline: every
value is definitional or exact mathematics, no device/drug/population number is
invented (deferred quantities are listed per-module as NEEDS_SOURCE).

They are deliberately NOT part of the canonical Feher-367 count and are excluded
from `_build_canonical_ids`/`generate_graph` scans: they neither call
register_equation nor perturb CANONICAL_EQUATIONS. Import them explicitly, e.g.
`from scripts.extensions import instrument`.
"""

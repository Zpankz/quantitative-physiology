"""SSOT guard: every equation count printed in SKILL.md must equal the single
source of truth, scripts/__init__.EQUATION_COUNTS (and its sum). This makes
doc-count drift impossible to merge silently — the counts are stated in prose in
several places, and this asserts all of them against the one authority.

Excluded by design (NOT current per-domain/total counts): the references/*.md
"N equations added in this batch" lines.

Run: python -m scripts.tests.test_doc_counts
"""
import re
from pathlib import Path

from scripts import EQUATION_COUNTS, TOTAL_EQUATIONS

ROOT = Path(__file__).resolve().parents[2]  # qp package root (…/qp)

# domain title (SKILL reference table) -> EQUATION_COUNTS key
TITLE_TO_KEY = {
    "Physical Foundations": "foundations",
    "Membranes & Transport": "membrane",
    "Excitable Cells": "excitable",
    "Nervous System": "nervous",
    "Cardiovascular": "cardiovascular",
    "Respiratory": "respiratory",
    "Renal": "renal",
    "Gastrointestinal": "gastrointestinal",
    "Endocrine": "endocrine",
}
DOMAIN_KEYS = set(EQUATION_COUNTS)


def _checks():
    """Yield (source, label, found_value, expected_value) for every count in the docs."""
    skill = (ROOT / "SKILL.md").read_text()

    # --- totals: "**N atomic equations**" / "# N atomic equations" / "DAG with N equations" ---
    for m in re.finditer(r"(\d+)\s+atomic equations", skill):
        yield ("SKILL", "total(atomic equations)", int(m.group(1)), TOTAL_EQUATIONS)
    for m in re.finditer(r"DAG with (\d+) equations", skill):
        yield ("SKILL", "total(DAG)", int(m.group(1)), TOTAL_EQUATIONS)

    # --- per-domain tree lines: "<domain>/ ...# [Unit X:] N equations" ---
    for line in skill.splitlines():
        m = re.search(r"(\w+)/\s*#.*?(\d+)\s+equations", line)
        if not m:
            continue
        key = m.group(1)
        if key in DOMAIN_KEYS:
            yield ("SKILL", f"tree:{key}", int(m.group(2)), EQUATION_COUNTS[key])

    # --- SKILL reference table: "| <Title> | `references/…` | N | …" ---
    for line in skill.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*`references/[^|]+`\s*\|\s*(\d+)\s*\|", line)
        if m and m.group(1).strip() in TITLE_TO_KEY:
            key = TITLE_TO_KEY[m.group(1).strip()]
            yield ("SKILL", f"table:{key}", int(m.group(2)), EQUATION_COUNTS[key])


def run():
    checks = list(_checks())
    mismatches = [(s, l, f, e) for (s, l, f, e) in checks if f != e]
    n = len(checks)
    if mismatches:
        msg = "; ".join(f"{s} {l}: doc={f} != SSOT={e}" for s, l, f, e in mismatches)
        raise AssertionError(f"doc-count drift vs EQUATION_COUNTS: {msg}")
    print(f"doc-count SSOT check: {n} count references all match EQUATION_COUNTS")
    return 0


def test_doc_counts_match_ssot():
    run()


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

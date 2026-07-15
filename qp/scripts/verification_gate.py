"""Sensor: which equations carry an external VALUE anchor vs none.

An equation is 'value-anchored' if its canonical id appears as a string literal
in one of the value-checking test suites below. Dimensional/structural tests do
NOT count (they never assert the number is right).

Usage: python -m scripts.verification_gate            # summary + counts
       python -m scripts.verification_gate --list      # print unanchored ids (tsv)
"""
import re
import sys
from pathlib import Path

from scripts.canonical_ids import CANONICAL_EQUATIONS

HERE = Path(__file__).parent
# Suites whose job is to assert a numeric expected value.
VALUE_SUITES = [
    HERE / "tests" / "test_reference_values_locked.py",
    HERE / "tests" / "test_reference_values_audit.py",
    HERE / "tests" / "test_coverage_additions.py",
    HERE / "tests" / "test_clinical_additions.py",
    HERE / "tests" / "test_integration_chains.py",
    HERE / "tests" / "test_reference_values_grok.py",
    HERE / "tests" / "test_review_additions.py",
    HERE / "tests" / "test_adversarial_review_fixes.py",
    HERE / "tests" / "test_backlog_additions.py",
]
# Structural/dimensional suites explicitly NOT counted as value anchors.

_LIT = re.compile(r"""['"]([a-z][a-z0-9_]{2,})['"]""")


def anchored_ids():
    seen = set()
    for f in VALUE_SUITES:
        if not f.exists():
            continue
        for m in _LIT.finditer(f.read_text()):
            seen.add(m.group(1))
    return {cid for cid in CANONICAL_EQUATIONS if cid in seen}


def run():
    all_ids = set(CANONICAL_EQUATIONS)
    anchored = anchored_ids()
    unanchored = sorted(all_ids - anchored)
    # group unanchored by domain
    by_dom = {}
    for cid in unanchored:
        dom = CANONICAL_EQUATIONS[cid]["domain"]
        by_dom.setdefault(dom, []).append(cid)
    print(f"equations: {len(all_ids)}")
    print(f"value-anchored: {len(anchored)}  ({100*len(anchored)//len(all_ids)}%)")
    print(f"UNANCHORED: {len(unanchored)}  ({100*len(unanchored)//len(all_ids)}%)")
    print("--- unanchored by domain ---")
    for dom in sorted(by_dom, key=lambda d: -len(by_dom[d])):
        print(f"  {dom:24s} {len(by_dom[dom])}")
    return unanchored


if __name__ == "__main__":
    un = run()
    if "--list" in sys.argv:
        for cid in un:
            d = CANONICAL_EQUATIONS[cid]
            print(f"{cid}\t{d['domain']}\t{d['module']}\t{d['object']}")

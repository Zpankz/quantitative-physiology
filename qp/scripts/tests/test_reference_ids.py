"""SSOT guard for reference-doc formulas. After the de-dup pass, references/*.md no
longer restate an equation's formula inline — each such formula is replaced by a
citation of the canonical equation id in the exact form  qp:`<equation_id>`  . The
equation object's `latex`/`simplified` is then the single source of the formula.

This test asserts every  qp:`<id>`  citation resolves to a real equation id, so a
typo or a renamed id can never silently dangle in the teaching prose.

Run: python -m scripts.tests.test_reference_ids
"""
import re
from pathlib import Path

# populate the global registry so load() resolves aliases too
import scripts.foundations, scripts.membrane, scripts.excitable, scripts.nervous  # noqa: F401
import scripts.cardiovascular, scripts.respiratory, scripts.renal  # noqa: F401
import scripts.gastrointestinal, scripts.endocrine  # noqa: F401
from scripts.canonical_ids import CANONICAL_EQUATIONS, resolve

ROOT = Path(__file__).resolve().parents[2]
REFDIR = ROOT / "references"
CITE = re.compile(r"qp:`([a-z_][a-z0-9_]*)`")


def _citations():
    """Yield (file, id) for every  qp:`id`  citation across references/*.md."""
    for md in sorted(REFDIR.glob("*.md")):
        text = md.read_text()
        for m in CITE.finditer(text):
            yield (md.name, m.group(1))


def run():
    cites = list(_citations())
    bad = []
    for fname, eid in cites:
        if eid in CANONICAL_EQUATIONS:
            continue
        try:
            resolve(eid)  # accepts aliases
        except Exception:
            bad.append(f"{fname}: qp:`{eid}` does not resolve")
    if bad:
        raise AssertionError("dangling reference citations:\n  " + "\n  ".join(bad))
    n_files = len({f for f, _ in cites})
    print(f"reference-id check: {len(cites)} citations across {n_files} files all resolve")
    return 0


def test_reference_ids_resolve():
    run()


if __name__ == "__main__":
    import sys
    try:
        run()
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    sys.exit(0)

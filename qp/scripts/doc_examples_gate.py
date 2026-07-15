"""Executable documentation gate: extract every fenced ``python`` code block
from the skill docs and RUN it against the live package. A study skill whose own
copy-paste examples raise is worse than no example — this gate makes "the docs
execute" a checked invariant, the sensor for the skill-evaluation workflow.

    python -m scripts.doc_examples_gate           # gate all docs
    python -m scripts.doc_examples_gate SKILL.md  # one file

A block is SKIPPED (not failed) only if it is explicitly tagged as illustrative
with a leading ``# doc-gate: skip`` comment (use sparingly, e.g. pseudo-code).
Every other python block must import and execute with no exception.

VALUE CHECK (closes the "runs != correct" gap): a block may assert its result
with a comment ``# doc-gate: expect <value> [tol=<x>]``. The gate evaluates the
block's LAST expression statement and asserts it is within tolerance of <value>
(default tol = 1% relative, or 1e-6 absolute for near-zero). This makes "the
example returns the value the prose claims" a checked invariant — a wrong-units
example (e.g. printing V while the comment says mV) fails the gate instead of
passing silently.
"""
import ast
import os
import re
import sys
import io
import contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DEFAULT = ["SKILL.md"] + [
    os.path.join("references", f) for f in sorted(
        os.listdir(os.path.join(ROOT, "references"))
    ) if f.endswith(".md")
] if os.path.isdir(os.path.join(ROOT, "references")) else ["SKILL.md"]

BLOCK = re.compile(r"```python\n(.*?)```", re.DOTALL)


def blocks(md_path):
    with open(md_path, encoding="utf-8") as fh:
        text = fh.read()
    for i, m in enumerate(BLOCK.finditer(text)):
        code = m.group(1)
        line = text[:m.start()].count("\n") + 1
        yield i, line, code


EXPECT = re.compile(r"#\s*doc-gate:\s*expect\s+([-+0-9.eE]+)(?:\s+tol=([-+0-9.eE]+))?")


def run_block(code):
    """Execute a block with the package importable. Returns (ok, err).

    If the block carries a ``# doc-gate: expect <value>`` comment, also assert
    the block's last expression evaluates within tolerance of that value.
    """
    if "# doc-gate: skip" in code:
        return None, "skipped"
    m = EXPECT.search(code)
    expect = float(m.group(1)) if m else None
    tol = float(m.group(2)) if (m and m.group(2)) else None

    g = {"__name__": "__doc_example__"}
    old = sys.path[:]
    sys.path.insert(0, ROOT)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            if expect is None:
                exec(compile(code, "<doc>", "exec"), g)
                return True, None
            # value check: run all but the last statement, then eval the last
            # expression so we can compare its result.
            tree = ast.parse(code)
            last = tree.body[-1] if tree.body else None
            if not isinstance(last, ast.Expr):
                # nothing to compare — fall back to run-only
                exec(compile(code, "<doc>", "exec"), g)
                return True, None
            head = ast.Module(body=tree.body[:-1], type_ignores=[])
            exec(compile(head, "<doc>", "exec"), g)
            val = eval(compile(ast.Expression(last.value), "<doc>", "eval"), g)
            fval = float(val)
            lim = tol if tol is not None else max(abs(expect) * 0.01, 1e-6)
            if abs(fval - expect) <= lim:
                return True, None
            return False, f"value {fval} != expected {expect} (tol {lim})"
    except Exception as e:  # noqa: BLE001 — doc gate reports any failure
        return False, f"{type(e).__name__}: {e}"
    finally:
        sys.path[:] = old


def gate(docs):
    total = passed = failed = skipped = 0
    failures = []
    for rel in docs:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        for i, line, code in blocks(path):
            total += 1
            ok, err = run_block(code)
            if ok is None:
                skipped += 1
            elif ok:
                passed += 1
            else:
                failed += 1
                failures.append((rel, line, err, code.strip().splitlines()[0] if code.strip() else ""))
    print(f"docs: {len(docs)}  python-blocks: {total}  "
          f"passed: {passed}  failed: {failed}  skipped: {skipped}")
    for rel, line, err, first in failures:
        print(f"  FAIL {rel}:{line}  {err}")
        print(f"       first line: {first}")
    return 1 if failed else 0


if __name__ == "__main__":
    docs = sys.argv[1:] or DOCS_DEFAULT
    sys.exit(gate(docs))

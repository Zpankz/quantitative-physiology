"""Adversarial model council — a 3-model review gate for proposed additions.

The council does NOT decide. It *critiques*. Every proposal it approves must
still pass the deterministic §4 gate; every proposal it rejects must still be
verified against the corpus/an external anchor before we act on the rejection
(grok/gemini review fan-out carries a large false-positive rate — a council
"REJECT: fabricated" is a lead to verify, not a verdict to obey). The council's
value is catching grounding violations (invented values, circular self-tests,
duplicated concepts, dimensional nonsense) that a single author misses.

Three members from three independent model families, reached through the local
vibeproxy (OpenAI-compatible):
  * gemini-3.1-pro-low          (google;  only 3.1-pro variant the proxy exposes)
  * claude-opus-4-6-thinking    (anthropic)
  * gpt-5.6-terra               (openai)

The requested third family was xAI's grok-4.5, but the proxy reports it
``auth_unavailable: no auth available (providers=xai)`` — every grok/xai model
returns 402/503, so grok cannot vote right now. gpt-5.6-terra substitutes as a
live, independent (OpenAI) perspective, keeping a genuine three-family panel
rather than a silent two-model quorum. `GROK_REQUESTED` records the original ask.

Each member is given the same adversarial-reviewer prompt and asked for a strict
JSON verdict. `review()` returns the three verdicts plus a tallied consensus. No
new dependency — stdlib urllib.
"""
from __future__ import annotations
import json
import re
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8317/v1/chat/completions"
GROK_REQUESTED = "grok-4.5"  # requested but auth_unavailable on this proxy (xai)
COUNCIL = ["gemini-3.1-pro-low", "claude-opus-4-6-thinking", "gpt-5.6-terra"]

REVIEWER_SYSTEM = (
    "You are an adversarial reviewer on a council vetting a proposed addition to a "
    "grounded quantitative-physiology equation library (CICM/ANZCA primary exam). "
    "The library's iron rule: EVERY value is executable and grounded in an "
    "independent external anchor (a textbook/reference number), never in a circular "
    "self-test. No fabricated coefficients, no invented corpus, no equation deleted "
    "or collapsed (additive only), no dimensional nonsense, no duplicate of an "
    "existing concept. Your job is to REFUTE: assume the proposal is flawed and look "
    "for the flaw. Be specific and terse.\n\n"
    "Reply with ONLY a JSON object, no prose around it:\n"
    '{"verdict": "APPROVE" | "REJECT",\n'
    ' "grounded": true | false,          // is every value externally anchored, not circular?\n'
    ' "dimensionally_ok": true | false,\n'
    ' "duplicate_of_existing": true | false,\n'
    ' "issues": ["..."],                 // concrete, each a thing to fix or verify\n'
    ' "verify_in_source": ["..."]}       // claims the author must check against the book/reference\n'
    "APPROVE only if grounded AND dimensionally_ok AND not a duplicate."
)


def _call(model: str, proposal: str, timeout: int = 120) -> dict:
    body = json.dumps({
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": REVIEWER_SYSTEM},
            {"role": "user", "content": proposal},
        ],
    }).encode()
    req = urllib.request.Request(
        BASE_URL, data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer local"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode())
        content = data["choices"][0]["message"]["content"]
        return {"model": model, **_parse_verdict(content), "raw": content[:400]}
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        return {"model": model, "verdict": "ERROR", "error": str(e)[:200]}
    except (KeyError, json.JSONDecodeError) as e:
        return {"model": model, "verdict": "ERROR", "error": f"bad response: {e}"}


def _parse_verdict(content: str) -> dict:
    """Pull the JSON object out of a possibly fenced / prose-wrapped reply."""
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.S)
    blob = m.group(1) if m else None
    if blob is None:
        m = re.search(r"\{.*\}", content, re.S)
        blob = m.group(0) if m else None
    if blob is None:
        return {"verdict": "UNPARSEABLE"}
    try:
        v = json.loads(blob)
    except json.JSONDecodeError:
        return {"verdict": "UNPARSEABLE"}
    v.setdefault("verdict", "UNPARSEABLE")
    return v


def review(title: str, proposal: str, models: list[str] | None = None) -> dict:
    """Send one proposal to every council member; tally the verdicts.

    `proposal` should be self-contained: what is being added, the equations/values,
    where each value is anchored, and what it does NOT claim. Returns
    {verdicts: [...], consensus: {approve, reject, error}, approved: bool,
     all_issues: [...], verify_in_source: [...]}.
    approved is True only when a strict majority (>=2/3) APPROVE with grounded=True.
    """
    models = models or COUNCIL
    full = f"# Proposal: {title}\n\n{proposal}"
    verdicts = [_call(m, full) for m in models]
    approve = sum(1 for v in verdicts if v.get("verdict") == "APPROVE" and v.get("grounded") is not False)
    reject = sum(1 for v in verdicts if v.get("verdict") == "REJECT")
    error = sum(1 for v in verdicts if v.get("verdict") in ("ERROR", "UNPARSEABLE"))
    issues, verify = [], []
    for v in verdicts:
        for it in v.get("issues", []) or []:
            issues.append(f"[{v['model']}] {it}")
        for it in v.get("verify_in_source", []) or []:
            verify.append(f"[{v['model']}] {it}")
    return {
        "title": title,
        "verdicts": verdicts,
        "consensus": {"approve": approve, "reject": reject, "error": error},
        "approved": approve >= 2,
        "all_issues": issues,
        "verify_in_source": verify,
    }


def _fmt(result: dict) -> str:
    c = result["consensus"]
    lines = [f"COUNCIL «{result['title']}» → approve={c['approve']} reject={c['reject']} error={c['error']}"
             f"  ⇒ {'APPROVED (still must pass gate)' if result['approved'] else 'NOT APPROVED'}"]
    for v in result["verdicts"]:
        tag = v.get("verdict")
        extra = f" grounded={v.get('grounded')}" if "grounded" in v else ""
        if v.get("error"):
            extra = f" ({v['error']})"
        lines.append(f"  - {v['model']}: {tag}{extra}")
    if result["all_issues"]:
        lines.append("  issues:")
        lines += [f"    · {i}" for i in result["all_issues"][:12]]
    return "\n".join(lines)


if __name__ == "__main__":
    # Cheap sanity check: the council must APPROVE a grounded proposal and REJECT
    # a fabricated one. If it waves the fabrication through, the mechanism is
    # worthless — better to learn that here than inside a workflow.
    good = (
        "Add `mean_arterial_pressure`: MAP = DBP + (SBP-DBP)/3. "
        "Anchored to the standard clinical formula; at SBP=120, DBP=80 → MAP=93.3 mmHg, "
        "which matches the widely published normal value. Dimensionally: mmHg throughout. "
        "Not a duplicate — no existing MAP-from-cuff-pressures equation."
    )
    bad = (
        "Add `magic_perfusion_index`: MPI = 0.732 * MAP^1.4 / sqrt(age). "
        "The coefficient 0.732 and exponent 1.4 are chosen so the model 'looks right'; "
        "there is no textbook or reference source for them — they are not anchored to any "
        "external value, and the only validation is that the function reproduces its own output."
    )
    for title, p in [("known-good MAP", good), ("known-bad fabricated MPI", bad)]:
        print(_fmt(review(title, p)))
        print()

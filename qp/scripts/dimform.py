"""Dimensional-form recovery: express an equation's OUTPUT dimension as a product
of its PARAMETER dimensions, i.e. the exponents ``e_i`` with
``∏ dim(param_i)**e_i == output``, and render them as ``"rho*v*d/eta"``.

For a dimensionless output (Reynolds, Womersley, a time constant, a ratio) this is
the *cancellation relation* that makes the number pure — the "full dimensional
expression" behind the dimensionless quantity, so it is coupled to its dimensional
parents rather than dropped as trivially dimensionless.

Pure function of ``(param units, output units)``. The parameters ARE the source of
truth, so the form is derived from them and can never drift from the equation; it
is cached onto the object (`AtomicEquation.dimensional_form`) once computed.
"""
from __future__ import annotations
from typing import Dict, Optional

from scripts.dimensions import parse


def _expr(exps: Dict[str, float]) -> str:
    """Render {'rho':1,'v':1,'d':1,'eta':-1} as 'rho*v*d/eta'."""
    def term(n, e):
        e = abs(e)
        return n if e == 1 else f"{n}^{e:g}"
    num = [term(n, e) for n, e in exps.items() if e > 0]
    den = [term(n, e) for n, e in exps.items() if e < 0]
    if not num and not den:
        return "1"
    s = "*".join(num) if num else "1"
    if den:
        s += "/" + "*".join(den)
    return s


def cancellation(param_units: Dict[str, Optional[str]],
                 output_units: Optional[str], snap: int = 2) -> Optional[dict]:
    """Recover the exponents composing ``output`` from the parameter dimensions.

    Returns ``{output, dimensionless, exponents, expression, param_dims}`` or
    ``None`` if the output is opaque/undeclared or the parameters carry no
    resolvable dimensions.
    """
    import numpy as np
    out = parse(output_units)
    items = [(n, parse(u)) for n, u in param_units.items()]
    items = [(n, d) for n, d in items if d.known]
    if not out.known or not items:
        return None
    A = np.array([list(d.v) for _, d in items], dtype=float).T   # 7 x n
    b = np.array(list(out.v), dtype=float)
    names = [n for n, _ in items]
    dimensionless = bool(np.allclose(b, 0.0))
    if dimensionless:
        _, s, vt = np.linalg.svd(A)
        null = [vt[k] for k in range(vt.shape[0]) if k >= len(s) or s[k] < 1e-9]
        if not null:
            return None
        x = null[0]
    else:
        x, *_ = np.linalg.lstsq(A, b, rcond=None)
        if not np.allclose(A @ x, b, atol=1e-9):
            return None
    mag = np.abs(x)[np.abs(x) > 1e-6]
    if len(mag):
        x = x / mag.min()
    lead = next((v for v in x if abs(v) > 1e-6), 0.0)
    if lead < 0:
        x = -x
    xr = np.round(x * snap) / snap
    ok = (np.allclose(A @ xr, 0.0, atol=1e-6) and not np.allclose(xr, 0.0)) \
        if dimensionless else np.allclose(A @ xr, b, atol=1e-6)
    if not ok:
        xr = x
    exps = {names[k]: round(float(xr[k]), 3)
            for k in range(len(names)) if abs(xr[k]) > 1e-6}
    return {"output": out.name(), "dimensionless": dimensionless,
            "exponents": exps, "expression": _expr(exps),
            "param_dims": {n: d.name() for n, d in items}}

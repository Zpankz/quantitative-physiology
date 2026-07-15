"""Dimensional-analysis engine for the qp equation library.

Parses the free-text unit strings used by every ``Parameter`` (and an equation's
``output_units``) into SI **dimension vectors** over the seven base quantities, so
that equations and variables can be compared, differenced, and combined by
*dimension* rather than by string. This is the substrate the graph layer
(:mod:`scripts.eqgraph`) uses for dimensional path-traversal and combinatorial
composition search.

Base dimensions (SI), in fixed order::

    M   mass          (kg)
    L   length        (m)
    T   time          (s)
    I   electric current (A)
    K   temperature   (K)
    N   amount        (mol)
    J   luminous intensity (cd)

A :class:`Dim` also carries a best-effort ``scale`` (the factor that converts a
value in the given unit to SI base units) and a ``known`` flag. Genuinely
opaque units ("arbitrary", "variable") parse to ``Dim.UNKNOWN`` (``known=False``)
so they never spuriously match in dimensional search; true dimensionless
quantities ("dimensionless", "%", "pH units") parse to the zero vector.

No third-party dependency — pure Python, portable with the skill.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Dict, Optional, Tuple
import re

_BASE = ("M", "L", "T", "I", "K", "N", "J")
_ZERO = (0,) * 7


@dataclass(frozen=True)
class Dim:
    """A physical dimension: an exponent vector over the SI base quantities."""
    v: Tuple[int, ...] = _ZERO
    scale: float = 1.0          # value_in_unit * scale = value in SI base units
    known: bool = True          # False => opaque; never dimension-matches
    arbitrary: bool = False     # True => a DECLARED opaque scale (sensation units,
                                # relative hormone activity): typed for reporting,
                                # but still never dimension-matches. Distinct from
                                # UNKNOWN, which is genuinely undeclared/unparseable.

    UNKNOWN: ClassVar["Dim"]
    DIMENSIONLESS: ClassVar["Dim"]
    ARBITRARY: ClassVar["Dim"]

    @property
    def declared(self) -> bool:
        """True if this quantity has an assigned type — a real SI dimension OR an
        explicit 'arbitrary' opaque scale. False only for genuinely UNKNOWN
        (undeclared / unparseable) units. Use this for 'how many are typed?'."""
        return self.known or self.arbitrary

    # -- algebra -----------------------------------------------------------
    def __mul__(self, o: "Dim") -> "Dim":
        if self.arbitrary or o.arbitrary:
            return Dim.ARBITRARY
        if not (self.known and o.known):
            return Dim.UNKNOWN
        return Dim(tuple(a + b for a, b in zip(self.v, o.v)), self.scale * o.scale)

    def __truediv__(self, o: "Dim") -> "Dim":
        if self.arbitrary or o.arbitrary:
            return Dim.ARBITRARY
        if not (self.known and o.known):
            return Dim.UNKNOWN
        return Dim(tuple(a - b for a, b in zip(self.v, o.v)),
                   self.scale / o.scale if o.scale else self.scale)

    def __pow__(self, k) -> "Dim":
        if self.arbitrary:
            return Dim.ARBITRARY
        if not self.known:
            return Dim.UNKNOWN
        return Dim(tuple(int(round(a * k)) for a in self.v), self.scale ** k)

    # -- comparison --------------------------------------------------------
    def same_dimension(self, o: "Dim") -> bool:
        """True if the two are the SAME physical dimension (ignores scale/unit)."""
        return self.known and o.known and self.v == o.v

    @property
    def is_dimensionless(self) -> bool:
        return self.known and self.v == _ZERO

    def diff(self, o: "Dim") -> Optional["Dim"]:
        """The dimension you must MULTIPLY ``self`` by to reach ``o`` (o/self).

        ``a.diff(b).is_dimensionless`` iff a and b share a dimension. Returns
        None if either side is opaque.
        """
        if not (self.known and o.known):
            return None
        return o / self

    # -- presentation ------------------------------------------------------
    def signature(self) -> str:
        if self.arbitrary:
            return "arbitrary"
        if not self.known:
            return "UNKNOWN"
        if self.v == _ZERO:
            return "1"  # dimensionless
        num, den = [], []
        for sym, e in zip(_BASE, self.v):
            if e > 0:
                num.append(sym if e == 1 else f"{sym}^{e}")
            elif e < 0:
                den.append(sym if e == -1 else f"{sym}^{-e}")
        s = "·".join(num) if num else "1"
        if den:
            s += "/" + "·".join(den)
        return s

    def name(self) -> str:
        """Human name of a common derived dimension, else its signature."""
        return _DERIVED_NAMES.get(self.v, self.signature())

    def __repr__(self) -> str:
        return f"Dim({self.name()})"


# sentinel instances (assigned after class body)
Dim.UNKNOWN = Dim(_ZERO, 1.0, known=False)          # type: ignore[attr-defined]
Dim.DIMENSIONLESS = Dim(_ZERO, 1.0, known=True)     # type: ignore[attr-defined]
Dim.ARBITRARY = Dim(_ZERO, 1.0, known=False, arbitrary=True)  # type: ignore[attr-defined]


def _d(M=0, L=0, T=0, I=0, K=0, N=0, J=0, scale=1.0) -> Dim:
    return Dim((M, L, T, I, K, N, J), float(scale))


# Named derived dimensions (by exponent vector) for readable output.
_DERIVED_NAMES: Dict[Tuple[int, ...], str] = {
    _d(L=1).v: "length", _d(M=1).v: "mass", _d(T=1).v: "time",
    _d(N=1).v: "amount", _d(K=1).v: "temperature", _d(I=1).v: "current",
    _d(L=2).v: "area", _d(L=3).v: "volume",
    _d(T=-1).v: "frequency", _d(L=1, T=-1).v: "velocity",
    _d(L=1, T=-2).v: "acceleration",
    _d(M=1, L=1, T=-2).v: "force", _d(M=1, L=2, T=-2).v: "energy",
    _d(M=1, L=2, T=-3).v: "power", _d(M=1, L=-1, T=-2).v: "pressure",
    _d(M=1, L=-1, T=-1).v: "dynamic_viscosity",
    _d(M=1, T=-2).v: "surface_tension",
    _d(L=3, T=-1).v: "volumetric_flow",
    _d(N=1, L=-3).v: "molar_concentration",
    _d(M=1, L=-3).v: "mass_concentration",
    _d(N=1, T=-1).v: "molar_rate", _d(M=1, T=-1).v: "mass_rate",
    _d(M=1, L=2, T=-3, I=-1).v: "voltage", _d(I=1, T=1).v: "charge",
    _d(I=-1, M=-1, L=-2, T=3).v: "resistance_electrical",
    _d(I=2, M=-1, L=-2, T=3).v: "conductance",
    _d(I=2, M=-1, L=-2, T=4).v: "capacitance",
    _d(M=-1, L=4, T=2).v: "compliance",
    _d(M=1, L=-4, T=-1).v: "vascular_resistance",
    _d(L=2, T=-1).v: "diffusivity",
}

# ---------------------------------------------------------------------------
# Unit registry: exact (case-sensitive) token -> Dim(vector, SI scale)
# Clinical prefixes are irregular (mmHg is not milli-mHg), so tokens are listed
# explicitly rather than by generic prefix algebra.
# ---------------------------------------------------------------------------
UNIT_TABLE: Dict[str, Dim] = {}


def _reg(dim: Dim, *tokens: str) -> None:
    for t in tokens:
        UNIT_TABLE[t] = dim


# dimensionless / opaque
_reg(Dim.DIMENSIONLESS, "dimensionless", "", "1", "%", "percent", "pH", "pH units",
     "ratio", "rad", "deg", "fraction", "count", "boolean")
# International/enzyme activity units (IU, U) are a defined biological COUNT with no
# SI dimension → treated as dimensionless, so e.g. mU/L parses to inverse-volume
# (a declared dimension) rather than UNKNOWN. Different hormones' activities are
# not interconvertible, but dimensionally an activity concentration is count/volume.
_reg(Dim.DIMENSIONLESS, "U", "IU", "mU", "mIU", "uU", "uIU", "µU", "µIU", "μU", "μIU")
_reg(Dim.ARBITRARY, "arbitrary", "arbitrary units", "variable", "au", "a.u.")
# length
_reg(_d(L=1), "m"); _reg(_d(L=1, scale=1e-2), "cm"); _reg(_d(L=1, scale=1e-3), "mm")
_reg(_d(L=1, scale=1e-6), "um", "µm", "μm"); _reg(_d(L=1, scale=1e-9), "nm")
_reg(_d(L=2), "m2", "m^2", "m²"); _reg(_d(L=2, scale=1e-4), "cm2", "cm^2", "cm²")
_reg(_d(L=3), "m3", "m^3", "m³")
# mass
_reg(_d(M=1), "kg"); _reg(_d(M=1, scale=1e-3), "g"); _reg(_d(M=1, scale=1e-6), "mg")
_reg(_d(M=1, scale=1e-9), "ug", "µg", "μg"); _reg(_d(M=1, scale=1e-12), "ng")
_reg(_d(M=1, scale=1e-15), "pg")
# time
_reg(_d(T=1), "s", "sec", "time"); _reg(_d(T=1, scale=1e-3), "ms")
_reg(_d(T=1, scale=60), "min"); _reg(_d(T=1, scale=3600), "h", "hour", "hr")
_reg(_d(T=1, scale=86400), "day"); _reg(_d(T=1, scale=3.156e7), "years", "year", "yr")
# amount (mol) — equivalents (Eq) and osmoles (Osm) treated as amount
_reg(_d(N=1), "mol", "Eq", "Osm", "osmol")
_reg(_d(N=1, scale=1e-3), "mmol", "mEq", "mOsm")
_reg(_d(N=1, scale=1e-6), "umol", "µmol", "μmol", "uEq")
_reg(_d(N=1, scale=1e-9), "nmol"); _reg(_d(N=1, scale=1e-12), "pmol")
# temperature / current
_reg(_d(K=1), "K", "°C", "C_temp")
_reg(_d(I=1), "A"); _reg(_d(I=1, scale=1e-3), "mA"); _reg(_d(I=1, scale=1e-6), "uA", "µA", "μA")
_reg(_d(I=1, scale=1e-12), "pA")
# charge / voltage / energy / power / force
_reg(_d(I=1, T=1), "C")           # coulomb (NB: 'C' here is charge; temperature is 'K')
_reg(_d(M=1, L=2, T=-3, I=-1), "V"); _reg(_d(M=1, L=2, T=-3, I=-1, scale=1e-3), "mV")
_reg(_d(M=1, L=2, T=-2), "J"); _reg(_d(M=1, L=2, T=-2, scale=4184.0), "kcal", "Cal")
_reg(_d(M=1, L=2, T=-3), "W")
_reg(_d(M=1, L=1, T=-2), "N")
_reg(_d(M=1, L=1, T=-2, scale=1e-5), "dyn")  # CGS force
# frequency
_reg(_d(T=-1), "Hz", "bpm", "spikes", "breaths", "beats", "cycles", "photons", "spike")
# pressure
_reg(_d(M=1, L=-1, T=-2), "Pa"); _reg(_d(M=1, L=-1, T=-2, scale=133.322), "mmHg", "Torr")
_reg(_d(M=1, L=-1, T=-2, scale=98.0665), "cmH2O"); _reg(_d(M=1, L=-1, T=-2, scale=1e3), "kPa")
# electrical S/Ω/F (siemens, ohm, farad)
_reg(_d(I=2, M=-1, L=-2, T=3), "S"); _reg(_d(I=2, M=-1, L=-2, T=3, scale=1e-3), "mS")
_reg(_d(I=2, M=-1, L=-2, T=3, scale=1e-9), "nS"); _reg(_d(I=2, M=-1, L=-2, T=3, scale=1e-12), "pS")
_reg(_d(M=1, L=2, T=-3, I=-2), "Ω", "ohm"); _reg(_d(M=1, L=2, T=-3, I=-2, scale=1e6), "MΩ")
_reg(_d(I=2, M=-1, L=-2, T=4), "F")
# volume (litres)
_reg(_d(L=3, scale=1e-3), "L"); _reg(_d(L=3, scale=1e-6), "mL"); _reg(_d(L=3, scale=1e-4), "dL")
_reg(_d(L=3, scale=1e-9), "uL", "µL", "μL"); _reg(_d(L=3, scale=1e-12), "nL")
_reg(_d(L=3, scale=1e-18), "fL")
# molar concentration convenience tokens (mol/L family) — dim N·L^-3
_reg(_d(N=1, L=-3, scale=1e3), "M"); _reg(_d(N=1, L=-3, scale=1.0), "mM")
_reg(_d(N=1, L=-3, scale=1e-3), "uM", "µM", "μM"); _reg(_d(N=1, L=-3, scale=1e-6), "nM")
_reg(_d(N=1, L=-3, scale=1e-9), "pM")
# misc named
_reg(_d(K=1), "Kelvin")
_reg(_d(M=1, L=-1, T=-2, scale=1e-3), "mPa")   # millipascal (blood viscosity)
_reg(_d(M=1, L=1, T=-2, scale=1e-3), "mN")     # millinewton (surface tension)
_reg(_d(I=2, M=-1, L=-2, T=4, scale=1e-6), "uF", "µF", "μF")  # microfarad


# ---------------------------------------------------------------------------
# Parser for compound unit strings
# ---------------------------------------------------------------------------
_SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5",
        "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-"}


def _normalise(s: str) -> str:
    s = s.strip()
    # drop parenthetical annotations: "L (STPD)", "Wood units (mmHg/(L/min))"
    # ...but keep parentheses that are structural (compound). Heuristic: strip a
    # trailing "(...)" note only when it follows whitespace.
    s = re.sub(r"\s+\([^()]*\)$", "", s)
    if " or " in s:                       # ambiguous alt-units: take the first
        s = s.split(" or ")[0].strip()
    if s.lower().startswith("wood unit"):
        return "mmHg/L*min"               # Wood units = mmHg/(L/min)
    for k, val in _SUP.items():           # unicode superscripts -> ^n
        s = s.replace(k, "^" + val if val != "-" else "^-")
    s = s.replace("^^", "^")
    s = s.replace(" per ", "/").replace("·", "*").replace(".", "*")
    for ann in ("STPD", "cells", "O2", "CO2"):   # non-dimensional annotations
        s = s.replace(ann, "")
    s = s.replace("%", "")                        # percent is dimensionless
    return s.strip().strip("*")


# atomic unit tokens, ^exponents, bare integers (e.g. the 1 in "1/s"), operators
_TOKEN = re.compile(r"[A-Za-zµμΩ°]+[A-Za-z0-9µμΩ°]*|\^-?\d+|\d+|[*/()]")


def parse(unit_str: Optional[str]) -> Dim:
    """Parse a (possibly compound) unit string into a :class:`Dim`.

    Understands ``*`` ``·`` ``/`` ``^`` and parentheses, unicode superscripts,
    "per", and "X or Y" (takes X). Unknown atomic tokens yield ``Dim.UNKNOWN``.
    """
    if unit_str is None:
        return Dim.UNKNOWN
    s = _normalise(unit_str)
    if s == "":
        return Dim.DIMENSIONLESS
    toks = _TOKEN.findall(s)
    if not toks:
        return Dim.UNKNOWN
    try:
        dim, _ = _parse_expr(toks, 0)
    except (IndexError, ValueError):
        return Dim.UNKNOWN
    return dim


def _atom(tok: str) -> Dim:
    if tok in UNIT_TABLE:
        return UNIT_TABLE[tok]
    if re.fullmatch(r"\d+", tok):         # bare number, e.g. "1" in "1/s"
        return Dim.DIMENSIONLESS
    return Dim.UNKNOWN


def _parse_expr(toks, i):
    """expr := term (('*' | '/') term)*"""
    dim, i = _parse_term(toks, i)
    while i < len(toks) and toks[i] in ("*", "/"):
        op = toks[i]
        rhs, i = _parse_term(toks, i + 1)
        dim = dim * rhs if op == "*" else dim / rhs
    return dim, i


def _parse_term(toks, i):
    """term := factor ('^' int)?"""
    dim, i = _parse_factor(toks, i)
    if i < len(toks) and toks[i].startswith("^"):
        dim = dim ** int(toks[i][1:])
        i += 1
    return dim, i


def _parse_factor(toks, i):
    """factor := '(' expr ')' | atom"""
    if toks[i] == "(":
        dim, i = _parse_expr(toks, i + 1)
        if i < len(toks) and toks[i] == ")":
            i += 1
        return dim, i
    if toks[i] in ("*", "/", ")"):
        raise ValueError("unexpected operator")
    return _atom(toks[i]), i + 1


def dimension_of_parameter(param) -> Dim:
    """Dim of a ``Parameter`` (from its ``units`` string)."""
    return parse(getattr(param, "units", None))


def dimension_of_equation(eq) -> Dim:
    """Dim of an equation's result, from its ``output_units`` (None => UNKNOWN)."""
    return parse(getattr(eq, "output_units", None))

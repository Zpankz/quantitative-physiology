"""
Quantitative Physiology Equation Library.

A hierarchical, modular system for physiological equations with:
- Atomic equation components with dependency tracking
- Multi-dimensional indexing (by ID, category, unit)
- Cross-domain registry for shared equations
- Parameter resolution with alias normalization
- Lazy imports for context minimization

Usage:
    # Import specific domains
    from scripts import foundations, membrane, cardiovascular

    # Import base classes
    from scripts.base import AtomicEquation, Parameter, create_equation

    # Import indexing
    from scripts.index import EquationIndex, get_global_index

    # Import cross-domain registry
    from scripts.registry import CROSS_DOMAIN_EQUATIONS

    # Import parameter resolution layer
    from scripts.context import ComputeContext, quick_compute, explain_equation

    # Smart computation with auto-resolved parameters
    ctx = ComputeContext()
    ctx.set(Hb=15, S_O2=0.97, PO2=100)  # Aliases normalized automatically
    result = ctx.compute("blood_oxygen_content")

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher
"""

import importlib
import sys

__version__ = "3.0.0"
__author__ = "Generated from Feher QHP 3rd Edition"

# Equation statistics (kept in sync by scripts/tests/test_public_api.py)
EQUATION_COUNTS = {
    "foundations": 38,
    "membrane": 30,
    "excitable": 29,
    "nervous": 36,
    "cardiovascular": 58,
    "respiratory": 62,
    "renal": 42,
    "gastrointestinal": 41,
    "endocrine": 31,
}
TOTAL_EQUATIONS = sum(EQUATION_COUNTS.values())  # 367

# Valid submodule names for lazy loading
_SUBMODULES = {
    "foundations", "membrane", "excitable", "nervous",
    "cardiovascular", "respiratory", "renal", "gastrointestinal",
    "endocrine", "base", "index", "registry", "context", "canonical_ids",
    "parameter_ranges"
}

def __getattr__(name: str):
    """Lazy import submodules on first access using importlib."""
    if name in _SUBMODULES:
        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module  # Cache in module globals
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    # Core modules
    "base",
    "index",
    "registry",
    "context",
    "canonical_ids",
    # Domain modules (lazy loaded)
    "foundations",
    "membrane",
    "excitable",
    "nervous",
    "cardiovascular",
    "respiratory",
    "renal",
    "gastrointestinal",
    "endocrine",
]

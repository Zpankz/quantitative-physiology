"""Cross-domain equation registry.

Tracks equations used across multiple physiological domains. This is now a
*derived* artifact: cross-domain membership, primary/used-in domains, module
paths and object names all come from `scripts.canonical_ids` (the single source
of truth). Every registered entry is therefore guaranteed to resolve to a real,
importable equation object. Previously this file hard-coded a routing table
whose ids and module paths had drifted out of sync with the code.

To change cross-domain membership, edit CROSS_DOMAIN in
scripts/_build_canonical_ids.py and re-run the builder; do not edit here.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

from .base import EquationCategory
from .canonical_ids import (
    CROSS_DOMAIN as _CANON_CROSS_DOMAIN,
    CANONICAL_EQUATIONS as _CANON,
)


@dataclass
class CrossDomainEquation:
    """An equation used in multiple domains.

    Attributes:
        id: Canonical equation identifier
        name: Human-readable name
        primary_domain: The domain where the equation is defined
        used_in_domains: Other domains that use it
        module_path: Import path to the defining module
        object_name: Module-level name bound to the equation (may differ from id)
        description: Brief description of cross-domain usage
    """
    id: str
    name: str
    primary_domain: EquationCategory
    used_in_domains: List[EquationCategory]
    module_path: str
    object_name: str = ""
    description: str = ""

    def all_domains(self) -> List[EquationCategory]:
        return [self.primary_domain] + self.used_in_domains

    def is_used_in(self, domain: EquationCategory) -> bool:
        return domain == self.primary_domain or domain in self.used_in_domains


class CrossDomainRegistry:
    """Registry for tracking cross-domain equation usage and import routing."""

    def __init__(self):
        self._equations: Dict[str, CrossDomainEquation] = {}
        self._by_primary: Dict[EquationCategory, List[str]] = {}
        self._by_usage: Dict[EquationCategory, List[str]] = {}

    def register(self, equation: CrossDomainEquation) -> None:
        if equation.id in self._equations:
            raise ValueError(f"Equation '{equation.id}' already registered")
        self._equations[equation.id] = equation
        self._by_primary.setdefault(equation.primary_domain, []).append(equation.id)
        for domain in equation.all_domains():
            bucket = self._by_usage.setdefault(domain, [])
            if equation.id not in bucket:
                bucket.append(equation.id)

    def get(self, eq_id: str) -> Optional[CrossDomainEquation]:
        return self._equations.get(eq_id)

    def defined_in(self, domain: EquationCategory) -> List[CrossDomainEquation]:
        return [self._equations[e] for e in self._by_primary.get(domain, [])]

    def used_in(self, domain: EquationCategory) -> List[CrossDomainEquation]:
        return [self._equations[e] for e in self._by_usage.get(domain, [])]

    def imported_to(self, domain: EquationCategory) -> List[CrossDomainEquation]:
        return [eq for eq in self.used_in(domain) if eq.primary_domain != domain]

    def shared_between(self, domain1: EquationCategory,
                       domain2: EquationCategory) -> List[CrossDomainEquation]:
        shared = set(self._by_usage.get(domain1, [])) & set(self._by_usage.get(domain2, []))
        return [self._equations[e] for e in shared]

    def get_import_path(self, eq_id: str) -> Optional[str]:
        eq = self._equations.get(eq_id)
        return eq.module_path if eq else None

    def generate_imports(self, domain: EquationCategory) -> List[str]:
        """Generate valid Python import statements for a domain's cross-domain
        equations, grouped by module. Uses the real object name (not the id),
        so the emitted imports are guaranteed to work."""
        by_module: Dict[str, List[str]] = {}
        for eq in self.used_in(domain):
            name = eq.object_name or eq.id
            by_module.setdefault(eq.module_path, []).append(name)
        return [f"from {module} import {', '.join(sorted(names))}"
                for module, names in sorted(by_module.items())]

    def all_equations(self) -> List[CrossDomainEquation]:
        return list(self._equations.values())

    def stats(self) -> Dict[str, int]:
        total_usages = sum(len(eq.used_in_domains) + 1 for eq in self._equations.values())
        n = len(self._equations)
        return {
            "total_equations": n,
            "total_cross_domain_usages": total_usages,
            "domains_with_shared": len(self._by_usage),
            "average_domains_per_equation": (total_usages / n if n else 0),
        }


# --- Populate from the canonical id map (single source of truth) ---
CROSS_DOMAIN_EQUATIONS = CrossDomainRegistry()

for _eq_id, (_name, _primary, _used_in) in _CANON_CROSS_DOMAIN.items():
    _entry = _CANON[_eq_id]
    CROSS_DOMAIN_EQUATIONS.register(CrossDomainEquation(
        id=_eq_id,
        name=_name,
        primary_domain=EquationCategory(_primary),
        used_in_domains=[EquationCategory(d) for d in _used_in],
        module_path=_entry["module"],
        object_name=_entry["object"],
    ))


def get_cross_domain_registry() -> CrossDomainRegistry:
    """Get the pre-populated cross-domain registry."""
    return CROSS_DOMAIN_EQUATIONS


def find_shared_equations(domain1: EquationCategory,
                          domain2: EquationCategory) -> List[CrossDomainEquation]:
    """Find equations shared between two domains."""
    return CROSS_DOMAIN_EQUATIONS.shared_between(domain1, domain2)


def get_domain_imports(domain: EquationCategory) -> List[str]:
    """Get import statements for a domain's cross-domain equations."""
    return CROSS_DOMAIN_EQUATIONS.generate_imports(domain)

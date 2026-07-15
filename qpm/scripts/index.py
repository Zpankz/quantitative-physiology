"""
Equation index and registry system.

Provides multi-dimensional lookup, dependency graph management,
and topological ordering for the atomic equation system.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher
"""

from typing import Dict, List, Optional, Set, Tuple, Iterator
from collections import defaultdict
import json
from pathlib import Path

from .base import AtomicEquation, EquationCategory


class EquationIndex:
    """
    Central registry for all equations with multi-dimensional lookup.

    Provides:
    - O(1) lookup by equation ID
    - Category-based filtering
    - Unit-based filtering
    - Dependency graph traversal
    - Topological ordering for computation sequences
    - Foundation and terminal equation identification

    Usage:
        index = EquationIndex()
        index.register(nernst_equation)
        index.register(goldman_equation)

        # Lookup
        eq = index.get("nernst_potential")

        # Filter
        membrane_eqs = index.by_category(EquationCategory.MEMBRANE)
        unit5_eqs = index.by_unit(5)

        # Dependencies
        foundations = index.get_foundations()
        order = index.topological_order()
    """

    def __init__(self):
        """Initialize empty index with all lookup structures."""
        self._by_id: Dict[str, AtomicEquation] = {}
        self._by_category: Dict[EquationCategory, List[str]] = defaultdict(list)
        self._by_unit: Dict[int, List[str]] = defaultdict(list)
        self._dependency_graph: Dict[str, List[str]] = {}
        self._reverse_graph: Dict[str, List[str]] = defaultdict(list)

    def register(self, equation: AtomicEquation) -> None:
        """
        Register an equation in the index.

        Updates all lookup structures and dependency graphs.

        Args:
            equation: AtomicEquation to register

        Raises:
            ValueError: If equation with same ID already exists
        """
        if equation.id in self._by_id:
            raise ValueError(f"Equation '{equation.id}' already registered")

        # Primary index
        self._by_id[equation.id] = equation

        # Category index
        self._by_category[equation.category].append(equation.id)

        # Unit index
        if equation.metadata:
            unit = equation.metadata.source_unit
            self._by_unit[unit].append(equation.id)

        # Dependency graph (forward: what this depends on)
        self._dependency_graph[equation.id] = equation.depends_on.copy()

        # Reverse graph (backward: what depends on this)
        for dep_id in equation.depends_on:
            self._reverse_graph[dep_id].append(equation.id)

        # Update used_by for dependencies already in index
        for dep_id in equation.depends_on:
            if dep_id in self._by_id:
                self._by_id[dep_id].used_by.append(equation.id)

        # Update this equation's used_by from reverse graph
        if equation.id in self._reverse_graph:
            equation.used_by.extend(self._reverse_graph[equation.id])

    def unregister(self, eq_id: str) -> Optional[AtomicEquation]:
        """
        Remove an equation from the index.

        Args:
            eq_id: ID of equation to remove

        Returns:
            The removed equation, or None if not found
        """
        if eq_id not in self._by_id:
            return None

        equation = self._by_id.pop(eq_id)

        # Remove from category index
        self._by_category[equation.category].remove(eq_id)

        # Remove from unit index
        if equation.metadata:
            unit = equation.metadata.source_unit
            if eq_id in self._by_unit[unit]:
                self._by_unit[unit].remove(eq_id)

        # Clean up dependency graphs
        del self._dependency_graph[eq_id]
        for dep_id in equation.depends_on:
            if dep_id in self._reverse_graph:
                if eq_id in self._reverse_graph[dep_id]:
                    self._reverse_graph[dep_id].remove(eq_id)

        # Clean up used_by in dependencies
        for dep_id in equation.depends_on:
            if dep_id in self._by_id:
                dep_eq = self._by_id[dep_id]
                if eq_id in dep_eq.used_by:
                    dep_eq.used_by.remove(eq_id)

        return equation

    def get(self, eq_id: str) -> Optional[AtomicEquation]:
        """Get equation by ID, or None if not found."""
        return self._by_id.get(eq_id)

    def __getitem__(self, eq_id: str) -> AtomicEquation:
        """Get equation by ID, raises KeyError if not found."""
        return self._by_id[eq_id]

    def __contains__(self, eq_id: str) -> bool:
        """Check if equation ID is registered."""
        return eq_id in self._by_id

    def __len__(self) -> int:
        """Return number of registered equations."""
        return len(self._by_id)

    def __iter__(self) -> Iterator[AtomicEquation]:
        """Iterate over all equations."""
        return iter(self._by_id.values())

    def by_category(self, category: EquationCategory) -> List[AtomicEquation]:
        """Get all equations in a category."""
        return [self._by_id[eid] for eid in self._by_category.get(category, [])]

    def by_unit(self, unit: int) -> List[AtomicEquation]:
        """Get all equations from a specific unit."""
        return [self._by_id[eid] for eid in self._by_unit.get(unit, [])]

    def get_foundations(self) -> List[AtomicEquation]:
        """
        Return equations with no dependencies (foundational).

        These are the "leaf" nodes in the dependency graph that
        other equations build upon.
        """
        return [
            eq for eq in self._by_id.values()
            if not eq.depends_on
        ]

    def get_terminals(self) -> List[AtomicEquation]:
        """
        Return equations with no dependents (terminal).

        These are equations that nothing else builds upon,
        often representing final calculated values.
        """
        return [
            eq for eq in self._by_id.values()
            if not eq.used_by
        ]

    def get_dependents(self, eq_id: str) -> List[str]:
        """
        Return all equation IDs that depend on the given equation.

        Args:
            eq_id: Source equation ID

        Returns:
            List of equation IDs that use this equation
        """
        return self._reverse_graph.get(eq_id, []).copy()

    def get_dependencies(self, eq_id: str) -> List[str]:
        """
        Return all equation IDs that the given equation depends on.

        Args:
            eq_id: Target equation ID

        Returns:
            List of equation IDs this equation uses
        """
        return self._dependency_graph.get(eq_id, []).copy()

    def get_all_ancestors(self, eq_id: str) -> Set[str]:
        """
        Get all transitive dependencies (ancestors in DAG).

        Args:
            eq_id: Starting equation ID

        Returns:
            Set of all equation IDs this transitively depends on
        """
        ancestors = set()
        stack = list(self._dependency_graph.get(eq_id, []))

        while stack:
            current = stack.pop()
            if current not in ancestors:
                ancestors.add(current)
                stack.extend(self._dependency_graph.get(current, []))

        return ancestors

    def get_all_descendants(self, eq_id: str) -> Set[str]:
        """
        Get all transitive dependents (descendants in DAG).

        Args:
            eq_id: Starting equation ID

        Returns:
            Set of all equation IDs that transitively use this
        """
        descendants = set()
        stack = list(self._reverse_graph.get(eq_id, []))

        while stack:
            current = stack.pop()
            if current not in descendants:
                descendants.add(current)
                stack.extend(self._reverse_graph.get(current, []))

        return descendants

    def topological_order(self) -> List[str]:
        """
        Return equation IDs in dependency order (foundations first).

        Uses Kahn's algorithm for topological sort.

        Returns:
            List of equation IDs where dependencies always appear
            before equations that use them.

        Raises:
            ValueError: If a dependency references an unregistered equation
                (dangling reference), or if a genuine dependency cycle exists.
                The two are reported distinctly so a stray id is never
                misdiagnosed as a cycle.
        """
        # Guard: every dependency must reference a registered equation.
        # Without this, a dependency id that is not a node inflates the
        # dependent's in-degree, which never decrements, and Kahn's algorithm
        # misreports the dependent as part of a cycle (see detect_cycles(),
        # which would return []). Surface dangling references explicitly.
        dangling = {
            eid: [d for d in deps if d not in self._by_id]
            for eid, deps in self._dependency_graph.items()
        }
        dangling = {eid: miss for eid, miss in dangling.items() if miss}
        if dangling:
            detail = "; ".join(f"{eid} -> {miss}" for eid, miss in sorted(dangling.items()))
            raise ValueError(
                "Cannot compute topological order: dangling dependency "
                f"reference(s) to unregistered equation ids: {detail}"
            )

        # Calculate in-degree for each node (all deps now guaranteed to be nodes)
        in_degree = {eid: len(deps) for eid, deps in self._dependency_graph.items()}

        # Queue starts with nodes having no dependencies
        queue = [eid for eid, deg in in_degree.items() if deg == 0]
        result = []

        while queue:
            current = queue.pop(0)
            result.append(current)

            # Reduce in-degree for dependents
            for dependent in self._reverse_graph.get(current, []):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        # Check for genuine cycles (dangling refs already excluded above)
        if len(result) != len(self._by_id):
            remaining = set(self._by_id.keys()) - set(result)
            raise ValueError(
                f"Dependency cycle detected involving: {remaining}"
            )

        return result

    def detect_cycles(self) -> List[List[str]]:
        """
        Detect all cycles in the dependency graph.

        Returns:
            List of cycles, where each cycle is a list of equation IDs
        """
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: List[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self._dependency_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])

            path.pop()
            rec_stack.remove(node)

        for node in self._by_id:
            if node not in visited:
                dfs(node, [])

        return cycles

    def get_clusters(self) -> Dict[str, List[str]]:
        """
        Identify clusters of related equations.

        Uses connected components in undirected version of graph.

        Returns:
            Dictionary mapping cluster ID to list of equation IDs
        """
        # Build undirected adjacency
        undirected = defaultdict(set)
        for eq_id, deps in self._dependency_graph.items():
            for dep in deps:
                undirected[eq_id].add(dep)
                undirected[dep].add(eq_id)

        visited = set()
        clusters = {}
        cluster_id = 0

        def bfs(start: str) -> List[str]:
            component = []
            queue = [start]
            while queue:
                node = queue.pop(0)
                if node not in visited:
                    visited.add(node)
                    component.append(node)
                    queue.extend(undirected[node] - visited)
            return component

        for node in self._by_id:
            if node not in visited:
                component = bfs(node)
                if component:
                    clusters[f"cluster_{cluster_id}"] = component
                    cluster_id += 1

        return clusters

    def categories(self) -> List[EquationCategory]:
        """Return list of categories with equations."""
        return [cat for cat, eqs in self._by_category.items() if eqs]

    def units(self) -> List[int]:
        """Return list of units with equations."""
        return sorted([unit for unit, eqs in self._by_unit.items() if eqs])

    def stats(self) -> Dict[str, int]:
        """Return statistics about the index."""
        return {
            "total_equations": len(self._by_id),
            "foundations": len(self.get_foundations()),
            "terminals": len(self.get_terminals()),
            "categories": len(self.categories()),
            "units": len(self.units()),
            "total_dependencies": sum(
                len(deps) for deps in self._dependency_graph.values()
            )
        }

    def to_dict(self) -> Dict:
        """Export entire index to dictionary."""
        return {
            "equations": {
                eq_id: eq.to_dict()
                for eq_id, eq in self._by_id.items()
            },
            "dependency_graph": dict(self._dependency_graph),
            "stats": self.stats()
        }

    def save(self, path: Path) -> None:
        """Save index to JSON file."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'EquationIndex':
        """Load index from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)

        index = cls()
        for eq_data in data.get("equations", {}).values():
            eq = AtomicEquation.from_dict(eq_data)
            index.register(eq)

        return index


# =============================================================================
# PHASE 3 (H5): Explicit Registry Initialization System
# Addresses ERROR CLASS 5: Global state registration conflicts
#
# Design Goals:
# 1. Prevent import-order dependencies
# 2. Support testing isolation via reset
# 3. Enable lazy loading without conflicts
# 4. Allow deferred registration for batch loading
# =============================================================================

# Global singleton index
_global_index: Optional[EquationIndex] = None

# Deferred registration queue (collects equations before explicit initialization)
_deferred_equations: List[AtomicEquation] = []

# Flag to control registration behavior
_auto_register: bool = True  # Default True for backwards compatibility


def get_global_index() -> EquationIndex:
    """Get or create the global equation index."""
    global _global_index
    if _global_index is None:
        _global_index = EquationIndex()
    return _global_index


def register_equation(equation: AtomicEquation) -> None:
    """
    Register an equation in the global index.

    Behavior depends on _auto_register flag:
    - True (default): Immediate registration (backwards compatible)
    - False: Deferred registration (collected for batch initialization)

    This supports ERROR CLASS 5 prevention by allowing explicit initialization
    control for testing isolation and import order independence.
    """
    global _auto_register, _deferred_equations

    if _auto_register:
        # Immediate registration (backwards compatible behavior)
        get_global_index().register(equation)
    else:
        # Deferred registration - collect for batch initialization
        _deferred_equations.append(equation)


def get_equation(eq_id: str) -> Optional[AtomicEquation]:
    """Get an equation from the global index."""
    return get_global_index().get(eq_id)


def set_deferred_registration(enabled: bool = True) -> None:
    """
    Enable or disable deferred registration mode.

    When enabled (True):
    - Equations are queued instead of immediately registered
    - Call initialize_registry() to batch-register all queued equations

    When disabled (False):
    - Equations are registered immediately (default/backwards compatible)

    Use Cases:
    - Testing isolation: defer registration, run tests, reset
    - Controlled initialization: load modules, then initialize once
    - Import order independence: collect all equations before processing

    Example:
        set_deferred_registration(True)
        # Import modules - equations queued but not registered
        from scripts.cardiovascular import cardiac
        from scripts.respiratory import gas_exchange
        # Now initialize all at once
        initialize_registry()
    """
    global _auto_register
    _auto_register = not enabled


def initialize_registry(clear_deferred: bool = True) -> int:
    """
    Initialize the registry with all deferred equations.

    Args:
        clear_deferred: If True, clear the deferred queue after initialization

    Returns:
        Number of equations registered

    This is the explicit initialization point for PHASE 3 (H5).
    Call this after all modules are imported when using deferred mode.
    """
    global _deferred_equations

    count = 0
    index = get_global_index()

    for eq in _deferred_equations:
        try:
            index.register(eq)
            count += 1
        except ValueError as e:
            # Handle duplicate registration gracefully
            import sys
            print(f"[QP-SKILL Warning] Skipping duplicate: {e}", file=sys.stderr)

    if clear_deferred:
        _deferred_equations = []

    # Re-enable auto-registration for any subsequent equations
    global _auto_register
    _auto_register = True

    return count


def reset_registry() -> None:
    """
    Reset the global registry to a clean state.

    This is essential for:
    - Testing isolation (each test gets fresh registry)
    - Preventing state pollution between test runs
    - Debugging import order issues

    Example (pytest fixture):
        @pytest.fixture(autouse=True)
        def clean_registry():
            reset_registry()
            yield
            reset_registry()
    """
    global _global_index, _deferred_equations, _auto_register
    _global_index = None
    _deferred_equations = []
    _auto_register = True


def get_deferred_count() -> int:
    """Return number of equations waiting in deferred queue."""
    return len(_deferred_equations)


def is_deferred_mode() -> bool:
    """Return True if currently in deferred registration mode."""
    return not _auto_register

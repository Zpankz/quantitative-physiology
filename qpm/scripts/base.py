"""
Base classes for atomic equation components.

This module defines the foundational dataclasses for representing
physiological equations as atomic, interconnected components with
full dependency tracking and metadata.

Source: Quantitative Human Physiology 3rd Edition - Joseph J. Feher
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple, Any, Set
from enum import Enum
import inspect
import numpy as np


# =============================================================================
# PHASE 1: Exception Classes for Configuration Errors
# =============================================================================

class ConfigurationError(Exception):
    """
    Raised when equation configuration is invalid.

    This includes:
    - Parameter name mismatches between metadata and compute function
    - Invalid unit specifications
    - Missing required parameters
    """
    pass


class UnitConversionError(Exception):
    """Raised when unit conversion fails or is undefined."""
    pass


# =============================================================================
# PHASE 1: Signature-Metadata Validation (H1)
# =============================================================================

def validate_signature_parameters(
    compute_func: Callable,
    parameters: List['Parameter'],
    equation_id: str
) -> None:
    """
    Validate that compute function signature matches parameter metadata.

    This prevents the ERROR CLASS 1 pattern where metadata defines parameters
    with names that don't match the compute function signature (e.g., T_body vs T).

    Args:
        compute_func: The equation's compute function
        parameters: List of Parameter objects from metadata
        equation_id: Equation identifier for error messages

    Raises:
        ConfigurationError: If parameter names don't match function signature
    """
    sig = inspect.signature(compute_func)
    func_params = set(sig.parameters.keys())
    metadata_params = {p.name for p in parameters}

    # Check for parameters in metadata but not in function signature
    missing_in_func = metadata_params - func_params
    if missing_in_func:
        raise ConfigurationError(
            f"Equation '{equation_id}': Parameters {missing_in_func} defined in metadata "
            f"but not in compute function signature. "
            f"Function expects: {func_params}, metadata defines: {metadata_params}"
        )

    # Check for required function parameters not in metadata
    # (parameters with no default value must be in metadata)
    required_func_params = {
        name for name, param in sig.parameters.items()
        if param.default is inspect.Parameter.empty
    }
    missing_in_metadata = required_func_params - metadata_params
    if missing_in_metadata:
        raise ConfigurationError(
            f"Equation '{equation_id}': Required function parameters {missing_in_metadata} "
            f"not defined in metadata. Add Parameter objects for these."
        )


# =============================================================================
# PHASE 1: Unit Validation System (H4)
# =============================================================================

# Common physiological unit conversions: (from_unit, to_unit) -> multiplier
UNIT_CONVERSIONS: Dict[Tuple[str, str], float] = {
    # Volume
    ("L", "mL"): 1000.0,
    ("mL", "L"): 0.001,
    ("L", "dL"): 10.0,
    ("dL", "L"): 0.1,
    ("mL", "µL"): 1000.0,
    ("µL", "mL"): 0.001,

    # Pressure
    ("mmHg", "kPa"): 0.133322,
    ("kPa", "mmHg"): 7.50062,
    ("cmH2O", "mmHg"): 0.7355,
    ("mmHg", "cmH2O"): 1.3595,

    # Concentration
    ("M", "mM"): 1000.0,
    ("mM", "M"): 0.001,
    ("mM", "µM"): 1000.0,
    ("µM", "mM"): 0.001,
    ("g/dL", "mg/dL"): 1000.0,
    ("mg/dL", "g/dL"): 0.001,
    ("g/dL", "g/L"): 10.0,
    ("g/L", "g/dL"): 0.1,

    # Time
    ("min", "s"): 60.0,
    ("s", "min"): 1/60,
    ("h", "min"): 60.0,
    ("min", "h"): 1/60,
    ("h", "s"): 3600.0,
    ("s", "h"): 1/3600,

    # Flow
    ("L/min", "mL/min"): 1000.0,
    ("mL/min", "L/min"): 0.001,
    ("L/min", "mL/s"): 1000/60,
    ("mL/s", "L/min"): 60/1000,

    # Temperature
    ("°C", "K"): lambda x: x + 273.15,
    ("K", "°C"): lambda x: x - 273.15,
}


class UnitValidator:
    """
    Lightweight unit validation and conversion for physiological parameters.

    Addresses ERROR CLASS 4: unit convention ambiguity (e.g., SV in mL vs L).
    Uses a bounded set of common physiological conversions rather than
    full dimensional analysis.
    """

    @staticmethod
    def can_convert(from_unit: str, to_unit: str) -> bool:
        """Check if conversion between units is defined."""
        if from_unit == to_unit:
            return True
        return (from_unit, to_unit) in UNIT_CONVERSIONS

    @staticmethod
    def convert(value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert value between units.

        Args:
            value: Numerical value to convert
            from_unit: Source unit string
            to_unit: Target unit string

        Returns:
            Converted value

        Raises:
            UnitConversionError: If conversion is not defined
        """
        if from_unit == to_unit:
            return value

        conversion = UNIT_CONVERSIONS.get((from_unit, to_unit))
        if conversion is None:
            raise UnitConversionError(
                f"No conversion defined from '{from_unit}' to '{to_unit}'"
            )

        # Handle callable conversions (e.g., temperature)
        if callable(conversion):
            return conversion(value)
        return value * conversion

    @staticmethod
    def suggest_unit_issue(
        param_name: str,
        value: float,
        expected_unit: str,
        physiological_range: Optional[Tuple[float, float]]
    ) -> Optional[str]:
        """
        Suggest if value might be in wrong units based on physiological range.

        Returns a warning message if value is outside range but would be
        valid with a common unit conversion.
        """
        if physiological_range is None:
            return None

        low, high = physiological_range
        if low <= value <= high:
            return None  # Value is in range, no issue

        # Check common conversion factors
        common_factors = [1000.0, 0.001, 100.0, 0.01, 60.0, 1/60]
        for factor in common_factors:
            converted = value * factor
            if low <= converted <= high:
                if factor == 1000.0:
                    suggestion = "milli- to base"
                elif factor == 0.001:
                    suggestion = "base to milli-"
                elif factor == 100.0:
                    suggestion = "centi- to base"
                elif factor == 0.01:
                    suggestion = "base to centi-"
                elif factor == 60.0:
                    suggestion = "per-minute to per-second"
                else:
                    suggestion = "per-second to per-minute"

                return (
                    f"Parameter '{param_name}'={value} is outside physiological range "
                    f"[{low}, {high}] {expected_unit}. "
                    f"Did you mean to convert {suggestion}? "
                    f"Converted value {converted:.4g} would be in range."
                )

        return None


class EquationCategory(Enum):
    """Domain categories for physiological equations."""
    FOUNDATIONS = "foundations"
    MEMBRANE = "membrane"
    EXCITABLE = "excitable"
    NERVOUS = "nervous"
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    RENAL = "renal"
    GASTROINTESTINAL = "gastrointestinal"
    ENDOCRINE = "endocrine"


@dataclass
class Parameter:
    """
    Represents a parameter in a physiological equation.

    Attributes:
        name: Parameter identifier (e.g., 'R', 'T', 'z')
        description: Human-readable description
        units: Physical units (e.g., 'J/(mol·K)')
        symbol: LaTeX symbol representation
        default_value: Default numerical value if constant
        physiological_range: Tuple of (min, max) for validation
    """
    name: str
    description: str
    units: str
    symbol: str
    default_value: Optional[float] = None
    physiological_range: Optional[Tuple[float, float]] = None

    def __post_init__(self):
        # L4: keep physiological_range a tuple even when constructed from JSON
        # (from_dict passes a list), so save/load round-trips are type-stable.
        if self.physiological_range is not None:
            self.physiological_range = tuple(self.physiological_range)

    def validate(self, value: float) -> bool:
        """Check if value is within physiological range."""
        if self.physiological_range is None:
            return True
        low, high = self.physiological_range
        return low <= value <= high

    def to_dict(self) -> Dict[str, Any]:
        """Export to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "units": self.units,
            "symbol": self.symbol,
            "default_value": self.default_value,
            "physiological_range": self.physiological_range
        }


@dataclass
class EquationMetadata:
    """
    Source metadata for equation provenance tracking.

    Attributes:
        source_unit: Unit number (1-9) from textbook
        source_chapter: Chapter identifier (e.g., '5.3')
        source_section: Section within chapter
        page_reference: Page number in textbook
        textbook_equation_number: Original equation number if labeled
    """
    source_unit: int
    source_chapter: str
    source_section: Optional[str] = None
    page_reference: Optional[int] = None
    textbook_equation_number: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Export to dictionary for JSON serialization."""
        return {
            "source_unit": self.source_unit,
            "source_chapter": self.source_chapter,
            "source_section": self.source_section,
            "page_reference": self.page_reference,
            "textbook_equation_number": self.textbook_equation_number
        }


@dataclass
class AtomicEquation:
    """
    Base class for all atomic equation components.

    Each equation is a self-contained unit with:
    - Mathematical definition (LaTeX and simplified forms)
    - Dependency tracking (what it builds on, what uses it)
    - Parameter specifications with validation
    - Computational implementation
    - Source metadata for provenance

    Attributes:
        id: Unique identifier (e.g., 'nernst_potential')
        name: Human-readable name (e.g., 'Nernst Equation')
        category: Domain category (EquationCategory enum)
        latex: Full LaTeX representation
        simplified: ASCII-friendly simplified form
        description: Explanation of the equation's purpose
        depends_on: List of equation IDs this builds upon
        used_by: List of equation IDs that use this (populated by index)
        parameters: List of Parameter objects
        metadata: Source provenance information
    """
    id: str
    name: str
    category: EquationCategory
    latex: str
    simplified: str
    description: str

    # Dependency tracking
    depends_on: List[str] = field(default_factory=list)
    used_by: List[str] = field(default_factory=list)

    # Parameters
    parameters: List[Parameter] = field(default_factory=list)

    # Metadata
    metadata: Optional[EquationMetadata] = None

    # Output binding (H3): canonical parameter name this equation's result
    # represents (e.g. cardiac_output -> "CO"). Lets ComputeContext bind this
    # equation's computed value to a downstream consumer's parameter of that
    # name. When None, the equation id (normalized through the parameter-alias
    # table) is used as the output name, which already covers equations whose id
    # is a known alias of their output quantity.
    produces: Optional[str] = None

    # Units of the value returned by compute() (e.g. "mmHg", "mL/min", "V").
    # Optional and backward-compatible: None means "not declared". Parsed by
    # scripts.dimensions.parse() into a dimension vector for the graph layer.
    output_units: Optional[str] = None

    # Implementation (set after instantiation)
    _compute_func: Optional[Callable] = field(default=None, repr=False)

    def compute(self, **kwargs) -> float:
        """
        Execute the equation's computational implementation.

        Args:
            **kwargs: Parameter values matching parameter names

        Returns:
            Computed result

        Raises:
            NotImplementedError: If no compute function is set
        """
        if self._compute_func is None:
            raise NotImplementedError(
                f"Compute function not implemented for '{self.id}'"
            )
        return self._compute_func(**kwargs)

    def set_compute_func(self, func: Callable) -> None:
        """Set the computational implementation function."""
        self._compute_func = func

    def validate_inputs(self, **kwargs) -> Tuple[bool, List[str]]:
        """
        Validate inputs against physiological ranges.

        Args:
            **kwargs: Parameter values to validate

        Returns:
            Tuple of (is_valid, list of validation error messages)
        """
        errors = []
        for param in self.parameters:
            if param.name in kwargs:
                val = kwargs[param.name]
                if not param.validate(val):
                    low, high = param.physiological_range
                    errors.append(
                        f"{param.name}={val} outside range [{low}, {high}]"
                    )
        return len(errors) == 0, errors

    def get_parameter(self, name: str) -> Optional[Parameter]:
        """Get a parameter by name."""
        for param in self.parameters:
            if param.name == name:
                return param
        return None

    @property
    def dimensional_form(self) -> Optional[dict]:
        """The equation's OUTPUT dimension expressed as a product of its PARAMETER
        dimensions — the exponents whose product yields the output, rendered as e.g.
        ``'rho*v*d/eta'`` in ``['expression']``. For a dimensionless output this is
        the cancellation relation (Reynolds = rho*v*d/eta), linking the pure number
        to the dimensional quantities it is built from. Derived from the parameters
        (the source of truth), then cached onto the object; ``None`` if the output
        or parameters carry no resolvable dimensions."""
        cached = self.__dict__.get("_dimensional_form", False)
        if cached is not False:
            return cached
        from scripts.dimform import cancellation
        val = cancellation({p.name: p.units for p in self.parameters},
                           self.output_units)
        self.__dict__["_dimensional_form"] = val
        return val

    def get_default_kwargs(self) -> Dict[str, float]:
        """Get dictionary of parameters with default values."""
        return {
            p.name: p.default_value
            for p in self.parameters
            if p.default_value is not None
        }

    def to_dict(self) -> Dict[str, Any]:
        """Export to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category.value,
            "latex": self.latex,
            "simplified": self.simplified,
            "description": self.description,
            "depends_on": self.depends_on,
            "used_by": self.used_by,
            "produces": self.produces,
            "output_units": self.output_units,
            "parameters": [p.to_dict() for p in self.parameters],
            "metadata": self.metadata.to_dict() if self.metadata else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AtomicEquation':
        """Create an AtomicEquation from a dictionary."""
        params = [
            Parameter(**p) for p in data.get("parameters", [])
        ]
        metadata = None
        if data.get("metadata"):
            metadata = EquationMetadata(**data["metadata"])

        return cls(
            id=data["id"],
            name=data["name"],
            category=EquationCategory(data["category"]),
            latex=data["latex"],
            simplified=data["simplified"],
            description=data["description"],
            depends_on=data.get("depends_on", []),
            used_by=data.get("used_by", []),
            produces=data.get("produces"),
            output_units=data.get("output_units"),
            parameters=params,
            metadata=metadata
        )

    def __hash__(self):
        """Enable use in sets and as dict keys."""
        return hash(self.id)

    def __eq__(self, other):
        """Equality based on ID."""
        if isinstance(other, AtomicEquation):
            return self.id == other.id
        return False


# Physical constants used across equations
PHYSICAL_CONSTANTS = {
    "R": Parameter(
        name="R",
        description="Universal gas constant",
        units="J/(mol·K)",
        symbol="R",
        default_value=8.314
    ),
    "F": Parameter(
        name="F",
        description="Faraday constant",
        units="C/mol",
        symbol="F",
        default_value=96485.0
    ),
    "k_B": Parameter(
        name="k_B",
        description="Boltzmann constant",
        units="J/K",
        symbol="k_B",
        default_value=1.38e-23
    ),
    "N_A": Parameter(
        name="N_A",
        description="Avogadro's number",
        units="1/mol",
        symbol="N_A",
        default_value=6.022e23
    ),
    "T_body": Parameter(
        name="T_body",
        description="Normal body temperature",
        units="K",
        symbol="T",
        default_value=310.0,  # 37°C
        physiological_range=(306.0, 315.0)  # 33-42°C
    ),
}


# =============================================================================
# PHASE 2: Hierarchical Equation ID System (H3)
# =============================================================================

def suggest_hierarchical_id(flat_id: str, category: EquationCategory) -> str:
    """
    Suggest a hierarchical ID based on category and flat ID.

    Hierarchical IDs follow the pattern: domain.subdomain.name
    This helps prevent ERROR CLASS 3 (duplicate equation IDs) by namespacing.

    Args:
        flat_id: Original flat equation ID (e.g., 'cardiac_output')
        category: EquationCategory for domain context

    Returns:
        Suggested hierarchical ID (e.g., 'cardiovascular.cardiac.cardiac_output')

    Examples:
        >>> suggest_hierarchical_id('cardiac_output', EquationCategory.CARDIOVASCULAR)
        'cardiovascular.cardiac.cardiac_output'
        >>> suggest_hierarchical_id('nernst_equation', EquationCategory.FOUNDATIONS)
        'foundations.thermodynamics.nernst_equation'
    """
    domain = category.value

    # Subdomain inference based on common patterns
    subdomain_patterns = {
        EquationCategory.FOUNDATIONS: {
            'diffusion': 'diffusion',
            'fick': 'diffusion',
            'poiseuille': 'transport',
            'laplace': 'transport',
            'hydraulic': 'transport',
            'gibbs': 'thermodynamics',
            'nernst': 'thermodynamics',
            'boltzmann': 'thermodynamics',
            'entropy': 'thermodynamics',
            'henderson': 'thermodynamics',
            'michaelis': 'kinetics',
            'hill': 'kinetics',
            'enzyme': 'kinetics',
        },
        EquationCategory.MEMBRANE: {
            'donnan': 'potential',
            'goldman': 'potential',
            'ghk': 'potential',
            'capacitance': 'structure',
            'permeability': 'structure',
            'channel': 'transport',
            'pump': 'transport',
            'carrier': 'transport',
            'osmotic': 'osmosis',
            'receptor': 'signaling',
            'scatchard': 'signaling',
        },
        EquationCategory.CARDIOVASCULAR: {
            'cardiac': 'cardiac',
            'output': 'cardiac',
            'ejection': 'cardiac',
            'starling': 'cardiac',
            'espvr': 'cardiac',
            'map': 'hemodynamics',
            'pressure': 'hemodynamics',
            'tpr': 'hemodynamics',
            'compliance': 'hemodynamics',
            'resistance': 'hemodynamics',
            'hematocrit': 'blood',
            'oxygen_content': 'blood',
            'hemoglobin': 'blood',
            'ecg': 'ecg',
            'qt': 'ecg',
            'heart_rate': 'ecg',
            'starling_force': 'microcirculation',
            'capillary': 'microcirculation',
            'shear': 'microcirculation',
        },
        EquationCategory.RESPIRATORY: {
            'compliance': 'mechanics',
            'resistance': 'mechanics',
            'work': 'mechanics',
            'alveolar': 'gas_exchange',
            'diffusing': 'gas_exchange',
            'oxygen': 'oxygen_transport',
            'hill': 'oxygen_transport',
            'saturation': 'oxygen_transport',
            'dead_space': 'ventilation',
            'ventilation': 'ventilation',
            'henderson': 'acid_base',
            'anion': 'acid_base',
            'chemoreceptor': 'control',
            'ventilatory': 'control',
        },
        EquationCategory.RENAL: {
            'rpf': 'blood_flow',
            'rbf': 'blood_flow',
            'autoregulation': 'blood_flow',
            'gfr': 'glomerular',
            'nfp': 'glomerular',
            'filtration': 'glomerular',
            'clearance': 'clearance',
            'filtered': 'clearance',
            'fractional': 'tubular',
            'tm': 'tubular',
            'reabsorption': 'tubular',
            'countercurrent': 'concentration',
            'adh': 'concentration',
            'concentrating': 'concentration',
            'nae': 'acid_base',
            'hco3': 'acid_base',
        },
        EquationCategory.GASTROINTESTINAL: {
            'gastric_emptying': 'motility',
            'peristalsis': 'motility',
            'gastric_acid': 'secretion',
            'pancreatic': 'secretion',
            'enzyme': 'digestion',
            'lipase': 'digestion',
            'sglt': 'absorption',
            'iron': 'absorption',
            'calcium_absorption': 'absorption',
            'gastrin': 'hormones',
            'cck': 'hormones',
            'glp': 'hormones',
            'hepatic': 'liver',
            'first_pass': 'liver',
        },
        EquationCategory.ENDOCRINE: {
            'kd': 'kinetics',
            'mcr': 'kinetics',
            'half_life': 'kinetics',
            'occupancy': 'receptor',
            'feedback': 'feedback',
            't4': 'thyroid',
            't3': 'thyroid',
            'thyroid': 'thyroid',
            'cortisol': 'adrenal',
            'insulin': 'pancreatic',
            'glucose': 'pancreatic',
            'pth': 'calcium',
            'vitamin_d': 'calcium',
            'lh': 'reproductive',
            'menstrual': 'reproductive',
        },
    }

    # Try to infer subdomain from ID patterns
    subdomain = 'general'
    patterns = subdomain_patterns.get(category, {})
    for pattern, sub in patterns.items():
        if pattern in flat_id.lower():
            subdomain = sub
            break

    return f"{domain}.{subdomain}.{flat_id}"


def parse_hierarchical_id(equation_id: str) -> Dict[str, str]:
    """
    Parse a hierarchical equation ID into components.

    Args:
        equation_id: Either hierarchical (domain.subdomain.name) or flat (name)

    Returns:
        Dictionary with 'domain', 'subdomain', 'name', and 'is_hierarchical' keys

    Examples:
        >>> parse_hierarchical_id('cardiovascular.cardiac.cardiac_output')
        {'domain': 'cardiovascular', 'subdomain': 'cardiac', 'name': 'cardiac_output', 'is_hierarchical': True}
        >>> parse_hierarchical_id('cardiac_output')
        {'domain': None, 'subdomain': None, 'name': 'cardiac_output', 'is_hierarchical': False}
    """
    parts = equation_id.split('.')

    if len(parts) >= 3:
        # Full hierarchical ID: domain.subdomain.name (or domain.subdomain.subsubdomain.name)
        return {
            'domain': parts[0],
            'subdomain': parts[1],
            'name': '.'.join(parts[2:]),  # Handle nested names
            'is_hierarchical': True
        }
    elif len(parts) == 2:
        # Partial hierarchical ID: domain.name
        return {
            'domain': parts[0],
            'subdomain': None,
            'name': parts[1],
            'is_hierarchical': True
        }
    else:
        # Flat ID
        return {
            'domain': None,
            'subdomain': None,
            'name': equation_id,
            'is_hierarchical': False
        }


def validate_equation_id(
    equation_id: str,
    category: EquationCategory,
    warn_flat_ids: bool = True
) -> Optional[str]:
    """
    Validate equation ID format and return warning if flat ID detected.

    For Phase 2 (H3), we prefer hierarchical IDs but maintain backwards
    compatibility with flat IDs. This function issues warnings for flat IDs
    to encourage migration to hierarchical format.

    Args:
        equation_id: The equation ID to validate
        category: EquationCategory for context
        warn_flat_ids: If True, return warning message for flat IDs

    Returns:
        Warning message string if flat ID detected, None if hierarchical

    Note:
        This does NOT raise exceptions - flat IDs are allowed but discouraged.
        The warning can be used for logging or developer feedback.
    """
    parsed = parse_hierarchical_id(equation_id)

    if parsed['is_hierarchical']:
        # Validate that domain matches category
        expected_domain = category.value
        if parsed['domain'] != expected_domain:
            return (
                f"ID '{equation_id}' has domain '{parsed['domain']}' but "
                f"category is '{expected_domain}'. Consider using "
                f"'{expected_domain}.{parsed['subdomain'] or 'general'}.{parsed['name']}'"
            )
        return None

    if warn_flat_ids:
        suggested = suggest_hierarchical_id(equation_id, category)
        return (
            f"Flat ID '{equation_id}' detected. For better organization and "
            f"to prevent ID collisions, consider using hierarchical ID: '{suggested}'"
        )

    return None


# M2: Flat-id migration warnings are opt-in (off by default). The library uses
# flat ids by design; emitting a warning for all ~249 equations on every import
# only trains users to ignore stderr. Set env QP_WARN_FLAT_ID=1 (or true/yes/on)
# to re-enable, e.g. during a migration to hierarchical ids.
import os as _os
WARN_ON_FLAT_ID: bool = _os.environ.get("QP_WARN_FLAT_ID", "").strip().lower() in ("1", "true", "yes", "on")


def create_equation(
    id: str,
    name: str,
    category: EquationCategory,
    latex: str,
    simplified: str,
    description: str,
    compute_func: Callable,
    parameters: Optional[List[Parameter]] = None,
    depends_on: Optional[List[str]] = None,
    metadata: Optional[EquationMetadata] = None,
    produces: Optional[str] = None,
    output_units: Optional[str] = None
) -> AtomicEquation:
    """
    Factory function to create an AtomicEquation with compute function.

    This is the recommended way to create equations as it ensures
    the compute function is properly attached.

    Args:
        id: Unique identifier
        name: Human-readable name
        category: Domain category
        latex: LaTeX representation
        simplified: ASCII representation
        description: Equation explanation
        compute_func: Callable that implements the equation
        parameters: List of parameters (optional)
        depends_on: List of dependency equation IDs (optional)
        metadata: Source metadata (optional)

    Returns:
        Fully configured AtomicEquation instance
    """
    # Resolve parameters list
    params = parameters or []

    # PHASE 1 (H1): Validate signature matches metadata BEFORE creating equation
    # This prevents ERROR CLASS 1: parameter name mismatches (e.g., T_body vs T)
    validate_signature_parameters(compute_func, params, id)

    # PHASE 2 (H3): Validate equation ID format and warn about flat IDs
    # This helps prevent ERROR CLASS 3: duplicate equation IDs by encouraging namespacing
    id_warning = validate_equation_id(id, category, warn_flat_ids=WARN_ON_FLAT_ID)
    if id_warning:
        # Non-blocking warning - prints to stderr but doesn't raise exception
        # This maintains backwards compatibility while encouraging hierarchical IDs
        import sys
        print(f"[QP-SKILL Warning] {id_warning}", file=sys.stderr)

    eq = AtomicEquation(
        id=id,
        name=name,
        category=category,
        latex=latex,
        simplified=simplified,
        description=description,
        parameters=params,
        depends_on=depends_on or [],
        metadata=metadata,
        produces=produces,
        output_units=output_units
    )
    eq.set_compute_func(compute_func)
    return eq

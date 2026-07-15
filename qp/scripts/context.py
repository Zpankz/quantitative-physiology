"""Parameter Resolution Layer for QP-SKILL v3.0.0.

Provides automatic parameter linking, alias normalization, dependency resolution,
and dynamic prompting for missing parameters.

Usage:
    from scripts.context import ComputeContext

    ctx = ComputeContext()
    ctx.set(Hb=15, S_O2=0.97, P_O2=100)

    result = ctx.compute("blood_oxygen_content")
    if result.success:
        print(f"CaO2 = {result.value:.2f} mL O2/dL")
    else:
        print(result.prompt_for_missing())
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Tuple, Callable
import math

# Import Unit Validator from base module (Phase 1 - H4)
from .base import UnitValidator


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ParameterRequirement:
    """Structured representation of a missing/required parameter."""
    name: str
    description: str
    units: str
    symbol: str
    default_value: Optional[float] = None
    physiological_range: Optional[Tuple[float, float]] = None
    source_equation: str = ""

    def to_prompt(self) -> str:
        """Generate human-readable prompt for this parameter."""
        parts = [f"  • {self.name}: {self.description}"]
        if self.units and self.units != "dimensionless":
            parts[0] += f" [{self.units}]"
        if self.physiological_range:
            low, high = self.physiological_range
            parts.append(f"    Normal range: {low} - {high}")
        if self.default_value is not None:
            parts.append(f"    Default: {self.default_value}")
        return "\n".join(parts)


@dataclass
class ComputeResult:
    """Result of computation with full context."""
    value: Optional[float] = None
    success: bool = False
    equation_id: str = ""
    equation_name: str = ""
    missing_params: List[ParameterRequirement] = field(default_factory=list)
    used_params: Dict[str, float] = field(default_factory=dict)
    computed_dependencies: Dict[str, float] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)

    def prompt_for_missing(self) -> str:
        """Generate prompt text for all missing parameters."""
        if not self.missing_params:
            return ""
        lines = [f"Missing parameters for '{self.equation_id}':"]
        for req in self.missing_params:
            lines.append(req.to_prompt())
        return "\n".join(lines)

    def summary(self) -> str:
        """Generate human-readable summary of computation."""
        if self.success:
            parts = [f"✓ {self.equation_name}: {self.value}"]
            if self.used_params:
                param_strs = [f"{k}={v}" for k, v in self.used_params.items()]
                parts.append(f"  Used: {', '.join(param_strs)}")
            if self.computed_dependencies:
                dep_strs = [f"{k}={v:.4g}" for k, v in self.computed_dependencies.items()]
                parts.append(f"  Dependencies computed: {', '.join(dep_strs)}")
            return "\n".join(parts)
        else:
            parts = [f"✗ {self.equation_id} failed"]
            if self.missing_params:
                parts.append(self.prompt_for_missing())
            if self.warnings:
                for w in self.warnings:
                    parts.append(f"  ⚠ {w}")
            return "\n".join(parts)


# =============================================================================
# PARAMETER ALIASES
# =============================================================================

# Comprehensive mapping of parameter aliases to canonical names
# Canonical name is the key; aliases are the set of alternative names
PARAMETER_ALIASES: Dict[str, Set[str]] = {
    # === Partial Pressures ===
    "PO2": {"P_O2", "pO2", "p_o2", "partial_pressure_O2", "oxygen_partial_pressure"},
    "PCO2": {"P_CO2", "pCO2", "p_co2", "partial_pressure_CO2", "carbon_dioxide_partial_pressure"},
    "P_iO2": {"PIO2", "P_IO2", "Pi_O2", "p_io2", "inspired_O2", "inspired_oxygen_pressure"},
    "P_ACO2": {"PACO2", "P_A_CO2", "alveolar_CO2", "alveolar_carbon_dioxide"},
    "P_AO2": {"PAO2", "P_A_O2", "alveolar_O2", "alveolar_oxygen"},
    "PaO2": {"Pa_O2", "arterial_O2", "arterial_oxygen_pressure"},
    "PaCO2": {"Pa_CO2", "arterial_CO2", "arterial_carbon_dioxide"},
    "P_50": {"P50", "p50", "half_saturation_pressure"},

    # === Concentrations ===
    "C_out": {"C_o", "Co", "c_out", "concentration_out", "external_concentration", "extracellular"},
    "C_in": {"C_i", "Ci", "c_in", "concentration_in", "internal_concentration", "intracellular"},
    "HCO3": {"HCO3_minus", "bicarbonate", "bicarb", "HCO3-"},
    "CaO2": {"C_aO2", "Ca_O2", "arterial_O2_content", "arterial_oxygen_content"},
    "CvO2": {"C_vO2", "Cv_O2", "venous_O2_content", "venous_oxygen_content"},

    # === Hemoglobin & Blood ===
    "Hb": {"hemoglobin", "hgb", "HGB", "Hemoglobin", "haemoglobin"},
    "S_O2": {"SO2", "saturation", "oxygen_saturation", "SpO2", "SaO2", "O2_sat"},
    "Hct": {"hematocrit", "HCT", "haematocrit", "packed_cell_volume", "PCV"},

    # === Cardiovascular ===
    "CO": {"cardiac_output", "Q_cardiac", "Qc", "Q_heart"},
    "HR": {"heart_rate", "HeartRate", "heart_rate_bpm", "rate"},
    "SV": {"stroke_volume", "StrokeVolume", "stroke_vol"},
    "EDV": {"end_diastolic_volume", "LVEDV"},
    "ESV": {"end_systolic_volume", "LVESV"},
    "EF": {"ejection_fraction", "EjectionFraction"},
    "MAP": {"mean_arterial_pressure", "MeanArterialPressure", "mean_BP"},
    "SBP": {"systolic_BP", "systolic", "systolic_pressure"},
    "DBP": {"diastolic_BP", "diastolic", "diastolic_pressure"},
    "PP": {"pulse_pressure", "PulsePressure"},
    # SVR_wood is map_from_flow's Wood-unit resistance param (mmHg*min/L) — same
    # quantity/units as TPR, so total_peripheral_resistance now feeds map_from_flow.
    # (svr_dyn's SVR output is dyn*s/cm^5 — a different scale — so it is NOT wired here.)
    "TPR": {"total_peripheral_resistance", "SVR", "systemic_vascular_resistance", "SVR_wood"},
    "CVP": {"central_venous_pressure", "venous_pressure"},

    # === Respiratory ===
    "V_T": {"VT", "tidal_volume", "TidalVolume", "Vt"},
    "V_D": {"VD", "dead_space", "DeadSpace", "Vd", "dead_space_volume"},
    "V_A": {"VA", "alveolar_ventilation", "AlveolarVentilation"},
    "RR": {"respiratory_rate", "RespiratoryRate", "breathing_rate", "f"},
    "FRC": {"functional_residual_capacity"},
    "TLC": {"total_lung_capacity"},
    "VC": {"vital_capacity", "VitalCapacity"},
    "RV": {"residual_volume", "ResidualVolume"},
    "R_resp": {"respiratory_quotient", "RQ", "R"},
    "DL_CO": {"DLCO", "diffusing_capacity", "DiffusingCapacity", "D_L"},

    # === Renal ===
    "GFR": {"glomerular_filtration_rate", "filtration_rate"},
    "RPF": {"renal_plasma_flow", "plasma_flow"},
    "RBF": {"renal_blood_flow", "kidney_blood_flow"},
    "K_f": {"Kf", "ultrafiltration_coefficient", "filtration_coefficient"},
    "NFP": {"net_filtration_pressure", "filtration_pressure"},
    "FF": {"filtration_fraction", "FiltrationFraction"},
    "U_x": {"Ux", "urine_concentration", "urinary_concentration"},
    "P_x": {"Px", "plasma_concentration"},
    "V_dot": {"urine_flow", "urine_flow_rate", "V_urine"},
    "C_x": {"Cx", "clearance"},
    "FE_x": {"FEx", "fractional_excretion"},
    "T_m": {"Tm", "transport_maximum", "tubular_maximum"},

    # === Physical Constants ===
    "R": {"gas_constant", "R_gas", "universal_gas_constant"},
    "F": {"faraday", "faraday_constant", "F_const"},
    "T": {"temperature", "temp", "T_kelvin", "absolute_temperature"},
    "z": {"valence", "charge", "ion_valence", "ion_charge"},

    # === Physical Properties ===
    "eta": {"viscosity", "η", "mu", "dynamic_viscosity"},
    "r": {"radius", "vessel_radius", "tube_radius"},
    "L": {"length", "vessel_length", "tube_length"},
    "D": {"diffusion_coefficient", "diffusivity", "D_eff"},
    "A": {"area", "cross_sectional_area", "surface_area"},
    "P": {"pressure", "hydrostatic_pressure"},
    "delta_P": {"pressure_difference", "ΔP", "dP", "pressure_gradient"},

    # === Kinetics ===
    "V_max": {"Vmax", "maximum_velocity", "max_rate"},
    "K_m": {"Km", "michaelis_constant", "Michaelis_constant"},
    "K_d": {"Kd", "dissociation_constant"},
    "k": {"rate_constant", "k_rate"},
    "n": {"hill_coefficient", "Hill_coefficient", "cooperativity"},
    "t_half": {"half_life", "t1_2", "t_1_2"},

    # === Membrane ===
    "V_m": {"Vm", "membrane_potential", "resting_potential", "Em"},
    "g": {"conductance", "membrane_conductance"},
    "C_m": {"Cm", "membrane_capacitance", "capacitance"},
    "R_m": {"Rm", "membrane_resistance", "resistance"},
    "P_K": {"PK", "potassium_permeability", "K_permeability"},
    "P_Na": {"PNa", "sodium_permeability", "Na_permeability"},
    "P_Cl": {"PCl", "chloride_permeability", "Cl_permeability"},

    # === Endocrine ===
    "MCR": {"metabolic_clearance_rate", "clearance_rate"},
    "PR": {"production_rate", "secretion_rate"},
    "k_el": {"elimination_constant", "elimination_rate"},
}

# =============================================================================
# DOMAIN-SCOPED ALIAS RESOLUTION (H2)
# =============================================================================

# Domain-specific parameter overrides for ambiguous names
# Key = domain name, Value = dict mapping ambiguous alias → canonical for that domain
DOMAIN_ALIASES: Dict[str, Dict[str, str]] = {
    "respiratory": {
        "R": "R_resp",           # R = respiratory quotient (0.8), not gas constant
        "V": "V_tidal",          # V = tidal volume, not generic volume
        "C": "C_lung",           # C = lung compliance
    },
    "cardiovascular": {
        "R": "R",                # R = gas constant (default)
        "V": "V_blood",          # V = blood volume
        "C": "C_vessel",         # C = vessel compliance
        "Q": "Q_cardiac",        # Q = cardiac output
    },
    "renal": {
        "C": "C_clearance",      # C = clearance
        "V": "V_urine",          # V = urine volume
        "GFR": "GFR",            # Keep as-is
    },
    "membrane": {
        "R": "R",                # R = gas constant (thermodynamics)
        "C": "C_membrane",       # C = membrane capacitance
        "G": "G_conductance",    # G = conductance
    },
    "foundations": {
        "R": "R",                # R = gas constant (thermodynamics default)
        "D": "D_diffusion",      # D = diffusion coefficient
    },
    "excitable": {
        "R": "R",                # R = gas constant
        "G": "G_conductance",    # G = conductance
        "C": "C_membrane",       # C = membrane capacitance
    },
    "kinetics": {
        "V": "V_max",            # V = Vmax in Michaelis-Menten
        "K": "K_m",              # K = Michaelis constant
    },
}


def get_domain_from_equation_id(equation_id: str) -> Optional[str]:
    """Extract domain from equation ID.

    Supports both flat IDs (tries to infer domain) and hierarchical IDs.

    Examples:
        "cardiovascular.blood.oxygen_content" -> "cardiovascular"
        "alveolar_gas_equation" -> "respiratory" (if registered)
        "nernst_equation" -> "foundations" (if registered)

    Args:
        equation_id: Equation identifier (flat or hierarchical)

    Returns:
        Domain string or None if cannot determine
    """
    # Check for hierarchical ID (domain.subdomain.name)
    if "." in equation_id:
        return equation_id.split(".")[0]

    # For flat IDs, check if equation is registered and get its category
    try:
        index = get_global_index()
        eq = index.get(equation_id)
        if eq and eq.category:
            return eq.category.value
    except Exception:
        pass

    return None


def get_domain_aliases(domain: Optional[str]) -> Dict[str, str]:
    """Get domain-specific alias overrides.

    Args:
        domain: Domain name (e.g., "respiratory", "cardiovascular")

    Returns:
        Dict mapping ambiguous aliases to domain-appropriate canonical names
    """
    if domain and domain in DOMAIN_ALIASES:
        return DOMAIN_ALIASES[domain]
    return {}


# Build reverse lookup for O(1) alias resolution
_ALIAS_TO_CANONICAL: Dict[str, str] = {}
for canonical, aliases in PARAMETER_ALIASES.items():
    _ALIAS_TO_CANONICAL[canonical] = canonical
    for alias in aliases:
        _ALIAS_TO_CANONICAL[alias] = canonical


def normalize_param_name(
    name: str,
    custom_aliases: Optional[Dict[str, str]] = None,
    domain: Optional[str] = None
) -> str:
    """Convert any alias to canonical parameter name with domain awareness.

    Resolution order (first match wins):
    1. custom_aliases (explicit overrides)
    2. DOMAIN_ALIASES[domain] (domain-specific disambiguation)
    3. _ALIAS_TO_CANONICAL (global alias registry)
    4. Original name (passthrough)

    Args:
        name: Parameter name (may be alias or canonical)
        custom_aliases: Optional dict mapping alias → canonical for explicit overrides
        domain: Optional domain name for domain-scoped alias resolution

    Returns:
        Canonical parameter name, or original name if no alias found

    Examples:
        >>> normalize_param_name("R", domain="respiratory")
        "R_resp"  # Respiratory quotient
        >>> normalize_param_name("R", domain="foundations")
        "R"  # Gas constant
        >>> normalize_param_name("RQ")  # Already canonical
        "R_resp"
    """
    # Priority 1: Custom aliases (explicit overrides)
    if custom_aliases and name in custom_aliases:
        return custom_aliases[name]

    # Priority 2: Domain-specific disambiguation
    domain_overrides = get_domain_aliases(domain)
    if name in domain_overrides:
        return domain_overrides[name]

    # Priority 3: Global alias registry
    return _ALIAS_TO_CANONICAL.get(name, name)


def get_aliases(canonical_name: str) -> Set[str]:
    """Get all known aliases for a canonical parameter name."""
    if canonical_name in PARAMETER_ALIASES:
        return PARAMETER_ALIASES[canonical_name] | {canonical_name}
    return {canonical_name}


# =============================================================================
# COMPUTE CONTEXT
# =============================================================================

class ComputeContext:
    """Smart computation context with parameter resolution and dependency chaining.

    Features:
    - Parameter alias normalization (P_O2, PO2, pO2 → canonical form)
    - Automatic dependency resolution (computes required upstream equations)
    - Instance-level result caching with cycle detection
    - Dynamic prompting for missing parameters
    - Physiological range validation with warnings

    Usage:
        ctx = ComputeContext()
        ctx.set(Hb=15, S_O2=0.97, PO2=100)

        # Compute single equation
        result = ctx.compute("blood_oxygen_content")

        # Compute with dependencies
        result = ctx.compute("systemic_oxygen_delivery")

        # Get parameter requirements
        print(ctx.explain("alveolar_gas_equation"))
    """

    def __init__(self, custom_aliases: Optional[Dict[str, str]] = None):
        """Initialize compute context.

        Args:
            custom_aliases: Optional dict mapping alias → canonical for domain-specific overrides
        """
        self.known_values: Dict[str, float] = {}
        self.computed_cache: Dict[str, float] = {}
        self.custom_aliases = custom_aliases or {}
        self._resolution_stack: Set[str] = set()  # Cycle detection
        self._index = None
        self._current_domain: Optional[str] = None  # Phase 2 (H2): Domain for alias resolution

    @property
    def index(self):
        """Lazy-load the global equation index, auto-importing all domain packages
        so a fresh ComputeContext() works without the caller pre-importing them
        (fixes the empty-index footgun)."""
        if self._index is None:
            from .index import get_global_index
            idx = get_global_index()
            if len(idx) == 0:  # empty registry -> populate it (non-validating check)
                import importlib
                for dom in ("foundations", "membrane", "excitable", "nervous",
                            "cardiovascular", "respiratory", "renal",
                            "gastrointestinal", "endocrine"):
                    importlib.import_module(f"scripts.{dom}")
                idx = get_global_index()
            self._index = idx
        return self._index

    def set(self, **values) -> "ComputeContext":
        """Set known values with alias normalization.

        Args:
            **values: Parameter name-value pairs (aliases accepted)

        Returns:
            self for method chaining
        """
        for name, value in values.items():
            canonical = normalize_param_name(name, self.custom_aliases)
            self.known_values[canonical] = value
        return self

    def clear_cache(self) -> "ComputeContext":
        """Clear computed value cache (keeps known values)."""
        self.computed_cache.clear()
        return self

    def reset(self) -> "ComputeContext":
        """Clear all known values and cache."""
        self.known_values.clear()
        self.computed_cache.clear()
        return self

    def _normalize(self, name: str) -> str:
        """Normalize parameter name using context's alias settings and current domain.

        Phase 2 (H2): Domain-aware normalization resolves ambiguous parameters
        like 'R' differently based on equation domain (respiratory vs foundations).
        """
        return normalize_param_name(name, self.custom_aliases, self._current_domain)

    def _resolve_param(self, param_name: str, eq_params: dict,
                       overrides: dict) -> Tuple[Optional[float], Optional[ParameterRequirement]]:
        """Resolve a single parameter value.

        Resolution order:
        1. Explicit overrides (highest priority)
        2. Known values (set via ctx.set())
        3. Computed cache (results from dependency computation)
        4. Parameter default value
        5. Missing (returns ParameterRequirement for prompting)

        Args:
            param_name: Original parameter name from equation
            eq_params: Dict of Parameter objects keyed by name
            overrides: Dict of override values

        Returns:
            Tuple of (resolved_value, requirement_if_missing)
        """
        canonical = self._normalize(param_name)
        param = eq_params.get(param_name)

        # 1. Check explicit overrides
        if canonical in overrides:
            return overrides[canonical], None
        if param_name in overrides:
            return overrides[param_name], None

        # 2. Check known values
        if canonical in self.known_values:
            return self.known_values[canonical], None
        if param_name in self.known_values:
            return self.known_values[param_name], None

        # 3. Check computed cache
        if param_name in self.computed_cache:
            return self.computed_cache[param_name], None
        if canonical in self.computed_cache:
            return self.computed_cache[canonical], None

        # 4. Check default value
        if param and param.default_value is not None:
            return param.default_value, None

        # 5. Missing - build requirement for prompting
        if param:
            req = ParameterRequirement(
                name=param_name,
                description=param.description,
                units=param.units,
                symbol=param.symbol,
                default_value=param.default_value,
                physiological_range=param.physiological_range,
            )
        else:
            req = ParameterRequirement(
                name=param_name,
                description="Unknown parameter",
                units="unknown",
                symbol=param_name
            )
        return None, req

    def _validate_range(self, param_name: str, value: float,
                        param) -> Optional[str]:
        """Check if value is within physiological range.

        Returns warning string if out of range, None otherwise.
        Uses UnitValidator to suggest potential unit issues when values
        are outside range but would fit with common unit conversions.
        """
        if param and param.physiological_range:
            low, high = param.physiological_range
            if value < low or value > high:
                # Phase 1 (H4): Check if this might be a unit conversion issue
                unit_suggestion = UnitValidator.suggest_unit_issue(
                    param_name=param_name,
                    value=value,
                    expected_unit=param.units if hasattr(param, 'units') else "unknown",
                    physiological_range=param.physiological_range
                )
                if unit_suggestion:
                    return unit_suggestion
                return f"{param_name}={value} outside normal range [{low}, {high}]"
        return None

    def _cache_result(self, eq, value: float) -> None:
        """Cache a computed result so downstream consumers can resolve it.

        Stores the value under the equation id AND under the canonical parameter
        name the equation produces -- eq.produces if set, otherwise the id
        normalized through the global parameter-alias table. This is the fix for
        the chaining defect (H3): previously a dependency's value was cached only
        under its equation id (e.g. 'cardiac_output') while a consumer looked it
        up by parameter canonical (e.g. 'CO'), so the two namespaces never met.
        Many equation ids are already aliases of their output quantity
        (cardiac_output->CO, mean_arterial_pressure->MAP, ...), so those chain
        automatically; set `produces` on any equation whose id is not.
        """
        self.computed_cache[eq.id] = value
        output_name = getattr(eq, "produces", None) or eq.id
        canonical = normalize_param_name(output_name)  # global canonical, domain-independent
        if canonical != eq.id:
            self.computed_cache[canonical] = value

    def compute(self, eq_id: str, resolve_dependencies: bool = True,
                **overrides) -> ComputeResult:
        """Compute equation with automatic parameter resolution.

        Args:
            eq_id: Equation identifier
            resolve_dependencies: If True, automatically compute dependency equations
            **overrides: Parameter values to use (override known values for this call)

        Returns:
            ComputeResult with value or missing parameter requirements
        """
        # Get equation
        eq = self.index.get(eq_id)
        if eq is None:
            return ComputeResult(
                success=False,
                equation_id=eq_id,
                warnings=[f"Equation '{eq_id}' not found in index"]
            )

        # Phase 2 (H2): Extract domain for context-aware parameter resolution
        # This allows 'R' to resolve correctly in respiratory vs foundations context
        self._current_domain = get_domain_from_equation_id(eq_id)
        if self._current_domain is None and eq.category:
            self._current_domain = eq.category.value
        eq_domain = self._current_domain  # M6: dependency recursion below overwrites _current_domain

        # Cycle detection
        if eq_id in self._resolution_stack:
            return ComputeResult(
                success=False,
                equation_id=eq_id,
                equation_name=eq.name,
                warnings=[f"Circular dependency detected: {eq_id} already in resolution stack"]
            )

        # Normalize overrides (now domain-aware via _normalize())
        normalized_overrides = {
            self._normalize(k): v for k, v in overrides.items()
        }

        # Build parameter lookup
        eq_params = {p.name: p for p in eq.parameters}

        # Resolve dependencies first if requested
        computed_deps = {}
        if resolve_dependencies and eq.depends_on:
            self._resolution_stack.add(eq_id)
            try:
                for dep_id in eq.depends_on:
                    if dep_id not in self.computed_cache:
                        dep_result = self.compute(dep_id, resolve_dependencies=True)
                        if dep_result.success:
                            computed_deps[dep_id] = dep_result.value
                        # If dependency fails, continue - might not be needed
            finally:
                self._resolution_stack.discard(eq_id)

        # M6: the dependency recursion above overwrote _current_domain with each
        # dependency's domain and never restored it, so the parent used to
        # normalize its own parameters under the LAST dependency's domain.
        # Restore this equation's domain before resolving its parameters.
        self._current_domain = eq_domain

        # Resolve all parameters
        used_params = {}
        missing_params = []
        warnings = []

        for param in eq.parameters:
            value, req = self._resolve_param(
                param.name, eq_params, normalized_overrides
            )

            if value is not None:
                used_params[param.name] = value
                # Validate range
                warning = self._validate_range(param.name, value, param)
                if warning:
                    warnings.append(warning)
            elif req is not None:
                req.source_equation = eq_id
                missing_params.append(req)

        # If missing parameters, return early with requirements
        if missing_params:
            return ComputeResult(
                success=False,
                equation_id=eq_id,
                equation_name=eq.name,
                missing_params=missing_params,
                used_params=used_params,
                computed_dependencies=computed_deps,
                warnings=warnings
            )

        # Compute
        try:
            if eq._compute_func is not None:
                value = eq._compute_func(**used_params)
            else:
                return ComputeResult(
                    success=False,
                    equation_id=eq_id,
                    equation_name=eq.name,
                    used_params=used_params,
                    warnings=["No compute function defined for this equation"]
                )

            # Validate result
            if value is None or (isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
                warnings.append(f"Computation returned invalid value: {value}")
                return ComputeResult(
                    success=False,
                    equation_id=eq_id,
                    equation_name=eq.name,
                    value=value,
                    used_params=used_params,
                    computed_dependencies=computed_deps,
                    warnings=warnings
                )

            # Cache result (under id + canonical output name for chaining)
            self._cache_result(eq, value)

            return ComputeResult(
                success=True,
                value=value,
                equation_id=eq_id,
                equation_name=eq.name,
                used_params=used_params,
                computed_dependencies=computed_deps,
                warnings=warnings
            )

        except Exception as e:
            return ComputeResult(
                success=False,
                equation_id=eq_id,
                equation_name=eq.name,
                used_params=used_params,
                computed_dependencies=computed_deps,
                warnings=[f"Computation error: {type(e).__name__}: {str(e)}"]
            )

    def explain(self, eq_id: str, show_aliases: bool = True) -> str:
        """Return human-readable parameter requirements and dependency graph.

        Args:
            eq_id: Equation identifier
            show_aliases: Include known aliases for each parameter

        Returns:
            Formatted string with equation info, parameters, and dependencies
        """
        eq = self.index.get(eq_id)
        if eq is None:
            return f"Equation '{eq_id}' not found in index"

        lines = [
            f"**{eq.name}**",
            f"ID: `{eq_id}`",
            "",
            f"Formula: {eq.simplified}",
            f"LaTeX: `{eq.latex}`",
            "",
            f"Description: {eq.description}",
            "",
            "## Parameters"
        ]

        for param in eq.parameters:
            canonical = self._normalize(param.name)
            status = ""
            if canonical in self.known_values:
                status = f" ✓ = {self.known_values[canonical]}"
            elif param.name in self.computed_cache:
                status = f" ✓ (cached) = {self.computed_cache[param.name]}"
            elif param.default_value is not None:
                status = f" (default: {param.default_value})"
            else:
                status = " ⚠ REQUIRED"

            lines.append(f"- **{param.name}**: {param.description}{status}")
            lines.append(f"  - Symbol: `{param.symbol}`")
            lines.append(f"  - Units: {param.units}")
            if param.physiological_range:
                lines.append(f"  - Normal range: {param.physiological_range[0]} - {param.physiological_range[1]}")

            if show_aliases:
                aliases = get_aliases(canonical)
                if len(aliases) > 1:
                    alias_str = ", ".join(sorted(aliases - {canonical}))
                    lines.append(f"  - Aliases: {alias_str}")

        if eq.depends_on:
            lines.append("")
            lines.append("## Dependencies")
            for dep in eq.depends_on:
                dep_eq = self.index.get(dep)
                if dep_eq:
                    cached = " ✓ (cached)" if dep in self.computed_cache else ""
                    lines.append(f"- `{dep}`: {dep_eq.name}{cached}")
                else:
                    lines.append(f"- `{dep}`: (not found)")

        if eq.used_by:
            lines.append("")
            lines.append("## Used By")
            for user in eq.used_by[:5]:  # Limit to first 5
                user_eq = self.index.get(user)
                if user_eq:
                    lines.append(f"- `{user}`: {user_eq.name}")
                else:
                    lines.append(f"- `{user}`")
            if len(eq.used_by) > 5:
                lines.append(f"- ... and {len(eq.used_by) - 5} more")

        return "\n".join(lines)

    def batch_compute(self, eq_ids: List[str], **overrides) -> Dict[str, ComputeResult]:
        """Compute multiple equations, resolving shared dependencies once.

        Args:
            eq_ids: List of equation identifiers
            **overrides: Parameter values for all computations

        Returns:
            Dict mapping eq_id → ComputeResult
        """
        results = {}
        for eq_id in eq_ids:
            results[eq_id] = self.compute(eq_id, **overrides)
        return results

    def available_equations(self, category: Optional[str] = None) -> List[str]:
        """List all available equation IDs, optionally filtered by category."""
        if category:
            from .base import EquationCategory
            try:
                cat_enum = EquationCategory(category.lower())
                return [eq.id for eq in self.index.by_category(cat_enum)]
            except ValueError:
                return []
        return list(self.index._by_id.keys())

    def search_equations(self, query: str) -> List[str]:
        """Search equations by name or description (case-insensitive)."""
        query_lower = query.lower()
        matches = []
        for eq_id, eq in self.index._by_id.items():
            if query_lower in eq_id.lower() or \
               query_lower in eq.name.lower() or \
               query_lower in eq.description.lower():
                matches.append(eq_id)
        return matches


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def quick_compute(eq_id: str, **params) -> ComputeResult:
    """One-shot computation without persistent context.

    Args:
        eq_id: Equation identifier
        **params: Parameter values

    Returns:
        ComputeResult
    """
    ctx = ComputeContext()
    ctx.set(**params)
    return ctx.compute(eq_id)


def explain_equation(eq_id: str) -> str:
    """Get human-readable explanation of an equation."""
    ctx = ComputeContext()
    return ctx.explain(eq_id)


def list_equations(category: Optional[str] = None) -> List[str]:
    """List available equation IDs."""
    ctx = ComputeContext()
    return ctx.available_equations(category)

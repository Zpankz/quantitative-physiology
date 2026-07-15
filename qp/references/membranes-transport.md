---
name: membranes-transport
description: Membrane structure, passive and active transport, osmosis, cell signaling, and cellular metabolism including glycolysis and oxidative phosphorylation
parent: quantitative-physiology
unit: 2
---

# Membranes, Transport, and Metabolism

## Overview

This sub-skill covers the quantitative aspects of biological membranes, transport mechanisms, and cellular energy metabolism. These concepts bridge the physical foundations (Unit 1) with the electrical properties of excitable cells (Unit 3).

## Core Concepts

### 1. Biological Membrane Structure

#### Lipid Bilayer Properties

**Membrane composition**:
- Phospholipids: ~50% of membrane mass
- Cholesterol: Modulates fluidity
- Proteins: Transport, signaling, structural
- Glycocalyx: Cell surface recognition

**Membrane thickness**: δ ≈ 4-5 nm (hydrophobic core)

**Membrane capacitance**:
Formula → qp:`membrane_capacitance`

Where:
- ε_m ≈ 2-3 (membrane dielectric constant)
- ε_0 = 8.85×10⁻¹² F/m
- δ = membrane thickness

#### Permeability Coefficient

**Definition**: Rate of passive diffusion across membrane
Formula → qp:`permeability_coefficient`

Where:
- D = diffusion coefficient in membrane
- K = partition coefficient (membrane/water)
- δ = membrane thickness

**Typical values**:
| Molecule | P (cm/s) |
|----------|----------|
| H₂O | 10⁻² |
| Urea | 10⁻⁶ |
| Glucose | 10⁻⁷ |
| Na⁺ | 10⁻¹² |
| Cl⁻ | 10⁻¹¹ |

### 2. Passive Transport

#### Simple Diffusion Through Membranes

**Fick's Law for membrane flux**:
Formula → qp:`ficks_membrane_flux`

**For charged species** (considering electrical gradient):
Formula → qp:`goldman_flux`
This is the **Goldman flux equation**.

#### Facilitated Diffusion

**Carrier-mediated transport** follows saturation kinetics:
Formula → qp:`carrier_transport`

**Characteristics**:
- Saturable (J_max limit)
- Specific (substrate selectivity)
- Competitive inhibition possible
- Temperature dependent (Q₁₀ > 1)

#### Channel-Mediated Diffusion

**Single channel conductance**:
Formula → qp:`single_channel_conductance`

Where:
- i = single channel current (pA)
- V_m = membrane potential
- E_ion = reversal potential

**Typical values**: 1-300 pS depending on channel type

**Whole-cell conductance**:
Formula → qp:`whole_cell_conductance`

Where:
- N = number of channels
- P_open = open probability

### 3. Active Transport

#### Primary Active Transport

**ATP-driven pumps** couple ATP hydrolysis to ion movement:

**Na⁺/K⁺-ATPase** (sodium-potassium pump):
```
3 Na⁺_in + 2 K⁺_out + ATP → 3 Na⁺_out + 2 K⁺_in + ADP + Pᵢ
```

**Stoichiometry**: 3 Na⁺ out : 2 K⁺ in per ATP
**Electrogenic**: Net outward current (hyperpolarizing)

**Pump rate**:
Formula → qp:`nak_pump_rate`

Typical: 100-300 cycles/second

**Ca²⁺-ATPase** (SERCA, PMCA):
```
Ca²⁺_cytoplasm + ATP → Ca²⁺_ER/extracellular + ADP + Pᵢ
```

#### Secondary Active Transport

**Symport** (co-transport): Na⁺-glucose, Na⁺-amino acid
```
ΔG_glucose = ΔG°_glucose + RT ln([Glc]_in/[Glc]_out)
ΔG_coupled = ΔG_glucose + ΔG_Na = ΔG_glucose + RT ln([Na⁺]_in/[Na⁺]_out) + F(V_m)
```

**Antiport** (counter-transport): Na⁺/Ca²⁺ exchanger, Na⁺/H⁺ exchanger

**Na⁺/Ca²⁺ exchanger** (NCX):
```
3 Na⁺_out + Ca²⁺_in ⇌ 3 Na⁺_in + Ca²⁺_out
```
Reversal potential:
Formula → qp:`ncx_reversal`

### 4. Osmosis and Water Balance

#### Osmotic Pressure

**Van't Hoff equation**:
Formula → qp:`osmotic_pressure`

Where:
- π = osmotic pressure
- σ = reflection coefficient (0-1)
- C = solute concentration
- R = gas constant
- T = temperature

**For ideal semipermeable membrane**: σ = 1

#### Osmolarity and Tonicity

**Osmolarity**: Total solute concentration (mOsm/L)
- Plasma: ~290 mOsm/L
- Intracellular: ~290 mOsm/L

**Tonicity**: Effective osmolarity (only membrane-impermeable solutes)

**Hypotonic**: Cell swells
**Hypertonic**: Cell shrinks
**Isotonic**: No net water movement

#### Water Flux

**Osmotic water flow**:
Formula → qp:`water_flux`

Where:
- L_p = hydraulic conductivity (cm/(s·mmHg))
- ΔP = hydrostatic pressure difference
- Δπ = osmotic pressure difference
- σ = reflection coefficient

### 5. Gibbs-Donnan Equilibrium

**For impermeant charged species** (proteins):

At equilibrium:
```
[K⁺]_1 × [Cl⁻]_1 = [K⁺]_2 × [Cl⁻]_2
```

**Donnan ratio** (r):
Formula → qp:`donnan_ratio`

**Donnan potential**:
Formula → qp:`donnan_potential`

**Consequences**:
- Unequal ion distributions
- Osmotic imbalance (requires active transport compensation)
- Contributes to resting membrane potential

### 6. Cell Signaling

#### Receptor Kinetics

**Ligand-receptor binding**:
```
R + L ⇌ RL
K_d = [R][L]/[RL]
```

**Fractional occupancy**:
Formula → qp:`receptor_occupancy`

**Scatchard analysis**:
Formula → qp:`scatchard_analysis`
Where B = bound, F = free ligand

#### Second Messenger Systems

**cAMP cascade**:
```
Receptor → G_s → Adenylyl cyclase → cAMP → PKA → Cellular response
```

**Amplification**: Each step amplifies signal 10-1000×

**Signal termination**:
- Phosphodiesterase: cAMP → AMP
- Phosphatases: Dephosphorylation
- GTPase: G-protein inactivation

### 7. Cellular Metabolism

#### Glycolysis

**Net reaction**:
```
Glucose + 2 NAD⁺ + 2 ADP + 2 Pᵢ → 2 Pyruvate + 2 NADH + 2 ATP + 2 H₂O
```

**ATP yield**: 2 ATP per glucose (net)
**Key regulatory enzymes**: Hexokinase, PFK-1, Pyruvate kinase

**Lactate production** (anaerobic):
```
Pyruvate + NADH + H⁺ → Lactate + NAD⁺
```

#### Citric Acid Cycle (TCA/Krebs)

**Per acetyl-CoA**:
```
Acetyl-CoA + 3 NAD⁺ + FAD + GDP + Pᵢ + 2 H₂O →
2 CO₂ + 3 NADH + FADH₂ + GTP + CoA-SH
```

**Yield per glucose**: 2 × (3 NADH + 1 FADH₂ + 1 GTP)

#### Oxidative Phosphorylation

**Electron transport chain**:
```
NADH → Complex I → Q → Complex III → Cyt c → Complex IV → O₂
FADH₂ → Complex II → Q → ...
```

**Chemiosmotic coupling** (Mitchell hypothesis):
Formula → qp:`chemiosmotic_coupling`

**P/O ratios**:
- NADH: ~2.5 ATP/O
- FADH₂: ~1.5 ATP/O

**Total ATP yield per glucose** (aerobic):
```
Glycolysis:           2 ATP
Pyruvate oxidation:   2 NADH → 5 ATP
TCA cycle:            6 NADH → 15 ATP, 2 FADH₂ → 3 ATP, 2 GTP → 2 ATP
─────────────────────────────────────────────────────────────────────
Total:                ~30-32 ATP
```

#### Metabolic Rate

**Basal metabolic rate** (BMR):
Formula → qp:`basal_metabolic_rate`
Where M = body mass (kg)

**Respiratory quotient** (RQ):
Formula → qp:`respiratory_quotient`
- Carbohydrates: RQ = 1.0
- Fats: RQ ≈ 0.7
- Proteins: RQ ≈ 0.8

## Computational Models

### Python Implementation

```python
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve

# Physical constants
R = 8.314       # J/(mol·K)
F = 96485       # C/mol
k_B = 1.38e-23  # J/K

class MembranesTransport:
    """Quantitative models for membrane transport and metabolism"""

    @staticmethod
    def membrane_capacitance(epsilon_m=2.5, thickness=4e-9):
        """
        Calculate membrane capacitance

        Parameters:
        -----------
        epsilon_m : float - Membrane dielectric constant
        thickness : float - Membrane thickness (m)

        Returns:
        --------
        C_m : float - Capacitance (F/m²)
        """
        epsilon_0 = 8.85e-12  # F/m
        return epsilon_m * epsilon_0 / thickness

    @staticmethod
    def permeability_coefficient(D, K, delta):
        """
        Calculate membrane permeability coefficient

        Parameters:
        -----------
        D : float - Diffusion coefficient in membrane (m²/s)
        K : float - Partition coefficient
        delta : float - Membrane thickness (m)

        Returns:
        --------
        P : float - Permeability coefficient (m/s)
        """
        return D * K / delta

    @staticmethod
    def goldman_flux(P, z, V_m, C_in, C_out, T=310):
        """
        Goldman flux equation for charged species

        Parameters:
        -----------
        P : float - Permeability coefficient (m/s)
        z : int - Ion valence
        V_m : float - Membrane potential (V)
        C_in, C_out : float - Concentrations (mol/m³)
        T : float - Temperature (K)

        Returns:
        --------
        J : float - Flux (mol/(m²·s))
        """
        u = z * F * V_m / (R * T)
        if abs(u) < 1e-6:  # Near zero potential
            return P * (C_in - C_out)
        return P * u * (C_in - C_out * np.exp(u)) / (1 - np.exp(u))

    @staticmethod
    def carrier_transport(S, J_max, K_m):
        """
        Carrier-mediated transport (Michaelis-Menten)

        Parameters:
        -----------
        S : float or array - Substrate concentration
        J_max : float - Maximum flux
        K_m : float - Half-saturation constant

        Returns:
        --------
        J : float or array - Transport rate
        """
        return J_max * S / (K_m + S)

    @staticmethod
    def osmotic_pressure(C, sigma=1.0, T=310):
        """
        Van't Hoff osmotic pressure

        Parameters:
        -----------
        C : float - Solute concentration (mol/m³)
        sigma : float - Reflection coefficient
        T : float - Temperature (K)

        Returns:
        --------
        pi : float - Osmotic pressure (Pa)
        """
        return sigma * C * R * T

    @staticmethod
    def water_flux(L_p, delta_P, delta_pi, sigma=1.0):
        """
        Osmotic water flow

        Parameters:
        -----------
        L_p : float - Hydraulic conductivity (m/(s·Pa))
        delta_P : float - Hydrostatic pressure difference (Pa)
        delta_pi : float - Osmotic pressure difference (Pa)
        sigma : float - Reflection coefficient

        Returns:
        --------
        J_v : float - Volume flux (m/s)
        """
        return L_p * (delta_P - sigma * delta_pi)

    @staticmethod
    def donnan_ratio(C_protein, z_protein, C_salt):
        """
        Calculate Gibbs-Donnan ratio

        Parameters:
        -----------
        C_protein : float - Protein concentration (mol/m³)
        z_protein : int - Protein charge (negative)
        C_salt : float - Salt concentration in compartment 2 (mol/m³)

        Returns:
        --------
        r : float - Donnan ratio
        """
        # Solve quadratic equation for electroneutrality
        # [K+]_1 - [Cl-]_1 = |z|*C_protein
        # [K+]_1 * [Cl-]_1 = [K+]_2 * [Cl-]_2 = C_salt²

        z = abs(z_protein)

        # [K+]_1 = (z*C_p + sqrt((z*C_p)² + 4*C_salt²)) / 2
        K1 = (z * C_protein + np.sqrt((z * C_protein)**2 + 4 * C_salt**2)) / 2
        return K1 / C_salt

    @staticmethod
    def receptor_occupancy(L, K_d):
        """
        Ligand-receptor binding (fractional occupancy)

        Parameters:
        -----------
        L : float or array - Ligand concentration
        K_d : float - Dissociation constant

        Returns:
        --------
        f : float or array - Fractional occupancy (0-1)
        """
        return L / (K_d + L)

    @staticmethod
    def glycolysis_atp(glucose_moles):
        """
        ATP yield from glycolysis

        Parameters:
        -----------
        glucose_moles : float - Moles of glucose

        Returns:
        --------
        dict : ATP and metabolite yields
        """
        return {
            'ATP': 2 * glucose_moles,
            'NADH': 2 * glucose_moles,
            'pyruvate': 2 * glucose_moles
        }

    @staticmethod
    def aerobic_atp_yield(glucose_moles, po_ratio_nadh=2.5, po_ratio_fadh2=1.5):
        """
        Total ATP yield from aerobic oxidation of glucose

        Parameters:
        -----------
        glucose_moles : float - Moles of glucose
        po_ratio_nadh : float - P/O ratio for NADH
        po_ratio_fadh2 : float - P/O ratio for FADH₂

        Returns:
        --------
        dict : ATP yields from each pathway
        """
        # Glycolysis
        glyco_atp = 2 * glucose_moles
        glyco_nadh = 2 * glucose_moles

        # Pyruvate dehydrogenase (2 per glucose)
        pdh_nadh = 2 * glucose_moles

        # TCA cycle (2 per glucose)
        tca_nadh = 6 * glucose_moles
        tca_fadh2 = 2 * glucose_moles
        tca_gtp = 2 * glucose_moles

        # Oxidative phosphorylation
        total_nadh = glyco_nadh + pdh_nadh + tca_nadh  # 10 NADH
        total_fadh2 = tca_fadh2  # 2 FADH₂

        oxphos_atp = total_nadh * po_ratio_nadh + total_fadh2 * po_ratio_fadh2

        return {
            'glycolysis_ATP': glyco_atp,
            'TCA_GTP': tca_gtp,
            'oxphos_ATP': oxphos_atp,
            'total_ATP': glyco_atp + tca_gtp + oxphos_atp,
            'total_NADH': total_nadh,
            'total_FADH2': total_fadh2
        }

    @staticmethod
    def basal_metabolic_rate(body_mass):
        """
        Kleiber's law for basal metabolic rate

        Parameters:
        -----------
        body_mass : float - Body mass (kg)

        Returns:
        --------
        BMR : float - Basal metabolic rate (kcal/day)
        """
        return 70 * body_mass**0.75


class NaKATPase:
    """Model of Na+/K+-ATPase pump"""

    def __init__(self, J_max=200, K_Na=10, K_K=2, K_ATP=0.5):
        """
        Parameters:
        -----------
        J_max : float - Maximum pump rate (cycles/s)
        K_Na : float - Half-saturation for intracellular Na+ (mM)
        K_K : float - Half-saturation for extracellular K+ (mM)
        K_ATP : float - Half-saturation for ATP (mM)
        """
        self.J_max = J_max
        self.K_Na = K_Na
        self.K_K = K_K
        self.K_ATP = K_ATP

    def pump_rate(self, Na_in, K_out, ATP):
        """
        Calculate pump rate based on substrate concentrations

        Returns:
        --------
        J : float - Pump rate (cycles/s)
        """
        f_Na = (Na_in / self.K_Na)**3 / (1 + (Na_in / self.K_Na)**3)
        f_K = (K_out / self.K_K)**2 / (1 + (K_out / self.K_K)**2)
        f_ATP = ATP / (self.K_ATP + ATP)

        return self.J_max * f_Na * f_K * f_ATP

    def current(self, Na_in, K_out, ATP, pump_density=1000):
        """
        Calculate pump current (electrogenic: 3 Na+ out, 2 K+ in)

        Parameters:
        -----------
        pump_density : float - Pumps per μm²

        Returns:
        --------
        I_pump : float - Pump current (pA/μm²)
        """
        e = 1.6e-19  # Elementary charge (C)
        J = self.pump_rate(Na_in, K_out, ATP)
        # Net outward current of 1 charge per cycle
        return pump_density * J * e * 1e12  # Convert to pA


# Example: Simulate cell volume regulation
def cell_volume_dynamics(y, t, params):
    """
    ODE for cell volume changes due to osmotic imbalance

    y = [V, n_Na, n_K]  (volume and ion amounts)
    """
    V, n_Na, n_K = y
    L_p, sigma, C_imp, pump_rate, P_Na, P_K = params

    # Intracellular concentrations
    C_Na_in = n_Na / V
    C_K_in = n_K / V

    # External concentrations (constant)
    C_Na_out = 145  # mM
    C_K_out = 5     # mM

    # Osmotic pressure difference
    C_in_total = C_Na_in + C_K_in + C_imp
    C_out_total = C_Na_out + C_K_out
    delta_pi = R * 310 * (C_in_total - C_out_total) * 1000  # Convert mM to mol/m³

    # Volume change
    dV_dt = L_p * (-sigma * delta_pi)  # Assuming ΔP = 0

    # Ion fluxes (simplified - passive leak + pump)
    J_Na = P_Na * (C_Na_out - C_Na_in) - 3 * pump_rate
    J_K = P_K * (C_K_out - C_K_in) + 2 * pump_rate

    dn_Na_dt = J_Na * V
    dn_K_dt = J_K * V

    return [dV_dt, dn_Na_dt, dn_K_dt]


# Example usage
if __name__ == "__main__":
    mt = MembranesTransport()

    # Calculate membrane capacitance
    C_m = mt.membrane_capacitance()
    print(f"Membrane capacitance: {C_m*1e4:.2f} μF/cm²")

    # Donnan ratio for typical cell
    r = mt.donnan_ratio(C_protein=1.0, z_protein=-20, C_salt=150)
    print(f"Donnan ratio: {r:.3f}")

    # ATP yield from glucose
    atp = mt.aerobic_atp_yield(1.0)
    print(f"Total ATP per glucose: {atp['total_ATP']:.1f}")

    # BMR for 70 kg person
    bmr = mt.basal_metabolic_rate(70)
    print(f"BMR for 70 kg: {bmr:.0f} kcal/day")
```

### Julia Implementation

```julia
using DifferentialEquations
using Plots

# Physical constants
const R = 8.314       # J/(mol·K)
const F = 96485       # C/mol

"""
    goldman_flux(P, z, V_m, C_in, C_out; T=310)

Calculate ion flux using Goldman flux equation.
"""
function goldman_flux(P, z, V_m, C_in, C_out; T=310)
    u = z * F * V_m / (R * T)
    if abs(u) < 1e-6
        return P * (C_in - C_out)
    end
    return P * u * (C_in - C_out * exp(u)) / (1 - exp(u))
end

"""
    osmotic_pressure(C; σ=1.0, T=310)

Van't Hoff osmotic pressure (Pa).
"""
osmotic_pressure(C; σ=1.0, T=310) = σ * C * R * T

"""
    donnan_equilibrium(C_protein, z_protein, C_salt)

Calculate Gibbs-Donnan equilibrium ion distributions.
Returns (K⁺_in, Cl⁻_in, donnan_ratio, donnan_potential)
"""
function donnan_equilibrium(C_protein, z_protein, C_salt; T=310)
    z = abs(z_protein)

    # Solve for cation concentration inside
    K_in = (z * C_protein + sqrt((z * C_protein)^2 + 4 * C_salt^2)) / 2
    Cl_in = C_salt^2 / K_in

    r = K_in / C_salt
    E_donnan = (R * T / F) * log(r)

    return (K_in=K_in, Cl_in=Cl_in, ratio=r, potential=E_donnan)
end

"""
    carrier_kinetics(S, J_max, K_m)

Michaelis-Menten carrier kinetics.
"""
carrier_kinetics(S, J_max, K_m) = J_max * S / (K_m + S)

"""
    nak_pump_rate(Na_in, K_out, ATP; J_max=200, K_Na=10, K_K=2, K_ATP=0.5)

Na⁺/K⁺-ATPase pump rate (cycles/s).
"""
function nak_pump_rate(Na_in, K_out, ATP; J_max=200, K_Na=10, K_K=2, K_ATP=0.5)
    f_Na = (Na_in / K_Na)^3 / (1 + (Na_in / K_Na)^3)
    f_K = (K_out / K_K)^2 / (1 + (K_out / K_K)^2)
    f_ATP = ATP / (K_ATP + ATP)

    return J_max * f_Na * f_K * f_ATP
end

"""
    atp_yield(glucose_moles; po_nadh=2.5, po_fadh2=1.5)

Calculate total ATP yield from aerobic glucose oxidation.
"""
function atp_yield(glucose_moles; po_nadh=2.5, po_fadh2=1.5)
    # Glycolysis: 2 ATP, 2 NADH
    # PDH: 2 NADH
    # TCA: 6 NADH, 2 FADH₂, 2 GTP

    total_nadh = 10 * glucose_moles
    total_fadh2 = 2 * glucose_moles

    glyco_atp = 2 * glucose_moles
    tca_gtp = 2 * glucose_moles
    oxphos_atp = total_nadh * po_nadh + total_fadh2 * po_fadh2

    return glyco_atp + tca_gtp + oxphos_atp
end

"""
Cell volume regulation ODE system.
"""
function cell_volume!(du, u, p, t)
    V, n_Na, n_K = u
    L_p, σ, C_imp, pump_rate_const, P_Na, P_K = p

    # Concentrations (mM)
    C_Na_in = n_Na / V
    C_K_in = n_K / V
    C_Na_out = 145.0
    C_K_out = 5.0

    # Total osmolarity
    C_in = C_Na_in + C_K_in + C_imp
    C_out = C_Na_out + C_K_out

    # Volume change (osmotic)
    Δπ = R * 310 * (C_in - C_out) * 1000  # Pa
    dV = L_p * (-σ * Δπ)

    # Ion fluxes
    pump = pump_rate_const * V
    J_Na = P_Na * (C_Na_out - C_Na_in) - 3 * pump
    J_K = P_K * (C_K_out - C_K_in) + 2 * pump

    du[1] = dV
    du[2] = J_Na * V
    du[3] = J_K * V
end

# Example: Plot carrier kinetics
function plot_carrier_kinetics()
    S = range(0, 10, length=100)
    J_max = 100
    K_m = 2

    J = carrier_kinetics.(S, J_max, K_m)

    plot(S, J,
         xlabel="Substrate concentration",
         ylabel="Transport rate",
         label="J_max=$J_max, K_m=$K_m",
         title="Carrier-Mediated Transport")
end
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify transport type**: Passive diffusion, facilitated, or active?
2. **Determine driving forces**: Concentration gradient, electrical gradient, or both?
3. **Select appropriate equation**: Fick's, Goldman, Michaelis-Menten?
4. **Consider coupling**: Is transport coupled to other processes?
5. **Calculate flux or rate**
6. **Check physiological reasonableness**

### Typical Problems

**Type 1: Membrane permeability**
- Given: Concentrations, flux
- Find: Permeability coefficient

**Type 2: Osmotic problems**
- Given: Concentrations, membrane properties
- Find: Water flux, cell volume change

**Type 3: Pump energetics**
- Given: Ion gradients, ATP availability
- Find: Required pump rate, energy cost

**Type 4: Metabolic yield**
- Given: Substrate amounts
- Find: ATP yield, oxygen consumption

## Key Relationships Summary

| Process | Driving Force | Equation |
|---------|---------------|----------|
| Simple diffusion | ΔC | J = P × ΔC |
| Electrodiffusion | ΔC + Δψ | Goldman equation |
| Facilitated | ΔC | J = J_max × S/(K_m + S) |
| Primary active | ATP | J = f([substrates], [ATP]) |
| Osmotic flow | Δπ | J_V = L_p × (ΔP - σΔπ) |


## Coverage-pass additions (Feher extraction)

11 equation(s) added to this domain, each verified against Feher and a worked example.

### Young's Modulus (Hooke's Law) (`youngs_modulus`)
- **Formula:** `sigma = E * epsilon`
- **LaTeX:** `\sigma = E \varepsilon`
- **Import:** `from scripts.membrane.mechanics import youngs_modulus` — or `from scripts.canonical_ids import load; load('youngs_modulus')`
- **Feher:** §2.1 — Appendix 2.1.A2 Mechanical Properties of Cytoskeletal Elements - Most cells appear to be viscoelastic
- Linear-elastic (Hookean) constitutive law defining Young's modulus (the coefficient of elasticity): the mechanical stress sigma = F/A developed in a material is proportional to its strain epsilon = dl/l0, with proportionality constant E.

### Kelvin-Voigt Viscoelastic Model (`kelvin_voigt_model`)
- **Formula:** `sigma = E*epsilon + eta*(depsilon/dt)`
- **LaTeX:** `\sigma = E \varepsilon + \eta \frac{d\varepsilon}{dt}`
- **Import:** `from scripts.membrane.mechanics import kelvin_voigt_model` — or `from scripts.canonical_ids import load; load('kelvin_voigt_model')`
- **Feher:** §2.1 — Appendix 2.1.A2 Mechanical Properties of Cytoskeletal Elements - Most cells appear to be viscoelastic
- Kelvin-Voigt viscoelastic constitutive law: a spring (elastic modulus E) and a dashpot (viscosity eta) connected in parallel share the same strain, so the total stress is the sum of the elastic stress (E*epsilon) and the viscous stress (eta * strain-rate).

### Maxwell Viscoelastic Model (`maxwell_model`)
- **Formula:** `depsilon_dt = dsigma_dt / E + sigma / eta`
- **LaTeX:** `\frac{d\varepsilon}{dt} = \frac{1}{E}\frac{d\sigma}{dt} + \frac{\sigma}{\eta}`
- **Import:** `from scripts.membrane.mechanics import maxwell_model` — or `from scripts.canonical_ids import load; load('maxwell_model')`
- **Feher:** §2.1 — Appendix 2.1.A2 Mechanical Properties of Cytoskeletal Elements - The Maxwell model arranges elastic and viscous elements in series
- Constitutive (governing) equation of the Maxwell viscoelastic model, in which an elastic spring (modulus E) and a viscous dashpot (viscosity eta) are arranged in series.

### Persistence Length (Tangent Correlation) (`persistence_length`)
- **Formula:** `<cos(Theta)> = exp(-L / l_p)`
- **LaTeX:** `\langle \cos\Theta \rangle = e^{-L/l_{p}}`
- **Import:** `from scripts.membrane.mechanics import persistence_length` — or `from scripts.canonical_ids import load; load('persistence_length')`
- **Feher:** §2.1 — Appendix 2.1.A2 - The persistence length describes the thermal stiffness of a polymer
- Worm-like-chain tangent-tangent correlation of a semiflexible polymer (microtubule, actin filament, intermediate filament, DNA).

### Poisson Ratio (`poisson_ratio`)
- **Formula:** `nu = -depsilon_trans / depsilon_axial`
- **LaTeX:** `\nu = -\frac{d\varepsilon_{trans}}{d\varepsilon_{axial}}`
- **Import:** `from scripts.membrane.mechanics import poisson_ratio` — or `from scripts.canonical_ids import load; load('poisson_ratio')`
- **Feher:** §2.1 — Appendix 2.1.A2 Mechanical Properties of Cytoskeletal Elements - The Poisson ratio describes how much a material thins when it is stretched
- The Poisson ratio, a dimensionless material property giving the fraction of transverse thinning per unit of axial stretch.

### Standard Linear Solid (Zener) Model (`standard_linear_solid`)
- **Formula:** `dsigma/dt = (E1 + E2)*(depsilon/dt) + (E1*E2/eta)*epsilon - (E2/eta)*sigma`
- **LaTeX:** `\frac{\eta}{E_2}\frac{d\sigma}{dt} + \sigma = \frac{\eta(E_1+E_2)}{E_2}\frac{d\varepsilon}{dt} + E_1 \varepsilon`
- **Import:** `from scripts.membrane.mechanics import standard_linear_solid` — or `from scripts.canonical_ids import load; load('standard_linear_solid')`
- **Feher:** §2.1 — THE STANDARD LINEAR SOLID MODEL COMBINES BOTH SERIES AND PARALLEL ELEMENTS
- Constitutive stress-strain relation of the standard linear solid (Zener) viscoelastic model, a parallel combination of a free elastic element (E1) and a Maxwell element (elastic E2 in series with a dashpot eta).

### Surface Pressure (`surface_pressure`)
- **Formula:** `pi = gamma_0 - gamma`
- **LaTeX:** `\pi = \gamma_0 - \gamma`
- **Import:** `from scripts.membrane.structure import surface_pressure` — or `from scripts.canonical_ids import load; load('surface_pressure')`
- **Feher:** §2.5 — AMPHIPATHIC MOLECULES SPREAD OVER A WATER SURFACE, REDUCE SURFACE TENSION, AND PRODUCE AN APPARENT SURFACE PRESSURE
- Apparent surface pressure exerted by an amphipathic (lipid) monolayer spread on an air-water interface, defined as the reduction in surface tension relative to the clean surface.

### Surface Free Energy (`surface_free_energy`)
- **Formula:** `dG = gamma * dA`
- **LaTeX:** `\mathrm{d}G = \gamma\,\mathrm{d}A`
- **Import:** `from scripts.membrane.structure import surface_free_energy` — or `from scripts.canonical_ids import load; load('surface_free_energy')`
- **Feher:** §2.5 — SURFACE TENSION OF THE AIR–WATER INTERFACE RESULTS FROM ASYMMETRIC FORCES
- Change in surface (Gibbs) free energy when the area of an air-water interface changes.

### Partition Coefficient (`partition_coefficient`)
- **Formula:** `k_s = C_lipid / C_water`
- **LaTeX:** `k_{s} = \dfrac{C_{\mathrm{eq,\,lipid}}}{C_{\mathrm{eq,\,water}}}`
- **Import:** `from scripts.membrane.structure import partition_coefficient` — or `from scripts.canonical_ids import load; load('partition_coefficient')`
- **Feher:** §2.6 — DISSOLUTION-DIFFUSION IN THE LIPID BILAYER IS ANOTHER MODEL FOR PASSIVE TRANSPORT
- Partition (distribution) coefficient: the ratio of a solute's equilibrium concentration in the membrane lipid phase to its equilibrium concentration in the adjacent aqueous phase.

### Ussing Flux Ratio Equation (`ussing_flux_ratio`)
- **Formula:** `J_(i->o)/J_(o->i) = -(C_in/C_out) * exp(z*F*E_m/(R*T))`
- **LaTeX:** `\frac{J_{i \to o}}{J_{o \to i}} = -\frac{C_i}{C_o}\, e^{\frac{z F E_m}{RT}}`
- **Import:** `from scripts.membrane.transport import ussing_flux_ratio` — or `from scripts.canonical_ids import load; load('ussing_flux_ratio')`
- **Feher:** §2.7 — APPENDIX 2.7.A1 DERIVATION OF THE USSING FLUX RATIO EQUATION
- Ussing flux ratio equation (Feher Appendix 2.7.A1, Eqn 2.7.A1.16): the ratio of the two unidirectional passive fluxes of an ion across a membrane, predicted from the trans-membrane concentrations and the membrane potential.

### Boyle-van't Hoff Relation (`boyle_vant_hoff_relation`)
- **Formula:** `V_C/V_0 = (1 - V_b/V_0) * (pi_0/pi_C) + V_b/V_0`
- **LaTeX:** `\frac{V_C}{V_0} = \left(1 - \frac{V_b}{V_0}\right)\frac{\pi_0}{\pi_C} + \frac{V_b}{V_0}`
- **Import:** `from scripts.membrane.osmosis import boyle_vant_hoff_relation` — or `from scripts.canonical_ids import load; load('boyle_vant_hoff_relation')`
- **Feher:** §2.9 — WHAT STOPS OSMOTIC FLUID FLOW IN ANISOTONIC MEDIA?
- Boyle-van't Hoff relation for the osmometric behaviour of a cell: predicts the relative cell-content volume V_C/V_0 reached at osmotic equilibrium in an anisotonic medium, given the osmolarity (effective osmotic-pressure) ratio and the osmotically inactive volume fraction b = V_b/V_0.


### Coverage pass 2 (residual reconsideration)

**Newtonian Viscous Stress** (`newtonian_viscosity`): `sigma = eta * d(epsilon)/dt` — `from scripts.membrane.mechanics import newtonian_viscosity`. Feher §2.1 (Eqn 2.1.A2.2). Newtonian viscous constitutive relation: stress in a linear viscous (dashpot) element equals viscosity times strain rate.


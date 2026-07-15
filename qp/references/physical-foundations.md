---
name: physical-foundations
description: Physical and chemical foundations of physiology - pressure-driven flow, electrical forces, diffusion, chemical energy, and thermodynamics
parent: quantitative-physiology
unit: 1
---

# Physical and Chemical Foundations of Physiology

## Overview

This sub-skill covers the quantitative physical and chemical principles underlying all physiological processes. These foundations are essential for understanding transport, signaling, and energy transformations in biological systems.

## Core Concepts

### 1. Pressure-Driven Flow

#### Flow and Flux Definitions

**Volume Flux** (J_V): Volume flowing per unit area per unit time
Formula → qp:`volume_flux`

**Solute Flux** (J_S): Amount of solute per unit area per unit time
Formula → qp:`solute_flux`

#### Continuity Equation

The fundamental conservation law for transport:
```
∂C/∂t = -∂J/∂x
```

**Physical meaning**: If flux varies spatially (∂J/∂x ≠ 0), concentration must change temporally.

**Steady state** (∂C/∂t = 0) requires uniform flux → linear concentration gradient.

#### Hydrostatic Pressure

Pressure at depth h in fluid:
Formula → qp:`hydrostatic_pressure`
Where:
- ρ = fluid density (kg/m³)
- g = gravitational acceleration (9.8 m/s²)
- h = height of fluid column (m)

**Clinical relevance**: Blood pressure measurement, CSF dynamics, edema formation.

#### Poiseuille's Law

For laminar flow through a cylindrical tube:
Formula → qp:`poiseuille_flow`

**Key insights**:
- Flow ∝ r⁴ (doubling radius → 16× flow)
- Flow ∝ 1/η (viscosity impedes flow)
- Flow ∝ ΔP (pressure gradient drives flow)
- Flow ∝ 1/L (longer tubes = more resistance)

**Hydraulic resistance**: R = 8ηL/(πr⁴)
```
Q_V = ΔP/R    (analogous to Ohm's law: I = V/R)
```

#### Law of Laplace

Relates wall tension to transmural pressure:

**Cylinder** (blood vessels):
Formula → qp:`laplace_cylinder`

**Sphere** (alveoli, cells):
Formula → qp:`laplace_sphere`

**Clinical implications**:
- Aneurysms: Larger radius → more wall tension → risk of rupture
- Alveoli: Surfactant reduces surface tension, preventing collapse
- Heart: Dilated ventricle requires more wall tension for same pressure

### 2. Electrical Forces

#### Coulomb's Law

Electrostatic force between point charges:
Formula → qp:`coulomb_law`

Where:
- q₁, q₂ = charges (C)
- ε₀ = 8.85×10⁻¹² C²/(J·m) (permittivity of free space)
- r = separation distance (m)

In a medium with dielectric constant ε:
Formula → qp:`coulomb_law_medium`

#### Electric Potential

Work per unit charge to move from reference to point A:
```
U_A = -∫(F·ds)/q_test
```

Units: Volts (V) = Joules per Coulomb (J/C)

#### Electric Field

Force per unit charge:
Formula → qp:`electric_field`

The field points from high to low potential (downhill for positive charges).

#### Capacitance

Definition:
Formula → qp:`capacitance`

Parallel plate capacitor:
Formula → qp:`parallel_plate_capacitor`

**Membrane as capacitor**:
- Typical membrane capacitance: 1 μF/cm²
- Lipid bilayer thickness: ~4 nm
- Membrane acts as insulator between two conductors

### 3. Diffusion

#### Fick's First Law

Diffusive flux is proportional to concentration gradient:
Formula → qp:`fick_first_law`

Where D = diffusion coefficient (m²/s)

**Negative sign**: Flux goes from high to low concentration (down the gradient).

#### Fick's Second Law

Time evolution of concentration during diffusion:
```
∂C/∂t = D(∂²C/∂x²)
```

Derived from Fick's First Law + Continuity Equation.

#### Diffusion Coefficient

**Einstein relation**:
```
D = kT/ζ
```
Where ζ = frictional coefficient

**Stokes-Einstein equation** (spherical particle):
Formula → qp:`stokes_einstein`
Where:
- k = 1.38×10⁻²³ J/K (Boltzmann constant)
- T = temperature (K)
- η = viscosity (Pa·s)
- a = particle radius (m)

**Typical values**:
| Molecule | D in water (m²/s) |
|----------|-------------------|
| Na⁺ | 1.3×10⁻⁹ |
| K⁺ | 2.0×10⁻⁹ |
| Glucose | 6.7×10⁻¹⁰ |
| Albumin | 6×10⁻¹¹ |

#### Diffusion Time

Characteristic time for diffusion over distance x:
Formula → qp:`diffusion_time`

**Example**: For D = 10⁻⁹ m²/s
- 1 μm: t ≈ 0.5 ms
- 10 μm: t ≈ 50 ms
- 100 μm: t ≈ 5 s
- 1 mm: t ≈ 500 s ≈ 8 min
- 1 cm: t ≈ 50,000 s ≈ 14 hours

**Implications**: Diffusion works for cells, fails for whole organisms → need circulation.

### 4. Chemical Energy and Thermodynamics

#### Enthalpy

Heat content at constant pressure:
Formula → qp:`enthalpy`

#### Entropy

Measure of disorder/randomness:
```
ΔS = Q_rev/T
```

#### Gibbs Free Energy

Maximum useful work from a process:
Formula → qp:`gibbs_free_energy`

**Spontaneity**:
- ΔG < 0: Spontaneous (exergonic)
- ΔG > 0: Non-spontaneous (endergonic)
- ΔG = 0: Equilibrium

#### Standard Free Energy

At 1 M concentrations, 1 atm, 25°C:
Formula → qp:`standard_free_energy`

Actual free energy change:
Formula → qp:`actual_free_energy`
Where Q = reaction quotient (actual concentration ratio)

#### ATP Hydrolysis

```
ATP + H₂O → ADP + Pᵢ
```

**Standard**: ΔG° ≈ -30.5 kJ/mol
**Cellular conditions**: ΔG ≈ -54 kJ/mol

The higher magnitude in cells is due to:
- Low ADP concentration
- Low Pᵢ concentration
- High ATP concentration

### 5. Electrochemical Potential

Unifying electrical and chemical driving forces:
Formula → qp:`electrochemical_potential`

Where:
- μ° = standard chemical potential
- RT ln(C) = concentration term
- zFψ = electrical term (z = valence, F = Faraday, ψ = potential)

**Equilibrium condition**: Δμ̃ = 0

This leads to the **Nernst equation**:
Formula → qp:`nernst_equation`

At 37°C (310 K):
```
E = (26.7 mV/z) ln(C_out/C_in)
E ≈ (61.5 mV/z) log₁₀(C_out/C_in)
```

## Computational Models

### Python Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Physical constants
R = 8.314       # J/(mol·K)
F = 96485       # C/mol
k_B = 1.38e-23  # J/K
N_A = 6.02e23   # mol⁻¹

class PhysicalFoundations:
    """Quantitative models for physical foundations of physiology"""

    @staticmethod
    def poiseuille_flow(delta_P, r, L, eta):
        """
        Calculate flow through cylindrical tube (Poiseuille's Law)

        Parameters:
        -----------
        delta_P : float - Pressure difference (Pa)
        r : float - Tube radius (m)
        L : float - Tube length (m)
        eta : float - Viscosity (Pa·s)

        Returns:
        --------
        Q : float - Volume flow rate (m³/s)
        """
        return (np.pi * r**4 * delta_P) / (8 * eta * L)

    @staticmethod
    def laplace_cylinder(T, r):
        """Transmural pressure for cylinder (blood vessel)"""
        return T / r

    @staticmethod
    def laplace_sphere(T, r):
        """Transmural pressure for sphere (alveolus)"""
        return 2 * T / r

    @staticmethod
    def diffusion_coeff(T, eta, a):
        """
        Stokes-Einstein diffusion coefficient

        Parameters:
        -----------
        T : float - Temperature (K)
        eta : float - Viscosity (Pa·s)
        a : float - Particle radius (m)

        Returns:
        --------
        D : float - Diffusion coefficient (m²/s)
        """
        return (k_B * T) / (6 * np.pi * eta * a)

    @staticmethod
    def diffusion_time(x, D):
        """Characteristic time for diffusion over distance x"""
        return x**2 / (2 * D)

    @staticmethod
    def nernst_potential(z, C_out, C_in, T=310):
        """
        Nernst equilibrium potential

        Parameters:
        -----------
        z : int - Ion valence
        C_out : float - Extracellular concentration
        C_in : float - Intracellular concentration
        T : float - Temperature (K), default 37°C

        Returns:
        --------
        E : float - Equilibrium potential (V)
        """
        return (R * T) / (z * F) * np.log(C_out / C_in)

    @staticmethod
    def gibbs_free_energy(delta_G0, Q, T=310):
        """
        Actual Gibbs free energy change

        Parameters:
        -----------
        delta_G0 : float - Standard free energy change (J/mol)
        Q : float - Reaction quotient
        T : float - Temperature (K)

        Returns:
        --------
        delta_G : float - Free energy change (J/mol)
        """
        return delta_G0 + R * T * np.log(Q)

    @staticmethod
    def diffusion_1d(C0, x, t, D):
        """
        1D diffusion from point source (Gaussian spreading)

        Parameters:
        -----------
        C0 : float - Initial amount
        x : array - Position array (m)
        t : float - Time (s)
        D : float - Diffusion coefficient (m²/s)

        Returns:
        --------
        C : array - Concentration profile
        """
        return (C0 / np.sqrt(4 * np.pi * D * t)) * np.exp(-x**2 / (4 * D * t))


# Example usage and visualization
if __name__ == "__main__":
    pf = PhysicalFoundations()

    # Example: Diffusion time scaling
    distances = np.logspace(-6, -2, 100)  # 1 μm to 1 cm
    D = 1e-9  # m²/s (typical small molecule)
    times = pf.diffusion_time(distances, D)

    plt.figure(figsize=(10, 6))
    plt.loglog(distances * 1e6, times, 'b-', linewidth=2)
    plt.xlabel('Distance (μm)')
    plt.ylabel('Diffusion Time (s)')
    plt.title('Diffusion Time vs Distance')
    plt.grid(True)
    plt.axhline(1, color='r', linestyle='--', label='1 second')
    plt.axhline(60, color='g', linestyle='--', label='1 minute')
    plt.legend()
    plt.savefig('diffusion_scaling.png', dpi=150)
```

### Julia Implementation

```julia
using Plots
using DifferentialEquations

# Physical constants
const R = 8.314       # J/(mol·K)
const F = 96485       # C/mol
const k_B = 1.38e-23  # J/K
const N_A = 6.02e23   # mol⁻¹

"""
    poiseuille_flow(ΔP, r, L, η)

Calculate volume flow through cylindrical tube.

# Arguments
- `ΔP`: Pressure difference (Pa)
- `r`: Tube radius (m)
- `L`: Tube length (m)
- `η`: Viscosity (Pa·s)

# Returns
- Volume flow rate (m³/s)
"""
function poiseuille_flow(ΔP, r, L, η)
    return (π * r^4 * ΔP) / (8 * η * L)
end

"""
    stokes_einstein(T, η, a)

Calculate diffusion coefficient for spherical particle.
"""
function stokes_einstein(T, η, a)
    return (k_B * T) / (6π * η * a)
end

"""
    nernst_potential(z, C_out, C_in; T=310)

Calculate Nernst equilibrium potential.
"""
function nernst_potential(z, C_out, C_in; T=310)
    return (R * T) / (z * F) * log(C_out / C_in)
end

"""
    diffusion_1d!(du, u, p, t)

1D diffusion equation for DifferentialEquations.jl

∂C/∂t = D × ∂²C/∂x²

Uses finite differences on grid.
"""
function diffusion_1d!(du, u, p, t)
    D, dx = p
    N = length(u)

    # Boundary conditions: no flux at edges
    du[1] = D * (u[2] - u[1]) / dx^2
    du[N] = D * (u[N-1] - u[N]) / dx^2

    # Interior points
    for i in 2:N-1
        du[i] = D * (u[i+1] - 2*u[i] + u[i-1]) / dx^2
    end
end

# Example: Simulate 1D diffusion
function run_diffusion_example()
    # Grid setup
    L = 1e-3  # 1 mm domain
    N = 100
    x = range(0, L, length=N)
    dx = L / (N-1)

    # Initial condition: point source at center
    u0 = zeros(N)
    u0[N÷2] = 1.0

    # Parameters
    D = 1e-9  # m²/s
    p = (D, dx)

    # Solve
    tspan = (0.0, 100.0)  # 100 seconds
    prob = ODEProblem(diffusion_1d!, u0, tspan, p)
    sol = solve(prob, Tsit5(), saveat=10.0)

    # Plot
    plt = plot(xlabel="Position (mm)", ylabel="Concentration (arb)",
               title="1D Diffusion Over Time")
    for (i, t) in enumerate(sol.t)
        plot!(plt, x*1e3, sol.u[i], label="t=$(t)s")
    end
    return plt
end
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify the process**: Flow, diffusion, electrical, or combination?
2. **List known quantities** with units
3. **Select appropriate equation**
4. **Check dimensional consistency**
5. **Calculate and interpret**
6. **Validate reasonableness**

### Typical Problems

**Type 1: Flow calculations**
- Given: Pressure, dimensions, viscosity
- Find: Flow rate, resistance, or required pressure

**Type 2: Diffusion problems**
- Given: Distances, time, or concentrations
- Find: Diffusion time, steady-state profiles, or D values

**Type 3: Electrical problems**
- Given: Charges, distances, or potentials
- Find: Forces, fields, or capacitance

**Type 4: Thermodynamic problems**
- Given: Concentrations, temperatures, or ΔG°
- Find: ΔG, equilibrium constants, or spontaneity

## Key Relationships Summary

| Quantity | Driving Force | Conductance |
|----------|---------------|-------------|
| Volume flow | ΔP | 1/R_hydraulic |
| Current | ΔV | 1/R_electrical |
| Diffusive flux | ΔC | D/Δx |
| Heat flow | ΔT | k/Δx |

All follow the general pattern:
```
Flux = Conductance × Driving Force
```

## Saturation Kinetics (added v3.1.0)

**Michaelis-Menten** — `from scripts.foundations.kinetics import michaelis_menten`

    J = J_max * [S] / (K_m + [S])

Saturable flux for enzyme- and carrier-mediated processes: first-order in [S]
when [S] << K_m, saturating at J_max when [S] >> K_m; K_m is the substrate
concentration giving half-maximal flux. This is the foundational form behind
carrier transport, renal tubular transport maxima (Tm), GI absorption and
receptor binding. Feher develops it in Unit 2 §2.6 (facilitated diffusion);
it is filed here as a cross-domain foundation. K_m is enzyme-specific, so each
consuming equation sets its own K_m range.


## Coverage-pass additions (Feher extraction)

9 equation(s) added to this domain, each verified against Feher and a worked example.

### Whole-Body Energy Balance (`body_energy_balance`)
- **Formula:** `dE_body = (E_food + E_drink + E_inspired_air) - (E_feces + E_urine + E_expired_air + E_exfoliation + E_heat + E_work)`
- **LaTeX:** `E_{\mathrm{in}} = E_{\mathrm{out}} + \Delta E_{\mathrm{body}}\,;\quad E_{\mathrm{food}}+E_{\mathrm{drink}}+E_{\mathrm{inspired\,air}} = E_{\mathrm{feces}}+E_{\mathrm{urine}}+E_{\mathrm{expired\,air}}+E_{\mathrm{exfoliation}}+E_{\mathrm{heat}}+E_{\mathrm{work}}+\Delta E_{\mathrm{body}}`
- **Import:** `from scripts.foundations.thermodynamics import body_energy_balance` — or `from scripts.canonical_ids import load; load('body_energy_balance')`
- **Feher:** §1.1 — LIVING BEINGS TRANSFORM MATTER AND ENERGY WHILE OBEYING CONSERVATION LAWS
- Whole-body energy balance: conservation of energy (first law) applied to the body, the Atwater indirect-calorimetry basis.

### Lennard-Jones Potential (`lennard_jones_potential`)
- **Formula:** `U(r) = 4*epsilon*((sigma/r)^12 - (sigma/r)^6)`
- **LaTeX:** `U(r) = 4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6}\right] = \varepsilon\left[\left(\frac{r_m}{r}\right)^{12} - 2\left(\frac{r_m}{r}\right)^{6}\right]`
- **Import:** `from scripts.foundations.electrical import lennard_jones_potential` — or `from scripts.canonical_ids import load; load('lennard_jones_potential')`
- **Feher:** §1.4 — CLOSE APPROACH OF MOLECULES RESULTS IN A REPULSIVE FORCE: THE LENNARD-JONES POTENTIAL
- Lennard-Jones 12-6 potential: the potential energy of interaction between two nonbonding atoms or molecules as a function of separation r.

### Electric Dipole Moment (`electric_dipole_moment`)
- **Formula:** `p = q * d`
- **LaTeX:** `\mathbf{p} = q\,\mathbf{d}`
- **Import:** `from scripts.foundations.electrical import electric_dipole_moment` — or `from scripts.canonical_ids import load; load('electric_dipole_moment')`
- **Feher:** §1.4 — WATER HAS POLAR BONDS / Appendix 1.4.A1 The Dipole Moment
- Electric dipole moment magnitude: the product of the separated charge magnitude and the charge-separation distance.

### Electric Potential of a Dipole (`dipole_potential`)
- **Formula:** `U = p*cos(theta) / (4*pi*epsilon_0*kappa*r^2)`
- **LaTeX:** `U(r,\theta) = \frac{p\,\cos\theta}{4\pi\varepsilon_0\,\kappa\,r^{2}}`
- **Import:** `from scripts.foundations.electrical import dipole_potential` — or `from scripts.canonical_ids import load; load('dipole_potential')`
- **Feher:** §1.4 — Dipole-Dipole Interactions Are Effective Only Over Short Distances (derived in Appendix 1.4.A1 The Dipole Moment)
- Electric (scalar) potential U at distance r and orientation angle theta from an electric dipole of moment p, in a medium of dielectric constant kappa.

### Arrhenius Equation (`arrhenius_equation`)
- **Formula:** `k = A * exp(-E_a / (R * T))`
- **LaTeX:** `k = A\,e^{-\frac{E_a}{RT}}`
- **Import:** `from scripts.foundations.kinetics import arrhenius_equation` — or `from scripts.canonical_ids import load; load('arrhenius_equation')`
- **Feher:** §1.5 — RATES OF CHEMICAL REACTIONS DEPEND ON THE ACTIVATION ENERGY
- Arrhenius equation: the temperature dependence of a chemical reaction rate constant.

### Volume of Distribution (Fick Indicator-Dilution Principle) (`volume_of_distribution`)
- **Formula:** `V = m / C`
- **LaTeX:** `V = \frac{m}{C}`
- **Import:** `from scripts.foundations.transport import volume_of_distribution` — or `from scripts.canonical_ids import load; load('volume_of_distribution')`
- **Feher:** §1.5 — CALCULATION OF FLUID VOLUMES BY THE FICK DILUTION PRINCIPLE
- Volume of distribution of an indicator (the Fick dilution principle): the fluid-compartment volume in which a known injected amount of indicator distributes, computed from the amount introduced (m) and its equilibrium concentration (C).

### Convection-Diffusion Equation (`convection_diffusion_flux`)
- **Formula:** `J_S = -D*(dC/dx) + J_V*C`
- **LaTeX:** `J_S = -D\frac{\partial C}{\partial x} + J_V C`
- **Import:** `from scripts.foundations.diffusion import convection_diffusion_flux` — or `from scripts.canonical_ids import load; load('convection_diffusion_flux')`
- **Feher:** §1.6 — EXTERNAL FORCES CAN MOVE PARTICLES AND ALTER THE FLUX
- Convection-diffusion equation: total one-dimensional solute flux when diffusion and bulk fluid flow (convection / solvent drag) act simultaneously.

### Redox Reaction Free Energy (`redox_free_energy`)
- **Formula:** `delta_G = -n*F*delta_E`
- **LaTeX:** `\Delta G = -n F \Delta E`
- **Import:** `from scripts.foundations.thermodynamics import redox_free_energy` — or `from scripts.canonical_ids import load; load('redox_free_energy')`
- **Feher:** §1.7 — OXIDATION-REDUCTION REACTIONS CAN DO WORK
- Free energy change of an oxidation-reduction (redox) reaction computed from the reduction-potential difference of its two half-cells: delta_G = -n*F*delta_E, where n is the number of electrons transferred per reaction, F is the Faraday constant, and delta_E is the difference in reduction potentials (E_acceptor - E_donor).

### Ideal Gas Law (`ideal_gas_law`)
- **Formula:** `P = n*R*T/V   (from P*V = n*R*T)`
- **LaTeX:** `PV = nRT`
- **Import:** `from scripts.foundations.thermodynamics import ideal_gas_law` — or `from scripts.canonical_ids import load; load('ideal_gas_law')`
- **Feher:** §6.1 — CHANGES IN LUNG VOLUMES PRODUCE THE PRESSURE DIFFERENCES THAT DRIVE AIR MOVEMENT
- The ideal gas law relates the pressure, volume, moles, and absolute temperature of an ideal gas of constant composition.


### Coverage pass 2 (residual reconsideration)

**Enthalpy** (`enthalpy`): `H = E + P*V` — `from scripts.foundations.thermodynamics import enthalpy`. Feher §1.4. Enthalpy: internal energy plus the pressure-volume product.



## Review additions (2026-07-15)

- **bioavailability_auc** — `F = (AUC_oral/AUC_iv)(D_iv/D_oral)` — Absolute oral bioavailability from dose-normalised exposure ratio. Import: `from scripts.foundations.kinetics import bioavailability_auc_equation` (or `load("bioavailability_auc")`).
- **average_steady_state_concentration** — `Css_avg = F*Dose/(CL*tau)` — Average steady-state level for repeated dosing (discrete infusion analogue). Import: `from scripts.foundations.kinetics import average_steady_state_concentration_equation` (or `load("average_steady_state_concentration")`).

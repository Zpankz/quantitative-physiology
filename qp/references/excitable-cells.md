---
name: excitable-cells
description: Membrane potential, action potentials, nerve conduction, and muscle mechanics including skeletal and smooth muscle
parent: quantitative-physiology
unit: 3
---

# Physiology of Excitable Cells

## Overview

This sub-skill covers the quantitative electrophysiology of excitable cells (neurons and muscle), including membrane potential generation, action potential dynamics, signal propagation, and muscle mechanics. These concepts form the foundation for understanding neural signaling and motor function.

## Core Concepts

### 1. The Membrane Potential

#### Nernst Equation

Equilibrium potential for a single ion species:
Formula → qp:`nernst_equation`

At 37°C (310 K):
```
E_ion = (26.7 mV/z) × ln(C_out/C_in)
E_ion ≈ (61.5 mV/z) × log₁₀(C_out/C_in)
```

**Typical equilibrium potentials**:
| Ion | [Out] mM | [In] mM | E_ion (mV) |
|-----|----------|---------|------------|
| K⁺ | 5 | 140 | -90 |
| Na⁺ | 145 | 12 | +67 |
| Ca²⁺ | 2 | 0.0001 | +129 |
| Cl⁻ | 120 | 4 | -89 |

#### Goldman-Hodgkin-Katz (GHK) Equation

Membrane potential with multiple permeable ions:
Formula → qp:`ghk_potential`

**Relative permeabilities at rest**:
- P_K : P_Na : P_Cl ≈ 1 : 0.04 : 0.45

**Resting membrane potential**: V_m ≈ -70 to -90 mV

#### Equivalent Circuit Model

**Membrane as electrical circuit**:
```
        ┌───R_Na───┐
   ─────┤    E_Na  ├─────
        └──────────┘
        ┌───R_K────┐
   ─────┤    E_K   ├─────
        └──────────┘
        ┌───R_Cl───┐
   ─────┤    E_Cl  ├─────
        └──────────┘
        ┌────C_m───┐
   ─────┤          ├─────
        └──────────┘
```

**Chord conductance equation**:
Formula → qp:`chord_conductance`

### 2. The Action Potential

#### Hodgkin-Huxley Model

**Membrane current equation**:
Formula → qp:`hh_membrane_current`

**Ionic currents**:
Formula → qp:`hh_sodium_current`
Formula → qp:`hh_potassium_current`
Formula → qp:`hh_leak_current`

**Gating variables** (m, h, n):
Formula → qp:`hh_gating_m`
Formula → qp:`hh_gating_h`
Formula → qp:`hh_gating_n`

**Rate constants** (original Hodgkin-Huxley):
```
α_m = 0.1(V+40) / [1 - exp(-(V+40)/10)]
β_m = 4 × exp(-(V+65)/18)
α_h = 0.07 × exp(-(V+65)/20)
β_h = 1 / [1 + exp(-(V+35)/10)]
α_n = 0.01(V+55) / [1 - exp(-(V+55)/10)]
β_n = 0.125 × exp(-(V+65)/80)
```

#### Action Potential Phases

| Phase | Duration | Mechanism | V_m change |
|-------|----------|-----------|------------|
| Resting | - | K⁺ leak dominates | -70 mV |
| Depolarization | ~0.5 ms | Na⁺ channels open | → +30 mV |
| Repolarization | ~1 ms | Na⁺ inactivate, K⁺ open | → -70 mV |
| Hyperpolarization | ~2-3 ms | K⁺ channels slow to close | → -80 mV |
| Refractory | ~2-4 ms | Na⁺ recovery | back to rest |

#### Threshold and All-or-None

**Threshold**: V_m ≈ -55 mV (typically ~15 mV above rest)

**Threshold condition**: Net inward current at threshold
```
I_Na + I_K + I_L = 0 with dI_Na/dV > dI_K/dV
```

**All-or-none property**: Once threshold reached, full AP fires regardless of stimulus strength.

### 3. Action Potential Propagation

#### Cable Theory

**Cable equation** (passive spread):
Formula → qp:`cable_equation`

**Space constant** (length constant):
Formula → qp:`space_constant`
Where:
- r_m = membrane resistance per unit length (Ω·cm)
- r_i = axoplasm resistance per unit length (Ω/cm)
- a = axon radius
- R_m = specific membrane resistance (Ω·cm²)
- R_i = axoplasm resistivity (Ω·cm)

**Time constant**:
Formula → qp:`membrane_time_constant`

**Typical values**:
- λ ≈ 0.1-1 mm (unmyelinated), 1-2 mm (myelinated)
- τ ≈ 1-20 ms

#### Conduction Velocity

**Unmyelinated axon**:
```
θ ∝ √a    (velocity proportional to √radius)
```

**Myelinated axon**:
```
θ ∝ a    (velocity proportional to radius)
```

Saltatory conduction: AP jumps node to node
- Internode distance ≈ 100 × axon diameter
- Node length ≈ 1 μm

**Typical velocities**:
| Fiber type | Diameter (μm) | Velocity (m/s) |
|------------|---------------|----------------|
| Aα | 12-20 | 70-120 |
| Aβ | 5-12 | 30-70 |
| Aδ | 2-5 | 12-30 |
| B | 1-3 | 3-15 |
| C (unmyelinated) | 0.4-1.2 | 0.5-2 |

### 4. Skeletal Muscle Mechanics

#### Force-Length Relationship

**Isometric tension** vs sarcomere length:

```
        Tension
           │
    100% ──┼────────╮
           │       ╱ ╲
           │      ╱   ╲
           │     ╱     ╲
           │    ╱       ╲
           │   ╱         ╲
         0 ┼──╱───────────╲────
           └────────────────────
              1.5  2.0  2.5  3.5
              Sarcomere length (μm)
```

**Optimal length**: ~2.0-2.2 μm (maximum overlap of thick and thin filaments)

**Mathematical model**:
```
F = F_max × f(L)
```

Where f(L) is the overlap function based on filament geometry.

#### Force-Velocity Relationship

**Hill equation** (hyperbolic):
Formula → qp:`hill_force_velocity`

Or equivalently:
Formula → qp:`hill_force_velocity`

Where:
- F_0 = isometric force (v = 0)
- a, b = Hill constants
- a/F_0 ≈ 0.25-0.5
- b ≈ 0.25 × muscle lengths/s

**Key points**:
- Maximum velocity (v_max) at F = 0: v_max = b × F_0/a
- Maximum power at F ≈ 0.3 × F_0

#### Twitch and Tetanus

**Single twitch**:
- Latent period: ~2 ms
- Contraction time: ~20-100 ms (depending on fiber type)
- Relaxation time: ~20-200 ms

**Temporal summation**:
```
F_tetanus ≈ 3-5 × F_twitch    (fused tetanus)
```

**Stimulation frequency for tetanus**:
- Fast twitch: >50 Hz
- Slow twitch: >20 Hz

### 5. Contractile Mechanisms

#### Cross-Bridge Cycle

**Huxley 1957 model**:
Formula → qp:`huxley_attachment_rate`
Formula → qp:`huxley_detachment_rate`

**Fraction of attached bridges** (n):
Formula → qp:`huxley_attached_fraction`

**Steady-state during isometric contraction**:
```
n = f / (f + g)
```

#### Power Output

**Mechanical power**:
Formula → qp:`muscle_power`

**Maximum power** occurs at:
```
F_opt ≈ 0.3 × F_0
v_opt ≈ 0.3 × v_max
P_max ≈ 0.1 × F_0 × v_max
```

#### Muscle Energetics

**ATP consumption**:
Formula → qp:`atp_consumption`

**Efficiency**:
Formula → qp:`muscle_efficiency`

Maximum efficiency ≈ 25-40%

**Heat components**:
- Activation heat: Released upon stimulation
- Shortening heat: Proportional to shortening distance
- Maintenance heat: Sustained during isometric contraction

### 6. Excitation-Contraction Coupling

#### Ca²⁺ Signaling

**T-tubule to SR coupling**:
```
AP → T-tubule depolarization → DHPR activation → RyR opening → Ca²⁺ release
```

**Ca²⁺ transient**:
- Resting [Ca²⁺]_i: ~50-100 nM
- Peak during contraction: ~1-10 μM
- Time course: ~50-100 ms (skeletal)

**Force-[Ca²⁺] relationship** (Hill equation):
Formula → qp:`ca_force_relationship`

Where n ≈ 2-4 (Hill coefficient, reflecting cooperative binding to troponin)

#### Neuromuscular Junction

**End-plate potential** (EPP):
```
EPP ≈ 70-80 mV    (suprathreshold)
MEPP ≈ 0.5-1 mV  (single vesicle)
```

**Quantal content**:
Formula → qp:`quantal_content_epp_mepp`

**Safety factor**: EPP/Threshold ≈ 3-4

### 7. Smooth Muscle

#### Differences from Skeletal Muscle

| Property | Skeletal | Smooth |
|----------|----------|--------|
| Control | Neural (voluntary) | Autonomic, hormonal |
| Ca²⁺ source | SR mainly | SR + extracellular |
| Regulatory protein | Troponin | Calmodulin-MLCK |
| Cross-bridge cycling | Fast | Slow (latch state) |
| Length-tension | Narrow range | Broad range |

#### Latch State

**Sustained contraction with low ATP use**:
- Dephosphorylated cross-bridges remain attached
- Force maintained at 10-20% of ATP cost
- Important for vascular tone, sphincters

## Computational Models

### Python Implementation

```python
import numpy as np
from scipy.integrate import odeint, solve_ivp
import matplotlib.pyplot as plt

# Physical constants
R = 8.314       # J/(mol·K)
F = 96485       # C/mol

class ExcitableCells:
    """Quantitative models for excitable cell physiology"""

    @staticmethod
    def nernst_potential(z, C_out, C_in, T=310):
        """
        Nernst equilibrium potential

        Parameters:
        -----------
        z : int - Ion valence
        C_out, C_in : float - Concentrations
        T : float - Temperature (K)

        Returns:
        --------
        E : float - Equilibrium potential (V)
        """
        return (R * T) / (z * F) * np.log(C_out / C_in)

    @staticmethod
    def ghk_potential(P_K, P_Na, P_Cl, K_o, K_i, Na_o, Na_i, Cl_o, Cl_i, T=310):
        """
        Goldman-Hodgkin-Katz potential

        Returns:
        --------
        V_m : float - Membrane potential (V)
        """
        numerator = P_K * K_o + P_Na * Na_o + P_Cl * Cl_i
        denominator = P_K * K_i + P_Na * Na_i + P_Cl * Cl_o
        return (R * T / F) * np.log(numerator / denominator)

    @staticmethod
    def space_constant(R_m, R_i, a):
        """
        Cable space constant (length constant)

        Parameters:
        -----------
        R_m : float - Specific membrane resistance (Ω·cm²)
        R_i : float - Axoplasm resistivity (Ω·cm)
        a : float - Axon radius (cm)

        Returns:
        --------
        lambda : float - Space constant (cm)
        """
        return np.sqrt(R_m * a / (2 * R_i))

    @staticmethod
    def time_constant(R_m, C_m):
        """
        Membrane time constant

        Parameters:
        -----------
        R_m : float - Specific membrane resistance (Ω·cm²)
        C_m : float - Specific membrane capacitance (F/cm²)

        Returns:
        --------
        tau : float - Time constant (s)
        """
        return R_m * C_m

    @staticmethod
    def hill_force_velocity(F_0, a, b, F=None, v=None):
        """
        Hill force-velocity relationship

        Provide either F or v to calculate the other.

        Parameters:
        -----------
        F_0 : float - Isometric force
        a, b : float - Hill constants
        F : float - Force (optional)
        v : float - Velocity (optional)

        Returns:
        --------
        v or F : float
        """
        if F is not None:
            return b * (F_0 - F) / (F + a)
        elif v is not None:
            return (F_0 * b - a * v) / (v + b)
        else:
            raise ValueError("Must provide either F or v")

    @staticmethod
    def muscle_power(F, v):
        """Mechanical power output"""
        return F * v

    @staticmethod
    def ca_force_relationship(Ca, K_d, n=3, F_max=1.0):
        """
        Force-calcium relationship (Hill equation)

        Parameters:
        -----------
        Ca : float or array - Calcium concentration
        K_d : float - Dissociation constant
        n : float - Hill coefficient
        F_max : float - Maximum force

        Returns:
        --------
        F : float or array - Force
        """
        return F_max * Ca**n / (K_d**n + Ca**n)


class HodgkinHuxley:
    """
    Hodgkin-Huxley model of the action potential
    """

    def __init__(self, C_m=1.0, g_Na=120, g_K=36, g_L=0.3,
                 E_Na=50, E_K=-77, E_L=-54.4):
        """
        Parameters:
        -----------
        C_m : float - Membrane capacitance (μF/cm²)
        g_Na, g_K, g_L : float - Maximum conductances (mS/cm²)
        E_Na, E_K, E_L : float - Reversal potentials (mV)
        """
        self.C_m = C_m
        self.g_Na = g_Na
        self.g_K = g_K
        self.g_L = g_L
        self.E_Na = E_Na
        self.E_K = E_K
        self.E_L = E_L

    def alpha_m(self, V):
        """Rate constant for m activation"""
        return 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10))

    def beta_m(self, V):
        """Rate constant for m deactivation"""
        return 4 * np.exp(-(V + 65) / 18)

    def alpha_h(self, V):
        """Rate constant for h deactivation"""
        return 0.07 * np.exp(-(V + 65) / 20)

    def beta_h(self, V):
        """Rate constant for h recovery"""
        return 1 / (1 + np.exp(-(V + 35) / 10))

    def alpha_n(self, V):
        """Rate constant for n activation"""
        return 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10))

    def beta_n(self, V):
        """Rate constant for n deactivation"""
        return 0.125 * np.exp(-(V + 65) / 80)

    def derivatives(self, t, y, I_ext=0):
        """
        ODE system for Hodgkin-Huxley model

        Parameters:
        -----------
        t : float - Time
        y : array - State variables [V, m, h, n]
        I_ext : float - External current (μA/cm²)

        Returns:
        --------
        dy : array - Derivatives
        """
        V, m, h, n = y

        # Ionic currents
        I_Na = self.g_Na * m**3 * h * (V - self.E_Na)
        I_K = self.g_K * n**4 * (V - self.E_K)
        I_L = self.g_L * (V - self.E_L)

        # Membrane potential
        dV = (I_ext - I_Na - I_K - I_L) / self.C_m

        # Gating variables
        dm = self.alpha_m(V) * (1 - m) - self.beta_m(V) * m
        dh = self.alpha_h(V) * (1 - h) - self.beta_h(V) * h
        dn = self.alpha_n(V) * (1 - n) - self.beta_n(V) * n

        return [dV, dm, dh, dn]

    def steady_state(self, V):
        """Calculate steady-state values of gating variables"""
        m_inf = self.alpha_m(V) / (self.alpha_m(V) + self.beta_m(V))
        h_inf = self.alpha_h(V) / (self.alpha_h(V) + self.beta_h(V))
        n_inf = self.alpha_n(V) / (self.alpha_n(V) + self.beta_n(V))
        return m_inf, h_inf, n_inf

    def simulate(self, t_span, I_ext_func=None, V0=-65):
        """
        Simulate action potential

        Parameters:
        -----------
        t_span : tuple - (t_start, t_end)
        I_ext_func : callable - External current as function of time
        V0 : float - Initial membrane potential

        Returns:
        --------
        t, V, m, h, n : arrays
        """
        if I_ext_func is None:
            I_ext_func = lambda t: 10 if 1 < t < 2 else 0

        # Initial conditions
        m0, h0, n0 = self.steady_state(V0)
        y0 = [V0, m0, h0, n0]

        # Wrapper for ODE solver
        def ode_func(t, y):
            return self.derivatives(t, y, I_ext_func(t))

        # Solve
        t_eval = np.linspace(t_span[0], t_span[1], 1000)
        sol = solve_ivp(ode_func, t_span, y0, t_eval=t_eval, method='RK45')

        return sol.t, sol.y[0], sol.y[1], sol.y[2], sol.y[3]


class HuxleyMuscle:
    """
    Huxley 1957 cross-bridge model
    """

    def __init__(self, f1=43.3, g1=10, g2=209, h=10e-9):
        """
        Parameters:
        -----------
        f1 : float - Attachment rate constant (s⁻¹)
        g1 : float - Detachment rate constant (s⁻¹)
        g2 : float - Rapid detachment rate (s⁻¹)
        h : float - Cross-bridge stroke distance (m)
        """
        self.f1 = f1
        self.g1 = g1
        self.g2 = g2
        self.h = h

    def f(self, x):
        """Attachment rate function"""
        if 0 < x < self.h:
            return self.f1 * (self.h - x) / self.h
        return 0

    def g(self, x):
        """Detachment rate function"""
        if x < 0:
            return self.g2 * (-x) / self.h
        elif 0 <= x < self.h:
            return self.g1
        else:
            return self.g2 * (x - self.h) / self.h

    def steady_state_n(self, x):
        """Steady-state fraction of attached bridges"""
        f = self.f(x)
        g = self.g(x)
        if f + g > 0:
            return f / (f + g)
        return 0


# Example usage and visualization
if __name__ == "__main__":
    # Create models
    ec = ExcitableCells()
    hh = HodgkinHuxley()

    # Calculate Nernst potentials
    E_K = ec.nernst_potential(1, 5, 140) * 1000  # mV
    E_Na = ec.nernst_potential(1, 145, 12) * 1000  # mV
    print(f"E_K = {E_K:.1f} mV")
    print(f"E_Na = {E_Na:.1f} mV")

    # Simulate action potential
    t, V, m, h, n = hh.simulate((0, 20))

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(t, V, 'b-', linewidth=2)
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane potential (mV)')
    plt.title('Hodgkin-Huxley Action Potential')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(t, m, 'r-', label='m (Na⁺ activation)')
    plt.plot(t, h, 'g-', label='h (Na⁺ inactivation)')
    plt.plot(t, n, 'b-', label='n (K⁺ activation)')
    plt.xlabel('Time (ms)')
    plt.ylabel('Gating variable')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('hodgkin_huxley.png', dpi=150)

    # Force-velocity relationship
    F_0 = 100  # N
    a = 25     # N
    b = 1.0    # m/s

    F_range = np.linspace(0, F_0, 100)
    v_range = ec.hill_force_velocity(F_0, a, b, F=F_range)
    P_range = F_range * v_range

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.plot(v_range, F_range, 'b-', linewidth=2)
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Force (N)')
    plt.title('Force-Velocity Relationship')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(v_range, P_range, 'r-', linewidth=2)
    plt.xlabel('Velocity (m/s)')
    plt.ylabel('Power (W)')
    plt.title('Power-Velocity Relationship')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('muscle_mechanics.png', dpi=150)
```

### Julia Implementation

```julia
using DifferentialEquations
using Plots

# Physical constants
const R = 8.314   # J/(mol·K)
const F_const = 96485  # C/mol

"""
    nernst_potential(z, C_out, C_in; T=310)

Calculate Nernst equilibrium potential (V).
"""
function nernst_potential(z, C_out, C_in; T=310)
    return (R * T) / (z * F_const) * log(C_out / C_in)
end

"""
    ghk_potential(P_K, P_Na, P_Cl, ions_out, ions_in; T=310)

Goldman-Hodgkin-Katz equation.
ions_out/in = (K, Na, Cl) tuples
"""
function ghk_potential(P_K, P_Na, P_Cl, ions_out, ions_in; T=310)
    K_o, Na_o, Cl_o = ions_out
    K_i, Na_i, Cl_i = ions_in

    num = P_K * K_o + P_Na * Na_o + P_Cl * Cl_i
    den = P_K * K_i + P_Na * Na_i + P_Cl * Cl_o

    return (R * T / F_const) * log(num / den)
end

"""
    hill_force_velocity(F_0, a, b, F)

Calculate velocity from force using Hill equation.
"""
function hill_force_velocity(F_0, a, b, F)
    return b * (F_0 - F) / (F + a)
end

"""
Hodgkin-Huxley model parameters and equations.
"""
module HodgkinHuxley

const C_m = 1.0      # μF/cm²
const g_Na = 120.0   # mS/cm²
const g_K = 36.0     # mS/cm²
const g_L = 0.3      # mS/cm²
const E_Na = 50.0    # mV
const E_K = -77.0    # mV
const E_L = -54.4    # mV

# Rate constants
α_m(V) = 0.1 * (V + 40) / (1 - exp(-(V + 40) / 10))
β_m(V) = 4 * exp(-(V + 65) / 18)
α_h(V) = 0.07 * exp(-(V + 65) / 20)
β_h(V) = 1 / (1 + exp(-(V + 35) / 10))
α_n(V) = 0.01 * (V + 55) / (1 - exp(-(V + 55) / 10))
β_n(V) = 0.125 * exp(-(V + 65) / 80)

# Steady states
m_inf(V) = α_m(V) / (α_m(V) + β_m(V))
h_inf(V) = α_h(V) / (α_h(V) + β_h(V))
n_inf(V) = α_n(V) / (α_n(V) + β_n(V))

"""
    hh_ode!(du, u, p, t)

Hodgkin-Huxley ODE system.
u = [V, m, h, n]
p = I_ext (external current function)
"""
function hh_ode!(du, u, p, t)
    V, m, h, n = u
    I_ext = p(t)

    # Ionic currents
    I_Na = g_Na * m^3 * h * (V - E_Na)
    I_K = g_K * n^4 * (V - E_K)
    I_L = g_L * (V - E_L)

    # Derivatives
    du[1] = (I_ext - I_Na - I_K - I_L) / C_m
    du[2] = α_m(V) * (1 - m) - β_m(V) * m
    du[3] = α_h(V) * (1 - h) - β_h(V) * h
    du[4] = α_n(V) * (1 - n) - β_n(V) * n
end

"""
    simulate(tspan, I_ext; V0=-65.0)

Simulate Hodgkin-Huxley model.
"""
function simulate(tspan, I_ext; V0=-65.0)
    # Initial conditions at steady state
    u0 = [V0, m_inf(V0), h_inf(V0), n_inf(V0)]

    prob = ODEProblem(hh_ode!, u0, tspan, I_ext)
    sol = solve(prob, Tsit5(), saveat=0.01)

    return sol
end

end  # module HodgkinHuxley

"""
    muscle_power_curve(F_0, a, b)

Generate force-velocity and power-velocity curves.
"""
function muscle_power_curve(F_0, a, b)
    F = range(0, F_0, length=100)
    v = hill_force_velocity.(F_0, a, b, F)
    P = F .* v

    return F, v, P
end

# Example: Simulate and plot action potential
function run_example()
    # Current pulse
    I_ext(t) = 1 < t < 2 ? 10.0 : 0.0

    sol = HodgkinHuxley.simulate((0.0, 20.0), I_ext)

    p1 = plot(sol.t, sol[1, :],
              xlabel="Time (ms)",
              ylabel="V (mV)",
              title="Hodgkin-Huxley Action Potential",
              legend=false)

    p2 = plot(sol.t, sol[2, :], label="m")
    plot!(p2, sol.t, sol[3, :], label="h")
    plot!(p2, sol.t, sol[4, :], label="n",
          xlabel="Time (ms)",
          ylabel="Gating variable",
          title="Gating Variables")

    plot(p1, p2, layout=(2, 1), size=(800, 600))
end
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify cell type**: Neuron, skeletal muscle, cardiac, smooth?
2. **Determine phase**: Resting, active, refractory?
3. **List relevant ions and their concentrations**
4. **Calculate equilibrium potentials** (Nernst)
5. **Apply appropriate model** (GHK, H-H, Hill)
6. **Validate physiological range**

### Typical Problems

**Type 1: Membrane potential**
- Given: Ion concentrations, permeabilities
- Find: Resting potential, reversal potential

**Type 2: Action potential**
- Given: Stimulus, channel properties
- Find: AP shape, threshold, refractory period

**Type 3: Conduction**
- Given: Axon properties
- Find: Conduction velocity, space/time constants

**Type 4: Muscle mechanics**
- Given: Force or velocity
- Find: The other, power output

## Key Relationships Summary

| Quantity | Equation | Units |
|----------|----------|-------|
| Nernst potential | E = (RT/zF)ln(C_o/C_i) | V |
| Space constant | λ = √(R_m·a/2R_i) | cm |
| Time constant | τ = R_m × C_m | s |
| Conduction velocity | θ ∝ √a (unmyel), θ ∝ a (myel) | m/s |
| Hill equation | (F+a)(v+b) = (F_0+a)b | - |
| Maximum power | P_max ≈ 0.1 × F_0 × v_max | W |


## Coverage-pass additions (Feher extraction)

3 equation(s) added to this domain, each verified against Feher and a worked example.

### Weiss Strength-Duration Equation (`strength_duration_weiss`)
- **Formula:** `I = I_rh * (t + tau_SD) / t`
- **LaTeX:** `I = I_{\mathrm{rh}}\frac{(t + \tau_{\mathrm{SD}})}{t} = I_{\mathrm{rh}} + I_{\mathrm{rh}}\frac{\tau_{\mathrm{SD}}}{t}`
- **Import:** `from scripts.excitable.action_potential import strength_duration_weiss` — or `from scripts.canonical_ids import load; load('strength_duration_weiss')`
- **Feher:** §3.2 — THE STRENGTH-DURATION RELATIONSHIP IS HYPERBOLIC
- Weiss strength-duration equation: the minimum (threshold) stimulus current needed to trigger an action potential with a rectangular current pulse of duration t.

### Architectural Gear Ratio (`architectural_gear_ratio`)
- **Formula:** `AGR = epsilon_x / epsilon_f = (dL_muscle/dt) / (dL_fiber/dt)`
- **LaTeX:** `AGR = \frac{\varepsilon_x}{\varepsilon_f} = \frac{dL_{\mathrm{muscle}}/dt}{dL_{\mathrm{fiber}}/dt}`
- **Import:** `from scripts.excitable.muscle import architectural_gear_ratio` — or `from scripts.canonical_ids import load; load('architectural_gear_ratio')`
- **Feher:** §3.4 — THE ARCHITECTURAL GEAR RATIO ALLOWS VARIATION IN SPEED AND FORCE
- The architectural gear ratio quantifies how skeletal-muscle architecture trades force for speed by relating the shortening of the whole muscle to the shortening of its constituent fibers.

### Motor Unit Tetanic Force (`motor_unit_force`)
- **Formula:** `F_MU = N * F_MF = N * A * F_S`
- **LaTeX:** `F_{\mathrm{MU}} = N F_{\mathrm{MF}} = N A F_{\mathrm{S}}`
- **Import:** `from scripts.excitable.muscle import motor_unit_force` — or `from scripts.canonical_ids import load; load('motor_unit_force')`
- **Feher:** §3.4 — THE INNERVATION RATIO RESULTS IN A PROPORTIONAL CONTROL OF MUSCLE FORCE
- Tetanic force produced by a single motor unit as the product of the innervation ratio (N, fibers per motor neuron), the cross-sectional area per fiber (A), and the fiber specific force (F_S, ~20 N/cm^2).



## Review additions (2026-07-15)

- **passive_membrane_charging** — `V(t) = I*R*(1 - e^-t/tau)` — Subthreshold RC charging; ~63% of steady IR at one time constant. Import: `from scripts.excitable.action_potential import passive_membrane_charging_equation` (or `load("passive_membrane_charging")`).
- **hursh_conduction_velocity** — `theta = 6 x D` — Myelinated-fibre conduction velocity vs outer diameter (Hursh 1939). Import: `from scripts.excitable.action_potential import hursh_conduction_velocity_equation` (or `load("hursh_conduction_velocity")`).

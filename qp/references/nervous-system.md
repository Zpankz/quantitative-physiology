---
name: nervous-system
description: Nervous system physiology - synaptic transmission, sensory physiology, motor control, and neural integration
parent: quantitative-physiology
unit: 4
---

# Nervous System Physiology

## Overview

This sub-skill covers the quantitative aspects of nervous system function, from synaptic transmission to sensory processing and motor output. It builds on the excitable cell foundations to explain neural communication, sensory encoding, and motor control.

## Core Concepts

### 1. Synaptic Transmission

#### Chemical Synapse Structure

**Components**:
- Presynaptic terminal (bouton): Contains vesicles with neurotransmitter
- Synaptic cleft: ~20-40 nm gap
- Postsynaptic membrane: Contains receptors

**Vesicle characteristics**:
- Diameter: ~40-50 nm (small clear vesicles)
- Neurotransmitter content: ~5000-10000 molecules per vesicle
- Release probability (p): 0.1-0.9 depending on synapse type

#### Vesicle Release Kinetics

**Calcium-triggered release**:
```
Release rate ∝ [Ca²⁺]ⁿ   where n ≈ 3-4
```

**Cooperative binding model**:
Formula → qp:`ca_release_cooperative`

Where K_d ≈ 10-20 μM for release machinery

**Quantal release**:
Formula → qp:`quantal_content`
Where:
- n = number of release sites
- p = probability of release per site

**Variance analysis**:
```
Variance = n × p × (1-p) × q²
Mean = n × p × q

Therefore: p = 1 - (Variance/Mean × q)
```

#### Postsynaptic Potentials

**Synaptic current**:
Formula → qp:`synaptic_current`

**EPSP amplitude**:
Formula → qp:`epsp_amplitude`

**Time course** (alpha function):
Formula → qp:`alpha_function`
Peak occurs at t = τ

**Double exponential synaptic conductance**:
Formula → qp:`double_exponential_synapse`

#### Synaptic Integration

**Temporal summation**:
```
V(t) = V₀ × e^(-t/τ_m) + EPSP_new
```

**Spatial summation** (linear approximation):
```
V_total = Σ EPSP_i × λ_i
```
Where λ_i accounts for electrotonic decay

**Cable equation for dendrites**:
Formula → qp:`cable_equation_dendrite`

**Input resistance of dendrite**:
Formula → qp:`dendrite_input_resistance`

### 2. Neurotransmitter Systems

#### Acetylcholine (ACh)

**Synthesis**:
```
Choline + Acetyl-CoA → ACh + CoA
         ChAT
```

**Nicotinic receptor kinetics**:
```
ACh + R ⇌ ACh·R → ACh·R* (open)
        K_d        β/α
```

**Channel conductance**: γ ≈ 25-30 pS

**Mean open time**:
```
τ_open = 1/(α + k_-2)  ≈ 1-2 ms
```

**Muscarinic receptor (G-protein coupled)**:
- M1, M3, M5: Gq → PLC → IP₃ + DAG
- M2, M4: Gi → ↓cAMP, ↑K⁺ conductance

#### Glutamate

**AMPA receptor**:
- Fast kinetics: τ_decay ≈ 2-5 ms
- Conductance: γ ≈ 10-15 pS
- E_rev ≈ 0 mV

**NMDA receptor**:
- Slow kinetics: τ_decay ≈ 50-200 ms
- Voltage-dependent Mg²⁺ block:
Formula → qp:`nmda_mg_block`
Where K_Mg ≈ 3.6 mM, V_half ≈ -17 mV

- Ca²⁺ permeability: P_Ca/P_Na ≈ 10

#### GABA

**GABA_A receptor**:
- Cl⁻ channel
- E_rev = E_Cl ≈ -70 to -80 mV
- τ_decay ≈ 10-30 ms

**Shunting inhibition**:
Formula → qp:`shunting_inhibition`

### 3. Sensory Physiology

#### Weber-Fechner Law

**Weber's Law** (difference threshold):
Formula → qp:`weber_fraction`

**Fechner's Law** (perceived intensity):
Formula → qp:`fechner_law`
Where:
- S = sensation magnitude
- I = stimulus intensity
- I₀ = threshold intensity

#### Stevens' Power Law

More accurate for most modalities:
Formula → qp:`stevens_power_law`

| Modality | Exponent n |
|----------|-----------|
| Brightness | 0.33 |
| Loudness | 0.6 |
| Electric shock | 3.5 |
| Length | 1.0 |
| Pressure | 1.1 |

#### Receptor Adaptation

**First-order adaptation**:
Formula → qp:`receptor_adaptation`

**Adaptation index**:
Formula → qp:`adaptation_index`

**Phasic vs tonic receptors**:
- Phasic: High AI, rapid adaptation (e.g., Pacinian corpuscle)
- Tonic: Low AI, sustained response (e.g., Merkel disc)

#### Visual System

**Photoreceptor response** (rod):
Formula → qp:`photoreceptor_response`
Where σ = half-saturation intensity, n ≈ 0.7-1

**Weber-Fechner in vision**:
```
ΔI/I ≈ 0.01-0.02 (under optimal conditions)
```

**Temporal frequency response**:
```
H(f) = (1 + i×f/f_c)^(-1) × (i×f/f_hp) / (1 + i×f/f_hp)
```
Bandpass filter with f_c ≈ 10-20 Hz, f_hp ≈ 1 Hz

**Receptive field** (difference of Gaussians):
Formula → qp:`receptive_field_dog`
Where σ_s > σ_c (surround larger than center)

#### Auditory System

**Basilar membrane mechanics**:
```
Characteristic frequency vs position:
f(x) = f_max × e^(-x/λ)
```
Where λ ≈ 7 mm for human cochlea

**Place theory**: Different frequencies maximally excite different locations

**Phase locking**: Up to ~4-5 kHz

**Intensity coding**:
- Rate coding: firing rate ∝ log(intensity)
- Population coding: recruitment of fibers

### 4. Motor Control

#### Motor Unit

**Motor unit** = α-motor neuron + muscle fibers it innervates

**Size principle** (Henneman):
```
Recruitment order: Small → Large motor neurons
```

**Twitch characteristics by fiber type**:
| Type | Contraction time | Fatigue resistance |
|------|-----------------|-------------------|
| Type I (slow) | 90-140 ms | High |
| Type IIa (fast) | 30-50 ms | Moderate |
| Type IIx (fast) | 20-40 ms | Low |

#### Force Modulation

**Rate coding**:
Formula → qp:`rate_force_relation`

**Fusion frequency**:
Formula → qp:`fusion_frequency`
- Slow fibers: ~20-30 Hz
- Fast fibers: ~50-100 Hz

**Total force** (summation):
```
F_total = Σ F_i × (recruited fraction_i)
```

#### Reflexes

**Stretch reflex gain**:
Formula → qp:`reflex_gain`

**Reflex latency**:
```
t_reflex = t_afferent + t_synapse + t_efferent + t_mechanical
```

Monosynaptic stretch reflex: ~25-35 ms

**H-reflex vs M-wave**:
- H-reflex: afferent pathway test
- M-wave: direct motor response

#### Proprioception

**Muscle spindle response**:
Formula → qp:`spindle_response`
Position + velocity sensitivity

**Golgi tendon organ**:
Formula → qp:`gto_response`
Force sensitivity (series with muscle)

### 5. Neural Coding

#### Rate Coding

**Firing rate**:
```
r = (number of spikes) / (time window)
```

**Relationship to stimulus**:
```
r = r_max × f(I) where f = sigmoid, log, or power function
```

#### Temporal Coding

**Spike timing precision**:
```
σ_timing ≈ 1-5 ms (cortical neurons)
```

**Information per spike**:
```
I_spike ≈ log₂(1/σ_timing × Δt)
```

#### Population Coding

**Vector averaging** (motor cortex):
```
M⃗ = Σ w_i × d⃗_i × r_i
```
Where d⃗_i = preferred direction of neuron i

**Fisher information** (for orientation):
```
I_F = Σ (df_i/dθ)² / σ_i²
```

### 6. Synaptic Plasticity

#### Short-Term Plasticity

**Facilitation**:
Formula → qp:`facilitation`
Calcium accumulation → enhanced release

**Depression**:
Formula → qp:`depression`
Vesicle depletion

**Tsodyks-Markram model**:
```
dx/dt = (1-x)/τ_rec - u × x × δ(t-t_spike)
du/dt = (U-u)/τ_fac + U × (1-u) × δ(t-t_spike)
EPSP ∝ A × u × x
```

#### Long-Term Plasticity

**LTP induction threshold** (calcium hypothesis):
```
[Ca²⁺]_i > θ_LTP → LTP
θ_LTD < [Ca²⁺]_i < θ_LTP → LTD
[Ca²⁺]_i < θ_LTD → no change
```

**BCM theory** (sliding threshold):
Formula → qp:`bcm_theory`
Where θ_m = f(⟨r⟩²) adjusts with activity

**STDP rule**:
Formula → qp:`stdp`
Where τ₊ ≈ 20 ms, τ₋ ≈ 20 ms

## Computational Models

### Python Implementation

```python
import numpy as np
from scipy.integrate import odeint
from scipy.signal import convolve

# Physical constants
R = 8.314       # J/(mol·K)
F = 96485       # C/mol
T = 310         # K (37°C)

class SynapticTransmission:
    """Models for synaptic transmission and integration"""

    @staticmethod
    def alpha_synapse(t, g_max, tau):
        """
        Alpha function synaptic conductance

        Parameters:
        -----------
        t : array - Time points (s)
        g_max : float - Peak conductance (S)
        tau : float - Time constant (s)

        Returns:
        --------
        g : array - Conductance time course
        """
        t = np.maximum(t, 0)  # Ensure t >= 0
        return g_max * (t / tau) * np.exp(1 - t / tau)

    @staticmethod
    def double_exp_synapse(t, g_max, tau_rise, tau_decay):
        """
        Double exponential synaptic conductance
        """
        factor = tau_decay / (tau_decay - tau_rise)
        return g_max * factor * (np.exp(-t/tau_decay) - np.exp(-t/tau_rise))

    @staticmethod
    def nmda_voltage_block(V, Mg_out=1.0, K_Mg=3.6, V_half=-17):
        """
        Voltage-dependent Mg²⁺ block of NMDA receptor

        Parameters:
        -----------
        V : float/array - Membrane potential (mV)
        Mg_out : float - External Mg²⁺ concentration (mM)

        Returns:
        --------
        Block factor (0-1)
        """
        return 1.0 / (1.0 + Mg_out/K_Mg * np.exp(-V/V_half))

    @staticmethod
    def quantal_release(n, p):
        """
        Calculate quantal content statistics

        Parameters:
        -----------
        n : int - Number of release sites
        p : float - Release probability

        Returns:
        --------
        dict with mean, variance, CV
        """
        mean = n * p
        variance = n * p * (1 - p)
        cv = np.sqrt(variance) / mean if mean > 0 else np.inf
        return {
            'mean': mean,
            'variance': variance,
            'cv': cv,
            'n': n,
            'p': p
        }

    @staticmethod
    def epsp_amplitude(g_syn, R_in, V_m, E_rev):
        """
        Calculate EPSP amplitude

        Parameters:
        -----------
        g_syn : float - Synaptic conductance (S)
        R_in : float - Input resistance (Ω)
        V_m : float - Membrane potential (V)
        E_rev : float - Reversal potential (V)

        Returns:
        --------
        EPSP amplitude (V)
        """
        return g_syn * R_in * (E_rev - V_m)


class SensoryPhysiology:
    """Models for sensory encoding"""

    @staticmethod
    def weber_fraction(I, delta_I):
        """Weber fraction (just noticeable difference)"""
        return delta_I / I

    @staticmethod
    def fechner_law(I, I_0, k):
        """
        Fechner's logarithmic psychophysical law

        Parameters:
        -----------
        I : array - Stimulus intensity
        I_0 : float - Threshold intensity
        k : float - Scaling constant

        Returns:
        --------
        Perceived magnitude
        """
        return k * np.log(I / I_0)

    @staticmethod
    def stevens_power_law(I, k, n):
        """
        Stevens' power law

        Parameters:
        -----------
        I : array - Stimulus intensity
        k : float - Scaling constant
        n : float - Exponent (modality-dependent)

        Returns:
        --------
        Perceived magnitude
        """
        return k * np.power(I, n)

    @staticmethod
    def receptor_adaptation(t, R_0, R_ss, tau_adapt):
        """
        First-order receptor adaptation

        Parameters:
        -----------
        t : array - Time (s)
        R_0 : float - Initial response
        R_ss : float - Steady-state response
        tau_adapt : float - Adaptation time constant (s)

        Returns:
        --------
        Response amplitude over time
        """
        return R_ss + (R_0 - R_ss) * np.exp(-t / tau_adapt)

    @staticmethod
    def receptive_field_dog(x, y, A_c, sigma_c, A_s, sigma_s):
        """
        Difference of Gaussians receptive field

        Parameters:
        -----------
        x, y : arrays - Spatial coordinates
        A_c : float - Center amplitude
        sigma_c : float - Center width
        A_s : float - Surround amplitude
        sigma_s : float - Surround width

        Returns:
        --------
        Receptive field sensitivity profile
        """
        r2 = x**2 + y**2
        center = A_c * np.exp(-r2 / (2 * sigma_c**2))
        surround = A_s * np.exp(-r2 / (2 * sigma_s**2))
        return center - surround


class MotorControl:
    """Models for motor system physiology"""

    @staticmethod
    def rate_force_relation(f, F_0, k):
        """
        Force vs firing rate

        Parameters:
        -----------
        f : array - Firing frequency (Hz)
        F_0 : float - Maximum force
        k : float - Rate constant

        Returns:
        --------
        Force
        """
        return F_0 * (1 - np.exp(-k * f))

    @staticmethod
    def fusion_frequency(tau_twitch):
        """
        Estimate fusion frequency from twitch time constant

        Parameters:
        -----------
        tau_twitch : float - Twitch duration (s)

        Returns:
        --------
        Fusion frequency (Hz)
        """
        return 3.0 / tau_twitch

    @staticmethod
    def spindle_response(L, L0, dL_dt, k_static, k_dynamic):
        """
        Muscle spindle Ia afferent response

        Parameters:
        -----------
        L : float - Muscle length
        L0 : float - Reference length
        dL_dt : float - Rate of length change
        k_static : float - Static sensitivity
        k_dynamic : float - Dynamic sensitivity

        Returns:
        --------
        Firing rate (Hz)
        """
        return k_static * (L - L0) + k_dynamic * dL_dt

    @staticmethod
    def gto_response(force, k_gto):
        """
        Golgi tendon organ response

        Parameters:
        -----------
        force : float - Muscle force
        k_gto : float - Sensitivity

        Returns:
        --------
        Firing rate (Hz)
        """
        return k_gto * force


class SynapticPlasticity:
    """Models for synaptic plasticity"""

    @staticmethod
    def stdp_weight_change(delta_t, A_plus, A_minus, tau_plus, tau_minus):
        """
        Spike-timing dependent plasticity

        Parameters:
        -----------
        delta_t : float - Time difference (post - pre) in ms
        A_plus : float - LTP amplitude
        A_minus : float - LTD amplitude
        tau_plus : float - LTP time constant (ms)
        tau_minus : float - LTD time constant (ms)

        Returns:
        --------
        Weight change
        """
        if delta_t > 0:
            return A_plus * np.exp(-delta_t / tau_plus)
        else:
            return -A_minus * np.exp(delta_t / tau_minus)

    @staticmethod
    def tsodyks_markram(t_spikes, U, tau_rec, tau_fac, A, dt=0.1):
        """
        Tsodyks-Markram short-term plasticity model

        Parameters:
        -----------
        t_spikes : array - Spike times (ms)
        U : float - Baseline release probability
        tau_rec : float - Recovery time constant (ms)
        tau_fac : float - Facilitation time constant (ms)
        A : float - Absolute synaptic efficacy
        dt : float - Time step (ms)

        Returns:
        --------
        t, x, u, EPSP : time course of resources, release prob, and EPSPs
        """
        t_max = np.max(t_spikes) + 100 if len(t_spikes) > 0 else 100
        t = np.arange(0, t_max, dt)
        x = np.ones_like(t)  # Available resources
        u = np.ones_like(t) * U  # Release probability
        EPSP = np.zeros_like(t)

        spike_indices = (np.array(t_spikes) / dt).astype(int)

        for i in range(1, len(t)):
            # Continuous dynamics
            dx = (1 - x[i-1]) / tau_rec
            du = (U - u[i-1]) / tau_fac

            x[i] = x[i-1] + dx * dt
            u[i] = u[i-1] + du * dt

            # Spike effects
            if i in spike_indices:
                EPSP[i] = A * u[i] * x[i]
                x[i] -= u[i] * x[i]
                u[i] += U * (1 - u[i])

        return t, x, u, EPSP


# Example: Simulate synaptic integration
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Create synaptic input
    t = np.linspace(0, 100, 1000)  # 100 ms

    # AMPA synapse
    g_ampa = SynapticTransmission.alpha_synapse(t - 10, g_max=1e-9, tau=2e-3)

    # NMDA synapse with voltage dependence
    g_nmda = SynapticTransmission.alpha_synapse(t - 10, g_max=0.5e-9, tau=50e-3)
    V_range = np.linspace(-80, 40, 50)
    nmda_block = SynapticTransmission.nmda_voltage_block(V_range)

    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Synaptic conductances
    axes[0, 0].plot(t, g_ampa * 1e9, 'b-', label='AMPA')
    axes[0, 0].plot(t, g_nmda * 1e9, 'r-', label='NMDA')
    axes[0, 0].set_xlabel('Time (ms)')
    axes[0, 0].set_ylabel('Conductance (nS)')
    axes[0, 0].legend()
    axes[0, 0].set_title('Synaptic Conductances')

    # NMDA voltage dependence
    axes[0, 1].plot(V_range, nmda_block)
    axes[0, 1].set_xlabel('Membrane Potential (mV)')
    axes[0, 1].set_ylabel('NMDA Conductance Factor')
    axes[0, 1].set_title('NMDA Mg²⁺ Block')

    # Stevens power law
    I = np.linspace(1, 100, 100)
    for n, label in [(0.33, 'Brightness'), (0.6, 'Loudness'), (1.0, 'Length')]:
        S = SensoryPhysiology.stevens_power_law(I, k=1, n=n)
        axes[1, 0].plot(I, S / S.max(), label=f'{label} (n={n})')
    axes[1, 0].set_xlabel('Stimulus Intensity')
    axes[1, 0].set_ylabel('Perceived Magnitude (normalized)')
    axes[1, 0].legend()
    axes[1, 0].set_title("Stevens' Power Law")

    # STDP curve
    delta_t = np.linspace(-50, 50, 100)
    dw = np.array([SynapticPlasticity.stdp_weight_change(dt, A_plus=1, A_minus=1,
                                                          tau_plus=20, tau_minus=20)
                   for dt in delta_t])
    axes[1, 1].plot(delta_t, dw)
    axes[1, 1].axhline(0, color='k', linestyle='--')
    axes[1, 1].axvline(0, color='k', linestyle='--')
    axes[1, 1].set_xlabel('Δt = t_post - t_pre (ms)')
    axes[1, 1].set_ylabel('Weight Change')
    axes[1, 1].set_title('Spike-Timing Dependent Plasticity')

    plt.tight_layout()
    plt.savefig('nervous_system_models.png', dpi=150)
```

### Julia Implementation

```julia
using DifferentialEquations
using Plots

# Physical constants
const R = 8.314       # J/(mol·K)
const F = 96485       # C/mol
const T = 310         # K (37°C)

"""
    alpha_synapse(t, g_max, τ)

Alpha function synaptic conductance time course.
"""
function alpha_synapse(t, g_max, τ)
    t = max(t, 0.0)
    return g_max * (t / τ) * exp(1 - t / τ)
end

"""
    double_exp_synapse(t, g_max, τ_rise, τ_decay)

Double exponential synaptic conductance.
"""
function double_exp_synapse(t, g_max, τ_rise, τ_decay)
    factor = τ_decay / (τ_decay - τ_rise)
    return g_max * factor * (exp(-t/τ_decay) - exp(-t/τ_rise))
end

"""
    nmda_voltage_block(V; Mg_out=1.0, K_Mg=3.6, V_half=-17)

Voltage-dependent Mg²⁺ block of NMDA receptors.
"""
function nmda_voltage_block(V; Mg_out=1.0, K_Mg=3.6, V_half=-17)
    return 1.0 / (1.0 + Mg_out/K_Mg * exp(-V/V_half))
end

"""
    quantal_analysis(n, p)

Calculate quantal release statistics.
"""
function quantal_analysis(n, p)
    mean = n * p
    variance = n * p * (1 - p)
    cv = sqrt(variance) / mean
    return (mean=mean, variance=variance, cv=cv)
end

"""
    stevens_power_law(I, k, n)

Stevens' power law for psychophysics.
"""
function stevens_power_law(I, k, n)
    return k * I^n
end

"""
    fechner_law(I, I₀, k)

Fechner's logarithmic psychophysical law.
"""
function fechner_law(I, I₀, k)
    return k * log(I / I₀)
end

"""
    receptor_adaptation(t, R₀, R_ss, τ_adapt)

First-order receptor adaptation.
"""
function receptor_adaptation(t, R₀, R_ss, τ_adapt)
    return R_ss + (R₀ - R_ss) * exp(-t / τ_adapt)
end

"""
    receptive_field_dog(x, y, A_c, σ_c, A_s, σ_s)

Difference of Gaussians receptive field.
"""
function receptive_field_dog(x, y, A_c, σ_c, A_s, σ_s)
    r² = x^2 + y^2
    center = A_c * exp(-r² / (2 * σ_c^2))
    surround = A_s * exp(-r² / (2 * σ_s^2))
    return center - surround
end

"""
    spindle_response(L, L₀, dL_dt, k_static, k_dynamic)

Muscle spindle Ia afferent response.
"""
function spindle_response(L, L₀, dL_dt, k_static, k_dynamic)
    return k_static * (L - L₀) + k_dynamic * dL_dt
end

"""
    stdp_weight_change(Δt, A₊, A₋, τ₊, τ₋)

Spike-timing dependent plasticity weight change.
"""
function stdp_weight_change(Δt, A₊, A₋, τ₊, τ₋)
    if Δt > 0
        return A₊ * exp(-Δt / τ₊)
    else
        return -A₋ * exp(Δt / τ₋)
    end
end

"""
Tsodyks-Markram short-term plasticity ODE system.
"""
function tsodyks_markram!(du, u, p, t)
    x, release_u = u
    U, τ_rec, τ_fac = p

    # Continuous dynamics between spikes
    du[1] = (1 - x) / τ_rec       # Resource recovery
    du[2] = (U - release_u) / τ_fac  # Facilitation decay
end

"""
    simulate_short_term_plasticity(spike_times, U, τ_rec, τ_fac, A; dt=0.1)

Simulate Tsodyks-Markram model for given spike train.
"""
function simulate_short_term_plasticity(spike_times, U, τ_rec, τ_fac, A; dt=0.1)
    t_max = maximum(spike_times) + 100

    # Initial conditions
    x = 1.0
    u = U

    t_points = Float64[]
    epsps = Float64[]
    x_vals = Float64[]
    u_vals = Float64[]

    t = 0.0
    spike_idx = 1

    while t < t_max
        push!(t_points, t)
        push!(x_vals, x)
        push!(u_vals, u)

        # Check for spike
        if spike_idx <= length(spike_times) && t >= spike_times[spike_idx]
            epsp = A * u * x
            push!(epsps, epsp)

            # Update after spike
            x -= u * x
            u += U * (1 - u)
            spike_idx += 1
        else
            push!(epsps, 0.0)
        end

        # Continuous dynamics
        dx = (1 - x) / τ_rec * dt
        du = (U - u) / τ_fac * dt
        x += dx
        u += du

        t += dt
    end

    return t_points, x_vals, u_vals, epsps
end

# Example simulations
function run_examples()
    # 1. Synaptic conductance comparison
    t = 0:0.1:100
    g_ampa = [alpha_synapse(ti - 10, 1.0, 2.0) for ti in t]
    g_nmda = [alpha_synapse(ti - 10, 0.5, 50.0) for ti in t]

    p1 = plot(t, g_ampa, label="AMPA (τ=2ms)",
              xlabel="Time (ms)", ylabel="Conductance (norm)")
    plot!(p1, t, g_nmda, label="NMDA (τ=50ms)")

    # 2. NMDA voltage dependence
    V = -80:1:40
    block = [nmda_voltage_block(v) for v in V]

    p2 = plot(V, block, xlabel="Membrane Potential (mV)",
              ylabel="NMDA Conductance Factor", legend=false)

    # 3. Stevens' power law
    I = 1:100
    p3 = plot(xlabel="Stimulus Intensity", ylabel="Perceived Magnitude")
    for (n, name) in [(0.33, "Brightness"), (0.6, "Loudness"), (1.0, "Length")]
        S = [stevens_power_law(i, 1.0, n) for i in I]
        plot!(p3, I, S ./ maximum(S), label="$name (n=$n)")
    end

    # 4. STDP curve
    Δt = -50:1:50
    dw = [stdp_weight_change(dt, 1.0, 1.0, 20.0, 20.0) for dt in Δt]

    p4 = plot(Δt, dw, xlabel="Δt (ms)", ylabel="Weight Change", legend=false)
    hline!(p4, [0], linestyle=:dash, color=:black)
    vline!(p4, [0], linestyle=:dash, color=:black)

    plot(p1, p2, p3, p4, layout=(2,2), size=(800, 600))
    savefig("nervous_system_julia.png")
end
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify the neural process**: Synaptic, sensory, or motor?
2. **Determine temporal/spatial scale**: ms vs s, μm vs mm
3. **Select appropriate model complexity**
4. **Apply relevant equations**
5. **Validate against physiological ranges**

### Typical Problems

**Type 1: Synaptic transmission**
- Given: Conductances, potentials, time constants
- Find: EPSP amplitude, integration, plasticity changes

**Type 2: Sensory encoding**
- Given: Stimulus parameters, receptor properties
- Find: Neural response, perceived magnitude, adaptation

**Type 3: Motor control**
- Given: Muscle properties, stimulation parameters
- Find: Force output, recruitment pattern, reflex responses

**Type 4: Plasticity**
- Given: Spike timing, calcium levels
- Find: Weight changes, learning rules

## Key Relationships Summary

| Process | Equation | Key Parameter |
|---------|----------|---------------|
| EPSP | g_syn × R_in × (E_rev - V_m) | Input resistance |
| Weber fraction | ΔI/I | Modality-dependent |
| Stevens' law | S = k × I^n | Exponent n |
| Rate coding | F = F₀(1-e^(-kf)) | Rate constant k |
| STDP | Δw = A×e^(-\|Δt\|/τ) | Time constant τ |

## Clinical Relevance

### Myasthenia Gravis
- Autoantibodies against nicotinic ACh receptors
- Reduced quantal content (effective n decreases)
- Treatment: Acetylcholinesterase inhibitors

### Parkinson's Disease
- Dopamine depletion in basal ganglia
- Motor initiation impairment
- Treatment: L-DOPA, deep brain stimulation

### Epilepsy
- Imbalance between excitation and inhibition
- Enhanced synchronization
- Treatment: GABAergic drugs, Na⁺ channel blockers

### Alzheimer's Disease
- Cholinergic neuron loss
- Synaptic plasticity impairment
- Treatment: Acetylcholinesterase inhibitors


## Coverage-pass additions (Feher extraction)

8 equation(s) added to this domain, each verified against Feher and a worked example.

### Direction Selectivity Index (`direction_selectivity_index`)
- **Formula:** `DSI = (R_pref - R_null) / (R_pref + R_null)`
- **LaTeX:** `\mathrm{DSI} = \frac{R_{\mathrm{pref}} - R_{\mathrm{null}}}{R_{\mathrm{pref}} + R_{\mathrm{null}}}`
- **Import:** `from scripts.nervous.sensory import direction_selectivity_index` — or `from scripts.canonical_ids import load; load('direction_selectivity_index')`
- **Feher:** §4.10 — SOME RETINAL GANGLION CELLS EXHIBIT DIRECTION OR ORIENTATION SELECTIVITY
- Direction selectivity index quantifies the directional tuning of a motion-selective retinal ganglion cell.

### Orientation Selectivity Index (`orientation_selectivity_index`)
- **Formula:** `OSI = (R_pref + R_null - R_orth+ - R_orth-) / (R_pref + R_null)`
- **LaTeX:** `\mathrm{OSI} = \frac{R_{\mathrm{pref}} + R_{\mathrm{null}} - R_{\mathrm{orth+}} - R_{\mathrm{orth-}}}{R_{\mathrm{pref}} + R_{\mathrm{null}}}`
- **Import:** `from scripts.nervous.sensory import orientation_selectivity_index` — or `from scripts.canonical_ids import load; load('orientation_selectivity_index')`
- **Feher:** §4.10 — SOME RETINAL GANGLION CELLS EXHIBIT DIRECTION OR ORIENTATION SELECTIVITY
- Orientation selectivity index (OSI) of a direction/orientation-selective retinal ganglion cell: contrasts the summed response along the preferred motion axis (preferred + null directions) against the summed response along the orthogonal axis (clockwise + counterclockwise orthogonal), normalized by the preferred-axis response.

### Norwich's Information-Theory Law of Sensation (`norwich_sensation_magnitude`)
- **Formula:** `psi = k * ln(1 + beta * Phi^n)`
- **LaTeX:** `\psi = k \ln(1 + \beta \Phi^{n})`
- **Import:** `from scripts.nervous.sensory import norwich_sensation_magnitude` — or `from scripts.canonical_ids import load; load('norwich_sensation_magnitude')`
- **Feher:** §4.3 — Appendix 4.3.A1 Weber's Law, Fechner's Law, and Steven's Law of Psychophysics
- Norwich's information-theory (entropy) law of sensation magnitude: perceived intensity psi is the logarithm of one plus a power of the stimulus strength Phi.

### Sound Intensity Level (Decibel) (`sound_intensity_level_db`)
- **Formula:** `L_dB = 10 * log10(I_sound / I_ref)`
- **LaTeX:** `L_{\mathrm{dB}} = 10 \, \log_{10}\!\left(\frac{I_{\mathrm{sound}}}{I_{\mathrm{ref}}}\right)`
- **Import:** `from scripts.nervous.hearing import sound_intensity_level_db` — or `from scripts.canonical_ids import load; load('sound_intensity_level_db')`
- **Feher:** §4.7 — THE HUMAN AUDITORY SYSTEM DISCRIMINATES AMONG TONE, TIMBRE, AND INTENSITY
- Sound intensity level (loudness) expressed in decibels: a base-10 logarithmic transform of the ratio of sound intensity to a reference intensity (1e-12 W/m^2 = 0 dB SPL).

### Acoustic Intensity (Sound Intensity) (`acoustic_intensity`)
- **Formula:** `I = dP0^2 / (2 * rho * c)`
- **LaTeX:** `I = \frac{\Delta P_0^{2}}{2 \rho c}`
- **Import:** `from scripts.nervous.hearing import acoustic_intensity` — or `from scripts.canonical_ids import load; load('acoustic_intensity')`
- **Feher:** §4.7 — The Intensity of Sound Is Proportional to the Square of the Pressure
- Acoustic (sound) intensity: power carried per unit area by a sound wave, equal to the square of the pressure amplitude divided by twice the characteristic acoustic impedance rho*c of the medium.

### Snell's Law of Refraction (`snells_law`)
- **Formula:** `n_i * sin(theta_i) = n_r * sin(theta_r)`
- **LaTeX:** `n_{\mathrm{i}} \sin\theta_{\mathrm{i}} = n_{\mathrm{r}} \sin\theta_{\mathrm{r}}`
- **Import:** `from scripts.nervous.vision import snells_law` — or `from scripts.canonical_ids import load; load('snells_law')`
- **Feher:** §4.9 — Appendix 4.9.A1 Refraction of Light and the Thin Lens Formula - The different speeds of light in two media cause refraction, the bending of light at their interface
- Snell's law of refraction relates the angle of incidence to the angle of refraction when light crosses the interface between two media of refractive indices n_i and n_r.

### Thin Lens Formula (`thin_lens_formula`)
- **Formula:** `1/O + 1/I = 1/f`
- **LaTeX:** `\frac{1}{O} + \frac{1}{I} = \frac{1}{f}`
- **Import:** `from scripts.nervous.vision import thin_lens_formula` — or `from scripts.canonical_ids import load; load('thin_lens_formula')`
- **Feher:** §4.9 — THE THIN LENS FORMULA LINKS REFRACTIVE POWER AND IMAGE FORMATION (Appendix 4.9.A1)
- Thin lens formula relating object distance O, image distance I, and focal length f of a thin lens (radii of curvature large compared to lens thickness).

### Refractive Power (Diopters) (`refractive_power_diopters`)
- **Formula:** `D = 1 / f`
- **LaTeX:** `\mathrm{Diopters}\;(D) = \frac{1}{f}`
- **Import:** `from scripts.nervous.vision import refractive_power_diopters` — or `from scripts.canonical_ids import load; load('refractive_power_diopters')`
- **Feher:** §4.9 — The Focal Length Is a Measure of the Refractive Power of a Lens
- Refractive power (dioptric power) of a lens or optical system, D = 1/f, with focal length f in metres and D in diopters (m^-1).


### Coverage pass 2 (residual reconsideration)

**Refractive Index** (`refractive_index`): `n = c / v` — `from scripts.nervous.vision import refractive_index`. Feher §4.9 (Eqn 4.9.A1.1). Refractive index of a medium: the ratio of the speed of light in vacuum to its speed in the medium.


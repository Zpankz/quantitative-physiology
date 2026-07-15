---
name: cardiovascular
description: Cardiovascular system physiology - blood, heart mechanics, ECG, hemodynamics, and vascular regulation
parent: quantitative-physiology
unit: 5
---

# Cardiovascular System Physiology

## Overview

This sub-skill covers the quantitative aspects of cardiovascular function, from blood composition to cardiac mechanics and systemic hemodynamics. It provides the mathematical foundations for understanding circulation as an integrated transport system.

## Core Concepts

### 1. Blood Composition and Properties

#### Blood Volume and Distribution

**Total blood volume**:
```
V_blood ≈ 70 mL/kg body weight ≈ 5 L (70 kg adult)
```

**Distribution**:
| Compartment | % of Blood Volume |
|-------------|------------------|
| Systemic veins | 64% |
| Pulmonary circulation | 9% |
| Heart | 7% |
| Systemic arteries | 13% |
| Capillaries | 7% |

#### Hematocrit and Viscosity

**Hematocrit** (Hct): Volume fraction of red blood cells
Formula → qp:`hematocrit`
Normal: 0.40-0.54 (males), 0.36-0.44 (females)

**Blood viscosity** depends on hematocrit:
Formula → qp:`blood_viscosity`
Where k ≈ 2.5, η_plasma ≈ 1.2 mPa·s

At normal Hct: η_blood ≈ 3-4 mPa·s

**Fåhræus-Lindqvist effect**: Apparent viscosity decreases in small vessels
```
η_apparent = η_plasma × (1 + (η_rel - 1) × f(d/d_c))
```
Where d_c ≈ 6-8 μm (critical diameter)

#### Oxygen Transport

**Oxygen content**:
Formula → qp:`blood_oxygen_content`
Where:
- 1.34 mL O₂/g Hb (Hüfner constant)
- Hb = hemoglobin concentration (g/dL)
- S_O2 = oxygen saturation (0-1)
- 0.003 mL O₂/(dL·mmHg) = solubility

**Hill equation** for hemoglobin saturation:
Formula → qp:`hill_saturation`
Where n ≈ 2.7 (Hill coefficient), P_50 ≈ 26 mmHg

**Oxygen delivery**:
Formula → qp:`systemic_oxygen_delivery`

### 2. Cardiac Electrophysiology

#### Action Potential Phases

**Ventricular AP phases**:
| Phase | Description | Ions | Duration |
|-------|-------------|------|----------|
| 0 | Rapid depolarization | Na⁺ in | 1-2 ms |
| 1 | Early repolarization | K⁺ out, Cl⁻ in | 10-30 ms |
| 2 | Plateau | Ca²⁺ in, K⁺ out | 150-200 ms |
| 3 | Repolarization | K⁺ out | 100-150 ms |
| 4 | Resting | K⁺ leak | - |

Total APD ≈ 200-400 ms (rate-dependent)

#### Pacemaker Activity

**Sinoatrial node automaticity**:
- Phase 4 depolarization: I_f (funny current) + I_CaT
- Intrinsic rate: 60-100 bpm

**Funny current** (HCN channels):
Formula → qp:`funny_current` (I_f); with HCN gating (no object):
```
dy/dt = (y_∞ - y) / τ_y
y_∞ = 1 / (1 + exp((V_m - V_half)/k))
```

**Rate dependence on autonomic tone**:
Formula → qp:`heart_rate_autonomic`

#### ECG Interpretation

**ECG intervals**:
| Interval | Normal Range | Represents |
|----------|-------------|------------|
| PR | 120-200 ms | AV conduction |
| QRS | 80-120 ms | Ventricular depolarization |
| QT | 350-440 ms | Ventricular APD |
| QTc | <450 ms (men), <460 ms (women) | Rate-corrected QT |

**Bazett's correction**:
Formula → qp:`qtc_bazett`

**Fridericia correction** (more accurate at extreme rates):
Formula → qp:`qtc_fridericia`

**Lead vectors and axis**:
```
Net QRS vector angle from standard leads:
tan(θ) = (aVL - aVR) / I
```
Normal axis: -30° to +90°

### 3. Cardiac Mechanics

#### Frank-Starling Mechanism

**Length-tension relationship**:
```
F = F_max × f(SL)
```
Optimal sarcomere length: 2.0-2.2 μm

**Starling's Law**:
```
SV ∝ EDV - ESV
SV = f(preload, afterload, contractility)
```

**Preload-recruitable stroke work**:
```
PRSW = SW / EDV
SW = ∫ P dV (stroke work)
```

#### Pressure-Volume Loops

**Key points on PV loop**:
1. End-diastolic point (EDV, EDP)
2. Isovolumetric contraction (volume constant, pressure rises)
3. Ejection (pressure falls, volume decreases)
4. End-systolic point (ESV, ESP)
5. Isovolumetric relaxation (volume constant, pressure falls)
6. Filling (pressure low, volume increases)

**End-systolic pressure-volume relationship (ESPVR)**:
Formula → qp:`espvr`
Where E_es = end-systolic elastance (index of contractility)

**End-diastolic pressure-volume relationship (EDPVR)**:
Formula → qp:`edpvr`
Exponential relationship reflecting chamber stiffness

#### Cardiac Output

**Cardiac output**:
Formula → qp:`cardiac_output`

**Fick principle**:
Formula → qp:`cardiac_output_fick`

**Ejection fraction**:
Formula → qp:`ejection_fraction`
Normal: 55-70%

**Cardiac index**:
Formula → qp:`cardiac_index`
Normal: 2.5-4.0 L/min/m²

**Body surface area** (Du Bois):
Formula → qp:`body_surface_area_dubois`
(W in kg, H in cm)

#### Ventricular Energetics

**Pressure-volume area (PVA)**:
```
PVA = PE + SW
```
Where PE = potential energy, SW = stroke work

**Myocardial oxygen consumption**:
```
MVO₂ = a × PVA + b × E_es + c × HR + d
```
Linear relationship with PVA

### 4. Hemodynamics

#### Fundamental Relationships

**Hydraulic resistance**:
Formula → qp:`poiseuille_resistance`

**Vascular resistance units**:
- PRU (peripheral resistance unit): mmHg/(mL/min)
- Wood units: mmHg/(L/min)
- dyn·s/cm⁵ = 80 × Wood units

**Total peripheral resistance (TPR)**:
Formula → qp:`total_peripheral_resistance`

**Mean arterial pressure**:
Formula → qp:`mean_arterial_pressure`
More precisely:
```
MAP = (1/T) × ∫₀ᵀ P(t) dt
```

#### Vascular Compliance

**Compliance definition**:
Formula → qp:`vascular_compliance`

**Arterial compliance** decreases with age and disease

**Windkessel model**:
```
P = Q × R (steady state)
C × dP/dt = Q_in - P/R (dynamic)
```

**Time constant**:
Formula → qp:`windkessel_time_constant`
Arterial system: τ ≈ 1.5-2 s

#### Pulse Wave Velocity

**Moens-Korteweg equation**:
Formula → qp:`moens_korteweg_pwv`
Where:
- E = elastic modulus of vessel wall
- h = wall thickness
- d = vessel diameter
- ρ = blood density

**Bramwell-Hill equation**:
Formula → qp:`bramwell_hill_pwv`

Normal aortic PWV: 4-6 m/s (young), 8-12 m/s (elderly)

#### Flow Profiles

**Reynolds number**:
Formula → qp:`reynolds_number_blood`
Turbulence threshold: Re > 2000

**Womersley number** (pulsatile flow):
Formula → qp:`womersley_number`

For α > 10: Flat velocity profile (plug flow)
For α < 1: Parabolic profile (Poiseuille)

### 5. Microcirculation

#### Capillary Exchange

**Starling equation**:
Formula → qp:`starling_filtration`
Where:
- J_v = fluid flux (mL/min)
- L_p = hydraulic conductivity
- S = surface area
- σ = reflection coefficient
- P_c, P_i = capillary, interstitial hydrostatic pressure
- π_c, π_i = capillary, interstitial oncotic pressure

**Net filtration pressure**:
Formula → qp:`net_filtration_pressure`

Typical values:
- Arterial end: NFP ≈ +10 mmHg (filtration)
- Venous end: NFP ≈ -7 mmHg (reabsorption)

#### Transcapillary Solute Exchange

**Fick's Law for diffusion**:
Formula → qp:`ficks_law_diffusion`

**Permeability-surface area product (PS)**:
Formula → qp:`ps_product`
Where E = extraction ratio

**Krogh cylinder model** for oxygen:
```
r_tissue = √(Q × C_O2 / (π × L × M))
```
Where M = metabolic rate

### 6. Vascular Regulation

#### Autoregulation

**Myogenic response**:
```
Pressure ↑ → Stretch → Depolarization → Ca²⁺ influx → Constriction
```

**Metabolic regulation**:
```
Flow ∝ Metabolism / [O₂]
```

Vasodilator metabolites: adenosine, CO₂, H⁺, K⁺

**Flow-mediated dilation**:
- Mechanism: Shear stress → NO release → Vasodilation
- Wall shear stress: Formula → qp:`wall_shear_stress`

#### Neurohumoral Control

**Sympathetic vasoconstriction**:
```
R = R_0 × (1 + α × [NE])
```

**Baroreceptor sensitivity**:
Formula → qp:`baroreceptor_sensitivity`
Normal: 10-20 ms/mmHg

## Computational Models

### Python Implementation

```python
import numpy as np
from scipy.integrate import odeint, solve_ivp
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# Physical constants
RHO_BLOOD = 1060  # kg/m³

class BloodProperties:
    """Blood composition and properties"""

    @staticmethod
    def hematocrit_viscosity(hct, eta_plasma=1.2):
        """
        Blood viscosity as function of hematocrit

        Parameters:
        -----------
        hct : float - Hematocrit (0-1)
        eta_plasma : float - Plasma viscosity (mPa·s)

        Returns:
        --------
        eta_blood : float - Blood viscosity (mPa·s)
        """
        return eta_plasma * np.exp(2.5 * hct)

    @staticmethod
    def oxygen_content(Hb, SO2, PO2):
        """
        Blood oxygen content

        Parameters:
        -----------
        Hb : float - Hemoglobin (g/dL)
        SO2 : float - Oxygen saturation (0-1)
        PO2 : float - Partial pressure O2 (mmHg)

        Returns:
        --------
        CaO2 : float - O2 content (mL O2/dL blood)
        """
        bound = 1.34 * Hb * SO2
        dissolved = 0.003 * PO2
        return bound + dissolved

    @staticmethod
    def hill_saturation(PO2, P50=26, n=2.7):
        """
        Hemoglobin oxygen saturation (Hill equation)

        Parameters:
        -----------
        PO2 : float/array - Oxygen partial pressure (mmHg)
        P50 : float - Half-saturation pressure (mmHg)
        n : float - Hill coefficient

        Returns:
        --------
        SO2 : float/array - Saturation (0-1)
        """
        return PO2**n / (P50**n + PO2**n)

    @staticmethod
    def oxygen_delivery(CO, Hb, SO2):
        """
        Oxygen delivery rate

        Parameters:
        -----------
        CO : float - Cardiac output (L/min)
        Hb : float - Hemoglobin (g/dL)
        SO2 : float - Saturation (0-1)

        Returns:
        --------
        DO2 : float - O2 delivery (mL/min)
        """
        CaO2 = 1.34 * Hb * SO2  # mL O2/dL
        return CO * CaO2 * 10  # Convert to mL/min


class CardiacMechanics:
    """Cardiac mechanics and hemodynamics"""

    @staticmethod
    def cardiac_output(hr, sv):
        """CO = HR × SV"""
        return hr * sv / 1000  # L/min if SV in mL

    @staticmethod
    def ejection_fraction(edv, esv):
        """EF = (EDV - ESV) / EDV"""
        return (edv - esv) / edv

    @staticmethod
    def mean_arterial_pressure(sbp, dbp):
        """MAP = DBP + (1/3)(SBP - DBP)"""
        return dbp + (sbp - dbp) / 3

    @staticmethod
    def total_peripheral_resistance(map_mmhg, co_lpm, cvp=0):
        """TPR = (MAP - CVP) / CO in Wood units"""
        return (map_mmhg - cvp) / co_lpm

    @staticmethod
    def body_surface_area(weight_kg, height_cm):
        """Du Bois formula for BSA (m²)"""
        return 0.007184 * weight_kg**0.425 * height_cm**0.725

    @staticmethod
    def cardiac_index(co, bsa):
        """CI = CO / BSA"""
        return co / bsa

    @staticmethod
    def qtc_bazett(qt_ms, rr_s):
        """Bazett's QTc correction"""
        return qt_ms / np.sqrt(rr_s)

    @staticmethod
    def qtc_fridericia(qt_ms, rr_s):
        """Fridericia's QTc correction"""
        return qt_ms / np.cbrt(rr_s)


class PVLoop:
    """Pressure-volume loop analysis"""

    def __init__(self, Ees=2.5, V0=10, Ea=2.0, Ped0=5, k_ed=0.02):
        """
        Initialize PV loop parameters

        Parameters:
        -----------
        Ees : float - End-systolic elastance (mmHg/mL)
        V0 : float - Volume intercept (mL)
        Ea : float - Arterial elastance (mmHg/mL)
        Ped0 : float - EDPVR offset (mmHg)
        k_ed : float - EDPVR stiffness constant
        """
        self.Ees = Ees
        self.V0 = V0
        self.Ea = Ea
        self.Ped0 = Ped0
        self.k_ed = k_ed

    def espvr(self, V):
        """End-systolic pressure-volume relationship"""
        return self.Ees * (V - self.V0)

    def edpvr(self, V):
        """End-diastolic pressure-volume relationship"""
        return self.Ped0 * (np.exp(self.k_ed * V) - 1)

    def operating_point(self, EDV):
        """
        Find ESV and pressures for given EDV

        Returns:
        --------
        dict with EDV, ESV, EDP, ESP, SV, EF, SW
        """
        EDP = self.edpvr(EDV)

        # ESV from intersection of ESPVR and arterial elastance
        # ESP = Ees(ESV - V0) = Ea(EDV - ESV)
        ESV = (self.Ea * EDV + self.Ees * self.V0) / (self.Ees + self.Ea)
        ESP = self.espvr(ESV)

        SV = EDV - ESV
        EF = SV / EDV

        # Stroke work (approximate as rectangle)
        SW = ESP * SV  # mmHg·mL = 0.00133 J

        return {
            'EDV': EDV, 'ESV': ESV, 'EDP': EDP, 'ESP': ESP,
            'SV': SV, 'EF': EF, 'SW': SW
        }

    def generate_loop(self, EDV, n_points=100):
        """
        Generate points for PV loop visualization

        Returns:
        --------
        V, P arrays for plotting
        """
        op = self.operating_point(EDV)
        ESV, EDV = op['ESV'], op['EDV']
        EDP, ESP = op['EDP'], op['ESP']

        V, P = [], []

        # 1. Filling (EDV previous to current EDV along EDPVR)
        v_fill = np.linspace(ESV, EDV, n_points//4)
        p_fill = self.edpvr(v_fill)
        V.extend(v_fill)
        P.extend(p_fill)

        # 2. Isovolumetric contraction
        p_ivc = np.linspace(EDP, ESP, n_points//4)
        v_ivc = np.ones_like(p_ivc) * EDV
        V.extend(v_ivc)
        P.extend(p_ivc)

        # 3. Ejection (along ESPVR approximately)
        v_eject = np.linspace(EDV, ESV, n_points//4)
        # Linear approximation from (EDV, ESP) to (ESV, ESP_final)
        p_eject = np.linspace(ESP, self.espvr(ESV), n_points//4)
        V.extend(v_eject)
        P.extend(p_eject)

        # 4. Isovolumetric relaxation
        ESP_final = self.espvr(ESV)
        EDP_next = self.edpvr(ESV)
        p_ivr = np.linspace(ESP_final, EDP_next, n_points//4)
        v_ivr = np.ones_like(p_ivr) * ESV
        V.extend(v_ivr)
        P.extend(p_ivr)

        return np.array(V), np.array(P)


class Windkessel:
    """Arterial windkessel model"""

    @staticmethod
    def two_element(t, Q, R, C, P0=80):
        """
        2-element Windkessel: C dP/dt + P/R = Q

        Parameters:
        -----------
        t : array - Time points (s)
        Q : array - Flow input (mL/s)
        R : float - Resistance (mmHg·s/mL)
        C : float - Compliance (mL/mmHg)
        P0 : float - Initial pressure (mmHg)

        Returns:
        --------
        P : array - Pressure time course (mmHg)
        """
        def dPdt(P, t_val, Q_func, R, C):
            Q_val = Q_func(t_val)
            return (Q_val - P/R) / C

        from scipy.interpolate import interp1d
        Q_interp = interp1d(t, Q, fill_value=0, bounds_error=False)

        P = odeint(dPdt, P0, t, args=(Q_interp, R, C))
        return P.flatten()

    @staticmethod
    def pulse_wave_velocity(E, h, d, rho=1060):
        """
        Moens-Korteweg PWV

        Parameters:
        -----------
        E : float - Elastic modulus (Pa)
        h : float - Wall thickness (m)
        d : float - Vessel diameter (m)
        rho : float - Blood density (kg/m³)

        Returns:
        --------
        PWV : float - Pulse wave velocity (m/s)
        """
        return np.sqrt(E * h / (rho * d))


class Microcirculation:
    """Capillary exchange and microvascular function"""

    @staticmethod
    def starling_filtration(Lp, S, Pc, Pi, pi_c, pi_i, sigma=1.0):
        """
        Starling equation for fluid flux

        Parameters:
        -----------
        Lp : float - Hydraulic conductivity (mL/(min·mmHg·cm²))
        S : float - Surface area (cm²)
        Pc : float - Capillary hydrostatic pressure (mmHg)
        Pi : float - Interstitial hydrostatic pressure (mmHg)
        pi_c : float - Capillary oncotic pressure (mmHg)
        pi_i : float - Interstitial oncotic pressure (mmHg)
        sigma : float - Reflection coefficient (0-1)

        Returns:
        --------
        Jv : float - Fluid flux (mL/min), positive = filtration
        """
        return Lp * S * ((Pc - Pi) - sigma * (pi_c - pi_i))

    @staticmethod
    def net_filtration_pressure(Pc, Pi, pi_c, pi_i, sigma=1.0):
        """Calculate net filtration pressure"""
        return (Pc - Pi) - sigma * (pi_c - pi_i)

    @staticmethod
    def extraction_ratio_to_ps(Q, E):
        """
        Convert extraction ratio to permeability-surface area product

        Parameters:
        -----------
        Q : float - Flow rate
        E : float - Extraction ratio (0-1)

        Returns:
        --------
        PS : float - Permeability-surface area product
        """
        return -Q * np.log(1 - E)


# Example simulations
if __name__ == "__main__":
    # 1. Oxygen dissociation curve
    PO2 = np.linspace(0, 100, 100)
    SO2 = BloodProperties.hill_saturation(PO2)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    axes[0, 0].plot(PO2, SO2 * 100)
    axes[0, 0].axhline(50, linestyle='--', color='gray')
    axes[0, 0].axvline(26, linestyle='--', color='gray')
    axes[0, 0].set_xlabel('PO₂ (mmHg)')
    axes[0, 0].set_ylabel('Saturation (%)')
    axes[0, 0].set_title('Oxygen Dissociation Curve')

    # 2. Viscosity vs hematocrit
    hct = np.linspace(0.2, 0.7, 50)
    eta = BloodProperties.hematocrit_viscosity(hct)

    axes[0, 1].plot(hct * 100, eta)
    axes[0, 1].axvline(45, linestyle='--', color='red', label='Normal Hct')
    axes[0, 1].set_xlabel('Hematocrit (%)')
    axes[0, 1].set_ylabel('Viscosity (mPa·s)')
    axes[0, 1].set_title('Blood Viscosity')
    axes[0, 1].legend()

    # 3. PV Loop
    pv = PVLoop(Ees=2.5, V0=10, Ea=2.0)
    V, P = pv.generate_loop(EDV=120)

    # Also show ESPVR and EDPVR
    V_range = np.linspace(10, 150, 100)
    axes[1, 0].plot(V, P, 'b-', linewidth=2, label='PV Loop')
    axes[1, 0].plot(V_range, pv.espvr(V_range), 'r--', label='ESPVR')
    axes[1, 0].plot(V_range, pv.edpvr(V_range), 'g--', label='EDPVR')
    axes[1, 0].set_xlabel('Volume (mL)')
    axes[1, 0].set_ylabel('Pressure (mmHg)')
    axes[1, 0].set_title('Pressure-Volume Loop')
    axes[1, 0].legend()
    axes[1, 0].set_xlim([0, 160])
    axes[1, 0].set_ylim([0, 150])

    # 4. Starling forces along capillary
    x = np.linspace(0, 1, 100)  # Position along capillary
    Pc = 35 - 20 * x  # Pressure drops from 35 to 15 mmHg
    Pi = -2  # Interstitial pressure
    pi_c = 25  # Plasma oncotic pressure
    pi_i = 5   # Interstitial oncotic pressure

    NFP = Microcirculation.net_filtration_pressure(Pc, Pi, pi_c, pi_i)

    axes[1, 1].plot(x * 100, NFP)
    axes[1, 1].axhline(0, color='k', linestyle='-')
    axes[1, 1].fill_between(x * 100, NFP, where=NFP > 0, alpha=0.3, color='blue',
                             label='Filtration')
    axes[1, 1].fill_between(x * 100, NFP, where=NFP < 0, alpha=0.3, color='red',
                             label='Reabsorption')
    axes[1, 1].set_xlabel('Position along capillary (%)')
    axes[1, 1].set_ylabel('Net Filtration Pressure (mmHg)')
    axes[1, 1].set_title('Starling Forces')
    axes[1, 1].legend()

    plt.tight_layout()
    plt.savefig('cardiovascular_models.png', dpi=150)
```

### Julia Implementation

```julia
using DifferentialEquations
using Plots

const RHO_BLOOD = 1060.0  # kg/m³

"""
Blood viscosity as function of hematocrit.
"""
function blood_viscosity(hct; η_plasma=1.2)
    return η_plasma * exp(2.5 * hct)
end

"""
Hill equation for hemoglobin saturation.
"""
function hill_saturation(PO2; P50=26.0, n=2.7)
    return PO2^n / (P50^n + PO2^n)
end

"""
Blood oxygen content (mL O₂/dL).
"""
function oxygen_content(Hb, SO2, PO2)
    bound = 1.34 * Hb * SO2
    dissolved = 0.003 * PO2
    return bound + dissolved
end

"""
Cardiac output (L/min).
"""
function cardiac_output(hr, sv_ml)
    return hr * sv_ml / 1000
end

"""
Ejection fraction.
"""
function ejection_fraction(edv, esv)
    return (edv - esv) / edv
end

"""
Mean arterial pressure.
"""
function mean_arterial_pressure(sbp, dbp)
    return dbp + (sbp - dbp) / 3
end

"""
Total peripheral resistance (Wood units).
"""
function total_peripheral_resistance(map_mmhg, co_lpm; cvp=0)
    return (map_mmhg - cvp) / co_lpm
end

"""
Body surface area (Du Bois formula).
"""
function body_surface_area(weight_kg, height_cm)
    return 0.007184 * weight_kg^0.425 * height_cm^0.725
end

"""
Bazett's QTc correction.
"""
function qtc_bazett(qt_ms, rr_s)
    return qt_ms / sqrt(rr_s)
end

"""
Moens-Korteweg pulse wave velocity.
"""
function pulse_wave_velocity(E, h, d; ρ=1060.0)
    return sqrt(E * h / (ρ * d))
end

"""
Starling filtration equation.
"""
function starling_filtration(Lp, S, Pc, Pi, πc, πi; σ=1.0)
    return Lp * S * ((Pc - Pi) - σ * (πc - πi))
end

"""
PV Loop structure for cardiac mechanics.
"""
struct PVLoop
    Ees::Float64   # End-systolic elastance
    V0::Float64    # Volume intercept
    Ea::Float64    # Arterial elastance
    Ped0::Float64  # EDPVR offset
    k_ed::Float64  # EDPVR stiffness
end

function espvr(pv::PVLoop, V)
    return pv.Ees * (V - pv.V0)
end

function edpvr(pv::PVLoop, V)
    return pv.Ped0 * (exp(pv.k_ed * V) - 1)
end

function operating_point(pv::PVLoop, EDV)
    EDP = edpvr(pv, EDV)
    ESV = (pv.Ea * EDV + pv.Ees * pv.V0) / (pv.Ees + pv.Ea)
    ESP = espvr(pv, ESV)
    SV = EDV - ESV
    EF = SV / EDV
    SW = ESP * SV

    return (EDV=EDV, ESV=ESV, EDP=EDP, ESP=ESP, SV=SV, EF=EF, SW=SW)
end

"""
2-element Windkessel model ODE.
"""
function windkessel!(dP, P, params, t)
    R, C, Q_func = params
    Q = Q_func(t)
    dP[1] = (Q - P[1]/R) / C
end

"""
Simulate Windkessel model.
"""
function simulate_windkessel(t_span, Q_func, R, C, P0)
    prob = ODEProblem(windkessel!, [P0], t_span, (R, C, Q_func))
    sol = solve(prob, Tsit5())
    return sol
end

# Example plots
function run_cv_examples()
    # 1. Oxygen dissociation curve
    PO2 = 0:1:100
    SO2 = [hill_saturation(p) * 100 for p in PO2]

    p1 = plot(PO2, SO2, xlabel="PO₂ (mmHg)", ylabel="Saturation (%)",
              title="O₂ Dissociation Curve", legend=false)
    hline!(p1, [50], linestyle=:dash, color=:gray)
    vline!(p1, [26], linestyle=:dash, color=:gray)

    # 2. Viscosity
    hct = 0.2:0.01:0.7
    η = [blood_viscosity(h) for h in hct]

    p2 = plot(hct .* 100, η, xlabel="Hematocrit (%)", ylabel="Viscosity (mPa·s)",
              title="Blood Viscosity", legend=false)
    vline!(p2, [45], linestyle=:dash, color=:red)

    # 3. PV Loop
    pv = PVLoop(2.5, 10.0, 2.0, 5.0, 0.02)
    V_range = 10:1:150

    espvr_line = [espvr(pv, v) for v in V_range]
    edpvr_line = [edpvr(pv, v) for v in V_range]

    p3 = plot(V_range, espvr_line, label="ESPVR", linestyle=:dash,
              xlabel="Volume (mL)", ylabel="Pressure (mmHg)",
              title="Pressure-Volume Relationships")
    plot!(p3, V_range, edpvr_line, label="EDPVR", linestyle=:dash)

    # 4. Starling forces
    x = 0:0.01:1
    Pc = 35 .- 20 .* x
    Pi = -2.0
    πc = 25.0
    πi = 5.0

    NFP = (Pc .- Pi) .- (πc - πi)

    p4 = plot(x .* 100, NFP, xlabel="Position (%)", ylabel="NFP (mmHg)",
              title="Starling Forces", legend=false)
    hline!(p4, [0], color=:black)

    plot(p1, p2, p3, p4, layout=(2, 2), size=(800, 600))
    savefig("cardiovascular_julia.png")
end
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify the cardiovascular subsystem**: Blood, heart, vessels, microcirculation?
2. **Define known hemodynamic variables**: Pressures, flows, volumes
3. **Select appropriate model**: Steady-state, dynamic, distributed
4. **Apply conservation laws**: Mass (flow continuity), energy (pressure-flow)
5. **Validate against normal ranges**

### Typical Problems

**Type 1: Cardiac function**
- Given: Volumes, pressures, heart rate
- Find: CO, EF, work, power

**Type 2: Hemodynamics**
- Given: MAP, CO, vessel dimensions
- Find: TPR, flow distribution, wall stress

**Type 3: Oxygen transport**
- Given: Hb, PO₂, cardiac output
- Find: O₂ delivery, extraction, reserve

**Type 4: Microvascular exchange**
- Given: Starling forces
- Find: Filtration rate, edema formation

## Key Relationships Summary

| Parameter | Equation | Normal Value |
|-----------|----------|--------------|
| Cardiac output | HR × SV | 5 L/min |
| Ejection fraction | (EDV-ESV)/EDV | 55-70% |
| MAP | DBP + PP/3 | 70-105 mmHg |
| TPR | MAP/CO | 15-20 Wood units |
| O₂ content | 1.34×Hb×SO₂ | 20 mL/dL |
| PWV | √(Eh/ρd) | 4-10 m/s |

## Clinical Correlations

### Heart Failure
- Reduced EF (<40%): Systolic HF
- Preserved EF (>50%): Diastolic HF
- Elevated filling pressures: Congestion

### Hypertension
- Elevated TPR
- Increased arterial stiffness (PWV ↑)
- Cardiac remodeling (wall thickening)

### Anemia
- Reduced O₂ carrying capacity
- Compensatory ↑CO, ↑HR
- Tissue hypoxia at low Hb

### Edema
- Elevated capillary pressure (Pc ↑)
- Reduced oncotic pressure (πc ↓)
- Increased permeability (Lp ↑)
- Lymphatic obstruction


## Coverage-pass additions (Feher extraction)

11 equation(s) added to this domain, each verified against Feher and a worked example.

### Cardiac Output (Indicator Dilution / Stewart-Hamilton) (`indicator_dilution_cardiac_output`)
- **Formula:** `CO = m / integral(C_m dt)`
- **LaTeX:** `Q_{\mathrm{a}} = \dfrac{m}{\int_0^t C_{\mathrm{m}}\,\mathrm{d}t}`
- **Import:** `from scripts.cardiovascular.cardiac import indicator_dilution_cardiac_output` — or `from scripts.canonical_ids import load; load('indicator_dilution_cardiac_output')`
- **Feher:** §5.10 — CARDIAC OUTPUT CAN BE DETERMINED BY THE INDICATOR DILUTION METHOD
- Stewart-Hamilton indicator dilution method for measuring cardiac output: a known amount m of indicator is injected into a vein and its concentration C_m is recorded over time in arterial blood; cardiac output equals m divided by the area under the concentration-time curve.

### Colloid Osmotic (Oncotic) Pressure (`colloid_osmotic_pressure`)
- **Formula:** `pi = a*C + b*C^2 + c*C^3  (albumin: a=2.8, b=0.18, c=0.012; globulin: a=1.6, b=0.15, c=0.006); pi in mmHg, C in g/dL`
- **LaTeX:** `\pi_{\mathrm{albumin}} = 2.8C + 0.18C^2 + 0.012C^3; \quad \pi_{\mathrm{globulin}} = 1.6C + 0.15C^2 + 0.006C^3`
- **Import:** `from scripts.cardiovascular.microcirculation import colloid_osmotic_pressure` — or `from scripts.canonical_ids import load; load('colloid_osmotic_pressure')`
- **Feher:** §5.12 — IN MOST TISSUES, NET FILTRATION PRESSURE DRIVES FLUID OUT OF THE CAPILLARIES AT THE ARTERIOLAR END
- Colloid osmotic (oncotic) pressure of plasma/interstitial proteins as an empirical cubic polynomial in protein MASS concentration (Landis-Pappenheimer relation).

### Capillary Pressure (Hydraulic Voltage Divider) (`capillary_pressure`)
- **Formula:** `P_C = P_A*[R_V/(R_A+R_V)] + P_V*[R_A/(R_A+R_V)]`
- **LaTeX:** `P_C = P_A \left[\dfrac{R_V}{R_A + R_V}\right] + P_V \left[\dfrac{R_A}{R_A + R_V}\right]`
- **Import:** `from scripts.cardiovascular.microcirculation import capillary_pressure` — or `from scripts.canonical_ids import load; load('capillary_pressure')`
- **Feher:** §5.13 — VASOCONSTRICTION DECREASES CAPILLARY PRESSURE
- Capillary hydrostatic pressure modelled as a two-resistor hydraulic voltage divider between arteriolar (precapillary) and venule (postcapillary) pressures, weighted by their resistances.

### Systemic Vascular Compliance (`systemic_vascular_compliance`)
- **Formula:** `C_S = C_A + C_V`
- **LaTeX:** `C_{\mathrm{S}} = C_{\mathrm{A}} + C_{\mathrm{V}}`
- **Import:** `from scripts.cardiovascular.hemodynamics import systemic_vascular_compliance` — or `from scripts.canonical_ids import load; load('systemic_vascular_compliance')`
- **Feher:** §5.14 — Filling the Empty Circulatory System Reveals Stressed and Unstressed Volumes
- Total systemic vascular compliance equals the sum of the arterial and venous compartment compliances.

### Vascular Function Curve (Venous Return) (`vascular_function_curve`)
- **Formula:** `Q_veins = -((1 + C_V/C_A)/TPR)*(P_RA - P_MS)`
- **LaTeX:** `Q_{\mathrm{veins}} = -\dfrac{\left[1 + C_{\mathrm{V}}/C_{\mathrm{A}}\right]}{\mathrm{TPR}}\left[P_{\mathrm{RA}} - P_{\mathrm{MS}}\right]`
- **Import:** `from scripts.cardiovascular.hemodynamics import vascular_function_curve` — or `from scripts.canonical_ids import load; load('vascular_function_curve')`
- **Feher:** §5.14 — THE VASCULAR FUNCTION CURVE CAN BE DERIVED FROM ARTERIAL AND VENOUS COMPLIANCES AND TPR
- Guyton/Levy vascular (venous return) function curve: expresses systemic venous return flow as a linear function of right atrial pressure.

### Mean Cell Volume (MCV) (`mean_cell_volume`)
- **Formula:** `MCV = Hct_ratio / n_rbc   (result x 1e15 to give fL/cell)`
- **LaTeX:** `\mathrm{MCV} = \frac{\mathrm{Hct\ ratio}}{n}`
- **Import:** `from scripts.cardiovascular.blood import mean_cell_volume` — or `from scripts.canonical_ids import load; load('mean_cell_volume')`
- **Feher:** §5.2 — EXAMPLE 5.2.1 Calculate the Mean Cell Volume
- Mean cell volume: the average volume of a single red blood cell, obtained by dividing the hematocrit ratio by the red-cell numerical density.

### Mean Corpuscular Hemoglobin Concentration (`mean_corpuscular_hemoglobin_concentration`)
- **Formula:** `MCHC = Hb_blood / Hct`
- **LaTeX:** `\mathrm{MCHC} = \frac{[\mathrm{Hb}]_{\text{whole blood}}}{\mathrm{Hct}}`
- **Import:** `from scripts.cardiovascular.blood import mean_corpuscular_hemoglobin_concentration` — or `from scripts.canonical_ids import load; load('mean_corpuscular_hemoglobin_concentration')`
- **Feher:** §5.2 — EXAMPLE 5.2.2 Calculate the Mean Corpuscular Hemoglobin Concentration and HB Content
- Mean corpuscular hemoglobin concentration: the average hemoglobin concentration within packed red cells, obtained by dividing whole-blood hemoglobin concentration by the hematocrit.

### Plasma Buffer Capacity (van Slyke) (`plasma_buffer_capacity`)
- **Formula:** `beta = delta_acid / delta_pH`
- **LaTeX:** `\beta = \dfrac{\Delta\,\text{acid}}{\Delta\,\text{pH}}`
- **Import:** `from scripts.cardiovascular.blood import plasma_buffer_capacity` — or `from scripts.canonical_ids import load; load('plasma_buffer_capacity')`
- **Feher:** §5.2 — PLASMA PROTEINS AND IONS BUFFER CHANGES IN PLASMA PH
- Buffer capacity (van Slyke buffer value) of plasma: the amount of strong acid (or base) needed to change plasma pH by one unit.

### Mean Corpuscular Hemoglobin (`mean_corpuscular_hemoglobin`)
- **Formula:** `MCH = [Hb]_whole_blood / n`
- **LaTeX:** `\mathrm{MCH} = \frac{[\mathrm{Hb}]_{\text{whole blood}}}{n}`
- **Import:** `from scripts.cardiovascular.blood import mean_corpuscular_hemoglobin` — or `from scripts.canonical_ids import load; load('mean_corpuscular_hemoglobin')`
- **Feher:** §5.2 — EXAMPLE 5.2.2 Calculate the Mean Corpuscular Hemoglobin Concentration and HB Content
- Mean corpuscular hemoglobin (MCH): the average mass of hemoglobin per red blood cell, calculated as the whole-blood hemoglobin concentration divided by the red-cell numerical density.

### Transferrin Saturation (`transferrin_saturation`)
- **Formula:** `TSAT = serum_iron / TIBC * 100`
- **LaTeX:** `\mathrm{TSAT} = \dfrac{\text{serum iron}}{\mathrm{TIBC}} \times 100`
- **Import:** `from scripts.cardiovascular.blood import transferrin_saturation` — or `from scripts.canonical_ids import load; load('transferrin_saturation')`
- **Feher:** §5.2 — TRANSFERRIN CARRIES FERRIC IRON IN THE PLASMA
- Transferrin saturation (TSAT): the percentage of transferrin iron-binding sites occupied by iron, computed as serum iron divided by total iron-binding capacity (TIBC), times 100.

### Stroke Volume (`stroke_volume`)
- **Formula:** `SV = EDV - ESV`
- **LaTeX:** `\mathrm{SV} = \mathrm{EDV} - \mathrm{ESV}`
- **Import:** `from scripts.cardiovascular.cardiac import stroke_volume` — or `from scripts.canonical_ids import load; load('stroke_volume')`
- **Feher:** §5.6 — Ejection Phase (Summary of the Events in the Cardiac Cycle)
- Stroke volume: the volume of blood ejected from the ventricle with each heartbeat, computed as the difference between end-diastolic and end-systolic volume.


### Coverage pass 2 (residual reconsideration)

**Einthoven's Law (limb leads)** (`einthoven_lead_relation`): `lead_II = lead_I + lead_III` — `from scripts.cardiovascular.ecg import einthoven_lead_relation`. Feher §5.8 (Eqn 5.8.3). Einthoven's law: with the standard bipolar limb-lead definitions and sign convention, the three limb-lead voltages satisfy II = I + III at every instant (Kirchhoff's voltage law around the Einthoven triangle).



## Review additions (2026-07-15)

- **coronary_perfusion_pressure** — `CPP = DBP - LVEDP` — Diastolic coronary supply pressure; falls with diastolic hypotension, high LVEDP, AS, tachycardia. Import: `from scripts.cardiovascular.hemodynamics import coronary_perfusion_pressure_equation` (or `load("coronary_perfusion_pressure")`).
- **stroke_work** — `SW = MAP x SV` — External work per beat (PV-loop area approximation); basis for PVA and efficiency. Import: `from scripts.cardiovascular.hemodynamics import stroke_work_equation` (or `load("stroke_work")`).

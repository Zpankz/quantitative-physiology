---
name: respiratory
description: Respiratory physiology - ventilation mechanics, gas exchange, oxygen/CO2 transport, respiratory control, and acid-base balance
parent: quantitative-physiology
unit: 6
---

# Respiratory Physiology

## Overview

This sub-skill covers the quantitative aspects of respiratory physiology, including the mechanics of breathing, gas exchange in the lungs, transport of oxygen and carbon dioxide in blood, control of ventilation, and acid-base balance. The respiratory system's primary function is to maintain arterial blood gas homeostasis through regulated gas exchange.

## Core Concepts

### 1. Lung Volumes and Capacities

#### Static Lung Volumes

**Tidal Volume (VT)**: Volume of air inhaled/exhaled per breath
```
VT ≈ 500 mL (resting)
```

**Inspiratory Reserve Volume (IRV)**: Additional volume above VT
```
IRV ≈ 3000 mL
```

**Expiratory Reserve Volume (ERV)**: Additional volume below VT
```
ERV ≈ 1100 mL
```

**Residual Volume (RV)**: Volume remaining after maximal expiration
```
RV ≈ 1200 mL
```

#### Lung Capacities (combinations)

**Total Lung Capacity**:
Formula → qp:`total_lung_capacity`

**Vital Capacity**:
Formula → qp:`vital_capacity`

**Functional Residual Capacity**:
Formula → qp:`functional_residual_capacity`

**Inspiratory Capacity**:
Formula → qp:`inspiratory_capacity`

#### Minute Ventilation

**Total minute ventilation**:
Formula → qp:`minute_ventilation`
Where f = respiratory frequency (breaths/min)

**Alveolar ventilation** (effective gas exchange):
Formula → qp:`alveolar_ventilation`
Where VD = dead space volume (~150 mL anatomical)

### 2. Mechanics of Breathing

#### Pressure Relationships

**Transmural pressure** (across lung wall):
Formula → qp:`transmural_pressure`
Where:
- P_alv = alveolar pressure
- P_pl = pleural pressure

**Transpulmonary pressure** drives lung expansion:
```
P_tp = P_alv - P_pl
```

At FRC (no flow): P_alv = 0, P_pl ≈ -5 cmH₂O → P_tp = +5 cmH₂O

#### Compliance

**Definition** (change in volume per unit pressure):
Formula → qp:`compliance`

**Lung compliance**:
```
C_L ≈ 0.2 L/cmH₂O
```

**Chest wall compliance**:
```
C_CW ≈ 0.2 L/cmH₂O
```

**Total respiratory system compliance** (series):
```
1/C_RS = 1/C_L + 1/C_CW
C_RS ≈ 0.1 L/cmH₂O
```

#### Elastance (inverse of compliance)

Formula → qp:`elastance`

**Total elastance** (series):
Formula → qp:`total_elastance`

#### Surface Tension and Surfactant

**Law of Laplace for sphere**:
Formula → qp:`laplace_pressure`

**Surfactant reduces surface tension**:
- Pure water: T ≈ 70 mN/m
- With surfactant: T ≈ 25 mN/m (varies with area)

**Surfactant composition**: ~90% lipids (DPPC), ~10% proteins (SP-A, SP-B, SP-C, SP-D)

**Hysteresis**: Inspiration requires more pressure than expiration (surfactant spreading)

#### Airway Resistance

**Poiseuille's law** for airway flow:
Formula → qp:`airway_resistance`

**Pressure-flow relationship**:
Formula → qp:`pressure_flow`

**Total airway resistance**:
```
R_aw ≈ 1-2 cmH₂O/(L/s)
```

**Key insight**: Most resistance in medium bronchi (generations 4-8), not smallest airways

**Reynolds number** determines flow pattern:
Formula → qp:`reynolds_number_airway`
- Re < 2000: Laminar flow
- Re > 2000: Turbulent flow (upper airways, bifurcations)

#### Time Constant

**Exponential filling/emptying**:
Formula → qp:`respiratory_time_constant`

**Volume change during expiration**:
Formula → qp:`exponential_emptying`

**Clinical**: τ_normal ≈ 0.5 s; 3τ ≈ 95% complete

### 3. Gas Exchange

#### Partial Pressures

**Dalton's Law**:
```
P_total = P₁ + P₂ + P₃ + ...
P_i = F_i × P_total
```

**Atmospheric composition** (dry, sea level):
```
P_O2 = 0.21 × 760 = 159.6 mmHg
P_N2 = 0.78 × 760 = 593 mmHg
P_CO2 = 0.0004 × 760 ≈ 0.3 mmHg
```

**Water vapor pressure** at 37°C:
```
P_H2O = 47 mmHg
```

**Inspired gas** (humidified):
```
P_iO2 = 0.21 × (760 - 47) = 150 mmHg
```

#### Alveolar Gas Equation

**Simplified form**:
Formula → qp:`alveolar_gas_equation`
Where R = respiratory exchange ratio ≈ 0.8

**Full form**:
```
P_AO2 = F_iO2 × (P_B - P_H2O) - P_ACO2 × (F_iO2 + (1-F_iO2)/R)
```

**Normal values**:
```
P_AO2 ≈ 100 mmHg
P_ACO2 ≈ 40 mmHg
```

**A-a gradient**:
```
A-a gradient = P_AO2 - P_aO2
Normal: 5-15 mmHg (increases with age)
```

#### Diffusion of Gases

**Fick's law for gas diffusion**:
```
V̇_gas = D_L × A × (P₁ - P₂) / T
```

**Diffusing capacity** (combines terms):
Formula → qp:`diffusing_capacity`

**Oxygen diffusing capacity**:
```
D_LO2 ≈ 21 mL/(min·mmHg) at rest
D_LO2 ≈ 65 mL/(min·mmHg) during exercise
```

**CO diffusing capacity** (clinical measurement):
```
D_LCO ≈ 25 mL/(min·mmHg)
D_LO2 ≈ 1.23 × D_LCO
```

**Conductance model** (resistance in series):
Formula → qp:`diffusion_conductance`
Where:
- D_M = membrane diffusing capacity
- θ = reaction rate of gas with Hb
- V_c = pulmonary capillary blood volume

**Transit time**: Blood spends ~0.75 s in pulmonary capillary (equilibration by ~0.25 s)

#### Diffusion vs Perfusion Limitation

**Diffusion-limited**: Gas equilibration incomplete (CO, O₂ at altitude)
**Perfusion-limited**: Gas equilibration complete (N₂O, O₂ at rest)

### 4. Ventilation-Perfusion Relationships

#### V/Q Ratio

**Definition**:
```
V̇A/Q̇ ratio
```

**Ideal matching**:
```
V̇A/Q̇ ≈ 0.8-1.0
```

**Regional variation** (upright lung):
- Apex: V̇A/Q̇ ≈ 3 (high V, low Q)
- Base: V̇A/Q̇ ≈ 0.6 (low V, high Q)

#### Shunt and Dead Space

**Shunt** (V̇A/Q̇ = 0):
Formula → qp:`shunt_equation`
Normal physiological shunt: 2-5%

**Dead space** (V̇A/Q̇ = ∞):
Formula → qp:`dead_space_bohr`
Bohr equation. Normal V_D/V_T ≈ 0.3

#### O₂-CO₂ Diagram

**V̇A/Q̇ line** connects:
- V̇A/Q̇ = 0: Mixed venous point (P_vO2 ≈ 40, P_vCO2 ≈ 46)
- V̇A/Q̇ = ∞: Inspired gas point (P_iO2 ≈ 150, P_iCO2 ≈ 0)

**Hypoxic pulmonary vasoconstriction (HPV)**: Local mechanism to improve V/Q matching

### 5. Oxygen Transport

#### Oxygen Content

**Total oxygen content**:
Formula → qp:`respiratory_oxygen_content`
Where:
- 1.34 = Hüfner constant (mL O₂/g Hb)
- [Hb] = hemoglobin concentration (g/dL)
- S_O2 = oxygen saturation (0-1)
- 0.003 = solubility coefficient (mL O₂/dL/mmHg)

**Normal arterial**: C_aO2 ≈ 20 mL O₂/dL
**Normal venous**: C_vO2 ≈ 15 mL O₂/dL
**a-v difference**: 5 mL O₂/dL (increases with exercise)

#### Oxygen-Hemoglobin Dissociation Curve

**Hill equation**:
Formula → qp:`hill_equation`
Where:
- P_50 ≈ 26.6 mmHg (PO2 at 50% saturation)
- n ≈ 2.7 (Hill coefficient, cooperativity)

**Key points on curve**:
- P_O2 = 100 mmHg → S_O2 ≈ 97%
- P_O2 = 60 mmHg → S_O2 ≈ 90% (steep decline below)
- P_O2 = 40 mmHg → S_O2 ≈ 75%
- P_O2 = 27 mmHg → S_O2 ≈ 50% (P50)

**Factors shifting curve** (Bohr effect):

Right shift (↓ affinity, ↑ P50):
- ↑ PCO2 (Bohr effect)
- ↓ pH
- ↑ Temperature
- ↑ 2,3-DPG

Left shift (↑ affinity, ↓ P50):
- ↓ PCO2
- ↑ pH
- ↓ Temperature
- ↓ 2,3-DPG
- Fetal Hb (HbF)
- CO poisoning

#### Oxygen Delivery

**Oxygen delivery**:
Formula → qp:`tissue_oxygen_delivery`
Where Q̇ = cardiac output (L/min)

**Normal**: D_O2 ≈ 1000 mL O₂/min

**Oxygen consumption** (Fick principle):
Formula → qp:`oxygen_consumption_fick`

**Normal**: V̇O2 ≈ 250 mL O₂/min (rest)

**Oxygen extraction ratio**:
Formula → qp:`oxygen_extraction_ratio`

### 6. Carbon Dioxide Transport

#### Forms of CO2 in Blood

**Dissolved CO2**:
```
[CO2]_dissolved = α × P_CO2
α = 0.03 mL CO₂/(dL·mmHg)
```
Represents ~5% of total CO2

**Bicarbonate** (major form, ~90%):
```
CO2 + H2O ⇌ H2CO3 ⇌ H⁺ + HCO3⁻
```
Catalyzed by carbonic anhydrase (CA)

**Carbamino compounds** (~5%):
```
CO2 + R-NH2 ⇌ R-NH-COO⁻ + H⁺
```
Primarily with deoxygenated Hb

#### Haldane Effect

Deoxygenated blood carries more CO2 at same PCO2:
- Enhanced carbamino formation
- Better H⁺ buffering by deoxy-Hb

**CO2 content difference**:
```
C_vCO2 - C_aCO2 ≈ 4 mL CO₂/dL
```

#### CO2 Dissociation Curve

**Near-linear** in physiological range (40-46 mmHg)

**Chloride shift**: HCO3⁻ exits RBC in exchange for Cl⁻

### 7. Control of Ventilation

#### Central Control

**Respiratory centers**:
- Medullary respiratory group (DRG, VRG)
- Pontine respiratory group (pneumotaxic, apneustic)

**Respiratory rhythm**: Generated in pre-Bötzinger complex

#### Chemoreceptors

**Central chemoreceptors** (medulla):
- Respond to [H⁺] in CSF (ultimately PCO2)
- CSF has low buffering capacity
- Account for ~80% of CO2 response

**CO2 response equation**:
Formula → qp:`co2_response`
Where S = CO2 sensitivity ≈ 2-3 L/min/mmHg

**Peripheral chemoreceptors** (carotid body):
- Respond to P_aO2, P_aCO2, pH
- Rapid response (<1 s)
- Type I (glomus) cells sense hypoxia

**O2 response** (hypoxic ventilatory response):
Formula → qp:`hypoxic_response`
Hyperbolic increase below P_aO2 ≈ 60 mmHg

#### Integrated Response

**CO2-O2 interaction**: Hypoxia potentiates CO2 response

**Altitude acclimatization**:
1. Immediate: Hypoxic ventilatory response
2. Hours-days: CSF pH adjustment
3. Days-weeks: Increased EPO, Hb

**Exercise response**:
- Phase I: Immediate (neural, anticipatory)
- Phase II: Exponential rise (metabolic factors)
- Phase III: Steady state

**Exercise hyperpnea**: V̇E increases linearly with V̇CO2 until anaerobic threshold

### 8. Acid-Base Balance

#### Henderson-Hasselbalch Equation

Formula → qp:`henderson_hasselbalch`

**Normal values**:
- pH = 7.40 (7.35-7.45)
- P_aCO2 = 40 mmHg (35-45)
- [HCO3⁻] = 24 mEq/L (22-26)

#### Primary Disorders

**Respiratory acidosis** (↑ PCO2):
- Acute: pH ↓ 0.08 per 10 mmHg ↑ PCO2
- Chronic: HCO3⁻ rises 3.5 mEq/L per 10 mmHg ↑ PCO2

**Respiratory alkalosis** (↓ PCO2):
- Acute: pH ↑ 0.08 per 10 mmHg ↓ PCO2
- Chronic: HCO3⁻ falls 5 mEq/L per 10 mmHg ↓ PCO2

**Metabolic acidosis** (↓ HCO3⁻):
- Respiratory compensation: PCO2 = 1.5 × [HCO3⁻] + 8 (Winter's formula)

**Metabolic alkalosis** (↑ HCO3⁻):
- Respiratory compensation: PCO2 = 0.7 × [HCO3⁻] + 21

#### Anion Gap

```
AG = [Na⁺] - [Cl⁻] - [HCO3⁻]
Normal: 8-12 mEq/L
```

**Elevated AG acidosis**: Lactic acidosis, ketoacidosis, uremia, toxins (MUDPILES)

#### Buffer Systems

**Bicarbonate buffer** (most important in blood):
```
CO2 + H2O ⇌ H2CO3 ⇌ H⁺ + HCO3⁻
```

**Hemoglobin buffer** (major intracellular):
```
Hb-H ⇌ Hb⁻ + H⁺
```

**Phosphate buffer** (important intracellularly and in urine):
```
H2PO4⁻ ⇌ HPO4²⁻ + H⁺
```

**Protein buffers**: Imidazole groups of histidine

## Computational Models

### Python Implementation

```python
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import fsolve

# Physical constants
R = 8.314  # J/(mol·K)

class LungVolumes:
    """Static and dynamic lung volume calculations"""

    # Typical adult values (mL)
    VT = 500      # Tidal volume
    IRV = 3000    # Inspiratory reserve
    ERV = 1100    # Expiratory reserve
    RV = 1200     # Residual volume
    VD = 150      # Anatomical dead space

    @classmethod
    def total_lung_capacity(cls):
        """TLC = VT + IRV + ERV + RV"""
        return cls.VT + cls.IRV + cls.ERV + cls.RV

    @classmethod
    def vital_capacity(cls):
        """VC = VT + IRV + ERV"""
        return cls.VT + cls.IRV + cls.ERV

    @classmethod
    def functional_residual_capacity(cls):
        """FRC = ERV + RV"""
        return cls.ERV + cls.RV

    @staticmethod
    def minute_ventilation(VT, f):
        """Total minute ventilation (mL/min)"""
        return VT * f

    @staticmethod
    def alveolar_ventilation(VT, VD, f):
        """Effective alveolar ventilation (mL/min)"""
        return (VT - VD) * f


class RespiratoryMechanics:
    """Lung mechanics calculations"""

    @staticmethod
    def compliance(delta_V, delta_P):
        """
        Compliance = ΔV/ΔP

        Parameters:
        -----------
        delta_V : float - Volume change (L)
        delta_P : float - Pressure change (cmH2O)

        Returns:
        --------
        C : float - Compliance (L/cmH2O)
        """
        return delta_V / delta_P

    @staticmethod
    def total_compliance(C_L, C_CW):
        """
        Series compliance of lung and chest wall
        1/C_total = 1/C_L + 1/C_CW
        """
        return 1 / (1/C_L + 1/C_CW)

    @staticmethod
    def elastance(C):
        """Elastance = 1/Compliance"""
        return 1 / C

    @staticmethod
    def airway_resistance(eta, L, r):
        """
        Poiseuille resistance: R = 8ηL/(πr⁴)

        Parameters:
        -----------
        eta : float - Viscosity (Pa·s)
        L : float - Length (m)
        r : float - Radius (m)

        Returns:
        --------
        R : float - Resistance (Pa·s/m³)
        """
        return (8 * eta * L) / (np.pi * r**4)

    @staticmethod
    def time_constant(R, C):
        """τ = R × C"""
        return R * C

    @staticmethod
    def exponential_emptying(V0, t, tau):
        """Volume during passive expiration"""
        return V0 * np.exp(-t / tau)

    @staticmethod
    def laplace_pressure(T, r):
        """Transmural pressure in sphere: ΔP = 2T/r"""
        return 2 * T / r


class GasExchange:
    """Gas exchange and partial pressure calculations"""

    @staticmethod
    def partial_pressure(F, P_total):
        """Dalton's law: P_i = F_i × P_total"""
        return F * P_total

    @staticmethod
    def inspired_PO2(FiO2, P_B=760, P_H2O=47):
        """
        Inspired PO2 (humidified)

        Parameters:
        -----------
        FiO2 : float - Fraction of inspired O2 (0-1)
        P_B : float - Barometric pressure (mmHg)
        P_H2O : float - Water vapor pressure (mmHg)
        """
        return FiO2 * (P_B - P_H2O)

    @staticmethod
    def alveolar_gas_equation(FiO2, P_B, P_H2O, PACO2, R=0.8):
        """
        Alveolar gas equation (simplified)
        PAO2 = PiO2 - PACO2/R

        Parameters:
        -----------
        FiO2 : float - Fraction inspired O2
        P_B : float - Barometric pressure (mmHg)
        P_H2O : float - Water vapor pressure (mmHg)
        PACO2 : float - Alveolar PCO2 (mmHg)
        R : float - Respiratory exchange ratio

        Returns:
        --------
        PAO2 : float - Alveolar PO2 (mmHg)
        """
        PiO2 = FiO2 * (P_B - P_H2O)
        return PiO2 - PACO2 / R

    @staticmethod
    def Aa_gradient(PAO2, PaO2):
        """Alveolar-arterial O2 gradient"""
        return PAO2 - PaO2

    @staticmethod
    def diffusing_capacity(V_gas, P_A, P_c):
        """
        DL = V̇_gas / (PA - Pc)
        """
        return V_gas / (P_A - P_c)

    @staticmethod
    def shunt_fraction(CcO2, CaO2, CvO2):
        """
        Shunt equation: Qs/Qt = (CcO2 - CaO2)/(CcO2 - CvO2)
        """
        return (CcO2 - CaO2) / (CcO2 - CvO2)

    @staticmethod
    def dead_space_fraction(PaCO2, PECO2):
        """
        Bohr equation: VD/VT = (PaCO2 - PECO2)/PaCO2
        """
        return (PaCO2 - PECO2) / PaCO2


class OxygenTransport:
    """Oxygen content and transport calculations"""

    @staticmethod
    def oxygen_content(Hb, SO2, PO2):
        """
        Total O2 content: CaO2 = (1.34 × Hb × SO2) + (0.003 × PO2)

        Parameters:
        -----------
        Hb : float - Hemoglobin concentration (g/dL)
        SO2 : float - Oxygen saturation (0-1)
        PO2 : float - Partial pressure of O2 (mmHg)

        Returns:
        --------
        CO2 : float - O2 content (mL O2/dL)
        """
        return (1.34 * Hb * SO2) + (0.003 * PO2)

    @staticmethod
    def hill_saturation(PO2, P50=26.6, n=2.7):
        """
        Hill equation for O2-Hb dissociation
        SO2 = PO2^n / (P50^n + PO2^n)

        Parameters:
        -----------
        PO2 : float or array - Partial pressure O2 (mmHg)
        P50 : float - PO2 at 50% saturation (mmHg)
        n : float - Hill coefficient

        Returns:
        --------
        SO2 : float or array - Saturation (0-1)
        """
        return PO2**n / (P50**n + PO2**n)

    @staticmethod
    def P50_shift(P50_standard, delta_pH=0, delta_T=0, delta_DPG=0):
        """
        Estimate P50 shift from standard conditions

        Approximate changes:
        - pH: ΔP50 ≈ -0.48 × ΔpH × P50 (Bohr effect)
        - Temperature: ~6% per °C
        - 2,3-DPG: ~3% per mM change
        """
        # Bohr effect
        bohr_factor = 10**(-0.48 * delta_pH)
        # Temperature effect
        temp_factor = 1.06**delta_T
        # DPG effect (simplified)
        dpg_factor = 1 + 0.03 * delta_DPG

        return P50_standard * bohr_factor * temp_factor * dpg_factor

    @staticmethod
    def oxygen_delivery(CO, CaO2):
        """
        DO2 = CO × CaO2 × 10

        Parameters:
        -----------
        CO : float - Cardiac output (L/min)
        CaO2 : float - Arterial O2 content (mL/dL)

        Returns:
        --------
        DO2 : float - O2 delivery (mL/min)
        """
        return CO * CaO2 * 10

    @staticmethod
    def oxygen_consumption(CO, CaO2, CvO2):
        """
        VO2 = CO × (CaO2 - CvO2) × 10
        """
        return CO * (CaO2 - CvO2) * 10

    @staticmethod
    def extraction_ratio(CaO2, CvO2):
        """O2 extraction ratio"""
        return (CaO2 - CvO2) / CaO2


class CO2Transport:
    """CO2 transport calculations"""

    @staticmethod
    def dissolved_CO2(PCO2, alpha=0.03):
        """
        Dissolved CO2 content
        alpha = 0.03 mL CO2/(dL·mmHg)
        """
        return alpha * PCO2

    @staticmethod
    def total_CO2_content(PCO2, HCO3, alpha=0.03):
        """
        Approximate total CO2 content
        Primarily HCO3 + dissolved
        """
        dissolved = alpha * PCO2
        # Convert HCO3 (mEq/L) to mL CO2/dL (simplified)
        from_bicarb = HCO3 * 2.24 / 10  # rough conversion
        return dissolved + from_bicarb


class VentilatoryControl:
    """Ventilatory control models"""

    @staticmethod
    def CO2_response(PaCO2, VE0=5, S=2.5, threshold=40):
        """
        CO2 ventilatory response
        VE = VE0 + S × (PaCO2 - threshold)

        Parameters:
        -----------
        PaCO2 : float - Arterial PCO2 (mmHg)
        VE0 : float - Baseline ventilation (L/min)
        S : float - CO2 sensitivity (L/min/mmHg)
        threshold : float - Apneic threshold (mmHg)

        Returns:
        --------
        VE : float - Minute ventilation (L/min)
        """
        VE = VE0 + S * (PaCO2 - threshold)
        return max(0, VE)  # Can't have negative ventilation

    @staticmethod
    def hypoxic_response(PaO2, VE0=5, A=30, B=30):
        """
        Hypoxic ventilatory response (hyperbolic)
        VE = VE0 × (1 + A/(PaO2 - B))

        Parameters:
        -----------
        PaO2 : float - Arterial PO2 (mmHg)
        VE0 : float - Normoxic baseline ventilation
        A : float - Hypoxic sensitivity parameter
        B : float - Asymptote (typically ~30 mmHg)
        """
        if PaO2 <= B:
            return np.inf  # Undefined below asymptote
        return VE0 * (1 + A / (PaO2 - B))

    @staticmethod
    def combined_response(PaO2, PaCO2, VE0=5, S_CO2=2.5, A_O2=30):
        """
        Combined CO2-O2 ventilatory response
        Hypoxia potentiates CO2 response
        """
        # CO2 drive
        CO2_drive = S_CO2 * max(0, PaCO2 - 40)

        # O2 modulation (increases CO2 sensitivity in hypoxia)
        if PaO2 > 60:
            O2_factor = 1.0
        else:
            O2_factor = 1 + A_O2 / (PaO2 - 30)

        return VE0 + CO2_drive * O2_factor


class AcidBase:
    """Acid-base calculations"""

    @staticmethod
    def henderson_hasselbalch(HCO3, PCO2, pKa=6.1, alpha=0.03):
        """
        Henderson-Hasselbalch equation
        pH = pKa + log([HCO3]/(alpha × PCO2))

        Parameters:
        -----------
        HCO3 : float - Bicarbonate concentration (mEq/L)
        PCO2 : float - Partial pressure CO2 (mmHg)
        pKa : float - pKa of carbonic acid (6.1)
        alpha : float - CO2 solubility

        Returns:
        --------
        pH : float
        """
        return pKa + np.log10(HCO3 / (alpha * PCO2))

    @staticmethod
    def PCO2_from_pH_HCO3(pH, HCO3, pKa=6.1, alpha=0.03):
        """Calculate PCO2 from pH and HCO3"""
        return HCO3 / (alpha * 10**(pH - pKa))

    @staticmethod
    def HCO3_from_pH_PCO2(pH, PCO2, pKa=6.1, alpha=0.03):
        """Calculate HCO3 from pH and PCO2"""
        return alpha * PCO2 * 10**(pH - pKa)

    @staticmethod
    def anion_gap(Na, Cl, HCO3):
        """
        Anion gap = [Na+] - [Cl-] - [HCO3-]
        Normal: 8-12 mEq/L
        """
        return Na - Cl - HCO3

    @staticmethod
    def winters_formula(HCO3):
        """
        Expected PCO2 in metabolic acidosis
        PCO2 = 1.5 × [HCO3] + 8 (± 2)
        """
        return 1.5 * HCO3 + 8

    @staticmethod
    def respiratory_compensation_metabolic_alkalosis(HCO3):
        """
        Expected PCO2 in metabolic alkalosis
        PCO2 = 0.7 × [HCO3] + 21
        """
        return 0.7 * HCO3 + 21

    @staticmethod
    def acute_respiratory_pH_change(delta_PCO2):
        """
        Acute respiratory: ΔpH = 0.008 × ΔPCO2
        """
        return -0.008 * delta_PCO2

    @staticmethod
    def chronic_respiratory_HCO3_change(delta_PCO2, is_acidosis=True):
        """
        Chronic respiratory compensation
        Acidosis: ↑HCO3 3.5 mEq/L per 10 mmHg ↑PCO2
        Alkalosis: ↓HCO3 5 mEq/L per 10 mmHg ↓PCO2
        """
        if is_acidosis:
            return 3.5 * delta_PCO2 / 10
        else:
            return -5 * delta_PCO2 / 10


# Simulation example
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # O2-Hb dissociation curve
    PO2 = np.linspace(0, 120, 200)
    SO2_normal = OxygenTransport.hill_saturation(PO2)

    # Right shift (acidosis, fever)
    P50_shifted = OxygenTransport.P50_shift(26.6, delta_pH=-0.1, delta_T=2)
    SO2_shifted = OxygenTransport.hill_saturation(PO2, P50=P50_shifted)

    plt.figure(figsize=(10, 6))
    plt.plot(PO2, SO2_normal * 100, 'b-', linewidth=2, label='Normal (P50=26.6)')
    plt.plot(PO2, SO2_shifted * 100, 'r--', linewidth=2,
             label=f'Right shift (P50={P50_shifted:.1f})')
    plt.axhline(50, color='gray', linestyle=':', alpha=0.5)
    plt.axvline(26.6, color='b', linestyle=':', alpha=0.5)
    plt.axvline(P50_shifted, color='r', linestyle=':', alpha=0.5)
    plt.xlabel('PO2 (mmHg)')
    plt.ylabel('Oxygen Saturation (%)')
    plt.title('Oxygen-Hemoglobin Dissociation Curve')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 120)
    plt.ylim(0, 105)
    plt.savefig('oxyhb_dissociation.png', dpi=150)
```

### Julia Implementation

```julia
using DifferentialEquations
using Plots

# ============================================
# Respiratory Physiology Module
# ============================================

module RespiratoryPhysiology

export LungVolumes, RespiratoryMechanics, GasExchange
export OxygenTransport, CO2Transport, VentilatoryControl, AcidBase

"""
Lung volume calculations
"""
module LungVolumes
    const VT = 500.0      # Tidal volume (mL)
    const IRV = 3000.0    # Inspiratory reserve (mL)
    const ERV = 1100.0    # Expiratory reserve (mL)
    const RV = 1200.0     # Residual volume (mL)
    const VD = 150.0      # Dead space (mL)

    TLC() = VT + IRV + ERV + RV
    VC() = VT + IRV + ERV
    FRC() = ERV + RV
    IC() = VT + IRV

    minute_ventilation(VT, f) = VT * f
    alveolar_ventilation(VT, VD, f) = (VT - VD) * f
end

"""
Respiratory mechanics calculations
"""
module RespiratoryMechanics
    compliance(ΔV, ΔP) = ΔV / ΔP
    total_compliance(C_L, C_CW) = 1 / (1/C_L + 1/C_CW)
    elastance(C) = 1 / C

    airway_resistance(η, L, r) = (8 * η * L) / (π * r^4)
    time_constant(R, C) = R * C

    exponential_emptying(V₀, t, τ) = V₀ * exp(-t / τ)
    laplace_pressure(T, r) = 2 * T / r
end

"""
Gas exchange calculations
"""
module GasExchange
    partial_pressure(F, P_total) = F * P_total

    function inspired_PO2(FiO2; P_B=760.0, P_H2O=47.0)
        return FiO2 * (P_B - P_H2O)
    end

    function alveolar_gas_equation(FiO2, PACO2; P_B=760.0, P_H2O=47.0, R=0.8)
        PiO2 = FiO2 * (P_B - P_H2O)
        return PiO2 - PACO2 / R
    end

    Aa_gradient(PAO2, PaO2) = PAO2 - PaO2
    diffusing_capacity(V_gas, P_A, P_c) = V_gas / (P_A - P_c)
    shunt_fraction(CcO2, CaO2, CvO2) = (CcO2 - CaO2) / (CcO2 - CvO2)
    dead_space_fraction(PaCO2, PECO2) = (PaCO2 - PECO2) / PaCO2
end

"""
Oxygen transport calculations
"""
module OxygenTransport
    function oxygen_content(Hb, SO2, PO2)
        return (1.34 * Hb * SO2) + (0.003 * PO2)
    end

    function hill_saturation(PO2; P50=26.6, n=2.7)
        return PO2^n / (P50^n + PO2^n)
    end

    function P50_shift(P50_standard; delta_pH=0.0, delta_T=0.0, delta_DPG=0.0)
        bohr_factor = 10^(-0.48 * delta_pH)
        temp_factor = 1.06^delta_T
        dpg_factor = 1 + 0.03 * delta_DPG
        return P50_standard * bohr_factor * temp_factor * dpg_factor
    end

    oxygen_delivery(CO, CaO2) = CO * CaO2 * 10
    oxygen_consumption(CO, CaO2, CvO2) = CO * (CaO2 - CvO2) * 10
    extraction_ratio(CaO2, CvO2) = (CaO2 - CvO2) / CaO2
end

"""
Ventilatory control models
"""
module VentilatoryControl
    function CO2_response(PaCO2; VE0=5.0, S=2.5, threshold=40.0)
        VE = VE0 + S * (PaCO2 - threshold)
        return max(0.0, VE)
    end

    function hypoxic_response(PaO2; VE0=5.0, A=30.0, B=30.0)
        PaO2 <= B && return Inf
        return VE0 * (1 + A / (PaO2 - B))
    end

    function combined_response(PaO2, PaCO2; VE0=5.0, S_CO2=2.5, A_O2=30.0)
        CO2_drive = S_CO2 * max(0.0, PaCO2 - 40.0)
        O2_factor = PaO2 > 60.0 ? 1.0 : (1 + A_O2 / (PaO2 - 30.0))
        return VE0 + CO2_drive * O2_factor
    end
end

"""
Acid-base calculations
"""
module AcidBase
    function henderson_hasselbalch(HCO3, PCO2; pKa=6.1, α=0.03)
        return pKa + log10(HCO3 / (α * PCO2))
    end

    function PCO2_from_pH_HCO3(pH, HCO3; pKa=6.1, α=0.03)
        return HCO3 / (α * 10^(pH - pKa))
    end

    function HCO3_from_pH_PCO2(pH, PCO2; pKa=6.1, α=0.03)
        return α * PCO2 * 10^(pH - pKa)
    end

    anion_gap(Na, Cl, HCO3) = Na - Cl - HCO3
    winters_formula(HCO3) = 1.5 * HCO3 + 8
    respiratory_compensation_alkalosis(HCO3) = 0.7 * HCO3 + 21
    acute_respiratory_pH_change(ΔPCO2) = -0.008 * ΔPCO2

    function chronic_respiratory_HCO3_change(ΔPCO2; acidosis=true)
        return acidosis ? 3.5 * ΔPCO2 / 10 : -5 * ΔPCO2 / 10
    end
end

end  # module RespiratoryPhysiology


# ============================================
# Dynamic Models
# ============================================

"""
Single compartment lung model
dV/dt = (P_mus + P_vent - V/C) / R

Parameters:
- C: compliance (L/cmH2O)
- R: resistance (cmH2O·s/L)
"""
function lung_single_compartment!(du, u, p, t)
    V = u[1]
    C, R, P_mus_func = p

    P_mus = P_mus_func(t)  # Muscle pressure (negative for inspiration)
    P_elastic = V / C       # Elastic recoil

    # Flow = (driving pressure) / resistance
    du[1] = (P_mus - P_elastic) / R
end

"""
Simulate breathing cycle
"""
function simulate_breathing(;
    C = 0.1,           # L/cmH2O
    R = 2.0,           # cmH2O·s/L
    P_max = -5.0,      # cmH2O (inspiratory pressure)
    Ti = 1.5,          # Inspiratory time (s)
    Te = 2.5,          # Expiratory time (s)
    n_breaths = 3
)
    T_total = Ti + Te

    # Muscle pressure function (sinusoidal inspiration)
    function P_mus(t)
        t_cycle = mod(t, T_total)
        if t_cycle < Ti
            return P_max * sin(π * t_cycle / Ti)
        else
            return 0.0
        end
    end

    # Initial condition
    FRC = 2.3  # L (functional residual capacity)
    u0 = [FRC]

    # Parameters
    p = (C, R, P_mus)

    # Solve
    tspan = (0.0, n_breaths * T_total)
    prob = ODEProblem(lung_single_compartment!, u0, tspan, p)
    sol = solve(prob, Tsit5(), saveat=0.01)

    return sol
end

"""
O2-CO2 exchange model
Simplified alveolar gas exchange dynamics
"""
function alveolar_gas_exchange!(du, u, p, t)
    PAO2, PACO2 = u
    VA, Q, PvO2, PvCO2, FiO2, PACO2_target = p

    # Alveolar ventilation drives gas exchange
    # Simplified model based on mass balance

    # O2: ventilation brings in O2, perfusion removes it
    PiO2 = FiO2 * 713  # Inspired PO2 (humidified)
    dPAO2 = (VA/2.5) * (PiO2 - PAO2) - (Q/5.0) * (PAO2 - PvO2)

    # CO2: ventilation removes CO2, perfusion brings it
    dPACO2 = (Q/5.0) * (PvCO2 - PACO2) - (VA/2.5) * PACO2

    du[1] = dPAO2
    du[2] = dPACO2
end

# ============================================
# Example Simulation
# ============================================

function run_respiratory_example()
    using .RespiratoryPhysiology

    # O2-Hb dissociation curve
    PO2_range = 0:1:120
    SO2_normal = [OxygenTransport.hill_saturation(p) for p in PO2_range]

    # Right-shifted curve
    P50_shifted = OxygenTransport.P50_shift(26.6; delta_pH=-0.1, delta_T=2.0)
    SO2_shifted = [OxygenTransport.hill_saturation(p; P50=P50_shifted) for p in PO2_range]

    plt = plot(PO2_range, SO2_normal .* 100,
               label="Normal (P50=26.6)", lw=2, color=:blue)
    plot!(plt, PO2_range, SO2_shifted .* 100,
          label="Right shift (P50=$(round(P50_shifted, digits=1)))",
          lw=2, color=:red, linestyle=:dash)
    xlabel!(plt, "PO2 (mmHg)")
    ylabel!(plt, "Oxygen Saturation (%)")
    title!(plt, "Oxygen-Hemoglobin Dissociation Curve")

    return plt
end

function run_breathing_simulation()
    sol = simulate_breathing()

    plt = plot(sol.t, sol[1,:] .* 1000,  # Convert to mL
               xlabel="Time (s)", ylabel="Volume (mL)",
               title="Single Compartment Lung Model",
               label="Lung Volume", lw=2, color=:blue)

    return plt
end
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify the process**: Ventilation, gas exchange, transport, or control?
2. **List known quantities** with units
3. **Select appropriate equation**
4. **Check dimensional consistency**
5. **Calculate and interpret**
6. **Validate against physiological ranges**

### Typical Problem Types

**Type 1: Ventilation calculations**
- Given: Volumes, frequencies, dead space
- Find: Alveolar ventilation, minute ventilation

**Type 2: Gas exchange problems**
- Given: FiO2, altitude, PCO2
- Find: PAO2, A-a gradient, diffusing capacity

**Type 3: Oxygen transport**
- Given: Hb, saturation, cardiac output
- Find: O2 content, delivery, consumption

**Type 4: Acid-base disorders**
- Given: pH, PCO2, HCO3
- Find: Primary disorder, compensation, anion gap

### Clinical Correlations

| Condition | Key Abnormality | Physiological Impact |
|-----------|-----------------|---------------------|
| COPD | ↑ Compliance, ↑ Resistance | ↑ Time constant, air trapping |
| Pulmonary fibrosis | ↓ Compliance | ↓ Lung volumes, ↓ DLCO |
| Asthma | ↑ Airway resistance | Obstruction, hyperinflation |
| ARDS | ↓ Compliance, V/Q mismatch | Hypoxemia, shunt |
| Pulmonary embolism | ↑ Dead space | V/Q mismatch, hypoxemia |
| Anemia | ↓ O2 carrying capacity | ↓ DO2, compensatory ↑ CO |
| High altitude | ↓ PiO2 | Hypoxic stimulation, alkalosis |
| CO poisoning | Left-shifted curve | Impaired O2 unloading |

## Key Relationships Summary

| Process | Driving Force | Key Equation |
|---------|---------------|--------------|
| Ventilation | Pressure gradient | V̇ = ΔP/R |
| O2 diffusion | PO2 gradient | V̇O2 = DL × (PA - Pc) |
| O2 binding | PO2 | Hill equation |
| CO2 transport | PCO2, pH | Henderson-Hasselbalch |
| Ventilatory drive | PCO2, PO2 | Chemoreflex response |

## References

- Feher JJ. Quantitative Human Physiology, 3rd ed. Unit 6.
- West JB. Respiratory Physiology: The Essentials.
- Nunn JF. Applied Respiratory Physiology.


## Coverage-pass additions (Feher extraction)

10 equation(s) added to this domain, each verified against Feher and a worked example.

### Rohrer Equation (`rohrer_equation`)
- **Formula:** `delta_P = K1*Q_V + K2*Q_V^2`
- **LaTeX:** `\Delta P = K_1 Q_V + K_2 Q_V^2`
- **Import:** `from scripts.respiratory.mechanics import rohrer_equation` — or `from scripts.canonical_ids import load; load('rohrer_equation')`
- **Feher:** §6.2 — TURBULENT AND LAMINAR FLOW RESULT IN SERIES RESISTANCES THAT ADD
- Rohrer equation for overall airway resistance: the pressure difference driving airflow is the sum of a laminar term (K1*Q_V, Ohmic/Poiseuille) and a turbulent term (K2*Q_V^2).

### FEV1/FVC Ratio (`fev1_fvc_ratio`)
- **Formula:** `FEV1/FVC`
- **LaTeX:** `\mathrm{FEV_1/FVC} = \frac{\mathrm{FEV}_1}{\mathrm{FVC}}`
- **Import:** `from scripts.respiratory.mechanics import fev1_fvc_ratio` — or `from scripts.canonical_ids import load; load('fev1_fvc_ratio')`
- **Feher:** §6.2 — SPIROMETRY ALSO PROVIDES A CLINICALLY USEFUL MEASURE OF AIRWAY RESISTANCE
- Ratio of forced expiratory volume in 1 second to forced vital capacity: a dimensionless spirometric index of airway resistance / airflow obstruction.

### Alveolar CO2 Partial Pressure (Alveolar Ventilation Equation) (`alveolar_pco2_equation`)
- **Formula:** `P_ACO2 = (Q_CO2 / Q_A) * (P_B - P_H2O)`
- **LaTeX:** `P_{A_{CO_2}} = \dfrac{\dot{Q}_{CO_2}}{\dot{Q}_A}\,(P_B - P_{H_2O})`
- **Import:** `from scripts.respiratory.gas_exchange import alveolar_pco2_equation` — or `from scripts.canonical_ids import load; load('alveolar_pco2_equation')`
- **Feher:** §6.3 — THE RATE OF CO2 PRODUCTION ALLOWS CALCULATION OF ALVEOLAR VENTILATION
- Alveolar (and, at equilibrium, arterial) CO2 partial pressure, obtained by rearranging Feher's alveolar ventilation equation.

### Oxygen Consumption (Inspired-Expired Gas Exchange) (`oxygen_consumption_gas_exchange`)
- **Formula:** `VO2 = Q_T_star * fIO2 - Q_T * fEO2`
- **LaTeX:** `\dot{Q}_{O_2} = Q_T^{*}\,f_{I_{O_2}} - Q_T\,f_{E_{O_2}}`
- **Import:** `from scripts.respiratory.oxygen_transport import oxygen_consumption_gas_exchange` — or `from scripts.canonical_ids import load; load('oxygen_consumption_gas_exchange')`
- **Feher:** §6.4 — OXYGEN CONSUMPTION CAN BE CALCULATED FROM THE DIFFERENCE BETWEEN INSPIRED O2 AND EXPIRED O2
- Whole-body oxygen consumption (VO2) from the open-circuit ventilatory mass balance: inspired O2 volumetric flow minus expired O2 volumetric flow.

### Base Excess (Van Slyke Equation) (`base_excess_van_slyke`)
- **Formula:** `BE = (HCO3 - 24.4 + (2.3*Hb + 7.7)*(pH - 7.4)) * (1 - 0.023*Hb)`
- **LaTeX:** `\mathrm{BE} = \left([\mathrm{HCO_3^-}] - 24.4 + (2.3\,[\mathrm{Hb}] + 7.7)(\mathrm{pH} - 7.4)\right)\left(1 - 0.023\,[\mathrm{Hb}]\right)`
- **Import:** `from scripts.respiratory.acid_base import base_excess_van_slyke` — or `from scripts.canonical_ids import load; load('base_excess_van_slyke')`
- **Feher:** §6.5 — THE CONCEPT OF BASE EXCESS OR BASE DEFICIT
- Siggaard-Andersen 'Van Slyke' equation for in-vitro base excess: the amount of strong acid (HCl) needed to titrate a blood sample to pH 7.4 at PCO2 40 mmHg and 37C (negative value = base deficit, the amount of strong base needed).

### Apparent Strong Ion Difference (SIDa) (`strong_ion_difference_apparent`)
- **Formula:** `SIDa = [Na+] + [K+] + 2[Ca2+] + 2[Mg2+] - [Cl-] - [lactate]`
- **LaTeX:** `[\mathrm{SID}]_a = [\mathrm{Na^+}] + [\mathrm{K^+}] + 2[\mathrm{Ca^{2+}}] + 2[\mathrm{Mg^{2+}}] - [\mathrm{Cl^-}] - [\mathrm{lactate}]`
- **Import:** `from scripts.respiratory.acid_base import strong_ion_difference_apparent` — or `from scripts.canonical_ids import load; load('strong_ion_difference_apparent')`
- **Feher:** §6.5 — THE STRONG ION DIFFERENCE
- Apparent strong ion difference from the Stewart quantitative acid-base approach: the sum of measured strong cation charges minus strong anion charges.

### Standard Base Excess (`standard_base_excess`)
- **Formula:** `SBE = [HCO3-] - 24.8 + 16.2 * (pH - 7.40)`
- **LaTeX:** `\mathrm{SBE} = [\mathrm{HCO_3^-}] - 24.8 + 16.2\,(\mathrm{pH} - 7.40)`
- **Import:** `from scripts.respiratory.acid_base import standard_base_excess` — or `from scripts.canonical_ids import load; load('standard_base_excess')`
- **Feher:** §6.5 — THE CONCEPT OF BASE EXCESS OR BASE DEFICIT
- Standard base excess: the Siggaard-Andersen whole-body (in vivo, extracellular-buffer) modification of the Van Slyke base-excess equation.

### Weak-Acid Anion Charge (Figge-Fencl) (`weak_acid_anion_charge`)
- **Formula:** `[A-] = (0.123*pH - 0.631)*[Alb] + (0.309*pH - 0.469)*[Pi]`
- **LaTeX:** `[\mathrm{A^-}] = (0.123\,\mathrm{pH} - 0.631)[\mathrm{Alb}] + (0.309\,\mathrm{pH} - 0.469)[\mathrm{Pi}]`
- **Import:** `from scripts.respiratory.acid_base import weak_acid_anion_charge` — or `from scripts.canonical_ids import load; load('weak_acid_anion_charge')`
- **Feher:** §6.5 — THE STRONG ION DIFFERENCE
- Figge-Fencl empirical estimate of the non-volatile weak-acid buffer charge (plasma protein + phosphate) as a function of pH.

### Effective Strong Ion Difference (`strong_ion_difference_effective`)
- **Formula:** `SIDe = [HCO3-] + [A-]`
- **LaTeX:** `[\mathrm{SID}]_e = [\mathrm{HCO_3^-}] + [\mathrm{A^-}]`
- **Import:** `from scripts.respiratory.acid_base import strong_ion_difference_effective` — or `from scripts.canonical_ids import load; load('strong_ion_difference_effective')`
- **Feher:** §6.5 — THE STRONG ION DIFFERENCE
- Effective strong ion difference in the Stewart approach to acid-base analysis: the sum of plasma bicarbonate and the net negative charge carried by plasma weak acids (albumin and phosphate).

### Strong Ion Gap (`strong_ion_gap`)
- **Formula:** `SIG = SID_a - SID_e`
- **LaTeX:** `\mathrm{SIG} = \mathrm{SID}_a - \mathrm{SID}_e`
- **Import:** `from scripts.respiratory.acid_base import strong_ion_gap` — or `from scripts.canonical_ids import load; load('strong_ion_gap')`
- **Feher:** §6.5 — THE STRONG ION DIFFERENCE
- Strong ion gap (Stewart quantitative acid-base): the difference between the apparent and effective strong ion difference.



## Review additions (2026-07-15)

- **kassirer_bleich_hydrogen_ion** — `[H+] = 24*PCO2/HCO3` — Log-free bedside [H+] in nmol/L (40 = pH 7.40). Import: `from scripts.respiratory.acid_base import kassirer_bleich_hydrogen_ion_equation` (or `load("kassirer_bleich_hydrogen_ion")`).
- **work_of_breathing_elastic** — `W_el = 0.5*dP*VT` — Elastic work per breath (triangle area on static P-V curve). Import: `from scripts.respiratory.mechanics import work_of_breathing_elastic_equation` (or `load("work_of_breathing_elastic")`).

## Adversarial-review additions (2026-07-15)

- **oxygenation_index** — `OI = FiO2 x MAP x 100 / PaO2` — ICU hypoxaemic-failure severity incorporating mean airway pressure (>40 a classic ECMO trigger); FiO2 fraction, MAP cmH2O, PaO2 mmHg. `load("oxygenation_index")`.
- **acute_respiratory_acidosis_hco3** — `HCO3 = 24 + 1.0(PCO2-40)/10` — expected bicarbonate in acute respiratory acidosis (+1 mEq/L per +10 mmHg PaCO2); deviation flags a mixed disorder. `load("acute_respiratory_acidosis_hco3")`.
- **acute_respiratory_alkalosis_hco3** — `HCO3 = 24 - 2.0(40-PCO2)/10` — expected bicarbonate in acute respiratory alkalosis (-2 mEq/L per -10 mmHg PaCO2). `load("acute_respiratory_alkalosis_hco3")`.

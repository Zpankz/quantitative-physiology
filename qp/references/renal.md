---
name: renal
description: Renal physiology - glomerular filtration, tubular transport, concentration mechanisms, acid-base regulation, and fluid/electrolyte balance
parent: quantitative-physiology
unit: 7
---

# Renal Physiology

## Overview

This sub-skill covers the quantitative principles of kidney function, including glomerular filtration, tubular reabsorption and secretion, urine concentration/dilution, acid-base handling, and fluid-electrolyte homeostasis. The kidney maintains plasma composition through sophisticated transport mechanisms and regulatory systems.

## Core Concepts

### 1. Renal Anatomy and Blood Flow

#### Functional Anatomy

**Nephron components**:
- Glomerulus (filtration)
- Proximal tubule (bulk reabsorption)
- Loop of Henle (concentration gradient)
- Distal tubule (fine-tuning)
- Collecting duct (final concentration)

**Nephron types**:
- Cortical nephrons: ~85%, short loops
- Juxtamedullary nephrons: ~15%, long loops into medulla

#### Renal Blood Flow

**Renal blood flow (RBF)**:
```
RBF ≈ 1.2 L/min (≈20-25% of cardiac output)
```

**Renal plasma flow (RPF)**:
```
RPF = RBF × (1 - Hct)
RPF ≈ 660 mL/min (for Hct = 0.45)
```

**Filtration fraction (FF)**:
```
FF = GFR / RPF ≈ 0.20 (20%)
```

**Renal vascular resistance**:
Formula → qp:`renal_vascular_resistance`

Two resistances in series:
- Afferent arteriole (R_A)
- Efferent arteriole (R_E)

### 2. Glomerular Filtration

#### Starling Forces in Glomerulus

**Net filtration pressure (NFP)**:
Formula → qp:`glomerular_nfp`

Where:
- P_GC = Glomerular capillary pressure (~60 mmHg)
- P_BC = Bowman's capsule pressure (~15 mmHg)
- π_GC = Glomerular oncotic pressure (~28 mmHg at afferent, ~35 mmHg at efferent)
- π_BC = Bowman's capsule oncotic pressure (~0, filtrate is protein-free)

**Typical values**:
```
NFP = 60 - 15 - 28 + 0 = 17 mmHg (afferent end)
NFP = 60 - 15 - 35 + 0 = 10 mmHg (efferent end)
```

#### Glomerular Filtration Rate (GFR)

**GFR equation**:
Formula → qp:`gfr_from_nfp`

Where K_f = ultrafiltration coefficient (product of hydraulic conductivity and surface area)

**Normal GFR**:
```
GFR ≈ 125 mL/min = 180 L/day
```

**GFR adjustment for body size**:
Formula → qp:`gfr_normalized`

#### Clearance

**Clearance definition**:
Formula → qp:`clearance`

Where:
- C_x = Clearance of substance x (mL/min)
- U_x = Urine concentration of x
- V̇ = Urine flow rate (mL/min)
- P_x = Plasma concentration of x

**Inulin clearance = GFR** (gold standard):
Formula → qp:`clearance`

**Creatinine clearance** (clinical estimate):
```
C_Cr ≈ GFR (slight overestimate due to secretion)
```

**Cockcroft-Gault equation**:
Formula → qp:`cockcroft_gault`

**MDRD/CKD-EPI equations** (more accurate for eGFR):
```
eGFR = 141 × min(S_Cr/κ, 1)^α × max(S_Cr/κ, 1)^(-1.209) × 0.993^age × [1.018 if female] × [1.159 if Black]
```

#### Filtered Load

**Amount filtered per unit time**:
Formula → qp:`filtered_load`

Example: Glucose filtered load
```
FL_glucose = 125 mL/min × 100 mg/dL = 125 mg/min = 180 g/day
```

### 3. Tubular Reabsorption and Secretion

#### Mass Balance

**Excretion equation**:
Formula → qp:`excretion_mass_balance`

**Fractional excretion**:
Formula → qp:`fractional_excretion_direct`

**For sodium**:
```
FE_Na = (U_Na × P_Cr) / (P_Na × U_Cr) × 100%

Normal FE_Na < 1%
```

#### PAH Clearance and RPF

**Para-aminohippuric acid (PAH)** is completely cleared in one pass:
```
C_PAH ≈ RPF (at low plasma concentrations)
```

**Extraction ratio**:
```
E_PAH = (P_a - P_v) / P_a ≈ 0.9
```

**True RPF**:
Formula → qp:`true_rpf_from_pah`

#### Transport Maximum (T_m)

**Saturable transport**:
Formula → qp:`transport_tm`

**Glucose reabsorption**:
- T_m glucose ≈ 375 mg/min
- Renal threshold ≈ 200 mg/dL (splay due to nephron heterogeneity)

**Titration curve**:
- Below threshold: All glucose reabsorbed, none excreted
- Above T_m: Excess glucose excreted (glucosuria)

#### Proximal Tubule Transport

**Reabsorption rates** (~65-70% of filtered load):
- Na⁺: ~65%
- Water: ~65% (follows solute)
- HCO₃⁻: ~80-90%
- Glucose: ~100%
- Amino acids: ~100%
- K⁺: ~65%
- Cl⁻: ~50%

**Na⁺/glucose cotransport (SGLT2)**:
Formula → qp:`transport_tm`

**Na⁺/H⁺ exchanger (NHE3)**:
```
Na⁺_in + H⁺_out (generates new HCO₃⁻)
```

### 4. Loop of Henle and Countercurrent System

#### Countercurrent Multiplication

**Medullary osmolality gradient**:
- Cortex: 300 mOsm/kg
- Outer medulla: 600 mOsm/kg
- Inner medulla: 900-1200 mOsm/kg (up to 1400 with dehydration)

**Single effect**:
```
Δπ ≈ 200 mOsm/kg (thick ascending limb)
```

**Multiplication factor**:
Formula → qp:`countercurrent_multiplication`
Where L = loop length, λ = characteristic length

#### Loop Segment Transport

**Thick ascending limb (TAL)**:
- Na⁺/K⁺/2Cl⁻ cotransporter (NKCC2)
- Impermeable to water
- Creates dilute tubular fluid
- Generates medullary hypertonicity

**NKCC2 inhibition** (loop diuretics):
```
J_NaCl = J_max × [NaCl] / (K_m + [NaCl]) × (1 - [furosemide]/K_i)
```

**Thin descending limb**:
- Permeable to water
- Relatively impermeable to solutes
- Equilibrates with medullary interstitium

#### Countercurrent Exchange (Vasa Recta)

**Hairpin arrangement** minimizes solute washout:
Formula → qp:`ficks_law_diffusion`

**Efficiency** depends on flow rate:
- Low flow: Better equilibration, maintains gradient
- High flow: Washout of medullary solutes

### 5. Distal Nephron and Collecting Duct

#### Distal Convoluted Tubule (DCT)

**Na⁺/Cl⁻ cotransporter (NCC)**:
- Thiazide-sensitive
- 5-10% of Na⁺ reabsorption

**Ca²⁺ reabsorption**:
Formula → qp:`ionic_current`
Enhanced by PTH and thiazides

#### Collecting Duct

**Principal cells**:
- ENaC (Na⁺ reabsorption, aldosterone-regulated)
- ROMK (K⁺ secretion)
- Aquaporin-2 (ADH-regulated water reabsorption)

**Na⁺ reabsorption via ENaC**:
```
I_Na = N × P_o × i × (V_m - E_Na)
```
Where N = channel number, P_o = open probability, i = single channel current

**Aldosterone effects** (hours):
- ↑ ENaC expression and activity
- ↑ Na⁺/K⁺-ATPase
- ↑ K⁺ secretion

**Intercalated cells**:
- Type A: H⁺ secretion (H⁺-ATPase), HCO₃⁻ reabsorption
- Type B: HCO₃⁻ secretion, H⁺ reabsorption

### 6. Urine Concentration and Dilution

#### ADH/Vasopressin Effects

**Aquaporin-2 insertion**:
Formula → qp:`adh_water_permeability`

**Water reabsorption**:
Formula → qp:`water_reabsorption_flux`

#### Concentration Mechanism

**Maximum urine osmolality**: ~1200 mOsm/kg

**Free water clearance**:
Formula → qp:`free_water_clearance`

Where:
- C_H2O > 0: Dilute urine (water excess)
- C_H2O < 0: Concentrated urine (water deficit) = T^c_H2O

**Urine-to-plasma osmolality ratio**:
```
U/P_osm = 0.2 - 4.0 (dilute to concentrated)
```

#### Dilution Mechanism

**Minimum urine osmolality**: ~50-100 mOsm/kg

**Water diuresis**:
```
V̇_max = C_osm + C_H2O_max
```

With C_osm ≈ 1 mL/min and maximal dilution:
```
V̇_max ≈ 15-20 mL/min (≈20 L/day)
```

### 7. Acid-Base Handling

#### Bicarbonate Reabsorption

**Proximal tubule** (80-90% of filtered HCO₃⁻):
```
Filtered HCO₃⁻ + secreted H⁺ → H₂CO₃ → CO₂ + H₂O
CO₂ diffuses into cell → regenerates HCO₃⁻
```

**Net reaction**:
```
HCO₃⁻_filtered → HCO₃⁻_reabsorbed (not new HCO₃⁻)
```

#### New Bicarbonate Generation

**Titratable acid** (phosphate buffer):
```
HPO₄²⁻ + H⁺ → H₂PO₄⁻
```
Generates ~30 mEq/day new HCO₃⁻

**Ammonium excretion**:
```
Glutamine → NH₄⁺ + new HCO₃⁻
NH₄⁺ trapped in urine (NH₃ + H⁺ → NH₄⁺)
```
Generates ~40 mEq/day new HCO₃⁻

**Total acid excretion**:
Formula → qp:`net_acid_excretion`

Normal: 50-100 mEq/day (matches dietary acid load)

#### Renal Compensation

**Metabolic acidosis** → ↑ H⁺ secretion, ↑ NH₄⁺ production
**Metabolic alkalosis** → ↓ H⁺ secretion, HCO₃⁻ excretion

**Compensation time course**:
- Begins in hours
- Complete in 3-5 days

### 8. Potassium Handling

#### K⁺ Balance

**Filtered K⁺**: ~720 mEq/day
**Excreted K⁺**: ~90 mEq/day (12.5% of filtered)

**Proximal tubule**: 65% reabsorption (paracellular)
**Loop of Henle**: 25% reabsorption (TAL, paracellular and transcellular)
**Collecting duct**: Variable secretion/reabsorption

#### K⁺ Secretion (Principal Cells)

**Driving force**:
Formula → qp:`k_secretion_flux`

**Factors increasing K⁺ secretion**:
- High plasma [K⁺]
- Aldosterone
- High tubular flow rate
- Alkalosis
- High Na⁺ delivery to CCD

**Electrochemical gradient**:
Formula → qp:`k_nernst_potential`

### 9. Sodium and Water Balance

#### Effective Circulating Volume

**Sensors**:
- Carotid/aortic baroreceptors
- Juxtaglomerular apparatus
- Atrial stretch receptors

#### Renin-Angiotensin-Aldosterone System (RAAS)

**Renin release stimulated by**:
- ↓ Renal perfusion pressure
- ↓ NaCl delivery to macula densa
- ↑ Sympathetic activity (β₁ receptors)

**Angiotensin II effects**:
- Vasoconstriction (↑ TPR)
- ↑ Na⁺ reabsorption (proximal tubule)
- ↑ Aldosterone release
- ↑ ADH release
- ↑ Thirst

**Aldosterone effects**:
- ↑ ENaC activity (↑ Na⁺ reabsorption)
- ↑ K⁺ secretion
- ↑ H⁺ secretion

#### Atrial Natriuretic Peptide (ANP)

**Released by**: Atrial stretch

**Effects**:
- ↑ GFR (afferent dilation, efferent constriction)
- ↓ Na⁺ reabsorption (collecting duct)
- ↓ Renin release
- ↓ Aldosterone release
- Natriuresis and diuresis

### 10. Regulation of GFR

#### Autoregulation

**Myogenic mechanism**:
```
↑ P_a → ↑ wall tension → smooth muscle contraction → ↑ R_A → stable RBF
```

**Tubuloglomerular feedback (TGF)**:
```
↑ NaCl at macula densa → ↑ ATP/adenosine release → afferent vasoconstriction → ↓ GFR
```

**Autoregulation range**: 80-180 mmHg MAP

#### Afferent vs Efferent Arteriole Effects

| Change | GFR | RBF | FF |
|--------|-----|-----|-----|
| ↑ R_A | ↓ | ↓ | ↔ |
| ↓ R_A | ↑ | ↑ | ↔ |
| ↑ R_E | ↑ | ↓ | ↑ |
| ↓ R_E | ↓ | ↑ | ↓ |

**ACE inhibitors**: ↓ Angiotensin II → ↓ R_E → ↓ GFR (but renoprotective long-term)

## Computational Models

### Python Implementation

```python
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import brentq
import matplotlib.pyplot as plt

# Physical constants
R = 8.314      # J/(mol·K)
F = 96485      # C/mol
T = 310        # K (37°C)


class GlomerularFiltration:
    """Glomerular filtration calculations"""

    @staticmethod
    def net_filtration_pressure(P_GC, P_BC, pi_GC, pi_BC=0):
        """
        Calculate net filtration pressure (Starling forces)

        Parameters:
        -----------
        P_GC : float - Glomerular capillary pressure (mmHg)
        P_BC : float - Bowman's capsule pressure (mmHg)
        pi_GC : float - Glomerular oncotic pressure (mmHg)
        pi_BC : float - Bowman's capsule oncotic pressure (mmHg)

        Returns:
        --------
        NFP : float - Net filtration pressure (mmHg)
        """
        return P_GC - P_BC - pi_GC + pi_BC

    @staticmethod
    def GFR(K_f, NFP):
        """
        Calculate GFR from ultrafiltration coefficient and NFP

        Parameters:
        -----------
        K_f : float - Ultrafiltration coefficient (mL/min/mmHg)
        NFP : float - Net filtration pressure (mmHg)

        Returns:
        --------
        GFR : float - Glomerular filtration rate (mL/min)
        """
        return K_f * NFP

    @staticmethod
    def filtration_fraction(GFR, RPF):
        """Calculate filtration fraction"""
        return GFR / RPF

    @staticmethod
    def RPF_from_RBF(RBF, Hct=0.45):
        """Calculate renal plasma flow from blood flow"""
        return RBF * (1 - Hct)


class Clearance:
    """Renal clearance calculations"""

    @staticmethod
    def clearance(U_x, V_dot, P_x):
        """
        Calculate clearance of substance x

        Parameters:
        -----------
        U_x : float - Urine concentration (mg/dL or mmol/L)
        V_dot : float - Urine flow rate (mL/min)
        P_x : float - Plasma concentration (same units as U_x)

        Returns:
        --------
        C_x : float - Clearance (mL/min)
        """
        return (U_x * V_dot) / P_x

    @staticmethod
    def filtered_load(GFR, P_x):
        """Calculate amount filtered per unit time"""
        return GFR * P_x

    @staticmethod
    def fractional_excretion(C_x, GFR):
        """Calculate fractional excretion"""
        return C_x / GFR

    @staticmethod
    def FE_Na(U_Na, P_Na, U_Cr, P_Cr):
        """
        Calculate fractional excretion of sodium

        Returns FE_Na as percentage
        """
        return (U_Na * P_Cr) / (P_Na * U_Cr) * 100

    @staticmethod
    def cockcroft_gault(age, weight, S_Cr, female=False):
        """
        Cockcroft-Gault equation for creatinine clearance

        Parameters:
        -----------
        age : float - Age (years)
        weight : float - Weight (kg)
        S_Cr : float - Serum creatinine (mg/dL)
        female : bool - True if female

        Returns:
        --------
        C_Cr : float - Estimated creatinine clearance (mL/min)
        """
        C_Cr = ((140 - age) * weight) / (72 * S_Cr)
        if female:
            C_Cr *= 0.85
        return C_Cr

    @staticmethod
    def free_water_clearance(V_dot, U_osm, P_osm):
        """
        Calculate free water clearance

        C_H2O > 0: dilute urine (water excess)
        C_H2O < 0: concentrated urine (water deficit)
        """
        C_osm = (U_osm * V_dot) / P_osm
        return V_dot - C_osm


class TubularTransport:
    """Tubular reabsorption and secretion"""

    @staticmethod
    def transport_Tm(T_max, S, K_m):
        """
        Saturable transport (Michaelis-Menten)

        Parameters:
        -----------
        T_max : float - Maximum transport rate
        S : float - Substrate concentration
        K_m : float - Michaelis constant

        Returns:
        --------
        T : float - Transport rate
        """
        return T_max * S / (K_m + S)

    @staticmethod
    def glucose_excretion(filtered_load, T_max=375):
        """
        Calculate glucose excretion

        Parameters:
        -----------
        filtered_load : float - Glucose filtered (mg/min)
        T_max : float - Maximum reabsorption (mg/min)

        Returns:
        --------
        excretion : float - Glucose excreted (mg/min)
        """
        if filtered_load <= T_max:
            return 0  # All reabsorbed
        else:
            return filtered_load - T_max

    @staticmethod
    def excretion_balance(GFR, P_x, R_x, S_x):
        """
        Mass balance: Excretion = Filtration - Reabsorption + Secretion
        """
        filtration = GFR * P_x
        return filtration - R_x + S_x


class CountercurrentSystem:
    """Medullary concentration gradient"""

    @staticmethod
    def medullary_gradient(depth, osm_cortex=300, osm_tip=1200):
        """
        Medullary osmolality as function of depth

        Parameters:
        -----------
        depth : float - Fractional depth into medulla (0-1)
        osm_cortex : float - Cortical osmolality (mOsm/kg)
        osm_tip : float - Papillary tip osmolality (mOsm/kg)

        Returns:
        --------
        osm : float - Osmolality at given depth
        """
        return osm_cortex + (osm_tip - osm_cortex) * depth

    @staticmethod
    def loop_multiplication_factor(loop_length, lambda_char):
        """
        Countercurrent multiplication factor

        Parameters:
        -----------
        loop_length : float - Length of loop of Henle
        lambda_char : float - Characteristic length
        """
        return np.exp(loop_length / lambda_char)


class AcidBaseKidney:
    """Renal acid-base handling"""

    @staticmethod
    def net_acid_excretion(TA, NH4, HCO3_excreted):
        """
        Calculate net acid excretion

        Parameters:
        -----------
        TA : float - Titratable acid (mEq/day)
        NH4 : float - Ammonium excretion (mEq/day)
        HCO3_excreted : float - Bicarbonate excreted (mEq/day)

        Returns:
        --------
        NAE : float - Net acid excretion (mEq/day)
        """
        return TA + NH4 - HCO3_excreted

    @staticmethod
    def new_HCO3_generation(TA, NH4):
        """
        New bicarbonate generated per day
        Equal to net acid excretion if HCO3 excretion = 0
        """
        return TA + NH4


class PotassiumBalance:
    """K+ handling calculations"""

    @staticmethod
    def K_secretion_driving_force(V_m, E_K):
        """
        Electrochemical driving force for K+ secretion

        Parameters:
        -----------
        V_m : float - Membrane potential (mV)
        E_K : float - K+ equilibrium potential (mV)

        Returns:
        --------
        Driving force (mV), positive = secretion favored
        """
        return V_m - E_K

    @staticmethod
    def E_K(K_lumen, K_cell, T=310):
        """
        Nernst potential for K+

        Parameters:
        -----------
        K_lumen : float - Luminal K+ concentration (mM)
        K_cell : float - Cell K+ concentration (mM)
        """
        return (R * T / F) * np.log(K_lumen / K_cell) * 1000  # mV


class WaterBalance:
    """Water handling and ADH effects"""

    @staticmethod
    def water_permeability(P_0, P_max, ADH, K_ADH):
        """
        ADH-dependent water permeability

        Parameters:
        -----------
        P_0 : float - Baseline permeability
        P_max : float - Maximum additional permeability
        ADH : float - ADH concentration
        K_ADH : float - Half-maximal ADH concentration
        """
        return P_0 + P_max * ADH / (K_ADH + ADH)

    @staticmethod
    def urine_osmolality_range():
        """Return range of possible urine osmolality"""
        return {'min': 50, 'max': 1200, 'unit': 'mOsm/kg'}

    @staticmethod
    def urine_concentration_ratio(U_osm, P_osm):
        """Urine to plasma osmolality ratio"""
        return U_osm / P_osm


class NephronModel:
    """Dynamic nephron simulation"""

    def __init__(self, GFR=125, RPF=660):
        self.GFR = GFR  # mL/min
        self.RPF = RPF  # mL/min

        # Segment parameters (fractional reabsorption)
        self.f_PT = 0.65    # Proximal tubule
        self.f_LOH = 0.25   # Loop of Henle
        self.f_DCT = 0.05   # Distal tubule
        self.f_CD = 0.05    # Collecting duct (variable)

    def single_nephron_GFR(self, n_nephrons=1e6):
        """Single nephron GFR"""
        return self.GFR / n_nephrons * 1000  # nL/min

    def tubular_flow(self, segment):
        """
        Flow rate at different tubular segments

        Parameters:
        -----------
        segment : str - 'PT', 'LOH', 'DCT', 'CD', 'urine'

        Returns:
        --------
        flow : float - Flow rate (mL/min)
        """
        remaining = 1.0

        if segment == 'PT':
            return self.GFR

        remaining -= self.f_PT
        if segment == 'LOH':
            return self.GFR * remaining

        remaining -= self.f_LOH
        if segment == 'DCT':
            return self.GFR * remaining

        remaining -= self.f_DCT
        if segment == 'CD':
            return self.GFR * remaining

        remaining -= self.f_CD
        if segment == 'urine':
            return self.GFR * remaining

        return None

    def concentration_profile(self, x, C_in, f_reabsorb, length=1.0):
        """
        Solute concentration along tubule

        Assumes exponential reabsorption pattern
        """
        k = -np.log(1 - f_reabsorb) / length
        return C_in * np.exp(-k * x)


def simulate_glucose_titration():
    """
    Simulate glucose titration curve

    Shows relationship between plasma glucose, filtered load,
    reabsorption, and excretion
    """
    GFR = 125  # mL/min
    T_max = 375  # mg/min

    # Plasma glucose range (mg/dL)
    P_glu = np.linspace(0, 600, 100)

    # Convert to filtered load (mg/min)
    # Note: 125 mL/min × mg/dL × (1 dL/100 mL) = 1.25 × mg/dL in mg/min
    filtered = GFR * P_glu / 100  # mg/min

    # Reabsorption (limited by Tm)
    reabsorbed = np.minimum(filtered, T_max)

    # Excretion
    excreted = filtered - reabsorbed

    # Renal threshold (with splay)
    threshold = T_max / (GFR / 100)  # ~300 mg/dL theoretical

    plt.figure(figsize=(10, 6))
    plt.plot(P_glu, filtered, 'b-', label='Filtered', linewidth=2)
    plt.plot(P_glu, reabsorbed, 'g-', label='Reabsorbed', linewidth=2)
    plt.plot(P_glu, excreted, 'r-', label='Excreted', linewidth=2)
    plt.axhline(T_max, color='gray', linestyle='--', label=f'Tm = {T_max} mg/min')
    plt.axvline(200, color='orange', linestyle=':', label='Renal threshold (~200 mg/dL)')

    plt.xlabel('Plasma Glucose (mg/dL)')
    plt.ylabel('Rate (mg/min)')
    plt.title('Glucose Titration Curve')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 600)
    plt.ylim(0, 800)

    return plt.gcf()


# Example usage
if __name__ == "__main__":
    # Example: Calculate GFR from clearance
    cl = Clearance()

    # Inulin clearance
    U_inulin = 30  # mg/dL
    V_dot = 1.5    # mL/min
    P_inulin = 0.36  # mg/dL

    GFR = cl.clearance(U_inulin, V_dot, P_inulin)
    print(f"GFR (inulin clearance): {GFR:.1f} mL/min")

    # Creatinine clearance estimate
    age = 45
    weight = 70
    S_Cr = 1.0
    C_Cr = cl.cockcroft_gault(age, weight, S_Cr)
    print(f"Estimated CrCl (Cockcroft-Gault): {C_Cr:.1f} mL/min")

    # FE_Na for acute kidney injury assessment
    fe_na = cl.FE_Na(U_Na=40, P_Na=140, U_Cr=100, P_Cr=1.0)
    print(f"FE_Na: {fe_na:.2f}% ({'prerenal' if fe_na < 1 else 'intrinsic renal'})")

    # Free water clearance
    C_H2O = cl.free_water_clearance(V_dot=2.0, U_osm=600, P_osm=290)
    print(f"Free water clearance: {C_H2O:.2f} mL/min")
    if C_H2O < 0:
        print(f"  -> Concentrated urine (T^c_H2O = {-C_H2O:.2f} mL/min)")
```

### Julia Implementation

```julia
module RenalPhysiology

using DifferentialEquations
using Plots

# Constants
const R = 8.314      # J/(mol·K)
const F = 96485      # C/mol
const T_body = 310   # K (37°C)

# =============================================================================
# Glomerular Filtration
# =============================================================================
module Glomerular

"""
    net_filtration_pressure(P_GC, P_BC, π_GC, π_BC=0)

Calculate net filtration pressure using Starling forces.
All pressures in mmHg.
"""
function net_filtration_pressure(P_GC, P_BC, π_GC, π_BC=0)
    return P_GC - P_BC - π_GC + π_BC
end

"""
    GFR(K_f, NFP)

Calculate GFR from ultrafiltration coefficient (mL/min/mmHg) and NFP (mmHg).
Returns GFR in mL/min.
"""
GFR(K_f, NFP) = K_f * NFP

"""
    filtration_fraction(GFR, RPF)

Calculate filtration fraction (dimensionless, typically ~0.20).
"""
filtration_fraction(GFR, RPF) = GFR / RPF

"""
    RPF_from_RBF(RBF; Hct=0.45)

Calculate renal plasma flow from renal blood flow.
"""
RPF_from_RBF(RBF; Hct=0.45) = RBF * (1 - Hct)

end # module Glomerular

# =============================================================================
# Clearance Calculations
# =============================================================================
module ClearanceCalcs

"""
    clearance(U_x, V̇, P_x)

Calculate clearance: C_x = (U_x × V̇) / P_x
"""
clearance(U_x, V̇, P_x) = (U_x * V̇) / P_x

"""
    filtered_load(GFR, P_x)

Calculate filtered load = GFR × P_x
"""
filtered_load(GFR, P_x) = GFR * P_x

"""
    fractional_excretion(C_x, GFR)

Calculate fractional excretion FE_x = C_x / GFR
"""
fractional_excretion(C_x, GFR) = C_x / GFR

"""
    FE_Na(U_Na, P_Na, U_Cr, P_Cr)

Calculate fractional excretion of sodium (%).
FE_Na < 1% suggests prerenal azotemia.
"""
FE_Na(U_Na, P_Na, U_Cr, P_Cr) = (U_Na * P_Cr) / (P_Na * U_Cr) * 100

"""
    cockcroft_gault(age, weight, S_Cr; female=false)

Estimate creatinine clearance using Cockcroft-Gault equation.
- age: years
- weight: kg
- S_Cr: serum creatinine (mg/dL)
"""
function cockcroft_gault(age, weight, S_Cr; female=false)
    C_Cr = ((140 - age) * weight) / (72 * S_Cr)
    return female ? C_Cr * 0.85 : C_Cr
end

"""
    free_water_clearance(V̇, U_osm, P_osm)

Calculate free water clearance.
- C_H2O > 0: dilute urine
- C_H2O < 0: concentrated urine (= T^c_H2O)
"""
function free_water_clearance(V̇, U_osm, P_osm)
    C_osm = (U_osm * V̇) / P_osm
    return V̇ - C_osm
end

end # module ClearanceCalcs

# =============================================================================
# Tubular Transport
# =============================================================================
module TubularTransport

"""
    transport_Tm(T_max, S, K_m)

Saturable transport following Michaelis-Menten kinetics.
"""
transport_Tm(T_max, S, K_m) = T_max * S / (K_m + S)

"""
    glucose_excretion(filtered_load; T_max=375)

Calculate glucose excretion (mg/min).
T_max for glucose ≈ 375 mg/min.
"""
function glucose_excretion(filtered_load; T_max=375)
    return max(0, filtered_load - T_max)
end

"""
    excretion_balance(GFR, P_x, R_x, S_x)

Mass balance: Excretion = Filtration - Reabsorption + Secretion
"""
excretion_balance(GFR, P_x, R_x, S_x) = GFR * P_x - R_x + S_x

# Fractional reabsorption by segment (typical Na+)
const SEGMENT_REABSORPTION = Dict(
    :PT => 0.65,    # Proximal tubule
    :LOH => 0.25,   # Loop of Henle
    :DCT => 0.05,   # Distal tubule
    :CD => 0.04     # Collecting duct
)

end # module TubularTransport

# =============================================================================
# Countercurrent System
# =============================================================================
module Countercurrent

"""
    medullary_gradient(depth; osm_cortex=300, osm_tip=1200)

Calculate medullary osmolality at fractional depth (0-1).
"""
function medullary_gradient(depth; osm_cortex=300, osm_tip=1200)
    return osm_cortex + (osm_tip - osm_cortex) * depth
end

"""
    single_effect()

Return the single effect of thick ascending limb (mOsm/kg).
"""
single_effect() = 200

"""
    multiplication_factor(loop_length, λ)

Countercurrent multiplication factor.
"""
multiplication_factor(loop_length, λ) = exp(loop_length / λ)

end # module Countercurrent

# =============================================================================
# Acid-Base (Renal)
# =============================================================================
module RenalAcidBase

"""
    net_acid_excretion(TA, NH4, HCO3_excreted)

Calculate net acid excretion (mEq/day).
Normal ≈ 50-100 mEq/day.
"""
net_acid_excretion(TA, NH4, HCO3_excreted) = TA + NH4 - HCO3_excreted

"""
    new_HCO3_generation(TA, NH4)

New bicarbonate generated per day (mEq/day).
TA ≈ 30 mEq/day, NH4 ≈ 40 mEq/day normally.
"""
new_HCO3_generation(TA, NH4) = TA + NH4

end # module RenalAcidBase

# =============================================================================
# Potassium Balance
# =============================================================================
module PotassiumBalance

"""
    E_K(K_lumen, K_cell; T=310)

Nernst potential for K+ (mV).
"""
function E_K(K_lumen, K_cell; T=310)
    return (8.314 * T / 96485) * log(K_lumen / K_cell) * 1000
end

"""
    K_secretion_driving_force(V_m, E_K)

Electrochemical driving force for K+ secretion.
Positive = secretion favored.
"""
K_secretion_driving_force(V_m, E_K) = V_m - E_K

end # module PotassiumBalance

# =============================================================================
# Water Balance
# =============================================================================
module WaterBalance

"""
    water_permeability(P_0, P_max, ADH, K_ADH)

ADH-dependent water permeability in collecting duct.
"""
water_permeability(P_0, P_max, ADH, K_ADH) = P_0 + P_max * ADH / (K_ADH + ADH)

"""
    urine_osmolality_limits()

Return physiological limits of urine concentration.
"""
urine_osmolality_limits() = (min=50, max=1200, unit="mOsm/kg")

"""
    concentration_ratio(U_osm, P_osm)

Urine-to-plasma osmolality ratio.
Range: 0.2 (very dilute) to 4.0 (maximally concentrated).
"""
concentration_ratio(U_osm, P_osm) = U_osm / P_osm

end # module WaterBalance

# =============================================================================
# Dynamic Nephron Model
# =============================================================================

"""
    nephron_Na_transport!(du, u, p, t)

ODE system for sodium transport along nephron.

State variables (u):
- u[1]: Na+ amount in proximal tubule
- u[2]: Na+ amount in loop of Henle
- u[3]: Na+ amount in distal tubule
- u[4]: Na+ amount in collecting duct
"""
function nephron_Na_transport!(du, u, p, t)
    # Parameters
    filtered_Na, k_PT, k_LOH, k_DCT, k_CD = p

    # Tubular segments
    Na_PT, Na_LOH, Na_DCT, Na_CD = u

    # Reabsorption rates (first-order kinetics)
    R_PT = k_PT * Na_PT
    R_LOH = k_LOH * Na_LOH
    R_DCT = k_DCT * Na_DCT
    R_CD = k_CD * Na_CD

    # ODEs (inflow - outflow - reabsorption)
    du[1] = filtered_Na - (Na_PT / 1.0) - R_PT          # PT
    du[2] = (Na_PT / 1.0) - (Na_LOH / 1.0) - R_LOH      # LOH
    du[3] = (Na_LOH / 1.0) - (Na_DCT / 1.0) - R_DCT     # DCT
    du[4] = (Na_DCT / 1.0) - (Na_CD / 1.0) - R_CD       # CD
end

"""
    simulate_nephron_transport()

Run nephron transport simulation.
"""
function simulate_nephron_transport()
    # Initial conditions
    u0 = [100.0, 35.0, 10.0, 5.0]  # Initial Na amounts

    # Parameters: filtered_Na, k_PT, k_LOH, k_DCT, k_CD
    p = (150.0, 0.65, 0.25, 0.05, 0.04)

    tspan = (0.0, 10.0)

    prob = ODEProblem(nephron_Na_transport!, u0, tspan, p)
    sol = solve(prob, Tsit5())

    return sol
end

"""
    plot_glucose_titration()

Generate glucose titration curve.
"""
function plot_glucose_titration()
    GFR = 125.0  # mL/min
    T_max = 375.0  # mg/min

    P_glu = 0:5:600  # Plasma glucose (mg/dL)
    filtered = GFR .* P_glu ./ 100  # mg/min
    reabsorbed = min.(filtered, T_max)
    excreted = filtered .- reabsorbed

    plt = plot(P_glu, filtered,
               label="Filtered", linewidth=2,
               xlabel="Plasma Glucose (mg/dL)",
               ylabel="Rate (mg/min)",
               title="Glucose Titration Curve")
    plot!(plt, P_glu, reabsorbed, label="Reabsorbed", linewidth=2)
    plot!(plt, P_glu, excreted, label="Excreted", linewidth=2)
    hline!(plt, [T_max], linestyle=:dash, label="Tm", color=:gray)
    vline!(plt, [200], linestyle=:dot, label="Threshold", color=:orange)

    return plt
end

end # module RenalPhysiology
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify the question type**: Clearance, filtration, transport, acid-base, concentration?
2. **Draw the nephron segment** involved
3. **Write the relevant equations**
4. **Substitute known values** with proper units
5. **Calculate and verify** physiological reasonableness
6. **Consider clinical implications**

### Typical Problems

**Type 1: Clearance and GFR**
- Given: Urine and plasma concentrations, urine flow
- Find: Clearance, GFR, filtered load, FE

**Type 2: Starling forces**
- Given: Capillary pressures, oncotic pressures
- Find: NFP, GFR, direction of fluid movement

**Type 3: Transport maximum**
- Given: Plasma concentration, GFR, Tm
- Find: Reabsorption, excretion rates

**Type 4: Concentration/dilution**
- Given: Urine osmolality, volume, plasma osmolality
- Find: Free water clearance, ADH status

**Type 5: Acid-base**
- Given: Urine pH, NH4+, titratable acid
- Find: Net acid excretion, renal compensation

### Clinical Correlations

| Condition | Key Finding | Mechanism |
|-----------|-------------|-----------|
| Prerenal AKI | FE_Na < 1% | Intact tubular function, low perfusion |
| ATN | FE_Na > 2% | Tubular damage, impaired reabsorption |
| SIADH | ↓ Serum Na+, concentrated urine | Excess ADH, water retention |
| Diabetes insipidus | Dilute urine, polyuria | Lack of ADH or response |
| RTA Type 1 | Urine pH > 5.5 in acidosis | Impaired H+ secretion in CD |
| RTA Type 2 | Low serum HCO3-, acidic urine | Impaired proximal HCO3- reabsorption |
| Hyperaldosteronism | Hypokalemia, alkalosis | ↑ K+ and H+ secretion |

## Key Equations Summary

| Process | Equation | Normal Value |
|---------|----------|--------------|
| Clearance | C_x = (U_x × V̇)/P_x | varies |
| GFR | ~125 mL/min | 90-120 mL/min |
| RPF | ~660 mL/min | 600-700 mL/min |
| FF | GFR/RPF | ~0.20 |
| FE_Na | (U_Na × P_Cr)/(P_Na × U_Cr) | < 1% |
| NAE | TA + NH4+ - HCO3- | 50-100 mEq/day |
| C_H2O | V̇ - C_osm | -2 to +15 mL/min |


## Autoregulation & Tubuloglomerular Feedback (added v3.1.0)

RBF and GFR stay near-constant across ~80-180 mmHg perfusion pressure via a
fast myogenic response and slower tubuloglomerular feedback (Feher Unit 7 §7.6).

**Tubuloglomerular feedback** — `from scripts.renal.regulation import tubuloglomerular_feedback`

    SNGFR = SNGFR_min + (SNGFR_max - SNGFR_min) * K_half^n / (K_half^n + [NaCl]^n)

The macula densa senses distal NaCl delivery; rising delivery raises afferent
tone and lowers single-nephron GFR (descending sigmoid), stabilising delivery.

**Renal autoregulatory index** — `from scripts.renal.regulation import renal_autoregulation_index`

    AI = (%change RBF) / (%change MAP)

AI ~ 0 denotes effective autoregulation; AI ~ 1 denotes pressure-passive flow.


## Coverage-pass additions (Feher extraction)

4 equation(s) added to this domain, each verified against Feher and a worked example.

### Lean Body Mass (Behnke) (`lean_body_mass`)
- **Formula:** `LBM = TBW / 0.73`
- **LaTeX:** `\mathrm{LBM} = \dfrac{\mathrm{TBW}}{0.73}`
- **Import:** `from scripts.renal.compartments import lean_body_mass` — or `from scripts.canonical_ids import load; load('lean_body_mass')`
- **Feher:** §7.1 — THE TOTAL BODY WATER VARIES WITH BODY COMPOSITION
- Lean body mass estimated from total body water via Albert Behnke's body-composition partition.

### Glomerular Sieving Coefficient (`sieving_coefficient`)
- **Formula:** `Theta = C_B / C_P`
- **LaTeX:** `\Theta = \frac{C_{B}}{C_{P}}`
- **Import:** `from scripts.renal.glomerular import sieving_coefficient` — or `from scripts.canonical_ids import load; load('sieving_coefficient')`
- **Feher:** §7.3 — THE SIEVING COEFFICIENT DEPENDS MAINLY ON THE SLIT DIAPHRAGM
- Glomerular sieving coefficient: the ratio of a solute's concentration in Bowman's-space filtrate (C_B) to its concentration in glomerular-capillary plasma (C_P).

### MDRD Study Equation (eGFR) (`mdrd_gfr`)
- **Formula:** `GFR (mL/min) = 175 * [Cr]^(-1.154) * Age^(-0.203) * K`
- **LaTeX:** `\mathrm{GFR}\,(\mathrm{mL\,min^{-1}}/1.73\,\mathrm{m^2}) = 175 \times [\mathrm{Cr}]^{-1.154} \times \mathrm{Age}^{-0.203} \times K`
- **Import:** `from scripts.renal.clearance import mdrd_gfr` — or `from scripts.canonical_ids import load; load('mdrd_gfr')`
- **Feher:** §7.4 — PLASMA CREATININE CONCENTRATION ALONE INDICATES THE GFR
- Modification of Diet in Renal Disease (MDRD) Study equation: estimates glomerular filtration rate normalized to 1.73 m^2 body surface area from IDMS-standardized serum creatinine, age, and a group correction constant K (0.742 if female, 1.212 if African American).

### Fractional Water Reabsorption from (TF/P)inulin (`fractional_water_reabsorption`)
- **Formula:** `V_R/V_T = 1 - 1/(TF/P)_inulin`
- **LaTeX:** `\dfrac{V_R}{V_T} = 1 - \dfrac{1}{(\mathrm{TF}/P)_{inulin}}`
- **Import:** `from scripts.renal.tubular import fractional_water_reabsorption` — or `from scripts.canonical_ids import load; load('fractional_water_reabsorption')`
- **Feher:** §7.4 — (TF/P)inulin MARKS WATER REABSORPTION
- Fraction of filtered water reabsorbed from the glomerulus up to a tubular sampling point, inferred from the tubular-fluid-to-plasma inulin concentration ratio.



## Review additions (2026-07-15)

- **ttkg** — `TTKG = (U_K/P_K)/(U_osm/P_osm)` — Index of distal K+ secretory (aldosterone) drive; valid when U_osm>P_osm. Import: `from scripts.renal.clearance import ttkg_equation` (or `load("ttkg")`).
- **ckd_epi_2021** — `eGFR = 142*min(Scr/k,1)^a*max(Scr/k,1)^-1.2*0.9938^age*(1.012 F)` — Modern race-free creatinine eGFR (Inker NEJM 2021). Import: `from scripts.renal.clearance import ckd_epi_2021_equation` (or `load("ckd_epi_2021")`).

- **ckd_epi_2021** now accepts `S_Cr_units="umol/L"` (SI labs, e.g. Australian) with auto-conversion `/88.4`, matching mdrd_gfr / cockcroft_gault; unknown unit strings raise (no silent mg/dL fallback).

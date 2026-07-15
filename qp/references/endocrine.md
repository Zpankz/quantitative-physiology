---
name: endocrine
description: Endocrine physiology - hormone secretion, receptor binding, feedback regulation, hypothalamic-pituitary axis, thyroid, adrenal, pancreatic, calcium regulation, and reproductive hormones
parent: quantitative-physiology
unit: 9
---

# Endocrine Physiology

## Overview

This sub-skill covers the quantitative aspects of the endocrine system, including hormone secretion kinetics, receptor binding dynamics, feedback regulation, and metabolic control. The endocrine system coordinates physiological processes through chemical messengers that act at distant target sites.

## Core Concepts

### 1. Hormone Principles

#### Classification by Chemistry

| Class | Examples | Receptor Location | Mechanism |
|-------|----------|-------------------|-----------|
| Peptide/Protein | Insulin, GH, PTH | Cell surface | Second messengers |
| Steroid | Cortisol, estradiol, testosterone | Intracellular | Gene transcription |
| Amine | Epinephrine, T3/T4 | Surface or intracellular | Varies |
| Eicosanoid | Prostaglandins | Cell surface | Second messengers |

#### Hormone Transport

**Free hormone hypothesis**: Only free (unbound) hormone is biologically active.

**Binding equilibrium**:
Formula → qp:`hormone_kd`

**Fraction free**:
Formula → qp:`hormone_fraction_free`

Where:
- [H] = free hormone concentration
- [P] = binding protein concentration
- [HP] = bound hormone concentration
- K_d = dissociation constant

**Typical binding**: Cortisol 90-95% bound (CBG), T4 99.97% bound (TBG, albumin)

#### Hormone Clearance

**Metabolic clearance rate**:
Formula → qp:`metabolic_clearance_rate`

**Half-life**:
Formula → qp:`hormone_half_life`

Where V_d = volume of distribution, CL = clearance

**Typical half-lives**:
| Hormone | Half-life |
|---------|-----------|
| Epinephrine | 1-2 min |
| Insulin | 5-10 min |
| Cortisol | 60-90 min |
| T4 | 6-7 days |
| T3 | 1 day |

### 2. Receptor Binding Kinetics

#### Saturation Binding

**Equilibrium binding**:
Formula → qp:`receptor_saturation_binding`

Where:
- B = bound hormone
- B_max = maximum binding (receptor number × affinity)
- K_d = dissociation constant (concentration at 50% saturation)

**Scatchard analysis** (linearization):
Formula → qp:`scatchard_transform`

Plot of B/[H] vs B: slope = -1/K_d, x-intercept = B_max

#### Receptor Occupancy

**Fractional occupancy**:
Formula → qp:`receptor_fractional_occupancy`

**Spare receptors**: Many hormone systems achieve maximal response at <10% receptor occupancy.

**EC50 vs K_d**: EC50 (half-maximal effect) often < K_d due to signal amplification.

#### Signal Amplification

**Cascade amplification** (e.g., epinephrine → cAMP):
- 1 hormone molecule
- → ~100 G-protein activations
- → ~1000 adenylyl cyclase activations
- → ~10,000 cAMP molecules
- → ~100,000 kinase activations
- → ~1,000,000 substrate phosphorylations

### 3. Hypothalamic-Pituitary Axis

#### Feedback Regulation

**Negative feedback** (most common):
Formula → qp:`feedback_target_dynamics`, qp:`feedback_tropic_dynamics`

**Setpoint determination**:
At steady state: [Target]_ss = k_basal / k_fb

**Gain of feedback**:
Formula → qp:`feedback_gain`

High gain = tight regulation around setpoint.

#### Pulsatile Secretion

Many hormones secreted in pulses (GH, LH, cortisol).

**Pulse parameters**:
- Frequency: pulses per unit time
- Amplitude: peak height above baseline
- Area under curve (AUC): total secretion

**Circadian rhythms**: ~24-hour cycles
- Cortisol: peak 6-8 AM, nadir midnight
- GH: highest during slow-wave sleep
- Melatonin: peak at night

#### Hypothalamic Hormones

| Hormone | Target | Effect on Pituitary |
|---------|--------|---------------------|
| GnRH | Gonadotropes | ↑ LH, FSH |
| TRH | Thyrotropes | ↑ TSH (and PRL) |
| CRH | Corticotropes | ↑ ACTH |
| GHRH | Somatotropes | ↑ GH |
| Somatostatin | Multiple | ↓ GH, TSH |
| Dopamine | Lactotropes | ↓ Prolactin |

#### Pituitary Hormones

**Growth hormone (GH)**:
- Pulsatile release, mainly nocturnal
- Half-life: 15-20 minutes
- Actions: growth, lipolysis, anti-insulin
- IGF-1 mediates many effects (half-life ~15 hours)

**Prolactin**:
- Tonically inhibited by dopamine
- Stimulated by suckling, TRH, stress
- Half-life: ~20 minutes

### 4. Thyroid Function

#### Thyroid Hormone Synthesis

**Iodide trapping**: NIS (Na⁺/I⁻ symporter)
- Concentrates I⁻ 20-40× plasma levels
- TSH-stimulated

**Organification**: Thyroid peroxidase
```
I⁻ + H₂O₂ → I₀ (active iodine)
I₀ + Tyrosine → MIT (monoiodotyrosine)
MIT + I₀ → DIT (diiodotyrosine)
```

**Coupling**:
```
DIT + DIT → T4 (thyroxine)
MIT + DIT → T3 (triiodothyronine)
```

**T4/T3 ratio in thyroglobulin**: ~10:1

#### Thyroid Hormone Kinetics

**Daily production**:
- T4: ~80-100 μg/day (all from thyroid)
- T3: ~30-40 μg/day (20% thyroid, 80% peripheral conversion)

**Deiodinase enzymes**:
- D1: Liver, kidney - converts T4 → T3
- D2: Brain, pituitary - local T3 production
- D3: Placenta, brain - inactivates T4 → rT3

**TSH-thyroid axis model**:
Formula → qp:`thyroid_tsh_dynamics`, qp:`thyroid_t4_dynamics`

Where n ≈ 2 (steep feedback)

#### Reference Values

| Parameter | Normal Range |
|-----------|--------------|
| TSH | 0.4-4.0 mU/L |
| Free T4 | 0.8-1.8 ng/dL |
| Free T3 | 2.3-4.2 pg/mL |
| Total T4 | 4.5-12 μg/dL |
| Total T3 | 80-200 ng/dL |

### 5. Adrenal Function

#### Adrenal Cortex

**Zones and hormones**:
- Zona glomerulosa: Aldosterone (mineralocorticoid)
- Zona fasciculata: Cortisol (glucocorticoid)
- Zona reticularis: DHEA, androstenedione (androgens)

**Cortisol secretion**:
- Daily production: 10-20 mg/day
- Circadian rhythm: peak 6-8 AM, nadir midnight
- Stress response: 10× increase possible

**ACTH-cortisol axis**:
Formula → qp:`hpa_crh_dynamics`, qp:`hpa_acth_dynamics`, qp:`hpa_cortisol_dynamics`

**Aldosterone regulation**:
Primary stimuli:
- Angiotensin II (RAAS)
- Hyperkalemia (direct)
- ACTH (minor)

Formula → qp:`aldosterone_regulation`

**Aldosterone actions**:
- ↑ ENaC (Na⁺ reabsorption)
- ↑ ROMK (K⁺ secretion)
- ↑ Na⁺/K⁺-ATPase

#### Adrenal Medulla

**Catecholamine synthesis**:
```
Tyrosine → L-DOPA → Dopamine → Norepinephrine → Epinephrine
```

Rate-limiting: Tyrosine hydroxylase

**Catecholamine release**:
- Epinephrine: 80% of adrenal medullary output
- Norepinephrine: 20%
- Stimulated by sympathetic activation (ACh → nAChR)

**Half-life**: 1-2 minutes (rapid MAO/COMT metabolism)

**Receptor effects**:
| Receptor | Agonist | Primary Effect |
|----------|---------|----------------|
| α1 | NE > E | Vasoconstriction |
| α2 | NE > E | ↓ NE release (presynaptic) |
| β1 | E = NE | ↑ HR, contractility |
| β2 | E >> NE | Bronchodilation, vasodilation |
| β3 | NE > E | Lipolysis |

### 6. Pancreatic Endocrine Function

#### Islet Cell Types

| Cell Type | Hormone | % of Islet | Location |
|-----------|---------|------------|----------|
| β-cells | Insulin | 60-80% | Core |
| α-cells | Glucagon | 15-20% | Periphery |
| δ-cells | Somatostatin | 5-10% | Scattered |
| PP-cells | Pancreatic polypeptide | <5% | Periphery |

#### Insulin Secretion

**Glucose-stimulated insulin secretion (GSIS)**:
```
Glucose → GLUT2 → Glycolysis → ↑ATP/ADP → K_ATP closure → Depolarization → Ca²⁺ entry → Exocytosis
```

**Biphasic response**:
- First phase: 2-5 minutes, readily releasable pool
- Second phase: 10-60+ minutes, sustained secretion

**Dose-response**:
Formula → qp:`pancreatic_gsis`

Where:
- EC50 ≈ 5-6 mM glucose
- n ≈ 2-3 (sigmoidal)
- I_max ≈ 10× I_basal

**Potentiators of GSIS**:
- Incretins (GLP-1, GIP): 50-70% of postprandial insulin
- Amino acids (arginine, leucine)
- Fatty acids (acute)
- Sulfonylureas (K_ATP blockers)

#### Insulin Kinetics

**Secretion rate**: ~1 U/hour basal, 5-10 U/meal
**Half-life**: 5-10 minutes
**Clearance**: 50% first-pass hepatic

**Insulin sensitivity index**:
Formula → qp:`pancreatic_homa_ir`
(glucose in mmol/L, insulin in μU/mL)

Normal HOMA-IR: <2.5

#### Glucagon

**Secretion stimuli**:
- Hypoglycemia (primary)
- Amino acids
- Sympathetic activation (β-adrenergic)
- GIP

**Secretion inhibitors**:
- Hyperglycemia
- Insulin (paracrine)
- Somatostatin
- GLP-1

**Glucagon actions**:
- ↑ Hepatic glycogenolysis
- ↑ Gluconeogenesis
- ↑ Ketogenesis

**Glucose counterregulation**:
1. ↓ Insulin secretion (threshold ~80 mg/dL)
2. ↑ Glucagon (threshold ~65-70 mg/dL)
3. ↑ Epinephrine (threshold ~65-70 mg/dL)
4. ↑ Cortisol, GH (prolonged hypoglycemia)

### 7. Calcium and Phosphate Regulation

#### Calcium Distribution

**Total body calcium**: ~1000-1200 g
- 99% in bone (hydroxyapatite)
- 1% extracellular and intracellular

**Plasma calcium**: ~9-10.5 mg/dL (2.2-2.6 mM)
- 45% ionized (free) - physiologically active
- 40% protein-bound (mostly albumin)
- 15% complexed (citrate, phosphate)

**Albumin correction**:
Formula → qp:`calcium_albumin_correction`
(Ca in mg/dL, albumin in g/dL)

#### Parathyroid Hormone (PTH)

**PTH secretion**:
Formula → qp:`calcium_pth_secretion`

Where:
- K ≈ 1.0-1.2 mM (setpoint)
- n ≈ 3-4 (steep, sigmoidal)

**Calcium-sensing receptor (CaSR)**:
- ↑ Ca²⁺ → ↑ CaSR activation → ↓ PTH secretion
- Operates over narrow range (~0.8-1.3 mM ionized Ca²⁺)

**PTH actions**:
| Site | Effect | Mechanism |
|------|--------|-----------|
| Bone | ↑ Ca²⁺ release | Osteoclast activation (indirect) |
| Kidney | ↑ Ca²⁺ reabsorption | DCT calcium channels |
| Kidney | ↓ PO₄³⁻ reabsorption | ↓ NaPi-2a |
| Kidney | ↑ 1,25(OH)₂D synthesis | ↑ 1α-hydroxylase |

**PTH kinetics**:
- Half-life: 2-4 minutes (intact PTH)
- Pulsatile secretion
- Fragments: longer half-life, may have biological activity

#### Vitamin D

**Synthesis pathway**:
```
7-dehydrocholesterol → (UV-B) → Vitamin D3 (cholecalciferol)
→ (Liver 25-hydroxylase) → 25(OH)D (calcidiol)
→ (Kidney 1α-hydroxylase) → 1,25(OH)₂D (calcitriol)
```

**Regulation of 1α-hydroxylase**:
- Stimulators: PTH, hypophosphatemia
- Inhibitors: 1,25(OH)₂D (feedback), FGF23, hypercalcemia

**1,25(OH)₂D actions**:
- Intestine: ↑ Ca²⁺ and PO₄³⁻ absorption
- Bone: Permissive for PTH action
- Kidney: ↑ Ca²⁺ reabsorption (minor)
- PTH: ↓ PTH gene transcription

**Reference values**:
| Parameter | Normal Range |
|-----------|--------------|
| 25(OH)D | 30-100 ng/mL (sufficient) |
| 1,25(OH)₂D | 20-60 pg/mL |
| PTH (intact) | 10-65 pg/mL |

#### Calcitonin

**Source**: Thyroid C-cells (parafollicular)

**Secretion stimulus**: Hypercalcemia

**Actions** (relatively minor in humans):
- ↓ Osteoclast activity → ↓ bone resorption
- ↓ Renal Ca²⁺ reabsorption

**Clinical use**: Marker for medullary thyroid cancer

#### Phosphate Regulation

**Plasma phosphate**: 2.5-4.5 mg/dL (0.8-1.5 mM)

**FGF23** (fibroblast growth factor 23):
- Source: Osteocytes
- Stimulus: ↑ phosphate, ↑ 1,25(OH)₂D
- Actions:
  - ↓ NaPi-2a/2c → ↑ phosphate excretion
  - ↓ 1α-hydroxylase → ↓ 1,25(OH)₂D
  - Requires Klotho as co-receptor

### 8. Reproductive Hormones

#### Hypothalamic-Pituitary-Gonadal Axis

**GnRH**: Pulsatile release essential
- High frequency: favors LH
- Low frequency: favors FSH

**Gonadotropins**:
| Hormone | Target | Primary Action |
|---------|--------|----------------|
| FSH | Sertoli cells / Granulosa | Spermatogenesis / Follicle development |
| LH | Leydig cells / Theca | Testosterone / Androgen synthesis |

#### Testosterone

**Male production**: 5-7 mg/day (95% testicular)

**Circadian rhythm**: Peak morning, nadir evening

**Transport**:
- 44% SHBG-bound
- 54% albumin-bound
- 2% free

**5α-reductase**:
```
Testosterone → DHT (5× more potent)
```

**Aromatase**:
```
Testosterone → Estradiol
```

**Reference values (adult male)**:
| Parameter | Normal Range |
|-----------|--------------|
| Total testosterone | 300-1000 ng/dL |
| Free testosterone | 50-210 pg/mL |
| LH | 1.5-9.0 mU/mL |
| FSH | 1.5-12 mU/mL |

#### Estrogen and Progesterone

**Menstrual cycle phases**:
1. **Follicular phase** (days 1-14):
   - ↑ FSH → follicle development
   - ↑ Estradiol from growing follicle
   - Negative feedback on FSH

2. **Ovulation** (~day 14):
   - Estradiol surge → positive feedback → LH surge
   - LH surge triggers ovulation (~36 hours later)

3. **Luteal phase** (days 14-28):
   - Corpus luteum produces progesterone + estradiol
   - Prepares endometrium for implantation
   - If no pregnancy: luteolysis → ↓ hormones → menses

**Hormone levels across cycle**:
| Phase | Estradiol (pg/mL) | Progesterone (ng/mL) | LH (mU/mL) |
|-------|-------------------|----------------------|------------|
| Early follicular | 20-50 | <1 | 2-15 |
| Preovulatory | 200-400 | <1 | 20-100 |
| Mid-luteal | 100-200 | 5-20 | 2-15 |

**Progesterone effects**:
- ↑ Basal body temperature (~0.3°C)
- Secretory endometrium
- Breast development
- ↓ GnRH pulse frequency

## Computational Models

### Python Implementation

```python
import numpy as np
from scipy.integrate import odeint
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Physical constants
R = 8.314       # J/(mol·K)
T = 310         # K (37°C)

class HormoneBinding:
    """Receptor binding and hormone transport models"""

    @staticmethod
    def saturation_binding(H, Bmax, Kd):
        """
        Equilibrium binding (Langmuir isotherm)

        Parameters:
        -----------
        H : float or array - Free hormone concentration
        Bmax : float - Maximum binding capacity
        Kd : float - Dissociation constant

        Returns:
        --------
        B : Bound hormone concentration
        """
        return Bmax * H / (Kd + H)

    @staticmethod
    def fraction_free(protein_conc, Kd):
        """
        Fraction of hormone that is free (unbound)

        Parameters:
        -----------
        protein_conc : float - Binding protein concentration
        Kd : float - Dissociation constant

        Returns:
        --------
        f_free : Fraction free (0-1)
        """
        return 1 / (1 + protein_conc / Kd)

    @staticmethod
    def scatchard_transform(H, B):
        """
        Transform binding data for Scatchard plot

        Returns:
        --------
        B_over_H, B for plotting
        """
        return B / H, B

    @staticmethod
    def half_life_to_clearance(t_half, Vd):
        """
        Calculate clearance from half-life

        Parameters:
        -----------
        t_half : float - Half-life (same time units as desired CL)
        Vd : float - Volume of distribution

        Returns:
        --------
        CL : Clearance
        """
        return 0.693 * Vd / t_half


class HPAAxis:
    """Hypothalamic-Pituitary-Adrenal axis model"""

    def __init__(self, k_CRH=1.0, k_ACTH=0.5, k_cort=0.1,
                 k_fb_CRH=0.2, k_fb_ACTH=0.3):
        self.k_CRH = k_CRH
        self.k_ACTH = k_ACTH
        self.k_cort = k_cort
        self.k_fb_CRH = k_fb_CRH
        self.k_fb_ACTH = k_fb_ACTH

    def derivatives(self, y, t, stress=0):
        """
        HPA axis ODE system

        State variables:
        y[0] = CRH
        y[1] = ACTH
        y[2] = Cortisol
        """
        CRH, ACTH, cortisol = y

        # CRH: stress input, cortisol feedback
        dCRH = self.k_CRH * (1 + stress) - self.k_fb_CRH * cortisol - 0.5 * CRH

        # ACTH: CRH stimulation, cortisol feedback
        dACTH = self.k_ACTH * CRH - self.k_fb_ACTH * cortisol - 0.3 * ACTH

        # Cortisol: ACTH stimulation, clearance
        dCortisol = self.k_cort * ACTH - 0.1 * cortisol

        return [dCRH, dACTH, dCortisol]

    def simulate(self, duration=24, stress_times=None, stress_magnitude=2.0):
        """
        Simulate HPA axis with optional stress inputs

        Parameters:
        -----------
        duration : float - Simulation duration (hours)
        stress_times : list - Times of stress events
        stress_magnitude : float - Stress intensity multiplier
        """
        t = np.linspace(0, duration, 1000)
        y0 = [1.0, 1.0, 10.0]  # Initial conditions

        # Simple simulation without time-varying stress
        solution = odeint(self.derivatives, y0, t, args=(0,))

        return t, solution


class ThyroidAxis:
    """Thyroid hormone regulation model"""

    @staticmethod
    def tsh_response(fT4, Kd=1.0, n=2.0, TSH_max=10.0):
        """
        TSH as function of free T4 (negative feedback)

        Parameters:
        -----------
        fT4 : float - Free T4 concentration
        Kd : float - Feedback setpoint
        n : float - Hill coefficient (steepness)
        TSH_max : float - Maximum TSH

        Returns:
        --------
        TSH : TSH concentration
        """
        return TSH_max / (1 + (fT4 / Kd) ** n)

    @staticmethod
    def t4_production(TSH, Vmax=100, Km=2.0):
        """
        T4 production rate as function of TSH
        """
        return Vmax * TSH / (Km + TSH)

    @staticmethod
    def t4_to_t3_conversion(T4, D1_activity=1.0, D3_activity=0.1):
        """
        T4 conversion to T3 and rT3

        Returns:
        --------
        T3, rT3 : Production rates
        """
        T3 = D1_activity * T4
        rT3 = D3_activity * T4
        return T3, rT3


class InsulinGlucose:
    """Insulin-glucose regulation model"""

    @staticmethod
    def glucose_stimulated_insulin(glucose, I_basal=5, I_max=50,
                                    EC50=6.0, n=2.5):
        """
        Insulin secretion as function of glucose

        Parameters:
        -----------
        glucose : float - Blood glucose (mM)
        I_basal : float - Basal insulin secretion rate
        I_max : float - Maximum insulin above basal
        EC50 : float - Glucose for half-maximal response
        n : float - Hill coefficient

        Returns:
        --------
        Insulin secretion rate
        """
        stim = glucose ** n / (EC50 ** n + glucose ** n)
        return I_basal + I_max * stim

    @staticmethod
    def incretin_effect(GLP1, glucose, I_base,
                        EC50_GLP1=10, glucose_threshold=5):
        """
        GLP-1 potentiation of insulin secretion
        (glucose-dependent)
        """
        if glucose < glucose_threshold:
            return 0
        potentiation = 1 + GLP1 / (EC50_GLP1 + GLP1)
        return I_base * potentiation

    @staticmethod
    def HOMA_IR(fasting_glucose_mmol, fasting_insulin_uU):
        """
        Calculate HOMA-IR insulin resistance index

        Normal < 2.5
        """
        return (fasting_glucose_mmol * fasting_insulin_uU) / 22.5

    @staticmethod
    def glucose_disposal(glucose, insulin, Vmax=10, Km_glucose=5,
                         insulin_sensitivity=1.0):
        """
        Glucose uptake by tissues (insulin-dependent)
        """
        insulin_effect = insulin_sensitivity * insulin / (10 + insulin)
        return Vmax * glucose / (Km_glucose + glucose) * (1 + insulin_effect)

    def minimal_model(self, y, t, G_input=0):
        """
        Bergman minimal model for glucose-insulin dynamics

        State variables:
        y[0] = G (glucose)
        y[1] = X (insulin action)
        y[2] = I (insulin)
        """
        G, X, I = y

        # Parameters
        p1 = 0.03   # Glucose effectiveness
        p2 = 0.02   # Rate of insulin action decay
        p3 = 5e-5   # Insulin sensitivity
        n = 0.2     # Insulin clearance
        Gb = 5.0    # Basal glucose
        Ib = 10.0   # Basal insulin

        # Glucose dynamics
        dG = -p1 * (G - Gb) - X * G + G_input

        # Insulin action compartment
        dX = -p2 * X + p3 * (I - Ib)

        # Insulin dynamics (simplified)
        if G > Gb:
            I_secretion = 0.5 * (G - Gb)
        else:
            I_secretion = 0
        dI = I_secretion - n * I

        return [dG, dX, dI]


class CalciumRegulation:
    """Calcium-PTH-Vitamin D regulation"""

    @staticmethod
    def pth_secretion(Ca_ionized, PTH_max=65, K=1.1, n=3.5):
        """
        PTH secretion as function of ionized calcium
        (inverse sigmoidal - calcium inhibits PTH)

        Parameters:
        -----------
        Ca_ionized : float - Ionized calcium (mM)
        PTH_max : float - Maximum PTH (pg/mL)
        K : float - Calcium setpoint (mM)
        n : float - Hill coefficient
        """
        return PTH_max * K ** n / (K ** n + Ca_ionized ** n)

    @staticmethod
    def calcium_correction(measured_Ca, albumin):
        """
        Albumin-corrected calcium

        Parameters:
        -----------
        measured_Ca : float - Measured total calcium (mg/dL)
        albumin : float - Serum albumin (g/dL)

        Returns:
        --------
        Corrected calcium (mg/dL)
        """
        return measured_Ca + 0.8 * (4.0 - albumin)

    @staticmethod
    def vitamin_d_activation(PTH, phosphate, FGF23,
                              k_PTH=1.0, k_phos=0.5, k_FGF23=0.3):
        """
        1,25(OH)2D production rate from 25(OH)D

        Stimulated by PTH and hypophosphatemia
        Inhibited by FGF23
        """
        stim = k_PTH * PTH + k_phos / (phosphate + 0.1)
        inhib = 1 + k_FGF23 * FGF23
        return stim / inhib

    @staticmethod
    def bone_calcium_flux(PTH, calcitonin, vitamin_D):
        """
        Net calcium flux from bone (resorption - formation)

        Positive = net release from bone
        """
        resorption = PTH * (1 + 0.2 * vitamin_D)
        formation = 0.5 + 0.1 * calcitonin
        return resorption - formation


class ReproductiveHormones:
    """Reproductive hormone models"""

    @staticmethod
    def lh_surge(estradiol, threshold=200, max_LH=80, baseline=5):
        """
        LH response to estradiol (positive feedback at high E2)

        Parameters:
        -----------
        estradiol : float - Estradiol (pg/mL)
        threshold : float - E2 threshold for positive feedback
        """
        if estradiol < threshold:
            # Negative feedback
            return baseline * threshold / (threshold + estradiol)
        else:
            # Positive feedback (surge)
            excess = estradiol - threshold
            return baseline + max_LH * excess / (50 + excess)

    @staticmethod
    def progesterone_temperature(progesterone, T_baseline=36.5):
        """
        Basal body temperature elevation from progesterone

        Parameters:
        -----------
        progesterone : float - Progesterone (ng/mL)

        Returns:
        --------
        Temperature (°C)
        """
        delta_T = 0.3 * progesterone / (5 + progesterone)
        return T_baseline + delta_T

    @staticmethod
    def follicle_growth(FSH, day, k_growth=0.1):
        """
        Simplified follicle size model

        Returns:
        --------
        Follicle diameter (mm)
        """
        # Exponential growth modulated by FSH
        return 5 * np.exp(k_growth * FSH * day)

    def menstrual_cycle_model(self, t):
        """
        Simplified menstrual cycle hormone profiles

        Parameters:
        -----------
        t : float - Day of cycle (1-28)

        Returns:
        --------
        E2, P4, LH, FSH concentrations
        """
        # Estradiol: rises in follicular, peak at ovulation, moderate in luteal
        if t < 12:
            E2 = 30 + 20 * t  # Rising follicular
        elif t < 15:
            E2 = 300 * np.exp(-((t - 14) ** 2) / 2)  # Ovulatory peak
        else:
            E2 = 100 + 50 * np.exp(-(t - 21) ** 2 / 20)  # Luteal

        # Progesterone: low until ovulation, high in luteal
        if t < 14:
            P4 = 0.5
        else:
            P4 = 15 * np.exp(-((t - 21) ** 2) / 30)

        # LH: surge at day 14
        LH = 5 + 80 * np.exp(-((t - 14) ** 2) / 2)

        # FSH: elevated early, suppressed mid, slight rise late
        FSH = 8 - 4 * np.sin(np.pi * t / 28) + 3 * np.exp(-((t - 2) ** 2) / 10)

        return E2, P4, LH, FSH


class EndocrineModel:
    """Integrated endocrine system model"""

    def __init__(self):
        self.hpa = HPAAxis()
        self.thyroid = ThyroidAxis()
        self.insulin_glucose = InsulinGlucose()
        self.calcium = CalciumRegulation()
        self.reproductive = ReproductiveHormones()

    def stress_response(self, stress_level, duration_hours=4):
        """
        Simulate stress response across multiple axes
        """
        # Cortisol response
        t, hpa_solution = self.hpa.simulate(duration=duration_hours)
        cortisol = hpa_solution[:, 2]

        # Glucose elevation from stress
        glucose_baseline = 5.0  # mM
        glucose = glucose_baseline * (1 + 0.3 * stress_level * np.exp(-t / 2))

        # Insulin response
        insulin = np.array([
            self.insulin_glucose.glucose_stimulated_insulin(g)
            for g in glucose
        ])

        return {
            'time': t,
            'cortisol': cortisol,
            'glucose': glucose,
            'insulin': insulin
        }


# Example usage and visualization
if __name__ == "__main__":
    # Initialize model
    model = EndocrineModel()

    # Example: Glucose-insulin response
    glucose_range = np.linspace(2, 20, 100)
    insulin = model.insulin_glucose.glucose_stimulated_insulin(glucose_range)

    plt.figure(figsize=(10, 6))
    plt.plot(glucose_range, insulin, 'b-', linewidth=2)
    plt.xlabel('Blood Glucose (mM)')
    plt.ylabel('Insulin Secretion Rate (μU/mL/min)')
    plt.title('Glucose-Stimulated Insulin Secretion')
    plt.axvline(5.6, color='g', linestyle='--', label='Normal fasting')
    plt.axhline(model.insulin_glucose.glucose_stimulated_insulin(5.6),
                color='g', linestyle='--')
    plt.legend()
    plt.grid(True)
    plt.savefig('gsis_curve.png', dpi=150)
```

### Julia Implementation

```julia
using DifferentialEquations
using Plots

# Physical constants
const R = 8.314    # J/(mol·K)
const T = 310.0    # K (37°C)

module HormoneBinding

"""
    saturation_binding(H, Bmax, Kd)

Equilibrium receptor binding (Langmuir isotherm).
"""
function saturation_binding(H, Bmax, Kd)
    return Bmax * H / (Kd + H)
end

"""
    fraction_free(protein_conc, Kd)

Fraction of hormone that is free (unbound).
"""
function fraction_free(protein_conc, Kd)
    return 1 / (1 + protein_conc / Kd)
end

"""
    receptor_occupancy(H, Kd)

Fractional receptor occupancy at given hormone concentration.
"""
function receptor_occupancy(H, Kd)
    return H / (Kd + H)
end

end  # module HormoneBinding


module HPAAxis

"""
    hpa_ode!(du, u, p, t)

HPA axis ODE system.
u = [CRH, ACTH, Cortisol]
"""
function hpa_ode!(du, u, p, t)
    CRH, ACTH, cortisol = u
    k_CRH, k_ACTH, k_cort, k_fb_CRH, k_fb_ACTH, stress = p

    # CRH dynamics
    du[1] = k_CRH * (1 + stress) - k_fb_CRH * cortisol - 0.5 * CRH

    # ACTH dynamics
    du[2] = k_ACTH * CRH - k_fb_ACTH * cortisol - 0.3 * ACTH

    # Cortisol dynamics
    du[3] = k_cort * ACTH - 0.1 * cortisol
end

"""
    simulate_hpa(duration; stress=0.0)

Simulate HPA axis for given duration (hours).
"""
function simulate_hpa(duration; stress=0.0)
    u0 = [1.0, 1.0, 10.0]  # Initial conditions
    p = (1.0, 0.5, 0.1, 0.2, 0.3, stress)
    tspan = (0.0, duration)

    prob = ODEProblem(hpa_ode!, u0, tspan, p)
    sol = solve(prob, Tsit5(), saveat=0.1)

    return sol
end

"""
    circadian_cortisol(t_hours)

Simple circadian cortisol model (peak ~6-8 AM).
"""
function circadian_cortisol(t_hours)
    # Cosine with peak at 6 AM (t=6)
    baseline = 12.0  # μg/dL
    amplitude = 8.0
    return baseline + amplitude * cos(2π * (t_hours - 6) / 24)
end

end  # module HPAAxis


module ThyroidAxis

"""
    tsh_response(fT4; Kd=1.0, n=2.0, TSH_max=10.0)

TSH as function of free T4 (negative feedback).
"""
function tsh_response(fT4; Kd=1.0, n=2.0, TSH_max=10.0)
    return TSH_max / (1 + (fT4 / Kd)^n)
end

"""
    t4_production(TSH; Vmax=100.0, Km=2.0)

T4 production rate as function of TSH.
"""
function t4_production(TSH; Vmax=100.0, Km=2.0)
    return Vmax * TSH / (Km + TSH)
end

"""
    thyroid_ode!(du, u, p, t)

Thyroid axis ODE system.
u = [TSH, T4, T3]
"""
function thyroid_ode!(du, u, p, t)
    TSH, T4, T3 = u
    TRH, k_clear_TSH, k_clear_T4, k_clear_T3, k_convert = p

    # TSH: TRH stimulation, T3/T4 feedback
    du[1] = TRH - k_clear_TSH * TSH - 0.5 * T3 - 0.1 * T4

    # T4: TSH stimulation, conversion to T3, clearance
    du[2] = t4_production(TSH) - k_convert * T4 - k_clear_T4 * T4

    # T3: conversion from T4, clearance
    du[3] = k_convert * T4 - k_clear_T3 * T3
end

end  # module ThyroidAxis


module InsulinGlucose

"""
    gsis(glucose; I_basal=5.0, I_max=50.0, EC50=6.0, n=2.5)

Glucose-stimulated insulin secretion (Hill function).
"""
function gsis(glucose; I_basal=5.0, I_max=50.0, EC50=6.0, n=2.5)
    stim = glucose^n / (EC50^n + glucose^n)
    return I_basal + I_max * stim
end

"""
    homa_ir(fasting_glucose_mmol, fasting_insulin_uU)

HOMA-IR insulin resistance index.
Normal < 2.5
"""
function homa_ir(fasting_glucose_mmol, fasting_insulin_uU)
    return (fasting_glucose_mmol * fasting_insulin_uU) / 22.5
end

"""
    minimal_model!(du, u, p, t)

Bergman minimal model for glucose-insulin dynamics.
u = [G, X, I] (glucose, insulin action, insulin)
"""
function minimal_model!(du, u, p, t)
    G, X, I = u
    p1, p2, p3, n, Gb, Ib, G_input = p

    # Glucose dynamics
    du[1] = -p1 * (G - Gb) - X * G + G_input

    # Insulin action compartment
    du[2] = -p2 * X + p3 * max(0, I - Ib)

    # Insulin dynamics
    I_secretion = G > Gb ? 0.5 * (G - Gb) : 0.0
    du[3] = I_secretion - n * I
end

"""
    simulate_ogtt(glucose_dose=75.0)

Simulate oral glucose tolerance test.
"""
function simulate_ogtt(glucose_dose=75.0)
    u0 = [5.0, 0.0, 10.0]  # Fasting glucose, X, insulin

    # Parameters: p1, p2, p3, n, Gb, Ib, G_input
    # G_input as impulse at t=0 would need different handling
    p = (0.03, 0.02, 5e-5, 0.2, 5.0, 10.0, 0.0)

    tspan = (0.0, 180.0)  # 3 hours
    prob = ODEProblem(minimal_model!, u0, tspan, p)

    # Add glucose input at t=0 (simplified as initial condition change)
    u0_post_glucose = [5.0 + glucose_dose / 10, 0.0, 10.0]
    prob_post = ODEProblem(minimal_model!, u0_post_glucose, tspan, p)
    sol = solve(prob_post, Tsit5(), saveat=5.0)

    return sol
end

end  # module InsulinGlucose


module CalciumRegulation

"""
    pth_secretion(Ca_ionized; PTH_max=65.0, K=1.1, n=3.5)

PTH secretion as inverse function of ionized calcium.
"""
function pth_secretion(Ca_ionized; PTH_max=65.0, K=1.1, n=3.5)
    return PTH_max * K^n / (K^n + Ca_ionized^n)
end

"""
    calcium_correction(measured_Ca, albumin)

Albumin-corrected calcium.
"""
function calcium_correction(measured_Ca, albumin)
    return measured_Ca + 0.8 * (4.0 - albumin)
end

"""
    calcium_ode!(du, u, p, t)

Calcium-PTH-VitD regulation ODE.
u = [Ca, PTH, VitD]
"""
function calcium_ode!(du, u, p, t)
    Ca, PTH, VitD = u
    k_bone, k_renal, k_intestine, k_clear_PTH, k_clear_VitD = p

    # PTH dynamics (calcium feedback)
    PTH_secretion = pth_secretion(Ca)
    du[2] = PTH_secretion - k_clear_PTH * PTH

    # Vitamin D activation (PTH stimulates)
    VitD_production = 0.1 * PTH
    du[3] = VitD_production - k_clear_VitD * VitD

    # Calcium dynamics
    bone_flux = k_bone * PTH
    renal_reabsorption = k_renal * PTH
    intestinal_absorption = k_intestine * VitD
    du[1] = bone_flux + intestinal_absorption + renal_reabsorption - 0.1 * Ca
end

end  # module CalciumRegulation


module ReproductiveHormones

"""
    lh_surge(estradiol; threshold=200.0, max_LH=80.0, baseline=5.0)

LH response to estradiol (switches from negative to positive feedback).
"""
function lh_surge(estradiol; threshold=200.0, max_LH=80.0, baseline=5.0)
    if estradiol < threshold
        # Negative feedback
        return baseline * threshold / (threshold + estradiol)
    else
        # Positive feedback (surge)
        excess = estradiol - threshold
        return baseline + max_LH * excess / (50 + excess)
    end
end

"""
    menstrual_cycle(day)

Simplified menstrual cycle hormone profiles.
Returns (E2, P4, LH, FSH) at given cycle day (1-28).
"""
function menstrual_cycle(day)
    # Estradiol
    if day < 12
        E2 = 30 + 20 * day
    elseif day < 15
        E2 = 300 * exp(-((day - 14)^2) / 2)
    else
        E2 = 100 + 50 * exp(-((day - 21)^2) / 20)
    end

    # Progesterone
    P4 = day < 14 ? 0.5 : 15 * exp(-((day - 21)^2) / 30)

    # LH surge
    LH = 5 + 80 * exp(-((day - 14)^2) / 2)

    # FSH
    FSH = 8 - 4 * sin(π * day / 28) + 3 * exp(-((day - 2)^2) / 10)

    return (E2=E2, P4=P4, LH=LH, FSH=FSH)
end

"""
    ovulation_timing(estradiol_series, time_series)

Predict ovulation timing from estradiol measurements.
Ovulation ~24-36 hours after E2 peak.
"""
function ovulation_timing(estradiol_series, time_series)
    peak_idx = argmax(estradiol_series)
    peak_time = time_series[peak_idx]
    return peak_time + 1.5  # ~36 hours after peak
end

end  # module ReproductiveHormones


# Example: Plot menstrual cycle hormones
function plot_menstrual_cycle()
    days = 1:0.5:28
    E2 = Float64[]
    P4 = Float64[]
    LH = Float64[]
    FSH = Float64[]

    for d in days
        hormones = ReproductiveHormones.menstrual_cycle(d)
        push!(E2, hormones.E2)
        push!(P4, hormones.P4)
        push!(LH, hormones.LH)
        push!(FSH, hormones.FSH)
    end

    p1 = plot(days, E2, label="Estradiol (pg/mL)", color=:red, linewidth=2)
    plot!(days, P4 * 10, label="Progesterone ×10 (ng/mL)", color=:purple, linewidth=2)

    p2 = plot(days, LH, label="LH (mU/mL)", color=:blue, linewidth=2)
    plot!(days, FSH, label="FSH (mU/mL)", color=:green, linewidth=2)

    plot(p1, p2, layout=(2, 1), xlabel="Cycle Day",
         title="Menstrual Cycle Hormones")
end
```

## Problem-Solving Approach

### Step-by-Step Method

1. **Identify the endocrine axis**: Which hormones and organs are involved?
2. **Determine the regulation type**: Negative feedback, positive feedback, or permissive?
3. **List known quantities** with units
4. **Select appropriate model**: Binding, kinetics, or dynamic ODE
5. **Apply equations and calculate**
6. **Interpret in physiological context**
7. **Consider clinical implications**

### Typical Problems

**Type 1: Hormone-receptor binding**
- Given: Hormone concentration, receptor parameters
- Find: Occupancy, response magnitude, or dose-response curve

**Type 2: Feedback regulation**
- Given: Stimulus or perturbation
- Find: Steady-state hormone levels, response kinetics

**Type 3: Clearance/kinetics**
- Given: Half-life, production rate, or concentration data
- Find: Clearance rate, steady-state level, or time course

**Type 4: Clinical interpretation**
- Given: Laboratory values
- Find: Diagnosis, mechanism, or expected compensatory changes

## Clinical Correlations

| Condition | Primary Defect | Expected Lab Pattern |
|-----------|----------------|----------------------|
| Primary hypothyroidism | ↓ T4 production | ↑↑ TSH, ↓ fT4 |
| Secondary hypothyroidism | ↓ TSH production | ↓ TSH, ↓ fT4 |
| Graves' disease | TSH receptor antibodies | ↓↓ TSH, ↑ fT4 |
| Primary hyperparathyroidism | PTH adenoma | ↑ PTH, ↑ Ca²⁺ |
| Secondary hyperparathyroidism | Chronic hypocalcemia | ↑↑ PTH, ↓ or normal Ca²⁺ |
| Addison's disease | Adrenal insufficiency | ↑ ACTH, ↓ cortisol |
| Cushing's syndrome | Excess cortisol | Varies by etiology |
| Type 1 diabetes | β-cell destruction | ↓↓ insulin, ↑ glucose |
| Type 2 diabetes | Insulin resistance | ↑ insulin (early), ↑ glucose |
| PCOS | Androgen excess | ↑ LH/FSH ratio, ↑ androgens |
| Hypogonadism | ↓ Sex steroids | ↑ FSH/LH (primary), ↓ (secondary) |

## Key Relationships Summary

| System | Driving Force | Response |
|--------|---------------|----------|
| HPT axis | ↓ T4/T3 | ↑ TSH secretion |
| HPA axis | Stress, ↓ cortisol | ↑ CRH, ↑ ACTH |
| Calcium-PTH | ↓ Ca²⁺ | ↑ PTH secretion |
| Insulin-glucose | ↑ Glucose | ↑ Insulin secretion |
| HPG axis (female) | ↑↑ Estradiol | LH surge (positive feedback) |
| HPG axis (male) | ↓ Testosterone | ↑ LH secretion |

**Unifying principle**: Most endocrine axes use negative feedback to maintain homeostasis, with specific exceptions (LH surge, milk ejection) employing positive feedback for trigger-like responses.


## Coverage-pass additions (Feher extraction)

3 equation(s) added to this domain, each verified against Feher and a worked example.

### Cheng-Prusoff Equation (Ki from IC50) (`cheng_prusoff_ki`)
- **Formula:** `K_i = IC_50 / (1 + [L]/K_d)`
- **LaTeX:** `K_i = \dfrac{\mathrm{IC}_{50}}{1 + \dfrac{[L]}{K_d}}`
- **Import:** `from scripts.endocrine.receptor import cheng_prusoff_ki` — or `from scripts.canonical_ids import load; load('cheng_prusoff_ki')`
- **Feher:** §9.1 — Competitive Inhibition of Binding
- Cheng-Prusoff equation for competitive inhibition of binding.

### Competitive Inhibition of Binding (`competitive_inhibition_binding`)
- **Formula:** `B = B_max*[L] / ([L] + K_d*(1 + [I]/K_i))`
- **LaTeX:** `B = \dfrac{B_{max}\,[L]}{[L] + K_d\left(1 + \dfrac{[I]}{K_i}\right)}`
- **Import:** `from scripts.endocrine.receptor import competitive_inhibition_binding` — or `from scripts.canonical_ids import load; load('competitive_inhibition_binding')`
- **Feher:** §9.1 — COMPETITIVE INHIBITION OF BINDING (Appendix 9.1.A1 Analysis of Ligand Binding)
- Bound ligand at equilibrium when a competitive inhibitor occupies the same binding site as the ligand.

### Beer–Lambert Attenuation (X-ray) (`beer_lambert_attenuation`)
- **Formula:** `I = I_0 * exp(-mu * x)`
- **LaTeX:** `I = I_0\, e^{-\mu x}`
- **Import:** `from scripts.endocrine.calcium import beer_lambert_attenuation` — or `from scripts.canonical_ids import load; load('beer_lambert_attenuation')`
- **Feher:** §9.8 — Clinical Applications: Dual Energy X-ray Absorptiometry and Bone Density
- Beer-Lambert law of radiation attenuation: transmitted intensity of an X-ray (or gamma) beam after passing through thickness x of an absorber with linear attenuation coefficient mu.



## Review additions (2026-07-15)

- **pancreatic_homa_b** — `HOMA-B = 20 x Insulin / (Glucose_mmol - 3.5)` — Fasting beta-cell function index (%), companion to HOMA-IR. Import: `from scripts.endocrine.pancreatic import pancreatic_homa_b_equation` (or `load("pancreatic_homa_b")`).

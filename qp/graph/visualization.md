# Equation Dependency Visualization

## Unit Dependency DAG

```mermaid
flowchart TD
    subgraph "Layer 0: Foundations"
        U1[Unit 1: Physical Foundations<br/>20 equations]
    end

    subgraph "Layer 1: Membrane"
        U2[Unit 2: Membranes & Transport<br/>18 equations]
    end

    subgraph "Layer 2: Excitable"
        U3[Unit 3: Excitable Cells<br/>22 equations]
    end

    subgraph "Layer 3: Systems"
        U4[Unit 4: Nervous System<br/>27 equations]
        U5[Unit 5: Cardiovascular<br/>31 equations]
        U8[Unit 8: Gastrointestinal<br/>34 equations]
    end

    subgraph "Layer 4: Integration"
        U6[Unit 6: Respiratory<br/>41 equations]
        U7[Unit 7: Renal<br/>30 equations]
        U9[Unit 9: Endocrine<br/>25 equations]
    end

    U1 --> U2
    U1 --> U3
    U2 --> U3
    U1 --> U4
    U2 --> U4
    U3 --> U4
    U1 --> U5
    U2 --> U5
    U3 --> U5
    U1 --> U6
    U5 --> U6
    U1 --> U7
    U5 --> U7
    U6 --> U7
    U1 --> U8
    U2 --> U8
    U1 --> U9
    U2 --> U9
    U7 --> U9
    U8 --> U9
```

## Cross-Domain Equation Flow

```mermaid
flowchart LR
    subgraph Foundations
        NE[Nernst Equation]
        FD[Fick Diffusion]
        PF[Poiseuille Flow]
        LL[Laplace Law]
        MM[Michaelis-Menten]
        HE[Hill Equation]
        HH_eq[Henderson-Hasselbalch]
    end

    subgraph Membrane
        GHK[Goldman-Hodgkin-Katz]
        DP[Donnan Potential]
    end

    subgraph Excitable
        HH[Hodgkin-Huxley]
        CE[Cable Equation]
        HFV[Hill Force-Velocity]
    end

    subgraph Cardiovascular
        CO[Cardiac Output]
        SF[Starling Forces]
        OD[Oxygen Delivery]
    end

    subgraph Respiratory
        AGE[Alveolar Gas Eq]
        OC[Oxygen Content]
        DC[Diffusing Capacity]
    end

    subgraph Renal
        GFR[GFR Calculation]
        CL[Clearance]
        NAE[Net Acid Excretion]
    end

    NE --> GHK
    NE --> DP
    GHK --> HH
    HH --> CE
    FD --> DC
    FD --> GFR
    PF --> CO
    PF --> GFR
    LL --> AGE
    HE --> OC
    HE --> HFV
    MM --> CL
    HH_eq --> NAE
    SF --> GFR
    CO --> OD
    OC --> OD
```

## Topological Layers

```mermaid
graph TB
    subgraph "Layer 4: Systems Integration"
        L4A[Oxygen Delivery]
        L4B[Acid-Base Compensation]
        L4C[Hormone Feedback Loops]
    end

    subgraph "Layer 3: Organ Function"
        L3A[Cardiac Output]
        L3B[Alveolar Gas Exchange]
        L3C[GFR Calculation]
        L3D[Synaptic Current]
    end

    subgraph "Layer 2: Excitable Tissue"
        L2A[HH Membrane Current]
        L2B[Cable Equation]
        L2C[Hill Force-Velocity]
    end

    subgraph "Layer 1: Membrane Properties"
        L1A[Membrane Capacitance]
        L1B[Donnan Potential]
        L1C[Goldman-Hodgkin-Katz]
        L1D[Osmotic Pressure]
    end

    subgraph "Layer 0: Physical Foundations"
        L0A[Gibbs Free Energy]
        L0B[Coulomb's Law]
        L0C[Diffusion Coefficient]
        L0D[Volume Flux]
        L0E[Nernst Equation]
    end

    L0A --> L1B
    L0E --> L1B
    L0E --> L1C
    L0B --> L1A
    L0C --> L1D
    L0D --> L1D

    L1A --> L2A
    L1C --> L2A
    L2A --> L2B

    L2A --> L3D
    L2B --> L3A
    L2C --> L3A

    L3A --> L4A
    L3B --> L4A
    L3C --> L4B
    L3D --> L4C
```

## Functional Clusters

```mermaid
mindmap
    root((Physiology<br/>248 Equations))
        Transport & Flow
            Poiseuille
            Hydraulic Resistance
            Laplace Cylinder
            Laplace Sphere
            TPR
            Airway Resistance
        Electrochemical
            Nernst
            Donnan
            GHK
            Chord Conductance
        Excitation-Contraction
            HH Current
            Cable Equation
            Ca-Force
            Hill F-V
            ESPVR
        Oxygen Cascade
            Alveolar Gas
            Diffusing Capacity
            Hill Saturation
            O2 Content
            O2 Delivery
            Fick Principle
        Acid-Base
            Henderson-Hasselbalch
            Anion Gap
            Winters Formula
            NAE
            HCO3 Generation
        Renal Function
            NFP
            GFR
            Clearance
            Filtered Load
            FE
            Starling
        Hormone Kinetics
            Kd
            MCR
            Occupancy
            Feedback Gain
            Receptor Binding
        Synaptic
            Quantal Content
            Synaptic Current
            EPSP
            STDP
            Safety Factor
        GI Function
            Gastric Acid
            Enzyme Kinetics
            SGLT1
            Hepatic Clearance
            Incretin Effect
        CV Regulation
            Cardiac Output
            MAP
            Baroreceptor
            Compliance
            ADH
```

## Dependency Chain Details

### Membrane to Action Potential Chain
```mermaid
sequenceDiagram
    participant NE as Nernst Equation
    participant GHK as Goldman-Hodgkin-Katz
    participant HH as HH Membrane Current
    participant Na as HH Sodium Current
    participant K as HH Potassium Current

    NE->>GHK: Ion equilibrium potentials
    GHK->>HH: Resting membrane potential
    HH->>Na: Voltage-gated activation
    HH->>K: Delayed rectification
    Na-->>HH: Depolarization phase
    K-->>HH: Repolarization phase
```

### Cardiovascular Oxygen Cascade
```mermaid
sequenceDiagram
    participant HS as Hill Saturation
    participant OC as Oxygen Content
    participant OD as Oxygen Delivery
    participant CO as Cardiac Output
    participant FP as Fick Principle

    HS->>OC: Hb saturation → CaO2
    OC->>OD: CaO2 × blood flow
    CO->>OD: Flow component
    OD->>FP: VO2 = CO × (CaO2-CvO2)
    FP-->>CO: Cardiac demand feedback
```

### Renal Clearance Chain
```mermaid
sequenceDiagram
    participant RPF as Renal Plasma Flow
    participant FF as Filtration Fraction
    participant GFR as GFR from NFP
    participant CL as Clearance
    participant FE as Fractional Excretion

    RPF->>FF: Flow input
    GFR->>FF: FF = GFR/RPF
    GFR->>CL: Filtered load
    CL->>FE: Excretion/Filtration
    FE-->>CL: Reabsorption assessment
```

## Summary Statistics

| Metric | Count |
|--------|-------|
| Total Equations | 248 |
| Physiological Units | 9 |
| Functional Clusters | 10 |
| Cross-Domain Equations | 10 |
| Dependency Chains | 5 |
| Topological Layers | 5 |

## Navigation

- **By Unit**: Use `dependency-graph.json` → `units` section
- **By Cluster**: Use `clusters.json` → `clusters` section
- **By Dependency**: Use `dependency-graph.json` → `cross_domain_equations`
- **By Chain**: Use `dependency-graph.json` → `dependency_chains`

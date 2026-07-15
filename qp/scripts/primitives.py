"""Universal primitives — the handful of functional FORMS that recur across the
corpus in varied physiological context.

The claim this module makes precise and *provable*: many named equations that look
unrelated are the same fundamental concept in a different context — Nernst,
Henderson–Hasselbalch, Gibbs and Donnan are all one *log-of-a-ratio* form;
Michaelis–Menten, Hill, receptor occupancy and SGLT transport are all one
*saturation* form; drug elimination, gastric emptying and membrane charging are
all one *first-order exponential*. So a study agent (or another Primary-Exam
skill) can reason from ~7 intuitions instead of hundreds of separate rules.

Grounding discipline (this is NOT a re-labelling):
  * Each primitive is a KERNEL function — the universal form.
  * An equation is a MEMBER iff the kernel, given a curated binding of that
    equation's own parameters, REPRODUCES ``equation.compute()`` to tolerance.
    Membership is therefore proven by execution, exactly like a value anchor —
    not asserted by a hand-tag or a regex over the formula string.
  * No equation is collapsed, renamed or deleted. Every named equation stays the
    authority (its constants, units and identity are physiological, not shared);
    the primitive only exposes the shared SKELETON. "Reduce dependencies" here is
    conceptual (367 rest on ~7 forms), never equation removal.

Not everything is a pure specialization — and that is reported honestly, not
padded: some equations are composites of two kernels, many are sui generis.
"""
from __future__ import annotations
import math
from typing import Callable, Dict, List, Optional


# ---------------------------------------------------------------- the kernels
def log_ratio(coeff: float, num: float, den: float,
              offset: float = 0.0, base: str = "e") -> float:
    """offset + coeff · log(num/den). The Boltzmann/Nernst form: a potential,
    energy or pH set by the LOGARITHM of a concentration/activity ratio, scaled
    by a thermal factor (RT/zF, RT, or 1/2.303). Nernst, GHK, Henderson–
    Hasselbalch, Gibbs (RT·lnQ), Donnan."""
    r = num / den
    lg = math.log(r) if base == "e" else math.log10(r)
    return offset + coeff * lg


def saturation(vmax: float, x: float, k: float, n: float = 1.0) -> float:
    """vmax · xⁿ / (kⁿ + xⁿ). The Michaelis–Menten/Hill form: a bounded response
    to a driving concentration, half-maximal at x=k, cooperativity n. Enzyme
    kinetics, carrier transport, haemoglobin saturation, receptor occupancy,
    SGLT/GLUT uptake, voltage-gated channel activation."""
    xn = x ** n
    return vmax * xn / (k ** n + xn)


def first_order(x0: float, k: float, t: float, plateau: float = 0.0) -> float:
    """plateau + (x0 − plateau)·e^(−k·t). First-order kinetics: a quantity
    relaxes exponentially toward a plateau with rate k (= 1/τ). Drug elimination,
    gastric emptying, wash-in/out, capacitor/membrane charging, radioactive-style
    decay."""
    return plateau + (x0 - plateau) * math.exp(-k * t)


def linear_flux(driving: float, resistance: Optional[float] = None,
                conductance: Optional[float] = None) -> float:
    """flux = driving_force / resistance = conductance · driving_force. The
    Ohm/Fick/Poiseuille/Starling/Darcy form: a gradient drives a proportional
    transport, opposed by a resistance (or eased by a conductance). Blood flow,
    diffusion, glomerular filtration, bulk water flux."""
    if resistance is not None:
        return driving / resistance
    assert conductance is not None, "linear_flux needs a resistance or a conductance"
    return conductance * driving


def laplace(a: float, r: float, coeff: float = 1.0) -> float:
    """coeff · a / r. Laplace's law of a curved wall relating transmural
    pressure, wall tension and radius (T = P·r/coeff). Alveolar/vessel/ventricular
    mechanics; the same relation solved for whichever variable is unknown."""
    return coeff * a / r


def linear_combination(terms, offset: float = 0.0) -> float:
    """offset + Σ cᵢ·xᵢ over ``terms`` = [(c, x), …]. The affine/balance form: an
    output is a weighted sum of contributions. Starling net filtration pressure
    (a balance of hydrostatic and oncotic pressures), the anion gap (a charge
    sum), MAP (a weighted mean of systolic/diastolic), albumin-corrected calcium
    (a baseline plus a correction). The most common shape in clinical physiology."""
    return offset + sum(c * x for c, x in terms)


def product(*factors: float) -> float:
    """∏ factors. A definitional/conservation product: an output is the direct
    product of its determinants. CO = HR·SV, filtered load = GFR·C, stroke work
    = MAP·SV, Fick flux = flow·(a−v) difference."""
    out = 1.0
    for f in factors:
        out *= f
    return out


KERNELS: Dict[str, Callable] = {
    "log_ratio": log_ratio, "saturation": saturation, "first_order": first_order,
    "linear_flux": linear_flux, "laplace": laplace, "product": product,
    "linear_combination": linear_combination,
}

INTUITION: Dict[str, str] = {
    "log_ratio":  "a potential/energy/pH set by the LOG of a ratio (RT·ln)",
    "saturation": "a bounded response to a driver, half-max at K, cooperativity n",
    "first_order":"exponential relaxation toward a plateau at rate k = 1/τ",
    "linear_flux":"gradient-driven transport = driving force / resistance",
    "laplace":    "curved-wall tension–pressure–radius law, T = P·r/coeff",
    "product":    "an output that is the direct product of its determinants",
    "linear_combination": "an affine balance: offset + a weighted sum of contributions",
}


# ---------------------------------------------------------------- the members
# Each: equation id -> (bind, test). `bind(**eq_inputs)` returns kernel kwargs;
# the membership is proven when kernel(**bind(**test)) == equation.compute(**test).
# `bind`s absorb each equation's context-specific constants (that is the point:
# the shared form, the private constants).
MEMBERS: Dict[str, Dict[str, dict]] = {
    "log_ratio": {
        "nernst_equation": dict(
            bind=lambda z, C_out, C_in, R=8.314, T_body=310.0, F=96485.0:
                dict(coeff=1000 * R * T_body / (z * F), num=C_out, den=C_in),
            test=dict(z=1, C_out=4.0, C_in=140.0)),
        "donnan_potential": dict(
            bind=lambda r, R=8.314, T_body=310.0, F=96485.0:
                dict(coeff=R * T_body / F, num=r, den=1.0),   # donnan returns volts
            test=dict(r=0.5)),
        "henderson_hasselbalch": dict(
            bind=lambda HCO3, PCO2, pKa, alpha:
                dict(offset=pKa, coeff=1.0, num=HCO3, den=alpha * PCO2, base="10"),
            test=dict(HCO3=24.0, PCO2=40.0, pKa=6.1, alpha=0.03)),
        "standard_free_energy": dict(
            bind=lambda K_eq, R=8.314, T_body=310.0:
                dict(coeff=-R * T_body, num=K_eq, den=1.0),
            test=dict(K_eq=1000.0)),
        "actual_free_energy": dict(
            bind=lambda delta_G0, Q, R=8.314, T_body=310.0:
                dict(offset=delta_G0, coeff=R * T_body, num=Q, den=1.0),
            test=dict(delta_G0=-1000.0, Q=10.0)),
        "electrochemical_potential": dict(   # zFψ is constant at fixed ψ -> folds into offset
            bind=lambda mu_0, C, z, psi, R=8.314, T_body=310.0, F=96485.0:
                dict(offset=mu_0 + z * F * psi, coeff=R * T_body, num=C, den=1.0),
            test=dict(mu_0=1000.0, C=5.0, z=1, psi=-0.07)),
    },
    "saturation": {
        "michaelis_menten": dict(
            bind=lambda S, J_max, K_m: dict(vmax=J_max, x=S, k=K_m, n=1.0),
            test=dict(S=5.0, J_max=10.0, K_m=2.0)),
        "hill_saturation": dict(
            bind=lambda P_O2, P_50, n: dict(vmax=1.0, x=P_O2, k=P_50, n=n),
            test=dict(P_O2=40.0, P_50=26.8, n=2.7)),
        "receptor_fractional_occupancy": dict(
            bind=lambda H, Kd: dict(vmax=1.0, x=H, k=Kd, n=1.0),
            test=dict(H=5.0, Kd=2.0)),
        "sglt1_glucose": dict(
            bind=lambda glucose_lumen, Vmax, Km: dict(vmax=Vmax, x=glucose_lumen, k=Km, n=1.0),
            test=dict(glucose_lumen=6.0, Vmax=10.0, Km=2.0)),
        "carrier_transport": dict(
            bind=lambda S, J_max, K_m: dict(vmax=J_max, x=S, k=K_m, n=1.0),
            test=dict(S=5.0, J_max=10.0, K_m=2.0)),
        "transport_tm": dict(
            bind=lambda T_max, S, K_m: dict(vmax=T_max, x=S, k=K_m, n=1.0),
            test=dict(T_max=10.0, S=5.0, K_m=2.0)),
        "amylase_kinetics": dict(
            bind=lambda starch_conc, J_max, Km: dict(vmax=J_max, x=starch_conc, k=Km, n=1.0),
            test=dict(starch_conc=5.0, J_max=10.0, Km=2.0)),
        "lipase_kinetics": dict(
            bind=lambda TG_conc, J_max, Km: dict(vmax=J_max, x=TG_conc, k=Km, n=1.0),
            test=dict(TG_conc=5.0, J_max=10.0, Km=2.0)),
        "glut5_fructose": dict(
            bind=lambda fructose_lumen, Vmax, Km: dict(vmax=Vmax, x=fructose_lumen, k=Km, n=1.0),
            test=dict(fructose_lumen=6.0, Vmax=10.0, Km=5.0)),
        "gastrin_acid_response": dict(   # Hill (cooperativity n)
            bind=lambda gastrin_pg_mL, Amax, EC50, n: dict(vmax=Amax, x=gastrin_pg_mL, k=EC50, n=n),
            test=dict(gastrin_pg_mL=100.0, Amax=10.0, EC50=50.0, n=2.0)),
        "pepsin_activity": dict(   # Hill in [H+]
            bind=lambda H_conc, A_max, K_H, n: dict(vmax=A_max, x=H_conc, k=K_H, n=n),
            test=dict(H_conc=1e-3, A_max=10.0, K_H=1e-3, n=2.0)),
    },
    "first_order": {
        "first_order_elimination": dict(
            bind=lambda C0, ke, t: dict(x0=C0, k=ke, t=t, plateau=0.0),
            test=dict(C0=100.0, ke=0.15, t=3.0)),
        "gastric_emptying_liquid": dict(
            bind=lambda t, V0, k: dict(x0=V0, k=k, t=t, plateau=0.0),
            test=dict(t=20.0, V0=300.0, k=0.03)),
        "passive_membrane_charging": dict(
            bind=lambda I, R, t, tau: dict(x0=0.0, k=1.0 / tau, t=t, plateau=I * R),
            test=dict(I=1e-9, R=1e8, t=2.0, tau=1.0)),
        "exponential_emptying": dict(
            bind=lambda V0, t, tau: dict(x0=V0, k=1.0 / tau, t=t, plateau=0.0),
            test=dict(V0=300.0, t=20.0, tau=30.0)),
    },
    "linear_flux": {
        "gfr_from_nfp": dict(
            bind=lambda K_f, NFP: dict(driving=NFP, conductance=K_f),
            test=dict(K_f=12.5, NFP=10.0)),
        "fick_first_law": dict(
            bind=lambda D, dC_dx: dict(driving=dC_dx, conductance=-D),
            test=dict(D=2.0, dC_dx=3.0)),
        "poiseuille_flow": dict(
            bind=lambda r, eta, delta_P, L:
                dict(driving=delta_P, conductance=math.pi * r ** 4 / (8 * eta * L)),
            test=dict(r=0.01, eta=0.004, delta_P=1000.0, L=0.1)),
        "water_flux": dict(   # J_V = L_p·(ΔP − σΔπ): net driving pressure over a conductance
            bind=lambda L_p, delta_P, delta_pi, sigma:
                dict(driving=delta_P - sigma * delta_pi, conductance=L_p),
            test=dict(L_p=1.0, delta_P=10.0, delta_pi=5.0, sigma=0.9)),
        "ionic_current": dict(   # I = g·(V_m − E): driving force × conductance (Ohm)
            bind=lambda g_ion, V_m, E_ion: dict(driving=V_m - E_ion, conductance=g_ion),
            test=dict(g_ion=2.0, V_m=-70.0, E_ion=-90.0)),
        "single_channel_conductance": dict(   # γ = i/(V_m − E): current over a driving voltage
            bind=lambda i, V_m, E_ion: dict(driving=i, resistance=V_m - E_ion),
            test=dict(i=2.0, V_m=-70.0, E_ion=-90.0)),
    },
    "laplace": {
        "laplace_sphere": dict(
            bind=lambda T, r: dict(a=T, r=r, coeff=2.0),
            test=dict(T=0.05, r=0.0001)),
        "laplace_cylinder": dict(
            bind=lambda T, r: dict(a=T, r=r, coeff=1.0),
            test=dict(T=0.05, r=0.0001)),
        "ventricular_wall_stress": dict(
            bind=lambda P, r, h: dict(a=P * r, r=h, coeff=0.5),
            test=dict(P=120.0, r=25.0, h=10.0)),
    },
    "product": {
        "cardiac_output": dict(
            bind=lambda HR, SV: dict(factors=(HR, SV / 1000.0)),
            test=dict(HR=70.0, SV=70.0)),
        "filtered_load": dict(
            bind=lambda GFR, P_x: dict(factors=(GFR, P_x, 0.01)),  # P_x mg/dL -> per-min unit factor
            test=dict(GFR=125.0, P_x=5.0)),
        "stroke_work": dict(
            bind=lambda MAP, SV: dict(factors=(MAP, SV)),
            test=dict(MAP=93.0, SV=70.0)),
        "systemic_oxygen_delivery": dict(   # DO2 = CO·(1.34·Hb·SO2)·10
            bind=lambda CO, Hb, S_O2: dict(factors=(CO, 1.34, Hb, S_O2, 10.0)),
            test=dict(CO=5.0, Hb=14.0, S_O2=0.97)),
        "tissue_oxygen_delivery": dict(
            bind=lambda Q, CaO2: dict(factors=(Q, CaO2, 10.0)),
            test=dict(Q=5.0, CaO2=20.0)),
        "minute_ventilation": dict(
            bind=lambda VT, f: dict(factors=(VT, f)),
            test=dict(VT=0.5, f=12.0)),
        "alveolar_ventilation": dict(   # (VT − VD)·f: product of an effective-volume difference
            bind=lambda VT, VD, f: dict(factors=(VT - VD, f)),
            test=dict(VT=0.5, VD=0.15, f=12.0)),
        "membrane_time_constant": dict(   # τ = R_m·C_m
            bind=lambda R_m, C_m: dict(factors=(R_m, C_m)),
            test=dict(R_m=10.0, C_m=2.0)),
    },
    "linear_combination": {
        "glomerular_nfp": dict(   # Starling balance: P_GC − P_BC − π_GC + π_BC
            bind=lambda P_GC, P_BC, pi_GC, pi_BC:
                dict(terms=[(1.0, P_GC), (-1.0, P_BC), (-1.0, pi_GC), (1.0, pi_BC)]),
            test=dict(P_GC=50.0, P_BC=15.0, pi_GC=25.0, pi_BC=0.0)),
        "net_filtration_pressure": dict(   # (P_c−P_i) − σ(π_c−π_i)
            bind=lambda P_c, P_i, pi_c, pi_i, sigma:
                dict(terms=[(1.0, P_c), (-1.0, P_i), (-sigma, pi_c), (sigma, pi_i)]),
            test=dict(P_c=30.0, P_i=3.0, pi_c=28.0, pi_i=8.0, sigma=0.9)),
        "anion_gap": dict(   # charge sum: Na − Cl − HCO3
            bind=lambda Na, Cl, HCO3: dict(terms=[(1.0, Na), (-1.0, Cl), (-1.0, HCO3)]),
            test=dict(Na=140.0, Cl=104.0, HCO3=24.0)),
        "mean_arterial_pressure": dict(   # weighted mean: ⅓SBP + ⅔DBP
            bind=lambda SBP, DBP: dict(terms=[(1.0 / 3.0, SBP), (2.0 / 3.0, DBP)]),
            test=dict(SBP=120.0, DBP=80.0)),
        "pulse_pressure": dict(
            bind=lambda SBP, DBP: dict(terms=[(1.0, SBP), (-1.0, DBP)]),
            test=dict(SBP=120.0, DBP=80.0)),
        "alveolar_gas_equation": dict(   # P_iO2 − P_ACO2/RQ (affine at fixed RQ)
            bind=lambda P_iO2, P_ACO2, RQ: dict(terms=[(1.0, P_iO2), (-1.0 / RQ, P_ACO2)]),
            test=dict(P_iO2=150.0, P_ACO2=40.0, RQ=0.8)),
        "calcium_albumin_correction": dict(   # Ca + 0.8·(4 − albumin) = Ca − 0.8·alb + 3.2
            bind=lambda measured_Ca, albumin:
                dict(terms=[(1.0, measured_Ca), (-0.8, albumin)], offset=3.2),
            test=dict(measured_Ca=2.1, albumin=30.0)),
        "corrected_anion_gap": dict(   # AG + 0.25·(40 − albumin)
            bind=lambda AG, albumin: dict(terms=[(1.0, AG), (-0.25, albumin)], offset=10.0),
            test=dict(AG=12.0, albumin=30.0)),
        "net_acid_excretion": dict(   # TA + NH4 − HCO3
            bind=lambda TA, NH4, HCO3_excreted:
                dict(terms=[(1.0, TA), (1.0, NH4), (-1.0, HCO3_excreted)]),
            test=dict(TA=30.0, NH4=40.0, HCO3_excreted=2.0)),
    },
}


# ---------------------------------------------------------------- verify + query
def _apply_kernel(prim: str, kwargs: dict) -> float:
    if prim == "product":
        return product(*kwargs["factors"])
    if prim == "linear_combination":
        return linear_combination(kwargs["terms"], kwargs.get("offset", 0.0))
    return KERNELS[prim](**kwargs)


def verify(prim: str, eid: str, tol: float = 1e-6) -> bool:
    """Prove membership: the kernel with the curated binding reproduces the
    equation's own compute at the test inputs."""
    from scripts.canonical_ids import load
    spec = MEMBERS[prim][eid]
    got = _apply_kernel(prim, spec["bind"](**spec["test"]))
    want = float(load(eid)._compute_func(**spec["test"]))
    denom = max(1.0, abs(want))
    return abs(got - want) / denom <= tol


def primitive_of(eid: str) -> List[str]:
    """Which universal primitive(s) an equation is a proven specialization of."""
    return [p for p, members in MEMBERS.items() if eid in members]


def members_of(prim: str) -> List[str]:
    """The equations proven to share this primitive's form."""
    return list(MEMBERS.get(prim, {}))


def explain(prim: str) -> dict:
    """The universal intuition + its proven members."""
    return {"primitive": prim, "intuition": INTUITION.get(prim, ""),
            "members": members_of(prim)}


def all_members() -> Dict[str, List[str]]:
    return {p: members_of(p) for p in MEMBERS}


if __name__ == "__main__":  # self-check / distribution report
    ok = bad = 0
    for prim, members in MEMBERS.items():
        for eid in members:
            if verify(prim, eid):
                ok += 1
            else:
                bad += 1
                print(f"FAIL  {prim} <- {eid}")
    total = ok + bad
    print(f"\n{ok}/{total} memberships proven "
          f"(kernel reproduces compute); {len(MEMBERS)} universal primitives")

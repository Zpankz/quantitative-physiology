"""Regenerator for graph/clusters.json.

Run from the package parent directory:  python -m scripts.generate_clusters

Functional clusters are human-curated groupings (each with a unifying
principle), but their equation lists must reference REAL equation ids. The
previous clusters.json used a hierarchical + ':' id scheme
(`cardiovascular.hemodynamics.tpr`) that matched no code id. This generator
embeds the curation with flat, real ids and validates every one against the
package before writing, so the file can no longer drift from the equations.

To change cluster membership, edit CLUSTERS below and re-run.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from scripts import canonical_ids as C  # noqa: E402

# key -> {name, unifying_principle, [real equation ids]}
CLUSTERS = {
    "transport_mechanics": {
        "name": "Transport & Fluid Mechanics",
        "unifying_principle": "Pressure-driven flow in tubes",
        "equations": ["poiseuille_flow", "hydraulic_resistance", "laplace_cylinder",
                       "laplace_sphere", "poiseuille_resistance",
                       "total_peripheral_resistance", "airway_resistance"],
    },
    "membrane_potential": {
        "name": "Electrochemical Gradients",
        "unifying_principle": "Ion distributions create electrical potentials",
        "equations": ["nernst_equation", "donnan_potential", "donnan_ratio",
                       "ghk_potential", "chord_conductance"],
    },
    "excitation_contraction": {
        "name": "Excitation-Contraction Coupling",
        "unifying_principle": "Electrical signals to mechanical force",
        "equations": ["hh_membrane_current", "cable_equation", "ca_force_relationship",
                       "hill_force_velocity", "espvr"],
    },
    "oxygen_cascade": {
        "name": "Oxygen Transport Cascade",
        "unifying_principle": "O2 from air to mitochondria",
        "equations": ["alveolar_gas_equation", "diffusing_capacity", "hill_equation",
                       "blood_oxygen_content", "respiratory_oxygen_content",
                       "systemic_oxygen_delivery", "tissue_oxygen_delivery",
                       "oxygen_consumption_fick"],
    },
    "acid_base": {
        "name": "Acid-Base Homeostasis",
        "unifying_principle": "pH regulation via buffers and compensation",
        "equations": ["henderson_hasselbalch", "anion_gap", "winters_formula",
                       "net_acid_excretion", "new_bicarbonate_generation"],
    },
    "renal_function": {
        "name": "Renal Filtration & Clearance",
        "unifying_principle": "Glomerular filtration and tubular processing",
        "equations": ["net_filtration_pressure", "gfr_from_nfp", "clearance",
                       "filtered_load", "fractional_excretion", "starling_filtration"],
    },
    "hormone_kinetics": {
        "name": "Hormone Kinetics & Feedback",
        "unifying_principle": "Ligand-receptor binding and feedback loops",
        "equations": ["hormone_kd", "metabolic_clearance_rate",
                       "receptor_fractional_occupancy", "feedback_gain",
                       "receptor_occupancy"],
    },
    "synaptic_transmission": {
        "name": "Synaptic & Neural Signaling",
        "unifying_principle": "Chemical neurotransmission",
        "equations": ["quantal_content", "synaptic_current", "epsp_amplitude",
                       "stdp", "safety_factor"],
    },
    "gastrointestinal_function": {
        "name": "GI Secretion & Absorption",
        "unifying_principle": "Digestion and nutrient absorption",
        "equations": ["gastric_acid_output", "gi_enzyme_kinetics", "sglt1_glucose",
                       "hepatic_clearance", "incretin_effect"],
    },
    "cardiovascular_regulation": {
        "name": "CV Regulation & Control",
        "unifying_principle": "Blood pressure and volume regulation",
        "equations": ["cardiac_output", "mean_arterial_pressure",
                       "baroreceptor_sensitivity", "compliance",
                       "adh_water_permeability"],
    },
}


def main():
    os.chdir(ROOT)
    real = set(C.CANONICAL_EQUATIONS)
    # validate every cluster id exists; fail loudly otherwise
    missing = {k: [e for e in cl["equations"] if e not in real]
               for k, cl in CLUSTERS.items()}
    missing = {k: v for k, v in missing.items() if v}
    if missing:
        raise SystemExit(f"clusters reference non-existent ids: {missing}")

    out = {
        "metadata": {
            "description": "Functional clusters of related equations across physiological domains",
            "generated_by": "scripts/generate_clusters.py",
            "do_not_edit_by_hand": True,
            "num_clusters": len(CLUSTERS),
        },
        "clusters": {
            key: {
                "name": cl["name"],
                "unifying_principle": cl["unifying_principle"],
                "equations": [
                    {"id": e, "module": C.CANONICAL_EQUATIONS[e]["module"],
                     "domain": C.CANONICAL_EQUATIONS[e]["domain"]}
                    for e in cl["equations"]
                ],
            } for key, cl in CLUSTERS.items()
        },
    }
    path = os.path.join("graph", "clusters.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    total = sum(len(cl["equations"]) for cl in CLUSTERS.values())
    print(f"wrote {path}  ({len(CLUSTERS)} clusters, {total} equation refs, all real)")


if __name__ == "__main__":
    main()

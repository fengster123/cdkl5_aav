"""
Normalized comparison data for CDKL5 AAV gene therapy studies.

This module provides conversion functions and normalized data structures
to enable like-for-like comparison between:
- PTC (AAV9-ICV) approach
- Wilson (AAV-PHP.eB-IV) approach
"""

# Mouse biological parameters for dose conversions
MOUSE_PARAMS = {
    "neonatal_p0": {
        "body_weight_g": 1.5,  # grams
        "brain_weight_g": 0.08,  # grams
        "brain_to_body_ratio": 0.08 / 1.5,  # ~0.053
    },
    "adult": {
        "body_weight_g": 22.0,  # grams
        "brain_weight_g": 0.45,  # grams
        "brain_to_body_ratio": 0.45 / 22.0,  # ~0.020
    },
}


def vg_per_kg_to_vg_per_g_brain(vg_per_kg, age="neonatal_p0"):
    """
    Convert dose from vg/kg body weight to vg/g brain tissue.

    Args:
        vg_per_kg: Vector genomes per kilogram body weight
        age: "neonatal_p0" or "adult"

    Returns:
        Estimated vg/g brain tissue

    Formula:
        vg/kg * (body_weight_kg / brain_weight_g)
        = vg/kg * (body_weight_g / 1000) / brain_weight_g

    Example:
        For neonatal P0 mouse:
        1e12 vg/kg * (1.5g / 1000) / 0.08g = 1e12 * 0.0015 / 0.08 = 1.875e10 vg/g brain
    """
    params = MOUSE_PARAMS[age]
    body_weight_kg = params["body_weight_g"] / 1000.0
    brain_weight_g = params["brain_weight_g"]

    vg_per_g_brain = vg_per_kg * (body_weight_kg / brain_weight_g)
    return vg_per_g_brain


def vg_per_g_brain_to_vg_per_kg(vg_per_g_brain, age="neonatal_p0"):
    """
    Convert dose from vg/g brain tissue to vg/kg body weight.

    Args:
        vg_per_g_brain: Vector genomes per gram brain tissue
        age: "neonatal_p0" or "adult"

    Returns:
        Estimated vg/kg body weight
    """
    params = MOUSE_PARAMS[age]
    body_weight_kg = params["body_weight_g"] / 1000.0
    brain_weight_g = params["brain_weight_g"]

    vg_per_kg = vg_per_g_brain / (body_weight_kg / brain_weight_g)
    return vg_per_kg


# Normalized dose comparison table
# All doses normalized to vg/g brain for neonatal dosing
DOSE_COMPARISON = {
    "ptc_doses": [
        {
            "dose_level": "low",
            "dose_vg_g_brain": 3e9,
            "dose_vg_kg": vg_per_g_brain_to_vg_per_kg(3e9, "neonatal_p0"),
            "route": "ICV",
            "study": "PTC Study 2",
        },
        {
            "dose_level": "mid",
            "dose_vg_g_brain": 3e10,
            "dose_vg_kg": vg_per_g_brain_to_vg_per_kg(3e10, "neonatal_p0"),
            "route": "ICV",
            "study": "PTC Study 2",
        },
        {
            "dose_level": "high",
            "dose_vg_g_brain": 3e11,
            "dose_vg_kg": vg_per_g_brain_to_vg_per_kg(3e11, "neonatal_p0"),
            "route": "ICV",
            "study": "PTC Study 2, 3",
        },
        {
            "dose_level": "very_high",
            "dose_vg_g_brain": 5e11,
            "dose_vg_kg": vg_per_g_brain_to_vg_per_kg(5e11, "neonatal_p0"),
            "route": "ICV",
            "study": "PTC Study 3",
        },
    ],
    "wilson_doses_neonatal": [
        {
            "dose_level": "low",
            "dose_vg_kg": 1e11,
            "dose_vg_g_brain": vg_per_kg_to_vg_per_g_brain(1e11, "neonatal_p0"),
            "route": "IV",
            "study": "Wilson neonatal",
        },
        {
            "dose_level": "low_mid",
            "dose_vg_kg": 3e11,
            "dose_vg_g_brain": vg_per_kg_to_vg_per_g_brain(3e11, "neonatal_p0"),
            "route": "IV",
            "study": "Wilson neonatal",
        },
        {
            "dose_level": "mid",
            "dose_vg_kg": 5e11,
            "dose_vg_g_brain": vg_per_kg_to_vg_per_g_brain(5e11, "neonatal_p0"),
            "route": "IV",
            "study": "Wilson neonatal",
        },
        {
            "dose_level": "high",
            "dose_vg_kg": 1e12,
            "dose_vg_g_brain": vg_per_kg_to_vg_per_g_brain(1e12, "neonatal_p0"),
            "route": "IV",
            "study": "Wilson neonatal",
        },
        {
            "dose_level": "very_high",
            "dose_vg_kg": 2e12,
            "dose_vg_g_brain": vg_per_kg_to_vg_per_g_brain(2e12, "neonatal_p0"),
            "route": "IV",
            "study": "Wilson neonatal",
        },
        {
            "dose_level": "ultra_high",
            "dose_vg_kg": 3e12,
            "dose_vg_g_brain": vg_per_kg_to_vg_per_g_brain(3e12, "neonatal_p0"),
            "route": "IV",
            "study": "Wilson neonatal",
        },
    ],
}


# CDKL5 protein expression levels (% of WT)
EXPRESSION_COMPARISON = {
    "ptc": {
        "hippocampus": [
            {"dose_vg_g": 3e9, "cdkl5_percent_wt": 1.8, "sem": 0.3},
            {"dose_vg_g": 3e10, "cdkl5_percent_wt": 3.9, "sem": 1.0},
            {"dose_vg_g": 3e11, "cdkl5_percent_wt_study2": 33, "sem_study2": 12},
            {"dose_vg_g": 3e11, "cdkl5_percent_wt_study3": 123, "sem_study3": 32},
            {"dose_vg_g": 5e11, "cdkl5_percent_wt": 347, "sem": 98},
        ],
        "cortex": [
            {"dose_vg_g": 3e9, "cdkl5_percent_wt": 1.3, "sem": 0.2},
            {"dose_vg_g": 3e10, "cdkl5_percent_wt": 2.2, "sem": 0.6},
            {"dose_vg_g": 3e11, "cdkl5_percent_wt_study2": 30, "sem_study2": 14},
            {"dose_vg_g": 3e11, "cdkl5_percent_wt_study3": 73, "sem_study3": 22},
            {"dose_vg_g": 5e11, "cdkl5_percent_wt": 136, "sem": 21},
        ],
        "cerebellum": [
            {"dose_vg_g": 3e9, "cdkl5_percent_wt": 1.0, "sem": 0.2},
            {"dose_vg_g": 3e10, "cdkl5_percent_wt": 0.9, "sem": 0.2},
            {"dose_vg_g": 3e11, "cdkl5_percent_wt_study2": 10, "sem_study2": 2},
            {"dose_vg_g": 3e11, "cdkl5_percent_wt_study3": 18, "sem_study3": 5},
            {"dose_vg_g": 5e11, "cdkl5_percent_wt": 33, "sem": 9},
        ],
        "notes": "Study-to-study variability noted at 3e11 vg/g dose",
    },
    "wilson": {
        "hippocampus": [
            {
                "dose_vg_kg": 1e12,
                "cdkl5_percent_wt_range": "50-100",
                "note": "From presentation slides; approximate range",
            },
            {
                "dose_vg_kg": 2e12,
                "cdkl5_percent_wt_range": "100-200",
                "note": "Supraphysiological at higher end",
            },
        ],
        "cortex": [
            {"dose_vg_kg": 1e12, "cdkl5_percent_wt_range": "50-100"},
            {"dose_vg_kg": 2e12, "cdkl5_percent_wt_range": "100-200"},
        ],
        "striatum": [
            {"dose_vg_kg": 1e12, "cdkl5_percent_wt_range": "30-70"},
            {"dose_vg_kg": 2e12, "cdkl5_percent_wt_range": "70-150"},
        ],
        "notes": "Less precise quantification from presentation; ranges estimated from figures",
    },
}


# Efficacy data - motor function
EFFICACY_MOTOR = {
    "ptc": {
        "hindlimb_clasp": [
            {
                "dose_vg_g": 3e9,
                "effect": "no improvement",
                "normalization_percent": 0,
            },
            {
                "dose_vg_g": 3e10,
                "effect": "no significant reduction",
                "normalization_percent": 0,
            },
            {
                "dose_vg_g": 3e11,
                "effect": "complete normalization",
                "normalization_percent": 100,
                "p_value": "<0.001",
                "timepoint_weeks": 11,
            },
        ],
        "open_field_distance": [
            {
                "dose_vg_g": 3e9,
                "effect": "no reduction",
                "normalization_percent": 0,
                "timepoint_weeks": 15,
            },
            {
                "dose_vg_g": 3e10,
                "effect": "no reduction",
                "normalization_percent": 0,
                "timepoint_weeks": 15,
            },
            {
                "dose_vg_g": 3e11,
                "effect": "no reduction",
                "normalization_percent": 0,
                "timepoint_weeks": 15,
            },
            {
                "dose_vg_g": 5e11,
                "effect": "mitigated hyperactivity",
                "normalization_percent": 43,
                "p_value": 0.39,
                "significance": "not significant",
                "timepoint_weeks": 14,
            },
        ],
        "open_field_mobility": [
            {
                "dose_vg_g": 5e11,
                "measure": "highly mobile time",
                "reduction_percent": 46,
                "p_value": "<0.01",
                "timepoint_weeks": 14,
            }
        ],
    },
    "wilson": {
        "rotarod": [
            {
                "dose_vg_kg": 1e12,
                "effect": "partial rescue",
                "description": "Improvement in motor coordination vs WT",
            },
            {
                "dose_vg_kg": 2e12,
                "effect": "near-normalization",
                "description": "Significant improvement",
            },
        ],
        "open_field": [
            {
                "dose_range_vg_kg": "therapeutic doses",
                "effect": "partial normalization of hyperactivity",
            }
        ],
    },
}


# Efficacy data - cognitive/learning
EFFICACY_COGNITIVE = {
    "ptc": {
        "fear_conditioning": [
            {
                "dose_vg_g": 3e9,
                "effect": "no improvement",
                "recovery_percent": 0,
            },
            {
                "dose_vg_g": 3e10,
                "effect": "no improvement",
                "recovery_percent": 0,
            },
            {
                "dose_vg_g": 3e11,
                "study": 2,
                "recovery_percent": 44,
                "p_value": "<0.05",
                "timepoint_weeks": 17,
            },
            {
                "dose_vg_g": 3e11,
                "study": 3,
                "recovery_percent": 62,
                "significance": "not significant",
                "timepoint_weeks": 16,
            },
            {
                "dose_vg_g": 5e11,
                "recovery_percent": 100,
                "effect": "complete normalization",
                "p_value": "<0.01",
                "timepoint_weeks": 16,
            },
        ],
    },
    "wilson": {
        "fear_conditioning": [
            {
                "dose_range": "therapeutic",
                "effect": "some improvement but not complete rescue",
            }
        ],
        "novel_object_recognition": [
            {"dose_range": "therapeutic", "effect": "partial rescue"}
        ],
        "barnes_maze": [{"dose_range": "therapeutic", "effect": "tested"}],
        "note": "Cognitive deficits may require earlier intervention or additional therapies",
    },
}


# Efficacy data - seizures (Wilson only)
EFFICACY_SEIZURES = {
    "wilson": {
        "neonatal_dosing": [
            {
                "dose_vg_kg": 1e12,
                "seizure_reduction_percent": "30-50",
                "onset_weeks": "2-4",
            },
            {
                "dose_vg_kg": 2e12,
                "seizure_reduction_percent": "60-80",
                "effect": "near-normalization of seizure burden",
            },
            {
                "dose_vg_kg": 3e12,
                "seizure_reduction_percent": "70-90",
                "effect": "robust suppression",
                "note": "highest efficacy but toxicity concerns",
            },
        ],
        "adult_dosing": [
            {
                "dose_vg_kg": 1e12,
                "seizure_reduction_percent": "20-30",
                "effect": "modest reduction",
            },
            {
                "dose_vg_kg": 2e12,
                "seizure_reduction_percent": "40-60",
                "effect": "moderate reduction",
                "note": "less efficacy than neonatal dosing",
            },
        ],
    },
    "ptc": {
        "note": "Seizures not directly measured via video-EEG; critical gap in study design"
    },
}


# Efficacy data - morphology (PTC emphasis)
EFFICACY_MORPHOLOGY = {
    "ptc": {
        "golgi_cox_ca1_pyramidal": [
            {
                "dose_vg_g": 3e10,
                "effect": "significant improvements in dendritic measures",
                "detail": "dose-dependent improvements",
            },
            {
                "dose_vg_g": 3e11,
                "effect": "near-normalization",
                "detail": "more pronounced than 3e10",
                "measures": [
                    "dendritic length (basal/apical)",
                    "spine count",
                    "spine density",
                    "Sholl branching",
                ],
            },
        ],
    },
    "wilson": {"note": "Limited morphology assessment; not primary endpoint"},
}


# Safety findings
SAFETY_COMPARISON = {
    "ptc": {
        "retinal_toxicity": {
            "observed": "Not reported",
            "note": "Either not assessed or not observed at doses tested",
        },
        "cns_toxicity": {"finding": "No overt toxicity up to 3.6e12 vg/g brain"},
        "peripheral_toxicity": {
            "finding": "Minimal",
            "note": "Low peripheral exposure due to ICV route",
        },
        "overexpression": {
            "highest_levels": "430% WT in hippocampus at 5e11 vg/g",
            "concern": "Unclear risk; duplications reported but not definitive",
        },
    },
    "wilson": {
        "retinal_toxicity": {
            "observed": "Yes, dose-dependent at ≥2e12 vg/kg with CAG promoter",
            "mechanism": "CDKL5 overexpression in photoreceptors",
            "histology": "Outer nuclear layer thinning, photoreceptor loss",
            "erg": "Reduced scotopic/photopic responses",
            "mitigation": "miR-183 target sites reduced retinal expression 70-90% while preserving brain expression",
        },
        "cns_toxicity": {
            "finding": "No overt toxicity at therapeutic doses",
            "concern": "Supraphysiological expression at highest doses",
        },
        "peripheral_toxicity": {
            "liver": "Transaminase elevations at highest doses (transient)",
            "other": "No overt toxicity in heart, kidney, spleen at therapeutic doses",
            "note": "Higher exposure due to IV route",
        },
        "overexpression": {
            "highest_levels": "200% WT in hippocampus/cortex at 2e12 vg/kg",
            "concern": "Potential for supraphysiological CNS expression",
        },
    },
}


# Biodistribution comparison
BIODISTRIBUTION_COMPARISON = {
    "ptc": {
        "route": "ICV",
        "pattern": "Broad distribution throughout brain; some regional variation",
        "cell_type": "Neurons only (Synapsin promoter; no GFAP+ expression)",
        "percent_neurons_transduced": {
            "dose_3_6e11": "1-25% NeuN+",
            "dose_1_2e12": "26-50% NeuN+",
            "dose_3_6e12": "51-75% NeuN+",
            "note": "Up to ~75% neurons at high dose",
        },
        "peripheral_exposure": "Significant in liver despite CNS route",
    },
    "wilson": {
        "route": "IV",
        "pattern": "Broad, relatively uniform CNS distribution with PHP.eB capsid",
        "cell_type": {
            "CAG_promoter": "Neurons (high) + astrocytes (moderate) + other CNS cells",
            "hSyn_promoter": "Neurons only; minimal astrocyte expression",
        },
        "percent_neurons_transduced": "Not quantified by % NeuN+",
        "peripheral_exposure": "High (liver, spleen, heart, kidney) due to IV route",
        "route_comparison": "IV (PHP.eB) more uniform than ICV",
    },
}


# Vector design comparison
VECTOR_DESIGN_COMPARISON = {
    "ptc": {
        "capsid": "AAV9",
        "capsid_translatability": "High - clinically validated",
        "promoter": "Synapsin (neuron-specific)",
        "promoter_strategy": "Cell-type restriction",
        "regulatory_elements": {
            "polyA": "bGH pA",
            "ITRs": "AAV2",
            "WPRE": "mentioned",
        },
        "safety_features": "Neuron-specific promoter limits off-target expression",
    },
    "wilson": {
        "capsid": "AAV-PHP.eB",
        "capsid_translatability": "Low - mouse-specific; requires human alternative",
        "promoters_tested": ["CAG (primary)", "hSyn", "CBA"],
        "promoter_strategy": "Ubiquitous expression + tissue detargeting (miR-183)",
        "regulatory_elements": {"ITRs": "AAV2", "polyA": "not specified"},
        "safety_features": "miR-183 sites for retinal detargeting",
    },
}


# Translational considerations
TRANSLATIONAL_COMPARISON = {
    "ptc": {
        "capsid_path": "AAV9 already clinically validated",
        "delivery_path": "ICV/IT requires surgery but established in clinical trials",
        "manufacturing": "Standard AAV9 production",
        "regulatory_precedent": "Similar to other AAV9-CNS therapies",
        "nhp_data": "Yes - biodistribution and tolerability in cynomolgus macaques",
        "challenges": [
            "Surgical delivery (ICV/IT)",
            "Need for broad neuron transduction",
            "High doses required",
        ],
    },
    "wilson": {
        "capsid_path": "Need human-compatible capsid (PHP.eB not translatable)",
        "delivery_path": "IV non-invasive IF human capsid available",
        "manufacturing": "Would need new capsid manufacturing",
        "regulatory_precedent": "Less established for systemic AAV-CNS",
        "nhp_data": "Not mentioned in presentation",
        "challenges": [
            "PHP.eB mouse-specific",
            "Retinal toxicity mitigation required",
            "Higher peripheral exposure with IV",
            "Need alternative capsid for humans",
        ],
    },
}


# Summary comparison
SUMMARY_COMPARISON = {
    "convergent_findings": [
        "Both achieve efficacy at ~50-200% WT CDKL5 levels in brain",
        "Clear dose-response relationship for efficacy",
        "Neonatal dosing effective in both approaches",
        "Broad CNS distribution correlates with efficacy",
        "Motor/behavioral improvements in both studies",
        "CNS well-tolerated at therapeutic doses",
        "Overexpression risk at very high doses (>200% WT)",
        "Both use neuron-targeting strategies (PTC: promoter, Wilson: primary effect)",
    ],
    "divergent_findings": [
        "Delivery route: ICV (PTC) vs IV (Wilson)",
        "Capsid: AAV9 (clinically translatable) vs PHP.eB (mouse-specific)",
        "Promoter: Neuron-specific (PTC) vs ubiquitous + detargeting (Wilson)",
        "Peripheral exposure: Lower (PTC) vs higher (Wilson)",
        "Retinal toxicity: Not observed/reported (PTC) vs identified and mitigated (Wilson)",
        "Primary endpoints: Morphology/behavior (PTC) vs seizures (Wilson)",
        "Translational readiness: Higher (PTC) vs lower (Wilson - needs capsid change)",
    ],
    "critical_gaps": [
        "PTC: No seizure assessment (video-EEG)",
        "Wilson: Limited morphology assessment",
        "PTC: No retinal safety assessment reported",
        "Wilson: Less precise dose-response quantification (presentation vs manuscript)",
        "Both: Primarily male mice; limited female data",
        "Both: Limited adult dosing efficacy data",
    ],
    "optimal_doses": {
        "ptc": {
            "range_vg_g": "3e11 - 5e11",
            "efficacy": "3e11 effective for some endpoints; 5e11 for full efficacy",
            "safety": "Up to 3.6e12 vg/g tested without overt CNS toxicity",
        },
        "wilson": {
            "range_vg_kg_neonatal": "1e12 - 2e12",
            "range_vg_g_brain_equivalent": "1.9e10 - 3.8e10 (estimated)",
            "efficacy": "1-2e12 vg/kg for seizure control and motor improvements",
            "safety": "≥2e12 vg/kg retinal toxicity risk without miR-183",
        },
    },
}


if __name__ == "__main__":
    # Demo conversions
    print("=== Dose Conversion Examples ===\n")

    print("Wilson doses (vg/kg) → PTC units (vg/g brain):")
    wilson_doses = [1e11, 5e11, 1e12, 2e12, 3e12]
    for dose in wilson_doses:
        converted = vg_per_kg_to_vg_per_g_brain(dose, "neonatal_p0")
        print(f"  {dose:.2e} vg/kg → {converted:.2e} vg/g brain")

    print("\nPTC doses (vg/g brain) → Wilson units (vg/kg):")
    ptc_doses = [3e9, 3e10, 3e11, 5e11]
    for dose in ptc_doses:
        converted = vg_per_g_brain_to_vg_per_kg(dose, "neonatal_p0")
        print(f"  {dose:.2e} vg/g brain → {converted:.2e} vg/kg")

    print("\n=== Comparable Dose Pairs ===\n")
    print("PTC 3e11 vg/g ≈ Wilson 1.6e13 vg/kg")
    print("Wilson 1e12 vg/kg ≈ PTC 1.9e10 vg/g")
    print("Wilson 2e12 vg/kg ≈ PTC 3.8e10 vg/g")

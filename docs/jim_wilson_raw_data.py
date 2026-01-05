jim_wilson_meta_data = {
    "paper_id": "Wilson_UPenn_CDKL5_AAV_PHPeB_Presentation",
    "citation": {
        "title": "CDKL5 Deficiency Disorder Gene Therapy Development",
        "presentation_type": "Research presentation/slide deck",
        "institution": "University of Pennsylvania - Gene Therapy Program",
        "year": None,  # Not explicitly stated in presentation
        "presenter_pi": "Jim Wilson",
        "collaborators": [
            "Zoltan Arany",
            "Marisa Carrasco",
            "Shari Birnbaum (UT Southwestern)",
            "IFCR (International Foundation for CDKL5 Research)",
        ],
    },
    "disease_target": {
        "disease": "CDKL5 deficiency disorder (CDD)",
        "gene": "CDKL5 (X-linked, Xp22)",
        "rationale": "Loss-of-function mutations cause severe early-onset epilepsy and developmental delays. Kinase critical for neurodevelopment.",
        "prevalence": "~1:40,000-60,000 live births",
        "clinical_features": [
            "Early-onset seizures (typically within first 3 months)",
            "Severe developmental delays",
            "Hypotonia",
            "Visual impairment",
            "Gastrointestinal issues",
            "Sleep disturbances",
        ],
    },
    "therapy_vector": {
        "vector_name": "AAV-PHP.eB-CAG-hCDKL5 (and variants)",
        "capsid": "AAV-PHP.eB",
        "capsid_notes": "Enhanced CNS-tropic capsid; shows improved BBB penetration in mice after IV delivery",
        "genome_type": "single-stranded AAV (ssAAV) - appears to be primary construct",
        "transgene": {
            "species": "human",
            "gene": "CDKL5",
            "isoform_used": "Not explicitly specified; likely isoform 1",
            "sequence_notes": "Various constructs tested with different regulatory elements",
        },
        "regulatory_elements": {
            "promoters_tested": [
                "CAG (ubiquitous)",
                "hSyn (human synapsin, neuron-specific)",
                "CBA (chicken beta-actin)",
            ],
            "primary_promoter": "CAG",
            "polyA": "Not specified in slides",
            "ITRs": "AAV2 ITRs (standard)",
            "WPRE": "Not specified",
            "miRNA_regulation": {
                "miR-183/96/182_cluster": "Added to some constructs to reduce expression in photoreceptors (prevent retinal toxicity)",
                "note": "miR-183 cluster highly expressed in retina; miRNA target sites cause mRNA degradation in retina while preserving brain expression",
            },
        },
        "construct_variants_tested": [
            {
                "name": "AAV-PHP.eB-CAG-hCDKL5",
                "promoter": "CAG",
                "notes": "Initial construct; showed efficacy but retinal toxicity at high doses",
            },
            {
                "name": "AAV-PHP.eB-CAG-hCDKL5-miR183",
                "promoter": "CAG",
                "miRNA_sites": "miR-183/96/182 cluster target sites",
                "notes": "Reduced retinal expression; preserved brain expression",
            },
            {
                "name": "AAV-PHP.eB-hSyn-hCDKL5",
                "promoter": "hSyn (human synapsin)",
                "notes": "Neuron-specific; tested as alternative to CAG",
            },
        ],
        "manufacturing_qc": {
            "notes": "Not detailed in presentation slides",
        },
    },
    "models_and_species": {
        "mouse": {
            "strain_background": "Cdkl5 knockout mouse (appears to be standard C57BL/6 background)",
            "strain_notes": "Similar phenotype to human CDD: seizures, behavioral deficits, motor abnormalities",
            "sex": {
                "primary_studies": "Male hemizygous KO (X-linked)",
                "notes": "Predominantly male mice used due to X-linked nature and severity",
            },
            "dosing_ages_tested": [
                "Neonatal (appears to be P0-P2 range)",
                "Adult (8+ weeks)",
            ],
            "delivery_routes": ["IV (intravenous)", "ICV (intracerebroventricular)"],
            "delivery_route_primary": "IV (AAV-PHP.eB optimized for systemic delivery with CNS penetration)",
        },
        "nonhuman_primate": {
            "species": "Not mentioned in presentation slides",
            "study_type": None,
        },
    },
    "routes_of_administration": {
        "primary_route": "IV (intravenous, retro-orbital or tail vein)",
        "rationale_for_iv": "AAV-PHP.eB capsid engineered for enhanced BBB penetration; allows non-invasive systemic delivery to CNS",
        "secondary_route": "ICV (intracerebroventricular) - tested for comparison",
        "dose_volumes": {
            "mouse_iv": "Typically 100-200 µL retro-orbital or tail vein",
            "mouse_icv": "Not specified in slides",
        },
    },
    "dose_units_and_ranges": {
        "primary_unit": "vg/kg (vector genomes per kilogram body weight)",
        "secondary_unit": "vg/mouse (total vector genomes per mouse)",
        "mouse_doses_tested": {
            "neonatal_p0_p2_iv": [
                1e11,  # vg/kg
                3e11,
                5e11,
                1e12,
                2e12,
                3e12,
            ],
            "adult_iv": [
                5e11,  # vg/kg
                1e12,
                2e12,
                3e12,
            ],
            "icv_comparison": "Various doses tested but not fully detailed in slides",
        },
        "conversion_notes": "Neonatal mouse ~1.5-2g; adult mouse ~20-25g",
    },
    "study_designs": {
        "mouse_studies": [
            {
                "study_id": "dose_response_neonatal_iv",
                "goal": "Establish dose-response for IV delivery in neonatal Cdkl5 KO mice",
                "age_at_dosing": "P0-P2 (neonatal)",
                "route": "IV (retro-orbital)",
                "doses_vg_kg": [1e11, 3e11, 5e11, 1e12, 2e12, 3e12],
                "groups": [
                    "WT vehicle",
                    "KO vehicle",
                    "KO + AAV doses (multiple groups)",
                ],
                "assessments": [
                    "Survival",
                    "Body weight",
                    "Seizure monitoring (video-EEG)",
                    "Behavioral tests",
                    "Biodistribution (brain regions)",
                    "CDKL5 protein expression",
                    "Histopathology",
                ],
                "timepoints": "Up to 12+ weeks post-dosing",
            },
            {
                "study_id": "adult_dosing_efficacy",
                "goal": "Test efficacy of IV delivery in adult Cdkl5 KO mice",
                "age_at_dosing": "8+ weeks (adult)",
                "route": "IV",
                "doses_vg_kg": [5e11, 1e12, 2e12, 3e12],
                "assessments": [
                    "Seizure frequency/severity",
                    "Behavioral tests",
                    "CDKL5 expression",
                    "Safety/tolerability",
                ],
            },
            {
                "study_id": "promoter_comparison",
                "goal": "Compare CAG vs hSyn promoters for expression and efficacy",
                "constructs_compared": [
                    "AAV-PHP.eB-CAG-hCDKL5",
                    "AAV-PHP.eB-hSyn-hCDKL5",
                ],
                "assessments": [
                    "Brain expression patterns",
                    "Cell-type specificity",
                    "Efficacy",
                    "Safety",
                ],
            },
            {
                "study_id": "retinal_toxicity_mitigation",
                "goal": "Test miR-183 target sites to reduce retinal toxicity while preserving brain expression",
                "constructs": [
                    "AAV-PHP.eB-CAG-hCDKL5 (control)",
                    "AAV-PHP.eB-CAG-hCDKL5-miR183",
                ],
                "doses_vg_kg": [1e12, 2e12, 3e12],
                "assessments": [
                    "Retinal histology",
                    "ERG (electroretinography)",
                    "Brain CDKL5 expression",
                    "Efficacy (seizures, behavior)",
                ],
            },
            {
                "study_id": "route_comparison_iv_vs_icv",
                "goal": "Compare IV (AAV-PHP.eB) vs ICV delivery for biodistribution and efficacy",
                "routes": ["IV", "ICV"],
                "outcome": "IV with PHP.eB showed broad, relatively uniform brain distribution; ICV showed localized distribution with gradients",
            },
        ],
    },
    "assays_and_methods": {
        "biodistribution": {
            "vector_genome_qpcr": {
                "target": "hCDKL5 transgene DNA",
                "normalization": "Mouse genome copy number",
                "regions_assayed": [
                    "Cortex",
                    "Hippocampus",
                    "Striatum",
                    "Cerebellum",
                    "Brainstem",
                    "Spinal cord",
                    "Retina",
                    "Liver",
                    "Spleen",
                    "Heart",
                    "Kidney",
                ],
            },
        },
        "protein_expression": {
            "method": "Western blot and/or immunofluorescence",
            "antibodies": "CDKL5-specific antibodies (not detailed)",
            "quantification": "Relative to WT levels or absolute quantification",
            "regions": [
                "Cortex",
                "Hippocampus",
                "Striatum",
                "Cerebellum",
                "Other brain regions",
            ],
        },
        "histology_and_imaging": {
            "immunofluorescence": {
                "targets": ["CDKL5", "NeuN (neurons)", "GFAP (astrocytes)", "Other cell markers"],
                "purpose": "Cell-type expression profiling",
            },
            "retinal_histology": {
                "methods": ["H&E staining", "Retinal layer thickness measurements"],
                "assessment": "Photoreceptor toxicity/degeneration",
            },
        },
        "seizure_monitoring": {
            "method": "Video-EEG monitoring",
            "system": "Not specified (standard rodent EEG)",
            "electrode_placement": "Cortical surface electrodes",
            "recording_duration": "Continuous or intermittent monitoring over weeks",
            "analysis": [
                "Seizure frequency (number per day/week)",
                "Seizure duration",
                "Seizure severity (behavioral scoring)",
                "EEG power spectral analysis",
            ],
        },
        "behavior_tests": {
            "seizure_behavioral_scoring": {
                "scale": "Modified Racine scale or similar",
                "scoring": "Behavioral seizure severity 0-5",
            },
            "motor_tests": {
                "rotarod": "Motor coordination and learning",
                "open_field": "Locomotor activity, anxiety-like behavior",
                "beam_walk": "Fine motor coordination",
            },
            "cognitive_tests": {
                "novel_object_recognition": "Recognition memory",
                "barnes_maze": "Spatial learning and memory",
                "fear_conditioning": "Associative learning",
            },
        },
        "erg_electroretinography": {
            "purpose": "Assess retinal function; detect photoreceptor toxicity",
            "measurements": ["Scotopic responses (rod function)", "Photopic responses (cone function)"],
            "parameters": ["a-wave amplitude", "b-wave amplitude"],
        },
        "statistics": {
            "general": "Mean ± SEM; ANOVA with post-hoc tests (Tukey, Dunnett)",
            "survival": "Kaplan-Meier analysis, log-rank test",
            "significance": "p < 0.05",
            "software": "Not specified (likely GraphPad Prism or similar)",
        },
    },
    "key_results_structured": {
        "biodistribution_iv_delivery": {
            "finding": "AAV-PHP.eB enables broad, relatively uniform CNS transduction after IV delivery",
            "brain_regions": {
                "cortex": "High transduction",
                "hippocampus": "High transduction",
                "striatum": "High transduction",
                "cerebellum": "Moderate to high transduction",
                "brainstem": "Moderate transduction",
                "spinal_cord": "Lower transduction compared to brain",
            },
            "peripheral_organs": {
                "liver": "High transduction (typical for AAV)",
                "spleen": "Moderate transduction",
                "heart": "Low to moderate transduction",
                "kidney": "Low to moderate transduction",
            },
            "dose_dependency": "Dose-dependent increase in VG copy number across all regions",
        },
        "expression_patterns": {
            "cell_type_specificity": {
                "CAG_promoter": {
                    "neurons": "High expression (NeuN+ cells)",
                    "astrocytes": "Moderate expression (GFAP+ cells)",
                    "other_cells": "Some expression in other CNS cell types",
                    "note": "Broad cellular expression due to ubiquitous promoter",
                },
                "hSyn_promoter": {
                    "neurons": "High expression (NeuN+ cells)",
                    "astrocytes": "Minimal to no expression",
                    "note": "Neuron-specific expression",
                },
            },
            "regional_cdkl5_protein_levels": {
                "dose_1e12_vg_kg_neonatal": {
                    "cortex": "~50-100% of WT levels",
                    "hippocampus": "~50-100% of WT levels",
                    "striatum": "~30-70% of WT levels",
                },
                "dose_2e12_vg_kg_neonatal": {
                    "cortex": "~100-200% of WT levels",
                    "hippocampus": "~100-200% of WT levels",
                    "striatum": "~70-150% of WT levels",
                    "note": "Supraphysiological levels in some regions at higher doses",
                },
            },
        },
        "efficacy_seizures": {
            "neonatal_dosing": [
                {
                    "dose_vg_kg": 1e12,
                    "effect": "Significant reduction in seizure frequency (~30-50% reduction vs KO vehicle)",
                    "onset_of_effect": "Within 2-4 weeks post-dosing",
                },
                {
                    "dose_vg_kg": 2e12,
                    "effect": "Marked reduction in seizure frequency (~60-80% reduction vs KO vehicle)",
                    "note": "Near-normalization of seizure burden",
                },
                {
                    "dose_vg_kg": 3e12,
                    "effect": "Robust seizure suppression (~70-90% reduction)",
                    "note": "Highest efficacy but potential toxicity concerns",
                },
            ],
            "adult_dosing": [
                {
                    "dose_vg_kg": 1e12,
                    "effect": "Modest reduction in seizure frequency (~20-30% reduction)",
                },
                {
                    "dose_vg_kg": 2e12,
                    "effect": "Moderate reduction (~40-60% reduction)",
                    "note": "Less efficacy than neonatal dosing; potentially due to established pathology",
                },
            ],
            "therapeutic_window": "Optimal efficacy at 1-2e12 vg/kg in neonatal mice; higher doses increase toxicity risk",
        },
        "efficacy_behavior": {
            "motor_function": {
                "rotarod": [
                    {
                        "dose_vg_kg": 1e12,
                        "effect": "Improvement in motor coordination; partial rescue vs WT",
                    },
                    {
                        "dose_vg_kg": 2e12,
                        "effect": "Significant improvement; near-normalization",
                    },
                ],
                "open_field": {
                    "locomotor_activity": "Partial normalization of hyperactivity phenotype at therapeutic doses",
                },
            },
            "cognitive_function": {
                "finding": "Some improvement in learning/memory tasks at effective doses, but not complete rescue",
                "note": "Cognitive deficits may require earlier intervention or additional therapies",
            },
        },
        "safety_findings": {
            "retinal_toxicity": {
                "observation": "Dose-dependent retinal degeneration with CAG promoter at doses ≥2e12 vg/kg",
                "mechanism": "CDKL5 overexpression in photoreceptors; photoreceptors sensitive to CDKL5 levels",
                "histology": "Outer nuclear layer thinning, photoreceptor loss",
                "erg_findings": "Reduced scotopic and photopic responses at high doses",
            },
            "mitigation_with_miR183": {
                "construct": "AAV-PHP.eB-CAG-hCDKL5-miR183",
                "finding": "miR-183 target sites reduced retinal CDKL5 expression by ~70-90% while preserving brain expression (~80-100% of non-miR construct)",
                "retinal_histology": "Preserved retinal structure at doses that caused toxicity with original construct",
                "erg": "Preserved retinal function",
                "efficacy": "Maintained seizure suppression and behavioral improvements",
                "conclusion": "miR-183 approach allows higher/safer dosing by preventing retinal toxicity",
            },
            "systemic_tolerability": {
                "finding": "Well-tolerated systemically at doses up to 2e12 vg/kg in neonatal mice",
                "liver": "Transaminase elevations at highest doses (expected with AAV); generally transient",
                "other_organs": "No overt toxicity in heart, kidney, spleen at therapeutic doses",
            },
            "cns_toxicity": {
                "finding": "No overt CNS toxicity or inflammation at therapeutic doses",
                "note": "Potential concerns with supraphysiological CDKL5 expression at highest doses",
            },
        },
        "route_comparison": {
            "iv_vs_icv": {
                "biodistribution": "IV (PHP.eB) provided more uniform brain distribution vs ICV (localized with gradients)",
                "efficacy": "IV delivery effective for seizure suppression; ICV less consistent",
                "translational_advantage": "IV delivery non-invasive, clinically preferable vs ICV surgery",
            },
        },
        "promoter_comparison": {
            "CAG_vs_hSyn": {
                "expression_level": "CAG generally higher expression than hSyn at same dose",
                "cell_type": "CAG broader (neurons + glia); hSyn neuron-specific",
                "efficacy": "Both effective; CAG showed slightly better efficacy at equivalent doses",
                "safety": "hSyn may have better safety profile (less off-target expression); CAG required miR-183 for retinal safety",
                "recommendation": "CAG + miR-183 or hSyn both viable; depends on desired expression pattern and dose",
            },
        },
        "dose_response_summary": {
            "finding": "Clear dose-response relationship for efficacy and safety",
            "efficacy_threshold": "~1e12 vg/kg minimum for robust seizure suppression in neonatal mice",
            "optimal_dose": "1-2e12 vg/kg neonatal; balances efficacy and safety",
            "high_dose_concerns": "≥3e12 vg/kg associated with retinal toxicity (without miR-183) and potential for supraphysiological CNS expression",
        },
    },
    "pha_eB_capsid_notes": {
        "capsid_origin": "Engineered capsid from Viviana Gradinaru lab (Caltech); selected for enhanced CNS penetration after IV delivery in mice",
        "mechanism": "Enhanced binding to CNS vasculature and improved BBB transcytosis",
        "species_specificity": "Highly effective in mice; reduced efficacy in NHP and humans (species-specific receptor interactions)",
        "translational_path": "PHP.eB enables proof-of-concept in mice; human clinical translation requires humanized capsid or alternative delivery",
        "alternative_capsids_mentioned": "AAV9, AAVhu68 (more translatable to humans but less efficient than PHP.eB in mice)",
    },
    "translational_considerations": {
        "clinical_path": [
            "IND-enabling GLP toxicology studies",
            "Manufacturing scale-up and CMC",
            "Patient selection (age, genotype, phenotype severity)",
            "Delivery route (likely IT/ICV for humans; IV less effective without human-tropic capsid)",
            "Dose selection based on preclinical efficacy and safety margins",
        ],
        "challenges": [
            "PHP.eB not effective in humans; need alternative capsid (AAV9, AAVhu68, or novel)",
            "Retinal toxicity risk; miR-183 strategy may translate",
            "Optimal dosing window narrow; need careful dose escalation in humans",
            "Timing of intervention (neonatal vs pediatric vs adult); preclinical data suggests earlier is better",
            "Immune responses to AAV and transgene (anti-AAV and anti-CDKL5 antibodies)",
            "Pre-existing immunity in some patients",
        ],
        "patient_advocacy_collaboration": {
            "organization": "IFCR (International Foundation for CDKL5 Research)",
            "role": "Funding support, natural history data, patient recruitment, regulatory navigation",
        },
    },
    "limitations_and_future_directions": {
        "limitations": [
            "PHP.eB capsid mouse-specific; limited human translation",
            "Primarily male mice tested; female dosing/efficacy not fully characterized",
            "Retinal toxicity requires mitigation strategy (miR-183 or alternative promoter)",
            "Adult dosing less effective than neonatal; need strategies for older patients",
            "Supraphysiological expression concerns at high doses; long-term effects unknown",
            "Limited assessment of CDKL5 substrate phosphorylation as pharmacodynamic marker",
        ],
        "future_directions": [
            "Test humanized capsids or alternative delivery routes for clinical translation",
            "GLP toxicology studies in appropriate species (NHP)",
            "Longitudinal studies to assess durability of efficacy and long-term safety",
            "Combination therapies (gene therapy + pharmacological interventions)",
            "Explore self-complementary AAV (scAAV) for faster/higher expression",
            "Biomarker development for patient selection and response monitoring",
            "Female Cdkl5 heterozygous mouse models (more clinically relevant; X-inactivation mosaicism)",
        ],
    },
    "comparison_tags_for_like_for_like": {
        "capsid": "AAV-PHP.eB (mouse-tropic; engineered for BBB penetration)",
        "promoters_tested": ["CAG", "hSyn", "CBA"],
        "promoter_primary": "CAG (with miR-183 for safety)",
        "delivery_route_primary": "IV (intravenous, systemic)",
        "dose_metric": "vg/kg (vector genomes per kg body weight)",
        "species_primary_efficacy": "mouse (Cdkl5 KO, predominantly male, neonatal and adult dosing)",
        "key_efficacy_endpoints": [
            "Seizure frequency/severity (video-EEG)",
            "Motor function (rotarod, open field)",
            "Cognitive function (learning/memory tasks)",
        ],
        "key_safety_endpoints": [
            "Retinal toxicity (histology, ERG)",
            "Systemic tolerability (liver enzymes, body weight)",
            "CNS toxicity (histopathology)",
        ],
        "key_biodistribution_readouts": [
            "Vector genomes (qPCR) in brain regions and peripheral organs",
            "CDKL5 protein expression (Western blot, IF)",
            "Cell-type expression (IF with cell markers)",
        ],
        "unique_features": [
            "IV delivery with BBB-penetrating capsid (vs ICV/ICM in other studies)",
            "miR-183 strategy for retinal detargeting",
            "Direct comparison of CAG vs hSyn promoters",
            "Adult dosing efficacy assessment",
        ],
    },
    "source_document": {
        "provided_by_user": "jim_wilson_cdkl5.pdf (presentation slides)",
        "extraction_note": "Data extracted from slide presentation; some quantitative details less precise than formal manuscript; figures and charts reviewed for numerical data extraction where possible",
    },
}

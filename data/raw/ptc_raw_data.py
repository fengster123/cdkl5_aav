ptc_raw_data = {
    "paper_id": "Voronin2024_MolecularTherapy_CD KL5_AAV9_Syn_hCDKL5",
    "citation": {
        "title": "Preclinical studies of gene replacement therapy for CDKL5 deficiency disorder",
        "journal": "Molecular Therapy",
        "year": 2024,
        "volume_issue_pages": "Vol. 32 No. 10 (Oct 2024) (in press at time of excerpt)",
        "doi": "10.1016/j.ymthe.2024.07.012",
        "authors_first_last": ["Voronin", "Narasimhan", "Weetall"],
        "affiliations_summary": [
            "PTC Therapeutics, Inc (Warren, NJ, USA)",
            "NeuroDigitech (San Diego, CA, USA)",
        ],
    },
    "disease_target": {
        "disease": "CDKL5 deficiency disorder (CDD)",
        "gene": "CDKL5 (X-linked)",
        "rationale": "Monogenic loss-of-function; restore CDKL5 in CNS neurons for benefit.",
    },
    "therapy_vector": {
        "vector_name": "AAV9.Syn.hCDKL5",
        "capsid": "AAV9",
        "genome_type": "single-stranded AAV (ssAAV)",
        "transgene": {
            "species": "human",
            "gene": "CDKL5",
            "isoform_used": "Isoform 1 (predominant in adult brain; stated used here and in other published studies)",
            "sequence_notes": "codon-optimized cDNA (complementary DNA) (as described)",
        },
        "regulatory_elements": {
            "promoter": "synapsin (neuronal-specific)",
            "polyA": "bovine growth hormone polyadenylation signal (bGH pA)",
            "ITRs": "AAV2 ITRs",
            "WPRE": "mentioned in plasmid standard name; vector genome details beyond excerpt not fully specified here",
        },
        "cell_type_targeting_claims": {
            "expected": "neurons (synapsin promoter)",
            "observed": {
                "neurons": "hCDKL5 mRNA colocalized with NeuN+ cells (RNAscope/ISH)",
                "glia": "no colocalization with GFAP+ cells (RNAscope/ISH)",
            },
        },
        "manufacturing_qc": {
            "empty_capsids_fraction": 0.15,  # ~15% empty capsids
            "qc_methods": [
                "capsid PAGE + silver stain (ProteoSilver)",
                "genome integrity by alkaline gel",
                "nanopore DNA sequencing",
            ],
        },
    },
    "models_and_species": {
        "mouse": {
            "strain_background": "C57BL/6J background (B6.129(FVB)-Cdkl5tm1.1Joez/J; Jackson #021967)",
            "sex": {
                "biodistribution_study_1": "male and female homozygous KO",
                "behavior_studies_2_3": "male only",
            },
            "dosing_age": "PND0 (postnatal day 0)",
            "anesthesia": "hypothermia on wet ice ~5 min (PND0 pups)",
        },
        "nonhuman_primate": {
            "species": "cynomolgus macaque (Macaca fascicularis)",
            "sex_age_weight": "male; 28–37 months; 2.3–2.9 kg",
            "study_type": "non-GLP biodistribution/tolerability",
            "euthanasia_timepoint": "4 weeks post-dose",
        },
    },
    "routes_of_administration": {
        "compared_in_mouse": [
            "i.c.v. (intracerebroventricular)",
            "i.c.m. (intra-cisterna magna)",
        ],
        "selected_for_efficacy_mouse": "i.c.v.",
        "nhp": "i.c.v. (unilateral left ventricle or bilateral)",
        "dose_volumes": {
            "mouse_icv": "2 µL/hemisphere (4 µL total)",
            "mouse_icm": "3 µL total",
            "nhp": {
                "infusion_rate": "0.1 mL/min",
                "volume": "3 mL per dose site (unilateral) or 1.5 mL per site (bilateral)",
                "posture": "Trendelenburg up to 20 min post-dose",
            },
        },
    },
    "dose_units_and_ranges": {
        "primary_unit": "vg/g brain (vector genomes per gram brain)",
        "mouse_doses_tested": {
            "study_1_biodistribution_pd": [
                3.6e11,
                1.2e12,
                3.6e12,
            ],  # i.c.v.; plus i.c.m. 2.7e11, 9.0e11, 2.7e12
            "study_2_behavior_dose_response": [3e9, 3e10, 3e11],
            "study_3_behavior_additional": [3e11, 5e11],
        },
        "nhp_doses_tested": {
            "vg_per_g_brain_assumed_brain_weight_75g": [2.0e10, 2.0e11],
            "vg_per_animal": [1.5e12, 1.5e13],
            "administration": [
                "unilateral (2.0e10, 2.0e11)",
                "bilateral total 2.0e11",
            ],
        },
    },
    "study_designs": {
        "mouse_studies": [
            {
                "study_id": 1,
                "goal": "biodistribution + pharmacodynamics; compare i.c.v. vs i.c.m.",
                "groups_summary_from_table": {
                    "icv": ["vehicle", 3.6e11, 1.2e12, 3.6e12],
                    "icm": ["vehicle", 2.7e11, 9.0e11, 2.7e12],
                    "wt_controls": True,
                },
                "n_per_group": "typically 8 for i.c.v. KO groups; 10–12 for i.c.m. KO groups; WT n=8 (per Table 1 excerpt)",
                "timepoints": {
                    "35_37_days_post": [
                        "vector DNA (qPCR)",
                        "hCDKL5 mRNA (RT-qPCR)",
                        "CDKL5 protein (ECL)",
                        "phospho-EB2 (WB ratio)",
                    ],
                    "11_weeks_post": ["RNAscope ISH (hCDKL5 mRNA)"],
                },
                "brain_regions_assayed": [
                    "olfactory bulb",
                    "prefrontal cortex",
                    "striatum",
                    "hippocampus",
                    "motor/parietal cortex",
                    "cerebellum",
                    "midbrain/brainstem",
                ],
            },
            {
                "study_id": 2,
                "goal": "dose-response efficacy (behavior + morphology) after PND0 i.c.v.",
                "groups": [
                    "WT vehicle",
                    "KO vehicle",
                    "KO 3e9",
                    "KO 3e10",
                    "KO 3e11",
                ],
                "n_per_group": {
                    "WT_vehicle": 29,
                    "KO_vehicle": 25,
                    "KO_3e9": 27,
                    "KO_3e10": 23,
                    "KO_3e11": 30,
                },
                "timepoints": {
                    "11_weeks": ["hindlimb clasp (HLC)"],
                    "15_weeks": ["open-field test (OFT) distance"],
                    "17_weeks": ["fear conditioning (FC)"],
                    "18_weeks": [
                        "Golgi-Cox morphology",
                        "RNAscope ISH",
                        "CDKL5 protein",
                    ],
                },
            },
            {
                "study_id": 3,
                "goal": "additional efficacy at higher dose; refine OFT/FC relationship",
                "groups": ["WT vehicle", "KO vehicle", "KO 3e11", "KO 5e11"],
                "n_per_group": {
                    "WT_vehicle": 24,
                    "KO_vehicle": 22,
                    "KO_3e11": 23,
                    "KO_5e11": 24,
                },
                "timepoints": {
                    "14_weeks": [
                        "OFT distance",
                        "OFT mobility state (highly mobile time)",
                    ],
                    "16_weeks": ["fear conditioning"],
                    "17_19_weeks": ["ISH (~19w)", "CDKL5 protein (~19w)"],
                },
            },
        ],
        "nhp_study": {
            "goal": "biodistribution + tolerability after i.c.v.",
            "groups_from_table": [
                {
                    "group": 1,
                    "dose_vg_animal": 1.5e12,
                    "dose_vg_g_brain": 2.0e10,
                    "injection": "unilateral",
                    "n_males": 3,
                },
                {
                    "group": 2,
                    "dose_vg_animal": 1.5e13,
                    "dose_vg_g_brain": 2.0e11,
                    "injection": "unilateral",
                    "n_males": 3,
                },
                {
                    "group": 3,
                    "dose_vg_animal": 1.5e13,
                    "dose_vg_g_brain": 2.0e11,
                    "injection": "bilateral",
                    "n_males": 3,
                },
            ],
            "assessments": [
                "clinical observations",
                "body weight",
                "neurobehavioral observations",
                "hematology/coagulation/chemistry",
                "qPCR biodistribution (CNS + periphery)",
            ],
        },
    },
    "assays_and_methods": {
        "vector_genome_qpcr": {
            "target": "hCDKL5 DNA (primer/probe set provided in excerpt)",
            "normalization_ref": "mouse Tfrc copy number reference assay (VIC-MGB)",
            "standard": "linearized plasmid standard",
            "cycling": "UNG 45°C 5 min; 95°C 7 min; 40 cycles (95°C 15s, 60°C 1min)",
            "instrument": "Bio-Rad CFX384",
        },
        "transgene_mrna_rt_qpcr": {
            "standard": "human CDKL5 synthetic RNA (IDT transcript 4; #17508277; ref #296408196)",
            "normalization_ref": "mouse Tfrc (VIC-MGB)",
            "instrument": "QuantStudio 7 Pro",
            "cycling": "50°C 10 min; 95°C 1 min; 40 cycles (95°C 15s, 60°C 1min)",
        },
        "protein_quantification": {
            "cdkl5_protein_ecl_msd": {
                "platform": "Meso Scale Discovery (ECL)",
                "capture_ab": "EMD Millipore MABS1132",
                "detect_ab": "Invitrogen PA5-19506 + Sulfo-tag goat anti-rabbit",
                "input": "~500 µg/mL total protein per sample (final)",
                "output_normalization": "ECL signal / total protein; then expressed as % of WT",
            },
            "phospho_eb2_total_ratio_western": {
                "pEB2_antibody": "Covalab pS222 EB2 (pab01032-P)",
                "total_EB2_antibody": "Covalab mab71717",
                "readout": "pEB2 band / total EB2 band",
                "instrument": "Odyssey Imager",
            },
        },
        "ish_rnascope": {
            "platform": "RNAscope 2.5 LS RED ISH (ACD)",
            "probe_specificity": "human CDKL5 mRNA; no cross-reactivity to mouse Cdkl5",
            "scoring": {
                "dots_per_cell_score_0_4": {
                    "0": "<1 dot/10 cells",
                    "1": "1–3 dots/cell",
                    "2": "4–9 dots/cell, few/no clusters",
                    "3": "10–15 dots/cell and/or <10% dots in clusters",
                    "4": ">15 dots/cell and/or >10% dots in clusters",
                },
                "percent_positive_bins": {
                    "study_1_bins": ["0%", "1–25%", "26–50%", "51–75%", "76–100%"],
                    "studies_2_3_bins": [
                        "0%",
                        "1–10%",
                        "11–25%",
                        "26–50%",
                        "51–75%",
                        "76–100%",
                    ],
                },
                "cell_identity": "double-positive NeuN + hCDKL5 mRNA used for % positive",
            },
        },
        "behavior": {
            "hindlimb_clasp": {
                "protocol": "3 consecutive 10s tail suspension trials; video scored by 3 blinded observers",
                "scoring": {
                    0: "normal extension",
                    1: "one limb retracted",
                    2: "both partially retracted",
                    3: "both fully retracted/touching abdomen",
                },
            },
            "open_field_test": {
                "arena": "40 cm x 40 cm",
                "duration": "30 min",
                "analysis": "EthoVision; distance traveled; mobility state (highly mobile/mobile/immobile by pixel change)",
            },
            "fear_conditioning": {
                "training": "2 min explore; 3 CS/US pairings; CS=30s tone 9kHz 80dB; US=2s 0.5mA shock at 28s into tone; 1 min intervals; +2 min after",
                "testing": "24h later context 5 min; freezing defined as lack of movement ≥2s (EthoVision XT15)",
                "primary_readout": "% freezing post-training (context/cue details in excerpt)",
            },
        },
        "morphology": {
            "golgi_cox_ca1_pyramidal": {
                "vendor": "NeuroDigitech",
                "readouts": [
                    "basal/apical dendritic length",
                    "spine count",
                    "spine density",
                    "Sholl intersections (30 µm steps)",
                ],
                "note_on_spines": "only spines orthogonal to shaft sampled; above/below shaft not sampled",
                "stats": "one-way and two-way ANOVA (per methods)",
            },
        },
        "statistics": {
            "general": "mean ± SEM; one-way ANOVA with Dunnett multiple comparisons vs KO vehicle; p<0.05 significant",
            "percent_improvement_formulas": {
                "when_pathology_decreases_value": "((Treated - KO) * 100) / (WT - KO)  # e.g., fear conditioning",
                "when_pathology_increases_value": "((Treated - WT) * 100) / (KO - WT)  # e.g., hindlimb clasp",
            },
            "software": "GraphPad Prism 10.0.0",
        },
    },
    "key_results_structured": {
        "route_comparison_mouse": {
            "finding": "i.c.v. gave broader/higher brain distribution than i.c.m., except cerebellum where i.c.m. relatively better",
            "example_lowest_icv_dose_3_6e11_vg_g": {
                "cdkl5_protein_percent_of_wt": {
                    "olfactory_bulb": 96,
                    "hippocampus": 76,
                    "striatum": 35,
                    "cerebellum": 41,
                }
            },
        },
        "pharmacodynamics_activity": {
            "substrate_marker": "EB2 phosphorylation (pEB2/total EB2)",
            "ko_baseline_percent_wt": 18,  # reported 18% (also 19% elsewhere)
            "dose_response_icv_5_weeks": [
                {
                    "dose_vg_g": 3.6e11,
                    "pEB2_total_percent_wt": 47,
                    "cdkl5_protein_percent_wt_hippocampus_example": 76,
                },
                {
                    "dose_vg_g": 1.2e12,
                    "pEB2_total_percent_wt": 82,
                    "cdkl5_protein_percent_wt_hippocampus_example": 210,
                    "note": "pEB2 near-normalized; CDKL5 over WT in hippocampus example",
                },
                {
                    "dose_vg_g": 3.6e12,
                    "pEB2_total_percent_wt": 112,
                    "cdkl5_protein_percent_wt_hippocampus_example": 430,
                },
            ],
            "correlations_reported": [
                "vector genomes ↔ hCDKL5 mRNA",
                "CDKL5 protein ↔ pEB2/total EB2 (hippocampus example)",
            ],
        },
        "biodistribution_rnascope_mouse": {
            "cell_type": "neurons only (NeuN+); not GFAP+ glia",
            "study_1_11_weeks_bins": {
                "icv_3_6e11": "1–25% NeuN+hCDKL5 (overall lowest range)",
                "icv_1_2e12": "26–50% NeuN+hCDKL5",
                "icv_3_6e12": "51–75% NeuN+hCDKL5",
                "icm_escalation": "no global increase with dose; aligns with limited protein by ECL",
            },
            "broad_distribution_note": "authors state up to ~75% of neurons can be transfected after PND0 i.c.v. at high dose (based on ISH).",
        },
        "behavior_mouse": {
            "hindlimb_clasp": [
                {
                    "study": 2,
                    "timepoint": "11 weeks",
                    "dose_vg_g": 3e11,
                    "effect": "complete prevention/normalization vs KO vehicle",
                    "stats_note": "p < 0.001 (as described)",
                },
                {"study": 2, "dose_vg_g": 3e9, "effect": "no improvement"},
                {
                    "study": 2,
                    "dose_vg_g": 3e10,
                    "effect": "no significant reduction",
                },
            ],
            "open_field_hyperactivity": [
                {
                    "study": 2,
                    "timepoint": "15 weeks",
                    "doses_vg_g": [3e9, 3e10, 3e11],
                    "effect": "no reduction in distance",
                },
                {
                    "study": 3,
                    "timepoint": "14 weeks",
                    "dose_vg_g": 5e11,
                    "effect": "mitigated hyperactivity; distance ~43% normalization (not significant p=0.39 per text due to small genotype window)",
                },
                {
                    "study": 3,
                    "timepoint": "14 weeks",
                    "dose_vg_g": 5e11,
                    "effect_detail": "highly-mobile time reduced 46%",
                    "stats_note": "p < 0.01",
                },
            ],
            "fear_conditioning_learning_memory": [
                {
                    "study": 2,
                    "timepoint": "17 weeks",
                    "dose_vg_g": 3e11,
                    "effect": "44% recovery; significant",
                    "stats_note": "p < 0.05",
                },
                {
                    "study": 2,
                    "doses_vg_g": [3e9, 3e10],
                    "effect": "no significant improvement",
                },
                {
                    "study": 3,
                    "timepoint": "16 weeks",
                    "dose_vg_g": 3e11,
                    "effect": "62% improvement (not significant)",
                },
                {
                    "study": 3,
                    "timepoint": "16 weeks",
                    "dose_vg_g": 5e11,
                    "effect": "complete normalization",
                    "stats_note": "p < 0.01",
                },
            ],
        },
        "neuronal_morphology_mouse": {
            "golgi_cox_ca1": {
                "baseline_ko_vs_wt": "KO had reduced dendritic lengths, spine counts, spine densities, and reduced branching (Sholl) vs WT",
                "treatment_effect": [
                    {
                        "dose_vg_g": 3e10,
                        "effect": "significant improvements in dendritic measures (dose-dependent)",
                    },
                    {
                        "dose_vg_g": 3e11,
                        "effect": "near-normalization; more pronounced than 3e10",
                    },
                ],
            }
        },
        "expression_vs_behavior_summary_table2": {
            # values as reported in Table 2 excerpt; note: these are study-level summaries
            "dose_vg_g_to_cdkl5_protein_percent_wt_mean_sem": {
                "vehicle": {"HPC": ">1.5", "cortex": ">1.5", "cerebellum": ">1.5"},
                "3e9": {
                    "HPC": "1.8 ± 0.3",
                    "cortex": "1.3 ± 0.2",
                    "cerebellum": "1.0 ± 0.2",
                },
                "3e10": {
                    "HPC": "3.9 ± 1.0",
                    "cortex": "2.2 ± 0.6",
                    "cerebellum": "0.9 ± 0.2",
                },
                "3e11_study2": {
                    "HPC": "33 ± 12",
                    "cortex": "30 ± 14",
                    "cerebellum": "10 ± 2",
                },
                "3e11_study3": {
                    "HPC": "123 ± 32",
                    "cortex": "73 ± 22",
                    "cerebellum": "18 ± 5",
                },
                "5e11_study3": {
                    "HPC": "347 ± 98",
                    "cortex": "136 ± 21",
                    "cerebellum": "33 ± 9",
                },
            },
            "dose_vg_g_to_rnascope_summary": {
                "vehicle": {"score": "0", "NeuN+hCDKL5_percent_bin": "0 (3/3)"},
                "3e9": {
                    "score": "2–3",
                    "NeuN+hCDKL5_percent_bin": "<1 (2/3), 1–10 (1/3)",
                },
                "3e10": {"score": "3–4", "NeuN+hCDKL5_percent_bin": "1–10 (3/3)"},
                "3e11_study2": {
                    "score": "3–4",
                    "NeuN+hCDKL5_percent_bin": "11–25 (3/3)",
                },
                "3e11_study3": {
                    "score": "3–4",
                    "NeuN+hCDKL5_percent_bin": "26–50 (3/3)",
                },
                "5e11_study3": {
                    "score": "3–4",
                    "NeuN+hCDKL5_percent_bin": "26–50 (3/3)",
                },
            },
            "claimed_efficacy_threshold": "functional improvements at ~3e11 to 5e11 vg/g; lower doses limited/none; authors associate with needing broad distribution (~≥50% neurons).",
        },
        "nhp_biodistribution_and_safety": {
            "cns_distribution": "measurable transduction throughout brain; dose-dependent; lowest in putamen; cerebellum/hindbrain not sampled",
            "unilateral_vs_bilateral": "no overt biodistribution differences",
            "periphery": "significant exposure in peripheral organs, especially liver",
            "tolerability": "no mortality; no AAV-related clinical/neurological observations; no body weight, hematology, coagulation, or chemistry changes (over 4 weeks)",
        },
        "toxicity_notes": {
            "mouse": "no overt toxicity noted at any dose in excerpt",
            "high_mouse_dose_noted": "3.6e12 vg/g mouse brain (study 1) without overt toxicity",
        },
    },
    "limitations_noted_by_authors": [
        "Only male Cdkl5 KO mice used for behavior; female dose-response not done.",
        "Did not assess all human-relevant phenotypes (e.g., seizures, autistic behaviors).",
        "NHP doses lower than highest mouse doses; more safety evaluation needed.",
        "Broad biodistribution required; suggests need for improved capsid / lower titer strategies.",
        "Unclear risk of CDKL5 overexpression; duplications reported but not definitive; GLP tox may clarify.",
    ],
    "data_and_code_availability": "Data available from authors upon request.",
    "comparison_tags_for_like_for_like": {
        # useful for aligning across papers
        "capsid": "AAV9",
        "promoter": "Synapsin (neuron-specific)",
        "delivery_route_primary": "i.c.v. CSF delivery",
        "dose_metric": "vg/g brain",
        "species_primary_efficacy": "mouse (Cdkl5 KO, male, PND0 dosing)",
        "key_pd_marker": "pEB2/total EB2",
        "key_behavior_endpoints": ["HLC", "OFT", "Fear conditioning"],
        "key_morphology_endpoints": [
            "CA1 Golgi-Cox dendritic length",
            "spine count/density",
            "Sholl branching",
        ],
        "key_biodistribution_readouts": [
            "vector genomes (qPCR)",
            "hCDKL5 mRNA (RT-qPCR)",
            "RNAscope ISH % NeuN+ cells",
            "CDKL5 protein (ECL/MSD)",
        ],
    },
    "source_document": {
        "provided_by_user": "ptc_cdkl5.pdf (text excerpt)",
        "extraction_scope_note": "Dictionary reflects only the content you pasted; figures/tables referenced but not fully digitized here.",
    },
}


# NOTE THAT AS OF 2025-01-05, the comparison_report.md is NOT accurate. we have yet checked the raw_data.py files, ie they might not reflect the true data presented in the pdf

# CDKL5 AAV Gene Therapy Research Comparison



A comprehensive comparison of two AAV gene therapy approaches for CDKL5 Deficiency Disorder (CDD):
- **PTC Therapeutics**: AAV9 + Synapsin promoter + ICV delivery
- **University of Pennsylvania (Jim Wilson lab)**: AAV-PHP.eB + CAG promoter + IV delivery

## Overview

This repository contains structured data extraction, normalization, and side-by-side comparison of preclinical AAV gene therapy studies for CDKL5 deficiency disorder. The goal is to enable like-for-like comparisons despite different methodologies, identify convergent findings, and assess translational potential.

## Key Findings

### Convergent (Both Studies Agree)
- ✅ Therapeutic efficacy achieved at **50-200% WT CDKL5 brain levels**
- ✅ Clear dose-response relationships
- ✅ Motor and behavioral improvements demonstrated
- ✅ CNS safe at therapeutic doses
- ✅ Overexpression risk flagged at >200% WT levels

### Divergent (Different Trade-offs)
- PTC more immediately **clinically translatable** (AAV9-ICV ready)
- Wilson has **stronger seizure data** (primary clinical endpoint)
- Wilson needs **capsid change** for humans (PHP.eB mouse-specific)
- Retinal toxicity: Wilson identified + mitigated; PTC not reported

## Repository Structure

```
cdkl5_aav/
├── README.md                    # This file
├── ai_prompts.md               # Original project prompts and goals
├── .gitignore                  # Git ignore rules
│
├── data/                       # All data files
│   ├── raw/                    # Raw extracted data from papers
│   │   ├── ptc_cdkl5.pdf              # PTC source paper
│   │   ├── ptc_raw_data.py            # PTC extracted data (Python dict)
│   │   ├── jim_wilson_cdkl5.pdf       # Wilson source presentation
│   │   └── jim_wilson_raw_data.py     # Wilson extracted data (Python dict)
│   │
│   └── processed/              # Processed/normalized data
│       └── comparison_data.py         # Normalized comparison data + conversion functions
│
├── analysis/                   # Analysis plans and methodologies
│   └── comparison_plan.md             # Detailed comparison methodology and plan
│
├── reports/                    # Final comparison reports
│   └── comparison_report.md           # Comprehensive side-by-side comparison report
│
└── cdkl5_aav/                  # Python package (future analysis scripts)
    └── __init__.py
```

## Quick Start

### 1. View the Comparison Report
The main deliverable is the comprehensive comparison report:

```bash
cat reports/comparison_report.md
```

**Key sections:**
- Vector design & delivery comparison
- Dosing comparison (normalized to comparable units)
- Efficacy across motor, cognitive, seizure, and morphology endpoints
- Safety profiles
- Translational readiness assessment
- Convergent vs divergent findings

### 2. Access Raw Data
All extracted data from source papers is in Python dictionary format:

```python
# PTC data
from data.raw.ptc_raw_data import ptc_raw_data

# Wilson data
from data.raw.jim_wilson_raw_data import jim_wilson_raw_data

# Example: View PTC dosing info
print(ptc_raw_data['dose_units_and_ranges'])
```

### 3. Use Comparison Data & Conversion Functions
Normalized data with dose conversion utilities:

```python
from data.processed.comparison_data import (
    vg_per_kg_to_vg_per_g_brain,
    vg_per_g_brain_to_vg_per_kg,
    DOSE_COMPARISON,
    EFFICACY_MOTOR,
    EFFICACY_COGNITIVE,
    SAFETY_COMPARISON
)

# Convert Wilson dose to PTC units
wilson_dose = 1e12  # vg/kg
ptc_equivalent = vg_per_kg_to_vg_per_g_brain(wilson_dose, age="neonatal_p0")
print(f"{wilson_dose:.2e} vg/kg ≈ {ptc_equivalent:.2e} vg/g brain")
# Output: 1.00e+12 vg/kg ≈ 1.88e+10 vg/g brain

# Access normalized efficacy data
print(EFFICACY_MOTOR['ptc']['hindlimb_clasp'])
print(EFFICACY_COGNITIVE['wilson']['fear_conditioning'])
```

## Data Dictionary Structure

Both raw data files (`ptc_raw_data.py` and `jim_wilson_raw_data.py`) follow a consistent schema:

```python
{
    "paper_id": "...",
    "citation": {...},
    "disease_target": {...},
    "therapy_vector": {
        "capsid": "...",
        "promoter": "...",
        "regulatory_elements": {...}
    },
    "models_and_species": {...},
    "routes_of_administration": {...},
    "dose_units_and_ranges": {...},
    "study_designs": {...},
    "assays_and_methods": {...},
    "key_results_structured": {
        "biodistribution": {...},
        "efficacy": {...},
        "safety": {...}
    },
    "comparison_tags_for_like_for_like": {...}
}
```

See `analysis/comparison_plan.md` for detailed methodology on how these structures enable comparison.

## Key Comparison Insights

### Dose Normalization Challenge
- **PTC uses**: vg/g brain (direct CNS measurement)
- **Wilson uses**: vg/kg body weight (systemic dosing)
- **Solution**: Conversion functions in `comparison_data.py` using mouse biology parameters
  - Neonatal P0 mouse: ~1.5g body, ~0.08g brain
  - Conversion: 1×10¹² vg/kg ≈ 1.9×10¹⁰ vg/g brain

### Efficacy Threshold (Convergent Finding)
Both studies converge on **50-100% WT CDKL5 brain levels** as minimum for therapeutic benefit:
- PTC: 3-5×10¹¹ vg/g administered → 33-347% WT achieved
- Wilson: 1-2×10¹² vg/kg administered → 50-200% WT achieved

Despite ~10-fold difference in administered dose, **actual brain tissue levels overlap** at therapeutic window.

### Critical Gaps Identified

**PTC Study:**
- ❌ No seizure assessment (video-EEG) - primary clinical feature of CDD
- ❓ No retinal safety assessment reported

**Wilson Study:**
- ⚠️ Limited morphology assessment (dendrites, spines)
- ❌ PHP.eB capsid mouse-specific (not translatable to humans)

**Both Studies:**
- Limited adult dosing data (both focused on neonatal)
- Primarily male mice (females more clinically relevant for X-linked disease)
- Long-term durability unknown (longest ~17-19 weeks)

## Translational Assessment

### Clinical Readiness

| Criterion | PTC | Wilson |
|-----------|-----|--------|
| **Capsid Translatability** | ✅ High (AAV9 validated) | ❌ Low (need human alternative) |
| **Delivery Translatability** | ⚠️ Moderate (surgery required) | ✅ High (IF capsid solved) |
| **Manufacturing** | ✅ Ready | ⚠️ Need new capsid |
| **Preclinical Efficacy** | ⚠️ Good (no seizure data) | ✅ Excellent (seizure data) |
| **Safety Profile** | ✅ Good | ✅ Good (retinal risk mitigated) |

**Timeline to Clinic:**
- **PTC**: ~2-3 years (AAV9-ICV ready for IND)
- **Wilson**: ~5-7 years (need human-compatible capsid development)

### Recommended Path Forward

**Near-term (2-5 years):**
- Advance **PTC approach** (AAV9-ICV) to clinic
- **Add seizure monitoring** as primary endpoint
- **Assess retinal safety** proactively

**Long-term (5-10 years):**
- Develop **AAV9-IV or AAVhu68-IV** (human-compatible systemic delivery)
- Incorporate **miR-183 retinal detargeting** strategy
- Combine **Wilson's seizure rigor** with **PTC's morphology assessments**

## Citations

### PTC Study
Voronin, D.V., Narasimhan, M., Weetall, M., et al. (2024). Preclinical studies of gene replacement therapy for CDKL5 deficiency disorder. *Molecular Therapy*, 32(10). doi: 10.1016/j.ymthe.2024.07.012

### Wilson Study
Wilson, J., et al. CDKL5 Deficiency Disorder Gene Therapy Development. University of Pennsylvania Gene Therapy Program presentation (collaboration with IFCR - International Foundation for CDKL5 Research).

## Usage Examples

### Example 1: Compare Efficacy at Similar Brain Doses

```python
from data.processed.comparison_data import EXPRESSION_COMPARISON, EFFICACY_MOTOR

# Find PTC dose achieving ~100-200% WT CDKL5
ptc_data = EXPRESSION_COMPARISON['ptc']['hippocampus']
# Result: 3e11 vg/g achieves 123% WT (study 3)

# Find Wilson dose achieving similar levels
wilson_data = EXPRESSION_COMPARISON['wilson']['hippocampus']
# Result: 1-2e12 vg/kg achieves 100-200% WT

# Compare motor efficacy at these doses
print("PTC motor efficacy at 3e11 vg/g:")
print(EFFICACY_MOTOR['ptc']['hindlimb_clasp'][2])  # Complete normalization

print("\nWilson motor efficacy at 1-2e12 vg/kg:")
print(EFFICACY_MOTOR['wilson']['rotarod'][0])  # Partial rescue at 1e12
print(EFFICACY_MOTOR['wilson']['rotarod'][1])  # Near-normalization at 2e12

# Conclusion: Convergent - both show motor improvements at ~100-200% WT doses
```

### Example 2: Safety Window Analysis

```python
from data.processed.comparison_data import SAFETY_COMPARISON, SUMMARY_COMPARISON

# Check retinal safety
ptc_retinal = SAFETY_COMPARISON['ptc']['retinal_toxicity']
wilson_retinal = SAFETY_COMPARISON['wilson']['retinal_toxicity']

print("PTC retinal safety:", ptc_retinal['observed'])
print("Wilson retinal safety:", wilson_retinal['observed'])
print("Wilson mitigation:", wilson_retinal['mitigation'])

# Optimal therapeutic doses
optimal = SUMMARY_COMPARISON['optimal_doses']
print("\nPTC optimal range:", optimal['ptc']['range_vg_g'])
print("Wilson optimal range:", optimal['wilson']['range_vg_kg_neonatal'])
print("Wilson brain equivalent:", optimal['wilson']['range_vg_g_brain_equivalent'])
```

### Example 3: Generate Custom Comparison Table

```python
from data.processed.comparison_data import DOSE_COMPARISON, vg_per_kg_to_vg_per_g_brain

# Create dose equivalence table
print("Dose Equivalence Table (Neonatal P0)")
print("-" * 60)
print(f"{'PTC (vg/g brain)':<20} {'Wilson (vg/kg)':<20} {'Normalized (vg/g)':<20}")
print("-" * 60)

ptc_doses = [3e9, 3e10, 3e11, 5e11]
wilson_doses = [1e11, 5e11, 1e12, 2e12, 3e12]

for ptc_dose in ptc_doses:
    normalized = ptc_dose
    print(f"{ptc_dose:<20.2e} {'-':<20} {normalized:<20.2e}")

print()
for wilson_dose in wilson_doses:
    normalized = vg_per_kg_to_vg_per_g_brain(wilson_dose, "neonatal_p0")
    print(f"{'-':<20} {wilson_dose:<20.2e} {normalized:<20.2e}")
```

## Analysis Workflow

The analysis followed this systematic workflow (documented in `analysis/comparison_plan.md`):

1. **Data Extraction**: Manually extracted all data from PDFs into structured Python dictionaries
2. **Normalization**: Created conversion functions to normalize dose metrics
3. **Like-for-Like Mapping**: Aligned comparable endpoints across studies
4. **Comparison Analysis**: Generated side-by-side tables for all dimensions
5. **Convergence Assessment**: Identified which findings point in same vs different directions
6. **Translational Evaluation**: Assessed clinical readiness and path forward

## Future Work

### Immediate Next Steps
1. Add third study when available (e.g., other academic groups, Jaguar/Taysha)
2. Create visualization scripts (dose-response curves, biodistribution heatmaps)
3. Develop statistical comparison framework (where quantitative data allows)

### Extended Analysis
1. Add patient natural history data (IFCR registry) for context
2. Compare to other CNS gene therapy precedents (SMA, Rett, etc.)
3. Pharmacoeconomic modeling (cost-effectiveness comparison)
4. Regulatory pathway analysis (FDA/EMA precedents)

## Contributing

This is a research analysis repository. To add new studies or update comparisons:

1. Add raw PDF to `data/raw/`
2. Create `{study_name}_raw_data.py` following the schema in existing files
3. Update `data/processed/comparison_data.py` with new study data
4. Regenerate `reports/comparison_report.md` with new comparisons

## License

This repository contains data extraction and analysis for research purposes only. Original source data copyrights remain with respective authors/publishers.

## Contact

For questions or collaboration:
- International Foundation for CDKL5 Research (IFCR): https://cdkl5.com
- PTC Therapeutics: https://www.ptcbio.com
- Penn Gene Therapy Program: https://www.med.upenn.edu/gtap/

---

**Last Updated**: 2026-01-05
**Analysis Version**: 1.0
**Studies Compared**: 2 (PTC 2024, Wilson UPenn presentation)

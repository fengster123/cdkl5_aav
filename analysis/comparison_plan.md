# Plan: Side-by-Side Comparison of CDKL5 AAV Gene Therapy Approaches

## Objective
Create reader-friendly comparison tables/visualizations that highlight:
1. What differs between PTC and Wilson approaches
2. What points in the same direction (convergent findings)
3. Enable assessment of whether both methods are equally viable or if one is superior

## Key Challenges to Address

### 1. Dose Metric Conversion
- **PTC uses**: vg/g brain (vector genomes per gram brain tissue)
- **Wilson uses**: vg/kg body weight
- **Need to normalize** for fair comparison
  - Mouse brain weight: ~0.4-0.5g (adult), ~0.05-0.1g (neonatal P0)
  - Mouse body weight: ~20-25g (adult), ~1.5-2g (neonatal P0)
  - Conversion factor depends on age at dosing

### 2. Different Delivery Routes
- **PTC**: ICV (direct CNS injection)
- **Wilson**: IV (systemic with BBB penetration)
- **Implication**: Different biodistribution patterns, peripheral exposure profiles
- **Comparison strategy**: Focus on CNS tissue levels achieved, not just dose administered

### 3. Different Timing of Dosing
- **PTC**: Neonatal P0 (postnatal day 0)
- **Wilson**: Both neonatal (P0-P2) and adult (8+ weeks)
- **Comparison strategy**: Compare neonatal-to-neonatal for primary analysis; note adult data separately

### 4. Different Efficacy Endpoints
- **PTC**: Hindlimb clasping, open field activity, fear conditioning, morphology
- **Wilson**: Seizure frequency/severity (video-EEG), motor tests, cognitive tests
- **Overlap**: Motor function, some behavioral measures
- **Challenge**: PTC didn't directly measure seizures; Wilson has limited morphology data

## Proposed Comparison Structure

### Section 1: Vector Design & Delivery
**Side-by-side table format:**

| Feature | PTC (AAV9) | Wilson (PHP.eB) | Interpretation |
|---------|------------|-----------------|----------------|
| Capsid | AAV9 | AAV-PHP.eB | Different: Wilson optimized for IV BBB crossing |
| Promoter | Synapsin (neuron-specific) | CAG (ubiquitous) + miR-183 | Different strategy: PTC cell-type restriction, Wilson expression + detargeting |
| Delivery Route | ICV (direct CNS) | IV (systemic) | Different: PTC invasive but targeted; Wilson non-invasive but broader exposure |
| Clinical Translatability | High (AAV9 used clinically) | Low (PHP.eB mouse-specific) | PTC more translatable |
| Peripheral Exposure | Lower (CNS-directed) | Higher (systemic IV) | Wilson requires more safety monitoring |

### Section 2: Dosing Comparison (Normalized)
**Challenge**: Convert both to common metric (vg/g brain achieved)

**Approach**:
1. For PTC: doses already in vg/g brain
2. For Wilson: estimate brain dose from body dose
   - Neonatal P0 mouse: ~1.5g body, ~0.08g brain → multiply vg/kg by 0.0015 / 0.08 = 0.01875
   - Adult mouse: ~22g body, ~0.45g brain → multiply vg/kg by 0.022 / 0.45 = 0.049

**Table format:**

| Study | Dose Level | Administered Dose | Estimated Brain Dose (vg/g) | Notes |
|-------|------------|-------------------|----------------------------|--------|
| PTC Low | 3e9 vg/g | 3e9 vg/g (ICV) | 3e9 | Direct measurement |
| Wilson Low | 1e11 vg/kg (P0) | 1e11 vg/kg (IV) | ~1.9e9 | Estimated from biodistribution |
| PTC Mid | 3e10 vg/g | 3e10 vg/g (ICV) | 3e10 | Direct measurement |
| Wilson Mid | 1e12 vg/kg (P0) | 1e12 vg/kg (IV) | ~1.9e10 | Estimated |
| PTC High | 3e11 vg/g | 3e11 vg/g (ICV) | 3e11 | Direct measurement |
| Wilson High | 2e12 vg/kg (P0) | 2e12 vg/kg (IV) | ~3.8e10 | Estimated |

**Note**: Actual brain tissue levels should be compared using CDKL5 protein expression data (% of WT)

### Section 3: Biodistribution & Expression
**Compare**: Brain regional expression, cell-type specificity, peripheral exposure

**Table format:**

| Measure | PTC | Wilson | Convergence? |
|---------|-----|--------|--------------|
| Cell Type Specificity | Neurons only (Syn promoter) | Neurons + some glia (CAG) | Different but both achieve neuronal expression |
| Brain Distribution | Broad (ICV can reach most regions) | Broad (IV + PHP.eB) | Convergent: both achieve wide CNS coverage |
| % Neurons Transduced | Up to ~75% (high dose) | Not quantified by % | Partial data |
| Regional CDKL5 Protein | Hippocampus: 33-347% WT (dose-dependent) | Hippocampus: 50-200% WT (dose-dependent) | Convergent: both achieve near/above WT levels |
| Peripheral Exposure | Lower (ICV route) | Higher (IV route, liver ++++) | Divergent: safety consideration |

### Section 4: Efficacy Comparison
**Strategy**: Compare overlapping endpoints; note unique endpoints separately

#### 4A. Motor Function
| Test | PTC Results | Wilson Results | Convergence |
|------|-------------|----------------|-------------|
| Hindlimb Clasping | Complete normalization at 3e11 vg/g | Not tested | N/A |
| Rotarod | Not tested | Improvement/normalization at 1-2e12 vg/kg | N/A |
| Open Field Activity | Partial mitigation at 5e11 vg/g (43% improvement) | Partial normalization at therapeutic doses | Convergent: both improve hyperactivity |

#### 4B. Cognitive/Learning
| Test | PTC Results | Wilson Results | Convergence |
|------|-------------|----------------|-------------|
| Fear Conditioning | Complete normalization at 5e11 vg/g; 44-62% at 3e11 vg/g | Some improvement but incomplete rescue | Convergent: both show learning/memory benefits |
| Novel Object Recognition | Not tested | Tested (partial rescue) | N/A |

#### 4C. Seizure Control
| Measure | PTC Results | Wilson Results | Convergence |
|---------|-------------|----------------|-------------|
| Seizure Frequency | Not directly measured | 60-90% reduction at 1-2e12 vg/kg (neonatal) | N/A (PTC didn't assess) |
| Note | PTC didn't include video-EEG | Wilson primary endpoint | Critical gap in PTC study |

#### 4D. Neuronal Morphology
| Measure | PTC Results | Wilson Results | Convergence |
|---------|-------------|----------------|-------------|
| Dendritic Length | Near-normalization at 3e11 vg/g | Not extensively tested | N/A |
| Spine Density | Improved at 3e10-3e11 vg/g | Not extensively tested | N/A |
| Sholl Analysis | Improved branching at 3e11 vg/g | Not tested | N/A |

### Section 5: Safety Profile
| Safety Parameter | PTC | Wilson | Convergence |
|------------------|-----|--------|-------------|
| Retinal Toxicity | Not reported | Dose-dependent; mitigated with miR-183 | Wilson identified risk; PTC didn't assess or didn't observe |
| CNS Toxicity | None observed up to 3.6e12 vg/g | None at therapeutic doses | Convergent: safe in CNS |
| Peripheral Toxicity | Minimal (low peripheral exposure) | Liver transaminase elevations (transient) | Divergent: due to route difference |
| Overexpression Risk | Noted at high doses (430% WT in hippocampus) | Noted at high doses (200% WT) | Convergent: both see supraphysiological levels at high doses |

### Section 6: Dose-Response Relationship
**Strategy**: Normalize to "% WT CDKL5 protein achieved" vs "efficacy improvement"

**Graph concept** (to be implemented):
- X-axis: CDKL5 protein expression (% of WT)
- Y-axis: Efficacy measure (% normalization of phenotype)
- Plot both studies' dose-response data
- Expected outcome: Both should show efficacy threshold around ~50-100% WT levels

### Section 7: Translational Path
| Consideration | PTC | Wilson | Assessment |
|---------------|-----|--------|------------|
| Capsid Translatability | High (AAV9 clinically validated) | Low (PHP.eB mouse-specific) | PTC advantage |
| Delivery Route Translatability | Moderate (ICV/IT requires surgery but feasible) | High if capsid solved (IV non-invasive) | Trade-off |
| Manufacturing | Standard AAV9 | Standard AAV (but need human capsid) | Similar |
| Regulatory Path | Established (similar to other AAV9-CNS therapies) | Need to switch capsid first | PTC more advanced |
| Safety Mitigation | Lower peripheral exposure inherent | miR-183 strategy adds complexity | PTC simpler |

### Section 8: Convergent Findings (Key Takeaways)
**What Both Studies Agree On:**

1. **Therapeutic Window**: Both achieve efficacy at ~50-200% WT CDKL5 levels in brain
2. **Dose-Response**: Clear dose-dependent efficacy in both studies
3. **Timing Matters**: Neonatal dosing more effective than adult (Wilson tested both)
4. **Broad CNS Distribution Needed**: Both achieve widespread brain transduction
5. **Motor/Behavioral Improvements**: Both see functional benefits across multiple domains
6. **Safety at Therapeutic Doses**: CNS well-tolerated at effective dose ranges
7. **Overexpression Risk**: Both note concern at very high doses (>200% WT)

### Section 9: Divergent Findings (Key Differences)
**What Differs:**

1. **Delivery Strategy**: Direct CNS (PTC) vs systemic BBB-crossing (Wilson)
2. **Capsid Choice**: Clinical AAV9 vs mouse-specific PHP.eB
3. **Promoter Strategy**: Cell-type restriction (PTC) vs broad expression + detargeting (Wilson)
4. **Peripheral Exposure**: Lower (PTC) vs higher (Wilson)
5. **Endpoints Assessed**: Morphology emphasis (PTC) vs seizure emphasis (Wilson)
6. **Retinal Safety**: Not observed/assessed (PTC) vs identified and mitigated (Wilson)

## Implementation Plan

### Phase 1: Data Extraction & Normalization
1. Extract all dose-response data from both raw_data files
2. Create conversion functions:
   - vg/kg → vg/g brain (using age-appropriate mouse weights)
   - Normalize efficacy metrics to % improvement
3. Build normalized comparison tables

### Phase 2: Comparison Table Generation
1. Create markdown tables for each section (1-9 above)
2. Format for readability (clear headers, alignment, notes)
3. Add interpretation column for each comparison

### Phase 3: Visualization (Optional)
1. Dose-response curves (if data sufficient)
2. Spider/radar plots for efficacy across multiple endpoints
3. Biodistribution heatmaps (regional expression comparison)

### Phase 4: Summary Report
1. Executive summary (1-2 pages)
2. Detailed comparison tables
3. Conclusions: Are both approaches viable? Which is preferable?

## Output Formats

### Primary Output: Markdown Report
- File: `cdkl5_aav_comparison_report.md`
- Sections as outlined above
- Tables in GitHub-flavored markdown
- Include references to raw data

### Secondary Output: Python Module (Optional)
- File: `comparison_analysis.py`
- Functions to:
  - Normalize doses across studies
  - Extract comparable metrics
  - Generate comparison tables programmatically
  - Calculate convergence metrics

### Tertiary Output: Summary Table (CSV/Excel)
- Quick-reference table
- One row per comparison dimension
- Columns: Dimension, PTC, Wilson, Convergence (Yes/Partial/No), Notes

## Key Questions the Comparison Should Answer

1. **Do both approaches achieve similar brain CDKL5 levels at their effective doses?**
   - Expected: Yes (convergent)

2. **Do both approaches show similar efficacy thresholds?**
   - Expected: Yes (both need ~50-100% WT levels)

3. **Is one approach safer than the other?**
   - Expected: PTC lower peripheral exposure; Wilson identified retinal risk

4. **Which approach is more clinically translatable?**
   - Expected: PTC (AAV9 + ICV) more straightforward; Wilson needs capsid switch

5. **Do efficacy outcomes converge despite different endpoints?**
   - Expected: Yes for overlapping measures (motor, behavior)

6. **What's the optimal dose range for each approach?**
   - PTC: 3e11 - 5e11 vg/g
   - Wilson: 1-2e12 vg/kg (~2-4e10 vg/g estimated)

7. **Are there critical gaps in either study?**
   - PTC: No seizure assessment
   - Wilson: Limited morphology assessment

## Success Criteria

The comparison will be successful if:
1. Clear side-by-side tables are produced for all major dimensions
2. Convergent findings are highlighted (builds confidence)
3. Divergent findings are explained (understand trade-offs)
4. Clinician/researcher can make informed decision about approach viability
5. Gaps in evidence are identified (guide future studies)

## Timeline Estimate

- Data extraction & normalization: ~2-3 hours
- Table generation: ~2-3 hours
- Report writing: ~2-3 hours
- Review & refinement: ~1-2 hours
- Total: ~7-11 hours of work

## Notes

- Some comparisons will be qualitative (different endpoints)
- Dose normalization will involve assumptions (mouse weights, biodistribution efficiency)
- Both studies use male KO mice primarily (sex difference not well explored in either)
- PTC has published manuscript; Wilson has presentation slides (less detail)

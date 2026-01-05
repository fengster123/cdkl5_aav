# CDKL5 AAV Gene Therapy: Side-by-Side Comparison

**PTC Therapeutics (AAV9-ICV) vs University of Pennsylvania/Jim Wilson (AAV-PHP.eB-IV)**

**Date**: 2026-01-05

---

## Executive Summary

Two distinct approaches to AAV gene therapy for CDKL5 deficiency disorder have been developed:

1. **PTC Approach**: AAV9 capsid + Synapsin promoter + ICV (direct CNS) delivery
2. **Wilson Approach**: AAV-PHP.eB capsid + CAG promoter + IV (systemic) delivery

**Key Convergent Findings** (pointing in the same direction):
- Both achieve therapeutic efficacy at 50-200% WT CDKL5 brain levels
- Both show clear dose-response relationships
- Both improve motor and behavioral phenotypes
- Both are safe in CNS at therapeutic doses
- Both identify overexpression risk at very high doses

**Key Divergent Findings** (different trade-offs):
- PTC more clinically translatable (AAV9 validated, but requires surgery)
- Wilson requires capsid change for humans (PHP.eB mouse-specific)
- Wilson identified retinal toxicity; PTC did not report/assess
- Different primary endpoints: PTC emphasizes morphology, Wilson emphasizes seizures

---

## 1. Vector Design & Delivery

| Feature | PTC (AAV9-ICV) | Wilson (PHP.eB-IV) | Interpretation |
|---------|----------------|--------------------|--------------------|
| **Capsid** | AAV9 | AAV-PHP.eB | **Different**: Wilson optimized for IV BBB crossing; PTC uses clinically validated capsid |
| **Capsid Translatability** | ✅ High (used in approved therapies) | ❌ Low (mouse-specific; needs human alternative) | **PTC advantage** for clinical path |
| **Promoter** | Synapsin (neuron-specific) | CAG (ubiquitous) + miR-183 detargeting | **Different strategy**: PTC restricts at transcription; Wilson restricts post-transcriptionally |
| **Delivery Route** | ICV (intracerebroventricular) | IV (intravenous, systemic) | **Different**: PTC invasive but targeted; Wilson non-invasive but broader exposure |
| **Delivery Translatability** | ⚠️ Moderate (requires surgery but established) | ✅ High IF human capsid available | **Trade-off**: Wilson easier IF capsid solved; PTC ready now |
| **Peripheral Exposure** | Lower (CNS-directed) | Higher (systemic IV) | **Wilson requires more peripheral safety monitoring** |
| **Safety Strategy** | Cell-type promoter restriction | Tissue detargeting (miR-183 for retina) | Both viable but different complexity |

**Verdict**: PTC more immediately translatable; Wilson more elegant (IV delivery) but requires capsid development.

---

## 2. Dosing Comparison (Normalized to vg/g Brain)

### Conversion Notes
- PTC doses already in vg/g brain (direct measurement)
- Wilson doses in vg/kg body weight → converted using neonatal mouse parameters:
  - Body weight: ~1.5g, Brain weight: ~0.08g
  - Conversion factor: vg/kg × 0.00187

### Normalized Dose Table

| Study | Dose Level | Administered Dose | **Normalized Brain Dose (vg/g)** | Notes |
|-------|------------|-------------------|---------------------------------|--------|
| **PTC** | Low | 3×10⁹ vg/g (ICV) | **3×10⁹** | Minimal efficacy |
| **Wilson** | Low | 1×10¹¹ vg/kg (IV) | **~1.9×10⁹** | Comparable to PTC low |
| **PTC** | Mid | 3×10¹⁰ vg/g (ICV) | **3×10¹⁰** | Some morphology benefit |
| **Wilson** | Mid | 5×10¹¹ vg/kg (IV) | **~9.4×10⁹** | Below PTC mid |
| **Wilson** | High | 1×10¹² vg/kg (IV) | **~1.9×10¹⁰** | Similar to PTC mid |
| **PTC** | High | 3×10¹¹ vg/g (ICV) | **3×10¹¹** | Robust efficacy |
| **Wilson** | Very High | 2×10¹² vg/kg (IV) | **~3.8×10¹⁰** | Below PTC high |
| **PTC** | Very High | 5×10¹¹ vg/g (ICV) | **5×10¹¹** | Maximum efficacy |
| **Wilson** | Ultra High | 3×10¹² vg/kg (IV) | **~5.6×10¹⁰** | Below PTC very high; retinal toxicity risk |

### Key Insight
**Wilson achieves efficacy at ~10-fold lower normalized brain doses than PTC.** This suggests:
1. IV delivery with PHP.eB may be more efficient (better biodistribution)
2. Different measurement methodologies (actual tissue levels vs administered dose)
3. ICV delivery may have local/regional gradients vs IV uniform distribution

### Actual Brain Tissue Levels Achieved (% WT CDKL5 Protein)

This is the **most important comparison** - what actually gets into the brain:

| Dose (Normalized) | PTC Hippocampus | Wilson Hippocampus | Convergence? |
|-------------------|-----------------|--------------------|--------------|
| ~2×10⁹ - 3×10⁹ | 1.8% WT | Not tested | N/A |
| ~1-2×10¹⁰ | 3.9% WT | 50-100% WT | **Divergent** - Wilson much higher at similar dose |
| ~3-4×10¹⁰ | 33% WT (study 2) to 123% WT (study 3) | 100-200% WT | **Convergent** - both reach therapeutic range |
| ~5×10¹¹ | 347% WT | Not tested | N/A |

**Critical Finding**: Both achieve **50-200% WT levels** at their therapeutic doses, but:
- PTC requires higher administered doses (3-5×10¹¹ vg/g)
- Wilson achieves similar tissue levels at lower administered doses (1-2×10¹² vg/kg ≈ 2-4×10¹⁰ vg/g)
- **Convergence**: Efficacy threshold is ~50-100% WT CDKL5 in both studies

---

## 3. Biodistribution & Expression Patterns

| Measure | PTC | Wilson | Convergence? |
|---------|-----|--------|--------------|
| **Cell Type Specificity** | Neurons only (Syn promoter; no GFAP+) | CAG: Neurons + glia; hSyn: neurons only | **Convergent**: Both achieve neuronal expression; differ in glia |
| **Brain Distribution** | Broad ICV coverage; regional variation | Broad IV coverage; relatively uniform with PHP.eB | **Convergent**: Both achieve wide CNS coverage |
| **% Neurons Transduced** | Up to ~75% NeuN+ at high dose (3.6×10¹² vg/g) | Not quantified by % NeuN+ | Partial data |
| **Regional CDKL5 Levels (Hippocampus)** | 33-347% WT (dose 3-5×10¹¹ vg/g) | 50-200% WT (dose 1-2×10¹² vg/kg) | **Convergent**: Both reach/exceed WT levels |
| **Regional CDKL5 Levels (Cortex)** | 30-136% WT | 50-200% WT | **Convergent** |
| **Regional CDKL5 Levels (Cerebellum)** | 10-33% WT (lower) | Moderate-high transduction | **Convergent**: Cerebellum harder to transduce |
| **Peripheral Exposure** | Lower (ICV route; but liver still exposed) | Higher (IV route; liver, spleen, heart, kidney) | **Divergent**: Route-dependent difference |

**Verdict**: Both achieve broad brain transduction with neuron-targeting. Wilson's IV approach gives more uniform distribution; PTC's ICV has some regional gradients.

---

## 4. Efficacy Comparison

### 4A. Motor Function

| Test | PTC Results | Wilson Results | Convergence |
|------|-------------|----------------|-------------|
| **Hindlimb Clasping** | ✅ Complete normalization at 3×10¹¹ vg/g (p<0.001) | Not tested | N/A |
| **Rotarod** | Not tested | ✅ Partial rescue at 1×10¹² vg/kg; near-normalization at 2×10¹² vg/kg | N/A |
| **Open Field Hyperactivity (Distance)** | ⚠️ 43% improvement at 5×10¹¹ vg/g (p=0.39, n.s.) | ✅ Partial normalization at therapeutic doses | **Convergent**: Both improve hyperactivity |
| **Open Field (Mobility State)** | ✅ 46% reduction in highly-mobile time at 5×10¹¹ vg/g (p<0.01) | Not separately quantified | Supports convergence |

**Verdict**: ✅ **Convergent** - Both studies show motor improvements at therapeutic doses. PTC complete rescue on HLC; Wilson strong on rotarod. Hyperactivity improved in both.

---

### 4B. Cognitive/Learning Function

| Test | PTC Results | Wilson Results | Convergence |
|------|-------------|----------------|-------------|
| **Fear Conditioning** | • 0% at 3×10⁹-3×10¹⁰<br>• 44-62% at 3×10¹¹<br>• ✅ 100% at 5×10¹¹ (p<0.01) | ⚠️ Some improvement but incomplete rescue | **Partial Convergent**: PTC full rescue at high dose; Wilson partial |
| **Novel Object Recognition** | Not tested | ⚠️ Partial rescue | N/A |
| **Barnes Maze** | Not tested | Tested | N/A |

**Verdict**: ⚠️ **Partially Convergent** - Both show cognitive benefits, but PTC achieved complete normalization at highest dose while Wilson saw incomplete rescue. May reflect dose differences or timing.

---

### 4C. Seizure Control ⚡

| Measure | PTC Results | Wilson Results | Convergence |
|---------|-------------|----------------|-------------|
| **Seizure Frequency (Video-EEG)** | ❌ **NOT MEASURED** | ✅ 30-50% reduction at 1×10¹² vg/kg<br>✅ 60-80% reduction at 2×10¹² vg/kg<br>✅ 70-90% reduction at 3×10¹² vg/kg | **❌ CRITICAL GAP in PTC study** |

**Verdict**: ❌ **Cannot compare** - PTC did not assess seizures, the primary clinical feature of CDKL5 deficiency. This is a **major limitation** of the PTC study.

**Wilson's seizure data is critical**: Shows robust dose-dependent seizure suppression, with near-normalization at 2×10¹² vg/kg (neonatal dosing).

---

### 4D. Neuronal Morphology

| Measure | PTC Results | Wilson Results | Convergence |
|---------|-------------|----------------|-------------|
| **Dendritic Length** | ✅ Near-normalization at 3×10¹¹ vg/g | Not extensively tested | N/A |
| **Spine Density** | ✅ Improved at 3×10¹⁰-3×10¹¹ vg/g | Not extensively tested | N/A |
| **Sholl Analysis (Branching)** | ✅ Improved at 3×10¹¹ vg/g | Not tested | N/A |

**Verdict**: PTC emphasized morphology and showed strong rescue. Wilson did not focus on this endpoint. Morphology improvements suggest structural restoration of neurons.

---

## 5. Safety Profile

| Safety Parameter | PTC | Wilson | Convergence |
|------------------|-----|--------|-------------|
| **Retinal Toxicity** | ❓ Not reported (either not assessed or not observed) | ⚠️ **YES** - dose-dependent at ≥2×10¹² vg/kg with CAG promoter<br>✅ Mitigated with miR-183 (70-90% reduction in retinal expression) | **❌ Divergent** - Wilson identified and solved; PTC silent |
| **CNS Toxicity** | ✅ None up to 3.6×10¹² vg/g | ✅ None at therapeutic doses | **✅ Convergent** - both safe in CNS |
| **Peripheral Toxicity** | ✅ Minimal (low exposure from ICV) | ⚠️ Liver transaminase elevations at high doses (transient) | **Divergent** - route-dependent |
| **Overexpression Risk** | ⚠️ Up to 430% WT in hippocampus at 5×10¹¹ vg/g<br>Authors note "unclear risk" | ⚠️ Up to 200% WT at 2×10¹² vg/kg<br>Authors note "potential concerns" | **✅ Convergent** - both see supraphysiological levels; both flag concern |
| **Highest Safe Dose Tested** | 3.6×10¹² vg/g (no overt CNS toxicity) | 2×10¹² vg/kg (retinal toxicity without miR-183) | Both have safety margins above therapeutic doses |

**Key Safety Insights**:
1. **Retinal toxicity**: Wilson's major finding. miR-183 strategy is innovative and effective. PTC either didn't look or didn't see it (route difference?)
2. **Both safe in CNS** at therapeutic ranges
3. **Overexpression concern** in both studies at highest doses - suggests upper limit exists
4. **Peripheral safety**: ICV (PTC) advantage for limiting peripheral exposure

---

## 6. Dose-Response Summary

### PTC Dose-Response

| Dose (vg/g) | CDKL5 Protein (% WT) | Efficacy | Safety |
|-------------|----------------------|----------|--------|
| 3×10⁹ | ~2% | ❌ No benefit | ✅ Safe |
| 3×10¹⁰ | ~4% | ⚠️ Some morphology improvement | ✅ Safe |
| 3×10¹¹ | 33-123% (study variability) | ✅ Motor + cognitive improvements | ✅ Safe |
| 5×10¹¹ | 347% | ✅ Maximum efficacy (complete rescue) | ⚠️ High overexpression |

**PTC Optimal Range**: 3-5×10¹¹ vg/g brain

---

### Wilson Dose-Response (Neonatal)

| Dose (vg/kg) | CDKL5 Protein (% WT) | Efficacy | Safety |
|--------------|----------------------|----------|--------|
| 1×10¹¹ | Not measured | ❌ Minimal | ✅ Safe |
| 1×10¹² | 50-100% | ✅ Moderate (30-50% seizure reduction; motor improvement) | ✅ Safe |
| 2×10¹² | 100-200% | ✅ Robust (60-80% seizure reduction; near-normalization) | ⚠️ Retinal toxicity (solved with miR-183) |
| 3×10¹² | >200% (estimated) | ✅ Maximum (70-90% seizure reduction) | ❌ Retinal toxicity + overexpression concern |

**Wilson Optimal Range**: 1-2×10¹² vg/kg (neonatal)

---

### Convergent Dose-Response Principle

**Both studies show efficacy threshold at ~50-100% WT CDKL5 levels in brain.**

Despite 10-fold difference in administered doses (due to route/efficiency), both converge on achieving:
- 50-100% WT: Moderate efficacy
- 100-200% WT: Robust efficacy
- >200% WT: Maximum efficacy but safety concerns

This is a **critical convergent finding** - suggests the therapeutic window is defined by brain tissue levels, not administered dose.

---

## 7. Translational Path to Clinic

| Consideration | PTC (AAV9-ICV) | Wilson (PHP.eB-IV) | Assessment |
|---------------|----------------|--------------------|------------|
| **Capsid Translatability** | ✅ AAV9 clinically validated (Zolgensma, others) | ❌ PHP.eB mouse-specific; must use AAV9, AAVhu68, or novel human capsid | **PTC clear advantage** |
| **Delivery Translatability** | ⚠️ ICV/IT surgery required but feasible (precedent in SMA, other CNS trials) | ✅ IV non-invasive IF human capsid works | **Trade-off**: PTC ready now; Wilson better IF capsid solved |
| **Manufacturing** | ✅ Standard AAV9 (established) | ⚠️ Need to develop/manufacture new capsid | PTC advantage |
| **Regulatory Path** | ✅ Clear precedent (similar to other AAV9-CNS gene therapies) | ⚠️ Less established for systemic AAV-CNS (need to solve capsid first) | PTC more advanced |
| **NHP Safety Data** | ✅ Yes - cynomolgus macaques, biodistribution + tolerability | ❓ Not mentioned in presentation | PTC has more tox data |
| **Safety Mitigation** | ✅ Lower peripheral exposure inherent to ICV | ⚠️ miR-183 strategy adds construct complexity | PTC simpler |
| **Clinical Endpoints** | ⚠️ No seizure data (would need to rely on behavioral/developmental endpoints) | ✅ Seizure data strong (primary clinical endpoint) | Wilson more clinically relevant |

**Translational Verdict**:
- **PTC is ~2-3 years closer to clinic** (capsid/delivery/manufacturing ready)
- **Wilson has better preclinical efficacy data** (seizures) but needs capsid development
- **Ideal scenario**: Combine PTC's translatable platform (AAV9-ICV) with Wilson's rigorous seizure endpoints

---

## 8. Convergent Findings (High Confidence)

These findings point in the **same direction** across both studies:

1. ✅ **Therapeutic efficacy achieved at 50-200% WT CDKL5 brain levels**
   - Both studies converge on this tissue level threshold despite different administered doses

2. ✅ **Clear dose-response relationship**
   - Both show dose-dependent improvements in efficacy

3. ✅ **Neonatal dosing is effective**
   - Both dosed at P0; Wilson also showed adult dosing less effective

4. ✅ **Broad CNS distribution required for efficacy**
   - Both achieved widespread brain transduction

5. ✅ **Motor function improvements**
   - PTC: Hindlimb clasping, open field
   - Wilson: Rotarod, open field
   - Both show convergent motor rescue

6. ✅ **Cognitive/learning improvements possible**
   - Both showed benefits in learning/memory tasks (fear conditioning, etc.)

7. ✅ **CNS safe at therapeutic doses**
   - Neither saw overt toxicity, inflammation, or pathology in brain at effective doses

8. ✅ **Overexpression risk at very high doses (>200% WT)**
   - Both flagged concern about supraphysiological levels
   - Suggests upper safety limit exists

9. ✅ **Neuron-targeting strategies work**
   - PTC: transcriptional (Synapsin promoter)
   - Wilson: primarily neuronal with CAG (hSyn also tested)
   - Both achieve neuronal expression

---

## 9. Divergent Findings (Different Trade-offs)

These findings differ but represent valid **alternative approaches**:

1. **Delivery Route**: ICV (PTC) vs IV (Wilson)
   - PTC: Invasive surgery but targeted, lower peripheral exposure
   - Wilson: Non-invasive but higher peripheral exposure, requires special capsid
   - **Trade-off, not contradiction**

2. **Capsid Choice**: AAV9 (PTC) vs PHP.eB (Wilson)
   - PTC: Clinically validated, ready to translate
   - Wilson: Mouse-specific proof-of-concept, need human alternative
   - **PTC advantage for near-term clinical translation**

3. **Promoter Strategy**: Cell-type restriction (PTC) vs broad + detargeting (Wilson)
   - PTC: Synapsin limits to neurons at transcription level
   - Wilson: CAG ubiquitous + miR-183 detargets retina post-transcriptionally
   - **Both valid strategies; different complexity**

4. **Peripheral Exposure**: Lower (PTC) vs Higher (Wilson)
   - Route-dependent; ICV inherently lower peripheral exposure
   - **PTC advantage for peripheral safety**

5. **Retinal Toxicity**: Not observed/reported (PTC) vs identified + mitigated (Wilson)
   - Wilson found dose-dependent retinal degeneration with CAG
   - PTC silent (either didn't assess, didn't observe, or dose/route difference)
   - **Wilson identified risk; unclear if PTC approach avoids it or just didn't look**

6. **Primary Endpoints**: Morphology/behavior (PTC) vs Seizures (Wilson)
   - PTC emphasized structural rescue (dendrites, spines)
   - Wilson emphasized clinical endpoint (seizure suppression)
   - **Wilson more clinically relevant; PTC more mechanistic**

7. **Translational Readiness**: Higher (PTC) vs Lower (Wilson)
   - PTC ready for IND with AAV9-ICV
   - Wilson needs capsid switch before clinical trial
   - **PTC ~2-3 years ahead**

---

## 10. Critical Gaps

### Gaps in PTC Study
1. ❌ **No seizure assessment (video-EEG)** - This is the primary clinical feature of CDD
2. ❓ **No retinal safety assessment reported** - Did they look? Is ICV route protective?
3. ⚠️ **Study-to-study variability** - Same dose (3×10¹¹ vg/g) showed 33% vs 123% WT protein
4. ⚠️ **Limited female data** - Mostly male mice

### Gaps in Wilson Study
1. ⚠️ **Less precise quantification** - Presentation format (slides) vs peer-reviewed manuscript
2. ⚠️ **Limited morphology assessment** - Didn't extensively characterize dendritic/spine rescue
3. ⚠️ **No human-compatible capsid tested** - PHP.eB proof-of-concept only
4. ❓ **No published NHP data mentioned** - May exist but not in presentation

### Gaps in Both Studies
1. ⚠️ **Limited adult dosing data** - Both primarily focused on neonatal intervention
2. ⚠️ **Primarily male mice** - Female heterozygotes more clinically relevant (X-linked)
3. ❓ **Long-term durability unknown** - Longest timepoints ~17-19 weeks; need lifetime studies
4. ❓ **Immune responses not fully characterized** - Anti-AAV, anti-CDKL5 antibodies?

---

## 11. Final Assessment: Which Approach is Better?

### Short Answer: **Both are viable; PTC is closer to clinic**

### Detailed Assessment:

| Criterion | Winner | Rationale |
|-----------|--------|-----------|
| **Clinical Translatability** | 🏆 **PTC** | AAV9-ICV ready now; Wilson needs capsid development |
| **Preclinical Efficacy Data** | 🏆 **Wilson** | Seizure data (primary clinical endpoint); more rigorous |
| **Safety Profile** | 🤝 **Tie** | Both safe in CNS; Wilson identified retinal risk and solved it; PTC lower peripheral exposure |
| **Delivery Convenience** | 🏆 **Wilson** (IF capsid solved) | IV non-invasive; but currently not translatable |
| **Manufacturing Readiness** | 🏆 **PTC** | AAV9 established; Wilson needs new capsid manufacturing |
| **Mechanistic Understanding** | 🏆 **PTC** | Strong morphology data; structural rescue demonstrated |
| **Dose Efficiency** | 🏆 **Wilson** | Achieves similar tissue levels at ~10× lower administered dose |

---

### Recommendations:

**For near-term clinical development (next 2-5 years)**:
- ✅ **PTC approach** is more ready (AAV9-ICV)
- ⚠️ But **add seizure monitoring** as primary endpoint
- ⚠️ And **assess retinal safety** proactively

**For optimal long-term solution (5-10 years)**:
- ✅ **Wilson IV approach** if human-tropic capsid developed (AAV9-IV, AAVhu68-IV, or novel)
- ✅ **Incorporate miR-183 strategy** for retinal safety
- ✅ Use **Wilson's seizure endpoint rigor** with **PTC's morphology assessments**

**Ideal next study**:
- **AAV9-IV** (human-compatible capsid)
- **CAG or Synapsin promoter** with **miR-183 sites**
- **Assess both seizures (Wilson) AND morphology (PTC)**
- **Test in both males and female heterozygotes**
- **Long-term durability and safety (12+ months)**

---

## 12. Key Takeaways for Clinicians/Researchers

1. **Both approaches work** - Achieve CDKL5 expression and functional improvements in mouse models

2. **Efficacy threshold**: ~50-100% WT CDKL5 in brain tissue required for benefit

3. **Safety**: Both safe in CNS at therapeutic doses; retinal toxicity a concern at high doses (Wilson); can be mitigated

4. **Clinical translation**: PTC closer (AAV9-ICV ready); Wilson needs capsid development but may be superior long-term (IV delivery)

5. **Critical gaps**:
   - PTC needs to assess seizures
   - Wilson needs human-compatible capsid
   - Both need long-term durability/safety data

6. **Convergent biology**: Despite different methods, both point to same therapeutic window (50-200% WT CDKL5) and demonstrate dose-dependent efficacy

7. **Complementary strengths**: PTC strong on morphology; Wilson strong on seizures. Ideal trial would combine both.

---

## Data Sources

- **PTC**: Voronin et al., Molecular Therapy 2024; doi: 10.1016/j.ymthe.2024.07.012
- **Wilson**: University of Pennsylvania presentation (Jim Wilson lab); IFCR collaboration

---

## Appendix: Dose Conversion Reference

For neonatal P0 mice:
- Body weight: ~1.5g
- Brain weight: ~0.08g
- Conversion: **1×10¹² vg/kg ≈ 1.9×10¹⁰ vg/g brain**

### Quick Reference Table

| Wilson (vg/kg) | ≈ PTC (vg/g brain) |
|----------------|--------------------|
| 1×10¹¹ | 1.9×10⁹ |
| 5×10¹¹ | 9.4×10⁹ |
| 1×10¹² | 1.9×10¹⁰ |
| 2×10¹² | 3.8×10¹⁰ |
| 3×10¹² | 5.6×10¹⁰ |

| PTC (vg/g brain) | ≈ Wilson (vg/kg) |
|------------------|------------------|
| 3×10⁹ | 1.6×10¹¹ |
| 3×10¹⁰ | 1.6×10¹² |
| 3×10¹¹ | 1.6×10¹³ |
| 5×10¹¹ | 2.7×10¹³ |

---

**End of Report**

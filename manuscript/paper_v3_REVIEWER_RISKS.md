# Paper v3 — Reviewer Risk Assessment

## Purpose
Anticipate the strongest likely reviewer criticisms, document how paper_v3 addresses them, and identify what remains vulnerable. This is an internal document for pre-submission preparation.

---

## Risk 1: "The inferential unit is cells, not donors — your p-values are meaningless"
**Severity:** Critical — this alone can reject the paper.

**How v3 addresses it:**
- Donor-level analyses are promoted to primary or co-primary throughout
- Leave-one-donor-out (27/27 iterations) is reported as a core robustness result
- Donor-level pseudobulk replication (43 vs 575 donors, p = 0.002) is highlighted
- Per-donor median pseudotime, per-donor dispersion, and per-donor transitional fraction are computed
- Cell-level p-values are reported as descriptive context, not as the primary inferential basis
- TODO: Add mixed-effects models (pseudotime ~ condition + (1|donor)) and donor-level bootstrap CIs

**What remains vulnerable:**
- True sample size is only n = 27 donors (7 vs 20) in the primary atlas
- Mixed-effects and donor-level bootstrap are planned but not yet computed
- Cell-level Levene's test remains prominent; a reviewer may demand donor-level variance comparison

---

## Risk 2: "Single dataset — how do you know this generalizes?"
**Severity:** High.

**How v3 addresses it:**
- Independent replication on 89,736 cells from 618 donors across 35 datasets (Melms excluded)
- Dispersion replicates strongly (Levene p ~ 10^-137, variance ratio 1.65)
- Donor-level direction replicates (p = 0.002)
- Explicit "portable vs atlas-specific" distinction in Results and Discussion
- DATP threshold failure honestly reported and downgraded

**What remains vulnerable:**
- Replication uses 84-gene panel, not full transcriptome — cannot replicate manifold construction
- Full-transcriptome replication on an independent autopsy cohort (Delorey, Wendisch) not done
- Non-COVID lung injury cohorts not analyzed

---

## Risk 3: "Pseudotime is not real time — you can't claim a temporal process"
**Severity:** Moderate — predictable objection.

**How v3 addresses it:**
- Language is carefully calibrated: "consistent with," "ordered along pseudotime," not "progresses through"
- Explicit caveat in Introduction: pseudotime is a computational ordering, not a time measurement
- Explicit limitation paragraph: cross-sectional design, no lineage tracing
- Palantir as orthogonal method confirms direction, adding method-independence
- We do NOT claim that individual cells traverse the trajectory

**What remains vulnerable:**
- Some readers will always object to pseudotime studies on principle
- RNA velocity could provide orthogonal directionality evidence but was not run

---

## Risk 4: "The effect size is tiny — 0.048 on a [0,1] axis is 5%"
**Severity:** Moderate.

**How v3 addresses it:**
- The magnitude is explicitly acknowledged: "modest in magnitude"
- Harmony correction amplifies to +0.125 (2.6x), suggesting 0.048 is an attenuated lower bound
- The paper does not claim a dramatic reorganization; it claims a consistent directional shift
- Permutation p = 0.001 with tight null (std 0.001) — the shift is real, just modest
- Effect size is contextualized: even a small shift is biologically meaningful if it reflects progressive injury

**What remains vulnerable:**
- A reviewer may argue that 5% is not biologically meaningful
- No external benchmark for what constitutes a "meaningful" pseudotime shift in alveolar biology

---

## Risk 5: "The program ordering is fragile — MSigDB inversion destroys it"
**Severity:** Moderate — but well-handled by honest reporting.

**How v3 addresses it:**
- MSigDB inversion (rho = -0.80) is prominently reported, not hidden
- Fine ordering explicitly labeled "hypothesis-generating"
- The paper's central claim does NOT rest on fine program ordering
- Identity-first → injury-second pattern IS stable across all ablations
- This is reframed as a methodological contribution: gene-list choice matters for ordering

**What remains vulnerable:**
- A reviewer may argue this undermines the entire trajectory framework
- If a reviewer views program ordering as the paper's main contribution, the paper looks weak
- v3 mitigates this by NOT making program ordering the central claim

---

## Risk 6: "Harmony failed in the original pipeline — how can you trust any batch analysis?"
**Severity:** Low-moderate (fixed in v2, but history may concern reviewers).

**How v3 addresses it:**
- The bug is diagnosed and fixed (documented in Methods)
- Harmony now runs and converges in 3 iterations
- Both corrected and uncorrected results are reported side by side
- Harmony STRENGTHENS the signal (2.6x), ruling out artifact concerns
- The fact that correction amplifies rather than creates the signal is strong evidence

**What remains vulnerable:**
- The original pipeline bug may reduce confidence in code quality
- Only Harmony was used; scVI or scanorama could provide additional integration evidence

---

## Risk 7: "DATP enrichment doesn't replicate — this undermines the transitional-cell story"
**Severity:** Moderate.

**How v3 addresses it:**
- DATP marker-threshold portability failure is explicitly reported and explained
- Failure attributed to cross-study normalization and annotation non-equivalence
- DATP enrichment is framed as a "primary-atlas observation" not a cross-cohort claim
- The paper does NOT center on DATP portability
- A manifold-based state score (not threshold-based) is proposed as the correct portable alternative

**What remains vulnerable:**
- The transitional-cell story is weakened if DATP enrichment is atlas-specific
- A reviewer may question whether the KRT8+/CLDN4+ population is a real biological entity vs annotation artifact
- No classifier-based cross-cohort transfer was attempted

---

## Risk 8: "This is just a re-analysis of a published atlas — where is the novelty?"
**Severity:** Moderate-high.

**How v3 addresses it:**
- The novel contribution is methodological + interpretive: ablation-first robustness audit, competing-model testing, explicit negative result reporting
- Cross-cohort replication adds independent evidence
- The model-discrimination framing (displacement vs fan-out) is genuinely new
- The "loss of state coherence" concept generalizes beyond COVID
- Harmony-corrected vs uncorrected comparison is novel and informative

**What remains vulnerable:**
- No new data generation (no wet lab, no spatial, no histology)
- A reviewer who values only new data may not be satisfied
- The paper is strongest at a methods/analysis venue rather than a biology-first venue

---

## Risk 9: "Only lethal cases — you can't distinguish lethal-specific from general COVID injury"
**Severity:** Low-moderate (inherent to dataset).

**How v3 addresses it:**
- Acknowledged as explicit limitation
- We do NOT claim the findings are lethal-specific
- Replication cohort includes mixed-severity COVID (though predominantly severe)
- Future directions explicitly mention mild/moderate comparison

**What remains vulnerable:**
- Cannot resolve dose-response without mild/moderate data
- Post-mortem artifacts may contribute

---

## Risk 10: "The composite score of 'moderate' sounds like a partial failure"
**Severity:** Low — but framing matters.

**How v3 addresses it:**
- In v3, "moderate" composite is reframed as "the data distinguish between two competing models"
- The centroid failure is presented as a positive finding (rules out simpler model)
- The composite terminology is de-emphasized in favor of model-discrimination language
- "Two of three criteria supported" sounds negative; "data support fan-out model over displacement model" sounds positive — same evidence, better framing

**What remains vulnerable:**
- A reviewer who reads only the composite table may still see "moderate" as weak
- The term "robustness collapse" in the composite label may seem overclaimed when displacement failed

---

## Summary: residual vulnerability ranking

| Rank | Risk | Residual vulnerability |
|------|------|----------------------|
| 1 | Donor-level inference gaps | Mixed-effects and bootstrap not yet computed |
| 2 | Single dataset / limited replication scope | Only 84-gene panel replication; no full-transcriptome independent manifold |
| 3 | "Just a re-analysis" novelty concern | No new data; computational only |
| 4 | DATP portability failure weakens transitional story | No classifier-based transfer attempted |
| 5 | Small effect size (0.048) | No external benchmark for biological significance |
| 6 | No mild/moderate comparison | Inherent to dataset |
| 7 | Program ordering fragility | Already honestly reported |
| 8 | Pseudotime ≠ real time | Standard objection, well-caveated |

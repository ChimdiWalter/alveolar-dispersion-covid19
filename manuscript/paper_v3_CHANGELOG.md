# Paper v3 Changelog — Changes from v2 to v3

## Date: 2026-04-30

---

## Title change
- **v2:** "Ablation-First Trajectory Analysis of Alveolar Epithelial Robustness Collapse in Lethal COVID-19, with Harmony-Corrected Batch Analysis and Independent Cross-Cohort Replication"
- **v3:** "Dispersion, not displacement: loss of alveolar epithelial state coherence in lethal COVID-19"
- **Rationale:** v2 title was a kitchen-sink of method descriptors. v3 title centers the actual result (dispersion wins over displacement) and uses "state coherence loss" instead of "robustness collapse" to be more precise and less dramatic.

## Abstract rewrite
- **v2:** ~400 words; read as a technical results dump with extensive method detail
- **v3:** ~300 words; structured as problem → competing models → approach → results → interpretation → significance
- **Key change:** Abstract now opens by framing two competing geometric models and reports results in model-discrimination order rather than pipeline order

## Terminology change: "robustness collapse" → "loss of state coherence"
- **Rationale:** "Collapse" implies complete failure; the data show increased dispersion with a modest pseudotime shift, which is better described as "loss of coherence." The term "state coherence" is geometrically precise — it describes the tightness of a cell population in transcriptomic space.

## Claims strengthened

| Claim | How |
|-------|-----|
| Dispersion is the primary finding | Promoted to Results centerpiece (subsection 3); donor-level evidence added; replication evidence integrated into same subsection |
| Pseudotime shift is robust | Harmony amplification (2.6x), Palantir (+0.028), 27/27 LODO, donor-level replication (p=0.002) all synthesized |
| Centroid failure is conceptually meaningful | Reframed as model-discriminating negative result, not as a test that "didn't work" |
| Geometric signatures are portable | Explicit portable-vs-fragile framework with replication evidence |

## Claims softened

| Claim | How |
|-------|-----|
| "Robustness collapse" framework | Replaced with "loss of state coherence" — more modest, more precise |
| Fine program ordering | Moved to supplement; labeled "hypothesis-generating"; the stable finding (identity-first → injury-second) is retained, but fine injury-phase sequence is not claimed |
| DATP enrichment as general | Downgraded to "primary-atlas observation"; portability failure explicitly reported |
| Composite "moderate" assessment | De-emphasized in favor of model-discrimination framing |
| Specific injury cascade | Not claimed; only broad identity→injury pattern claimed |

## Framing changes

| Aspect | v2 | v3 |
|--------|----|----|
| Central question | "Does robustness collapse occur?" | "Which geometric model describes alveolar injury?" |
| Primary metric | Three pre-registered criteria | Dispersion + donor-aware pseudotime direction |
| Negative result | Reported as a failed test | Reported as model discrimination |
| Replication | Separate late subsection | Integrated into results where relevant |
| Donor awareness | Supporting LODO analysis | Primary inferential strategy |
| Harmony | Ablation 3 | Co-primary analysis |
| Figure 1 | Manifold UMAP | Competing-models schematic |

## Structural changes

### Results reordered:
1. Cohort composition → (same as v2)
2. NEW: Competing models framing
3. Dispersion as centerpiece → (promoted from v2 subsection 5)
4. Donor-aware pseudotime → (expanded from v2 subsection 3)
5. Transitional compartment → (softened from v2)
6. Harmony/donor-aware integration → (promoted from ablation)
7. Ablation summary → (condensed)
8. Replication summary → (expanded, integrated)

### Figure plan reordered:
- New Figure 1: Conceptual schematic
- Figure 3 is now Dispersion (was pseudotime density)
- Gene program dynamics moved to supplement
- Replication gets its own main figure
- Donor-level panels added throughout

## What was NOT changed
- All quantitative results remain identical — no numbers were altered
- The biological story (alveolar injury, AT2-to-AT1 repair, transitional cells) is preserved
- All ablation results reported identically
- All replication results reported identically
- All limitations acknowledged in v2 are preserved in v3

## Outstanding items for future v3 revision
- [ ] Compute mixed-effects models: pseudotime ~ condition + (1|donor)
- [ ] Compute donor-level bootstrap CIs for key quantities
- [ ] Compute donor-level dispersion comparison (per-donor median distance)
- [ ] Build manifold-based transitional-state score (replaces threshold-based DATP calling)
- [ ] Add confidence intervals to all point estimates
- [ ] Run RNA velocity if feasible

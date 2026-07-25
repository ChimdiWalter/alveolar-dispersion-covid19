# Paper v3 — Results Rewrite Notes

## What changed from v2 to v3 in the Results

### Structural changes

| Change | Rationale |
|--------|-----------|
| **Results reordered** | v2 led with manifold/pseudotime, then centroid failure, then dispersion. v3 leads with cohort validation, then competing-model framing, then dispersion (strongest finding first), then donor-aware pseudotime. |
| **Competing-model framing added as explicit subsection** | v2 tested centroid displacement as one of three criteria. v3 explicitly frames the paper as testing two geometric models and shows the data discriminate between them. |
| **Dispersion promoted to centerpiece** | In v2, dispersion was one subsection among many. In v3, it is the central result with donor-level and replication panels. |
| **Gene program dynamics moved to secondary** | In v2, program ordering was a main result. In v3, fine ordering is explicitly "hypothesis-generating" and the program figure moves to supplement. The stable finding (identity-first → injury-second) is retained as a main text result. |
| **Donor-level analyses added throughout** | v2 reported donor-level consistency as a supporting figure. v3 adds donor-level panels to dispersion, pseudotime, and transitional-state figures. |
| **Harmony corrected results promoted** | v2 reported Harmony as an ablation. v3 reports Harmony side-by-side as co-primary evidence, with uncorrected serving as conservative lower bound. |
| **Replication given its own section** | v2 had replication as a subsection. v3 has a full results subsection with dispersion, donor-level direction, per-program, and DATP portability failure all reported. |
| **Portable vs atlas-specific distinction made explicit** | v2 mentioned portability. v3 has a portability matrix figure and explicit language distinguishing geometric (portable) from annotation-dependent (fragile) findings. |

### Claims strengthened

| Claim | How strengthened |
|-------|-----------------|
| Dispersion as the primary finding | Promoted to centerpiece; donor-level and replication evidence foregrounded |
| Pseudotime shift as robust | Harmony amplification (2.6x), Palantir confirmation (+0.028), 27/27 LODO, donor-level replication (p=0.002) |
| Centroid failure as conceptually meaningful | Reframed from "a test that failed" to "evidence discriminating between two competing models" |
| Cross-cohort portability of geometric signatures | Explicit "portable" label with replication evidence |

### Claims softened

| Claim | How softened |
|-------|-------------|
| "Robustness collapse" as a framework | Changed to "loss of epithelial state coherence" — more precise, less dramatic |
| Fine program ordering | Explicitly labeled "hypothesis-generating"; moved from main to supplement |
| DATP enrichment as a general finding | Downgraded to "primary-atlas observation"; portability failure prominently reported |
| Composite "moderate" assessment | De-emphasized; replaced with model-discrimination language |
| Specific injury-program cascade | Acknowledged as sensitive to gene-list choice; only the broad pattern (identity-first) is claimed |

### Why the new ordering is better for reviewers

1. **Strongest evidence first**: A reviewer reading the first two results subsections already knows the main finding and its replication status.

2. **Negative results positioned as model discrimination, not failure**: The centroid displacement failure is not buried — it is the conceptual contrast that makes the dispersion finding meaningful.

3. **Donor awareness throughout**: A statistical reviewer can immediately see that the paper treats donors, not cells, as the primary unit.

4. **Fragile findings clearly labeled**: A reviewer looking for overclaiming will find instead a paper that labels its own fragilities. This builds trust rather than inviting attack.

5. **Replication is structurally integrated**: Instead of reading the entire Results section before learning whether anything replicates, the reviewer encounters replication evidence within the dispersion and pseudotime subsections themselves.

---

## Subsection-by-subsection notes

### 1. Cohort composition and alveolar subset validation
- Mostly unchanged from v2
- Added: explicit statement of donor n as the inferential sample size
- Added: note on uneven per-donor cell counts and mitigation strategy

### 2. Competing models: coherent displacement versus fan-out
- NEW section in v3
- Frames the paper as explicitly testing two geometric models
- Reports centroid displacement failure as the first quantitative result
- Immediately sets up dispersion as the alternative
- This subsection makes the paper's logic clear in one read

### 3. Dispersion-dominated loss of state coherence
- Expanded from v2 dispersion subsection
- Added: donor-level dispersion comparison
- Added: replication dispersion in same subsection (not deferred)
- This is now the paper's centerpiece

### 4. Donor-aware pseudotime shift
- Rewritten to emphasize donor-level robustness
- Harmony amplification reported as evidence against batch artifact, not as a separate ablation
- Palantir confirmation noted
- LODO range reported
- Replication at donor-pseudobulk level reported

### 5. Transitional compartment enrichment
- Rewritten to be more cautious
- DATP enrichment is an atlas-specific observation
- Cross-cohort portability failure reported in same subsection
- Language: "consistent with stalled repair" not "demonstrates stalled repair"

### 6. Harmony/donor-aware integration
- Slightly expanded from v2 Ablation 3
- Framed as evidence that batch correction STRENGTHENS the signal
- Justification for promoting Harmony to co-primary

### 7. Ablation robustness
- Restructured as a summary rather than 10 individual paragraphs
- Key ablations highlighted: LODO (robust), MSigDB (fragile), broader epithelial (shift collapses)
- Ablation matrix figure referenced

### 8. Replication summary
- Expanded from v2
- Portable findings vs atlas-specific findings distinction made explicit
- Per-program replication reported honestly
- DATP transfer failure given full treatment

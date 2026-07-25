# From Homeostasis to Collapse: Reconstructing the Continuous Landscape of Alveolar Epithelial Failure in Lethal COVID-19

**Graduate Class Project Proposal**
**Computational Biology / Systems Biology**
**Dataset: Columbia University / NYP COVID-19 Lung Atlas (SCP1219)**

---

## 1. Project Title

*From Homeostasis to Collapse: Reconstructing the Continuous Landscape of Alveolar Epithelial Failure in Lethal COVID-19*

---

## 2. Introduction and Biological Motivation

Every breath depends on a thin, fragile layer of cells deep inside the lung. The alveolar epithelium --- composed of type I (AT1) and type II (AT2) cells --- lines the roughly 480 million air sacs where oxygen enters the bloodstream and carbon dioxide leaves it. AT1 cells are extraordinarily thin and flat, stretching across about 95 percent of the alveolar surface to form the gas-exchange barrier. AT2 cells are smaller and rounder, tucked into the corners of each alveolus, where they perform two functions that are easy to underestimate until they fail: they secrete surfactant, the lipid-protein film that keeps alveoli from collapsing with each exhalation, and they serve as the resident stem cells of the alveolar compartment. When AT1 cells are lost to injury, AT2 cells divide and differentiate to replace them. This AT2-to-AT1 transition is the lung's primary mechanism for alveolar self-repair.

In lethal COVID-19, this system is pushed beyond its breaking point. SARS-CoV-2 enters AT2 cells through the ACE2 receptor, directly infecting the very cells that the lung depends on for both surfactant production and regeneration. But viral cytotoxicity is only the beginning. The host immune response --- particularly a dysregulated inflammatory cascade involving excessive cytokine release --- inflicts massive collateral damage on the alveolar epithelium. AT1 cells are destroyed, eliminating gas exchange surface. AT2 cells are simultaneously injured and activated to repair the damage, creating a biological paradox: the progenitor cells tasked with rebuilding the epithelium are themselves under assault. Pathology reports from COVID-19 lungs consistently describe diffuse alveolar damage, loss of normal tissue architecture, flooding of the air spaces with protein-rich edema fluid, and the accumulation of abnormal transitional epithelial cells that appear to be stuck between AT2 and AT1 identity --- cells that started down the repair path but could not finish it.

This biological picture motivates a question that standard analytical approaches struggle to answer. The most common strategy in single-cell genomics is to cluster cells into discrete types and then compare gene expression between clusters or between conditions (healthy vs. disease). This approach is powerful for identifying cell types and finding differentially expressed genes, but it has a fundamental blind spot: it forces what may be a continuous biological process into discrete bins. If alveolar epithelial cells under COVID-19 injury are not simply switching from "healthy" to "damaged" but instead moving through a graded series of worsening states --- from mildly stressed, to actively inflamed, to attempting repair, to failing, to undergoing programmed cell death --- then clustering will either merge these states into one group or split them at arbitrary boundaries that do not correspond to biologically meaningful transitions. A list of differentially expressed genes between "healthy" and "COVID" will tell us what changed on average, but it cannot tell us the order in which things changed, whether some cells are closer to normal than others, whether there are branching paths (repair vs. death), or where exactly the point of no return might lie.

This project takes a different approach. Instead of sorting cells into bins, we treat each cell's gene expression profile as a position in a continuous biological landscape --- what computational biologists call a manifold, but which can be understood simply as the terrain of possible cell states. On this terrain, healthy cells should sit together in a stable, coherent region that reflects normal function. Cells from COVID-19 lungs, if the hypothesis is correct, should spread outward from this region along paths associated with stress, inflammation, failed repair, and apoptosis. By reconstructing these paths and ordering cells along them, we can ask whether the molecular evidence is consistent with a staged, progressive failure of the alveolar epithelial system --- and if so, what the stages look like at the level of gene programs.

The dataset that makes this project possible is the Columbia University / NYP COVID-19 Lung Atlas, publicly available through the Broad Institute's Single Cell Portal as study SCP1219. It contains single-nucleus RNA sequencing data from 116,313 cells: 36,677 from healthy donor lungs and 79,636 from the lungs of patients who died of COVID-19. More than 20,000 of these cells are alveolar epithelial cells, providing the statistical depth needed for manifold and trajectory analyses. The contrast between healthy donor tissue and tissue from lethal cases creates an unusually clean perturbation model: the healthy cells define what alveolar homeostasis looks like, and the COVID cells show what happens when that homeostasis is overwhelmed.

---

## 3. Project Essence in Plain Language

This project asks whether alveolar epithelial cells in lethal COVID-19 fail all at once or pass through a continuous series of worsening states that we can read from their gene expression. We will build a map of alveolar cell states using single-cell RNA sequencing data from healthy and COVID-19 lungs. On this map, healthy cells should occupy a tight, stable region. COVID cells, if our hypothesis is right, should scatter outward into regions associated with stress, inflammation, stalled repair, and cell death. By tracing paths through this map and tracking which gene programs turn on and off along the way, we aim to reconstruct the molecular sequence of alveolar failure --- not as a binary event, but as a progressive collapse of cellular identity and function.

We are not claiming to watch cells change in real time. All the cells in this dataset were collected at a single moment (the time of organ donation or death). But because the tissue contains cells at many different stages of injury, we can use their gene expression patterns to infer a plausible ordering --- much the same way a photographer at a marathon can reconstruct the sequence of the race from a single panoramic shot that captures runners at every stage from start to finish. This kind of inference, called pseudotemporal ordering, is standard in developmental and disease biology, and we will be explicit throughout the project about what it can and cannot prove.

---

## 4. Central Hypothesis

We hypothesize that alveolar epithelial cells in lethal COVID-19 do not simply switch from a healthy state to a damaged one. Instead, they distribute across a continuous transcriptomic landscape that reflects the progressive erosion of homeostatic identity, the activation and subsequent failure of repair programs, and the convergence toward apoptotic and exhaustion-associated terminal states. We call this process *epithelial robustness collapse* --- the loss of the system's ability to absorb perturbation and return to its functional baseline.

This central hypothesis rests on three testable supporting claims. First, we expect that healthy alveolar cells --- both AT1 and AT2 --- will occupy a compact, coherent region of the gene expression landscape, reflecting the stability of their normal identities, while COVID-19 cells will be dispersed outward from this region in directions that correspond to specific injury and stress programs. Second, we predict that a pseudotemporal ordering of cells, anchored in the healthy homeostatic state, will reveal a biologically interpretable sequence: early interferon and antiviral response, followed by inflammatory stress, then activation of repair and differentiation machinery, and finally upregulation of apoptosis with loss of canonical cell-type markers. Third, we expect that AT1 and AT2 cells will not fail in exactly the same way: AT2 cells, because of their dual role as both viral targets and alveolar progenitors, may show distinctive evidence of stalled differentiation --- cells that began the transition toward AT1 fate but could not complete it.

---

## 5. Specific Aims

### Aim 1: Characterize the transcriptomic landscape of healthy and COVID-19 alveolar epithelial cells

The first aim is to establish the basic geometry of the problem. We will extract all alveolar epithelial cells --- AT1, AT2, and any annotated transitional populations --- from the full atlas and construct a low-dimensional representation of their gene expression states. Dimensionality reduction is a method that compresses the information from thousands of genes into a smaller number of summary axes that capture the dominant patterns of variation, making it possible to visualize and analyze the data as a landscape rather than as an uninterpretable table of numbers. On this landscape, we will compare the spatial distributions of healthy and COVID cells. Specifically, we will measure whether COVID cells are, on average, displaced farther from the center of the healthy cell distribution than healthy cells are from each other, and whether COVID cells are more spread out (higher dispersion) than healthy cells. These two metrics --- displacement and dispersion --- are our primary operational signatures of robustness loss. If healthy cells form a tight cluster and COVID cells fan outward from it along identifiable axes, the data support a model of progressive state change rather than a binary healthy-to-damaged switch.

### Aim 2: Reconstruct the trajectory of alveolar epithelial failure and score injury-associated gene programs along it

The second aim is to move from static comparison to dynamic inference. We will apply trajectory analysis --- a computational method that finds the most plausible continuous paths connecting groups of cells in gene expression space --- and assign each cell a pseudotime value. Pseudotime is not real elapsed time; it is a numerical score that reflects how far a cell's gene expression has shifted from a designated starting point, which we will set in the densest region of healthy alveolar cells. A cell with low pseudotime is transcriptomically close to normal; a cell with high pseudotime has moved far from baseline. Along this inferred trajectory, we will score every cell for the activity of curated gene programs: interferon response, NF-kB-driven inflammation, oxidative stress, AT2 self-renewal, AT2-to-AT1 differentiation, apoptosis, and cellular senescence. The biological question is straightforward --- do these programs activate and deactivate in an order that makes sense as a staged failure process? If interferon genes come on first, followed by inflammatory stress, then repair-associated genes, and finally apoptosis markers (with simultaneous loss of AT2 and AT1 identity signatures), this ordering is consistent with a progressive collapse rather than random dysregulation.

### Aim 3: Test the robustness of the inferred failure landscape through ablation, sensitivity, and control analyses

The third aim is the self-critical one. Any computational analysis involves choices --- which cells to include, which embedding method to use, whether to correct for batch effects, which gene sets to score, where to root the pseudotime. Each of these choices could, in principle, create or destroy the patterns we observe. Ablation analysis (described in detail in Section 9) is the systematic practice of removing or changing one analytical choice at a time and checking whether the biological conclusions survive. If the core findings --- progressive displacement from homeostasis, ordered gene program activation, evidence of stalled repair --- persist across many variations in method, the biological interpretation is substantially strengthened. If a specific finding collapses when one component is changed, that finding is fragile and must be reported with appropriate caution. This aim transforms the project from a single analysis into a stress-tested body of evidence.

---

## 6. Study Design

### Dataset and cohort

The study uses the Columbia University / NYP COVID-19 Lung Atlas (SCP1219), a publicly available single-nucleus RNA-seq dataset containing 116,313 nuclei from human lung tissue. The cohort includes two groups: lungs from healthy organ donors (36,677 nuclei) and lungs from patients whose cause of death was COVID-19 (79,636 nuclei). Among these, more than 20,000 nuclei are alveolar epithelial cells, which form the primary analytical population for this project.

### Focus on alveolar epithelial cells

We restrict our analysis to AT1 cells, AT2 cells, and any transitional or aberrant epithelial populations annotated in the atlas. The rationale is biological: these are the cells that form the gas-exchange surface, produce surfactant, carry out alveolar repair, and are directly targeted by SARS-CoV-2. Their failure is the proximate cause of the respiratory collapse that kills patients with severe COVID-19. Other cell types in the lung --- macrophages, T cells, endothelial cells, fibroblasts --- are biologically important and interact with the alveolar epithelium, but including them in the manifold analysis would dilute the signal we care about and introduce cell-type variation that could obscure within-epithelial injury states. They remain available for supplementary context analyses if needed.

### Comparison structure

The fundamental comparison is between alveolar epithelial cells from healthy donors (representing baseline homeostasis) and alveolar epithelial cells from lethal COVID-19 patients (representing extreme perturbation). Critically, we do not treat the COVID group as monolithic. The biological hypothesis predicts internal structure within the COVID cells: some should remain relatively close to the healthy state (mildly affected or recently injured), while others should be displaced far from it (severely altered, apoptotic, or terminally exhausted). The analysis is designed to detect and characterize this internal gradient, not just the average difference between groups.

### A cross-sectional study with pseudo-dynamic inference

It is important to be precise about what this study can and cannot claim. All cells were collected at a single moment --- the time of death or organ procurement. We did not follow any cell over time. This is a cross-sectional study. However, because the tissue at the time of sampling contains cells at many different stages of injury and response, we can use computational methods to infer a plausible ordering of these states. This approach, called pseudo-dynamic or pseudotemporal inference, is widely used in developmental biology to reconstruct differentiation trajectories from single-cell snapshots. The logic is that if cells at various stages of a process coexist in the same tissue, their gene expression patterns may recapitulate the order of that process even though no single cell was observed transitioning.

We will use this approach throughout the project, and we will be explicit throughout the project that pseudotime is an inference, not a measurement. We will say "the data are consistent with," "the ordering suggests," and "this pattern would be expected if" --- not "this proves that cells undergo." The distinction is not a weakness of the project. It is the honest framing that makes the project credible.

### Operational definition of robustness loss

Because "robustness" is a concept and not a single measurement, we define it operationally through five convergent lines of evidence. We consider robustness to be lost when: (1) COVID cells are displaced significantly farther from the centroid of the healthy cell distribution than healthy cells are from each other; (2) COVID cells show greater dispersion, occupying a wider spread of states rather than shifting coherently to a single new state; (3) canonical AT1 and AT2 identity markers decline along the inferred trajectory; (4) stress and repair programs activate before apoptosis programs along pseudotime, consistent with a staged process rather than random gene dysregulation; and (5) AT2 cells in the COVID group show evidence of initiating but not completing the AT2-to-AT1 differentiation program. No single criterion is sufficient. The case for robustness collapse rests on the convergence of all five.

---

## 7. Data Processing and Analysis Plan

This section describes each step of the computational workflow. Every method is explained in terms of what it does biologically, not just technically. The goal is for a reader with a strong biology background but limited computational experience to understand why each step exists and what it contributes to the biological question.

### Quality control

Not every captured nucleus in a single-cell experiment represents a real, healthy cell. Some are empty droplets that captured ambient RNA. Others are damaged nuclei that lost most of their RNA content. Still others are doublets --- two nuclei captured in the same droplet, producing a blended expression profile that does not correspond to any actual cell. Quality control removes these artifacts before they contaminate the analysis.

We will filter nuclei based on three standard metrics: the number of distinct genes detected per nucleus (too few suggests an empty droplet, too many suggests a doublet), the total RNA count per nucleus (same logic), and the fraction of RNA coming from mitochondrial genes (an abnormally high fraction can indicate a damaged cell in single-cell data, though this metric behaves differently in single-nucleus preparations and requires careful threshold selection). We will also remove genes detected in very few cells, as these contribute noise without biological information. Thresholds will be set based on the distributions observed in this specific dataset, not from generic defaults.

### Normalization and feature selection

Cells differ in total RNA capture for purely technical reasons --- some nuclei happen to release more RNA during library preparation than others. Normalization removes this technical variation so that gene expression levels can be compared fairly across cells. The standard approach scales each cell's counts to a common total and then applies a logarithmic transformation, which compresses the enormous range of expression values (some genes are expressed thousands of times more than others) into a more interpretable scale.

After normalization, we identify the 2,000 to 3,000 most variable genes across the dataset. Most of the roughly 20,000 protein-coding genes in the human genome are either silent in alveolar cells or expressed at constant levels in every cell (housekeeping genes). These invariant genes are uninformative for distinguishing cell states and add statistical noise. Restricting the analysis to highly variable genes focuses it on the genes that actually differ between cell states --- the genes that carry biological signal.

### Cell-type subsetting and annotation validation

Using the cell-type labels provided with the atlas, we will extract all cells annotated as AT1, AT2, or transitional/aberrant epithelial. But we will not trust annotations blindly. We will verify each label by checking expression of canonical marker genes: *SFTPC*, *SFTPA1*, and *ABCA3* for AT2 cells; *AGER*, *PDPN*, *CLIC5*, and *HOPX* for AT1 cells; and *KRT8*, *CLDN4*, and *SFN* for transitional states described in the lung injury literature. If annotations and marker expression disagree, we will re-cluster the epithelial subset independently and assign labels based on marker evidence. This step is not optional. Every downstream analysis depends on knowing which cells are actually alveolar epithelial cells.

### Batch and donor effect assessment

Cells from different donors were processed in separate experimental batches, potentially introducing technical variation that has nothing to do with biology. If two healthy donors separate on the manifold not because their cells are biologically different but because they were processed on different days, we would risk misinterpreting technical noise as biological signal.

We will assess this by visualizing the manifold colored by donor and batch identity. If technical grouping is apparent, we will apply integration methods such as Harmony or scVI, which attempt to align cells across batches while preserving genuine biological differences. We will then verify that correction removed technical stratification without erasing the healthy-vs-COVID distinction. This is a judgment call, and Section 9 includes an ablation that tests what happens with and without correction, so the reader can evaluate both versions.

### Dimensionality reduction and manifold construction

Each cell's expression profile contains measurements for thousands of genes. Analyzing data in such a high-dimensional space is both computationally impractical and biologically unintuitive. Dimensionality reduction compresses this information into a much smaller number of axes --- typically 30 to 50 principal components that capture the dominant patterns of variation in the data. These components are the quantitative foundation for everything that follows.

For visualization, we project the data further into two dimensions using UMAP (Uniform Manifold Approximation and Projection), a method that places similar cells near each other and dissimilar cells far apart on a two-dimensional plot. UMAP plots are powerful for building visual intuition about the data, but they can distort distances and create visual artifacts, so they are used for illustration rather than for quantitative analysis. We will also compute diffusion maps, an alternative projection specifically designed to preserve continuous transitions between cell states. Where UMAP tends to pull apart clusters, diffusion maps tend to preserve gradients, making them more suitable for trajectory analysis. The biological content of the data should be robust to the choice of projection method --- an expectation we test explicitly in the ablation analyses.

After dimensionality reduction, we construct a nearest-neighbor graph: a network connecting each cell to the cells most similar to it in gene expression. This graph is a computational approximation of the manifold --- the landscape of biologically accessible cell states. It serves as the backbone for trajectory inference, clustering, and all spatial analyses that follow.

### Trajectory inference and pseudotime

Trajectory inference asks whether there is a continuous path through the cell-state landscape connecting one region to another. If cells are arranged not as isolated islands but as a continuous stream from healthy to injured to apoptotic, trajectory algorithms will find that stream and order the cells along it.

Pseudotime assigns each cell a number representing its position on the inferred path. We will root the trajectory in the densest region of healthy AT2 cells, which represents the homeostatic baseline. A cell with pseudotime near zero is close to normal; a cell with high pseudotime has moved far from baseline in the direction of injury. The trajectory may branch --- for instance, one branch leading toward AT2-to-AT1 differentiation (repair) and another toward apoptosis (death) --- and we will test for this possibility.

We will use diffusion pseudotime or a comparable algorithm (such as Palantir) for the primary analysis. The choice of root cell is biologically motivated but analytically consequential, so Section 9 includes an ablation that tests whether conclusions change when the root is moved.

### Gene program scoring

Rather than tracking thousands of individual genes, we will summarize cellular state using gene programs --- curated lists of genes known to participate in specific biological processes. Each cell receives a score for each program, reflecting the overall activity level of that process in that cell. This is analogous to checking whether a cell has turned on its antiviral alarm, its inflammatory response, its repair machinery, or its self-destruction program --- but doing so at the level of coordinated gene sets rather than one gene at a time.

The programs we will score include: AT2 cell identity (*SFTPC*, *SFTPA1*, *LAMP3* and related genes), AT1 cell identity (*AGER*, *PDPN*, *HOPX*), type I and type II interferon response (canonical interferon-stimulated genes reflecting antiviral signaling), NF-kB-driven inflammatory signaling, oxidative stress response, AT2-to-AT1 transitional differentiation (*KRT8*, *CLDN4*, *SFN*), apoptosis (including *BAX*, *CASP3*, *BCL2L11*, and the MSigDB Hallmark Apoptosis set), and cellular senescence. Scoring will use established methods (such as Scanpy's `score_genes` or AUCell) that estimate program activity relative to a background of randomly selected genes of similar expression level, controlling for the general expression level of each cell.

### Robustness and dispersion metrics

To move beyond visual impressions, we will quantify the degree of homeostatic displacement and dispersion using four complementary metrics. First, centroid distance: the average distance of each COVID cell from the center of the healthy cell distribution in the principal component space, compared to the average distance of healthy cells from their own center. Second, within-group dispersion: the variance of cell positions within the healthy group versus within the COVID group. Third, nearest-neighbor condition mixing: for each cell, the proportion of its nearest neighbors that share its condition label, which measures the degree of spatial overlap or separation between conditions. Fourth, pseudotime density: the distribution of cells along pseudotime, stratified by condition, which reveals whether COVID cells are concentrated at specific injury stages or spread broadly across the trajectory.

---

## 8. Main Experiments and Biological Interpretation

This section describes the core analytical experiments of the project. Each experiment addresses a specific biological question, and each is designed so that its results can be interpreted in terms of alveolar biology, not just statistical output.

### Experiment 1: Identification and validation of the alveolar epithelial population

Before any trajectory or manifold analysis, we must confirm that we are studying the right cells. We will subset all cells annotated as AT1, AT2, or transitional epithelial from the full atlas, then verify each population by examining canonical marker gene expression. AT2 cells should express *SFTPC* strongly and lack *AGER*; AT1 cells should show the reverse pattern. Transitional cells, if present, should co-express markers from both populations along with stress-associated genes like *KRT8*. Any cells whose marker profiles contradict their labels will be re-evaluated. The expected outcome is a clean, well-validated set of approximately 20,000 alveolar epithelial nuclei forming the foundation for all subsequent analyses. This step is methodological, but its importance cannot be overstated: every biological conclusion downstream depends on the accuracy of cell identity.

### Experiment 2: Construction of the alveolar manifold and condition-level comparison

With validated alveolar cells in hand, we will build the transcriptomic landscape. After PCA, nearest-neighbor graph construction, and UMAP embedding, we will color the resulting plot by condition (healthy vs. COVID), cell type (AT1, AT2, transitional), and donor identity. The biological question is visual and quantitative: do COVID cells occupy the same region as healthy cells, or are they displaced? If healthy cells form a compact cluster and COVID cells spread outward from it --- some nearby, some far away --- this directly visualizes the hypothesis that injury produces a gradient of states rather than a single new state. We will quantify this with centroid distance and dispersion metrics (described above), and we will report these metrics separately for AT1 and AT2 cells, since the two populations may respond differently to injury. If COVID AT2 cells show greater displacement than COVID AT1 cells, it could reflect their dual burden as both viral targets and the cells responsible for repair.

### Experiment 3: Pseudotime trajectory from homeostasis through injury to apoptosis

This experiment asks whether the distribution of cells on the manifold is consistent with a continuous path of progressive failure. We will apply diffusion pseudotime rooted in the healthy AT2 population and examine the trajectory structure. Does the trajectory extend smoothly from healthy cells toward increasingly injured and apoptotic cells? Does it branch --- with one arm toward repair (cells differentiating toward AT1) and another toward death? Branching would be biologically significant, suggesting that injured cells face a fate decision with distinct molecular signatures on each branch. The existence of a coherent trajectory (as opposed to randomly scattered cells) is itself a meaningful result: it means the injury process leaves a continuous transcriptomic trace, not just an endpoint.

### Experiment 4: Gene program dynamics along the trajectory

With cells ordered along pseudotime, we can now ask the most biologically specific question in the project: in what order do molecular programs activate and fail? We will plot each gene program score as a function of pseudotime, using smoothed trend lines to reveal the temporal pattern. The expected cascade --- based on known lung injury biology --- is: early activation of interferon-stimulated genes (the cell's first antiviral response), followed by NF-kB and inflammatory signaling (reflecting the broader tissue inflammatory environment), then upregulation of AT2-to-AT1 differentiation markers (the repair response), and finally activation of apoptosis genes accompanied by declining AT2 and AT1 identity scores (the failure of both repair and normal function).

If the data show this ordering, it supports a model of staged failure in which cells attempt to respond and recover before succumbing. If apoptosis genes activate simultaneously with the earliest stress genes, the process may be more catastrophic than staged. If repair genes never activate at all, the cells may be dying before repair can even begin. Each of these outcomes has a different biological interpretation, and the data will discriminate among them.

### Experiment 5: Quantification of homeostatic displacement

This experiment translates the visual impressions from Experiment 2 into statistical evidence. For every alveolar cell, we compute its distance from the centroid of the healthy cell distribution in principal component space. We then compare the distribution of these distances between healthy and COVID cells using a Mann-Whitney U test. We also compute dispersion (variance of positions) within each group. The prediction is that COVID cells are significantly farther from the healthy centroid and significantly more dispersed. We will perform this analysis separately for AT1 and AT2 cells, because the biological expectation is that AT2 cells may be more severely affected given their role as both viral targets and regenerative progenitors. A statistically significant result here provides the quantitative backbone for the qualitative claim that COVID-19 disrupts alveolar homeostatic positioning.

### Experiment 6: Identification of transitional and failed-repair states

One of the most clinically relevant questions in lung injury biology is whether AT2 progenitor cells attempt to repair the damaged epithelium and, if so, where and why repair stalls. We will examine cells at intermediate pseudotime positions for molecular signatures of the AT2-to-AT1 transitional state: co-expression of AT2 surfactant genes, partial AT1 markers, and the transitional markers *KRT8*, *CLDN4*, and *SFN* that have been described in mouse and human lung injury studies. If such cells exist predominantly in the COVID group and occupy a distinct region of the trajectory between healthy and apoptotic endpoints, they likely represent cells that initiated the differentiation program in response to AT1 loss but were unable to complete the transition. These stalled cells --- variously called "transitional," "damage-associated transient progenitors," or "aberrant basaloid cells" in the literature --- are of intense interest because they may represent a therapeutically accessible state: cells that have not yet committed to death but cannot complete repair without intervention.

### Experiment 7: Donor-level consistency

A result that depends on one unusual patient is not a generalizable biological finding. For each donor in the dataset, we will compute the distribution of pseudotime values among their alveolar cells and compare these distributions across donors within each condition. The prediction is that all or most COVID donors will show a shift toward higher pseudotime relative to all healthy donors, though the magnitude of the shift may vary (reflecting differences in disease duration or severity at the time of death). If one COVID donor's cells cluster entirely at low pseudotime while another's cluster at high pseudotime, this internal heterogeneity is itself informative --- it may reflect different stages of the disease process captured at the moment of tissue collection. What would undermine confidence is if the entire trajectory effect were driven by a single donor, which would suggest an artifact of that individual's tissue quality or an atypical clinical course.

---

## 9. Ablation and Sensitivity Analyses

This section is the self-critical backbone of the project, and it deserves careful explanation for readers who may not be familiar with the concept.

### What ablation means in this context

In experimental biology, one of the most powerful strategies for testing whether something matters is to remove it and observe the consequences. Knock out a gene. Block a receptor. Deplete a cell type. If the phenotype changes, the removed component was important. Ablation analysis in computational biology follows exactly the same logic, applied to analytical choices rather than biological components. We remove or change one element of the analysis at a time --- a cell population, an embedding method, a gene set, a batch correction step --- and ask whether the biological conclusions still hold. If a finding survives many such ablations, it is robust: the conclusion does not depend on any single choice we made. If it collapses when one specific component is removed, we know exactly where the fragility lies and can report it honestly.

The ablation analyses below are not busywork. They are the experiments that separate a defensible biological claim from a method-dependent artifact. Each ablation is described in terms of what is changed, why the change matters, and what outcome would strengthen or weaken our confidence in the core findings.

### Ablation 1: Analyzing AT2 cells alone versus AT1 and AT2 together

AT1 and AT2 cells have very different baseline transcriptomic profiles. When both are included in the same manifold, much of the variation in the data may simply reflect the difference between these two cell types rather than differences in injury state. By removing AT1 cells and analyzing AT2 cells alone, we test whether the injury trajectory and gene program ordering are visible within a single cell type. If healthy AT2 cells sit at one end of the trajectory and apoptotic COVID AT2 cells sit at the other, with the same ordered cascade of programs in between, the finding cannot be attributed to AT1-vs-AT2 compositional differences. If the trajectory disappears in the AT2-only analysis, it may have been driven by shifts in cell-type proportions rather than by changes within AT2 cells --- a fundamentally different biological story.

### Ablation 2: Comparing embedding methods

We will repeat the trajectory analysis using two different approaches to constructing the low-dimensional representation of the data: PCA with UMAP (the most common method, which emphasizes local cell neighborhoods) and diffusion maps (which emphasize smooth, continuous transitions). These methods make different mathematical assumptions, and they can produce different-looking landscapes from the same data. If the core trajectory --- healthy cells at one end, a progression through stress and repair, apoptotic cells at the other end --- appears under both methods, we can be more confident that it reflects genuine biological structure in the data rather than a property of one particular algorithm. Minor differences between methods are expected and do not undermine the finding; what would be concerning is a trajectory that exists under one method but vanishes entirely under the other.

### Ablation 3: With and without batch correction

Batch correction is necessary when technical variation between experimental batches is large enough to obscure biological signal. But batch correction is also an intervention that changes the data, and aggressive correction can remove real biological variation along with technical noise --- especially when disease state (the biology we care about) is partially correlated with batch (because healthy and COVID samples were processed separately). By running the full analysis with and without batch correction, we can see whether the trajectory is present in both versions. If it appears in both, the finding is robust to this choice. If it appears only after correction, it might be a genuine signal that was previously obscured by batch effects, but it could also be an artifact introduced by the correction. If it disappears after correction, the correction may have been too aggressive, or the original signal may have been a batch artifact. Presenting both versions transparently lets the reader evaluate the evidence.

### Ablation 4: Removing apoptosis genes from the manifold

Our hypothesis predicts that apoptosis is the terminal stage of the failure trajectory. But what if the entire trajectory is organized by apoptosis genes and nothing else? To test this, we will remove all apoptosis-related genes from the highly variable gene list before constructing the manifold and running trajectory analysis. If the trajectory persists --- carried now by interferon, stress, repair, and identity genes --- then the trajectory captures a multi-faceted biological process of which apoptosis is one component but not the sole driver. If the trajectory collapses without apoptosis genes, the manifold was essentially a gradient from "alive" to "dead" and the intermediate states we described may not have independent biological meaning. This is one of the most important ablations in the project because it directly tests whether the trajectory tells us more than a simple cell-viability score.

### Ablation 5: Varying the pseudotime root cell

Pseudotime algorithms require a starting point --- a root cell from which all other cells' distances are measured. We will root in the densest region of healthy AT2 cells by default, but we will also test alternative roots: a healthy AT1 cell, a randomly selected healthy cell, and a COVID cell at the extreme opposite end of the manifold. The biological conclusions should not depend on which specific healthy cell serves as the starting point. If the gene program ordering is preserved regardless of root choice (interferon before inflammation before repair before apoptosis), the trajectory structure is intrinsic to the data rather than an artifact of starting-point selection. Rooting in a COVID cell and observing the reverse ordering (apoptosis at low pseudotime, homeostasis at high pseudotime) would provide additional confirmation that the axis is real and biologically oriented.

### Ablation 6: Including neighboring epithelial populations

In severe lung injury, the boundary between alveolar and airway epithelium can blur. Metaplastic processes may introduce airway-like cells (club cells, basal cells) into the alveolar compartment. By expanding the analysis to include these neighboring epithelial populations alongside alveolar cells, we test two things: whether the alveolar-specific injury trajectory remains visible as a distinct feature within the broader epithelial landscape, and whether the gene program ordering along it is unchanged. If the alveolar trajectory survives embedding in a larger cellular context, it is a robust and specific feature of alveolar biology, not a generic epithelial response to injury.

### Ablation 7: Leave-one-donor-out

This is the single-cell equivalent of checking whether a clinical trial result holds when you remove one patient. We will rerun the trajectory analysis multiple times, each time excluding one donor from the dataset. If every iteration produces qualitatively similar results --- the same trajectory structure, the same gene program ordering, the same condition-level pseudotime shift --- the finding is not driven by any single donor's unusual biology or tissue quality. If removing one specific donor substantially changes the results, that donor warrants investigation: perhaps their tissue was processed differently, or perhaps their disease course was atypical. Either way, the leave-one-donor-out analysis tells us exactly how much each individual patient contributes to the overall conclusion.

---

## 10. Controls and Validation

### Biological controls

Every cell-type label used in this study will be validated against canonical marker gene expression. AT2 cells must express *SFTPC* and lack *AGER*; AT1 cells must show the reverse. Transitional cells should express *KRT8* alongside partial markers from both lineages. If labels and markers disagree, the labels are wrong, and we will re-annotate before proceeding.

Our inferred trajectory must recover known features of lung injury biology. The AT2-to-AT1 differentiation axis is well characterized in mouse models and human tissue studies: *KRT8* is upregulated in the transitional state, AT2 surfactant genes decline, and AT1 flatness-associated genes increase. If our trajectory contradicts this established biology --- for instance, if *SFTPC* increases along pseudotime while apoptosis markers decrease --- something in the analysis is likely wrong. Known biology serves as a ground-truth check on the computational inference.

As a basic sanity check, cells expressing known apoptosis effectors (*CASP3*, *BAX*) should receive high apoptosis program scores. Healthy cells should not score highly on interferon or apoptosis programs. Violations of these expectations would indicate a problem with gene set curation or scoring methodology.

### Analytical controls

We will use permutation testing to assess the statistical significance of the condition-pseudotime association. By randomly shuffling the healthy and COVID labels across cells and recomputing the pseudotime enrichment analysis, we generate a null distribution against which the real association can be compared. If the observed difference in pseudotime distributions between healthy and COVID cells is significantly greater than the permuted distribution, the association is unlikely to arise by chance.

We will also score cells using randomly generated gene sets of the same size as each curated program. If random gene sets show no structured trend along pseudotime while the curated biological programs do, this confirms that the program-pseudotime relationships are driven by coordinated biological signal rather than by statistical noise or general expression-level effects.

UMAP embeddings will be regenerated with different random seeds to confirm that the large-scale structure of the manifold (relative positions of healthy vs. COVID cells, AT1 vs. AT2 clusters) is stable. Features that shift between random seeds should not be interpreted biologically.

Where published analyses of this dataset or comparable COVID-19 lung atlases exist, we will compare our findings to them. Agreement with independent work strengthens confidence; disagreement requires investigation and honest reporting.

---

## 11. Expected Results

We state the following as realistic expectations grounded in known lung injury biology, not as guaranteed outcomes. The purpose of this section is to make our predictions explicit so that the data can confirm, refine, or contradict them.

We expect that healthy alveolar cells will form a compact, internally coherent region on the transcriptomic manifold, with AT1 and AT2 cells well separated from each other but tightly clustered within each type. This would reflect the stability of homeostatic cell identity in the uninjured lung.

We expect that COVID-19 alveolar cells will not form a single displaced cluster but will instead spread outward from the healthy region in multiple directions, occupying a broader and more diffuse territory on the manifold. This dispersion would reflect the heterogeneity of injury states captured at the time of tissue collection: some cells recently injured and still near baseline, others severely altered and far from normal.

We expect that pseudotime analysis will reveal an ordered molecular cascade along the trajectory from homeostasis to failure. Specifically, we predict early activation of interferon-stimulated genes, followed by NF-kB-driven inflammatory signaling, then partial activation of the AT2-to-AT1 differentiation program, and finally upregulation of apoptosis-associated genes accompanied by loss of canonical AT2 and AT1 identity markers. This ordering would be consistent with a staged failure process in which cells first respond to viral insult, then attempt repair, and finally succumb when repair fails.

We expect to identify a population of transitional cells at intermediate pseudotime positions --- cells co-expressing AT2 markers, partial AT1 markers, and stress-associated genes. These cells likely correspond to the "damage-associated transient progenitor" or "aberrant basaloid" states described in recent lung injury literature: AT2 cells that initiated repair-associated differentiation but stalled mid-process. We expect these cells to be found predominantly in the COVID group.

We expect the core findings to be broadly robust across the ablation analyses, though specific quantitative details (exact pseudotime values, precise locations of trajectory branch points) may vary with analytical choices. Findings that prove fragile will be identified and discussed transparently.

---

## 12. Potential Pitfalls and Alternative Strategies

### Noisy cell-type annotations

If the original atlas annotations misclassify non-alveolar cells as alveolar, every downstream analysis will be contaminated. Our mitigation is stringent: we validate all labels against canonical marker genes before proceeding, and we re-annotate from scratch if the existing labels are unreliable. This is labor-intensive but non-negotiable.

### Donor effects overwhelming biological signal

If the variability between individual donors is larger than the variability between healthy and COVID injury states, the manifold will organize by patient identity rather than by biology. Batch correction (Harmony, scVI) is the first-line response, followed by leave-one-donor-out analysis to confirm that no single donor drives the findings. If donor effects remain dominant even after correction, we will restrict the analysis to a carefully matched subset of donors processed under comparable conditions, accepting reduced sample size in exchange for cleaner signal.

### Absence of clear trajectory structure

If alveolar cells do not form a continuous gradient but instead cluster into discrete islands with no connecting bridge cells, pseudotime analysis will produce arbitrary orderings and the trajectory framework will not be appropriate. We will check for this by examining the connectivity of the nearest-neighbor graph and the continuity of the cell distribution before attempting trajectory inference. If the data genuinely lack trajectory structure, we will pivot to a cluster-based analysis that compares discrete cell states (homeostatic, stressed, transitional, apoptotic) through pairwise differential expression. This approach is less elegant but more honest when the data do not support continuous inference.

### Over-interpretation of pseudotime

Pseudotime infers an ordering from a snapshot. It does not prove that individual cells actually traverse the inferred path, nor does it establish the real-world timescale of the process. We will mitigate this by framing all results as "consistent with" rather than "demonstrating" a temporal progression, by checking whether the inferred gene program ordering matches known biology, and by stating explicitly in all written output that confirmation of temporal dynamics would require longitudinal studies or lineage tracing, which are beyond the scope of this project.

### Difficulty distinguishing apoptosis from general stress

Many apoptosis-associated genes are also induced by cellular stress, making it hard to separate cells that are committed to dying from cells that are stressed but potentially recoverable. We will use multiple independent apoptosis gene sets and compare them against general stress gene sets to determine whether these states can be distinguished transcriptomically. If they cannot, we will describe the terminal state honestly as "stress/apoptosis" rather than claiming to resolve a distinction the data do not support.

### The fundamental limitation of cross-sectional data

No analytical method can convert a cross-sectional dataset into a true time-course study. This limitation is inherent in the experimental design and cannot be fixed computationally. We can generate hypotheses about the temporal order of molecular events, and we can test whether the data are consistent with those hypotheses, but we cannot prove that the events occur in the inferred order in any individual cell. Acknowledging this limitation clearly and consistently is not a concession --- it is what separates a credible project from one that overclaims.

---

## 13. Biological Significance

This project addresses a question at the center of lung injury biology: how does the alveolar epithelium --- the tissue that makes breathing possible --- fail under extreme stress? The answer matters beyond COVID-19. Diffuse alveolar damage, the pathological pattern that destroys the gas-exchange surface, occurs in many forms of acute respiratory distress: bacterial pneumonia, aspiration injury, sepsis, ventilator-induced lung injury. In each case, the alveolar epithelium is challenged beyond its capacity to maintain structure and function. Understanding the sequence of molecular events that leads from homeostasis to collapse --- and identifying the intermediate states where repair is attempted and where it stalls --- has implications for any condition in which the lung's regenerative capacity is overwhelmed.

The concept at the heart of this project, robustness, is central to systems biology. A robust biological system maintains its function despite perturbation. The alveolar epithelium is robust to minor insults: small injuries heal, lost AT1 cells are replaced by differentiating AT2 cells, and the tissue returns to baseline. But when perturbation exceeds some threshold, robustness breaks down. The AT2 progenitors that should rebuild the epithelium are themselves damaged. Repair stalls. Cells accumulate in transitional states that are neither functional AT1 nor functional AT2. The tissue fills with fluid, gas exchange fails, and the patient dies.

By constructing a data-driven map of this failure process, we contribute to a growing body of work that treats disease not as a binary state (healthy or sick) but as a trajectory through a landscape of cellular states. This perspective creates opportunities for thinking about intervention in new ways: not just "block the virus" or "suppress inflammation," but "identify the cells that are stuck in transitional states and help them complete the repair program." This project will not identify therapeutic targets directly, but it will provide the kind of detailed, rigorously validated landscape that such translational work requires as a starting point.

---

## 14. Deliverables

**Final written report (15--25 pages).** A complete project report structured as an abbreviated research paper: introduction with biological motivation, methods described in accessible language, results with figures and quantitative analysis, discussion of findings and limitations, and references. Written for a mixed audience of biologists and computational scientists.

**Main figures (5--7).** Publication-quality figures covering the alveolar manifold, pseudotime trajectory, gene program dynamics, homeostatic displacement metrics, and key ablation results. Each figure will include a descriptive legend sufficient for interpretation without reference to the main text.

**Supplementary tables.** Table S1: curated gene lists for all scored programs, with literature sources. Table S2: quality control metrics and filtering thresholds applied. Table S3: top genes with significant expression trends along pseudotime. Table S4: donor-level summary statistics (cell counts, pseudotime distributions, QC metrics).

**Analysis notebook.** A documented Jupyter notebook (or organized set of Python scripts) that reproduces all analyses from processed counts to final figures. Code will be annotated, organized by analysis step, and executable from the project virtual environment (`lesegenv`, Python 3.10).

**Oral presentation (15--20 minutes).** A slide-based presentation summarizing the biological question, analytical approach, key findings, ablation results, and conclusions. Designed for a mixed audience of biologists and computational researchers.

---

## 15. Suggested Figures

**Figure 1: The alveolar epithelial manifold.** UMAP embedding of all alveolar epithelial cells, colored by condition (healthy vs. COVID) in one panel and by cell type (AT1, AT2, transitional) in a second panel. This figure establishes the visual foundation for the project by showing that healthy cells cluster compactly while COVID cells disperse outward.

**Figure 2: Pseudotime trajectory overlaid on the manifold.** The same UMAP embedding colored by inferred pseudotime value, from blue (low, homeostatic) to red (high, failure-associated), with trajectory paths drawn. This figure shows whether the cell-state landscape supports a continuous progression from health to failure.

**Figure 3: Gene program dynamics along pseudotime.** A multi-panel figure (heatmap or smoothed ribbon plot) showing the activity scores of each curated gene program as a function of pseudotime. This is the central result figure of the project: it reveals the order in which molecular programs activate and fail along the trajectory.

**Figure 4: Pseudotime density distributions by condition.** Split violin or ridge plots showing the distribution of pseudotime values for healthy cells versus COVID cells. This figure quantifies the shift: healthy cells are concentrated at low pseudotime, while COVID cells are displaced toward and distributed across higher pseudotime values.

**Figure 5: Individual marker gene expression along pseudotime.** Smoothed line plots for selected genes --- *SFTPC*, *AGER*, *KRT8*, *ISG15*, *CASP3*, *BAX* --- showing how canonical identity, transitional, interferon, and apoptosis markers behave along the inferred trajectory. This figure grounds the program-level analysis in specific molecular readouts.

**Figure 6: Ablation summary.** A compact multi-panel figure comparing the core finding (pseudotime distribution of COVID vs. healthy cells, or program ordering along pseudotime) across key ablations: AT2-only, alternative embedding, no batch correction, apoptosis genes removed. This figure demonstrates which findings are robust and which are sensitive to analytical choices.

**Figure 7: Donor-level consistency.** Boxplots or violin plots showing pseudotime distributions per individual donor, stratified by condition. This figure confirms that the trajectory shift is a general feature of COVID-19 alveolar injury, not an artifact of one outlier patient.

---

## 16. Timeline

**Week 1: Data acquisition and preprocessing.** Download the SCP1219 dataset. Perform quality control filtering. Normalize and log-transform. Identify highly variable genes. Verify cell-type annotations against canonical markers. Set up the analysis environment and establish the notebook structure.

**Week 2: Alveolar subsetting and manifold construction.** Extract the AT1, AT2, and transitional epithelial population. Assess and, if necessary, correct for batch and donor effects. Run PCA, compute the nearest-neighbor graph, and generate UMAP and diffusion map embeddings. Produce initial visualizations comparing healthy and COVID cell distributions. Compute centroid distance and dispersion metrics.

**Week 3: Trajectory inference and gene program analysis.** Run diffusion pseudotime (or Palantir) rooted in healthy AT2 cells. Score all cells for the eight curated gene programs. Plot program scores along pseudotime and assess the ordering. Identify transitional and failed-repair cell states. Compute robustness and dispersion statistics.

**Week 4: Ablation, sensitivity, and control analyses.** Execute all seven ablation experiments. Run permutation controls for pseudotime-condition association. Run random gene set controls for program scoring. Compile ablation results into a summary comparison.

**Week 5: Figures and writing.** Generate all main and supplementary figures. Write the methods and results sections of the report. Draft figure legends. Begin the introduction and discussion.

**Week 6: Completion and presentation.** Finish the written report (introduction, discussion, abstract). Prepare the oral presentation. Clean and document the analysis code. Review all figures for clarity and consistency. Final revision and submission.

---

## 17. Final Summary

This project investigates whether the alveolar epithelial cells of the human lung --- the cells responsible for gas exchange, surfactant production, and tissue self-repair --- fail through a continuous, staged process under lethal COVID-19 infection, or whether they simply switch from healthy to damaged without intermediate states. Using single-nucleus RNA sequencing data from 116,313 lung cells in the Columbia/NYP COVID-19 Lung Atlas, we construct a transcriptomic landscape of alveolar cell states, infer pseudotemporal trajectories from homeostasis toward failure, and score cells for the activity of interferon, inflammatory, repair, and apoptosis gene programs at each point along the trajectory. The project tests whether these programs activate in a biologically coherent order consistent with staged robustness collapse --- stress before repair, repair before apoptosis, apoptosis accompanied by loss of normal cell identity --- and whether intermediate states corresponding to stalled AT2-to-AT1 differentiation are enriched among COVID-19 cells. Seven systematic ablation analyses, varying cell-type composition, embedding methods, batch correction, gene set content, pseudotime root selection, cellular context, and donor inclusion, test whether the biological conclusions are robust to the analytical choices that produced them. The result is a rigorously validated, biology-centered map of how the alveolar epithelial system moves from function to failure under extreme perturbation, with implications for understanding lung injury, tissue robustness, and the limits of epithelial repair beyond COVID-19.

---

*Proposal prepared for a graduate-level computational biology / systems biology course.*
*Dataset: Columbia University / NYP COVID-19 Lung Atlas, Single Cell Portal SCP1219.*

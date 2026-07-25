# Graduate Class Project Plan: Alveolar Epithelial Robustness Under Lethal COVID-19

---

## 1. Project Title

**Option A:**
*Mapping the Loss of Alveolar Epithelial Robustness in Lethal COVID-19: A Transcriptomic Trajectory Analysis of Cell-State Exhaustion and Failed Repair*

**Option B:**
*From Homeostasis to Collapse: Reconstructing the Continuous Landscape of Alveolar Epithelial Failure in Severe SARS-CoV-2 Lung Injury*

**Option C:**
*Alveolar Epithelial Identity Under Extreme Perturbation: Pseudotemporal and Gene-Program Analysis of Cell-State Dissolution in the COVID-19 Lung*

---

## 2. Project Essence in Plain Language

The cells that line the air sacs of the lung --- alveolar epithelial cells --- are responsible for gas exchange, barrier integrity, and self-repair after injury. In patients who die from COVID-19, these cells face an overwhelming assault: viral infection, runaway inflammation, and tissue destruction that ultimately proves fatal. This project asks a simple but important question: do these alveolar cells fail all at once, or do they pass through a continuous series of worsening states --- from stressed, to injured, to attempting repair, to exhausted, to dying --- that we can read directly from their gene expression?

Rather than just sorting cells into "healthy" and "COVID" and asking which genes differ between the two groups, we will treat the gene expression of each individual cell as a position in a biological landscape. In that landscape, healthy cells should cluster together in a stable, coherent region that reflects normal lung function. COVID-19 cells, by contrast, may scatter across the landscape, occupying positions associated with inflammation, stress, failed attempts at regeneration, and programmed cell death. If we can reconstruct this landscape and trace plausible paths through it, we gain something that simple group comparisons cannot provide: a picture of the process by which alveolar cells progressively lose their identity and function. That picture matters, because understanding where cells get stuck, where repair fails, and where the point of no return lies could eventually inform how we think about therapeutic intervention in severe lung injury --- not only from COVID-19 but from other causes of acute respiratory distress.

---

## 3. Biological Background and Motivation

### The alveolar epithelium: structure and function

The human lung terminates in roughly 480 million alveoli --- tiny, thin-walled sacs where oxygen crosses into the blood and carbon dioxide crosses out. Two specialized epithelial cell types line these sacs. **Type I alveolar cells (AT1)** are extremely flat, covering about 95% of the alveolar surface area, and form the gas-exchange interface. **Type II alveolar cells (AT2)** are smaller and cuboidal, occupying the remaining 5% of the surface, and serve two critical roles: they secrete pulmonary surfactant (a lipid-protein mixture that keeps alveoli from collapsing), and they function as the resident stem/progenitor cells of the alveolar epithelium. When AT1 cells are damaged, AT2 cells proliferate and differentiate to replace them. This AT2-to-AT1 differentiation axis is the lung's primary mechanism for alveolar repair after injury.

### Why AT1 and AT2 cells matter in COVID-19 lung injury

SARS-CoV-2 enters cells primarily through the receptor ACE2, which is expressed on a subset of AT2 cells, making the alveolar epithelium a direct target of viral entry. In lethal COVID-19, the damage goes far beyond direct viral cytotoxicity. The host immune response --- particularly a dysregulated inflammatory cascade sometimes called a cytokine storm --- inflicts massive collateral damage on the alveolar epithelium. AT1 cells are destroyed, compromising gas exchange. AT2 cells are simultaneously injured and called upon to repair the damage, creating a cruel biological paradox: the cells that must regenerate the epithelium are themselves under assault. Pathological studies of COVID-19 lungs consistently describe diffuse alveolar damage (DAD), loss of normal alveolar architecture, accumulation of protein-rich fluid in the air spaces (pulmonary edema), and the appearance of abnormal, transitional epithelial cells that are neither fully AT2 nor fully AT1 --- cells apparently caught mid-repair and unable to complete the differentiation program.

### Lethal COVID-19 as a perturbation model

From a systems biology perspective, lethal COVID-19 represents an extreme natural perturbation of the lung epithelial system. Healthy lungs maintain a robust homeostatic state: AT1 and AT2 cells hold their identities, turnover is slow, and the tissue is structurally stable. COVID-19 pushes this system to its breaking point. The question is not simply "what genes change" but rather how the entire cellular landscape deforms under this perturbation --- whether cells are displaced smoothly or catastrophically, whether repair programs are activated and then stall, and whether identifiable intermediate states exist between health and death. The Columbia/NYP COVID-19 Lung Atlas (SCP1219) provides an unusually rich resource for this question, with single-nucleus RNA-seq data from 116,313 cells spanning healthy donor lungs and lungs from patients who died of COVID-19, including more than 20,000 alveolar epithelial cells.

### Why standard clustering and differential expression are not enough

The most common approach in single-cell biology is to cluster cells into discrete groups and then ask which genes are differentially expressed between clusters or between conditions. This approach is powerful but has a fundamental limitation: it forces a continuous biological process into discrete bins. If alveolar cells under COVID-19 injury are moving through a progressive series of states --- from mildly stressed, to actively inflamed, to attempting repair, to failing, to apoptotic --- then clustering will either lump these states together or split them into arbitrary groups whose boundaries do not reflect meaningful biological transitions. Differential expression between "healthy" and "COVID" will identify genes that change on average, but it will miss the order and directionality of change, the existence of branching paths (e.g., successful repair vs. apoptosis), and the possibility that some cells are closer to the healthy state while others have moved much further away.

### The case for a manifold and trajectory view

A more informative approach is to treat each cell's transcriptome as a point in a high-dimensional space, and then to learn the underlying shape --- the manifold --- of that space. A manifold, in biological terms, is simply the landscape of possible cell states that the data actually occupy. It is the terrain, and each cell sits at a particular location on that terrain. Once we have this landscape, we can ask trajectory questions: is there a continuous path from one region to another? Do cells appear to flow along that path, with gene programs turning on and off in a biologically coherent order? We can use pseudotime --- an ordering of cells along such a path that serves as a proxy for biological progression even though we are looking at a single snapshot in time --- to reconstruct the sequence of molecular events. This does not prove that any individual cell actually traversed the path (the data are cross-sectional, not longitudinal), but it can reveal whether the gene expression patterns are consistent with a progressive process and can generate testable hypotheses about the order in which stress responses, repair programs, and apoptotic programs are activated and fail.

---

## 4. Central Hypothesis

**Main Hypothesis:**
Alveolar epithelial cells in lethal COVID-19 do not simply switch from a healthy state to a damaged state; instead, they distribute across a continuous transcriptomic landscape that reflects progressive loss of homeostatic identity, activation and subsequent failure of repair programs, and convergence toward apoptotic and exhaustion-associated states --- a process we term *epithelial robustness collapse*.

**Sub-hypothesis 1:**
Healthy alveolar epithelial cells (both AT1 and AT2) occupy a compact, coherent region of the transcriptomic manifold, reflecting stable homeostatic identity, whereas COVID-19 alveolar cells are dispersed away from this region in directions associated with specific injury and stress programs.

**Sub-hypothesis 2:**
Pseudotime analysis rooted in the healthy homeostatic state will reveal an ordered, biologically interpretable progression from homeostasis through interferon response and inflammatory stress, into transitional/repair-attempting states, and ultimately toward apoptosis or terminal exhaustion --- and COVID-19 cells will be enriched at progressively later points along this trajectory.

**Sub-hypothesis 3:**
The loss of alveolar robustness is not a single uniform process: AT1 and AT2 cells may follow partially distinct trajectories of failure, reflecting their different functional roles and vulnerabilities, with AT2 cells potentially showing evidence of stalled or incomplete differentiation toward AT1 fate.

---

## 5. Specific Aims

### Aim 1: Characterize the transcriptomic landscape of healthy and COVID-19 alveolar epithelial cells

- **Biological objective:** Determine whether healthy and COVID-19 alveolar epithelial cells occupy distinct, separable regions of gene expression space, and whether the COVID-19 cells show evidence of progressive displacement rather than a simple binary shift.
- **Computational/analytical approach:** Subset alveolar epithelial cells (AT1, AT2, and transitional populations) from the full atlas. Perform dimensionality reduction --- a method that compresses the information from thousands of genes into a small number of summary axes that capture the major patterns of variation --- to construct a low-dimensional manifold (landscape) of alveolar cell states. Compare the spatial distribution of healthy vs. COVID cells on this landscape using density and dispersion metrics.
- **Expected biological insight:** If the healthy cells form a tight cluster and the COVID cells fan outward along identifiable axes, this supports the idea of progressive robustness loss rather than a simple on/off injury switch.

### Aim 2: Reconstruct the trajectory of alveolar epithelial failure and score injury-associated gene programs along it

- **Biological objective:** Determine whether alveolar cells under COVID-19 injury move through an ordered sequence of transcriptomic states that can be interpreted as stress, repair attempt, repair failure, and apoptosis.
- **Computational/analytical approach:** Apply trajectory inference (a method that finds the most plausible continuous paths connecting groups of cells in gene expression space) and pseudotime ordering (which assigns each cell a position along such a path, as a proxy for how far it has progressed through the process). Score each cell for activity of specific gene programs --- curated lists of genes known to participate in interferon response, NF-kB inflammation, oxidative stress, AT2 self-renewal, AT2-to-AT1 differentiation, and apoptosis --- and ask whether these programs activate and deactivate in a biologically coherent order along pseudotime.
- **Expected biological insight:** A coherent ordering would suggest that alveolar failure is a staged process, not a sudden collapse, and would identify specific molecular programs that mark the transition from recoverable injury to irreversible failure.

### Aim 3: Test the robustness of the inferred failure landscape through ablation, sensitivity, and control analyses

- **Biological objective:** Determine whether the biological conclusions from Aims 1 and 2 are robust to changes in analytical choices, or whether they are artifacts of a particular method, gene set, or batch effect.
- **Computational/analytical approach:** Systematically repeat the core analyses while varying one component at a time (ablation studies --- see Section 9). Assess donor-level consistency, test alternative embedding and trajectory methods, remove specific gene programs, and check whether conclusions hold in cell-type subsets.
- **Expected biological insight:** If the core findings --- progressive displacement from homeostasis, ordered activation of stress and apoptosis programs, and evidence of stalled repair --- survive these perturbations, the biological interpretation is substantially strengthened. If specific findings are fragile, this identifies exactly which conclusions should be stated with caution.

---

## 6. Study Design

### Dataset and cohort structure

This project uses the Columbia University / NYP COVID-19 Lung Atlas (Single Cell Portal SCP1219), a publicly available single-nucleus RNA-seq dataset comprising 116,313 nuclei from human lung tissue. The cohort includes lungs from healthy donors (36,677 nuclei) and lungs from patients who died of COVID-19 (79,636 nuclei). The dataset was generated by the Bhatt, Bhatt, and Bhatt group at Columbia University and has been used in published work characterizing COVID-19 lung pathology at single-cell resolution.

### Which cells will be analyzed and why

The primary analysis will focus on alveolar epithelial cells --- specifically AT1, AT2, and any annotated transitional or aberrant epithelial populations. The atlas contains more than 20,000 of these cells, providing strong statistical power for trajectory and manifold analyses. We focus on alveolar epithelial cells because they are (a) the primary functional unit of gas exchange, (b) direct targets of SARS-CoV-2, (c) responsible for alveolar repair, and (d) the cell type whose failure most directly causes the fatal respiratory collapse in severe COVID-19. Other lung cell types (immune cells, endothelial cells, fibroblasts) are biologically important but are outside the scope of this project; they may be used in supplementary analyses for context.

### Comparison groups

The fundamental comparison is between alveolar epithelial cells from **healthy donors** (baseline homeostasis) and alveolar epithelial cells from **lethal COVID-19 patients** (extreme perturbation). Within the COVID group, we will look for internal structure --- whether some COVID cells remain near the healthy state while others are displaced far from it --- rather than treating all COVID cells as a single homogeneous group.

### How healthy and COVID cells will be used

Healthy cells serve as the **reference anchor**: they define what normal alveolar epithelial identity looks like in gene expression space. COVID cells are then examined relative to this anchor. In pseudotime analysis, the healthy homeostatic region will serve as the root (starting point), and the trajectory will be traced outward from there. This design treats the healthy state as the origin and asks how far and in what direction COVID cells have traveled.

### Cross-sectional, inferential, or pseudo-dynamic?

This is a **cross-sectional** study: all cells were collected at a single time point (time of death or organ donation). We cannot observe any individual cell changing over time. However, because the dataset captures cells at many different points along the injury spectrum, we can use **pseudo-dynamic inference** --- the logic that if cells at various stages of a process coexist in the tissue at the time of sampling, their gene expression patterns may recapitulate the order of that process. This is the same logic used in developmental biology when reconstructing differentiation trajectories from single-cell snapshots. We will be explicit throughout the project that pseudotime is an inference, not a direct measurement of elapsed time.

### What counts as evidence for "loss of robustness"

We operationally define loss of robustness as the following observable pattern in the data:

1. **Displacement from homeostasis:** COVID alveolar cells are, on average, farther from the centroid of the healthy cell distribution on the transcriptomic manifold than healthy cells are from each other.
2. **Increased dispersion:** COVID alveolar cells are more spread out (higher variance, lower density) than healthy cells, suggesting they have been scattered into diverse injury states rather than transitioning coherently to a single new state.
3. **Loss of canonical identity markers:** Along the inferred trajectory, canonical AT1 and AT2 marker genes decrease while stress, damage, and apoptosis markers increase.
4. **Ordered program activation:** Stress and repair programs activate before apoptosis programs along pseudotime, consistent with a staged failure process rather than random gene dysregulation.
5. **Stalled differentiation:** AT2 cells in the COVID group show partial activation of AT2-to-AT1 differentiation programs but fail to complete the transition, remaining in a transitional state.

No single piece of evidence is sufficient; the case for robustness collapse rests on the convergence of multiple lines of evidence.

---

## 7. Data Processing and Analysis Plan

This section walks through each major step of the analysis in order, explaining what each step does and why it matters biologically. Technical terms are defined as they arise.

### Step 1: Data acquisition and initial inspection

Download the expression matrix, cell-level metadata, and any available cell-type annotations from SCP1219. Inspect the metadata to understand how many donors are represented, which conditions are present, how cell types were annotated, and what quality metrics are available. This step is simply getting oriented: knowing what we have before we do anything to it.

### Step 2: Quality control (QC)

Single-nucleus RNA-seq captures the mRNA content of individual cell nuclei, but not every captured nucleus yields good data. Some "cells" in the dataset may actually be empty droplets, damaged nuclei, or doublets (two nuclei captured together, producing a blended profile that does not represent any real cell). Quality control removes these artifacts.

Concretely, we will filter nuclei based on:
- **Number of detected genes per nucleus:** Nuclei with very few genes detected are likely low-quality or empty; nuclei with extremely many genes detected may be doublets. We will set thresholds based on the distribution of gene counts in this specific dataset.
- **Total RNA counts per nucleus:** Similar logic --- too low suggests poor capture, too high suggests doublets.
- **Mitochondrial gene fraction:** A high percentage of mitochondrial RNA can indicate a damaged or dying cell whose cytoplasmic RNA has leaked out, leaving mitochondrial RNA overrepresented. (Note: in single-nucleus data, mitochondrial content behaves differently than in single-cell data, so thresholds must be set carefully.)

We will also remove genes detected in very few cells, as these provide little information and add noise.

### Step 3: Normalization

Different nuclei yield different total amounts of RNA, simply due to technical variation in capture and sequencing. Normalization adjusts for this so that we can fairly compare gene expression levels across cells. The standard approach is to scale each cell's counts to a common total (e.g., 10,000 counts), then apply a log transformation. The log transformation is important because gene expression data span many orders of magnitude, and without it, a few highly expressed genes would dominate all downstream analyses. After normalization, a gene's expression value roughly reflects its relative abundance in that cell, on a compressed scale.

### Step 4: Feature selection --- identifying highly variable genes

The human genome contains roughly 20,000 protein-coding genes, but most of them are either not expressed in alveolar cells or are expressed at constant levels across all cells (housekeeping genes). These uninformative genes add noise without helping us distinguish cell states. We will identify the top 2,000--3,000 **highly variable genes** (HVGs) --- genes whose expression varies meaningfully across cells --- and restrict subsequent analyses to these genes. This step focuses the analysis on the genes that actually differ between cell states.

### Step 5: Cell-type filtering and subsetting

Using the cell-type annotations provided with the atlas (and verifying them by checking expression of known marker genes), we will extract the alveolar epithelial population: AT1 cells (marked by genes such as *AGER*, *PDPN*, *CLIC5*), AT2 cells (marked by *SFTPC*, *SFTPA1*, *ABCA3*), and any annotated transitional or aberrant epithelial states. This gives us our working dataset: approximately 20,000+ alveolar epithelial nuclei from healthy and COVID lungs.

We will verify annotation quality by visualizing marker gene expression and confirming that annotated cell types express expected markers. If annotations appear noisy, we will re-cluster the epithelial subset and re-annotate based on canonical markers.

### Step 6: Batch and donor correction (if needed)

Cells from different donors were processed in different experimental batches, which can introduce technical variation that looks like biological signal. For example, all cells from one donor might shift slightly in gene expression space simply because they were processed on a different day. If uncorrected, this could cause us to misinterpret technical variation as biological injury states.

We will assess batch effects by visualizing cells colored by donor and batch. If donors or batches separate in ways that do not correspond to biology (e.g., two healthy donors occupy very different regions), we will apply batch correction using a method such as Harmony or scVI. These methods attempt to align cells from different batches while preserving genuine biological differences (like the difference between healthy and COVID). We will carefully check that correction does not erase real biological signal.

### Step 7: Dimensionality reduction

Each cell's gene expression profile lives in a space of ~2,000--3,000 dimensions (one per highly variable gene). We cannot visualize or easily analyze data in such a high-dimensional space. Dimensionality reduction compresses this information into a much smaller number of axes --- typically 30--50 principal components (PCs) first, and then 2--3 dimensions for visualization.

- **PCA (Principal Component Analysis):** Finds the axes of greatest variation in the data. The first few PCs capture the dominant patterns --- the main differences between cell types and cell states. We will use the top 30--50 PCs as input to all subsequent analyses.
- **UMAP (Uniform Manifold Approximation and Projection):** A visualization method that projects the 30--50 PC dimensions into 2 dimensions while trying to preserve the local neighborhood relationships between cells. On a UMAP plot, cells that are similar to each other appear nearby, and cells that are very different appear far apart. UMAP is useful for visualization and intuition but is not used for quantitative trajectory analysis because it can distort distances and create visual artifacts.
- **Diffusion maps (optional/comparative):** An alternative to UMAP that is specifically designed to capture continuous transitions and gradual changes in cell state. Diffusion maps model the data as if a particle were randomly walking between similar cells; regions connected by smooth transitions will be connected on the map. This property makes diffusion maps particularly well-suited for trajectory analysis. We will compare UMAP and diffusion map embeddings to see whether they tell a consistent story.

### Step 8: Manifold learning and embedding

The term **manifold** refers to the underlying shape or structure of the data in gene expression space. In biological terms, it is the set of cell states that actually exist in the tissue --- the terrain on which cells sit. Our dimensionality reduction and embedding steps are attempts to learn and visualize this manifold. The key biological idea is that cells do not randomly scatter across all possible gene expression combinations; they are constrained to a much smaller set of biologically accessible states, and these states form a continuous landscape.

After dimensionality reduction, we will construct a **nearest-neighbor graph** --- a network where each cell is connected to the cells most similar to it. This graph is a discrete approximation of the manifold and is the foundation for clustering, trajectory inference, and pseudotime analysis.

### Step 9: Trajectory inference and pseudotime

**Trajectory inference** is the process of finding continuous paths through the cell-state landscape. If cells progress from one state to another (e.g., from healthy to injured to apoptotic), trajectory inference aims to reconstruct the path and order the cells along it.

**Pseudotime** assigns each cell a numerical value representing its position along the inferred trajectory. A cell with pseudotime = 0 is at the beginning (we will set this to the healthy homeostatic state), and cells with higher pseudotime values are further along the inferred progression. Pseudotime is not real time; it is an ordering that reflects how much a cell's gene expression has changed relative to the starting point. It is useful because it lets us ask: as cells progress along this ordering, which genes turn on first? Which turn off? Do stress genes precede apoptosis genes?

We will use **diffusion pseudotime** (DPT) or a comparable method (e.g., Palantir, Monocle 3's principal graph) to infer trajectories. The choice of root cell (the starting point) is biologically motivated: we will root the trajectory in the densest region of healthy alveolar cells, representing homeostasis.

### Step 10: Gene program scoring

Rather than examining individual genes, we will score each cell for the activity of **gene programs** --- curated lists of genes that are known to participate in specific biological processes. This is analogous to asking: "Is this cell activating its stress response? Its apoptosis machinery? Its repair program?" rather than asking about one gene at a time.

Programs we will score include:
- **AT2 identity:** canonical AT2 marker genes (e.g., *SFTPC*, *SFTPA1*, *LAMP3*)
- **AT1 identity:** canonical AT1 marker genes (e.g., *AGER*, *PDPN*, *HOPX*)
- **Interferon response:** genes induced by type I and type II interferons (ISGs), reflecting antiviral signaling
- **NF-kB / inflammatory signaling:** genes in the NF-kB pathway, reflecting pro-inflammatory activation
- **Oxidative stress:** genes involved in the response to reactive oxygen species
- **AT2-to-AT1 differentiation:** genes associated with the transitional state during alveolar repair (e.g., *KRT8*, *CLDN4*, *SFN*)
- **Apoptosis:** pro-apoptotic genes (e.g., from the Hallmark Apoptosis gene set or manually curated sets including *BAX*, *CASP3*, *BCL2L11*)
- **Senescence / cell cycle arrest:** genes associated with cellular senescence, which may mark cells that have exited the cell cycle permanently

Scoring will use a method like Scanpy's `score_genes` or AUCell, which estimates the extent to which a gene program is active in each cell relative to a background of randomly selected genes.

### Step 11: Differential expression and trend analysis along pseudotime

We will identify genes whose expression changes significantly along pseudotime using generalized additive models (GAMs) or similar methods. This asks: which genes systematically increase or decrease as cells move from homeostasis toward failure? We will look for patterns such as:
- Early activation of interferon and stress-response genes
- Mid-trajectory activation of repair and differentiation genes
- Late activation of apoptosis genes with simultaneous loss of AT2/AT1 identity markers

This analysis provides the gene-level detail underlying the program-level scores.

### Step 12: Robustness and dispersion metrics

To quantify loss of robustness, we will compute:
- **Centroid distance:** The average distance of COVID cells from the centroid (center of mass) of the healthy cell distribution, compared to the average distance of healthy cells from their own centroid. Greater displacement of COVID cells indicates loss of homeostatic positioning.
- **Dispersion (variance):** The spread of COVID cells relative to healthy cells. Higher dispersion among COVID cells suggests fragmentation into diverse injury states.
- **Nearest-neighbor condition mixing:** For each cell, the fraction of its nearest neighbors that come from the same condition (healthy or COVID). If healthy and COVID cells occupy distinct regions, this score will be high; overlap would indicate that some COVID cells remain near the healthy state.
- **Density along pseudotime:** Whether COVID cells are uniformly distributed along pseudotime or enriched at specific positions (e.g., late pseudotime corresponding to apoptosis).

---

## 8. Main Experiments / Analyses

### Experiment 1: Identification and validation of alveolar epithelial populations

- **Purpose:** Isolate the cell populations central to this study and confirm their identity.
- **Input data:** Full atlas (116,313 cells) with metadata and annotations.
- **Method:** Subset cells annotated as AT1, AT2, and transitional/aberrant epithelial. Verify annotations by plotting expression of canonical markers (*SFTPC*, *AGER*, *HOPX*, *LAMP3*, *KRT8*). Re-annotate if necessary using leiden clustering on the epithelial subset.
- **Expected result:** A clean, well-annotated set of 20,000+ alveolar epithelial cells with confident AT1, AT2, and transitional labels.
- **Biological interpretation:** Establishes the cellular foundation for all subsequent analyses and confirms that the dataset contains sufficient representation of the cell types we need.

### Experiment 2: Construction of the alveolar epithelial manifold and condition-level comparison

- **Purpose:** Build the transcriptomic landscape of alveolar cell states and determine how healthy and COVID cells are distributed on it.
- **Input data:** QC-filtered, normalized alveolar epithelial cells.
- **Method:** PCA, nearest-neighbor graph construction, UMAP embedding. Color cells by condition (healthy vs. COVID), cell type (AT1, AT2, transitional), and donor. Compute centroid distance and dispersion metrics.
- **Expected result:** Healthy cells form a compact cluster; COVID cells extend outward from it, occupying regions not populated by healthy cells. Some COVID cells may remain near the healthy cluster (less injured), while others are far away (severely altered).
- **Biological interpretation:** The spatial distribution of cells on the manifold directly visualizes the degree of displacement from homeostasis. If COVID cells form a gradient rather than a separate island, this supports the hypothesis of progressive rather than binary state change.

### Experiment 3: Pseudotime trajectory reconstruction from homeostasis through injury to apoptosis

- **Purpose:** Infer a continuous ordering of cells from healthy to maximally injured/apoptotic.
- **Input data:** Alveolar epithelial cells with diffusion map or PCA-based representations.
- **Method:** Diffusion pseudotime (DPT) or Palantir, rooted in the densest region of healthy AT2 cells. Assess whether trajectories branch (e.g., toward successful differentiation vs. toward apoptosis).
- **Expected result:** A pseudotime axis along which cells are ordered, with healthy cells at the beginning and apoptotic/exhausted COVID cells at the end. Possible branching toward a transitional/repair state and toward a terminal failure state.
- **Biological interpretation:** The inferred trajectory represents the computational reconstruction of a plausible biological process: the sequence of molecular events as alveolar cells move from health toward death. The existence of branches would suggest that cells face a decision point --- some attempt repair, others commit to apoptosis --- which is biologically consistent with known lung injury biology.

### Experiment 4: Gene program scoring along pseudotime

- **Purpose:** Determine whether stress, repair, and apoptosis programs activate in a biologically coherent order.
- **Input data:** Pseudotime-ordered cells; curated gene program lists.
- **Method:** Score each cell for each gene program. Plot program scores as a function of pseudotime using smoothed trend lines (e.g., LOESS or GAM fits). Test whether program activation order matches biological expectation.
- **Expected result:** Interferon and stress programs peak early in pseudotime. AT2-to-AT1 differentiation markers appear at intermediate pseudotime. Apoptosis scores increase at late pseudotime. AT2 and AT1 identity scores decline progressively.
- **Biological interpretation:** An ordered cascade --- stress before repair attempt before apoptosis --- is consistent with a staged failure model. If apoptosis genes activate simultaneously with stress genes (no lag), the process may be more catastrophic than staged. The data will tell us which model better fits.

### Experiment 5: Quantification of homeostatic displacement and dispersion

- **Purpose:** Provide quantitative, statistical evidence that COVID cells are displaced from and more dispersed than healthy cells.
- **Input data:** Manifold coordinates (PCA or diffusion map space) for all alveolar epithelial cells.
- **Method:** Compute per-cell distance from the healthy centroid. Compare distributions between healthy and COVID cells using statistical tests (e.g., Mann-Whitney U test). Compute variance/dispersion within each group. Perform this analysis separately for AT1 and AT2 cells.
- **Expected result:** COVID cells are significantly farther from the healthy centroid (p << 0.01) and show significantly greater dispersion. The effect may be larger in AT2 cells than AT1 cells, given AT2's dual role as both a viral target and the progenitor responsible for repair.
- **Biological interpretation:** Quantitative confirmation that COVID-19 does not merely shift alveolar cells to a new stable state but instead disperses them across a wide range of abnormal states --- a hallmark of robustness collapse.

### Experiment 6: Identification of transitional and failed-repair states

- **Purpose:** Determine whether intermediate cell states exist between healthy and apoptotic, and whether these states show evidence of stalled repair.
- **Input data:** Pseudotime-ordered cells, gene expression data.
- **Method:** Examine cells at intermediate pseudotime for co-expression of AT2 markers and AT1 markers (suggesting active differentiation) alongside stress markers (suggesting injury). Look for cells expressing *KRT8*, *CLDN4*, *SFN* --- markers associated with the transitional AT2-to-AT1 state described in lung injury literature. Check whether these cells are enriched in the COVID group.
- **Expected result:** A population of cells at intermediate pseudotime co-expressing AT2 markers, partial AT1 markers, and stress/damage markers. These cells are predominantly from COVID donors.
- **Biological interpretation:** These cells likely represent AT2 cells that initiated the differentiation program in response to AT1 loss but were unable to complete it --- a cellular state sometimes called "transitional" or "damage-associated." Their existence in lethal COVID-19 would suggest that repair was attempted but failed, contributing to the loss of functional alveolar epithelium.

### Experiment 7: Donor-level analysis of trajectory enrichment

- **Purpose:** Determine whether the trajectory findings are consistent across donors or driven by one or two outlier patients.
- **Input data:** Pseudotime values and donor identifiers.
- **Method:** For each donor, compute the distribution of pseudotime values among their alveolar cells. Compare across donors within each condition. Test whether all COVID donors are shifted to higher pseudotime relative to all healthy donors, or whether the effect is driven by specific donors.
- **Expected result:** All or most COVID donors show a shift toward higher pseudotime, though the magnitude may vary (reflecting different stages or severity of disease at time of death).
- **Biological interpretation:** Donor-level consistency strengthens the conclusion that the observed trajectory reflects a general biological process of COVID-19-induced alveolar failure, not an idiosyncrasy of one patient's biology or tissue processing.

---

## 9. Ablation and Sensitivity Analyses

### What is an ablation study, and why does it matter?

In experimental biology, a classic strategy for testing whether a factor is important is to remove it and see what happens --- knock out a gene, block a receptor, remove a cell type. Ablation studies in computational biology follow the same logic: we remove one analytical choice, gene set, or data subset at a time and ask whether the biological conclusions still hold. If a finding survives many ablations, we can be more confident that it reflects genuine biology rather than an artifact of one particular analytical decision. If it collapses when a specific component is removed, that tells us exactly where the conclusion is fragile and requires caution.

This section describes the ablation and sensitivity analyses we will perform, along with the rationale for each.

### Ablation 1: AT2 cells only vs. AT1 + AT2 together

- **What is being changed:** Analyze only AT2 cells, excluding AT1 and transitional cells.
- **Why it matters:** AT1 and AT2 cells have very different transcriptomic profiles. Including both in the same manifold could create structure that reflects cell-type differences rather than injury-state differences. By analyzing AT2 cells alone, we test whether the injury trajectory is visible within a single cell type, not just between cell types.
- **What outcome increases confidence:** If the pseudotime trajectory and gene program ordering are preserved in the AT2-only analysis (with healthy AT2 cells at one end and apoptotic COVID AT2 cells at the other), the findings are unlikely to be driven by AT1-vs-AT2 compositional differences.

### Ablation 2: PCA/UMAP embedding vs. diffusion-based embedding

- **What is being changed:** Replace the diffusion map embedding with standard PCA/UMAP, or vice versa.
- **Why it matters:** Different embedding methods make different mathematical assumptions about the data. UMAP emphasizes local neighborhood preservation but can distort global structure. Diffusion maps emphasize smooth transitions but may be less sensitive to rare populations. If the trajectory looks coherent under both methods, it is less likely to be an artifact of one method's assumptions.
- **What outcome increases confidence:** The broad structure --- healthy cells at one end, a progression through stress and repair, apoptotic cells at the other end --- should be qualitatively preserved regardless of embedding method, even if the exact shape of the manifold changes.

### Ablation 3: With and without donor/batch correction

- **What is being changed:** Run the full analysis twice: once with batch correction applied and once without.
- **Why it matters:** Batch correction is a powerful but potentially aggressive step. Under-correction leaves technical artifacts in the data that could masquerade as biological signal. Over-correction can remove genuine biological variation, especially if disease state is partially confounded with batch. Comparing results with and without correction reveals whether the trajectory is driven by biology or by batch effects.
- **What outcome increases confidence:** If the same trajectory and the same gene program ordering appear regardless of whether batch correction is applied, the findings are robust to this analytical choice. If the trajectory disappears after batch correction, it may have been a batch artifact; if it only appears after batch correction, the correction may have created the signal.

### Ablation 4: With and without apoptosis gene sets

- **What is being changed:** Remove apoptosis-related genes from the highly variable gene list before constructing the manifold and trajectory.
- **Why it matters:** If the entire trajectory is organized by apoptosis genes, then removing them should disrupt it. But if the trajectory reflects a broader process of cell-state change (of which apoptosis is just one component), it should persist even without apoptosis genes, with the remaining signal carried by stress, repair, and identity genes.
- **What outcome increases confidence:** The trajectory is preserved (perhaps with reduced resolution at the late/apoptotic end), and the ordered activation of non-apoptotic programs (interferon, stress, repair) is still visible. This would confirm that the trajectory captures a multi-faceted biological process, not just a gradient of cell death.

### Ablation 5: Different root cells for pseudotime

- **What is being changed:** Root pseudotime in different starting cells: (a) the default healthy AT2 centroid, (b) a healthy AT1 cell, (c) a randomly chosen healthy cell, (d) a COVID cell at the opposite extreme.
- **Why it matters:** Pseudotime algorithms can produce very different orderings depending on where they start. If the biological interpretation (stress before repair before apoptosis) is robust to root choice, it is more likely to reflect genuine trajectory structure rather than a mathematical artifact of starting-point selection.
- **What outcome increases confidence:** Regardless of root cell choice (within the healthy population), COVID cells are consistently assigned higher pseudotime values, and gene program ordering is preserved. If rooting in a COVID cell reverses the ordering in a biologically sensible way (apoptosis first, homeostasis last), this provides further validation.

### Ablation 6: Alveolar cells only vs. including neighboring epithelial populations

- **What is being changed:** Expand the analysis to include airway epithelial cells (club cells, ciliated cells, basal cells) alongside alveolar cells, and see whether the alveolar trajectory is preserved or distorted.
- **Why it matters:** In severe lung injury, metaplastic processes can occur where airway-like cells appear in the alveolar compartment. Including neighboring populations tests whether the alveolar injury trajectory is specific to alveolar cells or is part of a broader epithelial response. It also tests whether the manifold structure is stable when the cellular context changes.
- **What outcome increases confidence:** The alveolar-specific trajectory (homeostasis to injury to apoptosis) remains visible as a distinct branch or region, not subsumed into a broader epithelial manifold. The gene program ordering along the alveolar trajectory is unchanged.

### Ablation 7: Leave-one-donor-out analysis

- **What is being changed:** Systematically remove one donor at a time and rerun the trajectory analysis.
- **Why it matters:** If a single donor contributes a disproportionate number of cells at a critical point in the trajectory, the entire finding could be an artifact of that donor's unusual biology or tissue quality. Leave-one-donor-out analysis is the single-cell equivalent of checking that a clinical finding is not driven by one outlier patient.
- **What outcome increases confidence:** The trajectory and gene program ordering are qualitatively preserved in every leave-one-donor-out iteration. If removing one donor substantially changes the result, that donor should be investigated for quality issues or unusual clinical features.

---

## 10. Controls and Validation

### Biological controls

- **Marker gene validation:** For every cell-type label used in this study, confirm that canonical marker genes are appropriately expressed. AT2 cells should express *SFTPC* and not *AGER*; AT1 cells should express *AGER* and not *SFTPC*. If labels and markers disagree, the labels cannot be trusted.
- **Known biology benchmarks:** The AT2-to-AT1 differentiation trajectory is well-characterized in mouse studies and in human lung injury. Our inferred trajectory should recover known features of this process (e.g., upregulation of *KRT8* in transitional cells, progressive loss of AT2 surfactant genes, gain of AT1 flatness-related genes). If our trajectory contradicts known biology, something is likely wrong with the analysis.
- **Apoptosis-positive cells should score high on apoptosis programs:** This is a basic sanity check --- cells expressing known apoptosis markers (e.g., *CASP3*, *BAX*) should have high apoptosis program scores. If not, the scoring method needs to be recalibrated.
- **Healthy cells should not score high on injury programs:** If healthy alveolar cells show high interferon or apoptosis scores, it may indicate a technical artifact (e.g., ambient RNA contamination) or a scoring problem.

### Analytical controls

- **Donor-level consistency** (described in Experiment 7): Results should not be driven by one donor.
- **Permutation controls for pseudotime:** Randomly shuffle condition labels (healthy vs. COVID) across cells and recompute pseudotime enrichment. If the real data show significantly different pseudotime enrichment compared to permuted data, the condition-pseudotime association is unlikely to be due to chance.
- **Random gene set controls for program scoring:** Score cells using randomly selected gene sets of the same size as the curated programs. The real program scores should be more structured (showing stronger trends along pseudotime) than random gene set scores.
- **Embedding stability:** Rerun UMAP with different random seeds. The large-scale structure (relative positions of healthy vs. COVID cells, AT1 vs. AT2) should be stable; small-scale features that change across runs should not be over-interpreted.
- **Comparison to published findings:** Where possible, compare our results to published analyses of this same dataset or similar COVID-19 lung atlases. Agreement with independent analyses strengthens confidence; disagreement should be investigated.

---

## 11. Expected Results

The following are realistic expectations based on the known biology of COVID-19 lung injury and prior single-cell studies. They are stated as likely outcomes, not guaranteed findings.

**Healthy alveolar cells will occupy a compact, coherent region of the transcriptomic manifold.** AT1 and AT2 cells from healthy donors should form well-separated but internally tight clusters, reflecting stable homeostatic identities. Within each cell type, expression variance should be low, consistent with cells performing their normal functions in a non-injured lung.

**COVID-19 alveolar cells will be displaced from the healthy region and dispersed across the manifold.** Rather than forming a single new cluster, COVID cells are expected to spread outward from the healthy region in multiple directions, reflecting the heterogeneity of cellular responses to injury. Some COVID cells may remain near the healthy cluster (mildly affected), while others will be far removed (severely altered).

**Pseudotime analysis will reveal an ordered progression from homeostasis through injury to apoptosis.** The trajectory is expected to show a coherent sequence: first, activation of interferon-stimulated genes (reflecting antiviral response); then, upregulation of NF-kB and inflammatory signaling; followed by activation of stress-response and damage-associated genes; then partial activation of repair/differentiation programs; and finally, upregulation of apoptosis-related genes with concomitant loss of AT2 and AT1 identity markers.

**Transitional or failed-repair states will be identifiable.** A subset of cells at intermediate pseudotime are expected to show mixed expression of AT2 markers, partial AT1 markers, and stress markers --- consistent with AT2 cells that began differentiating toward AT1 fate in response to injury but failed to complete the transition. These cells likely correspond to the "aberrant basaloid" or "damage-associated transient progenitor" (DATP) states described in the recent lung injury literature.

**The findings will be broadly robust to ablation.** Core conclusions --- progressive displacement, ordered program activation, existence of transitional states --- are expected to survive most ablations, though specific details (exact pseudotime values, minor trajectory branches) may vary. If any finding is fragile, it will be identified and reported transparently.

---

## 12. Potential Pitfalls and Alternative Strategies

### Pitfall 1: Noisy or inconsistent cell-type annotations

- **Problem:** If the original atlas annotations are inaccurate, downstream analyses will be contaminated by non-alveolar cells.
- **Mitigation:** Independently validate all annotations using canonical marker genes. Re-cluster and re-annotate the epithelial subset if needed. Use a conservative approach: only include cells with unambiguous marker expression.

### Pitfall 2: Donor effects dominating the manifold

- **Problem:** If inter-donor variability is large relative to injury-state variability, the manifold may organize by donor rather than by biology.
- **Mitigation:** Apply batch correction (Harmony or scVI) and verify that the resulting manifold organizes by cell state rather than donor. Perform leave-one-donor-out analyses. If donor effects remain dominant, restrict the analysis to a matched subset of donors with similar processing.

### Pitfall 3: Weak or ambiguous trajectory signal

- **Problem:** If alveolar cell states are not arranged in a clear trajectory (e.g., they form discrete clusters with no bridging cells), pseudotime analysis will produce arbitrary orderings.
- **Mitigation:** Before interpreting pseudotime, check whether the nearest-neighbor graph is connected and whether cells form a continuous distribution. If not, switch from trajectory analysis to a cluster-based analysis with explicit pairwise comparisons (e.g., "homeostatic" vs. "stressed" vs. "apoptotic" clusters), which is less elegant but more honest.

### Pitfall 4: Over-interpretation of pseudotime

- **Problem:** Pseudotime is an inference from cross-sectional data. It does not prove that cells actually traverse the inferred path or that the process occurs in the inferred order in vivo.
- **Mitigation:** State this limitation explicitly in all interpretations. Frame pseudotime results as "consistent with" a progressive process, not as proof of one. Use gene program ordering as a plausibility check: if the order matches known biology, the inference is more trustworthy; if it contradicts known biology, the pseudotime ordering may be wrong.

### Pitfall 5: Difficulty separating apoptosis from general stress

- **Problem:** Many genes associated with apoptosis are also induced by stress, making it hard to distinguish cells that are truly committed to dying from cells that are stressed but potentially recoverable.
- **Mitigation:** Use multiple apoptosis gene sets (curated from different sources) and compare them to general stress gene sets. Look for cells that score high on apoptosis but low on stress, and vice versa, to assess whether these are separable states. If they are not, acknowledge this limitation and describe the combined state as "stress/apoptosis."

### Pitfall 6: Inability to prove true temporal dynamics from cross-sectional data

- **Problem:** All cells were collected at a single time point (death or organ donation). We cannot observe individual cells changing over time.
- **Mitigation:** This is a fundamental limitation of the study design, not a fixable problem. We can generate hypotheses about temporal dynamics but not prove them. The appropriate language throughout the project is "the data are consistent with," "the inferred ordering suggests," and "future time-course studies could test whether." Acknowledging this limitation is not a weakness --- it is a sign of scientific maturity.

---

## 13. Biological Significance

This project matters because it addresses a question that lies at the heart of lung injury biology: how does the alveolar epithelium --- the tissue responsible for every breath we take --- fail under extreme stress? The answer is not simply that cells die. The answer, as this project aims to show, is that cells pass through a series of intermediate states in which normal identity erodes, repair programs are activated but cannot be completed, and the system progressively loses its ability to maintain function. This process --- what we call robustness collapse --- is not unique to COVID-19. Diffuse alveolar damage occurs in many forms of acute lung injury, including bacterial pneumonia, aspiration, and ventilator-induced injury. By characterizing the transcriptomic landscape of alveolar failure in the extreme case of lethal COVID-19, we establish a framework that could be applied to other forms of lung injury and, more broadly, to any tissue system in which homeostatic robustness is challenged by disease.

The concept of robustness is central to systems biology. A robust system is one that maintains its function despite perturbation. The alveolar epithelium is robust to minor insults --- small injuries heal, AT2 cells replace lost AT1 cells, and the tissue returns to its baseline state. But beyond some threshold of perturbation, this robustness breaks down. Understanding where that threshold lies, what molecular programs are active at the breaking point, and whether there are identifiable intermediate states where intervention might still be effective is a question with both basic and translational significance. This project will not answer all of these questions, but it will provide a rigorous, data-driven map of the failure landscape that future studies --- both computational and experimental --- can build upon.

---

## 14. Deliverables for a Graduate Class Project

1. **Final written report** (15--25 pages): A complete project report structured as an abbreviated research paper, including introduction, methods, results, discussion, and references. Written for a biology-facing audience with all computational methods explained in accessible language.

2. **Main figures** (5--7 figures): Publication-quality figures covering the manifold, trajectory, gene program dynamics, and key ablation results (see Section 15).

3. **Supplementary tables:**
   - Table S1: Gene lists for all scored gene programs (with sources)
   - Table S2: QC metrics and filtering thresholds
   - Table S3: Top differentially expressed genes along pseudotime
   - Table S4: Summary statistics for donor-level analyses

4. **Analysis notebook / pipeline:** A well-documented Jupyter notebook (or set of Python scripts) that reproduces all analyses from raw counts to final figures. Code should be organized, commented, and runnable from the virtual environment (`lesegenv`).

5. **Oral presentation** (15--20 minutes): A slide-based presentation summarizing the project's motivation, approach, key findings, ablation results, and biological conclusions. Targeted at a mixed audience of biologists and computational scientists.

---

## 15. Suggested Figures

**Figure 1: UMAP embedding of the alveolar epithelial manifold, colored by condition and cell type.**
Shows the overall landscape of alveolar cell states, with healthy cells in a compact region and COVID cells extending outward, providing the visual foundation for the entire project.

**Figure 2: Pseudotime trajectory overlaid on the manifold, colored by inferred pseudotime value.**
Illustrates the continuous ordering from homeostasis (low pseudotime, blue) to failure (high pseudotime, red), with trajectory paths marked, showing whether cells progress smoothly or branch.

**Figure 3: Gene program scores as a function of pseudotime (multi-panel ribbon or heatmap).**
Displays the sequential activation and deactivation of interferon, stress, repair, identity, and apoptosis programs along the trajectory, revealing the temporal order of molecular events during alveolar failure.

**Figure 4: Density distribution of healthy vs. COVID cells along pseudotime.**
A split violin or ridge plot showing that healthy cells are concentrated at low pseudotime while COVID cells are shifted toward and spread across higher pseudotime values, quantifying the displacement from homeostasis.

**Figure 5: Marker gene expression along pseudotime (selected key genes).**
Line plots or heatmaps showing the behavior of individual genes (*SFTPC*, *AGER*, *KRT8*, *ISG15*, *CASP3*, *BAX*) along pseudotime, grounding the program-level analysis in specific molecular readouts.

**Figure 6: Ablation summary panel.**
A compact multi-panel figure comparing the core trajectory finding (e.g., pseudotime distribution of COVID vs. healthy cells) across key ablations: AT2-only, no batch correction, PCA-only, apoptosis genes removed. Demonstrates robustness or identifies fragility.

**Figure 7: Donor-level consistency analysis.**
Boxplots or violin plots showing the distribution of pseudotime values per donor, stratified by condition, confirming that the trajectory shift is not driven by one outlier donor.

---

## 16. Feasible Timeline

| Week | Activities |
|------|-----------|
| **Week 1** | Download and inspect the SCP1219 dataset. Perform quality control filtering. Normalize and identify highly variable genes. Verify cell-type annotations with marker genes. Set up the analysis environment and notebook structure. |
| **Week 2** | Subset alveolar epithelial cells (AT1, AT2, transitional). Assess and correct for batch/donor effects if needed. Perform dimensionality reduction (PCA, UMAP, diffusion maps). Construct the alveolar manifold. Generate initial visualizations of healthy vs. COVID cell distributions. |
| **Week 3** | Run trajectory inference and pseudotime analysis. Score cells for gene programs (interferon, stress, repair, apoptosis, identity). Analyze gene program dynamics along pseudotime. Compute robustness/dispersion metrics. Identify transitional and failed-repair states. |
| **Week 4** | Perform all ablation and sensitivity analyses (AT2-only, embedding comparison, batch correction on/off, apoptosis gene removal, root cell sensitivity, leave-one-donor-out). Run permutation controls. Compile ablation results. |
| **Week 5** | Generate all main and supplementary figures. Write the results and methods sections of the report. Draft figure legends. Begin the introduction and discussion. |
| **Week 6** | Complete the written report (introduction, discussion, abstract). Prepare the oral presentation slides. Clean and document the analysis notebook/pipeline. Revise all figures for clarity and consistency. Final review and submission. |

---

## 17. Final Project Summary

This project uses single-nucleus RNA-seq data from the Columbia/NYP COVID-19 Lung Atlas to investigate how alveolar epithelial cells --- the cells responsible for gas exchange in the human lung --- lose their functional identity and robustness under lethal SARS-CoV-2 infection. Rather than treating healthy and COVID-19 cells as two discrete categories, we construct a continuous transcriptomic landscape of alveolar cell states and use trajectory inference to ask whether cells move through an ordered progression from homeostasis through interferon activation, inflammatory stress, attempted but failed repair, and ultimately apoptosis. By scoring cells for curated gene programs at each point along this trajectory, we aim to reconstruct the molecular sequence of alveolar failure and identify intermediate states where repair stalls. Systematic ablation analyses --- varying the cell types included, the embedding methods used, the gene sets considered, and the donors analyzed --- test whether the biological conclusions are robust or fragile. The result is a rigorous, biology-centered analysis of how the alveolar epithelial system collapses under extreme perturbation, with implications for understanding lung injury, tissue robustness, and the limits of epithelial repair.

---

*Project plan prepared for a graduate-level computational biology / systems biology course.*
*Dataset: Columbia University / NYP COVID-19 Lung Atlas, SCP1219.*

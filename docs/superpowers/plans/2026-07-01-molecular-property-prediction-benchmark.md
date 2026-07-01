# Molecular Property Prediction Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible molecular property prediction benchmark comparing classical ML and MLP models across random and scaffold-aware splits on ESOL and FreeSolv.

**Architecture:** The project is a small research pipeline organized around data loading, featurization, splitting, modeling, evaluation, and analysis. MVP work focuses on CSV datasets, RDKit descriptors, Morgan fingerprints, random/scaffold splits, RF/XGBoost/Ridge/MLP models, and exported benchmark tables/figures.

**Tech Stack:** Python, pandas, numpy, RDKit, scikit-learn, XGBoost, PyTorch, matplotlib, seaborn, pytest, Jupyter.

---

## Phase 0: Repository Foundation

### Task 0.1: Create Project Skeleton

**Files:**
- Create: `README.md`
- Create: `requirements.txt`
- Create: `src/__init__.py`
- Create: `data/raw/.gitkeep`
- Create: `data/processed/.gitkeep`
- Create: `results/figures/.gitkeep`
- Create: `notebooks/.gitkeep`
- Create: `tests/.gitkeep`

- [ ] Create directories: `src`, `data/raw`, `data/processed`, `results/figures`, `notebooks`, `tests`.
- [ ] Add minimal package markers and `.gitkeep` files.
- [ ] Add dependencies: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `torch`, `rdkit`, `matplotlib`, `seaborn`, `umap-learn`, `shap`, `pytest`, `jupyter`.
- [ ] Commit: `chore: initialize project structure`.

**Acceptance Criteria:**
- `python -m pytest` runs without import errors.
- Repository layout matches the PRD section 7.

---

## Phase 1: Data Loading And Cleaning

### Task 1.1: Dataset Configuration

**Files:**
- Create: `src/config.py`
- Test: `tests/test_config.py`

- [ ] Define dataset metadata for `esol` and `freesolv`: dataset name, raw CSV path, processed CSV path, SMILES column, target column, and task type.
- [ ] Add tests that assert both MVP datasets are registered and have `regression` task type.
- [ ] Commit: `feat: add dataset configuration`.

**Acceptance Criteria:**
- `pytest tests/test_config.py -v` passes.
- ESOL and FreeSolv can be referenced by stable keys: `esol`, `freesolv`.

### Task 1.2: Load And Normalize CSV Data

**Files:**
- Create: `src/data_loader.py`
- Test: `tests/test_data_loader.py`

- [ ] Implement `load_raw_dataset(dataset_key: str) -> pandas.DataFrame`.
- [ ] Implement `normalize_dataset(df, smiles_col, target_col) -> pandas.DataFrame` returning exactly `smiles` and `target`.
- [ ] Drop rows with missing SMILES or target values.
- [ ] Add small fixture-style tests using in-memory DataFrames.
- [ ] Commit: `feat: add raw dataset loading`.

**Acceptance Criteria:**
- Returned DataFrame columns are exactly `smiles,target`.
- Missing SMILES or target rows are removed deterministically.

### Task 1.3: Validate SMILES With RDKit

**Files:**
- Modify: `src/data_loader.py`
- Test: `tests/test_data_loader.py`

- [ ] Implement `validate_smiles(df) -> tuple[pandas.DataFrame, pandas.DataFrame]`.
- [ ] Parse SMILES with `Chem.MolFromSmiles`.
- [ ] Return valid rows and invalid rows separately.
- [ ] Add tests with valid examples like `CCO` and invalid examples like `not_a_smiles`.
- [ ] Commit: `feat: validate smiles during preprocessing`.

**Acceptance Criteria:**
- Invalid molecules are excluded from processed data.
- Invalid rows can be logged or inspected later.

### Task 1.4: Save Processed Data

**Files:**
- Modify: `src/data_loader.py`
- Create: `scripts/preprocess_data.py`
- Test: `tests/test_data_loader.py`

- [ ] Implement `save_processed_dataset(dataset_key, df)`.
- [ ] Add CLI script accepting `--dataset esol` and `--dataset freesolv`.
- [ ] Save cleaned data to `data/processed/<dataset>.csv`.
- [ ] Commit: `feat: add preprocessing script`.

**Acceptance Criteria:**
- Running `python scripts/preprocess_data.py --dataset esol` writes `data/processed/esol.csv`.
- Processed CSV contains only `smiles,target`.

---

## Phase 2: Exploratory Data Analysis

### Task 2.1: Molecular Summary Statistics

**Files:**
- Create: `src/eda.py`
- Test: `tests/test_eda.py`

- [ ] Implement RDKit-derived summary columns: molecular weight, heavy atom count, atom count, ring count.
- [ ] Implement `target_summary(df)` returning count, mean, std, min, max.
- [ ] Add tests for non-empty summaries.
- [ ] Commit: `feat: add eda summary utilities`.

**Acceptance Criteria:**
- EDA functions run on cleaned ESOL and FreeSolv data.
- Summary outputs are plain DataFrames suitable for notebooks.

### Task 2.2: EDA Notebook

**Files:**
- Create: `notebooks/01_eda.ipynb`
- Output: `results/figures/esol_target_distribution.png`
- Output: `results/figures/freesolv_target_distribution.png`

- [ ] Load processed ESOL and FreeSolv.
- [ ] Plot molecular weight distribution.
- [ ] Plot atom count distribution.
- [ ] Plot target distribution.
- [ ] Save figures to `results/figures`.
- [ ] Commit: `docs: add eda notebook`.

**Acceptance Criteria:**
- Notebook can be run top-to-bottom.
- Figures exist for both MVP datasets.

---

## Phase 3: Featurization

### Task 3.1: RDKit Descriptor Features

**Files:**
- Create: `src/featurize.py`
- Test: `tests/test_featurize.py`

- [ ] Implement `compute_descriptors(smiles_list) -> pandas.DataFrame`.
- [ ] Include 20-30 descriptors covering molecular weight, LogP, TPSA, HBD, HBA, rotatable bonds, ring counts, aromatic rings, formal charge, fraction Csp3, and molar refractivity.
- [ ] Return one row per input SMILES.
- [ ] Add tests asserting numeric, finite descriptor values for `CCO`, `c1ccccc1`, and `CC(=O)O`.
- [ ] Commit: `feat: add rdkit descriptor featurizer`.

**Acceptance Criteria:**
- Descriptor DataFrame has stable column names.
- Invalid SMILES are not silently featurized.

### Task 3.2: Morgan Fingerprints

**Files:**
- Modify: `src/featurize.py`
- Test: `tests/test_featurize.py`

- [ ] Implement `compute_morgan_fingerprints(smiles_list, radius=2, n_bits=2048) -> numpy.ndarray`.
- [ ] Add tests for output shape and binary values.
- [ ] Add options for `n_bits=512`, `1024`, and `2048`.
- [ ] Commit: `feat: add morgan fingerprint featurizer`.

**Acceptance Criteria:**
- Fingerprint arrays have shape `(n_molecules, n_bits)`.
- Values are only `0` or `1`.

### Task 3.3: Feature Matrix Builder

**Files:**
- Modify: `src/featurize.py`
- Test: `tests/test_featurize.py`

- [ ] Implement `build_feature_matrix(df, feature_type)` with feature types `descriptors`, `fingerprints`, and `combined`.
- [ ] Standardize descriptors with `StandardScaler` inside training workflows only, not globally before splitting.
- [ ] Return feature matrix and feature names.
- [ ] Commit: `feat: add feature matrix builder`.

**Acceptance Criteria:**
- Descriptor, fingerprint, and combined feature modes are supported.
- Scaling is fit only on train data in model pipelines.

---

## Phase 4: Data Splitting

### Task 4.1: Random Split

**Files:**
- Create: `src/splits.py`
- Test: `tests/test_splits.py`

- [ ] Implement `random_split(df, train_size=0.8, val_size=0.1, test_size=0.1, seed=42)`.
- [ ] Return train, validation, and test index arrays.
- [ ] Add tests for deterministic output and non-overlapping indices.
- [ ] Commit: `feat: add random train validation test split`.

**Acceptance Criteria:**
- Splits cover all rows exactly once.
- Same seed produces same split.

### Task 4.2: Bemis-Murcko Scaffold Split

**Files:**
- Modify: `src/splits.py`
- Test: `tests/test_splits.py`

- [ ] Implement `compute_scaffold(smiles) -> str` using RDKit Bemis-Murcko scaffolds.
- [ ] Implement `scaffold_split(df, train_size=0.8, val_size=0.1, test_size=0.1, seed=42)`.
- [ ] Ensure molecules with the same scaffold never cross train/validation/test.
- [ ] Add tests with duplicated scaffolds.
- [ ] Commit: `feat: add scaffold-aware split`.

**Acceptance Criteria:**
- No scaffold appears in more than one split.
- Split sizes are close to requested ratios and reported explicitly.

### Task 4.3: Split Diagnostics

**Files:**
- Modify: `src/splits.py`
- Create: `src/visualize.py`
- Test: `tests/test_splits.py`

- [ ] Implement scaffold overlap diagnostics.
- [ ] Implement split size summaries.
- [ ] Add plotting helper for train/test scaffold counts.
- [ ] Commit: `feat: add split diagnostics`.

**Acceptance Criteria:**
- Diagnostics clearly show zero scaffold overlap for scaffold split.
- Diagnostics can be exported to CSV or plotted in notebooks.

---

## Phase 5: Model Baselines

### Task 5.1: Unified Model Registry

**Files:**
- Create: `src/models.py`
- Test: `tests/test_models.py`

- [ ] Implement a model factory for `ridge`, `lasso`, `random_forest`, `xgboost`, and `mlp`.
- [ ] Use scikit-learn-compatible `fit` and `predict` for all models.
- [ ] For descriptor and combined features, wrap scaling inside `Pipeline`.
- [ ] Add tests that each model can fit and predict on a tiny synthetic regression dataset.
- [ ] Commit: `feat: add model registry`.

**Acceptance Criteria:**
- All MVP models expose `fit(X_train, y_train)` and `predict(X_test)`.
- Prediction shape is `(n_samples,)`.

### Task 5.2: PyTorch MLP Regressor

**Files:**
- Modify: `src/models.py`
- Test: `tests/test_models.py`

- [ ] Implement `MLPRegressorTorch` with hidden layers, dropout, batch size, epochs, learning rate, seed, and early stopping.
- [ ] Add deterministic seed handling.
- [ ] Add smoke test that training reduces loss on a tiny synthetic dataset.
- [ ] Commit: `feat: add pytorch mlp regressor`.

**Acceptance Criteria:**
- MLP can be used through the same registry interface as classical models.
- CPU training works on small datasets.

---

## Phase 6: Evaluation And Benchmark Runner

### Task 6.1: Regression Metrics

**Files:**
- Create: `src/evaluate.py`
- Test: `tests/test_evaluate.py`

- [ ] Implement RMSE, MAE, and R2 metrics.
- [ ] Implement `evaluate_regression(y_true, y_pred) -> dict`.
- [ ] Add tests with known numeric values.
- [ ] Commit: `feat: add regression metrics`.

**Acceptance Criteria:**
- Metrics match scikit-learn definitions.
- RMSE, MAE, and R2 are always present in result rows.

### Task 6.2: Single Experiment Runner

**Files:**
- Create: `src/train.py`
- Test: `tests/test_train.py`

- [ ] Implement `run_experiment(dataset_key, feature_type, model_key, split_type, seed) -> dict`.
- [ ] Load processed data.
- [ ] Create split.
- [ ] Build features.
- [ ] Train model.
- [ ] Evaluate on validation and test.
- [ ] Return one flat result dictionary containing dataset, feature type, model, split type, seed, metrics, and split sizes.
- [ ] Commit: `feat: add single experiment runner`.

**Acceptance Criteria:**
- One ESOL Ridge descriptor experiment runs end-to-end.
- Result dictionary can be directly appended to a pandas DataFrame.

### Task 6.3: Benchmark Matrix Runner

**Files:**
- Modify: `src/train.py`
- Create: `scripts/run_benchmark.py`
- Output: `results/benchmark_results.csv`

- [ ] Run datasets: `esol`, `freesolv`.
- [ ] Run feature types: `descriptors`, `fingerprints`, `combined`.
- [ ] Run models: `ridge`, `lasso`, `random_forest`, `xgboost`, `mlp`.
- [ ] Run split types: `random`, `scaffold`.
- [ ] Run seeds: `0`, `1`, `2`, `3`, `4`.
- [ ] Write all rows to `results/benchmark_results.csv`.
- [ ] Commit: `feat: add full benchmark runner`.

**Acceptance Criteria:**
- Benchmark CSV has one row per dataset-feature-model-split-seed combination.
- Failed experiments are surfaced clearly instead of being silently skipped.

### Task 6.4: Aggregate Benchmark Results

**Files:**
- Modify: `src/evaluate.py`
- Create: `scripts/summarize_results.py`
- Output: `results/benchmark_summary.csv`

- [ ] Group by dataset, feature type, model, and split type.
- [ ] Compute mean and standard deviation for RMSE, MAE, and R2 across seeds.
- [ ] Save summary CSV.
- [ ] Commit: `feat: summarize benchmark results`.

**Acceptance Criteria:**
- Summary table supports direct random-vs-scaffold comparison.
- Means and standard deviations are included.

---

## Phase 7: Analysis And Visualizations

### Task 7.1: Prediction Plots

**Files:**
- Modify: `src/visualize.py`
- Create: `notebooks/02_benchmark.ipynb`
- Output: `results/figures/predicted_vs_actual_<dataset>_<model>_<split>.png`

- [ ] Save per-experiment predictions or rerun selected best models for plotting.
- [ ] Plot predicted vs actual scatter with identity line.
- [ ] Plot residual distributions.
- [ ] Commit: `feat: add benchmark visualization notebook`.

**Acceptance Criteria:**
- Notebook shows side-by-side random vs scaffold results.
- At least ESOL and FreeSolv each have one predicted-vs-actual figure.

### Task 7.2: Feature Importance And SHAP

**Files:**
- Create: `notebooks/03_analysis.ipynb`
- Modify: `src/visualize.py`
- Output: `results/figures/feature_importance_<dataset>.png`
- Output: `results/figures/shap_summary_<dataset>.png`

- [ ] Use RF/XGBoost built-in feature importances.
- [ ] Run SHAP on selected descriptor-based models.
- [ ] Save top feature importance plots.
- [ ] Commit: `feat: add interpretability analysis`.

**Acceptance Criteria:**
- Analysis identifies chemically meaningful descriptor effects when possible.
- SHAP is treated as analysis output, not required for every model.

### Task 7.3: Chemical Space Visualization

**Files:**
- Modify: `notebooks/03_analysis.ipynb`
- Output: `results/figures/chemical_space_<dataset>_<split>.png`

- [ ] Generate Morgan fingerprints.
- [ ] Reduce to 2D with UMAP or t-SNE.
- [ ] Color by train/validation/test assignment.
- [ ] Compare random split and scaffold split visually.
- [ ] Commit: `feat: add chemical space split visualization`.

**Acceptance Criteria:**
- Scaffold split visibly separates chemical families more than random split.
- Plots support the PRD's methodological argument.

### Task 7.4: Error Analysis And Candidate Ranking Demo

**Files:**
- Modify: `notebooks/03_analysis.ipynb`
- Output: `results/error_analysis.csv`
- Output: `results/candidate_ranking_demo.csv`

- [ ] Identify highest absolute error molecules and their scaffolds.
- [ ] For RF, compute tree-level prediction variance as uncertainty.
- [ ] Rank candidates using predicted target plus uncertainty.
- [ ] Commit: `feat: add error analysis and ranking demo`.

**Acceptance Criteria:**
- Error analysis table includes SMILES, target, prediction, absolute error, and scaffold.
- Candidate ranking demo explains how uncertainty affects prioritization.

---

## Phase 8: Documentation And Reproducibility

### Task 8.1: README For Portfolio Review

**Files:**
- Modify: `README.md`

- [ ] Explain project motivation and key methodological point: random split can overestimate generalization.
- [ ] Document setup commands.
- [ ] Document preprocessing, benchmark, and summary commands.
- [ ] Include result summary table.
- [ ] Include key figures.
- [ ] Commit: `docs: write project readme`.

**Acceptance Criteria:**
- A reviewer can understand the project in under 10 minutes.
- Commands are copy-paste runnable from a fresh clone.

### Task 8.2: Reproducibility Pass

**Files:**
- Modify: `requirements.txt`
- Modify: `README.md`
- Modify: `.gitignore`

- [ ] Pin dependency versions after the benchmark is working.
- [ ] Add `.gitignore` rules for caches, notebooks checkpoints, large raw data if needed, and model artifacts.
- [ ] Document fixed random seeds.
- [ ] Commit: `chore: improve reproducibility`.

**Acceptance Criteria:**
- Fresh environment can run preprocessing and at least one benchmark experiment.
- Random seeds are documented and used consistently.

---

## Phase 9: Optional Extensions

### Task 9.1: Simple GCN

**Files:**
- Create: `src/graph_featurize.py`
- Create: `src/gnn_models.py`
- Test: `tests/test_graph_featurize.py`

- [ ] Add atom and bond graph featurization.
- [ ] Add simple GCN model if PyTorch Geometric is available.
- [ ] Compare against MLP and classical baselines.

**Acceptance Criteria:**
- GNN is clearly marked as optional and does not block MVP.

### Task 9.2: Classification Dataset Extension

**Files:**
- Modify: `src/config.py`
- Modify: `src/evaluate.py`
- Modify: `src/models.py`
- Create: `tests/test_classification_metrics.py`

- [ ] Add BBBP or BACE.
- [ ] Add AUC, F1, accuracy, and precision/recall.
- [ ] Add classifier variants for supported models.

**Acceptance Criteria:**
- Classification path is separate from regression path and does not complicate MVP APIs.

---

## MVP Execution Order

1. Phase 0: Repository foundation.
2. Phase 1: Data loading and cleaning.
3. Phase 3: Featurization.
4. Phase 4: Random and scaffold splits.
5. Phase 5: Model baselines.
6. Phase 6: Evaluation and benchmark runner.
7. Phase 7.1 and 7.3: Key analysis plots.
8. Phase 8: README and reproducibility.

Phases 2, 7.2, and 7.4 are valuable portfolio polish. Phase 9 is optional expansion only.

## Coverage Check Against PRD

- Data processing: covered by Phase 1 and Phase 2.
- RDKit descriptors and Morgan fingerprints: covered by Phase 3.
- Random and scaffold splits: covered by Phase 4.
- RF, XGBoost, Ridge/Lasso, MLP: covered by Phase 5.
- RMSE, MAE, R2 and mean/std across seeds: covered by Phase 6.
- Prediction plots, SHAP, chemical space, error analysis, candidate ranking: covered by Phase 7.
- README, notebooks, result tables, figures: covered by Phase 8.
- GNN and classification datasets: scoped as optional Phase 9.

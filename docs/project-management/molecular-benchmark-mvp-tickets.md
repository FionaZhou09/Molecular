# Molecular Property Prediction Benchmark - MVP Project Management Plan

**Repository:** https://github.com/FionaZhou09/Molecular  
**Local path:** `/Users/yingzhou/Documents/Molecular`  
**Source PRD:** `molecular_property_prediction_PRD.md`  
**Source implementation plan:** `docs/superpowers/plans/2026-07-01-molecular-property-prediction-benchmark.md`  
**Manager scope:** Convert the implementation plan into executable tickets for SWE delivery and reviewer approval.

**Repository state note:** The local folder may not be initialized as a git repository yet. Recommended commit messages are retained for future GitHub workflow, but SWE windows should not commit unless the manager explicitly initializes git or asks for commits.

## Project Phase Overview

MVP priority is to build a reproducible benchmark first, then add portfolio polish.

| Phase | Scope | Status | Manager Decision |
|---|---|---:|---|
| Phase 0 | Repository skeleton and dependencies | MVP | Must go first |
| Phase 1 | Data loading, cleaning, SMILES validation | MVP | Data quality foundation |
| Phase 3 | RDKit descriptors, Morgan fingerprints, feature builder | MVP | Core benchmark inputs |
| Phase 4 | Random split, scaffold split, diagnostics | MVP | Main methodological value |
| Phase 5 | RF, XGBoost, Ridge, Lasso, MLP | MVP | Satisfies PRD success criteria |
| Phase 6 | Metrics, experiment runner, benchmark summary | MVP | Reproducible result backbone |
| Phase 7.1 | Predicted vs actual and residual plots | MVP | Portfolio-ready result display |
| Phase 7.3 | Chemical space split visualization | MVP | Supports random vs scaffold argument |
| Phase 8 | README and reproducibility pass | MVP | Required final deliverable |
| Phase 2 | EDA utilities and notebook | Portfolio polish | Useful but non-blocking |
| Phase 7.2 | Feature importance and SHAP | Portfolio polish | Adds interpretability |
| Phase 7.4 | Error analysis and candidate ranking | Portfolio polish | Adds depth |
| Phase 9 | GCN and classification extension | Optional | Not in MVP |

Every ticket follows this workflow:

1. SWE implements.
2. SWE self-tests.
3. Reviewer performs spec review.
4. SWE fixes spec issues.
5. Reviewer performs code quality review.
6. SWE fixes quality issues.
7. Manager marks complete.

## MVP Ticket List

### MOL-MVP-001 - Initialize Project Structure And Dependencies

- **Status:** Complete. Boss review accepted this ticket; `python -m pytest` reached the initialized project test state for this phase.
- **Background:** Create the PRD-defined repository layout so later work has stable paths.
- **Owner role:** SWE
- **Reviewer role:** Tech Lead
- **Input files:** `molecular_property_prediction_PRD.md`; implementation plan Phase 0
- **Output files:** `README.md`, `requirements.txt`, `src/__init__.py`, `data/raw/.gitkeep`, `data/processed/.gitkeep`, `results/figures/.gitkeep`, `notebooks/.gitkeep`, `tests/.gitkeep`
- **Implementation requirements:** Create the PRD section 7 directory structure. Add MVP dependencies: `pandas`, `numpy`, `scikit-learn`, `xgboost`, `torch`, `rdkit`, `matplotlib`, `seaborn`, `pytest`, `jupyter`. Do not implement business logic yet.
- **Testing requirements:** Run `python -m pytest`; it should start cleanly without import or syntax errors.
- **Acceptance criteria:** Repo layout matches PRD. Empty or initial test run does not fail because of project setup. No unrelated files are added.
- **Estimate:** S
- **Dependencies:** None
- **Recommended commit message:** `chore: initialize project structure`

### MOL-MVP-002 - Add Dataset Configuration And Raw Loading

- **Status:** Complete. Dataset metadata, raw loading, normalization, and tests were accepted by review.
- **Background:** MVP supports ESOL and FreeSolv, normalized to `{smiles, target}`.
- **Owner role:** SWE
- **Reviewer role:** ML Engineer
- **Input files:** PRD sections 4 and 5.1; implementation plan Phase 1.1 and 1.2; raw CSV files from MOL-MVP-002A
- **Output files:** `src/config.py`, `src/data_loader.py`, `tests/test_config.py`, `tests/test_data_loader.py`
- **Implementation requirements:** Register `esol` and `freesolv` metadata with raw path, processed path, source URL or source note, expected row count, SMILES column, target column, and `task_type="regression"`. Use actual raw columns documented in `data/raw/README.md`: ESOL SMILES column `smiles`, ESOL target column `measured log solubility in mols per litre`; FreeSolv SMILES column `smiles`, FreeSolv target column `y`. Implement `load_raw_dataset(dataset_key)` and `normalize_dataset(df, smiles_col, target_col)`. Normalized data must contain exactly `smiles,target`. Drop rows with missing SMILES or target.
- **Testing requirements:** Test both dataset keys exist and are regression tasks. Use in-memory DataFrames to test missing-row dropping and column normalization.
- **Acceptance criteria:** `pytest tests/test_config.py tests/test_data_loader.py -v` passes. Normalized output columns are exactly `smiles,target`. Dataset metadata points to existing raw CSV paths created by MOL-MVP-002A.
- **Estimate:** S
- **Dependencies:** MOL-MVP-001, MOL-MVP-002A
- **Recommended commit message:** `feat: add dataset configuration and raw loading`

### MOL-MVP-002A - Acquire ESOL And FreeSolv Raw CSVs

- **Status:** Complete. Raw CSVs were acquired from DeepChem MoleculeNet sources, verified readable, and documented in `data/raw/README.md`.
- **Background:** Later data loading tickets assume raw CSVs exist. This ticket makes dataset availability explicit before implementing loaders.
- **Owner role:** SWE
- **Reviewer role:** ML Engineer
- **Input files:** PRD section 4.3; official MoleculeNet or DeepChem dataset references
- **Output files:** `data/raw/esol.csv`, `data/raw/freesolv.csv`, optionally `data/raw/README.md`
- **Implementation requirements:** Acquire ESOL/Delaney and FreeSolv raw CSVs from a documented source. Preferred source is MoleculeNet official data; acceptable fallback is DeepChem's MoleculeNet loader or another clearly documented mirror if official download is unavailable. Preserve or document original source column names. Expected source columns are ESOL `smiles` plus `measured log solubility in mols per litre`, and FreeSolv `smiles` plus `y` for the acquired DeepChem CSV. Record source URL, retrieval date, and any filename normalization in `data/raw/README.md`.
- **Testing requirements:** Verify both CSV files exist, are readable by pandas, have nonzero rows, and contain expected SMILES/target source columns. Do not run RDKit validation in this ticket.
- **Acceptance criteria:** `data/raw/esol.csv` and `data/raw/freesolv.csv` exist. Source provenance is documented. Row counts are reported and roughly match expected MoleculeNet sizes: ESOL about 1128 rows, FreeSolv about 642 rows.
- **Estimate:** S
- **Dependencies:** MOL-MVP-001
- **Recommended commit message:** `data: add raw esol and freesolv datasets`

### MOL-MVP-003 - Add SMILES Validation And Preprocessing Script

- **Status note:** Ready to start. MOL-MVP-002 is complete.
- **Background:** Invalid molecules must be removed from processed data and remain inspectable.
- **Owner role:** SWE
- **Reviewer role:** ML Engineer
- **Input files:** `src/config.py`, `src/data_loader.py`, PRD section 5.1
- **Output files:** `src/data_loader.py`, `scripts/preprocess_data.py`, `tests/test_data_loader.py`, `data/processed/<dataset>.csv`
- **Implementation requirements:** Implement `validate_smiles(df) -> (valid_df, invalid_df)` with `Chem.MolFromSmiles`. Implement `save_processed_dataset(dataset_key, df)`. Add CLI support for `--dataset esol|freesolv`.
- **Testing requirements:** Test that `CCO` is valid and `not_a_smiles` is invalid. Test saved CSV contains only `smiles,target`.
- **Acceptance criteria:** `python scripts/preprocess_data.py --dataset esol` writes `data/processed/esol.csv`. Invalid rows do not enter processed output.
- **Estimate:** S
- **Dependencies:** MOL-MVP-002
- **Recommended commit message:** `feat: add smiles validation and preprocessing script`

### MOL-MVP-004 - Implement RDKit Descriptors And Morgan Fingerprints

- **Background:** Implement the two core MVP molecular representations.
- **Owner role:** SWE
- **Reviewer role:** ML Engineer
- **Input files:** PRD section 5.2; implementation plan Phase 3.1 and 3.2
- **Output files:** `src/featurize.py`, `tests/test_featurize.py`
- **Implementation requirements:** Implement `compute_descriptors(smiles_list)` with 20-30 stable descriptors, including molecular weight, LogP, TPSA, HBD, HBA, rotatable bonds, ring counts, aromatic rings, formal charge, FractionCSP3, and molar refractivity. Implement `compute_morgan_fingerprints(smiles_list, radius=2, n_bits=2048)` with support for 512, 1024, and 2048 bits. Invalid SMILES must not be silently featurized.
- **Testing requirements:** Test finite numeric descriptors for `CCO`, `c1ccccc1`, and `CC(=O)O`. Test fingerprint shape and binary values.
- **Acceptance criteria:** Descriptor column names are stable. Fingerprints have shape `(n_molecules, n_bits)` and values only `0` or `1`.
- **Estimate:** M
- **Dependencies:** MOL-MVP-003
- **Recommended commit message:** `feat: add rdkit descriptors and morgan fingerprints`

### MOL-MVP-005 - Add Feature Matrix Builder With No Global Scaling

- **Background:** Provide a single feature entrypoint while preventing descriptor scaling leakage.
- **Owner role:** SWE
- **Reviewer role:** ML Engineer
- **Input files:** `src/featurize.py`, PRD section 5.2
- **Output files:** `src/featurize.py`, `tests/test_featurize.py`
- **Implementation requirements:** Implement `build_feature_matrix(df, feature_type)` for `descriptors`, `fingerprints`, and `combined`. Return `X, feature_names`. Do not fit a `StandardScaler` inside this function. Scaling must happen inside model/train pipelines after splitting.
- **Testing requirements:** Test all three feature modes. Test combined feature dimension equals descriptor plus fingerprint dimensions. Confirm builder does not globally standardize descriptors.
- **Acceptance criteria:** Reviewer can verify descriptor scaling is fit only on train data in later workflows.
- **Estimate:** S
- **Dependencies:** MOL-MVP-004
- **Recommended commit message:** `feat: add feature matrix builder`

### MOL-MVP-006 - Implement Random And Scaffold Splits

- **Background:** Random split vs scaffold split is the project's central methodological comparison.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** PRD section 5.3; implementation plan Phase 4.1 and 4.2
- **Output files:** `src/splits.py`, `tests/test_splits.py`
- **Implementation requirements:** Implement `random_split(df, train_size=0.8, val_size=0.1, test_size=0.1, seed=42)`. Implement `compute_scaffold(smiles)` with RDKit Bemis-Murcko scaffolds. Implement `scaffold_split(...)` so the same scaffold never appears in more than one of train, validation, or test. Return index arrays.
- **Testing requirements:** Test deterministic random split, non-overlap, and full coverage. Test scaffold split with duplicated scaffolds.
- **Acceptance criteria:** Same seed gives same output. Splits cover all rows exactly once. No scaffold crosses split boundaries.
- **Estimate:** M
- **Dependencies:** MOL-MVP-003
- **Recommended commit message:** `feat: add random and scaffold-aware splits`

### MOL-MVP-007 - Add Split Diagnostics And Visualization Helpers

- **Background:** Scaffold split correctness must be auditable, not just asserted.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** `src/splits.py`, PRD section 5.3
- **Output files:** `src/splits.py`, `src/visualize.py`, `tests/test_splits.py`
- **Implementation requirements:** Add split size summary, scaffold overlap diagnostics, and a helper for plotting train/validation/test scaffold counts. Diagnostics should return DataFrames or dictionaries that can be exported.
- **Testing requirements:** Test scaffold diagnostics show zero overlap. Test summaries report all split sizes.
- **Acceptance criteria:** Reviewer can verify scaffold leakage is zero through diagnostics.
- **Estimate:** S
- **Dependencies:** MOL-MVP-006
- **Recommended commit message:** `feat: add split diagnostics`

### MOL-MVP-008 - Add Classical Model Registry

- **Background:** A unified model interface enables batch benchmark execution.
- **Owner role:** SWE
- **Reviewer role:** ML Engineer
- **Input files:** PRD section 5.4; implementation plan Phase 5.1
- **Output files:** `src/models.py`, `tests/test_models.py`
- **Implementation requirements:** Implement a model factory for `ridge`, `lasso`, `random_forest`, and `xgboost`. The required interface is `create_model(model_key, feature_type, seed, **kwargs)`. All models must expose scikit-learn-compatible `fit` and `predict`. If `feature_type` is `descriptors` or `combined`, wrap the estimator in a `Pipeline` with `StandardScaler` followed by the model so scaler fitting happens only inside `fit(X_train, y_train)`. If `feature_type` is `fingerprints`, do not scale binary fingerprint features. All applicable models should receive a seed.
- **Testing requirements:** Each model fits and predicts on a tiny synthetic regression dataset. Prediction shape is `(n_samples,)`.
- **Acceptance criteria:** Registry keys are stable. Tests verify descriptor and combined models include train-time scaling, while fingerprint-only models do not include `StandardScaler`. No scaler is fit on the full dataset.
- **Estimate:** M
- **Dependencies:** MOL-MVP-005
- **Recommended commit message:** `feat: add classical model registry`

### MOL-MVP-009 - Add PyTorch MLP Regressor

- **Background:** PRD requires at least one neural network model in the MVP benchmark.
- **Owner role:** SWE
- **Reviewer role:** ML Engineer
- **Input files:** `src/models.py`, PRD section 5.4
- **Output files:** `src/models.py`, `tests/test_models.py`
- **Implementation requirements:** Implement `MLPRegressorTorch` with hidden layers, dropout, batch size, epochs, learning rate, seed, and early stopping. Expose it as `mlp` through the same registry.
- **Testing requirements:** Smoke test on a tiny synthetic dataset. Training should reduce loss. Prediction shape must be correct. Seed handling should be inspectable.
- **Acceptance criteria:** MLP uses the same `fit/predict` interface as classical models and runs on CPU.
- **Estimate:** M
- **Dependencies:** MOL-MVP-008
- **Recommended commit message:** `feat: add pytorch mlp regressor`

### MOL-MVP-010 - Add Regression Metrics And Single Experiment Runner

- **Background:** Every experiment needs one traceable result row.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** `src/config.py`, `src/data_loader.py`, `src/featurize.py`, `src/splits.py`, `src/models.py`
- **Output files:** `src/evaluate.py`, `src/train.py`, `tests/test_evaluate.py`, `tests/test_train.py`
- **Implementation requirements:** Implement RMSE, MAE, and R2. Implement `evaluate_regression(y_true, y_pred)`. Implement `run_experiment(dataset_key, feature_type, model_key, split_type, seed)`. Return a flat result dictionary containing dataset, feature type, model, split type, seed, validation/test metrics, and split sizes. Also return or expose a prediction table for validation and test rows with columns: `dataset`, `feature_type`, `model_key`, `split_type`, `seed`, `split`, `smiles`, `target`, `prediction`, `residual`, and `scaffold`.
- **Testing requirements:** Metrics must match scikit-learn definitions. At least one Ridge descriptor experiment should run end-to-end with fixture or processed data.
- **Acceptance criteria:** Result rows can be appended directly to a pandas DataFrame and traced by `dataset / feature_type / model_key / split_type / seed`. Prediction rows can be appended to `results/predictions.csv` by the benchmark runner and are sufficient for predicted-vs-actual plots.
- **Estimate:** M
- **Dependencies:** MOL-MVP-006, MOL-MVP-008, MOL-MVP-009
- **Recommended commit message:** `feat: add regression metrics and single experiment runner`

### MOL-MVP-011 - Add Benchmark Matrix Runner And Summary

- **Background:** Produce the main benchmark table for random vs scaffold comparison.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** `src/train.py`, `src/evaluate.py`
- **Output files:** `scripts/run_benchmark.py`, `scripts/summarize_results.py`, `results/benchmark_results.csv`, `results/benchmark_summary.csv`, `results/predictions.csv`
- **Implementation requirements:** Run datasets `esol,freesolv`; feature types `descriptors,fingerprints,combined`; models `ridge,lasso,random_forest,xgboost,mlp`; split types `random,scaffold`; seeds `0,1,2,3,4`. Failed experiments must be explicit and not silently skipped. Write one metrics row per experiment to `results/benchmark_results.csv`. Write validation/test prediction rows to `results/predictions.csv` with the schema defined in MOL-MVP-010. Summary groups by dataset, feature type, model, and split type, with mean and std for RMSE, MAE, and R2.
- **Testing requirements:** Provide a small smoke mode or dry-run. Test summary aggregation produces mean and std.
- **Acceptance criteria:** Benchmark CSV has one row per dataset-feature-model-split-seed combination. Predictions CSV contains enough metadata to regenerate predicted-vs-actual and residual plots without retraining. Summary supports direct random-vs-scaffold comparison.
- **Estimate:** M
- **Dependencies:** MOL-MVP-010
- **Recommended commit message:** `feat: add benchmark runner and result summary`

### MOL-MVP-012 - Add Benchmark Notebook And Prediction Plots

- **Background:** Convert benchmark outputs into reviewer-friendly visuals.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** `results/benchmark_results.csv`, `results/benchmark_summary.csv`, `results/predictions.csv`, `src/visualize.py`
- **Output files:** `notebooks/02_benchmark.ipynb`, `results/figures/predicted_vs_actual_<dataset>_<model>_<split>.png`
- **Implementation requirements:** Show random vs scaffold summary. For ESOL and FreeSolv, output at least one predicted-vs-actual plot and one residual distribution. Figures must include dataset/model/split labels.
- **Testing requirements:** Notebook runs top-to-bottom. Figure files exist and are non-empty.
- **Acceptance criteria:** A reviewer can quickly see random vs scaffold performance differences.
- **Estimate:** M
- **Dependencies:** MOL-MVP-011
- **Recommended commit message:** `feat: add benchmark visualization notebook`

### MOL-MVP-013 - Add Chemical Space Split Visualization

- **Background:** Visualize why scaffold split is stricter than random split.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** `src/featurize.py`, `src/splits.py`, `notebooks/03_analysis.ipynb`
- **Output files:** `notebooks/03_analysis.ipynb`, `results/figures/chemical_space_<dataset>_<split>.png`
- **Implementation requirements:** Use Morgan fingerprints and reduce to 2D with UMAP or t-SNE. Color by train/validation/test assignment. Compare random split and scaffold split visually for ESOL and FreeSolv. Fix the dimensionality-reduction seed.
- **Testing requirements:** Notebook runs. Figures exist and are non-empty.
- **Acceptance criteria:** Plots support the PRD's methodological claim that scaffold split better represents chemical-family generalization.
- **Estimate:** M
- **Dependencies:** MOL-MVP-006, MOL-MVP-011
- **Recommended commit message:** `feat: add chemical space split visualization`

### MOL-MVP-014 - Write README And Reproducibility Pass

- **Background:** Final MVP must be understandable and reproducible from a fresh clone.
- **Owner role:** SWE
- **Reviewer role:** Engineering Manager
- **Input files:** PRD, benchmark outputs, figures
- **Output files:** `README.md`, `requirements.txt`, `.gitignore`
- **Implementation requirements:** Explain motivation and the random split vs scaffold split message. Document setup, preprocessing, benchmark, and summary commands. Include result summary table and key figures. Pin dependency versions after the benchmark works. Document fixed random seeds. Add `.gitignore` entries for caches, notebook checkpoints, large artifacts, and model artifacts.
- **Testing requirements:** From a fresh environment, documented commands should run preprocessing and at least one benchmark experiment.
- **Acceptance criteria:** A third-party reviewer can understand the project, reproduce a run, and identify the key result in under 10 minutes.
- **Estimate:** M
- **Dependencies:** MOL-MVP-012, MOL-MVP-013
- **Recommended commit message:** `docs: write readme and improve reproducibility`

## Portfolio Polish Ticket List

### MOL-POLISH-001 - Add EDA Utilities And Notebook

- **Background:** Improve portfolio storytelling with basic data understanding.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** Processed ESOL and FreeSolv data
- **Output files:** `src/eda.py`, `tests/test_eda.py`, `notebooks/01_eda.ipynb`, `results/figures/esol_target_distribution.png`, `results/figures/freesolv_target_distribution.png`
- **Implementation requirements:** Add molecular weight, heavy atom count, atom count, and ring count summaries. Add target summary. Notebook should plot molecular weight, atom count, and target distributions.
- **Testing requirements:** Summary functions return non-empty DataFrames on cleaned data.
- **Acceptance criteria:** Notebook runs top-to-bottom and saves figures.
- **Estimate:** M
- **Dependencies:** MOL-MVP-003, MOL-MVP-004
- **Recommended commit message:** `docs: add eda notebook and summary utilities`

### MOL-POLISH-002 - Add Feature Importance And SHAP Analysis

- **Background:** Add interpretability to the benchmark story.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** Benchmark results; selected RF/XGBoost descriptor experiments
- **Output files:** `notebooks/03_analysis.ipynb`, `src/visualize.py`, `results/figures/feature_importance_<dataset>.png`, `results/figures/shap_summary_<dataset>.png`
- **Implementation requirements:** Use RF/XGBoost built-in feature importances. Run SHAP on selected descriptor-based models only. Do not require SHAP for every model.
- **Testing requirements:** Notebook runs. Figures exist. SHAP failures must not block MVP benchmark execution.
- **Acceptance criteria:** Analysis identifies chemically meaningful descriptor effects without overclaiming causality.
- **Estimate:** M
- **Dependencies:** MOL-MVP-011
- **Recommended commit message:** `feat: add interpretability analysis`

### MOL-POLISH-003 - Add Error Analysis And Candidate Ranking Demo

- **Background:** Add advanced portfolio depth around errors and uncertainty-aware ranking.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** Selected experiment predictions; RF model outputs
- **Output files:** `notebooks/03_analysis.ipynb`, `results/error_analysis.csv`, `results/candidate_ranking_demo.csv`
- **Implementation requirements:** Identify highest absolute-error molecules and scaffolds. For RF, compute tree-level prediction variance as uncertainty. Ranking should include prediction and uncertainty.
- **Testing requirements:** Error analysis CSV includes SMILES, target, prediction, absolute error, and scaffold. Ranking output is stable under fixed seed.
- **Acceptance criteria:** Demo clearly explains how uncertainty affects prioritization.
- **Estimate:** M
- **Dependencies:** MOL-MVP-011, MOL-MVP-013
- **Recommended commit message:** `feat: add error analysis and ranking demo`

## Optional Ticket List

### MOL-OPT-001 - Add Optional Simple GCN Baseline

- **Background:** GNN is useful but must not delay MVP.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** PRD optional graph representation
- **Output files:** `src/graph_featurize.py`, `src/gnn_models.py`, `tests/test_graph_featurize.py`
- **Implementation requirements:** Implement atom and bond graph featurization. If PyTorch Geometric is available, add a simple GCN. Mark this path optional.
- **Testing requirements:** Graph featurization smoke test. MVP imports still work without PyTorch Geometric.
- **Acceptance criteria:** GNN comparison does not block or complicate MVP workflows.
- **Estimate:** L
- **Dependencies:** MOL-MVP-011
- **Recommended commit message:** `feat: add optional gcn baseline`

### MOL-OPT-002 - Add Optional Classification Dataset Extension

- **Background:** Classification broadens scope but should remain separate from regression MVP.
- **Owner role:** SWE
- **Reviewer role:** ML Reviewer
- **Input files:** PRD section 4.2
- **Output files:** `src/config.py`, `src/evaluate.py`, `src/models.py`, `tests/test_classification_metrics.py`
- **Implementation requirements:** Add BBBP or BACE. Add AUC, F1, accuracy, precision, and recall. Keep classification path separate from regression path.
- **Testing requirements:** Known-value classification metric tests. Existing regression tests still pass.
- **Acceptance criteria:** Classification does not complicate MVP regression APIs.
- **Estimate:** L
- **Dependencies:** MOL-MVP-014
- **Recommended commit message:** `feat: add optional classification benchmark`

## Reviewer Checklist

Use this checklist for every ticket:

- Does the implementation match the PRD?
- Does it match the implementation plan phase and ticket scope?
- Is there no over-implementation, especially no premature GNN, classification, MLflow/W&B, or complex HPO?
- Are there meaningful tests?
- Is the work reproducible?
- Are random seeds fixed and passed through split/model/MLP/UMAP where relevant?
- Is data leakage avoided?
- Does scaffold split guarantee the same Bemis-Murcko scaffold never crosses train/validation/test?
- Is descriptor scaling fit only on train data?
- Can each benchmark result be traced to dataset, feature type, model, split type, and seed?
- Does processed data contain only valid SMILES and targets?
- Are failed experiments surfaced clearly instead of silently skipped?
- Can figures and notebooks be regenerated from documented commands?
- Are README commands copy-paste runnable from a fresh clone?

## Recommended Execution Order

1. MOL-MVP-001
2. MOL-MVP-002A
3. MOL-MVP-002
4. MOL-MVP-003
5. MOL-MVP-004
6. MOL-MVP-005
7. MOL-MVP-006
8. MOL-MVP-007
9. MOL-MVP-008
10. MOL-MVP-009
11. MOL-MVP-010
12. MOL-MVP-011
13. MOL-MVP-012 and MOL-MVP-013 in parallel if two SWE windows are available
14. MOL-MVP-014
15. Portfolio polish tickets
16. Optional tickets only after MVP review

## Risk And Blocker Management

- **RDKit installation risk:** Verify import immediately after MOL-MVP-001. If pip install is unstable, document a conda-based environment path.
- **Python environment risk:** Dependencies may not be installed after project initialization. Before MOL-MVP-002A or MOL-MVP-002, SWE should create/activate an environment and install `requirements.txt`; if RDKit fails through pip, use a conda/mamba environment and document it.
- **Dataset source risk:** MOL-MVP-002A must resolve local raw CSV availability before loader work starts. Support local CSV first. Download automation is useful but should not block MVP.
- **Scaffold ratio mismatch:** Allow approximate 80/10/10 splits, but report actual split sizes and never allow scaffold leakage.
- **MLP instability on small datasets:** Use fixed seed and early stopping. Document that neural networks may underperform classical ML on small molecular datasets.
- **XGBoost or SHAP environment issues:** XGBoost is MVP and should be smoke-tested early. SHAP is polish and must not block MVP.
- **Benchmark runtime risk:** Add smoke mode for fast validation. Run full five-seed benchmark only after single-experiment workflow is stable.
- **Unexpected result pattern:** Do not tune to force scaffold split to look worse. First verify no leakage, train-only scaling, seed handling, and split correctness. If results are nuanced, document that honestly.

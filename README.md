# Molecular Property Prediction Benchmark

This project is a reproducible molecular property prediction benchmark for small regression datasets. It compares classical machine learning and a PyTorch MLP across molecular representations and, most importantly, compares random splits against scaffold-aware splits.

The key methodological point is that random splits can overestimate generalization for molecules: molecules with similar chemical scaffolds can land in both train and test sets. Scaffold splitting groups molecules by Bemis-Murcko scaffold before assigning train, validation, and test rows, so test performance better reflects generalization to new chemical families.

## Current MVP

- Datasets: ESOL and FreeSolv
- Features: RDKit descriptors, Morgan fingerprints, and combined descriptors + fingerprints
- Splits: random and scaffold train/validation/test splits
- Models: Ridge, Lasso, Random Forest, XGBoost, and PyTorch MLP
- Metrics: RMSE, MAE, and R2
- Outputs: benchmark result CSVs, prediction rows, summary tables, prediction plots, residual plots, and chemical-space split plots

## Key Result

Ridge on descriptor features shows the expected pattern: scaffold split performance is worse than random split performance, which is a more conservative estimate of chemical-family generalization.

| Dataset | Split | Test RMSE mean | Test RMSE std | Test MAE mean | Test R2 mean |
|---|---:|---:|---:|---:|---:|
| ESOL | random | 0.908 | 0.044 | 0.712 | 0.819 |
| ESOL | scaffold | 1.225 | 0.121 | 0.874 | 0.662 |
| FreeSolv | random | 0.411 | 0.018 | 0.312 | 0.799 |
| FreeSolv | scaffold | 0.574 | 0.038 | 0.425 | 0.687 |

Full results are in:

- `results/benchmark_results.csv`
- `results/benchmark_summary.csv`
- `results/predictions.csv`

## Figures

Prediction and residual figures:

- `results/figures/predicted_vs_actual_esol_ridge_random.png`
- `results/figures/predicted_vs_actual_freesolv_ridge_random.png`
- `results/figures/residuals_esol_ridge_random.png`
- `results/figures/residuals_freesolv_ridge_random.png`

Chemical-space split figures:

- `results/figures/chemical_space_esol_random.png`
- `results/figures/chemical_space_esol_scaffold.png`
- `results/figures/chemical_space_freesolv_random.png`
- `results/figures/chemical_space_freesolv_scaffold.png`

## Setup

Python 3.13 was used for the current MVP run. Install dependencies from the pinned requirements file:

```bash
python -m pip install -r requirements.txt
```

PyTorch wheels can vary by platform and Python version. If `pip install -r requirements.txt` cannot resolve `torch==2.12.1` on your machine, install PyTorch from the official PyTorch or conda-forge channel for your platform, then rerun the requirements command for the remaining packages.

Verify the environment:

```bash
python -m pytest
```

## Data

Raw and processed CSVs are included for the MVP datasets:

- `data/raw/esol.csv`
- `data/raw/freesolv.csv`
- `data/processed/esol.csv`
- `data/processed/freesolv.csv`

To regenerate processed datasets from raw CSVs:

```bash
python scripts/preprocess_data.py --dataset esol
python scripts/preprocess_data.py --dataset freesolv
```

## Run A Smoke Benchmark

Use smoke mode for a quick end-to-end check. It runs one ESOL Ridge descriptor random-split experiment. Write smoke outputs to temporary paths so the committed full benchmark artifacts are not overwritten:

```bash
python scripts/run_benchmark.py --smoke \
  --results-path /tmp/molecular_benchmark_results.csv \
  --predictions-path /tmp/molecular_predictions.csv
python scripts/summarize_results.py \
  --results-path /tmp/molecular_benchmark_results.csv \
  --summary-path /tmp/molecular_benchmark_summary.csv
```

## Run The Full Benchmark

The full MVP matrix has 300 experiments:

- 2 datasets: `esol`, `freesolv`
- 3 feature types: `descriptors`, `fingerprints`, `combined`
- 5 models: `ridge`, `lasso`, `random_forest`, `xgboost`, `mlp`
- 2 split types: `random`, `scaffold`
- 5 seeds: `0,1,2,3,4`

Preview the matrix:

```bash
python scripts/run_benchmark.py --dry-run
```

Run it and summarize results:

```bash
python scripts/run_benchmark.py
python scripts/summarize_results.py
```

Expected default outputs:

- `results/benchmark_results.csv`: one metrics row per experiment
- `results/predictions.csv`: validation and test prediction rows with SMILES, target, prediction, residual, and scaffold
- `results/benchmark_summary.csv`: mean and standard deviation by dataset, feature type, model, and split type

## Notebooks

Run the benchmark notebook:

```bash
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/02_benchmark.ipynb
```

Run the chemical-space analysis notebook:

```bash
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/03_analysis.ipynb
```

`notebooks/02_benchmark.ipynb` reads existing benchmark CSVs and generates predicted-vs-actual and residual plots. `notebooks/03_analysis.ipynb` generates Morgan fingerprint t-SNE chemical-space plots for random and scaffold splits.

## Reproducibility

Fixed seeds are used throughout:

- Benchmark seeds: `0,1,2,3,4`
- Default split seed for single experiments: caller-provided `seed`
- PyTorch MLP seed: passed through `create_model(..., seed=...)` and applied to Python, NumPy, and Torch
- Chemical-space t-SNE seed: `42`

Feature scaling is fit only inside model training pipelines for descriptor-like features. Morgan fingerprint features are not globally scaled.

The committed CSVs and figures were generated from the included processed datasets. Re-running the full benchmark may take several minutes because it includes XGBoost, random forests, and MLPs across all dataset/feature/split/seed combinations.

## Project Structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 02_benchmark.ipynb
│   └── 03_analysis.ipynb
├── results/
│   ├── benchmark_results.csv
│   ├── benchmark_summary.csv
│   ├── predictions.csv
│   └── figures/
├── scripts/
│   ├── preprocess_data.py
│   ├── run_benchmark.py
│   └── summarize_results.py
├── src/
│   ├── data_loader.py
│   ├── evaluate.py
│   ├── featurize.py
│   ├── models.py
│   ├── splits.py
│   ├── train.py
│   └── visualize.py
└── tests/
```

# Molecular Property Prediction Benchmark

Reproducible benchmark project for molecular property prediction, focused on comparing classical machine learning and neural network approaches across random and scaffold-aware validation.

This repository is currently initialized for the MVP implementation. Later tickets will add data loading, featurization, splitting, modeling, training, evaluation, and analysis notebooks.

## Project Structure

```text
.
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── src/
├── notebooks/
├── results/
│   └── figures/
└── tests/
```

## Setup

```bash
python -m pip install -r requirements.txt
python -m pytest
```

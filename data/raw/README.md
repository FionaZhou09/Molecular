# Raw Dataset Provenance

Retrieval date: 2026-07-01

This directory contains raw CSV snapshots for MOL-MVP-002A only. Filenames were normalized for stable downstream references, but source columns were preserved as downloaded.

## ESOL / Delaney

- Local file: `data/raw/esol.csv`
- Source URL: `https://deepchemdata.s3-us-west-1.amazonaws.com/datasets/delaney-processed.csv`
- Source name: DeepChem MoleculeNet Delaney/ESOL raw CSV
- Original filename: `delaney-processed.csv`
- Row count: 1128
- Observed columns:
  - `Compound ID`
  - `ESOL predicted log solubility in mols per litre`
  - `Minimum Degree`
  - `Molecular Weight`
  - `Number of H-Bond Donors`
  - `Number of Rings`
  - `Number of Rotatable Bonds`
  - `Polar Surface Area`
  - `measured log solubility in mols per litre`
  - `smiles`
- Observed SMILES column: `smiles`
- Observed target column: `measured log solubility in mols per litre`
- Filename-only normalization: `delaney-processed.csv` was saved as `esol.csv`.
- SHA256: `8c06a76f0c6487d29ab0f903e6a7a7139f189ab3c1178f159c8be8964602f189`

## FreeSolv

- Local file: `data/raw/freesolv.csv`
- Source URL: `https://deepchemdata.s3.us-west-1.amazonaws.com/datasets/freesolv.csv.gz`
- Source name: DeepChem MoleculeNet FreeSolv raw CSV gzip fallback
- Source note: the MoleculeNet publish zip URL `https://s3-us-west-1.amazonaws.com/deepchem.io/datasets/molnet_publish/FreeSolv.zip` returned HTTP 403 during retrieval, so the DeepChem MoleculeNet loader URL was used.
- Original filename: `freesolv.csv.gz` containing `freesolv.csv`
- Row count: 642
- Observed columns:
  - `smiles`
  - `y`
- Observed SMILES column: `smiles`
- Observed target column: `y`
- Filename-only normalization: `freesolv.csv` from the gzip archive was saved as `freesolv.csv`.
- SHA256: `53df8c32125f7a8e85bf6c1c5fdda3292e2653ec419dd95a8d4414ac25291283`

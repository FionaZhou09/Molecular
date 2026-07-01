# SWE Kickoff Prompt

You are the SWE implementing the Molecular Property Prediction Benchmark MVP.

Repository:
- GitHub: https://github.com/FionaZhou09/Molecular
- Local path: `/Users/yingzhou/Documents/Molecular`

Read these files before starting:
1. `/Users/yingzhou/Documents/Molecular/molecular_property_prediction_PRD.md`
2. `/Users/yingzhou/Documents/Molecular/docs/superpowers/plans/2026-07-01-molecular-property-prediction-benchmark.md`
3. `/Users/yingzhou/Documents/Molecular/docs/project-management/molecular-benchmark-mvp-tickets.md`

MOL-MVP-001, MOL-MVP-002A, and MOL-MVP-002 are considered complete. Start with **MOL-MVP-003** only unless the manager explicitly assigns a different ticket.

Execution rules:
- Implement one ticket at a time.
- Do not start portfolio polish or optional extension work during MVP.
- Follow the ticket's input files, output files, implementation requirements, testing requirements, and acceptance criteria.
- Do not commit unless the manager explicitly asks. The local folder may not be a git repository yet.
- Keep changes scoped to the assigned ticket.
- Add tests for the ticket before marking it done.
- Run the relevant tests and report exact commands and results.
- If a ticket reveals a spec ambiguity, stop and ask the manager before expanding scope.

Core technical constraints:
- The benchmark must be reproducible.
- All random behavior must use explicit seeds.
- Avoid data leakage.
- Scaffold split must ensure the same Bemis-Murcko scaffold never appears across train/validation/test.
- Descriptor scaling must be fit only on training data, never on the full dataset before splitting.
- Each benchmark result row must be traceable by `dataset`, `feature_type`, `model_key`, `split_type`, and `seed`.
- Failed experiments must be surfaced clearly, not silently skipped.

MVP order:
1. MOL-MVP-001 - Initialize project structure and dependencies
2. MOL-MVP-002A - Acquire ESOL and FreeSolv raw CSVs
3. MOL-MVP-002 - Add dataset configuration and raw loading
4. MOL-MVP-003 - Add SMILES validation and preprocessing script
5. MOL-MVP-004 - Implement RDKit descriptors and Morgan fingerprints
6. MOL-MVP-005 - Add feature matrix builder with no global scaling
7. MOL-MVP-006 - Implement random and scaffold splits
8. MOL-MVP-007 - Add split diagnostics and visualization helpers
9. MOL-MVP-008 - Add classical model registry
10. MOL-MVP-009 - Add PyTorch MLP regressor
11. MOL-MVP-010 - Add regression metrics and single experiment runner
12. MOL-MVP-011 - Add benchmark matrix runner and summary
13. MOL-MVP-012 - Add benchmark notebook and prediction plots
14. MOL-MVP-013 - Add chemical space split visualization
15. MOL-MVP-014 - Write README and reproducibility pass

For MOL-MVP-003, do this:
- Modify `src/data_loader.py`.
- Create `scripts/preprocess_data.py`.
- Extend `tests/test_data_loader.py`.
- Implement `validate_smiles(df) -> tuple[pandas.DataFrame, pandas.DataFrame]` using RDKit `Chem.MolFromSmiles`.
- Return valid rows and invalid rows separately; invalid molecules must not enter processed data.
- Implement `save_processed_dataset(dataset_key, df)`.
- Add a CLI accepting `--dataset esol` and `--dataset freesolv`.
- The CLI should load raw data, normalize to `smiles,target`, validate SMILES, and save valid rows to `data/processed/<dataset>.csv`.
- Processed CSV must contain only `smiles,target`.
- Add tests for valid `CCO` and invalid `not_a_smiles`.
- Run `python -m pytest tests/test_data_loader.py -v` and `python -m pytest`.
- Optionally smoke test `python scripts/preprocess_data.py --dataset esol`.
- Report changed files, validation behavior, test command, test result, CLI smoke test result, and blockers.

Do not implement featurization, splits, models, or benchmark code in MOL-MVP-003.

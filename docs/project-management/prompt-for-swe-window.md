# Prompt For SWE Window

你现在是这个项目的 SWE。请在新的工作窗口里开始执行下一个 MVP ticket。

项目路径：
`/Users/yingzhou/Documents/Molecular`

GitHub repo：
`https://github.com/FionaZhou09/Molecular`

请先阅读这些文件：

1. `/Users/yingzhou/Documents/Molecular/molecular_property_prediction_PRD.md`
2. `/Users/yingzhou/Documents/Molecular/docs/superpowers/plans/2026-07-01-molecular-property-prediction-benchmark.md`
3. `/Users/yingzhou/Documents/Molecular/docs/project-management/molecular-benchmark-mvp-tickets.md`

当前 manager 状态：

- MOL-MVP-001 已完成并通过 review。
- MOL-MVP-002A 已完成并通过 review；raw CSVs 已在 `data/raw/`。
- MOL-MVP-002 已完成并通过 review；`src/config.py` 和 `src/data_loader.py` 已存在。
- MOL-MVP-003 已完成并通过 review；processed CSVs 已在 `data/processed/`。
- MOL-MVP-004 已完成并通过 review；`src/featurize.py` 已有 descriptors 和 Morgan fingerprints。
- MOL-MVP-005 已完成并通过 review；`build_feature_matrix` 已支持 descriptors/fingerprints/combined，且没有 global scaling。
- MOL-MVP-006 已完成并通过 review；`src/splits.py` 已有 random/scaffold split。
- MOL-MVP-007 已完成并通过 review；split diagnostics 和 scaffold count plotting helper 已存在。
- MOL-MVP-008 已完成并通过 review；`src/models.py` 已有 classical model registry。
- MOL-MVP-009 已完成并通过 review；`src/models.py` 已有 PyTorch MLP regressor。
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-010 - Add Regression Metrics And Single Experiment Runner**。

不要做后续 ticket。不要实现 full benchmark matrix runner、summary scripts、notebooks 或 visual analysis。

MOL-MVP-010 要求：

- Create `src/evaluate.py`.
- Create `src/train.py`.
- Create tests:
  - `tests/test_evaluate.py`
  - `tests/test_train.py`
- Implement RMSE, MAE, and R2 metrics.
- Implement `evaluate_regression(y_true, y_pred) -> dict`.
- Metrics must match scikit-learn definitions.
- Implement `run_experiment(dataset_key, feature_type, model_key, split_type, seed)`.
- `run_experiment` should:
  - load processed data from `data/processed/<dataset>.csv`
  - create random or scaffold split
  - build features using existing `build_feature_matrix`
  - train model using existing `create_model`
  - evaluate validation and test predictions
  - return a flat result dictionary
  - also return or expose a prediction table for validation/test rows
- Result dictionary must include at least:
  - `dataset`
  - `feature_type`
  - `model_key`
  - `split_type`
  - `seed`
  - validation metrics
  - test metrics
  - split sizes
- Prediction table must include at least:
  - `dataset`
  - `feature_type`
  - `model_key`
  - `split_type`
  - `seed`
  - `split`
  - `smiles`
  - `target`
  - `prediction`
  - `residual`
  - `scaffold`
- At least one ESOL Ridge descriptor experiment should run end-to-end.
- Keep this ticket focused on a single experiment runner. Full grid benchmark belongs to MOL-MVP-011.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/data_loader.py`、`src/featurize.py`、`src/splits.py`、`src/models.py`，沿用 existing APIs。
3. 实现 MOL-MVP-010。
4. 运行：

```bash
python -m pytest tests/test_evaluate.py tests/test_train.py -v
```

5. 运行完整测试：

```bash
python -m pytest
```

6. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- metrics 和 `run_experiment` 返回结构。
- prediction table schema。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-011。

验收标准：

- `pytest tests/test_evaluate.py tests/test_train.py -v` passes。
- `python -m pytest` passes。
- RMSE、MAE、R2 match scikit-learn definitions。
- One ESOL Ridge descriptor experiment runs end-to-end。
- Result dict can be appended directly to a pandas DataFrame。
- Prediction table includes validation/test rows and required traceability fields。
- 没有实现超出 MOL-MVP-010 范围的业务代码。

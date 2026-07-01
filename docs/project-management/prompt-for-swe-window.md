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
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-008 - Add Classical Model Registry**。

不要做后续 ticket。不要实现 PyTorch MLP、training runner、benchmark 或 notebooks。

MOL-MVP-008 要求：

- Create `src/models.py`.
- Create `tests/test_models.py`.
- Implement a model factory for classical regression models:
  - `ridge`
  - `lasso`
  - `random_forest`
  - `xgboost`
- Required interface:
  - `create_model(model_key, feature_type, seed, **kwargs)`
- All returned models must expose scikit-learn-compatible:
  - `fit(X_train, y_train)`
  - `predict(X_test)`
- If `feature_type` is `descriptors` or `combined`, wrap estimator in a `Pipeline` with `StandardScaler` followed by the model.
- If `feature_type` is `fingerprints`, do **not** include `StandardScaler`.
- Scaling must happen only inside model `.fit(X_train, y_train)`, never globally in featurization.
- All applicable models should receive `seed` / `random_state`.
- Add tests that each model can fit and predict on a tiny synthetic regression dataset.
- Add tests that prediction shape is `(n_samples,)`.
- Add tests verifying descriptors/combined models include train-time scaling and fingerprint-only models do not.
- Do not implement `mlp` yet. That belongs to MOL-MVP-009.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/featurize.py`，确认 feature_type names: `descriptors`、`fingerprints`、`combined`。
3. 实现 MOL-MVP-008。
4. 运行：

```bash
python -m pytest tests/test_models.py -v
```

5. 运行完整测试：

```bash
python -m pytest
```

6. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- model registry keys 和 `create_model` interface。
- 哪些 feature_type 会加 scaler，哪些不会。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-009。

验收标准：

- `pytest tests/test_models.py -v` passes。
- `python -m pytest` passes。
- Registry supports `ridge`、`lasso`、`random_forest`、`xgboost`。
- All models expose `fit` and `predict`。
- Prediction shape is `(n_samples,)`。
- Descriptors/combined models include train-time `StandardScaler`。
- Fingerprint-only models do not include `StandardScaler`。
- 没有实现超出 MOL-MVP-008 范围的业务代码。

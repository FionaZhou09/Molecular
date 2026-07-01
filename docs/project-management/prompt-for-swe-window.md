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
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-009 - Add PyTorch MLP Regressor**。

不要做后续 ticket。不要实现 training runner、benchmark 或 notebooks。

MOL-MVP-009 要求：

- Modify `src/models.py`.
- Extend `tests/test_models.py`.
- Implement `MLPRegressorTorch`.
- MLP should support:
  - hidden layers
  - dropout
  - batch size
  - epochs
  - learning rate
  - seed
  - early stopping
- MLP must expose the same interface as classical models:
  - `fit(X_train, y_train)`
  - `predict(X_test)`
- Add `mlp` to `create_model(model_key, feature_type, seed, **kwargs)`.
- Keep CPU training working on small datasets.
- Add deterministic seed handling for Python/numpy/torch where relevant.
- Add smoke test that MLP trains on a tiny synthetic regression dataset.
- Add test that prediction shape is `(n_samples,)`.
- Add test or assertion that training reduces loss or reaches a lower final loss than initial loss on the tiny synthetic dataset.
- Preserve existing classical model behavior and scaling rules.
- Do not implement experiment runner yet. That belongs to MOL-MVP-010.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/models.py` 和 `tests/test_models.py`，沿用 existing registry style。
3. 实现 MOL-MVP-009。
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
- `MLPRegressorTorch` 的主要参数和 fit/predict interface。
- seed 和 early stopping 如何处理。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-010。

验收标准：

- `pytest tests/test_models.py -v` passes。
- `python -m pytest` passes。
- Registry supports `mlp` in addition to classical models。
- MLP exposes `fit` and `predict`。
- MLP prediction shape is `(n_samples,)`。
- CPU smoke training works on a tiny dataset。
- Existing classical model tests continue to pass。
- 没有实现超出 MOL-MVP-009 范围的业务代码。

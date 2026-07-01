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
- MOL-MVP-010 已完成并通过 review；`src/evaluate.py` 和 `src/train.py` 已有 metrics 与 single experiment runner。
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-011 - Add Benchmark Matrix Runner And Summary**。

不要做后续 ticket。不要实现 notebooks、prediction plots、chemical space visualization 或 README polish。

MOL-MVP-011 要求：

- Modify `src/train.py` if needed.
- Create `scripts/run_benchmark.py`.
- Create `scripts/summarize_results.py`.
- Add or extend tests, preferably `tests/test_train.py`, for benchmark matrix smoke/dry-run and summary aggregation.
- Full benchmark matrix should support:
  - datasets: `esol`, `freesolv`
  - feature types: `descriptors`, `fingerprints`, `combined`
  - models: `ridge`, `lasso`, `random_forest`, `xgboost`, `mlp`
  - split types: `random`, `scaffold`
  - seeds: `0`, `1`, `2`, `3`, `4`
- Output files:
  - `results/benchmark_results.csv`
  - `results/benchmark_summary.csv`
  - `results/predictions.csv`
- `benchmark_results.csv` should have one row per dataset-feature-model-split-seed experiment.
- `predictions.csv` should append validation/test prediction rows from `run_experiment`.
- `benchmark_summary.csv` should group by dataset, feature type, model, and split type.
- Summary should compute mean and standard deviation for RMSE, MAE, and R2 across seeds.
- Failed experiments must be surfaced clearly, not silently skipped.
- Add a smoke mode / dry-run option so tests do not run the full expensive matrix.
- Do not require full five-seed benchmark execution inside unit tests.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/train.py` 和 existing `run_experiment` return structure。
3. 实现 MOL-MVP-011。
4. 运行：

```bash
python -m pytest tests/test_train.py -v
```

5. 运行完整测试：

```bash
python -m pytest
```

6. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- benchmark runner 参数/矩阵。
- summary aggregation schema。
- smoke/dry-run 用法。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-012 和/或 MOL-MVP-013。

验收标准：

- `pytest tests/test_train.py -v` passes。
- `python -m pytest` passes。
- Benchmark runner can write `results/benchmark_results.csv`。
- Benchmark runner can write `results/predictions.csv`。
- Summary script can write `results/benchmark_summary.csv`。
- Summary supports direct random-vs-scaffold comparison by grouped mean/std。
- Smoke/dry-run test avoids full expensive benchmark。
- 没有实现超出 MOL-MVP-011 范围的业务代码。

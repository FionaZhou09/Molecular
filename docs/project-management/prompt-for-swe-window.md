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
- MOL-MVP-011 已完成并通过 review；benchmark results、predictions、summary CSV 已在 `results/`。
- MOL-MVP-012 已完成并通过 review；`notebooks/02_benchmark.ipynb` 和 prediction/residual figures 已存在。
- MOL-MVP-013 已完成并通过 review；`notebooks/03_analysis.ipynb` 和 chemical space figures 已存在。
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-014 - Write README And Reproducibility Pass**。

不要做 portfolio polish tickets、optional tickets、SHAP、feature importance、error analysis、GNN 或 classification extension。

MOL-MVP-014 要求：

- Modify `README.md`.
- Modify `requirements.txt` if needed.
- Modify `.gitignore` if needed.
- Explain project motivation and key methodological point: random split can overestimate generalization compared with scaffold split.
- Document setup commands.
- Document preprocessing commands.
- Document benchmark runner and summary commands.
- Include or reference result summary table.
- Include or reference key figures:
  - predicted-vs-actual plots
  - residual plots
  - chemical space plots
- Document fixed random seeds and reproducibility assumptions.
- Pin dependency versions after verifying the current environment.
- Ensure `.gitignore` covers caches, notebook checkpoints, model artifacts, and other generated clutter.
- Do not remove committed benchmark artifacts unless manager explicitly asks.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. Read current README, requirements, scripts, and results summary.
3. Implement MOL-MVP-014.
4. 运行：

```bash
python -m pytest
```

5. Run at least one documented smoke command if feasible, such as:

```bash
python scripts/run_benchmark.py --smoke
python scripts/summarize_results.py
```

6. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- README 覆盖了哪些 commands/results/figures。
- requirements 是否 pin versions。
- `.gitignore` 是否更新。
- 运行了什么测试命令。
- 测试结果是什么。
- 运行了什么 documented smoke command。
- 是否有 blocker。
- 下一步建议是否进入 portfolio polish 或停止 MVP。

验收标准：

- `python -m pytest` passes。
- README lets a third-party reviewer understand the project in under 10 minutes。
- README commands are copy-paste runnable from a fresh clone/environment。
- README explains random vs scaffold split methodology。
- README references key result files and figures。
- Random seeds are documented。
- Dependencies are pinned or reproducibility caveats are clearly documented。
- 没有实现超出 MOL-MVP-014 范围的业务代码。

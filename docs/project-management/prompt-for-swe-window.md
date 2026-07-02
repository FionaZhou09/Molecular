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
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-013 - Add Chemical Space Split Visualization**。

不要做后续 ticket。不要实现 README polish、SHAP、feature importance 或 error analysis。

MOL-MVP-013 要求：

- Modify `src/visualize.py` as needed.
- Create or update `notebooks/03_analysis.ipynb`.
- Use existing outputs:
  - `data/processed/esol.csv`
  - `data/processed/freesolv.csv`
- Generate Morgan fingerprints.
- Reduce fingerprints to 2D using UMAP or t-SNE.
- Color points by train/validation/test assignment.
- Compare random split and scaffold split visually.
- At minimum, output chemical space figures for ESOL and FreeSolv.
- Use output filenames like:
  - `results/figures/chemical_space_<dataset>_<split>.png`
- Fix the dimensionality-reduction seed.
- Figure labels/titles must include dataset and split type.
- Notebook should run top-to-bottom.
- Do not implement SHAP or error analysis; those are polish tickets.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/featurize.py` 和 `src/splits.py`，复用 Morgan fingerprints 和 split helpers。
3. 实现 MOL-MVP-013。
4. 运行：

```bash
python -m pytest
```

5. 验证 notebook 或 figure generation；确认 chemical space figure files exist and are non-empty。

6. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- chemical space notebook 生成了哪些图。
- 使用了哪些 dataset/split combinations。
- dimensionality reduction 使用的是 UMAP 还是 t-SNE，以及 seed。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-014。

验收标准：

- `python -m pytest` passes。
- `notebooks/03_analysis.ipynb` exists and can run top-to-bottom。
- Chemical space plots compare random and scaffold split visually。
- At least ESOL and FreeSolv each have chemical space figures。
- Figure files exist and are non-empty。
- 没有实现超出 MOL-MVP-013 范围的业务代码。

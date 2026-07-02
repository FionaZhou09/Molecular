# Prompt For Final Reviewer Window

你现在是这个项目的 Final Reviewer / ML Benchmark Reviewer / Portfolio Reviewer。

请在新的审核窗口中 review 整个项目。不要写代码，不要修改文件。你的任务是判断这个 MVP 是否已经达到“可以放到 GitHub / 简历 / 作品集展示”的标准，并给出具体、可执行的改进建议。

项目路径：
`/Users/yingzhou/Documents/Molecular`

GitHub repo：
`https://github.com/FionaZhou09/Molecular`

请先阅读：

1. `/Users/yingzhou/Documents/Molecular/README.md`
2. `/Users/yingzhou/Documents/Molecular/molecular_property_prediction_PRD.md`
3. `/Users/yingzhou/Documents/Molecular/docs/project-management/molecular-benchmark-mvp-tickets.md`

然后重点检查这些代码与结果：

- `src/data_loader.py`
- `src/featurize.py`
- `src/splits.py`
- `src/models.py`
- `src/evaluate.py`
- `src/train.py`
- `src/visualize.py`
- `scripts/preprocess_data.py`
- `scripts/run_benchmark.py`
- `scripts/summarize_results.py`
- `results/benchmark_results.csv`
- `results/benchmark_summary.csv`
- `results/predictions.csv`
- `notebooks/02_benchmark.ipynb`
- `notebooks/03_analysis.ipynb`

请运行或检查：

```bash
python -m pytest
python scripts/run_benchmark.py --smoke \
  --results-path /tmp/molecular_benchmark_results.csv \
  --predictions-path /tmp/molecular_predictions.csv
python scripts/summarize_results.py \
  --results-path /tmp/molecular_benchmark_results.csv \
  --summary-path /tmp/molecular_benchmark_summary.csv
```

如果你无法运行某个命令，请说明原因，并继续做静态 review。

## Review 重点

请从以下角度审核：

1. **PRD compliance**
   - 是否实现 ESOL + FreeSolv。
   - 是否实现 descriptors、Morgan fingerprints、combined features。
   - 是否实现 random split 和 scaffold split。
   - 是否实现 classical ML + PyTorch MLP。
   - 是否实现 RMSE、MAE、R2。
   - 是否有 benchmark results、figures、notebooks、README。

2. **Methodology correctness**
   - 是否避免 data leakage。
   - descriptor scaling 是否只在 train 上 fit。
   - Morgan fingerprints 是否没有被错误 scaling。
   - scaffold split 是否保证同一 Bemis-Murcko scaffold 不跨 train/validation/test。
   - random seed 是否固定且可追溯。
   - benchmark row 是否可追溯 dataset / feature_type / model_key / split_type / seed。

3. **Reproducibility**
   - README commands 是否可执行。
   - dependencies 是否 pin 或有清楚 caveat。
   - raw/processed data provenance 是否清楚。
   - results 是否能从 scripts 复现。
   - notebooks 是否能 top-to-bottom 执行。

4. **Code quality**
   - 模块边界是否清晰。
   - API 是否一致。
   - tests 是否覆盖关键风险。
   - 是否存在过度实现、重复逻辑、隐藏复杂度。
   - 是否有明显 bug、fragile behavior 或性能风险。

5. **Portfolio quality**
   - README 是否 10 分钟内讲清楚项目价值。
   - random vs scaffold 的核心结论是否突出。
   - 图表是否足够支持结论。
   - 这个项目是否适合放入简历。
   - 面试官可能会追问什么。

## 请输出 Markdown Review

请按这个结构输出：

## Overall Verdict

选择一个：

- Ready For Portfolio
- Ready With Minor Fixes
- Needs More Work

## Blocking Issues

如果有阻塞展示/复现/方法论正确性的问题，请列出。没有就写 `None`。

## High Priority Fixes

列出建议在展示前优先修的问题。

## Medium / Nice-To-Have Improvements

列出不阻塞，但能提升作品集质量的问题。

## Methodology Review

明确评价：

- data leakage
- scaffold split
- scaling
- random seeds
- result traceability

## Reproducibility Review

明确评价 README、requirements、scripts、notebooks、results artifacts。

## Portfolio Story Review

评价这个项目作为简历/作品集项目是否有说服力，并指出 README 或图表叙事上的改进点。

## Suggested Next Tickets

请建议下一步 3-5 个 ticket，按优先级排序。可以包括：

- EDA notebook
- README polish
- feature importance
- SHAP
- error analysis
- candidate ranking
- CI / GitHub Actions
- small refactors

## Final Recommendation

明确回答：

- 这个项目现在能不能放到 GitHub 展示？
- 需要先修哪些问题？
- 是否建议进入 portfolio polish？

请保持具体、直接、可执行。不要泛泛表扬。

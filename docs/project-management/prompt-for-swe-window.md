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
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-007 - Add Split Diagnostics And Visualization Helpers**。

不要做后续 ticket。不要实现 models、training、benchmark 或 notebooks。

MOL-MVP-007 要求：

- Modify `src/splits.py`.
- Create `src/visualize.py`.
- Extend `tests/test_splits.py`.
- Implement split size summaries for train/validation/test.
- Implement scaffold overlap diagnostics.
- Diagnostics should clearly show zero scaffold overlap for scaffold split.
- Diagnostics should return DataFrame or dictionary outputs that can be exported later.
- Add a plotting helper for train/validation/test scaffold counts in `src/visualize.py`.
- Keep plotting helper lightweight and matplotlib-based.
- Do not create notebooks yet.
- Do not implement model or benchmark logic.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/splits.py` 和 `tests/test_splits.py`，沿用现有 split return structure。
3. 实现 MOL-MVP-007。
4. 运行：

```bash
python -m pytest tests/test_splits.py -v
```

5. 运行完整测试：

```bash
python -m pytest
```

6. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- diagnostics 函数返回结构。
- scaffold overlap 如何表示 zero leakage。
- visualization helper 的输入/输出。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-008。

验收标准：

- `pytest tests/test_splits.py -v` passes。
- `python -m pytest` passes。
- Split size summaries report train/validation/test sizes。
- Scaffold diagnostics report zero overlap for scaffold split。
- Diagnostics can be exported as DataFrame/dict。
- Plotting helper exists for train/validation/test scaffold counts。
- 没有实现超出 MOL-MVP-007 范围的业务代码。

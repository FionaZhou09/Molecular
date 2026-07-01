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
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-006 - Implement Random And Scaffold Splits**。

不要做后续 ticket。不要实现 split diagnostics、models、training、benchmark 或 notebooks。

MOL-MVP-006 要求：

- Create `src/splits.py`.
- Create `tests/test_splits.py`.
- Implement `random_split(df, train_size=0.8, val_size=0.1, test_size=0.1, seed=42)`.
- `random_split` should return train, validation, and test index arrays.
- Splits must be deterministic for the same seed.
- Splits must be non-overlapping and cover all rows exactly once.
- Implement `compute_scaffold(smiles) -> str` using RDKit Bemis-Murcko scaffolds.
- Implement `scaffold_split(df, train_size=0.8, val_size=0.1, test_size=0.1, seed=42)`.
- `scaffold_split` should return train, validation, and test index arrays.
- Molecules with the same scaffold must never cross train/validation/test.
- Split sizes should be close to requested ratios, but scaffold integrity is more important than exact ratios.
- Add tests with duplicated scaffolds to prove scaffold groups do not cross sets.
- Invalid SMILES handling should fail clearly or be consistent with existing RDKit validation behavior.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/data_loader.py` / `src/featurize.py` style，沿用简单 function-based module pattern。
3. 实现 MOL-MVP-006。
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
- random split 和 scaffold split 的返回结构。
- scaffold 不跨集合的测试方式。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-007。

验收标准：

- `pytest tests/test_splits.py -v` passes。
- `python -m pytest` passes。
- Random split covers all rows exactly once。
- Same seed produces same random split。
- Scaffold split covers all rows exactly once。
- No scaffold appears in more than one split。
- 没有实现超出 MOL-MVP-006 范围的业务代码。

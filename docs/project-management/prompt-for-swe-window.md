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
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-003 - Add SMILES Validation And Preprocessing Script**。

不要做后续 ticket。不要实现 featurization、splits、models、training、benchmark 或 notebooks。

MOL-MVP-003 要求：

- Modify `src/data_loader.py`.
- Create `scripts/preprocess_data.py`.
- Extend `tests/test_data_loader.py`.
- Implement `validate_smiles(df) -> tuple[pandas.DataFrame, pandas.DataFrame]`.
- Use RDKit `Chem.MolFromSmiles`.
- Return valid rows and invalid rows separately.
- Invalid molecules must be excluded from processed output but remain inspectable in the invalid return value.
- Add tests with:
  - valid example: `CCO`
  - invalid example: `not_a_smiles`
- Implement `save_processed_dataset(dataset_key, df)`.
- Add CLI script accepting:
  - `--dataset esol`
  - `--dataset freesolv`
- The preprocessing flow should:
  - load raw dataset using existing config/loader
  - normalize to `smiles,target`
  - validate SMILES
  - save valid rows to `data/processed/<dataset>.csv`
- Processed CSV must contain only:
  - `smiles`
  - `target`

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/config.py` 和 `src/data_loader.py`，沿用现有 patterns。
3. 实现 MOL-MVP-003。
4. 运行：

```bash
python -m pytest tests/test_data_loader.py -v
```

5. 运行完整测试：

```bash
python -m pytest
```

6. 可用一个 dataset 做 CLI smoke test，例如：

```bash
python scripts/preprocess_data.py --dataset esol
```

7. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- RDKit validation 如何处理 valid/invalid rows。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否运行了 preprocessing CLI smoke test。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-004。

验收标准：

- `pytest tests/test_data_loader.py -v` passes。
- `python -m pytest` passes。
- `validate_smiles` excludes invalid molecules from valid output。
- Invalid rows can still be inspected separately。
- `python scripts/preprocess_data.py --dataset esol` writes `data/processed/esol.csv`。
- Processed CSV contains only `smiles,target`。
- 没有实现超出 MOL-MVP-003 范围的业务代码。

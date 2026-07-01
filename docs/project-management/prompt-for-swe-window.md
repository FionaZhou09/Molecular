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

- MOL-MVP-001 已由 boss review 认为基本完成。
- MOL-MVP-002A 已完成并通过 review；raw CSVs 已在 `data/raw/`。
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-002 - Add Dataset Configuration And Raw Loading**。

不要做后续 ticket。不要实现 SMILES validation、featurization、splits、models、training、benchmark 或 notebooks。

MOL-MVP-002 要求：

- Create `src/config.py`.
- Create `src/data_loader.py`.
- Create tests:
  - `tests/test_config.py`
  - `tests/test_data_loader.py`
- Register dataset metadata for exactly the MVP datasets:
  - `esol`
  - `freesolv`
- Metadata should include:
  - dataset display name
  - raw CSV path
  - processed CSV path
  - source URL or source note from `data/raw/README.md`
  - expected row count
  - SMILES column
  - target column
  - `task_type="regression"`
- Use actual raw columns:
  - ESOL SMILES column: `smiles`
  - ESOL target column: `measured log solubility in mols per litre`
  - FreeSolv SMILES column: `smiles`
  - FreeSolv target column: `y`
- Implement:
  - `load_raw_dataset(dataset_key: str) -> pandas.DataFrame`
  - `normalize_dataset(df, smiles_col, target_col) -> pandas.DataFrame`
- `normalize_dataset` must return exactly two columns:
  - `smiles`
  - `target`
- Drop rows with missing SMILES or target.
- Do not perform RDKit SMILES validation yet. That belongs to MOL-MVP-003.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `data/raw/README.md`，确认 raw column names。
3. 实现 MOL-MVP-002。
4. 运行：

```bash
python -m pytest tests/test_config.py tests/test_data_loader.py -v
```

也可以运行完整测试：

```bash
python -m pytest
```

5. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- dataset metadata 的 key 和 source columns。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-003。

验收标准：

- `pytest tests/test_config.py tests/test_data_loader.py -v` passes。
- ESOL 和 FreeSolv 可以通过 stable keys `esol`、`freesolv` 引用。
- 两个 dataset 都标记为 regression。
- `load_raw_dataset` 可以读取 `data/raw/esol.csv` 和 `data/raw/freesolv.csv`。
- `normalize_dataset` 输出列严格为 `smiles,target`。
- missing SMILES 或 target rows 被 deterministic drop。
- 没有实现超出 MOL-MVP-002 范围的业务代码。

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
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-004 - Implement RDKit Descriptors And Morgan Fingerprints**。

不要做后续 ticket。不要实现 feature matrix builder、splits、models、training、benchmark 或 notebooks。

MOL-MVP-004 要求：

- Create `src/featurize.py`.
- Create `tests/test_featurize.py`.
- Implement `compute_descriptors(smiles_list) -> pandas.DataFrame`.
- Include 20-30 stable RDKit descriptors covering at least:
  - molecular weight
  - LogP
  - TPSA
  - HBD
  - HBA
  - rotatable bonds
  - ring counts
  - aromatic rings
  - formal charge
  - FractionCSP3
  - molar refractivity
- Return one descriptor row per input SMILES.
- Descriptor column names must be stable and human-readable.
- Invalid SMILES must not be silently featurized; raise a clear error or otherwise fail explicitly.
- Implement `compute_morgan_fingerprints(smiles_list, radius=2, n_bits=2048) -> numpy.ndarray`.
- Support `n_bits=512`, `1024`, and `2048`.
- Fingerprint output shape must be `(n_molecules, n_bits)`.
- Fingerprint values must be binary `0` or `1`.
- Do not implement `build_feature_matrix` yet. That belongs to MOL-MVP-005.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/data_loader.py`，确认 processed data shape，但不要改 loader 除非测试需要。
3. 实现 MOL-MVP-004。
4. 运行：

```bash
python -m pytest tests/test_featurize.py -v
```

5. 运行完整测试：

```bash
python -m pytest
```

6. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- descriptor 列表和 fingerprint 参数支持。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-005。

验收标准：

- `pytest tests/test_featurize.py -v` passes。
- `python -m pytest` passes。
- Descriptor DataFrame has stable column names。
- Descriptor values are numeric and finite for `CCO`, `c1ccccc1`, and `CC(=O)O`。
- Invalid SMILES are not silently featurized。
- Fingerprints have shape `(n_molecules, n_bits)`。
- Fingerprints contain only `0` or `1`。
- 没有实现超出 MOL-MVP-004 范围的业务代码。

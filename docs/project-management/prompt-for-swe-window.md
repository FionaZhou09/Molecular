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
- 当前目录已连接 GitHub，但不要 commit，除非 manager 明确要求。

你的任务：

只执行 **MOL-MVP-005 - Add Feature Matrix Builder With No Global Scaling**。

不要做后续 ticket。不要实现 splits、models、training、benchmark 或 notebooks。

MOL-MVP-005 要求：

- Modify `src/featurize.py`.
- Extend `tests/test_featurize.py`.
- Implement `build_feature_matrix(df, feature_type)` with feature types:
  - `descriptors`
  - `fingerprints`
  - `combined`
- Input `df` should contain at least a `smiles` column.
- Return feature matrix and feature names.
- For `descriptors`, return descriptor features and descriptor names.
- For `fingerprints`, return Morgan fingerprint matrix and bit feature names such as `morgan_0`, `morgan_1`, ...
- For `combined`, concatenate descriptors and fingerprints in a stable order and return combined feature names.
- Do **not** fit or apply `StandardScaler` in this function.
- Descriptor scaling must remain train-only and be handled later in model/train workflows.
- Invalid or unsupported `feature_type` should raise a clear `ValueError`.

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 阅读 `src/featurize.py` 和现有 tests，沿用已有 featurizer style。
3. 实现 MOL-MVP-005。
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
- `build_feature_matrix` 支持的 feature types 和返回结构。
- 如何保证没有 global scaling。
- 运行了什么测试命令。
- 测试结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-006。

验收标准：

- `pytest tests/test_featurize.py -v` passes。
- `python -m pytest` passes。
- `descriptors`、`fingerprints`、`combined` 三种 feature modes 都支持。
- Returned feature names match matrix dimensions。
- `combined` 维度等于 descriptor + fingerprint 维度。
- `build_feature_matrix` 没有 import、fit 或 apply `StandardScaler`。
- 没有实现超出 MOL-MVP-005 范围的业务代码。

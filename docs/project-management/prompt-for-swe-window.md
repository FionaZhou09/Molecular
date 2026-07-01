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
- 当前目录可能还不是 git repo，所以不要 commit，除非 manager 明确要求。
- 下一步不要直接做 loader；先解决 raw dataset availability。

你的任务：

只执行 **MOL-MVP-002A - Acquire ESOL And FreeSolv Raw CSVs**。

不要做后续 ticket。不要实现 data loading、SMILES validation、featurization、splits、models、training、benchmark 或 notebooks。

MOL-MVP-002A 要求：

- Acquire ESOL/Delaney and FreeSolv raw CSVs from a documented source.
- Preferred source is official MoleculeNet data.
- Acceptable fallback is DeepChem's MoleculeNet loader or another clearly documented mirror if official download is unavailable.
- Save normalized filenames:
  - `data/raw/esol.csv`
  - `data/raw/freesolv.csv`
- Preserve the original source columns inside those raw CSVs. Do not normalize to `smiles,target` yet; that belongs to MOL-MVP-002.
- Create or update `data/raw/README.md` documenting:
  - source URL or package/source name
  - retrieval date
  - original filename if different
  - row count
  - observed SMILES column
  - observed target column
  - any filename-only normalization
- Expected source columns are typically:
  - ESOL: `smiles` and `measured log solubility in mols per litre`
  - FreeSolv: `mol` and `y`

执行流程：

1. 检查当前 repo 状态和已有文件。
2. 如果当前 Python environment 缺少 pandas 或数据获取所需依赖，先报告；只安装依赖如果你确认当前 window 允许安装。
3. 实现 MOL-MVP-002A。
4. 用一个轻量命令验证两个 CSV 可被 pandas 读取、非空、且包含预期 source columns。
5. 可以运行：

```bash
python -m pytest
```

如果 pytest 因为没有测试而返回 no tests collected，请说明这是当前阶段可接受状态；如果有 import/syntax/setup error，需要修复。

6. 不要 commit，除非我明确要求。

完成后请汇报：

- 你创建或修改了哪些文件。
- 数据来源是什么。
- ESOL 和 FreeSolv 的 row count 分别是多少。
- 你运行了什么验证命令。
- 验证结果是什么。
- 是否有 blocker。
- 下一步建议是否进入 MOL-MVP-002。

验收标准：

- `data/raw/esol.csv` 存在且可读取。
- `data/raw/freesolv.csv` 存在且可读取。
- `data/raw/README.md` 记录 source provenance。
- Row counts roughly match MoleculeNet expected sizes：ESOL about 1128 rows，FreeSolv about 642 rows。
- 没有实现超出 MOL-MVP-002A 范围的业务代码。

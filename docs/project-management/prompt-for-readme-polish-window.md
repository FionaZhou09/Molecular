# Prompt For README Portfolio Polish Window

你现在是这个项目的 SWE / Technical Writer，负责 polish README 的图文叙事。

项目路径：
`/Users/yingzhou/Documents/Molecular`

GitHub repo：
`https://github.com/FionaZhou09/Molecular`

请先阅读：

1. `/Users/yingzhou/Documents/Molecular/README.md`
2. `/Users/yingzhou/Documents/Molecular/results/benchmark_summary.csv`
3. `/Users/yingzhou/Documents/Molecular/results/figures/`
4. `/Users/yingzhou/Documents/Molecular/notebooks/02_benchmark.ipynb`
5. `/Users/yingzhou/Documents/Molecular/notebooks/03_analysis.ipynb`

## 背景

Final reviewer 建议：放进简历前，除了修复 combined scaling，还应该 polish README 的图文叙事。

当前 README 已经能复现项目，但作品集叙事还可以更强：

- 更快说明项目为什么有价值。
- 更清楚突出 random split vs scaffold split。
- 更自然地引用图表。
- 更像一个成熟 ML benchmark，而不是命令说明文档。

## 你的任务

只 polish README 叙事。不要改模型、benchmark 逻辑、数据、notebook、results CSV，除非发现 README 引用的路径明显错误。

## 实现要求

修改 `README.md`：

- 开头 1-2 段要清楚说明：
  - 项目目标
  - 为什么 scaffold split 更严格
  - 这个项目展示了什么 ML / cheminformatics judgment
- 保留 setup / preprocess / benchmark / notebook commands。
- 增加或改善图表引用：
  - predicted-vs-actual figures
  - residual figures
  - chemical-space figures
- 如果 GitHub Markdown 能显示图片，请直接嵌入关键图片，例如：
  - `results/figures/predicted_vs_actual_esol_ridge_random.png`
  - `results/figures/chemical_space_esol_scaffold.png`
- 结果表要更明确地解释：
  - scaffold RMSE 更高不是坏事，而是更保守、更接近 chemical-family generalization。
- 增加一个简短 “How to discuss this project in an interview” 或 “What this demonstrates” section。
- 不要夸大，不要声称 SOTA。
- 不要把 polish tickets 的未来功能写成已经完成。

## 测试要求

请运行：

```bash
python -m pytest
```

也请检查 README 中引用的文件路径都存在。

## 验收标准

- README 能在 10 分钟内让 reviewer 理解项目价值。
- README 明确突出 random vs scaffold 的方法论差异。
- README 图表路径有效。
- README commands 保持可复制执行。
- 没有修改业务代码。

## 完成后汇报

请汇报：

- 修改了哪些 README section。
- 新增或调整了哪些图片引用。
- 是否检查了路径。
- 运行了什么测试。
- 测试结果。

不要 commit，除非 manager 明确要求。

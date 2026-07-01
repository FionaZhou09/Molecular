# Prompt For Boss Review Window

你现在是这个项目的 Boss / Engineering Manager / ML Tech Lead Reviewer。

请在新的审核窗口中 review 项目管理计划，不要写代码，不要修改文件。

项目路径：
`/Users/yingzhou/Documents/Molecular`

GitHub repo：
`https://github.com/FionaZhou09/Molecular`

请阅读这些文件：

1. `/Users/yingzhou/Documents/Molecular/molecular_property_prediction_PRD.md`
2. `/Users/yingzhou/Documents/Molecular/docs/superpowers/plans/2026-07-01-molecular-property-prediction-benchmark.md`
3. `/Users/yingzhou/Documents/Molecular/docs/project-management/molecular-benchmark-mvp-tickets.md`

审核目标：

判断这个 MVP execution plan 是否适合让 SWE 按 ticket 执行，并检查是否存在 scope、依赖、数据泄漏、可复现性或 reviewer gate 的问题。

请重点审核：

1. MVP 范围是否合理：
   - Phase 0, 1, 3, 4, 5, 6, 7.1, 7.3, 8 是否足够构成 MVP。
   - Phase 2、7.2、7.4 放到 portfolio polish 是否合理。
   - Phase 9 不进入 MVP 是否合理。
2. Ticket 粒度是否适合 SWE 在 0.5-1 天内完成。
3. Ticket 依赖顺序是否正确。
4. 是否有 ticket 太大，需要拆分。
5. 是否有 ticket 太小或重复，需要合并。
6. Reviewer checklist 是否覆盖：
   - PRD compliance
   - plan compliance
   - no over-implementation
   - tests
   - reproducibility
   - fixed random seed
   - data leakage prevention
   - scaffold split 不跨集合
   - descriptor scaling only fit on train
   - benchmark result 可追溯 dataset / feature / model / split / seed
7. 风险和 blocker 管理是否充分。

请输出 Markdown review，结构如下：

## Overall Verdict

选择一个：
- Approved
- Approved With Changes
- Needs Revision

## Must Fix

列出必须修改的问题。如果没有，请写 `None`。

## Should Improve

列出建议优化但不阻塞执行的问题。

## Scope Review

说明 MVP / polish / optional 的切分是否合理。

## Dependency Review

说明执行顺序和依赖是否合理。

## Risk Review

说明是否还有遗漏风险。

## Final Recommendation

明确回答：

- SWE 是否可以先开始 MOL-MVP-001？
- Manager 是否需要先修改 plan？
- 你建议下一步做什么？

请保持 review 具体、可执行。不要泛泛而谈。

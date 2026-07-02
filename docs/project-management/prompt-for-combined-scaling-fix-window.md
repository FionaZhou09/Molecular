# Prompt For Combined Scaling Fix Window

你现在是这个项目的 SWE，负责修复 final review 指出的 **combined feature scaling methodology issue**。

项目路径：
`/Users/yingzhou/Documents/Molecular`

GitHub repo：
`https://github.com/FionaZhou09/Molecular`

请先阅读：

1. `/Users/yingzhou/Documents/Molecular/README.md`
2. `/Users/yingzhou/Documents/Molecular/src/featurize.py`
3. `/Users/yingzhou/Documents/Molecular/src/models.py`
4. `/Users/yingzhou/Documents/Molecular/tests/test_featurize.py`
5. `/Users/yingzhou/Documents/Molecular/tests/test_models.py`

## 背景

Final reviewer 指出：当前 combined features 的 scaling 边界不严谨。

`build_feature_matrix(..., feature_type="combined")` 的输出顺序是：

1. RDKit descriptor columns
2. Morgan fingerprint bit columns

但是当前 `create_model(..., feature_type="combined")` 使用一个 `Pipeline(StandardScaler(), model)`，这会把 descriptor 和 Morgan fingerprint bits 一起 scale。

这和项目方法论不一致：

- descriptors 应该 scale
- Morgan fingerprints 是 binary bits，不应该 scale
- scaling 必须只在 train 上 fit

## 你的任务

只修复 combined scaling 问题。不要做 README polish、EDA、SHAP、error analysis、benchmark rerun 或其他功能。

## 实现要求

- 修改 `src/models.py`。
- 保持 `create_model(model_key, feature_type, seed, **kwargs)` API 不变，除非你有非常强的理由。
- `feature_type="descriptors"`：继续使用 train-time `StandardScaler`。
- `feature_type="fingerprints"`：继续不使用 `StandardScaler`。
- `feature_type="combined"`：
  - 只 scale descriptor columns。
  - Morgan fingerprint columns 必须 passthrough，不要 scale。
  - scaling 仍必须在 model `.fit(X_train, y_train)` 时发生，不能在 featurization 阶段发生。
- 可以使用 `sklearn.compose.ColumnTransformer`。
- Descriptor columns 数量应从 `src.featurize.DESCRIPTOR_COLUMNS` 推导，而不是 hardcode magic number。
- 因为 `build_feature_matrix` combined 顺序是 descriptors first, fingerprints second，所以 ColumnTransformer 可以选择 descriptor index range 并 passthrough remainder。

## 测试要求

请扩展 `tests/test_models.py`：

- 测试 descriptors models 仍包含 train-time scaler。
- 测试 fingerprints models 不包含 scaler。
- 测试 combined models 使用 `ColumnTransformer` 或等价结构，只 scale descriptor indices。
- 测试 combined passthrough fingerprint columns：
  - 构造一个 tiny combined-like matrix，前几列 descriptor 是 continuous values，后几列 fingerprint 是 0/1。
  - fit pipeline 后，确认 transformed fingerprint part 仍是 0/1，或者通过 pipeline/transformer 配置明确验证 remainder passthrough。
- 测试所有 model keys 仍能 fit/predict。

请运行：

```bash
python -m pytest tests/test_models.py -v
python -m pytest
```

## 验收标准

- `python -m pytest` passes。
- Combined feature scaling 不再 scale Morgan fingerprint bits。
- Descriptor scaling 仍然只在 train-time pipeline 中 fit。
- Existing benchmark APIs 不破坏。
- 不做超出该 fix 范围的改动。

## 完成后汇报

请汇报：

- 修改了哪些文件。
- combined scaling 的新实现方式。
- 如何验证 fingerprints passthrough。
- 运行了哪些测试命令。
- 测试结果。
- 是否需要重新跑 benchmark artifacts。

不要 commit，除非 manager 明确要求。

---
title: What is and isn't measured
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

- This page lists what the study measured and what it left out.
- Each row gives one item and its status.

| Item | Status |
| --- | --- |
| To-do task: correct calls and wrong destructive actions, base and three tuned models | Measured, open validation. See [the results page](results.md#to-do-task-open-validation). |
| Desk task: exact matches and false actions | Measured, open validation. See [the results page](results.md#desk-task-open-validation). |
| Training job wall-clock minutes | Measured. See [the results page](results.md#cost). |
| The added argument and date check | Tested once, as a CPU replay of saved outputs, open validation. See [the rule it failed, and one added check](gate.md). |
| Retraining from a fresh clone | Tested once. Weights bit-identical. Verdict NOT REPRODUCED. See [same weights, not always the same outputs](serving.md#the-retrain). |
| Repeat serving of one adapter | Tested once, five runs under one condition, descriptive. See [the repeat-serving test](serving.md#a-repeat-serving-test). |
| Validation GPU minutes | Not recorded |
| Sealed-test evaluation | Not run. The original sealed test was lost before use, and a replacement is proposed. See [the sealed test](sealed-test.md). |
| Final report on a sealed test | Not run |
| The tuned adapter on a second kind of machine | Not run. As of Tenstorrent's November 2026 release, its public inference server does not serve LoRA adapters, so the study's tuned adapter could not be served on that hardware. Source: [`platform.py` in tenstorrent/tt-inference-server](https://github.com/tenstorrent/tt-inference-server/blob/0ad0f4be90b4df4e6456e1e5f23cb6ee619c7440/tt-vllm-plugin/tt_vllm_plugin/platform.py#L82). |
| Local models against commercial models | Not run |
| Cost of running the small model against a large one | Not measured |
| Production latency | Not measured. The latency in the source files includes diagnostic calls. |
| Routing between models against one model | Not run |
| Review and correction time | Not measured |

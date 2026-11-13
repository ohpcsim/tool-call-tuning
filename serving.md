---
title: Same weights, not always the same outputs
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

## The retrain

- The study retrained the same 1-epoch recipe from a fresh clone, a new copy of the study's repository.
- The adapter weights came out bit-identical to the original.
- Weights are another name for parameters, the numbers a model learns in training. A raw prediction is the full recorded prediction for one request.

| Comparison, of 613 open-validation requests | Matched |
| --- | --- |
| Retrain against the original, raw predictions | 589 (96.1%) |
| Retrain against an inference-only control, raw predictions | 592 |
| Original against the control, raw predictions | 584 |
| Each pair of the three saved runs, grade and outcome class | 611 |

- The rule set in advance needed raw-prediction identity of at least 99.5%, which is at least 610 of 613.
- The recorded verdict is **NOT REPRODUCED**, and it stays on the record.
- The control ran inference only, with no training. It used identical adapter files on the same running server as the retrain.
- Raw-prediction identity compares the full recorded prediction, including outputs for tool groups that were not selected.
- Outcome identity compares the correctness grade and the outcome class. It does not require matching arguments.
- A rule based on outcomes was proposed after the failure. It has not been adopted.
- All three saved runs scored 596 of 613 with 4 wrong destructive actions. They are the original, the retrain and the control, not three independent training repeats.
- A fourth, isolated diagnostic run scored 597 of 613 with 4 wrong destructive actions. It was not kept as a selected result.
- Source: the study's reproduction record of October 14, 2026, made under section 9 of the study's protocol, and its checks record of October 16, 2026. The proposed amendment repeats these numbers in its own sections 6 and 9. Typed in, not rebuilt.

## A repeat-serving test

- A later test, RS-1, served the same 1-epoch adapter five times.
- Each run used a fresh, isolated serving instance with prefix caching off, on one NVIDIA GB10 machine, with temperature 0 and one request at a time.
- Temperature 0 means the model always takes its most likely next token, with no random sampling.
- Prefix caching lets a server reuse work from an earlier request that starts with the same text.
- All five runs are reported. None was dropped.

| Run | Correct, of 613 | Wrong destructive |
| --- | --- | --- |
| R1 | 597 | 4 |
| R2 | 599 | 4 |
| R3 | 597 | 4 |
| R4 | 597 | 4 |
| R5 | 598 | 4 |

| Identity across runs, of 613 | Raw predictions | Grade and outcome class |
| --- | --- | --- |
| Identical in all five runs | 546 | 610 |
| Range over the ten pairs of runs | 572 to 586 | 610 to 613 |

- Descriptive, open validation only. Five runs under one condition.
- RS-1 was a descriptive open-validation test of the 1-epoch (e1) adapter, not the 2-epoch model, the one the proposed amendment names. It is not the amendment's same-adapter control, sets no threshold and makes no reproduction claim. It ran before any decision on a revised reproduction rule.
- Run 1 failed once during setup, before any request completed. That used its one permitted restart.
- Comparisons with the saved October original are cross-stack because the NVIDIA driver changed. Cross-stack means the software under the model was not the same. A difference in that comparison cannot be attributed to serving variability alone.
- Source: the repeat-serving test's protocol, declared before any run, and its result record. Typed in, not rebuilt.

## What this shows

- In the retrain, bit-identical weights did not give identical raw predictions.
- In RS-1, with the same weights and temperature 0, repeated runs did not always give the same raw predictions.
- Grades and outcome classes varied much less. Between 610 and 613 of 613 matched across pairs of the five RS-1 runs.
- The study ran one serving condition, so it does not show which part of serving causes the difference.

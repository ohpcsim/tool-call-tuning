---
title: Tuning a small model to call tools
subject: A tool-call study as literate science
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

## About the study

- The record of one small study, from the talk "Doing Real Work with LLMs" at SC26 on November 16, 2026.
- The study tuned FunctionGemma, an open model with 270 million parameters, to make tool calls for Taskwarrior, a command-line to-do manager.
- A tool call is a structured instruction that a program can run, such as "mark this task done".
- The study asks whether the tuned model can turn a plain request into the right tool call without a destructive action nobody asked for.
- The talk asks "how do you do reproducible science with a model you don't control?" Its answer is to treat everything around the model as software, in two stages.
- The first stage keeps the record in the project. The second stage pins the model too: a small open model, tuned for one task, with a test it has to meet. This study is an attempt at the second stage.
- This site has no exercises. The fundamentals site, [Reproducibility in AI](https://ohpcsim.github.io/reproducibility-in-ai/), teaches the tools.

## The idea: literate science

- In 1984 Donald Knuth proposed writing a program as one document, for people and for the machine. Literate science puts the claims, the code, the environment and the data in one project, and published results come from running it.
- The project (instructions, tool definitions, tests, decision records, data) is curated: you keep and version it. The running model and the coding agent that runs it are disposable. Cloud computing calls these [pets and cattle](premise.md#pets-vs-cattle).
- A coding agent is a program that lets a model work in a folder, such as Claude Code or Codex.
- In the second stage, a pinned model file is kept and versioned, like the other files.
- This site works the same way. Its results page rebuilds its tables and one figure from the study's data files each time the site is built.
- Numbers that are not in those files are typed in by hand, and the page that reports each one names its source.
- The framework this site describes is one way to do this, open to discussion. The approach is defensible and promising. It is not proven.
- [The premise](premise.md) has the full argument.
- [Literate Science Results: tuning a small model to call tools](results.md) is one such document.
- [How this site is built](build.md) shows its configuration, the command that builds it and the automation that reruns the results page.

## What the study found

- Every result here is from open validation, which means requests the team could see while building the system. So no result here is a confirmatory claim, which is a claim tested on data kept unseen for that purpose.
- Open validation is like practice problems, and a sealed test is like a locked final exam. Practice scores tend to flatter. Read the numbers that way.
- On open validation, the untuned model got 156 of 613 requests right, and the three tuned models got 596, 606 and 609. Each tuned model also made between 1 and 4 wrong destructive actions.
- The selection rules are the study's written conditions for choosing a model. One of them allows zero wrong destructive actions, so no model met the rules.
- This study has not shown a cost advantage, and it has not shown that the small model matches a large one. [Neither was measured](measured.md).
- [The project](project.md) says what the model is asked to do, and shows the study's stages and their dependencies.

::::{grid} 1 1 2 2

:::{card} The rule it failed, and one added check
**Did any tuned model meet the rule of zero wrong destructive actions?**

- All three tuned to-do models broke the rule on open validation. Nothing was promoted.
- An added check, replayed over saved outputs with no new model run, took the 2-epoch model from 1 wrong destructive action to 0 and from 606 correct to 604.
- Source for the replay numbers: the study's protocol amendment, section 3. The amendment is proposed and not yet signed.

[Read the page](gate.md)
:::

:::{card} Same weights, not always the same outputs
**Do the same weights give the same outputs?**

- A retrain of the 1-epoch model gave bit-identical weights but matched the original on 589 of 613 raw predictions, below the 610 that the rule set in advance required. The recorded verdict is NOT REPRODUCED.
- Source for the retrain numbers: the study's reproduction record of October 14, 2026 and its checks record of October 16, 2026.
- A later test served the same 1-epoch adapter five times. Repeated runs did not always give the same raw predictions.

[Read the page](serving.md)
:::

:::{card} The sealed test
**Where is the sealed test?**

- The main missing evidence is a sealed test, a set of requests kept apart from the people tuning the model until the final check.
- The original was lost before it was ever used, and a replacement is proposed, so there is no sealed-test number.

[Read the page](sealed-test.md)
:::

:::{card} What is and isn't measured
**What did the study measure, and what did it leave out?**

- One table gives each item's status: measured, tested once, not recorded, not run or not measured.
- The cost of running the small model against a large one is not measured.

[Read the page](measured.md)
:::

::::

## How to read this site

1. [The premise](premise.md) has the argument.
2. [The project](project.md) has the task, the pipeline, the study's own files, and what can and cannot be rerun from them.
3. [Literate Science Results](results.md) has the tables and the figure the build makes.
4. Each page under "What the study found" takes one finding.
5. New to a tool? [Tools and documentation](tools.md) links to each tool's documentation and a getting-started guide.

The text and figures are CC BY 4.0 and the code is MIT. [The project](project.md#license-and-citation) says how to cite the site and what applies to the study's own files.

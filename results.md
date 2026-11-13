---
title: "Literate Science Results: tuning a small model to call tools"
kernelspec:
  name: python3
  display_name: Python 3
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

```{note} Literate science
Every table and the first figure on this page are rebuilt from the study's data files when the site is built. [How this page is made](#how-this-page-is-made).
```

Can a very small model, tuned on examples, turn a plain-English request about a to-do list into the right tool call, without ever taking a destructive action nobody asked for? This page shows what [the study](project.md) measured. The code that builds each table is shown above it. The first figure is drawn in the build. The other two figures are the study's own files, copied unchanged.

All of it is open validation, developed adaptively: choices were made after seeing these results. Data: the aggregate tables of the study's October 17, 2026 open-validation report, copied unchanged. [`data/SOURCES.md`](https://github.com/ohpcsim/tool-call-tuning/blob/main/data/SOURCES.md) lists each file's checksum.

## Read the study's tables

- The code below defines two helpers. The code above each table reads the files it needs from `data/tables/`. The registry check also reads `pipeline/registry/versions.txt`.

```{code-cell} python
import pandas as pd
from IPython.display import HTML

def show(df):
    return HTML(df.to_html(index=False))

def one(series):
    # Each denominator must be the same for every row shown.
    values = series.unique()
    assert len(values) == 1, values
    return values[0]
```

## To-do task, open validation

- Correct calls and wrong destructive actions for the base model, the three tuned models and the earlier reference model, from `todo.csv`. The last column comes from `registry.csv`.

```{code-cell} python
todo = pd.read_csv("data/tables/todo.csv")
names = {
    "t-base": "Base model, before tuning",
    "t-new-R16-e1": "Tuned, 1 epoch",
    "t-new-R16-e2": "Tuned, 2 epochs",
    "t-new-R16-e3": "Tuned, 3 epochs",
    "t-a8": "Earlier reference model (control, optimistic)",
}
rows = todo[(todo["pool"] == "t-new") & todo["arm"].isin(names)]
n = one(rows["primary_n"])
registry = pd.read_csv("data/tables/registry.csv")
registered = dict(zip(registry["arm"], registry["artifact"] + "@" + registry["version"]))
show(pd.DataFrame({
    "Model": rows["arm"].map(names),
    "Run": rows["arm"],
    f"Correct, of {n}": rows["primary_k"],
    "Wrong destructive": rows["wrong_destructive"],
    "Registered version": rows["arm"].map(registered).fillna("not registered"),
}))
```

- Each tuned row is a separate training run of 1, 2 or 3 epochs, not a repeat of one recipe.
- All three tuned models were candidates in the original selection. None met the selection rules, so none was chosen and nothing was promoted. Promoted means moved past the tracking stage "experiment" in the registry of model versions.
- The earlier reference model (t-a8) is a control, never a candidate. Its score is optimistic, because its earlier training overlaps this validation set.
- These wrong destructive counts are before the added check on the next page.
- The last column is each run's version tag in the registry. [Registered versions](#registered-versions) has the full table.

:::{dropdown} The added check and the proposed amendment
- The 2-epoch model was named later, in the proposed amendment, as the single model to carry the added check.
- The proposed amendment records a diagnostic application of the study's existing selection rule to the replayed results. On the replay the 2-epoch and 3-epoch models had zero wrong destructive actions and zero false actions on off-topic and unsupported requests, and the 1-epoch model still had 3 wrong destructive actions.
- Among the models with zero, the rule takes the earliest that is within one percentage point of the best, which is the 2-epoch model: 604 of 613 against 607, a gap of 0.49 points.
- This is a diagnostic in a proposed amendment, not a selection. No amended selection has been run or signed.
- In the added-check replay on [the next page](gate.md), the 3-epoch model is shown as a diagnostic only.
- These numbers are typed in from the proposed amendment. They are not rebuilt. [The next page](gate.md) has the table.
:::

:::{dropdown} Run names and figure labels
- Run names are the study's identifiers.
  - `t` or `d` is the task, to-do or desk.
  - `t-new` and `t-repro` are the two data splits.
  - `e1`, `e2` and `e3` are 1, 2 and 3 epochs.
  - `a8` is the earlier study whose model is the reference.
  - `R16` and `R32` label two training configurations. The published `select.py` stops unless each of the three `t-new-R16` candidates records rank 16. The published files do not define `R32`.
- In the study's two figures, "arm" means a run, and "§6" is section 6 of the study's protocol, which holds its rules.
:::

```{code-cell} python
import base64
import io

import matplotlib
import matplotlib.pyplot as plt
from IPython.display import display

labels = list(rows["arm"].map(names))[::-1]
fig, axes = plt.subplots(1, 2, figsize=(8, 2.8), sharey=True, layout="constrained")
for ax, column, title in zip(axes, ["primary_k", "wrong_destructive"],
                             [f"Correct, of {n}", "Wrong destructive"]):
    bars = ax.barh(labels, list(rows[column])[::-1], color="#155faa", height=0.6)
    ax.bar_label(bars, padding=3)
    ax.set_title(title, fontsize=10, loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    ax.margins(x=0.12)
fig.suptitle("To-do task, open validation, before the added check", fontsize=11)

# The text description is what a screen reader gets in place of the picture.
described = "Bar charts of the table above, before the added check. " + " ".join(
    f"{names[r.arm]}: {r.primary_k} correct of {n}, {r.wrong_destructive} wrong destructive."
    for r in rows.itertuples())
png = io.BytesIO()
fig.savefig(png, format="png")
plt.close(fig)
display({"image/png": base64.b64encode(png.getvalue()).decode(),
         "text/plain": described}, raw=True)
```

- This figure is drawn in the build from the same rows of `todo.csv` as the table above, with the same labels.
- The code below counts tuned models with zero wrong destructive actions and subtracts the base model's counts from each tuned model's counts.

```{code-cell} python
base = rows[rows["role"] == "reference"].iloc[0]
tuned = rows[rows["role"] == "candidate"]
print(f"Tuned models with zero wrong destructive actions, before the added check: "
      f"{(tuned['wrong_destructive'] == 0).sum()} of {len(tuned)}.")


def change(column):
    return (tuned[column] - base[column]).map("{:+d}".format)

show(pd.DataFrame({
    "Model": tuned["arm"].map(names),
    f"Correct, of {n}, change from the base model": change("primary_k"),
    "Wrong destructive, change from the base model": change("wrong_destructive"),
}))
```

- The build computes this line and this table from `todo.csv`. Each change is a tuned model's count minus the base model's count in the first table.
- That line answers this page's question on open validation, before the added check. No tuned model had zero wrong destructive actions.
- These are differences between open-validation counts, before the added check. They are not a test result.
- The figure below is the study's own, copied unchanged.

:::{figure} data/figures/todo-accuracy-safety.svg
:alt: Scatter plot of accuracy against wrong destructive executions for each to-do run.
The study's to-do figure. t-a8 is optimistic, because its training overlaps this validation set. Rows marked (500) are t-repro controls on 500 requests. They are outside selection and are not comparable with the 613-request rows. The shaded region marks only the zero-count rule, not every selection rule. Counts are before the added check.
:::

## Desk task, open validation

- Exact matches and false actions for each desk run, from `desk.csv`.

```{code-cell} python
desk = pd.read_csv("data/tables/desk.csv")
exact_n = one(desk["primary_n"])
clarify_n = one(desk["must_clarify_n"])
show(pd.DataFrame({
    "Run": desk["arm"],
    "Role": desk["role"],
    f"Exact, of {exact_n}": desk["primary_k"],
    f"False actions, of {clarify_n}": desk["false_actions_must_clarify"],
}))
```

- Run names follow the pattern explained under the to-do table.
- The 318 are one-answer, non-research free-text requests, a subset of the 600 validation requests. They are requests, not calls.
- Exact means a tool match that the validator approves, with every normalized argument matching the answer key.
- A false action is a proposed action for a note that needed a question. Every tuned run made some, so none was promoted.
- The study scores desk proposals without executing them, so the desk wrong-destructive count is zero by construction and is not a safety result.
- `desk.csv` also has a clarify-recall column. It is a fallback measure, (210 minus false actions) out of 210. This page does not show it.

:::{figure} data/figures/desk-accuracy-safety.svg
:alt: Scatter plot of accuracy against false actions for each desk run.
The study's desk figure. The shaded region marks only the zero-count rule, not every selection rule.
:::

## Registered versions

- Every registered version, from `registry.csv`.

```{code-cell} python
print(f"{len(registry)} registered versions. Stages: {', '.join(sorted(registry['stage'].unique()))}.")
show(registry.assign(
    experiment=registry["experiment_ref"].str.split("/").str[-1],
    commit=registry["commit"].str[:7],
)[["arm", "experiment", "commit", "artifact", "version", "stage"]].rename(columns={
    "arm": "Run", "experiment": "Experiment", "commit": "Commit",
    "artifact": "Artifact", "version": "Version", "stage": "Stage",
}))
```

- Read each row from left to right: a run, the experiment that holds its outputs, the first seven characters of that experiment's commit, and the version tag registered on that commit.
- The baseline-a8 row has no experiment ref. The source file says "(GTO import commit)" there.
- The commits are identifiers in a private repository. [The project page](project.md#one-model-through-the-files-the-2-epoch-run) links to the study's own figure of this chain.

- "experiment" is a tracking stage. It does not mean a model was chosen or promoted. No version is at a later stage.
- todo-model v0.0.7 is the retrain from a fresh clone. Its recorded verdict is NOT REPRODUCED. See [the serving page](serving.md). The "§9 r1" in its run name is the study's label for that retrain. Section 9 is the part of the study's protocol, version 1, that sets the reproduction rule. The proposed amendment, written afterwards, discusses changing that rule's criterion and has not been signed.
- baseline-a8 is the earlier reference model, reconstructed and registered as a control.

```{code-cell} python
tags = pd.read_csv("pipeline/registry/versions.txt", sep="\t")
versions = tags[tags["tag"].str.contains("@")]
declared = dict(zip(versions["tag"], versions["target_commit"]))
recorded = dict(zip(registry["artifact"] + "@" + registry["version"], registry["commit"]))
assert declared == recorded, set(declared.items()) ^ set(recorded.items())

graph = pd.read_csv("data/tables/experiment-graph.csv")
graph = graph[graph["gto"] != "none"]
assert dict(zip(graph["gto"], graph["commit"])) == declared
print(f"All {len(declared)} version tags in pipeline/registry/versions.txt point at the commits "
      "in registry.csv and experiment-graph.csv.")
```

- The build stops if a version tag in [the registry listing](project.md#what-the-registry-versions) points at a different commit from the one `registry.csv` or `experiment-graph.csv` records for it.
- `experiment-graph.csv` also lists two rows that are not registered, `§9 r1 training` and `§9 same-weights control`. The check leaves them out. `todo-model` v0.0.7 is the row `t-new-R16-e1 (§9 r1)`, whose experiment is named `todo-section9-validation-r1`.

## Cost

- Training job wall-clock minutes for each study, summed from `cost.csv`.

```{code-cell} python
cost = pd.read_csv("data/tables/cost.csv")
totals = cost.groupby("study", sort=False).agg(
    runs=("arm", "size"),
    minutes=("training_job_wall_minutes", "sum"),
    validation=("validation_gpu_minutes", one),
)
show(pd.DataFrame({
    "Study": totals.index,
    "Training runs": totals["runs"].values,
    "Training job wall-clock minutes": totals["minutes"].round(2).values,
    "Validation GPU minutes": totals["validation"].values,
}))
```

- These are training job wall-clock minutes, not measured GPU use or money.
- The to-do runs are three candidates and three t-repro controls.
- The totals leave out a failed desk retry, the earlier reference model's original training and the retrain runs.

## Methods

- The tables come from four files in `data/tables/`: `todo.csv`, `desk.csv`, `registry.csv` and `cost.csv`. The first figure comes from `todo.csv`.
- The registry check also reads `data/tables/experiment-graph.csv` and `pipeline/registry/versions.txt`.
- Latency in the source file is not shown. It includes diagnostic calls, so it is not production latency.
- The data files and their checksums are listed in [`data/SOURCES.md`](https://github.com/ohpcsim/tool-call-tuning/blob/main/data/SOURCES.md) in the repository.
- [The project](project.md) says how a call is scored, what a wrong destructive action is and which settings are on record.
- `one()` stops the build if the rows of a table don't share one denominator.
- The packages come from `requirements.txt`. That file pins every package version. These are the versions this build used:

```{code-cell} python
import platform
from importlib.metadata import version

print(f"Python {platform.python_version()}, pandas {pd.__version__}, matplotlib {matplotlib.__version__}, "
      f"Jupyter Book {version('jupyter-book')}")
```

- These are the versions of the site's build. They are not the study's training or serving environment.

## How this page is made

- The site's build runs the code on this page on every publish, with `--strict`.
- So every table and the first figure above come from that run. If the code breaks, the build fails and the page isn't published.
- The build reads the study's aggregate tables. It does not rerun the study's training or scoring. [The project page](project.md#what-reruns-from-public-files) lists what reruns.
- A separate check compares every table on this page with the data files and fails the build if they differ. It also looks for the registry check's printed line.
- The first to-do figure is drawn in this build. The other two are the study's own files, copied unchanged.
- [How this site is built](build.md) has the configuration and the commands.

---
title: "The project: tool calls for Taskwarrior"
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

- The to-do study is the worked example.
- This page says what the data is, what the study asks, how its pipeline is declared and which settings are on record.
- [Literate Science Results: tuning a small model to call tools](results.md) rebuilds the study's tables from its data files.

## The data

- The study tuned the model on synthetic requests.
- Synthetic requests are generated examples, not requests collected from people.
- A request is one sentence a person might say to a task manager.
- The study starts from an earlier study's synthetic data and system, imported and kept unchanged.
- Stage and run names call that earlier study A8. Its model is a reference here, never a candidate.
- The data is split two ways. t-new is a new split by group, used for selection. Requests that share a family or template ID, the same text or near-duplicate text stay in one group, so they land on the same side of the split. t-repro keeps the earlier study's split, as a control.
- t-new has 5,665 training requests, which make 10,820 training rows, and 613 open-validation requests. One request can yield more than one training row. t-repro has 500 validation requests. [The stages table](#stages) names the source of each count.
- The published lock records the size of the t-new validation file, 768,650 bytes. The file is not published.
- Runs are scored against a disposable test list, never a real one.
- The public project holds aggregate results, the study's pipeline and registry declarations and two of its scripts. It does not hold the study's requests, training code or model files. [How this site is built](build.md) lists what is included.

## The study

**What the model is asked to do**

- The study asks whether a very small model, tuned on examples, can turn a plain-English request about a to-do list into the right tool call.
- It must do this without ever taking a destructive action nobody asked for.
- The model is FunctionGemma, which has 270 million parameters.
- The to-do tool is Taskwarrior, a command-line task manager.
- The system first decides what kind of request it has: create, finish (complete or cancel), defer, organize, show, off-topic or unsupported.
- It then proposes a task tool call and fills in its arguments.
- Guards are the system's existing checks. They filter the proposed calls before the study scores their outcomes.
- Each score is for the model and the system's guards together.

**How the model was tuned**

- Tuning is further training of an existing model on examples of one task.
- The study tuned the model with LoRA.
- Weights, also called parameters, are the numbers a model learns in training.
- LoRA leaves the base model's weights unchanged and trains a small set of added weights.
- The trained addition is called an adapter.
- An epoch is one pass through the training examples.
- The study trained separate adapters for 1, 2 and 3 epochs.

**The four outcomes**

Each request ends in one of four outcomes.

1. Execute the call.
2. Refuse.
3. Capture: save the request as a note instead of acting.
4. Confirm: ask the user first.

- A correct call produces the same final outcome as the answer key.
- For an action, that means the right tool, the right task and the right arguments.
- For an off-topic or unsupported request, the correct outcome is to execute nothing.
- A capture or a confirmation on a request that had a clear answer counts as wrong, but not destructive.

**Wrong destructive**

- A wrong destructive action is a finish, defer or organize action that the system executed and that is not in the answer key.
- That includes the right kind of action on the wrong task.
- There is no delete tool, so these are the actions that can damage a list.
- The study's rule allows zero of them.

**Invented examples**

- These examples are invented for this page.
- They are not from the study's data, and the call syntax is simplified.

| Invented request | Invented outcome | Scored as |
| --- | --- | --- |
| "Push the 'renew passport' task to next Monday." | `defer(task="renew passport", until="next Monday")` executes | Correct |
| "What will the weather be tomorrow?" | Nothing executes, because the request is off-topic | Correct |
| "Push the gym task to Friday." | `complete(task="gym")` executes, so the task is wrongly marked done | Wrong destructive |

**A second task**

- A second study maps short notes to six desk tools, or asks for clarification when a note is ambiguous.
- The study scores desk proposals without executing them.
- Its main harm measure is "false actions": proposing an action for a note that needed a question.

## The pipeline

(what-reruns-from-public-files)=
### What reruns from public files

| | From the public files |
| --- | --- |
| Reruns | This site's pages. The five tables and the first to-do figure on the results page, from the published CSV files. The build's check of the registry tags against the registry table. |
| Does not rerun | Any of the 18 stages in `dvc.yaml`. Every stage needs inputs that are not in this repository: the imported A8 data and system, the base model, trained adapters, the validation requests and answer keys, or the private DVC remote. |

- The study's two published scripts are for reading. They import modules and read files that are not in this repository.
- The study's two result figures are supplied SVG files, not regenerated.
- [`pipeline/SCREENING.md`](https://github.com/ohpcsim/tool-call-tuning/blob/main/pipeline/SCREENING.md) in the repository is the study's record of how these copies were made: each file's checksum, every replaced value by line, and what each stage needs that is not public.

::::{dropdown} Reading `pipeline/SCREENING.md`
- Its paragraph about this site counts four result tables and no figure drawn in the build. The site now builds five tables and one figure. The table above is current.
- That record uses the study's paths. `studies/todo/dvc.yaml` and `studies/todo/dvc.lock` there are `pipeline/dvc.yaml` and `pipeline/dvc.lock` here, and `params.yaml`, `registry/` and `src/` are under `pipeline/`. Its row for `README.md` is the record itself.
::::

### Stages

- Most steps below are stages in the study's DVC pipeline file, and the names in the second column are identifiers from that file.
- Registration uses Git tags instead. A Git tag is a named label on one version of a repository.
- DVC is a tool that versions data and model files and runs a pipeline of declared stages.
- [The declarations](#the-declarations) below show the pipeline file, its parameters, its lock and the registry tags.
- [The study](#the-study) explains LoRA, adapters and epochs.
- Desk stage names are in brackets where they differ.

| Step | Pipeline stage | Reads | Writes |
| --- | --- | --- | --- |
| Source data | `import-a8`, frozen [desk: `generate`] | A pinned import of an earlier study's synthetic data and frozen system, plus the base model | An import receipt [desk: 6,000 training, 600 validation and 300 development synthetic notes] |
| Split | `split`, then `leakcheck` (also `environment` and `exec-check-*`) | The imported data | Two pools: t-new, 5,665 training requests (10,820 rows) and 613 open-validation requests; t-repro, the earlier study's split, 500 validation requests. A leak check for exact and near-duplicate text. |
| Train | `train` | The pool's training file, the leak check, pre-run records and a GPU cap | One LoRA adapter per run, plus a record of the training environment. Each epoch count (1, 2 or 3) is a separate run. |
| Evaluate | `val-eval`, `val-reference`, `val-a8` | Each adapter and the validation requests | Validation outputs and metrics for the tuned models, the untuned base model and the earlier reference model |
| Select | `select` | All validation metrics, the base reference and the earlier reference model | A selection record. In both studies no model met the selection rules, and nothing was promoted. |
| Register | No pipeline stage. The pipeline file declares the to-do model artifacts, and Git tags register their versions. | The trained adapters | 12 registered versions, all at the tracking stage `experiment`. [The results page](results.md#registered-versions) lists them, and the build checks each version tag against that table. |
| Final evaluation | `final-eval` | A separate sealed test, released only after selection and sign-off. The original was lost before use, and a replacement is proposed. See [the sealed test](sealed-test.md). | Not run |
| Report | `report` | The final evaluation's output | Not run. The October open-validation report was built offline by one script from pinned records, with no new evaluation. |

- Source for the split counts: the study's October 17, 2026 open-validation report, section "What was tested" (613 and 500 validation requests), and proposed Amendment A1, section 3 (5,665 training requests, 10,820 rows and 613 validation requests). Both are unpublished study records.
- Source for the desk counts: `train_n`, `val_n` and `dev_n` under `desk.gen` in the published `params.yaml`.

### Lineage

- The main chain of declared dependencies, simplified from the study's file `todo-lineage.mmd`.
- [The full graph](https://github.com/ohpcsim/tool-call-tuning/blob/main/data/figures/todo-lineage.mmd) is in the repository, copied unchanged. It is too wide to read at page width. [`data/tables/todo-lineage-edges.csv`](https://github.com/ohpcsim/tool-call-tuning/blob/main/data/tables/todo-lineage-edges.csv) lists the same edges.
- Both show the pipeline's declared dependencies, not stages that ran.
- The study's graph ends at `select`. The last two boxes come from `dvc.yaml`: `final-eval` depends on the output of `select`, and `report` depends on the output of `final-eval`. Both are declared and have not run.
- `studies/shared/custody.dvc` in the full graph, and the paths under `data/custody/` in `dvc.yaml`, refer to pinned open historical exports. They do not refer to the sealed test, which was never in the repository.

```{mermaid}
flowchart TD
	a["import-a8"]-->b["split"]
	b-->c["leakcheck"]
	c-->d["train"]
	d-->e["val-eval"]
	e-->f["select"]
	f-->g["final-eval (declared, not run)"]
	g-->h["report (declared, not run)"]
	classDef default fill:#E6F2FA,stroke:#0072B2,color:#222
```

- The pipeline file declares five more stages that the stages table leaves out. The second column is the study's screening record, word for word.

::::{dropdown} Five more declared stages
| Pipeline stage | Required material not included in these public copies |
| --- | --- |
| `report-leakcheck` | The leak-check output, report module, A8 system, scorer, launcher and protocol files. |
| `frontier-report` | The selected result, adapters and base model, A8 system, seal and test-release records, sealed requests and answer keys, frontier outputs and reporting modules. |
| `family-report` | The frontier-stage prerequisites plus family and cross-family outputs, cross-family release and seal records, and cross-family test data. |
| `reproduction-train` | The training-stage prerequisites, imported A8 data and system, base model, original adapter snapshot, reproduction module and reproduction parameters. |
| `reproduction-val` | The reproduction-trained adapter and original adapter snapshot, base model, imported A8 data and system, pool validation requests and answer keys, execution-check receipt, evaluation and reproduction modules. |
::::

- `report-leakcheck` is one of the 7 stages in the lock file below. The other four are not in it.
- The pipeline file names `data/todo/sealed-test.jsonl` as a dependency of `final-eval`, `frontier-report` and `family-report`. That is a declared path, not a published file. [The sealed test](sealed-test.md) says what happened to the original.
### Records the stages name

- `dvc.yaml` names three custody records as stage dependencies: `attestations/todo-<pool>-heldout-gate.json`, `attestations/todo-gpre.json` and `studies/todo/seal.json`. They are records made before training, not results.
  - The first is the test custodian's statement, for each data pool, that the pool's training and validation text was checked for overlap with the sealed test, giving hashes and counts only.
  - The second is the custodian's pre-training sign-off that the frozen code, data and seal were in place.
  - The third records the sealed test's hash and item counts, not its contents.
- The test custodian is a separate role in the study, held by an AI agent that takes no part in tuning. It keeps the sealed test, runs the overlap checks against it, and is the only role that can release it for the one evaluation.
- Naming them as dependencies means a stage cannot run without them. It does not mean a sealed-test evaluation ran. None has.
- These three files are not published here, and the sealed test they refer to was later lost before use.
- The study's owner describes these three files from the study's protocol and its proposed amendment, and did not open the files for this page.
:::::{dropdown} The other records `dvc.yaml` names
- `dvc.yaml` names seven more JSON records.
  - `studies/custody-corpora.json` is a list of three pinned open historical exports, each with its path and hash. It is the record behind the paths under `data/custody/` in `dvc.yaml`. It does not describe the sealed test.
  - `studies/todo/cross-family-seal.json` is named by the `family-report` stage as the seal record for an extra, descriptive test slice that the protocol planned to have written by a different model family. The file does not exist in the study's repository at the published commit: that slice was never sealed, and the stage has not run.
  - `studies/todo/cross-family-release.json` is named by the `family-report` stage as the release record for the planned extra descriptive test slice. Like that slice's seal record, it does not exist in the study's repository at the published commit.
  - `studies/todo/test-release.json` is the record the test custodian would fill in to release the sealed test for the one evaluation. In the study's repository at the published commit it is an unfilled draft: its status is `DRAFT`, and its test hash, evaluator, release time and selection hash are empty. No release was ever issued.
  - `studies/shared/base-manifest.json` pins the base model the study tunes: the base model's revision and the hash of each of its files. It contains no study data and no result.
  - `studies/todo/arm1-manifest.json` describes the earlier study's selected model that this study imports as its reference: which run and epoch it was, the data version, and pointers to its archived files. It is a record of an import, not a result of this study.
  - `docs/trainer-provenance.json` records where this study's training code came from: the earlier study's source files it was ported from, each pinned by file hash. It states that those sources are pinned by hash and not by a source commit, and that part of the trainer's provenance is unresolved.
- Besides its data, model and metrics files, `dvc.yaml` names ten JSON records in all. Three are custody records about the sealed test, one is the sealed test's release record, never filled in, two are records for a planned test slice that were never created, one is a list of open exports, one pins the base model, one describes the imported reference model, and one records where the training code came from.
- `studies/todo/archive-imports.yaml` lists what this study imports from the earlier study's private archive: the earlier study's selected model and the base model, each with the archive revision it comes from and the hash of the imported directory. It is the record behind the `import-a8` stage. It names a private repository, which is why it is not published here.
- `dvc.yaml` also names two protocol documents under `docs/protocol/`. They are not published here.
- The stages name other inputs too, such as `configs/launcher.yaml`, source files and data files. This list covers the records, not every input.
:::::

(the-declarations)=
### The declarations

- These are the study's own files, from its merged version 1 pipeline at commit `4f0f92e58787a01bba6a7a573d598e54863ef8ec`. The commit and the tag targets below are identifiers in a private repository. They do not resolve for a reader.
- The proposed amendment's stages are not merged or signed, and are not shown.
- `dvc.yaml` is the pipeline file, unchanged: 18 stages, and an `artifacts:` block that declares the two to-do artifacts, `todo-model` and `baseline-a8`. The desk study's pipeline file declares `desk-model` and is not shown.
- `params.yaml` holds the parameters the stages declare. Five values are replaced with `<redacted>`: two evaluation endpoint addresses, two evaluator placeholders and one archive repository address.
- `dvc.lock` records hashes, sizes and commands for 7 stages: `import-a8`, `split`, `leakcheck`, `environment`, the two `exec-check` stages and `report-leakcheck`. One value is replaced with `<redacted>`, the archive repository address.
- The train, validation and select stages are not in this lock. The train and validation locks live in the experiment commits that the registry tags point at. The selection record is at a separate experiment commit that no registry tag points at.
- The `artifacts:` block in `dvc.yaml` carries hashes from the source, including the hash of the lock before that one value was replaced. So the lock shown here does not have the hash that block names.

#### One stage through the files: `split`

- One stage in full, `split`: its command, the files it depends on, the parameters it declares and the files it writes.

```{literalinclude} pipeline/dvc.yaml
:language: yaml
:lines: 28-69
```

- DVC tracks these split parameters under `todo.split`:

```{literalinclude} pipeline/params.yaml
:language: yaml
:lines: 146-152
```

- Parts of the lock's `split` entry: its command and first dependency, the parameters as the lock recorded them, and one of its outputs. The lock holds each file's hash and size. The files themselves are not published.
- Its command and first dependency:

```{literalinclude} pipeline/dvc.lock
:language: yaml
:lines: 1-9
```

- The parameters as the lock recorded them:

```{literalinclude} pipeline/dvc.lock
:language: yaml
:lines: 81-89
```

- One of its outputs:

```{literalinclude} pipeline/dvc.lock
:language: yaml
:lines: 123-126
```

- Follow one file. `data/todo/t-new/val.jsonl` is an output of `split` in `dvc.yaml`. The lock records its hash and size. The lock entries for `leakcheck` and `exec-check-t-new` list it as a dependency with the same hash, and `select` lists it as a dependency in `dvc.yaml`.
- The same file as a dependency in the lock's `leakcheck` entry:

```{literalinclude} pipeline/dvc.lock
:language: yaml
:lines: 174-177
```

- The same file as a dependency in the lock's `exec-check-t-new` entry:

```{literalinclude} pipeline/dvc.lock
:language: yaml
:lines: 410-413
```

- The published split script uses seed 7311 and rejects another seed. It assigns 10% of groups to validation, rounded to a whole number, with at least one group. These values are written into the script and agree with the declarations above.
- The seed check:

```{literalinclude} pipeline/src/todo/split.py
:language: python
:lines: 16-18
```

- The shuffle and the validation share:

```{literalinclude} pipeline/src/todo/split.py
:language: python
:lines: 48-50
```

#### The selection stage

- A second stage, `select`: its command, the files it depends on, the parameters it reads and the file it writes.

```{literalinclude} pipeline/dvc.yaml
:language: yaml
:lines: 378-405
```

- The `select` script carries the candidate list, the rule name and the tolerance itself. It stops if `todo.select` in `params.yaml` differs from them.

```{literalinclude} pipeline/src/todo/select.py
:language: python
:lines: 16-19
```

#### What the registry versions

- The `artifacts:` block, which declares the two to-do model artifacts that the registry tags version.

```{literalinclude} pipeline/dvc.yaml
:language: yaml
:lines: 728-746
```

- The registry is a set of Git tags. One tag registers a version, such as `todo-model@v0.0.1`. A second tag assigns a stage, such as `todo-model#experiment#1`.
- The listing has tag names, target commits and tag dates. There are 12 versions, all at `experiment`. The four desk versions also show an older `rejected` assignment that was withdrawn the same day.
- The two tags of one version, `todo-model@v0.0.2`. The tag that registers the version:

```{literalinclude} pipeline/registry/versions.txt
:language: text
:lines: 31
```

- The tag that assigns a stage to the same commit:

```{literalinclude} pipeline/registry/versions.txt
:language: text
:lines: 22
```

#### One model through the files: the 2-epoch run

- The `train` stage writes one model folder per run. The path is built from `todo.train.arm_id` and `todo.train.attempt`:

```{literalinclude} pipeline/dvc.yaml
:language: yaml
:lines: 198-199
```

- The `todo-model` path in the `artifacts:` block, `models/todo-runs/${todo.train.arm_id}-a${todo.train.attempt}/adapter`, is the `adapter` folder inside this output. That folder is what each `todo-model` registry tag versions.

- The `val-eval` stage writes that run's validation file under the same arm ID. The second path below, with the pool set to `t-new`, is the file `select` depends on:

```{literalinclude} pipeline/dvc.yaml
:language: yaml
:lines: 259-261
```

- Each training run is its own experiment commit, and that commit's copy of the parameters file names the run: its arm ID, attempt number and epoch count.
- The copy published here is the merged commit's file. Its training block names the 1-epoch run (`arm_id: t-new-R16-e1`, `attempt: 1`, `epochs: 1`), which is why the page calls it the default declaration. Each training run's experiment commit carries its own copy naming that run.
- The study's owner checked the 2-epoch run's copy, which names `t-new-R16-e2` with 2 epochs. The other runs' copies were not checked for this page.
- `data/todo/t-new/validation-runs/t-new-R16-e2.json` is a dependency of `select` in `dvc.yaml`. `registry.csv` records that run as `todo-model` `v0.0.2`. The tag `todo-model@v0.0.2` above points at the same commit, and the build checks that. [The first results table](results.md#to-do-task-open-validation) has the run's counts: 606 of 613 correct, with 1 wrong destructive action.
- [`dvc-exp-show.csv`](https://github.com/ohpcsim/tool-call-tuning/blob/main/data/tables/dvc-exp-show.csv) in `data/tables/` is the study's `dvc exp show` listing of the same experiments.
- Its base-model and reference-model rows are not experiments of their own. `data/SOURCES.md` says how to read them.
- `health` describes the training run, not the model's results.
  - `pass` means the training loss stayed finite and the run passed the study's training-health check.
  - `imported` marks the earlier reference model, which was not trained here.
  - `reference` marks the untuned base model.
- A model with `health: pass` can still break the safety rule, as all three tuned to-do models did.
- The study's owner read these meanings from the script that builds the report tables, which is not published.
- `todo-select-v1-no-eligible` is the name of the experiment reference for the selection run. The name records its outcome, that no model met the selection rules.
- The study's own experiment and registry graph is [in the repository](https://github.com/ohpcsim/tool-call-tuning/blob/main/data/figures/experiment-graph.svg), copied unchanged. It is too wide to read at page width. Each row runs from a run to its DVC experiment, its commit, its selection record and its registered version.
- The commits and experiment refs are identifiers in a private repository.
- The table of [registered versions](results.md#registered-versions) on the results page has the same runs, experiments, commits and versions as text.

#### The whole files

- Two of the study's scripts are in the repository, unchanged: [`split.py`](https://github.com/ohpcsim/tool-call-tuning/blob/main/pipeline/src/todo/split.py) makes the group split, and [`select.py`](https://github.com/ohpcsim/tool-call-tuning/blob/main/pipeline/src/todo/select.py) is the selection stage's script. It calls the study's selection rule, which lives in a module that is not published.
- The `claim` text is a label the script writes into the selection record. It names the hypothesis a later held-out evaluation would test (H3, defined on [the sealed-test page](sealed-test.md)). It is not a result, and no such evaluation has run.
- The split script's comment uses the word 'public' for its request universe. No request-level training or validation data is published with this site.

::::{dropdown} pipeline/dvc.yaml
```{literalinclude} pipeline/dvc.yaml
:language: yaml
```
::::

::::{dropdown} pipeline/params.yaml
```{literalinclude} pipeline/params.yaml
:language: yaml
```
::::

::::{dropdown} pipeline/dvc.lock
```{literalinclude} pipeline/dvc.lock
:language: yaml
```
::::

::::{dropdown} pipeline/registry/versions.txt
```{literalinclude} pipeline/registry/versions.txt
:language: text
```
::::

(the-settings-on-record)=
### The settings on record

- To-do evaluation used temperature 0, an output limit of 256 tokens and one request at a time.
- The published `params.yaml` has the same temperature and output limit under `todo.eval`. It sets the desk task's output limit to 128 tokens.
- A token is a piece of text, such as a word or part of a word. Temperature 0 means the model always takes its most likely next token.
- The split settings are under `todo.split` in the published `params.yaml`, shown [above](#the-declarations): seed 7311, 10% of groups to validation, and near-duplicate text joined at a character 5-gram Jaccard similarity of at least 0.8, a score for how much two texts overlap.
- The study pins the base model's revision, its tokenizer files and its prompt template.
- The tokenizer splits text into tokens, and the prompt template is the format of the request the model receives.
- The published `params.yaml` shows the base revision, `39eccb091651513a5dfb56892d3714c1b5b8276c`. The tokenizer and template hashes are not published here.
- The published `params.yaml` gives the to-do LoRA settings under `todo.train`: rank 16, alpha 32, dropout 0 and learning rate 0.0002.
- That is the default declaration. It does not replace each run's own record, which is in its experiment commit and is not published.
- The declaration's `todo.eval` block holds the settings the validation stages read: the model revision, temperature 0 and a 256-token limit. It also contains `split: sealed-test`, `release: DRAFT` and two thresholds. Those entries do not establish that an evaluation ran or that a model met the selection rules. No sealed-test evaluation has run, and the release entry is a placeholder. The scripts that read this block are not published. The study's owner checked them at the same source commit.
  - `exact_min: 0.95` and `false_action_max: 0.01` are not the to-do rule. They have the same values as the thresholds of the study's separate hypothesis for the desk task: at least 95% exact, and false actions at most 1% by the upper end of a 95% interval. The to-do rule of zero wrong destructive actions is applied by the selection rule, not by this entry. The study's owner found nothing in the to-do scripts that reads these two entries.
  - `desk.eval.thresholds` in the published `params.yaml` has the same two values, `exact_min: 0.95` and `false_action_max: 0.01`.

## Why this example

- This study is an attempt at [the second stage](premise.md#treat-it-as-a-software-problem): a small open model, tuned for one task, with a test it has to meet.
- Each request has a known right answer, so every call can be scored.
- A to-do list has actions that can do damage, such as marking the wrong task done. That gives the rule of zero wrong destructive actions something real to count.
- There is no delete tool, and runs are scored against a disposable test list, never a real one.
- The requests are synthetic, so no person's data is in them.
- It starts from an earlier study's data and system, kept unchanged, so the earlier model is a reference that does not change.
- The model is small enough to run on one local machine. Its file is on local disk, so it can be pinned.
- This study has not shown a cost advantage, and it has not shown that the small model matches a large one. [Neither was measured](measured.md).

## License and citation

- [`LICENSE`](https://github.com/ohpcsim/tool-call-tuning/blob/main/LICENSE) in the repository says the site's text and figures are licensed under Creative Commons Attribution 4.0 International, CC BY 4.0. It says the code is licensed under the MIT License: `build_site.sh`, `check_site.py` and the code on the site's pages.
- `myst.yml` declares the same two licenses: CC-BY-4.0 for content and MIT for code.
- The files under `pipeline/` are copies of the study's own files. `pipeline/SCREENING.md` says its content screen is not a license determination, and that the study's private repository has no license file. It says the site's license was not copied and does not determine rights in these study files.
- Cite it as: "Tuning a small model to call tools", https://ohpcsim.github.io/tool-call-tuning/, the record of a study for the talk "Doing Real Work with LLMs" at SC26, November 16, 2026.

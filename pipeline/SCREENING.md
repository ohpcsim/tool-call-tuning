# Screened pipeline and registry copies

Edited for publication: the owner's name was replaced with 'the study's owner', and the sentence that explained that name as an exception to the screen was removed. No other change.

Source: the study's private repository.
Source commit: `4f0f92e58787a01bba6a7a573d598e54863ef8ec`.
Preparation date: 2026-11-12, US Eastern time.

After the requested fetch, `origin/main` still resolved to that exact commit. File contents and the registry CSV cross-check use Git objects at that commit, not checkout files. Registry tag metadata comes from the fetched local tag refs on the preparation date; tags are separate from the commit tree. No amendment branch was read, no source checkout was changed, and nothing was published.

These copies passed a content screen. That is not publication approval or a licence determination; the study's private repository has no licence file, and the study's owner decides what is published.

The pipeline shown is the merged version 1 pipeline. The proposed amendment's stages are not merged or signed and are not included.

## Files and screen results

SHA256 values describe the exact delivered bytes. Generated files have no source-file counterpart. Content screening covered absolute paths, hosts, personal and account identifiers, email addresses, storage identifiers, remote addresses, credential settings, coordination identifiers, request text, item identifiers and answer arguments. The personal-data screen used the required installed checker without printing its denylist.

| File | SHA256 | Relationship to source | Content screen | Personal-data screen | Gitleaks matches |
| --- | --- | --- | --- | --- | ---: |
| `studies/todo/dvc.yaml` | `8307ae2413e55027d5a32ea761ef0a11b35b0a6ab4a5dbf65243f3a220905b9c` | Byte-identical | Pass | Pass | 0 |
| `params.yaml` | `78d692d672736e9d2bf22ee16cf90bff018278ca42f0463a9df4314fcfa40a3f` | Redacted | Pass | Pass | 0 |
| `studies/todo/dvc.lock` | `f6a5a4828c5d91f9c872d91787d6d5867ad55537868a3cf1312c8e82afe6c63d` | Redacted | Pass | Pass | 0 |
| `src/todo/select.py` | `15467423e9fdbef8760d798eadc7aae003adb94d7f308096012d4802934dee7f` | Byte-identical | Pass | Pass | 0 |
| `src/todo/split.py` | `7d993a88577f48de5b1e60e642c3134310baaba0a462b673f55445865a1421c6` | Byte-identical | Pass | Pass | 0 |
| `registry/versions.txt` | `0cd40e038e286fb66123b6e170f3cf7107aeed5cd6e4dd7aac6bb5ad7cc2707f` | Generated; no redactions | Pass | Pass | 0 |
| `registry/README.md` | `065b0f942ce54b63b30628774fbc85c553267866dbd62ed5461736aafe2d9deb` | Generated; no redactions | Pass | Pass | 0 |
| `README.md` | Final-byte SHA256 is in the completion report | Generated; no redactions | Pass with required wording below | Pass | 0 |

This README's final-byte SHA256 accompanies the completion report. Inserting its own digest here would change the bytes being hashed.

Gitleaks scanned this directory with the project configuration, full redaction, default rules enabled and no added suppressions. It reported **0 matches** across all eight files. There are therefore no findings to classify as secrets or content hashes. The long hexadecimal values present are file and directory content hashes, Git object identifiers, and public model revisions; none is a credential.

The `artifacts:` block still contains provenance hashes from the source, including the source lockfile hash. Those values were not rewritten to match the redacted copy.

## Redactions

Each replacement changes one entire scalar value to the literal `<redacted>`. Line numbers are one-based and unchanged between source and copy. Removed values are not reproduced here.

| File | Line | Description |
| --- | ---: | --- |
| `params.yaml` | 92 | Evaluation endpoint URL value. |
| `params.yaml` | 141 | Evaluator placeholder containing an internal role identifier. |
| `params.yaml` | 144 | Archive repository URL value. |
| `params.yaml` | 199 | Evaluation endpoint URL value. |
| `params.yaml` | 202 | Evaluator placeholder containing an internal role identifier. |
| `studies/todo/dvc.lock` | 392 | Archive repository URL value. |

The parameters file has five redactions; the lockfile has one. No other delivered file has a redaction. The source parameters SHA256 is `d0e8dff51b97eb53fe45cb4430ca9f42dffb7b12e5e78588106b6af09d5baaef`; the source lockfile SHA256 is `47ce2d64454d17c30e1ea9fb29116fb90ee6f9e73705bea001893ea44be960bd`.

## What the lockfile names

The lockfile records seven stages: `import-a8`, `split`, `leakcheck`, `environment`, `exec-check-t-new`, `exec-check-t-repro`, and `report-leakcheck`. It contains commands, parameter values, dependency and output paths, hashes, byte sizes and directory file counts. It does not contain the referenced data or models.

The only custody export it names is the open historical validation export `data/custody/a8-v4-validation.jsonl`. No listed path names a sealed test, a test-release record, a final-evaluation output or a custody payload outside that open export. This check covers the names in the lockfile; hashed directories were not opened or expanded. The imported A8 directory and base-model directory are recorded as directory hashes.

Its 45 distinct dependency and output paths are:

```text
configs/launcher.yaml
data/custody/a8-v4-validation.jsonl
data/todo/a8-import-receipt.json
data/todo/a8-train.jsonl
data/todo/a8-val.jsonl
data/todo/a8/arm1-e3
data/todo/dev-corpus.jsonl
data/todo/env.json
data/todo/leakcheck.json
data/todo/t-new/exec-check.json
data/todo/t-new/requests.jsonl
data/todo/t-new/split-membership.json
data/todo/t-new/split-receipt.json
data/todo/t-new/train-requests.jsonl
data/todo/t-new/train.jsonl
data/todo/t-new/val.jsonl
data/todo/t-new/validation-rows.jsonl
data/todo/t-repro/exec-check.json
data/todo/t-repro/requests.jsonl
data/todo/t-repro/split-membership.json
data/todo/t-repro/split-receipt.json
data/todo/t-repro/train-requests.jsonl
data/todo/t-repro/train.jsonl
data/todo/t-repro/val.jsonl
data/todo/t-repro/validation-rows.jsonl
docs/protocol/frontier-rulebook-v1.md
docs/protocol/protocol-v1.md
metrics/todo-leakcheck.json
models/base
pyproject.toml
src/desk/base.py
src/desk/environment.py
src/desk/leakcheck.py
src/desk/leakreport.py
src/desk/scorer.py
src/todo/common.py
src/todo/exec_check.py
src/todo/import_a8.py
src/todo/leakcheck.py
src/todo/split.py
studies/shared/base-manifest.json
studies/todo/a8-system
studies/todo/archive-imports.yaml
studies/todo/arm1-manifest.json
uv.lock
```

## Registry cross-check

`registry/versions.txt` contains 35 annotated tags: 12 version registrations, 15 experiment-stage assignments, four older rejected-stage assignments and four rejected-stage unassignments. The versions are four desk versions, seven to-do versions and one A8 baseline version. Every version tag's target commit matches `reports/mvp-20261017/tables/registry.csv` at the source commit, and all 12 rows in that report have stage `experiment`.

Each desk version has an older `rejected` assignment followed by a `rejected!` unassignment and an `experiment` assignment on 2026-10-13. Three to-do versions have repeated experiment assignments, so assignment count differs from version count. The latest recorded assignment for every registered version is `experiment`. Tag dates are tagger dates with their recorded timezone offsets, not commit dates. Annotation messages, author identities and email addresses were not read or copied.

## What a reader can rerun

No DVC stage can run from these public copies alone. Every stage declares the omitted A8 system, and the common prerequisites include omitted package metadata, launcher configuration, supporting modules and protocol documents. The two scripts are source excerpts, not standalone programs: `select.py` imports the omitted shared selection rule and provenance helpers, and `split.py` imports omitted data-import and grouping helpers.

| Stage | Required material not included in these public copies |
| --- | --- |
| `import-a8` | The imported A8 archive and frozen adapter, the A8 system, the base model, import code and manifests. This stage is frozen. |
| `split` | The imported A8 requests and labelled rows, import receipt, base model, open historical validation export, A8 system and supporting modules. |
| `leakcheck` | Training and validation requests and the split receipt for t-new, the A8 system, and leak-check and fingerprint helper modules. |
| `environment` | The environment module, launcher and dependency metadata, A8 system, scorer and protocol files. Even this stage lacks declared dependencies. |
| `exec-check-t-new` | The execution-check module, A8 system, t-new validation requests with answer keys, and split receipt. |
| `exec-check-t-repro` | The execution-check module, A8 system, t-repro validation requests with answer keys, and split receipt. |
| `train` | The training modules and environment, imported A8 data and system, base model, pool training and validation data, receipts, attestations, seal metadata, and three open historical exports. |
| `val-eval` | The trained adapter for the selected arm and attempt, base model, imported A8 data and system, pool validation requests and answer keys, execution-check receipt, evaluation modules and training prerequisites. |
| `val-reference` | The base model, imported A8 data and system, validation requests and answer keys, execution-check receipt and evaluation modules. It evaluates the base reference rather than a newly trained adapter. |
| `val-a8` | The imported A8 frozen adapter and system, base model, validation requests and answer keys, execution-check receipt and evaluation modules. |
| `select` | The shared selector and provenance helpers, A8 system, t-new validation requests and answer keys, reference and candidate validation metrics, t-repro reference and control metrics, and A8 control metrics. The copied wrapper also verifies the winning adapter files. |
| `final-eval` | The selected result, trained adapters, A8 frozen adapter and system, base model, release and seal records, sealed requests and answer keys, released outputs and evaluator modules. |
| `report` | The final-evaluation output, report and scoring modules, A8 system, archive manifest and protocol files. |
| `report-leakcheck` | The leak-check output, report module, A8 system, scorer, launcher and protocol files. |
| `frontier-report` | The selected result, adapters and base model, A8 system, seal and test-release records, sealed requests and answer keys, frontier outputs and reporting modules. |
| `family-report` | The frontier-stage prerequisites plus family and cross-family outputs, cross-family release and seal records, and cross-family test data. |
| `reproduction-train` | The training-stage prerequisites, imported A8 data and system, base model, original adapter snapshot, reproduction module and reproduction parameters. |
| `reproduction-val` | The reproduction-trained adapter and original adapter snapshot, base model, imported A8 data and system, pool validation requests and answer keys, execution-check receipt, evaluation and reproduction modules. |

The private DVC remote and its configuration are not supplied. Fetching missing tracked data or models requires authorized access to that remote or another authorized source; a lockfile supplies hashes, not the bytes. A stage can use an already populated local cache without a remote, but these copies include no cache. The base model has a public revision identifier, but its weights and the original acquisition and environment files are not in this bundle. No model was downloaded.

Read-only inspection of the public site's `results.md`, `build_site.sh`, `myst.yml`, `requirements.txt` and build workflow establishes that its Jupyter Book pages and four result tables rebuild from public sources and declared build dependencies. The executable cells read `data/tables/todo.csv`, `desk.csv`, `registry.csv` and `cost.csv` to produce the to-do, desk, registered-version and cost tables. The two result figures are included SVG files, not regenerated plots. This site build does not rerun training, scoring, inference or any study DVC stage. No site build or deployment was run for this preparation.

## What was left out and why

No requested file was excluded by the screen. The parameters file belongs at repository-root `params.yaml`; there is no `studies/todo/params.yaml` at the source commit. The pipeline's variable import points to the root file.

Only `src/todo/select.py` and `src/todo/split.py` are supplied as scripts. Training, evaluation, scoring, generator, contract and gate code, all other scripts and helpers, and every file under `studies/todo/a8-system` are not provided, as requested. The selection excerpt checks the candidate pool and delegates the numerical selection rule to omitted `src/desk/select.py`; it is not the full shared selector implementation.

Imported A8 data, all request and answer-key content, item-level results, models and adapters, validation outputs, sealed tests, test releases, final-evaluation outputs, custody payloads and fingerprints are not provided. The copied pipeline can name their dependency paths without supplying or opening them. DVC configuration, credentials, remote settings, tag annotation messages and the unmerged amendment are also excluded. The public site's licence was not copied and does not determine rights in these study files.

## Checks and limits

Checks covered source-commit equality after fetch, exact byte comparisons for the three unmodified files, complete value-only diffs for both redacted files, YAML parsing, the registry CSV and tag targets, all declared stages, all paths in the lockfile, the content screen, the personal-data checker and gitleaks. The source root tree has no licence file.

No DVC command, model, server or GPU was run. No private payload directory, sealed test, answer key or item-level prediction file was opened. No source worktree was created. Package installation, the website build, deployment, scientific results, tag signature validity, directory-hash contents, remote accessibility, publication approval and licensing rights were not checked.

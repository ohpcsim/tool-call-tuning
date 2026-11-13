# Data sources

These 17 files are the study's report files on this site. The pipeline and registry files under `pipeline/` are listed in `pipeline/SCREENING.md`. The 17 files are aggregate tables and figures from the study's October open-validation report. They hold no individual requests, answers or test items.

Source: the study's private repository, commit `4f0f92e58787a01bba6a7a573d598e54863ef8ec`, directory `reports/mvp-20261017/`. The commit is an identifier. It does not resolve for readers outside the study.

Copied on November 12, 2026, from a fresh clone checked out at that commit. The clone was deleted after copying.

| SHA256 | File |
| --- | --- |
| `d1ec9fb5e5e826b9599a276e341db36cf3e017a956331f84f45ebcc92208477a` | `figures/desk-accuracy-safety.svg` |
| `93683700345714e357ddba640ac4516295f6c17caf2f77a74f711600ab0d94bc` | `figures/desk-lineage.mmd` |
| `020d8e93ace2f216b85f6c70116cfb4d5e895ee580cd0ac478b79d619d992168` | `figures/experiment-graph.svg` |
| `0cbed96122294b96bae729e141bde109818360e1a893c1bda86fce7f19144dbf` | `figures/todo-accuracy-safety.svg` |
| `ef42b16367ad8bd5cdd504d707c990cd82b6d82936c4185eb3f3194b7d5e92b2` | `figures/todo-lineage.mmd` |
| `4ea90c4fba9075b6370bd95068cafbe6af43541c4b10dd8a41ac830737411fbe` | `tables/cost.csv` |
| `e3b43d93ded65c7f83b33b6ece1186fe5e044a8d0e631dfdb92344cdc8c3e207` | `tables/desk.csv` |
| `36e8c4031691a4ea6e6d3a58d104626c5a2c97ad2276498f2d9efeaee7d6304f` | `tables/desk-display.csv` |
| `4f329aa522b79e4ef004786b443a7bc2dbd1da1045ab3fede1a38d4789819293` | `tables/desk-lineage-edges.csv` |
| `484880a2f3e83441ca4382d0a67f72995b6255e4e682f47fd36fb36f137769f5` | `tables/desk-lineage-nodes.csv` |
| `18e20a15ac1d805ab0a17c8914113644f873f2bf017370e920f058fbc5bfe448` | `tables/dvc-exp-show.csv` |
| `439d4e1f6ebef41335d4a4aa2d2eba693c7a42faca5fff272f86feb9553cea95` | `tables/experiment-graph.csv` |
| `8416a04d02836e562ee24a5d35959143c705da421094b8a7120bca7393720339` | `tables/registry.csv` |
| `241a9342af6b4107b52c4f9b75f691be46aeeecf115df8def5e7757a236c9889` | `tables/todo.csv` |
| `17f2bf3aebd4f65e50968e6201cbe79d576b1f6dc9abe580991366eb6ee9907a` | `tables/todo-display.csv` |
| `d1103596a19170c9fa2fcd73a461bb8c56f067d730b7457e4a6782a755cfce7c` | `tables/todo-lineage-edges.csv` |
| `6bd3ef4593a494a772031fe881fe0b2ba62f2a6b2e1ebfcb302589c99f717197` | `tables/todo-lineage-nodes.csv` |

## Labels each file needs

Every display of these files needs the report's banner: "Working benchmark: open validation only; not held-out; no confirmatory claim". The figures and diagrams already show it. The CSV files have no comment lines, so the pages that show them add it.

- `todo-accuracy-safety.svg`, `todo.csv`, `todo-display.csv`. The t-a8 row is a control, never a candidate. Its score is optimistic, because its earlier training overlaps this validation set.
- The same todo files, t-repro rows. These use 500 requests, not 613. They are descriptive controls outside selection. Don't compare them with t-new rows or read them as a count of 613.
- The same todo files, wrong destructive counts. These are before the added argument and date check. That check's numbers come from the study's amendment, not from these files.
- Todo latency. It includes replay calls to every request group, so it is a diagnostic, not production latency. The t-repro rows also fall short of the protocol's 600-observation minimum.
- The shaded regions in both accuracy figures mark only the zero-count rule, not every selection rule.
- `desk-accuracy-safety.svg`, `desk.csv`, `desk-display.csv`. Desk "wrong destructive = 0" is zero by construction, because the study scores desk proposals without executing them. Do not present it as a safety result.
- The same desk files, "clarify recall". It is a fallback measure, (210 minus false actions) out of 210. It does not measure how well the model writes a clarifying question.
- The same desk files, "0/0" off-topic. That category is empty.
- `registry.csv`, `experiment-graph.csv`, `experiment-graph.svg`. "experiment" is a tracking stage. It does not mean a model was chosen or promoted. todo-model v0.0.7 is the retrain from a fresh clone, whose recorded verdict is NOT REPRODUCED. baseline-a8 is reconstructed.
- Commit hashes and experiment refs in those files point into a private repository. They are identifiers, not links.
- `cost.csv`. These are training job wall-clock minutes, not measured GPU use. Validation GPU time was not recorded. The totals leave out a failed desk retry, the earlier reference model's original training and the retrain runs.
- `dvc-exp-show.csv`. The d-base row says "historical select input". The t-base and t-a8 rows share the selection record's commit. Neither row is its own trained experiment.
- `desk-lineage.mmd`, `todo-lineage.mmd` and the four lineage CSV files. They show the pipeline's declared dependencies, not stages that ran. The desk graph also contains todo import nodes and a retraining node. The graphs end at `select`. `final-eval` has not run. The names data/custody and custody.dvc refer to pinned open historical exports. They do not refer to the sealed test, which was never in the repository.

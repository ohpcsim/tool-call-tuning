---
title: Tools and documentation
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

- This page lists the tools the study's pages name.
- Each row says what the tool is, where it is used, and where its official documentation and introduction are.
- This site does not teach the tools.

## Code

| Tool | What it is | Where it is used | Documentation | Start here |
|---|---|---|---|---|
| Git | Version control. It records each change to a project as a commit. | The study's code and records live in a Git repository, and Git tags register its model versions. | [Reference](https://git-scm.com/docs) | [About version control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control), from the Pro Git book |
| GitHub | A service that hosts Git repositories. | It hosts [this site's repository](https://github.com/ohpcsim/tool-call-tuning). | [GitHub Docs](https://docs.github.com/en) | [Hello World](https://docs.github.com/en/get-started/using-github/hello-world) |

## Environments

| Tool | What it is | Where it is used | Documentation | Start here |
|---|---|---|---|---|
| uv | A Python package and project manager, written in Rust. | All 18 stages in [the study's pipeline file](project.md#the-declarations) list `pyproject.toml` and `uv.lock` as dependencies. Those two files are not published. Six stages also list `envs/train/pyproject.toml` and `envs/train/uv.lock`. | [uv documentation](https://docs.astral.sh/uv/) | [Getting started](https://docs.astral.sh/uv/getting-started/) |

## Workflows

| Tool | What it is | Where it is used | Documentation | Start here |
|---|---|---|---|---|
| DVC pipelines | `dvc.yaml` declares each stage's command, inputs, parameters and outputs. DVC uses the declared dependencies and outputs to decide which stages need to run. | The study's 18 stages, in [the pipeline file](project.md#the-declarations). | [Pipelines](https://doc.dvc.org/user-guide/pipelines) | [Get started: data pipelines](https://doc.dvc.org/start/data-pipelines/data-pipelines) |

## Data and models

| Tool | What it is | Where it is used | Documentation | Start here |
|---|---|---|---|---|
| DVC | Data Version Control. Git keeps small pointer files, and the data goes to a separate store. | The study's lock file records the hash and size of the files its recorded stages read and write. The data is in a private DVC remote and is not published. [The declarations](project.md#the-declarations). | [DVC documentation](https://doc.dvc.org/) | [Get started](https://doc.dvc.org/start) |
| GTO | Git Tag Ops, an open-source tool from Iterative, which created DVC. It records model versions and stages as Git tags, so the registry lives in the repository. | The model registry. The study has 12 registered versions, all at the tracking stage `experiment`. [The results page](results.md#registered-versions) lists them, and [the declarations](project.md#what-the-registry-versions) show the tags. | [GTO documentation](https://mlem.ai/doc/gto) | [Get started](https://mlem.ai/doc/gto/get-started) |
| pandas | Data tables for Python. | The results page reads the study's data files and builds its tables with it. | [pandas documentation](https://pandas.pydata.org/docs/) | [Getting started](https://pandas.pydata.org/docs/getting_started/index.html) |
| matplotlib | Plots for Python. | The results page draws its first figure with it in the build. | [matplotlib documentation](https://matplotlib.org/stable/) | [Quick start](https://matplotlib.org/stable/users/explain/quick_start.html) |

## The model and the task

| Tool | What it is | Where it is used | Documentation | Start here |
|---|---|---|---|---|
| FunctionGemma | An open model with 270 million parameters. | It is the base model the study tuned. | [FunctionGemma model overview](https://ai.google.dev/gemma/docs/functiongemma) | [Model card](https://huggingface.co/google/functiongemma-270m-it) |
| LoRA | A way to tune a model. It leaves the base model's weights unchanged and trains a small set of added weights, called an adapter. | The study trained separate adapters for 1, 2 and 3 epochs. | The paper: [Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models", arXiv 2106.09685](https://arxiv.org/abs/2106.09685) | [LoRA conceptual guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora), from Hugging Face PEFT |
| Taskwarrior | A command-line to-do manager. | The tuned model makes tool calls for it. Runs are scored against a disposable test list, never a real one. | [Taskwarrior documentation](https://taskwarrior.org/docs/) | [30-second tutorial](https://taskwarrior.org/docs/30second/) |

## Documentation

| Tool | What it is | Where it is used | Documentation | Start here |
|---|---|---|---|---|
| Jupyter Book (mystmd) | Builds a website from Markdown files and notebooks. Jupyter Book 2 runs on mystmd, the MyST Markdown tools. | It builds this site and reruns the code on the results page. [How this site is built](build.md) has the details. | [Jupyter Book](https://jupyterbook.org/stable/), [MyST guide](https://mystmd.org/guide) | [Get started with MyST](https://mystmd.org/guide/quickstart) |
| Mermaid | Diagrams written as text. | The lineage diagram on [the project page](project.md#the-pipeline) and the diagram on [How this site is built](build.md). | [Mermaid documentation](https://mermaid.js.org/) | [Introduction](https://mermaid.js.org/intro/) |
| GitHub Actions and GitHub Pages | GitHub Actions runs a workflow when a repository changes. GitHub Pages serves a website from a repository. | A GitHub Actions workflow runs the build and the check on every push to `main`, then publishes the built site to GitHub Pages. | [GitHub Actions](https://docs.github.com/en/actions), [GitHub Pages](https://docs.github.com/en/pages) | [Quickstart for GitHub Actions](https://docs.github.com/en/actions/get-started/quickstart), [Quickstart for GitHub Pages](https://docs.github.com/en/pages/quickstart) |

## Hands-on material

- The fundamentals site, [Reproducibility in AI](https://ohpcsim.github.io/reproducibility-in-ai/), has hands-on material for these tools, including versioned data and pipelines with DVC and a model registry.

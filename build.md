---
title: How this site is built
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

::::{figure}
:label: how-built
```{mermaid}
flowchart TD
	repo["One repository: pages, myst.yml, data CSV files, pipeline files, requirements.txt"]
	push["Push to main"]
	actions["GitHub Actions"]
	build["build_site.sh with --execute --strict: the results tables and one figure are rebuilt from the CSV files"]
	check["check_site.py"]
	pages["GitHub Pages"]
	repo-->push
	push-->actions
	actions-->build
	build-->check
	check-->pages
	classDef default fill:#E6F2FA,stroke:#0072B2,color:#222
```

How this site is built, checked and published from one repository.
::::

- The steps in the figure, as text. A push to `main` starts GitHub Actions. `build_site.sh` rebuilds the results page from the CSV files with `--execute --strict`. `check_site.py` checks the built pages. GitHub Pages serves them.

## What this site is

- [The results page](results.md) is the literate-science example. On every publish, it rebuilds its tables and one figure from the study's aggregate data files.
- The other pages are written by hand. A number that is not in the data files names its source on the page that reports it.
- The site follows its own advice: everything it needs is declared in the repository, it rebuilds from a clean state, and the build fails if a cell raises an error, a cross-reference breaks, a table differs from the data or a registry tag differs from the registry table.
- It holds aggregate results and [the study's pipeline and registry declarations](project.md#the-declarations). A reader can rebuild the site and its tables, but can't rerun the study's training or scoring, because the requests, answer keys, training code and model files aren't published.
- It isn't a research publication. It is the record of a working benchmark, open validation only, with [its limits](measured.md) stated.

## The tools

- This site is a project too. Its pages, its configuration and the automation that builds it are in [one repository](https://github.com/ohpcsim/tool-call-tuning).
- [Jupyter Book 2](https://jupyterbook.org/stable/) builds it, on [mystmd](https://mystmd.org/guide).
- The code on the results page reruns in the build, so its tables come from a real run.

## The configuration

`myst.yml` names the pages, their order and the theme.

```{literalinclude} myst.yml
:language: yaml
```

## Build it on your own machine

- One command builds the site into `_build/html` from a clean state. It creates a Python environment from `requirements.txt` if one is missing. That file pins every package version. The script reuses an existing environment. If `requirements.txt` changes, delete `.venv` before building again.
- The publishing workflow uses Python 3.12 and Node.js 22. Local Python needs the venv module.

```bash
./build_site.sh
```

- The script builds with `--execute --strict`. `--execute` runs the code on the results page. `--strict` turns every warning into a failure.

```{literalinclude} build_site.sh
:language: bash
```

- A second command checks the built site.
- It fails if a table on the results page differs from the data files, or if a page lacks the banner.
- It also checks page text against the study's restricted result words and patterns for local paths, machine addresses and session identifiers. A maintainer can add private names in a local file that is not in the repository. The workflow on GitHub runs without that file.
- It scans the text inside the built site's SVG figures for the same words and patterns.
- It runs the path and address check on the published text files under `pipeline/` and `data/` too.
- It checks that the base and tuned correct counts, 156, 596, 606 and 609, appear on the home page and that each gate-table row's before counts match `todo.csv`. It does not check the home page's count labels or denominator, or the gate's replay counts.
- It fails if a sentence says a model, run or system passes or meets a rule. No amended selection has been run or signed.
- It fails if the registry check's printed line is missing from the results page.
- It fails if the results page's zero-count line differs from `todo.csv`, if its registered-versions line differs from `registry.csv`, or if a code cell on that page raised an error.

```bash
.venv/bin/python check_site.py
```

- [`check_site.py`](https://github.com/ohpcsim/tool-call-tuning/blob/main/check_site.py) is in the repository.

- The data files and their checksums are listed in [`data/SOURCES.md`](https://github.com/ohpcsim/tool-call-tuning/blob/main/data/SOURCES.md) in the repository.

## The automation on each push

- A GitHub Actions workflow runs the same build and the same check on every push to `main`, then publishes `_build/html` to GitHub Pages.

```{literalinclude} .github/workflows/site.yml
:language: yaml
```

## Other tools that do this

- [Quarto](https://quarto.org/docs/projects/code-execution.html) renders websites from notebooks and Markdown with executable code, and can store results so a full render doesn't rerun them.
- [Sphinx](https://www.sphinx-doc.org/en/master/) with [MyST-NB](https://myst-nb.readthedocs.io/en/latest/computation/execute.html) runs notebooks during the build and caches their outputs. Errors fail the build only with `-W` or `nb_execution_raise_on_error`.

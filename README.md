# Tuning a small model to call tools

> Working benchmark: open validation only; not held-out; no confirmatory claim

The literate-science record of a small study: can FunctionGemma, a 270-million-parameter open model, tuned on examples, turn a plain request into the right Taskwarrior call without a destructive action nobody asked for? It accompanies the talk "Doing Real Work with LLMs" at SC26 on November 16, 2026.

**Read it here: https://ohpcsim.github.io/tool-call-tuning/**

The site is a Jupyter Book 2 project. The results page rebuilds its tables and one figure from the CSV files in `data/` on every build. The repository holds aggregate results, the study's pipeline and registry declarations and two of its scripts. It can rebuild the site and its tables but cannot rerun the study's training or scoring. To build and check it locally:

```sh
./build_site.sh
.venv/bin/python check_site.py
```

Every push to `main` rebuilds the site with GitHub Actions and publishes it to GitHub Pages.

Text is licensed CC BY 4.0 and code MIT, as `LICENSE` says.

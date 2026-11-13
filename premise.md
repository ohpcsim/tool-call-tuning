---
title: The premise
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

## Problem statement

- LLMs are now part of how research gets done.
- When a model shapes a result, the model is part of the method, and a method has to be something another person can check.
- Work driven from a laptop with Claude or ChatGPT is very stateful.
- Two questions test that. If the chat or the laptop were lost, could the work resume? If the model changed tomorrow, could the result be produced again?

**The starting point: own the model**

- One answer is to own the model: open weights, run on your own hardware.
- That gives control, and it matters because a hosted model can change behind its name.
- Vendors document routers, safety classifiers and swapped versions behind a model's name. The talk cites Anthropic, OpenAI and Google documentation. Anthropic's page is [Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions).
- A named service was measured changing its behavior between releases ([Chen, Zaharia and Zou, "How is ChatGPT's behavior changing over time?", arXiv 2307.09009, 2023](https://arxiv.org/abs/2307.09009)).
- A result from a closed model can't be checked by rerunning it in the conventional way, so using one in research needs explicit justification ([Palmer, Smith and Spirling, "Using proprietary language models in academic research requires explicit justification", Nature Computational Science, 2023](https://www.nature.com/articles/s43588-023-00585-1)).

**What changed**

- Two things complicate that answer.
- Large open models are expensive to run, and requiring them splits research into groups that can pay and groups that can't.
- Small local models are cheap. Tuned for one task, they may be enough. This study tests that.
- Researchers also already use commercial tools.
- A 2026 preprint measured Harvard's FASRC cluster from July 7 to August 1, 2026: 19.5% of observed users ran coding agents, and those users accounted for 55.8% of jobs ([Zheng et al., "Towards Efficient HPC Systems for Agents: Challenges and Opportunities", arXiv 2609.38723](https://arxiv.org/abs/2609.38723)).

**So the question changes**

- The question was "which model to control?" It is now "how do you do reproducible science with a model you don't control?"

(ai-workflows)=
## AI workflows

An AI result depends on:

- Software you develop. It should be version controlled with Git.
- Software you consume.
- Workflows you develop.
- Data you collect or use.
- LLMs you use: the model, its version, how it was served, the instructions it was given and the tools it could call.
- Conclusions you draw from all of the above.

## Treat it as a software problem

- Everything around the model is software.
- A hosted service can't be pinned, but the instructions, the tool definitions, the tests and the record of decisions can be versioned, tested and reviewed like any other code.
- The talk calls the file that holds the instructions a contract file. `AGENTS.md` is one common file name.
- Decisions and results belong in the project, not in a chat.
- None of these practices was designed for LLMs. They were already how the other work was done.
- The approach is defensible and promising. It is not proven.

**Two stages**

- The problem statement asked two questions. Each one is a stage.
- The first stage answers the lost chat. The record lives in the project, so another person or another model can continue from it.
- The second stage answers the changed model. It pins the model too: a small open model, tuned for one task, with a test it has to meet, used for that task in place of a large and expensive model.
- A hosted model can't be pinned. A model file on local disk can.
- A pinned model file is kept and versioned, like the other files.
- This study is an attempt at the second stage. The site shows how far it got and what failed.

**Coding agents**

- A coding agent is a program that lets a model work in a folder. It reads the files, runs commands and proposes edits. Claude Code and Codex are examples.
- The work happens in the project, so the project can keep it.

**Repeatable and reproducible**

- Repeatable execution: run it again, get the same outputs.
- Reproducible conclusion: the answer holds when someone else checks it.
- [Same weights, not always the same outputs](serving.md) is about the gap between the two.

## Literate programming to literate science

**Literate programming**

- Donald Knuth developed literate programming in 1984, while he was writing TeX.
- A program is one document, for people and for the machine.
- Weave makes the document readable. Tangle makes it run.
- Knuth wrote: "Instead of imagining that our main task is to instruct a computer what to do, let us concentrate rather on explaining to human beings what we want a computer to do."

**Literate science**

- Literate science applies the same idea to the whole result, and not only to the program.
- The claims, the code, the environment and the data live in one project.
- Published results come from running the project, not from pasted output.
- When the data or the code changes, a rebuild recomputes the numbers.
- If the code breaks, the build breaks.
- Earlier work: Claerbout and Karrenbach (1992) on reproducible electronic documents, and Buckheit and Donoho (1995) on WaveLab.
- The step the fundamentals site, [Reproducibility in AI](https://ohpcsim.github.io/reproducibility-in-ai/), adds is doing it with cloud-native tools, which are stateless and declarative.

**Literate science for LLM work**

- An LLM result depends on more than code and data. [AI workflows](#ai-workflows) lists the rest.
- Serving means running the model so that it answers requests.
- Each of those belongs in the project record, next to the claims that rest on it.
- The framework is the idea above. The tools and the way this study used them are one implementation, open to discussion.

## Cloud-native and the history of \*Ops

- Cloud-native applications are designed to run in dynamic, distributed environments.
- They rely on automation, they scale, and they recover from failures.
- Cloud-native is an architectural approach. It means more than running in the cloud.

**Declarative**

- You specify what you want, not how to get it.
- The system works out the steps to reach that state.
- Examples are Docker Compose, Kubernetes manifests and conda's `environment.yml`.

**Stateless**

- A job keeps nothing on the node between runs.
- Inputs and results live in Git and object storage.
- Any node can rerun any job.

**The history of \*Ops**

- \*Ops, or "splat ops", applies ideas from DevOps to everything else.
- DevOps treats operations as a software development project.
- DataOps: data has versions, and pipelines are declared steps. [The lock file](project.md#the-declarations) records the hash and size of the files its recorded stages read and write.
- Workflows: each analysis step declares what it reads and writes, so a tool reruns only what changed. [The study's 18 declared stages](project.md#stages).
- GitOps: the declared state lives in Git, and automation makes the system match it. [This site's workflow](build.md#the-automation-on-each-push) publishes what is in Git.
- MLOps and LLMOps: models and prompts are versioned, tested and released like software. [The registry tags](project.md#what-the-registry-versions) version the to-do adapters.
- The fundamentals site, [Reproducibility in AI](https://ohpcsim.github.io/reproducibility-in-ai/), has an exercise for each.

Timeline:

1. 2009, DevOps: the first DevOpsDays, in Ghent, organized by Patrick Debois.
2. 2014, DataOps: the term is credited to Lenny Liebmann, and Andy Palmer popularized it in 2015.
3. 2017, GitOps: Weaveworks, "Operations by Pull Request".
4. Today, MLOps and LLMOps: the same ideas for models and prompts. There's no single origin year. An early paper on the problem is Sculley et al., ["Hidden Technical Debt in Machine Learning Systems"](https://research.google/pubs/hidden-technical-debt-in-machine-learning-systems/), NeurIPS 2015.

## Pets vs cattle

**The "pets" approach: a hand-built environment**

- Custom builds that "just work" on one system.
- SSH into specific nodes and hand-tune environments.
- Fear of losing a carefully curated environment, or work that lives only in a chat.
- When something breaks, you diagnose it, repair it and nurse it back to health.

**Cloud-native, the "cattle" approach**

- Servers have numbers, not names.
- Automation configures them identically.
- When something breaks, you terminate it and replace it.
- Any compatible node can run the workload.

**Why this matters for academic HPC**

Today:

- Long-running simulations run on specific nodes.
- Custom software builds "just work" on one system.
- People fear losing carefully curated environments.

The goal:

- Environments are defined in code and rebuild the same way.
- They're portable across a laptop, an HPC system and the cloud.
- Failures show up early, and recovery is quick.
- Collaborators share the same definitions.

**You don't have to choose one or the other**

- Computational infrastructure is cattle. You can throw it away and replace it.
- Your data is a pet. Keep and version it.
- Built files, such as figures and intermediate tables, are cattle. Rebuild them from the code and data.
- Software environments are declarative definitions under version control.
- Your research products (papers, code, data) are the pets. Everything that runs them is cattle.
- In LLM work, the project is the pet: the instructions, the tool definitions, the tests, the decision records and the data.
- The running model and the coding agent that runs it are cattle. Swap either one. The files stay, and the work continues.
- In the second stage, a pinned model file is kept and versioned, like the other files. [The registry listing](project.md#what-the-registry-versions) shows this study's versions.
- Chat state is not settled. Decisions and results belong in the project. Restoring a session in another coding agent is still open.

## Thesis

"Bringing cloud-native, declarative, and stateless concepts to computational workloads solves most problems."

- Interactive HPC workloads are stateful.
- You can't capture the state of an HPC system.
- Cloud-native tools declare the full computational environment.
- Declarative beats procedural: more portable, less fragile.
- Stateless systems make software, OS, libraries and data portable.
- Interactive conda or pip installs aren't reproducible. Declare and lock them.
- Data left on a POSIX file system doesn't capture its history or provenance. Version it, with GitOps and DataOps.
- Work done in an LLM chat isn't reproducible. Keep the prompts and decisions in the project.
- The project is the pet, and the running model and the coding agent that runs it are cattle. The test is whether another person or another model can continue from the saved files.

## From the ideas to the study

- The talk lists six building blocks. Each bullet says where this site shows one, or that it doesn't.
- Software, an environment file and its lock: the stages in [the pipeline file](project.md#the-declarations) list `pyproject.toml` and `uv.lock` as dependencies.
  - Those two files are not published, so the site does not show the study's locked environment.
  - The training and validation stages also list a second pair, `envs/train/pyproject.toml` and `envs/train/uv.lock`. That pair is not published either.
  - The site's own build installs from `requirements.txt`, which pins every package version. [How this site is built](build.md).
- Workflows, declared steps: the 18 stages in [the pipeline file](project.md#the-declarations), and their [lineage](project.md#lineage).
- Data, pointers in Git to stored data: the hashes and sizes in [the lock file](project.md#the-declarations). The data they point to is not published.
- Models, registered versions: [the registry listing](project.md#what-the-registry-versions) and the table of [12 registered versions](results.md#registered-versions).
- LLMs, the row the talk calls still open: the base model's pinned revision is in `params.yaml`, under [the settings on record](project.md#the-settings-on-record).
  - [Same weights, not always the same outputs](serving.md) shows that bit-identical weights did not give identical raw predictions.
  - The site does not show the study's instructions, tool definitions or tests.
- Documentation, all of it rebuilt as the result: [the results page](results.md) rebuilds its tables from the study's data files, and [How this site is built](build.md) shows the build and the check.
- This site does not teach the tools. The fundamentals site, [Reproducibility in AI](https://ohpcsim.github.io/reproducibility-in-ai/), has hands-on material for them, including versioned data and pipelines with DVC and a model registry. [Tools and documentation](tools.md) lists what this study used.

## Further reading

- [The History of Pets vs Cattle and How to Use the Analogy Properly](https://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/), Randy Bias, 2016. Where the analogy came from. He credits Bill Baker's talk on scaling SQL Server.
- [CERN Data Centre Evolution](https://www.slideshare.net/gmccance/cern-data-centre-evolution), Gavin McCance, SDCD12 in Bern, November 2012. Slides on moving CERN's data centre to a pets and cattle service model.
- [Literate Programming](https://doi.org/10.1093/comjnl/27.2.97), D. E. Knuth, The Computer Journal 27(2):97-111, 1984. The paper that introduced literate programming.

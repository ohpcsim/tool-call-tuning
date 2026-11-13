---
title: The sealed test
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

## What a sealed test is

- A sealed test is a set of requests kept apart from the people tuning the model until the final check.
- Its purpose is to measure the frozen system on requests that played no part in building it.
- Choices made after seeing open-validation results can fit those results. A test kept unseen until the system is frozen limits that risk.

## Status

- The study's own wording:

> The original sealed test was lost before it was ever used. Its storage directory was removed in an internal storage cleanup on October 25, 2026, and one authorized attempt to recover the file from archived records failed. The held-out evaluation on that test was not run. A replacement sealed test, written by an independent author after the system is frozen, has been proposed under an amendment that is not yet signed. Until a held-out evaluation is run and reported, every result on this site is open validation only.

- No sealed-test evaluation has run, and every result on this site is open validation.
- H3 is the study's hypothesis for the to-do task. On the sealed test, the tuned system must not score worse than the earlier reference system by more than two percentage points, judged by the lower end of a 95% interval on the paired difference, and it must make zero wrong destructive actions. It is a test of not being worse, not of being better: the study makes no claim that the tuned system beats the reference. H3 has not been tested.
- Source for H3: the study's protocol, version 1, and proposed Amendment A1, "What does not change".

## What this does not mean

- It does not mean the test was contaminated or exposed.
- It does not mean a recovered file failed its hash check. No file was recovered.
- It does not mean recovery is impossible by every route. One bounded attempt failed.

## What it teaches

- A test set is something to keep, like data or code.
- It needs a backup that the people tuning the model cannot read, and a recovery that has been tried.

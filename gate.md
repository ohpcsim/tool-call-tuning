---
title: The rule it failed, and one added check
---

:::{important}
Working benchmark: open validation only; not held-out; no confirmatory claim
:::

## The rule

- The study's rule allows zero wrong destructive actions.
- All three tuned to-do models broke it on open validation.
- The 1-, 2- and 3-epoch models made 4, 1 and 2 wrong destructive actions out of 613 requests.
- Nothing was promoted.

## One added check

- The study then added one check.
- Before a call executes, the check validates the call's arguments and dates, without using the answer key.
- The study replayed the saved model outputs through this check on a CPU.
- No model ran again.

| Model | Correct, of 613 | Wrong destructive |
| --- | --- | --- |
| Tuned, 2 epochs (named in the proposed amendment) | 606, then 604 | 1, then 0 |
| Tuned, 1 epoch | 596, then 594 | 4, then 3 |
| Tuned, 3 epochs (diagnostic only) | 609, then 607 | 2, then 0 |
| Earlier reference model (optimistic) | 612, then 610 | 0, then 0 |
| Base model, before tuning | 156, then 156 | 43, then 32 |

- Source: the study's protocol amendment, section 3.
- The protocol is the study's written plan. The amendment is a proposed change to it, not yet signed. Neither is published.
- These numbers are not in the data files on this site, so they are typed in, not rebuilt.

## What these numbers are, and are not

- Open validation, developed adaptively. The check was designed after seeing these failures.
- A CPU replay of saved outputs. There was no new model inference.
- The "before" counts already include the system's existing guards.
- The check cost two formerly correct calls each for the three tuned models and the reference model.
- The reference model's score is optimistic, because its training overlaps this validation set.
- A fresh inference run could still produce a wrong destructive action that the check does not catch. Nobody has measured how likely that is.
- The 3-epoch row is a diagnostic only in this replay. In the original selection the 3-epoch model was a candidate, like the other two. The proposed amendment names the 2-epoch model as the single model to carry the added check. The 3-epoch model cannot replace it after this feedback.
- No amended selection, freeze or sign-off has happened. The amendment's exact text is unsigned.

## The reviewed implementation

- An implementation of the check replays the saved outputs on the same 613 validation requests.
- It replays three systems: the 2-epoch model, the reference model and the base model, and it gives the same counts for each.
- Source: the implementation's parity record at its reviewed final head. Its counts and per-item digests for these three systems equal the October 13 replay record. The independent reviewer checked that in each review round.
- The 1-epoch and 3-epoch rows come from the October 13 replay and were not re-run by this implementation.
- AI models wrote and reviewed this implementation.
- The final head is the last version of the code that was reviewed.
- An independent reviewer from another vendor's model family reviewed the GPT-family author's implementation in six rounds. Rounds 1, 2, 4 and 5 returned FAIL. The final head passed independent review.
- The implementation is not merged, and the amendment is not signed or tagged.
- This is a CPU replay of saved outputs on open validation, with no new inference.

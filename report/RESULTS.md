---
title: "Proof Pursuit — results achieved"
subtitle: "Team: T. Tumini (Researcher), gabundos (Referee), M. Renzi (Creative), gio3r3gio · 26 September 2026"
lang: en
---

## In one line

Out of 24 cells, **10 closed** with a complete proof, a positive verdict from two independent automatic judges and human approval (18 points), **1 candidate** on the value, **13 honest partials**, all published. The multi-agent system worked end-to-end and closed 5 cells on its own; the other 5 were closed with proofs written by hand by the team and judged by the same Referee.

## What we closed

| Cell | How | Points |
|---|---|---|
| Problem 1, part 1 | proof written by the team (random half-turn), judged by the Referee, approved | 1 |
| Problem 1, part 2 | proof written by the team (induction with projection), judged, approved | 2 |
| Problem 2, part 1 | autonomous loop: Researcher with shell + Referee, human review | 1 |
| Problem 2, part 2 | autonomous loop, three Referee runs, reduction re-read by hand | 2 |
| Problem 2, part 3 | autonomous loop, one iteration: value, labelling and lower bound | 3 |
| Problem 3, part 1 | autonomous loop, one iteration | 1 |
| Problem 3, part 2 | autonomous loop, **two iterations**: motivated REJECT, then the proof completed | 2 |
| Problem 4, part 1 | proof written by the team (parity), judged, approved | 1 |
| Problem 4, part 2 | proof written by the team (prime cliques), judged, approved | 2 |
| Problem 4, part 3 | autonomous loop: reduction to a finite set + certified search with two implementations | 3 |

Autonomously (Researcher → Referee, no human intervention on the content): problem 2 parts 1, 2, 3; problem 3 parts 1, 2; problem 4 part 3. With a human proof and automatic judging: problem 1 parts 1, 2; problem 4 parts 1, 2.

## What remained partial, and what it contains

| Cell | Content of the partial |
|---|---|
| Problem 1, parts 3–5 | formalisation, reduction to deficits, the part-2 lemma as the building block, literature |
| Problem 1, part 6 | dimension-transfer lemmas (proved), no new infinite family; open since 1959 |
| Problem 2, part 4 | candidate value by the star construction, optimality proved within the family; lower bound missing |
| Problem 2, parts 5–6 | exact structural identity and reduction to decycling sets; known bounds not improved |
| Problem 3, part 3 | general bound proved for rank ≥ 5, exact table up to rank 11, value of the family conjectured with explicit extremals |
| Problem 3, parts 4–5 | exact table, conjectured formulas, residual values, extremals; uniform proof missing |
| Problem 3, part 6 | table as the basis for the conjecture; open |
| Problem 4, part 4 | certificate written and mathematics judged PASS up to size 13; re-runs not reproduced because of missing script arguments |
| Problem 4, part 5 | hand proof of the two isolated sizes; strengthened certificate missing |
| Problem 4, part 6 | recursion and an unconditional but weaker bound; the July 2026 arXiv paper improving the quoted bound is flagged |

## Why partial: the time

1. **Building the system during the contest.** Of the 7 hours, about 3 went into building and integrating the harness: Researcher, bridge, two-judge Referee, Creative, loop, arXiv search, submission packages. The first real runs started mid-afternoon.
2. **Latency per attempt.** A Researcher attempt with a shell takes 10–25 minutes, the Referee 4: one iteration is 15–30 minutes, two iterations an hour. The machine waits for the model; more CPU does not help, and parallelism was already at eleven cells.
3. **Four contract defects found by real runs** (a variadic flag swallowing the prompt; a judge's reservation voiding a PASS; missing trusted re-runs and official rules; claim provenance not admitted by the validator). Each fix cost one Referee run and 10–15 minutes; without real runs they would not have surfaced.
4. **An accidental session restart** 35 minutes before the end killed seven running loops, four of which already had an attempt written; they were recovered as partials, two second iterations were lost.
5. **Intrinsic difficulty.** The part-6 cells are open problems; the part-5 cells need uniform arguments or strengthened certificates worth hours of work. The plan declared 14–18 realistic points from the start: we are at 18 plus the candidate.

## What worked and should be kept

- Two-judge Referee with a deterministic merge: no false positives; every REJECT pointed to the exact missing step.
- The error loop: on problem 3 part 2 the Researcher read the rejection, fetched the source and completed the proof on the second round.
- Hand-written proofs judged by the Referee: four cells closed in twenty minutes.
- Explicit construction plus exact verification: for problem 2 the method of part 2 extended to part 3 in one iteration.
- Traceability: every submission reports the agents' decisions, the tokens, the arXiv sources and the re-run code.

## What to change next time

Harness ready before the contest; a portfolio of parallel Researchers per cell with different approach families; the Referee on human attempts from the start; scripts with explicit arguments and declared time limits; no session restarts with loops running.

Repository and write-ups: https://github.com/triborg0259/proof-pursuit · https://triborg0259.github.io/proof-pursuit/

# Catalogo di repository open-source per ricerca matematica assistita da AI e loop di ricerca autonomi

Observation date for every star count / last-commit date below: **2026-09-28**, via the GitHub REST API (`gh api repos/<owner>/<name>` and `/commits?per_page=1`), unless stated otherwise. "Last commit" = committer date of the newest commit on the default branch. License = SPDX id reported by GitHub (`NOASSERTION` = custom license file; `none` = no license detected). Repositories that returned 404 are marked **non verificato**. Nothing below was run locally; architecture notes come from each README as fetched on 2026-09-28.

## Key question 0 — The catalog itself: what each repository is, how it is built, what it needs, how mature it is

### Takeaway
The field splits cleanly into (1) generic "propose → evaluate → keep if better" harnesses whose verifier is a user-written numeric scorer (autoresearch, OpenEvolve, ShinkaEvolve, AlphaResearch) or an LLM reviewer (AI-Scientist, AI-Researcher, CycleResearcher), and (2) formal-math tooling where the verifier is the Lean kernel (LeanDojo/LeanCopilot, the provers, kimina-lean-server, LeanOpenProblems + Comparator, unsorry). Only the second family gives proofs; the first gives floats. Most of the 2024–2025 "AI scientist" repos are effectively frozen since late 2025; the actively maintained cores in Sept 2026 are ShinkaEvolve, OpenEvolve (last push July 2026), mathlib4, LeanCopilot, LeanDojo-v2, PutnamBench, MathArena, formal-conjectures, equational_theories, LeanOpenProblems.

### Cited Findings

#### Group 1 — Research-loop harnesses

**karpathy/autoresearch** — https://github.com/karpathy/autoresearch
- Owner: Andrej Karpathy. Stars 96,887; forks 13,527; open issues 195; created 2026-03-06; last commit 2026-03-26 ("Merge pull request #342"); not archived — [GitHub API, observed 2026-09-28](https://github.com/karpathy/autoresearch)
- License: GitHub reports no license (`none`) and the root file listing (`.gitignore .python-version README.md analysis.ipynb prepare.py program.md progress.png pyproject.toml train.py uv.lock`) contains **no LICENSE file**; the README as summarised by our fetch says "MIT" — treat the license as **unclear / conflicting** — [repo contents via API](https://github.com/karpathy/autoresearch); [README](https://github.com/karpathy/autoresearch)
- One sentence: "give an AI agent a small but real LLM training setup and let it experiment autonomously overnight. It modifies the code, trains for 5 minutes, checks if the result improved, keeps or discards, and repeats." — [README](https://github.com/karpathy/autoresearch)
- Architecture: three files — `prepare.py` (fixed, data prep + utilities, never edited by the agent), `train.py` (the single file the agent edits: GPT model, Muon+AdamW optimizer, training loop), `program.md` (human-written instructions for the agent). Metric `val_bpb` (lower is better). No separate verifier: the agent itself runs the training and reads the number. — [README](https://github.com/karpathy/autoresearch)
- Storage of attempts: `program.md` prescribes a run branch `autoresearch/<tag>`, one git commit per experiment, and an untracked `results.tsv` with header `commit	val_bpb	memory_gb	status	description`, status ∈ {`keep`, `discard`, `crash`}, `val_bpb = 0.000000` for crashes; results read with `grep "^val_bpb:\|^peak_vram_mb:" run.log`; "do not commit the results.tsv file" — [program.md, lines 64–103](https://github.com/karpathy/autoresearch/blob/master/program.md)
- Needs: single NVIDIA GPU (tested on H100), ~5 min per experiment, ~12 experiments/hour; "Claude/Codex or whatever you want"; CPU/MPS not supported upstream — [README](https://github.com/karpathy/autoresearch)
- Notable forks (stars, last push, all observed 2026-09-28 via `/forks?sort=stargazers`): `miolini/autoresearch-macos` 2,396 (2026-03-17), `jsegov/autoresearch-win-rtx` 730 (2026-03-14), `mutable-state-inc/autoresearch-at-home` 495, `eli-labz/ResearchSwarm` 266 (2026-06-30), `mishig25/hf-autoresearch` 179, `kousun12/darwin-derby` 53 ("research on anything"). Non-fork "descendants" found by name search: `aiming-lab/AutoResearchClaw` 14,538 stars MIT (2026-08-19), `davebcn87/pi-autoresearch` 8,130 MIT TypeScript (2026-09-10), `uditgoenka/autoresearch` 6,469 MIT Shell "Claude Autoresearch Skill" (2026-08-12), `EvoMap/AutoResearch` 2,789 Apache-2.0 (2026-09-16), `leo-lilinxiao/codex-autoresearch` 2,679 MIT, `trevin-creator/autoresearch-mlx` 1,848 MIT (2026-07-02) — [GitHub search API](https://github.com/search?q=autoresearch)
- Pitfall (issue #599, open): "Agent can lower val_bpb without improving the model" — the agent owns `train.py`, so it can skip `optimizer.step()` and still finish the budget, or wrap/replace the `evaluate_bpb` call; the "do not change" rule on `evaluate_bpb` "is prose only … nothing enforces it" — [issue #599](https://github.com/karpathy/autoresearch/issues/599)
- Maturity: upstream frozen since 2026-03-26 despite 195 open issues (many are "add my fork to notable forks" requests: #450, #75, #463, #596, #642, #582) — [issues search, observed 2026-09-28](https://github.com/karpathy/autoresearch/issues)

**aiming-lab/AutoResearchClaw** — https://github.com/aiming-lab/AutoResearchClaw
- Stars 14,538; MIT; Python; last push 2026-08-19 — [GitHub API](https://github.com/aiming-lab/AutoResearchClaw)
- One sentence: idea-to-paper pipeline, "23 stages across 8 phases" (scoping, literature, synthesis, design, sandbox execution with self-healing, analysis with PROCEED/REFINE/PIVOT, writing with peer review, finalization) — [README](https://github.com/aiming-lab/AutoResearchClaw)
- Verifier: citation verification (arXiv id, CrossRef DOI, title match, relevance), a "VerifiedRegistry" that sanitises unverified numbers before paper generation, LLM peer-review stage; run artifacts in timestamped folders with SHA256 checksums, JSON metrics — [README](https://github.com/aiming-lab/AutoResearchClaw)
- Needs: OpenAI-compatible key, optional Semantic Scholar/OpenAlex keys, Python 3.11+, GPU auto-detected with CPU fallback, Docker optional, LaTeX; paper arXiv:2605.20025 — [README](https://github.com/aiming-lab/AutoResearchClaw)

**algorithmicsuperintelligence/openevolve** (formerly `codelion/openevolve`; the old URL redirects) — https://github.com/algorithmicsuperintelligence/openevolve
- Stars 7,445; forks 1,166; open issues 122; Apache-2.0; Python; created 2025-05-15; last commit 2026-07-18 ("Boolean metrics: fix formatting and exclude from fitness") — [GitHub API](https://github.com/algorithmicsuperintelligence/openevolve)
- One sentence: "Open-source implementation of AlphaEvolve" — evolutionary coding agent — [GitHub API description](https://github.com/algorithmicsuperintelligence/openevolve)
- Architecture: LLM ensemble (weighted models, fallbacks) → program database with MAP-Elites quality-diversity grid and island populations with migration → user-defined evaluator taking a program path and returning `EvaluationResult(metrics=…, artifacts=…)`; artifacts (stderr, profiling, LLM feedback) are a side-channel fed back into prompts; cascade evaluation stages filter bad programs early — [README](https://github.com/algorithmicsuperintelligence/openevolve)
- Storage: programs and history in `openevolve_output/`, checkpoints at configurable intervals, deterministic seed (default 42), YAML config — [README](https://github.com/algorithmicsuperintelligence/openevolve)
- Needs: any OpenAI-compatible endpoint (OpenAI, Gemini, Ollama/vLLM/LM Studio local, OptiLLM proxy, "Claude Code CLI (no API key needed)"); Python 3.10+; no GPU; README estimates "~$0.01–0.60 per iteration" — [README](https://github.com/algorithmicsuperintelligence/openevolve)
- Results claimed: circle packing n=26 matching AlphaEvolve's published value; 2.8× Apple-M1 attention kernel speedup; symbolic regression; adaptive sorting in Rust — [README](https://github.com/algorithmicsuperintelligence/openevolve)
- Pitfalls from issues: #117 "Reproducing circle packing without providing `TARGET_VALUE = 2.635` from AlphaEvolve paper" (the target was leaked into the prompt), #106 "Not respecting the EVOLVE-BLOCK-START / END markers", #149 multi-file evolution missing — [issues](https://github.com/algorithmicsuperintelligence/openevolve/issues)
- Related: `ypwang61/ThetaEvolve` (180 stars, Apache-2.0, 2026-02-27, RL on top of OpenEvolve), `shyamsaktawat/OpenAlpha_Evolve` (1,053 stars, MIT, last push 2025-05-31 — abandoned), `Optima-CityU/LLM4AD` (778 stars, BSD-2) and `LLM4AD_Next` (527 stars, BSD-3, push 2026-09-27) — [GitHub search API](https://github.com/search?q=alphaevolve)

**SakanaAI/ShinkaEvolve** — https://github.com/SakanaAI/ShinkaEvolve
- Stars 1,416; Apache-2.0; Python; last push 2026-09-24; last commit 2026-08-21 ("Merge pull request #188 … fix/anthropic-content-b…") — [GitHub API](https://github.com/SakanaAI/ShinkaEvolve)
- One sentence: "Towards Open-Ended and Sample-Efficient Program Evolution" — [GitHub API description](https://github.com/SakanaAI/ShinkaEvolve)
- Architecture: LLM ensemble as mutation operators with bandit (UCB default, cost-aware) model selection; `evaluate.py` per task producing `combined_score`; **SQLite** program archive with islands, fitness/crowding replacement (elite ratio default 30%); novelty rejection by code embeddings (`text-embedding-3-small` or local, similarity threshold 0.99); `shinka_visualize` WebUI with genealogy trees; W&B optional; `pricing_snapshot.json` written per run — [README](https://github.com/SakanaAI/ShinkaEvolve)
- Needs: Python ≥3.10, Hydra; OpenAI/Google/Anthropic keys per configured model or local models; runs locally, on SLURM (Docker/Conda) or async distributed; no GPU needed for the loop — [README](https://github.com/SakanaAI/ShinkaEvolve)
- Results claimed: circle packing, ALE/2048, AtCoder-style tasks, MoE loss design; "Team Unagi used ShinkaEvolve to win ICFP 2025" — [README](https://github.com/SakanaAI/ShinkaEvolve)
- Pitfalls: misplaced `EVOLVE-BLOCK-START/END` markers break parsing; `max_patch_resamples` (default 3) too low stalls evolution; embedding-model mismatch; open issues #190 (patch re-indentation), #193 (fence extraction) — [README](https://github.com/SakanaAI/ShinkaEvolve); [issues](https://github.com/SakanaAI/ShinkaEvolve/issues)

**google-deepmind/funsearch** — https://github.com/google-deepmind/funsearch
- Stars 1,126; Apache-2.0 (code) / CC-BY-4.0 (other); Jupyter; last commit 2024-02-05; 14 commits total — [GitHub API](https://github.com/google-deepmind/funsearch)
- What it is: notebooks with the discovered programs (cap sets, admissible sets, bin packing, cyclic-graph independent sets) plus "a single-threaded implementation of the FunSearch pipeline"; it explicitly lacks "language models for generating new programs, the sandbox for executing untrusted code, nor the infrastructure for running FunSearch on our distributed system" — **not runnable end to end** — [README](https://github.com/google-deepmind/funsearch)

**google-deepmind/alphaevolve_results** — https://github.com/google-deepmind/alphaevolve_results
- Stars 301; Apache-2.0; Jupyter; last commit 2026-01-05 ("Fixed metadata typo") — [GitHub API](https://github.com/google-deepmind/alphaevolve_results)
- Sibling: **google-deepmind/alphaevolve_repository_of_problems** — 236 stars, Apache-2.0, Jupyter, last push 2026-07-11 — [GitHub API](https://github.com/google-deepmind/alphaevolve_repository_of_problems). Both are result/problem notebooks, not a runnable system (no system code found in either listing).

**answers111/alpha-research** — https://github.com/answers111/alpha-research
- Stars 61; GitHub license `none` (README says MIT — conflicting); Python; last commit 2025-11-12 ("Update README.md") — [GitHub API](https://github.com/answers111/alpha-research); [README](https://github.com/answers111/alpha-research)
- Architecture: proposer → execution-based verifier (benchmark score) → "peer review" via a trained reward model (AlphaResearch-RM-7B on Hugging Face); built on OpenEvolve; 8-problem "AlphaResearchComp" (circle packing n=26 reported 0.32% above human best) — [README](https://github.com/answers111/alpha-research)
- Needs GPU for the reward model; effectively unmaintained since Nov 2025.

**SakanaAI/AI-Scientist** — https://github.com/SakanaAI/AI-Scientist — and **SakanaAI/AI-Scientist-v2** — https://github.com/SakanaAI/AI-Scientist-v2
- v1: 14,627 stars; custom license (`NOASSERTION`); last commit 2025-12-19. v2: 7,227 stars; custom license; last commit 2025-12-19 — [GitHub API](https://github.com/SakanaAI/AI-Scientist-v2)
- v2 architecture: ideation (LLM + Semantic Scholar) → experimentation by best-first **agentic tree search** driven by an experiment manager → writing + LLM peer-review simulation; optional VLM reviewer; logs in timestamped `experiments/` folders with `unified_tree_viz.html` and final PDF — [README v2](https://github.com/SakanaAI/AI-Scientist-v2)
- Needs: Linux + NVIDIA GPU, LaTeX/poppler/chktex, Python 3.11+, OpenAI or Claude-via-Bedrock or Gemini key; README estimates $15–20 per run (Claude 3.5 Sonnet) and warns the system executes LLM-written code with "potential use of dangerous packages, uncontrolled web access, and spawning unintended processes" — run in Docker — [README v2](https://github.com/SakanaAI/AI-Scientist-v2)
- Result: "first workshop paper written entirely by AI and accepted through peer review" (ICLR 2025 workshop) — [README v2](https://github.com/SakanaAI/AI-Scientist-v2)
- Issues (v1): #253 "Request for specific Python and dependency versions to avoid installation conflicts", #158 "dependencies", #43 Mac Silicon, #173 `text8` download 403 — [issues](https://github.com/SakanaAI/AI-Scientist/issues)

**zhu-minjun/Researcher** (CycleResearcher / CycleReviewer / DeepReviewer) — https://github.com/zhu-minjun/Researcher
- Stars 404; custom "CycleResearcher-License" (non-commercial restrictions); Jupyter; last commit 2026-03-05 — [GitHub API](https://github.com/zhu-minjun/Researcher); [README](https://github.com/zhu-minjun/Researcher)
- Architecture: open-weight generator models (12B/72B/123B) and reviewer models (8B/70B/123B; DeepReviewer 7B/14B with "self-verification" and OpenScholar retrieval) — the **reviewer is the reward**; requires GPU/vLLM to host the weights — [README](https://github.com/zhu-minjun/Researcher)

**HKUDS/AI-Researcher** — https://github.com/HKUDS/AI-Researcher
- Stars 5,766; no license detected; Python; last commit 2025-10-16 ("Add files via upload"); NeurIPS 2025 — [GitHub API](https://github.com/HKUDS/AI-Researcher)
- Agents: literature review, idea generation, implementation, validation, paper writing; runs inside Docker image `tjbtech1/airesearcher:v1`; LLMs via LiteLLM (Claude/OpenAI/DeepSeek); GPU configurable — [README](https://github.com/HKUDS/AI-Researcher)
- Maturity: the description points to a commercial "production-ready version" (Novix); open-source repo not updated since Oct 2025 — [GitHub API description](https://github.com/HKUDS/AI-Researcher)

**SamuelSchmidgall/AgentLaboratory** — https://github.com/SamuelSchmidgall/AgentLaboratory
- Stars 5,869; MIT; Python; last commit 2025-08-20 — [GitHub API](https://github.com/SamuelSchmidgall/AgentLaboratory)
- Three phases (literature review, experimentation via `mlesolver.py`, report writing via `papersolver.py`), "copilot mode" for human-in-the-loop; checkpoints in `state_saves`; needs OpenAI (o1/gpt-4o/o3-mini) or DeepSeek key, Python 3.12, pdflatex optional; GPU optional; no cost figures in README — [README](https://github.com/SamuelSchmidgall/AgentLaboratory)

**Lean-native loop repos found by search (small, but with a real verifier):**
- **agenticsnz/unsorry** — https://github.com/agenticsnz/unsorry — 42 stars, Apache-2.0, Lean, last push 2026-09-03. "The repo is the work queue; the kernel is the judge": workers (Claude/Codex/Gemini or a deterministic sympy solver) pull a `sorry` goal, prove it, verify locally against the Lean kernel, open a PR that CI ("Gate A") re-verifies and auto-merges; claims "8,983 commits, 2,349 verified proofs, eight human contributors" in under two weeks from 2026-06-10 (self-reported) — [README](https://github.com/agenticsnz/unsorry)
- **cameronfreer/lean4-skills** — https://github.com/cameronfreer/lean4-skills — 451 stars, MIT, last push 2026-09-27. Host-agnostic skill pack (Claude Code plugin `/lean4:*`, Codex plugin, others) giving "a structured prove/review/golf loop, mathlib search, axiom checking, and safety guardrails" — [README](https://github.com/cameronfreer/lean4-skills)
- **Kripner/nanoproof** — 93 stars, MIT, Python, last push 2026-05-13, "Minimal open-source implementation of AlphaProof and HyperTree Proof Search" — [GitHub API](https://github.com/Kripner/nanoproof)
- **liuchengwucn/discover-and-prove** — 7 stars, custom license, Lean, push 2026-06-29, "(ACL 2026 Main) … Agentic Framework for Hard Mode Automated Theorem Proving in Lean 4" — [GitHub API](https://github.com/liuchengwucn/discover-and-prove)

#### Group 2 — Formal-math tooling and provers

**leanprover-community/mathlib4** — https://github.com/leanprover-community/mathlib4 — 4,196 stars; Apache-2.0; Lean; last push 2026-09-27 — [GitHub API](https://github.com/leanprover-community/mathlib4). **leanprover/lean4** — 9,324 stars; Apache-2.0; push 2026-09-27 — [GitHub API](https://github.com/leanprover/lean4).

**lean-dojo/LeanDojo** — https://github.com/lean-dojo/LeanDojo — 839 stars; MIT; Python; last commit 2026-01-18 "Update README to indicate LeanDojo is deprecated". README: "This original LeanDojo library is deprecated. Please use LeanDojo-v2 for all new projects … We will soon be moving LeanDojo-v2 here." Supports Lean 4 ≥ v4.3.0-rc2, Python 3.9–3.12, Linux/WSL/macOS, needs Git ≥2.25, wget, elan, GitHub token; no GPU for tracing — [README](https://github.com/lean-dojo/LeanDojo). Open issues: #252 "Lean4Repl.lean fails on newer Lean versions (missing Std.TreeSet.union)", #211 "Issues with Running Tactics on Repos Using Lean >= v4.12.0", #228 missing `*.ast.json` — [issues](https://github.com/lean-dojo/LeanDojo/issues)
- **lean-dojo/LeanDojo-v2** — https://github.com/lean-dojo/LeanDojo-v2 — 139 stars; Apache-2.0; Python; last push 2026-08-10; "end-to-end framework for training, evaluating, and deploying AI-assisted theorem provers" — [GitHub API](https://github.com/lean-dojo/LeanDojo-v2)
- **lean-dojo/ReProver** — 338 stars; MIT; last push 2025-01-30 (frozen). **lean-dojo/LeanAgent** — 87 stars; no license; push 2025-06-13 — [GitHub API](https://github.com/lean-dojo/LeanAgent)

**lean-dojo/LeanCopilot** — https://github.com/lean-dojo/LeanCopilot — 1,325 stars; MIT; C++; last commit 2026-09-18 ("Fix #200"). Tactics `suggest_tactics`, `search_proof` (LLM tactics + Aesop), `select_premises`; local inference via CTranslate2, GPU optional; Linux/macOS, Windows only via WSL; needs Git LFS, Lean ≥ v4.3.0-rc2; external models via `ExternalGenerator`/`ExternalEncoder` matching `external_model_api.yaml`. Known caveats: `libstdc++` linking with `lean_exe`, `search_proof` occasionally yields termination errors — [README](https://github.com/lean-dojo/LeanCopilot)

**cmu-l3/llmlean** — https://github.com/cmu-l3/llmlean — 213 stars; MIT; Lean; last push 2025-10-10; "LLMs + Lean, on your laptop or in the cloud" — [GitHub API](https://github.com/cmu-l3/llmlean)

**deepseek-ai/DeepSeek-Prover-V2** — https://github.com/deepseek-ai/DeepSeek-Prover-V2 — 1,303 stars; custom license (code MIT + separate Model License); last commit 2025-07-18 ("update putnam results"). Models 7B (32K context) and 671B on Hugging Face; reported miniF2F-test 88.9%, PutnamBench 49/658, new ProverBench (325 problems); cold-start via DeepSeek-V3 subgoal decomposition + 7B search per subgoal — [README](https://github.com/deepseek-ai/DeepSeek-Prover-V2). V1.5: 586 stars, MIT, push 2024-08-16 — [GitHub API](https://github.com/deepseek-ai/DeepSeek-Prover-V1.5)

**MoonshotAI/Kimina-Prover-Preview** — https://github.com/MoonshotAI/Kimina-Prover-Preview — 376 stars; no license; last commit 2025-07-10 ("add new miniF2F problems solved by Kimina-Prover-72B"). Technical report repo; distilled 1.5B/7B weights on Hugging Face; reports miniF2F 80.7% pass@8192 (arXiv 2504.11354) — [README](https://github.com/MoonshotAI/Kimina-Prover-Preview); [arXiv](https://arxiv.org/html/2504.11354v1). A repo named `MoonshotAI/Kimina-Prover` (non-preview) does **not exist** (404) — **non verificato**.

**project-numina/kimina-lean-server** — https://github.com/project-numina/kimina-lean-server — 211 stars; MIT; Python; last push 2026-01-11. FastAPI wrapper around the Lean 4 REPL with a pool of REPL workers (default CPU−1), Docker, default Lean v4.26.0, PyPI client `kimina-client` (sync/async), returns pass / sorry / error per request; ~8 GB RAM per REPL — [README](https://github.com/project-numina/kimina-lean-server)

**Goedel-LM/Goedel-Prover-V2** — https://github.com/Goedel-LM/Goedel-Prover-V2 — 191 stars; no license detected by GitHub (README shows Apache-2.0 badge — conflicting); last commit 2025-08-27. 8B and 32B weights; miniF2F pass@32 88.0% (32B) / 90.4% with self-correction / 84.6% (8B); PutnamBench 86 at pass@192; Linux, Python 3.10, Lean4+Mathlib4 via conda env; `bash scripts/pipeline.sh` — [README](https://github.com/Goedel-LM/Goedel-Prover-V2). V1: 239 stars, MIT, push 2025-04-04 — [GitHub API](https://github.com/Goedel-LM/Goedel-Prover)

**ByteDance-Seed/Seed-Prover** — https://github.com/ByteDance-Seed/Seed-Prover — 443 stars; Apache-2.0; Lean; last commit 2026-02-13 ("erdos_1051"). Contains Lean proofs of IMO 2025 P1/P3/P4/P5, natural-language proofs, and source for Seed-Prover 1.5 / 1.0 / Delta-Prover; **no model weights**; claims 88% of PutnamBench and 11/12 Putnam 2025; Lean v4.14.0 for the proofs — [README](https://github.com/ByteDance-Seed/Seed-Prover)

**DeepMind 2026 formal-proof releases:**
- **google-deepmind/alphaproof-nexus-results** — https://github.com/google-deepmind/alphaproof-nexus-results — 299 stars; Apache-2.0 (code) / CC-BY-4.0; Lean; last commit 2026-06-05 ("Add results from Stacks Project"). Lean proofs + prose for Erdős problems, OEIS problems, Stacks Project items and human-AI collaborations (additive combinatorics, algebraic geometry, graph theory, optimization, quantum optics); verify with `lake exe cache get && lake build`; **system code not released** — [README](https://github.com/google-deepmind/alphaproof-nexus-results). A repo `google-deepmind/alphaproof` does not exist (404).
- **google-deepmind/formal-conjectures** — https://github.com/google-deepmind/formal-conjectures — 1,295 stars; Apache-2.0; Lean; last push 2026-09-27; "A collection of formalised statements of conjectures in Lean, using mathlib"; arXiv 2605.13171; Zulip channel; goal "a great benchmark for automated theorem provers" — [README](https://github.com/google-deepmind/formal-conjectures). Community pipelines already merge AI-found proofs into it (e.g. PR #6611 "Erdős 522: mark solved and link a Lean 4 proof") — [PR #6611](https://github.com/google-deepmind/formal-conjectures/pull/6611)

**teorth/equational_theories** — https://github.com/teorth/equational_theories — 559 stars; Apache-2.0; Lean; last commit 2026-09-12. 4,694 equations, 22,028,942 implications; ATPs (Prover9/Mace4, Vampire, eprover, twee, Z3) generate proofs/counterexamples, all assertions Lean-verified; blueprint + dashboard; launched 2024-09-25 — [README](https://github.com/teorth/equational_theories)

**PatrickMassot/leanblueprint** — https://github.com/PatrickMassot/leanblueprint — 377 stars; Apache-2.0; Python (plasTeX plugin); last commit 2025-12-23 ("Bump version number") — [GitHub API](https://github.com/PatrickMassot/leanblueprint). **leanprover-community/lean4web** — 154 stars; Apache-2.0; push 2026-08-30 — [GitHub API](https://github.com/leanprover-community/lean4web)

#### Group 3 — Benchmarks and graders

- **openai/miniF2F** — https://github.com/openai/miniF2F — 436 stars; no license; **archived**; last commit 2023-08-16 — [GitHub API](https://github.com/openai/miniF2F). **facebookresearch/miniF2F** — 106 stars; MIT; "updated version of miniF2F with lots of fixes and informal statements / solutions"; last push 2025-01-04 — [GitHub API](https://github.com/facebookresearch/miniF2F). **yangky11/miniF2F-lean4** — 75 stars; MIT; last commit 2026-03-25 ("fix/correct-erroneous-formaliza…") — [GitHub API](https://github.com/yangky11/miniF2F-lean4)
- **trishullab/PutnamBench** — https://github.com/trishullab/PutnamBench — 265 stars; GitHub license `none` (README: Lean/Isabelle Apache-2.0, Coq MIT); Lean; last commit 2026-09-24 ("forall-astrio-leaderboard"). 1,724 formalizations: Lean 4 672, Isabelle 640, Coq 412; policy "Do not include proofs as confirmation in any public setting", leaderboard by private email — [README](https://github.com/trishullab/PutnamBench)
- **epoch-research/LeanOpenProblems** — https://github.com/epoch-research/LeanOpenProblems — 16 stars; custom license; Lean; last push 2026-09-27. Built on the Inspect framework; "A submission counts only if it passes Comparator, the Lean FRO's adversarially robust proof checker. The agent works in one sandboxed container, and comparator runs in a separate one"; problems mostly from formal-conjectures; basis of **FrontierMath Erdős** (arXiv 2609.25050) and **OEIS Open** (arXiv 2608.11941) — [README](https://github.com/epoch-research/LeanOpenProblems). FrontierMath Erdős: 68 open Erdős problems, $300 / 72 h per attempt, network-isolated Docker with Lean v4.27.0, Mathlib, SageMath, Python; GPT-6 Astra solved 5/68 across attempts, all other models 0 — [Epoch AI announcement](https://epoch.ai/latest/announcing-frontiermath-erdos); [arXiv 2609.25050](https://arxiv.org/html/2609.25050). Proof repos: `tadamcz/erdos548` (5 stars, Apache-2.0, 2026-09-21), `tadamcz/erdos1`, `tadamcz/erdos126`, `tadamcz/erdos571` — [GitHub](https://github.com/tadamcz/erdos548). The main FrontierMath problem set is **not on GitHub** (`openai/frontier-math`, `epoch-research/frontiermath` both 404) — **non verificato / private by design**.
- **eth-sri/matharena** — https://github.com/eth-sri/matharena — 288 stars; MIT; Python; last commit 2026-09-15 ("docker command"). Evaluates LLMs on fresh competitions; final-answer contests auto-graded; proof contests (Putnam, IMC, IMO 2025, USAMO 2025) human-graded, others via LLM judges in `configs/judges/`; outputs (full reasoning traces + solutions) saved under `outputs/`, browsable with `uv run python app/app.py`; models added via YAML in `configs/models/`; needs Python 3.12+/uv, provider API keys, Docker for harness models — [README](https://github.com/eth-sri/matharena)
- **Proof grading**: **EnvCommons/IMO-Bench** — https://github.com/EnvCommons/IMO-Bench — 1 star; no license; Python; push 2026-09-24 (AnswerBench / ProofBench / GradingBench, Google DeepMind, EMNLP 2025) — [GitHub API](https://github.com/EnvCommons/IMO-Bench); [imobench.github.io](https://imobench.github.io/). **ProofGrader / ProofBench** (145 problems, 435 solutions graded 0–7 by olympiad experts; ProofGrader MAE 0.926) — [proofgrader.github.io](https://proofgrader.github.io/); the code URL "github.com/proofgrader/" could not be resolved to a repo — **non verificato**. Other same-name hits are unrelated (`OpenBMB/MA-ProofBench` 6 stars Lean 2026-08-26; `scasella/Proofgrade` 0 stars) — [GitHub search](https://github.com/search?q=ProofBench)
- **QwenLM/ProcessBench** — https://github.com/QwenLM/ProcessBench — 195 stars; no license; Python; last commit 2025-05-20; ACL 2025 — [GitHub API](https://github.com/QwenLM/ProcessBench)
- **openai/prm800k** — https://github.com/openai/prm800k — 2,147 stars; MIT; **archived 2026-05-29**; 800k step-level labels (−1/0/+1) in JSONL via Git LFS; `grading/grader.grade_answer(model_answer, gt_answer)` uses SymPy, "conservative" — [README](https://github.com/openai/prm800k)
- **math-inc/FrontierMathOpen-Hypergraphs** — 61 stars; Apache-2.0; Lean; push 2026-03-13 — [GitHub API](https://github.com/math-inc/FrontierMathOpen-Hypergraphs)

#### Group 4 — Multi-agent orchestration frameworks
- **anthropics/claude-agent-sdk-python** — 8,174 stars; MIT; push 2026-09-25 — [GitHub API](https://github.com/anthropics/claude-agent-sdk-python). **openai/openai-agents-python** — 29,728 stars; MIT; push 2026-09-27. **langchain-ai/langgraph** — 42,370 stars; MIT; push 2026-09-27. **crewAIInc/crewAI** — 59,103 stars; MIT; push 2026-09-27 — [GitHub API](https://github.com/crewAIInc/crewAI)
- Concrete math-research use: the only verified ones are indirect — `cameronfreer/lean4-skills` ships as a Claude Code and Codex plugin, `unsorry` workers are Claude/Codex/Gemini agents, and OpenEvolve accepts "Claude Code CLI" as its LLM backend — [lean4-skills README](https://github.com/cameronfreer/lean4-skills); [unsorry README](https://github.com/agenticsnz/unsorry); [OpenEvolve README](https://github.com/algorithmicsuperintelligence/openevolve). A web search for LangGraph/CrewAI/Claude-SDK math or Lean examples returned only generic framework comparisons — [oxylabs comparison](https://github.com/oxylabs/AI-agent-frameworks)

#### Awesome lists / curated indexes (observed 2026-09-28)
- **webfuse-com/awesome-autoresearch** — https://github.com/webfuse-com/awesome-autoresearch — 2,542 stars; CC0-1.0; push 2026-09-21; six sections (general descendants, research-agent systems, platform ports, domain adaptations, evaluation & benchmarks, writeups); "emphasises empirical ML optimisation rather than formal mathematics" — [README](https://github.com/webfuse-com/awesome-autoresearch)
- **HKUST-KnowComp/Awesome-LLM-Scientific-Discovery** — 439 stars; MIT; push 2026-07-03; companion of EMNLP 2025 survey — [GitHub API](https://github.com/HKUST-KnowComp/Awesome-LLM-Scientific-Discovery)
- **tongyx361/Awesome-LLM4Math** — 160 stars; MIT; **last push 2024-07-12** (stale) — [GitHub API](https://github.com/tongyx361/Awesome-LLM4Math)
- **marcusm117/Awesome-Autoformalization** — 3 stars; Apache-2.0; push 2026-06-09 — [GitHub API](https://github.com/marcusm117/Awesome-Autoformalization)
- **subroy13/awesome-ai-proofs** — 15 stars; MIT; push 2026-09-09; "curated list of mathematical proofs generated by artificial intelligent system" — [GitHub search](https://github.com/subroy13/awesome-ai-proofs)
- **Xinze-Li-Moqian/awesome-ai4math** — 11 stars; MIT; push 2026-04-29 — [GitHub API](https://github.com/Xinze-Li-Moqian/awesome-ai4math)
- **zhaoyu-li/Awesome-Machine-Learning-for-Theorem-Proving**: 404 on 2026-09-28 and no matching repo under that user — **non verificato** (possibly renamed or removed).

### Inferences
- For a team that wants "proofs and certificates", the reusable building blocks are the verifier-side components: `kimina-lean-server` (HTTP Lean checker), `LeanOpenProblems` (Inspect task + Comparator, two-container isolation), `formal-conjectures` (problem statements), `lean4-skills` (agent workflow with axiom checking). The loop harnesses (autoresearch/OpenEvolve/ShinkaEvolve) are useful as *search* engines for constructions (packings, extremal objects) but their output is a float, not a proof.
- ShinkaEvolve is the most complete "store everything" harness (SQLite archive + genealogy UI + pricing snapshot); OpenEvolve is the most portable (any OpenAI-compatible endpoint, Claude Code CLI); autoresearch is the simplest (git branch + TSV) but its integrity model is prose-only.

### Gaps
- Exact Lean toolchain versions for alphaproof-nexus-results, PutnamBench, formal-conjectures were not read from `lean-toolchain` files.
- No cost or run-time figures published for AgentLaboratory, AI-Researcher, CycleResearcher.
- Whether `ProofGrader` code is public could not be confirmed.

## Key question 1 — Actively maintained (commit in last 3 months, i.e. after 2026-06-28) vs abandoned

### Takeaway
Active: ShinkaEvolve, OpenEvolve (borderline: 2026-07-18), AutoResearchClaw, mathlib4, lean4, LeanCopilot, LeanDojo-v2, PutnamBench, MathArena, formal-conjectures, equational_theories, LeanOpenProblems, lean4-skills, unsorry, lean4web, LLM4AD_Next. Frozen/abandoned: autoresearch upstream (Mar 2026), funsearch (Feb 2024), AI-Scientist v1/v2 (Dec 2025), AI-Researcher (Oct 2025), AgentLaboratory (Aug 2025), alpha-research (Nov 2025), all prover repos (DeepSeek-V2 Jul 2025, Kimina Jul 2025, Goedel-V2 Aug 2025, Seed-Prover Feb 2026), LeanDojo v1 (deprecated Jan 2026), ReProver, ProcessBench, prm800k (archived), openai/miniF2F (archived).

### Cited Findings
- Last commit dates (API, 2026-09-28): ShinkaEvolve 2026-08-21; OpenEvolve 2026-07-18; AutoResearchClaw push 2026-08-19; LeanCopilot 2026-09-18; LeanDojo-v2 push 2026-08-10; PutnamBench 2026-09-24; MathArena 2026-09-15; formal-conjectures 2026-09-27; equational_theories 2026-09-12; LeanOpenProblems push 2026-09-27; lean4-skills push 2026-09-27; unsorry push 2026-09-03 — [GitHub API commits endpoint](https://docs.github.com/rest/commits/commits)
- Frozen: autoresearch 2026-03-26; funsearch 2024-02-05; AI-Scientist and v2 2025-12-19; AI-Researcher 2025-10-16; AgentLaboratory 2025-08-20; alpha-research 2025-11-12; DeepSeek-Prover-V2 2025-07-18; Kimina-Prover-Preview 2025-07-10; Goedel-Prover-V2 2025-08-27; Seed-Prover 2026-02-13; LeanDojo 2026-01-18 (deprecation notice); ReProver 2025-01-30; ProcessBench 2025-05-20; llmlean 2025-10-10; leanblueprint 2025-12-23 — [GitHub API](https://docs.github.com/rest/commits/commits)
- Archived flags: `openai/miniF2F` archived=true; `openai/prm800k` archived=true (README: archived 2026-05-29) — [GitHub API](https://github.com/openai/prm800k)
- LeanDojo README: "deprecated. Please use LeanDojo-v2 for all new projects" — [README](https://github.com/lean-dojo/LeanDojo)

### Inferences
- Prover repos are release artifacts for papers; expect no support. Weight releases live on Hugging Face and the GitHub repo rarely changes afterwards.
- autoresearch's ecosystem moved to descendants (AutoResearchClaw, pi-autoresearch, Claude/Codex "skills") rather than the upstream repo.

### Gaps
- "Last push" (`pushed_at`) can be newer than the last default-branch commit because of branches/PRs; both are reported where they differ (e.g. ShinkaEvolve push 2026-09-24 vs commit 2026-08-21).

## Key question 2 — Runs on a laptop with only an LLM API key, no GPU?

### Takeaway
Yes: OpenEvolve, ShinkaEvolve, AlphaResearch's loop (but not its reward model), AgentLaboratory, AutoResearchClaw (CPU fallback), MathArena, kimina-lean-server (CPU + ~8 GB RAM per REPL), LeanDojo/LeanDojo-v2 tracing, lean4-skills, unsorry, LeanCopilot (CTranslate2 CPU). No: karpathy/autoresearch upstream (NVIDIA only; macOS/MLX forks exist), AI-Scientist-v2 (Linux + NVIDIA), all open-weight provers (7B–671B) and CycleResearcher/Reviewer weights.

### Cited Findings
- OpenEvolve: "any OpenAI-compatible API", local Ollama/vLLM/LM Studio, "Claude Code CLI (no API key needed)", Python 3.10+, no GPU mentioned — [README](https://github.com/algorithmicsuperintelligence/openevolve)
- ShinkaEvolve: Python ≥3.10, PyTorch optional, runs locally or on SLURM — [README](https://github.com/SakanaAI/ShinkaEvolve)
- autoresearch: single NVIDIA GPU, "does not support CPU or MPS"; forks `miolini/autoresearch-macos` (2,396 stars), `trevin-creator/autoresearch-mlx` (1,848), `ncdrone/autoresearch-ANE`, and open issue #582 "Apple Silicon MPS port" — [README](https://github.com/karpathy/autoresearch); [forks](https://github.com/karpathy/autoresearch/forks)
- AI-Scientist-v2: "Linux with NVIDIA GPUs (CUDA/PyTorch)", LaTeX, Python 3.11+, $15–20/run — [README](https://github.com/SakanaAI/AI-Scientist-v2)
- kimina-lean-server: REPL pool default CPU−1, "8GB+ RAM per REPL instance", Docker — [README](https://github.com/project-numina/kimina-lean-server)
- LeanCopilot: "Optional but recommended: CUDA-enabled GPU", CTranslate2 local inference, Linux/macOS — [README](https://github.com/lean-dojo/LeanCopilot)
- Goedel-Prover-V2 needs 8B/32B weights on GPU (`device_map="auto"`); DeepSeek-Prover-V2 is 7B or 671B — [Goedel README](https://github.com/Goedel-LM/Goedel-Prover-V2); [DeepSeek README](https://github.com/deepseek-ai/DeepSeek-Prover-V2)
- MathArena: uv + Python 3.12, provider API keys, Docker only for harness models — [README](https://github.com/eth-sri/matharena)

### Inferences
- A laptop stack for our use: Lean 4 + mathlib (cache download), kimina-lean-server or plain `lake env lean` as verifier, an API-key LLM (Claude/OpenAI) driven by OpenEvolve/ShinkaEvolve for constructions or lean4-skills for proofs. Mathlib build/cache needs tens of GB of disk and time — not measured here.

### Gaps
- No measured laptop timings for any harness; README cost estimates only (OpenEvolve $0.01–0.60/iteration; AI-Scientist $15–20/run).

## Key question 3 — Structured, reproducible storage of attempts, verdicts, traces

### Takeaway
ShinkaEvolve (SQLite + WebUI + pricing snapshot) and OpenEvolve (checkpointed `openevolve_output/`, seeded, YAML config) are the most structured; autoresearch uses a 5-column TSV plus one git commit per attempt; MathArena keeps full model traces in `outputs/`; AutoResearchClaw uses timestamped run folders with SHA256 checksums; AI-Scientist-v2 keeps a tree of experiment nodes in `experiments/`; LeanOpenProblems relies on the Inspect framework's eval logs; prm800k is a JSONL step-label schema.

### Cited Findings
- autoresearch `results.tsv`: columns `commit, val_bpb, memory_gb, status, description`, status `keep|discard|crash`, kept untracked; each experiment is a git commit on branch `autoresearch/<tag>` — [program.md](https://github.com/karpathy/autoresearch/blob/master/program.md)
- ShinkaEvolve: "Results persist in SQLite databases", islands/elites in DB, `results_dir` auto-created, `pricing_snapshot.json` at start, `shinka_visualize` genealogy WebUI, optional W&B — [README](https://github.com/SakanaAI/ShinkaEvolve)
- OpenEvolve: `openevolve_output/` with generation checkpoints, deterministic seed 42, "Hash-based component isolation", evaluator returns `metrics` + `artifacts` — [README](https://github.com/algorithmicsuperintelligence/openevolve)
- MathArena: `outputs/` with "full reasoning traces (if available) and solutions", local viewer app — [README](https://github.com/eth-sri/matharena)
- AutoResearchClaw: "Run artifacts stored in timestamped folders with SHA256 checksums", JSON metrics, knowledge-base entries with 30-day decay — [README](https://github.com/aiming-lab/AutoResearchClaw)
- AI-Scientist-v2: timestamped `experiments/` with `unified_tree_viz.html` — [README](https://github.com/SakanaAI/AI-Scientist-v2)
- AgentLaboratory: `state_saves` checkpoints — [README](https://github.com/SamuelSchmidgall/AgentLaboratory)
- LeanOpenProblems: "built on the Inspect evaluation framework", runs at scale with METR Hawk — [README](https://github.com/epoch-research/LeanOpenProblems)
- unsorry: git repo is the queue; claims and decompositions "in a machine-validated format (AISP)"; ADRs in `docs/adrs/` — [README](https://github.com/agenticsnz/unsorry)
- prm800k JSONL fields: labeler id, timestamp, generation, question metadata, steps with ratings −1/0/+1, completions, finish reason, labeling time — [README](https://github.com/openai/prm800k)

### Inferences
- None of the loop harnesses records a *proof-level* verdict; their "verdict" is the metric. For certificates, the storage model of LeanOpenProblems (Inspect log + Comparator pass/fail) or unsorry (PR + CI kernel re-check) is the relevant pattern.

### Gaps
- Exact SQLite schema of ShinkaEvolve and checkpoint file format of OpenEvolve were not inspected in code.

## Key question 4 — Separate verifier/referee component and how it is implemented

### Takeaway
Three implementation styles: (a) user-written numeric evaluator in-process (OpenEvolve `EvaluationResult`, ShinkaEvolve `evaluate.py`, autoresearch `val_bpb` — no isolation from the agent in autoresearch); (b) learned/LLM reviewer (AlphaResearch RM-7B, CycleReviewer/DeepReviewer, AI-Scientist reviewer, AutoResearchClaw peer-review + VerifiedRegistry, MathArena LLM judges for proofs); (c) Lean kernel as judge, ideally in a separate container (LeanOpenProblems + Comparator; unsorry CI "Gate A"; kimina-lean-server pass/sorry/error; Goedel-V2 compiler-feedback self-correction).

### Cited Findings
- LeanOpenProblems: "A submission counts only if it passes Comparator, the Lean FRO's adversarially robust proof checker. The agent works in one sandboxed container, and comparator runs in a separate one. This setup defeats many classes of attacks" — [README](https://github.com/epoch-research/LeanOpenProblems); Comparator at [leanprover/comparator](https://github.com/leanprover/comparator)
- unsorry: worker verifies locally, "Gate A re-verifies in CI and auto-merges … no human in the correctness path" — [README](https://github.com/agenticsnz/unsorry)
- kimina-lean-server returns whether proofs "succeed, contain sorries, or produce errors" per request id — [README](https://github.com/project-numina/kimina-lean-server)
- OpenEvolve: "User-defined scoring system that returns metrics and optional execution feedback"; cascade evaluation — [README](https://github.com/algorithmicsuperintelligence/openevolve)
- ShinkaEvolve: `evaluate.py` scripts "run multi-sample experiments, validate correctness, and aggregate metrics into a combined_score" — [README](https://github.com/SakanaAI/ShinkaEvolve)
- autoresearch: the metric is printed by the agent-editable `train.py`; issue #599 shows it can be gamed — [issue #599](https://github.com/karpathy/autoresearch/issues/599)
- AlphaResearch: "execution-based verifier" plus "a trained reward model to assess research quality" (AlphaResearch-RM-7B) — [README](https://github.com/answers111/alpha-research)
- CycleResearcher: reviewer models 8B/70B/123B; DeepReviewer with "self-verification" and OpenScholar retrieval — [README](https://github.com/zhu-minjun/Researcher)
- MathArena: LLM judges configured in `configs/judges/`; Putnam/IMC/IMO 2025/USAMO 2025 human-verified — [README](https://github.com/eth-sri/matharena)
- AutoResearchClaw: four-layer citation verification, "VerifiedRegistry enforces ground-truth experiment data; unverified numbers are sanitized" — [README](https://github.com/aiming-lab/AutoResearchClaw)
- Goedel-Prover-V2: "iteratively revise its own proofs by leveraging feedback from Lean's compiler", two correction rounds under 40K output tokens — [README](https://github.com/Goedel-LM/Goedel-Prover-V2)
- equational_theories: ATP outputs are re-verified in Lean; blueprint tracks status — [README](https://github.com/teorth/equational_theories)

### Inferences
- The only referee designs that are adversarially robust by construction are the Lean-kernel ones with process isolation (LeanOpenProblems). LLM-reviewer referees (b) are appropriate for triage, not for declaring a cell solved — consistent with our protocol (Researcher proposes, Referee approves).

### Gaps
- Comparator's own README was not fetched; its exact checks (axiom whitelist, `sorry`/`native_decide` handling) are not recorded here.

## Key question 5 — Concrete pitfalls reported in issues/discussions

### Takeaway
Reported pitfalls cluster into: metric gaming when the agent controls the evaluator (autoresearch #599); target-value leakage into prompts (OpenEvolve #117); prompt/marker parsing failures (OpenEvolve #106, ShinkaEvolve #190/#193 and README); cost (OpenEvolve README, AI-Scientist $15–20/run, ShinkaEvolve pricing snapshots, FrontierMath Erdős $300/attempt); broken dependencies and Lean version drift (LeanDojo #252/#211, AI-Scientist #253/#158); unsafe code execution requiring Docker (AI-Scientist-v2); benchmark contamination policies (PutnamBench "do not publish proofs").

### Cited Findings
- autoresearch #599: four ways to lower `val_bpb` without a better model (skip optimizer, short-circuit `evaluate_bpb`, …); rule is "prose only" — [issue #599](https://github.com/karpathy/autoresearch/issues/599)
- OpenEvolve #117 (open): "Reproducing circle packing without providing `TARGET_VALUE = 2.635` from AlphaEvolve paper"; #106 (open): "Not respecting the EVOLVE-BLOCK-START / END markers" — [issues](https://github.com/algorithmicsuperintelligence/openevolve/issues)
- OpenEvolve README "High costs: Start with fewer iterations, use cheaper models (Gemini-Flash), enable cascade evaluation"; "Evolution stagnation" — [README](https://github.com/algorithmicsuperintelligence/openevolve)
- ShinkaEvolve README pitfalls: misconfigured EVOLVE-BLOCK markers, low `max_patch_resamples`, embedding mismatch, unbalanced `max_evaluation_jobs` vs `max_proposal_jobs`; open issues #190 "re-base indentation when recovering a shifted patch", #193 "match extract_between tags literally" — [README](https://github.com/SakanaAI/ShinkaEvolve); [issues](https://github.com/SakanaAI/ShinkaEvolve/issues)
- AI-Scientist-v2 README: "$15–$20 per experiment run"; executes LLM-written code with "potential use of dangerous packages, uncontrolled web access, and spawning unintended processes"; Docker recommended; must disclose AI use in manuscripts — [README](https://github.com/SakanaAI/AI-Scientist-v2)
- AI-Scientist v1 issues #253 "Request for specific Python and dependency versions to avoid installation conflicts", #158 "dependencies", #173 `text8` 403 — [issues](https://github.com/SakanaAI/AI-Scientist/issues)
- LeanDojo issues #252 "Lean4Repl.lean fails on newer Lean versions (missing Std.TreeSet.union)", #211 "Issues with Running Tactics on Repos Using Lean >= v4.12.0", #250 "lean_dojo_repl not working" — [issues](https://github.com/lean-dojo/LeanDojo/issues)
- LeanCopilot README caveats: `libstdc++` symbol errors with `lean_exe`, `search_proof` termination errors, Windows native unsupported — [README](https://github.com/lean-dojo/LeanCopilot)
- PutnamBench: "Do not include proofs as confirmation in any public setting" — [README](https://github.com/trishullab/PutnamBench)
- FrontierMath Erdős budget: "$300 and 72 hours of working time per attempt", network-isolated container — [Epoch AI](https://epoch.ai/latest/announcing-frontiermath-erdos)
- prm800k grader "conservative … occasionally rejecting correct answers" — [README](https://github.com/openai/prm800k)

### Inferences
- Any loop we build must keep the evaluator outside the agent's write scope and re-run it independently (autoresearch's failure mode is exactly the one our CLAUDE.md forbids: "output float ⇒ never a proof").
- Pin Lean/Mathlib versions explicitly: every Lean tool above breaks on toolchain drift (LeanDojo v1, kimina default v4.26.0, Seed-Prover proofs v4.14.0, FrontierMath Erdős v4.27.0).

### Gaps
- No issue-tracker survey was done for MathArena, PutnamBench, LeanDojo-v2, AutoResearchClaw; cost blow-up reports for ShinkaEvolve/OpenEvolve beyond README guidance were not found in the sampled issues.

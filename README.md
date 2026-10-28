# everythingmath

**One command for any math problem, start to finish.** A Claude Code skill that acts as problem-setter, solver and the hardest referee you will meet. It works out what math job you have, reads the problem exactly, picks the best skills for it out of a catalog of about 120, solves with a plan, then tries to break its own answer three ways, fixes what it finds, and proves the result does what you asked before handing it over, with an honest confidence label.

```
/everythingmath prove that (a+b+c)^2 >= 3(ab+bc+ca) for positive reals
/everythingmath compute this integral and double check it
/everythingmath is my proof right? (paste or attach it)
/everythingmath solve this Putnam problem
/everythingmath explain Stokes' theorem from scratch
/everythingmath formalize this lemma in Lean
/everythingmath here is my problem set, help me with it
```

You do not have to type the command. Describing the math is enough ("solve this", "prove it", "check my answer").

## Why it is different

Most "solve my math problem" prompts produce a fluent answer that nobody checked. everythingmath is built around the ways math answers go wrong.

- **It tests claims, not formatting.** Every identity, derivative, integral value, closed form and limit goes through a bundled checker. A false statement is refuted by a counterexample, not argued around.
- **Two routes to every answer.** One derivation is a guess that looked consistent. The final answer must be confirmed by a second, independent method.
- **A blind re-solve.** A fresh agent sees only the problem, never your work, and solves it. The answers must match. A mismatch is the strongest error signal there is.
- **The referee reads every step.** `step_review.py` numbers each step; each is read against a ten-point test (theorem hypotheses, quantifier order, division by zero, case coverage, induction base, interchange of limits, and so on). A gate refuses to pass while a step is unread or a serious issue is open.
- **An adversarial verifier.** Another fresh agent hunts for the first failing step using a catalog of classic mistakes.
- **A closing gate.** Every thing you asked for is a numbered ledger line that must be marked PASS with evidence.
- **Honest labels.** `SOLVED`, `REFUTED`, `SOLVED-WITH-CAVEAT`, `PARTIAL`, `NO-CONFIDENT-SOLUTION`. It will not bluff, and it will say a problem statement is false when it is.
- **Integrity-aware.** If the material looks like a graded or application problem set, it asks whether outside help is allowed and otherwise switches to teach mode: hints, key ideas and checking your own attempt, instead of handing over a finished submission.

## The process

| Phase | What happens |
|---|---|
| 0 Ready check | Which helper skills and tools exist; mode (SOLVE, PROVE, COMPUTE, CHECK, FIX, WRITE, FORMALIZE, EXPLAIN, PACKET, RESEARCH, VISUAL); Light or Full |
| 1 Understand | Transcribe the problem verbatim and proofread it; restate; areas, level, deliverable, integrity check. Writes the **Math Brief**, the **Requirements Ledger**, the **Claim Ledger** |
| 2 Choose | One core method (for example `math-olympiad` or `math-proof-solo`) plus the fewest supporting skills |
| 3 Plan the attack | Small cases by script, conjecture, two or more candidate approaches with feasibility tests, theorems with exact hypotheses |
| 4 Solve | Notes, a stuck rule, a second route, a structured write-up |
| 5 Three check rounds | **Round 1** scripts. **Round 2** the referee's line-by-line read and fix. **Round 3** blind re-solve and adversarial verifier |
| 6 Closing gate | Ledger PASS or FAIL against your original words; claims and answer form confirmed |
| 7 Deliver | Solution, ledger, claims, checks, issues, notes (and `.tex`, PDF, Lean or code when asked) |
| 8 Report | Answer first with its confidence label, then what was checked and what needs you |

## Install

```bash
git clone https://github.com/aaryavvatts-lab/everythingmath ~/.claude/skills/everythingmath
```

Restart Claude Code (or start a new session), then type `/everythingmath`.

That is enough to use it: the checkers need only Python 3.9+ and the standard library. For the full power, install the helper skills it routes to. `catalog.md` lists every one with its source repository. Check what you have:

```bash
bash ~/.claude/skills/everythingmath/scripts/check_skills.sh --missing --tools
```

Optional programs: SymPy (`pip install sympy`), a LaTeX engine (tectonic, latexmk or pdflatex), Lean 4 with Lake. The skill says plainly when something it needs is absent and never claims a result it could not check.

## The tools

All plain Python 3 or bash, standard library only. Run them on their own any time.

| Script | What it does |
|---|---|
| `scripts/verify_identity.py` | `eq` (identities), `ineq` (inequalities, shows the tight point), `deriv`, `integral` (finite and improper), `sum` (exact rational), `limit`. A pass is evidence, a fail is a counterexample |
| `scripts/counterexample.py` | Brute-force search over integer ranges for counterexamples or witnesses, with helpers such as `is_prime`, `is_square`, `phi`, `tau`, `sigma` |
| `scripts/proof_lint.py` | Gap markers, hand-waving phrases, unbalanced math delimiters, induction without a base case, unfinished case splits, missing answer line |
| `scripts/step_review.py` | Numbers every step of a solution (S001...) and writes the Coverage checklist for the referee read |
| `scripts/issue_register.py` | Summarises issues and gates on open FATAL or MAJOR issues and unread steps |
| `scripts/ledger_check.py` | Grades the Requirements Ledger |
| `scripts/compile_check.sh` | Builds the LaTeX solution (tectonic, latexmk or pdflatex), counts errors and undefined references |
| `scripts/check_skills.sh` | Which catalog skills and programs are present |

Run the regression tests with `bash tests/run_tests.sh`. They seed false identities, a false inequality, a broken proof and open issues, and require each checker to catch them.

## Honest limits

- It cannot make a false statement true, and it will say so rather than produce a bogus proof.
- Passing the scripts is evidence, not proof. Whether an argument is valid is decided by the referee read and the independent agents, and a person still decides what to submit.
- Very hard or open problems may end `PARTIAL` or `NO-CONFIDENT-SOLUTION`. That is a feature.
- It cannot check Lean proofs without Lean installed, or build PDFs without a LaTeX engine; it says so.
- No tool can promise a correct answer on every problem. The point is to make wrong answers rare and visible.

## How it was built

Following the same pattern as the `fulldesign`, `everythingvideo`, `everythingpaper` and `everythingslideshow` director skills: inventory the best public math skills, read and vet them, write a catalog of what each is for and when to use it, write a director `SKILL.md` that understands the request, audits, routes, executes and checks, add deterministic scripts for what a model should not eyeball, and test against seeded failures (`tests/run_tests.sh`) until the scripts catch them. `evals/prompts.md` holds sample requests and what a good run must show.

## Repo layout

```
SKILL.md              the director: phases, ground rules, mode and core-method tables
catalog.md            every skill it can route to, with sources
references/
  recipes.md          step sequences per mode
  methods.md          toolbox per area of mathematics
  craft.md            rigor by level, solution structure, answer forms, confidence labels, teach mode
  checks.md           ledgers, the ten-point step test, failure patterns, verifier prompts, rubric
scripts/              the checkers (standard library only)
tests/run_tests.sh    regression tests with seeded failures
evals/prompts.md      sample requests
```

## Credits

The helper skills belong to their authors, linked in `catalog.md`: Anthropic's math-olympiad and math-proof plugins, googlarz/math-skill, foogtil/claude-code-math-skills, OctopusTide/claude-math-research-skill, XunZhiyang/math-proof-review, amelieloher/math-paper-skills, haruhisa-enomoto/math-paper-skills, hameefy/claude-latex-skill, cameronfreer/lean4-skills, scottnarmstrong/LeanAutoformalizationSkills, matt-w-horn/lean-skills, vltanh/formalize-math-paper, opum-ai/proof-skills, panpanc/math-skills, flonat/flonat-research, lingzhi227/agent-research-skills, parcadei/Continuous-Claude-v3, wanshuiyin/Auto-claude-code-research-in-sleep, K-Dense-AI/scientific-agent-skills, adithya-s-k/manim_skill and others. This repository is MIT licensed and holds only the director, catalog, references and checkers; helper skills keep their own licences.

## License

MIT.

# Recipes: step sequences per mode

Start from the matching recipe after Phase 2, then adjust. Every recipe still ends with the three check rounds, the closing gate and the report. Skill names are in `catalog.md`. Script names are in `scripts/`.

Contents: SOLVE · PROVE · COMPUTE · CHECK · FIX · WRITE · FORMALIZE · EXPLAIN · PACKET · RESEARCH · VISUAL · Multi-part problems with code

## SOLVE (find an answer and justify it)

1. Transcribe and restate (Phase 1). List what "all solutions" must include.
2. Explore small cases by script (`counterexample.py` to list solutions in a range, `verify_identity.py` to test a conjectured formula). Guess the answer.
3. Prove it: find all solutions, then show nothing else works (a necessity argument) and that the found ones work (a sufficiency check by substitution).
4. Core: `math-olympiad` for competition problems, `math-skill` for general ones.
5. Second route: a different derivation or numerical solve (for equations, solve numerically on a grid and compare the root list).
6. Rounds 1 to 3, gate, deliver. The answer sits at the top.

## PROVE (a statement is given)

1. Restate with quantifiers and hypotheses. Test the statement for small cases and edge cases first (`counterexample.py`). If it is false, the deliverable is the counterexample, verified by script and by hand, plus the nearest true statement with its proof; the label is `REFUTED` and the ledger's Asked lines are rewritten to "establish whether it holds". A refutation that fits in 15 lines is a Light job.
2. Choose the proof shape (direct, contradiction, induction, extremal, double counting, construction, invariant, probabilistic). `references/methods.md`.
3. Core: `math-proof-solo` (or `math-proof-siege` for hard cases), `math-rigor` for step-by-step with SymPy checks, `math-olympiad` for competition style.
4. Keep the Claim Ledger current; prove lemmas separately and check each by Round 1.
5. Rounds 1 to 3. The adversarial verifier gets the Claim Ledger. Gate. Deliver `solution.md` and optionally `.tex`.

## COMPUTE (calculation or derivation)

1. Write the setup and the conditions under which the technique applies (convergence, domain, orientation).
2. Compute by hand, with every step shown. Core: `math-skill`; `sympy` when installed.
3. Verify with `verify_identity.py`: `integral` for definite and improper integrals, `deriv` for derivatives, `sum` for finite sums, `limit` for limits, `eq` for identities. Compare with the claimed value.
4. Second route: a different technique (integration by parts versus substitution, series versus closed form, a numerical evaluation).
5. Light jobs may use short Round 2 and a one-line Round 3.

## CHECK (verify someone else's solution; report only)

1. Transcribe the problem and the solution. Do not trust the claimed answer; run a blind solve of the problem first.
2. Round 1 on their claims; Round 2 step by step with `step_review.py`; skills `math-proof-review`, `verify-math`, `proof-checker` as second readers.
3. The deliverable is a report: verdict (correct, correct with gaps, incorrect), the first failing step with quote and reason, every other issue by severity, and a suggested fix for each. No edits to their file.
4. Be fair: say what is right and what is only unjustified rather than wrong.

## FIX (find the errors and repair the proof)

1. Run CHECK first. Fix in severity order; keep the author's structure and notation where it is sound.
2. Write the repaired proof as a new file beside the original (never overwrite). List every change and why in `CHANGES.md`.
3. If a claim is false, say so, give the counterexample, and offer the nearest true statement with its proof.
4. Re-run Rounds 1 to 3 on the repaired proof.

## WRITE (typeset, polish, or turn a result into a document)

1. The math is checked first; writing never changes a claim. If the write-up exposes a gap, return to PROVE.
2. Skills: `latex-math-writing` for drafting and polish, `math-latex` for theorems and Beamer, `latex-guardian` to protect verified derivations during edits, `polish-math-prose` last, `sentence-audit` and `deslop` on prose only.
3. A whole paper: hand off to `/everythingpaper` with this skill as the proof engine.
4. Compile with `scripts/compile_check.sh`; read the PDF pages; check every symbol is defined before use and every reference resolves.
5. Citations: verify each exists (`citation-verifier`, `crossref`) and says what you claim.

## FORMALIZE (Lean 4)

1. Write the statement first and audit it: is it faithful, non-vacuous, free of junk values (`lean-verification`, `lean-statement-audit`)?
2. Skeleton with `sorry`, then fill one at a time (`lean4-theorem-proving`, `lean-proving`; `loogle` before proving anything from scratch).
3. Build with `lake build`; the result must contain no `sorry` and no unexpected axioms. If Lean is not installed, say so; never claim a proof compiles that you did not build.
4. For a whole paper use `formalize-math-paper`.

## EXPLAIN (teach)

1. Find the learner's level and what they already know; if unknown, assume one level below the topic.
2. Skills: `pp-deep-explain` for a thorough explanation, `pp-bottom-up` or `pp-reinvent-from-scratch` for motivation, `pp-theorem` for a theorem with its proof, `pp-generalization-ladder` for context.
3. Include a worked example, a non-example, and a short exercise with its answer.
4. If the integrity rule applies (graded work), stay in teach mode: hints and checks, not the finished submission.

## PACKET (several problems at once)

Homework sets, entrance problem sets, contest papers.

1. Transcribe all problems into `problems.md` (verbatim, one block per problem and part). Proofread the transcription.
2. Policy check once for the whole packet (Ground rules). If teach mode applies, produce a study plan and hints per problem instead of solutions.
3. Create `PACKET.md`: a table with problem, area, mode, status, confidence label, method, second route, blockers.
4. Solve each problem as its own Full or Light job in its own folder (`math/<set>/p1/`, ...). When the Agent tool is available, run independent problems in parallel, each with its own blind re-solve.
5. Order by dependency (a later part may use an earlier one), not by difficulty.
6. Consolidation pass: uniform notation, shared definitions stated once, cross-references correct, one final read of every answer against its question. Re-run `proof_lint.py` on the combined document.
7. Report one line per problem with its label, then the open gaps.

## RESEARCH (open-ended)

1. State the question precisely and what would count as progress. Literature first (`literature-search`, `paper-lookup`, scholarly search tools); every source opened and read.
2. Core: `math-research-campaign` for a gated multi-agent push, `math-proof-siege` for long proofs.
3. Keep a ledger of attempts and dead ends. Distinguish known, new, and conjectured; never present a conjecture as a theorem.
4. Formalize or computationally certify key claims where possible (`lean4-theorem-proving`, exact arithmetic).
5. The deliverable states plainly what is proved. If nothing new is proved, say so.

## VISUAL (slides, figures, animation)

1. The mathematics is correct first; visuals express it and never decide it.
2. Slides: `/everythingslideshow` (Beamer for equation-heavy talks). Figures: `math-figures` for TikZ, `academic-plotting` for plots. Animation: `manim-composer` to plan, `manimce-best-practices` to build.
3. Every plotted value comes from code you ran. Axes labelled, units stated, one idea per figure.
4. Check the equations on each slide against the verified solution, symbol by symbol.

## Multi-part problems with code (proof plus computation plus experiment)

Problems that ask for a proof, an exact formula, an algorithm and an experiment together (common in entrance sets):

1. Treat each part in its own form: the proof as a proof, the exact values as computations verified by script, the algorithm as pseudocode then runnable code, the experiment as a table.
2. Compute small exact cases first (by hand and by exact rational arithmetic); they are the check for the code.
3. Run the code with a stated seed and sample size; produce the table (parameters, sample size, estimate, exact value, absolute error) from the real run; compare with the stated error bound (for example, Hoeffding).
4. Include the code as a file in the output folder and print its output in the solution.
5. Rounds 1 to 3 apply to the proof parts as usual; for code parts, Round 1 is running it and comparing to exact values, and Round 3's blind agent re-implements it independently and the tables are compared.

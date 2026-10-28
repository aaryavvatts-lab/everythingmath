# Checks: ledgers, the referee's read, independent grading

Contents: Requirements Ledger · Claim Ledger · CHECKS.md · Round 1 checklist · Round 2 protocol and the ten-point step test · Failure patterns · Issue format and severity · Round 3 blind re-solve and adversarial verifier · Rubric

## Requirements Ledger (`ledger.md`)

Written in Phase 1, before solving. It is the contract. Phase 6 grades the finished solution against it.

```markdown
# Ledger: <problem or job name>
User request (verbatim): "<their words>"

| ID | Kind | Requirement | Status | Evidence |
|----|------|-------------|--------|----------|
| R1 | Asked | Find all real solutions of f(x) = 0 | OPEN | |
| R2 | Asked | Full proof, not just the answer | OPEN | |
| R3 | Implied | Every case covered, case split stated as exhaustive | OPEN | |
| R4 | Implied | Hypotheses of every cited theorem verified | OPEN | |
| R5 | Implied | Final answer confirmed by a second route | OPEN | |
| R6 | Implied | Answer in the requested form (simplified, exact) | OPEN | |
| R7 | Implied | No claim stronger than what was proved | OPEN | |
```

Status is `OPEN` until Phase 6, then `PASS`, `FAIL` or `BLOCKED` (needs something only the user can supply). Evidence names a step, script output or file. `ledger_check.py` exits non-zero while anything is `OPEN` or `FAIL`. Write requirements so they can be checked: "show the work" is vague, "every step has a stated reason" can be checked.

## Claim Ledger (`claims.md`)

```markdown
| Claim | Statement | How established | Status |
|-------|-----------|-----------------|--------|
| C1 | f is continuous on [0,1] | direct (composition of continuous maps) | proved |
| C2 | Max exists | Extreme Value Theorem; hypotheses: continuous on compact | cited-checked |
| C3 | The sum equals n(n+1)/2 | induction; verify_identity sum 1..60 | proved |
| C4 | The limit is 1/2 | numeric table only | numeric-only |
```

Statuses: `proved` (argument is on the page), `cited-checked` (a named theorem whose hypotheses you verified here), `numeric-only` (script evidence, no argument), `open` (neither). The final confidence label must be consistent with this table.

## CHECKS.md template

```markdown
# CHECKS
Date: ...  Problem: ...  Mode: ...  Core: ...

## Round 1 Technical
verify_identity: <which claims, pass/fail>
counterexample: <ranges searched, result>
proof_lint: <n FAIL, n WARN> -> fixed / explained
answer plugged back: <check and result>
second route: <method, result>
compile_check / Lean build: <result or n/a>

## Round 2 The referee's read
Steps reviewed: N of N. Issues: F FATAL, M MAJOR, m MINOR, n NIT. Fixed: ... Blocked: ...
issue_register --gate: PASS

## Round 3 Independent
Blind re-solve answer: ...   Match with solution: yes / no (explain)
Verifier scores: correctness 5, rigor 4, clarity 5, answer form 5, evidence 4. First failing step found: none / S014
Fixes after scoring: ...

## Closing gate
Ledger: R1 PASS ... (ledger_check: DONE)
Claims: all proved or cited-checked / open: ...
Confidence label: SOLVED | SOLVED-WITH-CAVEAT | PARTIAL | NO-CONFIDENT-SOLUTION
```

## Round 1 checklist

Run what applies; a pass is evidence only.

- Every identity, derivative, integral value, closed form and limit stated in the solution goes through `verify_identity.py`. Test the *claim as written*, not a re-derived version.
- Integer-valued claims (divisibility, primality, parity, residues, counts) go through `counterexample.py` over a range wide enough to include small special cases and the first nontrivial ones.
- The final answer is substituted into the original equation, constraint or definition (not into your simplified version of it).
- The general formula is tested at n = 1, 2, 3 and a boundary case. A formula that fails n = 1 is wrong or has a stated domain.
- Sizes and signs: is the answer's magnitude plausible (a probability in [0, 1], a length positive, an integral of a positive function positive)?
- `proof_lint.py` has no FAIL and each WARN is fixed or explained.
- LaTeX compiles with no undefined references; a Lean proof builds with no `sorry`.
- If code is part of the answer: it runs, is seeded, and the results table matches the exact values within the stated error bound.

## Round 2 protocol: the referee's read

1. `python3 scripts/step_review.py solution.md --out qc/review/`
2. For each step, in order, run the ten-point test below. Tick the Coverage box in `issues.md` when the step has been read, whether or not it had issues.
3. Then do the global pass: Is the claim being proved the claim that was asked? Is the answer complete (all solutions, all cases)? Is there a case or an object the argument never mentions? Would the argument still "prove" a false nearby statement? (A proof that also proves something false is wrong.) What is the weakest step, and is it justified?
4. Log, fix in severity order, re-run Round 1, re-run `step_review.py` (changed steps are un-ticked), then the gate.

### The ten-point step test

1. **Claim.** What exactly does this step assert?
2. **Reason.** Which earlier step, hypothesis, definition or named theorem justifies it?
3. **Hypotheses.** Are that theorem's hypotheses satisfied here (continuity, compactness, positivity, finite dimension, independence, coprimality)?
4. **Quantifiers.** Is the order of "for all" and "there exists" right? Does a constant depend on something it must not?
5. **Domain.** Any division by something that could be zero, root or log of something possibly negative, branch choice, empty set?
6. **Cases.** Are the cases exhaustive and are overlaps harmless? Is a boundary case missing?
7. **Computation.** Recompute it independently (by hand or by script). Sign, factor of 2, off-by-one?
8. **Degenerate and equality cases.** n = 0 or 1, the zero vector, the equality case of an inequality, ties.
9. **Limits and interchanges.** Is any swap of limit, sum, integral or derivative justified? Is "for large n" given a threshold, and does a constant hide a dependence?
10. **Logic.** Circular? Uses something not yet defined or proved? Converse proved when "iff" is claimed? Example offered as proof?

## Failure patterns (what classic wrong proofs do)

Use these as search keys, in the referee read and in the verifier prompt.

- Cited theorem applied outside its hypotheses; "by symmetry" when the symmetry is not actually present; WLOG that loses generality.
- Quantifier swap; uniformity assumed; a constant that secretly depends on n.
- Division by zero; multiplying or squaring an inequality without sign control; extraneous roots after squaring; log or root of a possibly negative quantity.
- Incomplete case split; a boundary case or the degenerate case skipped.
- Induction without a base case, with a base case at the wrong n, or whose step needs more than the hypothesis gives; strong induction used where simple induction was claimed; the step fails for the smallest n.
- Local extremum treated as global without compactness or boundary check.
- Existence proved but uniqueness assumed (or the reverse); a map not shown well defined on equivalence classes; "the" used before uniqueness.
- Limit, sum, integral or derivative interchange with no justification (dominated or monotone convergence, uniform convergence).
- Asymptotics: O-constants depending on parameters; limits and sup/inf swapped; Θ claimed from a one-sided bound.
- Counting: labelled versus unlabelled, ordered versus unordered, double counting, inclusion-exclusion with a missing term; off-by-one in ranges.
- Probability: independence assumed without proof; conditional versus joint; events not disjoint treated as disjoint.
- Direction: only one direction of an "iff" proved; sufficient mistaken for necessary.
- An example or a numerical check presented as a proof.
- Final answer: missing solutions, not simplified, wrong form, or valid only on part of the domain.
- Transcription: the problem statement itself was misread (an exponent, a sign, a hypothesis dropped).

## Issue format and severity

One block per issue in `issues.md`:

```markdown
## M003 | MAJOR | open
Location: S014 (and S015)
Quote: "Since f is continuous, f attains its maximum."
Problem: f is only continuous on the open interval (0,1); the Extreme Value Theorem needs a compact domain.
Fix: extend f to [0,1] or analyze the behaviour at the endpoints.
```

Severity: `FATAL` (the answer or the main argument is wrong), `MAJOR` (a gap or error a referee would reject for), `MINOR` (a fixable slip that does not change the result), `NIT` (style, notation, typography). Status: `open`, `fixed`, `blocked` (needs something only the user can supply), `out-of-scope` (a real issue outside what was asked, with a `Reason:` line).

## Round 3: independent minds

Both agents are fresh: they have not seen your reasoning. Give each exactly what is listed and nothing else.

### Blind re-solve prompt

> You are solving a math problem from scratch. Here is the problem, exactly as stated: <paste from problems.md>. Solve it completely. Report (1) your final answer in the form requested, (2) a derivation of at most 25 lines, (3) one independent check of your answer (a second method, special case, or substitution), and (4) your confidence (high, medium, low) with the step you trust least. Do not ask questions; state any interpretation you chose.

Compare the final answers. **They must agree** (up to equivalent form). If they disagree, find which is wrong by recomputing the disputed step by script. Do not choose by preference or by which one is more elegant.

### Adversarial verifier prompt

> You are a hostile but fair referee. Below are a problem and a proposed solution. Your job is to find the first step that fails. Before scoring, search the solution for each of these failure patterns: <paste "Failure patterns" above>. For every step, ask whether its hypotheses hold and recompute any calculation. Report: (1) the first failing step with a quoted line and exactly why it fails, or "no failing step found after checking every step"; (2) every gap you would reject a paper for; (3) scores 1 to 5 for correctness, completeness and rigor, clarity, answer form, and verification evidence; (4) the single weakest step. Do not praise; do not rewrite the solution.

Hand the verifier: the problem, `solution.md`, and the Claim Ledger. Do not hand it the Round 1 or 2 results (they would anchor it).

### Rubric

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Correctness | answer and every step verified; blind solve agrees | answer right, a step unjustified | wrong answer or wrong key step |
| Completeness and rigor | all cases, hypotheses checked, no gaps | a minor gap | main step missing |
| Clarity | a reader can follow every step | needs rereading | cannot follow |
| Answer form | exactly the requested form, simplified | right value, awkward form | missing or ambiguous |
| Verification evidence | second route and checks shown | one weak check | none |

Anything under 4 is fixed. A score that can only rise with something you do not have (a missing lemma you cannot prove) is not chased: record it as blocked and lower the confidence label.

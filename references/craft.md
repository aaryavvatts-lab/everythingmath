# Craft: how a finished solution should look

Contents: Rigor by level · Structure of a solution · Writing rules · Answer forms · Notation and LaTeX · Numerical evidence and code · Confidence labels · Teach mode

## Rigor by level

The bar is "a competent reader at that level could verify every step without guessing".

| Level | Expect |
|---|---|
| Calculus I to III (course work) | Show the method, the algebra, and the conditions (for example, why Green's theorem applies: closed, piecewise smooth, positively oriented; why a series converges: name the test and check its conditions). Answers exact, simplified, with units where relevant. |
| Linear algebra, ODE, intro analysis | Definitions used by name, theorems cited with hypotheses, epsilon-delta or sequence arguments written out where the course expects them. |
| Olympiad and entrance problems (AMC to IMO, Putnam, PRIMES-style) | A complete proof. Every case, every bound, every construction verified; the equality case stated; small cases checked. No "clearly". |
| Graduate and research | Full statements, precise hypotheses, every lemma proved or cited with a reference you checked; limitations stated. |
| Multi-part "explore" problems (proof plus computation plus code) | Each part answered in its own form: the proof written as a proof, the algorithm as pseudocode and code, the experiment as a table with parameters, estimate, exact value and error. |

## Structure of a solution

Use this skeleton in `solution.md` (adapt names to the problem):

```markdown
# Problem <n>
<statement, verbatim>

## Answer
<the final result, in the requested form, in one or two lines>

## Idea
<two or three sentences: the key insight and the plan>

## Solution
**Step 1.** <claim> Reason: <why>.
**Step 2.** ...
(case splits: "Case 1: ... Case 2: ... These cases are exhaustive because ...")

## Verification
<answer plugged back, special cases, the second method, the equality case>

## Remarks (optional)
<generalizations, why the hypotheses are needed, what fails without them>
```

Put the answer first: the reader should know the destination before the route. When the request holds a belief ("I think I can just use Green's theorem, right?"), the first line is the verdict ("No: the integral is 2 pi, and Green does not apply because ..."). For a pure proof, state the theorem in the "Answer" slot and end with the closing line ("which completes the proof").

## Writing rules

- One claim per step; every step carries its reason (a previous step number, a definition, a named theorem, a computation shown).
- Define every symbol once, before use. Keep one notation table for long solutions. Do not reuse a letter for two things.
- Name theorems and check hypotheses in the sentence that uses them ("the function is continuous on the compact set [0,1], so the Extreme Value Theorem gives a maximum").
- State what is being proved before proving it, especially in lemma chains and inductions ("We prove P(n) by induction on n. Base case n = 1: ... Inductive step: assume P(m); we show P(m+1): ...").
- Say why a case split is exhaustive. Say where each case's hypothesis is used.
- Prefer the shortest correct argument, then the clearest. A longer route that you verified beats an elegant one you did not.
- Never write "clearly", "obviously", "trivially", "it is easy to see", "similarly", "by symmetry", "the rest is routine" unless the reason follows in the same sentence.
- Do not pad. A solution is not improved by restating the problem in three ways.
- Honest limits: if a step is only numerically supported, say "numerically supported, not proved" at that step and in the label.
- Match the user's saved preferences (punctuation, tone, notation). Do not insert dashes the user has banned.

## Answer forms

- Exact over decimal: `\frac{\sqrt{3}}{2}`, not 0.866. Give a decimal beside it when the problem is applied.
- Simplified and rationalized; fractions in lowest terms; radicals reduced.
- Sets and intervals written as sets and intervals ("all real x with x > 2", `(2, \infty)`). "Find all" means a complete list and a proof there are no others.
- Constants named when asked ("the optimal constant is 2", with the extremal example and the proof of the bound).
- Probabilities in [0, 1], exact fractions when possible. Counts as integers.
- Multi-part problems: answer each lettered part under its own label, in the order asked.
- Existence versus value: if the problem says "find the minimum", show it is attained and where.

## Notation and LaTeX

- Inline `$...$`, display `$$...$$` or `\[...\]` in Markdown that will be read in a renderer; use `\begin{align*}` for multi-line derivations.
- One equation per line in long derivations, with the reason at the right or in the line above.
- Macros for repeated objects (`\newcommand{\R}{\mathbb{R}}`) in a `.tex` file; `\operatorname{}` for named operators.
- Compile and read the PDF page images; do not trust that the source "looks right". For a deliverable `.tex`, run `scripts/compile_check.sh`.

## Numerical evidence and code

- A table or a plot is evidence, not proof. Label it so.
- State the method, the sample size, the seed, and the tolerance. For Monte Carlo, give the standard error or the Hoeffding bound: with M samples, `P(|estimate - truth| > eps) <= 2 exp(-2 M eps^2)`, so `M >= ln(2/delta) / (2 eps^2)` gives error at most eps with confidence at least 1 - delta.
- Compare against the exact value whenever one exists (small cases, closed forms) and report the observed error in a table: parameters, sample size, estimate, exact value, absolute error.
- Make the code runnable as given: imports, seed, a `main` that prints the table. Run it before reporting numbers; never paste numbers you did not produce.
- Exact arithmetic (`fractions.Fraction`, rational arithmetic in SymPy) when the claim is an identity; floating point only for evidence of closeness.

## Confidence labels

State one in the report and at the top of the solution if it is not `SOLVED`.

- `SOLVED`: a complete argument; every claim `proved` or `cited-checked`; Round 1 to 3 passed; the blind re-solve agrees.
- `SOLVED-WITH-CAVEAT`: complete except one named step that is numerically supported but not proved (or a cited result you could not fully verify). The caveat is printed next to the answer.
- `REFUTED`: the statement as given is false. The counterexample is verified by script and by hand, and the nearest true statement is stated and proved. Say "false" first.
- `PARTIAL`: some parts proved, some gaps stated. List exactly which.
- `NO-CONFIDENT-SOLUTION`: no argument that survives checking. Report what was tried, what is known, and the most promising direction.

Never upgrade a label to look better. An honest `PARTIAL` is a good result; a hidden gap is not.

## Teach mode

Used when the integrity rule applies (graded, application or exam-like work) and the user has not confirmed that complete solutions are allowed, or when the user asks to learn.

Do: restate the problem, name the area and the standard technique, give graded hints (a nudge, then a stronger hint, then the key idea), explain the theorems involved with their hypotheses, check the student's own attempt line by line using Round 2, point at the exact step that fails and why, and suggest a similar practice problem you solve fully.
Do not: hand over a complete, submission-ready solution to the graded problem. Say in one line that you are in teach mode and that the user can tell you if solutions are allowed.

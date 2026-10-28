# Sample requests for everythingmath

Use these to try the skill and to check that a good run shows what is listed. Each states what a good run must show; none depends on a particular wording.

## 1. Routine calculus (Light)

> compute the integral of x*e^(-x) from 0 to infinity and double check it

A good run: Brief marks it Light; the answer 1 first; integration by parts shown; `verify_identity.py integral` run and reported; a second route (the Gamma function, Gamma(2) = 1); confidence `SOLVED`.

## 2. Olympiad-style proof (Full)

> Prove that for all positive reals a, b, c: (a+b+c)^2 >= 3(ab+bc+ca), and find when equality holds.

A good run: equality case a = b = c stated and proved; `verify_identity.py ineq` reports a tight margin near 0 at a = b = c; the proof is complete and uses no unjustified step; `proof_lint.py` clean; blind re-solve agrees; `claims.md` lists every claim.

## 3. A false claim (Full)

> Prove that n^2 + n + 41 is prime for every non-negative integer n.

A good run: runs `counterexample.py`, finds n = 40 (1681 = 41^2), says the statement is false, shows the verified counterexample, and offers the nearest true statement (it is prime for n = 0..39) with an honest note about what is and is not proved. It does not produce a bogus proof.

## 4. Check someone else's proof (CHECK mode)

> Is this right? "Let f(x) = |x|. Since f is continuous on [-1, 1], f is differentiable on (-1, 1) by the mean value theorem, so f'(0) exists."

A good run: report only, no edits; the first failing step quoted (the mean value theorem does not give differentiability; f is not differentiable at 0); the correct statement offered.

## 5. Multi-part problem with code (Full)

> (a) Show that the probability that a uniformly random binary string of length n has no two adjacent ones equals F(n+2)/2^n, where F(1) = F(2) = 1 are the Fibonacci numbers. (b) Write code estimating it by simulation and compare with the exact values for n = 4, 6 using at least two sample sizes.

A good run: exact counts F(n+2)/2^n verified by brute force; the code is saved, seeded and run; the table lists n, M, estimate, exact value, absolute error, all from the real run; the Hoeffding sample-size bound is stated.

## 6. Entrance or homework set (PACKET, integrity check)

> do my problem set (pdf attached) for the MIT PRIMES application

A good run: transcribes every problem verbatim; raises the integrity rule in one line (application problem sets usually require the applicant's own work); switches to teach mode unless the user confirms solutions are allowed: hints, key ideas, theorem hypotheses, and checking the user's own attempt. It does not hand over finished answers by default.

## 7. Photographed problem (Light)

> (photo of "Solve 2^x + 2^(x+1) = 12")

A good run: transcribes the equation and states the transcription for confirmation; solves (2^x * 3 = 12, so x = 2); plugs back; notes domain (all real x).

## 8. Lean (FORMALIZE)

> prove in Lean that the sum of the first n odd numbers is n^2

A good run: states the theorem, builds a skeleton, fills it, runs `lake build`, reports that no `sorry` remains. If Lean is not installed, says so instead of claiming a proof compiled.

## 9. Write-up (WRITE)

> typeset my solution to problem 3 as a clean LaTeX PDF (the solution is in solution.md)

A good run: does not change any claim; compiles with `compile_check.sh`; reads the PDF; defines every symbol before use.

## 10. Hard research-grade problem (RESEARCH)

> I want to improve the known lower bound for the cap set problem

A good run: states what is known with verified sources, does not claim a new result without a checked proof, labels the outcome `PARTIAL` or `NO-CONFIDENT-SOLUTION` honestly, and records the attempts.

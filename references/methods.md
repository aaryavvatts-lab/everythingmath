# Methods: the toolbox per area

Read in Phase 3. This is a map of standard moves, not a textbook. Use it to generate candidate approaches, then check feasibility.

Contents: First moves for any problem · Calculus I to III · Series and sequences · Differential equations · Linear algebra · Real and complex analysis · Abstract algebra · Number theory · Combinatorics · Probability · Geometry · Inequalities · Functional equations and polynomials · Proof shapes · Using code well

## First moves for any problem

- Small cases (n = 1, 2, 3, 4), degenerate cases, symmetric cases, extreme cases. Tabulate; look for the pattern; then prove it.
- Restate with quantifiers; find which hypotheses are doing the work (remove one and see what breaks).
- Look for an invariant, a monovariant, an extremal object, a symmetry, a bijection, a recursion.
- Strengthen the statement for induction; weaken for a first attempt.
- Work backwards from the target; find what would suffice.
- Ask: is the claim even true? Hunt a counterexample before investing in a proof.
- Special structure: homogeneity (normalize), symmetry (order the variables), periodicity, scaling.

## Calculus I to III

**Limits.** Algebraic simplification, conjugates, squeeze, L'Hopital (check the indeterminate form first), Taylor expansion, standard limits (sin x / x, (1 + 1/x)^x). One-sided limits for absolute values and piecewise functions.

**Derivatives and applications.** Chain, product, quotient, implicit and logarithmic differentiation. Optimization: critical points, endpoints, second-derivative test, and check that the extremum is global (compactness or behaviour at the boundary). Related rates: write the relation, differentiate in time, substitute only afterwards.

**Integration.** Decision order: simplify; substitution; parts (LIATE as a hint, tabular for repeated); trigonometric identities and substitutions; partial fractions (degree check first); completing the square; symmetry (odd/even, `x -> a - x`); differentiating under the integral sign; known integrals (Gaussian). Improper integrals: split at the singularities, test convergence (comparison, limit comparison, p-test) before computing. Always differentiate the antiderivative or run `verify_identity.py integral`.

**Series.** Convergence tests in order: divergence test; geometric/p-series; comparison/limit comparison; ratio/root; integral test; alternating series (and absolute versus conditional). Power series: radius by ratio test, then test the endpoints separately. Taylor with remainder: state the remainder bound (Lagrange). Closed forms by telescoping, differentiation/integration of a known series.

**Multivariable.** Partial derivatives and gradients; Lagrange multipliers (check the constraint qualification and compare all candidates plus boundary); second-derivative test (Hessian) and when it is inconclusive. Multiple integrals: sketch the region, choose coordinates (polar, cylindrical, spherical), compute the Jacobian, order of integration (Fubini conditions). Vector calculus: line integrals, conservative fields (curl zero on a simply connected domain), Green, Stokes, Divergence. Always state the hypotheses (closed, piecewise smooth, orientation) before using them.

## Series and sequences

Recurrences: characteristic equation, generating functions, telescoping, finding an invariant. Limits of sequences: monotone-bounded, squeeze, contraction fixed point. Asymptotics: compare with integrals, Stirling, Euler-Maclaurin; state the error term.

## Differential equations

Classify first (separable, linear first order, exact, homogeneous, Bernoulli; constant-coefficient linear; systems). Linear: homogeneous solution plus particular (undetermined coefficients, variation of parameters). Systems: eigenvalues and eigenvectors, matrix exponential. Always give the interval of validity, check the initial condition, and substitute back into the equation. Existence and uniqueness (Picard-Lindelof) when asked about solutions in general.

## Linear algebra

Row reduction for solving, rank, null space. Determinant tricks (row operations, block structure, matrix determinant lemma). Eigenvalues: characteristic polynomial, diagonalizability test (geometric versus algebraic multiplicity), spectral theorem for symmetric matrices, Jordan form when needed. Orthogonality: Gram-Schmidt, projections, least squares. Proof habits: prove things on a basis; use rank-nullity; use the trace and determinant as invariants; think of a matrix as a linear map. Check dimension counts.

## Real and complex analysis

Epsilon-delta: scratch work backwards to find delta, then write the forward proof. Compactness: Heine-Borel, extreme value, uniform continuity. Completeness: Cauchy sequences, monotone convergence, nested intervals. Uniform convergence and when it permits interchange; dominated and monotone convergence. Convexity: Jensen, tangent-line bounds. Complex: Cauchy-Riemann, contour integrals, residues (check the pole order and the contour), maximum modulus, Liouville. Always justify swapping limits.

## Abstract algebra

Check the structure axioms in the right order. Subgroup test; homomorphism and kernel; Lagrange, orbit-stabilizer, Sylow, class equation; isomorphism theorems. Rings: ideals, quotient, UFD/PID/Euclidean chain; polynomial rings and irreducibility (Eisenstein, reduction mod p, rational root). Fields: degree of extension, tower law, splitting fields. Show maps are well defined on cosets and classes.

## Number theory

Divisibility and gcd (Euclid, Bezout). Modular arithmetic: residues, orders, Fermat/Euler, CRT, quadratic residues and reciprocity. p-adic valuations and lifting-the-exponent. Diophantine equations: mod tricks to show no solutions, factoring, Vieta jumping, descent, parametrization, bounding then finite check (confirm the finite check by `counterexample.py`). Primes: sieve intuition, Chebyshev-type bounds (cite carefully). Multiplicative functions (tau, sigma, phi) and Dirichlet convolution.

## Combinatorics

Count the same thing two ways; bijections; inclusion-exclusion; recursion; generating functions; pigeonhole and its weighted forms; extremal principle; invariants and colorings; probabilistic method; graph theory basics (degree sum, trees, Hall, Turan). Decide labelled versus unlabelled, ordered versus unordered before counting. Verify counts for small n by brute force.

## Probability

Define the sample space and the probability measure. Linearity of expectation (no independence needed), indicator variables, conditioning and the law of total probability/expectation, symmetry, generating functions, coupling. Concentration: Markov, Chebyshev, Chernoff/Hoeffding (state the conditions). Monte Carlo and percolation-style models: exact small cases by enumeration, then simulation, then compare. Do not assume independence without proof.

## Geometry

Choose a method: synthetic (angle chasing, similar triangles, power of a point, cyclic quadrilaterals), coordinates, vectors, complex numbers, barycentric coordinates, inversion. Draw the configuration and check it on a second, different figure to avoid configuration-dependent errors. Lines in space: direction vectors, cross products, distances between skew lines via the scalar triple product, Plucker coordinates. Verify a computed result by coordinates numerically.

## Inequalities

Know the equality case first and keep it. Tools: AM-GM, Cauchy-Schwarz, Holder, Jensen, rearrangement, Chebyshev, Muirhead, SOS (sum of squares), Schur, tangent-line trick, substitution to normalize (homogeneity), mixing variables, calculus (single-variable minimization). Test numerically (`verify_identity.py ineq` reports the tightest point). Do not square or multiply without sign control.

## Functional equations and polynomials

Substitute special values (0, 1, -1, x = y, y = f(x)); prove injectivity/surjectivity; find f(0), f(1); guess the family, then verify it satisfies the equation (sufficiency) and that nothing else does (necessity). Polynomials: degree arguments, roots and multiplicities, Vieta, interpolation, Chebyshev polynomials, values at integers. Always check the final answer in the original equation.

## Proof shapes

Direct; contrapositive; contradiction; induction (simple, strong, structural, on a cleverly chosen quantity); construction (existence by example); counting; extremal; pigeonhole; probabilistic; invariants; compactness; continuity (intermediate value); algebraic identity plus positivity. Write down which one you are using in the first sentence.

## Using code well

- Exact first: `fractions.Fraction` or SymPy rational arithmetic for identities; floats for evidence.
- Brute force small cases to find or kill conjectures (`scripts/counterexample.py`), then prove.
- Monte Carlo: seed it, state M, compute the error against an exact value, use the Hoeffding bound for M.
- Search for extremal configurations numerically, then prove optimality analytically.
- Never report a number you did not run. Never present a numerical result as a proof.

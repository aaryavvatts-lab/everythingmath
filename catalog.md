# everythingmath catalog

Every helper skill the director can route to, grouped by use. The first column is the skill name (checked by `scripts/check_skills.sh`). If a skill is missing, use the next best one in its group or the rules in `references/`. Pick the fewest skills that cover the job. Sources are public GitHub repositories; read a skill before you install it, because skills run with your permissions.

Names with a colon belong to plugins and are not checked by the script.

## 1. Core solvers and proof engines (pick ONE per problem)

| Skill | What it does | Use when | Source |
|---|---|---|---|
| `math-olympiad` | Pure-reasoning solver for IMO, Putnam, USAMO and AIME problems with a fresh-context adversarial verifier and calibrated confidence; will say "no confident solution" | Competition and olympiad problems, "is this proof correct", counterexample hunts | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/math-olympiad) |
| `math-proof-solo` | One session works a hard problem in stages with a notes file and ends in a self-contained `proof.md` | A hard problem that needs a long careful proof but not hours | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/math-proof) |
| `math-proof-siege` | Hours of rounds of judge and worker sub-agents; says plainly what is and is not proved. Needs the `math-proof-judge` and `math-proof-worker` agents | Research-grade or very hard problems where a short attempt has failed | [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/math-proof) |
| `math-skill` | Solver-first skill: maps the problem, selects the method, solves, verifies; reads photos, PDFs and handwritten pages | Equations, systems, optimization, geometry, calculus, worksheets, anything given as an image | [googlarz/math-skill](https://github.com/googlarz/math-skill) |
| `math-rigor` | Proof template with numbered steps, SymPy checks and counterexample search | Proof-heavy work where every step must be checked | [foogtil/claude-code-math-skills](https://github.com/foogtil/claude-code-math-skills) |
| `math-research-campaign` | Gated multi-agent campaign: literature pool, target quantification, route cards, attacks, final audit, paper and Lean tracks | Pushing a bound, improving a constant, attacking a conjecture | [OctopusTide/claude-math-research-skill](https://github.com/OctopusTide/claude-math-research-skill) |
| `math-proof` | Writes clear detailed proofs for papers; expands sketches into full proofs | Proof for a paper | [flonat/flonat-research](https://github.com/flonat/flonat-research) |
| `math-reasoning` | Derivations, proofs, notation tables, statistical test selection in LaTeX | Math inside a research paper | [lingzhi227/agent-research-skills](https://github.com/lingzhi227/agent-research-skills) |
| `proof-writer` | Proof writing for theory papers | Theorem proofs in ML and theory papers | [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) |

## 2. Checking, refereeing and repairing proofs

| Skill | What it does | Use when | Source |
|---|---|---|---|
| `math-proof-review` | Rigorous correctness audit of theorems, lemmas and derivations in LaTeX papers | CHECK and FIX modes on a `.tex` proof | [XunZhiyang/math-proof-review](https://github.com/XunZhiyang/math-proof-review) |
| `verify-math` | Verifies a derivation or claim | A second opinion on an argument | [flonat/flonat-research](https://github.com/flonat/flonat-research) |
| `proof-checker` | Finds gaps in a LaTeX proof, fixes them with full derivations, re-reviews, writes an audit | Adversarial check of an existing proof | [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) |
| `proof-readability` | Makes proofs readable without changing their content | After a proof is correct | [flonat/flonat-research](https://github.com/flonat/flonat-research) |
| `proof-simplify` | Shortens and simplifies formal proofs | After a Lean proof works | [opum-ai/proof-skills](https://github.com/opum-ai/proof-skills) |

## 3. Lean 4 and formal verification

| Skill | What it does | Use when | Source |
|---|---|---|---|
| `lean4-theorem-proving` | Default Lean 4 and Mathlib workflow: build, fill sorries, search lemmas, fix errors, refute statements | Any `.lean` work | [cameronfreer/lean4-skills](https://github.com/cameronfreer/lean4-skills) |
| `lean-proving` | Write and plan Lean proofs and definitions, statement design | Proving a new theorem, stuck proof | [matt-w-horn/lean-skills](https://github.com/matt-w-horn/lean-skills) |
| `loogle` | Search Lean and Mathlib for a lemma by name, shape or conclusion | Before proving something from scratch | [matt-w-horn/lean-skills](https://github.com/matt-w-horn/lean-skills) |
| `lake` | Build, toolchain and Mathlib cache troubleshooting | Lean build problems | [matt-w-horn/lean-skills](https://github.com/matt-w-horn/lean-skills) |
| `lean-verification` | Checks that Lean work really proves what it claims (vacuity, junk values) | Auditing a formalization | [matt-w-horn/lean-skills](https://github.com/matt-w-horn/lean-skills) |
| `lean-claims-review` | Blinded docstring-versus-statement reviews | Large Lean libraries | [matt-w-horn/lean-skills](https://github.com/matt-w-horn/lean-skills) |
| `lean-refactoring` | Shorten and clean Lean proofs without changing statements | Cleanup passes | [matt-w-horn/lean-skills](https://github.com/matt-w-horn/lean-skills) |
| `lean-latex-sync` | Keep LaTeX and docstrings truthful to the Lean code | Paper plus formalization | [matt-w-horn/lean-skills](https://github.com/matt-w-horn/lean-skills) |
| `lean-check` | Formalize a self-authored lemma and require a clean build with no sorry | Machine-checking one lemma | [flonat/flonat-research](https://github.com/flonat/flonat-research) |
| `formalize-math-paper` | Formalize a whole paper in Lean 4, end to end, with audit report | A paper or numbered theorem list | [vltanh/formalize-math-paper](https://github.com/vltanh/formalize-math-paper) |
| `prove` | Five-phase Lean workflow: research, Loogle search, skeleton with sorries, fill, verify | Lean proof from a plain statement | [parcadei/Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3) |
| `lean-workflow` | Route Lean work through a repo's Mathlib and Lake conventions | Lean project hygiene | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `lean-search-discovery` | Find Mathlib declarations before proving | Lemma search | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `lean-proof-patterns` | Translate mathematical reasoning into maintainable tactics | Writing and refactoring proofs | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `lean-statement-audit` | Audit a frozen Lean declaration against its mathematical source | Before accepting a formal statement | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `lean-orchestrator` | Coordinate a large multi-agent formalization | Big formalization campaigns | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `lean-project-architecture` | Plan modules and stage a formalization | Starting a project | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `lean-learnings` | Reusable Lean and Mathlib lessons for analysis | Analysis formalizations | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `lean-naming-style` | Mathlib naming and docstring conventions | Before submitting Lean code | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `build-proof-dependency-graph` | Source-level dependency graph from LaTeX proofs to Lean declarations | Planning a paper formalization | [scottnarmstrong/LeanAutoformalizationSkills](https://github.com/scottnarmstrong/LeanAutoformalizationSkills) |
| `formal-math-ai` | Graduate analysis, formal verification and related notes | Graduate analysis questions, theorem prover surveys | [lonexreb/claude-code-math-skills](https://github.com/lonexreb/claude-code-math-skills) |
| `formal-verify`, `lean-model`, `tlaplus-model` | Model code in TLA+ or Lean and check it | Verifying software or protocols, not textbook math | [opum-ai/proof-skills](https://github.com/opum-ai/proof-skills) |

## 4. Calculus and symbolic computation

| Skill | What it does | Use when | Source |
|---|---|---|---|
| `sympy` | Symbolic algebra, calculus, equation solving, ODEs with SymPy | Any exact symbolic work; needs `pip install sympy` | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) |
| `umtymp-homework` | The user's own UMTYMP homework workflow | UMTYMP calculus and course sets | local |
| `umtymp-homework-feedback` | Feedback on UMTYMP homework | Checking a student attempt | local |

Calculus I to III is also covered by `math-skill`, the toolbox in `references/methods.md`, and `scripts/verify_identity.py` (derivatives, integrals including improper, sums, limits, identities).

## 5. Writing, typesetting and papers

| Skill | What it does | Use when | Source |
|---|---|---|---|
| `latex-math-writing` | Draft, edit and polish research-level mathematical LaTeX with complete proofs and rendered-page checks | WRITE mode for notes, papers, slides | [amelieloher/math-paper-skills](https://github.com/amelieloher/math-paper-skills) |
| `math-paper-campaign` | Whole-paper campaign with independent reviews, ledgers and phased polishing | A complete math paper | [amelieloher/math-paper-skills](https://github.com/amelieloher/math-paper-skills) |
| `math-figures` | TikZ figures, interactive figures and animations for math papers | Figures that express an idea | [amelieloher/math-paper-skills](https://github.com/amelieloher/math-paper-skills) |
| `visual-paper` | Visual companion websites and papers | Companion pages for a result | [amelieloher/math-paper-skills](https://github.com/amelieloher/math-paper-skills) |
| `read-research-paper` | Read a mathematical paper critically | Understanding a source paper | [haruhisa-enomoto/math-paper-skills](https://github.com/haruhisa-enomoto/math-paper-skills) |
| `write-research-paper` | Write a mathematics research paper | Drafting a paper | [haruhisa-enomoto/math-paper-skills](https://github.com/haruhisa-enomoto/math-paper-skills) |
| `polish-math-prose` | Rewrite AI-like mathematical prose into natural mathematical English | After the math is final | [haruhisa-enomoto/math-paper-skills](https://github.com/haruhisa-enomoto/math-paper-skills) |
| `coordinate-research-paper` | Multi-model relay: writer, isolated reviews, polish, audit | Automated paper relay | [haruhisa-enomoto/math-paper-skills](https://github.com/haruhisa-enomoto/math-paper-skills) |
| `math-latex` | Compilable LaTeX for theorems, proofs, algorithms, convergence analyses, Beamer | Typesetting applied math | [hameefy/claude-latex-skill](https://github.com/hameefy/claude-latex-skill) |
| `latex-guardian` | Protects verified derivations during edits; compile gate and structure checks | Editing a `.tex` proof safely | [foogtil/claude-code-math-skills](https://github.com/foogtil/claude-code-math-skills) |
| `latex-polish`, `latex-rescue`, `latex-fmt`, `pdf2tex` | LaTeX polish, repair, formatting, PDF to LaTeX | LaTeX trouble or conversion | see `/everythingpaper` catalog |
| `sentence-audit`, `deslop`, `humanizer-writing-skill`, `anti-defensive-writing`, `scientific-prose-style` | Sentence-level precision and removal of generated-text tells | Prose parts of a write-up, never the math | see `/everythingpaper` catalog |
| `abstract-writing`, `conclusion-writing` | Abstract and conclusion sections | Paper sections | see `/everythingpaper` catalog |

For a complete paper, hand the paper spine to `/everythingpaper` and use this skill as its proof engine.

## 6. Review, citations and literature

| Skill | What it does | Use when | Source |
|---|---|---|---|
| `paper-review` | Independent meta-review | Round 3 panel for a write-up | see `/everythingpaper` catalog |
| `academic-paper-reviewer` | Journal-style reviewer panel | Round 3 for a paper | see `/everythingpaper` catalog |
| `paperjury` | Venue-matched reviewer jury | CS-theory write-ups | [Spark-To-Paper-Skills/paperjury](https://github.com/Spark-To-Paper-Skills/paperjury) |
| `citation-verifier`, `alterlab-citation-verifier`, `crossref`, `reference-checker` | Confirm a citation exists and says what you claim | Any cited theorem or paper | see `/everythingpaper` catalog |
| `literature-search`, `paper-lookup`, `deep-research`, `novelty-assessment` | Find and check prior work | Is this known? what is the source? | see `/everythingpaper` catalog |
| `research-integrity` | Honest reporting rules | Any write-up | see `/everythingpaper` catalog |

## 7. Explaining and teaching

| Skill | What it does | Use when | Source |
|---|---|---|---|
| `pp-deep-explain` | Exhaustive reader-friendly explanation with notation decoding and worked examples | EXPLAIN a theorem or concept in depth | [panpanc/math-skills](https://github.com/panpanc/math-skills) |
| `pp-bottom-up` | Build a concept from elementary pieces, with motivation | "How could we invent this" | [panpanc/math-skills](https://github.com/panpanc/math-skills) |
| `pp-theorem` | Structured treatment of a theorem | Understanding a theorem and its proof | [panpanc/math-skills](https://github.com/panpanc/math-skills) |
| `pp-reinvent-from-scratch` | Rediscover a concept step by step | Deep understanding | [panpanc/math-skills](https://github.com/panpanc/math-skills) |
| `pp-connect-concepts` | Map links among several concepts | Studying a topic as a network | [panpanc/math-skills](https://github.com/panpanc/math-skills) |
| `pp-generalization-ladder` | Climb the generalizations of a concept | Seeing the big picture | [panpanc/math-skills](https://github.com/panpanc/math-skills) |
| `pp-mental-models` | Mental models behind a theorem | Learning to think like a mathematician | [panpanc/math-skills](https://github.com/panpanc/math-skills) |
| `pp-dependency-map` | Prerequisite DAG for a course or proof | Planning study or a proof structure | [panpanc/math-skills](https://github.com/panpanc/math-skills) |
| `pp-abstraction-levels`, `pp-motivate-learning`, `pp-term-origins`, `pp-field-mental-models` | Layered explanations, motivation, term origins, field models | Teaching and study | [panpanc/math-skills](https://github.com/panpanc/math-skills) |

## 8. Visuals, animation and slides

| Skill | What it does | Use when | Source |
|---|---|---|---|
| `manim-composer` | Plan an explainer video scene by scene | Before any Manim code | [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) |
| `manimce-best-practices` | Manim Community Edition scenes, MathTex, 3D | Math animation | [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) |
| `manimgl-best-practices` | 3Blue1Brown-style ManimGL | Interactive math animation | [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) |
| `beamer`, `beamer-academic`, `beamer-deck` | LaTeX Beamer decks | Math talks with equations | local and [flonat/flonat-research](https://github.com/flonat/flonat-research) |
| `academic-slides`, `thesis-defense-pptx`, `presenting-conference-talks` | Academic talk structure and decks | Seminars, defenses | local |
| `figure-creation`, `academic-plotting`, `scientific-figure-making`, `diagram-design` | Plots and diagrams | Graphs of functions, geometric figures, flowcharts | local |

For a full deck, call `/everythingslideshow`; for a video, `/everythingvideo`.

## 9. Other tools used by this skill

- `anthropic-skills:pdf`, `anthropic-skills:docx`: read a problem set or write a document.
- Scholarly search tools (`search_papers`, `get_paper`, `verify_reference`) when the connector is attached.
- `scripts/verify_identity.py`, `scripts/counterexample.py`: bundled numeric and exact checkers.
- Optional: SymPy (`pip install sympy`), a LaTeX engine (tectonic, latexmk or pdflatex), Lean 4 with Lake.

## Deliberately not routed to

- Skills that need an external CLI or service that is not installed, such as the `math-unified`, `math-router` and `math-help` skills of Continuous-Claude-v3 (they call a `scripts/cc_math` CLI from that repo). They are not copied here because they would fail and intercept math requests.
- Research-automation skills that submit or publish for you. Submitting and posting stay the user's call.

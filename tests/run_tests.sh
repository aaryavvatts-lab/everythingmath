#!/usr/bin/env bash
# Regression tests for the bundled checkers. Run: bash tests/run_tests.sh
# Each case states the exit code the checker must return, so a checker that stops catching
# seeded errors fails here.
here="$(cd "$(dirname "$0")/.." && pwd)"
S="$here/scripts"
tmp="$(mktemp -d "${TMPDIR:-/tmp}/emtests.XXXXXX")"
pass=0; fail=0
t() { # t "name" expected_rc command...
  local name="$1" want="$2"; shift 2
  out="$("$@" 2>&1)"; rc=$?
  if [ "$rc" -eq "$want" ]; then pass=$((pass+1)); echo "ok    $name"
  else fail=$((fail+1)); echo "FAIL  $name (rc=$rc, wanted $want)"; echo "$out" | sed 's/^/        /' | head -8; fi
}
v() { python3 "$S/verify_identity.py" "$@"; }
c() { python3 "$S/counterexample.py" "$@"; }

t "true identity passes"            0 v eq "sin(x)**2+cos(x)**2" "1" --vars x:-5:5
t "false identity is caught"        1 v eq "(x+1)**2" "x**2+1" --vars x:-5:5
t "true inequality passes"          0 v ineq "x**2+1 >= 2*x" --vars x:-10:10
t "false inequality is caught"      1 v ineq "x**2 >= x" --vars x:-1:1
t "correct derivative passes"       0 v deriv "x**3*sin(x)" "3*x**2*sin(x)+x**3*cos(x)" --var x --range 0.1:3
t "wrong derivative is caught"      1 v deriv "x**3*sin(x)" "3*x**2*sin(x)" --var x --range 0.1:3
t "improper integral matches"       0 v integral "x*exp(-x)" x 0 inf 1
t "gaussian over the real line"     0 v integral "exp(-x**2)" x -inf inf "sqrt(pi)"
t "wrong integral value is caught"  1 v integral "sin(x)" x 0 pi 3
t "closed form of sum of squares"   0 v sum "k**2" k 1 n "n*(n+1)*(2*n+1)/6" --nrange 1:60
t "wrong closed form is caught"     1 v sum "k**2" k 1 n "n*(n+1)/2" --nrange 1:60
t "sin(x)/x limit"                  0 v limit "sin(x)/x" x 0 1
t "wrong limit is caught"           1 v limit "sin(x)/x" x 0 2
t "limit at infinity"               0 v limit "(1+1/x)**x" x inf "e"
t "Euler polynomial fails at 40"    1 c "is_prime(n**2+n+41)" --vars n:0:100
t "sum of two squares mod 4"        0 c "(a*a+b*b) % 4 != 3" --vars a:0:100,b:0:100
t "witness search finds a square"   1 c "n % 7 == 2 and is_square(n)" --vars n:1:1000 --exists
t "unsafe code is refused"          2 v eq "__import__('os').system('echo hi')" "1" --vars x:0:1
t "all-undefined is inconclusive"   2 c "9**9**9 > 0" --vars n:0:1

cat >"$tmp/bad.md" <<'EOF'
# Problem
Prove that for all n, 1+2+...+n = n(n+1)/2.

## Solution
Clearly the formula holds. By induction.
Case 1: n is even. Obviously true.
[GAP: odd case]
So the formula follows. $x = 1
EOF
cat >"$tmp/good.md" <<'EOF'
# Problem
Prove that for all integers n >= 1, 1+2+...+n = n(n+1)/2.

## Solution
We use induction on n. Base case: for n = 1 both sides equal 1.
Inductive step: assume the formula holds for n = m. Then 1+...+m+(m+1) = m(m+1)/2 + (m+1) = (m+1)(m+2)/2,
which is the formula for n = m+1. By induction the formula holds for all n >= 1. QED
EOF
t "bad proof fails the lint"        1 python3 "$S/proof_lint.py" "$tmp/bad.md"
t "good proof passes the lint"      0 python3 "$S/proof_lint.py" "$tmp/good.md"

python3 "$S/step_review.py" "$tmp/good.md" --out "$tmp/qc" >/dev/null
t "unread steps block the gate"     1 python3 "$S/issue_register.py" "$tmp/qc/issues.md" --gate
sed -i.bak 's/- \[ \]/- [x]/' "$tmp/qc/issues.md"
t "all steps read passes the gate"  0 python3 "$S/issue_register.py" "$tmp/qc/issues.md" --gate
printf '\n## M001 | MAJOR | open\nLocation: S002\nProblem: gap\n' >>"$tmp/qc/issues.md"
sed -i.bak 's/^## Coverage/## Coverage/' "$tmp/qc/issues.md"
t "open MAJOR blocks the gate"      1 python3 "$S/issue_register.py" "$tmp/qc/issues.md" --gate

printf '| ID | Status | Requirement |\n|--|--|--|\n| R1 | PASS | answer is 5 |\n| R2 | OPEN | cites source |\n' >"$tmp/l.md"
t "open ledger line is not done"    1 python3 "$S/ledger_check.py" "$tmp/l.md"
printf '| ID | Status | Requirement |\n|--|--|--|\n| R1 | PASS | answer is 5 |\n| R2 | BLOCKED | needs user |\n' >"$tmp/l2.md"
t "blocked is allowed"              0 python3 "$S/ledger_check.py" "$tmp/l2.md"

t "check_skills runs"               0 bash "$S/check_skills.sh" --missing --tools

rm -rf "$tmp"
echo; echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]

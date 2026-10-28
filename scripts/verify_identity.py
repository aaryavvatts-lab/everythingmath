#!/usr/bin/env python3
"""Numerical and exact checks for claimed math facts (standard library only).

A passing check is evidence, never proof: it can refute a claim or raise confidence, nothing more.

  verify_identity.py eq    "sin(x)**2+cos(x)**2" "1" --vars x:-5:5
  verify_identity.py ineq  "x**2+1 >= 2*x" --vars x:-10:10
  verify_identity.py deriv "x**3*sin(x)" "3*x**2*sin(x)+x**3*cos(x)" --var x --range 0.1:3
  verify_identity.py deriv "x/(x**2+y**2)" "(y**2-x**2)/(x**2+y**2)**2" --var x --range 0.5:3 --others y:0.5:3
      (partial derivative of a function of two variables; use it twice to check Q_x = P_y for a curl)
  verify_identity.py integral "x*exp(-x)" x 0 inf "1"
  verify_identity.py sum   "k**2" k 1 n "n*(n+1)*(2*n+1)/6" --nrange 1:60      (exact rational arithmetic)
  verify_identity.py sum   "sin(k)" k 1 n "(cos(1/2)-cos(n+1/2))/(2*sin(1/2))" --float   (trig, exp, log terms)
  verify_identity.py limit "sin(x)/x" x 0 1

Expressions use Python syntax: ** or ^ for powers, explicit * for products, functions such as
sin cos tan exp log sqrt gamma erf, constants pi e inf. Exit code 0 = no problem found,
1 = a counterexample or mismatch, 2 = could not test (bad input or too few defined points).
"""
import argparse
import math
import os
import re
import signal
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _safe import UNDEFINED, close, parse, parse_vars, sample_points, used_names  # noqa: E402


def _warn_unused(ranges, *exprs):
    seen = set()
    for e in exprs:
        seen |= used_names(e)
    unused = [v for v in ranges if v not in seen]
    if unused and len(unused) == len(ranges):
        print("WARNING: none of the variables (%s) appear in the expressions, so this tests a constant. "
              "For exact integer identities use the sum command or counterexample.py." % ", ".join(unused))
    elif unused:
        print("WARNING: variable(s) %s do not appear in the expressions" % ", ".join(unused))


def _bad(x):
    return isinstance(x, complex) or x != x or x in (math.inf, -math.inf)


def _fixed(spec):
    out = {}
    for part in (spec or "").split(","):
        if part.strip():
            k, v = part.split("=")
            out[k.strip()] = float(v)
    return out


def cmd_eq(a):
    ranges = parse_vars(a.vars)
    fixed = _fixed(a.fix)
    names = set(ranges) | set(fixed)
    f, g = parse(a.lhs, names), parse(a.rhs, names)
    _warn_unused(ranges, a.lhs, a.rhs)
    tested = skipped = 0
    fails, worst = [], 0.0
    for p in sample_points(ranges, a.n, a.seed):
        p.update(fixed)
        try:
            x, y = f(p), g(p)
        except UNDEFINED:
            skipped += 1
            continue
        if _bad(x) or _bad(y):
            skipped += 1
            continue
        tested += 1
        err = abs(x - y) / max(1.0, abs(x), abs(y))
        worst = max(worst, err)
        if not close(x, y, a.tol):
            fails.append((p, x, y))
    return _verdict_eq(a, tested, skipped, fails, worst)


def _verdict_eq(a, tested, skipped, fails, worst):
    print("tested %d points (%d undefined or skipped), worst relative error %.3g" % (tested, skipped, worst))
    if fails:
        print("MISMATCH at %d points. First ones:" % len(fails))
        for p, x, y in fails[:3]:
            print("  at %s: lhs = %.12g, rhs = %.12g" % (_fmt(p), x, y))
        return 1
    if tested < max(5, a.n // 10):
        print("INCONCLUSIVE: too few defined points. Check the domain in --vars.")
        return 2
    print("NO COUNTEREXAMPLE FOUND (numerical evidence only, not a proof)")
    return 0


def _fmt(p):
    return ", ".join("%s=%.6g" % (k, v) for k, v in p.items())


def cmd_ineq(a):
    m = re.split(r"(<=|>=|<|>)", a.statement)
    if len(m) != 3:
        print("statement needs exactly one of <, <=, >, >= (got %r)" % a.statement)
        return 2
    left, op, right = m[0], m[1], m[2]
    ranges = parse_vars(a.vars)
    fixed = _fixed(a.fix)
    names = set(ranges) | set(fixed)
    f, g = parse(left, names), parse(right, names)
    _warn_unused(ranges, left, right)
    tested = skipped = 0
    viol = []
    tight = (math.inf, None)
    for p in sample_points(ranges, a.n, a.seed):
        p.update(fixed)
        try:
            x, y = f(p), g(p)
        except UNDEFINED:
            skipped += 1
            continue
        if _bad(x) or _bad(y):
            skipped += 1
            continue
        tested += 1
        margin = (y - x) if op in ("<", "<=") else (x - y)
        scale = max(1.0, abs(x), abs(y))
        strict = op in ("<", ">")
        if (margin < -a.tol * scale) or (strict and margin <= 0 and abs(margin) > a.tol * scale):
            viol.append((p, x, y))
        if margin / scale < tight[0]:
            tight = (margin / scale, p)
    print("tested %d points (%d skipped). Tightest relative margin %.3g at %s" % (
        tested, skipped, tight[0], _fmt(tight[1]) if tight[1] else "n/a"))
    if viol:
        print("VIOLATED at %d points. First ones:" % len(viol))
        for p, x, y in viol[:3]:
            print("  at %s: lhs = %.12g, rhs = %.12g" % (_fmt(p), x, y))
        return 1
    if tested < max(5, a.n // 10):
        print("INCONCLUSIVE: too few defined points.")
        return 2
    print("NO COUNTEREXAMPLE FOUND (numerical evidence only). A tight margin near 0 marks the "
          "equality case your proof must treat separately.")
    return 0


def _deriv(f, env, var, x):
    h = 1e-3 * max(1.0, abs(x))

    def d(hh):
        e1, e2 = dict(env), dict(env)
        e1[var], e2[var] = x + hh, x - hh
        return (f(e1) - f(e2)) / (2 * hh)
    return (4 * d(h / 2) - d(h)) / 3


def cmd_deriv(a):
    lo, hi = [float(t) for t in a.range.split(":")]
    fixed = _fixed(a.fix)
    others = parse_vars(a.others) if a.others else {}
    names = {a.var} | set(fixed) | set(others)
    f, claim = parse(a.expr, names), parse(a.derivative, names)
    tested = skipped = 0
    fails, worst = [], 0.0
    ranges = {a.var: (lo, hi)}
    ranges.update(others)
    for p in sample_points(ranges, a.n, a.seed):
        env = dict(fixed)
        env.update({k: v for k, v in p.items() if k != a.var})
        x = p[a.var]
        try:
            num = _deriv(f, env, a.var, x)
            env[a.var] = x
            val = claim(env)
        except UNDEFINED:
            skipped += 1
            continue
        if _bad(num) or _bad(val):
            skipped += 1
            continue
        tested += 1
        worst = max(worst, abs(num - val) / max(1.0, abs(num), abs(val)))
        if not close(num, val, a.tol):
            fails.append((dict(p), num, val))
    print("compared numerical d/d%s with the claimed derivative at %d points" % (a.var, tested))
    return _verdict_eq(argparse.Namespace(n=a.n, tol=a.tol), tested, skipped, fails, worst)


# Gauss-Legendre nodes on [-1, 1], computed with Newton's method.
def _gl(n):
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-15:
                break
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def _integrate(h, a, b, panels, order=24):
    xs, ws = _gl(order)
    total = 0.0
    width = (b - a) / panels
    for i in range(panels):
        c = a + (i + 0.5) * width
        for x, w in zip(xs, ws):
            total += w * h(c + 0.5 * width * x) * 0.5 * width
    return total


def cmd_integral(a):
    env0 = {}
    lo = parse(a.lower, set())(env0)
    hi = parse(a.upper, set())(env0)
    fixed = _fixed(a.fix)
    names = {a.var} | set(fixed)
    f = parse(a.expr, names)

    def raw(x):
        e = dict(fixed)
        e[a.var] = x
        return f(e)

    if lo == -math.inf and hi == math.inf:
        def h(t):
            x = t / (1 - t * t)
            return raw(x) * (1 + t * t) / (1 - t * t) ** 2
        a_, b_ = -1.0, 1.0
    elif hi == math.inf:
        def h(t):
            return raw(lo + t / (1 - t)) / (1 - t) ** 2
        a_, b_ = 0.0, 1.0
    elif lo == -math.inf:
        def h(t):
            return raw(hi - t / (1 - t)) / (1 - t) ** 2
        a_, b_ = 0.0, 1.0
    else:
        h, a_, b_ = raw, lo, hi
    try:
        v1 = _integrate(h, a_, b_, 32)
        v2 = _integrate(h, a_, b_, 64)
    except UNDEFINED as exc:
        print("could not evaluate the integrand: %s" % exc)
        return 2
    if _bad(v1) or _bad(v2):
        print("integrand blew up inside the interval: divergent or badly singular")
        return 2
    print("integral = %.12g (two resolutions differ by %.2g)" % (v2, abs(v2 - v1)))
    if abs(v2 - v1) > 1e-6 * max(1.0, abs(v2)):
        print("WARNING: resolutions disagree. The integral may diverge or have a hard singularity.")
    if a.claimed is None:
        return 0
    claim = parse(a.claimed, set())(env0)
    if close(v2, claim, a.tol):
        print("MATCHES claimed value %.12g (numerical evidence only)" % claim)
        return 0
    print("MISMATCH: claimed %.12g, numerical %.12g" % (claim, v2))
    return 1


def cmd_sum(a):
    lo_s, hi_s = a.nrange.split(":")
    mode = "float" if a.float else "exact"
    num = float if a.float else Fraction
    names = {a.idx, a.param}
    try:
        term = parse(a.expr, names, mode)
        lo_f, hi_f = parse(a.lower, {a.param}, mode), parse(a.upper, {a.param}, mode)
        closed = parse(a.closed, {a.param}, mode)
    except ValueError as exc:
        if not a.float:
            raise ValueError("%s. Exact mode supports rational arithmetic only (+ - * / ** and abs, min, max, "
                             "floor, ceil, binom, factorial, gcd). For trig, exp, log or sqrt terms add --float." % exc)
        raise
    checked = 0
    for n in range(int(lo_s), int(hi_s) + 1):
        env = {a.param: num(n)}
        lo, hi = int(lo_f(env)), int(hi_f(env))
        total = num(0)
        for k in range(lo, hi + 1):
            env[a.idx] = num(k)
            total += term(env)
        want = closed({a.param: num(n)})
        checked += 1
        if (not close(total, want, a.tol)) if a.float else (total != want):
            print("MISMATCH at %s=%d: sum = %s, closed form = %s" % (a.param, n, total, want))
            return 1
    print(("AGREEMENT to %g for %s = %s..%s (%d cases, floating point)" % (a.tol, a.param, lo_s, hi_s, checked)
           if a.float else
           "EXACT AGREEMENT for %s = %s..%s (%d cases, rational arithmetic)" % (a.param, lo_s, hi_s, checked))
          + ". Finite evidence; prove it by induction or telescoping.")
    return 0


def cmd_limit(a):
    point = parse(a.point, set())({})
    f = parse(a.expr, {a.var})
    vals = []
    for k in range(1, 8):
        row = {}
        for side, sgn in (("right", 1), ("left", -1)):
            if a.side not in ("both", side) or (side == "left" and point in (math.inf, -math.inf)):
                continue
            if point in (math.inf, -math.inf):
                x = (10.0 ** k) * (1 if point > 0 else -1)
            else:
                x = point + sgn * 10.0 ** (-k)
            try:
                v = f({a.var: x})
            except UNDEFINED:
                v = float("nan")
            row[side] = v
        vals.append((k, row))
    print("k   " + "   ".join("%-18s" % s for s in vals[0][1]))
    for k, row in vals:
        print("%d   " % k + "   ".join("%-18.12g" % v for v in row.values()))
    ests = {}
    for side in vals[0][1]:
        seq = [(k, row[side]) for k, row in vals if not _bad(row[side])]
        if len(seq) < 3:
            ests[side] = None
            continue
        best = min(range(1, len(seq)), key=lambda i: abs(seq[i][1] - seq[i - 1][1]))
        ests[side] = seq[best][1]
    print("estimates: " + ", ".join("%s -> %s" % (s, "none" if v is None else "%.8g" % v) for s, v in ests.items()))
    if a.claimed is None:
        return 0
    claim = parse(a.claimed, set())({})
    if any(v is None or not close(v, claim, a.tol) for v in ests.values()):
        print("MISMATCH or no convergence versus claimed %.8g (check one-sided limits, oscillation, blow-up)" % claim)
        return 1
    print("CONSISTENT with claimed limit %.8g (numerical evidence only)" % claim)
    return 0


def _protect_negatives(argv):
    """argparse treats -inf or -x**2 as options; wrap such expression arguments in parentheses."""
    out = []
    for t in argv:
        if t == "-h" or t.startswith("--"):
            out.append(t)
        elif t.startswith("-") and len(t) > 1 and not re.fullmatch(r"-\d+(\.\d*)?|-\.\d+", t):
            out.append("(" + t + ")")
        else:
            out.append(t)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--timeout", type=int, default=60)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, tol=1e-9):
        p.add_argument("--n", type=int, default=400)
        p.add_argument("--tol", type=float, default=tol)
        p.add_argument("--seed", type=int, default=1)
        p.add_argument("--fix", default="", help="fixed parameters, e.g. a=2,b=3")

    p = sub.add_parser("eq"); p.add_argument("lhs"); p.add_argument("rhs"); p.add_argument("--vars", required=True); common(p)
    p = sub.add_parser("ineq"); p.add_argument("statement"); p.add_argument("--vars", required=True); common(p)
    p = sub.add_parser("deriv"); p.add_argument("expr"); p.add_argument("derivative")
    p.add_argument("--var", default="x"); p.add_argument("--range", default="0.1:3")
    p.add_argument("--others", default="", help="ranges for the other variables, e.g. y:0.5:3 (partial derivatives, curl checks)")
    common(p, 1e-6)
    p = sub.add_parser("integral"); p.add_argument("expr"); p.add_argument("var"); p.add_argument("lower")
    p.add_argument("upper"); p.add_argument("claimed", nargs="?"); p.add_argument("--tol", type=float, default=1e-8)
    p.add_argument("--fix", default="")
    p = sub.add_parser("sum"); p.add_argument("expr"); p.add_argument("idx"); p.add_argument("lower")
    p.add_argument("upper"); p.add_argument("closed"); p.add_argument("--param", default="n"); p.add_argument("--nrange", default="1:40")
    p.add_argument("--float", action="store_true", help="floating point, allows sin, exp, log, sqrt in the terms")
    p.add_argument("--tol", type=float, default=1e-9)
    p = sub.add_parser("limit"); p.add_argument("expr"); p.add_argument("var"); p.add_argument("point")
    p.add_argument("claimed", nargs="?"); p.add_argument("--side", choices=["both", "left", "right"], default="both")
    p.add_argument("--tol", type=float, default=1e-3)
    a = ap.parse_args(_protect_negatives(sys.argv[1:]))
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, lambda *_: (print("TIMEOUT"), sys.exit(2)))
        signal.alarm(a.timeout)
    try:
        sys.exit({"eq": cmd_eq, "ineq": cmd_ineq, "deriv": cmd_deriv, "integral": cmd_integral,
                  "sum": cmd_sum, "limit": cmd_limit}[a.cmd](a))
    except ValueError as exc:
        print("input error: %s" % exc)
        sys.exit(2)


if __name__ == "__main__":
    main()

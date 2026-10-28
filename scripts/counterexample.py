#!/usr/bin/env python3
"""Brute-force search for counterexamples (or witnesses) over integers. Standard library only.

  counterexample.py "n**2 + n + 41 is_prime" ...   (write a boolean expression instead:)
  counterexample.py "is_prime(n**2 + n + 41)" --vars n:0:100
  counterexample.py "(a*a + b*b) % 4 != 3" --vars a:0:200,b:0:200
  counterexample.py "n % 7 == 3 and is_square(n)" --vars n:1:100000 --exists

By default the statement must hold for every integer point (forall); the script prints the points where
it fails. With --exists it prints witnesses where it holds. Finding nothing is NOT a proof.
Use // and % for integer division. Helpers: is_prime is_square gcd lcm isqrt comb factorial tau sigma phi digsum.
Exit code 0 = nothing found against the claim, 1 = counterexample (or witness) found, 2 = input error.
"""
import argparse
import itertools
import os
import signal
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _safe import UNDEFINED, parse  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("statement")
    ap.add_argument("--vars", required=True, help="integer ranges, inclusive: n:1:1000 or a:1:50,b:1:50")
    ap.add_argument("--exists", action="store_true", help="look for witnesses instead of counterexamples")
    ap.add_argument("--max", type=int, default=5, help="how many hits to print")
    ap.add_argument("--limit", type=int, default=5_000_000, help="refuse to evaluate more points than this")
    ap.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args()
    ranges = {}
    try:
        for part in a.vars.split(","):
            nm, lo, hi = part.split(":")
            ranges[nm.strip()] = range(int(lo), int(hi) + 1)
        f = parse(a.statement, set(ranges), "int")
    except ValueError as exc:
        print("input error: %s" % exc)
        return 2
    total = 1
    for r in ranges.values():
        total *= len(r)
    if total > a.limit:
        print("search space has %d points, over --limit %d. Shrink the ranges or raise --limit." % (total, a.limit))
        return 2
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, lambda *_: (print("TIMEOUT before finishing the range"), sys.exit(2)))
        signal.alarm(a.timeout)
    names = list(ranges)
    hits, errors, checked, last = [], 0, 0, None
    for combo in itertools.product(*ranges.values()):
        last = combo
        env = dict(zip(names, combo))
        try:
            ok = bool(f(env))
        except UNDEFINED:
            errors += 1
            continue
        checked += 1
        if ok == a.exists:
            hits.append(combo)
            if len(hits) >= a.max:
                break
    label = "witnesses" if a.exists else "counterexamples"
    if checked == 0:
        print("INCONCLUSIVE: the statement was undefined at all %d points (division by zero, overflow or a "
              "bad domain). Fix the statement or the ranges." % errors)
        return 2
    if hits:
        stopped = len(hits) >= a.max
        print("FOUND %s (%d shown; %s):" % (
            label, len(hits),
            "search stopped at --max after reaching %s, so there may be more" % ", ".join(
                "%s=%d" % (k, v) for k, v in zip(names, last)) if stopped
            else "the whole range was searched, these are all of them"))
        for h in hits:
            print("  " + ", ".join("%s=%d" % (k, v) for k, v in zip(names, h)))
        return 1
    print("no %s among %d points (%d undefined). This is evidence, not a proof." % (label, checked, errors))
    return 0


if __name__ == "__main__":
    sys.exit(main())

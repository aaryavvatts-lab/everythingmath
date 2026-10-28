#!/usr/bin/env python3
"""Grade the Requirements Ledger. Standard library only.

  ledger_check.py ledger.md

Reads table rows whose first cell is R1, R2, ... and whose Status cell is OPEN, PASS, FAIL or BLOCKED.
Exit 1 while anything is OPEN or FAIL. BLOCKED is allowed but listed, since it needs the user.
"""
import re
import sys


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    try:
        text = open(sys.argv[1], encoding="utf-8").read()
    except OSError as exc:
        print("cannot read %s: %s" % (sys.argv[1], exc))
        return 2
    rows = []
    for line in text.split("\n"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 3 and re.fullmatch(r"R\d+", cells[0]):
            status = next((c.upper() for c in cells[1:] if c.upper() in ("OPEN", "PASS", "FAIL", "BLOCKED")), None)
            rows.append((cells[0], status, cells[2] if len(cells) > 2 else ""))
    if not rows:
        print("no ledger rows found (expected a table whose first cell is R1, R2, ...)")
        return 2
    tally = {}
    for rid, st, req in rows:
        tally[st] = tally.get(st, 0) + 1
        if st != "PASS":
            print("%-4s %-8s %s" % (rid, st or "NO-STATUS", req[:80]))
    print("ledger: %d requirements; " % len(rows) + ", ".join("%d %s" % (v, k) for k, v in sorted(tally.items(), key=str)))
    bad = [r for r in rows if r[1] in ("OPEN", "FAIL", None)]
    if bad:
        print("LEDGER: NOT DONE")
        return 1
    print("LEDGER: DONE" + (" (some BLOCKED, tell the user)" if tally.get("BLOCKED") else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

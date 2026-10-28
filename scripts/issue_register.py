#!/usr/bin/env python3
"""Summarise issues.md and gate on open serious issues. Standard library only.

  issue_register.py qc/review/issues.md --gate

--gate exits 1 while any FATAL or MAJOR issue is `open`, while any Coverage step is unticked, or while a
ticked step has no note (tick steps with: step_review.py FILE --out DIR --tick S001-S009 --note "what you checked").
A blocked FATAL or MAJOR does not fail the gate but is printed, because it needs the user.
"""
import argparse
import re
import sys

BLOCK = re.compile(r"^## (\w+) \| (FATAL|MAJOR|MINOR|NIT) \| (open|fixed|blocked|out-of-scope)\s*$", re.M)
COV = re.compile(r"^- \[( |x)\] (S\d+) \([0-9a-f]{8}\)(.*)$", re.M)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--gate", action="store_true")
    a = ap.parse_args()
    try:
        text = open(a.file, encoding="utf-8").read()
    except OSError as exc:
        print("cannot read %s: %s" % (a.file, exc))
        return 2
    counts = {}
    openserious, blocked = [], []
    for iid, sev, status in BLOCK.findall(text):
        counts[(sev, status)] = counts.get((sev, status), 0) + 1
        if sev in ("FATAL", "MAJOR") and status == "open":
            openserious.append(iid)
        if sev in ("FATAL", "MAJOR") and status == "blocked":
            blocked.append(iid)
    for sev in ("FATAL", "MAJOR", "MINOR", "NIT"):
        row = ", ".join("%d %s" % (counts[(sev, s)], s) for s in ("open", "fixed", "blocked", "out-of-scope") if (sev, s) in counts)
        print("%-6s %s" % (sev, row or "none"))
    cov = COV.findall(text)
    unread = [sid for box, sid, _ in cov if box == " "]
    nonote = [sid for box, sid, rest in cov if box == "x" and not re.search(r" :: .{8,}", rest)]
    print("coverage: %d of %d steps reviewed" % (len(cov) - len(unread), len(cov)))
    if blocked:
        print("BLOCKED serious issues (need the user): " + ", ".join(blocked))
    if not a.gate:
        return 0
    if not cov:
        print("GATE: FAIL, no Coverage section (run step_review.py first)")
        return 1
    if openserious:
        print("GATE: FAIL, open FATAL/MAJOR: " + ", ".join(openserious))
        return 1
    if unread:
        print("GATE: FAIL, unreviewed steps: " + ", ".join(unread[:10]) + (" ..." if len(unread) > 10 else ""))
        return 1
    if nonote:
        print("GATE: FAIL, ticked without a note (use step_review.py --tick ... --note): " + ", ".join(nonote[:10]))
        return 1
    print("GATE: PASS (the read is complete and nothing fixable is open; this is not a promise the math is right)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

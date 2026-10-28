#!/usr/bin/env python3
"""Split a solution into numbered steps for the line-by-line referee read. Standard library only.

  step_review.py solution.md --out qc/review/

Writes qc/review/steps.md (every step with an ID such as S012 and the section it is in) and
qc/review/issues.md with a Coverage checklist. Re-running after edits keeps your issue blocks and
your ticked boxes for steps whose text did not change, and un-ticks steps that changed.
"""
import argparse
import hashlib
import os
import re
import sys

HEAD = re.compile(r"^(#{1,6}\s|\\(sub)*section\*?\{|\\begin\{(theorem|lemma|proof|claim|proposition)\})", re.I)


def split_steps(text):
    steps, buf, section = [], [], ""
    in_math = False

    def flush():
        if buf:
            steps.append((section, "\n".join(buf).strip()))
            buf.clear()

    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("$$") or s.startswith("\\["):
            in_math = not in_math or (s.count("$$") == 2)
        if not s and not in_math:
            flush()
            continue
        if HEAD.match(s):
            flush()
            section = s.lstrip("# ").strip()[:70]
            continue
        if re.match(r"^(\d+[.)]|[-*]\s|Step\s+\d+|Case\s+\d+)", s) and buf:
            flush()
        buf.append(line)
    flush()
    return [(sec, body) for sec, body in steps if body]


def digest(body):
    return hashlib.sha1(re.sub(r"\s+", " ", body).encode()).hexdigest()[:8]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--out", default="qc/review")
    a = ap.parse_args()
    text = open(a.file, encoding="utf-8").read()
    steps = split_steps(text)
    os.makedirs(a.out, exist_ok=True)
    issues_path = os.path.join(a.out, "issues.md")
    old = open(issues_path, encoding="utf-8").read() if os.path.exists(issues_path) else ""
    ticked = dict(re.findall(r"- \[x\] (S\d+) \(([0-9a-f]{8})\)", old))
    blocks = re.findall(r"(^## \w+ \| (?:FATAL|MAJOR|MINOR|NIT) \|.*?)(?=^## |\Z)", old, re.S | re.M)
    with open(os.path.join(a.out, "steps.md"), "w", encoding="utf-8") as fh:
        fh.write("# Steps of %s\n\nReview each step with the test in references/checks.md.\n\n" % os.path.basename(a.file))
        for i, (sec, body) in enumerate(steps, 1):
            fh.write("### S%03d  [%s]\n%s\n\n" % (i, sec or "top", body))
    cover, changed = [], 0
    for i, (sec, body) in enumerate(steps, 1):
        sid, h = "S%03d" % i, digest(body)
        done = ticked.get(sid) == h
        changed += 0 if done or sid not in ticked else 1
        cover.append("- [%s] %s (%s) %s" % ("x" if done else " ", sid, h, (sec or "top")))
    with open(issues_path, "w", encoding="utf-8") as fh:
        fh.write("# Issues\n\nBlock format (one per issue):\n\n"
                 "    ## M001 | MAJOR | open\n    Location: S012\n    Quote: ...\n    Problem: ...\n    Fix: ...\n\n"
                 "Severity: FATAL (answer or proof wrong), MAJOR (gap a referee would reject), MINOR, NIT.\n"
                 "Status: open, fixed, blocked, out-of-scope.\n\n")
        for b in blocks:
            fh.write(b.rstrip() + "\n\n")
        fh.write("## Coverage\n\nTick a step only after reading it against the test.\n\n" + "\n".join(cover) + "\n")
    print("%d steps written to %s (%d previously reviewed steps changed and were un-ticked)" % (
        len(steps), a.out, changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())

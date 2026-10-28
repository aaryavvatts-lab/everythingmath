#!/usr/bin/env python3
"""Split a solution into numbered steps for the referee read, and record what was read. Standard library only.

  step_review.py solution.md --out qc/review/                      # (re)build steps.md and issues.md
  step_review.py solution.md --out qc/review/ --tick S003,S005-S008 --note "hypotheses of EVT checked"

A step is a paragraph, a bold **Step N.** or **Case N.** block (also when it starts mid-paragraph), a list
item, a lemma/claim block, or up to 10 rows of a table. Headings start a new section.

Writes qc/review/steps.md (every step with its ID and section) and qc/review/issues.md with a Coverage
checklist. Re-running after edits keeps your issue blocks and ticks for steps whose text did not change, and
un-ticks steps that changed. Loop: edit -> rebuild -> re-read the un-ticked steps -> tick with a note -> gate.
A tick needs a note of at least 8 characters saying what you checked; issue_register.py --gate refuses
ticks without one. The note is an honour-system record: it cannot prove you read the step, but it makes
rubber-stamping an explicit false statement.
"""
import argparse
import hashlib
import os
import re
import sys

HEAD = re.compile(r"^(#{1,6}\s|\\(sub)*section\*?\{|\\begin\{(theorem|lemma|proof|claim|proposition)\})", re.I)
LABEL = re.compile(r"^\s*(\*\*|__)?(Step|Case|Lemma|Claim|Part|Proposition|Theorem|Corollary)\b", re.I)
INLINE = re.compile(r"(?<=[^\n])[ \t]*(?=(?:\*\*|__)(?:Step|Case)\s+\d+[.:])")
LIST = re.compile(r"^(\d+[.)]|[-*]\s)")
COV = re.compile(r"^- \[( |x)\] (S\d+) \(([0-9a-f]{8})\)(.*)$")
TABLE_CHUNK = 10


def split_steps(text):
    text = INLINE.sub("\n", text)
    steps, buf, tbl = [], [], []
    state = {"section": "", "math": False}

    def flush():
        if buf:
            steps.append((state["section"], "\n".join(buf).strip()))
            buf.clear()

    def flush_table():
        for i in range(0, len(tbl), TABLE_CHUNK):
            steps.append((state["section"], "\n".join(tbl[i:i + TABLE_CHUNK])))
        tbl.clear()

    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("|"):
            flush()
            tbl.append(line)
            continue
        if tbl:
            flush_table()
        if s.startswith("$$") or s.startswith("\\["):
            state["math"] = (not state["math"]) or (s.count("$$") == 2)
        if not s and not state["math"]:
            flush()
            continue
        if HEAD.match(s):
            flush()
            state["section"] = s.lstrip("# ").strip()[:70]
            continue
        if (LIST.match(s) or LABEL.match(s)) and buf:
            flush()
        buf.append(line)
    flush()
    flush_table()
    return [(sec, body) for sec, body in steps if body.strip()]


def digest(body):
    return hashlib.sha1(re.sub(r"\s+", " ", body).encode()).hexdigest()[:8]


def parse_cov(text):
    out = {}
    for line in text.split("\n"):
        m = COV.match(line)
        if m:
            note = m.group(4).split(" :: ", 1)[1].strip() if " :: " in m.group(4) else ""
            out[m.group(2)] = (m.group(1) == "x", m.group(3), note)
    return out


def expand(spec, known):
    ids = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if part.lower() == "all":
            return list(known)
        m = re.fullmatch(r"S(\d+)-S?(\d+)", part)
        if m:
            ids += ["S%03d" % i for i in range(int(m.group(1)), int(m.group(2)) + 1)]
        else:
            ids.append("S%03d" % int(part.lstrip("S")))
    return ids


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--out", default="qc/review")
    ap.add_argument("--tick", help="steps you have read: S003,S005-S008 or all (needs --note)")
    ap.add_argument("--note", default="", help="what you checked (at least 8 characters)")
    a = ap.parse_args()
    issues_path = os.path.join(a.out, "issues.md")

    if a.tick:
        if len(a.note.strip()) < 8:
            print("--tick needs --note saying what you checked (at least 8 characters)")
            return 2
        if not os.path.exists(issues_path):
            print("no %s yet: run step_review.py without --tick first" % issues_path)
            return 2
        text = open(issues_path, encoding="utf-8").read()
        cov = parse_cov(text)
        ids = expand(a.tick, cov)
        missing = [i for i in ids if i not in cov]
        if missing:
            print("unknown step id(s): " + ", ".join(missing))
            return 2
        lines = []
        for line in text.split("\n"):
            m = COV.match(line)
            if m and m.group(2) in ids:
                rest = m.group(4).split(" :: ")[0]
                line = "- [x] %s (%s)%s :: %s" % (m.group(2), m.group(3), rest, a.note.strip())
            lines.append(line)
        open(issues_path, "w", encoding="utf-8").write("\n".join(lines))
        print("ticked %d step(s)" % len(ids))
        return 0

    text = open(a.file, encoding="utf-8").read()
    steps = split_steps(text)
    os.makedirs(a.out, exist_ok=True)
    old = open(issues_path, encoding="utf-8").read() if os.path.exists(issues_path) else ""
    oldcov = parse_cov(old)
    blocks = re.findall(r"(^## \w+ \| (?:FATAL|MAJOR|MINOR|NIT) \|.*?)(?=^## |\Z)", old, re.S | re.M)
    with open(os.path.join(a.out, "steps.md"), "w", encoding="utf-8") as fh:
        fh.write("# Steps of %s\n\nRead each step with the ten-point test in references/checks.md.\n\n" % os.path.basename(a.file))
        for i, (sec, body) in enumerate(steps, 1):
            fh.write("### S%03d  [%s]\n%s\n\n" % (i, sec or "top", body))
    cover, unticked = [], 0
    for i, (sec, body) in enumerate(steps, 1):
        sid, h = "S%03d" % i, digest(body)
        prev = oldcov.get(sid)
        keep = bool(prev and prev[0] and prev[1] == h)
        if prev and prev[0] and not keep:
            unticked += 1
        note = " :: " + prev[2] if keep and prev[2] else ""
        cover.append("- [%s] %s (%s) %s%s" % ("x" if keep else " ", sid, h, sec or "top", note))
    with open(issues_path, "w", encoding="utf-8") as fh:
        fh.write("# Issues\n\nBlock format (one per issue):\n\n"
                 "    ## M001 | MAJOR | open\n    Location: S012\n    Quote: ...\n    Problem: ...\n    Fix: ...\n\n"
                 "Severity: FATAL (answer or proof wrong), MAJOR (gap a referee would reject), MINOR, NIT.\n"
                 "Status: open, fixed, blocked, out-of-scope.\n\n")
        for b in blocks:
            fh.write(b.rstrip() + "\n\n")
        fh.write("## Coverage\n\nTick with: step_review.py FILE --out DIR --tick S001,S003-S005 --note \"what you checked\"\n\n"
                 + "\n".join(cover) + "\n")
    print("%d steps written to %s (%d previously ticked steps changed and were un-ticked)" % (
        len(steps), a.out, unticked))
    return 0


if __name__ == "__main__":
    sys.exit(main())

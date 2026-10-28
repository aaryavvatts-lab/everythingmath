#!/usr/bin/env python3
"""Mechanical lint for a written solution or proof (.md or .tex). Standard library only.

Catches what a script can catch: gap markers, hand-waving phrases, unbalanced math delimiters,
unfinished case splits, induction missing a base case, a missing final answer line. It cannot tell
whether a step is true. That is the job of the line-by-line referee read.

  proof_lint.py solution.md [--no-answer-needed] [--no-dashes]

Exit code 1 when any FAIL is found, otherwise 0.
"""
import argparse
import re
import sys

HANDWAVE = [
    (r"\bclearly\b", "clearly"), (r"\bobviously\b", "obviously"), (r"\btrivially\b", "trivially"),
    (r"\beasy to (see|check|verify|show)\b", "easy to see"), (r"\bit is (well[- ]known|standard)\b", "it is well known"),
    (r"\bsimilarly\b", "similarly"), (r"\bby symmetry\b", "by symmetry"), (r"\bleft to the reader\b", "left to the reader"),
    (r"\bthe rest is (routine|easy|similar)\b", "the rest is routine"), (r"\bone can (show|check|verify)\b", "one can show"),
    (r"\bwe can (show|check|verify)\b", "we can show"), (r"\bit is (easy|straightforward)\b", "it is easy"),
    (r"\band so on\b", "and so on"), (r"\bafter (some )?(simple )?(algebra|computation|calculation)\b", "after some algebra"),
    (r"\bwithout loss of generality\b|\bWLOG\b", "WLOG (justify it)"), (r"\bit can be shown\b", "it can be shown"),
]
MARKERS = re.compile(r"\[(GAP|TODO|UNPROVEN|CHECK|FIXME)[^\]]*\]|\?\?\?|\bTODO\b", re.I)
END = re.compile(
    r"(final answer|answer\s*[:=]|^\s*#+\s*(final\s+)?answer|\\boxed|\bhence\b.*\bproved\b|\bQED\b|∎|\\qed|\\blacksquare"
    r"|therefore[, ].*(=|is|are)|completes? the (proof|solution|computation|calculation|argument)"
    r"|as (claimed|required|desired)|which (proves|establishes|shows)|the (answer|integral|limit|sum|value) is)",
    re.I | re.M)
AI = re.compile(r"\b(delve|tapestry|it is important to note|in conclusion|let's dive)\b", re.I)


def strip_code(text):
    return re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--no-answer-needed", action="store_true", help="skip the final-answer check")
    ap.add_argument("--no-dashes", action="store_true", help="flag em and en dashes")
    a = ap.parse_args()
    try:
        raw = open(a.file, encoding="utf-8").read()
    except OSError as exc:
        print("cannot read %s: %s" % (a.file, exc))
        return 2
    text = strip_code(raw)
    lines = text.split("\n")
    fails, warns = [], []

    for i, line in enumerate(lines, 1):
        if MARKERS.search(line):
            fails.append((i, "open gap marker: %s" % line.strip()[:80]))
    body = re.sub(r"%.*", "", text) if a.file.endswith(".tex") else text
    for i, line in enumerate(body.split("\n"), 1):
        for pat, label in HANDWAVE:
            if re.search(pat, line, re.I):
                warns.append((i, "hand-wave phrase '%s': prove it or say why it holds" % label))
        if a.no_dashes and re.search("[\u2013\u2014]", line):
            warns.append((i, "em or en dash (banned by your preferences)"))
        if AI.search(line):
            warns.append((i, "filler phrase typical of generated text"))

    flat = text.replace("\\$", "")
    if flat.count("$$") % 2:
        fails.append((0, "unbalanced $$ delimiters"))
    single = flat.replace("$$", "")
    if single.count("$") % 2:
        fails.append((0, "unbalanced $ delimiters (an odd number of $)"))
    for env in set(re.findall(r"\\begin\{(\w+\*?)\}", text)):
        if len(re.findall(r"\\begin\{%s\}" % re.escape(env), text)) != len(re.findall(r"\\end\{%s\}" % re.escape(env), text)):
            fails.append((0, "\\begin{%s} and \\end{%s} do not match" % (env, env)))
    depth = 0
    for ch in re.sub(r"\\[{}]", "", single):
        depth += ch == "{"
        depth -= ch == "}"
        if depth < 0:
            break
    if depth != 0 and a.file.endswith(".tex"):
        fails.append((0, "unbalanced braces"))

    def where(pattern):
        m = re.search(pattern, text, re.I)
        return text[:m.start()].count("\n") + 1 if m else 0

    cases = [int(x) for x in re.findall(r"\bCase\s+(\d+)", text, re.I)]
    if cases and 1 in cases and max(cases) < 2:
        warns.append((where(r"\bCase\s+1"), "'Case 1' appears with no 'Case 2': is the split complete?"))
    if cases and not re.search(r"\b(exhaust|all cases|these cases cover|in every case|covers all|complete)", text, re.I):
        warns.append((where(r"\bCase\s+\d+"), "case split found but no sentence says the cases are exhaustive"))
    if re.search(r"\binduction\b", text, re.I):
        if not re.search(r"base case|basis|\bn\s*=\s*(0|1)\b|P\(\s*(0|1)\s*\)", text, re.I):
            fails.append((where(r"\binduction\b"), "induction used but no base case is visible"))
        if not re.search(r"inductive (step|hypothesis)|induction (step|hypothesis)|assume .* for (some|all)|suppose .* holds for", text, re.I):
            warns.append((where(r"\binduction\b"), "induction used but no inductive step or hypothesis is stated"))
    if re.search(r"\bcontradiction\b", text, re.I) and not re.search(r"\b(assume|suppose)\b", text, re.I):
        warns.append((where(r"\bcontradiction\b"), "'contradiction' appears but no assumption is introduced"))
    iffpat = r"\b(if and only if|iff)\b|\\iff|\\Leftrightarrow"
    if re.search(iffpat, text, re.I):
        if not re.search(r"(\u21d2|\\Rightarrow|\\implies|converse|conversely|\(\s*\u21d0|\bonly if\b|\(\s*\\Leftarrow)", text, re.I):
            warns.append((where(iffpat), "'iff' claimed but both directions are not visibly proved (look for the converse)"))
    if not a.no_answer_needed and not END.search(text):
        warns.append((0, "no final answer, conclusion or QED line found"))
    if len(re.findall(r"\w+", text)) < 15:
        warns.append((0, "very short: is this a complete solution?"))

    for ln, msg in fails:
        print("FAIL line %s: %s" % (ln or "-", msg))
    for ln, msg in warns:
        print("WARN line %s: %s" % (ln or "-", msg))
    print("proof_lint: %d FAIL, %d WARN" % (len(fails), len(warns)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

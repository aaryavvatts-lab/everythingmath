#!/usr/bin/env bash
# Build a LaTeX solution in a scratch folder and report problems.
#   compile_check.sh solution.tex [--copy-to DIR]
# Uses tectonic, latexmk or pdflatex, whichever exists. Never claims a clean build it did not run.
set -u
tex="${1:-}"; shift || true
copy=""
while [ $# -gt 0 ]; do case "$1" in --copy-to) copy="$2"; shift 2;; *) shift;; esac; done
[ -f "$tex" ] || { echo "usage: compile_check.sh file.tex [--copy-to DIR]"; exit 2; }
work="$(mktemp -d "${TMPDIR:-/tmp}/emcompile.XXXXXX")"
src="$(cd "$(dirname "$tex")" && pwd)"; base="$(basename "$tex" .tex)"
cp -R "$src"/. "$work"/ 2>/dev/null
cd "$work" || exit 2
if command -v tectonic >/dev/null 2>&1; then
  tectonic -X compile "$base.tex" >build.log 2>&1; rc=$?; engine=tectonic
elif command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode "$base.tex" >build.log 2>&1; rc=$?; engine=latexmk
elif command -v pdflatex >/dev/null 2>&1; then
  pdflatex -interaction=nonstopmode "$base.tex" >build.log 2>&1; pdflatex -interaction=nonstopmode "$base.tex" >>build.log 2>&1; rc=$?; engine=pdflatex
else
  echo "NO LaTeX engine found (install tectonic, latexmk or pdflatex). Build NOT verified."; exit 2
fi
undef=$(grep -ciE "undefined (control sequence|reference)|Reference .* undefined|Citation .* undefined" build.log)
overfull=$(grep -c "Overfull" build.log)
errs=$(grep -cE "^! |error:" build.log)
pages="?"
[ -f "$base.pdf" ] && pages=$(python3 - "$base.pdf" <<'PY'
import re, sys
n = None
try:
    import fitz
    n = len(fitz.open(sys.argv[1]))
except Exception:
    try:
        import pypdf
        n = len(pypdf.PdfReader(sys.argv[1]).pages)
    except Exception:
        data = open(sys.argv[1], "rb").read()
        n = len(re.findall(rb"/Type\s*/Page[^s]", data))
print(n or "?")
PY
)
echo "engine=$engine exit=$rc errors=$errs undefined=$undef overfull=$overfull pages=$pages"
if [ "$rc" -ne 0 ] || [ ! -f "$base.pdf" ]; then echo "COMPILE: FAIL"; grep -E "^! |error:" build.log | head -8; exit 1; fi
[ -n "$copy" ] && { mkdir -p "$copy" && cp "$base.pdf" "$copy"/ && echo "pdf copied to $copy"; }
if [ "$undef" -gt 0 ]; then echo "COMPILE: WARN undefined references or symbols"; exit 1; fi
echo "COMPILE: PASS"

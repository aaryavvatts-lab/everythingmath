#!/usr/bin/env bash
# Report which catalog skills and which tools exist. Installs nothing.
#   check_skills.sh [--tools] [--missing]
here="$(cd "$(dirname "$0")/.." && pwd)"
skills_dir="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
tools=0; only_missing=0
for a in "$@"; do case "$a" in --tools) tools=1;; --missing) only_missing=1;; esac; done
present=0; missing=0; plugin=0
names=$(awk -F'|' '/^\| `/{print $2}' "$here/catalog.md" | grep -oE '`[a-zA-Z0-9:_-]+`' | tr -d '`' | sort -u)
for n in $names; do
  case "$n" in *:*) plugin=$((plugin+1)); continue;; esac
  if [ -e "$skills_dir/$n" ]; then present=$((present+1)); [ $only_missing -eq 0 ] && echo "ok       $n"
  else missing=$((missing+1)); echo "MISSING  $n"; fi
done
echo "catalog skills: $present present, $missing missing, $plugin plugin skills not checked (names with a colon)"
if [ $tools -eq 1 ]; then
  echo "--- tools"
  for t in python3 tectonic latexmk pdflatex lean lake node ffmpeg git gh; do
    if command -v $t >/dev/null 2>&1; then echo "ok       $t"; else echo "absent   $t"; fi
  done
  for m in sympy mpmath numpy scipy matplotlib; do
    if python3 -c "import $m" >/dev/null 2>&1; then echo "ok       python:$m"; else echo "absent   python:$m  (pip install $m, optional)"; fi
  done
  echo "The bundled checkers use only the Python standard library and always work."
fi
exit 0

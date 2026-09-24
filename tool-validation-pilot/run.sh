#!/usr/bin/env bash
# Launch the checks on every pilot case and print a verdict table.
# A case "variant" is FLAGGED if the tool reports a conformance violation or any
# semantic warning ("! ..."); otherwise it is "clean".
#
# Usage:  bash private/cve-pilot/run.sh
set -u
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"   # repo root
JAR="$ROOT/target/sam4c-cli.jar"

printf "%-26s %-7s %s\n" "CASE" "VARIANT" "VERDICT"
printf -- "------------------------------------------------------------\n"
for d in "$ROOT"/private/cve-pilot/c*/; do
  [ -d "$d" ] || continue
  case=$(basename "$d")
  for v in vuln fixed; do
    arch="$d/$v.arch.yaml"; rules="$d/$v.secdsl"
    [ -f "$arch" ] && [ -f "$rules" ] || continue
    out=$(java -jar "$JAR" "$arch" "$rules" 2>&1)
    if   echo "$out" | grep -q "Conformance violations"; then verdict="FLAGGED (conformance)"
    elif echo "$out" | grep -qE "^  ! ";                  then verdict="FLAGGED (semantic)"
    elif echo "$out" | grep -q "Error:";                  then verdict="ERROR (parse/load)"
    else                                                       verdict="clean"
    fi
    printf "%-26s %-7s %s\n" "$case" "$v" "$verdict"
  done
done

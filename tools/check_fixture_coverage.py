#!/usr/bin/env python3
"""Progress tracker for the hand-authored semantic fixtures (CreateTests.md).

Reads generated/rules-v1.0.0.json and the fixture folders, then reports:

  1. every non-schema rule that has no fixture yet (handwritten rules look in
     fixtures/handwritten/, ref-type rules in fixtures/generated/ref-type/),
     with "blocked" rules (see BLOCKED below) listed separately;
  2. every fixture file whose name cites a rule ID that does not exist (rule
     renumbering before release will cause this - Design.md);
  3. every fixture file whose name breaks the naming convention
     <rule-id>-<pass|fail>-<count>-<test>[-<rule-id-2>-<count-2>].sed2.json
     (or pass-<nn>-<test>.sed2.json for the rule-less "kit" pass fixtures);
  4. rules that have fail fixtures but no pass twin (and vice versa).

Exit status is 1 when (2) or (3) found anything, or when a testable rule has no
fixture; 0 otherwise. Run from anywhere:

    python3 tools/check_fixture_coverage.py [--root DIR] [--verbose]

ASCII only, per Claude.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict

# Rules that cannot be tested today, with the reason (CreateTests.md section 2).
BLOCKED = {
    "SEDDocument-0012": "duplicate JSON keys: deliberately not implemented in v1",
    "Plot-0008": "rule text contradicts the schema (see ProposedRules.md); generator skips it",
    "SEDBase-0014": "no outputs.json declares a runtime dimension 'min', so no class can trigger it",
}

# <rule-id>-<pass|fail>-<count>-<test>[-<rule-id-2>-<count-2>].sed2.json
# A rule id is <Word>-<4 digits>. The test name may contain hyphens, so the
# chain suffix is only recognised at the very end (same limitation as the
# harnesses: chained files use underscores inside the test name).
# Generic pass fixtures that belong to no single rule (the "kit") are named
# pass-<nn>-<test>.sed2.json; the harnesses accept that prefix as "must validate clean".
KIT_RE = re.compile(r"^pass-\d{2}-.+\.sed2\.json$")

NAME_RE = re.compile(
    r"^(?P<rule>[A-Za-z][A-Za-z0-9]*-\d{4})-(?P<kind>pass|fail)-(?P<count>\d{2})-(?P<test>.+?)"
    r"(?:-(?P<rule2>[A-Za-z][A-Za-z0-9]*-\d{4})-(?P<count2>\d{2}))?\.sed2\.json$"
)


def load_rules(root):
    path = os.path.join(root, "generated", "rules-v1.0.0.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rules = data["rules"] if isinstance(data, dict) and "rules" in data else data
    if isinstance(rules, dict):
        rules = [dict(v, id=k) for k, v in rules.items()]
    return {r["id"]: r for r in rules}


def walk_fixtures(folder):
    for dirpath, _dirs, files in os.walk(folder):
        for name in sorted(files):
            if name.endswith(".json"):
                yield os.path.join(dirpath, name), name


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),
                    help="repository root (default: parent of tools/)")
    ap.add_argument("--verbose", action="store_true", help="also list covered rules with counts")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)

    rules = load_rules(root)
    by_check = defaultdict(list)
    for rid, r in rules.items():
        by_check[r.get("check", "?")].append(rid)

    hw_dir = os.path.join(root, "fixtures", "handwritten")
    gen_dir = os.path.join(root, "fixtures", "generated")

    problems = 0
    # rule -> {"pass": n, "fail": n} across every fixture dir; chained files
    # count toward the first rule only for pass/fail, and toward the second as
    # a "chain" mention.
    seen = defaultdict(lambda: {"pass": 0, "fail": 0, "chain": 0})
    bad_names, unknown_ids = [], []
    for folder in (hw_dir, gen_dir):
        for path, name in walk_fixtures(folder):
            if not name.endswith(".sed2.json"):
                continue
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if KIT_RE.match(name):
                continue
            m = NAME_RE.match(name)
            if not m:
                bad_names.append(rel)
                continue
            for key in ("rule", "rule2"):
                rid = m.group(key)
                if rid and rid not in rules:
                    unknown_ids.append((rel, rid))
            seen[m.group("rule")][m.group("kind")] += 1
            if m.group("rule2"):
                seen[m.group("rule2")]["chain"] += 1

    def covered(rid):
        s = seen.get(rid)
        return bool(s) and (s["pass"] + s["fail"] + s["chain"]) > 0

    # 1. missing coverage
    missing, blocked = [], []
    for rid in sorted(by_check.get("handwritten", []) + by_check.get("ref-type", [])):
        if rid in BLOCKED:
            blocked.append(rid)
        elif not covered(rid):
            missing.append(rid)

    print("Rules by check kind: " + ", ".join(f"{k}={len(v)}" for k, v in sorted(by_check.items())))
    hw = sorted(by_check.get("handwritten", []))
    hw_done = [r for r in hw if covered(r)]
    print(f"Handwritten rules with fixtures: {len(hw_done)}/{len(hw)} "
          f"({sum(1 for r in blocked if r in hw)} blocked)")
    rt = sorted(by_check.get("ref-type", []))
    print(f"Ref-type rules with fixtures:    {sum(1 for r in rt if covered(r))}/{len(rt)}")

    if missing:
        print("\nNo fixture yet (testable):")
        for rid in missing:
            print(f"  {rid}  [{rules[rid].get('check')}]  {rules[rid].get('rule', '')[:80]}")
        problems += 1
    if blocked:
        print("\nBlocked (recorded, not faked):")
        for rid in blocked:
            print(f"  {rid}  {BLOCKED[rid]}")

    # 2. unknown ids
    if unknown_ids:
        print("\nFixtures naming a rule ID that does not exist:")
        for rel, rid in unknown_ids:
            print(f"  {rel}  ->  {rid}")
        problems += 1

    # 3. naming convention
    if bad_names:
        print("\nFixtures whose name breaks the convention:")
        for rel in bad_names:
            print(f"  {rel}")
        problems += 1

    # 4. fail without pass twin / pass without fail (handwritten rules only;
    # the generated tier guarantees its own twins).
    lopsided = []
    for rid in hw:
        if rid in BLOCKED:
            continue
        s = seen.get(rid, {"pass": 0, "fail": 0})
        if s["fail"] and not s["pass"]:
            lopsided.append((rid, "fail fixtures but no pass twin"))
        elif s["pass"] and not s["fail"]:
            lopsided.append((rid, "pass fixtures but no fail fixture"))
    if lopsided:
        print("\nHandwritten rules with unbalanced coverage:")
        for rid, why in lopsided:
            print(f"  {rid}  {why}")

    if args.verbose:
        print("\nPer-rule fixture counts (pass / fail / chained-in):")
        for rid in sorted(seen):
            s = seen[rid]
            print(f"  {rid:<28} {s['pass']:>4} {s['fail']:>4} {s['chain']:>4}")

    print("\nOK" if not problems else "\nIncomplete")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

"""Hand-written glue: runs every fixture in this tree's fixtures/ directory
through the generated library's parser + validate(), and checks it against
the rule ID(s)/count(s) encoded in the filename - see Design.md's Testing
section for the naming convention this parses.

This file lives under templates/python/tests/ (hand-written, never
regenerated - see Design.md's Code Generation section). generator/
emit_python.py copies it verbatim to <out>/python/test_fixtures.py as part
of every `generate.py` run that includes the python target (see
_copy_test_fixtures_py) - never by hand, so a fresh spec regeneration
always carries a matching, up-to-date copy with it.

Nothing below is specific to any one spec tree (test-specsheets/ vs.
specsheets/, or any future one): the generated package to import, the
fixtures directory to read, and which classes need "direct" (not
document-embedded) validation are all discovered at test-collection time
from whatever got generated and whatever fixture files exist on disk -
never a hardcoded package name or class list. Point this file at a
different generated tree and it "just works" unmodified.
"""
from __future__ import annotations

import glob
import importlib
import inspect
import json
import os
import re
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR = os.path.join(_HERE, "src")


def _generated_package_name() -> str:
    """The src/ layout this file is copied alongside always has exactly one
    top-level package - whatever name --python-package was given for this
    generate.py run. Discovered here (rather than hardcoded) so this same
    file works unmodified against any generated tree."""
    names = sorted(
        n for n in os.listdir(_SRC_DIR)
        if os.path.isdir(os.path.join(_SRC_DIR, n))
        and not n.startswith((".", "_"))
        and os.path.isfile(os.path.join(_SRC_DIR, n, "__init__.py"))
    )
    assert len(names) == 1, (
        f"expected exactly one generated package under {_SRC_DIR}, found {names} "
        "- test_fixtures.py can't auto-discover which one to import"
    )
    return names[0]


if _SRC_DIR not in sys.path:
    # Works whether or not the package was `pip install -e`'d - this file
    # is self-sufficient either way.
    sys.path.insert(0, _SRC_DIR)

t = importlib.import_module(_generated_package_name())
_model = importlib.import_module(t.__name__ + ".model")

# This file is always copied to <out>/python/test_fixtures.py, and every
# generated tree's own fixtures/ directory lives two levels up from
# <out>/python/ - as <spec-root-parent>/fixtures/ (e.g. generated/python/
# -> fixtures/, or test-specsheets/generated/python/ ->
# test-specsheets/fixtures/) - so this default needs no per-tree
# configuration. SED2_FIXTURES_DIR still overrides it, for local ad hoc runs
# against a different fixture set.
FIXTURES_DIR = os.environ.get(
    "SED2_FIXTURES_DIR",
    os.path.join(_HERE, "..", "..", "fixtures"),
)

FIXTURE_RE = re.compile(
    r"^(?:(?P<rule>[A-Za-z0-9_-]+)-(?P<kind>pass|fail)-(?P<count>\d+)-(?P<name>.+?)"
    r"(?P<chain>(?:-[A-Za-z0-9_-]+-\d+)*))\.sed2\.json$"
)


def _expected_from_filename(fname: str):
    """Returns (kind, [(rule_id, count), ...]) parsed from the fixture name."""
    base = os.path.basename(fname)
    if base.startswith("pass-"):
        return "pass", []
    m = FIXTURE_RE.match(base)
    assert m, f"fixture name doesn't match convention: {base}"
    rule, kind, count, chain = m.group("rule"), m.group("kind"), m.group("count"), m.group("chain")
    expected = [(rule, int(count))]
    if chain:
        parts = chain.strip("-").split("-")
        # parts alternate: <rule-id-segment...>-<count>, and rule ids
        # themselves always end in a numeric NNNN segment (4 digits) per
        # the rule-numbering convention, while a chained <count> is the
        # short (1-2 digit) count width used elsewhere in the filename -
        # so a 4-digit numeric token is part of the rule id, never a count
        # boundary, and only a non-4-digit numeric token ends a segment.
        nums = [i for i, p in enumerate(parts) if p.isdigit() and len(p) != 4]
        start = 0
        for idx in nums:
            rid = "-".join(parts[start:idx])
            cnt = int(parts[idx])
            expected.append((rid, cnt))
            start = idx + 1
    return kind, expected


def _all_fixture_files():
    """Every *.sed2.json anywhere under FIXTURES_DIR - flat, or in whatever
    subdirectories exist there (Design.md's Repository Layout documents
    fixtures/generated/ for schema-derivable fixtures and fixtures/
    handwritten/ for hand-authored semantic ones; a spec tree with neither
    subdirectory yet, or fixtures sitting flat at the top level, both work
    the same way here - nothing below assumes any particular subdirectory
    exists). fixtures/archive/ (deprecated-rule fixtures - Design.md) is
    the one deliberate exclusion: never part of the active suite."""
    pattern = os.path.join(FIXTURES_DIR, "**", "*.sed2.json")
    files = glob.glob(pattern, recursive=True)
    files = [
        f for f in files
        if "archive" not in os.path.relpath(f, FIXTURES_DIR).split(os.sep)[:-1]
    ]
    return sorted(files)


def _direct_only_classes() -> dict:
    """rule_id -> class, for every generated class whose own _type-const
    rule (RUNTIME's _validate_own: `self._TYPE_CONST is not None and
    instance.get("_type") != self._TYPE_CONST`) can only ever be exercised
    by validating that class directly. Embedded through a parent's
    discriminated dict/array field, a _type mismatch is caught by the
    PARENT discriminator's own dispatch before this rule could ever see it
    (it never resolves to any one concrete sibling class) - see whichever
    spec tree's fixtures/README.md explains this for its own tree's
    classes. Built from the generated model itself (every class's
    _TYPE_RULE_ID, set by generator/emit_python.py from the schema) rather
    than a hardcoded class list, so this adapts automatically to any spec's
    own set of _type-discriminated classes."""
    result = {}
    for _name, obj in inspect.getmembers(_model, inspect.isclass):
        rid = getattr(obj, "_TYPE_RULE_ID", None)
        if rid:
            result[rid] = obj
    return result


_DIRECT_ONLY = _direct_only_classes()


@pytest.mark.parametrize("path", _all_fixture_files(), ids=lambda p: os.path.basename(p))
def test_fixture(path):
    kind, expected = _expected_from_filename(path)
    with open(path) as f:
        raw = f.read()
    instance = json.loads(raw)

    primary_rule = expected[0][0] if expected else None
    direct_cls = _DIRECT_ONLY.get(primary_rule)
    if direct_cls is not None:
        obj = direct_cls()
        _model._load_fields(obj, instance)
        problems = obj.validate()
    else:
        doc = t.read_from_string(raw)
        problems = doc.validate()
        # round-trip check for pass fixtures
        if kind == "pass":
            rt = json.loads(t.write_to_string(doc))
            assert rt == instance, f"round-trip mismatch for {path}"

    if kind == "pass":
        assert problems == [], f"{path} expected to pass, got {problems}"
        return

    counts = {}
    for p in problems:
        counts[p.rule_id] = counts.get(p.rule_id, 0) + 1
    for rid, cnt in expected:
        assert counts.get(rid, 0) == cnt, (
            f"{path}: expected rule {rid} to fire {cnt} time(s), "
            f"got {counts.get(rid, 0)} (all problems: {problems})"
        )
    allowed_ids = {rid for rid, _ in expected}
    extra = {rid: c for rid, c in counts.items() if rid not in allowed_ids}
    assert not extra, f"{path}: unexpected extra violations: {extra} (all: {problems})"

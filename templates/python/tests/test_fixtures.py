"""Hand-written glue: runs every test-specsheets/fixtures/*.sed2.json fixture
through the generated libsed2test library's parser + validate(), and checks
it against the rule ID(s)/count(s) encoded in the filename - see Design.md's
Testing section for the naming convention this parses.

This file lives under templates/python/tests/ (hand-written, never
regenerated - see Design.md's Code Generation section) and is copied
alongside the generated library for `pytest` to run.
"""
import glob
import json
import os
import re

import pytest

import libsed2test as t

FIXTURES_DIR = os.environ.get(
    "SED2_FIXTURES_DIR",
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "fixtures"),
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
    return sorted(glob.glob(os.path.join(FIXTURES_DIR, "*.sed2.json")))


def _rule_id_of_direct_class(instance: dict):
    """Some rules (see fixtures/README.md - the six *_-0002 _type-const rules)
    are only reachable by validating one class's own schema directly, not
    embedded through a document. Route those fixtures at the named class."""
    direct_classes = {
        "Choice": t.Choice, "WeightedChoice": t.WeightedChoice,
        "SimpleWidget": t.SimpleWidget, "FancyWidget": t.FancyWidget,
        "SimpleReport": t.SimpleReport,
    }
    tv = instance.get("_type")
    for name, cls in direct_classes.items():
        if tv == cls._TYPE_CONST or (name == "SimpleWidget" and tv == "simpleWidget") :
            return cls
    return None


@pytest.mark.parametrize("path", _all_fixture_files(), ids=lambda p: os.path.basename(p))
def test_fixture(path):
    kind, expected = _expected_from_filename(path)
    with open(path) as f:
        raw = f.read()
    instance = json.loads(raw)

    if "acme-AcmeWidget-0002" in os.path.basename(path) or os.path.basename(path).startswith((
            "Choice-0002", "WeightedChoice-0002", "SimpleWidget-0002", "FancyWidget-0002", "SimpleReport-0002")):
        # direct-class-only rules (see fixtures/README.md)
        cls_map = {
            "Choice-0002": t.Choice, "WeightedChoice-0002": t.WeightedChoice,
            "SimpleWidget-0002": t.SimpleWidget, "FancyWidget-0002": t.FancyWidget,
            "SimpleReport-0002": t.SimpleReport, "acme-AcmeWidget-0002": t.AcmeWidget,
        }
        key = next(k for k in cls_map if os.path.basename(path).startswith(k))
        obj = cls_map[key]()
        from libsed2test.model import _load_fields
        _load_fields(obj, instance)
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

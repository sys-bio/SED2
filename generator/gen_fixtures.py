"""Schema-derivable fixture generator (Design.md's Test Generation and Spec
Evolution section): "Schema-derivable fixtures - for constraints the JSON
schema captures directly, like required fields, types, enums, and patterns -
are generated mechanically by the same generator run that produces the class
code... A required field implies a missing-it fixture... These are never
hand-edited and can't go stale."

Scope of this first pass (see Task tracking - kept honest rather than
over-claiming): one fail-fixture per REQUIRED field (every class, every
required attribute) and one fail-fixture per PATTERN-constrained field
(SId/SIdRef/version-style strings), across the whole class graph, each
embedded into a minimal otherwise-valid SEDDocument via the shortest
composition path from the document root. Enum-valued and custom
"X-or-reference" anyOf fields are not yet fixture-generated (see Task #13 -
neither shape currently has real live field data blocking this, but neither
is wired up yet either).

Every fixture this module writes is verified against the real generated
Python library before being written (see verify_fixtures.py) - a fixture
that doesn't actually fire the rule it claims, or fires something else too,
is a bug in this generator, not a fixture worth keeping.
"""
from __future__ import annotations

import json
import os
import re
from typing import Optional

from .spec import SpecModel, FieldType, Field, FlatClass


def _matches(pattern: Optional[str], s: str) -> bool:
    if not pattern:
        return True
    return re.match(pattern, s) is not None


def _candidate_leaf_value(f: Field):
    """A minimal value satisfying f's own schema-derivable shape (type +
    pattern + numeric bounds), or None if this module doesn't know how to
    synthesize one (caller should skip that field's fixture rather than
    guess wrong)."""
    t = f.type
    kind = t.kind
    if kind == "boolean":
        return True
    if kind == "integer":
        v = 1
        if t.minimum is not None:
            v = int(t.minimum) + (1 if t.exclusive_minimum is not None else 0)
        return v
    if kind == "number":
        v = 1.0
        if t.minimum is not None:
            v = float(t.minimum) + (1.0 if t.exclusive_minimum is not None else 0.0)
        return v
    if kind == "any":
        return {}
    # OrRef kinds: a minimal LITERAL value (not the reference alternative)
    # of the same underlying JSON shape - schema-derivable fixtures don't
    # need to exercise the reference side, only whether the field accepts
    # its declared literal shape at all.
    _ORREF_TO_PLAIN = {
        "NumberOrRef": "number", "IntegerOrRef": "integer", "BooleanOrRef": "boolean",
        "ArrayOrRef": "array", "DictOrRef": "dict",
    }
    if kind in _ORREF_TO_PLAIN:
        plain = _ORREF_TO_PLAIN[kind]
        if plain in ("array", "dict"):
            return [] if plain == "array" else {}
        return _candidate_leaf_value(Field(f.name, FieldType(kind=plain, minimum=t.minimum,
                                                               exclusive_minimum=t.exclusive_minimum),
                                            f.required, f.rule_id, f.required_rule_id, f.origin_class))
    if kind in ("string", "SId", "SIdRef", "StringOrRef"):
        candidates = ["x", "id1", "v1.0.0", "#tasks:x", "x1", "a"]
        pattern = t.pattern
        if kind == "SIdRef" and not pattern:
            pattern = r"^#.*$"
        if kind == "SId" and not pattern:
            pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"
        for c in candidates:
            if _matches(pattern, c):
                return c
        return None  # unknown pattern shape - don't guess
    return None  # dict/array/ref-class/ref-discriminator handled by the caller


def _invalid_leaf_value(f: Field):
    """A value that VIOLATES f's pattern/type - the deliberate corruption for
    a pattern-violation fixture. None if this field has nothing to violate
    this way (no pattern, or a kind this module doesn't corrupt)."""
    t = f.type
    if t.pattern or t.kind in ("SId", "SIdRef"):
        pattern = t.pattern
        if t.kind == "SIdRef" and not pattern:
            pattern = r"^#.*$"
        if t.kind == "SId" and not pattern:
            pattern = r"^[A-Za-z_][A-Za-z0-9_]*$"
        for bad in ("", "9bad id!", " "):
            if not _matches(pattern, bad):
                return bad
    return None


class _Embedder:
    """Finds a shortest composition path from the document root to every
    generatable class (via dict/array/ref-class/ref-discriminator fields),
    and builds minimal-but-otherwise-valid JSON instances along that path -
    see this module's docstring."""

    def __init__(self, model: SpecModel):
        self.model = model
        self._id_counter = 0
        self._paths: dict[str, list[tuple[str, str]]] = {}  # class -> [(field_name, via_class), ...] from doc
        self._build_paths()

    def _next_id(self) -> str:
        self._id_counter += 1
        return f"x{self._id_counter}"

    def _build_paths(self):
        doc_name = self.model.document_class
        # BFS over: class -> [(field_name, target_class), ...]
        from collections import deque
        edges: dict[str, list[tuple[str, str]]] = {}
        for cname, c in self.model.classes.items():
            outs = []
            for f in c.fields:
                t = f.type
                if t.kind == "dict" and t.item_discriminator:
                    disc = self.model.discriminators.get(t.item_discriminator)
                    if disc:
                        for br in disc.branches.values():
                            outs.append((f.name, br.class_name))
                elif t.kind == "array" and t.item_discriminator2:
                    disc = self.model.discriminators.get(t.item_discriminator2)
                    if disc:
                        for br in disc.branches.values():
                            outs.append((f.name, br.class_name))
                elif t.kind in ("dict", "array") and t.item_class:
                    outs.append((f.name, t.item_class))
                elif t.kind == "ref-class" and t.item_class:
                    outs.append((f.name, t.item_class))
                elif t.kind == "ref-discriminator" and t.item_discriminator:
                    disc = self.model.discriminators.get(t.item_discriminator)
                    if disc:
                        for br in disc.branches.values():
                            outs.append((f.name, br.class_name))
            edges[cname] = outs

        self._paths[doc_name] = []
        q = deque([doc_name])
        while q:
            cur = q.popleft()
            for field_name, target in edges.get(cur, []):
                if target not in self._paths:
                    self._paths[target] = self._paths[cur] + [(field_name, target)]
                    q.append(target)

    def path_to(self, class_name: str) -> Optional[list[tuple[str, str]]]:
        return self._paths.get(class_name)

    def field_of(self, class_name: str, field_name: str) -> Optional[Field]:
        for f in self.model.classes[class_name].fields:
            if f.name == field_name:
                return f
        return None

    def minimal_json(self, class_name: str, overrides: Optional[dict] = None,
                      omit: Optional[set] = None) -> Optional[dict]:
        """A minimal JSON object satisfying class_name's own required fields
        (plus _type, if it has one). Returns None if some required field
        can't be synthesized (unknown pattern shape, etc.) - caller skips."""
        omit = omit or set()
        c = self.model.classes[class_name]
        out = {}
        if c.has_type and c.type_const:
            out["_type"] = c.type_const
        for f in c.fields:
            if f.name in omit or not f.required:
                continue
            val = self._minimal_field_value(f)
            if val is None:
                return None
            out[f.name] = val
        if overrides:
            out.update(overrides)
        return out

    def _minimal_field_value(self, f: Field):
        t = f.type
        if t.kind in ("dict", "array"):
            return {} if t.kind == "dict" else []
        if t.kind == "ref-class" and t.item_class:
            return self.minimal_json(t.item_class)
        if t.kind == "ref-discriminator" and t.item_discriminator:
            disc = self.model.discriminators.get(t.item_discriminator)
            if not disc or not disc.branches:
                return None
            branch = next(iter(disc.branches.values()))
            return self.minimal_json(branch.class_name)
        return _candidate_leaf_value(f)

    def build_document(self, target_class: str, leaf_overrides: Optional[dict] = None,
                        leaf_omit: Optional[set] = None) -> Optional[dict]:
        """Builds a full, minimal SEDDocument JSON with one instance of
        target_class embedded via the shortest path from the root, with
        leaf_overrides/leaf_omit applied to that target instance (the
        deliberate fixture corruption). Returns None if any step along the
        way can't be synthesized."""
        path = self.path_to(target_class)
        if path is None:
            return None
        leaf = self.minimal_json(target_class, overrides=leaf_overrides, omit=leaf_omit)
        if leaf is None:
            return None
        classes_on_path = [self.model.document_class] + [t for _, t in path]
        current = leaf
        for i in range(len(path) - 1, -1, -1):
            field_name, _target = path[i]
            parent_class = classes_on_path[i]
            parent_field = self.field_of(parent_class, field_name)
            parent_json = self.minimal_json(parent_class, omit={field_name})
            if parent_json is None:
                return None
            if parent_field.type.kind == "dict":
                parent_json[field_name] = {self._next_id(): current}
            elif parent_field.type.kind == "array":
                parent_json[field_name] = [current]
            else:  # ref-class / ref-discriminator: a single nested object
                parent_json[field_name] = current
            current = parent_json
        return current


def _slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", name) or "x"


def generate_schema_fixtures(model: SpecModel) -> dict:
    """Writes fail-fixtures for every required field and every
    pattern-constrained field it can synthesize a document for, into
    out_dir. Returns a dict of {relative_filename: json_dict} - NOT written
    to disk unverified; see generate.py for the verify-then-write step."""
    embedder = _Embedder(model)
    fixtures: dict[str, dict] = {}
    skipped: list[str] = []

    for cname, c in model.classes.items():
        if embedder.path_to(cname) is None:
            continue  # not reachable from the document root - can't embed
        for f in c.fields:
            if f.from_namespace:
                continue  # namespace fixtures are out of scope here
            if f.required and f.required_rule_id:
                doc = embedder.build_document(cname, leaf_omit={f.name})
                if doc is None:
                    skipped.append(f"{cname}.{f.name} (required, could not synthesize siblings)")
                    continue
                fname = f"{f.required_rule_id}-fail-01-missing-{_slug(cname)}-{_slug(f.name)}.sed2.json"
                fixtures[fname] = doc
            bad = _invalid_leaf_value(f)
            if bad is not None and f.rule_id and isinstance(f.rule_id, str):
                doc = embedder.build_document(cname, leaf_overrides={f.name: bad})
                if doc is None:
                    skipped.append(f"{cname}.{f.name} (pattern, could not synthesize siblings)")
                    continue
                fname = f"{f.rule_id}-fail-01-pattern-{_slug(cname)}-{_slug(f.name)}.sed2.json"
                fixtures[fname] = doc

    if skipped:
        print(f"[gen_fixtures] skipped {len(skipped)} field(s) (see below) - "
              f"not yet synthesizable, not written as fixtures:")
        for s in skipped[:20]:
            print(f"  - {s}")
        if len(skipped) > 20:
            print(f"  ... and {len(skipped) - 20} more")

    return fixtures


def _rule_id_from_filename(fname: str) -> str:
    # <rule-id>-fail-01-... ; rule ids themselves may contain hyphens
    # (namespace ones), so cut at the literal "-fail-" marker instead of
    # splitting on "-".
    return fname.split("-fail-")[0]


def verify_and_write(fixtures: dict, out_dir: str, python_pkg_root: str, package_name: str) -> dict:
    """Loads the just-generated Python package fresh (no install - straight
    off disk) and runs every candidate fixture through read_from_string() +
    validate(), keeping only the ones that fire EXACTLY their claimed rule,
    exactly once, and nothing else. Writes the survivors to out_dir and
    returns a small report dict. A fixture that doesn't check out is a bug
    in this module's assumptions, not a fixture worth shipping - it's
    dropped and reported, never written."""
    import importlib
    import sys as _sys

    src_dir = os.path.join(python_pkg_root, "src")
    added = src_dir not in _sys.path
    if added:
        _sys.path.insert(0, src_dir)
    # Force a fresh import in case an older build of the same package name
    # is already loaded in this process (generate.py may run more than once
    # per process in tests).
    for mod in list(_sys.modules):
        if mod == package_name or mod.startswith(package_name + "."):
            del _sys.modules[mod]
    pkg = importlib.import_module(package_name)

    written = {}
    failed = {}
    try:
        for fname, doc_json in fixtures.items():
            expected_rule = _rule_id_from_filename(fname)
            try:
                raw = json.dumps(doc_json)
                doc = pkg.read_from_string(raw)
                problems = doc.validate()
            except Exception as e:  # noqa: BLE001 - report, never crash the generate run
                failed[fname] = f"raised {type(e).__name__}: {e}"
                continue
            counts: dict[str, int] = {}
            for p in problems:
                counts[p.rule_id] = counts.get(p.rule_id, 0) + 1
            if counts == {expected_rule: 1}:
                written[fname] = doc_json
            else:
                failed[fname] = f"expected {{{expected_rule!r}: 1}}, got {counts!r}"
    finally:
        if added:
            _sys.path.remove(src_dir)

    os.makedirs(out_dir, exist_ok=True)
    for fname, doc_json in written.items():
        with open(os.path.join(out_dir, fname), "w") as f:
            json.dump(doc_json, f, indent=2)
            f.write("\n")

    if failed:
        print(f"[gen_fixtures] {len(failed)} candidate fixture(s) failed verification "
              f"(dropped, not written):")
        for fname, why in list(failed.items())[:20]:
            print(f"  - {fname}: {why}")
        if len(failed) > 20:
            print(f"  ... and {len(failed) - 20} more")
    print(f"[gen_fixtures] wrote {len(written)} verified fixture(s) to {out_dir}")

    return {"written": sorted(written), "failed": failed}

"""Shared runtime for the generated libsed2test package. GENERATED - do not
hand-edit; regenerate from test-specsheets/ via generator/generate.py."""
from __future__ import annotations

import json
import re
import weakref
from dataclasses import dataclass, field as _field
from typing import Any, Optional

import jsonschema

SID_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
SIDREF_PATTERN = re.compile(r"^#.*$")
NAMESPACE_KEY_PATTERN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)@([A-Za-z_][A-Za-z0-9_]*)$")


class ApiError(Exception):
    """Raised for any misuse of the generated API itself (wrong-kind OrRef
    access, get on an unset field, an out-of-range insert, ...) - never for
    a document that merely fails a SED2 validation rule. See Design.md's
    Classes section."""


@dataclass
class ValidationProblem:
    rule_id: str
    severity: str
    rule: str
    message: str
    location: str

    def __repr__(self):
        return f"ValidationProblem({self.rule_id}, {self.severity!r}, {self.location!r})"


# ---- rule catalogue (generated) -------------------------------------------
# Populated by rules_data.py at import time: id -> (rule_text, message_template, severity)
RULE_CATALOG: dict[str, tuple[str, str, str]] = {}


def _fmt_message(rule_id: str, **placeholders) -> str:
    _rule_text, template, _sev = RULE_CATALOG.get(rule_id, ("", "{schema-message}", "error"))
    out = template
    for k, v in placeholders.items():
        out = out.replace("{" + k + "}", str(v))
    return out


def _severity_of(rule_id: str) -> str:
    return RULE_CATALOG.get(rule_id, ("", "", "error"))[2]


def make_problem(rule_id: str, location: str, **placeholders) -> ValidationProblem:
    rule_text = RULE_CATALOG.get(rule_id, ("", "", "error"))[0]
    return ValidationProblem(
        rule_id=rule_id,
        severity=_severity_of(rule_id),
        rule=rule_text,
        message=_fmt_message(rule_id, location=location, **placeholders),
        location=location,
    )


def is_reference(value: Any) -> bool:
    return isinstance(value, str) and value.startswith("#")


# ---- per-field leaf validation, via the real JSON Schema validator --------
_LEAF_SCHEMAS = {
    "string": {"type": "string"},
    "integer": {"type": "integer"},
    "number": {"type": "number"},
    "boolean": {"type": "boolean"},
    "SId": {"type": "string", "pattern": SID_PATTERN.pattern},
    "SIdRef": {"type": "string", "pattern": SIDREF_PATTERN.pattern},
    "StringOrRef": {"anyOf": [{"type": "string"}]},
    "NumberOrRef": {"anyOf": [{"type": "number"}, {"type": "string", "pattern": SIDREF_PATTERN.pattern}]},
}


def leaf_schema_for(kind: str, minimum=None, exclusive_minimum=None, pattern=None) -> dict:
    base = dict(_LEAF_SCHEMAS[kind])
    if minimum is not None:
        base = {**base, "minimum": minimum}
    if exclusive_minimum is not None:
        base = {**base, "exclusiveMinimum": exclusive_minimum}
    if pattern is not None and kind == "string":
        base = {**base, "pattern": pattern}
    return base


def leaf_value_ok(kind: str, value: Any, minimum=None, exclusive_minimum=None, pattern=None) -> bool:
    schema = leaf_schema_for(kind, minimum, exclusive_minimum, pattern)
    try:
        jsonschema.validate(value, schema)
        return True
    except jsonschema.ValidationError:
        return False


class FieldSpec:
    __slots__ = ("name", "kind", "required", "rule_id", "required_rule_id",
                 "origin_catchall", "minimum", "exclusive_minimum", "pattern",
                 "item_class", "item_discriminator")

    def __init__(self, name, kind, required, rule_id, required_rule_id,
                 origin_catchall, minimum=None, exclusive_minimum=None,
                 pattern=None, item_class=None, item_discriminator=None):
        self.name = name
        self.kind = kind
        self.required = required
        self.rule_id = rule_id
        self.required_rule_id = required_rule_id
        self.origin_catchall = origin_catchall
        self.minimum = minimum
        self.exclusive_minimum = exclusive_minimum
        self.pattern = pattern
        self.item_class = item_class
        self.item_discriminator = item_discriminator


LEAF_KINDS = {"string", "integer", "number", "boolean", "SId", "SIdRef", "StringOrRef", "NumberOrRef"}


class SedBase:
    """Universal base: every generated element (mirrors TestBaseFields'
    name/description) plus parent/document backpointers, generic namespace
    attribute storage, and the shared validate() engine. See Design.md's
    Classes section - Python uses weakref for parent/document to avoid
    reference cycles, matching this project's C++ raw-pointer intent."""

    _FIELDS: list = []            # set per concrete class
    _REQUIRED_NAMES: set = set()
    _TYPE_CONST: Optional[str] = None
    _TYPE_RULE_ID: Optional[str] = None
    _OWN_CATCHALL: str = ""
    _NAMESPACE_FIELDS: dict = {}       # prefix -> [FieldSpec, ...]
    _NAMESPACE_CATCHALL: dict = {}     # prefix -> "<Class>-<prefix>-0000"
    _KNOWN_NAMESPACE_PREFIXES: set = set()
    # The universal name/description mixin (TestBaseFields/SEDBaseFields)
    # isn't a per-class FieldSpec - its own rule IDs are set once, the same
    # on every concrete class, from the base mixin's own validation rules.
    _NAME_RULE_ID: Optional[str] = None
    _DESC_RULE_ID: Optional[str] = None
    _BASE_CATCHALL: str = ""

    def __init__(self):
        self._name: Optional[str] = None
        self._description: Optional[str] = None
        self._values: dict = {}          # field name -> stored value
        self._orref_is_ref: dict = {}    # field name -> bool, for OrRef fields
        self._ns_attrs: dict = {}        # (prefix, key) -> value, opaque or typed
        self._load_problems: list = []   # violations detected at load time (see _load_fields)
        self._parent_ref = None
        self._document_ref = None

    # -- backpointers --
    def get_parent(self):
        return self._parent_ref() if self._parent_ref else None

    def get_document(self):
        return self._document_ref() if self._document_ref else None

    def _attach(self, parent, document):
        self._parent_ref = weakref.ref(parent) if parent is not None else None
        self._document_ref = weakref.ref(document) if document is not None else None
        for child in self._children():
            child._attach(self, document)

    def _children(self):
        """Every SEDBase-derived child reachable from this element, for
        backpointer propagation and validate() recursion."""
        return []

    # -- universal name/description (TestBaseFields) --
    def get_name(self) -> str:
        if self._name is None:
            raise ApiError("name is not set")
        return self._name

    def is_set_name(self) -> bool:
        return self._name is not None

    def set_name(self, value: str) -> None:
        self._name = value

    def unset_name(self) -> None:
        self._name = None

    def get_description(self) -> str:
        if self._description is None:
            raise ApiError("description is not set")
        return self._description

    def is_set_description(self) -> bool:
        return self._description is not None

    def set_description(self, value: str) -> None:
        self._description = value

    def unset_description(self) -> None:
        self._description = None

    # -- generic namespace attribute store (Design.md's Namespaces section) --
    def get_namespace_attribute(self, prefix: str, key: str):
        try:
            return self._ns_attrs[(prefix, key)]
        except KeyError:
            raise ApiError(f"namespace attribute {prefix}@{key} is not set")

    def set_namespace_attribute(self, prefix: str, key: str, value) -> None:
        self._ns_attrs[(prefix, key)] = value

    def is_set_namespace_attribute(self, prefix: str, key: str) -> bool:
        return (prefix, key) in self._ns_attrs

    def unset_namespace_attribute(self, prefix: str, key: str) -> None:
        self._ns_attrs.pop((prefix, key), None)

    # -- generic OrRef-shaped storage helpers, used by generated accessors --
    def _get_orref_value(self, name):
        if name not in self._values:
            raise ApiError(f"{name} is not set")
        if self._orref_is_ref.get(name):
            raise ApiError(f"{name} holds a reference, not a literal value")
        return self._values[name]

    def _get_orref_ref(self, name):
        if name not in self._values:
            raise ApiError(f"{name} is not set")
        if not self._orref_is_ref.get(name):
            raise ApiError(f"{name} holds a literal value, not a reference")
        return self._values[name]

    def _set_orref_value(self, name, value):
        self._values[name] = value
        self._orref_is_ref[name] = False

    def _set_orref_ref(self, name, ref_str):
        if not is_reference(ref_str):
            raise ApiError(f"{ref_str!r} is not a valid reference (must start with '#')")
        self._values[name] = ref_str
        self._orref_is_ref[name] = True

    def _is_orref_ref(self, name):
        if name not in self._values:
            raise ApiError(f"{name} is not set")
        return bool(self._orref_is_ref.get(name))

    # -- clone --
    def clone(self):
        c = self.__class__()
        c._name = self._name
        c._description = self._description
        c._values = dict(self._values)
        c._orref_is_ref = dict(self._orref_is_ref)
        c._ns_attrs = dict(self._ns_attrs)
        return c

    # -- validate() engine --------------------------------------------------
    def validate(self, severity_at_least: str = "warning") -> list:
        problems = self._validate_own()
        seen = {(p.rule_id, p.location) for p in problems}
        for child, child_loc_prefix in self._children_with_locations():
            for p in child.validate(severity_at_least="warning"):
                p2 = ValidationProblem(p.rule_id, p.severity, p.rule, p.message,
                                        child_loc_prefix + p.location)
                key = (p2.rule_id, p2.location)
                if key in seen:
                    continue
                seen.add(key)
                problems.append(p2)
        order = {"warning": 0, "error": 1}
        threshold = order[severity_at_least]
        return [p for p in problems if order[p.severity] >= threshold]

    def _children_with_locations(self):
        """[(child_sedbase_instance, '/jsonPointerSegment'), ...] - override
        per concrete class. Default: none."""
        return []

    def _validate_own(self) -> list:
        # Extra/unrecognized properties (including bad-registered-namespace
        # keys), bad dict-of-discriminated-union keys, and item-dispatch
        # problems are all detected once, at load time, by the generated
        # _load_fields() - see Design.md's Schema-Pass Errors section. This
        # is the only reliable point to see genuinely-unrecognized raw JSON
        # keys, since they are never stored anywhere in the object itself.
        problems = list(self._load_problems)
        instance = self._own_json_value()
        # _type const (only meaningful when this class is validated directly,
        # e.g. not through a discriminator that already dispatched on it)
        if self._TYPE_CONST is not None and instance.get("_type") != self._TYPE_CONST \
                and self._TYPE_RULE_ID:
            problems.append(make_problem(
                self._TYPE_RULE_ID, "/_type", attr="_type",
                **{"class": self.__class__.__name__, "id": self._own_id_for_message(),
                   "value": instance.get("_type"), "allowed": self._TYPE_CONST}))
        # universal name/description mixin (TestBaseFields/SEDBaseFields) -
        # not a per-class FieldSpec, so checked directly here against the
        # base mixin's own rule IDs (the same on every concrete class).
        if self._name is not None and not leaf_value_ok("string", self._name):
            rid = self._NAME_RULE_ID or self._BASE_CATCHALL
            problems.append(make_problem(
                rid, "/name", attr="name",
                **{"class": self.__class__.__name__, "id": self._own_id_for_message(),
                   "value": self._name}))
        if self._description is not None and not leaf_value_ok("string", self._description):
            rid = self._DESC_RULE_ID or self._BASE_CATCHALL
            problems.append(make_problem(
                rid, "/description", attr="description",
                **{"class": self.__class__.__name__, "id": self._own_id_for_message(),
                   "value": self._description}))
        # required fields
        all_field_specs = list(self._FIELDS)
        for prefix, specs in self._NAMESPACE_FIELDS.items():
            all_field_specs = all_field_specs + specs
        for spec in all_field_specs:
            present = spec.name in instance
            if spec.required and not present:
                rid = spec.required_rule_id or spec.origin_catchall
                problems.append(make_problem(
                    rid, "/" + spec.name, attr=spec.name,
                    **{"class": self.__class__.__name__, "id": self._own_id_for_message()}))
                continue
            if not present:
                continue
            value = instance[spec.name]
            if spec.kind in LEAF_KINDS:
                if not leaf_value_ok(spec.kind, value, spec.minimum, spec.exclusive_minimum, spec.pattern):
                    rid = spec.rule_id or spec.origin_catchall
                    problems.append(make_problem(
                        rid, "/" + spec.name, attr=spec.name,
                        **{"class": self.__class__.__name__, "id": self._own_id_for_message(),
                           "value": value}))
        return problems

    def _own_id_for_message(self) -> str:
        return "?"

    def _own_json_value(self) -> dict:
        raise NotImplementedError

    def _allowed_keys(self) -> set:
        keys = {f.name for f in self._FIELDS}
        for specs in self._NAMESPACE_FIELDS.values():
            keys |= {f.name for f in specs}
        return keys


class IdKeyedCollection:
    """Backing store for an ID-keyed dict-of-discriminated-union field
    (TestDocument.widgets/.reports, FancyWidget.choices) - insertion order
    preserved, add-/remove-/insert-/rename (setId) per Design.md's Classes
    section."""

    def __init__(self, dispatch_fn):
        self._dispatch_fn = dispatch_fn  # (type_value) -> (class_or_None, is_unregistered_ns)
        self._order: list = []           # list of ids, in order
        self._items: dict = {}           # id -> SedBase instance

    def ids(self) -> list:
        return list(self._order)

    def get(self, item_id):
        if item_id not in self._items:
            raise ApiError(f"no entry with id {item_id!r}")
        return self._items[item_id]

    def add(self, item_id: str, obj) -> None:
        if item_id in self._items:
            raise ApiError(f"an entry with id {item_id!r} already exists")
        self._order.append(item_id)
        self._items[item_id] = obj

    def insert(self, index: int, item_id: str, obj) -> None:
        if item_id in self._items:
            raise ApiError(f"an entry with id {item_id!r} already exists")
        if not (0 <= index <= len(self._order)):
            raise ApiError(f"index {index} out of range")
        self._order.insert(index, item_id)
        self._items[item_id] = obj

    def remove(self, item_id: str) -> None:
        if item_id not in self._items:
            raise ApiError(f"no entry with id {item_id!r}")
        self._order.remove(item_id)
        del self._items[item_id]

    def set_id(self, old_id: str, new_id: str) -> None:
        if old_id not in self._items:
            raise ApiError(f"no entry with id {old_id!r}")
        if new_id in self._items and new_id != old_id:
            raise ApiError(f"an entry with id {new_id!r} already exists")
        idx = self._order.index(old_id)
        self._order[idx] = new_id
        self._items[new_id] = self._items.pop(old_id)

    def __len__(self):
        return len(self._order)


class ListCollection:
    """Backing store for a plain (non-ID-keyed) array-of-embedded-object
    field, e.g. WidgetOptions.notes: add- (append), remove- (by index),
    insert- (at index)."""

    def __init__(self):
        self._items: list = []

    def items(self) -> list:
        return list(self._items)

    def add(self, obj) -> None:
        self._items.append(obj)

    def insert(self, index: int, obj) -> None:
        if not (0 <= index <= len(self._items)):
            raise ApiError(f"index {index} out of range")
        self._items.insert(index, obj)

    def remove(self, index: int) -> None:
        if not (0 <= index < len(self._items)):
            raise ApiError(f"index {index} out of range")
        del self._items[index]

    def __len__(self):
        return len(self._items)

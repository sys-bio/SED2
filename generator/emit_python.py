"""Emit the generated Python target library (libsed2test) from a SpecModel.

Phase-1 scope (see Design.md's Testing / Classes sections): every rule in
test-specsheets/ has check: schema, so validate() is a schema pass plus the
Schema-Pass-Errors rule-ID mapping - no ref-type/handwritten rule dispatch,
no math grammar, no outputs.json shape inference (none of those patterns
appear in test-specsheets/). Real per-*field* type/pattern/const checks are
still run through the language's own real JSON Schema validator
(the `jsonschema` package here) against a tiny schema built from that one
field's already-resolved type - not against a whole-document schema - since
every combinator (allOf/oneOf) has already been resolved away by the
generator itself at compose time (see generator/spec.py). Required-field
presence and extra-property/namespace-key legality are plain structural
checks driven by the same generate-time metadata (x-required-rule-ids,
x-rule-id) rather than re-parsing the validator's own generic error text.
"""
from __future__ import annotations

import os
import re
from .spec import SpecModel, FieldType, Field, FlatClass

RUNTIME = r'''"""Shared runtime for the generated libsed2test package. GENERATED - do not
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
'''


def _pyname(name: str) -> str:
    """camelCase/PascalCase attribute name -> snake_case, namespace@key -> ns_key."""
    if "@" in name:
        prefix, key = name.split("@", 1)
        return f"{prefix}_{_pyname(key)}"
    s = re.sub(r"(?<!^)(?=[A-Z])", "_", name)
    return s.lower()


def emit_field_specs_literal(fields: list[Field]) -> str:
    parts = []
    for f in fields:
        t = f.type
        parts.append(
            "FieldSpec(%r, %r, %r, %r, %r, %r, minimum=%r, exclusive_minimum=%r, "
            "pattern=%r, item_class=%r, item_discriminator=%r)" % (
                f.name, t.kind, f.required, f.rule_id, f.required_rule_id,
                f"{f.origin_class}-0000", t.minimum, t.exclusive_minimum,
                t.pattern, t.item_class, t.item_discriminator,
            )
        )
    return "[" + ", ".join(parts) + "]"


def _leaf_accessors(cls_name: str, f: Field) -> str:
    py = _pyname(f.name)
    kind = f.type.kind
    lines = []
    if kind in ("StringOrRef", "NumberOrRef"):
        lines.append(f"    def get_{py}_value(self):\n        return self._get_orref_value({f.name!r})\n")
        lines.append(f"    def get_{py}_ref(self):\n        return self._get_orref_ref({f.name!r})\n")
        lines.append(f"    def set_{py}_value(self, value):\n        self._set_orref_value({f.name!r}, value)\n")
        lines.append(f"    def set_{py}_ref(self, ref):\n        self._set_orref_ref({f.name!r}, ref)\n")
        lines.append(f"    def is_{py}_ref(self):\n        return self._is_orref_ref({f.name!r})\n")
        lines.append(f"    def is_set_{py}(self):\n        return {f.name!r} in self._values\n")
        lines.append(f"    def unset_{py}(self):\n        self._values.pop({f.name!r}, None); self._orref_is_ref.pop({f.name!r}, None)\n")
    else:
        lines.append(f"    def get_{py}(self):\n        if {f.name!r} not in self._values: raise ApiError({py + ' is not set'!r})\n        return self._values[{f.name!r}]\n")
        lines.append(f"    def set_{py}(self, value):\n        self._values[{f.name!r}] = value\n")
        lines.append(f"    def is_set_{py}(self):\n        return {f.name!r} in self._values\n")
        lines.append(f"    def unset_{py}(self):\n        self._values.pop({f.name!r}, None)\n")
    return "\n".join(lines)


def _collection_accessors(f: Field, model: SpecModel) -> str:
    py = _pyname(f.name)
    t = f.type
    lines = []
    if t.kind == "dict":
        disc = t.item_discriminator
        lines.append(f"    def get_{py}(self):\n        return self._{py}.ids()\n")
        lines.append(f"    def get_{py}_item(self, item_id):\n        return self._{py}.get(item_id)\n")
        lines.append(f"    def add_{py}(self, item_id, obj):\n        self._{py}.add(item_id, obj); obj._attach(self, self.get_document())\n")
        lines.append(f"    def insert_{py}(self, index, item_id, obj):\n        self._{py}.insert(index, item_id, obj); obj._attach(self, self.get_document())\n")
        lines.append(f"    def remove_{py}(self, item_id):\n        self._{py}.remove(item_id)\n")
        lines.append(f"    def set_id_on_{py}(self, old_id, new_id):\n        self._{py}.set_id(old_id, new_id)\n")
    elif t.kind == "array":
        lines.append(f"    def get_{py}(self):\n        return self._{py}.items()\n")
        lines.append(f"    def add_{py}(self, obj):\n        self._{py}.add(obj); obj._attach(self, self.get_document())\n")
        lines.append(f"    def insert_{py}(self, index, obj):\n        self._{py}.insert(index, obj); obj._attach(self, self.get_document())\n")
        lines.append(f"    def remove_{py}(self, index):\n        self._{py}.remove(index)\n")
    return "\n".join(lines)


def _dispatch_fn_name(disc_name: str) -> str:
    return f"_dispatch_{disc_name}"


def emit_model_py(model: SpecModel) -> str:
    out = []
    out.append('"""Generated concrete SED2 classes for libsed2test. GENERATED - do not\n'
                'hand-edit; regenerate from test-specsheets/ via generator/generate.py."""\n'
                "from __future__ import annotations\n\n"
                "from ._runtime import (SedBase, FieldSpec, ApiError, IdKeyedCollection,\n"
                "                       ListCollection, make_problem, ValidationProblem,\n"
                "                       is_reference, SID_PATTERN, NAMESPACE_KEY_PATTERN)\n\n")

    gen_names = model.generatable_classes()
    base = model.base_mixin
    base_fields = model.classes[base].fields if base in model.classes else []
    base_name_rule_id = next((f.rule_id for f in base_fields if f.name == "name"), None)
    base_desc_rule_id = next((f.rule_id for f in base_fields if f.name == "description"), None)
    base_catchall = model.classes[base].own_catchall if base in model.classes else ""

    # -- unknown-class holders, one per discriminator --------------------
    for disc_name, disc in model.discriminators.items():
        uname = disc.unknown_class_name
        out.append(f'class {uname}(SedBase):\n'
                    f'    """Opaque holder for a {disc_name} instance whose _type names an\n'
                    f'    unregistered namespace prefix (see Design.md\'s Namespaces section) -\n'
                    f'    round-trips unchanged, never itself a validation error."""\n'
                    f"    def __init__(self, type_value, raw: dict):\n"
                    f"        super().__init__()\n"
                    f"        self._type_value = type_value\n"
                    f"        self._raw = dict(raw)\n\n"
                    f"    def get_type(self):\n"
                    f"        return self._type_value\n\n"
                    f"    def _own_json_value(self):\n"
                    f"        return self._raw\n\n"
                    f"    def _allowed_keys(self):\n"
                    f"        return set(self._raw.keys())\n\n"
                    f"    def _validate_own(self):\n"
                    f"        return []\n\n"
                    f"    def to_json_value(self):\n"
                    f"        d = dict(self._raw)\n"
                    f"        if self._name is not None: d['name'] = self._name\n"
                    f"        if self._description is not None: d['description'] = self._description\n"
                    f"        return d\n\n\n")

    # -- concrete classes --------------------------------------------------
    for name in gen_names:
        c = model.classes[name]
        own_fields = [f for f in c.fields if f.origin_class != base]
        collection_fields = [f for f in own_fields if f.type.kind in ("dict", "array")]
        leaf_fields = [f for f in own_fields if f.type.kind in ("StringOrRef", "NumberOrRef", "string",
                                                                  "integer", "number", "boolean", "SId", "SIdRef")]
        ns_field_lits = {p: emit_field_specs_literal(fs) for p, fs in c.namespace_updates.items()}

        out.append(f"class {name}(SedBase):\n")
        doc = f'    """Generated from test-specsheets/{c.category}/{name}/."""\n'
        out.append(doc)
        out.append(f"    _FIELDS = {emit_field_specs_literal(leaf_fields + [f for f in collection_fields])}\n")
        out.append(f"    _REQUIRED_NAMES = {{{', '.join(repr(f.name) for f in own_fields if f.required)}}}\n")
        out.append(f"    _TYPE_CONST = {c.type_const!r}\n")
        out.append(f"    _TYPE_RULE_ID = {c.type_rule_id!r}\n")
        out.append(f"    _OWN_CATCHALL = {c.own_catchall!r}\n")
        out.append(f"    _NAME_RULE_ID = {base_name_rule_id!r}\n")
        out.append(f"    _DESC_RULE_ID = {base_desc_rule_id!r}\n")
        out.append(f"    _BASE_CATCHALL = {base_catchall!r}\n")
        if ns_field_lits:
            items = ", ".join(f"{p!r}: {lit}" for p, lit in ns_field_lits.items())
            out.append(f"    _NAMESPACE_FIELDS = {{{items}}}\n")
            items2 = ", ".join(f"{p!r}: {c.namespace_catchalls[p]!r}" for p in ns_field_lits)
            out.append(f"    _NAMESPACE_CATCHALL = {{{items2}}}\n")
            out.append(f"    _KNOWN_NAMESPACE_PREFIXES = {{{', '.join(repr(p) for p in ns_field_lits)}}}\n")
        else:
            out.append("    _NAMESPACE_FIELDS = {}\n")
            out.append("    _NAMESPACE_CATCHALL = {}\n")

        out.append("\n    def __init__(self):\n        super().__init__()\n")
        for f in collection_fields:
            py = _pyname(f.name)
            if f.type.kind == "dict":
                out.append(f"        self._{py} = IdKeyedCollection({_dispatch_fn_name(f.type.item_discriminator)})\n")
            else:
                out.append(f"        self._{py} = ListCollection()\n")
        for p, fs in c.namespace_updates.items():
            pass  # namespace fields stored in the same self._values dict, no init needed
        out.append("\n")

        if c.type_const is not None:
            out.append(f"    def get_type(self):\n        return {c.type_const!r}\n\n")

        for f in leaf_fields:
            out.append(_leaf_accessors(name, f) + "\n")
        for f in collection_fields:
            out.append(_collection_accessors(f, model) + "\n")

        # namespace-typed convenience accessors
        for prefix, fs in c.namespace_updates.items():
            for f in fs:
                out.append(_namespace_accessor(prefix, f))

        out.append(f"    def _children(self):\n        kids = []\n")
        for f in collection_fields:
            py = _pyname(f.name)
            if f.type.kind == "dict":
                out.append(f"        kids.extend(self._{py}.get(i) for i in self._{py}.ids())\n")
            else:
                out.append(f"        kids.extend(self._{py}.items())\n")
        out.append("        return kids\n\n")

        out.append(f"    def _children_with_locations(self):\n        out = []\n")
        for f in collection_fields:
            py = _pyname(f.name)
            if f.type.kind == "dict":
                out.append(f"        for i in self._{py}.ids():\n            out.append((self._{py}.get(i), '/{f.name}/' + i))\n")
            else:
                out.append(f"        for idx, item in enumerate(self._{py}.items()):\n            out.append((item, '/{f.name}/%d' % idx))\n")
        out.append("        return out\n\n")

        out.append(f"    def _own_id_for_message(self):\n        p = self.get_parent()\n        return '?'\n\n")

        out.append("    def _own_json_value(self):\n        d = {}\n")
        out.append("        if self._name is not None: d['name'] = self._name\n")
        out.append("        if self._description is not None: d['description'] = self._description\n")
        if c.type_const is not None:
            out.append(f"        d['_type'] = self._values.get('_type', {c.type_const!r})\n")
        for f in leaf_fields:
            out.append(f"        if {f.name!r} in self._values: d[{f.name!r}] = self._values[{f.name!r}]\n")
        for prefix, fs in c.namespace_updates.items():
            for f in fs:
                out.append(f"        if {f.name!r} in self._values: d[{f.name!r}] = self._values[{f.name!r}]\n")
        for f in collection_fields:
            py = _pyname(f.name)
            if f.type.kind == "dict":
                out.append(f"        if len(self._{py}): d[{f.name!r}] = {{i: self._{py}.get(i).to_json_value() for i in self._{py}.ids()}}\n")
            else:
                out.append(f"        if len(self._{py}): d[{f.name!r}] = [it.to_json_value() for it in self._{py}.items()]\n")
        for (pfx, key), _ in []:
            pass
        out.append("        for (pfx, key), value in self._ns_attrs.items():\n")
        out.append("            d[f'{pfx}@{key}'] = value\n")
        out.append("        return d\n\n")
        out.append("    def to_json_value(self):\n        return self._own_json_value()\n\n\n")

    # -- from_json_value / dispatch functions per discriminator -----------
    for disc_name, disc in model.discriminators.items():
        uname = disc.unknown_class_name
        out.append(f"def _dispatch_{disc_name}(type_value):\n")
        out.append(f"    branches = {{\n")
        for tc, br in disc.branches.items():
            out.append(f"        {tc!r}: {br.class_name},\n")
        out.append("    }\n")
        out.append("    return branches.get(type_value)\n\n\n")

        out.append(f"def parse_{disc_name}(raw: dict):\n")
        out.append(f"    \"\"\"Returns (obj, problem_or_None). obj is None only when _type is\n"
                    f"    entirely absent; an unrecognized-but-registered or bare-unrecognized\n"
                    f"    _type still returns an {uname} holder plus a violation - an\n"
                    f"    unregistered-namespace _type returns one with no violation at all.\n"
                    f"    See Design.md's Namespaces / Schema-Pass Errors sections.\"\"\"\n")
        out.append("    if '_type' not in raw:\n")
        if disc.missing_type_rule_id:
            out.append(f"        return None, make_problem({disc.missing_type_rule_id!r}, '')\n")
        else:
            out.append(f"        return None, make_problem({disc_name + '-0000'!r}, '', **{{'schema-message': 'missing _type'}})\n")
        out.append("    tv = raw['_type']\n")
        out.append(f"    cls = _dispatch_{disc_name}(tv)\n")
        out.append("    if cls is not None:\n")
        out.append("        obj = cls()\n")
        out.append("        _load_fields(obj, raw)\n")
        out.append("        return obj, None\n")
        out.append("    from ._runtime import NAMESPACE_KEY_PATTERN\n")
        out.append("    m = NAMESPACE_KEY_PATTERN.match(tv) if isinstance(tv, str) else None\n")
        out.append(f"    known = {{{', '.join(repr(b.namespace) for b in disc.branches.values() if b.namespace)}}} \n")
        out.append("    if m and m.group(1) not in known:\n")
        out.append(f"        return {uname}(tv, raw), None\n")
        out.append(f"    return {uname}(tv, raw), make_problem({disc_name + '-0000'!r}, '', **{{'schema-message': f'unrecognized _type {{tv!r}}'}})\n\n\n")

    # -- generic field loader (used by parse_* and TestDocument.from_json) --
    # All load-time violations (extra/unrecognized properties, bad
    # dict-of-discriminated-union keys, bad container shapes, and dispatch
    # problems bubbled up from a nested item) are appended straight onto
    # obj._load_problems - this is the only point that sees the raw JSON
    # before unrecognized keys are dropped, so it's the only reliable place
    # to detect them (see Design.md's Schema-Pass Errors section).
    out.append("def _load_fields(obj, raw: dict):\n")
    out.append("    if 'name' in raw: obj.set_name(raw['name'])\n")
    out.append("    if 'description' in raw: obj.set_description(raw['description'])\n")
    out.append("    if '_type' in raw: obj._values['_type'] = raw['_type']\n")
    out.append("    for spec in obj._FIELDS:\n")
    out.append("        if spec.name not in raw or spec.kind in ('dict', 'array'):\n")
    out.append("            continue\n")
    out.append("        v = raw[spec.name]\n")
    out.append("        if spec.kind in ('StringOrRef', 'NumberOrRef'):\n")
    out.append("            if is_reference(v):\n")
    out.append("                obj._set_orref_ref(spec.name, v)\n")
    out.append("            else:\n")
    out.append("                obj._set_orref_value(spec.name, v)\n")
    out.append("        else:\n")
    out.append("            obj._values[spec.name] = v\n")
    out.append("    for prefix, specs in obj._NAMESPACE_FIELDS.items():\n")
    out.append("        for spec in specs:\n")
    out.append("            if spec.name in raw:\n")
    out.append("                obj._values[spec.name] = raw[spec.name]\n")
    out.append("    allowed = obj._allowed_keys()\n")
    out.append("    for key, value in raw.items():\n")
    out.append("        if key in ('_type', 'name', 'description'):\n")
    out.append("            continue\n")
    out.append("        if key in allowed:\n")
    out.append("            continue\n")
    out.append("        m = NAMESPACE_KEY_PATTERN.match(key)\n")
    out.append("        if m:\n")
    out.append("            prefix, ns_key = m.group(1), m.group(2)\n")
    out.append("            obj.set_namespace_attribute(prefix, ns_key, value)\n")
    out.append("            if prefix in obj._KNOWN_NAMESPACE_PREFIXES:\n")
    out.append("                catchall = obj._NAMESPACE_CATCHALL.get(prefix, obj._OWN_CATCHALL)\n")
    out.append("                obj._load_problems.append(make_problem(catchall, '', **{\n")
    out.append("                    'schema-message': f\"Additional property '{key}' is not allowed.\"}))\n")
    out.append("            continue\n")
    out.append("        obj._load_problems.append(make_problem(obj._OWN_CATCHALL, '', **{\n")
    out.append("            'schema-message': f\"Additional property '{key}' is not allowed.\"}))\n")
    out.append("    for spec in obj._FIELDS:\n")
    out.append("        if spec.kind == 'dict' and spec.name in raw:\n")
    out.append("            raw_value = raw[spec.name]\n")
    out.append("            if not isinstance(raw_value, dict):\n")
    out.append("                rid = spec.rule_id or spec.origin_catchall\n")
    out.append("                obj._load_problems.append(make_problem(rid, '/' + spec.name, **{\n")
    out.append("                    'attr': spec.name, 'class': obj.__class__.__name__,\n")
    out.append("                    'id': obj._own_id_for_message(), 'value': raw_value}))\n")
    out.append("                continue\n")
    out.append("            coll = getattr(obj, '_' + _pyname(spec.name))\n")
    out.append(f"            dispatch = globals()['parse_' + spec.item_discriminator]\n")
    out.append("            for item_id, item_raw in raw_value.items():\n")
    out.append("                if not SID_PATTERN.match(item_id):\n")
    out.append("                    rid = spec.rule_id or spec.origin_catchall\n")
    out.append("                    obj._load_problems.append(make_problem(rid, '/' + spec.name, **{\n")
    out.append("                        'attr': spec.name, 'class': obj.__class__.__name__,\n")
    out.append("                        'id': obj._own_id_for_message(), 'value': item_id}))\n")
    out.append("                child, problem = dispatch(item_raw)\n")
    out.append("                if problem is not None:\n")
    out.append("                    obj._load_problems.append(problem)\n")
    out.append("                if child is not None:\n")
    out.append("                    coll.add(item_id, child)\n")
    out.append("        elif spec.kind == 'array' and spec.name in raw:\n")
    out.append("            raw_value = raw[spec.name]\n")
    out.append("            if not isinstance(raw_value, list):\n")
    out.append("                rid = spec.rule_id or spec.origin_catchall\n")
    out.append("                obj._load_problems.append(make_problem(rid, '/' + spec.name, **{\n")
    out.append("                    'attr': spec.name, 'class': obj.__class__.__name__,\n")
    out.append("                    'id': obj._own_id_for_message(), 'value': raw_value}))\n")
    out.append("                continue\n")
    out.append("            coll = getattr(obj, '_' + _pyname(spec.name))\n")
    out.append(f"            item_cls = globals()[spec.item_class]\n")
    out.append("            for item_raw in raw_value:\n")
    out.append("                child = item_cls()\n")
    out.append("                _load_fields(child, item_raw)\n")
    out.append("                coll.add(child)\n")
    out.append("\n\n")
    out.append(f"def _pyname(name):\n")
    out.append("    import re as _re2\n")
    out.append("    if '@' in name:\n")
    out.append("        p, k = name.split('@', 1)\n")
    out.append("        return p + '_' + _pyname(k)\n")
    out.append("    return _re2.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()\n")

    return "".join(out)


def _namespace_accessor(prefix: str, f: Field) -> str:
    py = _pyname(f.name)
    if f.type.kind in ("StringOrRef", "NumberOrRef"):
        return (
            f"    def get_{py}_value(self):\n        return self._get_orref_value({f.name!r})\n"
            f"    def get_{py}_ref(self):\n        return self._get_orref_ref({f.name!r})\n"
            f"    def set_{py}_value(self, value):\n        self._set_orref_value({f.name!r}, value)\n"
            f"    def set_{py}_ref(self, ref):\n        self._set_orref_ref({f.name!r}, ref)\n"
            f"    def is_{py}_ref(self):\n        return self._is_orref_ref({f.name!r})\n"
            f"    def is_set_{py}(self):\n        return {f.name!r} in self._values\n"
            f"    def unset_{py}(self):\n        self._values.pop({f.name!r}, None)\n\n"
        )
    return (
        f"    def get_{py}(self):\n        if {f.name!r} not in self._values: raise ApiError({py + ' is not set'!r})\n        return self._values[{f.name!r}]\n"
        f"    def set_{py}(self, value):\n        self._values[{f.name!r}] = value\n"
        f"    def is_set_{py}(self):\n        return {f.name!r} in self._values\n"
        f"    def unset_{py}(self):\n        self._values.pop({f.name!r}, None)\n\n"
    )


def emit_rules_data_py(model: SpecModel) -> str:
    lines = ["\"\"\"Generated rule catalogue for libsed2test. GENERATED - do not hand-edit.\"\"\"",
             "from ._runtime import RULE_CATALOG", ""]
    lines.append("RULE_CATALOG.update({")
    for rid, r in sorted(model.rules.items()):
        lines.append(f"    {rid!r}: ({r.rule!r}, {r.message!r}, {r.severity!r}),")
    lines.append("})")
    return "\n".join(lines) + "\n"


def emit_document_helpers(model: SpecModel) -> str:
    doc_name = model.document_class
    return f'''"""Top-level read/write entry points for libsed2test. GENERATED."""
from __future__ import annotations
import json
from .model import {doc_name}, _load_fields


def read_from_string(text: str) -> "{doc_name}":
    raw = json.loads(text)
    obj = {doc_name}()
    _load_fields(obj, raw)
    obj._attach(None, obj)
    return obj


def read_from_file(path: str) -> "{doc_name}":
    with open(path, "r", encoding="utf-8") as f:
        return read_from_string(f.read())


def write_to_string(doc: "{doc_name}") -> str:
    return json.dumps(doc.to_json_value(), indent=2)


def write_to_file(doc: "{doc_name}", path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(write_to_string(doc))
'''


def emit_init_py(model: SpecModel) -> str:
    doc_name = model.document_class
    names = model.generatable_classes()
    return (
        '"""libsed2test - generated SED2 test-fixture library (Python target).\n'
        'GENERATED by generator/generate.py from test-specsheets/. Do not hand-edit."""\n'
        "from . import rules_data  # noqa: F401  (populates RULE_CATALOG on import)\n"
        f"from .model import {', '.join(names)}\n"
        f"from .io import read_from_string, read_from_file, write_to_string, write_to_file\n"
        "from ._runtime import ApiError, ValidationProblem\n\n"
        f"__all__ = {names + ['read_from_string', 'read_from_file', 'write_to_string', 'write_to_file', 'ApiError', 'ValidationProblem']!r}\n"
    )


def emit_python_package(model: SpecModel, out_dir: str) -> None:
    pkg_dir = os.path.join(out_dir, "src", "libsed2test")
    os.makedirs(pkg_dir, exist_ok=True)
    with open(os.path.join(pkg_dir, "_runtime.py"), "w") as f:
        f.write(RUNTIME)
    with open(os.path.join(pkg_dir, "rules_data.py"), "w") as f:
        f.write(emit_rules_data_py(model))
    with open(os.path.join(pkg_dir, "model.py"), "w") as f:
        f.write(emit_model_py(model))
    with open(os.path.join(pkg_dir, "io.py"), "w") as f:
        f.write(emit_document_helpers(model))
    with open(os.path.join(pkg_dir, "__init__.py"), "w") as f:
        f.write(emit_init_py(model))
    pyproject = '''[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "libsed2test"
version = "0.1.0"
description = "Generated SED2 test-fixture library (Python target) - exercises the SED2 generator against test-specsheets/, see Design.md's Testing section."
requires-python = ">=3.10"
dependencies = ["jsonschema>=4.18"]

[tool.setuptools.packages.find]
where = ["src"]
'''
    with open(os.path.join(out_dir, "pyproject.toml"), "w") as f:
        f.write(pyproject)

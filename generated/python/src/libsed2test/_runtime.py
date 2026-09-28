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


# ---- reference parsing/resolution (Design.md's Cross-references section, ---
# core-spec.md Section 4 / core/Types/v1.0.0/description.md's "References"
# paragraph). A reference is '#' + a colon-delimited containment path + an
# optional chain of dot-accessors/bracket-indices, e.g.
# "#tasks:loop1:subTasks:sim1.model['S1']". _parse_reference is pure syntax
# (never touches a document); get_sed_reference walks a parsed reference's
# containment path against an actual document (SEDBase-0006) to the target
# SedBase element, the getSEDReference() Design.md names. Neither one
# resolves the trailing dot-accessor/index chain against outputs.json -
# that's SEDBase-0008 through -0015's concern (hasSubvalue()-style
# plausibility, not yet implemented - see Task #10's tracked scope), so
# .accessors is parsed and carried but not yet interpreted here.
_REF_COLLECTIONS = ("tasks", "constants", "outputs", "styles")


@dataclass
class RefIndex:
    kind: str            # 'int' | 'label' | 'range'
    value: Any            # int | str | (int_or_None, int_or_None)


@dataclass
class ParsedReference:
    raw: str
    collection: Optional[str]      # the segment right after '#', or None if empty
    path: list                     # colon-segments after the collection
    accessors: list                # [('dot', name), ('index', RefIndex), ...] in order


def _parse_ref_index(part: str) -> RefIndex:
    part = part.strip()
    if ":" in part:
        a, b = part.split(":", 1)
        a = int(a) if a.strip() else None
        b = int(b) if b.strip() else None
        return RefIndex("range", (a, b))
    if len(part) >= 2 and part[0] == part[-1] and part[0] in ("'", '"'):
        return RefIndex("label", part[1:-1])
    try:
        return RefIndex("int", int(part))
    except ValueError:
        return RefIndex("label", part)  # bare unquoted label - lenient fallback


def _parse_reference(text: str) -> ParsedReference:
    body = text[1:] if text.startswith("#") else text
    m = re.search(r"[.\[]", body)
    path_part = body[: m.start()] if m else body
    accessor_part = body[m.start():] if m else ""
    segments = path_part.split(":") if path_part else []
    collection = segments[0] if segments else None
    path = segments[1:]
    accessors: list = []
    i, n = 0, len(accessor_part)
    while i < n:
        ch = accessor_part[i]
        if ch == ".":
            mm = re.match(r"\.([A-Za-z_][A-Za-z0-9_]*)", accessor_part[i:])
            if not mm:
                break
            accessors.append(("dot", mm.group(1)))
            i += mm.end()
        elif ch == "[":
            close = accessor_part.find("]", i)
            if close == -1:
                break
            inner = accessor_part[i + 1 : close]
            for part in inner.split(","):
                if part.strip():
                    accessors.append(("index", _parse_ref_index(part)))
            i = close + 1
        else:
            break
    return ParsedReference(raw=text, collection=collection, path=path, accessors=accessors)


def get_sed_reference(document, parsed: ParsedReference):
    """Walks parsed.path's containment tree against `document` one
    colon-segment at a time (SEDBase-0006). Returns (element, resolved_path)
    on success - resolved_path is the '#...'-prefixed string of everything
    walked - or (None, longest_resolved_prefix) on failure, per SEDBase-0006's
    own spec ("the longest prefix that failed to resolve"). Returns
    (None, None) outright when there's no document to walk (e.g. a class
    validated directly, never attached to one) or the collection name itself
    is unrecognized (SEDBase-0005's own concern, not this rule's)."""
    if document is None or parsed.collection not in _REF_COLLECTIONS:
        return None, None
    coll = document._get_id_collection(parsed.collection)
    prefix = "#" + parsed.collection
    if coll is None or not parsed.path:
        return None, prefix
    remaining = list(parsed.path)
    first_id = remaining.pop(0)
    if first_id not in coll.ids():
        return None, prefix
    current = coll.get(first_id)
    prefix = prefix + ":" + first_id
    while remaining:
        if len(remaining) < 2:
            # A lone trailing segment names a plain attribute, not an
            # ID-keyed child collection - SEDBase-0006: "a segment naming a
            # plain attribute... does not resolve".
            return None, prefix
        subcoll_name, item_id = remaining.pop(0), remaining.pop(0)
        subcoll = current._get_id_collection(subcoll_name)
        if subcoll is None or item_id not in subcoll.ids():
            return None, prefix
        current = subcoll.get(item_id)
        prefix = prefix + ":" + subcoll_name + ":" + item_id
    return current, prefix


def _check_reference_field(value, *, document, class_name, id_value, attr, location) -> list:
    """Shared per-type dispatcher for the reference-resolution rules
    (SEDBase-0005 through -0007 so far - see Task #10's tracked scope for
    -0008 through -0015, which need outputs.json and aren't implemented
    yet). Called for every SIdRef/*OrRef-kind field whose value is a
    reference (is_reference(value)); mirrors _check_math_field's shape and
    local-import-to-avoid-circularity convention (see its own docstring)."""
    try:
        from ._rules import sedbase_0005, sedbase_0006, sedbase_0007
    except ImportError:
        # This tree's own model.rules never defined SEDBase-0005 (see
        # _copy_handwritten_rules_py's docstring) - its own reference
        # convention (if it has one at all) isn't the tasks/constants/
        # outputs/styles vocabulary these rules check, so skip rather
        # than misapply a foreign convention or crash.
        return []

    parsed = _parse_reference(value)
    kwargs = dict(class_name=class_name, id_value=id_value, attr=attr, location=location,
                  make_problem=make_problem)
    problems = sedbase_0005.check(parsed, **kwargs)
    if problems:
        return problems  # unknown collection - nothing further can resolve
    problems = problems + sedbase_0007.check(parsed, **kwargs)
    resolved, resolved_prefix = get_sed_reference(document, parsed)
    problems = problems + sedbase_0006.check(parsed, resolved, resolved_prefix, **kwargs)
    return problems


def _check_math_field(value, *, class_name, id_value, attr, location) -> list:
    """Shared per-type dispatcher for the math-grammar rules (Types-0001
    through Types-0004 - Design.md's Validation section: "a rule filed
    under SEDBase or Types that applies wherever a field of a given
    declared type occurs... is called from a shared per-type helper that
    every class's generated validate() invokes automatically for each of
    its own fields of that type"). Called only for a FieldSpec with
    is_math=True, and only when its value is a literal string - never a
    reference: per Types-0001.md, "When the math attribute is itself a
    reference, this and the following math rules... apply only if the
    reference resolves statically to a string constant", which is out of
    scope until reference resolution exists (Design.md's Cross-references
    section), so a referenced math field is silently skipped here.

    The four templates/python/rules/Types-000N.py files (copied verbatim
    into ._rules/ at generate time - see Design.md's "fixed function-name
    convention, not a spliced fragment") take every collaborator they need
    as a keyword argument rather than importing this module themselves, so
    each stays independently callable and testable in isolation; this
    function is the only place that wires them together. The imports below
    are local (not at module level) to avoid a circular import, since
    ._rules/*.py and ._predefined_functions.py both exist only once this
    module has already finished loading."""
    from . import math_ast as _math_ast
    from ._predefined_functions import FUNCTIONS, CONSTANTS
    try:
        from ._rules import types_0001, types_0002, types_0003, types_0004
    except ImportError:
        # This tree's own model.rules never defined Types-0001 (see
        # _copy_handwritten_rules_py's docstring) - is_math should never be
        # True anywhere in that case, but degrade to a no-op rather than
        # crash if it somehow is.
        return []

    problems = types_0001.check(
        value, class_name=class_name, id_value=id_value, attr=attr, location=location,
        make_problem=make_problem, math_parse=_math_ast.parse,
        MathSyntaxError=_math_ast.MathSyntaxError)
    if problems:
        return problems  # unparseable - nothing left to walk for 0002-0004
    ast = _math_ast.parse(value)
    problems = problems + types_0002.check(
        ast, class_name=class_name, id_value=id_value, attr=attr, location=location,
        make_problem=make_problem, functions=FUNCTIONS)
    problems = problems + types_0003.check(
        ast, class_name=class_name, id_value=id_value, attr=attr, location=location,
        make_problem=make_problem, functions=FUNCTIONS)
    problems = problems + types_0004.check(
        ast, class_name=class_name, id_value=id_value, attr=attr, location=location,
        make_problem=make_problem, constants=CONSTANTS)
    return problems


def _walk_with_locations(obj, prefix=""):
    """Yields (descendant, absolute_location) for obj itself and every
    SedBase-derived descendant reachable through _children_with_locations(),
    depth-first - the same recursion validate() itself uses to build each
    problem's own location, reused here for the whole-document namespace
    scan below, which needs to inspect every node's own raw _type/_ns_attrs
    directly rather than just collect the ValidationProblems each node's own
    validate() call would already report. An any-dict field's raw-JSON
    entries are never yielded (they're excluded from _children_with_
    locations() already - see emit_model_py's any-dict branch), which is
    correct here too: an opaque stored value can't itself carry a namespace-
    prefixed attribute key or _type in the schema's own sense."""
    yield obj, prefix
    for child, child_loc in obj._children_with_locations():
        yield from _walk_with_locations(child, prefix + child_loc)


def _check_namespace_usage_and_version(document) -> list:
    """SEDDocument-0009 through -0011 (Design.md's Namespaces/Versioning
    sections) - whole-document checks, called once from _validate_own when
    _IS_DOCUMENT_CLASS is set (see there), matching Design.md's Validation
    section: "a rule filed under SEDDocument that needs the whole document
    ... is called once, from SEDDocument's own validate()". Degrades to a
    no-op tree-wide when this tree's own model.rules never defined
    SEDDocument-0009 (e.g. test-specsheets' TestDocument, which has no
    namespace/version rules of its own), matching every other handwritten-
    rule dispatcher's ImportError guard in this module (see
    _check_math_field/_check_reference_field)."""
    try:
        from ._rules import seddocument_0009, seddocument_0010, seddocument_0011
    except ImportError:
        return []

    # "used" means any attribute key or _type value of the form
    # prefix@identifier, anywhere in the document (SEDDocument-0009.md) -
    # registered and unregistered prefixes alike. The <prefix>@version
    # declaration itself (only ever stored on the document root) doesn't
    # count as a use of that prefix.
    declared = {}   # prefix -> "/<prefix>@version" (its own declaration site)
    for (pfx, key) in document._ns_attrs:
        if key == "version":
            declared[pfx] = f"/{pfx}@version"

    used = {}       # prefix -> [locations]
    for obj, loc in _walk_with_locations(document):
        for (pfx, key) in obj._ns_attrs:
            if obj is document and key == "version":
                continue
            used.setdefault(pfx, []).append(f"{loc}/{pfx}@{key}")
        if hasattr(obj, "get_type"):
            type_value = obj.get_type()
            if isinstance(type_value, str) and "@" in type_value:
                used.setdefault(type_value.split("@", 1)[0], []).append(f"{loc}/_type")

    problems = []
    for pfx, locations in used.items():
        if pfx in declared:
            continue
        for loc in locations:
            problems.extend(seddocument_0009.check(prefix=pfx, location=loc, make_problem=make_problem))
    for pfx, loc in declared.items():
        if pfx not in used:
            problems.extend(seddocument_0010.check(prefix=pfx, location=loc, make_problem=make_problem))
    problems.extend(seddocument_0011.check(document=document, make_problem=make_problem))
    return problems


def _check_constants_ordering(document) -> list:
    """SEDDocument-0013 (Design.md's Validation section scoping paragraph:
    "SEDDocument's own... constant-ordering... checks" are call-once-from-
    SEDDocument handwritten rules) - degrades to a no-op the same way as
    every other handwritten-rule dispatcher when this tree's own model.rules
    never defined SEDDocument-0013 (e.g. test-specsheets' TestDocument)."""
    try:
        from ._rules import seddocument_0013
    except ImportError:
        return []
    return seddocument_0013.check(
        document=document, make_problem=make_problem,
        is_reference=is_reference, parse_reference=_parse_reference)


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
    "IntegerOrRef": {"anyOf": [{"type": "integer"}, {"type": "string", "pattern": SIDREF_PATTERN.pattern}]},
    "BooleanOrRef": {"anyOf": [{"type": "boolean"}, {"type": "string", "pattern": SIDREF_PATTERN.pattern}]},
    "ArrayOrRef": {"anyOf": [{"type": "array"}, {"type": "string", "pattern": SIDREF_PATTERN.pattern}]},
    "DictOrRef": {"anyOf": [{"type": "object"}, {"type": "string", "pattern": SIDREF_PATTERN.pattern}]},
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
                 "item_class", "item_discriminator", "is_math")

    def __init__(self, name, kind, required, rule_id, required_rule_id,
                 origin_catchall, minimum=None, exclusive_minimum=None,
                 pattern=None, item_class=None, item_discriminator=None,
                 is_math=False):
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
        self.is_math = is_math


LEAF_KINDS = {"string", "integer", "number", "boolean", "SId", "SIdRef", "StringOrRef", "NumberOrRef",
              "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef"}

# Every LEAF_KINDS member whose value can structurally BE a reference (a
# plain "string"/"integer"/etc. field's schema never admits one) - SIdRef is
# always a reference, and every *OrRef kind's own anyOf includes one (see
# _LEAF_SCHEMAS). Drives _check_reference_field's dispatch in _validate_own
# below (SEDBase-0005 through -0007 so far).
_REFERENCE_CAPABLE_KINDS = {"SIdRef", "StringOrRef", "NumberOrRef", "IntegerOrRef",
                            "BooleanOrRef", "ArrayOrRef", "DictOrRef"}


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
    # True only on the generated document root class (SEDDocument/
    # TestDocument/...) - gates the whole-document checks (SEDDocument-0009
    # through -0011: namespace-usage-vs-declared-version, version-newer-
    # than-known) in _validate_own below, which only make sense run once,
    # from the document root, never per-node (Design.md's Validation
    # section: "a rule filed under SEDDocument that needs the whole
    # document... is called once, from SEDDocument's own validate()").
    _IS_DOCUMENT_CLASS: bool = False
    _MAX_KNOWN_DOCUMENT_VERSION: Optional[str] = None
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

    def _get_id_collection(self, field_name):
        """Default for classes with no ID-keyed collection fields at all
        (namespace-unknown holders, leaf classes) - every generated concrete
        class overrides this with its own dict-kind/any-dict-kind fields
        (see emit_model_py). Used by get_sed_reference()'s containment-tree
        walk (SEDBase-0006)."""
        return None

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
                elif spec.kind in _REFERENCE_CAPABLE_KINDS and is_reference(value):
                    problems.extend(_check_reference_field(
                        value, document=self.get_document(), class_name=self.__class__.__name__,
                        id_value=self._own_id_for_message(), attr=spec.name, location="/" + spec.name))
                elif spec.is_math and isinstance(value, str):
                    problems.extend(_check_math_field(
                        value, class_name=self.__class__.__name__, id_value=self._own_id_for_message(),
                        attr=spec.name, location="/" + spec.name))
            elif spec.kind == "any" and is_reference(value):
                # A scalar AnyValueOrRef field (e.g. LoopVariable.initialValue,
                # AggregationCalculation.input) isn't in LEAF_KINDS - "any
                # JSON value" has no leaf_value_ok() schema to check against -
                # but core/Types/v1.0.0/description.md's AnyValueOrRef entry
                # is explicit that an SIdRef string may still substitute for
                # it, so it needs the same reference-resolution dispatch as
                # every *OrRef-kind field above.
                problems.extend(_check_reference_field(
                    value, document=self.get_document(), class_name=self.__class__.__name__,
                    id_value=self._own_id_for_message(), attr=spec.name, location="/" + spec.name))
        if self._IS_DOCUMENT_CLASS:
            problems.extend(_check_namespace_usage_and_version(self))
            problems.extend(_check_constants_ordering(self))
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

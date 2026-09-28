"""Emit the generated Python target library from a SpecModel. Package name is
caller-supplied (see emit_python_package()) - "libsed2test" below is just the
Phase-1 test-tree default.

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

import json
import os
import re
from .spec import SpecModel, FieldType, Field, FlatClass

# Every FieldType.kind that gets the 5-accessor OrRef split (getXValue/
# getXRef/setXValue/setXRef/isXRef - see Design.md's Classes section). The
# storage/dispatch mechanics (_get_orref_value & co. in RUNTIME) are
# generic over the value's own shape, so a new kind only needs a
# _LEAF_SCHEMAS entry (see RUNTIME) plus a spot in this tuple - see
# spec.py's _classify_type/_orref_shape for how a real anyOf gets mapped to
# one of these.
_ORREF_KINDS = ("StringOrRef", "NumberOrRef", "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef")

# Handwritten rule files already authored under templates/python/rules/ (see
# Design.md's Validation section: "the generator fails its run if a
# handwritten rule is missing its file for any one of the three languages -
# ... enforced mechanically instead of by memory"). Of the ~25 rules whose
# rules-v1.0.0.json frontmatter has check=="handwritten", only the four
# math-grammar ones (Types-0001..0004) are implemented so far - this tuple,
# not "every handwritten rule in model.rules", is what's actually enforced
# today; it must grow as more get implemented, and once every handwritten
# rule has a file this can become a live scan of model.rules instead of a
# hardcoded allowlist. Java/C++ have no handwritten-rule dispatch mechanism
# yet at all (Phase 2 scope: Python only - see Design.md phase 2 status),
# so the missing-file check below only runs for Python.
_IMPLEMENTED_HANDWRITTEN_RULE_IDS = (
    "Types-0001", "Types-0002", "Types-0003", "Types-0004",
    "SEDBase-0005", "SEDBase-0006", "SEDBase-0007",
    "SEDDocument-0009", "SEDDocument-0010", "SEDDocument-0011", "SEDDocument-0013",
)

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
'''

# ASTNode: parse()/toString() for SED2 math strings (Design.md's Math
# section). Hand-authored (not per-class generated data) - written verbatim
# into every generated Python package, next to the ANTLR-generated
# mathLexer.py/mathParser.py/mathVisitor.py under ._antlr (see
# generator/antlr_tool.py and generator/math.g4). v1 has no evaluator, only
# parse()/toString() - see Math's opening paragraph.
MATH_AST_PY = r'''"""ASTNode: parses/serializes SED2 math strings into a tree and back
(Design.md's Math section). GENERATED for the libsed2test package - do not
hand-edit; regenerate via generator/generate.py. The grammar itself lives in
generator/math.g4; this module hand-builds the AST from the ANTLR parse
tree and re-serializes it, applying the libsbml-L3-infix-parser-derived
desugaring rules (relational-chain collapsing, n-ary and/or flattening, '%'
as rem()) that the grammar itself only describes informally."""
from __future__ import annotations

from dataclasses import dataclass, field as _field
from enum import Enum
from typing import Optional

from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from ._antlr.mathLexer import mathLexer
from ._antlr.mathParser import mathParser
from ._antlr.mathVisitor import mathVisitor


class MathSyntaxError(Exception):
    """Raised by parse()/ASTNode.parse() when the text isn't a well-formed
    SED2 math expression - the condition Types-0001 reports, with this
    exception's message as its {parse-message}."""


class ASTNodeType(Enum):
    NUMBER = "number"
    REFERENCE = "reference"
    NAME = "name"
    FUNCTION_CALL = "function-call"
    ARRAY = "array"
    UMINUS = "uminus"
    UPLUS = "uplus"
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    POW = "pow"


# Binding strength, used only so to_string() re-adds parentheses the source
# text may have relied on. Relational, logical and '%' all desugar to plain
# function calls (see Grammar) and a call's own parens make its arguments
# unambiguous, so only the five genuinely infix/prefix arithmetic shapes
# need this at all. Higher number binds tighter.
_PRECEDENCE = {
    ASTNodeType.ADD: 1,
    ASTNodeType.SUB: 1,
    ASTNodeType.MUL: 2,
    ASTNodeType.DIV: 2,
    ASTNodeType.UMINUS: 3,
    ASTNodeType.UPLUS: 3,
    ASTNodeType.POW: 4,
}
_ATOM_PRECEDENCE = 5  # NUMBER / REFERENCE / NAME / FUNCTION_CALL / ARRAY
_SYMBOL = {
    ASTNodeType.ADD: "+", ASTNodeType.SUB: "-",
    ASTNodeType.MUL: "*", ASTNodeType.DIV: "/", ASTNodeType.POW: "^",
}


@dataclass
class ASTNode:
    """Borrows the rough interface of libsbml's ASTNode, minus the XML
    dependency (Design.md's Math section)."""

    node_type: ASTNodeType
    text: Optional[str] = None        # NUMBER / REFERENCE: the raw source lexeme
    name: Optional[str] = None        # NAME / FUNCTION_CALL: the identifier
    children: list["ASTNode"] = _field(default_factory=list)

    def is_number(self) -> bool:
        return self.node_type is ASTNodeType.NUMBER

    def is_reference(self) -> bool:
        return self.node_type is ASTNodeType.REFERENCE

    def is_name(self) -> bool:
        return self.node_type is ASTNodeType.NAME

    def is_function_call(self) -> bool:
        return self.node_type is ASTNodeType.FUNCTION_CALL

    def get_num_children(self) -> int:
        return len(self.children)

    def get_child(self, index: int) -> "ASTNode":
        return self.children[index]

    def walk(self):
        """Depth-first iterator over this node and every descendant - the
        traversal a hand-written validate() uses for Types-0002 through
        Types-0004 (unknown function / bad arity / bare non-constant
        identifier)."""
        yield self
        for c in self.children:
            yield from c.walk()

    def to_string(self) -> str:
        return _render(self, 0)

    @staticmethod
    def parse(text: str) -> "ASTNode":
        return parse(text)


def _render(node: ASTNode, min_prec: int) -> str:
    t = node.node_type
    if t is ASTNodeType.NUMBER or t is ASTNodeType.REFERENCE:
        return node.text
    if t is ASTNodeType.NAME:
        return node.name
    if t is ASTNodeType.FUNCTION_CALL:
        return f"{node.name}({', '.join(_render(c, 0) for c in node.children)})"
    if t is ASTNodeType.ARRAY:
        return f"[{', '.join(_render(c, 0) for c in node.children)}]"
    if t is ASTNodeType.UMINUS or t is ASTNodeType.UPLUS:
        prec = _PRECEDENCE[t]
        inner = _render(node.children[0], prec)
        out = f"{'-' if t is ASTNodeType.UMINUS else '+'}{inner}"
        return f"({out})" if prec < min_prec else out
    prec = _PRECEDENCE[t]
    left, right = node.children
    if t is ASTNodeType.POW:  # right-associative
        left_s = _render(left, prec + 1)
        right_s = _render(right, prec)
    else:  # left-associative (ADD/SUB/MUL/DIV)
        left_s = _render(left, prec)
        right_s = _render(right, prec + 1)
    out = f"{left_s} {_SYMBOL[t]} {right_s}"
    return f"({out})" if prec < min_prec else out


_RELOP_KIND = {
    "==": "eq", "!=": "neq", "<>": "neq", "><": "neq",
    "<": "lt", ">": "gt", "<=": "leq", ">=": "geq",
}


def _build_relational(operands: list[ASTNode], kinds: list[str]) -> ASTNode:
    """a < b < c -> lt(a, b, c); a < b <= c -> and(lt(a, b), leq(b, c)) -
    consecutive identical relops merge into one n-ary call, a differing one
    starts a new run, and '!=' (however spelled) never merges into a run
    with anything, even another '!=' (Design.md: "!= is always binary and
    never joins a chain")."""
    if not kinds:
        return operands[0]
    runs: list[tuple[str, list[ASTNode]]] = []
    i = 0
    n = len(kinds)
    while i < n:
        kind = kinds[i]
        run_operands = [operands[i], operands[i + 1]]
        j = i + 1
        if kind != "neq":
            while j < n and kinds[j] == kind:
                run_operands.append(operands[j + 1])
                j += 1
        runs.append((kind, run_operands))
        i = j
    nodes = [ASTNode(ASTNodeType.FUNCTION_CALL, name=kind, children=run_operands)
             for kind, run_operands in runs]
    if len(nodes) == 1:
        return nodes[0]
    return ASTNode(ASTNodeType.FUNCTION_CALL, name="and", children=nodes)


def _flatten_logical(operands: list[ASTNode], ops: list[str]) -> ASTNode:
    """a && b && c -> and(a, b, c); a && b || c -> (a && b) || c, i.e.
    or(and(a, b), c) - one shared precedence level, left-associative, with
    runs of the *same* operator flattened into one n-ary call (Design.md's
    Grammar / precedence bullets)."""
    if not ops:
        return operands[0]
    groups: list[tuple[str, list[ASTNode]]] = []
    current_op = ops[0]
    current_operands = [operands[0], operands[1]]
    for i in range(1, len(ops)):
        if ops[i] == current_op:
            current_operands.append(operands[i + 1])
        else:
            groups.append((current_op, current_operands))
            current_op = ops[i]
            current_operands = [current_operands[-1], operands[i + 1]]
    groups.append((current_op, current_operands))
    result = ASTNode(ASTNodeType.FUNCTION_CALL, name=groups[0][0], children=groups[0][1])
    for op, opers in groups[1:]:
        result = ASTNode(ASTNodeType.FUNCTION_CALL, name=op, children=[result] + opers[1:])
    return result


class _Builder(mathVisitor):
    """Builds an ASTNode tree from the ANTLR parse tree, applying the
    desugaring in _build_relational()/_flatten_logical() above along the
    way - see Design.md's Grammar section (relational/logical/piecewise
    "follows libsbml's L3 infix parser", decided 2026-09-24)."""

    def visitStart(self, ctx):
        return self.visit(ctx.expr())

    def visitExpr(self, ctx):
        return self.visit(ctx.logical())

    def visitLogical(self, ctx):
        relationals = ctx.relational()
        if len(relationals) == 1:
            return self.visit(relationals[0])
        operands = [self.visit(r) for r in relationals]
        ops = ["and" if ctx.children[i].getText() == "&&" else "or"
               for i in range(1, len(ctx.children), 2)]
        return _flatten_logical(operands, ops)

    def visitRelational(self, ctx):
        additives = ctx.additive()
        if len(additives) == 1:
            return self.visit(additives[0])
        operands = [self.visit(a) for a in additives]
        kinds = [_RELOP_KIND[r.getText()] for r in ctx.relop()]
        return _build_relational(operands, kinds)

    def visitAdditive(self, ctx):
        muls = ctx.multiplicative()
        node = self.visit(muls[0])
        idx = 1
        for i in range(1, len(ctx.children), 2):
            op_text = ctx.children[i].getText()
            rhs = self.visit(muls[idx])
            idx += 1
            node = ASTNode(ASTNodeType.ADD if op_text == "+" else ASTNodeType.SUB,
                            children=[node, rhs])
        return node

    def visitMultiplicative(self, ctx):
        units = ctx.unary()
        node = self.visit(units[0])
        idx = 1
        for i in range(1, len(ctx.children), 2):
            op_text = ctx.children[i].getText()
            rhs = self.visit(units[idx])
            idx += 1
            if op_text == "*":
                node = ASTNode(ASTNodeType.MUL, children=[node, rhs])
            elif op_text == "/":
                node = ASTNode(ASTNodeType.DIV, children=[node, rhs])
            else:  # '%' is infix rem(), dividend's-sign semantics (Grammar)
                node = ASTNode(ASTNodeType.FUNCTION_CALL, name="rem", children=[node, rhs])
        return node

    def visitUnaryOp(self, ctx):
        op_text = ctx.getChild(0).getText()
        operand = self.visit(ctx.unary())
        if op_text == "!":
            return ASTNode(ASTNodeType.FUNCTION_CALL, name="not", children=[operand])
        return ASTNode(ASTNodeType.UMINUS if op_text == "-" else ASTNodeType.UPLUS,
                        children=[operand])

    def visitUnaryPower(self, ctx):
        return self.visit(ctx.power())

    def visitPower(self, ctx):
        base = self.visit(ctx.atom())
        if ctx.unary():
            return ASTNode(ASTNodeType.POW, children=[base, self.visit(ctx.unary())])
        return base

    def visitNumberAtom(self, ctx):
        return ASTNode(ASTNodeType.NUMBER, text=ctx.getText())

    def visitReferenceAtom(self, ctx):
        return ASTNode(ASTNodeType.REFERENCE, text=ctx.getText())

    def visitIdentAtom(self, ctx):
        return ASTNode(ASTNodeType.NAME, name=ctx.getText())

    def visitCallAtom(self, ctx):
        name = ctx.IDENTIFIER().getText()
        args = [self.visit(e) for e in (ctx.arglist().expr() if ctx.arglist() else [])]
        return ASTNode(ASTNodeType.FUNCTION_CALL, name=name, children=args)

    def visitArrayAtom(self, ctx):
        args = [self.visit(e) for e in (ctx.arglist().expr() if ctx.arglist() else [])]
        return ASTNode(ASTNodeType.ARRAY, children=args)

    def visitParenAtom(self, ctx):
        return self.visit(ctx.expr())


class _CollectingErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"line {line}:{column} {msg}")


def parse(text: str) -> ASTNode:
    """Parses a SED2 math string into an ASTNode tree (Types-0001). Raises
    MathSyntaxError with the parser's own message on any malformed input."""
    listener = _CollectingErrorListener()
    lexer = mathLexer(InputStream(text))
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)
    stream = CommonTokenStream(lexer)
    parser = mathParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    tree = parser.start()
    if listener.errors:
        raise MathSyntaxError("; ".join(listener.errors))
    return _Builder().visit(tree)


def to_string(node: ASTNode) -> str:
    return node.to_string()
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
            "pattern=%r, item_class=%r, item_discriminator=%r, is_math=%r)" % (
                f.name, t.kind, f.required, f.rule_id, f.required_rule_id,
                f"{f.origin_class}-0000", t.minimum, t.exclusive_minimum,
                t.pattern, t.item_class, t.item_discriminator, f.is_math,
            )
        )
    return "[" + ", ".join(parts) + "]"


def _leaf_accessors(cls_name: str, f: Field) -> str:
    py = _pyname(f.name)
    kind = f.type.kind
    lines = []
    if kind in _ORREF_KINDS:
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
    elif t.kind == "any-dict":
        # Same ID-keyed collection shape as "dict", but items are raw JSON
        # values (numbers/strings/lists/objects/bools), never SedBase
        # instances - so no ._attach() call (SEDDocument.constants today;
        # see spec.py's _classify_type additionalProperties branch).
        lines.append(f"    def get_{py}(self):\n        return self._{py}.ids()\n")
        lines.append(f"    def get_{py}_item(self, item_id):\n        return self._{py}.get(item_id)\n")
        lines.append(f"    def add_{py}(self, item_id, value):\n        self._{py}.add(item_id, value)\n")
        lines.append(f"    def insert_{py}(self, index, item_id, value):\n        self._{py}.insert(index, item_id, value)\n")
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
        collection_fields = [f for f in own_fields if f.type.kind in ("dict", "array", "any-dict")]
        leaf_fields = [f for f in own_fields if f.type.kind in _ORREF_KINDS + (
            "string", "integer", "number", "boolean", "SId", "SIdRef", "any")]
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
        if c.is_document:
            out.append(f"    _IS_DOCUMENT_CLASS = True\n")
            out.append(f"    _MAX_KNOWN_DOCUMENT_VERSION = {model.document_version!r}\n")
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
                if f.type.item_discriminator:
                    out.append(f"        self._{py} = IdKeyedCollection({_dispatch_fn_name(f.type.item_discriminator)})\n")
                else:
                    # Plain (non-discriminated) item class: every entry is
                    # the same fixed type, e.g. Loop.loopVariables ->
                    # LoopVariable - no _type dispatch needed.
                    out.append(
                        f"        self._{py} = IdKeyedCollection("
                        f"lambda tv, _cls={f.type.item_class}: (_cls, False))\n"
                    )
            elif f.type.kind == "any-dict":
                # Items are raw JSON values, never dispatched to a class -
                # the dispatch_fn is simply never called (see _load_fields's
                # any-dict branch below).
                out.append(f"        self._{py} = IdKeyedCollection(None)\n")
            else:
                out.append(f"        self._{py} = ListCollection()\n")
        for p, fs in c.namespace_updates.items():
            pass  # namespace fields stored in the same self._values dict, no init needed
        if c.is_document:
            # The document root is its own document (get_document() must
            # never be None for anything reachable from it) - read_from_string
            # sets this up for a deserialized document via its own
            # obj._attach(None, obj) call, but a document built up
            # programmatically (SEDDocument() then add_tasks(...), etc.,
            # never round-tripped through read_from_string) needs the same
            # self-attach here, or every backpointer-dependent thing
            # downstream (get_document(), get_parent(), and in particular
            # the SEDBase-0005/0006/0007 reference-resolution rules, which
            # silently no-op with no document to walk) breaks silently for
            # documents built that way.
            out.append("        self._attach(None, self)\n")
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
            elif f.type.kind == "array":
                out.append(f"        kids.extend(self._{py}.items())\n")
            # "any-dict" items are raw JSON values, never SedBase instances -
            # excluded from _children()/_children_with_locations() below, so
            # they get no backpointer attachment and no validate() recursion
            # (see SEDBase-0012 for the separate, still-open rule covering
            # a constant's own shape).
        out.append("        return kids\n\n")

        # Generic containment-tree lookup by field name (SEDBase-0006 /
        # get_sed_reference() in RUNTIME - Design.md's Cross-references
        # section): every ID-keyed collection this class owns, by its own
        # field name, so a reference's colon-segments can walk into any
        # class's own dict-kind field generically, not just SEDDocument's
        # top-level tasks/constants/outputs/styles. "any-dict" fields
        # (constants) are included too - their own values are plain JSON,
        # not further walkable, but get_sed_reference() itself stops there.
        id_coll_fields = [f for f in collection_fields if f.type.kind in ("dict", "any-dict")]
        out.append("    def _get_id_collection(self, field_name):\n")
        for f in id_coll_fields:
            out.append(f"        if field_name == {f.name!r}: return self._{_pyname(f.name)}\n")
        out.append("        return None\n\n")

        out.append(f"    def _children_with_locations(self):\n        out = []\n")
        for f in collection_fields:
            py = _pyname(f.name)
            if f.type.kind == "dict":
                out.append(f"        for i in self._{py}.ids():\n            out.append((self._{py}.get(i), '/{f.name}/' + i))\n")
            elif f.type.kind == "array":
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
            elif f.type.kind == "any-dict":
                # Raw JSON values, round-tripped as-is - no .to_json_value().
                out.append(f"        if len(self._{py}): d[{f.name!r}] = {{i: self._{py}.get(i) for i in self._{py}.ids()}}\n")
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
    out.append("        if spec.name not in raw or spec.kind in ('dict', 'array', 'any-dict'):\n")
    out.append("            continue\n")
    out.append("        v = raw[spec.name]\n")
    out.append(f"        if spec.kind in {_ORREF_KINDS!r}:\n")
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
    out.append("            dispatch = globals()['parse_' + spec.item_discriminator] if spec.item_discriminator else None\n")
    out.append("            for item_id, item_raw in raw_value.items():\n")
    out.append("                if not SID_PATTERN.match(item_id):\n")
    out.append("                    rid = spec.rule_id or spec.origin_catchall\n")
    out.append("                    obj._load_problems.append(make_problem(rid, '/' + spec.name, **{\n")
    out.append("                        'attr': spec.name, 'class': obj.__class__.__name__,\n")
    out.append("                        'id': obj._own_id_for_message(), 'value': item_id}))\n")
    out.append("                if dispatch is not None:\n")
    out.append("                    child, problem = dispatch(item_raw)\n")
    out.append("                    if problem is not None:\n")
    out.append("                        obj._load_problems.append(problem)\n")
    out.append("                else:\n")
    out.append("                    # Plain (non-discriminated) item class: no _type dispatch.\n")
    out.append("                    child = globals()[spec.item_class]()\n")
    out.append("                    _load_fields(child, item_raw)\n")
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
    out.append("        elif spec.kind == 'any-dict' and spec.name in raw:\n")
    out.append("            # Every value is stored as-is - a plain JSON value, never\n")
    out.append("            # constructed as a class instance (see spec.py's _classify_type\n")
    out.append("            # additionalProperties branch and _collection_accessors' any-dict\n")
    out.append("            # branch above).\n")
    out.append("            raw_value = raw[spec.name]\n")
    out.append("            if not isinstance(raw_value, dict):\n")
    out.append("                rid = spec.rule_id or spec.origin_catchall\n")
    out.append("                obj._load_problems.append(make_problem(rid, '/' + spec.name, **{\n")
    out.append("                    'attr': spec.name, 'class': obj.__class__.__name__,\n")
    out.append("                    'id': obj._own_id_for_message(), 'value': raw_value}))\n")
    out.append("                continue\n")
    out.append("            coll = getattr(obj, '_' + _pyname(spec.name))\n")
    out.append("            for item_id, item_value in raw_value.items():\n")
    out.append("                if not SID_PATTERN.match(item_id):\n")
    out.append("                    rid = spec.rule_id or spec.origin_catchall\n")
    out.append("                    obj._load_problems.append(make_problem(rid, '/' + spec.name, **{\n")
    out.append("                        'attr': spec.name, 'class': obj.__class__.__name__,\n")
    out.append("                        'id': obj._own_id_for_message(), 'value': item_id}))\n")
    out.append("                coll.add(item_id, item_value)\n")
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
    if f.type.kind in _ORREF_KINDS:
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


def _repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _normalize_arity(raw) -> tuple:
    """Normalizes one schema/predefined-functions.json arity value into the
    two-shape contract templates/python/rules/Types-0003.py documents and
    consumes: ("set", frozenset({...})) for a fixed handful of allowed
    counts (an int becomes a one-element set; a [1, 2]-style list becomes
    that set directly), or ("range", min, max) for an open-ended {min, max}
    object (max is None when unbounded, e.g. min/max/sum's {"min": 1,
    "max": null})."""
    if isinstance(raw, bool):
        raise ValueError(f"unrecognized arity shape: {raw!r}")
    if isinstance(raw, int):
        return ("set", frozenset({raw}))
    if isinstance(raw, list):
        return ("set", frozenset(raw))
    if isinstance(raw, dict):
        return ("range", raw.get("min", 0), raw.get("max"))
    raise ValueError(f"unrecognized arity shape: {raw!r}")


def emit_predefined_functions_py(registry_path: str | None = None) -> str:
    """Compiles schema/predefined-functions.json's callable-by-name entries
    (the "functions" array's SBML L3 Core MathML subset plus the "distrib"
    array's 12 csymbol draw functions - Design.md's Math section says
    Types-0002/-0003 check call names/arities against this same registry)
    into a plain data module, plus the "constants" array as a frozenset for
    Types-0004. Pure derived data, not hand-written logic - see Design.md's
    Validation section distinguishing handwritten rules from formulaic
    ones - so this is generated fresh every run rather than living under
    templates/, unlike templates/python/rules/Types-000N.py which consume
    it."""
    registry_path = registry_path or os.path.join(_repo_root(), "schema", "predefined-functions.json")
    with open(registry_path) as f:
        registry = json.load(f)
    functions: dict[str, tuple] = {}
    for entry in registry.get("functions", []):
        functions[entry["name"]] = _normalize_arity(entry["arity"])
    for entry in registry.get("distrib", []):
        lengths = frozenset(len(variant) for variant in entry["variants"])
        functions[entry["name"]] = ("set", lengths)
    constants = frozenset(entry["name"] for entry in registry.get("constants", []))

    def _fmt_spec(spec: tuple) -> str:
        if spec[0] == "set":
            return f"('set', frozenset({sorted(spec[1])!r}))"
        return f"('range', {spec[1]!r}, {spec[2]!r})"

    lines = [
        '"""Compiled math function/constant registry for Types-0002/-0003/-0004\'s '
        'math-grammar checks (Design.md\'s Math section). GENERATED from '
        'schema/predefined-functions.json by generator/generate.py - do not hand-edit."""',
        "",
        "FUNCTIONS = {",
    ]
    for name in sorted(functions):
        lines.append(f"    {name!r}: {_fmt_spec(functions[name])},")
    lines.append("}")
    lines.append("")
    lines.append(f"CONSTANTS = frozenset({sorted(constants)!r})")
    lines.append("")
    return "\n".join(lines) + "\n"


def _copy_handwritten_rules_py(pkg_dir: str, model: SpecModel) -> None:
    """Copies templates/python/rules/<RuleID>.py -> <pkg>/_rules/<rule_id>.py
    for every rule ID in _IMPLEMENTED_HANDWRITTEN_RULE_IDS that this MODEL
    actually defines (rid in model.rules), verbatim (a filename-case/hyphen-
    to-underscore rename only, so the file is importable as a submodule -
    the rule ID stays the source of truth, visible in the template's own
    filename per Design.md's Validation section).

    Some of these rules (today, SEDBase-0005 through -0007) encode a
    convention specific to the real SED2 spec's own SEDBase/SEDDocument
    (the '#tasks:'/'#constants:'/'#outputs:'/'#styles:' containment-root
    vocabulary) - a different spec tree, such as test-specsheets/'s
    synthetic TestBase, has no such rule IDs in its own model.rules at all,
    and would be validated by the WRONG convention if this ran anyway. So a
    rule id not present in model.rules is skipped here, silently - not a
    "forgotten file" bug, just this rule not applying to this tree - and
    the caller (_check_math_field / _check_reference_field in RUNTIME)
    degrades to a no-op for it via ImportError, rather than crashing or
    misapplying a foreign convention. The missing-file RuntimeError below
    still fires - failing the whole generator run, per Design.md's
    Validation section - for any rule id the model DOES define but whose
    template file is genuinely absent, which is the actually-forgotten
    case this check exists to catch."""
    templates_dir = os.path.join(_repo_root(), "templates", "python", "rules")
    rules_pkg_dir = os.path.join(pkg_dir, "_rules")
    os.makedirs(rules_pkg_dir, exist_ok=True)
    with open(os.path.join(rules_pkg_dir, "__init__.py"), "w") as f:
        f.write(
            '"""Hand-written per-rule check() functions (Design.md\'s Validation '
            'section). GENERATED COPY of templates/python/rules/ - do not hand-edit '
            'here; edit the template and regenerate."""\n'
        )
    missing = []
    for rid in _IMPLEMENTED_HANDWRITTEN_RULE_IDS:
        if rid not in model.rules:
            continue
        src = os.path.join(templates_dir, f"{rid}.py")
        if not os.path.isfile(src):
            missing.append(src)
            continue
        with open(src) as f:
            content = f.read()
        dest = os.path.join(rules_pkg_dir, rid.lower().replace("-", "_") + ".py")
        with open(dest, "w") as f:
            f.write(content)
    if missing:
        raise RuntimeError(
            "Missing hand-written rule file(s) required by the generator "
            "(Design.md's Validation section - \"the generator fails its run if a "
            "handwritten rule is missing its file\"): " + ", ".join(missing)
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
        "from ._runtime import ApiError, ValidationProblem\n"
        "from .math_ast import ASTNode, ASTNodeType, MathSyntaxError, parse as parse_math, to_string as math_to_string\n\n"
        f"__all__ = {names + ['read_from_string', 'read_from_file', 'write_to_string', 'write_to_file', 'ApiError', 'ValidationProblem', 'ASTNode', 'ASTNodeType', 'MathSyntaxError', 'parse_math', 'math_to_string']!r}\n"
    )


def emit_python_package(
    model: SpecModel,
    out_dir: str,
    package_name: str = "libsed2test",
    description: str | None = None,
    build_math: bool = True,
    antlr_cache_dir: str | None = None,
) -> None:
    description = description or (
        "Generated SED2 test-fixture library (Python target) - exercises the "
        "SED2 generator against test-specsheets/, see Design.md's Testing "
        "section."
    )
    # RUNTIME and the emit_*(model) bodies below only mention the Phase-1
    # default package name in their own cosmetic module docstrings (never in
    # actual code/identifiers - verified when this was parameterized), so a
    # plain substitution is safe and avoids threading package_name through
    # every one of those functions individually.
    def _named(text: str) -> str:
        return text.replace("libsed2test", package_name) if package_name != "libsed2test" else text

    pkg_dir = os.path.join(out_dir, "src", package_name)
    os.makedirs(pkg_dir, exist_ok=True)
    with open(os.path.join(pkg_dir, "_runtime.py"), "w") as f:
        f.write(_named(RUNTIME))
    with open(os.path.join(pkg_dir, "rules_data.py"), "w") as f:
        f.write(_named(emit_rules_data_py(model)))
    with open(os.path.join(pkg_dir, "model.py"), "w") as f:
        f.write(_named(emit_model_py(model)))
    with open(os.path.join(pkg_dir, "io.py"), "w") as f:
        f.write(_named(emit_document_helpers(model)))
    with open(os.path.join(pkg_dir, "math_ast.py"), "w") as f:
        f.write(_named(MATH_AST_PY))
    # Handwritten rule files (Design.md's Validation section) - copied from
    # templates/python/rules/ with a missing-file check that fails this
    # whole run, plus the compiled predefined-functions.json data they rely
    # on for Types-0002/-0003. Both are consumed lazily (see
    # _check_math_field in RUNTIME above) so write order relative to
    # _runtime.py/model.py doesn't matter.
    _copy_handwritten_rules_py(pkg_dir, model)
    with open(os.path.join(pkg_dir, "_predefined_functions.py"), "w") as f:
        f.write(emit_predefined_functions_py())
    with open(os.path.join(pkg_dir, "__init__.py"), "w") as f:
        f.write(_named(emit_init_py(model)))
    if build_math:
        # ANTLR tool is a build-time-only dependency of the generator itself
        # (Design.md's Parser Strategy) - runs here, writes the generated
        # mathLexer.py/mathParser.py/mathVisitor.py into ._antlr, which
        # math_ast.py above imports from.
        from .antlr_tool import generate_python_math_parser
        generate_python_math_parser(os.path.join(pkg_dir, "_antlr"), cache_dir=antlr_cache_dir)
    antlr_runtime_version = __import__("generator.antlr_tool", fromlist=["ANTLR_VERSION"]).ANTLR_VERSION
    pyproject = f'''[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "{package_name}"
version = "0.1.0"
description = "{description}"
requires-python = ">=3.10"
dependencies = ["jsonschema>=4.18", "antlr4-python3-runtime=={antlr_runtime_version}"]

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
{package_name} = ["_antlr/*.py"]
'''
    with open(os.path.join(out_dir, "pyproject.toml"), "w") as f:
        f.write(pyproject)

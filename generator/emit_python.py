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
    "SEDBase-0008", "SEDBase-0009", "SEDBase-0010", "SEDBase-0011", "SEDBase-0012",
    "SEDBase-0013", "SEDBase-0014", "SEDBase-0015", "SEDBase-0016", "SEDBase-0017",
    "SEDDocument-0009", "SEDDocument-0010", "SEDDocument-0011", "SEDDocument-0013",
    "AbstractTask-0003", "Repeat-0008", "Repeat-0009", "Repeat-0010", "LoopVariable-0004",
    # SEDDocument-0012 (duplicate JSON keys) is deliberately NOT implemented -
    # see SEDDocument-0012.md's own "Decided not to implement detection for
    # this rule in v1" paragraph. Every fixture for it is a documentation-
    # only stub, never expected to actually fire.
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


def _check_reference_field(value, *, document, class_name, id_value, attr, location,
                            referrer=None, field_kind=None, ref_type_rule_id=None,
                            expected_enum=None, constraints=None, ref_target=None) -> list:
    """Shared per-type dispatcher for every reference-resolution rule
    (SEDBase-0005 through -0015, plus the formulaic ref-type rules that
    piggyback on -0015's scalar-reduction check - Design.md's Validation
    section, "the formulaic 'if a reference, must resolve to type X' rules
    ... needing no per-rule authorship"). Called for every SIdRef/*OrRef/
    any-kind field whose value is a reference (is_reference(value));
    mirrors _check_math_field's shape and local-import-to-avoid-
    circularity convention (see its own docstring). `referrer` is the
    element carrying this reference (self, in _validate_own) - needed only
    by SEDBase-0013's own containment-tree scoping check, so it's the one
    argument every OTHER caller in this module besides _validate_own's own
    two call sites can safely omit. `field_kind`/`ref_type_rule_id`/
    `expected_enum` drive the ref-type dispatch at the very end and can
    likewise be omitted wherever there's no field-level ref-type rule to
    check (an "any"-kind AnyValueOrRef field, or a plain SIdRef field that
    only ever had one rule id to begin with)."""
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
    if resolved is None or parsed.collection == "outputs":
        # Nothing further to check against - either the reference didn't
        # resolve at all (SEDBase-0006 already reported it), or it targets
        # an Output (SEDBase-0007 already reported it; core-spec.md's
        # Outputs are never a data SOURCE, so there's no "shape" to check
        # an accessor/index chain against in the first place).
        return problems
    if parsed.collection != "constants":
        # A constants target is a raw JSON value (IdKeyedCollection stores
        # any-dict entries as-is, never dispatched to a SedBase instance -
        # see this module's own any-dict handling notes elsewhere), so
        # there's no containment ancestry to walk and SEDBase-0013's own
        # Repeat-scoping concept doesn't apply to it at all.
        problems = problems + _check_repeat_scoping(
            referrer, resolved, parsed, class_name=class_name, id_value=id_value, location=location, value=value)
    if parsed.collection == "tasks":
        # AbstractTask-0003's own chronological rule - only ever meaningful
        # for a '#tasks:...' target (a constants target has no ordering
        # concept beyond SEDDocument-0013's own separate constants-only
        # check; core-spec.md Section 3 exempts Output/Style referrers
        # entirely, which _check_task_order detects on its own via
        # _task_chain(referrer, ...) returning None for them).
        problems = problems + _check_task_order(
            referrer, resolved, document, parsed, class_name=class_name, id_value=id_value,
            attr=attr, location=location, value=value)
    problems = problems + _check_output_shape_and_ref_type(
        parsed, resolved, document, class_name=class_name, id_value=id_value, attr=attr, location=location,
        value=value, field_kind=field_kind, ref_type_rule_id=ref_type_rule_id, expected_enum=expected_enum,
        constraints=constraints, ref_target=ref_target)
    return problems


# ---- SEDBase-0013: Repeat subTasks/range/index/loopVariables scoping ------
# Pure containment-tree ancestry, no outputs.json/shape involved at all -
# see SEDBase-0013.md's own text and templates/python/rules/SEDBase-0013.py.

def _nearest_repeat_ancestor(elem):
    cur = elem
    while cur is not None:
        if cur._get_id_collection("subTasks") is not None:
            return cur
        cur = cur.get_parent()
    return None


def _is_ancestor_or_self(candidate, elem):
    cur = elem
    while cur is not None:
        if cur is candidate:
            return True
        cur = cur.get_parent()
    return False


def _check_repeat_scoping(referrer, resolved, parsed, *, class_name, id_value, location, value) -> list:
    try:
        from ._rules import sedbase_0013
    except ImportError:
        return []
    dot_name = next((v for k, v in parsed.accessors if k == "dot"), None)
    is_repeat_itself = resolved._get_id_collection("subTasks") is not None
    if is_repeat_itself:
        # A bare/.model/.aggregates/.strings reference to the Repeat ITSELF
        # is never scoped (SEDBase-0013.md's own clarifying paragraph -
        # "#tasks:loop1 or #tasks:loop1.aggregates ... from anywhere");
        # only its .range/.index outputs are, since those only have a
        # value during one iteration.
        target_repeat = resolved if dot_name in ("range", "index") else None
    else:
        parent = resolved.get_parent()
        target_repeat = _nearest_repeat_ancestor(parent) if parent is not None else None
    if target_repeat is None or referrer is None:
        return []
    if _is_ancestor_or_self(target_repeat, referrer):
        return []
    return sedbase_0013.check(
        False, target_repeat._own_id_for_message(), value=value,
        class_name=class_name, id_value=id_value, location=location, make_problem=make_problem)


# ---- AbstractTask-0003: the chronological ("no forward reference") rule --
# core-spec.md Section 3 - see AbstractTask-0003.md's own worked-out cases
# and templates/python/rules/AbstractTask-0003.py.

def _dict_membership(node):
    """(owner, coll_name, node_id, index) if node's own parent stores node
    directly under a 'tasks' or 'subTasks' id-keyed collection - the two
    collection kinds the chronological rule cares about (SEDDocument.tasks
    itself, and a Repeat-family class's own subTasks) - else None. A
    node stored under any OTHER id-keyed field (loopVariables,
    aggregateOutputVariables, constants, outputs, styles, ...) doesn't
    match here, which is exactly what lets _task_chain below collapse a
    reference living in one of those fields down to its owning task's own
    chronological position (see LoopVariable-0004.py's own docstring)."""
    parent = node.get_parent()
    if parent is None:
        return None
    for coll_name in ("tasks", "subTasks"):
        coll = parent._get_id_collection(coll_name)
        if coll is None:
            continue
        ids = list(coll.ids())
        for idx, iid in enumerate(ids):
            if coll.get(iid) is node:
                return (parent, coll_name, iid, idx)
    return None


def _task_chain(elem, doc):
    """The chain of dict-membership steps from SEDDocument.tasks down to
    whichever tasks/subTasks entry directly contains `elem` (elem itself,
    if elem IS such an entry) - outermost first, as a list of (id, index)
    pairs. None if elem isn't reachable inside doc.tasks at all (an
    Output/Style element, or doc itself) - core-spec.md Section 3: nothing
    outside the tasks tree has a chronological position to compare."""
    node = elem
    chain = []
    while node is not None and node is not doc:
        m = _dict_membership(node)
        if m is not None:
            owner, coll_name, node_id, idx = m
            chain.append((node_id, idx))
            node = owner
            continue
        node = node.get_parent()
    if not chain:
        return None
    chain.reverse()
    return chain


def _task_order_ok(rchain, tchain):
    """AbstractTask-0003.md's own chronological comparison, walked level by
    level (both chains are outermost-first): the first level where the two
    chains name a DIFFERENT task-dict entry is the decisive one - the
    target must be strictly earlier there ("a task appearing earlier in
    the same tasks dictionary" / "an earlier sibling subTask", recursively
    at whatever depth that turns out to be). If every level of the SHORTER
    chain matches, the two chains share a task-lineage prefix:
      - target chain no longer than referrer's: target names referrer's
        own task, or an ancestor Repeat of it ("R itself, or any Repeat
        enclosing R") - fine, UNLESS the two chains are the exact same
        length (target IS referrer's own task - "a task never references
        itself").
      - target chain longer: target is a descendant subTask of referrer's
        own task (Repeat-0008/-0009's own scenario: R's outputVariableMap/
        aggregateOutputVariables referencing one of R's own subTasks) -
        always fine, no ordering concept applies going downward."""
    n = min(len(rchain), len(tchain))
    for i in range(n):
        rid, ridx = rchain[i]
        tid, tidx = tchain[i]
        if rid != tid:
            return tidx < ridx
    if len(tchain) <= len(rchain):
        return len(tchain) < len(rchain)
    return True


def _check_task_order(referrer, resolved, document, parsed, *, class_name, id_value, attr, location, value) -> list:
    try:
        from ._rules import abstracttask_0003
    except ImportError:
        return []
    if referrer is None or document is None:
        return []
    rchain = _task_chain(referrer, document)
    if rchain is None:
        # The referring element itself isn't inside SEDDocument.tasks at
        # all (e.g. a Curve under outputs/ referencing a task) -
        # core-spec.md Section 3: outputs always come chronologically
        # after every task, so no ordering constraint applies to them.
        return []
    tchain = _task_chain(resolved, document)
    if tchain is None:
        return []
    ok = _task_order_ok(rchain, tchain)
    return abstracttask_0003.check(
        ok, value=value, class_name=class_name, id_value=id_value,
        attr=attr, location=location, make_problem=make_problem)


# ---- Repeat-0008/-0009/-0010: a Repeat-family instance's own children ----
# outputVariableMap/aggregateOutputVariables must stay scoped to that same
# instance's own subTasks, and an aggregateOutputVariables entry may never
# define appliedDimensions - see each rule's own templates/python/rules/
# file. Detected by class SHAPE (_get_id_collection('subTasks') is not
# None), not by name, so this applies uniformly to every Repeat-family
# class (Loop/ParameterScan/Scatter in the real spec) without hardcoding
# any of their names here.

def _element_parent(resolved):
    """The parent of a resolved reference target, or None when the target is
    not a document element at all - a reference into `constants` resolves to a
    bare JSON value (number, string, list, dict) that has no parent and must
    simply count as "not one of my own children", never crash validate()."""
    getter = getattr(resolved, "get_parent", None)
    return getter() if callable(getter) else None


def _check_repeat_own_children(self) -> list:
    try:
        from ._rules import repeat_0008, repeat_0009, repeat_0010
    except ImportError:
        return []
    if self._get_id_collection("subTasks") is None:
        return []
    document = self.get_document()

    def _resolves_to_own_child(ref_value):
        parsed = _parse_reference(ref_value)
        resolved, _ = get_sed_reference(document, parsed) if document is not None else (None, None)
        return resolved is not None and _element_parent(resolved) is self

    problems = []
    ovm = self._values.get("outputVariableMap")
    if isinstance(ovm, dict):
        for key, entry_value in ovm.items():
            if not is_reference(entry_value):
                continue
            if not _resolves_to_own_child(entry_value):
                problems.extend(repeat_0008.check(
                    False, value=entry_value, class_name=self.__class__.__name__,
                    id_value=self._own_id_for_message(), attr=key,
                    location=f"/outputVariableMap/{key}", make_problem=make_problem))
    agg_coll = self._get_id_collection("aggregateOutputVariables")
    if agg_coll is not None:
        for entry_id in agg_coll.ids():
            entry = agg_coll.get(entry_id)
            entry_json = entry._own_json_value()
            if "appliedDimensions" in entry_json:
                problems.extend(repeat_0010.check(
                    True, value=entry_json["appliedDimensions"], class_name=self.__class__.__name__,
                    id_value=self._own_id_for_message(), attr="appliedDimensions",
                    location=f"/aggregateOutputVariables/{entry_id}/appliedDimensions",
                    make_problem=make_problem))
            input_value = entry_json.get("input")
            if input_value is not None and is_reference(input_value) and not _resolves_to_own_child(input_value):
                problems.extend(repeat_0009.check(
                    False, value=input_value, class_name=self.__class__.__name__,
                    id_value=self._own_id_for_message(), attr="input",
                    location=f"/aggregateOutputVariables/{entry_id}/input", make_problem=make_problem))
    return problems


# ---- LoopVariable-0004: subsequentValues stays scoped to the enclosing ---
# Loop's own subTasks - same shape as Repeat-0008/-0009 above, but for the
# one field a LoopVariable itself carries.

def _check_loop_variable_scope(self) -> list:
    try:
        from ._rules import loopvariable_0004
    except ImportError:
        return []
    if "subsequentValues" not in self._values:
        return []
    value = self._values["subsequentValues"]
    if not is_reference(value):
        return []
    enclosing = self.get_parent()
    if enclosing is None:
        return []
    document = self.get_document()
    parsed = _parse_reference(value)
    resolved, _ = get_sed_reference(document, parsed) if document is not None else (None, None)
    ok = resolved is not None and _element_parent(resolved) is enclosing
    if ok:
        return []
    return loopvariable_0004.check(
        False, value=value, id_value=self._own_id_for_message(),
        location="/subsequentValues", make_problem=make_problem)


# ---- SEDBase-0008 through -0012/-0014/-0015, plus the formulaic ref-type -
# rules (Design.md's Validation section) - core-spec.md Section 8's
# outputs.json-driven hasSubvalue()-style shape resolution, via
# outputs_shape.py (imported lazily, mirroring _check_math_field's own
# local-import convention).

_SCALAR_ORREF_EXPECTED = {
    "NumberOrRef": "number", "StringOrRef": "string",
    "IntegerOrRef": "integer", "BooleanOrRef": "boolean",
}
# Every kind the formulaic ref-type rules check: the four scalar kinds above
# plus the two container kinds. "If a reference, must resolve to an array /
# dictionary" (ArrayOrRef / DictOrRef) is checked structurally against a
# constant's literal value (a list / a dict, with element/value kinds from
# the schema's items / additionalProperties - FieldSpec.item_kind), and a
# reference to a model is never acceptable for any of them: a model is a
# type of its own (ProposedRules.md).
_REF_TYPE_KINDS = set(_SCALAR_ORREF_EXPECTED) | {"ArrayOrRef", "DictOrRef"}
# TODO: a task output is never a dictionary, so a DictOrRef field that
# references a data output is wrong too, but it is only flagged for a model
# target for now (no fixture pins the data-output case down).


def _fmt_literal(value) -> str:
    try:
        return json.dumps(value)
    except (TypeError, ValueError):
        return str(value)


def _is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _literal_matches_kind(value, field_kind, expected_enum, constraints=None):
    """Only called once a constant's own literal value has already been
    fully indexed down (index_into_literal) - a REAL value, not a
    derived/declared type name, so enum membership, numeric bounds, and
    array/dict element kinds can be checked exactly here (unlike
    _ref_type_matches_declared below, for a task-output target).
    `constraints` is FieldSpec's (minimum, exclusive_minimum, item_kind).
    A bare JSON boolean never counts as a number. Inside an array/dict a
    reference-valued element is accepted (it may resolve to the right kind;
    that is not decidable here)."""
    minimum, exclusive_minimum, item_kind = constraints if constraints else (None, None, None)
    if field_kind in ("NumberOrRef", "IntegerOrRef"):
        if field_kind == "NumberOrRef":
            ok = _is_number(value)
        else:
            ok = (isinstance(value, int) and not isinstance(value, bool)) or \
                 (isinstance(value, float) and value.is_integer())
        if not ok:
            return False
        if minimum is not None and value < minimum:
            return False
        if exclusive_minimum is not None and value <= exclusive_minimum:
            return False
        return True
    if field_kind == "BooleanOrRef":
        return isinstance(value, bool)
    if field_kind == "StringOrRef":
        if not isinstance(value, str):
            return False
        if expected_enum is not None:
            return value in expected_enum
        return True
    if field_kind == "ArrayOrRef":
        if not isinstance(value, list):
            return False
        return all(_element_matches(v, item_kind) for v in value)
    if field_kind == "DictOrRef":
        if not isinstance(value, dict):
            return False
        return all(_element_matches(v, item_kind) for v in value.values())
    return None


def _element_matches(element, item_kind) -> bool:
    """One array element / dict value against the schema's declared kind
    ("string" | "number" | "ref" | "any"). A reference-valued element always
    passes for string/number (it stands in for a value of that kind)."""
    if item_kind == "string":
        return isinstance(element, str)
    if item_kind == "number":
        return _is_number(element) or (isinstance(element, str) and is_reference(element))
    if item_kind == "ref":
        return isinstance(element, str) and is_reference(element)
    return True


def _ref_type_matches_declared(expected, actual_declared_type):
    """A task-output target has no actual VALUE to type-check (nothing has
    been simulated) - only outputs.json's own declared "type" for the
    suffix entry (annotatedData/stringList/model). A model never matches a
    scalar/array/dict expectation (handled by the caller). Coarse by
    necessity: an annotatedData cell is always treated as number-shaped, a
    stringList entry as string-shaped: enum membership can never be verified
    this way (there is no literal value to check it against), so an
    enum-constrained StringOrRef field referencing a task output can only be
    checked at this coarse "string family" level, never rejected on enum
    grounds."""
    mapped = {"annotatedData": "number", "stringList": "string"}.get(actual_declared_type)
    if mapped is None:
        return None
    return mapped == expected


def _constant_target_kind(final_value):
    """(kind, description) of a constant's (fully indexed) literal value for
    SEDBase-0016/-0017: a number/string/boolean/array is AnnotatedData
    (ProposedRules.md: a scalar is AnnotatedData, an array is unlabeled
    AnnotatedData), an object is neither a model nor AnnotatedData. A JSON
    null is not decidable (None)."""
    if isinstance(final_value, bool):
        return "annotatedData", "a boolean"
    if isinstance(final_value, (int, float)):
        return "annotatedData", "a number"
    if isinstance(final_value, str):
        return "annotatedData", "a string"
    if isinstance(final_value, list):
        return "annotatedData", "an array"
    if isinstance(final_value, dict):
        return "object", "an object"
    return None, ""


def _output_target_kind(entry):
    """(kind, description) of a task-output suffix entry, from its
    outputs.json "type" (model/annotatedData/stringList), for
    SEDBase-0016/-0017; (None, "") when the entry declares no type."""
    declared = entry.get("type") if entry else None
    if declared == "model":
        return "model", "a model"
    if declared == "annotatedData":
        return "annotatedData", "an annotatedData value"
    if declared == "stringList":
        return "annotatedData", "a stringList value"
    return None, ""


def _check_ref_target(ref_target, kind, description, **kwargs) -> list:
    """SEDBase-0016 ("model") / SEDBase-0017 ("annotatedData") dispatch.
    A tree without those rules (a different spec) degrades to a no-op."""
    try:
        from ._rules import sedbase_0016, sedbase_0017
    except ImportError:
        return []
    if ref_target == "model":
        return list(sedbase_0016.check(kind, description, **kwargs))
    if ref_target == "annotatedData":
        return list(sedbase_0017.check(kind, description, **kwargs))
    return []


def _ref_type_problem(ref_type_rule_id, location, attr, value, class_name, id_value, resolved_desc):
    return make_problem(
        ref_type_rule_id, location, attr=attr, value=value,
        **{"class": class_name, "id": id_value, "resolved-value": resolved_desc})


def _check_constant_accessor(parsed, resolved, document, sedbase_0008, sedbase_0012, *,
                              class_name, id_value, attr, location, value,
                              field_kind, ref_type_rule_id, expected_enum, constraints=None,
                              ref_target=None) -> list:
    kwargs = dict(class_name=class_name, id_value=id_value, attr=attr, location=location,
                  make_problem=make_problem, value=value)
    dot_name = next((v for k, v in parsed.accessors if k == "dot"), None)
    if dot_name is not None:
        # SEDBase-0008.md: "For a constants ... target, no dot-accessor is
        # valid."
        return list(sedbase_0008.check(False, dot_name, **kwargs))
    from . import outputs_shape as _oshape
    index_accessors = [v for k, v in parsed.accessors if k == "index"]
    const_value = resolved
    if isinstance(const_value, str) and is_reference(const_value):
        # SEDBase-0012.md: "A constant whose value is itself a reference is
        # followed first." One hop only - a constant-of-a-constant chain
        # deeper than that isn't a documented case.
        inner_parsed = _parse_reference(const_value)
        inner_resolved, _ = get_sed_reference(document, inner_parsed)
        const_value = inner_resolved
    try:
        final_value = _oshape.index_into_literal(const_value, index_accessors)
    except _oshape.NotIndexable as e:
        bad = e.args[0] if e.args else ""
        return list(sedbase_0012.check(False, bad, _fmt_literal(const_value), **kwargs))
    if ref_target is not None:
        kind, description = _constant_target_kind(final_value)
        return _check_ref_target(ref_target, kind, description, **kwargs)
    if ref_type_rule_id is None or field_kind not in _REF_TYPE_KINDS:
        return []
    if _literal_matches_kind(final_value, field_kind, expected_enum, constraints) is False:
        return [_ref_type_problem(ref_type_rule_id, location, attr, value, class_name, id_value,
                                  _fmt_literal(final_value))]
    return []


def _check_output_shape_and_ref_type(parsed, resolved, document, *, class_name, id_value, attr, location,
                                      value, field_kind, ref_type_rule_id, expected_enum,
                                      constraints=None, ref_target=None) -> list:
    try:
        from ._rules import sedbase_0008, sedbase_0009, sedbase_0010, sedbase_0011, sedbase_0012, sedbase_0014, sedbase_0015
    except ImportError:
        # This tree's own model.rules never defined SEDBase-0008 (a
        # different spec tree with no outputs.json-shaped tasks/ vocabulary
        # at all) - degrade to a no-op, matching every other handwritten-
        # rule dispatcher's ImportError guard in this module.
        return []

    if parsed.collection == "constants":
        return _check_constant_accessor(
            parsed, resolved, document, sedbase_0008, sedbase_0012,
            class_name=class_name, id_value=id_value, attr=attr, location=location, value=value,
            field_kind=field_kind, ref_type_rule_id=ref_type_rule_id, expected_enum=expected_enum,
            constraints=constraints, ref_target=ref_target)

    kwargs = dict(class_name=class_name, id_value=id_value, attr=attr, location=location,
                  make_problem=make_problem, value=value)
    outputs_json = getattr(resolved, "_OUTPUTS_JSON", None)
    if outputs_json is None:
        # styles / outputs-collection-but-already-handled-above / a nested
        # non-tasks/-class element reached via a tasks: path (LoopVariable,
        # TaskParameter, ...) - SEDBase-0008.md's "For a constants,
        # loopVariables, or styles target, no dot-accessor is valid"
        # category. A bare reference (no accessor at all) is always fine
        # for these - only a dot-accessor on top is invalid - and there's
        # no outputs.json-driven shape to check brackets against either
        # way, so this dispatcher goes no further for them.
        dot_name = next((v for k, v in parsed.accessors if k == "dot"), None)
        if dot_name is None:
            return []
        return list(sedbase_0008.check(False, dot_name, **kwargs))

    from . import outputs_shape as _oshape
    depth = [0]

    def shape_of(ref_string):
        depth[0] += 1
        if depth[0] > 25:
            raise _oshape.NotStatic("shapeOf() recursion too deep")
        parsed2 = _parse_reference(ref_string)
        inner, _ = get_sed_reference(document, parsed2)
        inner_outputs_json = getattr(inner, "_OUTPUTS_JSON", None) if inner is not None else None
        if inner_outputs_json is None:
            raise _oshape.NotStatic("shapeOf() target has no outputs.json")
        inner_ok, _entry, _before, inner_after, _dot, _idx = _oshape.resolve_output(
            inner_outputs_json, inner._own_json_value(), parsed2.accessors, shape_of)
        if inner_ok is not True or inner_after is None:
            raise _oshape.NotStatic("shapeOf() target shape not statically known")
        return inner_after

    ok, entry, dims_before, dims_after, dot_name, index_accessors = _oshape.resolve_output(
        outputs_json, resolved._own_json_value(), parsed.accessors, shape_of)

    problems = list(sedbase_0008.check(ok, dot_name, **kwargs))
    if ok is not True:
        return problems
    problems += sedbase_0009.check(dims_before, index_accessors, **kwargs)
    problems += sedbase_0010.check(dims_before, index_accessors, **kwargs)
    problems += sedbase_0011.check(dims_before, index_accessors, **kwargs)
    problems += sedbase_0014.check(dims_before, index_accessors, **kwargs)

    if ref_target is not None:
        kind, description = _output_target_kind(entry)
        problems += _check_ref_target(ref_target, kind, description, **kwargs)
    if ref_type_rule_id is not None and field_kind in _REF_TYPE_KINDS:
        actual_declared = entry.get("type") if entry else None
        if actual_declared == "model":
            # A model is a type of its own: never a number, string, boolean,
            # array, or dictionary (ProposedRules.md).
            problems.append(_ref_type_problem(
                ref_type_rule_id, location, attr, value, class_name, id_value, "a model"))
        elif field_kind in _SCALAR_ORREF_EXPECTED:
            expected = _SCALAR_ORREF_EXPECTED[field_kind]
            problems += sedbase_0015.check(dims_after, expected, **kwargs)
            if dims_after is not None and len(dims_after) == 0:
                if _ref_type_matches_declared(expected, actual_declared) is False:
                    problems.append(_ref_type_problem(
                        ref_type_rule_id, location, attr, value, class_name, id_value,
                        f"a {actual_declared} value"))
        elif field_kind == "ArrayOrRef":
            # Only the unambiguous mismatch: an array of numbers fed a
            # stringList output. (annotatedData may carry labels, so an
            # array of strings from annotatedData is not flagged.)
            item_kind = constraints[2] if constraints else None
            if item_kind == "number" and actual_declared == "stringList":
                problems.append(_ref_type_problem(
                    ref_type_rule_id, location, attr, value, class_name, id_value,
                    "a stringList value"))
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
    # SEDBase-0005.md: the root-collection rule also applies to a REFERENCE
    # token embedded in a math string.
    try:
        from ._rules import sedbase_0005
    except ImportError:
        sedbase_0005 = None
    if sedbase_0005 is not None:
        for node in ast.walk():
            if node.is_reference():
                problems = problems + sedbase_0005.check(
                    _parse_reference(node.text), class_name=class_name, id_value=id_value,
                    attr=attr, location=location, make_problem=make_problem)
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


def leaf_schema_for(kind: str, minimum=None, exclusive_minimum=None, pattern=None,
                     min_length=None, enum=None) -> dict:
    base = dict(_LEAF_SCHEMAS[kind])
    # minimum/exclusiveMinimum are numeric-only JSON Schema keywords - a
    # no-op against a non-numeric instance (a reference string, for an
    # *OrRef kind) per the JSON Schema spec, so bolting them on at the top
    # level (sibling to "anyOf") is always safe.
    if minimum is not None:
        base = {**base, "minimum": minimum}
    if exclusive_minimum is not None:
        base = {**base, "exclusiveMinimum": exclusive_minimum}
    string_constraints = {}
    if pattern is not None:
        string_constraints["pattern"] = pattern
    if min_length is not None:
        string_constraints["minLength"] = min_length
    if enum is not None:
        string_constraints["enum"] = list(enum)
    if string_constraints:
        if kind == "StringOrRef":
            # Unlike minimum/exclusiveMinimum above, pattern/minLength/enum
            # are STRING-only keywords - and a StringOrRef's reference form
            # is *also* a plain string, so bolting these on at the top level
            # would incorrectly reject a perfectly valid reference too (it
            # isn't a no-op the way a numeric keyword is against a string
            # instance). Split explicitly into "the literal value, meeting
            # these constraints" vs. "a reference-shaped string" instead of
            # _LEAF_SCHEMAS["StringOrRef"]'s own single unconstrained
            # {"type": "string"} branch.
            base = {"anyOf": [
                {"type": "string", **string_constraints},
                {"type": "string", "pattern": SIDREF_PATTERN.pattern},
            ]}
        else:
            # "string"/"SId"/"SIdRef" - never a reference alternative to
            # worry about, so a direct bolt-on is fine (SId/SIdRef never
            # actually carry these - _classify_type returns them without
            # collecting further constraints - but handled generically
            # rather than asserting that stays true).
            base = {**base, **string_constraints}
    return base


def leaf_value_ok(kind: str, value: Any, minimum=None, exclusive_minimum=None, pattern=None,
                   min_length=None, enum=None) -> bool:
    schema = leaf_schema_for(kind, minimum, exclusive_minimum, pattern, min_length, enum)
    try:
        jsonschema.validate(value, schema)
        return True
    except jsonschema.ValidationError:
        return False


class FieldSpec:
    __slots__ = ("name", "kind", "required", "rule_id", "required_rule_id",
                 "origin_catchall", "minimum", "exclusive_minimum", "pattern",
                 "item_class", "item_discriminator", "is_math", "min_length",
                 "enum", "ref_type_rule_id", "item_kind", "ref_target")

    def __init__(self, name, kind, required, rule_id, required_rule_id,
                 origin_catchall, minimum=None, exclusive_minimum=None,
                 pattern=None, item_class=None, item_discriminator=None,
                 is_math=False, min_length=None, enum=None, ref_type_rule_id=None,
                 item_kind=None, ref_target=None):
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
        self.min_length = min_length
        self.enum = enum
        self.ref_type_rule_id = ref_type_rule_id
        self.item_kind = item_kind
        self.ref_target = ref_target


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
    # core-spec.md Section 8's per-class outputs.json envelope (see
    # emit_model_py's own per-class attribute emission below) - None for
    # every class except a concrete tasks/ one, matching FlatClass.
    # outputs_json's own None default (Design.md's Validation section,
    # SEDBase-0008 through -0015).
    _OUTPUTS_JSON: Optional[dict] = None
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
                if not leaf_value_ok(spec.kind, value, spec.minimum, spec.exclusive_minimum, spec.pattern,
                                      spec.min_length, spec.enum):
                    rid = spec.rule_id or spec.origin_catchall
                    extra = {"class": self.__class__.__name__, "id": self._own_id_for_message(),
                             "value": value}
                    if spec.enum is not None:
                        # A rule fired from an enum-constrained leaf's own
                        # message template may reference {allowed} (e.g.
                        # Curve-0002/Surface's own curveType/surfaceType
                        # rules) - harmless to always include, since
                        # _fmt_message only substitutes placeholders the
                        # template actually names.
                        extra["allowed"] = ", ".join(repr(v) for v in spec.enum)
                    problems.append(make_problem(rid, "/" + spec.name, attr=spec.name, **extra))
                elif spec.kind in _REFERENCE_CAPABLE_KINDS and is_reference(value):
                    problems.extend(_check_reference_field(
                        value, document=self.get_document(), class_name=self.__class__.__name__,
                        id_value=self._own_id_for_message(), attr=spec.name, location="/" + spec.name,
                        referrer=self, field_kind=spec.kind, ref_type_rule_id=spec.ref_type_rule_id,
                        expected_enum=spec.enum,
                        constraints=(spec.minimum, spec.exclusive_minimum, spec.item_kind),
                        ref_target=spec.ref_target))
                elif spec.kind == "DictOrRef" and isinstance(value, dict):
                    # The dict-literal branch of a DictOrRef field (e.g.
                    # Repeat.outputVariableMap: an SId-keyed map of column
                    # name -> SIdRef) - is_reference(value) above is False
                    # for this whole-field-is-a-dict shape, so each entry
                    # gets its OWN reference-resolution dispatch here
                    # (SEDBase-0005 through -0015, same as any other
                    # reference-capable field) rather than the field as a
                    # single unit. ref_type_rule_id is deliberately omitted
                    # (None) - the field's own ref_type_rule_id describes
                    # what the WHOLE FIELD must resolve to when IT is a
                    # reference (the other anyOf branch, handled above),
                    # not what each entry's own target must be; no per-entry
                    # expected type is declared for a DictOrRef's dict-form
                    # (Design.md's Validation section note on this scope
                    # limitation - see _REF_TYPE_KINDS's own comment in
                    # this module).
                    for key, entry_value in value.items():
                        if is_reference(entry_value):
                            problems.extend(_check_reference_field(
                                entry_value, document=self.get_document(),
                                class_name=self.__class__.__name__,
                                id_value=self._own_id_for_message(), attr=spec.name,
                                location=f"/{spec.name}/{key}",
                                referrer=self, field_kind=spec.kind,
                                ref_type_rule_id=None, expected_enum=None))
                elif spec.kind == "ArrayOrRef" and isinstance(value, list):
                    # The array-literal branch of an ArrayOrRef field: each
                    # element that is itself a reference gets its own
                    # reference-resolution dispatch (SEDBase-0005.md: the rule
                    # applies to "an element of an array or object value"),
                    # with no per-element expected type - same scope as the
                    # DictOrRef dict-literal branch above.
                    for idx, entry_value in enumerate(value):
                        if is_reference(entry_value):
                            problems.extend(_check_reference_field(
                                entry_value, document=self.get_document(),
                                class_name=self.__class__.__name__,
                                id_value=self._own_id_for_message(), attr=spec.name,
                                location=f"/{spec.name}/{idx}",
                                referrer=self, field_kind=spec.kind,
                                ref_type_rule_id=None, expected_enum=None))
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
                    id_value=self._own_id_for_message(), attr=spec.name, location="/" + spec.name,
                    referrer=self, field_kind="any", ref_type_rule_id=None, expected_enum=None))
        if self._IS_DOCUMENT_CLASS:
            problems.extend(_check_namespace_usage_and_version(self))
            problems.extend(_check_constants_ordering(self))
        # Repeat-0008/-0009/-0010 (own-subTasks scoping for a Repeat-family
        # instance's outputVariableMap/aggregateOutputVariables) and
        # LoopVariable-0004 (own-Loop scoping for subsequentValues) each
        # internally no-op for every class they don't apply to (a cheap
        # class-shape check, not a class-name check - see their own
        # docstrings) - called unconditionally here, the same as every
        # other per-instance handwritten check above.
        problems.extend(_check_repeat_own_children(self))
        problems.extend(_check_loop_variable_scope(self))
        return problems

    def _id_collection_names(self) -> list:
        """Every id-keyed collection field name THIS class declares (see
        emit_model_py's own per-class emission) - the default here (empty)
        covers every class with none (a leaf class with no dict/any-dict
        field of its own, and every discriminator's own Unknown* holder,
        which never overrides this). Used only by _own_id_for_message
        below, which needs to search a PARENT's own collections for self -
        _get_id_collection(name) already does the actual lookup once a
        name is in hand, this just enumerates the names to try."""
        return []

    def _own_id_for_message(self) -> str:
        """This element's own SId, for a validation message's {id}
        placeholder - Design.md's Classes section: id is implicit, the key
        under which an element is stored in its owning collection, never a
        field on the element itself (see spec.py's own field-flattening,
        which never produces an 'id' FieldSpec). So this walks up to the
        parent and searches every id-keyed collection IT declares for
        whichever key maps to self - generic over every concrete class,
        with no per-class override needed. Falls back to '?' for anything
        genuinely id-less: the document root (no parent at all), an
        array-item class (TaskParameter, WorkingAlgorithm, ...) stored
        positionally rather than by id, or an unattached/standalone
        instance no parent has claimed yet."""
        parent = self.get_parent()
        if parent is None:
            return "?"
        for name in parent._id_collection_names():
            coll = parent._get_id_collection(name)
            if coll is None:
                continue
            for iid in coll.ids():
                if coll.get(iid) is self:
                    return iid
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


# outputs.json expr/valid notation (core-spec.md Section 8) - parser,
# evaluator, shape/hasSubvalue() resolver. Hand-authored (not per-class
# generated data), same treatment as MATH_AST_PY above - written verbatim
# into every generated Python package as outputs_shape.py, imported lazily
# by _check_reference_field's own SEDBase-0008..-0015/ref-type dispatch
# (see that function's docstring in RUNTIME above).
OUTPUTS_SHAPE_PY = r'''"""outputs.json expr/valid notation (core-spec.md Section 8) - parser,
evaluator, and shape/hasSubvalue() resolver, backing SEDBase-0008 through
-0015 (Design.md's Validation section) and the formulaic ref-type rules
that piggyback on SEDBase-0015's scalar-reduction check. GENERATED - do not
hand-edit; regenerate via generator/generate.py.

Design choice (documented, not silent): core-spec.md's own wording for this
notation is "the generator... compil[es] it into real code in each target
language... rather than shipping a small runtime interpreter". This module
IS a small runtime interpreter - a deliberate, narrower reading of that
sentence: the alternative (a bespoke Python function generated per
outputs.json suffix entry, one per concrete tasks/ class) would multiply
authorship effort by the number of suffix entries in the whole spec for no
behavioral difference, since walking a handful-of-nodes AST against an
in-memory dict costs nothing at validate() time. This mirrors the ONE other
precedent already in this codebase for a small expression language:
math_ast.py's ANTLR-generated grammar still gets walked by hand-written,
non-per-field interpretation code in the Types-0002/-0003/-0004 rule files,
not compiled into bespoke functions either. What core-spec.md's sentence
does rule out, and what this module doesn't do, is re-deriving the
notation's *grammar* independently per language - the notation itself is
parsed exactly once, right here, the same "one canonical definition" the
math grammar and the schema tree already get.
"""
from __future__ import annotations


class NotStatic(Exception):
    """Raised whenever an expr can't be evaluated against the target's own
    literal fields - a reference where a literal was needed, a missing
    attribute, an unresolvable shape dependency, a cycle/depth guard, and so
    on. Every caller catches this and treats it as "the rule does not fire"
    (SEDBase-0008 through -0011/-0014's own "only fires when computable"
    language) rather than as an error."""


# ---- lexer ------------------------------------------------------------

def _tokenize(text: str) -> list:
    toks = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch == "=" and text[i:i + 2] == "==":
            toks.append(("==", "==")); i += 2; continue
        if ch in "+-!(),[].":
            toks.append((ch, ch)); i += 1; continue
        if ch.isdigit() or (ch == "." and i + 1 < n and text[i + 1].isdigit()):
            j = i
            while j < n and (text[j].isdigit() or text[j] == "."):
                j += 1
            toks.append(("NUMBER", text[i:j])); i = j; continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            word = text[i:j]
            if word in ("true", "false"):
                toks.append(("BOOL", word))
            elif word in ("or", "if", "else"):
                toks.append((word, word))
            else:
                toks.append(("IDENT", word))
            i = j
            continue
        raise NotStatic(f"unexpected character {ch!r} in expr {text!r}")
    toks.append(("EOF", ""))
    return toks


# ---- AST ----------------------------------------------------------------

class Num:
    __slots__ = ("value",)
    def __init__(self, value): self.value = value

class Bool:
    __slots__ = ("value",)
    def __init__(self, value): self.value = value

class ArrayLit:
    __slots__ = ("items",)
    def __init__(self, items): self.items = items

class Path:
    __slots__ = ("names",)
    def __init__(self, names): self.names = names

class Call:
    __slots__ = ("func", "args")
    def __init__(self, func, args): self.func = func; self.args = args

class UnaryNot:
    __slots__ = ("operand",)
    def __init__(self, operand): self.operand = operand

class BinOp:
    __slots__ = ("op", "left", "right")
    def __init__(self, op, left, right): self.op = op; self.left = left; self.right = right

class Conditional:
    __slots__ = ("cond", "then", "orelse")
    def __init__(self, cond, then, orelse): self.cond = cond; self.then = then; self.orelse = orelse


_FUNCS = ("len", "keys", "shapeOf", "dim", "provided")


class _Parser:
    def __init__(self, toks):
        self.toks = toks
        self.i = 0

    def _peek(self):
        return self.toks[self.i]

    def _eat(self, kind):
        tok = self.toks[self.i]
        if tok[0] != kind:
            raise NotStatic(f"expected {kind}, got {tok}")
        self.i += 1
        return tok

    def parse(self):
        node = self._conditional()
        self._eat("EOF")
        return node

    def _conditional(self):
        node = self._or_expr()
        if self._peek()[0] == "if":
            self._eat("if")
            cond = self._or_expr()
            self._eat("else")
            orelse = self._conditional()
            return Conditional(cond, node, orelse)
        return node

    def _or_expr(self):
        node = self._equality()
        while self._peek()[0] == "or":
            self._eat("or")
            node = BinOp("or", node, self._equality())
        return node

    def _equality(self):
        node = self._additive()
        if self._peek()[0] == "==":
            self._eat("==")
            node = BinOp("==", node, self._additive())
        return node

    def _additive(self):
        node = self._unary()
        while self._peek()[0] in ("+", "-"):
            op = self._eat(self._peek()[0])[0]
            node = BinOp(op, node, self._unary())
        return node

    def _unary(self):
        if self._peek()[0] == "!":
            self._eat("!")
            return UnaryNot(self._unary())
        return self._primary()

    def _primary(self):
        kind, text = self._peek()
        if kind == "NUMBER":
            self._eat("NUMBER")
            return Num(float(text) if "." in text else int(text))
        if kind == "BOOL":
            self._eat("BOOL")
            return Bool(text == "true")
        if kind == "[":
            self._eat("[")
            items = []
            if self._peek()[0] != "]":
                items.append(self._conditional())
                while self._peek()[0] == ",":
                    self._eat(","); items.append(self._conditional())
            self._eat("]")
            return ArrayLit(items)
        if kind == "IDENT":
            name = self._eat("IDENT")[1]
            if self._peek()[0] == "(" and name in _FUNCS:
                self._eat("(")
                args = []
                if self._peek()[0] != ")":
                    args.append(self._conditional())
                    while self._peek()[0] == ",":
                        self._eat(","); args.append(self._conditional())
                self._eat(")")
                return Call(name, args)
            names = [name]
            while self._peek()[0] == ".":
                self._eat("."); names.append(self._eat("IDENT")[1])
            return Path(names)
        raise NotStatic(f"unexpected token {self._peek()} in expr")


_PARSE_CACHE: dict = {}


def parse_expr(text: str):
    node = _PARSE_CACHE.get(text)
    if node is None:
        node = _Parser(_tokenize(text)).parse()
        _PARSE_CACHE[text] = node
    return node


# ---- scopes -------------------------------------------------------------

class _OutermostSentinel:
    def __repr__(self): return "OUTERMOST"


OUTERMOST = _OutermostSentinel()


class Scope:
    """Top-level scope: bare identifiers resolve against a task's own raw
    JSON field values (SedBase._own_json_value()) - core-spec.md: "A bare
    identifier names one of the task's own attributes and evaluates to its
    value"."""
    __slots__ = ("fields",)
    def __init__(self, fields): self.fields = fields

    def lookup(self, name):
        if name not in self.fields:
            raise NotStatic(f"attribute {name!r} not provided")
        return self.fields[name]

    def provided(self, name):
        return name in self.fields


class RepeatScope:
    """core-spec.md's repeat-entry scoping: bare identifiers resolve against
    the CURRENT array entry's own fields, and `self` refers to the entry as
    a whole."""
    __slots__ = ("entry", "outer")
    def __init__(self, entry, outer): self.entry = entry; self.outer = outer

    def lookup(self, name):
        if name == "self":
            return self.entry
        if not isinstance(self.entry, dict) or name not in self.entry:
            raise NotStatic(f"attribute {name!r} not provided on repeat entry")
        return self.entry[name]

    def provided(self, name):
        if name == "self":
            return True
        return isinstance(self.entry, dict) and name in self.entry


# ---- evaluation -----------------------------------------------------------

def _is_ref_value(value):
    return isinstance(value, str) and value.startswith("#")


def _resolve_path(node, scope):
    if node.names[0] == "outermost":
        if len(node.names) != 1:
            raise NotStatic("outermost is not a container")
        return OUTERMOST
    value = scope.lookup(node.names[0])
    for seg in node.names[1:]:
        if not isinstance(value, dict) or seg not in value:
            raise NotStatic(f"attribute {'.'.join(node.names)!r} not provided")
        value = value[seg]
    return value


def _is_provided(node, scope):
    if not isinstance(node, Path):
        raise NotStatic("provided() needs a bare identifier or dotted path")
    if node.names[0] == "outermost":
        return True
    if len(node.names) == 1:
        return scope.provided(node.names[0])
    try:
        value = scope.lookup(node.names[0])
    except NotStatic:
        return False
    for seg in node.names[1:-1]:
        if not isinstance(value, dict) or seg not in value:
            return False
        value = value[seg]
    return isinstance(value, dict) and node.names[-1] in value


def _fn_len(value):
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        # Range-family dispatch (core-spec.md): len(x.values) if
        # provided(x.values) else x.numberOfSteps + 1 for NumericRange/
        # ParameterRange; just len(x.values) for a bare Range. Covered
        # generically by this shape-based dispatch rather than naming the
        # discriminator consts explicitly. Anything else object-shaped is a
        # plain SId-keyed map (outputVariableMap, aggregateOutputVariables,
        # CreateDataBlock.data) - len() there just means key count, the
        # same as keys(x)'s own array's length would be.
        if "values" in value:
            values = value["values"]
            if isinstance(values, list):
                return len(values)
            raise NotStatic("values is not a literal array")
        if "numberOfSteps" in value:
            steps = value["numberOfSteps"]
            if isinstance(steps, (int, float)) and not isinstance(steps, bool):
                return int(steps) + 1
            raise NotStatic("numberOfSteps is not a literal number")
        return len(value)
    raise NotStatic("len() needs a literal array, object, or Range-family value")


def _fn_keys(value):
    if not isinstance(value, dict):
        raise NotStatic("keys() needs a literal object")
    return list(value.keys())


def eval_expr(node, scope, shape_of):
    if isinstance(node, Num):
        return node.value
    if isinstance(node, Bool):
        return node.value
    if isinstance(node, ArrayLit):
        return [eval_expr(item, scope, shape_of) for item in node.items]
    if isinstance(node, Path):
        return _resolve_path(node, scope)
    if isinstance(node, UnaryNot):
        return not bool(eval_expr(node.operand, scope, shape_of))
    if isinstance(node, Call):
        if node.func == "provided":
            if len(node.args) != 1:
                raise NotStatic("provided() takes exactly one argument")
            return _is_provided(node.args[0], scope)
        if node.func == "len":
            return _fn_len(eval_expr(node.args[0], scope, shape_of))
        if node.func == "keys":
            return _fn_keys(eval_expr(node.args[0], scope, shape_of))
        if node.func == "shapeOf":
            ref = eval_expr(node.args[0], scope, shape_of)
            if not isinstance(ref, str) or not ref.startswith("#"):
                raise NotStatic("shapeOf() needs a reference-valued operand")
            return shape_of(ref)
        if node.func == "dim":
            if len(node.args) != 1:
                raise NotStatic("dim() takes exactly one argument")
            value = eval_expr(node.args[0], scope, shape_of)
            if value is OUTERMOST:
                return [OUTERMOST]
            if isinstance(value, str):
                return [value]
            if isinstance(value, list):
                return value
            raise NotStatic("dim() needs a name or a list of names")
        raise NotStatic(f"unknown function {node.func}()")
    if isinstance(node, BinOp):
        if node.op == "or":
            if _is_provided(node.left, scope):
                return eval_expr(node.left, scope, shape_of)
            return eval_expr(node.right, scope, shape_of)
        left = eval_expr(node.left, scope, shape_of)
        if node.op == "-":
            # The only place "-" appears: shapeOf(x) - dim(y). `left` is a
            # resolved dims list (or None); `right` is a list of dimension
            # selectors from dim(). Handled inline (rather than deferred, as
            # an earlier draft of this module did) since both operands are
            # fully evaluated by this point anyway.
            right = eval_expr(node.right, scope, shape_of)
            return _apply_dim_minus(left, right)
        right = eval_expr(node.right, scope, shape_of)
        if node.op == "==":
            # A reference-valued operand (for example outputModel given as
            # "#constants:flag") has no statically known value, so the
            # comparison is not statically evaluable.
            if _is_ref_value(left) or _is_ref_value(right):
                raise NotStatic("== operand is a reference")
            return left == right
        if node.op == "+":
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            if isinstance(left, (int, float)) and not isinstance(left, bool) \
                    and isinstance(right, (int, float)) and not isinstance(right, bool):
                return left + right
            raise NotStatic("+ needs two arrays or two numbers")
        raise NotStatic(f"unknown operator {node.op}")
    if isinstance(node, Conditional):
        if bool(eval_expr(node.cond, scope, shape_of)):
            return eval_expr(node.then, scope, shape_of)
        return eval_expr(node.orelse, scope, shape_of)
    raise NotStatic(f"unknown AST node {node!r}")


def _apply_dim_minus(dims, selectors):
    """shapeOf(x) - dim(y): a dims list (see resolve_dims) with the
    dimension(s) named by `selectors` removed. This data model has no
    per-dimension naming beyond the reserved `outermost` sentinel (see this
    module's own docstring on dim()), so only that one case removes a
    SPECIFIC, still-fully-known dimension (the first); anything else can
    only shrink the known dimension COUNT, with the remaining dimensions'
    own details marked unknown rather than guessing which slot(s) a name
    like `appliedDimensions` was meant to select - safe (never mis-fires a
    downstream rule) even though it under-reports what SEDBase-0010/-0011
    could otherwise catch for those remaining dimensions."""
    if dims is None:
        return None
    count = len(selectors) if isinstance(selectors, list) else 1
    if count >= len(dims):
        return []
    if selectors == [OUTERMOST]:
        return dims[1:]
    return [{"size": None, "labels": None, "source": "runtime", "min": None}
            for _ in range(len(dims) - count)]


# ---- outputs.json "sourced" value resolution -----------------------------

def _eval_sourced_size(sourced, scope, shape_of):
    if sourced is None:
        return None
    if sourced.get("source") != "static":
        return None  # runtime / input-file - not statically known
    try:
        value = eval_expr(parse_expr(sourced["expr"]), scope, shape_of)
    except NotStatic:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return int(value)
    return None


def _eval_sourced_labels(labels_spec, scope, shape_of):
    """None (JSON null) means "no labels for this dimension" - statically
    known as empty, not "unresolvable" - so this returns [] for that case,
    reserving None for a genuine failure to resolve."""
    if labels_spec is None:
        return []
    if isinstance(labels_spec, list):
        return labels_spec
    if isinstance(labels_spec, dict):
        if labels_spec.get("source") != "static":
            return None
        try:
            value = eval_expr(parse_expr(labels_spec["expr"]), scope, shape_of)
        except NotStatic:
            return None
        if isinstance(value, list) and all(isinstance(v, str) for v in value):
            return value
        return None
    return None


def resolve_dims(dims_spec, scope, shape_of):
    """dims_spec is outputs.json's own "dimensions" value for one suffix
    entry (see schema/outputs-meta.schema.json's $defs/dimensions) - either
    a fixed-length array of per-dimension entries, or a single "sourced"
    object describing the whole shape. Returns a list of
    {"size": int|None, "labels": list[str]|None, "source": str, "min":
    int|None} - one per dimension, in order - or None when the dimension
    COUNT itself isn't statically known (a whole-shape runtime/input-file
    source, or a static expr that didn't evaluate to a resolved dims list)."""
    if dims_spec is None:
        return None
    if isinstance(dims_spec, list):
        result = []
        for d in dims_spec:
            if "repeat" in d:
                rep = d["repeat"]
                try:
                    over_val = scope.lookup(rep["over"])
                except NotStatic:
                    return None
                if not isinstance(over_val, list):
                    return None
                for item in over_val:
                    item_scope = RepeatScope(item, scope)
                    result.append({
                        "size": _eval_sourced_size(rep["size"], item_scope, shape_of),
                        "labels": _eval_sourced_labels(rep.get("labels"), item_scope, shape_of),
                        "source": rep["size"].get("source"),
                        "min": rep["size"].get("min"),
                    })
            else:
                result.append({
                    "size": _eval_sourced_size(d["size"], scope, shape_of),
                    "labels": _eval_sourced_labels(d.get("labels"), scope, shape_of),
                    "source": d["size"].get("source"),
                    "min": d["size"].get("min"),
                })
        return result
    # single sourced object - the whole shape's derivation
    if dims_spec.get("source") != "static":
        return None  # runtime / input-file - dimension count itself unknown
    try:
        value = eval_expr(parse_expr(dims_spec["expr"]), scope, shape_of)
    except NotStatic:
        return None
    return value if isinstance(value, list) else None


def _apply_index_chain(dims, index_accessors):
    """Applies a reference's own bracket-index chain to a resolved dims
    list, left-to-right, each index against the CORRESPONDING original
    dimension position (a range at position 0 doesn't renumber position 1 -
    ordinary multi-axis indexing semantics). A positional/label index drops
    its dimension from the result; a range keeps it (core-spec.md's
    Grammar); a dimension beyond the index chain's own length passes
    through untouched."""
    if dims is None:
        return None
    result = []
    for i, d in enumerate(dims):
        if i < len(index_accessors):
            if index_accessors[i].kind == "range":
                result.append(d)
            # positional/label -> dimension dropped
        else:
            result.append(d)
    return result


def eval_valid(entry, scope, shape_of):
    """A suffix entry that is listed in outputs.json is valid; one that
    isn't listed is not (resolve_output handles that). An entry's optional
    "valid" field is a boolean expr string over the task's own fields
    meaning "valid if". No "valid" field: always valid. Returns True/False,
    or None when the expr couldn't be evaluated statically (SEDBase-0008:
    "the rule does not fire" in that case)."""
    valid = entry.get("valid")
    if valid is None:
        return True
    if isinstance(valid, str):
        try:
            return bool(eval_expr(parse_expr(valid), scope, shape_of))
        except NotStatic:
            return None
    return False


def resolve_output(outputs_json, fields, accessors, shape_of):
    """The core hasSubvalue()-style resolution SEDBase-0008 through -0011/
    -0014/-0015 and the ref-type rules all share. `outputs_json` is a
    concrete tasks/ class's own parsed outputs.json ({"outputs": {...}});
    `fields` is the referenced task's own _own_json_value() dict; `accessors`
    is a ParsedReference's own .accessors list. Returns (accessor_ok, entry,
    dims_before, dims_after, dot_name, index_accessors):
      - accessor_ok: True (the suffix is listed and has no "valid" field,
        or its "valid" ("valid if") expr evaluated true), False (suffix
        not listed, or its "valid" expr evaluated false), or None
        (couldn't be determined statically - every caller treats this the
        same as False for "don't fire a positive claim" but ALSO suppresses
        every rule that would need to know for sure, per the "only fires
        when computable" convention).
      - entry: the raw outputEntry dict, or None if the suffix key itself
        isn't present in outputs.json at all.
      - dims_before / dims_after: resolve_dims()'s own result, before and
        after applying the index chain (see _apply_index_chain) - both None
        whenever accessor_ok isn't True, or whenever entry has no
        "dimensions" at all (a "model"-typed suffix, which has no shape
        concept to index into in the first place).
      - dot_name: the first ('dot', name) accessor's name, or None for a
        bare [id] reference.
      - index_accessors: every ('index', RefIndex) accessor, in order,
        regardless of where it fell relative to a dot accessor.
    """
    dot_name = None
    index_accessors = []
    for kind, val in accessors:
        if kind == "dot" and dot_name is None:
            dot_name = val
        elif kind == "index":
            index_accessors.append(val)
    suffix_key = "[id]" if dot_name is None else f"[id].{dot_name}"
    entry = (outputs_json or {}).get("outputs", {}).get(suffix_key)
    if entry is None:
        return False, None, None, None, dot_name, index_accessors
    scope = Scope(fields)
    ok = eval_valid(entry, scope, shape_of)
    if ok is not True:
        return ok, entry, None, None, dot_name, index_accessors
    dims_before = resolve_dims(entry.get("dimensions"), scope, shape_of)
    dims_after = _apply_index_chain(dims_before, index_accessors)
    return True, entry, dims_before, dims_after, dot_name, index_accessors


# ---- SEDBase-0012: indexing into a constant's own literal JSON value ------

class NotIndexable(Exception):
    """Raised by index_into_literal when the index chain can't be applied
    to the constant's own literal structure - the signal SEDBase-0012
    fires on."""


def index_into_literal(value, index_accessors):
    """core-spec.md / SEDBase-0012.md: constants have no outputs.json,
    their "shape" is just their own literal JSON value. Applies an index
    chain directly against it, following one level of reference first if
    the constant's own value is itself a reference string (SEDBase-0012.md:
    "A constant whose value is itself a reference is followed first") -
    callers pass an already-dereferenced `value` (see the RUNTIME dispatcher
    for the one-hop-then-stop resolution, mirroring how deeply nested
    constants-of-constants aren't a documented case). Raises NotIndexable
    the moment an index can't apply; returns the fully-indexed literal value
    otherwise (used by the ref-type check too, once indexing succeeds)."""
    cur = value
    for idx in index_accessors:
        if idx.kind == "label":
            if not isinstance(cur, dict) or idx.value not in cur:
                raise NotIndexable(idx.value)
            cur = cur[idx.value]
        elif idx.kind == "int":
            if not isinstance(cur, list):
                raise NotIndexable(idx.value)
            n = len(cur)
            i = idx.value
            if i < -n or i >= n:
                raise NotIndexable(idx.value)
            cur = cur[i]
        elif idx.kind == "range":
            if not isinstance(cur, list):
                raise NotIndexable(idx.value)
            a, b = idx.value
            n = len(cur)
            ea = a if a is not None else 0
            eb = b if b is not None else n
            if ea < 0: ea += n
            if eb < 0: eb += n
            cur = cur[max(ea, 0):max(eb, 0)]
        else:
            raise NotIndexable(idx.value)
    return cur
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
            "pattern=%r, item_class=%r, item_discriminator=%r, is_math=%r, "
            "min_length=%r, enum=%r, ref_type_rule_id=%r, item_kind=%r, ref_target=%r)" % (
                f.name, t.kind, f.required, f.rule_id, f.required_rule_id,
                f"{f.origin_class}-0000", t.minimum, t.exclusive_minimum,
                t.pattern, t.item_class, t.item_discriminator, f.is_math,
                t.min_length, t.enum, f.ref_type_rule_id, t.item_kind, f.ref_target,
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


def _child_accessors(f: Field) -> str:
    """A single nested SedBase-derived child, stored directly on the
    instance (self._{py}), not in an IdKeyedCollection/ListCollection -
    there is exactly zero or one of it, and it has no id of its own
    (unlike a dict-kind field's items). Covers both "ref-class" (a fixed
    target class, e.g. ExplicitODESimulation.independentVariableRange ->
    NumericRange) and "ref-discriminator" (a _type-dispatched target,
    e.g. Repeat.range -> RangeInline's NumericRange/VectorRange/...) - the
    accessors themselves don't care which; only _load_fields's own parsing
    (see emit_model_py) needs to tell them apart, to know whether to
    construct a fixed class or dispatch on the raw JSON's own _type."""
    py = _pyname(f.name)
    lines = []
    lines.append(
        f"    def get_{py}(self):\n"
        f"        if self._{py} is None: raise ApiError({py + ' is not set'!r})\n"
        f"        return self._{py}\n"
    )
    lines.append(
        f"    def set_{py}(self, obj):\n"
        f"        self._{py} = obj; obj._attach(self, self.get_document())\n"
    )
    lines.append(f"    def is_set_{py}(self):\n        return self._{py} is not None\n")
    lines.append(f"    def unset_{py}(self):\n        self._{py} = None\n")
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
        # name/description get their OWN dedicated, hardcoded treatment
        # (self._name/self._description slots on SedBase, set_name/
        # get_name/... accessors defined once there, special-cased inside
        # _validate_own and _load_fields) rather than flowing through the
        # generic per-field pipeline below - excluded here for that reason
        # alone. notes/annotations are every bit as much SEDBaseFields
        # members (composed into every class the same way), but need no
        # such special treatment: notes classifies as a plain "any"-kind
        # leaf field and annotations as a plain array-of-Annotation
        # collection field, both already fully handled by the SAME generic
        # per-field FieldSpec pipeline every other field goes through - so,
        # unlike name/description, they're deliberately NOT filtered out
        # here (Design.md's Validation section note on this gap: notes/
        # annotations were previously dropped from own_fields entirely,
        # rejected as "additional property not allowed" on every class).
        own_fields = [f for f in c.fields
                      if not (f.origin_class == base and f.name in ("name", "description"))]
        collection_fields = [f for f in own_fields if f.type.kind in ("dict", "array", "any-dict")]
        leaf_fields = [f for f in own_fields if f.type.kind in _ORREF_KINDS + (
            "string", "integer", "number", "boolean", "SId", "SIdRef", "any")]
        # A single nested SedBase-derived child, neither array- nor
        # dict-kind - a plain "one object" field (spec.py's _classify_type:
        # a $ref to a fixed class -> "ref-class", e.g.
        # ExplicitODESimulation.independentVariableRange; a $ref to an
        # x-generated-oneOf discriminator -> "ref-discriminator", e.g.
        # Repeat.range). See _child_accessors's own docstring.
        child_fields = [f for f in own_fields if f.type.kind in ("ref-class", "ref-discriminator")]
        ns_field_lits = {p: emit_field_specs_literal(fs) for p, fs in c.namespace_updates.items()}

        out.append(f"class {name}(SedBase):\n")
        doc = f'    """Generated from test-specsheets/{c.category}/{name}/."""\n'
        out.append(doc)
        out.append(f"    _FIELDS = {emit_field_specs_literal(leaf_fields + collection_fields + child_fields)}\n")
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
        if c.outputs_json is not None:
            # core-spec.md Section 8 - baked in as a plain dict literal so
            # RUNTIME's outputs_shape.resolve_output() can read it straight
            # off the instance at validate() time (SEDBase-0008 through
            # -0015). Only concrete tasks/ classes ever have one; every
            # other class (including abstract/mixin tasks/ classes like
            # Repeat, and every core/auxiliary/outputs/ class) leaves this
            # at SedBase's own None default.
            out.append(f"    _OUTPUTS_JSON = {c.outputs_json!r}\n")
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
        for f in child_fields:
            out.append(f"        self._{_pyname(f.name)} = None\n")
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
        for f in child_fields:
            out.append(_child_accessors(f) + "\n")

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
        for f in child_fields:
            py = _pyname(f.name)
            out.append(f"        if self._{py} is not None: kids.append(self._{py})\n")
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
        for f in child_fields:
            py = _pyname(f.name)
            out.append(f"        if self._{py} is not None: out.append((self._{py}, '/{f.name}'))\n")
        out.append("        return out\n\n")

        out.append("    def _id_collection_names(self):\n")
        out.append(f"        return {[f.name for f in id_coll_fields]!r}\n\n")

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
        for f in child_fields:
            py = _pyname(f.name)
            out.append(f"        if self._{py} is not None: d[{f.name!r}] = self._{py}.to_json_value()\n")
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
        # A non-string _type (a list/dict is unhashable; a number/bool/null
        # can never name a class) simply matches no branch - it must not
        # raise, since reading a document never throws.
        out.append("    if not isinstance(type_value, str):\n        return None\n")
        out.append("    return branches.get(type_value)\n\n\n")

        out.append(f"def parse_{disc_name}(raw: dict):\n")
        out.append(f"    \"\"\"Returns (obj, problem_or_None). obj is None only when _type is\n"
                    f"    entirely absent; an unrecognized-but-registered or bare-unrecognized\n"
                    f"    _type still returns an {uname} holder plus a violation - an\n"
                    f"    unregistered-namespace _type returns one with no violation at all.\n"
                    f"    See Design.md's Namespaces / Schema-Pass Errors sections.\"\"\"\n")
        out.append("    if not isinstance(raw, dict):\n        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)\n")
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
    out.append("    if not isinstance(raw, dict):\n        raw = {}  # a non-object is treated as an empty object (Java/C++ do the same)\n")
    out.append("    if 'name' in raw: obj.set_name(raw['name'])\n")
    out.append("    if 'description' in raw: obj.set_description(raw['description'])\n")
    out.append("    if '_type' in raw: obj._values['_type'] = raw['_type']\n")
    out.append("    for spec in obj._FIELDS:\n")
    out.append("        if spec.name not in raw or spec.kind in ('dict', 'array', 'any-dict', 'ref-class', 'ref-discriminator'):\n")
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
    out.append("        elif spec.kind in ('ref-class', 'ref-discriminator') and spec.name in raw:\n")
    out.append("            # A single nested SedBase-derived child (see emit_model_py's own\n")
    out.append("            # child_fields/_child_accessors docstring) - 'ref-class' constructs\n")
    out.append("            # a fixed target class directly; 'ref-discriminator' dispatches on\n")
    out.append("            # the raw JSON's own _type via the matching parse_* function, same\n")
    out.append("            # as a dict-kind field's own discriminated items above.\n")
    out.append("            raw_value = raw[spec.name]\n")
    out.append("            if not isinstance(raw_value, dict):\n")
    out.append("                rid = spec.rule_id or spec.origin_catchall\n")
    out.append("                obj._load_problems.append(make_problem(rid, '/' + spec.name, **{\n")
    out.append("                    'attr': spec.name, 'class': obj.__class__.__name__,\n")
    out.append("                    'id': obj._own_id_for_message(), 'value': raw_value}))\n")
    out.append("                continue\n")
    out.append("            if spec.kind == 'ref-discriminator':\n")
    out.append("                dispatch = globals()['parse_' + spec.item_discriminator]\n")
    out.append("                child, problem = dispatch(raw_value)\n")
    out.append("                if problem is not None:\n")
    out.append("                    obj._load_problems.append(problem)\n")
    out.append("            else:\n")
    out.append("                child = globals()[spec.item_class]()\n")
    out.append("                _load_fields(child, raw_value)\n")
    out.append("            if child is not None:\n")
    out.append("                setattr(obj, '_' + _pyname(spec.name), child)\n")
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


def _copy_test_fixtures_py(out_dir: str) -> None:
    """Copies templates/python/tests/test_fixtures.py -> <out>/test_fixtures.py
    verbatim (Design.md's Testing section - Task 12: the generated library
    is tested against whatever fixtures/*.sed2.json files exist for this
    spec tree, discovered at test-collection time, never a fixture list
    baked in here or in the template itself). Every `generate.py` run that
    includes the python target gets this automatically - no separate manual
    copy step required (in CI or locally) for the fixture suite to be
    runnable against a fresh regeneration."""
    src = os.path.join(_repo_root(), "templates", "python", "tests", "test_fixtures.py")
    with open(src) as f:
        content = f.read()
    with open(os.path.join(out_dir, "test_fixtures.py"), "w") as f:
        f.write(content)


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
    with open(os.path.join(pkg_dir, "outputs_shape.py"), "w") as f:
        f.write(_named(OUTPUTS_SHAPE_PY))
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
    _copy_test_fixtures_py(out_dir)

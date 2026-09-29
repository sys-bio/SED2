"""Shared runtime for the generated libsed2 package. GENERATED - do not
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
                            expected_enum=None, constraints=None) -> list:
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
        constraints=constraints)
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


def _ref_type_problem(ref_type_rule_id, location, attr, value, class_name, id_value, resolved_desc):
    return make_problem(
        ref_type_rule_id, location, attr=attr, value=value,
        **{"class": class_name, "id": id_value, "resolved-value": resolved_desc})


def _check_constant_accessor(parsed, resolved, document, sedbase_0008, sedbase_0012, *,
                              class_name, id_value, attr, location, value,
                              field_kind, ref_type_rule_id, expected_enum, constraints=None) -> list:
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
    if ref_type_rule_id is None or field_kind not in _REF_TYPE_KINDS:
        return []
    if _literal_matches_kind(final_value, field_kind, expected_enum, constraints) is False:
        return [_ref_type_problem(ref_type_rule_id, location, attr, value, class_name, id_value,
                                  _fmt_literal(final_value))]
    return []


def _check_output_shape_and_ref_type(parsed, resolved, document, *, class_name, id_value, attr, location,
                                      value, field_kind, ref_type_rule_id, expected_enum,
                                      constraints=None) -> list:
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
            constraints=constraints)

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
                 "enum", "ref_type_rule_id", "item_kind")

    def __init__(self, name, kind, required, rule_id, required_rule_id,
                 origin_catchall, minimum=None, exclusive_minimum=None,
                 pattern=None, item_class=None, item_discriminator=None,
                 is_math=False, min_length=None, enum=None, ref_type_rule_id=None,
                 item_kind=None):
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
                        constraints=(spec.minimum, spec.exclusive_minimum, spec.item_kind)))
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

#!/usr/bin/env python3
"""SED2 code generator - spec loading and composition.

Reads a specsheets-shaped tree (core/, tasks/, outputs/, auxiliary/, plus an
optional namespaces/ subtree) and builds an in-memory SpecModel: one
FlatClass per concrete, instantiable class, with every attribute it should
expose (its own + everything pulled in via allOf mixin composition, plus any
registered namespace's updated/ additions) flattened into one ordered field
list. Each field carries the numbered validation rule ID it maps to, and the
name of the Data Sheet folder that originally declared it (for the
class-catch-all fallback - see Design.md's Schema-Pass Errors section).

This module contains NO target-language code generation; see emit_python.py,
emit_java.py, emit_cpp.py for that. See Design.md's Classes/Namespaces
sections and core-spec.md Section 8 for the algorithm this implements.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Optional

CATEGORIES = ["core", "tasks", "outputs", "auxiliary"]
NS_ID_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*@[A-Za-z_][A-Za-z0-9_]*$")


def read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_rule_md(path: str) -> "RuleDoc":
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError(f"{path}: expected YAML frontmatter")
    front, body = m.group(1), m.group(2).strip()
    meta = {}
    for line in front.splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        meta[k.strip()] = v
    return RuleDoc(
        id=meta["id"],
        rule=meta.get("rule", ""),
        message=meta.get("message", ""),
        severity=meta.get("severity", "error"),
        status=meta.get("status", "active"),
        check=meta.get("check", "schema"),
        body=body,
    )


@dataclass
class RuleDoc:
    id: str
    rule: str
    message: str
    severity: str
    status: str
    check: str
    body: str


@dataclass
class FieldType:
    """Describes the shape of one field's value for codegen + light validation."""
    kind: str  # "string" | "number" | "integer" | "boolean" | "StringOrRef" |
    # "NumberOrRef" | "SIdRef" | "SId" | "dict" | "array"
    # For "dict": keyed by SId, values are branches of a discriminator.
    item_discriminator: Optional[str] = None
    # For "array": each item is either a plain class (no _type) or a
    # discriminator's branches.
    item_class: Optional[str] = None
    item_discriminator2: Optional[str] = None
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = None
    pattern: Optional[str] = None
    min_length: Optional[int] = None  # core/Types' URI leaf: "minLength": 1
    # A fixed set of legal string values (core/Types leaf defs like
    # CurveType/ScaleType/SurfaceType/DistributionURI - "type": "string",
    # "enum": [...]) - only ever set for kind == "string" or one of the
    # *OrRef kinds whose value-side is itself one of those enum-constrained
    # leaves (see _orref_value_kind's one-level-of-$ref resolution).
    enum: Optional[tuple] = None
    # For "ArrayOrRef" (element type) / "DictOrRef" (value type): one of
    # "string" | "number" | "ref" | "any". Drives the ref-type check that a
    # constant a reference resolves to actually has elements/values of the
    # declared kind. Only set for those two kinds.
    item_kind: Optional[str] = None


@dataclass
class Field:
    name: str
    type: FieldType
    required: bool
    rule_id: Optional[str]          # x-rule-id, if this exact constraint is numbered
    required_rule_id: Optional[str]  # x-required-rule-ids[name], if required
    origin_class: str               # Data Sheet folder that declared this field
    from_namespace: Optional[str] = None  # set for a namespace's updated/ addition
    is_math: bool = False            # x-math, if this field carries a SED2 infix math
    # string (Design.md's Math section / Types-0001..0004 - see Types-0001.md's own
    # note: "the schema type every math-bearing attribute uses" is StringOrRef, but
    # not every StringOrRef field is math-bearing, so this needs its own marker
    # rather than being inferred from the field's declared type)
    ref_target: Optional[str] = None
    # x-ref-target, if this SIdRef field must resolve to something specific:
    # "model" (SEDBase-0016) or "annotatedData" (SEDBase-0017). Generator-only
    # metadata, inert to JSON Schema validators, like x-rule-id and x-math.
    ref_type_rule_id: Optional[str] = None
    # core-spec.md Section 8's "x-rule-id is a single rule-ID string, or an
    # array of them when more than one rule governs the same property (most
    # commonly an OrRef field's separate direct-value and reference-form
    # rules)" - the second element (Design.md's Validation section: "the
    # formulaic 'if a reference, must resolve to type X' rules" - see
    # _check_ref_type in emit_python.py's RUNTIME), split out here so
    # `rule_id` itself stays a single string throughout - see _flatten_object
    # below for where the split actually happens.


@dataclass
class Branch:
    type_const: str
    class_name: str
    rule_id: Optional[str]          # x-rule-id on this branch's own _type const
    namespace: Optional[str] = None  # set for a namespace new/ branch


@dataclass
class Discriminator:
    name: str                       # e.g. "AbstractWidget"
    branches: dict = field(default_factory=dict)  # type_const -> Branch
    missing_type_rule_id: Optional[str] = None
    unknown_class_name: str = ""    # e.g. "UnknownWidget"


@dataclass
class FlatClass:
    name: str
    category: str
    has_type: bool
    type_const: Optional[str]
    type_rule_id: Optional[str]
    discriminator: Optional[str]    # discriminator this is a branch of, if any
    fields: list = field(default_factory=list)  # list[Field]
    namespace_updates: dict = field(default_factory=dict)  # prefix -> list[Field]
    namespace_catchalls: dict = field(default_factory=dict)  # prefix -> "<Class>-<ns>-0000"
    is_document: bool = False
    namespace: Optional[str] = None  # set when this whole class is a namespace new/ branch
    # core-spec.md Section 8's per-class outputs.json envelope (the raw
    # {"outputs": {"[id]": {...}, "[id].model": {...}, ...}} dict), when this
    # class's own Data Sheet folder has one - every concrete tasks/ class
    # does; abstract/mixin classes and every non-tasks/ category class don't
    # (see Design.md's Validation section, SEDBase-0008 through -0015).
    outputs_json: Optional[dict] = None

    @property
    def own_catchall(self) -> str:
        if self.namespace:
            return f"{self.namespace}-{self.name}-0000"
        return f"{self.name}-0000"


@dataclass
class SpecModel:
    classes: dict = field(default_factory=dict)          # name -> FlatClass
    discriminators: dict = field(default_factory=dict)    # name -> Discriminator
    rules: dict = field(default_factory=dict)             # id -> RuleDoc
    registered_namespaces: list = field(default_factory=list)  # ["acme", ...]
    document_class: Optional[str] = None
    base_mixin: Optional[str] = None   # e.g. "TestBase" / "SEDBase"
    spec_root: str = ""
    # The document class's own resolved version directory name (e.g.
    # "v1.0.0") - the newest version this generate run's specsheets/ tree
    # actually has for it. SEDDocument-0009 through -0011 (Design.md's
    # Namespaces/Versioning sections) compare an instance's own declared
    # `version` against this to warn when a document claims to be newer
    # than anything this library was generated to understand.
    document_version: Optional[str] = None

    def generatable_classes(self) -> list:
        """Names of classes that should get a standalone generated type:
        the document root, every discriminated concrete/branch class, and
        any plain embedded helper (like Note) referenced as an item type
        somewhere. Excludes shared base mixins (TestBase/SEDBase, folded
        into every class's own field list) and schema-only mixins that are
        never referenced except via allOf (like WidgetOptions)."""
        referenced = set()
        for c in self.classes.values():
            for f in c.fields:
                if f.type.item_class:
                    referenced.add(f.type.item_class)
        names = []
        for name, c in self.classes.items():
            if name == self.base_mixin:
                continue
            if c.is_document or c.has_type or name in referenced:
                names.append(name)
        return names


class _Loader:
    """Loads raw schema.json/common.schema.json/inline.schema.json/validation
    files from a specsheets-shaped tree, and composes them into a SpecModel."""

    def __init__(self, spec_root: str):
        self.spec_root = os.path.abspath(spec_root)
        self.rules: dict[str, RuleDoc] = {}
        self.schema_cache: dict[str, dict] = {}
        # class_name -> {"dir": path, "category": str, "schema": dict|None,
        #                "common": dict|None, "inline": dict|None}
        self.class_dirs: dict[str, dict] = {}
        self.registered_namespaces: list[str] = []
        # namespace -> {"new": [(category, class_name, dir)], "updated": [(category, class_name, dir)]}
        self.namespace_dirs: dict[str, dict] = {}

    # ---- filesystem discovery -------------------------------------------------
    def discover(self):
        for category in CATEGORIES:
            cat_dir = os.path.join(self.spec_root, category)
            if not os.path.isdir(cat_dir):
                continue
            for class_name in sorted(os.listdir(cat_dir)):
                class_dir = os.path.join(cat_dir, class_name)
                if not os.path.isdir(class_dir):
                    continue
                version_dir = self._latest_version_dir(class_dir)
                if version_dir is None:
                    continue
                self._load_class_dir(category, class_name, version_dir)

        ns_root = os.path.join(self.spec_root, "namespaces")
        if os.path.isdir(ns_root):
            for prefix in sorted(os.listdir(ns_root)):
                prefix_dir = os.path.join(ns_root, prefix)
                if not os.path.isdir(prefix_dir):
                    continue
                self.registered_namespaces.append(prefix)
                self.namespace_dirs[prefix] = {"new": [], "updated": []}
                for kind in ("new", "updated"):
                    kind_dir = os.path.join(prefix_dir, kind)
                    if not os.path.isdir(kind_dir):
                        continue
                    for category in CATEGORIES:
                        cat_dir = os.path.join(kind_dir, category)
                        if not os.path.isdir(cat_dir):
                            continue
                        for class_name in sorted(os.listdir(cat_dir)):
                            class_dir = os.path.join(cat_dir, class_name)
                            if not os.path.isdir(class_dir):
                                continue
                            version_dir = self._latest_version_dir(class_dir)
                            if version_dir is None:
                                continue
                            self.namespace_dirs[prefix][kind].append(
                                (category, class_name, version_dir)
                            )
                            self._load_rules(version_dir)

    def _latest_version_dir(self, class_dir: str) -> Optional[str]:
        versions = []
        for name in os.listdir(class_dir):
            m = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", name)
            if m and os.path.isdir(os.path.join(class_dir, name)):
                versions.append((tuple(int(g) for g in m.groups()), name))
        if not versions:
            return None
        versions.sort()
        return os.path.join(class_dir, versions[-1][1])

    def _load_class_dir(self, category: str, class_name: str, version_dir: str):
        entry = {"dir": version_dir, "category": category, "schema": None,
                 "common": None, "inline": None, "outputs": None}
        schema_path = os.path.join(version_dir, "schema.json")
        if os.path.isfile(schema_path):
            entry["schema"] = read_json(schema_path)
            entry["schema_path"] = schema_path
        common_path = os.path.join(version_dir, "common.schema.json")
        if os.path.isfile(common_path):
            entry["common"] = read_json(common_path)
            entry["common_path"] = common_path
        inline_path = os.path.join(version_dir, "inline.schema.json")
        if os.path.isfile(inline_path):
            entry["inline"] = read_json(inline_path)
            entry["inline_path"] = inline_path
        # core-spec.md Section 8's "Task output shapes (outputs.json)" - every
        # concrete tasks/ class (one with its own _type) carries one of
        # these, machine-describing what each output suffix ([id], [id].model,
        # [id].strings, [id].aggregates, ...) resolves to. Abstract/mixin
        # classes (AbstractSimulation, Repeat, ...) carry none - nothing is
        # ever instantiated as one directly, so there's no "outputs.json" to
        # even find here, matching FlatClass.outputs_json's own None default.
        outputs_path = os.path.join(version_dir, "outputs.json")
        if os.path.isfile(outputs_path):
            entry["outputs"] = read_json(outputs_path)
            entry["outputs_path"] = outputs_path
        self.class_dirs[class_name] = entry
        self._load_rules(version_dir)

    def _load_rules(self, version_dir: str):
        rules_dir = os.path.join(version_dir, "validation")
        if not os.path.isdir(rules_dir):
            return
        for fname in sorted(os.listdir(rules_dir)):
            if not fname.endswith(".md"):
                continue
            rule = parse_rule_md(os.path.join(rules_dir, fname))
            self.rules[rule.id] = rule


def _resolve_ref_file(ref: str, from_file: str, spec_root: str) -> tuple[str, str]:
    """Given a $ref like '../../../core/Types/v1.0.0/schema.json#/$defs/SId'
    resolve it (relative to from_file's directory) to (abs_path, fragment)."""
    if "#" in ref:
        path_part, frag = ref.split("#", 1)
    else:
        path_part, frag = ref, ""
    if path_part == "":
        abs_path = from_file
    else:
        abs_path = os.path.normpath(os.path.join(os.path.dirname(from_file), path_part))
    return abs_path, frag


def _defs_lookup(doc: dict, frag: str) -> dict:
    """Resolve a '#/$defs/Name' style fragment against a loaded schema doc."""
    if not frag:
        return doc
    parts = [p for p in frag.split("/") if p]
    node = doc
    for p in parts:
        node = node[p]
    return node


class _Composer:
    def __init__(self, loader: _Loader):
        self.loader = loader
        self.spec_root = loader.spec_root
        self._doc_cache: dict[str, dict] = {}
        self.discriminators: dict[str, Discriminator] = {}
        self.classes: dict[str, FlatClass] = {}

    def _load_doc(self, path: str) -> dict:
        path = os.path.normpath(path)
        if path not in self._doc_cache:
            self._doc_cache[path] = read_json(path)
        return self._doc_cache[path]

    # ---- discriminator discovery ----------------------------------------
    def find_discriminators(self):
        """Scan every schema/common/inline file for an x-generated-oneOf marker."""
        for name, entry in self.loader.class_dirs.items():
            for key in ("schema", "inline"):
                doc = entry.get(key)
                path = entry.get(f"{key}_path")
                if not doc:
                    continue
                defs = doc.get("$defs", {})
                for def_name, def_body in defs.items():
                    if "x-generated-oneOf" in def_body:
                        common_ref = def_body["x-generated-oneOf"]
                        common_path, common_frag = _resolve_ref_file(common_ref, path, self.spec_root)
                        disc = Discriminator(
                            name=def_name,
                            missing_type_rule_id=def_body.get("x-missing-type-rule-id"),
                            unknown_class_name=f"Unknown{def_name}",
                        )
                        disc.common_path = common_path  # type: ignore[attr-defined]
                        disc.common_frag = common_frag  # type: ignore[attr-defined]
                        self.discriminators[def_name] = disc

    def _transitive_allof_refs(self, def_body: dict, doc_path: str, _seen=None) -> set:
        """Every (resolved_path, frag) this $defs entry's own allOf list
        references, directly or transitively through intermediate mixins'
        own allOf chains - so a class several allOf-mixin levels removed
        from a discriminator's Common schema (Loop -> Repeat ->
        AbstractTaskCommon; BoundedODESimulation -> AbstractODESimulation ->
        AbstractSimulation -> AbstractTaskCommon) is still found as
        composing it, not just a class that allOf's the Common schema
        directly (Calculation, DrawFromDistribution, ...)."""
        if _seen is None:
            _seen = set()
        result = set()
        for ref_obj in def_body.get("allOf", []):
            ref = ref_obj.get("$ref")
            if not ref:
                continue
            rpath, rfrag = _resolve_ref_file(ref, doc_path, self.spec_root)
            key = (os.path.normpath(rpath), rfrag)
            if key in _seen:
                continue
            _seen.add(key)
            result.add(key)
            mixin_doc = self._load_doc(rpath)
            mixin_body = _defs_lookup(mixin_doc, rfrag)
            result |= self._transitive_allof_refs(mixin_body, rpath, _seen)
        return result

    def _composes(self, class_schema_doc: dict, class_schema_path: str,
                   target_path: str, target_frag: str) -> bool:
        """Does this class's top-level $defs entry allOf the given target
        Common schema (identified by resolved file path + fragment),
        directly or transitively through intermediate mixins?"""
        top = self._top_defs_entry(class_schema_doc)
        target_key = (os.path.normpath(target_path), target_frag)
        return target_key in self._transitive_allof_refs(top, class_schema_path)

    def _top_defs_entry(self, doc: dict) -> dict:
        top_ref = doc.get("$ref", "")
        frag = top_ref.split("#", 1)[1] if "#" in top_ref else ""
        return _defs_lookup(doc, frag)

    def find_branches(self):
        """For every discriminator, scan built-in classes + registered
        namespace new/ classes for a direct allOf match on its Common schema."""
        for disc in self.discriminators.values():
            for name, entry in self.loader.class_dirs.items():
                doc = entry.get("schema")
                path = entry.get("schema_path")
                if not doc:
                    continue
                top = self._top_defs_entry(doc)
                if "x-generated-oneOf" in top:
                    continue  # this file IS a discriminator, not a branch
                if self._composes(doc, path, disc.common_path, disc.common_frag):
                    type_const = top.get("properties", {}).get("_type", {}).get("const")
                    if type_const is None:
                        continue
                    rule_id = top.get("properties", {}).get("_type", {}).get("x-rule-id")
                    disc.branches[type_const] = Branch(type_const, name, rule_id)

            for prefix, kinds in self.loader.namespace_dirs.items():
                for category, class_name, version_dir in kinds["new"]:
                    schema_path = os.path.join(version_dir, "schema.json")
                    if not os.path.isfile(schema_path):
                        continue
                    doc = self._load_doc(schema_path)
                    top = self._top_defs_entry(doc)
                    if self._composes(doc, schema_path, disc.common_path, disc.common_frag):
                        type_const = top.get("properties", {}).get("_type", {}).get("const")
                        rule_id = top.get("properties", {}).get("_type", {}).get("x-rule-id")
                        disc.branches[type_const] = Branch(type_const, class_name, rule_id, namespace=prefix)

    # ---- field flattening --------------------------------------------------
    def _is_sidref_alt(self, alt: dict, from_file: str) -> bool:
        """True if this anyOf branch IS the reference side of an OrRef shape
        (a bare $ref to SIdRef, directly or one level of $ref indirection)."""
        aref = alt.get("$ref")
        if not aref:
            return False
        _rpath, rfrag = _resolve_ref_file(aref, from_file, self.spec_root)
        return rfrag.rsplit("/", 1)[-1] == "SIdRef"

    def _orref_value_kind(self, alt: dict, from_file: str) -> tuple:
        """Maps the non-reference side of an OrRef anyOf to one of the OrRef
        FieldType kinds emit_python.py knows how to generate accessors for,
        returning (kind, resolved_schema) - resolved_schema is `alt` itself
        for an inline shape, or the one-level-deep $ref target for a value
        side like Curve.curveType's CurveType (a core/Types leaf def: plain
        "type": "string", "enum": [...] - the enum-typed *OrRef family isn't
        a further OrRef itself, just one indirection away from an inline
        {"type": "string", ...} shape, so one level of $ref-following is
        enough; this doesn't recurse). Best-effort: a value shape this
        doesn't recognize (an exotic combinator, a $ref to something that
        still isn't a plain typed leaf) returns (None, alt)."""
        if "type" not in alt and "$ref" in alt:
            rpath, rfrag = _resolve_ref_file(alt["$ref"], from_file, self.spec_root)
            target_doc = self._load_doc(rpath)
            resolved = _defs_lookup(target_doc, rfrag)
        else:
            resolved = alt
        t = resolved.get("type")
        kind = {
            "string": "StringOrRef", "number": "NumberOrRef", "integer": "IntegerOrRef",
            "boolean": "BooleanOrRef", "array": "ArrayOrRef", "object": "DictOrRef",
        }.get(t)
        return kind, resolved

    def _container_item_kind(self, kind: str, resolved: dict, from_file: str) -> Optional[str]:
        """Element kind of an ArrayOrRef's "items" / value kind of a
        DictOrRef's "additionalProperties": "string" (StringOrRef or a plain
        string), "number" (NumberOrRef or a plain number/integer), "ref"
        (SIdRef), otherwise "any" (AnyValueOrRef, absent, or unrecognized)."""
        if kind not in ("ArrayOrRef", "DictOrRef"):
            return None
        sub = resolved.get("items" if kind == "ArrayOrRef" else "additionalProperties")
        if not isinstance(sub, dict):
            return "any"
        if "$ref" in sub:
            name = sub["$ref"].rsplit("/", 1)[-1]
            return {"StringOrRef": "string", "NumberOrRef": "number", "SIdRef": "ref",
                    "IntegerOrRef": "number", "AnyValueOrRef": "any"}.get(name, "any")
        return {"string": "string", "number": "number", "integer": "number"}.get(sub.get("type"), "any")

    def _orref_shape(self, alts: list, from_file: str) -> Optional[FieldType]:
        """Recognizes Design.md's Classes-section OrRef pattern generically:
        anyOf of [some literal/restricted-value shape, a reference to
        SIdRef] - in EITHER order - covering not just the two named
        core/Types defs (StringOrRef, NumberOrRef) but the whole family
        (IntegerOrRef, PositiveIntegerOrRef, BooleanOrRef, URIOrRef, ...),
        inline ad-hoc ones the real spec also uses (AbstractCurve.order/
        .yAxis, Repeat.outputVariableMap), AND the enum-constrained leaves
        one $ref away (Curve.curveType -> CurveType, Axis.scale's own
        ScaleTypeOrRef -> ScaleType, Surface.surfaceType -> SurfaceType,
        DrawFromDistribution's *OrRef -> DistributionURI) - see
        _orref_value_kind's one-level-of-$ref resolution. Numeric bounds/
        pattern/enum on the (possibly resolved) value side are carried
        through; anything this still doesn't recognize is accepted
        structurally (right JSON type) but its own finer constraint isn't
        re-derived here."""
        if len(alts) != 2:
            return None
        for i in (0, 1):
            value_alt, ref_alt = alts[i], alts[1 - i]
            if not self._is_sidref_alt(ref_alt, from_file):
                continue
            kind, resolved = self._orref_value_kind(value_alt, from_file)
            if kind is None:
                continue
            enum = resolved.get("enum")
            return FieldType(
                kind=kind,
                minimum=resolved.get("minimum"),
                exclusive_minimum=resolved.get("exclusiveMinimum"),
                pattern=resolved.get("pattern") if kind == "StringOrRef" else None,
                min_length=resolved.get("minLength") if kind == "StringOrRef" else None,
                enum=tuple(enum) if enum else None,
                item_kind=self._container_item_kind(kind, resolved, from_file),
            )
        return None

    def _resolve_inline_alias(self, target_top: dict, rpath: str) -> Optional[str]:
        """An 'XInline' wrapper schema (Design.md's Classes section - e.g.
        auxiliary/Span/v1.0.0/inline.schema.json's SpanInline) is a bare oneOf of
        exactly one $ref to the real class: not a discriminator (that's the
        separate x-generated-oneOf marker, e.g. RangeInline), just a way to
        embed a single concrete class as a named child field without an
        array or a dict wrapper. Unwrap it transparently to the referenced
        class's own name (recursing in case of a chained alias) rather than
        treating "SpanInline" itself as a class - it has no class_dirs entry
        and was never meant to be dispatched to one."""
        one = target_top.get("oneOf")
        if not one or len(one) != 1:
            return None
        ref = one[0].get("$ref")
        if not ref:
            return None
        rpath2, rfrag2 = _resolve_ref_file(ref, rpath, self.spec_root)
        leaf = rfrag2.rsplit("/", 1)[-1]
        nested_doc = self._load_doc(rpath2)
        nested_top = _defs_lookup(nested_doc, rfrag2)
        nested_alias = self._resolve_inline_alias(nested_top, rpath2)
        return nested_alias if nested_alias is not None else leaf

    def _classify_type(self, prop_schema: dict, from_file: str) -> FieldType:
        if "anyOf" in prop_schema and "$ref" not in prop_schema:
            ft = self._orref_shape(prop_schema["anyOf"], from_file)
            if ft is not None:
                return ft
        ref = prop_schema.get("$ref")
        if ref:
            rpath, rfrag = _resolve_ref_file(ref, from_file, self.spec_root)
            leaf = rfrag.rsplit("/", 1)[-1]
            if leaf in ("StringOrRef", "NumberOrRef", "SIdRef", "SId"):
                return FieldType(kind=leaf)
            # $ref to a Note-like plain embedded class or a discriminator/inline
            target_doc = self._load_doc(rpath)
            target_top = _defs_lookup(target_doc, rfrag)
            if "x-generated-oneOf" in target_top:
                return FieldType(kind="ref-discriminator", item_discriminator=leaf)
            alias = self._resolve_inline_alias(target_top, rpath)
            if alias is not None:
                return FieldType(kind="ref-class", item_class=alias)
            if "anyOf" in target_top:
                ft = self._orref_shape(target_top["anyOf"], rpath)
                if ft is not None:
                    return ft
            if "core/Types/" in rpath.replace(os.sep, "/"):
                return FieldType(kind="any")
            return FieldType(kind="ref-class", item_class=leaf)
        t = prop_schema.get("type")
        if t == "array":
            items = prop_schema.get("items", {})
            item_ref = items.get("$ref")
            if item_ref:
                rpath, rfrag = _resolve_ref_file(item_ref, from_file, self.spec_root)
                target_doc = self._load_doc(rpath)
                target_top = _defs_lookup(target_doc, rfrag)
                leaf = rfrag.rsplit("/", 1)[-1]
                if "x-generated-oneOf" in target_top:
                    return FieldType(kind="array", item_discriminator2=leaf)
                alias = self._resolve_inline_alias(target_top, rpath)
                return FieldType(kind="array", item_class=alias if alias is not None else leaf)
            return FieldType(kind="array")
        if t == "object" and "additionalProperties" in prop_schema:
            add = prop_schema["additionalProperties"]
            add_ref = add.get("$ref")
            if add_ref:
                rpath, rfrag = _resolve_ref_file(add_ref, from_file, self.spec_root)
                leaf = rfrag.rsplit("/", 1)[-1]
                # Mirror the array-items case just above: only an actual
                # x-generated-oneOf holder (AbstractTask, AbstractOutput, ...)
                # is a discriminator. Anything else is either a plain
                # embedded class (a dict of id -> single fixed type, like
                # Loop.loopVariables -> LoopVariable) or a shared core/Types
                # helper definition that was never meant to be a class at
                # all (Design.md's Classes section: core/Types "should be
                # treated as a source of shared type definitions ... not as
                # a class to generate get-/set-/isSet-/unset- accessors
                # for") - e.g. SEDDocument.constants -> AnyValueOrRef, which
                # is "any JSON value", stored and round-tripped as a plain
                # value rather than dispatched to a generated class.
                target_doc = self._load_doc(rpath)
                target_top = _defs_lookup(target_doc, rfrag)
                if "x-generated-oneOf" in target_top:
                    return FieldType(kind="dict", item_discriminator=leaf)
                if leaf in ("StringOrRef", "NumberOrRef", "SIdRef", "SId"):
                    return FieldType(kind=leaf)
                if "core/Types/" in rpath.replace(os.sep, "/"):
                    # A dict whose values are a bare core/Types leaf (today,
                    # only SEDDocument.constants -> AnyValueOrRef) is still a
                    # dict - each entry just isn't dispatched to a generated
                    # class. "any-dict" (not "any") keeps that dict-ness so
                    # the generator still emits get/add/insert/remove/setId
                    # collection accessors, just storing each raw JSON value
                    # as-is instead of a SedBase instance (see emit_python.py's
                    # _collection_accessors/_load_fields any-dict branches).
                    return FieldType(kind="any-dict")
                alias = self._resolve_inline_alias(target_top, rpath)
                return FieldType(kind="dict", item_class=alias if alias is not None else leaf)
            return FieldType(kind="dict")
        if t == "integer":
            ft = FieldType(kind="integer")
        elif t == "number":
            ft = FieldType(kind="number")
        elif t == "boolean":
            ft = FieldType(kind="boolean")
        else:
            ft = FieldType(kind="string")
        if "minimum" in prop_schema:
            ft.minimum = prop_schema["minimum"]
        if "exclusiveMinimum" in prop_schema:
            ft.exclusive_minimum = prop_schema["exclusiveMinimum"]
        if "pattern" in prop_schema:
            ft.pattern = prop_schema["pattern"]
        if "minLength" in prop_schema:
            ft.min_length = prop_schema["minLength"]
        if "enum" in prop_schema:
            ft.enum = tuple(prop_schema["enum"])
        return ft

    def _flatten_object(self, doc: dict, doc_path: str, origin_class: str) -> list[Field]:
        """Flatten one object-schema $defs entry's OWN properties (not
        recursing into allOf - the caller walks allOf separately so each
        composed piece keeps its own origin_class)."""
        top = self._top_defs_entry(doc)
        required = set(top.get("required", []))
        required_rule_ids = top.get("x-required-rule-ids", {})
        fields = []
        for pname, pschema in top.get("properties", {}).items():
            if pname == "_type":
                continue
            ftype = self._classify_type(pschema, doc_path)
            # core-spec.md Section 8: "x-rule-id is a single rule-ID string,
            # or an array of them when more than one rule governs the same
            # property (most commonly an OrRef field's separate direct-value
            # and reference-form rules)". Split here so every OTHER reader
            # of Field.rule_id (schema-pass error mapping, required-field
            # messages, ...) only ever sees a single rule id, never a raw
            # (unhashable, un-formattable) list.
            raw_rule_id = pschema.get("x-rule-id")
            if isinstance(raw_rule_id, list):
                rule_id = raw_rule_id[0] if raw_rule_id else None
                ref_type_rule_id = raw_rule_id[1] if len(raw_rule_id) > 1 else None
            else:
                rule_id = raw_rule_id
                ref_type_rule_id = None
            fields.append(Field(
                name=pname,
                type=ftype,
                required=pname in required,
                rule_id=rule_id,
                required_rule_id=required_rule_ids.get(pname),
                origin_class=origin_class,
                is_math=bool(pschema.get("x-math", False)),
                ref_target=pschema.get("x-ref-target"),
                ref_type_rule_id=ref_type_rule_id,
            ))
        return fields

    def _flatten_allof_chain(self, doc: dict, doc_path: str, origin_class: str) -> list[Field]:
        """Flatten this class's own properties plus every allOf-composed
        mixin's properties, transitively, each keeping ITS OWN origin_class."""
        fields = self._flatten_object(doc, doc_path, origin_class)
        top = self._top_defs_entry(doc)
        for ref_obj in top.get("allOf", []):
            ref = ref_obj.get("$ref")
            if not ref:
                continue
            rpath, rfrag = _resolve_ref_file(ref, doc_path, self.spec_root)
            target_doc = self._load_doc(rpath)
            mixin_origin = self._class_name_for_file(rpath)
            # Build a throwaway doc whose $ref points straight at the mixin's
            # $defs entry, so _flatten_object/_top_defs_entry see it directly.
            wrapper = {"$ref": "#" + rfrag}
            wrapper_doc = {**target_doc, "$ref": "#" + rfrag}
            fields.extend(self._flatten_allof_chain(wrapper_doc, rpath, mixin_origin))
        return fields

    def _class_name_for_file(self, path: str) -> str:
        """core/TestBase/v1.0.0/schema.json -> 'TestBase'; also handles
        common.schema.json / inline.schema.json living in the same folder."""
        version_dir = os.path.dirname(path)
        class_dir = os.path.dirname(version_dir)
        return os.path.basename(class_dir)

    def build_classes(self):
        # index: for each discriminator, which class_name is a branch of it
        branch_of: dict[str, str] = {}
        for disc in self.discriminators.values():
            for branch in disc.branches.values():
                if branch.namespace is None:
                    branch_of[branch.class_name] = disc.name

        for name, entry in self.loader.class_dirs.items():
            doc = entry.get("schema")
            path = entry.get("schema_path")
            if not doc:
                continue
            top = self._top_defs_entry(doc)
            if "x-generated-oneOf" in top:
                continue  # discriminator holder, not an instantiable class
            type_const = top.get("properties", {}).get("_type", {}).get("const")
            has_type = type_const is not None
            type_rule_id = top.get("properties", {}).get("_type", {}).get("x-rule-id") if has_type else None
            fc = FlatClass(
                name=name,
                category=entry["category"],
                has_type=has_type,
                type_const=type_const,
                type_rule_id=type_rule_id,
                discriminator=branch_of.get(name),
                is_document=(name == self.document_class_guess()),
                outputs_json=entry.get("outputs"),
            )
            fc.fields = self._flatten_allof_chain(doc, path, name)
            self.classes[name] = fc

        # namespace new/ classes (not already covered by class_dirs, since
        # they live under namespaces/<prefix>/new/...)
        for prefix, kinds in self.loader.namespace_dirs.items():
            for category, class_name, version_dir in kinds["new"]:
                schema_path = os.path.join(version_dir, "schema.json")
                if not os.path.isfile(schema_path):
                    continue
                doc = self._load_doc(schema_path)
                top = self._top_defs_entry(doc)
                type_const = top.get("properties", {}).get("_type", {}).get("const")
                type_rule_id = top.get("properties", {}).get("_type", {}).get("x-rule-id")
                disc_name = None
                for d in self.discriminators.values():
                    if type_const in d.branches and d.branches[type_const].namespace == prefix:
                        disc_name = d.name
                outputs_path = os.path.join(version_dir, "outputs.json")
                fc = FlatClass(
                    name=class_name,
                    category=category,
                    has_type=True,
                    type_const=type_const,
                    type_rule_id=type_rule_id,
                    discriminator=disc_name,
                    namespace=prefix,
                    outputs_json=read_json(outputs_path) if os.path.isfile(outputs_path) else None,
                )
                fc.fields = self._flatten_allof_chain(doc, schema_path, class_name)
                self.classes[class_name] = fc

            # updated/ fragments: add fields to an existing class
            for category, class_name, version_dir in kinds["updated"]:
                schema_path = os.path.join(version_dir, "schema.json")
                if not os.path.isfile(schema_path) or class_name not in self.classes:
                    continue
                doc = self._load_doc(schema_path)
                origin = f"{class_name}-{prefix}"
                new_fields = self._flatten_object(doc, schema_path, origin)
                for f in new_fields:
                    f.from_namespace = prefix
                self.classes[class_name].namespace_updates[prefix] = new_fields
                self.classes[class_name].namespace_catchalls[prefix] = f"{origin}-0000"

    def document_class_guess(self) -> Optional[str]:
        # Heuristic: exactly one class per tree has no discriminator, is in
        # "core", and isn't a shared-types-only folder. Overridden by caller
        # if a spec provides an explicit hint.
        for name, entry in self.loader.class_dirs.items():
            if entry["category"] != "core":
                continue
            doc = entry.get("schema")
            if not doc:
                continue
            top = self._top_defs_entry(doc)
            if "properties" in top and any(
                self._classify_type(p, entry["schema_path"]).kind in ("dict",)
                for p in top["properties"].values()
            ):
                return name
        return None


def load_spec(spec_root: str, document_class_hint: Optional[str] = None) -> SpecModel:
    loader = _Loader(spec_root)
    loader.discover()
    composer = _Composer(loader)
    composer.find_discriminators()
    composer.find_branches()
    composer.build_classes()
    doc_class = document_class_hint or composer.document_class_guess()
    doc_entry = loader.class_dirs.get(doc_class)
    doc_version = os.path.basename(doc_entry["dir"]) if doc_entry else None
    model = SpecModel(
        classes=composer.classes,
        discriminators=composer.discriminators,
        rules=loader.rules,
        registered_namespaces=loader.registered_namespaces,
        document_class=doc_class,
        spec_root=loader.spec_root,
        document_version=doc_version,
    )
    return model

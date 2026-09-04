#!/usr/bin/env python3
"""Generates sed2 C++ classes from the attribute tables under
codegen/spec_attributes/.

Each table describes one SED2 class: its attributes, and for each
attribute whether it is required, a list of scalars, an owned sub-object,
an ordered list of polymorphic sub-objects, or a raw-value dictionary.
This produces the get-/set-/isSet-/unset- pattern (and, for list
attributes, the add-/remove-/insert- pattern) described in Design.md,
"Classes" - by hand for one class this is routine but repetitive; across
~30 spec classes it is exactly the kind of thing that should be generated
from data instead of typed out, so that adding a class later means adding
a table, not writing C++.

Table shape:
    {
      "className": "ExplicitODESimulation",
      "typeName": "explicitODESimulation",
      "parent": "SEDBase",
      "generateBaseOnly": false,   // optional; see below
      "registerType": true,        // optional; see below
      "attributes": [
        {"name": "kisaoID", "kind": "scalar", "cppType": "std::string", "required": true},
        {"name": "independentVariableRange", "kind": "owned", "required": false},
        {"name": "outputVariables", "kind": "scalarList", "cppType": "std::string"},
        {"name": "tasks", "kind": "polymorphicList"},
        {"name": "constants", "kind": "map"}
      ]
    }

Attribute "kind" values:
    scalar           - a single value (cppType: std::string | double | bool | int64_t)
    owned            - a single owned, polymorphic ("_type"-tagged) sub-object
    scalarList       - an ordered list of scalar values
    polymorphicList  - an ordered, id-keyed list of owned, polymorphic sub-objects
    map              - an ordered string-to-JSON-value dictionary (e.g. 'constants')

"generateBaseOnly" (default false): when true, the class is generated into
the sed2::generated namespace instead of sed2, and is expected to be
wrapped by a hand-written subclass (see include/sed2/core/SEDDocument.h)
that adds behavior a table can't express - SEDDocument's file/JSON-string
loading and cross-reference resolution, for instance.

"registerType" (default true): when false, the class does not
self-register with TypeRegistry. Used for SEDDocument, which is always the
top-level object being parsed, never an embedded "_type"-tagged child of
something else.

"dotAccessors" (default []): the class's own SEDBase::getDeclaredDotAccessors()
override, for classes the UML spec shows declaring dot-accessor subvalues
(e.g. ModelImport's "model", for references like "#tasks:task1.model").
Omitted when empty, so the class falls back to SEDBase's own "none"
default rather than emitting a no-op override.

"bareReferenceValid" (default true): the class's own
SEDBase::isBareReferenceValid() override. Set to false for classes whose
spec-declared output is only ever one of their dot accessors, never the
bare reference itself (e.g. "#tasks:task1" means nothing for a
ModelImport - only "#tasks:task1.model" does). Omitted when true, so the
class falls back to SEDBase's own "yes" default.
"""
import argparse
import json
import os


SCALAR_DEFAULTS = {
    "double": "0.0",
    "bool": "false",
    "int64_t": "0",
}

# cppType values backed by AttributeTypes.h's ValueOrRef<T> aliases (see
# the "isRef" handling in Attribute.validate()) rather than a plain
# scalar - nlohmann (de)serializes these via the sed2::to_json/from_json
# overloads in AttributeTypes.h, so no other codegen branch needs to know
# about them beyond validate()'s reference check.
VALUE_OR_REF_TYPES = {"sed2::NumberOrRef", "sed2::IntegerOrRef", "sed2::BooleanOrRef"}

# The plain scalar type each VALUE_OR_REF_TYPES alias wraps - used by
# synth_scalar_cpp() below to synthesize a literal for a *OrRef attribute
# by recursing into its underlying type (ValueOrRef<T> has a non-explicit
# T constructor, so a plain literal converts implicitly wherever one of
# these is expected - see AttributeTypes.h).
VALUE_OR_REF_UNDERLYING = {
    "sed2::NumberOrRef": "double",
    "sed2::IntegerOrRef": "int64_t",
    "sed2::BooleanOrRef": "bool",
}


def synth_scalar_cpp(cpp_type, index):
    """A synthetic C++ literal for a scalar of 'cpp_type', parameterized by
    'index' so a list attribute's two populated entries (or two different
    attributes reusing the same helper) come out distinct. Used by both
    generate_test()'s round-trip population and its mechanical get/set
    tests - see Attribute.populate_lines()/mechanical_test_lines() below.
    """
    if cpp_type == "std::string":
        return f'"test-value-{index}"'
    if cpp_type == "double":
        return f"{index}.5"
    if cpp_type == "bool":
        return "true" if index % 2 == 1 else "false"
    if cpp_type == "int64_t":
        return str(index)
    if cpp_type == "Json":
        return f"sed2::Json({index})"
    if cpp_type in VALUE_OR_REF_TYPES:
        return synth_scalar_cpp(VALUE_OR_REF_UNDERLYING[cpp_type], index)
    raise ValueError(f"synth_scalar_cpp: no synthetic literal known for cppType {cpp_type!r}")

# Populated by main() before any generate_class() call: className -> whether
# that class's own table registers it with TypeRegistry (i.e. whether the
# spec gives it a real "_type" of its own). Consulted by Attribute.to_json
# for "owned"/"ownedArray"/"polymorphicList" attributes that fix their
# element type via "itemType" (Curve, Surface, Axis, LoopVariable,
# TaskParameter, OutputParameter, ...): those element classes have no
# "_type" property in the schema at all, so the "_type" SEDBase::toJSON
# always writes onto them has to be stripped back out before they're
# embedded in the owner's JSON - left in, it would be a stray property the
# schema (additionalProperties/unevaluatedProperties: false) rejects. An
# itemType like ParameterRange that *does* register its own "_type" (used
# via ParameterScan.parameterRanges) is left alone.
ITEM_TYPE_REGISTERS_TYPE = {}

# Populated by main() alongside ITEM_TYPE_REGISTERS_TYPE: className -> the
# Attribute list built from that class's own table. Consulted by
# populate_child_required_scalars() (see below) so a generated test that
# synthesizes a child of some other table's class (an "itemType" or
# "testItemType" target) can also satisfy *that* class's own required
# attributes, one level deep, without re-deriving its table from scratch.
ATTRIBUTE_TABLES = {}

# Attribute kinds that own a SEDBase-derived child (directly, in an array,
# or in an id-keyed list) - i.e. ones whose child(ren) get setParent(this)
# called on them somewhere, and so need it called again, with the new
# address, after this object is moved. "scalar"/"scalarList"/"map" never
# hold a SEDBase pointer, so they need no such fix-up - see
# generate_class()'s move constructor/assignment generation below.
OWNING_KINDS = {"owned", "ownedArray", "polymorphicList"}

HEADER_NOTE = (
    "// Generated by codegen/generate_classes.py from\n"
    "// codegen/spec_attributes/{class_name}.json. Do not hand-edit this file;\n"
    "// edit the attribute table and rebuild - CMake reruns the generator\n"
    "// automatically whenever a table or the generator script changes."
)


def pascal(name):
    """Capitalizes just the first character, e.g. 'kisaoID' -> 'KisaoID'."""
    if not name:
        return name
    return name[0].upper() + name[1:]


class Attribute:
    def __init__(self, data, class_name):
        self.name = data["name"]
        self.kind = data.get("kind", "scalar")
        self.cpp_type = data.get("cppType", "std::string")
        self.required = bool(data.get("required", False))
        # Only meaningful for a "scalar" attribute whose cppType is
        # std::string (an SIdRef, or a *OrRef whose literal form is a
        # string - see AttributeTypes.h): marks it as reference-checkable,
        # so validate() calls AttributeTypes::validateReference on it.
        self.is_ref = bool(data.get("isRef", False))
        self.method = pascal(self.name)
        self.field = self.name + "_"
        self.class_name = class_name
        # For list attributes, "name" is the plural used by the getter
        # (getTasks, getOutputVariables); add-/insert-/remove-/getNum- use
        # the singular "itemName" instead (addTask, not addTasks), matching
        # the conventional get<Plural>()/add<Singular>() list API. Defaults
        # to "name" itself when the table doesn't declare one - which reads
        # oddly for a plural attribute name, so scalarList/polymorphicList
        # tables should always set it explicitly.
        self.item_method = pascal(data.get("itemName", self.name))
        # "ownedArray": the fixed, non-polymorphic element type (required).
        # "polymorphicList": when set, skips TypeRegistry/loadPolymorphicChild
        # and default-constructs this fixed type instead - for containers
        # like Plot2D.curves whose entries have no '_type' to dispatch on
        # (there's only ever one concrete element type).
        self.item_type = data.get("itemType")
        # "scalarList" only: the schema's "ListOf*OrRef" shape - the JSON
        # value may be an array (populated normally) or a single SIdRef
        # standing in for the whole list (e.g. "outputVariables": "#tasks:
        # t1.names" instead of a literal array).
        self.single_ref_allowed = bool(data.get("singleRefAllowed", False))
        # "owned"/"polymorphicList" only, test-generation-only (no effect
        # on production (de)serialization): names a concrete class to
        # synthesize a child of when this attribute has no fixed itemType
        # of its own - i.e. one resolved via real TypeRegistry polymorphic
        # dispatch in production (SEDDocument.tasks, Loop.subTasks, an
        # ExplicitODESimulation's independentVariableRange, ...). Left
        # unset for an attribute the generated tests simply can't
        # synthesize a child for yet (SEDDocument.styles - no concrete
        # Style class exists in the spec); see synth_item_type() below.
        self.test_item_type = data.get("testItemType")

    # -- members -------------------------------------------------------

    def member_decl(self):
        if self.kind == "scalar":
            return f"    std::optional<{self.cpp_type}> {self.field};"
        if self.kind == "owned":
            return f"    std::unique_ptr<SEDBase> {self.field};"
        if self.kind == "scalarList":
            decl = f"    std::vector<{self.cpp_type}> {self.field};"
            if self.single_ref_allowed:
                decl += f"\n    std::optional<std::string> {self.field}WholeRef_;"
            return decl
        if self.kind == "polymorphicList":
            return f"    SEDList<SEDBase> {self.field};"
        if self.kind == "ownedArray":
            return f"    std::vector<std::unique_ptr<{self.item_type}>> {self.field};"
        if self.kind == "map":
            return f"    Json {self.field} = Json::object();"
        raise ValueError(f"{self.class_name}.{self.name}: unknown kind {self.kind!r}")

    # -- header declarations --------------------------------------------

    def declarations(self):
        m, T, im = self.method, self.cpp_type, self.item_method
        if self.kind == "scalar":
            getter_ret = f"const {T}&" if T == "std::string" else T
            setter_arg = f"const {T}&" if T == "std::string" else T
            return [
                f"    {getter_ret} get{m}() const;",
                f"    void set{m}({setter_arg} value);",
                f"    bool isSet{m}() const;",
                f"    void unset{m}();",
            ]
        if self.kind == "owned":
            return [
                f"    const SEDBase* get{m}() const;",
                f"    SEDBase* get{m}();",
                f"    void set{m}(std::unique_ptr<SEDBase> value);",
                f"    bool isSet{m}() const;",
                f"    void unset{m}();",
            ]
        if self.kind == "scalarList":
            decls = [
                f"    const std::vector<{T}>& get{m}() const;",
                f"    std::size_t getNum{m}() const;",
                f"    void add{im}(const {T}& value);",
                f"    void insert{im}(std::size_t index, const {T}& value);",
                f"    bool remove{im}(const {T}& value);",
                f"    bool isSet{m}() const;",
                f"    void unset{m}();",
            ]
            if self.single_ref_allowed:
                decls += [
                    f"    bool isSet{m}Reference() const;",
                    f"    const std::string& get{m}Reference() const;",
                    f"    void set{m}Reference(const std::string& ref);",
                ]
            return decls
        if self.kind == "ownedArray":
            it = self.item_type
            return [
                f"    std::vector<{it}*> get{m}() const;",
                f"    {it}* get{im}At(std::size_t index) const;",
                f"    std::size_t getNum{m}() const;",
                f"    void add{im}(std::unique_ptr<{it}> value);",
                f"    void insert{im}(std::size_t index, std::unique_ptr<{it}> value);",
                f"    bool remove{im}At(std::size_t index);",
                f"    bool isSet{m}() const;",
                f"    void unset{m}();",
            ]
        if self.kind == "polymorphicList":
            return [
                f"    std::vector<SEDBase*> get{m}() const;",
                f"    SEDBase* get{im}(const std::string& id) const;",
                f"    std::size_t getNum{m}() const;",
                f"    void add{im}(std::unique_ptr<SEDBase> value);",
                f"    void insert{im}(std::size_t index, std::unique_ptr<SEDBase> value);",
                f"    bool remove{im}(const std::string& id);",
                f"    bool isSet{m}() const;",
                f"    void unset{m}();",
            ]
        if self.kind == "map":
            return [
                f"    const Json& get{m}() const;",
                f"    void set{m}(const std::string& key, const Json& value);",
                f"    bool has{m}(const std::string& key) const;",
                f"    bool remove{m}(const std::string& key);",
                f"    bool isSet{m}() const;",
                f"    void unset{m}();",
            ]
        raise ValueError(f"{self.class_name}.{self.name}: unknown kind {self.kind!r}")

    # -- source definitions ----------------------------------------------

    def definitions(self, cls):
        m, T, f, im = self.method, self.cpp_type, self.field, self.item_method
        out = []
        if self.kind == "scalar":
            if T == "std::string":
                out.append(f"const std::string& {cls}::get{m}() const {{\n"
                           f"    static const std::string kDefault;\n"
                           f"    return {f}.has_value() ? *{f} : kDefault;\n}}")
                out.append(f"void {cls}::set{m}(const std::string& value) {{ {f} = value; }}")
            else:
                default = SCALAR_DEFAULTS.get(T, f"{T}{{}}")
                out.append(f"{T} {cls}::get{m}() const {{ return {f}.has_value() ? *{f} : {default}; }}")
                out.append(f"void {cls}::set{m}({T} value) {{ {f} = value; }}")
            out.append(f"bool {cls}::isSet{m}() const {{ return {f}.has_value(); }}")
            out.append(f"void {cls}::unset{m}() {{ {f}.reset(); }}")
        elif self.kind == "owned":
            out.append(f"const SEDBase* {cls}::get{m}() const {{ return {f}.get(); }}")
            out.append(f"SEDBase* {cls}::get{m}() {{ return {f}.get(); }}")
            out.append(
                f"void {cls}::set{m}(std::unique_ptr<SEDBase> value) {{\n"
                f"    if (value) value->setParent(this);\n"
                f"    {f} = std::move(value);\n}}"
            )
            out.append(f"bool {cls}::isSet{m}() const {{ return {f} != nullptr; }}")
            out.append(f"void {cls}::unset{m}() {{ {f}.reset(); }}")
        elif self.kind == "scalarList":
            out.append(f"const std::vector<{T}>& {cls}::get{m}() const {{ return {f}; }}")
            out.append(f"std::size_t {cls}::getNum{m}() const {{ return {f}.size(); }}")
            out.append(f"void {cls}::add{im}(const {T}& value) {{ {f}.push_back(value); }}")
            out.append(
                f"void {cls}::insert{im}(std::size_t index, const {T}& value) {{\n"
                f"    if (index > {f}.size()) index = {f}.size();\n"
                f"    {f}.insert({f}.begin() + static_cast<std::ptrdiff_t>(index), value);\n}}"
            )
            out.append(
                f"bool {cls}::remove{im}(const {T}& value) {{\n"
                f"    auto it = std::find({f}.begin(), {f}.end(), value);\n"
                f"    if (it == {f}.end()) return false;\n"
                f"    {f}.erase(it);\n    return true;\n}}"
            )
            if self.single_ref_allowed:
                out.append(f"bool {cls}::isSet{m}() const {{ return !{f}.empty() || {f}WholeRef_.has_value(); }}")
                out.append(f"void {cls}::unset{m}() {{ {f}.clear(); {f}WholeRef_.reset(); }}")
                out.append(f"bool {cls}::isSet{m}Reference() const {{ return {f}WholeRef_.has_value(); }}")
                out.append(
                    f"const std::string& {cls}::get{m}Reference() const {{\n"
                    f"    static const std::string kEmpty;\n"
                    f"    return {f}WholeRef_.has_value() ? *{f}WholeRef_ : kEmpty;\n}}"
                )
                out.append(f"void {cls}::set{m}Reference(const std::string& ref) {{ {f}WholeRef_ = ref; }}")
            else:
                out.append(f"bool {cls}::isSet{m}() const {{ return !{f}.empty(); }}")
                out.append(f"void {cls}::unset{m}() {{ {f}.clear(); }}")
        elif self.kind == "ownedArray":
            it = self.item_type
            out.append(
                f"std::vector<{it}*> {cls}::get{m}() const {{\n"
                f"    std::vector<{it}*> result;\n"
                f"    result.reserve({f}.size());\n"
                f"    for (const auto& item : {f}) result.push_back(item.get());\n"
                f"    return result;\n}}"
            )
            out.append(
                f"{it}* {cls}::get{im}At(std::size_t index) const {{\n"
                f"    return index < {f}.size() ? {f}[index].get() : nullptr;\n}}"
            )
            out.append(f"std::size_t {cls}::getNum{m}() const {{ return {f}.size(); }}")
            out.append(
                f"void {cls}::add{im}(std::unique_ptr<{it}> value) {{\n"
                f"    if (value) value->setParent(this);\n"
                f"    {f}.push_back(std::move(value));\n}}"
            )
            out.append(
                f"void {cls}::insert{im}(std::size_t index, std::unique_ptr<{it}> value) {{\n"
                f"    if (value) value->setParent(this);\n"
                f"    if (index > {f}.size()) index = {f}.size();\n"
                f"    {f}.insert({f}.begin() + static_cast<std::ptrdiff_t>(index), std::move(value));\n}}"
            )
            out.append(
                f"bool {cls}::remove{im}At(std::size_t index) {{\n"
                f"    if (index >= {f}.size()) return false;\n"
                f"    {f}.erase({f}.begin() + static_cast<std::ptrdiff_t>(index));\n    return true;\n}}"
            )
            out.append(f"bool {cls}::isSet{m}() const {{ return !{f}.empty(); }}")
            out.append(f"void {cls}::unset{m}() {{ {f}.clear(); }}")
        elif self.kind == "polymorphicList":
            out.append(f"std::vector<SEDBase*> {cls}::get{m}() const {{ return {f}.getAll(); }}")
            out.append(f"SEDBase* {cls}::get{im}(const std::string& id) const {{ return {f}.get(id); }}")
            out.append(f"std::size_t {cls}::getNum{m}() const {{ return {f}.size(); }}")
            out.append(
                f"void {cls}::add{im}(std::unique_ptr<SEDBase> value) {{\n"
                f"    if (value) value->setParent(this);\n"
                f"    {f}.add(std::move(value));\n}}"
            )
            out.append(
                f"void {cls}::insert{im}(std::size_t index, std::unique_ptr<SEDBase> value) {{\n"
                f"    if (value) value->setParent(this);\n"
                f"    {f}.insert(index, std::move(value));\n}}"
            )
            out.append(f"bool {cls}::remove{im}(const std::string& id) {{ return {f}.remove(id); }}")
            out.append(f"bool {cls}::isSet{m}() const {{ return !{f}.empty(); }}")
            out.append(f"void {cls}::unset{m}() {{ {f}.clear(); }}")
        elif self.kind == "map":
            out.append(f"const Json& {cls}::get{m}() const {{ return {f}; }}")
            out.append(f"void {cls}::set{m}(const std::string& key, const Json& value) {{ {f}[key] = value; }}")
            out.append(f"bool {cls}::has{m}(const std::string& key) const {{ return {f}.contains(key); }}")
            out.append(
                f"bool {cls}::remove{m}(const std::string& key) {{\n"
                f"    auto it = {f}.find(key);\n    if (it == {f}.end()) return false;\n"
                f"    {f}.erase(it);\n    return true;\n}}"
            )
            out.append(f"bool {cls}::isSet{m}() const {{ return !{f}.empty(); }}")
            out.append(f"void {cls}::unset{m}() {{ {f} = Json::object(); }}")
        return out

    # -- fromJSON / toJSON / validate fragments ---------------------------

    def from_json(self):
        # Every branch ends by erasing 'name' from unrecognizedFields_
        # (inherited from SEDBase): SEDBase::fromJSON runs first and, not
        # knowing this class's attributes, stashes *every* field it
        # doesn't itself recognize - including this one. Left unerased, a
        # subsequent toJSON() would still carry a first-seen-at-parse-time
        # copy under an unrecognizedFields_ key even after e.g. unsetX(),
        # since the parent's copy stays untouched by this class's own
        # setters/unsetters. Erasing here means unrecognizedFields_ ends up
        # holding only what truly no class in the hierarchy modeled.
        n, m, T, im = self.name, self.method, self.cpp_type, self.item_method
        erase = f'\n    unrecognizedFields_.erase("{n}");'
        if self.kind == "scalar":
            return f'    if (json.contains("{n}")) set{m}(json.at("{n}").get<{T}>());{erase}'
        if self.kind == "owned":
            if self.item_type:
                # A fixed, non-'_type' owned type (e.g. Axis) - constructed
                # directly rather than dispatched through TypeRegistry.
                return (
                    f'    if (json.contains("{n}")) {{\n'
                    f'        auto child = std::make_unique<{self.item_type}>();\n'
                    f'        child->fromJSON(json.at("{n}"));\n'
                    f'        set{m}(std::move(child));\n    }}{erase}'
                )
            return f'    if (json.contains("{n}")) set{m}(loadPolymorphicChild(json.at("{n}")));{erase}'
        if self.kind == "scalarList":
            if self.single_ref_allowed:
                return (
                    f'    if (json.contains("{n}")) {{\n'
                    f'        if (json.at("{n}").is_string()) {{\n'
                    f'            set{m}Reference(json.at("{n}").get<std::string>());\n'
                    f'        }} else {{\n'
                    f'            for (const auto& item : json.at("{n}")) add{im}(item.get<{T}>());\n'
                    f'        }}\n    }}{erase}'
                )
            return (f'    if (json.contains("{n}")) {{\n'
                    f'        for (const auto& item : json.at("{n}")) add{im}(item.get<{T}>());\n    }}{erase}')
        if self.kind == "ownedArray":
            return (
                f'    if (json.contains("{n}")) {{\n'
                f'        for (const auto& item : json.at("{n}")) {{\n'
                f'            auto child = std::make_unique<{self.item_type}>();\n'
                f'            child->fromJSON(item);\n'
                f'            add{im}(std::move(child));\n        }}\n    }}{erase}'
            )
        if self.kind == "polymorphicList":
            if self.item_type:
                construct = f'std::make_unique<{self.item_type}>()'
                return (
                    f'    if (json.contains("{n}")) {{\n'
                    f'        for (auto it = json.at("{n}").begin(); it != json.at("{n}").end(); ++it) {{\n'
                    f'            auto child = {construct};\n'
                    f'            child->fromJSON(it.value());\n'
                    f'            if (!child->isSetId()) child->setId(it.key());\n'
                    f'            add{im}(std::move(child));\n        }}\n    }}{erase}'
                )
            return (
                f'    if (json.contains("{n}")) {{\n'
                f'        for (auto it = json.at("{n}").begin(); it != json.at("{n}").end(); ++it) {{\n'
                f'            auto child = loadPolymorphicChild(it.value());\n'
                f'            if (!child->isSetId()) child->setId(it.key());\n'
                f'            add{im}(std::move(child));\n        }}\n    }}{erase}'
            )
        if self.kind == "map":
            return (
                f'    if (json.contains("{n}")) {{\n'
                f'        for (auto it = json.at("{n}").begin(); it != json.at("{n}").end(); ++it) {{\n'
                f'            set{m}(it.key(), it.value());\n        }}\n    }}{erase}'
            )
        raise ValueError(self.kind)

    def _item_type_omits_type(self):
        # True when this attribute's fixed itemType has no "_type" of its
        # own in the schema (see ITEM_TYPE_REGISTERS_TYPE) - the element
        # class's toJSON() always writes one anyway (SEDBase::toJSON), so
        # to_json has to strip it back out before embedding.
        return bool(self.item_type) and not ITEM_TYPE_REGISTERS_TYPE.get(self.item_type, True)

    def to_json(self):
        n, m, f = self.name, self.method, self.field
        if self.kind == "owned":
            if self._item_type_omits_type():
                return (f'    if (isSet{m}()) {{\n        Json child = {f}->toJSON();\n'
                        f'        child.erase("_type");\n        json["{n}"] = child;\n    }}')
            return f'    if (isSet{m}()) json["{n}"] = {f}->toJSON();'
        if self.kind == "scalarList" and self.single_ref_allowed:
            return (f'    if (isSet{m}Reference()) {{\n        json["{n}"] = get{m}Reference();\n'
                    f'    }} else if (isSet{m}()) {{\n        json["{n}"] = get{m}();\n    }}')
        if self.kind == "ownedArray":
            if self._item_type_omits_type():
                return (f'    if (isSet{m}()) {{\n        Json array = Json::array();\n'
                        f'        for (const auto* item : get{m}()) {{\n'
                        f'            Json itemJson = item->toJSON();\n'
                        f'            itemJson.erase("_type");\n'
                        f'            array.push_back(itemJson);\n        }}\n'
                        f'        json["{n}"] = array;\n    }}')
            return (f'    if (isSet{m}()) {{\n        Json array = Json::array();\n'
                    f'        for (const auto* item : get{m}()) array.push_back(item->toJSON());\n'
                    f'        json["{n}"] = array;\n    }}')
        if self.kind == "polymorphicList":
            # A polymorphicList's id is the dictionary key an item is
            # stored under, not a property of the item's own JSON (the
            # spec never declares "id" among a task/output/etc's allowed
            # properties, the same way SEDDocument itself carries no
            # "_type" - see SEDDocument::toJSON()), so it's erased here
            # after fromJSON's parse-time getId()/setId(it.key()) is done
            # using it. Fixed-itemType elements with no "_type" of their
            # own (see _item_type_omits_type) get that stripped too.
            erase_type = '\n            itemJson.erase("_type");' if self._item_type_omits_type() else ''
            return (
                f'    if (isSet{m}()) {{\n        Json container = Json::object();\n'
                f'        for (auto* item : {f}.getAll()) {{\n'
                f'            Json itemJson = item->toJSON();\n'
                f'            itemJson.erase("id");{erase_type}\n'
                f'            container[item->getId()] = itemJson;\n        }}\n'
                f'        json["{n}"] = container;\n    }}'
            )
        return f'    if (isSet{m}()) json["{n}"] = get{m}();'

    def validate(self, class_name):
        lines = []
        if self.required:
            lines.append(
                f'    if (!isSet{self.method}()) {{\n'
                f'        errors.emplace_back("", "{class_name}.{self.name} is required", "");\n    }}'
            )
        if self.kind == "owned":
            lines.append(f"    if ({self.field}) {self.field}->validate(errors);")
        elif self.kind == "polymorphicList":
            lines.append(f"    for (auto* item : {self.field}.getAll()) {{\n"
                         f"        if (item) item->validate(errors);\n    }}")
        elif self.kind == "ownedArray":
            lines.append(f"    for (const auto* item : get{self.method}()) {{\n"
                         f"        if (item) item->validate(errors);\n    }}")
        elif self.kind == "scalar" and self.is_ref and self.cpp_type == "std::string":
            lines.append(f'    validateReference(*this, "{self.name}", get{self.method}(), errors);')
        elif self.kind == "scalar" and self.is_ref and self.cpp_type in VALUE_OR_REF_TYPES:
            lines.append(
                f'    if (get{self.method}().isRef) '
                f'validateReference(*this, "{self.name}", get{self.method}().refValue, errors);'
            )
        elif self.kind == "scalarList" and self.single_ref_allowed and self.is_ref:
            lines.append(
                f'    if (isSet{self.method}Reference()) '
                f'validateReference(*this, "{self.name}", get{self.method}Reference(), errors);'
            )
        return lines

    # -- move constructor/assignment (see generate_class()) --------------

    def is_owning(self):
        return self.kind in OWNING_KINDS

    def move_assign_lines(self):
        # Every member type here (optional, unique_ptr, vector, SEDList,
        # Json) has its own move-assignment operator, so this is the same
        # one-liner regardless of kind - only the extra WholeRef_ member
        # (scalarList + singleRefAllowed) needs a second line.
        lines = [f"    {self.field} = std::move(other.{self.field});"]
        if self.kind == "scalarList" and self.single_ref_allowed:
            lines.append(f"    {self.field}WholeRef_ = std::move(other.{self.field}WholeRef_);")
        return lines

    def reconnect_lines(self):
        # Re-homes this attribute's child(ren) - which kept their own
        # addresses across the move (only the pointer/handle to them
        # moved) - onto the new owner address, undoing the dangling
        # SEDBase::parent_ a plain member-wise move would otherwise leave
        # behind. Only called for is_owning() attributes.
        f = self.field
        if self.kind == "owned":
            return [f"    if ({f}) {f}->setParent(this);"]
        if self.kind == "ownedArray":
            return [f"    for (auto& item : {f}) {{\n        if (item) item->setParent(this);\n    }}"]
        if self.kind == "polymorphicList":
            return [f"    for (auto* item : {f}.getAll()) {{\n        if (item) item->setParent(this);\n    }}"]
        return []

    # -- generated-test support (see generate_test() below) --------------

    def synth_item_type(self):
        # The concrete class a generated test constructs to populate this
        # "owned"/"ownedArray"/"polymorphicList" attribute: itemType when
        # the attribute is already fixed to one non-polymorphic type in
        # production, otherwise the test-only testItemType hint. None
        # means no generated test can synthesize this attribute at all
        # (e.g. SEDDocument.styles) - callers skip it rather than fail.
        return self.item_type or self.test_item_type

    def mechanical_test_lines(self):
        """The body (as a single string of statements operating on a
        stack variable 'obj') of this attribute's own get/set/isSet/unset
        TEST case. Returns None for an "owned"/"polymorphicList" attribute
        with no synth_item_type() - nothing to construct a child from.
        """
        m, T, im = self.method, self.cpp_type, self.item_method
        if self.kind == "scalar":
            lit = synth_scalar_cpp(T, 1)
            get_expr = f"obj.get{m}()"
            cmp_expr = f"{get_expr}.value" if T in VALUE_OR_REF_TYPES else get_expr
            return (
                f"    EXPECT_FALSE(obj.isSet{m}());\n"
                f"    obj.set{m}({lit});\n"
                f"    EXPECT_TRUE(obj.isSet{m}());\n"
                f"    EXPECT_EQ({cmp_expr}, {lit});\n"
                f"    obj.unset{m}();\n"
                f"    EXPECT_FALSE(obj.isSet{m}());"
            )
        if self.kind == "scalarList":
            lit1, lit2, lit3 = synth_scalar_cpp(T, 1), synth_scalar_cpp(T, 2), synth_scalar_cpp(T, 3)
            elem_expr = f"obj.get{m}()[1]"
            elem_cmp = f"{elem_expr}.value" if T in VALUE_OR_REF_TYPES else elem_expr
            return (
                f"    EXPECT_FALSE(obj.isSet{m}());\n"
                f"    obj.add{im}({lit1});\n"
                f"    obj.add{im}({lit2});\n"
                f"    EXPECT_EQ(obj.getNum{m}(), 2u);\n"
                f"    EXPECT_TRUE(obj.isSet{m}());\n"
                f"    obj.insert{im}(1, {lit3});\n"
                f"    ASSERT_EQ(obj.getNum{m}(), 3u);\n"
                f"    EXPECT_EQ({elem_cmp}, {lit3});\n"
                f"    EXPECT_TRUE(obj.remove{im}({lit3}));\n"
                f"    EXPECT_EQ(obj.getNum{m}(), 2u);\n"
                f"    obj.unset{m}();\n"
                f"    EXPECT_FALSE(obj.isSet{m}());"
            )
        if self.kind == "map":
            return (
                f"    EXPECT_FALSE(obj.isSet{m}());\n"
                f'    obj.set{m}("k", sed2::Json(1));\n'
                f'    EXPECT_TRUE(obj.has{m}("k"));\n'
                f"    EXPECT_TRUE(obj.isSet{m}());\n"
                f'    obj.remove{m}("k");\n'
                f"    EXPECT_FALSE(obj.isSet{m}());"
            )
        if self.kind == "ownedArray":
            it = self.item_type
            return (
                f"    EXPECT_FALSE(obj.isSet{m}());\n"
                f"    obj.add{im}(std::make_unique<sed2::{it}>());\n"
                f"    EXPECT_EQ(obj.getNum{m}(), 1u);\n"
                f"    EXPECT_TRUE(obj.isSet{m}());\n"
                f"    obj.unset{m}();\n"
                f"    EXPECT_FALSE(obj.isSet{m}());"
            )
        if self.kind == "owned":
            t = self.synth_item_type()
            if not t:
                return None
            return (
                f"    EXPECT_FALSE(obj.isSet{m}());\n"
                f"    obj.set{m}(std::make_unique<sed2::{t}>());\n"
                f"    EXPECT_TRUE(obj.isSet{m}());\n"
                f"    obj.unset{m}();\n"
                f"    EXPECT_FALSE(obj.isSet{m}());"
            )
        if self.kind == "polymorphicList":
            t = self.synth_item_type()
            if not t:
                return None
            return (
                f"    EXPECT_FALSE(obj.isSet{m}());\n"
                f"    {{\n"
                f"        auto child = std::make_unique<sed2::{t}>();\n"
                f'        child->setId("item1");\n'
                f"        obj.add{im}(std::move(child));\n"
                f"    }}\n"
                f"    EXPECT_EQ(obj.getNum{m}(), 1u);\n"
                f'    EXPECT_NE(obj.get{im}("item1"), nullptr);\n'
                f"    EXPECT_TRUE(obj.isSet{m}());\n"
                f"    obj.unset{m}();\n"
                f"    EXPECT_FALSE(obj.isSet{m}());"
            )
        raise ValueError(self.kind)

    def populate_lines(self, obj_var, index):
        """For generate_test()'s round-trip test: statements that set this
        attribute to a synthetic value on '{obj_var}.'. Returns (lines,
        next_index). An owning attribute with no synth_item_type() is left
        unpopulated (empty lines) rather than failing the whole class's
        test - its round trip just doesn't cover that one attribute.
        """
        m, im = self.method, self.item_method
        if self.kind == "scalar":
            return [f"    {obj_var}.set{m}({synth_scalar_cpp(self.cpp_type, index)});"], index + 1
        if self.kind == "scalarList":
            lit1 = synth_scalar_cpp(self.cpp_type, index)
            lit2 = synth_scalar_cpp(self.cpp_type, index + 1)
            return [f"    {obj_var}.add{im}({lit1});", f"    {obj_var}.add{im}({lit2});"], index + 2
        if self.kind == "map":
            return [f'    {obj_var}.set{m}("key{index}", sed2::Json({index}));'], index + 1
        if self.kind in OWNING_KINDS:
            t = self.synth_item_type()
            if not t:
                return [], index
            lines = ["    {"]
            if self.kind == "owned":
                lines.append(f"        auto child = std::make_unique<sed2::{t}>();")
                child_lines, index = populate_child_required_scalars(t, "child", index)
                lines += child_lines
                lines.append(f"        {obj_var}.set{m}(std::move(child));")
            elif self.kind == "ownedArray":
                lines.append(f"        auto child = std::make_unique<sed2::{self.item_type}>();")
                child_lines, index = populate_child_required_scalars(self.item_type, "child", index)
                lines += child_lines
                lines.append(f"        {obj_var}.add{im}(std::move(child));")
            else:  # polymorphicList
                lines.append(f"        auto child = std::make_unique<sed2::{t}>();")
                lines.append(f'        child->setId("child{index}");')
                index += 1
                child_lines, index = populate_child_required_scalars(t, "child", index)
                lines += child_lines
                lines.append(f"        {obj_var}.add{im}(std::move(child));")
            lines.append("    }")
            return lines, index
        raise ValueError(self.kind)

    def owned_populate_and_capture(self, obj_var, capture_var, index):
        """For generate_test()'s move-safety test: attaches one synthetic
        child to this (owning) attribute on '{obj_var}.' and pushes its
        raw SEDBase* onto '{capture_var}' (a std::vector<sed2::SEDBase*>
        already in scope), so the test can check its parent pointer after
        the move. Returns (lines, next_index), or (None, index) when this
        attribute has no synth_item_type() to construct - see
        synth_item_type(). Unlike populate_lines(), the synthesized
        child's own required attributes are left unset: this test only
        checks reparenting, not validate().
        """
        t = self.synth_item_type()
        if not t:
            return None, index
        m, im = self.method, self.item_method
        if self.kind == "owned":
            lines = [
                "    {",
                f"        auto child = std::make_unique<sed2::{t}>();",
                f"        {capture_var}.push_back(child.get());",
                f"        {obj_var}.set{m}(std::move(child));",
                "    }",
            ]
            return lines, index
        if self.kind == "ownedArray":
            lines = [
                "    {",
                f"        auto child = std::make_unique<sed2::{self.item_type}>();",
                f"        {capture_var}.push_back(child.get());",
                f"        {obj_var}.add{im}(std::move(child));",
                "    }",
            ]
            return lines, index
        # polymorphicList
        lines = [
            "    {",
            f"        auto child = std::make_unique<sed2::{t}>();",
            f'        child->setId("synthChild{index}");',
            f"        {capture_var}.push_back(child.get());",
            f"        {obj_var}.add{im}(std::move(child));",
            "    }",
        ]
        return lines, index + 1


def populate_child_required_scalars(class_name, var, index):
    """For generate_test()'s round-trip test (see Attribute.populate_lines
    above): after constructing a synthetic child of 'class_name', held in
    variable 'var' (a std::unique_ptr, accessed via '->'), populates just
    that child's own required scalar/scalarList/map attributes - not
    recursing into any owned/ownedArray/polymorphicList attribute of its
    own - so the child's own validate() doesn't fail with "X is required"
    once it's attached and the whole tree gets validated. One level deep
    is all today's catalog needs: no itemType/testItemType target class
    (TaskParameter, OutputParameter, Axis, Curve, Surface, LoopVariable,
    ParameterRange, Span, NumericRange, ModelImport, Report,
    AggregationCalculation) has a *required* owned/array/list attribute of
    its own. If a future one does, its required child stays unset here
    (silently, not an error) - the class's own generated round-trip test
    would then need this extended to recurse further.
    """
    lines = []
    for attr in ATTRIBUTE_TABLES.get(class_name, []):
        if not attr.required:
            continue
        if attr.kind == "scalar":
            lines.append(f"        {var}->set{attr.method}({synth_scalar_cpp(attr.cpp_type, index)});")
            index += 1
        elif attr.kind == "scalarList":
            lines.append(f"        {var}->add{attr.item_method}({synth_scalar_cpp(attr.cpp_type, index)});")
            index += 1
        elif attr.kind == "map":
            lines.append(f'        {var}->set{attr.method}("key{index}", sed2::Json({index}));')
            index += 1
        # else: a required owned/ownedArray/polymorphicList attribute -
        # not recursed into, see docstring above.
    return lines, index


def generate_class(table):
    class_name = table["className"]
    type_name = table["typeName"]
    parent = table.get("parent", "SEDBase")
    generate_base_only = bool(table.get("generateBaseOnly", False))
    register_type = bool(table.get("registerType", True))
    dot_accessors = table.get("dotAccessors", [])
    bare_reference_valid = bool(table.get("bareReferenceValid", True))
    attributes = [Attribute(a, class_name) for a in table.get("attributes", [])]

    emitted_namespace = "sed2::generated" if generate_base_only else "sed2"
    parent_include = "sed2/core/SEDBase.h" if parent == "SEDBase" else f"sed2/generated/{parent}.h"

    note = HEADER_NOTE.format(class_name=class_name)

    # -- header -----------------------------------------------------------
    member_decls = "\n".join(a.member_decl() for a in attributes)
    accessor_decls = "\n".join(line for a in attributes for line in a.declarations())

    # ownedArray, and polymorphicList with an explicit itemType, reference
    # a fixed element class by name in their accessor signatures - each
    # needs that class's own generated header.
    item_type_includes = sorted({a.item_type for a in attributes if a.item_type})
    item_type_include_lines = "\n".join(f'#include "sed2/generated/{t}.h"' for t in item_type_includes)

    # A class that owns at least one SEDBase-derived child (an "owned"/
    # "ownedArray"/"polymorphicList" attribute) needs a move constructor
    # and move-assignment operator that re-run setParent() on each direct
    # child afterward - a plain member-wise move (what the compiler would
    # otherwise generate implicitly) moves the unique_ptr/SEDList handles
    # correctly, but leaves every child's own SEDBase::parent_ pointing at
    # this object's OLD address. That address is only actually observed
    # to change today when a SEDDocument is returned by value from
    # fromFile()/fromJSONString() without NRVO (e.g. MSVC Debug), but the
    # same risk exists for any owning class, so every one of them gets
    # this fix uniformly rather than special-casing SEDDocument. A class
    # with no such attribute never owns a SEDBase pointer, so its default
    # (compiler-generated) move already has nothing to fix up and is left
    # alone. Declaring these also makes copy explicitly deleted (rather
    # than incidentally deleted via a non-copyable member, e.g. a
    # unique_ptr) - see codegen/generate_classes.py's module docstring.
    owning_attributes = [a for a in attributes if a.is_owning()]
    needs_move_fix = bool(owning_attributes)
    special_members_decl = ""
    reconnect_decl = ""
    if needs_move_fix:
        special_members_decl = (
            f"    {class_name}() = default;\n"
            f"    {class_name}(const {class_name}&) = delete;\n"
            f"    {class_name}& operator=(const {class_name}&) = delete;\n"
            f"    {class_name}({class_name}&& other) noexcept;\n"
            f"    {class_name}& operator=({class_name}&& other) noexcept;\n\n"
        )
        reconnect_decl = "    void reconnectOwnedChildren();\n"

    extra_overrides = ""
    if dot_accessors:
        accessor_list = ", ".join(f'"{a}"' for a in dot_accessors)
        extra_overrides += (
            f"    std::vector<std::string> getDeclaredDotAccessors() const override "
            f"{{ return {{{accessor_list}}}; }}\n"
        )
    if not bare_reference_valid:
        extra_overrides += "    bool isBareReferenceValid() const override { return false; }\n"

    header = f"""#pragma once
{note}

#include <cstddef>
#include <cstdint>
#include <memory>
#include <optional>
#include <string>
#include <vector>

#include "{parent_include}"
#include "sed2/core/AttributeTypes.h"
#include "sed2/core/Json.h"
#include "sed2/core/SEDList.h"
#include "sed2/core/TypeRegistry.h"
{item_type_include_lines}

namespace {emitted_namespace} {{

class {class_name} : public {parent} {{
public:
{special_members_decl}    std::string getTypeName() const override {{ return "{type_name}"; }}
{extra_overrides}
    void fromJSON(const Json& json) override;
    Json toJSON() const override;
    void validate(std::vector<ValidationError>& errors) const override;

{accessor_decls}

private:
{reconnect_decl}{member_decls}
}};

}}  // namespace {emitted_namespace}
"""

    # -- source -------------------------------------------------------------
    qualified_cls = f"{emitted_namespace}::{class_name}"
    definitions = "\n\n".join(
        "\n".join(a.definitions(class_name)) for a in attributes
    )
    from_json_body = "\n".join(a.from_json() for a in attributes)
    to_json_body = "\n".join(a.to_json() for a in attributes)
    validate_body = "\n".join(line for a in attributes for line in a.validate(class_name))

    # See the needs_move_fix comment above: move-assign every member
    # (moving the handle - unique_ptr/vector/SEDList/optional/Json - is
    # always correct on its own), then re-home the owning ones' children.
    # The move constructor just default-constructs and delegates to move-
    # assignment rather than duplicating the member list a second time.
    move_source = ""
    if needs_move_fix:
        move_assign_body = "\n".join(line for a in attributes for line in a.move_assign_lines())
        reconnect_body = "\n".join(line for a in owning_attributes for line in a.reconnect_lines())
        move_source = f"""
{class_name}::{class_name}({class_name}&& other) noexcept : {class_name}() {{
    *this = std::move(other);
}}

{class_name}& {class_name}::operator=({class_name}&& other) noexcept {{
    if (this == &other) return *this;
    {parent}::operator=(std::move(other));
{move_assign_body}
    reconnectOwnedChildren();
    return *this;
}}

void {class_name}::reconnectOwnedChildren() {{
{reconnect_body}
}}
"""

    # A named, externally-linked function (rather than an anonymous-
    # namespace static-initializer, per TypeRegistry.h) so registering this
    # class is a real symbol reference that a linker can't drop from a
    # static-library build - see registerGeneratedTypes() in
    # TypeRegistry.h/Registrations.cpp.
    registration = ""
    if register_type:
        registration = f"""
namespace sed2::codegen_registration {{
void register_{class_name}(TypeRegistry& registry) {{
    registry.registerType("{type_name}", [](const Json& json) -> std::unique_ptr<::sed2::SEDBase> {{
        auto object = std::make_unique<::{qualified_cls}>();
        object->fromJSON(json);
        return object;
    }});
}}
}}  // namespace sed2::codegen_registration
"""

    source = f"""{note}

#include "sed2/generated/{class_name}.h"

#include <algorithm>
#include <utility>

#include "sed2/core/AttributeTypes.h"

namespace {emitted_namespace} {{

void {class_name}::fromJSON(const Json& json) {{
    {parent}::fromJSON(json);
{from_json_body}
}}

Json {class_name}::toJSON() const {{
    Json json = {parent}::toJSON();
{to_json_body}
    return json;
}}

void {class_name}::validate(std::vector<ValidationError>& errors) const {{
    {parent}::validate(errors);
{validate_body}
}}
{move_source}
{definitions}

}}  // namespace {emitted_namespace}
{registration}"""

    return header, source, (class_name if register_type else None)


def generate_test(table):
    """Emits a gtest source (tests/test_<ClassName>.cpp, built into the
    separate sed2_generated_tests target - see tests/CMakeLists.txt) that
    mechanically exercises the class generate_class() just produced from
    this same table: its TypeName, that a fresh instance has nothing set,
    each attribute's own get/set/isSet/unset round trip, a full
    populate -> toJSON -> fromJSON -> toJSON round trip (asserting
    validate() finds nothing wrong), a missing-required-attributes check,
    and - for a class that owns at least one child - the move/reparenting
    regression this whole feature exists to generalize (see OWNING_KINDS's
    docstring and the hand-written tests this generalizes, e.g.
    tests/unit/test_SEDDocument.cpp's SurvivesExplicitMoveConstruction).

    Returns None for a "generateBaseOnly" class (SEDDocument today): that
    class is wrapped by a hand-written subclass adding behavior no table
    can express (file/string loading, cross-reference resolution - see
    include/sed2/core/SEDDocument.h), so testing sed2::generated::
    SEDDocument directly wouldn't test the class anything actually uses;
    tests/unit/test_SEDDocument.cpp covers it by hand instead.
    """
    if table.get("generateBaseOnly", False):
        return None

    class_name = table["className"]
    type_name = table["typeName"]
    attributes = ATTRIBUTE_TABLES[class_name]
    owning_attributes = [a for a in attributes if a.is_owning()]
    note = HEADER_NOTE.format(class_name=class_name)

    item_type_includes = sorted(
        {a.item_type for a in attributes if a.item_type} | {a.synth_item_type() for a in attributes if a.synth_item_type()}
    )
    include_lines = "\n".join(f'#include "sed2/generated/{t}.h"' for t in item_type_includes)

    tests = []

    tests.append(f'''TEST({class_name}Generated, TypeName) {{
    sed2::{class_name} obj;
    EXPECT_EQ(obj.getTypeName(), "{type_name}");
}}''')

    isset_checks = "\n".join(f"    EXPECT_FALSE(obj.isSet{a.method}());" for a in attributes)
    tests.append(f'''TEST({class_name}Generated, DefaultConstructionHasNothingSet) {{
    sed2::{class_name} obj;
{isset_checks}
}}''')

    for a in attributes:
        body = a.mechanical_test_lines()
        if body is None:
            continue
        tests.append(f'''TEST({class_name}Generated, {a.method}GetSetIsSetUnset) {{
    sed2::{class_name} obj;
{body}
}}''')

    populate_lines = []
    index = 1
    for a in attributes:
        plines, index = a.populate_lines("obj", index)
        populate_lines.extend(plines)
    populate_body = "\n".join(populate_lines)
    tests.append(f'''TEST({class_name}Generated, FromJsonToJsonRoundTrip) {{
    sed2::{class_name} obj;
{populate_body}

    std::vector<sed2::ValidationError> errors;
    obj.validate(errors);
    for (const auto& e : errors) ADD_FAILURE() << e.path << ": " << e.message;
    EXPECT_TRUE(errors.empty());

    sed2::Json firstPass = obj.toJSON();
    sed2::{class_name} reloaded;
    reloaded.fromJSON(firstPass);
    EXPECT_EQ(reloaded.toJSON(), firstPass);
}}''')

    required_count = sum(1 for a in attributes if a.required)
    if required_count:
        tests.append(f'''TEST({class_name}Generated, ValidateReportsMissingRequiredAttributes) {{
    sed2::{class_name} obj;
    std::vector<sed2::ValidationError> errors;
    obj.validate(errors);
    EXPECT_GE(errors.size(), {required_count}u);
}}''')

    if owning_attributes:
        attach_lines = []
        idx = 1
        for a in owning_attributes:
            plines, idx = a.owned_populate_and_capture("original", "children", idx)
            if plines:
                attach_lines.extend(plines)
        if attach_lines:
            attach_body = "\n".join(attach_lines)
            tests.append(f'''TEST({class_name}Generated, SurvivesExplicitMoveConstruction) {{
    sed2::{class_name} original;
    std::vector<sed2::SEDBase*> children;
{attach_body}

    sed2::{class_name} moved(std::move(original));

    for (auto* child : children) {{
        EXPECT_EQ(child->getParent(), &moved);
    }}
}}''')

    body = "\n\n".join(tests)

    return f"""{note}

#include <gtest/gtest.h>

#include <memory>
#include <utility>
#include <vector>

#include "sed2/core/SEDBase.h"
#include "sed2/core/Json.h"
#include "sed2/generated/{class_name}.h"
#include "sed2/validation/ValidationError.h"
{include_lines}

{body}
"""


def load_tables(tables_dir):
    """Reads every codegen/spec_attributes/*.json table into a {className:
    table} dict, keyed and validated the same way for any script that needs
    them (generate_classes.py's own main() below, and codegen/
    generate_ctypes.py, which binds the same tables to a C API/ctypes
    Python module rather than to C++ classes).
    """
    table_files = sorted(f for f in os.listdir(tables_dir) if f.endswith(".json"))
    tables = {}
    for filename in table_files:
        path = os.path.join(tables_dir, filename)
        with open(path, "r", encoding="utf-8") as fh:
            table = json.load(fh)

        expected_class = os.path.splitext(filename)[0]
        if table.get("className") != expected_class:
            raise SystemExit(
                f"{path}: className {table.get('className')!r} does not match "
                f"filename (expected {expected_class!r})"
            )
        tables[expected_class] = table
    return tables


def populate_globals(tables):
    """Fills in ITEM_TYPE_REGISTERS_TYPE and ATTRIBUTE_TABLES from a
    load_tables() result - shared by generate_classes.py's main() and
    codegen/generate_ctypes.py, both of which need these populated before
    generating anything (a table's itemType/testItemType target can be any
    other table's class, regardless of file order - see each global's own
    docstring above).
    """
    global ITEM_TYPE_REGISTERS_TYPE, ATTRIBUTE_TABLES
    ITEM_TYPE_REGISTERS_TYPE = {
        name: bool(table.get("registerType", True)) for name, table in tables.items()
    }
    ATTRIBUTE_TABLES = {
        name: [Attribute(a, name) for a in table.get("attributes", [])] for name, table in tables.items()
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tables-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    header_dir = os.path.join(args.out_dir, "include", "sed2", "generated")
    source_dir = os.path.join(args.out_dir, "src")
    tests_dir = os.path.join(args.out_dir, "tests")
    os.makedirs(header_dir, exist_ok=True)
    os.makedirs(source_dir, exist_ok=True)
    os.makedirs(tests_dir, exist_ok=True)

    tables = load_tables(args.tables_dir)
    populate_globals(tables)

    registered_classes = []
    for class_name, table in sorted(tables.items()):
        header, source, registered_class = generate_class(table)
        if registered_class:
            registered_classes.append(registered_class)

        with open(os.path.join(header_dir, f"{class_name}.h"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(header)
        with open(os.path.join(source_dir, f"{class_name}.cpp"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(source)

        test_source = generate_test(table)
        if test_source is not None:
            with open(os.path.join(tests_dir, f"test_{class_name}.cpp"), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(test_source)

    write_registrations(source_dir, registered_classes)

    print(f"sed2: generated {len(tables)} class(es) into {args.out_dir}")


def write_registrations(source_dir, registered_classes):
    """Emits Registrations.cpp: one forward declaration per generated,
    registerType:true class's register_<ClassName> function (see
    generate_class() above), aggregated into the registerGeneratedTypes()
    that TypeRegistry::instance() calls. Regenerated in full on every run
    (there's no attribute table of its own to key a rebuild off), so it
    always lists exactly the classes the rest of this run just produced.
    """
    declarations = "\n".join(
        f"void register_{name}(::sed2::TypeRegistry& registry);" for name in registered_classes
    )
    calls = "\n".join(f"    codegen_registration::register_{name}(registry);" for name in registered_classes)

    source = f"""// Generated by codegen/generate_classes.py. Do not hand-edit this file;
// it is rewritten from scratch, listing every registerType:true class
// under codegen/spec_attributes, on each run.

#include "sed2/core/TypeRegistry.h"

namespace sed2::codegen_registration {{
{declarations}
}}  // namespace sed2::codegen_registration

namespace sed2 {{

void registerGeneratedTypes(TypeRegistry& registry) {{
{calls}
}}

}}  // namespace sed2
"""
    with open(os.path.join(source_dir, "Registrations.cpp"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(source)


if __name__ == "__main__":
    main()

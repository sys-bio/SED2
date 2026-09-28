"""Emit the generated C++ target library from a SpecModel. Namespace/CMake
project+target name is caller-supplied (see emit_cpp_package()) - "sed2test"
below is just the Phase-1 test-tree default.

Mirrors generator/emit_python.py and generator/emit_java.py's architecture
and rule-mapping decisions exactly (see emit_python.py's docstring and
Design.md's Schema-Pass Errors / Toolchain sections): validate() is a
schema-pass rule-ID mapping, leaf fields are checked against a tiny
per-field JSON Schema fragment using the language's own real validator
library (jsoncons's bundled jsonschema extension, per Design.md's Toolchain
mandate), and every load-time violation (extra properties, bad
dict-of-discriminated-union keys, bad container shapes, dispatch problems
bubbled up from a nested item) is detected once, at load time, in
load_fields() - the only point that still has the raw JSON before an
unrecognized key is dropped.

The library is emitted header-only (all methods defined inline) since
every type here is either a thin wrapper over jsoncons::json or a small
value/aggregate type - this sidesteps needing a compiled static library
target while still giving CMake a clean INTERFACE library to link tests
against. jsoncons itself is header-only for the same reason.

Ownership: children (dict/array collection items) are owned via
std::unique_ptr<SedBase>; parent/document backpointers are non-owning raw
pointers, matching Design.md's stated C++ raw-pointer intent (the same
design the Python target's weakref usage and the Java target's
WeakReference usage both approximate in their own languages).
"""
from __future__ import annotations

import json as _json
import os
from .spec import SpecModel, Field, FlatClass

NS = "sed2test"


def _cpp_ident(name: str) -> str:
    """Field/property name -> a snake_case-ish C++ identifier fragment,
    e.g. 'acme@priority' -> 'acme_priority'. Plain field names in
    test-specsheets/ schemas are camelCase (value, label, timeoutSeconds);
    kept as-is since C++ has no strong naming convention friction there,
    only '@' needs handling."""
    if "@" in name:
        prefix, key = name.split("@", 1)
        return f"{prefix}_{_cpp_ident(key)}"
    return name


def _cpp_lit(s) -> str:
    """None -> C++ nullopt marker handled by caller; else a C++ string
    literal. json.dumps produces double-quoted, backslash-escaped text
    that is also valid C++ source."""
    return _json.dumps(s)


def _cpp_opt_str(s) -> str:
    return "std::nullopt" if s is None else f"std::string({_cpp_lit(s)})"


def _cpp_opt_double(v) -> str:
    return "std::nullopt" if v is None else repr(float(v))


# ---------------------------------------------------------------------------
# Runtime.hpp - hand-authored, identical for every spec (one copy per
# generate.py run, exactly like emit_python.py's RUNTIME string and
# emit_java.py's runtime_files()).
# ---------------------------------------------------------------------------

def _runtime_hpp(NS: str) -> str:
    # NS shadows the module-level default of the same name on purpose, so
    # every {NS} interpolation below picks up the caller's namespace - see
    # emit_cpp_package(), the only caller.
    return f'''// Shared runtime. GENERATED - do not
// hand-edit; regenerate via generator/generate.py.
#pragma once

#include <algorithm>
#include <map>
#include <memory>
#include <optional>
#include <ostream>
#include <regex>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

#include <jsoncons/json.hpp>
#include <jsoncons_ext/jsonschema/jsonschema.hpp>

namespace {NS} {{

/// Raised for any misuse of the generated API itself (wrong-kind OrRef
/// access, get on an unset field, an out-of-range insert, ...) - never for
/// a document that merely fails a SED2 validation rule. See Design.md's
/// Classes section.
class ApiError : public std::runtime_error {{
public:
    explicit ApiError(const std::string& message) : std::runtime_error(message) {{}}
}};

struct ValidationProblem {{
    std::string rule_id;
    std::string severity;
    std::string rule;
    std::string message;
    std::string location;

    bool operator==(const ValidationProblem& other) const {{
        return rule_id == other.rule_id && location == other.location;
    }}
}};

inline std::ostream& operator<<(std::ostream& os, const ValidationProblem& p) {{
    os << "ValidationProblem(" << p.rule_id << ", " << p.severity << ", " << p.location << ")";
    return os;
}}

/// Plain aggregate - deliberately no user-declared constructors, so it can
/// be brace-initialized positionally by generated code (see
/// generator/emit_cpp.py's _field_spec_expr()).
struct FieldSpec {{
    std::string name;
    std::string kind;
    bool required;
    std::optional<std::string> rule_id;
    std::optional<std::string> required_rule_id;
    std::string origin_catchall;
    std::optional<double> minimum;
    std::optional<double> exclusive_minimum;
    std::optional<std::string> pattern;
    std::optional<std::string> item_class;
    std::optional<std::string> item_discriminator;
}};

/// Rule catalogue + ValidationProblem factory. Populated by
/// RulesData::register_rules() - see Io::read_from_string(), which calls
/// it once. Placeholders are an explicit map (not variadic/kwargs-style),
/// so - unlike the Python target's original make_problem() bug - there is
/// no possible collision with the `location` parameter.
class RuleCatalog {{
public:
    struct Entry {{
        std::string rule;
        std::string message_template;
        std::string severity;
    }};

    static std::unordered_map<std::string, Entry>& catalog() {{
        static std::unordered_map<std::string, Entry> instance;
        return instance;
    }}

    static Entry get(const std::string& rule_id) {{
        auto it = catalog().find(rule_id);
        if (it != catalog().end()) return it->second;
        return Entry{{"", "{{schema-message}}", "error"}};
    }}

    static std::string severity_of(const std::string& rule_id) {{
        return get(rule_id).severity;
    }}

    static std::string format_message(const std::string& rule_id, const std::string& location,
                                       const std::map<std::string, std::string>& placeholders) {{
        Entry e = get(rule_id);
        std::string out = e.message_template;
        replace_all(out, "{{location}}", location);
        for (const auto& kv : placeholders) {{
            replace_all(out, "{{" + kv.first + "}}", kv.second);
        }}
        return out;
    }}

    static ValidationProblem make_problem(const std::string& rule_id, const std::string& location,
                                           const std::map<std::string, std::string>& placeholders = {{}}) {{
        Entry e = get(rule_id);
        return ValidationProblem{{rule_id, e.severity, e.rule,
                                  format_message(rule_id, location, placeholders), location}};
    }}

private:
    static void replace_all(std::string& s, const std::string& from, const std::string& to) {{
        if (from.empty()) return;
        size_t pos = 0;
        while ((pos = s.find(from, pos)) != std::string::npos) {{
            s.replace(pos, from.length(), to);
            pos += to.length();
        }}
    }}
}};

/// Per-field leaf validation, via the real JSON Schema validator
/// (jsoncons's bundled jsonschema extension, per Design.md's Toolchain
/// mandate) - a tiny schema fragment is built from one already-resolved
/// field's own type, never a whole-document schema, since every combinator
/// has already been resolved away by the generator at compose time (see
/// generator/spec.py).
class LeafValidation {{
public:
    static constexpr const char* SID_PATTERN = "^[A-Za-z_][A-Za-z0-9_]*$";
    static constexpr const char* SIDREF_PATTERN = "^#.*$";

    static bool is_sid(const std::string& s) {{
        static const std::regex re(SID_PATTERN);
        return std::regex_match(s, re);
    }}

    static bool leaf_value_ok(const std::string& kind, const jsoncons::json& value,
                               std::optional<double> minimum = std::nullopt,
                               std::optional<double> exclusive_minimum = std::nullopt,
                               std::optional<std::string> pattern = std::nullopt) {{
        jsoncons::json schema = base_schema(kind);
        if (minimum) schema["minimum"] = *minimum;
        if (exclusive_minimum) schema["exclusiveMinimum"] = *exclusive_minimum;
        if (pattern && kind == "string") schema["pattern"] = *pattern;
        auto compiled = jsoncons::jsonschema::make_json_schema(schema);
        bool ok = true;
        auto reporter = [&](const jsoncons::jsonschema::validation_message&) -> jsoncons::jsonschema::walk_result {{
            ok = false;
            return jsoncons::jsonschema::walk_result::advance;
        }};
        compiled.validate(value, reporter);
        return ok;
    }}

private:
    static jsoncons::json base_schema(const std::string& kind) {{
        jsoncons::json n = jsoncons::json::object();
        if (kind == "string") {{
            n["type"] = "string";
        }} else if (kind == "integer") {{
            n["type"] = "integer";
        }} else if (kind == "number") {{
            n["type"] = "number";
        }} else if (kind == "boolean") {{
            n["type"] = "boolean";
        }} else if (kind == "SId") {{
            n["type"] = "string";
            n["pattern"] = SID_PATTERN;
        }} else if (kind == "SIdRef") {{
            n["type"] = "string";
            n["pattern"] = SIDREF_PATTERN;
        }} else if (kind == "StringOrRef") {{
            jsoncons::json any = jsoncons::json::array();
            jsoncons::json s = jsoncons::json::object();
            s["type"] = "string";
            any.push_back(s);
            n["anyOf"] = any;
        }} else if (kind == "NumberOrRef") {{
            jsoncons::json any = jsoncons::json::array();
            jsoncons::json num = jsoncons::json::object();
            num["type"] = "number";
            jsoncons::json ref = jsoncons::json::object();
            ref["type"] = "string";
            ref["pattern"] = SIDREF_PATTERN;
            any.push_back(num);
            any.push_back(ref);
            n["anyOf"] = any;
        }} else {{
            throw std::invalid_argument("unknown leaf kind: " + kind);
        }}
        return n;
    }}
}};

inline const std::regex& namespace_key_pattern() {{
    static const std::regex re("^([A-Za-z_][A-Za-z0-9_]*)@([A-Za-z_][A-Za-z0-9_]*)$");
    return re;
}}

inline bool is_reference(const std::string& value) {{
    return !value.empty() && value[0] == '#';
}}

class IdKeyedCollection;
class ListCollection;

/// Universal base: every generated element (mirrors TestBaseFields'
/// name/description) plus parent/document backpointers, generic namespace
/// attribute storage, and the shared validate() engine. See Design.md's
/// Classes section - parent/document are non-owning raw pointers, per
/// Design.md's stated C++ raw-pointer intent.
///
/// Storage members (values_, or_ref_is_ref_, ns_attrs_, load_problems_,
/// name_node_, description_node_) are public: they are written directly by
/// the free function load_fields() in Dispatch.hpp (there is no C++
/// equivalent of Python/Java's same-module/same-package access, and a
/// dozen individual friend declarations would be noisier than one comment
/// marking them internal-use).
class SedBase {{
public:
    virtual ~SedBase() = default;

    // -- per-concrete-class metadata, overridden by generated subclasses --
    virtual const std::vector<FieldSpec>& field_specs() const {{
        static const std::vector<FieldSpec> empty;
        return empty;
    }}
    virtual const std::set<std::string>& required_names() const {{
        static const std::set<std::string> empty;
        return empty;
    }}
    virtual std::optional<std::string> type_const() const {{ return std::nullopt; }}
    virtual std::optional<std::string> type_rule_id() const {{ return std::nullopt; }}
    virtual std::string own_catchall() const {{ return ""; }}
    virtual const std::map<std::string, std::vector<FieldSpec>>& namespace_fields() const {{
        static const std::map<std::string, std::vector<FieldSpec>> empty;
        return empty;
    }}
    virtual const std::map<std::string, std::string>& namespace_catchall() const {{
        static const std::map<std::string, std::string> empty;
        return empty;
    }}
    virtual const std::set<std::string>& known_namespace_prefixes() const {{
        static const std::set<std::string> empty;
        return empty;
    }}
    virtual std::optional<std::string> name_rule_id() const {{ return std::nullopt; }}
    virtual std::optional<std::string> desc_rule_id() const {{ return std::nullopt; }}
    virtual std::string base_catchall() const {{ return ""; }}
    virtual std::string class_name() const = 0;

    // -- backpointers --
    SedBase* get_parent() const {{ return parent_; }}
    SedBase* get_document() const {{ return document_; }}

    void attach(SedBase* parent, SedBase* document) {{
        parent_ = parent;
        document_ = document;
        for (SedBase* child : children()) child->attach(this, document);
    }}

    /// Every SedBase-derived child reachable from this element, for
    /// backpointer propagation and validate() recursion.
    virtual std::vector<SedBase*> children() {{ return {{}}; }}

    // -- universal name/description (TestBaseFields) --
    // Stored as the raw jsoncons::json (not a coerced std::string) so a
    // wrong-typed incoming value (e.g. a JSON number for `name`) is
    // preserved for the leaf-type check in validate_own() instead of
    // being silently stringified away.
    std::string get_name() const {{
        if (!name_node_) throw ApiError("name is not set");
        return name_node_->as<std::string>();
    }}
    bool is_set_name() const {{ return name_node_.has_value(); }}
    void set_name(const std::string& value) {{ name_node_ = jsoncons::json(value); }}
    void unset_name() {{ name_node_.reset(); }}

    std::string get_description() const {{
        if (!description_node_) throw ApiError("description is not set");
        return description_node_->as<std::string>();
    }}
    bool is_set_description() const {{ return description_node_.has_value(); }}
    void set_description(const std::string& value) {{ description_node_ = jsoncons::json(value); }}
    void unset_description() {{ description_node_.reset(); }}

    // -- generic namespace attribute store (Design.md's Namespaces section) --
    jsoncons::json get_namespace_attribute(const std::string& prefix, const std::string& key) const {{
        std::string k = prefix + "@" + key;
        auto it = ns_attrs_.find(k);
        if (it == ns_attrs_.end()) throw ApiError("namespace attribute " + k + " is not set");
        return it->second;
    }}
    void set_namespace_attribute(const std::string& prefix, const std::string& key, const jsoncons::json& value) {{
        ns_attrs_[prefix + "@" + key] = value;
    }}
    bool is_set_namespace_attribute(const std::string& prefix, const std::string& key) const {{
        return ns_attrs_.count(prefix + "@" + key) > 0;
    }}
    void unset_namespace_attribute(const std::string& prefix, const std::string& key) {{
        ns_attrs_.erase(prefix + "@" + key);
    }}

    // -- generic OrRef-shaped storage helpers, used by generated accessors --
    jsoncons::json get_or_ref_value_node(const std::string& name) const {{
        auto it = values_.find(name);
        if (it == values_.end()) throw ApiError(name + " is not set");
        auto rit = or_ref_is_ref_.find(name);
        if (rit != or_ref_is_ref_.end() && rit->second) {{
            throw ApiError(name + " holds a reference, not a literal value");
        }}
        return it->second;
    }}
    jsoncons::json get_or_ref_ref_node(const std::string& name) const {{
        auto it = values_.find(name);
        if (it == values_.end()) throw ApiError(name + " is not set");
        auto rit = or_ref_is_ref_.find(name);
        if (rit == or_ref_is_ref_.end() || !rit->second) {{
            throw ApiError(name + " holds a literal value, not a reference");
        }}
        return it->second;
    }}
    void set_or_ref_value_node(const std::string& name, const jsoncons::json& value) {{
        values_[name] = value;
        or_ref_is_ref_[name] = false;
    }}
    void set_or_ref_ref_node(const std::string& name, const std::string& ref) {{
        if (!is_reference(ref)) throw ApiError("'" + ref + "' is not a valid reference (must start with '#')");
        values_[name] = jsoncons::json(ref);
        or_ref_is_ref_[name] = true;
    }}
    bool is_or_ref_ref(const std::string& name) const {{
        auto it = values_.find(name);
        if (it == values_.end()) throw ApiError(name + " is not set");
        auto rit = or_ref_is_ref_.find(name);
        return rit != or_ref_is_ref_.end() && rit->second;
    }}

    // -- collection field access (overridden per generated concrete class,
    // mirroring the Python target's getattr(obj, '_' + pyname(name))) --
    virtual IdKeyedCollection& get_dict_collection(const std::string& field_name);
    virtual ListCollection& get_list_collection(const std::string& field_name);

    // -- validate() engine --------------------------------------------------
    std::vector<ValidationProblem> validate(const std::string& severity_at_least = "warning");

    struct ChildLoc {{
        SedBase* child;
        std::string location_prefix;
    }};

    /// [(child, "/jsonPointerSegment"), ...] - override per concrete class.
    /// Default: none.
    virtual std::vector<ChildLoc> children_with_locations() {{ return {{}}; }}

    virtual std::string own_id_for_message() const {{ return "?"; }}
    virtual jsoncons::json own_json_value() const = 0;

    virtual std::set<std::string> allowed_keys() const {{
        std::set<std::string> keys;
        for (const auto& f : field_specs()) keys.insert(f.name);
        for (const auto& kv : namespace_fields()) {{
            for (const auto& f : kv.second) keys.insert(f.name);
        }}
        return keys;
    }}

    jsoncons::json to_json_value() const {{ return own_json_value(); }}

    // -- internal storage (see class comment) --
    std::optional<jsoncons::json> name_node_;
    std::optional<jsoncons::json> description_node_;
    std::map<std::string, jsoncons::json> values_;
    std::map<std::string, bool> or_ref_is_ref_;
    std::map<std::string, jsoncons::json> ns_attrs_;
    std::vector<ValidationProblem> load_problems_;

protected:
    virtual std::vector<ValidationProblem> validate_own();

private:
    SedBase* parent_ = nullptr;
    SedBase* document_ = nullptr;
}};

inline std::vector<ValidationProblem> SedBase::validate_own() {{
    // Extra/unrecognized properties (including bad-registered-namespace
    // keys), bad dict-of-discriminated-union keys, and item-dispatch
    // problems are all detected once, at load time, by load_fields() (see
    // Dispatch.hpp) - see Design.md's Schema-Pass Errors section. This is
    // the only reliable point to see genuinely-unrecognized raw JSON keys,
    // since they are never stored anywhere in the object itself.
    std::vector<ValidationProblem> problems = load_problems_;
    jsoncons::json instance = own_json_value();

    if (type_const() && type_rule_id()) {{
        bool has_type = instance.contains("_type") && !instance["_type"].is_null();
        std::string actual = has_type ? instance["_type"].as<std::string>() : "";
        if (!has_type || actual != *type_const()) {{
            std::map<std::string, std::string> ph;
            ph["attr"] = "_type";
            ph["class"] = class_name();
            ph["id"] = own_id_for_message();
            ph["value"] = has_type ? actual : "null";
            ph["allowed"] = *type_const();
            problems.push_back(RuleCatalog::make_problem(*type_rule_id(), "/_type", ph));
        }}
    }}

    // universal name/description mixin (TestBaseFields/SEDBaseFields) -
    // not a per-class FieldSpec, so checked directly here against the
    // base mixin's own rule IDs (the same on every concrete class).
    if (name_node_ && !LeafValidation::leaf_value_ok("string", *name_node_)) {{
        std::string rid = name_rule_id() ? *name_rule_id() : base_catchall();
        std::map<std::string, std::string> ph;
        ph["attr"] = "name";
        ph["class"] = class_name();
        ph["id"] = own_id_for_message();
        ph["value"] = name_node_->is_string() ? name_node_->as<std::string>() : name_node_->to_string();
        problems.push_back(RuleCatalog::make_problem(rid, "/name", ph));
    }}
    if (description_node_ && !LeafValidation::leaf_value_ok("string", *description_node_)) {{
        std::string rid = desc_rule_id() ? *desc_rule_id() : base_catchall();
        std::map<std::string, std::string> ph;
        ph["attr"] = "description";
        ph["class"] = class_name();
        ph["id"] = own_id_for_message();
        ph["value"] = description_node_->is_string() ? description_node_->as<std::string>() : description_node_->to_string();
        problems.push_back(RuleCatalog::make_problem(rid, "/description", ph));
    }}

    static const std::set<std::string> leaf_kinds = {{
        "string", "integer", "number", "boolean", "SId", "SIdRef", "StringOrRef", "NumberOrRef"}};

    std::vector<FieldSpec> all(field_specs().begin(), field_specs().end());
    for (const auto& kv : namespace_fields()) {{
        for (const auto& f : kv.second) all.push_back(f);
    }}

    for (const auto& spec : all) {{
        bool present = instance.contains(spec.name);
        if (spec.required && !present) {{
            std::string rid = spec.required_rule_id ? *spec.required_rule_id : spec.origin_catchall;
            std::map<std::string, std::string> ph;
            ph["attr"] = spec.name;
            ph["class"] = class_name();
            ph["id"] = own_id_for_message();
            problems.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
            continue;
        }}
        if (!present) continue;
        const jsoncons::json& value = instance[spec.name];
        if (leaf_kinds.count(spec.kind)) {{
            if (!LeafValidation::leaf_value_ok(spec.kind, value, spec.minimum, spec.exclusive_minimum, spec.pattern)) {{
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = class_name();
                ph["id"] = own_id_for_message();
                ph["value"] = value.is_string() ? value.as<std::string>() : value.to_string();
                problems.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
            }}
        }}
    }}
    return problems;
}}

inline std::vector<ValidationProblem> SedBase::validate(const std::string& severity_at_least) {{
    std::vector<ValidationProblem> problems = validate_own();
    std::set<std::pair<std::string, std::string>> seen;
    for (const auto& p : problems) seen.insert({{p.rule_id, p.location}});
    for (const auto& cl : children_with_locations()) {{
        for (const auto& p : cl.child->validate("warning")) {{
            ValidationProblem p2{{p.rule_id, p.severity, p.rule, p.message, cl.location_prefix + p.location}};
            auto key = std::make_pair(p2.rule_id, p2.location);
            if (seen.count(key)) continue;
            seen.insert(key);
            problems.push_back(p2);
        }}
    }}
    int threshold = (severity_at_least == "warning") ? 0 : 1;
    std::vector<ValidationProblem> out;
    for (const auto& p : problems) {{
        int lvl = (p.severity == "warning") ? 0 : 1;
        if (lvl >= threshold) out.push_back(p);
    }}
    return out;
}}

/// Backing store for an ID-keyed dict-of-discriminated-union field
/// (TestDocument.widgets/.reports, FancyWidget.choices) - insertion order
/// preserved, add-/remove-/insert-/rename (set_id) per Design.md's Classes
/// section. Owns its items via unique_ptr; exposes only non-owning
/// SedBase* to callers.
class IdKeyedCollection {{
public:
    std::vector<std::string> ids() const {{ return order_; }}

    SedBase* get(const std::string& item_id) const {{
        auto it = items_.find(item_id);
        if (it == items_.end()) throw ApiError("no entry with id " + item_id);
        return it->second.get();
    }}

    void add(const std::string& item_id, std::unique_ptr<SedBase> obj) {{
        if (items_.count(item_id)) throw ApiError("an entry with id " + item_id + " already exists");
        order_.push_back(item_id);
        items_.emplace(item_id, std::move(obj));
    }}

    void insert(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) {{
        if (items_.count(item_id)) throw ApiError("an entry with id " + item_id + " already exists");
        if (index > order_.size()) throw ApiError("index out of range");
        order_.insert(order_.begin() + static_cast<long>(index), item_id);
        items_.emplace(item_id, std::move(obj));
    }}

    void remove(const std::string& item_id) {{
        auto it = items_.find(item_id);
        if (it == items_.end()) throw ApiError("no entry with id " + item_id);
        order_.erase(std::remove(order_.begin(), order_.end(), item_id), order_.end());
        items_.erase(it);
    }}

    void set_id(const std::string& old_id, const std::string& new_id) {{
        auto it = items_.find(old_id);
        if (it == items_.end()) throw ApiError("no entry with id " + old_id);
        if (items_.count(new_id) && new_id != old_id) {{
            throw ApiError("an entry with id " + new_id + " already exists");
        }}
        for (auto& id : order_) {{
            if (id == old_id) {{ id = new_id; break; }}
        }}
        auto node = items_.extract(it);
        node.key() = new_id;
        items_.insert(std::move(node));
    }}

    size_t size() const {{ return order_.size(); }}

private:
    std::vector<std::string> order_;
    std::map<std::string, std::unique_ptr<SedBase>> items_;
}};

/// Backing store for a plain (non-ID-keyed) array-of-embedded-object
/// field, e.g. WidgetOptions.notes: add- (append), remove- (by index),
/// insert- (at index). Owns its items via unique_ptr.
class ListCollection {{
public:
    std::vector<SedBase*> items() const {{
        std::vector<SedBase*> out;
        out.reserve(items_.size());
        for (const auto& p : items_) out.push_back(p.get());
        return out;
    }}

    void add(std::unique_ptr<SedBase> obj) {{ items_.push_back(std::move(obj)); }}

    void insert(size_t index, std::unique_ptr<SedBase> obj) {{
        if (index > items_.size()) throw ApiError("index out of range");
        items_.insert(items_.begin() + static_cast<long>(index), std::move(obj));
    }}

    void remove(size_t index) {{
        if (index >= items_.size()) throw ApiError("index out of range");
        items_.erase(items_.begin() + static_cast<long>(index));
    }}

    size_t size() const {{ return items_.size(); }}

private:
    std::vector<std::unique_ptr<SedBase>> items_;
}};

inline IdKeyedCollection& SedBase::get_dict_collection(const std::string& field_name) {{
    throw ApiError("no such dict field: " + field_name);
}}

inline ListCollection& SedBase::get_list_collection(const std::string& field_name) {{
    throw ApiError("no such list field: " + field_name);
}}

}}  // namespace {NS}
'''


def runtime_files(ns: str) -> dict:
    return {"Runtime.hpp": _runtime_hpp(ns)}


# ---------------------------------------------------------------------------
# Per-spec generated files: GeneratedModel.hpp, Dispatch.hpp, RulesData.hpp,
# Io.hpp.
# ---------------------------------------------------------------------------

def _field_spec_expr(f: Field) -> str:
    t = f.type
    return (
        f"FieldSpec{{{_cpp_lit(f.name)}, {_cpp_lit(t.kind)}, {str(f.required).lower()}, "
        f"{_cpp_opt_str(f.rule_id)}, {_cpp_opt_str(f.required_rule_id)}, {_cpp_lit(f.origin_class + '-0000')}, "
        f"{_cpp_opt_double(t.minimum)}, {_cpp_opt_double(t.exclusive_minimum)}, {_cpp_opt_str(t.pattern)}, "
        f"{_cpp_opt_str(t.item_class)}, {_cpp_opt_str(t.item_discriminator)}}}"
    )


def _cpp_leaf_type(kind: str) -> str:
    return {"string": "std::string", "SId": "std::string", "SIdRef": "std::string",
            "integer": "int64_t", "number": "double", "boolean": "bool"}[kind]


def _leaf_accessors_cpp(f: Field) -> str:
    ident = _cpp_ident(f.name)
    kind = f.type.kind
    name_lit = _cpp_lit(f.name)
    lines = []
    if kind in ("StringOrRef", "NumberOrRef"):
        if kind == "StringOrRef":
            java_t, get_expr, wrap = "std::string", '.as<std::string>()', "jsoncons::json(value)"
            param_t = "const std::string&"
        else:
            java_t, get_expr, wrap = "double", ".as<double>()", "jsoncons::json(value)"
            param_t = "double"
        lines.append(f"    {java_t} get_{ident}_value() const {{ return get_or_ref_value_node({name_lit}){get_expr}; }}")
        lines.append(f"    std::string get_{ident}_ref() const {{ return get_or_ref_ref_node({name_lit}).as<std::string>(); }}")
        lines.append(f"    void set_{ident}_value({param_t} value) {{ set_or_ref_value_node({name_lit}, {wrap}); }}")
        lines.append(f"    void set_{ident}_ref(const std::string& ref) {{ set_or_ref_ref_node({name_lit}, ref); }}")
        lines.append(f"    bool is_{ident}_ref() const {{ return is_or_ref_ref({name_lit}); }}")
        lines.append(f"    bool is_set_{ident}() const {{ return values_.count({name_lit}) > 0; }}")
        lines.append(f"    void unset_{ident}() {{ values_.erase({name_lit}); or_ref_is_ref_.erase({name_lit}); }}")
    else:
        cpp_t = _cpp_leaf_type(kind)
        param_t = "const std::string&" if cpp_t == "std::string" else cpp_t
        get_expr = f".as<{cpp_t}>()"
        lines.append(f"    {cpp_t} get_{ident}() const {{ auto it = values_.find({name_lit}); "
                      f"if (it == values_.end()) throw ApiError(std::string({name_lit}) + \" is not set\"); "
                      f"return it->second{get_expr}; }}")
        lines.append(f"    void set_{ident}({param_t} value) {{ values_[{name_lit}] = jsoncons::json(value); }}")
        lines.append(f"    bool is_set_{ident}() const {{ return values_.count({name_lit}) > 0; }}")
        lines.append(f"    void unset_{ident}() {{ values_.erase({name_lit}); }}")
    return "\n".join(lines) + "\n"


def _collection_accessors_cpp(f: Field) -> str:
    ident = _cpp_ident(f.name)
    name_lit = _cpp_lit(f.name)
    lines = []
    if f.type.kind == "dict":
        lines.append(f"    std::vector<std::string> get_{ident}() const {{ return {ident}_.ids(); }}")
        lines.append(f"    SedBase* get_{ident}_item(const std::string& item_id) const {{ return {ident}_.get(item_id); }}")
        lines.append(f"    void add_{ident}(const std::string& item_id, std::unique_ptr<SedBase> obj) {{ "
                      f"SedBase* raw = obj.get(); {ident}_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }}")
        lines.append(f"    void insert_{ident}(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) {{ "
                      f"SedBase* raw = obj.get(); {ident}_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }}")
        lines.append(f"    void remove_{ident}(const std::string& item_id) {{ {ident}_.remove(item_id); }}")
        lines.append(f"    void set_id_on_{ident}(const std::string& old_id, const std::string& new_id) {{ {ident}_.set_id(old_id, new_id); }}")
    else:
        lines.append(f"    std::vector<SedBase*> get_{ident}() const {{ return {ident}_.items(); }}")
        lines.append(f"    void add_{ident}(std::unique_ptr<SedBase> obj) {{ "
                      f"SedBase* raw = obj.get(); {ident}_.add(std::move(obj)); raw->attach(this, get_document()); }}")
        lines.append(f"    void insert_{ident}(size_t index, std::unique_ptr<SedBase> obj) {{ "
                      f"SedBase* raw = obj.get(); {ident}_.insert(index, std::move(obj)); raw->attach(this, get_document()); }}")
        lines.append(f"    void remove_{ident}(size_t index) {{ {ident}_.remove(index); }}")
    return "\n".join(lines) + "\n"


def _collection_field_decl_cpp(f: Field) -> str:
    ident = _cpp_ident(f.name)
    cls = "IdKeyedCollection" if f.type.kind == "dict" else "ListCollection"
    return f"    {cls} {ident}_;\n"


def emit_model_hpp(model: SpecModel) -> str:
    base = model.base_mixin
    base_fields = model.classes[base].fields if base in model.classes else []
    base_name_rule_id = next((f.rule_id for f in base_fields if f.name == "name"), None)
    base_desc_rule_id = next((f.rule_id for f in base_fields if f.name == "description"), None)
    base_catchall = model.classes[base].own_catchall if base in model.classes else ""

    out = [f'''// Generated concrete SED2 classes. GENERATED - do not
// hand-edit; regenerate from test-specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"

#include <memory>
#include <string>
#include <vector>

namespace {NS} {{

''']

    for name in model.generatable_classes():
        c = model.classes[name]
        own_fields = [f for f in c.fields if f.origin_class != base]
        collection_fields = [f for f in own_fields if f.type.kind in ("dict", "array")]
        leaf_fields = [f for f in own_fields if f.type.kind in
                       ("StringOrRef", "NumberOrRef", "string", "integer", "number", "boolean", "SId", "SIdRef")]
        dict_fields = [f for f in collection_fields if f.type.kind == "dict"]
        array_fields = [f for f in collection_fields if f.type.kind == "array"]
        has_ns = bool(c.namespace_updates)

        out.append(f"/// Generated from test-specsheets/{c.category}/{name}/.\n")
        out.append(f"class {name} : public SedBase {{\npublic:\n")

        field_specs = leaf_fields + collection_fields
        if field_specs:
            exprs = ",\n            ".join(_field_spec_expr(f) for f in field_specs)
            out.append(f"    const std::vector<FieldSpec>& field_specs() const override {{\n"
                        f"        static const std::vector<FieldSpec> specs = {{\n            {exprs}\n        }};\n"
                        f"        return specs;\n    }}\n")
        req_names = [f.name for f in own_fields if f.required]
        if req_names:
            names_lit = ", ".join(_cpp_lit(n) for n in req_names)
            out.append(f"    const std::set<std::string>& required_names() const override {{\n"
                        f"        static const std::set<std::string> names = {{{names_lit}}};\n        return names;\n    }}\n")

        out.append(f"    std::optional<std::string> type_const() const override {{ return {_cpp_opt_str(c.type_const)}; }}\n")
        out.append(f"    std::optional<std::string> type_rule_id() const override {{ return {_cpp_opt_str(c.type_rule_id)}; }}\n")
        out.append(f"    std::string own_catchall() const override {{ return {_cpp_lit(c.own_catchall)}; }}\n")
        out.append(f"    std::optional<std::string> name_rule_id() const override {{ return {_cpp_opt_str(base_name_rule_id)}; }}\n")
        out.append(f"    std::optional<std::string> desc_rule_id() const override {{ return {_cpp_opt_str(base_desc_rule_id)}; }}\n")
        out.append(f"    std::string base_catchall() const override {{ return {_cpp_lit(base_catchall)}; }}\n")
        out.append(f"    std::string class_name() const override {{ return {_cpp_lit(name)}; }}\n")
        if has_ns:
            ns_field_entries = []
            for prefix, fs in c.namespace_updates.items():
                exprs = ", ".join(_field_spec_expr(f) for f in fs)
                ns_field_entries.append(f"{{{_cpp_lit(prefix)}, {{{exprs}}}}}")
            out.append(f"    const std::map<std::string, std::vector<FieldSpec>>& namespace_fields() const override {{\n"
                        f"        static const std::map<std::string, std::vector<FieldSpec>> m = {{\n            "
                        + ",\n            ".join(ns_field_entries) + "\n        };\n        return m;\n    }\n")
            catchall_entries = ", ".join(f"{{{_cpp_lit(p)}, {_cpp_lit(cc)}}}" for p, cc in c.namespace_catchalls.items())
            out.append(f"    const std::map<std::string, std::string>& namespace_catchall() const override {{\n"
                        f"        static const std::map<std::string, std::string> m = {{{catchall_entries}}};\n"
                        f"        return m;\n    }}\n")
            known_prefixes = ", ".join(_cpp_lit(p) for p in c.namespace_updates)
            out.append(f"    const std::set<std::string>& known_namespace_prefixes() const override {{\n"
                        f"        static const std::set<std::string> s = {{{known_prefixes}}};\n"
                        f"        return s;\n    }}\n")
        if c.type_const is not None:
            out.append(f"    std::string get_type() const {{ return {_cpp_lit(c.type_const)}; }}\n")
        out.append("\n")

        for f in leaf_fields:
            out.append(_leaf_accessors_cpp(f) + "\n")
        for f in collection_fields:
            out.append(_collection_accessors_cpp(f) + "\n")
        for prefix, fs in c.namespace_updates.items():
            for f in fs:
                out.append(_leaf_accessors_cpp(f) + "\n")

        if collection_fields:
            out.append("    std::vector<SedBase*> children() override {\n        std::vector<SedBase*> kids;\n")
            for f in dict_fields:
                ident = _cpp_ident(f.name)
                out.append(f"        for (const auto& i : {ident}_.ids()) kids.push_back({ident}_.get(i));\n")
            for f in array_fields:
                ident = _cpp_ident(f.name)
                out.append(f"        for (auto* item : {ident}_.items()) kids.push_back(item);\n")
            out.append("        return kids;\n    }\n\n")

            out.append("    std::vector<ChildLoc> children_with_locations() override {\n        std::vector<ChildLoc> out;\n")
            for f in dict_fields:
                ident = _cpp_ident(f.name)
                out.append(f"        for (const auto& i : {ident}_.ids()) out.push_back(ChildLoc{{{ident}_.get(i), \"/{f.name}/\" + i}});\n")
            for f in array_fields:
                ident = _cpp_ident(f.name)
                out.append(f"        {{ size_t idx = 0; for (auto* item : {ident}_.items()) {{ "
                            f"out.push_back(ChildLoc{{item, \"/{f.name}/\" + std::to_string(idx)}}); idx++; }} }}\n")
            out.append("        return out;\n    }\n\n")

        if dict_fields:
            out.append("    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {\n")
            for f in dict_fields:
                ident = _cpp_ident(f.name)
                out.append(f"        if (field_name == {_cpp_lit(f.name)}) return {ident}_;\n")
            out.append("        return SedBase::get_dict_collection(field_name);\n    }\n\n")
        if array_fields:
            out.append("    ListCollection& get_list_collection(const std::string& field_name) override {\n")
            for f in array_fields:
                ident = _cpp_ident(f.name)
                out.append(f"        if (field_name == {_cpp_lit(f.name)}) return {ident}_;\n")
            out.append("        return SedBase::get_list_collection(field_name);\n    }\n\n")

        out.append("    jsoncons::json own_json_value() const override {\n        jsoncons::json d = jsoncons::json::object();\n")
        out.append("        if (name_node_) d[\"name\"] = *name_node_;\n")
        out.append("        if (description_node_) d[\"description\"] = *description_node_;\n")
        if c.type_const is not None:
            out.append(f"        d[\"_type\"] = values_.count(\"_type\") ? values_.at(\"_type\") : jsoncons::json({_cpp_lit(c.type_const)});\n")
        for f in leaf_fields:
            out.append(f"        if (values_.count({_cpp_lit(f.name)})) d[{_cpp_lit(f.name)}] = values_.at({_cpp_lit(f.name)});\n")
        for prefix, fs in c.namespace_updates.items():
            for f in fs:
                out.append(f"        if (values_.count({_cpp_lit(f.name)})) d[{_cpp_lit(f.name)}] = values_.at({_cpp_lit(f.name)});\n")
        for f in dict_fields:
            ident = _cpp_ident(f.name)
            out.append(f"        if ({ident}_.size() > 0) {{ jsoncons::json sub = jsoncons::json::object(); "
                        f"for (const auto& i : {ident}_.ids()) sub[i] = {ident}_.get(i)->to_json_value(); d[{_cpp_lit(f.name)}] = sub; }}\n")
        for f in array_fields:
            ident = _cpp_ident(f.name)
            out.append(f"        if ({ident}_.size() > 0) {{ jsoncons::json arr = jsoncons::json::array(); "
                        f"for (auto* item : {ident}_.items()) arr.push_back(item->to_json_value()); d[{_cpp_lit(f.name)}] = arr; }}\n")
        out.append("        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;\n")
        out.append("        return d;\n    }\n")

        if collection_fields:
            out.append("\nprivate:\n")
            for f in collection_fields:
                out.append(_collection_field_decl_cpp(f))

        out.append("};\n\n")

    for disc_name, disc in model.discriminators.items():
        uname = disc.unknown_class_name
        out.append(f'''/// Opaque holder for a {disc_name} instance whose _type names an
/// unregistered namespace prefix (see Design.md's Namespaces section) -
/// round-trips unchanged, never itself a validation error.
class {uname} : public SedBase {{
public:
    {uname}(std::string type_value, jsoncons::json raw)
        : type_value_(std::move(type_value)), raw_(std::move(raw)) {{}}

    std::string get_type() const {{ return type_value_; }}
    std::string class_name() const override {{ return {_cpp_lit(uname)}; }}

    jsoncons::json own_json_value() const override {{
        jsoncons::json d = raw_;
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        return d;
    }}

    std::set<std::string> allowed_keys() const override {{
        std::set<std::string> keys;
        for (const auto& kv : raw_.object_range()) keys.insert(kv.key());
        return keys;
    }}

protected:
    std::vector<ValidationProblem> validate_own() override {{ return {{}}; }}

private:
    std::string type_value_;
    jsoncons::json raw_;
}};

''')

    out.append(f"}}  // namespace {NS}\n")
    return "".join(out)


def emit_dispatch_hpp(model: SpecModel) -> str:
    out = [f'''// Generated dispatch/parse per discriminator, plus the generic field
// loader used by every parse_* function and by Io::read_from_string().
// All load-time violations (extra/unrecognized properties, bad
// dict-of-discriminated-union keys, bad container shapes, and dispatch
// problems bubbled up from a nested item) are appended straight onto
// obj->load_problems_ - this is the only point that sees the raw JSON
// before an unrecognized key is dropped, so it is the only reliable place
// to detect them (see Design.md's Schema-Pass Errors section - mirrors
// generator/emit_python.py's _load_fields()). GENERATED - do not
// hand-edit; regenerate from test-specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"
#include "GeneratedModel.hpp"

#include <memory>
#include <optional>
#include <regex>
#include <set>
#include <string>

namespace {NS} {{

struct DispatchResult {{
    std::unique_ptr<SedBase> value;
    std::optional<ValidationProblem> problem;
}};

inline void load_fields(SedBase* obj, const jsoncons::json& raw);

''']

    for disc_name, disc in model.discriminators.items():
        uname = disc.unknown_class_name
        out.append(f"inline DispatchResult parse_{disc_name}(const jsoncons::json& raw) {{\n")
        out.append("    if (!raw.contains(\"_type\")) {\n")
        if disc.missing_type_rule_id:
            out.append(f"        return DispatchResult{{nullptr, RuleCatalog::make_problem({_cpp_lit(disc.missing_type_rule_id)}, \"\")}};\n")
        else:
            out.append("        std::map<std::string, std::string> ph0;\n")
            out.append("        ph0[\"schema-message\"] = \"missing _type\";\n")
            out.append(f"        return DispatchResult{{nullptr, RuleCatalog::make_problem({_cpp_lit(disc_name + '-0000')}, \"\", ph0)}};\n")
        out.append("    }\n")
        out.append("    std::string tv = raw.at(\"_type\").as<std::string>();\n")
        out.append("    std::unique_ptr<SedBase> obj;\n")
        for i, (tc, br) in enumerate(disc.branches.items()):
            kw = "if" if i == 0 else "else if"
            out.append(f"    {kw} (tv == {_cpp_lit(tc)}) obj = std::make_unique<{br.class_name}>();\n")
        out.append("    if (obj) {\n")
        out.append("        load_fields(obj.get(), raw);\n")
        out.append("        return DispatchResult{std::move(obj), std::nullopt};\n")
        out.append("    }\n")
        out.append("    std::smatch m;\n")
        out.append("    bool ns_match = std::regex_match(tv, m, namespace_key_pattern());\n")
        known = ", ".join(_cpp_lit(b.namespace) for b in disc.branches.values() if b.namespace)
        out.append(f"    static const std::set<std::string> known = {{{known}}};\n")
        out.append("    if (ns_match && !known.count(m[1].str())) {\n")
        out.append(f"        return DispatchResult{{std::make_unique<{uname}>(tv, raw), std::nullopt}};\n")
        out.append("    }\n")
        out.append("    std::map<std::string, std::string> ph;\n")
        out.append("    ph[\"schema-message\"] = \"unrecognized _type '\" + tv + \"'\";\n")
        out.append(f"    return DispatchResult{{std::make_unique<{uname}>(tv, raw), "
                    f"RuleCatalog::make_problem({_cpp_lit(disc_name + '-0000')}, \"\", ph)}};\n")
        out.append("}\n\n")

    out.append("inline DispatchResult dispatch_parse(const std::string& disc_name, const jsoncons::json& raw) {\n")
    for i, disc_name in enumerate(model.discriminators):
        kw = "if" if i == 0 else "else if"
        out.append(f"    {kw} (disc_name == {_cpp_lit(disc_name)}) return parse_{disc_name}(raw);\n")
    out.append("    throw ApiError(\"unknown discriminator \" + disc_name);\n}\n\n")

    item_classes = sorted({f.type.item_class for c in model.classes.values() for f in c.fields
                            if f.type.kind == "array" and f.type.item_class})
    out.append("inline std::unique_ptr<SedBase> new_item_instance(const std::string& class_name) {\n")
    for i, cls_name in enumerate(item_classes):
        kw = "if" if i == 0 else "else if"
        out.append(f"    {kw} (class_name == {_cpp_lit(cls_name)}) return std::make_unique<{cls_name}>();\n")
    out.append("    throw ApiError(\"unknown item class \" + class_name);\n}\n\n")

    out.append('''inline void load_fields(SedBase* obj, const jsoncons::json& raw) {
    if (raw.contains("name") && !raw.at("name").is_null()) obj->name_node_ = raw.at("name");
    if (raw.contains("description") && !raw.at("description").is_null()) obj->description_node_ = raw.at("description");
    if (raw.contains("_type")) obj->values_["_type"] = raw.at("_type");

    for (const auto& spec : obj->field_specs()) {
        if (!raw.contains(spec.name) || spec.kind == "dict" || spec.kind == "array") continue;
        const jsoncons::json& v = raw.at(spec.name);
        if (spec.kind == "StringOrRef" || spec.kind == "NumberOrRef") {
            if (v.is_string() && is_reference(v.as<std::string>())) {
                obj->set_or_ref_ref_node(spec.name, v.as<std::string>());
            } else {
                obj->set_or_ref_value_node(spec.name, v);
            }
        } else {
            obj->values_[spec.name] = v;
        }
    }
    for (const auto& kv : obj->namespace_fields()) {
        for (const auto& spec : kv.second) {
            if (raw.contains(spec.name)) obj->values_[spec.name] = raw.at(spec.name);
        }
    }

    std::set<std::string> allowed = obj->allowed_keys();
    for (const auto& kv : raw.object_range()) {
        const std::string& key = kv.key();
        if (key == "_type" || key == "name" || key == "description") continue;
        if (allowed.count(key)) continue;
        std::smatch m;
        if (std::regex_match(key, m, namespace_key_pattern())) {
            std::string prefix = m[1].str(), ns_key = m[2].str();
            obj->set_namespace_attribute(prefix, ns_key, kv.value());
            if (obj->known_namespace_prefixes().count(prefix)) {
                std::string catchall = obj->namespace_catchall().count(prefix)
                        ? obj->namespace_catchall().at(prefix) : obj->own_catchall();
                std::map<std::string, std::string> ph;
                ph["schema-message"] = "Additional property '" + key + "' is not allowed.";
                obj->load_problems_.push_back(RuleCatalog::make_problem(catchall, "", ph));
            }
            continue;
        }
        std::map<std::string, std::string> ph;
        ph["schema-message"] = "Additional property '" + key + "' is not allowed.";
        obj->load_problems_.push_back(RuleCatalog::make_problem(obj->own_catchall(), "", ph));
    }

    for (const auto& spec : obj->field_specs()) {
        if (spec.kind == "dict" && raw.contains(spec.name)) {
            const jsoncons::json& raw_value = raw.at(spec.name);
            if (!raw_value.is_object()) {
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = obj->class_name();
                ph["id"] = obj->own_id_for_message();
                ph["value"] = raw_value.to_string();
                obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                continue;
            }
            IdKeyedCollection& coll = obj->get_dict_collection(spec.name);
            for (const auto& item_kv : raw_value.object_range()) {
                const std::string& item_id = item_kv.key();
                const jsoncons::json& item_raw = item_kv.value();
                if (!LeafValidation::is_sid(item_id)) {
                    std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                    std::map<std::string, std::string> ph;
                    ph["attr"] = spec.name;
                    ph["class"] = obj->class_name();
                    ph["id"] = obj->own_id_for_message();
                    ph["value"] = item_id;
                    obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                }
                DispatchResult r = dispatch_parse(*spec.item_discriminator, item_raw);
                if (r.problem) obj->load_problems_.push_back(*r.problem);
                if (r.value) coll.add(item_id, std::move(r.value));
            }
        } else if (spec.kind == "array" && raw.contains(spec.name)) {
            const jsoncons::json& raw_value = raw.at(spec.name);
            if (!raw_value.is_array()) {
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = obj->class_name();
                ph["id"] = obj->own_id_for_message();
                ph["value"] = raw_value.to_string();
                obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                continue;
            }
            ListCollection& coll = obj->get_list_collection(spec.name);
            for (const auto& item_raw : raw_value.array_range()) {
                std::unique_ptr<SedBase> child = new_item_instance(*spec.item_class);
                load_fields(child.get(), item_raw);
                coll.add(std::move(child));
            }
        }
    }
}

''')
    out.append(f"}}  // namespace {NS}\n")
    return "".join(out)


def emit_direct_only_hpp(model: SpecModel) -> str:
    """rule_id -> factory, for every generated class whose own _type-const
    rule can only be exercised by validating that class directly - not
    embedded through a parent's discriminated dict/array field, where a
    _type mismatch is caught by the parent's own dispatch first (see
    Design.md's Testing section). C++ has no runtime reflection (unlike
    Python's inspect.getmembers() or Java's classloader-based scan - see
    templates/python/tests/test_fixtures.py and templates/java/tests/
    FixtureTest.java), so this table is built here, at generate time, from
    the same per-class type_rule_id() metadata those two discover at their
    own run time - every class in model.generatable_classes() with a
    non-empty type_rule_id, which is exactly the set with a default
    constructor available (the only other classes, the discriminator
    Unknown* holders, take constructor arguments and have no type_rule_id
    to begin with - see emit_dispatch_hpp's Unknown* handling). This keeps
    templates/cpp/tests/FixtureTest.cpp itself free of any spec-specific
    class or rule-ID knowledge, the same as the other two targets.
    GENERATED - do not hand-edit; regenerate via generator/generate.py."""
    out = [f'''// Generated direct-only-class registry (see this file's own generator,
// generator/emit_cpp.py's emit_direct_only_hpp, for what this is and why
// it exists). GENERATED - do not hand-edit; regenerate via
// generator/generate.py.
#pragma once

#include "GeneratedModel.hpp"

#include <functional>
#include <map>
#include <memory>
#include <string>

namespace {NS} {{

inline const std::map<std::string, std::function<std::unique_ptr<SedBase>()>>& direct_only_classes() {{
    static const std::map<std::string, std::function<std::unique_ptr<SedBase>()>> m = {{
''']
    for name in model.generatable_classes():
        rid = model.classes[name].type_rule_id
        if rid:
            out.append(f"        {{{_cpp_lit(rid)}, [] {{ return std::unique_ptr<SedBase>(std::make_unique<{name}>()); }}}},\n")
    out.append("    };\n    return m;\n}\n\n")
    out.append(f"}}  // namespace {NS}\n")
    return "".join(out)


def emit_rules_data_hpp(model: SpecModel) -> str:
    out = [f'''// Generated rule catalogue. GENERATED - do not hand-edit;
// regenerate from test-specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"

namespace {NS} {{

inline void register_rules() {{
    static bool done = false;
    if (done) return;
    done = true;
''']
    for rid, r in sorted(model.rules.items()):
        out.append(f"    RuleCatalog::catalog()[{_cpp_lit(rid)}] = "
                    f"RuleCatalog::Entry{{{_cpp_lit(r.rule)}, {_cpp_lit(r.message)}, {_cpp_lit(r.severity)}}};\n")
    out.append("}\n\n")
    out.append(f"}}  // namespace {NS}\n")
    return "".join(out)


def emit_io_hpp(model: SpecModel) -> str:
    doc_name = model.document_class
    return f'''// Top-level read/write entry points. GENERATED - do not
// hand-edit; regenerate from test-specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"
#include "GeneratedModel.hpp"
#include "Dispatch.hpp"
#include "RulesData.hpp"

#include <fstream>
#include <memory>
#include <sstream>
#include <string>

namespace {NS} {{

inline std::unique_ptr<{doc_name}> read_from_string(const std::string& text) {{
    register_rules();
    jsoncons::json raw = jsoncons::json::parse(text);
    auto obj = std::make_unique<{doc_name}>();
    load_fields(obj.get(), raw);
    obj->attach(nullptr, obj.get());
    return obj;
}}

inline std::unique_ptr<{doc_name}> read_from_file(const std::string& path) {{
    std::ifstream f(path);
    std::stringstream ss;
    ss << f.rdbuf();
    return read_from_string(ss.str());
}}

inline std::string write_to_string(const {doc_name}& doc) {{
    jsoncons::json v = doc.to_json_value();
    std::string out;
    v.dump(out, jsoncons::indenting::indent);
    return out;
}}

inline void write_to_file(const {doc_name}& doc, const std::string& path) {{
    std::ofstream f(path);
    f << write_to_string(doc);
}}

}}  // namespace {NS}
'''


def _repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _copy_fixture_test_cpp(out_dir: str, ns: str) -> None:
    """Copies templates/cpp/tests/FixtureTest.cpp -> <out_dir>/tests/
    FixtureTest.cpp, rewriting its #include lines and using-namespace
    declaration to match ns. Every other reference in that file resolves
    generically (auto-deduced document type, or the generated
    direct_only_classes() registry - see the file's own top-of-file
    comment), so these lines are the one place this copy step needs to
    touch content rather than copying verbatim - the preprocessor and
    `using namespace` both need a literal name, unlike Python (no
    equivalent concept) or Java (same-package visibility handles it - see
    emit_java.py's _copy_fixture_test_java)."""
    src = os.path.join(_repo_root(), "templates", "cpp", "tests", "FixtureTest.cpp")
    with open(src) as f:
        content = f.read()
    for old in (
        "#include <sed2test/DirectOnly.hpp>",
        "#include <sed2test/Io.hpp>",
        "using namespace sed2test;",
    ):
        assert old in content, f"templates/cpp/tests/FixtureTest.cpp must contain {old!r}"
    content = content.replace("sed2test/DirectOnly.hpp", f"{ns}/DirectOnly.hpp")
    content = content.replace("sed2test/Io.hpp", f"{ns}/Io.hpp")
    content = content.replace("using namespace sed2test;", f"using namespace {ns};")
    tests_dir = os.path.join(out_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, "FixtureTest.cpp"), "w") as f:
        f.write(content)


def _cmake_lists(name: str) -> str:
    build_tests_opt = f"{name.upper()}_BUILD_TESTS"
    return f'''cmake_minimum_required(VERSION 3.16)
project({name} CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)

set(JSONCONS_BUILD_TESTS OFF CACHE BOOL "" FORCE)
FetchContent_Declare(
  jsoncons
  GIT_REPOSITORY https://github.com/danielaparker/jsoncons.git
  GIT_TAG v0.176.0
)
FetchContent_MakeAvailable(jsoncons)

# {name} is header-only (see generator/emit_cpp.py's module docstring),
# so it is exposed as an INTERFACE library: nothing to compile here, only
# include paths and its jsoncons dependency to propagate to consumers.
add_library({name} INTERFACE)
target_include_directories({name} INTERFACE ${{CMAKE_CURRENT_SOURCE_DIR}}/include)
target_link_libraries({name} INTERFACE jsoncons)

option({build_tests_opt} "Build the fixture test suite" ON)
if({build_tests_opt})
  set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
  set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
  FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.15.2
  )
  FetchContent_MakeAvailable(googletest)

  enable_testing()
  add_executable(fixture_tests tests/FixtureTest.cpp)
  target_link_libraries(fixture_tests PRIVATE {name} GTest::gtest_main)
  # fixtures/ always lives two levels up from this file's own directory
  # (see generate.py: fixtures/ is written under dirname(--out), and cpp
  # sources under --out/cpp) - baked in here, at configure time, rather
  # than guessed at run time from the test binary's working directory
  # (which gtest_discover_tests/ctest don't guarantee the same way across
  # generators). See templates/cpp/tests/FixtureTest.cpp's fixtures_dir().
  target_compile_definitions(fixture_tests PRIVATE
    SED2_FIXTURES_DIR_DEFAULT="${{CMAKE_CURRENT_SOURCE_DIR}}/../../fixtures")
  include(GoogleTest)
  gtest_discover_tests(fixture_tests)
endif()
'''


def emit_cpp_package(model: SpecModel, out_dir: str, cpp_namespace: str = "sed2test") -> None:
    global NS
    NS = cpp_namespace

    inc_dir = os.path.join(out_dir, "include", NS)
    os.makedirs(inc_dir, exist_ok=True)

    for fname, content in runtime_files(NS).items():
        with open(os.path.join(inc_dir, fname), "w") as f:
            f.write(content)
    with open(os.path.join(inc_dir, "GeneratedModel.hpp"), "w") as f:
        f.write(emit_model_hpp(model))
    with open(os.path.join(inc_dir, "Dispatch.hpp"), "w") as f:
        f.write(emit_dispatch_hpp(model))
    with open(os.path.join(inc_dir, "DirectOnly.hpp"), "w") as f:
        f.write(emit_direct_only_hpp(model))
    with open(os.path.join(inc_dir, "RulesData.hpp"), "w") as f:
        f.write(emit_rules_data_hpp(model))
    with open(os.path.join(inc_dir, "Io.hpp"), "w") as f:
        f.write(emit_io_hpp(model))

    with open(os.path.join(out_dir, "CMakeLists.txt"), "w") as f:
        f.write(_cmake_lists(NS))

    _copy_fixture_test_cpp(out_dir, NS)

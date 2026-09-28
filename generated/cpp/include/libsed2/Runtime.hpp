// Shared runtime. GENERATED - do not
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

namespace libsed2 {

/// Raised for any misuse of the generated API itself (wrong-kind OrRef
/// access, get on an unset field, an out-of-range insert, ...) - never for
/// a document that merely fails a SED2 validation rule. See Design.md's
/// Classes section.
class ApiError : public std::runtime_error {
public:
    explicit ApiError(const std::string& message) : std::runtime_error(message) {}
};

struct ValidationProblem {
    std::string rule_id;
    std::string severity;
    std::string rule;
    std::string message;
    std::string location;

    bool operator==(const ValidationProblem& other) const {
        return rule_id == other.rule_id && location == other.location;
    }
};

inline std::ostream& operator<<(std::ostream& os, const ValidationProblem& p) {
    os << "ValidationProblem(" << p.rule_id << ", " << p.severity << ", " << p.location << ")";
    return os;
}

/// Plain aggregate - deliberately no user-declared constructors, so it can
/// be brace-initialized positionally by generated code (see
/// generator/emit_cpp.py's _field_spec_expr()).
struct FieldSpec {
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
};

/// Rule catalogue + ValidationProblem factory. Populated by
/// RulesData::register_rules() - see Io::read_from_string(), which calls
/// it once. Placeholders are an explicit map (not variadic/kwargs-style),
/// so - unlike the Python target's original make_problem() bug - there is
/// no possible collision with the `location` parameter.
class RuleCatalog {
public:
    struct Entry {
        std::string rule;
        std::string message_template;
        std::string severity;
    };

    static std::unordered_map<std::string, Entry>& catalog() {
        static std::unordered_map<std::string, Entry> instance;
        return instance;
    }

    static Entry get(const std::string& rule_id) {
        auto it = catalog().find(rule_id);
        if (it != catalog().end()) return it->second;
        return Entry{"", "{schema-message}", "error"};
    }

    static std::string severity_of(const std::string& rule_id) {
        return get(rule_id).severity;
    }

    static std::string format_message(const std::string& rule_id, const std::string& location,
                                       const std::map<std::string, std::string>& placeholders) {
        Entry e = get(rule_id);
        std::string out = e.message_template;
        replace_all(out, "{location}", location);
        for (const auto& kv : placeholders) {
            replace_all(out, "{" + kv.first + "}", kv.second);
        }
        return out;
    }

    static ValidationProblem make_problem(const std::string& rule_id, const std::string& location,
                                           const std::map<std::string, std::string>& placeholders = {}) {
        Entry e = get(rule_id);
        return ValidationProblem{rule_id, e.severity, e.rule,
                                  format_message(rule_id, location, placeholders), location};
    }

private:
    static void replace_all(std::string& s, const std::string& from, const std::string& to) {
        if (from.empty()) return;
        size_t pos = 0;
        while ((pos = s.find(from, pos)) != std::string::npos) {
            s.replace(pos, from.length(), to);
            pos += to.length();
        }
    }
};

/// Per-field leaf validation, via the real JSON Schema validator
/// (jsoncons's bundled jsonschema extension, per Design.md's Toolchain
/// mandate) - a tiny schema fragment is built from one already-resolved
/// field's own type, never a whole-document schema, since every combinator
/// has already been resolved away by the generator at compose time (see
/// generator/spec.py).
class LeafValidation {
public:
    static constexpr const char* SID_PATTERN = "^[A-Za-z_][A-Za-z0-9_]*$";
    static constexpr const char* SIDREF_PATTERN = "^#.*$";

    static bool is_sid(const std::string& s) {
        static const std::regex re(SID_PATTERN);
        return std::regex_match(s, re);
    }

    static bool leaf_value_ok(const std::string& kind, const jsoncons::json& value,
                               std::optional<double> minimum = std::nullopt,
                               std::optional<double> exclusive_minimum = std::nullopt,
                               std::optional<std::string> pattern = std::nullopt) {
        jsoncons::json schema = base_schema(kind);
        if (minimum) schema["minimum"] = *minimum;
        if (exclusive_minimum) schema["exclusiveMinimum"] = *exclusive_minimum;
        if (pattern && kind == "string") schema["pattern"] = *pattern;
        auto compiled = jsoncons::jsonschema::make_json_schema(schema);
        bool ok = true;
        auto reporter = [&](const jsoncons::jsonschema::validation_message&) -> jsoncons::jsonschema::walk_result {
            ok = false;
            return jsoncons::jsonschema::walk_result::advance;
        };
        compiled.validate(value, reporter);
        return ok;
    }

private:
    static jsoncons::json base_schema(const std::string& kind) {
        jsoncons::json n = jsoncons::json::object();
        if (kind == "string") {
            n["type"] = "string";
        } else if (kind == "integer") {
            n["type"] = "integer";
        } else if (kind == "number") {
            n["type"] = "number";
        } else if (kind == "boolean") {
            n["type"] = "boolean";
        } else if (kind == "SId") {
            n["type"] = "string";
            n["pattern"] = SID_PATTERN;
        } else if (kind == "SIdRef") {
            n["type"] = "string";
            n["pattern"] = SIDREF_PATTERN;
        } else if (kind == "StringOrRef") {
            jsoncons::json any = jsoncons::json::array();
            jsoncons::json s = jsoncons::json::object();
            s["type"] = "string";
            any.push_back(s);
            n["anyOf"] = any;
        } else if (kind == "NumberOrRef") {
            jsoncons::json any = jsoncons::json::array();
            jsoncons::json num = jsoncons::json::object();
            num["type"] = "number";
            jsoncons::json ref = jsoncons::json::object();
            ref["type"] = "string";
            ref["pattern"] = SIDREF_PATTERN;
            any.push_back(num);
            any.push_back(ref);
            n["anyOf"] = any;
        } else {
            throw std::invalid_argument("unknown leaf kind: " + kind);
        }
        return n;
    }
};

inline const std::regex& namespace_key_pattern() {
    static const std::regex re("^([A-Za-z_][A-Za-z0-9_]*)@([A-Za-z_][A-Za-z0-9_]*)$");
    return re;
}

inline bool is_reference(const std::string& value) {
    return !value.empty() && value[0] == '#';
}

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
class SedBase {
public:
    virtual ~SedBase() = default;

    // -- per-concrete-class metadata, overridden by generated subclasses --
    virtual const std::vector<FieldSpec>& field_specs() const {
        static const std::vector<FieldSpec> empty;
        return empty;
    }
    virtual const std::set<std::string>& required_names() const {
        static const std::set<std::string> empty;
        return empty;
    }
    virtual std::optional<std::string> type_const() const { return std::nullopt; }
    virtual std::optional<std::string> type_rule_id() const { return std::nullopt; }
    virtual std::string own_catchall() const { return ""; }
    virtual const std::map<std::string, std::vector<FieldSpec>>& namespace_fields() const {
        static const std::map<std::string, std::vector<FieldSpec>> empty;
        return empty;
    }
    virtual const std::map<std::string, std::string>& namespace_catchall() const {
        static const std::map<std::string, std::string> empty;
        return empty;
    }
    virtual const std::set<std::string>& known_namespace_prefixes() const {
        static const std::set<std::string> empty;
        return empty;
    }
    virtual std::optional<std::string> name_rule_id() const { return std::nullopt; }
    virtual std::optional<std::string> desc_rule_id() const { return std::nullopt; }
    virtual std::string base_catchall() const { return ""; }
    virtual std::string class_name() const = 0;

    // -- backpointers --
    SedBase* get_parent() const { return parent_; }
    SedBase* get_document() const { return document_; }

    void attach(SedBase* parent, SedBase* document) {
        parent_ = parent;
        document_ = document;
        for (SedBase* child : children()) child->attach(this, document);
    }

    /// Every SedBase-derived child reachable from this element, for
    /// backpointer propagation and validate() recursion.
    virtual std::vector<SedBase*> children() { return {}; }

    // -- universal name/description (TestBaseFields) --
    // Stored as the raw jsoncons::json (not a coerced std::string) so a
    // wrong-typed incoming value (e.g. a JSON number for `name`) is
    // preserved for the leaf-type check in validate_own() instead of
    // being silently stringified away.
    std::string get_name() const {
        if (!name_node_) throw ApiError("name is not set");
        return name_node_->as<std::string>();
    }
    bool is_set_name() const { return name_node_.has_value(); }
    void set_name(const std::string& value) { name_node_ = jsoncons::json(value); }
    void unset_name() { name_node_.reset(); }

    std::string get_description() const {
        if (!description_node_) throw ApiError("description is not set");
        return description_node_->as<std::string>();
    }
    bool is_set_description() const { return description_node_.has_value(); }
    void set_description(const std::string& value) { description_node_ = jsoncons::json(value); }
    void unset_description() { description_node_.reset(); }

    // -- generic namespace attribute store (Design.md's Namespaces section) --
    jsoncons::json get_namespace_attribute(const std::string& prefix, const std::string& key) const {
        std::string k = prefix + "@" + key;
        auto it = ns_attrs_.find(k);
        if (it == ns_attrs_.end()) throw ApiError("namespace attribute " + k + " is not set");
        return it->second;
    }
    void set_namespace_attribute(const std::string& prefix, const std::string& key, const jsoncons::json& value) {
        ns_attrs_[prefix + "@" + key] = value;
    }
    bool is_set_namespace_attribute(const std::string& prefix, const std::string& key) const {
        return ns_attrs_.count(prefix + "@" + key) > 0;
    }
    void unset_namespace_attribute(const std::string& prefix, const std::string& key) {
        ns_attrs_.erase(prefix + "@" + key);
    }

    // -- generic OrRef-shaped storage helpers, used by generated accessors --
    jsoncons::json get_or_ref_value_node(const std::string& name) const {
        auto it = values_.find(name);
        if (it == values_.end()) throw ApiError(name + " is not set");
        auto rit = or_ref_is_ref_.find(name);
        if (rit != or_ref_is_ref_.end() && rit->second) {
            throw ApiError(name + " holds a reference, not a literal value");
        }
        return it->second;
    }
    jsoncons::json get_or_ref_ref_node(const std::string& name) const {
        auto it = values_.find(name);
        if (it == values_.end()) throw ApiError(name + " is not set");
        auto rit = or_ref_is_ref_.find(name);
        if (rit == or_ref_is_ref_.end() || !rit->second) {
            throw ApiError(name + " holds a literal value, not a reference");
        }
        return it->second;
    }
    void set_or_ref_value_node(const std::string& name, const jsoncons::json& value) {
        values_[name] = value;
        or_ref_is_ref_[name] = false;
    }
    void set_or_ref_ref_node(const std::string& name, const std::string& ref) {
        if (!is_reference(ref)) throw ApiError("'" + ref + "' is not a valid reference (must start with '#')");
        values_[name] = jsoncons::json(ref);
        or_ref_is_ref_[name] = true;
    }
    bool is_or_ref_ref(const std::string& name) const {
        auto it = values_.find(name);
        if (it == values_.end()) throw ApiError(name + " is not set");
        auto rit = or_ref_is_ref_.find(name);
        return rit != or_ref_is_ref_.end() && rit->second;
    }

    // -- collection field access (overridden per generated concrete class,
    // mirroring the Python target's getattr(obj, '_' + pyname(name))) --
    virtual IdKeyedCollection& get_dict_collection(const std::string& field_name);
    virtual ListCollection& get_list_collection(const std::string& field_name);

    // -- validate() engine --------------------------------------------------
    std::vector<ValidationProblem> validate(const std::string& severity_at_least = "warning");

    struct ChildLoc {
        SedBase* child;
        std::string location_prefix;
    };

    /// [(child, "/jsonPointerSegment"), ...] - override per concrete class.
    /// Default: none.
    virtual std::vector<ChildLoc> children_with_locations() { return {}; }

    virtual std::string own_id_for_message() const { return "?"; }
    virtual jsoncons::json own_json_value() const = 0;

    virtual std::set<std::string> allowed_keys() const {
        std::set<std::string> keys;
        for (const auto& f : field_specs()) keys.insert(f.name);
        for (const auto& kv : namespace_fields()) {
            for (const auto& f : kv.second) keys.insert(f.name);
        }
        return keys;
    }

    jsoncons::json to_json_value() const { return own_json_value(); }

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
};

inline std::vector<ValidationProblem> SedBase::validate_own() {
    // Extra/unrecognized properties (including bad-registered-namespace
    // keys), bad dict-of-discriminated-union keys, and item-dispatch
    // problems are all detected once, at load time, by load_fields() (see
    // Dispatch.hpp) - see Design.md's Schema-Pass Errors section. This is
    // the only reliable point to see genuinely-unrecognized raw JSON keys,
    // since they are never stored anywhere in the object itself.
    std::vector<ValidationProblem> problems = load_problems_;
    jsoncons::json instance = own_json_value();

    if (type_const() && type_rule_id()) {
        bool has_type = instance.contains("_type") && !instance["_type"].is_null();
        std::string actual = has_type ? instance["_type"].as<std::string>() : "";
        if (!has_type || actual != *type_const()) {
            std::map<std::string, std::string> ph;
            ph["attr"] = "_type";
            ph["class"] = class_name();
            ph["id"] = own_id_for_message();
            ph["value"] = has_type ? actual : "null";
            ph["allowed"] = *type_const();
            problems.push_back(RuleCatalog::make_problem(*type_rule_id(), "/_type", ph));
        }
    }

    // universal name/description mixin (TestBaseFields/SEDBaseFields) -
    // not a per-class FieldSpec, so checked directly here against the
    // base mixin's own rule IDs (the same on every concrete class).
    if (name_node_ && !LeafValidation::leaf_value_ok("string", *name_node_)) {
        std::string rid = name_rule_id() ? *name_rule_id() : base_catchall();
        std::map<std::string, std::string> ph;
        ph["attr"] = "name";
        ph["class"] = class_name();
        ph["id"] = own_id_for_message();
        ph["value"] = name_node_->is_string() ? name_node_->as<std::string>() : name_node_->to_string();
        problems.push_back(RuleCatalog::make_problem(rid, "/name", ph));
    }
    if (description_node_ && !LeafValidation::leaf_value_ok("string", *description_node_)) {
        std::string rid = desc_rule_id() ? *desc_rule_id() : base_catchall();
        std::map<std::string, std::string> ph;
        ph["attr"] = "description";
        ph["class"] = class_name();
        ph["id"] = own_id_for_message();
        ph["value"] = description_node_->is_string() ? description_node_->as<std::string>() : description_node_->to_string();
        problems.push_back(RuleCatalog::make_problem(rid, "/description", ph));
    }

    static const std::set<std::string> leaf_kinds = {
        "string", "integer", "number", "boolean", "SId", "SIdRef", "StringOrRef", "NumberOrRef"};

    std::vector<FieldSpec> all(field_specs().begin(), field_specs().end());
    for (const auto& kv : namespace_fields()) {
        for (const auto& f : kv.second) all.push_back(f);
    }

    for (const auto& spec : all) {
        bool present = instance.contains(spec.name);
        if (spec.required && !present) {
            std::string rid = spec.required_rule_id ? *spec.required_rule_id : spec.origin_catchall;
            std::map<std::string, std::string> ph;
            ph["attr"] = spec.name;
            ph["class"] = class_name();
            ph["id"] = own_id_for_message();
            problems.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
            continue;
        }
        if (!present) continue;
        const jsoncons::json& value = instance[spec.name];
        if (leaf_kinds.count(spec.kind)) {
            if (!LeafValidation::leaf_value_ok(spec.kind, value, spec.minimum, spec.exclusive_minimum, spec.pattern)) {
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = class_name();
                ph["id"] = own_id_for_message();
                ph["value"] = value.is_string() ? value.as<std::string>() : value.to_string();
                problems.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
            }
        }
    }
    return problems;
}

inline std::vector<ValidationProblem> SedBase::validate(const std::string& severity_at_least) {
    std::vector<ValidationProblem> problems = validate_own();
    std::set<std::pair<std::string, std::string>> seen;
    for (const auto& p : problems) seen.insert({p.rule_id, p.location});
    for (const auto& cl : children_with_locations()) {
        for (const auto& p : cl.child->validate("warning")) {
            ValidationProblem p2{p.rule_id, p.severity, p.rule, p.message, cl.location_prefix + p.location};
            auto key = std::make_pair(p2.rule_id, p2.location);
            if (seen.count(key)) continue;
            seen.insert(key);
            problems.push_back(p2);
        }
    }
    int threshold = (severity_at_least == "warning") ? 0 : 1;
    std::vector<ValidationProblem> out;
    for (const auto& p : problems) {
        int lvl = (p.severity == "warning") ? 0 : 1;
        if (lvl >= threshold) out.push_back(p);
    }
    return out;
}

/// Backing store for an ID-keyed dict-of-discriminated-union field
/// (TestDocument.widgets/.reports, FancyWidget.choices) - insertion order
/// preserved, add-/remove-/insert-/rename (set_id) per Design.md's Classes
/// section. Owns its items via unique_ptr; exposes only non-owning
/// SedBase* to callers.
class IdKeyedCollection {
public:
    std::vector<std::string> ids() const { return order_; }

    SedBase* get(const std::string& item_id) const {
        auto it = items_.find(item_id);
        if (it == items_.end()) throw ApiError("no entry with id " + item_id);
        return it->second.get();
    }

    void add(const std::string& item_id, std::unique_ptr<SedBase> obj) {
        if (items_.count(item_id)) throw ApiError("an entry with id " + item_id + " already exists");
        order_.push_back(item_id);
        items_.emplace(item_id, std::move(obj));
    }

    void insert(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) {
        if (items_.count(item_id)) throw ApiError("an entry with id " + item_id + " already exists");
        if (index > order_.size()) throw ApiError("index out of range");
        order_.insert(order_.begin() + static_cast<long>(index), item_id);
        items_.emplace(item_id, std::move(obj));
    }

    void remove(const std::string& item_id) {
        auto it = items_.find(item_id);
        if (it == items_.end()) throw ApiError("no entry with id " + item_id);
        order_.erase(std::remove(order_.begin(), order_.end(), item_id), order_.end());
        items_.erase(it);
    }

    void set_id(const std::string& old_id, const std::string& new_id) {
        auto it = items_.find(old_id);
        if (it == items_.end()) throw ApiError("no entry with id " + old_id);
        if (items_.count(new_id) && new_id != old_id) {
            throw ApiError("an entry with id " + new_id + " already exists");
        }
        for (auto& id : order_) {
            if (id == old_id) { id = new_id; break; }
        }
        auto node = items_.extract(it);
        node.key() = new_id;
        items_.insert(std::move(node));
    }

    size_t size() const { return order_.size(); }

private:
    std::vector<std::string> order_;
    std::map<std::string, std::unique_ptr<SedBase>> items_;
};

/// Backing store for a plain (non-ID-keyed) array-of-embedded-object
/// field, e.g. WidgetOptions.notes: add- (append), remove- (by index),
/// insert- (at index). Owns its items via unique_ptr.
class ListCollection {
public:
    std::vector<SedBase*> items() const {
        std::vector<SedBase*> out;
        out.reserve(items_.size());
        for (const auto& p : items_) out.push_back(p.get());
        return out;
    }

    void add(std::unique_ptr<SedBase> obj) { items_.push_back(std::move(obj)); }

    void insert(size_t index, std::unique_ptr<SedBase> obj) {
        if (index > items_.size()) throw ApiError("index out of range");
        items_.insert(items_.begin() + static_cast<long>(index), std::move(obj));
    }

    void remove(size_t index) {
        if (index >= items_.size()) throw ApiError("index out of range");
        items_.erase(items_.begin() + static_cast<long>(index));
    }

    size_t size() const { return items_.size(); }

private:
    std::vector<std::unique_ptr<SedBase>> items_;
};

inline IdKeyedCollection& SedBase::get_dict_collection(const std::string& field_name) {
    throw ApiError("no such dict field: " + field_name);
}

inline ListCollection& SedBase::get_list_collection(const std::string& field_name) {
    throw ApiError("no such list field: " + field_name);
}

}  // namespace libsed2

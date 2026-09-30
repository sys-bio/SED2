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

#include "PyFormat.hpp"
#include "Reference.hpp"

namespace sed2test {

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
    bool is_math = false;  // x-math (Design.md's Math section / Types-0001..0004)
    std::optional<int64_t> min_length;                 // "minLength" (string-shaped leaves)
    std::optional<std::vector<std::string>> enum_values;  // "enum" (string-shaped leaves)
    std::optional<std::string> ref_type_rule_id;       // the formulaic "if a reference, must resolve to type X" rule
    std::optional<std::string> item_kind;              // ArrayOrRef element / DictOrRef value kind
    std::optional<std::string> ref_target;             // x-ref-target: "model" | "annotatedData"
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

/// Forward-declared here (full declaration, no body) so SedBase::validate_own()
/// below can call MathRules::check_math_field() for any FieldSpec::is_math
/// field - the body lives in MathRules.hpp as an out-of-line `inline`
/// definition, since MathRules.hpp itself needs ValidationProblem/RuleCatalog
/// from this header and the two would otherwise include each other. See
/// MathRules.hpp's own docstring/comment for the other half of this split.
class MathRules {
public:
    static std::vector<ValidationProblem> check_math_field(
            const std::string& value, const std::string& class_name, const std::string& id_value,
            const std::string& attr, const std::string& location);
};

class SedBase;

/// Forward-declared (full declaration, no body) for the same header-cycle
/// reason as MathRules above: SedBase::validate_own() dispatches every
/// reference-driven rule (SEDBase-0005 .. -0017, AbstractTask-0003,
/// Repeat-0008 .. -0010, LoopVariable-0004, SEDDocument-0009 .. -0011 and
/// -0013) through these entry points, whose `inline` bodies live in
/// RefRules.hpp (pulled in by GeneratedModel.hpp). Each one is a no-op for a
/// spec tree that did not define the corresponding rules.
class RefRules {
public:
    static std::vector<ValidationProblem> check_reference_field(
            const std::string& value, SedBase* document, const RuleCtx& base_ctx, SedBase* referrer,
            const RefFieldInfo& info);
    static std::vector<ValidationProblem> check_repeat_own_children(SedBase* self);
    static std::vector<ValidationProblem> check_loop_variable_scope(SedBase* self);
    static std::vector<ValidationProblem> check_namespace_usage_and_version(SedBase* document);
    static std::vector<ValidationProblem> check_constants_ordering(SedBase* document);
    /// SEDBase-0005 applied to a REFERENCE token embedded in a math string
    /// (SEDBase-0005.md); a no-op when the tree has no reference rules.
    static std::vector<ValidationProblem> check_math_reference_root(
            const std::string& reference_text, const std::string& class_name, const std::string& id_value,
            const std::string& attr, const std::string& location);
};

/// Per-field leaf validation, via the real JSON Schema validator
/// (jsoncons's bundled jsonschema extension, per Design.md's Toolchain
/// mandate) - a tiny schema fragment is built from one already-resolved
/// field's own type, never a whole-document schema, since every combinator
/// has already been resolved away by the generator at compose time (see
/// generator/spec.py). Mirrors emit_python.py's leaf_schema_for()/
/// leaf_value_ok() exactly; compiled fragments are cached by their
/// parameters, since the same handful recur for every element validated.
class LeafValidation {
public:
    static constexpr const char* SID_PATTERN = "^[A-Za-z_][A-Za-z0-9_]*$";
    static constexpr const char* SIDREF_PATTERN = "^#.*$";

    static bool is_sid(const std::string& s) {
        static const std::regex re(SID_PATTERN);
        return std::regex_match(s, re);
    }

    static bool leaf_value_ok(const std::string& kind, const Json& value,
                               std::optional<double> minimum = std::nullopt,
                               std::optional<double> exclusive_minimum = std::nullopt,
                               std::optional<std::string> pattern = std::nullopt,
                               std::optional<int64_t> min_length = std::nullopt,
                               const std::optional<std::vector<std::string>>& enum_values = std::nullopt) {
        using schema_t = jsoncons::jsonschema::json_schema<Json>;
        static std::map<std::string, std::unique_ptr<schema_t>> cache;
        std::string key = kind;
        key += '\x1f';
        if (minimum) key += "m" + std::to_string(*minimum);
        key += '\x1f';
        if (exclusive_minimum) key += "x" + std::to_string(*exclusive_minimum);
        key += '\x1f';
        if (pattern) key += "p" + *pattern;
        key += '\x1f';
        if (min_length) key += "l" + std::to_string(*min_length);
        key += '\x1f';
        if (enum_values) {
            key += "e";
            for (const auto& e : *enum_values) key += e + '\x1e';
        }
        auto it = cache.find(key);
        if (it == cache.end()) {
            Json schema = leaf_schema_for(kind, minimum, exclusive_minimum, pattern, min_length, enum_values);
            it = cache.emplace(key, std::make_unique<schema_t>(jsoncons::jsonschema::make_json_schema(schema))).first;
        }
        bool ok = true;
        auto reporter = [&](const jsoncons::jsonschema::validation_message&) -> jsoncons::jsonschema::walk_result {
            ok = false;
            return jsoncons::jsonschema::walk_result::advance;
        };
        it->second->validate(value, reporter);
        return ok;
    }

private:
    static Json type_schema(const char* type) {
        Json n = Json::object();
        n["type"] = type;
        return n;
    }
    static Json ref_schema() {
        Json ref = Json::object();
        ref["type"] = "string";
        ref["pattern"] = SIDREF_PATTERN;
        return ref;
    }
    static Json any_of(const Json& a, const Json& b) {
        Json any = Json::array();
        any.push_back(a);
        any.push_back(b);
        Json n = Json::object();
        n["anyOf"] = any;
        return n;
    }

    static Json base_schema(const std::string& kind) {
        if (kind == "string") return type_schema("string");
        if (kind == "integer") return type_schema("integer");
        if (kind == "number") return type_schema("number");
        if (kind == "boolean") return type_schema("boolean");
        if (kind == "SId" || kind == "SIdRef") {
            Json n = type_schema("string");
            n["pattern"] = kind == "SId" ? SID_PATTERN : SIDREF_PATTERN;
            return n;
        }
        if (kind == "StringOrRef") {
            Json any = Json::array();
            any.push_back(type_schema("string"));
            Json n = Json::object();
            n["anyOf"] = any;
            return n;
        }
        if (kind == "NumberOrRef") return any_of(type_schema("number"), ref_schema());
        if (kind == "IntegerOrRef") return any_of(type_schema("integer"), ref_schema());
        if (kind == "BooleanOrRef") return any_of(type_schema("boolean"), ref_schema());
        if (kind == "ArrayOrRef") return any_of(type_schema("array"), ref_schema());
        if (kind == "DictOrRef") return any_of(type_schema("object"), ref_schema());
        throw std::invalid_argument("unknown leaf kind: " + kind);
    }

    static Json leaf_schema_for(const std::string& kind, std::optional<double> minimum,
                                 std::optional<double> exclusive_minimum, const std::optional<std::string>& pattern,
                                 std::optional<int64_t> min_length,
                                 const std::optional<std::vector<std::string>>& enum_values) {
        Json base = base_schema(kind);
        // minimum/exclusiveMinimum are numeric-only keywords - a no-op against
        // a non-numeric instance (a reference string, for an *OrRef kind).
        if (minimum) base["minimum"] = *minimum;
        if (exclusive_minimum) base["exclusiveMinimum"] = *exclusive_minimum;
        if (pattern || min_length || enum_values) {
            Json sc = Json::object();
            if (pattern) sc["pattern"] = *pattern;
            if (min_length) sc["minLength"] = *min_length;
            if (enum_values) {
                Json arr = Json::array();
                for (const auto& e : *enum_values) arr.push_back(e);
                sc["enum"] = arr;
            }
            if (kind == "StringOrRef") {
                // A StringOrRef's reference form is also a plain string, so
                // pattern/minLength/enum are split onto the literal branch only.
                Json lit = type_schema("string");
                for (const auto& kv : sc.object_range()) lit[kv.key()] = kv.value();
                base = any_of(lit, ref_schema());
            } else {
                for (const auto& kv : sc.object_range()) base[kv.key()] = kv.value();
            }
        }
        return base;
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
class AnyDictCollection;

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

    // -- reference-resolution metadata (Design.md's Cross-references / -
    // Validation sections), overridden per generated concrete class; see
    // RefRules.hpp. Mirrors the reference implementation's
    // _get_id_collection / _id_collection_names / _OUTPUTS_JSON /
    // _IS_DOCUMENT_CLASS / _MAX_KNOWN_DOCUMENT_VERSION / get_type().
    /// The ID-keyed dict-kind collection stored under `field_name`, or null.
    virtual const IdKeyedCollection* find_dict_collection(const std::string& field_name) const {
        (void)field_name;
        return nullptr;
    }
    /// The any-dict-kind collection (raw JSON values, e.g. constants), or null.
    virtual const AnyDictCollection* find_any_dict_collection(const std::string& field_name) const {
        (void)field_name;
        return nullptr;
    }
    /// Every ID-keyed collection field name THIS class declares (dict-kind and
    /// any-dict-kind), for own_id_for_message().
    virtual std::vector<std::string> id_collection_names() const { return {}; }
    /// core-spec.md Section 8's per-class outputs.json envelope; null for every
    /// class except a concrete tasks/ one.
    virtual const Json* outputs_json() const { return nullptr; }
    virtual bool is_document_class() const { return false; }
    virtual std::optional<std::string> max_known_document_version() const { return std::nullopt; }
    /// The class's own _type value (a generated class's const, or an Unknown
    /// holder's raw type), when it has one.
    virtual std::optional<std::string> get_type_value() const { return std::nullopt; }

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
    // Stored as the raw Json (not a coerced std::string) so a
    // wrong-typed incoming value (e.g. a JSON number for `name`) is
    // preserved for the leaf-type check in validate_own() instead of
    // being silently stringified away.
    std::string get_name() const {
        if (!name_node_) throw ApiError("name is not set");
        return name_node_->as<std::string>();
    }
    bool is_set_name() const { return name_node_.has_value(); }
    void set_name(const std::string& value) { name_node_ = Json(value); }
    void unset_name() { name_node_.reset(); }

    std::string get_description() const {
        if (!description_node_) throw ApiError("description is not set");
        return description_node_->as<std::string>();
    }
    bool is_set_description() const { return description_node_.has_value(); }
    void set_description(const std::string& value) { description_node_ = Json(value); }
    void unset_description() { description_node_.reset(); }

    // -- generic namespace attribute store (Design.md's Namespaces section) --
    Json get_namespace_attribute(const std::string& prefix, const std::string& key) const {
        std::string k = prefix + "@" + key;
        auto it = ns_attrs_.find(k);
        if (it == ns_attrs_.end()) throw ApiError("namespace attribute " + k + " is not set");
        return it->second;
    }
    void set_namespace_attribute(const std::string& prefix, const std::string& key, const Json& value) {
        ns_attrs_[prefix + "@" + key] = value;
    }
    bool is_set_namespace_attribute(const std::string& prefix, const std::string& key) const {
        return ns_attrs_.count(prefix + "@" + key) > 0;
    }
    void unset_namespace_attribute(const std::string& prefix, const std::string& key) {
        ns_attrs_.erase(prefix + "@" + key);
    }

    // -- generic OrRef-shaped storage helpers, used by generated accessors --
    Json get_or_ref_value_node(const std::string& name) const {
        auto it = values_.find(name);
        if (it == values_.end()) throw ApiError(name + " is not set");
        auto rit = or_ref_is_ref_.find(name);
        if (rit != or_ref_is_ref_.end() && rit->second) {
            throw ApiError(name + " holds a reference, not a literal value");
        }
        return it->second;
    }
    Json get_or_ref_ref_node(const std::string& name) const {
        auto it = values_.find(name);
        if (it == values_.end()) throw ApiError(name + " is not set");
        auto rit = or_ref_is_ref_.find(name);
        if (rit == or_ref_is_ref_.end() || !rit->second) {
            throw ApiError(name + " holds a literal value, not a reference");
        }
        return it->second;
    }
    void set_or_ref_value_node(const std::string& name, const Json& value) {
        values_[name] = value;
        or_ref_is_ref_[name] = false;
    }
    void set_or_ref_ref_node(const std::string& name, const std::string& ref) {
        if (!is_reference(ref)) throw ApiError("'" + ref + "' is not a valid reference (must start with '#')");
        values_[name] = Json(ref);
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

    /// Backing store for an "any-dict"-kind field (an ID-keyed collection of
    /// raw JSON values, never SedBase instances - e.g. SEDDocument.
    /// constants). Overridden per generated concrete class, mirroring
    /// get_dict_collection above.
    virtual AnyDictCollection& get_any_dict_collection(const std::string& field_name);

    /// Sets a "ref-class"/"ref-discriminator"-kind field's single nested
    /// child (taking ownership) - used only by load_fields() in
    /// Dispatch.hpp, which constructs the child generically and needs a way
    /// to store it back onto the right instance field without knowing the
    /// concrete class. Overridden per generated concrete class.
    virtual void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child);

    // -- validate() engine --------------------------------------------------
    std::vector<ValidationProblem> validate(const std::string& severity_at_least = "warning");

    struct ChildLoc {
        SedBase* child;
        std::string location_prefix;
    };

    /// [(child, "/jsonPointerSegment"), ...] - override per concrete class.
    /// Default: none.
    virtual std::vector<ChildLoc> children_with_locations() { return {}; }

    /// This element's own SId, for a validation message's {id} placeholder:
    /// id is implicit (the key under which an element is stored in its owning
    /// collection), so this searches the parent's ID-keyed collections for
    /// self; "?" for anything genuinely id-less (the document root, an
    /// array-item class, an unattached instance).
    virtual std::string own_id_for_message() const;
    virtual Json own_json_value() const = 0;

    virtual std::set<std::string> allowed_keys() const {
        std::set<std::string> keys;
        for (const auto& f : field_specs()) keys.insert(f.name);
        for (const auto& kv : namespace_fields()) {
            for (const auto& f : kv.second) keys.insert(f.name);
        }
        return keys;
    }

    Json to_json_value() const { return own_json_value(); }

    // -- internal storage (see class comment) --
    std::optional<Json> name_node_;
    std::optional<Json> description_node_;
    std::map<std::string, Json> values_;
    std::map<std::string, bool> or_ref_is_ref_;
    std::map<std::string, Json> ns_attrs_;
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
    Json instance = own_json_value();
    const std::string cls = class_name();
    const std::string self_id = own_id_for_message();

    if (type_const() && type_rule_id()) {
        bool ok = instance.contains("_type") && instance["_type"].is_string() &&
                  instance["_type"].as<std::string>() == *type_const();
        if (!ok) {
            std::map<std::string, std::string> ph;
            ph["attr"] = "_type";
            ph["class"] = cls;
            ph["id"] = self_id;
            ph["value"] = instance.contains("_type") ? pyfmt::str(instance["_type"]) : "None";
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
        ph["class"] = cls;
        ph["id"] = self_id;
        ph["value"] = pyfmt::str(*name_node_);
        problems.push_back(RuleCatalog::make_problem(rid, "/name", ph));
    }
    if (description_node_ && !LeafValidation::leaf_value_ok("string", *description_node_)) {
        std::string rid = desc_rule_id() ? *desc_rule_id() : base_catchall();
        std::map<std::string, std::string> ph;
        ph["attr"] = "description";
        ph["class"] = cls;
        ph["id"] = self_id;
        ph["value"] = pyfmt::str(*description_node_);
        problems.push_back(RuleCatalog::make_problem(rid, "/description", ph));
    }

    // "any" is deliberately NOT a member: an AnyValueOrRef-typed field (any
    // JSON value) has no leaf_value_ok()-equivalent schema to check against,
    // but an SIdRef string may still substitute for it, so it gets the same
    // reference-resolution dispatch as every *OrRef kind (see below).
    static const std::set<std::string> leaf_kinds = {
        "string", "integer", "number", "boolean", "SId", "SIdRef", "StringOrRef", "NumberOrRef",
        "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef"};
    // Every leaf kind whose value can structurally BE a reference - SIdRef is
    // always one, and every *OrRef kind's own anyOf includes one.
    static const std::set<std::string> reference_capable = {
        "SIdRef", "StringOrRef", "NumberOrRef", "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef"};

    auto is_ref_value = [](const Json& v) {
        return v.is_string() && !v.as<std::string>().empty() && v.as<std::string>()[0] == '#';
    };

    auto check_spec = [&](const FieldSpec& spec) {
        bool present = instance.contains(spec.name);
        if (spec.required && !present) {
            std::string rid = spec.required_rule_id ? *spec.required_rule_id : spec.origin_catchall;
            std::map<std::string, std::string> ph;
            ph["attr"] = spec.name;
            ph["class"] = cls;
            ph["id"] = self_id;
            problems.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
            return;
        }
        if (!present) return;
        const Json& value = instance[spec.name];
        const std::string loc = "/" + spec.name;
        if (leaf_kinds.count(spec.kind)) {
            if (!LeafValidation::leaf_value_ok(spec.kind, value, spec.minimum, spec.exclusive_minimum, spec.pattern,
                                                spec.min_length, spec.enum_values)) {
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = cls;
                ph["id"] = self_id;
                ph["value"] = pyfmt::str(value);
                if (spec.enum_values) {
                    // A rule fired from an enum-constrained leaf's own message
                    // template may reference {allowed} - harmless to always
                    // include, since only placeholders the template names are
                    // substituted.
                    std::string allowed;
                    for (size_t i = 0; i < spec.enum_values->size(); i++) {
                        if (i) allowed += ", ";
                        allowed += pyfmt::str_repr((*spec.enum_values)[i]);
                    }
                    ph["allowed"] = allowed;
                }
                problems.push_back(RuleCatalog::make_problem(rid, loc, ph));
            } else if (reference_capable.count(spec.kind) && is_ref_value(value)) {
                RefFieldInfo info;
                info.field_kind = spec.kind;
                info.ref_type_rule_id = spec.ref_type_rule_id;
                info.expected_enum = spec.enum_values ? &*spec.enum_values : nullptr;
                info.minimum = spec.minimum;
                info.exclusive_minimum = spec.exclusive_minimum;
                info.item_kind = spec.item_kind;
                info.ref_target = spec.ref_target;
                RuleCtx ctx{cls, self_id, spec.name, loc, ""};
                auto more = RefRules::check_reference_field(value.as<std::string>(), get_document(), ctx, this, info);
                problems.insert(problems.end(), more.begin(), more.end());
            } else if (spec.kind == "DictOrRef" && value.is_object()) {
                // The dict-literal branch of a DictOrRef field (e.g.
                // Repeat.outputVariableMap: an SId-keyed map of column name ->
                // SIdRef): each entry gets its OWN reference-resolution
                // dispatch (SEDBase-0005 .. -0015) rather than the field as a
                // single unit. No ref-type rule is passed - the field's own
                // ref_type_rule_id describes what the WHOLE FIELD must resolve
                // to when IT is a reference, not what each entry's target must be.
                for (const auto& kv : value.object_range()) {
                    if (!is_ref_value(kv.value())) continue;
                    RefFieldInfo info;
                    info.field_kind = spec.kind;
                    RuleCtx ctx{cls, self_id, spec.name, loc + "/" + std::string(kv.key()), ""};
                    auto more = RefRules::check_reference_field(kv.value().as<std::string>(), get_document(), ctx,
                                                                this, info);
                    problems.insert(problems.end(), more.begin(), more.end());
                }
            } else if (spec.kind == "ArrayOrRef" && value.is_array()) {
                // The array-literal branch of an ArrayOrRef field: each
                // element that is itself a reference gets its own
                // reference-resolution dispatch (SEDBase-0005.md: the rule
                // applies to "an element of an array or object value"), with
                // no per-element expected type - same scope as the DictOrRef
                // dict-literal branch above.
                size_t idx = 0;
                for (const auto& el : value.array_range()) {
                    if (is_ref_value(el)) {
                        RefFieldInfo info;
                        info.field_kind = spec.kind;
                        RuleCtx ctx{cls, self_id, spec.name, loc + "/" + std::to_string(idx), ""};
                        auto more = RefRules::check_reference_field(el.as<std::string>(), get_document(), ctx,
                                                                    this, info);
                        problems.insert(problems.end(), more.begin(), more.end());
                    }
                    idx++;
                }
            } else if (spec.is_math && value.is_string()) {
                // Types-0001..0004 (Design.md's Math section) - only for a
                // literal string value that already passed its own leaf schema
                // check above; a reference form of a math field is skipped.
                auto math_problems = MathRules::check_math_field(value.as<std::string>(), cls, self_id, spec.name, loc);
                problems.insert(problems.end(), math_problems.begin(), math_problems.end());
            }
        } else if (spec.kind == "any" && is_ref_value(value)) {
            RefFieldInfo info;
            info.field_kind = "any";
            RuleCtx ctx{cls, self_id, spec.name, loc, ""};
            auto more = RefRules::check_reference_field(value.as<std::string>(), get_document(), ctx, this, info);
            problems.insert(problems.end(), more.begin(), more.end());
        }
    };

    for (const auto& spec : field_specs()) check_spec(spec);
    for (const auto& kv : namespace_fields()) {
        for (const auto& spec : kv.second) check_spec(spec);
    }

    if (is_document_class()) {
        auto ns = RefRules::check_namespace_usage_and_version(this);
        problems.insert(problems.end(), ns.begin(), ns.end());
        auto co = RefRules::check_constants_ordering(this);
        problems.insert(problems.end(), co.begin(), co.end());
    }
    // Repeat-0008/-0009/-0010 and LoopVariable-0004 each internally no-op for
    // every class they don't apply to (a cheap class-shape check, not a
    // class-name check).
    auto rep = RefRules::check_repeat_own_children(this);
    problems.insert(problems.end(), rep.begin(), rep.end());
    auto lv = RefRules::check_loop_variable_scope(this);
    problems.insert(problems.end(), lv.begin(), lv.end());
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

    /// Like get(), but null (never throws) for an unknown id.
    SedBase* find(const std::string& item_id) const {
        auto it = items_.find(item_id);
        return it == items_.end() ? nullptr : it->second.get();
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

inline std::string SedBase::own_id_for_message() const {
    SedBase* parent = get_parent();
    if (parent == nullptr) return "?";
    for (const auto& name : parent->id_collection_names()) {
        const IdKeyedCollection* coll = parent->find_dict_collection(name);
        if (coll == nullptr) continue;
        for (const auto& iid : coll->ids()) {
            if (coll->find(iid) == this) return iid;
        }
    }
    return "?";
}

inline IdKeyedCollection& SedBase::get_dict_collection(const std::string& field_name) {
    throw ApiError("no such dict field: " + field_name);
}

inline ListCollection& SedBase::get_list_collection(const std::string& field_name) {
    throw ApiError("no such list field: " + field_name);
}

/// Backing store for an "any-dict"-kind field - same ID-keyed-collection
/// shape as IdKeyedCollection above, but holds plain Json values
/// directly (no ownership/unique_ptr involved, since a raw JSON value isn't
/// a SedBase) - e.g. SEDDocument.constants. Mirrors
/// generator/emit_python.py's _collection_accessors any-dict branch and
/// emit_java.py's IdKeyedCollection<JsonNode> re-use, the reference
/// implementations this ports (C++'s IdKeyedCollection is itself
/// unique_ptr<SedBase>-owning, so - unlike Java, which merely relaxed a
/// generic bound - it can't be reused as-is here; a separate small class is
/// the natural equivalent).
class AnyDictCollection {
public:
    std::vector<std::string> ids() const { return order_; }

    Json get(const std::string& item_id) const {
        auto it = items_.find(item_id);
        if (it == items_.end()) throw ApiError("no entry with id " + item_id);
        return it->second;
    }

    /// Like get(), but a pointer to the stored value (null for an unknown id).
    const Json* find(const std::string& item_id) const {
        auto it = items_.find(item_id);
        return it == items_.end() ? nullptr : &it->second;
    }

    void add(const std::string& item_id, Json value) {
        if (items_.count(item_id)) throw ApiError("an entry with id " + item_id + " already exists");
        order_.push_back(item_id);
        items_.emplace(item_id, std::move(value));
    }

    void insert(size_t index, const std::string& item_id, Json value) {
        if (items_.count(item_id)) throw ApiError("an entry with id " + item_id + " already exists");
        if (index > order_.size()) throw ApiError("index out of range");
        order_.insert(order_.begin() + static_cast<long>(index), item_id);
        items_.emplace(item_id, std::move(value));
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
    std::map<std::string, Json> items_;
};

inline AnyDictCollection& SedBase::get_any_dict_collection(const std::string& field_name) {
    throw ApiError("no such any-dict field: " + field_name);
}

inline void SedBase::set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) {
    (void)child;
    throw ApiError("no such child field: " + field_name);
}

}  // namespace sed2test

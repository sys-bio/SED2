// Generated dispatch/parse per discriminator, plus the generic field
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

namespace sed2test {

struct DispatchResult {
    std::unique_ptr<SedBase> value;
    std::optional<ValidationProblem> problem;
};

inline void load_fields(SedBase* obj, const Json& raw);

inline DispatchResult parse_AbstractWidget(const Json& raw) {
    if (!raw.contains("_type")) {
        return DispatchResult{nullptr, RuleCatalog::make_problem("AbstractWidget-0002", "")};
    }
    const Json& tvj = raw.at("_type");
    const bool tv_is_str = tvj.is_string();
    std::string tv = tv_is_str ? tvj.as<std::string>() : pyfmt::str(tvj);
    std::unique_ptr<SedBase> obj;
    if (tv_is_str && tv == "fancyWidget") obj = std::make_unique<FancyWidget>();
    else if (tv_is_str && tv == "mathWidget") obj = std::make_unique<MathWidget>();
    else if (tv_is_str && tv == "simpleWidget") obj = std::make_unique<SimpleWidget>();
    else if (tv_is_str && tv == "typesWidget") obj = std::make_unique<TypesWidget>();
    else if (tv_is_str && tv == "acme@acmeWidget") obj = std::make_unique<AcmeWidget>();
    if (obj) {
        load_fields(obj.get(), raw);
        return DispatchResult{std::move(obj), std::nullopt};
    }
    std::smatch m;
    bool ns_match = tv_is_str && std::regex_match(tv, m, namespace_key_pattern());
    static const std::set<std::string> known = {"acme"};
    if (ns_match && !known.count(m[1].str())) {
        return DispatchResult{std::make_unique<UnknownAbstractWidget>(tv, raw), std::nullopt};
    }
    std::map<std::string, std::string> ph;
    ph["schema-message"] = "unrecognized _type " + pyfmt::repr(tvj);
    return DispatchResult{std::make_unique<UnknownAbstractWidget>(tv, raw), RuleCatalog::make_problem("AbstractWidget-0000", "", ph)};
}

inline DispatchResult parse_AbstractReport(const Json& raw) {
    if (!raw.contains("_type")) {
        return DispatchResult{nullptr, RuleCatalog::make_problem("AbstractReport-0002", "")};
    }
    const Json& tvj = raw.at("_type");
    const bool tv_is_str = tvj.is_string();
    std::string tv = tv_is_str ? tvj.as<std::string>() : pyfmt::str(tvj);
    std::unique_ptr<SedBase> obj;
    if (tv_is_str && tv == "simpleReport") obj = std::make_unique<SimpleReport>();
    if (obj) {
        load_fields(obj.get(), raw);
        return DispatchResult{std::move(obj), std::nullopt};
    }
    std::smatch m;
    bool ns_match = tv_is_str && std::regex_match(tv, m, namespace_key_pattern());
    static const std::set<std::string> known = {};
    if (ns_match && !known.count(m[1].str())) {
        return DispatchResult{std::make_unique<UnknownAbstractReport>(tv, raw), std::nullopt};
    }
    std::map<std::string, std::string> ph;
    ph["schema-message"] = "unrecognized _type " + pyfmt::repr(tvj);
    return DispatchResult{std::make_unique<UnknownAbstractReport>(tv, raw), RuleCatalog::make_problem("AbstractReport-0000", "", ph)};
}

inline DispatchResult parse_ChoiceInline(const Json& raw) {
    if (!raw.contains("_type")) {
        std::map<std::string, std::string> ph0;
        ph0["schema-message"] = "missing _type";
        return DispatchResult{nullptr, RuleCatalog::make_problem("ChoiceInline-0000", "", ph0)};
    }
    const Json& tvj = raw.at("_type");
    const bool tv_is_str = tvj.is_string();
    std::string tv = tv_is_str ? tvj.as<std::string>() : pyfmt::str(tvj);
    std::unique_ptr<SedBase> obj;
    if (tv_is_str && tv == "choice") obj = std::make_unique<Choice>();
    else if (tv_is_str && tv == "weightedChoice") obj = std::make_unique<WeightedChoice>();
    if (obj) {
        load_fields(obj.get(), raw);
        return DispatchResult{std::move(obj), std::nullopt};
    }
    std::smatch m;
    bool ns_match = tv_is_str && std::regex_match(tv, m, namespace_key_pattern());
    static const std::set<std::string> known = {};
    if (ns_match && !known.count(m[1].str())) {
        return DispatchResult{std::make_unique<UnknownChoiceInline>(tv, raw), std::nullopt};
    }
    std::map<std::string, std::string> ph;
    ph["schema-message"] = "unrecognized _type " + pyfmt::repr(tvj);
    return DispatchResult{std::make_unique<UnknownChoiceInline>(tv, raw), RuleCatalog::make_problem("ChoiceInline-0000", "", ph)};
}

inline DispatchResult dispatch_parse(const std::string& disc_name, const Json& raw) {
    if (disc_name == "AbstractWidget") return parse_AbstractWidget(raw);
    else if (disc_name == "AbstractReport") return parse_AbstractReport(raw);
    else if (disc_name == "ChoiceInline") return parse_ChoiceInline(raw);
    throw ApiError("unknown discriminator " + disc_name);
}

inline std::unique_ptr<SedBase> new_item_instance(const std::string& class_name) {
    if (class_name == "Note") return std::make_unique<Note>();
    throw ApiError("unknown item class " + class_name);
}

inline void load_fields(SedBase* obj, const Json& raw) {
    if (!raw.is_object()) return;   // never throw for a malformed document
    if (raw.contains("name") && !raw.at("name").is_null()) obj->name_node_ = raw.at("name");
    if (raw.contains("description") && !raw.at("description").is_null()) obj->description_node_ = raw.at("description");
    if (raw.contains("_type")) obj->values_["_type"] = raw.at("_type");

    // The full OrRef family whose value is loaded via the generic
    // set_or_ref_value_node/set_or_ref_ref_node pair rather than a plain
    // obj->values_[...] assignment - see generator/emit_cpp.py's
    // _ORREF_KINDS_CPP (the same six kinds every generated model class's
    // own accessors handle).
    static const std::set<std::string> orref_kinds = {
        "StringOrRef", "NumberOrRef", "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef"};

    for (const auto& spec : obj->field_specs()) {
        if (!raw.contains(spec.name) || spec.kind == "dict" || spec.kind == "array"
                || spec.kind == "any-dict" || spec.kind == "ref-class"
                || spec.kind == "ref-discriminator") continue;
        const Json& v = raw.at(spec.name);
        if (orref_kinds.count(spec.kind)) {
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
            const Json& raw_value = raw.at(spec.name);
            if (!raw_value.is_object()) {
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = obj->class_name();
                ph["id"] = obj->own_id_for_message();
                ph["value"] = pyfmt::str(raw_value);
                obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                continue;
            }
            IdKeyedCollection& coll = obj->get_dict_collection(spec.name);
            // A dict-kind field is either _type-dispatched (item_discriminator
            // set, e.g. SEDDocument.tasks -> AbstractTask) or a plain
            // fixed-class dict with no _type dispatch at all (item_class set
            // instead, e.g. SEDDocument.styles -> Style, Loop.loopVariables
            // -> LoopVariable) - dereferencing spec.item_discriminator
            // unconditionally would be undefined behavior when it's
            // std::nullopt, so this mirrors the "array"-kind branch's own
            // new_item_instance fallback just below, and
            // generator/emit_python.py's _load_fields dict branch
            // (`dispatch = ... if spec.item_discriminator else None`), the
            // reference implementation this ports.
            for (const auto& item_kv : raw_value.object_range()) {
                const std::string& item_id = item_kv.key();
                const Json& item_raw = item_kv.value();
                if (!LeafValidation::is_sid(item_id)) {
                    std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                    std::map<std::string, std::string> ph;
                    ph["attr"] = spec.name;
                    ph["class"] = obj->class_name();
                    ph["id"] = obj->own_id_for_message();
                    ph["value"] = item_id;
                    obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                }
                std::unique_ptr<SedBase> child;
                if (spec.item_discriminator) {
                    DispatchResult r = dispatch_parse(*spec.item_discriminator, item_raw);
                    if (r.problem) obj->load_problems_.push_back(*r.problem);
                    child = std::move(r.value);
                } else {
                    child = new_item_instance(*spec.item_class);
                    load_fields(child.get(), item_raw);
                }
                if (child) coll.add(item_id, std::move(child));
            }
        } else if (spec.kind == "array" && raw.contains(spec.name)) {
            const Json& raw_value = raw.at(spec.name);
            if (!raw_value.is_array()) {
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = obj->class_name();
                ph["id"] = obj->own_id_for_message();
                ph["value"] = pyfmt::str(raw_value);
                obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                continue;
            }
            ListCollection& coll = obj->get_list_collection(spec.name);
            for (const auto& item_raw : raw_value.array_range()) {
                std::unique_ptr<SedBase> child = new_item_instance(*spec.item_class);
                load_fields(child.get(), item_raw);
                coll.add(std::move(child));
            }
        } else if (spec.kind == "any-dict" && raw.contains(spec.name)) {
            // Same ID-keyed-collection shape as "dict" just above, but every
            // value is stored as-is - a plain Json, never
            // constructed as a class instance (see this module's
            // _collection_accessors_cpp any-dict branch and
            // generator/emit_python.py's _load_fields any-dict branch, the
            // reference implementation this mirrors).
            const Json& raw_value = raw.at(spec.name);
            if (!raw_value.is_object()) {
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = obj->class_name();
                ph["id"] = obj->own_id_for_message();
                ph["value"] = pyfmt::str(raw_value);
                obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                continue;
            }
            AnyDictCollection& coll = obj->get_any_dict_collection(spec.name);
            for (const auto& item_kv : raw_value.object_range()) {
                const std::string& item_id = item_kv.key();
                if (!LeafValidation::is_sid(item_id)) {
                    std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                    std::map<std::string, std::string> ph;
                    ph["attr"] = spec.name;
                    ph["class"] = obj->class_name();
                    ph["id"] = obj->own_id_for_message();
                    ph["value"] = item_id;
                    obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                }
                coll.add(item_id, item_kv.value());
            }
        } else if ((spec.kind == "ref-class" || spec.kind == "ref-discriminator") && raw.contains(spec.name)) {
            // A single nested SedBase-derived child (see this module's
            // _child_accessors_cpp docstring) - "ref-class" constructs a
            // fixed target class directly; "ref-discriminator" dispatches
            // on the raw JSON's own _type via the matching parse_*
            // function, same as a dict-kind field's own discriminated
            // items above. Mirrors generator/emit_python.py's _load_fields
            // ref-class/ref-discriminator branch.
            const Json& raw_value = raw.at(spec.name);
            if (!raw_value.is_object()) {
                std::string rid = spec.rule_id ? *spec.rule_id : spec.origin_catchall;
                std::map<std::string, std::string> ph;
                ph["attr"] = spec.name;
                ph["class"] = obj->class_name();
                ph["id"] = obj->own_id_for_message();
                ph["value"] = pyfmt::str(raw_value);
                obj->load_problems_.push_back(RuleCatalog::make_problem(rid, "/" + spec.name, ph));
                continue;
            }
            std::unique_ptr<SedBase> child;
            if (spec.kind == "ref-discriminator") {
                DispatchResult r = dispatch_parse(*spec.item_discriminator, raw_value);
                if (r.problem) obj->load_problems_.push_back(*r.problem);
                child = std::move(r.value);
            } else {
                child = new_item_instance(*spec.item_class);
                load_fields(child.get(), raw_value);
            }
            if (child) obj->set_child_field(spec.name, std::move(child));
        }
    }
}

}  // namespace sed2test

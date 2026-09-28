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

namespace libsed2 {

struct DispatchResult {
    std::unique_ptr<SedBase> value;
    std::optional<ValidationProblem> problem;
};

inline void load_fields(SedBase* obj, const jsoncons::json& raw);

inline DispatchResult parse_AbstractTask(const jsoncons::json& raw) {
    if (!raw.contains("_type")) {
        return DispatchResult{nullptr, RuleCatalog::make_problem("AbstractTask-0002", "")};
    }
    std::string tv = raw.at("_type").as<std::string>();
    std::unique_ptr<SedBase> obj;
    if (tv == "aggregationCalculation") obj = std::make_unique<AggregationCalculation>();
    else if (tv == "boundedODESimulation") obj = std::make_unique<BoundedODESimulation>();
    else if (tv == "boundedStochasticSimulation") obj = std::make_unique<BoundedStochasticSimulation>();
    else if (tv == "calculation") obj = std::make_unique<Calculation>();
    else if (tv == "createDataBlock") obj = std::make_unique<CreateDataBlock>();
    else if (tv == "csvImport") obj = std::make_unique<CsvImport>();
    else if (tv == "dataImport") obj = std::make_unique<DataImport>();
    else if (tv == "drawFromDistribution") obj = std::make_unique<DrawFromDistribution>();
    else if (tv == "explicitODESimulation") obj = std::make_unique<ExplicitODESimulation>();
    else if (tv == "explicitStochasticSimulation") obj = std::make_unique<ExplicitStochasticSimulation>();
    else if (tv == "fluxBalanceAnalysis") obj = std::make_unique<FluxBalanceAnalysis>();
    else if (tv == "jacobianFull") obj = std::make_unique<JacobianFull>();
    else if (tv == "jacobianReduced") obj = std::make_unique<JacobianReduced>();
    else if (tv == "loop") obj = std::make_unique<Loop>();
    else if (tv == "modelChange") obj = std::make_unique<ModelChange>();
    else if (tv == "modelElementList") obj = std::make_unique<ModelElementList>();
    else if (tv == "modelImport") obj = std::make_unique<ModelImport>();
    else if (tv == "numericRange") obj = std::make_unique<NumericRange>();
    else if (tv == "oneStepODE") obj = std::make_unique<OneStepODESimulation>();
    else if (tv == "oneStepStochastic") obj = std::make_unique<OneStepStochasticSimulation>();
    else if (tv == "parameterRange") obj = std::make_unique<ParameterRange>();
    else if (tv == "parameterScan") obj = std::make_unique<ParameterScan>();
    else if (tv == "range") obj = std::make_unique<Range>();
    else if (tv == "relabelData") obj = std::make_unique<RelabelData>();
    else if (tv == "scatter") obj = std::make_unique<Scatter>();
    else if (tv == "steadyState") obj = std::make_unique<SteadyState>();
    else if (tv == "stringFormation") obj = std::make_unique<StringFormation>();
    if (obj) {
        load_fields(obj.get(), raw);
        return DispatchResult{std::move(obj), std::nullopt};
    }
    std::smatch m;
    bool ns_match = std::regex_match(tv, m, namespace_key_pattern());
    static const std::set<std::string> known = {};
    if (ns_match && !known.count(m[1].str())) {
        return DispatchResult{std::make_unique<UnknownAbstractTask>(tv, raw), std::nullopt};
    }
    std::map<std::string, std::string> ph;
    ph["schema-message"] = "unrecognized _type '" + tv + "'";
    return DispatchResult{std::make_unique<UnknownAbstractTask>(tv, raw), RuleCatalog::make_problem("AbstractTask-0000", "", ph)};
}

inline DispatchResult parse_RangeInline(const jsoncons::json& raw) {
    if (!raw.contains("_type")) {
        return DispatchResult{nullptr, RuleCatalog::make_problem("Range-0004", "")};
    }
    std::string tv = raw.at("_type").as<std::string>();
    std::unique_ptr<SedBase> obj;
    if (tv == "numericRange") obj = std::make_unique<NumericRange>();
    else if (tv == "parameterRange") obj = std::make_unique<ParameterRange>();
    else if (tv == "range") obj = std::make_unique<Range>();
    if (obj) {
        load_fields(obj.get(), raw);
        return DispatchResult{std::move(obj), std::nullopt};
    }
    std::smatch m;
    bool ns_match = std::regex_match(tv, m, namespace_key_pattern());
    static const std::set<std::string> known = {};
    if (ns_match && !known.count(m[1].str())) {
        return DispatchResult{std::make_unique<UnknownRangeInline>(tv, raw), std::nullopt};
    }
    std::map<std::string, std::string> ph;
    ph["schema-message"] = "unrecognized _type '" + tv + "'";
    return DispatchResult{std::make_unique<UnknownRangeInline>(tv, raw), RuleCatalog::make_problem("RangeInline-0000", "", ph)};
}

inline DispatchResult parse_AbstractOutput(const jsoncons::json& raw) {
    if (!raw.contains("_type")) {
        return DispatchResult{nullptr, RuleCatalog::make_problem("AbstractOutput-0002", "")};
    }
    std::string tv = raw.at("_type").as<std::string>();
    std::unique_ptr<SedBase> obj;
    if (tv == "plot2D") obj = std::make_unique<Plot2D>();
    else if (tv == "plot3D") obj = std::make_unique<Plot3D>();
    else if (tv == "report") obj = std::make_unique<Report>();
    if (obj) {
        load_fields(obj.get(), raw);
        return DispatchResult{std::move(obj), std::nullopt};
    }
    std::smatch m;
    bool ns_match = std::regex_match(tv, m, namespace_key_pattern());
    static const std::set<std::string> known = {};
    if (ns_match && !known.count(m[1].str())) {
        return DispatchResult{std::make_unique<UnknownAbstractOutput>(tv, raw), std::nullopt};
    }
    std::map<std::string, std::string> ph;
    ph["schema-message"] = "unrecognized _type '" + tv + "'";
    return DispatchResult{std::make_unique<UnknownAbstractOutput>(tv, raw), RuleCatalog::make_problem("AbstractOutput-0000", "", ph)};
}

inline DispatchResult parse_AbstractCurve(const jsoncons::json& raw) {
    if (!raw.contains("_type")) {
        return DispatchResult{nullptr, RuleCatalog::make_problem("AbstractCurve-0008", "")};
    }
    std::string tv = raw.at("_type").as<std::string>();
    std::unique_ptr<SedBase> obj;
    if (tv == "curve") obj = std::make_unique<Curve>();
    if (obj) {
        load_fields(obj.get(), raw);
        return DispatchResult{std::move(obj), std::nullopt};
    }
    std::smatch m;
    bool ns_match = std::regex_match(tv, m, namespace_key_pattern());
    static const std::set<std::string> known = {};
    if (ns_match && !known.count(m[1].str())) {
        return DispatchResult{std::make_unique<UnknownAbstractCurve>(tv, raw), std::nullopt};
    }
    std::map<std::string, std::string> ph;
    ph["schema-message"] = "unrecognized _type '" + tv + "'";
    return DispatchResult{std::make_unique<UnknownAbstractCurve>(tv, raw), RuleCatalog::make_problem("AbstractCurve-0000", "", ph)};
}

inline DispatchResult dispatch_parse(const std::string& disc_name, const jsoncons::json& raw) {
    if (disc_name == "AbstractTask") return parse_AbstractTask(raw);
    else if (disc_name == "RangeInline") return parse_RangeInline(raw);
    else if (disc_name == "AbstractOutput") return parse_AbstractOutput(raw);
    else if (disc_name == "AbstractCurve") return parse_AbstractCurve(raw);
    throw ApiError("unknown discriminator " + disc_name);
}

inline std::unique_ptr<SedBase> new_item_instance(const std::string& class_name) {
    if (class_name == "Annotation") return std::make_unique<Annotation>();
    else if (class_name == "OutputParameter") return std::make_unique<OutputParameter>();
    else if (class_name == "ParameterRange") return std::make_unique<ParameterRange>();
    else if (class_name == "TaskParameter") return std::make_unique<TaskParameter>();
    else if (class_name == "WorkingAlgorithm") return std::make_unique<WorkingAlgorithm>();
    throw ApiError("unknown item class " + class_name);
}

inline void load_fields(SedBase* obj, const jsoncons::json& raw) {
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

}  // namespace libsed2

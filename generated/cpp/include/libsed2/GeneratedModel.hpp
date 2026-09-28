// Generated concrete SED2 classes. GENERATED - do not
// hand-edit; regenerate from test-specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"

#include <memory>
#include <string>
#include <vector>

namespace libsed2 {

/// Generated from test-specsheets/core/SEDDocument/.
class SEDDocument : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"version", "string", true, std::string("SEDDocument-0002"), std::string("SEDDocument-0001"), "SEDDocument-0000", std::nullopt, std::nullopt, std::string("^v\\d+\\.\\d+\\.\\d+$"), std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"constants", "any-dict", false, std::string("SEDDocument-0005"), std::nullopt, "SEDDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"tasks", "dict", false, std::string("SEDDocument-0006"), std::nullopt, "SEDDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractTask")},
            FieldSpec{"outputs", "dict", false, std::string("SEDDocument-0007"), std::nullopt, "SEDDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractOutput")},
            FieldSpec{"styles", "dict", false, std::string("SEDDocument-0008"), std::nullopt, "SEDDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Style"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"version"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "SEDDocument-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "SEDDocument"; }

    std::string get_version() const { auto it = values_.find("version"); if (it == values_.end()) throw ApiError(std::string("version") + " is not set"); return it->second.as<std::string>(); }
    void set_version(const std::string& value) { values_["version"] = jsoncons::json(value); }
    bool is_set_version() const { return values_.count("version") > 0; }
    void unset_version() { values_.erase("version"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<std::string> get_constants() const { return constants_.ids(); }
    jsoncons::json get_constants_item(const std::string& item_id) const { return constants_.get(item_id); }
    void add_constants(const std::string& item_id, const jsoncons::json& value) { constants_.add(item_id, value); }
    void insert_constants(size_t index, const std::string& item_id, const jsoncons::json& value) { constants_.insert(index, item_id, value); }
    void remove_constants(const std::string& item_id) { constants_.remove(item_id); }
    void set_id_on_constants(const std::string& old_id, const std::string& new_id) { constants_.set_id(old_id, new_id); }

    std::vector<std::string> get_tasks() const { return tasks_.ids(); }
    SedBase* get_tasks_item(const std::string& item_id) const { return tasks_.get(item_id); }
    void add_tasks(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); tasks_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_tasks(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); tasks_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_tasks(const std::string& item_id) { tasks_.remove(item_id); }
    void set_id_on_tasks(const std::string& old_id, const std::string& new_id) { tasks_.set_id(old_id, new_id); }

    std::vector<std::string> get_outputs() const { return outputs_.ids(); }
    SedBase* get_outputs_item(const std::string& item_id) const { return outputs_.get(item_id); }
    void add_outputs(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputs_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_outputs(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputs_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_outputs(const std::string& item_id) { outputs_.remove(item_id); }
    void set_id_on_outputs(const std::string& old_id, const std::string& new_id) { outputs_.set_id(old_id, new_id); }

    std::vector<std::string> get_styles() const { return styles_.ids(); }
    SedBase* get_styles_item(const std::string& item_id) const { return styles_.get(item_id); }
    void add_styles(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); styles_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_styles(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); styles_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_styles(const std::string& item_id) { styles_.remove(item_id); }
    void set_id_on_styles(const std::string& old_id, const std::string& new_id) { styles_.set_id(old_id, new_id); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : tasks_.ids()) kids.push_back(tasks_.get(i));
        for (const auto& i : outputs_.ids()) kids.push_back(outputs_.get(i));
        for (const auto& i : styles_.ids()) kids.push_back(styles_.get(i));
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : tasks_.ids()) out.push_back(ChildLoc{tasks_.get(i), "/tasks/" + i});
        for (const auto& i : outputs_.ids()) out.push_back(ChildLoc{outputs_.get(i), "/outputs/" + i});
        for (const auto& i : styles_.ids()) out.push_back(ChildLoc{styles_.get(i), "/styles/" + i});
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "tasks") return tasks_;
        if (field_name == "outputs") return outputs_;
        if (field_name == "styles") return styles_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    AnyDictCollection& get_any_dict_collection(const std::string& field_name) override {
        if (field_name == "constants") return constants_;
        return SedBase::get_any_dict_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("version")) d["version"] = values_.at("version");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (tasks_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : tasks_.ids()) sub[i] = tasks_.get(i)->to_json_value(); d["tasks"] = sub; }
        if (outputs_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : outputs_.ids()) sub[i] = outputs_.get(i)->to_json_value(); d["outputs"] = sub; }
        if (styles_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : styles_.ids()) sub[i] = styles_.get(i)->to_json_value(); d["styles"] = sub; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (constants_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : constants_.ids()) sub[i] = constants_.get(i); d["constants"] = sub; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    AnyDictCollection constants_;
    IdKeyedCollection tasks_;
    IdKeyedCollection outputs_;
    IdKeyedCollection styles_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/core/Style/.
class Style : public SedBase {
public:
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "Style-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Style"; }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/tasks/AggregationCalculation/.
class AggregationCalculation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"input", "any", true, std::nullopt, std::string("AggregationCalculation-0001"), "AggregationCalculation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"appliedDimensions", "ArrayOrRef", false, std::string("AggregationCalculation-0002"), std::nullopt, "AggregationCalculation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"input"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("aggregationCalculation"); }
    std::optional<std::string> type_rule_id() const override { return std::string("AggregationCalculation-0004"); }
    std::string own_catchall() const override { return "AggregationCalculation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "AggregationCalculation"; }
    std::string get_type() const { return "aggregationCalculation"; }

    jsoncons::json get_input() const { auto it = values_.find("input"); if (it == values_.end()) throw ApiError(std::string("input") + " is not set"); return it->second; }
    void set_input(const jsoncons::json& value) { values_["input"] = value; }
    bool is_set_input() const { return values_.count("input") > 0; }
    void unset_input() { values_.erase("input"); }

    jsoncons::json get_appliedDimensions_value() const { return get_or_ref_value_node("appliedDimensions"); }
    std::string get_appliedDimensions_ref() const { return get_or_ref_ref_node("appliedDimensions").as<std::string>(); }
    void set_appliedDimensions_value(const jsoncons::json& value) { set_or_ref_value_node("appliedDimensions", value); }
    void set_appliedDimensions_ref(const std::string& ref) { set_or_ref_ref_node("appliedDimensions", ref); }
    bool is_appliedDimensions_ref() const { return is_or_ref_ref("appliedDimensions"); }
    bool is_set_appliedDimensions() const { return values_.count("appliedDimensions") > 0; }
    void unset_appliedDimensions() { values_.erase("appliedDimensions"); or_ref_is_ref_.erase("appliedDimensions"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("aggregationCalculation");
        if (values_.count("input")) d["input"] = values_.at("input");
        if (values_.count("appliedDimensions")) d["appliedDimensions"] = values_.at("appliedDimensions");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/BoundedODESimulation/.
class BoundedODESimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"relativeTolerance", "NumberOrRef", false, std::string("AbstractODESimulation-0001"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteTolerance", "NumberOrRef", false, std::string("AbstractODESimulation-0003"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceVector", "ArrayOrRef", false, std::string("AbstractODESimulation-0005"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceAdjustmentFactor", "NumberOrRef", false, std::string("AbstractODESimulation-0007"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"toleranceForRootFinder", "NumberOrRef", false, std::string("AbstractODESimulation-0009"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"initialStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0011"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumberOfSteps", "NumberOrRef", false, std::string("AbstractODESimulation-0013"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalSteps", "IntegerOrRef", false, std::string("AbstractODESimulation-0015"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0017"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minInternalStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0019"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"forcePhysicalCorrectness", "BooleanOrRef", false, std::string("AbstractODESimulation-0021"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"integrateReducedModel", "BooleanOrRef", false, std::string("AbstractODESimulation-0023"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"useReducedModel", "BooleanOrRef", false, std::string("AbstractODESimulation-0025"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"useStiffSolver", "BooleanOrRef", false, std::string("AbstractODESimulation-0027"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxBDForder", "IntegerOrRef", false, std::string("AbstractODESimulation-0029"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxAdamsOrder", "IntegerOrRef", false, std::string("AbstractODESimulation-0031"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"variableStepSize", "BooleanOrRef", false, std::string("AbstractODESimulation-0033"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxOutputRows", "IntegerOrRef", false, std::string("AbstractODESimulation-0035"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string("AbstractSimulation-0002"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string("AbstractSimulation-0004"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariables", "ArrayOrRef", false, std::string("AbstractSimulation-0006"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"independentVariableSpan", "ref-class", true, std::string("BoundedODESimulation-0005"), std::string("BoundedODESimulation-0004"), "BoundedODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Span"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"independentVariableSpan"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("boundedODESimulation"); }
    std::optional<std::string> type_rule_id() const override { return std::string("BoundedODESimulation-0006"); }
    std::string own_catchall() const override { return "BoundedODESimulation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "BoundedODESimulation"; }
    std::string get_type() const { return "boundedODESimulation"; }

    double get_relativeTolerance_value() const { return get_or_ref_value_node("relativeTolerance").as<double>(); }
    std::string get_relativeTolerance_ref() const { return get_or_ref_ref_node("relativeTolerance").as<std::string>(); }
    void set_relativeTolerance_value(double value) { set_or_ref_value_node("relativeTolerance", jsoncons::json(value)); }
    void set_relativeTolerance_ref(const std::string& ref) { set_or_ref_ref_node("relativeTolerance", ref); }
    bool is_relativeTolerance_ref() const { return is_or_ref_ref("relativeTolerance"); }
    bool is_set_relativeTolerance() const { return values_.count("relativeTolerance") > 0; }
    void unset_relativeTolerance() { values_.erase("relativeTolerance"); or_ref_is_ref_.erase("relativeTolerance"); }

    double get_absoluteTolerance_value() const { return get_or_ref_value_node("absoluteTolerance").as<double>(); }
    std::string get_absoluteTolerance_ref() const { return get_or_ref_ref_node("absoluteTolerance").as<std::string>(); }
    void set_absoluteTolerance_value(double value) { set_or_ref_value_node("absoluteTolerance", jsoncons::json(value)); }
    void set_absoluteTolerance_ref(const std::string& ref) { set_or_ref_ref_node("absoluteTolerance", ref); }
    bool is_absoluteTolerance_ref() const { return is_or_ref_ref("absoluteTolerance"); }
    bool is_set_absoluteTolerance() const { return values_.count("absoluteTolerance") > 0; }
    void unset_absoluteTolerance() { values_.erase("absoluteTolerance"); or_ref_is_ref_.erase("absoluteTolerance"); }

    jsoncons::json get_absoluteToleranceVector_value() const { return get_or_ref_value_node("absoluteToleranceVector"); }
    std::string get_absoluteToleranceVector_ref() const { return get_or_ref_ref_node("absoluteToleranceVector").as<std::string>(); }
    void set_absoluteToleranceVector_value(const jsoncons::json& value) { set_or_ref_value_node("absoluteToleranceVector", value); }
    void set_absoluteToleranceVector_ref(const std::string& ref) { set_or_ref_ref_node("absoluteToleranceVector", ref); }
    bool is_absoluteToleranceVector_ref() const { return is_or_ref_ref("absoluteToleranceVector"); }
    bool is_set_absoluteToleranceVector() const { return values_.count("absoluteToleranceVector") > 0; }
    void unset_absoluteToleranceVector() { values_.erase("absoluteToleranceVector"); or_ref_is_ref_.erase("absoluteToleranceVector"); }

    double get_absoluteToleranceAdjustmentFactor_value() const { return get_or_ref_value_node("absoluteToleranceAdjustmentFactor").as<double>(); }
    std::string get_absoluteToleranceAdjustmentFactor_ref() const { return get_or_ref_ref_node("absoluteToleranceAdjustmentFactor").as<std::string>(); }
    void set_absoluteToleranceAdjustmentFactor_value(double value) { set_or_ref_value_node("absoluteToleranceAdjustmentFactor", jsoncons::json(value)); }
    void set_absoluteToleranceAdjustmentFactor_ref(const std::string& ref) { set_or_ref_ref_node("absoluteToleranceAdjustmentFactor", ref); }
    bool is_absoluteToleranceAdjustmentFactor_ref() const { return is_or_ref_ref("absoluteToleranceAdjustmentFactor"); }
    bool is_set_absoluteToleranceAdjustmentFactor() const { return values_.count("absoluteToleranceAdjustmentFactor") > 0; }
    void unset_absoluteToleranceAdjustmentFactor() { values_.erase("absoluteToleranceAdjustmentFactor"); or_ref_is_ref_.erase("absoluteToleranceAdjustmentFactor"); }

    double get_toleranceForRootFinder_value() const { return get_or_ref_value_node("toleranceForRootFinder").as<double>(); }
    std::string get_toleranceForRootFinder_ref() const { return get_or_ref_ref_node("toleranceForRootFinder").as<std::string>(); }
    void set_toleranceForRootFinder_value(double value) { set_or_ref_value_node("toleranceForRootFinder", jsoncons::json(value)); }
    void set_toleranceForRootFinder_ref(const std::string& ref) { set_or_ref_ref_node("toleranceForRootFinder", ref); }
    bool is_toleranceForRootFinder_ref() const { return is_or_ref_ref("toleranceForRootFinder"); }
    bool is_set_toleranceForRootFinder() const { return values_.count("toleranceForRootFinder") > 0; }
    void unset_toleranceForRootFinder() { values_.erase("toleranceForRootFinder"); or_ref_is_ref_.erase("toleranceForRootFinder"); }

    double get_initialStepSize_value() const { return get_or_ref_value_node("initialStepSize").as<double>(); }
    std::string get_initialStepSize_ref() const { return get_or_ref_ref_node("initialStepSize").as<std::string>(); }
    void set_initialStepSize_value(double value) { set_or_ref_value_node("initialStepSize", jsoncons::json(value)); }
    void set_initialStepSize_ref(const std::string& ref) { set_or_ref_ref_node("initialStepSize", ref); }
    bool is_initialStepSize_ref() const { return is_or_ref_ref("initialStepSize"); }
    bool is_set_initialStepSize() const { return values_.count("initialStepSize") > 0; }
    void unset_initialStepSize() { values_.erase("initialStepSize"); or_ref_is_ref_.erase("initialStepSize"); }

    double get_maxNumberOfSteps_value() const { return get_or_ref_value_node("maxNumberOfSteps").as<double>(); }
    std::string get_maxNumberOfSteps_ref() const { return get_or_ref_ref_node("maxNumberOfSteps").as<std::string>(); }
    void set_maxNumberOfSteps_value(double value) { set_or_ref_value_node("maxNumberOfSteps", jsoncons::json(value)); }
    void set_maxNumberOfSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxNumberOfSteps", ref); }
    bool is_maxNumberOfSteps_ref() const { return is_or_ref_ref("maxNumberOfSteps"); }
    bool is_set_maxNumberOfSteps() const { return values_.count("maxNumberOfSteps") > 0; }
    void unset_maxNumberOfSteps() { values_.erase("maxNumberOfSteps"); or_ref_is_ref_.erase("maxNumberOfSteps"); }

    int64_t get_maxInternalSteps_value() const { return get_or_ref_value_node("maxInternalSteps").as<int64_t>(); }
    std::string get_maxInternalSteps_ref() const { return get_or_ref_ref_node("maxInternalSteps").as<std::string>(); }
    void set_maxInternalSteps_value(int64_t value) { set_or_ref_value_node("maxInternalSteps", jsoncons::json(value)); }
    void set_maxInternalSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxInternalSteps", ref); }
    bool is_maxInternalSteps_ref() const { return is_or_ref_ref("maxInternalSteps"); }
    bool is_set_maxInternalSteps() const { return values_.count("maxInternalSteps") > 0; }
    void unset_maxInternalSteps() { values_.erase("maxInternalSteps"); or_ref_is_ref_.erase("maxInternalSteps"); }

    double get_maxInternalStepSize_value() const { return get_or_ref_value_node("maxInternalStepSize").as<double>(); }
    std::string get_maxInternalStepSize_ref() const { return get_or_ref_ref_node("maxInternalStepSize").as<std::string>(); }
    void set_maxInternalStepSize_value(double value) { set_or_ref_value_node("maxInternalStepSize", jsoncons::json(value)); }
    void set_maxInternalStepSize_ref(const std::string& ref) { set_or_ref_ref_node("maxInternalStepSize", ref); }
    bool is_maxInternalStepSize_ref() const { return is_or_ref_ref("maxInternalStepSize"); }
    bool is_set_maxInternalStepSize() const { return values_.count("maxInternalStepSize") > 0; }
    void unset_maxInternalStepSize() { values_.erase("maxInternalStepSize"); or_ref_is_ref_.erase("maxInternalStepSize"); }

    double get_minInternalStepSize_value() const { return get_or_ref_value_node("minInternalStepSize").as<double>(); }
    std::string get_minInternalStepSize_ref() const { return get_or_ref_ref_node("minInternalStepSize").as<std::string>(); }
    void set_minInternalStepSize_value(double value) { set_or_ref_value_node("minInternalStepSize", jsoncons::json(value)); }
    void set_minInternalStepSize_ref(const std::string& ref) { set_or_ref_ref_node("minInternalStepSize", ref); }
    bool is_minInternalStepSize_ref() const { return is_or_ref_ref("minInternalStepSize"); }
    bool is_set_minInternalStepSize() const { return values_.count("minInternalStepSize") > 0; }
    void unset_minInternalStepSize() { values_.erase("minInternalStepSize"); or_ref_is_ref_.erase("minInternalStepSize"); }

    bool get_forcePhysicalCorrectness_value() const { return get_or_ref_value_node("forcePhysicalCorrectness").as<bool>(); }
    std::string get_forcePhysicalCorrectness_ref() const { return get_or_ref_ref_node("forcePhysicalCorrectness").as<std::string>(); }
    void set_forcePhysicalCorrectness_value(bool value) { set_or_ref_value_node("forcePhysicalCorrectness", jsoncons::json(value)); }
    void set_forcePhysicalCorrectness_ref(const std::string& ref) { set_or_ref_ref_node("forcePhysicalCorrectness", ref); }
    bool is_forcePhysicalCorrectness_ref() const { return is_or_ref_ref("forcePhysicalCorrectness"); }
    bool is_set_forcePhysicalCorrectness() const { return values_.count("forcePhysicalCorrectness") > 0; }
    void unset_forcePhysicalCorrectness() { values_.erase("forcePhysicalCorrectness"); or_ref_is_ref_.erase("forcePhysicalCorrectness"); }

    bool get_integrateReducedModel_value() const { return get_or_ref_value_node("integrateReducedModel").as<bool>(); }
    std::string get_integrateReducedModel_ref() const { return get_or_ref_ref_node("integrateReducedModel").as<std::string>(); }
    void set_integrateReducedModel_value(bool value) { set_or_ref_value_node("integrateReducedModel", jsoncons::json(value)); }
    void set_integrateReducedModel_ref(const std::string& ref) { set_or_ref_ref_node("integrateReducedModel", ref); }
    bool is_integrateReducedModel_ref() const { return is_or_ref_ref("integrateReducedModel"); }
    bool is_set_integrateReducedModel() const { return values_.count("integrateReducedModel") > 0; }
    void unset_integrateReducedModel() { values_.erase("integrateReducedModel"); or_ref_is_ref_.erase("integrateReducedModel"); }

    bool get_useReducedModel_value() const { return get_or_ref_value_node("useReducedModel").as<bool>(); }
    std::string get_useReducedModel_ref() const { return get_or_ref_ref_node("useReducedModel").as<std::string>(); }
    void set_useReducedModel_value(bool value) { set_or_ref_value_node("useReducedModel", jsoncons::json(value)); }
    void set_useReducedModel_ref(const std::string& ref) { set_or_ref_ref_node("useReducedModel", ref); }
    bool is_useReducedModel_ref() const { return is_or_ref_ref("useReducedModel"); }
    bool is_set_useReducedModel() const { return values_.count("useReducedModel") > 0; }
    void unset_useReducedModel() { values_.erase("useReducedModel"); or_ref_is_ref_.erase("useReducedModel"); }

    bool get_useStiffSolver_value() const { return get_or_ref_value_node("useStiffSolver").as<bool>(); }
    std::string get_useStiffSolver_ref() const { return get_or_ref_ref_node("useStiffSolver").as<std::string>(); }
    void set_useStiffSolver_value(bool value) { set_or_ref_value_node("useStiffSolver", jsoncons::json(value)); }
    void set_useStiffSolver_ref(const std::string& ref) { set_or_ref_ref_node("useStiffSolver", ref); }
    bool is_useStiffSolver_ref() const { return is_or_ref_ref("useStiffSolver"); }
    bool is_set_useStiffSolver() const { return values_.count("useStiffSolver") > 0; }
    void unset_useStiffSolver() { values_.erase("useStiffSolver"); or_ref_is_ref_.erase("useStiffSolver"); }

    int64_t get_maxBDForder_value() const { return get_or_ref_value_node("maxBDForder").as<int64_t>(); }
    std::string get_maxBDForder_ref() const { return get_or_ref_ref_node("maxBDForder").as<std::string>(); }
    void set_maxBDForder_value(int64_t value) { set_or_ref_value_node("maxBDForder", jsoncons::json(value)); }
    void set_maxBDForder_ref(const std::string& ref) { set_or_ref_ref_node("maxBDForder", ref); }
    bool is_maxBDForder_ref() const { return is_or_ref_ref("maxBDForder"); }
    bool is_set_maxBDForder() const { return values_.count("maxBDForder") > 0; }
    void unset_maxBDForder() { values_.erase("maxBDForder"); or_ref_is_ref_.erase("maxBDForder"); }

    int64_t get_maxAdamsOrder_value() const { return get_or_ref_value_node("maxAdamsOrder").as<int64_t>(); }
    std::string get_maxAdamsOrder_ref() const { return get_or_ref_ref_node("maxAdamsOrder").as<std::string>(); }
    void set_maxAdamsOrder_value(int64_t value) { set_or_ref_value_node("maxAdamsOrder", jsoncons::json(value)); }
    void set_maxAdamsOrder_ref(const std::string& ref) { set_or_ref_ref_node("maxAdamsOrder", ref); }
    bool is_maxAdamsOrder_ref() const { return is_or_ref_ref("maxAdamsOrder"); }
    bool is_set_maxAdamsOrder() const { return values_.count("maxAdamsOrder") > 0; }
    void unset_maxAdamsOrder() { values_.erase("maxAdamsOrder"); or_ref_is_ref_.erase("maxAdamsOrder"); }

    bool get_variableStepSize_value() const { return get_or_ref_value_node("variableStepSize").as<bool>(); }
    std::string get_variableStepSize_ref() const { return get_or_ref_ref_node("variableStepSize").as<std::string>(); }
    void set_variableStepSize_value(bool value) { set_or_ref_value_node("variableStepSize", jsoncons::json(value)); }
    void set_variableStepSize_ref(const std::string& ref) { set_or_ref_ref_node("variableStepSize", ref); }
    bool is_variableStepSize_ref() const { return is_or_ref_ref("variableStepSize"); }
    bool is_set_variableStepSize() const { return values_.count("variableStepSize") > 0; }
    void unset_variableStepSize() { values_.erase("variableStepSize"); or_ref_is_ref_.erase("variableStepSize"); }

    int64_t get_maxOutputRows_value() const { return get_or_ref_value_node("maxOutputRows").as<int64_t>(); }
    std::string get_maxOutputRows_ref() const { return get_or_ref_ref_node("maxOutputRows").as<std::string>(); }
    void set_maxOutputRows_value(int64_t value) { set_or_ref_value_node("maxOutputRows", jsoncons::json(value)); }
    void set_maxOutputRows_ref(const std::string& ref) { set_or_ref_ref_node("maxOutputRows", ref); }
    bool is_maxOutputRows_ref() const { return is_or_ref_ref("maxOutputRows"); }
    bool is_set_maxOutputRows() const { return values_.count("maxOutputRows") > 0; }
    void unset_maxOutputRows() { values_.erase("maxOutputRows"); or_ref_is_ref_.erase("maxOutputRows"); }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    std::string get_independentVariable_value() const { return get_or_ref_value_node("independentVariable").as<std::string>(); }
    std::string get_independentVariable_ref() const { return get_or_ref_ref_node("independentVariable").as<std::string>(); }
    void set_independentVariable_value(const std::string& value) { set_or_ref_value_node("independentVariable", jsoncons::json(value)); }
    void set_independentVariable_ref(const std::string& ref) { set_or_ref_ref_node("independentVariable", ref); }
    bool is_independentVariable_ref() const { return is_or_ref_ref("independentVariable"); }
    bool is_set_independentVariable() const { return values_.count("independentVariable") > 0; }
    void unset_independentVariable() { values_.erase("independentVariable"); or_ref_is_ref_.erase("independentVariable"); }

    double get_independentVariableInit_value() const { return get_or_ref_value_node("independentVariableInit").as<double>(); }
    std::string get_independentVariableInit_ref() const { return get_or_ref_ref_node("independentVariableInit").as<std::string>(); }
    void set_independentVariableInit_value(double value) { set_or_ref_value_node("independentVariableInit", jsoncons::json(value)); }
    void set_independentVariableInit_ref(const std::string& ref) { set_or_ref_ref_node("independentVariableInit", ref); }
    bool is_independentVariableInit_ref() const { return is_or_ref_ref("independentVariableInit"); }
    bool is_set_independentVariableInit() const { return values_.count("independentVariableInit") > 0; }
    void unset_independentVariableInit() { values_.erase("independentVariableInit"); or_ref_is_ref_.erase("independentVariableInit"); }

    jsoncons::json get_outputVariables_value() const { return get_or_ref_value_node("outputVariables"); }
    std::string get_outputVariables_ref() const { return get_or_ref_ref_node("outputVariables").as<std::string>(); }
    void set_outputVariables_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariables", value); }
    void set_outputVariables_ref(const std::string& ref) { set_or_ref_ref_node("outputVariables", ref); }
    bool is_outputVariables_ref() const { return is_or_ref_ref("outputVariables"); }
    bool is_set_outputVariables() const { return values_.count("outputVariables") > 0; }
    void unset_outputVariables() { values_.erase("outputVariables"); or_ref_is_ref_.erase("outputVariables"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_independentVariableSpan() const { if (!independentVariableSpan_) throw ApiError(std::string("independentVariableSpan") + " is not set"); return independentVariableSpan_.get(); }
    void set_independentVariableSpan(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); independentVariableSpan_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_independentVariableSpan() const { return independentVariableSpan_ != nullptr; }
    void unset_independentVariableSpan() { independentVariableSpan_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (independentVariableSpan_) kids.push_back(independentVariableSpan_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (independentVariableSpan_) out.push_back(ChildLoc{independentVariableSpan_.get(), "/independentVariableSpan"});
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "independentVariableSpan") { independentVariableSpan_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("boundedODESimulation");
        if (values_.count("relativeTolerance")) d["relativeTolerance"] = values_.at("relativeTolerance");
        if (values_.count("absoluteTolerance")) d["absoluteTolerance"] = values_.at("absoluteTolerance");
        if (values_.count("absoluteToleranceVector")) d["absoluteToleranceVector"] = values_.at("absoluteToleranceVector");
        if (values_.count("absoluteToleranceAdjustmentFactor")) d["absoluteToleranceAdjustmentFactor"] = values_.at("absoluteToleranceAdjustmentFactor");
        if (values_.count("toleranceForRootFinder")) d["toleranceForRootFinder"] = values_.at("toleranceForRootFinder");
        if (values_.count("initialStepSize")) d["initialStepSize"] = values_.at("initialStepSize");
        if (values_.count("maxNumberOfSteps")) d["maxNumberOfSteps"] = values_.at("maxNumberOfSteps");
        if (values_.count("maxInternalSteps")) d["maxInternalSteps"] = values_.at("maxInternalSteps");
        if (values_.count("maxInternalStepSize")) d["maxInternalStepSize"] = values_.at("maxInternalStepSize");
        if (values_.count("minInternalStepSize")) d["minInternalStepSize"] = values_.at("minInternalStepSize");
        if (values_.count("forcePhysicalCorrectness")) d["forcePhysicalCorrectness"] = values_.at("forcePhysicalCorrectness");
        if (values_.count("integrateReducedModel")) d["integrateReducedModel"] = values_.at("integrateReducedModel");
        if (values_.count("useReducedModel")) d["useReducedModel"] = values_.at("useReducedModel");
        if (values_.count("useStiffSolver")) d["useStiffSolver"] = values_.at("useStiffSolver");
        if (values_.count("maxBDForder")) d["maxBDForder"] = values_.at("maxBDForder");
        if (values_.count("maxAdamsOrder")) d["maxAdamsOrder"] = values_.at("maxAdamsOrder");
        if (values_.count("variableStepSize")) d["variableStepSize"] = values_.at("variableStepSize");
        if (values_.count("maxOutputRows")) d["maxOutputRows"] = values_.at("maxOutputRows");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (values_.count("outputVariables")) d["outputVariables"] = values_.at("outputVariables");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (independentVariableSpan_) d["independentVariableSpan"] = independentVariableSpan_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> independentVariableSpan_;
};

/// Generated from test-specsheets/tasks/BoundedStochasticSimulation/.
class BoundedStochasticSimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"seed", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0001"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"timeDependentRelativeTolerance", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0003"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"variableStepSize", "BooleanOrRef", false, std::string("AbstractStochasticSimulation-0005"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minimumTimeStep", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0007"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maximumTimeStep", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0009"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"nonNegative", "BooleanOrRef", false, std::string("AbstractStochasticSimulation-0011"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxOutputRows", "IntegerOrRef", false, std::string("AbstractStochasticSimulation-0013"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumSteps", "IntegerOrRef", false, std::string("AbstractStochasticSimulation-0015"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string("AbstractSimulation-0002"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string("AbstractSimulation-0004"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariables", "ArrayOrRef", false, std::string("AbstractSimulation-0006"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"independentVariableSpan", "ref-class", true, std::string("BoundedStochasticSimulation-0005"), std::string("BoundedStochasticSimulation-0004"), "BoundedStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Span"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"independentVariableSpan"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("boundedStochasticSimulation"); }
    std::optional<std::string> type_rule_id() const override { return std::string("BoundedStochasticSimulation-0006"); }
    std::string own_catchall() const override { return "BoundedStochasticSimulation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "BoundedStochasticSimulation"; }
    std::string get_type() const { return "boundedStochasticSimulation"; }

    double get_seed_value() const { return get_or_ref_value_node("seed").as<double>(); }
    std::string get_seed_ref() const { return get_or_ref_ref_node("seed").as<std::string>(); }
    void set_seed_value(double value) { set_or_ref_value_node("seed", jsoncons::json(value)); }
    void set_seed_ref(const std::string& ref) { set_or_ref_ref_node("seed", ref); }
    bool is_seed_ref() const { return is_or_ref_ref("seed"); }
    bool is_set_seed() const { return values_.count("seed") > 0; }
    void unset_seed() { values_.erase("seed"); or_ref_is_ref_.erase("seed"); }

    double get_timeDependentRelativeTolerance_value() const { return get_or_ref_value_node("timeDependentRelativeTolerance").as<double>(); }
    std::string get_timeDependentRelativeTolerance_ref() const { return get_or_ref_ref_node("timeDependentRelativeTolerance").as<std::string>(); }
    void set_timeDependentRelativeTolerance_value(double value) { set_or_ref_value_node("timeDependentRelativeTolerance", jsoncons::json(value)); }
    void set_timeDependentRelativeTolerance_ref(const std::string& ref) { set_or_ref_ref_node("timeDependentRelativeTolerance", ref); }
    bool is_timeDependentRelativeTolerance_ref() const { return is_or_ref_ref("timeDependentRelativeTolerance"); }
    bool is_set_timeDependentRelativeTolerance() const { return values_.count("timeDependentRelativeTolerance") > 0; }
    void unset_timeDependentRelativeTolerance() { values_.erase("timeDependentRelativeTolerance"); or_ref_is_ref_.erase("timeDependentRelativeTolerance"); }

    bool get_variableStepSize_value() const { return get_or_ref_value_node("variableStepSize").as<bool>(); }
    std::string get_variableStepSize_ref() const { return get_or_ref_ref_node("variableStepSize").as<std::string>(); }
    void set_variableStepSize_value(bool value) { set_or_ref_value_node("variableStepSize", jsoncons::json(value)); }
    void set_variableStepSize_ref(const std::string& ref) { set_or_ref_ref_node("variableStepSize", ref); }
    bool is_variableStepSize_ref() const { return is_or_ref_ref("variableStepSize"); }
    bool is_set_variableStepSize() const { return values_.count("variableStepSize") > 0; }
    void unset_variableStepSize() { values_.erase("variableStepSize"); or_ref_is_ref_.erase("variableStepSize"); }

    double get_minimumTimeStep_value() const { return get_or_ref_value_node("minimumTimeStep").as<double>(); }
    std::string get_minimumTimeStep_ref() const { return get_or_ref_ref_node("minimumTimeStep").as<std::string>(); }
    void set_minimumTimeStep_value(double value) { set_or_ref_value_node("minimumTimeStep", jsoncons::json(value)); }
    void set_minimumTimeStep_ref(const std::string& ref) { set_or_ref_ref_node("minimumTimeStep", ref); }
    bool is_minimumTimeStep_ref() const { return is_or_ref_ref("minimumTimeStep"); }
    bool is_set_minimumTimeStep() const { return values_.count("minimumTimeStep") > 0; }
    void unset_minimumTimeStep() { values_.erase("minimumTimeStep"); or_ref_is_ref_.erase("minimumTimeStep"); }

    double get_maximumTimeStep_value() const { return get_or_ref_value_node("maximumTimeStep").as<double>(); }
    std::string get_maximumTimeStep_ref() const { return get_or_ref_ref_node("maximumTimeStep").as<std::string>(); }
    void set_maximumTimeStep_value(double value) { set_or_ref_value_node("maximumTimeStep", jsoncons::json(value)); }
    void set_maximumTimeStep_ref(const std::string& ref) { set_or_ref_ref_node("maximumTimeStep", ref); }
    bool is_maximumTimeStep_ref() const { return is_or_ref_ref("maximumTimeStep"); }
    bool is_set_maximumTimeStep() const { return values_.count("maximumTimeStep") > 0; }
    void unset_maximumTimeStep() { values_.erase("maximumTimeStep"); or_ref_is_ref_.erase("maximumTimeStep"); }

    bool get_nonNegative_value() const { return get_or_ref_value_node("nonNegative").as<bool>(); }
    std::string get_nonNegative_ref() const { return get_or_ref_ref_node("nonNegative").as<std::string>(); }
    void set_nonNegative_value(bool value) { set_or_ref_value_node("nonNegative", jsoncons::json(value)); }
    void set_nonNegative_ref(const std::string& ref) { set_or_ref_ref_node("nonNegative", ref); }
    bool is_nonNegative_ref() const { return is_or_ref_ref("nonNegative"); }
    bool is_set_nonNegative() const { return values_.count("nonNegative") > 0; }
    void unset_nonNegative() { values_.erase("nonNegative"); or_ref_is_ref_.erase("nonNegative"); }

    int64_t get_maxOutputRows_value() const { return get_or_ref_value_node("maxOutputRows").as<int64_t>(); }
    std::string get_maxOutputRows_ref() const { return get_or_ref_ref_node("maxOutputRows").as<std::string>(); }
    void set_maxOutputRows_value(int64_t value) { set_or_ref_value_node("maxOutputRows", jsoncons::json(value)); }
    void set_maxOutputRows_ref(const std::string& ref) { set_or_ref_ref_node("maxOutputRows", ref); }
    bool is_maxOutputRows_ref() const { return is_or_ref_ref("maxOutputRows"); }
    bool is_set_maxOutputRows() const { return values_.count("maxOutputRows") > 0; }
    void unset_maxOutputRows() { values_.erase("maxOutputRows"); or_ref_is_ref_.erase("maxOutputRows"); }

    int64_t get_maxNumSteps_value() const { return get_or_ref_value_node("maxNumSteps").as<int64_t>(); }
    std::string get_maxNumSteps_ref() const { return get_or_ref_ref_node("maxNumSteps").as<std::string>(); }
    void set_maxNumSteps_value(int64_t value) { set_or_ref_value_node("maxNumSteps", jsoncons::json(value)); }
    void set_maxNumSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxNumSteps", ref); }
    bool is_maxNumSteps_ref() const { return is_or_ref_ref("maxNumSteps"); }
    bool is_set_maxNumSteps() const { return values_.count("maxNumSteps") > 0; }
    void unset_maxNumSteps() { values_.erase("maxNumSteps"); or_ref_is_ref_.erase("maxNumSteps"); }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    std::string get_independentVariable_value() const { return get_or_ref_value_node("independentVariable").as<std::string>(); }
    std::string get_independentVariable_ref() const { return get_or_ref_ref_node("independentVariable").as<std::string>(); }
    void set_independentVariable_value(const std::string& value) { set_or_ref_value_node("independentVariable", jsoncons::json(value)); }
    void set_independentVariable_ref(const std::string& ref) { set_or_ref_ref_node("independentVariable", ref); }
    bool is_independentVariable_ref() const { return is_or_ref_ref("independentVariable"); }
    bool is_set_independentVariable() const { return values_.count("independentVariable") > 0; }
    void unset_independentVariable() { values_.erase("independentVariable"); or_ref_is_ref_.erase("independentVariable"); }

    double get_independentVariableInit_value() const { return get_or_ref_value_node("independentVariableInit").as<double>(); }
    std::string get_independentVariableInit_ref() const { return get_or_ref_ref_node("independentVariableInit").as<std::string>(); }
    void set_independentVariableInit_value(double value) { set_or_ref_value_node("independentVariableInit", jsoncons::json(value)); }
    void set_independentVariableInit_ref(const std::string& ref) { set_or_ref_ref_node("independentVariableInit", ref); }
    bool is_independentVariableInit_ref() const { return is_or_ref_ref("independentVariableInit"); }
    bool is_set_independentVariableInit() const { return values_.count("independentVariableInit") > 0; }
    void unset_independentVariableInit() { values_.erase("independentVariableInit"); or_ref_is_ref_.erase("independentVariableInit"); }

    jsoncons::json get_outputVariables_value() const { return get_or_ref_value_node("outputVariables"); }
    std::string get_outputVariables_ref() const { return get_or_ref_ref_node("outputVariables").as<std::string>(); }
    void set_outputVariables_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariables", value); }
    void set_outputVariables_ref(const std::string& ref) { set_or_ref_ref_node("outputVariables", ref); }
    bool is_outputVariables_ref() const { return is_or_ref_ref("outputVariables"); }
    bool is_set_outputVariables() const { return values_.count("outputVariables") > 0; }
    void unset_outputVariables() { values_.erase("outputVariables"); or_ref_is_ref_.erase("outputVariables"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_independentVariableSpan() const { if (!independentVariableSpan_) throw ApiError(std::string("independentVariableSpan") + " is not set"); return independentVariableSpan_.get(); }
    void set_independentVariableSpan(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); independentVariableSpan_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_independentVariableSpan() const { return independentVariableSpan_ != nullptr; }
    void unset_independentVariableSpan() { independentVariableSpan_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (independentVariableSpan_) kids.push_back(independentVariableSpan_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (independentVariableSpan_) out.push_back(ChildLoc{independentVariableSpan_.get(), "/independentVariableSpan"});
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "independentVariableSpan") { independentVariableSpan_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("boundedStochasticSimulation");
        if (values_.count("seed")) d["seed"] = values_.at("seed");
        if (values_.count("timeDependentRelativeTolerance")) d["timeDependentRelativeTolerance"] = values_.at("timeDependentRelativeTolerance");
        if (values_.count("variableStepSize")) d["variableStepSize"] = values_.at("variableStepSize");
        if (values_.count("minimumTimeStep")) d["minimumTimeStep"] = values_.at("minimumTimeStep");
        if (values_.count("maximumTimeStep")) d["maximumTimeStep"] = values_.at("maximumTimeStep");
        if (values_.count("nonNegative")) d["nonNegative"] = values_.at("nonNegative");
        if (values_.count("maxOutputRows")) d["maxOutputRows"] = values_.at("maxOutputRows");
        if (values_.count("maxNumSteps")) d["maxNumSteps"] = values_.at("maxNumSteps");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (values_.count("outputVariables")) d["outputVariables"] = values_.at("outputVariables");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (independentVariableSpan_) d["independentVariableSpan"] = independentVariableSpan_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> independentVariableSpan_;
};

/// Generated from test-specsheets/tasks/Calculation/.
class Calculation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"math", "StringOrRef", true, std::string("Calculation-0002"), std::string("Calculation-0001"), "Calculation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"math"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("calculation"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Calculation-0004"); }
    std::string own_catchall() const override { return "Calculation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Calculation"; }
    std::string get_type() const { return "calculation"; }

    std::string get_math_value() const { return get_or_ref_value_node("math").as<std::string>(); }
    std::string get_math_ref() const { return get_or_ref_ref_node("math").as<std::string>(); }
    void set_math_value(const std::string& value) { set_or_ref_value_node("math", jsoncons::json(value)); }
    void set_math_ref(const std::string& ref) { set_or_ref_ref_node("math", ref); }
    bool is_math_ref() const { return is_or_ref_ref("math"); }
    bool is_set_math() const { return values_.count("math") > 0; }
    void unset_math() { values_.erase("math"); or_ref_is_ref_.erase("math"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("calculation");
        if (values_.count("math")) d["math"] = values_.at("math");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/CreateDataBlock/.
class CreateDataBlock : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"data", "DictOrRef", true, std::string("CreateDataBlock-0002"), std::string("CreateDataBlock-0001"), "CreateDataBlock-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"data"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("createDataBlock"); }
    std::optional<std::string> type_rule_id() const override { return std::string("CreateDataBlock-0004"); }
    std::string own_catchall() const override { return "CreateDataBlock-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "CreateDataBlock"; }
    std::string get_type() const { return "createDataBlock"; }

    jsoncons::json get_data_value() const { return get_or_ref_value_node("data"); }
    std::string get_data_ref() const { return get_or_ref_ref_node("data").as<std::string>(); }
    void set_data_value(const jsoncons::json& value) { set_or_ref_value_node("data", value); }
    void set_data_ref(const std::string& ref) { set_or_ref_ref_node("data", ref); }
    bool is_data_ref() const { return is_or_ref_ref("data"); }
    bool is_set_data() const { return values_.count("data") > 0; }
    void unset_data() { values_.erase("data"); or_ref_is_ref_.erase("data"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("createDataBlock");
        if (values_.count("data")) d["data"] = values_.at("data");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/CsvImport/.
class CsvImport : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"location", "StringOrRef", true, std::string("CsvImport-0002"), std::string("CsvImport-0001"), "CsvImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"organization", "StringOrRef", false, std::string("CsvImport-0004"), std::nullopt, "CsvImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"separator", "StringOrRef", false, std::string("CsvImport-0006"), std::nullopt, "CsvImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"headers", "BooleanOrRef", false, std::string("CsvImport-0008"), std::nullopt, "CsvImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"columnNames", "ArrayOrRef", false, std::string("CsvImport-0010"), std::nullopt, "CsvImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"ncols", "IntegerOrRef", false, std::string("CsvImport-0012"), std::nullopt, "CsvImport-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"nrows", "IntegerOrRef", false, std::string("CsvImport-0014"), std::nullopt, "CsvImport-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"units", "ArrayOrRef", false, std::string("CsvImport-0016"), std::nullopt, "CsvImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"location"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("csvImport"); }
    std::optional<std::string> type_rule_id() const override { return std::string("CsvImport-0018"); }
    std::string own_catchall() const override { return "CsvImport-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "CsvImport"; }
    std::string get_type() const { return "csvImport"; }

    std::string get_location_value() const { return get_or_ref_value_node("location").as<std::string>(); }
    std::string get_location_ref() const { return get_or_ref_ref_node("location").as<std::string>(); }
    void set_location_value(const std::string& value) { set_or_ref_value_node("location", jsoncons::json(value)); }
    void set_location_ref(const std::string& ref) { set_or_ref_ref_node("location", ref); }
    bool is_location_ref() const { return is_or_ref_ref("location"); }
    bool is_set_location() const { return values_.count("location") > 0; }
    void unset_location() { values_.erase("location"); or_ref_is_ref_.erase("location"); }

    std::string get_organization_value() const { return get_or_ref_value_node("organization").as<std::string>(); }
    std::string get_organization_ref() const { return get_or_ref_ref_node("organization").as<std::string>(); }
    void set_organization_value(const std::string& value) { set_or_ref_value_node("organization", jsoncons::json(value)); }
    void set_organization_ref(const std::string& ref) { set_or_ref_ref_node("organization", ref); }
    bool is_organization_ref() const { return is_or_ref_ref("organization"); }
    bool is_set_organization() const { return values_.count("organization") > 0; }
    void unset_organization() { values_.erase("organization"); or_ref_is_ref_.erase("organization"); }

    std::string get_separator_value() const { return get_or_ref_value_node("separator").as<std::string>(); }
    std::string get_separator_ref() const { return get_or_ref_ref_node("separator").as<std::string>(); }
    void set_separator_value(const std::string& value) { set_or_ref_value_node("separator", jsoncons::json(value)); }
    void set_separator_ref(const std::string& ref) { set_or_ref_ref_node("separator", ref); }
    bool is_separator_ref() const { return is_or_ref_ref("separator"); }
    bool is_set_separator() const { return values_.count("separator") > 0; }
    void unset_separator() { values_.erase("separator"); or_ref_is_ref_.erase("separator"); }

    bool get_headers_value() const { return get_or_ref_value_node("headers").as<bool>(); }
    std::string get_headers_ref() const { return get_or_ref_ref_node("headers").as<std::string>(); }
    void set_headers_value(bool value) { set_or_ref_value_node("headers", jsoncons::json(value)); }
    void set_headers_ref(const std::string& ref) { set_or_ref_ref_node("headers", ref); }
    bool is_headers_ref() const { return is_or_ref_ref("headers"); }
    bool is_set_headers() const { return values_.count("headers") > 0; }
    void unset_headers() { values_.erase("headers"); or_ref_is_ref_.erase("headers"); }

    jsoncons::json get_columnNames_value() const { return get_or_ref_value_node("columnNames"); }
    std::string get_columnNames_ref() const { return get_or_ref_ref_node("columnNames").as<std::string>(); }
    void set_columnNames_value(const jsoncons::json& value) { set_or_ref_value_node("columnNames", value); }
    void set_columnNames_ref(const std::string& ref) { set_or_ref_ref_node("columnNames", ref); }
    bool is_columnNames_ref() const { return is_or_ref_ref("columnNames"); }
    bool is_set_columnNames() const { return values_.count("columnNames") > 0; }
    void unset_columnNames() { values_.erase("columnNames"); or_ref_is_ref_.erase("columnNames"); }

    int64_t get_ncols_value() const { return get_or_ref_value_node("ncols").as<int64_t>(); }
    std::string get_ncols_ref() const { return get_or_ref_ref_node("ncols").as<std::string>(); }
    void set_ncols_value(int64_t value) { set_or_ref_value_node("ncols", jsoncons::json(value)); }
    void set_ncols_ref(const std::string& ref) { set_or_ref_ref_node("ncols", ref); }
    bool is_ncols_ref() const { return is_or_ref_ref("ncols"); }
    bool is_set_ncols() const { return values_.count("ncols") > 0; }
    void unset_ncols() { values_.erase("ncols"); or_ref_is_ref_.erase("ncols"); }

    int64_t get_nrows_value() const { return get_or_ref_value_node("nrows").as<int64_t>(); }
    std::string get_nrows_ref() const { return get_or_ref_ref_node("nrows").as<std::string>(); }
    void set_nrows_value(int64_t value) { set_or_ref_value_node("nrows", jsoncons::json(value)); }
    void set_nrows_ref(const std::string& ref) { set_or_ref_ref_node("nrows", ref); }
    bool is_nrows_ref() const { return is_or_ref_ref("nrows"); }
    bool is_set_nrows() const { return values_.count("nrows") > 0; }
    void unset_nrows() { values_.erase("nrows"); or_ref_is_ref_.erase("nrows"); }

    jsoncons::json get_units_value() const { return get_or_ref_value_node("units"); }
    std::string get_units_ref() const { return get_or_ref_ref_node("units").as<std::string>(); }
    void set_units_value(const jsoncons::json& value) { set_or_ref_value_node("units", value); }
    void set_units_ref(const std::string& ref) { set_or_ref_ref_node("units", ref); }
    bool is_units_ref() const { return is_or_ref_ref("units"); }
    bool is_set_units() const { return values_.count("units") > 0; }
    void unset_units() { values_.erase("units"); or_ref_is_ref_.erase("units"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("csvImport");
        if (values_.count("location")) d["location"] = values_.at("location");
        if (values_.count("organization")) d["organization"] = values_.at("organization");
        if (values_.count("separator")) d["separator"] = values_.at("separator");
        if (values_.count("headers")) d["headers"] = values_.at("headers");
        if (values_.count("columnNames")) d["columnNames"] = values_.at("columnNames");
        if (values_.count("ncols")) d["ncols"] = values_.at("ncols");
        if (values_.count("nrows")) d["nrows"] = values_.at("nrows");
        if (values_.count("units")) d["units"] = values_.at("units");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/DataImport/.
class DataImport : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"location", "StringOrRef", true, std::string("DataImport-0002"), std::string("DataImport-0001"), "DataImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"format", "StringOrRef", true, std::string("DataImport-0005"), std::string("DataImport-0004"), "DataImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"location", "format"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("dataImport"); }
    std::optional<std::string> type_rule_id() const override { return std::string("DataImport-0007"); }
    std::string own_catchall() const override { return "DataImport-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "DataImport"; }
    std::string get_type() const { return "dataImport"; }

    std::string get_location_value() const { return get_or_ref_value_node("location").as<std::string>(); }
    std::string get_location_ref() const { return get_or_ref_ref_node("location").as<std::string>(); }
    void set_location_value(const std::string& value) { set_or_ref_value_node("location", jsoncons::json(value)); }
    void set_location_ref(const std::string& ref) { set_or_ref_ref_node("location", ref); }
    bool is_location_ref() const { return is_or_ref_ref("location"); }
    bool is_set_location() const { return values_.count("location") > 0; }
    void unset_location() { values_.erase("location"); or_ref_is_ref_.erase("location"); }

    std::string get_format_value() const { return get_or_ref_value_node("format").as<std::string>(); }
    std::string get_format_ref() const { return get_or_ref_ref_node("format").as<std::string>(); }
    void set_format_value(const std::string& value) { set_or_ref_value_node("format", jsoncons::json(value)); }
    void set_format_ref(const std::string& ref) { set_or_ref_ref_node("format", ref); }
    bool is_format_ref() const { return is_or_ref_ref("format"); }
    bool is_set_format() const { return values_.count("format") > 0; }
    void unset_format() { values_.erase("format"); or_ref_is_ref_.erase("format"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("dataImport");
        if (values_.count("location")) d["location"] = values_.at("location");
        if (values_.count("format")) d["format"] = values_.at("format");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/DrawFromDistribution/.
class DrawFromDistribution : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"distribution", "StringOrRef", true, std::string("DrawFromDistribution-0008"), std::string("DrawFromDistribution-0007"), "DrawFromDistribution-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputPersistent", "BooleanOrRef", false, std::string("DrawFromDistribution-0004"), std::nullopt, "DrawFromDistribution-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"arguments", "ArrayOrRef", true, std::string("DrawFromDistribution-0002"), std::string("DrawFromDistribution-0001"), "DrawFromDistribution-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"distribution", "arguments"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("drawFromDistribution"); }
    std::optional<std::string> type_rule_id() const override { return std::string("DrawFromDistribution-0006"); }
    std::string own_catchall() const override { return "DrawFromDistribution-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "DrawFromDistribution"; }
    std::string get_type() const { return "drawFromDistribution"; }

    std::string get_distribution_value() const { return get_or_ref_value_node("distribution").as<std::string>(); }
    std::string get_distribution_ref() const { return get_or_ref_ref_node("distribution").as<std::string>(); }
    void set_distribution_value(const std::string& value) { set_or_ref_value_node("distribution", jsoncons::json(value)); }
    void set_distribution_ref(const std::string& ref) { set_or_ref_ref_node("distribution", ref); }
    bool is_distribution_ref() const { return is_or_ref_ref("distribution"); }
    bool is_set_distribution() const { return values_.count("distribution") > 0; }
    void unset_distribution() { values_.erase("distribution"); or_ref_is_ref_.erase("distribution"); }

    bool get_outputPersistent_value() const { return get_or_ref_value_node("outputPersistent").as<bool>(); }
    std::string get_outputPersistent_ref() const { return get_or_ref_ref_node("outputPersistent").as<std::string>(); }
    void set_outputPersistent_value(bool value) { set_or_ref_value_node("outputPersistent", jsoncons::json(value)); }
    void set_outputPersistent_ref(const std::string& ref) { set_or_ref_ref_node("outputPersistent", ref); }
    bool is_outputPersistent_ref() const { return is_or_ref_ref("outputPersistent"); }
    bool is_set_outputPersistent() const { return values_.count("outputPersistent") > 0; }
    void unset_outputPersistent() { values_.erase("outputPersistent"); or_ref_is_ref_.erase("outputPersistent"); }

    jsoncons::json get_arguments_value() const { return get_or_ref_value_node("arguments"); }
    std::string get_arguments_ref() const { return get_or_ref_ref_node("arguments").as<std::string>(); }
    void set_arguments_value(const jsoncons::json& value) { set_or_ref_value_node("arguments", value); }
    void set_arguments_ref(const std::string& ref) { set_or_ref_ref_node("arguments", ref); }
    bool is_arguments_ref() const { return is_or_ref_ref("arguments"); }
    bool is_set_arguments() const { return values_.count("arguments") > 0; }
    void unset_arguments() { values_.erase("arguments"); or_ref_is_ref_.erase("arguments"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("drawFromDistribution");
        if (values_.count("distribution")) d["distribution"] = values_.at("distribution");
        if (values_.count("outputPersistent")) d["outputPersistent"] = values_.at("outputPersistent");
        if (values_.count("arguments")) d["arguments"] = values_.at("arguments");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/ExplicitODESimulation/.
class ExplicitODESimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"relativeTolerance", "NumberOrRef", false, std::string("AbstractODESimulation-0001"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteTolerance", "NumberOrRef", false, std::string("AbstractODESimulation-0003"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceVector", "ArrayOrRef", false, std::string("AbstractODESimulation-0005"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceAdjustmentFactor", "NumberOrRef", false, std::string("AbstractODESimulation-0007"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"toleranceForRootFinder", "NumberOrRef", false, std::string("AbstractODESimulation-0009"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"initialStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0011"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumberOfSteps", "NumberOrRef", false, std::string("AbstractODESimulation-0013"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalSteps", "IntegerOrRef", false, std::string("AbstractODESimulation-0015"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0017"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minInternalStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0019"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"forcePhysicalCorrectness", "BooleanOrRef", false, std::string("AbstractODESimulation-0021"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"integrateReducedModel", "BooleanOrRef", false, std::string("AbstractODESimulation-0023"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"useReducedModel", "BooleanOrRef", false, std::string("AbstractODESimulation-0025"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"useStiffSolver", "BooleanOrRef", false, std::string("AbstractODESimulation-0027"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxBDForder", "IntegerOrRef", false, std::string("AbstractODESimulation-0029"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxAdamsOrder", "IntegerOrRef", false, std::string("AbstractODESimulation-0031"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"variableStepSize", "BooleanOrRef", false, std::string("AbstractODESimulation-0033"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxOutputRows", "IntegerOrRef", false, std::string("AbstractODESimulation-0035"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string("AbstractSimulation-0002"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string("AbstractSimulation-0004"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariables", "ArrayOrRef", false, std::string("AbstractSimulation-0006"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"independentVariableRange", "ref-class", true, std::string("ExplicitODESimulation-0005"), std::string("ExplicitODESimulation-0004"), "ExplicitODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("NumericRange"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"independentVariableRange"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("explicitODESimulation"); }
    std::optional<std::string> type_rule_id() const override { return std::string("ExplicitODESimulation-0006"); }
    std::string own_catchall() const override { return "ExplicitODESimulation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "ExplicitODESimulation"; }
    std::string get_type() const { return "explicitODESimulation"; }

    double get_relativeTolerance_value() const { return get_or_ref_value_node("relativeTolerance").as<double>(); }
    std::string get_relativeTolerance_ref() const { return get_or_ref_ref_node("relativeTolerance").as<std::string>(); }
    void set_relativeTolerance_value(double value) { set_or_ref_value_node("relativeTolerance", jsoncons::json(value)); }
    void set_relativeTolerance_ref(const std::string& ref) { set_or_ref_ref_node("relativeTolerance", ref); }
    bool is_relativeTolerance_ref() const { return is_or_ref_ref("relativeTolerance"); }
    bool is_set_relativeTolerance() const { return values_.count("relativeTolerance") > 0; }
    void unset_relativeTolerance() { values_.erase("relativeTolerance"); or_ref_is_ref_.erase("relativeTolerance"); }

    double get_absoluteTolerance_value() const { return get_or_ref_value_node("absoluteTolerance").as<double>(); }
    std::string get_absoluteTolerance_ref() const { return get_or_ref_ref_node("absoluteTolerance").as<std::string>(); }
    void set_absoluteTolerance_value(double value) { set_or_ref_value_node("absoluteTolerance", jsoncons::json(value)); }
    void set_absoluteTolerance_ref(const std::string& ref) { set_or_ref_ref_node("absoluteTolerance", ref); }
    bool is_absoluteTolerance_ref() const { return is_or_ref_ref("absoluteTolerance"); }
    bool is_set_absoluteTolerance() const { return values_.count("absoluteTolerance") > 0; }
    void unset_absoluteTolerance() { values_.erase("absoluteTolerance"); or_ref_is_ref_.erase("absoluteTolerance"); }

    jsoncons::json get_absoluteToleranceVector_value() const { return get_or_ref_value_node("absoluteToleranceVector"); }
    std::string get_absoluteToleranceVector_ref() const { return get_or_ref_ref_node("absoluteToleranceVector").as<std::string>(); }
    void set_absoluteToleranceVector_value(const jsoncons::json& value) { set_or_ref_value_node("absoluteToleranceVector", value); }
    void set_absoluteToleranceVector_ref(const std::string& ref) { set_or_ref_ref_node("absoluteToleranceVector", ref); }
    bool is_absoluteToleranceVector_ref() const { return is_or_ref_ref("absoluteToleranceVector"); }
    bool is_set_absoluteToleranceVector() const { return values_.count("absoluteToleranceVector") > 0; }
    void unset_absoluteToleranceVector() { values_.erase("absoluteToleranceVector"); or_ref_is_ref_.erase("absoluteToleranceVector"); }

    double get_absoluteToleranceAdjustmentFactor_value() const { return get_or_ref_value_node("absoluteToleranceAdjustmentFactor").as<double>(); }
    std::string get_absoluteToleranceAdjustmentFactor_ref() const { return get_or_ref_ref_node("absoluteToleranceAdjustmentFactor").as<std::string>(); }
    void set_absoluteToleranceAdjustmentFactor_value(double value) { set_or_ref_value_node("absoluteToleranceAdjustmentFactor", jsoncons::json(value)); }
    void set_absoluteToleranceAdjustmentFactor_ref(const std::string& ref) { set_or_ref_ref_node("absoluteToleranceAdjustmentFactor", ref); }
    bool is_absoluteToleranceAdjustmentFactor_ref() const { return is_or_ref_ref("absoluteToleranceAdjustmentFactor"); }
    bool is_set_absoluteToleranceAdjustmentFactor() const { return values_.count("absoluteToleranceAdjustmentFactor") > 0; }
    void unset_absoluteToleranceAdjustmentFactor() { values_.erase("absoluteToleranceAdjustmentFactor"); or_ref_is_ref_.erase("absoluteToleranceAdjustmentFactor"); }

    double get_toleranceForRootFinder_value() const { return get_or_ref_value_node("toleranceForRootFinder").as<double>(); }
    std::string get_toleranceForRootFinder_ref() const { return get_or_ref_ref_node("toleranceForRootFinder").as<std::string>(); }
    void set_toleranceForRootFinder_value(double value) { set_or_ref_value_node("toleranceForRootFinder", jsoncons::json(value)); }
    void set_toleranceForRootFinder_ref(const std::string& ref) { set_or_ref_ref_node("toleranceForRootFinder", ref); }
    bool is_toleranceForRootFinder_ref() const { return is_or_ref_ref("toleranceForRootFinder"); }
    bool is_set_toleranceForRootFinder() const { return values_.count("toleranceForRootFinder") > 0; }
    void unset_toleranceForRootFinder() { values_.erase("toleranceForRootFinder"); or_ref_is_ref_.erase("toleranceForRootFinder"); }

    double get_initialStepSize_value() const { return get_or_ref_value_node("initialStepSize").as<double>(); }
    std::string get_initialStepSize_ref() const { return get_or_ref_ref_node("initialStepSize").as<std::string>(); }
    void set_initialStepSize_value(double value) { set_or_ref_value_node("initialStepSize", jsoncons::json(value)); }
    void set_initialStepSize_ref(const std::string& ref) { set_or_ref_ref_node("initialStepSize", ref); }
    bool is_initialStepSize_ref() const { return is_or_ref_ref("initialStepSize"); }
    bool is_set_initialStepSize() const { return values_.count("initialStepSize") > 0; }
    void unset_initialStepSize() { values_.erase("initialStepSize"); or_ref_is_ref_.erase("initialStepSize"); }

    double get_maxNumberOfSteps_value() const { return get_or_ref_value_node("maxNumberOfSteps").as<double>(); }
    std::string get_maxNumberOfSteps_ref() const { return get_or_ref_ref_node("maxNumberOfSteps").as<std::string>(); }
    void set_maxNumberOfSteps_value(double value) { set_or_ref_value_node("maxNumberOfSteps", jsoncons::json(value)); }
    void set_maxNumberOfSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxNumberOfSteps", ref); }
    bool is_maxNumberOfSteps_ref() const { return is_or_ref_ref("maxNumberOfSteps"); }
    bool is_set_maxNumberOfSteps() const { return values_.count("maxNumberOfSteps") > 0; }
    void unset_maxNumberOfSteps() { values_.erase("maxNumberOfSteps"); or_ref_is_ref_.erase("maxNumberOfSteps"); }

    int64_t get_maxInternalSteps_value() const { return get_or_ref_value_node("maxInternalSteps").as<int64_t>(); }
    std::string get_maxInternalSteps_ref() const { return get_or_ref_ref_node("maxInternalSteps").as<std::string>(); }
    void set_maxInternalSteps_value(int64_t value) { set_or_ref_value_node("maxInternalSteps", jsoncons::json(value)); }
    void set_maxInternalSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxInternalSteps", ref); }
    bool is_maxInternalSteps_ref() const { return is_or_ref_ref("maxInternalSteps"); }
    bool is_set_maxInternalSteps() const { return values_.count("maxInternalSteps") > 0; }
    void unset_maxInternalSteps() { values_.erase("maxInternalSteps"); or_ref_is_ref_.erase("maxInternalSteps"); }

    double get_maxInternalStepSize_value() const { return get_or_ref_value_node("maxInternalStepSize").as<double>(); }
    std::string get_maxInternalStepSize_ref() const { return get_or_ref_ref_node("maxInternalStepSize").as<std::string>(); }
    void set_maxInternalStepSize_value(double value) { set_or_ref_value_node("maxInternalStepSize", jsoncons::json(value)); }
    void set_maxInternalStepSize_ref(const std::string& ref) { set_or_ref_ref_node("maxInternalStepSize", ref); }
    bool is_maxInternalStepSize_ref() const { return is_or_ref_ref("maxInternalStepSize"); }
    bool is_set_maxInternalStepSize() const { return values_.count("maxInternalStepSize") > 0; }
    void unset_maxInternalStepSize() { values_.erase("maxInternalStepSize"); or_ref_is_ref_.erase("maxInternalStepSize"); }

    double get_minInternalStepSize_value() const { return get_or_ref_value_node("minInternalStepSize").as<double>(); }
    std::string get_minInternalStepSize_ref() const { return get_or_ref_ref_node("minInternalStepSize").as<std::string>(); }
    void set_minInternalStepSize_value(double value) { set_or_ref_value_node("minInternalStepSize", jsoncons::json(value)); }
    void set_minInternalStepSize_ref(const std::string& ref) { set_or_ref_ref_node("minInternalStepSize", ref); }
    bool is_minInternalStepSize_ref() const { return is_or_ref_ref("minInternalStepSize"); }
    bool is_set_minInternalStepSize() const { return values_.count("minInternalStepSize") > 0; }
    void unset_minInternalStepSize() { values_.erase("minInternalStepSize"); or_ref_is_ref_.erase("minInternalStepSize"); }

    bool get_forcePhysicalCorrectness_value() const { return get_or_ref_value_node("forcePhysicalCorrectness").as<bool>(); }
    std::string get_forcePhysicalCorrectness_ref() const { return get_or_ref_ref_node("forcePhysicalCorrectness").as<std::string>(); }
    void set_forcePhysicalCorrectness_value(bool value) { set_or_ref_value_node("forcePhysicalCorrectness", jsoncons::json(value)); }
    void set_forcePhysicalCorrectness_ref(const std::string& ref) { set_or_ref_ref_node("forcePhysicalCorrectness", ref); }
    bool is_forcePhysicalCorrectness_ref() const { return is_or_ref_ref("forcePhysicalCorrectness"); }
    bool is_set_forcePhysicalCorrectness() const { return values_.count("forcePhysicalCorrectness") > 0; }
    void unset_forcePhysicalCorrectness() { values_.erase("forcePhysicalCorrectness"); or_ref_is_ref_.erase("forcePhysicalCorrectness"); }

    bool get_integrateReducedModel_value() const { return get_or_ref_value_node("integrateReducedModel").as<bool>(); }
    std::string get_integrateReducedModel_ref() const { return get_or_ref_ref_node("integrateReducedModel").as<std::string>(); }
    void set_integrateReducedModel_value(bool value) { set_or_ref_value_node("integrateReducedModel", jsoncons::json(value)); }
    void set_integrateReducedModel_ref(const std::string& ref) { set_or_ref_ref_node("integrateReducedModel", ref); }
    bool is_integrateReducedModel_ref() const { return is_or_ref_ref("integrateReducedModel"); }
    bool is_set_integrateReducedModel() const { return values_.count("integrateReducedModel") > 0; }
    void unset_integrateReducedModel() { values_.erase("integrateReducedModel"); or_ref_is_ref_.erase("integrateReducedModel"); }

    bool get_useReducedModel_value() const { return get_or_ref_value_node("useReducedModel").as<bool>(); }
    std::string get_useReducedModel_ref() const { return get_or_ref_ref_node("useReducedModel").as<std::string>(); }
    void set_useReducedModel_value(bool value) { set_or_ref_value_node("useReducedModel", jsoncons::json(value)); }
    void set_useReducedModel_ref(const std::string& ref) { set_or_ref_ref_node("useReducedModel", ref); }
    bool is_useReducedModel_ref() const { return is_or_ref_ref("useReducedModel"); }
    bool is_set_useReducedModel() const { return values_.count("useReducedModel") > 0; }
    void unset_useReducedModel() { values_.erase("useReducedModel"); or_ref_is_ref_.erase("useReducedModel"); }

    bool get_useStiffSolver_value() const { return get_or_ref_value_node("useStiffSolver").as<bool>(); }
    std::string get_useStiffSolver_ref() const { return get_or_ref_ref_node("useStiffSolver").as<std::string>(); }
    void set_useStiffSolver_value(bool value) { set_or_ref_value_node("useStiffSolver", jsoncons::json(value)); }
    void set_useStiffSolver_ref(const std::string& ref) { set_or_ref_ref_node("useStiffSolver", ref); }
    bool is_useStiffSolver_ref() const { return is_or_ref_ref("useStiffSolver"); }
    bool is_set_useStiffSolver() const { return values_.count("useStiffSolver") > 0; }
    void unset_useStiffSolver() { values_.erase("useStiffSolver"); or_ref_is_ref_.erase("useStiffSolver"); }

    int64_t get_maxBDForder_value() const { return get_or_ref_value_node("maxBDForder").as<int64_t>(); }
    std::string get_maxBDForder_ref() const { return get_or_ref_ref_node("maxBDForder").as<std::string>(); }
    void set_maxBDForder_value(int64_t value) { set_or_ref_value_node("maxBDForder", jsoncons::json(value)); }
    void set_maxBDForder_ref(const std::string& ref) { set_or_ref_ref_node("maxBDForder", ref); }
    bool is_maxBDForder_ref() const { return is_or_ref_ref("maxBDForder"); }
    bool is_set_maxBDForder() const { return values_.count("maxBDForder") > 0; }
    void unset_maxBDForder() { values_.erase("maxBDForder"); or_ref_is_ref_.erase("maxBDForder"); }

    int64_t get_maxAdamsOrder_value() const { return get_or_ref_value_node("maxAdamsOrder").as<int64_t>(); }
    std::string get_maxAdamsOrder_ref() const { return get_or_ref_ref_node("maxAdamsOrder").as<std::string>(); }
    void set_maxAdamsOrder_value(int64_t value) { set_or_ref_value_node("maxAdamsOrder", jsoncons::json(value)); }
    void set_maxAdamsOrder_ref(const std::string& ref) { set_or_ref_ref_node("maxAdamsOrder", ref); }
    bool is_maxAdamsOrder_ref() const { return is_or_ref_ref("maxAdamsOrder"); }
    bool is_set_maxAdamsOrder() const { return values_.count("maxAdamsOrder") > 0; }
    void unset_maxAdamsOrder() { values_.erase("maxAdamsOrder"); or_ref_is_ref_.erase("maxAdamsOrder"); }

    bool get_variableStepSize_value() const { return get_or_ref_value_node("variableStepSize").as<bool>(); }
    std::string get_variableStepSize_ref() const { return get_or_ref_ref_node("variableStepSize").as<std::string>(); }
    void set_variableStepSize_value(bool value) { set_or_ref_value_node("variableStepSize", jsoncons::json(value)); }
    void set_variableStepSize_ref(const std::string& ref) { set_or_ref_ref_node("variableStepSize", ref); }
    bool is_variableStepSize_ref() const { return is_or_ref_ref("variableStepSize"); }
    bool is_set_variableStepSize() const { return values_.count("variableStepSize") > 0; }
    void unset_variableStepSize() { values_.erase("variableStepSize"); or_ref_is_ref_.erase("variableStepSize"); }

    int64_t get_maxOutputRows_value() const { return get_or_ref_value_node("maxOutputRows").as<int64_t>(); }
    std::string get_maxOutputRows_ref() const { return get_or_ref_ref_node("maxOutputRows").as<std::string>(); }
    void set_maxOutputRows_value(int64_t value) { set_or_ref_value_node("maxOutputRows", jsoncons::json(value)); }
    void set_maxOutputRows_ref(const std::string& ref) { set_or_ref_ref_node("maxOutputRows", ref); }
    bool is_maxOutputRows_ref() const { return is_or_ref_ref("maxOutputRows"); }
    bool is_set_maxOutputRows() const { return values_.count("maxOutputRows") > 0; }
    void unset_maxOutputRows() { values_.erase("maxOutputRows"); or_ref_is_ref_.erase("maxOutputRows"); }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    std::string get_independentVariable_value() const { return get_or_ref_value_node("independentVariable").as<std::string>(); }
    std::string get_independentVariable_ref() const { return get_or_ref_ref_node("independentVariable").as<std::string>(); }
    void set_independentVariable_value(const std::string& value) { set_or_ref_value_node("independentVariable", jsoncons::json(value)); }
    void set_independentVariable_ref(const std::string& ref) { set_or_ref_ref_node("independentVariable", ref); }
    bool is_independentVariable_ref() const { return is_or_ref_ref("independentVariable"); }
    bool is_set_independentVariable() const { return values_.count("independentVariable") > 0; }
    void unset_independentVariable() { values_.erase("independentVariable"); or_ref_is_ref_.erase("independentVariable"); }

    double get_independentVariableInit_value() const { return get_or_ref_value_node("independentVariableInit").as<double>(); }
    std::string get_independentVariableInit_ref() const { return get_or_ref_ref_node("independentVariableInit").as<std::string>(); }
    void set_independentVariableInit_value(double value) { set_or_ref_value_node("independentVariableInit", jsoncons::json(value)); }
    void set_independentVariableInit_ref(const std::string& ref) { set_or_ref_ref_node("independentVariableInit", ref); }
    bool is_independentVariableInit_ref() const { return is_or_ref_ref("independentVariableInit"); }
    bool is_set_independentVariableInit() const { return values_.count("independentVariableInit") > 0; }
    void unset_independentVariableInit() { values_.erase("independentVariableInit"); or_ref_is_ref_.erase("independentVariableInit"); }

    jsoncons::json get_outputVariables_value() const { return get_or_ref_value_node("outputVariables"); }
    std::string get_outputVariables_ref() const { return get_or_ref_ref_node("outputVariables").as<std::string>(); }
    void set_outputVariables_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariables", value); }
    void set_outputVariables_ref(const std::string& ref) { set_or_ref_ref_node("outputVariables", ref); }
    bool is_outputVariables_ref() const { return is_or_ref_ref("outputVariables"); }
    bool is_set_outputVariables() const { return values_.count("outputVariables") > 0; }
    void unset_outputVariables() { values_.erase("outputVariables"); or_ref_is_ref_.erase("outputVariables"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_independentVariableRange() const { if (!independentVariableRange_) throw ApiError(std::string("independentVariableRange") + " is not set"); return independentVariableRange_.get(); }
    void set_independentVariableRange(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); independentVariableRange_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_independentVariableRange() const { return independentVariableRange_ != nullptr; }
    void unset_independentVariableRange() { independentVariableRange_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (independentVariableRange_) kids.push_back(independentVariableRange_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (independentVariableRange_) out.push_back(ChildLoc{independentVariableRange_.get(), "/independentVariableRange"});
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "independentVariableRange") { independentVariableRange_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("explicitODESimulation");
        if (values_.count("relativeTolerance")) d["relativeTolerance"] = values_.at("relativeTolerance");
        if (values_.count("absoluteTolerance")) d["absoluteTolerance"] = values_.at("absoluteTolerance");
        if (values_.count("absoluteToleranceVector")) d["absoluteToleranceVector"] = values_.at("absoluteToleranceVector");
        if (values_.count("absoluteToleranceAdjustmentFactor")) d["absoluteToleranceAdjustmentFactor"] = values_.at("absoluteToleranceAdjustmentFactor");
        if (values_.count("toleranceForRootFinder")) d["toleranceForRootFinder"] = values_.at("toleranceForRootFinder");
        if (values_.count("initialStepSize")) d["initialStepSize"] = values_.at("initialStepSize");
        if (values_.count("maxNumberOfSteps")) d["maxNumberOfSteps"] = values_.at("maxNumberOfSteps");
        if (values_.count("maxInternalSteps")) d["maxInternalSteps"] = values_.at("maxInternalSteps");
        if (values_.count("maxInternalStepSize")) d["maxInternalStepSize"] = values_.at("maxInternalStepSize");
        if (values_.count("minInternalStepSize")) d["minInternalStepSize"] = values_.at("minInternalStepSize");
        if (values_.count("forcePhysicalCorrectness")) d["forcePhysicalCorrectness"] = values_.at("forcePhysicalCorrectness");
        if (values_.count("integrateReducedModel")) d["integrateReducedModel"] = values_.at("integrateReducedModel");
        if (values_.count("useReducedModel")) d["useReducedModel"] = values_.at("useReducedModel");
        if (values_.count("useStiffSolver")) d["useStiffSolver"] = values_.at("useStiffSolver");
        if (values_.count("maxBDForder")) d["maxBDForder"] = values_.at("maxBDForder");
        if (values_.count("maxAdamsOrder")) d["maxAdamsOrder"] = values_.at("maxAdamsOrder");
        if (values_.count("variableStepSize")) d["variableStepSize"] = values_.at("variableStepSize");
        if (values_.count("maxOutputRows")) d["maxOutputRows"] = values_.at("maxOutputRows");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (values_.count("outputVariables")) d["outputVariables"] = values_.at("outputVariables");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (independentVariableRange_) d["independentVariableRange"] = independentVariableRange_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> independentVariableRange_;
};

/// Generated from test-specsheets/tasks/ExplicitStochasticSimulation/.
class ExplicitStochasticSimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"seed", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0001"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"timeDependentRelativeTolerance", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0003"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"variableStepSize", "BooleanOrRef", false, std::string("AbstractStochasticSimulation-0005"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minimumTimeStep", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0007"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maximumTimeStep", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0009"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"nonNegative", "BooleanOrRef", false, std::string("AbstractStochasticSimulation-0011"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxOutputRows", "IntegerOrRef", false, std::string("AbstractStochasticSimulation-0013"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumSteps", "IntegerOrRef", false, std::string("AbstractStochasticSimulation-0015"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string("AbstractSimulation-0002"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string("AbstractSimulation-0004"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariables", "ArrayOrRef", false, std::string("AbstractSimulation-0006"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"independentVariableRange", "ref-class", true, std::string("ExplicitStochasticSimulation-0005"), std::string("ExplicitStochasticSimulation-0004"), "ExplicitStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("NumericRange"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"independentVariableRange"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("explicitStochasticSimulation"); }
    std::optional<std::string> type_rule_id() const override { return std::string("ExplicitStochasticSimulation-0006"); }
    std::string own_catchall() const override { return "ExplicitStochasticSimulation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "ExplicitStochasticSimulation"; }
    std::string get_type() const { return "explicitStochasticSimulation"; }

    double get_seed_value() const { return get_or_ref_value_node("seed").as<double>(); }
    std::string get_seed_ref() const { return get_or_ref_ref_node("seed").as<std::string>(); }
    void set_seed_value(double value) { set_or_ref_value_node("seed", jsoncons::json(value)); }
    void set_seed_ref(const std::string& ref) { set_or_ref_ref_node("seed", ref); }
    bool is_seed_ref() const { return is_or_ref_ref("seed"); }
    bool is_set_seed() const { return values_.count("seed") > 0; }
    void unset_seed() { values_.erase("seed"); or_ref_is_ref_.erase("seed"); }

    double get_timeDependentRelativeTolerance_value() const { return get_or_ref_value_node("timeDependentRelativeTolerance").as<double>(); }
    std::string get_timeDependentRelativeTolerance_ref() const { return get_or_ref_ref_node("timeDependentRelativeTolerance").as<std::string>(); }
    void set_timeDependentRelativeTolerance_value(double value) { set_or_ref_value_node("timeDependentRelativeTolerance", jsoncons::json(value)); }
    void set_timeDependentRelativeTolerance_ref(const std::string& ref) { set_or_ref_ref_node("timeDependentRelativeTolerance", ref); }
    bool is_timeDependentRelativeTolerance_ref() const { return is_or_ref_ref("timeDependentRelativeTolerance"); }
    bool is_set_timeDependentRelativeTolerance() const { return values_.count("timeDependentRelativeTolerance") > 0; }
    void unset_timeDependentRelativeTolerance() { values_.erase("timeDependentRelativeTolerance"); or_ref_is_ref_.erase("timeDependentRelativeTolerance"); }

    bool get_variableStepSize_value() const { return get_or_ref_value_node("variableStepSize").as<bool>(); }
    std::string get_variableStepSize_ref() const { return get_or_ref_ref_node("variableStepSize").as<std::string>(); }
    void set_variableStepSize_value(bool value) { set_or_ref_value_node("variableStepSize", jsoncons::json(value)); }
    void set_variableStepSize_ref(const std::string& ref) { set_or_ref_ref_node("variableStepSize", ref); }
    bool is_variableStepSize_ref() const { return is_or_ref_ref("variableStepSize"); }
    bool is_set_variableStepSize() const { return values_.count("variableStepSize") > 0; }
    void unset_variableStepSize() { values_.erase("variableStepSize"); or_ref_is_ref_.erase("variableStepSize"); }

    double get_minimumTimeStep_value() const { return get_or_ref_value_node("minimumTimeStep").as<double>(); }
    std::string get_minimumTimeStep_ref() const { return get_or_ref_ref_node("minimumTimeStep").as<std::string>(); }
    void set_minimumTimeStep_value(double value) { set_or_ref_value_node("minimumTimeStep", jsoncons::json(value)); }
    void set_minimumTimeStep_ref(const std::string& ref) { set_or_ref_ref_node("minimumTimeStep", ref); }
    bool is_minimumTimeStep_ref() const { return is_or_ref_ref("minimumTimeStep"); }
    bool is_set_minimumTimeStep() const { return values_.count("minimumTimeStep") > 0; }
    void unset_minimumTimeStep() { values_.erase("minimumTimeStep"); or_ref_is_ref_.erase("minimumTimeStep"); }

    double get_maximumTimeStep_value() const { return get_or_ref_value_node("maximumTimeStep").as<double>(); }
    std::string get_maximumTimeStep_ref() const { return get_or_ref_ref_node("maximumTimeStep").as<std::string>(); }
    void set_maximumTimeStep_value(double value) { set_or_ref_value_node("maximumTimeStep", jsoncons::json(value)); }
    void set_maximumTimeStep_ref(const std::string& ref) { set_or_ref_ref_node("maximumTimeStep", ref); }
    bool is_maximumTimeStep_ref() const { return is_or_ref_ref("maximumTimeStep"); }
    bool is_set_maximumTimeStep() const { return values_.count("maximumTimeStep") > 0; }
    void unset_maximumTimeStep() { values_.erase("maximumTimeStep"); or_ref_is_ref_.erase("maximumTimeStep"); }

    bool get_nonNegative_value() const { return get_or_ref_value_node("nonNegative").as<bool>(); }
    std::string get_nonNegative_ref() const { return get_or_ref_ref_node("nonNegative").as<std::string>(); }
    void set_nonNegative_value(bool value) { set_or_ref_value_node("nonNegative", jsoncons::json(value)); }
    void set_nonNegative_ref(const std::string& ref) { set_or_ref_ref_node("nonNegative", ref); }
    bool is_nonNegative_ref() const { return is_or_ref_ref("nonNegative"); }
    bool is_set_nonNegative() const { return values_.count("nonNegative") > 0; }
    void unset_nonNegative() { values_.erase("nonNegative"); or_ref_is_ref_.erase("nonNegative"); }

    int64_t get_maxOutputRows_value() const { return get_or_ref_value_node("maxOutputRows").as<int64_t>(); }
    std::string get_maxOutputRows_ref() const { return get_or_ref_ref_node("maxOutputRows").as<std::string>(); }
    void set_maxOutputRows_value(int64_t value) { set_or_ref_value_node("maxOutputRows", jsoncons::json(value)); }
    void set_maxOutputRows_ref(const std::string& ref) { set_or_ref_ref_node("maxOutputRows", ref); }
    bool is_maxOutputRows_ref() const { return is_or_ref_ref("maxOutputRows"); }
    bool is_set_maxOutputRows() const { return values_.count("maxOutputRows") > 0; }
    void unset_maxOutputRows() { values_.erase("maxOutputRows"); or_ref_is_ref_.erase("maxOutputRows"); }

    int64_t get_maxNumSteps_value() const { return get_or_ref_value_node("maxNumSteps").as<int64_t>(); }
    std::string get_maxNumSteps_ref() const { return get_or_ref_ref_node("maxNumSteps").as<std::string>(); }
    void set_maxNumSteps_value(int64_t value) { set_or_ref_value_node("maxNumSteps", jsoncons::json(value)); }
    void set_maxNumSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxNumSteps", ref); }
    bool is_maxNumSteps_ref() const { return is_or_ref_ref("maxNumSteps"); }
    bool is_set_maxNumSteps() const { return values_.count("maxNumSteps") > 0; }
    void unset_maxNumSteps() { values_.erase("maxNumSteps"); or_ref_is_ref_.erase("maxNumSteps"); }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    std::string get_independentVariable_value() const { return get_or_ref_value_node("independentVariable").as<std::string>(); }
    std::string get_independentVariable_ref() const { return get_or_ref_ref_node("independentVariable").as<std::string>(); }
    void set_independentVariable_value(const std::string& value) { set_or_ref_value_node("independentVariable", jsoncons::json(value)); }
    void set_independentVariable_ref(const std::string& ref) { set_or_ref_ref_node("independentVariable", ref); }
    bool is_independentVariable_ref() const { return is_or_ref_ref("independentVariable"); }
    bool is_set_independentVariable() const { return values_.count("independentVariable") > 0; }
    void unset_independentVariable() { values_.erase("independentVariable"); or_ref_is_ref_.erase("independentVariable"); }

    double get_independentVariableInit_value() const { return get_or_ref_value_node("independentVariableInit").as<double>(); }
    std::string get_independentVariableInit_ref() const { return get_or_ref_ref_node("independentVariableInit").as<std::string>(); }
    void set_independentVariableInit_value(double value) { set_or_ref_value_node("independentVariableInit", jsoncons::json(value)); }
    void set_independentVariableInit_ref(const std::string& ref) { set_or_ref_ref_node("independentVariableInit", ref); }
    bool is_independentVariableInit_ref() const { return is_or_ref_ref("independentVariableInit"); }
    bool is_set_independentVariableInit() const { return values_.count("independentVariableInit") > 0; }
    void unset_independentVariableInit() { values_.erase("independentVariableInit"); or_ref_is_ref_.erase("independentVariableInit"); }

    jsoncons::json get_outputVariables_value() const { return get_or_ref_value_node("outputVariables"); }
    std::string get_outputVariables_ref() const { return get_or_ref_ref_node("outputVariables").as<std::string>(); }
    void set_outputVariables_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariables", value); }
    void set_outputVariables_ref(const std::string& ref) { set_or_ref_ref_node("outputVariables", ref); }
    bool is_outputVariables_ref() const { return is_or_ref_ref("outputVariables"); }
    bool is_set_outputVariables() const { return values_.count("outputVariables") > 0; }
    void unset_outputVariables() { values_.erase("outputVariables"); or_ref_is_ref_.erase("outputVariables"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_independentVariableRange() const { if (!independentVariableRange_) throw ApiError(std::string("independentVariableRange") + " is not set"); return independentVariableRange_.get(); }
    void set_independentVariableRange(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); independentVariableRange_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_independentVariableRange() const { return independentVariableRange_ != nullptr; }
    void unset_independentVariableRange() { independentVariableRange_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (independentVariableRange_) kids.push_back(independentVariableRange_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (independentVariableRange_) out.push_back(ChildLoc{independentVariableRange_.get(), "/independentVariableRange"});
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "independentVariableRange") { independentVariableRange_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("explicitStochasticSimulation");
        if (values_.count("seed")) d["seed"] = values_.at("seed");
        if (values_.count("timeDependentRelativeTolerance")) d["timeDependentRelativeTolerance"] = values_.at("timeDependentRelativeTolerance");
        if (values_.count("variableStepSize")) d["variableStepSize"] = values_.at("variableStepSize");
        if (values_.count("minimumTimeStep")) d["minimumTimeStep"] = values_.at("minimumTimeStep");
        if (values_.count("maximumTimeStep")) d["maximumTimeStep"] = values_.at("maximumTimeStep");
        if (values_.count("nonNegative")) d["nonNegative"] = values_.at("nonNegative");
        if (values_.count("maxOutputRows")) d["maxOutputRows"] = values_.at("maxOutputRows");
        if (values_.count("maxNumSteps")) d["maxNumSteps"] = values_.at("maxNumSteps");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (values_.count("outputVariables")) d["outputVariables"] = values_.at("outputVariables");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (independentVariableRange_) d["independentVariableRange"] = independentVariableRange_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> independentVariableRange_;
};

/// Generated from test-specsheets/tasks/FluxBalanceAnalysis/.
class FluxBalanceAnalysis : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("FluxBalanceAnalysis-0002"), std::string("FluxBalanceAnalysis-0001"), "FluxBalanceAnalysis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariables", "ArrayOrRef", true, std::string("FluxBalanceAnalysis-0004"), std::string("FluxBalanceAnalysis-0003"), "FluxBalanceAnalysis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputModel", "BooleanOrRef", false, std::string("FluxBalanceAnalysis-0006"), std::nullopt, "FluxBalanceAnalysis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"model", "outputVariables"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("fluxBalanceAnalysis"); }
    std::optional<std::string> type_rule_id() const override { return std::string("FluxBalanceAnalysis-0008"); }
    std::string own_catchall() const override { return "FluxBalanceAnalysis-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "FluxBalanceAnalysis"; }
    std::string get_type() const { return "fluxBalanceAnalysis"; }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    jsoncons::json get_outputVariables_value() const { return get_or_ref_value_node("outputVariables"); }
    std::string get_outputVariables_ref() const { return get_or_ref_ref_node("outputVariables").as<std::string>(); }
    void set_outputVariables_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariables", value); }
    void set_outputVariables_ref(const std::string& ref) { set_or_ref_ref_node("outputVariables", ref); }
    bool is_outputVariables_ref() const { return is_or_ref_ref("outputVariables"); }
    bool is_set_outputVariables() const { return values_.count("outputVariables") > 0; }
    void unset_outputVariables() { values_.erase("outputVariables"); or_ref_is_ref_.erase("outputVariables"); }

    bool get_outputModel_value() const { return get_or_ref_value_node("outputModel").as<bool>(); }
    std::string get_outputModel_ref() const { return get_or_ref_ref_node("outputModel").as<std::string>(); }
    void set_outputModel_value(bool value) { set_or_ref_value_node("outputModel", jsoncons::json(value)); }
    void set_outputModel_ref(const std::string& ref) { set_or_ref_ref_node("outputModel", ref); }
    bool is_outputModel_ref() const { return is_or_ref_ref("outputModel"); }
    bool is_set_outputModel() const { return values_.count("outputModel") > 0; }
    void unset_outputModel() { values_.erase("outputModel"); or_ref_is_ref_.erase("outputModel"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("fluxBalanceAnalysis");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("outputVariables")) d["outputVariables"] = values_.at("outputVariables");
        if (values_.count("outputModel")) d["outputModel"] = values_.at("outputModel");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/JacobianFull/.
class JacobianFull : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("JacobianFull-0002"), std::string("JacobianFull-0001"), "JacobianFull-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"model"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("jacobianFull"); }
    std::optional<std::string> type_rule_id() const override { return std::string("JacobianFull-0003"); }
    std::string own_catchall() const override { return "JacobianFull-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "JacobianFull"; }
    std::string get_type() const { return "jacobianFull"; }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("jacobianFull");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/JacobianReduced/.
class JacobianReduced : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("JacobianReduced-0002"), std::string("JacobianReduced-0001"), "JacobianReduced-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"model"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("jacobianReduced"); }
    std::optional<std::string> type_rule_id() const override { return std::string("JacobianReduced-0003"); }
    std::string own_catchall() const override { return "JacobianReduced-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "JacobianReduced"; }
    std::string get_type() const { return "jacobianReduced"; }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("jacobianReduced");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/Loop/.
class Loop : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"outputVariableMap", "DictOrRef", false, std::string("Repeat-0002"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"loopVariables", "dict", true, std::string("Loop-0003"), std::string("Loop-0002"), "Loop-0000", std::nullopt, std::nullopt, std::nullopt, std::string("LoopVariable"), std::nullopt},
            FieldSpec{"subTasks", "dict", false, std::string("Repeat-0001"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractTask")},
            FieldSpec{"aggregateOutputVariables", "dict", false, std::string("Repeat-0004"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::string("AggregationCalculation"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"range", "ref-discriminator", false, std::string("Repeat-0005"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("RangeInline")}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"loopVariables"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("loop"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Loop-0005"); }
    std::string own_catchall() const override { return "Loop-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Loop"; }
    std::string get_type() const { return "loop"; }

    jsoncons::json get_outputVariableMap_value() const { return get_or_ref_value_node("outputVariableMap"); }
    std::string get_outputVariableMap_ref() const { return get_or_ref_ref_node("outputVariableMap").as<std::string>(); }
    void set_outputVariableMap_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariableMap", value); }
    void set_outputVariableMap_ref(const std::string& ref) { set_or_ref_ref_node("outputVariableMap", ref); }
    bool is_outputVariableMap_ref() const { return is_or_ref_ref("outputVariableMap"); }
    bool is_set_outputVariableMap() const { return values_.count("outputVariableMap") > 0; }
    void unset_outputVariableMap() { values_.erase("outputVariableMap"); or_ref_is_ref_.erase("outputVariableMap"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<std::string> get_loopVariables() const { return loopVariables_.ids(); }
    SedBase* get_loopVariables_item(const std::string& item_id) const { return loopVariables_.get(item_id); }
    void add_loopVariables(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); loopVariables_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_loopVariables(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); loopVariables_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_loopVariables(const std::string& item_id) { loopVariables_.remove(item_id); }
    void set_id_on_loopVariables(const std::string& old_id, const std::string& new_id) { loopVariables_.set_id(old_id, new_id); }

    std::vector<std::string> get_subTasks() const { return subTasks_.ids(); }
    SedBase* get_subTasks_item(const std::string& item_id) const { return subTasks_.get(item_id); }
    void add_subTasks(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); subTasks_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_subTasks(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); subTasks_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_subTasks(const std::string& item_id) { subTasks_.remove(item_id); }
    void set_id_on_subTasks(const std::string& old_id, const std::string& new_id) { subTasks_.set_id(old_id, new_id); }

    std::vector<std::string> get_aggregateOutputVariables() const { return aggregateOutputVariables_.ids(); }
    SedBase* get_aggregateOutputVariables_item(const std::string& item_id) const { return aggregateOutputVariables_.get(item_id); }
    void add_aggregateOutputVariables(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); aggregateOutputVariables_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_aggregateOutputVariables(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); aggregateOutputVariables_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_aggregateOutputVariables(const std::string& item_id) { aggregateOutputVariables_.remove(item_id); }
    void set_id_on_aggregateOutputVariables(const std::string& old_id, const std::string& new_id) { aggregateOutputVariables_.set_id(old_id, new_id); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_range() const { if (!range_) throw ApiError(std::string("range") + " is not set"); return range_.get(); }
    void set_range(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); range_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_range() const { return range_ != nullptr; }
    void unset_range() { range_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : loopVariables_.ids()) kids.push_back(loopVariables_.get(i));
        for (const auto& i : subTasks_.ids()) kids.push_back(subTasks_.get(i));
        for (const auto& i : aggregateOutputVariables_.ids()) kids.push_back(aggregateOutputVariables_.get(i));
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (range_) kids.push_back(range_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : loopVariables_.ids()) out.push_back(ChildLoc{loopVariables_.get(i), "/loopVariables/" + i});
        for (const auto& i : subTasks_.ids()) out.push_back(ChildLoc{subTasks_.get(i), "/subTasks/" + i});
        for (const auto& i : aggregateOutputVariables_.ids()) out.push_back(ChildLoc{aggregateOutputVariables_.get(i), "/aggregateOutputVariables/" + i});
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (range_) out.push_back(ChildLoc{range_.get(), "/range"});
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "loopVariables") return loopVariables_;
        if (field_name == "subTasks") return subTasks_;
        if (field_name == "aggregateOutputVariables") return aggregateOutputVariables_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "range") { range_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("loop");
        if (values_.count("outputVariableMap")) d["outputVariableMap"] = values_.at("outputVariableMap");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (loopVariables_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : loopVariables_.ids()) sub[i] = loopVariables_.get(i)->to_json_value(); d["loopVariables"] = sub; }
        if (subTasks_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : subTasks_.ids()) sub[i] = subTasks_.get(i)->to_json_value(); d["subTasks"] = sub; }
        if (aggregateOutputVariables_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : aggregateOutputVariables_.ids()) sub[i] = aggregateOutputVariables_.get(i)->to_json_value(); d["aggregateOutputVariables"] = sub; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (range_) d["range"] = range_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection loopVariables_;
    IdKeyedCollection subTasks_;
    IdKeyedCollection aggregateOutputVariables_;
    ListCollection taskParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> range_;
};

/// Generated from test-specsheets/tasks/ModelChange/.
class ModelChange : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"inputModel", "SIdRef", true, std::string("ModelChange-0002"), std::string("ModelChange-0001"), "ModelChange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"setValues", "DictOrRef", false, std::string("ModelChange-0003"), std::nullopt, "ModelChange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"removeElements", "ArrayOrRef", false, std::string("ModelChange-0005"), std::nullopt, "ModelChange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"addElements", "ArrayOrRef", false, std::string("ModelChange-0007"), std::nullopt, "ModelChange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"replaceElements", "DictOrRef", false, std::string("ModelChange-0009"), std::nullopt, "ModelChange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"inputModel"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("modelChange"); }
    std::optional<std::string> type_rule_id() const override { return std::string("ModelChange-0011"); }
    std::string own_catchall() const override { return "ModelChange-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "ModelChange"; }
    std::string get_type() const { return "modelChange"; }

    std::string get_inputModel() const { auto it = values_.find("inputModel"); if (it == values_.end()) throw ApiError(std::string("inputModel") + " is not set"); return it->second.as<std::string>(); }
    void set_inputModel(const std::string& value) { values_["inputModel"] = jsoncons::json(value); }
    bool is_set_inputModel() const { return values_.count("inputModel") > 0; }
    void unset_inputModel() { values_.erase("inputModel"); }

    jsoncons::json get_setValues_value() const { return get_or_ref_value_node("setValues"); }
    std::string get_setValues_ref() const { return get_or_ref_ref_node("setValues").as<std::string>(); }
    void set_setValues_value(const jsoncons::json& value) { set_or_ref_value_node("setValues", value); }
    void set_setValues_ref(const std::string& ref) { set_or_ref_ref_node("setValues", ref); }
    bool is_setValues_ref() const { return is_or_ref_ref("setValues"); }
    bool is_set_setValues() const { return values_.count("setValues") > 0; }
    void unset_setValues() { values_.erase("setValues"); or_ref_is_ref_.erase("setValues"); }

    jsoncons::json get_removeElements_value() const { return get_or_ref_value_node("removeElements"); }
    std::string get_removeElements_ref() const { return get_or_ref_ref_node("removeElements").as<std::string>(); }
    void set_removeElements_value(const jsoncons::json& value) { set_or_ref_value_node("removeElements", value); }
    void set_removeElements_ref(const std::string& ref) { set_or_ref_ref_node("removeElements", ref); }
    bool is_removeElements_ref() const { return is_or_ref_ref("removeElements"); }
    bool is_set_removeElements() const { return values_.count("removeElements") > 0; }
    void unset_removeElements() { values_.erase("removeElements"); or_ref_is_ref_.erase("removeElements"); }

    jsoncons::json get_addElements_value() const { return get_or_ref_value_node("addElements"); }
    std::string get_addElements_ref() const { return get_or_ref_ref_node("addElements").as<std::string>(); }
    void set_addElements_value(const jsoncons::json& value) { set_or_ref_value_node("addElements", value); }
    void set_addElements_ref(const std::string& ref) { set_or_ref_ref_node("addElements", ref); }
    bool is_addElements_ref() const { return is_or_ref_ref("addElements"); }
    bool is_set_addElements() const { return values_.count("addElements") > 0; }
    void unset_addElements() { values_.erase("addElements"); or_ref_is_ref_.erase("addElements"); }

    jsoncons::json get_replaceElements_value() const { return get_or_ref_value_node("replaceElements"); }
    std::string get_replaceElements_ref() const { return get_or_ref_ref_node("replaceElements").as<std::string>(); }
    void set_replaceElements_value(const jsoncons::json& value) { set_or_ref_value_node("replaceElements", value); }
    void set_replaceElements_ref(const std::string& ref) { set_or_ref_ref_node("replaceElements", ref); }
    bool is_replaceElements_ref() const { return is_or_ref_ref("replaceElements"); }
    bool is_set_replaceElements() const { return values_.count("replaceElements") > 0; }
    void unset_replaceElements() { values_.erase("replaceElements"); or_ref_is_ref_.erase("replaceElements"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("modelChange");
        if (values_.count("inputModel")) d["inputModel"] = values_.at("inputModel");
        if (values_.count("setValues")) d["setValues"] = values_.at("setValues");
        if (values_.count("removeElements")) d["removeElements"] = values_.at("removeElements");
        if (values_.count("addElements")) d["addElements"] = values_.at("addElements");
        if (values_.count("replaceElements")) d["replaceElements"] = values_.at("replaceElements");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/ModelElementList/.
class ModelElementList : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("ModelElementList-0002"), std::string("ModelElementList-0001"), "ModelElementList-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"includeElements", "ArrayOrRef", false, std::string("ModelElementList-0003"), std::nullopt, "ModelElementList-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"includeTypes", "ArrayOrRef", false, std::string("ModelElementList-0005"), std::nullopt, "ModelElementList-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"excludeElements", "ArrayOrRef", false, std::string("ModelElementList-0007"), std::nullopt, "ModelElementList-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"excludeTypes", "ArrayOrRef", false, std::string("ModelElementList-0009"), std::nullopt, "ModelElementList-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"model"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("modelElementList"); }
    std::optional<std::string> type_rule_id() const override { return std::string("ModelElementList-0011"); }
    std::string own_catchall() const override { return "ModelElementList-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "ModelElementList"; }
    std::string get_type() const { return "modelElementList"; }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    jsoncons::json get_includeElements_value() const { return get_or_ref_value_node("includeElements"); }
    std::string get_includeElements_ref() const { return get_or_ref_ref_node("includeElements").as<std::string>(); }
    void set_includeElements_value(const jsoncons::json& value) { set_or_ref_value_node("includeElements", value); }
    void set_includeElements_ref(const std::string& ref) { set_or_ref_ref_node("includeElements", ref); }
    bool is_includeElements_ref() const { return is_or_ref_ref("includeElements"); }
    bool is_set_includeElements() const { return values_.count("includeElements") > 0; }
    void unset_includeElements() { values_.erase("includeElements"); or_ref_is_ref_.erase("includeElements"); }

    jsoncons::json get_includeTypes_value() const { return get_or_ref_value_node("includeTypes"); }
    std::string get_includeTypes_ref() const { return get_or_ref_ref_node("includeTypes").as<std::string>(); }
    void set_includeTypes_value(const jsoncons::json& value) { set_or_ref_value_node("includeTypes", value); }
    void set_includeTypes_ref(const std::string& ref) { set_or_ref_ref_node("includeTypes", ref); }
    bool is_includeTypes_ref() const { return is_or_ref_ref("includeTypes"); }
    bool is_set_includeTypes() const { return values_.count("includeTypes") > 0; }
    void unset_includeTypes() { values_.erase("includeTypes"); or_ref_is_ref_.erase("includeTypes"); }

    jsoncons::json get_excludeElements_value() const { return get_or_ref_value_node("excludeElements"); }
    std::string get_excludeElements_ref() const { return get_or_ref_ref_node("excludeElements").as<std::string>(); }
    void set_excludeElements_value(const jsoncons::json& value) { set_or_ref_value_node("excludeElements", value); }
    void set_excludeElements_ref(const std::string& ref) { set_or_ref_ref_node("excludeElements", ref); }
    bool is_excludeElements_ref() const { return is_or_ref_ref("excludeElements"); }
    bool is_set_excludeElements() const { return values_.count("excludeElements") > 0; }
    void unset_excludeElements() { values_.erase("excludeElements"); or_ref_is_ref_.erase("excludeElements"); }

    jsoncons::json get_excludeTypes_value() const { return get_or_ref_value_node("excludeTypes"); }
    std::string get_excludeTypes_ref() const { return get_or_ref_ref_node("excludeTypes").as<std::string>(); }
    void set_excludeTypes_value(const jsoncons::json& value) { set_or_ref_value_node("excludeTypes", value); }
    void set_excludeTypes_ref(const std::string& ref) { set_or_ref_ref_node("excludeTypes", ref); }
    bool is_excludeTypes_ref() const { return is_or_ref_ref("excludeTypes"); }
    bool is_set_excludeTypes() const { return values_.count("excludeTypes") > 0; }
    void unset_excludeTypes() { values_.erase("excludeTypes"); or_ref_is_ref_.erase("excludeTypes"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("modelElementList");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("includeElements")) d["includeElements"] = values_.at("includeElements");
        if (values_.count("includeTypes")) d["includeTypes"] = values_.at("includeTypes");
        if (values_.count("excludeElements")) d["excludeElements"] = values_.at("excludeElements");
        if (values_.count("excludeTypes")) d["excludeTypes"] = values_.at("excludeTypes");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/ModelImport/.
class ModelImport : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"location", "StringOrRef", true, std::string("ModelImport-0002"), std::string("ModelImport-0001"), "ModelImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"language", "StringOrRef", true, std::string("ModelImport-0005"), std::string("ModelImport-0004"), "ModelImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"location", "language"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("modelImport"); }
    std::optional<std::string> type_rule_id() const override { return std::string("ModelImport-0007"); }
    std::string own_catchall() const override { return "ModelImport-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "ModelImport"; }
    std::string get_type() const { return "modelImport"; }

    std::string get_location_value() const { return get_or_ref_value_node("location").as<std::string>(); }
    std::string get_location_ref() const { return get_or_ref_ref_node("location").as<std::string>(); }
    void set_location_value(const std::string& value) { set_or_ref_value_node("location", jsoncons::json(value)); }
    void set_location_ref(const std::string& ref) { set_or_ref_ref_node("location", ref); }
    bool is_location_ref() const { return is_or_ref_ref("location"); }
    bool is_set_location() const { return values_.count("location") > 0; }
    void unset_location() { values_.erase("location"); or_ref_is_ref_.erase("location"); }

    std::string get_language_value() const { return get_or_ref_value_node("language").as<std::string>(); }
    std::string get_language_ref() const { return get_or_ref_ref_node("language").as<std::string>(); }
    void set_language_value(const std::string& value) { set_or_ref_value_node("language", jsoncons::json(value)); }
    void set_language_ref(const std::string& ref) { set_or_ref_ref_node("language", ref); }
    bool is_language_ref() const { return is_or_ref_ref("language"); }
    bool is_set_language() const { return values_.count("language") > 0; }
    void unset_language() { values_.erase("language"); or_ref_is_ref_.erase("language"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("modelImport");
        if (values_.count("location")) d["location"] = values_.at("location");
        if (values_.count("language")) d["language"] = values_.at("language");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/NumericRange/.
class NumericRange : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"start", "NumberOrRef", false, std::string("NumericRange-0001"), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"end", "NumberOrRef", false, std::string("NumericRange-0003"), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"interval", "NumberOrRef", false, std::string("NumericRange-0005"), std::nullopt, "NumericRange-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"numberOfSteps", "IntegerOrRef", false, std::string("NumericRange-0007"), std::nullopt, "NumericRange-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"scale", "StringOrRef", false, std::string("NumericRange-0009"), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"values", "ArrayOrRef", false, std::string("NumericRange-0011"), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"values", "ArrayOrRef", false, std::string("Range-0001"), std::nullopt, "Range-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    std::optional<std::string> type_const() const override { return std::string("numericRange"); }
    std::optional<std::string> type_rule_id() const override { return std::string("NumericRange-0013"); }
    std::string own_catchall() const override { return "NumericRange-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "NumericRange"; }
    std::string get_type() const { return "numericRange"; }

    double get_start_value() const { return get_or_ref_value_node("start").as<double>(); }
    std::string get_start_ref() const { return get_or_ref_ref_node("start").as<std::string>(); }
    void set_start_value(double value) { set_or_ref_value_node("start", jsoncons::json(value)); }
    void set_start_ref(const std::string& ref) { set_or_ref_ref_node("start", ref); }
    bool is_start_ref() const { return is_or_ref_ref("start"); }
    bool is_set_start() const { return values_.count("start") > 0; }
    void unset_start() { values_.erase("start"); or_ref_is_ref_.erase("start"); }

    double get_end_value() const { return get_or_ref_value_node("end").as<double>(); }
    std::string get_end_ref() const { return get_or_ref_ref_node("end").as<std::string>(); }
    void set_end_value(double value) { set_or_ref_value_node("end", jsoncons::json(value)); }
    void set_end_ref(const std::string& ref) { set_or_ref_ref_node("end", ref); }
    bool is_end_ref() const { return is_or_ref_ref("end"); }
    bool is_set_end() const { return values_.count("end") > 0; }
    void unset_end() { values_.erase("end"); or_ref_is_ref_.erase("end"); }

    double get_interval_value() const { return get_or_ref_value_node("interval").as<double>(); }
    std::string get_interval_ref() const { return get_or_ref_ref_node("interval").as<std::string>(); }
    void set_interval_value(double value) { set_or_ref_value_node("interval", jsoncons::json(value)); }
    void set_interval_ref(const std::string& ref) { set_or_ref_ref_node("interval", ref); }
    bool is_interval_ref() const { return is_or_ref_ref("interval"); }
    bool is_set_interval() const { return values_.count("interval") > 0; }
    void unset_interval() { values_.erase("interval"); or_ref_is_ref_.erase("interval"); }

    int64_t get_numberOfSteps_value() const { return get_or_ref_value_node("numberOfSteps").as<int64_t>(); }
    std::string get_numberOfSteps_ref() const { return get_or_ref_ref_node("numberOfSteps").as<std::string>(); }
    void set_numberOfSteps_value(int64_t value) { set_or_ref_value_node("numberOfSteps", jsoncons::json(value)); }
    void set_numberOfSteps_ref(const std::string& ref) { set_or_ref_ref_node("numberOfSteps", ref); }
    bool is_numberOfSteps_ref() const { return is_or_ref_ref("numberOfSteps"); }
    bool is_set_numberOfSteps() const { return values_.count("numberOfSteps") > 0; }
    void unset_numberOfSteps() { values_.erase("numberOfSteps"); or_ref_is_ref_.erase("numberOfSteps"); }

    std::string get_scale_value() const { return get_or_ref_value_node("scale").as<std::string>(); }
    std::string get_scale_ref() const { return get_or_ref_ref_node("scale").as<std::string>(); }
    void set_scale_value(const std::string& value) { set_or_ref_value_node("scale", jsoncons::json(value)); }
    void set_scale_ref(const std::string& ref) { set_or_ref_ref_node("scale", ref); }
    bool is_scale_ref() const { return is_or_ref_ref("scale"); }
    bool is_set_scale() const { return values_.count("scale") > 0; }
    void unset_scale() { values_.erase("scale"); or_ref_is_ref_.erase("scale"); }

    jsoncons::json get_values_value() const { return get_or_ref_value_node("values"); }
    std::string get_values_ref() const { return get_or_ref_ref_node("values").as<std::string>(); }
    void set_values_value(const jsoncons::json& value) { set_or_ref_value_node("values", value); }
    void set_values_ref(const std::string& ref) { set_or_ref_ref_node("values", ref); }
    bool is_values_ref() const { return is_or_ref_ref("values"); }
    bool is_set_values() const { return values_.count("values") > 0; }
    void unset_values() { values_.erase("values"); or_ref_is_ref_.erase("values"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("numericRange");
        if (values_.count("start")) d["start"] = values_.at("start");
        if (values_.count("end")) d["end"] = values_.at("end");
        if (values_.count("interval")) d["interval"] = values_.at("interval");
        if (values_.count("numberOfSteps")) d["numberOfSteps"] = values_.at("numberOfSteps");
        if (values_.count("scale")) d["scale"] = values_.at("scale");
        if (values_.count("values")) d["values"] = values_.at("values");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/OneStepODESimulation/.
class OneStepODESimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"independentStep", "NumberOrRef", true, std::string("OneStepODESimulation-0005"), std::string("OneStepODESimulation-0004"), "OneStepODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"relativeTolerance", "NumberOrRef", false, std::string("AbstractODESimulation-0001"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteTolerance", "NumberOrRef", false, std::string("AbstractODESimulation-0003"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceVector", "ArrayOrRef", false, std::string("AbstractODESimulation-0005"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceAdjustmentFactor", "NumberOrRef", false, std::string("AbstractODESimulation-0007"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"toleranceForRootFinder", "NumberOrRef", false, std::string("AbstractODESimulation-0009"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"initialStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0011"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumberOfSteps", "NumberOrRef", false, std::string("AbstractODESimulation-0013"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalSteps", "IntegerOrRef", false, std::string("AbstractODESimulation-0015"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0017"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minInternalStepSize", "NumberOrRef", false, std::string("AbstractODESimulation-0019"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"forcePhysicalCorrectness", "BooleanOrRef", false, std::string("AbstractODESimulation-0021"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"integrateReducedModel", "BooleanOrRef", false, std::string("AbstractODESimulation-0023"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"useReducedModel", "BooleanOrRef", false, std::string("AbstractODESimulation-0025"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"useStiffSolver", "BooleanOrRef", false, std::string("AbstractODESimulation-0027"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxBDForder", "IntegerOrRef", false, std::string("AbstractODESimulation-0029"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxAdamsOrder", "IntegerOrRef", false, std::string("AbstractODESimulation-0031"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"variableStepSize", "BooleanOrRef", false, std::string("AbstractODESimulation-0033"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxOutputRows", "IntegerOrRef", false, std::string("AbstractODESimulation-0035"), std::nullopt, "AbstractODESimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string("AbstractSimulation-0002"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string("AbstractSimulation-0004"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariables", "ArrayOrRef", false, std::string("AbstractSimulation-0006"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"independentStep"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("oneStepODE"); }
    std::optional<std::string> type_rule_id() const override { return std::string("OneStepODESimulation-0007"); }
    std::string own_catchall() const override { return "OneStepODESimulation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "OneStepODESimulation"; }
    std::string get_type() const { return "oneStepODE"; }

    double get_independentStep_value() const { return get_or_ref_value_node("independentStep").as<double>(); }
    std::string get_independentStep_ref() const { return get_or_ref_ref_node("independentStep").as<std::string>(); }
    void set_independentStep_value(double value) { set_or_ref_value_node("independentStep", jsoncons::json(value)); }
    void set_independentStep_ref(const std::string& ref) { set_or_ref_ref_node("independentStep", ref); }
    bool is_independentStep_ref() const { return is_or_ref_ref("independentStep"); }
    bool is_set_independentStep() const { return values_.count("independentStep") > 0; }
    void unset_independentStep() { values_.erase("independentStep"); or_ref_is_ref_.erase("independentStep"); }

    double get_relativeTolerance_value() const { return get_or_ref_value_node("relativeTolerance").as<double>(); }
    std::string get_relativeTolerance_ref() const { return get_or_ref_ref_node("relativeTolerance").as<std::string>(); }
    void set_relativeTolerance_value(double value) { set_or_ref_value_node("relativeTolerance", jsoncons::json(value)); }
    void set_relativeTolerance_ref(const std::string& ref) { set_or_ref_ref_node("relativeTolerance", ref); }
    bool is_relativeTolerance_ref() const { return is_or_ref_ref("relativeTolerance"); }
    bool is_set_relativeTolerance() const { return values_.count("relativeTolerance") > 0; }
    void unset_relativeTolerance() { values_.erase("relativeTolerance"); or_ref_is_ref_.erase("relativeTolerance"); }

    double get_absoluteTolerance_value() const { return get_or_ref_value_node("absoluteTolerance").as<double>(); }
    std::string get_absoluteTolerance_ref() const { return get_or_ref_ref_node("absoluteTolerance").as<std::string>(); }
    void set_absoluteTolerance_value(double value) { set_or_ref_value_node("absoluteTolerance", jsoncons::json(value)); }
    void set_absoluteTolerance_ref(const std::string& ref) { set_or_ref_ref_node("absoluteTolerance", ref); }
    bool is_absoluteTolerance_ref() const { return is_or_ref_ref("absoluteTolerance"); }
    bool is_set_absoluteTolerance() const { return values_.count("absoluteTolerance") > 0; }
    void unset_absoluteTolerance() { values_.erase("absoluteTolerance"); or_ref_is_ref_.erase("absoluteTolerance"); }

    jsoncons::json get_absoluteToleranceVector_value() const { return get_or_ref_value_node("absoluteToleranceVector"); }
    std::string get_absoluteToleranceVector_ref() const { return get_or_ref_ref_node("absoluteToleranceVector").as<std::string>(); }
    void set_absoluteToleranceVector_value(const jsoncons::json& value) { set_or_ref_value_node("absoluteToleranceVector", value); }
    void set_absoluteToleranceVector_ref(const std::string& ref) { set_or_ref_ref_node("absoluteToleranceVector", ref); }
    bool is_absoluteToleranceVector_ref() const { return is_or_ref_ref("absoluteToleranceVector"); }
    bool is_set_absoluteToleranceVector() const { return values_.count("absoluteToleranceVector") > 0; }
    void unset_absoluteToleranceVector() { values_.erase("absoluteToleranceVector"); or_ref_is_ref_.erase("absoluteToleranceVector"); }

    double get_absoluteToleranceAdjustmentFactor_value() const { return get_or_ref_value_node("absoluteToleranceAdjustmentFactor").as<double>(); }
    std::string get_absoluteToleranceAdjustmentFactor_ref() const { return get_or_ref_ref_node("absoluteToleranceAdjustmentFactor").as<std::string>(); }
    void set_absoluteToleranceAdjustmentFactor_value(double value) { set_or_ref_value_node("absoluteToleranceAdjustmentFactor", jsoncons::json(value)); }
    void set_absoluteToleranceAdjustmentFactor_ref(const std::string& ref) { set_or_ref_ref_node("absoluteToleranceAdjustmentFactor", ref); }
    bool is_absoluteToleranceAdjustmentFactor_ref() const { return is_or_ref_ref("absoluteToleranceAdjustmentFactor"); }
    bool is_set_absoluteToleranceAdjustmentFactor() const { return values_.count("absoluteToleranceAdjustmentFactor") > 0; }
    void unset_absoluteToleranceAdjustmentFactor() { values_.erase("absoluteToleranceAdjustmentFactor"); or_ref_is_ref_.erase("absoluteToleranceAdjustmentFactor"); }

    double get_toleranceForRootFinder_value() const { return get_or_ref_value_node("toleranceForRootFinder").as<double>(); }
    std::string get_toleranceForRootFinder_ref() const { return get_or_ref_ref_node("toleranceForRootFinder").as<std::string>(); }
    void set_toleranceForRootFinder_value(double value) { set_or_ref_value_node("toleranceForRootFinder", jsoncons::json(value)); }
    void set_toleranceForRootFinder_ref(const std::string& ref) { set_or_ref_ref_node("toleranceForRootFinder", ref); }
    bool is_toleranceForRootFinder_ref() const { return is_or_ref_ref("toleranceForRootFinder"); }
    bool is_set_toleranceForRootFinder() const { return values_.count("toleranceForRootFinder") > 0; }
    void unset_toleranceForRootFinder() { values_.erase("toleranceForRootFinder"); or_ref_is_ref_.erase("toleranceForRootFinder"); }

    double get_initialStepSize_value() const { return get_or_ref_value_node("initialStepSize").as<double>(); }
    std::string get_initialStepSize_ref() const { return get_or_ref_ref_node("initialStepSize").as<std::string>(); }
    void set_initialStepSize_value(double value) { set_or_ref_value_node("initialStepSize", jsoncons::json(value)); }
    void set_initialStepSize_ref(const std::string& ref) { set_or_ref_ref_node("initialStepSize", ref); }
    bool is_initialStepSize_ref() const { return is_or_ref_ref("initialStepSize"); }
    bool is_set_initialStepSize() const { return values_.count("initialStepSize") > 0; }
    void unset_initialStepSize() { values_.erase("initialStepSize"); or_ref_is_ref_.erase("initialStepSize"); }

    double get_maxNumberOfSteps_value() const { return get_or_ref_value_node("maxNumberOfSteps").as<double>(); }
    std::string get_maxNumberOfSteps_ref() const { return get_or_ref_ref_node("maxNumberOfSteps").as<std::string>(); }
    void set_maxNumberOfSteps_value(double value) { set_or_ref_value_node("maxNumberOfSteps", jsoncons::json(value)); }
    void set_maxNumberOfSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxNumberOfSteps", ref); }
    bool is_maxNumberOfSteps_ref() const { return is_or_ref_ref("maxNumberOfSteps"); }
    bool is_set_maxNumberOfSteps() const { return values_.count("maxNumberOfSteps") > 0; }
    void unset_maxNumberOfSteps() { values_.erase("maxNumberOfSteps"); or_ref_is_ref_.erase("maxNumberOfSteps"); }

    int64_t get_maxInternalSteps_value() const { return get_or_ref_value_node("maxInternalSteps").as<int64_t>(); }
    std::string get_maxInternalSteps_ref() const { return get_or_ref_ref_node("maxInternalSteps").as<std::string>(); }
    void set_maxInternalSteps_value(int64_t value) { set_or_ref_value_node("maxInternalSteps", jsoncons::json(value)); }
    void set_maxInternalSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxInternalSteps", ref); }
    bool is_maxInternalSteps_ref() const { return is_or_ref_ref("maxInternalSteps"); }
    bool is_set_maxInternalSteps() const { return values_.count("maxInternalSteps") > 0; }
    void unset_maxInternalSteps() { values_.erase("maxInternalSteps"); or_ref_is_ref_.erase("maxInternalSteps"); }

    double get_maxInternalStepSize_value() const { return get_or_ref_value_node("maxInternalStepSize").as<double>(); }
    std::string get_maxInternalStepSize_ref() const { return get_or_ref_ref_node("maxInternalStepSize").as<std::string>(); }
    void set_maxInternalStepSize_value(double value) { set_or_ref_value_node("maxInternalStepSize", jsoncons::json(value)); }
    void set_maxInternalStepSize_ref(const std::string& ref) { set_or_ref_ref_node("maxInternalStepSize", ref); }
    bool is_maxInternalStepSize_ref() const { return is_or_ref_ref("maxInternalStepSize"); }
    bool is_set_maxInternalStepSize() const { return values_.count("maxInternalStepSize") > 0; }
    void unset_maxInternalStepSize() { values_.erase("maxInternalStepSize"); or_ref_is_ref_.erase("maxInternalStepSize"); }

    double get_minInternalStepSize_value() const { return get_or_ref_value_node("minInternalStepSize").as<double>(); }
    std::string get_minInternalStepSize_ref() const { return get_or_ref_ref_node("minInternalStepSize").as<std::string>(); }
    void set_minInternalStepSize_value(double value) { set_or_ref_value_node("minInternalStepSize", jsoncons::json(value)); }
    void set_minInternalStepSize_ref(const std::string& ref) { set_or_ref_ref_node("minInternalStepSize", ref); }
    bool is_minInternalStepSize_ref() const { return is_or_ref_ref("minInternalStepSize"); }
    bool is_set_minInternalStepSize() const { return values_.count("minInternalStepSize") > 0; }
    void unset_minInternalStepSize() { values_.erase("minInternalStepSize"); or_ref_is_ref_.erase("minInternalStepSize"); }

    bool get_forcePhysicalCorrectness_value() const { return get_or_ref_value_node("forcePhysicalCorrectness").as<bool>(); }
    std::string get_forcePhysicalCorrectness_ref() const { return get_or_ref_ref_node("forcePhysicalCorrectness").as<std::string>(); }
    void set_forcePhysicalCorrectness_value(bool value) { set_or_ref_value_node("forcePhysicalCorrectness", jsoncons::json(value)); }
    void set_forcePhysicalCorrectness_ref(const std::string& ref) { set_or_ref_ref_node("forcePhysicalCorrectness", ref); }
    bool is_forcePhysicalCorrectness_ref() const { return is_or_ref_ref("forcePhysicalCorrectness"); }
    bool is_set_forcePhysicalCorrectness() const { return values_.count("forcePhysicalCorrectness") > 0; }
    void unset_forcePhysicalCorrectness() { values_.erase("forcePhysicalCorrectness"); or_ref_is_ref_.erase("forcePhysicalCorrectness"); }

    bool get_integrateReducedModel_value() const { return get_or_ref_value_node("integrateReducedModel").as<bool>(); }
    std::string get_integrateReducedModel_ref() const { return get_or_ref_ref_node("integrateReducedModel").as<std::string>(); }
    void set_integrateReducedModel_value(bool value) { set_or_ref_value_node("integrateReducedModel", jsoncons::json(value)); }
    void set_integrateReducedModel_ref(const std::string& ref) { set_or_ref_ref_node("integrateReducedModel", ref); }
    bool is_integrateReducedModel_ref() const { return is_or_ref_ref("integrateReducedModel"); }
    bool is_set_integrateReducedModel() const { return values_.count("integrateReducedModel") > 0; }
    void unset_integrateReducedModel() { values_.erase("integrateReducedModel"); or_ref_is_ref_.erase("integrateReducedModel"); }

    bool get_useReducedModel_value() const { return get_or_ref_value_node("useReducedModel").as<bool>(); }
    std::string get_useReducedModel_ref() const { return get_or_ref_ref_node("useReducedModel").as<std::string>(); }
    void set_useReducedModel_value(bool value) { set_or_ref_value_node("useReducedModel", jsoncons::json(value)); }
    void set_useReducedModel_ref(const std::string& ref) { set_or_ref_ref_node("useReducedModel", ref); }
    bool is_useReducedModel_ref() const { return is_or_ref_ref("useReducedModel"); }
    bool is_set_useReducedModel() const { return values_.count("useReducedModel") > 0; }
    void unset_useReducedModel() { values_.erase("useReducedModel"); or_ref_is_ref_.erase("useReducedModel"); }

    bool get_useStiffSolver_value() const { return get_or_ref_value_node("useStiffSolver").as<bool>(); }
    std::string get_useStiffSolver_ref() const { return get_or_ref_ref_node("useStiffSolver").as<std::string>(); }
    void set_useStiffSolver_value(bool value) { set_or_ref_value_node("useStiffSolver", jsoncons::json(value)); }
    void set_useStiffSolver_ref(const std::string& ref) { set_or_ref_ref_node("useStiffSolver", ref); }
    bool is_useStiffSolver_ref() const { return is_or_ref_ref("useStiffSolver"); }
    bool is_set_useStiffSolver() const { return values_.count("useStiffSolver") > 0; }
    void unset_useStiffSolver() { values_.erase("useStiffSolver"); or_ref_is_ref_.erase("useStiffSolver"); }

    int64_t get_maxBDForder_value() const { return get_or_ref_value_node("maxBDForder").as<int64_t>(); }
    std::string get_maxBDForder_ref() const { return get_or_ref_ref_node("maxBDForder").as<std::string>(); }
    void set_maxBDForder_value(int64_t value) { set_or_ref_value_node("maxBDForder", jsoncons::json(value)); }
    void set_maxBDForder_ref(const std::string& ref) { set_or_ref_ref_node("maxBDForder", ref); }
    bool is_maxBDForder_ref() const { return is_or_ref_ref("maxBDForder"); }
    bool is_set_maxBDForder() const { return values_.count("maxBDForder") > 0; }
    void unset_maxBDForder() { values_.erase("maxBDForder"); or_ref_is_ref_.erase("maxBDForder"); }

    int64_t get_maxAdamsOrder_value() const { return get_or_ref_value_node("maxAdamsOrder").as<int64_t>(); }
    std::string get_maxAdamsOrder_ref() const { return get_or_ref_ref_node("maxAdamsOrder").as<std::string>(); }
    void set_maxAdamsOrder_value(int64_t value) { set_or_ref_value_node("maxAdamsOrder", jsoncons::json(value)); }
    void set_maxAdamsOrder_ref(const std::string& ref) { set_or_ref_ref_node("maxAdamsOrder", ref); }
    bool is_maxAdamsOrder_ref() const { return is_or_ref_ref("maxAdamsOrder"); }
    bool is_set_maxAdamsOrder() const { return values_.count("maxAdamsOrder") > 0; }
    void unset_maxAdamsOrder() { values_.erase("maxAdamsOrder"); or_ref_is_ref_.erase("maxAdamsOrder"); }

    bool get_variableStepSize_value() const { return get_or_ref_value_node("variableStepSize").as<bool>(); }
    std::string get_variableStepSize_ref() const { return get_or_ref_ref_node("variableStepSize").as<std::string>(); }
    void set_variableStepSize_value(bool value) { set_or_ref_value_node("variableStepSize", jsoncons::json(value)); }
    void set_variableStepSize_ref(const std::string& ref) { set_or_ref_ref_node("variableStepSize", ref); }
    bool is_variableStepSize_ref() const { return is_or_ref_ref("variableStepSize"); }
    bool is_set_variableStepSize() const { return values_.count("variableStepSize") > 0; }
    void unset_variableStepSize() { values_.erase("variableStepSize"); or_ref_is_ref_.erase("variableStepSize"); }

    int64_t get_maxOutputRows_value() const { return get_or_ref_value_node("maxOutputRows").as<int64_t>(); }
    std::string get_maxOutputRows_ref() const { return get_or_ref_ref_node("maxOutputRows").as<std::string>(); }
    void set_maxOutputRows_value(int64_t value) { set_or_ref_value_node("maxOutputRows", jsoncons::json(value)); }
    void set_maxOutputRows_ref(const std::string& ref) { set_or_ref_ref_node("maxOutputRows", ref); }
    bool is_maxOutputRows_ref() const { return is_or_ref_ref("maxOutputRows"); }
    bool is_set_maxOutputRows() const { return values_.count("maxOutputRows") > 0; }
    void unset_maxOutputRows() { values_.erase("maxOutputRows"); or_ref_is_ref_.erase("maxOutputRows"); }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    std::string get_independentVariable_value() const { return get_or_ref_value_node("independentVariable").as<std::string>(); }
    std::string get_independentVariable_ref() const { return get_or_ref_ref_node("independentVariable").as<std::string>(); }
    void set_independentVariable_value(const std::string& value) { set_or_ref_value_node("independentVariable", jsoncons::json(value)); }
    void set_independentVariable_ref(const std::string& ref) { set_or_ref_ref_node("independentVariable", ref); }
    bool is_independentVariable_ref() const { return is_or_ref_ref("independentVariable"); }
    bool is_set_independentVariable() const { return values_.count("independentVariable") > 0; }
    void unset_independentVariable() { values_.erase("independentVariable"); or_ref_is_ref_.erase("independentVariable"); }

    double get_independentVariableInit_value() const { return get_or_ref_value_node("independentVariableInit").as<double>(); }
    std::string get_independentVariableInit_ref() const { return get_or_ref_ref_node("independentVariableInit").as<std::string>(); }
    void set_independentVariableInit_value(double value) { set_or_ref_value_node("independentVariableInit", jsoncons::json(value)); }
    void set_independentVariableInit_ref(const std::string& ref) { set_or_ref_ref_node("independentVariableInit", ref); }
    bool is_independentVariableInit_ref() const { return is_or_ref_ref("independentVariableInit"); }
    bool is_set_independentVariableInit() const { return values_.count("independentVariableInit") > 0; }
    void unset_independentVariableInit() { values_.erase("independentVariableInit"); or_ref_is_ref_.erase("independentVariableInit"); }

    jsoncons::json get_outputVariables_value() const { return get_or_ref_value_node("outputVariables"); }
    std::string get_outputVariables_ref() const { return get_or_ref_ref_node("outputVariables").as<std::string>(); }
    void set_outputVariables_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariables", value); }
    void set_outputVariables_ref(const std::string& ref) { set_or_ref_ref_node("outputVariables", ref); }
    bool is_outputVariables_ref() const { return is_or_ref_ref("outputVariables"); }
    bool is_set_outputVariables() const { return values_.count("outputVariables") > 0; }
    void unset_outputVariables() { values_.erase("outputVariables"); or_ref_is_ref_.erase("outputVariables"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("oneStepODE");
        if (values_.count("independentStep")) d["independentStep"] = values_.at("independentStep");
        if (values_.count("relativeTolerance")) d["relativeTolerance"] = values_.at("relativeTolerance");
        if (values_.count("absoluteTolerance")) d["absoluteTolerance"] = values_.at("absoluteTolerance");
        if (values_.count("absoluteToleranceVector")) d["absoluteToleranceVector"] = values_.at("absoluteToleranceVector");
        if (values_.count("absoluteToleranceAdjustmentFactor")) d["absoluteToleranceAdjustmentFactor"] = values_.at("absoluteToleranceAdjustmentFactor");
        if (values_.count("toleranceForRootFinder")) d["toleranceForRootFinder"] = values_.at("toleranceForRootFinder");
        if (values_.count("initialStepSize")) d["initialStepSize"] = values_.at("initialStepSize");
        if (values_.count("maxNumberOfSteps")) d["maxNumberOfSteps"] = values_.at("maxNumberOfSteps");
        if (values_.count("maxInternalSteps")) d["maxInternalSteps"] = values_.at("maxInternalSteps");
        if (values_.count("maxInternalStepSize")) d["maxInternalStepSize"] = values_.at("maxInternalStepSize");
        if (values_.count("minInternalStepSize")) d["minInternalStepSize"] = values_.at("minInternalStepSize");
        if (values_.count("forcePhysicalCorrectness")) d["forcePhysicalCorrectness"] = values_.at("forcePhysicalCorrectness");
        if (values_.count("integrateReducedModel")) d["integrateReducedModel"] = values_.at("integrateReducedModel");
        if (values_.count("useReducedModel")) d["useReducedModel"] = values_.at("useReducedModel");
        if (values_.count("useStiffSolver")) d["useStiffSolver"] = values_.at("useStiffSolver");
        if (values_.count("maxBDForder")) d["maxBDForder"] = values_.at("maxBDForder");
        if (values_.count("maxAdamsOrder")) d["maxAdamsOrder"] = values_.at("maxAdamsOrder");
        if (values_.count("variableStepSize")) d["variableStepSize"] = values_.at("variableStepSize");
        if (values_.count("maxOutputRows")) d["maxOutputRows"] = values_.at("maxOutputRows");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (values_.count("outputVariables")) d["outputVariables"] = values_.at("outputVariables");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/OneStepStochasticSimulation/.
class OneStepStochasticSimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"independentStep", "NumberOrRef", false, std::string("OneStepStochasticSimulation-0004"), std::nullopt, "OneStepStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"seed", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0001"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"timeDependentRelativeTolerance", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0003"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"variableStepSize", "BooleanOrRef", false, std::string("AbstractStochasticSimulation-0005"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minimumTimeStep", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0007"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maximumTimeStep", "NumberOrRef", false, std::string("AbstractStochasticSimulation-0009"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"nonNegative", "BooleanOrRef", false, std::string("AbstractStochasticSimulation-0011"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxOutputRows", "IntegerOrRef", false, std::string("AbstractStochasticSimulation-0013"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumSteps", "IntegerOrRef", false, std::string("AbstractStochasticSimulation-0015"), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string("AbstractSimulation-0002"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string("AbstractSimulation-0004"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariables", "ArrayOrRef", false, std::string("AbstractSimulation-0006"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    std::optional<std::string> type_const() const override { return std::string("oneStepStochastic"); }
    std::optional<std::string> type_rule_id() const override { return std::string("OneStepStochasticSimulation-0006"); }
    std::string own_catchall() const override { return "OneStepStochasticSimulation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "OneStepStochasticSimulation"; }
    std::string get_type() const { return "oneStepStochastic"; }

    double get_independentStep_value() const { return get_or_ref_value_node("independentStep").as<double>(); }
    std::string get_independentStep_ref() const { return get_or_ref_ref_node("independentStep").as<std::string>(); }
    void set_independentStep_value(double value) { set_or_ref_value_node("independentStep", jsoncons::json(value)); }
    void set_independentStep_ref(const std::string& ref) { set_or_ref_ref_node("independentStep", ref); }
    bool is_independentStep_ref() const { return is_or_ref_ref("independentStep"); }
    bool is_set_independentStep() const { return values_.count("independentStep") > 0; }
    void unset_independentStep() { values_.erase("independentStep"); or_ref_is_ref_.erase("independentStep"); }

    double get_seed_value() const { return get_or_ref_value_node("seed").as<double>(); }
    std::string get_seed_ref() const { return get_or_ref_ref_node("seed").as<std::string>(); }
    void set_seed_value(double value) { set_or_ref_value_node("seed", jsoncons::json(value)); }
    void set_seed_ref(const std::string& ref) { set_or_ref_ref_node("seed", ref); }
    bool is_seed_ref() const { return is_or_ref_ref("seed"); }
    bool is_set_seed() const { return values_.count("seed") > 0; }
    void unset_seed() { values_.erase("seed"); or_ref_is_ref_.erase("seed"); }

    double get_timeDependentRelativeTolerance_value() const { return get_or_ref_value_node("timeDependentRelativeTolerance").as<double>(); }
    std::string get_timeDependentRelativeTolerance_ref() const { return get_or_ref_ref_node("timeDependentRelativeTolerance").as<std::string>(); }
    void set_timeDependentRelativeTolerance_value(double value) { set_or_ref_value_node("timeDependentRelativeTolerance", jsoncons::json(value)); }
    void set_timeDependentRelativeTolerance_ref(const std::string& ref) { set_or_ref_ref_node("timeDependentRelativeTolerance", ref); }
    bool is_timeDependentRelativeTolerance_ref() const { return is_or_ref_ref("timeDependentRelativeTolerance"); }
    bool is_set_timeDependentRelativeTolerance() const { return values_.count("timeDependentRelativeTolerance") > 0; }
    void unset_timeDependentRelativeTolerance() { values_.erase("timeDependentRelativeTolerance"); or_ref_is_ref_.erase("timeDependentRelativeTolerance"); }

    bool get_variableStepSize_value() const { return get_or_ref_value_node("variableStepSize").as<bool>(); }
    std::string get_variableStepSize_ref() const { return get_or_ref_ref_node("variableStepSize").as<std::string>(); }
    void set_variableStepSize_value(bool value) { set_or_ref_value_node("variableStepSize", jsoncons::json(value)); }
    void set_variableStepSize_ref(const std::string& ref) { set_or_ref_ref_node("variableStepSize", ref); }
    bool is_variableStepSize_ref() const { return is_or_ref_ref("variableStepSize"); }
    bool is_set_variableStepSize() const { return values_.count("variableStepSize") > 0; }
    void unset_variableStepSize() { values_.erase("variableStepSize"); or_ref_is_ref_.erase("variableStepSize"); }

    double get_minimumTimeStep_value() const { return get_or_ref_value_node("minimumTimeStep").as<double>(); }
    std::string get_minimumTimeStep_ref() const { return get_or_ref_ref_node("minimumTimeStep").as<std::string>(); }
    void set_minimumTimeStep_value(double value) { set_or_ref_value_node("minimumTimeStep", jsoncons::json(value)); }
    void set_minimumTimeStep_ref(const std::string& ref) { set_or_ref_ref_node("minimumTimeStep", ref); }
    bool is_minimumTimeStep_ref() const { return is_or_ref_ref("minimumTimeStep"); }
    bool is_set_minimumTimeStep() const { return values_.count("minimumTimeStep") > 0; }
    void unset_minimumTimeStep() { values_.erase("minimumTimeStep"); or_ref_is_ref_.erase("minimumTimeStep"); }

    double get_maximumTimeStep_value() const { return get_or_ref_value_node("maximumTimeStep").as<double>(); }
    std::string get_maximumTimeStep_ref() const { return get_or_ref_ref_node("maximumTimeStep").as<std::string>(); }
    void set_maximumTimeStep_value(double value) { set_or_ref_value_node("maximumTimeStep", jsoncons::json(value)); }
    void set_maximumTimeStep_ref(const std::string& ref) { set_or_ref_ref_node("maximumTimeStep", ref); }
    bool is_maximumTimeStep_ref() const { return is_or_ref_ref("maximumTimeStep"); }
    bool is_set_maximumTimeStep() const { return values_.count("maximumTimeStep") > 0; }
    void unset_maximumTimeStep() { values_.erase("maximumTimeStep"); or_ref_is_ref_.erase("maximumTimeStep"); }

    bool get_nonNegative_value() const { return get_or_ref_value_node("nonNegative").as<bool>(); }
    std::string get_nonNegative_ref() const { return get_or_ref_ref_node("nonNegative").as<std::string>(); }
    void set_nonNegative_value(bool value) { set_or_ref_value_node("nonNegative", jsoncons::json(value)); }
    void set_nonNegative_ref(const std::string& ref) { set_or_ref_ref_node("nonNegative", ref); }
    bool is_nonNegative_ref() const { return is_or_ref_ref("nonNegative"); }
    bool is_set_nonNegative() const { return values_.count("nonNegative") > 0; }
    void unset_nonNegative() { values_.erase("nonNegative"); or_ref_is_ref_.erase("nonNegative"); }

    int64_t get_maxOutputRows_value() const { return get_or_ref_value_node("maxOutputRows").as<int64_t>(); }
    std::string get_maxOutputRows_ref() const { return get_or_ref_ref_node("maxOutputRows").as<std::string>(); }
    void set_maxOutputRows_value(int64_t value) { set_or_ref_value_node("maxOutputRows", jsoncons::json(value)); }
    void set_maxOutputRows_ref(const std::string& ref) { set_or_ref_ref_node("maxOutputRows", ref); }
    bool is_maxOutputRows_ref() const { return is_or_ref_ref("maxOutputRows"); }
    bool is_set_maxOutputRows() const { return values_.count("maxOutputRows") > 0; }
    void unset_maxOutputRows() { values_.erase("maxOutputRows"); or_ref_is_ref_.erase("maxOutputRows"); }

    int64_t get_maxNumSteps_value() const { return get_or_ref_value_node("maxNumSteps").as<int64_t>(); }
    std::string get_maxNumSteps_ref() const { return get_or_ref_ref_node("maxNumSteps").as<std::string>(); }
    void set_maxNumSteps_value(int64_t value) { set_or_ref_value_node("maxNumSteps", jsoncons::json(value)); }
    void set_maxNumSteps_ref(const std::string& ref) { set_or_ref_ref_node("maxNumSteps", ref); }
    bool is_maxNumSteps_ref() const { return is_or_ref_ref("maxNumSteps"); }
    bool is_set_maxNumSteps() const { return values_.count("maxNumSteps") > 0; }
    void unset_maxNumSteps() { values_.erase("maxNumSteps"); or_ref_is_ref_.erase("maxNumSteps"); }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    std::string get_independentVariable_value() const { return get_or_ref_value_node("independentVariable").as<std::string>(); }
    std::string get_independentVariable_ref() const { return get_or_ref_ref_node("independentVariable").as<std::string>(); }
    void set_independentVariable_value(const std::string& value) { set_or_ref_value_node("independentVariable", jsoncons::json(value)); }
    void set_independentVariable_ref(const std::string& ref) { set_or_ref_ref_node("independentVariable", ref); }
    bool is_independentVariable_ref() const { return is_or_ref_ref("independentVariable"); }
    bool is_set_independentVariable() const { return values_.count("independentVariable") > 0; }
    void unset_independentVariable() { values_.erase("independentVariable"); or_ref_is_ref_.erase("independentVariable"); }

    double get_independentVariableInit_value() const { return get_or_ref_value_node("independentVariableInit").as<double>(); }
    std::string get_independentVariableInit_ref() const { return get_or_ref_ref_node("independentVariableInit").as<std::string>(); }
    void set_independentVariableInit_value(double value) { set_or_ref_value_node("independentVariableInit", jsoncons::json(value)); }
    void set_independentVariableInit_ref(const std::string& ref) { set_or_ref_ref_node("independentVariableInit", ref); }
    bool is_independentVariableInit_ref() const { return is_or_ref_ref("independentVariableInit"); }
    bool is_set_independentVariableInit() const { return values_.count("independentVariableInit") > 0; }
    void unset_independentVariableInit() { values_.erase("independentVariableInit"); or_ref_is_ref_.erase("independentVariableInit"); }

    jsoncons::json get_outputVariables_value() const { return get_or_ref_value_node("outputVariables"); }
    std::string get_outputVariables_ref() const { return get_or_ref_ref_node("outputVariables").as<std::string>(); }
    void set_outputVariables_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariables", value); }
    void set_outputVariables_ref(const std::string& ref) { set_or_ref_ref_node("outputVariables", ref); }
    bool is_outputVariables_ref() const { return is_or_ref_ref("outputVariables"); }
    bool is_set_outputVariables() const { return values_.count("outputVariables") > 0; }
    void unset_outputVariables() { values_.erase("outputVariables"); or_ref_is_ref_.erase("outputVariables"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("oneStepStochastic");
        if (values_.count("independentStep")) d["independentStep"] = values_.at("independentStep");
        if (values_.count("seed")) d["seed"] = values_.at("seed");
        if (values_.count("timeDependentRelativeTolerance")) d["timeDependentRelativeTolerance"] = values_.at("timeDependentRelativeTolerance");
        if (values_.count("variableStepSize")) d["variableStepSize"] = values_.at("variableStepSize");
        if (values_.count("minimumTimeStep")) d["minimumTimeStep"] = values_.at("minimumTimeStep");
        if (values_.count("maximumTimeStep")) d["maximumTimeStep"] = values_.at("maximumTimeStep");
        if (values_.count("nonNegative")) d["nonNegative"] = values_.at("nonNegative");
        if (values_.count("maxOutputRows")) d["maxOutputRows"] = values_.at("maxOutputRows");
        if (values_.count("maxNumSteps")) d["maxNumSteps"] = values_.at("maxNumSteps");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (values_.count("outputVariables")) d["outputVariables"] = values_.at("outputVariables");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/ParameterRange/.
class ParameterRange : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"modelElement", "StringOrRef", true, std::string("ParameterRange-0002"), std::string("ParameterRange-0001"), "ParameterRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"start", "NumberOrRef", false, std::string("NumericRange-0001"), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"end", "NumberOrRef", false, std::string("NumericRange-0003"), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"interval", "NumberOrRef", false, std::string("NumericRange-0005"), std::nullopt, "NumericRange-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"numberOfSteps", "IntegerOrRef", false, std::string("NumericRange-0007"), std::nullopt, "NumericRange-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"scale", "StringOrRef", false, std::string("NumericRange-0009"), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"values", "ArrayOrRef", false, std::string("NumericRange-0011"), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"values", "ArrayOrRef", false, std::string("Range-0001"), std::nullopt, "Range-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"modelElement"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("parameterRange"); }
    std::optional<std::string> type_rule_id() const override { return std::string("ParameterRange-0016"); }
    std::string own_catchall() const override { return "ParameterRange-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "ParameterRange"; }
    std::string get_type() const { return "parameterRange"; }

    std::string get_modelElement_value() const { return get_or_ref_value_node("modelElement").as<std::string>(); }
    std::string get_modelElement_ref() const { return get_or_ref_ref_node("modelElement").as<std::string>(); }
    void set_modelElement_value(const std::string& value) { set_or_ref_value_node("modelElement", jsoncons::json(value)); }
    void set_modelElement_ref(const std::string& ref) { set_or_ref_ref_node("modelElement", ref); }
    bool is_modelElement_ref() const { return is_or_ref_ref("modelElement"); }
    bool is_set_modelElement() const { return values_.count("modelElement") > 0; }
    void unset_modelElement() { values_.erase("modelElement"); or_ref_is_ref_.erase("modelElement"); }

    double get_start_value() const { return get_or_ref_value_node("start").as<double>(); }
    std::string get_start_ref() const { return get_or_ref_ref_node("start").as<std::string>(); }
    void set_start_value(double value) { set_or_ref_value_node("start", jsoncons::json(value)); }
    void set_start_ref(const std::string& ref) { set_or_ref_ref_node("start", ref); }
    bool is_start_ref() const { return is_or_ref_ref("start"); }
    bool is_set_start() const { return values_.count("start") > 0; }
    void unset_start() { values_.erase("start"); or_ref_is_ref_.erase("start"); }

    double get_end_value() const { return get_or_ref_value_node("end").as<double>(); }
    std::string get_end_ref() const { return get_or_ref_ref_node("end").as<std::string>(); }
    void set_end_value(double value) { set_or_ref_value_node("end", jsoncons::json(value)); }
    void set_end_ref(const std::string& ref) { set_or_ref_ref_node("end", ref); }
    bool is_end_ref() const { return is_or_ref_ref("end"); }
    bool is_set_end() const { return values_.count("end") > 0; }
    void unset_end() { values_.erase("end"); or_ref_is_ref_.erase("end"); }

    double get_interval_value() const { return get_or_ref_value_node("interval").as<double>(); }
    std::string get_interval_ref() const { return get_or_ref_ref_node("interval").as<std::string>(); }
    void set_interval_value(double value) { set_or_ref_value_node("interval", jsoncons::json(value)); }
    void set_interval_ref(const std::string& ref) { set_or_ref_ref_node("interval", ref); }
    bool is_interval_ref() const { return is_or_ref_ref("interval"); }
    bool is_set_interval() const { return values_.count("interval") > 0; }
    void unset_interval() { values_.erase("interval"); or_ref_is_ref_.erase("interval"); }

    int64_t get_numberOfSteps_value() const { return get_or_ref_value_node("numberOfSteps").as<int64_t>(); }
    std::string get_numberOfSteps_ref() const { return get_or_ref_ref_node("numberOfSteps").as<std::string>(); }
    void set_numberOfSteps_value(int64_t value) { set_or_ref_value_node("numberOfSteps", jsoncons::json(value)); }
    void set_numberOfSteps_ref(const std::string& ref) { set_or_ref_ref_node("numberOfSteps", ref); }
    bool is_numberOfSteps_ref() const { return is_or_ref_ref("numberOfSteps"); }
    bool is_set_numberOfSteps() const { return values_.count("numberOfSteps") > 0; }
    void unset_numberOfSteps() { values_.erase("numberOfSteps"); or_ref_is_ref_.erase("numberOfSteps"); }

    std::string get_scale_value() const { return get_or_ref_value_node("scale").as<std::string>(); }
    std::string get_scale_ref() const { return get_or_ref_ref_node("scale").as<std::string>(); }
    void set_scale_value(const std::string& value) { set_or_ref_value_node("scale", jsoncons::json(value)); }
    void set_scale_ref(const std::string& ref) { set_or_ref_ref_node("scale", ref); }
    bool is_scale_ref() const { return is_or_ref_ref("scale"); }
    bool is_set_scale() const { return values_.count("scale") > 0; }
    void unset_scale() { values_.erase("scale"); or_ref_is_ref_.erase("scale"); }

    jsoncons::json get_values_value() const { return get_or_ref_value_node("values"); }
    std::string get_values_ref() const { return get_or_ref_ref_node("values").as<std::string>(); }
    void set_values_value(const jsoncons::json& value) { set_or_ref_value_node("values", value); }
    void set_values_ref(const std::string& ref) { set_or_ref_ref_node("values", ref); }
    bool is_values_ref() const { return is_or_ref_ref("values"); }
    bool is_set_values() const { return values_.count("values") > 0; }
    void unset_values() { values_.erase("values"); or_ref_is_ref_.erase("values"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("parameterRange");
        if (values_.count("modelElement")) d["modelElement"] = values_.at("modelElement");
        if (values_.count("start")) d["start"] = values_.at("start");
        if (values_.count("end")) d["end"] = values_.at("end");
        if (values_.count("interval")) d["interval"] = values_.at("interval");
        if (values_.count("numberOfSteps")) d["numberOfSteps"] = values_.at("numberOfSteps");
        if (values_.count("scale")) d["scale"] = values_.at("scale");
        if (values_.count("values")) d["values"] = values_.at("values");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/ParameterScan/.
class ParameterScan : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("ParameterScan-0002"), std::string("ParameterScan-0001"), "ParameterScan-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariableMap", "DictOrRef", false, std::string("Repeat-0002"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"parameterRanges", "array", true, std::string("ParameterScan-0004"), std::string("ParameterScan-0003"), "ParameterScan-0000", std::nullopt, std::nullopt, std::nullopt, std::string("ParameterRange"), std::nullopt},
            FieldSpec{"subTasks", "dict", false, std::string("Repeat-0001"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractTask")},
            FieldSpec{"aggregateOutputVariables", "dict", false, std::string("Repeat-0004"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::string("AggregationCalculation"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"range", "ref-discriminator", false, std::string("Repeat-0005"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("RangeInline")}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"model", "parameterRanges"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("parameterScan"); }
    std::optional<std::string> type_rule_id() const override { return std::string("ParameterScan-0006"); }
    std::string own_catchall() const override { return "ParameterScan-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "ParameterScan"; }
    std::string get_type() const { return "parameterScan"; }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    jsoncons::json get_outputVariableMap_value() const { return get_or_ref_value_node("outputVariableMap"); }
    std::string get_outputVariableMap_ref() const { return get_or_ref_ref_node("outputVariableMap").as<std::string>(); }
    void set_outputVariableMap_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariableMap", value); }
    void set_outputVariableMap_ref(const std::string& ref) { set_or_ref_ref_node("outputVariableMap", ref); }
    bool is_outputVariableMap_ref() const { return is_or_ref_ref("outputVariableMap"); }
    bool is_set_outputVariableMap() const { return values_.count("outputVariableMap") > 0; }
    void unset_outputVariableMap() { values_.erase("outputVariableMap"); or_ref_is_ref_.erase("outputVariableMap"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_parameterRanges() const { return parameterRanges_.items(); }
    void add_parameterRanges(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); parameterRanges_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_parameterRanges(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); parameterRanges_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_parameterRanges(size_t index) { parameterRanges_.remove(index); }

    std::vector<std::string> get_subTasks() const { return subTasks_.ids(); }
    SedBase* get_subTasks_item(const std::string& item_id) const { return subTasks_.get(item_id); }
    void add_subTasks(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); subTasks_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_subTasks(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); subTasks_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_subTasks(const std::string& item_id) { subTasks_.remove(item_id); }
    void set_id_on_subTasks(const std::string& old_id, const std::string& new_id) { subTasks_.set_id(old_id, new_id); }

    std::vector<std::string> get_aggregateOutputVariables() const { return aggregateOutputVariables_.ids(); }
    SedBase* get_aggregateOutputVariables_item(const std::string& item_id) const { return aggregateOutputVariables_.get(item_id); }
    void add_aggregateOutputVariables(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); aggregateOutputVariables_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_aggregateOutputVariables(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); aggregateOutputVariables_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_aggregateOutputVariables(const std::string& item_id) { aggregateOutputVariables_.remove(item_id); }
    void set_id_on_aggregateOutputVariables(const std::string& old_id, const std::string& new_id) { aggregateOutputVariables_.set_id(old_id, new_id); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_range() const { if (!range_) throw ApiError(std::string("range") + " is not set"); return range_.get(); }
    void set_range(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); range_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_range() const { return range_ != nullptr; }
    void unset_range() { range_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : subTasks_.ids()) kids.push_back(subTasks_.get(i));
        for (const auto& i : aggregateOutputVariables_.ids()) kids.push_back(aggregateOutputVariables_.get(i));
        for (auto* item : parameterRanges_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (range_) kids.push_back(range_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : subTasks_.ids()) out.push_back(ChildLoc{subTasks_.get(i), "/subTasks/" + i});
        for (const auto& i : aggregateOutputVariables_.ids()) out.push_back(ChildLoc{aggregateOutputVariables_.get(i), "/aggregateOutputVariables/" + i});
        { size_t idx = 0; for (auto* item : parameterRanges_.items()) { out.push_back(ChildLoc{item, "/parameterRanges/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (range_) out.push_back(ChildLoc{range_.get(), "/range"});
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "subTasks") return subTasks_;
        if (field_name == "aggregateOutputVariables") return aggregateOutputVariables_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "parameterRanges") return parameterRanges_;
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "range") { range_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("parameterScan");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("outputVariableMap")) d["outputVariableMap"] = values_.at("outputVariableMap");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (subTasks_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : subTasks_.ids()) sub[i] = subTasks_.get(i)->to_json_value(); d["subTasks"] = sub; }
        if (aggregateOutputVariables_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : aggregateOutputVariables_.ids()) sub[i] = aggregateOutputVariables_.get(i)->to_json_value(); d["aggregateOutputVariables"] = sub; }
        if (parameterRanges_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : parameterRanges_.items()) arr.push_back(item->to_json_value()); d["parameterRanges"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (range_) d["range"] = range_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection parameterRanges_;
    IdKeyedCollection subTasks_;
    IdKeyedCollection aggregateOutputVariables_;
    ListCollection taskParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> range_;
};

/// Generated from test-specsheets/tasks/Range/.
class Range : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"values", "ArrayOrRef", false, std::string("Range-0001"), std::nullopt, "Range-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    std::optional<std::string> type_const() const override { return std::string("range"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Range-0003"); }
    std::string own_catchall() const override { return "Range-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Range"; }
    std::string get_type() const { return "range"; }

    jsoncons::json get_values_value() const { return get_or_ref_value_node("values"); }
    std::string get_values_ref() const { return get_or_ref_ref_node("values").as<std::string>(); }
    void set_values_value(const jsoncons::json& value) { set_or_ref_value_node("values", value); }
    void set_values_ref(const std::string& ref) { set_or_ref_ref_node("values", ref); }
    bool is_values_ref() const { return is_or_ref_ref("values"); }
    bool is_set_values() const { return values_.count("values") > 0; }
    void unset_values() { values_.erase("values"); or_ref_is_ref_.erase("values"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("range");
        if (values_.count("values")) d["values"] = values_.at("values");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/RelabelData/.
class RelabelData : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"input", "SIdRef", true, std::string("RelabelData-0002"), std::string("RelabelData-0001"), "RelabelData-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"labels", "ArrayOrRef", true, std::string("RelabelData-0004"), std::string("RelabelData-0003"), "RelabelData-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"input", "labels"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("relabelData"); }
    std::optional<std::string> type_rule_id() const override { return std::string("RelabelData-0006"); }
    std::string own_catchall() const override { return "RelabelData-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "RelabelData"; }
    std::string get_type() const { return "relabelData"; }

    std::string get_input() const { auto it = values_.find("input"); if (it == values_.end()) throw ApiError(std::string("input") + " is not set"); return it->second.as<std::string>(); }
    void set_input(const std::string& value) { values_["input"] = jsoncons::json(value); }
    bool is_set_input() const { return values_.count("input") > 0; }
    void unset_input() { values_.erase("input"); }

    jsoncons::json get_labels_value() const { return get_or_ref_value_node("labels"); }
    std::string get_labels_ref() const { return get_or_ref_ref_node("labels").as<std::string>(); }
    void set_labels_value(const jsoncons::json& value) { set_or_ref_value_node("labels", value); }
    void set_labels_ref(const std::string& ref) { set_or_ref_ref_node("labels", ref); }
    bool is_labels_ref() const { return is_or_ref_ref("labels"); }
    bool is_set_labels() const { return values_.count("labels") > 0; }
    void unset_labels() { values_.erase("labels"); or_ref_is_ref_.erase("labels"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("relabelData");
        if (values_.count("input")) d["input"] = values_.at("input");
        if (values_.count("labels")) d["labels"] = values_.at("labels");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/Scatter/.
class Scatter : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"outputVariableMap", "DictOrRef", false, std::string("Repeat-0002"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"subTasks", "dict", false, std::string("Repeat-0001"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractTask")},
            FieldSpec{"aggregateOutputVariables", "dict", false, std::string("Repeat-0004"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::string("AggregationCalculation"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"range", "ref-discriminator", false, std::string("Repeat-0005"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("RangeInline")}
        };
        return specs;
    }
    std::optional<std::string> type_const() const override { return std::string("scatter"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Scatter-0003"); }
    std::string own_catchall() const override { return "Scatter-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Scatter"; }
    std::string get_type() const { return "scatter"; }

    jsoncons::json get_outputVariableMap_value() const { return get_or_ref_value_node("outputVariableMap"); }
    std::string get_outputVariableMap_ref() const { return get_or_ref_ref_node("outputVariableMap").as<std::string>(); }
    void set_outputVariableMap_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariableMap", value); }
    void set_outputVariableMap_ref(const std::string& ref) { set_or_ref_ref_node("outputVariableMap", ref); }
    bool is_outputVariableMap_ref() const { return is_or_ref_ref("outputVariableMap"); }
    bool is_set_outputVariableMap() const { return values_.count("outputVariableMap") > 0; }
    void unset_outputVariableMap() { values_.erase("outputVariableMap"); or_ref_is_ref_.erase("outputVariableMap"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<std::string> get_subTasks() const { return subTasks_.ids(); }
    SedBase* get_subTasks_item(const std::string& item_id) const { return subTasks_.get(item_id); }
    void add_subTasks(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); subTasks_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_subTasks(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); subTasks_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_subTasks(const std::string& item_id) { subTasks_.remove(item_id); }
    void set_id_on_subTasks(const std::string& old_id, const std::string& new_id) { subTasks_.set_id(old_id, new_id); }

    std::vector<std::string> get_aggregateOutputVariables() const { return aggregateOutputVariables_.ids(); }
    SedBase* get_aggregateOutputVariables_item(const std::string& item_id) const { return aggregateOutputVariables_.get(item_id); }
    void add_aggregateOutputVariables(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); aggregateOutputVariables_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_aggregateOutputVariables(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); aggregateOutputVariables_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_aggregateOutputVariables(const std::string& item_id) { aggregateOutputVariables_.remove(item_id); }
    void set_id_on_aggregateOutputVariables(const std::string& old_id, const std::string& new_id) { aggregateOutputVariables_.set_id(old_id, new_id); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_range() const { if (!range_) throw ApiError(std::string("range") + " is not set"); return range_.get(); }
    void set_range(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); range_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_range() const { return range_ != nullptr; }
    void unset_range() { range_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : subTasks_.ids()) kids.push_back(subTasks_.get(i));
        for (const auto& i : aggregateOutputVariables_.ids()) kids.push_back(aggregateOutputVariables_.get(i));
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (range_) kids.push_back(range_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : subTasks_.ids()) out.push_back(ChildLoc{subTasks_.get(i), "/subTasks/" + i});
        for (const auto& i : aggregateOutputVariables_.ids()) out.push_back(ChildLoc{aggregateOutputVariables_.get(i), "/aggregateOutputVariables/" + i});
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (range_) out.push_back(ChildLoc{range_.get(), "/range"});
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "subTasks") return subTasks_;
        if (field_name == "aggregateOutputVariables") return aggregateOutputVariables_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "range") { range_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("scatter");
        if (values_.count("outputVariableMap")) d["outputVariableMap"] = values_.at("outputVariableMap");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (subTasks_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : subTasks_.ids()) sub[i] = subTasks_.get(i)->to_json_value(); d["subTasks"] = sub; }
        if (aggregateOutputVariables_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : aggregateOutputVariables_.ids()) sub[i] = aggregateOutputVariables_.get(i)->to_json_value(); d["aggregateOutputVariables"] = sub; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (range_) d["range"] = range_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection subTasks_;
    IdKeyedCollection aggregateOutputVariables_;
    ListCollection taskParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> range_;
};

/// Generated from test-specsheets/tasks/Span/.
class Span : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"start", "NumberOrRef", true, std::string("Span-0002"), std::string("Span-0001"), "Span-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"end", "NumberOrRef", true, std::string("Span-0005"), std::string("Span-0004"), "Span-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"start", "end"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("span"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Span-0007"); }
    std::string own_catchall() const override { return "Span-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Span"; }
    std::string get_type() const { return "span"; }

    double get_start_value() const { return get_or_ref_value_node("start").as<double>(); }
    std::string get_start_ref() const { return get_or_ref_ref_node("start").as<std::string>(); }
    void set_start_value(double value) { set_or_ref_value_node("start", jsoncons::json(value)); }
    void set_start_ref(const std::string& ref) { set_or_ref_ref_node("start", ref); }
    bool is_start_ref() const { return is_or_ref_ref("start"); }
    bool is_set_start() const { return values_.count("start") > 0; }
    void unset_start() { values_.erase("start"); or_ref_is_ref_.erase("start"); }

    double get_end_value() const { return get_or_ref_value_node("end").as<double>(); }
    std::string get_end_ref() const { return get_or_ref_ref_node("end").as<std::string>(); }
    void set_end_value(double value) { set_or_ref_value_node("end", jsoncons::json(value)); }
    void set_end_ref(const std::string& ref) { set_or_ref_ref_node("end", ref); }
    bool is_end_ref() const { return is_or_ref_ref("end"); }
    bool is_set_end() const { return values_.count("end") > 0; }
    void unset_end() { values_.erase("end"); or_ref_is_ref_.erase("end"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("span");
        if (values_.count("start")) d["start"] = values_.at("start");
        if (values_.count("end")) d["end"] = values_.at("end");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/SteadyState/.
class SteadyState : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::nullopt, std::string("SteadyState-0001"), "SteadyState-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string("SteadyState-0004"), std::nullopt, "SteadyState-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariables", "ArrayOrRef", true, std::nullopt, std::string("SteadyState-0002"), "SteadyState-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputModel", "BooleanOrRef", false, std::string("SteadyState-0005"), std::nullopt, "SteadyState-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"model", "outputVariables"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("steadyState"); }
    std::optional<std::string> type_rule_id() const override { return std::string("SteadyState-0003"); }
    std::string own_catchall() const override { return "SteadyState-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "SteadyState"; }
    std::string get_type() const { return "steadyState"; }

    std::string get_model() const { auto it = values_.find("model"); if (it == values_.end()) throw ApiError(std::string("model") + " is not set"); return it->second.as<std::string>(); }
    void set_model(const std::string& value) { values_["model"] = jsoncons::json(value); }
    bool is_set_model() const { return values_.count("model") > 0; }
    void unset_model() { values_.erase("model"); }

    std::string get_independentVariable_value() const { return get_or_ref_value_node("independentVariable").as<std::string>(); }
    std::string get_independentVariable_ref() const { return get_or_ref_ref_node("independentVariable").as<std::string>(); }
    void set_independentVariable_value(const std::string& value) { set_or_ref_value_node("independentVariable", jsoncons::json(value)); }
    void set_independentVariable_ref(const std::string& ref) { set_or_ref_ref_node("independentVariable", ref); }
    bool is_independentVariable_ref() const { return is_or_ref_ref("independentVariable"); }
    bool is_set_independentVariable() const { return values_.count("independentVariable") > 0; }
    void unset_independentVariable() { values_.erase("independentVariable"); or_ref_is_ref_.erase("independentVariable"); }

    jsoncons::json get_outputVariables_value() const { return get_or_ref_value_node("outputVariables"); }
    std::string get_outputVariables_ref() const { return get_or_ref_ref_node("outputVariables").as<std::string>(); }
    void set_outputVariables_value(const jsoncons::json& value) { set_or_ref_value_node("outputVariables", value); }
    void set_outputVariables_ref(const std::string& ref) { set_or_ref_ref_node("outputVariables", ref); }
    bool is_outputVariables_ref() const { return is_or_ref_ref("outputVariables"); }
    bool is_set_outputVariables() const { return values_.count("outputVariables") > 0; }
    void unset_outputVariables() { values_.erase("outputVariables"); or_ref_is_ref_.erase("outputVariables"); }

    bool get_outputModel_value() const { return get_or_ref_value_node("outputModel").as<bool>(); }
    std::string get_outputModel_ref() const { return get_or_ref_ref_node("outputModel").as<std::string>(); }
    void set_outputModel_value(bool value) { set_or_ref_value_node("outputModel", jsoncons::json(value)); }
    void set_outputModel_ref(const std::string& ref) { set_or_ref_ref_node("outputModel", ref); }
    bool is_outputModel_ref() const { return is_or_ref_ref("outputModel"); }
    bool is_set_outputModel() const { return values_.count("outputModel") > 0; }
    void unset_outputModel() { values_.erase("outputModel"); or_ref_is_ref_.erase("outputModel"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("steadyState");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("outputVariables")) d["outputVariables"] = values_.at("outputVariables");
        if (values_.count("outputModel")) d["outputModel"] = values_.at("outputModel");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/tasks/StringFormation/.
class StringFormation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"concatenate", "ArrayOrRef", true, std::string("StringFormation-0002"), std::string("StringFormation-0001"), "StringFormation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"concatenate"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("stringFormation"); }
    std::optional<std::string> type_rule_id() const override { return std::string("StringFormation-0004"); }
    std::string own_catchall() const override { return "StringFormation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "StringFormation"; }
    std::string get_type() const { return "stringFormation"; }

    jsoncons::json get_concatenate_value() const { return get_or_ref_value_node("concatenate"); }
    std::string get_concatenate_ref() const { return get_or_ref_ref_node("concatenate").as<std::string>(); }
    void set_concatenate_value(const jsoncons::json& value) { set_or_ref_value_node("concatenate", value); }
    void set_concatenate_ref(const std::string& ref) { set_or_ref_ref_node("concatenate", ref); }
    bool is_concatenate_ref() const { return is_or_ref_ref("concatenate"); }
    bool is_set_concatenate() const { return values_.count("concatenate") > 0; }
    void unset_concatenate() { values_.erase("concatenate"); or_ref_is_ref_.erase("concatenate"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("stringFormation");
        if (values_.count("concatenate")) d["concatenate"] = values_.at("concatenate");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/outputs/Plot2D/.
class Plot2D : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"legend", "BooleanOrRef", false, std::string("Plot-0001"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"height", "NumberOrRef", false, std::string("Plot-0003"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"width", "NumberOrRef", false, std::string("Plot-0005"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"curves", "dict", true, std::string("Plot2D-0002"), std::string("Plot2D-0001"), "Plot2D-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractCurve")},
            FieldSpec{"outputParameters", "array", false, std::string("AbstractOutput-0001"), std::nullopt, "AbstractOutput-0000", std::nullopt, std::nullopt, std::nullopt, std::string("OutputParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"rightYAxis", "ref-class", false, std::string("Plot2D-0003"), std::nullopt, "Plot2D-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Axis"), std::nullopt},
            FieldSpec{"xAxis", "ref-class", false, std::string("Plot-0007"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Axis"), std::nullopt},
            FieldSpec{"yAxis", "ref-class", false, std::string("Plot-0008"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Axis"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"curves"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("plot2D"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Plot2D-0004"); }
    std::string own_catchall() const override { return "Plot2D-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Plot2D"; }
    std::string get_type() const { return "plot2D"; }

    bool get_legend_value() const { return get_or_ref_value_node("legend").as<bool>(); }
    std::string get_legend_ref() const { return get_or_ref_ref_node("legend").as<std::string>(); }
    void set_legend_value(bool value) { set_or_ref_value_node("legend", jsoncons::json(value)); }
    void set_legend_ref(const std::string& ref) { set_or_ref_ref_node("legend", ref); }
    bool is_legend_ref() const { return is_or_ref_ref("legend"); }
    bool is_set_legend() const { return values_.count("legend") > 0; }
    void unset_legend() { values_.erase("legend"); or_ref_is_ref_.erase("legend"); }

    double get_height_value() const { return get_or_ref_value_node("height").as<double>(); }
    std::string get_height_ref() const { return get_or_ref_ref_node("height").as<std::string>(); }
    void set_height_value(double value) { set_or_ref_value_node("height", jsoncons::json(value)); }
    void set_height_ref(const std::string& ref) { set_or_ref_ref_node("height", ref); }
    bool is_height_ref() const { return is_or_ref_ref("height"); }
    bool is_set_height() const { return values_.count("height") > 0; }
    void unset_height() { values_.erase("height"); or_ref_is_ref_.erase("height"); }

    double get_width_value() const { return get_or_ref_value_node("width").as<double>(); }
    std::string get_width_ref() const { return get_or_ref_ref_node("width").as<std::string>(); }
    void set_width_value(double value) { set_or_ref_value_node("width", jsoncons::json(value)); }
    void set_width_ref(const std::string& ref) { set_or_ref_ref_node("width", ref); }
    bool is_width_ref() const { return is_or_ref_ref("width"); }
    bool is_set_width() const { return values_.count("width") > 0; }
    void unset_width() { values_.erase("width"); or_ref_is_ref_.erase("width"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<std::string> get_curves() const { return curves_.ids(); }
    SedBase* get_curves_item(const std::string& item_id) const { return curves_.get(item_id); }
    void add_curves(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); curves_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_curves(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); curves_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_curves(const std::string& item_id) { curves_.remove(item_id); }
    void set_id_on_curves(const std::string& old_id, const std::string& new_id) { curves_.set_id(old_id, new_id); }

    std::vector<SedBase*> get_outputParameters() const { return outputParameters_.items(); }
    void add_outputParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_outputParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_outputParameters(size_t index) { outputParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_rightYAxis() const { if (!rightYAxis_) throw ApiError(std::string("rightYAxis") + " is not set"); return rightYAxis_.get(); }
    void set_rightYAxis(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); rightYAxis_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_rightYAxis() const { return rightYAxis_ != nullptr; }
    void unset_rightYAxis() { rightYAxis_.reset(); }

    SedBase* get_xAxis() const { if (!xAxis_) throw ApiError(std::string("xAxis") + " is not set"); return xAxis_.get(); }
    void set_xAxis(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); xAxis_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_xAxis() const { return xAxis_ != nullptr; }
    void unset_xAxis() { xAxis_.reset(); }

    SedBase* get_yAxis() const { if (!yAxis_) throw ApiError(std::string("yAxis") + " is not set"); return yAxis_.get(); }
    void set_yAxis(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); yAxis_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_yAxis() const { return yAxis_ != nullptr; }
    void unset_yAxis() { yAxis_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : curves_.ids()) kids.push_back(curves_.get(i));
        for (auto* item : outputParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (rightYAxis_) kids.push_back(rightYAxis_.get());
        if (xAxis_) kids.push_back(xAxis_.get());
        if (yAxis_) kids.push_back(yAxis_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : curves_.ids()) out.push_back(ChildLoc{curves_.get(i), "/curves/" + i});
        { size_t idx = 0; for (auto* item : outputParameters_.items()) { out.push_back(ChildLoc{item, "/outputParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (rightYAxis_) out.push_back(ChildLoc{rightYAxis_.get(), "/rightYAxis"});
        if (xAxis_) out.push_back(ChildLoc{xAxis_.get(), "/xAxis"});
        if (yAxis_) out.push_back(ChildLoc{yAxis_.get(), "/yAxis"});
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "curves") return curves_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "outputParameters") return outputParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "rightYAxis") { rightYAxis_ = std::move(child); return; }
        if (field_name == "xAxis") { xAxis_ = std::move(child); return; }
        if (field_name == "yAxis") { yAxis_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("plot2D");
        if (values_.count("legend")) d["legend"] = values_.at("legend");
        if (values_.count("height")) d["height"] = values_.at("height");
        if (values_.count("width")) d["width"] = values_.at("width");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (curves_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : curves_.ids()) sub[i] = curves_.get(i)->to_json_value(); d["curves"] = sub; }
        if (outputParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : outputParameters_.items()) arr.push_back(item->to_json_value()); d["outputParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (rightYAxis_) d["rightYAxis"] = rightYAxis_->to_json_value();
        if (xAxis_) d["xAxis"] = xAxis_->to_json_value();
        if (yAxis_) d["yAxis"] = yAxis_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection curves_;
    ListCollection outputParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> rightYAxis_;
    std::unique_ptr<SedBase> xAxis_;
    std::unique_ptr<SedBase> yAxis_;
};

/// Generated from test-specsheets/outputs/Plot3D/.
class Plot3D : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"legend", "BooleanOrRef", false, std::string("Plot-0001"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"height", "NumberOrRef", false, std::string("Plot-0003"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"width", "NumberOrRef", false, std::string("Plot-0005"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"surfaces", "dict", true, std::string("Plot3D-0002"), std::string("Plot3D-0001"), "Plot3D-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Surface"), std::nullopt},
            FieldSpec{"outputParameters", "array", false, std::string("AbstractOutput-0001"), std::nullopt, "AbstractOutput-0000", std::nullopt, std::nullopt, std::nullopt, std::string("OutputParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt},
            FieldSpec{"zAxis", "ref-class", false, std::string("Plot3D-0003"), std::nullopt, "Plot3D-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Axis"), std::nullopt},
            FieldSpec{"xAxis", "ref-class", false, std::string("Plot-0007"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Axis"), std::nullopt},
            FieldSpec{"yAxis", "ref-class", false, std::string("Plot-0008"), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Axis"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"surfaces"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("plot3D"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Plot3D-0004"); }
    std::string own_catchall() const override { return "Plot3D-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Plot3D"; }
    std::string get_type() const { return "plot3D"; }

    bool get_legend_value() const { return get_or_ref_value_node("legend").as<bool>(); }
    std::string get_legend_ref() const { return get_or_ref_ref_node("legend").as<std::string>(); }
    void set_legend_value(bool value) { set_or_ref_value_node("legend", jsoncons::json(value)); }
    void set_legend_ref(const std::string& ref) { set_or_ref_ref_node("legend", ref); }
    bool is_legend_ref() const { return is_or_ref_ref("legend"); }
    bool is_set_legend() const { return values_.count("legend") > 0; }
    void unset_legend() { values_.erase("legend"); or_ref_is_ref_.erase("legend"); }

    double get_height_value() const { return get_or_ref_value_node("height").as<double>(); }
    std::string get_height_ref() const { return get_or_ref_ref_node("height").as<std::string>(); }
    void set_height_value(double value) { set_or_ref_value_node("height", jsoncons::json(value)); }
    void set_height_ref(const std::string& ref) { set_or_ref_ref_node("height", ref); }
    bool is_height_ref() const { return is_or_ref_ref("height"); }
    bool is_set_height() const { return values_.count("height") > 0; }
    void unset_height() { values_.erase("height"); or_ref_is_ref_.erase("height"); }

    double get_width_value() const { return get_or_ref_value_node("width").as<double>(); }
    std::string get_width_ref() const { return get_or_ref_ref_node("width").as<std::string>(); }
    void set_width_value(double value) { set_or_ref_value_node("width", jsoncons::json(value)); }
    void set_width_ref(const std::string& ref) { set_or_ref_ref_node("width", ref); }
    bool is_width_ref() const { return is_or_ref_ref("width"); }
    bool is_set_width() const { return values_.count("width") > 0; }
    void unset_width() { values_.erase("width"); or_ref_is_ref_.erase("width"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<std::string> get_surfaces() const { return surfaces_.ids(); }
    SedBase* get_surfaces_item(const std::string& item_id) const { return surfaces_.get(item_id); }
    void add_surfaces(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); surfaces_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_surfaces(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); surfaces_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_surfaces(const std::string& item_id) { surfaces_.remove(item_id); }
    void set_id_on_surfaces(const std::string& old_id, const std::string& new_id) { surfaces_.set_id(old_id, new_id); }

    std::vector<SedBase*> get_outputParameters() const { return outputParameters_.items(); }
    void add_outputParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_outputParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_outputParameters(size_t index) { outputParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    SedBase* get_zAxis() const { if (!zAxis_) throw ApiError(std::string("zAxis") + " is not set"); return zAxis_.get(); }
    void set_zAxis(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); zAxis_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_zAxis() const { return zAxis_ != nullptr; }
    void unset_zAxis() { zAxis_.reset(); }

    SedBase* get_xAxis() const { if (!xAxis_) throw ApiError(std::string("xAxis") + " is not set"); return xAxis_.get(); }
    void set_xAxis(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); xAxis_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_xAxis() const { return xAxis_ != nullptr; }
    void unset_xAxis() { xAxis_.reset(); }

    SedBase* get_yAxis() const { if (!yAxis_) throw ApiError(std::string("yAxis") + " is not set"); return yAxis_.get(); }
    void set_yAxis(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); yAxis_ = std::move(obj); raw->attach(this, get_document()); }
    bool is_set_yAxis() const { return yAxis_ != nullptr; }
    void unset_yAxis() { yAxis_.reset(); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : surfaces_.ids()) kids.push_back(surfaces_.get(i));
        for (auto* item : outputParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        if (zAxis_) kids.push_back(zAxis_.get());
        if (xAxis_) kids.push_back(xAxis_.get());
        if (yAxis_) kids.push_back(yAxis_.get());
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : surfaces_.ids()) out.push_back(ChildLoc{surfaces_.get(i), "/surfaces/" + i});
        { size_t idx = 0; for (auto* item : outputParameters_.items()) { out.push_back(ChildLoc{item, "/outputParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        if (zAxis_) out.push_back(ChildLoc{zAxis_.get(), "/zAxis"});
        if (xAxis_) out.push_back(ChildLoc{xAxis_.get(), "/xAxis"});
        if (yAxis_) out.push_back(ChildLoc{yAxis_.get(), "/yAxis"});
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "surfaces") return surfaces_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "outputParameters") return outputParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    void set_child_field(const std::string& field_name, std::unique_ptr<SedBase> child) override {
        if (field_name == "zAxis") { zAxis_ = std::move(child); return; }
        if (field_name == "xAxis") { xAxis_ = std::move(child); return; }
        if (field_name == "yAxis") { yAxis_ = std::move(child); return; }
        SedBase::set_child_field(field_name, std::move(child));
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("plot3D");
        if (values_.count("legend")) d["legend"] = values_.at("legend");
        if (values_.count("height")) d["height"] = values_.at("height");
        if (values_.count("width")) d["width"] = values_.at("width");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (surfaces_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : surfaces_.ids()) sub[i] = surfaces_.get(i)->to_json_value(); d["surfaces"] = sub; }
        if (outputParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : outputParameters_.items()) arr.push_back(item->to_json_value()); d["outputParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        if (zAxis_) d["zAxis"] = zAxis_->to_json_value();
        if (xAxis_) d["xAxis"] = xAxis_->to_json_value();
        if (yAxis_) d["yAxis"] = yAxis_->to_json_value();
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection surfaces_;
    ListCollection outputParameters_;
    ListCollection annotations_;
    std::unique_ptr<SedBase> zAxis_;
    std::unique_ptr<SedBase> xAxis_;
    std::unique_ptr<SedBase> yAxis_;
};

/// Generated from test-specsheets/outputs/Report/.
class Report : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"data", "SIdRef", true, std::string("Report-0002"), std::string("Report-0001"), "Report-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputParameters", "array", false, std::string("AbstractOutput-0001"), std::nullopt, "AbstractOutput-0000", std::nullopt, std::nullopt, std::nullopt, std::string("OutputParameter"), std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"data"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("report"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Report-0003"); }
    std::string own_catchall() const override { return "Report-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Report"; }
    std::string get_type() const { return "report"; }

    std::string get_data() const { auto it = values_.find("data"); if (it == values_.end()) throw ApiError(std::string("data") + " is not set"); return it->second.as<std::string>(); }
    void set_data(const std::string& value) { values_["data"] = jsoncons::json(value); }
    bool is_set_data() const { return values_.count("data") > 0; }
    void unset_data() { values_.erase("data"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_outputParameters() const { return outputParameters_.items(); }
    void add_outputParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_outputParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_outputParameters(size_t index) { outputParameters_.remove(index); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : outputParameters_.items()) kids.push_back(item);
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : outputParameters_.items()) { out.push_back(ChildLoc{item, "/outputParameters/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "outputParameters") return outputParameters_;
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("report");
        if (values_.count("data")) d["data"] = values_.at("data");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (outputParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : outputParameters_.items()) arr.push_back(item->to_json_value()); d["outputParameters"] = arr; }
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection outputParameters_;
    ListCollection annotations_;
};

/// Generated from test-specsheets/outputs/Surface/.
class Surface : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"surfaceType", "StringOrRef", true, std::string("Surface-0002"), std::string("Surface-0001"), "Surface-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"x", "SIdRef", true, std::string("Surface-0005"), std::string("Surface-0004"), "Surface-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"y", "SIdRef", true, std::string("Surface-0007"), std::string("Surface-0006"), "Surface-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"z", "SIdRef", true, std::string("Surface-0009"), std::string("Surface-0008"), "Surface-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"style", "SIdRef", false, std::string("Surface-0010"), std::nullopt, "Surface-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"order", "IntegerOrRef", false, std::string("Surface-0011"), std::nullopt, "Surface-0000", 0.0, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"surfaceType", "x", "y", "z"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "Surface-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Surface"; }

    std::string get_surfaceType_value() const { return get_or_ref_value_node("surfaceType").as<std::string>(); }
    std::string get_surfaceType_ref() const { return get_or_ref_ref_node("surfaceType").as<std::string>(); }
    void set_surfaceType_value(const std::string& value) { set_or_ref_value_node("surfaceType", jsoncons::json(value)); }
    void set_surfaceType_ref(const std::string& ref) { set_or_ref_ref_node("surfaceType", ref); }
    bool is_surfaceType_ref() const { return is_or_ref_ref("surfaceType"); }
    bool is_set_surfaceType() const { return values_.count("surfaceType") > 0; }
    void unset_surfaceType() { values_.erase("surfaceType"); or_ref_is_ref_.erase("surfaceType"); }

    std::string get_x() const { auto it = values_.find("x"); if (it == values_.end()) throw ApiError(std::string("x") + " is not set"); return it->second.as<std::string>(); }
    void set_x(const std::string& value) { values_["x"] = jsoncons::json(value); }
    bool is_set_x() const { return values_.count("x") > 0; }
    void unset_x() { values_.erase("x"); }

    std::string get_y() const { auto it = values_.find("y"); if (it == values_.end()) throw ApiError(std::string("y") + " is not set"); return it->second.as<std::string>(); }
    void set_y(const std::string& value) { values_["y"] = jsoncons::json(value); }
    bool is_set_y() const { return values_.count("y") > 0; }
    void unset_y() { values_.erase("y"); }

    std::string get_z() const { auto it = values_.find("z"); if (it == values_.end()) throw ApiError(std::string("z") + " is not set"); return it->second.as<std::string>(); }
    void set_z(const std::string& value) { values_["z"] = jsoncons::json(value); }
    bool is_set_z() const { return values_.count("z") > 0; }
    void unset_z() { values_.erase("z"); }

    std::string get_style() const { auto it = values_.find("style"); if (it == values_.end()) throw ApiError(std::string("style") + " is not set"); return it->second.as<std::string>(); }
    void set_style(const std::string& value) { values_["style"] = jsoncons::json(value); }
    bool is_set_style() const { return values_.count("style") > 0; }
    void unset_style() { values_.erase("style"); }

    int64_t get_order_value() const { return get_or_ref_value_node("order").as<int64_t>(); }
    std::string get_order_ref() const { return get_or_ref_ref_node("order").as<std::string>(); }
    void set_order_value(int64_t value) { set_or_ref_value_node("order", jsoncons::json(value)); }
    void set_order_ref(const std::string& ref) { set_or_ref_ref_node("order", ref); }
    bool is_order_ref() const { return is_or_ref_ref("order"); }
    bool is_set_order() const { return values_.count("order") > 0; }
    void unset_order() { values_.erase("order"); or_ref_is_ref_.erase("order"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("surfaceType")) d["surfaceType"] = values_.at("surfaceType");
        if (values_.count("x")) d["x"] = values_.at("x");
        if (values_.count("y")) d["y"] = values_.at("y");
        if (values_.count("z")) d["z"] = values_.at("z");
        if (values_.count("style")) d["style"] = values_.at("style");
        if (values_.count("order")) d["order"] = values_.at("order");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection annotations_;
};

/// Generated from test-specsheets/auxiliary/Annotation/.
class Annotation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"qualifier", "any", true, std::string("Annotation-0002"), std::string("Annotation-0001"), "Annotation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"value", "any", true, std::nullopt, std::string("Annotation-0003"), "Annotation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"qualifier", "value"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "Annotation-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Annotation"; }

    jsoncons::json get_qualifier() const { auto it = values_.find("qualifier"); if (it == values_.end()) throw ApiError(std::string("qualifier") + " is not set"); return it->second; }
    void set_qualifier(const jsoncons::json& value) { values_["qualifier"] = value; }
    bool is_set_qualifier() const { return values_.count("qualifier") > 0; }
    void unset_qualifier() { values_.erase("qualifier"); }

    jsoncons::json get_value() const { auto it = values_.find("value"); if (it == values_.end()) throw ApiError(std::string("value") + " is not set"); return it->second; }
    void set_value(const jsoncons::json& value) { values_["value"] = value; }
    bool is_set_value() const { return values_.count("value") > 0; }
    void unset_value() { values_.erase("value"); }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("qualifier")) d["qualifier"] = values_.at("qualifier");
        if (values_.count("value")) d["value"] = values_.at("value");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/Axis/.
class Axis : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"scale", "StringOrRef", false, std::string("Axis-0001"), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"min", "NumberOrRef", false, std::string("Axis-0003"), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"max", "NumberOrRef", false, std::string("Axis-0005"), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"grid", "BooleanOrRef", false, std::string("Axis-0007"), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"style", "SIdRef", false, std::string("Axis-0009"), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"reverse", "BooleanOrRef", false, std::string("Axis-0010"), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "Axis-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Axis"; }

    std::string get_scale_value() const { return get_or_ref_value_node("scale").as<std::string>(); }
    std::string get_scale_ref() const { return get_or_ref_ref_node("scale").as<std::string>(); }
    void set_scale_value(const std::string& value) { set_or_ref_value_node("scale", jsoncons::json(value)); }
    void set_scale_ref(const std::string& ref) { set_or_ref_ref_node("scale", ref); }
    bool is_scale_ref() const { return is_or_ref_ref("scale"); }
    bool is_set_scale() const { return values_.count("scale") > 0; }
    void unset_scale() { values_.erase("scale"); or_ref_is_ref_.erase("scale"); }

    double get_min_value() const { return get_or_ref_value_node("min").as<double>(); }
    std::string get_min_ref() const { return get_or_ref_ref_node("min").as<std::string>(); }
    void set_min_value(double value) { set_or_ref_value_node("min", jsoncons::json(value)); }
    void set_min_ref(const std::string& ref) { set_or_ref_ref_node("min", ref); }
    bool is_min_ref() const { return is_or_ref_ref("min"); }
    bool is_set_min() const { return values_.count("min") > 0; }
    void unset_min() { values_.erase("min"); or_ref_is_ref_.erase("min"); }

    double get_max_value() const { return get_or_ref_value_node("max").as<double>(); }
    std::string get_max_ref() const { return get_or_ref_ref_node("max").as<std::string>(); }
    void set_max_value(double value) { set_or_ref_value_node("max", jsoncons::json(value)); }
    void set_max_ref(const std::string& ref) { set_or_ref_ref_node("max", ref); }
    bool is_max_ref() const { return is_or_ref_ref("max"); }
    bool is_set_max() const { return values_.count("max") > 0; }
    void unset_max() { values_.erase("max"); or_ref_is_ref_.erase("max"); }

    bool get_grid_value() const { return get_or_ref_value_node("grid").as<bool>(); }
    std::string get_grid_ref() const { return get_or_ref_ref_node("grid").as<std::string>(); }
    void set_grid_value(bool value) { set_or_ref_value_node("grid", jsoncons::json(value)); }
    void set_grid_ref(const std::string& ref) { set_or_ref_ref_node("grid", ref); }
    bool is_grid_ref() const { return is_or_ref_ref("grid"); }
    bool is_set_grid() const { return values_.count("grid") > 0; }
    void unset_grid() { values_.erase("grid"); or_ref_is_ref_.erase("grid"); }

    std::string get_style() const { auto it = values_.find("style"); if (it == values_.end()) throw ApiError(std::string("style") + " is not set"); return it->second.as<std::string>(); }
    void set_style(const std::string& value) { values_["style"] = jsoncons::json(value); }
    bool is_set_style() const { return values_.count("style") > 0; }
    void unset_style() { values_.erase("style"); }

    bool get_reverse_value() const { return get_or_ref_value_node("reverse").as<bool>(); }
    std::string get_reverse_ref() const { return get_or_ref_ref_node("reverse").as<std::string>(); }
    void set_reverse_value(bool value) { set_or_ref_value_node("reverse", jsoncons::json(value)); }
    void set_reverse_ref(const std::string& ref) { set_or_ref_ref_node("reverse", ref); }
    bool is_reverse_ref() const { return is_or_ref_ref("reverse"); }
    bool is_set_reverse() const { return values_.count("reverse") > 0; }
    void unset_reverse() { values_.erase("reverse"); or_ref_is_ref_.erase("reverse"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("scale")) d["scale"] = values_.at("scale");
        if (values_.count("min")) d["min"] = values_.at("min");
        if (values_.count("max")) d["max"] = values_.at("max");
        if (values_.count("grid")) d["grid"] = values_.at("grid");
        if (values_.count("style")) d["style"] = values_.at("style");
        if (values_.count("reverse")) d["reverse"] = values_.at("reverse");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection annotations_;
};

/// Generated from test-specsheets/auxiliary/Curve/.
class Curve : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"curveType", "StringOrRef", true, std::string("Curve-0002"), std::string("Curve-0001"), "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"y", "SIdRef", true, std::string("Curve-0005"), std::string("Curve-0004"), "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"xErrorUpper", "SIdRef", false, std::string("Curve-0006"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"xErrorLower", "SIdRef", false, std::string("Curve-0007"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yErrorUpper", "SIdRef", false, std::string("Curve-0008"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yErrorLower", "SIdRef", false, std::string("Curve-0009"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yFrom", "SIdRef", false, std::string("Curve-0010"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yTo", "SIdRef", false, std::string("Curve-0011"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"x", "SIdRef", true, std::string("AbstractCurve-0002"), std::string("AbstractCurve-0001"), "AbstractCurve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"order", "IntegerOrRef", false, std::string("AbstractCurve-0003"), std::nullopt, "AbstractCurve-0000", 0.0, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"style", "SIdRef", false, std::string("AbstractCurve-0005"), std::nullopt, "AbstractCurve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yAxis", "StringOrRef", false, std::string("AbstractCurve-0006"), std::nullopt, "AbstractCurve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"curveType", "y", "x"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("curve"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Curve-0012"); }
    std::string own_catchall() const override { return "Curve-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "Curve"; }
    std::string get_type() const { return "curve"; }

    std::string get_curveType_value() const { return get_or_ref_value_node("curveType").as<std::string>(); }
    std::string get_curveType_ref() const { return get_or_ref_ref_node("curveType").as<std::string>(); }
    void set_curveType_value(const std::string& value) { set_or_ref_value_node("curveType", jsoncons::json(value)); }
    void set_curveType_ref(const std::string& ref) { set_or_ref_ref_node("curveType", ref); }
    bool is_curveType_ref() const { return is_or_ref_ref("curveType"); }
    bool is_set_curveType() const { return values_.count("curveType") > 0; }
    void unset_curveType() { values_.erase("curveType"); or_ref_is_ref_.erase("curveType"); }

    std::string get_y() const { auto it = values_.find("y"); if (it == values_.end()) throw ApiError(std::string("y") + " is not set"); return it->second.as<std::string>(); }
    void set_y(const std::string& value) { values_["y"] = jsoncons::json(value); }
    bool is_set_y() const { return values_.count("y") > 0; }
    void unset_y() { values_.erase("y"); }

    std::string get_xErrorUpper() const { auto it = values_.find("xErrorUpper"); if (it == values_.end()) throw ApiError(std::string("xErrorUpper") + " is not set"); return it->second.as<std::string>(); }
    void set_xErrorUpper(const std::string& value) { values_["xErrorUpper"] = jsoncons::json(value); }
    bool is_set_xErrorUpper() const { return values_.count("xErrorUpper") > 0; }
    void unset_xErrorUpper() { values_.erase("xErrorUpper"); }

    std::string get_xErrorLower() const { auto it = values_.find("xErrorLower"); if (it == values_.end()) throw ApiError(std::string("xErrorLower") + " is not set"); return it->second.as<std::string>(); }
    void set_xErrorLower(const std::string& value) { values_["xErrorLower"] = jsoncons::json(value); }
    bool is_set_xErrorLower() const { return values_.count("xErrorLower") > 0; }
    void unset_xErrorLower() { values_.erase("xErrorLower"); }

    std::string get_yErrorUpper() const { auto it = values_.find("yErrorUpper"); if (it == values_.end()) throw ApiError(std::string("yErrorUpper") + " is not set"); return it->second.as<std::string>(); }
    void set_yErrorUpper(const std::string& value) { values_["yErrorUpper"] = jsoncons::json(value); }
    bool is_set_yErrorUpper() const { return values_.count("yErrorUpper") > 0; }
    void unset_yErrorUpper() { values_.erase("yErrorUpper"); }

    std::string get_yErrorLower() const { auto it = values_.find("yErrorLower"); if (it == values_.end()) throw ApiError(std::string("yErrorLower") + " is not set"); return it->second.as<std::string>(); }
    void set_yErrorLower(const std::string& value) { values_["yErrorLower"] = jsoncons::json(value); }
    bool is_set_yErrorLower() const { return values_.count("yErrorLower") > 0; }
    void unset_yErrorLower() { values_.erase("yErrorLower"); }

    std::string get_yFrom() const { auto it = values_.find("yFrom"); if (it == values_.end()) throw ApiError(std::string("yFrom") + " is not set"); return it->second.as<std::string>(); }
    void set_yFrom(const std::string& value) { values_["yFrom"] = jsoncons::json(value); }
    bool is_set_yFrom() const { return values_.count("yFrom") > 0; }
    void unset_yFrom() { values_.erase("yFrom"); }

    std::string get_yTo() const { auto it = values_.find("yTo"); if (it == values_.end()) throw ApiError(std::string("yTo") + " is not set"); return it->second.as<std::string>(); }
    void set_yTo(const std::string& value) { values_["yTo"] = jsoncons::json(value); }
    bool is_set_yTo() const { return values_.count("yTo") > 0; }
    void unset_yTo() { values_.erase("yTo"); }

    std::string get_x() const { auto it = values_.find("x"); if (it == values_.end()) throw ApiError(std::string("x") + " is not set"); return it->second.as<std::string>(); }
    void set_x(const std::string& value) { values_["x"] = jsoncons::json(value); }
    bool is_set_x() const { return values_.count("x") > 0; }
    void unset_x() { values_.erase("x"); }

    int64_t get_order_value() const { return get_or_ref_value_node("order").as<int64_t>(); }
    std::string get_order_ref() const { return get_or_ref_ref_node("order").as<std::string>(); }
    void set_order_value(int64_t value) { set_or_ref_value_node("order", jsoncons::json(value)); }
    void set_order_ref(const std::string& ref) { set_or_ref_ref_node("order", ref); }
    bool is_order_ref() const { return is_or_ref_ref("order"); }
    bool is_set_order() const { return values_.count("order") > 0; }
    void unset_order() { values_.erase("order"); or_ref_is_ref_.erase("order"); }

    std::string get_style() const { auto it = values_.find("style"); if (it == values_.end()) throw ApiError(std::string("style") + " is not set"); return it->second.as<std::string>(); }
    void set_style(const std::string& value) { values_["style"] = jsoncons::json(value); }
    bool is_set_style() const { return values_.count("style") > 0; }
    void unset_style() { values_.erase("style"); }

    std::string get_yAxis_value() const { return get_or_ref_value_node("yAxis").as<std::string>(); }
    std::string get_yAxis_ref() const { return get_or_ref_ref_node("yAxis").as<std::string>(); }
    void set_yAxis_value(const std::string& value) { set_or_ref_value_node("yAxis", jsoncons::json(value)); }
    void set_yAxis_ref(const std::string& ref) { set_or_ref_ref_node("yAxis", ref); }
    bool is_yAxis_ref() const { return is_or_ref_ref("yAxis"); }
    bool is_set_yAxis() const { return values_.count("yAxis") > 0; }
    void unset_yAxis() { values_.erase("yAxis"); or_ref_is_ref_.erase("yAxis"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("curve");
        if (values_.count("curveType")) d["curveType"] = values_.at("curveType");
        if (values_.count("y")) d["y"] = values_.at("y");
        if (values_.count("xErrorUpper")) d["xErrorUpper"] = values_.at("xErrorUpper");
        if (values_.count("xErrorLower")) d["xErrorLower"] = values_.at("xErrorLower");
        if (values_.count("yErrorUpper")) d["yErrorUpper"] = values_.at("yErrorUpper");
        if (values_.count("yErrorLower")) d["yErrorLower"] = values_.at("yErrorLower");
        if (values_.count("yFrom")) d["yFrom"] = values_.at("yFrom");
        if (values_.count("yTo")) d["yTo"] = values_.at("yTo");
        if (values_.count("x")) d["x"] = values_.at("x");
        if (values_.count("order")) d["order"] = values_.at("order");
        if (values_.count("style")) d["style"] = values_.at("style");
        if (values_.count("yAxis")) d["yAxis"] = values_.at("yAxis");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection annotations_;
};

/// Generated from test-specsheets/auxiliary/LoopVariable/.
class LoopVariable : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"initialValue", "any", true, std::nullopt, std::string("LoopVariable-0001"), "LoopVariable-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"subsequentValues", "SIdRef", true, std::string("LoopVariable-0003"), std::string("LoopVariable-0002"), "LoopVariable-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"initialValue", "subsequentValues"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "LoopVariable-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "LoopVariable"; }

    jsoncons::json get_initialValue() const { auto it = values_.find("initialValue"); if (it == values_.end()) throw ApiError(std::string("initialValue") + " is not set"); return it->second; }
    void set_initialValue(const jsoncons::json& value) { values_["initialValue"] = value; }
    bool is_set_initialValue() const { return values_.count("initialValue") > 0; }
    void unset_initialValue() { values_.erase("initialValue"); }

    std::string get_subsequentValues() const { auto it = values_.find("subsequentValues"); if (it == values_.end()) throw ApiError(std::string("subsequentValues") + " is not set"); return it->second.as<std::string>(); }
    void set_subsequentValues(const std::string& value) { values_["subsequentValues"] = jsoncons::json(value); }
    bool is_set_subsequentValues() const { return values_.count("subsequentValues") > 0; }
    void unset_subsequentValues() { values_.erase("subsequentValues"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("initialValue")) d["initialValue"] = values_.at("initialValue");
        if (values_.count("subsequentValues")) d["subsequentValues"] = values_.at("subsequentValues");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection annotations_;
};

/// Generated from test-specsheets/auxiliary/OutputParameter/.
class OutputParameter : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"value", "any", true, std::nullopt, std::string("OutputParameter-0001"), "OutputParameter-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"value"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "OutputParameter-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "OutputParameter"; }

    jsoncons::json get_value() const { auto it = values_.find("value"); if (it == values_.end()) throw ApiError(std::string("value") + " is not set"); return it->second; }
    void set_value(const jsoncons::json& value) { values_["value"] = value; }
    bool is_set_value() const { return values_.count("value") > 0; }
    void unset_value() { values_.erase("value"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("value")) d["value"] = values_.at("value");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection annotations_;
};

/// Generated from test-specsheets/auxiliary/TaskParameter/.
class TaskParameter : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"value", "any", true, std::nullopt, std::string("TaskParameter-0001"), "TaskParameter-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"value"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "TaskParameter-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "TaskParameter"; }

    jsoncons::json get_value() const { auto it = values_.find("value"); if (it == values_.end()) throw ApiError(std::string("value") + " is not set"); return it->second; }
    void set_value(const jsoncons::json& value) { values_["value"] = value; }
    bool is_set_value() const { return values_.count("value") > 0; }
    void unset_value() { values_.erase("value"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("value")) d["value"] = values_.at("value");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection annotations_;
};

/// Generated from test-specsheets/auxiliary/WorkingAlgorithm/.
class WorkingAlgorithm : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"algorithm", "StringOrRef", true, std::nullopt, std::string("WorkingAlgorithm-0001"), "WorkingAlgorithm-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"notes", "any", false, std::string("SEDBase-0003"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"annotations", "array", false, std::string("SEDBase-0004"), std::nullopt, "SEDBase-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Annotation"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"algorithm"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "WorkingAlgorithm-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("SEDBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::string("SEDBase-0002"); }
    std::string base_catchall() const override { return "SEDBase-0000"; }
    std::string class_name() const override { return "WorkingAlgorithm"; }

    std::string get_algorithm_value() const { return get_or_ref_value_node("algorithm").as<std::string>(); }
    std::string get_algorithm_ref() const { return get_or_ref_ref_node("algorithm").as<std::string>(); }
    void set_algorithm_value(const std::string& value) { set_or_ref_value_node("algorithm", jsoncons::json(value)); }
    void set_algorithm_ref(const std::string& ref) { set_or_ref_ref_node("algorithm", ref); }
    bool is_algorithm_ref() const { return is_or_ref_ref("algorithm"); }
    bool is_set_algorithm() const { return values_.count("algorithm") > 0; }
    void unset_algorithm() { values_.erase("algorithm"); or_ref_is_ref_.erase("algorithm"); }

    jsoncons::json get_notes() const { auto it = values_.find("notes"); if (it == values_.end()) throw ApiError(std::string("notes") + " is not set"); return it->second; }
    void set_notes(const jsoncons::json& value) { values_["notes"] = value; }
    bool is_set_notes() const { return values_.count("notes") > 0; }
    void unset_notes() { values_.erase("notes"); }

    std::vector<SedBase*> get_annotations() const { return annotations_.items(); }
    void add_annotations(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_annotations(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); annotations_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_annotations(size_t index) { annotations_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : annotations_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : annotations_.items()) { out.push_back(ChildLoc{item, "/annotations/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "annotations") return annotations_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("algorithm")) d["algorithm"] = values_.at("algorithm");
        if (values_.count("notes")) d["notes"] = values_.at("notes");
        if (annotations_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : annotations_.items()) arr.push_back(item->to_json_value()); d["annotations"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection annotations_;
};

/// Opaque holder for a AbstractTask instance whose _type names an
/// unregistered namespace prefix (see Design.md's Namespaces section) -
/// round-trips unchanged, never itself a validation error.
class UnknownAbstractTask : public SedBase {
public:
    UnknownAbstractTask(std::string type_value, jsoncons::json raw)
        : type_value_(std::move(type_value)), raw_(std::move(raw)) {}

    std::string get_type() const { return type_value_; }
    std::string class_name() const override { return "UnknownAbstractTask"; }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = raw_;
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        return d;
    }

    std::set<std::string> allowed_keys() const override {
        std::set<std::string> keys;
        for (const auto& kv : raw_.object_range()) keys.insert(kv.key());
        return keys;
    }

protected:
    std::vector<ValidationProblem> validate_own() override { return {}; }

private:
    std::string type_value_;
    jsoncons::json raw_;
};

/// Opaque holder for a RangeInline instance whose _type names an
/// unregistered namespace prefix (see Design.md's Namespaces section) -
/// round-trips unchanged, never itself a validation error.
class UnknownRangeInline : public SedBase {
public:
    UnknownRangeInline(std::string type_value, jsoncons::json raw)
        : type_value_(std::move(type_value)), raw_(std::move(raw)) {}

    std::string get_type() const { return type_value_; }
    std::string class_name() const override { return "UnknownRangeInline"; }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = raw_;
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        return d;
    }

    std::set<std::string> allowed_keys() const override {
        std::set<std::string> keys;
        for (const auto& kv : raw_.object_range()) keys.insert(kv.key());
        return keys;
    }

protected:
    std::vector<ValidationProblem> validate_own() override { return {}; }

private:
    std::string type_value_;
    jsoncons::json raw_;
};

/// Opaque holder for a AbstractOutput instance whose _type names an
/// unregistered namespace prefix (see Design.md's Namespaces section) -
/// round-trips unchanged, never itself a validation error.
class UnknownAbstractOutput : public SedBase {
public:
    UnknownAbstractOutput(std::string type_value, jsoncons::json raw)
        : type_value_(std::move(type_value)), raw_(std::move(raw)) {}

    std::string get_type() const { return type_value_; }
    std::string class_name() const override { return "UnknownAbstractOutput"; }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = raw_;
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        return d;
    }

    std::set<std::string> allowed_keys() const override {
        std::set<std::string> keys;
        for (const auto& kv : raw_.object_range()) keys.insert(kv.key());
        return keys;
    }

protected:
    std::vector<ValidationProblem> validate_own() override { return {}; }

private:
    std::string type_value_;
    jsoncons::json raw_;
};

/// Opaque holder for a AbstractCurve instance whose _type names an
/// unregistered namespace prefix (see Design.md's Namespaces section) -
/// round-trips unchanged, never itself a validation error.
class UnknownAbstractCurve : public SedBase {
public:
    UnknownAbstractCurve(std::string type_value, jsoncons::json raw)
        : type_value_(std::move(type_value)), raw_(std::move(raw)) {}

    std::string get_type() const { return type_value_; }
    std::string class_name() const override { return "UnknownAbstractCurve"; }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = raw_;
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        return d;
    }

    std::set<std::string> allowed_keys() const override {
        std::set<std::string> keys;
        for (const auto& kv : raw_.object_range()) keys.insert(kv.key());
        return keys;
    }

protected:
    std::vector<ValidationProblem> validate_own() override { return {}; }

private:
    std::string type_value_;
    jsoncons::json raw_;
};

}  // namespace libsed2

// Generated concrete SED2 classes for libsed2test. GENERATED - do not
// hand-edit; regenerate from test-specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"

#include <memory>
#include <string>
#include <vector>

namespace sed2test {

/// Generated from test-specsheets/core/SEDDocument/.
class SEDDocument : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"version", "string", true, std::string(["SEDDocument-0002", "SEDDocument-0003"]), std::string("SEDDocument-0001"), "SEDDocument-0000", std::nullopt, std::nullopt, std::string("^v\\d+\\.\\d+\\.\\d+$"), std::nullopt, std::nullopt},
            FieldSpec{"constants", "dict", false, std::string("SEDDocument-0005"), std::nullopt, "SEDDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AnyValueOrRef")},
            FieldSpec{"tasks", "dict", false, std::string("SEDDocument-0006"), std::nullopt, "SEDDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractTask")},
            FieldSpec{"outputs", "dict", false, std::string("SEDDocument-0007"), std::nullopt, "SEDDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractOutput")},
            FieldSpec{"styles", "dict", false, std::string("SEDDocument-0008"), std::nullopt, "SEDDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("Style")}
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

    std::vector<std::string> get_constants() const { return constants_.ids(); }
    SedBase* get_constants_item(const std::string& item_id) const { return constants_.get(item_id); }
    void add_constants(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); constants_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_constants(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); constants_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
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

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : constants_.ids()) kids.push_back(constants_.get(i));
        for (const auto& i : tasks_.ids()) kids.push_back(tasks_.get(i));
        for (const auto& i : outputs_.ids()) kids.push_back(outputs_.get(i));
        for (const auto& i : styles_.ids()) kids.push_back(styles_.get(i));
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : constants_.ids()) out.push_back(ChildLoc{constants_.get(i), "/constants/" + i});
        for (const auto& i : tasks_.ids()) out.push_back(ChildLoc{tasks_.get(i), "/tasks/" + i});
        for (const auto& i : outputs_.ids()) out.push_back(ChildLoc{outputs_.get(i), "/outputs/" + i});
        for (const auto& i : styles_.ids()) out.push_back(ChildLoc{styles_.get(i), "/styles/" + i});
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "constants") return constants_;
        if (field_name == "tasks") return tasks_;
        if (field_name == "outputs") return outputs_;
        if (field_name == "styles") return styles_;
        return SedBase::get_dict_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("version")) d["version"] = values_.at("version");
        if (constants_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : constants_.ids()) sub[i] = constants_.get(i)->to_json_value(); d["constants"] = sub; }
        if (tasks_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : tasks_.ids()) sub[i] = tasks_.get(i)->to_json_value(); d["tasks"] = sub; }
        if (outputs_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : outputs_.ids()) sub[i] = outputs_.get(i)->to_json_value(); d["outputs"] = sub; }
        if (styles_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : styles_.ids()) sub[i] = styles_.get(i)->to_json_value(); d["styles"] = sub; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection constants_;
    IdKeyedCollection tasks_;
    IdKeyedCollection outputs_;
    IdKeyedCollection styles_;
};

/// Generated from test-specsheets/tasks/AggregationCalculation/.
class AggregationCalculation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("aggregationCalculation");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/BoundedODESimulation/.
class BoundedODESimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"relativeTolerance", "NumberOrRef", false, std::string(["AbstractODESimulation-0001", "AbstractODESimulation-0002"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteTolerance", "NumberOrRef", false, std::string(["AbstractODESimulation-0003", "AbstractODESimulation-0004"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceAdjustmentFactor", "NumberOrRef", false, std::string(["AbstractODESimulation-0007", "AbstractODESimulation-0008"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"toleranceForRootFinder", "NumberOrRef", false, std::string(["AbstractODESimulation-0009", "AbstractODESimulation-0010"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"initialStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0011", "AbstractODESimulation-0012"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumberOfSteps", "NumberOrRef", false, std::string(["AbstractODESimulation-0013", "AbstractODESimulation-0014"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0017", "AbstractODESimulation-0018"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minInternalStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0019", "AbstractODESimulation-0020"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string(["AbstractSimulation-0002", "AbstractSimulation-0003"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string(["AbstractSimulation-0004", "AbstractSimulation-0005"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("boundedODESimulation");
        if (values_.count("relativeTolerance")) d["relativeTolerance"] = values_.at("relativeTolerance");
        if (values_.count("absoluteTolerance")) d["absoluteTolerance"] = values_.at("absoluteTolerance");
        if (values_.count("absoluteToleranceAdjustmentFactor")) d["absoluteToleranceAdjustmentFactor"] = values_.at("absoluteToleranceAdjustmentFactor");
        if (values_.count("toleranceForRootFinder")) d["toleranceForRootFinder"] = values_.at("toleranceForRootFinder");
        if (values_.count("initialStepSize")) d["initialStepSize"] = values_.at("initialStepSize");
        if (values_.count("maxNumberOfSteps")) d["maxNumberOfSteps"] = values_.at("maxNumberOfSteps");
        if (values_.count("maxInternalStepSize")) d["maxInternalStepSize"] = values_.at("maxInternalStepSize");
        if (values_.count("minInternalStepSize")) d["minInternalStepSize"] = values_.at("minInternalStepSize");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/BoundedStochasticSimulation/.
class BoundedStochasticSimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"seed", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0001", "AbstractStochasticSimulation-0002"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"timeDependentRelativeTolerance", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0003", "AbstractStochasticSimulation-0004"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minimumTimeStep", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0007", "AbstractStochasticSimulation-0008"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maximumTimeStep", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0009", "AbstractStochasticSimulation-0010"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string(["AbstractSimulation-0002", "AbstractSimulation-0003"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string(["AbstractSimulation-0004", "AbstractSimulation-0005"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("boundedStochasticSimulation");
        if (values_.count("seed")) d["seed"] = values_.at("seed");
        if (values_.count("timeDependentRelativeTolerance")) d["timeDependentRelativeTolerance"] = values_.at("timeDependentRelativeTolerance");
        if (values_.count("minimumTimeStep")) d["minimumTimeStep"] = values_.at("minimumTimeStep");
        if (values_.count("maximumTimeStep")) d["maximumTimeStep"] = values_.at("maximumTimeStep");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/Calculation/.
class Calculation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"math", "StringOrRef", true, std::string(["Calculation-0002", "Calculation-0003"]), std::string("Calculation-0001"), "Calculation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("calculation");
        if (values_.count("math")) d["math"] = values_.at("math");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/CreateDataBlock/.
class CreateDataBlock : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"data", "string", true, std::string(["CreateDataBlock-0002", "CreateDataBlock-0003"]), std::string("CreateDataBlock-0001"), "CreateDataBlock-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_data() const { auto it = values_.find("data"); if (it == values_.end()) throw ApiError(std::string("data") + " is not set"); return it->second.as<std::string>(); }
    void set_data(const std::string& value) { values_["data"] = jsoncons::json(value); }
    bool is_set_data() const { return values_.count("data") > 0; }
    void unset_data() { values_.erase("data"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("createDataBlock");
        if (values_.count("data")) d["data"] = values_.at("data");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/CsvImport/.
class CsvImport : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"organization", "StringOrRef", false, std::string(["CsvImport-0004", "CsvImport-0005"]), std::nullopt, "CsvImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"separator", "StringOrRef", false, std::string(["CsvImport-0006", "CsvImport-0007"]), std::nullopt, "CsvImport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("csvImport");
        if (values_.count("organization")) d["organization"] = values_.at("organization");
        if (values_.count("separator")) d["separator"] = values_.at("separator");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/DataImport/.
class DataImport : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("dataImport");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/DrawFromDistribution/.
class DrawFromDistribution : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"distribution", "string", true, std::string(["DrawFromDistribution-0008", "DrawFromDistribution-0009"]), std::string("DrawFromDistribution-0007"), "DrawFromDistribution-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_distribution() const { auto it = values_.find("distribution"); if (it == values_.end()) throw ApiError(std::string("distribution") + " is not set"); return it->second.as<std::string>(); }
    void set_distribution(const std::string& value) { values_["distribution"] = jsoncons::json(value); }
    bool is_set_distribution() const { return values_.count("distribution") > 0; }
    void unset_distribution() { values_.erase("distribution"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("drawFromDistribution");
        if (values_.count("distribution")) d["distribution"] = values_.at("distribution");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/ExplicitODESimulation/.
class ExplicitODESimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"relativeTolerance", "NumberOrRef", false, std::string(["AbstractODESimulation-0001", "AbstractODESimulation-0002"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteTolerance", "NumberOrRef", false, std::string(["AbstractODESimulation-0003", "AbstractODESimulation-0004"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceAdjustmentFactor", "NumberOrRef", false, std::string(["AbstractODESimulation-0007", "AbstractODESimulation-0008"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"toleranceForRootFinder", "NumberOrRef", false, std::string(["AbstractODESimulation-0009", "AbstractODESimulation-0010"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"initialStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0011", "AbstractODESimulation-0012"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumberOfSteps", "NumberOrRef", false, std::string(["AbstractODESimulation-0013", "AbstractODESimulation-0014"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0017", "AbstractODESimulation-0018"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minInternalStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0019", "AbstractODESimulation-0020"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string(["AbstractSimulation-0002", "AbstractSimulation-0003"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string(["AbstractSimulation-0004", "AbstractSimulation-0005"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("explicitODESimulation");
        if (values_.count("relativeTolerance")) d["relativeTolerance"] = values_.at("relativeTolerance");
        if (values_.count("absoluteTolerance")) d["absoluteTolerance"] = values_.at("absoluteTolerance");
        if (values_.count("absoluteToleranceAdjustmentFactor")) d["absoluteToleranceAdjustmentFactor"] = values_.at("absoluteToleranceAdjustmentFactor");
        if (values_.count("toleranceForRootFinder")) d["toleranceForRootFinder"] = values_.at("toleranceForRootFinder");
        if (values_.count("initialStepSize")) d["initialStepSize"] = values_.at("initialStepSize");
        if (values_.count("maxNumberOfSteps")) d["maxNumberOfSteps"] = values_.at("maxNumberOfSteps");
        if (values_.count("maxInternalStepSize")) d["maxInternalStepSize"] = values_.at("maxInternalStepSize");
        if (values_.count("minInternalStepSize")) d["minInternalStepSize"] = values_.at("minInternalStepSize");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/ExplicitStochasticSimulation/.
class ExplicitStochasticSimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"seed", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0001", "AbstractStochasticSimulation-0002"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"timeDependentRelativeTolerance", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0003", "AbstractStochasticSimulation-0004"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minimumTimeStep", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0007", "AbstractStochasticSimulation-0008"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maximumTimeStep", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0009", "AbstractStochasticSimulation-0010"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string(["AbstractSimulation-0002", "AbstractSimulation-0003"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string(["AbstractSimulation-0004", "AbstractSimulation-0005"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("explicitStochasticSimulation");
        if (values_.count("seed")) d["seed"] = values_.at("seed");
        if (values_.count("timeDependentRelativeTolerance")) d["timeDependentRelativeTolerance"] = values_.at("timeDependentRelativeTolerance");
        if (values_.count("minimumTimeStep")) d["minimumTimeStep"] = values_.at("minimumTimeStep");
        if (values_.count("maximumTimeStep")) d["maximumTimeStep"] = values_.at("maximumTimeStep");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/FluxBalanceAnalysis/.
class FluxBalanceAnalysis : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("FluxBalanceAnalysis-0002"), std::string("FluxBalanceAnalysis-0001"), "FluxBalanceAnalysis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("fluxBalanceAnalysis");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/JacobianFull/.
class JacobianFull : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("JacobianFull-0002"), std::string("JacobianFull-0001"), "JacobianFull-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("jacobianFull");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/JacobianReduced/.
class JacobianReduced : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("JacobianReduced-0002"), std::string("JacobianReduced-0001"), "JacobianReduced-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("jacobianReduced");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/Loop/.
class Loop : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"outputVariableMap", "string", false, std::string(["Repeat-0002", "Repeat-0003"]), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"loopVariables", "dict", true, std::string("Loop-0003"), std::string("Loop-0002"), "Loop-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("LoopVariable")},
            FieldSpec{"subTasks", "dict", false, std::string("Repeat-0001"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractTask")},
            FieldSpec{"aggregateOutputVariables", "dict", false, std::string("Repeat-0004"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AggregationCalculation")},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_outputVariableMap() const { auto it = values_.find("outputVariableMap"); if (it == values_.end()) throw ApiError(std::string("outputVariableMap") + " is not set"); return it->second.as<std::string>(); }
    void set_outputVariableMap(const std::string& value) { values_["outputVariableMap"] = jsoncons::json(value); }
    bool is_set_outputVariableMap() const { return values_.count("outputVariableMap") > 0; }
    void unset_outputVariableMap() { values_.erase("outputVariableMap"); }

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

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : loopVariables_.ids()) kids.push_back(loopVariables_.get(i));
        for (const auto& i : subTasks_.ids()) kids.push_back(subTasks_.get(i));
        for (const auto& i : aggregateOutputVariables_.ids()) kids.push_back(aggregateOutputVariables_.get(i));
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : loopVariables_.ids()) out.push_back(ChildLoc{loopVariables_.get(i), "/loopVariables/" + i});
        for (const auto& i : subTasks_.ids()) out.push_back(ChildLoc{subTasks_.get(i), "/subTasks/" + i});
        for (const auto& i : aggregateOutputVariables_.ids()) out.push_back(ChildLoc{aggregateOutputVariables_.get(i), "/aggregateOutputVariables/" + i});
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
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
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("loop");
        if (values_.count("outputVariableMap")) d["outputVariableMap"] = values_.at("outputVariableMap");
        if (loopVariables_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : loopVariables_.ids()) sub[i] = loopVariables_.get(i)->to_json_value(); d["loopVariables"] = sub; }
        if (subTasks_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : subTasks_.ids()) sub[i] = subTasks_.get(i)->to_json_value(); d["subTasks"] = sub; }
        if (aggregateOutputVariables_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : aggregateOutputVariables_.ids()) sub[i] = aggregateOutputVariables_.get(i)->to_json_value(); d["aggregateOutputVariables"] = sub; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection loopVariables_;
    IdKeyedCollection subTasks_;
    IdKeyedCollection aggregateOutputVariables_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/ModelChange/.
class ModelChange : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"inputModel", "SIdRef", true, std::string("ModelChange-0002"), std::string("ModelChange-0001"), "ModelChange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"setValues", "string", false, std::string(["ModelChange-0003", "ModelChange-0004"]), std::nullopt, "ModelChange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"replaceElements", "string", false, std::string(["ModelChange-0009", "ModelChange-0010"]), std::nullopt, "ModelChange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_setValues() const { auto it = values_.find("setValues"); if (it == values_.end()) throw ApiError(std::string("setValues") + " is not set"); return it->second.as<std::string>(); }
    void set_setValues(const std::string& value) { values_["setValues"] = jsoncons::json(value); }
    bool is_set_setValues() const { return values_.count("setValues") > 0; }
    void unset_setValues() { values_.erase("setValues"); }

    std::string get_replaceElements() const { auto it = values_.find("replaceElements"); if (it == values_.end()) throw ApiError(std::string("replaceElements") + " is not set"); return it->second.as<std::string>(); }
    void set_replaceElements(const std::string& value) { values_["replaceElements"] = jsoncons::json(value); }
    bool is_set_replaceElements() const { return values_.count("replaceElements") > 0; }
    void unset_replaceElements() { values_.erase("replaceElements"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("modelChange");
        if (values_.count("inputModel")) d["inputModel"] = values_.at("inputModel");
        if (values_.count("setValues")) d["setValues"] = values_.at("setValues");
        if (values_.count("replaceElements")) d["replaceElements"] = values_.at("replaceElements");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/ModelElementList/.
class ModelElementList : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("ModelElementList-0002"), std::string("ModelElementList-0001"), "ModelElementList-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("modelElementList");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/ModelImport/.
class ModelImport : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("modelImport");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/NumericRange/.
class NumericRange : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"start", "NumberOrRef", false, std::string(["NumericRange-0001", "NumericRange-0002"]), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"end", "NumberOrRef", false, std::string(["NumericRange-0003", "NumericRange-0004"]), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"values", "string", false, std::string(["NumericRange-0011", "NumericRange-0012"]), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"values", "string", false, std::string(["Range-0001", "Range-0002"]), std::nullopt, "Range-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_values() const { auto it = values_.find("values"); if (it == values_.end()) throw ApiError(std::string("values") + " is not set"); return it->second.as<std::string>(); }
    void set_values(const std::string& value) { values_["values"] = jsoncons::json(value); }
    bool is_set_values() const { return values_.count("values") > 0; }
    void unset_values() { values_.erase("values"); }

    std::string get_values() const { auto it = values_.find("values"); if (it == values_.end()) throw ApiError(std::string("values") + " is not set"); return it->second.as<std::string>(); }
    void set_values(const std::string& value) { values_["values"] = jsoncons::json(value); }
    bool is_set_values() const { return values_.count("values") > 0; }
    void unset_values() { values_.erase("values"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("numericRange");
        if (values_.count("start")) d["start"] = values_.at("start");
        if (values_.count("end")) d["end"] = values_.at("end");
        if (values_.count("values")) d["values"] = values_.at("values");
        if (values_.count("values")) d["values"] = values_.at("values");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/OneStepODESimulation/.
class OneStepODESimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"independentStep", "NumberOrRef", true, std::string(["OneStepODESimulation-0005", "OneStepODESimulation-0006"]), std::string("OneStepODESimulation-0004"), "OneStepODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"relativeTolerance", "NumberOrRef", false, std::string(["AbstractODESimulation-0001", "AbstractODESimulation-0002"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteTolerance", "NumberOrRef", false, std::string(["AbstractODESimulation-0003", "AbstractODESimulation-0004"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"absoluteToleranceAdjustmentFactor", "NumberOrRef", false, std::string(["AbstractODESimulation-0007", "AbstractODESimulation-0008"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"toleranceForRootFinder", "NumberOrRef", false, std::string(["AbstractODESimulation-0009", "AbstractODESimulation-0010"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"initialStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0011", "AbstractODESimulation-0012"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxNumberOfSteps", "NumberOrRef", false, std::string(["AbstractODESimulation-0013", "AbstractODESimulation-0014"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maxInternalStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0017", "AbstractODESimulation-0018"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minInternalStepSize", "NumberOrRef", false, std::string(["AbstractODESimulation-0019", "AbstractODESimulation-0020"]), std::nullopt, "AbstractODESimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string(["AbstractSimulation-0002", "AbstractSimulation-0003"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string(["AbstractSimulation-0004", "AbstractSimulation-0005"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
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
        if (values_.count("absoluteToleranceAdjustmentFactor")) d["absoluteToleranceAdjustmentFactor"] = values_.at("absoluteToleranceAdjustmentFactor");
        if (values_.count("toleranceForRootFinder")) d["toleranceForRootFinder"] = values_.at("toleranceForRootFinder");
        if (values_.count("initialStepSize")) d["initialStepSize"] = values_.at("initialStepSize");
        if (values_.count("maxNumberOfSteps")) d["maxNumberOfSteps"] = values_.at("maxNumberOfSteps");
        if (values_.count("maxInternalStepSize")) d["maxInternalStepSize"] = values_.at("maxInternalStepSize");
        if (values_.count("minInternalStepSize")) d["minInternalStepSize"] = values_.at("minInternalStepSize");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/OneStepStochasticSimulation/.
class OneStepStochasticSimulation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"independentStep", "NumberOrRef", false, std::string(["OneStepStochasticSimulation-0004", "OneStepStochasticSimulation-0005"]), std::nullopt, "OneStepStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"seed", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0001", "AbstractStochasticSimulation-0002"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"timeDependentRelativeTolerance", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0003", "AbstractStochasticSimulation-0004"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"minimumTimeStep", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0007", "AbstractStochasticSimulation-0008"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"maximumTimeStep", "NumberOrRef", false, std::string(["AbstractStochasticSimulation-0009", "AbstractStochasticSimulation-0010"]), std::nullopt, "AbstractStochasticSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"model", "SIdRef", false, std::string("AbstractSimulation-0001"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string(["AbstractSimulation-0002", "AbstractSimulation-0003"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariableInit", "NumberOrRef", false, std::string(["AbstractSimulation-0004", "AbstractSimulation-0005"]), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"workingAlgorithms", "array", false, std::string("AbstractSimulation-0008"), std::nullopt, "AbstractSimulation-0000", std::nullopt, std::nullopt, std::nullopt, std::string("WorkingAlgorithm"), std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_workingAlgorithms() const { return workingAlgorithms_.items(); }
    void add_workingAlgorithms(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_workingAlgorithms(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); workingAlgorithms_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_workingAlgorithms(size_t index) { workingAlgorithms_.remove(index); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : workingAlgorithms_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : workingAlgorithms_.items()) { out.push_back(ChildLoc{item, "/workingAlgorithms/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "workingAlgorithms") return workingAlgorithms_;
        if (field_name == "taskParameters") return taskParameters_;
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
        if (values_.count("minimumTimeStep")) d["minimumTimeStep"] = values_.at("minimumTimeStep");
        if (values_.count("maximumTimeStep")) d["maximumTimeStep"] = values_.at("maximumTimeStep");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (values_.count("independentVariableInit")) d["independentVariableInit"] = values_.at("independentVariableInit");
        if (workingAlgorithms_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : workingAlgorithms_.items()) arr.push_back(item->to_json_value()); d["workingAlgorithms"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection workingAlgorithms_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/ParameterRange/.
class ParameterRange : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"modelElement", "StringOrRef", true, std::string(["ParameterRange-0002", "ParameterRange-0003"]), std::string("ParameterRange-0001"), "ParameterRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"start", "NumberOrRef", false, std::string(["NumericRange-0001", "NumericRange-0002"]), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"end", "NumberOrRef", false, std::string(["NumericRange-0003", "NumericRange-0004"]), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"values", "string", false, std::string(["NumericRange-0011", "NumericRange-0012"]), std::nullopt, "NumericRange-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"values", "string", false, std::string(["Range-0001", "Range-0002"]), std::nullopt, "Range-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_values() const { auto it = values_.find("values"); if (it == values_.end()) throw ApiError(std::string("values") + " is not set"); return it->second.as<std::string>(); }
    void set_values(const std::string& value) { values_["values"] = jsoncons::json(value); }
    bool is_set_values() const { return values_.count("values") > 0; }
    void unset_values() { values_.erase("values"); }

    std::string get_values() const { auto it = values_.find("values"); if (it == values_.end()) throw ApiError(std::string("values") + " is not set"); return it->second.as<std::string>(); }
    void set_values(const std::string& value) { values_["values"] = jsoncons::json(value); }
    bool is_set_values() const { return values_.count("values") > 0; }
    void unset_values() { values_.erase("values"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
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
        if (values_.count("values")) d["values"] = values_.at("values");
        if (values_.count("values")) d["values"] = values_.at("values");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/ParameterScan/.
class ParameterScan : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::string("ParameterScan-0002"), std::string("ParameterScan-0001"), "ParameterScan-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputVariableMap", "string", false, std::string(["Repeat-0002", "Repeat-0003"]), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"parameterRanges", "array", true, std::string("ParameterScan-0004"), std::string("ParameterScan-0003"), "ParameterScan-0000", std::nullopt, std::nullopt, std::nullopt, std::string("ParameterRangeInline"), std::nullopt},
            FieldSpec{"subTasks", "dict", false, std::string("Repeat-0001"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractTask")},
            FieldSpec{"aggregateOutputVariables", "dict", false, std::string("Repeat-0004"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AggregationCalculation")},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_outputVariableMap() const { auto it = values_.find("outputVariableMap"); if (it == values_.end()) throw ApiError(std::string("outputVariableMap") + " is not set"); return it->second.as<std::string>(); }
    void set_outputVariableMap(const std::string& value) { values_["outputVariableMap"] = jsoncons::json(value); }
    bool is_set_outputVariableMap() const { return values_.count("outputVariableMap") > 0; }
    void unset_outputVariableMap() { values_.erase("outputVariableMap"); }

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

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : subTasks_.ids()) kids.push_back(subTasks_.get(i));
        for (const auto& i : aggregateOutputVariables_.ids()) kids.push_back(aggregateOutputVariables_.get(i));
        for (auto* item : parameterRanges_.items()) kids.push_back(item);
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : subTasks_.ids()) out.push_back(ChildLoc{subTasks_.get(i), "/subTasks/" + i});
        for (const auto& i : aggregateOutputVariables_.ids()) out.push_back(ChildLoc{aggregateOutputVariables_.get(i), "/aggregateOutputVariables/" + i});
        { size_t idx = 0; for (auto* item : parameterRanges_.items()) { out.push_back(ChildLoc{item, "/parameterRanges/" + std::to_string(idx)}); idx++; } }
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
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
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("parameterScan");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("outputVariableMap")) d["outputVariableMap"] = values_.at("outputVariableMap");
        if (subTasks_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : subTasks_.ids()) sub[i] = subTasks_.get(i)->to_json_value(); d["subTasks"] = sub; }
        if (aggregateOutputVariables_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : aggregateOutputVariables_.ids()) sub[i] = aggregateOutputVariables_.get(i)->to_json_value(); d["aggregateOutputVariables"] = sub; }
        if (parameterRanges_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : parameterRanges_.items()) arr.push_back(item->to_json_value()); d["parameterRanges"] = arr; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection parameterRanges_;
    IdKeyedCollection subTasks_;
    IdKeyedCollection aggregateOutputVariables_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/Range/.
class Range : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"values", "string", false, std::string(["Range-0001", "Range-0002"]), std::nullopt, "Range-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_values() const { auto it = values_.find("values"); if (it == values_.end()) throw ApiError(std::string("values") + " is not set"); return it->second.as<std::string>(); }
    void set_values(const std::string& value) { values_["values"] = jsoncons::json(value); }
    bool is_set_values() const { return values_.count("values") > 0; }
    void unset_values() { values_.erase("values"); }

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("range");
        if (values_.count("values")) d["values"] = values_.at("values");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/RelabelData/.
class RelabelData : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"input", "SIdRef", true, std::string("RelabelData-0002"), std::string("RelabelData-0001"), "RelabelData-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("relabelData");
        if (values_.count("input")) d["input"] = values_.at("input");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/Scatter/.
class Scatter : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"outputVariableMap", "string", false, std::string(["Repeat-0002", "Repeat-0003"]), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"subTasks", "dict", false, std::string("Repeat-0001"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractTask")},
            FieldSpec{"aggregateOutputVariables", "dict", false, std::string("Repeat-0004"), std::nullopt, "Repeat-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AggregationCalculation")},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::string get_outputVariableMap() const { auto it = values_.find("outputVariableMap"); if (it == values_.end()) throw ApiError(std::string("outputVariableMap") + " is not set"); return it->second.as<std::string>(); }
    void set_outputVariableMap(const std::string& value) { values_["outputVariableMap"] = jsoncons::json(value); }
    bool is_set_outputVariableMap() const { return values_.count("outputVariableMap") > 0; }
    void unset_outputVariableMap() { values_.erase("outputVariableMap"); }

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

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : subTasks_.ids()) kids.push_back(subTasks_.get(i));
        for (const auto& i : aggregateOutputVariables_.ids()) kids.push_back(aggregateOutputVariables_.get(i));
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : subTasks_.ids()) out.push_back(ChildLoc{subTasks_.get(i), "/subTasks/" + i});
        for (const auto& i : aggregateOutputVariables_.ids()) out.push_back(ChildLoc{aggregateOutputVariables_.get(i), "/aggregateOutputVariables/" + i});
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "subTasks") return subTasks_;
        if (field_name == "aggregateOutputVariables") return aggregateOutputVariables_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("scatter");
        if (values_.count("outputVariableMap")) d["outputVariableMap"] = values_.at("outputVariableMap");
        if (subTasks_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : subTasks_.ids()) sub[i] = subTasks_.get(i)->to_json_value(); d["subTasks"] = sub; }
        if (aggregateOutputVariables_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : aggregateOutputVariables_.ids()) sub[i] = aggregateOutputVariables_.get(i)->to_json_value(); d["aggregateOutputVariables"] = sub; }
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection subTasks_;
    IdKeyedCollection aggregateOutputVariables_;
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/Span/.
class Span : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"start", "NumberOrRef", true, std::string(["Span-0002", "Span-0003"]), std::string("Span-0001"), "Span-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"end", "NumberOrRef", true, std::string(["Span-0005", "Span-0006"]), std::string("Span-0004"), "Span-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
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

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("span");
        if (values_.count("start")) d["start"] = values_.at("start");
        if (values_.count("end")) d["end"] = values_.at("end");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/tasks/SteadyState/.
class SteadyState : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"model", "SIdRef", true, std::nullopt, std::string("SteadyState-0001"), "SteadyState-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"independentVariable", "StringOrRef", false, std::string("SteadyState-0004"), std::nullopt, "SteadyState-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("steadyState");
        if (values_.count("model")) d["model"] = values_.at("model");
        if (values_.count("independentVariable")) d["independentVariable"] = values_.at("independentVariable");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/tasks/StringFormation/.
class StringFormation : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"taskParameters", "array", false, std::string("AbstractTask-0001"), std::nullopt, "AbstractTask-0000", std::nullopt, std::nullopt, std::nullopt, std::string("TaskParameter"), std::nullopt}
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

    std::vector<SedBase*> get_taskParameters() const { return taskParameters_.items(); }
    void add_taskParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_taskParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); taskParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_taskParameters(size_t index) { taskParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : taskParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : taskParameters_.items()) { out.push_back(ChildLoc{item, "/taskParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "taskParameters") return taskParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("stringFormation");
        if (taskParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : taskParameters_.items()) arr.push_back(item->to_json_value()); d["taskParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection taskParameters_;
};

/// Generated from test-specsheets/outputs/Plot2D/.
class Plot2D : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"height", "NumberOrRef", false, std::string(["Plot-0003", "Plot-0004"]), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"width", "NumberOrRef", false, std::string(["Plot-0005", "Plot-0006"]), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"curves", "dict", true, std::string("Plot2D-0002"), std::string("Plot2D-0001"), "Plot2D-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractCurve")},
            FieldSpec{"outputParameters", "array", false, std::string("AbstractOutput-0001"), std::nullopt, "AbstractOutput-0000", std::nullopt, std::nullopt, std::nullopt, std::string("OutputParameter"), std::nullopt}
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

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : curves_.ids()) kids.push_back(curves_.get(i));
        for (auto* item : outputParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : curves_.ids()) out.push_back(ChildLoc{curves_.get(i), "/curves/" + i});
        { size_t idx = 0; for (auto* item : outputParameters_.items()) { out.push_back(ChildLoc{item, "/outputParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "curves") return curves_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "outputParameters") return outputParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("plot2D");
        if (values_.count("height")) d["height"] = values_.at("height");
        if (values_.count("width")) d["width"] = values_.at("width");
        if (curves_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : curves_.ids()) sub[i] = curves_.get(i)->to_json_value(); d["curves"] = sub; }
        if (outputParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : outputParameters_.items()) arr.push_back(item->to_json_value()); d["outputParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection curves_;
    ListCollection outputParameters_;
};

/// Generated from test-specsheets/outputs/Plot3D/.
class Plot3D : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"height", "NumberOrRef", false, std::string(["Plot-0003", "Plot-0004"]), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"width", "NumberOrRef", false, std::string(["Plot-0005", "Plot-0006"]), std::nullopt, "Plot-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"surfaces", "dict", true, std::string("Plot3D-0002"), std::string("Plot3D-0001"), "Plot3D-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("Surface")},
            FieldSpec{"outputParameters", "array", false, std::string("AbstractOutput-0001"), std::nullopt, "AbstractOutput-0000", std::nullopt, std::nullopt, std::nullopt, std::string("OutputParameter"), std::nullopt}
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

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : surfaces_.ids()) kids.push_back(surfaces_.get(i));
        for (auto* item : outputParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : surfaces_.ids()) out.push_back(ChildLoc{surfaces_.get(i), "/surfaces/" + i});
        { size_t idx = 0; for (auto* item : outputParameters_.items()) { out.push_back(ChildLoc{item, "/outputParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "surfaces") return surfaces_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "outputParameters") return outputParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("plot3D");
        if (values_.count("height")) d["height"] = values_.at("height");
        if (values_.count("width")) d["width"] = values_.at("width");
        if (surfaces_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : surfaces_.ids()) sub[i] = surfaces_.get(i)->to_json_value(); d["surfaces"] = sub; }
        if (outputParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : outputParameters_.items()) arr.push_back(item->to_json_value()); d["outputParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection surfaces_;
    ListCollection outputParameters_;
};

/// Generated from test-specsheets/outputs/Report/.
class Report : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"data", "SIdRef", true, std::string("Report-0002"), std::string("Report-0001"), "Report-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"outputParameters", "array", false, std::string("AbstractOutput-0001"), std::nullopt, "AbstractOutput-0000", std::nullopt, std::nullopt, std::nullopt, std::string("OutputParameter"), std::nullopt}
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

    std::vector<SedBase*> get_outputParameters() const { return outputParameters_.items(); }
    void add_outputParameters(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputParameters_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_outputParameters(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); outputParameters_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_outputParameters(size_t index) { outputParameters_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (auto* item : outputParameters_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        { size_t idx = 0; for (auto* item : outputParameters_.items()) { out.push_back(ChildLoc{item, "/outputParameters/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "outputParameters") return outputParameters_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("report");
        if (values_.count("data")) d["data"] = values_.at("data");
        if (outputParameters_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : outputParameters_.items()) arr.push_back(item->to_json_value()); d["outputParameters"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    ListCollection outputParameters_;
};

/// Generated from test-specsheets/auxiliary/Annotation/.
class Annotation : public SedBase {
public:
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

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/Axis/.
class Axis : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"min", "NumberOrRef", false, std::string(["Axis-0003", "Axis-0004"]), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"max", "NumberOrRef", false, std::string(["Axis-0005", "Axis-0006"]), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"style", "SIdRef", false, std::string("Axis-0009"), std::nullopt, "Axis-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
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

    std::string get_style() const { auto it = values_.find("style"); if (it == values_.end()) throw ApiError(std::string("style") + " is not set"); return it->second.as<std::string>(); }
    void set_style(const std::string& value) { values_["style"] = jsoncons::json(value); }
    bool is_set_style() const { return values_.count("style") > 0; }
    void unset_style() { values_.erase("style"); }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("min")) d["min"] = values_.at("min");
        if (values_.count("max")) d["max"] = values_.at("max");
        if (values_.count("style")) d["style"] = values_.at("style");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/Curve/.
class Curve : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"curveType", "string", true, std::string(["Curve-0002", "Curve-0003"]), std::string("Curve-0001"), "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"y", "SIdRef", true, std::string("Curve-0005"), std::string("Curve-0004"), "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"xErrorUpper", "SIdRef", false, std::string("Curve-0006"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"xErrorLower", "SIdRef", false, std::string("Curve-0007"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yErrorUpper", "SIdRef", false, std::string("Curve-0008"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yErrorLower", "SIdRef", false, std::string("Curve-0009"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yFrom", "SIdRef", false, std::string("Curve-0010"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yTo", "SIdRef", false, std::string("Curve-0011"), std::nullopt, "Curve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"x", "SIdRef", true, std::string("AbstractCurve-0002"), std::string("AbstractCurve-0001"), "AbstractCurve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"style", "SIdRef", false, std::string("AbstractCurve-0005"), std::nullopt, "AbstractCurve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"yAxis", "string", false, std::string(["AbstractCurve-0006", "AbstractCurve-0007"]), std::nullopt, "AbstractCurve-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
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

    std::string get_curveType() const { auto it = values_.find("curveType"); if (it == values_.end()) throw ApiError(std::string("curveType") + " is not set"); return it->second.as<std::string>(); }
    void set_curveType(const std::string& value) { values_["curveType"] = jsoncons::json(value); }
    bool is_set_curveType() const { return values_.count("curveType") > 0; }
    void unset_curveType() { values_.erase("curveType"); }

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

    std::string get_style() const { auto it = values_.find("style"); if (it == values_.end()) throw ApiError(std::string("style") + " is not set"); return it->second.as<std::string>(); }
    void set_style(const std::string& value) { values_["style"] = jsoncons::json(value); }
    bool is_set_style() const { return values_.count("style") > 0; }
    void unset_style() { values_.erase("style"); }

    std::string get_yAxis() const { auto it = values_.find("yAxis"); if (it == values_.end()) throw ApiError(std::string("yAxis") + " is not set"); return it->second.as<std::string>(); }
    void set_yAxis(const std::string& value) { values_["yAxis"] = jsoncons::json(value); }
    bool is_set_yAxis() const { return values_.count("yAxis") > 0; }
    void unset_yAxis() { values_.erase("yAxis"); }

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
        if (values_.count("style")) d["style"] = values_.at("style");
        if (values_.count("yAxis")) d["yAxis"] = values_.at("yAxis");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/OutputParameter/.
class OutputParameter : public SedBase {
public:
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

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/TaskParameter/.
class TaskParameter : public SedBase {
public:
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

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/WorkingAlgorithm/.
class WorkingAlgorithm : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"algorithm", "StringOrRef", true, std::nullopt, std::string("WorkingAlgorithm-0001"), "WorkingAlgorithm-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
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

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("algorithm")) d["algorithm"] = values_.at("algorithm");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
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

}  // namespace sed2test

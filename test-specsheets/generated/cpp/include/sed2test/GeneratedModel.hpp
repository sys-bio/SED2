// Generated concrete SED2 classes. GENERATED - do not
// hand-edit; regenerate from test-specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"

#include <memory>
#include <string>
#include <vector>

namespace sed2test {

/// Generated from test-specsheets/core/TestDocument/.
class TestDocument : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"version", "string", true, std::nullopt, std::string("TestDocument-0001"), "TestDocument-0000", std::nullopt, std::nullopt, std::string("^v\\d+\\.\\d+\\.\\d+$"), std::nullopt, std::nullopt},
            FieldSpec{"widgets", "dict", false, std::string("TestDocument-0002"), std::nullopt, "TestDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractWidget")},
            FieldSpec{"reports", "dict", false, std::string("TestDocument-0003"), std::nullopt, "TestDocument-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("AbstractReport")}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"version"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "TestDocument-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("TestBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::nullopt; }
    std::string base_catchall() const override { return "TestBase-0000"; }
    std::string class_name() const override { return "TestDocument"; }

    std::string get_version() const { auto it = values_.find("version"); if (it == values_.end()) throw ApiError(std::string("version") + " is not set"); return it->second.as<std::string>(); }
    void set_version(const std::string& value) { values_["version"] = jsoncons::json(value); }
    bool is_set_version() const { return values_.count("version") > 0; }
    void unset_version() { values_.erase("version"); }

    std::vector<std::string> get_widgets() const { return widgets_.ids(); }
    SedBase* get_widgets_item(const std::string& item_id) const { return widgets_.get(item_id); }
    void add_widgets(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); widgets_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_widgets(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); widgets_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_widgets(const std::string& item_id) { widgets_.remove(item_id); }
    void set_id_on_widgets(const std::string& old_id, const std::string& new_id) { widgets_.set_id(old_id, new_id); }

    std::vector<std::string> get_reports() const { return reports_.ids(); }
    SedBase* get_reports_item(const std::string& item_id) const { return reports_.get(item_id); }
    void add_reports(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); reports_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_reports(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); reports_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_reports(const std::string& item_id) { reports_.remove(item_id); }
    void set_id_on_reports(const std::string& old_id, const std::string& new_id) { reports_.set_id(old_id, new_id); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : widgets_.ids()) kids.push_back(widgets_.get(i));
        for (const auto& i : reports_.ids()) kids.push_back(reports_.get(i));
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : widgets_.ids()) out.push_back(ChildLoc{widgets_.get(i), "/widgets/" + i});
        for (const auto& i : reports_.ids()) out.push_back(ChildLoc{reports_.get(i), "/reports/" + i});
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "widgets") return widgets_;
        if (field_name == "reports") return reports_;
        return SedBase::get_dict_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("version")) d["version"] = values_.at("version");
        if (widgets_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : widgets_.ids()) sub[i] = widgets_.get(i)->to_json_value(); d["widgets"] = sub; }
        if (reports_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : reports_.ids()) sub[i] = reports_.get(i)->to_json_value(); d["reports"] = sub; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection widgets_;
    IdKeyedCollection reports_;
};

/// Generated from test-specsheets/tasks/FancyWidget/.
class FancyWidget : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"value", "StringOrRef", true, std::nullopt, std::string("FancyWidget-0001"), "FancyWidget-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"label", "StringOrRef", false, std::string("AbstractWidget-0001"), std::nullopt, "AbstractWidget-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"retries", "integer", false, std::string("WidgetOptions-0001"), std::nullopt, "WidgetOptions-0000", 0.0, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"timeoutSeconds", "number", false, std::string("WidgetOptions-0002"), std::nullopt, "WidgetOptions-0000", std::nullopt, 0.0, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"choices", "dict", false, std::nullopt, std::nullopt, "FancyWidget-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::string("ChoiceInline")},
            FieldSpec{"notes", "array", false, std::nullopt, std::nullopt, "WidgetOptions-0000", std::nullopt, std::nullopt, std::nullopt, std::string("Note"), std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"value"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("fancyWidget"); }
    std::optional<std::string> type_rule_id() const override { return std::string("FancyWidget-0002"); }
    std::string own_catchall() const override { return "FancyWidget-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("TestBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::nullopt; }
    std::string base_catchall() const override { return "TestBase-0000"; }
    std::string class_name() const override { return "FancyWidget"; }
    std::string get_type() const { return "fancyWidget"; }

    std::string get_value_value() const { return get_or_ref_value_node("value").as<std::string>(); }
    std::string get_value_ref() const { return get_or_ref_ref_node("value").as<std::string>(); }
    void set_value_value(const std::string& value) { set_or_ref_value_node("value", jsoncons::json(value)); }
    void set_value_ref(const std::string& ref) { set_or_ref_ref_node("value", ref); }
    bool is_value_ref() const { return is_or_ref_ref("value"); }
    bool is_set_value() const { return values_.count("value") > 0; }
    void unset_value() { values_.erase("value"); or_ref_is_ref_.erase("value"); }

    std::string get_label_value() const { return get_or_ref_value_node("label").as<std::string>(); }
    std::string get_label_ref() const { return get_or_ref_ref_node("label").as<std::string>(); }
    void set_label_value(const std::string& value) { set_or_ref_value_node("label", jsoncons::json(value)); }
    void set_label_ref(const std::string& ref) { set_or_ref_ref_node("label", ref); }
    bool is_label_ref() const { return is_or_ref_ref("label"); }
    bool is_set_label() const { return values_.count("label") > 0; }
    void unset_label() { values_.erase("label"); or_ref_is_ref_.erase("label"); }

    int64_t get_retries() const { auto it = values_.find("retries"); if (it == values_.end()) throw ApiError(std::string("retries") + " is not set"); return it->second.as<int64_t>(); }
    void set_retries(int64_t value) { values_["retries"] = jsoncons::json(value); }
    bool is_set_retries() const { return values_.count("retries") > 0; }
    void unset_retries() { values_.erase("retries"); }

    double get_timeoutSeconds() const { auto it = values_.find("timeoutSeconds"); if (it == values_.end()) throw ApiError(std::string("timeoutSeconds") + " is not set"); return it->second.as<double>(); }
    void set_timeoutSeconds(double value) { values_["timeoutSeconds"] = jsoncons::json(value); }
    bool is_set_timeoutSeconds() const { return values_.count("timeoutSeconds") > 0; }
    void unset_timeoutSeconds() { values_.erase("timeoutSeconds"); }

    std::vector<std::string> get_choices() const { return choices_.ids(); }
    SedBase* get_choices_item(const std::string& item_id) const { return choices_.get(item_id); }
    void add_choices(const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); choices_.add(item_id, std::move(obj)); raw->attach(this, get_document()); }
    void insert_choices(size_t index, const std::string& item_id, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); choices_.insert(index, item_id, std::move(obj)); raw->attach(this, get_document()); }
    void remove_choices(const std::string& item_id) { choices_.remove(item_id); }
    void set_id_on_choices(const std::string& old_id, const std::string& new_id) { choices_.set_id(old_id, new_id); }

    std::vector<SedBase*> get_notes() const { return notes_.items(); }
    void add_notes(std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); notes_.add(std::move(obj)); raw->attach(this, get_document()); }
    void insert_notes(size_t index, std::unique_ptr<SedBase> obj) { SedBase* raw = obj.get(); notes_.insert(index, std::move(obj)); raw->attach(this, get_document()); }
    void remove_notes(size_t index) { notes_.remove(index); }

    std::vector<SedBase*> children() override {
        std::vector<SedBase*> kids;
        for (const auto& i : choices_.ids()) kids.push_back(choices_.get(i));
        for (auto* item : notes_.items()) kids.push_back(item);
        return kids;
    }

    std::vector<ChildLoc> children_with_locations() override {
        std::vector<ChildLoc> out;
        for (const auto& i : choices_.ids()) out.push_back(ChildLoc{choices_.get(i), "/choices/" + i});
        { size_t idx = 0; for (auto* item : notes_.items()) { out.push_back(ChildLoc{item, "/notes/" + std::to_string(idx)}); idx++; } }
        return out;
    }

    IdKeyedCollection& get_dict_collection(const std::string& field_name) override {
        if (field_name == "choices") return choices_;
        return SedBase::get_dict_collection(field_name);
    }

    ListCollection& get_list_collection(const std::string& field_name) override {
        if (field_name == "notes") return notes_;
        return SedBase::get_list_collection(field_name);
    }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("fancyWidget");
        if (values_.count("value")) d["value"] = values_.at("value");
        if (values_.count("label")) d["label"] = values_.at("label");
        if (values_.count("retries")) d["retries"] = values_.at("retries");
        if (values_.count("timeoutSeconds")) d["timeoutSeconds"] = values_.at("timeoutSeconds");
        if (choices_.size() > 0) { jsoncons::json sub = jsoncons::json::object(); for (const auto& i : choices_.ids()) sub[i] = choices_.get(i)->to_json_value(); d["choices"] = sub; }
        if (notes_.size() > 0) { jsoncons::json arr = jsoncons::json::array(); for (auto* item : notes_.items()) arr.push_back(item->to_json_value()); d["notes"] = arr; }
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }

private:
    IdKeyedCollection choices_;
    ListCollection notes_;
};

/// Generated from test-specsheets/tasks/SimpleWidget/.
class SimpleWidget : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"value", "StringOrRef", true, std::nullopt, std::string("SimpleWidget-0001"), "SimpleWidget-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"label", "StringOrRef", false, std::string("AbstractWidget-0001"), std::nullopt, "AbstractWidget-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"value"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("simpleWidget"); }
    std::optional<std::string> type_rule_id() const override { return std::string("SimpleWidget-0002"); }
    std::string own_catchall() const override { return "SimpleWidget-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("TestBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::nullopt; }
    std::string base_catchall() const override { return "TestBase-0000"; }
    std::string class_name() const override { return "SimpleWidget"; }
    const std::map<std::string, std::vector<FieldSpec>>& namespace_fields() const override {
        static const std::map<std::string, std::vector<FieldSpec>> m = {
            {"acme", {FieldSpec{"acme@priority", "NumberOrRef", false, std::string("SimpleWidget-acme-0001"), std::nullopt, "SimpleWidget-acme-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}}}
        };
        return m;
    }
    const std::map<std::string, std::string>& namespace_catchall() const override {
        static const std::map<std::string, std::string> m = {{"acme", "SimpleWidget-acme-0000"}};
        return m;
    }
    const std::set<std::string>& known_namespace_prefixes() const override {
        static const std::set<std::string> s = {"acme"};
        return s;
    }
    std::string get_type() const { return "simpleWidget"; }

    std::string get_value_value() const { return get_or_ref_value_node("value").as<std::string>(); }
    std::string get_value_ref() const { return get_or_ref_ref_node("value").as<std::string>(); }
    void set_value_value(const std::string& value) { set_or_ref_value_node("value", jsoncons::json(value)); }
    void set_value_ref(const std::string& ref) { set_or_ref_ref_node("value", ref); }
    bool is_value_ref() const { return is_or_ref_ref("value"); }
    bool is_set_value() const { return values_.count("value") > 0; }
    void unset_value() { values_.erase("value"); or_ref_is_ref_.erase("value"); }

    std::string get_label_value() const { return get_or_ref_value_node("label").as<std::string>(); }
    std::string get_label_ref() const { return get_or_ref_ref_node("label").as<std::string>(); }
    void set_label_value(const std::string& value) { set_or_ref_value_node("label", jsoncons::json(value)); }
    void set_label_ref(const std::string& ref) { set_or_ref_ref_node("label", ref); }
    bool is_label_ref() const { return is_or_ref_ref("label"); }
    bool is_set_label() const { return values_.count("label") > 0; }
    void unset_label() { values_.erase("label"); or_ref_is_ref_.erase("label"); }

    double get_acme_priority_value() const { return get_or_ref_value_node("acme@priority").as<double>(); }
    std::string get_acme_priority_ref() const { return get_or_ref_ref_node("acme@priority").as<std::string>(); }
    void set_acme_priority_value(double value) { set_or_ref_value_node("acme@priority", jsoncons::json(value)); }
    void set_acme_priority_ref(const std::string& ref) { set_or_ref_ref_node("acme@priority", ref); }
    bool is_acme_priority_ref() const { return is_or_ref_ref("acme@priority"); }
    bool is_set_acme_priority() const { return values_.count("acme@priority") > 0; }
    void unset_acme_priority() { values_.erase("acme@priority"); or_ref_is_ref_.erase("acme@priority"); }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("simpleWidget");
        if (values_.count("value")) d["value"] = values_.at("value");
        if (values_.count("label")) d["label"] = values_.at("label");
        if (values_.count("acme@priority")) d["acme@priority"] = values_.at("acme@priority");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/outputs/SimpleReport/.
class SimpleReport : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"source", "SIdRef", true, std::nullopt, std::string("SimpleReport-0001"), "SimpleReport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"format", "StringOrRef", false, std::string("AbstractReport-0001"), std::nullopt, "AbstractReport-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"source"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("simpleReport"); }
    std::optional<std::string> type_rule_id() const override { return std::string("SimpleReport-0002"); }
    std::string own_catchall() const override { return "SimpleReport-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("TestBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::nullopt; }
    std::string base_catchall() const override { return "TestBase-0000"; }
    std::string class_name() const override { return "SimpleReport"; }
    std::string get_type() const { return "simpleReport"; }

    std::string get_source() const { auto it = values_.find("source"); if (it == values_.end()) throw ApiError(std::string("source") + " is not set"); return it->second.as<std::string>(); }
    void set_source(const std::string& value) { values_["source"] = jsoncons::json(value); }
    bool is_set_source() const { return values_.count("source") > 0; }
    void unset_source() { values_.erase("source"); }

    std::string get_format_value() const { return get_or_ref_value_node("format").as<std::string>(); }
    std::string get_format_ref() const { return get_or_ref_ref_node("format").as<std::string>(); }
    void set_format_value(const std::string& value) { set_or_ref_value_node("format", jsoncons::json(value)); }
    void set_format_ref(const std::string& ref) { set_or_ref_ref_node("format", ref); }
    bool is_format_ref() const { return is_or_ref_ref("format"); }
    bool is_set_format() const { return values_.count("format") > 0; }
    void unset_format() { values_.erase("format"); or_ref_is_ref_.erase("format"); }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("simpleReport");
        if (values_.count("source")) d["source"] = values_.at("source");
        if (values_.count("format")) d["format"] = values_.at("format");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/Choice/.
class Choice : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"label", "StringOrRef", false, std::string("Choice-0003"), std::nullopt, "Choice-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
        };
        return specs;
    }
    std::optional<std::string> type_const() const override { return std::string("choice"); }
    std::optional<std::string> type_rule_id() const override { return std::string("Choice-0002"); }
    std::string own_catchall() const override { return "Choice-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("TestBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::nullopt; }
    std::string base_catchall() const override { return "TestBase-0000"; }
    std::string class_name() const override { return "Choice"; }
    std::string get_type() const { return "choice"; }

    std::string get_label_value() const { return get_or_ref_value_node("label").as<std::string>(); }
    std::string get_label_ref() const { return get_or_ref_ref_node("label").as<std::string>(); }
    void set_label_value(const std::string& value) { set_or_ref_value_node("label", jsoncons::json(value)); }
    void set_label_ref(const std::string& ref) { set_or_ref_ref_node("label", ref); }
    bool is_label_ref() const { return is_or_ref_ref("label"); }
    bool is_set_label() const { return values_.count("label") > 0; }
    void unset_label() { values_.erase("label"); or_ref_is_ref_.erase("label"); }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("choice");
        if (values_.count("label")) d["label"] = values_.at("label");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/Note/.
class Note : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"text", "StringOrRef", true, std::nullopt, std::string("Note-0001"), "Note-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"text"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::nullopt; }
    std::optional<std::string> type_rule_id() const override { return std::nullopt; }
    std::string own_catchall() const override { return "Note-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("TestBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::nullopt; }
    std::string base_catchall() const override { return "TestBase-0000"; }
    std::string class_name() const override { return "Note"; }

    std::string get_text_value() const { return get_or_ref_value_node("text").as<std::string>(); }
    std::string get_text_ref() const { return get_or_ref_ref_node("text").as<std::string>(); }
    void set_text_value(const std::string& value) { set_or_ref_value_node("text", jsoncons::json(value)); }
    void set_text_ref(const std::string& ref) { set_or_ref_ref_node("text", ref); }
    bool is_text_ref() const { return is_or_ref_ref("text"); }
    bool is_set_text() const { return values_.count("text") > 0; }
    void unset_text() { values_.erase("text"); or_ref_is_ref_.erase("text"); }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        if (values_.count("text")) d["text"] = values_.at("text");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/auxiliary/WeightedChoice/.
class WeightedChoice : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"weight", "NumberOrRef", true, std::nullopt, std::string("WeightedChoice-0001"), "WeightedChoice-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"label", "StringOrRef", false, std::string("Choice-0003"), std::nullopt, "Choice-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"weight"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("weightedChoice"); }
    std::optional<std::string> type_rule_id() const override { return std::string("WeightedChoice-0002"); }
    std::string own_catchall() const override { return "WeightedChoice-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("TestBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::nullopt; }
    std::string base_catchall() const override { return "TestBase-0000"; }
    std::string class_name() const override { return "WeightedChoice"; }
    std::string get_type() const { return "weightedChoice"; }

    double get_weight_value() const { return get_or_ref_value_node("weight").as<double>(); }
    std::string get_weight_ref() const { return get_or_ref_ref_node("weight").as<std::string>(); }
    void set_weight_value(double value) { set_or_ref_value_node("weight", jsoncons::json(value)); }
    void set_weight_ref(const std::string& ref) { set_or_ref_ref_node("weight", ref); }
    bool is_weight_ref() const { return is_or_ref_ref("weight"); }
    bool is_set_weight() const { return values_.count("weight") > 0; }
    void unset_weight() { values_.erase("weight"); or_ref_is_ref_.erase("weight"); }

    std::string get_label_value() const { return get_or_ref_value_node("label").as<std::string>(); }
    std::string get_label_ref() const { return get_or_ref_ref_node("label").as<std::string>(); }
    void set_label_value(const std::string& value) { set_or_ref_value_node("label", jsoncons::json(value)); }
    void set_label_ref(const std::string& ref) { set_or_ref_ref_node("label", ref); }
    bool is_label_ref() const { return is_or_ref_ref("label"); }
    bool is_set_label() const { return values_.count("label") > 0; }
    void unset_label() { values_.erase("label"); or_ref_is_ref_.erase("label"); }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("weightedChoice");
        if (values_.count("weight")) d["weight"] = values_.at("weight");
        if (values_.count("label")) d["label"] = values_.at("label");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Generated from test-specsheets/tasks/AcmeWidget/.
class AcmeWidget : public SedBase {
public:
    const std::vector<FieldSpec>& field_specs() const override {
        static const std::vector<FieldSpec> specs = {
            FieldSpec{"acme@acmeLevel", "NumberOrRef", true, std::nullopt, std::string("acme-AcmeWidget-0001"), "AcmeWidget-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt},
            FieldSpec{"label", "StringOrRef", false, std::string("AbstractWidget-0001"), std::nullopt, "AbstractWidget-0000", std::nullopt, std::nullopt, std::nullopt, std::nullopt, std::nullopt}
        };
        return specs;
    }
    const std::set<std::string>& required_names() const override {
        static const std::set<std::string> names = {"acme@acmeLevel"};
        return names;
    }
    std::optional<std::string> type_const() const override { return std::string("acme@acmeWidget"); }
    std::optional<std::string> type_rule_id() const override { return std::string("acme-AcmeWidget-0002"); }
    std::string own_catchall() const override { return "acme-AcmeWidget-0000"; }
    std::optional<std::string> name_rule_id() const override { return std::string("TestBase-0001"); }
    std::optional<std::string> desc_rule_id() const override { return std::nullopt; }
    std::string base_catchall() const override { return "TestBase-0000"; }
    std::string class_name() const override { return "AcmeWidget"; }
    std::string get_type() const { return "acme@acmeWidget"; }

    double get_acme_acmeLevel_value() const { return get_or_ref_value_node("acme@acmeLevel").as<double>(); }
    std::string get_acme_acmeLevel_ref() const { return get_or_ref_ref_node("acme@acmeLevel").as<std::string>(); }
    void set_acme_acmeLevel_value(double value) { set_or_ref_value_node("acme@acmeLevel", jsoncons::json(value)); }
    void set_acme_acmeLevel_ref(const std::string& ref) { set_or_ref_ref_node("acme@acmeLevel", ref); }
    bool is_acme_acmeLevel_ref() const { return is_or_ref_ref("acme@acmeLevel"); }
    bool is_set_acme_acmeLevel() const { return values_.count("acme@acmeLevel") > 0; }
    void unset_acme_acmeLevel() { values_.erase("acme@acmeLevel"); or_ref_is_ref_.erase("acme@acmeLevel"); }

    std::string get_label_value() const { return get_or_ref_value_node("label").as<std::string>(); }
    std::string get_label_ref() const { return get_or_ref_ref_node("label").as<std::string>(); }
    void set_label_value(const std::string& value) { set_or_ref_value_node("label", jsoncons::json(value)); }
    void set_label_ref(const std::string& ref) { set_or_ref_ref_node("label", ref); }
    bool is_label_ref() const { return is_or_ref_ref("label"); }
    bool is_set_label() const { return values_.count("label") > 0; }
    void unset_label() { values_.erase("label"); or_ref_is_ref_.erase("label"); }

    jsoncons::json own_json_value() const override {
        jsoncons::json d = jsoncons::json::object();
        if (name_node_) d["name"] = *name_node_;
        if (description_node_) d["description"] = *description_node_;
        d["_type"] = values_.count("_type") ? values_.at("_type") : jsoncons::json("acme@acmeWidget");
        if (values_.count("acme@acmeLevel")) d["acme@acmeLevel"] = values_.at("acme@acmeLevel");
        if (values_.count("label")) d["label"] = values_.at("label");
        for (const auto& kv : ns_attrs_) d[kv.first] = kv.second;
        return d;
    }
};

/// Opaque holder for a AbstractWidget instance whose _type names an
/// unregistered namespace prefix (see Design.md's Namespaces section) -
/// round-trips unchanged, never itself a validation error.
class UnknownAbstractWidget : public SedBase {
public:
    UnknownAbstractWidget(std::string type_value, jsoncons::json raw)
        : type_value_(std::move(type_value)), raw_(std::move(raw)) {}

    std::string get_type() const { return type_value_; }
    std::string class_name() const override { return "UnknownAbstractWidget"; }

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

/// Opaque holder for a AbstractReport instance whose _type names an
/// unregistered namespace prefix (see Design.md's Namespaces section) -
/// round-trips unchanged, never itself a validation error.
class UnknownAbstractReport : public SedBase {
public:
    UnknownAbstractReport(std::string type_value, jsoncons::json raw)
        : type_value_(std::move(type_value)), raw_(std::move(raw)) {}

    std::string get_type() const { return type_value_; }
    std::string class_name() const override { return "UnknownAbstractReport"; }

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

/// Opaque holder for a ChoiceInline instance whose _type names an
/// unregistered namespace prefix (see Design.md's Namespaces section) -
/// round-trips unchanged, never itself a validation error.
class UnknownChoiceInline : public SedBase {
public:
    UnknownChoiceInline(std::string type_value, jsoncons::json raw)
        : type_value_(std::move(type_value)), raw_(std::move(raw)) {}

    std::string get_type() const { return type_value_; }
    std::string class_name() const override { return "UnknownChoiceInline"; }

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

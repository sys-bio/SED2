// Top-level read/write entry points for libsed2test. GENERATED - do not
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

namespace sed2test {

inline std::unique_ptr<TestDocument> read_from_string(const std::string& text) {
    register_rules();
    jsoncons::json raw = jsoncons::json::parse(text);
    auto obj = std::make_unique<TestDocument>();
    load_fields(obj.get(), raw);
    obj->attach(nullptr, obj.get());
    return obj;
}

inline std::unique_ptr<TestDocument> read_from_file(const std::string& path) {
    std::ifstream f(path);
    std::stringstream ss;
    ss << f.rdbuf();
    return read_from_string(ss.str());
}

inline std::string write_to_string(const TestDocument& doc) {
    jsoncons::json v = doc.to_json_value();
    std::string out;
    v.dump(out, jsoncons::indenting::indent);
    return out;
}

inline void write_to_file(const TestDocument& doc, const std::string& path) {
    std::ofstream f(path);
    f << write_to_string(doc);
}

}  // namespace sed2test

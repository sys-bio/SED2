// Top-level read/write entry points. GENERATED - do not
// hand-edit; regenerate from specsheets/ via generator/generate.py.
#pragma once

#include "Runtime.hpp"
#include "GeneratedModel.hpp"
#include "Dispatch.hpp"
#include "RulesData.hpp"
// The public reference API (parse_reference, get_sed_reference,
// apply_indices, get_reference_value) comes with this entry point header.
#include "RefRules.hpp"

#include <fstream>
#include <memory>
#include <sstream>
#include <string>

namespace libsed2 {

inline std::unique_ptr<SEDDocument> read_from_string(const std::string& text) {
    register_rules();
    Json raw = Json::parse(text);
    auto obj = std::make_unique<SEDDocument>();
    load_fields(obj.get(), raw);
    obj->attach(nullptr, obj.get());
    return obj;
}

inline std::unique_ptr<SEDDocument> read_from_file(const std::string& path) {
    std::ifstream f(path);
    std::stringstream ss;
    ss << f.rdbuf();
    return read_from_string(ss.str());
}

inline std::string write_to_string(const SEDDocument& doc) {
    Json v = doc.to_json_value();
    std::string out;
    v.dump(out, jsoncons::indenting::indent);
    return out;
}

inline void write_to_file(const SEDDocument& doc, const std::string& path) {
    std::ofstream f(path);
    f << write_to_string(doc);
}

}  // namespace libsed2

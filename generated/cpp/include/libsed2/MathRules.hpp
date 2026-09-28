#pragma once

#include "libsed2/MathAst.hpp"
#include "libsed2/PredefinedFunctions.hpp"
#include "libsed2/Runtime.hpp"

#include <map>
#include <string>
#include <vector>

/* GENERATED - do not hand-edit; regenerate via generator/generate.py. */
namespace libsed2 {

/// Types-0001..0004: the shared math-grammar rules any field with
/// FieldSpec::is_math (x-math) runs on its own literal string value - see
/// SedBase::validate_own() and class MathRules's forward declaration, both
/// in Runtime.hpp.
///
/// value is the field's own raw string - never a reference: validate_own()
/// only calls here for a literal string value (Types-0001.md: "When the
/// math attribute is itself a reference, ... apply only if the reference
/// resolves statically to a string constant", out of scope until reference
/// resolution exists for C++ - see this module's docstring). Returns {}
/// if value parses and every function call / bare identifier it contains
/// checks out; otherwise one ValidationProblem per violation (Types-0001
/// short-circuits the rest, same as the Python/Java targets - an
/// unparseable expression has no tree left to walk for 0002-0004).
inline std::vector<ValidationProblem> MathRules::check_math_field(
        const std::string& value, const std::string& class_name, const std::string& id_value,
        const std::string& attr, const std::string& location) {
        std::vector<ValidationProblem> problems;
        std::shared_ptr<MathNode> ast;
        try {
            ast = math_parse(value);
        } catch (const MathSyntaxError& e) {
            std::map<std::string, std::string> ph;
            ph["attr"] = attr;
            ph["class"] = class_name;
            ph["id"] = id_value;
            ph["expr"] = value;
            ph["parse-message"] = e.what();
            problems.push_back(RuleCatalog::make_problem("Types-0001", location, ph));
            return problems;
        }
        for (const MathNode* node : ast->walk()) {
            if (node->is_function_call() && !PredefinedFunctions::functions().count(node->name)) {
                std::map<std::string, std::string> ph;
                ph["attr"] = attr;
                ph["class"] = class_name;
                ph["id"] = id_value;
                ph["function"] = node->name;
                problems.push_back(RuleCatalog::make_problem("Types-0002", location, ph));
            }
        }
        for (const MathNode* node : ast->walk()) {
            if (!node->is_function_call()) continue;
            auto it = PredefinedFunctions::functions().find(node->name);
            if (it == PredefinedFunctions::functions().end()) continue;  // Types-0002's concern, not a duplicate diagnosis
            int count = static_cast<int>(node->get_num_children());
            if (!it->second.ok(count)) {
                std::map<std::string, std::string> ph;
                ph["attr"] = attr;
                ph["class"] = class_name;
                ph["id"] = id_value;
                ph["function"] = node->name;
                ph["count"] = std::to_string(count);
                ph["expected-count"] = it->second.format();
                problems.push_back(RuleCatalog::make_problem("Types-0003", location, ph));
            }
        }
        for (const MathNode* node : ast->walk()) {
            if (node->is_name() && !PredefinedFunctions::constants().count(node->name)) {
                std::map<std::string, std::string> ph;
                ph["attr"] = attr;
                ph["class"] = class_name;
                ph["id"] = id_value;
                ph["value"] = node->name;
                problems.push_back(RuleCatalog::make_problem("Types-0004", location, ph));
            }
        }
        return problems;
}

}  // namespace libsed2

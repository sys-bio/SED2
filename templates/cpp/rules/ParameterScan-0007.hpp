// ParameterScan-0007 (specsheets/tasks/ParameterScan/v1.0.0/validation/ParameterScan-0007.md):
// "The entries of a ParameterScan's parameterRanges must have pairwise distinct
// modelElement values."
//
// The dispatcher (RefRules::check_parameter_scan_ranges) has already reduced
// each entry of parameterRanges to its modelElement string, in order: the
// literal text, or the string a reference to a constant resolves to. An entry
// whose modelElement is missing, is not a string, or is a reference that does
// not resolve to a string is passed as nullopt and ignored here (the schema and
// reference rules report those). One problem per distinct value that appears
// more than once, in order of first appearance, located at the second entry
// that has the value (ctx.location + "/<index>/modelElement"; ctx.location is
// the parameterRanges list itself) so that two different duplicated values
// never share a location, which validate() would collapse into one problem.
// Comparison is exact (case-sensitive).
//
// Hand-written template (templates/cpp/rules/ParameterScan-0007.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/ParameterScan-0007.py (the reference implementation).
// ASCII only.
#pragma once

#include <map>
#include <optional>
#include <string>
#include <vector>

#include "../Runtime.hpp"

namespace sed2test {
namespace rules {
namespace parameterscan_0007 {

inline std::vector<ValidationProblem> check(const std::vector<std::optional<std::string>>& model_elements,
                                            const RuleCtx& ctx) {
    std::map<std::string, int> seen;
    std::vector<ValidationProblem> out;
    for (size_t index = 0; index < model_elements.size(); index++) {
        if (!model_elements[index]) continue;
        const std::string& element = *model_elements[index];
        if (++seen[element] == 2) {
            out.push_back(RuleCatalog::make_problem("ParameterScan-0007",
                ctx.location + "/" + std::to_string(index) + "/modelElement",
                {{"value", element}, {"class", ctx.class_name}, {"id", ctx.id_value}}));
        }
    }
    return out;
}

}  // namespace parameterscan_0007
}  // namespace rules
}  // namespace sed2test

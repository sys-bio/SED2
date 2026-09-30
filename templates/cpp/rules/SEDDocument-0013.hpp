// SEDDocument-0013 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0013.md):
// "A constant may only reference constants that appear before it in the
// constants dictionary."
//
// Only a constant whose own value IS a reference is in scope. A reference that
// isn't shaped like '#constants:...', or whose target constant doesn't precede
// this one (including one that doesn't exist, or names this same constant) is
// "not an earlier constant" by this rule's own wording. `constants` is the
// document's constants in insertion order.
//
// Hand-written template (templates/cpp/rules/SEDDocument-0013.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDDocument-0013.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../Reference.hpp"

namespace sed2test {
namespace rules {
namespace seddocument_0013 {

inline std::vector<ValidationProblem> check(const std::vector<std::pair<std::string, Json>>& constants) {
    std::vector<ValidationProblem> problems;
    for (size_t i = 0; i < constants.size(); i++) {
        const Json& value = constants[i].second;
        if (!value.is_string()) continue;
        std::string text = value.as<std::string>();
        if (text.empty() || text[0] != '#') continue;
        ParsedReference parsed = parse_reference(text);
        if (!parsed.collection || *parsed.collection != "constants" || parsed.path.empty()) continue;
        const std::string& target = parsed.path[0];
        bool earlier = false;
        for (size_t k = 0; k < i; k++) if (constants[k].first == target) earlier = true;
        if (!earlier) {
            problems.push_back(RuleCatalog::make_problem("SEDDocument-0013", "/constants/" + constants[i].first,
                {{"attr", constants[i].first}, {"value", text}}));
        }
    }
    return problems;
}

}  // namespace seddocument_0013
}  // namespace rules
}  // namespace sed2test

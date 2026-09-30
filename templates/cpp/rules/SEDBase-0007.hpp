// SEDBase-0007 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0007.md):
// "A reference must not target an AbstractOutput, or anything contained in
// one."
//
// Decided purely from the collection name: 'outputs' is the only root
// collection whose every member is AbstractOutput-rooted.
//
// Hand-written template (templates/cpp/rules/SEDBase-0007.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0007.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../Reference.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0007 {

inline std::vector<ValidationProblem> check(const ParsedReference& parsed, const RuleCtx& ctx) {
    if (parsed.collection && *parsed.collection == "outputs") {
        return {RuleCatalog::make_problem("SEDBase-0007", ctx.location,
            {{"attr", ctx.attr}, {"value", parsed.raw}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
    }
    return {};
}

}  // namespace sedbase_0007
}  // namespace rules
}  // namespace sed2test

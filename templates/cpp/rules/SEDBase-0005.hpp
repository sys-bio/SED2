// SEDBase-0005 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0005.md):
// "The first segment of a reference must name one of SEDDocument's ID-keyed
// collections: tasks, constants, outputs, or styles."
//
// Fires once if parsed.collection isn't one of the four known root collections -
// including when the reference has no colon segment at all.
//
// Hand-written template (templates/cpp/rules/SEDBase-0005.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0005.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../Reference.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0005 {

inline std::vector<ValidationProblem> check(const ParsedReference& parsed, const RuleCtx& ctx) {
    if (!parsed.collection || (*parsed.collection != "tasks" && *parsed.collection != "constants" &&
                               *parsed.collection != "outputs" && *parsed.collection != "styles")) {
        return {RuleCatalog::make_problem("SEDBase-0005", ctx.location,
            {{"attr", ctx.attr}, {"value", parsed.raw}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
    }
    return {};
}

}  // namespace sedbase_0005
}  // namespace rules
}  // namespace sed2test

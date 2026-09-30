// SEDBase-0012 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0012.md):
// "A bracket index into a constant must match the structure of that
// constant's literal value."
//
// The dispatcher has already done the actual indexing (following one
// reference-hop first) and hands this rule just the outcome: ok, the specific
// index that failed (bad_subvalue), and the constant's own literal value
// pre-formatted as a compact string for the message's {resolved-value}.
//
// Hand-written template (templates/cpp/rules/SEDBase-0012.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0012.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0012 {

inline std::vector<ValidationProblem> check(bool ok, const std::string& bad_subvalue,
                                            const std::string& resolved_value, const RuleCtx& ctx) {
    if (ok) return {};
    return {RuleCatalog::make_problem("SEDBase-0012", ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"subvalue", bad_subvalue}, {"resolved-value", resolved_value}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace sedbase_0012
}  // namespace rules
}  // namespace sed2test

// Repeat-0010 (specsheets/tasks/Repeat/v1.0.0/validation/Repeat-0010.md):
// "An entry in a Repeat's aggregateOutputVariables must not define
// appliedDimensions."
//
// defines_applied_dimensions says whether the entry's own JSON value defines
// 'appliedDimensions' at all; ctx.value is the appliedDimensions value itself.
//
// Hand-written template (templates/cpp/rules/Repeat-0010.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "libsed2" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/Repeat-0010.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace libsed2 {
namespace rules {
namespace repeat_0010 {

inline std::vector<ValidationProblem> check(bool defines_applied_dimensions, const RuleCtx& ctx) {
    if (!defines_applied_dimensions) return {};
    return {RuleCatalog::make_problem("Repeat-0010", ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace repeat_0010
}  // namespace rules
}  // namespace libsed2

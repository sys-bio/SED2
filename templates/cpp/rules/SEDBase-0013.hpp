// SEDBase-0013 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0013.md):
// "A reference to a Repeat's subTasks, its .range/.index outputs, or one of
// its loop variables is only legal when the element holding the reference is
// that Repeat itself, or lies within that Repeat's own subTasks (at any depth,
// including through a nested Repeat)."
//
// The dispatcher has already worked out which Repeat (if any) scopes this
// reference and whether the referring element is that Repeat itself or lies
// within its own subTasks (in_scope) - a plain containment-tree ancestor walk.
// The message uses no {attr}: the violation is about the reference's LOCATION
// relative to the Repeat.
//
// Hand-written template (templates/cpp/rules/SEDBase-0013.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0013.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0013 {

inline std::vector<ValidationProblem> check(bool in_scope, const std::string& target_repeat_id, const RuleCtx& ctx) {
    if (in_scope) return {};
    return {RuleCatalog::make_problem("SEDBase-0013", ctx.location,
        {{"value", ctx.value}, {"resolved-value", target_repeat_id}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace sedbase_0013
}  // namespace rules
}  // namespace sed2test

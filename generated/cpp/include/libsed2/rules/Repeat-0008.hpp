// Repeat-0008 (specsheets/tasks/Repeat/v1.0.0/validation/Repeat-0008.md):
// "Every value in a Repeat's outputVariableMap must reference one of that
// Repeat's own subTasks, or an output of one."
//
// ok is whether the entry's own reference resolved to one of THIS Repeat's own
// direct subTasks. ctx.attr is the outputVariableMap ENTRY's own key.
//
// Hand-written template (templates/cpp/rules/Repeat-0008.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "libsed2" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/Repeat-0008.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace libsed2 {
namespace rules {
namespace repeat_0008 {

inline std::vector<ValidationProblem> check(bool ok, const RuleCtx& ctx) {
    if (ok) return {};
    return {RuleCatalog::make_problem("Repeat-0008", ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace repeat_0008
}  // namespace rules
}  // namespace libsed2

// LoopVariable-0004 (specsheets/auxiliary/LoopVariable/v1.0.0/validation/LoopVariable-0004.md):
// "The subsequentValues of a LoopVariable must reference one of its enclosing
// Loop's own subTasks, or an output of one."
//
// ok is whether subsequentValues's own reference resolved to one of the enclosing
// Loop's own direct subTasks. The message uses neither {class} nor {attr}: it
// always names the fixed "LoopVariable" class.
//
// Hand-written template (templates/cpp/rules/LoopVariable-0004.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "libsed2" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/LoopVariable-0004.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace libsed2 {
namespace rules {
namespace loopvariable_0004 {

inline std::vector<ValidationProblem> check(bool ok, const RuleCtx& ctx) {
    if (ok) return {};
    return {RuleCatalog::make_problem("LoopVariable-0004", ctx.location,
        {{"value", ctx.value}, {"class", "LoopVariable"}, {"id", ctx.id_value}})};
}

}  // namespace loopvariable_0004
}  // namespace rules
}  // namespace libsed2

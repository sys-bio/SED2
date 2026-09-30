// AbstractTask-0003 (specsheets/tasks/AbstractTask/v1.0.0/validation/AbstractTask-0003.md):
// "A task may only reference constants, tasks that appear earlier in the same
// tasks dictionary, or (for a subTask) the elements listed in this rule's
// explanation." core-spec.md Section 3's chronological rule, made checkable.
//
// The dispatcher (RefRules) has already walked both the referring element's own and
// the reference's resolved target's chronological position within
// SEDDocument.tasks (through any Repeat-family subTasks nesting) and compared them
// per this rule's worked-out cases - ok is that comparison's own outcome.
//
// Hand-written template (templates/cpp/rules/AbstractTask-0003.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/AbstractTask-0003.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace sed2test {
namespace rules {
namespace abstracttask_0003 {

inline std::vector<ValidationProblem> check(bool ok, const RuleCtx& ctx) {
    if (ok) return {};
    return {RuleCatalog::make_problem("AbstractTask-0003", ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace abstracttask_0003
}  // namespace rules
}  // namespace sed2test

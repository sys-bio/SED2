// SEDBase-0008 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0008.md):
// "A dot-accessor in a reference must be one the target declares valid."
//
// accessor_ok is the dispatcher's own resolution of whether this reference's
// suffix is a declared-valid output of its target - true, false, or nullopt (not
// statically determinable). Fires only on an outright false.
//
// Hand-written template (templates/cpp/rules/SEDBase-0008.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0008.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../Reference.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0008 {

inline std::vector<ValidationProblem> check(const std::optional<bool>& accessor_ok,
                                            const std::optional<std::string>& dot_name, const RuleCtx& ctx) {
    if (!accessor_ok || *accessor_ok) return {};
    return {RuleCatalog::make_problem("SEDBase-0008", ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"subvalue", dot_name ? *dot_name : std::string()}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace sedbase_0008
}  // namespace rules
}  // namespace sed2test

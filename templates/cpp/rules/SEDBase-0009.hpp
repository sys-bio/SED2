// SEDBase-0009 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0009.md):
// "A reference must not apply more bracket indices than its target has
// dimensions."
//
// dims_before is the resolver's pre-index dimensions list, or nullopt whenever the
// target's dimension COUNT isn't statically known - only fires when it is.
//
// Hand-written template (templates/cpp/rules/SEDBase-0009.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0009.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../OutputsShape.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0009 {

inline std::vector<ValidationProblem> check(const oshape::OptDims& dims_before,
                                            const std::vector<RefIndex>& index_accessors, const RuleCtx& ctx) {
    if (!dims_before) return {};
    size_t count = index_accessors.size();
    size_t expected = dims_before->size();
    if (count <= expected) return {};
    return {RuleCatalog::make_problem("SEDBase-0009", ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"count", std::to_string(count)}, {"expected-count", std::to_string(expected)}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace sedbase_0009
}  // namespace rules
}  // namespace sed2test

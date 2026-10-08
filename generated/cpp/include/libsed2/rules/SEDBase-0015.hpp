// SEDBase-0015 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0015.md):
// "A reference required to resolve to a scalar value must apply enough
// non-range indices to reduce its target's shape to zero remaining
// dimensions."
//
// dims_after is the resolver's post-index dimensions list (only ever computed for
// a field whose declared kind requires a scalar). nullopt means the shape wasn't
// statically known - nothing to say either way. expected_type is the field's own
// declared scalar kind ("number", "string", "integer", "boolean").
//
// Hand-written template (templates/cpp/rules/SEDBase-0015.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "libsed2" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0015.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../OutputsShape.hpp"

namespace libsed2 {
namespace rules {
namespace sedbase_0015 {

inline std::vector<ValidationProblem> check(const oshape::OptDims& dims_after, const std::string& expected_type,
                                            const RuleCtx& ctx) {
    if (!dims_after) return {};
    // A trailing placeholder (source "open") stands for dimensions of an unknown
    // number: it never makes the shape definitely non-scalar.
    size_t count = 0;
    for (const auto& d : *dims_after) if (!oshape::is_open(d)) count++;
    if (count == 0) return {};
    return {RuleCatalog::make_problem("SEDBase-0015", ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"expected-type", expected_type}, {"count", std::to_string(count)}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace sedbase_0015
}  // namespace rules
}  // namespace libsed2

// SEDBase-0014 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0014.md):
// "An integer or range index into a dimension whose size is sourced as
// runtime and documents a min should warn when the index requires more
// entries than min guarantees."
//
// Per-dimension: only fires when that dimension's own source is "runtime" AND it
// carries a min - the complement of SEDBase-0011's own guard. A bare index n needs
// min > n; a range [a:b] only checks the given end b (an explicit, non-negative
// value) and needs min >= b.
//
// Hand-written template (templates/cpp/rules/SEDBase-0014.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0014.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../OutputsShape.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0014 {

inline std::vector<ValidationProblem> check(const oshape::OptDims& dims_before,
                                            const std::vector<RefIndex>& index_accessors, const RuleCtx& ctx) {
    std::vector<ValidationProblem> problems;
    if (!dims_before) return problems;
    for (size_t i = 0; i < index_accessors.size(); i++) {
        if (i >= dims_before->size()) continue;
        const oshape::Dim& dim = (*dims_before)[i];
        if (!dim.source || *dim.source != "runtime" || !dim.min) continue;
        long long m = *dim.min;
        const RefIndex& idx = index_accessors[i];
        if (idx.is_int()) {
            if (!(m > idx.ival)) {
                problems.push_back(RuleCatalog::make_problem("SEDBase-0014", ctx.location,
                    {{"attr", ctx.attr}, {"value", ctx.value}, {"subvalue", std::to_string(idx.ival)}, {"min", std::to_string(m)}, {"class", ctx.class_name}, {"id", ctx.id_value}}));
            }
        } else if (idx.is_range()) {
            if (idx.b && *idx.b >= 0 && !(m >= *idx.b)) {
                std::string subvalue = "[" + (idx.a ? std::to_string(*idx.a) : std::string()) + ":" +
                                       std::to_string(*idx.b) + "]";
                problems.push_back(RuleCatalog::make_problem("SEDBase-0014", ctx.location,
                    {{"attr", ctx.attr}, {"value", ctx.value}, {"subvalue", subvalue}, {"min", std::to_string(m)}, {"class", ctx.class_name}, {"id", ctx.id_value}}));
            }
        }
    }
    return problems;
}

}  // namespace sedbase_0014
}  // namespace rules
}  // namespace sed2test

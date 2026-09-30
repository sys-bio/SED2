// SEDBase-0010 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0010.md):
// "A label index in a reference must name one of the labels of the dimension
// it indexes."
//
// Only checks index positions that fall within dims_before's own length, and only
// when that dimension's labels are static.
//
// Hand-written template (templates/cpp/rules/SEDBase-0010.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0010.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../OutputsShape.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0010 {

inline std::vector<ValidationProblem> check(const oshape::OptDims& dims_before,
                                            const std::vector<RefIndex>& index_accessors, const RuleCtx& ctx) {
    std::vector<ValidationProblem> problems;
    if (!dims_before) return problems;
    for (size_t i = 0; i < index_accessors.size(); i++) {
        const RefIndex& idx = index_accessors[i];
        if (!idx.is_label() || i >= dims_before->size()) continue;
        const auto& labels = (*dims_before)[i].labels;
        if (!labels) continue;
        bool found = false;
        std::string allowed;
        for (size_t k = 0; k < labels->size(); k++) {
            if ((*labels)[k] == idx.sval) found = true;
            if (k) allowed += ", ";
            allowed += (*labels)[k];
        }
        if (!found) {
            problems.push_back(RuleCatalog::make_problem("SEDBase-0010", ctx.location,
                {{"attr", ctx.attr}, {"value", ctx.value}, {"subvalue", idx.sval}, {"allowed", allowed}, {"class", ctx.class_name}, {"id", ctx.id_value}}));
        }
    }
    return problems;
}

}  // namespace sedbase_0010
}  // namespace rules
}  // namespace sed2test

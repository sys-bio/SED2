// SEDBase-0011 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0011.md):
// "An integer or range index in a reference must fall within the size of the
// dimension it indexes."
//
// Per-dimension: only fires when THAT dimension's own size resolved to a concrete
// int. Negative indices count from the end: for size n, legal integer indices are
// -n..n-1; for a range [a:b], BOTH given ends must lie within -n..n and the range
// must select at least one element once open ends are filled in.
//
// Hand-written template (templates/cpp/rules/SEDBase-0011.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0011.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../OutputsShape.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0011 {

inline std::string range_text(const std::optional<long long>& a, const std::optional<long long>& b) {
    return "[" + (a ? std::to_string(*a) : std::string()) + ":" + (b ? std::to_string(*b) : std::string()) + "]";
}

inline std::vector<ValidationProblem> check(const oshape::OptDims& dims_before,
                                            const std::vector<RefIndex>& index_accessors, const RuleCtx& ctx) {
    std::vector<ValidationProblem> problems;
    if (!dims_before) return problems;
    for (size_t i = 0; i < index_accessors.size(); i++) {
        if (i >= dims_before->size()) continue;
        const auto& size = (*dims_before)[i].size;
        if (!size) continue;
        long long n = *size;
        const RefIndex& idx = index_accessors[i];
        if (idx.is_int()) {
            if (idx.ival < -n || idx.ival > n - 1) {
                problems.push_back(RuleCatalog::make_problem("SEDBase-0011", ctx.location,
                    {{"attr", ctx.attr}, {"value", ctx.value}, {"subvalue", std::to_string(idx.ival)}, {"min", std::to_string(-n)}, {"max", std::to_string(n - 1)}, {"class", ctx.class_name}, {"id", ctx.id_value}}));
            }
        } else if (idx.is_range()) {
            bool bad = false;
            if (idx.a && !(-n <= *idx.a && *idx.a <= n)) bad = true;
            if (idx.b && !(-n <= *idx.b && *idx.b <= n)) bad = true;
            if (!bad) {
                long long ea = idx.a ? *idx.a : 0;
                long long eb = idx.b ? *idx.b : n;
                if (ea < 0) ea += n;
                if (eb < 0) eb += n;
                if (ea >= eb) bad = true;
            }
            if (bad) {
                problems.push_back(RuleCatalog::make_problem("SEDBase-0011", ctx.location,
                    {{"attr", ctx.attr}, {"value", ctx.value}, {"subvalue", range_text(idx.a, idx.b)}, {"min", std::to_string(-n)}, {"max", std::to_string(n - 1)}, {"class", ctx.class_name}, {"id", ctx.id_value}}));
            }
        }
    }
    return problems;
}

}  // namespace sedbase_0011
}  // namespace rules
}  // namespace sed2test

// SEDBase-0016 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0016.md):
// "A reference required to resolve to a model must resolve to a model."
//
// Applies to every field whose schema property carries "x-ref-target": "model"
// (FieldSpec::ref_target). resolved_kind is "model", "annotatedData", "object", or
// nullopt when what the reference resolves to is not statically known (silent
// then). Only model is acceptable.
//
// Hand-written template (templates/cpp/rules/SEDBase-0016.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "libsed2" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0016.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace libsed2 {
namespace rules {
namespace sedbase_0016 {

inline std::vector<ValidationProblem> check(const std::optional<std::string>& resolved_kind,
                                            const std::string& resolved_description, const RuleCtx& ctx) {
    if (!resolved_kind || *resolved_kind == "model") return {};
    return {RuleCatalog::make_problem("SEDBase-0016", ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"resolved-value", resolved_description}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace sedbase_0016
}  // namespace rules
}  // namespace libsed2

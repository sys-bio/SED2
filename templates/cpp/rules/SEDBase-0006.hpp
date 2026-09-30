// SEDBase-0006 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0006.md):
// "Every colon-delimited segment of a reference must resolve to an existing
// element."
//
// resolved_prefix is nullopt only when there was no document to walk at all - not
// a genuine resolution failure, so this rule stays silent. Otherwise `resolved`
// says whether resolution succeeded and resolved_prefix is the longest prefix
// that DID resolve (the message's {subvalue}).
//
// Hand-written template (templates/cpp/rules/SEDBase-0006.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDBase-0006.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include "../Reference.hpp"

namespace sed2test {
namespace rules {
namespace sedbase_0006 {

inline std::vector<ValidationProblem> check(const ParsedReference& parsed, bool resolved,
                                            const std::optional<std::string>& resolved_prefix, const RuleCtx& ctx) {
    if (!resolved_prefix || resolved) return {};
    return {RuleCatalog::make_problem("SEDBase-0006", ctx.location,
        {{"attr", ctx.attr}, {"value", parsed.raw}, {"subvalue", *resolved_prefix}, {"class", ctx.class_name}, {"id", ctx.id_value}})};
}

}  // namespace sedbase_0006
}  // namespace rules
}  // namespace sed2test

// SEDDocument-0009 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0009.md):
// "For every namespace prefix used anywhere in the document, SEDDocument must
// declare a <prefix>@version attribute."
//
// Called once per usage site of an undeclared-version namespace prefix; `location`
// is that usage's own JSON pointer, not the (missing) declaration's.
//
// Hand-written template (templates/cpp/rules/SEDDocument-0009.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "sed2test" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDDocument-0009.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace sed2test {
namespace rules {
namespace seddocument_0009 {

inline std::vector<ValidationProblem> check(const std::string& prefix, const std::string& location) {
    return {RuleCatalog::make_problem("SEDDocument-0009", location, {{"prefix", prefix}})};
}

}  // namespace seddocument_0009
}  // namespace rules
}  // namespace sed2test

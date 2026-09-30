// SEDDocument-0010 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0010.md):
// "A <prefix>@version attribute should not be declared for a namespace the
// document never uses." A warning, not an error.
//
// Called once per declared-but-unused prefix; `location` is the declaration's own
// JSON pointer ("/<prefix>@version").
//
// Hand-written template (templates/cpp/rules/SEDDocument-0010.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "libsed2" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDDocument-0010.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"

namespace libsed2 {
namespace rules {
namespace seddocument_0010 {

inline std::vector<ValidationProblem> check(const std::string& prefix, const std::string& location) {
    return {RuleCatalog::make_problem("SEDDocument-0010", location,
        {{"prefix", prefix}, {"attr", prefix + "@version"}})};
}

}  // namespace seddocument_0010
}  // namespace rules
}  // namespace libsed2

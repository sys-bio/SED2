// SEDDocument-0011 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0011.md):
// "The version of a SEDDocument should not be newer than the newest document
// version this library knows."
//
// max_known is the class-level constant the generator bakes in (the newest version
// directory this run's specsheets/ tree had for the document class); version is
// the document's own stored `version` value (nullptr when unset). A missing or
// malformed (not v#.#.#) version is reported by SEDDocument's own required-field
// and pattern rules - this rule only compares two well-formed versions.
//
// Hand-written template (templates/cpp/rules/SEDDocument-0011.hpp), one small file per
// rule with a fixed check() function name in namespace rules::<id> - copied
// verbatim into the generated include tree by generator/emit_cpp.py except
// that the literal namespace name "libsed2" is rewritten to --cpp-namespace.
// Mirrors templates/python/rules/SEDDocument-0011.py (the reference implementation).
// ASCII only.
#pragma once

#include "../Runtime.hpp"
#include <regex>

namespace libsed2 {
namespace rules {
namespace seddocument_0011 {

inline bool version_tuple(const Json& value, long long out[3]) {
    if (!value.is_string()) return false;
    static const std::regex re("^v([0-9]+)\\.([0-9]+)\\.([0-9]+)$");
    std::string s = value.as<std::string>();
    std::smatch m;
    if (!std::regex_match(s, m, re)) return false;
    for (int i = 0; i < 3; i++) {
        try { out[i] = std::stoll(m[i + 1].str()); } catch (...) { return false; }
    }
    return true;
}

inline std::vector<ValidationProblem> check(const std::optional<std::string>& max_known, const Json* version) {
    if (!max_known || !version) return {};
    long long vt[3], mt[3];
    if (!version_tuple(*version, vt) || !version_tuple(Json(*max_known), mt)) return {};
    bool newer = false;
    for (int i = 0; i < 3; i++) {
        if (vt[i] != mt[i]) { newer = vt[i] > mt[i]; break; }
    }
    if (!newer) return {};
    return {RuleCatalog::make_problem("SEDDocument-0011", "/version",
        {{"value", pyfmt::str(*version)}, {"max", *max_known}})};
}

}  // namespace seddocument_0011
}  // namespace rules
}  // namespace libsed2

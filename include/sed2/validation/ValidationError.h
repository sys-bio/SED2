#pragma once

#include <string>

namespace sed2 {

// Ordered least to most severe, matching the numeric levels
// spec/numbered-validation-rules.md refers to them by (0-3): a finding the
// validator can't act on but wants the caller to see (Info, e.g. "no
// document was available to check this reference against"), a plausible
// but unconfirmed problem (Warning), a confirmed problem (Error), and a
// JSON Schema violation specifically (SchemaViolation - kept distinct from
// a plain Error so a caller can tell "the document is structurally
// invalid" apart from "a cross-reference didn't resolve").
enum class ValidationSeverity {
    Info,
    Warning,
    Error,
    SchemaViolation,
};

// One validation problem found in a SED2 document. 'code' refers to an
// entry in spec/numbered-validation-rules.md for anything that isn't a
// plain JSON Schema violation (those carry the schema's own message and an
// empty code).
struct ValidationError {
    std::string code;
    std::string message;
    std::string path;
    ValidationSeverity severity = ValidationSeverity::Error;

    ValidationError() = default;
    ValidationError(std::string code_, std::string message_, std::string path_,
                     ValidationSeverity severity_ = ValidationSeverity::Error)
        : code(std::move(code_)),
          message(std::move(message_)),
          path(std::move(path_)),
          severity(severity_) {}
};

}  // namespace sed2

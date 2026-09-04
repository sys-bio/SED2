#pragma once

#include <memory>
#include <string>
#include <vector>

#include "sed2/core/Json.h"
#include "sed2/validation/ValidationError.h"

namespace sed2 {

// Wraps pboettch/json-schema-validator against spec/sed2.schema.json for
// the general structural validation pass (Design.md, "Validation":
// "General validation can be performed by a JSON schema"). This
// complements, rather than replaces, each class's own validate(): the
// schema catches shape violations before this library's C++ classes even
// get involved (a completely malformed document, an attribute of the
// wrong JSON type, an unknown enum value); validate() catches everything
// spec-specific a schema can't express (reference resolution, for
// instance). Uses the pimpl idiom so callers don't need
// nlohmann/json-schema.hpp just to hold a SchemaValidator.
class SchemaValidator {
public:
    // Loads the schema from 'schemaPath' (by default, the copy of
    // spec/sed2.schema.json this library was built with - see
    // SED2_SCHEMA_PATH in CMakeLists.txt). Throws std::runtime_error if
    // the file can't be read, or isn't a valid JSON Schema document.
    explicit SchemaValidator(const std::string& schemaPath = defaultSchemaPath());

    // Validates 'document' against the schema, appending one
    // ValidationError per violation found - all of them, not just the
    // first (Design.md: "All validation errors are collected and
    // presented to the user as a list").
    void validate(const Json& document, std::vector<ValidationError>& errors) const;

    static std::string defaultSchemaPath();

private:
    struct Impl;
    std::shared_ptr<Impl> impl_;
};

}  // namespace sed2

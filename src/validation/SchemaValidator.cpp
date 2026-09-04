#include "sed2/validation/SchemaValidator.h"

#include <fstream>
#include <stdexcept>

#include <nlohmann/json-schema.hpp>

namespace sed2 {

namespace {

// Collects every violation nlohmann::json_schema::json_validator finds,
// instead of the library's default of throwing on the first one.
class CollectingErrorHandler : public nlohmann::json_schema::error_handler {
public:
    explicit CollectingErrorHandler(std::vector<ValidationError>& errors) : errors_(errors) {}

    void error(const nlohmann::json::json_pointer& pointer, const nlohmann::json& instance,
               const std::string& message) override {
        (void)instance;
        errors_.emplace_back("", message, pointer.to_string(), ValidationSeverity::SchemaViolation);
    }

private:
    std::vector<ValidationError>& errors_;
};

nlohmann::json loadSchemaFile(const std::string& schemaPath) {
    std::ifstream in(schemaPath);
    if (!in) throw std::runtime_error("sed2: could not open schema file: " + schemaPath);
    nlohmann::json schema;
    in >> schema;
    return schema;
}

}  // namespace

struct SchemaValidator::Impl {
    nlohmann::json_schema::json_validator validator;
};

std::string SchemaValidator::defaultSchemaPath() {
#ifdef SED2_SCHEMA_PATH
    return SED2_SCHEMA_PATH;
#else
    return "spec/sed2.schema.json";
#endif
}

SchemaValidator::SchemaValidator(const std::string& schemaPath) : impl_(std::make_shared<Impl>()) {
    impl_->validator.set_root_schema(loadSchemaFile(schemaPath));
}

void SchemaValidator::validate(const Json& document, std::vector<ValidationError>& errors) const {
    // json-schema-validator validates nlohmann::json specifically; sed2::Json
    // (ordered_json) converts to it losslessly - only key-iteration order
    // changes, which schema validation doesn't depend on.
    nlohmann::json plain = document;
    CollectingErrorHandler handler(errors);
    impl_->validator.validate(plain, handler);
}

}  // namespace sed2

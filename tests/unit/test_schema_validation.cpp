#include <gtest/gtest.h>

#include <fstream>
#include <sstream>

#include "sed2/validation/SchemaValidator.h"

namespace {
sed2::Json loadJsonFile(const std::string& path) {
    std::ifstream in(path);
    std::ostringstream buffer;
    buffer << in.rdbuf();
    return sed2::Json::parse(buffer.str());
}
}  // namespace

TEST(SchemaValidator, AcceptsValidDocument) {
    sed2::SchemaValidator validator;
    sed2::Json doc = loadJsonFile(std::string(SED2_TEST_VALID_DOCS_DIR) + "/explicit_ode_simulation.json");

    std::vector<sed2::ValidationError> errors;
    validator.validate(doc, errors);
    for (const auto& e : errors) ADD_FAILURE() << e.path << ": " << e.message;
    EXPECT_TRUE(errors.empty());
}

TEST(SchemaValidator, RejectsMissingRequiredVersionNum) {
    sed2::SchemaValidator validator;
    sed2::Json doc = loadJsonFile(std::string(SED2_TEST_INVALID_DOCS_DIR) + "/missing_version_num.json");

    std::vector<sed2::ValidationError> errors;
    validator.validate(doc, errors);
    EXPECT_FALSE(errors.empty());
}

TEST(SchemaValidator, RejectsUnknownTaskType) {
    sed2::SchemaValidator validator;
    sed2::Json doc = loadJsonFile(std::string(SED2_TEST_INVALID_DOCS_DIR) + "/unknown_task_type.json");

    std::vector<sed2::ValidationError> errors;
    validator.validate(doc, errors);
    EXPECT_FALSE(errors.empty());
}

TEST(SchemaValidator, RejectsExplicitODESimulationMissingModel) {
    sed2::SchemaValidator validator;
    sed2::Json doc = loadJsonFile(std::string(SED2_TEST_INVALID_DOCS_DIR) + "/missing_required_model.json");

    std::vector<sed2::ValidationError> errors;
    validator.validate(doc, errors);
    EXPECT_FALSE(errors.empty());
}

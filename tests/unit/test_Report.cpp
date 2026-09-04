#include <gtest/gtest.h>

#include <memory>

#include "sed2/core/SEDDocument.h"
#include "sed2/generated/ModelImport.h"
#include "sed2/generated/Report.h"

using sed2::ModelImport;
using sed2::Report;
using sed2::SEDDocument;

// TypeName, DataGetSetIsSetUnset, and a plain fromJSON/toJSON round trip
// are now covered generically by ReportGenerated.* (see
// codegen/generate_classes.py's generated tests, in the
// sed2_generated_tests target). What's left here is what the generator
// can't produce: reference resolution against a real SEDDocument, and the
// exact wording of the "no document" Info message.
TEST(Report, ValidateRequiresData) {
    Report report;
    std::vector<sed2::ValidationError> errors;
    report.validate(errors);
    EXPECT_EQ(errors.size(), 1u);

    // With data set but no owning SEDDocument, validate() can't tell
    // whether "#tasks:sim1" resolves - it says so (Info), rather than
    // reporting no problem at all (see AttributeTypes::validateReference).
    errors.clear();
    report.setData("#tasks:sim1");
    report.validate(errors);
    ASSERT_EQ(errors.size(), 1u);
    EXPECT_EQ(errors[0].severity, sed2::ValidationSeverity::Info);
    EXPECT_EQ(errors[0].message,
              "Unable to tell whether the referenced '#tasks:sim1' exists, as no document was provided.");
}

TEST(Report, ValidateWithDocumentResolvesReference) {
    SEDDocument doc;
    auto task = std::make_unique<ModelImport>();
    task->setId("sim1");
    task->setLocation("model.xml");
    task->setLanguage("urn:sedml:language:sbml");
    doc.addTask(std::move(task));

    // A ModelImport task's own bare reference isn't meaningful - only its
    // "model" dot accessor is (see ModelImport's "bareReferenceValid":
    // false table entry) - so a Report pointing at one for real data has
    // to spell that out.
    auto report = std::make_unique<Report>();
    report->setData("#tasks:sim1.model");
    Report* reportPtr = report.get();
    doc.addOutput(std::move(report));

    std::vector<sed2::ValidationError> errors;
    reportPtr->validate(errors);
    EXPECT_TRUE(errors.empty());
}

TEST(Report, ValidateWithDocumentReportsErrorForUnresolvedReference) {
    SEDDocument doc;
    auto report = std::make_unique<Report>();
    report->setData("#tasks:doesNotExist");
    Report* reportPtr = report.get();
    doc.addOutput(std::move(report));

    std::vector<sed2::ValidationError> errors;
    reportPtr->validate(errors);
    ASSERT_EQ(errors.size(), 1u);
    EXPECT_EQ(errors[0].severity, sed2::ValidationSeverity::Error);
}

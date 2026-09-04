#include <gtest/gtest.h>

#include <memory>

#include "sed2/core/AttributeTypes.h"
#include "sed2/core/SEDDocument.h"
#include "sed2/generated/ExplicitODESimulation.h"
#include "sed2/generated/Loop.h"
#include "sed2/generated/ModelImport.h"
#include "sed2/generated/Report.h"

using sed2::ExplicitODESimulation;
using sed2::hasSubvalue;
using sed2::isReference;
using sed2::Loop;
using sed2::ModelImport;
using sed2::parseReferencePath;
using sed2::Report;
using sed2::ReferencePathSegment;
using sed2::scanReferenceLength;
using sed2::SEDDocument;
using sed2::validateReference;
using sed2::ValidationError;
using sed2::ValidationSeverity;

namespace {
// A minimal SEDBase subclass that declares one dot-accessor, so
// validateReference's Warning branch can be exercised directly alongside
// the generated classes that now declare real ones too (ModelImport,
// below - see SEDBase::getDeclaredDotAccessors, V0002).
class ElementWithDotAccessor : public sed2::SEDBase {
public:
    std::string getTypeName() const override { return "elementWithDotAccessor"; }
    std::vector<std::string> getDeclaredDotAccessors() const override { return {"model"}; }
};
}  // namespace

TEST(AttributeTypes, IsReference) {
    EXPECT_TRUE(isReference("#tasks:sim1"));
    EXPECT_FALSE(isReference("tasks:sim1"));
    EXPECT_FALSE(isReference(""));
}

TEST(AttributeTypes, ParseReferencePathFullChain) {
    auto segments = parseReferencePath("#tasks:sim1.model['S1']");
    ASSERT_TRUE(segments.has_value());
    ASSERT_EQ(segments->size(), 4u);
    EXPECT_EQ((*segments)[0].kind, ReferencePathSegment::Kind::Colon);
    EXPECT_EQ((*segments)[0].name, "tasks");
    EXPECT_EQ((*segments)[1].kind, ReferencePathSegment::Kind::Colon);
    EXPECT_EQ((*segments)[1].name, "sim1");
    EXPECT_EQ((*segments)[2].kind, ReferencePathSegment::Kind::Dot);
    EXPECT_EQ((*segments)[2].name, "model");
    EXPECT_EQ((*segments)[3].kind, ReferencePathSegment::Kind::IndexString);
    EXPECT_EQ((*segments)[3].stringValue, "S1");
}

TEST(AttributeTypes, ParseReferencePathIntegerAndSliceIndices) {
    auto intIndex = parseReferencePath("#x[3]");
    ASSERT_TRUE(intIndex.has_value());
    ASSERT_EQ(intIndex->size(), 2u);
    EXPECT_EQ((*intIndex)[1].kind, ReferencePathSegment::Kind::IndexInt);
    EXPECT_EQ((*intIndex)[1].intValue, 3);

    auto slice = parseReferencePath("#x[0:5]");
    ASSERT_TRUE(slice.has_value());
    EXPECT_EQ((*slice)[1].kind, ReferencePathSegment::Kind::IndexSlice);
    EXPECT_EQ((*slice)[1].intValue, 0);
    EXPECT_EQ((*slice)[1].intValue2, 5);
}

TEST(AttributeTypes, ParseReferencePathRejectsMalformed) {
    EXPECT_FALSE(parseReferencePath("#").has_value());
    EXPECT_FALSE(parseReferencePath("#x[").has_value());
    EXPECT_FALSE(parseReferencePath("#x['unterminated").has_value());
    EXPECT_FALSE(parseReferencePath("not-a-reference").has_value());
}

TEST(AttributeTypes, ScanReferenceLengthStopsAtEmbeddingContext) {
    std::string text = "#tasks:sim1.value + 1";
    auto length = scanReferenceLength(text, 0);
    ASSERT_TRUE(length.has_value());
    EXPECT_EQ(text.substr(0, *length), "#tasks:sim1.value");
}

TEST(AttributeTypes, HasSubvalueDotAccessor) {
    std::vector<std::string> declared = {"model", "outputVariables"};
    EXPECT_TRUE(hasSubvalue(declared, ".model"));
    EXPECT_FALSE(hasSubvalue(declared, ".notDeclared"));
}

TEST(AttributeTypes, HasSubvalueBracketAccessorIsAlwaysSyntacticallyPlausible) {
    std::vector<std::string> declared;  // no dot-accessors declared
    EXPECT_TRUE(hasSubvalue(declared, "['S1']"));
    EXPECT_TRUE(hasSubvalue(declared, "[3]"));
    EXPECT_TRUE(hasSubvalue(declared, "[0:5]"));
    EXPECT_FALSE(hasSubvalue(declared, "[unterminated"));
}

TEST(SEDDocumentCrossReferences, GetSEDReferenceResolvesColonPath) {
    std::string error;
    SEDDocument doc =
        SEDDocument::fromFile(std::string(SED2_TEST_VALID_DOCS_DIR) + "/explicit_ode_simulation.json", &error);
    ASSERT_TRUE(error.empty()) << error;

    EXPECT_EQ(doc.getSEDReference("#tasks:sim1"), doc.getTask("sim1"));
    EXPECT_EQ(doc.getSEDReference("#outputs:sim1_out"), doc.getOutput("sim1_out"));

    // Trailing subvalue accessors are not resolved further: the anchor
    // object the colon path names is still what's returned.
    EXPECT_EQ(doc.getSEDReference("#tasks:sim1.model['S1']"), doc.getTask("sim1"));

    EXPECT_EQ(doc.getSEDReference("#tasks:doesNotExist"), nullptr);
    EXPECT_EQ(doc.getSEDReference("not-a-reference"), nullptr);
}

TEST(SEDDocumentCrossReferences, GetSEDDocumentWalksMultipleParentLevels) {
    SEDDocument doc;
    auto loop = std::make_unique<Loop>();
    Loop* loopPtr = loop.get();
    doc.addTask(std::move(loop));

    auto subTask = std::make_unique<ModelImport>();
    ModelImport* subTaskPtr = subTask.get();
    loopPtr->addSubTask(std::move(subTask));

    EXPECT_EQ(loopPtr->getSEDDocument(), &doc);
    EXPECT_EQ(subTaskPtr->getSEDDocument(), &doc);

    ModelImport orphan;
    EXPECT_EQ(orphan.getSEDDocument(), nullptr);
}

TEST(AttributeTypes, ValidateReferenceNoOpForNonReferenceValue) {
    Report owner;
    std::vector<ValidationError> errors;
    validateReference(owner, "data", "not-a-reference", errors);
    EXPECT_TRUE(errors.empty());
}

TEST(AttributeTypes, ValidateReferenceInfoWithoutDocument) {
    Report owner;
    std::vector<ValidationError> errors;
    validateReference(owner, "data", "#tasks:sim1", errors);
    ASSERT_EQ(errors.size(), 1u);
    EXPECT_EQ(errors[0].severity, ValidationSeverity::Info);
}

TEST(AttributeTypes, ValidateReferenceErrorWhenDocumentButUnresolved) {
    SEDDocument doc;
    auto report = std::make_unique<Report>();
    Report* reportPtr = report.get();
    doc.addOutput(std::move(report));

    std::vector<ValidationError> errors;
    validateReference(*reportPtr, "data", "#tasks:doesNotExist", errors);
    ASSERT_EQ(errors.size(), 1u);
    EXPECT_EQ(errors[0].severity, ValidationSeverity::Error);
}

TEST(AttributeTypes, ValidateReferenceWarningForImplausibleDotAccessor) {
    SEDDocument doc;
    auto element = std::make_unique<ElementWithDotAccessor>();
    element->setId("sim1");
    ElementWithDotAccessor* elementPtr = element.get();
    doc.addTask(std::move(element));

    std::vector<ValidationError> errors;
    validateReference(*elementPtr, "someField", "#tasks:sim1.notDeclared", errors);
    ASSERT_EQ(errors.size(), 1u);
    EXPECT_EQ(errors[0].severity, ValidationSeverity::Warning);
}

// ModelImport is one of the generated classes that now actually declares
// its dot-accessors ("model") and its bare-reference-invalidity (only
// "#tasks:id.model" is meaningful, not "#tasks:id" alone) - see
// ModelImport.json's "dotAccessors"/"bareReferenceValid" table entries.
// These exercise the Warning path end to end through real generated code,
// not just the test-only ElementWithDotAccessor above.
TEST(AttributeTypes, ValidateReferenceAcceptsModelImportDeclaredDotAccessor) {
    SEDDocument doc;
    auto task = std::make_unique<ModelImport>();
    task->setId("model1");
    task->setLocation("model.xml");
    task->setLanguage("urn:sedml:language:sbml");
    ModelImport* taskPtr = task.get();
    doc.addTask(std::move(task));

    std::vector<ValidationError> errors;
    validateReference(*taskPtr, "someField", "#tasks:model1.model", errors);
    EXPECT_TRUE(errors.empty());
}

TEST(AttributeTypes, ValidateReferenceWarnsOnModelImportUndeclaredDotAccessor) {
    SEDDocument doc;
    auto task = std::make_unique<ModelImport>();
    task->setId("model1");
    task->setLocation("model.xml");
    task->setLanguage("urn:sedml:language:sbml");
    ModelImport* taskPtr = task.get();
    doc.addTask(std::move(task));

    std::vector<ValidationError> errors;
    validateReference(*taskPtr, "someField", "#tasks:model1.notDeclared", errors);
    ASSERT_EQ(errors.size(), 1u);
    EXPECT_EQ(errors[0].severity, ValidationSeverity::Warning);
}

TEST(AttributeTypes, ValidateReferenceWarnsOnModelImportBareReference) {
    SEDDocument doc;
    auto task = std::make_unique<ModelImport>();
    task->setId("model1");
    task->setLocation("model.xml");
    task->setLanguage("urn:sedml:language:sbml");
    ModelImport* taskPtr = task.get();
    doc.addTask(std::move(task));

    // "#tasks:model1" with no trailing ".model" refers to the whole
    // ModelImport, which - per the spec - has no meaningful value of its
    // own (see ModelImport's "bareReferenceValid": false table entry).
    std::vector<ValidationError> errors;
    validateReference(*taskPtr, "someField", "#tasks:model1", errors);
    ASSERT_EQ(errors.size(), 1u);
    EXPECT_EQ(errors[0].severity, ValidationSeverity::Warning);
}

TEST(AttributeTypes, ValidateReferenceAcceptsBareReferenceWhenClassAllowsIt) {
    // Unlike ModelImport, ExplicitODESimulation doesn't set
    // "bareReferenceValid": false - "#tasks:sim1" alone is meaningful (the
    // simulation's own result), so no warning is expected.
    SEDDocument doc;
    auto task = std::make_unique<ExplicitODESimulation>();
    task->setId("sim1");
    ExplicitODESimulation* taskPtr = task.get();
    doc.addTask(std::move(task));

    std::vector<ValidationError> errors;
    validateReference(*taskPtr, "someField", "#tasks:sim1", errors);
    EXPECT_TRUE(errors.empty());
}

// Regression test for a latent bug fixed alongside the dot-accessor
// rollout: SEDDocument::getSEDReference only resolves the first two colon
// segments (root type + id) of a reference, so a deeper colon path (e.g. a
// Loop's subTasks, "#tasks:repeat:subTasks:sim1") has colon segments past
// index 2 that are still part of the "bare" colon path, not a dot/bracket
// accessor. Before the fix, validateReference's accessor-plausibility loop
// treated each of those extra colon segments as its own (empty, always-
// implausible) accessor and warned once per segment; now they're skipped.
TEST(AttributeTypes, ValidateReferenceDoesNotWarnOnDeepColonPathSegments) {
    SEDDocument doc;
    auto loop = std::make_unique<Loop>();
    loop->setId("repeat");
    doc.addTask(std::move(loop));

    std::vector<ValidationError> errors;
    validateReference(*doc.getTask("repeat"), "someField", "#tasks:repeat:subTasks:sim1", errors);
    // Only the first two colon segments ("tasks", "repeat") resolve today;
    // everything past that is still colon-shaped, so there's no trailing
    // accessor to warn about, and Loop doesn't set "bareReferenceValid":
    // false, so this should be silent - not one warning per extra segment.
    EXPECT_TRUE(errors.empty());
}

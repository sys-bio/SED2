#include <gtest/gtest.h>

#include <string>
#include <utility>

#include "sed2/core/SEDDocument.h"
#include "sed2/generated/ExplicitODESimulation.h"
#include "sed2/generated/ModelImport.h"
#include "sed2/generated/Report.h"

using sed2::SEDDocument;

namespace {
std::string validDocPath(const std::string& name) { return std::string(SED2_TEST_VALID_DOCS_DIR) + "/" + name; }
}  // namespace

TEST(SEDDocument, LoadsFromFile) {
    std::string error;
    SEDDocument doc = SEDDocument::fromFile(validDocPath("explicit_ode_simulation.json"), &error);
    EXPECT_TRUE(error.empty()) << error;
    EXPECT_EQ(doc.getVersionStr(), "SED v2.0 alpha");
    EXPECT_EQ(doc.getVersionNum(), 2.0);
    EXPECT_EQ(doc.getNumTasks(), 2u);
    EXPECT_EQ(doc.getNumOutputs(), 1u);
}

TEST(SEDDocument, TasksAreDispatchedByType) {
    std::string error;
    SEDDocument doc = SEDDocument::fromFile(validDocPath("explicit_ode_simulation.json"), &error);
    ASSERT_TRUE(error.empty()) << error;

    auto* model1 = doc.getTask("model1");
    ASSERT_NE(model1, nullptr);
    auto* modelImport = dynamic_cast<sed2::ModelImport*>(model1);
    ASSERT_NE(modelImport, nullptr);
    EXPECT_EQ(model1->getTypeName(), "modelImport");
    EXPECT_EQ(modelImport->getLocation(), "three_species_chain.xml");

    auto* sim1 = doc.getTask("sim1");
    ASSERT_NE(sim1, nullptr);
    auto* explicitSim = dynamic_cast<sed2::ExplicitODESimulation*>(sim1);
    ASSERT_NE(explicitSim, nullptr);
    EXPECT_EQ(explicitSim->getKisaoID(), "KISAO:0000694");

    auto* out = doc.getOutput("sim1_out");
    ASSERT_NE(out, nullptr);
    auto* report = dynamic_cast<sed2::Report*>(out);
    ASSERT_NE(report, nullptr);
    EXPECT_EQ(report->getData(), "#tasks:sim1");
}

TEST(SEDDocument, RoundTripPreservesModelImportFields) {
    std::string error;
    SEDDocument doc = SEDDocument::fromFile(validDocPath("explicit_ode_simulation.json"), &error);
    ASSERT_TRUE(error.empty()) << error;

    sed2::Json roundTripped = doc.toJSON();
    ASSERT_TRUE(roundTripped.at("tasks").contains("model1"));
    EXPECT_EQ(roundTripped.at("tasks").at("model1").at("location").get<std::string>(),
              "three_species_chain.xml");
}

TEST(SEDDocument, ValidateOnCompleteDocumentReportsNoErrors) {
    std::string error;
    SEDDocument doc = SEDDocument::fromFile(validDocPath("explicit_ode_simulation.json"), &error);
    ASSERT_TRUE(error.empty()) << error;

    std::vector<sed2::ValidationError> errors;
    doc.validate(errors);
    for (const auto& e : errors) ADD_FAILURE() << e.path << ": " << e.message;
    EXPECT_TRUE(errors.empty());
}

TEST(SEDDocument, ValidateOnFullCatalogDocumentReportsNoErrors) {
    // Exercises cross-references between several of the classes generated
    // in this pass (ModelImport, SteadyState, ParameterScan + subTasks +
    // parameterRanges, Report, Plot2D + curves) inside one real document,
    // rather than each in isolation - see tests/valid_documents/
    // full_catalog.json.
    std::string error;
    SEDDocument doc = SEDDocument::fromFile(validDocPath("full_catalog.json"), &error);
    ASSERT_TRUE(error.empty()) << error;

    std::vector<sed2::ValidationError> errors;
    doc.validate(errors);
    for (const auto& e : errors) ADD_FAILURE() << e.path << ": " << e.message;
    EXPECT_TRUE(errors.empty());
}

// SEDDocument::fromFile/fromJSONString return by value from a named local
// ("return document;"), which only avoids an actual move when the compiler
// applies NRVO - an optional optimization some compilers (notably MSVC
// Debug) skip more often than others. These tests force a real move
// explicitly (std::move on a distinct, already-existing lvalue is never
// elided, on any compiler) so the fix - reconnectOwnedChildren() re-homing
// each child's SEDBase::parent_ after the move - has actual coverage here,
// rather than depending on whether this build's compiler happens to elide
// the copy inside fromFile/fromJSONString.
TEST(SEDDocument, SurvivesExplicitMoveConstruction) {
    SEDDocument original;
    original.setVersionStr("SED v2.0 alpha");
    original.setVersionNum(2.0);
    auto task = std::make_unique<sed2::ModelImport>();
    task->setId("model1");
    task->setLocation("model.xml");
    task->setLanguage("urn:sedml:language:sbml");
    original.addTask(std::move(task));

    SEDDocument moved(std::move(original));

    auto* movedTask = moved.getTask("model1");
    ASSERT_NE(movedTask, nullptr);
    EXPECT_EQ(movedTask->getSEDDocument(), &moved);

    std::vector<sed2::ValidationError> errors;
    moved.validate(errors);
    for (const auto& e : errors) ADD_FAILURE() << e.path << ": " << e.message;
}

TEST(SEDDocument, SurvivesExplicitMoveAssignment) {
    SEDDocument original;
    auto task = std::make_unique<sed2::ModelImport>();
    task->setId("model1");
    task->setLocation("model.xml");
    task->setLanguage("urn:sedml:language:sbml");
    original.addTask(std::move(task));

    SEDDocument moved;
    moved = std::move(original);

    auto* movedTask = moved.getTask("model1");
    ASSERT_NE(movedTask, nullptr);
    EXPECT_EQ(movedTask->getSEDDocument(), &moved);
}

TEST(SEDDocument, FromFileReportsErrorForMissingFile) {
    std::string error;
    SEDDocument doc = SEDDocument::fromFile("/no/such/file.json", &error);
    EXPECT_FALSE(error.empty());
    EXPECT_FALSE(doc.isSetVersionStr());
}

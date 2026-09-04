#include <gtest/gtest.h>

#include "sed2/generated/BoundedODESimulation.h"
#include "sed2/generated/BoundedStochasticSimulation.h"
#include "sed2/generated/ExplicitStochasticSimulation.h"
#include "sed2/generated/FluxBalanceAnalysis.h"
#include "sed2/generated/Jacobian.h"
#include "sed2/generated/NumericRange.h"
#include "sed2/generated/OneStepODE.h"
#include "sed2/generated/OneStepStochastic.h"
#include "sed2/generated/SteadyState.h"

using sed2::BoundedODESimulation;
using sed2::BoundedStochasticSimulation;
using sed2::ExplicitStochasticSimulation;
using sed2::FluxBalanceAnalysis;
using sed2::Jacobian;
using sed2::OneStepODE;
using sed2::OneStepStochastic;
using sed2::SteadyState;

namespace {
// A standalone object's references can never resolve (no owning
// SEDDocument), so validate() reports each as Info rather than silence -
// see AttributeTypes::validateReference. Callers just want to know no
// Warning/Error/SchemaViolation slipped in.
void expectOnlyInfoSeverity(const std::vector<sed2::ValidationError>& errors) {
    for (const auto& error : errors) {
        EXPECT_EQ(error.severity, sed2::ValidationSeverity::Info) << error.message;
    }
}
}  // namespace

TEST(BoundedODESimulation, ValidateReportsMissingRequiredAttributes) {
    BoundedODESimulation sim;
    std::vector<sed2::ValidationError> errors;
    sim.validate(errors);
    // kisaoID, model, independentVariable, outputVariables,
    // independentVariableSpan are all required.
    EXPECT_GE(errors.size(), 5u);
}

TEST(BoundedODESimulation, FromJsonToJsonRoundTrip) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "boundedODESimulation",
        "kisaoID": "KISAO:0000019",
        "model": "#tasks:model1.model",
        "independentVariable": "urn:sedml:symbol:time",
        "outputVariables": ["S1"],
        "independentVariableSpan": {"_type": "span", "start": 0, "end": 10}
    })");
    BoundedODESimulation sim;
    sim.fromJSON(json);
    EXPECT_EQ(sim.getModel(), "#tasks:model1.model");
    ASSERT_NE(sim.getIndependentVariableSpan(), nullptr);
    EXPECT_EQ(sim.toJSON(), json);

    std::vector<sed2::ValidationError> errors;
    sim.validate(errors);
    expectOnlyInfoSeverity(errors);
}

TEST(BoundedStochasticSimulation, FromJsonToJsonRoundTrip) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "boundedStochasticSimulation",
        "kisaoID": "KISAO:0000241",
        "model": "#tasks:model1.model",
        "independentVariable": "urn:sedml:symbol:time",
        "outputVariables": ["S1"],
        "independentVariableSpan": {"_type": "span", "start": 0, "end": 10}
    })");
    BoundedStochasticSimulation sim;
    sim.fromJSON(json);
    EXPECT_EQ(sim.toJSON(), json);

    std::vector<sed2::ValidationError> errors;
    sim.validate(errors);
    expectOnlyInfoSeverity(errors);
}

TEST(ExplicitStochasticSimulation, FromJsonToJsonRoundTrip) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "explicitStochasticSimulation",
        "kisaoID": "KISAO:0000029",
        "model": "#tasks:model1.model",
        "independentVariable": "urn:sedml:symbol:time",
        "outputVariables": ["S1"],
        "independentVariableRange": {"_type": "numericRange", "start": 0, "end": 10, "numberOfSteps": 5}
    })");
    ExplicitStochasticSimulation sim;
    sim.fromJSON(json);
    EXPECT_EQ(sim.toJSON(), json);

    std::vector<sed2::ValidationError> errors;
    sim.validate(errors);
    expectOnlyInfoSeverity(errors);
}

TEST(OneStepODE, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "oneStepODE",
        "kisaoID": "KISAO:0000019",
        "model": "#tasks:model1.model",
        "independentVariable": "urn:sedml:symbol:time",
        "outputVariables": ["S1"],
        "independentStep": 0.1
    })");
    OneStepODE sim;
    sim.fromJSON(json);
    EXPECT_EQ(sim.getIndependentStep().value, 0.1);
    EXPECT_EQ(sim.toJSON(), json);

    OneStepODE empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // kisaoID, model, independentVariable, outputVariables, independentStep.
    EXPECT_GE(errors.size(), 5u);
}

TEST(OneStepStochastic, FromJsonToJsonRoundTrip) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "oneStepStochastic",
        "kisaoID": "KISAO:0000241",
        "model": "#tasks:model1.model",
        "independentVariable": "urn:sedml:symbol:time",
        "outputVariables": ["S1"]
    })");
    OneStepStochastic sim;
    sim.fromJSON(json);
    EXPECT_EQ(sim.toJSON(), json);
}

TEST(SteadyState, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "steadyState",
        "kisaoID": "KISAO:0000407",
        "model": "#tasks:model1.model",
        "outputVariables": ["S1"]
    })");
    SteadyState sim;
    sim.fromJSON(json);
    EXPECT_EQ(sim.toJSON(), json);

    SteadyState empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // kisaoID, model, outputVariables.
    EXPECT_GE(errors.size(), 3u);
}

TEST(FluxBalanceAnalysis, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "fluxBalanceAnalysis",
        "kisaoID": "KISAO:0000527",
        "model": "#tasks:model1.model",
        "outputVariables": ["R1"]
    })");
    FluxBalanceAnalysis sim;
    sim.fromJSON(json);
    EXPECT_EQ(sim.toJSON(), json);

    FluxBalanceAnalysis empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    EXPECT_GE(errors.size(), 3u);
}

TEST(Jacobian, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "jacobian",
        "kisaoID": "KISAO:0000415",
        "model": "#tasks:model1.model",
        "isFull": true
    })");
    Jacobian sim;
    sim.fromJSON(json);
    EXPECT_TRUE(sim.getIsFull().value);
    EXPECT_EQ(sim.toJSON(), json);

    Jacobian empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // kisaoID, model.
    EXPECT_GE(errors.size(), 2u);
}

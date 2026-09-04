// Most of this class's mechanics (TypeName, default-construction, each
// attribute's own get/set/isSet/unset - including scalarList's insert/
// remove - the missing-required-attributes count, and the move/reparenting
// fix for its owned independentVariableRange) are now covered generically
// by codegen/generate_classes.py's generated tests (see
// ExplicitODESimulationGenerated.* in the sed2_generated_tests target).
// What's left here is what the generator can't produce: realistic,
// reference-bearing content.
#include <gtest/gtest.h>

#include "sed2/generated/ExplicitODESimulation.h"

using sed2::ExplicitODESimulation;

TEST(ExplicitODESimulation, FromJsonToJsonRoundTrip) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "explicitODESimulation",
        "kisaoID": "KISAO:0000694",
        "model": "#tasks:model1.model",
        "independentVariable": "urn:sedml:symbol:time",
        "independentVariableInit": 0,
        "independentVariableRange": {
            "_type": "numericRange",
            "start": 0,
            "end": 20,
            "numberOfSteps": 100,
            "scale": "linear"
        },
        "outputVariables": ["S1", "S2", "S3"],
        "outputModel": false
    })");

    ExplicitODESimulation sim;
    sim.fromJSON(json);

    std::vector<sed2::ValidationError> errors;
    sim.validate(errors);
    // A standalone ExplicitODESimulation (no owning SEDDocument) can't have
    // its "model" reference resolved either way, so validate() reports
    // that as Info rather than staying silent about it (see
    // AttributeTypes::validateReference) - not a defect in the document.
    for (const auto& error : errors) {
        EXPECT_EQ(error.severity, sed2::ValidationSeverity::Info) << error.message;
    }

    sed2::Json out = sim.toJSON();
    EXPECT_EQ(out.at("kisaoID").get<std::string>(), "KISAO:0000694");
    EXPECT_EQ(out.at("outputVariables"), json.at("outputVariables"));
    ASSERT_TRUE(out.contains("independentVariableRange"));
    EXPECT_EQ(out.at("independentVariableRange").at("_type").get<std::string>(), "numericRange");
}

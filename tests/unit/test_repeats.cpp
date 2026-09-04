#include <gtest/gtest.h>

#include "sed2/generated/Loop.h"
#include "sed2/generated/ParameterRange.h"
#include "sed2/generated/ParameterScan.h"
#include "sed2/generated/Range.h"
#include "sed2/generated/Scatter.h"

using sed2::Loop;
using sed2::ParameterRange;
using sed2::ParameterScan;
using sed2::Range;
using sed2::Scatter;

TEST(Range, FromJsonToJsonRoundTripWithLiteralValues) {
    sed2::Json json = sed2::Json::parse(R"({"_type": "range", "values": [1, 2, 3]})");
    Range range;
    range.fromJSON(json);
    EXPECT_FALSE(range.isSetValuesReference());
    EXPECT_EQ(range.getNumValues(), 3u);
    EXPECT_EQ(range.toJSON(), json);
}

TEST(Range, FromJsonToJsonRoundTripWithWholeListReference) {
    sed2::Json json = sed2::Json::parse(R"({"_type": "range", "values": "#tasks:otherRange"})");
    Range range;
    range.fromJSON(json);
    EXPECT_TRUE(range.isSetValuesReference());
    EXPECT_EQ(range.getValuesReference(), "#tasks:otherRange");
    EXPECT_EQ(range.toJSON(), json);

    std::vector<sed2::ValidationError> errors;
    range.validate(errors);
    // Standalone: can't tell whether "#tasks:otherRange" resolves.
    ASSERT_EQ(errors.size(), 1u);
    EXPECT_EQ(errors[0].severity, sed2::ValidationSeverity::Info);
}

TEST(ParameterRange, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "parameterRange",
        "modelElement": "#tasks:model1['k1']",
        "start": 0,
        "end": 10,
        "numberOfSteps": 5,
        "scale": "linear"
    })");
    ParameterRange range;
    range.fromJSON(json);
    EXPECT_EQ(range.getStart().value, 0.0);
    EXPECT_EQ(range.getNumberOfSteps().value, 5);
    EXPECT_EQ(range.toJSON(), json);

    ParameterRange empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // modelElement.
    EXPECT_GE(errors.size(), 1u);
}

TEST(Scatter, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "scatter",
        "subTasks": {
            "sub1": {"_type": "modelImport", "location": "model.xml", "language": "urn:sedml:language:sbml"}
        },
        "range": {"_type": "range", "values": [1, 2, 3]}
    })");
    Scatter scatter;
    scatter.fromJSON(json);
    EXPECT_EQ(scatter.getNumSubTasks(), 1u);
    ASSERT_NE(scatter.getSubTask("sub1"), nullptr);
    ASSERT_NE(scatter.getRange(), nullptr);
    EXPECT_EQ(scatter.toJSON(), json);

    Scatter empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // subTasks.
    EXPECT_GE(errors.size(), 1u);
}

TEST(Loop, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "loop",
        "subTasks": {
            "sub1": {"_type": "modelImport", "location": "model.xml", "language": "urn:sedml:language:sbml"}
        },
        "loopVariables": {
            "i": {"initialValue": 0, "subsequentValues": "#tasks:range1"}
        }
    })");
    Loop loop;
    loop.fromJSON(json);
    EXPECT_EQ(loop.getNumLoopVariables(), 1u);
    ASSERT_NE(loop.getLoopVariable("i"), nullptr);
    EXPECT_EQ(loop.toJSON(), json);

    Loop empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // subTasks, loopVariables.
    EXPECT_GE(errors.size(), 2u);
}

TEST(ParameterScan, FromJsonToJsonRoundTripAndValidate) {
    // Key order matches ParameterScan.json's attribute order (subTasks
    // before model before parameterRanges) - sed2::Json is nlohmann's
    // ordered_json, whose operator== is order-sensitive for objects.
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "parameterScan",
        "subTasks": {
            "sim1": {"_type": "steadyState", "kisaoID": "KISAO:0000407", "model": "#tasks:model1.model",
                     "outputVariables": ["S1"]}
        },
        "model": "#tasks:model1.model",
        "parameterRanges": [
            {"_type": "parameterRange", "modelElement": "#tasks:model1['k1']", "start": 0, "end": 10, "numberOfSteps": 5}
        ]
    })");
    ParameterScan scan;
    scan.fromJSON(json);
    EXPECT_EQ(scan.getNumParameterRanges(), 1u);
    EXPECT_EQ(scan.toJSON(), json);

    ParameterScan empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // model, subTasks, parameterRanges.
    EXPECT_GE(errors.size(), 3u);
}

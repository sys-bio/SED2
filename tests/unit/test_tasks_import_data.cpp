#include <gtest/gtest.h>

#include "sed2/generated/AggregationCalculation.h"
#include "sed2/generated/Calculation.h"
#include "sed2/generated/CreateDataBlock.h"
#include "sed2/generated/CsvImport.h"
#include "sed2/generated/DataImport.h"
#include "sed2/generated/DrawFromDistribution.h"
#include "sed2/generated/ModelChange.h"
#include "sed2/generated/ModelElementList.h"
#include "sed2/generated/ModelImport.h"
#include "sed2/generated/RelabelData.h"
#include "sed2/generated/StringFormation.h"

using sed2::AggregationCalculation;
using sed2::Calculation;
using sed2::CreateDataBlock;
using sed2::CsvImport;
using sed2::DataImport;
using sed2::DrawFromDistribution;
using sed2::ModelChange;
using sed2::ModelElementList;
using sed2::ModelImport;
using sed2::RelabelData;
using sed2::StringFormation;

TEST(ModelImport, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "modelImport",
        "location": "model.xml",
        "language": "urn:sedml:language:sbml"
    })");
    ModelImport task;
    task.fromJSON(json);
    EXPECT_EQ(task.getLocation(), "model.xml");
    EXPECT_EQ(task.toJSON(), json);

    ModelImport empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // location, language.
    EXPECT_GE(errors.size(), 2u);
}

TEST(DataImport, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "dataImport",
        "location": "data.csv",
        "format": "urn:sedml:format:csv"
    })");
    DataImport task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    DataImport empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    EXPECT_GE(errors.size(), 2u);
}

TEST(CsvImport, FromJsonToJsonRoundTrip) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "csvImport",
        "location": "data.csv",
        "headers": true,
        "columnNames": ["time", "S1"],
        "ncols": 2
    })");
    CsvImport task;
    task.fromJSON(json);
    EXPECT_TRUE(task.getHeaders().value);
    EXPECT_EQ(task.getNumColumnNames(), 2u);
    EXPECT_EQ(task.toJSON(), json);

    CsvImport empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // location.
    EXPECT_GE(errors.size(), 1u);
}

TEST(ModelChange, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "modelChange",
        "inputModel": "#tasks:model1.model",
        "setValues": {"S1": 5.0},
        "addElements": ["#tasks:model1['S2']"]
    })");
    ModelChange task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    ModelChange empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // inputModel.
    EXPECT_GE(errors.size(), 1u);
}

TEST(ModelElementList, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "modelElementList",
        "model": "#tasks:model1.model",
        "includeTypes": ["species"]
    })");
    ModelElementList task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    ModelElementList empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    EXPECT_GE(errors.size(), 1u);
}

TEST(CreateDataBlock, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "createDataBlock",
        "data": [1, 2, 3]
    })");
    CreateDataBlock task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    CreateDataBlock empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    EXPECT_GE(errors.size(), 1u);
}

TEST(RelabelData, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "relabelData",
        "input": "#tasks:data1",
        "labels": ["a", "b"]
    })");
    RelabelData task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    RelabelData empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // input, labels.
    EXPECT_GE(errors.size(), 2u);
}

TEST(StringFormation, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "stringFormation",
        "concatenate": ["prefix_", "#tasks:sim1"]
    })");
    StringFormation task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    StringFormation empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    EXPECT_GE(errors.size(), 1u);
}

TEST(Calculation, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "calculation",
        "math": "x + 1"
    })");
    Calculation task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    Calculation empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    EXPECT_GE(errors.size(), 1u);
}

TEST(AggregationCalculation, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "aggregationCalculation",
        "kisaoID": "KISAO:0000825",
        "input": "#tasks:scatter1.outputs",
        "appliedDimensions": ["dim1"]
    })");
    AggregationCalculation task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    AggregationCalculation empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // kisaoID, input.
    EXPECT_GE(errors.size(), 2u);
}

TEST(DrawFromDistribution, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "drawFromDistribution",
        "altDefinition": "urn:example:dist",
        "arguments": {"mean": 0, "stdDev": 1}
    })");
    DrawFromDistribution task;
    task.fromJSON(json);
    EXPECT_EQ(task.toJSON(), json);

    DrawFromDistribution empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // altDefinition, arguments.
    EXPECT_GE(errors.size(), 2u);
}

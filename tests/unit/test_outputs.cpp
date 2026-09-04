#include <gtest/gtest.h>

#include "sed2/generated/Curve.h"
#include "sed2/generated/Plot2D.h"
#include "sed2/generated/Plot3D.h"
#include "sed2/generated/Surface.h"

using sed2::Curve;
using sed2::Plot2D;
using sed2::Plot3D;
using sed2::Surface;

TEST(Curve, ScalarAttributesAndValidate) {
    Curve curve;
    curve.setCurveType("points");
    curve.setX("#tasks:sim1.model['S1']");
    curve.setY("#tasks:sim1.model['S2']");
    EXPECT_EQ(curve.getCurveType(), "points");

    std::vector<sed2::ValidationError> errors;
    curve.validate(errors);
    // x/y are references; standalone (no owning SEDDocument), so validate()
    // can only say it can't tell whether they resolve (Info), not that they
    // do - see AttributeTypes::validateReference.
    for (const auto& error : errors) {
        EXPECT_EQ(error.severity, sed2::ValidationSeverity::Info) << error.message;
    }

    Curve empty;
    errors.clear();
    empty.validate(errors);
    // curveType, x, y.
    EXPECT_GE(errors.size(), 3u);
}

TEST(Surface, ScalarAttributesAndValidate) {
    Surface surface;
    surface.setSurfaceType("heatMap");
    surface.setX("#tasks:sim1.model['S1']");
    surface.setY("#tasks:sim1.model['S2']");
    surface.setZ("#tasks:sim1.model['S3']");

    std::vector<sed2::ValidationError> errors;
    surface.validate(errors);
    for (const auto& error : errors) {
        EXPECT_EQ(error.severity, sed2::ValidationSeverity::Info) << error.message;
    }

    Surface empty;
    errors.clear();
    empty.validate(errors);
    // surfaceType, x, y, z.
    EXPECT_GE(errors.size(), 4u);
}

// Axis's own get/set/isSet/unset mechanics are now covered generically by
// AxisGenerated.* (see codegen/generate_classes.py's generated tests, in
// the sed2_generated_tests target); it doesn't need a hand-written
// counterpart here.

TEST(Plot2D, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "plot2D",
        "xAxis": {"scale": "linear"},
        "yAxis": {"scale": "log10"},
        "curves": {
            "curve1": {"curveType": "points", "x": "#tasks:sim1.model['time']", "y": "#tasks:sim1.model['S1']"}
        }
    })");
    Plot2D plot;
    plot.fromJSON(json);
    ASSERT_NE(plot.getXAxis(), nullptr);
    EXPECT_EQ(plot.getNumCurves(), 1u);
    ASSERT_NE(plot.getCurve("curve1"), nullptr);
    EXPECT_EQ(plot.toJSON(), json);

    Plot2D empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // curves.
    EXPECT_GE(errors.size(), 1u);
}

TEST(Plot3D, FromJsonToJsonRoundTripAndValidate) {
    sed2::Json json = sed2::Json::parse(R"({
        "_type": "plot3D",
        "zAxis": {"scale": "linear"},
        "surfaces": {
            "surface1": {"surfaceType": "heatMap", "x": "#tasks:sim1.model['S1']",
                         "y": "#tasks:sim1.model['S2']", "z": "#tasks:sim1.model['S3']"}
        }
    })");
    Plot3D plot;
    plot.fromJSON(json);
    ASSERT_NE(plot.getZAxis(), nullptr);
    EXPECT_EQ(plot.getNumSurfaces(), 1u);
    EXPECT_EQ(plot.toJSON(), json);

    Plot3D empty;
    std::vector<sed2::ValidationError> errors;
    empty.validate(errors);
    // surfaces.
    EXPECT_GE(errors.size(), 1u);
}

#include <gtest/gtest.h>

#include "sed2/core/SEDBase.h"

namespace {

// SEDBase is abstract (getTypeName() is pure virtual); a minimal concrete
// subclass is all these tests need.
class TestElement : public sed2::SEDBase {
public:
    std::string getTypeName() const override { return "testElement"; }
};

}  // namespace

TEST(SEDBase, IdGetSetIsSetUnset) {
    TestElement element;
    EXPECT_FALSE(element.isSetId());
    EXPECT_EQ(element.getId(), "");

    element.setId("x1");
    EXPECT_TRUE(element.isSetId());
    EXPECT_EQ(element.getId(), "x1");

    element.unsetId();
    EXPECT_FALSE(element.isSetId());
    EXPECT_EQ(element.getId(), "");
}

TEST(SEDBase, NameDescriptionNotesGetSetIsSetUnset) {
    TestElement element;

    element.setName("Example");
    EXPECT_TRUE(element.isSetName());
    EXPECT_EQ(element.getName(), "Example");
    element.unsetName();
    EXPECT_FALSE(element.isSetName());

    element.setDescription("A description.");
    EXPECT_TRUE(element.isSetDescription());
    element.unsetDescription();
    EXPECT_FALSE(element.isSetDescription());

    element.setNotes("Some *markdown* notes.");
    EXPECT_TRUE(element.isSetNotes());
    EXPECT_EQ(element.getNotes(), "Some *markdown* notes.");
    element.unsetNotes();
    EXPECT_FALSE(element.isSetNotes());
}

TEST(SEDBase, AnnotationsListApi) {
    TestElement element;
    EXPECT_FALSE(element.isSetAnnotations());
    EXPECT_EQ(element.getNumAnnotations(), 0u);

    element.addAnnotation({"bibo:Journal", "first"});
    element.addAnnotation({"dc:license", "second"});
    ASSERT_EQ(element.getNumAnnotations(), 2u);
    EXPECT_TRUE(element.isSetAnnotations());

    element.insertAnnotation(1, {"dc:title", "middle"});
    ASSERT_EQ(element.getNumAnnotations(), 3u);
    EXPECT_EQ(element.getAnnotations()[0].value, "first");
    EXPECT_EQ(element.getAnnotations()[1].value, "middle");
    EXPECT_EQ(element.getAnnotations()[2].value, "second");

    EXPECT_TRUE(element.removeAnnotationAt(0));
    ASSERT_EQ(element.getNumAnnotations(), 2u);
    EXPECT_EQ(element.getAnnotations()[0].value, "middle");
    EXPECT_FALSE(element.removeAnnotationAt(10));

    element.unsetAnnotations();
    EXPECT_FALSE(element.isSetAnnotations());
    EXPECT_EQ(element.getNumAnnotations(), 0u);
}

TEST(SEDBase, RoundTripsAndPreservesUnrecognizedFields) {
    TestElement element;
    sed2::Json json = sed2::Json::parse(R"({
        "id": "x1",
        "name": "Example",
        "annotations": [{"qualifier": "dc:title", "value": "v"}],
        "futureAttribute": 42
    })");

    element.fromJSON(json);
    EXPECT_EQ(element.getId(), "x1");
    EXPECT_EQ(element.getName(), "Example");
    ASSERT_EQ(element.getNumAnnotations(), 1u);
    EXPECT_EQ(element.getAnnotations()[0].qualifier, "dc:title");

    sed2::Json out = element.toJSON();
    EXPECT_EQ(out.at("_type").get<std::string>(), "testElement");
    EXPECT_EQ(out.at("id").get<std::string>(), "x1");
    // Not modeled by SEDBase or TestElement, but must survive the round trip.
    EXPECT_EQ(out.at("futureAttribute").get<int>(), 42);
}

TEST(SEDBase, ValidateHasNoRequiredAttributesOfItsOwn) {
    TestElement element;
    std::vector<sed2::ValidationError> errors;
    element.validate(errors);
    EXPECT_TRUE(errors.empty());
}

// Hand-written API tests for the library functions that are not validation
// rules: an element's own id (get_id / is_set_id), the public reference API
// (parse_reference / get_sed_reference), index and label accessors on
// constants and literals (apply_indices / get_reference_value).
//
// This file lives under templates/cpp/tests/ (hand-written, never
// regenerated - see Design.md's Code Generation section). generator/
// emit_cpp.py copies it to <out>/tests/ApiTest.cpp (see _copy_api_test_cpp),
// rewriting its #include lines and using-namespace declaration to match
// --cpp-namespace, and only for a spec tree that has the real SED2 classes
// (tasks, outputs, constants): these tests use them directly. It is built
// into the same fixture_tests executable as FixtureTest.cpp. Its documents
// come from fixtures/api/ (see the README there), found the same way
// FixtureTest.cpp finds fixtures/. The Python and Java targets have the same
// tests (test_api.py, ApiTest.java); keep the three in step. ASCII only.

#include <libsed2/Io.hpp>

#include <gtest/gtest.h>

#include <algorithm>
#include <cstdlib>
#include <memory>
#include <set>
#include <string>
#include <utility>
#include <vector>

using namespace libsed2;

namespace {

std::string fixtures_dir() {
    const char* env = std::getenv("SED2_FIXTURES_DIR");
    if (env && *env) return std::string(env);
#ifdef SED2_FIXTURES_DIR_DEFAULT
    return SED2_FIXTURES_DIR_DEFAULT;
#else
    return "../../fixtures";
#endif
}

std::unique_ptr<SEDDocument> load_doc() {
    return read_from_file(fixtures_dir() + "/api/ids-and-references.doc.json");
}

using Strings = std::vector<std::string>;

/// One accessor chain as a compact string: ".model", "['S1']", "[1]", "[0:2]", "[:3]", "[2:]".
std::string describe(const ParsedReference& p) {
    std::string out;
    for (const auto& a : p.accessors) {
        if (a.is_dot) {
            out += "." + a.name;
        } else if (a.index.is_label()) {
            out += "['" + a.index.sval + "']";
        } else if (a.index.is_int()) {
            out += "[" + std::to_string(a.index.ival) + "]";
        } else {
            out += "[" + (a.index.a ? std::to_string(*a.index.a) : std::string()) + ":" +
                   (a.index.b ? std::to_string(*a.index.b) : std::string()) + "]";
        }
    }
    return out;
}

SedBase* sub_task(SEDDocument& doc, const std::string& loop_id, const std::string& sub_id) {
    auto* loop = dynamic_cast<Loop*>(doc.get_tasks_item(loop_id));
    EXPECT_NE(loop, nullptr);
    return loop ? loop->get_subTasks_item(sub_id) : nullptr;
}

}  // namespace

TEST(ApiTest, DocumentIsValid) {
    auto doc = load_doc();
    EXPECT_TRUE(doc->validate().empty());
}

// ---- G-005: a math field is text, with value accessors only ----------------
// (The absence of get/set/is_math_ref is a compile-time fact in C++.)

TEST(ApiTest, MathFieldHasValueAccessors) {
    Calculation calc;
    EXPECT_FALSE(calc.is_set_math());
    EXPECT_THROW(calc.get_math_value(), ApiError);
    calc.set_math_value("#constants:k_num * 2");
    EXPECT_TRUE(calc.is_set_math());
    EXPECT_EQ(calc.get_math_value(), "#constants:k_num * 2");
    calc.unset_math();
    EXPECT_FALSE(calc.is_set_math());
}

TEST(ApiTest, MathFieldThatIsOnlyAReferenceIsStillMath) {
    auto doc = load_doc();
    auto calc = std::make_unique<Calculation>();
    Calculation* c = calc.get();
    c->set_math_value("#constants:k_num");
    doc->add_tasks("calc1", std::move(calc));
    EXPECT_EQ(c->get_math_value(), "#constants:k_num");
    EXPECT_TRUE(doc->validate().empty());
}

// ---- G-001: an element's own id --------------------------------------------

TEST(ApiTest, IdOfTopLevelTasksAndOutputs) {
    auto doc = load_doc();
    EXPECT_EQ(doc->get_tasks(), (Strings{"m1", "sim1", "loop1"}));
    for (const auto& id : doc->get_tasks()) {
        SedBase* task = doc->get_tasks_item(id);
        EXPECT_TRUE(task->is_set_id());
        EXPECT_EQ(task->get_id(), id);
    }
    EXPECT_EQ(doc->get_outputs(), (Strings{"rep1"}));
    EXPECT_EQ(doc->get_outputs_item("rep1")->get_id(), "rep1");
}

TEST(ApiTest, IdOfNestedElements) {
    auto doc = load_doc();
    auto* loop = dynamic_cast<Loop*>(doc->get_tasks_item("loop1"));
    ASSERT_NE(loop, nullptr);
    EXPECT_EQ(loop->get_subTasks(), (Strings{"s1", "s2"}));
    for (const auto& id : loop->get_subTasks()) {
        SedBase* sub = loop->get_subTasks_item(id);
        EXPECT_EQ(sub->get_id(), id);
        EXPECT_EQ(sub->get_parent(), loop);   // the owning element, not the collection
    }
    EXPECT_EQ(loop->get_loopVariables_item("lv1")->get_id(), "lv1");
    EXPECT_EQ(loop->get_aggregateOutputVariables_item("a1")->get_id(), "a1");
}

TEST(ApiTest, TopLevelParentIsTheDocumentNotTheCollection) {
    auto doc = load_doc();
    EXPECT_EQ(doc->get_tasks_item("m1")->get_parent(), doc.get());
}

TEST(ApiTest, IdIsNotSetForElementsOutsideIdKeyedCollections) {
    auto doc = load_doc();
    EXPECT_FALSE(doc->is_set_id());
    EXPECT_THROW(doc->get_id(), ApiError);
    auto* sim = dynamic_cast<ExplicitODESimulation*>(doc->get_tasks_item("sim1"));
    ASSERT_NE(sim, nullptr);
    SedBase* embedded = sim->get_independentVariableRange();   // a single embedded child
    EXPECT_FALSE(embedded->is_set_id());
    EXPECT_THROW(embedded->get_id(), ApiError);
}

TEST(ApiTest, IdOfCreatedElementFollowsAddInsertRename) {
    auto doc = load_doc();
    auto created = std::make_unique<ModelImport>();
    ModelImport* c = created.get();
    EXPECT_FALSE(c->is_set_id());
    EXPECT_THROW(c->get_id(), ApiError);

    doc->add_tasks("m2", std::move(created));
    EXPECT_TRUE(c->is_set_id());
    EXPECT_EQ(c->get_id(), "m2");

    auto other = std::make_unique<ModelImport>();
    ModelImport* o = other.get();
    doc->insert_tasks(0, "first", std::move(other));
    EXPECT_EQ(o->get_id(), "first");
    EXPECT_EQ(doc->get_tasks()[0], "first");

    doc->set_id_on_tasks("m2", "m3");                          // a renamed id
    EXPECT_EQ(c->get_id(), "m3");
    EXPECT_EQ(doc->get_tasks_item("m3"), c);
    // (remove_tasks() destroys the element - the collection owns it - so a
    // removed element's id cannot be asked for in C++.)
}

TEST(ApiTest, IdOfCreatedElementInNestedCollection) {
    auto doc = load_doc();
    auto* loop = dynamic_cast<Loop*>(doc->get_tasks_item("loop1"));
    ASSERT_NE(loop, nullptr);
    auto created = std::make_unique<ModelImport>();
    ModelImport* c = created.get();
    loop->add_subTasks("s3", std::move(created));
    EXPECT_EQ(c->get_id(), "s3");
    loop->set_id_on_subTasks("s3", "s4");
    EXPECT_EQ(c->get_id(), "s4");
}

TEST(ApiTest, IdOfRenamedExistingElement) {
    auto doc = load_doc();
    SedBase* sim = doc->get_tasks_item("sim1");
    doc->set_id_on_tasks("sim1", "sim_renamed");
    EXPECT_EQ(sim->get_id(), "sim_renamed");
}

TEST(ApiTest, IdOfUnregisteredNamespaceTaskHolder) {
    auto doc = read_from_string(
        "{\"version\":\"v1.0.0\",\"tasks\":{\"x1\":{\"_type\":\"acme@Thing\",\"foo\":1}}}");
    SedBase* holder = doc->get_tasks_item("x1");
    ASSERT_TRUE(holder->get_type_value().has_value());
    EXPECT_EQ(*holder->get_type_value(), "acme@Thing");
    EXPECT_EQ(holder->get_id(), "x1");
}

TEST(ApiTest, IdIsNotPartOfTheSerializedDocument) {
    auto doc = load_doc();
    Json before = doc->to_json_value();
    for (const auto& id : doc->get_tasks()) doc->get_tasks_item(id)->get_id();
    EXPECT_EQ(doc->to_json_value(), before);
}

// ---- G-002(a): public reference parsing and resolution ----------------------

TEST(ApiTest, IsReferenceDetectsHashPrefix) {
    EXPECT_TRUE(is_reference("#tasks:a"));
    EXPECT_FALSE(is_reference("tasks:a"));
    EXPECT_FALSE(is_reference(""));
}

TEST(ApiTest, ParseReferencePathAndDotAndLabel) {
    ParsedReference p = parse_reference("#tasks:loop1:subTasks:s1.model['S1']");
    EXPECT_EQ(p.raw, "#tasks:loop1:subTasks:s1.model['S1']");
    ASSERT_TRUE(p.collection.has_value());
    EXPECT_EQ(*p.collection, "tasks");
    EXPECT_EQ(p.path, (Strings{"loop1", "subTasks", "s1"}));
    ASSERT_EQ(p.accessors.size(), 2u);
    EXPECT_TRUE(p.accessors[0].is_dot);
    EXPECT_EQ(p.accessors[0].name, "model");
    EXPECT_TRUE(p.accessors[1].index.is_label());
    EXPECT_EQ(p.accessors[1].index.sval, "S1");
    EXPECT_EQ(p.first_dot().value_or(""), "model");
}

TEST(ApiTest, ParseReferenceAccessors) {
    const std::vector<std::pair<std::string, std::string>> cases = {
        {"#constants:k_array[1]", "[1]"},
        {"#constants:k_array[-1]", "[-1]"},
        {"#tasks:sim1[0:2]", "[0:2]"},
        {"#tasks:sim1[:3]", "[:3]"},
        {"#tasks:sim1[2:]", "[2:]"},
        {"#tasks:sim1[0][1]", "[0][1]"},
        {"#tasks:sim1[0,1]", "[0][1]"},
        {"#tasks:sim1[\"S1\"]", "['S1']"},
        {"#tasks:sim1.range", ".range"},
        {"#tasks:sim1.model[0]", ".model[0]"},
        {"#tasks:sim1", ""},
    };
    for (const auto& c : cases) {
        SCOPED_TRACE(c.first);
        ParsedReference p = parse_reference(c.first);
        ASSERT_TRUE(p.collection.has_value());
        EXPECT_TRUE(*p.collection == "tasks" || *p.collection == "constants");
        EXPECT_EQ(p.path.size(), 1u);
        EXPECT_EQ(describe(p), c.second);
    }
}

TEST(ApiTest, ParseReferenceIsLenientAndNeverThrows) {
    ParsedReference empty = parse_reference("#");
    EXPECT_FALSE(empty.collection.has_value());
    EXPECT_TRUE(empty.path.empty());
    EXPECT_TRUE(empty.accessors.empty());
    ParsedReference no_hash = parse_reference("tasks:sim1");     // a leading '#' is optional
    EXPECT_EQ(no_hash.collection.value_or(""), "tasks");
    EXPECT_EQ(no_hash.path, (Strings{"sim1"}));
    ParsedReference unterminated = parse_reference("#tasks:sim1[");   // text after a failed accessor is ignored
    EXPECT_EQ(unterminated.path, (Strings{"sim1"}));
    EXPECT_EQ(describe(unterminated), "");
    EXPECT_EQ(describe(parse_reference("#tasks:sim1.model[1")), ".model");
    EXPECT_EQ(describe(parse_reference("#tasks:sim1.")), "");
}

TEST(ApiTest, GetSedReferenceResolvesTasks) {
    auto doc = load_doc();
    const std::vector<std::vector<std::string>> cases = {
        {"#tasks:m1", "m1", "#tasks:m1"},
        {"#tasks:sim1", "sim1", "#tasks:sim1"},
        {"#tasks:loop1:subTasks:s1", "s1", "#tasks:loop1:subTasks:s1"},
        {"#tasks:loop1:subTasks:s2", "s2", "#tasks:loop1:subTasks:s2"},
        {"#tasks:sim1.model['S1']", "sim1", "#tasks:sim1"},          // accessors are not applied
        {"#tasks:loop1:subTasks:s1[0][1]", "s1", "#tasks:loop1:subTasks:s1"},
    };
    for (const auto& c : cases) {
        SCOPED_TRACE(c[0]);
        ReferenceTarget by_text = get_sed_reference(doc.get(), c[0]);
        ReferenceTarget by_parsed = get_sed_reference(doc.get(), parse_reference(c[0]));
        for (const ReferenceTarget& r : {by_text, by_parsed}) {
            ASSERT_NE(r.element, nullptr);
            EXPECT_EQ(r.value, nullptr);
            EXPECT_TRUE(r.is_resolved());
            EXPECT_EQ(r.element->get_id(), c[1]);
            EXPECT_EQ(r.resolved_prefix.value_or("<none>"), c[2]);
        }
    }
}

TEST(ApiTest, GetSedReferenceReturnsTheElementItself) {
    auto doc = load_doc();
    EXPECT_EQ(get_sed_reference(doc.get(), "#tasks:loop1:subTasks:s1").element, sub_task(*doc, "loop1", "s1"));
    ReferenceTarget out = get_sed_reference(doc.get(), "#outputs:rep1");   // resolves, though validate() forbids referencing it
    EXPECT_EQ(out.element, doc->get_outputs_item("rep1"));
    EXPECT_EQ(out.resolved_prefix.value_or("<none>"), "#outputs:rep1");
}

TEST(ApiTest, GetSedReferenceResolvesConstantsToRawValues) {
    auto doc = load_doc();
    ReferenceTarget num = get_sed_reference(doc.get(), "#constants:k_num");
    EXPECT_EQ(num.element, nullptr);
    ASSERT_NE(num.value, nullptr);
    EXPECT_DOUBLE_EQ(num.value->as<double>(), 1.5);
    EXPECT_EQ(num.resolved_prefix.value_or("<none>"), "#constants:k_num");
    ReferenceTarget strings = get_sed_reference(doc.get(), "#constants:k_strings");
    ASSERT_NE(strings.value, nullptr);
    EXPECT_EQ(strings.value->to_string(), "[\"a\",\"b\"]");
    // the index chain is parsed, not applied: the whole constant comes back
    ReferenceTarget indexed = get_sed_reference(doc.get(), "#constants:k_strings[1]");
    ASSERT_NE(indexed.value, nullptr);
    EXPECT_EQ(indexed.value->to_string(), "[\"a\",\"b\"]");
    EXPECT_EQ(indexed.resolved_prefix.value_or("<none>"), "#constants:k_strings");
}

TEST(ApiTest, GetSedReferenceUnresolvedReportsLongestResolvedPrefix) {
    auto doc = load_doc();
    const std::vector<std::pair<std::string, std::string>> cases = {
        {"#tasks:nope", "#tasks"},
        {"#tasks", "#tasks"},
        {"#tasks:loop1:subTasks:nope", "#tasks:loop1"},
        {"#tasks:loop1:subTasks", "#tasks:loop1"},                  // a lone trailing segment is an attribute
        {"#tasks:loop1:nosuchcollection:s1", "#tasks:loop1"},
        {"#tasks:m1:subTasks:s1", "#tasks:m1"},                     // m1 has no sub-collections
        {"#constants:nope", "#constants"},
        {"#constants:k_num:x:y", "#constants:k_num"},               // a raw value has no children
        {"#outputs:nope", "#outputs"},
    };
    for (const auto& c : cases) {
        SCOPED_TRACE(c.first);
        ReferenceTarget r = get_sed_reference(doc.get(), c.first);
        EXPECT_EQ(r.element, nullptr);
        EXPECT_EQ(r.value, nullptr);
        EXPECT_FALSE(r.is_resolved());
        EXPECT_EQ(r.resolved_prefix.value_or("<none>"), c.second);
    }
}

TEST(ApiTest, GetSedReferenceUnrecognizedCollectionOrNoDocument) {
    auto doc = load_doc();
    for (const ReferenceTarget& r : {get_sed_reference(doc.get(), "#bogus:x"), get_sed_reference(doc.get(), "#"),
                                     get_sed_reference(nullptr, "#tasks:m1")}) {
        EXPECT_EQ(r.element, nullptr);
        EXPECT_EQ(r.value, nullptr);
        EXPECT_FALSE(r.resolved_prefix.has_value());
    }
}

// ---- G-002(b): index and label accessors on constants and literals -----------

namespace {

Json J(const std::string& text) { return Json::parse(text); }

template <typename F>
std::string error_of(F f) {
    try {
        f();
    } catch (const ApiError& e) {
        return e.what();
    }
    ADD_FAILURE() << "expected an ApiError";
    return "";
}

bool contains(const std::string& text, const std::string& part) { return text.find(part) != std::string::npos; }

}  // namespace

TEST(ApiTest, ApplyIndicesOnLiterals) {
    struct Case { const char* value; const char* accessors; const char* expected; };
    const std::vector<Case> cases = {
        {"[10,20,30,40]", "[0]", "10"},
        {"[10,20,30,40]", "[3]", "40"},
        {"[10,20,30,40]", "[-1]", "40"},
        {"[10,20,30,40]", "[-4]", "10"},
        {"[10,20,30,40]", "[1:3]", "[20,30]"},
        {"[10,20,30,40]", "[:2]", "[10,20]"},
        {"[10,20,30,40]", "[-2:]", "[30,40]"},
        {"[10,20,30,40]", "[:]", "[10,20,30,40]"},
        {"[10,20,30,40]", "[1:99]", "[20,30,40]"},
        {"[10,20,30,40]", "[3:1]", "[]"},
        {R"({"S1":[1,2,3],"S2":[4,5,6]})", "['S2']", "[4,5,6]"},
        {R"({"S1":[1,2,3],"S2":[4,5,6]})", "[\"S1\"][2]", "3"},
        {R"({"S1":[1,2,3],"S2":[4,5,6]})", "['S2'][-2:]", "[5,6]"},
        {R"({"a":{"b":7}})", "['a']['b']", "7"},
        {"[[1,2],[3,4]]", "[1][0]", "3"},
        {"[[1,2],[3,4]]", "[0:2][1]", "[3,4]"},
        {"[[1,2],[3,4]]", "[0:2][0:1]", "[[1,2]]"},
        {"[[1,2],[3,4],[5,6]]", "[0:2][1]", "[3,4]"},
        {"[[1,2],[3,4],[5,6]]", "[0:2, 1]", "[2,4]"},
        {"[[1,2],[3,4],[5,6]]", "[1:3, 0]", "[3,5]"},
        {"[[1,2],[3,4],[5,6]]", "[:, 1]", "[2,4,6]"},
        {"[[1,2],[3,4],[5,6]]", "[1, 0]", "3"},
        {"[[1,2],[3,4],[5,6]]", "[1, :]", "[3,4]"},
        {"[[1,2],[3,4],[5,6]]", "[0:2, 0:1]", "[[1],[3]]"},
        {"[[1,2],[3,4],[5,6]]", "[0:2, 1][0]", "2"},
        {"[[1,2],[3,4],[5,6]]", "[0:2][1, 0]", "3"},
        {"[[1,2],[3,4],[5,6]]", "[0:3][1:3][1]", "[5,6]"},
        {R"({"S1":[1,2,3],"S2":[4,5,6]})", "['S2', 1:]", "[5,6]"},
        {R"([{"a":1},{"a":2}])", "[0:2, 'a']", "[1,2]"},
        {"[[1,2],[3,4]]", "[2:2, 9]", "[]"},
        {R"({"x":null})", "['x']", "null"},
        {"5", "", "5"},
        {R"("abc")", "", R"("abc")"},
    };
    for (const auto& c : cases) {
        SCOPED_TRACE(std::string(c.value) + " " + c.accessors);
        EXPECT_EQ(apply_indices(J(c.value), std::string(c.accessors)), J(c.expected));
    }
}

TEST(ApiTest, ApplyIndicesAcceptsTextParsedReferenceOrIndexObjects) {
    Json value = J(R"({"S1":[1,2,3]})");
    EXPECT_EQ(apply_indices(value, std::string("['S1'][1]")), J("2"));
    EXPECT_EQ(apply_indices(value, std::string("#constants:anything['S1'][1]")), J("2"));   // the path is ignored
    EXPECT_EQ(apply_indices(value, parse_reference("['S1'][1]")), J("2"));
    RefIndex label;
    label.kind = RefIndex::LABEL;
    label.sval = "S1";
    RefIndex one;
    one.kind = RefIndex::INT;
    one.ival = 1;
    EXPECT_EQ(apply_indices(value, std::vector<RefIndex>{label, one}), J("2"));
    EXPECT_EQ(apply_indices(value, std::vector<RefIndex>{}), value);                        // no indices: the value itself
}

TEST(ApiTest, ApplyIndicesRejectsAnIndexThatDoesNotFit) {
    const std::vector<std::pair<const char*, const char*>> cases = {
        {"[1,2,3]", "[3]"},
        {"[1,2,3]", "[-4]"},
        {"[1,2,3]", "['S1']"},
        {R"({"S1":1})", "[0]"},
        {R"({"S1":1})", "[0:1]"},
        {R"({"S1":1})", "['S2']"},
        {"5", "[0]"},
        {R"("abc")", "[0]"},
        {"null", "[0]"},
        {"[1,2,3]", "[0][0]"},
        {"[[1,2],[3,4]]", "[0:2][2]"},
        {"[[1,2],[3,4]]", "[0:2, 2]"},
        {"[[1,2],[3,4]]", "[0:2]['S1']"},
        {"[1,2,3]", "[0, 0]"},
        {"[[1,2],[3,4]]", "[0:2, 0, 0]"},
    };
    for (const auto& c : cases) {
        SCOPED_TRACE(std::string(c.first) + " " + c.second);
        std::string msg = error_of([&] { apply_indices(J(c.first), std::string(c.second)); });
        EXPECT_TRUE(contains(msg, "SEDBase-0012")) << msg;
    }
}

TEST(ApiTest, ParseMarksTheIndicesOfOneBracket) {
    ParsedReference p = parse_reference("#tasks:sim1[0:2, 'S1'][1]");
    ASSERT_EQ(p.accessors.size(), 3u);
    EXPECT_FALSE(p.accessors[0].index.same_bracket);
    EXPECT_TRUE(p.accessors[1].index.same_bracket);
    EXPECT_FALSE(p.accessors[2].index.same_bracket);
    EXPECT_TRUE(p.accessors[0].index.is_range());
    EXPECT_TRUE(p.accessors[1].index.is_label());
    EXPECT_TRUE(p.accessors[2].index.is_int());
    ParsedReference q = parse_reference("#tasks:sim1[0][1]");
    EXPECT_FALSE(q.accessors[1].index.same_bracket);
}

TEST(ApiTest, ApplyIndicesRejectsDotAccessors) {
    EXPECT_TRUE(contains(error_of([] { apply_indices(J(R"({"a":1})"), std::string("['a'].model")); }), "SEDBase-0008"));
    EXPECT_TRUE(contains(error_of([] { apply_indices(J(R"({"a":1})"), std::string(".model")); }), "SEDBase-0008"));
}

TEST(ApiTest, ApplyIndicesErrorNamesTheFailingIndex) {
    EXPECT_TRUE(contains(error_of([] { apply_indices(J(R"({"S1":1})"), std::string("['S3']")); }), "['S3']"));
    EXPECT_TRUE(contains(error_of([] { apply_indices(J("[[1]]"), std::string("[0][7]")); }), "[7]"));
}

TEST(ApiTest, GetReferenceValueEvaluatesConstants) {
    auto doc = load_doc();
    const std::vector<std::pair<const char*, const char*>> cases = {
        {"#constants:k_num", "1.5"},
        {"#constants:k_strings", R"(["a","b"])"},
        {"#constants:k_strings[1]", R"("b")"},
        {"#constants:k_strings[-2]", R"("a")"},
        {"#constants:k_list[1:3]", "[20,30]"},
        {"#constants:k_table['S1']", "[1,2,3]"},
        {"#constants:k_table['S2'][0]", "4"},
        {"#constants:k_table['S2'][1:]", "[5,6]"},
        {"#constants:k_alias", "[4,5,6]"},
        {"#constants:k_alias[2]", "6"},
        {"#constants:k_alias2", "[4,5,6]"},
        {"#constants:k_alias2[-1]", "6"},
        {"#constants:k_none", "null"},
    };
    for (const auto& c : cases) {
        SCOPED_TRACE(c.first);
        EXPECT_EQ(get_reference_value(doc.get(), std::string(c.first)), J(c.second));
        EXPECT_EQ(get_reference_value(doc.get(), parse_reference(c.first)), J(c.second));
    }
}

TEST(ApiTest, GetReferenceValueReportsWhatDoesNotApply) {
    auto doc = load_doc();
    const std::vector<std::pair<const char*, const char*>> cases = {
        {"#constants:nope", "SEDBase-0006"},
        {"#constants", "SEDBase-0006"},
        {"#constants:k_num:x:y", "SEDBase-0006"},
        {"#constants:k_num[0]", "SEDBase-0012"},
        {"#constants:k_list[4]", "SEDBase-0012"},
        {"#constants:k_list['S1']", "SEDBase-0012"},
        {"#constants:k_table[0]", "SEDBase-0012"},
        {"#constants:k_table['S3']", "SEDBase-0012"},
        {"#constants:k_alias[3]", "SEDBase-0012"},
        {"#constants:k_table.model", "SEDBase-0008"},
    };
    for (const auto& c : cases) {
        SCOPED_TRACE(c.first);
        std::string msg = error_of([&] { get_reference_value(doc.get(), std::string(c.first)); });
        EXPECT_TRUE(contains(msg, c.second)) << msg;
    }
}

TEST(ApiTest, GetReferenceValueOnlyConstantsHaveAValueBeforeRunTime) {
    auto doc = load_doc();
    for (const char* ref : {"#tasks:m1", "#tasks:sim1.model", "#outputs:rep1", "#styles:x", "#bogus:x"}) {
        SCOPED_TRACE(ref);
        std::string msg = error_of([&] { get_reference_value(doc.get(), std::string(ref)); });
        EXPECT_TRUE(contains(msg, "does not name a constant")) << msg;
    }
}

TEST(ApiTest, GetReferenceValueWithoutADocument) {
    EXPECT_TRUE(contains(error_of([] { get_reference_value(nullptr, std::string("#constants:k_num")); }), "SEDBase-0006"));
}

TEST(ApiTest, GetReferenceValueRejectsACircularChain) {
    auto d = read_from_string(R"({"version":"v1.0.0","constants":{"a":"#constants:b","b":"#constants:a"}})");
    EXPECT_TRUE(contains(error_of([&] { get_reference_value(d.get(), std::string("#constants:a")); }), "circular"));
}

TEST(ApiTest, GetReferenceValueFollowsAConstantThatPointsAtATaskToAnError) {
    auto d = read_from_string(R"({"version":"v1.0.0","constants":{"a":"#tasks:m1"}})");
    EXPECT_TRUE(contains(error_of([&] { get_reference_value(d.get(), std::string("#constants:a")); }),
                         "does not name a constant"));
}

TEST(ApiTest, GetReferenceValueSeesApiEdits) {
    auto doc = load_doc();
    doc->add_constants("fresh", J("[7,8,9]"));
    EXPECT_EQ(get_reference_value(doc.get(), std::string("#constants:fresh[-1]")), J("9"));
}

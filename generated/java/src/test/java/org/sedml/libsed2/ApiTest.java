package org.sedml.libsed2;

/*
 * Hand-written API tests for the library functions that are not validation
 * rules: an element's own id (getId / isSetId), the public reference API
 * (References.parse / References.getSedReference), index and label accessors on
 * constants and literals (References.applyIndices / References.getReferenceValue).
 *
 * This file lives under templates/java/tests/ (hand-written, never
 * regenerated - see Design.md's Code Generation section) and is copied, with
 * its package line rewritten to match --java-package, to
 * <out>/java/src/test/java/<package-path>/ApiTest.java by generator/
 * emit_java.py (see _copy_api_test_java), but only for a spec tree that has
 * the real SED2 classes (tasks, outputs, constants): these tests use them
 * directly. Its documents come from fixtures/api/ (see the README there),
 * found the same way FixtureTest finds fixtures/. The Python and C++ targets
 * have the same tests (test_api.py, ApiTest.cpp); keep the three in step.
 */

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class ApiTest {

    private static File fixturesDir() {
        String env = System.getenv("SED2_FIXTURES_DIR");
        if (env != null && !env.isEmpty()) return new File(env);
        String prop = System.getProperty("sed2.fixturesDir");
        if (prop != null && !prop.isEmpty()) return new File(prop);
        return new File("../../fixtures");
    }

    private SEDDocument doc;

    @BeforeEach
    void loadDocument() throws IOException {
        doc = Io.readFromFile(new File(fixturesDir(), "api/ids-and-references.doc.json").getPath());
    }

    @Test
    void apiDocumentIsValid() {
        assertEquals(0, doc.validate().size());
    }

    // ---- G-001: an element's own id ---------------------------------------

    @Test
    void idOfTopLevelTasksAndOutputs() {
        assertEquals(List.of("m1", "sim1", "loop1"), doc.getTasks());
        for (String id : doc.getTasks()) {
            SedBase task = doc.getTasksItem(id);
            assertTrue(task.isSetId());
            assertEquals(id, task.getId());
        }
        assertEquals(List.of("rep1"), doc.getOutputs());
        assertEquals("rep1", doc.getOutputsItem("rep1").getId());
    }

    @Test
    void idOfNestedElements() {
        Loop loop = (Loop) doc.getTasksItem("loop1");
        assertEquals(List.of("s1", "s2"), loop.getSubTasks());
        for (String id : loop.getSubTasks()) {
            SedBase sub = loop.getSubTasksItem(id);
            assertEquals(id, sub.getId());
            assertSame(loop, sub.getParent());      // the owning element, not the collection
        }
        assertEquals("lv1", loop.getLoopVariablesItem("lv1").getId());
        assertEquals("a1", loop.getAggregateOutputVariablesItem("a1").getId());
    }

    @Test
    void topLevelParentIsTheDocumentNotTheCollection() {
        assertSame(doc, doc.getTasksItem("m1").getParent());
    }

    @Test
    void idIsNotSetForElementsOutsideIdKeyedCollections() {
        assertFalse(doc.isSetId());
        assertThrows(ApiError.class, () -> doc.getId());
        ExplicitODESimulation sim = (ExplicitODESimulation) doc.getTasksItem("sim1");
        SedBase embedded = sim.getIndependentVariableRange();        // a single embedded child
        assertFalse(embedded.isSetId());
        assertThrows(ApiError.class, embedded::getId);
    }

    @Test
    void idOfCreatedElementFollowsAddInsertRenameRemove() {
        ModelImport created = new ModelImport();
        assertFalse(created.isSetId());
        assertThrows(ApiError.class, created::getId);

        doc.addTasks("m2", created);
        assertTrue(created.isSetId());
        assertEquals("m2", created.getId());

        ModelImport other = new ModelImport();
        doc.insertTasks(0, "first", other);
        assertEquals("first", other.getId());
        assertEquals("first", doc.getTasks().get(0));

        doc.setIdOnTasks("m2", "m3");                                // a renamed id
        assertEquals("m3", created.getId());
        assertSame(created, doc.getTasksItem("m3"));

        doc.removeTasks("m3");
        assertFalse(created.isSetId());
        assertThrows(ApiError.class, created::getId);
    }

    @Test
    void idOfCreatedElementInNestedCollection() {
        Loop loop = (Loop) doc.getTasksItem("loop1");
        ModelImport created = new ModelImport();
        loop.addSubTasks("s3", created);
        assertEquals("s3", created.getId());
        loop.setIdOnSubTasks("s3", "s4");
        assertEquals("s4", created.getId());
    }

    @Test
    void idOfRenamedExistingElement() {
        SedBase sim = doc.getTasksItem("sim1");
        doc.setIdOnTasks("sim1", "sim_renamed");
        assertEquals("sim_renamed", sim.getId());
    }

    @Test
    void idOfUnregisteredNamespaceTaskHolder() throws IOException {
        String text = "{\"version\":\"v1.0.0\",\"tasks\":{\"x1\":{\"_type\":\"acme@Thing\",\"foo\":1}}}";
        SEDDocument d = Io.readFromString(text);
        SedBase holder = d.getTasksItem("x1");
        assertEquals("acme@Thing", holder.typeValue());
        assertEquals("x1", holder.getId());
    }

    @Test
    void idIsNotPartOfTheSerializedDocument() {
        JsonNode before = doc.toJsonValue().deepCopy();
        for (String id : doc.getTasks()) doc.getTasksItem(id).getId();
        assertEquals(before, doc.toJsonValue());
    }

    // ---- G-002(a): public reference parsing and resolution ----------------

    /** One accessor chain as a compact string: ".model", "['S1']", "[1]", "[0:2]", "[:3]", "[2:]". */
    private static String describe(ParsedReference p) {
        StringBuilder sb = new StringBuilder();
        for (ParsedReference.Accessor a : p.accessors) {
            if (a.isDot()) {
                sb.append('.').append(a.dotName);
            } else if (a.index.kind.equals("label")) {
                sb.append("['").append(a.index.label).append("']");
            } else if (a.index.kind.equals("int")) {
                sb.append('[').append(a.index.intValue).append(']');
            } else {
                sb.append('[').append(a.index.rangeStart == null ? "" : a.index.rangeStart.toString())
                        .append(':').append(a.index.rangeEnd == null ? "" : a.index.rangeEnd.toString()).append(']');
            }
        }
        return sb.toString();
    }

    @Test
    void isReferenceDetectsHashPrefix() {
        assertTrue(References.isReference("#tasks:a"));
        assertFalse(References.isReference("tasks:a"));
        assertFalse(References.isReference((String) null));
    }

    @Test
    void parseReferencePathAndDotAndLabel() {
        ParsedReference p = References.parse("#tasks:loop1:subTasks:s1.model['S1']");
        assertEquals("#tasks:loop1:subTasks:s1.model['S1']", p.raw);
        assertEquals("tasks", p.collection);
        assertEquals(List.of("loop1", "subTasks", "s1"), p.path);
        assertEquals(2, p.accessors.size());
        assertTrue(p.accessors.get(0).isDot());
        assertEquals("model", p.accessors.get(0).dotName);
        assertEquals("label", p.accessors.get(1).index.kind);
        assertEquals("S1", p.accessors.get(1).index.label);
        assertEquals("model", p.firstDotName());
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', value = {
            "#constants:k_array[1]|[1]",
            "#constants:k_array[-1]|[-1]",
            "#tasks:sim1[0:2]|[0:2]",
            "#tasks:sim1[:3]|[:3]",
            "#tasks:sim1[2:]|[2:]",
            "#tasks:sim1[0][1]|[0][1]",
            "#tasks:sim1[0,1]|[0][1]",
            "#tasks:sim1[\"S1\"]|['S1']",
            "#tasks:sim1.range|.range",
            "#tasks:sim1.model[0]|.model[0]",
    })
    void parseReferenceAccessors(String text, String expected) {
        ParsedReference p = References.parse(text);
        assertTrue(p.collection.equals("tasks") || p.collection.equals("constants"));
        assertEquals(1, p.path.size());
        assertEquals(expected, describe(p));
    }

    @Test
    void parseReferenceWithoutAccessorsHasNone() {
        assertEquals(0, References.parse("#tasks:sim1").accessors.size());
    }

    @Test
    void parseReferenceIsLenientAndNeverThrows() {
        ParsedReference empty = References.parse("#");
        assertNull(empty.collection);
        assertEquals(0, empty.path.size());
        assertEquals(0, empty.accessors.size());
        ParsedReference noHash = References.parse("tasks:sim1");     // a leading '#' is optional
        assertEquals("tasks", noHash.collection);
        assertEquals(List.of("sim1"), noHash.path);
        ParsedReference unterminated = References.parse("#tasks:sim1[");   // text after a failed accessor is ignored
        assertEquals(List.of("sim1"), unterminated.path);
        assertEquals("", describe(unterminated));
        assertEquals(".model", describe(References.parse("#tasks:sim1.model[1")));
        assertEquals("", describe(References.parse("#tasks:sim1.")));
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', value = {
            "#tasks:m1|m1|#tasks:m1",
            "#tasks:sim1|sim1|#tasks:sim1",
            "#tasks:loop1:subTasks:s1|s1|#tasks:loop1:subTasks:s1",
            "#tasks:loop1:subTasks:s2|s2|#tasks:loop1:subTasks:s2",
            "#tasks:sim1.model['S1']|sim1|#tasks:sim1",
            "#tasks:loop1:subTasks:s1[0][1]|s1|#tasks:loop1:subTasks:s1",
    })
    void getSedReferenceResolvesTasks(String ref, String taskId, String prefix) {
        for (References.Resolved r : new References.Resolved[] {
                References.getSedReference(doc, ref),                       // text
                References.getSedReference(doc, References.parse(ref))}) {  // ParsedReference
            assertTrue(r.element instanceof SedBase);
            assertEquals(taskId, ((SedBase) r.element).getId());
            assertEquals(prefix, r.prefix);
        }
    }

    @Test
    void getSedReferenceReturnsTheElementItself() {
        Loop loop = (Loop) doc.getTasksItem("loop1");
        assertSame(loop.getSubTasksItem("s1"), References.getSedReference(doc, "#tasks:loop1:subTasks:s1").element);
        References.Resolved out = References.getSedReference(doc, "#outputs:rep1");   // resolves, though validate() forbids referencing it
        assertSame(doc.getOutputsItem("rep1"), out.element);
        assertEquals("#outputs:rep1", out.prefix);
    }

    @Test
    void getSedReferenceResolvesConstantsToRawValues() throws IOException {
        ObjectMapper m = new ObjectMapper();
        References.Resolved num = References.getSedReference(doc, "#constants:k_num");
        assertEquals(m.readTree("1.5"), num.element);
        assertEquals("#constants:k_num", num.prefix);
        References.Resolved strings = References.getSedReference(doc, "#constants:k_strings");
        assertEquals(m.readTree("[\"a\",\"b\"]"), strings.element);
        // the index chain is parsed, not applied: the whole constant comes back
        References.Resolved indexed = References.getSedReference(doc, "#constants:k_strings[1]");
        assertEquals(m.readTree("[\"a\",\"b\"]"), indexed.element);
        assertEquals("#constants:k_strings", indexed.prefix);
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', value = {
            "#tasks:nope|#tasks",
            "#tasks|#tasks",
            "#tasks:loop1:subTasks:nope|#tasks:loop1",
            "#tasks:loop1:subTasks|#tasks:loop1",
            "#tasks:loop1:nosuchcollection:s1|#tasks:loop1",
            "#tasks:m1:subTasks:s1|#tasks:m1",
            "#constants:nope|#constants",
            "#constants:k_num:x:y|#constants:k_num",
            "#outputs:nope|#outputs",
    })
    void getSedReferenceUnresolvedReportsLongestResolvedPrefix(String ref, String prefix) {
        References.Resolved r = References.getSedReference(doc, ref);
        assertNull(r.element);
        assertEquals(prefix, r.prefix);
    }

    @Test
    void getSedReferenceUnrecognizedCollectionOrNoDocument() {
        for (References.Resolved r : new References.Resolved[] {
                References.getSedReference(doc, "#bogus:x"),
                References.getSedReference(doc, "#"),
                References.getSedReference(null, "#tasks:m1")}) {
            assertNull(r.element);
            assertNull(r.prefix);
        }
    }

    // ---- G-002(b): index and label accessors on constants and literals ----

    private static final ObjectMapper MAPPER = new ObjectMapper();

    private static JsonNode json(String text) {
        try {
            return MAPPER.readTree(text);
        } catch (IOException e) {
            throw new AssertionError(e);
        }
    }

    private static String errorOf(Runnable r) {
        ApiError e = assertThrows(ApiError.class, r::run);
        return e.getMessage();
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', quoteCharacter = '^', value = {
            "[10,20,30,40]|[0]|10",
            "[10,20,30,40]|[3]|40",
            "[10,20,30,40]|[-1]|40",
            "[10,20,30,40]|[-4]|10",
            "[10,20,30,40]|[1:3]|[20,30]",
            "[10,20,30,40]|[:2]|[10,20]",
            "[10,20,30,40]|[-2:]|[30,40]",
            "[10,20,30,40]|[:]|[10,20,30,40]",
            "[10,20,30,40]|[1:99]|[20,30,40]",
            "[10,20,30,40]|[3:1]|[]",
            "{\"S1\":[1,2,3],\"S2\":[4,5,6]}|['S2']|[4,5,6]",
            "{\"S1\":[1,2,3],\"S2\":[4,5,6]}|[\"S1\"][2]|3",
            "{\"S1\":[1,2,3],\"S2\":[4,5,6]}|['S2'][-2:]|[5,6]",
            "{\"a\":{\"b\":7}}|['a']['b']|7",
            "[[1,2],[3,4]]|[1][0]|3",
            "[[1,2],[3,4]]|[0:2][1]|[3,4]",
            "[[1,2],[3,4]]|[0:2][0:1]|[[1,2]]",
            "{\"x\":null}|['x']|null",
            "5||5",
            "\"abc\"||\"abc\"",
    })
    void applyIndicesOnLiterals(String value, String accessors, String expected) {
        String text = accessors == null ? "" : accessors;
        assertEquals(json(expected), References.applyIndices(json(value), text));
    }

    @Test
    void applyIndicesAcceptsTextParsedReferenceOrIndexObjects() {
        JsonNode value = json("{\"S1\":[1,2,3]}");
        assertEquals(json("2"), References.applyIndices(value, "['S1'][1]"));
        assertEquals(json("2"), References.applyIndices(value, "#constants:anything['S1'][1]"));   // the path is ignored
        assertEquals(json("2"), References.applyIndices(value, References.parse("['S1'][1]")));
        assertEquals(json("2"), References.applyIndices(value,
                List.of(RefIndex.ofLabel("S1"), RefIndex.ofInt(java.math.BigInteger.ONE))));
        assertSame(value, References.applyIndices(value, new ArrayList<RefIndex>()));          // no indices: the value itself
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', quoteCharacter = '^', value = {
            "[1,2,3]|[3]",
            "[1,2,3]|[-4]",
            "[1,2,3]|['S1']",
            "{\"S1\":1}|[0]",
            "{\"S1\":1}|[0:1]",
            "{\"S1\":1}|['S2']",
            "5|[0]",
            "\"abc\"|[0]",
            "null|[0]",
            "[1,2,3]|[0][0]",
    })
    void applyIndicesRejectsAnIndexThatDoesNotFit(String value, String accessors) {
        assertTrue(errorOf(() -> References.applyIndices(json(value), accessors)).contains("SEDBase-0012"));
    }

    @Test
    void applyIndicesRejectsDotAccessors() {
        assertTrue(errorOf(() -> References.applyIndices(json("{\"a\":1}"), "['a'].model")).contains("SEDBase-0008"));
        assertTrue(errorOf(() -> References.applyIndices(json("{\"a\":1}"), ".model")).contains("SEDBase-0008"));
    }

    @Test
    void applyIndicesErrorNamesTheFailingIndex() {
        assertTrue(errorOf(() -> References.applyIndices(json("{\"S1\":1}"), "['S3']")).contains("['S3']"));
        assertTrue(errorOf(() -> References.applyIndices(json("[[1]]"), "[0][7]")).contains("[7]"));
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', quoteCharacter = '^', value = {
            "#constants:k_num|1.5",
            "#constants:k_strings|[\"a\",\"b\"]",
            "#constants:k_strings[1]|\"b\"",
            "#constants:k_strings[-2]|\"a\"",
            "#constants:k_list[1:3]|[20,30]",
            "#constants:k_table['S1']|[1,2,3]",
            "#constants:k_table['S2'][0]|4",
            "#constants:k_table['S2'][1:]|[5,6]",
            "#constants:k_alias|[4,5,6]",
            "#constants:k_alias[2]|6",
            "#constants:k_alias2|[4,5,6]",
            "#constants:k_alias2[-1]|6",
            "#constants:k_none|null",
    })
    void getReferenceValueEvaluatesConstants(String ref, String expected) {
        assertEquals(json(expected), References.getReferenceValue(doc, ref));
        assertEquals(json(expected), References.getReferenceValue(doc, References.parse(ref)));
    }

    @ParameterizedTest
    @CsvSource(delimiter = '|', quoteCharacter = '^', value = {
            "#constants:nope|SEDBase-0006",
            "#constants|SEDBase-0006",
            "#constants:k_num:x:y|SEDBase-0006",
            "#constants:k_num[0]|SEDBase-0012",
            "#constants:k_list[4]|SEDBase-0012",
            "#constants:k_list['S1']|SEDBase-0012",
            "#constants:k_table[0]|SEDBase-0012",
            "#constants:k_table['S3']|SEDBase-0012",
            "#constants:k_alias[3]|SEDBase-0012",
            "#constants:k_table.model|SEDBase-0008",
    })
    void getReferenceValueReportsWhatDoesNotApply(String ref, String rule) {
        assertTrue(errorOf(() -> References.getReferenceValue(doc, ref)).contains(rule));
    }

    @ParameterizedTest
    @CsvSource({"#tasks:m1", "#tasks:sim1.model", "#outputs:rep1", "#styles:x", "#bogus:x"})
    void getReferenceValueOnlyConstantsHaveAValueBeforeRunTime(String ref) {
        assertTrue(errorOf(() -> References.getReferenceValue(doc, ref)).contains("does not name a constant"));
    }

    @Test
    void getReferenceValueWithoutADocument() {
        assertTrue(errorOf(() -> References.getReferenceValue(null, "#constants:k_num")).contains("SEDBase-0006"));
    }

    @Test
    void getReferenceValueRejectsACircularChain() {
        SEDDocument d = new SEDDocument();
        d.addConstants("a", json("\"#constants:b\""));
        d.addConstants("b", json("\"#constants:a\""));
        assertTrue(errorOf(() -> References.getReferenceValue(d, "#constants:a")).contains("circular"));
    }

    @Test
    void getReferenceValueFollowsAConstantThatPointsAtATaskToAnError() {
        SEDDocument d = new SEDDocument();
        d.addConstants("a", json("\"#tasks:m1\""));
        assertTrue(errorOf(() -> References.getReferenceValue(d, "#constants:a")).contains("does not name a constant"));
    }

    @Test
    void getReferenceValueSeesApiEdits() {
        doc.addConstants("fresh", json("[7,8,9]"));
        assertEquals(json("9"), References.getReferenceValue(doc, "#constants:fresh[-1]"));
    }
}

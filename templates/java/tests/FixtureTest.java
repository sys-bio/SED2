package org.sed2test;

/*
 * Hand-written glue: runs every test-specsheets/fixtures/*.sed2.json fixture
 * through the generated libsed2test library's parser + validate(), and
 * checks it against the rule ID(s)/count(s) encoded in the filename - see
 * Design.md's Testing section for the naming convention this parses.
 *
 * This file lives under templates/java/tests/ (hand-written, never
 * regenerated - see Design.md's Code Generation section) and is copied
 * alongside the generated library, under src/test/java/org/sed2test/, for
 * `mvn test` to run. It is the Java analog of
 * templates/python/tests/test_fixtures.py - see that file for the
 * reference implementation this one mirrors, including its fix for the
 * chain-suffix parsing bug (a rule ID's own trailing NNNN segment is
 * always 4 digits, never a chain-count boundary).
 */

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assertions.fail;

public class FixtureTest {

    private static final Pattern FIXTURE_RE = Pattern.compile(
            "^(?<rule>[A-Za-z0-9_-]+)-(?<kind>pass|fail)-(?<count>\\d+)-(?<name>.+?)"
                    + "(?<chain>(?:-[A-Za-z0-9_-]+-\\d+)*)\\.sed2\\.json$");

    private static File fixturesDir() {
        String env = System.getenv("SED2_FIXTURES_DIR");
        if (env != null && !env.isEmpty()) return new File(env);
        return new File("../../../../fixtures");
    }

    static Stream<File> fixtureFiles() {
        File dir = fixturesDir();
        File[] files = dir.listFiles((d, name) -> name.endsWith(".sed2.json"));
        if (files == null) return Stream.empty();
        List<File> list = new ArrayList<>(List.of(files));
        list.sort((a, b) -> a.getName().compareTo(b.getName()));
        return list.stream();
    }

    private static final class Expected {
        final String kind;
        final List<Map.Entry<String, Integer>> rules;

        Expected(String kind, List<Map.Entry<String, Integer>> rules) {
            this.kind = kind;
            this.rules = rules;
        }
    }

    private static Expected expectedFromFilename(String base) {
        if (base.startsWith("pass-")) {
            return new Expected("pass", List.of());
        }
        Matcher m = FIXTURE_RE.matcher(base);
        assertTrue(m.matches(), "fixture name doesn't match convention: " + base);
        String rule = m.group("rule");
        String kind = m.group("kind");
        int count = Integer.parseInt(m.group("count"));
        String chain = m.group("chain");
        List<Map.Entry<String, Integer>> expected = new ArrayList<>();
        expected.add(Map.entry(rule, count));
        if (chain != null && !chain.isEmpty()) {
            String stripped = chain.replaceAll("^-+", "").replaceAll("-+$", "");
            String[] parts = stripped.split("-");
            // A chain segment is "<rule-id-tokens...>-<count>". Rule ids
            // themselves always end in a 4-digit NNNN segment, while a
            // chain count uses the same short (1-2 digit) width used
            // elsewhere in the filename - so only a non-4-digit numeric
            // token ends a segment (see test_fixtures.py's fix, mirrored
            // here).
            List<Integer> nums = new ArrayList<>();
            for (int i = 0; i < parts.length; i++) {
                if (parts[i].matches("\\d+") && parts[i].length() != 4) nums.add(i);
            }
            int start = 0;
            for (int idx : nums) {
                StringBuilder rid = new StringBuilder();
                for (int j = start; j < idx; j++) {
                    if (rid.length() > 0) rid.append('-');
                    rid.append(parts[j]);
                }
                int cnt = Integer.parseInt(parts[idx]);
                expected.add(Map.entry(rid.toString(), cnt));
                start = idx + 1;
            }
        }
        return new Expected(kind, expected);
    }

    private static final Map<String, Class<? extends SedBase>> DIRECT_CLASSES = Map.of(
            "Choice-0002", Choice.class,
            "WeightedChoice-0002", WeightedChoice.class,
            "SimpleWidget-0002", SimpleWidget.class,
            "FancyWidget-0002", FancyWidget.class,
            "SimpleReport-0002", SimpleReport.class,
            "acme-AcmeWidget-0002", AcmeWidget.class);

    @ParameterizedTest(name = "{0}")
    @MethodSource("fixtureFiles")
    void testFixture(File path) throws Exception {
        String base = path.getName();
        Expected expected = expectedFromFilename(base);
        String raw = Files.readString(path.toPath());
        ObjectMapper mapper = new ObjectMapper();
        JsonNode instance = mapper.readTree(raw);

        // ensure the rule catalog is populated even if Io hasn't been
        // touched yet by this test run
        RulesData.register();

        List<ValidationProblem> problems;
        String directKey = null;
        for (String k : DIRECT_CLASSES.keySet()) {
            if (base.startsWith(k)) {
                directKey = k;
                break;
            }
        }
        if (directKey != null) {
            SedBase obj = DIRECT_CLASSES.get(directKey).getConstructor().newInstance();
            Dispatch.loadFields(obj, instance);
            problems = obj.validate();
        } else {
            TestDocument doc = Io.readFromString(raw);
            problems = doc.validate();
            if (expected.kind.equals("pass")) {
                JsonNode rt = mapper.readTree(Io.writeToString(doc));
                assertEquals(instance, rt, "round-trip mismatch for " + path);
            }
        }

        if (expected.kind.equals("pass")) {
            assertTrue(problems.isEmpty(), path + " expected to pass, got " + problems);
            return;
        }

        Map<String, Integer> counts = new HashMap<>();
        for (ValidationProblem p : problems) counts.merge(p.ruleId, 1, Integer::sum);
        for (Map.Entry<String, Integer> e : expected.rules) {
            int got = counts.getOrDefault(e.getKey(), 0);
            assertEquals(e.getValue().intValue(), got,
                    path + ": expected rule " + e.getKey() + " to fire " + e.getValue()
                            + " time(s), got " + got + " (all problems: " + problems + ")");
        }
        java.util.Set<String> allowedIds = new java.util.HashSet<>();
        for (Map.Entry<String, Integer> e : expected.rules) allowedIds.add(e.getKey());
        Map<String, Integer> extra = new HashMap<>();
        for (Map.Entry<String, Integer> e : counts.entrySet()) {
            if (!allowedIds.contains(e.getKey())) extra.put(e.getKey(), e.getValue());
        }
        if (!extra.isEmpty()) {
            fail(path + ": unexpected extra violations: " + extra + " (all: " + problems + ")");
        }
    }
}

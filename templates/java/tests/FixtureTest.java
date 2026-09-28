package org.sed2test;

/*
 * Hand-written glue: runs every fixture in this tree's fixtures/ directory
 * through the generated library's parser + validate(), and checks it
 * against the rule ID(s)/count(s) encoded in the filename - see Design.md's
 * Testing section for the naming convention this parses.
 *
 * This file lives under templates/java/tests/ (hand-written, never
 * regenerated - see Design.md's Code Generation section) and is copied,
 * with its package line rewritten to match --java-package, to
 * <out>/java/src/test/java/<package-path>/FixtureTest.java as part of
 * every `generate.py` run that includes the java target (see
 * generator/emit_java.py's _copy_fixture_test_java) - never by hand, so a
 * fresh spec regeneration always carries a matching, up-to-date copy with
 * it. It is the Java analog of templates/python/tests/test_fixtures.py -
 * see that file for the reference implementation this one mirrors,
 * including its fix for the chain-suffix parsing bug (a rule ID's own
 * trailing NNNN segment is always 4 digits, never a chain-count boundary).
 *
 * Nothing below is specific to any one spec tree (test-specsheets/ vs.
 * specsheets/, or any future one): the document root class, which classes
 * need "direct" (not document-embedded) validation, and which fixture
 * files to run are all discovered at test time from whatever got generated
 * and whatever fixture files exist on disk - never a hardcoded class name
 * or list. Point this file at a different generated tree (i.e. let the
 * generator copy it there) and it "just works" unmodified. The package
 * line above is the one exception - Java requires it to match this file's
 * own location on disk, so the generator rewrites it (and only it) at
 * copy time; every class this file refers to below is resolved by same-
 * package visibility (SedBase, Dispatch, Io, RulesData, ValidationProblem)
 * or by reflection (the document root class, direct-only classes), so
 * nothing else here needs to change when the package does.
 */

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Constructor;
import java.lang.reflect.Modifier;
import java.net.URL;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
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

    /**
     * Maven's surefire plugin runs tests with the module's own directory
     * (the one holding pom.xml, i.e. <out>/java) as the process working
     * directory by default ("workingDirectory" defaults to
     * "${project.basedir}") - true whether `mvn test` is invoked from that
     * directory or with -f from elsewhere, and independent of how deep
     * --java-package nests this class's own source file. fixtures/ always
     * lives two levels up from <out>/java (see generate.py: fixtures/ is
     * written under dirname(--out), and java sources under --out/java), so
     * a plain relative default is safe here - unlike a path derived from
     * this class's own file location (which Java doesn't expose to a
     * compiled class the way Python's __file__ does). The generated
     * pom.xml also sets a sed2.fixturesDir system property to this same
     * path explicitly (belt-and-suspenders, and self-documenting from the
     * pom itself); SED2_FIXTURES_DIR remains the highest-priority override
     * for CI/manual runs, same as the Python target.
     */
    private static File fixturesDir() {
        String env = System.getenv("SED2_FIXTURES_DIR");
        if (env != null && !env.isEmpty()) return new File(env);
        String prop = System.getProperty("sed2.fixturesDir");
        if (prop != null && !prop.isEmpty()) return new File(prop);
        return new File("../../fixtures");
    }

    /** Every *.sed2.json anywhere under fixturesDir(), except beneath an
     * "archive" subdirectory (deprecated-rule fixtures, excluded from the
     * active suite - see Design.md's Repository Layout section). Recursive
     * so this picks up fixtures/generated/, fixtures/handwritten/, and any
     * future subdirectory Design.md's layout adds, without this file
     * needing to know about any of them by name. */
    static Stream<File> fixtureFiles() throws IOException {
        File dir = fixturesDir();
        if (!dir.isDirectory()) return Stream.empty();
        Path base = dir.toPath();
        List<File> list = new ArrayList<>();
        try (Stream<Path> walk = Files.walk(base)) {
            walk.filter(p -> p.getFileName().toString().endsWith(".sed2.json"))
                    .filter(p -> !underArchiveDir(base, p))
                    .forEach(p -> list.add(p.toFile()));
        }
        list.sort(Comparator.comparing(File::getName));
        return list.stream();
    }

    private static boolean underArchiveDir(Path base, Path file) {
        Path parent = base.relativize(file).getParent();
        if (parent == null) return false;
        for (Path part : parent) {
            if (part.toString().equals("archive")) return true;
        }
        return false;
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

    /** rule_id -> class, for every generated class whose own _type-const
     * rule (see SedBase.typeConst()/typeRuleId()) can only ever be
     * exercised by validating that class directly - not embedded through a
     * parent's discriminated dict/array field, where a _type mismatch is
     * caught by the parent's own dispatch first. Built by scanning every
     * .class file the classloader can see under this file's own package
     * (same package as every generated class - see the file-top note) and
     * probing each concrete SedBase subclass's typeRuleId(), rather than a
     * hardcoded class list, so this works unmodified against any generated
     * tree. The document root class is naturally excluded (its own
     * typeRuleId() is null), as are classes with no no-arg constructor
     * (the Unknown*Holder classes), with no special-casing needed for
     * either. */
    private static Map<String, Class<? extends SedBase>> discoverDirectOnlyClasses() throws IOException {
        Map<String, Class<? extends SedBase>> result = new HashMap<>();
        for (Class<?> cls : classesInThisPackage()) {
            if (!SedBase.class.isAssignableFrom(cls)) continue;
            if (Modifier.isAbstract(cls.getModifiers()) || cls.isInterface()) continue;
            Constructor<?> ctor;
            try {
                ctor = cls.getDeclaredConstructor();
            } catch (NoSuchMethodException e) {
                continue; // no no-arg constructor - not directly instantiable this way
            }
            try {
                ctor.setAccessible(true);
                SedBase probe = (SedBase) ctor.newInstance();
                String rid = probe.typeRuleId();
                if (rid != null) {
                    @SuppressWarnings("unchecked")
                    Class<? extends SedBase> sedBaseCls = (Class<? extends SedBase>) cls;
                    result.put(rid, sedBaseCls);
                }
            } catch (ReflectiveOperationException e) {
                throw new RuntimeException("failed probing generated class " + cls, e);
            }
        }
        return result;
    }

    private static List<Class<?>> classesInThisPackage() throws IOException {
        String pkgName = FixtureTest.class.getPackageName();
        String pkgPath = pkgName.replace('.', '/');
        List<Class<?>> classes = new ArrayList<>();
        Enumeration<URL> roots = Thread.currentThread().getContextClassLoader().getResources(pkgPath);
        while (roots.hasMoreElements()) {
            URL root = roots.nextElement();
            if (!"file".equals(root.getProtocol())) continue; // classes-on-disk only - mvn test never packs a jar first
            File dir;
            try {
                dir = new File(root.toURI());
            } catch (java.net.URISyntaxException e) {
                dir = new File(root.getPath());
            }
            File[] files = dir.listFiles((d, name) -> name.endsWith(".class"));
            if (files == null) continue;
            for (File f : files) {
                String simple = f.getName().substring(0, f.getName().length() - ".class".length());
                if (simple.contains("$")) continue; // skip nested/inner classes
                try {
                    classes.add(Class.forName(pkgName + "." + simple));
                } catch (ClassNotFoundException | LinkageError e) {
                    // not a loadable top-level class (e.g. this test class
                    // itself, package-info, ...) - skip
                }
            }
        }
        return classes;
    }

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

        Map<String, Class<? extends SedBase>> directOnly = discoverDirectOnlyClasses();
        String primaryRule = expected.rules.isEmpty() ? null : expected.rules.get(0).getKey();
        Class<? extends SedBase> directCls = primaryRule == null ? null : directOnly.get(primaryRule);

        List<ValidationProblem> problems;
        if (directCls != null) {
            SedBase obj = directCls.getDeclaredConstructor().newInstance();
            Dispatch.loadFields(obj, instance);
            problems = obj.validate();
        } else {
            var doc = Io.readFromString(raw);
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
        Set<String> allowedIds = new HashSet<>();
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

package org.sed2test;

/*
 * SEDDocument-0011 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0011.md):
 * The version of a SEDDocument should not be newer than the newest document version this library knows.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDDocument-0011.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDDocument-0011 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import com.fasterxml.jackson.databind.JsonNode;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public final class SedDocument0011 {
    private SedDocument0011() {}

    private static final Pattern VERSION_RE = Pattern.compile("^v(\\d+)\\.(\\d+)\\.(\\d+)$");

    private static long[] versionTuple(String value) {
        if (value == null) return null;
        Matcher m = VERSION_RE.matcher(value);
        if (!m.find()) return null;
        try {
            return new long[]{Long.parseLong(m.group(1)), Long.parseLong(m.group(2)), Long.parseLong(m.group(3))};
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private static int compare(long[] a, long[] b) {
        for (int i = 0; i < 3; i++) {
            if (a[i] != b[i]) return Long.compare(a[i], b[i]);
        }
        return 0;
    }

    /** `document.maxKnownDocumentVersion()` is a per-class constant the
     * generator bakes in at generate time (the newest version directory this
     * run's specsheets/ tree actually had for the document class). A document
     * with no `version` set at all, or one that doesn't match the v#.#.#
     * pattern, is already reported by SEDDocument's own required-field/pattern
     * rules elsewhere - this rule only compares two well-formed versions, and
     * stays silent otherwise rather than duplicating those. */
    public static List<ValidationProblem> check(SedBase document) {
        List<ValidationProblem> out = new ArrayList<>();
        String maxV = document.maxKnownDocumentVersion();
        JsonNode versionNode = document.valueNode("version");
        if (maxV == null || versionNode == null) return out;
        String value = versionNode.isTextual() ? versionNode.textValue() : null;
        long[] vt = versionTuple(value), mt = versionTuple(maxV);
        if (vt == null || mt == null || compare(vt, mt) <= 0) return out;
        out.add(RuleCatalog.problem("SEDDocument-0011", "/version", "value", value, "max", maxV));
        return out;
    }
}

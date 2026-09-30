package org.sed2test;

/*
 * SEDBase-0005 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0005.md):
 * The first segment of a reference must name one of SEDDocument's ID-keyed collections: tasks, constants, outputs, or styles.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0005.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0005 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0005 {
    private SedBase0005() {}

    private static final List<String> KNOWN_COLLECTIONS = List.of("tasks", "constants", "outputs", "styles");

    /** parsed is the field's own ParsedReference. Fires once if
     * parsed.collection isn't one of the four known root collections -
     * including when the reference has no colon segment at all
     * (parsed.collection is null). */
    public static List<ValidationProblem> check(ParsedReference parsed, String className, String idValue,
                                                String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (parsed.collection == null || !KNOWN_COLLECTIONS.contains(parsed.collection)) {
            out.add(RuleCatalog.problem("SEDBase-0005", location, "attr", attr, "value", parsed.raw,
                    "class", className, "id", idValue));
        }
        return out;
    }
}

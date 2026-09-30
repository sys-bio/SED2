package org.sedml.libsed2;

/*
 * SEDBase-0017 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0017.md):
 * A reference required to resolve to AnnotatedData must resolve to AnnotatedData.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0017.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0017 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0017 {
    private SedBase0017() {}

    /** resolvedKind is "annotatedData", "model", "object", or null when what
     * the reference resolves to is not statically known (silent then). Only
     * AnnotatedData is acceptable. */
    public static List<ValidationProblem> check(String resolvedKind, String resolvedDescription, String value,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (resolvedKind == null || resolvedKind.equals("annotatedData")) return out;
        out.add(RuleCatalog.problem("SEDBase-0017", location, "attr", attr, "value", value,
                "class", className, "id", idValue, "resolved-value", resolvedDescription));
        return out;
    }
}

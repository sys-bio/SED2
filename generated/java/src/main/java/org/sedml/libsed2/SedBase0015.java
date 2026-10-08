package org.sedml.libsed2;

/*
 * SEDBase-0015 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0015.md):
 * A reference required to resolve to a scalar value must apply enough non-range indices to reduce its target's shape to zero remaining dimensions.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0015.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0015 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0015 {
    private SedBase0015() {}

    /** dimsAfter is OutputsShape.resolveOutput()'s own post-index dimensions
     * list (only ever computed here for a field whose declared kind requires a
     * scalar - NumberOrRef/StringOrRef/IntegerOrRef/BooleanOrRef; ArrayOrRef/
     * DictOrRef fields never call this rule). null means the shape wasn't
     * statically known at all - nothing to say either way, so this stays
     * silent. expectedType is the field's own declared scalar kind, in the
     * message's own vocabulary ("number", "string", "integer", "boolean"). */
    public static List<ValidationProblem> check(List<Dim> dimsAfter, String expectedType, String value,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (dimsAfter == null) return out;
        // A trailing placeholder (source "open") stands for dimensions of an
        // unknown number: it never makes the shape definitely non-scalar.
        int count = 0;
        for (Dim d : dimsAfter) if (!"open".equals(d.source)) count++;
        if (count == 0) return out;
        out.add(RuleCatalog.problem("SEDBase-0015", location, "attr", attr, "value", value,
                "class", className, "id", idValue, "expected-type", expectedType, "count", count));
        return out;
    }
}

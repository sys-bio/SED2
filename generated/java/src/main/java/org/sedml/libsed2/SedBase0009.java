package org.sedml.libsed2;

/*
 * SEDBase-0009 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0009.md):
 * A reference must not apply more bracket indices than its target has dimensions.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0009.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0009 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0009 {
    private SedBase0009() {}

    /** dimsBefore is OutputsShape.resolveOutput()'s own pre-index dimensions
     * list, or null whenever the target's dimension COUNT itself isn't
     * statically known (a whole-shape runtime/input-file source, or no
     * "dimensions" at all - a "model"-typed suffix) - SEDBase-0009.md: "Only
     * fires when the target's dimension count is static... A 'runtime' or
     * 'input-file' dimension count never fires this rule." Note this is about
     * the ARRAY's own length being fixed, not each dimension's individual
     * size - an array-form "dimensions" always has a static count even when
     * some entries' own sizes are themselves runtime/input-file (see
     * SEDBase-0011/-0014 for those). */
    public static List<ValidationProblem> check(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (dimsBefore == null) return out;
        int count = indexAccessors.size();
        int expected = dimsBefore.size();
        if (count <= expected) return out;
        out.add(RuleCatalog.problem("SEDBase-0009", location, "attr", attr, "value", value,
                "class", className, "id", idValue, "count", count, "expected-count", expected));
        return out;
    }
}

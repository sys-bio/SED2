package org.sed2test;

/*
 * SEDBase-0016 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0016.md):
 * A reference required to resolve to a model must resolve to a model.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0016.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0016 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0016 {
    private SedBase0016() {}

    /** resolvedKind is "model", "annotatedData", "object", or null when what
     * the reference resolves to is not statically known (nothing to say then,
     * same "only fires when computable" convention as SEDBase-0008 through
     * -0015). Only a model is acceptable. */
    public static List<ValidationProblem> check(String resolvedKind, String resolvedDescription, String value,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (resolvedKind == null || resolvedKind.equals("model")) return out;
        out.add(RuleCatalog.problem("SEDBase-0016", location, "attr", attr, "value", value,
                "class", className, "id", idValue, "resolved-value", resolvedDescription));
        return out;
    }
}

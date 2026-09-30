package org.sedml.libsed2;

/*
 * SEDBase-0012 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0012.md):
 * A bracket index into a constant must match the structure of that constant's literal value.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0012.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0012 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0012 {
    private SedBase0012() {}

    /** The dispatcher has already done the actual indexing (following one
     * reference-hop first per SEDBase-0012.md: "A constant whose value is
     * itself a reference is followed first" - OutputsShape.indexIntoLiteral,
     * catching NotIndexable) and hands this rule just the outcome: ok (whether
     * every index in the chain applied cleanly), the specific index that
     * failed (badSubvalue, meaningful only when not ok), and resolvedValue -
     * the constant's own (post-dereference) literal value, pre-formatted as a
     * compact string for the message's {resolved-value}. */
    public static List<ValidationProblem> check(boolean ok, String badSubvalue, String resolvedValue, String value,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (ok) return out;
        out.add(RuleCatalog.problem("SEDBase-0012", location, "attr", attr, "value", value,
                "subvalue", badSubvalue, "class", className, "id", idValue, "resolved-value", resolvedValue));
        return out;
    }
}

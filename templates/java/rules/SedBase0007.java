package org.sed2test;

/*
 * SEDBase-0007 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0007.md):
 * A reference must not target an AbstractOutput, or anything contained in one.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0007.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0007 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0007 {
    private SedBase0007() {}

    /** 'outputs' is deliberately kept a syntactically legal collection name by
     * SEDBase-0005; this rule is what actually rejects using it - and it can
     * do so purely from the collection name, with no containment-tree walk
     * needed, since 'outputs' is the only root collection whose every member
     * (and everything nested inside one) is AbstractOutput-rooted. */
    public static List<ValidationProblem> check(ParsedReference parsed, String className, String idValue,
                                                String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if ("outputs".equals(parsed.collection)) {
            out.add(RuleCatalog.problem("SEDBase-0007", location, "attr", attr, "value", parsed.raw,
                    "class", className, "id", idValue));
        }
        return out;
    }
}

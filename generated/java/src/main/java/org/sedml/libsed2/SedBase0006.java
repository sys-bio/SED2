package org.sedml.libsed2;

/*
 * SEDBase-0006 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0006.md):
 * Every colon-delimited segment of a reference must resolve to an existing element.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0006.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0006 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0006 {
    private SedBase0006() {}

    /** `resolved` and `resolvedPrefix` are References.getSedReference()'s own
     * result - the dispatcher has already called it once and passes both
     * through rather than resolving twice.
     *
     * resolvedPrefix is null only when there was no document to walk at all
     * (e.g. a class validated directly, never attached to one) - not a genuine
     * resolution failure, so this rule stays silent rather than firing on
     * incomplete information. Otherwise, resolved is null iff resolution
     * failed, and resolvedPrefix is the longest prefix that DID resolve
     * (SEDBase-0006.md's own note) - the {subvalue} this rule's message uses. */
    public static List<ValidationProblem> check(ParsedReference parsed, Object resolved, String resolvedPrefix,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (resolvedPrefix == null || resolved != null) return out;
        out.add(RuleCatalog.problem("SEDBase-0006", location, "attr", attr, "value", parsed.raw,
                "subvalue", resolvedPrefix, "class", className, "id", idValue));
        return out;
    }
}

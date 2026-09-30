package org.sed2test;

/*
 * SEDBase-0013 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0013.md):
 * A reference to a Repeat's subTasks, its .range/.index outputs, or one of its loop variables is only legal when the element holding the reference is that Repeat itself, or lies within that Repeat's own subTasks (at any depth, including through a nested Repeat).
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0013.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0013 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0013 {
    private SedBase0013() {}

    /** The dispatcher has already worked out which Repeat (if any) scopes this
     * reference and whether the referring element is that Repeat itself or
     * lies within its own subTasks at any depth (inScope) - a plain
     * containment-tree ancestor walk, nothing here depends on outputs.json /
     * shape at all. Fires once when a scoped reference reaches outside its
     * Repeat; targetRepeatId feeds the message's {resolved-value}
     * (SEDBase-0013.md's own message template doesn't use {attr}). */
    public static List<ValidationProblem> check(boolean inScope, String targetRepeatId, String value,
                                                String className, String idValue, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (inScope) return out;
        out.add(RuleCatalog.problem("SEDBase-0013", location, "value", value,
                "class", className, "id", idValue, "resolved-value", targetRepeatId));
        return out;
    }
}

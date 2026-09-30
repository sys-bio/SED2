package org.sed2test;

/*
 * Repeat-0009 (specsheets/tasks/Repeat/v1.0.0/validation/Repeat-0009.md):
 * The input of every entry in a Repeat's aggregateOutputVariables must reference one of that Repeat's own subTasks, or an output of one.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/Repeat-0009.py, and, like it, only for
 * a spec tree whose own rule set actually defines Repeat-0009 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class Repeat0009 {
    private Repeat0009() {}

    /** The dispatcher (References.checkRepeatOwnChildren) has already resolved
     * the aggregateOutputVariables entry's own `input` reference and checked
     * whether its target's immediate parent is this Repeat instance itself -
     * ok is that outcome. `attr` is always "input" here, per the message's own
     * "has input '{value}'" wording. */
    public static List<ValidationProblem> check(boolean ok, Object value, String className, String idValue,
                                                String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (ok) return out;
        out.add(RuleCatalog.problem("Repeat-0009", location, "attr", attr, "value", value,
                "class", className, "id", idValue));
        return out;
    }
}

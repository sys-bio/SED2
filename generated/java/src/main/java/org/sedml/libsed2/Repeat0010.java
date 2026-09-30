package org.sedml.libsed2;

/*
 * Repeat-0010 (specsheets/tasks/Repeat/v1.0.0/validation/Repeat-0010.md):
 * An entry in a Repeat's aggregateOutputVariables must not define appliedDimensions.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/Repeat-0010.py, and, like it, only for
 * a spec tree whose own rule set actually defines Repeat-0010 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class Repeat0010 {
    private Repeat0010() {}

    /** The dispatcher (References.checkRepeatOwnChildren) has already checked
     * whether this aggregateOutputVariables entry's own JSON value defines
     * 'appliedDimensions' at all - definesAppliedDimensions is that outcome;
     * `value` is the appliedDimensions value itself, for the message's own
     * {value} (unused by this rule's own message template but harmless to
     * always pass, same as every other rule here). */
    public static List<ValidationProblem> check(boolean definesAppliedDimensions, Object value, String className,
                                                String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (!definesAppliedDimensions) return out;
        out.add(RuleCatalog.problem("Repeat-0010", location, "attr", attr, "value", value,
                "class", className, "id", idValue));
        return out;
    }
}

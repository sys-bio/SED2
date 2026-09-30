package org.sed2test;

/*
 * LoopVariable-0004 (specsheets/auxiliary/LoopVariable/v1.0.0/validation/LoopVariable-0004.md):
 * The subsequentValues of a LoopVariable must reference one of its enclosing Loop's own subTasks, or an output of one.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/LoopVariable-0004.py, and, like it, only for
 * a spec tree whose own rule set actually defines LoopVariable-0004 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class LoopVariable0004 {
    private LoopVariable0004() {}

    /** The dispatcher (References.checkLoopVariableScope) has already resolved
     * subsequentValues's own reference and checked whether its target's
     * immediate parent is this LoopVariable's own enclosing Loop - ok is that
     * outcome. This rule's own message template uses neither {class} nor
     * {attr} (unlike every other SEDBase/Repeat-family rule) - it always names
     * the fixed "LoopVariable" class and the one field a LoopVariable can ever
     * fail this way. */
    public static List<ValidationProblem> check(boolean ok, Object value, String idValue, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (ok) return out;
        out.add(RuleCatalog.problem("LoopVariable-0004", location, "value", value,
                "class", "LoopVariable", "id", idValue));
        return out;
    }
}

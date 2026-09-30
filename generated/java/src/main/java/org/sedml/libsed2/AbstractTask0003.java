package org.sedml.libsed2;

/*
 * AbstractTask-0003 (specsheets/tasks/AbstractTask/v1.0.0/validation/AbstractTask-0003.md):
 * A task may only reference constants, tasks that appear earlier in the same tasks dictionary, or (for a subTask) the elements listed in this rule's explanation.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/AbstractTask-0003.py, and, like it, only for
 * a spec tree whose own rule set actually defines AbstractTask-0003 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class AbstractTask0003 {
    private AbstractTask0003() {}

    /** The dispatcher (References.checkTaskOrder) has already walked both the
     * referring element's own and the reference's resolved target's
     * chronological position within SEDDocument.tasks (through any
     * Repeat-family subTasks nesting) and compared them per this rule's own
     * worked-out cases - ok is that comparison's own outcome. */
    public static List<ValidationProblem> check(boolean ok, String value, String className, String idValue,
                                                String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (ok) return out;
        out.add(RuleCatalog.problem("AbstractTask-0003", location, "attr", attr, "value", value,
                "class", className, "id", idValue));
        return out;
    }
}

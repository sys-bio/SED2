package org.sedml.libsed2;

/*
 * SEDBase-0008 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0008.md):
 * A dot-accessor in a reference must be one the target declares valid.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0008.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0008 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0008 {
    private SedBase0008() {}

    /** accessorOk is the dispatcher's own resolution of whether this
     * reference's suffix is a declared-valid output of its target - TRUE,
     * FALSE or null. Fires only on an outright FALSE; null means the
     * dispatcher couldn't determine this statically (a "valid" expr that
     * depends on something not knowable ahead of time), which
     * SEDBase-0008.md says should leave the rule silent - so null is
     * deliberately NOT treated as "invalid" here. */
    public static List<ValidationProblem> check(Boolean accessorOk, String dotName, String value, String className,
                                                String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (!Boolean.FALSE.equals(accessorOk)) return out;
        out.add(RuleCatalog.problem("SEDBase-0008", location, "attr", attr, "value", value,
                "subvalue", dotName == null ? "" : dotName, "class", className, "id", idValue));
        return out;
    }
}

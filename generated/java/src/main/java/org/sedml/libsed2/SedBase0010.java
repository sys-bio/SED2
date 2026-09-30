package org.sedml.libsed2;

/*
 * SEDBase-0010 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0010.md):
 * A label index in a reference must name one of the labels of the dimension it indexes.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0010.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0010 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0010 {
    private SedBase0010() {}

    /** dimsBefore is the pre-index dimensions list, or null when the target's
     * dimension count itself isn't static (see SedBase0009) - in which case
     * there's nothing to check a label index against at all. Only checks index
     * positions that fall within dimsBefore's own length; a label index beyond
     * it is SEDBase-0009's concern, not this rule's, so it's skipped here
     * rather than double-firing. */
    public static List<ValidationProblem> check(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (dimsBefore == null) return out;
        for (int i = 0; i < indexAccessors.size(); i++) {
            RefIndex idx = indexAccessors.get(i);
            if (!idx.kind.equals("label") || i >= dimsBefore.size()) continue;
            List<String> labels = dimsBefore.get(i).labels;
            if (labels == null) continue;   // SEDBase-0010.md: "Only fires when that dimension's labels are static"
            if (!labels.contains(idx.label)) {
                out.add(RuleCatalog.problem("SEDBase-0010", location, "attr", attr, "value", value,
                        "subvalue", idx.label, "class", className, "id", idValue,
                        "allowed", String.join(", ", labels)));
            }
        }
        return out;
    }
}

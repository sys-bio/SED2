package org.sedml.libsed2;

/*
 * ParameterScan-0007 (specsheets/tasks/ParameterScan/v1.0.0/validation/ParameterScan-0007.md):
 * The entries of a ParameterScan's parameterRanges must have pairwise distinct modelElement values.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/ParameterScan-0007.py, and, like it, only for
 * a spec tree whose own rule set actually defines ParameterScan-0007 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class ParameterScan0007 {
    private ParameterScan0007() {}

    /** The dispatcher (References.checkParameterScanRanges) has already
     * reduced each entry of parameterRanges to its modelElement string, in
     * order: the literal text, or the string a reference to a constant
     * resolves to. An entry whose modelElement is missing, is not a string,
     * or is a reference that does not resolve to a string is passed as null
     * and ignored here (the schema and reference rules report those). One
     * problem per distinct value that appears more than once, in order of
     * first appearance, located at the second entry that has the value
     * (location/index/modelElement; `location` is the parameterRanges list
     * itself) so that two different duplicated values never share a
     * location, which validate() would collapse into one problem.
     * Comparison is exact (case-sensitive). */
    public static List<ValidationProblem> check(List<String> modelElements, String className, String idValue,
                                                String location) {
        Map<String, Integer> seen = new HashMap<>();
        List<ValidationProblem> out = new ArrayList<>();
        for (int index = 0; index < modelElements.size(); index++) {
            String element = modelElements.get(index);
            if (element == null) continue;
            if (seen.merge(element, 1, Integer::sum) == 2) {
                out.add(RuleCatalog.problem("ParameterScan-0007", location + "/" + index + "/modelElement",
                        "value", element, "class", className, "id", idValue));
            }
        }
        return out;
    }
}

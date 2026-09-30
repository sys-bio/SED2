package org.sed2test;

/*
 * SEDBase-0014 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0014.md):
 * An integer or range index into a dimension whose size is sourced as runtime and documents a min should warn when the index requires more entries than min guarantees.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0014.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0014 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0014 {
    private SedBase0014() {}

    /** dimsBefore is the pre-index dimensions list, or null when the target's
     * dimension count itself isn't static. Per-dimension: only fires when that
     * dimension's own "source" is "runtime" AND it carries a "min"
     * (SEDBase-0014.md) - the complement of SEDBase-0011's own guard (which
     * needs a concrete size, never present here), so the two rules never both
     * fire for the same index. A bare index n needs min > n (this also
     * naturally never fires for a negative n, since min is always >= 0). A
     * range [a:b] only checks the given end b (SEDBase-0014.md: "a range
     * [a:b] needs min >= b" - silent on a and on an open-ended b), so this
     * only fires when b is an explicit, non-negative value. */
    public static List<ValidationProblem> check(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (dimsBefore == null) return out;
        for (int i = 0; i < indexAccessors.size(); i++) {
            if (i >= dimsBefore.size()) continue;
            Dim dim = dimsBefore.get(i);
            if (!"runtime".equals(dim.source) || dim.min == null) continue;
            long m = dim.min;
            RefIndex idx = indexAccessors.get(i);
            if (idx.kind.equals("int")) {
                if (!(m > idx.intValue)) {
                    out.add(RuleCatalog.problem("SEDBase-0014", location, "attr", attr, "value", value,
                            "subvalue", idx.intText, "class", className, "id", idValue, "min", m));
                }
            } else if (idx.kind.equals("range")) {
                Long a = idx.rangeStart, b = idx.rangeEnd;
                if (b != null && b >= 0 && !(m >= b)) {
                    out.add(RuleCatalog.problem("SEDBase-0014", location, "attr", attr, "value", value,
                            "subvalue", "[" + (idx.rangeStartText == null ? "" : idx.rangeStartText) + ":" + idx.rangeEndText + "]",
                            "class", className, "id", idValue, "min", m));
                }
            }
        }
        return out;
    }
}

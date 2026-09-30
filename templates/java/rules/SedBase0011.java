package org.sed2test;

/*
 * SEDBase-0011 (specsheets/core/SEDBase/v1.0.0/validation/SEDBase-0011.md):
 * An integer or range index in a reference must fall within the size of the dimension it indexes.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDBase-0011.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDBase-0011 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedBase0011 {
    private SedBase0011() {}

    /** dimsBefore is the pre-index dimensions list, or null when the target's
     * dimension count itself isn't static. Per-dimension: only fires when THAT
     * dimension's own size resolved to a concrete number (SEDBase-0011.md:
     * "Only fires when that dimension's size is 'static' and computable"; a
     * size sourced as runtime/input-file resolves to null and is SEDBase-0014's
     * concern instead). Negative indices count from the end (Python-style):
     * for size n, legal integer indices are -n..n-1; for a range [a:b], BOTH
     * given ends must lie within -n..n (note the wider n, not n-1 - a range
     * end can equal n), and the range must select at least one element once
     * open ends are filled in as 0/n and negative ends are normalized. */
    public static List<ValidationProblem> check(List<Dim> dimsBefore, List<RefIndex> indexAccessors, String value,
                                                String className, String idValue, String attr, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        if (dimsBefore == null) return out;
        for (int i = 0; i < indexAccessors.size(); i++) {
            if (i >= dimsBefore.size()) continue;
            Long size = dimsBefore.get(i).size;
            if (size == null) continue;
            long n = size;
            RefIndex idx = indexAccessors.get(i);
            if (idx.kind.equals("int")) {
                if (idx.intValue < -n || idx.intValue > n - 1) {
                    out.add(RuleCatalog.problem("SEDBase-0011", location, "attr", attr, "value", value,
                            "subvalue", idx.intText, "class", className, "id", idValue,
                            "min", -n, "max", n - 1));
                }
            } else if (idx.kind.equals("range")) {
                Long a = idx.rangeStart, b = idx.rangeEnd;
                boolean bad = false;
                if (a != null && !(-n <= a && a <= n)) bad = true;
                if (b != null && !(-n <= b && b <= n)) bad = true;
                if (!bad) {
                    long ea = a != null ? a : 0;
                    long eb = b != null ? b : n;
                    if (ea < 0) ea += n;
                    if (eb < 0) eb += n;
                    if (ea >= eb) bad = true;
                }
                if (bad) {
                    out.add(RuleCatalog.problem("SEDBase-0011", location, "attr", attr, "value", value,
                            "subvalue", idx.rangeText(), "class", className, "id", idValue,
                            "min", -n, "max", n - 1));
                }
            }
        }
        return out;
    }
}

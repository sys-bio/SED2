package org.sed2test;

/*
 * SEDDocument-0010 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0010.md):
 * A <prefix>@version attribute should not be declared for a namespace the document never uses.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDDocument-0010.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDDocument-0010 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedDocument0010 {
    private SedDocument0010() {}

    /** Called once per declared-but-unused prefix - the caller
     * (References.checkNamespaceUsageAndVersion) has already confirmed
     * `prefix` has a "<prefix>@version" declared on the document but no usage
     * site anywhere in the document tree; `location` is the declaration's own
     * JSON pointer ("/<prefix>@version"). */
    public static List<ValidationProblem> check(String prefix, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        out.add(RuleCatalog.problem("SEDDocument-0010", location, "prefix", prefix, "attr", prefix + "@version"));
        return out;
    }
}

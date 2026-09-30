package org.sed2test;

/*
 * SEDDocument-0009 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0009.md):
 * For every namespace prefix used anywhere in the document, SEDDocument must declare a <prefix>@version attribute.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDDocument-0009.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDDocument-0009 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import java.util.ArrayList;
import java.util.List;

public final class SedDocument0009 {
    private SedDocument0009() {}

    /** Called once per usage site of an undeclared-version namespace prefix (an
     * attribute key or _type value of the form prefix@identifier) - the caller
     * (References.checkNamespaceUsageAndVersion, a whole-document scan) has
     * already determined `prefix` has no matching "<prefix>@version" on the
     * document and found this one `location` where it's used; `location` is
     * that usage's own JSON pointer, not the (missing) declaration's. */
    public static List<ValidationProblem> check(String prefix, String location) {
        List<ValidationProblem> out = new ArrayList<>();
        out.add(RuleCatalog.problem("SEDDocument-0009", location, "prefix", prefix));
        return out;
    }
}

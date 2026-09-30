package org.sedml.libsed2;

/*
 * SEDDocument-0013 (specsheets/core/SEDDocument/v1.0.0/validation/SEDDocument-0013.md):
 * A constant may only reference constants that appear before it in the constants dictionary.
 *
 * Hand-written rule template, copied verbatim (only this file's leading
 * `package ...;` line is rewritten to match --java-package) into the
 * generated package by generator/emit_java.py's _copy_handwritten_rules_java
 * - the Java analog of templates/python/rules/SEDDocument-0013.py, and, like it, only for
 * a spec tree whose own rule set actually defines SEDDocument-0013 (a tree that doesn't,
 * such as test-specsheets/, gets a no-op in the generated Handwritten
 * facade instead). Fixed convention: one final class named from the rule ID
 * with one static `check` method returning the (possibly empty) list of
 * violations; the shared dispatcher in References.java (the Python target's
 * RUNTIME) decides when to call it and with what.
 */

import com.fasterxml.jackson.databind.JsonNode;

import java.util.ArrayList;
import java.util.List;

public final class SedDocument0013 {
    private SedDocument0013() {}

    /** `constants` is the document's own constants collection (null when the
     * document class has none). Only a constant whose own value IS a reference
     * (AnyValueOrRef's SIdRef-substitution case) is in scope; a plain JSON
     * value constant has nothing to check. A reference that isn't even shaped
     * like '#constants:...', or whose target constant doesn't precede this one
     * in the document's own insertion order (including one that doesn't exist
     * as a constant at all, or names this same constant) is "not an earlier
     * constant" by this rule's own wording, without a separate resolution
     * check first. */
    public static List<ValidationProblem> check(IdCollection constants) {
        List<ValidationProblem> out = new ArrayList<>();
        if (constants == null) return out;
        List<String> ids = constants.ids();
        for (int i = 0; i < ids.size(); i++) {
            String cid = ids.get(i);
            Object v = constants.getObject(cid);
            if (!(v instanceof JsonNode) || !References.isReference((JsonNode) v)) continue;
            String value = ((JsonNode) v).textValue();
            ParsedReference parsed = References.parse(value);
            if (!"constants".equals(parsed.collection) || parsed.path.isEmpty()) continue;
            String target = parsed.path.get(0);
            if (!ids.subList(0, i).contains(target)) {
                out.add(RuleCatalog.problem("SEDDocument-0013", "/constants/" + cid, "attr", cid, "value", value));
            }
        }
        return out;
    }
}

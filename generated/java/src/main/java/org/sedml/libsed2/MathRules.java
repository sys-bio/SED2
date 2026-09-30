package org.sedml.libsed2;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Types-0001..0004: the shared math-grammar rules any field with
 * FieldSpec.isMath (x-math) runs on its own literal string value - see
 * SedBase.validateOwn(). GENERATED - do not hand-edit; regenerate via
 * generator/generate.py. */
public final class MathRules {
    private MathRules() {}

    /** value is the field's own raw string - never a reference: SedBase's
     * validateOwn() only calls here for a literal string value (Types-
     * 0001.md: "When the math attribute is itself a reference, ... apply
     * only if the reference resolves statically to a string constant" -
     * not implemented by either target: a reference-form value goes to the
     * reference rules instead). Returns [] if value parses and every function
     * call / bare identifier it contains checks out; otherwise one
     * ValidationProblem per violation (Types-0001 short-circuits the rest,
     * same as emit_python.py's _check_math_field - an unparseable
     * expression has no tree left to walk for 0002-0004). */
    public static List<ValidationProblem> checkMathField(
            String value, String className, String idValue, String attr, String location) {
        List<ValidationProblem> problems = new ArrayList<>();
        MathAst.Node ast;
        try {
            ast = MathAst.parse(value);
        } catch (MathAst.MathSyntaxError e) {
            Map<String, Object> ph = new HashMap<>();
            ph.put("attr", attr);
            ph.put("class", className);
            ph.put("id", idValue);
            ph.put("expr", value);
            ph.put("parse-message", e.getMessage());
            problems.add(RuleCatalog.makeProblem("Types-0001", location, ph));
            return problems;
        }
        if (Handwritten.HAS_REFERENCE_RULES) {
            // SEDBase-0005.md: the root-collection rule also applies to a
            // REFERENCE token embedded in a math string.
            for (MathAst.Node node : ast.walk()) {
                if (node.isReference()) {
                    problems.addAll(Handwritten.sedBase0005(
                            References.parse(node.text), className, idValue, attr, location));
                }
            }
        }
        for (MathAst.Node node : ast.walk()) {
            if (node.isFunctionCall() && !PredefinedFunctions.FUNCTIONS.containsKey(node.name)) {
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", attr);
                ph.put("class", className);
                ph.put("id", idValue);
                ph.put("function", node.name);
                problems.add(RuleCatalog.makeProblem("Types-0002", location, ph));
            }
        }
        for (MathAst.Node node : ast.walk()) {
            if (!node.isFunctionCall()) continue;
            PredefinedFunctions.Arity spec = PredefinedFunctions.FUNCTIONS.get(node.name);
            if (spec == null) continue;  // Types-0002's concern, not a duplicate diagnosis here
            int count = node.getNumChildren();
            if (!spec.ok(count)) {
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", attr);
                ph.put("class", className);
                ph.put("id", idValue);
                ph.put("function", node.name);
                ph.put("count", count);
                ph.put("expected-count", spec.format());
                problems.add(RuleCatalog.makeProblem("Types-0003", location, ph));
            }
        }
        for (MathAst.Node node : ast.walk()) {
            if (node.isName() && !PredefinedFunctions.CONSTANTS.contains(node.name)) {
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", attr);
                ph.put("class", className);
                ph.put("id", idValue);
                ph.put("value", node.name);
                problems.add(RuleCatalog.makeProblem("Types-0004", location, ph));
            }
        }
        return problems;
    }
}

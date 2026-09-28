package org.sed2test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

/** Compiled math function/constant registry for Types-0002/-0003/-0004's
 * math-grammar checks (mirrors generator/emit_python.py's
 * emit_predefined_functions_py / _predefined_functions.py). GENERATED
 * from schema/predefined-functions.json by generator/generate.py - do
 * not hand-edit. */
public final class PredefinedFunctions {
    private PredefinedFunctions() {}

    /** ('set', {2, 4}) for a fixed handful of allowed argument counts
     * (an exact arity normalizes to a one-element set), or ('range', min,
     * max) with max possibly null for unbounded (e.g. min/max/sum's
     * {"min": 1, "max": null}) - same two-shape contract as
     * emit_python.py's _normalize_arity / templates/python/rules/
     * Types-0003.py's _arity_ok/_format_arity. */
    public static final class Arity {
        public final boolean isRange;
        public final Set<Integer> values;  // set only
        public final int min;              // range only
        public final Integer max;          // range only; null = unbounded

        private Arity(boolean isRange, Set<Integer> values, int min, Integer max) {
            this.isRange = isRange;
            this.values = values;
            this.min = min;
            this.max = max;
        }

        static Arity ofSet(int... vals) {
            Set<Integer> s = new TreeSet<>();
            for (int v : vals) s.add(v);
            return new Arity(false, s, 0, null);
        }

        static Arity ofRange(int lo, Integer hi) {
            return new Arity(true, null, lo, hi);
        }

        public boolean ok(int count) {
            if (!isRange) return values.contains(count);
            return count >= min && (max == null || count <= max);
        }

        /** Renders this arity for a {expected-count} placeholder -
         * "2 or 4", "1", "1 or more", "2 to 4". */
        public String format() {
            if (!isRange) {
                List<String> parts = new ArrayList<>();
                for (int v : values) parts.add(String.valueOf(v));
                return String.join(" or ", parts);
            }
            if (max == null) return min + " or more";
            if (min == max) return String.valueOf(min);
            return min + " to " + max;
        }
    }

    public static final Map<String, Arity> FUNCTIONS = new HashMap<>();
    public static final Set<String> CONSTANTS = new HashSet<>(Arrays.asList(
        "exponentiale", "false", "infinity", "notanumber", "pi", "true"
    ));

    static {
        FUNCTIONS.put("abs", Arity.ofSet(1));
        FUNCTIONS.put("and", Arity.ofRange(0, null));
        FUNCTIONS.put("arccos", Arity.ofSet(1));
        FUNCTIONS.put("arccosh", Arity.ofSet(1));
        FUNCTIONS.put("arccot", Arity.ofSet(1));
        FUNCTIONS.put("arccoth", Arity.ofSet(1));
        FUNCTIONS.put("arccsc", Arity.ofSet(1));
        FUNCTIONS.put("arccsch", Arity.ofSet(1));
        FUNCTIONS.put("arcsec", Arity.ofSet(1));
        FUNCTIONS.put("arcsech", Arity.ofSet(1));
        FUNCTIONS.put("arcsin", Arity.ofSet(1));
        FUNCTIONS.put("arcsinh", Arity.ofSet(1));
        FUNCTIONS.put("arctan", Arity.ofSet(1));
        FUNCTIONS.put("arctanh", Arity.ofSet(1));
        FUNCTIONS.put("bernoulli", Arity.ofSet(1));
        FUNCTIONS.put("binomial", Arity.ofSet(2, 4));
        FUNCTIONS.put("cauchy", Arity.ofSet(1, 2, 4));
        FUNCTIONS.put("ceiling", Arity.ofSet(1));
        FUNCTIONS.put("chisquare", Arity.ofSet(1, 3));
        FUNCTIONS.put("cos", Arity.ofSet(1));
        FUNCTIONS.put("cosh", Arity.ofSet(1));
        FUNCTIONS.put("cot", Arity.ofSet(1));
        FUNCTIONS.put("coth", Arity.ofSet(1));
        FUNCTIONS.put("csc", Arity.ofSet(1));
        FUNCTIONS.put("csch", Arity.ofSet(1));
        FUNCTIONS.put("eq", Arity.ofRange(2, null));
        FUNCTIONS.put("exp", Arity.ofSet(1));
        FUNCTIONS.put("exponential", Arity.ofSet(1, 3));
        FUNCTIONS.put("factorial", Arity.ofSet(1));
        FUNCTIONS.put("floor", Arity.ofSet(1));
        FUNCTIONS.put("gamma", Arity.ofSet(2, 4));
        FUNCTIONS.put("geq", Arity.ofRange(2, null));
        FUNCTIONS.put("gt", Arity.ofRange(2, null));
        FUNCTIONS.put("implies", Arity.ofSet(2));
        FUNCTIONS.put("laplace", Arity.ofSet(1, 2, 4));
        FUNCTIONS.put("leq", Arity.ofRange(2, null));
        FUNCTIONS.put("ln", Arity.ofSet(1));
        FUNCTIONS.put("log", Arity.ofSet(1, 2));
        FUNCTIONS.put("lognormal", Arity.ofSet(2, 4));
        FUNCTIONS.put("lt", Arity.ofRange(2, null));
        FUNCTIONS.put("max", Arity.ofRange(1, null));
        FUNCTIONS.put("min", Arity.ofRange(1, null));
        FUNCTIONS.put("neq", Arity.ofSet(2));
        FUNCTIONS.put("normal", Arity.ofSet(2, 4));
        FUNCTIONS.put("not", Arity.ofSet(1));
        FUNCTIONS.put("or", Arity.ofRange(0, null));
        FUNCTIONS.put("piecewise", Arity.ofRange(1, null));
        FUNCTIONS.put("poisson", Arity.ofSet(1, 3));
        FUNCTIONS.put("quotient", Arity.ofSet(2));
        FUNCTIONS.put("rayleigh", Arity.ofSet(1, 3));
        FUNCTIONS.put("rem", Arity.ofSet(2));
        FUNCTIONS.put("root", Arity.ofSet(1, 2));
        FUNCTIONS.put("sec", Arity.ofSet(1));
        FUNCTIONS.put("sech", Arity.ofSet(1));
        FUNCTIONS.put("sin", Arity.ofSet(1));
        FUNCTIONS.put("sinh", Arity.ofSet(1));
        FUNCTIONS.put("sum", Arity.ofSet(1));
        FUNCTIONS.put("tan", Arity.ofSet(1));
        FUNCTIONS.put("tanh", Arity.ofSet(1));
        FUNCTIONS.put("uniform", Arity.ofSet(2));
        FUNCTIONS.put("xor", Arity.ofRange(0, null));
    }
}


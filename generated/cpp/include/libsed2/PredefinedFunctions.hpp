#pragma once

#include <algorithm>
#include <map>
#include <optional>
#include <set>
#include <string>
#include <vector>

/* Compiled math function/constant registry for Types-0002/-0003/-0004's
 * math-grammar checks (mirrors generator/emit_python.py's
 * emit_predefined_functions_py / emit_java.py's
 * emit_predefined_functions_java). GENERATED from
 * schema/predefined-functions.json by generator/generate.py - do not
 * hand-edit; regenerate via generator/generate.py. */
namespace libsed2 {

class PredefinedFunctions {
public:
    /// ('set', {2, 4}) for a fixed handful of allowed argument counts
    /// (an exact arity normalizes to a one-element set), or ('range', min,
    /// max) with max possibly nullopt for unbounded (e.g. min/max/sum's
    /// {"min": 1, "max": null}) - same two-shape contract as
    /// emit_python.py's _normalize_arity / templates/python/rules/
    /// Types-0003.py's _arity_ok/_format_arity.
    class Arity {
    public:
        bool is_range;
        std::set<int> values;         // set only
        int min = 0;                  // range only
        std::optional<int> max;       // range only; nullopt = unbounded

        static Arity of_set(std::set<int> vals) {
            Arity a; a.is_range = false; a.values = std::move(vals); return a;
        }

        static Arity of_range(int lo, std::optional<int> hi) {
            Arity a; a.is_range = true; a.min = lo; a.max = hi; return a;
        }

        bool ok(int count) const {
            if (!is_range) return values.count(count) > 0;
            return count >= min && (!max || count <= *max);
        }

        /// Renders this arity for a {expected-count} placeholder -
        /// "2 or 4", "1", "1 or more", "2 to 4".
        std::string format() const {
            if (!is_range) {
                std::string out;
                bool first = true;
                for (int v : values) {
                    if (!first) out += " or ";
                    out += std::to_string(v);
                    first = false;
                }
                return out;
            }
            if (!max) return std::to_string(min) + " or more";
            if (min == *max) return std::to_string(min);
            return std::to_string(min) + " to " + std::to_string(*max);
        }
    };

    static const std::map<std::string, Arity>& functions() {
        static const std::map<std::string, Arity> m = [] {
            std::map<std::string, Arity> m;
        m.emplace("abs", Arity::of_set({1}));
        m.emplace("and", Arity::of_range(0, std::nullopt));
        m.emplace("arccos", Arity::of_set({1}));
        m.emplace("arccosh", Arity::of_set({1}));
        m.emplace("arccot", Arity::of_set({1}));
        m.emplace("arccoth", Arity::of_set({1}));
        m.emplace("arccsc", Arity::of_set({1}));
        m.emplace("arccsch", Arity::of_set({1}));
        m.emplace("arcsec", Arity::of_set({1}));
        m.emplace("arcsech", Arity::of_set({1}));
        m.emplace("arcsin", Arity::of_set({1}));
        m.emplace("arcsinh", Arity::of_set({1}));
        m.emplace("arctan", Arity::of_set({1}));
        m.emplace("arctanh", Arity::of_set({1}));
        m.emplace("bernoulli", Arity::of_set({1}));
        m.emplace("binomial", Arity::of_set({2, 4}));
        m.emplace("cauchy", Arity::of_set({1, 2, 4}));
        m.emplace("ceiling", Arity::of_set({1}));
        m.emplace("chisquare", Arity::of_set({1, 3}));
        m.emplace("cos", Arity::of_set({1}));
        m.emplace("cosh", Arity::of_set({1}));
        m.emplace("cot", Arity::of_set({1}));
        m.emplace("coth", Arity::of_set({1}));
        m.emplace("csc", Arity::of_set({1}));
        m.emplace("csch", Arity::of_set({1}));
        m.emplace("eq", Arity::of_range(2, std::nullopt));
        m.emplace("exp", Arity::of_set({1}));
        m.emplace("exponential", Arity::of_set({1, 3}));
        m.emplace("factorial", Arity::of_set({1}));
        m.emplace("floor", Arity::of_set({1}));
        m.emplace("gamma", Arity::of_set({2, 4}));
        m.emplace("geq", Arity::of_range(2, std::nullopt));
        m.emplace("gt", Arity::of_range(2, std::nullopt));
        m.emplace("implies", Arity::of_set({2}));
        m.emplace("laplace", Arity::of_set({1, 2, 4}));
        m.emplace("leq", Arity::of_range(2, std::nullopt));
        m.emplace("ln", Arity::of_set({1}));
        m.emplace("log", Arity::of_set({1, 2}));
        m.emplace("lognormal", Arity::of_set({2, 4}));
        m.emplace("lt", Arity::of_range(2, std::nullopt));
        m.emplace("max", Arity::of_range(1, std::nullopt));
        m.emplace("min", Arity::of_range(1, std::nullopt));
        m.emplace("neq", Arity::of_set({2}));
        m.emplace("normal", Arity::of_set({2, 4}));
        m.emplace("not", Arity::of_set({1}));
        m.emplace("or", Arity::of_range(0, std::nullopt));
        m.emplace("piecewise", Arity::of_range(1, std::nullopt));
        m.emplace("poisson", Arity::of_set({1, 3}));
        m.emplace("quotient", Arity::of_set({2}));
        m.emplace("rayleigh", Arity::of_set({1, 3}));
        m.emplace("rem", Arity::of_set({2}));
        m.emplace("root", Arity::of_set({1, 2}));
        m.emplace("sec", Arity::of_set({1}));
        m.emplace("sech", Arity::of_set({1}));
        m.emplace("sin", Arity::of_set({1}));
        m.emplace("sinh", Arity::of_set({1}));
        m.emplace("sum", Arity::of_set({1}));
        m.emplace("tan", Arity::of_set({1}));
        m.emplace("tanh", Arity::of_set({1}));
        m.emplace("uniform", Arity::of_set({2}));
        m.emplace("xor", Arity::of_range(0, std::nullopt));
            return m;
        }();
        return m;
    }

    static const std::set<std::string>& constants() {
        static const std::set<std::string> s = {"exponentiale", "false", "infinity", "notanumber", "pi", "true"};
        return s;
    }
};

}  // namespace libsed2

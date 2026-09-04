#include "sed2/math/FunctionTable.h"

namespace sed2 {

namespace {

const std::vector<std::string> kConstants = {
    "pi", "exponentiale", "avogadro", "true", "false", "notanumber", "infinity", "time",
};

const std::vector<FunctionSignature> kFunctions = {
    // MathML core functions, as used by libsbml's ASTNode.
    {"abs", 1, 1}, {"ceiling", 1, 1}, {"floor", 1, 1},
    {"exp", 1, 1}, {"ln", 1, 1}, {"log", 1, 2}, {"log10", 1, 1},
    {"power", 2, 2}, {"root", 1, 2}, {"factorial", 1, 1},
    {"sin", 1, 1}, {"cos", 1, 1}, {"tan", 1, 1},
    {"sec", 1, 1}, {"csc", 1, 1}, {"cot", 1, 1},
    {"sinh", 1, 1}, {"cosh", 1, 1}, {"tanh", 1, 1},
    {"sech", 1, 1}, {"csch", 1, 1}, {"coth", 1, 1},
    {"arcsin", 1, 1}, {"arccos", 1, 1}, {"arctan", 1, 1},
    {"arcsec", 1, 1}, {"arccsc", 1, 1}, {"arccot", 1, 1},
    {"arcsinh", 1, 1}, {"arccosh", 1, 1}, {"arctanh", 1, 1},
    {"arcsech", 1, 1}, {"arccsch", 1, 1}, {"arccoth", 1, 1},
    {"min", 1, -1}, {"max", 1, -1}, {"rem", 2, 2}, {"quotient", 2, 2},
    {"plus", 0, -1}, {"times", 0, -1},
    {"and", 0, -1}, {"or", 0, -1}, {"not", 1, 1}, {"xor", 0, -1},
    {"eq", 2, -1}, {"neq", 2, 2}, {"gt", 2, -1}, {"lt", 2, -1}, {"geq", 2, -1}, {"leq", 2, -1},
    {"piecewise", 1, -1}, {"delay", 2, 2}, {"selector", 2, -1},
    // SBML 'distrib' package distribution functions.
    {"normal", 2, 4}, {"uniform", 2, 2}, {"bernoulli", 1, 1},
    {"binomial", 2, 4}, {"cauchy", 2, 4}, {"chisquare", 1, 3},
    {"exponential", 1, 3}, {"gamma", 2, 4}, {"laplace", 2, 4},
    {"lognormal", 2, 4}, {"poisson", 1, 3}, {"rayleigh", 1, 3}, {"weibull", 2, 4},
};

}  // namespace

const std::vector<std::string>& predefinedConstants() { return kConstants; }
const std::vector<FunctionSignature>& predefinedFunctions() { return kFunctions; }

bool isPredefinedConstant(const std::string& name) {
    for (const auto& c : kConstants) {
        if (c == name) return true;
    }
    return false;
}

bool isPredefinedFunction(const std::string& name) {
    for (const auto& f : kFunctions) {
        if (f.name == name) return true;
    }
    return false;
}

}  // namespace sed2

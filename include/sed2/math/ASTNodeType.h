#pragma once

namespace sed2 {

enum class ASTNodeType {
    Number,      // a literal numeric constant, e.g. 1.3
    Reference,   // a #hash-reference, e.g. #tasks:sim1.model['S1']
    Identifier,  // a bare name: a predefined constant (pi) or a plain symbol
    Operator,    // +, -, *, /, ^, or unary minus ("u-")
    Function,    // a named function call, e.g. sin(x), normal(mu, sigma)
};

}  // namespace sed2

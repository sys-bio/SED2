#pragma once

#include <memory>
#include <string>

#include "sed2/math/ASTNode.h"
#include "sed2/math/Lexer.h"

namespace sed2 {

// Hand-written recursive-descent / precedence-climbing parser for SED2's
// infix math strings (Design.md, "Math": inspired by libsbml's bison 'l3'
// parser, but hand-written here to avoid a flex/bison build dependency -
// see Lexer.h for why). Grammar (highest to lowest precedence):
//   primary       := NUMBER | REFERENCE | IDENTIFIER ['(' args ')'] | '(' expression ')'
//   power         := primary ('^' unary)?              // right-associative
//   unary         := '-' unary | power
//   multiplicative:= unary (('*' | '/') unary)*
//   additive      := multiplicative (('+' | '-') multiplicative)*
//   expression    := additive
class Parser {
public:
    // Parses 'expression' fully. On success, returns the resulting tree;
    // on failure (a lexical error, or leftover/unexpected tokens), returns
    // nullptr and, if 'errorMessage' is non-null, explains why in it.
    static std::unique_ptr<ASTNode> parse(const std::string& expression, std::string* errorMessage = nullptr);

private:
    explicit Parser(std::string expression);

    std::unique_ptr<ASTNode> parseExpression();
    std::unique_ptr<ASTNode> parseAdditive();
    std::unique_ptr<ASTNode> parseMultiplicative();
    std::unique_ptr<ASTNode> parseUnary();
    std::unique_ptr<ASTNode> parsePower();
    std::unique_ptr<ASTNode> parsePrimary();

    bool fail(const std::string& message);

    Lexer lexer_;
    bool failed_ = false;
    std::string errorMessage_;
};

}  // namespace sed2

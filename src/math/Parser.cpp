#include "sed2/math/Parser.h"

#include <utility>

namespace sed2 {

std::unique_ptr<ASTNode> Parser::parse(const std::string& expression, std::string* errorMessage) {
    Parser parser(expression);
    auto tree = parser.parseExpression();
    if (!parser.failed_ && tree && parser.lexer_.peek().type != TokenType::End) {
        parser.fail("Unexpected trailing input in expression");
        tree.reset();
    }
    if (parser.failed_) {
        if (errorMessage) *errorMessage = parser.errorMessage_;
        return nullptr;
    }
    return tree;
}

Parser::Parser(std::string expression) : lexer_(std::move(expression)) {}

bool Parser::fail(const std::string& message) {
    if (!failed_) {
        failed_ = true;
        errorMessage_ = message;
    }
    return false;
}

std::unique_ptr<ASTNode> Parser::parseExpression() { return parseAdditive(); }

std::unique_ptr<ASTNode> Parser::parseAdditive() {
    auto left = parseMultiplicative();
    if (!left) return nullptr;
    while (!failed_) {
        const Token& token = lexer_.peek();
        if (token.type != TokenType::Operator || (token.text != "+" && token.text != "-")) break;
        std::string op = token.text;
        lexer_.next();
        auto right = parseMultiplicative();
        if (!right) return nullptr;
        auto node = std::make_unique<ASTNode>(ASTNodeType::Operator);
        node->setName(op);
        node->addChild(std::move(left));
        node->addChild(std::move(right));
        left = std::move(node);
    }
    return left;
}

std::unique_ptr<ASTNode> Parser::parseMultiplicative() {
    auto left = parseUnary();
    if (!left) return nullptr;
    while (!failed_) {
        const Token& token = lexer_.peek();
        if (token.type != TokenType::Operator || (token.text != "*" && token.text != "/")) break;
        std::string op = token.text;
        lexer_.next();
        auto right = parseUnary();
        if (!right) return nullptr;
        auto node = std::make_unique<ASTNode>(ASTNodeType::Operator);
        node->setName(op);
        node->addChild(std::move(left));
        node->addChild(std::move(right));
        left = std::move(node);
    }
    return left;
}

std::unique_ptr<ASTNode> Parser::parseUnary() {
    const Token& token = lexer_.peek();
    if (token.type == TokenType::Operator && token.text == "-") {
        lexer_.next();
        auto operand = parseUnary();
        if (!operand) return nullptr;
        auto node = std::make_unique<ASTNode>(ASTNodeType::Operator);
        node->setName("u-");
        node->addChild(std::move(operand));
        return node;
    }
    return parsePower();
}

std::unique_ptr<ASTNode> Parser::parsePower() {
    auto base = parsePrimary();
    if (!base) return nullptr;
    const Token& token = lexer_.peek();
    if (token.type == TokenType::Operator && token.text == "^") {
        lexer_.next();
        auto exponent = parseUnary();  // right-associative; also allows e.g. 2^-1
        if (!exponent) return nullptr;
        auto node = std::make_unique<ASTNode>(ASTNodeType::Operator);
        node->setName("^");
        node->addChild(std::move(base));
        node->addChild(std::move(exponent));
        return node;
    }
    return base;
}

std::unique_ptr<ASTNode> Parser::parsePrimary() {
    Token token = lexer_.next();
    switch (token.type) {
        case TokenType::Number: {
            auto node = std::make_unique<ASTNode>(ASTNodeType::Number);
            node->setNumberValue(token.numberValue);
            return node;
        }
        case TokenType::Reference: {
            auto node = std::make_unique<ASTNode>(ASTNodeType::Reference);
            node->setReferenceText(token.text);
            return node;
        }
        case TokenType::Identifier: {
            if (lexer_.peek().type == TokenType::LParen) {
                lexer_.next();  // consume '('
                auto node = std::make_unique<ASTNode>(ASTNodeType::Function);
                node->setName(token.text);
                if (lexer_.peek().type != TokenType::RParen) {
                    while (true) {
                        auto arg = parseExpression();
                        if (!arg) return nullptr;
                        node->addChild(std::move(arg));
                        if (lexer_.peek().type == TokenType::Comma) {
                            lexer_.next();
                            continue;
                        }
                        break;
                    }
                }
                if (lexer_.peek().type != TokenType::RParen) {
                    fail("Expected ')' to close call to '" + token.text + "'");
                    return nullptr;
                }
                lexer_.next();  // consume ')'
                return node;
            }
            auto node = std::make_unique<ASTNode>(ASTNodeType::Identifier);
            node->setName(token.text);
            return node;
        }
        case TokenType::LParen: {
            auto inner = parseExpression();
            if (!inner) return nullptr;
            if (lexer_.peek().type != TokenType::RParen) {
                fail("Expected ')'");
                return nullptr;
            }
            lexer_.next();  // consume ')'
            return inner;
        }
        case TokenType::Error:
            fail("Unrecognized character '" + token.text + "' in expression");
            return nullptr;
        default:
            fail("Unexpected end of expression");
            return nullptr;
    }
}

}  // namespace sed2

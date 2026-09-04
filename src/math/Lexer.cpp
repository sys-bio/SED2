#include "sed2/math/Lexer.h"

#include <cctype>
#include <cstdlib>
#include <utility>

#include "sed2/core/AttributeTypes.h"

namespace sed2 {

namespace {
bool isIdentStart(char c) { return std::isalpha(static_cast<unsigned char>(c)) != 0 || c == '_'; }
bool isIdentChar(char c) { return std::isalnum(static_cast<unsigned char>(c)) != 0 || c == '_'; }
bool isDigit(char c) { return std::isdigit(static_cast<unsigned char>(c)) != 0; }
}  // namespace

Lexer::Lexer(std::string input) : input_(std::move(input)) {}

Token Lexer::next() {
    if (hasPeeked_) {
        hasPeeked_ = false;
        return peeked_;
    }
    return lexOne();
}

const Token& Lexer::peek() {
    if (!hasPeeked_) {
        peeked_ = lexOne();
        hasPeeked_ = true;
    }
    return peeked_;
}

void Lexer::skipWhitespace() {
    while (pos_ < input_.size() && std::isspace(static_cast<unsigned char>(input_[pos_])) != 0) ++pos_;
}

Token Lexer::lexOne() {
    skipWhitespace();
    if (pos_ >= input_.size()) return Token{TokenType::End, "", 0.0};

    char c = input_[pos_];
    if (c == '#') return lexReference();
    if (isDigit(c) || (c == '.' && pos_ + 1 < input_.size() && isDigit(input_[pos_ + 1]))) return lexNumber();
    if (isIdentStart(c)) return lexIdentifier();

    if (c == '+' || c == '-' || c == '*' || c == '/' || c == '^') {
        ++pos_;
        return Token{TokenType::Operator, std::string(1, c), 0.0};
    }
    if (c == '(') {
        ++pos_;
        return Token{TokenType::LParen, "(", 0.0};
    }
    if (c == ')') {
        ++pos_;
        return Token{TokenType::RParen, ")", 0.0};
    }
    if (c == ',') {
        ++pos_;
        return Token{TokenType::Comma, ",", 0.0};
    }

    ++pos_;
    return Token{TokenType::Error, std::string(1, c), 0.0};
}

Token Lexer::lexNumber() {
    std::size_t start = pos_;
    while (pos_ < input_.size() && isDigit(input_[pos_])) ++pos_;
    if (pos_ < input_.size() && input_[pos_] == '.') {
        ++pos_;
        while (pos_ < input_.size() && isDigit(input_[pos_])) ++pos_;
    }
    if (pos_ < input_.size() && (input_[pos_] == 'e' || input_[pos_] == 'E')) {
        std::size_t expStart = pos_;
        std::size_t i = pos_ + 1;
        if (i < input_.size() && (input_[i] == '+' || input_[i] == '-')) ++i;
        std::size_t digitsStart = i;
        while (i < input_.size() && isDigit(input_[i])) ++i;
        if (i > digitsStart) {
            pos_ = i;
        } else {
            pos_ = expStart;  // no exponent digits: leave the 'e' for the next token
        }
    }

    std::string text = input_.substr(start, pos_ - start);
    Token token;
    token.type = TokenType::Number;
    token.text = text;
    token.numberValue = std::strtod(text.c_str(), nullptr);
    return token;
}

Token Lexer::lexReference() {
    auto length = scanReferenceLength(input_, pos_);
    if (!length.has_value()) {
        Token token;
        token.type = TokenType::Error;
        token.text = input_.substr(pos_, 1);
        ++pos_;
        return token;
    }
    Token token;
    token.type = TokenType::Reference;
    token.text = input_.substr(pos_, *length);
    pos_ += *length;
    return token;
}

Token Lexer::lexIdentifier() {
    std::size_t start = pos_;
    ++pos_;
    while (pos_ < input_.size() && isIdentChar(input_[pos_])) ++pos_;
    Token token;
    token.type = TokenType::Identifier;
    token.text = input_.substr(start, pos_ - start);
    return token;
}

}  // namespace sed2

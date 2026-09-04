#include <gtest/gtest.h>

#include "sed2/math/Lexer.h"

using sed2::Lexer;
using sed2::TokenType;

TEST(Lexer, Numbers) {
    Lexer lexer("1 1.3 .5 2e3 1.5e-2");
    EXPECT_DOUBLE_EQ(lexer.next().numberValue, 1.0);
    EXPECT_DOUBLE_EQ(lexer.next().numberValue, 1.3);
    EXPECT_DOUBLE_EQ(lexer.next().numberValue, 0.5);
    EXPECT_DOUBLE_EQ(lexer.next().numberValue, 2000.0);
    EXPECT_DOUBLE_EQ(lexer.next().numberValue, 0.015);
    EXPECT_EQ(lexer.next().type, TokenType::End);
}

TEST(Lexer, Reference) {
    Lexer lexer("#tasks:sim1.model['S1'] + 1");
    auto ref = lexer.next();
    ASSERT_EQ(ref.type, TokenType::Reference);
    EXPECT_EQ(ref.text, "#tasks:sim1.model['S1']");

    auto plus = lexer.next();
    EXPECT_EQ(plus.type, TokenType::Operator);
    EXPECT_EQ(plus.text, "+");

    EXPECT_DOUBLE_EQ(lexer.next().numberValue, 1.0);
}

TEST(Lexer, IdentifiersOperatorsAndPunctuation) {
    Lexer lexer("sin(x, pi) - 1");
    EXPECT_EQ(lexer.next().text, "sin");
    EXPECT_EQ(lexer.next().type, TokenType::LParen);
    EXPECT_EQ(lexer.next().text, "x");
    EXPECT_EQ(lexer.next().type, TokenType::Comma);
    EXPECT_EQ(lexer.next().text, "pi");
    EXPECT_EQ(lexer.next().type, TokenType::RParen);
    EXPECT_EQ(lexer.next().text, "-");
    EXPECT_DOUBLE_EQ(lexer.next().numberValue, 1.0);
}

TEST(Lexer, MalformedReferenceProducesErrorToken) {
    Lexer lexer("#");
    EXPECT_EQ(lexer.next().type, TokenType::Error);
}

TEST(Lexer, UnknownCharacterProducesErrorToken) {
    Lexer lexer("1 @ 2");
    EXPECT_EQ(lexer.next().type, TokenType::Number);
    EXPECT_EQ(lexer.next().type, TokenType::Error);
}

TEST(Lexer, PeekDoesNotAdvance) {
    Lexer lexer("42");
    EXPECT_EQ(lexer.peek().type, TokenType::Number);
    EXPECT_DOUBLE_EQ(lexer.next().numberValue, 42.0);
    EXPECT_EQ(lexer.next().type, TokenType::End);
}

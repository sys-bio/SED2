#include <gtest/gtest.h>

#include "sed2/math/Parser.h"

using sed2::ASTNodeType;
using sed2::Parser;

TEST(Parser, PrecedenceAndRoundTrip) {
    std::string error;
    auto tree = Parser::parse("1 + 2 * 3", &error);
    ASSERT_NE(tree, nullptr) << error;
    EXPECT_EQ(tree->getType(), ASTNodeType::Operator);
    EXPECT_EQ(tree->getName(), "+");
    ASSERT_EQ(tree->getNumChildren(), 2u);
    EXPECT_EQ(tree->getChild(1)->getName(), "*");
    EXPECT_EQ(tree->toInfixString(), "1 + 2 * 3");
}

TEST(Parser, ParenthesesOverridePrecedence) {
    auto tree = Parser::parse("(1 + 2) * 3");
    ASSERT_NE(tree, nullptr);
    EXPECT_EQ(tree->getName(), "*");
    EXPECT_EQ(tree->getChild(0)->getName(), "+");
    EXPECT_EQ(tree->toInfixString(), "(1 + 2) * 3");
}

TEST(Parser, UnaryMinusBindsOutsidePower) {
    auto tree = Parser::parse("-x^2");
    ASSERT_NE(tree, nullptr);
    // "-x^2" parses as -(x^2): '^' binds tighter than unary minus.
    EXPECT_EQ(tree->getType(), ASTNodeType::Operator);
    EXPECT_EQ(tree->getName(), "u-");
    ASSERT_EQ(tree->getNumChildren(), 1u);
    EXPECT_EQ(tree->getChild(0)->getName(), "^");
}

TEST(Parser, FunctionCallWithMultipleArguments) {
    auto tree = Parser::parse("normal(0, 1)");
    ASSERT_NE(tree, nullptr);
    EXPECT_EQ(tree->getType(), ASTNodeType::Function);
    EXPECT_EQ(tree->getName(), "normal");
    ASSERT_EQ(tree->getNumChildren(), 2u);
}

TEST(Parser, ReferenceAsOperand) {
    auto tree = Parser::parse("#tasks:sim1.model + 1");
    ASSERT_NE(tree, nullptr);
    EXPECT_EQ(tree->getChild(0)->getType(), ASTNodeType::Reference);
    EXPECT_EQ(tree->getChild(0)->getReferenceText(), "#tasks:sim1.model");
}

TEST(Parser, MalformedExpressionFails) {
    std::string error;
    auto tree = Parser::parse("1 + * 2", &error);
    EXPECT_EQ(tree, nullptr);
    EXPECT_FALSE(error.empty());
}

TEST(Parser, UnmatchedParenFails) {
    std::string error;
    auto tree = Parser::parse("(1 + 2", &error);
    EXPECT_EQ(tree, nullptr);
    EXPECT_FALSE(error.empty());
}

TEST(Parser, TrailingGarbageFails) {
    std::string error;
    auto tree = Parser::parse("1 + 2 3", &error);
    EXPECT_EQ(tree, nullptr);
    EXPECT_FALSE(error.empty());
}

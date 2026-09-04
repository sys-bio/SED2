#include "sed2/math/ASTNode.h"

#include <sstream>

namespace sed2 {

ASTNode::ASTNode(ASTNodeType type) : type_(type) {}

ASTNodeType ASTNode::getType() const { return type_; }
void ASTNode::setType(ASTNodeType type) { type_ = type; }

double ASTNode::getNumberValue() const { return numberValue_; }
void ASTNode::setNumberValue(double value) { numberValue_ = value; }

const std::string& ASTNode::getReferenceText() const { return text_; }
void ASTNode::setReferenceText(const std::string& text) { text_ = text; }

const std::string& ASTNode::getName() const { return text_; }
void ASTNode::setName(const std::string& name) { text_ = name; }

std::size_t ASTNode::getNumChildren() const { return children_.size(); }

ASTNode* ASTNode::getChild(std::size_t index) const {
    if (index >= children_.size()) return nullptr;
    return children_[index].get();
}

void ASTNode::addChild(std::unique_ptr<ASTNode> child) { children_.push_back(std::move(child)); }

namespace {

int precedenceOf(const std::string& op) {
    if (op == "+" || op == "-") return 1;
    if (op == "*" || op == "/") return 2;
    if (op == "^") return 3;
    if (op == "u-") return 4;  // unary minus binds tighter than any binary operator
    return 5;
}

bool isBinaryOperator(const std::string& op) {
    return op == "+" || op == "-" || op == "*" || op == "/" || op == "^";
}

std::string renderNumber(double value) {
    std::ostringstream out;
    out.precision(15);
    out << value;
    return out.str();
}

// Renders 'node' to infix text, wrapping it in parens if its own operator
// precedence is lower than 'parentPrecedence' (i.e. it would be
// misparsed as part of its parent without them). 'parentPrecedence' of 0
// means "no parens needed regardless" (used at the top level and inside
// function-call arguments).
std::string render(const ASTNode& node, int parentPrecedence) {
    switch (node.getType()) {
        case ASTNodeType::Number:
            return renderNumber(node.getNumberValue());
        case ASTNodeType::Reference:
            return node.getReferenceText();
        case ASTNodeType::Identifier:
            return node.getName();
        case ASTNodeType::Function: {
            std::ostringstream out;
            out << node.getName() << "(";
            for (std::size_t i = 0; i < node.getNumChildren(); ++i) {
                if (i > 0) out << ", ";
                out << render(*node.getChild(i), 0);
            }
            out << ")";
            return out.str();
        }
        case ASTNodeType::Operator: {
            const std::string& op = node.getName();
            int myPrecedence = precedenceOf(op);
            std::string result;
            if (op == "u-" && node.getNumChildren() == 1) {
                result = "-" + render(*node.getChild(0), myPrecedence);
            } else if (isBinaryOperator(op) && node.getNumChildren() == 2) {
                // The right operand is rendered as if it needed strictly
                // higher precedence than this operator, so a same-precedence
                // right-associated chain (e.g. a - (b - c)) is parenthesized
                // rather than silently reassociated to a - b - c.
                result = render(*node.getChild(0), myPrecedence) + " " + op + " " +
                         render(*node.getChild(1), myPrecedence + 1);
            } else {
                result = op;
            }
            if (myPrecedence < parentPrecedence) return "(" + result + ")";
            return result;
        }
    }
    return "";
}

}  // namespace

std::string ASTNode::toInfixString() const { return render(*this, 0); }

}  // namespace sed2

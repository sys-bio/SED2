#pragma once

#include <cstddef>
#include <memory>
#include <string>
#include <vector>

#include "sed2/math/ASTNodeType.h"

namespace sed2 {

// A node in a parsed infix math expression tree (Design.md, "Math": "an
// ASTNode class, borrowing the rough interface from libsbml's ASTNode
// class, without the XML dependency"). Owns its children.
class ASTNode {
public:
    explicit ASTNode(ASTNodeType type = ASTNodeType::Number);

    ASTNodeType getType() const;
    void setType(ASTNodeType type);

    // Number nodes.
    double getNumberValue() const;
    void setNumberValue(double value);

    // Reference nodes: the reference text verbatim, e.g.
    // "#tasks:sim1.model['S1']". Kept as text rather than pre-resolved,
    // since what it points to is only meaningful in the context of a
    // document (see AttributeTypes::parseReferencePath).
    const std::string& getReferenceText() const;
    void setReferenceText(const std::string& text);

    // Identifier, Operator and Function nodes: the name/symbol, e.g.
    // "pi", "+", "sin", "normal".
    const std::string& getName() const;
    void setName(const std::string& name);

    std::size_t getNumChildren() const;
    ASTNode* getChild(std::size_t index) const;
    void addChild(std::unique_ptr<ASTNode> child);

    // Renders the tree back to infix text. Parsing the result again
    // produces an equivalent tree, though not necessarily
    // whitespace-for-whitespace identical text.
    std::string toInfixString() const;

private:
    ASTNodeType type_;
    double numberValue_ = 0.0;
    std::string text_;  // reference text, or identifier/operator/function name
    std::vector<std::unique_ptr<ASTNode>> children_;
};

}  // namespace sed2

#pragma once

#include "libsed2/antlr/mathLexer.h"
#include "libsed2/antlr/mathParser.h"
#include "libsed2/antlr/mathBaseVisitor.h"
#include "antlr4-runtime.h"

#include <any>
#include <map>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

/* GENERATED - do not hand-edit; regenerate via generator/generate.py. */
namespace libsed2 {

enum class MathNodeType {
    NUMBER, REFERENCE, NAME, FUNCTION_CALL, ARRAY,
    UMINUS, UPLUS, ADD, SUB, MUL, DIV, POW
};

/// Borrows the rough interface of libsbml's ASTNode, minus the XML
/// dependency - same design note as the Python/Java targets' AST node.
class MathNode {
public:
    MathNodeType node_type;
    std::string text;   // NUMBER / REFERENCE: the raw source lexeme
    std::string name;   // NAME / FUNCTION_CALL: the identifier
    std::vector<std::shared_ptr<MathNode>> children;

    MathNode(MathNodeType t, std::string text_, std::string name_,
             std::vector<std::shared_ptr<MathNode>> children_)
        : node_type(t), text(std::move(text_)), name(std::move(name_)), children(std::move(children_)) {}

    bool is_number() const { return node_type == MathNodeType::NUMBER; }
    bool is_reference() const { return node_type == MathNodeType::REFERENCE; }
    bool is_name() const { return node_type == MathNodeType::NAME; }
    bool is_function_call() const { return node_type == MathNodeType::FUNCTION_CALL; }
    size_t get_num_children() const { return children.size(); }
    const MathNode& get_child(size_t index) const { return *children[index]; }

    /// Depth-first (this node first, then each child) - the traversal
    /// MathRules.hpp uses for Types-0002 through Types-0004.
    std::vector<const MathNode*> walk() const {
        std::vector<const MathNode*> out;
        walk_into(out);
        return out;
    }

private:
    void walk_into(std::vector<const MathNode*>& out) const {
        out.push_back(this);
        for (const auto& c : children) c->walk_into(out);
    }
};

/// Raised by math_parse() when the text isn't a well-formed SED2 math
/// expression - the condition Types-0001 reports, with this exception's
/// what() as its {parse-message}.
class MathSyntaxError : public std::runtime_error {
public:
    explicit MathSyntaxError(const std::string& message) : std::runtime_error(message) {}
};

namespace math_detail {

using NodePtr = std::shared_ptr<MathNode>;

inline const std::map<std::string, std::string>& relop_kind_map() {
    static const std::map<std::string, std::string> m = {
        {"==", "eq"}, {"!=", "neq"}, {"<>", "neq"}, {"><", "neq"},
        {"<", "lt"}, {">", "gt"}, {"<=", "leq"}, {">=", "geq"},
    };
    return m;
}

/// a < b < c -> lt(a, b, c); a < b <= c -> and(lt(a, b), leq(b, c)) - see
/// emit_python.py's _build_relational for the full rationale this mirrors
/// verbatim.
inline NodePtr build_relational(const std::vector<NodePtr>& operands, const std::vector<std::string>& kinds) {
    if (kinds.empty()) return operands[0];
    std::vector<NodePtr> run_nodes;
    size_t i = 0;
    size_t n = kinds.size();
    while (i < n) {
        const std::string& kind = kinds[i];
        std::vector<NodePtr> run_operands = {operands[i], operands[i + 1]};
        size_t j = i + 1;
        if (kind != "neq") {
            while (j < n && kinds[j] == kind) {
                run_operands.push_back(operands[j + 1]);
                j++;
            }
        }
        run_nodes.push_back(std::make_shared<MathNode>(MathNodeType::FUNCTION_CALL, "", kind, run_operands));
        i = j;
    }
    if (run_nodes.size() == 1) return run_nodes[0];
    return std::make_shared<MathNode>(MathNodeType::FUNCTION_CALL, "", "and", run_nodes);
}

/// a && b && c -> and(a, b, c); a && b || c -> or(and(a, b), c) - see
/// emit_python.py's _flatten_logical for the full rationale this mirrors
/// verbatim.
inline NodePtr flatten_logical(const std::vector<NodePtr>& operands, const std::vector<std::string>& ops) {
    if (ops.empty()) return operands[0];
    std::vector<std::string> group_ops;
    std::vector<std::vector<NodePtr>> group_operands;
    std::string current_op = ops[0];
    std::vector<NodePtr> current_operands = {operands[0], operands[1]};
    for (size_t i = 1; i < ops.size(); i++) {
        if (ops[i] == current_op) {
            current_operands.push_back(operands[i + 1]);
        } else {
            group_ops.push_back(current_op);
            group_operands.push_back(current_operands);
            current_op = ops[i];
            current_operands = {group_operands.back().back(), operands[i + 1]};
        }
    }
    group_ops.push_back(current_op);
    group_operands.push_back(current_operands);
    NodePtr result = std::make_shared<MathNode>(MathNodeType::FUNCTION_CALL, "", group_ops[0], group_operands[0]);
    for (size_t g = 1; g < group_ops.size(); g++) {
        std::vector<NodePtr> children = {result};
        for (size_t k = 1; k < group_operands[g].size(); k++) children.push_back(group_operands[g][k]);
        result = std::make_shared<MathNode>(MathNodeType::FUNCTION_CALL, "", group_ops[g], children);
    }
    return result;
}

class Builder : public libsed2::antlr::mathBaseVisitor {
public:
    NodePtr visit_node(antlr4::tree::ParseTree* tree) {
        return std::any_cast<NodePtr>(visit(tree));
    }

    std::any visitStart(libsed2::antlr::mathParser::StartContext *ctx) override {
        return visit_node(ctx->expr());
    }

    std::any visitExpr(libsed2::antlr::mathParser::ExprContext *ctx) override {
        return visit_node(ctx->logical());
    }

    std::any visitLogical(libsed2::antlr::mathParser::LogicalContext *ctx) override {
        auto relationals = ctx->relational();
        if (relationals.size() == 1) return visit_node(relationals[0]);
        std::vector<NodePtr> operands;
        for (auto* r : relationals) operands.push_back(visit_node(r));
        std::vector<std::string> ops;
        for (size_t i = 1; i < ctx->children.size(); i += 2) {
            ops.push_back(ctx->children[i]->getText() == "&&" ? "and" : "or");
        }
        return flatten_logical(operands, ops);
    }

    std::any visitRelational(libsed2::antlr::mathParser::RelationalContext *ctx) override {
        auto additives = ctx->additive();
        if (additives.size() == 1) return visit_node(additives[0]);
        std::vector<NodePtr> operands;
        for (auto* a : additives) operands.push_back(visit_node(a));
        std::vector<std::string> kinds;
        for (auto* r : ctx->relop()) kinds.push_back(relop_kind_map().at(r->getText()));
        return build_relational(operands, kinds);
    }

    std::any visitAdditive(libsed2::antlr::mathParser::AdditiveContext *ctx) override {
        auto muls = ctx->multiplicative();
        NodePtr node = visit_node(muls[0]);
        size_t idx = 1;
        for (size_t i = 1; i < ctx->children.size(); i += 2) {
            std::string op_text = ctx->children[i]->getText();
            NodePtr rhs = visit_node(muls[idx]);
            idx++;
            node = std::make_shared<MathNode>(op_text == "+" ? MathNodeType::ADD : MathNodeType::SUB, "", "",
                                               std::vector<NodePtr>{node, rhs});
        }
        return node;
    }

    std::any visitMultiplicative(libsed2::antlr::mathParser::MultiplicativeContext *ctx) override {
        auto units = ctx->unary();
        NodePtr node = visit_node(units[0]);
        size_t idx = 1;
        for (size_t i = 1; i < ctx->children.size(); i += 2) {
            std::string op_text = ctx->children[i]->getText();
            NodePtr rhs = visit_node(units[idx]);
            idx++;
            if (op_text == "*") {
                node = std::make_shared<MathNode>(MathNodeType::MUL, "", "", std::vector<NodePtr>{node, rhs});
            } else if (op_text == "/") {
                node = std::make_shared<MathNode>(MathNodeType::DIV, "", "", std::vector<NodePtr>{node, rhs});
            } else {
                // infix '%' is rem(), dividend's-sign semantics (Grammar)
                node = std::make_shared<MathNode>(MathNodeType::FUNCTION_CALL, "", "rem", std::vector<NodePtr>{node, rhs});
            }
        }
        return node;
    }

    std::any visitUnaryOp(libsed2::antlr::mathParser::UnaryOpContext *ctx) override {
        std::string op_text = ctx->children[0]->getText();
        NodePtr operand = visit_node(ctx->unary());
        if (op_text == "!") {
            return std::make_shared<MathNode>(MathNodeType::FUNCTION_CALL, "", "not", std::vector<NodePtr>{operand});
        }
        return std::make_shared<MathNode>(op_text == "-" ? MathNodeType::UMINUS : MathNodeType::UPLUS, "", "",
                                           std::vector<NodePtr>{operand});
    }

    std::any visitUnaryPower(libsed2::antlr::mathParser::UnaryPowerContext *ctx) override {
        return visit_node(ctx->power());
    }

    std::any visitPower(libsed2::antlr::mathParser::PowerContext *ctx) override {
        NodePtr base = visit_node(ctx->atom());
        if (ctx->unary()) {
            return std::make_shared<MathNode>(MathNodeType::POW, "", "",
                                               std::vector<NodePtr>{base, visit_node(ctx->unary())});
        }
        return base;
    }

    std::any visitNumberAtom(libsed2::antlr::mathParser::NumberAtomContext *ctx) override {
        return std::make_shared<MathNode>(MathNodeType::NUMBER, ctx->getText(), "", std::vector<NodePtr>{});
    }

    std::any visitReferenceAtom(libsed2::antlr::mathParser::ReferenceAtomContext *ctx) override {
        return std::make_shared<MathNode>(MathNodeType::REFERENCE, ctx->getText(), "", std::vector<NodePtr>{});
    }

    std::any visitIdentAtom(libsed2::antlr::mathParser::IdentAtomContext *ctx) override {
        return std::make_shared<MathNode>(MathNodeType::NAME, "", ctx->getText(), std::vector<NodePtr>{});
    }

    std::any visitCallAtom(libsed2::antlr::mathParser::CallAtomContext *ctx) override {
        std::string name = ctx->IDENTIFIER()->getText();
        std::vector<NodePtr> args;
        if (ctx->arglist()) {
            for (auto* e : ctx->arglist()->expr()) args.push_back(visit_node(e));
        }
        return std::make_shared<MathNode>(MathNodeType::FUNCTION_CALL, "", name, args);
    }

    std::any visitArrayAtom(libsed2::antlr::mathParser::ArrayAtomContext *ctx) override {
        std::vector<NodePtr> args;
        if (ctx->arglist()) {
            for (auto* e : ctx->arglist()->expr()) args.push_back(visit_node(e));
        }
        return std::make_shared<MathNode>(MathNodeType::ARRAY, "", "", args);
    }

    std::any visitParenAtom(libsed2::antlr::mathParser::ParenAtomContext *ctx) override {
        return visit_node(ctx->expr());
    }
};

class CollectingErrorListener : public antlr4::BaseErrorListener {
public:
    std::vector<std::string> errors;

    void syntaxError(antlr4::Recognizer* /*recognizer*/, antlr4::Token* /*offendingSymbol*/, size_t line,
                      size_t char_position_in_line, const std::string& msg, std::exception_ptr /*e*/) override {
        errors.push_back("line " + std::to_string(line) + ":" + std::to_string(char_position_in_line) + " " + msg);
    }
};

}  // namespace math_detail

/// Parses a SED2 math string into a MathNode tree (Types-0001). Throws
/// MathSyntaxError with the parser's own message on any malformed input.
inline std::shared_ptr<MathNode> math_parse(const std::string& text) {
    math_detail::CollectingErrorListener listener;
    antlr4::ANTLRInputStream input(text);
    libsed2::antlr::mathLexer lexer(&input);
    lexer.removeErrorListeners();
    lexer.addErrorListener(&listener);
    antlr4::CommonTokenStream tokens(&lexer);
    libsed2::antlr::mathParser parser(&tokens);
    parser.removeErrorListeners();
    parser.addErrorListener(&listener);
    libsed2::antlr::mathParser::StartContext* tree = parser.start();
    if (!listener.errors.empty()) {
        std::string joined;
        for (size_t i = 0; i < listener.errors.size(); i++) {
            if (i) joined += "; ";
            joined += listener.errors[i];
        }
        throw MathSyntaxError(joined);
    }
    math_detail::Builder builder;
    return builder.visit_node(tree);
}

}  // namespace libsed2


// Generated from math.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "mathParser.h"


namespace sed2test::antlr {

/**
 * This class defines an abstract visitor for a parse tree
 * produced by mathParser.
 */
class  mathVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by mathParser.
   */
    virtual std::any visitStart(mathParser::StartContext *context) = 0;

    virtual std::any visitExpr(mathParser::ExprContext *context) = 0;

    virtual std::any visitLogical(mathParser::LogicalContext *context) = 0;

    virtual std::any visitRelational(mathParser::RelationalContext *context) = 0;

    virtual std::any visitRelop(mathParser::RelopContext *context) = 0;

    virtual std::any visitAdditive(mathParser::AdditiveContext *context) = 0;

    virtual std::any visitMultiplicative(mathParser::MultiplicativeContext *context) = 0;

    virtual std::any visitUnaryOp(mathParser::UnaryOpContext *context) = 0;

    virtual std::any visitUnaryPower(mathParser::UnaryPowerContext *context) = 0;

    virtual std::any visitPower(mathParser::PowerContext *context) = 0;

    virtual std::any visitNumberAtom(mathParser::NumberAtomContext *context) = 0;

    virtual std::any visitReferenceAtom(mathParser::ReferenceAtomContext *context) = 0;

    virtual std::any visitCallAtom(mathParser::CallAtomContext *context) = 0;

    virtual std::any visitIdentAtom(mathParser::IdentAtomContext *context) = 0;

    virtual std::any visitArrayAtom(mathParser::ArrayAtomContext *context) = 0;

    virtual std::any visitParenAtom(mathParser::ParenAtomContext *context) = 0;

    virtual std::any visitArglist(mathParser::ArglistContext *context) = 0;


};

}  // namespace sed2test::antlr

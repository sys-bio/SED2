
// Generated from math.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "mathVisitor.h"


namespace libsed2::antlr {

/**
 * This class provides an empty implementation of mathVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  mathBaseVisitor : public mathVisitor {
public:

  virtual std::any visitStart(mathParser::StartContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpr(mathParser::ExprContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitLogical(mathParser::LogicalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRelational(mathParser::RelationalContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitRelop(mathParser::RelopContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAdditive(mathParser::AdditiveContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitMultiplicative(mathParser::MultiplicativeContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitUnaryOp(mathParser::UnaryOpContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitUnaryPower(mathParser::UnaryPowerContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitPower(mathParser::PowerContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitNumberAtom(mathParser::NumberAtomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitReferenceAtom(mathParser::ReferenceAtomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitCallAtom(mathParser::CallAtomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitIdentAtom(mathParser::IdentAtomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitArrayAtom(mathParser::ArrayAtomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitParenAtom(mathParser::ParenAtomContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitArglist(mathParser::ArglistContext *ctx) override {
    return visitChildren(ctx);
  }


};

}  // namespace libsed2::antlr

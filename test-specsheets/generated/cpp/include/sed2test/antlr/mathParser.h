
// Generated from math.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"


namespace sed2test::antlr {


class  mathParser : public antlr4::Parser {
public:
  enum {
    AND = 1, OR = 2, EQ = 3, NEQ = 4, NE_ALT = 5, LE = 6, GE = 7, LT = 8, 
    GT = 9, PLUS = 10, MINUS = 11, STAR = 12, SLASH = 13, PERCENT = 14, 
    BANG = 15, CARET = 16, LPAREN = 17, RPAREN = 18, LBRACK = 19, RBRACK = 20, 
    COMMA = 21, NUMBER = 22, REFERENCE = 23, IDENTIFIER = 24, WS = 25, ERRCHAR = 26
  };

  enum {
    RuleStart = 0, RuleExpr = 1, RuleLogical = 2, RuleRelational = 3, RuleRelop = 4, 
    RuleAdditive = 5, RuleMultiplicative = 6, RuleUnary = 7, RulePower = 8, 
    RuleAtom = 9, RuleArglist = 10
  };

  explicit mathParser(antlr4::TokenStream *input);

  mathParser(antlr4::TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options);

  ~mathParser() override;

  std::string getGrammarFileName() const override;

  const antlr4::atn::ATN& getATN() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;


  class StartContext;
  class ExprContext;
  class LogicalContext;
  class RelationalContext;
  class RelopContext;
  class AdditiveContext;
  class MultiplicativeContext;
  class UnaryContext;
  class PowerContext;
  class AtomContext;
  class ArglistContext; 

  class  StartContext : public antlr4::ParserRuleContext {
  public:
    StartContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    ExprContext *expr();
    antlr4::tree::TerminalNode *EOF();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  StartContext* start();

  class  ExprContext : public antlr4::ParserRuleContext {
  public:
    ExprContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    LogicalContext *logical();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ExprContext* expr();

  class  LogicalContext : public antlr4::ParserRuleContext {
  public:
    LogicalContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<RelationalContext *> relational();
    RelationalContext* relational(size_t i);
    std::vector<antlr4::tree::TerminalNode *> AND();
    antlr4::tree::TerminalNode* AND(size_t i);
    std::vector<antlr4::tree::TerminalNode *> OR();
    antlr4::tree::TerminalNode* OR(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  LogicalContext* logical();

  class  RelationalContext : public antlr4::ParserRuleContext {
  public:
    RelationalContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<AdditiveContext *> additive();
    AdditiveContext* additive(size_t i);
    std::vector<RelopContext *> relop();
    RelopContext* relop(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  RelationalContext* relational();

  class  RelopContext : public antlr4::ParserRuleContext {
  public:
    RelopContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    antlr4::tree::TerminalNode *EQ();
    antlr4::tree::TerminalNode *NEQ();
    antlr4::tree::TerminalNode *NE_ALT();
    antlr4::tree::TerminalNode *LE();
    antlr4::tree::TerminalNode *GE();
    antlr4::tree::TerminalNode *LT();
    antlr4::tree::TerminalNode *GT();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  RelopContext* relop();

  class  AdditiveContext : public antlr4::ParserRuleContext {
  public:
    AdditiveContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<MultiplicativeContext *> multiplicative();
    MultiplicativeContext* multiplicative(size_t i);
    std::vector<antlr4::tree::TerminalNode *> PLUS();
    antlr4::tree::TerminalNode* PLUS(size_t i);
    std::vector<antlr4::tree::TerminalNode *> MINUS();
    antlr4::tree::TerminalNode* MINUS(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  AdditiveContext* additive();

  class  MultiplicativeContext : public antlr4::ParserRuleContext {
  public:
    MultiplicativeContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<UnaryContext *> unary();
    UnaryContext* unary(size_t i);
    std::vector<antlr4::tree::TerminalNode *> STAR();
    antlr4::tree::TerminalNode* STAR(size_t i);
    std::vector<antlr4::tree::TerminalNode *> SLASH();
    antlr4::tree::TerminalNode* SLASH(size_t i);
    std::vector<antlr4::tree::TerminalNode *> PERCENT();
    antlr4::tree::TerminalNode* PERCENT(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  MultiplicativeContext* multiplicative();

  class  UnaryContext : public antlr4::ParserRuleContext {
  public:
    UnaryContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    UnaryContext() = default;
    void copyFrom(UnaryContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  UnaryPowerContext : public UnaryContext {
  public:
    UnaryPowerContext(UnaryContext *ctx);

    PowerContext *power();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  UnaryOpContext : public UnaryContext {
  public:
    UnaryOpContext(UnaryContext *ctx);

    UnaryContext *unary();
    antlr4::tree::TerminalNode *MINUS();
    antlr4::tree::TerminalNode *PLUS();
    antlr4::tree::TerminalNode *BANG();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  UnaryContext* unary();

  class  PowerContext : public antlr4::ParserRuleContext {
  public:
    PowerContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    AtomContext *atom();
    antlr4::tree::TerminalNode *CARET();
    UnaryContext *unary();


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  PowerContext* power();

  class  AtomContext : public antlr4::ParserRuleContext {
  public:
    AtomContext(antlr4::ParserRuleContext *parent, size_t invokingState);
   
    AtomContext() = default;
    void copyFrom(AtomContext *context);
    using antlr4::ParserRuleContext::copyFrom;

    virtual size_t getRuleIndex() const override;

   
  };

  class  CallAtomContext : public AtomContext {
  public:
    CallAtomContext(AtomContext *ctx);

    antlr4::tree::TerminalNode *IDENTIFIER();
    antlr4::tree::TerminalNode *LPAREN();
    antlr4::tree::TerminalNode *RPAREN();
    ArglistContext *arglist();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  IdentAtomContext : public AtomContext {
  public:
    IdentAtomContext(AtomContext *ctx);

    antlr4::tree::TerminalNode *IDENTIFIER();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ArrayAtomContext : public AtomContext {
  public:
    ArrayAtomContext(AtomContext *ctx);

    antlr4::tree::TerminalNode *LBRACK();
    antlr4::tree::TerminalNode *RBRACK();
    ArglistContext *arglist();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ParenAtomContext : public AtomContext {
  public:
    ParenAtomContext(AtomContext *ctx);

    antlr4::tree::TerminalNode *LPAREN();
    ExprContext *expr();
    antlr4::tree::TerminalNode *RPAREN();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  NumberAtomContext : public AtomContext {
  public:
    NumberAtomContext(AtomContext *ctx);

    antlr4::tree::TerminalNode *NUMBER();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  class  ReferenceAtomContext : public AtomContext {
  public:
    ReferenceAtomContext(AtomContext *ctx);

    antlr4::tree::TerminalNode *REFERENCE();

    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
  };

  AtomContext* atom();

  class  ArglistContext : public antlr4::ParserRuleContext {
  public:
    ArglistContext(antlr4::ParserRuleContext *parent, size_t invokingState);
    virtual size_t getRuleIndex() const override;
    std::vector<ExprContext *> expr();
    ExprContext* expr(size_t i);
    std::vector<antlr4::tree::TerminalNode *> COMMA();
    antlr4::tree::TerminalNode* COMMA(size_t i);


    virtual std::any accept(antlr4::tree::ParseTreeVisitor *visitor) override;
   
  };

  ArglistContext* arglist();


  // By default the static state used to implement the parser is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:
};

}  // namespace sed2test::antlr

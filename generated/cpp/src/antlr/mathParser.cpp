
// Generated from math.g4 by ANTLR 4.13.2


#include "mathVisitor.h"

#include "mathParser.h"


using namespace antlrcpp;
using namespace libsed2::antlr;

using namespace antlr4;

namespace {

struct MathParserStaticData final {
  MathParserStaticData(std::vector<std::string> ruleNames,
                        std::vector<std::string> literalNames,
                        std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  MathParserStaticData(const MathParserStaticData&) = delete;
  MathParserStaticData(MathParserStaticData&&) = delete;
  MathParserStaticData& operator=(const MathParserStaticData&) = delete;
  MathParserStaticData& operator=(MathParserStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag mathParserOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
std::unique_ptr<MathParserStaticData> mathParserStaticData = nullptr;

void mathParserInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (mathParserStaticData != nullptr) {
    return;
  }
#else
  assert(mathParserStaticData == nullptr);
#endif
  auto staticData = std::make_unique<MathParserStaticData>(
    std::vector<std::string>{
      "start", "expr", "logical", "relational", "relop", "additive", "multiplicative", 
      "unary", "power", "atom", "arglist"
    },
    std::vector<std::string>{
      "", "'&&'", "'||'", "'=='", "'!='", "", "'<='", "'>='", "'<'", "'>'", 
      "'+'", "'-'", "'*'", "'/'", "'%'", "'!'", "'^'", "'('", "')'", "'['", 
      "']'", "','"
    },
    std::vector<std::string>{
      "", "AND", "OR", "EQ", "NEQ", "NE_ALT", "LE", "GE", "LT", "GT", "PLUS", 
      "MINUS", "STAR", "SLASH", "PERCENT", "BANG", "CARET", "LPAREN", "RPAREN", 
      "LBRACK", "RBRACK", "COMMA", "NUMBER", "REFERENCE", "IDENTIFIER", 
      "WS", "ERRCHAR"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,1,26,101,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,2,
  	7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,1,0,1,0,1,1,1,1,1,2,1,2,1,2,5,2,31,
  	8,2,10,2,12,2,34,9,2,1,3,1,3,1,3,1,3,5,3,40,8,3,10,3,12,3,43,9,3,1,4,
  	1,4,1,5,1,5,1,5,5,5,50,8,5,10,5,12,5,53,9,5,1,6,1,6,1,6,5,6,58,8,6,10,
  	6,12,6,61,9,6,1,7,1,7,1,7,3,7,66,8,7,1,8,1,8,1,8,3,8,71,8,8,1,9,1,9,1,
  	9,1,9,1,9,3,9,78,8,9,1,9,1,9,1,9,1,9,3,9,84,8,9,1,9,1,9,1,9,1,9,1,9,3,
  	9,91,8,9,1,10,1,10,1,10,5,10,96,8,10,10,10,12,10,99,9,10,1,10,0,0,11,
  	0,2,4,6,8,10,12,14,16,18,20,0,5,1,0,1,2,1,0,3,9,1,0,10,11,1,0,12,14,2,
  	0,10,11,15,15,103,0,22,1,0,0,0,2,25,1,0,0,0,4,27,1,0,0,0,6,35,1,0,0,0,
  	8,44,1,0,0,0,10,46,1,0,0,0,12,54,1,0,0,0,14,65,1,0,0,0,16,67,1,0,0,0,
  	18,90,1,0,0,0,20,92,1,0,0,0,22,23,3,2,1,0,23,24,5,0,0,1,24,1,1,0,0,0,
  	25,26,3,4,2,0,26,3,1,0,0,0,27,32,3,6,3,0,28,29,7,0,0,0,29,31,3,6,3,0,
  	30,28,1,0,0,0,31,34,1,0,0,0,32,30,1,0,0,0,32,33,1,0,0,0,33,5,1,0,0,0,
  	34,32,1,0,0,0,35,41,3,10,5,0,36,37,3,8,4,0,37,38,3,10,5,0,38,40,1,0,0,
  	0,39,36,1,0,0,0,40,43,1,0,0,0,41,39,1,0,0,0,41,42,1,0,0,0,42,7,1,0,0,
  	0,43,41,1,0,0,0,44,45,7,1,0,0,45,9,1,0,0,0,46,51,3,12,6,0,47,48,7,2,0,
  	0,48,50,3,12,6,0,49,47,1,0,0,0,50,53,1,0,0,0,51,49,1,0,0,0,51,52,1,0,
  	0,0,52,11,1,0,0,0,53,51,1,0,0,0,54,59,3,14,7,0,55,56,7,3,0,0,56,58,3,
  	14,7,0,57,55,1,0,0,0,58,61,1,0,0,0,59,57,1,0,0,0,59,60,1,0,0,0,60,13,
  	1,0,0,0,61,59,1,0,0,0,62,63,7,4,0,0,63,66,3,14,7,0,64,66,3,16,8,0,65,
  	62,1,0,0,0,65,64,1,0,0,0,66,15,1,0,0,0,67,70,3,18,9,0,68,69,5,16,0,0,
  	69,71,3,14,7,0,70,68,1,0,0,0,70,71,1,0,0,0,71,17,1,0,0,0,72,91,5,22,0,
  	0,73,91,5,23,0,0,74,75,5,24,0,0,75,77,5,17,0,0,76,78,3,20,10,0,77,76,
  	1,0,0,0,77,78,1,0,0,0,78,79,1,0,0,0,79,91,5,18,0,0,80,91,5,24,0,0,81,
  	83,5,19,0,0,82,84,3,20,10,0,83,82,1,0,0,0,83,84,1,0,0,0,84,85,1,0,0,0,
  	85,91,5,20,0,0,86,87,5,17,0,0,87,88,3,2,1,0,88,89,5,18,0,0,89,91,1,0,
  	0,0,90,72,1,0,0,0,90,73,1,0,0,0,90,74,1,0,0,0,90,80,1,0,0,0,90,81,1,0,
  	0,0,90,86,1,0,0,0,91,19,1,0,0,0,92,97,3,2,1,0,93,94,5,21,0,0,94,96,3,
  	2,1,0,95,93,1,0,0,0,96,99,1,0,0,0,97,95,1,0,0,0,97,98,1,0,0,0,98,21,1,
  	0,0,0,99,97,1,0,0,0,10,32,41,51,59,65,70,77,83,90,97
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  mathParserStaticData = std::move(staticData);
}

}

mathParser::mathParser(TokenStream *input) : mathParser(input, antlr4::atn::ParserATNSimulatorOptions()) {}

mathParser::mathParser(TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options) : Parser(input) {
  mathParser::initialize();
  _interpreter = new atn::ParserATNSimulator(this, *mathParserStaticData->atn, mathParserStaticData->decisionToDFA, mathParserStaticData->sharedContextCache, options);
}

mathParser::~mathParser() {
  delete _interpreter;
}

const atn::ATN& mathParser::getATN() const {
  return *mathParserStaticData->atn;
}

std::string mathParser::getGrammarFileName() const {
  return "math.g4";
}

const std::vector<std::string>& mathParser::getRuleNames() const {
  return mathParserStaticData->ruleNames;
}

const dfa::Vocabulary& mathParser::getVocabulary() const {
  return mathParserStaticData->vocabulary;
}

antlr4::atn::SerializedATNView mathParser::getSerializedATN() const {
  return mathParserStaticData->serializedATN;
}


//----------------- StartContext ------------------------------------------------------------------

mathParser::StartContext::StartContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

mathParser::ExprContext* mathParser::StartContext::expr() {
  return getRuleContext<mathParser::ExprContext>(0);
}

tree::TerminalNode* mathParser::StartContext::EOF() {
  return getToken(mathParser::EOF, 0);
}


size_t mathParser::StartContext::getRuleIndex() const {
  return mathParser::RuleStart;
}


std::any mathParser::StartContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitStart(this);
  else
    return visitor->visitChildren(this);
}

mathParser::StartContext* mathParser::start() {
  StartContext *_localctx = _tracker.createInstance<StartContext>(_ctx, getState());
  enterRule(_localctx, 0, mathParser::RuleStart);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(22);
    expr();
    setState(23);
    match(mathParser::EOF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExprContext ------------------------------------------------------------------

mathParser::ExprContext::ExprContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

mathParser::LogicalContext* mathParser::ExprContext::logical() {
  return getRuleContext<mathParser::LogicalContext>(0);
}


size_t mathParser::ExprContext::getRuleIndex() const {
  return mathParser::RuleExpr;
}


std::any mathParser::ExprContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitExpr(this);
  else
    return visitor->visitChildren(this);
}

mathParser::ExprContext* mathParser::expr() {
  ExprContext *_localctx = _tracker.createInstance<ExprContext>(_ctx, getState());
  enterRule(_localctx, 2, mathParser::RuleExpr);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(25);
    logical();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LogicalContext ------------------------------------------------------------------

mathParser::LogicalContext::LogicalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<mathParser::RelationalContext *> mathParser::LogicalContext::relational() {
  return getRuleContexts<mathParser::RelationalContext>();
}

mathParser::RelationalContext* mathParser::LogicalContext::relational(size_t i) {
  return getRuleContext<mathParser::RelationalContext>(i);
}

std::vector<tree::TerminalNode *> mathParser::LogicalContext::AND() {
  return getTokens(mathParser::AND);
}

tree::TerminalNode* mathParser::LogicalContext::AND(size_t i) {
  return getToken(mathParser::AND, i);
}

std::vector<tree::TerminalNode *> mathParser::LogicalContext::OR() {
  return getTokens(mathParser::OR);
}

tree::TerminalNode* mathParser::LogicalContext::OR(size_t i) {
  return getToken(mathParser::OR, i);
}


size_t mathParser::LogicalContext::getRuleIndex() const {
  return mathParser::RuleLogical;
}


std::any mathParser::LogicalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitLogical(this);
  else
    return visitor->visitChildren(this);
}

mathParser::LogicalContext* mathParser::logical() {
  LogicalContext *_localctx = _tracker.createInstance<LogicalContext>(_ctx, getState());
  enterRule(_localctx, 4, mathParser::RuleLogical);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(27);
    relational();
    setState(32);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == mathParser::AND

    || _la == mathParser::OR) {
      setState(28);
      _la = _input->LA(1);
      if (!(_la == mathParser::AND

      || _la == mathParser::OR)) {
      _errHandler->recoverInline(this);
      }
      else {
        _errHandler->reportMatch(this);
        consume();
      }
      setState(29);
      relational();
      setState(34);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- RelationalContext ------------------------------------------------------------------

mathParser::RelationalContext::RelationalContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<mathParser::AdditiveContext *> mathParser::RelationalContext::additive() {
  return getRuleContexts<mathParser::AdditiveContext>();
}

mathParser::AdditiveContext* mathParser::RelationalContext::additive(size_t i) {
  return getRuleContext<mathParser::AdditiveContext>(i);
}

std::vector<mathParser::RelopContext *> mathParser::RelationalContext::relop() {
  return getRuleContexts<mathParser::RelopContext>();
}

mathParser::RelopContext* mathParser::RelationalContext::relop(size_t i) {
  return getRuleContext<mathParser::RelopContext>(i);
}


size_t mathParser::RelationalContext::getRuleIndex() const {
  return mathParser::RuleRelational;
}


std::any mathParser::RelationalContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitRelational(this);
  else
    return visitor->visitChildren(this);
}

mathParser::RelationalContext* mathParser::relational() {
  RelationalContext *_localctx = _tracker.createInstance<RelationalContext>(_ctx, getState());
  enterRule(_localctx, 6, mathParser::RuleRelational);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(35);
    additive();
    setState(41);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 1016) != 0)) {
      setState(36);
      relop();
      setState(37);
      additive();
      setState(43);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- RelopContext ------------------------------------------------------------------

mathParser::RelopContext::RelopContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* mathParser::RelopContext::EQ() {
  return getToken(mathParser::EQ, 0);
}

tree::TerminalNode* mathParser::RelopContext::NEQ() {
  return getToken(mathParser::NEQ, 0);
}

tree::TerminalNode* mathParser::RelopContext::NE_ALT() {
  return getToken(mathParser::NE_ALT, 0);
}

tree::TerminalNode* mathParser::RelopContext::LE() {
  return getToken(mathParser::LE, 0);
}

tree::TerminalNode* mathParser::RelopContext::GE() {
  return getToken(mathParser::GE, 0);
}

tree::TerminalNode* mathParser::RelopContext::LT() {
  return getToken(mathParser::LT, 0);
}

tree::TerminalNode* mathParser::RelopContext::GT() {
  return getToken(mathParser::GT, 0);
}


size_t mathParser::RelopContext::getRuleIndex() const {
  return mathParser::RuleRelop;
}


std::any mathParser::RelopContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitRelop(this);
  else
    return visitor->visitChildren(this);
}

mathParser::RelopContext* mathParser::relop() {
  RelopContext *_localctx = _tracker.createInstance<RelopContext>(_ctx, getState());
  enterRule(_localctx, 8, mathParser::RuleRelop);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(44);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 1016) != 0))) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AdditiveContext ------------------------------------------------------------------

mathParser::AdditiveContext::AdditiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<mathParser::MultiplicativeContext *> mathParser::AdditiveContext::multiplicative() {
  return getRuleContexts<mathParser::MultiplicativeContext>();
}

mathParser::MultiplicativeContext* mathParser::AdditiveContext::multiplicative(size_t i) {
  return getRuleContext<mathParser::MultiplicativeContext>(i);
}

std::vector<tree::TerminalNode *> mathParser::AdditiveContext::PLUS() {
  return getTokens(mathParser::PLUS);
}

tree::TerminalNode* mathParser::AdditiveContext::PLUS(size_t i) {
  return getToken(mathParser::PLUS, i);
}

std::vector<tree::TerminalNode *> mathParser::AdditiveContext::MINUS() {
  return getTokens(mathParser::MINUS);
}

tree::TerminalNode* mathParser::AdditiveContext::MINUS(size_t i) {
  return getToken(mathParser::MINUS, i);
}


size_t mathParser::AdditiveContext::getRuleIndex() const {
  return mathParser::RuleAdditive;
}


std::any mathParser::AdditiveContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitAdditive(this);
  else
    return visitor->visitChildren(this);
}

mathParser::AdditiveContext* mathParser::additive() {
  AdditiveContext *_localctx = _tracker.createInstance<AdditiveContext>(_ctx, getState());
  enterRule(_localctx, 10, mathParser::RuleAdditive);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(46);
    multiplicative();
    setState(51);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == mathParser::PLUS

    || _la == mathParser::MINUS) {
      setState(47);
      _la = _input->LA(1);
      if (!(_la == mathParser::PLUS

      || _la == mathParser::MINUS)) {
      _errHandler->recoverInline(this);
      }
      else {
        _errHandler->reportMatch(this);
        consume();
      }
      setState(48);
      multiplicative();
      setState(53);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- MultiplicativeContext ------------------------------------------------------------------

mathParser::MultiplicativeContext::MultiplicativeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<mathParser::UnaryContext *> mathParser::MultiplicativeContext::unary() {
  return getRuleContexts<mathParser::UnaryContext>();
}

mathParser::UnaryContext* mathParser::MultiplicativeContext::unary(size_t i) {
  return getRuleContext<mathParser::UnaryContext>(i);
}

std::vector<tree::TerminalNode *> mathParser::MultiplicativeContext::STAR() {
  return getTokens(mathParser::STAR);
}

tree::TerminalNode* mathParser::MultiplicativeContext::STAR(size_t i) {
  return getToken(mathParser::STAR, i);
}

std::vector<tree::TerminalNode *> mathParser::MultiplicativeContext::SLASH() {
  return getTokens(mathParser::SLASH);
}

tree::TerminalNode* mathParser::MultiplicativeContext::SLASH(size_t i) {
  return getToken(mathParser::SLASH, i);
}

std::vector<tree::TerminalNode *> mathParser::MultiplicativeContext::PERCENT() {
  return getTokens(mathParser::PERCENT);
}

tree::TerminalNode* mathParser::MultiplicativeContext::PERCENT(size_t i) {
  return getToken(mathParser::PERCENT, i);
}


size_t mathParser::MultiplicativeContext::getRuleIndex() const {
  return mathParser::RuleMultiplicative;
}


std::any mathParser::MultiplicativeContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitMultiplicative(this);
  else
    return visitor->visitChildren(this);
}

mathParser::MultiplicativeContext* mathParser::multiplicative() {
  MultiplicativeContext *_localctx = _tracker.createInstance<MultiplicativeContext>(_ctx, getState());
  enterRule(_localctx, 12, mathParser::RuleMultiplicative);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(54);
    unary();
    setState(59);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 28672) != 0)) {
      setState(55);
      _la = _input->LA(1);
      if (!((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & 28672) != 0))) {
      _errHandler->recoverInline(this);
      }
      else {
        _errHandler->reportMatch(this);
        consume();
      }
      setState(56);
      unary();
      setState(61);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- UnaryContext ------------------------------------------------------------------

mathParser::UnaryContext::UnaryContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t mathParser::UnaryContext::getRuleIndex() const {
  return mathParser::RuleUnary;
}

void mathParser::UnaryContext::copyFrom(UnaryContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- UnaryPowerContext ------------------------------------------------------------------

mathParser::PowerContext* mathParser::UnaryPowerContext::power() {
  return getRuleContext<mathParser::PowerContext>(0);
}

mathParser::UnaryPowerContext::UnaryPowerContext(UnaryContext *ctx) { copyFrom(ctx); }


std::any mathParser::UnaryPowerContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitUnaryPower(this);
  else
    return visitor->visitChildren(this);
}
//----------------- UnaryOpContext ------------------------------------------------------------------

mathParser::UnaryContext* mathParser::UnaryOpContext::unary() {
  return getRuleContext<mathParser::UnaryContext>(0);
}

tree::TerminalNode* mathParser::UnaryOpContext::MINUS() {
  return getToken(mathParser::MINUS, 0);
}

tree::TerminalNode* mathParser::UnaryOpContext::PLUS() {
  return getToken(mathParser::PLUS, 0);
}

tree::TerminalNode* mathParser::UnaryOpContext::BANG() {
  return getToken(mathParser::BANG, 0);
}

mathParser::UnaryOpContext::UnaryOpContext(UnaryContext *ctx) { copyFrom(ctx); }


std::any mathParser::UnaryOpContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitUnaryOp(this);
  else
    return visitor->visitChildren(this);
}
mathParser::UnaryContext* mathParser::unary() {
  UnaryContext *_localctx = _tracker.createInstance<UnaryContext>(_ctx, getState());
  enterRule(_localctx, 14, mathParser::RuleUnary);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(65);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case mathParser::PLUS:
      case mathParser::MINUS:
      case mathParser::BANG: {
        _localctx = _tracker.createInstance<mathParser::UnaryOpContext>(_localctx);
        enterOuterAlt(_localctx, 1);
        setState(62);
        _la = _input->LA(1);
        if (!((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & 35840) != 0))) {
        _errHandler->recoverInline(this);
        }
        else {
          _errHandler->reportMatch(this);
          consume();
        }
        setState(63);
        unary();
        break;
      }

      case mathParser::LPAREN:
      case mathParser::LBRACK:
      case mathParser::NUMBER:
      case mathParser::REFERENCE:
      case mathParser::IDENTIFIER: {
        _localctx = _tracker.createInstance<mathParser::UnaryPowerContext>(_localctx);
        enterOuterAlt(_localctx, 2);
        setState(64);
        power();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PowerContext ------------------------------------------------------------------

mathParser::PowerContext::PowerContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

mathParser::AtomContext* mathParser::PowerContext::atom() {
  return getRuleContext<mathParser::AtomContext>(0);
}

tree::TerminalNode* mathParser::PowerContext::CARET() {
  return getToken(mathParser::CARET, 0);
}

mathParser::UnaryContext* mathParser::PowerContext::unary() {
  return getRuleContext<mathParser::UnaryContext>(0);
}


size_t mathParser::PowerContext::getRuleIndex() const {
  return mathParser::RulePower;
}


std::any mathParser::PowerContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitPower(this);
  else
    return visitor->visitChildren(this);
}

mathParser::PowerContext* mathParser::power() {
  PowerContext *_localctx = _tracker.createInstance<PowerContext>(_ctx, getState());
  enterRule(_localctx, 16, mathParser::RulePower);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(67);
    atom();
    setState(70);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == mathParser::CARET) {
      setState(68);
      match(mathParser::CARET);
      setState(69);
      unary();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AtomContext ------------------------------------------------------------------

mathParser::AtomContext::AtomContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}


size_t mathParser::AtomContext::getRuleIndex() const {
  return mathParser::RuleAtom;
}

void mathParser::AtomContext::copyFrom(AtomContext *ctx) {
  ParserRuleContext::copyFrom(ctx);
}

//----------------- CallAtomContext ------------------------------------------------------------------

tree::TerminalNode* mathParser::CallAtomContext::IDENTIFIER() {
  return getToken(mathParser::IDENTIFIER, 0);
}

tree::TerminalNode* mathParser::CallAtomContext::LPAREN() {
  return getToken(mathParser::LPAREN, 0);
}

tree::TerminalNode* mathParser::CallAtomContext::RPAREN() {
  return getToken(mathParser::RPAREN, 0);
}

mathParser::ArglistContext* mathParser::CallAtomContext::arglist() {
  return getRuleContext<mathParser::ArglistContext>(0);
}

mathParser::CallAtomContext::CallAtomContext(AtomContext *ctx) { copyFrom(ctx); }


std::any mathParser::CallAtomContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitCallAtom(this);
  else
    return visitor->visitChildren(this);
}
//----------------- IdentAtomContext ------------------------------------------------------------------

tree::TerminalNode* mathParser::IdentAtomContext::IDENTIFIER() {
  return getToken(mathParser::IDENTIFIER, 0);
}

mathParser::IdentAtomContext::IdentAtomContext(AtomContext *ctx) { copyFrom(ctx); }


std::any mathParser::IdentAtomContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitIdentAtom(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ArrayAtomContext ------------------------------------------------------------------

tree::TerminalNode* mathParser::ArrayAtomContext::LBRACK() {
  return getToken(mathParser::LBRACK, 0);
}

tree::TerminalNode* mathParser::ArrayAtomContext::RBRACK() {
  return getToken(mathParser::RBRACK, 0);
}

mathParser::ArglistContext* mathParser::ArrayAtomContext::arglist() {
  return getRuleContext<mathParser::ArglistContext>(0);
}

mathParser::ArrayAtomContext::ArrayAtomContext(AtomContext *ctx) { copyFrom(ctx); }


std::any mathParser::ArrayAtomContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitArrayAtom(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ParenAtomContext ------------------------------------------------------------------

tree::TerminalNode* mathParser::ParenAtomContext::LPAREN() {
  return getToken(mathParser::LPAREN, 0);
}

mathParser::ExprContext* mathParser::ParenAtomContext::expr() {
  return getRuleContext<mathParser::ExprContext>(0);
}

tree::TerminalNode* mathParser::ParenAtomContext::RPAREN() {
  return getToken(mathParser::RPAREN, 0);
}

mathParser::ParenAtomContext::ParenAtomContext(AtomContext *ctx) { copyFrom(ctx); }


std::any mathParser::ParenAtomContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitParenAtom(this);
  else
    return visitor->visitChildren(this);
}
//----------------- NumberAtomContext ------------------------------------------------------------------

tree::TerminalNode* mathParser::NumberAtomContext::NUMBER() {
  return getToken(mathParser::NUMBER, 0);
}

mathParser::NumberAtomContext::NumberAtomContext(AtomContext *ctx) { copyFrom(ctx); }


std::any mathParser::NumberAtomContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitNumberAtom(this);
  else
    return visitor->visitChildren(this);
}
//----------------- ReferenceAtomContext ------------------------------------------------------------------

tree::TerminalNode* mathParser::ReferenceAtomContext::REFERENCE() {
  return getToken(mathParser::REFERENCE, 0);
}

mathParser::ReferenceAtomContext::ReferenceAtomContext(AtomContext *ctx) { copyFrom(ctx); }


std::any mathParser::ReferenceAtomContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitReferenceAtom(this);
  else
    return visitor->visitChildren(this);
}
mathParser::AtomContext* mathParser::atom() {
  AtomContext *_localctx = _tracker.createInstance<AtomContext>(_ctx, getState());
  enterRule(_localctx, 18, mathParser::RuleAtom);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(90);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 8, _ctx)) {
    case 1: {
      _localctx = _tracker.createInstance<mathParser::NumberAtomContext>(_localctx);
      enterOuterAlt(_localctx, 1);
      setState(72);
      match(mathParser::NUMBER);
      break;
    }

    case 2: {
      _localctx = _tracker.createInstance<mathParser::ReferenceAtomContext>(_localctx);
      enterOuterAlt(_localctx, 2);
      setState(73);
      match(mathParser::REFERENCE);
      break;
    }

    case 3: {
      _localctx = _tracker.createInstance<mathParser::CallAtomContext>(_localctx);
      enterOuterAlt(_localctx, 3);
      setState(74);
      match(mathParser::IDENTIFIER);
      setState(75);
      match(mathParser::LPAREN);
      setState(77);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & 30051328) != 0)) {
        setState(76);
        arglist();
      }
      setState(79);
      match(mathParser::RPAREN);
      break;
    }

    case 4: {
      _localctx = _tracker.createInstance<mathParser::IdentAtomContext>(_localctx);
      enterOuterAlt(_localctx, 4);
      setState(80);
      match(mathParser::IDENTIFIER);
      break;
    }

    case 5: {
      _localctx = _tracker.createInstance<mathParser::ArrayAtomContext>(_localctx);
      enterOuterAlt(_localctx, 5);
      setState(81);
      match(mathParser::LBRACK);
      setState(83);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & 30051328) != 0)) {
        setState(82);
        arglist();
      }
      setState(85);
      match(mathParser::RBRACK);
      break;
    }

    case 6: {
      _localctx = _tracker.createInstance<mathParser::ParenAtomContext>(_localctx);
      enterOuterAlt(_localctx, 6);
      setState(86);
      match(mathParser::LPAREN);
      setState(87);
      expr();
      setState(88);
      match(mathParser::RPAREN);
      break;
    }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ArglistContext ------------------------------------------------------------------

mathParser::ArglistContext::ArglistContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<mathParser::ExprContext *> mathParser::ArglistContext::expr() {
  return getRuleContexts<mathParser::ExprContext>();
}

mathParser::ExprContext* mathParser::ArglistContext::expr(size_t i) {
  return getRuleContext<mathParser::ExprContext>(i);
}

std::vector<tree::TerminalNode *> mathParser::ArglistContext::COMMA() {
  return getTokens(mathParser::COMMA);
}

tree::TerminalNode* mathParser::ArglistContext::COMMA(size_t i) {
  return getToken(mathParser::COMMA, i);
}


size_t mathParser::ArglistContext::getRuleIndex() const {
  return mathParser::RuleArglist;
}


std::any mathParser::ArglistContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<mathVisitor*>(visitor))
    return parserVisitor->visitArglist(this);
  else
    return visitor->visitChildren(this);
}

mathParser::ArglistContext* mathParser::arglist() {
  ArglistContext *_localctx = _tracker.createInstance<ArglistContext>(_ctx, getState());
  enterRule(_localctx, 20, mathParser::RuleArglist);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(92);
    expr();
    setState(97);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == mathParser::COMMA) {
      setState(93);
      match(mathParser::COMMA);
      setState(94);
      expr();
      setState(99);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

void mathParser::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  mathParserInitialize();
#else
  ::antlr4::internal::call_once(mathParserOnceFlag, mathParserInitialize);
#endif
}

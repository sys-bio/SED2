
// Generated from math.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"


namespace libsed2::antlr {


class  mathLexer : public antlr4::Lexer {
public:
  enum {
    AND = 1, OR = 2, EQ = 3, NEQ = 4, NE_ALT = 5, LE = 6, GE = 7, LT = 8, 
    GT = 9, PLUS = 10, MINUS = 11, STAR = 12, SLASH = 13, PERCENT = 14, 
    BANG = 15, CARET = 16, LPAREN = 17, RPAREN = 18, LBRACK = 19, RBRACK = 20, 
    COMMA = 21, NUMBER = 22, REFERENCE = 23, IDENTIFIER = 24, WS = 25, ERRCHAR = 26
  };

  explicit mathLexer(antlr4::CharStream *input);

  ~mathLexer() override;


  std::string getGrammarFileName() const override;

  const std::vector<std::string>& getRuleNames() const override;

  const std::vector<std::string>& getChannelNames() const override;

  const std::vector<std::string>& getModeNames() const override;

  const antlr4::dfa::Vocabulary& getVocabulary() const override;

  antlr4::atn::SerializedATNView getSerializedATN() const override;

  const antlr4::atn::ATN& getATN() const override;

  // By default the static state used to implement the lexer is lazily initialized during the first
  // call to the constructor. You can call this function if you wish to initialize the static state
  // ahead of time.
  static void initialize();

private:

  // Individual action functions triggered by action() above.

  // Individual semantic predicate functions triggered by sempred() above.

};

}  // namespace libsed2::antlr

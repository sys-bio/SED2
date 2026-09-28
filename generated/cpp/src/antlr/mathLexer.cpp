
// Generated from math.g4 by ANTLR 4.13.2


#include "mathLexer.h"


using namespace antlr4;

using namespace libsed2::antlr;


using namespace antlr4;

namespace {

struct MathLexerStaticData final {
  MathLexerStaticData(std::vector<std::string> ruleNames,
                          std::vector<std::string> channelNames,
                          std::vector<std::string> modeNames,
                          std::vector<std::string> literalNames,
                          std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), channelNames(std::move(channelNames)),
        modeNames(std::move(modeNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  MathLexerStaticData(const MathLexerStaticData&) = delete;
  MathLexerStaticData(MathLexerStaticData&&) = delete;
  MathLexerStaticData& operator=(const MathLexerStaticData&) = delete;
  MathLexerStaticData& operator=(MathLexerStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> channelNames;
  const std::vector<std::string> modeNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag mathlexerLexerOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
std::unique_ptr<MathLexerStaticData> mathlexerLexerStaticData = nullptr;

void mathlexerLexerInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (mathlexerLexerStaticData != nullptr) {
    return;
  }
#else
  assert(mathlexerLexerStaticData == nullptr);
#endif
  auto staticData = std::make_unique<MathLexerStaticData>(
    std::vector<std::string>{
      "AND", "OR", "EQ", "NEQ", "NE_ALT", "LE", "GE", "LT", "GT", "PLUS", 
      "MINUS", "STAR", "SLASH", "PERCENT", "BANG", "CARET", "LPAREN", "RPAREN", 
      "LBRACK", "RBRACK", "COMMA", "NUMBER", "EXP", "DIGIT", "REFERENCE", 
      "SUBACCESS_FRAG", "INDEX_FRAG", "SIGNED_INT_FRAG", "IDENT_FRAG", "IDENTIFIER", 
      "WS", "ERRCHAR"
    },
    std::vector<std::string>{
      "DEFAULT_TOKEN_CHANNEL", "HIDDEN"
    },
    std::vector<std::string>{
      "DEFAULT_MODE"
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
  	4,0,26,219,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,
  	7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,
  	7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,2,27,7,27,2,28,
  	7,28,2,29,7,29,2,30,7,30,2,31,7,31,1,0,1,0,1,0,1,1,1,1,1,1,1,2,1,2,1,
  	2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,3,4,82,8,4,1,5,1,5,1,5,1,6,1,6,1,6,1,7,
  	1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,12,1,12,1,13,1,13,1,14,1,14,
  	1,15,1,15,1,16,1,16,1,17,1,17,1,18,1,18,1,19,1,19,1,20,1,20,1,21,4,21,
  	119,8,21,11,21,12,21,120,1,21,1,21,4,21,125,8,21,11,21,12,21,126,3,21,
  	129,8,21,1,21,3,21,132,8,21,1,21,1,21,4,21,136,8,21,11,21,12,21,137,1,
  	21,3,21,141,8,21,3,21,143,8,21,1,22,1,22,3,22,147,8,22,1,22,4,22,150,
  	8,22,11,22,12,22,151,1,23,1,23,1,24,1,24,1,24,1,24,5,24,160,8,24,10,24,
  	12,24,163,9,24,1,24,5,24,166,8,24,10,24,12,24,169,9,24,1,25,1,25,1,25,
  	1,25,1,25,1,25,3,25,177,8,25,1,26,1,26,1,26,3,26,182,8,26,1,26,1,26,5,
  	26,186,8,26,10,26,12,26,189,9,26,1,26,3,26,192,8,26,1,27,3,27,195,8,27,
  	1,27,4,27,198,8,27,11,27,12,27,199,1,28,1,28,5,28,204,8,28,10,28,12,28,
  	207,9,28,1,29,1,29,1,30,4,30,212,8,30,11,30,12,30,213,1,30,1,30,1,31,
  	1,31,0,0,32,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,
  	25,13,27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,22,45,0,47,0,
  	49,23,51,0,53,0,55,0,57,0,59,24,61,25,63,26,1,0,7,2,0,69,69,101,101,2,
  	0,43,43,45,45,1,0,48,57,3,0,10,10,13,13,39,39,3,0,65,90,95,95,97,122,
  	4,0,48,57,65,90,95,95,97,122,3,0,9,10,13,13,32,32,232,0,1,1,0,0,0,0,3,
  	1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,
  	0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,
  	1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,
  	0,0,0,37,1,0,0,0,0,39,1,0,0,0,0,41,1,0,0,0,0,43,1,0,0,0,0,49,1,0,0,0,
  	0,59,1,0,0,0,0,61,1,0,0,0,0,63,1,0,0,0,1,65,1,0,0,0,3,68,1,0,0,0,5,71,
  	1,0,0,0,7,74,1,0,0,0,9,81,1,0,0,0,11,83,1,0,0,0,13,86,1,0,0,0,15,89,1,
  	0,0,0,17,91,1,0,0,0,19,93,1,0,0,0,21,95,1,0,0,0,23,97,1,0,0,0,25,99,1,
  	0,0,0,27,101,1,0,0,0,29,103,1,0,0,0,31,105,1,0,0,0,33,107,1,0,0,0,35,
  	109,1,0,0,0,37,111,1,0,0,0,39,113,1,0,0,0,41,115,1,0,0,0,43,142,1,0,0,
  	0,45,144,1,0,0,0,47,153,1,0,0,0,49,155,1,0,0,0,51,176,1,0,0,0,53,191,
  	1,0,0,0,55,194,1,0,0,0,57,201,1,0,0,0,59,208,1,0,0,0,61,211,1,0,0,0,63,
  	217,1,0,0,0,65,66,5,38,0,0,66,67,5,38,0,0,67,2,1,0,0,0,68,69,5,124,0,
  	0,69,70,5,124,0,0,70,4,1,0,0,0,71,72,5,61,0,0,72,73,5,61,0,0,73,6,1,0,
  	0,0,74,75,5,33,0,0,75,76,5,61,0,0,76,8,1,0,0,0,77,78,5,60,0,0,78,82,5,
  	62,0,0,79,80,5,62,0,0,80,82,5,60,0,0,81,77,1,0,0,0,81,79,1,0,0,0,82,10,
  	1,0,0,0,83,84,5,60,0,0,84,85,5,61,0,0,85,12,1,0,0,0,86,87,5,62,0,0,87,
  	88,5,61,0,0,88,14,1,0,0,0,89,90,5,60,0,0,90,16,1,0,0,0,91,92,5,62,0,0,
  	92,18,1,0,0,0,93,94,5,43,0,0,94,20,1,0,0,0,95,96,5,45,0,0,96,22,1,0,0,
  	0,97,98,5,42,0,0,98,24,1,0,0,0,99,100,5,47,0,0,100,26,1,0,0,0,101,102,
  	5,37,0,0,102,28,1,0,0,0,103,104,5,33,0,0,104,30,1,0,0,0,105,106,5,94,
  	0,0,106,32,1,0,0,0,107,108,5,40,0,0,108,34,1,0,0,0,109,110,5,41,0,0,110,
  	36,1,0,0,0,111,112,5,91,0,0,112,38,1,0,0,0,113,114,5,93,0,0,114,40,1,
  	0,0,0,115,116,5,44,0,0,116,42,1,0,0,0,117,119,3,47,23,0,118,117,1,0,0,
  	0,119,120,1,0,0,0,120,118,1,0,0,0,120,121,1,0,0,0,121,128,1,0,0,0,122,
  	124,5,46,0,0,123,125,3,47,23,0,124,123,1,0,0,0,125,126,1,0,0,0,126,124,
  	1,0,0,0,126,127,1,0,0,0,127,129,1,0,0,0,128,122,1,0,0,0,128,129,1,0,0,
  	0,129,131,1,0,0,0,130,132,3,45,22,0,131,130,1,0,0,0,131,132,1,0,0,0,132,
  	143,1,0,0,0,133,135,5,46,0,0,134,136,3,47,23,0,135,134,1,0,0,0,136,137,
  	1,0,0,0,137,135,1,0,0,0,137,138,1,0,0,0,138,140,1,0,0,0,139,141,3,45,
  	22,0,140,139,1,0,0,0,140,141,1,0,0,0,141,143,1,0,0,0,142,118,1,0,0,0,
  	142,133,1,0,0,0,143,44,1,0,0,0,144,146,7,0,0,0,145,147,7,1,0,0,146,145,
  	1,0,0,0,146,147,1,0,0,0,147,149,1,0,0,0,148,150,3,47,23,0,149,148,1,0,
  	0,0,150,151,1,0,0,0,151,149,1,0,0,0,151,152,1,0,0,0,152,46,1,0,0,0,153,
  	154,7,2,0,0,154,48,1,0,0,0,155,156,5,35,0,0,156,161,3,57,28,0,157,158,
  	5,58,0,0,158,160,3,57,28,0,159,157,1,0,0,0,160,163,1,0,0,0,161,159,1,
  	0,0,0,161,162,1,0,0,0,162,167,1,0,0,0,163,161,1,0,0,0,164,166,3,51,25,
  	0,165,164,1,0,0,0,166,169,1,0,0,0,167,165,1,0,0,0,167,168,1,0,0,0,168,
  	50,1,0,0,0,169,167,1,0,0,0,170,171,5,46,0,0,171,177,3,57,28,0,172,173,
  	5,91,0,0,173,174,3,53,26,0,174,175,5,93,0,0,175,177,1,0,0,0,176,170,1,
  	0,0,0,176,172,1,0,0,0,177,52,1,0,0,0,178,181,3,55,27,0,179,180,5,58,0,
  	0,180,182,3,55,27,0,181,179,1,0,0,0,181,182,1,0,0,0,182,192,1,0,0,0,183,
  	187,5,39,0,0,184,186,8,3,0,0,185,184,1,0,0,0,186,189,1,0,0,0,187,185,
  	1,0,0,0,187,188,1,0,0,0,188,190,1,0,0,0,189,187,1,0,0,0,190,192,5,39,
  	0,0,191,178,1,0,0,0,191,183,1,0,0,0,192,54,1,0,0,0,193,195,5,45,0,0,194,
  	193,1,0,0,0,194,195,1,0,0,0,195,197,1,0,0,0,196,198,3,47,23,0,197,196,
  	1,0,0,0,198,199,1,0,0,0,199,197,1,0,0,0,199,200,1,0,0,0,200,56,1,0,0,
  	0,201,205,7,4,0,0,202,204,7,5,0,0,203,202,1,0,0,0,204,207,1,0,0,0,205,
  	203,1,0,0,0,205,206,1,0,0,0,206,58,1,0,0,0,207,205,1,0,0,0,208,209,3,
  	57,28,0,209,60,1,0,0,0,210,212,7,6,0,0,211,210,1,0,0,0,212,213,1,0,0,
  	0,213,211,1,0,0,0,213,214,1,0,0,0,214,215,1,0,0,0,215,216,6,30,0,0,216,
  	62,1,0,0,0,217,218,9,0,0,0,218,64,1,0,0,0,21,0,81,120,126,128,131,137,
  	140,142,146,151,161,167,176,181,187,191,194,199,205,213,1,6,0,0
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  mathlexerLexerStaticData = std::move(staticData);
}

}

mathLexer::mathLexer(CharStream *input) : Lexer(input) {
  mathLexer::initialize();
  _interpreter = new atn::LexerATNSimulator(this, *mathlexerLexerStaticData->atn, mathlexerLexerStaticData->decisionToDFA, mathlexerLexerStaticData->sharedContextCache);
}

mathLexer::~mathLexer() {
  delete _interpreter;
}

std::string mathLexer::getGrammarFileName() const {
  return "math.g4";
}

const std::vector<std::string>& mathLexer::getRuleNames() const {
  return mathlexerLexerStaticData->ruleNames;
}

const std::vector<std::string>& mathLexer::getChannelNames() const {
  return mathlexerLexerStaticData->channelNames;
}

const std::vector<std::string>& mathLexer::getModeNames() const {
  return mathlexerLexerStaticData->modeNames;
}

const dfa::Vocabulary& mathLexer::getVocabulary() const {
  return mathlexerLexerStaticData->vocabulary;
}

antlr4::atn::SerializedATNView mathLexer::getSerializedATN() const {
  return mathlexerLexerStaticData->serializedATN;
}

const atn::ATN& mathLexer::getATN() const {
  return *mathlexerLexerStaticData->atn;
}




void mathLexer::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  mathlexerLexerInitialize();
#else
  ::antlr4::internal::call_once(mathlexerLexerOnceFlag, mathlexerLexerInitialize);
#endif
}

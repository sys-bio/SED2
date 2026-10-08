
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
      "SUBACCESS_FRAG", "INDEX_FRAG", "BLANKS", "SIGNED_INT_FRAG", "IDENT_FRAG", 
      "IDENTIFIER", "WS", "ERRCHAR"
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
  	4,0,26,252,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,
  	7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,
  	7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,2,27,7,27,2,28,
  	7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,1,0,1,0,1,0,1,1,1,1,1,1,
  	1,2,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,4,1,4,3,4,84,8,4,1,5,1,5,1,5,1,6,1,
  	6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,12,1,12,1,13,1,13,
  	1,14,1,14,1,15,1,15,1,16,1,16,1,17,1,17,1,18,1,18,1,19,1,19,1,20,1,20,
  	1,21,4,21,121,8,21,11,21,12,21,122,1,21,1,21,4,21,127,8,21,11,21,12,21,
  	128,3,21,131,8,21,1,21,3,21,134,8,21,1,21,1,21,4,21,138,8,21,11,21,12,
  	21,139,1,21,3,21,143,8,21,3,21,145,8,21,1,22,1,22,3,22,149,8,22,1,22,
  	4,22,152,8,22,11,22,12,22,153,1,23,1,23,1,24,1,24,1,24,1,24,5,24,162,
  	8,24,10,24,12,24,165,9,24,1,24,5,24,168,8,24,10,24,12,24,171,9,24,1,25,
  	1,25,1,25,1,25,1,25,1,25,1,25,1,25,1,25,1,25,5,25,183,8,25,10,25,12,25,
  	186,9,25,1,25,1,25,1,25,3,25,191,8,25,1,26,1,26,3,26,195,8,26,1,26,1,
  	26,1,26,1,26,3,26,201,8,26,1,26,1,26,5,26,205,8,26,10,26,12,26,208,9,
  	26,1,26,1,26,1,26,5,26,213,8,26,10,26,12,26,216,9,26,1,26,3,26,219,8,
  	26,1,27,5,27,222,8,27,10,27,12,27,225,9,27,1,28,3,28,228,8,28,1,28,4,
  	28,231,8,28,11,28,12,28,232,1,29,1,29,5,29,237,8,29,10,29,12,29,240,9,
  	29,1,30,1,30,1,31,4,31,245,8,31,11,31,12,31,246,1,31,1,31,1,32,1,32,0,
  	0,33,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,25,13,
  	27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,22,45,0,47,0,49,23,
  	51,0,53,0,55,0,57,0,59,0,61,24,63,25,65,26,1,0,9,2,0,69,69,101,101,2,
  	0,43,43,45,45,1,0,48,57,3,0,10,10,13,13,39,39,3,0,10,10,13,13,34,34,2,
  	0,9,9,32,32,3,0,65,90,95,95,97,122,4,0,48,57,65,90,95,95,97,122,3,0,9,
  	10,13,13,32,32,270,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,
  	9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,
  	0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,
  	0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,0,37,1,0,0,0,0,39,1,0,0,0,0,
  	41,1,0,0,0,0,43,1,0,0,0,0,49,1,0,0,0,0,61,1,0,0,0,0,63,1,0,0,0,0,65,1,
  	0,0,0,1,67,1,0,0,0,3,70,1,0,0,0,5,73,1,0,0,0,7,76,1,0,0,0,9,83,1,0,0,
  	0,11,85,1,0,0,0,13,88,1,0,0,0,15,91,1,0,0,0,17,93,1,0,0,0,19,95,1,0,0,
  	0,21,97,1,0,0,0,23,99,1,0,0,0,25,101,1,0,0,0,27,103,1,0,0,0,29,105,1,
  	0,0,0,31,107,1,0,0,0,33,109,1,0,0,0,35,111,1,0,0,0,37,113,1,0,0,0,39,
  	115,1,0,0,0,41,117,1,0,0,0,43,144,1,0,0,0,45,146,1,0,0,0,47,155,1,0,0,
  	0,49,157,1,0,0,0,51,190,1,0,0,0,53,218,1,0,0,0,55,223,1,0,0,0,57,227,
  	1,0,0,0,59,234,1,0,0,0,61,241,1,0,0,0,63,244,1,0,0,0,65,250,1,0,0,0,67,
  	68,5,38,0,0,68,69,5,38,0,0,69,2,1,0,0,0,70,71,5,124,0,0,71,72,5,124,0,
  	0,72,4,1,0,0,0,73,74,5,61,0,0,74,75,5,61,0,0,75,6,1,0,0,0,76,77,5,33,
  	0,0,77,78,5,61,0,0,78,8,1,0,0,0,79,80,5,60,0,0,80,84,5,62,0,0,81,82,5,
  	62,0,0,82,84,5,60,0,0,83,79,1,0,0,0,83,81,1,0,0,0,84,10,1,0,0,0,85,86,
  	5,60,0,0,86,87,5,61,0,0,87,12,1,0,0,0,88,89,5,62,0,0,89,90,5,61,0,0,90,
  	14,1,0,0,0,91,92,5,60,0,0,92,16,1,0,0,0,93,94,5,62,0,0,94,18,1,0,0,0,
  	95,96,5,43,0,0,96,20,1,0,0,0,97,98,5,45,0,0,98,22,1,0,0,0,99,100,5,42,
  	0,0,100,24,1,0,0,0,101,102,5,47,0,0,102,26,1,0,0,0,103,104,5,37,0,0,104,
  	28,1,0,0,0,105,106,5,33,0,0,106,30,1,0,0,0,107,108,5,94,0,0,108,32,1,
  	0,0,0,109,110,5,40,0,0,110,34,1,0,0,0,111,112,5,41,0,0,112,36,1,0,0,0,
  	113,114,5,91,0,0,114,38,1,0,0,0,115,116,5,93,0,0,116,40,1,0,0,0,117,118,
  	5,44,0,0,118,42,1,0,0,0,119,121,3,47,23,0,120,119,1,0,0,0,121,122,1,0,
  	0,0,122,120,1,0,0,0,122,123,1,0,0,0,123,130,1,0,0,0,124,126,5,46,0,0,
  	125,127,3,47,23,0,126,125,1,0,0,0,127,128,1,0,0,0,128,126,1,0,0,0,128,
  	129,1,0,0,0,129,131,1,0,0,0,130,124,1,0,0,0,130,131,1,0,0,0,131,133,1,
  	0,0,0,132,134,3,45,22,0,133,132,1,0,0,0,133,134,1,0,0,0,134,145,1,0,0,
  	0,135,137,5,46,0,0,136,138,3,47,23,0,137,136,1,0,0,0,138,139,1,0,0,0,
  	139,137,1,0,0,0,139,140,1,0,0,0,140,142,1,0,0,0,141,143,3,45,22,0,142,
  	141,1,0,0,0,142,143,1,0,0,0,143,145,1,0,0,0,144,120,1,0,0,0,144,135,1,
  	0,0,0,145,44,1,0,0,0,146,148,7,0,0,0,147,149,7,1,0,0,148,147,1,0,0,0,
  	148,149,1,0,0,0,149,151,1,0,0,0,150,152,3,47,23,0,151,150,1,0,0,0,152,
  	153,1,0,0,0,153,151,1,0,0,0,153,154,1,0,0,0,154,46,1,0,0,0,155,156,7,
  	2,0,0,156,48,1,0,0,0,157,158,5,35,0,0,158,163,3,59,29,0,159,160,5,58,
  	0,0,160,162,3,59,29,0,161,159,1,0,0,0,162,165,1,0,0,0,163,161,1,0,0,0,
  	163,164,1,0,0,0,164,169,1,0,0,0,165,163,1,0,0,0,166,168,3,51,25,0,167,
  	166,1,0,0,0,168,171,1,0,0,0,169,167,1,0,0,0,169,170,1,0,0,0,170,50,1,
  	0,0,0,171,169,1,0,0,0,172,173,5,46,0,0,173,191,3,59,29,0,174,175,5,91,
  	0,0,175,176,3,55,27,0,176,184,3,53,26,0,177,178,3,55,27,0,178,179,5,44,
  	0,0,179,180,3,55,27,0,180,181,3,53,26,0,181,183,1,0,0,0,182,177,1,0,0,
  	0,183,186,1,0,0,0,184,182,1,0,0,0,184,185,1,0,0,0,185,187,1,0,0,0,186,
  	184,1,0,0,0,187,188,3,55,27,0,188,189,5,93,0,0,189,191,1,0,0,0,190,172,
  	1,0,0,0,190,174,1,0,0,0,191,52,1,0,0,0,192,219,3,57,28,0,193,195,3,57,
  	28,0,194,193,1,0,0,0,194,195,1,0,0,0,195,196,1,0,0,0,196,197,3,55,27,
  	0,197,198,5,58,0,0,198,200,3,55,27,0,199,201,3,57,28,0,200,199,1,0,0,
  	0,200,201,1,0,0,0,201,219,1,0,0,0,202,206,5,39,0,0,203,205,8,3,0,0,204,
  	203,1,0,0,0,205,208,1,0,0,0,206,204,1,0,0,0,206,207,1,0,0,0,207,209,1,
  	0,0,0,208,206,1,0,0,0,209,219,5,39,0,0,210,214,5,34,0,0,211,213,8,4,0,
  	0,212,211,1,0,0,0,213,216,1,0,0,0,214,212,1,0,0,0,214,215,1,0,0,0,215,
  	217,1,0,0,0,216,214,1,0,0,0,217,219,5,34,0,0,218,192,1,0,0,0,218,194,
  	1,0,0,0,218,202,1,0,0,0,218,210,1,0,0,0,219,54,1,0,0,0,220,222,7,5,0,
  	0,221,220,1,0,0,0,222,225,1,0,0,0,223,221,1,0,0,0,223,224,1,0,0,0,224,
  	56,1,0,0,0,225,223,1,0,0,0,226,228,5,45,0,0,227,226,1,0,0,0,227,228,1,
  	0,0,0,228,230,1,0,0,0,229,231,3,47,23,0,230,229,1,0,0,0,231,232,1,0,0,
  	0,232,230,1,0,0,0,232,233,1,0,0,0,233,58,1,0,0,0,234,238,7,6,0,0,235,
  	237,7,7,0,0,236,235,1,0,0,0,237,240,1,0,0,0,238,236,1,0,0,0,238,239,1,
  	0,0,0,239,60,1,0,0,0,240,238,1,0,0,0,241,242,3,59,29,0,242,62,1,0,0,0,
  	243,245,7,8,0,0,244,243,1,0,0,0,245,246,1,0,0,0,246,244,1,0,0,0,246,247,
  	1,0,0,0,247,248,1,0,0,0,248,249,6,31,0,0,249,64,1,0,0,0,250,251,9,0,0,
  	0,251,66,1,0,0,0,25,0,83,122,128,130,133,139,142,144,148,153,163,169,
  	184,190,194,200,206,214,218,223,227,232,238,246,1,6,0,0
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

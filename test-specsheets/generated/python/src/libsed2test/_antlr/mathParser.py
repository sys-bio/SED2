# Generated from /home/runner/work/SED2/SED2/generator/math.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,26,101,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,1,0,1,0,1,1,1,1,1,2,1,2,
        1,2,5,2,31,8,2,10,2,12,2,34,9,2,1,3,1,3,1,3,1,3,5,3,40,8,3,10,3,
        12,3,43,9,3,1,4,1,4,1,5,1,5,1,5,5,5,50,8,5,10,5,12,5,53,9,5,1,6,
        1,6,1,6,5,6,58,8,6,10,6,12,6,61,9,6,1,7,1,7,1,7,3,7,66,8,7,1,8,1,
        8,1,8,3,8,71,8,8,1,9,1,9,1,9,1,9,1,9,3,9,78,8,9,1,9,1,9,1,9,1,9,
        3,9,84,8,9,1,9,1,9,1,9,1,9,1,9,3,9,91,8,9,1,10,1,10,1,10,5,10,96,
        8,10,10,10,12,10,99,9,10,1,10,0,0,11,0,2,4,6,8,10,12,14,16,18,20,
        0,5,1,0,1,2,1,0,3,9,1,0,10,11,1,0,12,14,2,0,10,11,15,15,103,0,22,
        1,0,0,0,2,25,1,0,0,0,4,27,1,0,0,0,6,35,1,0,0,0,8,44,1,0,0,0,10,46,
        1,0,0,0,12,54,1,0,0,0,14,65,1,0,0,0,16,67,1,0,0,0,18,90,1,0,0,0,
        20,92,1,0,0,0,22,23,3,2,1,0,23,24,5,0,0,1,24,1,1,0,0,0,25,26,3,4,
        2,0,26,3,1,0,0,0,27,32,3,6,3,0,28,29,7,0,0,0,29,31,3,6,3,0,30,28,
        1,0,0,0,31,34,1,0,0,0,32,30,1,0,0,0,32,33,1,0,0,0,33,5,1,0,0,0,34,
        32,1,0,0,0,35,41,3,10,5,0,36,37,3,8,4,0,37,38,3,10,5,0,38,40,1,0,
        0,0,39,36,1,0,0,0,40,43,1,0,0,0,41,39,1,0,0,0,41,42,1,0,0,0,42,7,
        1,0,0,0,43,41,1,0,0,0,44,45,7,1,0,0,45,9,1,0,0,0,46,51,3,12,6,0,
        47,48,7,2,0,0,48,50,3,12,6,0,49,47,1,0,0,0,50,53,1,0,0,0,51,49,1,
        0,0,0,51,52,1,0,0,0,52,11,1,0,0,0,53,51,1,0,0,0,54,59,3,14,7,0,55,
        56,7,3,0,0,56,58,3,14,7,0,57,55,1,0,0,0,58,61,1,0,0,0,59,57,1,0,
        0,0,59,60,1,0,0,0,60,13,1,0,0,0,61,59,1,0,0,0,62,63,7,4,0,0,63,66,
        3,14,7,0,64,66,3,16,8,0,65,62,1,0,0,0,65,64,1,0,0,0,66,15,1,0,0,
        0,67,70,3,18,9,0,68,69,5,16,0,0,69,71,3,14,7,0,70,68,1,0,0,0,70,
        71,1,0,0,0,71,17,1,0,0,0,72,91,5,22,0,0,73,91,5,23,0,0,74,75,5,24,
        0,0,75,77,5,17,0,0,76,78,3,20,10,0,77,76,1,0,0,0,77,78,1,0,0,0,78,
        79,1,0,0,0,79,91,5,18,0,0,80,91,5,24,0,0,81,83,5,19,0,0,82,84,3,
        20,10,0,83,82,1,0,0,0,83,84,1,0,0,0,84,85,1,0,0,0,85,91,5,20,0,0,
        86,87,5,17,0,0,87,88,3,2,1,0,88,89,5,18,0,0,89,91,1,0,0,0,90,72,
        1,0,0,0,90,73,1,0,0,0,90,74,1,0,0,0,90,80,1,0,0,0,90,81,1,0,0,0,
        90,86,1,0,0,0,91,19,1,0,0,0,92,97,3,2,1,0,93,94,5,21,0,0,94,96,3,
        2,1,0,95,93,1,0,0,0,96,99,1,0,0,0,97,95,1,0,0,0,97,98,1,0,0,0,98,
        21,1,0,0,0,99,97,1,0,0,0,10,32,41,51,59,65,70,77,83,90,97
    ]

class mathParser ( Parser ):

    grammarFileName = "math.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'&&'", "'||'", "'=='", "'!='", "<INVALID>", 
                     "'<='", "'>='", "'<'", "'>'", "'+'", "'-'", "'*'", 
                     "'/'", "'%'", "'!'", "'^'", "'('", "')'", "'['", "']'", 
                     "','" ]

    symbolicNames = [ "<INVALID>", "AND", "OR", "EQ", "NEQ", "NE_ALT", "LE", 
                      "GE", "LT", "GT", "PLUS", "MINUS", "STAR", "SLASH", 
                      "PERCENT", "BANG", "CARET", "LPAREN", "RPAREN", "LBRACK", 
                      "RBRACK", "COMMA", "NUMBER", "REFERENCE", "IDENTIFIER", 
                      "WS", "ERRCHAR" ]

    RULE_start = 0
    RULE_expr = 1
    RULE_logical = 2
    RULE_relational = 3
    RULE_relop = 4
    RULE_additive = 5
    RULE_multiplicative = 6
    RULE_unary = 7
    RULE_power = 8
    RULE_atom = 9
    RULE_arglist = 10

    ruleNames =  [ "start", "expr", "logical", "relational", "relop", "additive", 
                   "multiplicative", "unary", "power", "atom", "arglist" ]

    EOF = Token.EOF
    AND=1
    OR=2
    EQ=3
    NEQ=4
    NE_ALT=5
    LE=6
    GE=7
    LT=8
    GT=9
    PLUS=10
    MINUS=11
    STAR=12
    SLASH=13
    PERCENT=14
    BANG=15
    CARET=16
    LPAREN=17
    RPAREN=18
    LBRACK=19
    RBRACK=20
    COMMA=21
    NUMBER=22
    REFERENCE=23
    IDENTIFIER=24
    WS=25
    ERRCHAR=26

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(mathParser.ExprContext,0)


        def EOF(self):
            return self.getToken(mathParser.EOF, 0)

        def getRuleIndex(self):
            return mathParser.RULE_start

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = mathParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self.expr()
            self.state = 23
            self.match(mathParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def logical(self):
            return self.getTypedRuleContext(mathParser.LogicalContext,0)


        def getRuleIndex(self):
            return mathParser.RULE_expr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = mathParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self.logical()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LogicalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def relational(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(mathParser.RelationalContext)
            else:
                return self.getTypedRuleContext(mathParser.RelationalContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(mathParser.AND)
            else:
                return self.getToken(mathParser.AND, i)

        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(mathParser.OR)
            else:
                return self.getToken(mathParser.OR, i)

        def getRuleIndex(self):
            return mathParser.RULE_logical

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogical" ):
                return visitor.visitLogical(self)
            else:
                return visitor.visitChildren(self)




    def logical(self):

        localctx = mathParser.LogicalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_logical)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27
            self.relational()
            self.state = 32
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==2:
                self.state = 28
                _la = self._input.LA(1)
                if not(_la==1 or _la==2):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 29
                self.relational()
                self.state = 34
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def additive(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(mathParser.AdditiveContext)
            else:
                return self.getTypedRuleContext(mathParser.AdditiveContext,i)


        def relop(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(mathParser.RelopContext)
            else:
                return self.getTypedRuleContext(mathParser.RelopContext,i)


        def getRuleIndex(self):
            return mathParser.RULE_relational

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelational" ):
                return visitor.visitRelational(self)
            else:
                return visitor.visitChildren(self)




    def relational(self):

        localctx = mathParser.RelationalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_relational)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.additive()
            self.state = 41
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1016) != 0):
                self.state = 36
                self.relop()
                self.state = 37
                self.additive()
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(mathParser.EQ, 0)

        def NEQ(self):
            return self.getToken(mathParser.NEQ, 0)

        def NE_ALT(self):
            return self.getToken(mathParser.NE_ALT, 0)

        def LE(self):
            return self.getToken(mathParser.LE, 0)

        def GE(self):
            return self.getToken(mathParser.GE, 0)

        def LT(self):
            return self.getToken(mathParser.LT, 0)

        def GT(self):
            return self.getToken(mathParser.GT, 0)

        def getRuleIndex(self):
            return mathParser.RULE_relop

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelop" ):
                return visitor.visitRelop(self)
            else:
                return visitor.visitChildren(self)




    def relop(self):

        localctx = mathParser.RelopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_relop)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1016) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicative(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(mathParser.MultiplicativeContext)
            else:
                return self.getTypedRuleContext(mathParser.MultiplicativeContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(mathParser.PLUS)
            else:
                return self.getToken(mathParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(mathParser.MINUS)
            else:
                return self.getToken(mathParser.MINUS, i)

        def getRuleIndex(self):
            return mathParser.RULE_additive

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditive" ):
                return visitor.visitAdditive(self)
            else:
                return visitor.visitChildren(self)




    def additive(self):

        localctx = mathParser.AdditiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_additive)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 46
            self.multiplicative()
            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==10 or _la==11:
                self.state = 47
                _la = self._input.LA(1)
                if not(_la==10 or _la==11):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 48
                self.multiplicative()
                self.state = 53
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def unary(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(mathParser.UnaryContext)
            else:
                return self.getTypedRuleContext(mathParser.UnaryContext,i)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(mathParser.STAR)
            else:
                return self.getToken(mathParser.STAR, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(mathParser.SLASH)
            else:
                return self.getToken(mathParser.SLASH, i)

        def PERCENT(self, i:int=None):
            if i is None:
                return self.getTokens(mathParser.PERCENT)
            else:
                return self.getToken(mathParser.PERCENT, i)

        def getRuleIndex(self):
            return mathParser.RULE_multiplicative

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicative" ):
                return visitor.visitMultiplicative(self)
            else:
                return visitor.visitChildren(self)




    def multiplicative(self):

        localctx = mathParser.MultiplicativeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_multiplicative)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self.unary()
            self.state = 59
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 28672) != 0):
                self.state = 55
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 28672) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 56
                self.unary()
                self.state = 61
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UnaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return mathParser.RULE_unary

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class UnaryPowerContext(UnaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a mathParser.UnaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def power(self):
            return self.getTypedRuleContext(mathParser.PowerContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryPower" ):
                return visitor.visitUnaryPower(self)
            else:
                return visitor.visitChildren(self)


    class UnaryOpContext(UnaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a mathParser.UnaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def unary(self):
            return self.getTypedRuleContext(mathParser.UnaryContext,0)

        def MINUS(self):
            return self.getToken(mathParser.MINUS, 0)
        def PLUS(self):
            return self.getToken(mathParser.PLUS, 0)
        def BANG(self):
            return self.getToken(mathParser.BANG, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryOp" ):
                return visitor.visitUnaryOp(self)
            else:
                return visitor.visitChildren(self)



    def unary(self):

        localctx = mathParser.UnaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_unary)
        self._la = 0 # Token type
        try:
            self.state = 65
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [10, 11, 15]:
                localctx = mathParser.UnaryOpContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 62
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 35840) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 63
                self.unary()
                pass
            elif token in [17, 19, 22, 23, 24]:
                localctx = mathParser.UnaryPowerContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 64
                self.power()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PowerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(mathParser.AtomContext,0)


        def CARET(self):
            return self.getToken(mathParser.CARET, 0)

        def unary(self):
            return self.getTypedRuleContext(mathParser.UnaryContext,0)


        def getRuleIndex(self):
            return mathParser.RULE_power

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPower" ):
                return visitor.visitPower(self)
            else:
                return visitor.visitChildren(self)




    def power(self):

        localctx = mathParser.PowerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_power)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 67
            self.atom()
            self.state = 70
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 68
                self.match(mathParser.CARET)
                self.state = 69
                self.unary()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return mathParser.RULE_atom

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class CallAtomContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a mathParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(mathParser.IDENTIFIER, 0)
        def LPAREN(self):
            return self.getToken(mathParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(mathParser.RPAREN, 0)
        def arglist(self):
            return self.getTypedRuleContext(mathParser.ArglistContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCallAtom" ):
                return visitor.visitCallAtom(self)
            else:
                return visitor.visitChildren(self)


    class IdentAtomContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a mathParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENTIFIER(self):
            return self.getToken(mathParser.IDENTIFIER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentAtom" ):
                return visitor.visitIdentAtom(self)
            else:
                return visitor.visitChildren(self)


    class ArrayAtomContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a mathParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LBRACK(self):
            return self.getToken(mathParser.LBRACK, 0)
        def RBRACK(self):
            return self.getToken(mathParser.RBRACK, 0)
        def arglist(self):
            return self.getTypedRuleContext(mathParser.ArglistContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayAtom" ):
                return visitor.visitArrayAtom(self)
            else:
                return visitor.visitChildren(self)


    class ParenAtomContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a mathParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(mathParser.LPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(mathParser.ExprContext,0)

        def RPAREN(self):
            return self.getToken(mathParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenAtom" ):
                return visitor.visitParenAtom(self)
            else:
                return visitor.visitChildren(self)


    class NumberAtomContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a mathParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(mathParser.NUMBER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberAtom" ):
                return visitor.visitNumberAtom(self)
            else:
                return visitor.visitChildren(self)


    class ReferenceAtomContext(AtomContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a mathParser.AtomContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def REFERENCE(self):
            return self.getToken(mathParser.REFERENCE, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReferenceAtom" ):
                return visitor.visitReferenceAtom(self)
            else:
                return visitor.visitChildren(self)



    def atom(self):

        localctx = mathParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.state = 90
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                localctx = mathParser.NumberAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 72
                self.match(mathParser.NUMBER)
                pass

            elif la_ == 2:
                localctx = mathParser.ReferenceAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 73
                self.match(mathParser.REFERENCE)
                pass

            elif la_ == 3:
                localctx = mathParser.CallAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 74
                self.match(mathParser.IDENTIFIER)
                self.state = 75
                self.match(mathParser.LPAREN)
                self.state = 77
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30051328) != 0):
                    self.state = 76
                    self.arglist()


                self.state = 79
                self.match(mathParser.RPAREN)
                pass

            elif la_ == 4:
                localctx = mathParser.IdentAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 80
                self.match(mathParser.IDENTIFIER)
                pass

            elif la_ == 5:
                localctx = mathParser.ArrayAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 81
                self.match(mathParser.LBRACK)
                self.state = 83
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 30051328) != 0):
                    self.state = 82
                    self.arglist()


                self.state = 85
                self.match(mathParser.RBRACK)
                pass

            elif la_ == 6:
                localctx = mathParser.ParenAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 86
                self.match(mathParser.LPAREN)
                self.state = 87
                self.expr()
                self.state = 88
                self.match(mathParser.RPAREN)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArglistContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(mathParser.ExprContext)
            else:
                return self.getTypedRuleContext(mathParser.ExprContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(mathParser.COMMA)
            else:
                return self.getToken(mathParser.COMMA, i)

        def getRuleIndex(self):
            return mathParser.RULE_arglist

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArglist" ):
                return visitor.visitArglist(self)
            else:
                return visitor.visitChildren(self)




    def arglist(self):

        localctx = mathParser.ArglistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_arglist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self.expr()
            self.state = 97
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==21:
                self.state = 93
                self.match(mathParser.COMMA)
                self.state = 94
                self.expr()
                self.state = 99
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx






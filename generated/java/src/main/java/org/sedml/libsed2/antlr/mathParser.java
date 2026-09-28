// Generated from math.g4 by ANTLR 4.13.2
package org.sedml.libsed2.antlr;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class mathParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		AND=1, OR=2, EQ=3, NEQ=4, NE_ALT=5, LE=6, GE=7, LT=8, GT=9, PLUS=10, MINUS=11, 
		STAR=12, SLASH=13, PERCENT=14, BANG=15, CARET=16, LPAREN=17, RPAREN=18, 
		LBRACK=19, RBRACK=20, COMMA=21, NUMBER=22, REFERENCE=23, IDENTIFIER=24, 
		WS=25, ERRCHAR=26;
	public static final int
		RULE_start = 0, RULE_expr = 1, RULE_logical = 2, RULE_relational = 3, 
		RULE_relop = 4, RULE_additive = 5, RULE_multiplicative = 6, RULE_unary = 7, 
		RULE_power = 8, RULE_atom = 9, RULE_arglist = 10;
	private static String[] makeRuleNames() {
		return new String[] {
			"start", "expr", "logical", "relational", "relop", "additive", "multiplicative", 
			"unary", "power", "atom", "arglist"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'&&'", "'||'", "'=='", "'!='", null, "'<='", "'>='", "'<'", "'>'", 
			"'+'", "'-'", "'*'", "'/'", "'%'", "'!'", "'^'", "'('", "')'", "'['", 
			"']'", "','"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "AND", "OR", "EQ", "NEQ", "NE_ALT", "LE", "GE", "LT", "GT", "PLUS", 
			"MINUS", "STAR", "SLASH", "PERCENT", "BANG", "CARET", "LPAREN", "RPAREN", 
			"LBRACK", "RBRACK", "COMMA", "NUMBER", "REFERENCE", "IDENTIFIER", "WS", 
			"ERRCHAR"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "math.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public mathParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StartContext extends ParserRuleContext {
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode EOF() { return getToken(mathParser.EOF, 0); }
		public StartContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_start; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitStart(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StartContext start() throws RecognitionException {
		StartContext _localctx = new StartContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_start);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(22);
			expr();
			setState(23);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExprContext extends ParserRuleContext {
		public LogicalContext logical() {
			return getRuleContext(LogicalContext.class,0);
		}
		public ExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expr; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitExpr(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ExprContext expr() throws RecognitionException {
		ExprContext _localctx = new ExprContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_expr);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(25);
			logical();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LogicalContext extends ParserRuleContext {
		public List<RelationalContext> relational() {
			return getRuleContexts(RelationalContext.class);
		}
		public RelationalContext relational(int i) {
			return getRuleContext(RelationalContext.class,i);
		}
		public List<TerminalNode> AND() { return getTokens(mathParser.AND); }
		public TerminalNode AND(int i) {
			return getToken(mathParser.AND, i);
		}
		public List<TerminalNode> OR() { return getTokens(mathParser.OR); }
		public TerminalNode OR(int i) {
			return getToken(mathParser.OR, i);
		}
		public LogicalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_logical; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitLogical(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LogicalContext logical() throws RecognitionException {
		LogicalContext _localctx = new LogicalContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_logical);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(27);
			relational();
			setState(32);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==AND || _la==OR) {
				{
				{
				setState(28);
				_la = _input.LA(1);
				if ( !(_la==AND || _la==OR) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(29);
				relational();
				}
				}
				setState(34);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RelationalContext extends ParserRuleContext {
		public List<AdditiveContext> additive() {
			return getRuleContexts(AdditiveContext.class);
		}
		public AdditiveContext additive(int i) {
			return getRuleContext(AdditiveContext.class,i);
		}
		public List<RelopContext> relop() {
			return getRuleContexts(RelopContext.class);
		}
		public RelopContext relop(int i) {
			return getRuleContext(RelopContext.class,i);
		}
		public RelationalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relational; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitRelational(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RelationalContext relational() throws RecognitionException {
		RelationalContext _localctx = new RelationalContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_relational);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(35);
			additive();
			setState(41);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 1016L) != 0)) {
				{
				{
				setState(36);
				relop();
				setState(37);
				additive();
				}
				}
				setState(43);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class RelopContext extends ParserRuleContext {
		public TerminalNode EQ() { return getToken(mathParser.EQ, 0); }
		public TerminalNode NEQ() { return getToken(mathParser.NEQ, 0); }
		public TerminalNode NE_ALT() { return getToken(mathParser.NE_ALT, 0); }
		public TerminalNode LE() { return getToken(mathParser.LE, 0); }
		public TerminalNode GE() { return getToken(mathParser.GE, 0); }
		public TerminalNode LT() { return getToken(mathParser.LT, 0); }
		public TerminalNode GT() { return getToken(mathParser.GT, 0); }
		public RelopContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_relop; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitRelop(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RelopContext relop() throws RecognitionException {
		RelopContext _localctx = new RelopContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_relop);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(44);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 1016L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AdditiveContext extends ParserRuleContext {
		public List<MultiplicativeContext> multiplicative() {
			return getRuleContexts(MultiplicativeContext.class);
		}
		public MultiplicativeContext multiplicative(int i) {
			return getRuleContext(MultiplicativeContext.class,i);
		}
		public List<TerminalNode> PLUS() { return getTokens(mathParser.PLUS); }
		public TerminalNode PLUS(int i) {
			return getToken(mathParser.PLUS, i);
		}
		public List<TerminalNode> MINUS() { return getTokens(mathParser.MINUS); }
		public TerminalNode MINUS(int i) {
			return getToken(mathParser.MINUS, i);
		}
		public AdditiveContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_additive; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitAdditive(this);
			else return visitor.visitChildren(this);
		}
	}

	public final AdditiveContext additive() throws RecognitionException {
		AdditiveContext _localctx = new AdditiveContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_additive);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(46);
			multiplicative();
			setState(51);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==PLUS || _la==MINUS) {
				{
				{
				setState(47);
				_la = _input.LA(1);
				if ( !(_la==PLUS || _la==MINUS) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(48);
				multiplicative();
				}
				}
				setState(53);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class MultiplicativeContext extends ParserRuleContext {
		public List<UnaryContext> unary() {
			return getRuleContexts(UnaryContext.class);
		}
		public UnaryContext unary(int i) {
			return getRuleContext(UnaryContext.class,i);
		}
		public List<TerminalNode> STAR() { return getTokens(mathParser.STAR); }
		public TerminalNode STAR(int i) {
			return getToken(mathParser.STAR, i);
		}
		public List<TerminalNode> SLASH() { return getTokens(mathParser.SLASH); }
		public TerminalNode SLASH(int i) {
			return getToken(mathParser.SLASH, i);
		}
		public List<TerminalNode> PERCENT() { return getTokens(mathParser.PERCENT); }
		public TerminalNode PERCENT(int i) {
			return getToken(mathParser.PERCENT, i);
		}
		public MultiplicativeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_multiplicative; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitMultiplicative(this);
			else return visitor.visitChildren(this);
		}
	}

	public final MultiplicativeContext multiplicative() throws RecognitionException {
		MultiplicativeContext _localctx = new MultiplicativeContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_multiplicative);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(54);
			unary();
			setState(59);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 28672L) != 0)) {
				{
				{
				setState(55);
				_la = _input.LA(1);
				if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 28672L) != 0)) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(56);
				unary();
				}
				}
				setState(61);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UnaryContext extends ParserRuleContext {
		public UnaryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unary; }
	 
		public UnaryContext() { }
		public void copyFrom(UnaryContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnaryPowerContext extends UnaryContext {
		public PowerContext power() {
			return getRuleContext(PowerContext.class,0);
		}
		public UnaryPowerContext(UnaryContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitUnaryPower(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnaryOpContext extends UnaryContext {
		public UnaryContext unary() {
			return getRuleContext(UnaryContext.class,0);
		}
		public TerminalNode MINUS() { return getToken(mathParser.MINUS, 0); }
		public TerminalNode PLUS() { return getToken(mathParser.PLUS, 0); }
		public TerminalNode BANG() { return getToken(mathParser.BANG, 0); }
		public UnaryOpContext(UnaryContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitUnaryOp(this);
			else return visitor.visitChildren(this);
		}
	}

	public final UnaryContext unary() throws RecognitionException {
		UnaryContext _localctx = new UnaryContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_unary);
		int _la;
		try {
			setState(65);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case PLUS:
			case MINUS:
			case BANG:
				_localctx = new UnaryOpContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(62);
				_la = _input.LA(1);
				if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 35840L) != 0)) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(63);
				unary();
				}
				break;
			case LPAREN:
			case LBRACK:
			case NUMBER:
			case REFERENCE:
			case IDENTIFIER:
				_localctx = new UnaryPowerContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(64);
				power();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PowerContext extends ParserRuleContext {
		public AtomContext atom() {
			return getRuleContext(AtomContext.class,0);
		}
		public TerminalNode CARET() { return getToken(mathParser.CARET, 0); }
		public UnaryContext unary() {
			return getRuleContext(UnaryContext.class,0);
		}
		public PowerContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_power; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitPower(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PowerContext power() throws RecognitionException {
		PowerContext _localctx = new PowerContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_power);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(67);
			atom();
			setState(70);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==CARET) {
				{
				setState(68);
				match(CARET);
				setState(69);
				unary();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AtomContext extends ParserRuleContext {
		public AtomContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_atom; }
	 
		public AtomContext() { }
		public void copyFrom(AtomContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CallAtomContext extends AtomContext {
		public TerminalNode IDENTIFIER() { return getToken(mathParser.IDENTIFIER, 0); }
		public TerminalNode LPAREN() { return getToken(mathParser.LPAREN, 0); }
		public TerminalNode RPAREN() { return getToken(mathParser.RPAREN, 0); }
		public ArglistContext arglist() {
			return getRuleContext(ArglistContext.class,0);
		}
		public CallAtomContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitCallAtom(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IdentAtomContext extends AtomContext {
		public TerminalNode IDENTIFIER() { return getToken(mathParser.IDENTIFIER, 0); }
		public IdentAtomContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitIdentAtom(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ArrayAtomContext extends AtomContext {
		public TerminalNode LBRACK() { return getToken(mathParser.LBRACK, 0); }
		public TerminalNode RBRACK() { return getToken(mathParser.RBRACK, 0); }
		public ArglistContext arglist() {
			return getRuleContext(ArglistContext.class,0);
		}
		public ArrayAtomContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitArrayAtom(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParenAtomContext extends AtomContext {
		public TerminalNode LPAREN() { return getToken(mathParser.LPAREN, 0); }
		public ExprContext expr() {
			return getRuleContext(ExprContext.class,0);
		}
		public TerminalNode RPAREN() { return getToken(mathParser.RPAREN, 0); }
		public ParenAtomContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitParenAtom(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NumberAtomContext extends AtomContext {
		public TerminalNode NUMBER() { return getToken(mathParser.NUMBER, 0); }
		public NumberAtomContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitNumberAtom(this);
			else return visitor.visitChildren(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ReferenceAtomContext extends AtomContext {
		public TerminalNode REFERENCE() { return getToken(mathParser.REFERENCE, 0); }
		public ReferenceAtomContext(AtomContext ctx) { copyFrom(ctx); }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitReferenceAtom(this);
			else return visitor.visitChildren(this);
		}
	}

	public final AtomContext atom() throws RecognitionException {
		AtomContext _localctx = new AtomContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_atom);
		int _la;
		try {
			setState(90);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,8,_ctx) ) {
			case 1:
				_localctx = new NumberAtomContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(72);
				match(NUMBER);
				}
				break;
			case 2:
				_localctx = new ReferenceAtomContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(73);
				match(REFERENCE);
				}
				break;
			case 3:
				_localctx = new CallAtomContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(74);
				match(IDENTIFIER);
				setState(75);
				match(LPAREN);
				setState(77);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 30051328L) != 0)) {
					{
					setState(76);
					arglist();
					}
				}

				setState(79);
				match(RPAREN);
				}
				break;
			case 4:
				_localctx = new IdentAtomContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(80);
				match(IDENTIFIER);
				}
				break;
			case 5:
				_localctx = new ArrayAtomContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(81);
				match(LBRACK);
				setState(83);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 30051328L) != 0)) {
					{
					setState(82);
					arglist();
					}
				}

				setState(85);
				match(RBRACK);
				}
				break;
			case 6:
				_localctx = new ParenAtomContext(_localctx);
				enterOuterAlt(_localctx, 6);
				{
				setState(86);
				match(LPAREN);
				setState(87);
				expr();
				setState(88);
				match(RPAREN);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArglistContext extends ParserRuleContext {
		public List<ExprContext> expr() {
			return getRuleContexts(ExprContext.class);
		}
		public ExprContext expr(int i) {
			return getRuleContext(ExprContext.class,i);
		}
		public List<TerminalNode> COMMA() { return getTokens(mathParser.COMMA); }
		public TerminalNode COMMA(int i) {
			return getToken(mathParser.COMMA, i);
		}
		public ArglistContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arglist; }
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof mathVisitor ) return ((mathVisitor<? extends T>)visitor).visitArglist(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArglistContext arglist() throws RecognitionException {
		ArglistContext _localctx = new ArglistContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_arglist);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(92);
			expr();
			setState(97);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==COMMA) {
				{
				{
				setState(93);
				match(COMMA);
				setState(94);
				expr();
				}
				}
				setState(99);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u0001\u001ae\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0005"+
		"\u0002\u001f\b\u0002\n\u0002\f\u0002\"\t\u0002\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0005\u0003(\b\u0003\n\u0003\f\u0003+\t\u0003"+
		"\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005"+
		"2\b\u0005\n\u0005\f\u00055\t\u0005\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0005\u0006:\b\u0006\n\u0006\f\u0006=\t\u0006\u0001\u0007\u0001\u0007"+
		"\u0001\u0007\u0003\u0007B\b\u0007\u0001\b\u0001\b\u0001\b\u0003\bG\b\b"+
		"\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0003\tN\b\t\u0001\t\u0001\t"+
		"\u0001\t\u0001\t\u0003\tT\b\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t"+
		"\u0003\t[\b\t\u0001\n\u0001\n\u0001\n\u0005\n`\b\n\n\n\f\nc\t\n\u0001"+
		"\n\u0000\u0000\u000b\u0000\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014"+
		"\u0000\u0005\u0001\u0000\u0001\u0002\u0001\u0000\u0003\t\u0001\u0000\n"+
		"\u000b\u0001\u0000\f\u000e\u0002\u0000\n\u000b\u000f\u000fg\u0000\u0016"+
		"\u0001\u0000\u0000\u0000\u0002\u0019\u0001\u0000\u0000\u0000\u0004\u001b"+
		"\u0001\u0000\u0000\u0000\u0006#\u0001\u0000\u0000\u0000\b,\u0001\u0000"+
		"\u0000\u0000\n.\u0001\u0000\u0000\u0000\f6\u0001\u0000\u0000\u0000\u000e"+
		"A\u0001\u0000\u0000\u0000\u0010C\u0001\u0000\u0000\u0000\u0012Z\u0001"+
		"\u0000\u0000\u0000\u0014\\\u0001\u0000\u0000\u0000\u0016\u0017\u0003\u0002"+
		"\u0001\u0000\u0017\u0018\u0005\u0000\u0000\u0001\u0018\u0001\u0001\u0000"+
		"\u0000\u0000\u0019\u001a\u0003\u0004\u0002\u0000\u001a\u0003\u0001\u0000"+
		"\u0000\u0000\u001b \u0003\u0006\u0003\u0000\u001c\u001d\u0007\u0000\u0000"+
		"\u0000\u001d\u001f\u0003\u0006\u0003\u0000\u001e\u001c\u0001\u0000\u0000"+
		"\u0000\u001f\"\u0001\u0000\u0000\u0000 \u001e\u0001\u0000\u0000\u0000"+
		" !\u0001\u0000\u0000\u0000!\u0005\u0001\u0000\u0000\u0000\" \u0001\u0000"+
		"\u0000\u0000#)\u0003\n\u0005\u0000$%\u0003\b\u0004\u0000%&\u0003\n\u0005"+
		"\u0000&(\u0001\u0000\u0000\u0000\'$\u0001\u0000\u0000\u0000(+\u0001\u0000"+
		"\u0000\u0000)\'\u0001\u0000\u0000\u0000)*\u0001\u0000\u0000\u0000*\u0007"+
		"\u0001\u0000\u0000\u0000+)\u0001\u0000\u0000\u0000,-\u0007\u0001\u0000"+
		"\u0000-\t\u0001\u0000\u0000\u0000.3\u0003\f\u0006\u0000/0\u0007\u0002"+
		"\u0000\u000002\u0003\f\u0006\u00001/\u0001\u0000\u0000\u000025\u0001\u0000"+
		"\u0000\u000031\u0001\u0000\u0000\u000034\u0001\u0000\u0000\u00004\u000b"+
		"\u0001\u0000\u0000\u000053\u0001\u0000\u0000\u00006;\u0003\u000e\u0007"+
		"\u000078\u0007\u0003\u0000\u00008:\u0003\u000e\u0007\u000097\u0001\u0000"+
		"\u0000\u0000:=\u0001\u0000\u0000\u0000;9\u0001\u0000\u0000\u0000;<\u0001"+
		"\u0000\u0000\u0000<\r\u0001\u0000\u0000\u0000=;\u0001\u0000\u0000\u0000"+
		">?\u0007\u0004\u0000\u0000?B\u0003\u000e\u0007\u0000@B\u0003\u0010\b\u0000"+
		"A>\u0001\u0000\u0000\u0000A@\u0001\u0000\u0000\u0000B\u000f\u0001\u0000"+
		"\u0000\u0000CF\u0003\u0012\t\u0000DE\u0005\u0010\u0000\u0000EG\u0003\u000e"+
		"\u0007\u0000FD\u0001\u0000\u0000\u0000FG\u0001\u0000\u0000\u0000G\u0011"+
		"\u0001\u0000\u0000\u0000H[\u0005\u0016\u0000\u0000I[\u0005\u0017\u0000"+
		"\u0000JK\u0005\u0018\u0000\u0000KM\u0005\u0011\u0000\u0000LN\u0003\u0014"+
		"\n\u0000ML\u0001\u0000\u0000\u0000MN\u0001\u0000\u0000\u0000NO\u0001\u0000"+
		"\u0000\u0000O[\u0005\u0012\u0000\u0000P[\u0005\u0018\u0000\u0000QS\u0005"+
		"\u0013\u0000\u0000RT\u0003\u0014\n\u0000SR\u0001\u0000\u0000\u0000ST\u0001"+
		"\u0000\u0000\u0000TU\u0001\u0000\u0000\u0000U[\u0005\u0014\u0000\u0000"+
		"VW\u0005\u0011\u0000\u0000WX\u0003\u0002\u0001\u0000XY\u0005\u0012\u0000"+
		"\u0000Y[\u0001\u0000\u0000\u0000ZH\u0001\u0000\u0000\u0000ZI\u0001\u0000"+
		"\u0000\u0000ZJ\u0001\u0000\u0000\u0000ZP\u0001\u0000\u0000\u0000ZQ\u0001"+
		"\u0000\u0000\u0000ZV\u0001\u0000\u0000\u0000[\u0013\u0001\u0000\u0000"+
		"\u0000\\a\u0003\u0002\u0001\u0000]^\u0005\u0015\u0000\u0000^`\u0003\u0002"+
		"\u0001\u0000_]\u0001\u0000\u0000\u0000`c\u0001\u0000\u0000\u0000a_\u0001"+
		"\u0000\u0000\u0000ab\u0001\u0000\u0000\u0000b\u0015\u0001\u0000\u0000"+
		"\u0000ca\u0001\u0000\u0000\u0000\n )3;AFMSZa";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}
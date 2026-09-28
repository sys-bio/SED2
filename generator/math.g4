// SED2 math grammar. Canonical source for the ANTLR-generated C++/Java/Python
// lexer+parser used by ASTNode.parse()/toString() in every generated library.
// See Design.md's Math section (Grammar / Lexer / Parser Strategy) - this file
// is the literal transcription of the EBNF sketch there, plus the libsbml-L3
// -derived relational/logical/piecewise semantics (decided 2026-09-24).
//
// GENERATED LIBRARIES NEVER HAND-EDIT THIS FILE'S OUTPUT. This file itself is
// hand-authored and lives under generator/, not specsheets/ - it isn't
// per-class data (see Repository Layout).
grammar math;

// ============================== Parser ==============================

// Top-level entry point for a whole math string (Calculation's math,
// DrawFromDistribution's arguments, ...). EOF makes trailing garbage a
// parse error rather than being silently ignored.
start : expr EOF ;

expr : logical ;

// && / || share one precedence level, left-associative (libsbml: one level).
logical : relational ( (AND | OR) relational )* ;

// Relational operators chain (a < b < c collapses to lt(a, b, c) at the
// AST-building stage - the grammar just captures the flat chain here).
relational : additive ( relop additive )* ;

relop : EQ | NEQ | NE_ALT | LE | GE | LT | GT ;

additive : multiplicative ( (PLUS | MINUS) multiplicative )* ;

multiplicative : unary ( (STAR | SLASH | PERCENT) unary )* ;

unary
    : (MINUS | PLUS | BANG) unary   # unaryOp
    | power                         # unaryPower
    ;

// Right-associative: the exponent side recurses through unary -> power.
power : atom (CARET unary)? ;

atom
    : NUMBER                                # numberAtom
    | REFERENCE                             # referenceAtom
    | IDENTIFIER LPAREN arglist? RPAREN     # callAtom
    | IDENTIFIER                            # identAtom
    | LBRACK arglist? RBRACK                # arrayAtom
    | LPAREN expr RPAREN                    # parenAtom
    ;

arglist : expr (COMMA expr)* ;

// ============================== Lexer ==============================

AND : '&&' ;
OR  : '||' ;

EQ     : '==' ;
NEQ    : '!=' ;
NE_ALT : '<>' | '><' ;
LE     : '<=' ;
GE     : '>=' ;
LT     : '<' ;
GT     : '>' ;

PLUS    : '+' ;
MINUS   : '-' ;
STAR    : '*' ;
SLASH   : '/' ;
PERCENT : '%' ;
BANG    : '!' ;
CARET   : '^' ;

LPAREN : '(' ;
RPAREN : ')' ;
LBRACK : '[' ;
RBRACK : ']' ;
COMMA  : ',' ;

NUMBER
    : DIGIT+ ('.' DIGIT+)? EXP?
    | '.' DIGIT+ EXP?
    ;
fragment EXP   : [eE] [+-]? DIGIT+ ;
fragment DIGIT : [0-9] ;

// The one real lexical hazard (Design.md's Lexer section): '.' means decimal
// point in a bare NUMBER and named-output accessor inside a reference. Fixed
// by never letting the two lexing paths interleave - on seeing '#', this
// single rule (via ANTLR's own maximal-munch) greedily consumes the entire
// reference production - IDENTIFIER, colon-groups, then any run of
// subaccesses - as one opaque REFERENCE token, so '.' inside it is never
// offered to NUMBER's lexing path at all. The reference's own internal
// structure (id / colon segments / subaccesses) is decoded later by a
// hand-written decomposer, not by a second grammar rule here - see
// Design.md: "the reference grammar's own internal structure never has to
// round-trip through the general expression lexer/parser at all".
REFERENCE
    : '#' IDENT_FRAG (':' IDENT_FRAG)* SUBACCESS_FRAG*
    ;
fragment SUBACCESS_FRAG
    : '.' IDENT_FRAG
    | '[' INDEX_FRAG ']'
    ;
fragment INDEX_FRAG
    : SIGNED_INT_FRAG (':' SIGNED_INT_FRAG)?
    | '\'' (~['\r\n])* '\''
    ;
fragment SIGNED_INT_FRAG : '-'? DIGIT+ ;
fragment IDENT_FRAG      : [A-Za-z_][A-Za-z0-9_]* ;

IDENTIFIER : IDENT_FRAG ;

WS : [ \t\r\n]+ -> skip ;

// Catch-all so unrecognized characters surface as a normal ANTLR lexer error
// (caught and reported through Types-0001's {parse-message}) rather than the
// generated lexer silently skipping them.
ERRCHAR : . ;

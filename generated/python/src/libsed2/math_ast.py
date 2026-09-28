"""ASTNode: parses/serializes SED2 math strings into a tree and back
(Design.md's Math section). GENERATED for the libsed2 package - do not
hand-edit; regenerate via generator/generate.py. The grammar itself lives in
generator/math.g4; this module hand-builds the AST from the ANTLR parse
tree and re-serializes it, applying the libsbml-L3-infix-parser-derived
desugaring rules (relational-chain collapsing, n-ary and/or flattening, '%'
as rem()) that the grammar itself only describes informally."""
from __future__ import annotations

from dataclasses import dataclass, field as _field
from enum import Enum
from typing import Optional

from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from ._antlr.mathLexer import mathLexer
from ._antlr.mathParser import mathParser
from ._antlr.mathVisitor import mathVisitor


class MathSyntaxError(Exception):
    """Raised by parse()/ASTNode.parse() when the text isn't a well-formed
    SED2 math expression - the condition Types-0001 reports, with this
    exception's message as its {parse-message}."""


class ASTNodeType(Enum):
    NUMBER = "number"
    REFERENCE = "reference"
    NAME = "name"
    FUNCTION_CALL = "function-call"
    ARRAY = "array"
    UMINUS = "uminus"
    UPLUS = "uplus"
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    POW = "pow"


# Binding strength, used only so to_string() re-adds parentheses the source
# text may have relied on. Relational, logical and '%' all desugar to plain
# function calls (see Grammar) and a call's own parens make its arguments
# unambiguous, so only the five genuinely infix/prefix arithmetic shapes
# need this at all. Higher number binds tighter.
_PRECEDENCE = {
    ASTNodeType.ADD: 1,
    ASTNodeType.SUB: 1,
    ASTNodeType.MUL: 2,
    ASTNodeType.DIV: 2,
    ASTNodeType.UMINUS: 3,
    ASTNodeType.UPLUS: 3,
    ASTNodeType.POW: 4,
}
_ATOM_PRECEDENCE = 5  # NUMBER / REFERENCE / NAME / FUNCTION_CALL / ARRAY
_SYMBOL = {
    ASTNodeType.ADD: "+", ASTNodeType.SUB: "-",
    ASTNodeType.MUL: "*", ASTNodeType.DIV: "/", ASTNodeType.POW: "^",
}


@dataclass
class ASTNode:
    """Borrows the rough interface of libsbml's ASTNode, minus the XML
    dependency (Design.md's Math section)."""

    node_type: ASTNodeType
    text: Optional[str] = None        # NUMBER / REFERENCE: the raw source lexeme
    name: Optional[str] = None        # NAME / FUNCTION_CALL: the identifier
    children: list["ASTNode"] = _field(default_factory=list)

    def is_number(self) -> bool:
        return self.node_type is ASTNodeType.NUMBER

    def is_reference(self) -> bool:
        return self.node_type is ASTNodeType.REFERENCE

    def is_name(self) -> bool:
        return self.node_type is ASTNodeType.NAME

    def is_function_call(self) -> bool:
        return self.node_type is ASTNodeType.FUNCTION_CALL

    def get_num_children(self) -> int:
        return len(self.children)

    def get_child(self, index: int) -> "ASTNode":
        return self.children[index]

    def walk(self):
        """Depth-first iterator over this node and every descendant - the
        traversal a hand-written validate() uses for Types-0002 through
        Types-0004 (unknown function / bad arity / bare non-constant
        identifier)."""
        yield self
        for c in self.children:
            yield from c.walk()

    def to_string(self) -> str:
        return _render(self, 0)

    @staticmethod
    def parse(text: str) -> "ASTNode":
        return parse(text)


def _render(node: ASTNode, min_prec: int) -> str:
    t = node.node_type
    if t is ASTNodeType.NUMBER or t is ASTNodeType.REFERENCE:
        return node.text
    if t is ASTNodeType.NAME:
        return node.name
    if t is ASTNodeType.FUNCTION_CALL:
        return f"{node.name}({', '.join(_render(c, 0) for c in node.children)})"
    if t is ASTNodeType.ARRAY:
        return f"[{', '.join(_render(c, 0) for c in node.children)}]"
    if t is ASTNodeType.UMINUS or t is ASTNodeType.UPLUS:
        prec = _PRECEDENCE[t]
        inner = _render(node.children[0], prec)
        out = f"{'-' if t is ASTNodeType.UMINUS else '+'}{inner}"
        return f"({out})" if prec < min_prec else out
    prec = _PRECEDENCE[t]
    left, right = node.children
    if t is ASTNodeType.POW:  # right-associative
        left_s = _render(left, prec + 1)
        right_s = _render(right, prec)
    else:  # left-associative (ADD/SUB/MUL/DIV)
        left_s = _render(left, prec)
        right_s = _render(right, prec + 1)
    out = f"{left_s} {_SYMBOL[t]} {right_s}"
    return f"({out})" if prec < min_prec else out


_RELOP_KIND = {
    "==": "eq", "!=": "neq", "<>": "neq", "><": "neq",
    "<": "lt", ">": "gt", "<=": "leq", ">=": "geq",
}


def _build_relational(operands: list[ASTNode], kinds: list[str]) -> ASTNode:
    """a < b < c -> lt(a, b, c); a < b <= c -> and(lt(a, b), leq(b, c)) -
    consecutive identical relops merge into one n-ary call, a differing one
    starts a new run, and '!=' (however spelled) never merges into a run
    with anything, even another '!=' (Design.md: "!= is always binary and
    never joins a chain")."""
    if not kinds:
        return operands[0]
    runs: list[tuple[str, list[ASTNode]]] = []
    i = 0
    n = len(kinds)
    while i < n:
        kind = kinds[i]
        run_operands = [operands[i], operands[i + 1]]
        j = i + 1
        if kind != "neq":
            while j < n and kinds[j] == kind:
                run_operands.append(operands[j + 1])
                j += 1
        runs.append((kind, run_operands))
        i = j
    nodes = [ASTNode(ASTNodeType.FUNCTION_CALL, name=kind, children=run_operands)
             for kind, run_operands in runs]
    if len(nodes) == 1:
        return nodes[0]
    return ASTNode(ASTNodeType.FUNCTION_CALL, name="and", children=nodes)


def _flatten_logical(operands: list[ASTNode], ops: list[str]) -> ASTNode:
    """a && b && c -> and(a, b, c); a && b || c -> (a && b) || c, i.e.
    or(and(a, b), c) - one shared precedence level, left-associative, with
    runs of the *same* operator flattened into one n-ary call (Design.md's
    Grammar / precedence bullets)."""
    if not ops:
        return operands[0]
    groups: list[tuple[str, list[ASTNode]]] = []
    current_op = ops[0]
    current_operands = [operands[0], operands[1]]
    for i in range(1, len(ops)):
        if ops[i] == current_op:
            current_operands.append(operands[i + 1])
        else:
            groups.append((current_op, current_operands))
            current_op = ops[i]
            current_operands = [current_operands[-1], operands[i + 1]]
    groups.append((current_op, current_operands))
    result = ASTNode(ASTNodeType.FUNCTION_CALL, name=groups[0][0], children=groups[0][1])
    for op, opers in groups[1:]:
        result = ASTNode(ASTNodeType.FUNCTION_CALL, name=op, children=[result] + opers[1:])
    return result


class _Builder(mathVisitor):
    """Builds an ASTNode tree from the ANTLR parse tree, applying the
    desugaring in _build_relational()/_flatten_logical() above along the
    way - see Design.md's Grammar section (relational/logical/piecewise
    "follows libsbml's L3 infix parser", decided 2026-09-24)."""

    def visitStart(self, ctx):
        return self.visit(ctx.expr())

    def visitExpr(self, ctx):
        return self.visit(ctx.logical())

    def visitLogical(self, ctx):
        relationals = ctx.relational()
        if len(relationals) == 1:
            return self.visit(relationals[0])
        operands = [self.visit(r) for r in relationals]
        ops = ["and" if ctx.children[i].getText() == "&&" else "or"
               for i in range(1, len(ctx.children), 2)]
        return _flatten_logical(operands, ops)

    def visitRelational(self, ctx):
        additives = ctx.additive()
        if len(additives) == 1:
            return self.visit(additives[0])
        operands = [self.visit(a) for a in additives]
        kinds = [_RELOP_KIND[r.getText()] for r in ctx.relop()]
        return _build_relational(operands, kinds)

    def visitAdditive(self, ctx):
        muls = ctx.multiplicative()
        node = self.visit(muls[0])
        idx = 1
        for i in range(1, len(ctx.children), 2):
            op_text = ctx.children[i].getText()
            rhs = self.visit(muls[idx])
            idx += 1
            node = ASTNode(ASTNodeType.ADD if op_text == "+" else ASTNodeType.SUB,
                            children=[node, rhs])
        return node

    def visitMultiplicative(self, ctx):
        units = ctx.unary()
        node = self.visit(units[0])
        idx = 1
        for i in range(1, len(ctx.children), 2):
            op_text = ctx.children[i].getText()
            rhs = self.visit(units[idx])
            idx += 1
            if op_text == "*":
                node = ASTNode(ASTNodeType.MUL, children=[node, rhs])
            elif op_text == "/":
                node = ASTNode(ASTNodeType.DIV, children=[node, rhs])
            else:  # '%' is infix rem(), dividend's-sign semantics (Grammar)
                node = ASTNode(ASTNodeType.FUNCTION_CALL, name="rem", children=[node, rhs])
        return node

    def visitUnaryOp(self, ctx):
        op_text = ctx.getChild(0).getText()
        operand = self.visit(ctx.unary())
        if op_text == "!":
            return ASTNode(ASTNodeType.FUNCTION_CALL, name="not", children=[operand])
        return ASTNode(ASTNodeType.UMINUS if op_text == "-" else ASTNodeType.UPLUS,
                        children=[operand])

    def visitUnaryPower(self, ctx):
        return self.visit(ctx.power())

    def visitPower(self, ctx):
        base = self.visit(ctx.atom())
        if ctx.unary():
            return ASTNode(ASTNodeType.POW, children=[base, self.visit(ctx.unary())])
        return base

    def visitNumberAtom(self, ctx):
        return ASTNode(ASTNodeType.NUMBER, text=ctx.getText())

    def visitReferenceAtom(self, ctx):
        return ASTNode(ASTNodeType.REFERENCE, text=ctx.getText())

    def visitIdentAtom(self, ctx):
        return ASTNode(ASTNodeType.NAME, name=ctx.getText())

    def visitCallAtom(self, ctx):
        name = ctx.IDENTIFIER().getText()
        args = [self.visit(e) for e in (ctx.arglist().expr() if ctx.arglist() else [])]
        return ASTNode(ASTNodeType.FUNCTION_CALL, name=name, children=args)

    def visitArrayAtom(self, ctx):
        args = [self.visit(e) for e in (ctx.arglist().expr() if ctx.arglist() else [])]
        return ASTNode(ASTNodeType.ARRAY, children=args)

    def visitParenAtom(self, ctx):
        return self.visit(ctx.expr())


class _CollectingErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors: list[str] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"line {line}:{column} {msg}")


def parse(text: str) -> ASTNode:
    """Parses a SED2 math string into an ASTNode tree (Types-0001). Raises
    MathSyntaxError with the parser's own message on any malformed input."""
    listener = _CollectingErrorListener()
    lexer = mathLexer(InputStream(text))
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)
    stream = CommonTokenStream(lexer)
    parser = mathParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    tree = parser.start()
    if listener.errors:
        raise MathSyntaxError("; ".join(listener.errors))
    return _Builder().visit(tree)


def to_string(node: ASTNode) -> str:
    return node.to_string()

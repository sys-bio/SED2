package org.sedml.libsed2;

import org.sedml.libsed2.antlr.mathLexer;
import org.sedml.libsed2.antlr.mathParser;
import org.sedml.libsed2.antlr.mathBaseVisitor;
import org.antlr.v4.runtime.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** SED2 math-grammar AST + parser (Types-0001's "well-formed expression"
 * check and the shared tree the other three Types rules walk). GENERATED -
 * do not hand-edit; regenerate via generator/generate.py. */
public final class MathAst {
    private MathAst() {}

    public enum NodeType {
        NUMBER, REFERENCE, NAME, FUNCTION_CALL, ARRAY,
        UMINUS, UPLUS, ADD, SUB, MUL, DIV, POW
    }

    /** Borrows the rough interface of libsbml's ASTNode, minus the XML
     * dependency - same design note as emit_python.py's ASTNode. */
    public static final class Node {
        public final NodeType nodeType;
        public final String text;   // NUMBER / REFERENCE: the raw source lexeme
        public final String name;   // NAME / FUNCTION_CALL: the identifier
        public final List<Node> children;

        Node(NodeType nodeType, String text, String name, List<Node> children) {
            this.nodeType = nodeType;
            this.text = text;
            this.name = name;
            this.children = children;
        }

        public boolean isNumber() { return nodeType == NodeType.NUMBER; }
        public boolean isReference() { return nodeType == NodeType.REFERENCE; }
        public boolean isName() { return nodeType == NodeType.NAME; }
        public boolean isFunctionCall() { return nodeType == NodeType.FUNCTION_CALL; }
        public int getNumChildren() { return children.size(); }
        public Node getChild(int index) { return children.get(index); }

        /** Depth-first (this node first, then each child) - the traversal
         * MathRules.java uses for Types-0002 through Types-0004. */
        public List<Node> walk() {
            List<Node> out = new ArrayList<>();
            walkInto(out);
            return out;
        }

        private void walkInto(List<Node> out) {
            out.add(this);
            for (Node c : children) c.walkInto(out);
        }
    }

    /** Raised by parse() when the text isn't a well-formed SED2 math
     * expression - the condition Types-0001 reports, with this exception's
     * message as its {parse-message}. */
    public static final class MathSyntaxError extends RuntimeException {
        public MathSyntaxError(String message) { super(message); }
    }

    private static final Map<String, String> RELOP_KIND = Map.of(
            "==", "eq", "!=", "neq", "<>", "neq", "><", "neq",
            "<", "lt", ">", "gt", "<=", "leq", ">=", "geq");

    /** a < b < c -> lt(a, b, c); a < b <= c -> and(lt(a, b), leq(b, c)) -
     * see emit_python.py's _build_relational for the full rationale this
     * mirrors verbatim. */
    private static Node buildRelational(List<Node> operands, List<String> kinds) {
        if (kinds.isEmpty()) return operands.get(0);
        List<Node> runNodes = new ArrayList<>();
        int i = 0;
        int n = kinds.size();
        while (i < n) {
            String kind = kinds.get(i);
            List<Node> runOperands = new ArrayList<>();
            runOperands.add(operands.get(i));
            runOperands.add(operands.get(i + 1));
            int j = i + 1;
            if (!kind.equals("neq")) {
                while (j < n && kinds.get(j).equals(kind)) {
                    runOperands.add(operands.get(j + 1));
                    j++;
                }
            }
            runNodes.add(new Node(NodeType.FUNCTION_CALL, null, kind, runOperands));
            i = j;
        }
        if (runNodes.size() == 1) return runNodes.get(0);
        return new Node(NodeType.FUNCTION_CALL, null, "and", runNodes);
    }

    /** a && b && c -> and(a, b, c); a && b || c -> or(and(a, b), c) - see
     * emit_python.py's _flatten_logical for the full rationale this
     * mirrors verbatim. */
    private static Node flattenLogical(List<Node> operands, List<String> ops) {
        if (ops.isEmpty()) return operands.get(0);
        List<String> groupOps = new ArrayList<>();
        List<List<Node>> groupOperands = new ArrayList<>();
        String currentOp = ops.get(0);
        List<Node> currentOperands = new ArrayList<>();
        currentOperands.add(operands.get(0));
        currentOperands.add(operands.get(1));
        for (int i = 1; i < ops.size(); i++) {
            if (ops.get(i).equals(currentOp)) {
                currentOperands.add(operands.get(i + 1));
            } else {
                groupOps.add(currentOp);
                groupOperands.add(currentOperands);
                currentOp = ops.get(i);
                currentOperands = new ArrayList<>();
                currentOperands.add(groupOperands.get(groupOperands.size() - 1)
                        .get(groupOperands.get(groupOperands.size() - 1).size() - 1));
                currentOperands.add(operands.get(i + 1));
            }
        }
        groupOps.add(currentOp);
        groupOperands.add(currentOperands);
        Node result = new Node(NodeType.FUNCTION_CALL, null, groupOps.get(0), groupOperands.get(0));
        for (int g = 1; g < groupOps.size(); g++) {
            List<Node> children = new ArrayList<>();
            children.add(result);
            children.addAll(groupOperands.get(g).subList(1, groupOperands.get(g).size()));
            result = new Node(NodeType.FUNCTION_CALL, null, groupOps.get(g), children);
        }
        return result;
    }

    private static final class Builder extends mathBaseVisitor<Node> {
        @Override
        public Node visitStart(mathParser.StartContext ctx) { return visit(ctx.expr()); }

        @Override
        public Node visitExpr(mathParser.ExprContext ctx) { return visit(ctx.logical()); }

        @Override
        public Node visitLogical(mathParser.LogicalContext ctx) {
            List<mathParser.RelationalContext> relationals = ctx.relational();
            if (relationals.size() == 1) return visit(relationals.get(0));
            List<Node> operands = new ArrayList<>();
            for (mathParser.RelationalContext r : relationals) operands.add(visit(r));
            List<String> ops = new ArrayList<>();
            for (int i = 1; i < ctx.getChildCount(); i += 2) {
                ops.add(ctx.getChild(i).getText().equals("&&") ? "and" : "or");
            }
            return flattenLogical(operands, ops);
        }

        @Override
        public Node visitRelational(mathParser.RelationalContext ctx) {
            List<mathParser.AdditiveContext> additives = ctx.additive();
            if (additives.size() == 1) return visit(additives.get(0));
            List<Node> operands = new ArrayList<>();
            for (mathParser.AdditiveContext a : additives) operands.add(visit(a));
            List<String> kinds = new ArrayList<>();
            for (mathParser.RelopContext r : ctx.relop()) kinds.add(RELOP_KIND.get(r.getText()));
            return buildRelational(operands, kinds);
        }

        @Override
        public Node visitAdditive(mathParser.AdditiveContext ctx) {
            List<mathParser.MultiplicativeContext> muls = ctx.multiplicative();
            Node node = visit(muls.get(0));
            int idx = 1;
            for (int i = 1; i < ctx.getChildCount(); i += 2) {
                String opText = ctx.getChild(i).getText();
                Node rhs = visit(muls.get(idx));
                idx++;
                node = new Node(opText.equals("+") ? NodeType.ADD : NodeType.SUB, null, null, List.of(node, rhs));
            }
            return node;
        }

        @Override
        public Node visitMultiplicative(mathParser.MultiplicativeContext ctx) {
            List<mathParser.UnaryContext> units = ctx.unary();
            Node node = visit(units.get(0));
            int idx = 1;
            for (int i = 1; i < ctx.getChildCount(); i += 2) {
                String opText = ctx.getChild(i).getText();
                Node rhs = visit(units.get(idx));
                idx++;
                if (opText.equals("*")) {
                    node = new Node(NodeType.MUL, null, null, List.of(node, rhs));
                } else if (opText.equals("/")) {
                    node = new Node(NodeType.DIV, null, null, List.of(node, rhs));
                } else {
                    // infix '%' is rem(), dividend's-sign semantics (Grammar)
                    node = new Node(NodeType.FUNCTION_CALL, null, "rem", List.of(node, rhs));
                }
            }
            return node;
        }

        @Override
        public Node visitUnaryOp(mathParser.UnaryOpContext ctx) {
            String opText = ctx.getChild(0).getText();
            Node operand = visit(ctx.unary());
            if (opText.equals("!")) {
                return new Node(NodeType.FUNCTION_CALL, null, "not", List.of(operand));
            }
            return new Node(opText.equals("-") ? NodeType.UMINUS : NodeType.UPLUS, null, null, List.of(operand));
        }

        @Override
        public Node visitUnaryPower(mathParser.UnaryPowerContext ctx) { return visit(ctx.power()); }

        @Override
        public Node visitPower(mathParser.PowerContext ctx) {
            Node base = visit(ctx.atom());
            if (ctx.unary() != null) {
                return new Node(NodeType.POW, null, null, List.of(base, visit(ctx.unary())));
            }
            return base;
        }

        @Override
        public Node visitNumberAtom(mathParser.NumberAtomContext ctx) {
            return new Node(NodeType.NUMBER, ctx.getText(), null, List.of());
        }

        @Override
        public Node visitReferenceAtom(mathParser.ReferenceAtomContext ctx) {
            return new Node(NodeType.REFERENCE, ctx.getText(), null, List.of());
        }

        @Override
        public Node visitIdentAtom(mathParser.IdentAtomContext ctx) {
            return new Node(NodeType.NAME, null, ctx.getText(), List.of());
        }

        @Override
        public Node visitCallAtom(mathParser.CallAtomContext ctx) {
            String name = ctx.IDENTIFIER().getText();
            List<Node> args = new ArrayList<>();
            if (ctx.arglist() != null) {
                for (mathParser.ExprContext e : ctx.arglist().expr()) args.add(visit(e));
            }
            return new Node(NodeType.FUNCTION_CALL, null, name, args);
        }

        @Override
        public Node visitArrayAtom(mathParser.ArrayAtomContext ctx) {
            List<Node> args = new ArrayList<>();
            if (ctx.arglist() != null) {
                for (mathParser.ExprContext e : ctx.arglist().expr()) args.add(visit(e));
            }
            return new Node(NodeType.ARRAY, null, null, args);
        }

        @Override
        public Node visitParenAtom(mathParser.ParenAtomContext ctx) { return visit(ctx.expr()); }
    }

    /** The Java ANTLR runtime's DefaultErrorStrategy.recoverInline() reports a
     * failed match() against the state sync() last deferred at (its
     * nextTokensContext bookkeeping), so a trailing-junk error reads "expecting
     * {'&&', '||', ...}"; the Python runtime does not track that and reports
     * the set at the state that actually failed ("expecting <EOF>"). Python is
     * the reference implementation, so this strategy is recoverInline() minus
     * the deferred-state bookkeeping, keeping the parse-message text of
     * Types-0001 identical across targets. */
    private static final class SimpleErrorStrategy extends DefaultErrorStrategy {
        @Override
        public Token recoverInline(Parser recognizer) throws RecognitionException {
            Token matchedSymbol = singleTokenDeletion(recognizer);
            if (matchedSymbol != null) {
                recognizer.consume();
                return matchedSymbol;
            }
            if (singleTokenInsertion(recognizer)) return getMissingSymbol(recognizer);
            throw new InputMismatchException(recognizer);
        }
    }

    private static final class CollectingErrorListener extends BaseErrorListener {
        final List<String> errors = new ArrayList<>();

        @Override
        public void syntaxError(Recognizer<?, ?> recognizer, Object offendingSymbol, int line,
                                 int charPositionInLine, String msg, RecognitionException e) {
            errors.add("line " + line + ":" + charPositionInLine + " " + msg);
        }
    }

    /** Parses a SED2 math string into a Node tree (Types-0001). Throws
     * MathSyntaxError with the parser's own message on any malformed
     * input. */
    public static Node parse(String text) {
        CollectingErrorListener listener = new CollectingErrorListener();
        mathLexer lexer = new mathLexer(CharStreams.fromString(text));
        lexer.removeErrorListeners();
        lexer.addErrorListener(listener);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        mathParser parser = new mathParser(tokens);
        parser.setErrorHandler(new SimpleErrorStrategy());
        parser.removeErrorListeners();
        parser.addErrorListener(listener);
        mathParser.StartContext tree = parser.start();
        if (!listener.errors.isEmpty()) {
            throw new MathSyntaxError(String.join("; ", listener.errors));
        }
        return new Builder().visit(tree);
    }
}

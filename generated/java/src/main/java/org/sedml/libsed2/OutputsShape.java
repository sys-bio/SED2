package org.sedml.libsed2;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

/** outputs.json expr/valid notation (core-spec.md Section 8) - parser,
 * evaluator, and shape/hasSubvalue() resolver, backing SEDBase-0008 through
 * -0015 (Design.md's Validation section) and the formulaic ref-type rules
 * that piggyback on SEDBase-0015's scalar-reduction check. Java port of
 * OUTPUTS_SHAPE_PY in generator/emit_python.py (the reference
 * implementation); like it, a small runtime interpreter of the notation
 * rather than code compiled per suffix entry.
 *
 * Values inside an expression are plain Java objects mirroring the Python
 * ones: null (JSON null), Boolean, Long / BigInteger (integers), Double,
 * String, List (arrays and computed lists), Map (objects), Dim (a resolved
 * dimension), and the OUTERMOST sentinel. GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class OutputsShape {
    private OutputsShape() {}

    private static final ObjectMapper MAPPER = new ObjectMapper();

    /** Parses one class's embedded outputs.json text. */
    public static JsonNode parseJson(String text) {
        try {
            return MAPPER.readTree(text);
        } catch (java.io.IOException e) {
            throw new IllegalStateException("bad embedded outputs.json: " + e.getMessage(), e);
        }
    }

    /** Raised whenever an expr can't be evaluated against the target's own
     * literal fields - a reference where a literal was needed, a missing
     * attribute, an unresolvable shape dependency, a depth guard, and so on.
     * Every caller treats it as "the rule does not fire". */
    public static final class NotStatic extends RuntimeException {
        public NotStatic(String message) { super(message, null, false, false); }
    }

    /** Raised by indexIntoLiteral when the index chain can't be applied to a
     * constant's own literal structure - the signal SEDBase-0012 fires on. */
    public static final class NotIndexable extends RuntimeException {
        public final String bad;   // the failing index as Python would print it
        public final RefIndex index;   // the failing index, or null

        public NotIndexable(String bad) {
            this(bad, null);
        }

        public NotIndexable(String bad, RefIndex index) {
            super(bad, null, false, false);
            this.bad = bad;
            this.index = index;
        }
    }

    public static final Object OUTERMOST = new Object() {
        @Override public String toString() { return "OUTERMOST"; }
    };

    // ---- value helpers ---------------------------------------------------

    /** JSON -> the Java object model described in the class comment. */
    public static Object fromJson(JsonNode n) {
        if (n == null || n.isNull() || n.isMissingNode()) return null;
        if (n.isBoolean()) return n.booleanValue();
        if (n.isTextual()) return n.textValue();
        if (n.isIntegralNumber()) {
            BigInteger b = n.bigIntegerValue();
            return b.bitLength() < 64 ? (Object) b.longValue() : (Object) b;
        }
        if (n.isNumber()) return n.doubleValue();
        if (n.isArray()) {
            List<Object> out = new ArrayList<>();
            for (JsonNode c : n) out.add(fromJson(c));
            return out;
        }
        Map<String, Object> out = new LinkedHashMap<>();
        Iterator<Map.Entry<String, JsonNode>> it = n.fields();
        while (it.hasNext()) {
            Map.Entry<String, JsonNode> e = it.next();
            out.put(e.getKey(), fromJson(e.getValue()));
        }
        return out;
    }

    private static boolean isNumber(Object o) {
        return o instanceof Long || o instanceof BigInteger || o instanceof Double;
    }

    private static boolean isRefValue(Object o) {
        return o instanceof String && ((String) o).startsWith("#");
    }

    private static boolean isInt(Object o) { return o instanceof Long || o instanceof BigInteger; }

    private static double dbl(Object o) {
        if (o instanceof Long) return (Long) o;
        if (o instanceof BigInteger) return ((BigInteger) o).doubleValue();
        return (Double) o;
    }

    private static BigInteger big(Object o) {
        return o instanceof Long ? BigInteger.valueOf((Long) o) : (BigInteger) o;
    }

    private static Object normInt(BigInteger b) {
        return b.bitLength() < 64 ? (Object) b.longValue() : (Object) b;
    }

    /** Python truthiness. */
    static boolean truthy(Object o) {
        if (o == null) return false;
        if (o instanceof Boolean) return (Boolean) o;
        if (o instanceof Long) return (Long) o != 0L;
        if (o instanceof BigInteger) return ((BigInteger) o).signum() != 0;
        if (o instanceof Double) return (Double) o != 0.0;
        if (o instanceof String) return !((String) o).isEmpty();
        if (o instanceof List) return !((List<?>) o).isEmpty();
        if (o instanceof Map) return !((Map<?, ?>) o).isEmpty();
        return true;
    }

    private static Object numOfBool(Object o) {
        if (o instanceof Boolean) return ((Boolean) o) ? 1L : 0L;
        return o;
    }

    /** Python == over the value model (True == 1, 1 == 1.0). */
    static boolean pyEq(Object a, Object b) {
        a = numOfBool(a);
        b = numOfBool(b);
        if (a == null || b == null) return a == b;
        if (isNumber(a) && isNumber(b)) {
            if (isInt(a) && isInt(b)) return big(a).equals(big(b));
            return dbl(a) == dbl(b);
        }
        if (a instanceof String && b instanceof String) return a.equals(b);
        if (a instanceof List && b instanceof List) {
            List<?> x = (List<?>) a, y = (List<?>) b;
            if (x.size() != y.size()) return false;
            for (int i = 0; i < x.size(); i++) if (!pyEq(x.get(i), y.get(i))) return false;
            return true;
        }
        if (a instanceof Map && b instanceof Map) {
            Map<?, ?> x = (Map<?, ?>) a, y = (Map<?, ?>) b;
            if (x.size() != y.size()) return false;
            for (Map.Entry<?, ?> e : x.entrySet()) {
                if (!y.containsKey(e.getKey())) return false;
                if (!pyEq(e.getValue(), y.get(e.getKey()))) return false;
            }
            return true;
        }
        if (a instanceof Dim && b instanceof Dim) return a.equals(b);
        return a == b;
    }

    // ---- lexer -------------------------------------------------------------

    private static final class Tok {
        final String kind, text;
        Tok(String kind, String text) { this.kind = kind; this.text = text; }
        @Override public String toString() { return "(" + kind + ", " + text + ")"; }
    }

    private static List<Tok> tokenize(String text) {
        List<Tok> toks = new ArrayList<>();
        int i = 0, n = text.length();
        while (i < n) {
            char ch = text.charAt(i);
            if (Character.isWhitespace(ch)) { i++; continue; }
            if (ch == '=' && text.startsWith("==", i)) { toks.add(new Tok("==", "==")); i += 2; continue; }
            if ("+-!(),[].".indexOf(ch) >= 0) { toks.add(new Tok(String.valueOf(ch), String.valueOf(ch))); i++; continue; }
            if (isDigit(ch) || (ch == '.' && i + 1 < n && isDigit(text.charAt(i + 1)))) {
                int j = i;
                while (j < n && (isDigit(text.charAt(j)) || text.charAt(j) == '.')) j++;
                toks.add(new Tok("NUMBER", text.substring(i, j)));
                i = j;
                continue;
            }
            if (isAlpha(ch) || ch == '_') {
                int j = i;
                while (j < n && (isAlpha(text.charAt(j)) || isDigit(text.charAt(j)) || text.charAt(j) == '_')) j++;
                String word = text.substring(i, j);
                if (word.equals("true") || word.equals("false")) toks.add(new Tok("BOOL", word));
                else if (word.equals("or") || word.equals("if") || word.equals("else")) toks.add(new Tok(word, word));
                else toks.add(new Tok("IDENT", word));
                i = j;
                continue;
            }
            throw new NotStatic("unexpected character '" + ch + "' in expr '" + text + "'");
        }
        toks.add(new Tok("EOF", ""));
        return toks;
    }

    private static boolean isDigit(char c) { return c >= '0' && c <= '9'; }

    private static boolean isAlpha(char c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'); }

    // ---- AST ---------------------------------------------------------------

    interface Node {}
    record Num(Object value) implements Node {}
    record Bool(boolean value) implements Node {}
    record ArrayLit(List<Node> items) implements Node {}
    record Path(List<String> names) implements Node {}
    record Call(String func, List<Node> args) implements Node {}
    record UnaryNot(Node operand) implements Node {}
    record BinOp(String op, Node left, Node right) implements Node {}
    record Conditional(Node cond, Node then, Node orelse) implements Node {}

    private static final List<String> FUNCS = List.of("len", "keys", "shapeOf", "dim", "provided");

    private static final class Parser {
        private final List<Tok> toks;
        private int i = 0;

        Parser(List<Tok> toks) { this.toks = toks; }

        private Tok peek() { return toks.get(i); }

        private Tok eat(String kind) {
            Tok t = toks.get(i);
            if (!t.kind.equals(kind)) throw new NotStatic("expected " + kind + ", got " + t);
            i++;
            return t;
        }

        Node parse() {
            Node node = conditional();
            eat("EOF");
            return node;
        }

        private Node conditional() {
            Node node = orExpr();
            if (peek().kind.equals("if")) {
                eat("if");
                Node cond = orExpr();
                eat("else");
                Node orelse = conditional();
                return new Conditional(cond, node, orelse);
            }
            return node;
        }

        private Node orExpr() {
            Node node = equality();
            while (peek().kind.equals("or")) {
                eat("or");
                node = new BinOp("or", node, equality());
            }
            return node;
        }

        private Node equality() {
            Node node = additive();
            if (peek().kind.equals("==")) {
                eat("==");
                node = new BinOp("==", node, additive());
            }
            return node;
        }

        private Node additive() {
            Node node = unary();
            while (peek().kind.equals("+") || peek().kind.equals("-")) {
                String op = eat(peek().kind).kind;
                node = new BinOp(op, node, unary());
            }
            return node;
        }

        private Node unary() {
            if (peek().kind.equals("!")) {
                eat("!");
                return new UnaryNot(unary());
            }
            return primary();
        }

        private Node primary() {
            Tok t = peek();
            String kind = t.kind, text = t.text;
            if (kind.equals("NUMBER")) {
                eat("NUMBER");
                try {
                    if (text.contains(".")) return new Num(Double.parseDouble(text));
                    BigInteger b = new BigInteger(text);
                    return new Num(normInt(b));
                } catch (NumberFormatException e) {
                    throw new NotStatic("bad number '" + text + "'");
                }
            }
            if (kind.equals("BOOL")) {
                eat("BOOL");
                return new Bool(text.equals("true"));
            }
            if (kind.equals("[")) {
                eat("[");
                List<Node> items = new ArrayList<>();
                if (!peek().kind.equals("]")) {
                    items.add(conditional());
                    while (peek().kind.equals(",")) { eat(","); items.add(conditional()); }
                }
                eat("]");
                return new ArrayLit(items);
            }
            if (kind.equals("IDENT")) {
                String name = eat("IDENT").text;
                if (peek().kind.equals("(") && FUNCS.contains(name)) {
                    eat("(");
                    List<Node> args = new ArrayList<>();
                    if (!peek().kind.equals(")")) {
                        args.add(conditional());
                        while (peek().kind.equals(",")) { eat(","); args.add(conditional()); }
                    }
                    eat(")");
                    return new Call(name, args);
                }
                List<String> names = new ArrayList<>();
                names.add(name);
                while (peek().kind.equals(".")) { eat("."); names.add(eat("IDENT").text); }
                return new Path(names);
            }
            throw new NotStatic("unexpected token " + peek() + " in expr");
        }
    }

    private static final Map<String, Node> PARSE_CACHE = new HashMap<>();

    static Node parseExpr(String text) {
        synchronized (PARSE_CACHE) {
            Node node = PARSE_CACHE.get(text);
            if (node == null) {
                node = new Parser(tokenize(text)).parse();
                PARSE_CACHE.put(text, node);
            }
            return node;
        }
    }

    // ---- scopes --------------------------------------------------------------

    /** Bare identifiers resolve against a task's own raw JSON field values
     * (core-spec.md: "A bare identifier names one of the task's own
     * attributes and evaluates to its value"), or, inside a "repeat"
     * dimension, against the current array entry ("self" is the entry). */
    interface Scope {
        Object lookup(String name);
        boolean provided(String name);
    }

    private static final class FieldScope implements Scope {
        private final JsonNode fields;
        FieldScope(JsonNode fields) { this.fields = fields; }

        @Override public Object lookup(String name) {
            if (!fields.has(name)) throw new NotStatic("attribute '" + name + "' not provided");
            return fromJson(fields.get(name));
        }

        @Override public boolean provided(String name) { return fields.has(name); }
    }

    private static final class RepeatScope implements Scope {
        private final Object entry;
        RepeatScope(Object entry) { this.entry = entry; }

        @Override public Object lookup(String name) {
            if (name.equals("self")) return entry;
            if (!(entry instanceof Map) || !((Map<?, ?>) entry).containsKey(name)) {
                throw new NotStatic("attribute '" + name + "' not provided on repeat entry");
            }
            return ((Map<?, ?>) entry).get(name);
        }

        @Override public boolean provided(String name) {
            if (name.equals("self")) return true;
            return entry instanceof Map && ((Map<?, ?>) entry).containsKey(name);
        }
    }

    // ---- evaluation --------------------------------------------------------

    private static Object resolvePath(Path node, Scope scope) {
        if (node.names().get(0).equals("outermost")) {
            if (node.names().size() != 1) throw new NotStatic("outermost is not a container");
            return OUTERMOST;
        }
        Object value = scope.lookup(node.names().get(0));
        for (int i = 1; i < node.names().size(); i++) {
            String seg = node.names().get(i);
            if (!(value instanceof Map) || !((Map<?, ?>) value).containsKey(seg)) {
                throw new NotStatic("attribute '" + String.join(".", node.names()) + "' not provided");
            }
            value = ((Map<?, ?>) value).get(seg);
        }
        return value;
    }

    private static boolean isProvided(Node node, Scope scope) {
        if (!(node instanceof Path)) throw new NotStatic("provided() needs a bare identifier or dotted path");
        List<String> names = ((Path) node).names();
        if (names.get(0).equals("outermost")) return true;
        if (names.size() == 1) return scope.provided(names.get(0));
        Object value;
        try {
            value = scope.lookup(names.get(0));
        } catch (NotStatic e) {
            return false;
        }
        for (int i = 1; i < names.size() - 1; i++) {
            if (!(value instanceof Map) || !((Map<?, ?>) value).containsKey(names.get(i))) return false;
            value = ((Map<?, ?>) value).get(names.get(i));
        }
        return value instanceof Map && ((Map<?, ?>) value).containsKey(names.get(names.size() - 1));
    }

    private static Object fnLen(Object value) {
        if (value instanceof List) return (long) ((List<?>) value).size();
        if (value instanceof Map) {
            Map<?, ?> m = (Map<?, ?>) value;
            // Range-family dispatch (core-spec.md): len(x.values) if
            // provided(x.values) else x.numberOfSteps + 1; anything else
            // object-shaped is a plain SId-keyed map, so len() is its key
            // count.
            if (m.containsKey("values")) {
                Object values = m.get("values");
                if (values instanceof List) return (long) ((List<?>) values).size();
                throw new NotStatic("values is not a literal array");
            }
            if (m.containsKey("numberOfSteps")) {
                Object steps = m.get("numberOfSteps");
                if (isNumber(steps)) return toLongTrunc(steps) + 1;
                throw new NotStatic("numberOfSteps is not a literal number");
            }
            return (long) m.size();
        }
        throw new NotStatic("len() needs a literal array, object, or Range-family value");
    }

    private static long toLongTrunc(Object n) {
        if (n instanceof Long) return (Long) n;
        if (n instanceof BigInteger) return RefIndex.saturate((BigInteger) n);
        double d = (Double) n;
        if (Double.isNaN(d) || Double.isInfinite(d)) throw new NotStatic("non-finite number");
        return (long) d;
    }

    private static Object fnKeys(Object value) {
        if (!(value instanceof Map)) throw new NotStatic("keys() needs a literal object");
        return new ArrayList<Object>(((Map<?, ?>) value).keySet());
    }

    static Object eval(Node node, Scope scope, Function<String, List<Dim>> shapeOf) {
        if (node instanceof Num) return ((Num) node).value();
        if (node instanceof Bool) return ((Bool) node).value();
        if (node instanceof ArrayLit) {
            List<Object> out = new ArrayList<>();
            for (Node item : ((ArrayLit) node).items()) out.add(eval(item, scope, shapeOf));
            return out;
        }
        if (node instanceof Path) return resolvePath((Path) node, scope);
        if (node instanceof UnaryNot) return !truthy(eval(((UnaryNot) node).operand(), scope, shapeOf));
        if (node instanceof Call) {
            Call call = (Call) node;
            switch (call.func()) {
                case "provided":
                    if (call.args().size() != 1) throw new NotStatic("provided() takes exactly one argument");
                    return isProvided(call.args().get(0), scope);
                case "len":
                    if (call.args().isEmpty()) throw new NotStatic("len() takes one argument");
                    return fnLen(eval(call.args().get(0), scope, shapeOf));
                case "keys":
                    if (call.args().isEmpty()) throw new NotStatic("keys() takes one argument");
                    return fnKeys(eval(call.args().get(0), scope, shapeOf));
                case "shapeOf": {
                    if (call.args().isEmpty()) throw new NotStatic("shapeOf() takes one argument");
                    Object ref = eval(call.args().get(0), scope, shapeOf);
                    if (!(ref instanceof String) || !((String) ref).startsWith("#")) {
                        throw new NotStatic("shapeOf() needs a reference-valued operand");
                    }
                    return shapeOf.apply((String) ref);
                }
                case "dim": {
                    if (call.args().size() != 1) throw new NotStatic("dim() takes exactly one argument");
                    Object value = eval(call.args().get(0), scope, shapeOf);
                    if (value == OUTERMOST) {
                        List<Object> l = new ArrayList<>();
                        l.add(OUTERMOST);
                        return l;
                    }
                    if (value instanceof String) {
                        List<Object> l = new ArrayList<>();
                        l.add(value);
                        return l;
                    }
                    if (value instanceof List) return value;
                    throw new NotStatic("dim() needs a name or a list of names");
                }
                default:
                    throw new NotStatic("unknown function " + call.func() + "()");
            }
        }
        if (node instanceof BinOp) {
            BinOp b = (BinOp) node;
            if (b.op().equals("or")) {
                if (isProvided(b.left(), scope)) return eval(b.left(), scope, shapeOf);
                return eval(b.right(), scope, shapeOf);
            }
            Object left = eval(b.left(), scope, shapeOf);
            if (b.op().equals("-")) {
                Object right = eval(b.right(), scope, shapeOf);
                return applyDimMinus(left, right);
            }
            Object right = eval(b.right(), scope, shapeOf);
            if (b.op().equals("==")) {
                if (isRefValue(left) || isRefValue(right)) throw new NotStatic("== operand is a reference");
                return pyEq(left, right);
            }
            if (b.op().equals("+")) {
                if (left instanceof List && right instanceof List) {
                    List<Object> out = new ArrayList<>((List<?>) left);
                    out.addAll((List<?>) right);
                    return out;
                }
                if (isNumber(left) && isNumber(right)) {
                    if (isInt(left) && isInt(right)) return normInt(big(left).add(big(right)));
                    return dbl(left) + dbl(right);
                }
                throw new NotStatic("+ needs two arrays or two numbers");
            }
            throw new NotStatic("unknown operator " + b.op());
        }
        if (node instanceof Conditional) {
            Conditional c = (Conditional) node;
            if (truthy(eval(c.cond(), scope, shapeOf))) return eval(c.then(), scope, shapeOf);
            return eval(c.orelse(), scope, shapeOf);
        }
        throw new NotStatic("unknown AST node " + node);
    }

    /** shapeOf(x) - dim(y): a dims list (see resolveDims) with the
     * dimension(s) named by `selectors` removed. Only the reserved
     * `outermost` sentinel removes a SPECIFIC, still-fully-known dimension
     * (the first); anything else can only shrink the known dimension COUNT,
     * with the remaining dimensions' own details marked unknown. */
    private static Object applyDimMinus(Object dims, Object selectors) {
        if (dims == null) return null;
        if (!(dims instanceof List)) throw new NotStatic("- needs a dimensions list on the left");
        List<?> d = (List<?>) dims;
        int count = selectors instanceof List ? ((List<?>) selectors).size() : 1;
        if (count >= d.size()) return new ArrayList<Object>();
        if (selectors instanceof List && ((List<?>) selectors).size() == 1
                && ((List<?>) selectors).get(0) == OUTERMOST) {
            return new ArrayList<Object>(d.subList(1, d.size()));
        }
        List<Object> out = new ArrayList<>();
        for (int i = 0; i < d.size() - count; i++) out.add(new Dim(null, null, "runtime", null));
        return out;
    }

    // ---- outputs.json "sourced" value resolution ---------------------------

    private static String text(JsonNode n) {
        return (n != null && n.isTextual()) ? n.textValue() : null;
    }

    private static Long sizeOf(JsonNode n) {
        if (n == null || !n.isNumber()) return null;
        return n.isIntegralNumber() ? Long.valueOf(RefIndex.saturate(n.bigIntegerValue())) : Long.valueOf((long) n.doubleValue());
    }

    private static Long evalSourcedSize(JsonNode sourced, Scope scope, Function<String, List<Dim>> shapeOf) {
        if (sourced == null || sourced.isNull()) return null;
        if (!"static".equals(text(sourced.get("source")))) return null;   // runtime / input-file
        Object value;
        try {
            value = eval(parseExpr(text(sourced.get("expr"))), scope, shapeOf);
        } catch (NotStatic | NullPointerException e) {
            return null;
        }
        if (isNumber(value)) {
            try {
                return toLongTrunc(value);
            } catch (NotStatic e) {
                return null;
            }
        }
        return null;
    }

    /** null (JSON null) means "no labels for this dimension" - statically
     * known as empty, not "unresolvable" - so this returns an empty list for
     * that case, reserving null for a genuine failure to resolve. */
    @SuppressWarnings("unchecked")
    private static List<String> evalSourcedLabels(JsonNode spec, Scope scope, Function<String, List<Dim>> shapeOf) {
        if (spec == null || spec.isNull()) return new ArrayList<>();
        if (spec.isArray()) {
            List<String> out = new ArrayList<>();
            for (JsonNode c : spec) {
                if (!c.isTextual()) return null;
                out.add(c.textValue());
            }
            return out;
        }
        if (spec.isObject()) {
            if (!"static".equals(text(spec.get("source")))) return null;
            Object value;
            try {
                value = eval(parseExpr(text(spec.get("expr"))), scope, shapeOf);
            } catch (NotStatic | NullPointerException e) {
                return null;
            }
            if (value instanceof List) {
                List<String> out = new ArrayList<>();
                for (Object v : (List<Object>) value) {
                    if (!(v instanceof String)) return null;
                    out.add((String) v);
                }
                return out;
            }
            return null;
        }
        return null;
    }

    /** dimsSpec is outputs.json's own "dimensions" value for one suffix entry
     * - either a fixed-length array of per-dimension entries, or a single
     * "sourced" object describing the whole shape. Returns one Dim per
     * dimension, in order, or null when the dimension COUNT itself isn't
     * statically known. */
    @SuppressWarnings("unchecked")
    static List<Dim> resolveDims(JsonNode dimsSpec, Scope scope, Function<String, List<Dim>> shapeOf) {
        if (dimsSpec == null || dimsSpec.isNull()) return null;
        if (dimsSpec.isArray()) {
            List<Dim> result = new ArrayList<>();
            for (JsonNode d : dimsSpec) {
                if (d.has("repeat")) {
                    JsonNode rep = d.get("repeat");
                    Object overVal;
                    try {
                        overVal = scope.lookup(text(rep.get("over")));
                    } catch (NotStatic | NullPointerException e) {
                        return null;
                    }
                    if (!(overVal instanceof List)) return null;
                    for (Object item : (List<Object>) overVal) {
                        Scope itemScope = new RepeatScope(item);
                        JsonNode size = rep.get("size");
                        result.add(new Dim(evalSourcedSize(size, itemScope, shapeOf),
                                evalSourcedLabels(rep.get("labels"), itemScope, shapeOf),
                                text(size.get("source")), sizeOf(size.get("min"))));
                    }
                } else {
                    JsonNode size = d.get("size");
                    result.add(new Dim(evalSourcedSize(size, scope, shapeOf),
                            evalSourcedLabels(d.get("labels"), scope, shapeOf),
                            text(size.get("source")), sizeOf(size.get("min"))));
                }
            }
            return result;
        }
        // single sourced object - the whole shape's derivation
        if (!"static".equals(text(dimsSpec.get("source")))) return null;
        Object value;
        try {
            value = eval(parseExpr(text(dimsSpec.get("expr"))), scope, shapeOf);
        } catch (NotStatic | NullPointerException e) {
            return null;
        }
        if (!(value instanceof List)) return null;
        List<Dim> out = new ArrayList<>();
        for (Object o : (List<Object>) value) {
            if (!(o instanceof Dim)) return null;
            out.add((Dim) o);
        }
        return out;
    }

    /** Splits a reference's index list into its brackets: "[0:2, 1][3]" is
     * two groups, [0:2, 1] and [3] (RefIndex.sameBracket marks an index that
     * continues the previous one's bracket). */
    public static List<List<RefIndex>> indexGroups(List<RefIndex> indexAccessors) {
        List<List<RefIndex>> groups = new ArrayList<>();
        for (RefIndex idx : indexAccessors) {
            if (idx.sameBracket && !groups.isEmpty()) {
                groups.get(groups.size() - 1).add(idx);
            } else {
                List<RefIndex> g = new ArrayList<>();
                g.add(idx);
                groups.add(g);
            }
        }
        return groups;
    }

    /** The dimension a range index leaves behind: as many entries as the
     * range selects, with the matching labels. Whatever can't be told
     * statically (a runtime size, an out-of-bounds or empty range - the
     * latter is SEDBase-0011's to report) becomes unknown, so later indices
     * are not judged against a guess. */
    private static Dim slicedDim(Dim dim, RefIndex idx) {
        Long n = dim.size;
        Long a = idx.rangeStart, b = idx.rangeEnd;
        boolean ok = n != null && !(a != null && !(-n <= a && a <= n)) && !(b != null && !(-n <= b && b <= n));
        long ea = 0, eb = 0;
        if (ok) {
            ea = a != null ? a : 0;
            eb = b != null ? b : n;
            if (ea < 0) ea += n;
            if (eb < 0) eb += n;
            ok = ea < eb;
        }
        if (!ok) return new Dim(null, null, dim.source, null);
        List<String> labels = null;
        // An unlabeled dimension is stored as an empty label list and stays that
        // way; otherwise the labels of the selected entries are kept.
        if (dim.labels != null && dim.labels.isEmpty()) labels = new ArrayList<>();
        else if (dim.labels != null && dim.labels.size() == n) labels = new ArrayList<>(dim.labels.subList((int) ea, (int) eb));
        return new Dim(eb - ea, labels, dim.source, null);
    }

    /** The result of bindIndices: see that method. */
    public static final class Bound {
        public final List<Dim> seen;
        public final List<Dim> after;

        Bound(List<Dim> seen, List<Dim> after) {
            this.seen = seen;
            this.after = after;
        }
    }

    /** Applies a reference's own bracket indices to a resolved dims list.
     * Separate brackets chain (each applies to the result of the one before:
     * "[0:2][1]" indexes the first dimension twice); the indices inside one
     * bracket apply to consecutive dimensions ("[0:2, 1]" - numpy style). A
     * positional/label index drops its dimension from the result; a range
     * keeps it, narrowed to the entries it selects; dimensions no index
     * reaches pass through untouched. `seen` has one entry per index, in
     * order - the dimension that index is applied to, as the earlier indices
     * left it - and stops short when an index finds no dimension left
     * (SEDBase-0009); `after` is the dimensions of the result. Both null when
     * dims is null. */
    public static Bound bindIndices(List<Dim> dims, List<RefIndex> indexAccessors) {
        if (dims == null) return new Bound(null, null);
        List<Dim> view = new ArrayList<>(dims);
        List<Dim> seen = new ArrayList<>();
        for (List<RefIndex> group : indexGroups(indexAccessors)) {
            int k = Math.min(group.size(), view.size());
            seen.addAll(view.subList(0, k));
            if (k < group.size()) break;
            List<Dim> next = new ArrayList<>();
            for (int j = 0; j < view.size(); j++) {
                if (j < k) {
                    if (group.get(j).kind.equals("range")) next.add(slicedDim(view.get(j), group.get(j)));
                } else {
                    next.add(view.get(j));
                }
            }
            view = next;
        }
        return new Bound(seen, view);
    }

    static List<Dim> applyIndexChain(List<Dim> dims, List<RefIndex> indexAccessors) {
        return bindIndices(dims, indexAccessors).after;
    }

    /** A suffix entry that is listed in outputs.json is valid; one that isn't
     * listed is not (resolveOutput handles that). An entry's optional "valid"
     * field is a boolean expr string over the task's own fields meaning
     * "valid if"; no "valid" field means always valid. Returns TRUE/FALSE, or
     * null when the expr couldn't be evaluated statically ("the rule does not
     * fire"). */
    static Boolean evalValid(JsonNode entry, Scope scope, Function<String, List<Dim>> shapeOf) {
        JsonNode valid = entry.get("valid");
        if (valid == null) return Boolean.TRUE;
        if (valid.isTextual()) {
            try {
                return truthy(eval(parseExpr(valid.textValue()), scope, shapeOf));
            } catch (NotStatic e) {
                return null;
            }
        }
        return Boolean.FALSE;
    }

    /** The result of resolveOutput: see that method. */
    public static final class Resolution {
        /** TRUE (suffix is listed and has no "valid" field, or its "valid"
         * ("valid if") expr evaluated true), FALSE (not listed, or the expr
         * evaluates false), or null (couldn't be determined statically). */
        public final Boolean ok;
        public final JsonNode entry;            // the raw outputEntry, or null when the suffix key is absent
        public final List<Dim> dimsBefore;      // null unless ok == TRUE and the entry has resolvable "dimensions"
        public final List<Dim> dimsAfter;       // dimsBefore after the index chain
        public final String dotName;            // first dot-accessor, or null for a bare [id] reference
        public final List<RefIndex> indexAccessors;

        Resolution(Boolean ok, JsonNode entry, List<Dim> dimsBefore, List<Dim> dimsAfter, String dotName,
                   List<RefIndex> indexAccessors) {
            this.ok = ok;
            this.entry = entry;
            this.dimsBefore = dimsBefore;
            this.dimsAfter = dimsAfter;
            this.dotName = dotName;
            this.indexAccessors = indexAccessors;
        }
    }

    /** The core hasSubvalue()-style resolution SEDBase-0008 through -0011 /
     * -0014 / -0015 and the ref-type rules all share. outputsJson is a
     * concrete tasks/ class's own parsed outputs.json ({"outputs": {...}});
     * fields is the referenced task's own JSON value; accessors is a
     * ParsedReference's own accessor list. */
    public static Resolution resolveOutput(JsonNode outputsJson, JsonNode fields,
                                           List<ParsedReference.Accessor> accessors,
                                           Function<String, List<Dim>> shapeOf) {
        String dotName = null;
        List<RefIndex> indexAccessors = new ArrayList<>();
        for (ParsedReference.Accessor a : accessors) {
            if (a.isDot() && dotName == null) dotName = a.dotName;
            else if (!a.isDot()) indexAccessors.add(a.index);
        }
        String suffixKey = dotName == null ? "[id]" : "[id]." + dotName;
        JsonNode outputs = outputsJson == null ? null : outputsJson.get("outputs");
        JsonNode entry = outputs == null ? null : outputs.get(suffixKey);
        if (entry == null) return new Resolution(Boolean.FALSE, null, null, null, dotName, indexAccessors);
        Scope scope = new FieldScope(fields);
        Boolean ok = evalValid(entry, scope, shapeOf);
        if (!Boolean.TRUE.equals(ok)) return new Resolution(ok, entry, null, null, dotName, indexAccessors);
        List<Dim> dimsBefore = resolveDims(entry.get("dimensions"), scope, shapeOf);
        List<Dim> dimsAfter = applyIndexChain(dimsBefore, indexAccessors);
        return new Resolution(Boolean.TRUE, entry, dimsBefore, dimsAfter, dotName, indexAccessors);
    }

    // ---- SEDBase-0012: indexing into a constant's own literal JSON value ---

    /** core-spec.md / SEDBase-0012.md: constants have no outputs.json, their
     * "shape" is just their own literal JSON value. Applies an index chain
     * directly against it; `value` is the (already dereferenced) literal - a
     * JsonNode, or anything else (a document element, null) which is simply
     * not indexable. Throws NotIndexable the moment an index can't apply;
     * returns the fully-indexed value otherwise. */
    public static Object indexIntoLiteral(Object value, List<RefIndex> indexAccessors) {
        Object cur = value;
        for (List<RefIndex> group : indexGroups(indexAccessors)) cur = applyBracket(cur, group, 0);
        return cur;
    }

    private static NotIndexable notIndexable(RefIndex idx) {
        String bad;
        switch (idx.kind) {
            case "label": bad = idx.label; break;
            case "int": bad = idx.intText; break;
            case "range":
                bad = "(" + (idx.rangeStartText == null ? "None" : idx.rangeStartText) + ", "
                        + (idx.rangeEndText == null ? "None" : idx.rangeEndText) + ")";
                break;
            default: bad = idx.valueText();
        }
        return new NotIndexable(bad, idx);
    }

    /** One bracket's indices against a literal: the first applies to cur
     * itself, the rest to the corresponding dimension of what it selects (a
     * range selects several entries, so the rest applies inside each). */
    private static Object applyBracket(Object cur, List<RefIndex> group, int from) {
        if (from >= group.size()) return cur;
        RefIndex idx = group.get(from);
        JsonNode node = cur instanceof JsonNode ? (JsonNode) cur : null;
        switch (idx.kind) {
            case "label":
                if (node == null || !node.isObject() || !node.has(idx.label)) throw notIndexable(idx);
                return applyBracket(node.get(idx.label), group, from + 1);
            case "int": {
                if (node == null || !node.isArray()) throw notIndexable(idx);
                long n = node.size();
                long i = idx.intValue;
                if (i < -n || i >= n) throw notIndexable(idx);
                return applyBracket(node.get((int) (i < 0 ? i + n : i)), group, from + 1);
            }
            case "range": {
                if (node == null || !node.isArray()) throw notIndexable(idx);
                long n = node.size();
                long ea = idx.rangeStart != null ? idx.rangeStart : 0;
                long eb = idx.rangeEnd != null ? idx.rangeEnd : n;
                if (ea < 0) ea += n;
                if (eb < 0) eb += n;
                ea = Math.max(ea, 0);
                eb = Math.max(eb, 0);
                ArrayNode out = JsonNodeFactory.instance.arrayNode();
                for (long k = ea; k < Math.min(eb, n); k++) {
                    JsonNode el = node.get((int) k);
                    out.add(from + 1 >= group.size() ? el : (JsonNode) applyBracket(el, group, from + 1));
                }
                return out;
            }
            default:
                throw notIndexable(idx);
        }
    }
}

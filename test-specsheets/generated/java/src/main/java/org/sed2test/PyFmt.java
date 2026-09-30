package org.sed2test;

import com.fasterxml.jackson.databind.JsonNode;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/** Python-compatible text rendering of parsed JSON values, so a validation
 * message reads identically across the Python, Java and C++ targets (the
 * reference implementation formats placeholders with Python's str(), and a
 * literal with json.dumps()). GENERATED - do not hand-edit; regenerate via
 * generator/generate.py. */
public final class PyFmt {
    private PyFmt() {}

    /** Python's repr() of a float (shortest round-trip digits, exponent form
     * outside 1e-4 .. 1e16). */
    public static String floatRepr(double d) {
        if (Double.isNaN(d)) return "nan";
        if (Double.isInfinite(d)) return d > 0 ? "inf" : "-inf";
        if (d == 0.0) return (1.0 / d < 0) ? "-0.0" : "0.0";
        String sign = d < 0 ? "-" : "";
        BigDecimal bd = new BigDecimal(Double.toString(Math.abs(d))).stripTrailingZeros();
        String digits = bd.unscaledValue().toString();
        int decpt = digits.length() - bd.scale();   // value = 0.DIGITS * 10^decpt
        String out;
        if (decpt > 16 || decpt <= -4) {
            int exp = decpt - 1;
            String mant = digits.length() > 1 ? digits.charAt(0) + "." + digits.substring(1) : digits;
            String es = Integer.toString(Math.abs(exp));
            if (es.length() < 2) es = "0" + es;
            out = mant + "e" + (exp < 0 ? "-" : "+") + es;
        } else if (decpt <= 0) {
            out = "0." + "0".repeat(-decpt) + digits;
        } else if (decpt >= digits.length()) {
            out = digits + "0".repeat(decpt - digits.length()) + ".0";
        } else {
            out = digits.substring(0, decpt) + "." + digits.substring(decpt);
        }
        return sign + out;
    }

    private static boolean printable(int cp) {
        int t = Character.getType(cp);
        switch (t) {
            case Character.CONTROL: case Character.FORMAT: case Character.SURROGATE:
            case Character.PRIVATE_USE: case Character.UNASSIGNED:
            case Character.LINE_SEPARATOR: case Character.PARAGRAPH_SEPARATOR:
                return false;
            case Character.SPACE_SEPARATOR:
                return cp == 0x20;
            default:
                return true;
        }
    }

    /** Python's repr() of a str. */
    public static String reprStr(String s) {
        boolean hasSingle = s.indexOf('\'') >= 0, hasDouble = s.indexOf('"') >= 0;
        char q = (hasSingle && !hasDouble) ? '"' : '\'';
        StringBuilder sb = new StringBuilder();
        sb.append(q);
        for (int i = 0; i < s.length(); ) {
            int cp = s.codePointAt(i);
            i += Character.charCount(cp);
            if (cp == q || cp == '\\') { sb.append('\\').appendCodePoint(cp); }
            else if (cp == '\n') sb.append("\\n");
            else if (cp == '\r') sb.append("\\r");
            else if (cp == '\t') sb.append("\\t");
            else if (cp < 0x20 || cp == 0x7f) sb.append(String.format("\\x%02x", cp));
            else if (cp < 0x7f || printable(cp)) sb.appendCodePoint(cp);
            else if (cp <= 0xff) sb.append(String.format("\\x%02x", cp));
            else if (cp <= 0xffff) sb.append(String.format("\\u%04x", cp));
            else sb.append(String.format("\\U%08x", cp));
        }
        sb.append(q);
        return sb.toString();
    }

    /** Python's repr() of the value json.loads() would produce for `n`. */
    public static String repr(JsonNode n) {
        if (n == null || n.isNull() || n.isMissingNode()) return "None";
        if (n.isBoolean()) return n.booleanValue() ? "True" : "False";
        if (n.isTextual()) return reprStr(n.textValue());
        if (n.isIntegralNumber()) return n.bigIntegerValue().toString();
        if (n.isNumber()) return floatRepr(n.doubleValue());
        StringBuilder sb = new StringBuilder();
        if (n.isArray()) {
            sb.append('[');
            boolean first = true;
            for (JsonNode c : n) { if (!first) sb.append(", "); first = false; sb.append(repr(c)); }
            return sb.append(']').toString();
        }
        sb.append('{');
        boolean first = true;
        Iterator<Map.Entry<String, JsonNode>> it = n.fields();
        while (it.hasNext()) {
            Map.Entry<String, JsonNode> e = it.next();
            if (!first) sb.append(", ");
            first = false;
            sb.append(reprStr(e.getKey())).append(": ").append(repr(e.getValue()));
        }
        return sb.append('}').toString();
    }

    /** Python's str() of the value json.loads() would produce for `n`. */
    public static String str(JsonNode n) {
        if (n != null && n.isTextual()) return n.textValue();
        return repr(n);
    }

    /** Python's str() of a placeholder value: a String is itself, a JsonNode
     * renders as its parsed Python value, a Boolean as True/False, null as
     * None. */
    public static String str(Object o) {
        if (o == null) return "None";
        if (o instanceof String) return (String) o;
        if (o instanceof JsonNode) return str((JsonNode) o);
        if (o instanceof Boolean) return ((Boolean) o) ? "True" : "False";
        if (o instanceof Double || o instanceof Float) return floatRepr(((Number) o).doubleValue());
        if (o instanceof List) {
            StringBuilder sb = new StringBuilder("[");
            boolean first = true;
            for (Object x : (List<?>) o) {
                if (!first) sb.append(", ");
                first = false;
                sb.append(x instanceof String ? reprStr((String) x) : str(x));
            }
            return sb.append(']').toString();
        }
        return String.valueOf(o);
    }

    private static void jsonString(StringBuilder sb, String s) {
        sb.append('"');
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"': sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                case '\b': sb.append("\\b"); break;
                case '\f': sb.append("\\f"); break;
                default:
                    if (c < 0x20 || c > 0x7e) sb.append(String.format("\\u%04x", (int) c));
                    else sb.append(c);
            }
        }
        sb.append('"');
    }

    /** Python's json.dumps() (default separators, ensure_ascii) of `n`. */
    public static String jsonDumps(JsonNode n) {
        StringBuilder sb = new StringBuilder();
        dumps(sb, n);
        return sb.toString();
    }

    private static void dumps(StringBuilder sb, JsonNode n) {
        if (n == null || n.isNull() || n.isMissingNode()) { sb.append("null"); return; }
        if (n.isBoolean()) { sb.append(n.booleanValue() ? "true" : "false"); return; }
        if (n.isTextual()) { jsonString(sb, n.textValue()); return; }
        if (n.isIntegralNumber()) { sb.append(n.bigIntegerValue().toString()); return; }
        if (n.isNumber()) {
            double d = n.doubleValue();
            if (Double.isNaN(d)) sb.append("NaN");
            else if (Double.isInfinite(d)) sb.append(d > 0 ? "Infinity" : "-Infinity");
            else sb.append(floatRepr(d));
            return;
        }
        if (n.isArray()) {
            sb.append('[');
            boolean first = true;
            for (JsonNode c : n) { if (!first) sb.append(", "); first = false; dumps(sb, c); }
            sb.append(']');
            return;
        }
        sb.append('{');
        boolean first = true;
        Iterator<Map.Entry<String, JsonNode>> it = n.fields();
        while (it.hasNext()) {
            Map.Entry<String, JsonNode> e = it.next();
            if (!first) sb.append(", ");
            first = false;
            jsonString(sb, e.getKey());
            sb.append(": ");
            dumps(sb, e.getValue());
        }
        sb.append('}');
    }

    /** str() of an integer as Python would print it. */
    public static String intStr(BigInteger b) { return b.toString(); }
}

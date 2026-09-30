package org.sed2test;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.networknt.schema.JsonSchema;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.SpecVersion;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

/** Per-field leaf validation, via the real JSON Schema validator
 * (networknt's json-schema-validator, per Design.md's Toolchain mandate) -
 * a tiny schema fragment is built from one already-resolved field's own
 * type, never a whole-document schema, since every combinator has already
 * been resolved away by the generator at compose time (see
 * generator/spec.py). GENERATED - do not hand-edit. */
public final class LeafValidation {
    private static final JsonSchemaFactory FACTORY =
            JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V202012);

    public static final String SID_PATTERN = "^[A-Za-z_][A-Za-z0-9_]*$";
    public static final String SIDREF_PATTERN = "^#.*$";

    private LeafValidation() {}

    private static ObjectNode baseSchema(String kind) {
        ObjectNode n = JsonNodeFactory.instance.objectNode();
        switch (kind) {
            case "string":
                n.put("type", "string");
                break;
            case "integer":
                n.put("type", "integer");
                break;
            case "number":
                n.put("type", "number");
                break;
            case "boolean":
                n.put("type", "boolean");
                break;
            case "SId":
                n.put("type", "string");
                n.put("pattern", SID_PATTERN);
                break;
            case "SIdRef":
                n.put("type", "string");
                n.put("pattern", SIDREF_PATTERN);
                break;
            case "StringOrRef": {
                ArrayNode any = n.putArray("anyOf");
                ObjectNode s = JsonNodeFactory.instance.objectNode();
                s.put("type", "string");
                any.add(s);
                break;
            }
            case "NumberOrRef": {
                ArrayNode any = n.putArray("anyOf");
                ObjectNode num = JsonNodeFactory.instance.objectNode();
                num.put("type", "number");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(num);
                any.add(ref);
                break;
            }
            case "IntegerOrRef": {
                ArrayNode any = n.putArray("anyOf");
                ObjectNode val = JsonNodeFactory.instance.objectNode();
                val.put("type", "integer");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(val);
                any.add(ref);
                break;
            }
            case "BooleanOrRef": {
                ArrayNode any = n.putArray("anyOf");
                ObjectNode val = JsonNodeFactory.instance.objectNode();
                val.put("type", "boolean");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(val);
                any.add(ref);
                break;
            }
            case "ArrayOrRef": {
                ArrayNode any = n.putArray("anyOf");
                ObjectNode val = JsonNodeFactory.instance.objectNode();
                val.put("type", "array");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(val);
                any.add(ref);
                break;
            }
            case "DictOrRef": {
                ArrayNode any = n.putArray("anyOf");
                ObjectNode val = JsonNodeFactory.instance.objectNode();
                val.put("type", "object");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(val);
                any.add(ref);
                break;
            }
            default:
                throw new IllegalArgumentException("unknown leaf kind: " + kind);
        }
        return n;
    }

    /** Java port of emit_python.py's leaf_schema_for(): the per-field schema
     * fragment for one already-resolved field type. minimum/exclusiveMinimum
     * are numeric-only JSON Schema keywords - a no-op against a non-numeric
     * instance (a reference string, for an *OrRef kind) - so bolting them on
     * at the top level is always safe. pattern/minLength/enum are STRING-only
     * keywords, and a StringOrRef's reference form is *also* a plain string,
     * so for that kind the literal value's constraints are split into their
     * own anyOf branch beside a reference-shaped string, rather than
     * incorrectly rejecting a perfectly valid reference. */
    static ObjectNode leafSchemaFor(String kind, Double minimum, Double exclusiveMinimum, String pattern,
                                    Integer minLength, List<String> enumValues) {
        ObjectNode base = baseSchema(kind);
        if (minimum != null) base.put("minimum", minimum);
        if (exclusiveMinimum != null) base.put("exclusiveMinimum", exclusiveMinimum);
        boolean hasStringConstraints = pattern != null || minLength != null || enumValues != null;
        if (hasStringConstraints) {
            ObjectNode constraints = JsonNodeFactory.instance.objectNode();
            if (pattern != null) constraints.put("pattern", pattern);
            if (minLength != null) constraints.put("minLength", minLength);
            if (enumValues != null) {
                ArrayNode en = constraints.putArray("enum");
                for (String v : enumValues) en.add(v);
            }
            if (kind.equals("StringOrRef")) {
                ObjectNode wrapped = JsonNodeFactory.instance.objectNode();
                ArrayNode any = wrapped.putArray("anyOf");
                ObjectNode lit = JsonNodeFactory.instance.objectNode();
                lit.put("type", "string");
                lit.setAll(constraints);
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(lit);
                any.add(ref);
                return wrapped;
            }
            base.setAll(constraints);
        }
        return base;
    }

    // Compiled schemas, keyed by the schema's own text - a document has many
    // fields of a handful of distinct shapes.
    private static final Map<String, JsonSchema> SCHEMA_CACHE = new ConcurrentHashMap<>();

    public static boolean leafValueOk(String kind, JsonNode value, Double minimum, Double exclusiveMinimum,
                                      String pattern, Integer minLength, List<String> enumValues) {
        ObjectNode schema = leafSchemaFor(kind, minimum, exclusiveMinimum, pattern, minLength, enumValues);
        JsonSchema s = SCHEMA_CACHE.computeIfAbsent(schema.toString(), k -> FACTORY.getSchema(schema));
        Set<?> errors = s.validate(value);
        return errors.isEmpty();
    }

    public static boolean leafValueOk(String kind, JsonNode value, Double minimum, Double exclusiveMinimum,
                                      String pattern) {
        return leafValueOk(kind, value, minimum, exclusiveMinimum, pattern, null, null);
    }

    public static boolean isSId(String s) {
        return s != null && s.matches(SID_PATTERN);
    }
}

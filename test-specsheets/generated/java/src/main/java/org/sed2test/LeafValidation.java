package org.sed2test;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.networknt.schema.JsonSchema;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.SpecVersion;

import java.util.Set;

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

    public static boolean leafValueOk(String kind, JsonNode value, Double minimum, Double exclusiveMinimum, String pattern) {
        ObjectNode schema = baseSchema(kind);
        if (minimum != null) schema.put("minimum", minimum);
        if (exclusiveMinimum != null) schema.put("exclusiveMinimum", exclusiveMinimum);
        if (pattern != null && "string".equals(kind)) schema.put("pattern", pattern);
        JsonSchema s = FACTORY.getSchema(schema);
        Set<?> errors = s.validate(value);
        return errors.isEmpty();
    }

    public static boolean isSId(String s) {
        return s != null && s.matches(SID_PATTERN);
    }
}

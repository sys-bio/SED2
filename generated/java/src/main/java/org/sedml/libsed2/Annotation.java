package org.sedml.libsed2;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.BooleanNode;
import com.fasterxml.jackson.databind.node.DoubleNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.LongNode;
import com.fasterxml.jackson.databind.node.NullNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.node.TextNode;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Generated from test-specsheets/auxiliary/Annotation/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Annotation extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("qualifier", "any", true, "Annotation-0002", "Annotation-0001", "Annotation-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("value", "any", true, null, "Annotation-0003", "Annotation-0000", null, null, null, null, null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("qualifier", "value");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "Annotation-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }

    public JsonNode getQualifier() { if (!values.containsKey("qualifier")) throw new ApiError("qualifier" + " is not set"); return values.get("qualifier"); }
    public void setQualifier(JsonNode value) { values.put("qualifier", value); }
    public boolean isSetQualifier() { return values.containsKey("qualifier"); }
    public void unsetQualifier() { values.remove("qualifier"); }

    public JsonNode getValue() { if (!values.containsKey("value")) throw new ApiError("value" + " is not set"); return values.get("value"); }
    public void setValue(JsonNode value) { values.put("value", value); }
    public boolean isSetValue() { return values.containsKey("value"); }
    public void unsetValue() { values.remove("value"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        if (values.containsKey("qualifier")) d.set("qualifier", values.get("qualifier"));
        if (values.containsKey("value")) d.set("value", values.get("value"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

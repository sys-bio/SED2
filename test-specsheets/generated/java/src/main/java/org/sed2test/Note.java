package org.sed2test;

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

/** Generated from test-specsheets/auxiliary/Note/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Note extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("text", "StringOrRef", true, null, "Note-0001", "Note-0000", null, null, null, null, null, false)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("text");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "Note-0000"; }
    @Override public String nameRuleId() { return "TestBase-0001"; }
    @Override public String descRuleId() { return null; }
    @Override public String baseCatchall() { return "TestBase-0000"; }

    public String getTextValue() { return getOrRefValueNode("text").asText(); }
    public String getTextRef() { return getOrRefRefNode("text").asText(); }
    public void setTextValue(String value) { setOrRefValueNode("text", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setTextRef(String ref) { setOrRefRefNode("text", ref); }
    public boolean isTextRef() { return isOrRefRef("text"); }
    public boolean isSetText() { return values.containsKey("text"); }
    public void unsetText() { values.remove("text"); orRefIsRef.remove("text"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        if (values.containsKey("text")) d.set("text", values.get("text"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

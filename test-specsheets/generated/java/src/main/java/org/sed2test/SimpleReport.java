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

/** Generated from test-specsheets/outputs/SimpleReport/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class SimpleReport extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("source", "SIdRef", true, null, "SimpleReport-0001", "SimpleReport-0000", null, null, null, null, null),
        new FieldSpec("format", "StringOrRef", false, "AbstractReport-0001", null, "AbstractReport-0000", null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("source");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "simpleReport"; }
    @Override public String typeRuleId() { return "SimpleReport-0002"; }
    @Override public String ownCatchall() { return "SimpleReport-0000"; }
    @Override public String nameRuleId() { return "TestBase-0001"; }
    @Override public String descRuleId() { return null; }
    @Override public String baseCatchall() { return "TestBase-0000"; }
    public String getType() { return "simpleReport"; }

    public String getSource() { if (!values.containsKey("source")) throw new ApiError("source" + " is not set"); return values.get("source").asText(); }
    public void setSource(String value) { values.put("source", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetSource() { return values.containsKey("source"); }
    public void unsetSource() { values.remove("source"); }

    public String getFormatValue() { return getOrRefValueNode("format").asText(); }
    public String getFormatRef() { return getOrRefRefNode("format").asText(); }
    public void setFormatValue(String value) { setOrRefValueNode("format", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setFormatRef(String ref) { setOrRefRefNode("format", ref); }
    public boolean isFormatRef() { return isOrRefRef("format"); }
    public boolean isSetFormat() { return values.containsKey("format"); }
    public void unsetFormat() { values.remove("format"); orRefIsRef.remove("format"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("simpleReport"));
        if (values.containsKey("source")) d.set("source", values.get("source"));
        if (values.containsKey("format")) d.set("format", values.get("format"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

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

/** Generated from test-specsheets/tasks/SimpleWidget/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class SimpleWidget extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("value", "StringOrRef", true, null, "SimpleWidget-0001", "SimpleWidget-0000", null, null, null, null, null, false),
        new FieldSpec("label", "StringOrRef", false, "AbstractWidget-0001", null, "AbstractWidget-0000", null, null, null, null, null, false)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("value");
    private static final Map<String, List<FieldSpec>> NAMESPACE_FIELDS = Map.of(
        "acme", List.of(new FieldSpec("acme@priority", "NumberOrRef", false, "SimpleWidget-acme-0001", null, "SimpleWidget-acme-0000", null, null, null, null, null, false))
    );
    private static final Map<String, String> NAMESPACE_CATCHALL = Map.of("acme", "SimpleWidget-acme-0000");
    private static final Set<String> KNOWN_NAMESPACE_PREFIXES = Set.of("acme");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "simpleWidget"; }
    @Override public String typeRuleId() { return "SimpleWidget-0002"; }
    @Override public String ownCatchall() { return "SimpleWidget-0000"; }
    @Override public String nameRuleId() { return "TestBase-0001"; }
    @Override public String descRuleId() { return null; }
    @Override public String baseCatchall() { return "TestBase-0000"; }
    @Override public Map<String, List<FieldSpec>> namespaceFields() { return NAMESPACE_FIELDS; }
    @Override public Map<String, String> namespaceCatchall() { return NAMESPACE_CATCHALL; }
    @Override public Set<String> knownNamespacePrefixes() { return KNOWN_NAMESPACE_PREFIXES; }
    public String getType() { return "simpleWidget"; }

    public String getValueValue() { return getOrRefValueNode("value").asText(); }
    public String getValueRef() { return getOrRefRefNode("value").asText(); }
    public void setValueValue(String value) { setOrRefValueNode("value", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setValueRef(String ref) { setOrRefRefNode("value", ref); }
    public boolean isValueRef() { return isOrRefRef("value"); }
    public boolean isSetValue() { return values.containsKey("value"); }
    public void unsetValue() { values.remove("value"); orRefIsRef.remove("value"); }

    public String getLabelValue() { return getOrRefValueNode("label").asText(); }
    public String getLabelRef() { return getOrRefRefNode("label").asText(); }
    public void setLabelValue(String value) { setOrRefValueNode("label", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLabelRef(String ref) { setOrRefRefNode("label", ref); }
    public boolean isLabelRef() { return isOrRefRef("label"); }
    public boolean isSetLabel() { return values.containsKey("label"); }
    public void unsetLabel() { values.remove("label"); orRefIsRef.remove("label"); }

    public double getAcmePriorityValue() { return getOrRefValueNode("acme@priority").asDouble(); }
    public String getAcmePriorityRef() { return getOrRefRefNode("acme@priority").asText(); }
    public void setAcmePriorityValue(double value) { setOrRefValueNode("acme@priority", DoubleNode.valueOf(value)); }
    public void setAcmePriorityRef(String ref) { setOrRefRefNode("acme@priority", ref); }
    public boolean isAcmePriorityRef() { return isOrRefRef("acme@priority"); }
    public boolean isSetAcmePriority() { return values.containsKey("acme@priority"); }
    public void unsetAcmePriority() { values.remove("acme@priority"); orRefIsRef.remove("acme@priority"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("simpleWidget"));
        if (values.containsKey("value")) d.set("value", values.get("value"));
        if (values.containsKey("label")) d.set("label", values.get("label"));
        if (values.containsKey("acme@priority")) d.set("acme@priority", values.get("acme@priority"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

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

/** Generated from test-specsheets/auxiliary/WeightedChoice/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class WeightedChoice extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("weight", "NumberOrRef", true, null, "WeightedChoice-0001", "WeightedChoice-0000", null, null, null, null, null, false),
        new FieldSpec("label", "StringOrRef", false, "Choice-0003", null, "Choice-0000", null, null, null, null, null, false)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("weight");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "weightedChoice"; }
    @Override public String typeRuleId() { return "WeightedChoice-0002"; }
    @Override public String ownCatchall() { return "WeightedChoice-0000"; }
    @Override public String nameRuleId() { return "TestBase-0001"; }
    @Override public String descRuleId() { return null; }
    @Override public String baseCatchall() { return "TestBase-0000"; }
    public String getType() { return "weightedChoice"; }

    public double getWeightValue() { return getOrRefValueNode("weight").asDouble(); }
    public String getWeightRef() { return getOrRefRefNode("weight").asText(); }
    public void setWeightValue(double value) { setOrRefValueNode("weight", DoubleNode.valueOf(value)); }
    public void setWeightRef(String ref) { setOrRefRefNode("weight", ref); }
    public boolean isWeightRef() { return isOrRefRef("weight"); }
    public boolean isSetWeight() { return values.containsKey("weight"); }
    public void unsetWeight() { values.remove("weight"); orRefIsRef.remove("weight"); }

    public String getLabelValue() { return getOrRefValueNode("label").asText(); }
    public String getLabelRef() { return getOrRefRefNode("label").asText(); }
    public void setLabelValue(String value) { setOrRefValueNode("label", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLabelRef(String ref) { setOrRefRefNode("label", ref); }
    public boolean isLabelRef() { return isOrRefRef("label"); }
    public boolean isSetLabel() { return values.containsKey("label"); }
    public void unsetLabel() { values.remove("label"); orRefIsRef.remove("label"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("weightedChoice"));
        if (values.containsKey("weight")) d.set("weight", values.get("weight"));
        if (values.containsKey("label")) d.set("label", values.get("label"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

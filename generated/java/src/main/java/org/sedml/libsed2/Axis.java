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

/** Generated from test-specsheets/auxiliary/Axis/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Axis extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("scale", "StringOrRef", false, "Axis-0001", null, "Axis-0000", null, null, null, null, null),
        new FieldSpec("min", "NumberOrRef", false, "Axis-0003", null, "Axis-0000", null, null, null, null, null),
        new FieldSpec("max", "NumberOrRef", false, "Axis-0005", null, "Axis-0000", null, null, null, null, null),
        new FieldSpec("style", "SIdRef", false, "Axis-0009", null, "Axis-0000", null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "Axis-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }

    public String getScaleValue() { return getOrRefValueNode("scale").asText(); }
    public String getScaleRef() { return getOrRefRefNode("scale").asText(); }
    public void setScaleValue(String value) { setOrRefValueNode("scale", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setScaleRef(String ref) { setOrRefRefNode("scale", ref); }
    public boolean isScaleRef() { return isOrRefRef("scale"); }
    public boolean isSetScale() { return values.containsKey("scale"); }
    public void unsetScale() { values.remove("scale"); orRefIsRef.remove("scale"); }

    public double getMinValue() { return getOrRefValueNode("min").asDouble(); }
    public String getMinRef() { return getOrRefRefNode("min").asText(); }
    public void setMinValue(double value) { setOrRefValueNode("min", DoubleNode.valueOf(value)); }
    public void setMinRef(String ref) { setOrRefRefNode("min", ref); }
    public boolean isMinRef() { return isOrRefRef("min"); }
    public boolean isSetMin() { return values.containsKey("min"); }
    public void unsetMin() { values.remove("min"); orRefIsRef.remove("min"); }

    public double getMaxValue() { return getOrRefValueNode("max").asDouble(); }
    public String getMaxRef() { return getOrRefRefNode("max").asText(); }
    public void setMaxValue(double value) { setOrRefValueNode("max", DoubleNode.valueOf(value)); }
    public void setMaxRef(String ref) { setOrRefRefNode("max", ref); }
    public boolean isMaxRef() { return isOrRefRef("max"); }
    public boolean isSetMax() { return values.containsKey("max"); }
    public void unsetMax() { values.remove("max"); orRefIsRef.remove("max"); }

    public String getStyle() { if (!values.containsKey("style")) throw new ApiError("style" + " is not set"); return values.get("style").asText(); }
    public void setStyle(String value) { values.put("style", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetStyle() { return values.containsKey("style"); }
    public void unsetStyle() { values.remove("style"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        if (values.containsKey("scale")) d.set("scale", values.get("scale"));
        if (values.containsKey("min")) d.set("min", values.get("min"));
        if (values.containsKey("max")) d.set("max", values.get("max"));
        if (values.containsKey("style")) d.set("style", values.get("style"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

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

/** Generated from test-specsheets/tasks/Span/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Span extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("start", "NumberOrRef", true, "Span-0002", "Span-0001", "Span-0000", null, null, null, null, null),
        new FieldSpec("end", "NumberOrRef", true, "Span-0005", "Span-0004", "Span-0000", null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("start", "end");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "span"; }
    @Override public String typeRuleId() { return "Span-0007"; }
    @Override public String ownCatchall() { return "Span-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "span"; }

    public double getStartValue() { return getOrRefValueNode("start").asDouble(); }
    public String getStartRef() { return getOrRefRefNode("start").asText(); }
    public void setStartValue(double value) { setOrRefValueNode("start", DoubleNode.valueOf(value)); }
    public void setStartRef(String ref) { setOrRefRefNode("start", ref); }
    public boolean isStartRef() { return isOrRefRef("start"); }
    public boolean isSetStart() { return values.containsKey("start"); }
    public void unsetStart() { values.remove("start"); orRefIsRef.remove("start"); }

    public double getEndValue() { return getOrRefValueNode("end").asDouble(); }
    public String getEndRef() { return getOrRefRefNode("end").asText(); }
    public void setEndValue(double value) { setOrRefValueNode("end", DoubleNode.valueOf(value)); }
    public void setEndRef(String ref) { setOrRefRefNode("end", ref); }
    public boolean isEndRef() { return isOrRefRef("end"); }
    public boolean isSetEnd() { return values.containsKey("end"); }
    public void unsetEnd() { values.remove("end"); orRefIsRef.remove("end"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("span"));
        if (values.containsKey("start")) d.set("start", values.get("start"));
        if (values.containsKey("end")) d.set("end", values.get("end"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

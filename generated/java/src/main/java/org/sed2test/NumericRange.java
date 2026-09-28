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

/** Generated from test-specsheets/tasks/NumericRange/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class NumericRange extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("start", "NumberOrRef", false, ["NumericRange-0001", "NumericRange-0002"], null, "NumericRange-0000", null, null, null, null, null),
        new FieldSpec("end", "NumberOrRef", false, ["NumericRange-0003", "NumericRange-0004"], null, "NumericRange-0000", null, null, null, null, null),
        new FieldSpec("values", "string", false, ["NumericRange-0011", "NumericRange-0012"], null, "NumericRange-0000", null, null, null, null, null),
        new FieldSpec("values", "string", false, ["Range-0001", "Range-0002"], null, "Range-0000", null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "numericRange"; }
    @Override public String typeRuleId() { return "NumericRange-0013"; }
    @Override public String ownCatchall() { return "NumericRange-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "numericRange"; }

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

    public String getValues() { if (!values.containsKey("values")) throw new ApiError("values" + " is not set"); return values.get("values").asText(); }
    public void setValues(String value) { values.put("values", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetValues() { return values.containsKey("values"); }
    public void unsetValues() { values.remove("values"); }

    public String getValues() { if (!values.containsKey("values")) throw new ApiError("values" + " is not set"); return values.get("values").asText(); }
    public void setValues(String value) { values.put("values", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetValues() { return values.containsKey("values"); }
    public void unsetValues() { values.remove("values"); }

    public List<SedBase> getTaskParameters() { return taskParameters.items(); }
    public void addTaskParameters(SedBase obj) { taskParameters.add(obj); obj.attach(this, getDocument()); }
    public void insertTaskParameters(int index, SedBase obj) { taskParameters.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeTaskParameters(int index) { taskParameters.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        kids.addAll(taskParameters.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "taskParameters": return taskParameters;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("numericRange"));
        if (values.containsKey("start")) d.set("start", values.get("start"));
        if (values.containsKey("end")) d.set("end", values.get("end"));
        if (values.containsKey("values")) d.set("values", values.get("values"));
        if (values.containsKey("values")) d.set("values", values.get("values"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

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

/** Generated from test-specsheets/tasks/SteadyState/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class SteadyState extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("model", "SIdRef", true, null, "SteadyState-0001", "SteadyState-0000", null, null, null, null, null),
        new FieldSpec("independentVariable", "StringOrRef", false, "SteadyState-0004", null, "SteadyState-0000", null, null, null, null, null),
        new FieldSpec("outputVariables", "ArrayOrRef", true, null, "SteadyState-0002", "SteadyState-0000", null, null, null, null, null),
        new FieldSpec("outputModel", "BooleanOrRef", false, "SteadyState-0005", null, "SteadyState-0000", null, null, null, null, null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("model", "outputVariables");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "steadyState"; }
    @Override public String typeRuleId() { return "SteadyState-0003"; }
    @Override public String ownCatchall() { return "SteadyState-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "steadyState"; }

    public String getModel() { if (!values.containsKey("model")) throw new ApiError("model" + " is not set"); return values.get("model").asText(); }
    public void setModel(String value) { values.put("model", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetModel() { return values.containsKey("model"); }
    public void unsetModel() { values.remove("model"); }

    public String getIndependentVariableValue() { return getOrRefValueNode("independentVariable").asText(); }
    public String getIndependentVariableRef() { return getOrRefRefNode("independentVariable").asText(); }
    public void setIndependentVariableValue(String value) { setOrRefValueNode("independentVariable", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setIndependentVariableRef(String ref) { setOrRefRefNode("independentVariable", ref); }
    public boolean isIndependentVariableRef() { return isOrRefRef("independentVariable"); }
    public boolean isSetIndependentVariable() { return values.containsKey("independentVariable"); }
    public void unsetIndependentVariable() { values.remove("independentVariable"); orRefIsRef.remove("independentVariable"); }

    public JsonNode getOutputVariablesValue() { return getOrRefValueNode("outputVariables"); }
    public String getOutputVariablesRef() { return getOrRefRefNode("outputVariables").asText(); }
    public void setOutputVariablesValue(JsonNode value) { setOrRefValueNode("outputVariables", value); }
    public void setOutputVariablesRef(String ref) { setOrRefRefNode("outputVariables", ref); }
    public boolean isOutputVariablesRef() { return isOrRefRef("outputVariables"); }
    public boolean isSetOutputVariables() { return values.containsKey("outputVariables"); }
    public void unsetOutputVariables() { values.remove("outputVariables"); orRefIsRef.remove("outputVariables"); }

    public boolean getOutputModelValue() { return getOrRefValueNode("outputModel").asBoolean(); }
    public String getOutputModelRef() { return getOrRefRefNode("outputModel").asText(); }
    public void setOutputModelValue(boolean value) { setOrRefValueNode("outputModel", BooleanNode.valueOf(value)); }
    public void setOutputModelRef(String ref) { setOrRefRefNode("outputModel", ref); }
    public boolean isOutputModelRef() { return isOrRefRef("outputModel"); }
    public boolean isSetOutputModel() { return values.containsKey("outputModel"); }
    public void unsetOutputModel() { values.remove("outputModel"); orRefIsRef.remove("outputModel"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

    public List<SedBase> getTaskParameters() { return taskParameters.items(); }
    public void addTaskParameters(SedBase obj) { taskParameters.add(obj); obj.attach(this, getDocument()); }
    public void insertTaskParameters(int index, SedBase obj) { taskParameters.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeTaskParameters(int index) { taskParameters.remove(index); }

    public List<SedBase> getAnnotations() { return annotations.items(); }
    public void addAnnotations(SedBase obj) { annotations.add(obj); obj.attach(this, getDocument()); }
    public void insertAnnotations(int index, SedBase obj) { annotations.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeAnnotations(int index) { annotations.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        kids.addAll(taskParameters.items());
        kids.addAll(annotations.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "taskParameters": return taskParameters;
            case "annotations": return annotations;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("steadyState"));
        if (values.containsKey("model")) d.set("model", values.get("model"));
        if (values.containsKey("independentVariable")) d.set("independentVariable", values.get("independentVariable"));
        if (values.containsKey("outputVariables")) d.set("outputVariables", values.get("outputVariables"));
        if (values.containsKey("outputModel")) d.set("outputModel", values.get("outputModel"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

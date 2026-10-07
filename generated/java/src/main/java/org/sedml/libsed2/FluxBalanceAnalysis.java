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

/** Generated from specsheets/tasks/FluxBalanceAnalysis/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class FluxBalanceAnalysis extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("model", "SIdRef", true, "FluxBalanceAnalysis-0002", "FluxBalanceAnalysis-0001", "FluxBalanceAnalysis-0000", null, null, null, null, null, false, null, null, null, null, "model"),
        new FieldSpec("outputVariables", "ArrayOrRef", true, "FluxBalanceAnalysis-0004", "FluxBalanceAnalysis-0003", "FluxBalanceAnalysis-0000", null, null, null, null, null, false, null, null, "FluxBalanceAnalysis-0005", "string", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("workingAlgorithms", "array", false, "FluxBalanceAnalysis-0009", null, "FluxBalanceAnalysis-0000", null, null, null, "WorkingAlgorithm", null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("model", "outputVariables");
    private final ListCollection<SedBase> workingAlgorithms = new ListCollection<>();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "fluxBalanceAnalysis"; }
    @Override public String typeRuleId() { return "FluxBalanceAnalysis-0008"; }
    @Override public String ownCatchall() { return "FluxBalanceAnalysis-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "fluxBalanceAnalysis"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"len(outputVariables)\"}, \"labels\": {\"source\": \"static\", \"expr\": \"outputVariables\"}}]}, \"[id].model\": {\"type\": \"model\"}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public String getModel() { if (!values.containsKey("model")) throw new ApiError("model" + " is not set"); return values.get("model").asText(); }
    public void setModel(String value) { values.put("model", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetModel() { return values.containsKey("model"); }
    public void unsetModel() { values.remove("model"); }

    public JsonNode getOutputVariablesValue() { return getOrRefValueNode("outputVariables"); }
    public String getOutputVariablesRef() { return getOrRefRefNode("outputVariables").asText(); }
    public void setOutputVariablesValue(JsonNode value) { setOrRefValueNode("outputVariables", value); }
    public void setOutputVariablesRef(String ref) { setOrRefRefNode("outputVariables", ref); }
    public boolean isOutputVariablesRef() { return isOrRefRef("outputVariables"); }
    public boolean isSetOutputVariables() { return values.containsKey("outputVariables"); }
    public void unsetOutputVariables() { values.remove("outputVariables"); orRefIsRef.remove("outputVariables"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

    public List<SedBase> getWorkingAlgorithms() { return workingAlgorithms.items(); }
    public void addWorkingAlgorithms(SedBase obj) { workingAlgorithms.add(obj); obj.attach(this, getDocument()); }
    public void insertWorkingAlgorithms(int index, SedBase obj) { workingAlgorithms.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeWorkingAlgorithms(int index) { workingAlgorithms.remove(index); }

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
        kids.addAll(workingAlgorithms.items());
        kids.addAll(taskParameters.items());
        kids.addAll(annotations.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : workingAlgorithms.items()) { out.add(new ChildLoc(item, "/workingAlgorithms/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "workingAlgorithms": return workingAlgorithms;
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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("fluxBalanceAnalysis"));
        if (values.containsKey("model")) d.set("model", values.get("model"));
        if (values.containsKey("outputVariables")) d.set("outputVariables", values.get("outputVariables"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (workingAlgorithms.size() > 0) { ArrayNode arr = d.putArray("workingAlgorithms"); for (SedBase item : workingAlgorithms.items()) arr.add(item.toJsonValue()); }
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

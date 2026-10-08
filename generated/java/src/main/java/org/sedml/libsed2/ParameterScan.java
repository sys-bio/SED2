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

/** Generated from specsheets/tasks/ParameterScan/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class ParameterScan extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("model", "SIdRef", true, "ParameterScan-0002", "ParameterScan-0001", "ParameterScan-0000", null, null, null, null, null, false, null, null, null, null, "model"),
        new FieldSpec("outputVariableMap", "DictOrRef", false, "Repeat-0002", null, "Repeat-0000", null, null, null, null, null, false, null, null, "Repeat-0003", "ref", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("parameterRanges", "array", true, "ParameterScan-0004", "ParameterScan-0003", "ParameterScan-0000", null, null, null, "ParameterRange", null, false, null, null, null, null, null),
        new FieldSpec("subTasks", "dict", false, "Repeat-0001", null, "Repeat-0000", null, null, null, null, "AbstractTask", false, null, null, null, null, null),
        new FieldSpec("aggregateOutputVariables", "dict", false, "Repeat-0004", null, "Repeat-0000", null, null, null, "AggregationCalculation", null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("model", "parameterRanges");
    private final ListCollection<SedBase> parameterRanges = new ListCollection<>();
    private final IdKeyedCollection<SedBase> subTasks = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> aggregateOutputVariables = new IdKeyedCollection<>();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "parameterScan"; }
    @Override public String typeRuleId() { return "ParameterScan-0006"; }
    @Override public String ownCatchall() { return "ParameterScan-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "parameterScan"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"type\": \"annotatedData\", \"dimensions\": [{\"repeat\": {\"over\": \"parameterRanges\", \"size\": {\"source\": \"static\", \"expr\": \"len(self)\"}, \"labels\": {\"source\": \"static\", \"expr\": \"modelElement\"}, \"note\": \"one dimension per entry of parameterRanges, each sized by that entry's own length; len(self) dispatches on the entry's actual Range/NumericRange/ParameterRange type - see core-spec.md Section 8; each dimension is labeled with (identified by) that entry's modelElement, in parameterRanges order\"}}, {\"size\": {\"source\": \"static\", \"expr\": \"len(outputVariableMap)\"}, \"labels\": null}]}, \"[id].aggregates\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"len(aggregateOutputVariables)\"}, \"labels\": null}]}, \"[id].ranges\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"len(parameterRanges)\"}, \"labels\": {\"source\": \"static\", \"expr\": \"parameterRanges.modelElement\"}, \"note\": \"one entry per ParameterRange child, in order, labeled with that child's modelElement (parameterRanges.modelElement is the modelElement of each entry, in order)\"}], \"note\": \"the current value of each entry of parameterRanges, within the loop only\"}, \"[id].indexes\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"len(parameterRanges)\"}, \"labels\": {\"source\": \"static\", \"expr\": \"parameterRanges.modelElement\"}, \"note\": \"one entry per ParameterRange child, in order, labeled with that child's modelElement (parameterRanges.modelElement is the modelElement of each entry, in order)\"}], \"note\": \"the current index into each entry of parameterRanges, within the loop only\"}, \"[id].model\": {\"type\": \"model\", \"note\": \"the model as modified for the current iteration, within the loop only\"}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public String getModel() { if (!values.containsKey("model")) throw new ApiError("model" + " is not set"); return values.get("model").asText(); }
    public void setModel(String value) { values.put("model", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetModel() { return values.containsKey("model"); }
    public void unsetModel() { values.remove("model"); }

    public JsonNode getOutputVariableMapValue() { return getOrRefValueNode("outputVariableMap"); }
    public String getOutputVariableMapRef() { return getOrRefRefNode("outputVariableMap").asText(); }
    public void setOutputVariableMapValue(JsonNode value) { setOrRefValueNode("outputVariableMap", value); }
    public void setOutputVariableMapRef(String ref) { setOrRefRefNode("outputVariableMap", ref); }
    public boolean isOutputVariableMapRef() { return isOrRefRef("outputVariableMap"); }
    public boolean isSetOutputVariableMap() { return values.containsKey("outputVariableMap"); }
    public void unsetOutputVariableMap() { values.remove("outputVariableMap"); orRefIsRef.remove("outputVariableMap"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

    public List<SedBase> getParameterRanges() { return parameterRanges.items(); }
    public void addParameterRanges(SedBase obj) { parameterRanges.add(obj); obj.attach(this, getDocument()); }
    public void insertParameterRanges(int index, SedBase obj) { parameterRanges.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeParameterRanges(int index) { parameterRanges.remove(index); }

    public List<String> getSubTasks() { return subTasks.ids(); }
    public SedBase getSubTasksItem(String itemId) { return subTasks.get(itemId); }
    public void addSubTasks(String itemId, SedBase obj) { subTasks.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertSubTasks(int index, String itemId, SedBase obj) { subTasks.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeSubTasks(String itemId) { subTasks.remove(itemId); }
    public void setIdOnSubTasks(String oldId, String newId) { subTasks.setId(oldId, newId); }

    public List<String> getAggregateOutputVariables() { return aggregateOutputVariables.ids(); }
    public SedBase getAggregateOutputVariablesItem(String itemId) { return aggregateOutputVariables.get(itemId); }
    public void addAggregateOutputVariables(String itemId, SedBase obj) { aggregateOutputVariables.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertAggregateOutputVariables(int index, String itemId, SedBase obj) { aggregateOutputVariables.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeAggregateOutputVariables(String itemId) { aggregateOutputVariables.remove(itemId); }
    public void setIdOnAggregateOutputVariables(String oldId, String newId) { aggregateOutputVariables.setId(oldId, newId); }

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
        for (String i : subTasks.ids()) kids.add(subTasks.get(i));
        for (String i : aggregateOutputVariables.ids()) kids.add(aggregateOutputVariables.get(i));
        kids.addAll(parameterRanges.items());
        kids.addAll(taskParameters.items());
        kids.addAll(annotations.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : subTasks.ids()) out.add(new ChildLoc(subTasks.get(i), "/subTasks/" + i));
        for (String i : aggregateOutputVariables.ids()) out.add(new ChildLoc(aggregateOutputVariables.get(i), "/aggregateOutputVariables/" + i));
        { int idx = 0; for (SedBase item : parameterRanges.items()) { out.add(new ChildLoc(item, "/parameterRanges/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        return out;
    }

    @Override
    public IdCollection getIdCollection(String fieldName) {
        switch (fieldName) {
            case "subTasks": return subTasks;
            case "aggregateOutputVariables": return aggregateOutputVariables;
            default: return null;
        }
    }

    @Override
    public List<String> idCollectionNames() { return List.of("subTasks", "aggregateOutputVariables"); }

    @Override
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        switch (fieldName) {
            case "subTasks": return subTasks;
            case "aggregateOutputVariables": return aggregateOutputVariables;
            default: return super.getDictCollection(fieldName);
        }
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "parameterRanges": return parameterRanges;
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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("parameterScan"));
        if (values.containsKey("model")) d.set("model", values.get("model"));
        if (values.containsKey("outputVariableMap")) d.set("outputVariableMap", values.get("outputVariableMap"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (subTasks.size() > 0) { ObjectNode sub = d.putObject("subTasks"); for (String i : subTasks.ids()) sub.set(i, subTasks.get(i).toJsonValue()); }
        if (aggregateOutputVariables.size() > 0) { ObjectNode sub = d.putObject("aggregateOutputVariables"); for (String i : aggregateOutputVariables.ids()) sub.set(i, aggregateOutputVariables.get(i).toJsonValue()); }
        if (parameterRanges.size() > 0) { ArrayNode arr = d.putArray("parameterRanges"); for (SedBase item : parameterRanges.items()) arr.add(item.toJsonValue()); }
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

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

/** Generated from specsheets/tasks/Loop/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Loop extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("outputVariableMap", "DictOrRef", false, "Repeat-0002", null, "Repeat-0000", null, null, null, null, null, false, null, null, "Repeat-0003", "ref", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("loopVariables", "dict", true, "Loop-0003", "Loop-0002", "Loop-0000", null, null, null, "LoopVariable", null, false, null, null, null, null, null),
        new FieldSpec("subTasks", "dict", false, "Repeat-0001", null, "Repeat-0000", null, null, null, null, "AbstractTask", false, null, null, null, null, null),
        new FieldSpec("aggregateOutputVariables", "dict", false, "Repeat-0004", null, "Repeat-0000", null, null, null, "AggregationCalculation", null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null),
        new FieldSpec("range", "ref-discriminator", true, "Loop-0007", "Loop-0006", "Loop-0000", null, null, null, null, "RangeInline", false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("loopVariables", "range");
    private final IdKeyedCollection<SedBase> loopVariables = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> subTasks = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> aggregateOutputVariables = new IdKeyedCollection<>();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();
    private SedBase range;

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "loop"; }
    @Override public String typeRuleId() { return "Loop-0005"; }
    @Override public String ownCatchall() { return "Loop-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "loop"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"len(range)\"}, \"labels\": {\"source\": \"runtime\", \"note\": \"the range's values, written as text the way numbers appear in formed strings (an integral value without a decimal point: 1, 2; otherwise 0.5, 0.25); known only once the range is expanded, so a label index here is not checked ahead of time\"}, \"note\": \"dimension 0 is the iteration: one row per value in range, labeled by those values (there is no separate column holding the range values); len(range) dispatches on range's actual Range/NumericRange/ParameterRange type\"}, {\"size\": {\"source\": \"static\", \"expr\": \"len(outputVariableMap)\"}, \"labels\": {\"source\": \"static\", \"expr\": \"keys(outputVariableMap)\"}, \"note\": \"dimension 1 holds the outputVariableMap entries, one per key, labeled by the keys; length 0 if outputVariableMap is empty\"}, {\"trailing\": {\"of\": \"outputVariableMap\", \"note\": \"the dimensions of the outputVariableMap entries' own values, if they have any, follow (all entries must have the same shape, since they are stacked into one array); how many there are is not known ahead of time\"}}]}, \"[id].aggregates\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"len(aggregateOutputVariables)\"}, \"labels\": null, \"note\": \"each entry collapses the iteration dimension of [id] to a single value (per Repeat, the applied dimension defaults to this Loop's own iterations), unless the underlying subTask output was itself multi-dimensional, in which case that dimensionality carries through per entry\"}, {\"trailing\": {\"of\": \"aggregateOutputVariables\", \"note\": \"if the underlying subTask output was itself multi-dimensional, that dimensionality carries through per entry; how many dimensions that is is not known ahead of time\"}}]}, \"[id].range\": {\"type\": \"annotatedData\", \"dimensions\": [], \"note\": \"the current value of range, within the loop\"}, \"[id].index\": {\"type\": \"annotatedData\", \"dimensions\": [], \"note\": \"the current index into range, within the loop\"}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

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

    public List<String> getLoopVariables() { return loopVariables.ids(); }
    public SedBase getLoopVariablesItem(String itemId) { return loopVariables.get(itemId); }
    public void addLoopVariables(String itemId, SedBase obj) { loopVariables.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertLoopVariables(int index, String itemId, SedBase obj) { loopVariables.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeLoopVariables(String itemId) { loopVariables.remove(itemId); }
    public void setIdOnLoopVariables(String oldId, String newId) { loopVariables.setId(oldId, newId); }

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

    public SedBase getRange() { if (range == null) throw new ApiError("range" + " is not set"); return range; }
    public void setRange(SedBase obj) { range = obj; obj.attach(this, getDocument()); }
    public boolean isSetRange() { return range != null; }
    public void unsetRange() { range = null; }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        for (String i : loopVariables.ids()) kids.add(loopVariables.get(i));
        for (String i : subTasks.ids()) kids.add(subTasks.get(i));
        for (String i : aggregateOutputVariables.ids()) kids.add(aggregateOutputVariables.get(i));
        kids.addAll(taskParameters.items());
        kids.addAll(annotations.items());
        if (range != null) kids.add(range);
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : loopVariables.ids()) out.add(new ChildLoc(loopVariables.get(i), "/loopVariables/" + i));
        for (String i : subTasks.ids()) out.add(new ChildLoc(subTasks.get(i), "/subTasks/" + i));
        for (String i : aggregateOutputVariables.ids()) out.add(new ChildLoc(aggregateOutputVariables.get(i), "/aggregateOutputVariables/" + i));
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        if (range != null) out.add(new ChildLoc(range, "/range"));
        return out;
    }

    @Override
    public IdCollection getIdCollection(String fieldName) {
        switch (fieldName) {
            case "loopVariables": return loopVariables;
            case "subTasks": return subTasks;
            case "aggregateOutputVariables": return aggregateOutputVariables;
            default: return null;
        }
    }

    @Override
    public List<String> idCollectionNames() { return List.of("loopVariables", "subTasks", "aggregateOutputVariables"); }

    @Override
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        switch (fieldName) {
            case "loopVariables": return loopVariables;
            case "subTasks": return subTasks;
            case "aggregateOutputVariables": return aggregateOutputVariables;
            default: return super.getDictCollection(fieldName);
        }
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
    protected void setChildField(String fieldName, SedBase child) {
        switch (fieldName) {
            case "range": range = child; return;
            default: super.setChildField(fieldName, child);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("loop"));
        if (values.containsKey("outputVariableMap")) d.set("outputVariableMap", values.get("outputVariableMap"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (loopVariables.size() > 0) { ObjectNode sub = d.putObject("loopVariables"); for (String i : loopVariables.ids()) sub.set(i, loopVariables.get(i).toJsonValue()); }
        if (subTasks.size() > 0) { ObjectNode sub = d.putObject("subTasks"); for (String i : subTasks.ids()) sub.set(i, subTasks.get(i).toJsonValue()); }
        if (aggregateOutputVariables.size() > 0) { ObjectNode sub = d.putObject("aggregateOutputVariables"); for (String i : aggregateOutputVariables.ids()) sub.set(i, aggregateOutputVariables.get(i).toJsonValue()); }
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        if (range != null) d.set("range", range.toJsonValue());
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

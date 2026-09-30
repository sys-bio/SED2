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

/** Generated from test-specsheets/tasks/AggregationCalculation/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class AggregationCalculation extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("input", "any", true, null, "AggregationCalculation-0001", "AggregationCalculation-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("appliedDimensions", "ArrayOrRef", false, "AggregationCalculation-0002", null, "AggregationCalculation-0000", null, null, null, null, null, false, null, null, "AggregationCalculation-0003", "string", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("input");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "aggregationCalculation"; }
    @Override public String typeRuleId() { return "AggregationCalculation-0004"; }
    @Override public String ownCatchall() { return "AggregationCalculation-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "aggregationCalculation"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"valid\": true, \"type\": \"annotatedData\", \"dimensions\": {\"source\": \"static\", \"expr\": \"shapeOf(input) - dim(appliedDimensions or outermost)\", \"note\": \"shape is input's shape with the dimension(s) named in appliedDimensions removed (or the outermost dimension, if appliedDimensions is unset); dimension count/sizes are therefore only as knowable as input's own shape is\"}}, \"[id].model\": {\"valid\": false}, \"[id].strings\": {\"valid\": false}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public JsonNode getInput() { if (!values.containsKey("input")) throw new ApiError("input" + " is not set"); return values.get("input"); }
    public void setInput(JsonNode value) { values.put("input", value); }
    public boolean isSetInput() { return values.containsKey("input"); }
    public void unsetInput() { values.remove("input"); }

    public JsonNode getAppliedDimensionsValue() { return getOrRefValueNode("appliedDimensions"); }
    public String getAppliedDimensionsRef() { return getOrRefRefNode("appliedDimensions").asText(); }
    public void setAppliedDimensionsValue(JsonNode value) { setOrRefValueNode("appliedDimensions", value); }
    public void setAppliedDimensionsRef(String ref) { setOrRefRefNode("appliedDimensions", ref); }
    public boolean isAppliedDimensionsRef() { return isOrRefRef("appliedDimensions"); }
    public boolean isSetAppliedDimensions() { return values.containsKey("appliedDimensions"); }
    public void unsetAppliedDimensions() { values.remove("appliedDimensions"); orRefIsRef.remove("appliedDimensions"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("aggregationCalculation"));
        if (values.containsKey("input")) d.set("input", values.get("input"));
        if (values.containsKey("appliedDimensions")) d.set("appliedDimensions", values.get("appliedDimensions"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

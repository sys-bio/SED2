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

/** Generated from test-specsheets/tasks/ModelElementList/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class ModelElementList extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("model", "SIdRef", true, "ModelElementList-0002", "ModelElementList-0001", "ModelElementList-0000", null, null, null, null, null, false, null, null, null, null, "model"),
        new FieldSpec("includeElements", "ArrayOrRef", false, "ModelElementList-0003", null, "ModelElementList-0000", null, null, null, null, null, false, null, null, "ModelElementList-0004", "string", null),
        new FieldSpec("includeTypes", "ArrayOrRef", false, "ModelElementList-0005", null, "ModelElementList-0000", null, null, null, null, null, false, null, null, "ModelElementList-0006", "string", null),
        new FieldSpec("excludeElements", "ArrayOrRef", false, "ModelElementList-0007", null, "ModelElementList-0000", null, null, null, null, null, false, null, null, "ModelElementList-0008", "string", null),
        new FieldSpec("excludeTypes", "ArrayOrRef", false, "ModelElementList-0009", null, "ModelElementList-0000", null, null, null, null, null, false, null, null, "ModelElementList-0010", "string", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("model");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "modelElementList"; }
    @Override public String typeRuleId() { return "ModelElementList-0011"; }
    @Override public String ownCatchall() { return "ModelElementList-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "modelElementList"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"valid\": false}, \"[id].model\": {\"valid\": false}, \"[id].strings\": {\"valid\": true, \"type\": \"stringList\", \"dimensions\": [{\"size\": {\"source\": \"input-file\", \"from\": \"model\", \"extract\": \"matchedElementIds\", \"note\": \"length = number of elements in the referenced model matched after includeElements/includeTypes/excludeElements/excludeTypes filtering\"}, \"labels\": {\"source\": \"input-file\", \"from\": \"model\", \"extract\": \"matchedElementIds\", \"note\": \"the matched element ids themselves\"}}]}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public String getModel() { if (!values.containsKey("model")) throw new ApiError("model" + " is not set"); return values.get("model").asText(); }
    public void setModel(String value) { values.put("model", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetModel() { return values.containsKey("model"); }
    public void unsetModel() { values.remove("model"); }

    public JsonNode getIncludeElementsValue() { return getOrRefValueNode("includeElements"); }
    public String getIncludeElementsRef() { return getOrRefRefNode("includeElements").asText(); }
    public void setIncludeElementsValue(JsonNode value) { setOrRefValueNode("includeElements", value); }
    public void setIncludeElementsRef(String ref) { setOrRefRefNode("includeElements", ref); }
    public boolean isIncludeElementsRef() { return isOrRefRef("includeElements"); }
    public boolean isSetIncludeElements() { return values.containsKey("includeElements"); }
    public void unsetIncludeElements() { values.remove("includeElements"); orRefIsRef.remove("includeElements"); }

    public JsonNode getIncludeTypesValue() { return getOrRefValueNode("includeTypes"); }
    public String getIncludeTypesRef() { return getOrRefRefNode("includeTypes").asText(); }
    public void setIncludeTypesValue(JsonNode value) { setOrRefValueNode("includeTypes", value); }
    public void setIncludeTypesRef(String ref) { setOrRefRefNode("includeTypes", ref); }
    public boolean isIncludeTypesRef() { return isOrRefRef("includeTypes"); }
    public boolean isSetIncludeTypes() { return values.containsKey("includeTypes"); }
    public void unsetIncludeTypes() { values.remove("includeTypes"); orRefIsRef.remove("includeTypes"); }

    public JsonNode getExcludeElementsValue() { return getOrRefValueNode("excludeElements"); }
    public String getExcludeElementsRef() { return getOrRefRefNode("excludeElements").asText(); }
    public void setExcludeElementsValue(JsonNode value) { setOrRefValueNode("excludeElements", value); }
    public void setExcludeElementsRef(String ref) { setOrRefRefNode("excludeElements", ref); }
    public boolean isExcludeElementsRef() { return isOrRefRef("excludeElements"); }
    public boolean isSetExcludeElements() { return values.containsKey("excludeElements"); }
    public void unsetExcludeElements() { values.remove("excludeElements"); orRefIsRef.remove("excludeElements"); }

    public JsonNode getExcludeTypesValue() { return getOrRefValueNode("excludeTypes"); }
    public String getExcludeTypesRef() { return getOrRefRefNode("excludeTypes").asText(); }
    public void setExcludeTypesValue(JsonNode value) { setOrRefValueNode("excludeTypes", value); }
    public void setExcludeTypesRef(String ref) { setOrRefRefNode("excludeTypes", ref); }
    public boolean isExcludeTypesRef() { return isOrRefRef("excludeTypes"); }
    public boolean isSetExcludeTypes() { return values.containsKey("excludeTypes"); }
    public void unsetExcludeTypes() { values.remove("excludeTypes"); orRefIsRef.remove("excludeTypes"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("modelElementList"));
        if (values.containsKey("model")) d.set("model", values.get("model"));
        if (values.containsKey("includeElements")) d.set("includeElements", values.get("includeElements"));
        if (values.containsKey("includeTypes")) d.set("includeTypes", values.get("includeTypes"));
        if (values.containsKey("excludeElements")) d.set("excludeElements", values.get("excludeElements"));
        if (values.containsKey("excludeTypes")) d.set("excludeTypes", values.get("excludeTypes"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

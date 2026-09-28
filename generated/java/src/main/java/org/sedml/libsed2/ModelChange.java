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

/** Generated from test-specsheets/tasks/ModelChange/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class ModelChange extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("inputModel", "SIdRef", true, "ModelChange-0002", "ModelChange-0001", "ModelChange-0000", null, null, null, null, null),
        new FieldSpec("setValues", "DictOrRef", false, "ModelChange-0003", null, "ModelChange-0000", null, null, null, null, null),
        new FieldSpec("removeElements", "ArrayOrRef", false, "ModelChange-0005", null, "ModelChange-0000", null, null, null, null, null),
        new FieldSpec("addElements", "ArrayOrRef", false, "ModelChange-0007", null, "ModelChange-0000", null, null, null, null, null),
        new FieldSpec("replaceElements", "DictOrRef", false, "ModelChange-0009", null, "ModelChange-0000", null, null, null, null, null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("inputModel");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "modelChange"; }
    @Override public String typeRuleId() { return "ModelChange-0011"; }
    @Override public String ownCatchall() { return "ModelChange-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "modelChange"; }

    public String getInputModel() { if (!values.containsKey("inputModel")) throw new ApiError("inputModel" + " is not set"); return values.get("inputModel").asText(); }
    public void setInputModel(String value) { values.put("inputModel", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetInputModel() { return values.containsKey("inputModel"); }
    public void unsetInputModel() { values.remove("inputModel"); }

    public JsonNode getSetValuesValue() { return getOrRefValueNode("setValues"); }
    public String getSetValuesRef() { return getOrRefRefNode("setValues").asText(); }
    public void setSetValuesValue(JsonNode value) { setOrRefValueNode("setValues", value); }
    public void setSetValuesRef(String ref) { setOrRefRefNode("setValues", ref); }
    public boolean isSetValuesRef() { return isOrRefRef("setValues"); }
    public boolean isSetSetValues() { return values.containsKey("setValues"); }
    public void unsetSetValues() { values.remove("setValues"); orRefIsRef.remove("setValues"); }

    public JsonNode getRemoveElementsValue() { return getOrRefValueNode("removeElements"); }
    public String getRemoveElementsRef() { return getOrRefRefNode("removeElements").asText(); }
    public void setRemoveElementsValue(JsonNode value) { setOrRefValueNode("removeElements", value); }
    public void setRemoveElementsRef(String ref) { setOrRefRefNode("removeElements", ref); }
    public boolean isRemoveElementsRef() { return isOrRefRef("removeElements"); }
    public boolean isSetRemoveElements() { return values.containsKey("removeElements"); }
    public void unsetRemoveElements() { values.remove("removeElements"); orRefIsRef.remove("removeElements"); }

    public JsonNode getAddElementsValue() { return getOrRefValueNode("addElements"); }
    public String getAddElementsRef() { return getOrRefRefNode("addElements").asText(); }
    public void setAddElementsValue(JsonNode value) { setOrRefValueNode("addElements", value); }
    public void setAddElementsRef(String ref) { setOrRefRefNode("addElements", ref); }
    public boolean isAddElementsRef() { return isOrRefRef("addElements"); }
    public boolean isSetAddElements() { return values.containsKey("addElements"); }
    public void unsetAddElements() { values.remove("addElements"); orRefIsRef.remove("addElements"); }

    public JsonNode getReplaceElementsValue() { return getOrRefValueNode("replaceElements"); }
    public String getReplaceElementsRef() { return getOrRefRefNode("replaceElements").asText(); }
    public void setReplaceElementsValue(JsonNode value) { setOrRefValueNode("replaceElements", value); }
    public void setReplaceElementsRef(String ref) { setOrRefRefNode("replaceElements", ref); }
    public boolean isReplaceElementsRef() { return isOrRefRef("replaceElements"); }
    public boolean isSetReplaceElements() { return values.containsKey("replaceElements"); }
    public void unsetReplaceElements() { values.remove("replaceElements"); orRefIsRef.remove("replaceElements"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("modelChange"));
        if (values.containsKey("inputModel")) d.set("inputModel", values.get("inputModel"));
        if (values.containsKey("setValues")) d.set("setValues", values.get("setValues"));
        if (values.containsKey("removeElements")) d.set("removeElements", values.get("removeElements"));
        if (values.containsKey("addElements")) d.set("addElements", values.get("addElements"));
        if (values.containsKey("replaceElements")) d.set("replaceElements", values.get("replaceElements"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

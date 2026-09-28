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

/** Generated from test-specsheets/tasks/ModelImport/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class ModelImport extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("location", "StringOrRef", true, "ModelImport-0002", "ModelImport-0001", "ModelImport-0000", null, null, null, null, null),
        new FieldSpec("language", "StringOrRef", true, "ModelImport-0005", "ModelImport-0004", "ModelImport-0000", null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("location", "language");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "modelImport"; }
    @Override public String typeRuleId() { return "ModelImport-0007"; }
    @Override public String ownCatchall() { return "ModelImport-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "modelImport"; }

    public String getLocationValue() { return getOrRefValueNode("location").asText(); }
    public String getLocationRef() { return getOrRefRefNode("location").asText(); }
    public void setLocationValue(String value) { setOrRefValueNode("location", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLocationRef(String ref) { setOrRefRefNode("location", ref); }
    public boolean isLocationRef() { return isOrRefRef("location"); }
    public boolean isSetLocation() { return values.containsKey("location"); }
    public void unsetLocation() { values.remove("location"); orRefIsRef.remove("location"); }

    public String getLanguageValue() { return getOrRefValueNode("language").asText(); }
    public String getLanguageRef() { return getOrRefRefNode("language").asText(); }
    public void setLanguageValue(String value) { setOrRefValueNode("language", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLanguageRef(String ref) { setOrRefRefNode("language", ref); }
    public boolean isLanguageRef() { return isOrRefRef("language"); }
    public boolean isSetLanguage() { return values.containsKey("language"); }
    public void unsetLanguage() { values.remove("language"); orRefIsRef.remove("language"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("modelImport"));
        if (values.containsKey("location")) d.set("location", values.get("location"));
        if (values.containsKey("language")) d.set("language", values.get("language"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

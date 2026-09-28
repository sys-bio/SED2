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

/** Generated from test-specsheets/tasks/DataImport/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class DataImport extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("location", "StringOrRef", true, "DataImport-0002", "DataImport-0001", "DataImport-0000", null, null, null, null, null),
        new FieldSpec("format", "StringOrRef", true, "DataImport-0005", "DataImport-0004", "DataImport-0000", null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("location", "format");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "dataImport"; }
    @Override public String typeRuleId() { return "DataImport-0007"; }
    @Override public String ownCatchall() { return "DataImport-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "dataImport"; }

    public String getLocationValue() { return getOrRefValueNode("location").asText(); }
    public String getLocationRef() { return getOrRefRefNode("location").asText(); }
    public void setLocationValue(String value) { setOrRefValueNode("location", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLocationRef(String ref) { setOrRefRefNode("location", ref); }
    public boolean isLocationRef() { return isOrRefRef("location"); }
    public boolean isSetLocation() { return values.containsKey("location"); }
    public void unsetLocation() { values.remove("location"); orRefIsRef.remove("location"); }

    public String getFormatValue() { return getOrRefValueNode("format").asText(); }
    public String getFormatRef() { return getOrRefRefNode("format").asText(); }
    public void setFormatValue(String value) { setOrRefValueNode("format", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setFormatRef(String ref) { setOrRefRefNode("format", ref); }
    public boolean isFormatRef() { return isOrRefRef("format"); }
    public boolean isSetFormat() { return values.containsKey("format"); }
    public void unsetFormat() { values.remove("format"); orRefIsRef.remove("format"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("dataImport"));
        if (values.containsKey("location")) d.set("location", values.get("location"));
        if (values.containsKey("format")) d.set("format", values.get("format"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

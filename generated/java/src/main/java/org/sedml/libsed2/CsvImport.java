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

/** Generated from test-specsheets/tasks/CsvImport/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class CsvImport extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("location", "StringOrRef", true, "CsvImport-0002", "CsvImport-0001", "CsvImport-0000", null, null, null, null, null, false, 1, null, "CsvImport-0003", null, null),
        new FieldSpec("organization", "StringOrRef", false, "CsvImport-0004", null, "CsvImport-0000", null, null, null, null, null, false, null, null, "CsvImport-0005", null, null),
        new FieldSpec("separator", "StringOrRef", false, "CsvImport-0006", null, "CsvImport-0000", null, null, null, null, null, false, null, null, "CsvImport-0007", null, null),
        new FieldSpec("headers", "BooleanOrRef", false, "CsvImport-0008", null, "CsvImport-0000", null, null, null, null, null, false, null, null, "CsvImport-0009", null, null),
        new FieldSpec("columnNames", "ArrayOrRef", false, "CsvImport-0010", null, "CsvImport-0000", null, null, null, null, null, false, null, null, "CsvImport-0011", "string", null),
        new FieldSpec("ncols", "IntegerOrRef", false, "CsvImport-0012", null, "CsvImport-0000", null, 0.0, null, null, null, false, null, null, "CsvImport-0013", null, null),
        new FieldSpec("nrows", "IntegerOrRef", false, "CsvImport-0014", null, "CsvImport-0000", null, 0.0, null, null, null, false, null, null, "CsvImport-0015", null, null),
        new FieldSpec("units", "ArrayOrRef", false, "CsvImport-0016", null, "CsvImport-0000", null, null, null, null, null, false, null, null, "CsvImport-0017", "string", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("location");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "csvImport"; }
    @Override public String typeRuleId() { return "CsvImport-0018"; }
    @Override public String ownCatchall() { return "CsvImport-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "csvImport"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"valid\": true, \"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"input-file\", \"from\": \"location\", \"extract\": \"rowCount\", \"note\": \"row count, read from the CSV file at location\"}, \"labels\": null}, {\"size\": {\"source\": \"input-file\", \"from\": \"location\", \"extract\": \"columnCount\", \"note\": \"column count, read from the CSV file at location together with organization/headers/ncols\"}, \"labels\": {\"source\": \"input-file\", \"from\": \"location\", \"extract\": \"columnHeaders\", \"note\": \"column labels, read from the CSV header row when headers is true, else from columnNames\"}}]}, \"[id].model\": {\"valid\": false}, \"[id].strings\": {\"valid\": false}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public String getLocationValue() { return getOrRefValueNode("location").asText(); }
    public String getLocationRef() { return getOrRefRefNode("location").asText(); }
    public void setLocationValue(String value) { setOrRefValueNode("location", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLocationRef(String ref) { setOrRefRefNode("location", ref); }
    public boolean isLocationRef() { return isOrRefRef("location"); }
    public boolean isSetLocation() { return values.containsKey("location"); }
    public void unsetLocation() { values.remove("location"); orRefIsRef.remove("location"); }

    public String getOrganizationValue() { return getOrRefValueNode("organization").asText(); }
    public String getOrganizationRef() { return getOrRefRefNode("organization").asText(); }
    public void setOrganizationValue(String value) { setOrRefValueNode("organization", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setOrganizationRef(String ref) { setOrRefRefNode("organization", ref); }
    public boolean isOrganizationRef() { return isOrRefRef("organization"); }
    public boolean isSetOrganization() { return values.containsKey("organization"); }
    public void unsetOrganization() { values.remove("organization"); orRefIsRef.remove("organization"); }

    public String getSeparatorValue() { return getOrRefValueNode("separator").asText(); }
    public String getSeparatorRef() { return getOrRefRefNode("separator").asText(); }
    public void setSeparatorValue(String value) { setOrRefValueNode("separator", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setSeparatorRef(String ref) { setOrRefRefNode("separator", ref); }
    public boolean isSeparatorRef() { return isOrRefRef("separator"); }
    public boolean isSetSeparator() { return values.containsKey("separator"); }
    public void unsetSeparator() { values.remove("separator"); orRefIsRef.remove("separator"); }

    public boolean getHeadersValue() { return getOrRefValueNode("headers").asBoolean(); }
    public String getHeadersRef() { return getOrRefRefNode("headers").asText(); }
    public void setHeadersValue(boolean value) { setOrRefValueNode("headers", BooleanNode.valueOf(value)); }
    public void setHeadersRef(String ref) { setOrRefRefNode("headers", ref); }
    public boolean isHeadersRef() { return isOrRefRef("headers"); }
    public boolean isSetHeaders() { return values.containsKey("headers"); }
    public void unsetHeaders() { values.remove("headers"); orRefIsRef.remove("headers"); }

    public JsonNode getColumnNamesValue() { return getOrRefValueNode("columnNames"); }
    public String getColumnNamesRef() { return getOrRefRefNode("columnNames").asText(); }
    public void setColumnNamesValue(JsonNode value) { setOrRefValueNode("columnNames", value); }
    public void setColumnNamesRef(String ref) { setOrRefRefNode("columnNames", ref); }
    public boolean isColumnNamesRef() { return isOrRefRef("columnNames"); }
    public boolean isSetColumnNames() { return values.containsKey("columnNames"); }
    public void unsetColumnNames() { values.remove("columnNames"); orRefIsRef.remove("columnNames"); }

    public long getNcolsValue() { return getOrRefValueNode("ncols").asLong(); }
    public String getNcolsRef() { return getOrRefRefNode("ncols").asText(); }
    public void setNcolsValue(long value) { setOrRefValueNode("ncols", LongNode.valueOf(value)); }
    public void setNcolsRef(String ref) { setOrRefRefNode("ncols", ref); }
    public boolean isNcolsRef() { return isOrRefRef("ncols"); }
    public boolean isSetNcols() { return values.containsKey("ncols"); }
    public void unsetNcols() { values.remove("ncols"); orRefIsRef.remove("ncols"); }

    public long getNrowsValue() { return getOrRefValueNode("nrows").asLong(); }
    public String getNrowsRef() { return getOrRefRefNode("nrows").asText(); }
    public void setNrowsValue(long value) { setOrRefValueNode("nrows", LongNode.valueOf(value)); }
    public void setNrowsRef(String ref) { setOrRefRefNode("nrows", ref); }
    public boolean isNrowsRef() { return isOrRefRef("nrows"); }
    public boolean isSetNrows() { return values.containsKey("nrows"); }
    public void unsetNrows() { values.remove("nrows"); orRefIsRef.remove("nrows"); }

    public JsonNode getUnitsValue() { return getOrRefValueNode("units"); }
    public String getUnitsRef() { return getOrRefRefNode("units").asText(); }
    public void setUnitsValue(JsonNode value) { setOrRefValueNode("units", value); }
    public void setUnitsRef(String ref) { setOrRefRefNode("units", ref); }
    public boolean isUnitsRef() { return isOrRefRef("units"); }
    public boolean isSetUnits() { return values.containsKey("units"); }
    public void unsetUnits() { values.remove("units"); orRefIsRef.remove("units"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("csvImport"));
        if (values.containsKey("location")) d.set("location", values.get("location"));
        if (values.containsKey("organization")) d.set("organization", values.get("organization"));
        if (values.containsKey("separator")) d.set("separator", values.get("separator"));
        if (values.containsKey("headers")) d.set("headers", values.get("headers"));
        if (values.containsKey("columnNames")) d.set("columnNames", values.get("columnNames"));
        if (values.containsKey("ncols")) d.set("ncols", values.get("ncols"));
        if (values.containsKey("nrows")) d.set("nrows", values.get("nrows"));
        if (values.containsKey("units")) d.set("units", values.get("units"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

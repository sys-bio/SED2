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

/** Generated from test-specsheets/tasks/TypesWidget/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class TypesWidget extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("anyValue", "any", false, null, null, "TypesWidget-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("enabled", "BooleanOrRef", false, "TypesWidget-0001", null, "TypesWidget-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("count", "IntegerOrRef", false, "TypesWidget-0003", null, "TypesWidget-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("items", "ArrayOrRef", false, "TypesWidget-0004", null, "TypesWidget-0000", null, null, null, null, null, false, null, null, null, "any", null),
        new FieldSpec("settings", "DictOrRef", false, "TypesWidget-0005", null, "TypesWidget-0000", null, null, null, null, null, false, null, null, null, "any", null),
        new FieldSpec("label", "StringOrRef", false, "AbstractWidget-0001", null, "AbstractWidget-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("extras", "any-dict", false, "TypesWidget-0007", null, "TypesWidget-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("primaryNote", "ref-class", false, "TypesWidget-0006", null, "TypesWidget-0000", null, null, null, "Note", null, false, null, null, null, null, null),
        new FieldSpec("report", "ref-discriminator", false, null, null, "TypesWidget-0000", null, null, null, null, "AbstractReport", false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of();
    private final IdKeyedCollection<JsonNode> extras = new IdKeyedCollection<>();
    private SedBase primaryNote;
    private SedBase report;

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "typesWidget"; }
    @Override public String typeRuleId() { return "TypesWidget-0002"; }
    @Override public String ownCatchall() { return "TypesWidget-0000"; }
    @Override public String nameRuleId() { return "TestBase-0001"; }
    @Override public String descRuleId() { return null; }
    @Override public String baseCatchall() { return "TestBase-0000"; }
    public String getType() { return "typesWidget"; }

    public JsonNode getAnyValue() { if (!values.containsKey("anyValue")) throw new ApiError("anyValue" + " is not set"); return values.get("anyValue"); }
    public void setAnyValue(JsonNode value) { values.put("anyValue", value); }
    public boolean isSetAnyValue() { return values.containsKey("anyValue"); }
    public void unsetAnyValue() { values.remove("anyValue"); }

    public boolean getEnabledValue() { return getOrRefValueNode("enabled").asBoolean(); }
    public String getEnabledRef() { return getOrRefRefNode("enabled").asText(); }
    public void setEnabledValue(boolean value) { setOrRefValueNode("enabled", BooleanNode.valueOf(value)); }
    public void setEnabledRef(String ref) { setOrRefRefNode("enabled", ref); }
    public boolean isEnabledRef() { return isOrRefRef("enabled"); }
    public boolean isSetEnabled() { return values.containsKey("enabled"); }
    public void unsetEnabled() { values.remove("enabled"); orRefIsRef.remove("enabled"); }

    public long getCountValue() { return getOrRefValueNode("count").asLong(); }
    public String getCountRef() { return getOrRefRefNode("count").asText(); }
    public void setCountValue(long value) { setOrRefValueNode("count", LongNode.valueOf(value)); }
    public void setCountRef(String ref) { setOrRefRefNode("count", ref); }
    public boolean isCountRef() { return isOrRefRef("count"); }
    public boolean isSetCount() { return values.containsKey("count"); }
    public void unsetCount() { values.remove("count"); orRefIsRef.remove("count"); }

    public JsonNode getItemsValue() { return getOrRefValueNode("items"); }
    public String getItemsRef() { return getOrRefRefNode("items").asText(); }
    public void setItemsValue(JsonNode value) { setOrRefValueNode("items", value); }
    public void setItemsRef(String ref) { setOrRefRefNode("items", ref); }
    public boolean isItemsRef() { return isOrRefRef("items"); }
    public boolean isSetItems() { return values.containsKey("items"); }
    public void unsetItems() { values.remove("items"); orRefIsRef.remove("items"); }

    public JsonNode getSettingsValue() { return getOrRefValueNode("settings"); }
    public String getSettingsRef() { return getOrRefRefNode("settings").asText(); }
    public void setSettingsValue(JsonNode value) { setOrRefValueNode("settings", value); }
    public void setSettingsRef(String ref) { setOrRefRefNode("settings", ref); }
    public boolean isSettingsRef() { return isOrRefRef("settings"); }
    public boolean isSetSettings() { return values.containsKey("settings"); }
    public void unsetSettings() { values.remove("settings"); orRefIsRef.remove("settings"); }

    public String getLabelValue() { return getOrRefValueNode("label").asText(); }
    public String getLabelRef() { return getOrRefRefNode("label").asText(); }
    public void setLabelValue(String value) { setOrRefValueNode("label", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLabelRef(String ref) { setOrRefRefNode("label", ref); }
    public boolean isLabelRef() { return isOrRefRef("label"); }
    public boolean isSetLabel() { return values.containsKey("label"); }
    public void unsetLabel() { values.remove("label"); orRefIsRef.remove("label"); }

    public List<String> getExtras() { return extras.ids(); }
    public JsonNode getExtrasItem(String itemId) { return extras.get(itemId); }
    public void addExtras(String itemId, JsonNode value) { extras.add(itemId, value); }
    public void insertExtras(int index, String itemId, JsonNode value) { extras.insert(index, itemId, value); }
    public void removeExtras(String itemId) { extras.remove(itemId); }
    public void setIdOnExtras(String oldId, String newId) { extras.setId(oldId, newId); }

    public SedBase getPrimaryNote() { if (primaryNote == null) throw new ApiError("primaryNote" + " is not set"); return primaryNote; }
    public void setPrimaryNote(SedBase obj) { primaryNote = obj; obj.attach(this, getDocument()); }
    public boolean isSetPrimaryNote() { return primaryNote != null; }
    public void unsetPrimaryNote() { primaryNote = null; }

    public SedBase getReport() { if (report == null) throw new ApiError("report" + " is not set"); return report; }
    public void setReport(SedBase obj) { report = obj; obj.attach(this, getDocument()); }
    public boolean isSetReport() { return report != null; }
    public void unsetReport() { report = null; }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        if (primaryNote != null) kids.add(primaryNote);
        if (report != null) kids.add(report);
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        if (primaryNote != null) out.add(new ChildLoc(primaryNote, "/primaryNote"));
        if (report != null) out.add(new ChildLoc(report, "/report"));
        return out;
    }

    @Override
    public IdCollection getIdCollection(String fieldName) {
        switch (fieldName) {
            case "extras": return extras;
            default: return null;
        }
    }

    @Override
    public List<String> idCollectionNames() { return List.of("extras"); }

    @Override
    protected IdKeyedCollection<JsonNode> getAnyDictCollection(String fieldName) {
        switch (fieldName) {
            case "extras": return extras;
            default: return super.getAnyDictCollection(fieldName);
        }
    }

    @Override
    protected void setChildField(String fieldName, SedBase child) {
        switch (fieldName) {
            case "primaryNote": primaryNote = child; return;
            case "report": report = child; return;
            default: super.setChildField(fieldName, child);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("typesWidget"));
        if (values.containsKey("anyValue")) d.set("anyValue", values.get("anyValue"));
        if (values.containsKey("enabled")) d.set("enabled", values.get("enabled"));
        if (values.containsKey("count")) d.set("count", values.get("count"));
        if (values.containsKey("items")) d.set("items", values.get("items"));
        if (values.containsKey("settings")) d.set("settings", values.get("settings"));
        if (values.containsKey("label")) d.set("label", values.get("label"));
        if (extras.size() > 0) { ObjectNode sub = d.putObject("extras"); for (String i : extras.ids()) sub.set(i, extras.get(i)); }
        if (primaryNote != null) d.set("primaryNote", primaryNote.toJsonValue());
        if (report != null) d.set("report", report.toJsonValue());
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

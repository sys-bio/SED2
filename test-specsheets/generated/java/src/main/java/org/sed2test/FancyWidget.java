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

/** Generated from test-specsheets/tasks/FancyWidget/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class FancyWidget extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("value", "StringOrRef", true, null, "FancyWidget-0001", "FancyWidget-0000", null, null, null, null, null, false),
        new FieldSpec("label", "StringOrRef", false, "AbstractWidget-0001", null, "AbstractWidget-0000", null, null, null, null, null, false),
        new FieldSpec("retries", "integer", false, "WidgetOptions-0001", null, "WidgetOptions-0000", 0.0, null, null, null, null, false),
        new FieldSpec("timeoutSeconds", "number", false, "WidgetOptions-0002", null, "WidgetOptions-0000", null, 0.0, null, null, null, false),
        new FieldSpec("choices", "dict", false, null, null, "FancyWidget-0000", null, null, null, null, "ChoiceInline", false),
        new FieldSpec("notes", "array", false, null, null, "WidgetOptions-0000", null, null, null, "Note", null, false)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("value");
    private final IdKeyedCollection<SedBase> choices = new IdKeyedCollection<>();
    private final ListCollection<SedBase> notes = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "fancyWidget"; }
    @Override public String typeRuleId() { return "FancyWidget-0002"; }
    @Override public String ownCatchall() { return "FancyWidget-0000"; }
    @Override public String nameRuleId() { return "TestBase-0001"; }
    @Override public String descRuleId() { return null; }
    @Override public String baseCatchall() { return "TestBase-0000"; }
    public String getType() { return "fancyWidget"; }

    public String getValueValue() { return getOrRefValueNode("value").asText(); }
    public String getValueRef() { return getOrRefRefNode("value").asText(); }
    public void setValueValue(String value) { setOrRefValueNode("value", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setValueRef(String ref) { setOrRefRefNode("value", ref); }
    public boolean isValueRef() { return isOrRefRef("value"); }
    public boolean isSetValue() { return values.containsKey("value"); }
    public void unsetValue() { values.remove("value"); orRefIsRef.remove("value"); }

    public String getLabelValue() { return getOrRefValueNode("label").asText(); }
    public String getLabelRef() { return getOrRefRefNode("label").asText(); }
    public void setLabelValue(String value) { setOrRefValueNode("label", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLabelRef(String ref) { setOrRefRefNode("label", ref); }
    public boolean isLabelRef() { return isOrRefRef("label"); }
    public boolean isSetLabel() { return values.containsKey("label"); }
    public void unsetLabel() { values.remove("label"); orRefIsRef.remove("label"); }

    public long getRetries() { if (!values.containsKey("retries")) throw new ApiError("retries" + " is not set"); return values.get("retries").asLong(); }
    public void setRetries(long value) { values.put("retries", LongNode.valueOf(value)); }
    public boolean isSetRetries() { return values.containsKey("retries"); }
    public void unsetRetries() { values.remove("retries"); }

    public double getTimeoutSeconds() { if (!values.containsKey("timeoutSeconds")) throw new ApiError("timeoutSeconds" + " is not set"); return values.get("timeoutSeconds").asDouble(); }
    public void setTimeoutSeconds(double value) { values.put("timeoutSeconds", DoubleNode.valueOf(value)); }
    public boolean isSetTimeoutSeconds() { return values.containsKey("timeoutSeconds"); }
    public void unsetTimeoutSeconds() { values.remove("timeoutSeconds"); }

    public List<String> getChoices() { return choices.ids(); }
    public SedBase getChoicesItem(String itemId) { return choices.get(itemId); }
    public void addChoices(String itemId, SedBase obj) { choices.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertChoices(int index, String itemId, SedBase obj) { choices.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeChoices(String itemId) { choices.remove(itemId); }
    public void setIdOnChoices(String oldId, String newId) { choices.setId(oldId, newId); }

    public List<SedBase> getNotes() { return notes.items(); }
    public void addNotes(SedBase obj) { notes.add(obj); obj.attach(this, getDocument()); }
    public void insertNotes(int index, SedBase obj) { notes.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeNotes(int index) { notes.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        for (String i : choices.ids()) kids.add(choices.get(i));
        kids.addAll(notes.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : choices.ids()) out.add(new ChildLoc(choices.get(i), "/choices/" + i));
        { int idx = 0; for (SedBase item : notes.items()) { out.add(new ChildLoc(item, "/notes/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        switch (fieldName) {
            case "choices": return choices;
            default: return super.getDictCollection(fieldName);
        }
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "notes": return notes;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("fancyWidget"));
        if (values.containsKey("value")) d.set("value", values.get("value"));
        if (values.containsKey("label")) d.set("label", values.get("label"));
        if (values.containsKey("retries")) d.set("retries", values.get("retries"));
        if (values.containsKey("timeoutSeconds")) d.set("timeoutSeconds", values.get("timeoutSeconds"));
        if (choices.size() > 0) { ObjectNode sub = d.putObject("choices"); for (String i : choices.ids()) sub.set(i, choices.get(i).toJsonValue()); }
        if (notes.size() > 0) { ArrayNode arr = d.putArray("notes"); for (SedBase item : notes.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

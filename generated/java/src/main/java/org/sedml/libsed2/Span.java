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

/** Generated from test-specsheets/tasks/Span/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Span extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("start", "NumberOrRef", true, "Span-0002", "Span-0001", "Span-0000", null, null, null, null, null, false, null, null, "Span-0003", null, null),
        new FieldSpec("end", "NumberOrRef", true, "Span-0005", "Span-0004", "Span-0000", null, null, null, null, null, false, null, null, "Span-0006", null, null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("start", "end");
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "span"; }
    @Override public String typeRuleId() { return "Span-0007"; }
    @Override public String ownCatchall() { return "Span-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "span"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public double getStartValue() { return getOrRefValueNode("start").asDouble(); }
    public String getStartRef() { return getOrRefRefNode("start").asText(); }
    public void setStartValue(double value) { setOrRefValueNode("start", DoubleNode.valueOf(value)); }
    public void setStartRef(String ref) { setOrRefRefNode("start", ref); }
    public boolean isStartRef() { return isOrRefRef("start"); }
    public boolean isSetStart() { return values.containsKey("start"); }
    public void unsetStart() { values.remove("start"); orRefIsRef.remove("start"); }

    public double getEndValue() { return getOrRefValueNode("end").asDouble(); }
    public String getEndRef() { return getOrRefRefNode("end").asText(); }
    public void setEndValue(double value) { setOrRefValueNode("end", DoubleNode.valueOf(value)); }
    public void setEndRef(String ref) { setOrRefRefNode("end", ref); }
    public boolean isEndRef() { return isOrRefRef("end"); }
    public boolean isSetEnd() { return values.containsKey("end"); }
    public void unsetEnd() { values.remove("end"); orRefIsRef.remove("end"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

    public List<SedBase> getAnnotations() { return annotations.items(); }
    public void addAnnotations(SedBase obj) { annotations.add(obj); obj.attach(this, getDocument()); }
    public void insertAnnotations(int index, SedBase obj) { annotations.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeAnnotations(int index) { annotations.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        kids.addAll(annotations.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "annotations": return annotations;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("span"));
        if (values.containsKey("start")) d.set("start", values.get("start"));
        if (values.containsKey("end")) d.set("end", values.get("end"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

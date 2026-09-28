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

/** Generated from test-specsheets/auxiliary/LoopVariable/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class LoopVariable extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("initialValue", "any", true, null, "LoopVariable-0001", "LoopVariable-0000", null, null, null, null, null, false),
        new FieldSpec("subsequentValues", "SIdRef", true, "LoopVariable-0003", "LoopVariable-0002", "LoopVariable-0000", null, null, null, null, null, false),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("initialValue", "subsequentValues");
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "LoopVariable-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }

    public JsonNode getInitialValue() { if (!values.containsKey("initialValue")) throw new ApiError("initialValue" + " is not set"); return values.get("initialValue"); }
    public void setInitialValue(JsonNode value) { values.put("initialValue", value); }
    public boolean isSetInitialValue() { return values.containsKey("initialValue"); }
    public void unsetInitialValue() { values.remove("initialValue"); }

    public String getSubsequentValues() { if (!values.containsKey("subsequentValues")) throw new ApiError("subsequentValues" + " is not set"); return values.get("subsequentValues").asText(); }
    public void setSubsequentValues(String value) { values.put("subsequentValues", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetSubsequentValues() { return values.containsKey("subsequentValues"); }
    public void unsetSubsequentValues() { values.remove("subsequentValues"); }

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
        if (values.containsKey("initialValue")) d.set("initialValue", values.get("initialValue"));
        if (values.containsKey("subsequentValues")) d.set("subsequentValues", values.get("subsequentValues"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

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

/** Generated from test-specsheets/core/SEDDocument/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class SEDDocument extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("version", "string", true, "SEDDocument-0002", "SEDDocument-0001", "SEDDocument-0000", null, null, "^v\\d+\\.\\d+\\.\\d+$", null, null, false, null, null, "SEDDocument-0003", null, null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("constants", "any-dict", false, "SEDDocument-0005", null, "SEDDocument-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("tasks", "dict", false, "SEDDocument-0006", null, "SEDDocument-0000", null, null, null, null, "AbstractTask", false, null, null, null, null, null),
        new FieldSpec("outputs", "dict", false, "SEDDocument-0007", null, "SEDDocument-0000", null, null, null, null, "AbstractOutput", false, null, null, null, null, null),
        new FieldSpec("styles", "dict", false, "SEDDocument-0008", null, "SEDDocument-0000", null, null, null, "Style", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("version");
    private final IdKeyedCollection<JsonNode> constants = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> tasks = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> outputs = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> styles = new IdKeyedCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "SEDDocument-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public SEDDocument() { attach(null, this); }
    @Override public boolean isDocumentClass() { return true; }
    @Override public String maxKnownDocumentVersion() { return "v1.0.0"; }

    public String getVersion() { if (!values.containsKey("version")) throw new ApiError("version" + " is not set"); return values.get("version").asText(); }
    public void setVersion(String value) { values.put("version", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetVersion() { return values.containsKey("version"); }
    public void unsetVersion() { values.remove("version"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

    public List<String> getConstants() { return constants.ids(); }
    public JsonNode getConstantsItem(String itemId) { return constants.get(itemId); }
    public void addConstants(String itemId, JsonNode value) { constants.add(itemId, value); }
    public void insertConstants(int index, String itemId, JsonNode value) { constants.insert(index, itemId, value); }
    public void removeConstants(String itemId) { constants.remove(itemId); }
    public void setIdOnConstants(String oldId, String newId) { constants.setId(oldId, newId); }

    public List<String> getTasks() { return tasks.ids(); }
    public SedBase getTasksItem(String itemId) { return tasks.get(itemId); }
    public void addTasks(String itemId, SedBase obj) { tasks.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertTasks(int index, String itemId, SedBase obj) { tasks.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeTasks(String itemId) { tasks.remove(itemId); }
    public void setIdOnTasks(String oldId, String newId) { tasks.setId(oldId, newId); }

    public List<String> getOutputs() { return outputs.ids(); }
    public SedBase getOutputsItem(String itemId) { return outputs.get(itemId); }
    public void addOutputs(String itemId, SedBase obj) { outputs.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertOutputs(int index, String itemId, SedBase obj) { outputs.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeOutputs(String itemId) { outputs.remove(itemId); }
    public void setIdOnOutputs(String oldId, String newId) { outputs.setId(oldId, newId); }

    public List<String> getStyles() { return styles.ids(); }
    public SedBase getStylesItem(String itemId) { return styles.get(itemId); }
    public void addStyles(String itemId, SedBase obj) { styles.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertStyles(int index, String itemId, SedBase obj) { styles.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeStyles(String itemId) { styles.remove(itemId); }
    public void setIdOnStyles(String oldId, String newId) { styles.setId(oldId, newId); }

    public List<SedBase> getAnnotations() { return annotations.items(); }
    public void addAnnotations(SedBase obj) { annotations.add(obj); obj.attach(this, getDocument()); }
    public void insertAnnotations(int index, SedBase obj) { annotations.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeAnnotations(int index) { annotations.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        for (String i : tasks.ids()) kids.add(tasks.get(i));
        for (String i : outputs.ids()) kids.add(outputs.get(i));
        for (String i : styles.ids()) kids.add(styles.get(i));
        kids.addAll(annotations.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : tasks.ids()) out.add(new ChildLoc(tasks.get(i), "/tasks/" + i));
        for (String i : outputs.ids()) out.add(new ChildLoc(outputs.get(i), "/outputs/" + i));
        for (String i : styles.ids()) out.add(new ChildLoc(styles.get(i), "/styles/" + i));
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        return out;
    }

    @Override
    public IdCollection getIdCollection(String fieldName) {
        switch (fieldName) {
            case "constants": return constants;
            case "tasks": return tasks;
            case "outputs": return outputs;
            case "styles": return styles;
            default: return null;
        }
    }

    @Override
    public List<String> idCollectionNames() { return List.of("constants", "tasks", "outputs", "styles"); }

    @Override
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        switch (fieldName) {
            case "tasks": return tasks;
            case "outputs": return outputs;
            case "styles": return styles;
            default: return super.getDictCollection(fieldName);
        }
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "annotations": return annotations;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    protected IdKeyedCollection<JsonNode> getAnyDictCollection(String fieldName) {
        switch (fieldName) {
            case "constants": return constants;
            default: return super.getAnyDictCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        if (values.containsKey("version")) d.set("version", values.get("version"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (tasks.size() > 0) { ObjectNode sub = d.putObject("tasks"); for (String i : tasks.ids()) sub.set(i, tasks.get(i).toJsonValue()); }
        if (outputs.size() > 0) { ObjectNode sub = d.putObject("outputs"); for (String i : outputs.ids()) sub.set(i, outputs.get(i).toJsonValue()); }
        if (styles.size() > 0) { ObjectNode sub = d.putObject("styles"); for (String i : styles.ids()) sub.set(i, styles.get(i).toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        if (constants.size() > 0) { ObjectNode sub = d.putObject("constants"); for (String i : constants.ids()) sub.set(i, constants.get(i)); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

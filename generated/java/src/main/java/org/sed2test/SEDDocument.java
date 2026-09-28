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

/** Generated from test-specsheets/core/SEDDocument/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class SEDDocument extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("version", "string", true, ["SEDDocument-0002", "SEDDocument-0003"], "SEDDocument-0001", "SEDDocument-0000", null, null, "^v\\d+\\.\\d+\\.\\d+$", null, null),
        new FieldSpec("tasks", "dict", false, "SEDDocument-0006", null, "SEDDocument-0000", null, null, null, null, "AbstractTask"),
        new FieldSpec("outputs", "dict", false, "SEDDocument-0007", null, "SEDDocument-0000", null, null, null, null, "AbstractOutput"),
        new FieldSpec("styles", "dict", false, "SEDDocument-0008", null, "SEDDocument-0000", null, null, null, "Style", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("version");
    private final IdKeyedCollection<SedBase> tasks = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> outputs = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> styles = new IdKeyedCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "SEDDocument-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }

    public String getVersion() { if (!values.containsKey("version")) throw new ApiError("version" + " is not set"); return values.get("version").asText(); }
    public void setVersion(String value) { values.put("version", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetVersion() { return values.containsKey("version"); }
    public void unsetVersion() { values.remove("version"); }

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

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        for (String i : tasks.ids()) kids.add(tasks.get(i));
        for (String i : outputs.ids()) kids.add(outputs.get(i));
        for (String i : styles.ids()) kids.add(styles.get(i));
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : tasks.ids()) out.add(new ChildLoc(tasks.get(i), "/tasks/" + i));
        for (String i : outputs.ids()) out.add(new ChildLoc(outputs.get(i), "/outputs/" + i));
        for (String i : styles.ids()) out.add(new ChildLoc(styles.get(i), "/styles/" + i));
        return out;
    }

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
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        if (values.containsKey("version")) d.set("version", values.get("version"));
        if (tasks.size() > 0) { ObjectNode sub = d.putObject("tasks"); for (String i : tasks.ids()) sub.set(i, tasks.get(i).toJsonValue()); }
        if (outputs.size() > 0) { ObjectNode sub = d.putObject("outputs"); for (String i : outputs.ids()) sub.set(i, outputs.get(i).toJsonValue()); }
        if (styles.size() > 0) { ObjectNode sub = d.putObject("styles"); for (String i : styles.ids()) sub.set(i, styles.get(i).toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

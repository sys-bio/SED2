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

/** Generated from test-specsheets/tasks/Loop/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Loop extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("loopVariables", "dict", true, "Loop-0003", "Loop-0002", "Loop-0000", null, null, null, "LoopVariable", null),
        new FieldSpec("subTasks", "dict", false, "Repeat-0001", null, "Repeat-0000", null, null, null, null, "AbstractTask"),
        new FieldSpec("aggregateOutputVariables", "dict", false, "Repeat-0004", null, "Repeat-0000", null, null, null, "AggregationCalculation", null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("loopVariables");
    private final IdKeyedCollection<SedBase> loopVariables = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> subTasks = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> aggregateOutputVariables = new IdKeyedCollection<>();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "loop"; }
    @Override public String typeRuleId() { return "Loop-0005"; }
    @Override public String ownCatchall() { return "Loop-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "loop"; }

    public List<String> getLoopVariables() { return loopVariables.ids(); }
    public SedBase getLoopVariablesItem(String itemId) { return loopVariables.get(itemId); }
    public void addLoopVariables(String itemId, SedBase obj) { loopVariables.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertLoopVariables(int index, String itemId, SedBase obj) { loopVariables.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeLoopVariables(String itemId) { loopVariables.remove(itemId); }
    public void setIdOnLoopVariables(String oldId, String newId) { loopVariables.setId(oldId, newId); }

    public List<String> getSubTasks() { return subTasks.ids(); }
    public SedBase getSubTasksItem(String itemId) { return subTasks.get(itemId); }
    public void addSubTasks(String itemId, SedBase obj) { subTasks.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertSubTasks(int index, String itemId, SedBase obj) { subTasks.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeSubTasks(String itemId) { subTasks.remove(itemId); }
    public void setIdOnSubTasks(String oldId, String newId) { subTasks.setId(oldId, newId); }

    public List<String> getAggregateOutputVariables() { return aggregateOutputVariables.ids(); }
    public SedBase getAggregateOutputVariablesItem(String itemId) { return aggregateOutputVariables.get(itemId); }
    public void addAggregateOutputVariables(String itemId, SedBase obj) { aggregateOutputVariables.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertAggregateOutputVariables(int index, String itemId, SedBase obj) { aggregateOutputVariables.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeAggregateOutputVariables(String itemId) { aggregateOutputVariables.remove(itemId); }
    public void setIdOnAggregateOutputVariables(String oldId, String newId) { aggregateOutputVariables.setId(oldId, newId); }

    public List<SedBase> getTaskParameters() { return taskParameters.items(); }
    public void addTaskParameters(SedBase obj) { taskParameters.add(obj); obj.attach(this, getDocument()); }
    public void insertTaskParameters(int index, SedBase obj) { taskParameters.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeTaskParameters(int index) { taskParameters.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        for (String i : loopVariables.ids()) kids.add(loopVariables.get(i));
        for (String i : subTasks.ids()) kids.add(subTasks.get(i));
        for (String i : aggregateOutputVariables.ids()) kids.add(aggregateOutputVariables.get(i));
        kids.addAll(taskParameters.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : loopVariables.ids()) out.add(new ChildLoc(loopVariables.get(i), "/loopVariables/" + i));
        for (String i : subTasks.ids()) out.add(new ChildLoc(subTasks.get(i), "/subTasks/" + i));
        for (String i : aggregateOutputVariables.ids()) out.add(new ChildLoc(aggregateOutputVariables.get(i), "/aggregateOutputVariables/" + i));
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        switch (fieldName) {
            case "loopVariables": return loopVariables;
            case "subTasks": return subTasks;
            case "aggregateOutputVariables": return aggregateOutputVariables;
            default: return super.getDictCollection(fieldName);
        }
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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("loop"));
        if (loopVariables.size() > 0) { ObjectNode sub = d.putObject("loopVariables"); for (String i : loopVariables.ids()) sub.set(i, loopVariables.get(i).toJsonValue()); }
        if (subTasks.size() > 0) { ObjectNode sub = d.putObject("subTasks"); for (String i : subTasks.ids()) sub.set(i, subTasks.get(i).toJsonValue()); }
        if (aggregateOutputVariables.size() > 0) { ObjectNode sub = d.putObject("aggregateOutputVariables"); for (String i : aggregateOutputVariables.ids()) sub.set(i, aggregateOutputVariables.get(i).toJsonValue()); }
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

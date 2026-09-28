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

/** Generated from test-specsheets/tasks/CreateDataBlock/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class CreateDataBlock extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("data");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "createDataBlock"; }
    @Override public String typeRuleId() { return "CreateDataBlock-0004"; }
    @Override public String ownCatchall() { return "CreateDataBlock-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "createDataBlock"; }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("createDataBlock"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

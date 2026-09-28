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

/** Generated from test-specsheets/tasks/ExplicitStochasticSimulation/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class ExplicitStochasticSimulation extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("seed", "NumberOrRef", false, "AbstractStochasticSimulation-0001", null, "AbstractStochasticSimulation-0000", null, null, null, null, null),
        new FieldSpec("timeDependentRelativeTolerance", "NumberOrRef", false, "AbstractStochasticSimulation-0003", null, "AbstractStochasticSimulation-0000", null, null, null, null, null),
        new FieldSpec("minimumTimeStep", "NumberOrRef", false, "AbstractStochasticSimulation-0007", null, "AbstractStochasticSimulation-0000", null, null, null, null, null),
        new FieldSpec("maximumTimeStep", "NumberOrRef", false, "AbstractStochasticSimulation-0009", null, "AbstractStochasticSimulation-0000", null, null, null, null, null),
        new FieldSpec("model", "SIdRef", false, "AbstractSimulation-0001", null, "AbstractSimulation-0000", null, null, null, null, null),
        new FieldSpec("independentVariable", "StringOrRef", false, "AbstractSimulation-0002", null, "AbstractSimulation-0000", null, null, null, null, null),
        new FieldSpec("independentVariableInit", "NumberOrRef", false, "AbstractSimulation-0004", null, "AbstractSimulation-0000", null, null, null, null, null),
        new FieldSpec("workingAlgorithms", "array", false, "AbstractSimulation-0008", null, "AbstractSimulation-0000", null, null, null, "WorkingAlgorithm", null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("independentVariableRange");
    private final ListCollection<SedBase> workingAlgorithms = new ListCollection<>();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "explicitStochasticSimulation"; }
    @Override public String typeRuleId() { return "ExplicitStochasticSimulation-0006"; }
    @Override public String ownCatchall() { return "ExplicitStochasticSimulation-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "explicitStochasticSimulation"; }

    public double getSeedValue() { return getOrRefValueNode("seed").asDouble(); }
    public String getSeedRef() { return getOrRefRefNode("seed").asText(); }
    public void setSeedValue(double value) { setOrRefValueNode("seed", DoubleNode.valueOf(value)); }
    public void setSeedRef(String ref) { setOrRefRefNode("seed", ref); }
    public boolean isSeedRef() { return isOrRefRef("seed"); }
    public boolean isSetSeed() { return values.containsKey("seed"); }
    public void unsetSeed() { values.remove("seed"); orRefIsRef.remove("seed"); }

    public double getTimeDependentRelativeToleranceValue() { return getOrRefValueNode("timeDependentRelativeTolerance").asDouble(); }
    public String getTimeDependentRelativeToleranceRef() { return getOrRefRefNode("timeDependentRelativeTolerance").asText(); }
    public void setTimeDependentRelativeToleranceValue(double value) { setOrRefValueNode("timeDependentRelativeTolerance", DoubleNode.valueOf(value)); }
    public void setTimeDependentRelativeToleranceRef(String ref) { setOrRefRefNode("timeDependentRelativeTolerance", ref); }
    public boolean isTimeDependentRelativeToleranceRef() { return isOrRefRef("timeDependentRelativeTolerance"); }
    public boolean isSetTimeDependentRelativeTolerance() { return values.containsKey("timeDependentRelativeTolerance"); }
    public void unsetTimeDependentRelativeTolerance() { values.remove("timeDependentRelativeTolerance"); orRefIsRef.remove("timeDependentRelativeTolerance"); }

    public double getMinimumTimeStepValue() { return getOrRefValueNode("minimumTimeStep").asDouble(); }
    public String getMinimumTimeStepRef() { return getOrRefRefNode("minimumTimeStep").asText(); }
    public void setMinimumTimeStepValue(double value) { setOrRefValueNode("minimumTimeStep", DoubleNode.valueOf(value)); }
    public void setMinimumTimeStepRef(String ref) { setOrRefRefNode("minimumTimeStep", ref); }
    public boolean isMinimumTimeStepRef() { return isOrRefRef("minimumTimeStep"); }
    public boolean isSetMinimumTimeStep() { return values.containsKey("minimumTimeStep"); }
    public void unsetMinimumTimeStep() { values.remove("minimumTimeStep"); orRefIsRef.remove("minimumTimeStep"); }

    public double getMaximumTimeStepValue() { return getOrRefValueNode("maximumTimeStep").asDouble(); }
    public String getMaximumTimeStepRef() { return getOrRefRefNode("maximumTimeStep").asText(); }
    public void setMaximumTimeStepValue(double value) { setOrRefValueNode("maximumTimeStep", DoubleNode.valueOf(value)); }
    public void setMaximumTimeStepRef(String ref) { setOrRefRefNode("maximumTimeStep", ref); }
    public boolean isMaximumTimeStepRef() { return isOrRefRef("maximumTimeStep"); }
    public boolean isSetMaximumTimeStep() { return values.containsKey("maximumTimeStep"); }
    public void unsetMaximumTimeStep() { values.remove("maximumTimeStep"); orRefIsRef.remove("maximumTimeStep"); }

    public String getModel() { if (!values.containsKey("model")) throw new ApiError("model" + " is not set"); return values.get("model").asText(); }
    public void setModel(String value) { values.put("model", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetModel() { return values.containsKey("model"); }
    public void unsetModel() { values.remove("model"); }

    public String getIndependentVariableValue() { return getOrRefValueNode("independentVariable").asText(); }
    public String getIndependentVariableRef() { return getOrRefRefNode("independentVariable").asText(); }
    public void setIndependentVariableValue(String value) { setOrRefValueNode("independentVariable", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setIndependentVariableRef(String ref) { setOrRefRefNode("independentVariable", ref); }
    public boolean isIndependentVariableRef() { return isOrRefRef("independentVariable"); }
    public boolean isSetIndependentVariable() { return values.containsKey("independentVariable"); }
    public void unsetIndependentVariable() { values.remove("independentVariable"); orRefIsRef.remove("independentVariable"); }

    public double getIndependentVariableInitValue() { return getOrRefValueNode("independentVariableInit").asDouble(); }
    public String getIndependentVariableInitRef() { return getOrRefRefNode("independentVariableInit").asText(); }
    public void setIndependentVariableInitValue(double value) { setOrRefValueNode("independentVariableInit", DoubleNode.valueOf(value)); }
    public void setIndependentVariableInitRef(String ref) { setOrRefRefNode("independentVariableInit", ref); }
    public boolean isIndependentVariableInitRef() { return isOrRefRef("independentVariableInit"); }
    public boolean isSetIndependentVariableInit() { return values.containsKey("independentVariableInit"); }
    public void unsetIndependentVariableInit() { values.remove("independentVariableInit"); orRefIsRef.remove("independentVariableInit"); }

    public List<SedBase> getWorkingAlgorithms() { return workingAlgorithms.items(); }
    public void addWorkingAlgorithms(SedBase obj) { workingAlgorithms.add(obj); obj.attach(this, getDocument()); }
    public void insertWorkingAlgorithms(int index, SedBase obj) { workingAlgorithms.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeWorkingAlgorithms(int index) { workingAlgorithms.remove(index); }

    public List<SedBase> getTaskParameters() { return taskParameters.items(); }
    public void addTaskParameters(SedBase obj) { taskParameters.add(obj); obj.attach(this, getDocument()); }
    public void insertTaskParameters(int index, SedBase obj) { taskParameters.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeTaskParameters(int index) { taskParameters.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        kids.addAll(workingAlgorithms.items());
        kids.addAll(taskParameters.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : workingAlgorithms.items()) { out.add(new ChildLoc(item, "/workingAlgorithms/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "workingAlgorithms": return workingAlgorithms;
            case "taskParameters": return taskParameters;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("explicitStochasticSimulation"));
        if (values.containsKey("seed")) d.set("seed", values.get("seed"));
        if (values.containsKey("timeDependentRelativeTolerance")) d.set("timeDependentRelativeTolerance", values.get("timeDependentRelativeTolerance"));
        if (values.containsKey("minimumTimeStep")) d.set("minimumTimeStep", values.get("minimumTimeStep"));
        if (values.containsKey("maximumTimeStep")) d.set("maximumTimeStep", values.get("maximumTimeStep"));
        if (values.containsKey("model")) d.set("model", values.get("model"));
        if (values.containsKey("independentVariable")) d.set("independentVariable", values.get("independentVariable"));
        if (values.containsKey("independentVariableInit")) d.set("independentVariableInit", values.get("independentVariableInit"));
        if (workingAlgorithms.size() > 0) { ArrayNode arr = d.putArray("workingAlgorithms"); for (SedBase item : workingAlgorithms.items()) arr.add(item.toJsonValue()); }
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

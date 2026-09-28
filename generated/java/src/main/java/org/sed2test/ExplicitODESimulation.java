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

/** Generated from test-specsheets/tasks/ExplicitODESimulation/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class ExplicitODESimulation extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("relativeTolerance", "NumberOrRef", false, ["AbstractODESimulation-0001", "AbstractODESimulation-0002"], null, "AbstractODESimulation-0000", null, null, null, null, null),
        new FieldSpec("absoluteTolerance", "NumberOrRef", false, ["AbstractODESimulation-0003", "AbstractODESimulation-0004"], null, "AbstractODESimulation-0000", null, null, null, null, null),
        new FieldSpec("absoluteToleranceAdjustmentFactor", "NumberOrRef", false, ["AbstractODESimulation-0007", "AbstractODESimulation-0008"], null, "AbstractODESimulation-0000", null, null, null, null, null),
        new FieldSpec("toleranceForRootFinder", "NumberOrRef", false, ["AbstractODESimulation-0009", "AbstractODESimulation-0010"], null, "AbstractODESimulation-0000", null, null, null, null, null),
        new FieldSpec("initialStepSize", "NumberOrRef", false, ["AbstractODESimulation-0011", "AbstractODESimulation-0012"], null, "AbstractODESimulation-0000", null, null, null, null, null),
        new FieldSpec("maxNumberOfSteps", "NumberOrRef", false, ["AbstractODESimulation-0013", "AbstractODESimulation-0014"], null, "AbstractODESimulation-0000", null, null, null, null, null),
        new FieldSpec("maxInternalStepSize", "NumberOrRef", false, ["AbstractODESimulation-0017", "AbstractODESimulation-0018"], null, "AbstractODESimulation-0000", null, null, null, null, null),
        new FieldSpec("minInternalStepSize", "NumberOrRef", false, ["AbstractODESimulation-0019", "AbstractODESimulation-0020"], null, "AbstractODESimulation-0000", null, null, null, null, null),
        new FieldSpec("model", "SIdRef", false, "AbstractSimulation-0001", null, "AbstractSimulation-0000", null, null, null, null, null),
        new FieldSpec("independentVariable", "StringOrRef", false, ["AbstractSimulation-0002", "AbstractSimulation-0003"], null, "AbstractSimulation-0000", null, null, null, null, null),
        new FieldSpec("independentVariableInit", "NumberOrRef", false, ["AbstractSimulation-0004", "AbstractSimulation-0005"], null, "AbstractSimulation-0000", null, null, null, null, null),
        new FieldSpec("workingAlgorithms", "array", false, "AbstractSimulation-0008", null, "AbstractSimulation-0000", null, null, null, "WorkingAlgorithm", null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("independentVariableRange");
    private final ListCollection<SedBase> workingAlgorithms = new ListCollection<>();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "explicitODESimulation"; }
    @Override public String typeRuleId() { return "ExplicitODESimulation-0006"; }
    @Override public String ownCatchall() { return "ExplicitODESimulation-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "explicitODESimulation"; }

    public double getRelativeToleranceValue() { return getOrRefValueNode("relativeTolerance").asDouble(); }
    public String getRelativeToleranceRef() { return getOrRefRefNode("relativeTolerance").asText(); }
    public void setRelativeToleranceValue(double value) { setOrRefValueNode("relativeTolerance", DoubleNode.valueOf(value)); }
    public void setRelativeToleranceRef(String ref) { setOrRefRefNode("relativeTolerance", ref); }
    public boolean isRelativeToleranceRef() { return isOrRefRef("relativeTolerance"); }
    public boolean isSetRelativeTolerance() { return values.containsKey("relativeTolerance"); }
    public void unsetRelativeTolerance() { values.remove("relativeTolerance"); orRefIsRef.remove("relativeTolerance"); }

    public double getAbsoluteToleranceValue() { return getOrRefValueNode("absoluteTolerance").asDouble(); }
    public String getAbsoluteToleranceRef() { return getOrRefRefNode("absoluteTolerance").asText(); }
    public void setAbsoluteToleranceValue(double value) { setOrRefValueNode("absoluteTolerance", DoubleNode.valueOf(value)); }
    public void setAbsoluteToleranceRef(String ref) { setOrRefRefNode("absoluteTolerance", ref); }
    public boolean isAbsoluteToleranceRef() { return isOrRefRef("absoluteTolerance"); }
    public boolean isSetAbsoluteTolerance() { return values.containsKey("absoluteTolerance"); }
    public void unsetAbsoluteTolerance() { values.remove("absoluteTolerance"); orRefIsRef.remove("absoluteTolerance"); }

    public double getAbsoluteToleranceAdjustmentFactorValue() { return getOrRefValueNode("absoluteToleranceAdjustmentFactor").asDouble(); }
    public String getAbsoluteToleranceAdjustmentFactorRef() { return getOrRefRefNode("absoluteToleranceAdjustmentFactor").asText(); }
    public void setAbsoluteToleranceAdjustmentFactorValue(double value) { setOrRefValueNode("absoluteToleranceAdjustmentFactor", DoubleNode.valueOf(value)); }
    public void setAbsoluteToleranceAdjustmentFactorRef(String ref) { setOrRefRefNode("absoluteToleranceAdjustmentFactor", ref); }
    public boolean isAbsoluteToleranceAdjustmentFactorRef() { return isOrRefRef("absoluteToleranceAdjustmentFactor"); }
    public boolean isSetAbsoluteToleranceAdjustmentFactor() { return values.containsKey("absoluteToleranceAdjustmentFactor"); }
    public void unsetAbsoluteToleranceAdjustmentFactor() { values.remove("absoluteToleranceAdjustmentFactor"); orRefIsRef.remove("absoluteToleranceAdjustmentFactor"); }

    public double getToleranceForRootFinderValue() { return getOrRefValueNode("toleranceForRootFinder").asDouble(); }
    public String getToleranceForRootFinderRef() { return getOrRefRefNode("toleranceForRootFinder").asText(); }
    public void setToleranceForRootFinderValue(double value) { setOrRefValueNode("toleranceForRootFinder", DoubleNode.valueOf(value)); }
    public void setToleranceForRootFinderRef(String ref) { setOrRefRefNode("toleranceForRootFinder", ref); }
    public boolean isToleranceForRootFinderRef() { return isOrRefRef("toleranceForRootFinder"); }
    public boolean isSetToleranceForRootFinder() { return values.containsKey("toleranceForRootFinder"); }
    public void unsetToleranceForRootFinder() { values.remove("toleranceForRootFinder"); orRefIsRef.remove("toleranceForRootFinder"); }

    public double getInitialStepSizeValue() { return getOrRefValueNode("initialStepSize").asDouble(); }
    public String getInitialStepSizeRef() { return getOrRefRefNode("initialStepSize").asText(); }
    public void setInitialStepSizeValue(double value) { setOrRefValueNode("initialStepSize", DoubleNode.valueOf(value)); }
    public void setInitialStepSizeRef(String ref) { setOrRefRefNode("initialStepSize", ref); }
    public boolean isInitialStepSizeRef() { return isOrRefRef("initialStepSize"); }
    public boolean isSetInitialStepSize() { return values.containsKey("initialStepSize"); }
    public void unsetInitialStepSize() { values.remove("initialStepSize"); orRefIsRef.remove("initialStepSize"); }

    public double getMaxNumberOfStepsValue() { return getOrRefValueNode("maxNumberOfSteps").asDouble(); }
    public String getMaxNumberOfStepsRef() { return getOrRefRefNode("maxNumberOfSteps").asText(); }
    public void setMaxNumberOfStepsValue(double value) { setOrRefValueNode("maxNumberOfSteps", DoubleNode.valueOf(value)); }
    public void setMaxNumberOfStepsRef(String ref) { setOrRefRefNode("maxNumberOfSteps", ref); }
    public boolean isMaxNumberOfStepsRef() { return isOrRefRef("maxNumberOfSteps"); }
    public boolean isSetMaxNumberOfSteps() { return values.containsKey("maxNumberOfSteps"); }
    public void unsetMaxNumberOfSteps() { values.remove("maxNumberOfSteps"); orRefIsRef.remove("maxNumberOfSteps"); }

    public double getMaxInternalStepSizeValue() { return getOrRefValueNode("maxInternalStepSize").asDouble(); }
    public String getMaxInternalStepSizeRef() { return getOrRefRefNode("maxInternalStepSize").asText(); }
    public void setMaxInternalStepSizeValue(double value) { setOrRefValueNode("maxInternalStepSize", DoubleNode.valueOf(value)); }
    public void setMaxInternalStepSizeRef(String ref) { setOrRefRefNode("maxInternalStepSize", ref); }
    public boolean isMaxInternalStepSizeRef() { return isOrRefRef("maxInternalStepSize"); }
    public boolean isSetMaxInternalStepSize() { return values.containsKey("maxInternalStepSize"); }
    public void unsetMaxInternalStepSize() { values.remove("maxInternalStepSize"); orRefIsRef.remove("maxInternalStepSize"); }

    public double getMinInternalStepSizeValue() { return getOrRefValueNode("minInternalStepSize").asDouble(); }
    public String getMinInternalStepSizeRef() { return getOrRefRefNode("minInternalStepSize").asText(); }
    public void setMinInternalStepSizeValue(double value) { setOrRefValueNode("minInternalStepSize", DoubleNode.valueOf(value)); }
    public void setMinInternalStepSizeRef(String ref) { setOrRefRefNode("minInternalStepSize", ref); }
    public boolean isMinInternalStepSizeRef() { return isOrRefRef("minInternalStepSize"); }
    public boolean isSetMinInternalStepSize() { return values.containsKey("minInternalStepSize"); }
    public void unsetMinInternalStepSize() { values.remove("minInternalStepSize"); orRefIsRef.remove("minInternalStepSize"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("explicitODESimulation"));
        if (values.containsKey("relativeTolerance")) d.set("relativeTolerance", values.get("relativeTolerance"));
        if (values.containsKey("absoluteTolerance")) d.set("absoluteTolerance", values.get("absoluteTolerance"));
        if (values.containsKey("absoluteToleranceAdjustmentFactor")) d.set("absoluteToleranceAdjustmentFactor", values.get("absoluteToleranceAdjustmentFactor"));
        if (values.containsKey("toleranceForRootFinder")) d.set("toleranceForRootFinder", values.get("toleranceForRootFinder"));
        if (values.containsKey("initialStepSize")) d.set("initialStepSize", values.get("initialStepSize"));
        if (values.containsKey("maxNumberOfSteps")) d.set("maxNumberOfSteps", values.get("maxNumberOfSteps"));
        if (values.containsKey("maxInternalStepSize")) d.set("maxInternalStepSize", values.get("maxInternalStepSize"));
        if (values.containsKey("minInternalStepSize")) d.set("minInternalStepSize", values.get("minInternalStepSize"));
        if (values.containsKey("model")) d.set("model", values.get("model"));
        if (values.containsKey("independentVariable")) d.set("independentVariable", values.get("independentVariable"));
        if (values.containsKey("independentVariableInit")) d.set("independentVariableInit", values.get("independentVariableInit"));
        if (workingAlgorithms.size() > 0) { ArrayNode arr = d.putArray("workingAlgorithms"); for (SedBase item : workingAlgorithms.items()) arr.add(item.toJsonValue()); }
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

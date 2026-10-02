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

/** Generated from test-specsheets/tasks/OneStepStochasticSimulation/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class OneStepStochasticSimulation extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("independentStep", "NumberOrRef", false, "OneStepStochasticSimulation-0004", null, "OneStepStochasticSimulation-0000", null, null, null, null, null, false, null, null, "OneStepStochasticSimulation-0005", null, null),
        new FieldSpec("seed", "NumberOrRef", false, "AbstractStochasticSimulation-0001", null, "AbstractStochasticSimulation-0000", null, null, null, null, null, false, null, null, "AbstractStochasticSimulation-0002", null, null),
        new FieldSpec("timeDependentRelativeTolerance", "NumberOrRef", false, "AbstractStochasticSimulation-0003", null, "AbstractStochasticSimulation-0000", null, null, null, null, null, false, null, null, "AbstractStochasticSimulation-0004", null, null),
        new FieldSpec("variableStepSize", "BooleanOrRef", false, "AbstractStochasticSimulation-0005", null, "AbstractStochasticSimulation-0000", null, null, null, null, null, false, null, null, "AbstractStochasticSimulation-0006", null, null),
        new FieldSpec("minimumTimeStep", "NumberOrRef", false, "AbstractStochasticSimulation-0007", null, "AbstractStochasticSimulation-0000", null, null, null, null, null, false, null, null, "AbstractStochasticSimulation-0008", null, null),
        new FieldSpec("maximumTimeStep", "NumberOrRef", false, "AbstractStochasticSimulation-0009", null, "AbstractStochasticSimulation-0000", null, null, null, null, null, false, null, null, "AbstractStochasticSimulation-0010", null, null),
        new FieldSpec("nonNegative", "BooleanOrRef", false, "AbstractStochasticSimulation-0011", null, "AbstractStochasticSimulation-0000", null, null, null, null, null, false, null, null, "AbstractStochasticSimulation-0012", null, null),
        new FieldSpec("maxOutputRows", "IntegerOrRef", false, "AbstractStochasticSimulation-0013", null, "AbstractStochasticSimulation-0000", null, 0.0, null, null, null, false, null, null, "AbstractStochasticSimulation-0014", null, null),
        new FieldSpec("maxNumSteps", "IntegerOrRef", false, "AbstractStochasticSimulation-0015", null, "AbstractStochasticSimulation-0000", null, 0.0, null, null, null, false, null, null, "AbstractStochasticSimulation-0016", null, null),
        new FieldSpec("model", "SIdRef", false, "AbstractSimulation-0001", null, "AbstractSimulation-0000", null, null, null, null, null, false, null, null, null, null, "model"),
        new FieldSpec("independentVariable", "StringOrRef", false, "AbstractSimulation-0002", null, "AbstractSimulation-0000", null, null, null, null, null, false, null, null, "AbstractSimulation-0003", null, null),
        new FieldSpec("independentVariableInit", "NumberOrRef", false, "AbstractSimulation-0004", null, "AbstractSimulation-0000", null, null, null, null, null, false, null, null, "AbstractSimulation-0005", null, null),
        new FieldSpec("outputVariables", "ArrayOrRef", false, "AbstractSimulation-0006", null, "AbstractSimulation-0000", null, null, null, null, null, false, null, null, "AbstractSimulation-0007", "string", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("workingAlgorithms", "array", false, "AbstractSimulation-0008", null, "AbstractSimulation-0000", null, null, null, "WorkingAlgorithm", null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of();
    private final ListCollection<SedBase> workingAlgorithms = new ListCollection<>();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "oneStepStochastic"; }
    @Override public String typeRuleId() { return "OneStepStochasticSimulation-0006"; }
    @Override public String ownCatchall() { return "OneStepStochasticSimulation-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "oneStepStochastic"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"len(outputVariables)\"}, \"labels\": {\"source\": \"static\", \"expr\": \"outputVariables\"}, \"note\": \"a single point, not a series\"}]}, \"[id].model\": {\"type\": \"model\"}, \"[id].independentStep\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"1\"}, \"labels\": null}], \"note\": \"the actual elapsed step; if independentStep was given as input it equals that value, otherwise its value is generated by the simulation\"}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public double getIndependentStepValue() { return getOrRefValueNode("independentStep").asDouble(); }
    public String getIndependentStepRef() { return getOrRefRefNode("independentStep").asText(); }
    public void setIndependentStepValue(double value) { setOrRefValueNode("independentStep", DoubleNode.valueOf(value)); }
    public void setIndependentStepRef(String ref) { setOrRefRefNode("independentStep", ref); }
    public boolean isIndependentStepRef() { return isOrRefRef("independentStep"); }
    public boolean isSetIndependentStep() { return values.containsKey("independentStep"); }
    public void unsetIndependentStep() { values.remove("independentStep"); orRefIsRef.remove("independentStep"); }

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

    public boolean getVariableStepSizeValue() { return getOrRefValueNode("variableStepSize").asBoolean(); }
    public String getVariableStepSizeRef() { return getOrRefRefNode("variableStepSize").asText(); }
    public void setVariableStepSizeValue(boolean value) { setOrRefValueNode("variableStepSize", BooleanNode.valueOf(value)); }
    public void setVariableStepSizeRef(String ref) { setOrRefRefNode("variableStepSize", ref); }
    public boolean isVariableStepSizeRef() { return isOrRefRef("variableStepSize"); }
    public boolean isSetVariableStepSize() { return values.containsKey("variableStepSize"); }
    public void unsetVariableStepSize() { values.remove("variableStepSize"); orRefIsRef.remove("variableStepSize"); }

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

    public boolean getNonNegativeValue() { return getOrRefValueNode("nonNegative").asBoolean(); }
    public String getNonNegativeRef() { return getOrRefRefNode("nonNegative").asText(); }
    public void setNonNegativeValue(boolean value) { setOrRefValueNode("nonNegative", BooleanNode.valueOf(value)); }
    public void setNonNegativeRef(String ref) { setOrRefRefNode("nonNegative", ref); }
    public boolean isNonNegativeRef() { return isOrRefRef("nonNegative"); }
    public boolean isSetNonNegative() { return values.containsKey("nonNegative"); }
    public void unsetNonNegative() { values.remove("nonNegative"); orRefIsRef.remove("nonNegative"); }

    public long getMaxOutputRowsValue() { return getOrRefValueNode("maxOutputRows").asLong(); }
    public String getMaxOutputRowsRef() { return getOrRefRefNode("maxOutputRows").asText(); }
    public void setMaxOutputRowsValue(long value) { setOrRefValueNode("maxOutputRows", LongNode.valueOf(value)); }
    public void setMaxOutputRowsRef(String ref) { setOrRefRefNode("maxOutputRows", ref); }
    public boolean isMaxOutputRowsRef() { return isOrRefRef("maxOutputRows"); }
    public boolean isSetMaxOutputRows() { return values.containsKey("maxOutputRows"); }
    public void unsetMaxOutputRows() { values.remove("maxOutputRows"); orRefIsRef.remove("maxOutputRows"); }

    public long getMaxNumStepsValue() { return getOrRefValueNode("maxNumSteps").asLong(); }
    public String getMaxNumStepsRef() { return getOrRefRefNode("maxNumSteps").asText(); }
    public void setMaxNumStepsValue(long value) { setOrRefValueNode("maxNumSteps", LongNode.valueOf(value)); }
    public void setMaxNumStepsRef(String ref) { setOrRefRefNode("maxNumSteps", ref); }
    public boolean isMaxNumStepsRef() { return isOrRefRef("maxNumSteps"); }
    public boolean isSetMaxNumSteps() { return values.containsKey("maxNumSteps"); }
    public void unsetMaxNumSteps() { values.remove("maxNumSteps"); orRefIsRef.remove("maxNumSteps"); }

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

    public JsonNode getOutputVariablesValue() { return getOrRefValueNode("outputVariables"); }
    public String getOutputVariablesRef() { return getOrRefRefNode("outputVariables").asText(); }
    public void setOutputVariablesValue(JsonNode value) { setOrRefValueNode("outputVariables", value); }
    public void setOutputVariablesRef(String ref) { setOrRefRefNode("outputVariables", ref); }
    public boolean isOutputVariablesRef() { return isOrRefRef("outputVariables"); }
    public boolean isSetOutputVariables() { return values.containsKey("outputVariables"); }
    public void unsetOutputVariables() { values.remove("outputVariables"); orRefIsRef.remove("outputVariables"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

    public List<SedBase> getWorkingAlgorithms() { return workingAlgorithms.items(); }
    public void addWorkingAlgorithms(SedBase obj) { workingAlgorithms.add(obj); obj.attach(this, getDocument()); }
    public void insertWorkingAlgorithms(int index, SedBase obj) { workingAlgorithms.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeWorkingAlgorithms(int index) { workingAlgorithms.remove(index); }

    public List<SedBase> getTaskParameters() { return taskParameters.items(); }
    public void addTaskParameters(SedBase obj) { taskParameters.add(obj); obj.attach(this, getDocument()); }
    public void insertTaskParameters(int index, SedBase obj) { taskParameters.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeTaskParameters(int index) { taskParameters.remove(index); }

    public List<SedBase> getAnnotations() { return annotations.items(); }
    public void addAnnotations(SedBase obj) { annotations.add(obj); obj.attach(this, getDocument()); }
    public void insertAnnotations(int index, SedBase obj) { annotations.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeAnnotations(int index) { annotations.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        kids.addAll(workingAlgorithms.items());
        kids.addAll(taskParameters.items());
        kids.addAll(annotations.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : workingAlgorithms.items()) { out.add(new ChildLoc(item, "/workingAlgorithms/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "workingAlgorithms": return workingAlgorithms;
            case "taskParameters": return taskParameters;
            case "annotations": return annotations;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("oneStepStochastic"));
        if (values.containsKey("independentStep")) d.set("independentStep", values.get("independentStep"));
        if (values.containsKey("seed")) d.set("seed", values.get("seed"));
        if (values.containsKey("timeDependentRelativeTolerance")) d.set("timeDependentRelativeTolerance", values.get("timeDependentRelativeTolerance"));
        if (values.containsKey("variableStepSize")) d.set("variableStepSize", values.get("variableStepSize"));
        if (values.containsKey("minimumTimeStep")) d.set("minimumTimeStep", values.get("minimumTimeStep"));
        if (values.containsKey("maximumTimeStep")) d.set("maximumTimeStep", values.get("maximumTimeStep"));
        if (values.containsKey("nonNegative")) d.set("nonNegative", values.get("nonNegative"));
        if (values.containsKey("maxOutputRows")) d.set("maxOutputRows", values.get("maxOutputRows"));
        if (values.containsKey("maxNumSteps")) d.set("maxNumSteps", values.get("maxNumSteps"));
        if (values.containsKey("model")) d.set("model", values.get("model"));
        if (values.containsKey("independentVariable")) d.set("independentVariable", values.get("independentVariable"));
        if (values.containsKey("independentVariableInit")) d.set("independentVariableInit", values.get("independentVariableInit"));
        if (values.containsKey("outputVariables")) d.set("outputVariables", values.get("outputVariables"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (workingAlgorithms.size() > 0) { ArrayNode arr = d.putArray("workingAlgorithms"); for (SedBase item : workingAlgorithms.items()) arr.add(item.toJsonValue()); }
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

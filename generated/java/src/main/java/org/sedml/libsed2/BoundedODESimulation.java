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

/** Generated from test-specsheets/tasks/BoundedODESimulation/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class BoundedODESimulation extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("relativeTolerance", "NumberOrRef", false, "AbstractODESimulation-0001", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0002", null, null),
        new FieldSpec("absoluteTolerance", "NumberOrRef", false, "AbstractODESimulation-0003", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0004", null, null),
        new FieldSpec("absoluteToleranceVector", "ArrayOrRef", false, "AbstractODESimulation-0005", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0006", "number", null),
        new FieldSpec("absoluteToleranceAdjustmentFactor", "NumberOrRef", false, "AbstractODESimulation-0007", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0008", null, null),
        new FieldSpec("toleranceForRootFinder", "NumberOrRef", false, "AbstractODESimulation-0009", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0010", null, null),
        new FieldSpec("initialStepSize", "NumberOrRef", false, "AbstractODESimulation-0011", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0012", null, null),
        new FieldSpec("maxNumberOfSteps", "NumberOrRef", false, "AbstractODESimulation-0013", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0014", null, null),
        new FieldSpec("maxInternalSteps", "IntegerOrRef", false, "AbstractODESimulation-0015", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0016", null, null),
        new FieldSpec("maxInternalStepSize", "NumberOrRef", false, "AbstractODESimulation-0017", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0018", null, null),
        new FieldSpec("minInternalStepSize", "NumberOrRef", false, "AbstractODESimulation-0019", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0020", null, null),
        new FieldSpec("forcePhysicalCorrectness", "BooleanOrRef", false, "AbstractODESimulation-0021", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0022", null, null),
        new FieldSpec("integrateReducedModel", "BooleanOrRef", false, "AbstractODESimulation-0023", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0024", null, null),
        new FieldSpec("useReducedModel", "BooleanOrRef", false, "AbstractODESimulation-0025", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0026", null, null),
        new FieldSpec("useStiffSolver", "BooleanOrRef", false, "AbstractODESimulation-0027", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0028", null, null),
        new FieldSpec("maxBDForder", "IntegerOrRef", false, "AbstractODESimulation-0029", null, "AbstractODESimulation-0000", null, 0.0, null, null, null, false, null, null, "AbstractODESimulation-0030", null, null),
        new FieldSpec("maxAdamsOrder", "IntegerOrRef", false, "AbstractODESimulation-0031", null, "AbstractODESimulation-0000", null, 0.0, null, null, null, false, null, null, "AbstractODESimulation-0032", null, null),
        new FieldSpec("variableStepSize", "BooleanOrRef", false, "AbstractODESimulation-0033", null, "AbstractODESimulation-0000", null, null, null, null, null, false, null, null, "AbstractODESimulation-0034", null, null),
        new FieldSpec("maxOutputRows", "IntegerOrRef", false, "AbstractODESimulation-0035", null, "AbstractODESimulation-0000", null, 0.0, null, null, null, false, null, null, "AbstractODESimulation-0036", null, null),
        new FieldSpec("model", "SIdRef", false, "AbstractSimulation-0001", null, "AbstractSimulation-0000", null, null, null, null, null, false, null, null, null, null, "model"),
        new FieldSpec("independentVariable", "StringOrRef", false, "AbstractSimulation-0002", null, "AbstractSimulation-0000", null, null, null, null, null, false, null, null, "AbstractSimulation-0003", null, null),
        new FieldSpec("independentVariableInit", "NumberOrRef", false, "AbstractSimulation-0004", null, "AbstractSimulation-0000", null, null, null, null, null, false, null, null, "AbstractSimulation-0005", null, null),
        new FieldSpec("outputVariables", "ArrayOrRef", false, "AbstractSimulation-0006", null, "AbstractSimulation-0000", null, null, null, null, null, false, null, null, "AbstractSimulation-0007", "string", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("workingAlgorithms", "array", false, "AbstractSimulation-0008", null, "AbstractSimulation-0000", null, null, null, "WorkingAlgorithm", null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null),
        new FieldSpec("independentVariableSpan", "ref-class", true, "BoundedODESimulation-0005", "BoundedODESimulation-0004", "BoundedODESimulation-0000", null, null, null, "Span", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("independentVariableSpan");
    private final ListCollection<SedBase> workingAlgorithms = new ListCollection<>();
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();
    private SedBase independentVariableSpan;

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "boundedODESimulation"; }
    @Override public String typeRuleId() { return "BoundedODESimulation-0006"; }
    @Override public String ownCatchall() { return "BoundedODESimulation-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "boundedODESimulation"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"runtime\", \"note\": \"row count is chosen by the solver/simulator at run time under variable step size, not fixed by independentVariableSpan (only its start/end bound the range)\"}, \"labels\": null}, {\"size\": {\"source\": \"static\", \"expr\": \"1 + len(outputVariables)\"}, \"labels\": {\"source\": \"static\", \"expr\": \"[independentVariable] + outputVariables\"}}]}, \"[id].model\": {\"type\": \"model\"}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

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

    public JsonNode getAbsoluteToleranceVectorValue() { return getOrRefValueNode("absoluteToleranceVector"); }
    public String getAbsoluteToleranceVectorRef() { return getOrRefRefNode("absoluteToleranceVector").asText(); }
    public void setAbsoluteToleranceVectorValue(JsonNode value) { setOrRefValueNode("absoluteToleranceVector", value); }
    public void setAbsoluteToleranceVectorRef(String ref) { setOrRefRefNode("absoluteToleranceVector", ref); }
    public boolean isAbsoluteToleranceVectorRef() { return isOrRefRef("absoluteToleranceVector"); }
    public boolean isSetAbsoluteToleranceVector() { return values.containsKey("absoluteToleranceVector"); }
    public void unsetAbsoluteToleranceVector() { values.remove("absoluteToleranceVector"); orRefIsRef.remove("absoluteToleranceVector"); }

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

    public long getMaxInternalStepsValue() { return getOrRefValueNode("maxInternalSteps").asLong(); }
    public String getMaxInternalStepsRef() { return getOrRefRefNode("maxInternalSteps").asText(); }
    public void setMaxInternalStepsValue(long value) { setOrRefValueNode("maxInternalSteps", LongNode.valueOf(value)); }
    public void setMaxInternalStepsRef(String ref) { setOrRefRefNode("maxInternalSteps", ref); }
    public boolean isMaxInternalStepsRef() { return isOrRefRef("maxInternalSteps"); }
    public boolean isSetMaxInternalSteps() { return values.containsKey("maxInternalSteps"); }
    public void unsetMaxInternalSteps() { values.remove("maxInternalSteps"); orRefIsRef.remove("maxInternalSteps"); }

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

    public boolean getForcePhysicalCorrectnessValue() { return getOrRefValueNode("forcePhysicalCorrectness").asBoolean(); }
    public String getForcePhysicalCorrectnessRef() { return getOrRefRefNode("forcePhysicalCorrectness").asText(); }
    public void setForcePhysicalCorrectnessValue(boolean value) { setOrRefValueNode("forcePhysicalCorrectness", BooleanNode.valueOf(value)); }
    public void setForcePhysicalCorrectnessRef(String ref) { setOrRefRefNode("forcePhysicalCorrectness", ref); }
    public boolean isForcePhysicalCorrectnessRef() { return isOrRefRef("forcePhysicalCorrectness"); }
    public boolean isSetForcePhysicalCorrectness() { return values.containsKey("forcePhysicalCorrectness"); }
    public void unsetForcePhysicalCorrectness() { values.remove("forcePhysicalCorrectness"); orRefIsRef.remove("forcePhysicalCorrectness"); }

    public boolean getIntegrateReducedModelValue() { return getOrRefValueNode("integrateReducedModel").asBoolean(); }
    public String getIntegrateReducedModelRef() { return getOrRefRefNode("integrateReducedModel").asText(); }
    public void setIntegrateReducedModelValue(boolean value) { setOrRefValueNode("integrateReducedModel", BooleanNode.valueOf(value)); }
    public void setIntegrateReducedModelRef(String ref) { setOrRefRefNode("integrateReducedModel", ref); }
    public boolean isIntegrateReducedModelRef() { return isOrRefRef("integrateReducedModel"); }
    public boolean isSetIntegrateReducedModel() { return values.containsKey("integrateReducedModel"); }
    public void unsetIntegrateReducedModel() { values.remove("integrateReducedModel"); orRefIsRef.remove("integrateReducedModel"); }

    public boolean getUseReducedModelValue() { return getOrRefValueNode("useReducedModel").asBoolean(); }
    public String getUseReducedModelRef() { return getOrRefRefNode("useReducedModel").asText(); }
    public void setUseReducedModelValue(boolean value) { setOrRefValueNode("useReducedModel", BooleanNode.valueOf(value)); }
    public void setUseReducedModelRef(String ref) { setOrRefRefNode("useReducedModel", ref); }
    public boolean isUseReducedModelRef() { return isOrRefRef("useReducedModel"); }
    public boolean isSetUseReducedModel() { return values.containsKey("useReducedModel"); }
    public void unsetUseReducedModel() { values.remove("useReducedModel"); orRefIsRef.remove("useReducedModel"); }

    public boolean getUseStiffSolverValue() { return getOrRefValueNode("useStiffSolver").asBoolean(); }
    public String getUseStiffSolverRef() { return getOrRefRefNode("useStiffSolver").asText(); }
    public void setUseStiffSolverValue(boolean value) { setOrRefValueNode("useStiffSolver", BooleanNode.valueOf(value)); }
    public void setUseStiffSolverRef(String ref) { setOrRefRefNode("useStiffSolver", ref); }
    public boolean isUseStiffSolverRef() { return isOrRefRef("useStiffSolver"); }
    public boolean isSetUseStiffSolver() { return values.containsKey("useStiffSolver"); }
    public void unsetUseStiffSolver() { values.remove("useStiffSolver"); orRefIsRef.remove("useStiffSolver"); }

    public long getMaxBDForderValue() { return getOrRefValueNode("maxBDForder").asLong(); }
    public String getMaxBDForderRef() { return getOrRefRefNode("maxBDForder").asText(); }
    public void setMaxBDForderValue(long value) { setOrRefValueNode("maxBDForder", LongNode.valueOf(value)); }
    public void setMaxBDForderRef(String ref) { setOrRefRefNode("maxBDForder", ref); }
    public boolean isMaxBDForderRef() { return isOrRefRef("maxBDForder"); }
    public boolean isSetMaxBDForder() { return values.containsKey("maxBDForder"); }
    public void unsetMaxBDForder() { values.remove("maxBDForder"); orRefIsRef.remove("maxBDForder"); }

    public long getMaxAdamsOrderValue() { return getOrRefValueNode("maxAdamsOrder").asLong(); }
    public String getMaxAdamsOrderRef() { return getOrRefRefNode("maxAdamsOrder").asText(); }
    public void setMaxAdamsOrderValue(long value) { setOrRefValueNode("maxAdamsOrder", LongNode.valueOf(value)); }
    public void setMaxAdamsOrderRef(String ref) { setOrRefRefNode("maxAdamsOrder", ref); }
    public boolean isMaxAdamsOrderRef() { return isOrRefRef("maxAdamsOrder"); }
    public boolean isSetMaxAdamsOrder() { return values.containsKey("maxAdamsOrder"); }
    public void unsetMaxAdamsOrder() { values.remove("maxAdamsOrder"); orRefIsRef.remove("maxAdamsOrder"); }

    public boolean getVariableStepSizeValue() { return getOrRefValueNode("variableStepSize").asBoolean(); }
    public String getVariableStepSizeRef() { return getOrRefRefNode("variableStepSize").asText(); }
    public void setVariableStepSizeValue(boolean value) { setOrRefValueNode("variableStepSize", BooleanNode.valueOf(value)); }
    public void setVariableStepSizeRef(String ref) { setOrRefRefNode("variableStepSize", ref); }
    public boolean isVariableStepSizeRef() { return isOrRefRef("variableStepSize"); }
    public boolean isSetVariableStepSize() { return values.containsKey("variableStepSize"); }
    public void unsetVariableStepSize() { values.remove("variableStepSize"); orRefIsRef.remove("variableStepSize"); }

    public long getMaxOutputRowsValue() { return getOrRefValueNode("maxOutputRows").asLong(); }
    public String getMaxOutputRowsRef() { return getOrRefRefNode("maxOutputRows").asText(); }
    public void setMaxOutputRowsValue(long value) { setOrRefValueNode("maxOutputRows", LongNode.valueOf(value)); }
    public void setMaxOutputRowsRef(String ref) { setOrRefRefNode("maxOutputRows", ref); }
    public boolean isMaxOutputRowsRef() { return isOrRefRef("maxOutputRows"); }
    public boolean isSetMaxOutputRows() { return values.containsKey("maxOutputRows"); }
    public void unsetMaxOutputRows() { values.remove("maxOutputRows"); orRefIsRef.remove("maxOutputRows"); }

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

    public SedBase getIndependentVariableSpan() { if (independentVariableSpan == null) throw new ApiError("independentVariableSpan" + " is not set"); return independentVariableSpan; }
    public void setIndependentVariableSpan(SedBase obj) { independentVariableSpan = obj; obj.attach(this, getDocument()); }
    public boolean isSetIndependentVariableSpan() { return independentVariableSpan != null; }
    public void unsetIndependentVariableSpan() { independentVariableSpan = null; }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        kids.addAll(workingAlgorithms.items());
        kids.addAll(taskParameters.items());
        kids.addAll(annotations.items());
        if (independentVariableSpan != null) kids.add(independentVariableSpan);
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : workingAlgorithms.items()) { out.add(new ChildLoc(item, "/workingAlgorithms/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        if (independentVariableSpan != null) out.add(new ChildLoc(independentVariableSpan, "/independentVariableSpan"));
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
    protected void setChildField(String fieldName, SedBase child) {
        switch (fieldName) {
            case "independentVariableSpan": independentVariableSpan = child; return;
            default: super.setChildField(fieldName, child);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("boundedODESimulation"));
        if (values.containsKey("relativeTolerance")) d.set("relativeTolerance", values.get("relativeTolerance"));
        if (values.containsKey("absoluteTolerance")) d.set("absoluteTolerance", values.get("absoluteTolerance"));
        if (values.containsKey("absoluteToleranceVector")) d.set("absoluteToleranceVector", values.get("absoluteToleranceVector"));
        if (values.containsKey("absoluteToleranceAdjustmentFactor")) d.set("absoluteToleranceAdjustmentFactor", values.get("absoluteToleranceAdjustmentFactor"));
        if (values.containsKey("toleranceForRootFinder")) d.set("toleranceForRootFinder", values.get("toleranceForRootFinder"));
        if (values.containsKey("initialStepSize")) d.set("initialStepSize", values.get("initialStepSize"));
        if (values.containsKey("maxNumberOfSteps")) d.set("maxNumberOfSteps", values.get("maxNumberOfSteps"));
        if (values.containsKey("maxInternalSteps")) d.set("maxInternalSteps", values.get("maxInternalSteps"));
        if (values.containsKey("maxInternalStepSize")) d.set("maxInternalStepSize", values.get("maxInternalStepSize"));
        if (values.containsKey("minInternalStepSize")) d.set("minInternalStepSize", values.get("minInternalStepSize"));
        if (values.containsKey("forcePhysicalCorrectness")) d.set("forcePhysicalCorrectness", values.get("forcePhysicalCorrectness"));
        if (values.containsKey("integrateReducedModel")) d.set("integrateReducedModel", values.get("integrateReducedModel"));
        if (values.containsKey("useReducedModel")) d.set("useReducedModel", values.get("useReducedModel"));
        if (values.containsKey("useStiffSolver")) d.set("useStiffSolver", values.get("useStiffSolver"));
        if (values.containsKey("maxBDForder")) d.set("maxBDForder", values.get("maxBDForder"));
        if (values.containsKey("maxAdamsOrder")) d.set("maxAdamsOrder", values.get("maxAdamsOrder"));
        if (values.containsKey("variableStepSize")) d.set("variableStepSize", values.get("variableStepSize"));
        if (values.containsKey("maxOutputRows")) d.set("maxOutputRows", values.get("maxOutputRows"));
        if (values.containsKey("model")) d.set("model", values.get("model"));
        if (values.containsKey("independentVariable")) d.set("independentVariable", values.get("independentVariable"));
        if (values.containsKey("independentVariableInit")) d.set("independentVariableInit", values.get("independentVariableInit"));
        if (values.containsKey("outputVariables")) d.set("outputVariables", values.get("outputVariables"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (workingAlgorithms.size() > 0) { ArrayNode arr = d.putArray("workingAlgorithms"); for (SedBase item : workingAlgorithms.items()) arr.add(item.toJsonValue()); }
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        if (independentVariableSpan != null) d.set("independentVariableSpan", independentVariableSpan.toJsonValue());
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

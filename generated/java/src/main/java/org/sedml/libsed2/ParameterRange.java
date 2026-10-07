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

/** Generated from specsheets/tasks/ParameterRange/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class ParameterRange extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("modelElement", "StringOrRef", true, "ParameterRange-0002", "ParameterRange-0001", "ParameterRange-0000", null, null, null, null, null, false, null, null, "ParameterRange-0003", null, null),
        new FieldSpec("start", "NumberOrRef", false, "NumericRange-0001", null, "NumericRange-0000", null, null, null, null, null, false, null, null, "NumericRange-0002", null, null),
        new FieldSpec("end", "NumberOrRef", false, "NumericRange-0003", null, "NumericRange-0000", null, null, null, null, null, false, null, null, "NumericRange-0004", null, null),
        new FieldSpec("interval", "NumberOrRef", false, "NumericRange-0005", null, "NumericRange-0000", null, 0.0, null, null, null, false, null, null, "NumericRange-0006", null, null),
        new FieldSpec("numberOfSteps", "IntegerOrRef", false, "NumericRange-0007", null, "NumericRange-0000", null, 0.0, null, null, null, false, null, null, "NumericRange-0008", null, null),
        new FieldSpec("scale", "StringOrRef", false, "NumericRange-0009", null, "NumericRange-0000", null, null, null, null, null, false, null, List.of("linear", "log10"), "NumericRange-0010", null, null),
        new FieldSpec("values", "ArrayOrRef", false, "NumericRange-0011", null, "NumericRange-0000", null, null, null, null, null, false, null, null, "NumericRange-0012", "number", null),
        new FieldSpec("values", "ArrayOrRef", false, "Range-0001", null, "Range-0000", null, null, null, null, null, false, null, null, "Range-0002", "any", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("modelElement");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "parameterRange"; }
    @Override public String typeRuleId() { return "ParameterRange-0016"; }
    @Override public String ownCatchall() { return "ParameterRange-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "parameterRange"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"type\": \"annotatedData\", \"dimensions\": [{\"size\": {\"source\": \"static\", \"expr\": \"len(values) if provided(values) else numberOfSteps + 1\", \"note\": \"same derivation as NumericRange, inherited via NumericRangeCommon\"}, \"labels\": null}]}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public String getModelElementValue() { return getOrRefValueNode("modelElement").asText(); }
    public String getModelElementRef() { return getOrRefRefNode("modelElement").asText(); }
    public void setModelElementValue(String value) { setOrRefValueNode("modelElement", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setModelElementRef(String ref) { setOrRefRefNode("modelElement", ref); }
    public boolean isModelElementRef() { return isOrRefRef("modelElement"); }
    public boolean isSetModelElement() { return values.containsKey("modelElement"); }
    public void unsetModelElement() { values.remove("modelElement"); orRefIsRef.remove("modelElement"); }

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

    public double getIntervalValue() { return getOrRefValueNode("interval").asDouble(); }
    public String getIntervalRef() { return getOrRefRefNode("interval").asText(); }
    public void setIntervalValue(double value) { setOrRefValueNode("interval", DoubleNode.valueOf(value)); }
    public void setIntervalRef(String ref) { setOrRefRefNode("interval", ref); }
    public boolean isIntervalRef() { return isOrRefRef("interval"); }
    public boolean isSetInterval() { return values.containsKey("interval"); }
    public void unsetInterval() { values.remove("interval"); orRefIsRef.remove("interval"); }

    public long getNumberOfStepsValue() { return getOrRefValueNode("numberOfSteps").asLong(); }
    public String getNumberOfStepsRef() { return getOrRefRefNode("numberOfSteps").asText(); }
    public void setNumberOfStepsValue(long value) { setOrRefValueNode("numberOfSteps", LongNode.valueOf(value)); }
    public void setNumberOfStepsRef(String ref) { setOrRefRefNode("numberOfSteps", ref); }
    public boolean isNumberOfStepsRef() { return isOrRefRef("numberOfSteps"); }
    public boolean isSetNumberOfSteps() { return values.containsKey("numberOfSteps"); }
    public void unsetNumberOfSteps() { values.remove("numberOfSteps"); orRefIsRef.remove("numberOfSteps"); }

    public String getScaleValue() { return getOrRefValueNode("scale").asText(); }
    public String getScaleRef() { return getOrRefRefNode("scale").asText(); }
    public void setScaleValue(String value) { setOrRefValueNode("scale", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setScaleRef(String ref) { setOrRefRefNode("scale", ref); }
    public boolean isScaleRef() { return isOrRefRef("scale"); }
    public boolean isSetScale() { return values.containsKey("scale"); }
    public void unsetScale() { values.remove("scale"); orRefIsRef.remove("scale"); }

    public JsonNode getValuesValue() { return getOrRefValueNode("values"); }
    public String getValuesRef() { return getOrRefRefNode("values").asText(); }
    public void setValuesValue(JsonNode value) { setOrRefValueNode("values", value); }
    public void setValuesRef(String ref) { setOrRefRefNode("values", ref); }
    public boolean isValuesRef() { return isOrRefRef("values"); }
    public boolean isSetValues() { return values.containsKey("values"); }
    public void unsetValues() { values.remove("values"); orRefIsRef.remove("values"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

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
        kids.addAll(taskParameters.items());
        kids.addAll(annotations.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : taskParameters.items()) { out.add(new ChildLoc(item, "/taskParameters/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("parameterRange"));
        if (values.containsKey("modelElement")) d.set("modelElement", values.get("modelElement"));
        if (values.containsKey("start")) d.set("start", values.get("start"));
        if (values.containsKey("end")) d.set("end", values.get("end"));
        if (values.containsKey("interval")) d.set("interval", values.get("interval"));
        if (values.containsKey("numberOfSteps")) d.set("numberOfSteps", values.get("numberOfSteps"));
        if (values.containsKey("scale")) d.set("scale", values.get("scale"));
        if (values.containsKey("values")) d.set("values", values.get("values"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

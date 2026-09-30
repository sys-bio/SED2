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

/** Generated from test-specsheets/tasks/DrawFromDistribution/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class DrawFromDistribution extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("distribution", "StringOrRef", true, "DrawFromDistribution-0008", "DrawFromDistribution-0007", "DrawFromDistribution-0000", null, null, null, null, null, false, null, List.of("http://www.sbml.org/sbml/symbols/distrib/normal", "http://www.sbml.org/sbml/symbols/distrib/uniform", "http://www.sbml.org/sbml/symbols/distrib/bernoulli", "http://www.sbml.org/sbml/symbols/distrib/binomial", "http://www.sbml.org/sbml/symbols/distrib/cauchy", "http://www.sbml.org/sbml/symbols/distrib/chisquare", "http://www.sbml.org/sbml/symbols/distrib/exponential", "http://www.sbml.org/sbml/symbols/distrib/gamma", "http://www.sbml.org/sbml/symbols/distrib/laplace", "http://www.sbml.org/sbml/symbols/distrib/lognormal", "http://www.sbml.org/sbml/symbols/distrib/poisson", "http://www.sbml.org/sbml/symbols/distrib/rayleigh"), "DrawFromDistribution-0009", null, null),
        new FieldSpec("outputPersistent", "BooleanOrRef", false, "DrawFromDistribution-0004", null, "DrawFromDistribution-0000", null, null, null, null, null, false, null, null, "DrawFromDistribution-0005", null, null),
        new FieldSpec("arguments", "ArrayOrRef", true, "DrawFromDistribution-0002", "DrawFromDistribution-0001", "DrawFromDistribution-0000", null, null, null, null, null, false, null, null, "DrawFromDistribution-0003", "any", null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("taskParameters", "array", false, "AbstractTask-0001", null, "AbstractTask-0000", null, null, null, "TaskParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("distribution", "arguments");
    private final ListCollection<SedBase> taskParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "drawFromDistribution"; }
    @Override public String typeRuleId() { return "DrawFromDistribution-0006"; }
    @Override public String ownCatchall() { return "DrawFromDistribution-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "drawFromDistribution"; }
    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson("{\"outputs\": {\"[id]\": {\"valid\": true, \"type\": \"annotatedData\", \"dimensions\": [], \"note\": \"currently always a single scalar value (0-D), indexed historically as [id][0]; the type is multidimensional AnnotatedData to leave room for future correlated multi-value draws (shape of that future case is not yet designed - see core-spec.md Section 10)\"}, \"[id].model\": {\"valid\": false}, \"[id].strings\": {\"valid\": false}}}");
    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }

    public String getDistributionValue() { return getOrRefValueNode("distribution").asText(); }
    public String getDistributionRef() { return getOrRefRefNode("distribution").asText(); }
    public void setDistributionValue(String value) { setOrRefValueNode("distribution", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setDistributionRef(String ref) { setOrRefRefNode("distribution", ref); }
    public boolean isDistributionRef() { return isOrRefRef("distribution"); }
    public boolean isSetDistribution() { return values.containsKey("distribution"); }
    public void unsetDistribution() { values.remove("distribution"); orRefIsRef.remove("distribution"); }

    public boolean getOutputPersistentValue() { return getOrRefValueNode("outputPersistent").asBoolean(); }
    public String getOutputPersistentRef() { return getOrRefRefNode("outputPersistent").asText(); }
    public void setOutputPersistentValue(boolean value) { setOrRefValueNode("outputPersistent", BooleanNode.valueOf(value)); }
    public void setOutputPersistentRef(String ref) { setOrRefRefNode("outputPersistent", ref); }
    public boolean isOutputPersistentRef() { return isOrRefRef("outputPersistent"); }
    public boolean isSetOutputPersistent() { return values.containsKey("outputPersistent"); }
    public void unsetOutputPersistent() { values.remove("outputPersistent"); orRefIsRef.remove("outputPersistent"); }

    public JsonNode getArgumentsValue() { return getOrRefValueNode("arguments"); }
    public String getArgumentsRef() { return getOrRefRefNode("arguments").asText(); }
    public void setArgumentsValue(JsonNode value) { setOrRefValueNode("arguments", value); }
    public void setArgumentsRef(String ref) { setOrRefRefNode("arguments", ref); }
    public boolean isArgumentsRef() { return isOrRefRef("arguments"); }
    public boolean isSetArguments() { return values.containsKey("arguments"); }
    public void unsetArguments() { values.remove("arguments"); orRefIsRef.remove("arguments"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("drawFromDistribution"));
        if (values.containsKey("distribution")) d.set("distribution", values.get("distribution"));
        if (values.containsKey("outputPersistent")) d.set("outputPersistent", values.get("outputPersistent"));
        if (values.containsKey("arguments")) d.set("arguments", values.get("arguments"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (taskParameters.size() > 0) { ArrayNode arr = d.putArray("taskParameters"); for (SedBase item : taskParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

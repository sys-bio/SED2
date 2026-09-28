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

/** Generated from test-specsheets/outputs/Report/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Report extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("data", "SIdRef", true, "Report-0002", "Report-0001", "Report-0000", null, null, null, null, null),
        new FieldSpec("outputParameters", "array", false, "AbstractOutput-0001", null, "AbstractOutput-0000", null, null, null, "OutputParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("data");
    private final ListCollection<SedBase> outputParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "report"; }
    @Override public String typeRuleId() { return "Report-0003"; }
    @Override public String ownCatchall() { return "Report-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "report"; }

    public String getData() { if (!values.containsKey("data")) throw new ApiError("data" + " is not set"); return values.get("data").asText(); }
    public void setData(String value) { values.put("data", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetData() { return values.containsKey("data"); }
    public void unsetData() { values.remove("data"); }

    public List<SedBase> getOutputParameters() { return outputParameters.items(); }
    public void addOutputParameters(SedBase obj) { outputParameters.add(obj); obj.attach(this, getDocument()); }
    public void insertOutputParameters(int index, SedBase obj) { outputParameters.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeOutputParameters(int index) { outputParameters.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        kids.addAll(outputParameters.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : outputParameters.items()) { out.add(new ChildLoc(item, "/outputParameters/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "outputParameters": return outputParameters;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("report"));
        if (values.containsKey("data")) d.set("data", values.get("data"));
        if (outputParameters.size() > 0) { ArrayNode arr = d.putArray("outputParameters"); for (SedBase item : outputParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

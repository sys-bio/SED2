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

/** Generated from test-specsheets/auxiliary/LoopVariable/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class LoopVariable extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("subsequentValues", "SIdRef", true, "LoopVariable-0003", "LoopVariable-0002", "LoopVariable-0000", null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("initialValue", "subsequentValues");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "LoopVariable-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }

    public String getSubsequentValues() { if (!values.containsKey("subsequentValues")) throw new ApiError("subsequentValues" + " is not set"); return values.get("subsequentValues").asText(); }
    public void setSubsequentValues(String value) { values.put("subsequentValues", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetSubsequentValues() { return values.containsKey("subsequentValues"); }
    public void unsetSubsequentValues() { values.remove("subsequentValues"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        if (values.containsKey("subsequentValues")) d.set("subsequentValues", values.get("subsequentValues"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

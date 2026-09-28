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

/** Generated from test-specsheets/tasks/AcmeWidget/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class AcmeWidget extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("acme@acmeLevel", "NumberOrRef", true, null, "acme-AcmeWidget-0001", "AcmeWidget-0000", null, null, null, null, null),
        new FieldSpec("label", "StringOrRef", false, "AbstractWidget-0001", null, "AbstractWidget-0000", null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("acme@acmeLevel");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "acme@acmeWidget"; }
    @Override public String typeRuleId() { return "acme-AcmeWidget-0002"; }
    @Override public String ownCatchall() { return "acme-AcmeWidget-0000"; }
    @Override public String nameRuleId() { return "TestBase-0001"; }
    @Override public String descRuleId() { return null; }
    @Override public String baseCatchall() { return "TestBase-0000"; }
    public String getType() { return "acme@acmeWidget"; }

    public double getAcmeAcmeLevelValue() { return getOrRefValueNode("acme@acmeLevel").asDouble(); }
    public String getAcmeAcmeLevelRef() { return getOrRefRefNode("acme@acmeLevel").asText(); }
    public void setAcmeAcmeLevelValue(double value) { setOrRefValueNode("acme@acmeLevel", DoubleNode.valueOf(value)); }
    public void setAcmeAcmeLevelRef(String ref) { setOrRefRefNode("acme@acmeLevel", ref); }
    public boolean isAcmeAcmeLevelRef() { return isOrRefRef("acme@acmeLevel"); }
    public boolean isSetAcmeAcmeLevel() { return values.containsKey("acme@acmeLevel"); }
    public void unsetAcmeAcmeLevel() { values.remove("acme@acmeLevel"); orRefIsRef.remove("acme@acmeLevel"); }

    public String getLabelValue() { return getOrRefValueNode("label").asText(); }
    public String getLabelRef() { return getOrRefRefNode("label").asText(); }
    public void setLabelValue(String value) { setOrRefValueNode("label", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setLabelRef(String ref) { setOrRefRefNode("label", ref); }
    public boolean isLabelRef() { return isOrRefRef("label"); }
    public boolean isSetLabel() { return values.containsKey("label"); }
    public void unsetLabel() { values.remove("label"); orRefIsRef.remove("label"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("acme@acmeWidget"));
        if (values.containsKey("acme@acmeLevel")) d.set("acme@acmeLevel", values.get("acme@acmeLevel"));
        if (values.containsKey("label")) d.set("label", values.get("label"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

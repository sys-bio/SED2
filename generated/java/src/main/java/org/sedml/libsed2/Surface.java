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

/** Generated from test-specsheets/outputs/Surface/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Surface extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("surfaceType", "StringOrRef", true, "Surface-0002", "Surface-0001", "Surface-0000", null, null, null, null, null),
        new FieldSpec("x", "SIdRef", true, "Surface-0005", "Surface-0004", "Surface-0000", null, null, null, null, null),
        new FieldSpec("y", "SIdRef", true, "Surface-0007", "Surface-0006", "Surface-0000", null, null, null, null, null),
        new FieldSpec("z", "SIdRef", true, "Surface-0009", "Surface-0008", "Surface-0000", null, null, null, null, null),
        new FieldSpec("style", "SIdRef", false, "Surface-0010", null, "Surface-0000", null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("surfaceType", "x", "y", "z");

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "Surface-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }

    public String getSurfaceTypeValue() { return getOrRefValueNode("surfaceType").asText(); }
    public String getSurfaceTypeRef() { return getOrRefRefNode("surfaceType").asText(); }
    public void setSurfaceTypeValue(String value) { setOrRefValueNode("surfaceType", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setSurfaceTypeRef(String ref) { setOrRefRefNode("surfaceType", ref); }
    public boolean isSurfaceTypeRef() { return isOrRefRef("surfaceType"); }
    public boolean isSetSurfaceType() { return values.containsKey("surfaceType"); }
    public void unsetSurfaceType() { values.remove("surfaceType"); orRefIsRef.remove("surfaceType"); }

    public String getX() { if (!values.containsKey("x")) throw new ApiError("x" + " is not set"); return values.get("x").asText(); }
    public void setX(String value) { values.put("x", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetX() { return values.containsKey("x"); }
    public void unsetX() { values.remove("x"); }

    public String getY() { if (!values.containsKey("y")) throw new ApiError("y" + " is not set"); return values.get("y").asText(); }
    public void setY(String value) { values.put("y", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetY() { return values.containsKey("y"); }
    public void unsetY() { values.remove("y"); }

    public String getZ() { if (!values.containsKey("z")) throw new ApiError("z" + " is not set"); return values.get("z").asText(); }
    public void setZ(String value) { values.put("z", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetZ() { return values.containsKey("z"); }
    public void unsetZ() { values.remove("z"); }

    public String getStyle() { if (!values.containsKey("style")) throw new ApiError("style" + " is not set"); return values.get("style").asText(); }
    public void setStyle(String value) { values.put("style", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetStyle() { return values.containsKey("style"); }
    public void unsetStyle() { values.remove("style"); }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        if (values.containsKey("surfaceType")) d.set("surfaceType", values.get("surfaceType"));
        if (values.containsKey("x")) d.set("x", values.get("x"));
        if (values.containsKey("y")) d.set("y", values.get("y"));
        if (values.containsKey("z")) d.set("z", values.get("z"));
        if (values.containsKey("style")) d.set("style", values.get("style"));
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

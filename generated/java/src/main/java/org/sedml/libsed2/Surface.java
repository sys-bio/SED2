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

/** Generated from test-specsheets/outputs/Surface/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Surface extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("surfaceType", "StringOrRef", true, "Surface-0002", "Surface-0001", "Surface-0000", null, null, null, null, null),
        new FieldSpec("x", "SIdRef", true, "Surface-0005", "Surface-0004", "Surface-0000", null, null, null, null, null),
        new FieldSpec("y", "SIdRef", true, "Surface-0007", "Surface-0006", "Surface-0000", null, null, null, null, null),
        new FieldSpec("z", "SIdRef", true, "Surface-0009", "Surface-0008", "Surface-0000", null, null, null, null, null),
        new FieldSpec("style", "SIdRef", false, "Surface-0010", null, "Surface-0000", null, null, null, null, null),
        new FieldSpec("order", "IntegerOrRef", false, "Surface-0011", null, "Surface-0000", 0.0, null, null, null, null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("surfaceType", "x", "y", "z");
    private final ListCollection<SedBase> annotations = new ListCollection<>();

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

    public long getOrderValue() { return getOrRefValueNode("order").asLong(); }
    public String getOrderRef() { return getOrRefRefNode("order").asText(); }
    public void setOrderValue(long value) { setOrRefValueNode("order", LongNode.valueOf(value)); }
    public void setOrderRef(String ref) { setOrRefRefNode("order", ref); }
    public boolean isOrderRef() { return isOrRefRef("order"); }
    public boolean isSetOrder() { return values.containsKey("order"); }
    public void unsetOrder() { values.remove("order"); orRefIsRef.remove("order"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

    public List<SedBase> getAnnotations() { return annotations.items(); }
    public void addAnnotations(SedBase obj) { annotations.add(obj); obj.attach(this, getDocument()); }
    public void insertAnnotations(int index, SedBase obj) { annotations.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeAnnotations(int index) { annotations.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        kids.addAll(annotations.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "annotations": return annotations;
            default: return super.getListCollection(fieldName);
        }
    }

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
        if (values.containsKey("order")) d.set("order", values.get("order"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

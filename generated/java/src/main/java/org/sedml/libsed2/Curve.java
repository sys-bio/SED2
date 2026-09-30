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

/** Generated from test-specsheets/auxiliary/Curve/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Curve extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("curveType", "StringOrRef", true, "Curve-0002", "Curve-0001", "Curve-0000", null, null, null, null, null, false, null, List.of("points", "bar", "barStacked", "horizontalBar", "horizontalBarStacked", "shadedArea"), "Curve-0003", null, null),
        new FieldSpec("y", "SIdRef", true, "Curve-0005", "Curve-0004", "Curve-0000", null, null, null, null, null, false, null, null, null, null, "annotatedData"),
        new FieldSpec("xErrorUpper", "SIdRef", false, "Curve-0006", null, "Curve-0000", null, null, null, null, null, false, null, null, null, null, "annotatedData"),
        new FieldSpec("xErrorLower", "SIdRef", false, "Curve-0007", null, "Curve-0000", null, null, null, null, null, false, null, null, null, null, "annotatedData"),
        new FieldSpec("yErrorUpper", "SIdRef", false, "Curve-0008", null, "Curve-0000", null, null, null, null, null, false, null, null, null, null, "annotatedData"),
        new FieldSpec("yErrorLower", "SIdRef", false, "Curve-0009", null, "Curve-0000", null, null, null, null, null, false, null, null, null, null, "annotatedData"),
        new FieldSpec("yFrom", "SIdRef", false, "Curve-0010", null, "Curve-0000", null, null, null, null, null, false, null, null, null, null, "annotatedData"),
        new FieldSpec("yTo", "SIdRef", false, "Curve-0011", null, "Curve-0000", null, null, null, null, null, false, null, null, null, null, "annotatedData"),
        new FieldSpec("x", "SIdRef", true, "AbstractCurve-0002", "AbstractCurve-0001", "AbstractCurve-0000", null, null, null, null, null, false, null, null, null, null, "annotatedData"),
        new FieldSpec("order", "IntegerOrRef", false, "AbstractCurve-0003", null, "AbstractCurve-0000", 0.0, null, null, null, null, false, null, null, "AbstractCurve-0004", null, null),
        new FieldSpec("style", "SIdRef", false, "AbstractCurve-0005", null, "AbstractCurve-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("yAxis", "StringOrRef", false, "AbstractCurve-0006", null, "AbstractCurve-0000", null, null, null, null, null, false, null, List.of("right", "left"), "AbstractCurve-0007", null, null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("curveType", "y", "x");
    private final ListCollection<SedBase> annotations = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "curve"; }
    @Override public String typeRuleId() { return "Curve-0012"; }
    @Override public String ownCatchall() { return "Curve-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "curve"; }

    public String getCurveTypeValue() { return getOrRefValueNode("curveType").asText(); }
    public String getCurveTypeRef() { return getOrRefRefNode("curveType").asText(); }
    public void setCurveTypeValue(String value) { setOrRefValueNode("curveType", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setCurveTypeRef(String ref) { setOrRefRefNode("curveType", ref); }
    public boolean isCurveTypeRef() { return isOrRefRef("curveType"); }
    public boolean isSetCurveType() { return values.containsKey("curveType"); }
    public void unsetCurveType() { values.remove("curveType"); orRefIsRef.remove("curveType"); }

    public String getY() { if (!values.containsKey("y")) throw new ApiError("y" + " is not set"); return values.get("y").asText(); }
    public void setY(String value) { values.put("y", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetY() { return values.containsKey("y"); }
    public void unsetY() { values.remove("y"); }

    public String getXErrorUpper() { if (!values.containsKey("xErrorUpper")) throw new ApiError("xErrorUpper" + " is not set"); return values.get("xErrorUpper").asText(); }
    public void setXErrorUpper(String value) { values.put("xErrorUpper", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetXErrorUpper() { return values.containsKey("xErrorUpper"); }
    public void unsetXErrorUpper() { values.remove("xErrorUpper"); }

    public String getXErrorLower() { if (!values.containsKey("xErrorLower")) throw new ApiError("xErrorLower" + " is not set"); return values.get("xErrorLower").asText(); }
    public void setXErrorLower(String value) { values.put("xErrorLower", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetXErrorLower() { return values.containsKey("xErrorLower"); }
    public void unsetXErrorLower() { values.remove("xErrorLower"); }

    public String getYErrorUpper() { if (!values.containsKey("yErrorUpper")) throw new ApiError("yErrorUpper" + " is not set"); return values.get("yErrorUpper").asText(); }
    public void setYErrorUpper(String value) { values.put("yErrorUpper", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetYErrorUpper() { return values.containsKey("yErrorUpper"); }
    public void unsetYErrorUpper() { values.remove("yErrorUpper"); }

    public String getYErrorLower() { if (!values.containsKey("yErrorLower")) throw new ApiError("yErrorLower" + " is not set"); return values.get("yErrorLower").asText(); }
    public void setYErrorLower(String value) { values.put("yErrorLower", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetYErrorLower() { return values.containsKey("yErrorLower"); }
    public void unsetYErrorLower() { values.remove("yErrorLower"); }

    public String getYFrom() { if (!values.containsKey("yFrom")) throw new ApiError("yFrom" + " is not set"); return values.get("yFrom").asText(); }
    public void setYFrom(String value) { values.put("yFrom", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetYFrom() { return values.containsKey("yFrom"); }
    public void unsetYFrom() { values.remove("yFrom"); }

    public String getYTo() { if (!values.containsKey("yTo")) throw new ApiError("yTo" + " is not set"); return values.get("yTo").asText(); }
    public void setYTo(String value) { values.put("yTo", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetYTo() { return values.containsKey("yTo"); }
    public void unsetYTo() { values.remove("yTo"); }

    public String getX() { if (!values.containsKey("x")) throw new ApiError("x" + " is not set"); return values.get("x").asText(); }
    public void setX(String value) { values.put("x", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetX() { return values.containsKey("x"); }
    public void unsetX() { values.remove("x"); }

    public long getOrderValue() { return getOrRefValueNode("order").asLong(); }
    public String getOrderRef() { return getOrRefRefNode("order").asText(); }
    public void setOrderValue(long value) { setOrRefValueNode("order", LongNode.valueOf(value)); }
    public void setOrderRef(String ref) { setOrRefRefNode("order", ref); }
    public boolean isOrderRef() { return isOrRefRef("order"); }
    public boolean isSetOrder() { return values.containsKey("order"); }
    public void unsetOrder() { values.remove("order"); orRefIsRef.remove("order"); }

    public String getStyle() { if (!values.containsKey("style")) throw new ApiError("style" + " is not set"); return values.get("style").asText(); }
    public void setStyle(String value) { values.put("style", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetStyle() { return values.containsKey("style"); }
    public void unsetStyle() { values.remove("style"); }

    public String getYAxisValue() { return getOrRefValueNode("yAxis").asText(); }
    public String getYAxisRef() { return getOrRefRefNode("yAxis").asText(); }
    public void setYAxisValue(String value) { setOrRefValueNode("yAxis", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public void setYAxisRef(String ref) { setOrRefRefNode("yAxis", ref); }
    public boolean isYAxisRef() { return isOrRefRef("yAxis"); }
    public boolean isSetYAxis() { return values.containsKey("yAxis"); }
    public void unsetYAxis() { values.remove("yAxis"); orRefIsRef.remove("yAxis"); }

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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("curve"));
        if (values.containsKey("curveType")) d.set("curveType", values.get("curveType"));
        if (values.containsKey("y")) d.set("y", values.get("y"));
        if (values.containsKey("xErrorUpper")) d.set("xErrorUpper", values.get("xErrorUpper"));
        if (values.containsKey("xErrorLower")) d.set("xErrorLower", values.get("xErrorLower"));
        if (values.containsKey("yErrorUpper")) d.set("yErrorUpper", values.get("yErrorUpper"));
        if (values.containsKey("yErrorLower")) d.set("yErrorLower", values.get("yErrorLower"));
        if (values.containsKey("yFrom")) d.set("yFrom", values.get("yFrom"));
        if (values.containsKey("yTo")) d.set("yTo", values.get("yTo"));
        if (values.containsKey("x")) d.set("x", values.get("x"));
        if (values.containsKey("order")) d.set("order", values.get("order"));
        if (values.containsKey("style")) d.set("style", values.get("style"));
        if (values.containsKey("yAxis")) d.set("yAxis", values.get("yAxis"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

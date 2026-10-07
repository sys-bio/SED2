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

/** Generated from specsheets/outputs/Plot2D/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Plot2D extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("legend", "BooleanOrRef", false, "Plot-0001", null, "Plot-0000", null, null, null, null, null, false, null, null, "Plot-0002", null, null),
        new FieldSpec("height", "NumberOrRef", false, "Plot-0003", null, "Plot-0000", null, null, null, null, null, false, null, null, "Plot-0004", null, null),
        new FieldSpec("width", "NumberOrRef", false, "Plot-0005", null, "Plot-0000", null, null, null, null, null, false, null, null, "Plot-0006", null, null),
        new FieldSpec("notes", "any", false, "SEDBase-0003", null, "SEDBase-0000", null, null, null, null, null, false, null, null, null, null, null),
        new FieldSpec("curves", "dict", true, "Plot2D-0002", "Plot2D-0001", "Plot2D-0000", null, null, null, null, "AbstractCurve", false, null, null, null, null, null),
        new FieldSpec("outputParameters", "array", false, "AbstractOutput-0001", null, "AbstractOutput-0000", null, null, null, "OutputParameter", null, false, null, null, null, null, null),
        new FieldSpec("annotations", "array", false, "SEDBase-0004", null, "SEDBase-0000", null, null, null, "Annotation", null, false, null, null, null, null, null),
        new FieldSpec("rightYAxis", "ref-class", false, "Plot2D-0003", null, "Plot2D-0000", null, null, null, "Axis", null, false, null, null, null, null, null),
        new FieldSpec("xAxis", "ref-class", false, "Plot-0007", null, "Plot-0000", null, null, null, "Axis", null, false, null, null, null, null, null),
        new FieldSpec("yAxis", "ref-class", false, "Plot-0008", null, "Plot-0000", null, null, null, "Axis", null, false, null, null, null, null, null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("curves");
    private final IdKeyedCollection<SedBase> curves = new IdKeyedCollection<>();
    private final ListCollection<SedBase> outputParameters = new ListCollection<>();
    private final ListCollection<SedBase> annotations = new ListCollection<>();
    private SedBase rightYAxis;
    private SedBase xAxis;
    private SedBase yAxis;

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "plot2D"; }
    @Override public String typeRuleId() { return "Plot2D-0004"; }
    @Override public String ownCatchall() { return "Plot2D-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "plot2D"; }

    public boolean getLegendValue() { return getOrRefValueNode("legend").asBoolean(); }
    public String getLegendRef() { return getOrRefRefNode("legend").asText(); }
    public void setLegendValue(boolean value) { setOrRefValueNode("legend", BooleanNode.valueOf(value)); }
    public void setLegendRef(String ref) { setOrRefRefNode("legend", ref); }
    public boolean isLegendRef() { return isOrRefRef("legend"); }
    public boolean isSetLegend() { return values.containsKey("legend"); }
    public void unsetLegend() { values.remove("legend"); orRefIsRef.remove("legend"); }

    public double getHeightValue() { return getOrRefValueNode("height").asDouble(); }
    public String getHeightRef() { return getOrRefRefNode("height").asText(); }
    public void setHeightValue(double value) { setOrRefValueNode("height", DoubleNode.valueOf(value)); }
    public void setHeightRef(String ref) { setOrRefRefNode("height", ref); }
    public boolean isHeightRef() { return isOrRefRef("height"); }
    public boolean isSetHeight() { return values.containsKey("height"); }
    public void unsetHeight() { values.remove("height"); orRefIsRef.remove("height"); }

    public double getWidthValue() { return getOrRefValueNode("width").asDouble(); }
    public String getWidthRef() { return getOrRefRefNode("width").asText(); }
    public void setWidthValue(double value) { setOrRefValueNode("width", DoubleNode.valueOf(value)); }
    public void setWidthRef(String ref) { setOrRefRefNode("width", ref); }
    public boolean isWidthRef() { return isOrRefRef("width"); }
    public boolean isSetWidth() { return values.containsKey("width"); }
    public void unsetWidth() { values.remove("width"); orRefIsRef.remove("width"); }

    public JsonNode getNotes() { if (!values.containsKey("notes")) throw new ApiError("notes" + " is not set"); return values.get("notes"); }
    public void setNotes(JsonNode value) { values.put("notes", value); }
    public boolean isSetNotes() { return values.containsKey("notes"); }
    public void unsetNotes() { values.remove("notes"); }

    public List<String> getCurves() { return curves.ids(); }
    public SedBase getCurvesItem(String itemId) { return curves.get(itemId); }
    public void addCurves(String itemId, SedBase obj) { curves.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertCurves(int index, String itemId, SedBase obj) { curves.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeCurves(String itemId) { curves.remove(itemId); }
    public void setIdOnCurves(String oldId, String newId) { curves.setId(oldId, newId); }

    public List<SedBase> getOutputParameters() { return outputParameters.items(); }
    public void addOutputParameters(SedBase obj) { outputParameters.add(obj); obj.attach(this, getDocument()); }
    public void insertOutputParameters(int index, SedBase obj) { outputParameters.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeOutputParameters(int index) { outputParameters.remove(index); }

    public List<SedBase> getAnnotations() { return annotations.items(); }
    public void addAnnotations(SedBase obj) { annotations.add(obj); obj.attach(this, getDocument()); }
    public void insertAnnotations(int index, SedBase obj) { annotations.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeAnnotations(int index) { annotations.remove(index); }

    public SedBase getRightYAxis() { if (rightYAxis == null) throw new ApiError("rightYAxis" + " is not set"); return rightYAxis; }
    public void setRightYAxis(SedBase obj) { rightYAxis = obj; obj.attach(this, getDocument()); }
    public boolean isSetRightYAxis() { return rightYAxis != null; }
    public void unsetRightYAxis() { rightYAxis = null; }

    public SedBase getXAxis() { if (xAxis == null) throw new ApiError("xAxis" + " is not set"); return xAxis; }
    public void setXAxis(SedBase obj) { xAxis = obj; obj.attach(this, getDocument()); }
    public boolean isSetXAxis() { return xAxis != null; }
    public void unsetXAxis() { xAxis = null; }

    public SedBase getYAxis() { if (yAxis == null) throw new ApiError("yAxis" + " is not set"); return yAxis; }
    public void setYAxis(SedBase obj) { yAxis = obj; obj.attach(this, getDocument()); }
    public boolean isSetYAxis() { return yAxis != null; }
    public void unsetYAxis() { yAxis = null; }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        for (String i : curves.ids()) kids.add(curves.get(i));
        kids.addAll(outputParameters.items());
        kids.addAll(annotations.items());
        if (rightYAxis != null) kids.add(rightYAxis);
        if (xAxis != null) kids.add(xAxis);
        if (yAxis != null) kids.add(yAxis);
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : curves.ids()) out.add(new ChildLoc(curves.get(i), "/curves/" + i));
        { int idx = 0; for (SedBase item : outputParameters.items()) { out.add(new ChildLoc(item, "/outputParameters/" + idx)); idx++; } }
        { int idx = 0; for (SedBase item : annotations.items()) { out.add(new ChildLoc(item, "/annotations/" + idx)); idx++; } }
        if (rightYAxis != null) out.add(new ChildLoc(rightYAxis, "/rightYAxis"));
        if (xAxis != null) out.add(new ChildLoc(xAxis, "/xAxis"));
        if (yAxis != null) out.add(new ChildLoc(yAxis, "/yAxis"));
        return out;
    }

    @Override
    public IdCollection getIdCollection(String fieldName) {
        switch (fieldName) {
            case "curves": return curves;
            default: return null;
        }
    }

    @Override
    public List<String> idCollectionNames() { return List.of("curves"); }

    @Override
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        switch (fieldName) {
            case "curves": return curves;
            default: return super.getDictCollection(fieldName);
        }
    }

    @Override
    protected ListCollection<SedBase> getListCollection(String fieldName) {
        switch (fieldName) {
            case "outputParameters": return outputParameters;
            case "annotations": return annotations;
            default: return super.getListCollection(fieldName);
        }
    }

    @Override
    protected void setChildField(String fieldName, SedBase child) {
        switch (fieldName) {
            case "rightYAxis": rightYAxis = child; return;
            case "xAxis": xAxis = child; return;
            case "yAxis": yAxis = child; return;
            default: super.setChildField(fieldName, child);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("plot2D"));
        if (values.containsKey("legend")) d.set("legend", values.get("legend"));
        if (values.containsKey("height")) d.set("height", values.get("height"));
        if (values.containsKey("width")) d.set("width", values.get("width"));
        if (values.containsKey("notes")) d.set("notes", values.get("notes"));
        if (curves.size() > 0) { ObjectNode sub = d.putObject("curves"); for (String i : curves.ids()) sub.set(i, curves.get(i).toJsonValue()); }
        if (outputParameters.size() > 0) { ArrayNode arr = d.putArray("outputParameters"); for (SedBase item : outputParameters.items()) arr.add(item.toJsonValue()); }
        if (annotations.size() > 0) { ArrayNode arr = d.putArray("annotations"); for (SedBase item : annotations.items()) arr.add(item.toJsonValue()); }
        if (rightYAxis != null) d.set("rightYAxis", rightYAxis.toJsonValue());
        if (xAxis != null) d.set("xAxis", xAxis.toJsonValue());
        if (yAxis != null) d.set("yAxis", yAxis.toJsonValue());
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

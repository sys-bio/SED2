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

/** Generated from test-specsheets/outputs/Plot3D/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Plot3D extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("height", "NumberOrRef", false, ["Plot-0003", "Plot-0004"], null, "Plot-0000", null, null, null, null, null),
        new FieldSpec("width", "NumberOrRef", false, ["Plot-0005", "Plot-0006"], null, "Plot-0000", null, null, null, null, null),
        new FieldSpec("surfaces", "dict", true, "Plot3D-0002", "Plot3D-0001", "Plot3D-0000", null, null, null, "Surface", null),
        new FieldSpec("outputParameters", "array", false, "AbstractOutput-0001", null, "AbstractOutput-0000", null, null, null, "OutputParameter", null)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("surfaces");
    private final IdKeyedCollection<SedBase> surfaces = new IdKeyedCollection<>();
    private final ListCollection<SedBase> outputParameters = new ListCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return "plot3D"; }
    @Override public String typeRuleId() { return "Plot3D-0004"; }
    @Override public String ownCatchall() { return "Plot3D-0000"; }
    @Override public String nameRuleId() { return "SEDBase-0001"; }
    @Override public String descRuleId() { return "SEDBase-0002"; }
    @Override public String baseCatchall() { return "SEDBase-0000"; }
    public String getType() { return "plot3D"; }

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

    public List<String> getSurfaces() { return surfaces.ids(); }
    public SedBase getSurfacesItem(String itemId) { return surfaces.get(itemId); }
    public void addSurfaces(String itemId, SedBase obj) { surfaces.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertSurfaces(int index, String itemId, SedBase obj) { surfaces.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeSurfaces(String itemId) { surfaces.remove(itemId); }
    public void setIdOnSurfaces(String oldId, String newId) { surfaces.setId(oldId, newId); }

    public List<SedBase> getOutputParameters() { return outputParameters.items(); }
    public void addOutputParameters(SedBase obj) { outputParameters.add(obj); obj.attach(this, getDocument()); }
    public void insertOutputParameters(int index, SedBase obj) { outputParameters.insert(index, obj); obj.attach(this, getDocument()); }
    public void removeOutputParameters(int index) { outputParameters.remove(index); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        for (String i : surfaces.ids()) kids.add(surfaces.get(i));
        kids.addAll(outputParameters.items());
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : surfaces.ids()) out.add(new ChildLoc(surfaces.get(i), "/surfaces/" + i));
        { int idx = 0; for (SedBase item : outputParameters.items()) { out.add(new ChildLoc(item, "/outputParameters/" + idx)); idx++; } }
        return out;
    }

    @Override
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        switch (fieldName) {
            case "surfaces": return surfaces;
            default: return super.getDictCollection(fieldName);
        }
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
        d.set("_type", values.containsKey("_type") ? values.get("_type") : TextNode.valueOf("plot3D"));
        if (values.containsKey("height")) d.set("height", values.get("height"));
        if (values.containsKey("width")) d.set("width", values.get("width"));
        if (surfaces.size() > 0) { ObjectNode sub = d.putObject("surfaces"); for (String i : surfaces.ids()) sub.set(i, surfaces.get(i).toJsonValue()); }
        if (outputParameters.size() > 0) { ArrayNode arr = d.putArray("outputParameters"); for (SedBase item : outputParameters.items()) arr.add(item.toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

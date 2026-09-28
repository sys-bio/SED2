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

/** Generated from test-specsheets/core/TestDocument/. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class TestDocument extends SedBase {
    private static final List<FieldSpec> FIELD_SPECS = List.of(
        new FieldSpec("version", "string", true, null, "TestDocument-0001", "TestDocument-0000", null, null, "^v\\d+\\.\\d+\\.\\d+$", null, null, false),
        new FieldSpec("widgets", "dict", false, "TestDocument-0002", null, "TestDocument-0000", null, null, null, null, "AbstractWidget", false),
        new FieldSpec("reports", "dict", false, "TestDocument-0003", null, "TestDocument-0000", null, null, null, null, "AbstractReport", false)
    );
    private static final Set<String> REQUIRED_NAMES = Set.of("version");
    private final IdKeyedCollection<SedBase> widgets = new IdKeyedCollection<>();
    private final IdKeyedCollection<SedBase> reports = new IdKeyedCollection<>();

    @Override public List<FieldSpec> fieldSpecs() { return FIELD_SPECS; }
    @Override public Set<String> requiredNames() { return REQUIRED_NAMES; }
    @Override public String typeConst() { return null; }
    @Override public String typeRuleId() { return null; }
    @Override public String ownCatchall() { return "TestDocument-0000"; }
    @Override public String nameRuleId() { return "TestBase-0001"; }
    @Override public String descRuleId() { return null; }
    @Override public String baseCatchall() { return "TestBase-0000"; }

    public String getVersion() { if (!values.containsKey("version")) throw new ApiError("version" + " is not set"); return values.get("version").asText(); }
    public void setVersion(String value) { values.put("version", value == null ? NullNode.getInstance() : TextNode.valueOf(value)); }
    public boolean isSetVersion() { return values.containsKey("version"); }
    public void unsetVersion() { values.remove("version"); }

    public List<String> getWidgets() { return widgets.ids(); }
    public SedBase getWidgetsItem(String itemId) { return widgets.get(itemId); }
    public void addWidgets(String itemId, SedBase obj) { widgets.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertWidgets(int index, String itemId, SedBase obj) { widgets.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeWidgets(String itemId) { widgets.remove(itemId); }
    public void setIdOnWidgets(String oldId, String newId) { widgets.setId(oldId, newId); }

    public List<String> getReports() { return reports.ids(); }
    public SedBase getReportsItem(String itemId) { return reports.get(itemId); }
    public void addReports(String itemId, SedBase obj) { reports.add(itemId, obj); obj.attach(this, getDocument()); }
    public void insertReports(int index, String itemId, SedBase obj) { reports.insert(index, itemId, obj); obj.attach(this, getDocument()); }
    public void removeReports(String itemId) { reports.remove(itemId); }
    public void setIdOnReports(String oldId, String newId) { reports.setId(oldId, newId); }

    @Override
    public List<SedBase> children() {
        List<SedBase> kids = new ArrayList<>();
        for (String i : widgets.ids()) kids.add(widgets.get(i));
        for (String i : reports.ids()) kids.add(reports.get(i));
        return kids;
    }

    @Override
    public List<ChildLoc> childrenWithLocations() {
        List<ChildLoc> out = new ArrayList<>();
        for (String i : widgets.ids()) out.add(new ChildLoc(widgets.get(i), "/widgets/" + i));
        for (String i : reports.ids()) out.add(new ChildLoc(reports.get(i), "/reports/" + i));
        return out;
    }

    @Override
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        switch (fieldName) {
            case "widgets": return widgets;
            case "reports": return reports;
            default: return super.getDictCollection(fieldName);
        }
    }

    @Override
    public ObjectNode ownJsonValue() {
        ObjectNode d = JsonNodeFactory.instance.objectNode();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        if (values.containsKey("version")) d.set("version", values.get("version"));
        if (widgets.size() > 0) { ObjectNode sub = d.putObject("widgets"); for (String i : widgets.ids()) sub.set(i, widgets.get(i).toJsonValue()); }
        if (reports.size() > 0) { ObjectNode sub = d.putObject("reports"); for (String i : reports.ids()) sub.set(i, reports.get(i).toJsonValue()); }
        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());
        return d;
    }
}

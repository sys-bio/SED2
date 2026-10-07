package org.sedml.libsed2;

import com.fasterxml.jackson.databind.JsonNode;

import java.util.LinkedHashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;

/** Generated dispatch/parse per discriminator, plus the generic field
 * loader used by every parse* method and by Io.readFromString(). All
 * load-time violations (extra/unrecognized properties, bad dict-of-
 * discriminated-union keys, bad container shapes, and dispatch problems
 * bubbled up from a nested item) are appended straight onto
 * obj.loadProblems - this is the only point that sees the raw JSON before
 * an unrecognized key is dropped, so it is the only reliable place to
 * detect them (see Design.md's Schema-Pass Errors section - mirrors
 * generator/emit_python.py's _load_fields()). GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Dispatch {
    private Dispatch() {}

    // The full OrRef family whose value is loaded via the generic
    // setOrRefValueNode/setOrRefRefNode pair rather than a plain
    // obj.values.put() - see generator/emit_java.py's _ORREF_KINDS_JAVA
    // (the same six kinds every generated model class's own accessors
    // handle).
    private static final Set<String> ORREF_KINDS = Set.of(
            "StringOrRef", "NumberOrRef", "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef");

    public static final class Result {
        public final SedBase value;
        public final ValidationProblem problem;

        public Result(SedBase value, ValidationProblem problem) {
            this.value = value;
            this.problem = problem;
        }
    }

    @FunctionalInterface
    public interface ParseFn {
        Result parse(JsonNode raw);
    }

    public static Result parseAbstractTask(JsonNode raw) {
        if (!raw.has("_type")) {
            return new Result(null, RuleCatalog.makeProblem("AbstractTask-0002", ""));
        }
        String tv = raw.get("_type").asText();
        SedBase obj = null;
        switch (tv) {
            case "aggregationCalculation": obj = new AggregationCalculation(); break;
            case "boundedODESimulation": obj = new BoundedODESimulation(); break;
            case "boundedStochasticSimulation": obj = new BoundedStochasticSimulation(); break;
            case "calculation": obj = new Calculation(); break;
            case "createDataBlock": obj = new CreateDataBlock(); break;
            case "csvImport": obj = new CsvImport(); break;
            case "dataImport": obj = new DataImport(); break;
            case "drawFromDistribution": obj = new DrawFromDistribution(); break;
            case "explicitODESimulation": obj = new ExplicitODESimulation(); break;
            case "explicitStochasticSimulation": obj = new ExplicitStochasticSimulation(); break;
            case "fluxBalanceAnalysis": obj = new FluxBalanceAnalysis(); break;
            case "jacobianFull": obj = new JacobianFull(); break;
            case "jacobianReduced": obj = new JacobianReduced(); break;
            case "loop": obj = new Loop(); break;
            case "modelChange": obj = new ModelChange(); break;
            case "modelElementList": obj = new ModelElementList(); break;
            case "modelImport": obj = new ModelImport(); break;
            case "numericRange": obj = new NumericRange(); break;
            case "oneStepODESimulation": obj = new OneStepODESimulation(); break;
            case "oneStepStochasticSimulation": obj = new OneStepStochasticSimulation(); break;
            case "parameterRange": obj = new ParameterRange(); break;
            case "parameterScan": obj = new ParameterScan(); break;
            case "range": obj = new Range(); break;
            case "relabelData": obj = new RelabelData(); break;
            case "scatter": obj = new Scatter(); break;
            case "steadyState": obj = new SteadyState(); break;
            case "stringFormation": obj = new StringFormation(); break;
        }
        if (obj != null) {
            loadFields(obj, raw);
            return new Result(obj, null);
        }
        Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(tv);
        Set<String> known = Set.of();
        if (m.matches() && !known.contains(m.group(1))) {
            return new Result(new UnknownAbstractTask(tv, raw), null);
        }
        Map<String, Object> ph = new LinkedHashMap<>();
        ph.put("schema-message", "unrecognized _type " + PyFmt.repr(raw.get("_type")));
        return new Result(new UnknownAbstractTask(tv, raw), RuleCatalog.makeProblem("AbstractTask-0000", "", ph));
    }

    public static Result parseRangeInline(JsonNode raw) {
        if (!raw.has("_type")) {
            return new Result(null, RuleCatalog.makeProblem("Range-0004", ""));
        }
        String tv = raw.get("_type").asText();
        SedBase obj = null;
        switch (tv) {
            case "numericRange": obj = new NumericRange(); break;
            case "parameterRange": obj = new ParameterRange(); break;
            case "range": obj = new Range(); break;
        }
        if (obj != null) {
            loadFields(obj, raw);
            return new Result(obj, null);
        }
        Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(tv);
        Set<String> known = Set.of();
        if (m.matches() && !known.contains(m.group(1))) {
            return new Result(new UnknownRangeInline(tv, raw), null);
        }
        Map<String, Object> ph = new LinkedHashMap<>();
        ph.put("schema-message", "unrecognized _type " + PyFmt.repr(raw.get("_type")));
        return new Result(new UnknownRangeInline(tv, raw), RuleCatalog.makeProblem("RangeInline-0000", "", ph));
    }

    public static Result parseAbstractOutput(JsonNode raw) {
        if (!raw.has("_type")) {
            return new Result(null, RuleCatalog.makeProblem("AbstractOutput-0002", ""));
        }
        String tv = raw.get("_type").asText();
        SedBase obj = null;
        switch (tv) {
            case "plot2D": obj = new Plot2D(); break;
            case "plot3D": obj = new Plot3D(); break;
            case "report": obj = new Report(); break;
        }
        if (obj != null) {
            loadFields(obj, raw);
            return new Result(obj, null);
        }
        Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(tv);
        Set<String> known = Set.of();
        if (m.matches() && !known.contains(m.group(1))) {
            return new Result(new UnknownAbstractOutput(tv, raw), null);
        }
        Map<String, Object> ph = new LinkedHashMap<>();
        ph.put("schema-message", "unrecognized _type " + PyFmt.repr(raw.get("_type")));
        return new Result(new UnknownAbstractOutput(tv, raw), RuleCatalog.makeProblem("AbstractOutput-0000", "", ph));
    }

    public static Result parseAbstractCurve(JsonNode raw) {
        if (!raw.has("_type")) {
            return new Result(null, RuleCatalog.makeProblem("AbstractCurve-0008", ""));
        }
        String tv = raw.get("_type").asText();
        SedBase obj = null;
        switch (tv) {
            case "curve": obj = new Curve(); break;
        }
        if (obj != null) {
            loadFields(obj, raw);
            return new Result(obj, null);
        }
        Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(tv);
        Set<String> known = Set.of();
        if (m.matches() && !known.contains(m.group(1))) {
            return new Result(new UnknownAbstractCurve(tv, raw), null);
        }
        Map<String, Object> ph = new LinkedHashMap<>();
        ph.put("schema-message", "unrecognized _type " + PyFmt.repr(raw.get("_type")));
        return new Result(new UnknownAbstractCurve(tv, raw), RuleCatalog.makeProblem("AbstractCurve-0000", "", ph));
    }

    private static ParseFn parserFor(String discName) {
        switch (discName) {
            case "AbstractTask": return Dispatch::parseAbstractTask;
            case "RangeInline": return Dispatch::parseRangeInline;
            case "AbstractOutput": return Dispatch::parseAbstractOutput;
            case "AbstractCurve": return Dispatch::parseAbstractCurve;
            default: throw new ApiError("unknown discriminator " + discName);
        }
    }

    private static SedBase newItemInstance(String className) {
        switch (className) {
            case "AggregationCalculation": return new AggregationCalculation();
            case "Annotation": return new Annotation();
            case "Axis": return new Axis();
            case "LoopVariable": return new LoopVariable();
            case "NumericRange": return new NumericRange();
            case "OutputParameter": return new OutputParameter();
            case "ParameterRange": return new ParameterRange();
            case "Span": return new Span();
            case "Style": return new Style();
            case "Surface": return new Surface();
            case "TaskParameter": return new TaskParameter();
            case "WorkingAlgorithm": return new WorkingAlgorithm();
            default: throw new ApiError("unknown item class " + className);
        }
    }

    public static void loadFields(SedBase obj, JsonNode raw) {
        if (raw.has("name") && !raw.get("name").isNull()) obj.nameNode = raw.get("name");
        if (raw.has("description") && !raw.get("description").isNull()) obj.descriptionNode = raw.get("description");
        if (raw.has("_type")) obj.values.put("_type", raw.get("_type"));

        for (FieldSpec spec : obj.fieldSpecs()) {
            if (!raw.has(spec.name) || spec.kind.equals("dict") || spec.kind.equals("array")
                    || spec.kind.equals("any-dict") || spec.kind.equals("ref-class")
                    || spec.kind.equals("ref-discriminator")) continue;
            JsonNode v = raw.get(spec.name);
            if (ORREF_KINDS.contains(spec.kind)) {
                if (v.isTextual() && v.asText().startsWith("#")) {
                    obj.setOrRefRefNode(spec.name, v.asText());
                } else {
                    obj.setOrRefValueNode(spec.name, v);
                }
            } else {
                obj.values.put(spec.name, v);
            }
        }
        for (Map.Entry<String, java.util.List<FieldSpec>> e : obj.namespaceFields().entrySet()) {
            for (FieldSpec spec : e.getValue()) {
                if (raw.has(spec.name)) obj.values.put(spec.name, raw.get(spec.name));
            }
        }

        Set<String> allowed = obj.allowedKeys();
        Iterator<String> keyIt = raw.fieldNames();
        while (keyIt.hasNext()) {
            String key = keyIt.next();
            if (key.equals("_type") || key.equals("name") || key.equals("description")) continue;
            if (allowed.contains(key)) continue;
            Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(key);
            if (m.matches()) {
                String prefix = m.group(1), nsKey = m.group(2);
                obj.setNamespaceAttribute(prefix, nsKey, raw.get(key));
                if (obj.knownNamespacePrefixes().contains(prefix)) {
                    String catchall = obj.namespaceCatchall().getOrDefault(prefix, obj.ownCatchall());
                    Map<String, Object> ph = new LinkedHashMap<>();
                    ph.put("schema-message", "Additional property '" + key + "' is not allowed.");
                    obj.loadProblems.add(RuleCatalog.makeProblem(catchall, "", ph));
                }
                continue;
            }
            Map<String, Object> ph = new LinkedHashMap<>();
            ph.put("schema-message", "Additional property '" + key + "' is not allowed.");
            obj.loadProblems.add(RuleCatalog.makeProblem(obj.ownCatchall(), "", ph));
        }

        for (FieldSpec spec : obj.fieldSpecs()) {
            if (spec.kind.equals("dict") && raw.has(spec.name)) {
                JsonNode rawValue = raw.get(spec.name);
                if (!rawValue.isObject()) {
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new LinkedHashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", obj.getClass().getSimpleName());
                    ph.put("id", obj.ownIdForMessage());
                    ph.put("value", rawValue);
                    obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    continue;
                }
                IdKeyedCollection<SedBase> coll = obj.getDictCollection(spec.name);
                // A dict-kind field is either _type-dispatched
                // (itemDiscriminator set, e.g. SEDDocument.tasks ->
                // AbstractTask) or a plain fixed-class dict with no _type
                // dispatch at all (itemClass set instead, e.g.
                // SEDDocument.styles -> Style, Loop.loopVariables ->
                // LoopVariable) - parserFor(null) would throw, so this
                // mirrors the "array"-kind branch's own newItemInstance
                // fallback just below, and generator/emit_python.py's
                // _load_fields dict branch (`dispatch = ... if
                // spec.item_discriminator else None`), the reference
                // implementation this ports.
                ParseFn dispatch = spec.itemDiscriminator != null ? parserFor(spec.itemDiscriminator) : null;
                Iterator<String> ids = rawValue.fieldNames();
                while (ids.hasNext()) {
                    String itemId = ids.next();
                    JsonNode itemRaw = rawValue.get(itemId);
                    if (!itemId.matches(LeafValidation.SID_PATTERN)) {
                        String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                        Map<String, Object> ph = new LinkedHashMap<>();
                        ph.put("attr", spec.name);
                        ph.put("class", obj.getClass().getSimpleName());
                        ph.put("id", obj.ownIdForMessage());
                        ph.put("value", itemId);
                        obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    }
                    SedBase child;
                    if (dispatch != null) {
                        Result r = dispatch.parse(itemRaw);
                        if (r.problem != null) obj.loadProblems.add(r.problem);
                        child = r.value;
                    } else {
                        child = newItemInstance(spec.itemClass);
                        loadFields(child, itemRaw);
                    }
                    if (child != null) coll.add(itemId, child);
                }
            } else if (spec.kind.equals("array") && raw.has(spec.name)) {
                JsonNode rawValue = raw.get(spec.name);
                if (!rawValue.isArray()) {
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new LinkedHashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", obj.getClass().getSimpleName());
                    ph.put("id", obj.ownIdForMessage());
                    ph.put("value", rawValue);
                    obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    continue;
                }
                ListCollection<SedBase> coll = obj.getListCollection(spec.name);
                for (JsonNode itemRaw : rawValue) {
                    SedBase child = newItemInstance(spec.itemClass);
                    loadFields(child, itemRaw);
                    coll.add(child);
                }
            } else if (spec.kind.equals("any-dict") && raw.has(spec.name)) {
                // Same ID-keyed-collection shape as "dict" just above, but
                // every value is stored as-is - a plain JsonNode, never
                // constructed as a class instance (see this module's
                // _collection_accessors_java any-dict branch and
                // generator/emit_python.py's _load_fields any-dict branch,
                // the reference implementation this mirrors).
                JsonNode rawValue = raw.get(spec.name);
                if (!rawValue.isObject()) {
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new LinkedHashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", obj.getClass().getSimpleName());
                    ph.put("id", obj.ownIdForMessage());
                    ph.put("value", rawValue);
                    obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    continue;
                }
                IdKeyedCollection<JsonNode> coll = obj.getAnyDictCollection(spec.name);
                Iterator<String> ids = rawValue.fieldNames();
                while (ids.hasNext()) {
                    String itemId = ids.next();
                    JsonNode itemValue = rawValue.get(itemId);
                    if (!itemId.matches(LeafValidation.SID_PATTERN)) {
                        String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                        Map<String, Object> ph = new LinkedHashMap<>();
                        ph.put("attr", spec.name);
                        ph.put("class", obj.getClass().getSimpleName());
                        ph.put("id", obj.ownIdForMessage());
                        ph.put("value", itemId);
                        obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    }
                    coll.add(itemId, itemValue);
                }
            } else if ((spec.kind.equals("ref-class") || spec.kind.equals("ref-discriminator")) && raw.has(spec.name)) {
                // A single nested SedBase-derived child (see this module's
                // _child_accessors_java docstring) - "ref-class" constructs
                // a fixed target class directly; "ref-discriminator"
                // dispatches on the raw JSON's own _type via the matching
                // parse* method, same as a dict-kind field's own
                // discriminated items above. Mirrors
                // generator/emit_python.py's _load_fields ref-class/
                // ref-discriminator branch.
                JsonNode rawValue = raw.get(spec.name);
                if (!rawValue.isObject()) {
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new LinkedHashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", obj.getClass().getSimpleName());
                    ph.put("id", obj.ownIdForMessage());
                    ph.put("value", rawValue);
                    obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    continue;
                }
                SedBase child;
                if (spec.kind.equals("ref-discriminator")) {
                    ParseFn dispatch = parserFor(spec.itemDiscriminator);
                    Result r = dispatch.parse(rawValue);
                    if (r.problem != null) obj.loadProblems.add(r.problem);
                    child = r.value;
                } else {
                    child = newItemInstance(spec.itemClass);
                    loadFields(child, rawValue);
                }
                if (child != null) obj.setChildField(spec.name, child);
            }
        }
    }
}

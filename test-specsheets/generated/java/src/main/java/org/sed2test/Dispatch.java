package org.sed2test;

import com.fasterxml.jackson.databind.JsonNode;

import java.util.HashMap;
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

    public static Result parseAbstractWidget(JsonNode raw) {
        if (!raw.has("_type")) {
            return new Result(null, RuleCatalog.makeProblem("AbstractWidget-0002", ""));
        }
        String tv = raw.get("_type").asText();
        SedBase obj = null;
        switch (tv) {
            case "fancyWidget": obj = new FancyWidget(); break;
            case "simpleWidget": obj = new SimpleWidget(); break;
            case "acme@acmeWidget": obj = new AcmeWidget(); break;
        }
        if (obj != null) {
            loadFields(obj, raw);
            return new Result(obj, null);
        }
        Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(tv);
        Set<String> known = Set.of("acme");
        if (m.matches() && !known.contains(m.group(1))) {
            return new Result(new UnknownAbstractWidget(tv, raw), null);
        }
        Map<String, Object> ph = new HashMap<>();
        ph.put("schema-message", "unrecognized _type '" + tv + "'");
        return new Result(new UnknownAbstractWidget(tv, raw), RuleCatalog.makeProblem("AbstractWidget-0000", "", ph));
    }

    public static Result parseAbstractReport(JsonNode raw) {
        if (!raw.has("_type")) {
            return new Result(null, RuleCatalog.makeProblem("AbstractReport-0002", ""));
        }
        String tv = raw.get("_type").asText();
        SedBase obj = null;
        switch (tv) {
            case "simpleReport": obj = new SimpleReport(); break;
        }
        if (obj != null) {
            loadFields(obj, raw);
            return new Result(obj, null);
        }
        Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(tv);
        Set<String> known = Set.of();
        if (m.matches() && !known.contains(m.group(1))) {
            return new Result(new UnknownAbstractReport(tv, raw), null);
        }
        Map<String, Object> ph = new HashMap<>();
        ph.put("schema-message", "unrecognized _type '" + tv + "'");
        return new Result(new UnknownAbstractReport(tv, raw), RuleCatalog.makeProblem("AbstractReport-0000", "", ph));
    }

    public static Result parseChoiceInline(JsonNode raw) {
        if (!raw.has("_type")) {
            Map<String, Object> ph0 = new HashMap<>();
            ph0.put("schema-message", "missing _type");
            return new Result(null, RuleCatalog.makeProblem("ChoiceInline-0000", "", ph0));
        }
        String tv = raw.get("_type").asText();
        SedBase obj = null;
        switch (tv) {
            case "choice": obj = new Choice(); break;
            case "weightedChoice": obj = new WeightedChoice(); break;
        }
        if (obj != null) {
            loadFields(obj, raw);
            return new Result(obj, null);
        }
        Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(tv);
        Set<String> known = Set.of();
        if (m.matches() && !known.contains(m.group(1))) {
            return new Result(new UnknownChoiceInline(tv, raw), null);
        }
        Map<String, Object> ph = new HashMap<>();
        ph.put("schema-message", "unrecognized _type '" + tv + "'");
        return new Result(new UnknownChoiceInline(tv, raw), RuleCatalog.makeProblem("ChoiceInline-0000", "", ph));
    }

    private static ParseFn parserFor(String discName) {
        switch (discName) {
            case "AbstractWidget": return Dispatch::parseAbstractWidget;
            case "AbstractReport": return Dispatch::parseAbstractReport;
            case "ChoiceInline": return Dispatch::parseChoiceInline;
            default: throw new ApiError("unknown discriminator " + discName);
        }
    }

    private static SedBase newItemInstance(String className) {
        switch (className) {
            case "Note": return new Note();
            default: throw new ApiError("unknown item class " + className);
        }
    }

    public static void loadFields(SedBase obj, JsonNode raw) {
        if (raw.has("name") && !raw.get("name").isNull()) obj.nameNode = raw.get("name");
        if (raw.has("description") && !raw.get("description").isNull()) obj.descriptionNode = raw.get("description");
        if (raw.has("_type")) obj.values.put("_type", raw.get("_type"));

        for (FieldSpec spec : obj.fieldSpecs()) {
            if (!raw.has(spec.name) || spec.kind.equals("dict") || spec.kind.equals("array")) continue;
            JsonNode v = raw.get(spec.name);
            if (spec.kind.equals("StringOrRef") || spec.kind.equals("NumberOrRef")) {
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
                    Map<String, Object> ph = new HashMap<>();
                    ph.put("schema-message", "Additional property '" + key + "' is not allowed.");
                    obj.loadProblems.add(RuleCatalog.makeProblem(catchall, "", ph));
                }
                continue;
            }
            Map<String, Object> ph = new HashMap<>();
            ph.put("schema-message", "Additional property '" + key + "' is not allowed.");
            obj.loadProblems.add(RuleCatalog.makeProblem(obj.ownCatchall(), "", ph));
        }

        for (FieldSpec spec : obj.fieldSpecs()) {
            if (spec.kind.equals("dict") && raw.has(spec.name)) {
                JsonNode rawValue = raw.get(spec.name);
                if (!rawValue.isObject()) {
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new HashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", obj.getClass().getSimpleName());
                    ph.put("id", obj.ownIdForMessage());
                    ph.put("value", rawValue.toString());
                    obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    continue;
                }
                IdKeyedCollection<SedBase> coll = obj.getDictCollection(spec.name);
                ParseFn dispatch = parserFor(spec.itemDiscriminator);
                Iterator<String> ids = rawValue.fieldNames();
                while (ids.hasNext()) {
                    String itemId = ids.next();
                    JsonNode itemRaw = rawValue.get(itemId);
                    if (!itemId.matches(LeafValidation.SID_PATTERN)) {
                        String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                        Map<String, Object> ph = new HashMap<>();
                        ph.put("attr", spec.name);
                        ph.put("class", obj.getClass().getSimpleName());
                        ph.put("id", obj.ownIdForMessage());
                        ph.put("value", itemId);
                        obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    }
                    Result r = dispatch.parse(itemRaw);
                    if (r.problem != null) obj.loadProblems.add(r.problem);
                    if (r.value != null) coll.add(itemId, r.value);
                }
            } else if (spec.kind.equals("array") && raw.has(spec.name)) {
                JsonNode rawValue = raw.get(spec.name);
                if (!rawValue.isArray()) {
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new HashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", obj.getClass().getSimpleName());
                    ph.put("id", obj.ownIdForMessage());
                    ph.put("value", rawValue.toString());
                    obj.loadProblems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                    continue;
                }
                ListCollection<SedBase> coll = obj.getListCollection(spec.name);
                for (JsonNode itemRaw : rawValue) {
                    SedBase child = newItemInstance(spec.itemClass);
                    loadFields(child, itemRaw);
                    coll.add(child);
                }
            }
        }
    }
}

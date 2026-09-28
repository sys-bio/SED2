package org.sedml.libsed2;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.lang.ref.WeakReference;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Pattern;

/** Universal base: every generated element (mirrors TestBaseFields'
 * name/description) plus parent/document backpointers, generic namespace
 * attribute storage, and the shared validate() engine. See Design.md's
 * Classes section - Java uses WeakReference for parent/document to avoid
 * reference cycles, matching this project's C++ raw-pointer intent (the
 * same design as the Python target's weakref usage).
 * GENERATED (this file) - do not hand-edit; regenerate via
 * generator/generate.py. */
public abstract class SedBase {
    public static final Pattern NAMESPACE_KEY_PATTERN =
            Pattern.compile("^([A-Za-z_][A-Za-z0-9_]*)@([A-Za-z_][A-Za-z0-9_]*)$");

    protected static final Set<String> LEAF_KINDS = new HashSet<>(List.of(
            "string", "integer", "number", "boolean", "SId", "SIdRef", "StringOrRef", "NumberOrRef"));

    // -- per-concrete-class metadata, overridden by generated subclasses --
    public List<FieldSpec> fieldSpecs() { return Collections.emptyList(); }
    public Set<String> requiredNames() { return Collections.emptySet(); }
    public String typeConst() { return null; }
    public String typeRuleId() { return null; }
    public String ownCatchall() { return ""; }
    public Map<String, List<FieldSpec>> namespaceFields() { return Collections.emptyMap(); }
    public Map<String, String> namespaceCatchall() { return Collections.emptyMap(); }
    public Set<String> knownNamespacePrefixes() { return Collections.emptySet(); }
    public String nameRuleId() { return null; }
    public String descRuleId() { return null; }
    public String baseCatchall() { return ""; }

    protected JsonNode nameNode;
    protected JsonNode descriptionNode;
    // Every leaf/namespace-leaf/OrRef/_type value is stored as its actual
    // JsonNode, not a converted native Java primitive - this keeps storage,
    // re-serialization (ownJsonValue()) and leaf validation (which also
    // wants a JsonNode) all using one representation, and generated
    // accessors do the one conversion to a natural Java type at the point
    // of use (see generator/emit_java.py's _leaf_accessors_java()).
    protected final Map<String, JsonNode> values = new LinkedHashMap<>();
    protected final Map<String, Boolean> orRefIsRef = new HashMap<>();
    // "prefix@key" -> raw JsonNode - so an opaque passthrough attribute
    // (object/array/number/string/bool) round-trips losslessly, matching
    // the Python target's use of Python's native json.loads() types for
    // the same purpose.
    protected final Map<String, JsonNode> nsAttrs = new LinkedHashMap<>();
    protected final List<ValidationProblem> loadProblems = new ArrayList<>();

    private WeakReference<SedBase> parentRef;
    private WeakReference<SedBase> documentRef;

    // -- backpointers --
    public SedBase getParent() { return parentRef == null ? null : parentRef.get(); }

    public SedBase getDocument() { return documentRef == null ? null : documentRef.get(); }

    public void attach(SedBase parent, SedBase document) {
        this.parentRef = parent == null ? null : new WeakReference<>(parent);
        this.documentRef = document == null ? null : new WeakReference<>(document);
        for (SedBase child : children()) {
            child.attach(this, document);
        }
    }

    /** Every SedBase-derived child reachable from this element, for
     * backpointer propagation and validate() recursion. */
    public List<SedBase> children() { return Collections.emptyList(); }

    // -- universal name/description (TestBaseFields) --
    // Stored as the raw JsonNode (not a coerced String) so a wrong-typed
    // incoming value (e.g. a JSON number for `name`) is preserved for the
    // leaf-type check in validateOwn() instead of being silently
    // stringified away - see generator/emit_java.py's Dispatch.loadFields.
    public String getName() {
        if (nameNode == null) throw new ApiError("name is not set");
        return nameNode.asText();
    }

    public boolean isSetName() { return nameNode != null; }

    public void setName(String value) { this.nameNode = value == null ? null : com.fasterxml.jackson.databind.node.TextNode.valueOf(value); }

    public void unsetName() { this.nameNode = null; }

    public String getDescription() {
        if (descriptionNode == null) throw new ApiError("description is not set");
        return descriptionNode.asText();
    }

    public boolean isSetDescription() { return descriptionNode != null; }

    public void setDescription(String value) { this.descriptionNode = value == null ? null : com.fasterxml.jackson.databind.node.TextNode.valueOf(value); }

    public void unsetDescription() { this.descriptionNode = null; }

    // -- generic namespace attribute store (Design.md's Namespaces section) --
    public JsonNode getNamespaceAttribute(String prefix, String key) {
        String k = prefix + "@" + key;
        if (!nsAttrs.containsKey(k)) throw new ApiError("namespace attribute " + k + " is not set");
        return nsAttrs.get(k);
    }

    public void setNamespaceAttribute(String prefix, String key, JsonNode value) {
        nsAttrs.put(prefix + "@" + key, value);
    }

    public boolean isSetNamespaceAttribute(String prefix, String key) {
        return nsAttrs.containsKey(prefix + "@" + key);
    }

    public void unsetNamespaceAttribute(String prefix, String key) {
        nsAttrs.remove(prefix + "@" + key);
    }

    // -- generic OrRef-shaped storage helpers, used by generated accessors --
    protected JsonNode getOrRefValueNode(String name) {
        if (!values.containsKey(name)) throw new ApiError(name + " is not set");
        if (Boolean.TRUE.equals(orRefIsRef.get(name))) throw new ApiError(name + " holds a reference, not a literal value");
        return values.get(name);
    }

    protected JsonNode getOrRefRefNode(String name) {
        if (!values.containsKey(name)) throw new ApiError(name + " is not set");
        if (!Boolean.TRUE.equals(orRefIsRef.get(name))) throw new ApiError(name + " holds a literal value, not a reference");
        return values.get(name);
    }

    protected void setOrRefValueNode(String name, JsonNode value) {
        values.put(name, value);
        orRefIsRef.put(name, false);
    }

    protected void setOrRefRefNode(String name, String ref) {
        if (!isReference(ref)) throw new ApiError("'" + ref + "' is not a valid reference (must start with '#')");
        values.put(name, com.fasterxml.jackson.databind.node.TextNode.valueOf(ref));
        orRefIsRef.put(name, true);
    }

    protected boolean isOrRefRef(String name) {
        if (!values.containsKey(name)) throw new ApiError(name + " is not set");
        return Boolean.TRUE.equals(orRefIsRef.get(name));
    }

    public static boolean isReference(String value) {
        return value != null && value.startsWith("#");
    }

    // -- collection field access (overridden per generated concrete class,
    // mirroring the Python target's getattr(obj, '_' + pyname(name))) --
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {
        throw new ApiError("no such dict field: " + fieldName);
    }

    protected ListCollection<SedBase> getListCollection(String fieldName) {
        throw new ApiError("no such list field: " + fieldName);
    }

    // -- validate() engine --------------------------------------------------
    public List<ValidationProblem> validate() {
        return validate("warning");
    }

    public List<ValidationProblem> validate(String severityAtLeast) {
        List<ValidationProblem> problems = new ArrayList<>(validateOwn());
        Set<String> seen = new HashSet<>();
        for (ValidationProblem p : problems) seen.add(p.ruleId + "\u0000" + p.location);
        for (ChildLoc cl : childrenWithLocations()) {
            for (ValidationProblem p : cl.child.validate("warning")) {
                ValidationProblem p2 = new ValidationProblem(
                        p.ruleId, p.severity, p.rule, p.message, cl.locationPrefix + p.location);
                String key = p2.ruleId + "\u0000" + p2.location;
                if (seen.contains(key)) continue;
                seen.add(key);
                problems.add(p2);
            }
        }
        int threshold = "warning".equals(severityAtLeast) ? 0 : 1;
        List<ValidationProblem> out = new ArrayList<>();
        for (ValidationProblem p : problems) {
            int lvl = "warning".equals(p.severity) ? 0 : 1;
            if (lvl >= threshold) out.add(p);
        }
        return out;
    }

    public static final class ChildLoc {
        public final SedBase child;
        public final String locationPrefix;

        public ChildLoc(SedBase child, String locationPrefix) {
            this.child = child;
            this.locationPrefix = locationPrefix;
        }
    }

    /** [(child, "/jsonPointerSegment"), ...] - override per concrete class.
     * Default: none. */
    public List<ChildLoc> childrenWithLocations() { return Collections.emptyList(); }

    protected List<ValidationProblem> validateOwn() {
        // Extra/unrecognized properties (including bad-registered-namespace
        // keys), bad dict-of-discriminated-union keys, and item-dispatch
        // problems are all detected once, at load time, by
        // Dispatch.loadFields() - see Design.md's Schema-Pass Errors
        // section. This is the only reliable point to see genuinely-
        // unrecognized raw JSON keys, since they are never stored anywhere
        // in the object itself.
        List<ValidationProblem> problems = new ArrayList<>(loadProblems);
        ObjectNode instance = ownJsonValue();

        // _type const (only meaningful when this class is validated
        // directly, e.g. not through a discriminator that already
        // dispatched on it)
        if (typeConst() != null && typeRuleId() != null) {
            JsonNode tv = instance.get("_type");
            String actual = (tv == null || tv.isNull()) ? null : tv.asText();
            if (!typeConst().equals(actual)) {
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", "_type");
                ph.put("class", getClass().getSimpleName());
                ph.put("id", ownIdForMessage());
                ph.put("value", actual == null ? "null" : actual);
                ph.put("allowed", typeConst());
                problems.add(RuleCatalog.makeProblem(typeRuleId(), "/_type", ph));
            }
        }

        // universal name/description mixin (TestBaseFields/SEDBaseFields) -
        // not a per-class FieldSpec, so checked directly here against the
        // base mixin's own rule IDs (the same on every concrete class).
        if (nameNode != null && !LeafValidation.leafValueOk("string", nameNode, null, null, null)) {
            String rid = nameRuleId() != null ? nameRuleId() : baseCatchall();
            Map<String, Object> ph = new HashMap<>();
            ph.put("attr", "name");
            ph.put("class", getClass().getSimpleName());
            ph.put("id", ownIdForMessage());
            ph.put("value", nameNode.isTextual() ? nameNode.asText() : nameNode.toString());
            problems.add(RuleCatalog.makeProblem(rid, "/name", ph));
        }
        if (descriptionNode != null && !LeafValidation.leafValueOk("string", descriptionNode, null, null, null)) {
            String rid = descRuleId() != null ? descRuleId() : baseCatchall();
            Map<String, Object> ph = new HashMap<>();
            ph.put("attr", "description");
            ph.put("class", getClass().getSimpleName());
            ph.put("id", ownIdForMessage());
            ph.put("value", descriptionNode.isTextual() ? descriptionNode.asText() : descriptionNode.toString());
            problems.add(RuleCatalog.makeProblem(rid, "/description", ph));
        }

        List<FieldSpec> all = new ArrayList<>(fieldSpecs());
        for (List<FieldSpec> specs : namespaceFields().values()) all.addAll(specs);

        for (FieldSpec spec : all) {
            boolean present = instance.has(spec.name);
            if (spec.required && !present) {
                String rid = spec.requiredRuleId != null ? spec.requiredRuleId : spec.originCatchall;
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", spec.name);
                ph.put("class", getClass().getSimpleName());
                ph.put("id", ownIdForMessage());
                problems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                continue;
            }
            if (!present) continue;
            JsonNode value = instance.get(spec.name);
            if (LEAF_KINDS.contains(spec.kind)) {
                if (!LeafValidation.leafValueOk(spec.kind, value, spec.minimum, spec.exclusiveMinimum, spec.pattern)) {
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new HashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", getClass().getSimpleName());
                    ph.put("id", ownIdForMessage());
                    ph.put("value", value.isTextual() ? value.asText() : value.toString());
                    problems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                }
            }
        }
        return problems;
    }

    public String ownIdForMessage() { return "?"; }

    public abstract ObjectNode ownJsonValue();

    public Set<String> allowedKeys() {
        Set<String> keys = new HashSet<>();
        for (FieldSpec f : fieldSpecs()) keys.add(f.name);
        for (List<FieldSpec> specs : namespaceFields().values()) {
            for (FieldSpec f : specs) keys.add(f.name);
        }
        return keys;
    }

    public ObjectNode toJsonValue() { return ownJsonValue(); }
}

package org.sed2test;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.lang.ref.WeakReference;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
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
            "string", "integer", "number", "boolean", "SId", "SIdRef", "StringOrRef", "NumberOrRef",
            "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef"));
    // "any" is deliberately NOT a member: an AnyValueOrRef-typed field (any
    // JSON value) has no leafValueOk()-equivalent schema to check against -
    // its reference form is dispatched separately in validateOwn(), like
    // generator/emit_python.py's own LEAF_KINDS set and its _validate_own's
    // `elif spec.kind == "any"` branch.

    // Every LEAF_KINDS member whose value can structurally BE a reference (a
    // plain "string"/"integer"/etc. field's schema never admits one) - SIdRef
    // is always a reference, and every *OrRef kind's own anyOf includes one.
    protected static final Set<String> REFERENCE_CAPABLE_KINDS = new HashSet<>(List.of(
            "SIdRef", "StringOrRef", "NumberOrRef", "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef"));

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

    /** core-spec.md Section 8's per-class outputs.json envelope (the parsed
     * JSON) - non-null only for a concrete tasks/ class; read by the
     * shape-resolution rules SEDBase-0008 through -0015. */
    public JsonNode outputsJson() { return null; }

    /** True only on the generated document root class - gates the
     * whole-document checks (SEDDocument-0009 through -0011 and -0013), which
     * only make sense run once, from the document root. */
    public boolean isDocumentClass() { return false; }

    /** The newest document version this generator run's spec tree knows (the
     * document root class only; see SEDDocument-0011). */
    public String maxKnownDocumentVersion() { return null; }

    /** Every id-keyed collection field name THIS class declares (its "dict" and
     * "any-dict" fields) - used by ownIdForMessage() to search a PARENT's own
     * collections for `this`. */
    public List<String> idCollectionNames() { return Collections.emptyList(); }

    /** The id-keyed collection stored in field `fieldName` ("dict" or
     * "any-dict" kind), or null if this class has no such field - reference
     * resolution (References.getSedReference) walks the containment tree
     * through this. */
    public IdCollection getIdCollection(String fieldName) { return null; }

    /** The _type value this element carries (its class's const, or an unknown
     * holder's raw value), or null for a class without one. */
    public String typeValue() { return typeConst(); }

    /** The stored raw value of a plain leaf field, or null when unset. */
    public JsonNode valueNode(String name) { return values.get(name); }

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

    /** Backing store for an "any-dict"-kind field (an ID-keyed collection of
     * raw JSON values, never SedBase instances - e.g. SEDDocument.constants).
     * Overridden per generated concrete class, mirroring getDictCollection
     * above. */
    protected IdKeyedCollection<JsonNode> getAnyDictCollection(String fieldName) {
        throw new ApiError("no such any-dict field: " + fieldName);
    }

    /** Sets a "ref-class"/"ref-discriminator"-kind field's single nested
     * child (see generator/emit_java.py's _child_accessors_java) - used only
     * by Dispatch.loadFields, which constructs the child generically and
     * needs a way to store it back onto the right instance field without
     * knowing the concrete class. Overridden per generated concrete class. */
    protected void setChildField(String fieldName, SedBase child) {
        throw new ApiError("no such child field: " + fieldName);
    }

    // -- validate() engine --------------------------------------------------
    public List<ValidationProblem> validate() {
        return validate("warning");
    }

    public List<ValidationProblem> validate(String severityAtLeast) {
        try {
            return validateChecked(severityAtLeast);
        } finally {
            // parent/document backpointers are WeakReferences (see attach()),
            // so nothing else may keep the root alive while its own validate()
            // runs: the JIT is free to treat `this` as dead after its last use,
            // and a collection mid-validate would silently turn every
            // reference rule off ("no document to walk"). Python's refcounting
            // gives the caller's frame this guarantee for free.
            java.lang.ref.Reference.reachabilityFence(this);
        }
    }

    private List<ValidationProblem> validateChecked(String severityAtLeast) {
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
        String className = getClass().getSimpleName();
        String ownId = ownIdForMessage();

        // _type const (only meaningful when this class is validated
        // directly, e.g. not through a discriminator that already
        // dispatched on it)
        if (typeConst() != null && typeRuleId() != null) {
            JsonNode tv = instance.get("_type");
            boolean same = tv != null && tv.isTextual() && typeConst().equals(tv.textValue());
            if (!same) {
                problems.add(RuleCatalog.problem(typeRuleId(), "/_type", "attr", "_type", "class", className,
                        "id", ownId, "value", tv, "allowed", typeConst()));
            }
        }

        // universal name/description mixin (TestBaseFields/SEDBaseFields) -
        // not a per-class FieldSpec, so checked directly here against the
        // base mixin's own rule IDs (the same on every concrete class).
        if (nameNode != null && !LeafValidation.leafValueOk("string", nameNode, null, null, null)) {
            String rid = nameRuleId() != null ? nameRuleId() : baseCatchall();
            problems.add(RuleCatalog.problem(rid, "/name", "attr", "name", "class", className, "id", ownId,
                    "value", nameNode));
        }
        if (descriptionNode != null && !LeafValidation.leafValueOk("string", descriptionNode, null, null, null)) {
            String rid = descRuleId() != null ? descRuleId() : baseCatchall();
            problems.add(RuleCatalog.problem(rid, "/description", "attr", "description", "class", className,
                    "id", ownId, "value", descriptionNode));
        }

        List<FieldSpec> all = new ArrayList<>(fieldSpecs());
        for (List<FieldSpec> specs : namespaceFields().values()) all.addAll(specs);

        for (FieldSpec spec : all) {
            boolean present = instance.has(spec.name);
            if (spec.required && !present) {
                String rid = spec.requiredRuleId != null ? spec.requiredRuleId : spec.originCatchall;
                problems.add(RuleCatalog.problem(rid, "/" + spec.name, "attr", spec.name, "class", className,
                        "id", ownId));
                continue;
            }
            if (!present) continue;
            JsonNode value = instance.get(spec.name);
            if (LEAF_KINDS.contains(spec.kind)) {
                if (!LeafValidation.leafValueOk(spec.kind, value, spec.minimum, spec.exclusiveMinimum, spec.pattern,
                        spec.minLength, spec.enumValues)) {
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new LinkedHashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", className);
                    ph.put("id", ownId);
                    ph.put("value", value);
                    if (spec.enumValues != null) {
                        // A rule fired from an enum-constrained leaf's own
                        // message template may reference {allowed} (e.g.
                        // Curve-0002/Surface's own curveType/surfaceType
                        // rules) - harmless to always include, since
                        // formatMessage only substitutes placeholders the
                        // template actually names.
                        List<String> reprs = new ArrayList<>();
                        for (String v : spec.enumValues) reprs.add(PyFmt.reprStr(v));
                        ph.put("allowed", String.join(", ", reprs));
                    }
                    problems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                } else if (REFERENCE_CAPABLE_KINDS.contains(spec.kind) && References.isReference(value)) {
                    problems.addAll(References.checkReferenceField(
                            value.textValue(), getDocument(), className, ownId, spec.name, "/" + spec.name,
                            this, References.FieldInfo.of(spec)));
                } else if (spec.kind.equals("DictOrRef") && value.isObject()) {
                    // The dict-literal branch of a DictOrRef field (e.g.
                    // Repeat.outputVariableMap: an SId-keyed map of column
                    // name -> SIdRef) - References.isReference(value) above is
                    // false for this whole-field-is-a-dict shape, so each
                    // entry gets its OWN reference-resolution dispatch here
                    // (SEDBase-0005 through -0015, same as any other
                    // reference-capable field) rather than the field as a
                    // single unit. No ref-type rule id is passed: the field's
                    // own describes what the WHOLE FIELD must resolve to when
                    // IT is a reference, not what each entry's target must be.
                    Iterator<Map.Entry<String, JsonNode>> it = value.fields();
                    while (it.hasNext()) {
                        Map.Entry<String, JsonNode> e = it.next();
                        if (References.isReference(e.getValue())) {
                            problems.addAll(References.checkReferenceField(
                                    e.getValue().textValue(), getDocument(), className, ownId, spec.name,
                                    "/" + spec.name + "/" + e.getKey(), this,
                                    References.FieldInfo.bare(spec.kind)));
                        }
                    }
                } else if (spec.kind.equals("ArrayOrRef") && value.isArray()) {
                    // The array-literal branch of an ArrayOrRef field: each
                    // element that is itself a reference gets its own
                    // reference-resolution dispatch (SEDBase-0005.md: the rule
                    // applies to "an element of an array or object value"),
                    // with no per-element expected type - same scope as the
                    // DictOrRef dict-literal branch above.
                    for (int idx = 0; idx < value.size(); idx++) {
                        JsonNode el = value.get(idx);
                        if (References.isReference(el)) {
                            problems.addAll(References.checkReferenceField(
                                    el.textValue(), getDocument(), className, ownId, spec.name,
                                    "/" + spec.name + "/" + idx, this,
                                    References.FieldInfo.bare(spec.kind)));
                        }
                    }
                } else if (spec.isMath && value.isTextual()) {
                    // Types-0001..0004 (Design.md's Math section) - only for
                    // a literal string value that already passed its own
                    // leaf schema check above; a reference-form value of an
                    // OrRef math field is dispatched to the reference rules
                    // in the branch above instead.
                    problems.addAll(MathRules.checkMathField(
                            value.asText(), className, ownId, spec.name, "/" + spec.name));
                }
            } else if (spec.kind.equals("any") && References.isReference(value)) {
                // A scalar AnyValueOrRef field (e.g. LoopVariable.initialValue,
                // AggregationCalculation.input) isn't in LEAF_KINDS - "any JSON
                // value" has no leafValueOk() schema to check against - but an
                // SIdRef string may still substitute for it, so it needs the
                // same reference-resolution dispatch as every *OrRef-kind
                // field above.
                problems.addAll(References.checkReferenceField(
                        value.textValue(), getDocument(), className, ownId, spec.name, "/" + spec.name,
                        this, References.FieldInfo.bare("any")));
            }
        }
        if (isDocumentClass()) {
            problems.addAll(References.checkNamespaceUsageAndVersion(this));
            problems.addAll(References.checkConstantsOrdering(this));
        }
        // Repeat-0008/-0009/-0010 (own-subTasks scoping for a Repeat-family
        // instance's outputVariableMap/aggregateOutputVariables) and
        // LoopVariable-0004 (own-Loop scoping for subsequentValues) each
        // internally no-op for every class they don't apply to (a cheap
        // class-shape check, not a class-name check) - called unconditionally
        // here, the same as every other per-instance handwritten check above.
        problems.addAll(References.checkRepeatOwnChildren(this));
        problems.addAll(References.checkLoopVariableScope(this));
        return problems;
    }

    /** This element's own SId, for a validation message's {id} placeholder -
     * Design.md's Classes section: id is implicit, the key under which an
     * element is stored in its owning collection, never a field on the
     * element itself. So this walks up to the parent and searches every
     * id-keyed collection IT declares for whichever key maps to `this`.
     * Falls back to "?" for anything genuinely id-less: the document root, an
     * array-item class stored positionally rather than by id, or an
     * unattached/standalone instance no parent has claimed yet. */
    public String ownIdForMessage() {
        SedBase parent = getParent();
        if (parent == null) return "?";
        for (String name : parent.idCollectionNames()) {
            IdCollection coll = parent.getIdCollection(name);
            if (coll == null) continue;
            for (String iid : coll.ids()) {
                if (coll.getObject(iid) == this) return iid;
            }
        }
        return "?";
    }

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

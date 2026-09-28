"""Emit the generated Java target library from a SpecModel. Package name,
Maven groupId/artifactId are caller-supplied (see emit_java_package()) -
"org.sed2test"/"libsed2test" below are just the Phase-1 test-tree defaults.

Mirrors generator/emit_python.py's architecture and rule-mapping decisions
exactly (see that module's docstring and Design.md's Schema-Pass Errors /
Toolchain sections): validate() is a schema-pass rule-ID mapping, leaf
fields are checked against a tiny per-field JSON Schema fragment using the
language's own real validator library (networknt's json-schema-validator,
per Design.md's Toolchain mandate), and every load-time violation (extra
properties, bad dict-of-discriminated-union keys, bad container shapes,
dispatch problems bubbled up from a nested item) is detected once, at load
time, in Dispatch.loadFields - the only point that still has the raw JSON
before an unrecognized key is dropped.

Unlike the Python target, Java's static typing means there is no
kwargs-collision hazard equivalent to the `make_problem()` duplicate-
`location`-argument bug fixed in emit_python.py: RuleCatalog.makeProblem()
takes an explicit Map<String,Object> of placeholders, so this whole bug
class cannot arise here by construction.
"""
from __future__ import annotations

import os
from .spec import SpecModel, Field, FlatClass

PKG = "org.sed2test"  # default; emit_java_package() overrides this module-level
                      # value per invocation (see that function) so every
                      # helper below that reads PKG as a free variable picks
                      # up the caller's chosen package for that run.


def _java_ident(name: str) -> str:
    """Field/property name -> a Java identifier fragment usable in method
    names, e.g. 'acme@priority' -> 'acmePriority'. Plain field names in
    test-specsheets/ schemas are already camelCase (value, label,
    timeoutSeconds, ...), so they pass through unchanged."""
    if "@" in name:
        prefix, key = name.split("@", 1)
        key_ident = _java_ident(key)
        return prefix + key_ident[0:1].upper() + key_ident[1:]
    return name


def _cap(ident: str) -> str:
    return ident[0:1].upper() + ident[1:] if ident else ident


# ---------------------------------------------------------------------------
# Hand-authored runtime files (never regenerated per-spec beyond this
# function existing at all - one copy is emitted per generate.py run,
# identical for every spec, exactly like emit_python.py's RUNTIME string).
# ---------------------------------------------------------------------------

def _validation_problem_java() -> str:
    # Built lazily (called from runtime_files(), after emit_java_package()
    # has set the real PKG for this run) rather than as a module-level f-
    # string constant - see this module's PKG comment: an f-string baked at
    # import time freezes whatever PKG was at that moment ("org.sed2test"),
    # and reassigning the global later can't retroactively fix an already-
    # interpolated string. This was the root cause of ~48/56 real-spec
    # .java files shipping the wrong `package` line.
    return f'''package {PKG};

/** GENERATED - do not hand-edit; regenerate via generator/generate.py. */
public final class ValidationProblem {{
    public final String ruleId;
    public final String severity;
    public final String rule;
    public final String message;
    public final String location;

    public ValidationProblem(String ruleId, String severity, String rule, String message, String location) {{
        this.ruleId = ruleId;
        this.severity = severity;
        this.rule = rule;
        this.message = message;
        this.location = location;
    }}

    public String getRuleId() {{ return ruleId; }}
    public String getSeverity() {{ return severity; }}
    public String getRule() {{ return rule; }}
    public String getMessage() {{ return message; }}
    public String getLocation() {{ return location; }}

    @Override
    public String toString() {{
        return "ValidationProblem(" + ruleId + ", " + severity + ", " + location + ")";
    }}

    @Override
    public boolean equals(Object o) {{
        if (!(o instanceof ValidationProblem)) return false;
        ValidationProblem p = (ValidationProblem) o;
        return ruleId.equals(p.ruleId) && location.equals(p.location);
    }}

    @Override
    public int hashCode() {{
        return ruleId.hashCode() * 31 + location.hashCode();
    }}
}}
'''

def _api_error_java() -> str:
    return f'''package {PKG};

/** Raised for any misuse of the generated API itself (wrong-kind OrRef
 * access, get on an unset field, an out-of-range insert, ...) - never for
 * a document that merely fails a SED2 validation rule. See Design.md's
 * Classes section. GENERATED - do not hand-edit. */
public class ApiError extends RuntimeException {{
    public ApiError(String message) {{ super(message); }}
}}
'''

def _field_spec_java() -> str:
    return f'''package {PKG};

/** GENERATED - do not hand-edit; regenerate via generator/generate.py. */
public final class FieldSpec {{
    public final String name;
    public final String kind;
    public final boolean required;
    public final String ruleId;            // nullable
    public final String requiredRuleId;    // nullable
    public final String originCatchall;
    public final Double minimum;           // nullable
    public final Double exclusiveMinimum;  // nullable
    public final String pattern;           // nullable
    public final String itemClass;         // nullable
    public final String itemDiscriminator; // nullable

    public FieldSpec(String name, String kind, boolean required, String ruleId, String requiredRuleId,
                      String originCatchall, Double minimum, Double exclusiveMinimum, String pattern,
                      String itemClass, String itemDiscriminator) {{
        this.name = name;
        this.kind = kind;
        this.required = required;
        this.ruleId = ruleId;
        this.requiredRuleId = requiredRuleId;
        this.originCatchall = originCatchall;
        this.minimum = minimum;
        this.exclusiveMinimum = exclusiveMinimum;
        this.pattern = pattern;
        this.itemClass = itemClass;
        this.itemDiscriminator = itemDiscriminator;
    }}
}}
'''

def _rule_catalog_java() -> str:
    return f'''package {PKG};

import java.util.HashMap;
import java.util.Map;

/** Rule catalogue + ValidationProblem factory. GENERATED (this file) - do
 * not hand-edit; regenerate via generator/generate.py. Populated by
 * RulesData at class-init time: ruleId -> (rule text, message template,
 * severity). Unlike the Python target's make_problem(), this takes an
 * explicit Map of placeholders rather than **kwargs, so there is no
 * possible collision with the `location` parameter - see this module's
 * docstring in generator/emit_java.py. */
public final class RuleCatalog {{
    public static final class Entry {{
        public final String rule;
        public final String messageTemplate;
        public final String severity;

        public Entry(String rule, String messageTemplate, String severity) {{
            this.rule = rule;
            this.messageTemplate = messageTemplate;
            this.severity = severity;
        }}
    }}

    public static final Map<String, Entry> CATALOG = new HashMap<>();

    private RuleCatalog() {{}}

    public static Entry get(String ruleId) {{
        Entry e = CATALOG.get(ruleId);
        return e != null ? e : new Entry("", "{{schema-message}}", "error");
    }}

    public static String severityOf(String ruleId) {{
        return get(ruleId).severity;
    }}

    public static String formatMessage(String ruleId, String location, Map<String, Object> placeholders) {{
        String out = get(ruleId).messageTemplate;
        out = out.replace("{{location}}", String.valueOf(location));
        for (Map.Entry<String, Object> e : placeholders.entrySet()) {{
            out = out.replace("{{" + e.getKey() + "}}", String.valueOf(e.getValue()));
        }}
        return out;
    }}

    public static ValidationProblem makeProblem(String ruleId, String location, Map<String, Object> placeholders) {{
        Entry e = get(ruleId);
        return new ValidationProblem(ruleId, e.severity, e.rule, formatMessage(ruleId, location, placeholders), location);
    }}

    public static ValidationProblem makeProblem(String ruleId, String location) {{
        return makeProblem(ruleId, location, new HashMap<>());
    }}
}}
'''

def _leaf_validation_java() -> str:
    return f'''package {PKG};

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.networknt.schema.JsonSchema;
import com.networknt.schema.JsonSchemaFactory;
import com.networknt.schema.SpecVersion;

import java.util.Set;

/** Per-field leaf validation, via the real JSON Schema validator
 * (networknt's json-schema-validator, per Design.md's Toolchain mandate) -
 * a tiny schema fragment is built from one already-resolved field's own
 * type, never a whole-document schema, since every combinator has already
 * been resolved away by the generator at compose time (see
 * generator/spec.py). GENERATED - do not hand-edit. */
public final class LeafValidation {{
    private static final JsonSchemaFactory FACTORY =
            JsonSchemaFactory.getInstance(SpecVersion.VersionFlag.V202012);

    public static final String SID_PATTERN = "^[A-Za-z_][A-Za-z0-9_]*$";
    public static final String SIDREF_PATTERN = "^#.*$";

    private LeafValidation() {{}}

    private static ObjectNode baseSchema(String kind) {{
        ObjectNode n = JsonNodeFactory.instance.objectNode();
        switch (kind) {{
            case "string":
                n.put("type", "string");
                break;
            case "integer":
                n.put("type", "integer");
                break;
            case "number":
                n.put("type", "number");
                break;
            case "boolean":
                n.put("type", "boolean");
                break;
            case "SId":
                n.put("type", "string");
                n.put("pattern", SID_PATTERN);
                break;
            case "SIdRef":
                n.put("type", "string");
                n.put("pattern", SIDREF_PATTERN);
                break;
            case "StringOrRef": {{
                ArrayNode any = n.putArray("anyOf");
                ObjectNode s = JsonNodeFactory.instance.objectNode();
                s.put("type", "string");
                any.add(s);
                break;
            }}
            case "NumberOrRef": {{
                ArrayNode any = n.putArray("anyOf");
                ObjectNode num = JsonNodeFactory.instance.objectNode();
                num.put("type", "number");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(num);
                any.add(ref);
                break;
            }}
            case "IntegerOrRef": {{
                ArrayNode any = n.putArray("anyOf");
                ObjectNode val = JsonNodeFactory.instance.objectNode();
                val.put("type", "integer");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(val);
                any.add(ref);
                break;
            }}
            case "BooleanOrRef": {{
                ArrayNode any = n.putArray("anyOf");
                ObjectNode val = JsonNodeFactory.instance.objectNode();
                val.put("type", "boolean");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(val);
                any.add(ref);
                break;
            }}
            case "ArrayOrRef": {{
                ArrayNode any = n.putArray("anyOf");
                ObjectNode val = JsonNodeFactory.instance.objectNode();
                val.put("type", "array");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(val);
                any.add(ref);
                break;
            }}
            case "DictOrRef": {{
                ArrayNode any = n.putArray("anyOf");
                ObjectNode val = JsonNodeFactory.instance.objectNode();
                val.put("type", "object");
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(val);
                any.add(ref);
                break;
            }}
            default:
                throw new IllegalArgumentException("unknown leaf kind: " + kind);
        }}
        return n;
    }}

    public static boolean leafValueOk(String kind, JsonNode value, Double minimum, Double exclusiveMinimum, String pattern) {{
        ObjectNode schema = baseSchema(kind);
        if (minimum != null) schema.put("minimum", minimum);
        if (exclusiveMinimum != null) schema.put("exclusiveMinimum", exclusiveMinimum);
        if (pattern != null && "string".equals(kind)) schema.put("pattern", pattern);
        JsonSchema s = FACTORY.getSchema(schema);
        Set<?> errors = s.validate(value);
        return errors.isEmpty();
    }}

    public static boolean isSId(String s) {{
        return s != null && s.matches(SID_PATTERN);
    }}
}}
'''

def _id_keyed_collection_java() -> str:
    return f'''package {PKG};

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** Backing store for an ID-keyed dict-of-discriminated-union field
 * (TestDocument.widgets/.reports, FancyWidget.choices) - insertion order
 * preserved, add-/remove-/insert-/rename (setId) per Design.md's Classes
 * section. Deliberately unbounded (not "T extends SedBase"): none of this
 * class's own methods call any SedBase-specific behavior, and an
 * "any-dict"-kind field (see generator/emit_java.py's emit_model_java_files)
 * reuses this same collection to hold raw JsonNode values instead of
 * SedBase instances - see generator/emit_python.py's _collection_accessors
 * any-dict branch for the reference implementation this mirrors.
 * GENERATED - do not hand-edit. */
public final class IdKeyedCollection<T> {{
    private final List<String> order = new ArrayList<>();
    private final Map<String, T> items = new LinkedHashMap<>();

    public List<String> ids() {{ return new ArrayList<>(order); }}

    public T get(String itemId) {{
        if (!items.containsKey(itemId)) throw new ApiError("no entry with id " + itemId);
        return items.get(itemId);
    }}

    public void add(String itemId, T obj) {{
        if (items.containsKey(itemId)) throw new ApiError("an entry with id " + itemId + " already exists");
        order.add(itemId);
        items.put(itemId, obj);
    }}

    public void insert(int index, String itemId, T obj) {{
        if (items.containsKey(itemId)) throw new ApiError("an entry with id " + itemId + " already exists");
        if (index < 0 || index > order.size()) throw new ApiError("index " + index + " out of range");
        order.add(index, itemId);
        items.put(itemId, obj);
    }}

    public void remove(String itemId) {{
        if (!items.containsKey(itemId)) throw new ApiError("no entry with id " + itemId);
        order.remove(itemId);
        items.remove(itemId);
    }}

    public void setId(String oldId, String newId) {{
        if (!items.containsKey(oldId)) throw new ApiError("no entry with id " + oldId);
        if (items.containsKey(newId) && !newId.equals(oldId)) {{
            throw new ApiError("an entry with id " + newId + " already exists");
        }}
        int idx = order.indexOf(oldId);
        order.set(idx, newId);
        T v = items.remove(oldId);
        items.put(newId, v);
    }}

    public int size() {{ return order.size(); }}
}}
'''

def _list_collection_java() -> str:
    return f'''package {PKG};

import java.util.ArrayList;
import java.util.List;

/** Backing store for a plain (non-ID-keyed) array-of-embedded-object
 * field, e.g. WidgetOptions.notes: add- (append), remove- (by index),
 * insert- (at index). GENERATED - do not hand-edit. */
public final class ListCollection<T extends SedBase> {{
    private final List<T> items = new ArrayList<>();

    public List<T> items() {{ return new ArrayList<>(items); }}

    public void add(T obj) {{ items.add(obj); }}

    public void insert(int index, T obj) {{
        if (index < 0 || index > items.size()) throw new ApiError("index " + index + " out of range");
        items.add(index, obj);
    }}

    public void remove(int index) {{
        if (index < 0 || index >= items.size()) throw new ApiError("index " + index + " out of range");
        items.remove(index);
    }}

    public int size() {{ return items.size(); }}
}}
'''

def _sed_base_java() -> str:
    return f'''package {PKG};

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
public abstract class SedBase {{
    public static final Pattern NAMESPACE_KEY_PATTERN =
            Pattern.compile("^([A-Za-z_][A-Za-z0-9_]*)@([A-Za-z_][A-Za-z0-9_]*)$");

    protected static final Set<String> LEAF_KINDS = new HashSet<>(List.of(
            "string", "integer", "number", "boolean", "SId", "SIdRef", "StringOrRef", "NumberOrRef",
            "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef"));
    // "any" is deliberately NOT a member: an AnyValueOrRef-typed field (any
    // JSON value) has no leaf_value_ok()-equivalent schema to check against
    // - see generator/emit_python.py's own LEAF_KINDS set and its
    // _validate_own's `elif spec.kind == "any"` branch (whose reference-
    // resolution dispatch this Java port deliberately does not carry over -
    // see Design.md's Testing section on Phase 2 scope).

    // -- per-concrete-class metadata, overridden by generated subclasses --
    public List<FieldSpec> fieldSpecs() {{ return Collections.emptyList(); }}
    public Set<String> requiredNames() {{ return Collections.emptySet(); }}
    public String typeConst() {{ return null; }}
    public String typeRuleId() {{ return null; }}
    public String ownCatchall() {{ return ""; }}
    public Map<String, List<FieldSpec>> namespaceFields() {{ return Collections.emptyMap(); }}
    public Map<String, String> namespaceCatchall() {{ return Collections.emptyMap(); }}
    public Set<String> knownNamespacePrefixes() {{ return Collections.emptySet(); }}
    public String nameRuleId() {{ return null; }}
    public String descRuleId() {{ return null; }}
    public String baseCatchall() {{ return ""; }}

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
    public SedBase getParent() {{ return parentRef == null ? null : parentRef.get(); }}

    public SedBase getDocument() {{ return documentRef == null ? null : documentRef.get(); }}

    public void attach(SedBase parent, SedBase document) {{
        this.parentRef = parent == null ? null : new WeakReference<>(parent);
        this.documentRef = document == null ? null : new WeakReference<>(document);
        for (SedBase child : children()) {{
            child.attach(this, document);
        }}
    }}

    /** Every SedBase-derived child reachable from this element, for
     * backpointer propagation and validate() recursion. */
    public List<SedBase> children() {{ return Collections.emptyList(); }}

    // -- universal name/description (TestBaseFields) --
    // Stored as the raw JsonNode (not a coerced String) so a wrong-typed
    // incoming value (e.g. a JSON number for `name`) is preserved for the
    // leaf-type check in validateOwn() instead of being silently
    // stringified away - see generator/emit_java.py's Dispatch.loadFields.
    public String getName() {{
        if (nameNode == null) throw new ApiError("name is not set");
        return nameNode.asText();
    }}

    public boolean isSetName() {{ return nameNode != null; }}

    public void setName(String value) {{ this.nameNode = value == null ? null : com.fasterxml.jackson.databind.node.TextNode.valueOf(value); }}

    public void unsetName() {{ this.nameNode = null; }}

    public String getDescription() {{
        if (descriptionNode == null) throw new ApiError("description is not set");
        return descriptionNode.asText();
    }}

    public boolean isSetDescription() {{ return descriptionNode != null; }}

    public void setDescription(String value) {{ this.descriptionNode = value == null ? null : com.fasterxml.jackson.databind.node.TextNode.valueOf(value); }}

    public void unsetDescription() {{ this.descriptionNode = null; }}

    // -- generic namespace attribute store (Design.md's Namespaces section) --
    public JsonNode getNamespaceAttribute(String prefix, String key) {{
        String k = prefix + "@" + key;
        if (!nsAttrs.containsKey(k)) throw new ApiError("namespace attribute " + k + " is not set");
        return nsAttrs.get(k);
    }}

    public void setNamespaceAttribute(String prefix, String key, JsonNode value) {{
        nsAttrs.put(prefix + "@" + key, value);
    }}

    public boolean isSetNamespaceAttribute(String prefix, String key) {{
        return nsAttrs.containsKey(prefix + "@" + key);
    }}

    public void unsetNamespaceAttribute(String prefix, String key) {{
        nsAttrs.remove(prefix + "@" + key);
    }}

    // -- generic OrRef-shaped storage helpers, used by generated accessors --
    protected JsonNode getOrRefValueNode(String name) {{
        if (!values.containsKey(name)) throw new ApiError(name + " is not set");
        if (Boolean.TRUE.equals(orRefIsRef.get(name))) throw new ApiError(name + " holds a reference, not a literal value");
        return values.get(name);
    }}

    protected JsonNode getOrRefRefNode(String name) {{
        if (!values.containsKey(name)) throw new ApiError(name + " is not set");
        if (!Boolean.TRUE.equals(orRefIsRef.get(name))) throw new ApiError(name + " holds a literal value, not a reference");
        return values.get(name);
    }}

    protected void setOrRefValueNode(String name, JsonNode value) {{
        values.put(name, value);
        orRefIsRef.put(name, false);
    }}

    protected void setOrRefRefNode(String name, String ref) {{
        if (!isReference(ref)) throw new ApiError("'" + ref + "' is not a valid reference (must start with '#')");
        values.put(name, com.fasterxml.jackson.databind.node.TextNode.valueOf(ref));
        orRefIsRef.put(name, true);
    }}

    protected boolean isOrRefRef(String name) {{
        if (!values.containsKey(name)) throw new ApiError(name + " is not set");
        return Boolean.TRUE.equals(orRefIsRef.get(name));
    }}

    public static boolean isReference(String value) {{
        return value != null && value.startsWith("#");
    }}

    // -- collection field access (overridden per generated concrete class,
    // mirroring the Python target's getattr(obj, '_' + pyname(name))) --
    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {{
        throw new ApiError("no such dict field: " + fieldName);
    }}

    protected ListCollection<SedBase> getListCollection(String fieldName) {{
        throw new ApiError("no such list field: " + fieldName);
    }}

    /** Backing store for an "any-dict"-kind field (an ID-keyed collection of
     * raw JSON values, never SedBase instances - e.g. SEDDocument.constants).
     * Overridden per generated concrete class, mirroring getDictCollection
     * above. */
    protected IdKeyedCollection<JsonNode> getAnyDictCollection(String fieldName) {{
        throw new ApiError("no such any-dict field: " + fieldName);
    }}

    /** Sets a "ref-class"/"ref-discriminator"-kind field's single nested
     * child (see generator/emit_java.py's _child_accessors_java) - used only
     * by Dispatch.loadFields, which constructs the child generically and
     * needs a way to store it back onto the right instance field without
     * knowing the concrete class. Overridden per generated concrete class. */
    protected void setChildField(String fieldName, SedBase child) {{
        throw new ApiError("no such child field: " + fieldName);
    }}

    // -- validate() engine --------------------------------------------------
    public List<ValidationProblem> validate() {{
        return validate("warning");
    }}

    public List<ValidationProblem> validate(String severityAtLeast) {{
        List<ValidationProblem> problems = new ArrayList<>(validateOwn());
        Set<String> seen = new HashSet<>();
        for (ValidationProblem p : problems) seen.add(p.ruleId + "\\u0000" + p.location);
        for (ChildLoc cl : childrenWithLocations()) {{
            for (ValidationProblem p : cl.child.validate("warning")) {{
                ValidationProblem p2 = new ValidationProblem(
                        p.ruleId, p.severity, p.rule, p.message, cl.locationPrefix + p.location);
                String key = p2.ruleId + "\\u0000" + p2.location;
                if (seen.contains(key)) continue;
                seen.add(key);
                problems.add(p2);
            }}
        }}
        int threshold = "warning".equals(severityAtLeast) ? 0 : 1;
        List<ValidationProblem> out = new ArrayList<>();
        for (ValidationProblem p : problems) {{
            int lvl = "warning".equals(p.severity) ? 0 : 1;
            if (lvl >= threshold) out.add(p);
        }}
        return out;
    }}

    public static final class ChildLoc {{
        public final SedBase child;
        public final String locationPrefix;

        public ChildLoc(SedBase child, String locationPrefix) {{
            this.child = child;
            this.locationPrefix = locationPrefix;
        }}
    }}

    /** [(child, "/jsonPointerSegment"), ...] - override per concrete class.
     * Default: none. */
    public List<ChildLoc> childrenWithLocations() {{ return Collections.emptyList(); }}

    protected List<ValidationProblem> validateOwn() {{
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
        if (typeConst() != null && typeRuleId() != null) {{
            JsonNode tv = instance.get("_type");
            String actual = (tv == null || tv.isNull()) ? null : tv.asText();
            if (!typeConst().equals(actual)) {{
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", "_type");
                ph.put("class", getClass().getSimpleName());
                ph.put("id", ownIdForMessage());
                ph.put("value", actual == null ? "null" : actual);
                ph.put("allowed", typeConst());
                problems.add(RuleCatalog.makeProblem(typeRuleId(), "/_type", ph));
            }}
        }}

        // universal name/description mixin (TestBaseFields/SEDBaseFields) -
        // not a per-class FieldSpec, so checked directly here against the
        // base mixin's own rule IDs (the same on every concrete class).
        if (nameNode != null && !LeafValidation.leafValueOk("string", nameNode, null, null, null)) {{
            String rid = nameRuleId() != null ? nameRuleId() : baseCatchall();
            Map<String, Object> ph = new HashMap<>();
            ph.put("attr", "name");
            ph.put("class", getClass().getSimpleName());
            ph.put("id", ownIdForMessage());
            ph.put("value", nameNode.isTextual() ? nameNode.asText() : nameNode.toString());
            problems.add(RuleCatalog.makeProblem(rid, "/name", ph));
        }}
        if (descriptionNode != null && !LeafValidation.leafValueOk("string", descriptionNode, null, null, null)) {{
            String rid = descRuleId() != null ? descRuleId() : baseCatchall();
            Map<String, Object> ph = new HashMap<>();
            ph.put("attr", "description");
            ph.put("class", getClass().getSimpleName());
            ph.put("id", ownIdForMessage());
            ph.put("value", descriptionNode.isTextual() ? descriptionNode.asText() : descriptionNode.toString());
            problems.add(RuleCatalog.makeProblem(rid, "/description", ph));
        }}

        List<FieldSpec> all = new ArrayList<>(fieldSpecs());
        for (List<FieldSpec> specs : namespaceFields().values()) all.addAll(specs);

        for (FieldSpec spec : all) {{
            boolean present = instance.has(spec.name);
            if (spec.required && !present) {{
                String rid = spec.requiredRuleId != null ? spec.requiredRuleId : spec.originCatchall;
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", spec.name);
                ph.put("class", getClass().getSimpleName());
                ph.put("id", ownIdForMessage());
                problems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                continue;
            }}
            if (!present) continue;
            JsonNode value = instance.get(spec.name);
            if (LEAF_KINDS.contains(spec.kind)) {{
                if (!LeafValidation.leafValueOk(spec.kind, value, spec.minimum, spec.exclusiveMinimum, spec.pattern)) {{
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new HashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", getClass().getSimpleName());
                    ph.put("id", ownIdForMessage());
                    ph.put("value", value.isTextual() ? value.asText() : value.toString());
                    problems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                }}
            }}
        }}
        return problems;
    }}

    public String ownIdForMessage() {{ return "?"; }}

    public abstract ObjectNode ownJsonValue();

    public Set<String> allowedKeys() {{
        Set<String> keys = new HashSet<>();
        for (FieldSpec f : fieldSpecs()) keys.add(f.name);
        for (List<FieldSpec> specs : namespaceFields().values()) {{
            for (FieldSpec f : specs) keys.add(f.name);
        }}
        return keys;
    }}

    public ObjectNode toJsonValue() {{ return ownJsonValue(); }}
}}
'''


def runtime_files() -> dict:
    return {
        "ValidationProblem.java": _validation_problem_java(),
        "ApiError.java": _api_error_java(),
        "FieldSpec.java": _field_spec_java(),
        "RuleCatalog.java": _rule_catalog_java(),
        "LeafValidation.java": _leaf_validation_java(),
        "IdKeyedCollection.java": _id_keyed_collection_java(),
        "ListCollection.java": _list_collection_java(),
        "SedBase.java": _sed_base_java(),
    }


# ---------------------------------------------------------------------------
# Per-spec generated files: model classes, Unknown holders, Dispatch.java,
# RulesData.java, Io.java.
# ---------------------------------------------------------------------------
import json as _json


def _java_lit(s) -> str:
    """None -> Java `null`; else a Java string literal. json.dumps produces
    double-quoted, backslash-escaped text that is also valid Java source."""
    return "null" if s is None else _json.dumps(s)


def _java_double_lit(v) -> str:
    return "null" if v is None else repr(float(v))


def _field_spec_expr(f: Field) -> str:
    t = f.type
    return (
        f"new FieldSpec({_java_lit(f.name)}, {_java_lit(t.kind)}, {str(f.required).lower()}, "
        f"{_java_lit(f.rule_id)}, {_java_lit(f.required_rule_id)}, {_java_lit(f.origin_class + '-0000')}, "
        f"{_java_double_lit(t.minimum)}, {_java_double_lit(t.exclusive_minimum)}, {_java_lit(t.pattern)}, "
        f"{_java_lit(t.item_class)}, {_java_lit(t.item_discriminator)})"
    )


# The full OrRef family (Design.md's Validation section / core/Types) -
# StringOrRef/NumberOrRef were the only two the Phase-1 test-specsheets/
# vocabulary exercised; the real spec (specsheets/) also uses the other
# four. Every one of these gets the same six get-/set-/is-Ref-/isSet-/
# unset- accessors, generic OrRef storage (getOrRefValueNode/
# setOrRefValueNode/... in SedBase.java), differing only in the natural
# Java type on the value side - ArrayOrRef/DictOrRef have no better native
# Java collection representation than the raw JsonNode itself without a lot
# more work outside this port's scope (Design.md's Phase 2 scope note),
# so their "value" is the JsonNode as-is, same treatment as "any" below.
_ORREF_KINDS_JAVA = ("StringOrRef", "NumberOrRef", "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef")

# Every kind emit_model_java_files treats as a "leaf" field (own FIELD_SPECS
# entry + a get-/set-/isSet-/unset()-shaped accessor stored directly in
# `values`) - mirrors emit_python.py's emit_model_py leaf_fields
# classification (_ORREF_KINDS + ("string", "integer", ... , "any")).
_LEAF_KINDS_JAVA = _ORREF_KINDS_JAVA + ("string", "integer", "number", "boolean", "SId", "SIdRef", "any")

# kind -> (java value type, get-conversion suffix ("" = no conversion, the
# JsonNode itself), set-time wrap expression turning a `value` of that java
# type into a JsonNode).
_ORREF_JAVA_TYPES = {
    "StringOrRef": ("String", ".asText()", "value == null ? NullNode.getInstance() : TextNode.valueOf(value)"),
    "NumberOrRef": ("double", ".asDouble()", "DoubleNode.valueOf(value)"),
    "IntegerOrRef": ("long", ".asLong()", "LongNode.valueOf(value)"),
    "BooleanOrRef": ("boolean", ".asBoolean()", "BooleanNode.valueOf(value)"),
    "ArrayOrRef": ("JsonNode", "", "value"),
    "DictOrRef": ("JsonNode", "", "value"),
}


def _leaf_java_type(kind: str) -> str:
    return {"string": "String", "SId": "String", "SIdRef": "String",
            "integer": "long", "number": "double", "boolean": "boolean"}[kind]


def _leaf_accessors_java(f: Field) -> str:
    ident = _java_ident(f.name)
    cap = _cap(ident)
    kind = f.type.kind
    name_lit = _java_lit(f.name)
    lines = []
    if kind in _ORREF_KINDS_JAVA:
        java_t, get_expr, set_wrap = _ORREF_JAVA_TYPES[kind]
        get_body = f"getOrRefValueNode({name_lit}){get_expr}"
        lines.append(f"    public {java_t} get{cap}Value() {{ return {get_body}; }}")
        lines.append(f"    public String get{cap}Ref() {{ return getOrRefRefNode({name_lit}).asText(); }}")
        lines.append(f"    public void set{cap}Value({java_t} value) {{ setOrRefValueNode({name_lit}, {set_wrap}); }}")
        lines.append(f"    public void set{cap}Ref(String ref) {{ setOrRefRefNode({name_lit}, ref); }}")
        lines.append(f"    public boolean is{cap}Ref() {{ return isOrRefRef({name_lit}); }}")
        lines.append(f"    public boolean isSet{cap}() {{ return values.containsKey({name_lit}); }}")
        lines.append(f"    public void unset{cap}() {{ values.remove({name_lit}); orRefIsRef.remove({name_lit}); }}")
    elif kind == "any":
        # AnyValueOrRef: no fixed shape, so no type conversion either way -
        # the raw JsonNode is both the getter's return type and the
        # setter's parameter type. Mirrors emit_python.py's plain (non-
        # OrRef) accessor shape for this kind (see that module's
        # emit_model_py leaf_fields classification, which folds "any" in
        # alongside string/integer/... rather than treating it as its own
        # thing) - "any" is deliberately absent from LEAF_KINDS above, so
        # this accessor's stored value is never schema-checked in
        # validateOwn(), only checked for required-ness.
        lines.append(f"    public JsonNode get{cap}() {{ if (!values.containsKey({name_lit})) throw new ApiError({name_lit} + \" is not set\"); return values.get({name_lit}); }}")
        lines.append(f"    public void set{cap}(JsonNode value) {{ values.put({name_lit}, value); }}")
        lines.append(f"    public boolean isSet{cap}() {{ return values.containsKey({name_lit}); }}")
        lines.append(f"    public void unset{cap}() {{ values.remove({name_lit}); }}")
    else:
        java_t = _leaf_java_type(kind)
        if java_t == "String":
            get_expr, set_wrap = ".asText()", "value == null ? NullNode.getInstance() : TextNode.valueOf(value)"
        elif java_t == "long":
            get_expr, set_wrap = ".asLong()", "LongNode.valueOf(value)"
        elif java_t == "double":
            get_expr, set_wrap = ".asDouble()", "DoubleNode.valueOf(value)"
        else:
            get_expr, set_wrap = ".asBoolean()", "BooleanNode.valueOf(value)"
        lines.append(f"    public {java_t} get{cap}() {{ if (!values.containsKey({name_lit})) throw new ApiError({name_lit} + \" is not set\"); return values.get({name_lit}){get_expr}; }}")
        lines.append(f"    public void set{cap}({java_t} value) {{ values.put({name_lit}, {set_wrap}); }}")
        lines.append(f"    public boolean isSet{cap}() {{ return values.containsKey({name_lit}); }}")
        lines.append(f"    public void unset{cap}() {{ values.remove({name_lit}); }}")
    return "\n".join(lines) + "\n"


def _child_accessors_java(f: Field) -> str:
    """A single nested SedBase-derived child, stored directly on the
    instance (a private field), not in an IdKeyedCollection/ListCollection -
    there is exactly zero or one of it, and it has no id of its own. Covers
    both "ref-class" (a fixed target class) and "ref-discriminator" (a
    _type-dispatched target) - the accessors don't care which; only
    Dispatch.loadFields's own parsing needs to tell them apart (see
    generator/emit_python.py's _child_accessors, the reference
    implementation this mirrors)."""
    ident = _java_ident(f.name)
    cap = _cap(ident)
    name_lit = _java_lit(f.name)
    lines = []
    lines.append(f"    public SedBase get{cap}() {{ if ({ident} == null) throw new ApiError({name_lit} + \" is not set\"); return {ident}; }}")
    lines.append(f"    public void set{cap}(SedBase obj) {{ {ident} = obj; obj.attach(this, getDocument()); }}")
    lines.append(f"    public boolean isSet{cap}() {{ return {ident} != null; }}")
    lines.append(f"    public void unset{cap}() {{ {ident} = null; }}")
    return "\n".join(lines) + "\n"


def _collection_field_decl_java(f: Field) -> str:
    ident = _java_ident(f.name)
    if f.type.kind == "dict":
        return f"    private final IdKeyedCollection<SedBase> {ident} = new IdKeyedCollection<>();\n"
    if f.type.kind == "any-dict":
        return f"    private final IdKeyedCollection<JsonNode> {ident} = new IdKeyedCollection<>();\n"
    return f"    private final ListCollection<SedBase> {ident} = new ListCollection<>();\n"


def _collection_accessors_java(f: Field) -> str:
    ident = _java_ident(f.name)
    cap = _cap(ident)
    lines = []
    if f.type.kind == "dict":
        lines.append(f"    public List<String> get{cap}() {{ return {ident}.ids(); }}")
        lines.append(f"    public SedBase get{cap}Item(String itemId) {{ return {ident}.get(itemId); }}")
        lines.append(f"    public void add{cap}(String itemId, SedBase obj) {{ {ident}.add(itemId, obj); obj.attach(this, getDocument()); }}")
        lines.append(f"    public void insert{cap}(int index, String itemId, SedBase obj) {{ {ident}.insert(index, itemId, obj); obj.attach(this, getDocument()); }}")
        lines.append(f"    public void remove{cap}(String itemId) {{ {ident}.remove(itemId); }}")
        lines.append(f"    public void setIdOn{cap}(String oldId, String newId) {{ {ident}.setId(oldId, newId); }}")
    elif f.type.kind == "any-dict":
        # Same ID-keyed collection shape as "dict", but items are raw
        # JsonNode values, never SedBase instances - so no .attach() call
        # (SEDDocument.constants today; mirrors emit_python.py's
        # _collection_accessors any-dict branch).
        lines.append(f"    public List<String> get{cap}() {{ return {ident}.ids(); }}")
        lines.append(f"    public JsonNode get{cap}Item(String itemId) {{ return {ident}.get(itemId); }}")
        lines.append(f"    public void add{cap}(String itemId, JsonNode value) {{ {ident}.add(itemId, value); }}")
        lines.append(f"    public void insert{cap}(int index, String itemId, JsonNode value) {{ {ident}.insert(index, itemId, value); }}")
        lines.append(f"    public void remove{cap}(String itemId) {{ {ident}.remove(itemId); }}")
        lines.append(f"    public void setIdOn{cap}(String oldId, String newId) {{ {ident}.setId(oldId, newId); }}")
    else:
        lines.append(f"    public List<SedBase> get{cap}() {{ return {ident}.items(); }}")
        lines.append(f"    public void add{cap}(SedBase obj) {{ {ident}.add(obj); obj.attach(this, getDocument()); }}")
        lines.append(f"    public void insert{cap}(int index, SedBase obj) {{ {ident}.insert(index, obj); obj.attach(this, getDocument()); }}")
        lines.append(f"    public void remove{cap}(int index) {{ {ident}.remove(index); }}")
    return "\n".join(lines) + "\n"


def _model_file_imports() -> str:
    # Same lazy-evaluation fix as the runtime-file builders above - this is
    # what every generated model class (SEDDocument.java, Plot2D.java, ...)
    # opens with, so it accounted for the bulk of the ~48 wrongly-packaged
    # files.
    return f'''package {PKG};

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

'''


def emit_model_java_files(model: SpecModel) -> dict:
    """One .java file per generatable class - Java requires a public
    top-level class's filename to match its name, unlike Python's single
    model.py module (see generator/emit_python.py's emit_model_py())."""
    files = {}
    base = model.base_mixin
    base_fields = model.classes[base].fields if base in model.classes else []
    base_name_rule_id = next((f.rule_id for f in base_fields if f.name == "name"), None)
    base_desc_rule_id = next((f.rule_id for f in base_fields if f.name == "description"), None)
    base_catchall = model.classes[base].own_catchall if base in model.classes else ""

    for name in model.generatable_classes():
        c = model.classes[name]
        # Mirrors emit_python.py's own_fields filter exactly: excludes ONLY
        # name/description when they originate from the base mixin (every
        # concrete class handles those two via the dedicated nameNode/
        # descriptionNode fields on SedBase itself, never a FieldSpec) -
        # NOT every base-origin field. The base mixin (SEDBase/TestBase)
        # also declares "notes"/"annotations" in the real spec (TestBase
        # happens to declare only name/description, which is why this
        # distinction was invisible under test-specsheets/ alone) and those
        # must still get their own FieldSpec/accessor like any other field -
        # the previous `f.origin_class != base` filter silently dropped
        # them entirely, which is what caused this module's own investigation
        # into Task #28 to trace two Annotation fixture failures back here:
        # a SEDDocument.annotations value was rejected as an unrecognized
        # extra property before ever reaching Annotation's own required-
        # field check, since Java's FIELD_SPECS never even knew "annotations"
        # was a legal key on every element in the first place.
        own_fields = [f for f in c.fields
                      if not (f.origin_class == base and f.name in ("name", "description"))]
        collection_fields_all = [f for f in own_fields if f.type.kind in ("dict", "array", "any-dict")]
        leaf_fields_all = [f for f in own_fields if f.type.kind in _LEAF_KINDS_JAVA]
        child_fields_all = [f for f in own_fields if f.type.kind in ("ref-class", "ref-discriminator")]

        # A field name can legitimately appear twice in own_fields (see the
        # req_names comment below) - Python tolerates a same-named accessor
        # being `def`-ed twice in a row (the second silently shadows the
        # first; both bodies are identical anyway, since an accessor's code
        # is generated from the field's name+kind only, never its rule-id -
        # see _leaf_accessors_java/_child_accessors_java/
        # _collection_field_decl_java), but Java cannot compile two members
        # with the same name. Field DECLARATIONS and their ACCESSOR METHODS
        # are deduplicated (last occurrence wins, matching Python's
        # overwrite order); FIELD_SPECS below deliberately is NOT - it
        # keeps every declaration, exactly like emit_python.py's own
        # _FIELDS, since validate() iterating both is harmless (same
        # field, checked twice) and this mirrors the reference
        # implementation's behavior precisely rather than guessing at a
        # "fix" the spec composition itself doesn't ask for.
        def _dedup_last(fields):
            by_name = {}
            order = []
            for f in fields:
                if f.name not in by_name:
                    order.append(f.name)
                by_name[f.name] = f
            return [by_name[n] for n in order]

        collection_fields = _dedup_last(collection_fields_all)
        leaf_fields = _dedup_last(leaf_fields_all)
        child_fields = _dedup_last(child_fields_all)
        dict_fields = [f for f in collection_fields if f.type.kind == "dict"]
        array_fields = [f for f in collection_fields if f.type.kind == "array"]
        any_dict_fields = [f for f in collection_fields if f.type.kind == "any-dict"]

        out = [_model_file_imports()]
        out.append(f"/** Generated from test-specsheets/{c.category}/{name}/. GENERATED - do not\n"
                    f" * hand-edit; regenerate via generator/generate.py. */\n")
        out.append(f"public final class {name} extends SedBase {{\n")

        field_specs = leaf_fields_all + collection_fields_all + child_fields_all
        if field_specs:
            exprs = ",\n        ".join(_field_spec_expr(f) for f in field_specs)
            out.append(f"    private static final List<FieldSpec> FIELD_SPECS = List.of(\n        {exprs}\n    );\n")
        else:
            out.append("    private static final List<FieldSpec> FIELD_SPECS = List.of();\n")

        # dict.fromkeys(...) dedupes while preserving first-seen order -
        # needed because a field name can legitimately appear twice in
        # own_fields (a subclass re-declaring a field its own mixin already
        # declares with a tighter constraint, e.g. NumericRange/
        # ParameterRange's own "values" alongside Range's mixin "values" -
        # both keep their own separate FieldSpec entry in field_specs below,
        # matching emit_python.py's _FIELDS, but Set.of() throws at runtime
        # on a literal duplicate, unlike Python's set literal).
        req_names = list(dict.fromkeys(f.name for f in own_fields if f.required))
        if req_names:
            out.append(f"    private static final Set<String> REQUIRED_NAMES = Set.of({', '.join(_java_lit(n) for n in req_names)});\n")
        else:
            out.append("    private static final Set<String> REQUIRED_NAMES = Set.of();\n")

        has_ns = bool(c.namespace_updates)
        if has_ns:
            ns_field_entries = []
            for prefix, fs in c.namespace_updates.items():
                exprs = ", ".join(_field_spec_expr(f) for f in fs)
                ns_field_entries.append(f"{_java_lit(prefix)}, List.of({exprs})")
            out.append(f"    private static final Map<String, List<FieldSpec>> NAMESPACE_FIELDS = Map.of(\n        "
                        + ",\n        ".join(ns_field_entries) + "\n    );\n")
            ns_catchall_entries = ", ".join(f"{_java_lit(p)}, {_java_lit(cc)}" for p, cc in c.namespace_catchalls.items())
            out.append(f"    private static final Map<String, String> NAMESPACE_CATCHALL = Map.of({ns_catchall_entries});\n")
            known_prefixes = ", ".join(_java_lit(p) for p in c.namespace_updates)
            out.append(f"    private static final Set<String> KNOWN_NAMESPACE_PREFIXES = Set.of({known_prefixes});\n")

        for f in collection_fields:
            out.append(_collection_field_decl_java(f))
        for f in child_fields:
            ident = _java_ident(f.name)
            out.append(f"    private SedBase {ident};\n")

        out.append("\n")
        out.append(f"    @Override public List<FieldSpec> fieldSpecs() {{ return FIELD_SPECS; }}\n")
        out.append(f"    @Override public Set<String> requiredNames() {{ return REQUIRED_NAMES; }}\n")
        out.append(f"    @Override public String typeConst() {{ return {_java_lit(c.type_const)}; }}\n")
        out.append(f"    @Override public String typeRuleId() {{ return {_java_lit(c.type_rule_id)}; }}\n")
        out.append(f"    @Override public String ownCatchall() {{ return {_java_lit(c.own_catchall)}; }}\n")
        out.append(f"    @Override public String nameRuleId() {{ return {_java_lit(base_name_rule_id)}; }}\n")
        out.append(f"    @Override public String descRuleId() {{ return {_java_lit(base_desc_rule_id)}; }}\n")
        out.append(f"    @Override public String baseCatchall() {{ return {_java_lit(base_catchall)}; }}\n")
        if has_ns:
            out.append("    @Override public Map<String, List<FieldSpec>> namespaceFields() { return NAMESPACE_FIELDS; }\n")
            out.append("    @Override public Map<String, String> namespaceCatchall() { return NAMESPACE_CATCHALL; }\n")
            out.append("    @Override public Set<String> knownNamespacePrefixes() { return KNOWN_NAMESPACE_PREFIXES; }\n")
        if c.type_const is not None:
            out.append(f"    public String getType() {{ return {_java_lit(c.type_const)}; }}\n")
        out.append("\n")

        for f in leaf_fields:
            out.append(_leaf_accessors_java(f) + "\n")
        for f in collection_fields:
            out.append(_collection_accessors_java(f) + "\n")
        for f in child_fields:
            out.append(_child_accessors_java(f) + "\n")
        for prefix, fs in c.namespace_updates.items():
            for f in fs:
                out.append(_leaf_accessors_java(f) + "\n")

        if collection_fields or child_fields:
            out.append("    @Override\n    public List<SedBase> children() {\n        List<SedBase> kids = new ArrayList<>();\n")
            for f in dict_fields:
                ident = _java_ident(f.name)
                out.append(f"        for (String i : {ident}.ids()) kids.add({ident}.get(i));\n")
            for f in array_fields:
                ident = _java_ident(f.name)
                out.append(f"        kids.addAll({ident}.items());\n")
            for f in child_fields:
                ident = _java_ident(f.name)
                out.append(f"        if ({ident} != null) kids.add({ident});\n")
            out.append("        return kids;\n    }\n\n")

            out.append("    @Override\n    public List<ChildLoc> childrenWithLocations() {\n        List<ChildLoc> out = new ArrayList<>();\n")
            for f in dict_fields:
                ident = _java_ident(f.name)
                out.append(f"        for (String i : {ident}.ids()) out.add(new ChildLoc({ident}.get(i), \"/{f.name}/\" + i));\n")
            for f in array_fields:
                ident = _java_ident(f.name)
                out.append(f"        {{ int idx = 0; for (SedBase item : {ident}.items()) {{ out.add(new ChildLoc(item, \"/{f.name}/\" + idx)); idx++; }} }}\n")
            for f in child_fields:
                ident = _java_ident(f.name)
                out.append(f"        if ({ident} != null) out.add(new ChildLoc({ident}, \"/{f.name}\"));\n")
            out.append("        return out;\n    }\n\n")

        if dict_fields:
            out.append("    @Override\n    protected IdKeyedCollection<SedBase> getDictCollection(String fieldName) {\n        switch (fieldName) {\n")
            for f in dict_fields:
                ident = _java_ident(f.name)
                out.append(f"            case {_java_lit(f.name)}: return {ident};\n")
            out.append("            default: return super.getDictCollection(fieldName);\n        }\n    }\n\n")
        if array_fields:
            out.append("    @Override\n    protected ListCollection<SedBase> getListCollection(String fieldName) {\n        switch (fieldName) {\n")
            for f in array_fields:
                ident = _java_ident(f.name)
                out.append(f"            case {_java_lit(f.name)}: return {ident};\n")
            out.append("            default: return super.getListCollection(fieldName);\n        }\n    }\n\n")
        if any_dict_fields:
            out.append("    @Override\n    protected IdKeyedCollection<JsonNode> getAnyDictCollection(String fieldName) {\n        switch (fieldName) {\n")
            for f in any_dict_fields:
                ident = _java_ident(f.name)
                out.append(f"            case {_java_lit(f.name)}: return {ident};\n")
            out.append("            default: return super.getAnyDictCollection(fieldName);\n        }\n    }\n\n")
        if child_fields:
            out.append("    @Override\n    protected void setChildField(String fieldName, SedBase child) {\n        switch (fieldName) {\n")
            for f in child_fields:
                ident = _java_ident(f.name)
                out.append(f"            case {_java_lit(f.name)}: {ident} = child; return;\n")
            out.append("            default: super.setChildField(fieldName, child);\n        }\n    }\n\n")

        out.append("    @Override\n    public ObjectNode ownJsonValue() {\n        ObjectNode d = JsonNodeFactory.instance.objectNode();\n")
        out.append("        if (nameNode != null) d.set(\"name\", nameNode);\n")
        out.append("        if (descriptionNode != null) d.set(\"description\", descriptionNode);\n")
        if c.type_const is not None:
            out.append(f"        d.set(\"_type\", values.containsKey(\"_type\") ? values.get(\"_type\") : TextNode.valueOf({_java_lit(c.type_const)}));\n")
        for f in leaf_fields:
            out.append(f"        if (values.containsKey({_java_lit(f.name)})) d.set({_java_lit(f.name)}, values.get({_java_lit(f.name)}));\n")
        for prefix, fs in c.namespace_updates.items():
            for f in fs:
                out.append(f"        if (values.containsKey({_java_lit(f.name)})) d.set({_java_lit(f.name)}, values.get({_java_lit(f.name)}));\n")
        for f in dict_fields:
            ident = _java_ident(f.name)
            out.append(f"        if ({ident}.size() > 0) {{ ObjectNode sub = d.putObject({_java_lit(f.name)}); for (String i : {ident}.ids()) sub.set(i, {ident}.get(i).toJsonValue()); }}\n")
        for f in array_fields:
            ident = _java_ident(f.name)
            out.append(f"        if ({ident}.size() > 0) {{ ArrayNode arr = d.putArray({_java_lit(f.name)}); for (SedBase item : {ident}.items()) arr.add(item.toJsonValue()); }}\n")
        for f in any_dict_fields:
            ident = _java_ident(f.name)
            out.append(f"        if ({ident}.size() > 0) {{ ObjectNode sub = d.putObject({_java_lit(f.name)}); for (String i : {ident}.ids()) sub.set(i, {ident}.get(i)); }}\n")
        for f in child_fields:
            ident = _java_ident(f.name)
            out.append(f"        if ({ident} != null) d.set({_java_lit(f.name)}, {ident}.toJsonValue());\n")
        out.append("        for (Map.Entry<String, JsonNode> e : nsAttrs.entrySet()) d.set(e.getKey(), e.getValue());\n")
        out.append("        return d;\n    }\n")

        out.append("}\n")
        files[f"{name}.java"] = "".join(out)

    return files


def emit_unknown_holder_files(model: SpecModel) -> dict:
    files = {}
    for disc_name, disc in model.discriminators.items():
        uname = disc.unknown_class_name
        out = [f'''package {PKG};

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/** Opaque holder for a {disc_name} instance whose _type names an
 * unregistered namespace prefix (see Design.md's Namespaces section) -
 * round-trips unchanged, never itself a validation error. GENERATED - do
 * not hand-edit; regenerate via generator/generate.py. */
public final class {uname} extends SedBase {{
    private final String typeValue;
    private final ObjectNode raw;

    public {uname}(String typeValue, JsonNode raw) {{
        this.typeValue = typeValue;
        this.raw = raw.deepCopy();
    }}

    public String getType() {{ return typeValue; }}

    @Override
    public ObjectNode ownJsonValue() {{
        ObjectNode d = raw.deepCopy();
        if (nameNode != null) d.set("name", nameNode);
        if (descriptionNode != null) d.set("description", descriptionNode);
        return d;
    }}

    @Override
    public Set<String> allowedKeys() {{
        Set<String> keys = new HashSet<>();
        raw.fieldNames().forEachRemaining(keys::add);
        return keys;
    }}

    @Override
    protected List<ValidationProblem> validateOwn() {{
        return new ArrayList<>();
    }}
}}
''']
        files[f"{uname}.java"] = "".join(out)
    return files


def emit_dispatch_java(model: SpecModel) -> str:
    out = [f'''package {PKG};

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
public final class Dispatch {{
    private Dispatch() {{}}

    // The full OrRef family whose value is loaded via the generic
    // setOrRefValueNode/setOrRefRefNode pair rather than a plain
    // obj.values.put() - see generator/emit_java.py's _ORREF_KINDS_JAVA
    // (the same six kinds every generated model class's own accessors
    // handle).
    private static final Set<String> ORREF_KINDS = Set.of(
            "StringOrRef", "NumberOrRef", "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef");

    public static final class Result {{
        public final SedBase value;
        public final ValidationProblem problem;

        public Result(SedBase value, ValidationProblem problem) {{
            this.value = value;
            this.problem = problem;
        }}
    }}

    @FunctionalInterface
    public interface ParseFn {{
        Result parse(JsonNode raw);
    }}

''']

    for disc_name, disc in model.discriminators.items():
        uname = disc.unknown_class_name
        out.append(f"    public static Result parse{disc_name}(JsonNode raw) {{\n")
        out.append("        if (!raw.has(\"_type\")) {\n")
        if disc.missing_type_rule_id:
            out.append(f"            return new Result(null, RuleCatalog.makeProblem({_java_lit(disc.missing_type_rule_id)}, \"\"));\n")
        else:
            out.append(f"            Map<String, Object> ph0 = new HashMap<>();\n")
            out.append(f"            ph0.put(\"schema-message\", \"missing _type\");\n")
            out.append(f"            return new Result(null, RuleCatalog.makeProblem({_java_lit(disc_name + '-0000')}, \"\", ph0));\n")
        out.append("        }\n")
        out.append("        String tv = raw.get(\"_type\").asText();\n")
        out.append("        SedBase obj = null;\n")
        out.append("        switch (tv) {\n")
        for tc, br in disc.branches.items():
            out.append(f"            case {_java_lit(tc)}: obj = new {br.class_name}(); break;\n")
        out.append("        }\n")
        out.append("        if (obj != null) {\n")
        out.append("            loadFields(obj, raw);\n")
        out.append("            return new Result(obj, null);\n")
        out.append("        }\n")
        out.append("        Matcher m = SedBase.NAMESPACE_KEY_PATTERN.matcher(tv);\n")
        known = ", ".join(_java_lit(b.namespace) for b in disc.branches.values() if b.namespace)
        out.append(f"        Set<String> known = Set.of({known});\n" if known else "        Set<String> known = Set.of();\n")
        out.append("        if (m.matches() && !known.contains(m.group(1))) {\n")
        out.append(f"            return new Result(new {uname}(tv, raw), null);\n")
        out.append("        }\n")
        out.append("        Map<String, Object> ph = new HashMap<>();\n")
        out.append("        ph.put(\"schema-message\", \"unrecognized _type '\" + tv + \"'\");\n")
        out.append(f"        return new Result(new {uname}(tv, raw), RuleCatalog.makeProblem({_java_lit(disc_name + '-0000')}, \"\", ph));\n")
        out.append("    }\n\n")

    out.append("    private static ParseFn parserFor(String discName) {\n        switch (discName) {\n")
    for disc_name in model.discriminators:
        out.append(f"            case {_java_lit(disc_name)}: return Dispatch::parse{disc_name};\n")
    out.append("            default: throw new ApiError(\"unknown discriminator \" + discName);\n        }\n    }\n\n")

    out.append("    private static SedBase newItemInstance(String className) {\n        switch (className) {\n")
    # Covers an "array"-kind field's own item_class, a "dict"-kind field's
    # item_class when it has no _type dispatch of its own (SEDDocument.
    # styles -> Style, Loop.loopVariables -> LoopVariable, ...), and a
    # "ref-class"-kind field's item_class (the fixed target class a single
    # nested child constructs directly) - same construction need in all
    # three, just a different cardinality (Design.md's Classes section /
    # this module's _child_accessors_java).
    item_classes = sorted({f.type.item_class for c in model.classes.values() for f in c.fields
                            if f.type.item_class and f.type.kind in ("array", "dict", "ref-class")})
    for cls_name in item_classes:
        out.append(f"            case {_java_lit(cls_name)}: return new {cls_name}();\n")
    out.append("            default: throw new ApiError(\"unknown item class \" + className);\n        }\n    }\n\n")

    out.append('''    public static void loadFields(SedBase obj, JsonNode raw) {
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
                        Map<String, Object> ph = new HashMap<>();
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
                    Map<String, Object> ph = new HashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", obj.getClass().getSimpleName());
                    ph.put("id", obj.ownIdForMessage());
                    ph.put("value", rawValue.toString());
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
                        Map<String, Object> ph = new HashMap<>();
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
                    Map<String, Object> ph = new HashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", obj.getClass().getSimpleName());
                    ph.put("id", obj.ownIdForMessage());
                    ph.put("value", rawValue.toString());
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
''')
    return "".join(out)


def emit_rules_data_java(model: SpecModel) -> str:
    out = [f'''package {PKG};

/** Generated rule catalogue. GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class RulesData {{
    private RulesData() {{}}

    public static void register() {{
''']
    for rid, r in sorted(model.rules.items()):
        out.append(f"        RuleCatalog.CATALOG.put({_java_lit(rid)}, "
                    f"new RuleCatalog.Entry({_java_lit(r.rule)}, {_java_lit(r.message)}, {_java_lit(r.severity)}));\n")
    out.append("    }\n}\n")
    return "".join(out)


def emit_io_java(model: SpecModel) -> str:
    doc_name = model.document_class
    return f'''package {PKG};

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/** Top-level read/write entry points. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class Io {{
    private static final ObjectMapper MAPPER = new ObjectMapper();

    static {{
        RulesData.register();
    }}

    private Io() {{}}

    public static {doc_name} readFromString(String text) throws IOException {{
        JsonNode raw = MAPPER.readTree(text);
        {doc_name} obj = new {doc_name}();
        Dispatch.loadFields(obj, raw);
        obj.attach(null, obj);
        return obj;
    }}

    public static {doc_name} readFromFile(String path) throws IOException {{
        String text = Files.readString(Path.of(path), StandardCharsets.UTF_8);
        return readFromString(text);
    }}

    public static String writeToString({doc_name} doc) {{
        try {{
            return MAPPER.writerWithDefaultPrettyPrinter().writeValueAsString(doc.toJsonValue());
        }} catch (IOException e) {{
            throw new RuntimeException(e);
        }}
    }}

    public static void writeToFile({doc_name} doc, String path) throws IOException {{
        Files.writeString(Path.of(path), writeToString(doc), StandardCharsets.UTF_8);
    }}
}}
'''


def _repo_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _copy_fixture_test_java(out_dir: str, java_package: str) -> None:
    """Copies templates/java/tests/FixtureTest.java -> <out_dir>/src/test/
    java/<package-path>/FixtureTest.java, rewriting only its leading
    `package ...;` line to match java_package. Every other reference in
    that file resolves generically (same-package visibility or reflection
    - see the file's own top-of-file comment), so the package line is the
    one place this copy step needs to touch content rather than copying
    verbatim - unlike _copy_test_fixtures_py in emit_python.py, where
    Python's lack of a package-declaration concept means no rewrite is
    needed at all."""
    src = os.path.join(_repo_root(), "templates", "java", "tests", "FixtureTest.java")
    with open(src) as f:
        content = f.read()
    first_nl = content.index("\n")
    assert content[:first_nl].startswith("package "), (
        "templates/java/tests/FixtureTest.java must start with a `package ...;` line"
    )
    content = f"package {java_package};" + content[first_nl:]
    test_pkg_dir = os.path.join(out_dir, "src", "test", "java", *java_package.split("."))
    os.makedirs(test_pkg_dir, exist_ok=True)
    with open(os.path.join(test_pkg_dir, "FixtureTest.java"), "w") as f:
        f.write(content)


def _pom_xml(group_id: str, artifact_id: str, description: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{group_id}</groupId>
  <artifactId>{artifact_id}</artifactId>
  <version>0.1.0</version>
  <packaging>jar</packaging>
  <description>{description}</description>

  <properties>
    <maven.compiler.release>21</maven.compiler.release>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-databind</artifactId>
      <version>2.17.2</version>
    </dependency>
    <dependency>
      <groupId>com.networknt</groupId>
      <artifactId>json-schema-validator</artifactId>
      <version>1.5.1</version>
    </dependency>
    <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.10.3</version>
      <scope>test</scope>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <version>3.2.5</version>
        <configuration>
          <!-- surefire's default workingDirectory is ${{project.basedir}},
               i.e. this module's own directory, regardless of where mvn
               itself was invoked from - templates/java/tests/FixtureTest.
               java's fixturesDir() relies on that for its own plain
               relative fallback. This property is a second, explicit way
               to give it the same path (see that file's comment), always
               correct no matter how deeply the java package option nests
               this module's sources. -->
          <systemPropertyVariables>
            <sed2.fixturesDir>${{project.basedir}}/../../fixtures</sed2.fixturesDir>
          </systemPropertyVariables>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
'''


def emit_java_package(
    model: SpecModel,
    out_dir: str,
    java_package: str = "org.sed2test",
    maven_group_id: str | None = None,
    maven_artifact_id: str = "libsed2test",
    description: str | None = None,
) -> None:
    global PKG
    PKG = java_package
    maven_group_id = maven_group_id or java_package
    description = description or (
        "Generated SED2 test-fixture library (Java target) - exercises "
        "the SED2 generator against test-specsheets/, see Design.md's Testing "
        "section."
    )

    pkg_dir = os.path.join(out_dir, "src", "main", "java", *PKG.split("."))
    os.makedirs(pkg_dir, exist_ok=True)

    for fname, content in runtime_files().items():
        with open(os.path.join(pkg_dir, fname), "w") as f:
            f.write(content)
    for fname, content in emit_model_java_files(model).items():
        with open(os.path.join(pkg_dir, fname), "w") as f:
            f.write(content)
    for fname, content in emit_unknown_holder_files(model).items():
        with open(os.path.join(pkg_dir, fname), "w") as f:
            f.write(content)
    with open(os.path.join(pkg_dir, "Dispatch.java"), "w") as f:
        f.write(emit_dispatch_java(model))
    with open(os.path.join(pkg_dir, "RulesData.java"), "w") as f:
        f.write(emit_rules_data_java(model))
    with open(os.path.join(pkg_dir, "Io.java"), "w") as f:
        f.write(emit_io_java(model))

    with open(os.path.join(out_dir, "pom.xml"), "w") as f:
        f.write(_pom_xml(maven_group_id, maven_artifact_id, description))

    _copy_fixture_test_java(out_dir, PKG)

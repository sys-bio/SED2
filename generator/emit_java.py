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

Beyond that schema pass, validate() runs every check the Python target does
(Python is the reference implementation; the two must report the same rule
IDs, locations, severities and messages for every document):
  - the math-grammar rules (Types-0001..0004, MathRules.java);
  - reference parsing/resolution and every rule that hangs off a resolved
    reference - SEDBase-0005 .. -0017 (including the formulaic ref-type field
    rules and the x-ref-target "model"/"annotatedData" rules), SEDBase-0013's
    Repeat scoping, AbstractTask-0003's ordering, Repeat-0008/-0009/-0010,
    LoopVariable-0004 - via References.java (the shared dispatcher, the Java
    port of the Python RUNTIME's reference machinery) and OutputsShape.java
    (the outputs.json expr/valid interpreter, the port of OUTPUTS_SHAPE_PY);
  - the whole-document rules SEDDocument-0009/-0010/-0011 (namespaces,
    version) and -0013 (constants ordering).
The per-rule logic of the last two groups is one small hand-written class per
rule under templates/java/rules/ (named from the rule ID, e.g.
SedBase0015.java), copied into the generated package by
_copy_handwritten_rules_java only for rule IDs this spec tree defines - the
Java analog of emit_python.py's _copy_handwritten_rules_py and its
ImportError-style "rule absent from this tree -> skip" behavior, realized
through the generated Handwritten.java facade (no-op stubs + HAS_* flags).
Only concrete tasks/ classes carry an outputs.json (embedded in each class as
JSON text). Text placeholders are rendered the way Python's str()/json.dumps()
would (PyFmt.java), so message text matches across targets.

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

import java.util.List;

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
    public final boolean isMath;           // x-math (Design.md's Math section / Types-0001..0004)
    public final Integer minLength;        // nullable (core/Types' URI leaf: "minLength": 1)
    public final List<String> enumValues;  // nullable: a fixed set of legal string values
    public final String refTypeRuleId;     // nullable: the formulaic "if a reference, must resolve to type X" rule
    public final String itemKind;          // nullable: ArrayOrRef element / DictOrRef value kind ("string" | "number" | "ref" | "any")
    public final String refTarget;         // nullable: x-ref-target ("model" -> SEDBase-0016, "annotatedData" -> SEDBase-0017)

    public FieldSpec(String name, String kind, boolean required, String ruleId, String requiredRuleId,
                      String originCatchall, Double minimum, Double exclusiveMinimum, String pattern,
                      String itemClass, String itemDiscriminator, boolean isMath, Integer minLength,
                      List<String> enumValues, String refTypeRuleId, String itemKind, String refTarget) {{
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
        this.isMath = isMath;
        this.minLength = minLength;
        this.enumValues = enumValues;
        this.refTypeRuleId = refTypeRuleId;
        this.itemKind = itemKind;
        this.refTarget = refTarget;
    }}
}}
'''

def _rule_catalog_java() -> str:
    return f'''package {PKG};

import java.util.HashMap;
import java.util.LinkedHashMap;
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
            out = out.replace("{{" + e.getKey() + "}}", PyFmt.str(e.getValue()));
        }}
        return out;
    }}

    /** makeProblem() with the placeholders given as alternating key, value
     * arguments - kept in argument order (so substitution order matches the
     * Python target's make_problem(**kwargs)); a value renders the way
     * Python's str() would (see PyFmt). */
    public static ValidationProblem problem(String ruleId, String location, Object... keyValues) {{
        Map<String, Object> ph = new LinkedHashMap<>();
        for (int i = 0; i + 1 < keyValues.length; i += 2) ph.put((String) keyValues[i], keyValues[i + 1]);
        return makeProblem(ruleId, location, ph);
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

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

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

    /** Java port of emit_python.py's leaf_schema_for(): the per-field schema
     * fragment for one already-resolved field type. minimum/exclusiveMinimum
     * are numeric-only JSON Schema keywords - a no-op against a non-numeric
     * instance (a reference string, for an *OrRef kind) - so bolting them on
     * at the top level is always safe. pattern/minLength/enum are STRING-only
     * keywords, and a StringOrRef's reference form is *also* a plain string,
     * so for that kind the literal value's constraints are split into their
     * own anyOf branch beside a reference-shaped string, rather than
     * incorrectly rejecting a perfectly valid reference. */
    static ObjectNode leafSchemaFor(String kind, Double minimum, Double exclusiveMinimum, String pattern,
                                    Integer minLength, List<String> enumValues) {{
        ObjectNode base = baseSchema(kind);
        if (minimum != null) base.put("minimum", minimum);
        if (exclusiveMinimum != null) base.put("exclusiveMinimum", exclusiveMinimum);
        boolean hasStringConstraints = pattern != null || minLength != null || enumValues != null;
        if (hasStringConstraints) {{
            ObjectNode constraints = JsonNodeFactory.instance.objectNode();
            if (pattern != null) constraints.put("pattern", pattern);
            if (minLength != null) constraints.put("minLength", minLength);
            if (enumValues != null) {{
                ArrayNode en = constraints.putArray("enum");
                for (String v : enumValues) en.add(v);
            }}
            if (kind.equals("StringOrRef")) {{
                ObjectNode wrapped = JsonNodeFactory.instance.objectNode();
                ArrayNode any = wrapped.putArray("anyOf");
                ObjectNode lit = JsonNodeFactory.instance.objectNode();
                lit.put("type", "string");
                lit.setAll(constraints);
                ObjectNode ref = JsonNodeFactory.instance.objectNode();
                ref.put("type", "string");
                ref.put("pattern", SIDREF_PATTERN);
                any.add(lit);
                any.add(ref);
                return wrapped;
            }}
            base.setAll(constraints);
        }}
        return base;
    }}

    // Compiled schemas, keyed by the schema's own text - a document has many
    // fields of a handful of distinct shapes.
    private static final Map<String, JsonSchema> SCHEMA_CACHE = new ConcurrentHashMap<>();

    public static boolean leafValueOk(String kind, JsonNode value, Double minimum, Double exclusiveMinimum,
                                      String pattern, Integer minLength, List<String> enumValues) {{
        ObjectNode schema = leafSchemaFor(kind, minimum, exclusiveMinimum, pattern, minLength, enumValues);
        JsonSchema s = SCHEMA_CACHE.computeIfAbsent(schema.toString(), k -> FACTORY.getSchema(schema));
        Set<?> errors = s.validate(value);
        return errors.isEmpty();
    }}

    public static boolean leafValueOk(String kind, JsonNode value, Double minimum, Double exclusiveMinimum,
                                      String pattern) {{
        return leafValueOk(kind, value, minimum, exclusiveMinimum, pattern, null, null);
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
public final class IdKeyedCollection<T> implements IdCollection {{
    private final List<String> order = new ArrayList<>();
    private final Map<String, T> items = new LinkedHashMap<>();

    @Override
    public List<String> ids() {{ return new ArrayList<>(order); }}

    @Override
    public boolean has(String itemId) {{ return items.containsKey(itemId); }}

    @Override
    public Object getObject(String itemId) {{ return items.get(itemId); }}

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
public abstract class SedBase {{
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

    /** core-spec.md Section 8's per-class outputs.json envelope (the parsed
     * JSON) - non-null only for a concrete tasks/ class; read by the
     * shape-resolution rules SEDBase-0008 through -0015. */
    public JsonNode outputsJson() {{ return null; }}

    /** True only on the generated document root class - gates the
     * whole-document checks (SEDDocument-0009 through -0011 and -0013), which
     * only make sense run once, from the document root. */
    public boolean isDocumentClass() {{ return false; }}

    /** The newest document version this generator run's spec tree knows (the
     * document root class only; see SEDDocument-0011). */
    public String maxKnownDocumentVersion() {{ return null; }}

    /** Every id-keyed collection field name THIS class declares (its "dict" and
     * "any-dict" fields) - used by ownIdForMessage() to search a PARENT's own
     * collections for `this`. */
    public List<String> idCollectionNames() {{ return Collections.emptyList(); }}

    /** The id-keyed collection stored in field `fieldName` ("dict" or
     * "any-dict" kind), or null if this class has no such field - reference
     * resolution (References.getSedReference) walks the containment tree
     * through this. */
    public IdCollection getIdCollection(String fieldName) {{ return null; }}

    /** The _type value this element carries (its class's const, or an unknown
     * holder's raw value), or null for a class without one. */
    public String typeValue() {{ return typeConst(); }}

    /** The stored raw value of a plain leaf field, or null when unset. */
    public JsonNode valueNode(String name) {{ return values.get(name); }}

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
        try {{
            return validateChecked(severityAtLeast);
        }} finally {{
            // parent/document backpointers are WeakReferences (see attach()),
            // so nothing else may keep the root alive while its own validate()
            // runs: the JIT is free to treat `this` as dead after its last use,
            // and a collection mid-validate would silently turn every
            // reference rule off ("no document to walk"). Python's refcounting
            // gives the caller's frame this guarantee for free.
            java.lang.ref.Reference.reachabilityFence(this);
        }}
    }}

    private List<ValidationProblem> validateChecked(String severityAtLeast) {{
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
        String className = getClass().getSimpleName();
        String ownId = ownIdForMessage();

        // _type const (only meaningful when this class is validated
        // directly, e.g. not through a discriminator that already
        // dispatched on it)
        if (typeConst() != null && typeRuleId() != null) {{
            JsonNode tv = instance.get("_type");
            boolean same = tv != null && tv.isTextual() && typeConst().equals(tv.textValue());
            if (!same) {{
                problems.add(RuleCatalog.problem(typeRuleId(), "/_type", "attr", "_type", "class", className,
                        "id", ownId, "value", tv, "allowed", typeConst()));
            }}
        }}

        // universal name/description mixin (TestBaseFields/SEDBaseFields) -
        // not a per-class FieldSpec, so checked directly here against the
        // base mixin's own rule IDs (the same on every concrete class).
        if (nameNode != null && !LeafValidation.leafValueOk("string", nameNode, null, null, null)) {{
            String rid = nameRuleId() != null ? nameRuleId() : baseCatchall();
            problems.add(RuleCatalog.problem(rid, "/name", "attr", "name", "class", className, "id", ownId,
                    "value", nameNode));
        }}
        if (descriptionNode != null && !LeafValidation.leafValueOk("string", descriptionNode, null, null, null)) {{
            String rid = descRuleId() != null ? descRuleId() : baseCatchall();
            problems.add(RuleCatalog.problem(rid, "/description", "attr", "description", "class", className,
                    "id", ownId, "value", descriptionNode));
        }}

        List<FieldSpec> all = new ArrayList<>(fieldSpecs());
        for (List<FieldSpec> specs : namespaceFields().values()) all.addAll(specs);

        for (FieldSpec spec : all) {{
            boolean present = instance.has(spec.name);
            if (spec.required && !present) {{
                String rid = spec.requiredRuleId != null ? spec.requiredRuleId : spec.originCatchall;
                problems.add(RuleCatalog.problem(rid, "/" + spec.name, "attr", spec.name, "class", className,
                        "id", ownId));
                continue;
            }}
            if (!present) continue;
            JsonNode value = instance.get(spec.name);
            if (LEAF_KINDS.contains(spec.kind)) {{
                if (!LeafValidation.leafValueOk(spec.kind, value, spec.minimum, spec.exclusiveMinimum, spec.pattern,
                        spec.minLength, spec.enumValues)) {{
                    String rid = spec.ruleId != null ? spec.ruleId : spec.originCatchall;
                    Map<String, Object> ph = new LinkedHashMap<>();
                    ph.put("attr", spec.name);
                    ph.put("class", className);
                    ph.put("id", ownId);
                    ph.put("value", value);
                    if (spec.enumValues != null) {{
                        // A rule fired from an enum-constrained leaf's own
                        // message template may reference {{allowed}} (e.g.
                        // Curve-0002/Surface's own curveType/surfaceType
                        // rules) - harmless to always include, since
                        // formatMessage only substitutes placeholders the
                        // template actually names.
                        List<String> reprs = new ArrayList<>();
                        for (String v : spec.enumValues) reprs.add(PyFmt.reprStr(v));
                        ph.put("allowed", String.join(", ", reprs));
                    }}
                    problems.add(RuleCatalog.makeProblem(rid, "/" + spec.name, ph));
                }} else if (REFERENCE_CAPABLE_KINDS.contains(spec.kind) && References.isReference(value)) {{
                    problems.addAll(References.checkReferenceField(
                            value.textValue(), getDocument(), className, ownId, spec.name, "/" + spec.name,
                            this, References.FieldInfo.of(spec)));
                }} else if (spec.kind.equals("DictOrRef") && value.isObject()) {{
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
                    while (it.hasNext()) {{
                        Map.Entry<String, JsonNode> e = it.next();
                        if (References.isReference(e.getValue())) {{
                            problems.addAll(References.checkReferenceField(
                                    e.getValue().textValue(), getDocument(), className, ownId, spec.name,
                                    "/" + spec.name + "/" + e.getKey(), this,
                                    References.FieldInfo.bare(spec.kind)));
                        }}
                    }}
                }} else if (spec.kind.equals("ArrayOrRef") && value.isArray()) {{
                    // The array-literal branch of an ArrayOrRef field: each
                    // element that is itself a reference gets its own
                    // reference-resolution dispatch (SEDBase-0005.md: the rule
                    // applies to "an element of an array or object value"),
                    // with no per-element expected type - same scope as the
                    // DictOrRef dict-literal branch above.
                    for (int idx = 0; idx < value.size(); idx++) {{
                        JsonNode el = value.get(idx);
                        if (References.isReference(el)) {{
                            problems.addAll(References.checkReferenceField(
                                    el.textValue(), getDocument(), className, ownId, spec.name,
                                    "/" + spec.name + "/" + idx, this,
                                    References.FieldInfo.bare(spec.kind)));
                        }}
                    }}
                }} else if (spec.isMath && value.isTextual()) {{
                    // Types-0001..0004 (Design.md's Math section) - only for
                    // a literal string value that already passed its own
                    // leaf schema check above; a reference-form value of an
                    // OrRef math field is dispatched to the reference rules
                    // in the branch above instead.
                    problems.addAll(MathRules.checkMathField(
                            value.asText(), className, ownId, spec.name, "/" + spec.name));
                }}
            }} else if (spec.kind.equals("any") && References.isReference(value)) {{
                // A scalar AnyValueOrRef field (e.g. LoopVariable.initialValue,
                // AggregationCalculation.input) isn't in LEAF_KINDS - "any JSON
                // value" has no leafValueOk() schema to check against - but an
                // SIdRef string may still substitute for it, so it needs the
                // same reference-resolution dispatch as every *OrRef-kind
                // field above.
                problems.addAll(References.checkReferenceField(
                        value.textValue(), getDocument(), className, ownId, spec.name, "/" + spec.name,
                        this, References.FieldInfo.bare("any")));
            }}
        }}
        if (isDocumentClass()) {{
            problems.addAll(References.checkNamespaceUsageAndVersion(this));
            problems.addAll(References.checkConstantsOrdering(this));
        }}
        // Repeat-0008/-0009/-0010 (own-subTasks scoping for a Repeat-family
        // instance's outputVariableMap/aggregateOutputVariables) and
        // LoopVariable-0004 (own-Loop scoping for subsequentValues) each
        // internally no-op for every class they don't apply to (a cheap
        // class-shape check, not a class-name check) - called unconditionally
        // here, the same as every other per-instance handwritten check above.
        problems.addAll(References.checkRepeatOwnChildren(this));
        problems.addAll(References.checkLoopVariableScope(this));
        problems.addAll(References.checkParameterScanRanges(this));
        return problems;
    }}

    /** This element's own id, or null when it has none - Design.md's Classes
     * section: id is implicit, the key under which an element is stored in
     * its owning collection, never a field on the element itself. So this
     * walks up to the parent and searches every id-keyed collection IT
     * declares for whichever key maps to `this`. Looked up on every call
     * rather than cached, so a rename (setIdOn&lt;Collection&gt;) is always
     * reflected. Null for anything genuinely id-less: the document root, an
     * array-item class stored positionally rather than by id, a single
     * embedded child (e.g. a simulation's independent-variable range), or an
     * unattached/standalone instance no parent has claimed yet. */
    private String findOwnId() {{
        SedBase parent = getParent();
        if (parent == null) return null;
        for (String name : parent.idCollectionNames()) {{
            IdCollection coll = parent.getIdCollection(name);
            if (coll == null) continue;
            for (String iid : coll.ids()) {{
                if (coll.getObject(iid) == this) return iid;
            }}
        }}
        return null;
    }}

    /** True when this element currently has an id, i.e. it is stored under a
     * key in an id-keyed collection of its parent (tasks, outputs, styles, a
     * Repeat's subTasks, ...). False for the document itself, array items,
     * embedded single children, and elements not (yet) added to any
     * collection. */
    public boolean isSetId() {{ return findOwnId() != null; }}

    /** This element's own id: the key it has in the id-keyed collection that
     * holds it (e.g. the task id for an entry of the document's tasks, the
     * sub-task id for an entry of a Loop's subTasks). Follows renames. Throws
     * ApiError when the element has no id (see isSetId) - the same as
     * getXxx() on an unset attribute. Note getParent() is the owning element
     * (the document for a top-level task), not the collection. */
    public String getId() {{
        String iid = findOwnId();
        if (iid == null) {{
            throw new ApiError("this element has no id: it is not stored under a key in an "
                    + "id-keyed collection of its parent");
        }}
        return iid;
    }}

    /** This element's own id for a validation message's {{id}} placeholder:
     * getId()'s value, or "?" for an element with none. */
    public String ownIdForMessage() {{
        String iid = findOwnId();
        return iid == null ? "?" : iid;
    }}

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


def _math_ast_java() -> str:
    """MathAst.java - Java port of emit_python.py's math_ast.py (the
    RUNTIME-embedded ASTNode/_Builder/parse() trio), trimmed to what
    MathRules.java's Types-0002/-0003/-0004 checks actually walk (no
    to_string()/_render - that's for round-tripping parsed math back to
    text, not needed by validation). Builds on the ANTLR-generated
    mathLexer/mathParser/mathBaseVisitor in the `{PKG}.antlr` subpackage
    (see antlr_tool.generate_java_math_parser, called from
    emit_java_package) - same math.g4 grammar as the Python target, so this
    desugaring (relational-chain / logical-run flattening, '%' -> rem(),
    unary '!' -> not()) mirrors _Builder in emit_python.py's math_ast.py
    exactly; see that class's own comments for the semantics. GENERATED -
    do not hand-edit; regenerate via generator/generate.py."""
    return f'''package {PKG};

import {PKG}.antlr.mathLexer;
import {PKG}.antlr.mathParser;
import {PKG}.antlr.mathBaseVisitor;
import org.antlr.v4.runtime.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/** SED2 math-grammar AST + parser (Types-0001's "well-formed expression"
 * check and the shared tree the other three Types rules walk). GENERATED -
 * do not hand-edit; regenerate via generator/generate.py. */
public final class MathAst {{
    private MathAst() {{}}

    public enum NodeType {{
        NUMBER, REFERENCE, NAME, FUNCTION_CALL, ARRAY,
        UMINUS, UPLUS, ADD, SUB, MUL, DIV, POW
    }}

    /** Borrows the rough interface of libsbml's ASTNode, minus the XML
     * dependency - same design note as emit_python.py's ASTNode. */
    public static final class Node {{
        public final NodeType nodeType;
        public final String text;   // NUMBER / REFERENCE: the raw source lexeme
        public final String name;   // NAME / FUNCTION_CALL: the identifier
        public final List<Node> children;

        Node(NodeType nodeType, String text, String name, List<Node> children) {{
            this.nodeType = nodeType;
            this.text = text;
            this.name = name;
            this.children = children;
        }}

        public boolean isNumber() {{ return nodeType == NodeType.NUMBER; }}
        public boolean isReference() {{ return nodeType == NodeType.REFERENCE; }}
        public boolean isName() {{ return nodeType == NodeType.NAME; }}
        public boolean isFunctionCall() {{ return nodeType == NodeType.FUNCTION_CALL; }}
        public int getNumChildren() {{ return children.size(); }}
        public Node getChild(int index) {{ return children.get(index); }}

        /** Depth-first (this node first, then each child) - the traversal
         * MathRules.java uses for Types-0002 through Types-0004. */
        public List<Node> walk() {{
            List<Node> out = new ArrayList<>();
            walkInto(out);
            return out;
        }}

        private void walkInto(List<Node> out) {{
            out.add(this);
            for (Node c : children) c.walkInto(out);
        }}
    }}

    /** Raised by parse() when the text isn't a well-formed SED2 math
     * expression - the condition Types-0001 reports, with this exception's
     * message as its {{parse-message}}. */
    public static final class MathSyntaxError extends RuntimeException {{
        public MathSyntaxError(String message) {{ super(message); }}
    }}

    private static final Map<String, String> RELOP_KIND = Map.of(
            "==", "eq", "!=", "neq", "<>", "neq", "><", "neq",
            "<", "lt", ">", "gt", "<=", "leq", ">=", "geq");

    /** a < b < c -> lt(a, b, c); a < b <= c -> and(lt(a, b), leq(b, c)) -
     * see emit_python.py's _build_relational for the full rationale this
     * mirrors verbatim. */
    private static Node buildRelational(List<Node> operands, List<String> kinds) {{
        if (kinds.isEmpty()) return operands.get(0);
        List<Node> runNodes = new ArrayList<>();
        int i = 0;
        int n = kinds.size();
        while (i < n) {{
            String kind = kinds.get(i);
            List<Node> runOperands = new ArrayList<>();
            runOperands.add(operands.get(i));
            runOperands.add(operands.get(i + 1));
            int j = i + 1;
            if (!kind.equals("neq")) {{
                while (j < n && kinds.get(j).equals(kind)) {{
                    runOperands.add(operands.get(j + 1));
                    j++;
                }}
            }}
            runNodes.add(new Node(NodeType.FUNCTION_CALL, null, kind, runOperands));
            i = j;
        }}
        if (runNodes.size() == 1) return runNodes.get(0);
        return new Node(NodeType.FUNCTION_CALL, null, "and", runNodes);
    }}

    /** a && b && c -> and(a, b, c); a && b || c -> or(and(a, b), c) - see
     * emit_python.py's _flatten_logical for the full rationale this
     * mirrors verbatim. */
    private static Node flattenLogical(List<Node> operands, List<String> ops) {{
        if (ops.isEmpty()) return operands.get(0);
        List<String> groupOps = new ArrayList<>();
        List<List<Node>> groupOperands = new ArrayList<>();
        String currentOp = ops.get(0);
        List<Node> currentOperands = new ArrayList<>();
        currentOperands.add(operands.get(0));
        currentOperands.add(operands.get(1));
        for (int i = 1; i < ops.size(); i++) {{
            if (ops.get(i).equals(currentOp)) {{
                currentOperands.add(operands.get(i + 1));
            }} else {{
                groupOps.add(currentOp);
                groupOperands.add(currentOperands);
                currentOp = ops.get(i);
                currentOperands = new ArrayList<>();
                currentOperands.add(groupOperands.get(groupOperands.size() - 1)
                        .get(groupOperands.get(groupOperands.size() - 1).size() - 1));
                currentOperands.add(operands.get(i + 1));
            }}
        }}
        groupOps.add(currentOp);
        groupOperands.add(currentOperands);
        Node result = new Node(NodeType.FUNCTION_CALL, null, groupOps.get(0), groupOperands.get(0));
        for (int g = 1; g < groupOps.size(); g++) {{
            List<Node> children = new ArrayList<>();
            children.add(result);
            children.addAll(groupOperands.get(g).subList(1, groupOperands.get(g).size()));
            result = new Node(NodeType.FUNCTION_CALL, null, groupOps.get(g), children);
        }}
        return result;
    }}

    private static final class Builder extends mathBaseVisitor<Node> {{
        @Override
        public Node visitStart(mathParser.StartContext ctx) {{ return visit(ctx.expr()); }}

        @Override
        public Node visitExpr(mathParser.ExprContext ctx) {{ return visit(ctx.logical()); }}

        @Override
        public Node visitLogical(mathParser.LogicalContext ctx) {{
            List<mathParser.RelationalContext> relationals = ctx.relational();
            if (relationals.size() == 1) return visit(relationals.get(0));
            List<Node> operands = new ArrayList<>();
            for (mathParser.RelationalContext r : relationals) operands.add(visit(r));
            List<String> ops = new ArrayList<>();
            for (int i = 1; i < ctx.getChildCount(); i += 2) {{
                ops.add(ctx.getChild(i).getText().equals("&&") ? "and" : "or");
            }}
            return flattenLogical(operands, ops);
        }}

        @Override
        public Node visitRelational(mathParser.RelationalContext ctx) {{
            List<mathParser.AdditiveContext> additives = ctx.additive();
            if (additives.size() == 1) return visit(additives.get(0));
            List<Node> operands = new ArrayList<>();
            for (mathParser.AdditiveContext a : additives) operands.add(visit(a));
            List<String> kinds = new ArrayList<>();
            for (mathParser.RelopContext r : ctx.relop()) kinds.add(RELOP_KIND.get(r.getText()));
            return buildRelational(operands, kinds);
        }}

        @Override
        public Node visitAdditive(mathParser.AdditiveContext ctx) {{
            List<mathParser.MultiplicativeContext> muls = ctx.multiplicative();
            Node node = visit(muls.get(0));
            int idx = 1;
            for (int i = 1; i < ctx.getChildCount(); i += 2) {{
                String opText = ctx.getChild(i).getText();
                Node rhs = visit(muls.get(idx));
                idx++;
                node = new Node(opText.equals("+") ? NodeType.ADD : NodeType.SUB, null, null, List.of(node, rhs));
            }}
            return node;
        }}

        @Override
        public Node visitMultiplicative(mathParser.MultiplicativeContext ctx) {{
            List<mathParser.UnaryContext> units = ctx.unary();
            Node node = visit(units.get(0));
            int idx = 1;
            for (int i = 1; i < ctx.getChildCount(); i += 2) {{
                String opText = ctx.getChild(i).getText();
                Node rhs = visit(units.get(idx));
                idx++;
                if (opText.equals("*")) {{
                    node = new Node(NodeType.MUL, null, null, List.of(node, rhs));
                }} else if (opText.equals("/")) {{
                    node = new Node(NodeType.DIV, null, null, List.of(node, rhs));
                }} else {{
                    // infix '%' is rem(), dividend's-sign semantics (Grammar)
                    node = new Node(NodeType.FUNCTION_CALL, null, "rem", List.of(node, rhs));
                }}
            }}
            return node;
        }}

        @Override
        public Node visitUnaryOp(mathParser.UnaryOpContext ctx) {{
            String opText = ctx.getChild(0).getText();
            Node operand = visit(ctx.unary());
            if (opText.equals("!")) {{
                return new Node(NodeType.FUNCTION_CALL, null, "not", List.of(operand));
            }}
            return new Node(opText.equals("-") ? NodeType.UMINUS : NodeType.UPLUS, null, null, List.of(operand));
        }}

        @Override
        public Node visitUnaryPower(mathParser.UnaryPowerContext ctx) {{ return visit(ctx.power()); }}

        @Override
        public Node visitPower(mathParser.PowerContext ctx) {{
            Node base = visit(ctx.atom());
            if (ctx.unary() != null) {{
                return new Node(NodeType.POW, null, null, List.of(base, visit(ctx.unary())));
            }}
            return base;
        }}

        @Override
        public Node visitNumberAtom(mathParser.NumberAtomContext ctx) {{
            return new Node(NodeType.NUMBER, ctx.getText(), null, List.of());
        }}

        @Override
        public Node visitReferenceAtom(mathParser.ReferenceAtomContext ctx) {{
            return new Node(NodeType.REFERENCE, ctx.getText(), null, List.of());
        }}

        @Override
        public Node visitIdentAtom(mathParser.IdentAtomContext ctx) {{
            return new Node(NodeType.NAME, null, ctx.getText(), List.of());
        }}

        @Override
        public Node visitCallAtom(mathParser.CallAtomContext ctx) {{
            String name = ctx.IDENTIFIER().getText();
            List<Node> args = new ArrayList<>();
            if (ctx.arglist() != null) {{
                for (mathParser.ExprContext e : ctx.arglist().expr()) args.add(visit(e));
            }}
            return new Node(NodeType.FUNCTION_CALL, null, name, args);
        }}

        @Override
        public Node visitArrayAtom(mathParser.ArrayAtomContext ctx) {{
            List<Node> args = new ArrayList<>();
            if (ctx.arglist() != null) {{
                for (mathParser.ExprContext e : ctx.arglist().expr()) args.add(visit(e));
            }}
            return new Node(NodeType.ARRAY, null, null, args);
        }}

        @Override
        public Node visitParenAtom(mathParser.ParenAtomContext ctx) {{ return visit(ctx.expr()); }}
    }}

    /** The Java ANTLR runtime's DefaultErrorStrategy.recoverInline() reports a
     * failed match() against the state sync() last deferred at (its
     * nextTokensContext bookkeeping), so a trailing-junk error reads "expecting
     * {{'&&', '||', ...}}"; the Python runtime does not track that and reports
     * the set at the state that actually failed ("expecting <EOF>"). Python is
     * the reference implementation, so this strategy is recoverInline() minus
     * the deferred-state bookkeeping, keeping the parse-message text of
     * Types-0001 identical across targets. */
    private static final class SimpleErrorStrategy extends DefaultErrorStrategy {{
        @Override
        public Token recoverInline(Parser recognizer) throws RecognitionException {{
            Token matchedSymbol = singleTokenDeletion(recognizer);
            if (matchedSymbol != null) {{
                recognizer.consume();
                return matchedSymbol;
            }}
            if (singleTokenInsertion(recognizer)) return getMissingSymbol(recognizer);
            throw new InputMismatchException(recognizer);
        }}
    }}

    private static final class CollectingErrorListener extends BaseErrorListener {{
        final List<String> errors = new ArrayList<>();

        @Override
        public void syntaxError(Recognizer<?, ?> recognizer, Object offendingSymbol, int line,
                                 int charPositionInLine, String msg, RecognitionException e) {{
            errors.add("line " + line + ":" + charPositionInLine + " " + msg);
        }}
    }}

    /** Parses a SED2 math string into a Node tree (Types-0001). Throws
     * MathSyntaxError with the parser's own message on any malformed
     * input. */
    public static Node parse(String text) {{
        CollectingErrorListener listener = new CollectingErrorListener();
        mathLexer lexer = new mathLexer(CharStreams.fromString(text));
        lexer.removeErrorListeners();
        lexer.addErrorListener(listener);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        mathParser parser = new mathParser(tokens);
        parser.setErrorHandler(new SimpleErrorStrategy());
        parser.removeErrorListeners();
        parser.addErrorListener(listener);
        mathParser.StartContext tree = parser.start();
        if (!listener.errors.isEmpty()) {{
            throw new MathSyntaxError(String.join("; ", listener.errors));
        }}
        return new Builder().visit(tree);
    }}
}}
'''


def _math_rules_java() -> str:
    """MathRules.java - Types-0001 through Types-0004 (Design.md's Math
    section), combined into one dispatcher (checkMathField) the way
    emit_python.py's _check_math_field wires together
    templates/python/rules/Types-000N.py's four `check()` functions. Unlike
    the other handwritten rules (one class each under templates/java/rules/),
    these four predate that mechanism and are simple and self-contained
    enough to stay together here. GENERATED - do not hand-edit; regenerate via
    generator/generate.py."""
    return f'''package {PKG};

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/** Types-0001..0004: the shared math-grammar rules any field with
 * FieldSpec.isMath (x-math) runs on its own literal string value - see
 * SedBase.validateOwn(). GENERATED - do not hand-edit; regenerate via
 * generator/generate.py. */
public final class MathRules {{
    private MathRules() {{}}

    /** value is the field's own raw string - never a reference: SedBase's
     * validateOwn() only calls here for a literal string value (Types-
     * 0001.md: "When the math attribute is itself a reference, ... apply
     * only if the reference resolves statically to a string constant" -
     * not implemented by either target: a reference-form value goes to the
     * reference rules instead). Returns [] if value parses and every function
     * call / bare identifier it contains checks out; otherwise one
     * ValidationProblem per violation (Types-0001 short-circuits the rest,
     * same as emit_python.py's _check_math_field - an unparseable
     * expression has no tree left to walk for 0002-0004). */
    public static List<ValidationProblem> checkMathField(
            String value, String className, String idValue, String attr, String location) {{
        List<ValidationProblem> problems = new ArrayList<>();
        MathAst.Node ast;
        try {{
            ast = MathAst.parse(value);
        }} catch (MathAst.MathSyntaxError e) {{
            Map<String, Object> ph = new HashMap<>();
            ph.put("attr", attr);
            ph.put("class", className);
            ph.put("id", idValue);
            ph.put("expr", value);
            ph.put("parse-message", e.getMessage());
            problems.add(RuleCatalog.makeProblem("Types-0001", location, ph));
            return problems;
        }}
        if (Handwritten.HAS_REFERENCE_RULES) {{
            // SEDBase-0005.md: the root-collection rule also applies to a
            // REFERENCE token embedded in a math string.
            for (MathAst.Node node : ast.walk()) {{
                if (node.isReference()) {{
                    problems.addAll(Handwritten.sedBase0005(
                            References.parse(node.text), className, idValue, attr, location));
                }}
            }}
        }}
        for (MathAst.Node node : ast.walk()) {{
            if (node.isFunctionCall() && !PredefinedFunctions.FUNCTIONS.containsKey(node.name)) {{
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", attr);
                ph.put("class", className);
                ph.put("id", idValue);
                ph.put("function", node.name);
                problems.add(RuleCatalog.makeProblem("Types-0002", location, ph));
            }}
        }}
        for (MathAst.Node node : ast.walk()) {{
            if (!node.isFunctionCall()) continue;
            PredefinedFunctions.Arity spec = PredefinedFunctions.FUNCTIONS.get(node.name);
            if (spec == null) continue;  // Types-0002's concern, not a duplicate diagnosis here
            int count = node.getNumChildren();
            if (!spec.ok(count)) {{
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", attr);
                ph.put("class", className);
                ph.put("id", idValue);
                ph.put("function", node.name);
                ph.put("count", count);
                ph.put("expected-count", spec.format());
                problems.add(RuleCatalog.makeProblem("Types-0003", location, ph));
            }}
        }}
        for (MathAst.Node node : ast.walk()) {{
            if (node.isName() && !PredefinedFunctions.CONSTANTS.contains(node.name)) {{
                Map<String, Object> ph = new HashMap<>();
                ph.put("attr", attr);
                ph.put("class", className);
                ph.put("id", idValue);
                ph.put("value", node.name);
                problems.add(RuleCatalog.makeProblem("Types-0004", location, ph));
            }}
        }}
        return problems;
    }}
}}
'''


def _normalize_arity_java(raw) -> tuple:
    """Same two-shape contract as emit_python.py's _normalize_arity
    (kept as an independent copy rather than a cross-module import - see
    this module's docstring on Java/Python emitters staying self-
    contained): ("set", sorted_list_of_ints) for a fixed handful of allowed
    counts, or ("range", min, max) with max possibly None for unbounded."""
    if isinstance(raw, bool):
        raise ValueError(f"unrecognized arity shape: {raw!r}")
    if isinstance(raw, int):
        return ("set", [raw])
    if isinstance(raw, list):
        return ("set", sorted(set(raw)))
    if isinstance(raw, dict):
        return ("range", raw.get("min", 0), raw.get("max"))
    raise ValueError(f"unrecognized arity shape: {raw!r}")


def emit_predefined_functions_java(registry_path: str | None = None) -> str:
    """Java analog of emit_python.py's emit_predefined_functions_py -
    compiles schema/predefined-functions.json into PredefinedFunctions.java
    (FUNCTIONS: name -> Arity, CONSTANTS: set of names) for MathRules.java's
    Types-0002/-0003/-0004 checks. Pure derived data (Design.md's
    Validation section), so generated fresh every run like its Python
    counterpart, not copied from a template."""
    registry_path = registry_path or os.path.join(_repo_root(), "schema", "predefined-functions.json")
    with open(registry_path) as f:
        registry = _json.load(f)
    functions: dict[str, tuple] = {}
    for entry in registry.get("functions", []):
        functions[entry["name"]] = _normalize_arity_java(entry["arity"])
    for entry in registry.get("distrib", []):
        lengths = sorted(set(len(variant) for variant in entry["variants"]))
        functions[entry["name"]] = ("set", lengths)
    constants = sorted(set(entry["name"] for entry in registry.get("constants", [])))

    def _fmt_entry(name: str, spec: tuple) -> str:
        if spec[0] == "set":
            vals = ", ".join(str(v) for v in spec[1])
            return f"        FUNCTIONS.put({_java_lit(name)}, Arity.ofSet({vals}));"
        _, lo, hi = spec
        hi_lit = "null" if hi is None else str(hi)
        return f"        FUNCTIONS.put({_java_lit(name)}, Arity.ofRange({lo}, {hi_lit}));"

    lines = [
        f"package {PKG};",
        "",
        "import java.util.ArrayList;",
        "import java.util.Arrays;",
        "import java.util.HashMap;",
        "import java.util.HashSet;",
        "import java.util.List;",
        "import java.util.Map;",
        "import java.util.Set;",
        "import java.util.TreeSet;",
        "",
        "/** Compiled math function/constant registry for Types-0002/-0003/-0004's",
        " * math-grammar checks (mirrors generator/emit_python.py's",
        " * emit_predefined_functions_py / _predefined_functions.py). GENERATED",
        " * from schema/predefined-functions.json by generator/generate.py - do",
        " * not hand-edit. */",
        "public final class PredefinedFunctions {",
        "    private PredefinedFunctions() {}",
        "",
        "    /** ('set', {2, 4}) for a fixed handful of allowed argument counts",
        "     * (an exact arity normalizes to a one-element set), or ('range', min,",
        "     * max) with max possibly null for unbounded (e.g. min/max/sum's",
        '     * {"min": 1, "max": null}) - same two-shape contract as',
        "     * emit_python.py's _normalize_arity / templates/python/rules/",
        "     * Types-0003.py's _arity_ok/_format_arity. */",
        "    public static final class Arity {",
        "        public final boolean isRange;",
        "        public final Set<Integer> values;  // set only",
        "        public final int min;              // range only",
        "        public final Integer max;          // range only; null = unbounded",
        "",
        "        private Arity(boolean isRange, Set<Integer> values, int min, Integer max) {",
        "            this.isRange = isRange;",
        "            this.values = values;",
        "            this.min = min;",
        "            this.max = max;",
        "        }",
        "",
        "        static Arity ofSet(int... vals) {",
        "            Set<Integer> s = new TreeSet<>();",
        "            for (int v : vals) s.add(v);",
        "            return new Arity(false, s, 0, null);",
        "        }",
        "",
        "        static Arity ofRange(int lo, Integer hi) {",
        "            return new Arity(true, null, lo, hi);",
        "        }",
        "",
        "        public boolean ok(int count) {",
        "            if (!isRange) return values.contains(count);",
        "            return count >= min && (max == null || count <= max);",
        "        }",
        "",
        '        /** Renders this arity for a {expected-count} placeholder -',
        '         * "2 or 4", "1", "1 or more", "2 to 4". */',
        "        public String format() {",
        "            if (!isRange) {",
        "                List<String> parts = new ArrayList<>();",
        "                for (int v : values) parts.add(String.valueOf(v));",
        '                return String.join(" or ", parts);',
        "            }",
        '            if (max == null) return min + " or more";',
        "            if (min == max) return String.valueOf(min);",
        '            return min + " to " + max;',
        "        }",
        "    }",
        "",
        "    public static final Map<String, Arity> FUNCTIONS = new HashMap<>();",
        "    public static final Set<String> CONSTANTS = new HashSet<>(Arrays.asList(",
        "        " + ", ".join(_java_lit(c) for c in constants),
        "    ));",
        "",
        "    static {",
    ]
    for name in sorted(functions):
        lines.append(_fmt_entry(name, functions[name]))
    lines.append("    }")
    lines.append("}")
    lines.append("")
    return "\n".join(lines) + "\n"


# ---- BEGIN embedded reference-machinery runtime (Java sources) ----
# Hand-authored Java for the reference-resolution / outputs.json machinery
# (Java port of the corresponding half of emit_python.py's RUNTIME and
# OUTPUTS_SHAPE_PY - see each file's own header). Kept as verbatim Java text
# with an @PKG@ placeholder for the package (rather than f-strings, which
# would need every brace doubled); runtime_files() substitutes the package
# and emits one file per entry, identical for every spec, like the other
# runtime pieces above.
_STATIC_RUNTIME_JAVA = {
    'Dim.java': r'''package @PKG@;

import java.util.List;
import java.util.Objects;

/** One statically-resolved dimension of a task output's shape (see
 * OutputsShape.resolveDims): its size and labels when known, and where
 * that knowledge comes from. GENERATED - do not hand-edit; regenerate via
 * generator/generate.py. */
public final class Dim {
    public final Long size;             // null when not statically known
    public final List<String> labels;   // null when not statically known
    public final String source;         // "static" | "input-file" | "runtime" | null
    public final Long min;              // guaranteed minimum size, or null

    public Dim(Long size, List<String> labels, String source, Long min) {
        this.size = size;
        this.labels = labels;
        this.source = source;
        this.min = min;
    }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Dim)) return false;
        Dim d = (Dim) o;
        return Objects.equals(size, d.size) && Objects.equals(labels, d.labels)
                && Objects.equals(source, d.source) && Objects.equals(min, d.min);
    }

    @Override
    public int hashCode() { return Objects.hash(size, labels, source, min); }
}
''',
    'IdCollection.java': r'''package @PKG@;

import java.util.List;

/** Read-only, type-erased view of an ID-keyed collection field (a "dict" of
 * elements or an "any-dict" of raw JSON values), so reference resolution
 * (References.getSedReference) can walk any class's containment tree
 * generically. GENERATED - do not hand-edit; regenerate via
 * generator/generate.py. */
public interface IdCollection {
    List<String> ids();

    boolean has(String itemId);

    /** The entry stored under itemId: a SedBase element for a "dict"
     * collection, a raw JsonNode for an "any-dict" one. */
    Object getObject(String itemId);
}
''',
    'OutputsShape.java': r'''package @PKG@;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

/** outputs.json expr/valid notation (core-spec.md Section 8) - parser,
 * evaluator, and shape/hasSubvalue() resolver, backing SEDBase-0008 through
 * -0015 (Design.md's Validation section) and the formulaic ref-type rules
 * that piggyback on SEDBase-0015's scalar-reduction check. Java port of
 * OUTPUTS_SHAPE_PY in generator/emit_python.py (the reference
 * implementation); like it, a small runtime interpreter of the notation
 * rather than code compiled per suffix entry.
 *
 * Values inside an expression are plain Java objects mirroring the Python
 * ones: null (JSON null), Boolean, Long / BigInteger (integers), Double,
 * String, List (arrays and computed lists), Map (objects), Dim (a resolved
 * dimension), and the OUTERMOST sentinel. GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class OutputsShape {
    private OutputsShape() {}

    private static final ObjectMapper MAPPER = new ObjectMapper();

    /** Parses one class's embedded outputs.json text. */
    public static JsonNode parseJson(String text) {
        try {
            return MAPPER.readTree(text);
        } catch (java.io.IOException e) {
            throw new IllegalStateException("bad embedded outputs.json: " + e.getMessage(), e);
        }
    }

    /** Raised whenever an expr can't be evaluated against the target's own
     * literal fields - a reference where a literal was needed, a missing
     * attribute, an unresolvable shape dependency, a depth guard, and so on.
     * Every caller treats it as "the rule does not fire". */
    public static final class NotStatic extends RuntimeException {
        public NotStatic(String message) { super(message, null, false, false); }
    }

    /** Raised by indexIntoLiteral when the index chain can't be applied to a
     * constant's own literal structure - the signal SEDBase-0012 fires on. */
    public static final class NotIndexable extends RuntimeException {
        public final String bad;   // the failing index as Python would print it
        public final RefIndex index;   // the failing index, or null

        public NotIndexable(String bad) {
            this(bad, null);
        }

        public NotIndexable(String bad, RefIndex index) {
            super(bad, null, false, false);
            this.bad = bad;
            this.index = index;
        }
    }

    public static final Object OUTERMOST = new Object() {
        @Override public String toString() { return "OUTERMOST"; }
    };

    // ---- value helpers ---------------------------------------------------

    /** JSON -> the Java object model described in the class comment. */
    public static Object fromJson(JsonNode n) {
        if (n == null || n.isNull() || n.isMissingNode()) return null;
        if (n.isBoolean()) return n.booleanValue();
        if (n.isTextual()) return n.textValue();
        if (n.isIntegralNumber()) {
            BigInteger b = n.bigIntegerValue();
            return b.bitLength() < 64 ? (Object) b.longValue() : (Object) b;
        }
        if (n.isNumber()) return n.doubleValue();
        if (n.isArray()) {
            List<Object> out = new ArrayList<>();
            for (JsonNode c : n) out.add(fromJson(c));
            return out;
        }
        Map<String, Object> out = new LinkedHashMap<>();
        Iterator<Map.Entry<String, JsonNode>> it = n.fields();
        while (it.hasNext()) {
            Map.Entry<String, JsonNode> e = it.next();
            out.put(e.getKey(), fromJson(e.getValue()));
        }
        return out;
    }

    private static boolean isNumber(Object o) {
        return o instanceof Long || o instanceof BigInteger || o instanceof Double;
    }

    private static boolean isRefValue(Object o) {
        return o instanceof String && ((String) o).startsWith("#");
    }

    private static boolean isInt(Object o) { return o instanceof Long || o instanceof BigInteger; }

    private static double dbl(Object o) {
        if (o instanceof Long) return (Long) o;
        if (o instanceof BigInteger) return ((BigInteger) o).doubleValue();
        return (Double) o;
    }

    private static BigInteger big(Object o) {
        return o instanceof Long ? BigInteger.valueOf((Long) o) : (BigInteger) o;
    }

    private static Object normInt(BigInteger b) {
        return b.bitLength() < 64 ? (Object) b.longValue() : (Object) b;
    }

    /** Python truthiness. */
    static boolean truthy(Object o) {
        if (o == null) return false;
        if (o instanceof Boolean) return (Boolean) o;
        if (o instanceof Long) return (Long) o != 0L;
        if (o instanceof BigInteger) return ((BigInteger) o).signum() != 0;
        if (o instanceof Double) return (Double) o != 0.0;
        if (o instanceof String) return !((String) o).isEmpty();
        if (o instanceof List) return !((List<?>) o).isEmpty();
        if (o instanceof Map) return !((Map<?, ?>) o).isEmpty();
        return true;
    }

    private static Object numOfBool(Object o) {
        if (o instanceof Boolean) return ((Boolean) o) ? 1L : 0L;
        return o;
    }

    /** Python == over the value model (True == 1, 1 == 1.0). */
    static boolean pyEq(Object a, Object b) {
        a = numOfBool(a);
        b = numOfBool(b);
        if (a == null || b == null) return a == b;
        if (isNumber(a) && isNumber(b)) {
            if (isInt(a) && isInt(b)) return big(a).equals(big(b));
            return dbl(a) == dbl(b);
        }
        if (a instanceof String && b instanceof String) return a.equals(b);
        if (a instanceof List && b instanceof List) {
            List<?> x = (List<?>) a, y = (List<?>) b;
            if (x.size() != y.size()) return false;
            for (int i = 0; i < x.size(); i++) if (!pyEq(x.get(i), y.get(i))) return false;
            return true;
        }
        if (a instanceof Map && b instanceof Map) {
            Map<?, ?> x = (Map<?, ?>) a, y = (Map<?, ?>) b;
            if (x.size() != y.size()) return false;
            for (Map.Entry<?, ?> e : x.entrySet()) {
                if (!y.containsKey(e.getKey())) return false;
                if (!pyEq(e.getValue(), y.get(e.getKey()))) return false;
            }
            return true;
        }
        if (a instanceof Dim && b instanceof Dim) return a.equals(b);
        return a == b;
    }

    // ---- lexer -------------------------------------------------------------

    private static final class Tok {
        final String kind, text;
        Tok(String kind, String text) { this.kind = kind; this.text = text; }
        @Override public String toString() { return "(" + kind + ", " + text + ")"; }
    }

    private static List<Tok> tokenize(String text) {
        List<Tok> toks = new ArrayList<>();
        int i = 0, n = text.length();
        while (i < n) {
            char ch = text.charAt(i);
            if (Character.isWhitespace(ch)) { i++; continue; }
            if (ch == '=' && text.startsWith("==", i)) { toks.add(new Tok("==", "==")); i += 2; continue; }
            if ("+-!(),[].".indexOf(ch) >= 0) { toks.add(new Tok(String.valueOf(ch), String.valueOf(ch))); i++; continue; }
            if (isDigit(ch) || (ch == '.' && i + 1 < n && isDigit(text.charAt(i + 1)))) {
                int j = i;
                while (j < n && (isDigit(text.charAt(j)) || text.charAt(j) == '.')) j++;
                toks.add(new Tok("NUMBER", text.substring(i, j)));
                i = j;
                continue;
            }
            if (isAlpha(ch) || ch == '_') {
                int j = i;
                while (j < n && (isAlpha(text.charAt(j)) || isDigit(text.charAt(j)) || text.charAt(j) == '_')) j++;
                String word = text.substring(i, j);
                if (word.equals("true") || word.equals("false")) toks.add(new Tok("BOOL", word));
                else if (word.equals("or") || word.equals("if") || word.equals("else")) toks.add(new Tok(word, word));
                else toks.add(new Tok("IDENT", word));
                i = j;
                continue;
            }
            throw new NotStatic("unexpected character '" + ch + "' in expr '" + text + "'");
        }
        toks.add(new Tok("EOF", ""));
        return toks;
    }

    private static boolean isDigit(char c) { return c >= '0' && c <= '9'; }

    private static boolean isAlpha(char c) { return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'); }

    // ---- AST ---------------------------------------------------------------

    interface Node {}
    record Num(Object value) implements Node {}
    record Bool(boolean value) implements Node {}
    record ArrayLit(List<Node> items) implements Node {}
    record Path(List<String> names) implements Node {}
    record Call(String func, List<Node> args) implements Node {}
    record UnaryNot(Node operand) implements Node {}
    record BinOp(String op, Node left, Node right) implements Node {}
    record Conditional(Node cond, Node then, Node orelse) implements Node {}

    private static final List<String> FUNCS = List.of("len", "keys", "shapeOf", "dim", "provided");

    private static final class Parser {
        private final List<Tok> toks;
        private int i = 0;

        Parser(List<Tok> toks) { this.toks = toks; }

        private Tok peek() { return toks.get(i); }

        private Tok eat(String kind) {
            Tok t = toks.get(i);
            if (!t.kind.equals(kind)) throw new NotStatic("expected " + kind + ", got " + t);
            i++;
            return t;
        }

        Node parse() {
            Node node = conditional();
            eat("EOF");
            return node;
        }

        private Node conditional() {
            Node node = orExpr();
            if (peek().kind.equals("if")) {
                eat("if");
                Node cond = orExpr();
                eat("else");
                Node orelse = conditional();
                return new Conditional(cond, node, orelse);
            }
            return node;
        }

        private Node orExpr() {
            Node node = equality();
            while (peek().kind.equals("or")) {
                eat("or");
                node = new BinOp("or", node, equality());
            }
            return node;
        }

        private Node equality() {
            Node node = additive();
            if (peek().kind.equals("==")) {
                eat("==");
                node = new BinOp("==", node, additive());
            }
            return node;
        }

        private Node additive() {
            Node node = unary();
            while (peek().kind.equals("+") || peek().kind.equals("-")) {
                String op = eat(peek().kind).kind;
                node = new BinOp(op, node, unary());
            }
            return node;
        }

        private Node unary() {
            if (peek().kind.equals("!")) {
                eat("!");
                return new UnaryNot(unary());
            }
            return primary();
        }

        private Node primary() {
            Tok t = peek();
            String kind = t.kind, text = t.text;
            if (kind.equals("NUMBER")) {
                eat("NUMBER");
                try {
                    if (text.contains(".")) return new Num(Double.parseDouble(text));
                    BigInteger b = new BigInteger(text);
                    return new Num(normInt(b));
                } catch (NumberFormatException e) {
                    throw new NotStatic("bad number '" + text + "'");
                }
            }
            if (kind.equals("BOOL")) {
                eat("BOOL");
                return new Bool(text.equals("true"));
            }
            if (kind.equals("[")) {
                eat("[");
                List<Node> items = new ArrayList<>();
                if (!peek().kind.equals("]")) {
                    items.add(conditional());
                    while (peek().kind.equals(",")) { eat(","); items.add(conditional()); }
                }
                eat("]");
                return new ArrayLit(items);
            }
            if (kind.equals("IDENT")) {
                String name = eat("IDENT").text;
                if (peek().kind.equals("(") && FUNCS.contains(name)) {
                    eat("(");
                    List<Node> args = new ArrayList<>();
                    if (!peek().kind.equals(")")) {
                        args.add(conditional());
                        while (peek().kind.equals(",")) { eat(","); args.add(conditional()); }
                    }
                    eat(")");
                    return new Call(name, args);
                }
                List<String> names = new ArrayList<>();
                names.add(name);
                while (peek().kind.equals(".")) { eat("."); names.add(eat("IDENT").text); }
                return new Path(names);
            }
            throw new NotStatic("unexpected token " + peek() + " in expr");
        }
    }

    private static final Map<String, Node> PARSE_CACHE = new HashMap<>();

    static Node parseExpr(String text) {
        synchronized (PARSE_CACHE) {
            Node node = PARSE_CACHE.get(text);
            if (node == null) {
                node = new Parser(tokenize(text)).parse();
                PARSE_CACHE.put(text, node);
            }
            return node;
        }
    }

    // ---- scopes --------------------------------------------------------------

    /** Bare identifiers resolve against a task's own raw JSON field values
     * (core-spec.md: "A bare identifier names one of the task's own
     * attributes and evaluates to its value"), or, inside a "repeat"
     * dimension, against the current array entry ("self" is the entry). */
    interface Scope {
        Object lookup(String name);
        boolean provided(String name);
    }

    private static final class FieldScope implements Scope {
        private final JsonNode fields;
        FieldScope(JsonNode fields) { this.fields = fields; }

        @Override public Object lookup(String name) {
            if (!fields.has(name)) throw new NotStatic("attribute '" + name + "' not provided");
            return fromJson(fields.get(name));
        }

        @Override public boolean provided(String name) { return fields.has(name); }
    }

    private static final class RepeatScope implements Scope {
        private final Object entry;
        RepeatScope(Object entry) { this.entry = entry; }

        @Override public Object lookup(String name) {
            if (name.equals("self")) return entry;
            if (!(entry instanceof Map) || !((Map<?, ?>) entry).containsKey(name)) {
                throw new NotStatic("attribute '" + name + "' not provided on repeat entry");
            }
            return ((Map<?, ?>) entry).get(name);
        }

        @Override public boolean provided(String name) {
            if (name.equals("self")) return true;
            return entry instanceof Map && ((Map<?, ?>) entry).containsKey(name);
        }
    }

    // ---- evaluation --------------------------------------------------------

    private static Object resolvePath(Path node, Scope scope) {
        if (node.names().get(0).equals("outermost")) {
            if (node.names().size() != 1) throw new NotStatic("outermost is not a container");
            return OUTERMOST;
        }
        Object value = scope.lookup(node.names().get(0));
        for (int i = 1; i < node.names().size(); i++) {
            String seg = node.names().get(i);
            if (!(value instanceof Map) || !((Map<?, ?>) value).containsKey(seg)) {
                throw new NotStatic("attribute '" + String.join(".", node.names()) + "' not provided");
            }
            value = ((Map<?, ?>) value).get(seg);
        }
        return value;
    }

    private static boolean isProvided(Node node, Scope scope) {
        if (!(node instanceof Path)) throw new NotStatic("provided() needs a bare identifier or dotted path");
        List<String> names = ((Path) node).names();
        if (names.get(0).equals("outermost")) return true;
        if (names.size() == 1) return scope.provided(names.get(0));
        Object value;
        try {
            value = scope.lookup(names.get(0));
        } catch (NotStatic e) {
            return false;
        }
        for (int i = 1; i < names.size() - 1; i++) {
            if (!(value instanceof Map) || !((Map<?, ?>) value).containsKey(names.get(i))) return false;
            value = ((Map<?, ?>) value).get(names.get(i));
        }
        return value instanceof Map && ((Map<?, ?>) value).containsKey(names.get(names.size() - 1));
    }

    private static Object fnLen(Object value) {
        if (value instanceof List) return (long) ((List<?>) value).size();
        if (value instanceof Map) {
            Map<?, ?> m = (Map<?, ?>) value;
            // Range-family dispatch (core-spec.md): len(x.values) if
            // provided(x.values) else x.numberOfSteps + 1; anything else
            // object-shaped is a plain SId-keyed map, so len() is its key
            // count.
            if (m.containsKey("values")) {
                Object values = m.get("values");
                if (values instanceof List) return (long) ((List<?>) values).size();
                throw new NotStatic("values is not a literal array");
            }
            if (m.containsKey("numberOfSteps")) {
                Object steps = m.get("numberOfSteps");
                if (isNumber(steps)) return toLongTrunc(steps) + 1;
                throw new NotStatic("numberOfSteps is not a literal number");
            }
            return (long) m.size();
        }
        throw new NotStatic("len() needs a literal array, object, or Range-family value");
    }

    private static long toLongTrunc(Object n) {
        if (n instanceof Long) return (Long) n;
        if (n instanceof BigInteger) return RefIndex.saturate((BigInteger) n);
        double d = (Double) n;
        if (Double.isNaN(d) || Double.isInfinite(d)) throw new NotStatic("non-finite number");
        return (long) d;
    }

    private static Object fnKeys(Object value) {
        if (!(value instanceof Map)) throw new NotStatic("keys() needs a literal object");
        return new ArrayList<Object>(((Map<?, ?>) value).keySet());
    }

    static Object eval(Node node, Scope scope, Function<String, List<Dim>> shapeOf) {
        if (node instanceof Num) return ((Num) node).value();
        if (node instanceof Bool) return ((Bool) node).value();
        if (node instanceof ArrayLit) {
            List<Object> out = new ArrayList<>();
            for (Node item : ((ArrayLit) node).items()) out.add(eval(item, scope, shapeOf));
            return out;
        }
        if (node instanceof Path) return resolvePath((Path) node, scope);
        if (node instanceof UnaryNot) return !truthy(eval(((UnaryNot) node).operand(), scope, shapeOf));
        if (node instanceof Call) {
            Call call = (Call) node;
            switch (call.func()) {
                case "provided":
                    if (call.args().size() != 1) throw new NotStatic("provided() takes exactly one argument");
                    return isProvided(call.args().get(0), scope);
                case "len":
                    if (call.args().isEmpty()) throw new NotStatic("len() takes one argument");
                    return fnLen(eval(call.args().get(0), scope, shapeOf));
                case "keys":
                    if (call.args().isEmpty()) throw new NotStatic("keys() takes one argument");
                    return fnKeys(eval(call.args().get(0), scope, shapeOf));
                case "shapeOf": {
                    if (call.args().isEmpty()) throw new NotStatic("shapeOf() takes one argument");
                    Object ref = eval(call.args().get(0), scope, shapeOf);
                    if (!(ref instanceof String) || !((String) ref).startsWith("#")) {
                        throw new NotStatic("shapeOf() needs a reference-valued operand");
                    }
                    return shapeOf.apply((String) ref);
                }
                case "dim": {
                    if (call.args().size() != 1) throw new NotStatic("dim() takes exactly one argument");
                    Object value = eval(call.args().get(0), scope, shapeOf);
                    if (value == OUTERMOST) {
                        List<Object> l = new ArrayList<>();
                        l.add(OUTERMOST);
                        return l;
                    }
                    if (value instanceof String) {
                        List<Object> l = new ArrayList<>();
                        l.add(value);
                        return l;
                    }
                    if (value instanceof List) return value;
                    throw new NotStatic("dim() needs a name or a list of names");
                }
                default:
                    throw new NotStatic("unknown function " + call.func() + "()");
            }
        }
        if (node instanceof BinOp) {
            BinOp b = (BinOp) node;
            if (b.op().equals("or")) {
                if (isProvided(b.left(), scope)) return eval(b.left(), scope, shapeOf);
                return eval(b.right(), scope, shapeOf);
            }
            Object left = eval(b.left(), scope, shapeOf);
            if (b.op().equals("-")) {
                Object right = eval(b.right(), scope, shapeOf);
                return applyDimMinus(left, right);
            }
            Object right = eval(b.right(), scope, shapeOf);
            if (b.op().equals("==")) {
                if (isRefValue(left) || isRefValue(right)) throw new NotStatic("== operand is a reference");
                return pyEq(left, right);
            }
            if (b.op().equals("+")) {
                if (left instanceof List && right instanceof List) {
                    List<Object> out = new ArrayList<>((List<?>) left);
                    out.addAll((List<?>) right);
                    return out;
                }
                if (isNumber(left) && isNumber(right)) {
                    if (isInt(left) && isInt(right)) return normInt(big(left).add(big(right)));
                    return dbl(left) + dbl(right);
                }
                throw new NotStatic("+ needs two arrays or two numbers");
            }
            throw new NotStatic("unknown operator " + b.op());
        }
        if (node instanceof Conditional) {
            Conditional c = (Conditional) node;
            if (truthy(eval(c.cond(), scope, shapeOf))) return eval(c.then(), scope, shapeOf);
            return eval(c.orelse(), scope, shapeOf);
        }
        throw new NotStatic("unknown AST node " + node);
    }

    /** shapeOf(x) - dim(y): a dims list (see resolveDims) with the
     * dimension(s) named by `selectors` removed. Only the reserved
     * `outermost` sentinel removes a SPECIFIC, still-fully-known dimension
     * (the first); anything else can only shrink the known dimension COUNT,
     * with the remaining dimensions' own details marked unknown. */
    private static Object applyDimMinus(Object dims, Object selectors) {
        if (dims == null) return null;
        if (!(dims instanceof List)) throw new NotStatic("- needs a dimensions list on the left");
        List<?> d = (List<?>) dims;
        int count = selectors instanceof List ? ((List<?>) selectors).size() : 1;
        if (count >= d.size()) return new ArrayList<Object>();
        if (selectors instanceof List && ((List<?>) selectors).size() == 1
                && ((List<?>) selectors).get(0) == OUTERMOST) {
            return new ArrayList<Object>(d.subList(1, d.size()));
        }
        List<Object> out = new ArrayList<>();
        for (int i = 0; i < d.size() - count; i++) out.add(new Dim(null, null, "runtime", null));
        return out;
    }

    // ---- outputs.json "sourced" value resolution ---------------------------

    private static String text(JsonNode n) {
        return (n != null && n.isTextual()) ? n.textValue() : null;
    }

    private static Long sizeOf(JsonNode n) {
        if (n == null || !n.isNumber()) return null;
        return n.isIntegralNumber() ? Long.valueOf(RefIndex.saturate(n.bigIntegerValue())) : Long.valueOf((long) n.doubleValue());
    }

    private static Long evalSourcedSize(JsonNode sourced, Scope scope, Function<String, List<Dim>> shapeOf) {
        if (sourced == null || sourced.isNull()) return null;
        if (!"static".equals(text(sourced.get("source")))) return null;   // runtime / input-file
        Object value;
        try {
            value = eval(parseExpr(text(sourced.get("expr"))), scope, shapeOf);
        } catch (NotStatic | NullPointerException e) {
            return null;
        }
        if (isNumber(value)) {
            try {
                return toLongTrunc(value);
            } catch (NotStatic e) {
                return null;
            }
        }
        return null;
    }

    /** null (JSON null) means "no labels for this dimension" - statically
     * known as empty, not "unresolvable" - so this returns an empty list for
     * that case, reserving null for a genuine failure to resolve. */
    @SuppressWarnings("unchecked")
    private static List<String> evalSourcedLabels(JsonNode spec, Scope scope, Function<String, List<Dim>> shapeOf) {
        if (spec == null || spec.isNull()) return new ArrayList<>();
        if (spec.isArray()) {
            List<String> out = new ArrayList<>();
            for (JsonNode c : spec) {
                if (!c.isTextual()) return null;
                out.add(c.textValue());
            }
            return out;
        }
        if (spec.isObject()) {
            if (!"static".equals(text(spec.get("source")))) return null;
            Object value;
            try {
                value = eval(parseExpr(text(spec.get("expr"))), scope, shapeOf);
            } catch (NotStatic | NullPointerException e) {
                return null;
            }
            if (value instanceof List) {
                List<String> out = new ArrayList<>();
                for (Object v : (List<Object>) value) {
                    if (!(v instanceof String)) return null;
                    out.add((String) v);
                }
                return out;
            }
            return null;
        }
        return null;
    }

    /** dimsSpec is outputs.json's own "dimensions" value for one suffix entry
     * - either a fixed-length array of per-dimension entries, or a single
     * "sourced" object describing the whole shape. Returns one Dim per
     * dimension, in order, or null when the dimension COUNT itself isn't
     * statically known. */
    @SuppressWarnings("unchecked")
    static List<Dim> resolveDims(JsonNode dimsSpec, Scope scope, Function<String, List<Dim>> shapeOf) {
        if (dimsSpec == null || dimsSpec.isNull()) return null;
        if (dimsSpec.isArray()) {
            List<Dim> result = new ArrayList<>();
            for (JsonNode d : dimsSpec) {
                if (d.has("repeat")) {
                    JsonNode rep = d.get("repeat");
                    Object overVal;
                    try {
                        overVal = scope.lookup(text(rep.get("over")));
                    } catch (NotStatic | NullPointerException e) {
                        return null;
                    }
                    if (!(overVal instanceof List)) return null;
                    for (Object item : (List<Object>) overVal) {
                        Scope itemScope = new RepeatScope(item);
                        JsonNode size = rep.get("size");
                        result.add(new Dim(evalSourcedSize(size, itemScope, shapeOf),
                                evalSourcedLabels(rep.get("labels"), itemScope, shapeOf),
                                text(size.get("source")), sizeOf(size.get("min"))));
                    }
                } else {
                    JsonNode size = d.get("size");
                    result.add(new Dim(evalSourcedSize(size, scope, shapeOf),
                            evalSourcedLabels(d.get("labels"), scope, shapeOf),
                            text(size.get("source")), sizeOf(size.get("min"))));
                }
            }
            return result;
        }
        // single sourced object - the whole shape's derivation
        if (!"static".equals(text(dimsSpec.get("source")))) return null;
        Object value;
        try {
            value = eval(parseExpr(text(dimsSpec.get("expr"))), scope, shapeOf);
        } catch (NotStatic | NullPointerException e) {
            return null;
        }
        if (!(value instanceof List)) return null;
        List<Dim> out = new ArrayList<>();
        for (Object o : (List<Object>) value) {
            if (!(o instanceof Dim)) return null;
            out.add((Dim) o);
        }
        return out;
    }

    /** Splits a reference's index list into its brackets: "[0:2, 1][3]" is
     * two groups, [0:2, 1] and [3] (RefIndex.sameBracket marks an index that
     * continues the previous one's bracket). */
    public static List<List<RefIndex>> indexGroups(List<RefIndex> indexAccessors) {
        List<List<RefIndex>> groups = new ArrayList<>();
        for (RefIndex idx : indexAccessors) {
            if (idx.sameBracket && !groups.isEmpty()) {
                groups.get(groups.size() - 1).add(idx);
            } else {
                List<RefIndex> g = new ArrayList<>();
                g.add(idx);
                groups.add(g);
            }
        }
        return groups;
    }

    /** The dimension a range index leaves behind: as many entries as the
     * range selects, with the matching labels. Whatever can't be told
     * statically (a runtime size, an out-of-bounds or empty range - the
     * latter is SEDBase-0011's to report) becomes unknown, so later indices
     * are not judged against a guess. */
    private static Dim slicedDim(Dim dim, RefIndex idx) {
        Long n = dim.size;
        Long a = idx.rangeStart, b = idx.rangeEnd;
        boolean ok = n != null && !(a != null && !(-n <= a && a <= n)) && !(b != null && !(-n <= b && b <= n));
        long ea = 0, eb = 0;
        if (ok) {
            ea = a != null ? a : 0;
            eb = b != null ? b : n;
            if (ea < 0) ea += n;
            if (eb < 0) eb += n;
            ok = ea < eb;
        }
        if (!ok) return new Dim(null, null, dim.source, null);
        List<String> labels = null;
        // An unlabeled dimension is stored as an empty label list and stays that
        // way; otherwise the labels of the selected entries are kept.
        if (dim.labels != null && dim.labels.isEmpty()) labels = new ArrayList<>();
        else if (dim.labels != null && dim.labels.size() == n) labels = new ArrayList<>(dim.labels.subList((int) ea, (int) eb));
        return new Dim(eb - ea, labels, dim.source, null);
    }

    /** The result of bindIndices: see that method. */
    public static final class Bound {
        public final List<Dim> seen;
        public final List<Dim> after;

        Bound(List<Dim> seen, List<Dim> after) {
            this.seen = seen;
            this.after = after;
        }
    }

    /** Applies a reference's own bracket indices to a resolved dims list.
     * Separate brackets chain (each applies to the result of the one before:
     * "[0:2][1]" indexes the first dimension twice); the indices inside one
     * bracket apply to consecutive dimensions ("[0:2, 1]" - numpy style). A
     * positional/label index drops its dimension from the result; a range
     * keeps it, narrowed to the entries it selects; dimensions no index
     * reaches pass through untouched. `seen` has one entry per index, in
     * order - the dimension that index is applied to, as the earlier indices
     * left it - and stops short when an index finds no dimension left
     * (SEDBase-0009); `after` is the dimensions of the result. Both null when
     * dims is null. */
    public static Bound bindIndices(List<Dim> dims, List<RefIndex> indexAccessors) {
        if (dims == null) return new Bound(null, null);
        List<Dim> view = new ArrayList<>(dims);
        List<Dim> seen = new ArrayList<>();
        for (List<RefIndex> group : indexGroups(indexAccessors)) {
            int k = Math.min(group.size(), view.size());
            seen.addAll(view.subList(0, k));
            if (k < group.size()) break;
            List<Dim> next = new ArrayList<>();
            for (int j = 0; j < view.size(); j++) {
                if (j < k) {
                    if (group.get(j).kind.equals("range")) next.add(slicedDim(view.get(j), group.get(j)));
                } else {
                    next.add(view.get(j));
                }
            }
            view = next;
        }
        return new Bound(seen, view);
    }

    static List<Dim> applyIndexChain(List<Dim> dims, List<RefIndex> indexAccessors) {
        return bindIndices(dims, indexAccessors).after;
    }

    /** A suffix entry that is listed in outputs.json is valid; one that isn't
     * listed is not (resolveOutput handles that). An entry's optional "valid"
     * field is a boolean expr string over the task's own fields meaning
     * "valid if"; no "valid" field means always valid. Returns TRUE/FALSE, or
     * null when the expr couldn't be evaluated statically ("the rule does not
     * fire"). */
    static Boolean evalValid(JsonNode entry, Scope scope, Function<String, List<Dim>> shapeOf) {
        JsonNode valid = entry.get("valid");
        if (valid == null) return Boolean.TRUE;
        if (valid.isTextual()) {
            try {
                return truthy(eval(parseExpr(valid.textValue()), scope, shapeOf));
            } catch (NotStatic e) {
                return null;
            }
        }
        return Boolean.FALSE;
    }

    /** The result of resolveOutput: see that method. */
    public static final class Resolution {
        /** TRUE (suffix is listed and has no "valid" field, or its "valid"
         * ("valid if") expr evaluated true), FALSE (not listed, or the expr
         * evaluates false), or null (couldn't be determined statically). */
        public final Boolean ok;
        public final JsonNode entry;            // the raw outputEntry, or null when the suffix key is absent
        public final List<Dim> dimsBefore;      // null unless ok == TRUE and the entry has resolvable "dimensions"
        public final List<Dim> dimsAfter;       // dimsBefore after the index chain
        public final String dotName;            // first dot-accessor, or null for a bare [id] reference
        public final List<RefIndex> indexAccessors;

        Resolution(Boolean ok, JsonNode entry, List<Dim> dimsBefore, List<Dim> dimsAfter, String dotName,
                   List<RefIndex> indexAccessors) {
            this.ok = ok;
            this.entry = entry;
            this.dimsBefore = dimsBefore;
            this.dimsAfter = dimsAfter;
            this.dotName = dotName;
            this.indexAccessors = indexAccessors;
        }
    }

    /** The core hasSubvalue()-style resolution SEDBase-0008 through -0011 /
     * -0014 / -0015 and the ref-type rules all share. outputsJson is a
     * concrete tasks/ class's own parsed outputs.json ({"outputs": {...}});
     * fields is the referenced task's own JSON value; accessors is a
     * ParsedReference's own accessor list. */
    public static Resolution resolveOutput(JsonNode outputsJson, JsonNode fields,
                                           List<ParsedReference.Accessor> accessors,
                                           Function<String, List<Dim>> shapeOf) {
        String dotName = null;
        List<RefIndex> indexAccessors = new ArrayList<>();
        for (ParsedReference.Accessor a : accessors) {
            if (a.isDot() && dotName == null) dotName = a.dotName;
            else if (!a.isDot()) indexAccessors.add(a.index);
        }
        String suffixKey = dotName == null ? "[id]" : "[id]." + dotName;
        JsonNode outputs = outputsJson == null ? null : outputsJson.get("outputs");
        JsonNode entry = outputs == null ? null : outputs.get(suffixKey);
        if (entry == null) return new Resolution(Boolean.FALSE, null, null, null, dotName, indexAccessors);
        Scope scope = new FieldScope(fields);
        Boolean ok = evalValid(entry, scope, shapeOf);
        if (!Boolean.TRUE.equals(ok)) return new Resolution(ok, entry, null, null, dotName, indexAccessors);
        List<Dim> dimsBefore = resolveDims(entry.get("dimensions"), scope, shapeOf);
        List<Dim> dimsAfter = applyIndexChain(dimsBefore, indexAccessors);
        return new Resolution(Boolean.TRUE, entry, dimsBefore, dimsAfter, dotName, indexAccessors);
    }

    // ---- SEDBase-0012: indexing into a constant's own literal JSON value ---

    /** core-spec.md / SEDBase-0012.md: constants have no outputs.json, their
     * "shape" is just their own literal JSON value. Applies an index chain
     * directly against it; `value` is the (already dereferenced) literal - a
     * JsonNode, or anything else (a document element, null) which is simply
     * not indexable. Throws NotIndexable the moment an index can't apply;
     * returns the fully-indexed value otherwise. */
    public static Object indexIntoLiteral(Object value, List<RefIndex> indexAccessors) {
        Object cur = value;
        for (List<RefIndex> group : indexGroups(indexAccessors)) cur = applyBracket(cur, group, 0);
        return cur;
    }

    private static NotIndexable notIndexable(RefIndex idx) {
        String bad;
        switch (idx.kind) {
            case "label": bad = idx.label; break;
            case "int": bad = idx.intText; break;
            case "range":
                bad = "(" + (idx.rangeStartText == null ? "None" : idx.rangeStartText) + ", "
                        + (idx.rangeEndText == null ? "None" : idx.rangeEndText) + ")";
                break;
            default: bad = idx.valueText();
        }
        return new NotIndexable(bad, idx);
    }

    /** One bracket's indices against a literal: the first applies to cur
     * itself, the rest to the corresponding dimension of what it selects (a
     * range selects several entries, so the rest applies inside each). */
    private static Object applyBracket(Object cur, List<RefIndex> group, int from) {
        if (from >= group.size()) return cur;
        RefIndex idx = group.get(from);
        JsonNode node = cur instanceof JsonNode ? (JsonNode) cur : null;
        switch (idx.kind) {
            case "label":
                if (node == null || !node.isObject() || !node.has(idx.label)) throw notIndexable(idx);
                return applyBracket(node.get(idx.label), group, from + 1);
            case "int": {
                if (node == null || !node.isArray()) throw notIndexable(idx);
                long n = node.size();
                long i = idx.intValue;
                if (i < -n || i >= n) throw notIndexable(idx);
                return applyBracket(node.get((int) (i < 0 ? i + n : i)), group, from + 1);
            }
            case "range": {
                if (node == null || !node.isArray()) throw notIndexable(idx);
                long n = node.size();
                long ea = idx.rangeStart != null ? idx.rangeStart : 0;
                long eb = idx.rangeEnd != null ? idx.rangeEnd : n;
                if (ea < 0) ea += n;
                if (eb < 0) eb += n;
                ea = Math.max(ea, 0);
                eb = Math.max(eb, 0);
                ArrayNode out = JsonNodeFactory.instance.arrayNode();
                for (long k = ea; k < Math.min(eb, n); k++) {
                    JsonNode el = node.get((int) k);
                    out.add(from + 1 >= group.size() ? el : (JsonNode) applyBracket(el, group, from + 1));
                }
                return out;
            }
            default:
                throw notIndexable(idx);
        }
    }
}
''',
    'ParsedReference.java': r'''package @PKG@;

import java.util.List;

/** A parsed reference string: '#' + colon-delimited containment path +
 * an optional chain of dot-accessors / bracket indices, e.g.
 * "#tasks:loop1:subTasks:sim1.model['S1']" (see References.parse). Pure
 * syntax - never touches a document. GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class ParsedReference {
    /** One accessor: either a dot-accessor (name) or a bracket index. */
    public static final class Accessor {
        public final String dotName;    // non-null for a dot-accessor
        public final RefIndex index;    // non-null for a bracket index

        public Accessor(String dotName, RefIndex index) {
            this.dotName = dotName;
            this.index = index;
        }

        public boolean isDot() { return dotName != null; }
    }

    public final String raw;
    public final String collection;        // the segment right after '#', or null if empty
    public final List<String> path;        // colon-segments after the collection
    public final List<Accessor> accessors;

    public ParsedReference(String raw, String collection, List<String> path, List<Accessor> accessors) {
        this.raw = raw;
        this.collection = collection;
        this.path = path;
        this.accessors = accessors;
    }

    /** The first dot-accessor's name, or null. */
    public String firstDotName() {
        for (Accessor a : accessors) if (a.isDot()) return a.dotName;
        return null;
    }

    /** Every bracket index, in order, wherever it fell relative to a dot. */
    public List<RefIndex> indexAccessors() {
        List<RefIndex> out = new java.util.ArrayList<>();
        for (Accessor a : accessors) if (!a.isDot()) out.add(a.index);
        return out;
    }
}
''',
    'PyFmt.java': r'''package @PKG@;

import com.fasterxml.jackson.databind.JsonNode;

import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/** Python-compatible text rendering of parsed JSON values, so a validation
 * message reads identically across the Python, Java and C++ targets (the
 * reference implementation formats placeholders with Python's str(), and a
 * literal with json.dumps()). GENERATED - do not hand-edit; regenerate via
 * generator/generate.py. */
public final class PyFmt {
    private PyFmt() {}

    /** Python's repr() of a float (shortest round-trip digits, exponent form
     * outside 1e-4 .. 1e16). */
    public static String floatRepr(double d) {
        if (Double.isNaN(d)) return "nan";
        if (Double.isInfinite(d)) return d > 0 ? "inf" : "-inf";
        if (d == 0.0) return (1.0 / d < 0) ? "-0.0" : "0.0";
        String sign = d < 0 ? "-" : "";
        BigDecimal bd = new BigDecimal(Double.toString(Math.abs(d))).stripTrailingZeros();
        String digits = bd.unscaledValue().toString();
        int decpt = digits.length() - bd.scale();   // value = 0.DIGITS * 10^decpt
        String out;
        if (decpt > 16 || decpt <= -4) {
            int exp = decpt - 1;
            String mant = digits.length() > 1 ? digits.charAt(0) + "." + digits.substring(1) : digits;
            String es = Integer.toString(Math.abs(exp));
            if (es.length() < 2) es = "0" + es;
            out = mant + "e" + (exp < 0 ? "-" : "+") + es;
        } else if (decpt <= 0) {
            out = "0." + "0".repeat(-decpt) + digits;
        } else if (decpt >= digits.length()) {
            out = digits + "0".repeat(decpt - digits.length()) + ".0";
        } else {
            out = digits.substring(0, decpt) + "." + digits.substring(decpt);
        }
        return sign + out;
    }

    private static boolean printable(int cp) {
        int t = Character.getType(cp);
        switch (t) {
            case Character.CONTROL: case Character.FORMAT: case Character.SURROGATE:
            case Character.PRIVATE_USE: case Character.UNASSIGNED:
            case Character.LINE_SEPARATOR: case Character.PARAGRAPH_SEPARATOR:
                return false;
            case Character.SPACE_SEPARATOR:
                return cp == 0x20;
            default:
                return true;
        }
    }

    /** Python's repr() of a str. */
    public static String reprStr(String s) {
        boolean hasSingle = s.indexOf('\'') >= 0, hasDouble = s.indexOf('"') >= 0;
        char q = (hasSingle && !hasDouble) ? '"' : '\'';
        StringBuilder sb = new StringBuilder();
        sb.append(q);
        for (int i = 0; i < s.length(); ) {
            int cp = s.codePointAt(i);
            i += Character.charCount(cp);
            if (cp == q || cp == '\\') { sb.append('\\').appendCodePoint(cp); }
            else if (cp == '\n') sb.append("\\n");
            else if (cp == '\r') sb.append("\\r");
            else if (cp == '\t') sb.append("\\t");
            else if (cp < 0x20 || cp == 0x7f) sb.append(String.format("\\x%02x", cp));
            else if (cp < 0x7f || printable(cp)) sb.appendCodePoint(cp);
            else if (cp <= 0xff) sb.append(String.format("\\x%02x", cp));
            else if (cp <= 0xffff) sb.append(String.format("\\u%04x", cp));
            else sb.append(String.format("\\U%08x", cp));
        }
        sb.append(q);
        return sb.toString();
    }

    /** Python's repr() of the value json.loads() would produce for `n`. */
    public static String repr(JsonNode n) {
        if (n == null || n.isNull() || n.isMissingNode()) return "None";
        if (n.isBoolean()) return n.booleanValue() ? "True" : "False";
        if (n.isTextual()) return reprStr(n.textValue());
        if (n.isIntegralNumber()) return n.bigIntegerValue().toString();
        if (n.isNumber()) return floatRepr(n.doubleValue());
        StringBuilder sb = new StringBuilder();
        if (n.isArray()) {
            sb.append('[');
            boolean first = true;
            for (JsonNode c : n) { if (!first) sb.append(", "); first = false; sb.append(repr(c)); }
            return sb.append(']').toString();
        }
        sb.append('{');
        boolean first = true;
        Iterator<Map.Entry<String, JsonNode>> it = n.fields();
        while (it.hasNext()) {
            Map.Entry<String, JsonNode> e = it.next();
            if (!first) sb.append(", ");
            first = false;
            sb.append(reprStr(e.getKey())).append(": ").append(repr(e.getValue()));
        }
        return sb.append('}').toString();
    }

    /** Python's str() of the value json.loads() would produce for `n`. */
    public static String str(JsonNode n) {
        if (n != null && n.isTextual()) return n.textValue();
        return repr(n);
    }

    /** Python's str() of a placeholder value: a String is itself, a JsonNode
     * renders as its parsed Python value, a Boolean as True/False, null as
     * None. */
    public static String str(Object o) {
        if (o == null) return "None";
        if (o instanceof String) return (String) o;
        if (o instanceof JsonNode) return str((JsonNode) o);
        if (o instanceof Boolean) return ((Boolean) o) ? "True" : "False";
        if (o instanceof Double || o instanceof Float) return floatRepr(((Number) o).doubleValue());
        if (o instanceof List) {
            StringBuilder sb = new StringBuilder("[");
            boolean first = true;
            for (Object x : (List<?>) o) {
                if (!first) sb.append(", ");
                first = false;
                sb.append(x instanceof String ? reprStr((String) x) : str(x));
            }
            return sb.append(']').toString();
        }
        return String.valueOf(o);
    }

    private static void jsonString(StringBuilder sb, String s) {
        sb.append('"');
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"': sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                case '\b': sb.append("\\b"); break;
                case '\f': sb.append("\\f"); break;
                default:
                    if (c < 0x20 || c > 0x7e) sb.append(String.format("\\u%04x", (int) c));
                    else sb.append(c);
            }
        }
        sb.append('"');
    }

    /** Python's json.dumps() (default separators, ensure_ascii) of `n`. */
    public static String jsonDumps(JsonNode n) {
        StringBuilder sb = new StringBuilder();
        dumps(sb, n);
        return sb.toString();
    }

    private static void dumps(StringBuilder sb, JsonNode n) {
        if (n == null || n.isNull() || n.isMissingNode()) { sb.append("null"); return; }
        if (n.isBoolean()) { sb.append(n.booleanValue() ? "true" : "false"); return; }
        if (n.isTextual()) { jsonString(sb, n.textValue()); return; }
        if (n.isIntegralNumber()) { sb.append(n.bigIntegerValue().toString()); return; }
        if (n.isNumber()) {
            double d = n.doubleValue();
            if (Double.isNaN(d)) sb.append("NaN");
            else if (Double.isInfinite(d)) sb.append(d > 0 ? "Infinity" : "-Infinity");
            else sb.append(floatRepr(d));
            return;
        }
        if (n.isArray()) {
            sb.append('[');
            boolean first = true;
            for (JsonNode c : n) { if (!first) sb.append(", "); first = false; dumps(sb, c); }
            sb.append(']');
            return;
        }
        sb.append('{');
        boolean first = true;
        Iterator<Map.Entry<String, JsonNode>> it = n.fields();
        while (it.hasNext()) {
            Map.Entry<String, JsonNode> e = it.next();
            if (!first) sb.append(", ");
            first = false;
            jsonString(sb, e.getKey());
            sb.append(": ");
            dumps(sb, e.getValue());
        }
        sb.append('}');
    }

    /** str() of an integer as Python would print it. */
    public static String intStr(BigInteger b) { return b.toString(); }
}
''',
    'RefIndex.java': r'''package @PKG@;

import java.math.BigInteger;

/** One bracket index of a reference: [n] / [-n] ("int"), ['label'] ("label")
 * or [a:b] ("range", either end optional). GENERATED - do not hand-edit;
 * regenerate via generator/generate.py. */
public final class RefIndex {
    public final String kind;       // "int" | "label" | "range"
    public final long intValue;     // "int": the index (saturated to the long range)
    public final String intText;    // "int": the index as Python would print it
    public final String label;      // "label": the label
    public final Long rangeStart;   // "range": start (saturated to the long range), or null when open
    public final Long rangeEnd;     // "range": end (saturated to the long range), or null when open
    public final String rangeStartText;   // "range": the start as Python would print it, or null when open
    public final String rangeEndText;     // "range": the end as Python would print it, or null when open
    /** True when this index was written after a comma inside the same pair of
     * brackets as the previous index: "[0:2, 1]" is two indices, the second
     * flagged sameBracket. Separate brackets ("[0:2][1]") chain - each
     * bracket indexes the result of the one before - while the indices of one
     * bracket apply to consecutive dimensions of the value they start from,
     * like numpy's x[0:2, 1]. */
    public final boolean sameBracket;

    private RefIndex(RefIndex o, boolean sameBracket) {
        this.kind = o.kind;
        this.intValue = o.intValue;
        this.intText = o.intText;
        this.label = o.label;
        this.rangeStart = o.rangeStart;
        this.rangeEnd = o.rangeEnd;
        this.rangeStartText = o.rangeStartText;
        this.rangeEndText = o.rangeEndText;
        this.sameBracket = sameBracket;
    }

    /** A copy of this index with its sameBracket flag set as given. */
    public RefIndex withSameBracket(boolean sameBracket) {
        return new RefIndex(this, sameBracket);
    }

    private RefIndex(String kind, long intValue, String intText, String label, BigInteger rangeStart,
                     BigInteger rangeEnd) {
        this.kind = kind;
        this.intValue = intValue;
        this.intText = intText;
        this.label = label;
        this.rangeStart = rangeStart == null ? null : Long.valueOf(saturate(rangeStart));
        this.rangeEnd = rangeEnd == null ? null : Long.valueOf(saturate(rangeEnd));
        this.rangeStartText = rangeStart == null ? null : rangeStart.toString();
        this.rangeEndText = rangeEnd == null ? null : rangeEnd.toString();
        this.sameBracket = false;
    }

    public static RefIndex ofInt(BigInteger v) {
        return new RefIndex("int", saturate(v), v.toString(), null, null, null);
    }

    public static RefIndex ofLabel(String label) {
        return new RefIndex("label", 0, null, label, null, null);
    }

    public static RefIndex ofRange(BigInteger a, BigInteger b) {
        return new RefIndex("range", 0, null, null, a, b);
    }

    public static long saturate(BigInteger v) {
        if (v.bitLength() < 64) return v.longValue();
        return v.signum() < 0 ? Long.MIN_VALUE : Long.MAX_VALUE;
    }

    /** The index value as the reference rules print it in a message's
     * {subvalue} (the label itself, or the integer). */
    public String valueText() {
        if (kind.equals("int")) return intText;
        if (kind.equals("label")) return label;
        return rangeText();
    }

    /** "[a:b]" with an open end left empty. */
    public String rangeText() {
        return "[" + (rangeStartText == null ? "" : rangeStartText) + ":"
                + (rangeEndText == null ? "" : rangeEndText) + "]";
    }
}
''',
    'References.java': r'''package @PKG@;

import com.fasterxml.jackson.databind.JsonNode;

import java.math.BigInteger;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Reference parsing / resolution (Design.md's Cross-references section,
 * core-spec.md Section 4) and every check that hangs off a resolved
 * reference: SEDBase-0005 through -0017 (including the formulaic
 * "if a reference, must resolve to type X" field rules), SEDBase-0013's
 * Repeat scoping, AbstractTask-0003's chronological ordering, Repeat-0008
 * through -0010, LoopVariable-0004, SEDDocument-0009 through -0011 and
 * -0013. Java port of the reference-machinery half of RUNTIME in
 * generator/emit_python.py (the reference implementation - keep the two in
 * step, message text and locations included). The per-rule logic itself
 * lives in the small hand-written classes under templates/java/rules/,
 * reached through the generated Handwritten facade; this class is the
 * shared plumbing that decides which rules to call, with what. A reference
 * into `constants` resolves to a raw JSON value, never an element, and
 * nothing here ever throws for a bad document. GENERATED - do not
 * hand-edit; regenerate via generator/generate.py. */
public final class References {
    private References() {}

    static final List<String> REF_COLLECTIONS = List.of("tasks", "constants", "outputs", "styles");

    private static final Pattern DOT_ACCESSOR = Pattern.compile("^\\.([A-Za-z_][A-Za-z0-9_]*)");

    /** True when `value` is a JSON string that starts with "#", i.e. is a
     * reference. Public API. */
    public static boolean isReference(JsonNode value) {
        return value != null && value.isTextual() && value.textValue().startsWith("#");
    }

    /** True when `value` starts with "#", i.e. is a reference. Public API. */
    public static boolean isReference(String value) {
        return value != null && value.startsWith("#");
    }

    // ---- parsing -------------------------------------------------------------

    /** Python's int(str): optional surrounding whitespace and sign, decimal
     * digits (single underscores allowed between digits). null when invalid. */
    static BigInteger pyInt(String s) {
        String t = s.strip();
        if (t.isEmpty()) return null;
        int i = 0;
        boolean neg = false;
        if (t.charAt(0) == '+' || t.charAt(0) == '-') { neg = t.charAt(0) == '-'; i = 1; }
        if (i >= t.length()) return null;
        StringBuilder digits = new StringBuilder();
        boolean prevUnderscore = true;   // a leading underscore is invalid too
        for (; i < t.length(); i++) {
            char c = t.charAt(i);
            if (c == '_') {
                if (prevUnderscore) return null;
                prevUnderscore = true;
                continue;
            }
            int d = Character.digit(c, 10);
            if (d < 0) return null;
            digits.append((char) ('0' + d));
            prevUnderscore = false;
        }
        if (prevUnderscore) return null;
        BigInteger b = new BigInteger(digits.toString());
        return neg ? b.negate() : b;
    }

    static RefIndex parseRefIndex(String rawPart) {
        String part = rawPart.strip();
        if (part.indexOf(':') >= 0) {
            int c = part.indexOf(':');
            String a = part.substring(0, c), b = part.substring(c + 1);
            BigInteger av = null, bv = null;
            boolean ok = true;
            if (!a.strip().isEmpty()) {
                av = pyInt(a);
                if (av == null) ok = false;
            }
            if (ok && !b.strip().isEmpty()) {
                bv = pyInt(b);
                if (bv == null) ok = false;
            }
            // (Python raises ValueError on a non-integer range end; validate()
            // must never throw, so fall through to the bare-label reading.)
            if (ok) return RefIndex.ofRange(av, bv);
            return RefIndex.ofLabel(part);
        }
        if (part.length() >= 2 && part.charAt(0) == part.charAt(part.length() - 1)
                && (part.charAt(0) == '\'' || part.charAt(0) == '"')) {
            return RefIndex.ofLabel(part.substring(1, part.length() - 1));
        }
        BigInteger n = pyInt(part);
        if (n != null) return RefIndex.ofInt(n);
        return RefIndex.ofLabel(part);   // bare unquoted label - lenient fallback
    }

    /** Parses a reference string into its parts: '#' + a colon-delimited
     * containment path + an optional chain of dot-accessors / bracket
     * indices, e.g. "#tasks:loop1:subTasks:sim1.model['S1']" gives collection
     * "tasks", path [loop1, subTasks, sim1] and accessors [.model, ['S1']].
     * Pure syntax: never touches a document and never throws. A leading '#'
     * is stripped when present, and parsing is lenient - text after the point
     * where an accessor stops parsing (an unterminated '[', a '.' not followed
     * by a name) is ignored, so use isReference() and validate() to decide
     * whether a string is a well-formed reference at all. The accessor chain
     * is parsed and carried, never applied to a value. Public API. */
    public static ParsedReference parse(String text) {
        String body = text.startsWith("#") ? text.substring(1) : text;
        int split = -1;
        for (int i = 0; i < body.length(); i++) {
            char c = body.charAt(i);
            if (c == '.' || c == '[') { split = i; break; }
        }
        String pathPart = split >= 0 ? body.substring(0, split) : body;
        String accessorPart = split >= 0 ? body.substring(split) : "";
        List<String> segments = new ArrayList<>();
        if (!pathPart.isEmpty()) {
            for (String s : pathPart.split(":", -1)) segments.add(s);
        }
        String collection = segments.isEmpty() ? null : segments.get(0);
        List<String> path = segments.isEmpty() ? new ArrayList<>() : new ArrayList<>(segments.subList(1, segments.size()));
        List<ParsedReference.Accessor> accessors = new ArrayList<>();
        int i = 0, n = accessorPart.length();
        while (i < n) {
            char ch = accessorPart.charAt(i);
            if (ch == '.') {
                Matcher m = DOT_ACCESSOR.matcher(accessorPart.substring(i));
                if (!m.find()) break;
                accessors.add(new ParsedReference.Accessor(m.group(1), null));
                i += m.end();
            } else if (ch == '[') {
                int close = accessorPart.indexOf(']', i);
                if (close == -1) break;
                String inner = accessorPart.substring(i + 1, close);
                boolean firstInBracket = true;
                for (String part : inner.split(",", -1)) {
                    if (!part.strip().isEmpty()) {
                        RefIndex ri = parseRefIndex(part);
                        if (!firstInBracket) ri = ri.withSameBracket(true);
                        firstInBracket = false;
                        accessors.add(new ParsedReference.Accessor(null, ri));
                    }
                }
                i = close + 1;
            } else {
                break;
            }
        }
        return new ParsedReference(text, collection, path, accessors);
    }

    // ---- resolution ----------------------------------------------------------

    /** getSedReference()'s result: the target (a SedBase element, or a raw
     * JsonNode for a constants target) - null on failure - and the
     * '#...'-prefixed string of everything walked (on failure: the longest
     * prefix that resolved). prefix is null when there was no document to
     * walk, or the collection name itself is unrecognized. Public API. */
    public static final class Resolved {
        /** A SedBase (tasks/outputs/styles target), a JsonNode (constants
         * target), or null when the reference did not resolve. */
        public final Object element;
        public final String prefix;

        Resolved(Object element, String prefix) {
            this.element = element;
            this.prefix = prefix;
        }
    }

    /** Resolves a reference given as text: parse(reference), then
     * getSedReference(document, parsed). Public API. */
    public static Resolved getSedReference(SedBase document, String reference) {
        return getSedReference(document, parse(reference));
    }

    /** Resolves a reference to its target by walking its containment path
     * (everything before the first '.' or '[') against `document` one
     * colon-segment at a time (SEDBase-0006). The result's element is the
     * SedBase element for a "#tasks:", "#outputs:" or "#styles:" reference,
     * or the constant's raw JsonNode for a "#constants:" reference, and null
     * when the reference does not resolve (or the constant is JSON null);
     * its prefix is the "#..."-prefixed string of everything walked (on
     * failure, the longest prefix that resolved) - null when there was no
     * document to walk or the collection name is unrecognized. The
     * accessor chain is not applied. Public API. */
    public static Resolved getSedReference(SedBase document, ParsedReference parsed) {
        if (document == null || parsed.collection == null || !REF_COLLECTIONS.contains(parsed.collection)) {
            return new Resolved(null, null);
        }
        IdCollection coll = document.getIdCollection(parsed.collection);
        String prefix = "#" + parsed.collection;
        if (coll == null || parsed.path.isEmpty()) return new Resolved(null, prefix);
        List<String> remaining = new ArrayList<>(parsed.path);
        String firstId = remaining.remove(0);
        if (!coll.has(firstId)) return new Resolved(null, prefix);
        Object current = coll.getObject(firstId);
        prefix = prefix + ":" + firstId;
        while (!remaining.isEmpty()) {
            if (remaining.size() < 2) {
                // A lone trailing segment names a plain attribute, not an
                // ID-keyed child collection (SEDBase-0006: "a segment naming
                // a plain attribute... does not resolve").
                return new Resolved(null, prefix);
            }
            String subcollName = remaining.remove(0), itemId = remaining.remove(0);
            if (!(current instanceof SedBase)) return new Resolved(null, prefix);   // a raw value has no children
            IdCollection subcoll = ((SedBase) current).getIdCollection(subcollName);
            if (subcoll == null || !subcoll.has(itemId)) return new Resolved(null, prefix);
            current = subcoll.getObject(itemId);
            prefix = prefix + ":" + subcollName + ":" + itemId;
        }
        // A constant holding a JSON null is "no element" too: the Python
        // target's resolution returns None for it, indistinguishable from an
        // unresolved reference (so SEDBase-0006 reports it).
        if (current instanceof JsonNode && ((JsonNode) current).isNull()) current = null;
        return new Resolved(current, prefix);
    }

    // ---- values of constants and literals -----------------------------------

    /** A RefIndex as it is written in a reference: [3], ['S1'], [2:5]. */
    private static String formatIndex(RefIndex idx) {
        switch (idx.kind) {
            case "label": return "['" + idx.label + "']";
            case "range":
                return "[" + (idx.rangeStartText == null ? "" : idx.rangeStartText) + ":"
                        + (idx.rangeEndText == null ? "" : idx.rangeEndText) + "]";
            default: return "[" + idx.intText + "]";
        }
    }

    /** applyIndices(value, parse(accessors)). `accessors` is the accessor
     * text ("[2]['S1']") or a whole reference. Public API. */
    public static JsonNode applyIndices(JsonNode value, String accessors) {
        return applyIndices(value, parse(accessors));
    }

    /** Applies the bracket indices of `accessors` (its containment path is
     * ignored) to a literal JSON value; see applyIndices(JsonNode, List).
     * Throws ApiError when `accessors` contains a dot-accessor, since a
     * constant or literal has no named outputs (SEDBase-0008). Public API. */
    public static JsonNode applyIndices(JsonNode value, ParsedReference accessors) {
        List<RefIndex> indices = new ArrayList<>();
        for (ParsedReference.Accessor acc : accessors.accessors) {
            if (acc.isDot()) {
                throw new ApiError("cannot apply dot-accessor '." + acc.dotName + "' to a constant or literal value: "
                        + "only bracket indices apply to one (SEDBase-0008)");
            }
            indices.add(acc.index);
        }
        return applyIndices(value, indices);
    }

    /** Applies bracket indices to a literal JSON value - a constant's value,
     * or any other literal (a number, string, array or object) - and returns
     * the selected part. Indices follow the reference grammar (Design.md,
     * Cross-references): an int ([3], or [-1] counting from the end) indexes
     * an array; a label (['S1']) indexes an object by key; a range ([2:5],
     * either end optional) slices an array, end-exclusive, clamped to the
     * array like a Python slice, and keeps the dimension, while an int or
     * label drops it. The same rules back SEDBase-0012, so a reference that
     * validates cleanly always applies cleanly. Throws ApiError when an index
     * does not fit the value (an int or range into anything but an array, a
     * label into anything but an object that has the key, an int outside
     * -n..n-1, any index into a scalar). The result is part of `value`
     * itself, not a copy. Public API. */
    public static JsonNode applyIndices(JsonNode value, List<RefIndex> indices) {
        try {
            return (JsonNode) OutputsShape.indexIntoLiteral(value, indices);
        } catch (OutputsShape.NotIndexable e) {
            throw new ApiError("cannot apply index " + formatIndex(e.index)
                    + ": the value does not contain it (SEDBase-0012)");
        }
    }

    /** getReferenceValue(document, parse(reference)). Public API. */
    public static JsonNode getReferenceValue(SedBase document, String reference) {
        return getReferenceValue(document, parse(reference));
    }

    /** Evaluates a reference that has a value before any experiment runs: a
     * "#constants:" reference, with any bracket indices applied to the
     * constant's literal value (see applyIndices). A constant whose value is
     * itself a reference string is followed first (SEDBase-0012), through any
     * number of constants; a chain that loops throws ApiError. A constant
     * holding JSON null evaluates to a NullNode. Throws ApiError when the
     * constant does not exist (SEDBase-0006), when the reference targets
     * anything but a constant (a task, output or style has a value only when
     * the experiment runs), when it carries a dot-accessor, or when an index
     * does not fit the value. The result is part of the stored value, not a
     * copy. Public API. */
    public static JsonNode getReferenceValue(SedBase document, ParsedReference parsed) {
        return getReferenceValue(document, parsed, new java.util.HashSet<String>());
    }

    private static JsonNode getReferenceValue(SedBase document, ParsedReference parsed, Set<String> seen) {
        if (!"constants".equals(parsed.collection)) {
            throw new ApiError("reference '" + parsed.raw + "' does not name a constant, so it has no value "
                    + "before the experiment runs");
        }
        IdCollection coll = document == null ? null : document.getIdCollection("constants");
        if (coll == null || parsed.path.size() != 1 || !coll.has(parsed.path.get(0))) {
            throw new ApiError("reference '" + parsed.raw + "' does not resolve: no such constant (SEDBase-0006)");
        }
        String key = parsed.path.get(0);
        if (seen.contains(key)) {
            throw new ApiError("reference '" + parsed.raw + "' is circular: constant '" + key
                    + "' refers back to itself");
        }
        Set<String> next = new java.util.HashSet<>(seen);
        next.add(key);
        JsonNode value = (JsonNode) coll.getObject(key);
        if (isReference(value)) value = getReferenceValue(document, parse(value.textValue()), next);
        return applyIndices(value, parsed);
    }

    /** The parent of a resolved reference target, or null when the target is
     * not a document element at all - a reference into `constants` resolves
     * to a bare JSON value that has no parent and must simply count as "not
     * one of my own children", never crash validate(). */
    static SedBase elementParent(Object resolved) {
        return resolved instanceof SedBase ? ((SedBase) resolved).getParent() : null;
    }

    // ---- per-field description handed to the reference dispatcher -----------

    /** What a reference-carrying field declares about itself: its kind and,
     * when the generator derived them, the formulaic ref-type rule id, the
     * enum / numeric bounds / container item kind the target's literal value
     * must satisfy, and the x-ref-target ("model" / "annotatedData"). */
    public static final class FieldInfo {
        public final String fieldKind;
        public final String refTypeRuleId;
        public final List<String> expectedEnum;
        public final Double minimum;
        public final Double exclusiveMinimum;
        public final String itemKind;
        public final String refTarget;

        FieldInfo(String fieldKind, String refTypeRuleId, List<String> expectedEnum, Double minimum,
                  Double exclusiveMinimum, String itemKind, String refTarget) {
            this.fieldKind = fieldKind;
            this.refTypeRuleId = refTypeRuleId;
            this.expectedEnum = expectedEnum;
            this.minimum = minimum;
            this.exclusiveMinimum = exclusiveMinimum;
            this.itemKind = itemKind;
            this.refTarget = refTarget;
        }

        /** The whole-field form: everything the field's own spec declares. */
        public static FieldInfo of(FieldSpec spec) {
            return new FieldInfo(spec.kind, spec.refTypeRuleId, spec.enumValues, spec.minimum,
                    spec.exclusiveMinimum, spec.itemKind, spec.refTarget);
        }

        /** A reference with no field-level ref-type rule to check: an
         * "any"-kind field, or one entry of a DictOrRef dict literal. */
        public static FieldInfo bare(String fieldKind) {
            return new FieldInfo(fieldKind, null, null, null, null, null, null);
        }
    }

    // ---- shared dispatcher ---------------------------------------------------

    /** Shared per-type dispatcher for every reference-resolution rule
     * (SEDBase-0005 through -0015, plus the formulaic ref-type rules that
     * piggyback on -0015's scalar-reduction check). Called for every
     * SIdRef/*OrRef/any-kind field whose value is a reference. `referrer` is
     * the element carrying the reference - needed only by SEDBase-0013's
     * containment-tree scoping check and AbstractTask-0003. */
    public static List<ValidationProblem> checkReferenceField(
            String value, SedBase document, String className, String idValue, String attr, String location,
            SedBase referrer, FieldInfo info) {
        if (!Handwritten.HAS_REFERENCE_RULES) {
            // This tree's own model.rules never defined SEDBase-0005 - its own
            // reference convention (if any) isn't the tasks/constants/outputs/
            // styles vocabulary these rules check, so skip rather than
            // misapply a foreign convention.
            return new ArrayList<>();
        }
        ParsedReference parsed = parse(value);
        List<ValidationProblem> problems = new ArrayList<>(
                Handwritten.sedBase0005(parsed, className, idValue, attr, location));
        if (!problems.isEmpty()) return problems;   // unknown collection - nothing further can resolve
        problems.addAll(Handwritten.sedBase0007(parsed, className, idValue, attr, location));
        Resolved r = getSedReference(document, parsed);
        problems.addAll(Handwritten.sedBase0006(parsed, r.element, r.prefix, className, idValue, attr, location));
        if (r.element == null || "outputs".equals(parsed.collection)) {
            // Nothing further to check against - either the reference didn't
            // resolve (SEDBase-0006 already said so), or it targets an Output
            // (SEDBase-0007 already said so; outputs are never a data SOURCE).
            return problems;
        }
        if (!"constants".equals(parsed.collection)) {
            if (!(r.element instanceof SedBase)) return problems;   // a raw value below a task: no ancestry to walk
            // A constants target is a raw JSON value, so there is no
            // containment ancestry to walk and Repeat scoping doesn't apply.
            problems.addAll(checkRepeatScoping(referrer, (SedBase) r.element, parsed, className, idValue, location, value));
        }
        if ("tasks".equals(parsed.collection)) {
            problems.addAll(checkTaskOrder(referrer, (SedBase) r.element, document, className, idValue, attr, location, value));
        }
        problems.addAll(checkOutputShapeAndRefType(parsed, r.element, document, className, idValue, attr, location, value, info));
        return problems;
    }

    // ---- SEDBase-0013: Repeat subTasks/range/index/loopVariables scoping ----

    static SedBase nearestRepeatAncestor(SedBase elem) {
        SedBase cur = elem;
        while (cur != null) {
            if (cur.getIdCollection("subTasks") != null) return cur;
            cur = cur.getParent();
        }
        return null;
    }

    static boolean isAncestorOrSelf(SedBase candidate, SedBase elem) {
        SedBase cur = elem;
        while (cur != null) {
            if (cur == candidate) return true;
            cur = cur.getParent();
        }
        return false;
    }

    static List<ValidationProblem> checkRepeatScoping(SedBase referrer, SedBase resolved, ParsedReference parsed,
            String className, String idValue, String location, String value) {
        if (!Handwritten.HAS_SCOPING_RULES) return new ArrayList<>();
        String dotName = parsed.firstDotName();
        boolean isRepeatItself = resolved.getIdCollection("subTasks") != null;
        SedBase targetRepeat;
        if (isRepeatItself) {
            // A bare/.model/.aggregates/.strings reference to the Repeat ITSELF
            // is never scoped; only its per-iteration outputs are, since those
            // only have a value during one iteration: .range/.index, and a
            // ParameterScan's .ranges/.indexes and .model (the model as
            // modified for the current iteration).
            boolean loopOnly = "range".equals(dotName) || "index".equals(dotName)
                    || (("model".equals(dotName) || "ranges".equals(dotName) || "indexes".equals(dotName))
                        && "ParameterScan".equals(resolved.getClass().getSimpleName()));
            targetRepeat = loopOnly ? resolved : null;
        } else {
            SedBase parent = resolved.getParent();
            targetRepeat = parent != null ? nearestRepeatAncestor(parent) : null;
        }
        if (targetRepeat == null || referrer == null) return new ArrayList<>();
        if (isAncestorOrSelf(targetRepeat, referrer)) return new ArrayList<>();
        return Handwritten.sedBase0013(false, targetRepeat.ownIdForMessage(), value, className, idValue, location);
    }

    // ---- AbstractTask-0003: the chronological ("no forward reference") rule -

    /** One step of a chain: the id under which a node is stored in a
     * tasks/subTasks dictionary, and its position there. */
    private static final class Step {
        final String id;
        final int index;
        final SedBase owner;

        Step(String id, int index, SedBase owner) {
            this.id = id;
            this.index = index;
            this.owner = owner;
        }
    }

    /** (owner, id, index) if node's own parent stores node directly under a
     * 'tasks' or 'subTasks' id-keyed collection - the two collection kinds
     * the chronological rule cares about - else null. A node stored under
     * any OTHER id-keyed field (loopVariables, aggregateOutputVariables,
     * constants, outputs, styles, ...) doesn't match, which is what lets
     * taskChain collapse a reference living in one of those fields down to
     * its owning task's own chronological position. */
    private static Step dictMembership(SedBase node) {
        SedBase parent = node.getParent();
        if (parent == null) return null;
        for (String collName : new String[]{"tasks", "subTasks"}) {
            IdCollection coll = parent.getIdCollection(collName);
            if (coll == null) continue;
            List<String> ids = coll.ids();
            for (int idx = 0; idx < ids.size(); idx++) {
                if (coll.getObject(ids.get(idx)) == node) return new Step(ids.get(idx), idx, parent);
            }
        }
        return null;
    }

    /** The chain of dict-membership steps from SEDDocument.tasks down to
     * whichever tasks/subTasks entry directly contains `elem` (elem itself,
     * if it IS such an entry) - outermost first. null if elem isn't
     * reachable inside doc.tasks at all (an Output/Style element, or the
     * document itself). */
    private static List<Step> taskChain(SedBase elem, SedBase doc) {
        SedBase node = elem;
        List<Step> chain = new ArrayList<>();
        while (node != null && node != doc) {
            Step m = dictMembership(node);
            if (m != null) {
                chain.add(m);
                node = m.owner;
                continue;
            }
            node = node.getParent();
        }
        if (chain.isEmpty()) return null;
        java.util.Collections.reverse(chain);
        return chain;
    }

    /** AbstractTask-0003.md's own chronological comparison, walked level by
     * level (both chains outermost-first): the first level where the two
     * chains name a DIFFERENT task-dict entry is decisive - the target must
     * be strictly earlier there. If every level of the SHORTER chain
     * matches, the two share a task-lineage prefix: a target chain no
     * longer than the referrer's names the referrer's own task or an
     * enclosing Repeat (fine unless the chains are the exact same length -
     * "a task never references itself"); a longer target chain is a
     * descendant subTask of the referrer's own task (always fine). */
    private static boolean taskOrderOk(List<Step> rchain, List<Step> tchain) {
        int n = Math.min(rchain.size(), tchain.size());
        for (int i = 0; i < n; i++) {
            Step r = rchain.get(i), t = tchain.get(i);
            if (!r.id.equals(t.id)) return t.index < r.index;
        }
        if (tchain.size() <= rchain.size()) return tchain.size() < rchain.size();
        return true;
    }

    static List<ValidationProblem> checkTaskOrder(SedBase referrer, SedBase resolved, SedBase document,
            String className, String idValue, String attr, String location, String value) {
        if (!Handwritten.HAS_TASK_ORDER_RULE) return new ArrayList<>();
        if (referrer == null || document == null) return new ArrayList<>();
        List<Step> rchain = taskChain(referrer, document);
        if (rchain == null) {
            // The referring element isn't inside SEDDocument.tasks at all
            // (e.g. a Curve under outputs/): outputs always come
            // chronologically after every task, so no constraint applies.
            return new ArrayList<>();
        }
        List<Step> tchain = taskChain(resolved, document);
        if (tchain == null) return new ArrayList<>();
        boolean ok = taskOrderOk(rchain, tchain);
        return Handwritten.abstractTask0003(ok, value, className, idValue, attr, location);
    }

    // ---- Repeat-0008/-0009/-0010: a Repeat-family instance's own children ---

    /** outputVariableMap / aggregateOutputVariables of a Repeat-family
     * instance must stay scoped to that same instance's own subTasks, and an
     * aggregateOutputVariables entry may never define appliedDimensions.
     * Detected by class SHAPE (has a subTasks collection), not by name. */
    static List<ValidationProblem> checkRepeatOwnChildren(SedBase self) {
        if (!Handwritten.HAS_REPEAT_OWN_RULES) return new ArrayList<>();
        if (self.getIdCollection("subTasks") == null) return new ArrayList<>();
        SedBase document = self.getDocument();
        String className = self.getClass().getSimpleName();
        List<ValidationProblem> problems = new ArrayList<>();
        JsonNode ovm = self.values.get("outputVariableMap");
        if (ovm != null && ovm.isObject()) {
            java.util.Iterator<Map.Entry<String, JsonNode>> it = ovm.fields();
            while (it.hasNext()) {
                Map.Entry<String, JsonNode> e = it.next();
                JsonNode entryValue = e.getValue();
                if (!isReference(entryValue)) continue;
                if (!resolvesToOwnChild(document, entryValue.textValue(), self)) {
                    problems.addAll(Handwritten.repeat0008(false, entryValue, className, self.ownIdForMessage(),
                            e.getKey(), "/outputVariableMap/" + e.getKey()));
                }
            }
        }
        IdCollection agg = self.getIdCollection("aggregateOutputVariables");
        if (agg != null) {
            for (String entryId : agg.ids()) {
                Object entry = agg.getObject(entryId);
                if (!(entry instanceof SedBase)) continue;
                JsonNode entryJson = ((SedBase) entry).ownJsonValue();
                if (entryJson.has("appliedDimensions")) {
                    problems.addAll(Handwritten.repeat0010(true, entryJson.get("appliedDimensions"), className,
                            self.ownIdForMessage(), "appliedDimensions",
                            "/aggregateOutputVariables/" + entryId + "/appliedDimensions"));
                }
                JsonNode inputValue = entryJson.get("input");
                if (inputValue != null && !inputValue.isNull() && isReference(inputValue)
                        && !resolvesToOwnChild(document, inputValue.textValue(), self)) {
                    problems.addAll(Handwritten.repeat0009(false, inputValue, className, self.ownIdForMessage(),
                            "input", "/aggregateOutputVariables/" + entryId + "/input"));
                }
            }
        }
        return problems;
    }

    private static boolean resolvesToOwnChild(SedBase document, String refValue, SedBase self) {
        if (document == null) return false;
        Resolved r = getSedReference(document, parse(refValue));
        return r.element != null && elementParent(r.element) == self;
    }

    // ---- ParameterScan-0007: the modelElement values of a ParameterScan's ---
    // parameterRanges are pairwise distinct. Detected by class SHAPE (has a
    // parameterRanges list), not by name.

    static List<ValidationProblem> checkParameterScanRanges(SedBase self) {
        if (!Handwritten.HAS_PARAMETER_SCAN_RULE) return new ArrayList<>();
        ListCollection<SedBase> ranges;
        try {
            ranges = self.getListCollection("parameterRanges");
        } catch (ApiError e) {
            return new ArrayList<>();
        }
        SedBase document = self.getDocument();
        List<String> elements = new ArrayList<>();
        for (SedBase entry : ranges.items()) {
            JsonNode element = entry.ownJsonValue().get("modelElement");
            if (element != null && isReference(element)) {
                // compared by the string it resolves to; anything that does
                // not resolve to a string is some other rule's concern
                try {
                    element = getReferenceValue(document, parse(element.textValue()));
                } catch (ApiError e) {
                    element = null;
                }
            }
            elements.add(element != null && element.isTextual() ? element.textValue() : null);
        }
        return Handwritten.parameterScan0007(elements, self.getClass().getSimpleName(), self.ownIdForMessage(),
                "/parameterRanges");
    }

    // ---- LoopVariable-0004: subsequentValues stays scoped to the enclosing --
    // Loop's own subTasks - same shape as Repeat-0008/-0009 above, but for the
    // one field a LoopVariable itself carries.

    static List<ValidationProblem> checkLoopVariableScope(SedBase self) {
        if (!Handwritten.HAS_LOOPVAR_RULE) return new ArrayList<>();
        JsonNode value = self.values.get("subsequentValues");
        if (value == null || !isReference(value)) return new ArrayList<>();
        SedBase enclosing = self.getParent();
        if (enclosing == null) return new ArrayList<>();
        SedBase document = self.getDocument();
        Resolved r = document == null ? new Resolved(null, null) : getSedReference(document, parse(value.textValue()));
        boolean ok = r.element != null && elementParent(r.element) == enclosing;
        if (ok) return new ArrayList<>();
        return Handwritten.loopVariable0004(false, value, self.ownIdForMessage(), "/subsequentValues");
    }

    // ---- formulaic ref-type rules + SEDBase-0008..0012/0014/0015 ------------

    private static final Map<String, String> SCALAR_ORREF_EXPECTED = Map.of(
            "NumberOrRef", "number", "StringOrRef", "string", "IntegerOrRef", "integer", "BooleanOrRef", "boolean");

    // Every kind the formulaic ref-type rules check: the four scalar kinds
    // plus the two container kinds. A reference to a model is never
    // acceptable for any of them: a model is a type of its own
    // (ProposedRules.md).
    private static final Set<String> REF_TYPE_KINDS = Set.of(
            "NumberOrRef", "StringOrRef", "IntegerOrRef", "BooleanOrRef", "ArrayOrRef", "DictOrRef");

    static String fmtLiteral(Object value) {
        if (value == null) return "null";
        if (value instanceof JsonNode) return PyFmt.jsonDumps((JsonNode) value);
        return "<" + value.getClass().getSimpleName() + " object>";
    }

    private static boolean isNumberNode(Object o) {
        return o instanceof JsonNode && ((JsonNode) o).isNumber();
    }

    /** Only called once a constant's own literal value has already been fully
     * indexed down - a REAL value - so enum membership, numeric bounds and
     * array/dict element kinds can be checked exactly. A bare JSON boolean
     * never counts as a number. Inside an array/dict a reference-valued
     * element is accepted (it may resolve to the right kind). Returns null
     * for a kind this doesn't check. */
    static Boolean literalMatchesKind(Object value, FieldInfo info) {
        JsonNode n = value instanceof JsonNode ? (JsonNode) value : null;
        switch (info.fieldKind) {
            case "NumberOrRef":
            case "IntegerOrRef": {
                boolean ok;
                if (n == null || !n.isNumber()) ok = false;
                else if (info.fieldKind.equals("NumberOrRef")) ok = true;
                else ok = n.isIntegralNumber() || (n.isFloatingPointNumber() && !Double.isInfinite(n.doubleValue())
                        && !Double.isNaN(n.doubleValue()) && n.doubleValue() == Math.floor(n.doubleValue()));
                if (!ok) return false;
                double d = n.doubleValue();
                if (info.minimum != null && d < info.minimum) return false;
                if (info.exclusiveMinimum != null && d <= info.exclusiveMinimum) return false;
                return true;
            }
            case "BooleanOrRef":
                return n != null && n.isBoolean();
            case "StringOrRef":
                if (n == null || !n.isTextual()) return false;
                if (info.expectedEnum != null) return info.expectedEnum.contains(n.textValue());
                return true;
            case "ArrayOrRef":
                if (n == null || !n.isArray()) return false;
                for (JsonNode v : n) if (!elementMatches(v, info.itemKind)) return false;
                return true;
            case "DictOrRef":
                if (n == null || !n.isObject()) return false;
                for (JsonNode v : n) if (!elementMatches(v, info.itemKind)) return false;
                return true;
            default:
                return null;
        }
    }

    /** One array element / dict value against the schema's declared kind
     * ("string" | "number" | "ref" | "any"). A reference-valued element
     * always passes for string/number (it stands in for a value of that
     * kind). */
    private static boolean elementMatches(JsonNode element, String itemKind) {
        if ("string".equals(itemKind)) return element.isTextual();
        if ("number".equals(itemKind)) return element.isNumber() || isReference(element);
        if ("ref".equals(itemKind)) return isReference(element);
        return true;
    }

    /** A task-output target has no actual VALUE to type-check - only
     * outputs.json's own declared "type" for the suffix entry. Coarse by
     * necessity: an annotatedData cell is always treated as number-shaped, a
     * stringList entry as string-shaped. null when the declared type maps to
     * neither. */
    private static Boolean refTypeMatchesDeclared(String expected, String actualDeclared) {
        String mapped = "annotatedData".equals(actualDeclared) ? "number"
                : "stringList".equals(actualDeclared) ? "string" : null;
        if (mapped == null) return null;
        return mapped.equals(expected);
    }

    /** (kind, description) of a constant's (fully indexed) literal value for
     * SEDBase-0016/-0017: a number/string/boolean/array is AnnotatedData, an
     * object is neither a model nor AnnotatedData; a JSON null is not
     * decidable. */
    private static String[] constantTargetKind(Object finalValue) {
        if (finalValue instanceof JsonNode) {
            JsonNode n = (JsonNode) finalValue;
            if (n.isBoolean()) return new String[]{"annotatedData", "a boolean"};
            if (n.isNumber()) return new String[]{"annotatedData", "a number"};
            if (n.isTextual()) return new String[]{"annotatedData", "a string"};
            if (n.isArray()) return new String[]{"annotatedData", "an array"};
            if (n.isObject()) return new String[]{"object", "an object"};
        }
        return new String[]{null, ""};
    }

    /** (kind, description) of a task-output suffix entry, from its
     * outputs.json "type", for SEDBase-0016/-0017. */
    private static String[] outputTargetKind(JsonNode entry) {
        String declared = entry != null && entry.has("type") && entry.get("type").isTextual()
                ? entry.get("type").textValue() : null;
        if ("model".equals(declared)) return new String[]{"model", "a model"};
        if ("annotatedData".equals(declared)) return new String[]{"annotatedData", "an annotatedData value"};
        if ("stringList".equals(declared)) return new String[]{"annotatedData", "a stringList value"};
        return new String[]{null, ""};
    }

    /** SEDBase-0016 ("model") / SEDBase-0017 ("annotatedData") dispatch. */
    private static List<ValidationProblem> checkRefTarget(String refTarget, String kind, String description,
            String value, String className, String idValue, String attr, String location) {
        if (!Handwritten.HAS_REF_TARGET_RULES) return new ArrayList<>();
        if ("model".equals(refTarget)) {
            return Handwritten.sedBase0016(kind, description, value, className, idValue, attr, location);
        }
        if ("annotatedData".equals(refTarget)) {
            return Handwritten.sedBase0017(kind, description, value, className, idValue, attr, location);
        }
        return new ArrayList<>();
    }

    private static ValidationProblem refTypeProblem(String ruleId, String location, String attr, String value,
            String className, String idValue, String resolvedDesc) {
        return RuleCatalog.problem(ruleId, location, "attr", attr, "value", value,
                "class", className, "id", idValue, "resolved-value", resolvedDesc);
    }

    /** followConstantAlias()'s result: the followed value, or why it could
     * not be followed ("unresolved": the chain leads nowhere that can be
     * evaluated here - a missing constant, a cycle, a dot-accessor; some
     * other rule reports those - or "index": an index in the chain does not
     * fit the value it is applied to, with bad the index as SEDBase-0012's
     * {subvalue} prints it and literal the value indexed). */
    private static final class Followed {
        final Object value;
        final String failure;   // null, "unresolved" or "index"
        final String bad;
        final String literal;

        Followed(Object value, String failure, String bad, String literal) {
            this.value = value;
            this.failure = failure;
            this.bad = bad;
            this.literal = literal;
        }
    }

    /** A constant's value once it has been followed through every reference
     * it is made of (SEDBase-0012.md: "A constant whose value is itself a
     * reference is followed first"): for a value that is a reference string
     * to another constant, that constant's value, itself followed, with the
     * reference's own bracket indices applied - so an alias such as
     * "#constants:table['S2']" is its row, not the whole table, and an alias
     * of an alias is followed to the end. A reference to a task, output or
     * style is returned as the element (its indices are not applied). */
    private static Followed followConstantAlias(SedBase document, Object value, Set<String> seen) {
        if (!(value instanceof JsonNode && isReference((JsonNode) value))) return new Followed(value, null, null, null);
        ParsedReference inner = parse(((JsonNode) value).textValue());
        if (!"constants".equals(inner.collection)) {
            return new Followed(getSedReference(document, inner).element, null, null, null);
        }
        IdCollection coll = document == null ? null : document.getIdCollection("constants");
        if (coll == null || inner.path.size() != 1 || !coll.has(inner.path.get(0)) || seen.contains(inner.path.get(0))
                || inner.firstDotName() != null) {
            return new Followed(null, "unresolved", null, null);
        }
        Set<String> next = new java.util.HashSet<>(seen);
        next.add(inner.path.get(0));
        Followed base = followConstantAlias(document, coll.getObject(inner.path.get(0)), next);
        if (base.failure != null) return base;
        try {
            return new Followed(OutputsShape.indexIntoLiteral(base.value, inner.indexAccessors()), null, null, null);
        } catch (OutputsShape.NotIndexable e) {
            return new Followed(null, "index", e.bad, fmtLiteral(base.value));
        }
    }

    private static List<ValidationProblem> checkConstantAccessor(ParsedReference parsed, Object resolved,
            SedBase document, String className, String idValue, String attr, String location, String value,
            FieldInfo info) {
        String dotName = parsed.firstDotName();
        if (dotName != null) {
            // SEDBase-0008.md: "For a constants ... target, no dot-accessor is valid."
            return new ArrayList<>(Handwritten.sedBase0008(false, dotName, value, className, idValue, attr, location));
        }
        List<RefIndex> indexAccessors = parsed.indexAccessors();
        // SEDBase-0012.md: "A constant whose value is itself a reference is
        // followed first" - through a chain of constants and with each alias's
        // own indices applied (followConstantAlias).
        Followed followed = followConstantAlias(document, resolved, new java.util.HashSet<String>());
        if (followed.failure != null) {
            if ("index".equals(followed.failure)) {
                return new ArrayList<>(Handwritten.sedBase0012(false, followed.bad, followed.literal, value,
                        className, idValue, attr, location));
            }
            return new ArrayList<>();
        }
        Object constValue = followed.value;
        Object finalValue;
        try {
            finalValue = OutputsShape.indexIntoLiteral(constValue, indexAccessors);
        } catch (OutputsShape.NotIndexable e) {
            return new ArrayList<>(Handwritten.sedBase0012(false, e.bad, fmtLiteral(constValue), value, className,
                    idValue, attr, location));
        }
        if (info.refTarget != null) {
            String[] k = constantTargetKind(finalValue);
            return checkRefTarget(info.refTarget, k[0], k[1], value, className, idValue, attr, location);
        }
        if (info.refTypeRuleId == null || !REF_TYPE_KINDS.contains(info.fieldKind)) return new ArrayList<>();
        if (Boolean.FALSE.equals(literalMatchesKind(finalValue, info))) {
            List<ValidationProblem> out = new ArrayList<>();
            out.add(refTypeProblem(info.refTypeRuleId, location, attr, value, className, idValue, fmtLiteral(finalValue)));
            return out;
        }
        return new ArrayList<>();
    }

    /** shapeOf(ref) support for outputs.json expressions: resolves another
     * reference's post-index dimensions, statically, or gives up with
     * NotStatic. The depth guard is shared across one check. */
    private static final class ShapeResolver implements java.util.function.Function<String, List<Dim>> {
        private final SedBase document;
        private int depth = 0;

        ShapeResolver(SedBase document) { this.document = document; }

        @Override
        public List<Dim> apply(String refString) {
            depth++;
            if (depth > 25) throw new OutputsShape.NotStatic("shapeOf() recursion too deep");
            ParsedReference parsed2 = parse(refString);
            Object inner = getSedReference(document, parsed2).element;
            JsonNode innerOutputs = inner instanceof SedBase ? ((SedBase) inner).outputsJson() : null;
            if (innerOutputs == null) throw new OutputsShape.NotStatic("shapeOf() target has no outputs.json");
            OutputsShape.Resolution r = OutputsShape.resolveOutput(
                    innerOutputs, ((SedBase) inner).ownJsonValue(), parsed2.accessors, this);
            if (!Boolean.TRUE.equals(r.ok) || r.dimsAfter == null) {
                throw new OutputsShape.NotStatic("shapeOf() target shape not statically known");
            }
            return r.dimsAfter;
        }
    }

    private static List<ValidationProblem> checkOutputShapeAndRefType(ParsedReference parsed, Object resolved,
            SedBase document, String className, String idValue, String attr, String location, String value,
            FieldInfo info) {
        if (!Handwritten.HAS_SHAPE_RULES) {
            // This tree's own model.rules never defined SEDBase-0008 (a
            // different spec tree with no outputs.json-shaped tasks/
            // vocabulary at all).
            return new ArrayList<>();
        }
        if ("constants".equals(parsed.collection)) {
            return checkConstantAccessor(parsed, resolved, document, className, idValue, attr, location, value, info);
        }
        JsonNode outputsJson = resolved instanceof SedBase ? ((SedBase) resolved).outputsJson() : null;
        if (outputsJson == null) {
            // styles / a nested non-tasks/-class element reached via a tasks:
            // path (LoopVariable, TaskParameter, ...): a bare reference is
            // always fine, only a dot-accessor on top is invalid, and there's
            // no outputs.json-driven shape to check brackets against.
            String dotName = parsed.firstDotName();
            if (dotName == null) return new ArrayList<>();
            return new ArrayList<>(Handwritten.sedBase0008(false, dotName, value, className, idValue, attr, location));
        }
        SedBase target = (SedBase) resolved;
        OutputsShape.Resolution r = OutputsShape.resolveOutput(
                outputsJson, target.ownJsonValue(), parsed.accessors, new ShapeResolver(document));
        List<ValidationProblem> problems = new ArrayList<>(
                Handwritten.sedBase0008(r.ok, r.dotName, value, className, idValue, attr, location));
        if (!Boolean.TRUE.equals(r.ok)) return problems;
        // Each rule judges an index against the dimension that index is applied
        // to (chained brackets: the dimension as the earlier ranges left it).
        List<Dim> seenDims = OutputsShape.bindIndices(r.dimsBefore, r.indexAccessors).seen;
        problems.addAll(Handwritten.sedBase0009(seenDims, r.indexAccessors, value, className, idValue, attr, location));
        problems.addAll(Handwritten.sedBase0010(seenDims, r.indexAccessors, value, className, idValue, attr, location));
        problems.addAll(Handwritten.sedBase0011(seenDims, r.indexAccessors, value, className, idValue, attr, location));
        problems.addAll(Handwritten.sedBase0014(seenDims, r.indexAccessors, value, className, idValue, attr, location));

        if (info.refTarget != null) {
            String[] k = outputTargetKind(r.entry);
            problems.addAll(checkRefTarget(info.refTarget, k[0], k[1], value, className, idValue, attr, location));
        }
        if (info.refTypeRuleId != null && REF_TYPE_KINDS.contains(info.fieldKind)) {
            String actualDeclared = r.entry != null && r.entry.has("type") && r.entry.get("type").isTextual()
                    ? r.entry.get("type").textValue() : null;
            if ("model".equals(actualDeclared)) {
                // A model is a type of its own: never a number, string,
                // boolean, array, or dictionary (ProposedRules.md).
                problems.add(refTypeProblem(info.refTypeRuleId, location, attr, value, className, idValue, "a model"));
            } else if (SCALAR_ORREF_EXPECTED.containsKey(info.fieldKind)) {
                String expected = SCALAR_ORREF_EXPECTED.get(info.fieldKind);
                problems.addAll(Handwritten.sedBase0015(r.dimsAfter, expected, value, className, idValue, attr, location));
                if (r.dimsAfter != null && r.dimsAfter.isEmpty()) {
                    if (Boolean.FALSE.equals(refTypeMatchesDeclared(expected, actualDeclared))) {
                        problems.add(refTypeProblem(info.refTypeRuleId, location, attr, value, className, idValue,
                                "a " + actualDeclared + " value"));
                    }
                }
            } else if (info.fieldKind.equals("ArrayOrRef")) {
                // Only the unambiguous mismatch: an array of numbers fed a
                // stringList output.
                if ("number".equals(info.itemKind) && "stringList".equals(actualDeclared)) {
                    problems.add(refTypeProblem(info.refTypeRuleId, location, attr, value, className, idValue,
                            "a stringList value"));
                }
            }
        }
        return problems;
    }

    // ---- SEDDocument-0009 .. -0011: namespaces + version --------------------

    private static void walk(SedBase obj, String prefix, List<SedBase> objs, List<String> locs) {
        objs.add(obj);
        locs.add(prefix);
        for (SedBase.ChildLoc cl : obj.childrenWithLocations()) walk(cl.child, prefix + cl.locationPrefix, objs, locs);
    }

    /** SEDDocument-0009 through -0011 - whole-document checks, called once
     * from the document root's validate(). A prefix is "used" when any
     * attribute key or _type value of the form prefix@identifier appears
     * anywhere in the document (registered and unregistered prefixes alike);
     * the <prefix>@version declaration itself (only ever on the root) doesn't
     * count as a use of that prefix. */
    static List<ValidationProblem> checkNamespaceUsageAndVersion(SedBase document) {
        if (!Handwritten.HAS_NAMESPACE_RULES) return new ArrayList<>();
        Map<String, String> declared = new LinkedHashMap<>();   // prefix -> "/<prefix>@version"
        for (String k : document.nsAttrs.keySet()) {
            int at = k.indexOf('@');
            if (k.substring(at + 1).equals("version")) declared.put(k.substring(0, at), "/" + k);
        }
        Map<String, List<String>> used = new LinkedHashMap<>();  // prefix -> [locations]
        List<SedBase> objs = new ArrayList<>();
        List<String> locs = new ArrayList<>();
        walk(document, "", objs, locs);
        for (int i = 0; i < objs.size(); i++) {
            SedBase obj = objs.get(i);
            String loc = locs.get(i);
            for (String k : obj.nsAttrs.keySet()) {
                int at = k.indexOf('@');
                String pfx = k.substring(0, at), key = k.substring(at + 1);
                if (obj == document && key.equals("version")) continue;
                used.computeIfAbsent(pfx, x -> new ArrayList<>()).add(loc + "/" + pfx + "@" + key);
            }
            String typeValue = obj.typeValue();
            if (typeValue != null && typeValue.contains("@")) {
                used.computeIfAbsent(typeValue.split("@", 2)[0], x -> new ArrayList<>()).add(loc + "/_type");
            }
        }
        List<ValidationProblem> problems = new ArrayList<>();
        for (Map.Entry<String, List<String>> e : used.entrySet()) {
            if (declared.containsKey(e.getKey())) continue;
            for (String loc : e.getValue()) problems.addAll(Handwritten.sedDocument0009(e.getKey(), loc));
        }
        for (Map.Entry<String, String> e : declared.entrySet()) {
            if (!used.containsKey(e.getKey())) problems.addAll(Handwritten.sedDocument0010(e.getKey(), e.getValue()));
        }
        problems.addAll(Handwritten.sedDocument0011(document));
        return problems;
    }

    /** SEDDocument-0013: a constant whose value is a reference may only
     * reference a constant declared EARLIER in the constants dictionary. */
    static List<ValidationProblem> checkConstantsOrdering(SedBase document) {
        if (!Handwritten.HAS_CONSTANTS_ORDER_RULE) return new ArrayList<>();
        return Handwritten.sedDocument0013(document.getIdCollection("constants"));
    }
}
''',
}
# ---- END embedded reference-machinery runtime (Java sources) ----


def runtime_files() -> dict:
    files = {
        "ValidationProblem.java": _validation_problem_java(),
        "ApiError.java": _api_error_java(),
        "FieldSpec.java": _field_spec_java(),
        "RuleCatalog.java": _rule_catalog_java(),
        "LeafValidation.java": _leaf_validation_java(),
        "IdKeyedCollection.java": _id_keyed_collection_java(),
        "ListCollection.java": _list_collection_java(),
        "SedBase.java": _sed_base_java(),
        "MathAst.java": _math_ast_java(),
        "MathRules.java": _math_rules_java(),
    }
    for fname, src in _STATIC_RUNTIME_JAVA.items():
        files[fname] = src.replace("@PKG@", PKG)
    return files


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


def _java_int_lit(v) -> str:
    return "null" if v is None else str(int(v))


def _java_str_list_lit(vs) -> str:
    if vs is None:
        return "null"
    return "List.of(" + ", ".join(_java_lit(v) for v in vs) + ")"


def _field_spec_expr(f: Field) -> str:
    t = f.type
    return (
        f"new FieldSpec({_java_lit(f.name)}, {_java_lit(t.kind)}, {str(f.required).lower()}, "
        f"{_java_lit(f.rule_id)}, {_java_lit(f.required_rule_id)}, {_java_lit(f.origin_class + '-0000')}, "
        f"{_java_double_lit(t.minimum)}, {_java_double_lit(t.exclusive_minimum)}, {_java_lit(t.pattern)}, "
        f"{_java_lit(t.item_class)}, {_java_lit(t.item_discriminator)}, {str(f.is_math).lower()}, "
        f"{_java_int_lit(t.min_length)}, {_java_str_list_lit(t.enum)}, {_java_lit(f.ref_type_rule_id)}, "
        f"{_java_lit(t.item_kind)}, {_java_lit(f.ref_target)})"
    )


# The full OrRef family (Design.md's Validation section / core/Types) -
# StringOrRef/NumberOrRef were the only two the Phase-1 test-specsheets/
# vocabulary exercised; the real spec (specsheets/) also uses the other
# four. Every one of these gets the same six get-/set-/is-Ref-/isSet-/
# unset- accessors, generic OrRef storage (getOrRefValueNode/
# setOrRefValueNode/... in SedBase.java), differing only in the natural
# Java type on the value side - ArrayOrRef/DictOrRef have no better native
# Java collection representation than the raw JsonNode itself without a lot
# more work than it is worth here,
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
        out.append(f"/** Generated from {model.spec_root_label()}/{c.category}/{name}/. GENERATED - do not\n"
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
        if c.is_document:
            # The document root is its own document (getDocument() must never
            # be null for anything reachable from it) - Io.readFromString sets
            # this up for a deserialized document via its own attach(null, obj)
            # call, but a document built up programmatically (new SEDDocument()
            # then addTasks(...), never round-tripped through readFromString)
            # needs the same self-attach here, or every backpointer-dependent
            # thing downstream (getDocument(), and in particular the
            # SEDBase-0005/0006/0007 reference-resolution rules, which
            # silently no-op with no document to walk) breaks silently for
            # documents built that way. Mirrors emit_python.py's __init__.
            out.append(f"    public {name}() {{ attach(null, this); }}\n")
            out.append("    @Override public boolean isDocumentClass() { return true; }\n")
            out.append(f"    @Override public String maxKnownDocumentVersion() {{ return {_java_lit(model.document_version)}; }}\n")
        if c.outputs_json is not None:
            # core-spec.md Section 8 - the class's own outputs.json, embedded
            # as its JSON text and parsed once at class-init time, so the
            # OutputsShape interpreter can read it straight off the instance
            # at validate() time (SEDBase-0008 through -0015). Only concrete
            # tasks/ classes ever have one; every other class leaves
            # SedBase.outputsJson()'s own null default.
            out.append(f"    private static final JsonNode OUTPUTS_JSON = OutputsShape.parseJson({_java_lit(_json.dumps(c.outputs_json))});\n")
            out.append("    @Override public JsonNode outputsJson() { return OUTPUTS_JSON; }\n")
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

        # Generic containment-tree lookup by field name (SEDBase-0006 /
        # References.getSedReference - Design.md's Cross-references section):
        # every ID-keyed collection this class owns, by its own field name, so
        # a reference's colon-segments can walk into any class's own dict-kind
        # field generically, not just SEDDocument's top-level tasks/constants/
        # outputs/styles. "any-dict" fields (constants) are included too -
        # their own values are plain JSON, not further walkable, but
        # getSedReference() itself stops there. Mirrors emit_python.py's
        # _get_id_collection / _id_collection_names.
        id_coll_fields = [f for f in collection_fields if f.type.kind in ("dict", "any-dict")]
        if id_coll_fields:
            out.append("    @Override\n    public IdCollection getIdCollection(String fieldName) {\n        switch (fieldName) {\n")
            for f in id_coll_fields:
                ident = _java_ident(f.name)
                out.append(f"            case {_java_lit(f.name)}: return {ident};\n")
            out.append("            default: return null;\n        }\n    }\n\n")
            names = ", ".join(_java_lit(f.name) for f in id_coll_fields)
            out.append(f"    @Override\n    public List<String> idCollectionNames() {{ return List.of({names}); }}\n\n")

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
    public String typeValue() {{ return typeValue; }}

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
            out.append(f"            Map<String, Object> ph0 = new LinkedHashMap<>();\n")
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
        out.append("        Map<String, Object> ph = new LinkedHashMap<>();\n")
        out.append("        ph.put(\"schema-message\", \"unrecognized _type \" + PyFmt.repr(raw.get(\"_type\")));\n")
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


# Handwritten rule IDs whose per-rule Java logic lives under
# templates/java/rules/<ClassName>.java (see _copy_handwritten_rules_java) -
# the Java analog of emit_python.py's _IMPLEMENTED_HANDWRITTEN_RULE_IDS. The
# four math-grammar rules (Types-0001..0004) are the one exception: they were
# implemented before this mechanism existed and stay together in the emitted
# MathRules.java, so they are not listed here. SEDDocument-0012 (duplicate
# JSON keys) is deliberately NOT implemented - see its own rule file's
# "Decided not to implement detection for this rule in v1" paragraph.
_IMPLEMENTED_HANDWRITTEN_RULE_IDS = (
    "SEDBase-0005", "SEDBase-0006", "SEDBase-0007",
    "SEDBase-0008", "SEDBase-0009", "SEDBase-0010", "SEDBase-0011", "SEDBase-0012",
    "SEDBase-0013", "SEDBase-0014", "SEDBase-0015", "SEDBase-0016", "SEDBase-0017",
    "SEDDocument-0009", "SEDDocument-0010", "SEDDocument-0011", "SEDDocument-0013",
    "AbstractTask-0003", "Repeat-0008", "Repeat-0009", "Repeat-0010", "LoopVariable-0004",
    "ParameterScan-0007",
)

# Which rule IDs a dispatcher in References.java needs all of before it runs
# at all - the Java analog of the `try: from ._rules import ...; except
# ImportError: return []` guards in emit_python.py's RUNTIME. A spec tree
# whose own rule set lacks one (e.g. test-specsheets/) gets `false` here and
# the dispatcher no-ops.
_RULE_GROUPS = (
    ("HAS_REFERENCE_RULES", ("SEDBase-0005", "SEDBase-0006", "SEDBase-0007")),
    ("HAS_SHAPE_RULES", ("SEDBase-0008", "SEDBase-0009", "SEDBase-0010", "SEDBase-0011",
                         "SEDBase-0012", "SEDBase-0014", "SEDBase-0015")),
    ("HAS_REF_TARGET_RULES", ("SEDBase-0016", "SEDBase-0017")),
    ("HAS_SCOPING_RULES", ("SEDBase-0013",)),
    ("HAS_TASK_ORDER_RULE", ("AbstractTask-0003",)),
    ("HAS_REPEAT_OWN_RULES", ("Repeat-0008", "Repeat-0009", "Repeat-0010")),
    ("HAS_LOOPVAR_RULE", ("LoopVariable-0004",)),
    ("HAS_PARAMETER_SCAN_RULE", ("ParameterScan-0007",)),
    ("HAS_NAMESPACE_RULES", ("SEDDocument-0009", "SEDDocument-0010", "SEDDocument-0011")),
    ("HAS_CONSTANTS_ORDER_RULE", ("SEDDocument-0013",)),
)


def _rule_class_name(rule_id: str) -> str:
    """'SEDBase-0005' -> 'SedBase0005', 'AbstractTask-0003' ->
    'AbstractTask0003': the rule template's class name (and file stem)."""
    prefix, num = rule_id.rsplit("-", 1)
    if prefix.startswith("SED"):
        prefix = "Sed" + prefix[3:]
    return prefix + num


def _rule_method_name(rule_id: str) -> str:
    cn = _rule_class_name(rule_id)
    return cn[0].lower() + cn[1:]


def _parse_check_signature(java_src: str, where: str) -> list:
    """[(java type, param name), ...] of the one `public static
    List<ValidationProblem> check(...)` a rule template must define."""
    import re
    m = re.search(r"public\s+static\s+List<ValidationProblem>\s+check\s*\((.*?)\)\s*\{", java_src, re.S)
    if not m:
        raise RuntimeError(f"{where}: no `public static List<ValidationProblem> check(...)` found")
    text, depth, parts, cur = m.group(1), 0, [], ""
    for ch in text:
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur)
    out = []
    for part in parts:
        toks = part.split()
        out.append((" ".join(toks[:-1]), toks[-1]))
    return out


def _copy_handwritten_rules_java(pkg_dir: str, model: SpecModel) -> str:
    """Copies templates/java/rules/<ClassName>.java -> <pkg>/<ClassName>.java
    for every rule ID in _IMPLEMENTED_HANDWRITTEN_RULE_IDS that this MODEL
    actually defines (rid in model.rules), verbatim except for the leading
    `package ...;` line (Java requires it to match the destination) - the
    Java analog of emit_python.py's _copy_handwritten_rules_py - and returns
    the source of the generated Handwritten facade.

    Like the Python target, a rule id NOT defined by this model is skipped
    silently: some of these rules encode a convention specific to the real
    SED2 spec (the '#tasks:'/'#constants:'/'#outputs:'/'#styles:' vocabulary)
    and a different spec tree, such as the synthetic test-specsheets/, would
    be validated by the WRONG convention if they ran anyway. Where Python's
    dispatchers degrade to a no-op through an ImportError, Java's degrade
    through the facade: Handwritten.<method> for an absent rule is a no-op
    with the very same signature (taken from the template itself), and the
    Handwritten.HAS_* flags let a dispatcher skip its whole group. The
    missing-file RuntimeError below still fires - failing the whole generator
    run, per Design.md's Validation section - for any rule id the model DOES
    define but whose template file is genuinely absent."""
    templates_dir = os.path.join(_repo_root(), "templates", "java", "rules")
    missing = []
    present = {}
    sigs = {}
    for rid in _IMPLEMENTED_HANDWRITTEN_RULE_IDS:
        cn = _rule_class_name(rid)
        src = os.path.join(templates_dir, f"{cn}.java")
        if not os.path.isfile(src):
            if rid in model.rules:
                missing.append(src)
            continue
        with open(src) as f:
            content = f.read()
        sigs[rid] = _parse_check_signature(content, src)
        if rid not in model.rules:
            continue
        first_nl = content.index("\n")
        assert content[:first_nl].startswith("package "), f"{src} must start with a `package ...;` line"
        content = f"package {PKG};" + content[first_nl:]
        with open(os.path.join(pkg_dir, f"{cn}.java"), "w") as f:
            f.write(content)
        present[rid] = True
    if missing:
        raise RuntimeError(
            "Missing hand-written rule file(s) required by the generator "
            "(Design.md's Validation section - \"the generator fails its run if a "
            "handwritten rule is missing its file\"): " + ", ".join(missing)
        )

    lines = [f"package {PKG};", "", "import java.util.ArrayList;", "import java.util.List;", "",
             "/** Facade over the hand-written per-rule check() classes (templates/java/rules/),",
             " * one static method per implemented rule with the same signature as the rule's own",
             " * check() - or, for a rule this spec tree does not define, the same signature as a",
             " * no-op - plus the HAS_* group flags References.java's dispatchers consult (the Java",
             " * analog of emit_python.py's ImportError guards). GENERATED - do not hand-edit;",
             " * regenerate via generator/generate.py. */",
             "public final class Handwritten {", "    private Handwritten() {}", ""]
    for flag, rids in _RULE_GROUPS:
        ok = all(r in present for r in rids)
        lines.append(f"    public static final boolean {flag} = {str(ok).lower()};   // {', '.join(rids)}")
    lines.append("")
    for rid in _IMPLEMENTED_HANDWRITTEN_RULE_IDS:
        if rid not in sigs:
            continue
        params = ", ".join(f"{t} {n}" for t, n in sigs[rid])
        args = ", ".join(n for _t, n in sigs[rid])
        lines.append(f"    /** {rid}. */")
        lines.append(f"    public static List<ValidationProblem> {_rule_method_name(rid)}({params}) {{")
        if rid in present:
            lines.append(f"        return {_rule_class_name(rid)}.check({args});")
        else:
            lines.append("        return new ArrayList<>();")
        lines.append("    }")
        lines.append("")
    lines.append("}")
    return "\n".join(lines) + "\n"


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


def _copy_api_test_java(out_dir: str, java_package: str, model: SpecModel) -> None:
    """Copies templates/java/tests/ApiTest.java -> <out_dir>/src/test/java/
    <package-path>/ApiTest.java, rewriting only its leading `package ...;`
    line (as _copy_fixture_test_java does), and only for a spec tree with the
    real SED2 document classes (see SpecModel.has_api_tests): the tests use
    them directly. Its documents are read from fixtures/api/."""
    if not model.has_api_tests():
        return
    src = os.path.join(_repo_root(), "templates", "java", "tests", "ApiTest.java")
    with open(src) as f:
        content = f.read()
    first_nl = content.index("\n")
    assert content[:first_nl].startswith("package "), (
        "templates/java/tests/ApiTest.java must start with a `package ...;` line"
    )
    content = f"package {java_package};" + content[first_nl:]
    test_pkg_dir = os.path.join(out_dir, "src", "test", "java", *java_package.split("."))
    os.makedirs(test_pkg_dir, exist_ok=True)
    with open(os.path.join(test_pkg_dir, "ApiTest.java"), "w") as f:
        f.write(content)


def _pom_xml(group_id: str, artifact_id: str, description: str, antlr_runtime_version: str, version: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{group_id}</groupId>
  <artifactId>{artifact_id}</artifactId>
  <version>{version}</version>
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
    <!-- Build-time-only dependency of the *generator* is the ANTLR tool jar
         (antlr_tool.py); this is the small runtime the ANTLR-generated
         mathLexer/mathParser/mathBaseVisitor (MathAst.java) need at
         compile+run time - same pinned version, mirrors emit_python.py's
         antlr4-python3-runtime pyproject.toml dependency. -->
    <dependency>
      <groupId>org.antlr</groupId>
      <artifactId>antlr4-runtime</artifactId>
      <version>{antlr_runtime_version}</version>
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

  <!-- `mvn -Prelease package` additionally attaches the -sources and
       -javadoc jars next to the main jar, which is what a published release
       carries (CI's release-java job, see .github/workflows/ci.yml). Off by
       default so the everyday build/test cycle stays fast. Javadoc's doclint
       is off because this is generated code, not hand-written prose. -->
  <profiles>
    <profile>
      <id>release</id>
      <build>
        <plugins>
          <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-source-plugin</artifactId>
            <version>3.3.1</version>
            <executions>
              <execution>
                <id>attach-sources</id>
                <goals>
                  <goal>jar-no-fork</goal>
                </goals>
              </execution>
            </executions>
          </plugin>
          <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-javadoc-plugin</artifactId>
            <version>3.10.1</version>
            <configuration>
              <doclint>none</doclint>
              <quiet>true</quiet>
            </configuration>
            <executions>
              <execution>
                <id>attach-javadocs</id>
                <goals>
                  <goal>jar</goal>
                </goals>
              </execution>
            </executions>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>
</project>
'''


def emit_java_package(
    model: SpecModel,
    out_dir: str,
    java_package: str = "org.sed2test",
    maven_group_id: str | None = None,
    maven_artifact_id: str = "libsed2test",
    description: str | None = None,
    build_math: bool = True,
    antlr_cache_dir: str | None = None,
    version: str | None = None,
) -> None:
    global PKG
    from .version import check_version, library_version
    version = check_version(version, "version") if version is not None else library_version()
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
    with open(os.path.join(pkg_dir, "Handwritten.java"), "w") as f:
        f.write(_copy_handwritten_rules_java(pkg_dir, model))
    with open(os.path.join(pkg_dir, "Dispatch.java"), "w") as f:
        f.write(emit_dispatch_java(model))
    with open(os.path.join(pkg_dir, "RulesData.java"), "w") as f:
        f.write(emit_rules_data_java(model))
    with open(os.path.join(pkg_dir, "Io.java"), "w") as f:
        f.write(emit_io_java(model))
    with open(os.path.join(pkg_dir, "PredefinedFunctions.java"), "w") as f:
        f.write(emit_predefined_functions_java())

    from .antlr_tool import generate_java_math_parser, ANTLR_VERSION
    if build_math:
        # ANTLR tool is a build-time-only dependency of the generator itself
        # (Design.md's Parser Strategy) - runs here, writes the generated
        # mathLexer.java/mathParser.java/mathVisitor.java/mathBaseVisitor.java
        # into <pkg>/antlr/, which MathAst.java above imports from. Mirrors
        # emit_python.py's generate_python_math_parser call exactly (same
        # build_math escape hatch for callers that want to skip the ANTLR
        # jar's one-time download, e.g. offline tests).
        generate_java_math_parser(os.path.join(pkg_dir, "antlr"), PKG + ".antlr", cache_dir=antlr_cache_dir)

    with open(os.path.join(out_dir, "pom.xml"), "w") as f:
        f.write(_pom_xml(maven_group_id, maven_artifact_id, description, ANTLR_VERSION, version))

    _copy_fixture_test_java(out_dir, PKG)
    _copy_api_test_java(out_dir, PKG, model)

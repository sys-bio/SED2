package org.sedml.libsed2;

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

    public static boolean isReference(JsonNode value) {
        return value != null && value.isTextual() && value.textValue().startsWith("#");
    }

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

    /** '#' + a colon-delimited containment path + an optional chain of
     * dot-accessors / bracket indices. Pure syntax, never touches a
     * document. */
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
                for (String part : inner.split(",", -1)) {
                    if (!part.strip().isEmpty()) accessors.add(new ParsedReference.Accessor(null, parseRefIndex(part)));
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
     * walk, or the collection name itself is unrecognized. */
    public static final class Resolved {
        public final Object element;
        public final String prefix;

        Resolved(Object element, String prefix) {
            this.element = element;
            this.prefix = prefix;
        }
    }

    /** Walks parsed.path's containment tree against `document` one
     * colon-segment at a time (SEDBase-0006). */
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
            // is never scoped; only its .range/.index outputs are, since those
            // only have a value during one iteration.
            targetRepeat = ("range".equals(dotName) || "index".equals(dotName)) ? resolved : null;
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

    private static List<ValidationProblem> checkConstantAccessor(ParsedReference parsed, Object resolved,
            SedBase document, String className, String idValue, String attr, String location, String value,
            FieldInfo info) {
        String dotName = parsed.firstDotName();
        if (dotName != null) {
            // SEDBase-0008.md: "For a constants ... target, no dot-accessor is valid."
            return new ArrayList<>(Handwritten.sedBase0008(false, dotName, value, className, idValue, attr, location));
        }
        List<RefIndex> indexAccessors = parsed.indexAccessors();
        Object constValue = resolved;
        if (constValue instanceof JsonNode && isReference((JsonNode) constValue)) {
            // SEDBase-0012.md: "A constant whose value is itself a reference is
            // followed first." One hop only.
            constValue = getSedReference(document, parse(((JsonNode) constValue).textValue())).element;
        }
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
        problems.addAll(Handwritten.sedBase0009(r.dimsBefore, r.indexAccessors, value, className, idValue, attr, location));
        problems.addAll(Handwritten.sedBase0010(r.dimsBefore, r.indexAccessors, value, className, idValue, attr, location));
        problems.addAll(Handwritten.sedBase0011(r.dimsBefore, r.indexAccessors, value, className, idValue, attr, location));
        problems.addAll(Handwritten.sedBase0014(r.dimsBefore, r.indexAccessors, value, className, idValue, attr, location));

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

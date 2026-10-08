// Reference resolution and the dispatchers for every reference-driven rule -
// the C++ port of the reference implementation's RUNTIME dispatch
// (generator/emit_python.py: get_sed_reference, _check_reference_field,
// _check_repeat_scoping, _check_task_order, _check_output_shape_and_ref_type,
// _check_constant_accessor, _check_repeat_own_children,
// _check_loop_variable_scope, _check_namespace_usage_and_version,
// _check_constants_ordering). SEDBase-0005 .. -0017, AbstractTask-0003,
// Repeat-0008 .. -0010, LoopVariable-0004 and SEDDocument-0009 .. -0011 /
// -0013 themselves live one-per-file in rules/ (templates/cpp/rules/); this
// file only works out what each one needs to be told and calls it.
//
// SedBase::validate_own() (Runtime.hpp) only *declares* class RefRules (to
// break the header cycle, exactly like MathRules); this file supplies the
// out-of-line `inline` bodies. A rule group whose files this spec tree did not
// define (a different spec, such as the synthetic test tree, whose own
// convention is not the tasks/constants/outputs/styles vocabulary) is compiled
// out via the SED2_REFRULES_* macros Rules.hpp defines - the C++ analog of the
// reference implementation's ImportError guards - and its checks degrade to a
// no-op. Nothing here ever throws for a bad document.
//
// Hand-written template (templates/cpp/runtime/RefRules.hpp), copied into the
// generated include tree by generator/emit_cpp.py with the literal namespace
// name "libsed2" rewritten to --cpp-namespace. ASCII only.
#pragma once

#include "Runtime.hpp"
#include "OutputsShape.hpp"
#include "Reference.hpp"
#include "Rules.hpp"

#include <algorithm>
#include <cmath>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace libsed2 {

namespace refdetail {

/// What a reference's containment path resolved to: a document element
/// (tasks / outputs / styles entries and anything nested in them), or a raw
/// JSON value (a `constants` entry - never an element, so it has no parent and
/// counts simply as "not one of my own children").
struct ResolvedRef {
    SedBase* elem = nullptr;
    const Json* raw = nullptr;
    // A JSON null constant counts as "did not resolve": the reference
    // implementation's get_sed_reference() signals failure with None, which a
    // null constant value is indistinguishable from.
    bool ok() const { return elem != nullptr || (raw != nullptr && !raw->is_null()); }
};

struct GetRef {
    ResolvedRef resolved;
    std::optional<std::string> prefix;   // nullopt: nothing to walk (no document / unknown collection)
};

/// Walks parsed.path's containment tree against `document` one colon-segment
/// at a time (SEDBase-0006). Returns the target plus the '#...'-prefixed string
/// of everything walked (the longest resolved prefix, on failure).
inline GetRef resolve_target(SedBase* document, const ParsedReference& parsed) {
    GetRef out;
    if (document == nullptr || !parsed.collection) return out;
    const std::string& cname = *parsed.collection;
    if (cname != "tasks" && cname != "constants" && cname != "outputs" && cname != "styles") return out;
    std::string prefix = "#" + cname;
    out.prefix = prefix;
    const IdKeyedCollection* dcoll = document->find_dict_collection(cname);
    const AnyDictCollection* acoll = document->find_any_dict_collection(cname);
    if ((!dcoll && !acoll) || parsed.path.empty()) return out;
    size_t pos = 0;
    const std::string& first_id = parsed.path[pos++];
    ResolvedRef current;
    if (dcoll) {
        current.elem = dcoll->find(first_id);
    } else {
        current.raw = acoll->find(first_id);
    }
    if (current.elem == nullptr && current.raw == nullptr) return out;   // no such entry
    prefix += ":" + first_id;
    out.prefix = prefix;
    while (pos < parsed.path.size()) {
        if (parsed.path.size() - pos < 2) return out;   // a lone trailing segment names a plain attribute
        const std::string& subcoll_name = parsed.path[pos];
        const std::string& item_id = parsed.path[pos + 1];
        pos += 2;
        if (!current.elem) return out;                  // a raw constant value has no child collections
        const IdKeyedCollection* sub = current.elem->find_dict_collection(subcoll_name);
        if (!sub) return out;
        SedBase* next = sub->find(item_id);
        if (!next) return out;
        current = ResolvedRef();
        current.elem = next;
        prefix += ":" + subcoll_name + ":" + item_id;
        out.prefix = prefix;
    }
    out.resolved = current;
    return out;
}

inline void append(std::vector<ValidationProblem>& into, std::vector<ValidationProblem> more) {
    for (auto& p : more) into.push_back(std::move(p));
}

inline bool is_ref_string(const Json& v) {
    return v.is_string() && !v.as<std::string>().empty() && v.as<std::string>()[0] == '#';
}

// ---- SEDBase-0013 / AbstractTask-0003 support: containment-tree walks -----

inline SedBase* nearest_repeat_ancestor(SedBase* elem) {
    for (SedBase* cur = elem; cur != nullptr; cur = cur->get_parent()) {
        if (cur->find_dict_collection("subTasks") != nullptr) return cur;
    }
    return nullptr;
}

inline bool is_ancestor_or_self(SedBase* candidate, SedBase* elem) {
    for (SedBase* cur = elem; cur != nullptr; cur = cur->get_parent()) {
        if (cur == candidate) return true;
    }
    return false;
}

struct Membership {
    SedBase* owner = nullptr;
    std::string id;
    size_t index = 0;
};

/// The (owner, id, index) if node's own parent stores node directly under a
/// 'tasks' or 'subTasks' id-keyed collection.
inline std::optional<Membership> dict_membership(SedBase* node) {
    SedBase* parent = node->get_parent();
    if (!parent) return std::nullopt;
    for (const char* coll_name : {"tasks", "subTasks"}) {
        const IdKeyedCollection* coll = parent->find_dict_collection(coll_name);
        if (!coll) continue;
        size_t idx = 0;
        for (const auto& iid : coll->ids()) {
            if (coll->find(iid) == node) {
                Membership m;
                m.owner = parent;
                m.id = iid;
                m.index = idx;
                return m;
            }
            idx++;
        }
    }
    return std::nullopt;
}

using Chain = std::vector<std::pair<std::string, size_t>>;

/// The chain of dict-membership steps from SEDDocument.tasks down to whichever
/// tasks/subTasks entry contains `elem`, outermost first; nullopt if elem isn't
/// reachable inside doc.tasks at all.
inline std::optional<Chain> task_chain(SedBase* elem, SedBase* doc) {
    SedBase* node = elem;
    Chain chain;
    while (node != nullptr && node != doc) {
        auto m = dict_membership(node);
        if (m) {
            chain.push_back({m->id, m->index});
            node = m->owner;
            continue;
        }
        node = node->get_parent();
    }
    if (chain.empty()) return std::nullopt;
    std::reverse(chain.begin(), chain.end());
    return chain;
}

inline bool task_order_ok(const Chain& rchain, const Chain& tchain) {
    size_t n = std::min(rchain.size(), tchain.size());
    for (size_t i = 0; i < n; i++) {
        if (rchain[i].first != tchain[i].first) return tchain[i].second < rchain[i].second;
    }
    if (tchain.size() <= rchain.size()) return tchain.size() < rchain.size();
    return true;
}

// ---- ref-type helpers ------------------------------------------------------

inline bool is_ref_type_kind(const std::string& k) {
    return k == "NumberOrRef" || k == "StringOrRef" || k == "IntegerOrRef" || k == "BooleanOrRef" ||
           k == "ArrayOrRef" || k == "DictOrRef";
}

inline const char* scalar_expected(const std::string& k) {
    if (k == "NumberOrRef") return "number";
    if (k == "StringOrRef") return "string";
    if (k == "IntegerOrRef") return "integer";
    if (k == "BooleanOrRef") return "boolean";
    return nullptr;
}

inline bool element_matches(const Json& element, const std::optional<std::string>& item_kind) {
    if (item_kind && *item_kind == "string") return element.is_string();
    if (item_kind && *item_kind == "number") return element.is_number() || is_ref_string(element);
    if (item_kind && *item_kind == "ref") return is_ref_string(element);
    return true;
}

/// The reference implementation's _literal_matches_kind for a REAL value (a
/// constant's own literal, fully indexed): enum membership, numeric bounds and
/// array/dict element kinds can be checked exactly here.
inline bool literal_matches_kind(const oshape::Literal& lit, const RefFieldInfo& info) {
    if (lit.kind != oshape::Literal::JSON) return false;
    const Json& value = lit.j;
    const std::string& kind = info.field_kind;
    if (kind == "NumberOrRef" || kind == "IntegerOrRef") {
        bool ok;
        if (kind == "NumberOrRef") {
            ok = value.is_number();
        } else {
            ok = (value.is_number() && !value.is_double()) ||
                 (value.is_double() && std::floor(value.as<double>()) == value.as<double>());
        }
        if (!ok) return false;
        double d = value.as<double>();
        if (info.minimum && d < *info.minimum) return false;
        if (info.exclusive_minimum && d <= *info.exclusive_minimum) return false;
        return true;
    }
    if (kind == "BooleanOrRef") return value.is_bool();
    if (kind == "StringOrRef") {
        if (!value.is_string()) return false;
        if (info.expected_enum) {
            std::string s = value.as<std::string>();
            for (const auto& e : *info.expected_enum) if (e == s) return true;
            return false;
        }
        return true;
    }
    if (kind == "ArrayOrRef") {
        if (!value.is_array()) return false;
        for (const auto& e : value.array_range()) if (!element_matches(e, info.item_kind)) return false;
        return true;
    }
    if (kind == "DictOrRef") {
        if (!value.is_object()) return false;
        for (const auto& kv : value.object_range()) if (!element_matches(kv.value(), info.item_kind)) return false;
        return true;
    }
    return true;
}

inline std::string fmt_literal(const oshape::Literal& lit) {
    if (lit.kind == oshape::Literal::JSON) return pyfmt::dumps(lit.j);
    if (lit.kind == oshape::Literal::NONE) return "null";
    return lit.element_repr;
}

/// (kind, description) of a constant's (fully indexed) literal value for
/// SEDBase-0016/-0017: a number/string/boolean/array is AnnotatedData, an
/// object is neither a model nor AnnotatedData, anything else undecidable.
inline std::pair<std::optional<std::string>, std::string> constant_target_kind(const oshape::Literal& lit) {
    if (lit.kind != oshape::Literal::JSON) return {std::nullopt, ""};
    const Json& v = lit.j;
    if (v.is_bool()) return {std::string("annotatedData"), "a boolean"};
    if (v.is_number()) return {std::string("annotatedData"), "a number"};
    if (v.is_string()) return {std::string("annotatedData"), "a string"};
    if (v.is_array()) return {std::string("annotatedData"), "an array"};
    if (v.is_object()) return {std::string("object"), "an object"};
    return {std::nullopt, ""};
}

// `indexed`: the reference applies bracket indices, so a model is the current
// value of the element it names (core Types, "Elements of models"), a number.
inline std::pair<std::optional<std::string>, std::string> output_target_kind(const Json* entry, bool indexed = false) {
    if (entry && entry->is_object() && entry->contains("type") && entry->at("type").is_string()) {
        std::string declared = entry->at("type").as<std::string>();
        if (declared == "model" && indexed) return {std::string("annotatedData"), "a model element's value"};
        if (declared == "model") return {std::string("model"), "a model"};
        if (declared == "annotatedData") return {std::string("annotatedData"), "an annotatedData value"};
        if (declared == "stringList") return {std::string("annotatedData"), "a stringList value"};
    }
    return {std::nullopt, ""};
}

inline std::vector<ValidationProblem> check_ref_target(const std::optional<std::string>& ref_target,
                                                       const std::optional<std::string>& kind,
                                                       const std::string& description, const RuleCtx& ctx) {
#ifdef SED2_REFRULES_TARGET
    if (ref_target && *ref_target == "model") return rules::sedbase_0016::check(kind, description, ctx);
    if (ref_target && *ref_target == "annotatedData") return rules::sedbase_0017::check(kind, description, ctx);
#else
    (void)ref_target; (void)kind; (void)description; (void)ctx;
#endif
    return {};
}

inline ValidationProblem ref_type_problem(const std::string& rule_id, const RuleCtx& ctx,
                                          const std::string& resolved_desc) {
    return RuleCatalog::make_problem(rule_id, ctx.location,
        {{"attr", ctx.attr}, {"value", ctx.value}, {"class", ctx.class_name}, {"id", ctx.id_value},
         {"resolved-value", resolved_desc}});
}

inline std::string element_repr(SedBase* elem) {
    return "<" + elem->class_name() + " object>";
}

#ifdef SED2_REFRULES_SHAPE

/// follow_constant_alias()'s result: the followed value, or why it could not be
/// followed ("unresolved": the chain leads nowhere that can be evaluated here -
/// a missing constant, a cycle, a dot-accessor; some other rule reports those -
/// or "index": an index in the chain does not fit the value it is applied to,
/// with bad the index as SEDBase-0012's {subvalue} prints it and literal_text
/// the value indexed).
struct Followed {
    oshape::Literal value;
    std::string failure;   // "", "unresolved" or "index"
    std::string bad;
    std::string literal_text;
};

/// A constant's value once it has been followed through every reference it is
/// made of (SEDBase-0012.md: "A constant whose value is itself a reference is
/// followed first"): for a value that is a reference string to another
/// constant, that constant's value, itself followed, with the reference's own
/// bracket indices applied - so an alias such as "#constants:table['S2']" is its
/// row, not the whole table, and an alias of an alias is followed to the end. A
/// reference to a task, output or style is returned as the element (its indices
/// are not applied).
inline Followed follow_constant_alias(SedBase* document, const Json& value, const std::set<std::string>& seen) {
    Followed out;
    out.value.kind = oshape::Literal::JSON;
    out.value.j = value;
    if (!is_ref_string(value)) return out;
    ParsedReference inner = parse_reference(value.as<std::string>());
    if (!inner.collection || *inner.collection != "constants") {
        GetRef g = resolve_target(document, inner);
        if (g.resolved.raw) {
            out.value.j = *g.resolved.raw;
        } else if (g.resolved.elem) {
            out.value.kind = oshape::Literal::ELEMENT;
            out.value.j = Json();
            out.value.element_repr = element_repr(g.resolved.elem);
        } else {
            out.value.kind = oshape::Literal::NONE;
            out.value.j = Json();
        }
        return out;
    }
    const AnyDictCollection* coll = document ? document->find_any_dict_collection("constants") : nullptr;
    const Json* stored = (coll && inner.path.size() == 1) ? coll->find(inner.path[0]) : nullptr;
    if (!stored || seen.count(inner.path[0]) || inner.first_dot()) {
        out.failure = "unresolved";
        return out;
    }
    std::set<std::string> next = seen;
    next.insert(inner.path[0]);
    Followed base = follow_constant_alias(document, *stored, next);
    if (!base.failure.empty()) return base;
    oshape::IndexResult ir = oshape::index_into_literal(base.value, inner.indices());
    if (!ir.ok) {
        out.failure = "index";
        out.bad = ir.bad_subvalue;
        out.literal_text = fmt_literal(base.value);
        return out;
    }
    out.value = ir.value;
    return out;
}

inline std::vector<ValidationProblem> check_constant_accessor(const ParsedReference& parsed, const Json& raw,
                                                              SedBase* document, const RuleCtx& ctx,
                                                              const RefFieldInfo& info) {
    auto dot = parsed.first_dot();
    if (dot) return rules::sedbase_0008::check(std::optional<bool>(false), dot, ctx);
    std::vector<RefIndex> index_accessors = parsed.indices();
    // SEDBase-0012.md: "A constant whose value is itself a reference is
    // followed first" - through a chain of constants and with each alias's own
    // indices applied (follow_constant_alias).
    Followed followed = follow_constant_alias(document, raw, {});
    if (!followed.failure.empty()) {
        if (followed.failure == "index") return rules::sedbase_0012::check(false, followed.bad, followed.literal_text, ctx);
        return {};
    }
    oshape::Literal lit = followed.value;
    oshape::IndexResult ir = oshape::index_into_literal(lit, index_accessors);
    if (!ir.ok) return rules::sedbase_0012::check(false, ir.bad_subvalue, fmt_literal(lit), ctx);
    if (info.ref_target) {
        auto kd = constant_target_kind(ir.value);
        return check_ref_target(info.ref_target, kd.first, kd.second, ctx);
    }
    if (!info.ref_type_rule_id || !is_ref_type_kind(info.field_kind)) return {};
    if (!literal_matches_kind(ir.value, info)) {
        return {ref_type_problem(*info.ref_type_rule_id, ctx, fmt_literal(ir.value))};
    }
    return {};
}

inline std::vector<ValidationProblem> check_output_shape_and_ref_type(const ParsedReference& parsed,
                                                                      const ResolvedRef& resolved,
                                                                      SedBase* document, const RuleCtx& ctx,
                                                                      const RefFieldInfo& info) {
    if (parsed.collection && *parsed.collection == "constants") {
        if (!resolved.raw) return {};
        return check_constant_accessor(parsed, *resolved.raw, document, ctx, info);
    }
    if (!resolved.elem) return {};
    const Json* outputs_json = resolved.elem->outputs_json();
    if (outputs_json == nullptr) {
        // styles / a nested non-tasks/ class reached via a tasks: path
        // (LoopVariable, TaskParameter, ...): a bare reference is always fine,
        // only a dot-accessor on top is invalid (SEDBase-0008.md).
        auto dot = parsed.first_dot();
        if (!dot) return {};
        return rules::sedbase_0008::check(std::optional<bool>(false), dot, ctx);
    }

    int depth = 0;
    oshape::ShapeOf shape_of;
    shape_of = [&](const std::string& ref_string) -> oshape::Dims {
        depth++;
        if (depth > 25) throw oshape::NotStatic("shapeOf() recursion too deep");
        ParsedReference parsed2 = parse_reference(ref_string);
        GetRef g2 = resolve_target(document, parsed2);
        SedBase* inner = g2.resolved.elem;
        const Json* inner_oj = inner ? inner->outputs_json() : nullptr;
        if (inner_oj == nullptr) throw oshape::NotStatic("shapeOf() target has no outputs.json");
        Json inner_fields = inner->own_json_value();
        oshape::OutputResolution r = oshape::resolve_output(*inner_oj, inner_fields, parsed2.accessors, shape_of);
        if (r.ok != std::optional<bool>(true) || !r.dims_after) {
            throw oshape::NotStatic("shapeOf() target shape not statically known");
        }
        return *r.dims_after;
    };

    oshape::OutputResolution res;
    try {
        Json fields = resolved.elem->own_json_value();
        res = oshape::resolve_output(*outputs_json, fields, parsed.accessors, shape_of);
    } catch (const std::exception&) {
        return {};
    }

    std::vector<ValidationProblem> problems = rules::sedbase_0008::check(res.ok, res.dot_name, ctx);
    if (res.ok != std::optional<bool>(true)) return problems;
    // Each rule judges an index against the dimension that index is applied
    // to (chained brackets: the dimension as the earlier ranges left it).
    oshape::OptDims seen_dims = oshape::bind_indices(res.dims_before, res.index_accessors).seen;
    append(problems, rules::sedbase_0009::check(seen_dims, res.index_accessors, ctx));
    append(problems, rules::sedbase_0010::check(seen_dims, res.index_accessors, ctx));
    append(problems, rules::sedbase_0011::check(seen_dims, res.index_accessors, ctx));
    append(problems, rules::sedbase_0014::check(seen_dims, res.index_accessors, ctx));

    if (info.ref_target) {
        auto kd = output_target_kind(res.entry, !res.index_accessors.empty());
        append(problems, check_ref_target(info.ref_target, kd.first, kd.second, ctx));
    }
    if (info.ref_type_rule_id && is_ref_type_kind(info.field_kind)) {
        std::string actual_declared;
        bool has_declared = false;
        if (res.entry && res.entry->is_object() && res.entry->contains("type") && res.entry->at("type").is_string()) {
            actual_declared = res.entry->at("type").as<std::string>();
            has_declared = true;
            // An indexed model is the value of one of its elements: a number.
            if (actual_declared == "model" && !res.index_accessors.empty()) actual_declared = "annotatedData";
        }
        if (has_declared && actual_declared == "model") {
            // A model is a type of its own: never a number, string, boolean,
            // array, or dictionary.
            problems.push_back(ref_type_problem(*info.ref_type_rule_id, ctx, "a model"));
        } else if (scalar_expected(info.field_kind)) {
            std::string expected = scalar_expected(info.field_kind);
            append(problems, rules::sedbase_0015::check(res.dims_after, expected, ctx));
            if (res.dims_after && res.dims_after->empty()) {
                const char* mapped = nullptr;
                if (has_declared && actual_declared == "annotatedData") mapped = "number";
                if (has_declared && actual_declared == "stringList") mapped = "string";
                if (mapped != nullptr && expected != mapped) {
                    problems.push_back(ref_type_problem(*info.ref_type_rule_id, ctx,
                                                        "a " + actual_declared + " value"));
                }
            }
        } else if (info.field_kind == "ArrayOrRef") {
            // Only the unambiguous mismatch: an array of numbers fed a
            // stringList output.
            if (info.item_kind && *info.item_kind == "number" && has_declared && actual_declared == "stringList") {
                problems.push_back(ref_type_problem(*info.ref_type_rule_id, ctx, "a stringList value"));
            }
        }
    }
    return problems;
}

#endif  // SED2_REFRULES_SHAPE

}  // namespace refdetail

// ---- the RefRules entry points declared in Runtime.hpp -------------------

inline std::vector<ValidationProblem> RefRules::check_reference_field(
        const std::string& value, SedBase* document, const RuleCtx& base_ctx, SedBase* referrer,
        const RefFieldInfo& info) {
    std::vector<ValidationProblem> problems;
#ifdef SED2_REFRULES_BASIC
    using namespace refdetail;
    ParsedReference parsed = parse_reference(value);
    RuleCtx ctx = base_ctx;
    ctx.value = value;
    problems = rules::sedbase_0005::check(parsed, ctx);
    if (!problems.empty()) return problems;   // unknown collection - nothing further can resolve
    append(problems, rules::sedbase_0007::check(parsed, ctx));
    GetRef g = resolve_target(document, parsed);
    append(problems, rules::sedbase_0006::check(parsed, g.resolved.ok(), g.prefix, ctx));
    if (!g.resolved.ok() || *parsed.collection == "outputs") return problems;

#ifdef SED2_REFRULES_SCOPE
    if (*parsed.collection != "constants" && g.resolved.elem && referrer) {
        // Pure containment-tree ancestry (SEDBase-0013): a Repeat's subTasks,
        // its .range/.index outputs (and a ParameterScan's .ranges/.indexes/.model) and its loop
        // variables are only legal from inside that Repeat. A constants target is a raw JSON value with no
        // containment ancestry, so the concept doesn't apply to it at all.
        SedBase* resolved = g.resolved.elem;
        auto dot_name = parsed.first_dot();
        SedBase* target_repeat = nullptr;
        if (resolved->find_dict_collection("subTasks") != nullptr) {
            // A bare/.model/.aggregates/.strings reference to the Repeat ITSELF
            // is never scoped; only its per-iteration outputs are:
            // .range/.index, and a ParameterScan's .ranges/.indexes and
            // .model (the model as modified for the current iteration).
            if (dot_name && (*dot_name == "range" || *dot_name == "index" ||
                             ((*dot_name == "model" || *dot_name == "ranges" || *dot_name == "indexes") &&
                              resolved->class_name() == "ParameterScan"))) {
                target_repeat = resolved;
            }
        } else {
            SedBase* parent = resolved->get_parent();
            if (parent) target_repeat = nearest_repeat_ancestor(parent);
        }
        if (target_repeat && !is_ancestor_or_self(target_repeat, referrer)) {
            append(problems, rules::sedbase_0013::check(false, target_repeat->own_id_for_message(), ctx));
        }
    }
#endif
#ifdef SED2_REFRULES_TASKORDER
    if (*parsed.collection == "tasks" && g.resolved.elem && referrer && document) {
        // AbstractTask-0003's chronological rule; Output/Style referrers have
        // no chain and are exempt (core-spec.md Section 3).
        auto rchain = task_chain(referrer, document);
        if (rchain) {
            auto tchain = task_chain(g.resolved.elem, document);
            if (tchain) append(problems, rules::abstracttask_0003::check(task_order_ok(*rchain, *tchain), ctx));
        }
    }
#endif
#ifdef SED2_REFRULES_SHAPE
    append(problems, check_output_shape_and_ref_type(parsed, g.resolved, document, ctx, info));
#endif
#else
    (void)value; (void)document; (void)base_ctx; (void)referrer; (void)info;
#endif
    return problems;
}

namespace refdetail {

#ifdef SED2_REFRULES_REPEAT

inline bool resolves_to_own_child(SedBase* self, SedBase* document, const std::string& ref_value) {
    if (document == nullptr) return false;
    ParsedReference parsed = parse_reference(ref_value);
    GetRef g = resolve_target(document, parsed);
    return g.resolved.elem != nullptr && g.resolved.elem->get_parent() == self;
}

#endif

}  // namespace refdetail

/// Repeat-0008/-0009/-0010: a Repeat-family instance's own children
/// (outputVariableMap / aggregateOutputVariables) must stay scoped to that same
/// instance's own subTasks, and an aggregateOutputVariables entry may never
/// define appliedDimensions. Detected by class SHAPE (a subTasks collection),
/// not by name, so this applies uniformly to every Repeat-family class.
inline std::vector<ValidationProblem> RefRules::check_repeat_own_children(SedBase* self) {
    std::vector<ValidationProblem> problems;
#ifdef SED2_REFRULES_REPEAT
    using namespace refdetail;
    if (self->find_dict_collection("subTasks") == nullptr) return problems;
    SedBase* document = self->get_document();
    std::string cls = self->class_name();
    std::string self_id = self->own_id_for_message();

    auto ovm_it = self->values_.find("outputVariableMap");
    if (ovm_it != self->values_.end() && ovm_it->second.is_object()) {
        for (const auto& kv : ovm_it->second.object_range()) {
            if (!is_ref_string(kv.value())) continue;
            std::string key(kv.key());
            std::string entry_value = kv.value().as<std::string>();
            if (!resolves_to_own_child(self, document, entry_value)) {
                RuleCtx ctx{cls, self_id, key, "/outputVariableMap/" + key, entry_value};
                append(problems, rules::repeat_0008::check(false, ctx));
            }
        }
    }
    const IdKeyedCollection* agg = self->find_dict_collection("aggregateOutputVariables");
    if (agg != nullptr) {
        for (const auto& entry_id : agg->ids()) {
            SedBase* entry = agg->find(entry_id);
            Json entry_json = entry->own_json_value();
            if (entry_json.contains("appliedDimensions")) {
                RuleCtx ctx{cls, self_id, "appliedDimensions",
                            "/aggregateOutputVariables/" + entry_id + "/appliedDimensions",
                            pyfmt::str(entry_json.at("appliedDimensions"))};
                append(problems, rules::repeat_0010::check(true, ctx));
            }
            if (entry_json.contains("input") && is_ref_string(entry_json.at("input"))) {
                std::string input_value = entry_json.at("input").as<std::string>();
                if (!resolves_to_own_child(self, document, input_value)) {
                    RuleCtx ctx{cls, self_id, "input", "/aggregateOutputVariables/" + entry_id + "/input",
                                input_value};
                    append(problems, rules::repeat_0009::check(false, ctx));
                }
            }
        }
    }
#else
    (void)self;
#endif
    return problems;
}

/// LoopVariable-0004: subsequentValues stays scoped to the enclosing Loop's own
/// subTasks - same shape as Repeat-0008/-0009, for the one field a LoopVariable
/// itself carries.
inline std::vector<ValidationProblem> RefRules::check_loop_variable_scope(SedBase* self) {
    std::vector<ValidationProblem> problems;
#if defined(SED2_REFRULES_LOOPVAR)
    using namespace refdetail;
    auto it = self->values_.find("subsequentValues");
    if (it == self->values_.end() || !is_ref_string(it->second)) return problems;
    SedBase* enclosing = self->get_parent();
    if (enclosing == nullptr) return problems;
    SedBase* document = self->get_document();
    std::string value = it->second.as<std::string>();
    bool ok = false;
    if (document != nullptr) {
        GetRef g = resolve_target(document, parse_reference(value));
        ok = g.resolved.elem != nullptr && g.resolved.elem->get_parent() == enclosing;
    }
    if (ok) return problems;
    RuleCtx ctx{"LoopVariable", self->own_id_for_message(), "subsequentValues", "/subsequentValues", value};
    append(problems, rules::loopvariable_0004::check(false, ctx));
#else
    (void)self;
#endif
    return problems;
}

namespace refdetail {

inline void walk_with_locations(SedBase* obj, const std::string& prefix,
                                std::vector<std::pair<SedBase*, std::string>>& out) {
    out.push_back({obj, prefix});
    for (const auto& cl : obj->children_with_locations()) walk_with_locations(cl.child, prefix + cl.location_prefix, out);
}

}  // namespace refdetail

/// SEDDocument-0009 .. -0011: whole-document namespace-usage-vs-declared-version
/// and version-newer-than-known checks, called once from the document root.
inline std::vector<ValidationProblem> RefRules::check_namespace_usage_and_version(SedBase* document) {
    std::vector<ValidationProblem> problems;
#ifdef SED2_REFRULES_NS
    using namespace refdetail;
    // "used" means any attribute key or _type value of the form
    // prefix@identifier anywhere in the document - registered and unregistered
    // prefixes alike. The <prefix>@version declaration itself (only ever stored
    // on the document root) doesn't count as a use of that prefix.
    std::map<std::string, std::string> declared;   // prefix -> "/<prefix>@version"
    for (const auto& kv : document->ns_attrs_) {
        size_t at = kv.first.find('@');
        if (at == std::string::npos) continue;
        if (kv.first.substr(at + 1) == "version") declared[kv.first.substr(0, at)] = "/" + kv.first;
    }
    std::map<std::string, std::vector<std::string>> used;   // prefix -> [locations]
    std::vector<std::pair<SedBase*, std::string>> nodes;
    walk_with_locations(document, "", nodes);
    for (const auto& n : nodes) {
        SedBase* obj = n.first;
        for (const auto& kv : obj->ns_attrs_) {
            size_t at = kv.first.find('@');
            if (at == std::string::npos) continue;
            std::string pfx = kv.first.substr(0, at), key = kv.first.substr(at + 1);
            if (obj == document && key == "version") continue;
            used[pfx].push_back(n.second + "/" + kv.first);
        }
        auto tv = obj->get_type_value();
        if (tv && tv->find('@') != std::string::npos) used[tv->substr(0, tv->find('@'))].push_back(n.second + "/_type");
    }
    for (const auto& kv : used) {
        if (declared.count(kv.first)) continue;
        for (const auto& loc : kv.second) append(problems, rules::seddocument_0009::check(kv.first, loc));
    }
    for (const auto& kv : declared) {
        if (!used.count(kv.first)) append(problems, rules::seddocument_0010::check(kv.first, kv.second));
    }
    const Json* version = nullptr;
    auto vit = document->values_.find("version");
    if (vit != document->values_.end()) version = &vit->second;
    append(problems, rules::seddocument_0011::check(document->max_known_document_version(), version));
#else
    (void)document;
#endif
    return problems;
}

/// SEDDocument-0013: a constant may only reference constants that appear
/// before it in the constants dictionary.
inline std::vector<ValidationProblem> RefRules::check_constants_ordering(SedBase* document) {
    std::vector<ValidationProblem> problems;
#ifdef SED2_REFRULES_CONSTORDER
    const AnyDictCollection* coll = document->find_any_dict_collection("constants");
    if (coll == nullptr) return problems;
    std::vector<std::pair<std::string, Json>> constants;
    for (const auto& cid : coll->ids()) constants.push_back({cid, *coll->find(cid)});
    problems = rules::seddocument_0013::check(constants);
#else
    (void)document;
#endif
    return problems;
}

/// SEDBase-0005 applied to a REFERENCE token embedded in a math string.
inline std::vector<ValidationProblem> RefRules::check_math_reference_root(
        const std::string& reference_text, const std::string& class_name, const std::string& id_value,
        const std::string& attr, const std::string& location) {
#ifdef SED2_REFRULES_BASIC
    RuleCtx ctx{class_name, id_value, attr, location, reference_text};
    return rules::sedbase_0005::check(parse_reference(reference_text), ctx);
#else
    (void)reference_text; (void)class_name; (void)id_value; (void)attr; (void)location;
    return {};
#endif
}

// ---- public API: reference resolution ------------------------------------
// (parse_reference() / ParsedReference / RefIndex, in Reference.hpp, are the
// other half of the public reference API.)

/// What get_sed_reference() found. For a "#tasks:", "#outputs:" or "#styles:"
/// reference `element` points at the target element; for a "#constants:"
/// reference `value` points at the constant's raw JSON value. Both pointers
/// are non-owning and point into the document, so they are valid only while
/// the document is alive and unmodified. Both are null when the reference did
/// not resolve (a constant holding JSON null counts as not resolved, too).
struct ReferenceTarget {
    SedBase* element = nullptr;
    const Json* value = nullptr;
    /// The "#..."-prefixed text of everything walked (on failure, the longest
    /// prefix that resolved); nullopt when there was no document to walk or the
    /// collection name itself is unrecognized.
    std::optional<std::string> resolved_prefix;

    /// True when the reference resolved to an element or to a non-null constant.
    bool is_resolved() const { return element != nullptr || (value != nullptr && !value->is_null()); }
};

/// Resolves a reference to its target by walking its containment path
/// (everything before the first '.' or '[') against `document` one
/// colon-segment at a time (SEDBase-0006). The trailing accessor chain is
/// parsed (see ParsedReference::accessors) but never applied. Never throws for
/// an unresolvable reference; check is_resolved(). Public API.
inline ReferenceTarget get_sed_reference(SedBase* document, const ParsedReference& parsed) {
    refdetail::GetRef g = refdetail::resolve_target(document, parsed);
    ReferenceTarget out;
    out.element = g.resolved.elem;
    out.value = (g.resolved.raw != nullptr && !g.resolved.raw->is_null()) ? g.resolved.raw : nullptr;
    out.resolved_prefix = g.prefix;
    return out;
}

/// Resolves a reference given as text: parse_reference(reference), then
/// get_sed_reference(document, parsed). Public API.
inline ReferenceTarget get_sed_reference(SedBase* document, const std::string& reference) {
    return get_sed_reference(document, parse_reference(reference));
}

// ---- public API: values of constants and literals -------------------------

namespace refdetail {

/// A RefIndex as it is written in a reference: [3], ['S1'], [2:5].
inline std::string format_index(const RefIndex& idx) {
    if (idx.is_label()) return "['" + idx.sval + "']";
    if (idx.is_range()) {
        return "[" + (idx.a ? std::to_string(*idx.a) : std::string()) + ":" +
               (idx.b ? std::to_string(*idx.b) : std::string()) + "]";
    }
    return "[" + std::to_string(idx.ival) + "]";
}

}  // namespace refdetail

/// Applies bracket indices to a literal JSON value - a constant's value, or
/// any other literal (a number, string, array or object) - and returns a copy
/// of the selected part. Indices follow the reference grammar (Design.md,
/// Cross-references): an int ([3], or [-1] counting from the end) indexes an
/// array; a label (['S1']) indexes an object by key; a range ([2:5], either
/// end optional) slices an array, end-exclusive, clamped to the array like a
/// Python slice, and keeps the dimension, while an int or label drops it. The
/// same rules back SEDBase-0012, so a reference that validates cleanly always
/// applies cleanly. Throws ApiError when an index does not fit the value (an
/// int or range into anything but an array, a label into anything but an
/// object that has the key, an int outside -n..n-1, any index into a
/// scalar). Public API.
inline Json apply_indices(const Json& value, const std::vector<RefIndex>& indices) {
    oshape::Literal lit;
    lit.kind = oshape::Literal::JSON;
    lit.j = value;
    oshape::IndexResult ir = oshape::index_into_literal(lit, indices);
    if (!ir.ok) {
        throw ApiError("cannot apply index " + refdetail::format_index(ir.bad_index) +
                       ": the value does not contain it (SEDBase-0012)");
    }
    return ir.value.j;
}

/// Applies the bracket indices of `accessors` (its containment path is
/// ignored) to a literal JSON value; see the vector overload. Throws ApiError
/// when `accessors` contains a dot-accessor, since a constant or literal has
/// no named outputs (SEDBase-0008). Public API.
inline Json apply_indices(const Json& value, const ParsedReference& accessors) {
    for (const auto& acc : accessors.accessors) {
        if (acc.is_dot) {
            throw ApiError("cannot apply dot-accessor '." + acc.name + "' to a constant or literal value: "
                           "only bracket indices apply to one (SEDBase-0008)");
        }
    }
    return apply_indices(value, accessors.indices());
}

/// apply_indices(value, parse_reference(accessors)); `accessors` is the
/// accessor text ("[2]['S1']") or a whole reference. Public API.
inline Json apply_indices(const Json& value, const std::string& accessors) {
    return apply_indices(value, parse_reference(accessors));
}

namespace refdetail {

inline Json get_reference_value_impl(SedBase* document, const ParsedReference& parsed, std::set<std::string> seen) {
    if (!parsed.collection || *parsed.collection != "constants") {
        throw ApiError("reference '" + parsed.raw + "' does not name a constant, so it has no value "
                       "before the experiment runs");
    }
    const AnyDictCollection* coll = document ? document->find_any_dict_collection("constants") : nullptr;
    const Json* stored = (coll && parsed.path.size() == 1) ? coll->find(parsed.path[0]) : nullptr;
    if (!stored) {
        throw ApiError("reference '" + parsed.raw + "' does not resolve: no such constant (SEDBase-0006)");
    }
    const std::string& key = parsed.path[0];
    if (seen.count(key)) {
        throw ApiError("reference '" + parsed.raw + "' is circular: constant '" + key +
                       "' refers back to itself");
    }
    seen.insert(key);
    Json value = *stored;
    if (is_ref_string(value)) {
        value = get_reference_value_impl(document, parse_reference(value.as<std::string>()), seen);
    }
    return apply_indices(value, parsed);
}

}  // namespace refdetail

/// Evaluates a reference that has a value before any experiment runs: a
/// "#constants:" reference, with any bracket indices applied to the
/// constant's literal value (see apply_indices). A constant whose value is
/// itself a reference string is followed first (SEDBase-0012), through any
/// number of constants; a chain that loops throws ApiError. A constant
/// holding JSON null evaluates to a null Json. Throws ApiError when the
/// constant does not exist (SEDBase-0006), when the reference targets
/// anything but a constant (a task, output or style has a value only when the
/// experiment runs), when it carries a dot-accessor, or when an index does
/// not fit the value. Returns a copy. Public API.
inline Json get_reference_value(SedBase* document, const ParsedReference& parsed) {
    return refdetail::get_reference_value_impl(document, parsed, {});
}

/// get_reference_value(document, parse_reference(reference)). Public API.
inline Json get_reference_value(SedBase* document, const std::string& reference) {
    return get_reference_value(document, parse_reference(reference));
}

/// ParameterScan-0007: the modelElement values of a ParameterScan's
/// parameterRanges are pairwise distinct; a modelElement given as a reference
/// is compared by the string it resolves to. Detected by class SHAPE (has a
/// parameterRanges list), not by name. Defined here, after
/// get_reference_value(), which it uses.
inline std::vector<ValidationProblem> RefRules::check_parameter_scan_ranges(SedBase* self) {
    std::vector<ValidationProblem> problems;
#ifdef SED2_REFRULES_PARAMSCAN
    std::vector<SedBase*> entries;
    try {
        entries = self->get_list_collection("parameterRanges").items();
    } catch (const ApiError&) {
        return problems;   // not a class with a parameterRanges list
    }
    SedBase* document = self->get_document();
    std::vector<std::optional<std::string>> elements;
    for (SedBase* entry : entries) {
        Json entry_json = entry->own_json_value();
        std::optional<std::string> element;
        if (entry_json.contains("modelElement")) {
            const Json& raw = entry_json.at("modelElement");
            if (refdetail::is_ref_string(raw)) {
                // compared by the string it resolves to; anything that does not
                // resolve to a string is some other rule's concern
                try {
                    Json resolved = get_reference_value(document, raw.as<std::string>());
                    if (resolved.is_string()) element = resolved.as<std::string>();
                } catch (const ApiError&) {
                }
            } else if (raw.is_string()) {
                element = raw.as<std::string>();
            }
        }
        elements.push_back(element);
    }
    RuleCtx ctx{self->class_name(), self->own_id_for_message(), "parameterRanges", "/parameterRanges", ""};
    refdetail::append(problems, rules::parameterscan_0007::check(elements, ctx));
#else
    (void)self;
#endif
    return problems;
}

}  // namespace libsed2

// outputs.json expr/valid notation (core-spec.md Section 8) - parser,
// evaluator, and shape/hasSubvalue() resolver, backing SEDBase-0008 through
// -0015 and the formulaic ref-type rules that piggyback on SEDBase-0015's
// scalar-reduction check. C++ port of the reference implementation's
// OUTPUTS_SHAPE_PY (generator/emit_python.py): a small runtime interpreter
// over each concrete task class's own embedded outputs.json.
//
// Every caller treats NotStatic as "the rule does not fire" (SEDBase-0008
// through -0011/-0014's "only fires when computable" language) rather than
// an error - validate() never throws for a bad document.
//
// Hand-written template (templates/cpp/runtime/OutputsShape.hpp), copied into
// the generated include tree by generator/emit_cpp.py with the literal
// namespace name "sed2test" rewritten to --cpp-namespace. ASCII only.
#pragma once

#include <algorithm>
#include <functional>
#include <map>
#include <memory>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

#include "PyFormat.hpp"
#include "Reference.hpp"

namespace sed2test {
namespace oshape {

class NotStatic : public std::runtime_error {
public:
    explicit NotStatic(const std::string& m) : std::runtime_error(m) {}
};

/// One resolved dimension: the reference implementation's
/// {"size", "labels", "source", "min"} dict.
struct Dim {
    std::optional<long long> size;
    std::optional<std::vector<std::string>> labels;
    std::optional<std::string> source;
    std::optional<long long> min;
};
using Dims = std::vector<Dim>;
using OptDims = std::optional<Dims>;

/// The `source` of the placeholder dimension a "trailing" entry in outputs.json
/// resolves to: zero or more further dimensions (those of the output's own
/// entries), of unknown number, size and labels. Indices that reach it are not
/// judged (it takes any number of them); on its own it never makes the result
/// "still shaped" (SEDBase-0015).
inline bool is_open(const Dim& d) { return d.source && *d.source == "open"; }

// ---- lexer ------------------------------------------------------------

struct Tok {
    std::string kind;
    std::string text;
};

inline std::vector<Tok> tokenize(const std::string& text) {
    std::vector<Tok> toks;
    size_t i = 0, n = text.size();
    while (i < n) {
        char ch = text[i];
        if (std::isspace(static_cast<unsigned char>(ch))) { i++; continue; }
        if (ch == '=' && text.compare(i, 2, "==") == 0) { toks.push_back({"==", "=="}); i += 2; continue; }
        if (std::string("+-!(),[].").find(ch) != std::string::npos) {
            toks.push_back({std::string(1, ch), std::string(1, ch)});
            i++;
            continue;
        }
        bool digit = std::isdigit(static_cast<unsigned char>(ch)) != 0;
        if (digit || (ch == '.' && i + 1 < n && std::isdigit(static_cast<unsigned char>(text[i + 1])))) {
            size_t j = i;
            while (j < n && (std::isdigit(static_cast<unsigned char>(text[j])) || text[j] == '.')) j++;
            toks.push_back({"NUMBER", text.substr(i, j - i)});
            i = j;
            continue;
        }
        if (std::isalpha(static_cast<unsigned char>(ch)) || ch == '_') {
            size_t j = i;
            while (j < n && (std::isalnum(static_cast<unsigned char>(text[j])) || text[j] == '_')) j++;
            std::string word = text.substr(i, j - i);
            if (word == "true" || word == "false") toks.push_back({"BOOL", word});
            else if (word == "or" || word == "if" || word == "else") toks.push_back({word, word});
            else toks.push_back({"IDENT", word});
            i = j;
            continue;
        }
        throw NotStatic(std::string("unexpected character '") + ch + "' in expr");
    }
    toks.push_back({"EOF", ""});
    return toks;
}

// ---- AST ----------------------------------------------------------------

struct Node;
using NodePtr = std::shared_ptr<Node>;

struct Node {
    enum Type { NUM, BOOL, ARRAY, PATH, CALL, NOT, BINOP, COND };
    Type type = NUM;
    bool is_float = false;
    double num = 0;
    long long inum = 0;
    bool bval = false;
    std::vector<std::string> names;   // PATH names / CALL func (names[0]) / BINOP op (names[0])
    std::vector<NodePtr> kids;        // ARRAY items / CALL args / BINOP left,right / NOT operand / COND cond,then,else
};

class Parser {
public:
    explicit Parser(std::vector<Tok> toks) : toks_(std::move(toks)) {}

    NodePtr parse() {
        NodePtr node = conditional();
        eat("EOF");
        return node;
    }

private:
    std::vector<Tok> toks_;
    size_t i_ = 0;

    const Tok& peek() const { return toks_[i_]; }
    Tok eat(const std::string& kind) {
        const Tok& t = toks_[i_];
        if (t.kind != kind) throw NotStatic("expected " + kind + ", got " + t.kind);
        i_++;
        return t;
    }

    static NodePtr mk(Node::Type t) {
        auto n = std::make_shared<Node>();
        n->type = t;
        return n;
    }
    static NodePtr binop(const std::string& op, NodePtr l, NodePtr r) {
        auto n = mk(Node::BINOP);
        n->names = {op};
        n->kids = {std::move(l), std::move(r)};
        return n;
    }

    NodePtr conditional() {
        NodePtr node = or_expr();
        if (peek().kind == "if") {
            eat("if");
            NodePtr cond = or_expr();
            eat("else");
            NodePtr orelse = conditional();
            auto n = mk(Node::COND);
            n->kids = {cond, node, orelse};
            return n;
        }
        return node;
    }

    NodePtr or_expr() {
        NodePtr node = equality();
        while (peek().kind == "or") {
            eat("or");
            node = binop("or", node, equality());
        }
        return node;
    }

    NodePtr equality() {
        NodePtr node = additive();
        if (peek().kind == "==") {
            eat("==");
            node = binop("==", node, additive());
        }
        return node;
    }

    NodePtr additive() {
        NodePtr node = unary();
        while (peek().kind == "+" || peek().kind == "-") {
            std::string op = eat(peek().kind).kind;
            node = binop(op, node, unary());
        }
        return node;
    }

    NodePtr unary() {
        if (peek().kind == "!") {
            eat("!");
            auto n = mk(Node::NOT);
            n->kids = {unary()};
            return n;
        }
        return primary();
    }

    static bool is_func(const std::string& name) {
        return name == "len" || name == "keys" || name == "shapeOf" || name == "dim" || name == "provided";
    }

    NodePtr primary() {
        const Tok tok = peek();
        if (tok.kind == "NUMBER") {
            eat("NUMBER");
            auto n = mk(Node::NUM);
            if (tok.text.find('.') != std::string::npos) {
                size_t used = 0;
                try { n->num = std::stod(tok.text, &used); } catch (...) { throw NotStatic("bad number"); }
                if (used != tok.text.size()) throw NotStatic("bad number");
                n->is_float = true;
            } else {
                try { n->inum = std::stoll(tok.text); } catch (...) { throw NotStatic("bad number"); }
            }
            return n;
        }
        if (tok.kind == "BOOL") {
            eat("BOOL");
            auto n = mk(Node::BOOL);
            n->bval = tok.text == "true";
            return n;
        }
        if (tok.kind == "[") {
            eat("[");
            auto n = mk(Node::ARRAY);
            if (peek().kind != "]") {
                n->kids.push_back(conditional());
                while (peek().kind == ",") { eat(","); n->kids.push_back(conditional()); }
            }
            eat("]");
            return n;
        }
        if (tok.kind == "IDENT") {
            std::string name = eat("IDENT").text;
            if (peek().kind == "(" && is_func(name)) {
                eat("(");
                auto n = mk(Node::CALL);
                n->names = {name};
                if (peek().kind != ")") {
                    n->kids.push_back(conditional());
                    while (peek().kind == ",") { eat(","); n->kids.push_back(conditional()); }
                }
                eat(")");
                return n;
            }
            auto n = mk(Node::PATH);
            n->names = {name};
            while (peek().kind == ".") { eat("."); n->names.push_back(eat("IDENT").text); }
            return n;
        }
        throw NotStatic("unexpected token " + tok.kind + " in expr");
    }
};

inline NodePtr parse_expr(const std::string& text) {
    static std::map<std::string, NodePtr> cache;
    auto it = cache.find(text);
    if (it != cache.end()) return it->second;
    NodePtr node = Parser(tokenize(text)).parse();
    cache[text] = node;
    return node;
}

// ---- values & scopes ----------------------------------------------------

/// An evaluated expr value. JSON covers everything a document field can hold
/// (and arrays/numbers/strings built by the notation); the other kinds are the
/// notation's own: the `outermost` sentinel, a resolved dims list (shapeOf()),
/// and a dim() selector list.
struct Val {
    enum Kind { JSON, OUTERMOST, DIMS, SELECTORS };
    Kind kind = JSON;
    Json j;
    Dims dims;
    size_t sel_count = 0;
    bool sel_outermost_only = false;

    static Val of(Json v) { Val x; x.j = std::move(v); return x; }
};

using ShapeOf = std::function<Dims(const std::string&)>;

/// Top-level scope (bare identifiers resolve against the task's own raw
/// fields) or a repeat-entry scope (bare identifiers resolve against the
/// current array entry, and `self` is the entry as a whole).
struct Scope {
    const Json* fields = nullptr;
    bool repeat = false;
    const Json* entry = nullptr;

    const Json* lookup(const std::string& name) const {
        if (repeat) {
            if (name == "self") return entry;
            if (!entry->is_object() || !entry->contains(name)) throw NotStatic("attribute not provided on repeat entry");
            return &entry->at(name);
        }
        if (!fields->contains(name)) throw NotStatic("attribute '" + name + "' not provided");
        return &fields->at(name);
    }
    bool provided(const std::string& name) const {
        if (repeat) {
            if (name == "self") return true;
            return entry->is_object() && entry->contains(name);
        }
        return fields->contains(name);
    }
};

inline Val resolve_path(const Node& node, const Scope& scope) {
    if (node.names[0] == "outermost") {
        if (node.names.size() != 1) throw NotStatic("outermost is not a container");
        Val v;
        v.kind = Val::OUTERMOST;
        return v;
    }
    const Json* value = scope.lookup(node.names[0]);
    for (size_t k = 1; k < node.names.size(); k++) {
        if (!value->is_object() || !value->contains(node.names[k])) throw NotStatic("attribute not provided");
        value = &value->at(node.names[k]);
    }
    return Val::of(*value);
}

inline bool is_provided(const Node& node, const Scope& scope) {
    if (node.type != Node::PATH) throw NotStatic("provided() needs a bare identifier or dotted path");
    if (node.names[0] == "outermost") return true;
    if (node.names.size() == 1) return scope.provided(node.names[0]);
    const Json* value = nullptr;
    try { value = scope.lookup(node.names[0]); } catch (const NotStatic&) { return false; }
    for (size_t k = 1; k + 1 < node.names.size(); k++) {
        if (!value->is_object() || !value->contains(node.names[k])) return false;
        value = &value->at(node.names[k]);
    }
    return value->is_object() && value->contains(node.names.back());
}

inline bool is_int_json(const Json& v) { return v.is_number() && !v.is_double(); }

inline Val fn_len(const Val& v) {
    if (v.kind == Val::DIMS) return Val::of(Json(static_cast<long long>(v.dims.size())));
    if (v.kind == Val::SELECTORS) return Val::of(Json(static_cast<long long>(v.sel_count)));
    if (v.kind != Val::JSON) throw NotStatic("len() needs a literal array, object, or Range-family value");
    const Json& j = v.j;
    if (j.is_array()) return Val::of(Json(static_cast<long long>(j.size())));
    if (j.is_object()) {
        if (j.contains("values")) {
            const Json& values = j.at("values");
            if (values.is_array()) return Val::of(Json(static_cast<long long>(values.size())));
            throw NotStatic("values is not a literal array");
        }
        if (j.contains("numberOfSteps")) {
            const Json& steps = j.at("numberOfSteps");
            if (steps.is_number()) {
                long long s = steps.is_double() ? static_cast<long long>(steps.as<double>())
                                                : steps.as<long long>();
                return Val::of(Json(s + 1));
            }
            throw NotStatic("numberOfSteps is not a literal number");
        }
        return Val::of(Json(static_cast<long long>(j.size())));
    }
    throw NotStatic("len() needs a literal array, object, or Range-family value");
}

inline bool val_truthy(const Val& v) {
    switch (v.kind) {
        case Val::JSON: return pyfmt::truthy(v.j);
        case Val::OUTERMOST: return true;
        case Val::DIMS: return !v.dims.empty();
        case Val::SELECTORS: return v.sel_count > 0;
    }
    return true;
}

inline Val apply_dim_minus(const Val& left, const Val& right) {
    if (left.kind != Val::DIMS) throw NotStatic("shapeOf(x) - dim(y) needs a resolved shape on the left");
    const Dims& dims = left.dims;
    size_t count = 1;
    bool outermost_only = false;
    if (right.kind == Val::SELECTORS) { count = right.sel_count; outermost_only = right.sel_outermost_only; }
    else if (right.kind == Val::JSON && right.j.is_array()) count = right.j.size();
    Val out;
    out.kind = Val::DIMS;
    {
        size_t known = 0;
        bool any_open = false;
        for (const auto& d : dims) { if (is_open(d)) any_open = true; else known++; }
        if (any_open) {
            // Whatever is removed, the unknown trailing dimensions may remain.
            if (outermost_only && known > 0) {
                out.dims.assign(dims.begin() + 1, dims.end());
                return out;
            }
            Dim unknown;
            unknown.source = std::string("runtime");
            out.dims.assign(known > count ? known - count : 0, unknown);
            for (const auto& d : dims) if (is_open(d)) out.dims.push_back(d);
            return out;
        }
    }
    if (count >= dims.size()) return out;
    if (outermost_only) {
        out.dims.assign(dims.begin() + 1, dims.end());
        return out;
    }
    Dim unknown;
    unknown.source = std::string("runtime");
    out.dims.assign(dims.size() - count, unknown);
    return out;
}

inline Val eval_expr(const Node& node, const Scope& scope, const ShapeOf& shape_of) {
    switch (node.type) {
        case Node::NUM:
            return Val::of(node.is_float ? Json(node.num) : Json(node.inum));
        case Node::BOOL:
            return Val::of(Json(node.bval));
        case Node::ARRAY: {
            Json arr = Json::array();
            for (const auto& item : node.kids) {
                Val v = eval_expr(*item, scope, shape_of);
                if (v.kind != Val::JSON) throw NotStatic("array literal item is not a plain value");
                arr.push_back(v.j);
            }
            return Val::of(arr);
        }
        case Node::PATH:
            return resolve_path(node, scope);
        case Node::NOT:
            return Val::of(Json(!val_truthy(eval_expr(*node.kids[0], scope, shape_of))));
        case Node::CALL: {
            const std::string& func = node.names[0];
            if (func == "provided") {
                if (node.kids.size() != 1) throw NotStatic("provided() takes exactly one argument");
                return Val::of(Json(is_provided(*node.kids[0], scope)));
            }
            if (node.kids.empty()) throw NotStatic(func + "() needs an argument");
            if (func == "len") return fn_len(eval_expr(*node.kids[0], scope, shape_of));
            if (func == "keys") {
                Val v = eval_expr(*node.kids[0], scope, shape_of);
                if (v.kind != Val::JSON || !v.j.is_object()) throw NotStatic("keys() needs a literal object");
                Json arr = Json::array();
                for (const auto& kv : v.j.object_range()) arr.push_back(std::string(kv.key()));
                return Val::of(arr);
            }
            if (func == "shapeOf") {
                Val ref = eval_expr(*node.kids[0], scope, shape_of);
                if (ref.kind != Val::JSON || !ref.j.is_string()) throw NotStatic("shapeOf() needs a reference-valued operand");
                std::string s = ref.j.as<std::string>();
                if (s.empty() || s[0] != '#') throw NotStatic("shapeOf() needs a reference-valued operand");
                Val out;
                out.kind = Val::DIMS;
                out.dims = shape_of(s);
                return out;
            }
            if (func == "dim") {
                if (node.kids.size() != 1) throw NotStatic("dim() takes exactly one argument");
                Val v = eval_expr(*node.kids[0], scope, shape_of);
                Val out;
                out.kind = Val::SELECTORS;
                if (v.kind == Val::OUTERMOST) { out.sel_count = 1; out.sel_outermost_only = true; return out; }
                if (v.kind == Val::JSON && v.j.is_string()) { out.sel_count = 1; return out; }
                if (v.kind == Val::JSON && v.j.is_array()) { out.sel_count = v.j.size(); return out; }
                throw NotStatic("dim() needs a name or a list of names");
            }
            throw NotStatic("unknown function " + func + "()");
        }
        case Node::BINOP: {
            const std::string& op = node.names[0];
            if (op == "or") {
                if (is_provided(*node.kids[0], scope)) return eval_expr(*node.kids[0], scope, shape_of);
                return eval_expr(*node.kids[1], scope, shape_of);
            }
            Val left = eval_expr(*node.kids[0], scope, shape_of);
            if (op == "-") {
                Val right = eval_expr(*node.kids[1], scope, shape_of);
                return apply_dim_minus(left, right);
            }
            Val right = eval_expr(*node.kids[1], scope, shape_of);
            if (op == "==") {
                auto is_ref = [](const Val& v) {
                    return v.kind == Val::JSON && v.j.is_string() && !v.j.template as<std::string>().empty()
                        && v.j.template as<std::string>()[0] == '#';
                };
                if (is_ref(left) || is_ref(right)) throw NotStatic("== operand is a reference");
                if (left.kind == Val::JSON && right.kind == Val::JSON) return Val::of(Json(pyfmt::equal(left.j, right.j)));
                return Val::of(Json(left.kind == Val::OUTERMOST && right.kind == Val::OUTERMOST));
            }
            if (op == "+") {
                if (left.kind == Val::JSON && right.kind == Val::JSON) {
                    if (left.j.is_array() && right.j.is_array()) {
                        Json arr = left.j;
                        for (const auto& e : right.j.array_range()) arr.push_back(e);
                        return Val::of(arr);
                    }
                    if (left.j.is_number() && right.j.is_number()) {
                        if (left.j.is_double() || right.j.is_double())
                            return Val::of(Json(left.j.as<double>() + right.j.as<double>()));
                        return Val::of(Json(left.j.as<long long>() + right.j.as<long long>()));
                    }
                }
                throw NotStatic("+ needs two arrays or two numbers");
            }
            throw NotStatic("unknown operator " + op);
        }
        case Node::COND: {
            if (val_truthy(eval_expr(*node.kids[0], scope, shape_of))) return eval_expr(*node.kids[1], scope, shape_of);
            return eval_expr(*node.kids[2], scope, shape_of);
        }
    }
    throw NotStatic("unknown AST node");
}

// ---- outputs.json "sourced" value resolution -----------------------------

inline std::optional<long long> json_source_min(const Json& sourced) {
    if (!sourced.is_object() || !sourced.contains("min")) return std::nullopt;
    const Json& m = sourced.at("min");
    if (!m.is_number()) return std::nullopt;
    return m.is_double() ? static_cast<long long>(m.as<double>()) : m.as<long long>();
}

inline std::optional<std::string> json_source_source(const Json& sourced) {
    if (!sourced.is_object() || !sourced.contains("source")) return std::nullopt;
    const Json& s = sourced.at("source");
    if (!s.is_string()) return std::nullopt;
    return s.as<std::string>();
}

inline std::optional<long long> eval_sourced_size(const Json* sourced, const Scope& scope, const ShapeOf& shape_of) {
    if (!sourced || sourced->is_null()) return std::nullopt;
    auto src = json_source_source(*sourced);
    if (!src || *src != "static") return std::nullopt;
    try {
        Val v = eval_expr(*parse_expr(sourced->at("expr").as<std::string>()), scope, shape_of);
        if (v.kind == Val::JSON && v.j.is_number()) {
            return v.j.is_double() ? static_cast<long long>(v.j.as<double>()) : v.j.as<long long>();
        }
    } catch (const NotStatic&) {
    }
    return std::nullopt;
}

inline std::vector<std::string> strings_of(const Json& arr) {
    std::vector<std::string> out;
    for (const auto& e : arr.array_range()) out.push_back(pyfmt::str(e));
    return out;
}

/// nullopt means "unresolvable" - JSON null ("no labels for this dimension")
/// is statically known as empty, so it returns an empty list instead.
inline std::optional<std::vector<std::string>> eval_sourced_labels(const Json* spec, const Scope& scope,
                                                                    const ShapeOf& shape_of) {
    if (!spec || spec->is_null()) return std::vector<std::string>{};
    if (spec->is_array()) return strings_of(*spec);
    if (spec->is_object()) {
        auto src = json_source_source(*spec);
        if (!src || *src != "static") return std::nullopt;
        try {
            Val v = eval_expr(*parse_expr(spec->at("expr").as<std::string>()), scope, shape_of);
            if (v.kind == Val::JSON && v.j.is_array()) {
                bool all_str = true;
                for (const auto& e : v.j.array_range()) if (!e.is_string()) all_str = false;
                if (all_str) return strings_of(v.j);
            }
        } catch (const NotStatic&) {
        }
        return std::nullopt;
    }
    return std::nullopt;
}

inline const Json* member(const Json& obj, const char* key) {
    if (!obj.is_object() || !obj.contains(key)) return nullptr;
    return &obj.at(key);
}

/// dims_spec is outputs.json's own "dimensions" value for one suffix entry:
/// either a fixed-length array of per-dimension entries, or a single "sourced"
/// object describing the whole shape. nullopt when the dimension COUNT itself
/// isn't statically known.
inline OptDims resolve_dims(const Json* dims_spec, const Scope& scope, const ShapeOf& shape_of) {
    if (!dims_spec || dims_spec->is_null()) return std::nullopt;
    if (dims_spec->is_array()) {
        Dims result;
        for (const auto& d : dims_spec->array_range()) {
            if (d.contains("trailing")) {
                Dim open;
                open.source = std::string("open");
                result.push_back(open);
            } else if (d.contains("repeat")) {
                const Json& rep = d.at("repeat");
                const Json* over_val = nullptr;
                try { over_val = scope.lookup(rep.at("over").as<std::string>()); }
                catch (const NotStatic&) { return std::nullopt; }
                if (!over_val->is_array()) return std::nullopt;
                for (const auto& item : over_val->array_range()) {
                    Scope item_scope;
                    item_scope.repeat = true;
                    item_scope.entry = &item;
                    Dim dim;
                    dim.size = eval_sourced_size(&rep.at("size"), item_scope, shape_of);
                    dim.labels = eval_sourced_labels(member(rep, "labels"), item_scope, shape_of);
                    dim.source = json_source_source(rep.at("size"));
                    dim.min = json_source_min(rep.at("size"));
                    result.push_back(dim);
                }
            } else {
                Dim dim;
                dim.size = eval_sourced_size(&d.at("size"), scope, shape_of);
                dim.labels = eval_sourced_labels(member(d, "labels"), scope, shape_of);
                dim.source = json_source_source(d.at("size"));
                dim.min = json_source_min(d.at("size"));
                result.push_back(dim);
            }
        }
        return result;
    }
    auto src = json_source_source(*dims_spec);
    if (!src || *src != "static") return std::nullopt;
    try {
        Val v = eval_expr(*parse_expr(dims_spec->at("expr").as<std::string>()), scope, shape_of);
        if (v.kind == Val::DIMS) return v.dims;
    } catch (const NotStatic&) {
    }
    return std::nullopt;
}

/// Splits a reference's index list into its brackets: "[0:2, 1][3]" is two
/// groups, [0:2, 1] and [3] (RefIndex::same_bracket marks an index that
/// continues the previous one's bracket).
inline std::vector<std::vector<RefIndex>> index_groups(const std::vector<RefIndex>& index_accessors) {
    std::vector<std::vector<RefIndex>> groups;
    for (const auto& idx : index_accessors) {
        if (idx.same_bracket && !groups.empty()) groups.back().push_back(idx);
        else groups.push_back({idx});
    }
    return groups;
}

/// The dimension a range index leaves behind: as many entries as the range
/// selects, with the matching labels. Whatever can't be told statically (a
/// runtime size, an out-of-bounds or empty range - the latter is
/// SEDBase-0011's to report) becomes unknown, so later indices are not
/// judged against a guess.
inline Dim sliced_dim(const Dim& dim, const RefIndex& idx) {
    Dim out;
    out.source = dim.source;
    if (!dim.size) return out;
    long long n = *dim.size;
    bool ok = !(idx.a && !(-n <= *idx.a && *idx.a <= n)) && !(idx.b && !(-n <= *idx.b && *idx.b <= n));
    long long ea = 0, eb = 0;
    if (ok) {
        ea = idx.a ? *idx.a : 0;
        eb = idx.b ? *idx.b : n;
        if (ea < 0) ea += n;
        if (eb < 0) eb += n;
        ok = ea < eb;
    }
    if (!ok) return out;
    out.size = eb - ea;
    // An unlabeled dimension is stored as an empty label list and stays that
    // way; otherwise the labels of the selected entries are kept.
    if (dim.labels && dim.labels->empty()) {
        out.labels = std::vector<std::string>();
    } else if (dim.labels && static_cast<long long>(dim.labels->size()) == n) {
        out.labels = std::vector<std::string>(dim.labels->begin() + ea, dim.labels->begin() + eb);
    }
    return out;
}

struct BoundIndices {
    OptDims seen;
    OptDims after;
};

/// Applies a reference's own bracket indices to a resolved dims list.
/// Separate brackets chain (each applies to the result of the one before:
/// "[0:2][1]" indexes the first dimension twice); the indices inside one
/// bracket apply to consecutive dimensions ("[0:2, 1]" - numpy style). A
/// positional/label index drops its dimension from the result; a range keeps
/// it, narrowed to the entries it selects; dimensions no index reaches pass
/// through untouched. `seen` has one entry per index, in order - the
/// dimension that index is applied to, as the earlier indices left it - and
/// stops short when an index finds no dimension left (SEDBase-0009); `after`
/// is the dimensions of the result. Both nullopt when dims is nullopt.
inline BoundIndices bind_indices(const OptDims& dims, const std::vector<RefIndex>& index_accessors) {
    BoundIndices out;
    if (!dims) return out;
    Dims view = *dims;
    Dims seen;
    for (const auto& group : index_groups(index_accessors)) {
        // An open placeholder (the last dimension) takes any number of indices.
        bool has_open = !view.empty() && is_open(view.back());
        size_t k = has_open ? group.size() : std::min(group.size(), view.size());
        for (size_t j = 0; j < k; j++) seen.push_back(j < view.size() ? view[j] : view.back());
        if (k < group.size()) break;
        Dims next;
        for (size_t j = 0; j < view.size(); j++) {
            if (j < k) {
                if (is_open(view[j])) next.push_back(view[j]);
                else if (group[j].is_range()) next.push_back(sliced_dim(view[j], group[j]));
            } else {
                next.push_back(view[j]);
            }
        }
        view = next;
    }
    out.seen = seen;
    out.after = view;
    return out;
}

inline OptDims apply_index_chain(const OptDims& dims, const std::vector<RefIndex>& index_accessors) {
    return bind_indices(dims, index_accessors).after;
}

/// A suffix entry that is listed in outputs.json is valid; one that isn't
/// listed is not (resolve_output handles that). An entry's optional "valid"
/// field is a boolean expr string over the task's own fields meaning "valid
/// if"; no "valid" field means always valid. nullopt when the expr couldn't
/// be evaluated statically.
inline std::optional<bool> eval_valid(const Json& entry, const Scope& scope, const ShapeOf& shape_of) {
    const Json* valid = member(entry, "valid");
    if (!valid) return true;
    if (valid->is_string()) {
        try {
            return val_truthy(eval_expr(*parse_expr(valid->as<std::string>()), scope, shape_of));
        } catch (const NotStatic&) {
            return std::nullopt;
        }
    }
    return false;
}

struct OutputResolution {
    std::optional<bool> ok;          // true / false / nullopt (not determinable)
    const Json* entry = nullptr;     // the raw outputEntry, or null
    OptDims dims_before;
    OptDims dims_after;
    std::optional<std::string> dot_name;
    std::vector<RefIndex> index_accessors;
};

/// The core hasSubvalue()-style resolution SEDBase-0008 through -0011/-0014/
/// -0015 and the ref-type rules all share. outputs_json is a concrete tasks/
/// class's own parsed outputs.json ({"outputs": {...}}); fields is the
/// referenced task's own JSON value; accessors is a ParsedReference's own
/// accessor list.
inline OutputResolution resolve_output(const Json& outputs_json, const Json& fields,
                                       const std::vector<Accessor>& accessors, const ShapeOf& shape_of) {
    OutputResolution r;
    for (const auto& acc : accessors) {
        if (acc.is_dot && !r.dot_name) r.dot_name = acc.name;
        else if (!acc.is_dot) r.index_accessors.push_back(acc.index);
    }
    std::string suffix_key = r.dot_name ? "[id]." + *r.dot_name : "[id]";
    const Json* outputs = member(outputs_json, "outputs");
    const Json* entry = outputs ? member(*outputs, suffix_key.c_str()) : nullptr;
    if (!entry) {
        r.ok = false;
        return r;
    }
    r.entry = entry;
    Scope scope;
    scope.fields = &fields;
    r.ok = eval_valid(*entry, scope, shape_of);
    if (r.ok != std::optional<bool>(true)) return r;
    r.dims_before = resolve_dims(member(*entry, "dimensions"), scope, shape_of);
    r.dims_after = apply_index_chain(r.dims_before, r.index_accessors);
    return r;
}

// ---- SEDBase-0012: indexing into a constant's own literal JSON value ------

/// A constant's literal value after (at most) one reference hop: a raw JSON
/// value, or - when the hop landed on a document element / nothing at all -
/// something with no JSON structure to index into.
struct Literal {
    enum Kind { JSON, ELEMENT, NONE };
    Kind kind = JSON;
    Json j;
    std::string element_repr;   // ELEMENT: how the value is rendered in a message
};

struct IndexResult {
    bool ok = true;
    std::string bad_subvalue;   // when !ok: str() of the failing index's value
    RefIndex bad_index;         // when !ok and the failure was an index: that index
    Literal value;
};

namespace detail {

inline bool fail(IndexResult& res, const RefIndex& idx) {
    res.ok = false;
    res.bad_subvalue = idx.value_str();
    res.bad_index = idx;
    return false;
}

/// One bracket's indices against a literal: the first applies to cur
/// itself, the rest to the corresponding dimension of what it selects (a
/// range selects several entries, so the rest applies inside each).
inline bool apply_bracket(const Json& cur, const std::vector<RefIndex>& group, size_t from, Json& out,
                          IndexResult& res) {
    if (from >= group.size()) { out = cur; return true; }
    const RefIndex& idx = group[from];
    if (idx.is_label()) {
        if (!cur.is_object() || !cur.contains(idx.sval)) return fail(res, idx);
        Json next = cur.at(idx.sval);
        return apply_bracket(next, group, from + 1, out, res);
    }
    if (idx.is_int()) {
        if (!cur.is_array()) return fail(res, idx);
        long long n = static_cast<long long>(cur.size());
        long long i = idx.ival;
        if (i < -n || i >= n) return fail(res, idx);
        if (i < 0) i += n;
        Json next = cur[static_cast<size_t>(i)];
        return apply_bracket(next, group, from + 1, out, res);
    }
    if (!cur.is_array()) return fail(res, idx);
    long long n = static_cast<long long>(cur.size());
    long long ea = idx.a ? *idx.a : 0;
    long long eb = idx.b ? *idx.b : n;
    if (ea < 0) ea += n;
    if (eb < 0) eb += n;
    if (ea < 0) ea = 0;
    if (eb < 0) eb = 0;
    if (eb > n) eb = n;
    Json arr = Json::array();
    for (long long k = ea; k < eb; k++) {
        Json el = cur[static_cast<size_t>(k)];
        if (from + 1 >= group.size()) {
            arr.push_back(el);
        } else {
            Json inner;
            if (!apply_bracket(el, group, from + 1, inner, res)) return false;
            arr.push_back(inner);
        }
    }
    out = arr;
    return true;
}

}  // namespace detail

inline IndexResult index_into_literal(const Literal& value, const std::vector<RefIndex>& index_accessors) {
    IndexResult res;
    res.value = value;
    if (value.kind != Literal::JSON) {
        if (!index_accessors.empty()) {
            res.ok = false;
            res.bad_subvalue = index_accessors[0].value_str();
            res.bad_index = index_accessors[0];
        }
        return res;
    }
    Json cur = value.j;
    for (const auto& group : index_groups(index_accessors)) {
        Json next;
        if (!detail::apply_bracket(cur, group, 0, next, res)) return res;
        cur = next;
    }
    res.value.j = cur;
    return res;
}

}  // namespace oshape
}  // namespace sed2test

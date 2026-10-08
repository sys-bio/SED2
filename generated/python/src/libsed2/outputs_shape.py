"""outputs.json expr/valid notation (core-spec.md Section 8) - parser,
evaluator, and shape/hasSubvalue() resolver, backing SEDBase-0008 through
-0015 (Design.md's Validation section) and the formulaic ref-type rules
that piggyback on SEDBase-0015's scalar-reduction check. GENERATED - do not
hand-edit; regenerate via generator/generate.py.

Design choice (documented, not silent): core-spec.md's own wording for this
notation is "the generator... compil[es] it into real code in each target
language... rather than shipping a small runtime interpreter". This module
IS a small runtime interpreter - a deliberate, narrower reading of that
sentence: the alternative (a bespoke Python function generated per
outputs.json suffix entry, one per concrete tasks/ class) would multiply
authorship effort by the number of suffix entries in the whole spec for no
behavioral difference, since walking a handful-of-nodes AST against an
in-memory dict costs nothing at validate() time. This mirrors the ONE other
precedent already in this codebase for a small expression language:
math_ast.py's ANTLR-generated grammar still gets walked by hand-written,
non-per-field interpretation code in the Types-0002/-0003/-0004 rule files,
not compiled into bespoke functions either. What core-spec.md's sentence
does rule out, and what this module doesn't do, is re-deriving the
notation's *grammar* independently per language - the notation itself is
parsed exactly once, right here, the same "one canonical definition" the
math grammar and the schema tree already get.
"""
from __future__ import annotations


class NotStatic(Exception):
    """Raised whenever an expr can't be evaluated against the target's own
    literal fields - a reference where a literal was needed, a missing
    attribute, an unresolvable shape dependency, a cycle/depth guard, and so
    on. Every caller catches this and treats it as "the rule does not fire"
    (SEDBase-0008 through -0011/-0014's own "only fires when computable"
    language) rather than as an error."""


# ---- lexer ------------------------------------------------------------

def _tokenize(text: str) -> list:
    toks = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        if ch == "=" and text[i:i + 2] == "==":
            toks.append(("==", "==")); i += 2; continue
        if ch in "+-!(),[].":
            toks.append((ch, ch)); i += 1; continue
        if ch.isdigit() or (ch == "." and i + 1 < n and text[i + 1].isdigit()):
            j = i
            while j < n and (text[j].isdigit() or text[j] == "."):
                j += 1
            toks.append(("NUMBER", text[i:j])); i = j; continue
        if ch.isalpha() or ch == "_":
            j = i
            while j < n and (text[j].isalnum() or text[j] == "_"):
                j += 1
            word = text[i:j]
            if word in ("true", "false"):
                toks.append(("BOOL", word))
            elif word in ("or", "if", "else"):
                toks.append((word, word))
            else:
                toks.append(("IDENT", word))
            i = j
            continue
        raise NotStatic(f"unexpected character {ch!r} in expr {text!r}")
    toks.append(("EOF", ""))
    return toks


# ---- AST ----------------------------------------------------------------

class Num:
    __slots__ = ("value",)
    def __init__(self, value): self.value = value

class Bool:
    __slots__ = ("value",)
    def __init__(self, value): self.value = value

class ArrayLit:
    __slots__ = ("items",)
    def __init__(self, items): self.items = items

class Path:
    __slots__ = ("names",)
    def __init__(self, names): self.names = names

class Call:
    __slots__ = ("func", "args")
    def __init__(self, func, args): self.func = func; self.args = args

class UnaryNot:
    __slots__ = ("operand",)
    def __init__(self, operand): self.operand = operand

class BinOp:
    __slots__ = ("op", "left", "right")
    def __init__(self, op, left, right): self.op = op; self.left = left; self.right = right

class Conditional:
    __slots__ = ("cond", "then", "orelse")
    def __init__(self, cond, then, orelse): self.cond = cond; self.then = then; self.orelse = orelse


_FUNCS = ("len", "keys", "shapeOf", "dim", "provided")


class _Parser:
    def __init__(self, toks):
        self.toks = toks
        self.i = 0

    def _peek(self):
        return self.toks[self.i]

    def _eat(self, kind):
        tok = self.toks[self.i]
        if tok[0] != kind:
            raise NotStatic(f"expected {kind}, got {tok}")
        self.i += 1
        return tok

    def parse(self):
        node = self._conditional()
        self._eat("EOF")
        return node

    def _conditional(self):
        node = self._or_expr()
        if self._peek()[0] == "if":
            self._eat("if")
            cond = self._or_expr()
            self._eat("else")
            orelse = self._conditional()
            return Conditional(cond, node, orelse)
        return node

    def _or_expr(self):
        node = self._equality()
        while self._peek()[0] == "or":
            self._eat("or")
            node = BinOp("or", node, self._equality())
        return node

    def _equality(self):
        node = self._additive()
        if self._peek()[0] == "==":
            self._eat("==")
            node = BinOp("==", node, self._additive())
        return node

    def _additive(self):
        node = self._unary()
        while self._peek()[0] in ("+", "-"):
            op = self._eat(self._peek()[0])[0]
            node = BinOp(op, node, self._unary())
        return node

    def _unary(self):
        if self._peek()[0] == "!":
            self._eat("!")
            return UnaryNot(self._unary())
        return self._primary()

    def _primary(self):
        kind, text = self._peek()
        if kind == "NUMBER":
            self._eat("NUMBER")
            return Num(float(text) if "." in text else int(text))
        if kind == "BOOL":
            self._eat("BOOL")
            return Bool(text == "true")
        if kind == "[":
            self._eat("[")
            items = []
            if self._peek()[0] != "]":
                items.append(self._conditional())
                while self._peek()[0] == ",":
                    self._eat(","); items.append(self._conditional())
            self._eat("]")
            return ArrayLit(items)
        if kind == "IDENT":
            name = self._eat("IDENT")[1]
            if self._peek()[0] == "(" and name in _FUNCS:
                self._eat("(")
                args = []
                if self._peek()[0] != ")":
                    args.append(self._conditional())
                    while self._peek()[0] == ",":
                        self._eat(","); args.append(self._conditional())
                self._eat(")")
                return Call(name, args)
            names = [name]
            while self._peek()[0] == ".":
                self._eat("."); names.append(self._eat("IDENT")[1])
            return Path(names)
        raise NotStatic(f"unexpected token {self._peek()} in expr")


_PARSE_CACHE: dict = {}


def parse_expr(text: str):
    node = _PARSE_CACHE.get(text)
    if node is None:
        node = _Parser(_tokenize(text)).parse()
        _PARSE_CACHE[text] = node
    return node


# ---- scopes -------------------------------------------------------------

class _OutermostSentinel:
    def __repr__(self): return "OUTERMOST"


OUTERMOST = _OutermostSentinel()


class Scope:
    """Top-level scope: bare identifiers resolve against a task's own raw
    JSON field values (SedBase._own_json_value()) - core-spec.md: "A bare
    identifier names one of the task's own attributes and evaluates to its
    value"."""
    __slots__ = ("fields",)
    def __init__(self, fields): self.fields = fields

    def lookup(self, name):
        if name not in self.fields:
            raise NotStatic(f"attribute {name!r} not provided")
        return self.fields[name]

    def provided(self, name):
        return name in self.fields


class RepeatScope:
    """core-spec.md's repeat-entry scoping: bare identifiers resolve against
    the CURRENT array entry's own fields, and `self` refers to the entry as
    a whole."""
    __slots__ = ("entry", "outer")
    def __init__(self, entry, outer): self.entry = entry; self.outer = outer

    def lookup(self, name):
        if name == "self":
            return self.entry
        if not isinstance(self.entry, dict) or name not in self.entry:
            raise NotStatic(f"attribute {name!r} not provided on repeat entry")
        return self.entry[name]

    def provided(self, name):
        if name == "self":
            return True
        return isinstance(self.entry, dict) and name in self.entry


# ---- evaluation -----------------------------------------------------------

def _is_ref_value(value):
    return isinstance(value, str) and value.startswith("#")


def _resolve_path(node, scope):
    if node.names[0] == "outermost":
        if len(node.names) != 1:
            raise NotStatic("outermost is not a container")
        return OUTERMOST
    value = scope.lookup(node.names[0])
    for seg in node.names[1:]:
        if not isinstance(value, dict) or seg not in value:
            raise NotStatic(f"attribute {'.'.join(node.names)!r} not provided")
        value = value[seg]
    return value


def _is_provided(node, scope):
    if not isinstance(node, Path):
        raise NotStatic("provided() needs a bare identifier or dotted path")
    if node.names[0] == "outermost":
        return True
    if len(node.names) == 1:
        return scope.provided(node.names[0])
    try:
        value = scope.lookup(node.names[0])
    except NotStatic:
        return False
    for seg in node.names[1:-1]:
        if not isinstance(value, dict) or seg not in value:
            return False
        value = value[seg]
    return isinstance(value, dict) and node.names[-1] in value


def _fn_len(value):
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        # Range-family dispatch (core-spec.md): len(x.values) if
        # provided(x.values) else x.numberOfSteps + 1 for NumericRange/
        # ParameterRange; just len(x.values) for a bare Range. Covered
        # generically by this shape-based dispatch rather than naming the
        # discriminator consts explicitly. Anything else object-shaped is a
        # plain SId-keyed map (outputVariableMap, aggregateOutputVariables,
        # CreateDataBlock.data) - len() there just means key count, the
        # same as keys(x)'s own array's length would be.
        if "values" in value:
            values = value["values"]
            if isinstance(values, list):
                return len(values)
            raise NotStatic("values is not a literal array")
        if "numberOfSteps" in value:
            steps = value["numberOfSteps"]
            if isinstance(steps, (int, float)) and not isinstance(steps, bool):
                return int(steps) + 1
            raise NotStatic("numberOfSteps is not a literal number")
        return len(value)
    raise NotStatic("len() needs a literal array, object, or Range-family value")


def _fn_keys(value):
    if not isinstance(value, dict):
        raise NotStatic("keys() needs a literal object")
    return list(value.keys())


def eval_expr(node, scope, shape_of):
    if isinstance(node, Num):
        return node.value
    if isinstance(node, Bool):
        return node.value
    if isinstance(node, ArrayLit):
        return [eval_expr(item, scope, shape_of) for item in node.items]
    if isinstance(node, Path):
        return _resolve_path(node, scope)
    if isinstance(node, UnaryNot):
        return not bool(eval_expr(node.operand, scope, shape_of))
    if isinstance(node, Call):
        if node.func == "provided":
            if len(node.args) != 1:
                raise NotStatic("provided() takes exactly one argument")
            return _is_provided(node.args[0], scope)
        if node.func == "len":
            return _fn_len(eval_expr(node.args[0], scope, shape_of))
        if node.func == "keys":
            return _fn_keys(eval_expr(node.args[0], scope, shape_of))
        if node.func == "shapeOf":
            ref = eval_expr(node.args[0], scope, shape_of)
            if not isinstance(ref, str) or not ref.startswith("#"):
                raise NotStatic("shapeOf() needs a reference-valued operand")
            return shape_of(ref)
        if node.func == "dim":
            if len(node.args) != 1:
                raise NotStatic("dim() takes exactly one argument")
            value = eval_expr(node.args[0], scope, shape_of)
            if value is OUTERMOST:
                return [OUTERMOST]
            if isinstance(value, str):
                return [value]
            if isinstance(value, list):
                return value
            raise NotStatic("dim() needs a name or a list of names")
        raise NotStatic(f"unknown function {node.func}()")
    if isinstance(node, BinOp):
        if node.op == "or":
            if _is_provided(node.left, scope):
                return eval_expr(node.left, scope, shape_of)
            return eval_expr(node.right, scope, shape_of)
        left = eval_expr(node.left, scope, shape_of)
        if node.op == "-":
            # The only place "-" appears: shapeOf(x) - dim(y). `left` is a
            # resolved dims list (or None); `right` is a list of dimension
            # selectors from dim(). Handled inline (rather than deferred, as
            # an earlier draft of this module did) since both operands are
            # fully evaluated by this point anyway.
            right = eval_expr(node.right, scope, shape_of)
            return _apply_dim_minus(left, right)
        right = eval_expr(node.right, scope, shape_of)
        if node.op == "==":
            # A reference-valued operand (for example outputModel given as
            # "#constants:flag") has no statically known value, so the
            # comparison is not statically evaluable.
            if _is_ref_value(left) or _is_ref_value(right):
                raise NotStatic("== operand is a reference")
            return left == right
        if node.op == "+":
            if isinstance(left, list) and isinstance(right, list):
                return left + right
            if isinstance(left, (int, float)) and not isinstance(left, bool) \
                    and isinstance(right, (int, float)) and not isinstance(right, bool):
                return left + right
            raise NotStatic("+ needs two arrays or two numbers")
        raise NotStatic(f"unknown operator {node.op}")
    if isinstance(node, Conditional):
        if bool(eval_expr(node.cond, scope, shape_of)):
            return eval_expr(node.then, scope, shape_of)
        return eval_expr(node.orelse, scope, shape_of)
    raise NotStatic(f"unknown AST node {node!r}")


def _apply_dim_minus(dims, selectors):
    """shapeOf(x) - dim(y): a dims list (see resolve_dims) with the
    dimension(s) named by `selectors` removed. This data model has no
    per-dimension naming beyond the reserved `outermost` sentinel (see this
    module's own docstring on dim()), so only that one case removes a
    SPECIFIC, still-fully-known dimension (the first); anything else can
    only shrink the known dimension COUNT, with the remaining dimensions'
    own details marked unknown rather than guessing which slot(s) a name
    like `appliedDimensions` was meant to select - safe (never mis-fires a
    downstream rule) even though it under-reports what SEDBase-0010/-0011
    could otherwise catch for those remaining dimensions."""
    if dims is None:
        return None
    count = len(selectors) if isinstance(selectors, list) else 1
    if any(is_open(d) for d in dims):
        # Whatever is removed, the unknown trailing dimensions may remain.
        known = [d for d in dims if not is_open(d)]
        if selectors == [OUTERMOST] and known:
            return dims[1:]
        return [{"size": None, "labels": None, "source": "runtime", "min": None}
                for _ in range(max(len(known) - count, 0))] + [d for d in dims if is_open(d)]
    if count >= len(dims):
        return []
    if selectors == [OUTERMOST]:
        return dims[1:]
    return [{"size": None, "labels": None, "source": "runtime", "min": None}
            for _ in range(len(dims) - count)]


# ---- outputs.json "sourced" value resolution -----------------------------

def _eval_sourced_size(sourced, scope, shape_of):
    if sourced is None:
        return None
    if sourced.get("source") != "static":
        return None  # runtime / input-file - not statically known
    try:
        value = eval_expr(parse_expr(sourced["expr"]), scope, shape_of)
    except NotStatic:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return int(value)
    return None


def _eval_sourced_labels(labels_spec, scope, shape_of):
    """None (JSON null) means "no labels for this dimension" - statically
    known as empty, not "unresolvable" - so this returns [] for that case,
    reserving None for a genuine failure to resolve."""
    if labels_spec is None:
        return []
    if isinstance(labels_spec, list):
        return labels_spec
    if isinstance(labels_spec, dict):
        if labels_spec.get("source") != "static":
            return None
        try:
            value = eval_expr(parse_expr(labels_spec["expr"]), scope, shape_of)
        except NotStatic:
            return None
        if isinstance(value, list) and all(isinstance(v, str) for v in value):
            return value
        return None
    return None


# The `source` of the placeholder dimension a "trailing" entry in outputs.json
# resolves to: zero or more further dimensions (those of the output's own
# entries), of unknown number, size and labels. Indices that reach it are not
# judged (it can take any number of them); it never makes the result "still
# shaped" (SEDBase-0015) on its own.
OPEN_SOURCE = "open"


def is_open(dim):
    return dim.get("source") == OPEN_SOURCE


def resolve_dims(dims_spec, scope, shape_of):
    """dims_spec is outputs.json's own "dimensions" value for one suffix
    entry (see schema/outputs-meta.schema.json's $defs/dimensions) - either
    a fixed-length array of per-dimension entries, or a single "sourced"
    object describing the whole shape. Returns a list of
    {"size": int|None, "labels": list[str]|None, "source": str, "min":
    int|None} - one per dimension, in order - or None when the dimension
    COUNT itself isn't statically known (a whole-shape runtime/input-file
    source, or a static expr that didn't evaluate to a resolved dims list)."""
    if dims_spec is None:
        return None
    if isinstance(dims_spec, list):
        result = []
        for d in dims_spec:
            if "trailing" in d:
                # The entries' own dimensions follow the listed ones: how many
                # there are is not statically known (see OPEN_SOURCE).
                result.append({"size": None, "labels": None, "source": OPEN_SOURCE, "min": None})
            elif "repeat" in d:
                rep = d["repeat"]
                try:
                    over_val = scope.lookup(rep["over"])
                except NotStatic:
                    return None
                if not isinstance(over_val, list):
                    return None
                for item in over_val:
                    item_scope = RepeatScope(item, scope)
                    result.append({
                        "size": _eval_sourced_size(rep["size"], item_scope, shape_of),
                        "labels": _eval_sourced_labels(rep.get("labels"), item_scope, shape_of),
                        "source": rep["size"].get("source"),
                        "min": rep["size"].get("min"),
                    })
            else:
                result.append({
                    "size": _eval_sourced_size(d["size"], scope, shape_of),
                    "labels": _eval_sourced_labels(d.get("labels"), scope, shape_of),
                    "source": d["size"].get("source"),
                    "min": d["size"].get("min"),
                })
        return result
    # single sourced object - the whole shape's derivation
    if dims_spec.get("source") != "static":
        return None  # runtime / input-file - dimension count itself unknown
    try:
        value = eval_expr(parse_expr(dims_spec["expr"]), scope, shape_of)
    except NotStatic:
        return None
    return value if isinstance(value, list) else None


def index_groups(index_accessors):
    """Splits a reference's index list into its brackets: "[0:2, 1][3]" is
    two groups, [0:2, 1] and [3] (RefIndex.same_bracket marks an index that
    continues the previous one's bracket)."""
    groups = []
    for idx in index_accessors:
        if getattr(idx, "same_bracket", False) and groups:
            groups[-1].append(idx)
        else:
            groups.append([idx])
    return groups


def _sliced_dim(dim, idx):
    """The dimension a range index leaves behind: as many entries as the
    range selects, with the matching labels. Whatever can't be told
    statically (a runtime size, an out-of-bounds or empty range - the
    latter is SEDBase-0011's to report) becomes unknown, so later indices
    are not judged against a guess."""
    n = dim["size"]
    a, b = idx.value
    out = dict(dim)
    out["min"] = None
    ok = n is not None and not (a is not None and not -n <= a <= n) and not (b is not None and not -n <= b <= n)
    if ok:
        ea = 0 if a is None else a
        eb = n if b is None else b
        if ea < 0:
            ea += n
        if eb < 0:
            eb += n
        ok = ea < eb
    if not ok:
        out["size"] = None
        out["labels"] = None
        return out
    out["size"] = eb - ea
    # An unlabeled dimension is stored as an empty label list and stays that
    # way; otherwise the labels of the selected entries are kept.
    labels = dim["labels"]
    if labels is not None and (not labels or len(labels) == n):
        out["labels"] = list(labels[ea:eb])
    else:
        out["labels"] = None
    return out


def bind_indices(dims, index_accessors):
    """Applies a reference's own bracket indices to a resolved dims list.
    Separate brackets chain (each applies to the result of the one before:
    "[0:2][1]" indexes the first dimension twice); the indices inside one
    bracket apply to consecutive dimensions ("[0:2, 1]" - numpy style). A
    positional/label index drops its dimension from the result; a range
    keeps it, narrowed to the entries it selects (core-spec.md's Grammar);
    dimensions no index reaches pass through untouched. Returns
    (seen, after): `seen` has one entry per index, in order - the dimension
    that index is applied to, as the earlier indices left it - and stops
    short when an index finds no dimension left (SEDBase-0009); `after` is
    the dimensions of the result. (None, None) when dims is None."""
    if dims is None:
        return None, None
    view = list(dims)
    seen = []
    for group in index_groups(index_accessors):
        # An open placeholder (the last dimension) takes any number of indices.
        has_open = bool(view) and is_open(view[-1])
        k = len(group) if has_open else min(len(group), len(view))
        seen.extend(view[j] if j < len(view) else view[-1] for j in range(k))
        if k < len(group):
            break
        new = []
        for j, d in enumerate(view):
            if j < k:
                if is_open(d):
                    new.append(d)
                elif group[j].kind == "range":
                    new.append(_sliced_dim(d, group[j]))
            else:
                new.append(d)
        view = new
    return seen, view


def _apply_index_chain(dims, index_accessors):
    return bind_indices(dims, index_accessors)[1]


def eval_valid(entry, scope, shape_of):
    """A suffix entry that is listed in outputs.json is valid; one that
    isn't listed is not (resolve_output handles that). An entry's optional
    "valid" field is a boolean expr string over the task's own fields
    meaning "valid if". No "valid" field: always valid. Returns True/False,
    or None when the expr couldn't be evaluated statically (SEDBase-0008:
    "the rule does not fire" in that case)."""
    valid = entry.get("valid")
    if valid is None:
        return True
    if isinstance(valid, str):
        try:
            return bool(eval_expr(parse_expr(valid), scope, shape_of))
        except NotStatic:
            return None
    return False


def resolve_output(outputs_json, fields, accessors, shape_of):
    """The core hasSubvalue()-style resolution SEDBase-0008 through -0011/
    -0014/-0015 and the ref-type rules all share. `outputs_json` is a
    concrete tasks/ class's own parsed outputs.json ({"outputs": {...}});
    `fields` is the referenced task's own _own_json_value() dict; `accessors`
    is a ParsedReference's own .accessors list. Returns (accessor_ok, entry,
    dims_before, dims_after, dot_name, index_accessors):
      - accessor_ok: True (the suffix is listed and has no "valid" field,
        or its "valid" ("valid if") expr evaluated true), False (suffix
        not listed, or its "valid" expr evaluated false), or None
        (couldn't be determined statically - every caller treats this the
        same as False for "don't fire a positive claim" but ALSO suppresses
        every rule that would need to know for sure, per the "only fires
        when computable" convention).
      - entry: the raw outputEntry dict, or None if the suffix key itself
        isn't present in outputs.json at all.
      - dims_before / dims_after: resolve_dims()'s own result, before and
        after applying the index chain (see _apply_index_chain) - both None
        whenever accessor_ok isn't True, or whenever entry has no
        "dimensions" at all (a "model"-typed suffix, which has no shape
        concept to index into in the first place).
      - dot_name: the first ('dot', name) accessor's name, or None for a
        bare [id] reference.
      - index_accessors: every ('index', RefIndex) accessor, in order,
        regardless of where it fell relative to a dot accessor.
    """
    dot_name = None
    index_accessors = []
    for kind, val in accessors:
        if kind == "dot" and dot_name is None:
            dot_name = val
        elif kind == "index":
            index_accessors.append(val)
    suffix_key = "[id]" if dot_name is None else f"[id].{dot_name}"
    entry = (outputs_json or {}).get("outputs", {}).get(suffix_key)
    if entry is None:
        return False, None, None, None, dot_name, index_accessors
    scope = Scope(fields)
    ok = eval_valid(entry, scope, shape_of)
    if ok is not True:
        return ok, entry, None, None, dot_name, index_accessors
    dims_before = resolve_dims(entry.get("dimensions"), scope, shape_of)
    dims_after = _apply_index_chain(dims_before, index_accessors)
    return True, entry, dims_before, dims_after, dot_name, index_accessors


# ---- SEDBase-0012: indexing into a constant's own literal JSON value ------

class NotIndexable(Exception):
    """Raised by index_into_literal when the index chain can't be applied
    to the constant's own literal structure - the signal SEDBase-0012
    fires on. args[0] is the failing index's value; .index is the RefIndex."""

    index = None


def _not_indexable(idx):
    err = NotIndexable(idx.value)
    err.index = idx
    return err


def _apply_bracket(cur, group):
    """One bracket's indices against a literal: the first applies to cur
    itself, the rest to the corresponding dimension of what it selects (a
    range selects several entries, so the rest applies inside each)."""
    if not group:
        return cur
    idx, rest = group[0], group[1:]
    if idx.kind == "label":
        if not isinstance(cur, dict) or idx.value not in cur:
            raise _not_indexable(idx)
        return _apply_bracket(cur[idx.value], rest)
    if idx.kind == "int":
        if not isinstance(cur, list):
            raise _not_indexable(idx)
        n = len(cur)
        i = idx.value
        if i < -n or i >= n:
            raise _not_indexable(idx)
        return _apply_bracket(cur[i], rest)
    if idx.kind == "range":
        if not isinstance(cur, list):
            raise _not_indexable(idx)
        a, b = idx.value
        n = len(cur)
        ea = a if a is not None else 0
        eb = b if b is not None else n
        if ea < 0: ea += n
        if eb < 0: eb += n
        part = cur[max(ea, 0):max(eb, 0)]
        if not rest:
            return part
        return [_apply_bracket(el, rest) for el in part]
    raise _not_indexable(idx)


def index_into_literal(value, index_accessors):
    """core-spec.md / SEDBase-0012.md: constants have no outputs.json,
    their "shape" is just their own literal JSON value. Applies an index
    chain directly against it: separate brackets chain (each applies to the
    result of the one before), the indices inside one bracket apply to
    consecutive dimensions (see index_groups). Callers pass an
    already-dereferenced `value` (the RUNTIME dispatcher follows alias
    constants first). Raises NotIndexable the moment an index can't apply;
    returns the fully-indexed literal value otherwise (used by the ref-type
    check too, once indexing succeeds)."""
    cur = value
    for group in index_groups(index_accessors):
        cur = _apply_bracket(cur, group)
    return cur

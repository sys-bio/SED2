"""ref-type fixture generator (Design.md's Testing and Test Generation and
Spec Evolution sections).

A `ref-type` rule is the formulaic "when the value of <field> is a reference,
it must be a reference to <type>" kind: the generator derives it straight from
the field's own declared type (NumberOrRef, BooleanOrRef, ...), so the fixtures
that exercise it are derivable too, and are regenerated every run rather than
hand-written.

Every fixture is a copy of one shared prefix - the same `constants` block plus
one `modelImport` task (`model1`) - with one more element added (a task or
output of whatever class owns the field under test) whose single field under
test references one of those constants, or the model. For each ref-type rule:

  * fail fixtures: a reference to a value of the wrong type (a wrong scalar,
    an array/AnnotatedData constant, a model, an out-of-range value for a
    bounded type, ...), each named for what is wrong;
  * pass twins: a reference to a correctly typed constant.

Unlike the schema-derivable tier (gen_fixtures.py), fail fixtures here are
written even if the generated library does not yet fire the rule - they are
ordinary tests that are expected to fail until the check is implemented. The
one thing this module does verify is the host document: a pass twin that does
not validate clean means the synthesized host is wrong, so that rule is
skipped (and reported) rather than shipped with a broken host. A fail fixture
that trips some *other* rule is dropped for the same reason.

The same machinery also covers SEDBase-0016 / SEDBase-0017 (a bare SIdRef field
marked x-ref-target must resolve to a model / to AnnotatedData), one group of
fixtures per marked field.

ASCII only, per Claude.md.
"""
from __future__ import annotations

import glob
import json
import os
import re
from typing import Optional

from .gen_fixtures import _Embedder
from .spec import Field, SpecModel

# The shared constants block - identical in every fixture this module writes.
CONSTANTS = {
    "mybool": True,
    "mynumber": 1.3,
    "myint": 5,
    "myzero": 0,
    "mynegint": -1,
    "mystring": "hello",
    "myNumberArray": [1.2, 2, 6.6],
    "myStringArray": ["how", "are", "you?"],
    "myobject": {"a": 1, "b": 2},
    "myStringObject": {"a": "x", "b": "y"},
}

MODEL_TASK_ID = "model1"
MODEL_TASK = {
    "_type": "modelImport",
    "location": "filename.xml",
    "language": "urn:sedml:language:sbml",
}
MODEL_REF = f"#tasks:{MODEL_TASK_ID}.model"
SIM_TASK_ID = "sim1"

# Required reference fields whose target must be a model (everything else that
# is required-and-a-reference is fed AnnotatedData).
MODEL_FIELDS = {"model", "inputModel"}


def _const(name: str) -> str:
    return f"#constants:{name}"


_REQUIRED_RE = re.compile(r"^The (\w+) attribute of an? (\w+) is required\.?$")


class _HostEmbedder(_Embedder):
    """_Embedder that synthesizes hosts whose *references* actually resolve
    (a model reference where a model is needed, an AnnotatedData constant
    elsewhere) and that also fills attributes a class's numbered rules call
    required even when the flattened field list does not mark them so."""

    def __init__(self, model: SpecModel):
        super().__init__(model)
        self.rule_required: dict[str, set] = {}
        for rid, r in model.rules.items():
            m = _REQUIRED_RE.match(r.rule)
            if m:
                self.rule_required.setdefault(m.group(2), set()).add(m.group(1))
        self.data_ref = _const("myNumberArray")
        self._in_progress: set = set()

    def minimal_json(self, class_name, overrides=None, omit=None):
        omit = omit or set()
        c = self.model.classes[class_name]
        must = self.rule_required.get(class_name, set())
        out = {}
        if c.has_type and c.type_const:
            out["_type"] = c.type_const
        for f in c.fields:
            if f.name in omit or not (f.required or f.name in must):
                continue
            val = self._minimal_field_value(f)
            if val is None:
                return None
            out[f.name] = val
        if overrides:
            out.update(overrides)
        return out

    def _minimal_field_value(self, f: Field):
        t = f.type
        if t.kind == "SIdRef":
            return MODEL_REF if f.name in MODEL_FIELDS else self.data_ref
        if getattr(t, "enum", None):
            return t.enum[0]
        if t.kind in ("dict", "array"):
            # A required container must not be empty (the library treats an
            # empty one as missing) - give it one minimally valid element.
            elem = self._one_element(t)
            if elem is not None:
                return {"e1": elem} if t.kind == "dict" else [elem]
        return super()._minimal_field_value(f)

    def _one_element(self, t):
        disc_name = t.item_discriminator or t.item_discriminator2
        if disc_name:
            if disc_name == "AbstractTask":
                return dict(MODEL_TASK)
            disc = self.model.discriminators.get(disc_name)
            if not disc or not disc.branches:
                return None
            for br in sorted(disc.branches.values(), key=lambda b: b.class_name):
                if br.class_name in self._in_progress:
                    continue
                self._in_progress.add(br.class_name)
                try:
                    return self.minimal_json(br.class_name)
                finally:
                    self._in_progress.discard(br.class_name)
            return None
        if t.item_class and t.item_class not in self._in_progress:
            self._in_progress.add(t.item_class)
            try:
                return self.minimal_json(t.item_class)
            finally:
                self._in_progress.discard(t.item_class)
        return None


# ---------------------------------------------------------------------------
# Classifying a ref-type rule's expected target

def _classify(field: Field, rule_text: str) -> Optional[dict]:
    """Returns {family, target, ...} describing what the reference must
    resolve to, or None if this module does not know the shape."""
    t = field.type
    kind = t.kind
    if kind in ("NumberOrRef", "IntegerOrRef"):
        integer = kind == "IntegerOrRef"
        bound = None
        if t.exclusive_minimum is not None and t.exclusive_minimum == 0:
            bound = "positive"
        elif t.minimum is not None and t.minimum == 0:
            bound = "non-negative"
        name = ("integer" if integer else "number")
        return {"family": "scalar", "target": name, "bound": bound}
    if kind == "BooleanOrRef":
        return {"family": "scalar", "target": "boolean", "bound": None}
    if kind == "StringOrRef":
        if t.enum:
            return {"family": "scalar", "target": "enum", "bound": None, "enum": list(t.enum)}
        return {"family": "scalar", "target": "string", "bound": None}
    if kind == "ArrayOrRef":
        low = rule_text.lower()
        if "array of strings" in low:
            item = "string"
        elif "array of numbers" in low or "numberorref" in low:
            item = "number"
        else:
            item = "any"
        return {"family": "array", "item": item}
    if kind == "DictOrRef":
        low = rule_text
        if "StringOrRef" in low:
            val = "string"
        elif "SIdRef" in low:
            val = "ref"
        else:
            val = "any"
        return {"family": "dict", "values": val}
    return None


def _cases(info: dict) -> tuple[list, list]:
    """(fail_cases, pass_cases), each a list of (test_name, reference_string,
    extra_constants). extra_constants is a dict added to the shared block for
    that one fixture only (used just for enum pass twins)."""
    fails, passes = [], []
    model = ("model-ref", MODEL_REF, None)
    fam = info["family"]
    if fam == "scalar":
        tgt, bound = info["target"], info["bound"]
        if tgt == "number":
            fails += [("string-constant", _const("mystring"), None),
                      ("bool-constant", _const("mybool"), None),
                      ("array-constant", _const("myNumberArray"), None)]
            if bound in ("positive", "non-negative"):
                fails.append(("out-of-range-constant",
                              _const("myzero" if bound == "positive" else "mynegint"), None))
            passes += [("correct-type", _const("mynumber"), None),
                       ("int-constant", _const("myint"), None)]
        elif tgt == "integer":
            fails += [("string-constant", _const("mystring"), None),
                      ("non-integer-constant", _const("mynumber"), None),
                      ("bool-constant", _const("mybool"), None),
                      ("array-constant", _const("myNumberArray"), None)]
            if bound in ("positive", "non-negative"):
                fails.append(("out-of-range-constant",
                              _const("myzero" if bound == "positive" else "mynegint"), None))
            passes.append(("correct-type", _const("myint"), None))
        elif tgt == "boolean":
            fails += [("number-constant", _const("mynumber"), None),
                      ("string-constant", _const("mystring"), None),
                      ("array-constant", _const("myNumberArray"), None)]
            passes.append(("correct-type", _const("mybool"), None))
        elif tgt == "string":
            fails += [("number-constant", _const("mynumber"), None),
                      ("bool-constant", _const("mybool"), None),
                      ("array-constant", _const("myStringArray"), None)]
            passes.append(("correct-type", _const("mystring"), None))
        elif tgt == "enum":
            enum = info["enum"]
            bad = "mystring" if "hello" not in enum else "mynumber"
            fails += [("non-member-constant", _const(bad), None),
                      ("number-constant", _const("mynumber"), None),
                      ("array-constant", _const("myStringArray"), None)]
            passes.append(("correct-type", _const("myenum"), {"myenum": enum[0]}))
        fails.append(model)
    elif fam == "array":
        item = info["item"]
        fails += [("scalar-constant", _const("mynumber"), None)]
        if item == "string":
            fails.append(("number-array-constant", _const("myNumberArray"), None))
            passes.append(("correct-type", _const("myStringArray"), None))
        elif item == "number":
            fails.append(("string-array-constant", _const("myStringArray"), None))
            passes.append(("correct-type", _const("myNumberArray"), None))
        else:
            fails.append(("object-constant", _const("myobject"), None))
            passes += [("number-array", _const("myNumberArray"), None),
                       ("string-array", _const("myStringArray"), None)]
        fails.append(model)
    elif fam == "dict":
        val = info["values"]
        fails += [("scalar-constant", _const("mynumber"), None),
                  ("array-constant", _const("myNumberArray"), None)]
        if val == "string":
            fails.append(("number-values-constant", _const("myobject"), None))
            passes.append(("correct-type", _const("myStringObject"), None))
        elif val == "any":
            passes.append(("correct-type", _const("myobject"), None))
        # val == "ref": no constant holds references to subTask outputs, so
        # there is no honest pass twin here (skipped, reported).
        fails.append(model)
    return fails, passes


# ---------------------------------------------------------------------------

def _point_loop_variables_at_subtasks(tasks: dict) -> None:
    """A LoopVariable's subsequentValues must reference one of its own Loop's
    subTasks (LoopVariable-0004); the host synthesizer only knows to make it a
    reference, and the Loop's id is assigned later, so fix it up here for every
    top-level task that has loopVariables and subTasks."""
    for task_id, task in tasks.items():
        if not isinstance(task, dict):
            continue
        lvs, subs = task.get("loopVariables"), task.get("subTasks")
        if isinstance(lvs, dict) and isinstance(subs, dict) and subs:
            target = f"#tasks:{task_id}:subTasks:{next(iter(subs))}.model"  # the host subTask is a modelImport
            for lv in lvs.values():
                if isinstance(lv, dict) and "subsequentValues" in lv:
                    lv["subsequentValues"] = target


def _assemble(doc: dict, constants: dict, extra_tasks: Optional[dict] = None) -> dict:
    """The document with the shared prefix added, in canonical key order:
    version, constants, tasks (model1 first, then any extras, then the
    fixture's own), then everything else."""
    out = {"version": doc.get("version", "v1.0.0"), "constants": dict(constants)}
    tasks = {MODEL_TASK_ID: dict(MODEL_TASK)}
    if extra_tasks:
        tasks.update(extra_tasks)
    tasks.update(doc.get("tasks", {}))
    _point_loop_variables_at_subtasks(tasks)
    out["tasks"] = tasks
    for k, v in doc.items():
        if k not in ("version", "constants", "tasks"):
            out[k] = v
    return out


def _slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", s) or "x"


def _uses_data_ref(node, data_ref) -> bool:
    if isinstance(node, dict):
        return any(_uses_data_ref(v, data_ref) for k, v in node.items() if k != "constants")
    if isinstance(node, list):
        return any(_uses_data_ref(v, data_ref) for v in node)
    return node == data_ref


def _sim_fed(doc: dict, data_ref: str, sim_task: dict) -> dict:
    """Copy of doc with every AnnotatedData constant reference replaced by a
    reference to a simulation task's output (bare `#tasks:sim1`, which
    ExplicitODESimulation's outputs.json declares as annotatedData), and that
    simulation added right after model1."""
    ref = f"#tasks:{SIM_TASK_ID}"

    def swap(node):
        if isinstance(node, dict):
            return {k: (v if k == "constants" else swap(v)) for k, v in node.items()}
        if isinstance(node, list):
            return [swap(v) for v in node]
        return ref if node == data_ref else node

    out = swap(doc)
    tasks = {MODEL_TASK_ID: out["tasks"][MODEL_TASK_ID], SIM_TASK_ID: dict(sim_task)}
    tasks.update({k: v for k, v in out["tasks"].items() if k != MODEL_TASK_ID})
    out["tasks"] = tasks
    return out


def generate_reftype_fixtures(model: SpecModel) -> dict:
    """Returns {rule_id: [candidate, ...]} where each candidate is
    {"host": "Class.field", "fixtures": {filename: document}} - one candidate
    per concrete class that carries the field, tried in name order by
    verify_and_write until one whose pass twin validates clean is found (some
    hosts, e.g. a Loop, need more than this module synthesizes)."""
    emb = _HostEmbedder(model)
    sim_task = emb.minimal_json("ExplicitODESimulation") if "ExplicitODESimulation" in model.classes else None
    rules: dict[str, list] = {}
    for cname in sorted(model.classes):
        c = model.classes[cname]
        if emb.path_to(cname) is None:
            continue
        for f in c.fields:
            rid = f.ref_type_rule_id
            if not rid or f.from_namespace:
                continue
            rule = model.rules.get(rid)
            if rule is None or rule.check != "ref-type":
                continue
            info = _classify(f, rule.rule)
            if info is None:
                rules.setdefault(rid, [])
                continue
            fails, passes = _cases(info)
            fx: dict[str, dict] = {}
            variants: dict[str, dict] = {}
            for tname, ref, extra in fails + passes:
                is_pass = (tname, ref, extra) in passes
                constants = dict(CONSTANTS)
                if extra:
                    constants.update(extra)
                emb._id_counter = 0  # deterministic ids: fixtures must not change between runs
                doc = emb.build_document(cname, leaf_overrides={f.name: ref})
                if doc is None:
                    fx = {}
                    break
                doc = _assemble(doc, constants)
                fx[f"{rid}-{'pass' if is_pass else 'fail'}-{'00' if is_pass else '01'}-{tname}.sed2.json"] = doc
                # Where the host takes AnnotatedData (curves, surfaces, ...),
                # also make a slightly more complicated variant of the first
                # fail case and the first pass twin, with that data coming
                # from a simulation's output instead of a constant.
                if sim_task is not None and ref != emb.data_ref and _uses_data_ref(doc, emb.data_ref) and (
                        (is_pass and (tname, ref, extra) == passes[0]) or
                        (not is_pass and (tname, ref, extra) == fails[0])):
                    vdoc = _sim_fed(doc, emb.data_ref, sim_task)
                    variants[f"{rid}-{'pass' if is_pass else 'fail'}-{'00' if is_pass else '01'}-{tname}-sim-fed.sed2.json"] = vdoc
            if fx:
                rules.setdefault(rid, []).append(
                    {"host": f"{cname}.{f.name}", "fixtures": fx, "variants": variants,
                     "has_pass": bool(passes)})

    # SEDBase-0016 / -0017: a bare SIdRef field marked x-ref-target must
    # resolve to a model / to AnnotatedData. One group per (declaring class,
    # field); one candidate per concrete class that carries it.
    sim_ref = f"#tasks:{SIM_TASK_ID}"
    target_cases = {
        # (rule, fails, passes); each case is (name, reference, needs_sim)
        "model": ("SEDBase-0016",
                  [("number-constant", _const("mynumber"), False),
                   ("array-constant", _const("myNumberArray"), False),
                   ("object-constant", _const("myobject"), False),
                   ("data-output", sim_ref, True)],
                  [("correct-type", MODEL_REF, False)]),
        "annotatedData": ("SEDBase-0017",
                          [("model-ref", MODEL_REF, False),
                           ("object-constant", _const("myobject"), False)],
                          [("array-constant", _const("myNumberArray"), False),
                           ("string-array-constant", _const("myStringArray"), False),
                           ("number-constant", _const("mynumber"), False),
                           ("string-constant", _const("mystring"), False),
                           ("data-output", sim_ref, True)]),
    }
    for cname in sorted(model.classes):
        c = model.classes[cname]
        if emb.path_to(cname) is None:
            continue
        for f in c.fields:
            if not f.ref_target or f.from_namespace or f.ref_target not in target_cases:
                continue
            rid, fails, passes = target_cases[f.ref_target]
            group = f"{rid}@{f.origin_class}.{f.name}"
            fx: dict[str, dict] = {}
            for is_pass, cases in ((False, fails), (True, passes)):
                for tname, ref, needs_sim in cases:
                    if needs_sim and sim_task is None:
                        continue
                    emb._id_counter = 0
                    doc = emb.build_document(cname, leaf_overrides={f.name: ref})
                    if doc is None:
                        fx = {}
                        break
                    doc = _assemble(doc, CONSTANTS, {SIM_TASK_ID: dict(sim_task)} if needs_sim else None)
                    kind = "pass" if is_pass else "fail"
                    fname = f"{rid}-{kind}-{'00' if is_pass else '01'}-{f.origin_class}-{f.name}-{tname}.sed2.json"
                    fx[fname] = doc
                if not fx:
                    break
            if fx:
                rules.setdefault(group, []).append(
                    {"host": f"{cname}.{f.name}", "fixtures": fx, "variants": {}, "has_pass": True})
    return rules


def verify_and_write(rules: dict, out_dir: str, python_pkg_root: str, package_name: str) -> dict:
    """Runs candidates through the generated Python library. For each rule
    picks the first host whose pass twin(s) validate clean (a host that does
    not is a bug in this module's synthesis, not something to ship). Fail
    fixtures that trip a rule other than the one they name are dropped and
    reported; fail fixtures that simply do not fire their own rule yet are
    KEPT - they are the tests the implementation is to be written against.
    Writes to out_dir/ref-type/, clearing that folder first (it is fully owned
    by this module)."""
    import importlib
    import sys as _sys

    src_dir = os.path.join(python_pkg_root, "src")
    added = src_dir not in _sys.path
    if added:
        _sys.path.insert(0, src_dir)
    for mod in list(_sys.modules):
        if mod == package_name or mod.startswith(package_name + "."):
            del _sys.modules[mod]
    pkg = importlib.import_module(package_name)

    def problems_of(doc_json):
        doc = pkg.read_from_string(json.dumps(doc_json))
        counts: dict[str, int] = {}
        for p in doc.validate():
            counts[p.rule_id] = counts.get(p.rule_id, 0) + 1
        return counts

    keep: dict[str, dict] = {}
    results: dict[str, str] = {}
    hosts: dict[str, str] = {}
    problems: dict[str, str] = {}
    try:
        for rid in sorted(rules):
            cands = rules[rid]
            if not cands:
                problems[rid] = "unknown field kind - no fixtures"
                continue
            chosen = None
            why_all = []
            for cand in cands:
                bad = None
                for fname, doc_json in cand["fixtures"].items():
                    if "-pass-" not in fname:
                        continue
                    try:
                        counts = problems_of(doc_json)
                    except Exception as e:  # noqa: BLE001
                        counts = {"<exception>": f"{type(e).__name__}: {e}"}
                    if counts:
                        bad = f"{cand['host']}: pass twin raised {counts}"
                        break
                if bad is None:
                    chosen = cand
                    break
                why_all.append(bad)
            if chosen is None:
                problems[rid] = "; ".join(why_all)[:300]
                continue
            hosts[rid] = chosen["host"]
            variants = chosen.get("variants") or {}
            vpass = [fn for fn in variants if "-pass-" in fn]
            v_ok = bool(variants)
            for fn in vpass:
                try:
                    vc = problems_of(variants[fn])
                except Exception as e:  # noqa: BLE001
                    vc = {"<exception>": f"{type(e).__name__}: {e}"}
                if vc:
                    v_ok = False
                    problems[fn] = f"variant skipped: pass twin raised {vc}"
            if v_ok:
                chosen = dict(chosen)
                chosen["fixtures"] = {**chosen["fixtures"], **variants}
            if not chosen["has_pass"]:
                problems[rid + "#pass"] = f"no pass twin possible ({chosen['host']}: no suitable constant)"
            for fname, doc_json in chosen["fixtures"].items():
                frid = fname.split("-pass-")[0].split("-fail-")[0]
                if "-pass-" in fname:
                    keep[fname] = doc_json
                    results[fname] = "pass-ok"
                    continue
                try:
                    counts = problems_of(doc_json)
                except Exception as e:  # noqa: BLE001
                    # validate() is specified never to throw (Design.md,
                    # Validation Results) - a crash is a library bug the
                    # fixture rightly exposes, so keep it.
                    keep[fname] = doc_json
                    results[fname] = "crashes"
                    problems[fname] = f"kept: validate() raised {type(e).__name__}: {e}"
                    continue
                extra = {k: v for k, v in counts.items() if k != frid}
                if extra:
                    problems[fname] = f"dropped: also fires {extra}"
                    continue
                keep[fname] = doc_json
                results[fname] = "fires" if counts.get(frid, 0) == 1 else "silent"
    finally:
        if added:
            _sys.path.remove(src_dir)

    target = os.path.join(out_dir, "ref-type")
    os.makedirs(target, exist_ok=True)
    for stale in glob.glob(os.path.join(target, "*.sed2.json")):
        os.remove(stale)
    for fname, doc_json in keep.items():
        with open(os.path.join(target, fname), "w") as fh:
            json.dump(doc_json, fh, indent=2)
            fh.write("\n")

    tally = {"pass-ok": 0, "fires": 0, "silent": 0, "crashes": 0}
    for r in results.values():
        tally[r] += 1
    print(f"[gen_reftype_fixtures] {len(hosts)}/{len(rules)} rules covered; wrote {len(keep)} fixture(s) to "
          f"{target}: {tally['pass-ok']} pass twins, {tally['fires']} fail fixtures already firing, "
          f"{tally['silent']} fail fixtures awaiting implementation, "
          f"{tally['crashes']} fail fixtures that crash validate()")
    for k, why in sorted(problems.items()):
        print(f"  - {k}: {why}")
    return {"hosts": hosts, "problems": problems, "results": results, "tally": tally, "written": len(keep)}

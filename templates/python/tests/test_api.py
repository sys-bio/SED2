"""Hand-written API tests for the library functions that are not validation
rules: an element's own id (get_id / is_set_id), the public reference API
(parse_reference / get_sed_reference), index and label accessors on
constants and literals (apply_indices / get_reference_value).

This file lives under templates/python/tests/ (hand-written, never
regenerated - see Design.md's Code Generation section) and is copied
verbatim to <out>/python/test_api.py by generator/emit_python.py, but only
for a spec tree that has the real SEDDocument classes (tasks, outputs,
constants): these tests use them directly. Its documents come from
fixtures/api/ (see the README there), found the same way test_fixtures.py
finds fixtures/ (SED2_FIXTURES_DIR overrides). The Java and C++ targets have
the same tests (ApiTest.java, ApiTest.cpp); keep the three in step.
"""
from __future__ import annotations

import importlib
import json
import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC_DIR = os.path.join(_HERE, "src")


def _generated_package_name() -> str:
    names = sorted(
        n for n in os.listdir(_SRC_DIR)
        if os.path.isdir(os.path.join(_SRC_DIR, n))
        and not n.startswith((".", "_"))
        and os.path.isfile(os.path.join(_SRC_DIR, n, "__init__.py"))
    )
    assert len(names) == 1, f"expected exactly one generated package under {_SRC_DIR}, found {names}"
    return names[0]


if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

t = importlib.import_module(_generated_package_name())
_functions = importlib.import_module(t.__name__ + "._predefined_functions")

FIXTURES_DIR = os.environ.get("SED2_FIXTURES_DIR", os.path.join(_HERE, "..", "..", "fixtures"))
DOC_PATH = os.path.join(FIXTURES_DIR, "api", "ids-and-references.doc.json")


@pytest.fixture
def doc():
    return t.read_from_file(DOC_PATH)


def test_api_document_is_valid(doc):
    assert doc.validate() == []


# ---- G-001: an element's own id --------------------------------------------

def test_id_of_top_level_tasks_and_outputs(doc):
    for task_id in doc.get_tasks():
        task = doc.get_tasks_item(task_id)
        assert task.is_set_id()
        assert task.get_id() == task_id
    assert doc.get_tasks() == ["m1", "sim1", "loop1"]
    assert doc.get_outputs() == ["rep1"]
    assert doc.get_outputs_item("rep1").get_id() == "rep1"


def test_id_of_nested_elements(doc):
    loop = doc.get_tasks_item("loop1")
    assert loop.get_sub_tasks() == ["s1", "s2"]
    for sub_id in loop.get_sub_tasks():
        sub = loop.get_sub_tasks_item(sub_id)
        assert sub.get_id() == sub_id
        assert sub.get_parent() is loop           # the owning element, not the collection
    assert loop.get_loop_variables_item("lv1").get_id() == "lv1"
    assert loop.get_aggregate_output_variables_item("a1").get_id() == "a1"


def test_top_level_parent_is_the_document_not_the_collection(doc):
    assert doc.get_tasks_item("m1").get_parent() is doc


def test_id_is_not_set_for_elements_outside_id_keyed_collections(doc):
    assert not doc.is_set_id()
    with pytest.raises(t.ApiError):
        doc.get_id()
    sim = doc.get_tasks_item("sim1")
    embedded = sim.get_independent_variable_range()          # a single embedded child
    assert not embedded.is_set_id()
    with pytest.raises(t.ApiError):
        embedded.get_id()


def test_id_of_created_element_follows_add_insert_rename_remove(doc):
    created = t.ModelImport()
    assert not created.is_set_id()
    with pytest.raises(t.ApiError):
        created.get_id()

    doc.add_tasks("m2", created)
    assert created.is_set_id()
    assert created.get_id() == "m2"

    other = t.ModelImport()
    doc.insert_tasks(0, "first", other)
    assert other.get_id() == "first"
    assert doc.get_tasks()[0] == "first"

    doc.set_id_on_tasks("m2", "m3")                           # a renamed id
    assert created.get_id() == "m3"
    assert doc.get_tasks_item("m3") is created

    doc.remove_tasks("m3")
    assert not created.is_set_id()
    with pytest.raises(t.ApiError):
        created.get_id()


def test_id_of_created_element_in_nested_collection(doc):
    loop = doc.get_tasks_item("loop1")
    created = t.ModelImport()
    loop.add_sub_tasks("s3", created)
    assert created.get_id() == "s3"
    loop.set_id_on_sub_tasks("s3", "s4")
    assert created.get_id() == "s4"


def test_id_of_renamed_existing_element(doc):
    sim = doc.get_tasks_item("sim1")
    doc.set_id_on_tasks("sim1", "sim_renamed")
    assert sim.get_id() == "sim_renamed"


def test_id_of_unregistered_namespace_task_holder():
    text = json.dumps({"version": "v1.0.0", "tasks": {"x1": {"_type": "acme@Thing", "foo": 1}}})
    d = t.read_from_string(text)
    holder = d.get_tasks_item("x1")
    assert holder.get_type() == "acme@Thing"
    assert holder.get_id() == "x1"


def test_id_is_not_part_of_the_serialized_document(doc):
    before = doc.to_json_value()
    for task_id in doc.get_tasks():
        doc.get_tasks_item(task_id).get_id()
    assert doc.to_json_value() == before


# ---- G-002(a): public reference parsing and resolution --------------------

def test_package_exports_the_reference_api():
    for name in ("ParsedReference", "RefIndex", "is_reference", "parse_reference", "get_sed_reference",
                 "apply_indices", "get_reference_value"):
        assert hasattr(t, name), name
        assert name in t.__all__, name
    assert t.is_reference("#tasks:a")
    assert not t.is_reference("tasks:a")
    assert not t.is_reference(5)


def test_parse_reference_path_and_dot_and_label():
    p = t.parse_reference("#tasks:loop1:subTasks:s1.model['S1']")
    assert isinstance(p, t.ParsedReference)
    assert p.raw == "#tasks:loop1:subTasks:s1.model['S1']"
    assert p.collection == "tasks"
    assert p.path == ["loop1", "subTasks", "s1"]
    assert p.accessors == [("dot", "model"), ("index", t.RefIndex("label", "S1"))]


@pytest.mark.parametrize("text, expected", [
    ("#constants:k_array[1]", [("index", t.RefIndex("int", 1))]),
    ("#constants:k_array[-1]", [("index", t.RefIndex("int", -1))]),
    ("#tasks:sim1[0:2]", [("index", t.RefIndex("range", (0, 2)))]),
    ("#tasks:sim1[:3]", [("index", t.RefIndex("range", (None, 3)))]),
    ("#tasks:sim1[2:]", [("index", t.RefIndex("range", (2, None)))]),
    ("#tasks:sim1[0][1]", [("index", t.RefIndex("int", 0)), ("index", t.RefIndex("int", 1))]),
    ("#tasks:sim1[0,1]", [("index", t.RefIndex("int", 0)), ("index", t.RefIndex("int", 1, same_bracket=True))]),
    ('#tasks:sim1["S1"]', [("index", t.RefIndex("label", "S1"))]),
    ("#tasks:sim1.range", [("dot", "range")]),
    ("#tasks:sim1.model[0]", [("dot", "model"), ("index", t.RefIndex("int", 0))]),
    ("#tasks:sim1", []),
])
def test_parse_reference_accessors(text, expected):
    p = t.parse_reference(text)
    assert p.collection == "tasks" or p.collection == "constants"
    assert p.path in (["sim1"], ["k_array"])
    assert p.accessors == expected


def test_parse_reference_is_lenient_and_never_raises():
    empty = t.parse_reference("#")
    assert (empty.collection, empty.path, empty.accessors) == (None, [], [])
    no_hash = t.parse_reference("tasks:sim1")                  # a leading '#' is optional
    assert (no_hash.collection, no_hash.path) == ("tasks", ["sim1"])
    unterminated = t.parse_reference("#tasks:sim1[")           # text after a failed accessor is ignored
    assert (unterminated.path, unterminated.accessors) == (["sim1"], [])
    partly = t.parse_reference("#tasks:sim1.model[1")
    assert partly.accessors == [("dot", "model")]
    assert t.parse_reference("#tasks:sim1.").accessors == []


@pytest.mark.parametrize("ref, task_id, prefix", [
    ("#tasks:m1", "m1", "#tasks:m1"),
    ("#tasks:sim1", "sim1", "#tasks:sim1"),
    ("#tasks:loop1:subTasks:s1", "s1", "#tasks:loop1:subTasks:s1"),
    ("#tasks:loop1:subTasks:s2", "s2", "#tasks:loop1:subTasks:s2"),
    ("#tasks:sim1.model['S1']", "sim1", "#tasks:sim1"),         # accessors are not applied
    ("#tasks:loop1:subTasks:s1[0][1]", "s1", "#tasks:loop1:subTasks:s1"),
])
def test_get_sed_reference_resolves_tasks(doc, ref, task_id, prefix):
    for form in (ref, t.parse_reference(ref)):                  # text or ParsedReference
        target, resolved = t.get_sed_reference(doc, form)
        assert target is not None
        assert target.get_id() == task_id
        assert resolved == prefix


def test_get_sed_reference_returns_the_element_itself(doc):
    target, _ = t.get_sed_reference(doc, "#tasks:loop1:subTasks:s1")
    assert target is doc.get_tasks_item("loop1").get_sub_tasks_item("s1")
    target, prefix = t.get_sed_reference(doc, "#outputs:rep1")   # resolves, though validate() forbids referencing it
    assert target is doc.get_outputs_item("rep1")
    assert prefix == "#outputs:rep1"


def test_get_sed_reference_resolves_constants_to_raw_values(doc):
    assert t.get_sed_reference(doc, "#constants:k_num") == (1.5, "#constants:k_num")
    assert t.get_sed_reference(doc, "#constants:k_strings") == (["a", "b"], "#constants:k_strings")
    # the index chain is parsed, not applied: the whole constant comes back
    assert t.get_sed_reference(doc, "#constants:k_strings[1]") == (["a", "b"], "#constants:k_strings")


@pytest.mark.parametrize("ref, prefix", [
    ("#tasks:nope", "#tasks"),
    ("#tasks", "#tasks"),
    ("#tasks:loop1:subTasks:nope", "#tasks:loop1"),
    ("#tasks:loop1:subTasks", "#tasks:loop1"),                  # a lone trailing segment is an attribute
    ("#tasks:loop1:nosuchcollection:s1", "#tasks:loop1"),
    ("#tasks:m1:subTasks:s1", "#tasks:m1"),                     # m1 has no sub-collections
    ("#constants:nope", "#constants"),
    ("#constants:k_num:x:y", "#constants:k_num"),               # a raw value has no children
    ("#outputs:nope", "#outputs"),
])
def test_get_sed_reference_unresolved_reports_longest_resolved_prefix(doc, ref, prefix):
    assert t.get_sed_reference(doc, ref) == (None, prefix)


def test_get_sed_reference_unrecognized_collection_or_no_document(doc):
    assert t.get_sed_reference(doc, "#bogus:x") == (None, None)
    assert t.get_sed_reference(doc, "#") == (None, None)
    assert t.get_sed_reference(None, "#tasks:m1") == (None, None)


# ---- G-002(b): index and label accessors on constants and literals --------

@pytest.mark.parametrize("value, accessors, expected", [
    ([10, 20, 30, 40], "[0]", 10),
    ([10, 20, 30, 40], "[3]", 40),
    ([10, 20, 30, 40], "[-1]", 40),
    ([10, 20, 30, 40], "[-4]", 10),
    ([10, 20, 30, 40], "[1:3]", [20, 30]),                  # end-exclusive, like Python
    ([10, 20, 30, 40], "[:2]", [10, 20]),
    ([10, 20, 30, 40], "[-2:]", [30, 40]),
    ([10, 20, 30, 40], "[:]", [10, 20, 30, 40]),
    ([10, 20, 30, 40], "[1:99]", [20, 30, 40]),             # a range clamps like a slice
    ([10, 20, 30, 40], "[3:1]", []),
    ({"S1": [1, 2, 3], "S2": [4, 5, 6]}, "['S2']", [4, 5, 6]),
    ({"S1": [1, 2, 3], "S2": [4, 5, 6]}, '["S1"][2]', 3),   # double quotes work too
    ({"S1": [1, 2, 3], "S2": [4, 5, 6]}, "['S2'][-2:]", [5, 6]),
    ({"a": {"b": 7}}, "['a']['b']", 7),
    ([[1, 2], [3, 4]], "[1][0]", 3),
    ([[1, 2], [3, 4]], "[0:2][1]", [3, 4]),                 # a range keeps its dimension; [1] then indexes it
    ([[1, 2], [3, 4]], "[0:2][0:1]", [[1, 2]]),
    # separate brackets chain (Python's x[a:b][c]); indices inside ONE bracket
    # apply to consecutive dimensions (numpy's x[a:b, c])
    ([[1, 2], [3, 4], [5, 6]], "[0:2][1]", [3, 4]),
    ([[1, 2], [3, 4], [5, 6]], "[0:2, 1]", [2, 4]),
    ([[1, 2], [3, 4], [5, 6]], "[1:3, 0]", [3, 5]),
    ([[1, 2], [3, 4], [5, 6]], "[:, 1]", [2, 4, 6]),
    ([[1, 2], [3, 4], [5, 6]], "[1, 0]", 3),
    ([[1, 2], [3, 4], [5, 6]], "[1, :]", [3, 4]),
    ([[1, 2], [3, 4], [5, 6]], "[0:2, 0:1]", [[1], [3]]),
    ([[1, 2], [3, 4], [5, 6]], "[0:2, 1][0]", 2),
    ([[1, 2], [3, 4], [5, 6]], "[0:2][1, 0]", 3),
    ([[1, 2], [3, 4], [5, 6]], "[0:3][1:3][1]", [5, 6]),
    ({"S1": [1, 2, 3], "S2": [4, 5, 6]}, "['S2', 1:]", [5, 6]),
    ([{"a": 1}, {"a": 2}], "[0:2, 'a']", [1, 2]),
    ([[1, 2], [3, 4]], "[2:2, 9]", []),                   # nothing selected: nothing to check further in
    ({"x": None}, "['x']", None),
    (5, "", 5),                                             # no indices: the value itself
    ("abc", "", "abc"),
])
def test_apply_indices_on_literals(value, accessors, expected):
    assert t.apply_indices(value, accessors) == expected


def test_apply_indices_accepts_text_parsed_reference_or_index_objects():
    value = {"S1": [1, 2, 3]}
    assert t.apply_indices(value, "['S1'][1]") == 2
    assert t.apply_indices(value, "#constants:anything['S1'][1]") == 2   # the containment path is ignored
    assert t.apply_indices(value, t.parse_reference("['S1'][1]")) == 2
    assert t.apply_indices(value, [t.RefIndex("label", "S1"), t.RefIndex("int", 1)]) == 2
    assert t.apply_indices(value, []) is value                            # no indices: the stored value itself


@pytest.mark.parametrize("value, accessors", [
    ([1, 2, 3], "[3]"),                  # past the end
    ([1, 2, 3], "[-4]"),                 # before the start
    ([1, 2, 3], "['S1']"),               # a label into a list
    ({"S1": 1}, "[0]"),                  # an int into a dict
    ({"S1": 1}, "[0:1]"),                # a range into a dict
    ({"S1": 1}, "['S2']"),               # a label the dict does not have
    (5, "[0]"),                          # any index into a scalar
    ("abc", "[0]"),                      # strings are scalars
    (None, "[0]"),
    ([1, 2, 3], "[0][0]"),               # the second index hits a scalar
    ([[1, 2], [3, 4]], "[0:2][2]"),      # chained: row 2 of a two-row slice
    ([[1, 2], [3, 4]], "[0:2, 2]"),      # comma: column 2 of two-column rows
    ([[1, 2], [3, 4]], "[0:2]['S1']"),   # a label into the slice, which is a list
    ([1, 2, 3], "[0, 0]"),               # the second index of a bracket hits a scalar
    ([[1, 2], [3, 4]], "[0:2, 0, 0]"),
])
def test_apply_indices_rejects_an_index_that_does_not_fit(value, accessors):
    with pytest.raises(t.ApiError, match="SEDBase-0012"):
        t.apply_indices(value, accessors)


def test_parse_reference_marks_the_indices_of_one_bracket():
    p = t.parse_reference("#tasks:sim1[0:2, 'S1'][1]")
    assert [(kind, idx.same_bracket) for kind, idx in p.accessors] == [
        ("index", False), ("index", True), ("index", False)]
    assert [idx.kind for _, idx in p.accessors] == ["range", "label", "int"]
    q = t.parse_reference("#tasks:sim1[0][1]")
    assert [idx.same_bracket for _, idx in q.accessors] == [False, False]


def test_apply_indices_rejects_dot_accessors():
    with pytest.raises(t.ApiError, match="SEDBase-0008"):
        t.apply_indices({"a": 1}, "['a'].model")
    with pytest.raises(t.ApiError, match="SEDBase-0008"):
        t.apply_indices({"a": 1}, ".model")


def test_apply_indices_error_names_the_failing_index():
    with pytest.raises(t.ApiError, match=r"\['S3'\]"):
        t.apply_indices({"S1": 1}, "['S3']")
    with pytest.raises(t.ApiError, match=r"\[7\]"):
        t.apply_indices([[1]], "[0][7]")


@pytest.mark.parametrize("ref, expected", [
    ("#constants:k_num", 1.5),
    ("#constants:k_strings", ["a", "b"]),
    ("#constants:k_strings[1]", "b"),
    ("#constants:k_strings[-2]", "a"),
    ("#constants:k_list[1:3]", [20, 30]),
    ("#constants:k_table['S1']", [1, 2, 3]),
    ("#constants:k_table['S2'][0]", 4),
    ("#constants:k_table['S2'][1:]", [5, 6]),
    ("#constants:k_alias", [4, 5, 6]),                     # a constant that is a reference is followed first
    ("#constants:k_alias[2]", 6),
    ("#constants:k_alias2", [4, 5, 6]),                    # ... through a chain of constants
    ("#constants:k_alias2[-1]", 6),
    ("#constants:k_none", None),
])
def test_get_reference_value_evaluates_constants(doc, ref, expected):
    assert t.get_reference_value(doc, ref) == expected
    assert t.get_reference_value(doc, t.parse_reference(ref)) == expected


@pytest.mark.parametrize("ref, rule", [
    ("#constants:nope", "SEDBase-0006"),
    ("#constants", "SEDBase-0006"),
    ("#constants:k_num:x:y", "SEDBase-0006"),              # a constant has no children
    ("#constants:k_num[0]", "SEDBase-0012"),               # index into a scalar
    ("#constants:k_list[4]", "SEDBase-0012"),
    ("#constants:k_list['S1']", "SEDBase-0012"),
    ("#constants:k_table[0]", "SEDBase-0012"),
    ("#constants:k_table['S3']", "SEDBase-0012"),
    ("#constants:k_alias[3]", "SEDBase-0012"),             # the index applies to the followed value
    ("#constants:k_table.model", "SEDBase-0008"),
])
def test_get_reference_value_reports_what_does_not_apply(doc, ref, rule):
    with pytest.raises(t.ApiError, match=rule):
        t.get_reference_value(doc, ref)


@pytest.mark.parametrize("ref", ["#tasks:m1", "#tasks:sim1.model", "#outputs:rep1", "#styles:x", "#bogus:x"])
def test_get_reference_value_only_constants_have_a_value_before_run_time(doc, ref):
    with pytest.raises(t.ApiError, match="does not name a constant"):
        t.get_reference_value(doc, ref)


def test_get_reference_value_without_a_document():
    with pytest.raises(t.ApiError, match="SEDBase-0006"):
        t.get_reference_value(None, "#constants:k_num")


def test_get_reference_value_rejects_a_circular_chain():
    d = t.SEDDocument()
    d.add_constants("a", "#constants:b")
    d.add_constants("b", "#constants:a")
    with pytest.raises(t.ApiError, match="circular"):
        t.get_reference_value(d, "#constants:a")


def test_get_reference_value_follows_a_constant_that_points_at_a_task_to_an_error(doc):
    d = t.SEDDocument()
    d.add_constants("a", "#tasks:m1")
    with pytest.raises(t.ApiError, match="does not name a constant"):
        t.get_reference_value(d, "#constants:a")


def test_get_reference_value_sees_api_edits(doc):
    doc.add_constants("fresh", [7, 8, 9])
    assert t.get_reference_value(doc, "#constants:fresh[-1]") == 9


def test_every_constant_reference_in_the_api_document_applies(doc):
    # what validate() accepts for a constant (SEDBase-0012) must also apply
    for ref in ("#constants:k_strings[0]", "#constants:k_table['S1'][2]", "#constants:k_alias[0:2]"):
        assert t.get_reference_value(doc, ref) is not None


# ---- G-004: generated headers name the real spec tree -----------------------

def test_generated_headers_name_the_real_spec_tree():
    for module in (t, importlib.import_module(t.__name__ + "._runtime"),
                   importlib.import_module(t.__name__ + ".model")):
        doc = module.__doc__
        assert "specsheets/" in doc and "test-specsheets" not in doc, module.__name__

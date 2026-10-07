# fixtures/api

Documents for the per-language API tests (Python `test_api.py`, Java
`ApiTest.java`, C++ `ApiTest.cpp`): the library functions that are not
validation rules (an element's own id, the public reference API, index and label
accessors on constants and literals). Not run by the rule-fixture harnesses: they only pick up
`*.sed2.json` files, and these are named `*.doc.json` on purpose.

Each document must validate with no problems in every target (the API tests
assert this).

| File | Used for |
|---|---|
| `ids-and-references.doc.json` | `get_id()` on top-level tasks, outputs and nested collections (a Loop's `subTasks`, `loopVariables`, `aggregateOutputVariables`); `parse_reference()` / `get_sed_reference()` against tasks, nested sub-tasks, outputs and constants; `apply_indices()` / `get_reference_value()` against the `k_list`, `k_table`, `k_alias`, `k_alias2` (a constant that refers to another) and `k_none` constants |

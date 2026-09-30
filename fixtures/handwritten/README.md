# fixtures/handwritten

Hand-authored document-level tests for the validation rules the JSON schema
pass cannot catch (the "semantic tier" - see ../../CreateTests.md for the plan
and Design.md, Test Generation). The ref-type rules are not here: they are
generated into ../generated/ref-type/ by generator/gen_reftype_fixtures.py.

Every file is run by all three targets (Python `test_fixtures.py`, Java
`FixtureTest.java`, C++ `FixtureTest.cpp`). Nothing here is language specific.

## Naming

    <rule-id>-<pass|fail>-<count>-<test>[-<rule-id-2>-<count-2>].sed2.json
    pass-<nn>-<test>.sed2.json                      (kit files, no single rule)

- `fail`: the named rule(s) must fire exactly `count` times and nothing else
  may fire. `pass`: the document must validate with no problems and round-trip
  (key order ignored, numbers compared by value).
- The optional chain suffix names a second rule the fixture deliberately also
  fires. The harnesses cannot tell a hyphenated test name from a chain, so in a
  chained file write the test name with underscores
  (`SEDBase-0006-fail-01-missing_task_in_scalar_field_no_ref_type.sed2.json`).
- A fail fixture has at least one pass twin (the same shape with the defect
  fixed). Count-2 fixtures exist where a rule can fire more than once.
- Schema must pass in every fixture; ASCII only; short ids (`sim1`, `m1`).
- `tools/check_fixture_coverage.py` lists rules without fixtures, unknown rule
  ids and convention breaks. Run it after adding or renumbering anything.

## The kit (pass-01 .. pass-06)

Minimal valid documents that the rest were built from. Shared vocabulary:

| Name | What it is |
|---|---|
| `m1` | `modelImport` (only `.model` is a valid accessor) |
| `sim1` | `explicitODESimulation`, `outputVariables ["S1","S2"]`, `numericRange` with `values [0,1,2,3]`: a 4 x 3 table, labels `["time","S1","S2"]` |
| `loop1`, `s1` | a `loop` with one loop variable and one subTask |
| `k_num`, `k_strings`, `k_array`, `k_obj`, `k_str` | constants: number 1.5, `["a","b"]`, `[10,20,30]`, `{"a":1,"b":2}`, `"hello"` |
| `r1`, `r2` ... | `relabelData` "holder" tasks: a place to put one reference under test (`input` is the reference, `labels` points at `#constants:k_strings`) |

## Status

Everything testable is covered; see `python3 tools/check_fixture_coverage.py`.
Blocked, recorded rather than faked:
- SEDDocument-0012 (duplicate keys): not implemented in v1.
- SEDBase-0014: no outputs.json declares a runtime dimension `min`.
- Plot-0008 (ref-type): rule text contradicts the schema; no fixtures.

## Decisions

Where a rule's text left a choice open, this is what the fixtures assume.
Tell the spec owner if any is wrong.

1. **Array elements and math strings count for SEDBase-0005.** The rule text
   says it applies to "an element of an array or object value, or a REFERENCE
   token embedded in a math string". Fixtures `SEDBase-0005-*-array-and-math`,
   `-array-element`, `-math-string` pin this. (Implemented in all three
   languages when these fixtures were written; before that only whole-attribute
   values and DictOrRef entries were checked.) Only SEDBase-0005 is applied to
   a reference inside a math string; its target is not resolved (no
   SEDBase-0006/-0007 there yet), and an array element gets the full reference
   dispatch with no per-element expected type.
2. **Math-string reference alone:** `1 + #foo:x` fires SEDBase-0005 once and
   Types-0001 does not fire (the lexer accepts any reference-shaped token).
3. **SEDBase-0008 is silent when its `valid` expression depends on a
   reference.** `outputModel: "#constants:k_bool"` on a steadyState means the
   accessor condition (`outputModel == true`) cannot be evaluated statically,
   so nothing fires (`SEDBase-0008-pass-00-conditional-accessor-depends-on-reference`).
   Previously the reference string itself was compared to `true`.
4. **SEDDocument-0013 fires for a constant that references anything that is not
   an earlier constant**, including a task (`#tasks:sim1`), itself, and a later
   or missing constant. Count is per offending constant.
5. **SEDDocument-0009 counts per use site**, not per prefix: two uses of one
   undeclared prefix give count 2 (`SEDDocument-0009-fail-02-same-prefix-used-twice`).
6. **SEDDocument-0011** fires for any version newer than the library supports
   (newer major, minor or patch), once per document.
7. **SEDBase-0011 indices are checked against the literal `values` length** of
   a `numericRange` (kit: 4 rows). The `numberOfSteps` vs `numberOfSteps + 1`
   question is avoided by using `values`; it is still open for the other range
   form.
8. **A missing task in a scalar field fires SEDBase-0006 only**; the ref-type
   rule for the field stays silent (`SEDBase-0006-fail-01-missing_task_in_scalar_field_no_ref_type`).
   Likewise a shaped target with too few indices fires SEDBase-0015 only
   (`SEDBase-0015-fail-01-shaped_target_in_scalar_field_no_ref_type`).
9. **A reference at or into an output fires SEDBase-0007, and SEDBase-0006 too
   when the output does not exist** (`SEDBase-0007-fail-01-output_that_does_not_exist-SEDBase-0006-01`).
10. **LoopVariable-0004 pass fixtures** point `subsequentValues` at the Loop's
    own subTask, a forward reference in file order that AbstractTask-0003 must
    not flag. A `subsequentValues` pointing into another loop's subTask also
    fires SEDBase-0013 (chained name).
11. **Types-0002..0004 fire once per offending node per attribute**, so a
    count-2 fixture needs two calculations (or two bad nodes).
12. `pow` is not a predefined function; use `rem` (arity 2) for arity tests.

## Known differences from the rule text (not failing anything)

- SEDBase-0006's `{subvalue}` holds the last prefix that resolved (for example
  `#tasks`), where the rule text says the longest prefix that failed to
  resolve (`#tasks:loop1:subTasks:sim9`). Fixtures check the rule id and count,
  not the message.
- SteadyState.model has no `x-rule-id`, and AggregationCalculation.input is
  typed `any`; both are schema questions for the spec owner.

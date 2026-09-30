# CreateTests.md - Plan for hand-authored semantic fixtures

Goal: write the document-level test files (`.sed2.json`) for every validation
rule that the JSON schema pass cannot catch, for the real spec (`specsheets/`).
These are the "semantic tier" described in Design.md under Test Generation and
Spec Evolution. Schema-derivable rules (required, type, enum, pattern) are
already covered by `fixtures/generated/` and are out of scope here.

## 1. Scope: which rules need hand-made fixtures

`generated/rules-v1.0.0.json` has 410 rules. Each has a `check` field:

| check | count | fixtures needed? |
|---|---|---|
| `schema` | 298 | No - `fixtures/generated/` (gen_fixtures.py) |
| `ref-type` | 87 | **Yes** - "if a reference, must resolve to type X" |
| `handwritten` | 25 | **Yes** - bespoke reference, scoping, ordering, namespace, math rules |

That is 112 rules. Two of the 25 cannot be tested today (Section 2). The 25
handwritten rules are authored by hand (blocks A-G, I); the 87 ref-type rules
are generated (block H).

Where the files go: `fixtures/handwritten/` (named in Design.md's Repository
Layout; README.md there holds the conventions and the running Decisions list).
No harness work is needed:
`generated/python/test_fixtures.py` globs `fixtures/**/*.sed2.json`, and the
`*-main` CI jobs pick up that folder automatically.

## 2. Rules that cannot be tested yet (record, do not fake)

- **SEDDocument-0012** (duplicate JSON keys): deliberately not implemented in v1
  in any language, so nothing can fire it. No fixture. (Design.md also bars
  chaining it onto other fixtures.)
- **SEDBase-0014** (warning: index may exceed a runtime dimension's `min`): no
  `outputs.json` under `specsheets/tasks/` declares a `min` on any runtime
  dimension, so no real class can trigger it. Options: (a) add a `min` to one
  outputs.json (e.g. Loop's runtime row dimension) - a spec change you would
  make; or (b) cover it only in `test-specsheets/`. Until then, skip it and
  keep it listed as "blocked" in the coverage report.
- Checks that need to read an external model or data file are not drafted (core-spec
  Section 10), so there are no rules to test.

## 3. Conventions (all blocks)

- Filename: `<rule-id>-<pass|fail>-<count>-<test>[-<rule-id-2>-<count-2>].sed2.json`.
  Examples: `SEDBase-0006-fail-01-missing-task.sed2.json`,
  `SEDBase-0006-pass-00-valid-subtask-ref.sed2.json`.
- **One rule per fail fixture.** It must fire only the rule(s) in its name. The
  harness fails on any unexpected extra rule, so this is enforced for us.
- `count` is how many times the rule fires. Include at least one count > 1
  fixture per rule where it makes sense (two bad references in one document).
- Warning-severity rules (SEDDocument-0010, -0011) are still `fail` fixtures.
- Each fail fixture gets at least one **pass twin**: the same shape with the one
  defect fixed. This is what catches false positives.
- Pass fixtures must round-trip exactly, key order included.
- Schema must pass in every fixture: valid `version`, all required attributes
  present, references shaped like `#...`. A fixture that trips the schema rule
  instead of the target rule is a bad fixture.
- ASCII only, per Claude.md. Use short IDs (`sim1`, `m1`, `k1`) so the reference
  under test is easy to spot.
- Chain (`-<rule>-<count>`) only for deliberate interaction fixtures (Section 6).
- Never chain SEDDocument-0012.

## 4. Step 0 - foundation (DONE)

Status: `fixtures/handwritten/README.md`, the six kit files (`pass-01-kit-*`)
and `tools/check_fixture_coverage.py` all exist. The coverage tool reports 25 of
27 handwritten rules covered (the other two are blocked, section 2) and 86 of 87
ref-type rules (Plot-0008 skipped), exit status 0. The original plan follows.

1. Create `fixtures/handwritten/` with a short `README.md` (conventions above
   plus a running "Decisions" list, Section 7).
2. Author the **kit**: a handful of minimal valid pass fixtures that every block
   copies from. Each is verified with pytest before anything is built on it.
   - `pass-01-kit-model-import`: one `modelImport` (needs `location`, `language`).
     Only `.model` is a valid accessor - ideal for accessor tests.
   - `pass-02-kit-explicit-ode`: `explicitODESimulation` (needs `model`,
     `independentVariable`, `outputVariables`, `independentVariableRange`),
     with a literal `outputVariables` list such as `["S1","S2"]`. Its output has
     static, labeled dimensions - ideal for index/label/range tests.
   - `pass-03-kit-loop`: a `loop` with `loopVariables` and a `subTasks` dict,
     plus an `outputVariableMap`. For scoping tests.
   - `pass-04-kit-calculation`: `calculation` with a literal `math`.
   - `pass-05-kit-report`: `report` referencing a task. For output-reference tests.
   - `pass-06-kit-constants`: constants of several JSON types (number, string,
     boolean, array, object, and one constant that is itself a reference).
3. `tools/check_fixture_coverage.py` (small, optional but recommended): reads
   `generated/rules-v1.0.0.json`, lists every non-schema rule with no fixture in
   `fixtures/handwritten/`, flags fixtures naming a rule ID that no longer
   exists (pre-release renumbering will cause this - Design.md), and flags names
   that break the convention. This is the progress tracker for everything below.

## 5. The blocks

Status: blocks A-G and I are authored and pass in Python, Java and C++
(`fixtures/handwritten/` holds 165 fixture files: the 6 kit files, 7 earlier
regression fixtures, 152 block fixtures; with `fixtures/generated/` the suite
is 782 tests per language). Block H is generated. The per-block lists below are
the original plan; the files themselves are the authority.

Grouped by what the rule is *about*, so that each block reuses one part of the
kit and one mental model. Each block is one sitting and one commit. Numbers are
rough file counts (fail + pass twins).

| Block | Theme | Rules | ~Files |
|---|---|---|---|
| A | Reference syntax and resolution | SEDBase-0005, -0006, -0007 | 10 |
| B | Accessors and indices on task outputs | SEDBase-0008, -0009, -0010, -0011, -0015 | 22 |
| C | Indexing into constants | SEDBase-0012 | 7 |
| D | Ordering and scoping | AbstractTask-0003, SEDDocument-0013, SEDBase-0013 | 16 |
| E | Repeat / Loop internals | Repeat-0008, -0009, -0010, LoopVariable-0004 | 12 |
| F | Namespaces and versions | SEDDocument-0009, -0010, -0011 | 9 |
| G | Math grammar | Types-0001, -0002, -0003, -0004 | 12 |
| H | ref-type: field must resolve to type X (generated) | 87 rules + SEDBase-0016/-0017 | 617 |
| I | Interactions (chained names) | mixed | 6 |

### Block A - Reference syntax and resolution
- **SEDBase-0005** (bad first segment): `#task:sim1` (typo), `#foo:x`. Count-2
  fixture with two bad roots in one array value. Pass: `#constants:k1`. Also try a
  reference token inside a `math` string (rule says these count) - watch for
  Types-0001 co-firing.
- **SEDBase-0006** (segment does not resolve): missing task key; missing subTask
  `#tasks:loop1:subTasks:sim9` where `loop1` exists (checks the "longest failing
  prefix" `{subvalue}`); a segment that names a plain attribute
  (`#tasks:sim1:model`). Pass: a valid deep reference from inside the Repeat.
- **SEDBase-0007** (target is an output): a task referencing `#outputs:rep1`; an
  output referencing another output; a reference to something contained in an
  output. Pass: output referencing a task.

### Block B - Accessors and indices on task outputs
Use `modelImport` for accessors and `explicitODESimulation` (labels =
`[independentVariable] + outputVariables`, so 2 dimensions) for indices.
- **SEDBase-0008**: bare `#tasks:m1` on a modelImport (empty `{subvalue}`);
  `.strings` on a simulation; an unknown accessor; any accessor on a constant;
  a conditionally-valid accessor whose `valid` expression evaluates false
  (Loop `.range` with no `range` set). Pass: `#tasks:m1.model`, and a case whose
  condition depends on a reference (must not fire).
- **SEDBase-0009** (too many indices): 3 indices on a 2-D target. Pass: exactly 2;
  indices on a runtime-dimension target (Loop `[id]`) never fire.
- **SEDBase-0010** (bad label): `['S3']` when `outputVariables` is `["S1","S2"]`
  (message lists allowed labels). Pass: `['S2']`; and `outputVariables` given as
  a reference (cannot fire).
- **SEDBase-0011** (index out of range): integer beyond size, negative beyond
  `-n`, range end beyond `n`, empty range. Pass on the boundaries: `-n`, `n-1`,
  range ending exactly at `n`. First confirm what `len(independentVariableRange)`
  is for the chosen range (Section 7).
- **SEDBase-0015** (still shaped): a scalar field (e.g. a NumberOrRef such as
  `relativeTolerance`) referencing a 2-D target with no index, with one index,
  and with a range index that keeps the dimension. Pass: fully indexed with
  positional or label indices. Confirm the ref-type rule does not double-fire.

### Block C - Indexing into constants
- **SEDBase-0012**: integer index past an array's length; label index into an
  array; missing key in an object; any index into a scalar constant. Pass: valid
  index; a constant that is itself a reference (followed first) with a valid and
  an invalid index.

### Block D - Ordering and scoping
- **AbstractTask-0003**: reference to a later task; a task referencing itself;
  a subTask referencing a later sibling. Passes: earlier task, any constant,
  earlier sibling subTask, a subTask using its enclosing Repeat's `.range`,
  `.index` or a loop variable.
- **SEDDocument-0013**: constant referencing a later constant; referencing a
  task; self-reference; count-2 case. Pass: earlier constant.
- **SEDBase-0013**: a top-level task, and separately an output, reaching into a
  Repeat's subTask, `.range`, `.index`, or loop variable; a sibling Repeat
  reaching in. Passes: subTask using its own Repeat's `.index`; a nested subTask
  using the outer Repeat's `.index`; outside code referencing `#tasks:loop1` or
  `.aggregates` (legal, governed by SEDBase-0008).

### Block E - Repeat / Loop internals
- **Repeat-0008**: `outputVariableMap` value pointing at a top-level task; at a
  constant. Pass: a subTask reference with accessor and index.
- **Repeat-0009**: an `aggregateOutputVariables` entry whose `input` is outside
  the Repeat. Pass: input is a subTask output.
- **Repeat-0010**: an aggregate entry defining `appliedDimensions`; count-2 with
  two entries. Pass: entries without it.
- **LoopVariable-0004**: `subsequentValues` pointing at a task outside the Loop.
  Pass: pointing at the Loop's own subTask - a forward reference in file order
  that AbstractTask-0003 must *not* flag (also make this a chained interaction
  pass in Block I).

### Block F - Namespaces and versions
- **SEDDocument-0009**: a `_type` or attribute key using `acme@...` with no
  `acme@version`; an unregistered prefix; two prefixes missing. Pass: declared.
- **SEDDocument-0010** (warning): `foo@version` declared and never used.
  Pass: declared and used.
- **SEDDocument-0011** (warning): `version` newer than the library supports
  (e.g. `v99.0.0`, still matching the schema pattern). Pass: `v1.0.0`.

### Block G - Math grammar
`Calculation.math` is the only math field in the real spec. Same four rules the
test-specsheets fixtures already cover against a synthetic class; this proves them on
the real one.
- **Types-0001** unparseable (`1 +`); **Types-0002** unknown function (`foo(1)`);
  **Types-0003** wrong arity (`sin(1, 2)`); **Types-0004** bare identifier
  (`x + 1`; must be a predefined constant such as `pi`).
- Passes: predefined constants and functions, `#reference` tokens (skipped by the
  math rules), and a `math` value that is itself a reference (skipped).

### Block H - ref-type rules (87) - GENERATED, not hand-written
Decision (status: done): these are derived from each field's declared type, so they are
generated by `generator/gen_reftype_fixtures.py` (called from `generate.py`,
regenerated every run) into `fixtures/generated/ref-type/`. Nothing in that
folder is hand-edited.

Every fixture is the same shared prefix - one `constants` block plus a
`modelImport` named `model1` - with one more task or output added whose single
field under test references something. The shared constants: `mybool`,
`mynumber` (1.3), `myint` (5), `myzero`, `mynegint`, `mystring`,
`myNumberArray`, `myStringArray`, `myobject`, `myStringObject` (plus a
one-off `myenum` in enum pass twins). Per rule:
- fail fixtures, one per kind of mistake: wrong scalar type, a boolean in a
  numeric field (an error, decided), an array/AnnotatedData constant, a model
  reference (`#tasks:model1.model`), an out-of-range constant for bounded
  types, a non-member for enums, wrong element type for arrays;
- pass twins: a correctly typed constant (numbers also get an int constant);
- for hosts that take AnnotatedData (curves, surfaces, plots, RelabelData), a
  `-sim-fed` variant of the first fail and pass with the data coming from a
  simulation's output instead of a constant.

These are ordinary tests, not xfail: the ones whose check is not implemented
yet simply fail until it is. The generator only verifies the host: a rule whose
pass twin does not validate clean is skipped and reported, and a fail fixture
that trips some other rule is dropped.

Status (run against the current generated Python library):
- 617 fixtures: 86 of the 87 ref-type rules (Plot-0008 skipped: its rule text contradicts
  the schema - see ProposedRules.md);
  plus 131 for the new SEDBase-0016/-0017 (one group per model or AnnotatedData
  field, 21 fields);
- 199 pass twins, all clean;
- 418 fail fixtures fire their rule in the Python library (array, dict,
  bounded-range, model-reference checks and SEDBase-0016/-0017 are all
  implemented there); none are silent, so all 617 pass;
- two NumericRange-0012 fixtures also fire Range-0002, because NumericRange
  re-declares Range's `values` and both classes' rules apply; they are named
  with the chain syntax (`...-scalar_constant-Range-0002-01`; underscores in the
  test name because the harness's file-name regex cannot tell a hyphenated name
  from the start of a chain);
- 0 crashes. (Earlier runs had 3 Repeat-0003 fixtures crash `validate()`; that was
  a real bug - a reference into `constants` from a Loop called `.get_parent()` on a
  bare value - now fixed in emit_python.py and pinned by four regression fixtures in
  `fixtures/handwritten/`, LoopVariable-0004 x2, Repeat-0008, Repeat-0009.)

### Block I - Interactions (chained names)
A few deliberate multi-rule fixtures, since Design.md's naming supports them:
- LoopVariable-0004 pass beside AbstractTask-0003 (forward reference allowed).
- A reference to a missing task in a scalar field: SEDBase-0006 fires and the
  ref-type rule for that field does not.
- A shaped target in a scalar field: SEDBase-0015 fires and the ref-type rule
  does not.
- Two different chained failures in one document with counts, e.g.
  `SEDBase-0006-fail-01-...-AbstractTask-0003-01`.

## 6. Working method (each block)

1. Copy the nearest kit fixture; break exactly one thing.
2. Name it by rule, `fail`, and expected count.
3. Run only that rule's fixtures:
   `pytest generated/python/test_fixtures.py -k "SEDBase-0006"`.
4. If an extra rule fires, fix the fixture (or log a rule ambiguity, Section 7).
5. Write the pass twin; confirm it round-trips.
6. Run the coverage script; commit the block.

## 7. Open questions to settle while authoring (answers logged in fixtures/handwritten/README.md)

Settled while authoring (see the README's Decisions list for the detail):
SEDDocument-0009 counts per use site; a reference in a math string fires
SEDBase-0005 alone (no Types-0001); a missing task or a shaped target in a
scalar field fires SEDBase-0006 / SEDBase-0015 only, not the ref-type rule.
Still open: what `len(independentVariableRange)` is for a `numericRange` given by
`numberOfSteps` (the fixtures use literal `values` to avoid it), and whether a
ref-type rule skips silently on a task-output target (current behaviour: yes).

Original list:
Where a rule's text does not pin down behavior, decide, record the decision, and
tell the spec owner. Known candidates:
- SEDDocument-0009: is the count per namespace prefix or per use site?
- SEDBase-0011: what is `len(independentVariableRange)` for a `numericRange`
  (`numberOfSteps` or `numberOfSteps + 1`)? Boundary fixtures depend on it.
- ref-type on a reference whose target is a task output: does it skip silently?
  (Rule text says `{resolved-value}` is omitted for runtime targets, implying
  yes.)
- Overlap of SEDBase-0006, -0015 and the ref-type rules on one bad reference
  (Block I fixes the intended behavior).
- SEDBase-0005 for references inside math strings: does it fire alone, or does
  Types-0001 also fire?

## 8. Suggested order and effort

Block H is already generated. For the handwritten rules: Step 0, then A, C, B,
D, E, F, G (the 23 testable handwritten rules, ~90 files, stable and
independent of individual field definitions), then I. Design.md defers
hand-authored semantic fixtures until the spec settles; the generated tier
regenerates with the spec, so it carries no such risk.

All three targets now implement the handwritten rules (`templates/<lang>/rules/`;
Types-0001..0004 live in each language's generated math-rules file instead).
These fixtures are language-independent and run against every target.

## 9. Decisions made

- Block H is generated, not hand-written (see Block H).
- A boolean constant in a numeric field is an error.
- A model reference where a number/boolean/string is expected is an error
  (existing ref-type rules cover it; the library does not check it yet).
- An array counts as AnnotatedData, no labels needed.
- A model field needs a model input, and a scalar constant counts as
  AnnotatedData: adopted as SEDBase-0016 and SEDBase-0017 (ProposedRules.md).

- Authoring the handwritten blocks found four places where the libraries did not
  match the rule text; all four were fixed in Python, Java and C++ and pinned by
  fixtures (README Decisions 1, 3, 4): SEDBase-0005 did not look inside array
  elements or math strings; SEDBase-0008 fired when its `valid` expression
  depended on a reference-valued field; SEDDocument-0013 ignored a constant that
  referenced a task.

## 10. Still open

- **SEDBase-0014**: add a `min` to one outputs.json so it becomes testable, or
  leave it blocked?
- Plot-0008 conflicts with the schema (see ProposedRules.md).
- The fixtures pin behaviour that the spec owner has not confirmed (README
  Decisions); when the spec changes, re-run the coverage tool and the three
  suites and fix the fixtures that name changed rules.
- References inside math strings are checked for SEDBase-0005 only; resolving
  them (SEDBase-0006/-0007) is not done.
- SEDBase-0006 `{subvalue}` reports the last resolved prefix, the rule text says
  the longest failing prefix.

## 11. TODO list

- Generate a NaN test: strict JSON (RFC 8259) has no NaN/Infinity literal, so a
  document cannot contain a raw NaN. Whether the string `"nan"` counts as a
  number is unsettled (Types says NaN/inf strings are valid numbers among
  numbers; you consider `"nan"` just a string). Revisit with a test that
  *produces* a NaN at run time rather than writing one in JSON.
- Python, Java and C++ all have the array/dict/bounded/model-target ref-type
  checks and the full reference/handwritten-rule validation; the CI jobs for
  Java and C++ against the real spec are now hard gates. A 17,253-document
  parity corpus (every fixture plus reference mutations, namespace, version,
  constants-order and math cases) gave identical rule, location, severity and
  message output in all three languages when this landed. The corpus lives
  outside the repo (it was built in scratch); rebuilding it is a script over
  the fixtures (see the parity note in section 11).
- Ref-type checks still deliberately loose: a DictOrRef fed a data output is
  not flagged (only a model is); a string-array field fed an annotatedData
  output is not flagged (labels may be strings); a number-array field fed a
  stringList output is.
- SEDBase-0016/-0017 are implemented in all three languages.
- Parity harness: turn the scratch differential-testing scripts (corpus builder,
  per-language dump programs, diff) into a checked-in tool, so regressions between
  languages are caught in CI rather than only by fixtures.
- test-specsheets/fixtures/constants.sed2.json is a junk file that fails in all
  three languages; remove or fix it.
- Style-target rules once `Style` is specified.
- Run `tools/check_fixture_coverage.py` in CI (it needs only Python and the
  checked-in rules JSON).

# SED2 Core Specification

This document describes the overall shape and design of a SED2 document. It is deliberately short: the detailed, per-class rules (attributes, types, outputs, UML diagram) now live in individual **Specification Sheets** under `specsheets/`, one per Task, Output, and supporting class, each versioned (`v1.0.0/`, and later `v1.0.1/`, etc.) so the spec can evolve without breaking documents or tools written against an earlier version.

## 1. What a SED2 document is

A SED2 document contains two main sections for describing a simulation experiment: **Tasks** and **Outputs**. Tasks define *how to do things*; Outputs define *how to report the results*. The document also holds predefined **constants** (centrally located so they can be referenced and changed in one place) and **styles** (presentation settings used by plots - still a placeholder, see below).

Full attribute list and UML: [`specsheets/core/SEDDocument/v1.0.0/`](specsheets/core/SEDDocument/v1.0.0/description.md)

```json
{
    "version": "v1.0.0",
    "constants": { "maxTime": 200, "pi": 3.14159 },
    "tasks": { "model1": {}, "sim1": {} },
    "outputs": { "plot1": {} },
    "styles": { "style1": {} }
}
```

## 2. Every element (`SEDBase`)

Every element in a SED2 document may optionally carry `name`, `description`, `notes` (markdown), and `annotations` (qualifier/value pairs). Most elements also have an implicit `id`, which is not a child field but the dictionary key under which the element appears in its parent collection.

Full detail: [`specsheets/core/SEDBase/v1.0.0/`](specsheets/core/SEDBase/v1.0.0/description.md)

## 3. The DAG design: inputs, outputs, and the chronological rule

Every SED2 element defines its inputs and outputs, so a document can be understood as a **Directed Acyclic Graph (DAG)**: Tasks and Outputs are nodes, and references between them (`#tasks:...`, `#constants:...`, etc.) are the edges.

**Chronological organization.** No Task nor Output may depend on input from a later Task. A conforming reader can therefore always execute a document correctly by walking `tasks` and then `outputs` in file order - while a more sophisticated interpreter may instead distribute independent Tasks across parallel workers by following the DAG's connected components. When a Repeat (`Scatter`/`Loop`/`ParameterScan`) defines child `subTasks`, those children follow the same internal ordering rule.

**Abstraction.** SED2 resembles a workflow language, but describes general, abstract tasks rather than specific implementations. Where a workflow language might run `ls -asF`, SED2 would describe a "list the contents of a directory" task with an input directory, a list-of-strings output, and parameters for whether to include sizes and file/directory type.

## 4. Types and references

Every value in a SED2 document is either a literal or a **reference** (an `SIdRef`) to a value elsewhere in the document - anywhere a `double` is expected, a string like `"#tasks:sim1.model['S1']"` may appear instead, and must be resolved to a double at execution time. 

The references point to task outputs.  Each task defines what the shape of its output or outputs are.  The three basic types of output references are:
* `[id]`: a number or block of numbers, in AnnotatedData format.
* `[id].model`: a model.
* `[id].strings`: a string or block of strings, in AnnotatedData format.

Other references may be defined by individual tasks, but every task must explicitly state which, if any, of the three basic references are valid, and, if so, what shape they take.

A full primitive/reference type catalogue: [`specsheets/core/Types/v1.0.0/`](specsheets/core/Types/v1.0.0/description.md)

## 5. Tasks

Every Task derives from `AbstractTask`, which itself derives from `SEDBase`: an implicit id plus a `_type` discriminator naming the concrete task class. Every concrete Task subclass must define what its output(s) are - see [`specsheets/core/SEDBase`](specsheets/core/SEDBase/v1.0.0/description.md) and each task's own Data Sheet under [`specsheets/tasks/`](specsheets/tasks/) for the details.


## 6. Outputs

Every Output derives from `AbstractOutput`, which itself derives from `SEDBase`. An `AbstractOutput` may **never** be used as input to anything else in the document - it is always the final stage of processing; anything that needs to be reused belongs in a Task instead. SED2 dictates only what data an output must contain, not the concrete form it takes (an in-memory object, a web page, exported files).

There are two basic families, documented under [`specsheets/outputs/`](specsheets/outputs/):

- **`Report`** - exports raw data.
- **`Plot`** - exports graphical output.

## 7. Namespaces

SED2 allows third parties to extend a document with their own attributes and classes under a **namespace**, written `namespace@identifier` (e.g. `saurolab@thisFactor` as an extra attribute, or `saurolab@thisAnalysis` as a whole new type). This applies at two levels:

- **Attribute-level**: an extra `namespace@key` field alongside an element's normal attributes.
- **Class-level**: a `_type` value of the form `namespace@identifier` naming an entirely new task or output type, not one of the built-in concrete classes.

A namespace a reader doesn't recognize should not be treated as an error: readers that don't know a given namespace store its content as opaque, unvalidated data and pass it through unchanged. A namespace that supplies its own schema can be validated against it by tools that know about it: known namespaces are composed directly into the schema at generate time, from a `namespaces/<prefix>/` directory.

A namespace also carries its own version, independent of the document's own `version` attribute. Any document that uses a given namespace anywhere must declare that namespace's version too, as a `<prefix>@version` attribute on the document itself (e.g. `saurolab@version`).

## 8. Data Sheet folder layout and versioning

```
specsheets/
  core/          - document-level & base-class infrastructure (not a Task or Output itself)
    Types/v1.0.0/
    SEDBase/v1.0.0/
    SEDDocument/v1.0.0/
    Style/v1.0.0/
  tasks/         - every class that can appear as a "tasks" dictionary entry, plus their shared abstract bases
    AbstractTask/v1.0.0/
    ModelImport/v1.0.0/
    ... (one folder per task class)
  outputs/       - every class that can appear as an "outputs" dictionary entry, plus their shared abstract bases
    AbstractOutput/v1.0.0/
    Report/v1.0.0/
    ...
  auxiliary/     - child/component types that are never themselves a "tasks" or "outputs" dictionary entry
    Range/v1.0.0/
    Axis/v1.0.0/
    Curve/v1.0.0/
    ...
```

Each `<Category>/<ClassName>/v1.0.0/` folder normally contains exactly:

- **`schema.json`** - a standalone JSON Schema (2020-12) for that one class, with its own `$id`. Shared primitives and base-class fields are pulled in via `$ref` to the relevant `core/`/`tasks/`/`outputs/`/`auxiliary/` schema file rather than duplicated, so the file stays small; it can still be dropped into another JSON Schema document and resolved as long as the relative folder layout above is preserved (or the `$id` is used with a schema-aware `$ref` resolver/registry).
- **`description.md`** - a link to the class's UML diagram (or a note that one doesn't exist yet), what the class does, a table of its child attributes (name, type, required/optional), and a description of what referencing the class's id produces as output.
- **`<ClassName>.png`** - the UML class diagram, when one exists (see Section 10 for gaps).

Every `schema.json`'s `required` array carries a sibling `x-required-rule-ids` object mapping each required field's name to the numbered validation rule that documents its presence requirement, and any property whose own constraint - a `_type` discriminator `const`, or a type/shape check beyond bare presence - has a matching numbered rule carries a sibling `x-rule-id` alongside that constraint (as a sibling of `$ref` where the property is declared that way); `x-rule-id` is a single rule-ID string, or an array of them when more than one rule governs the same property (most commonly an `OrRef` field's separate direct-value and reference-form rules, e.g. `AbstractODESimulation.forcePhysicalCorrectness`). Both are inert to any JSON Schema validator (unknown keywords are ignored) and exist purely as generator-only metadata - see Design.md's Validation section - so the generator can wire each hand-written `validate()` check straight to the schema location it corresponds to rather than re-deriving that mapping itself. Not every numbered rule has a schema-visible home this way: most are semantic (cross-reference resolution, math well-formedness, tolerance interactions, and the like) with no single JSON Schema keyword to attach to; only presence, discriminator, and simple type/shape constraints get one. A class whose own requiredness is disjunctive rather than a flat list - so far, only `Repeat`, whose subclasses need at least one of `outputVariableMap` or `aggregateOutputVariables` rather than a fixed set - expresses that as an `anyOf` of single-field `required` objects at the class's own top level (sibling to `properties`), with a sibling `x-anyof-required-rule-id` naming the one rule documenting the whole disjunction, rather than forcing it into `x-required-rule-ids`'s per-field mapping. A `oneOf` discriminator built via `x-generated-oneOf` (see Design.md's Classes section) can similarly carry a sibling `x-missing-type-rule-id`, naming a rule for the narrower case where `_type` is absent from the instance entirely, rather than present but unrecognized - a more specific error than the discriminator's own catch-all, for whichever discriminators want to distinguish it (e.g. `AbstractTask-0002`).

**Task output shapes (`outputs.json`).** Every concrete `tasks/` class (one with its own `_type`) additionally carries an `outputs.json`, machine-describing what each output suffix (`[id]`, `[id].model`, `[id].strings`, and any class-specific suffix like `Loop`'s `[id].aggregates`/`[id].range`/`[id].index`) resolves to - replacing the free-text "Valid"/"Invalid"/"Dimensions:" bullets that used to be the only record of this. Each suffix entry has a `valid` flag (`true`/`false`, or a boolean expression string over the task's own fields, e.g. `"outputModel == true"`, `"provided(range)"`), a `type` (`annotatedData`/`model`/`stringList`) when valid, and for `annotatedData` a `dimensions` list. Every place a size, a label set, or a whole shape needs stating, it's tagged with where that knowledge actually comes from - `"static"` (an `expr` computed from the task's own fields: `len(outputVariables)`, `independentVariableRange.numberOfSteps`, `keys(data)`, `[independentVariable] + outputVariables` as an array-literal-plus-concatenation, `shapeOf(input)` to inherit another reference's whole shape, optionally minus a dropped dimension via `- dim(...)`), `"input-file"` (knowable only by reading whatever external resource a field like `model` or `location` points to - `JacobianFull`'s species count, `CsvImport`'s column headers - tagged with `from`/`extract`/`note` rather than a formula, since the actual parsing is format-specific generator work, not something this file does itself), or `"runtime"` (genuinely not derivable without executing the simulation, e.g. `BoundedODESimulation`'s solver-chosen row count under variable step size, or `Loop`'s iteration count - always paired with a `note` explaining why). A `"runtime"` size may also carry an optional `min`, a guaranteed lower bound when one is actually known (e.g. "at least 2 rows"); an index or range that requires more entries than `min` guarantees is flagged by `SEDBase-0014` as a warning rather than an error, since it may still be valid once the simulation actually runs. `dimensions` itself is either a fixed array of per-dimension entries - an ordinary entry, or a `repeat` entry that expands to one dimension per entry of a named array-valued attribute (e.g. `ParameterScan`'s one dimension per entry of `parameterRanges`) - when the shape is decomposable dimension-by-dimension, or a single sourced object describing the whole shape's derivation, for the genuinely non-decomposable cases (`shapeOf(x)` whole-shape inheritance, or a `"runtime"`/`"input-file"` source where the dimension count itself isn't knowable ahead of time). `schema/outputs-meta.schema.json` validates every class's `outputs.json` envelope (the object shapes above); it does not parse `expr`/`note` string contents, which stay documentation for whoever implements the generator's shape-inference step. Abstract/mixin classes (`AbstractSimulation` and friends, `Repeat`) carry no `outputs.json` of their own, the same reasoning as why they carry no `_type` - nothing is ever instantiated as one directly, so "what does referencing this task's output produce" has no meaning until a concrete leaf class answers it, flatly, the same way those classes already flatten every other inherited constraint into their own `schema.json`.

**The `expr`/`valid` notation.** Both fields reuse one small expression language, evaluated against the task's own attribute values at generate/validate time - never against runtime data, and not the SED2 math grammar `Types-0001` through `Types-0004` validate (see this section's `x-rule-id` paragraph above and `Design.md`'s Math section for that separate grammar): `outputs.json` describes shape, `math` describes computation. A bare identifier names one of the task's own attributes and evaluates to its value (`outputVariables`); a dotted path reaches into a nested attribute the same way (`independentVariableRange.numberOfSteps`). `[x]` is an array literal (`[independentVariable]`); JSON numbers and `true`/`false` are literals too. Five functions: `len(x)` - the length of an array-valued `x`; or, when `x` is a Range-family value (a `RangeInline`/`NumericRangeInline`/`ParameterRangeInline`-typed field, or the reserved identifier `self` inside a `repeat` entry - see below), the number of points it resolves to, dispatched on `x`'s own discriminated type: `len(x.values) if provided(x.values) else x.numberOfSteps + 1` for `NumericRange`/`ParameterRange`, or just `len(x.values)` for a bare `Range` (which has no `numberOfSteps` alternative); `keys(x)` - the keys of an object-valued `x`, as an array; `shapeOf(x)` - the whole `dimensions` shape of a referenced AnnotatedData value; `dim(x)` - the dimension(s) named by `x` (a single name or a list of names) within a shape, meaningful only as the right operand of `-`; `provided(x)` - `true` iff attribute `x` was given a value in the document. Operators, at ordinary precedence: `!x` (boolean negation); `x == y` (equality); `x + y` (numeric addition when both operands are numbers, array concatenation when both are arrays - `1 + len(outputVariables)` vs. `[independentVariable] + outputVariables`); `shapeOf(x) - dim(y)` (a shape with the named dimension(s) removed - the only place `-` appears); `x or y` (`x`'s value when `provided(x)` holds, else the literal `y` - used for a field with a documented default, e.g. `dim(appliedDimensions or outermost)`, where `outermost` is a sentinel meaning the shape's own first dimension); and a conditional `x if provided(y) else z` for a value with two different derivations depending on whether an alternate field was given instead (e.g. `NumericRange`'s `len(values) if provided(values) else numberOfSteps + 1`). This is the only formal definition of the notation - `schema/outputs-meta.schema.json` does not parse it, as noted above - so a generator's shape-inference step implements it by hand. Inside a `dimensions` array's `repeat` entry (see above), this same notation applies to that entry's own `size`/`labels`, with two scoping additions: a bare identifier there resolves against the current array entry's own fields, not the task's top-level attributes; and the reserved identifier `self` refers to the current entry as a whole (for taking its `len()`, per above) rather than one of its fields. `ParameterScan`'s `repeat` over `parameterRanges` uses `size: len(self)`, letting each entry's own type (`Range`/`NumericRange`/`ParameterRange`) determine its own length the same way `Scatter`'s `len(range)` and `ExplicitODESimulation`'s `len(independentVariableRange)` do for their own named Range-family fields.

**Exception - the four Range/Span "inline" wrappers.** `Range`, `NumericRange`, `ParameterRange`, and `Span` can each be used two ways: standalone, as an entry in the `tasks` dictionary (with the full task apparatus - the `_type` discriminator, `taskParameters`, etc.), or embedded as a named child field of another task (e.g. `ExplicitODESimulation.independentVariableRange`, `BoundedODESimulation.independentVariableSpan`, `Scatter.range`, `ParameterScan.parameterRanges[]`). The schema represents the second, embedded form with four small wrapper `$defs` - `RangeInline`, `NumericRangeInline`, `ParameterRangeInline`, `SpanInline` - that exist purely to give the embedded-child usage its own schema seam (so it could diverge from the standalone-task form later) without being a distinct modeled *class* with its own UML diagram. Rather than give each of those four its own folder, they are merged into their base class's folder as extra schema files:

```
tasks/Range/v1.0.0/                  tasks/NumericRange/v1.0.0/             tasks/ParameterRange/v1.0.0/        tasks/Span/v1.0.0/
  schema.json   (Range)              schema.json   (NumericRange)          schema.json   (ParameterRange)      schema.json   (Span)
  common.schema.json (RangeCommon)   common.schema.json (NumericRangeCommon)
  inline.schema.json (RangeInline)   inline.schema.json (NumericRangeInline) inline.schema.json (ParameterRangeInline) inline.schema.json (SpanInline)
  Range.png                          NumericRange.png                       ParameterRange.png                  Span.png
  description.md                     description.md                        description.md                      description.md
```

`Range` and `NumericRange` carry an extra `common.schema.json` that `ParameterRange` and `Span` don't need: `Range` is both directly instantiable and the parent of `NumericRange`, and `NumericRange` is in turn both directly instantiable and the parent of `ParameterRange` - so each contributes a `RangeCommon`/`NumericRangeCommon` mixin (composed via `allOf`) carrying the fields its subclass inherits, alongside its own `schema.json` for the standalone-task form. `ParameterRange` and `Span` are leaves - nothing subclasses them - so they need no such split. Each mixin composes the next one up in turn (`NumericRangeCommon` composes `RangeCommon`, which composes `AbstractTaskCommon`), so a concrete class's own `allOf` names only its one most specific ancestor mixin - `ParameterRange` lists just `NumericRangeCommon`, not `RangeCommon` and `NumericRangeCommon` side by side - mirroring the UML chain directly rather than flattening every ancestor into each leaf; see `Design.md`'s Classes section for why.

Each `description.md` in these four folders explains all of that folder's schema files. Everything else in the document - including every cross-reference into these four classes from other Data Sheets' `schema.json` files - still resolves correctly; this was verified by validating real SED2 example documents against the split schemas after the merge. All four live under `tasks/` rather than `auxiliary/`, so each also carries the ordinary `outputs.json` every concrete `tasks/` class does - `Range`, `NumericRange`, and `ParameterRange` describe their `[id]` output for when they're used as a standalone `tasks` entry, and `Span`'s marks every suffix invalid, matching its own `description.md` (`Span` can never be a standalone `tasks` entry, only ever an embedded child, so it has no output of its own).

**Exception - the two `*Common` mixins.** `AbstractTaskCommon` and `AbstractOutputCommon` are schema-only mixins (composed via `allOf`) rather than modeled classes with their own UML box: they contribute the fields every concrete Task (or Output) picks up beyond `SEDBase` - `taskParameters`/`outputParameters` - but have no `_type` of their own and are never instantiated directly. Rather than give them placeholder folders, each is merged into its family's base-class folder as a second schema file:

```
tasks/AbstractTask/v1.0.0/              outputs/AbstractOutput/v1.0.0/
  schema.json      (AbstractTask)     schema.json      (AbstractOutput)
  common.schema.json (AbstractTaskCommon) common.schema.json (AbstractOutputCommon)
  AbstractTask.png                    AbstractOutput.png
  description.md                      description.md
```

`schema.json` in each of these two folders still holds only the `oneOf` discriminator over the concrete subclasses, unchanged; `common.schema.json` holds the mixin, and every concrete Task/Output's own `schema.json` still `$ref`s the mixin the same way it always did - just pointed at `common.schema.json` instead of a dropped standalone folder. Re-validated the same way as the Range/Span merge above. This `oneOf` is generator-populated rather than hand-maintained: each discriminator-bearing `$defs` entry (`AbstractTask`, `AbstractOutput`, and `RangeInline` - see the exception above) carries a structured pointer at the `common.schema.json` mixin it discriminates over, and the generator finds every concrete class that composes that same mixin and pins a `_type` const, treating each as a branch - so a newly-introduced abstract-class family needs no generator code changes, just its own mixin file and pointer. See `Design.md`'s Classes section for the full algorithm.

**Exception - standalone schema-only mixins with no oneOf of their own.** `AbstractSimulation`, `AbstractODESimulation`, and `AbstractStochasticSimulation` (all under `tasks/`) are schema-only mixins too, but unlike `AbstractTaskCommon`/`AbstractOutputCommon` above, nothing else ever needs to reference them as a field type, so there's no bare oneOf-bearing sibling to merge them into. Each simply gets its own ordinary-looking folder (`schema.json` + `description.md` + `<ClassName>.png`) whose `schema.json` holds a mixin instead of a concrete class - no `_type`, no `oneOf`, composed via `allOf` by its subclasses like any other mixin. `AbstractSimulation` provides the fields shared by every ODE/stochastic simulation task (superseding the former `SimulationCommon` - see Section 10); `AbstractODESimulation` and `AbstractStochasticSimulation` each add solver-tuning fields on top of it, composing `AbstractSimulation` via `allOf` in turn. `ExplicitODESimulation`/`BoundedODESimulation`/`OneStepODESimulation` and their three stochastic counterparts then each compose only their own one most-specific mixin (`AbstractODESimulation` or `AbstractStochasticSimulation`), which already reaches `AbstractSimulation`, `AbstractTaskCommon`, and `SEDBaseFields` transitively - mirroring the UML inheritance chain directly rather than flattening every ancestor's composition at the leaf (see Classes). `WorkingAlgorithm` (`auxiliary/WorkingAlgorithm/v1.0.0/`, referenced from `AbstractSimulation.workingAlgorithms`) needs no such exception - it's an ordinary directly-instantiable class inheriting only from `SEDBase`, following the general folder pattern above.

Any future changes to a class creates a sibling `v#.#.#/` folder alongside `v1.0.0/`, leaving existing references to `v1.0.0/` intact.

## 9. Validating a document against these schemas

To validate a whole SED2 document, `$ref` the appropriate `specsheets/core/SEDDocument/v1.0.0/schema.json` (which itself only needs `AbstractTask`/`AbstractOutput`, which in turn enumerate the concrete task/output classes) with a schema registry that can resolve relative file `$ref`s - e.g. Python's `referencing`/`jsonschema` packages, pointed at the `specsheets/` root. To validate or compose against just one class (e.g. embedding `ExplicitODESimulation`'s schema inside a larger tool-specific document), `$ref` that class's own `specsheets/tasks/ExplicitODESimulation/v1.0.0/schema.json` directly - its external refs resolve the same way.

## 10. Known gaps and inconsistencies (flagged, not fixed here)

Per the project's own working rule, this split is descriptive - it surfaces inconsistencies for you to resolve rather than silently deciding them:

- **`Style` is unspecified.** Both the prose (`"[To be filled in; should be a straight copy of SED-ML's Style class.]"`) and the schema (a permissive `{"type": "object"}` placeholder) mark this as incomplete.
- **9 classes have no standalone UML diagram of their own**, and instead their `description.md` links directly to another class's diagram (a relative-path image reference, not a copied file) rather than claiming no diagram exists. 6 of these are fully drawn inside the referenced diagram as a linked box with their own attributes: `auxiliary/Annotation` (in `core/SEDBase`'s diagram), `auxiliary/TaskParameter` (in `tasks/AbstractTask`'s), `auxiliary/OutputParameter` (in `outputs/AbstractOutput`'s), `auxiliary/LoopVariable` (in `tasks/Loop`'s), `auxiliary/Axis` (in `outputs/Plot`'s), and `auxiliary/WorkingAlgorithm` (in `tasks/AbstractSimulation`'s). The other 3 don't have a separately-cropped diagram of their own: `tasks/NumericRange` and `tasks/ParameterRange` just point to `tasks/Range`'s diagram, since inheriting from `Range` is all there is to show, and `auxiliary/Curve` points to `auxiliary/AbstractCurve`'s diagram, which already draws `Curve` directly as `AbstractCurve`'s one concrete subclass. (`tasks/Span` used to be in this list too, reusing `BoundedODESimulation`'s diagram, but now has its own standalone diagram.)
- **`core/Style` is the one class with genuinely no UML diagram anywhere**, as it does not yet have a full definition. It keeps its `DIAGRAM-PENDING.md` for now.
- **`tasks/AbstractTaskCommon` and `outputs/AbstractOutputCommon` are schema-only mixins, not modeled classes** - they were never drawn as their own UML box (their fields are drawn flattened onto `AbstractTask`'s/`AbstractOutput`'s own box instead), so there's no gap to flag for them; see Section 8's exception for how they're now filed as a second schema file (`common.schema.json`) in their base class's folder.
- **`sed\spec\sed2.schema.json` (in the `sed` repo/folder) is corrupted** - it has a complete, valid JSON document followed by ~1,140 bytes of duplicated trailing content that makes the file as a whole invalid JSON. This split was generated from the *valid prefix* of that file (which is also the more complete of the two `sed2.schema.json` copies found - `SED2\spec\sed2.schema.json` is missing the `Surface` definition and part of `Curve`). Worth cleaning up that file directly.
- **`Jacobian`'s worked example** repeats the `_type` key four times with different, mutually exclusive values in the same JSON object - a copy/paste artifact that should be cleaned up in the prose. (The schema-level ambiguity this reflected is now resolved: `Jacobian` has been split into `JacobianFull`/`JacobianReduced`, each with its own `_type` and no `isFull` flag - but the `description.md` prose still needs its own cleanup to match.)
- **`CSVImport`'s prose section is an unfinished sentence** ("All of the other arguments are optional,"), while the schema fully specifies `organization`/`separator`/`headers`/`columnNames`/`ncols`/`nrows`/`units`. The Data Sheet leans on the schema; the prose should be filled in to match.
- **`AggregationCalculation` and `DrawFromDistribution` are expected to be split into one concrete class per variant, the way `Jacobian` was split into `JacobianFull`/`JacobianReduced`.** Neither currently has a clean way to select or parameterize its variant: `AggregationCalculation` dropped its `kisaoID` attribute (rolled into `_type`, see Section 8) without gaining a replacement, so nothing in its schema says which KISAO:0000824 aggregation function (sum, mean, standard deviation, ...) is actually being computed. `DrawFromDistribution` has a `distribution` attribute naming which of the 12 SBML distrib functions to draw from, but `arguments` is still a flat, unlabeled array - there's no schema-level way to say a `normal` draw needs `mean`/`stdev` (or `mean`/`stdev`/`min`/`max`) while a `cauchy` draw needs a different, differently-shaped parameter list (see `schema/predefined-functions.json`'s `distrib` entries). The expected fix in both cases mirrors `Jacobian`'s: one concrete class per variant (e.g. `SumCalculation`/`MeanCalculation`/... per KISAO:0000824 child; `DrawFromNormalDistribution`/`DrawFromCauchyDistribution`/... per distrib function), each with its own `_type` and properly named, properly required attributes instead of a generic `arguments` array or an absent selector. Not yet designed or scoped.
- **Checks that require reading a referenced model or data file are not yet drafted** (e.g. that a task's `outputVariables` names actually exist in the SBML model its `model` points at, or that a `CsvImport`'s named columns exist in its file). `outputs.json`'s `"input-file"` dimension-source entries already anticipate this; each needs its own per-format reader before it can become a rule. Later work.
- **Open design questions carried over verbatim from original:** whether `ModelChange.replaceElements` should be kept in SED2 at all; whether it's acceptable that `OneStepODESimulation` neither tracks nor outputs the independent variable's own final value; a COMBINE-2026 note wanting `AggregationCalculation` to be usable as an objective function (e.g. "scan and return the best").

## 11. Multi-target consistency reminder

Per this project's own working rules: any future design change to the SED2 class model, cross-reference/math syntax, or validation rules must be reflected in **all three** generated libraries (C++, Java, Python) in the same change - this document split does not touch code generation, but any content change that follows from resolving Section 10's open items will.

# SED2 validation rules

Rules here are the ones Design.md's "Validation" section calls for
separately from the JSON Schema pass: things the spec requires that a
schema can't express (they depend on the rest of the document, or on
run-time behavior the schema has no way to see). Each is numbered so code
and tests can refer to it (`ValidationError::code`), and the list grows as
more such rules are found while working through the spec - it is not
meant to be complete yet.

A rule that a JSON Schema *can* express (an attribute's required-ness, its
JSON type, an enum's allowed values) belongs in `spec/sed2.schema.json`
instead, not here.

## V0001 - SIdRef must resolve

Any attribute value that is a reference (a string starting with `#`) must
resolve to an object that actually exists in the document, once its
colon-delimited path is followed from the document root (`SEDDocument::
getSEDReference`).

Status: implemented. `AttributeTypes::validateReference` is the entry
point every generated class's `validate()` calls for each attribute whose
table entry sets `"isRef": true`, across the full class catalog (every
`AbstractTask`/`AbstractOutput` concrete type, not just a vertical
slice). Resolution walks from the attribute's owner up the `SEDBase`
parent chain (`getParent`/`setParent`, wired automatically by codegen's
`owned`/`ownedArray`/`polymorphicList` setters) to the owning
`SEDDocument` (`SEDBase::getSEDDocument`), then calls `SEDDocument::
getSEDReference` on it. See V0003 for what happens when that walk
doesn't reach a document at all. Exercised by `tests/unit/
test_cross_references.cpp`, `test_Report.cpp`, and the per-class-family
test files (`test_simulations.cpp`, `test_tasks_import_data.cpp`,
`test_repeats.cpp`, `test_outputs.cpp`).

One disclosed gap: attributes modeled as a plain `Json`-typed scalar (the
pragmatic simplification used for schema shapes like `AnyValueOrRef` and
`anyOf[object, SIdRef]` - see `codegen/generate_classes.py`'s handling of
`cppType: "Json"`) are not wired to `validateReference`, even when the
JSON value they hold is or contains a reference string. Examples:
`TaskParameter.value`, `Loop.outputVariableMap`, `ModelChange.setValues`.
Recognizing a reference nested inside an arbitrary JSON value is a
different problem from checking one scalar string attribute, and is left
for a future pass.

## V0002 - subvalue accessor plausibility

A reference's trailing dot-accessor (`.model`) or bracket accessor
(`['S1']`, `[3]`, `[0:5]`) must be *plausible*: a dot-accessor must name
something the referenced class actually declares
(`SEDBase::getDeclaredDotAccessors`), and a bracket accessor must at least
be syntactically well-formed. Per the spec (and Design.md's own
"Cross-references" section), what a subvalue accessor actually resolves to
is a run-time quantity - it only exists once the experiment the document
describes is executed - so this can only ever be a plausibility check, not
a resolution to a concrete value or pointer.

A closely related check lives here too: whether a reference with *no*
trailing accessor at all (`"#tasks:task1"`) is itself meaningful
(`SEDBase::isBareReferenceValid`). Most classes' bare reference means "the
whole object," which is fine; a few (e.g. `ModelImport` - only
`"#tasks:task1.model"` means anything, `"#tasks:task1"` on its own does
not, per the spec) declare that their bare reference isn't meaningful, and
`validateReference` warns if one is used anyway.

Status: implemented across the full class catalog. Each generated class's
attribute table sets `"dotAccessors"`/`"bareReferenceValid"` where the UML
spec declares something other than the defaults (no dot-accessors, bare
reference valid) - see `codegen/generate_classes.py`'s handling of those
two table fields. `AttributeTypes::hasSubvalue` implements the accessor
plausibility check itself; `AttributeTypes::validateReference` calls it
for a reference's trailing dot/bracket accessor, and separately checks
`isBareReferenceValid()` when there is no trailing accessor at all. A
resolved object of unrecognized type (`RawElement` - see V0001) skips both
checks, since its declared accessors/bare-reference-validity are unknown,
not "none."

Eighteen of the catalog's 37 classes declare non-default values: the
import/data-manipulation family (`ModelImport`, `ModelChange`,
`ModelElementList`, `StringFormation` - `dotAccessors` plus
`bareReferenceValid: false`, since only their declared subvalue is
meaningful), the simulation family (`ExplicitODESimulation`,
`BoundedODESimulation`, `ExplicitStochasticSimulation`,
`BoundedStochasticSimulation`, `OneStepODE`, `OneStepStochastic`,
`SteadyState`, `FluxBalanceAnalysis` - `dotAccessors: ["model"]`, bare
reference still valid), the repeat/scan family (`Loop`, `Scatter`,
`ParameterScan` - `dotAccessors: ["aggregates", "range", "index"]`,
inherited in the UML sense from `Repeat`, but declared directly per class
since no C++ base class exists for that UML-only grouping), and the
`AbstractOutput` family (`Report`, `Plot2D`, `Plot3D` -
`bareReferenceValid: false` only, per the spec's "may not be used as input
for anything else"). The remaining 19 classes need no table entry - the
defaults already match what the spec (or its silence) implies.

Covered by `tests/unit/test_cross_references.cpp`, including end to end
through real generated classes (`ModelImport`'s declared/undeclared dot
accessor and bare-reference warning, `ExplicitODESimulation`'s valid bare
reference), not just the test-only `ElementWithDotAccessor` subclass used
for the plausibility check in isolation.

Note: `Style` (referenced by `SEDDocument.styles`) has no declared shape
in the spec yet - its own definition says "Placeholder for the Style
class. The spec is incomplete," with no properties and no `_type` of its
own. Documents that use it fall back to `RawElement` (the same path any
unregistered `_type` takes) and validate only as opaque, unrecognized
JSON; no attribute table is written for it until the spec settles.

## V0003 - reference resolution requires a document

An object validated outside a `SEDDocument` - one whose `SEDBase` parent
chain never reaches a root document, because it (or an ancestor) was
never attached to one, e.g. a class constructed standalone in a test -
cannot have its reference-typed attributes resolved one way or the
other: there is nothing for `SEDDocument::getSEDReference` to walk. This
is a limitation of the validation *context*, not a defect in whatever
document (if any) the object will eventually belong to, so `validate()`
reports it as `ValidationSeverity::Info`, distinct from the `Error` a
reference gets when a document *is* reachable but the reference still
doesn't resolve within it.

Status: implemented in `AttributeTypes::validateReference` (the
`doc == nullptr` branch). Exercised directly in `tests/unit/
test_cross_references.cpp` and, end to end through a real generated
class, in `test_Report.cpp`'s `ValidateRequiresData`.

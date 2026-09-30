# ProposedRules.md - reference-target rules for model and AnnotatedData fields

Status: ADOPTED (the shared pair, at your request). `SEDBase-0016` and
`SEDBase-0017` are now in `specsheets/core/SEDBase/v1.0.0/validation/`, the
`x-ref-target` marker is on the 21 fields, `generator/spec.py` reads it, and
`generator/gen_reftype_fixtures.py` generates fixtures for both (131 files).
The rule logic is implemented in Python
(`templates/python/rules/SEDBase-0016.py` and `-0017.py`) and all 131 fixtures
pass, and Java and C++ implement them too. The text below is kept as the design record; the
per-field alternative was not taken.

## The gap

The ref-type rules ("when the value of X is a reference, it must resolve to a
number/boolean/...") only exist for `*OrRef` fields. A field declared as a bare
`SIdRef` today only has a schema rule saying "must be a reference (starts with
#)". Nothing says *what* it must resolve to. So all of these are accepted with
no error:

- `model: "#constants:mynumber"`, or `model: "#tasks:sim1"` (data, not a model)
- `Curve.x: "#tasks:model1.model"` (a model where AnnotatedData is expected)

You confirmed a model is a type like any other, so a model field needs a model.

## Fields affected (21)

Model targets (8):
AbstractSimulation.model, FluxBalanceAnalysis.model, JacobianFull.model,
JacobianReduced.model, ModelChange.inputModel, ModelElementList.model,
ParameterScan.model, SteadyState.model.

AnnotatedData targets (13):
AbstractCurve.x; Curve.y, .xErrorUpper, .xErrorLower, .yErrorUpper,
.yErrorLower, .yFrom, .yTo; Surface.x, .y, .z; RelabelData.input; Report.data.
(Also AggregationCalculation.input, but see "Related findings" - it is typed
`any`, not `SIdRef`.)

## Proposal: one marker plus two shared rules

Rather than 21 near-identical per-field rules, follow the SEDBase precedent
(SEDBase-0005 through -0015 already apply "to every SIdRef/OrRef field,
regardless of class"):

1. Add a generator-only marker next to each affected field's `SIdRef`, like the
   existing `x-math`: `"x-ref-target": "model"` or `"x-ref-target":
   "annotatedData"`. JSON Schema validators ignore it.
2. Add two rules to `specsheets/core/SEDBase/v1.0.0/validation/`:

`SEDBase-0016.md`
```
---
id: SEDBase-0016
rule: "A reference required to resolve to a model must resolve to a model."
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to {resolved-value}, not a model."
severity: error
status: active
check: handwritten
---

Applies to every field carrying x-ref-target: "model". A reference resolves to
a model only when it names a task output whose outputs.json entry has
"type": "model" (for example #tasks:model1.model, or #tasks:ss1.model when the
task exports one). Constants are never models. A reference that does not
resolve at all (SEDBase-0006), or that uses an accessor its target does not
declare (SEDBase-0008), fires those rules instead, not this one.
{resolved-value} is a description of what it did resolve to, such as
"a number", "an array", or "a annotatedData value".
```

`SEDBase-0017.md`
```
---
id: SEDBase-0017
rule: "A reference required to resolve to AnnotatedData must resolve to AnnotatedData."
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to {resolved-value}, not AnnotatedData."
severity: error
status: active
check: handwritten
---

Applies to every field carrying x-ref-target: "annotatedData". AnnotatedData
is an n-dimensional block of values, labeled or not. A reference resolves to
it when it names (a) a constant whose value is a scalar (number, string,
boolean) or an array (unlabeled AnnotatedData), or (b) a task output whose outputs.json entry has "type":
"annotatedData" or "stringList". A model is not AnnotatedData, and neither is
an object constant. Unresolvable references and bad accessors fire SEDBase-0006
and SEDBase-0008 instead.
```

(The numbers 0016 and 0017 are the next free ones in SEDBase.)

### What resolves to what

| Reference target | model field | AnnotatedData field |
|---|---|---|
| `#tasks:model1.model` | OK | error (SEDBase-0017) |
| `#tasks:sim1` (its `[id]` data) | error (SEDBase-0016) | OK |
| `#tasks:sim1.model` where the task exports a model | OK | error |
| `#constants:` array | error | OK |
| `#constants:` number/string/boolean | error | OK (decided: a scalar is AnnotatedData) |
| `#constants:` object | error | error |
| `#outputs:...` | SEDBase-0007 | SEDBase-0007 |

## Alternative: per-field rules

If you prefer the existing one-rule-per-field style (the `x-rule-id` array
form, second element the ref-type rule), the next free IDs would be:

- model: AbstractSimulation-0009, FluxBalanceAnalysis-0009, JacobianFull-0004,
  JacobianReduced-0004, ModelChange-0012, ModelElementList-0012,
  ParameterScan-0007, SteadyState-0007
- AnnotatedData: AbstractCurve-0009, Curve-0013 through -0019 (y and the six
  error/from/to fields), Surface-0013 through -0015, RelabelData-0007,
  Report-0004

Each would read "When the value of <field> of a <Class> is a reference, it must
be a reference to a model / AnnotatedData", with the same message shape as the
other ref-type rules. Same behavior, 21 files instead of 2, and the generator
would derive them from a field-level marker just the same. I recommend the
shared pair.

## Related findings (not new rules, but you will want to know)

- **Plot-0008 looks stale.** Its file says `yAxis` of a `Plot` is "one of
  right/left or a reference", but `Plot.yAxis` in the schema is an `Axis`
  object (Plot-0007, its neighbor, says so for `xAxis`). The right/left
  enum belongs to `AbstractCurve.yAxis`. No fixture can be generated for
  Plot-0008 until one of the two is fixed; 86 of the 87 ref-type rules have
  fixtures.
- **SteadyState.model has no x-rule-id**, so it has no numbered "must be a
  reference" rule, unlike every other model field.
- **AggregationCalculation.input is typed `any`**, not `SIdRef`, so nothing
  requires it to be a reference at all. It reads like an AnnotatedData field.
- **Style targets**: `style` on Axis, AbstractCurve, and Surface should
  resolve to a `#styles:` entry. `Style` is still an unspecified placeholder, so
  I left this out; it fits the same marker (`x-ref-target: "style"`) later.
- **Fixed: `validate()` crashed on a reference into `constants` from a Loop.**
  `LoopVariable-0004` and `Repeat-0008`/`-0009` called `.get_parent()` on
  whatever a reference resolved to, but a constant resolves to a bare JSON value
  (a list, number, ...), so `subsequentValues: "#constants:myNumberArray"`
  raised `AttributeError`. Now a non-element target simply counts as "not one of
  my own children" and the rule fires. Regression fixtures are in
  `fixtures/handwritten/`. (I first blamed `Repeat-0003`'s dict field; the
  cause was my test host's loop variable.)

## Open questions

1. (Settled) A scalar constant counts as AnnotatedData; an object constant does
   not.
2. Should a `LoopVariable` that holds a model count as a model target? Not
   covered here.

## Fixtures for these rules (generated)

In `fixtures/generated/ref-type/`, named
`SEDBase-0016-<fail|pass>-<count>-<Class>-<field>-<case>.sed2.json`:
- model field: fails for a number constant, an array constant, an object
  constant, and a simulation's data output (`#tasks:sim1`); pass for
  `#tasks:model1.model`;
- AnnotatedData field: fails for `#tasks:model1.model` and an object constant;
  passes for an array, a string array, a number, a string, and a simulation's
  data output.

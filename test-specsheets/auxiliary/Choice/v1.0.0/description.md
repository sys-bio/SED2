# Choice

**Category:** auxiliary
**Schema:** [`schema.json`](./schema.json) + [`common.schema.json`](./common.schema.json) (`ChoiceCommon`) + [`inline.schema.json`](./inline.schema.json) (`ChoiceInline`)

## What it does

Trimmed analog of `specsheets/tasks/Range`/`RangeInline`: a class that is both directly instantiable on its own (`_type` "choice") and the root of a further subclass, `WeightedChoice` - the "Common mixin" pattern from Design.md's Classes section (`ChoiceCommon` gets its own file, separate from `schema.json`'s own `Choice` entry, because `Choice` can't simultaneously be the concrete class and the union placeholder). `inline.schema.json`'s `ChoiceInline` is the generated-`oneOf` union used wherever a `Choice` or `WeightedChoice` appears as a named embedded child rather than a top-level task.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `label` | StringOrRef | no | inherited via `ChoiceCommon` |

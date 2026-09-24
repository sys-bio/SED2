# WeightedChoice

**Category:** auxiliary
**Schema:** [`schema.json`](./schema.json)

## What it does

A `Choice` subtype (`_type` "weightedChoice") composing `ChoiceCommon` directly, adding a required `weight`. Terminal leaf - unlike `Choice` itself, nothing subclasses `WeightedChoice`, so it needs no `common.schema.json`/`inline.schema.json` of its own (see the note on this in Design.md's Classes section).

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `label` | StringOrRef | no | inherited via `ChoiceCommon` |
| `weight` | NumberOrRef | yes | |

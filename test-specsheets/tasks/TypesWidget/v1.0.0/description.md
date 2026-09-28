# TypesWidget

**Category:** tasks
**Schema:** [`schema.json`](./schema.json)

## What it does

Leaf branch of `AbstractWidget` (`_type` "typesWidget") that flatly composes `TestBaseFields` + `AbstractWidgetCommon`. Every attribute is optional and exists only to give the generator one field of each type it classifies that no other test-specsheets/ class exercised: `any`, `BooleanOrRef`, `IntegerOrRef`, `ArrayOrRef`, `DictOrRef`, `ref-class`, `ref-discriminator`, and `any-dict`. The "Generator kind" column below is the `FieldType.kind` that `generator/spec.py` assigns.

## Attributes

| Attribute | Type | Generator kind | Required | Notes |
|---|---|---|---|---|
| `anyValue` | AnyValueOrRef | any | no | any JSON value, including null |
| `enabled` | BooleanOrRef | BooleanOrRef | no | |
| `count` | IntegerOrRef | IntegerOrRef | no | |
| `items` | ArrayOrRef | ArrayOrRef | no | array of anything, or a reference |
| `settings` | DictOrRef | DictOrRef | no | object of anything, or a reference |
| `primaryNote` | Note | ref-class | no | one embedded `Note` |
| `report` | AbstractReport | ref-discriminator | no | one embedded report branch, dispatched on `_type` |
| `extras` | map<SId, AnyValueOrRef> | any-dict | no | keys must be SIds; values unconstrained |

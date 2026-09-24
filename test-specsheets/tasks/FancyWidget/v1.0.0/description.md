# FancyWidget

**Category:** tasks
**Schema:** [`schema.json`](./schema.json)

## What it does

Leaf branch of `AbstractWidget` that flatly composes `TestBaseFields` + `AbstractWidgetCommon` + `WidgetOptions` (see the "flat-listing" convention in `core-spec.md` Section 8), exercising a class with more than one composed-in mixin. `_type` "fancyWidget", one required attribute plus the optional `retries`/`timeoutSeconds` it picks up from `WidgetOptions`.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `value` | StringOrRef | yes | |
| `retries` | integer | no | inherited from `WidgetOptions` |
| `timeoutSeconds` | number | no | inherited from `WidgetOptions` |

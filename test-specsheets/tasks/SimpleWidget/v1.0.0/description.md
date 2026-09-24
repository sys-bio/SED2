# SimpleWidget

**Category:** tasks
**Schema:** [`schema.json`](./schema.json)

## What it does

A plain leaf branch of `AbstractWidget` - flatly composes `TestBaseFields` + `AbstractWidgetCommon`, `_type` "simpleWidget", one required attribute. The un-extended counterpart to `FancyWidget`, which additionally composes `WidgetOptions`. Also the target of the `namespaces/acme/updated/tasks/SimpleWidget` example fragment.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `value` | StringOrRef | yes | |

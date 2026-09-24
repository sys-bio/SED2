# WidgetOptions

**Category:** tasks
**Schema:** [`schema.json`](./schema.json)

## What it does

Standalone schema-only mixin with no `oneOf` of its own - not itself a discriminated branch, and never referenced as a field type by anything else, only composed via `allOf` into whichever concrete classes opt in (here, `FancyWidget`). Trimmed analog of `specsheets/tasks/AbstractSimulation` - see Design.md's "standalone schema-only mixins" exception in `core-spec.md` Section 8.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `retries` | integer | no | >= 0 |
| `timeoutSeconds` | number | no | > 0 |

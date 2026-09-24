# acme@AcmeWidget (namespace `new/` example)

**Category:** tasks (namespace: `acme`, `new/`)
**Schema:** [`schema.json`](./schema.json)

## What it does

Example `new/` namespace class (see Design.md's Namespaces section): a wholly new task type the `acme` namespace defines from scratch, composing `TestBaseFields` + `AbstractWidgetCommon` exactly like a built-in `AbstractWidget` branch would, discovered by the generator's scan the same way. Its `_type` is the namespaced form `acme@acmeWidget`, and it declares one namespace-prefixed attribute, `acme@acmeLevel`.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `acme@acmeLevel` | NumberOrRef | yes | namespace-prefixed |

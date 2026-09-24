# acme updates to SimpleWidget (namespace `updated/` example)

**Category:** tasks (namespace: `acme`, `updated/`)
**Schema:** [`schema.json`](./schema.json)

## What it does

Example `updated/` namespace fragment (see Design.md's Namespaces section): the `acme` namespace adds one namespace-prefixed attribute, `acme@priority`, to the existing `tasks/SimpleWidget` class. This file declares only the addition - the generator assembles it with `SimpleWidget`'s own schema via `allOf` at generate time; this fragment is never hand-composed with the base class itself, and `tasks/SimpleWidget/v1.0.0/schema.json` is never edited to know about it.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `acme@priority` | NumberOrRef | no | namespace-prefixed addition to `SimpleWidget` |

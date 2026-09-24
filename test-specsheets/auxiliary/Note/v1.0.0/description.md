# Note

**Category:** auxiliary
**Schema:** [`schema.json`](./schema.json)

## What it does

A simple helper object with no `_type` of its own - never a discriminated branch, only ever embedded as a child field of some other class (compare `specsheets/auxiliary/TaskParameter`/`WorkingAlgorithm`). Not currently referenced by any other fixture class here; included to exercise the plain-helper-class pattern on its own.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `text` | StringOrRef | yes | |

## Outputs

Not independently referenceable - an embedded helper object only.

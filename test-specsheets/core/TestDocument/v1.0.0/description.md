# TestDocument

**Category:** core
**Schema:** [`schema.json`](./schema.json)

## What it does

Root class of the test-specsheets/ fixture tree, trimmed analog of `specsheets/core/SEDDocument`: a `version` string plus `widgets` (a dict of `AbstractWidget` branches) and `reports` (a dict of `AbstractReport` branches). Exercises the generator's handling of a document-level class with dictionary-of-discriminated-union fields.

## Attributes

| Attribute | Type | Required | Notes |
|---|---|---|---|
| `version` | string | yes | `v#.#.#` |
| `widgets` | map<SId, AbstractWidget> | no | |
| `reports` | map<SId, AbstractReport> | no | |

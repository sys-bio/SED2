# Types

*(No UML class box of its own - shared `$defs` only. Trimmed analog of `specsheets/core/Types`.)*

**Category:** core
**Schema:** [`schema.json`](./schema.json)

## What this covers

A small, self-contained set of primitive/reference-helper types (`SId`, `SIdRef`, `StringOrRef`, `NumberOrRef`) reused across `test-specsheets/`, the same way `core/Types` is reused across `specsheets/`. This tree is a synthetic generator-test fixture - see Design.md's Specification Assembly section - so the type set is deliberately trimmed to whatever the fixture classes actually need, not a full mirror of `core/Types`.

## Attributes

Not attributes of a class - bundles shared `$defs` for use via `$ref` from other test-specsheets/ Data Sheets.

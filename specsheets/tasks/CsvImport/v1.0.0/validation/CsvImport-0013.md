---
id: CsvImport-0013
rule: When the value of ncols of a CsvImport is a reference, it must be a reference to a positive integer.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a positive integer."
severity: error
status: active
---

`ncols` is `PositiveIntegerOrRef`: when the value is a reference, it must resolve to a positive integer.

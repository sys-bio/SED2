---
id: CsvImport-0015
rule: When the value of nrows of a CsvImport is a reference, it must be a reference to a positive integer.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a positive integer."
severity: error
status: active
check: ref-type
---

`nrows` is `PositiveIntegerOrRef`: when the value is a reference, it must resolve to a positive integer.

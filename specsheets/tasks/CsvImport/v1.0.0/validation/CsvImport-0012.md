---
id: CsvImport-0012
rule: When the value of ncols of a CsvImport is provided directly, it must be a positive integer.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a positive integer."
severity: error
status: active
check: schema
---

`ncols` is `PositiveIntegerOrRef`: the value, when not a reference, must be a positive integer.

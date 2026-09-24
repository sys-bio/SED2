---
id: CsvImport-0008
rule: When the value of headers of a CsvImport is provided directly, it must be a boolean.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a boolean."
severity: error
status: active
---

`headers` is `BooleanOrRef`: the value, when not a reference, must be a boolean.

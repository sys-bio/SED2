---
id: CsvImport-0006
rule: When the value of separator of a CsvImport is provided directly, it must be a string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a string."
severity: error
status: active
check: schema
---

`separator` is `StringOrRef`: the value, when not a reference, must be a string.

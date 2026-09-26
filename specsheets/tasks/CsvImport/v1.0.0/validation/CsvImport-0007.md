---
id: CsvImport-0007
rule: When the value of separator of a CsvImport is a reference, it must be a reference to a string.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a string."
severity: error
status: active
check: ref-type
---

`separator` is `StringOrRef`: when the value is a reference, it must resolve to a string.

---
id: CsvImport-0010
rule: When the value of columnNames of a CsvImport is provided directly, it must be an array of strings.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of strings."
severity: error
status: active
check: schema
---

`columnNames` is `ListOfStringsOrRef`: the value, when not a reference, must be an array of strings.

---
id: CsvImport-0003
rule: When the value of location of a CsvImport is a reference, it must be a reference to a URI string.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a URI string."
severity: error
status: active
---

`location` is `URIOrRef`: when the value is a reference, it must resolve to a URI string.

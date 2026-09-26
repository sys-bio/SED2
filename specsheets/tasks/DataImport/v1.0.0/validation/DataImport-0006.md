---
id: DataImport-0006
rule: When the value of format of a DataImport is a reference, it must be a reference to a URI string.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a URI string."
severity: error
status: active
check: ref-type
---

`format` is `URIOrRef`: when the value is a reference, it must resolve to a URI string.

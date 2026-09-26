---
id: DataImport-0005
rule: When the value of format of a DataImport is provided directly, it must be a URI string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a URI string."
severity: error
status: active
check: schema
---

`format` is `URIOrRef`: the value, when not a reference, must be a URI string.

---
id: ModelImport-0002
rule: When the value of location of a ModelImport is provided directly, it must be a URI string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a URI string."
severity: error
status: active
---

`location` is `URIOrRef`: the value, when not a reference, must be a URI string.

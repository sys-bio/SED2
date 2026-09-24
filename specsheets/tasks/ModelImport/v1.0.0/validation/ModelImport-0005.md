---
id: ModelImport-0005
rule: When the value of language of a ModelImport is provided directly, it must be a URN string.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not a URN string."
severity: error
status: active
---

`language` is `URNOrRef`: the value, when not a reference, must be a URN string.

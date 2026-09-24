---
id: ModelImport-0006
rule: When the value of language of a ModelImport is a reference, it must be a reference to a URN string.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not a URN string."
severity: error
status: active
---

`language` is `URNOrRef`: when the value is a reference, it must resolve to a URN string.

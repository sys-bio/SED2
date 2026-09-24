---
id: ModelElementList-0003
rule: When the value of includeElements of a ModelElementList is provided directly, it must be an array of strings.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of strings."
severity: error
status: active
---

`includeElements` is `ListOfStringsOrRef`: the value, when not a reference, must be an array of strings.

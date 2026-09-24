---
id: ModelElementList-0007
rule: When the value of excludeElements of a ModelElementList is provided directly, it must be an array of strings.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of strings."
severity: error
status: active
---

`excludeElements` is `ListOfStringsOrRef`: the value, when not a reference, must be an array of strings.

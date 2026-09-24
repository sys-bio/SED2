---
id: ModelElementList-0010
rule: When the value of excludeTypes of a ModelElementList is a reference, it must be a reference to an array of strings.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an array of strings."
severity: error
status: active
---

`excludeTypes` is `ListOfStringsOrRef`: when the value is a reference, it must resolve to an array of strings.

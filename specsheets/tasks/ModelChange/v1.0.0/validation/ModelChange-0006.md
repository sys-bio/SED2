---
id: ModelChange-0006
rule: When the value of removeElements of a ModelChange is a reference, it must be a reference to an array of strings.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an array of strings."
severity: error
status: active
check: ref-type
---

`removeElements` is `ListOfStringsOrRef`: when the value is a reference, it must resolve to an array of strings.

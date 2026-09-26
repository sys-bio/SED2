---
id: RelabelData-0004
rule: When the value of labels of a RelabelData is provided directly, it must be an array of strings.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of strings."
severity: error
status: active
check: schema
---

`labels` is `ListOfStringsOrRef`: the value, when not a reference, must be an array of strings.

---
id: StringFormation-0003
rule: When the value of concatenate of a StringFormation is a reference, it must be a reference to an array of values.
message: "Attribute '{attr}' of {class} '{id}' is the reference '{value}', which resolves to '{resolved-value}', not an array of values."
severity: error
status: active
---

`concatenate` is `ListOfAnyOrRef`: when the value is a reference, it must resolve to an array of values.

---
id: StringFormation-0002
rule: When the value of concatenate of a StringFormation is provided directly, it must be an array of values.
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which is not an array of values."
severity: error
status: active
check: schema
---

`concatenate` is `ListOfAnyOrRef`: the value, when not a reference, must be an array of values.

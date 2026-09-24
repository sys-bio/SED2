---
id: StringFormation-0004
rule: The _type attribute of a StringFormation must be "stringFormation".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `StringFormation` it must always equal `"stringFormation"`.

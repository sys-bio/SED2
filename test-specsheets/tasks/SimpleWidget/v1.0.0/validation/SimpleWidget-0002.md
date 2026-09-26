---
id: SimpleWidget-0002
rule: The _type attribute of a SimpleWidget must be "simpleWidget".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `SimpleWidget` it must always equal `"simpleWidget"`.

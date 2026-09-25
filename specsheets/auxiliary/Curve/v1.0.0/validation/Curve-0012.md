---
id: Curve-0012
rule: The _type attribute of a Curve must be "curve".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `Curve` it must always equal `"curve"`.

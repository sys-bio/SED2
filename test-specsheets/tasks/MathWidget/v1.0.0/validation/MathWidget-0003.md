---
id: MathWidget-0003
rule: The _type attribute of a MathWidget must be "mathWidget".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
check: schema
---

`_type` is the discriminator field. For `MathWidget` it must always equal `"mathWidget"`.

---
id: Scatter-0003
rule: The _type attribute of a Scatter must be "scatter".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `Scatter` it must always equal `"scatter"`.

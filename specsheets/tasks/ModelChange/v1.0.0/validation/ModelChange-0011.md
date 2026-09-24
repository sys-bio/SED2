---
id: ModelChange-0011
rule: The _type attribute of a ModelChange must be "modelChange".
message: "Attribute '{attr}' of {class} '{id}' has value '{value}', which does not match the required value '{allowed}'."
severity: error
status: active
---

`_type` is the discriminator field. For `ModelChange` it must always equal `"modelChange"`.
